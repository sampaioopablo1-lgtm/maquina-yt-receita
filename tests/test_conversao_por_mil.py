"""A conversao por mil, travada com as leituras que a corrigiram.

Os numeros daqui sao os de 09, 10 e 11/10/2026, e cada teste corresponde a um
erro que eu cometi fazendo esta conta no olho. Eu usei 1,32 e 0,95 por mil o
dia 09/10 inteiro; o certo era 1,10 e 0,75, e a diferenca era o DENOMINADOR.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import conversao as C  # noqa: E402

# Medido em 09/10 18:10, 153 ids em quatro lotes, os quatro `200` (697).
# Guardo a SOMA porque e o que a medicao registrou; `denominador` soma pecas,
# entao uma lista de um elemento com a soma e equivalente para a aritmetica.
EPOMENO_09 = 15_454
KOLEJNY_09 = 10_625

# O contador do CANAL na mesma hora — e ele e MENOR que a soma das pecas.
CANAL_EPOMENO_09 = 12_152
CANAL_KOLEJNY_09 = 8_406


def test_o_numero_que_eu_usei_errado_o_dia_todo():
    """1,10 e 0,75 — nao 1,32 e 0,95."""
    assert round(C.por_mil("epomeno-epipedo", 17, [EPOMENO_09]), 2) == 1.10
    assert round(C.por_mil("kolejny-poziom", 8, [KOLEJNY_09]), 2) == 0.75


def test_o_contador_do_canal_nao_pode_ser_a_soma():
    """Um total nao pode ser menor que uma de suas partes.

    Este teste existe para que o 697 nao precise ser relido: se alguem voltar a
    usar o `viewCount` do canal como denominador, a conta de dois canais passa
    a dar MAIOR que a verdadeira, e aqui esta a prova aritmetica de que o
    contador e menor que a soma das pecas da propria maquina.
    """
    assert CANAL_EPOMENO_09 < EPOMENO_09
    assert CANAL_KOLEJNY_09 < KOLEJNY_09
    # e usa-lo INFLA a conversao, que foi exatamente o erro
    inflado = 1000.0 * 17 / CANAL_EPOMENO_09
    certo = C.por_mil("epomeno-epipedo", 17, [EPOMENO_09])
    assert inflado > certo


def test_canal_com_acervo_anterior_devolve_None_e_nao_zero():
    """`None` e a resposta CERTA, nao falha (668).

    Zero diria "nao converte"; None diz "nao da para saber daqui". Tratar um
    como o outro foi o que me fez eleger o labtreinamento como o melhor da
    frota por um dia.
    """
    assert C.por_mil("labtreinamento", 67, [4_165]) is None
    assert "NAO NORMALIZAVEL" in C.relato_por_mil("labtreinamento", 67, [4_165])


def test_o_relato_diz_qual_denominador_usou():
    linha = C.relato_por_mil("kolejny-poziom", 8, [KOLEJNY_09])
    assert "10625" in linha and "697" in linha


def test_o_denominador_soma_peca_a_peca():
    assert C.denominador([430, 241, 167]) == 838
    assert C.denominador([]) == 0
    assert C.por_mil("epomeno-epipedo", 3, []) is None


def test_as_leituras_seguintes_continuam_batendo():
    """22:15 de 09/10 e 06:09 de 10/10 — o numero anda, a conta nao."""
    assert round(C.por_mil("epomeno-epipedo", 17, [15_751]), 2) == 1.08
    assert round(C.por_mil("kolejny-poziom", 8, [10_830]), 2) == 0.74
    assert round(C.por_mil("epomeno-epipedo", 17, [15_818]), 3) == 1.075
    assert round(C.por_mil("kolejny-poziom", 8, [10_824]), 3) == 0.739
