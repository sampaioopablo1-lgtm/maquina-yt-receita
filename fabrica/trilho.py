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

# MEDIDO por variancia temporal no video DELE — ver o docstring. Estas duas
# fracoes sao HISTORIA a partir de 19/10 as 12:3x, e ficam escritas porque a
# ALTURA da faixa sai delas.
REF_Y0, REF_Y1 = 0.028, 0.069
FAIXA_ALT = REF_Y1 - REF_Y0          # 0,041 do quadro — a medida que sobrevive

# RETRATACAO DE 19/10 AS 12:3x, E ELA E DE POSICAO, NAO DE MEDIDA.
# Eu desenhava a faixa em `REF_Y0` e com recuo lateral de 0,055, e na PRIMEIRA
# spec de longo que declarou o campo o portao `layout` reprovou as 64 cenas:
# y 30 a 74 px e x 106 px caem DENTRO do que o portao chama de risco (y >= 130,
# x >= 231 em 1920x1080). A causa esta medida e e de enquadramento — o video do
# dono tem ZERO zoom e o nosso render aplica Ken Burns em toda cena —, e vai
# inteira no `fabrica/area_segura.py`. O que atravessa do video dele e a ALTURA
# da faixa e o fato de ela ser permanente; a POSICAO e nossa, derivada do
# portao, e vai declarada como tal.
_AS = None


def _area():
    global _AS
    if _AS is None:
        import area_segura
        _AS = area_segura
    return _AS


def faixa_y0() -> float:
    """O topo da faixa: o primeiro y que o portao `layout` deixa pintar."""
    return _area().janela()[0]


def faixa_y1() -> float:
    return faixa_y0() + FAIXA_ALT


def margem_x() -> float:
    """O recuo lateral: o primeiro x que o portao deixa pintar."""
    return _area().janela()[0]


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
    util = W * (1 - 2 * margem_x())
    teto = corpo_max if corpo_max is not None else FAIXA_ALT * H
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
    y = H * (faixa_y0() + faixa_y1()) / 2 + corpo * 0.35
    x = W * margem_x()
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
    return _largura_estimada(texto_do_trilho(capitulos, 0), corpo) <= W * (1 - 2 * margem_x()) + 0.5


def relato(capitulos, W=1920, H=1080) -> str:
    corpo = corpo_que_cabe(capitulos, W, H)
    larg = _largura_estimada(texto_do_trilho(capitulos, 0), corpo)
    return (f"TRILHO: {len(capitulos)} capitulos, corpo {corpo:.1f}px, "
            f"largura {larg:.0f} de {W * (1 - 2 * margem_x()):.0f} uteis, "
            f"faixa y {H * faixa_y0():.0f} a {H * faixa_y1():.0f} "
            f"(ALTURA medida por variancia temporal no longo da referencia; "
            f"POSICAO derivada do portao `layout`, ver area_segura.py)")


if __name__ == "__main__":
    print(relato(["A armadilha", "Os três limites", "O que o PROCX muda",
                  "Quando usar cada um"]))


# ---------------------------------------------------------------------------
# O TRILHO DEIXOU DE SER CAMPO ESCRITO A MAO — 19/10 as 09:2x
#
# As 08:1x o despacho do render passou a desenhar a faixa, e no mesmo passo
# ficou visivel que NADA a alimentava: nenhuma spec de longo do disco declara o
# campo `trilho`, logo o conserto daquela hora era reachable e **sem dado**. E a
# mesma classe do defeito que ele conserta, uma camada acima: la o codigo nao
# era chamado, aqui ele e chamado e nunca recebe nada. Escrever `trilho` a mao
# em 66 cenas seria o passo manual que a §11-bis manda tirar — e seria eu
# repetindo, cena por cena, uma lista que a propria spec ja carrega.
#
# A DERIVACAO, e a regra do separador e MEDIDA, nao escolhida: capitulo e cena
# de layout `titulo`, e kicker que aparece MAIS DE UMA VEZE nao e capitulo, e
# separador. Medido no `labtreinamento-002`, cujas treze cenas `titulo` sao sete
# capitulos intercalados por seis cenas chamadas "Ponte"; sem essa regra o
# trilho sairia com treze entradas e seis delas iguais.
#
# E ELE RECUSA EM VEZ DE ENCOLHER. Varridas as 131 specs de longo da frota com
# voz modelada, o trilho derivado CABE em **17** e nao cabe em **114** — porque
# na geracao antiga quase toda cena e `titulo` (ha specs com 81 delas), e um
# trilho de quarenta entradas nao e um trilho, e uma linha de ruido. Encolher a
# fonte ate caber seria o portao verde fabricado do §3.8: a faixa existiria e
# ninguem leria. As duas specs do formato atual que eu de fato uso como origem
# — `epomeno-epipedo-013` (8) e `labtreinamento-002` (7) — cabem.


def capitulos_do_longo(cenas) -> list:
    """Os capitulos de uma spec de longo, DERIVADOS das cenas `titulo`.

    Kicker repetido NAO entra: ele e separador, nao capitulo (medido no
    `labtreinamento-002`, seis cenas "Ponte"). Kicker vazio tambem nao.
    """
    pela_ordem = [(i, (c.get("kicker") or "").strip())
                  for i, c in enumerate(cenas)
                  if c.get("layout") == "titulo"]
    vezes = {}
    for _, k in pela_ordem:
        vezes[k] = vezes.get(k, 0) + 1
    return [k for _, k in pela_ordem if k and vezes[k] == 1]


def _indices_dos_capitulos(cenas, caps) -> list:
    restantes = list(caps)
    saida = []
    for i, c in enumerate(cenas):
        k = (c.get("kicker") or "").strip()
        if c.get("layout") == "titulo" and restantes and k == restantes[0]:
            saida.append(i)
            restantes.pop(0)
    return saida


def aplica_no_longo(cenas, W: float = 1920, H: float = 1080) -> int:
    """Poe `trilho` e `trilho_atual` em TODA cena, e devolve quantos capitulos.

    LEVANTA em vez de produzir faixa ilegivel:
      * zero capitulos derivados — nao ha o que desenhar, e inventar seria pior;
      * trilho que nao CABE na largura — encolher a fonte ate caber e o portao
        verde fabricado do §3.8. Varrida a frota, isso acontece em 114 das 131
        specs de longo, todas da geracao em que quase toda cena e `titulo`.

    Muta as cenas no lugar, porque o render le a cena; e idempotente.
    """
    caps = capitulos_do_longo(cenas)
    if not caps:
        raise ValueError(
            "ZERO capitulos derivados: nenhuma cena `titulo` com kicker proprio. "
            "Trilho de nada nao e trilho vazio, e ausencia de leitura (739)."
        )
    if not cabe(caps, W, H):
        raise ValueError(
            f"o trilho de {len(caps)} capitulos NAO cabe em {W:.0f}px: "
            f"{relato(caps, W, H)}. Encolher a fonte ate caber e fabricar faixa "
            "ilegivel — o §3.8. Esta spec e da geracao em que quase toda cena e "
            "`titulo`, e ela precisa de capitulos de verdade antes do trilho."
        )
    marcos = _indices_dos_capitulos(cenas, caps)
    atual = 0
    for i, c in enumerate(cenas):
        while atual + 1 < len(marcos) and i >= marcos[atual + 1]:
            atual += 1
        c["trilho"] = list(caps)
        c["trilho_atual"] = atual
    return len(caps)
