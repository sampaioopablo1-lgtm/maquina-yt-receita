"""O numero que eu reportava ao dono toda rodada estava SUBCONTADO.

A contradicao do 740/748 — mira VERDE na previsao e real FORA do teto do canal —
e o item mais antigo da fila do dono, e eu relatava a frequencia dela a cada
rodada: "cinco de sete", "dez de treze", "onze de quatorze". Esses numeros saiam
da minha cabeca: eu incrementava o tally da rodada anterior em vez de recontar a
serie.

Medido pelo `mira.tally_fora_da_mira` em 16/10 as 22:2x: **20 de 23**. Eu estava
subcontando, e no sentido pior — o erro fazia a contradicao parecer MENOS
frequente do que ela e, justamente no numero que sustenta um pedido ao dono.

E a causa e a do item 3 da §10: conta que eu faco a mao vira erro meu. A diferenca
aqui e que ela ficou de pe por muitas rodadas porque cada incremento era
plausivel — ninguem erra "+1", erra-se o TOTAL de onde se parte.

Ressalva declarada no modulo e repetida aqui: o tally aplica a mira ATUAL a todas
as pecas da serie, inclusive as da fronteira do override `5dfc87f` (13/10). Para
essas pode ser mira retroativa. O numero e o melhor que existe e nao e limpo.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "fabrica"))

import ensaio  # noqa: E402
import mira  # noqa: E402

from test_residuo_quebra_o_limite_de_dois_segundos import SERIE  # noqa: E402

# O que eu vinha reportando, e o que a contagem devolveu.
EU_REPORTAVA = (11, 14)
MEDIDO_EM_16_10 = (20, 23)


def test_o_tally_medido_e_MAIOR_do_que_eu_reportava():
    t = mira.tally_fora_da_mira(SERIE)
    d = t["labtreinamento"]
    n_fora, n = len(d["fora"]), len(d["fora"]) + len(d["dentro"])
    assert (n_fora, n) >= MEDIDO_EM_16_10, (n_fora, n)
    assert n_fora > EU_REPORTAVA[0], (
        "se o tally medido voltar a caber no numero que eu contava a mao, "
        "alguem mudou a serie ou a mira — RELEIA em vez de ajustar")


def test_o_erro_era_no_sentido_que_ESCONDE_a_contradicao():
    """O sentido importa: ele fazia o problema parecer menor para o dono."""
    assert EU_REPORTAVA[0] < MEDIDO_EM_16_10[0]
    assert EU_REPORTAVA[1] < MEDIDO_EM_16_10[1]


def test_so_conta_canal_com_mira_PROPRIA():
    """Contar a faixa da FROTA para canal sem override inflaria o tally."""
    t = mira.tally_fora_da_mira(SERIE)
    assert set(t) <= set(ensaio.ALVO_POR_CANAL)
    assert "kolejny-poziom" not in t, (
        "o kolejny nao tem ALVO_POR_CANAL; se passar a ter, este teste tem de "
        "ser RELIDO porque o tally ganha um canal")


def test_so_conta_o_provedor_PEDIDO():
    """A previsao de cada mundo e outra; misturar os dois mede coisa nenhuma."""
    so_piper = mira.tally_fora_da_mira(SERIE, provedor="piper")
    todos = {p for p, _, _, prov in SERIE if prov == "piper"}
    assert not so_piper or todos, "sem peca do piper o tally dele e vazio"
    edge = mira.tally_fora_da_mira(SERIE, provedor="edge")
    assert edge, "a serie tem pecas do edge"


def test_o_relato_DIZ_o_que_nao_mede():
    texto = mira.relato_do_tally(SERIE)
    assert "FORA do teto da mira" in texto
    assert "mira estava VERDE" in texto, (
        "sem essa linha o tally se le como 'N pecas com a mira verde deram "
        "fora', e a mira de cada peca vive na copy dela, nao aqui")


def test_a_ressalva_do_override_RETROATIVO_esta_escrita():
    texto = " ".join(mira.tally_fora_da_mira.__doc__.split())
    assert "retroativa" in texto
    assert "nao e limpo" in texto


def test_o_docstring_registra_a_CAUSA_do_erro():
    texto = " ".join(__doc__.split())
    assert "incrementava o tally da rodada anterior" in texto
