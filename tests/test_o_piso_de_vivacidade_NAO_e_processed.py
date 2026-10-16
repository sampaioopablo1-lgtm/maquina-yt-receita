"""O numero que o dono pede e `processed`, e o que eu consigo medir e um PISO.

A rotina manda contar **so peca `processed`** — a regra existe porque em 08/10 eu
afirmei "21 entregues" e tive de retratar (666). Hoje o `uploadStatus` vive no
`videos.list` com `part=status`, que pede token, que pede `pg_net`, que pede o
`execute_sql`: negado em treze rodadas seguidas. Logo a pergunta do dono NAO tem
a resposta exata que ele pediu, e dizer que tem seria o §3.8.

O que existe sao duas rotas publicas sem credencial: `lengthSeconds` maior que
zero (que NEGA o `P0D` do 665) e `oembed` em 200 (que diz publica e indexada).
As duas juntas sao estritamente MAIS FRACAS que `processed` — o 758 mediu uma
peca com `uploadStatus: uploaded` e `duration: PT27S` ao mesmo tempo.

Medido em 16/10 as 20:2x nas 22 pecas do dia: 22 de 22 no piso.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "fabrica"))

import vivacidade_publica as vp  # noqa: E402

# A leitura real, (duracao maior lida, http do oembed).
MEDIDO_16_10 = {
    "idkn35TYGE0": (44, 200), "n1VJoPqokm8": (28, 200), "fHUBz98PjgA": (44, 200),
    "PA4k1nrpMMI": (43, 200), "8DVWFC5agrg": (124, 200), "RT_qRi_S1Mw": (44, 200),
    "QH9xoIC69jM": (42, 200), "7KZjro4H8ls": (43, 200), "stj6tmBAOLI": (43, 200),
    "Z8KZL5z8nxI": (28, 200), "WxlzxXVcMXI": (42, 200), "SVOd6xvXE7g": (43, 200),
    "JawBDlwnxzI": (27, 200), "6nPIaKuFm2Y": (43, 200), "I51f8_fKbok": (26, 200),
    "SX9xQnDzuac": (43, 200), "yqK9KcgDslg": (43, 200), "JwWis4o6CqE": (27, 200),
    "53GpMFpGuks": (44, 200), "MvmwHqFmYvY": (43, 200), "BwrCyzuFQT0": (27, 200),
    "FmD7olILCwo": (42, 200),
}


def test_as_22_pecas_do_dia_passam_o_PISO():
    por = vp.piso(MEDIDO_16_10)
    assert len(por.get("viva", [])) == 22
    assert not por.get("P0D") and not por.get("nao_publica")


def test_o_relato_DIZ_que_e_piso_e_NOMEIA_o_que_falta():
    texto = vp.relato(MEDIDO_16_10)
    assert "PISO" in texto
    assert "processed" in texto, (
        "o relato tem de nomear a condicao que ele NAO mede; sem isso 22 de 22 "
        "se le como 'o alvo do dono foi atingido', que e o erro do 666"
    )


def test_a_duracao_sai_do_MAIOR_lengthSeconds():
    """Medido: a pagina do `epomeno-epipedo-s046` trouxe 41 E 42."""
    html = '"lengthSeconds":"41" ... "lengthSeconds":"42"'
    assert vp.duracao_do_html(html) == 42


def test_campo_AUSENTE_nao_e_duracao_zero():
    """200 com 1,2 MB e zero `lengthSeconds` ja aconteceu — e rota, nao peca."""
    assert vp.duracao_do_html("pagina grande sem o campo") is None
    assert vp.veredito(None, 200) == "sem_leitura"
    assert vp.veredito(0, 200) == "P0D", "duracao zero lida E defeito"


def test_sem_leitura_NAO_entra_na_conta_dos_defeitos():
    por = vp.piso({"a": (43, 200), "b": (None, 200), "c": (0, 200)})
    assert por["viva"] == ["a"]
    assert por["sem_leitura"] == ["b"]
    assert por["P0D"] == ["c"]
    assert "b" not in por.get("P0D", []), (
        "somar rota fechada com peca morta e o erro de enquadramento mais caro "
        "deste projeto"
    )


def test_dicionario_vazio_LEVANTA():
    """Zero leituras nao e 'zero pecas vivas'."""
    try:
        vp.piso({})
    except ValueError as e:
        assert "AUSENCIA DE LEITURA" in str(e)
    else:
        raise AssertionError("tinha de levantar")


def test_nao_publica_e_distinto_de_P0D():
    assert vp.veredito(43, 404) == "nao_publica"
    assert vp.veredito(43, 200) == "viva"


def test_o_docstring_do_modulo_declara_o_limite():
    texto = " ".join(vp.__doc__.split())
    assert "estritamente mais fraco" in texto
    assert "758" in texto, "o contraexemplo medido vai citado, nao suposto"
