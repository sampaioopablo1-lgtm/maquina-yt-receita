"""O modo ponte publica sem a API do Supabase — e sem afrouxar as travas.

Medido em 25/08/2026: a organizacao entrou em restricao de Fair Use e o
gateway do Supabase passou a devolver 402 em TUDO. Nao foi so o Storage —
PostgREST e Edge Functions caem junto (run 32805083587 bate nas tres portas e
as tres respondem 402). O runner do frota.yml le o token do canal e grava o
registro por PostgREST, entao a frota parou inteira.

A tentacao obvia era um atalho: publicar pulando as duas travas anti-duplicata
"so desta vez". Seria repetir de proposito o defeito que ja custou tres
duplicatas em tres canais em 17/08. O que o modo ponte faz e outra coisa —
troca a FONTE do estado, nao a conferencia. Mesmo criterio, mesmo recuse, os
dados chegando por arquivo em vez de por rede. E a mesma ideia que o
`orquestra.py --dados` usa desde 13/08.

Estes testes existem para garantir que a trava que roda quando a rede cai
recusa exatamente o que a outra recusaria. E justamente ela que ninguem
exercita no dia a dia.
"""

import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import publicar as P  # noqa: E402


SPEC = {
    "pacote": "agla-level-006",
    "slug": "agla-level-006",
    "longo": [{}] * 74,
    "short": [{}] * 4,
}
COPY = {
    "titulo": "EPFO 3.0: ATM se 50%, UPI se 75%",
    "descricao": "abre\n\n0:00 Intro\n2:10 A conta\n11:28 O que fazer",
}


# --------------------------------------------------- a trava por titulo

def test_a_trava_offline_recusa_o_mesmo_titulo():
    estado = {"titulos_no_ar": [
        {"titulo": "EPFO 3.0: ATM se 50%, UPI se 75%", "formato": "longo",
         "youtube_id": "abc123", "pacote": "outro-nome-de-rodada"}]}
    iguais = P._iguais_no_estado(estado, "EPFO 3.0: ATM se 50%, UPI se 75%")
    assert [l["youtube_id"] for l in iguais] == ["abc123"]


def test_a_trava_offline_ignora_caixa_e_espaco_como_a_online():
    """Mesmo criterio dos dois lados, ou a ponte vira uma trava mais frouxa."""
    estado = {"titulos_no_ar": [
        {"titulo": "  epfo 3.0: ATM SE 50%, upi se 75%  ", "formato": "longo",
         "youtube_id": "abc123", "pacote": "p"}]}
    assert P._iguais_no_estado(estado, "EPFO 3.0: ATM se 50%, UPI se 75%")


def test_a_trava_offline_libera_titulo_diferente():
    estado = {"titulos_no_ar": [
        {"titulo": "Outro video inteiramente", "formato": "longo",
         "youtube_id": "abc123", "pacote": "p"}]}
    assert P._iguais_no_estado(estado, "EPFO 3.0: ATM se 50%, UPI se 75%") == []


def test_titulo_vazio_nao_casa_com_nada():
    """Sem titulo a trava nao pode 'casar com o primeiro que achar'.

    O modo de falha ruim aqui e o falso POSITIVO: segurar publicacao boa por
    causa de um copy que ainda nao tem titulo.
    """
    estado = {"titulos_no_ar": [{"titulo": "", "formato": "longo",
                                 "youtube_id": "x", "pacote": "p"}]}
    assert P._iguais_no_estado(estado, "") == []
    assert P._iguais_no_estado(estado, None) == []


def test_estado_sem_a_chave_nao_estoura():
    """Arquivo de estado incompleto nao pode virar traceback no runner."""
    assert P._iguais_no_estado({}, "qualquer coisa") == []


# ------------------------------------------------------ o registro em arquivo

def test_registro_em_arquivo_traz_as_mesmas_linhas(tmp_path, monkeypatch):
    def nunca(*a, **k):
        raise AssertionError("o modo ponte nao pode tocar no PostgREST")

    monkeypatch.setattr(P, "_req", nunca)
    json.dump([10.0] * 74, open(tmp_path / "tempos.json", "w"))
    destino = tmp_path / "registro.json"

    linhas = P.registrar({"short": "sSHORT", "longo": "vLONGO"},
                         SPEC, COPY, str(tmp_path), "agla-level",
                         "https://sb", "k", registro_json=str(destino))

    gravado = json.load(open(destino))
    assert gravado["canal"] == "agla-level"
    assert gravado["pacote"] == "agla-level-006"
    por_formato = {l["formato"]: l for l in gravado["linhas"]}
    assert por_formato["longo"]["youtube_id"] == "vLONGO"
    assert por_formato["shorts"]["youtube_id"] == "sSHORT"
    assert por_formato["longo"]["cenas"] == 74
    assert gravado["linhas"] == linhas


def test_registro_em_arquivo_grava_supabase_url_nulo(tmp_path, monkeypatch):
    """Sem Storage alcancavel, link montado por convencao seria mentira.

    A `_existe` foi escrita justamente para nao gravar URL que aponta para
    nada. No modo ponte o gateway devolve 402 ate no HEAD, entao a conferencia
    nem chega a acontecer — e o valor honesto e NULL.
    """
    monkeypatch.setattr(P, "_req", lambda *a, **k: (_ for _ in ()).throw(
        AssertionError("nao deve haver rede no modo ponte")))
    json.dump([10.0] * 74, open(tmp_path / "tempos.json", "w"))
    destino = tmp_path / "registro.json"
    P.registrar({"short": "s", "longo": "v"}, SPEC, COPY, str(tmp_path),
                "agla-level", "https://sb", "k", registro_json=str(destino))
    for linha in json.load(open(destino))["linhas"]:
        assert linha["supabase_url"] is None


def test_sem_publicacao_nao_grava_arquivo(tmp_path):
    destino = tmp_path / "registro.json"
    json.dump([10.0] * 74, open(tmp_path / "tempos.json", "w"))
    assert P.registrar({}, SPEC, COPY, str(tmp_path), "agla-level",
                       "https://sb", "k", registro_json=str(destino)) == []
    assert not destino.exists()


# ------------------------------------------------------------ os argumentos

def _rodar(argv, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["publicar.py"] + argv)
    with pytest.raises(SystemExit) as e:
        P.main()
    return str(e.value)


def test_ponte_pela_metade_e_recusada(monkeypatch, tmp_path):
    """--access-token sozinho deixaria as duas travas cegas."""
    spec = tmp_path / "spec.json"
    json.dump(SPEC, open(spec, "w"))
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    msg = _rodar([str(spec), "--canal", "agla-level", "--idioma", "hi",
                  "--access-token", "ya29.x"], monkeypatch)
    assert "MODO PONTE incompleto" in msg


def test_sem_ponte_e_sem_ambiente_diz_o_que_fazer(monkeypatch, tmp_path):
    spec = tmp_path / "spec.json"
    json.dump(SPEC, open(spec, "w"))
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    msg = _rodar([str(spec), "--canal", "agla-level", "--idioma", "hi"],
                 monkeypatch)
    assert "AMBIENTE" in msg and "modo ponte" in msg


def test_a_trava_por_pacote_barra_pelo_estado_em_arquivo(monkeypatch, tmp_path):
    """A prova de que a ponte NAO e um atalho para republicar."""
    spec = tmp_path / "spec.json"
    json.dump(SPEC, open(spec, "w"))
    estado = tmp_path / "estado.json"
    json.dump({"ja_publicado": {"longo": "jaEstaNoAr"}, "titulos_no_ar": []},
              open(estado, "w"))
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    msg = _rodar([str(spec), "--canal", "agla-level", "--idioma", "hi",
                  "--access-token", "ya29.x", "--estado-json", str(estado)],
                 monkeypatch)
    assert "JA ESTA no ar" in msg and "jaEstaNoAr" in msg
