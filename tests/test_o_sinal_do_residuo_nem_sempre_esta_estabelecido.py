#!/usr/bin/env python3
"""O SINAL do resíduo só está estabelecido quando a janela de arredondamento do
real fica TODA acima da previsão — aprendizado 770, `alto`, 14/10/2026 22:2x.

POR QUE ISTO EXISTE. Eu venho escrevendo, desde o 734, a frase "N de N acima da
previsão do provedor que de fato narrou", e ela cresceu até "vinte e sete de
vinte e sete". O `epomeno-epipedo-s029` mostrou que a frase nunca foi inteira:
previsão edge **41,9** (provedor MEDIDO pela anotação, zero avisos
`NARRACAO PELO PIPER` no job `116135075389`) e real **42 s**.

**O YouTube ARREDONDA PARA CIMA** (711). Logo real 42 significa duração
verdadeira em **(41; 42]**, e a previsão de 41,9 cai DENTRO desse intervalo: o
resíduo verdadeiro está em **(-0,9; +0,1]** e pode ser NEGATIVO. O sinal não é
uma observação, é uma consequência de eu ter lido o inteiro como se fosse a
medida.

**O critério, e ele é aritmético:** com arredondamento para cima, o real inteiro
`R` diz `t ∈ (R-1; R]`. O sinal do resíduo `t - P` só está estabelecido quando
`R - 1 >= P`, isto é quando **`R - P > 1,0`**.

Conferida a série inteira, **três dos 28 pontos não passam** — e os três são
exatamente os que definiram o PISO da banda ao longo do tempo: o
`epomeno-epipedo-s024` (+0,9, piso do 734), o `kolejny-poziom-s027` (+0,5, piso
do 769) e o `epomeno-epipedo-s029` (+0,1, piso de hoje). Entre os **25**
estabelecidos o piso nominal é **1,1**.

**O que isto NÃO derruba:** o teto da banda (3,7, do `labtreinamento-s043`,
real 27 contra previsão 23,3 — folga de 3,7, muito acima de 1,0) e a decisão de
cobrar a faixa nos DOIS mundos. **O que derruba é a minha contagem**, e é a
terceira vez em dois dias que o limite do INSTRUMENTO aparece como se fosse
achado (733, 768, agora este).

**E a consequência prática é só uma, e vai dita:** a `faixa_real` continua
somando o piso NOMINAL (0,1), porque é o menor resíduo que a observação mostra e
prometer um piso maior seria prometer o que não se mediu. O efeito é que a banda
ficou com **3,6 s de largura** contra 1 s de granularidade do real — ela informa
cada vez menos, e isso é a leitura honesta, não um defeito a esconder.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "fabrica"))

import mira  # noqa: E402

from test_residuo_quebra_o_limite_de_dois_segundos import SERIE  # noqa: E402

GRANULARIDADE_DO_REAL = 1.0  # o YouTube arredonda PARA CIMA (711)


def _nominal(p, r):
    return round(r - p, 1)


def _estabelecidos():
    return [s for s in SERIE if s[2] - s[1] > GRANULARIDADE_DO_REAL + 1e-9]


def _nao_estabelecidos():
    return [s for s in SERIE if s[2] - s[1] <= GRANULARIDADE_DO_REAL + 1e-9]


def test_quatro_pontos_da_serie_tem_o_sinal_NAO_estabelecido():
    nomes = sorted(n for n, _, _, _ in _nao_estabelecidos())
    assert nomes == [
        "epomeno-epipedo-s024",
        "epomeno-epipedo-s029",
        "epomeno-epipedo-s030",
        "kolejny-poziom-s027",
    ], (
        "o conjunto dos pontos cujo sinal o instrumento NAO resolve mudou; releia"
        f" o 770 antes de reescrever a contagem. Hoje: {nomes}"
    )


def test_a_implicacao_vale_de_UM_LADO_SO__piso_implica_nao_estabelecido():
    """REFINADO em 15/10 pelo `epomeno-epipedo-s030`, e a correcao e minha.

    Com tres pontos eu escrevi que os nao-estabelecidos eram "exatamente os que
    definiram o PISO da banda". O quarto ponto (+0,4) e nao-estabelecido e NAO
    moveu o piso — logo aquela correspondencia era coincidencia de amostra
    pequena. O que vale e a implicacao em UM sentido: residuo pequeno o bastante
    para ser piso e necessariamente pequeno o bastante para nao ser
    estabelecido; a volta nao vale.
    """
    nao = {n: _nominal(p, r) for n, p, r, _ in _nao_estabelecidos()}
    assert sorted(nao.values()) == [0.1, 0.4, 0.5, 0.9], nao
    # o piso da banda e um dos nao-estabelecidos (o lado que VALE)
    assert mira.RESIDUO_OBSERVADO[0] in nao.values()
    assert mira.RESIDUO_OBSERVADO[0] == min(nao.values())
    # e existe nao-estabelecido que NAO e o piso (o lado que NAO vale)
    assert any(v != mira.RESIDUO_OBSERVADO[0] for v in nao.values()), (
        "se todos os nao-estabelecidos voltarem a ser definidores de piso,"
        " releia o 770 em vez de restaurar a frase antiga")


def test_entre_os_estabelecidos_o_sinal_e_positivo_em_TODOS():
    """O que sobrevive da frase antiga, e so isto."""
    neg = [(n, _nominal(p, r)) for n, p, r, _ in _estabelecidos() if r - p <= 0]
    assert not neg, f"ponto estabelecido com sinal nao positivo: {neg}"


def test_o_piso_dos_estabelecidos_e_MAIOR_que_o_piso_da_banda():
    """A banda e mais larga do que a evidencia estabelecida justifica, e isso vai
    MEDIDO em vez de dito de memoria."""
    piso_est = min(_nominal(p, r) for _, p, r, _ in _estabelecidos())
    assert piso_est == 1.1, piso_est
    assert piso_est > mira.RESIDUO_OBSERVADO[0]


def test_a_contagem_de_estabelecidos_e_31_de_35():
    assert len(SERIE) == mira.RESIDUO_N == 35
    assert len(_estabelecidos()) == 31
    assert len(_nao_estabelecidos()) == 4


def test_o_TETO_da_banda_vem_de_um_ponto_ESTABELECIDO():
    """Se o teto viesse de ponto com sinal indeterminado, a banda inteira cairia."""
    teto = max(_nominal(p, r) for _, p, r, _ in SERIE)
    dono = [n for n, p, r, _ in SERIE if _nominal(p, r) == teto]
    assert teto == mira.RESIDUO_OBSERVADO[1] == 3.7
    assert dono == ["labtreinamento-s043"], dono
    assert ("labtreinamento-s043",) == tuple(
        n for n, p, r, _ in _estabelecidos() if n == "labtreinamento-s043"
    ), "o ponto que define o TETO saiu do conjunto estabelecido — releia o 770"


def test_a_banda_ficou_MENOS_util_e_isso_e_medido_nao_opinado():
    """Largura contra a granularidade do real: 1,5 (739) -> 2,8 (752) -> 3,2
    (769) -> 3,6 (770). Quando a largura passa de tres vezes o passo do
    instrumento, a faixa cobre tres inteiros de real e preve pouco."""
    lo, hi = mira.RESIDUO_OBSERVADO
    largura = round(hi - lo, 1)
    assert largura == 3.6, largura
    assert largura > 3 * GRANULARIDADE_DO_REAL, (
        "a banda encolheu abaixo de tres passos do instrumento; releia o 770 em"
        " vez de comemorar — o piso so sobe se alguem o reescrever a mao"
    )
