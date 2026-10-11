"""A conta de cadencia do short: caracteres por cena a partir da voz.

Ela existe porque eu generalizei o pior caso de uma voz para a frota inteira
(ver o docstring de `chars_por_cena`). O teste trava as duas propriedades que
me fariam repetir o erro: a sobrecarga e POR VOZ, e os intervalos sao `n-1`.
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import ensaio as E  # noqa: E402

PT = "pt-BR-ThalitaMultilingualNeural"
PL = "pl-PL-MarekNeural"


def test_a_conta_fecha_no_total_pedido():
    """O que a funcao devolve, remontado pelo `duracao_cena`, da o total."""
    for voz in (PT, PL, "el-GR-NestorasNeural"):
        n, total = 11, 33.0
        chars = E.chars_por_cena(voz, n, total)
        nar = "a" * (chars - 1) + "."     # UMA frase, `chars` no total
        medido = n * E.duracao_cena(nar, voz) + (n - 1) * E.GAP_CENA_S
        assert medido <= total + 0.05, (voz, medido, total)
        assert medido >= total - 1.5, (voz, medido, total)


def test_a_sobrecarga_e_por_voz_e_nao_da_frota():
    """O polones paga mais silencio por frase, logo cabe MENOS texto.

    Se algum dia isto empatar, voltou o numero unico da frota que o
    CLAUDE.md retratou em 11/10.
    """
    assert E.chars_por_cena(PT, 11, 33.0) > E.chars_por_cena(PL, 11, 33.0)


def test_sao_n_menos_um_intervalos():
    """Com `n` intervalos em vez de `n-1` sobraria uma cena fantasma."""
    voz, total = PT, 33.0
    chars = E.chars_por_cena(voz, 11, total)
    por_cena = (total - 10 * E.GAP_CENA_S) / 11
    R, P = E.MODELO_VOZ[voz]
    assert chars == int((por_cena - P) * R)


def test_cena_impossivel_devolve_zero_em_vez_de_negativo():
    """Pedir cadencia abaixo do proprio silencio da voz nao pode virar texto."""
    assert E.chars_por_cena(PL, 40, 10.0) == 0
