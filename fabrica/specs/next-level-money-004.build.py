#!/usr/bin/env python3
"""Monta a spec next-level-money-004.

EIXO. Primeira medicao do nicho (18/08/2026, 45 videos de 90 dias, em
pautas_banco): mediana 84,3 v/d — nicho de cauda pesadissima: 18 outliers
>=3x, e DEZ deles sao o MESMO assunto: divida de cartao em recorde. PBS
NewsHour 27.490 v/d, Bordenaro 11.136, Minhaj (short) 8.050, "$1.26T CREDIT
CARD TRAP" 5.116. Dor datada de UMA SEMANA: o relatorio trimestral do NY Fed
saiu em 11/08. Achado negativo: o cluster "why groceries are expensive" esta
MORTO (0,3 a 2,4 v/d na cauda) — nao tocar.

O canal ja usou: historia economica (VOC), credito como produto de dados
("You Are the Product"), custo de delivery. O eixo do RECORDE e da mecanica
do pagamento minimo esta intocado — e e o que o noticiario nao faz: PBS e
ABC dao o numero; ninguem faz a aritmetica de para onde vai o primeiro
pagamento.

NUMEROS, bloco unico e primario (NY Fed, Quarterly Report on Household Debt
and Credit, 11/08/2026; ecoado por CNBC, ABC, Yahoo Finance; complementos
LendingTree/US News):
    cartao: US$ 1,26 tri no Q2/2026 (+US$ 21 bi no trimestre)
    pico historico: US$ 1,28 tri (Q4/2025)
    fatia dos saldos 90+ dias sem pagamento: 7,6% (meados de 2022) -> 12,8%
    ~175 milhoes de americanos com cartao; ~60% nao quitam o mes
    APR medio ~21%; pesquisadores do proprio Fed falam em economia em K

A CONTA DA CASA (aritmetica ilustrativa, declarada como tal na copy): saldo
de US$ 5.000 a 21% ao ano gera US$ 87,50 de juros por mes. O minimo tipico
de 2% e US$ 100. Ou seja: dos primeiros cem dolares pagos, oitenta e sete e
cinquenta sao juros — doze e cinquenta tocam a divida. O video mostra por
que o minimo e desenhado assim, e fecha com a planilha de seis linhas que
transforma o saldo do espectador na resposta dele.

VOZ. en-US-AndrewNeural (16,50 chars/s, P=0,101) — calibracao de PRODUCAO,
n=142. P quase nulo: os chars dominam; ~12 mil chars para ~13 min.
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


# ------------------------------------------------------------------- cap 1
T("Two numbers", "from the same week",
  "One point two six trillion dollars. And eighty seven dollars fifty. The "
  "first made every headline last week. The second explains it, and almost "
  "nobody says it out loud.",
  cap="The two numbers")
I("The first", "the New York Fed's count",
  "The first is the New York Fed's official count of America's credit card "
  "debt. One point two six trillion dollars, as of the second quarter.")
I("The second", "inside a minimum payment",
  "The second is what happens inside one ordinary minimum payment on a five "
  "thousand dollar balance. We will get there, and it will explain more than "
  "the trillion does.")
I("This is not a lecture", "it is a machine",
  "This video is not a lecture about spending less. It is a tour of a "
  "machine — a beautifully engineered one — and the maths it runs on.")
I("Why this matters now", "the report is a week old",
  "Why now? Because the Fed's quarterly report landed a week ago, every "
  "outlet quoted the trillion, and every one of them stopped exactly where "
  "the interesting part begins.")
I("The news tells you the size", "we do the mechanism",
  "The news tells you the size of the lake. This channel is about the "
  "plumbing — where the water comes in, and why the drain is built so "
  "narrow.")
T("The claim", "the minimum is the product",
  "Here is the claim we will test with arithmetic: the minimum payment is "
  "not a safety feature. It is the product.")
L("The route", ["The record, in context", "The delinquency curve",
                "The minimum payment machine", "Why twenty one percent",
                "Your six-line sheet"],
  "Five stops. The record and what sits inside it. The delinquency curve. "
  "The minimum payment machine itself. Why the interest rate is what it is. "
  "And the sheet that turns your own balance into your own answer.")
I("One promise", "every number has an owner",
  "One promise before we start. Every number here has an owner and a date — "
  "most of them from the Fed's own quarterly report, published August the "
  "eleventh.")
I("And one warning", "the examples are examples",
  "And one warning. The five thousand dollar balance we will use is an "
  "illustration. The method is the point — you will run it on your own "
  "numbers at the end.")
I("Start", "with the record",
  "Start with the record, because the trillion is not the interesting part:")

# ------------------------------------------------------------------- cap 2
T("The record", "and what it hides",
  "One point two six trillion. Up twenty one billion in a single quarter. "
  "Just short of the all time peak of one point two eight trillion.",
  cap="The record, in context")
I("Who holds it", "175 million people",
  "Who holds it? About one hundred and seventy five million Americans have "
  "at least one credit card.")
I("The split that matters", "sixty percent carry",
  "And the split that matters: roughly sixty percent of them do not pay the "
  "balance off each month. They carry it, and the interest meter runs.")
B("Two Americas", ["Pay in full", "Carry a balance"], [67, 100],
  "That is the real headline. Two groups using the same product. For one it "
  "is a payments tool with rewards. For the other it is the most expensive "
  "loan they will ever hold.")
I("Scale check", "per carrying household",
  "Do the scale check yourself. A trillion and a quarter, spread over the "
  "carrying minority, lands in the thousands per household — not a rounding "
  "error in anyone's budget.")
I("And it grew", "twenty one billion in ninety days",
  "And it grew by twenty one billion dollars in ninety days. That is the "
  "speed of the gap between paychecks and prices, measured quarterly.")
I("Near the peak", "and climbing back",
  "The all time peak was set just two quarters ago. After a brief dip, the "
  "balance is climbing straight back toward it. Records here do not stand "
  "for long.")
I("The Fed's own phrase", "a K-shaped economy",
  "The Fed's own researchers describe it as a K-shaped economy. One arm of "
  "the K rising, one falling, both holding the same piece of plastic.")
I("And the trillion", "is the falling arm's bill",
  "And the trillion is mostly the falling arm's bill. Money already spent — "
  "on groceries, on repairs, on months where the paycheck ran out early.")
I("Which is why", "the record keeps records",
  "Which is why this record keeps breaking. It is not a shopping spree. It "
  "is a gap between income and life, financed at card rates.")
T("Bridge", "and the cracks show",
  "And when a gap is financed at card rates, the cracks show up in one "
  "specific statistic. That is our second stop:")

# ------------------------------------------------------------------- cap 3
T("The curve", "nobody puts on a thumbnail",
  "The share of card balances that have gone at least ninety days without a "
  "payment. The quiet statistic. And the one that moved most.",
  cap="The delinquency curve")
I("From seven point six", "to twelve point eight",
  "In mid twenty twenty two, seven point six percent of balances were that "
  "far behind. By early this year: twelve point eight percent.")
B("The climb", ["Mid-2022", "Early 2026"], [59, 100],
  "That is not a wobble. That is a climb of two thirds, through years the "
  "economy was officially fine.")
I("What ninety days means", "the account changes state",
  "Ninety days is not just a number. Past it, the account changes state. "
  "Collection calls, frozen limits, and a credit score that falls faster "
  "than it will ever climb back.")
I("And it is selective", "the K again",
  "The curve is selective too. It is the same K shape. Households with a "
  "cushion barely register in it. Stretched households slide from thirty "
  "days late to sixty and then to ninety.")
I("Ninety is a cliff", "not a milestone",
  "And ninety days is a cliff, not a milestone. Before it, a hardship plan "
  "can still reset the account. After it, the options narrow to collections "
  "or charge-off.")
I("Which explains", "the freezing you read about",
  "Which explains the other headline going around: banks quietly freezing "
  "and cutting card limits. They read this same curve, and they are "
  "closing the exits.")
I("One in eight dollars", "is already stuck",
  "Put simply: about one in eight borrowed dollars on America's cards is "
  "already stuck. The machine keeps running anyway. In fact, it runs ON "
  "this.")
T("Bridge", "open the machine",
  "So let us open the machine and look at the gears. This is the part the "
  "news never does:")

# ------------------------------------------------------------------- cap 4
T("The machine", "one ordinary payment",
  "Take one ordinary card. Five thousand dollars of balance, twenty one "
  "percent interest — the average rate. Now watch a single minimum payment "
  "move through it.",
  cap="The minimum payment machine")
I("Step one", "the interest meter",
  "Step one, the meter. Take the balance and apply the average rate. The "
  "result is eighty seven dollars fifty of interest per month. Before you "
  "buy a single new thing.")
I("Step two", "the minimum arrives",
  "Step two. The typical minimum is around two percent of the balance. On "
  "five thousand, that is one hundred dollars.")
B("Where the $100 goes", ["Interest", "Your debt"], [100, 14],
  "Step three. Of your hundred dollars, eighty seven fifty pays the "
  "interest meter. Twelve dollars fifty touches the actual debt.")
I("Read that again", "12.50 of 100",
  "Read that again. You paid a hundred. Your debt shrank by twelve and a "
  "half. The other eighty seven and a half bought you one more month of "
  "owing.")
I("Now stretch it", "the decades shape",
  "Now stretch that forward. At minimums only, a balance like this takes "
  "decades to die, and the interest paid along the way can exceed the "
  "original debt itself.")
I("And the meter reloads", "every single month",
  "Remember: the meter reloads every month. Pay the minimum, and next month "
  "the balance is nearly unchanged — so the interest charge is nearly "
  "unchanged too. The wheel resets.")
I("Compare a mortgage", "same idea, honest version",
  "Compare a mortgage. It also starts interest-heavy — but it is built to "
  "END, on a fixed schedule. A card minimum has no schedule. It is a loan "
  "designed to renew itself.")
I("The industry word", "revolvers",
  "The industry has a word for people in this loop: revolvers. Not "
  "borrowers. Revolvers. The name of the customer is the name of the "
  "motion.")
I("This is not an accident", "it is the design",
  "And none of this is an accident. The minimum is set low enough to keep "
  "the account alive and paying, not high enough to kill the debt. That is "
  "the design brief.")
I("The proof", "your own statement",
  "The proof is printed on your own statement. US card statements must show "
  "the minimum-payments-only payoff time by law. Find that box. It is the "
  "most honest sentence your bank publishes.")
I("That box has a birthday", "2009",
  "That disclosure box has a birthday, by the way. It was forced onto "
  "statements by the two thousand nine CARD Act — because before it, the "
  "payoff maths lived nowhere at all.")
I("And the escape", "is boring arithmetic",
  "The escape is boring arithmetic. Any fixed payment above the minimum — "
  "even slightly above — collapses the timeline, because every extra dollar "
  "goes straight to the debt.")
B("Minimum vs fixed", ["Minimum only", "Fixed higher payment"], [100, 30],
  "Same balance, same rate. One choice pays for decades. The other pays for "
  "a couple of years. The difference is not income. It is the shape of the "
  "payment.")
T("Bridge", "but why twenty one",
  "Which leaves one question the machine prefers you not ask. Why is the "
  "rate twenty one percent in the first place?")

# ------------------------------------------------------------------- cap 5
T("Why 21%", "the stickiest price in finance",
  "Card interest is the stickiest price in American finance. It climbs "
  "quickly when rates rise, and it barely moves when they fall.",
  cap="Why twenty one percent")
I("How it is built", "a base plus a margin",
  "The rate is built as a base — tied to the Fed — plus a margin the bank "
  "chooses. The base moves with the economy. The margin mostly grows.")
I("Why it can grow", "you are not shopping",
  "The margin can grow because almost nobody shops for card rates. People "
  "shop rewards, cash back, sign-up bonuses. The rate is read later, in a "
  "bad month.")
I("And risk is priced in", "the twelve point eight",
  "And the twelve point eight percent of stuck balances is priced in too. "
  "The borrowers who pay are charged for the borrowers who cannot.")
I("The margin's history", "it widened",
  "And the margin has widened over the years — quietly, a fraction at a "
  "time, in the fine print of terms updates almost nobody reads.")
I("Deposits versus cards", "the spread in one glance",
  "Want the spread in one glance? Look at what your bank pays on your "
  "savings, and what it charges on your card. Same institution, same "
  "dollar, two different worlds.")
I("The uncomfortable line", "reliable payers subsidise",
  "Which produces the uncomfortable line of this chapter: if you carry a "
  "balance and pay reliably, part of your twenty one percent is covering "
  "someone else's default.")
T("Bridge", "your sheet",
  "You cannot vote on the margin. You can only decide how many months it "
  "gets to bill you. So let us build your sheet:")

# ------------------------------------------------------------------- cap 6
T("Six lines", "your balance, your answer",
  "Six lines. Any spreadsheet, or paper. Ten minutes.",
  cap="Your six-line sheet")
L("The six lines", ["Balance", "Your APR", "Interest per month",
                    "Your minimum", "Debt actually paid", "Months to zero"],
  "Your balance. Your interest rate. Interest per month. Your minimum. How "
  "much of it actually pays debt. And months to zero at your current pace.")
I("Gather three documents", "statement, app, rate table",
  "You need three things: your latest statement, your banking app for the "
  "exact balance, and the rate table from your card agreement. Five minutes "
  "of gathering.")
I("Line three", "one multiplication",
  "Line three is one multiplication: balance, times rate, divided by "
  "twelve. That is the meter. Most people have never once computed it.")
I("Line five", "the twelve fifty line",
  "Line five is the twelve-fifty line: your payment minus line three. If it "
  "is small, you are renting your debt, not repaying it.")
I("Line six", "steal it from the statement",
  "Line six you do not even have to compute. Steal it from the statement's "
  "own payoff box, then watch it collapse as you test higher fixed "
  "payments.")
I("The lever", "fix the payment",
  "The lever is one decision: stop paying the minimum percentage and pay a "
  "fixed amount. The minimum shrinks as the balance falls. Your fixed "
  "payment does not — so it kills the debt faster every month.")
I("If you hold several cards", "highest rate first",
  "If you hold several cards, list the rates and put every spare dollar on "
  "the highest one while paying minimums on the rest. The arithmetic of "
  "that order beats every other order.")
I("A worked example", "watch the collapse",
  "Run one worked example to feel it. On the five thousand dollar balance, "
  "test a fixed two hundred a month against the shrinking minimum. Watch "
  "years turn into a couple of dozen months.")
I("And stop the refill", "while you drain",
  "One structural rule while you drain the balance: new purchases go on "
  "debit or cash. Draining a tank while refilling it is the machine's "
  "favourite customer behaviour.")
I("Date the sheet", "rates move",
  "And date the sheet. Rates move, balances move. A sheet from last year "
  "answers last year's question.")
T("Bridge", "three mistakes",
  "Before we close, the three mistakes that keep the machine fed:")

# ------------------------------------------------------------------- cap 7
T("Three mistakes", "and the takeaway",
  "Three mistakes. Each one is a gift to the margin.",
  cap="Three mistakes and the takeaway")
I("First", "reading the minimum as advice",
  "First: reading the minimum as a recommendation. It is not a suggestion "
  "of what you should pay. It is the smallest amount that keeps you "
  "profitable.")
I("A mistake inside the first", "trusting autopay minimums",
  "A sub-mistake inside the first: setting autopay to the minimum and "
  "calling the debt handled. Automation makes the machine frictionless — "
  "for the machine.")
I("Second", "judging debt by the payment",
  "Second: judging affordability by the monthly payment instead of the "
  "meter. A hundred a month feels fine — until you see that twelve fifty is "
  "all that reaches the debt.")
I("Third", "waiting for rates to fall",
  "Third: waiting for card rates to fall. They are the stickiest price in "
  "finance. The falling you are waiting for is not coming to this product.")
L("The video in five lines", ["$1.26T, near the peak",
                              "12.8% of balances stuck",
                              "$87.50 of the first $100",
                              "The minimum is the product",
                              "Fix the payment, kill the debt"],
  "The recap is on screen. Pause it, and argue with it in the comments — "
  "with your line five, ideally.")
I("What almost nobody does", "line three",
  "The thing almost nobody does is line three. One multiplication. Balance "
  "times rate over twelve. It changes how every statement reads forever.")
I("What not to do", "shame arithmetic",
  "One thing not to do: turn this into shame. Sixty percent of cardholders "
  "carry a balance. The maths is not a moral failing. It is just a machine "
  "— and machines can be beaten by design, not by guilt.")
I("A note on balance transfers", "a tool, with a fee",
  "A note on the famous escape hatch: zero percent balance transfers. They "
  "work — as a tool, with a transfer fee, and only if the spending that "
  "built the balance stops. Otherwise they are a second tank.")
I("If you do one thing", "find the payoff box",
  "If you do one thing after this video, open your last statement and find "
  "the minimum-payment payoff box. Read the number of years out loud. That "
  "is the whole wake-up call.")
I("It takes ten minutes", "not a finance degree",
  "And the sheet takes ten minutes, not a finance degree. Six lines, one "
  "multiplication, one decision.")
C("Next Level Money", "count it before it counts you",
  "If you ran your sheet, drop line five in the comments — how much of "
  "your payment actually reaches the debt. I am collecting them for the "
  "next video.")
C("Next Level Money", "count it before it counts you",
  "And if you want this same treatment on another machine — auto loans, "
  "buy now pay later, student debt — say which. Most requested goes first.")

SHORT = [
    {"layout": "titulo", "kicker": "$1.26 TRILLION", "sub": "and one payment",
     "nar": "America's credit card debt just hit one point two six trillion. "
            "But the real story fits inside one minimum payment.",
     "sem_cap": True},
    {"layout": "item", "kicker": "$5,000 at 21%", "preco": "$87.50/month interest",
     "nar": "Five thousand dollars at twenty one percent generates eighty "
            "seven fifty of interest a month. Before you buy anything.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Your $100 minimum", "preco": "$12.50 hits the debt",
     "nar": "So of a hundred dollar minimum payment, twelve fifty touches "
            "the debt. The rest buys you another month of owing.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Not a bug", "preco": "the design",
     "nar": "That is not a bug. The minimum is set to keep the account "
            "alive, not to kill the debt.", "sem_cap": True},
    {"layout": "cta", "kicker": "Next Level Money", "sub": "the full machine",
     "nar": "The full machine, and the six line sheet that beats it, is in "
            "the long video.", "sem_cap": True},
]


def _copy_existente():
    """Le a copy do .json ao lado, se ja existir com conteudo real."""
    import os
    alvo = "fabrica/specs/next-level-money-004.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500:
            return c
    return "gerado a partir dos capitulos reais apos o render"


SPEC = {
    "slug": "next-level-money",
    "pacote": "next-level-money-004",
    "idioma": "en",
    "voz": "en-US-AndrewNeural",
    "trilha": "Deliberate_Thought",
    "paleta": {"ink": "#1A1A1A", "c1": "#E4572E", "c2": "#F2B134",
               "bg": "#F2ECDF"},
    "thumb": {"l1": "$87.50 OF $100", "l2": "the minimum trap"},
    "longo": CENAS,
    "short": SHORT,
    "copy": _copy_existente(),
}

if __name__ == "__main__":
    p = "fabrica/specs/next-level-money-004.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=1)
        f.write("\n")
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ensaio import duracao_estimada
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
