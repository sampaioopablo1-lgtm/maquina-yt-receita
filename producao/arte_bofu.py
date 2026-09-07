# -*- coding: utf-8 -*-
"""Arte de FUNDO DE FUNIL da mentoria O Proximo Cliente.

Por que e diferente da arte de topo (arte.py / arte2.py):
o topo entrega um pensamento, o fundo entrega uma OFERTA. Entao ganha tres
elementos que o topo nao tem -- etiqueta de turma no alto, numero como heroi
quando ele e o argumento, e barra de CTA solida no pe. Sem barra de CTA nao
e fundo de funil, e post bonito.

Referencia estudada em 07/09/2026 na Biblioteca de Anuncios da Meta (BR):
so 7 anuncios ativos nesse posicionamento, quase todos emoji + promessa de
renda ("R$ 20k por semana"). O caminho contrario -- sobrio, numero real,
sem promessa de faturamento -- e o que separa esta peca daquele bolo.

Dois modos:
  "foto"  -- retrato do Pablo, degrade colorido no pe, texto embaixo
  "tipo"  -- fundo escuro da marca, o numero/palavra e o heroi

python3 arte_bofu.py bofu.json
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1350
LARANJA = (255, 122, 26)
CREME = (255, 246, 224)
BRANCO = (255, 255, 255)
APOIO = (255, 214, 176)
GRAFITE = (17, 17, 22)
LARG_MAX = 950

FUNDOS = {"vinho": (58, 12, 20), "grafite": (24, 22, 28), "petroleo": (10, 34, 44),
          "terra": (52, 26, 12), "roxo": (34, 14, 46), "escuro": (11, 18, 32)}


def fonte(path, corpo, peso):
    f = ImageFont.truetype(path, corpo)
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


SANS = "fontes/Montserrat.ttf"
ITAL = "fontes/Playfair-Italic.ttf"


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
    return y, y + (b - t), (r - l), x


def cobrir(foto, alto=0.35):
    im = Image.open(foto).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x0 = (im.width - W) // 2
    y0 = int((im.height - H) * alto)
    im = im.crop((x0, y0, x0 + W, y0 + H))
    im = ImageEnhance.Color(im).enhance(1.18)
    return ImageEnhance.Contrast(im).enhance(1.10)


def degrade(im, cor, y_ini=560):
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


def scrim(im, cor, y0=700):
    for _ in range(8):
        if brilho(im, 820, 1180) <= 62:
            break
        sombra = Image.new("RGB", (W, H), cor)
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).rectangle((0, y0, W, H), fill=95)
        im = Image.composite(sombra, im, m.filter(ImageFilter.GaussianBlur(60)))
    return im


def etiqueta(d, txt):
    """Tarja de turma no alto. E ela que diz 'isto e uma oferta', nao um post."""
    f = fonte(SANS, 26, 700)
    l, t, r, b = d.textbbox((0, 0), txt, font=f)
    lw, lh = (r - l) + 56, (b - t) + 30
    x0, y0 = (W - lw) / 2, 62
    d.rounded_rectangle((x0, y0, x0 + lw, y0 + lh), radius=lh / 2, fill=LARANJA)
    d.text((x0 + 28 - l, y0 + 15 - t), txt, font=f, fill=GRAFITE)


def botao(d, principal, apoio):
    """Barra de CTA. Solida, cor cheia, texto escuro: tem que parecer clicavel."""
    f = fonte(SANS, 40, 800)
    l, t, r, b = d.textbbox((0, 0), principal, font=f)
    bw, bh = W - 150, 108
    x0, y0 = 75, 1128
    d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius=16, fill=LARANJA)
    d.text(((W - (r - l)) / 2 - l, y0 + (bh - (b - t)) / 2 - t), principal, font=f, fill=GRAFITE)
    fa = fonte(SANS, 24, 600)
    la, ta, ra, ba = d.textbbox((0, 0), apoio, font=fa)
    d.text(((W - (ra - la)) / 2 - la, 1258 - ta), apoio, font=fa, fill=APOIO)


def desenhar(p, saida):
    cor = FUNDOS[p.get("fundo", "grafite")]
    if p.get("modo") == "tipo":
        im = Image.new("RGB", (W, H), cor)
        d = ImageDraw.Draw(im)
        # textura discreta: um halo laranja atras do numero, para nao ficar chapado
        halo = Image.new("RGB", (W, H), cor)
        hd = ImageDraw.Draw(halo)
        hd.ellipse((W / 2 - 420, 380, W / 2 + 420, 900), fill=(min(255, cor[0] + 46),
                                                               min(255, cor[1] + 20), cor[2]))
        im = Image.blend(im, halo.filter(ImageFilter.GaussianBlur(150)), 0.55)
        d = ImageDraw.Draw(im)
    else:
        im = scrim(degrade(cobrir(p["foto"], p.get("alto", 0.32)), cor), cor)
        d = ImageDraw.Draw(im)

    etiqueta(d, p.get("etiqueta", "MENTORIA O PRÓXIMO CLIENTE"))

    y = p.get("y", 830)
    caixas = []
    if p.get("riscado"):
        f = cabe(d, p["riscado"], SANS, 800, 88)
        y0, y1, larg, x = centrar(d, p["riscado"], f, y, (196, 196, 206))
        d.line((x - 6, (y0 + y1) / 2, x + larg + 6, (y0 + y1) / 2), fill=(214, 60, 50), width=9)
        caixas.append((y0, y1)); y = y1 + 22

    f = cabe(d, p["linha_sans"], SANS, 800, p.get("corpo_sans", 58))
    y0, y1, _, _ = centrar(d, p["linha_sans"], f, y, BRANCO)
    caixas.append((y0, y1)); y = y1 + p.get("gap", 14)

    f = cabe(d, p["linha_cursiva"], ITAL, 700, p.get("corpo_cursiva", 132))
    y0, y1, _, _ = centrar(d, p["linha_cursiva"], f, y, LARANJA)
    caixas.append((y0, y1)); y = y1 + 34

    if p.get("linha_apoio"):
        f = cabe(d, p["linha_apoio"], SANS, 600, 32)
        y0, y1, _, _ = centrar(d, p["linha_apoio"], f, y, APOIO, sombra=False)
        caixas.append((y0, y1))

    botao(d, p.get("cta", "PREENCHER APLICAÇÃO"),
          p.get("cta_apoio", "3 perguntas · turma de setembro · vagas limitadas"))

    folga = min(1128 - caixas[-1][1], 999)
    gaps = [caixas[i + 1][0] - caixas[i][1] for i in range(len(caixas) - 1)]
    ok = folga >= 0 and all(g >= 0 for g in gaps)
    im.save(saida, quality=94)
    print("%-32s folga p/ botao %4d  gaps %s  %s" %
          (os.path.basename(saida), folga, [round(g) for g in gaps], "OK" if ok else "REFAZER"))
    return ok


if __name__ == "__main__":
    os.makedirs("bofu", exist_ok=True)
    todos = True
    for p in json.load(open(sys.argv[1])):
        todos &= desenhar(p, "bofu/%s.jpg" % p["slug"])
    print("todas OK" if todos else "ALGUMA PRECISA DE AJUSTE")
