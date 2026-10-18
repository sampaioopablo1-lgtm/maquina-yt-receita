"""O instrumento de 01:2x contava ID, e grupo de copias inflava a pauta.

Medido as 03:1x de 18/10, na PRIMEIRA vez que o `origens_sem_uso` teve o que
dizer: no `kolejny-poziom` ele devolveu SEIS origens de zero usos (ranks 16 a 20
e 22 da ordem viva) e as SEIS tinham o MESMO titulo — sao copias, do grupo das
46 duplicatas. Por TITULO DISTINTO eram ZERO origens novas, nao seis.

E o efeito (C-2) da rotina nomeia isso desde o 658: contar por id premia
duplicata. Eu escrevi o instrumento SEM a guarda, duas horas depois de escrever
outro (`origem_de_outro_canal`) que tambem precisou de uma.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import concentracao  # noqa: E402

# Ordem VIVA medida as 03:0x de 18/10 pela playlist UUGe6s... — 23 longos.
ORDEM_VIVA_KOL = [
    "GUiq15usizw", "kWZW-qV4tQc", "IuBLU-P4Aj8", "nPyVHJmY2HA", "-5aMrDsxlZE",
    "EwUkhdwyuuo", "vcJf6WipLtY", "SP7Vz8qHdRY", "kDkagIf2isA", "wb1RGIx7OJI",
    "42hpD7eaptE", "Rj7beZkOeYo", "34SgUG7rf0U", "iqV7m6tKb5A", "ef_oZmfmdz4",
    "SZV9Vk5YFwI", "qcY5XC1KtlQ", "_M8t8SPC_f0", "jDa9SM8A7os", "5gHnniPl0f8",
    "MjI4ZGJAhIo", "YLGwalTND7M", "Xgt32iH8Ft8",
]
# Titulo MEDIDO na pagina de cada um dos seis — identico nos seis.
O_MESMO = "Emerytura z ZUS: 34,4% pensji w 2050 roku. Ile musisz odlozyc sam?"
AS_SEIS = ["SZV9Vk5YFwI", "qcY5XC1KtlQ", "_M8t8SPC_f0", "jDa9SM8A7os",
           "5gHnniPl0f8", "YLGwalTND7M"]
TITULO_DE = {i: O_MESMO for i in AS_SEIS}


def test_sem_o_titulo_ele_devolve_SEIS():
    """O defeito, ancorado: e preciso que ele exista para o conserto valer."""
    cru = concentracao.origens_sem_uso("kolejny-poziom", ORDEM_VIVA_KOL)
    assert cru == AS_SEIS


def test_com_o_titulo_ele_devolve_UMA():
    colapsado = concentracao.origens_sem_uso(
        "kolejny-poziom", ORDEM_VIVA_KOL, None, TITULO_DE
    )
    assert len(colapsado) == 1


def test_e_a_que_sobra_e_a_PRIMEIRA_da_ordem():
    """Colapsar nao pode escolher ao acaso: fica a mais recente da ordem viva."""
    colapsado = concentracao.origens_sem_uso(
        "kolejny-poziom", ORDEM_VIVA_KOL, None, TITULO_DE
    )
    assert colapsado == ["SZV9Vk5YFwI"]


def test_o_tamanho_da_inflacao_sai_CONTADO():
    assert concentracao.copias_colapsadas(
        "kolejny-poziom", ORDEM_VIVA_KOL, TITULO_DE
    ) == 5


def test_titulo_DESCONHECIDO_nao_colapsa_com_nada():
    """Senao dois ids sem titulo virariam um, que e inventar duplicata."""
    parcial = {"SZV9Vk5YFwI": O_MESMO}   # os outros cinco sem titulo
    saida = concentracao.origens_sem_uso(
        "kolejny-poziom", ORDEM_VIVA_KOL, None, parcial
    )
    assert len(saida) == 6
    assert saida[0] == "SZV9Vk5YFwI"


def test_titulos_DIFERENTES_nao_colapsam():
    """Contraprova no outro sentido: sem copia, nada sai."""
    distintos = {i: f"titulo {n}" for n, i in enumerate(AS_SEIS)}
    saida = concentracao.origens_sem_uso(
        "kolejny-poziom", ORDEM_VIVA_KOL, None, distintos
    )
    assert saida == AS_SEIS
    assert concentracao.copias_colapsadas(
        "kolejny-poziom", ORDEM_VIVA_KOL, distintos
    ) == 0


def test_mapa_VAZIO_nao_e_tratado_como_mapa():
    """`{}` tem de cair no ramo 'sem titulo', nao colapsar tudo em nada."""
    assert concentracao.origens_sem_uso(
        "kolejny-poziom", ORDEM_VIVA_KOL, None, {}
    ) == AS_SEIS


def test_origem_JA_usada_continua_fora_dos_dois_ramos():
    for tit in (None, TITULO_DE):
        saida = concentracao.origens_sem_uso(
            "kolejny-poziom", ORDEM_VIVA_KOL, None, tit
        )
        assert "SP7Vz8qHdRY" not in saida
        assert "GUiq15usizw" not in saida


def test_a_nota_do_defeito_continua_escrita():
    """Sem ela o proximo reescreve a funcao contando id outra vez."""
    doc = concentracao.origens_sem_uso.__doc__
    assert "658" in doc
    assert "TITULO" in doc.upper()
    assert "copias" in doc


def test_e_a_nota_do_762_771_nao_foi_apagada_pelo_conserto():
    doc = concentracao.origens_sem_uso.__doc__
    assert "762" in doc and "771" in doc
    assert "OMITE" in doc.upper()
