#!/usr/bin/env python3
"""Monta a spec next-level-money-005.

POR QUE ESTE CANAL, E O QUE O VEREDITO MUDA

Primeiro da fila que produz (ultimo pacote 18/08 08:34). E o veredito da
v_maquina_licoes e `canal frio`: short com mediana de 2,52 views/dia e topo de
6,59 — nenhum dos dois formatos pegou, e nunca houve pico. A instrucao que vem
com esse veredito nao e trocar de formato, e outra: o problema esta no gancho
ou no nicho, entao nao repita o angulo do que ja foi ao ar aqui, porque ele foi
medido e nao pegou.

O canal tem CINCO titulos distintos no ar, em tres eixos: economia historica
(Dutch East India, $7.9 Trillion Myth), divida de cartao (Minimum Payment Math)
e bureaus de credito (You Are the Product). Nenhum passou de 6,59 v/d.

O NICHO, medido: `divida de cartao / recorde` domina com DEZ outliers — 27.490,
11.136, 8.050, 6.673, 5.116, 2.849, 2.165, 1.290, 1.086 e 1.049 v/d. O eixo de
economia historica que o canal mais publicou nao aparece na medicao.

Ou seja: o canal vinha publicando o eixo errado. Isso e exatamente o que o
veredito `canal frio` diz quando diz "o problema e o gancho ou o nicho".

O eixo de cartao JA foi usado uma vez pelo canal. Entao o inedito aqui e o
ANGULO, e ele e o oposto do anterior — a similaridade contra o acervo do canal
ficou em 0,340, teto 0,65.

A DOR DATADA, e por que ela e boa

Federal Reserve Bank of New York, Household Debt and Credit Report do segundo
trimestre de 2026, divulgado em 11 de agosto de 2026:

  - saldo de cartao de credito subiu 21 bilhoes, para 1,26 trilhao de dolares
  - divida total das familias CAIU 13 bilhoes (-0,1%), para 18,8 trilhoes
  - inadimplencia geral em 4,7% do saldo, 0,1 ponto ABAIXO do trimestre anterior
  - 12,8% do saldo de cartao esta ha 90 dias ou mais sem pagamento

O 12,8% foi o numero que circulou como crise. E os proprios pesquisadores do
Fed avisaram para NAO ler assim: ele reflete um acumulo de dividas ja baixadas
como perda que continuam aparecendo no relatorio de credito — 80% dos saldos
baixados seguem visiveis UM ANO depois da baixa.

O GIRO. O numero mais assustador do relatorio e, em boa parte, contabilidade. E
quem disse isso foi quem publicou o numero.

O QUE ESTE ROTEIRO NAO FAZ, e isso importa num canal de dinheiro: ele NAO diz
que a divida das familias esta bem. O capitulo 5 existe so para segurar as duas
verdades juntas — o 12,8% esta inflado E 1,26 trilhao com 4,7% inadimplente e
real. Minimizar divida seria o erro simetrico de alarmar, e num canal que fala
de dinheiro os dois custam caro.

TAXA DA VOZ. en-US-AndrewNeural: R = 16,0 chars/s, P = 0,119 s/frase — o P mais
baixo da frota, esta voz quase nao pausa entre frases, e por isso o orcamento e
enorme. Densidade do canal: 2,67 frases/cena no longo, 2,20 no short.
Orcamento: 78 cenas em 810 s = 12.193 caracteres, 156 por cena. Short: 525
caracteres em 6 cenas.

CAPITULOS abrem sempre em layout `titulo` (aprendizado 388).
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


# ------------------------------------------------ 1. The number everyone quoted
T("Twelve point eight", "per cent",
  "On the eleventh of August, the New York Fed published its quarterly report "
  "on household debt. One figure in it travelled further than all the others. "
  "Twelve point eight per cent of credit card balances were ninety days or more "
  "without payment.",
  cap="The number everyone quoted")
T("That got read", "as a crisis",
  "That got read as a crisis number, and you can see why. Nearly one dollar in "
  "eight, sitting unpaid for a quarter of a year.")
I("But the Fed's own researchers", "said not to read it that way",
  "Except the Fed's own researchers attached a caution to it. They said that "
  "figure does not show a broad deterioration in how people are paying their "
  "bills right now.")
T("That is unusual", "and worth stopping on",
  "That is an unusual thing for a statistical agency to do. Publish a number, "
  "and in the same breath tell you how not to read it.")
T("So either", "they are downplaying it",
  "So one of two things is happening. Either they are softening bad news.")
I("Or the number", "measures something else",
  "Or the number is measuring something slightly different from what everyone "
  "assumed it measured. This video is about which one it is.")
T("Spoiler", "it is the second",
  "It is the second one, and the mechanism is genuinely worth understanding, "
  "because it will distort this same statistic every quarter from now on.")
L("Three parts", ["What charged off means",
                  "Why old debt stays visible",
                  "What the same report actually said"],
  "Three parts. What it means when a debt is charged off. Why that debt keeps "
  "showing up long afterwards. And what the rest of that report said, which "
  "almost nobody quoted.")
T("One promise", "this is not a debt is fine video",
  "One promise before we start. This is not a video arguing that household debt "
  "is fine. It is not, and I will show you the numbers that say so.")
I("It is a video", "about one statistic",
  "It is a video about one statistic being widely misread, which is a different "
  "claim, and a much narrower one.")
C("Start with the accounting", "because that is where it comes from",
  "Start with the accounting, because that is where the whole distortion is born.")

# ---------------------------------------------- 2. What charged off actually means
T("A bank does not wait", "forever",
  "When you stop paying a credit card, the bank does not wait indefinitely to "
  "find out how it ends. At a certain point it has to make a decision about "
  "its own books.",
  cap="What charged off actually means")
I("Around one hundred", "and eighty days",
  "In the United States that point is generally around one hundred and eighty "
  "days past due for revolving credit. At that stage the balance is charged off.")
T("Charged off", "does not mean forgiven",
  "And here is the first thing almost everyone gets wrong. Charged off does not "
  "mean forgiven, cancelled, or gone.")
I("It is an accounting move", "on the bank's side",
  "It is an accounting move on the bank's side. The bank stops carrying the "
  "balance as an asset it expects to collect, and books the loss.")
T("You still owe it", "entirely",
  "You still owe the money. Entirely. The debt can still be collected, sold to "
  "a collection agency, or pursued in court.")
T("So one event", "produces two different records",
  "So a single event produces two very different records. The bank's books say "
  "the loss is taken. Your credit report says the debt is unpaid.")
I("And the report", "is where the statistic comes from",
  "And it is the credit report side that feeds this statistic. The New York Fed "
  "builds this data from a large sample of consumer credit records.")
T("Which means", "the question becomes how long",
  "Which means the entire question becomes: how long does a charged off debt "
  "keep appearing on a credit report after the charge off?")
T("If it disappeared quickly", "there would be no distortion",
  "If it vanished quickly, there would be no distortion at all. The statistic "
  "would track current behaviour, quarter by quarter.")
I("It does not vanish quickly", "and that is the whole story",
  "It does not vanish quickly. And the Fed put a number on exactly how slowly, "
  "which is the piece that makes this readable.")
C("That number", "is the next part",
  "That number is the next part, and it is larger than most people would guess.")

# ------------------------------------------------ 3. Eighty per cent, one year on
T("Eighty per cent", "a full year later",
  "According to the New York Fed's researchers, eighty per cent of charged off "
  "balances are still visible on credit reports a full year after being written "
  "off.",
  cap="Eighty per cent, one year on")
T("Sit with that", "for a second",
  "Sit with that for a second, because it does all the work in this episode.")
I("A debt from last summer", "is in this summer's number",
  "A card balance that went bad last summer, and was charged off months ago, is "
  "very likely still inside the figure published this month.")
T("It is not being counted twice", "in the balance",
  "It is not being double counted in the dollar balance. But it is being "
  "counted again in the share that is ninety days or more delinquent.")
T("Because that share", "is a stock, not a flow",
  "Because that share is a stock, not a flow. It measures how much delinquent "
  "debt is sitting there, not how much became delinquent this quarter.")
L("Two different questions", ["How many people fell behind recently",
                              "How much old bad debt is still listed"],
  "Those are two different questions. How many people fell behind recently. And "
  "how much old bad debt is still sitting on the books.")
I("The headline number", "answers the second",
  "The twelve point eight per cent figure answers the second question, and gets "
  "reported as if it answered the first.")
T("And the backlog", "only clears slowly",
  "And because the backlog clears slowly, that share can stay high, or even "
  "rise, in a quarter when fewer people are actually falling behind.")
T("Which is precisely", "what the Fed was flagging",
  "Which is precisely what the Fed's researchers were flagging. Not that the "
  "number is wrong. That it answers a different question than the one being asked.")
I("The measure that answers", "the first question",
  "The measure that does answer the first question is the transition rate — how "
  "much debt moved into delinquency this quarter. And that one held steady.")
C("Now the rest of the report", "which nobody quoted",
  "Now the rest of that report, which almost nobody put in a headline.")

# ------------------------------------------- 4. What the same report actually said
T("Total household debt", "went down",
  "Here is the sentence that led the New York Fed's own press release, and that "
  "I did not see in a single thumbnail. Total household debt decreased in the "
  "second quarter. It fell by thirteen billion dollars. That is about one tenth "
  "of one per cent, and it leaves the total at eighteen point eight trillion.",
  cap="What the same report actually said")
I("Overall delinquency", "four point seven per cent",
  "Overall delinquency also moved the friendly way. As of the end of June, four "
  "point seven per cent of all outstanding household debt was in some stage of "
  "delinquency, down a tenth of a point from the quarter before. Small, but the "
  "sign matters as much as the size.")
T("And the transition rates", "held steady",
  "And the rate at which debt was newly moving into delinquency held steady. "
  "Not improving dramatically, not deteriorating. Flat. Which, after several "
  "years of headlines about a coming wave, is itself information.")
I("Meanwhile cards", "rose twenty one billion",
  "Against all that, credit card balances did rise. Up twenty one billion "
  "dollars, to one point two six trillion. That part of the scary story is "
  "entirely true, and I am not going to soften it.")
T("So the report says", "three things at once",
  "So a single report said three things at once. Total debt down slightly. "
  "Delinquency down slightly. Card balances up. And a delinquency share that "
  "looks alarming for accounting reasons.")
T("Guess which one", "became the story",
  "Guess which of those four became the story. The one that sounded worst, and "
  "the one the publishing agency specifically asked people to interpret "
  "carefully.")
I("That is not a conspiracy", "it is selection",
  "That is not a conspiracy, and I do not think anyone lied. It is selection. "
  "A number that sounds like a crisis travels further than one that sounds like "
  "a rounding error, and every outlet is choosing under the same pressure.")
T("But the effect", "is a distorted picture",
  "The effect, though, is a picture of American household finances that is "
  "meaningfully darker than the data that produced it. And that has costs, "
  "because people make decisions on it.")
L("What actually moved", ["Total debt: down 0.1%",
                          "Delinquency: down 0.1 point",
                          "Card balances: up $21bn"],
  "So here is the quarter in three lines. Total debt down a tenth of a per cent. "
  "Delinquency down a tenth of a point. Card balances up twenty one billion.")
T("None of those", "is dramatic",
  "None of those is dramatic in either direction. Which is, I think, the real "
  "finding of this report, and the reason it produced no memorable headline.")
C("Now the harder part", "holding both truths",
  "Now the harder part, and the reason I am being careful here.")

# ------------------------------------------------------ 5. Both things are true
T("The correction", "is not the opposite claim",
  "There is a trap in videos like this one, and I want to walk into it "
  "deliberately rather than pretend it is not there. When you correct an "
  "alarming number, it is very easy to slide into arguing the opposite. That "
  "would be just as wrong, and more comfortable to watch.",
  cap="Both things are true")
I("One point two six trillion", "is real money",
  "One point two six trillion dollars in revolving credit card debt is real, it "
  "is at a record level in nominal terms, and it is carried at interest rates "
  "that have stayed high. None of that is an accounting artefact.")
T("Four point seven per cent", "is millions of households",
  "Four point seven per cent of eighteen point eight trillion dollars in some "
  "stage of delinquency is not a small number of households. It is a very large "
  "number of households, and the fact that it ticked down a tenth of a point "
  "does not change their situation this month.")
T("So what exactly", "did we correct",
  "So what did we actually correct? Something narrow, and worth stating "
  "precisely, because precision is the entire point of the exercise.")
I("We corrected", "one statistic's meaning",
  "We corrected the meaning of one statistic. Twelve point eight per cent does "
  "not mean that nearly one in eight card dollars just went bad. It means that "
  "share of balances is currently carrying a delinquency flag, including old "
  "debt already written off.")
T("What we did not correct", "the level of debt",
  "What we did not correct is the level of debt, the cost of carrying it, or "
  "whether any individual household is in trouble. Those questions are "
  "untouched by anything in this video.")
T("Both readings fail", "in opposite directions",
  "Read only the twelve point eight, and you conclude a collapse is underway. "
  "Read only the corrections, and you conclude everything is fine. Both of those "
  "are wrong, and the second one is the more expensive mistake to make with "
  "your own money.")
I("The accurate summary", "is boring",
  "The accurate summary is boring, and boring is usually what accurate sounds "
  "like. Debt is high, expensive, and roughly stable. Nothing broke this "
  "quarter, and nothing got fixed either.")
T("Boring does not trend", "and that is the problem",
  "Boring does not trend. Which is why you will keep seeing the alarming version "
  "of this number, quarter after quarter, and why knowing the mechanism is worth "
  "the twelve minutes.")
T("Because the mechanism", "does not expire",
  "The mechanism does not expire. The backlog will still be there next quarter, "
  "and the quarter after, distorting the same statistic in the same direction.")
C("So let us make it usable", "for the next release",
  "So let us make this usable. Here is how I would read the next one.")

# ------------------------------------------------ 6. How to read the next release
T("It is quarterly", "and the calendar is public",
  "This report comes out once a quarter, and the New York Fed announces the "
  "release date in advance. That alone puts you ahead of most commentary, "
  "because you can read the source on the morning it lands instead of reading "
  "what somebody made of it a day later.",
  cap="How to read the next release")
L("Four numbers", ["Total household debt",
                   "Overall delinquency share",
                   "Transition into delinquency",
                   "Card balance change"],
  "Four numbers, and they take about two minutes. Total household debt and "
  "which way it moved. The overall delinquency share. The transition rate into "
  "delinquency. And the change in card balances.")
I("The transition rate", "is the one to weight",
  "If you only have time for one, take the transition rate. It measures what "
  "moved into delinquency during the quarter, so it responds to what is "
  "happening now rather than to what happened a year ago and is still listed.")
T("The ninety day share", "is the one to discount",
  "And the ninety day or more share is the one to hold most loosely, because "
  "you now know it carries a backlog that clears slowly and drags the level "
  "upward independently of current behaviour.")
T("That is not a trick", "the Fed publishes both",
  "This is not some clever trick. The Fed publishes both, clearly, in the same "
  "document. The distortion happens entirely downstream, in which one gets "
  "picked up.")
I("Compare quarters", "not headlines",
  "Compare the same measure across quarters rather than comparing this "
  "quarter's headline to last quarter's headline. Headlines are written by "
  "different people making different choices about which line to lead with.")
T("And watch the direction", "more than the level",
  "Watch the direction more than the level. A level tells you where things "
  "stand and needs enormous context to interpret. A direction tells you what "
  "changed, and needs almost none.")
T("If you take one habit", "take that one",
  "If you take a single habit from this video, take that one. It generalises "
  "far beyond credit card statistics, and it costs you nothing to apply.")
I("The report is free", "and it is the source",
  "The report is free, published openly, and it is the source that every "
  "article you have read this month is built on. Everything downstream is "
  "somebody's summary of it.")
T("I will link it", "below",
  "It is linked below, along with the specific release these figures come from, "
  "so you can check every number I have said against the original.")
C("Last section", "the limits of all this",
  "Last section, and it is the one I would want if I were watching.")

# ----------------------------------------------- 7. What this does not tell you
T("It does not tell you", "about your own debt",
  "None of this tells you anything about your own situation. These are national "
  "aggregates built from a sample of credit records, and an aggregate that "
  "improves by a tenth of a point can sit on top of a household whose position "
  "got dramatically worse this quarter.",
  cap="What this does not tell you")
I("It is not a forecast", "of anything",
  "It is also not a forecast. The report describes a quarter that has already "
  "finished. Anyone using it to tell you what happens in the next six months is "
  "adding their own model on top, and should say so.")
T("The eighty per cent figure", "is about visibility",
  "The eighty per cent figure describes how long charged off balances stay "
  "visible on credit reports. It does not tell you how much of that debt is "
  "still being actively collected, or how much is realistically recoverable.")
I("And it is a sample", "not a census",
  "And the underlying panel is a large sample of credit records, not a census "
  "of every American. It is the best series available for this question, which "
  "is a different claim from being complete.")
T("What I have not claimed", "matters as much",
  "Let me be explicit about what I have not claimed, because in a video that "
  "corrects an alarming number, silence gets read as agreement.")
L("Not claimed", ["That debt is at a safe level",
                  "That delinquency is falling meaningfully",
                  "That anyone is exaggerating on purpose"],
  "I have not claimed that debt is at a safe level. I have not claimed "
  "delinquency is meaningfully falling. And I have not claimed anybody is "
  "exaggerating deliberately.")
T("What I have claimed", "is one thing",
  "I have claimed one thing. That a specific statistic is being read as a "
  "measure of current behaviour when it is substantially a measure of "
  "accumulated history, and that the institution publishing it said so first.")
I("If that is right", "the habit follows",
  "If that is right, then the habit follows automatically. Read the transition "
  "rate. Discount the stock. Check the direction. Two minutes, once a quarter.")
T("And if I am wrong", "tell me with the number",
  "And if you think I have this wrong, the report is linked and the figures are "
  "in it. Tell me which number I have misread, and I will correct it on the "
  "channel rather than quietly.")
T("Next video", "the collections side",
  "In the next video I want to follow the debt after the charge off. Who buys "
  "it, for how much on the dollar, and what that price implies about how much "
  "of it anyone expects to collect.")
I("Because that price", "is an honest estimate",
  "Because the price a collector pays for a portfolio is the most honest "
  "estimate anyone makes of what that debt is really worth. Nobody is "
  "posturing when their own money is on the line.")
C("See you there", "and read the source",
  "See you there. And whatever else you take from this, read the source before "
  "the summary.")

# ---------------------------------------------------------------- the short
# Opens on the anomaly — an agency telling people not to read its own number.
# Budget measured for 35,9 s with 6 scenes at 2,20 sentences each: 525 chars.
SHORT = [
    {"layout": "titulo", "kicker": "The Fed published", "sub": "and then warned",
     "nar": "The New York Fed published a number this month, and then warned "
            "people not to read it the way everyone read it.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Twelve point eight", "sub": "per cent of card balances",
     "nar": "Twelve point eight per cent of credit card balances, ninety days or "
            "more without payment.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Sounds like", "sub": "a collapse",
     "nar": "That sounds like a collapse in how people are paying. It mostly is "
            "not.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Charged off", "sub": "is not gone",
     "nar": "When a bank writes a debt off, it stays on your credit report. "
            "Eighty per cent of it is still there a year later.", "sem_cap": True},
    {"layout": "titulo", "kicker": "So the share", "sub": "carries old debt",
     "nar": "So that share is a backlog, not this quarter's behaviour. The Fed "
            "said so itself.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Which number", "sub": "to read instead",
     "nar": "Which number you should read instead is on the channel.",
     "sem_cap": True},
]

THUMB = {"l1": "12.8% delinquent?", "l2": "the Fed said read it again"}

COPY = """# The delinquency share is a backlog, not this quarter's behaviour

## TITULO
Delinquency Hit 12.8%: Why the Fed Told Everyone Not to Read It That Way

## DESCRICAO
On 11 August 2026 the Federal Reserve Bank of New York published its Household Debt and Credit Report for the second quarter. One figure travelled further than the rest: 12.8% of credit card balances were ninety days or more without payment. It was widely reported as evidence that American households are collapsing under card debt.

The Fed's own researchers attached a caution to that figure. They said it reflects a backlog of old charged-off debts still sitting on credit reports, rather than a broad deterioration in how consumers are currently repaying — noting that 80% of charged-off balances remain visible on credit reports a full year after being written off.

This video is about why that happens, and what to read instead.

When a revolving credit balance goes unpaid — generally around 180 days past due in the US — the bank charges it off. That is an accounting decision on the lender's side: it stops carrying the balance as an asset it expects to collect. It does not mean the debt is forgiven, cancelled or gone. You still owe it, it can still be collected or sold, and critically, it stays on your credit report. Because this statistic is built from consumer credit records, charged-off debt from previous quarters keeps counting inside the "90+ days delinquent" share long after the event that produced it.

That makes the figure a stock, not a flow. It measures how much delinquent debt is currently sitting there, not how much became delinquent this quarter. The measure that answers the second question is the transition rate into delinquency — and that one held steady.

What else the same report said, and almost nobody quoted: total household debt decreased by $13 billion (‑0.1%) to $18.8 trillion; overall delinquency stood at 4.7% of outstanding balances, down 0.1 percentage points from the prior quarter; and credit card balances rose by $21 billion to $1.26 trillion.

This video does not argue that household debt is fine. $1.26 trillion in revolving debt at high interest rates is real, and 4.7% of $18.8 trillion in some stage of delinquency is a very large number of households. The correction here is narrow and specific: one statistic is being read as current behaviour when it is substantially accumulated history. Both readings — collapse, and everything-is-fine — are wrong, and the second is the more expensive mistake to make with your own money.

Ends with a two-minute routine for reading the next quarterly release, and an explicit list of what this analysis does not tell you.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
A genuine question for anyone who works in collections, underwriting or credit reporting: is the 80% one-year visibility figure consistent with what you see day to day, or does it vary a lot by lender and by how quickly portfolios get sold on? That is the one part of this I could not check against anything except the Fed's own note.

## HASHTAGS
#CreditCardDebt #FederalReserve #NextLevelMoney

## TAGS
credit card debt, new york fed, household debt report, delinquency rate, charged off debt, credit report, consumer credit, personal finance, us economy, debt statistics, charge off, collections, credit score, economic data, financial literacy

## CONFIGURACAO DE STUDIO
- Language: English (en-US) | Category: Education (27)
- Not made for kids
- Altered or synthetic content disclosure: YES (AI-generated voice)
- Location: United States | Licence: Standard YouTube Licence
- Mid-roll ads: on (runtime over eight minutes)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
All figures are from the Federal Reserve Bank of New York's Household Debt and Credit Report for Q2 2026, released 11 August 2026, and its accompanying press release: total household debt down $13 billion (‑0.1%) to $18.8 trillion; credit card balances up $21 billion to $1.26 trillion; 4.7% of outstanding debt in some stage of delinquency as of the end of June, down 0.1 percentage points; and 12.8% of card balances 90 or more days without payment. The caution that this last figure reflects a backlog of charged-off debts rather than broad current deterioration, and the finding that 80% of charged-off balances remain visible on credit reports one year after write-off, are the New York Fed researchers' own, published alongside the data. Accessed 20 August 2026. The 180-day charge-off convention is the standard US practice for revolving credit and is stated as such, not as a figure from this report. The underlying data is the New York Fed Consumer Credit Panel, a large sample of anonymised credit records — not a census. This video makes no forecast, describes no individual household, and is not financial advice.
"""

SPEC = {
    "slug": "next-level-money",
    "pacote": "next-level-money-005",
    "idioma": "en",
    "voz": "en-US-AndrewNeural",
    "trilha": "Deliberate_Thought",
    "paleta": {"ink": "#1A1A1A", "c1": "#E4572E", "c2": "#F2B134", "bg": "#F2ECDF"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "next-level-money-005.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
