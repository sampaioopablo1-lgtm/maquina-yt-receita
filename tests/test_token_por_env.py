"""O token do canal pelo ENV — o que tira a publicacao da minha mao.

Estes testes travam a ordem (env antes do REST), a recusa de canal errado e as
duas mensagens de erro. A recusa e a que mais importa: publicar no canal errado
já aconteceu uma vez, em 14/08/2026, e um `YT_TOKEN_JSON` genérico é
exatamente o jeito de fazer isso de novo sem perceber.
"""
import json

import pytest

import publicar


def test_nome_do_env_segue_a_convencao_do_legendar_yml():
    assert publicar._env_do_canal("epomeno-epipedo") == "YT_TOKEN_EPOMENO_EPIPEDO"
    assert publicar._env_do_canal("labtreinamento") == "YT_TOKEN_LABTREINAMENTO"
    assert publicar._env_do_canal("kolejny-poziom") == "YT_TOKEN_KOLEJNY_POZIOM"


def test_env_vence_o_rest(monkeypatch):
    """Com o secret no lugar, nem olha para o Supabase.

    Se alguem invertesse a ordem, o 402 voltaria a derrubar a publicacao no
    runner e ninguem descobriria antes de um render inteiro.
    """
    def _explode(*a, **k):
        raise AssertionError("tentou o REST tendo o env")

    monkeypatch.setattr(publicar, "_req", _explode)
    monkeypatch.setenv("YT_TOKEN_LABTREINAMENTO",
                       json.dumps({"refresh_token": "r", "client_id": "c"}))
    tok = publicar.token_do_canal("labtreinamento", "https://x", "k")
    assert tok["refresh_token"] == "r"


def test_yt_token_json_serve_de_reserva(monkeypatch):
    monkeypatch.setattr(publicar, "_req", lambda *a, **k: pytest.fail("usou REST"))
    monkeypatch.setenv("YT_TOKEN_JSON", json.dumps({"refresh_token": "r"}))
    assert publicar.token_do_canal("kolejny-poziom", "", "")["refresh_token"] == "r"


def test_token_que_nomeia_OUTRO_canal_e_recusado(monkeypatch):
    """A trava contra o erro de 14/08. Não publique; recuse."""
    monkeypatch.setenv("YT_TOKEN_JSON",
                       json.dumps({"refresh_token": "r", "canal": "setiap-level"}))
    with pytest.raises(SystemExit) as e:
        publicar.token_do_canal("labtreinamento", "", "")
    assert "setiap-level" in str(e.value) and "labtreinamento" in str(e.value)


def test_secret_truncado_falha_dizendo_que_e_o_secret(monkeypatch):
    monkeypatch.setenv("YT_TOKEN_LABTREINAMENTO", '{"refresh_token": "r"')
    with pytest.raises(SystemExit) as e:
        publicar.token_do_canal("labtreinamento", "", "")
    assert "YT_TOKEN_LABTREINAMENTO" in str(e.value)


def test_token_sem_refresh_token_falha_antes_de_subir(monkeypatch):
    monkeypatch.setenv("YT_TOKEN_LABTREINAMENTO", json.dumps({"client_id": "c"}))
    with pytest.raises(SystemExit) as e:
        publicar.token_do_canal("labtreinamento", "", "")
    assert "refresh_token" in str(e.value)


def test_sem_env_e_sem_supabase_a_mensagem_nomeia_AS_DUAS_portas(monkeypatch):
    monkeypatch.delenv("YT_TOKEN_JSON", raising=False)
    monkeypatch.delenv("YT_TOKEN_LABTREINAMENTO", raising=False)
    with pytest.raises(SystemExit) as e:
        publicar.token_do_canal("labtreinamento", "", "")
    msg = str(e.value)
    assert "YT_TOKEN_LABTREINAMENTO" in msg and "SUPABASE_URL" in msg


def test_sem_env_cai_no_rest(monkeypatch):
    monkeypatch.delenv("YT_TOKEN_JSON", raising=False)
    monkeypatch.delenv("YT_TOKEN_LABTREINAMENTO", raising=False)

    class _R:
        def read(self):
            return json.dumps([{"valor": {"refresh_token": "do-rest"}}]).encode()

    monkeypatch.setattr(publicar, "_req", lambda *a, **k: _R())
    tok = publicar.token_do_canal("labtreinamento", "https://x", "k")
    assert tok["refresh_token"] == "do-rest"
