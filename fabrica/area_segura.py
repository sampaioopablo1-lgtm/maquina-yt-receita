"""A janela que o portao `layout` deixa desenhar — UM dono, lido de la.

POR QUE EXISTE (19/10/2026, 12:3x). Eu passei tres rodadas relatando que o
trilho de capitulos e os cinco layouts de longo "deixaram de ser promessa", e
na PRIMEIRA vez que uma spec de longo os declarou o portao `layout` reprovou
**as 64 cenas**. Medido:

    | o que                        | onde desenha            | janela do portao |
    |------------------------------|-------------------------|------------------|
    | `trilho` (faixa)             | y 30 a 74 px de 1080    | y >= 130 px      |
    | `trilho` (recuo lateral)     | x 106 px de 1920        | x >= 231 px      |
    | `comparar` (duas colunas)    | x 130 a 1790            | x 231 a 1689     |
    | `divisor` (faixa de parte)   | x 0 a 1920 (tela cheia) | x 231 a 1689     |
    | `formula` (seta da nota)     | x 192                   | x >= 231         |

**A causa e de ENQUADRAMENTO, e e o 679/698/725 em geometria.** As posicoes do
trilho sao MEDIDAS por variancia temporal no longo do dono — e o video dele tem
**zero** zoom (medido em 16/10: mediana 0,072 contra 0,39 a 0,63 nossas, e zero
transicoes acima de `scene 0,15`). O NOSSO render aplica Ken Burns em toda cena,
logo corta `corte_do_ken_burns()` de cada lado antes de mostrar qualquer coisa.
**Transplantei uma posicao medida num quadro que nao se move para um render que
se move**, e o que estava no topo da tela dele esta FORA do quadro no nosso.

E o portao esta certo: ele existe porque o `kp-plan-9233` foi pego com 6/6
quadros com tinta na borda e o `seviye-seviye-010` reprovou em t=333,9 s. Afrouxar
`MARGEM_VISUAL` para caber a geometria seria limiar sem procedencia (§10) — e
pior, seria afrouxar o portao para salvar a peca, que e o avesso do trabalho.

**ESTE MODULO E A CORRECAO ESTRUTURAL, nao o remendo:** a janela deixa de ser
numero escrito em dois lugares e passa a ser LIDA do proprio portao. Era o
defeito de dois donos da mesma regra — o que congelou a legenda, parou a mira de
conferir por seis pecas e pos job inventado na serie —, agora na geometria.

**O CUSTO VAI DITO:** a largura util do trilho cai de 1709 px para ~1442 px
(-16%), logo CABEM MENOS CAPITULOS. Isso nao se contorna encolhendo a fonte:
`trilho.corpo_que_cabe` ja tem piso, e faixa ilegivel e o §3.8 em tipografia.
"""

# A folga contra o anti-aliasing da rasterizacao. O portao mede PIXEL diferente
# do fundo, e uma borda desenhada exatamente no limite deixa meio pixel do lado
# de fora. Nao e limiar de producao: e o arredondamento do rasterizador.
FOLGA = 0.004


def faixa_de_risco() -> float:
    """O que o portao `layout` chama de risco, lido DELE.

    O import e tardio de proposito: o `layout` importa o `fabrica`, e o
    `fabrica` importa o `trilho` e o `layouts_longo`, que importam este modulo.
    Import no topo fecharia o ciclo.
    """
    import layout

    return layout.faixa_de_risco()


def janela() -> tuple:
    """(inicio, fim) em fracao de quadro, igual nos dois eixos.

    A fracao vale para LARGURA e ALTURA porque o `faixa_de_risco` e uma fracao
    de cada dimensao — em 1920x1080 isso da 231 px nos lados e 130 px no topo e
    na base.
    """
    r = faixa_de_risco() + FOLGA
    return r, 1.0 - r


def dentro(frac: float) -> float:
    """Mapeia uma fracao de quadro CHEIO para dentro da janela segura.

    Serve para a geometria que foi escrita contra 1920x1080 inteiros — as
    coordenadas transcritas do motor do dono e as derivadas da nossa grade.
    Preserva a PROPORCAO entre os elementos, que e o que aquela geometria
    carrega de informacao, e abandona a posicao absoluta, que e o que o nosso
    zoom invalida.
    """
    x0, x1 = janela()
    return x0 + float(frac) * (x1 - x0)


def escala() -> float:
    """Quanto a janela segura mede, em fracao do quadro cheio."""
    x0, x1 = janela()
    return x1 - x0


def relato() -> str:
    x0, x1 = janela()
    return (f"AREA SEGURA: {x0:.4f} a {x1:.4f} do quadro "
            f"({escala() * 100:.1f}% dele) — em 1920x1080 isso e "
            f"x {x0 * 1920:.0f} a {x1 * 1920:.0f} e "
            f"y {x0 * 1080:.0f} a {x1 * 1080:.0f}. "
            f"Lida do portao `layout.faixa_de_risco` "
            f"({faixa_de_risco():.4f}) mais {FOLGA} de anti-aliasing.")


if __name__ == "__main__":
    print(relato())
