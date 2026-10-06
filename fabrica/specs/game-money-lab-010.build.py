"""game-money-lab-010 — o imposto no preco do jogo e decidido onde VOCE esta.

ALAVANCA ATACADA: A (conversao short -> inscrito), pela FORMA do pacote.

O NUMERO DE PARTIDA, do PROPRIO canal, deduplicado e com a ULTIMA leitura de
`metricas` (a trava do 549 acusou 170 quedas em 4.046 linhas lifetime nesta
rodada — `max(views)` esta proibido, aprendizados 592 e 594):

    pacote  short -> longo  dur   titulo
    006        18 ->   6    567s  In-Game Currency: Two Divisions That Show What You Actually Paid
    002        52 ->   2    736s  $300 Million Per Game: The Math That Broke AAA
    004        21 ->   2    730s  Gaming Layoffs 2026: Forecast Revised Up 78%
    007         7 ->   2    484s  The Refund Button Is Not the Right: Fourteen Days
    003        91 ->   1    736s  GTA 6 Costs $80: The 20-Year Price Freeze
    005         8 ->   1    701s  1,294,188 Signatures: Why the EU Chose a Code of Conduct
    008         2 ->   0    546s  Sale Haul or Full Price?
    009         0 ->   0    577s  publicado ontem, sem leitura

A HONESTIDADE SOBRE A ESCALA, primeiro: o teto deste canal e SEIS views de
longo e ele tem ZERO inscritos depois de oito pacotes. Como no
next-level-money, numeros desse tamanho NAO PERMITEM ler sinal dentro do canal.
A diferenca entre seis e duas views e ruido. Nao vou inventar padrao.

O QUE DA PARA DIZER, e sao duas coisas que nao dependem de distinguir dois de
seis:
  1. O MAIOR short do canal — noventa e uma views, o pacote 003 — entregou UMA
     view de longo. O segundo maior (52) entregou duas. Mesma direcao do
     aprendizado 594 em escala de frota, e agora em quatro canais no mesmo dia.
  2. O unico pacote acima do ruido (006) e um pacote de METODO: "Two Divisions
     That Show What You Actually Paid". E a forma da alavanca A em estado puro
     — uma conta que a pessoa faz na propria compra. E e o segundo mais curto.
  E os dois titulos em PERGUNTA pura (008 e 009) deram zero.

O QUE VOU MUDAR: repetir a forma do 006 — uma conta sobre a propria compra —
num eixo que o canal nunca tocou, e ficar no piso de oito minutos.

VEREDITO DO CANAL: `canal frio` (v_maquina_licoes, 7 shorts e 7 longos
medidos, 213 views). Eixo novo e piso de 8 minutos por analogia com
`suspenso`. Saiu em 8,9 min.

EIXO, e por que ele e novo. Os oito pacotes falam de moeda interna, orcamento
AAA, demissoes, direito de reembolso, preco do GTA, peticao europeia, preco por
hora jogada e preco de referencia na wishlist. NENHUM fala de IMPOSTO — e o
imposto e a parte do preco que nao vai para o jogo nem para a loja.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ESTE VIDEO NAO CITA NENHUMA ALIQUOTA. Nenhuma. Aliquota muda por pais e por
# ano, e video que recita aliquota nasce com data de validade. O que entra e a
# REGRA DE LUGAR, fechada em DUAS INSTITUICOES que dizem a mesma coisa:
#
#   * legislation.gov.uk (The National Archives, texto oficial da legislacao),
#     Value Added Tax Act 1994, Schedule 4A, paragrafo 15(1): "A supply to a
#     person who is not a relevant business person of services to which this
#     paragraph applies is to be treated as made in the country in which the
#     recipient belongs" — e o 15(2)(a) diz que o paragrafo se aplica a
#     "electronically supplied services".
#   * gov.uk, orientacao do HMRC sobre servicos digitais a consumidores, que
#     diz, com estas palavras: "the place of supply rules set a common
#     framework for deciding in which country a transaction should be subject
#     to tax"; "If you are a business making supplies of digital services to UK
#     consumers, those supplies are liable to UK VAT. If you make supplies of
#     digital services to consumers outside the UK these are not liable to UK
#     VAT. They may be liable to VAT in the country where the consumer is
#     based."; e "If you supply digital services to consumers via a third party
#     platform or marketplace, the digital platform is responsible for
#     accounting for VAT on the supply instead of you."
#
#   As duas batem no que importa: o imposto segue o CONSUMIDOR, nao o
#   vendedor; e numa loja, quem responde pelo imposto e a LOJA, nao quem fez o
#   jogo.
#
# DESCARTADO, e por que — isto e o que eu QUERIA dizer e nao disse: eu ia
# afirmar a regra EUROPEIA tambem, pelo texto da Diretiva do IVA. NAO ENTRA.
# O eur-lex.europa.eu devolveu 202 (pagina de desafio, sem texto) nesta rodada,
# as duas paginas da Comissao sobre IVA digital deram 404 e o oecd.org deu 403.
# Entao eu li e verifiquei UMA jurisdicao, e o video diz exatamente isso: diz
# qual texto eu li, e manda a pessoa procurar a regra e a aliquota do pais
# DELA. Nao afirmo o conteudo de lei que nao consegui abrir.
#
# TAMBEM FORA: nao digo que o imposto e alto, baixo, justo ou injusto; nao digo
# que loja ou estudio ganha ou perde com isso; e nao ensino ninguem a mudar de
# regiao de conta para pagar menos — isso costuma violar os termos da loja e o
# video nao vai por ali.
#
# O NUMERO QUE DECIDE E DO ESPECTADOR: o recibo dele e a aliquota do pais dele.
# Uma divisao sobre o proprio preco pago mostra quanto daquele dinheiro era
# imposto — e essa parte nunca foi para o jogo.
"""
import json

CENAS = []


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


# Link gravado na spec pela busca via `pg_net` dentro do banco, que e onde a
# chave do Pexels mora. Com o link gravado o pacote fica reproduzivel.
BROLL = {
    # Pessoa jogando no console, sob a cena que fala do "last game you bought".
    # 22 s para uma cena de 10,3 s.
    7985919: ("https://videos.pexels.com/video-files/7985919/7985919-hd_1920_1080_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/man-playing-game-console-7985919/"),
    # Pessoa com cartao na mao usando o laptop — a compra de onde sai o recibo
    # que o capitulo da resposta manda abrir. 18 s / 6,4 s.
    8937990: ("https://videos.pexels.com/video-files/8937990/8937990-hd_1920_1080_30fps.mp4",
              "Leeloo The First",
              "https://www.pexels.com/video/person-holding-a-card-while-using-a-laptop-8937990/"),
    # Navegando numa LOJA online, sob o capitulo que explica que quem responde
    # pelo imposto e a loja e nao quem fez o jogo. 14 s / 9,2 s.
    7568745: ("https://videos.pexels.com/video-files/7568745/7568745-hd_1920_1080_25fps.mp4",
              "Ivan S",
              "https://www.pexels.com/video/person-browsing-on-online-store-7568745/"),
}

# TRES b-rolls, nao quatro, e de proposito. Os capitulos 2, 7 e 8 pedem
# "texto de lei" e "mao escrevendo", e nenhuma das buscas desta rodada
# devolveu clipe que diga isso sem forcar. Clipe que nao casa com a narracao e
# pior que lower-third: ja descartei quatro vezes o mesmo clipe de "TAX FRAUD"
# por isso. Fica em tres bem casados.


def B(kicker, sub, nar, q, pexels_id, cap=None):
    link, autor, pagina = BROLL[pexels_id]
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q, "broll_url": link,
         "broll_credito": {"pexels_id": pexels_id, "autor": autor,
                           "url": pagina}}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================
# A resposta — uma divisao sobre o proprio preco pago — fecha no capitulo 3.

# -------------------------------------------------------------------- cap 1
B("Part of the price never reaches the game", "and the rule says where it goes",
  "A part of what you paid for your last game never reached the studio and "
  "never reached the store. And the rule that decides that part is about you.",
  "person playing on a game console", 7985919,
  cap="Part of the price never reaches the game")
T("Not about the studio", "about where you are",
  "It is not about where the studio is, and not about where the company is "
  "registered. The rule turns on where the person buying the thing is.")
T("That rule has a name", "place of supply",
  "That rule has a name: place of supply. It decides, for tax purposes, in "
  "which country a transaction is treated as having happened.")
T("And it is written down", "in one short paragraph",
  "And it is written down in one short paragraph, which I am going to read the "
  "sense of in a moment. Short enough that you can check me.")
T("Why this is not trivia", "because it changes what you compare",
  "This is not trivia, because it decides what you are comparing when you "
  "compare prices across two countries. Two different numbers can hold the same price.")
T("And one more thing", "on a store, the store answers for it",
  "There is one more piece, and it surprises people: when the sale happens "
  "through a store or marketplace, the store is the one that accounts for the tax.")
T("The number that is yours", "your receipt",
  "And there is a number that only you have: your own receipt, and the rate "
  "where you live. That is what we are going to divide.")

# -------------------------------------------------------------------- cap 2
T("What the paragraph says", "and I will name it exactly",
  "Now the text. I am going to name the instrument exactly, so that you can "
  "open it yourself instead of taking my word for it.",
  cap="What the paragraph says")
T("The instrument", "an act, a schedule, a paragraph",
  "It is the United Kingdom's Value Added Tax Act of nineteen ninety four, "
  "Schedule four A, paragraph fifteen. Three coordinates, and it is findable.")
T("What paragraph fifteen sets", "treated as made where the recipient belongs",
  "Paragraph fifteen says that a supply to a person who is not a business is "
  "to be treated as made in the country in which the recipient belongs.")
T("And what it applies to", "electronically supplied services",
  "And the next part lists what it applies to. The first item on that list is "
  "electronically supplied services, which is what a downloaded game is.")
T("Read those two together", "and the whole thing follows",
  "Read those two sentences together and the whole thing follows: for a "
  "digital purchase by a private person, the country that counts is yours.")
T("The agency says the same", "in plainer words",
  "The tax authority's own guidance says the same in plainer words: supplies "
  "to consumers in the country are liable to that country's tax.")
T("And supplies outside it", "are not",
  "And it adds the mirror: supplies to consumers outside the country are not "
  "liable to it, and may be liable where that consumer is based instead.")

# -------------------------------------------------------------------- cap 3
B("Now divide your own receipt", "three inputs, one division",
  "Now your turn. You need three things, and two of them you already have.",
  "paying online with a card and laptop", 8937990,
  cap="Now divide your own receipt")
T("Input one", "what you actually paid",
  "The first is the amount you actually paid for the last game you bought. "
  "The total, as it appeared on the receipt, not the shelf number.")
T("Input two", "the rate where you live",
  "The second is the rate that applies where you live. Look that up on your "
  "own country's tax authority page, because I am not going to say a number here.")
T("Input three", "whether the price included it",
  "The third is whether the price you saw already included the tax. For "
  "consumers that is usually the case, and the receipt normally says so.")
T("The division", "paid, divided by one plus the rate",
  "If it was included, divide what you paid by one plus the rate written as a "
  "decimal. The result is the part that was the price before tax.")
T("Subtract to see the rest", "and that is your number",
  "Subtract that result from what you paid. What is left is the tax you paid, "
  "and that part never reached the game. That is your number.")
T("Write both on one line", "paid, and of which tax",
  "Write both figures on one line: what you paid, and of that, how much was "
  "tax. The rest of this is only so you do not misread it.")

# -------------------------------------------------------------------- cap 4
B("Why the store, not the studio", "and this is in the guidance",
  "First refinement, and it is written in the guidance: when the sale goes "
  "through a third party store or marketplace, the store accounts for the tax.",
  "browsing an online store", 7568745,
  cap="Why the store, not the studio")
T("What that means in practice", "the developer is not the one filing",
  "In practice that means the developer is not the one filing that tax for "
  "your purchase. The platform is, and it does it for every country it sells into.")
T("So the storefront carries it", "and that is why prices differ",
  "That is part of why the same game shows different numbers in different "
  "stores and countries. The tax is attached to your location, not to the game.")
T("It is not a markup", "and not the studio's choice",
  "So a higher number in your country is not automatically a markup by the "
  "studio. Part of it may be a rate that neither the studio nor you chose.")
T("And not always", "regional pricing exists too",
  "But be careful with the reverse claim as well: stores also set regional "
  "prices deliberately. Tax explains part of the gap, not all of it.")
T("Which is why you divide", "to separate the two",
  "That is exactly why the division matters. It separates the part that is tax "
  "from the part that is a pricing decision, instead of guessing which is which.")
T("One number, two causes", "and now you can tell them apart",
  "The number on the page has at least two causes, and until you divide, they "
  "look like one. After you divide, they do not.")

# -------------------------------------------------------------------- cap 5
T("What people get wrong", "and almost none of it is carelessness",
  "Now the part that gets read wrong most, and almost none of it is "
  "carelessness. There are good reasons the picture is confusing.",
  cap="What people get wrong")
T("First reason", "the shelf price hides it",
  "First: for consumers the displayed price usually already contains the tax, "
  "so there is nothing on the page that looks like a tax line at all. Nothing "
  "is being hidden from you — it is simply shown as one number.")
T("Second reason", "the currency moves too",
  "Second: when you compare two countries you are also comparing two "
  "currencies, and the exchange rate moves independently of any rule.")
T("Third reason", "the rate is not one rate",
  "Third: a country can apply more than one rate, and which of them applies to "
  "a digital good is a question about that country's own list of categories, "
  "which is published separately from the rule itself.")
T("Fourth reason", "the seller may not be where you think",
  "Fourth: the legal seller of a digital game is often the platform, not the "
  "studio whose logo is on the box art.")
T("Fifth reason", "sales change the base",
  "Fifth: a discount changes the base the tax is computed on, so the tax "
  "amount falls with the price. The share stays, the amount does not.")
T("So before concluding", "divide first, judge second",
  "So before concluding that someone is overcharging you, do the division. "
  "The order matters: divide first, judge second.")

# -------------------------------------------------------------------- cap 6
T("What this does not mean", "and I will be exact",
  "Now the limits, and I will be exact, because this is where a video like "
  "this usually says more than its sources do.",
  cap="What this does not mean")
T("No judgement on the rate", "high or low is not my claim",
  "First: I am not saying the rate is high, low, fair or unfair. I read where "
  "the rule points, and that is a different question from what it should be.")
T("No claim about winners", "not store, not studio",
  "Second: I am not telling you that the store wins or the studio loses. Who "
  "bears what is an economics question this video does not answer.")
T("No region switching", "and I mean that plainly",
  "Third: I am not telling you to change your account region to pay less. "
  "That usually breaks the store's own terms, and this video does not go there.")
T("One jurisdiction read", "and I will say which",
  "Fourth, and this is the real limit: I read one country's text, and I named "
  "it. I am not asserting the wording of any other country's law.")
T("Why I say that out loud", "because I could not open the others",
  "I say it out loud because I tried to open two other official sources for "
  "this and could not. So I am telling you what I verified, and nothing beyond it.")
T("What you get instead", "the question to ask at home",
  "What you get instead is the exact question to ask about your own country, "
  "and the division to run once you have the answer.")

# -------------------------------------------------------------------- cap 7
T("What I left out on purpose", "and this part is usually skipped",
  "Now the part that is usually skipped entirely. Things are missing from this "
  "video on purpose, and I will name each one.",
  cap="What I left out on purpose")
T("No rates", "not one percentage",
  "First: no rates. Not a single percentage, because rates differ by country "
  "and get changed, and a recited rate is wrong soon and stays online.")
T("No country comparison table", "that is a snapshot, not a rule",
  "Second: no table comparing countries. Any such table is a snapshot of a "
  "day, and this video is about the rule that outlives the snapshot.")
T("No business rules", "this is the consumer side",
  "Third: nothing about business to business supplies. The paragraph I read is "
  "specifically about a person who is not a business, and that is you here.")
T("No other taxes", "import, customs, or anything else",
  "Fourth: no import duty, no customs, no other charge. One tax, one rule, one "
  "division — widening it would mean sources I do not have.")
T("And nothing about your account", "I cannot see your receipt",
  "Fifth: nothing about your specific purchase. I have not seen your receipt "
  "and I do not know which rate applied to it.")
T("The rule I follow", "two sources, or it stays out",
  "The rule I follow is simple: if it does not match in two official sources, "
  "it does not go in the video. That is why this one is narrow and checkable.")

# -------------------------------------------------------------------- cap 8
T("Four steps", "start to finish",
  "Here is the whole thing in four steps, so you can run it after this ends.",
  cap="Four steps")
T("Step one", "open your last receipt",
  "Step one: open the receipt for the last digital game you bought. The email "
  "or the purchase history both work.")
T("Step two", "find your own rate",
  "Step two: look up the rate your country applies to digital goods, on your "
  "own tax authority's page. Write it down as a decimal.")
T("Step three", "divide, then subtract",
  "Step three: divide the amount you paid by one plus that decimal, then "
  "subtract the result from what you paid. That difference is the tax.")
T("Step four", "write both numbers down",
  "Step four: write the amount paid and the tax amount side by side, with the "
  "date. One line per purchase, on the same sheet.")
T("Then one comparison", "the same game, another country",
  "Then, if you want one more thing, compare that line with the listed price "
  "of the same game in another country, and see how much of the gap your division explains.")
T("Repeat on the next sale", "because the base moves",
  "Repeat it on your next discounted purchase, because the tax amount falls "
  "with the price while the share stays the same. Two lines show that immediately.")
T("And one note", "if there is no receipt, that is step zero",
  "One last note: if you cannot find a receipt, that is not a dead end. "
  "Finding where your purchase history lives is your actual first step.")

C("Post the share, not the receipt", "the percentage, not your purchases",
  "In the comments, post only the share of your price that turned out to be "
  "tax. Do not post your receipt, your account or what you bought.")

THUMB = {"l1": "One division", "l2": "two causes"}


SHORT = [
    {"layout": "titulo", "kicker": "Part of the price never reaches the game",
     "sub": "and the rule is about you",
     "nar": "Part of what you paid for your last game never reached the studio "
            "or the store. The rule that decides it is about you.", "sem_cap": True},
    {"layout": "titulo", "kicker": "One", "sub": "taxed where you belong",
     "nar": "One: for a private buyer, a digital supply is treated as made in "
            "the country where the recipient belongs.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Two", "sub": "the store accounts for it",
     "nar": "Two: when the sale goes through a store or marketplace, the store "
            "accounts for the tax, not the developer.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Three", "sub": "divide by one plus the rate",
     "nar": "Three: divide what you paid by one plus your rate, then subtract. "
            "The difference is the tax.", "sem_cap": True},
    {"layout": "titulo", "kicker": "And that part", "sub": "never reached the game",
     "nar": "That part never reached the game. Divide first, then judge whether "
            "a price gap is a markup.", "sem_cap": True},
]


COPY = """# game-money-lab-010

## TITULO
The Tax in Your Game Price Is Set Where You Live: Schedule 4A, Paragraph 15

## TITULO SHORT
Schedule 4A: taxed where you live

## DESCRICAO
A part of what you paid for your last game never reached the studio and never
reached the store. The rule that decides that part is not about where the
company is registered — it is about where you are. This video does not quote a
single rate, and that is deliberate. What it gives you is the rule, the exact
place it is written, and one division you can run on your own receipt.

The rule has a name: place of supply. It decides, for tax purposes, in which
country a transaction is treated as having happened. In the United Kingdom's
Value Added Tax Act 1994, Schedule 4A, paragraph 15(1), a supply to a person
who is not a relevant business person is "to be treated as made in the country
in which the recipient belongs" — and paragraph 15(2)(a) applies that to
"electronically supplied services", which is what a downloaded game is. HMRC's
own guidance says the same in plainer words: supplies of digital services to
consumers in the country are liable to that country's VAT, while supplies to
consumers outside it are not, and "may be liable to VAT in the country where
the consumer is based".

There is a second piece that surprises people, and it is in the same guidance:
"If you supply digital services to consumers via a third party platform or
marketplace, the digital platform is responsible for accounting for VAT on the
supply instead of you." On a store, the store answers for the tax — not the
developer whose logo is on the box art.

The number that decides is yours. Take what you actually paid, find the rate
your own country applies to digital goods on your own tax authority's page, and
if the price already included it, divide what you paid by one plus that rate as
a decimal. Subtract the result from what you paid: the difference is the tax,
and that part never reached the game.

That division matters because a price gap between two countries has at least
two causes — the applicable rate and a deliberate regional price — and until
you divide, they look like one. The video also lists five legitimate reasons the
picture is confusing: the displayed price usually hides the tax; comparing
countries also compares currencies; a country can apply more than one rate; the
legal seller is often the platform; and a discount changes the base, so the tax
amount falls while the share stays.

What this video does not do: it does not call the rate high, low, fair or
unfair; it does not say who wins between store and studio; and it does not tell
you to change your account region, which usually breaks the store's own terms.
And one real limit, stated plainly: I read and verified one jurisdiction's text,
and I name it. Two other official sources for this would not open for me, so I
assert nothing about any other country's wording — instead the video gives you
the exact question to ask about your own.

Chapters:
00:00 Part of the price never reaches the game
01:06 What the paragraph says
02:12 Now divide your own receipt
03:18 Why the store, not the studio
04:24 What people get wrong
05:30 What this does not mean
06:36 What I left out on purpose
07:42 Four steps

In the comments, post only the share of your price that turned out to be tax —
not your receipt, your account or what you bought.

## DISCLOSURE
The narration and visuals in this video were produced with artificial
intelligence. The rule described is quoted from the published text of the
legislation and from the tax authority's own guidance, both named above.

## HASHTAGS
#GameEconomics #VAT #DigitalGoods

## TAGS
vat on digital games, place of supply, schedule 4a paragraph 15, why game prices differ by country, digital services vat, marketplace accounts for vat, regional pricing games, tax in game price, how to calculate vat from total, value added tax act 1994, electronically supplied services, game price breakdown, steam price by country, digital goods taxation, consumer vat rules

## COMENTARIO FIXADO
Four steps: open the receipt for your last digital game → look up the rate your
country applies to digital goods on your own tax authority's page → divide what
you paid by one plus that rate as a decimal, then subtract → write the amount
paid and the tax side by side with the date. That difference never reached the
game. Post only the share, not the receipt.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/game-money-lab-010.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "game-money-lab",
    "pacote": "game-money-lab-010",
    "idioma": "en",
    "voz": "en-GB-RyanNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1A2430", "c1": "#A63D2F", "c2": "#1E6F6A", "bg": "#F4F2ED"},
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
    from ensaio import duracao_estimada, duracao_estimada_short, duracao_cena, GAP_CENA_S
    grava(SPEC, "fabrica/specs/game-money-lab-010.json")
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
        t += duracao_cena(c.get("nar", ""), SPEC["voz"]) + GAP_CENA_S
    if ult:
        print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s  (ultimo)")
