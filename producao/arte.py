# -*- coding: utf-8 -*-
"""Post de imagem do OPC, na identidade de opc.config.spec_publicar.
   python3 arte.py posts.json
posts.json: lista de {slug, foto, linha_sans, linha_cursiva, linha_apoio}"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
FUNDO = (11, 18, 32)        # #0B1220
CREME = (255, 246, 224)     # #FFF6E0
LARANJA = (255, 122, 26)    # #FF7A1A
APOIO = (170, 180, 195)     # #AAB4C3
BRANCO = (255, 255, 255)
LARG_MAX = 960
LIMITE_TEXTO = 0.20 * W * H

# A mensagem central da mentoria, em destaque nas dez artes de topo (pedido do
# Pablo em 07/09/2026). Ela e a MESMA string do arte2.py e do arte_bofu.py: se
# mudar, muda nos tres -- promessa que varia de arte para arte nao vira memoria
# de ninguem. "aprenda", nao "receba": e o que separa mentoria de agencia.
PROMESSA = ["aprenda a criar anúncios que trazem cliente todo dia no seu WhatsApp",
            "sem agência e sem investir alto"]


def fonte(path, corpo, peso):
    f = ImageFont.truetype(path, corpo)
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


def cabe(draw, txt, path, peso, corpo, larg=LARG_MAX):
    """Reduz o corpo ate a linha caber na largura pedida."""
    while corpo > 20:
        f = fonte(path, corpo, peso)
        if draw.textlength(txt, font=f) <= larg:
            return f
        corpo -= 2
    return fonte(path, corpo, peso)


def cobrir(foto):
    im = Image.open(foto).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x0 = (im.width - W) // 2
    y0 = (im.height - H) // 2
    return im.crop((x0, y0, x0 + W, y0 + H))


def degrade(im, y_ini=660):
    """Degrade para o fundo a partir de y_ini ate o pe do quadro."""
    base = im.copy()
    px = base.load()
    for y in range(y_ini, H):
        t = (y - y_ini) / (H - y_ini)
        t = t * t * (3 - 2 * t)  # suave
        for x in range(W):
            r, g, b = px[x, y]
            px[x, y] = (round(r + (FUNDO[0] - r) * t),
                        round(g + (FUNDO[1] - g) * t),
                        round(b + (FUNDO[2] - b) * t))
    return base


def brilho_faixa(im, y0=840, y1=1300):
    g = im.convert("L").crop((0, y0, W, y1))
    h = g.histogram()
    n = sum(h)
    return sum(i * c for i, c in enumerate(h)) / n


def scrim(im):
    """Escurece a faixa do texto ate o brilho medio ficar abaixo de 52."""
    for _ in range(8):
        b = brilho_faixa(im)
        if b <= 52:
            return im, b
        sombra = Image.new("RGB", (W, H), FUNDO)
        mask = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(mask)
        md.rectangle((0, 780, W, H), fill=90)
        mask = mask.filter(ImageFilter.GaussianBlur(60))
        im = Image.composite(sombra, im, mask)
    return im, brilho_faixa(im)


def desenhar(p, saida):
    im = degrade(cobrir(p["foto"]))
    im, brilho = scrim(im)
    d = ImageDraw.Draw(im)

    blocos = [
        (766,  p["linha_sans"],    "fontes/Montserrat.ttf",      800, 86,  BRANCO),
        (862,  p["linha_cursiva"], "fontes/Playfair-Italic.ttf", 700, 176, CREME),
        (1064, p["linha_apoio"],   "fontes/Montserrat.ttf",      650, 52,  APOIO),
        (1262, "@oproximocliente", "fontes/Montserrat.ttf",      700, 34,  LARANJA),
    ]
    caixas = []
    for y_topo, txt, path, peso, corpo, cor in blocos:
        # frase curta ("e sumiu") nao enche a linha e derruba a densidade da
        # peca inteira. corpo_cursiva/corpo_sans no json compensam caso a caso.
        if txt == p.get("linha_cursiva"):
            corpo = p.get("corpo_cursiva", corpo)
        elif txt == p.get("linha_sans"):
            corpo = p.get("corpo_sans", corpo)
        f = cabe(d, txt, path, peso, corpo)
        l, t, r, b = d.textbbox((0, 0), txt, font=f)
        x = (W - (r - l)) / 2 - l
        # y e o TOPO da caixa: compensa o bbox_top da fonte
        d.text((x, y_topo - t), txt, font=f, fill=cor)
        caixas.append((y_topo, y_topo + (b - t), (r - l) * (b - t)))

    # A faixa da promessa toma o lugar do filete: o filete so separava, a faixa
    # separa E diz o que eu faco. Fundo cheio porque texto pequeno sobre pele
    # nao le.
    # A promessa NAO vai em barra solida aqui. No fundo de funil a barra laranja
    # significa "clique"; no topo nao ha o que clicar, e barra no pe faz a peca
    # PARECER anuncio -- que e justamente o que encarece o alcance numa campanha
    # de reconhecimento. O post de dor funciona porque nao parece anuncio.
    # Entao: filete fino em cima, texto creme embaixo. Presente e legivel, sem
    # imitar o CTA da outra campanha.
    d.rectangle(((W - 120) // 2, 1132, (W + 120) // 2, 1136), fill=LARANJA)
    yy = 1152
    tinta = 0          # a promessa do pe conta na area: e texto na imagem
    for i, t in enumerate(PROMESSA):
        f = cabe(d, t, "fontes/Montserrat.ttf", 600 if i == 0 else 800, 36, 970)
        l0, t0, r0, b0 = d.textbbox((0, 0), t, font=f)
        x0 = (W - (r0 - l0)) / 2 - l0
        d.text((x0 + 2, yy - t0 + 2), t, font=f, fill=(0, 0, 0))
        tinta += (r0 - l0) * (b0 - t0)
        d.text((x0, yy - t0), t, font=f, fill=CREME if i == 0 else LARANJA)
        yy += (b0 - t0) + 9

    # conferencias que a receita exige
    gaps = [caixas[i + 1][0] - caixas[i][1] for i in range(len(caixas) - 1)]
    area = (sum(c[2] for c in caixas) + tinta) / (W * H)
    ok = all(g >= 0 for g in gaps) and 0.18 <= area <= 0.30
    im.save(saida, quality=94)
    print("%-28s brilho %5.1f  gaps %s  texto %4.1f%%  %s" %
          (os.path.basename(saida), brilho, [round(g) for g in gaps], area * 100,
           "OK" if ok else "REFAZER"))
    return ok


if __name__ == "__main__":
    posts = json.load(open(sys.argv[1]))
    os.makedirs("artes", exist_ok=True)
    todos = True
    for p in posts:
        todos &= desenhar(p, "artes/%s.jpg" % p["slug"])
    print("todas OK" if todos else "ALGUMA PRECISA DE AJUSTE")
