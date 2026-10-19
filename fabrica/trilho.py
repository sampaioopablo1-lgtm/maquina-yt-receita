"""O trilho de capitulos permanente do topo — a assinatura do longo.

POR QUE EXISTE. Em 16/10/2026, medindo o longo da referencia quadro a quadro, eu
listei TRES distancias entre a peca do dono e as nossas, e as tres sao de LONGO:
o trilho permanente no topo, os 18,9 s por plano, e cinco layouts que o
`layout.py` nao tem. Em 19/10 o dono decidiu a direcao: *"busco deixar tudo por
aqui na nuvem, produzindo videos melhores que este de 8 min"*. Este modulo e o
primeiro tijolo — o trilho.

**A GEOMETRIA E MEDIDA, NAO ESCOLHIDA.** O trilho e, por definicao, o que NAO
muda entre quadros; logo ele se acha por variancia temporal. Medido em 19/10 as
01:4x no proprio video (`FtCtIJPsc_Q`, 21 quadros amostrados a 1/25 s, escala
256x144, desvio-padrao temporal por linha):

    linha 0 a 3     desvio ~1,0   — margem escura, nada
    **linha 4 a 9   desvio 10 a 28, brilho 26 a 42  — O TRILHO**
    linha 10 a 15   desvio ~1,2   — margem escura outra vez
    linha 16+       desvio 3 a 29 — o painel, que troca a cada capitulo

O desvio ALTO nas linhas 4 a 9 nao contradiz "permanente": o trilho fica, e o
DESTAQUE anda de um capitulo para o outro, e e o destaque que varia. As linhas
0-3 e 10-15, escuras e quietas, delimitam a faixa por cima e por baixo.

    4/144 = 0,028   e   9/144 = 0,069

**O que isto NAO mede:** a fonte, o peso e o espacamento exatos. Esses saem do
tema `noite` do pipeline do dono (`paleta_referencia.FONTES_DO_TEMA`), que e a
ferramenta com que a peca foi produzida.
"""

# Medido por variancia temporal — ver o docstring. Fracoes da ALTURA do quadro.
FAIXA_Y0 = 0.028
FAIXA_Y1 = 0.069
MARGEM_X = 0.055          # recuo lateral, na mesma proporcao do painel
SEPARADOR = "  |  "


def _largura_estimada(texto: str, corpo: float) -> float:
    """Largura aproximada de uma linha, em unidades de quadro.

    0,52 por caractere e a razao largura/corpo de uma sem-serifa de peso medio.
    E ESTIMATIVA declarada: ela so precisa acertar o bastante para ESCOLHER o
    corpo que cabe, e o teste cobra a propriedade (cabe), nao o numero.
    """
    return len(texto) * corpo * 0.52


def texto_do_trilho(capitulos, atual: int) -> str:
    """A linha inteira, como ela aparece — `1 Titulo | 2 Titulo | ...`."""
    return SEPARADOR.join(f"{i + 1} {c}" for i, c in enumerate(capitulos))


def corpo_que_cabe(capitulos, W: float, H: float,
                   corpo_max: float = None, corpo_min: float = None) -> float:
    """O maior corpo de fonte que mantem o trilho DENTRO da largura util.

    Encolhe em vez de cortar: trilho cortado le como defeito de render, e um
    capitulo que some do trilho desfaz a unica funcao dele, que e dizer onde o
    espectador esta.
    """
    util = W * (1 - 2 * MARGEM_X)
    teto = corpo_max if corpo_max is not None else (FAIXA_Y1 - FAIXA_Y0) * H
    piso = corpo_min if corpo_min is not None else teto * 0.45
    linha = texto_do_trilho(capitulos, 0)
    if not linha:
        return teto
    corpo = util / (len(linha) * 0.52)
    return max(piso, min(teto, corpo))


def faixa(capitulos, atual: int, pal: dict, W: float, H: float) -> str:
    """O fragmento SVG do trilho, para entrar em TODA cena do longo.

    `atual` e o indice 0-based do capitulo corrente; ele sai no `acc` do tema e
    os outros no `mut`, que e o par que o proprio tema do dono declara.

    **UM `<text>` com `<tspan>`, e isso e conserto de um defeito meu.** A
    primeira versao posicionava CADA pedaco com um `x` calculado pela minha
    estimativa de largura (0,52 por caractere). Renderizada, a prova foi
    imediata: os separadores sairam deslocados, porque o erro da estimativa
    ACUMULA a cada pedaco. Com tspans sem `x`, quem avanca o cursor e o
    renderizador, que sabe a largura real de cada glifo.

    A estimativa continua existindo — mas so para ESCOLHER o corpo que cabe,
    onde errar um pouco encolhe a fonte um pouco. Ela saiu do posicionamento,
    que e onde errar um pouco quebra o desenho.
    """
    if not capitulos:
        return ""
    if not 0 <= atual < len(capitulos):
        raise ValueError(
            f"capitulo atual {atual} fora de 0..{len(capitulos) - 1} — "
            "trilho que destaca o capitulo errado e pior que trilho nenhum"
        )
    corpo = corpo_que_cabe(capitulos, W, H)
    y = H * (FAIXA_Y0 + FAIXA_Y1) / 2 + corpo * 0.35
    x = W * MARGEM_X
    aceso = pal.get("c1") or pal.get("acc") or "#3DDBD9"
    apagado = pal.get("mut") or pal.get("c2") or "#8B95A5"

    def esc(s):
        return (s.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;"))

    tspans = []
    for i, cap in enumerate(capitulos):
        if i:
            tspans.append(f'<tspan fill="{apagado}" opacity="0.5">'
                          f'{esc(SEPARADOR)}</tspan>')
        if i == atual:
            tspans.append(f'<tspan fill="{aceso}" opacity="1.0" '
                          f'font-weight="700">{esc(f"{i + 1} {cap}")}</tspan>')
        else:
            tspans.append(f'<tspan fill="{apagado}" opacity="0.75" '
                          f'font-weight="400">{esc(f"{i + 1} {cap}")}</tspan>')
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{corpo:.1f}" '
            f'font-family="Inter, DejaVu Sans, sans-serif" '
            f'xml:space="preserve">{"".join(tspans)}</text>')


def cabe(capitulos, W: float, H: float) -> bool:
    """O trilho inteiro cabe na largura util com o corpo escolhido?"""
    corpo = corpo_que_cabe(capitulos, W, H)
    return _largura_estimada(texto_do_trilho(capitulos, 0), corpo) <= W * (1 - 2 * MARGEM_X) + 0.5


def relato(capitulos, W=1920, H=1080) -> str:
    corpo = corpo_que_cabe(capitulos, W, H)
    larg = _largura_estimada(texto_do_trilho(capitulos, 0), corpo)
    return (f"TRILHO: {len(capitulos)} capitulos, corpo {corpo:.1f}px, "
            f"largura {larg:.0f} de {W * (1 - 2 * MARGEM_X):.0f} uteis, "
            f"faixa y {H * FAIXA_Y0:.0f} a {H * FAIXA_Y1:.0f} "
            f"(medida por variancia temporal no longo da referencia)")


if __name__ == "__main__":
    print(relato(["A armadilha", "Os três limites", "O que o PROCX muda",
                  "Quando usar cada um"]))
