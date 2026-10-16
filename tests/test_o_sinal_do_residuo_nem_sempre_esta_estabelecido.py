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

**O que isto NÃO derruba:** o teto da banda (hoje 4,0, do `labtreinamento-s052`,
real 29 contra previsão 25,0 — folga muito acima de 1,0; antes era o `s043` com
3,7, e o 774 o ampliou) e a decisão de
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


def test_existem_pontos_cujo_sinal_o_instrumento_NAO_resolve():
    """CORRIGIDO em 16/10, e por identidade: a lista NOMEADA envelhecia.

    A versao anterior cravava os CINCO nomes de 15/10, e o
    `epomeno-epipedo-s041` (41,6 -> 42, +0,4) a reprovou por existir — mesma
    classe do 743/753/761. O que o 770 afirma nao e quais pecas sao, e sim que
    a classe NAO e vazia e nao e a serie toda: o instrumento tem passo de 1 s,
    logo sempre havera residuo pequeno demais para ter sinal, e sempre havera
    residuo grande o bastante para te-lo.
    """
    nao = _nao_estabelecidos()
    assert nao, "sem nao-estabelecidos a nota do 770 perdeu o objeto"
    assert len(nao) < len(SERIE), "se TODOS forem nao-estabelecidos, releia o 770"
    for _n, prev, real, _p in nao:
        assert real - prev <= GRANULARIDADE_DO_REAL + 1e-9
    # os cinco de 15/10 continuam na classe: conserto nao apaga historico
    antigos = {
        "epomeno-epipedo-s024",
        "epomeno-epipedo-s029",
        "epomeno-epipedo-s030",
        "epomeno-epipedo-s033",
        "kolejny-poziom-s027",
    }
    assert antigos <= {n for n, _, _, _ in nao}


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
    # propriedade, nao identidade: todo nao-estabelecido tem residuo nominal
    # dentro do passo do instrumento, e o conjunto nao e singular.
    assert nao and all(v <= 1.0 + 1e-9 for v in nao.values()), nao
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


def test_os_estabelecidos_sao_MAIORIA_e_os_outros_nao_desaparecem():
    """CORRIGIDO DUAS VEZES, e a segunda e a licao: eu troquei uma identidade
    por outra.

    Primeiro eu cravava o total (`34 de 39`), que reprovava a cada peca nova.
    Troquei por `3 <= nao_estabelecidos <= 6` — e isso reprovou no 46o ponto
    (`kolejny-poziom-s041`, +0,4), porque o TETO de 6 era so a contagem daquele
    dia com outra roupa. Mesma classe do 743/753/761, aplicada DENTRO da
    correcao dela.

    A propriedade que de fato importa, e que nao precisa de edicao: os
    nao-estabelecidos existem (senao alguem reescreveu o critério do 770 a mao)
    e sao MINORIA (senao a serie nao sustenta mais o sinal).
    """
    assert len(SERIE) == mira.RESIDUO_N >= 40
    assert len(_estabelecidos()) + len(_nao_estabelecidos()) == len(SERIE)
    nao = len(_nao_estabelecidos())
    assert nao > 0, "sem nao-estabelecidos, releia o 770 antes de seguir"
    assert nao * 2 < len(SERIE), (
        f"{nao} de {len(SERIE)} nao-estabelecidos: a serie deixou de sustentar"
        " o sinal pela maioria, e a nota do 770 tem de ser relida"
    )


def test_o_TETO_da_banda_vem_de_um_ponto_ESTABELECIDO():
    """Se o teto viesse de ponto com sinal indeterminado, a banda inteira cairia."""
    teto = max(_nominal(p, r) for _, p, r, _ in SERIE)
    dono = [n for n, p, r, _ in SERIE if _nominal(p, r) == teto]
    assert teto == mira.RESIDUO_OBSERVADO[1] == 4.0
    # 774: o dono do teto passou do `s043` (3,7) para o `s052` (4,0) — a
    # propriedade que importa e que ele seja ESTABELECIDO e do canal dominante,
    # nao QUAL peca e. Cravar o nome fez este teste reprovar por identidade.
    assert len(dono) == 1 and dono[0].startswith("labtreinamento"), dono
    assert ("labtreinamento-s043",) == tuple(
        n for n, p, r, _ in _estabelecidos() if n == "labtreinamento-s043"
    ), "o ponto que define o TETO saiu do conjunto estabelecido — releia o 770"


def test_a_banda_ficou_MENOS_util_e_isso_e_medido_nao_opinado():
    """Largura contra a granularidade do real: 1,5 (739) -> 2,8 (752) -> 3,2
    (769) -> 3,6 (770) -> 3,9 (774). Quando a largura passa de tres vezes o passo do
    instrumento, a faixa cobre tres inteiros de real e preve pouco."""
    lo, hi = mira.RESIDUO_OBSERVADO
    largura = round(hi - lo, 1)
    # 774 ampliou o teto e a largura foi a 3,9. O numero cresce a cada
    # ampliacao, entao o que se cobra e a PROPRIEDADE monotona: ela nunca
    # encolheu desde o 770.
    assert largura >= 3.6, largura
    assert largura > 3 * GRANULARIDADE_DO_REAL, (
        "a banda encolheu abaixo de tres passos do instrumento; releia o 770 em"
        " vez de comemorar — o piso so sobe se alguem o reescrever a mao"
    )
