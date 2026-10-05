#!/usr/bin/env python3
"""Monta a spec next-level-money-009.

ALAVANCA ATACADA: **A — conversao pela FORMA**, com o eixo novo que o veredito
`canal frio` manda, e e a troca mais radical que este canal ja levou: de FATO
SOBRE O SISTEMA para METODO NO PROPRIO EXTRATO.

NUMERO DE PARTIDA, medido em 05/10/2026 em dado de vida inteira (ultima linha
de `videos.list` por video — nunca `max(views)`, aprendizado 557):

    pacote   short   longo   travessia
    003        16       1       6,3%
    004        13       1       7,7%
    005         4       7      175%
    006        17       2      11,8%
    007        22       1       4,5%
    008         2       2      100%

    next-level-money: 24 videos, 160 views DE CANAL
    teto de um video: 25 views (e e uma das duplicatas de cron)
    veredito: `canal frio`

O QUE NAO DEU, e precisa ser dito sem rodeio: este e o canal mais frio da frota
em numero absoluto. Cento e sessenta views em vinte e quatro videos, com teto de
vinte e cinco. As travessias de 175% e 100% nao sao boa noticia — sao divisao
por quatro e por dois, ruido de amostra minuscula. Nao ha sinal de alcance aqui
para interpretar.

E ele NAO tem a desculpa do agla-level: next-level-money nao esta na lista dos
cinco canais sem `youtube.com/verify`, entao as capas desenhadas SUBIRAM. O que
sobra e o caso mais duro da frota: ingles, o idioma mais disputado do YouTube,
canal minusculo, capa propria, e ninguem chega.

O QUE DEU CERTO: nada que eu possa chamar de sinal. Seria desonesto apontar um
padrao em views de 2 a 25.

O QUE SE VE NOS TITULOS, e e a unica leitura que a amostra sustenta: TODOS
abrem com numero institucional — um virgula vinte e seis trilhao de divida de
cartao, doze virgula oito por cento de inadimplencia, dezesseis por cento dos
adultos no BNPL, sete virgula nove trilhoes da Companhia das Indias. Sao fatos
sobre o sistema. O aprendizado 482 diz que fato nao converte, metodo converte, e
este canal e doze pacotes seguidos de fato.

O QUE MUDO POR CAUSA DISSO: **EIXO NOVO**, e nao e so de assunto — e de
natureza. Sai o fato sobre o sistema e entra uma conta que o espectador faz no
extrato DELE. O angulo de "dinheiro e poder" do canal nao e abandonado, e
virado para dentro: a pergunta deixa de ser quem decide o dinheiro do mundo e
passa a ser **quanto do dinheiro DELE ja foi decidido por outra pessoa antes de
ele ver**.

--------------------------------------------------------------- DIMENSIONAMENTO

`canal frio`: eixo novo e piso de oito minutos por analogia com `suspenso`. Com
o longo em zero virgula zero dois views/dia de mediana, qualquer segundo acima
do piso e render gasto em algo que ninguem termina.

Oito capitulos de ~68s NA ESTIMATIVA, bem acima dos 64,2s que o
`prontidao.MARGEM_CAP` cobra. A en-US-AndrewNeural tem duas medidas de desvio no
`ensaio.py` — +0,5% e +3,8%, de lotes diferentes — e as duas empurram o
capitulo para CIMA, que e o lado seguro do portao.

A resposta fecha dentro dos primeiros 200 s, no capitulo 3. O tempo REAL sai do
`legendas.srt`.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO: **a parte do dinheiro dele que ja estava comprometida antes de ele
decidir qualquer coisa.**

Os eixos ja publicados neste canal sao bureaus de credito, divida de cartao e
pagamento minimo, inadimplencia, BNPL, vesting de 401k, recompensa de cartao
contra anuidade, e a Companhia das Indias Orientais (sete vezes, pelas
duplicatas de cron). Nenhum deles e este, e nenhum deles pede o extrato do
espectador.

AS TRES CONDICOES DO APRENDIZADO 504:
1. o dinheiro e DELE — o que saiu da conta dele no mes passado;
2. e ESCOLHA COM PRAZO — as datas de debito automatico do mes que vem;
3. o SHORT entrega a conta — a divisao fechada, com o resultado.

FONTES: este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao
institucional. Nao cita aliquota, nao cita taxa de juro, nao cita media
nacional, nao cita percentual recomendado de orcamento, nao cita nome de banco
nem de produto. Os dois numeros da conta sao do proprio espectador: o que saiu
da conta dele e o que entrou. ISSO E DELIBERADO, e e o que o aprendizado dos
doze pacotes anteriores manda: numero institucional e o que este canal ja fez
doze vezes sem alcance nenhum.

O QUE O VIDEO NAO FAZ: nao diz qual percentual e saudavel, nao recomenda
cancelar nada, nao compara o espectador com media nenhuma, nao diz que divida e
erro, e nao e aconselhamento financeiro.
"""
import json

CENAS = []

# Links resolvidos em 05/10/2026 pela pre-busca rodada do sandbox, onde
# `api.pexels.com` responde. `--conferir`: 3/3 clipes que o CDN entrega. Com o
# link gravado o pacote fica reproduzivel — sem ele, dois renders da mesma spec
# pegam clipes diferentes, porque o Pexels reordena a busca.
BROLL = {
    6862466: ("https://videos.pexels.com/video-files/6862466/6862466-hd_1366_720_25fps.mp4",
              "cottonbro studio",
              "https://www.pexels.com/video/a-person-looking-bank-check-while-using-laptop-6862466/"),
    6327790: ("https://videos.pexels.com/video-files/6327790/6327790-hd_1366_720_25fps.mp4",
              "Kaboompics",
              "https://www.pexels.com/video/person-counting-money-6327790/"),
    6964247: ("https://videos.pexels.com/video-files/6964247/6964247-hd_1280_720_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/man-using-calculator-6964247/"),
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


def I(kicker, preco, nar):
    CENAS.append({"layout": "item", "kicker": kicker, "preco": preco,
                  "nar": nar, "sem_cap": True})


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================= OS PRIMEIROS 200 SEGUNDOS ===========================

# -------------------------------------------------------------------- cap 1
B("One account", "two kinds of money",
  "There is money in your account that you decide, and money that was already "
  "decided before you ever saw it. Same account. Same balance.",
  "person looking at bank statement on a laptop", 6862466,
  cap="Two kinds of money, one account")
I("This is not a trap", "it is a structure",
  "Nobody is tricking you. Rent gets decided once and then repeats. So does "
  "insurance. So does a loan payment. That is how those things work.")
I("But the size of it", "you should know",
  "What you should know is how big that part is, because it is the part you "
  "cannot move this month no matter what you decide.")
I("And it is not about discipline", "it is about timing",
  "This also is not a discipline problem. The committed part is not money "
  "you spent badly — it is money whose decision happened in the past, which "
  "is a completely different thing to work on than a habit.")
I("No number of mine", "both numbers are yours",
  "There is not a single number of mine in this. No rate, no average, no "
  "recommended percentage, no bank name. Both numbers are already in your "
  "account.")
I("And the deadline is yours", "next month's autopay dates",
  "The deadline is yours too: the autopay dates on next month's statement. "
  "They are already scheduled.")
I("Most people guess low", "and guess by feel",
  "Almost everyone guesses this number low, and guesses it by feel. The "
  "guess and the statement rarely land close, and the gap between them is "
  "the whole reason to open the statement at all.")
I("Two chapters", "and the math is done",
  "Two chapters from now the math is finished. One addition, one division, and "
  "both numbers come off paper you already have.")

# -------------------------------------------------------------------- cap 2
T("The first number", "from the statement, not memory",
  "The first number is what left your account last month, and memory is no "
  "good here. Memory counts the normal month and skips the real one.",
  cap="First number: from the statement")
I("Open one month", "every line that left",
  "Open last month on your bank or card statement. Every line that left the "
  "account. Not the plan, not the budget — what actually went out.")
I("Now split it", "decided then, or decided now",
  "Now split those lines in two. On one side, the ones you decided LAST month. "
  "On the other, the ones that were decided once, earlier, and simply "
  "repeated.")
I("The second side counts", "and only that side",
  "Only the second side counts for this number. Rent or mortgage. Insurance. "
  "The minimum on any loan. Anything on autopay. Withholding, which left before "
  "the money ever reached you.")
I("The test is one question", "could you have skipped it?",
  "If a line is hard to place, ask one question: could you have skipped it "
  "last month without breaking an agreement you already signed? If yes, you "
  "decided it. If no, it was decided for you.")
I("Groceries do not count", "you chose them this month",
  "Groceries do not count. Dinner out does not count. A repair does not count. "
  "You decided those last month, even when they felt unavoidable.")
I("One month is enough", "but it has to be a whole one",
  "One month is enough, as long as it is a whole one. Half a month cuts the "
  "commitments that fall on the other half, and those are usually the "
  "biggest ones on the statement.")
I("And add them up", "that is the first number",
  "Add the second side up. That total is the first number: what was already "
  "committed before the month started.")

# -------------------------------------------------------------------- cap 3
B("The second number", "already printed",
  "The second number you do not have to estimate. It is already printed, and "
  "it is at the top of the same statement.",
  "hands holding a paper bank statement", 6327790,
  cap="Second number, and the division")
I("What came in", "the amount that landed",
  "What came in last month — the amount that actually landed in the account, "
  "not the amount on the offer letter.")
I("Now divide", "first by second",
  "Divide the first number by the second and multiply by one hundred. The "
  "percentage you get is the share of your money that was decided before you "
  "saw it.")
I("Use what landed, not gross", "you pay with what landed",
  "Use what landed and not the gross figure, because you pay the committed "
  "part out of what landed. Using gross makes the percentage look smaller "
  "than the month actually felt.")
I("One more turn", "percent into days",
  "If you want it in days instead: take that percentage, multiply by thirty, "
  "and divide by one hundred. That is how many days of the month were spent "
  "before the first of the month.")
I("Write both numbers down", "not just the percent",
  "Write both numbers down, not only the percentage. A percentage alone "
  "cannot tell you later whether it moved because the committed part shrank "
  "or because your income grew, and those two call for opposite decisions.")
I("The math is done", "what is left is where",
  "The math is finished. What is left is the question it just created: where "
  "that committed part comes from, and which parts of it can still move.")
I("And one warning", "I will not say what is healthy",
  "One warning now: this video will not tell you what percentage is healthy. "
  "That depends on where you live and what you earn, and you know those, not "
  "me.")

# ================= DEPOIS DA RESPOSTA — POR QUE CONTINUAR ====================

# -------------------------------------------------------------------- cap 4
T("Why it comes out high", "four places, not one",
  "That number almost always comes out higher than people guess, and the "
  "reason is not one thing. It accumulates in four separate places.",
  cap="The four places it accumulates")
I("The first place", "decided before it arrives",
  "The first place is the money that never reached the account: withholding "
  "and anything deducted at the source. It is the largest for most people and "
  "the easiest to forget, because it is invisible on the statement.")
I("The second place", "a one-time choice that repeats",
  "The second place is a choice you made once, years ago, that still repeats "
  "every month. The deciding happened once; the paying did not stop.")
I("The third place", "small and automatic",
  "The third place is the small automatic ones. Each is too small to argue "
  "with, and none of them has a day on which you decide it again.")
I("The fourth place", "the minimum on a balance",
  "The fourth place is the minimum on a balance. It is committed money that "
  "grows if you only ever pay the committed part — which is why it belongs in "
  "this count and not in the other one.")
I("And they hide differently", "which is why four",
  "They hide in different ways, and that is why counting them as a single "
  "number is not enough. The first never appears on the statement at all. "
  "The next appears every month, in the same place. Another arrives in small "
  "pieces. And the last one looks like progress while it stands still.")
I("Four places", "and the first is the biggest",
  "Four places, and they are not equal. For most people the first one is "
  "larger than the other three together, and it is the one nobody looks at.")

# -------------------------------------------------------------------- cap 5
B("Four places", "four moves",
  "Each place has one move, and none of them asks you for a number you do not "
  "already have.",
  "person writing notes next to a calculator", 6964247,
  cap="One move for each place")
I("For the first", "read the deduction lines",
  "For the first: read the deduction lines on your own pay statement, one by "
  "one, and find out which of them you chose and which you did not. Some are "
  "choices wearing the clothes of a rule.")
I("For the second", "put a date on it",
  "For the second: give each repeating commitment a date on which you look at "
  "it again. Once a year is enough. Without a date, a decision made once "
  "becomes permanent by default.")
I("For the third", "one statement, one pass",
  "For the third: go down one statement and mark every automatic charge. Not "
  "to cancel them — to see them in one place, which is the thing that has "
  "never happened.")
I("For the fourth", "one dollar above the minimum",
  "For the fourth: pay anything above the minimum, even a little. The minimum "
  "is the amount that keeps the commitment alive; anything above it is the only "
  "part that ends it.")
I("And measure before you move", "so the move is readable",
  "Do the measurement before you change anything. If you move first and "
  "measure after, you will never know which of the four places the "
  "difference came from, and the next decision gets harder, not easier.")
I("Pick one", "not four",
  "And do not do all four this month. Pick the place where your own number is "
  "biggest, and work only on that one until you measure again.")

# -------------------------------------------------------------------- cap 6
T("What this leaves out", "on purpose",
  "Now the part that is better said than hidden: three things are deliberately "
  "NOT in this division.",
  cap="What the division leaves out")
I("Saving is not counted", "it is still yours",
  "Money you moved into savings is not counted as committed, even on autopay. "
  "It did not leave your control; it changed rooms.")
I("One-time bills", "they distort the month",
  "A one-time bill is not counted either. A repair or an annual payment makes "
  "one month look terrible and tells you nothing about the pattern.")
I("And value is not counted", "only timing",
  "This number says nothing about whether the commitments are worth it. "
  "Insurance you need and a subscription you forgot look identical here, "
  "because this count measures WHEN a thing was decided, not whether it was "
  "wise.")
I("A small number is a result too", "and a real one",
  "And if your percentage comes out small, that is a legitimate result, not a "
  "failed measurement. It means this is not where your money is going, and the "
  "next question is where it is.")
I("And it is not a score", "nobody grades this",
  "This is not a score and nobody grades it. A high number can be the right "
  "answer for someone who chose a house on purpose, and a low one can hide "
  "an income that is simply too small to commit anything.")
I("What matters", "that it repeats the same way",
  "What matters is not whether the number is high or low. It is that you can "
  "measure it the same way next month, because only then does the difference "
  "between two numbers mean something.")

# -------------------------------------------------------------------- cap 7
T("Same pay, different share", "and it fools everyone",
  "Here is the case that fools almost everyone: two people with the same "
  "amount landing in the account, and completely different freedom.",
  cap="Same pay, different committed share")
I("The pay is equal", "the committed part is not",
  "The amount that lands is identical. But for the first of them, most of it "
  "was decided in advance, and for the second, far less was. So when "
  "something goes wrong in a month, one of them has room and the other does "
  "not — on the same pay.")
I("Which is why", "pay is a bad comparison",
  "Which is why comparing two jobs, or two cities, or two years of your own "
  "life by what lands in the account tells you much less than people think.")
I("The comparison that works", "what is left after the committed part",
  "The comparison that works is what remains after the committed part. That is "
  "the number you actually spend decisions on.")
I("It also explains a raise", "that changed nothing",
  "It also explains the raise that somehow changed nothing. If the committed "
  "part grows with the raise, the room you spend decisions on stays exactly "
  "where it was, and the feeling of standing still is accurate.")
I("And it explains the opposite", "a smaller pay that felt easier",
  "And the opposite case, which people rarely talk about: a smaller amount "
  "landing in the account that somehow felt easier, because the committed "
  "share went down more than the pay did.")
I("And it moves slowly", "which is the good news",
  "The committed share moves slowly, which cuts both ways: it will not improve "
  "in a week, and it will not collapse in a week either. It responds to "
  "decisions made once, which is exactly what you can do.")

# -------------------------------------------------------------------- cap 8
T("Today, three steps", "with what you already have",
  "So today, three steps, and all three use paper you already have.",
  cap="Three steps today")
I("Step one", "one month, two sides",
  "First: open last month's statement and split what left into decided-then "
  "and decided-now. Add up the decided-then side. That is your first number.")
I("Step two", "what landed",
  "Second: take what landed in the account that same month. Not gross. The "
  "amount that arrived.")
I("Step three", "divide, and write the date",
  "Third: divide, multiply by one hundred, and write the percentage down with "
  "today's date next to it. The date is the part people skip, and it is the "
  "part that makes the second measurement worth anything.")
I("Then do it again next month", "same two sides",
  "Then do exactly the same thing next month, splitting the statement the "
  "same way. Two dated percentages are worth more than one careful "
  "percentage, because only the difference tells you anything.")
C("Put the percent below", "not your pay, not your city",
  "And in the comments, put one thing: the percentage. Not your pay, not your "
  "city, not where you work. Just the percent. I want to see how far apart "
  "this number lands for people who look alike on paper.")


# =============================== O SHORT =====================================
# O short fecha UMA pergunta — a divisao, com o resultado — e o longo abre
# OUTRA: de onde vem a parte comprometida (aprendizado 563).

SHORT = [
    {"layout": "titulo", "kicker": "Two kinds of money",
     "sub": "in one account",
     "nar": "Some of the money in your account was already decided before you "
            "saw it. Here is how much.", "sem_cap": True},
    {"layout": "titulo", "kicker": "First", "sub": "what repeated",
     "nar": "First: last month's statement. Add only the lines that were "
            "decided once and repeated. Rent, insurance, autopay, minimums, "
            "withholding.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Second", "sub": "what landed",
     "nar": "Second: what actually landed in the account that month.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Divide", "sub": "that is your share",
     "nar": "Divide the first by the second, times one hundred. That is the "
            "share of your money someone else decided.", "sem_cap": True},
    {"layout": "cta", "kicker": "Where it comes from",
     "sub": "four places, below",
     "nar": "It piles up in four places, and all four are in the video below.",
     "sem_cap": True},
]

THUMB = {"l1": "Already", "l2": "spent"}

COPY = """# The share of your money that was decided before you saw it

## TITULO
Your Money Is Already Spent: The Share Someone Else Decided Before You Saw It

## TITULO SHORT
How much of your pay is already spent?

## DESCRICAO
There is money in your account that you decide, and money that was already decided before you ever saw it. Same account, same balance. Nobody is tricking you — rent gets decided once and then repeats, and so does insurance, and so does a loan payment. That is how those things work. What you should know is how big that part is, because it is the part you cannot move this month no matter what you decide.

There is not a single number of mine in this video. No rate, no average, no recommended budget percentage, no bank name, no product name. That is deliberate, and it comes from this channel's own record: twelve packages in a row opened with an institutional number — trillions in card debt, delinquency percentages, adoption percentages — and none of them reached anyone. Both numbers in this calculation are already sitting in your account.

The first number cannot come from memory, because memory counts the normal month and skips the real one. Open last month on your statement and look at every line that left the account. Then split those lines in two: the ones you decided LAST month, and the ones that were decided once, earlier, and simply repeated. Only the second side counts — rent or mortgage, insurance, the minimum on any loan, anything on autopay, and withholding, which left before the money ever reached you. Groceries do not count. Dinner out does not count. A repair does not count. You decided those, even when they felt unavoidable.

The second number is already printed at the top of the same statement: what actually landed in the account, not what the offer letter says. Divide the first by the second, multiply by one hundred, and the percentage you get is the share of your money that was decided before you saw it. If you want it in days, multiply that percentage by thirty and divide by one hundred — that is how many days of the month were spent before the first of the month.

One chapter is about why that number comes out higher than people guess, and there are four separate places it accumulates: the money that never reached the account; a one-time choice that still repeats; the small automatic charges that are each too small to argue with; and the minimum on a balance, which is committed money that grows if you only ever pay the committed part. For most people the first place is larger than the other three together, and it is the one nobody looks at. The next chapter gives one move for each place, and asks you to pick only one.

One chapter lists what the division deliberately leaves out, because that is better said than hidden: money moved into savings, one-time bills, and the question of whether a commitment is worth it at all. This number measures WHEN a thing was decided, not whether it was wise — which is why insurance you need and a subscription you forgot look identical in it. And a small percentage is a legitimate result, not a failed measurement.

One chapter is about the case that fools almost everyone: two people with the same amount landing in the account and completely different freedom, because one had eighty percent decided in advance and the other had forty.

At the end, three steps, all using paper you already have.

Footage: Pexels (free license) — cottonbro studio, Kaboompics, Mikhail Nilov.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Run the number and put one thing in the comments: the percentage. Not your pay, not your city, not where you work — just the percent. I want to see how far apart this lands for people who look alike on paper. And if it comes out small, post that too; that is a result.

## HASHTAGS
#PersonalFinance #Money #NextLevelMoney

## TAGS
how to read a bank statement, fixed vs variable expenses, committed spending, autopay audit, paycheck withholding explained, take home pay, monthly budget math, minimum payment trap, recurring charges, subscription audit, personal finance basics, money management, cash flow, financial freedom math, where my money goes

## CONFIGURACOES DO STUDIO
- Idioma: Ingles (en) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Estados Unidos | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita aliquota de imposto, nao cita taxa de juro, nao cita media nacional, nao cita percentual recomendado de orcamento, nao cita nome de banco, de produto nem de aplicativo. Os dois numeros da conta sao do proprio espectador: o que saiu da conta dele no mes passado, separado por ELE em duas categorias, e o que entrou nela no mesmo mes. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA, e por que: (1) qualquer percentual de referencia do tipo "o normal e comprometer X por cento", porque nao existe fonte oficial para isso e o video nao faz essa comparacao — a conta e sobre o extrato dele, nao sobre uma media; (2) qualquer aliquota ou regra de retencao na fonte, porque muda por pais, por estado e por situacao, e citar uma tornaria a conta errada para a maioria de quem assiste, justamente quando o numero certo esta impresso na folha de pagamento dele; (3) o JUIZO sobre cada compromisso — o video diz explicitamente que seguro necessario e assinatura esquecida sao identicos nesta conta, porque ela mede QUANDO a coisa foi decidida e nao se foi acertada. ESTE EIXO SUBSTITUI O NUMERO INSTITUCIONAL DE PROPOSITO: os doze pacotes anteriores deste canal abriram com um (1,26 trilhao de divida de cartao, 12,8% de inadimplencia, 16% dos adultos no BNPL, 7,9 trilhoes da Companhia das Indias) e somaram 160 views de canal em 24 videos. O video tambem nao diz qual percentual e saudavel, nao recomenda cancelar nada, nao compara o espectador com media nenhuma, nao diz que divida e erro e nao e aconselhamento financeiro.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/next-level-money-009.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "next-level-money",
    "pacote": "next-level-money-009",
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
    from ensaio import duracao_estimada, duracao_estimada_short, duracao_cena
    grava(SPEC, "fabrica/specs/next-level-money-009.json")
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
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: {c['broll_q']}")
