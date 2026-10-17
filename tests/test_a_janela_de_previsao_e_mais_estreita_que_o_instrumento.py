"""Cinco pontos numa janela de 0,4 s, e um real com granularidade de 1 s.

NASCEU DE DUAS AFIRMACOES MINHAS SEGUIDAS, as duas sobre os MESMOS dados e as
duas em excesso:

  * as 18:2x (766) eu escrevi que "a previsao REPRODUZ nesta faixa", a partir de
    dois pontos do epomeno (41,4 -> 43 e 41,3 -> 43);
  * as 19:1x (767) eu retratei isso, a partir de dois pontos do kolejny que
    INVERTEM (41,2 -> 44 e 41,6 -> 43).

O quinto ponto (epomeno-epipedo-s028, 41,5 -> 43, as 20:1x) fecha a conta e
mostra que NENHUMA das duas podia ser medida: as cinco previsoes caem numa
janela de **0,4 s** e o real tem granularidade de **1 s, arredondado para
cima**. Uma janela mais ESTREITA que o passo do instrumento nao pode ordenar
nada — e o 733 ja havia dito isso sobre o "paradoxo" do 732, com tres pontos
dentro de 1,0 s. Eu reapliquei o erro que aquele aprendizado nomeia, duas vezes,
em duas horas.

O QUE ESTES TESTES AFIRMAM: a propriedade de FORMA — que a janela e mais estreita
que a granularidade, logo a serie nesta faixa nao decide reprodutibilidade em
sentido nenhum.

O QUE ELES NAO AFIRMAM: que a previsao reproduz, nem que nao reproduz. Para
decidir isso e preciso previsao separada por MAIS de 1 s, e isso e desenho, nao
leitura dos dados que ja existem.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

from test_residuo_quebra_o_limite_de_dois_segundos import SERIE  # noqa: E402

GRANULARIDADE_DO_REAL = 1.0  # o YouTube devolve segundo inteiro, para CIMA
FAIXA = (41.0, 42.0)


def _janela():
    return [(p, prev, real) for p, prev, real, _ in SERIE
            if FAIXA[0] <= prev <= FAIXA[1]]


def test_a_janela_existe_e_tem_pelo_menos_CINCO_pontos():
    j = _janela()
    assert len(j) >= 5, f"a nota do 768 foi escrita com cinco pontos, achei {len(j)}"


def test_a_largura_da_PREVISAO_e_menor_que_a_granularidade_do_REAL():
    """E esta e a razao pela qual as duas afirmacoes cairam."""
    j = _janela()
    largura = max(p for _, p, _ in j) - min(p for _, p, _ in j)
    # EM 16/10 as 21:2x A LARGURA CHEGOU EXATAMENTE AO PASSO: o
    # `kolejny-poziom-s045` entrou com previsao 41,0, o extremo inferior da
    # faixa, e a largura foi de 0,8 para **1,00 s**. O criterio do 768 e "mais
    # estreita que o passo nao ordena", e largura IGUAL ao passo tambem nao
    # ordena — dois pontos a exatamente 1 s de distancia podem cair no mesmo
    # inteiro ou em inteiros vizinhos, dependendo so de onde o arredondamento
    # pega. Logo o `<=`; o que exige releitura e a largura PASSAR do passo, e e
    # isso que este assert cobra. A fronteira fica registrada em vez de ser
    # suavizada em silencio.
    assert largura <= GRANULARIDADE_DO_REAL, (
        f"largura {largura:.2f} s já passou do passo do instrumento "
        f"({GRANULARIDADE_DO_REAL} s): agora a serie PODE ordenar, e a nota do "
        "768 tem de ser RELIDA em vez de reaproveitada")


def test_a_janela_e_MULTICANAL__nao_e_efeito_de_um_canal():
    j = _janela()
    canais = {p.rsplit("-s", 1)[0] for p, _, _ in j}
    assert len(canais) >= 2, canais


def test_o_real_da_janela_ESPALHA_mais_do_que_a_previsao_explica():
    """E isto FORTALECE o 768 em vez de enfraquece-lo — aprendizado 769.

    Quando este arquivo nasceu (cinco pontos) os reais eram 43, 43, 43, 43 e 44,
    e eu travei "quase constante". O sexto ponto (`kolejny-poziom-s027`, previsao
    41,5 e real **42**) espalhou a janela para TRES inteiros — 42, 43 e 44 — com
    as previsoes ainda dentro de 0,4 s.

    Logo a propriedade certa nao e "o real e quase constante": e que **a
    dispersao do real nao cabe na largura da previsao**. Uma previsao que varia
    0,4 s nao pode produzir 2 s de real por relacao nenhuma; o que produz isso e
    o que a previsao NAO modela. Travar "quase constante" era travar um acidente
    de amostra pequena, e o proprio teste me obrigou a reler.
    """
    j = _janela()
    reais = [r for _, _, r in j]
    largura_prev = max(p for _, p, _ in j) - min(p for _, p, _ in j)
    espalhamento = max(reais) - min(reais)
    assert espalhamento > largura_prev, (
        f'real espalha {espalhamento} s contra {largura_prev:.1f} s de previsao: '
        'se o real passar a caber na largura da previsao, a previsao voltou a '
        'ordenar nesta faixa e o 768/769 tem de ser relido')


def test_a_janela_NAO_ordena__nem_no_sentido_monotono_nem_no_oposto():
    """A versao anterior deste teste CAIU, e a queda e o achado — 16/10, 21:2x.

    Ela cobrava que o real MAIOR viesse da previsao MENOR (41,2 -> 44), isto e,
    o oposto de uma relacao monotona. Com o `kolejny-poziom-s045` (previsao
    **41,0**, a menor da janela, real **41**, o menor) o extremo inferior passou
    a casar no sentido MONOTONO — e o teste reprovou.

    Nenhuma das duas versoes era a propriedade certa. Travar "o oposto de
    monotono" e tao arbitrario quanto travar "monotono": com 1,0 s de largura de
    previsao e 1 s de passo no real, **a janela nao ordena em sentido nenhum**, e
    qualquer par que pareca ordenar e indistinguivel do arredondamento. Era o
    erro do 733/768 outra vez, agora dentro do teste escrito para nomea-lo.

    O que sobrevive, e e verificavel: o real ESPALHA mais do que a largura da
    previsao explica (o teste acima), e a correlacao entre previsao e real nesta
    janela e FRACA. O limiar e declarado e frouxo de proposito — ele existe para
    acusar ordenacao FORTE, que seria a releitura do 768, nao para medir a
    ausencia dela.
    """
    j = _janela()
    assert len(j) >= 10, "com menos de dez pontos a correlacao nao diz nada"
    prevs = [p for _, p, _ in j]
    reais = [r for _, _, r in j]
    n = len(j)
    mx, my = sum(prevs) / n, sum(reais) / n
    num = sum((a - mx) * (b - my) for a, b in zip(prevs, reais))
    den = (sum((a - mx) ** 2 for a in prevs) * sum((b - my) ** 2 for b in reais)) ** 0.5
    r = num / den if den else 0.0
    assert abs(r) < 0.6, (
        f"correlacao previsao x real = {r:+.2f} nesta janela de "
        f"{max(prevs) - min(prevs):.1f} s: se ficar FORTE, a previsao passou a "
        "ordenar aqui e o 768/769 tem de ser RELIDO em vez de reaproveitado")

def test_a_janela_e_JUSTAMENTE_onde_o_negativo_apareceu():
    """O que sobrevive dos tres aprendizados e so o SINAL."""
    for p, prev, real in _janela():
        # `>= 0` desde 16/10: o `kolejny-poziom-s045` deu residuo ZERO (41,0 -> 41).
        # RETRATADO em 17/10 as 20:1x: o `epomeno-epipedo-s054` (41,6 -> 41)
        # e o PRIMEIRO real ABAIXO da previsao em 78 pontos, e o sinal dele esta
        # estabelecido para BAIXO (arredondamento para cima: (40; 41] fica todo
        # abaixo de 41,6). Logo "nenhum ponto e negativo" CAIU. A propriedade que
        # sobra e que o negativo e RARO, e quem a cobra e
        # `test_o_sinal_NAO_e_mais_de_N_de_N__e_o_negativo_apareceu`.
        assert real - prev <= 4.0, p
    negativos = [pk for pk, pr, r in _janela() if r < pr]
    # E ele caiu DENTRO desta janela estreita, que e o ponto do 768/769: uma
    # previsao que varia menos de 1 s produz real espalhado para os DOIS lados.
    assert negativos, "o negativo e desta janela; se saiu, releia o 768/769"
