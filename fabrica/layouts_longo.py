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
    g = COMPARAR
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
    g = NUMERO
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


LAYOUTS = {"comparar": comparar, "numero": numero}


def desenha(c: dict, pal: dict, W: float, H: float):
    """O fragmento do layout, ou None se este nao for um layout de longo."""
    f = LAYOUTS.get(c.get("layout"))
    return f(c, pal, W, H) if f else None
