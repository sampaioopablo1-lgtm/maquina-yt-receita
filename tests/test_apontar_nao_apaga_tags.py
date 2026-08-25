"""O passo que liga o short ao longo estava apagando as tags do short.

MEDIDO EM 25/08/2026, contra a API e nao contra o codigo. Pedi o snippet de
seis shorts e dois longos da frota:

    ktkGZ-el-Qc  short  tags= 8
    BGKWxWGpC6g  short  tags= 0
    xKhdMry9Uqo  short  tags= 0
    p2YBHWv_6IA  short  tags= 0
    REz_hpFTH0Y  short  tags= 0
    WXiLGTxHYQE  short  tags= 8
    65YArnqcGYc  longo  tags=15
    3KtwRYxl7_U  longo  tags=15

A assimetria entrega a causa sozinha: TODO longo mantem as quinze tags, e
quatro de seis shorts perderam as oito. A unica coisa que acontece com o short
e nao acontece com o longo e o `apontar_para_longo` — um `videos.update` que
le o snippet e o grava de volta com o link no fim.

Logo apos o upload, essa leitura as vezes volta SEM `tags`: o video ainda esta
sendo indexado. O write-back seguinte grava o snippet incompleto por cima e
apaga o que o proprio upload tinha acabado de enviar. Intermitente, silencioso,
e nada falha.

Reler ate vir com tags nao resolve — nao ha como distinguir "ainda nao indexou"
de "nunca teve". O remedio e nao depender da leitura para o que ja se sabe: o
snippet do upload volta como `base` e repoe o que faltar.

Custo de nao consertar: o short e o unico formato desta frota que recebe
distribuicao, e tag e busca.
"""

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import publicar as P  # noqa: E402


BASE = {"snippet": {"title": "Titulo do short", "description": "Paragrafo um.",
                    "tags": ["fap 2027", "fapweb", "rat"], "categoryId": "27",
                    "defaultLanguage": "pt-BR", "defaultAudioLanguage": "pt-BR"}}


class _Falso:
    """Dubla `_req`: guarda o PUT em vez de falar com a rede."""

    def __init__(self, lido):
        self.lido, self.enviado = lido, None

    def __call__(self, url, data=None, method=None, headers=None):
        if method == "PUT":
            self.enviado = json.loads(data.decode())
            return _Corpo("{}")
        return _Corpo(json.dumps({"items": [{"snippet": self.lido}]}))


class _Corpo:
    def __init__(self, txt):
        self.txt = txt

    def read(self):
        return self.txt.encode()


def _roda(monkeypatch, lido, base=BASE):
    falso = _Falso(lido)
    monkeypatch.setattr(P, "_req", falso)
    r = P.apontar_para_longo("tok", "SHORT1", "LONGO1", base=base)
    return r, falso.enviado


# ------------------------------------------------- o defeito medido, prendido

def test_leitura_sem_tags_nao_apaga_as_tags(monkeypatch):
    """Este e o caso que apagou quatro shorts da frota."""
    lido = {"title": "Titulo do short", "description": "Paragrafo um.",
            "categoryId": "27"}          # <- sem `tags`, como a API devolveu
    r, enviado = _roda(monkeypatch, lido)
    assert enviado["snippet"]["tags"] == ["fap 2027", "fapweb", "rat"]
    assert "repos" in r and "tags" in r


def test_leitura_sem_idioma_nao_apaga_o_idioma(monkeypatch):
    """Mesma classe de perda: idioma errado marca o video na lingua errada."""
    lido = {"title": "Titulo do short", "description": "Paragrafo um.",
            "categoryId": "27"}
    _, enviado = _roda(monkeypatch, lido)
    assert enviado["snippet"]["defaultLanguage"] == "pt-BR"
    assert enviado["snippet"]["defaultAudioLanguage"] == "pt-BR"


def test_a_leitura_vence_quando_ela_tem_o_campo(monkeypatch):
    """`base` repoe o que FALTA; nao sobrescreve o que a API ja tem.

    Se alguem editou o titulo no Studio, esse titulo e mais recente que o do
    upload e tem de sobreviver ao apontamento.
    """
    lido = {"title": "Titulo editado no Studio", "description": "Paragrafo um.",
            "tags": ["editada"], "categoryId": "27",
            "defaultLanguage": "pt-BR", "defaultAudioLanguage": "pt-BR"}
    r, enviado = _roda(monkeypatch, lido)
    assert enviado["snippet"]["title"] == "Titulo editado no Studio"
    assert enviado["snippet"]["tags"] == ["editada"]
    assert r == "ok", "nada a repor, entao nada a anunciar"


def test_o_link_do_longo_entra_no_fim(monkeypatch):
    lido = {"title": "t", "description": "Paragrafo um.", "categoryId": "27"}
    _, enviado = _roda(monkeypatch, lido)
    assert enviado["snippet"]["description"].endswith("https://youtu.be/LONGO1")
    assert enviado["snippet"]["description"].startswith("Paragrafo um.")


def test_nao_duplica_o_link(monkeypatch):
    lido = {"title": "t", "description": "Paragrafo um.\n\nhttps://youtu.be/LONGO1",
            "tags": ["a"], "categoryId": "27"}
    r, enviado = _roda(monkeypatch, lido)
    assert r == "ja apontava"
    assert enviado is None


def test_descricao_perdida_na_leitura_volta_da_base(monkeypatch):
    """Descricao vazia + link seria um short sem texto nenhum."""
    lido = {"title": "t", "categoryId": "27"}
    _, enviado = _roda(monkeypatch, lido)
    assert enviado["snippet"]["description"].startswith("Paragrafo um.")


def test_sem_base_continua_funcionando(monkeypatch):
    """Compatibilidade: quem chamar sem `base` mantem o comportamento antigo."""
    lido = {"title": "t", "description": "Paragrafo um.", "tags": ["a"],
            "categoryId": "27"}
    falso = _Falso(lido)
    monkeypatch.setattr(P, "_req", falso)
    assert P.apontar_para_longo("tok", "S", "L") == "ok"
    assert falso.enviado["snippet"]["tags"] == ["a"]


def test_falha_de_rede_nao_derruba_a_publicacao(monkeypatch):
    """Os dois videos ja subiram: aqui nada pode virar excecao."""
    def _explode(*a, **k):
        raise RuntimeError("timeout")
    monkeypatch.setattr(P, "_req", _explode)
    assert P.apontar_para_longo("tok", "S", "L", base=BASE).startswith("falhou")
