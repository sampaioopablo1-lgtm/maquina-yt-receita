"""game-money-lab-009 — o desconto e medido de um preco que talvez nunca foi cobrado.

ALAVANCA ATACADA: A (conversao short -> inscrito), MAS com uma ressalva que o
dado deste canal impoe e que eu nao vou esconder.

O NUMERO DE PARTIDA, e ele CONTRARIA a alavanca A dentro deste canal:

    003  GTA 6 custa oitenta dolares, o congelamento de vinte anos ....  91 views
    002  trezentos milhoes por jogo, a conta que quebrou o AAA ........  52
    004  demissoes, previsao revisada em setenta e oito por cento .....  21
    006  moeda do jogo: duas divisoes que mostram o que voce pagou ....  18
    005  um milhao e duzentas mil assinaturas, e a UE escolheu codigo ..   8
    007  o botao de reembolso nao e o direito: catorze dias, tres ......   7
    008  promocao ou preco cheio? divida pelas horas que voce jogou ...   2

Os dois de cima entregam FATO sobre a industria. Os dois de METODO, que a
alavanca A manda preferir, deram dezoito e dois. Na frota a regra e o contrario
(aprendizado 482) e no seja-mais-magra ela se reproduziu limpa. Aqui, nao.

FRAQUEZA DA LEITURA, DECLARADA: a ordem de views e quase a ordem de ANTIGUIDADE.
002 e 003 sao de treze e dezoito de agosto, os mais velhos; 008 e de primeiro de
setembro, o mais novo. O alcance do canal caiu ao longo da serie
independentemente da forma, e com sete pontos eu NAO consigo separar forma de
data. Entao eu nao declaro a alavanca A invalidada neste canal — declaro que o
dado dele nao a sustenta e que o confundidor tem nome.

O QUE DEU CERTO: numero concreto, grande e CONFERIVEL, pregado numa coisa que o
espectador conhece pelo nome — o preco de um jogo especifico.
O QUE NAO DEU: metodo sem ancora. O 008 manda "divida pelas horas que voce
jogou" e nao pregou a conta em nada que o espectador reconheca de imediato.
O QUE VOU MUDAR: as duas coisas ao mesmo tempo, em vez de escolher uma. A conta
e do espectador (alavanca A), mas a ancora e um numero que ele ja viu na
propria tela de loja e pode conferir em dez segundos — que e o que mediu melhor
aqui. Se o short passar de cinquenta views, foi a sintese; se ficar abaixo de
vinte, a ancora nao bastou e o confundidor da data era o fator real.

EIXO, e por que ele e novo. Os sete anteriores falam de ORCAMENTO de estudio
(002), de PRECO DE TABELA (003), de EMPREGO (004), de REGULACAO (005), de MOEDA
INTERNA (006), de REEMBOLSO (007) e de CUSTO POR HORA (008). Nenhum fala do
DENOMINADOR DO DESCONTO. Este fala: "menos setenta por cento" e uma divisao, o
numero de baixo e um preco de referencia, e a lista de desejos do proprio
espectador diz se aquele preco de referencia ja foi cobrado alguma vez. A
decisao com prazo que o longo responde: esta promocao que acaba domingo e
promocao ou nao?

VEREDITO: `canal frio` (v_maquina_licoes, 04/10/2026) — eixo novo e piso de oito
minutos por analogia com `suspenso`. Com oito capitulos e o MARGEM_CAP o minimo
aritmetico ja e 514 s, entao o alvo fica logo acima disso.

ALAVANCA B, E A LICAO 575 APLICADA: a `en-GB-RyanNeural` tem residuo de mais um
virgula dois por cento no `ensaio.py`. Entao a resposta foi posicionada pela
estimativa CORRIGIDA, nao pela crua — foi exatamente o erro que custou dois
segundos no seja-mais-magra-009, onde eu mirei 190,6 s crus na Francisca de
mais quatro virgula nove por cento e o bloco da resposta terminou em 202,2 s.

SHORT: quarenta segundos, e a mudanca vem do numero DESTE canal. Os dois shorts
mais vistos aqui tem quarenta virgula seis e quarenta e um segundos; o menos
visto tem quarenta virgula nove, entao duracao nao e o fator — mas nao ha
motivo para encurtar para trinta como no setiap-level, onde os curtos mediram
melhor de verdade.

TITULO PROPRIO DO SHORT: tem. Seis dos sete pacotes deste canal mandaram o short
herdar o titulo do longo (so o 002 teve titulo proprio, e foi o segundo mais
visto). Aprendizado 548.
"""

import json

CENAS = []

# Resolvidos em 05/10/2026 por `pg_net` dentro do Postgres — `net.http_get` para
# api.pexels.com com a chave lida do `config` na mesma consulta, entao ela nao
# atravessa a sandbox nem o chat (aprendizado 574). No runner a busca nao roda:
# `api.pexels.com` da TimeoutError em 7 de 7 cenas pela faixa de IP dele.
BROLL = {
    6994624: ("https://videos.pexels.com/video-files/6994624/6994624-hd_1280_720_30fps.mp4",
              "Kindel Media",
              "https://www.pexels.com/video/a-girl-shopping-online-6994624/"),
    7668105: ("https://videos.pexels.com/video-files/7668105/7668105-hd_1280_720_25fps.mp4",
              "Pavel Danilyuk",
              "https://www.pexels.com/video/close-up-view-of-a-person-playing-7668105/"),
    8479266: ("https://videos.pexels.com/video-files/8479266/8479266-hd_1280_720_25fps.mp4",
              "ArtHouse Studio",
              "https://www.pexels.com/video/close-up-video-of-a-person-counting-8479266/"),
    8342359: ("https://videos.pexels.com/video-files/8342359/8342359-hd_1280_720_25fps.mp4",
              "Pavel Danilyuk",
              "https://www.pexels.com/video/girl-writing-in-notebook-8342359/"),
}


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def B(kicker, sub, nar, q, pexels_id=None, cap=None):
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q}
    if pexels_id and pexels_id in BROLL:
        link, autor, pagina = BROLL[pexels_id]
        c["broll_url"] = link
        c["broll_credito"] = {"pexels_id": pexels_id, "autor": autor,
                              "url": pagina}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================= THE FIRST TWO HUNDRED SECONDS =======================

# -------------------------------------------------------------------- cap 1
T("Minus seventy percent", "of what, exactly",
  "A discount is a division. The number on the banner is the top of it, and "
  "the bottom is a price someone chose. You can find out which one.",
  cap="A discount is a division, and you can see the bottom of it")
T("Nobody is lying", "the maths is real",
  "The store is not making the percentage up. It divides honestly. The "
  "question is only what it divides by.")
B("Two numbers", "on the same page",
  "And both numbers are on the page you are already looking at: the price "
  "today, and the price it is being compared against.",
  "person browsing a game store on a laptop", 6994624)
T("The one that matters", "is the bottom one",
  "The bottom one is the reference price. It is usually the launch price, and "
  "that is not the same as a price charged for long.")
T("What this costs you", "in a decision, not in money",
  "That difference costs you a decision: a record sale and a sale five "
  "dollars off the usual floor look identical on the banner.")
T("Not a scam", "a denominator",
  "This is not a scam. It is a denominator, and reading one is a skill you "
  "can have in a minute.")
T("No number of mine", "in any of this",
  "There is no number of mine in this. No average discount, no store name. "
  "Both numbers come off your own screen.")
T("Your deadline too", "the sale ends Sunday",
  "The deadline is yours as well: the sale on your list ends on a date the "
  "page already shows you.")

# -------------------------------------------------------------------- cap 2
T("Where the bottom comes from", "three possibilities",
  "The reference price is one of three things, and which one changes what the "
  "percentage means.",
  cap="What the reference price actually is")
T("The first", "the launch price",
  "The first is the launch price: what the game cost on day one. It may not "
  "have been charged since that first week.")
T("The second", "the current list price",
  "The second is the current list price, which a publisher can raise or lower "
  "whenever it wants.")
B("The third", "the regional price",
  "The third is the price for your region, which can differ from the one in "
  "the trailer and from the one your friend sees.",
  "hand holding a game controller close up", 7668105)
T("All three are legitimate", "and none is the floor",
  "All three are legitimate. None is the lowest the game actually sold for, "
  "and that is the number you need.")
T("The floor", "what it has really gone down to",
  "Call it the floor: the cheapest this game has ever actually been. It is "
  "not on the banner, and that is exactly why it is useful.")
T("Why the floor", "it is the only honest comparison",
  "The floor is the only honest comparison: it is the one price you know was "
  "actually paid.")
T("And it is personal", "your floor, not the internet's",
  "And the floor belongs to you. The cheapest price that existed somewhere is "
  "not the cheapest that existed for your account.")
T("What comes next", "the account, in two steps",
  "What comes next is the account. Two steps, two numbers, and nothing beyond "
  "the store page you already have open.")

# -------------------------------------------------------------------- cap 3
T("Step one", "today's price",
  "Step one: the price today — what you would actually be charged, after the "
  "discount, in your own currency.",
  cap="The account: two numbers, one division")
T("Not the banner", "the checkout line",
  "Not the banner. The checkout line, because regional pricing and taxes "
  "land there.")
T("Step two", "the floor",
  "Step two: the floor — the cheapest that game has ever been for you. Your "
  "purchase history and wishlist alerts hold it.")
T("If you never saw it low", "use the lowest you ever saw",
  "Never seen it cheap? Use the lowest you have personally seen. An "
  "imperfect floor still beats the launch price.")
T("Now divide", "today by the floor",
  "Now divide today's price by the floor. Not the other way round.")
T("The result", "that is your real discount",
  "If the result is one, this sale matches the best price you have ever seen. "
  "Above one, you are paying more than the floor. Below one, this is genuinely "
  "the cheapest it has been for you.")
T("Turn it into a percent", "if you prefer",
  "Subtract one and multiply by one hundred if you prefer a percentage. A "
  "result of one point two means twenty percent above your own floor.")
T("Keep both", "today and the floor",
  "Keep both numbers, not just the ratio. Without the floor written down you "
  "cannot tell next time whether the floor moved or the sale did.")

# ============================ AFTER THE ANSWER ===============================

# -------------------------------------------------------------------- cap 4
T("Why not the list price", "it is a choice, not a fact",
  "The reason to divide by the floor and not the list price is simple: the "
  "list price is a decision somebody makes, and the floor is a thing that "
  "happened.",
  cap="Why the floor beats the list price")
T("A list price can move", "upward, before a sale",
  "A list price can move up. When it does, every percentage measured from it "
  "gets larger without a single cent coming off what you pay.")
T("The floor cannot move up", "it only ever goes down",
  "A floor cannot move up. It is the lowest value in a history, so new data "
  "either lowers it or leaves it alone. That is what makes it a baseline.")
T("Same page, two stories", "and only one is checkable",
  "So the same page tells two stories. One is a percentage off a number "
  "chosen by the seller; the other is a ratio against a number from the past.")
T("You are not cynical", "you are using a baseline",
  "Using the floor does not mean assuming bad faith. It means comparing "
  "against a fixed point instead of a moving one, which is what a baseline "
  "is for.")
T("And it works both ways", "it also finds real sales",
  "And it works in your favour too. A ratio below one is a genuine record "
  "low, and the banner will not tell you that either.")
T("The number is not a verdict", "on the game",
  "The ratio says nothing about whether the game is good or worth your "
  "evening. It says what this price is, compared with prices that existed.")
T("Next", "how to read a sale with it",
  "What is left is using it. How to look at a sale and decide, with two "
  "conditions.")

# -------------------------------------------------------------------- cap 5
T("Two conditions", "both have to hold",
  "Two conditions, and a sale has to clear both before it counts as a real "
  "one for you.",
  cap="How to decide whether a sale is a sale")
T("Condition one", "the ratio is at or below one",
  "Condition one: the ratio is at one or below. At one it matches your floor; "
  "below one it beats it.")
T("Condition two", "you wanted it before the banner",
  "Condition two: the game was on your list before you saw the banner. A "
  "discount on something you had not wanted is not a saving, it is a purchase.")
B("Both, not either", "that is the whole filter",
  "Both, not either. Condition one without condition two is how a wishlist "
  "turns into a library you never open.",
  "writing numbers on a notepad with a calculator", 8479266)
T("When the ratio is above one", "waiting costs nothing",
  "When the ratio comes out above one, waiting costs you nothing except "
  "patience, because the floor already proved that price is reachable.")
T("When it is well below one", "that is the moment",
  "When it comes out well below one, that is the moment, and your own history "
  "is what told you so rather than the size of the banner.")
T("What not to do", "change the floor to fit",
  "What not to do: quietly raise the floor in your head so the sale passes. "
  "The floor is a record, not an opinion, and editing it defeats the point.")
T("And do not compare games", "compare each with itself",
  "And do not compare one game's ratio with another's. Each floor belongs to "
  "one game, in one region, for one person.")

# -------------------------------------------------------------------- cap 6
T("Three mistakes", "the floor makes visible",
  "With a floor written down, three ordinary mistakes become obvious. All "
  "three are the same confusion: reading the percentage as the saving.",
  cap="Three mistakes the floor makes visible")
T("Mistake one", "trusting the banner size",
  "Mistake one: trusting the size of the percentage. A ninety percent off a "
  "launch price can be worse than a thirty percent off a current one.")
T("Mistake two", "buying the bundle for the discount",
  "Mistake two: taking the bundle because the bundle shows the bigger number. "
  "Divide by your floor for the one game you actually wanted.")
T("Mistake three", "treating the first sale as the best",
  "Mistake three: assuming the first sale after launch is the deepest. For "
  "most games it is the shallowest one they will ever run.")
T("None of the three", "is being bad with money",
  "None of the three is being careless. All three are reading a ratio without "
  "knowing its denominator, which is a measurement problem with a "
  "measurement fix.")
T("The expensive case", "buying at twice your floor",
  "The expensive case is buying at twice your own floor during a sale that "
  "felt generous, which happens most often with games you have been watching "
  "for a long time.")
T("And the reverse", "waiting past a record low",
  "The reverse costs too: waiting through a genuine record low because the "
  "banner looked ordinary, then paying more three months later.")
T("One number fixes both", "and it is the same one",
  "The same floor fixes both cases, which is why it is worth the minute it "
  "takes to look up.")

# -------------------------------------------------------------------- cap 7
T("What to write down", "and in what shape",
  "The shape of the record matters, because it decides whether this still "
  "works for you in six months.",
  cap="What to record, and why two numbers and not one")
T("Per game, two numbers", "the floor and the date",
  "Per game, write two things: the floor, and the date you saw it. The date "
  "is what tells you later whether the floor is stale.")
T("Not the percentage", "it is not a number about the game",
  "Do not record the percentage. It belongs to one banner on one day and it "
  "describes the seller's choice, not the game's price history.")
T("Five games is enough", "you do not need a database",
  "Five games is enough to start. You do not need a database, and the ones "
  "worth tracking are the ones you keep almost buying.")
B("Any list works", "paper included",
  "Any list works. Paper, notes app, a spreadsheet. What it must show is the "
  "number and the date, not a chart with the shape smoothed out.",
  "person writing in a notebook at a desk", 8342359)
T("In one sale season", "you have a baseline set",
  "After one sale season you have five floors with dates, and a banner stops "
  "being the thing that decides.")
T("And floors do fall", "that is information too",
  "Floors do keep falling, and that is information as well: a floor that "
  "dropped twice in a year is telling you about the game's demand.")
T("None of this costs", "anything at all",
  "And none of this requires an extension, a subscription or a tool. It "
  "requires two numbers and one division.")

# -------------------------------------------------------------------- cap 8
T("One caveat", "about what this is not",
  "Before the end, one caveat, and it matters more than the account does.",
  cap="What this account does NOT say")
T("It does not say", "whether to buy",
  "This does not tell you whether to buy anything. It tells you where this "
  "price sits against prices that existed. Whether the game is worth it is "
  "not a number.")
T("It is not a price prediction", "the floor is history",
  "It is also not a forecast. A floor is a record of the past, and nothing "
  "guarantees the game goes that low again.")
T("Regional prices differ", "so floors are personal",
  "And because regional pricing exists, your floor is yours. Someone else's "
  "screenshot of a cheaper price is not your floor.")
T("What you are left with", "a ratio, and that is all",
  "What you are left with is one ratio, computed from your own screen and "
  "your own history. At or below one, it is a real sale for you.")
T("And one more limit", "it says nothing about value",
  "It also says nothing about whether the price is fair. A game can sit at "
  "its floor and still cost more than an evening is worth to you, and that "
  "judgement is not something a ratio can hand over.")
T("Start with one game", "the one you keep almost buying",
  "Start with one game: the one you keep almost buying. Look up its floor "
  "today, before the next banner.")
C("Put your ratio below", "just the number",
  "In the comments, put just the ratio for one game. Not the title, not the "
  "price. I want to see how far from one these land during the same sale.")

# ================================== SHORT ====================================

# O short fecha UMA pergunta — esta promocao e promocao? — com a divisao
# inteira, e o longo abre OUTRA: o que fazer quando a razao da acima de um
# (aprendizado 563). Quarenta segundos, porque os dois shorts mais vistos deste
# canal tem quarenta virgula seis e quarenta e um.

SHORT = [
    {"layout": "titulo", "kicker": "Minus seventy percent", "sub": "of what",
     "nar": "A discount is a division, and the bottom of it is a price "
            "somebody chose. Here is how to check your own.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "First", "sub": "the checkout price",
     "nar": "First: the price at checkout today, in your currency, after the "
            "discount. Not the number on the banner.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Second", "sub": "your floor",
     "nar": "Second: the cheapest that game has ever been for you. Your "
            "purchase history holds it.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Divide", "sub": "today by the floor",
     "nar": "Divide today by the floor. At one, it matches your best price "
            "ever. Above one, you are paying over your own floor.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "When it comes out above one",
     "sub": "two conditions, in the video",
     "nar": "What to do when it lands above one is two conditions, and both "
            "are in the video.",
     "sem_cap": True},
]

THUMB = {"l1": "Off what", "l2": "exactly"}

COPY = """# The denominator of a discount, and how to find your own floor

## TITULO
Seventy Percent Off What? The Reference Price in Your Wishlist, and the Real Floor

## TITULO SHORT
Seventy percent off what, exactly?

## DESCRICAO
A discount is a division. The percentage on the banner is the top of it, and the bottom is a price somebody chose — usually the launch price, sometimes the current list price, sometimes the price for your region. The store is not making the maths up. The only question is what it divides by, and you can find that out from the page you already have open.

The number you actually need is not on the banner: it is the floor — the cheapest that game has ever genuinely been for you. The floor has one property the list price does not. A list price is a decision, and it can move upward, which makes every percentage measured from it look bigger without a cent coming off what you pay. A floor is the lowest value in a history, so new data either lowers it or leaves it alone. That is what makes it a baseline.

The account has two steps and no number of mine. Step one: the price at checkout today, in your currency, after the discount — the line at checkout and not the poster, because regional pricing and taxes land there. Step two: the floor, which your own purchase history and your wishlist alerts already hold; if you have never seen the game cheap, use the lowest price you have personally seen on it, because an imperfect floor still beats the launch price. Then divide today by the floor. At one, this sale matches the best price you have ever seen. Above one, you are paying more than your own floor. Below one, it is a genuine record low — and the banner will not tell you that either.

The video closes that account in the first three minutes, then shows what to do with the ratio: the two conditions a sale has to clear before it counts (the ratio at or below one, AND the game was on your list before you saw the banner), three mistakes the floor makes visible, and what to record per game so this still works for you next sale season.

One caveat that matters more than the account: this does not tell you whether to buy anything, and it is not a forecast. A floor is a record of the past, and nothing guarantees a game goes that low again. Whether a game is worth your evening is not a number.

CAPITULOS
{CAPITULOS}

In the comments, put just the ratio for one game. Not the title, not the price. I want to see how far from one these land during the same sale.

## DISCLOSURE
Narration and visuals in this video are computer-generated. The script is original, and this is information, not financial or purchasing advice.

## HASHTAGS
#gamedeals #gamingprices #wishlist

## TAGS
game discounts, reference price, wishlist price history, real discount, price floor, how to read a sale, steam sale maths, regional pricing, list price vs floor, record low price, game price tracking, is this sale good, launch price, discount denominator, when to buy games

## COMENTARIO FIXADO
The whole thing in two lines: take the checkout price today, in your currency; take the cheapest that game has ever actually been for you. Divide today by the floor. At or below one it is a real sale; above one you are paying over your own floor. Put just that ratio here — not the title, not the price.

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita desconto medio de nenhuma loja, nao cita politica de preco de nenhuma plataforma, nao cita nome de loja, de publisher nem de rastreador de preco, nao cita quanto tempo um jogo leva para chegar ao piso e nao cita percentual tipico de promocao. Os dois numeros da conta sao do proprio espectador: o preco no checkout dele, na moeda dele, e o menor preco que ELE ja viu naquele jogo. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA, e por que: (1) qualquer afirmacao sobre COMO cada loja calcula o preco de referencia, porque isso varia por loja, por regiao e por acordo com o publisher, e eu nao fecharia esse numero em duas fontes institucionais — o video diz que o preco de referencia pode ser preco de lancamento, preco de tabela atual ou preco regional, que sao as tres possibilidades, sem atribuir nenhuma a nenhuma loja especifica; (2) qualquer previsao de quando um jogo volta ao piso, porque piso e registro do passado e tratar registro como previsao e o erro oposto ao que o video corrige; (3) qualquer juizo sobre o jogo — o video diz explicitamente que a razao nao fala do jogo, so do preco contra precos que existiram. ESTE EIXO SUBSTITUI O NUMERO INSTITUCIONAL DE PROPOSITO, e a escolha tem uma ressalva honesta: os dois shorts mais vistos deste canal (noventa e uma e cinquenta e duas views) entregaram FATO sobre a industria, e os dois de metodo entregaram dezoito e duas. A ordem de views, porem, e quase a ordem de antiguidade — 002 e 003 sao de agosto e 008 e de setembro — e com sete pontos nao da para separar forma de data. Entao este pacote tenta a sintese: conta do espectador, mas ancorada num numero que ele ve na propria tela de loja e confere em dez segundos. Se o short passar de cinquenta views foi a sintese; se ficar abaixo de vinte, a ancora nao bastou.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/game-money-lab-009.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "game-money-lab",
    "pacote": "game-money-lab-009",
    "idioma": "en",
    "voz": "en-GB-RyanNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#181C2A", "c1": "#EF476F", "c2": "#22D3EE",
               "bg": "#F4F4F8"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": _copy_existente(),
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada, duracao_estimada_short, duracao_cena
    grava(SPEC, "fabrica/specs/game-money-lab-009.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
    t, ult = 0.0, None
    for c in CENAS:
        if c.get("cap"):
            if ult:
                print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s")
            ult = (c["cap"], t)
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
    if ult:
        print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s")
    # ONDE A RESPOSTA FECHA, crua e CORRIGIDA pelo residuo da voz. O
    # aprendizado 575 existe porque eu mirei a crua uma vez e perdi por 2,2 s.
    RESIDUO = 1.012   # en-GB-RyanNeural, +1,2% no ensaio.py
    t = 0.0
    for i, c in enumerate(CENAS):
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
        if "If the result is one" in (c.get("nar") or ""):
            print(f"  a divisao fecha em {t:.1f}s cru -> "
                  f"{t * RESIDUO:.1f}s corrigido (cena {i})")
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: "
                  f"{c['broll_q']}")
