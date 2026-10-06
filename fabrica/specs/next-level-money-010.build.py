"""next-level-money-010 — um unico juro, cinco respostas diferentes.

ALAVANCA ATACADA: A (conversao short -> inscrito), pela FORMA do pacote.

O NUMERO DE PARTIDA, do PROPRIO canal, deduplicado e com a ULTIMA leitura de
`metricas` (a trava do 549 acusou 170 quedas em 4.046 linhas lifetime nesta
rodada — `max(views)` esta proibido, aprendizados 592 e 594):

    pacote  short -> longo  dur   titulo
    005         4 ->   7    793s  Delinquency Hit 12.8%: Why the Fed Told Everyone Not to Read It That Way
    006        17 ->   2    781s  Buy Now Pay Later Reached 16% of Adults
    008         2 ->   2    558s  Rewards or Fee? What Your Card Actually Paid You
    003        16 ->   1    792s  The Economics Behind Credit Bureaus
    004        13 ->   1    756s  Credit Card Debt Hit $1.26 Trillion
    voc         2 ->   1    728s  The Dutch East India Company
    007        22 ->   0    484s  One Balance, Two Kinds of Money: 401(k) Vesting
    009         0 ->   0    586s  publicado ontem, sem leitura

PRIMEIRO, A HONESTIDADE SOBRE A ESCALA: o teto deste canal e SETE views de
longo, e ele tem ZERO inscritos depois de treze pacotes publicados. Com numeros
desse tamanho NAO DA PARA LER SINAL DENTRO DO CANAL — a diferenca entre sete e
dois nao e um achado, e ruido. Nao vou inventar padrao a partir disso.

O QUE DA PARA DIZER, e so isso: o 007 tem o MAIOR short do canal (22 views) e
ZERO views de longo, e e tambem o longo mais curto (484 s). Isso e consistente
com o 584/594 em escala de frota — short que estoura nao traz ninguem — mas um
pacote nao prova nada sozinho.

ENTAO O GUIA DESTA RODADA E DE FORA DO CANAL, de proposito: os aprendizados
589/595, medidos na frota inteira e refeitos hoje com a ultima leitura (digito
nove a zero, dois-pontos sete a zero, interrogacao seis a um). Titulo
declarativo, com a coisa buscavel NOMEADA, dois-pontos, digito, sem ponto de
interrogacao. O 008 deste canal e o unico titulo em pergunta e deu duas views.

E O 005, QUE E O MELHOR, da a VOZ do canal: um numero oficial que todo mundo
le de um jeito e o orgao que o publica avisa para nao ler assim. Este pacote
repete essa voz num numero novo.

VEREDITO DO CANAL: `canal frio` (v_maquina_licoes, 12 shorts e 12 longos
medidos, 160 views). Pela rotina isso manda eixo novo e PISO DE 8 MINUTOS por
analogia com `suspenso`. Saiu em 8,96 min — piso, nao teto.

EIXO, e por que ele e novo. Os oito pacotes falam de inadimplencia, BNPL,
cartao (recompensa contra tarifa), bureaus de credito, divida de cartao,
Companhia das Indias, vesting do 401(k) e renda ja comprometida. NENHUM fala
do juro que o PROPRIO governo cobra e paga — e e ai que a assimetria aparece
escrita na lei.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# O QUE ENTRA, e esta fechado em DUAS INSTITUICOES INDEPENDENTES:
#
#   * a REGRA, do texto da lei: 26 U.S.C. paragrafo 6621, lido no
#     govinfo.gov (U.S. Government Publishing Office, USCODE-2023-title26):
#       - taxa de RESTITUICAO = federal short-term rate + TRES pontos
#         percentuais, "(2 percentage points in the case of a corporation)";
#       - restituicao de empresa na parte que passa de dez mil dolares: a lei
#         manda substituir por "0.5 percentage point";
#       - taxa de DEBITO = federal short-term rate + TRES pontos, para todos;
#       - "large corporate underpayment": a lei manda substituir tres por
#         "5 percentage points" (6621(c));
#       - o federal short-term rate e determinado mensalmente pelo Secretario
#         sob a secao 1274(d) e arredondado para o inteiro mais proximo.
#   * a MESMA REGRA, da agencia que a aplica: irs.gov/payments/quarterly-
#     interest-rates, que publica a tabela de formulas por categoria e a frase
#     "Different interest rates apply to underpayments and overpayments,
#     depending on whether you're an individual or a corporation."
#
#   As duas fontes BATEM nos quatro spreads: 3, 2, 0,5 e 5 pontos. E esses
#   spreads NAO mudam de trimestre — estao no codigo, nao no boletim.
#
# DESCARTADO, e por que: as TAXAS TRIMESTRAIS (o irs.gov publica 7%, 6%, 9% e
# 4,5% para 2026). Elas estao na mesma pagina e batem com a lei, mas mudam a
# cada trimestre com o federal short-term rate — citar a cifra e nascer com
# data de validade. O video manda a pessoa ler a taxa do trimestre dela na
# propria pagina do IRS. Diz onde, nao diz quanto.
#
# TAMBEM FORA: nao digo que a assimetria e ilegal, nem injusta, nem proposital.
# Digo o que a lei diz e deixo a leitura para quem assiste. E nao e orientacao
# fiscal: nao digo a ninguem para pagar menos, atrasar ou pedir restituicao.
#
# O NUMERO QUE DECIDE E DO ESPECTADOR: o valor dele e os dias dele. Ele pega a
# taxa do trimestre na fonte, multiplica pelo proprio valor e pelos proprios
# dias, e descobre quanto aquele dinheiro rendeu ou custou enquanto esteve
# parado do outro lado.
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
    # Predio do Tesouro dos EUA. Nao e enfeite patriotico: o federal
    # short-term rate que esta debaixo de tudo e determinado mensalmente pelo
    # Secretario do Tesouro sob a secao 1274(d), que e exatamente o que a cena
    # de abertura diz. 20 s para uma cena de 9,4 s.
    29188207: ("https://videos.pexels.com/video-files/29188207/12603662_1920_1080_30fps.mp4",
               "In Old News LLC",
               "https://www.pexels.com/video/us-treasury-building-in-washington-dc-29188207/"),
    # Alguem VIRANDO PAGINAS de um livro, sob a cena que diz que a secao e
    # curta o bastante para ler de uma vez. Rejeitei o 6964665 (close de
    # braille) e os dois de livro parado: a cena fala de LER, nao de ter. 17 s
    # para uma cena de 13,5 s.
    9198046: ("https://videos.pexels.com/video-files/9198046/9198046-hd_1920_1080_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/a-man-turning-pages-of-a-book-9198046/"),
    # Pessoa escrevendo no calendario, sob o capitulo da resposta, que manda
    # contar os dias entre duas datas. 17 s para uma cena de 12,3 s.
    5408798: ("https://videos.pexels.com/video-files/5408798/5408798-hd_1920_1080_30fps.mp4",
              "Leeloo The First",
              "https://www.pexels.com/video/a-person-writing-on-calendar-5408798/"),
    # Mao escrevendo no papel, no capitulo dos quatro passos. 21 s para 4,8 s.
    7428839: ("https://videos.pexels.com/video-files/7428839/7428839-hd_1366_720_25fps.mp4",
              "cottonbro studio",
              "https://www.pexels.com/video/person-writing-on-a-paper-7428839/"),
}


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
# A resposta — o espectador calcula o juro do proprio dinheiro — fecha no
# capitulo 3.

# -------------------------------------------------------------------- cap 1
B("One rate, five answers", "and only one of them is symmetric",
  "There is a single interest rate underneath federal tax interest, and it "
  "produces five different numbers. Which one you get depends on who you are.",
  "US Treasury building exterior", 29188207,
  cap="One rate, five answers")
T("Why this is worth knowing", "because money sits on both sides",
  "This matters because money sits on both sides of that line. Sometimes the "
  "government is holding yours, and sometimes you are holding the government's.")
T("The base rate", "determined monthly, not by the agency alone",
  "The base is called the federal short-term rate. It is determined every "
  "month under a separate section of the code, and then rounded to a whole number.")
T("Then points are added", "and the number of points is the whole story",
  "On top of that base, the code adds a fixed number of percentage points. "
  "That number of points is the entire story, and it is not the same for everyone.")
T("Four different spreads", "written in one section",
  "There are four different spreads written into one section of the code. "
  "They do not change from quarter to quarter, because they are not a rate.")
T("What does change", "the base, every quarter",
  "What changes every quarter is only the base. So the spreads are permanent "
  "and the published percentage is temporary, which is backwards from how people read it.")
T("And one number is yours", "the one on your own account",
  "And there is a number that no page will tell you: the interest on your own "
  "balance, for your own days. That is the one we are going to calculate.")

# -------------------------------------------------------------------- cap 2
B("What the code actually says", "section sixty six twenty one",
  "The section is numbered sixty six twenty one, and it is short enough to "
  "read in one sitting. It is worth reading because the numbers in it are not "
  "the ones that get reported. Here is what it sets, in plain order.",
  "person turning pages of a book", 9198046,
  cap="What the code actually says")
T("If the government owes you", "base plus three points",
  "If the government is holding an overpayment of yours, the rate is the base "
  "plus three percentage points. That is the general rule.")
T("Unless you are a corporation", "then base plus two",
  "Unless the overpayment belongs to a corporation. Then the code says two "
  "percentage points instead of three, in the same sentence.")
T("And on the large part", "half a point",
  "And for the part of a corporate overpayment above ten thousand dollars, "
  "the code substitutes half of one percentage point. Not two, and not three.")
T("If you owe the government", "base plus three, for everyone",
  "Now the other direction. If you owe, the rate is the base plus three "
  "percentage points, and the code sets that one the same for everyone.")
T("Except the largest underpayments", "base plus five",
  "Except for what the code calls a large corporate underpayment. There, five "
  "percentage points replaces three, after a date the code defines.")
T("Line them up", "and the asymmetry is visible",
  "Line those up and something becomes visible that no single number shows. "
  "The spread is not symmetric, and it is not symmetric in the same direction for everyone.")

# -------------------------------------------------------------------- cap 3
B("Now calculate yours", "three inputs, one multiplication",
  "Now your turn. You need three things to do this, and you already have two "
  "of them sitting in front of you right now. The third one takes a minute to "
  "look up, and I will tell you exactly where.",
  "writing dates on a calendar", 5408798,
  cap="Now calculate yours")
T("Input one", "the amount",
  "The first input is the amount. Either what you overpaid and have not been "
  "refunded yet, or what you owe and have not paid yet.")
T("Input two", "the days",
  "The second input is the number of days that amount has been sitting on the "
  "other side. Count from the date it was due to the date it moved.")
T("Input three", "the rate for your quarter",
  "The third input is the rate for the quarter you are in. Look that one up "
  "on the agency's own page, because it changes and I am not going to say it here.")
T("The multiplication", "amount times rate times days over a year",
  "Then multiply: your amount, times the rate as a decimal, times your days "
  "divided by three hundred sixty five. That is the simple version.")
T("That is your number", "and now you have something to compare",
  "That result is your number. Now you know what the waiting was actually "
  "worth, and the rest of this is only so you do not misread it.")
T("Write it next to the amount", "two figures, one line",
  "Write it on one line next to the amount itself. Those two figures together "
  "are the whole answer, and they will mean something next year too.")

# -------------------------------------------------------------------- cap 4
T("Why it compounds daily", "and why the simple version is low",
  "First refinement, and it is the one that explains most small mismatches: "
  "the real calculation compounds daily, not once at the end. So the simple "
  "multiplication you just did comes out slightly low, and predictably so.",
  cap="Why it compounds daily")
T("How much lower", "at these rates, not much",
  "At rates in this range and over a few months, the difference between simple "
  "and daily compounding is small. It matters more the longer the money sits.")
T("Why start simple anyway", "because it tells you the order of size",
  "Starting simple is still right, because what you needed first was the order "
  "of magnitude. Knowing whether it is dollars or hundreds decides what you do next.")
T("And the agency compounds", "so expect slightly more",
  "The agency's own computation compounds, so expect the official figure to "
  "come out slightly above your simple one. That direction is predictable.")
T("If yours is far off", "check days before you check rate",
  "If your number is far from theirs, check your day count before you suspect "
  "the rate. Day counting is where almost every mismatch comes from.")
T("Because the dates are defined", "not chosen",
  "And the dates are defined by rule, not by preference. When interest starts "
  "and stops is set, and it is rarely the date you remember.")
T("Which is the real lesson", "the clock is not yours to set",
  "That is the quieter lesson of this whole section. The amount may be yours, "
  "but the clock on it is defined somewhere else.")

# -------------------------------------------------------------------- cap 5
T("The part people misread", "and it is not the percentage",
  "Here is the part that gets misread most often, and it is not the "
  "percentage itself. It is what the percentage is attached to, and that "
  "confusion survives even among people who quote the figure correctly.",
  cap="The part people misread")
T("A spread is not a rate", "and the news reports the rate",
  "A spread is not a rate. When a figure is reported each quarter, that "
  "figure is already the base plus a spread, added together before anyone "
  "printed it.")
T("So the quarterly number moves", "while the rule does not",
  "So the quarterly number moves while the rule behind it sits perfectly "
  "still. Watching the quarterly number tells you nothing about the rule.")
T("And comparing quarters", "compares bases, not fairness",
  "Comparing one quarter's published percentage to another's compares two "
  "bases. It does not tell you anything about who the code treats how.")
T("The comparison that works", "same quarter, two categories",
  "The comparison that works is within one quarter, across two categories. "
  "That holds the base still and lets the spread show.")
T("Do that once", "and the structure appears",
  "Do that one comparison once, with any quarter's published table, and the "
  "structure appears immediately. You do not need history for it.")
T("And it will keep appearing", "because the spreads are in the code",
  "And it will keep appearing next quarter and the one after, because the "
  "spreads are in the code and the code is not reprinted quarterly.")

# -------------------------------------------------------------------- cap 6
T("What this does not mean", "and I am going to be exact",
  "Now the limits of what I just showed you, and I am going to be exact about "
  "them, because this is precisely where a video like this one usually "
  "overreaches and turns a reading into an accusation.",
  cap="What this does not mean")
T("Not a claim of illegality", "the code says what it says",
  "First: nothing here says that anything is illegal. The code sets these "
  "numbers openly and publishes them, and I am reading them out loud, not "
  "accusing anyone of anything.")
T("Not a claim about intent", "I do not know why",
  "Second: I am not telling you why the spreads differ. Legislative reasons "
  "exist in the record and they are not in this video.")
T("Not unfair by arithmetic", "a difference is not a verdict",
  "Third: a difference is not automatically unfair. Showing that two numbers "
  "differ is not the same thing as showing that one of them is wrong, and the "
  "step between those two claims is the whole argument.")
T("And not tax advice", "this is an arithmetic lesson",
  "Fourth: this is not tax advice. Nothing here tells you to pay late, pay "
  "early, or expect anything in particular from your own filing.")
T("What it is", "a reading of one section",
  "What it is, is a reading of one numbered section and a multiplication you "
  "can do on your own balance. That is the whole scope.")
T("And why that is enough", "because the number becomes yours",
  "And that scope is enough, because at the end the number in your hand is "
  "yours. You did not take it from a headline.")

# -------------------------------------------------------------------- cap 7
T("What I left out on purpose", "and this is the part usually skipped",
  "Now the part that usually gets skipped entirely. There are things that are "
  "deliberately missing from this video, and I am going to name each one and "
  "say why it is not here.",
  cap="What I left out on purpose")
T("No quarterly percentage", "not one",
  "First: I did not say a single quarterly percentage out loud. The agency "
  "publishes them, they are correct, and they are replaced every three months "
  "by a new set that is equally correct.")
T("Why that matters", "a cited rate ages badly",
  "A video that recites this quarter's percentage is wrong three months later "
  "and stays online anyway. The spreads do not have that problem.")
T("No dollar thresholds beyond one", "and that one is in the statute",
  "Second: the only dollar figure I used is the ten thousand dollar threshold, "
  "and that one is written in the statute itself, not in a quarterly notice.")
T("No state interest", "this is federal only",
  "Third: none of this covers state tax interest. States set their own, and "
  "they are not what this section governs.")
T("No penalty rates", "interest and penalties are different",
  "Fourth: interest is not the same thing as penalties. They are computed "
  "separately under different sections, and this video is only about the "
  "interest side of it.")
T("And nothing about your case", "I have not seen your account",
  "And fifth: nothing here evaluates your situation. I have not seen your "
  "account and I cannot tell you what your dates are.")

# -------------------------------------------------------------------- cap 8
B("Four steps", "start to finish",
  "Here is the whole check in four steps, so you can do it after this ends.",
  "hand writing on paper", 7428839,
  cap="Four steps")
T("Step one", "write the amount and the two dates",
  "Step one: write down the amount, the date it was due, and the date it "
  "actually moved. Three items, on paper.")
T("Step two", "count the days between them",
  "Step two: count the days between those two dates. Count them, do not "
  "estimate them in months, because months are not equal.")
T("Step three", "look up your quarter on the agency page",
  "Step three: open the agency's quarterly interest page and find the "
  "category and quarter that match you. Read the percentage from there.")
T("Step four", "multiply and write it down",
  "Step four: multiply amount, by rate, by days over three hundred sixty "
  "five. Write the result next to the amount, on the same line.")
T("Then the comparison", "same quarter, other category",
  "Then do one comparison: in that same quarter's table, read the category "
  "that is not yours. The gap between them is the spread you just learned about.")
T("Repeat it next year", "and the line becomes a record",
  "Repeat this next year on the same sheet. Two lines tell you more than one, "
  "because the base will have moved and the spread will not have.")
T("And one note", "if you have no dates, that is step zero",
  "One last note: if you cannot find the dates, that is not a dead end. That "
  "is your actual first step, and it comes before any arithmetic.")

C("Comment the spread, not your balance", "two points, not two dollars",
  "In the comments, post only the gap in percentage points between two "
  "categories in one quarter. Do not post your balance or your dates.")

THUMB = {"l1": "One rate", "l2": "five answers"}


SHORT = [
    {"layout": "titulo", "kicker": "One rate, five answers",
     "sub": "and the spread is in the code",
     "nar": "Federal tax interest is one base rate plus a fixed spread. The "
            "spread is not the same for everyone.", "sem_cap": True},
    {"layout": "titulo", "kicker": "One", "sub": "owed to you: three points",
     "nar": "One: if the government holds your overpayment, the code adds "
            "three percentage points.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Two", "sub": "a corporation: two points",
     "nar": "Two: for a corporation's overpayment it adds two, and above ten "
            "thousand dollars, half of one.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Three", "sub": "owing: three, or five",
     "nar": "Three: if you owe, it adds three for everyone, but five for a "
            "large corporate underpayment.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Now yours", "sub": "amount, days, rate",
     "nar": "Take your amount, your days, and this quarter's rate from the "
            "agency page. Multiply. That is your number.", "sem_cap": True},
]


COPY = """# next-level-money-010

## TITULO
IRS Code 6621: You Get 3 Points Both Ways, a Corporation Does Not

## TITULO SHORT
IRS 6621: 3 points both ways

## DESCRICAO
Federal tax interest is not one number. Underneath it there is a single base —
the federal short-term rate, determined monthly — and on top of that base the
Internal Revenue Code adds a fixed number of percentage points. That number of
points is the whole story, and it is not the same for everyone.

Section 6621 of Title 26 sets four different spreads. If the government is
holding an overpayment of yours, the rate is the base plus three percentage
points — "2 percentage points in the case of a corporation", in the statute's
own words. For the part of a corporate overpayment above ten thousand dollars,
the code substitutes half of one percentage point. In the other direction, if
you owe, the rate is the base plus three percentage points for everyone — except
for what the code calls a large corporate underpayment, where five percentage
points replaces three.

Line those up and the asymmetry is visible: an individual is charged and paid at
the same spread, and a corporation is not.

This video does not quote a single quarterly percentage, and that is
deliberate. The published percentages are correct and they change every three
months, so a video that recites them is wrong by the next quarter and stays
online anyway. The spreads do not have that problem, because they are in the
code and the code is not reprinted quarterly. What you are shown instead is
where to read your own quarter's rate, and how to use it.

The number that decides is yours: your amount, your days. Take what you
overpaid and have not been refunded, or what you owe and have not paid, count
the days it has been sitting on the other side, read the rate for your quarter
and category from the agency's own page, and multiply amount by rate by days
over three hundred sixty five. The real computation compounds daily, so expect
the official figure to come out slightly above your simple one — and if yours
is far off, check your day count before you suspect the rate.

What this video does not say: it does not claim anything here is illegal, it
does not explain why the spreads differ, it does not call the difference unfair,
and it is not tax advice. It also leaves out state tax interest and penalties,
which are governed separately.

Sources, and they agree: 26 U.S.C. 6621 as published by the U.S. Government
Publishing Office, and the Internal Revenue Service's own quarterly interest
rates page, which states that different rates apply to underpayments and
overpayments depending on whether you are an individual or a corporation.

Chapters:
00:00 One rate, five answers
01:07 What the code actually says
02:14 Now calculate yours
03:21 Why it compounds daily
04:28 The part people misread
05:35 What this does not mean
06:42 What I left out on purpose
07:49 Four steps

In the comments, post only the gap in percentage points between two categories
in one quarter — not your balance and not your dates.

## DISCLOSURE
The narration and visuals in this video were produced with artificial
intelligence. The rules described are quoted from the statute and from the
administering agency, both linked above.

## HASHTAGS
#TaxInterest #IRS #PersonalFinance

## TAGS
irs interest rate, section 6621, federal short term rate, overpayment interest, underpayment interest, large corporate underpayment, how irs interest is calculated, tax refund interest, quarterly interest rates irs, title 26 section 6621, irs interest formula, daily compounding interest tax, corporate overpayment rate, tax interest explained, calculate irs interest

## COMENTARIO FIXADO
Four steps: write the amount and the two dates → count the days between them →
read your quarter and category on the agency's quarterly interest page →
multiply amount by rate by days over three hundred sixty five. Then read the
category that is not yours in that same quarter: the gap is the spread. Post
only that gap, not your balance.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/next-level-money-010.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "next-level-money",
    "pacote": "next-level-money-010",
    "idioma": "en",
    "voz": "en-US-AndrewNeural",
    "trilha": "Deliberate_Thought",
    "paleta": {"ink": "#16202B", "c1": "#9A3412", "c2": "#115E59", "bg": "#F5F3EE"},
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
    grava(SPEC, "fabrica/specs/next-level-money-010.json")
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
