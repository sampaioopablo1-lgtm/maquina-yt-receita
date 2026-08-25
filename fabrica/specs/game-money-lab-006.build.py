#!/usr/bin/env python3
"""Monta a spec game-money-lab-006.

ALAVANCA ATACADA: **A — conversao short -> inscrito**. Numero de partida:
**0,00%**. Quatro shorts, 170 views somadas, zero inscritos. Oito videos no
canal, 171 views, zero inscritos.

O QUE DEU CERTO, e este canal separa os dois grupos com uma nitidez rara:

    91 views  12,22 v/d  54,8% ret  "GTA 6 Costs $80: The 20-Year Price
                                     Freeze That Broke Gaming"
    52 views   4,11 v/d  78,9% ret  "$300 Million Per Game"
    21 views   4,08 v/d  35,4% ret  "Gaming Layoffs 2026: Forecast Revised
                                     Up 78%"
     6 views   1,30 v/d  27,4% ret  "1,294,188 Signatures: Why the EU Chose
                                     a Code of Conduct"

Os dois de cima sao PRECOS que o espectador reconhece — o que ele paga por um
jogo, o que custa fazer um jogo. Os dois de baixo sao noticia de industria:
previsao de demissoes e peticao. E o 002 tem 78,9% de retencao, a maior da
frota inteira.

O QUE NAO DEU: o longo, completamente. Quatro longos, UMA view somada.
Veredito `canal frio`.

O QUE VOU MUDAR: eixo novo (o `canal frio` manda), na forma que mediu melhor —
preco — mas dando o passo que faltava. Os dois shorts que funcionaram falam do
preco DE ALGUEM: os oitenta dolares do GTA 6, os trezentos milhoes do estudio.
Nenhum deles faz o espectador calcular o PROPRIO. Pelo aprendizado 487, e
justamente isso que separa view de inscrito.

--------------------------------------------------------------------- A PAUTA

Eixo: **moeda virtual dentro do jogo, e o preco real que ela esconde**. Nunca
usado. Os publicados cobrem orcamento de AAA, preco do GTA 6, demissoes e
preservacao de jogos.

E e o unico assunto deste nicho em que o numero de partida esta na conta do
proprio espectador: a ultima compra de moeda que ele fez.

FONTES INSTITUCIONAIS, duas independentes que se confirmam:

  1. COMISSAO EUROPEIA (commission.europa.eu e o presscorner):
       Key Principles on In-Game Virtual Currencies .... adotados pela rede
           CPC em MARCO DE 2025, sob lideranca da ACM holandesa e da
           autoridade do consumidor da Noruega.
       o que sao moedas virtuais ...... representacoes digitais de valor
           compradas com dinheiro real e depois usadas para pagar por
           conteudo ou servico digital dentro do jogo.
       o que os principios exigem ..... preco claro e transparente e
           informacao pre-contratual; NAO obscurecer o custo do conteudo;
           NAO obrigar o consumidor a comprar moeda virtual; e o preco
           indicado em DINHEIRO DO MUNDO REAL, porque preco e informacao
           material.
       acao de fiscalizacao (IP/25/831) ... a rede CPC, liderada pela agencia
           sueca e pela norueguesa, acionou a Star Stable Entertainment AB.
           Entre os pontos: exortar criancas a comprar, o que nao e
           permitido; relogios de contagem regressiva pressionando decisao;
           e precos NAO apresentados em moeda do mundo real.
       junho de 2025 .................. a Comissao reuniu as partes
           interessadas para discutir a aplicacao dos principios.

  2. ACM — AUTORIDADE DOS PAISES BAIXOS PARA CONSUMIDORES E MERCADOS
     (acm.nl), co-lider dos principios, em publicacao propria: o uso de
     moedas virtuais dentro de jogos precisa ficar mais claro para proteger
     o consumidor.

A CONTA, na segunda pessoa, com o numero que so o espectador tem:
  1. pegue o ultimo pacote de moeda que voce comprou: quanto pagou, e quantas
     moedas recebeu;
  2. divida o dinheiro pelas moedas — esse e o valor de UMA moeda;
  3. multiplique pelo preco em moedas do item que voce queria — esse e o
     preco real dele, em dinheiro;
  4. e veja quantas moedas sobraram sem poder virar nada.

O CUIDADO QUE O VIDEO TOMA: o exemplo numerico e declaradamente EXEMPLO, com
numeros redondos, e nao afirma preco de jogo nenhum. Os unicos numeros tratados
como fato sao os das duas fontes: a data dos principios e o teor da acao.

O QUE O VIDEO NAO FAZ: nao acusa nenhuma empresa alem da que consta na acao
publica da propria Comissao, nao diz que moeda virtual e ilegal (nao e), e nao
da conselho juridico.
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


def I(kicker, preco, nar):
    CENAS.append({"layout": "item", "kicker": kicker, "preco": preco,
                  "nar": nar, "sem_cap": True})


def L(kicker, itens, nar):
    CENAS.append({"layout": "lista", "kicker": kicker, "itens": itens,
                  "nar": nar, "sem_cap": True})


def B(kicker, itens, alturas, nar):
    CENAS.append({"layout": "barras", "kicker": kicker, "itens": itens,
                  "alturas": alturas, "nar": nar, "sem_cap": True})


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ============================ OS PRIMEIROS 200 SEGUNDOS ======================
# As duas divisoes que revelam o preco real saem nos capitulos 1 a 3.

# ------------------------------------------------------------------- cap 1
T("A camada no meio", "voce nao paga em dinheiro",
  "When you buy something inside a game, you almost never pay in money. You "
  "pay in coins, gems, or points that you bought earlier with money.",
  cap="The layer between you and the price")
I("Why that matters", "the price stops being a price",
  "That extra layer does something specific: it stops the number on the item "
  "from being a price you can compare with anything else in your life.")
I("A concrete symptom", "you cannot say it out loud",
  "Here is the test. Think of the last thing you bought inside a game, and "
  "try to say what it cost in your own currency. Most people cannot.")
I("That is not you", "the design does that",
  "That is not carelessness on your part. The currency layer is doing exactly "
  "what it was built to do.")
I("And regulators noticed", "not a fringe complaint",
  "This is not a fringe complaint either. European consumer authorities "
  "published a common position on it, and I will come back to that.")
I("It is not a new trick", "arcades did it first",
  "The idea is old, by the way. Arcades ran on tokens for the same reason, "
  "and nobody pretended otherwise.")
I("What changed", "the rate is now invisible",
  "What changed is the rate. At the arcade the exchange was printed on the "
  "machine. In a store with a dozen bundle sizes, it is not printed anywhere.")
I("What you get here", "two divisions",
  "But first, the useful part: two divisions that turn coins back into money, "
  "using only numbers you already have.")

# ------------------------------------------------------------------- cap 2
T("Step one", "what one coin costs you",
  "First step, and you can do it from your purchase history right now.",
  cap="Step one: what one coin costs")
I("Take your last pack", "two numbers",
  "Open the last currency pack you bought. Write down two numbers: what you "
  "paid, and how many coins you received.")
I("Divide", "money by coins",
  "Divide the money by the coins. That gives you what a single coin cost "
  "you.")
I("Worked example", "and it is only an example",
  "An example with round numbers, and it is only an example. Say you paid ten "
  "and received one thousand coins. Then a single coin cost you one cent.")
I("Keep that number", "it unlocks everything else",
  "Keep that number somewhere. It is the exchange rate between the game and "
  "your bank account, and nothing in the store will show it to you.")
I("It changes per pack", "bigger packs, different rate",
  "And check it per pack, because larger packs usually carry a different "
  "rate. The coin is not worth the same in every bundle.")
I("Where to find it", "your receipts",
  "If you cannot remember the pack, the platform keeps a purchase history. "
  "Both numbers are in there, on the same line.")
I("Do it for the pack you buy most", "not the biggest one",
  "And do it for the pack you actually buy most often, not the largest one on "
  "the page. The largest is rarely the one people pick.")
I("That alone", "already changes shopping",
  "That single number already changes how the store looks, before you buy "
  "anything else.")

# ------------------------------------------------------------------- cap 3
T("Step two", "price the thing you wanted",
  "Second step, and this is the one that surprises people.",
  cap="Step two: price what you wanted")
I("Take the item", "its price in coins",
  "Take the item you actually wanted and look at its price in coins.")
I("Multiply", "coins times coin cost",
  "Multiply that by what one coin cost you. The result is the real price of "
  "the item, in money.")
I("Same example", "eight hundred coins",
  "In the same example, an item at eight hundred coins costs you eight units "
  "of your currency. Not eight hundred of anything, which is roughly how the "
  "number feels while you are looking at it in the store.")
I("Do it before you buy", "not after",
  "The order matters here. Do this before the purchase, because afterwards "
  "the coins are already gone and the number stops being a decision.")
I("It works on bundles too", "split the coin price",
  "It works on bundles as well. Take the total coin price, convert it, and "
  "then judge the bundle against what you would pay outside.")
I("Now compare", "to something outside the game",
  "Now compare that to something outside the game that costs the same. That "
  "comparison is the one the coin layer was preventing.")
I("That is the method", "two divisions and a multiplication",
  "That is the whole method: divide to get the coin cost, multiply to get "
  "the item cost. Everything after this is why it works the way it does.")

# ============ ate aqui, ~200 segundos. O que segue aprofunda. ===============

# ------------------------------------------------------------------- cap 4
T("The leftover", "and why it is always there",
  "Now the part people notice but rarely name: the coins left over.",
  cap="Why there is always a leftover")
I("Pack sizes and item prices", "they do not line up",
  "Currency packs are sold in one set of sizes, and items are priced in "
  "another. The two sets rarely line up.")
I("The result", "you end just short",
  "So you routinely end up just short of the next item, holding coins that "
  "cannot become anything on their own.")
I("What that does", "it pulls the next purchase",
  "Those stranded coins do work for the store. They make the next pack feel "
  "smaller than it is, because you are only topping up.")
I("Run your own numbers", "count the leftover",
  "So add a third step to your own check: after you buy, count how many "
  "coins are stranded, and price them with your coin cost.")
I("That number is real", "you paid for it",
  "That amount is money you have already paid and not yet received anything "
  "for. It belongs in your calculation.")
I("An easy check", "does any pack match any item",
  "Here is a quick way to see it. Look at the pack sizes and the item prices "
  "side by side, and ask whether any pack lands exactly on any item.")
I("Usually none does", "and that is the point",
  "Usually none of them does. That is not a coincidence you have to prove; "
  "it is something you can observe in about ten seconds.")
I("Not an accusation", "just arithmetic",
  "None of this says anyone broke a rule. It says the arithmetic is worth "
  "doing, and the store will not do it for you.")

# ------------------------------------------------------------------- cap 5
T("What Europe decided", "March of last year",
  "Here is where the regulators come in, and what they actually said.",
  cap="What Europe decided")
I("The document", "Key Principles",
  "In March of two thousand and twenty five, the European consumer protection "
  "network adopted a set of Key Principles on in game virtual currencies.")
I("Who led it", "two national authorities",
  "They were prepared under the lead of the Dutch consumer authority and the "
  "Norwegian consumer authority, and coordinated by the European Commission.")
I("What a virtual currency is", "their definition",
  "Their definition is precise: a digital representation of value, bought "
  "with real money, then used to pay for digital content or services inside "
  "a game.")
I("The core requirement", "price in real money",
  "And the core requirement is the one you have been doing by hand: consumers "
  "should be able to understand the true cost, with the price indicated in "
  "real world money.")
I("Two more", "no hiding, no forcing",
  "Two more principles matter here: traders should not hide the cost of in "
  "game content, and should not oblige consumers to buy virtual currency at "
  "all.")
I("Why this document exists", "the layer was the problem",
  "Notice what the document is aimed at. Not the existence of virtual money, "
  "but the fact that the layer made the real price hard to see.")
I("Status", "principles, then monitoring",
  "These are principles for the industry to adapt to, with the network "
  "monitoring progress and enforcement possible if harmful practices "
  "continue.")

# ------------------------------------------------------------------- cap 6
T("One case", "how it looks in practice",
  "And there is a public case that shows what those words mean in a real "
  "game.",
  cap="How it looks in a real case")
I("The action", "a coordinated request",
  "The same network, led by the Swedish and Norwegian authorities, opened a "
  "coordinated action about a game aimed at children.")
I("First point", "urging children to buy",
  "One of the points raised was that players were being urged to make "
  "purchases, which is not allowed when the game appeals to children.")
I("Second point", "countdown timers",
  "Another was countdown timers used to push players into deciding quickly.")
I("Third point", "prices not in real money",
  "And the third is the one from your own arithmetic: prices of items not "
  "presented in real world currency.")
I("What happens next", "respond, or enforcement",
  "The company was given time to respond and to propose remedies. If that "
  "is not enough, national authorities can act individually.")
I("Why a game for children", "the bar is higher there",
  "The case involves a game aimed at children, and that matters legally: "
  "practices that are merely aggressive elsewhere are simply not allowed when "
  "the audience is children.")
I("The pattern is general", "even if the case is one",
  "But the third point applies to every store, not just that one. Showing a "
  "price only in coins is the same mechanic wherever it appears.")
I("Why I mention it", "it names the mechanic",
  "I mention this because it names the mechanic in an official document, "
  "instead of leaving it as a feeling players have.")

# ------------------------------------------------------------------- cap 7
T("Where this comes from", "two sources",
  "Where all of this comes from, because that question is always fair.",
  cap="Where this comes from")
I("First source", "the European Commission",
  "The principles, their date, the definition, and the enforcement action all "
  "come from the European Commission, in its own published material.")
I("Second source", "the Dutch authority",
  "The Dutch consumer authority, which co led the work, published its own "
  "statement saying the use of in game virtual currencies must become "
  "clearer.")
I("What I did not do", "no prices claimed",
  "What I did not do is claim the price of any specific game, pack or item. "
  "My example uses round numbers, and I said so out loud while using them, "
  "because a made up number quoted confidently is still a made up number.")
I("Where you can read it", "both are public",
  "Both are public documents. The principles and the action are on the "
  "Commission site, and the statement is on the Dutch authority site.")
I("Check me on it", "that is the point of citing",
  "Check them if you want. Citing a source only means something when the "
  "source can be opened by the person listening.")
I("Why that line matters", "your numbers are the real ones",
  "That line matters because the numbers that count here are yours, not mine. "
  "Mine only show the shape of the calculation.")

# ------------------------------------------------------------------- cap 8
T("Before your next purchase", "three lines",
  "Three lines to write before the next time you buy currency in a game.",
  cap="Before your next purchase")
I("First", "your coin cost",
  "What one coin costs you, from your last pack: money divided by coins.")
I("Second", "the real price of the item",
  "The real price of the item you want: its coin price multiplied by that "
  "number.")
L("Third", ["What one coin costs me",
            "What the item really costs",
            "What my stranded coins are worth"],
  "And what your stranded coins are worth, using the same rate.")
I("Why the third", "it is the invisible one",
  "The third line is the one nobody writes, and it is usually the one that "
  "changes the decision.")
I("Then decide", "with the number visible",
  "Then decide normally. The point is not to stop buying. The point is to "
  "decide with the number visible.")
I("One habit", "check the rate per pack",
  "And one habit worth keeping: when a store changes its bundle sizes, redo "
  "the first division. The rate moves when the sizes move.")
I("Recap", "divide, multiply, count",
  "So: divide to find your coin cost, multiply to price the item, and count "
  "what is stranded.")
C("Game Money Lab", "run it on your last purchase",
  "Do it once, on the last purchase you already made. Here we take one number "
  "from your own account and turn it into a calculation you run yourself. If "
  "that is what you are here for, subscribe.")


# -------------------------------------------------------------------- short
#
# A divisao inteira, na segunda pessoa, com o numero que so o espectador tem:
# a ultima compra dele. Aprendizado 487.
SHORT = [
    {"layout": "titulo", "kicker": "You do not pay in money", "sub": "you pay in coins",
     "nar": "Inside a game you never pay in money. You pay in coins you "
            "bought earlier, and that hides the price.", "sem_cap": True},
    {"layout": "item", "kicker": "Open your last pack", "preco": "two numbers",
     "nar": "Open the last currency pack you bought. What you paid, and how "
            "many coins you got.", "sem_cap": True},
    {"layout": "item", "kicker": "Divide", "preco": "money by coins",
     "nar": "Divide one by the other. That is what a single coin costs you, "
            "and no store will show it.", "sem_cap": True},
    {"layout": "item", "kicker": "Then multiply", "preco": "by the item price",
     "nar": "Multiply that by the item price in coins. Now you know what it "
            "really costs.", "sem_cap": True},
    {"layout": "cta", "kicker": "Game Money Lab", "sub": "run it once",
     "nar": "Run it on a purchase you already made.", "sem_cap": True},
]

COPY = """# In-game currency: the two divisions that turn coins back into money

## TITULO
In-Game Currency: Two Divisions That Show What You Actually Paid

## DESCRICAO
When you buy something inside a game, you almost never pay in money. You pay in coins, gems or points that you bought earlier with money — and that extra layer does something specific: it stops the number on the item from being a price you can compare with anything else in your life. Here is the test: think of the last thing you bought inside a game and try to say what it cost in your own currency. Most people cannot. That is not carelessness on your part; the currency layer is doing what it was built to do. This video shows two divisions that turn coins back into money, using only numbers already in your purchase history.

THE METHOD (two steps, plus one nobody does)

1) Open the last currency pack you bought and write down two numbers: what you paid, and how many coins you received. Divide the money by the coins — that is what a single coin cost you. Check it per pack, because larger bundles usually carry a different rate. 2) Take the item you actually wanted, look at its price in coins, and multiply by that number. The result is its real price, in money. 3) The step nobody takes: after buying, count how many coins are stranded — too few to become anything — and price them at the same rate. That is money already paid for which you have received nothing yet.

Worked example, with round numbers and nothing more: pay 10 and receive 1,000 coins, and one coin cost you 1 cent; an item at 800 coins then costs you 8. Not 800 of anything.

WHY THE LEFTOVER IS ALWAYS THERE: currency packs are sold in one set of sizes and items are priced in another, and the two rarely line up. So you routinely end up just short of the next item. Those stranded coins make the next pack feel smaller than it is, because you are only topping up.

WHAT EUROPE DECIDED (source: European Commission)

In March 2025 the EU Consumer Protection Cooperation (CPC) Network adopted Key Principles on In-Game Virtual Currencies, prepared under the lead of the Netherlands Authority for Consumers and Markets (ACM) and the Norwegian Consumer Authority, coordinated by the European Commission. Their definition is precise: virtual currencies are digital representations of value purchased with real-world money and then used to pay for in-game digital content or services. The core requirement is the one you have just been doing by hand — consumers should be able to understand the true cost, with the price indicated in real-world money, because price information is material information. Two further principles: traders should not hide the cost of in-game content, and should not oblige consumers to purchase virtual currency. The network monitors progress and may consider enforcement if harmful practices continue.

A PUBLIC CASE: the same network, led by the Swedish and Norwegian authorities, opened a coordinated action concerning a game aimed at children. The points raised included players being urged to make purchases (not allowed when the game appeals to children), countdown timers pressuring quick decisions, and item prices not presented in real-world currency. The company was given time to respond and propose remedies; if that is insufficient, national authorities can act individually.

This video does not claim the price of any specific game or currency pack — the worked example uses round numbers and says so. It does not say virtual currencies are illegal (they are not), and it is not legal advice.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Run the first division on a purchase you already made and post one number: what a single coin cost you. Not the game, not the pack — just the rate. I want to see how far apart the rates are across different games and bundle sizes, because that spread is the whole point.

## HASHTAGS
#GameMoneyLab #InGameCurrency #GamingEconomics

## TAGS
in-game currency, virtual currency, microtransactions, game economics, cpc network, european commission, consumer protection, real money price, currency packs, gaming costs, premium currency, acm netherlands, key principles, game store, spending calculator

## CONFIGURACOES DO STUDIO
- Idioma: Ingles (en) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Reino Unido | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
As afirmacoes vem de DUAS fontes institucionais independentes que se confirmam. (1) COMISSAO EUROPEIA (commission.europa.eu e o presscorner): os Key Principles on In-Game Virtual Currencies foram adotados pela rede de Cooperacao para a Protecao do Consumidor (CPC) em MARCO DE 2025, preparados sob lideranca da Autoridade dos Paises Baixos para Consumidores e Mercados (ACM) e da autoridade do consumidor da Noruega, com coordenacao da Comissao; a definicao adotada e "representacoes digitais de valor compradas com dinheiro do mundo real e depois usadas para pagar por conteudo ou servico digital dentro do jogo"; as exigencias centrais sao preco claro e transparente com informacao pre-contratual, o preco indicado em dinheiro do mundo real porque informacao de preco e informacao material, a proibicao de praticas que obscurecam o custo, e a proibicao de obrigar o consumidor a comprar moeda virtual; a rede monitora o progresso e pode considerar medidas de fiscalizacao. Em junho de 2025 a Comissao reuniu as partes interessadas para discutir a aplicacao desses principios. A ACAO DE FISCALIZACAO citada e publica (IP/25/831): a rede CPC, liderada pela agencia sueca e pela norueguesa, acionou a Star Stable Entertainment AB por praticas num jogo dirigido a criancas, entre elas exortar criancas a comprar (nao permitido), relogios de contagem regressiva pressionando decisoes rapidas, e precos de itens NAO apresentados em moeda do mundo real; a empresa recebeu prazo para responder e propor compromissos. (2) ACM (acm.nl), co-lider dos principios, em publicacao propria: o uso de moedas virtuais dentro de jogos precisa ficar mais claro para proteger o consumidor. O EXEMPLO NUMERICO DO VIDEO E DECLARADAMENTE EXEMPLO, com numeros redondos, e o roteiro diz isso em voz alta enquanto o usa: nenhum preco de jogo, pacote ou item foi afirmado como fato, porque os numeros que valem aqui sao os do proprio espectador. O video nao afirma que moeda virtual e ilegal, nao acusa empresa alguma alem da que consta na acao publica da propria Comissao, e nao e aconselhamento juridico.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/game-money-lab-006.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "game-money-lab",
    "pacote": "game-money-lab-006",
    "idioma": "en",
    "voz": "en-GB-RyanNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#181C2A", "c1": "#7C3AED", "c2": "#22D3EE",
               "bg": "#F4F4F8"},
    "thumb": {"l1": "What one coin", "l2": "costs you"},
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
    from ensaio import duracao_estimada, duracao_estimada_short
    grava(SPEC, "fabrica/specs/game-money-lab-006.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
