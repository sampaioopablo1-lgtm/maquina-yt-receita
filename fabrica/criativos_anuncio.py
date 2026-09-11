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

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

import caminhos
from broll import chave

API = "https://api.pexels.com/v1/search"
DESTINO = "entregas/campanha/imagens"

L, A = 1080, 1350          # 4:5, o formato que mais entrega no feed
MARGEM = 72
INK = (11, 11, 12)
BRANCO = (255, 255, 255)
ACENTO = (245, 179, 1)     # ambar: a categoria e toda verde WhatsApp
CINZA = (214, 214, 218)
MARCA = "O PRÓXIMO CLIENTE"

# id, funil, busca no Pexels, sobrancelha, chamada, apoio, botao
PECAS = [
    # ---------------- TOPO: uma dor so, dita de dez jeitos ------------------
    # Antes o topo passeava por ferias, dia 20, funcionario e seguidor. Dores
    # diferentes diluem: quem ve tres pecas da campanha nao monta uma promessa
    # na cabeca. Agora todas batem no mesmo lugar — falta de cliente novo — e
    # todas fecham com a mesma saida: cliente todo dia pelo WhatsApp.
    ("TF01_entrou_hoje", "topo", "brazilian small business owner thinking",
     "AGÊNCIA DE ANÚNCIOS", "Entrou algum cliente novo hoje?",
     "Fazemos anúncios que trazem cliente todo dia no seu WhatsApp.", "Veja como funciona"),
    ("TF02_whatsapp_nao_toca", "topo", "person looking at phone bored office",
     "AGÊNCIA DE ANÚNCIOS", "Seu WhatsApp não toca há quanto tempo?",
     "Nossos anúncios colocam cliente novo falando com você todo dia.", "Veja como funciona"),
    ("TF03_mes_nao_fecha", "topo", "stressed man paperwork desk night",
     "AGÊNCIA DE ANÚNCIOS", "Sem cliente novo, o mês não fecha",
     "Fazemos anúncios online que trazem gente nova todo dia.", "Veja como funciona"),
    ("TF04_indicacao", "topo", "two people talking cafe casual",
     "AGÊNCIA DE ANÚNCIOS", "Só entra cliente quando indicam?",
     "Com anúncio no ar, cliente novo chega todo dia no seu WhatsApp.", "Veja como funciona"),
    ("TF05_movimento_caiu", "topo", "empty restaurant interior tables",
     "AGÊNCIA DE ANÚNCIOS", "O movimento caiu e ninguém te avisou",
     "Fazemos anúncios que trazem cliente novo todo dia.", "Veja como funciona"),
    ("TF06_semana_sem_orcamento", "topo", "empty office desk quiet",
     "AGÊNCIA DE ANÚNCIOS", "Uma semana inteira sem um orçamento novo",
     "Nossos anúncios enchem seu WhatsApp de quem quer comprar.", "Veja como funciona"),
    ("TF07_seguidor_nao_compra", "topo", "social media phone scrolling",
     "AGÊNCIA DE ANÚNCIOS", "Seguidor não vira cliente sozinho",
     "Fazemos anúncios que trazem cliente todo dia no seu WhatsApp.", "Veja como funciona"),
    ("TF08_concorrente_recebe", "topo", "smartphone screen social media feed",
     "AGÊNCIA DE ANÚNCIOS", "O cliente que era seu está falando com ele",
     "Ele anuncia. A gente coloca o seu anúncio na frente também.", "Veja como funciona"),
    ("TF09_quantos_essa_semana", "topo", "calendar desk anxiety",
     "AGÊNCIA DE ANÚNCIOS", "Quantos clientes novos você teve essa semana?",
     "Com anúncio no ar, essa conta muda todo dia.", "Veja como funciona"),
    ("TF10_esperar_nao_e_plano", "topo", "bored shop owner leaning counter",
     "AGÊNCIA DE ANÚNCIOS", "Esperar cliente aparecer não é plano",
     "Fazemos anúncios que trazem cliente novo todo dia.", "Veja como funciona"),

    # ---------------- FUNDO: a mesma promessa, agora com a oferta -----------
    ("BF01_clientes_todo_dia", "fundo", "smartphone many messages notification",
     "O QUE VOCÊ GANHA", "Clientes novos no seu WhatsApp, todo dia",
     "É isso que anúncio online bem feito entrega. A gente cuida de tudo.", "Agende 20 minutos"),
    ("BF02_fazemos_voce_atende", "fundo", "happy business owner smartphone notification",
     "O QUE FAZEMOS", "Fazemos seus anúncios. Você atende os clientes.",
     "Todo dia gente nova chamando para comprar.", "Agende 20 minutos"),
    ("BF03_tocando_de_manha", "fundo", "hands holding smartphone morning",
     "O RESULTADO", "Seu WhatsApp tocando desde cedo",
     "Anúncio no ar para quem procura hoje o que você vende.", "Agende 20 minutos"),
    ("BF04_de_parado_a_cheio", "fundo", "busy shop customers counter",
     "A MUDANÇA", "De WhatsApp parado a agenda cheia",
     "Fazemos os anúncios. Você só atende quem chega.", "Agende 20 minutos"),
    ("BF05_quanto_custa_cada_cliente", "fundo", "financial charts screen analytics",
     "TRANSPARÊNCIA", "Você vai saber quanto custa cada cliente",
     "Relatório com número. Sem adjetivo, sem enrolação.", "Agende 20 minutos"),
    ("BF06_para_quem_e", "fundo", "confident business owner boutique shop",
     "PARA QUEM É", "Para quem já vende e quer vender mais",
     "Trazemos cliente novo todo dia. Você cuida de atender.", "Agende 20 minutos"),
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
     "COMEÇO", "Comece esta semana a receber clientes",
     "Escolhe o horário. Em 20 minutos você entende como funciona.", "Agende 20 minutos"),
    # ---------------- RIO: o mesmo recado, com o bairro no nome -------------
    # A varredura da Biblioteca mostrou que quem converte nomeia o leitor
    # ("Feito para provedor com 10 anos", "Receba Leads de 3 a 29 Vidas"). No
    # anuncio local, nomear o bairro e a forma mais barata de fazer isso — e
    # a sobrancelha ja era o lugar do leitor, entao ela vira o bairro.
    #
    # O gancho e sempre o mesmo: o anuncio aparece so para quem esta perto.
    # Isso e verdade (a Meta segmenta por raio) e e o que o dono de bairro
    # entende na hora, sem precisar saber o que e trafego pago.
    ("RJ01_copacabana", "topo", "copacabana beach rio de janeiro",
     "COPACABANA", "Quem mora aqui ainda não sabe que você existe",
     "Fazemos anúncios que aparecem só para quem está perto do seu negócio.", "Veja como funciona"),
    ("RJ02_ipanema", "topo", "ipanema beach rio de janeiro",
     "IPANEMA", "Tem cliente a três quadras procurando o que você vende",
     "Nossos anúncios colocam seu WhatsApp na frente de quem está no seu bairro.", "Veja como funciona"),
    ("RJ03_tijuca", "topo", "rio de janeiro street neighborhood",
     "TIJUCA", "Anuncie para quem passa na sua porta",
     "Anúncio no ar só para o seu bairro. Cliente novo todo dia no WhatsApp.", "Veja como funciona"),
    ("RJ04_niteroi", "topo", "niteroi rio de janeiro",
     "NITERÓI", "Seu cliente está aqui, não do outro lado da ponte",
     "Fazemos anúncios que só aparecem para quem mora perto de você.", "Veja como funciona"),
    ("RJ05_botafogo", "topo", "sugarloaf botafogo rio",
     "BOTAFOGO", "O bairro tem cliente. Ele só não te achou ainda.",
     "Nossos anúncios trazem cliente novo todo dia pelo WhatsApp.", "Veja como funciona"),
    ("RJ06_zona_norte", "topo", "maracana rio de janeiro",
     "ZONA NORTE", "Seu concorrente do bairro está anunciando. Você não.",
     "A gente coloca o seu anúncio na frente de quem mora aqui.", "Veja como funciona"),
]


def dir_fontes():
    """Onde o Montserrat e baixado, sob a raiz de trabalho.

    Nao escrever o caminho a mao e regra da casa, cercada por
    test_caminhos.py: literal de workdir copiado pela metade ja fez o render
    terminar num lugar e a publicacao procurar em outro.
    """
    return os.path.join(caminhos.raiz(), "fontes")


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
        os.path.join(dir_fontes(), f"Montserrat-{sufixo_m}.ttf"),
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
            f"baixe o Montserrat em {dir_fontes()}")
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


def tratar(img):
    """Mesmo tratamento de cor em todas as pecas.

    Sem isto, vinte fotos de banco continuam parecendo vinte fotos de banco:
    cada uma com sua temperatura e saturacao. Dessaturar, ganhar contraste e
    puxar a sombra para o mesmo azul-tinta faz o conjunto ler como uma
    campanha so — e e o que separa anuncio de agencia de anuncio de amador.
    """
    img = ImageEnhance.Color(img).enhance(0.72)
    img = ImageEnhance.Contrast(img).enhance(1.10)
    return Image.blend(img, Image.new("RGB", img.size, (14, 16, 26)), 0.10)


def vinheta(img):
    """Escurece os cantos de leve.

    A foto passa a ter centro, e o olho para de escorregar para fora da arte.
    Raio generoso e 34% de forca de proposito: vinheta que se percebe vira
    efeito de filtro de rede social, que e o oposto de profissional.
    """
    m = Image.new("L", (L // 6, A // 6), 0)
    ImageDraw.Draw(m).ellipse([-L // 24, -A // 24, L // 6 + L // 24, A // 6 + A // 24],
                              fill=255)
    m = m.filter(ImageFilter.GaussianBlur(L // 40)).resize((L, A), Image.LANCZOS)
    return Image.composite(img, Image.blend(img, Image.new("RGB", img.size, INK), 0.34), m)


def escurecer(img):
    """Gradiente do rodape para cima, para o texto ter contraste.

    Curva em potencia 1.6: a transicao fica mais longa e some antes de virar
    faixa preta reta, que e o que denuncia arte feita as pressas.
    """
    veu = Image.new("L", (1, A), 0)
    for y in range(A):
        t = (y - A * 0.30) / (A * 0.70)
        veu.putpixel((0, y), 0 if t < 0 else int(242 * min(1.0, t) ** 1.6))
    sombra = Image.new("RGB", (L, A), INK)
    return Image.composite(sombra, img, veu.resize((L, A)))


def compor(foto, peca):
    """A peca pronta: foto tratada, escurecida e com a tipografia por cima.

    A regua ambar a esquerda do bloco de texto existe para ancorar a leitura:
    sem ela o texto flutua sobre a foto e a peca parece legenda, nao anuncio.
    """
    _id, _funil, _q, sobrancelha, chamada, apoio, botao = peca
    img = escurecer(vinheta(tratar(cobrir(foto))))
    d = ImageDraw.Draw(img)
    REGUA = 6
    RECUO = MARGEM + REGUA + 26
    util = L - RECUO - MARGEM

    f_cham, linhas = ajustar(chamada, util, d, 88, 50, 3)
    f_marca, f_sobr = fonte(24), fonte(26)
    f_apoio, f_bot = fonte(31, negrito=False), fonte(29)

    linhas_apoio = quebrar(apoio, f_apoio, util, d)
    # Entrelinha de 1.06: chamada de anuncio e bloco, nao paragrafo.
    passo_cham = int(f_cham.size * 1.06)
    alt_cham = passo_cham * len(linhas)
    alt_apoio = sum(int(f_apoio.size * 1.32) for _ in linhas_apoio)
    alt_botao = f_bot.size + 40

    topo_sobr = A - MARGEM - alt_botao - 40 - alt_apoio - 26 - alt_cham - 46
    y = topo_sobr

    # A regua cobre da sobrancelha ao fim do apoio, nao o botao: o botao e
    # outro objeto, e amarelo sobre amarelo empastela.
    d.rectangle([MARGEM, y, MARGEM + REGUA,
                 y + 46 + alt_cham + 26 + alt_apoio], fill=ACENTO)

    # Moldura fina a 22% de branco: da borda a peca no feed, onde o fundo do
    # aplicativo e claro e a arte sem contorno "vaza" para a interface. Em
    # RGB nao ha alfa no traco, entao ela e desenhada numa camada e composta.
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(camada).rectangle(
        [28, 28, L - 29, A - 29], outline=(255, 255, 255, 56), width=2)
    img = Image.alpha_composite(img.convert("RGBA"), camada).convert("RGB")
    d = ImageDraw.Draw(img)

    d.text((MARGEM, MARGEM), " ".join(MARCA), font=f_marca, fill=(255, 255, 255, 180))
    d.text((RECUO, y), " ".join(sobrancelha), font=f_sobr, fill=ACENTO)
    y += 46

    for ln in linhas:
        # Sombra de 3px antes do texto: sobre foto clara ou ocupada a chamada
        # branca perde a borda e some. A sombra segura sem escurecer a arte.
        d.text((RECUO + 3, y + 3), ln, font=f_cham, fill=(0, 0, 0))
        d.text((RECUO, y), ln, font=f_cham, fill=BRANCO)
        y += passo_cham
    y += 26

    for ln in linhas_apoio:
        d.text((RECUO, y), ln, font=f_apoio, fill=CINZA)
        y += int(f_apoio.size * 1.32)
    y += 40

    rotulo = f"{botao}  →"
    larg_bot = int(d.textlength(rotulo, font=f_bot)) + 60
    d.rounded_rectangle([RECUO, y, RECUO + larg_bot, y + alt_botao],
                        radius=alt_botao // 2, fill=ACENTO)
    d.text((RECUO + 30, y + alt_botao // 2 - int(f_bot.size * 0.68)),
           rotulo, font=f_bot, fill=INK)
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
