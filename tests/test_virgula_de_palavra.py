# -*- coding: utf-8 -*-
"""A virgula de "ό,τι" e ortografica, nao e pausa.

Em grego "ό,τι" (o que) se escreve com virgula no meio, e e ela que o
distingue de "ότι" (que). Contando essa virgula, uma frase com DUAS pausas
reais era acusada de ter tres.
"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fabrica"))

from narracao import MAX_VIRGULAS, analisa, conta_virgulas  # noqa: E402

FRASE = "Ποσοστό, μετά συμψηφισμός, μετά ό,τι μένει σε σένα."


def test_a_virgula_de_o_ti_nao_conta_em_grego():
    assert FRASE.count(",") == 3          # o texto tem tres virgulas
    assert conta_virgulas(FRASE, "el") == 2   # mas so duas sao pausa


def test_a_mesma_frase_em_outro_idioma_conta_tudo():
    """A tabela e por idioma: fora do grego, ",": e virgula e ponto final."""
    assert conta_virgulas(FRASE, "pl") == 3


def test_tres_virgulas_de_verdade_continuam_contando():
    """O conserto nao pode cegar o portao."""
    assert conta_virgulas("Ένα, δύο, τρία, τέσσερα.", "el") == 3


def test_maiuscula_tambem_e_reconhecida():
    assert conta_virgulas("Ό,τι και να γίνει, μένει.", "el") == 1


def test_o_portao_nao_avisa_mais_nesta_frase():
    _, avisos, _ = analisa({"longo": [{"nar": FRASE}]}, "el")
    assert not [a for a in avisos if "virgulas" in a]


def test_o_portao_ainda_avisa_quando_ha_tres():
    _, avisos, _ = analisa({"longo": [{"nar": "Ένα, δύο, τρία, τέσσερα."}]}, "el")
    assert [a for a in avisos if "virgulas" in a]


def test_o_limite_continua_o_mesmo():
    assert MAX_VIRGULAS == 3
