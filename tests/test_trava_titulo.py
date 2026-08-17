"""A trava por nome de pacote nao segura duplicata. A por titulo, sim.

Medido em 17/08/2026. Um disparo automatico da frota levava sete pacotes; tres
deles — kolejny-poziom-002, seviye-seviye-002 e next-level-money-002 — tinham
ZERO linhas na trava por pacote e os tres ja estavam no ar, como YLGwalTND7M,
v2j35YekImM e UK-FswAW4QE.

A trava respondia certo e liberava errado: o mesmo render vive sob dois nomes,
o da spec e o da rodada que o publicou, e `videos.pacote` guarda o segundo.
Perguntar pelo primeiro devolve "nunca publicado", que e verdade sobre o nome e
mentira sobre o video.
"""

import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import publicar as P  # noqa: E402


@pytest.fixture
def banco(monkeypatch):
    """Finge o PostgREST: devolve as linhas de `videos` publicadas."""
    linhas = [
        {"pacote": "kp-plan-9233-20260811", "formato": "longo",
         "youtube_id": "Xgt32iH8Ft8",
         "titulo": "Jak ułożyć finanse przy średniej pensji 9233 zł?"},
        {"pacote": "kp-emerytura-zus-34-20260805", "formato": "longo",
         "youtube_id": "YLGwalTND7M",
         "titulo": "Emerytura z ZUS: 34,4% pensji w 2050 roku. Ile musisz odłożyć sam?"},
    ]

    class Resp:
        def read(self_inner):
            return json.dumps(linhas).encode()

    monkeypatch.setattr(P, "_req", lambda *a, **k: Resp())
    return linhas


def test_acha_o_mesmo_titulo_sob_outro_pacote(banco):
    """O caso real: a spec chama kolejny-poziom-002, o banco guarda a rodada."""
    achados = P.ja_no_ar_pelo_titulo(
        "Emerytura z ZUS: 34,4% pensji w 2050 roku. Ile musisz odłożyć sam?",
        "https://sb", "k")
    assert len(achados) == 1
    assert achados[0]["youtube_id"] == "YLGwalTND7M"
    assert achados[0]["pacote"] == "kp-emerytura-zus-34-20260805"


def test_titulo_inedito_passa(banco):
    assert P.ja_no_ar_pelo_titulo(
        "Ozempic e Mounjaro: O Que Você Reganha Não É o Que Você Perdeu",
        "https://sb", "k") == []


def test_ignora_caixa_e_espaco_nas_pontas(banco):
    """Mesmo video, digitado com outra caixa, continua sendo o mesmo video."""
    assert P.ja_no_ar_pelo_titulo(
        "  EMERYTURA Z ZUS: 34,4% PENSJI W 2050 ROKU. ILE MUSISZ ODŁOŻYĆ SAM?  ",
        "https://sb", "k")


def test_titulo_vazio_nao_consulta_o_banco(monkeypatch):
    """Sem titulo nao da para decidir, e casar '' com '' barraria tudo."""
    def explode(*a, **k):
        raise AssertionError("nao devia consultar o banco sem titulo")
    monkeypatch.setattr(P, "_req", explode)
    assert P.ja_no_ar_pelo_titulo("", "https://sb", "k") == []
    assert P.ja_no_ar_pelo_titulo(None, "https://sb", "k") == []


def test_a_trava_por_pacote_sozinha_teria_liberado(banco, monkeypatch):
    """O nucleo do defeito, explicito.

    Perguntando por 'kolejny-poziom-002', a trava por pacote devolve vazio —
    porque nenhuma linha tem esse nome. Ela nao esta com defeito; ela responde
    outra pergunta.
    """
    class Vazio:
        def read(self):
            return b"[]"
    monkeypatch.setattr(P, "_req", lambda *a, **k: Vazio())
    assert P.ja_publicado("kolejny-poziom-002", "https://sb", "k") == {}
