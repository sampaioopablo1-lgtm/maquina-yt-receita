# -*- coding: utf-8 -*-
"""Post de imagem, versao COR VIVA (pedido do Pablo em 07/09/2026).

O que muda em relacao a arte.py: a foto ganha saturacao e contraste, o degrade
do pe do quadro vai para uma cor quente da marca em vez do azul quase preto, e
a palavra em destaque sai em laranja cheio. O resto da identidade fica igual:
Montserrat 800 caixa baixa, Playfair italic no destaque, filete laranja,
assinatura em @oproximocliente.
"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from tipografia import paragrafo, PISO_PROMESSA

W, H = 1080, 1350
LARANJA = (255, 122, 26)
CREME = (255, 246, 224)
BRANCO = (255, 255, 255)
APOIO = (255, 214, 176)
SANS_PATH = "fontes/Montserrat.ttf"
LARG_MAX = 960

# A mensagem central da mentoria, em destaque nas dez artes de topo (pedido do
# Pablo em 07/09/2026, depois de ver que so a BF04 dizia o que se aprende).
#
# O topo NAO vende: ele entrega um pensamento sobre a dor e assina. Por isso a
# promessa entra numa faixa propria abaixo do apoio, e nao no lugar da frase de
# efeito -- quem para no post para pela dor, e so depois descobre o que eu faco.
# "aprenda", nao "receba": e o que separa mentoria de agencia.
PROMESSA = ["aprenda a criar anúncios que trazem cliente todo dia no seu WhatsApp",
            "sem agência e sem investir alto"]

# pes do degrade: cada arte escolhe um, para a serie nao ficar monocorde
FUNDOS = {
    "vinho":  (58, 12, 20),
    "grafite":(24, 22, 28),
    "petroleo":(10, 34, 44),
    "terra":  (52, 26, 12),
    "roxo":   (34, 14, 46),
}


def fonte(path, corpo, peso):
    f = ImageFont.truetype(path, corpo)
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


def cabe(d, txt, path, peso, corpo, larg=LARG_MAX):
    while corpo > 20:
        f = fonte(path, corpo, peso)
        if d.textlength(txt, font=f) <= larg:
            return f
        corpo -= 2
    return fonte(path, corpo, peso)


def cobrir(foto):
    im = Image.open(foto).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x0 = (im.width - W) // 2
    y0 = int((im.height - H) * 0.35)      # um pouco acima do centro: sobra pe para o texto
    return im.crop((x0, y0, x0 + W, y0 + H))


def vivo(im):
    """Cor viva SEM cozinhar a pele.

    A primeira versao usava saturacao 1,55 e ainda puxava o vermelho: o rosto
    dele saiu alaranjado, parecendo filtro ruim. A cor da serie vem do degrade
    colorido no pe do quadro e do laranja do destaque -- a foto so precisa de
    um empurrao leve para nao ficar apagada ao lado deles.
    """
    im = ImageEnhance.Color(im).enhance(1.18)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    return im


def degrade(im, cor, y_ini=620):
    px = im.load()
    for y in range(y_ini, H):
        t = (y - y_ini) / (H - y_ini)
        t = t * t * (3 - 2 * t)
        for x in range(W):
            r, g, b = px[x, y]
            px[x, y] = (round(r + (cor[0] - r) * t),
                        round(g + (cor[1] - g) * t),
                        round(b + (cor[2] - b) * t))
    return im


def brilho_faixa(im, y0=840, y1=1300):
    g = im.convert("L").crop((0, y0, W, y1))
    h = g.histogram()
    return sum(i * c for i, c in enumerate(h)) / sum(h)


def scrim(im, cor):
    for _ in range(8):
        if brilho_faixa(im) <= 62:      # teto um pouco mais alto: fundo colorido, nao preto
            break
        sombra = Image.new("RGB", (W, H), cor)
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).rectangle((0, 760, W, H), fill=95)
        im = Image.composite(sombra, im, mask.filter(ImageFilter.GaussianBlur(60)))
    return im, brilho_faixa(im)


def chapeu(im, cor, ate=200):
    """Escurece a facha de cima, onde agora fica a assinatura."""
    px = im.load()
    for y in range(ate):
        t = 1 - (y / ate)
        t = t * t * (3 - 2 * t) * 0.80
        for x in range(W):
            r, g, b = px[x, y]
            px[x, y] = (round(r + (cor[0] - r) * t), round(g + (cor[1] - g) * t),
                        round(b + (cor[2] - b) * t))
    return im


def desenhar(p, saida):
    cor = FUNDOS[p.get("fundo", "grafite")]
    im = chapeu(degrade(vivo(cobrir(p["foto"])), cor), cor)
    im, brilho = scrim(im, cor)
    d = ImageDraw.Draw(im)

    blocos = [
        (62,   "@oproximocliente", SANS_PATH,                    700, 34,  CREME),
        (716,  p["linha_sans"],    SANS_PATH,                    800, 86,  BRANCO),
        (812,  p["linha_cursiva"], "fontes/Playfair-Italic.ttf", 700, 176, LARANJA),
        (1016, p["linha_apoio"],   SANS_PATH,                    650, 52,  APOIO),
    ]
    # A assinatura subiu para o alto do quadro. Ela ocupava a ultima linha,
    # e o pe agora e da promessa -- que precisa de tres linhas grandes, nao
    # de uma tira de 26 px. Marca em cima, mensagem embaixo.
    caixas = []
    for y_topo, txt, path, peso, corpo, c in blocos:
        f = cabe(d, txt, path, peso, corpo)
        l, t, r, b = d.textbbox((0, 0), txt, font=f)
        # sombra curta, so para descolar do fundo colorido
        d.text(((W - (r - l)) / 2 - l + 2, y_topo - t + 3), txt, font=f, fill=(0, 0, 0))
        d.text(((W - (r - l)) / 2 - l, y_topo - t), txt, font=f, fill=c)
        caixas.append((y_topo, y_topo + (b - t), (r - l) * (b - t)))

    # A faixa da promessa. Fundo cheio em vez de texto solto: o topo tem foto
    # atras, e texto pequeno sobre pele nao le. A faixa tambem separa a
    # promessa do apoio -- sao duas coisas, a dor e a saida.
    # A promessa NAO vai em barra solida aqui. No fundo de funil a barra laranja
    # significa "clique"; no topo nao ha o que clicar, e barra no pe faz a peca
    # PARECER anuncio -- que e justamente o que encarece o alcance numa campanha
    # de reconhecimento. O post de dor funciona porque nao parece anuncio.
    # Entao: filete fino em cima, texto creme embaixo. Presente e legivel, sem
    # imitar o CTA da outra campanha.

    # ------------------------------------------------------------------
    # A PROMESSA, em corpo FIXO de 42/46 px, quebrando em quantas linhas
    # precisar. Ate 08/09/2026 ela era encolhida ate caber numa linha so e
    # saia a 26 PX -- a mensagem central da mentoria era a menor letra do
    # quadro. O portao de 18-30% nao pegava isso, porque area total nao mede
    # legibilidade: uma cursiva de 176 px esconde qualquer letra miuda.
    # Regra nova, em tipografia.py: largura e negociavel, corpo nao e.
    #
    # A promessa NAO vai em barra solida. No fundo de funil a barra laranja
    # significa "clique"; no topo nao ha o que clicar, e barra no pe faz a peca
    # PARECER anuncio -- que e o que encarece o alcance numa campanha de
    # reconhecimento. Filete fino em cima, texto embaixo.
    d.rectangle(((W - 120) // 2, 1088, (W + 120) // 2, 1092), fill=LARANJA)
    sent = [(PROMESSA[0], fonte(SANS_PATH, PISO_PROMESSA, 600), APOIO),
            (PROMESSA[1], fonte(SANS_PATH, PISO_PROMESSA + 4, 800), CREME)]
    fim_pe, tinta = paragrafo(d, sent, 1108, 970, W)

    gaps = [caixas[i + 1][0] - caixas[i][1] for i in range(len(caixas) - 1)]
    area = (sum(c[2] for c in caixas) + tinta) / (W * H)
    folga = 1088 - caixas[-1][1]
    ok = all(g >= 0 for g in gaps) and folga >= 0 and 0.18 <= area <= 0.30
    im.save(saida, quality=94)
    print("%-34s brilho %5.1f  gaps %s  texto %4.1f%%  %s" %
          (os.path.basename(saida), brilho, [round(g) for g in gaps], area * 100,
           "OK" if ok else "REFAZER"))
    return ok


if __name__ == "__main__":
    os.makedirs("artes2", exist_ok=True)
    todos = True
    for p in json.load(open(sys.argv[1])):
        todos &= desenhar(p, "artes2/%s.jpg" % p["slug"])
    print("todas OK" if todos else "ALGUMA PRECISA DE AJUSTE")
