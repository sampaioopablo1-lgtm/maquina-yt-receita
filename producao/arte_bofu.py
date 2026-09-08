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
from tipografia import paragrafo, PISO_APOIO, PISO_PROMESSA, PISO_CTA

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


def cabe(d, txt, path, peso, corpo, larg=LARG_MAX, piso=34):
    """Encolhe ate caber -- mas nunca abaixo do piso.

    Antes o piso era 18 px, o que na pratica e "sem piso": a linha sumia e a
    peca passava no portao mesmo assim. Agora, se o texto nao couber no piso,
    ele volta NO PISO e o portao la embaixo reprova. Corrigir e reescrever o
    texto mais curto, nao diminuir a letra.
    """
    while corpo > piso:
        f = fonte(path, corpo, peso)
        if d.textlength(txt, font=f) <= larg:
            return f
        corpo -= 2
    return fonte(path, piso, peso)


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


def chapeu(im, cor, ate=360):
    """Escurece o TOPO do quadro.

    Necessario desde que a promessa passou a ocupar tres linhas grandes no alto
    (08/09/2026): antes ela era uma tira fina de 26 px e cabia em qualquer
    fundo; agora atravessa o rosto. Sem isto o texto branco encosta na pele e
    perde contorno, que e o mesmo defeito de legibilidade -- so que na outra
    ponta do quadro.
    """
    px = im.load()
    for y in range(ate):
        t = 1 - (y / ate)
        t = t * t * (3 - 2 * t) * 0.88
        for x in range(W):
            r, g, b = px[x, y]
            px[x, y] = (round(r + (cor[0] - r) * t), round(g + (cor[1] - g) * t),
                        round(b + (cor[2] - b) * t))
    return im


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


# A promessa, fixa nas dez artes. Sem ela so a BF04 dizia o que a pessoa vai
# aprender: as outras nove ("vagas limitadas", "3 perguntas", "a maquina fica
# com voce") assumem que quem le ja sabe o que e a mentoria. Num anuncio frio
# ninguem sabe — a etiqueta diz TURMA DE SETEMBRO e o leitor pergunta "de que".
# "aprenda", nao "receba": e mentoria, nao agencia -- e essa palavra que separa
# as duas coisas. "online" saiu para a linha caber em corpo maior; no contexto
# de um anuncio no Instagram ninguem le "anuncio" como outdoor.
# A frase central da mentoria, nas duas linhas em que ela cabe legivel. A
# segunda nao e enfeite: "sem agencia e sem investir alto" e o que separa esta
# oferta de uma agencia, e sem ela a promessa descreve o que uma agencia
# tambem entrega.
PROMESSA = ["aprenda a criar anúncios que trazem cliente todo dia no seu WhatsApp",
            "sem agência e sem investir alto"]


def etiqueta(d, txt, sub=PROMESSA):
    """Tarja de turma no alto, com a promessa logo abaixo.

    E a tarja que diz 'isto e uma oferta, nao um post'; e a linha de baixo que
    diz de que oferta se trata. Uma sem a outra nao fecha.

    A promessa vai em corpo FIXO (42/46) e quebra em quantas linhas precisar.
    Ate 08/09/2026 ela era encolhida para caber numa linha so e saia a 26 px --
    a frase central da mentoria era a menor letra da peca. Ver tipografia.py.
    """
    f = fonte(SANS, 34, 700)
    l, t, r, b = d.textbbox((0, 0), txt, font=f)
    lw, lh = (r - l) + 64, (b - t) + 34
    x0, y0 = (W - lw) / 2, 52
    d.rounded_rectangle((x0, y0, x0 + lw, y0 + lh), radius=lh / 2, fill=LARANJA)
    d.text((x0 + 28 - l, y0 + 15 - t), txt, font=f, fill=GRAFITE)
    if not sub:
        return lw * lh, y0 + lh
    # a segunda sentenca vem em branco cheio e mais forte: e a parte que
    # separa esta oferta de uma agencia, e a que o leitor precisa levar embora
    sent = [(sub[0], fonte(SANS, PISO_PROMESSA, 600), APOIO),
            (sub[1], fonte(SANS, PISO_PROMESSA + 4, 800), BRANCO)]
    fim, area = paragrafo(d, sent, y0 + lh + 24, 980, W)
    return lw * lh + area, fim


def botao(d, principal, apoio):
    """Barra de CTA. Solida, cor cheia, texto escuro: tem que parecer clicavel."""
    f = fonte(SANS, PISO_CTA + 4, 800)
    l, t, r, b = d.textbbox((0, 0), principal, font=f)
    bw, bh = W - 96, 132
    x0, y0 = 48, 1150
    d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius=16, fill=LARANJA)
    d.text(((W - (r - l)) / 2 - l, y0 + (bh - (b - t)) / 2 - t), principal, font=f, fill=GRAFITE)
    return bw * bh
    # A linha de 24px embaixo do botao SAIU. Era o menor texto da peca e o mais
    # redundante: "turma de setembro" ja esta na etiqueta e "3 perguntas" ja
    # esta dentro do botao. Texto pequeno demais para ler no feed nao informa,
    # so rouba espaco de quem precisa ser lido.


def desenhar(p, saida, devolver=False):
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
        im = scrim(degrade(chapeu(cobrir(p["foto"], p.get("alto", 0.32)), cor), cor), cor)
        d = ImageDraw.Draw(im)

    tinta, fim_topo = etiqueta(d, p.get("etiqueta", "MENTORIA O PRÓXIMO CLIENTE"))

    y = p.get("y", 830)
    caixas = []
    if p.get("riscado"):
        f = cabe(d, p["riscado"], SANS, 800, p.get("corpo_riscado", 96))
        y0, y1, larg, x = centrar(d, p["riscado"], f, y, (196, 196, 206))
        d.line((x - 6, (y0 + y1) / 2, x + larg + 6, (y0 + y1) / 2), fill=(214, 60, 50), width=9)
        caixas.append((y0, y1, larg)); y = y1 + 22

    f = cabe(d, p["linha_sans"], SANS, 800, p.get("corpo_sans", 70))
    y0, y1, lg, _ = centrar(d, p["linha_sans"], f, y, BRANCO)
    caixas.append((y0, y1, lg)); y = y1 + p.get("gap", 14)

    f = cabe(d, p["linha_cursiva"], ITAL, 700, p.get("corpo_cursiva", 132))
    y0, y1, lg, _ = centrar(d, p["linha_cursiva"], f, y, LARANJA)
    caixas.append((y0, y1, lg)); y = y1 + 34

    if p.get("linha_apoio"):
        # 40 px fixos, quebrando em duas linhas se precisar. Encolhendo, o
        # apoio da BF02 saia a 30 px -- menor que o piso de leitura no feed.
        fim, area_ap = paragrafo(d, [(p["linha_apoio"], fonte(SANS, 40, 650), APOIO)],
                                 y, 950, W, entre=6)
        caixas.append((y, fim, 0))
        tinta += area_ap

    # "RESPONDER AS 3 PERGUNTAS", nao "PREENCHER APLICACAO". Num formulario
    # instantaneo o inimigo e a fricção PERCEBIDA, nao a falta de vontade:
    # "aplicacao" soa trabalhoso, "3 perguntas" diz o tamanho real do pedido.
    # O botao de verdade fica ABAIXO do criativo, escolhido na campanha
    # (recomendado: "Candidatar-se") -- esta barra so o espelha.
    tinta += botao(d, p.get("cta", "RESPONDER AS 3 PERGUNTAS"),
          p.get("cta_apoio", "leva menos de um minuto · turma de setembro · vagas limitadas"))

    # AREA DE TEXTO: o pedido do Pablo em 08/09/2026 e "ate 30%". Abaixo de 18%
    # a peca fica com letra pequena demais para o feed -- foi o defeito da
    # primeira versao, que empilhava oito blocos e encolhia todos para caber.
    # A conta soma a caixa de cada bloco, a etiqueta e a barra de CTA.
    area = (sum((b - a) * lg for a, b, lg in caixas) + tinta) / (W * H)
    folga = min(1150 - caixas[-1][1], caixas[0][0] - fim_topo, 999)
    gaps = [caixas[i + 1][0] - caixas[i][1] for i in range(len(caixas) - 1)]
    ok = folga >= 0 and all(g >= 0 for g in gaps) and 0.18 <= area <= 0.30
    if devolver:
        return ok, area, folga
    im.save(saida, quality=94)
    print("%-34s texto %4.1f%%  folga %4d  gaps %s  %s" %
          (os.path.basename(saida), area * 100, folga, [round(g) for g in gaps],
           "OK" if ok else "REFAZER"))
    return ok


def ajustar(p):
    """Acha o maior corpo de cursiva que ainda respeita o teto de 30% e o pe.

    Antes eu escolhia esses numeros a mao no bofu.json, e eles ficavam errados
    a cada mudanca de texto -- foi assim que a promessa maior estourou dez
    pecas de uma vez. Quem cede espaco e a cursiva: ela e enfeite, a promessa
    e a mensagem. O sans acompanha, para a hierarquia nao inverter.
    """
    base_c = p.get("corpo_cursiva", 132)
    base_s = p.get("corpo_sans", 70)
    for passo in range(0, 22):
        q = dict(p, corpo_cursiva=base_c - passo * 6,
                 corpo_sans=max(52, base_s - passo * 2))
        ok, area, folga = desenhar(q, None, devolver=True)
        if ok:
            return q, passo
    return p, None


if __name__ == "__main__":
    os.makedirs("bofu", exist_ok=True)
    todos = True
    for p in json.load(open(sys.argv[1])):
        q, passo = ajustar(p)
        if passo is None:
            print("%-34s NAO FECHA -- encurte o texto" % p["slug"])
            todos = False
            continue
        todos &= desenhar(q, "bofu/%s.jpg" % q["slug"])
    print("todas OK" if todos else "ALGUMA PRECISA DE AJUSTE")
