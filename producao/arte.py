# -*- coding: utf-8 -*-
"""Post de imagem do OPC, na identidade de opc.config.spec_publicar.
   python3 arte.py posts.json
posts.json: lista de {slug, foto, linha_sans, linha_cursiva, linha_apoio}"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from tipografia import paragrafo, PISO_PROMESSA

W, H = 1080, 1350
FUNDO = (11, 18, 32)        # #0B1220
CREME = (255, 246, 224)     # #FFF6E0
LARANJA = (255, 122, 26)    # #FF7A1A
APOIO = (170, 180, 195)     # #AAB4C3
BRANCO = (255, 255, 255)
SANS_PATH = "fontes/Montserrat.ttf"
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
    im = chapeu(degrade(cobrir(p["foto"])), FUNDO)
    im, brilho = scrim(im)
    d = ImageDraw.Draw(im)

    blocos = [
        (62,   "@oproximocliente", SANS_PATH,                    700, 34,  LARANJA),
        (716,  p["linha_sans"],    SANS_PATH,                    800, 86,  BRANCO),
        (812,  p["linha_cursiva"], "fontes/Playfair-Italic.ttf", 700, 176, CREME),
        (1016, p["linha_apoio"],   SANS_PATH,                    650, 52,  APOIO),
    ]
    # A assinatura subiu para o alto do quadro. Ela ocupava a ultima linha,
    # e o pe agora e da promessa -- que precisa de tres linhas grandes, nao
    # de uma tira de 26 px. Marca em cima, mensagem embaixo.
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
    sent = [(PROMESSA[0], fonte(SANS_PATH, PISO_PROMESSA, 600), CREME),
            (PROMESSA[1], fonte(SANS_PATH, PISO_PROMESSA + 4, 800), LARANJA)]
    fim_pe, tinta = paragrafo(d, sent, 1108, 970, W)

    gaps = [caixas[i + 1][0] - caixas[i][1] for i in range(len(caixas) - 1)]
    area = (sum(c[2] for c in caixas) + tinta) / (W * H)
    folga = 1088 - caixas[-1][1]
    ok = all(g >= 0 for g in gaps) and folga >= 0 and 0.18 <= area <= 0.30
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
