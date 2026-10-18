# -*- coding: utf-8 -*-
"""O modelo do V10 — o unico criativo da conta que gera lead.

Apurado em 11/09/2026: dos dez anuncios dos conjuntos de formulario, nove
sao video e nenhum entregou. O decimo, chamado "V10 — Cliente todo dia
(video E)", **e uma imagem** (object_type SHARE, com image_hash) e sozinho
fez 4 leads a R$2,24, com CTR de 3,1% a 3,5%. O nome mentia, e por pouco
nao foi pausado junto com os videos.

Entao a imagem ja tinha ganhado dos nove videos. Este arquivo transforma
essa peca em MODELO, para as proximas nascerem iguais a ela.

Estrutura, medida na peca original (BF02_whatsapp_cheio):

    pilula laranja no topo, texto preto em caixa alta
    foto cobrindo o quadro 4:5
    degrade escuro subindo do pe, para o texto ter onde pousar
    linha sans branca  ->  linha cursiva laranja grande  ->  linha de apoio creme
    barra de CTA laranja solida no pe

O que NAO muda entre variacoes: cor, fonte, posicao, barra. So mudam a foto
e as tres linhas. E isso que faz dez pecas parecerem uma campanha em vez de
dez anuncios soltos.

    python3 fabrica/modelo_v10.py pecas.json

As fontes vem de caminhos.raiz()/fontes (o repositorio tem portao contra
literal de workdir escrito a mao — ver tests/test_caminhos.py).
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import caminhos  # noqa: E402

L, A = 1080, 1350
LARANJA = (255, 122, 26)
BRANCO = (255, 255, 255)
APOIO = (255, 214, 176)
GRAFITE = (17, 17, 22)
LARG_MAX = 950
PISO = 34

FUNDOS = {"petroleo": (10, 34, 44), "grafite": (24, 22, 28), "vinho": (58, 12, 20),
          "terra": (52, 26, 12), "roxo": (34, 14, 46), "escuro": (11, 18, 32)}


def dir_fontes():
    return os.path.join(caminhos.raiz(), "fontes")


def fonte(nome, corpo):
    return ImageFont.truetype(os.path.join(dir_fontes(), nome), corpo)


def sans(corpo):
    return fonte("Montserrat-Bold.ttf", corpo)


def italico(corpo):
    return fonte("Playfair-Italic.ttf", corpo)


def cabe(d, txt, familia, corpo, larg=LARG_MAX):
    """Encolhe ate caber, nunca abaixo do piso.

    Largura e negociavel, corpo de letra nao: abaixo de 34px a linha some no
    feed. Se nem no piso couber, a peca volta no piso e quem conserta e o
    texto, nao o layout.
    """
    while corpo > PISO:
        f = familia(corpo)
        if d.textlength(txt, font=f) <= larg:
            return f
        corpo -= 2
    return familia(PISO)


def cobrir(caminho, alto=0.30):
    """Recorta em 4:5 sem distorcer, privilegiando o alto do quadro."""
    im = Image.open(caminho).convert("RGB")
    e = max(L / im.width, A / im.height)
    im = im.resize((int(im.width * e + 1), int(im.height * e + 1)), Image.LANCZOS)
    x = (im.width - L) // 2
    y = int((im.height - A) * alto)
    return im.crop((x, y, x + L, y + A))


def degrade(im, cor):
    """Escurece o pe. Sem isto o texto branco some sobre foto clara."""
    capa = Image.new("RGB", (L, A), cor)
    masc = Image.new("L", (1, A))
    for y in range(A):
        t = max(0.0, (y - A * 0.34) / (A * 0.66))
        masc.putpixel((0, y), int(255 * min(1.0, t ** 1.45)))
    im.paste(capa, (0, 0), masc.resize((L, A)))
    return im


def chapeu(im, cor):
    """Escurecida leve no topo, para a pilula laranja destacar."""
    capa = Image.new("RGB", (L, A), cor)
    masc = Image.new("L", (1, A))
    for y in range(A):
        masc.putpixel((0, y), int(150 * max(0.0, 1 - y / (A * 0.22))))
    im.paste(capa, (0, 0), masc.resize((L, A)))
    return im


def tratar(im, cor):
    """Mesmo tratamento de cor em todas: dez fotos de banco viram uma campanha."""
    im = ImageEnhance.Color(im).enhance(0.80)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    return Image.blend(im, Image.new("RGB", im.size, cor), 0.10)


def etiqueta(d, txt):
    f = sans(34)
    lg = d.textlength(txt, font=f)
    px, alt = 34, 78
    x0 = (L - (lg + px * 2)) / 2
    d.rounded_rectangle((x0, 42, x0 + lg + px * 2, 42 + alt), radius=alt / 2, fill=LARANJA)
    d.text((x0 + px, 42 + 17), txt, font=f, fill=GRAFITE)
    return 42 + alt


def centrar(d, txt, f, y, cor):
    lg = d.textlength(txt, font=f)
    a, b = f.getbbox(txt)[1], f.getbbox(txt)[3]
    d.text(((L - lg) / 2, y - a), txt, font=f, fill=cor)
    return y + (b - a)


def barra(d, txt):
    """A barra espelha o botao real, que fica ABAIXO do criativo e e escolhido
    na campanha. Ela existe porque sem barra no pe a peca de fundo de funil
    vira post bonito e nao anuncio."""
    f = sans(52)
    y0, alt = 1160, 118
    d.rounded_rectangle((48, y0, L - 48, y0 + alt), radius=16, fill=LARANJA)
    lg = d.textlength(txt, font=f)
    d.text(((L - lg) / 2, y0 + 30), txt, font=f, fill=GRAFITE)


def compor(p, saida):
    cor = FUNDOS[p.get("fundo", "petroleo")]
    im = tratar(degrade(chapeu(cobrir(p["foto"], p.get("alto", 0.30)), cor), cor), cor)
    d = ImageDraw.Draw(im)
    fim_topo = etiqueta(d, p["etiqueta"])

    y = p.get("y", 826)
    y = centrar(d, p["linha_sans"], cabe(d, p["linha_sans"], sans, p.get("corpo_sans", 72)),
                y, BRANCO) + 12
    y = centrar(d, p["linha_cursiva"],
                cabe(d, p["linha_cursiva"], italico, p.get("corpo_cursiva", 148)),
                y, LARANJA) + 30
    y = centrar(d, p["linha_apoio"], sans(38), y, APOIO)

    folga = 1160 - y
    barra(d, p["cta"])
    im.save(saida, quality=94)
    ok = folga >= 10 and y > fim_topo
    print("%-34s folga %4d  %s" % (os.path.basename(saida), folga, "OK" if ok else "REFAZER"))
    return ok


def main(lista, destino):
    pecas = json.load(open(lista, encoding="utf-8"))
    os.makedirs(destino, exist_ok=True)
    bom = all([compor(p, os.path.join(destino, "%s.jpg" % p["slug"])) for p in pecas])
    print("todas OK" if bom else "ALGUMA PRECISA REFAZER")
    return 0 if bom else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "saida"))
