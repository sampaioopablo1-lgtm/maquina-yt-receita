#!/usr/bin/env python3
"""Monta a spec game-money-lab-008.

ALAVANCA ATACADA: **A — conversao short -> inscrito.** Quarto pacote do
experimento 26: o PEDIDO do short vira a inscricao.

NUMERO DE PARTIDA, medido em 31/08 e 01/09/2026:

    game-money-lab .... 7 pacotes, 188 views TOTAIS, ZERO inscritos
                        short: mediana 1,69 views/dia, topo 6,62
                        longo: mediana 0,04 views/dia
                        veredito: `canal frio`

POR QUE ESTE CANAL, APESAR DO APRENDIZADO 540. Ontem eu registrei este canal
como candidato a PAUSA, e o argumento continua de pe: o `game-money-lab-006`
("In-Game Currency") ja entregava a divisao FECHADA dentro do short — abra o
ultimo pacote de moedas, divida o preco pela quantidade, multiplique pelo item
— e teve CINCO views. Forma certa, alcance nulo.

Produzo assim mesmo por dois motivos, e os dois sao verificaveis. Primeiro:
neste horario ele e o UNICO canal liberado — dez estao no teto de um longo por
dia e dois estao com token morto. Nao produzir seria publicar zero. Segundo, e
mais importante: fui conferir o CTA do 006 e ele NAO pede inscricao — termina
em "run it on a purchase you already made". Ou seja, a variavel do experimento
26 nunca foi testada aqui tambem. Este pacote e o quarto braco dele, nao uma
repeticao.

O QUE DEU CERTO: o alcance deste canal nao e uniformemente cinco. O short do
GTA seis teve noventa e uma views com cinquenta e quatro virgula oito por cento
de retencao, e o dos trezentos milhoes teve cinquenta e duas com setenta e oito
virgula nove — a maior retencao do canal. Quando o assunto pega, ele pega.

O QUE NAO DEU: os longos. Sete de sete entre zero e duas views. E os quatro
mais antigos tem entre setecentos e setecentos e trinta e seis segundos,
dimensionados para o teto.

O QUE MUDO:
1. **EIXO NOVO** (regra do `canal frio`): sai a economia da industria — custo
   de producao, demissoes, preco do GTA, regra da UE, reembolso — e entra a
   biblioteca DELE. E o unico lugar deste nicho onde as tres condicoes do
   aprendizado 504 cabem juntas (aprendizado 534).
2. **O PEDIDO** (experimento 26): o short entrega a conta fechada E pede a
   inscricao, amarrada ao metodo. Nao aponta para o longo, e nao termina em
   "va fazer".

--------------------------------------------------------------- DIMENSIONAMENTO

`canal frio`: eixo novo e piso de **oito minutos**. Oito capitulos com ~64s NA
ESTIMATIVA, nunca 60 — o desvio por voz vai de menos um virgula nove a mais
quatro virgula nove por cento em sete vozes medidas, e capitulo desenhado no
limite some do `copy_md` quando a voz corre curta (aprendizado 537).

E a regra dos duzentos segundos vai ser conferida onde ela realmente se mede:
no `legendas.srt` do pacote renderizado, no timestamp do ultimo passo da conta.
A abertura do capitulo seguinte e um proxy que erra por quarenta e poucos
segundos, e me fez registrar tres pacotes como fora da regra quando os tres
estavam dentro.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO: **o custo por hora da ultima leva de promocao, com a biblioteca e as
horas jogadas dele**. Nunca usado neste canal, e ele usa o unico dado que todo
jogador tem a mao e ninguem olha somado: as horas que a propria loja conta.

AS TRES CONDICOES DO APRENDIZADO 504:
1. o dinheiro e DELE — o que ele pagou em cada jogo da ultima promocao;
2. e ESCOLHA COM PRAZO — a proxima promocao, que tem data;
3. o SHORT entrega a conta — a divisao fechada, e depois pede a inscricao.

FONTES: este video NAO faz nenhuma afirmacao institucional e NAO cita nenhum
numero meu. Nao cita preco de jogo, nao cita percentual de desconto, nao cita
nome de loja, de jogo nem de plataforma, e nao cita media de horas de ninguem.
Os dois numeros da conta estao os dois na conta dele, na mesma tela. Nao ha
numero meu para certificar em duas fontes, e por isso nao ha numero meu que
possa envelhecer nem que dependa da loja dele.

O QUE O VIDEO NAO FAZ: nao diz que promocao e boa ou ruim, nao recomenda loja
nem jogo, nao promete economia e nao e aconselhamento financeiro.
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


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================

# -------------------------------------------------------------------- cap 1
T("You bought on sale", "and never checked after",
  "You bought a handful of games in the last big sale. You felt good about it. "
  "And you have probably never gone back to check what that haul actually "
  "cost you.",
  cap="The haul you never checked")
I("Not about spending less", "about knowing",
  "This is not a video about spending less on games. It is about knowing what "
  "you got per pound spent, which is a different question and a more useful "
  "one.")
I("And it has a deadline", "the next sale",
  "It also has a deadline, and you know roughly when: the next sale. That is "
  "when this number would actually change something.")
I("Both numbers exist", "and both are yours",
  "Both numbers you need already exist, and both are yours. One is what you "
  "paid. The other your store has been counting for you the whole time.")
I("Nobody adds them up", "not even the store",
  "Nobody puts those two together for you. The store shows the discount, "
  "because the discount is what sells.")
I("Nothing to install", "nothing to track",
  "You do not need to install anything or start tracking anything. Both "
  "numbers are already sitting in your account.")
I("What is coming", "one division",
  "In a few minutes you will run this yourself. It is one division, done once "
  "per game, on a list you already have.")

# -------------------------------------------------------------------- cap 2
T("The two sides", "what you paid, what you played",
  "The calculation has two sides, and almost everyone only looks at the "
  "first one.",
  cap="What you paid, what you played")
I("Side one", "what you actually paid",
  "Side one is what you actually paid for each game. Not the original price, "
  "not the discount percentage. The amount that left your account.")
I("Ignore the percentage", "it is not a side",
  "Ignore the discount percentage entirely. It describes the shop, not you, "
  "and it is the number that makes people buy things they never open.")
I("Side two", "hours played",
  "Side two is the hours you have played each of those games. Your store "
  "counts this, and it has been counting since the day you installed them.")
I("Including the zeroes", "especially those",
  "Include the games with zero hours. Especially those. They are the whole "
  "reason this calculation is worth doing.")
I("Same window", "the same sale",
  "Use one sale, and all of it. Picking your favourite three from that haul "
  "proves nothing except that you can pick favourites.")
I("Now the sides match", "money against hours",
  "With money on one side and hours on the other, this stops being a feeling "
  "about a good deal and becomes arithmetic about your last one.")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA — os tres passos na PRIMEIRA METADE do capitulo.
T("The math", "one division",
  "So here is the math. One division per game, then one for the haul.",
  cap="The math: one division")
I("Step one", "price divided by hours",
  "Step one: for each game, divide what you paid by the hours you have "
  "played. That is your cost per hour on that game.")
I("Step two", "add the haul up",
  "Step two: add up everything you paid in that sale, and add up all the "
  "hours across those games.")
I("Step three", "divide the totals",
  "Step three: divide the total paid by the total hours. That single number is "
  "what the whole haul cost you per hour played.")
I("That is the answer", "in your currency",
  "That is the answer, and it is in money per hour. Not a percentage, and not "
  "an opinion about whether you overspent.")
I("Now compare", "against one full-price game",
  "Now compare it against one game you paid full price for and loved. Run the "
  "same division on that one, and put the two numbers side by side.")
I("The comparison decides", "not the discount",
  "That comparison is what tells you whether the sale served you. The "
  "discount percentage never could.")
I("Math ends here", "the rest is why",
  "The math ends here and you can run yours now. The rest of this video is "
  "where the numbers hide, what the division misses, and when it lies.")

# ================== DEPOIS DA RESPOSTA — POR QUE CONTINUAR ===================

# -------------------------------------------------------------------- cap 4
T("Where the numbers are", "already in your account",
  "Now where to find those numbers, because most people have never opened "
  "these two screens.",
  cap="Where the numbers are")
I("Purchase history", "the amount paid",
  "Your account has a purchase history with the amount actually charged. That "
  "is side one, already itemised.")
I("Not the wishlist price", "the charged price",
  "Use the charged amount, not the price you remember or the one still shown "
  "on the page. Those two drift apart constantly.")
I("Playtime", "on the library page",
  "Playtime sits on the library page next to each title. You do not have to "
  "estimate anything.")
I("Round the small ones", "to the nearest hour",
  "Round short playtimes to the nearest hour, and let anything under an hour "
  "be zero. Precision there changes nothing and costs time.")
I("Bundles", "split by the number of games",
  "If part of the haul was a bundle, split what you paid evenly across the "
  "games in it. It is rough, and it is honest enough for this.")
I("Gift cards and credit", "still count",
  "Money that came from a gift card or store credit still counts. It was "
  "money, and something was given up to get it.")
I("Refunded ones come out", "of both sides",
  "Anything you refunded comes out of both sides — the money and the hours. "
  "It never happened, for this purpose.")
I("Twenty minutes", "for a whole haul",
  "For a normal haul this is about twenty minutes of work, most of it "
  "scrolling. There is nothing to calculate until the end.")

# -------------------------------------------------------------------- cap 5
T("What it misses", "and it is fair to say",
  "There are things this division does not capture, and naming them is more "
  "honest than pretending it settles the question.",
  cap="What the division misses")
I("A game you will play later", "is not a failure yet",
  "The first: a game you have not started is not necessarily wasted. Some of "
  "them wait a year and then get played properly.")
I("But test that honestly", "look at last year",
  "Test that claim against your own history, though. Look at the sale before "
  "last: how many of those did you eventually play?")
I("The second", "short games score badly",
  "The second: a short game scores badly here by design. Ten superb hours "
  "will always lose to two hundred mediocre ones on this metric.")
I("So do not rank by it", "read it as a total",
  "So do not use this to rank individual games. Read the haul number, and use "
  "the per-game ones only to see where the money went.")
I("The third", "hours are not enjoyment",
  "The third: hours are not enjoyment. A game you played out of stubbornness "
  "counts the same as one you loved, and only you know which is which.")
I("The fourth", "a refund window closed",
  "And a smaller fourth: a game you bought and bounced off within the refund "
  "window is a different mistake from one you kept. Worth separating.")
I("Add that after", "never before",
  "Bring all of this in AFTER the division, never before. Raised first, they "
  "become reasons not to look at the number at all.")

# -------------------------------------------------------------------- cap 6
T("When it lies", "the one big game",
  "Now the case that fools almost everyone.",
  cap="When the number lies")
I("One game carries the haul", "and hides the rest",
  "Usually one game in the haul has most of the hours. It drags the average "
  "down and makes the whole purchase look sensible.")
I("So run it twice", "with and without",
  "So run the haul number twice: once with that game, once without it. The "
  "gap between the two is the real finding.")
I("If the gap is huge", "you bought one game",
  "If the gap is large, what you actually did was buy one game and collect "
  "the rest. That is fine, and it is worth knowing.")
I("The reverse also happens", "spread evenly",
  "The reverse happens too: a haul where the hours are spread across most of "
  "the titles. That is a sale that genuinely worked for you.")
I("And a first sale", "is not typical",
  "A first sale after a long gap is not typical either. There was a backlog "
  "waiting, and the next one will not look like it.")
I("Both outcomes are valid", "your number decides",
  "Buying on sale and paying full price are both defensible, and neither is "
  "right in general. The right one is whatever your number points to. The only "
  "wrong move is buying on the percentage and never looking again.")

# -------------------------------------------------------------------- cap 7
T("From one sale", "to the year",
  "Now the step that makes the size of this real.",
  cap="From one sale to the year")
I("One sale", "looks small",
  "One sale usually looks small on its own. It is small, and that is exactly "
  "why it repeats without ever being examined.")
I("Multiply", "by the sales you buy in",
  "Multiply by how many sales you buy in during a year. Most calendars have "
  "several, and most people buy in most of them.")
I("Then look forward", "the next one has a date",
  "Then look forward, because the next one already has a date, and the same "
  "behaviour will produce the same result.")
I("Compare it", "with one full-price game",
  "To feel the size, compare the year's total against the price of one game "
  "at full price. If a year of hauls buys three games you never opened, that "
  "says one thing. If it buys hundreds of played hours, it says another.")
I("It might be fine", "that is an answer too",
  "It might come out fine, and nothing needs to change. That is a complete "
  "answer, and now it is measured instead of assumed.")
I("And the list gets shorter", "on its own",
  "There is a second effect worth noticing: people who run this once tend to "
  "buy fewer titles in the next sale without deciding to. The number does the "
  "work.")
I("The good part", "the next sale is a fresh decision",
  "The good part is that the next sale is a fresh decision, and it arrives "
  "whole. One bad haul does not commit the next one.")

# -------------------------------------------------------------------- cap 8
T("What to do today", "three steps",
  "We will close with what you can do today, in three steps.",
  cap="What to do today")
L("Three steps",
  ["Open the last sale's receipts", "Write the hours next to each",
   "Divide the totals"],
  "First: open the purchase history for the last sale. Second: write the "
  "playtime next to each game, zeroes included. Third: divide total paid by "
  "total hours.")
I("Then run it once more", "on a full-price game",
  "Then run the same division on one full-price game you loved, so the "
  "number has something to sit against.")
I("Do not change your habits yet", "just know the number",
  "You do not have to change anything today. Knowing the number is the whole "
  "step, and it is enough.")
I("And keep it somewhere", "for the next sale",
  "Keep it somewhere you will find again. When the next sale starts, that "
  "number is the only thing standing between you and the percentage.")
# EXPERIMENTO 26 — o pedido do longo tambem fecha em conta.
I("One line is enough", "not a spreadsheet",
  "One line per game on a piece of paper is enough. This is not a spreadsheet "
  "you maintain, it is a number you get once and keep.")
C("Post your number", "in the comments",
  "If you run it, post one thing below: your cost per hour for the haul. No "
  "game names, no spend totals, just the number. I want to see how far these "
  "spread between people who bought in the same sale.")

# =============================== O SHORT =====================================
# EXPERIMENTO 26, quarto pacote. Entrega a divisao FECHADA e gasta o pedido na
# INSCRICAO. O short do 006 entregava a conta mas terminava em "va fazer" —
# nunca pediu inscricao, e converteu zero.

SHORT = [
    {"layout": "titulo", "kicker": "Your last sale haul",
     "sub": "what did it cost per hour?",
     "nar": "That pile of games from the last sale. What did it cost you per "
            "hour played?", "sem_cap": True},
    {"layout": "titulo", "kicker": "Number one", "sub": "what you paid",
     "nar": "Number one: the total you paid in that sale. From the purchase "
            "history, not the discount percentage.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Number two", "sub": "hours played",
     "nar": "Number two: the hours played across those games, from your "
            "library page. Include every zero.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Divide", "sub": "that is your answer",
     "nar": "Divide the money by the hours. That is what the haul cost you "
            "per hour. Run it on one full-price game you loved and compare "
            "the two.", "sem_cap": True},
    {"layout": "cta", "kicker": "If that was useful",
     "sub": "subscribe — one a week",
     "nar": "If that was useful, subscribe. One gaming money calculation a "
            "week, run on your own account.", "sem_cap": True},
]

THUMB = {"l1": "Sale haul", "l2": "per hour"}

COPY = """# What your last sale haul cost per hour played, from your own account

## TITULO
Sale Haul or Full Price? Divide by the Hours You Actually Played

## DESCRICAO
You bought a handful of games in the last big sale, you felt good about it, and you have probably never gone back to check what that haul actually cost you. This is not a video about spending less on games — it is about knowing what you got per pound spent, which is a different question and a more useful one. And it has a deadline you already know: the next sale.

There is not a single number of mine in this video. No game price, no discount percentage, no store, platform or title named, and no average playtime for anybody. Both numbers in the calculation are yours, and both are already sitting in your account.

The math is one division. For each game in that haul, divide what you actually paid — the amount charged, not the original price and never the discount percentage — by the hours you have played it. Then add up everything you paid in that sale, add up all the hours across those games, and divide the totals. That single number is what the whole haul cost you per hour played. Include the games with zero hours; they are the entire reason this is worth doing.

Then compare it against one game you paid full price for and loved, run through the same division. That comparison is what tells you whether the sale served you. The discount percentage never could.

One chapter covers where the numbers are: the purchase history has the amount actually charged, and playtime sits on the library page next to each title, so nothing has to be estimated. Bundles get split evenly across the games in them, and money that came from a gift card still counts.

One chapter covers what the division misses, because naming it is more honest: a game you have not started is not necessarily wasted, though it is worth testing that claim against the sale before last; a short game scores badly here by design, so read the haul number rather than ranking individual games; and hours are not enjoyment — a game played out of stubbornness counts the same as one you loved.

And one chapter covers when the number lies. Usually one game carries most of the hours and drags the average down, making the whole purchase look sensible. Run the haul number twice, with and without that game. The gap between the two is the real finding.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Run it and post one thing below: your cost per hour for the last haul. No game names, no spend totals, just the number. I want to see how far these spread between people who bought in the same sale.

## HASHTAGS
#Gaming #PersonalFinance #GameMoneyLab

## TAGS
game sale worth it, cost per hour gaming, steam sale math, backlog problem, unplayed games, gaming budget, price per hour played, library playtime, buying games on sale, full price vs sale, game spending, gaming finance, run the numbers, purchase history, discount trap

## CONFIGURACOES DO STUDIO
- Idioma: Ingles (en) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Reino Unido | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita preco de jogo, nao cita percentual de desconto, nao cita nome de loja, de plataforma nem de titulo, nao cita media de horas de ninguem e nao compara lojas entre si. Os dois numeros da conta sao do proprio espectador e os dois estao na conta dele: o valor cobrado esta no historico de compras, e as horas jogadas estao na pagina da biblioteca. Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa da regiao, da loja ou do catalogo dele. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA: qualquer preco de jogo ou percentual de desconto. Esses valores mudam por regiao, por promocao e por data, e citar um so deles tornaria a conta errada para a maioria de quem assiste. O video tambem nao diz que comprar em promocao e bom ou ruim — as duas respostas sao legitimas e dependem do numero de cada um —, nao recomenda loja nem jogo, nao promete economia e nao e aconselhamento financeiro.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/game-money-lab-008.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "game-money-lab",
    "pacote": "game-money-lab-008",
    "idioma": "en",
    "voz": "en-GB-RyanNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#181C2A", "c1": "#EF476F", "c2": "#22D3EE", "bg": "#F4F4F8"},
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
    from ensaio import duracao_estimada, duracao_estimada_short
    grava(SPEC, "fabrica/specs/game-money-lab-008.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
