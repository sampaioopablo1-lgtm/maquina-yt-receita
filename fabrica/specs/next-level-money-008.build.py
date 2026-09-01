#!/usr/bin/env python3
"""Monta a spec next-level-money-008.

ALAVANCA ATACADA: **A — conversao short -> inscrito.** E esta rodada carrega o
experimento 26, aberto ontem: o PEDIDO do short vira a inscricao.

NUMERO DE PARTIDA, medido em 31/08 e 01/09/2026:

    next-level-money ... 11 pacotes, 128 views TOTAIS, ZERO inscritos
                         short: mediana 0,81 views/dia, topo 4,42
                         longo: mediana 0,06 views/dia
                         veredito: `canal frio`

O QUE DEU CERTO — e e a unica coisa: a RETENCAO de dois shorts. "Three
Companies Hold a File on You" segurou noventa e quatro virgula um por cento, e
o da Companhia das Indias Orientais segurou sessenta e tres virgula nove. Quem
chega assiste. O problema deste canal nao e o espectador desistir.

O QUE NAO DEU: os longos. Onze pacotes, e TODOS os longos entre zero e uma
view. Nao um, nao a maioria: todos. E os quatro mais antigos tem entre
setecentos e vinte e oito e setecentos e noventa e tres segundos, dimensionados
para o teto quando a alavanca B ja mandava o piso.

E os titulos dizem o porque: um virgula vinte e seis trilhoes de divida no
cartao, doze virgula oito por cento de inadimplencia, dezesseis por cento dos
adultos no parcelamento, sete virgula nove trilhoes da Companhia das Indias
Orientais, os bureaus de credito. Sao numeros GRANDES sobre o mundo. Nenhum
deles e uma conta que o espectador faca em si mesmo. A unica excecao,
"One Balance, Two Kinds of Money", e sobre vesting — conta dele — e teve vinte
views no short e ZERO no longo.

O QUE MUDO POR CAUSA DISSO, e sao duas coisas:

1. **EIXO NOVO** (regra do `canal frio`): sai o numero grande sobre o sistema,
   entra a conta no extrato dele. Zero numero meu — nao ha taxa, nao ha
   percentual de cashback, nao ha nome de banco nem de cartao.

2. **O PEDIDO** (experimento 26, aberto em `resep-naik-level-009`): o short
   entrega a conta fechada E pede a inscricao, amarrada ao metodo. Nao aponta
   para o longo. A razao esta medida: dois shorts da frota com cerca de mil
   views cada — `labtreinamento-006` e `resep-naik-level-008` — deram ZERO
   inscritos, um segurando a conta e o outro entregando. Os dois gastaram o
   unico pedido num clique para o video completo, e o completo ficou com zero
   view. Em canal sem inscrito, o longo nao e o ativo; a inscricao e.
   (Aprendizado 539, corrigido ontem.)

Este e o segundo pacote do experimento 26. Dois canais, duas linguas, mesma
variavel.

--------------------------------------------------------------- DIMENSIONAMENTO

`canal frio`: eixo novo, e o piso mais conservador da rotina — **oito
minutos**. Com todos os longos do canal em zero ou uma view, dimensionar para
treze minutos seria gastar render em algo que ninguem abre.

Oito capitulos, cada um com ~64s NA ESTIMATIVA e nunca 60 (aprendizado 537: o
desvio da estimativa nao tem sinal fixo e varia POR VOZ — medido em cinco
vozes, de menos um virgula nove a mais dois virgula oito por cento no total, e
ate mais sete por cento no ponto dos duzentos segundos). A resposta fecha ate
~192s na estimativa, e o tempo REAL vai ser conferido no copy.md renderizado.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO: **o que o cartao de recompensas pagou de verdade no ultimo ano,
menos o que ele cobrou**. Os eixos ja publicados aqui sao divida de cartao,
inadimplencia, parcelamento, bureaus de credito, vesting e historia economica.
Nenhum deles subtrai duas linhas do extrato dele.

AS TRES CONDICOES DO APRENDIZADO 504:
1. o dinheiro e DELE — o que o cartao devolveu e o que ele pagou de anuidade;
2. e ESCOLHA COM PRAZO — a anuidade cai numa data, e ele decide antes dela;
3. o SHORT entrega a conta — a subtracao fechada, com o resultado, e depois
   pede a inscricao.

FONTES: este video NAO faz nenhuma afirmacao institucional e NAO cita nenhum
numero meu. Nao cita percentual de recompensa, nao cita valor de anuidade, nao
cita taxa de juro, nao cita nome de banco, de cartao nem de programa. Os dois
numeros da conta estao no extrato do proprio espectador. Nao ha numero meu para
certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer
nem que dependa do cartao dele.

O QUE O VIDEO NAO FAZ: nao recomenda cartao nenhum, nao diz que anuidade e boa
ou ruim, nao promete economia, nao fala de score de credito e nao e
aconselhamento financeiro.
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
T("A card that pays you", "and charges you",
  "You have a card that pays you back. It also charges you to hold it. And "
  "almost nobody has ever put those two numbers side by side.",
  cap="A card that pays and charges")
I("This is not about the card", "it is about your year",
  "This is not a video about which card is better. It is about what YOUR card "
  "did for you last year, which is a different question and a far more useful "
  "one.")
I("And it has a deadline", "the fee posts on a date",
  "It also has a deadline. The fee posts on a specific date, and you decide "
  "before that date, every year, whether to keep paying it.")
I("Both numbers exist", "and both are yours",
  "The good news is that both numbers already exist, and both are yours. One "
  "is what came back to you. The other is what you paid to hold the card.")
I("One is easy", "the other is scattered",
  "One of them is easy to find. The other is scattered across twelve months, "
  "which is the only reason this is not obvious already.")
I("Nobody does it for you", "not the issuer",
  "Nobody runs this for you. The issuer has no reason to, and you have never "
  "had the two numbers in front of you at the same time.")
I("It takes one sitting", "not a system",
  "This is not a budgeting system. It is one sitting, with statements you "
  "already have.")
I("What is coming", "one subtraction",
  "In a few minutes you will run this yourself. It is one subtraction, with "
  "numbers already printed on your own statements.")

# -------------------------------------------------------------------- cap 2
T("The two sides", "what came back, what went out",
  "The calculation has two sides, and the common mistake is looking at only "
  "the first.",
  cap="The two sides of it")
I("Side one", "what the card returned",
  "Side one is everything the card returned to you over twelve months. Cash "
  "back, statement credits, points you actually redeemed.")
I("Points you did not use", "do not count",
  "Points sitting unredeemed do not count. They are not money until you spend "
  "them, and plenty of them expire that way.")
I("Value them the boring way", "what you would have paid",
  "And when you do redeem points, value them at what you would otherwise have "
  "paid in cash. Not at the number the program shows you.")
I("Side two", "what holding it cost",
  "Side two is what holding the card cost you: the annual fee, and any fee you "
  "paid because of this card and not another.")
I("Same twelve months", "on both sides",
  "Use the same twelve months on both sides. Mixing a full year of rewards "
  "with one month of fees proves whatever you already believed.")
I("Sign-up bonuses", "separate them out",
  "If a sign-up bonus landed in that window, keep it separate for now. It is "
  "real money, but it happens once and it distorts the picture.")
I("And referral credits", "same treatment",
  "Referral credits get the same treatment. Anything that will not repeat next "
  "year goes in its own line.")
I("Now they are comparable", "money against money",
  "With both sides in the same unit and the same window, this stops being an "
  "opinion about cards and becomes arithmetic about your year.")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA.
T("The math", "one subtraction",
  "So here is the math. One subtraction, and one optional division.",
  cap="The math: one subtraction")
I("Step one", "add what came back",
  "Step one: add up everything the card returned to you across those twelve "
  "months. Write it down.")
I("Step two", "add what you paid",
  "Step two: add the annual fee and any fee that exists only because you hold "
  "this card. Write that down too.")
I("Step three", "subtract",
  "Step three: subtract the second from the first. What is left is what the "
  "card actually paid you last year.")
I("If it is positive", "that is your number",
  "If the result is positive, that is real money the card handed you, and now "
  "you know the size of it instead of guessing.")
I("If it is negative", "that is the price",
  "If it is negative, that is what the card cost you to carry. Not a rate, "
  "not a percentage. A number, in your currency.")
I("The optional part", "divide by twelve",
  "If you want it in monthly terms, divide by twelve. That makes it easier to "
  "compare with the other things you pay every month.")
I("Do it on paper", "four lines",
  "Four lines on paper is enough: rewards, fees, the difference, and the date "
  "the fee posts. That last line is what makes it actionable.")
I("The math ends here", "the rest is why",
  "The math ends here and you can run yours now. The rest of this video is "
  "where the numbers hide, what the subtraction misses, and when it lies.")

# ================== DEPOIS DA RESPOSTA — POR QUE CONTINUAR ===================

# -------------------------------------------------------------------- cap 4
T("Where the numbers hide", "on your own statements",
  "Now the part that makes people get this wrong: where those numbers are "
  "actually kept.",
  cap="Where the numbers hide")
I("The year-end summary", "start there",
  "Most card issuers produce a year-end summary. Start there, because it "
  "collects twelve months in one place.")
I("But check it", "summaries can be partial",
  "Then check it against your statements, because those summaries sometimes "
  "count only one category and quietly leave others out.")
I("Statement credits", "look like discounts",
  "Watch for statement credits. They arrive looking like a discount on a "
  "purchase, so they are easy to miss on the rewards side.")
I("The fee", "may not say fee",
  "The fee may not be labelled the way you expect, and on some cards it "
  "arrives split or waived for the first year only.")
I("Foreign transaction charges", "belong here",
  "Charges that exist because of this card and not another belong on the cost "
  "side too. If another card in your wallet would not have charged it, it "
  "counts.")
I("Twelve statements", "beats memory",
  "If the summary looks thin, open the twelve statements themselves. It takes "
  "twenty minutes and it removes all the guessing.")
I("Note the date", "while you are there",
  "While you are in there, note the date the annual fee posted. That is your "
  "deadline for next year, and it is the one thing people never write down.")
I("If in doubt", "undercount the rewards",
  "When you are unsure, undercount the rewards side. If the answer still looks "
  "good under a stingy count, it really is good.")

# -------------------------------------------------------------------- cap 5
T("What it misses", "and it is fair to say",
  "There are things this subtraction does not capture, and it is more honest "
  "to name them than to pretend it settles everything.",
  cap="What the subtraction misses")
I("Protections", "worth something, rarely used",
  "The first: purchase and travel protections. They are worth something, and "
  "most people never use them.")
I("Value them as insurance", "not as a feature list",
  "Value them the way you would value insurance: by what you would have paid "
  "for the same cover, not by how long the feature list is.")
I("The second", "what it made you spend",
  "The second cuts the other way. If chasing rewards made you spend more than "
  "you otherwise would, that difference belongs on the cost side.")
I("That one is uncomfortable", "and it is real",
  "That number is uncomfortable and rarely written down, but it is the one "
  "that turns a good-looking result into a bad year.")
I("The third", "interest",
  "The third is simple. If you ever carried a balance on this card, interest "
  "goes on the cost side, and it usually dwarfs everything else here.")
I("The fourth", "time you spend on it",
  "There is a fourth, smaller one: the time spent tracking categories and "
  "chasing redemptions. If that is hours a month, it belongs somewhere.")
I("None of these are excuses", "they come after",
  "All of these belong AFTER the subtraction, never before it. Raised first, "
  "they become reasons not to look at the number at all.")
I("Then rewards stop mattering", "the balance decides",
  "In that case the rewards question is not the important one. The balance is, "
  "and no reward rate outruns it.")

# -------------------------------------------------------------------- cap 6
T("When it lies", "the first year",
  "Now the case that fools almost everyone.",
  cap="When the number lies")
I("A first year", "is not a normal year",
  "A first year is not a normal year. Sign-up bonuses and waived fees make the "
  "result look better than the card will ever look again.")
I("So run year two", "if you have one",
  "If you have held the card longer than a year, run the calculation on a year "
  "with no bonus in it. That is the honest one.")
I("And an unusual year", "cuts both ways",
  "An unusual year cuts the other way too. A year with one large purchase, or "
  "one you spent mostly at home, is not the year ahead either.")
I("Two years is enough", "to see the pattern",
  "Two ordinary years are enough to tell whether you are looking at a pattern "
  "or at one strange twelve months.")
I("Downgrades exist", "not only cancel or keep",
  "And the choice is rarely just keep or cancel. Most issuers have a version "
  "of the same card with no fee, and moving to it is a third option.")
I("That option keeps the age", "which matters to some",
  "That option also tends to preserve how long the account has been open, "
  "which some people care about for reasons outside this calculation.")
I("Ask before deciding", "the fee window",
  "There is usually a window after the fee posts in which the decision can "
  "still be reversed. Worth knowing before you need it.")
I("Both answers are valid", "your number decides",
  "Keeping the card and dropping it are both defensible, and neither is right "
  "in general. The right one is whatever your number points to. The only wrong "
  "move is renewing by default and never looking.")

# -------------------------------------------------------------------- cap 7
T("From one year", "to several",
  "Now the step that makes the size of this feel real.",
  cap="From one year to several")
I("One year", "looks small",
  "The difference in a single year usually looks small, in either direction. "
  "It is small, and that is exactly why it survives unexamined.")
I("Multiply", "by the years you have held it",
  "Multiply it by the number of years you have held the card. Same behaviour, "
  "added up.")
I("Then look forward", "the fee repeats",
  "Then look forward, because the fee repeats on a schedule and so does the "
  "result, with the same sign.")
I("Compare it", "with something you know",
  "To feel the size, compare it with something familiar. If several years add "
  "up to a flight you would have taken anyway, that says one thing. If they "
  "add up to a coffee, that says something very different.")
I("A small answer", "is still an answer",
  "It is entirely possible the number comes out near zero, and nothing needs "
  "to change. That is a complete answer, and now it is measured rather than "
  "assumed.")
I("Do it per card", "not per wallet",
  "Run this per card, not across your whole wallet. Two cards can pull in "
  "opposite directions, and averaging them hides both.")
I("The pattern shows fast", "two cards is enough",
  "Two cards run side by side is usually enough to see which one is carrying "
  "the other.")
I("The good part", "it comes back every year",
  "The good part is that this decision returns every year, and returns whole. "
  "One bad year does not commit the next one.")

# -------------------------------------------------------------------- cap 8
T("What to do today", "three steps",
  "We will close with what you can do today, in three steps.",
  cap="What to do today")
L("Three steps",
  ["Add what came back", "Add what you paid", "Subtract"],
  "First: add everything the card returned to you over twelve months. Second: "
  "add the annual fee and any fee that exists only because of this card. "
  "Third: subtract the second from the first.")
I("Do it once", "on last year",
  "Do it once, on last year, using the year-end summary as your starting "
  "point. It is one sitting.")
I("If it is positive", "you are done",
  "If it comes out positive, you are done, and you can stop wondering about it "
  "every time the fee posts.")
I("If it is negative", "you now know the price",
  "If it comes out negative, the decision now has a visible price. You are "
  "still allowed to pay it — the difference is that you know.")
I("Change one thing", "not everything",
  "And if you do change something, change one thing: the card, or how you "
  "redeem. Changing both at once means you will never know which one worked.")
# EXPERIMENTO 26: o pedido do longo tambem fecha em conta, nao em clique.
I("Put the date somewhere", "you will see it",
  "And put the fee date somewhere you will actually see it, a month ahead. "
  "That single line is what turns this from a one-off into a decision.")
C("Post your number", "in the comments",
  "If you run it, post one thing below: the result, with its sign. No card "
  "name, no balance, just the number. I want to see how far these spread "
  "between people holding the same kind of card.")

# =============================== O SHORT =====================================
# EXPERIMENTO 26, segundo pacote. O short entrega a subtracao FECHADA e gasta o
# pedido na INSCRICAO, amarrada ao metodo. Nao aponta para o longo.

SHORT = [
    {"layout": "titulo", "kicker": "Your rewards card",
     "sub": "did it pay you?",
     "nar": "Your rewards card pays you back and charges you to hold it. Which "
            "one won last year? Run it now.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Number one",
     "sub": "what came back",
     "nar": "Number one: everything the card returned over twelve months. Cash "
            "back, statement credits, points you actually redeemed.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Number two", "sub": "what you paid",
     "nar": "Number two: the annual fee, plus any fee that exists only because "
            "you hold this card.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Subtract", "sub": "that is your answer",
     "nar": "Subtract the second from the first. Positive means the card paid "
            "you. Negative is what it cost you to carry. That is the whole "
            "calculation.", "sem_cap": True},
    {"layout": "cta", "kicker": "If that was useful",
     "sub": "subscribe — one a week",
     "nar": "If that was useful, subscribe. One money calculation a week, run "
            "on your own numbers.", "sem_cap": True},
]

THUMB = {"l1": "Rewards", "l2": "or fee"}

COPY = """# What your rewards card actually paid you last year, from your own statements

## TITULO
Rewards or Fee? What Your Card Actually Paid You Last Year

## DESCRICAO
You have a card that pays you back. It also charges you to hold it. And almost nobody has ever put those two numbers side by side. This is not a video about which card is better — it is about what YOUR card did for you last year, which is a different question and a far more useful one. It also has a deadline: the fee posts on a specific date, and you decide before that date, every year, whether to keep paying it.

There is not a single number of mine in this video. No reward percentage, no fee amount, no interest rate, no bank, card, or programme named. Both numbers in the calculation are yours, and both are already printed on your own statements.

The math is one subtraction. Add up everything the card returned to you across twelve months — cash back, statement credits, and points you actually redeemed, valued at what you would otherwise have paid in cash rather than at the number the programme shows you. Points sitting unredeemed do not count; they are not money until you spend them. Then add the annual fee and any fee that exists only because you hold this card. Subtract the second from the first. What is left is what the card actually paid you last year. Divide by twelve if you want it in monthly terms.

One chapter covers where those numbers hide: the year-end summary is the place to start, but check it against your statements, because those summaries sometimes count one category and quietly leave others out. Statement credits arrive looking like a discount on a purchase, so they are easy to miss. And fees are not always labelled the way you expect.

One chapter covers what the subtraction misses, because naming it is more honest than pretending it settles everything: purchase and travel protections, which are worth something and are rarely used — value them as insurance, by what the same cover would cost; the spending the rewards themselves encouraged, which belongs on the cost side and is the number that turns a good-looking result into a bad year; and interest, which goes on the cost side if you ever carried a balance, and usually dwarfs everything else here.

And one chapter covers when the number lies. A first year is not a normal year: sign-up bonuses and waived fees make it look better than the card will ever look again. If you have held it longer, run a year with no bonus in it. Two ordinary years tell you whether you are seeing a pattern or one strange twelve months.

The close is three steps you can run today, from the summary you already have.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Run it on last year and post one thing below: the result, with its sign. No card name, no balance, no spending — just the number. I want to see how far these spread between people holding the same kind of card.

## HASHTAGS
#PersonalFinance #CreditCards #NextLevelMoney

## TAGS
rewards card worth it, annual fee worth it, cash back math, credit card rewards, is my card worth the fee, year end summary, statement credits, redeem points value, personal finance, money calculation, card annual fee, rewards vs fee, budgeting, financial literacy, run the numbers

## CONFIGURACOES DO STUDIO
- Idioma: Ingles (en) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Estados Unidos | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita percentual de recompensa, nao cita valor de anuidade, nao cita taxa de juro, nao cita nome de banco, de cartao nem de programa de pontos, e nao compara produtos entre si. Os dois numeros da conta sao do proprio espectador e os dois estao no extrato dele: o que o cartao devolveu em doze meses e o que ele pagou para manter o cartao no mesmo periodo. Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa do pais, do emissor ou do produto dele. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA: qualquer percentual de cashback, valor de anuidade ou taxa. Esses valores mudam por emissor, por produto e por data, e citar um so deles tornaria a conta errada para a maioria de quem assiste. O video tambem nao recomenda cartao nenhum, nao diz que anuidade e boa ou ruim — as duas respostas sao legitimas e dependem do numero de cada um —, nao fala de score de credito, nao promete economia e nao e aconselhamento financeiro.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/next-level-money-008.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "next-level-money",
    "pacote": "next-level-money-008",
    "idioma": "en",
    "voz": "en-US-AndrewNeural",
    "trilha": "Deliberate_Thought",
    "paleta": {"ink": "#1A1A1A", "c1": "#2A6F97", "c2": "#E9C46A", "bg": "#F2ECDF"},
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
    grava(SPEC, "fabrica/specs/next-level-money-008.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
