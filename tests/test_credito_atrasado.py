"""O credito que entra no video velho tem de ser o MESMO que entra no novo.

Duas redacoes do mesmo credito no mesmo canal e pior que uma so: quem olha nao
sabe qual e a certa, e a proxima correcao passa a ter dois alvos. Por isso o
`credito_atrasado.credito` e cobrado contra o `copy_md.credito_trilha`, que e a
funcao que a esteira usa de verdade.

E o segundo grupo prende a trava que evita o estrago classico deste tipo de
script: `videos.update` exige o snippet INTEIRO, entao mandar so a descricao
APAGA titulo, tags e categoria de todos os videos tocados.
"""

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import credito_atrasado as C  # noqa: E402


# ---------------------------------------------- o texto nao pode divergir

def test_o_texto_e_o_mesmo_da_esteira(tmp_path, monkeypatch):
    """Se `copy_md.credito_trilha` mudar de redacao, este teste cai junto."""
    import copy_md

    (tmp_path / "Wholesome.mp3").write_bytes(b"\xff\xfb\x00")
    monkeypatch.setattr(copy_md, "TRILHA_DIR", str(tmp_path))
    monkeypatch.setattr(copy_md, "TRILHAS_VALIDAS", {"Wholesome"})
    esperado = copy_md.credito_trilha("kolejny-poziom", registrada="Wholesome")
    assert C.credito("Wholesome") == esperado


def test_underscore_do_arquivo_vira_espaco_no_credito():
    """Deliberate_Thought.mp3 se chama "Deliberate Thought" no credito."""
    assert "Deliberate Thought by Kevin MacLeod" in C.credito("Deliberate_Thought")
    assert "_" not in C.credito("Deliberate_Thought")


def test_o_credito_traz_a_url_da_licenca():
    assert "creativecommons.org/licenses/by/4.0/" in C.credito("Inspired")


# ------------------------------------------------ quem ja credita fica quieto

def test_reconhece_credito_existente_pela_url_e_nao_pelo_nome():
    """Nome de faixa muda por canal; a URL da licenca nao muda nunca."""
    assert C.ja_credita("bla\n\n" + C.credito("Inspired"))
    assert C.ja_credita("http://creativecommons.org/licenses/by/4.0/")
    assert not C.ja_credita("Music: Inspired by Kevin MacLeod")
    assert not C.ja_credita("")
    assert not C.ja_credita(None)


# ------------------------------------- o snippet inteiro, nunca so a descricao

class _Falso:
    """Dubla `_req`: guarda o que seria enviado em vez de falar com a rede."""

    def __init__(self, snippet):
        self.snippet, self.enviado = snippet, None

    def __call__(self, url, data=None, method=None, headers=None):
        if method == "PUT":
            self.enviado = json.loads(data.decode())
            return _Corpo("{}")
        return _Corpo(json.dumps({"items": [{"snippet": self.snippet}]}))


class _Corpo:
    def __init__(self, txt):
        self.txt = txt

    def read(self):
        return self.txt.encode()


def _snippet(desc="descricao antiga"):
    return {"title": "Titulo Original", "description": desc,
            "tags": ["a", "b"], "categoryId": "27",
            "defaultLanguage": "pl", "defaultAudioLanguage": "pl"}


def test_grava_o_snippet_inteiro(monkeypatch):
    """O modo de falha caro: PUT com so a descricao apaga titulo e tags."""
    falso = _Falso(_snippet())
    monkeypatch.setattr(C, "_req", falso)
    assert C.consertar("tok", "abc", "Wholesome") == "creditado"
    enviado = falso.enviado["snippet"]
    assert enviado["title"] == "Titulo Original"
    assert enviado["tags"] == ["a", "b"]
    assert enviado["categoryId"] == "27"
    assert enviado["defaultLanguage"] == "pl"
    assert "creativecommons.org/licenses" in enviado["description"]
    assert enviado["description"].startswith("descricao antiga")


def test_nao_grava_quando_ja_credita(monkeypatch):
    falso = _Falso(_snippet("ja tem\n\n" + C.credito("Wholesome")))
    monkeypatch.setattr(C, "_req", falso)
    assert C.consertar("tok", "abc", "Wholesome") == "ja creditava"
    assert falso.enviado is None, "nao pode reescrever quem ja esta certo"


def test_modo_seco_nao_grava(monkeypatch):
    falso = _Falso(_snippet())
    monkeypatch.setattr(C, "_req", falso)
    r = C.consertar("tok", "abc", "Wholesome", seco=True)
    assert "nada enviado" in r
    assert falso.enviado is None


def test_descricao_no_teto_e_recusada_em_vez_de_truncada(monkeypatch):
    """Truncar para caber o credito trocaria um problema por outro."""
    falso = _Falso(_snippet("x" * (C.MAX_DESCRICAO - 20)))
    monkeypatch.setattr(C, "_req", falso)
    r = C.consertar("tok", "abc", "Wholesome")
    assert r.startswith("nao coube")
    assert falso.enviado is None


def test_video_sumido_nao_estoura(monkeypatch):
    """Apagado, privado ou de outro canal: e resposta, nao excecao."""
    def _vazio(url, data=None, method=None, headers=None):
        return _Corpo(json.dumps({"items": []}))
    monkeypatch.setattr(C, "_req", _vazio)
    assert C.consertar("tok", "abc", "Wholesome").startswith("sumiu")


# ------------------------------------------------------- o corte por data

def test_o_corte_aponta_para_o_commit_que_tornou_canais_trilha_confiavel():
    """Antes de 8544196 a faixa saia de um hash: o banco nao prova o audio."""
    assert C.CORTE_TRILHA_CONFIAVEL == "2026-08-13T19:23:31Z"
