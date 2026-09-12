# -*- coding: utf-8 -*-
"""Legenda do canal: Montserrat 800 caixa baixa + UMA palavra em Playfair 700 italic creme.
Blocos de ate 4 palavras / 26 caracteres, minimo 0,45 s, nunca atravessando corte.
y = 1478, altura 200. Sombra em duas camadas."""
import json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from plano import FALA, blocos

W, Y, ALT = 1080, 1478, 200
CREME = (255, 246, 224)
BRANCO = (255, 255, 255)
MAXP, MAXC, MINDUR = 4, 26, 0.45

LIGACAO = set("a o e de da do das dos que em no na nos nas um uma uns umas para por com "
              "se ao aos as à às pela pelo mais muito ja e é".split())

TROCA = {"lhe": "", "WhatsApp.": "whatsapp", "Instagram,": "instagram"}

# Erros que o reconhecimento comete SEMPRE, em qualquer take. Ao contrario do
# MANUAL abaixo, estes NAO sao por video -- ficam ligados para todo mundo.
#
# "o proximo cliente" sai "OU proximo cliente" em cinco dos treze takes. E o
# nome do canal: legenda queimada com a marca escrita errada e o pior erro que
# esta esteira pode cometer, e nao da para depender de alguem reparar a tempo.
# "em uma hora" vira "em minha hora" pelo mesmo motivo -- fala rapida.
#
# A correcao e por SEQUENCIA, nao por palavra solta: trocar todo "ou" por "o"
# quebraria as frases em que ele realmente diz "ou".
# Levantei todas as variantes nos treze takes: "ou proximo cliente" em cinco,
# "ao proximo cliente" em um, "mentoria proximo cliente" em um. Sao TRES
# palavras de propriedade: "ao proximo" e portugues legitimo fora deste
# contexto ("vamos ao proximo passo"), entao a regra so dispara com "cliente"
# na sequencia.
SEQUENCIAS = [
    (["ou", "próximo", "cliente"], ["o", "próximo", "cliente"]),
    (["ao", "próximo", "cliente"], ["o", "próximo", "cliente"]),
    (["em", "minha", "hora"], ["em", "uma", "hora"]),
]


def corrige(pal):
    for erro, certo in SEQUENCIAS:
        i = 0
        while i <= len(pal) - len(erro):
            if [p["t"] for p in pal[i:i + len(erro)]] == erro:
                for j, t in enumerate(certo):
                    pal[i + j]["t"] = t
                i += len(erro)
            else:
                i += 1
    return pal


# Onde a transcricao automatica erra, a palavra vai na mao com o tempo da FONTE.
# ATENCAO: isto e POR VIDEO. Esvazie os dois ao trocar de take.
MANUAL = {}
# gagueiras e palavras que invadem o trecho seguinte, por indice de FALA
FORA = set()


def carrega():
    tr = json.load(open("tr.json"))
    pal = [w for s in tr for w in s["w"]]
    _, ini = blocos()
    saida = []
    for i, (a, b, _) in enumerate(FALA):
        if i in MANUAL:
            fonte = [{"t": t, "s": s, "e": e} for t, s, e in MANUAL[i]]
        else:
            fonte = [w for w in pal if w["s"] >= a - 0.02 and w["s"] < b - 0.06]
        for w in fonte:
            t = TROCA.get(w["t"], w["t"]).strip(" ,.").lower()
            if not t or (i, t) in FORA:
                continue
            novo = {"t": t,
                    "ini": round(ini[i] + (w["s"] - a), 2),
                    "fim": round(ini[i] + (min(w["e"], b) - a), 2),
                    "seg": i}
            # enclise: "-lo", "-la", "-se" colam na palavra anterior em vez de
            # virar um bloco sozinho ("destrava" + "-lo" leem como texto quebrado)
            if t.startswith("-") and saida and saida[-1]["seg"] == i:
                saida[-1]["t"] += t
                saida[-1]["fim"] = novo["fim"]
                continue
            saida.append(novo)
    return corrige(saida)


def agrupa(pal):
    bl, cur = [], []
    for w in pal:
        novo = (not cur or cur[-1]["seg"] != w["seg"]
                or len(cur) >= MAXP
                or len(" ".join(x["t"] for x in cur) + " " + w["t"]) > MAXC)
        if novo and cur:
            bl.append(cur); cur = []
        cur.append(w)
    if cur:
        bl.append(cur)
    out = []
    for b in bl:
        ini, fim = b[0]["ini"], max(b[-1]["fim"], b[0]["ini"] + MINDUR)
        # nao atravessa o fim do trecho de fala
        out.append({"palavras": [x["t"] for x in b], "ini": ini, "fim": fim, "seg": b[0]["seg"]})
    for i in range(len(out) - 1):
        out[i]["fim"] = min(out[i]["fim"], out[i + 1]["ini"] - 0.01)
    return [b for b in out if b["fim"] - b["ini"] >= 0.20]


def destaque(pal):
    """A palavra em cursiva nunca e palavra de ligacao. Indice ZERO-BASED."""
    cand = [i for i, p in enumerate(pal) if p not in LIGACAO and len(p) > 3]
    if not cand:
        cand = [i for i, p in enumerate(pal) if p not in LIGACAO] or [len(pal) - 1]
    return max(cand, key=lambda i: len(pal[i]))


def desenha(pal, idx, path):
    im = Image.new("RGBA", (W, ALT), (0, 0, 0, 0))
    sans = ImageFont.truetype("fontes/Montserrat.ttf", 72)
    try:
        sans.set_variation_by_axes([800])
    except Exception:
        pass
    ital = ImageFont.truetype("fontes/Playfair-Italic.ttf", 78)
    try:
        ital.set_variation_by_axes([700])
    except Exception:
        pass
    d = ImageDraw.Draw(im)
    partes = [(p, ital if i == idx else sans, CREME if i == idx else BRANCO)
              for i, p in enumerate(pal)]
    esp = d.textlength(" ", font=sans)
    larg = sum(d.textlength(p, font=f) for p, f, _ in partes) + esp * (len(partes) - 1)
    x = (W - larg) / 2
    for p, f, c in partes:
        d.text((x, ALT / 2), p, font=f, fill=c, anchor="lm")
        x += d.textlength(p, font=f) + esp
    # sombra em duas camadas -- uma so some na camisa branca dele
    alpha = im.split()[3]
    s1 = Image.new("RGBA", im.size, (0, 0, 0, 0))
    s1.putalpha(alpha.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 165 / 255)))
    s2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
    s2.putalpha(alpha.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 225 / 255)))
    base = Image.new("RGBA", im.size, (0, 0, 0, 0))
    base.alpha_composite(s1)
    base.alpha_composite(s2, (0, 4))
    base.alpha_composite(im)
    base.save(path)


if __name__ == "__main__":
    os.makedirs("leg", exist_ok=True)
    bl = agrupa(carrega())
    meta = []
    for i, b in enumerate(bl):
        idx = destaque(b["palavras"])
        p = "leg/l%03d.png" % i
        desenha(b["palavras"], idx, p)
        meta.append({"png": p, "ini": b["ini"], "fim": b["fim"],
                     "txt": " ".join(b["palavras"]), "grifo": b["palavras"][idx]})
        print("%5.2f-%5.2f  %-28s  grifo: %s" % (b["ini"], b["fim"], " ".join(b["palavras"]), b["palavras"][idx]))
    json.dump(meta, open("leg/meta.json", "w"), ensure_ascii=False, indent=1)
    print("%d blocos" % len(meta))
