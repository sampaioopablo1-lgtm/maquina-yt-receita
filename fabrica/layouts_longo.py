"""Os layouts do LONGO que o `layout.py` nao tinha — geometria do motor do dono.

POR QUE (19/10/2026). Em 16/10 eu medi o longo da referencia e listei CINCO
layouts que nos nao temos. O dono decidiu a direcao — *"busco deixar tudo por
aqui na nuvem, produzindo videos melhores que este de 8 min"* — e depois apontou
a fonte: *"aprenda com o video, tenha como referencia, alem da documentacao das
pastas zip. Javascripts."*

O arquivo e o `motor/scenes.html` do pacote dele: 335 linhas que desenham as 24
cenas em 1920x1080. **A geometria daqui e COPIADA de la, nao inventada por mim**,
e cada numero vai com a linha de origem. Isso nao e importar pipeline alheio por
cima do nosso (a trava da §10): nada do motor dele roda aqui, e o render
continua sendo o nosso SVG. O que atravessa e MEDIDA — as coordenadas de um
layout que o dono ja usa e ja publicou.

O QUE ENTROU, e por que estes dois primeiro:

  * `comparar` — duas colunas com ✕ e ✓. E o layout que carrega a correcao de
    uma entrada errada, que e a unidade de conteudo da nossa pauta inteira;
  * `numero` — cartao de numero grande. E o unico dos cinco que resolve
    "mostrar uma quantidade sem virar lista".

Os outros tres (formula anotada, cartao de erro, divisor de parte) ficam para o
proximo passo, e o motivo vai dito: layout sem peca que o use e codigo morto.

**O QUE NAO ATRAVESSOU, de proposito:** o faseamento no tempo (`T(...)`,
`TT(...)`), que no motor dele faz cada elemento entrar na hora da fala. O nosso
equivalente e `svg_cena(..., camada=k)`, que ja existe e e por onde isso tem de
passar — reimplementar o relogio dele seria duas regras para a mesma coisa, que
e o defeito do `assert 20 <= ds <= 60`.
"""

# ATENCAO (19/10, 06:1x): o `motor/scenes.html` NAO ESTA NO REPO — nem no
# historico, nem neste conteiner, nem no sandbox. O pacote ZIP do dono foi lido
# numa sessao anterior e nunca foi comitado, logo o que esta abaixo e uma
# TRANSCRICAO que NAO SE RECONFERE aqui. Ela e o apoio UNICO destas coordenadas:
# ao contrario das cores (que tem a medicao do video publicado como segunda
# fonte), nao existe nada que confirme `x=130` ou `800x760` alem deste codigo.
# O motivo e a consequencia — layout NOVO de longo nao se escreve "copiando de
# la", porque nao ha de onde — estao em
# `docs/pacote-do-dono-NAO-esta-no-repo.md`.
# Coordenadas do `motor/scenes.html`, em quadro de 1920x1080. A fracao vai ao
# lado porque o nosso render recebe W e H e nao pode cravar pixel.
BASE_W, BASE_H = 1920.0, 1080.0


# RETRATACAO DE 19/10 AS 12:3x — a geometria abaixo e de QUADRO CHEIO e o nosso
# render nao mostra o quadro cheio. Na primeira spec de longo que usou estes
# layouts o portao `layout` reprovou: `comparar` com 20,64% de tinta na borda,
# `divisor` com 7,57%, `formula` com 2,17%. O motivo e que o nosso render aplica
# Ken Burns e corta a borda, e o motor do dono (de onde estas coordenadas vem)
# nao tem zoom nenhum — medido em 16/10. A conta inteira esta em
# `fabrica/area_segura.py`, que e UM dono lido do proprio portao.
#
# `_x` mapeia uma fracao de LARGURA do quadro cheio para dentro da janela
# segura; `_y` faz o mesmo na ALTURA. A PROPORCAO entre os elementos — que e o
# que a transcricao carrega de informacao — sobrevive; a posicao absoluta, que e
# o que o nosso zoom invalida, nao.
def _AS():
    import area_segura
    return area_segura


def _x(frac: float) -> float:
    return _AS().dentro(frac)


def _y(frac: float) -> float:
    return _AS().dentro(frac)


def _esc_geo(frac: float) -> float:
    """Comprimento (largura/altura), nao posicao: so encolhe, nao desloca."""
    return float(frac) * _AS().escala()


# comparar(s): x=130 e x=990, top=170, 800x760, border-top 8px
COMPARAR = dict(
    x_esq=130 / BASE_W, x_dir=990 / BASE_W, y=170 / BASE_H,
    larg=800 / BASE_W, alt=760 / BASE_H, barra=8 / BASE_H,
    corpo_titulo=56 / BASE_H, corpo_item=36 / BASE_H,
    recuo=30 / BASE_W, passo_item=62 / BASE_H, primeiro_item=120 / BASE_H,
)
# numero(s): valor 300px, legenda 54px em top 590, nota 30px em top 760
NUMERO = dict(
    corpo_valor=300 / BASE_H, y_valor_so=330 / BASE_H, y_valor_com=210 / BASE_H,
    corpo_legenda=54 / BASE_H, y_legenda=590 / BASE_H,
    corpo_nota=30 / BASE_H, y_nota=760 / BASE_H,
)
ICONE_ERRADO, ICONE_CERTO = "✕", "✓"

# A geometria MAPEADA, cacheada. A regra de qual chave e posicao e qual e
# comprimento e uniforme e vai escrita porque errar nela desloca o desenho sem
# avisar: chave que comeca em `x_`/`y_`, ou que e exatamente `x`/`y`, e POSICAO
# e passa pelo mapeamento; todo o resto — largura, altura, recuo, passo e corpo
# de fonte — e COMPRIMENTO e so encolhe na mesma escala da janela.
_GEO: dict = {}


def _e_posicao(chave: str) -> bool:
    return chave in ("x", "y") or chave.startswith(("x_", "y_"))


def geo(nome: str) -> dict:
    """O dict de geometria do layout, ja dentro da janela segura."""
    if nome not in _GEO:
        base = globals()[nome]
        _GEO[nome] = {k: (_x(v) if _e_posicao(k) else _esc_geo(v))
                      for k, v in base.items()}
    return _GEO[nome]


def janela_x() -> tuple:
    """(x0, largura) da janela segura, em fracao de LARGURA de quadro."""
    a = _AS().janela()
    return a[0], a[1] - a[0]




def _esc(s: str) -> str:
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def _cores(pal: dict):
    """O par errado/certo. O tema do dono declara `red` e `ok`; sem eles, o
    nosso `c2`/`c1`, que e o unico par de acento que toda spec nossa tem."""
    errado = pal.get("red") or pal.get("c2") or "#FF5A5F"
    certo = pal.get("ok") or pal.get("c1") or "#3CCB7F"
    return errado, certo


def comparar(c: dict, pal: dict, W: float, H: float) -> str:
    """Duas colunas: o que se faz errado contra o que se faz certo.

    `c` traz `esq` e `dir`, cada um com `titulo` e `itens`.
    """
    g = geo("COMPARAR")
    errado, certo = _cores(pal)
    ink = pal.get("ink", "#EEF1F5")
    painel = pal.get("panel") or pal.get("bg", "#161B24")
    s = []
    for lado, chave, cor, icone in (("esq", "esq", errado, ICONE_ERRADO),
                                    ("dir", "dir", certo, ICONE_CERTO)):
        col = c.get(chave) or {}
        x = W * (g["x_esq"] if lado == "esq" else g["x_dir"])
        y = H * g["y"]
        lw, lh = W * g["larg"], H * g["alt"]
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{lw:.1f}" '
                 f'height="{lh:.1f}" rx="{H * 0.018:.1f}" fill="{painel}"/>')
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{lw:.1f}" '
                 f'height="{H * g["barra"]:.1f}" fill="{cor}"/>')
        tx = x + W * g["recuo"]
        ty = y + H * g["primeiro_item"] - H * 0.035
        s.append(f'<text x="{tx:.1f}" y="{ty:.1f}" '
                 f'font-size="{H * g["corpo_titulo"]:.1f}" fill="{cor}" '
                 f'font-weight="700" font-family="Anton, DejaVu Sans, sans-serif">'
                 f'{_esc(icone)} {_esc(col.get("titulo", ""))}</text>')
        iy = y + H * g["primeiro_item"] + H * 0.055
        for item in (col.get("itens") or []):
            s.append(f'<text x="{tx:.1f}" y="{iy:.1f}" '
                     f'font-size="{H * g["corpo_item"]:.1f}" fill="{cor}" '
                     f'font-family="Inter, DejaVu Sans, sans-serif">{_esc(icone)}</text>')
            s.append(f'<text x="{tx + W * 0.022:.1f}" y="{iy:.1f}" '
                     f'font-size="{H * g["corpo_item"]:.1f}" fill="{ink}" '
                     f'font-weight="600" font-family="Inter, DejaVu Sans, sans-serif">'
                     f'{_esc(item)}</text>')
            iy += H * g["passo_item"]
    return "".join(s)


def numero(c: dict, pal: dict, W: float, H: float) -> str:
    """Cartao de numero grande: um valor, uma legenda, uma nota."""
    g = geo("NUMERO")
    acc = pal.get("acc") or pal.get("c1", "#3DDBD9")
    ink = pal.get("ink", "#EEF1F5")
    mut = pal.get("mut") or pal.get("c2", "#8B95A5")
    cx = W / 2
    tem_leg = bool(c.get("legenda"))
    y = H * (g["y_valor_com"] if tem_leg else g["y_valor_so"])
    corpo = H * g["corpo_valor"] * float(c.get("escala", 1.0))
    s = [f'<text x="{cx:.1f}" y="{y + corpo * 0.78:.1f}" text-anchor="middle" '
         f'font-size="{corpo:.1f}" fill="{acc}" font-weight="400" '
         f'font-family="Anton, DejaVu Sans, sans-serif">'
         f'{_esc(c.get("valor", ""))}</text>']
    if tem_leg:
        s.append(f'<text x="{cx:.1f}" y="{H * g["y_legenda"]:.1f}" '
                 f'text-anchor="middle" font-size="{H * g["corpo_legenda"]:.1f}" '
                 f'fill="{ink}" font-weight="700" '
                 f'font-family="Inter, DejaVu Sans, sans-serif">'
                 f'{_esc(c["legenda"])}</text>')
    if c.get("nota"):
        s.append(f'<text x="{cx:.1f}" y="{H * g["y_nota"]:.1f}" '
                 f'text-anchor="middle" font-size="{H * g["corpo_nota"]:.1f}" '
                 f'fill="{mut}" font-family="Inter, DejaVu Sans, sans-serif">'
                 f'{_esc(c["nota"])}</text>')
    return "".join(s)


# ---------------------------------------------------------------------------
# OS TRES QUE FALTAVAM — e a GEOMETRIA DELES E NOSSA, nao copiada
#
# A medicao de 16/10 no video do dono nomeia cinco layouts que o `layout.py` nao
# tinha. Dois entraram em 19/10 as 04:2x com coordenadas transcritas do
# `motor/scenes.html`. **Em 19/10 as 06:1x ficou medido que aquele arquivo nao
# esta no repo** — nem no historico, nem no conteiner, nem no sandbox: ver
# `docs/pacote-do-dono-NAO-esta-no-repo.md`.
#
# Logo estes tres NAO podem dizer "copiado de la", porque nao ha de onde copiar.
# **A geometria abaixo e DERIVADA da nossa propria grade**, reusando as fracoes
# que os dois primeiros ja fixaram — `y=170/1080` de topo, `alt=760/1080` de
# painel, `rx=0,018H`, a barra de 8/1080 e os corpos de 56 e 36 sobre H. Isso e
# escolha nossa e vai dita, em vez de vestir procedencia que nao existe.
#
# **O que a medicao do video DELE sustenta, e e so isto:** que os tres existem
# como FORMA (formula anotada argumento por argumento, cartao de erro, divisor
# de parte) e que o mundo visual e monocromatico e estatico — mediana 0,072 e
# 96% de quadros congelados em 530 s. Nenhum pixel de posicao vem de la.
FORMULA = dict(
    y_linha=300 / BASE_H, corpo_linha=96 / BASE_H,
    y_primeira_nota=470 / BASE_H, corpo_nota=34 / BASE_H,
    passo_nota=64 / BASE_H, x_nota=240 / BASE_W, recuo_seta=40 / BASE_W,
)
# cartao de erro: o painel do `comparar` centrado, com o codigo grande em cima
ERRO = dict(
    larg=900 / BASE_W, y=200 / BASE_H, alt=620 / BASE_H,
    corpo_codigo=180 / BASE_H, y_codigo=300 / BASE_H,
    corpo_causa=44 / BASE_H, y_causa=560 / BASE_H,
    corpo_saida=34 / BASE_H, y_saida=680 / BASE_H,
)
# divisor de parte: faixa fina no meio da tela, numero da parte a esquerda
DIVISOR = dict(
    y_faixa=470 / BASE_H, alt_faixa=140 / BASE_H,
    corpo_num=120 / BASE_H, corpo_titulo=64 / BASE_H,
    x_num=200 / BASE_W, x_titulo=400 / BASE_W,
)


# A monospace e MAIS LARGA que a sem-serifa do estimador: 0,60 por caractere
# contra 0,52. O fator vai aqui porque e desta fonte, e nao do estimador.
RAZAO_MONO = 0.60 / 0.52


def _corpo_que_cabe(texto: str, corpo: float, W: float,
                    piso: float = 0.45) -> float:
    """O corpo que mantem a linha DENTRO da janela segura, encolhendo so o
    necessario.

    MEDIDO em 19/10 as 13:3x: sem isto, formula longa transbordava e o portao
    `layout` reprovava a cena — 1,32% de tinta na borda no
    `kolejny-poziom-020`. O estimador de largura e o do `trilho`, que e UM dono,
    e nao uma copia nascida aqui.

    Encolhe com PISO: abaixo dele devolve o piso e deixa o portao reprovar, em
    vez de fabricar formula ilegivel para a peca passar (§3.8).
    """
    import trilho

    util = W * _AS().escala()
    atual = float(corpo)
    minimo = atual * piso
    while atual > minimo:
        if trilho.largura_estimada(texto, atual) * RAZAO_MONO <= util:
            return atual
        atual -= 1.0
    return minimo


def formula(c: dict, pal: dict, W: float, H: float) -> str:
    """Formula anotada argumento por argumento.

    `c` traz `formula` (o texto da linha) e `notas` (lista de str, uma por
    argumento). A anotacao e uma seta curta e o texto, empilhados — o motor do
    dono faz isso com posicao por argumento, e NAO temos as coordenadas dele,
    logo aqui elas sao uniformes e isso vai declarado no cabecalho da secao.
    """
    g = geo("FORMULA")
    ink = pal.get("ink", "#EEF1F5")
    acc = pal.get("acc") or pal.get("c1", "#3DDBD9")
    mut = pal.get("mut") or pal.get("c2", "#8B95A5")
    corpo = _corpo_que_cabe(c.get("formula", ""), H * g["corpo_linha"], W)
    s = [f'<text x="{W * 0.5:.1f}" y="{H * g["y_linha"]:.1f}" '
         f'text-anchor="middle" font-size="{corpo:.1f}" '
         f'fill="{ink}" font-weight="700" '
         f'font-family="DejaVu Sans Mono, monospace">'
         f'{_esc(c.get("formula", ""))}</text>']
    y = H * g["y_primeira_nota"]
    for nota in (c.get("notas") or []):
        s.append(f'<text x="{W * g["x_nota"]:.1f}" y="{y:.1f}" '
                 f'font-size="{H * g["corpo_nota"]:.1f}" fill="{acc}" '
                 f'font-family="Inter, DejaVu Sans, sans-serif">&#8627;</text>')
        s.append(f'<text x="{W * (g["x_nota"]) + W * g["recuo_seta"]:.1f}" '
                 f'y="{y:.1f}" font-size="{H * g["corpo_nota"]:.1f}" '
                 f'fill="{mut}" '
                 f'font-family="Inter, DejaVu Sans, sans-serif">'
                 f'{_esc(nota)}</text>')
        y += H * g["passo_nota"]
    return "".join(s)


def erro(c: dict, pal: dict, W: float, H: float) -> str:
    """Cartao de erro: o codigo que a tela mostra, a causa e a saida.

    `c` traz `codigo` (ex. `#REF!`), `causa` e `saida`.
    """
    g = geo("ERRO")
    ink = pal.get("ink", "#EEF1F5")
    vermelho = pal.get("red") or pal.get("c2") or "#FF5A5F"
    painel = pal.get("panel") or pal.get("bg", "#161B24")
    mut = pal.get("mut") or pal.get("c2", "#8B95A5")
    x = (W - W * g["larg"]) / 2
    s = [f'<rect x="{x:.1f}" y="{H * g["y"]:.1f}" width="{W * g["larg"]:.1f}" '
         f'height="{H * g["alt"]:.1f}" rx="{H * 0.018:.1f}" fill="{painel}"/>',
         f'<rect x="{x:.1f}" y="{H * g["y"]:.1f}" width="{W * g["larg"]:.1f}" '
         f'height="{H * COMPARAR["barra"]:.1f}" fill="{vermelho}"/>',
         f'<text x="{W * 0.5:.1f}" y="{H * g["y_codigo"]:.1f}" '
         f'text-anchor="middle" font-size="{H * g["corpo_codigo"]:.1f}" '
         f'fill="{vermelho}" font-weight="700" '
         f'font-family="DejaVu Sans Mono, monospace">'
         f'{_esc(c.get("codigo", ""))}</text>']
    if c.get("causa"):
        s.append(f'<text x="{W * 0.5:.1f}" y="{H * g["y_causa"]:.1f}" '
                 f'text-anchor="middle" font-size="{H * g["corpo_causa"]:.1f}" '
                 f'fill="{ink}" font-weight="700" '
                 f'font-family="Inter, DejaVu Sans, sans-serif">'
                 f'{_esc(c["causa"])}</text>')
    if c.get("saida"):
        s.append(f'<text x="{W * 0.5:.1f}" y="{H * g["y_saida"]:.1f}" '
                 f'text-anchor="middle" font-size="{H * g["corpo_saida"]:.1f}" '
                 f'fill="{mut}" '
                 f'font-family="Inter, DejaVu Sans, sans-serif">'
                 f'{_esc(c["saida"])}</text>')
    return "".join(s)


def divisor(c: dict, pal: dict, W: float, H: float) -> str:
    """Divisor de parte: `parte` (o numero) e `titulo` da parte que comeca."""
    g = geo("DIVISOR")
    ink = pal.get("ink", "#EEF1F5")
    acc = pal.get("acc") or pal.get("c1", "#3DDBD9")
    painel = pal.get("panel") or pal.get("bg", "#161B24")
    s = [f'<rect x="{W * janela_x()[0]:.1f}" y="{H * g["y_faixa"]:.1f}" width="{W * janela_x()[1]:.1f}" '
         f'height="{H * g["alt_faixa"]:.1f}" fill="{painel}"/>',
         f'<rect x="{W * janela_x()[0]:.1f}" y="{H * g["y_faixa"]:.1f}" width="{W * janela_x()[1]:.1f}" '
         f'height="{H * COMPARAR["barra"]:.1f}" fill="{acc}"/>',
         f'<text x="{W * g["x_num"]:.1f}" '
         f'y="{H * (g["y_faixa"] + g["alt_faixa"] * 0.72):.1f}" '
         f'font-size="{H * g["corpo_num"]:.1f}" fill="{acc}" '
         f'font-weight="700" font-family="Anton, DejaVu Sans, sans-serif">'
         f'{_esc(c.get("parte", ""))}</text>',
         f'<text x="{W * g["x_titulo"]:.1f}" '
         f'y="{H * (g["y_faixa"] + g["alt_faixa"] * 0.66):.1f}" '
         f'font-size="{H * g["corpo_titulo"]:.1f}" fill="{ink}" '
         f'font-weight="700" font-family="Inter, DejaVu Sans, sans-serif">'
         f'{_esc(c.get("titulo", ""))}</text>']
    return "".join(s)


LAYOUTS = {"comparar": comparar, "numero": numero,
           "formula": formula, "erro": erro, "divisor": divisor}


def desenha(c: dict, pal: dict, W: float, H: float):
    """O fragmento do layout, ou None se este nao for um layout de longo."""
    f = LAYOUTS.get(c.get("layout"))
    return f(c, pal, W, H) if f else None
