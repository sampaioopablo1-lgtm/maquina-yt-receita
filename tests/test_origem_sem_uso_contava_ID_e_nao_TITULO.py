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

# E ESTE ARQUIVO REPROVOU EM 18/10 as 09:2x, UM DIA depois de eu o escrever: ele
# cravava a lista das SEIS por IDENTIDADE e a rodada CONSUMIU a primeira delas
# (`SZV9Vk5YFwI` virou o `kolejny-poziom-s059`), logo sobram cinco e a que fica e
# outra. E a classe do 743/753/761 — identidade onde havia propriedade — pela
# QUARTA vez, agora num arquivo meu de um dia de vida.
#
# A propriedade e esta, e nao a lista: das copias do grupo, as que AINDA nao
# renderam short saem uma a uma sem o mapa de titulos, e colapsam em UMA com
# ele, que e a PRIMEIRA delas na ordem viva. Isso vale com seis, com cinco e com
# duas — e quando sobrar UMA so, colapsar deixa de ter o que medir, o que vai
# DITO em vez de passar por vacuidade.


def _livres(titulo_de=None):
    """As copias do grupo que a producao ainda nao consumiu, na ordem viva."""
    saida = concentracao.origens_sem_uso(
        "kolejny-poziom", ORDEM_VIVA_KOL, None, titulo_de
    )
    return [i for i in saida if i in AS_SEIS]


def test_sem_o_titulo_ele_devolve_UMA_POR_COPIA_LIVRE():
    """O defeito, ancorado na PROPRIEDADE: sem titulo, cada copia conta.

    Em 03:1x eram as seis; hoje sao as que sobraram. O que o conserto precisa
    que exista e a INFLACAO — mais de uma saida para um titulo so.
    """
    livres = _livres()
    assert len(livres) >= 2, (
        "sobrou menos de duas copias livres neste grupo, logo nao ha inflacao "
        "para medir e este arquivo perdeu a ancora — releia a nota acima em vez "
        "de apagar o teste"
    )
    assert set(livres) <= set(AS_SEIS)
    assert livres == [i for i in ORDEM_VIVA_KOL if i in livres]


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
    assert colapsado == [_livres()[0]], (
        "colapsou numa copia que nao e a primeira da ordem viva entre as livres"
    )


def test_o_tamanho_da_inflacao_sai_CONTADO():
    assert concentracao.copias_colapsadas(
        "kolejny-poziom", ORDEM_VIVA_KOL, TITULO_DE
    ) == len(_livres()) - 1


def test_titulo_DESCONHECIDO_nao_colapsa_com_nada():
    """Senao dois ids sem titulo virariam um, que e inventar duplicata."""
    livres = _livres()
    parcial = {livres[0]: O_MESMO}       # as outras livres SEM titulo
    saida = _livres(parcial)
    assert len(saida) == len(livres), "titulo desconhecido colapsou com algo"
    assert saida[0] == livres[0]


def test_titulos_DIFERENTES_nao_colapsam():
    """Contraprova no outro sentido: sem copia, nada sai."""
    distintos = {i: f"titulo {n}" for n, i in enumerate(AS_SEIS)}
    saida = _livres(distintos)
    assert saida == _livres()
    assert concentracao.copias_colapsadas(
        "kolejny-poziom", ORDEM_VIVA_KOL, distintos
    ) == 0


def test_mapa_VAZIO_nao_e_tratado_como_mapa():
    """`{}` tem de cair no ramo 'sem titulo', nao colapsar tudo em nada."""
    assert _livres({}) == _livres()


def test_origem_JA_usada_continua_fora_dos_dois_ramos():
    for tit in (None, TITULO_DE):
        saida = concentracao.origens_sem_uso(
            "kolejny-poziom", ORDEM_VIVA_KOL, None, tit
        )
        assert "SP7Vz8qHdRY" not in saida
        assert "GUiq15usizw" not in saida
        # e a copia que ESTA rodada consumiu tambem saiu dos dois ramos
        assert "SZV9Vk5YFwI" not in saida


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
