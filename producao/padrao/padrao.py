# -*- coding: utf-8 -*-
"""Sistema visual dos criativos do OPC — tres formatos, um so vocabulario.

POR QUE TRES E NAO UM. A REGRA V3 pede cinco anuncios por conjunto com
mensagens diferentes. Cinco variacoes do mesmo layout nao sao cinco criativos:
sao o defeito que a LISTA cataloga nos concorrentes (Bruno Deretti roda 14
anuncios com 2 headlines; Camila Becker repete o proprio nome em 10 cards).
Formatos diferentes disputam atencao de jeitos diferentes no mesmo feed.

O QUE ESTE ARQUIVO SUBSTITUI. A primeira versao era foto de banco com tarja
preta por cima — template, e pior, a tarja cobria metade da foto e a expressao
da pessoa contradizia a frase. Os tres formatos abaixo nasceram dessa critica:
em cada um a imagem carrega a mensagem em vez de decorar.

REGRAS DURAS (valem para qualquer peca nova):
  - 1080x1350. A conta inteira e 4:5; 1:1 sai cortado no feed.
  - Teto de 25% de texto (ordem do Pablo). `monta_lote` mede e RECUSA quem passar.
  - Nunca a foto do Pablo. Nunca preco, nunca promessa em reais, nunca "Rio",
    nunca "90 dias" — briefing da campanha.
  - Largura e negociavel, corpo de letra nao: `encaixa` reduz ate o piso e para.
    Se nao coube no piso, a copy e reescrita mais curta, nao a fonte diminuida.
  - Fontes reais (fontes.sh). Liberation/Arial da cara de PowerPoint.

Uso:
    ./producao/padrao/fontes.sh
    python3 producao/padrao/padrao.py            # gera os tres exemplos
    python3 producao/padrao/padrao.py --saida X  # noutro diretorio
"""
from __future__ import annotations

import argparse
import os
from PIL import Image, ImageDraw, ImageFont

L, A = 1080, 1350
MARGEM = 80
TETO_DE_TEXTO = 25.0

LARANJA = (255, 122, 26)
GRAFITE = (14, 16, 20)
CREME = (242, 240, 235)
BRANCO = (255, 255, 255)

MONT = "fontes/Montserrat.ttf"
PLAY = "fontes/Playfair-Italic.ttf"

ASSINATURA = "oproximocliente.com.br"


def fonte(caminho: str, corpo: int, peso: str = "Bold") -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(caminho, corpo)
    try:
        f.set_variation_by_name(peso)
    except Exception:
        pass  # fonte estatica: o peso ja vem no arquivo
    return f


def encaixa(caminho, texto, limite, piso, teto, peso="Bold"):
    """Maior corpo que cabe na largura, nunca abaixo do piso."""
    for corpo in range(teto, piso - 1, -2):
        f = fonte(caminho, corpo, peso)
        if f.getbbox(texto)[2] <= limite:
            return f
    return fonte(caminho, piso, peso)


def _pct(caixas) -> float:
    return 100 * sum((b[2] - b[0]) * (b[3] - b[1]) for b in caixas) / (L * A)


def _rodape(d, caixas, cor_texto, cor_linha, texto=ASSINATURA):
    """Fecha a peca. Sem isto sobram ~200px mortos no pe."""
    d.line([(MARGEM, A - 152), (L - MARGEM, A - 152)], fill=cor_linha, width=2)
    f = fonte(MONT, 32, "Bold")
    d.text((MARGEM, A - 120), texto, font=f, fill=cor_texto)
    caixas.append(f.getbbox(texto))


def _bloco(d, caixas, linhas, y, limite, piso, teto, espaco=20):
    """Empilha as linhas da chamada. Cada linha e (texto, fonte, cor, peso)."""
    for texto, caminho, cor, peso in linhas:
        f = encaixa(caminho, texto, limite, piso, teto, peso)
        b = f.getbbox(texto)
        d.text((MARGEM, y - b[1]), texto, font=f, fill=cor)
        caixas.append(b)
        y += (b[3] - b[1]) + espaco
    return y


# ─────────────────────────────────────────────────────────────────────
# FORMATO 1 — AGENDA. A imagem E o argumento: trinta horarios, dois
# ocupados. Nenhuma das 178 paginas da LISTA desenha isso.
# ─────────────────────────────────────────────────────────────────────
def agenda(chamada, apoio, kicker="SUA SEMANA", ocupados=((1, 2), (3, 4))):
    im = Image.new("RGB", (L, A), GRAFITE)
    d = ImageDraw.Draw(im)
    cx = []

    f_k = fonte(MONT, 30, "Bold")
    d.text((MARGEM, 96), kicker, font=f_k, fill=LARANJA)
    cx.append(f_k.getbbox(kicker))

    larg, alt, gap, y0 = 172, 74, 12, 186
    f_d = fonte(MONT, 26, "SemiBold")
    for i, dia in enumerate(["SEG", "TER", "QUA", "QUI", "SEX"]):
        d.text((MARGEM + i * (larg + gap) + 6, y0), dia, font=f_d, fill=(120, 127, 140))
        cx.append(f_d.getbbox(dia))

    ocupados = set(map(tuple, ocupados))
    yb = y0 + 46
    for linha in range(6):
        for col in range(5):
            x = MARGEM + col * (larg + gap)
            y = yb + linha * (alt + gap)
            if (col, linha) in ocupados:
                d.rounded_rectangle([x, y, x + larg, y + alt], 8, fill=(38, 42, 50))
                d.rectangle([x, y, x + 6, y + alt], fill=LARANJA)
            else:
                d.rounded_rectangle([x, y, x + larg, y + alt], 8,
                                    outline=(34, 38, 46), width=2)

    y = _bloco(d, cx, chamada, yb + 6 * (alt + gap) + 54, L - 160, 56, 86, 18)
    f_ap = fonte(MONT, 32, "Medium")
    d.text((MARGEM, y + 16), apoio, font=f_ap, fill=(150, 157, 170))
    cx.append(f_ap.getbbox(apoio))
    _rodape(d, cx, BRANCO, (52, 58, 68))
    return im, _pct(cx)


# ─────────────────────────────────────────────────────────────────────
# FORMATO 2 — PERGUNTA. Fundo claro de proposito: nas varreduras de hoje
# (1.793 anuncios de imobiliaria, 201 de holding) o feed inteiro e escuro
# e saturado. O creme para o dedo. A pergunta e do leitor sobre o negocio
# dele — nao e promessa nossa, e o briefing proibe promessa.
# ─────────────────────────────────────────────────────────────────────
def pergunta(chamada, apoio, kicker="DONO DE EMPRESA"):
    im = Image.new("RGB", (L, A), CREME)
    d = ImageDraw.Draw(im)
    cx = []

    d.rectangle([MARGEM, 222, MARGEM + 96, 232], fill=LARANJA)
    f_k = fonte(MONT, 28, "Bold")
    d.text((MARGEM, 272), kicker, font=f_k, fill=(138, 132, 120))
    cx.append(f_k.getbbox(kicker))

    y = _bloco(d, cx, chamada, 392, L - 160, 62, 104, 26)
    f_ap = fonte(MONT, 34, "Medium")
    for i, linha in enumerate(apoio):
        d.text((MARGEM, y + 40 + i * 48), linha, font=f_ap, fill=(96, 92, 86))
        cx.append(f_ap.getbbox(linha))
    _rodape(d, cx, (24, 24, 26), (206, 202, 194))
    return im, _pct(cx)


# ─────────────────────────────────────────────────────────────────────
# FORMATO 3 — FOTO. Sem tarja: o escuro e um degrade so na coluna onde a
# foto ja era vazia, entao o rosto continua vivo. A foto precisa ter
# espaco negativo a esquerda E expressao que concorde com a frase.
# ─────────────────────────────────────────────────────────────────────
def foto(caminho_foto, chamada, apoio, kicker="PARA QUEM JÁ FATURA"):
    im = Image.open(caminho_foto).convert("RGB")
    escala = max(L / im.width, A / im.height)
    im = im.resize((round(im.width * escala), round(im.height * escala)), Image.LANCZOS)
    im = im.crop(((im.width - L) // 2, 0, (im.width - L) // 2 + L, A))

    veu = Image.new("L", (L, 1), 0)
    for x in range(L):
        t = max(0.0, 1 - x / (L * 0.72))
        veu.putpixel((x, 0), int(228 * t ** 0.8))
    im = Image.composite(Image.new("RGB", (L, A), (8, 10, 14)), im, veu.resize((L, A)))

    d = ImageDraw.Draw(im)
    cx = []
    f_k = fonte(MONT, 28, "Bold")
    d.text((MARGEM, 150), kicker, font=f_k, fill=LARANJA)
    cx.append(f_k.getbbox(kicker))

    y = _bloco(d, cx, chamada, 226, 560, 62, 98, 16)
    f_ap = fonte(MONT, 32, "Medium")
    for i, linha in enumerate(apoio):
        d.text((MARGEM, y + 34 + i * 44), linha, font=f_ap, fill=(178, 184, 196))
        cx.append(f_ap.getbbox(linha))
    _rodape(d, cx, BRANCO, (70, 76, 88))
    return im, _pct(cx)


def monta_lote(pecas, saida="entregas/campanha/imagens"):
    """Gera e mede. Peca acima do teto nao e salva — a copy e que encurta."""
    os.makedirs(saida, exist_ok=True)
    recusadas = []
    for nome, fn, args in pecas:
        im, pct = fn(*args)
        if pct > TETO_DE_TEXTO:
            recusadas.append((nome, pct))
            print(f"  {nome}: {pct:.1f}% — RECUSADA, encurte a chamada")
            continue
        im.save(os.path.join(saida, f"{nome}.jpg"), quality=94)
        print(f"  {nome}: {pct:.1f}% de texto — ok")
    return recusadas


EXEMPLOS = [
    ("PAD1_agenda", agenda, (
        [("Duas reuniões.", MONT, BRANCO, "Bold"),
         ("O resto é espera.", PLAY, LARANJA, "Bold")],
        "Lead não falta. Falta quem ligue.")),
    ("PAD2_pergunta", pergunta, (
        [("Dos seus últimos", MONT, (24, 24, 26), "Bold"),
         ("30 leads,", MONT, (24, 24, 26), "Black"),
         ("quantos viraram", MONT, (24, 24, 26), "Bold"),
         ("reunião?", PLAY, LARANJA, "Bold")],
        ["Se você não sabe responder,", "o problema não é o tráfego."])),
]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--saida", default="entregas/campanha/imagens")
    p.add_argument("--foto", help="foto para o formato 3 (espaco livre a esquerda)")
    a = p.parse_args()

    pecas = list(EXEMPLOS)
    if a.foto:
        pecas.append(("PAD3_foto", foto, (
            a.foto,
            [("Você não", MONT, BRANCO, "Black"),
             ("precisa de", MONT, BRANCO, "Black"),
             ("mais lead.", PLAY, LARANJA, "Bold")],
            ["Precisa de agenda", "cheia na segunda."])))
    recusadas = monta_lote(pecas, a.saida)
    raise SystemExit(1 if recusadas else 0)


if __name__ == "__main__":
    main()
