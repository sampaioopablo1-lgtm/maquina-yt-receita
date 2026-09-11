"""As 20 pecas de anuncio: foto do Pexels + tipografia, prontas para subir.

Por que compor aqui em vez de no Canva: sao 20 pecas que mudam de copy toda
semana. No Canva, trocar uma palavra em 20 artes e uma tarde; aqui e uma linha
em PECAS e um `python3 fabrica/criativos_anuncio.py`.

O padrao visual saiu de varrer a Biblioteca de Anuncios (11/09/2026). Quem
converte na categoria tem uma coisa em comum: a chamada **nomeia o negocio do
leitor** ("Receba Leads de 3 a 29 Vidas", "Feito para provedor com 10 anos").
Quem nao converte usa o campo padrao do Facebook — "Converse conosco" — e ate
agencia de trafego faz isso.

Fundo escuro com acento ambar de proposito: a categoria inteira e verde
WhatsApp. No feed, verde sobre verde some.

TOPO (TF) nao oferece nada — so nomeia a dor, para publico frio.
FUNDO (BF) oferece, porque ali o publico ja sabe quem somos.

Chave do Pexels: broll.chave() — env PEXELS_API_KEY ou config.pexels_api_key no
Supabase. A sessao do agente nao alcanca o Pexels (egresso nega CONNECT), entao
isto roda no runner do GitHub Actions ou no sandbox do Composio.
"""
import json
import os
import ssl
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw, ImageFont

from broll import chave

API = "https://api.pexels.com/v1/search"
DESTINO = "entregas/campanha/imagens"

L, A = 1080, 1350          # 4:5, o formato que mais entrega no feed
MARGEM = 72
INK = (11, 11, 12)
BRANCO = (255, 255, 255)
ACENTO = (245, 179, 1)     # ambar: a categoria e toda verde WhatsApp

# id, funil, busca no Pexels, sobrancelha, chamada, apoio, botao
PECAS = [
    # ---------------- TOPO: abre pela dor, mas ja diz o que fazemos ---------
    # Publico frio nao leva oferta na cara, mas precisa entender o servico em
    # dois segundos, senao a peca vira frase de efeito sem dono.
    ("TF01_indicacao", "topo", "brazilian small business owner thinking",
     "AGÊNCIA DE ANÚNCIOS", "Sua agenda depende de indicação?",
     "Fazemos anúncios online que trazem cliente novo todo dia.", "Veja como funciona"),
    ("TF02_falta_cliente_novo", "topo", "empty restaurant interior tables",
     "AGÊNCIA DE ANÚNCIOS", "Faz quanto tempo que não entra um rosto novo?",
     "Colocamos seu negócio na frente de quem está procurando hoje.", "Veja como funciona"),
    ("TF03_whatsapp_parado", "topo", "person looking at phone bored office",
     "AGÊNCIA DE ANÚNCIOS", "Seu WhatsApp parado o dia inteiro",
     "Nossos anúncios trazem cliente todo dia. Ele volta a tocar.", "Veja como funciona"),
    ("TF04_perguntou_o_preco", "topo", "hand typing message smartphone",
     "AGÊNCIA DE ANÚNCIOS", "Perguntou o preço e sumiu",
     "Anúncio bem feito traz quem já chega decidido a comprar.", "Veja como funciona"),
    ("TF05_seguidor_nao_e_cliente", "topo", "social media phone scrolling",
     "AGÊNCIA DE ANÚNCIOS", "Seguidor não paga boleto",
     "Fazemos anúncios que trazem cliente, não curtida.", "Veja como funciona"),
    ("TF06_tirar_do_proprio_bolso", "topo", "stressed man paperwork desk night",
     "AGÊNCIA DE ANÚNCIOS", "Tirando do próprio bolso de novo?",
     "Cliente entrando todo dia começa com anúncio no ar.", "Veja como funciona"),
    ("TF07_funcionario_ganha_mais", "topo", "business owner late night work",
     "AGÊNCIA DE ANÚNCIOS", "Seu funcionário ganha mais que você",
     "Fazemos os anúncios que enchem a sua agenda.", "Veja como funciona"),
    ("TF08_sem_ferias", "topo", "empty beach chair vacation",
     "AGÊNCIA DE ANÚNCIOS", "Quantos anos sem tirar férias?",
     "Negócio com cliente entrando todo dia não depende só de você.", "Veja como funciona"),
    ("TF09_medo_do_dia_20", "topo", "calendar desk anxiety",
     "AGÊNCIA DE ANÚNCIOS", "O dia em que a conta aperta",
     "Nossos anúncios trazem cliente todo dia, não só no aperto.", "Veja como funciona"),
    ("TF10_concorrente_menor", "topo", "smartphone screen social media feed",
     "AGÊNCIA DE ANÚNCIOS", "Menor que você, e aparece mais",
     "Ele anuncia. A gente faz o seu, e melhor.", "Veja como funciona"),

    # ---------------- FUNDO: servico e beneficio na chamada -----------------
    ("BF01_fazemos_seus_anuncios", "fundo", "happy business owner smartphone notification",
     "O QUE FAZEMOS", "Fazemos seus anúncios. Você atende os clientes.",
     "Todo dia gente nova chamando no seu WhatsApp.", "Agende 20 minutos"),
    ("BF02_clientes_todo_dia", "fundo", "smartphone many messages notification",
     "O BENEFÍCIO", "Clientes novos no seu WhatsApp, todo dia",
     "É o que anúncio online bem feito entrega. A gente cuida de tudo.", "Agende 20 minutos"),
    ("BF03_nos_cuidamos", "fundo", "marketing team working laptops office",
     "COMO FUNCIONA", "Você não precisa entender de anúncio",
     "Nosso time cria, publica e acompanha. Você só atende quem chega.", "Agende 20 minutos"),
    ("BF04_anuncio_no_ar", "fundo", "woman typing laptop modern office",
     "VELOCIDADE", "Seu anúncio no ar esta semana",
     "Sem projeto de três meses. Começa, traz cliente, ajusta.", "Agende 20 minutos"),
    ("BF05_quanto_custa_cada_cliente", "fundo", "financial charts screen analytics",
     "TRANSPARÊNCIA", "Você vai saber quanto custa cada cliente",
     "Relatório com número. Sem adjetivo, sem enrolação.", "Agende 20 minutos"),
    ("BF06_para_quem_e", "fundo", "confident business owner boutique shop",
     "PARA QUEM É", "Para quem já vende e quer vender mais",
     "Fazemos os anúncios. Você cuida de atender a demanda.", "Agende 20 minutos"),
    ("BF07_nao_e_renda_extra", "fundo", "professional office meeting serious",
     "NÃO É PARA TODO MUNDO", "Não é renda extra. É empresa.",
     "Anúncios para quem já tem cliente, equipe e conta para pagar.", "Agende 20 minutos"),
    ("BF08_sai_sabendo", "fundo", "two people conversation laptop consulting",
     "A CONVERSA", "20 minutos e você sai sabendo o que fazer",
     "A gente olha seu negócio e diz qual anúncio traz cliente.", "Agende 20 minutos"),
    ("BF09_especialistas", "fundo", "professional team discussion office",
     "QUEM ATENDE", "Fale com quem faz anúncio todo dia",
     "Não é robô nem estagiário. É o time que vai tocar sua conta.", "Agende 20 minutos"),
    ("BF10_comecar_esta_semana", "fundo", "calendar schedule planning desk",
     "AGENDA", "Ainda dá para começar esta semana",
     "Escolhe o horário. Em 20 minutos você entende como funciona.", "Agende 20 minutos"),
]


def caminho_fonte(negrito=True):
    """O primeiro arquivo de fonte que existe nesta maquina, ou None.

    Montserrat primeiro (o peso que a categoria usa, baixado pelo workflow);
    DejaVu e Liberation depois, porque uma das duas costuma vir instalada.
    Devolver None em vez de cair no bitmap padrao e proposital: `ajustar` mede
    largura de texto para escolher o corpo da fonte, e a metrica do bitmap nao
    corresponde a nenhuma arte real — a peca sairia com a chamada no tamanho
    errado sem nada acusar.
    """
    sufixo_m = "Bold" if negrito else "Regular"
    sufixo_d = "-Bold" if negrito else ""
    for caminho in (
        f"/tmp/fontes/Montserrat-{sufixo_m}.ttf",
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans{sufixo_d}.ttf",
        f"/usr/share/fonts/truetype/liberation/LiberationSans{sufixo_d or '-Regular'}.ttf",
        f"/usr/share/fonts/truetype/freefont/FreeSans{sufixo_d}.ttf",
    ):
        if os.path.exists(caminho):
            return caminho
    return None


def fonte(tamanho, negrito=True):
    caminho = caminho_fonte(negrito)
    if caminho is None:
        raise RuntimeError(
            "nenhuma fonte TrueType encontrada — instale fonts-dejavu-core ou "
            "baixe o Montserrat em /tmp/fontes")
    return ImageFont.truetype(caminho, tamanho)


def quebrar(texto, fnt, largura, desenho):
    linhas, atual = [], ""
    for palavra in texto.split():
        teste = f"{atual} {palavra}".strip()
        if desenho.textlength(teste, font=fnt) <= largura:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def ajustar(texto, largura, desenho, maior, menor, max_linhas):
    """A maior fonte em que o texto cabe em max_linhas.

    Chamada longa com fonte fixa ou vaza da arte ou vira quatro linhas finas —
    nos dois casos a peca morre no feed, onde o julgamento dura menos de 2s.
    """
    for tam in range(maior, menor - 1, -4):
        fnt = fonte(tam)
        linhas = quebrar(texto, fnt, largura, desenho)
        if len(linhas) <= max_linhas:
            return fnt, linhas
    fnt = fonte(menor)
    return fnt, quebrar(texto, fnt, largura, desenho)[:max_linhas]


def cobrir(foto):
    """Recorta para 1080x1350 sem distorcer, mantendo o centro."""
    p = foto.convert("RGB")
    escala = max(L / p.width, A / p.height)
    nova = p.resize((max(L, int(p.width * escala + 0.5)),
                     max(A, int(p.height * escala + 0.5))), Image.LANCZOS)
    esq = (nova.width - L) // 2
    topo = (nova.height - A) // 2
    return nova.crop((esq, topo, esq + L, topo + A))


def escurecer(img):
    """Gradiente preto de baixo para cima, para o texto ter contraste.

    Sem isto o texto branco cai sobre ceu claro em metade das fotos e some.
    O gradiente comeca em 42% da altura: acima disso a foto fica limpa.
    """
    veu = Image.new("L", (1, A), 0)
    for y in range(A):
        t = (y - A * 0.42) / (A * 0.58)
        veu.putpixel((0, y), 0 if t < 0 else int(235 * min(1.0, t) ** 1.25))
    sombra = Image.new("RGB", (L, A), INK)
    return Image.composite(sombra, img, veu.resize((L, A)))


def compor(foto, peca):
    """A peca pronta: foto recortada, escurecida e com a tipografia por cima."""
    _id, _funil, _q, sobrancelha, chamada, apoio, botao = peca
    img = escurecer(cobrir(foto))
    d = ImageDraw.Draw(img)
    util = L - 2 * MARGEM

    f_cham, linhas = ajustar(chamada, util, d, 92, 52, 3)
    f_sobr = fonte(28)
    f_apoio = fonte(32, negrito=False)
    f_bot = fonte(30)

    linhas_apoio = quebrar(apoio, f_apoio, util, d)
    alt_cham = sum(f_cham.size + 14 for _ in linhas)
    alt_apoio = sum(f_apoio.size + 10 for _ in linhas_apoio)
    alt_botao = f_bot.size + 38

    y = A - MARGEM - alt_botao - 34 - alt_apoio - 22 - alt_cham

    # Sobrancelha: quem e o leitor. A pesquisa diz que nomear o negocio do
    # leitor e o que separa quem converte de quem escreve "Converse conosco".
    d.text((MARGEM, y - 46), " ".join(sobrancelha), font=f_sobr, fill=ACENTO)

    for ln in linhas:
        d.text((MARGEM, y), ln, font=f_cham, fill=BRANCO)
        y += f_cham.size + 14
    y += 22

    for ln in linhas_apoio:
        d.text((MARGEM, y), ln, font=f_apoio, fill=(225, 225, 228))
        y += f_apoio.size + 10
    y += 34

    larg_bot = int(d.textlength(botao, font=f_bot)) + 56
    d.rounded_rectangle([MARGEM, y, MARGEM + larg_bot, y + alt_botao],
                        radius=alt_botao // 2, fill=ACENTO)
    d.text((MARGEM + 28, y + 19 - f_bot.size // 2), botao, font=f_bot, fill=INK)
    return img


def buscar(q, api_key, tentativas=3):
    url = f"{API}?{urllib.parse.urlencode({'query': q, 'per_page': 15, 'orientation': 'portrait'})}"
    # User-Agent de navegador: o Pexels devolve 403 para o urllib padrao
    # (medido no broll.py em 18/08). Tentativa tripla porque a primeira
    # estoura o timeout no runner.
    req = urllib.request.Request(
        url, headers={"Authorization": api_key,
                      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    ultimo = None
    for n in range(tentativas):
        try:
            with urllib.request.urlopen(req, timeout=30 * (n + 1),
                                        context=ssl.create_default_context()) as r:
                return json.load(r)
        except Exception as e:
            ultimo = e
    raise ultimo


def escolher(dados):
    """A maior foto retrato utilizavel, e o credito.

    Minimo 1080x1350 porque abaixo disso o recorte amplia e a peca sai borrada
    num feed que e quase todo retina.
    """
    for f in dados.get("photos", []):
        if f.get("width", 0) < L or f.get("height", 0) < A:
            continue
        link = f.get("src", {}).get("large2x") or f.get("src", {}).get("original")
        if link:
            return link, {"pexels_id": f["id"], "autor": f.get("photographer", ""),
                          "url": f.get("url", "")}
    return None


def baixar(link):
    req = urllib.request.Request(
        link, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    with urllib.request.urlopen(req, timeout=60,
                                context=ssl.create_default_context()) as r:
        dados = r.read()
    if len(dados) < 10000:
        raise ValueError(f"resposta de {len(dados)} bytes")
    import io
    return Image.open(io.BytesIO(dados))


def main():
    api_key = chave()
    if not api_key:
        from broll import ORIGEM_DA_CHAVE
        raise SystemExit(f"sem chave do Pexels — {ORIGEM_DA_CHAVE}")

    creditos, faltando = {}, []
    for peca in PECAS:
        pid, funil, q = peca[0], peca[1], peca[2]
        pasta = os.path.join(DESTINO, funil)
        os.makedirs(pasta, exist_ok=True)
        try:
            escolha = escolher(buscar(q, api_key))
            if not escolha:
                print(f"{pid}: '{q}' sem foto no criterio")
                faltando.append(pid)
                continue
            link, credito = escolha
            compor(baixar(link), peca).save(
                os.path.join(pasta, f"{pid}.jpg"), quality=92, optimize=True)
        except Exception as e:
            print(f"{pid}: {type(e).__name__}: {e}")
            faltando.append(pid)
            continue
        creditos[pid] = credito
        print(f"{pid}: ok — {credito['autor']}")

    with open(os.path.join(DESTINO, "creditos.json"), "w", encoding="utf-8") as fp:
        json.dump(creditos, fp, ensure_ascii=False, indent=2)
    print(f"\n{len(creditos)} de {len(PECAS)} geradas")
    if faltando:
        print(f"faltando: {', '.join(faltando)}")


if __name__ == "__main__":
    main()
