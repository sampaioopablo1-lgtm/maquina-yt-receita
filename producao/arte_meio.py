# -*- coding: utf-8 -*-
"""Arte de MEIO DE FUNIL da mentoria O Proximo Cliente.

As tres etapas pedem tres pecas diferentes, e a diferenca precisa ser VISIVEL:

  topo (arte.py / arte2.py)   nomeia a dor. nao pede nada. filete + assinatura.
  MEIO (este)                 explica COMO funciona. CTA brando.
  fundo (arte_bofu.py)        e oferta. barra laranja solida = clique aqui.

Quem chega no meio ja viu o topo: sabe que tem a dor e comeca a suspeitar que
anuncio resolve. O que falta e acreditar no MECANISMO -- e por isso que toda
peca daqui responde "como isso funciona" ou "por que aprender em vez de
contratar", nunca "compre".

A marca visual do meio e a etiqueta VAZADA (contorno laranja, texto creme) em
vez da pilula cheia do fundo. Contorno le como assunto; pilula cheia le como
oferta. Nao ha barra de CTA -- ela pertence a outra campanha, e repetir a
mesma barra nas tres etapas ensina o olho que laranja e sempre anuncio.

python3 arte_meio.py meio.json
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1350
LARANJA = (255, 122, 26)
CREME = (255, 246, 224)
BRANCO = (255, 255, 255)
APOIO = (255, 214, 176)
LARG_MAX = 960

FUNDOS = {"vinho": (58, 12, 20), "grafite": (24, 22, 28), "petroleo": (10, 34, 44),
          "terra": (52, 26, 12), "roxo": (34, 14, 46), "escuro": (11, 18, 32)}

SANS = "fontes/Montserrat.ttf"
ITAL = "fontes/Playfair-Italic.ttf"

# A mesma string do arte.py, do arte2.py e do arte_bofu.py. Se mudar, muda nos
# quatro: promessa que varia de peca para peca nao vira memoria de ninguem.
PROMESSA = ["aprenda a criar anúncios que trazem cliente todo dia no seu WhatsApp",
            "sem agência e sem investir alto"]


def fonte(path, corpo, peso):
    f = ImageFont.truetype(path, corpo)
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


def cabe(d, txt, path, peso, corpo, larg=LARG_MAX):
    while corpo > 18:
        f = fonte(path, corpo, peso)
        if d.textlength(txt, font=f) <= larg:
            return f
        corpo -= 2
    return fonte(path, corpo, peso)


def centrar(d, txt, f, y, cor, sombra=True):
    l, t, r, b = d.textbbox((0, 0), txt, font=f)
    x = (W - (r - l)) / 2 - l
    if sombra:
        d.text((x + 2, y - t + 3), txt, font=f, fill=(0, 0, 0))
    d.text((x, y - t), txt, font=f, fill=cor)
    return y, y + (b - t), (r - l)


def cobrir(foto, alto=0.32):
    im = Image.open(foto).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x0 = (im.width - W) // 2
    y0 = int((im.height - H) * alto)
    im = im.crop((x0, y0, x0 + W, y0 + H))
    im = ImageEnhance.Color(im).enhance(1.18)
    return ImageEnhance.Contrast(im).enhance(1.10)


def degrade(im, cor, y_ini=520):
    px = im.load()
    for y in range(y_ini, H):
        t = (y - y_ini) / (H - y_ini)
        t = t * t * (3 - 2 * t)
        for x in range(W):
            r, g, b = px[x, y]
            px[x, y] = (round(r + (cor[0] - r) * t), round(g + (cor[1] - g) * t),
                        round(b + (cor[2] - b) * t))
    return im


def brilho(im, y0, y1):
    g = im.convert("L").crop((0, y0, W, y1))
    h = g.histogram()
    return sum(i * c for i, c in enumerate(h)) / sum(h)


def scrim(im, cor, y0=660):
    for _ in range(8):
        if brilho(im, 780, 1200) <= 60:
            break
        sombra = Image.new("RGB", (W, H), cor)
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).rectangle((0, y0, W, H), fill=95)
        im = Image.composite(sombra, im, m.filter(ImageFilter.GaussianBlur(60)))
    return im


def etiqueta(d, txt):
    """VAZADA, nao cheia. Contorno le como assunto; pilula cheia le como oferta,
    e oferta e trabalho da outra campanha."""
    f = fonte(SANS, 32, 700)
    l, t, r, b = d.textbbox((0, 0), txt, font=f)
    lw, lh = (r - l) + 60, (b - t) + 32
    x0, y0 = (W - lw) / 2, 54
    d.rounded_rectangle((x0, y0, x0 + lw, y0 + lh), radius=lh / 2, outline=LARANJA, width=4)
    d.text((x0 + 30 - l, y0 + 16 - t), txt, font=f, fill=CREME)
    return lw * lh, y0 + lh


def desenhar(p, saida):
    cor = FUNDOS[p.get("fundo", "grafite")]
    if p.get("modo") == "tipo":
        im = Image.new("RGB", (W, H), cor)
        halo = Image.new("RGB", (W, H), cor)
        ImageDraw.Draw(halo).ellipse((W / 2 - 430, 340, W / 2 + 430, 900),
                                     fill=(min(255, cor[0] + 46), min(255, cor[1] + 20), cor[2]))
        im = Image.blend(im, halo.filter(ImageFilter.GaussianBlur(150)), 0.55)
    else:
        im = scrim(degrade(cobrir(p["foto"], p.get("alto", 0.32)), cor), cor)
    d = ImageDraw.Draw(im)

    tinta, _ = etiqueta(d, p["etiqueta"])
    caixas = []

    y = p.get("y", 726)
    f = cabe(d, p["linha_sans"], SANS, 800, p.get("corpo_sans", 80))
    y0, y1, lg = centrar(d, p["linha_sans"], f, y, BRANCO)
    caixas.append((y0, y1, lg)); y = y1 + 14

    f = cabe(d, p["linha_cursiva"], ITAL, 700, p.get("corpo_cursiva", 152))
    y0, y1, lg = centrar(d, p["linha_cursiva"], f, y, LARANJA)
    caixas.append((y0, y1, lg)); y = y1 + 30

    f = cabe(d, p["linha_apoio"], SANS, 650, 46, 990)
    y0, y1, lg = centrar(d, p["linha_apoio"], f, y, APOIO, sombra=False)
    caixas.append((y0, y1, lg))

    # o pe: filete + promessa + assinatura, igual ao topo. Sem barra de CTA.
    d.rectangle(((W - 120) // 2, 1146, (W + 120) // 2, 1150), fill=LARANJA)
    yy = 1168
    for i, t in enumerate(PROMESSA):
        f = cabe(d, t, SANS, 600 if i == 0 else 800, 32, 940)
        l0, t0, r0, b0 = d.textbbox((0, 0), t, font=f)
        x0 = (W - (r0 - l0)) / 2 - l0
        d.text((x0 + 2, yy - t0 + 2), t, font=f, fill=(0, 0, 0))
        d.text((x0, yy - t0), t, font=f, fill=APOIO if i == 0 else CREME)
        tinta += (r0 - l0) * (b0 - t0)
        yy += (b0 - t0) + 9
    f = fonte(SANS, 30, 700)
    l0, t0, r0, b0 = d.textbbox((0, 0), "@oproximocliente", font=f)
    d.text(((W - (r0 - l0)) / 2 - l0, 1268 - t0), "@oproximocliente", font=f, fill=CREME)
    tinta += (r0 - l0) * (b0 - t0)

    area = (sum((b - a) * lg for a, b, lg in caixas) + tinta) / (W * H)
    folga = 1146 - caixas[-1][1]
    gaps = [caixas[i + 1][0] - caixas[i][1] for i in range(len(caixas) - 1)]
    ok = folga >= 0 and all(g >= 0 for g in gaps) and 0.18 <= area <= 0.30
    im.save(saida, quality=94)
    print("%-34s texto %4.1f%%  folga %4d  gaps %s  %s" %
          (os.path.basename(saida), area * 100, folga, [round(g) for g in gaps],
           "OK" if ok else "REFAZER"))
    return ok


if __name__ == "__main__":
    os.makedirs("meio", exist_ok=True)
    todos = True
    for p in json.load(open(sys.argv[1])):
        todos &= desenhar(p, "meio/%s.jpg" % p["slug"])
    print("todas OK" if todos else "ALGUMA PRECISA DE AJUSTE")
