# Monta as imagens-guia do playbook (ligação normal e ligação pelo WhatsApp), com dados de lead borrados.
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def fonte(n):
    for f in ("C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"):
        try:
            return ImageFont.truetype(f, n)
        except OSError:
            pass
F = fonte(24); FT = fonte(32); V = (229, 32, 32)

def borra(im, *boxes):
    for b in boxes:
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(10)), b)

def seta(d, a, b, w=6):
    d.line([a, b], fill=V, width=w)
    ang = math.atan2(b[1] - a[1], b[0] - a[0]); L = 22
    d.polygon([b, (b[0] - L * math.cos(ang - .45), b[1] - L * math.sin(ang - .45)),
               (b[0] - L * math.cos(ang + .45), b[1] - L * math.sin(ang + .45))], fill=V)

def rot(d, n, txt, pos):
    x, y = pos; w = d.textlength(txt, font=F) + 72
    d.rounded_rectangle((x, y, x + w, y + 46), 12, fill=V); d.ellipse((x + 8, y + 7, x + 40, y + 39), fill="white")
    d.text((x + 24, y + 23), str(n), font=F, fill=V, anchor="mm"); d.text((x + 52, y + 9), txt, font=F, fill="white")
    return (x, y, x + w, y + 46)

def marca(d, box, n, txt, pos):
    d.rectangle(box, outline=V, width=5); r = rot(d, n, txt, pos)
    cx = (box[0] + box[2]) / 2; cy = (box[1] + box[3]) / 2
    if r[0] <= cx <= r[2] and r[1] <= cy <= r[3]:
        return
    sx = min(max(cx, r[0] + 20), r[2] - 20)
    sy = r[3] if cy > r[3] else (r[1] if cy < r[1] else (r[1] + r[3]) / 2)
    tx = min(max(sx, box[0] + 10), box[2] - 10)
    ty = box[1] - 4 if sy < box[1] else (box[3] + 4 if sy > box[3] else cy)
    if abs(tx - sx) + abs(ty - sy) > 30:
        seta(d, (sx, sy), (tx, ty))

def painel(im, titulo):
    out = Image.new("RGB", (1500, im.height + 70), (255, 255, 255)); out.paste(im, (0, 70))
    dd = ImageDraw.Draw(out); dd.rectangle((0, 0, 1500, 70), fill=(16, 24, 40)); dd.text((20, 16), titulo, font=FT, fill="white")
    return out, 70

def pilha(ps, nome):
    H = sum(p.height for p in ps) + 20 * (len(ps) - 1); out = Image.new("RGB", (1500, H), (255, 255, 255)); y = 0
    for p in ps:
        out.paste(p, (0, y)); y += p.height + 20
    out.save(nome); print(nome, out.size)

def ficha(canal, n0, com_ligar):
    im = Image.open("pb2_ficha.png").convert("RGB")
    borra(im, (305, 166, 420, 196), (628, 298, 745, 328), (268, 580, 420, 604), (1170, 513, 1265, 535), (1117, 198, 1433, 356))
    p, o = painel(im, "Na ficha do lead"); d = ImageDraw.Draw(p); n = n0
    if com_ligar:
        marca(d, (783, 293 + o, 860, 330 + o), n, "Ligar (número fixo da empresa)", (380, 215 + o)); n += 1
    marca(d, (1455, 262 + o, 1493, 304 + o), n, "Observações (lápis): abre a nota amarela", (820, 120 + o)); n += 1
    marca(d, (1122, 372 + o, 1345, 412 + o), n, "Abrir formulário + agenda", (620, 560 + o)); n += 1
    marca(d, (257, 612 + o, 543, 738 + o), n, "Ao desligar: Canal = %s + Resultado" % canal, (260, 480 + o)); n += 1
    return p, n

def form(n):
    im = Image.open("form_test2.png").convert("RGB").crop((0, 0, 900, 1650)); borra(im, (60, 100, 840, 350))
    k = 0.62; im = im.resize((int(900 * k), int(1650 * k)))
    base = Image.new("RGB", (1500, im.height), (255, 255, 255)); base.paste(im, (40, 0))
    p, o = painel(base, "O formulário abre preenchido"); d = ImageDraw.Draw(p)
    marca(d, (40 + 60 * k, 720 * k + o, 40 + 840 * k, 1380 * k + o), n, "Complete Q1 a Q6 (o que veio do anúncio já está lá)", (640, 560 + o))
    marca(d, (40 + 60 * k, 1550 * k + o, 40 + 840 * k, 1605 * k + o), n + 1, "Enviar e agendar reunião → abre a agenda do closer", (640, 940 + o))
    return p

# ===== ligação normal
im = Image.open("pb1_lista.png").convert("RGB"); borra(im, (305, 272, 528, 862), (535, 272, 762, 862))
p1, o = painel(im, "LIGAÇÃO NORMAL (telefone) — um por vez, pela Minha fila"); d = ImageDraw.Draw(p1)
marca(d, (782, 100 + o, 928, 146 + o), 1, "Contatos → Listas inteligentes → Minha fila — SDR", (560, 160 + o))
marca(d, (305, 274 + o, 528, 300 + o), 2, "Clique no nome do lead de cima (os quentes vêm primeiro)", (560, 330 + o))
f, n = ficha("Telefone", 3, True)
pilha([p1, f, form(n)], "guia_ligacao_normal.png")

# ===== ligação pelo WhatsApp
im = Image.open("pb4_callcenter.png").convert("RGB"); borra(im, (438, 535, 1255, 617))
p1, o = painel(im, "LIGAÇÃO PELO WHATSAPP — Call Center em lote, tag fila-wa"); d = ImageDraw.Draw(p1)
rot(d, 1, "Botão roxo Call Center (no alto da tela)", (20, 90))
marca(d, (229, 303 + o, 400, 345 + o), 2, "Fila de ligações", (20, 400 + o))
marca(d, (846, 298 + o, 1247, 336 + o), 3, "Aba Tag → escolha fila-wa", (900, 230 + o))
marca(d, (440, 398 + o, 1249, 437 + o), 4, "Puxar contatos desta tag", (470, 480 + o))
marca(d, (850, 655 + o, 1260, 699 + o), 5, "Pausa: 30 s ou mais", (1000, 590 + o))
marca(d, (430, 716 + o, 1260, 766 + o), 6, "Iniciar discagem", (560, 790 + o))
im = Image.open("pb3_busca.png").convert("RGB"); borra(im, (312, 112, 400, 140), (333, 266, 700, 306), (333, 366, 440, 390))
p2, o = painel(im, "O lead atendeu: abra a ficha dele"); d = ImageDraw.Draw(p2)
marca(d, (283, 104 + o, 1222, 148 + o), 7, "Aperte Ctrl+K e digite o nome ou o telefone", (300, 520 + o))
marca(d, (280, 260 + o, 1222, 314 + o), 8, "Enter (ou Abrir) no contato", (700, 600 + o))
f, n = ficha("WhatsApp", 9, False)
pilha([p1, p2, f, form(n)], "guia_ligacao_whatsapp.png")
