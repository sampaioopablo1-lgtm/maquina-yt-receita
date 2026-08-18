#!/usr/bin/env python3
"""Monta a spec game-money-lab-003.

EIXO. Primeira medicao do nicho (18/08/2026, 22 videos de 90 dias, em
pautas_banco): mediana 1.549,3 v/d. Outliers: "WTF Is Happening To The Video
Game Industry?" (How Money Works, 56.039,6 v/d — explainer de economia, o
formato exato deste canal) e "GTA VI WILL BE $80" (short, 51.054,5 v/d). O
-002 do canal foi o CUSTO de producao (US$ 300 mi); o eixo do PRECO ao
consumidor esta intocado.

E o eixo e bipolar, o que decide o angulo: o short de 51 mil v/d convive com
CINCO videos de preco MORTOS (0,2 a 66 v/d) na mesma janela. Preco so
performa com angulo forte; noticiario morno de preco morre. O angulo forte e
o contraintuitivo que a conta sustenta: o jogo de 80 dolares ainda e mais
barato, em termos reais, que o de 2005 — e e exatamente por isso que o resto
ficou caro.

NUMEROS, dois blocos (buscas de 18/08/2026):

  GTA 6 (Variety; confirmado em gtaboom, gameluster, thepcenthusiast)
    padrao US$ 79,99 | Ultimate US$ 99,99 | lancamento 19/11/2026
    pre-venda desde 25/06/2026 | SO digital, sem disco | pre-load 12/11

  Inflacao dos precos (apophenialabs.ai/video-game-inflation; gameflation;
  videogameconsolelibrary — todos sobre CPI oficial do BLS)
    US$ 60 de 2005 = US$ 98,89 de hoje: a inflacao comeu ~40% enquanto a
    etiqueta ficou parada quinze anos
    cartucho de SNES de 1993 custava, em termos reais, quase o DOBRO de um
    lancamento atual
    o aumento real veio por fora: DLC, season pass, battle pass, edicoes —
    o custo da experiencia "completa" dobrou

A tese: o preco nao subiu — MUDOU DE LUGAR. A etiqueta congelada por quinze
anos nao foi generosidade; foi a construcao de um andar de cima (edicoes,
passes, assinaturas, moeda virtual) onde o aumento mora sem aparecer na
manchete. O video fecha com a unica conta que importa ao jogador: custo por
hora jogada, na planilha da casa.

VOZ. en-GB-RyanNeural (18,74 chars/s, P=1,089) — calibracao de PRODUCAO,
n=51. ~10,5 mil chars para ~13 min.
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
T("Two numbers", "one broken argument",
  "Seventy nine ninety nine. And ninety eight dollars eighty nine. The first "
  "is the most controversial price in gaming. The second is why the "
  "controversy has the maths backwards.",
  cap="The two numbers")
I("The first", "GTA Six, standard edition",
  "The first number is official. GTA Six, standard edition, seventy nine "
  "ninety nine. Launching November the nineteenth, digital only, pre-orders "
  "open since June.")
I("The second", "your 2005 game, today",
  "The second number is what a sixty dollar game from two thousand and five "
  "costs in today's money. Ninety eight dollars and eighty nine cents.")
B("Side by side", ["GTA 6", "2005 game, real terms"], [81, 100],
  "Put them side by side and the outrage inverts. The most expensive "
  "blockbuster ever made is still cheaper, in real money, than a mid "
  "two-thousands disc.")
I("So the question changes", "from why so dear to why so cheap",
  "So the honest question is not why games got so expensive. It is how they "
  "stayed this cheap — and who has been quietly paying the difference.")
T("This video", "the maths, not the mood",
  "This video does the maths the comment section skips. No outrage, no "
  "defence of publishers. Just where the money actually went.")
L("The route", ["The 20-year freeze", "Where the rise hid",
                "The producer squeeze", "Cost per hour",
                "Your own sheet"],
  "Five stops. The twenty year price freeze. Where the rise went into "
  "hiding. What the freeze did to the people making games. The only number "
  "that matters to a player. And a sheet you fill in yourself.")
I("One warning", "every number has an owner",
  "One warning before we start: every number here has an owner and a date. "
  "Official announcements, and inflation maths on public price records.")
I("Starting point", "the freezer",
  "Start with the freezer. Because the strangest thing about game prices is "
  "not that they finally moved. It is how long they refused to:")

# ------------------------------------------------------------------- cap 2
T("Fifteen years", "of fifty nine ninety nine",
  "From the mid two-thousands to twenty twenty, a full priced console game "
  "cost fifty nine ninety nine. Consoles changed twice. The sticker did not "
  "move once.",
  cap="The 20-year freeze")
I("Meanwhile", "everything else rose",
  "Meanwhile everything else in your life rose. Rent rose. Food rose. Cinema "
  "tickets and streaming rose. The game on the shelf sat still.")
I("What inflation did", "ate forty percent",
  "And a frozen sticker is not a frozen price. Inflation ate roughly forty "
  "percent of its value while it sat there.")
I("In real terms", "games got cheaper every year",
  "In real terms, every year of the freeze made games cheaper. Silently, "
  "automatically, without a single press release.")
I("Go back further", "the SNES cartridge",
  "Go back further and it gets starker. A Super Nintendo cartridge in the "
  "early nineties cost, in today's money, nearly double a current release.")
I("Why freeze at all", "a price war in disguise",
  "Why would an industry freeze its own price? Because the sticker was a "
  "weapon. Two console makers anchoring at fifty nine ninety nine, each "
  "afraid to blink first.")
I("And the 2020 move", "undershot",
  "And look closely at the twenty twenty move. Ten dollars, after fifteen "
  "years in which inflation had taken forty percent. The rise itself "
  "undershot the freeze.")
I("The first move", "seventy, in 2020",
  "The first sticker move in fifteen years came in twenty twenty: seventy "
  "dollars for the new console generation.")
I("The second move", "eighty, now",
  "The second is happening now. Eighty dollars, with GTA Six as the "
  "battering ram. Two moves in twenty years.")
B("The sticker vs inflation", ["Sticker path", "Inflation path"], [81, 100],
  "And even after both moves, the sticker sits below where inflation alone "
  "would have carried it. That gap is the whole story.")
I("Because that gap", "did not stay unpaid",
  "Because that gap did not stay unpaid. Somebody built a second floor on "
  "top of the sticker, and that is our next stop.")
T("Bridge", "where the rise hid",
  "If the front door price could not rise, the rise had to come in through "
  "the back. Here is the back door:")

# ------------------------------------------------------------------- cap 3
T("The price did not rise", "it moved",
  "Here is the real headline. The price of games did not rise. It moved — "
  "out of the sticker and into everything around it.",
  cap="Where the rise hid")
L("The second floor", ["Deluxe editions", "Season passes",
                       "Battle passes", "Virtual currency"],
  "The second floor has four rooms. Deluxe and ultimate editions. Season "
  "passes. Battle passes. And virtual currency sold in bundles that never "
  "quite match the shop prices.")
I("Exhibit one", "the Ultimate edition",
  "Exhibit one is on the GTA Six pre-order page itself. Standard, seventy "
  "nine ninety nine. Ultimate, ninety nine ninety nine. The eighty dollar "
  "game comes with a hundred dollar option attached.")
I("The complete game", "roughly doubled",
  "Add the passes and the add-ons, and the cost of the complete experience "
  "of a big game has roughly doubled compared to the disc era.")
I("Which explains the feeling", "both sides are right",
  "Which explains why both sides of the argument feel right. The sticker "
  "really is historically cheap. And your total spend really is higher than "
  "ever.")
I("The trick", "unbundling",
  "The trick has a boring name: unbundling. Sell the core for a frozen "
  "price, and price the rest of the experience separately, where inflation "
  "can run free.")
I("Exhibit two", "Rockstar's own history",
  "Exhibit two is the seller itself. GTA Five sold over two hundred million "
  "copies — and its online mode still made billions AFTER the purchase, "
  "year upon year, through virtual currency.")
I("Which reframes the 80", "an entry ticket",
  "Which reframes the eighty dollars. For a game built to live for a "
  "decade, the sticker is not the price. It is the entry ticket.")
I("And the ground floor", "costs zero",
  "And do not forget the ground floor of this building: free to play. The "
  "most profitable games of the last decade charged nothing at the door. We "
  "counted that model on this channel before.")
I("Subscriptions", "the third floor",
  "And above the second floor there is a third: subscriptions. A monthly fee "
  "that never appears in any argument about the price of a game, and never "
  "stops charging.")
I("None of this is a scandal", "it is a structure",
  "None of this is a hidden scandal. Every price is public. It is a "
  "structure — one designed so that no single number looks like a rise.")
T("Bridge", "who paid on the other side",
  "And structures have two ends. If the player's sticker was frozen, "
  "someone on the making side was absorbing the freeze:")

# ------------------------------------------------------------------- cap 4
T("The other side", "of a frozen sticker",
  "On the other side of a frozen sticker sits a studio whose costs were "
  "never frozen.",
  cap="The producer squeeze")
I("We counted it", "three hundred million",
  "We counted that side on this channel already: the three hundred million "
  "dollar blockbuster. Budgets that grew tenfold while the sticker grew "
  "thirty three percent.")
I("The squeeze", "two lines crossing",
  "That is the squeeze in one picture. Costs climbing for twenty years, "
  "revenue per copy flat for fifteen of them. Two lines crossing.")
I("What crossing lines buy", "layoffs and closures",
  "And the news you have been reading for three years — the layoffs, the "
  "studio closures, the cancelled projects — lives exactly where those "
  "lines cross.")
I("The scale", "tens of thousands",
  "Industry trackers have counted tens of thousands of games jobs lost "
  "across the last three years. Not one bad quarter — a structural wave.")
I("The eighty dollars", "arrives late",
  "Seen from that side, the eighty dollar sticker is not greed arriving "
  "early. It is arithmetic arriving late.")
I("But honesty cuts both ways", "the second floor pays too",
  "But honesty cuts both ways. The publishers crying over costs also built "
  "the second floor, and the second floor collects billions. The squeeze is "
  "real, and so is the workaround.")
T("Bridge", "so what should YOU pay",
  "Which leaves the only question this channel cares about. Not what games "
  "should cost. What they cost YOU:")

# ------------------------------------------------------------------- cap 5
T("The only honest metric", "cost per hour",
  "The only honest price of a game is not on the box. It is the price "
  "divided by the hours you actually play.",
  cap="Cost per hour")
I("The eighty dollar game", "at a hundred hours",
  "Take the eighty dollar blockbuster you play for a hundred hours. Eighty "
  "cents an hour.")
I("Compare the cinema", "several times that",
  "A cinema ticket buys two hours. Do that division and the game is one of "
  "the cheapest hours of entertainment money can buy.")
I("Now flip it", "the impulse buy",
  "Now flip it. The thirty dollar impulse buy you drop after ninety "
  "minutes costs twenty dollars an hour. The expensive game is the one you "
  "do not play.")
I("Same logic", "for the passes",
  "The same division works on the second floor. A pass you grind every "
  "week is cheap. A pass you bought in March and forgot by April is the "
  "most expensive item in your library.")
I("And timing is a price too", "the patient discount",
  "Timing is a price lever as well. The same game, six or twelve months "
  "after launch, routinely sells for a fraction of the sticker. Patience "
  "is the one discount nobody advertises.")
I("Launch price", "is a choice, not a rule",
  "So the launch price is a choice you make, not a rule you obey. Paying "
  "it is rational exactly when your hours will be highest at launch — "
  "which is true for some games and false for most.")
I("Price tags lie", "libraries do not",
  "Price tags start arguments. Libraries end them. Your play history "
  "already knows which purchases were worth it.")
T("Bridge", "make it a sheet",
  "So let us turn your library into the sheet that answers this for your "
  "case, not for the comment section's:")

# ------------------------------------------------------------------- cap 6
T("Six lines", "any spreadsheet will do",
  "Six lines. Any spreadsheet, or the notes app on your phone.",
  cap="Your own sheet")
L("The six lines", ["Games bought this year", "Editions and passes",
                    "Subscriptions x 12", "Hours actually played",
                    "Cost per hour", "The one to cut"],
  "Games bought this year. Editions and passes on top. Subscriptions times "
  "twelve. Hours actually played, from your console's own stats. Cost per "
  "hour. And the line you decide to cut.")
I("Line one and two", "sticker versus second floor",
  "Lines one and two split your spend into sticker and second floor. Most "
  "people have never seen that split. It is usually the surprise.")
I("Line three", "the invisible twelve",
  "Line three is the quiet one. Any subscription times twelve. It never "
  "feels like game spending, and it is often the biggest number on the "
  "sheet.")
I("Line four", "your console already counts it",
  "Line four needs no honesty test. Your console and your launcher already "
  "count your hours. Copy the number, do not estimate it.")
I("Line five", "one division",
  "Line five is one division: total spend over total hours. That is your "
  "personal price of gaming. Not the industry's. Yours.")
I("Line six", "the cut",
  "Line six is the decision. Whatever scored worst per hour this year — a "
  "subscription, a pass, a genre — that is the line you cut before the "
  "next launch season.")
I("Date it", "prices move twice a year now",
  "And date the sheet. The freeze is over — stickers move now, and passes "
  "reprice every season. An undated sheet goes stale in months.")
T("Bridge", "three mistakes before we close",
  "Before we close, the three mistakes that ruin this comparison every "
  "single time:")

# ------------------------------------------------------------------- cap 7
T("Three mistakes", "and the takeaway",
  "Three mistakes, each one expensive in its own way.",
  cap="Three mistakes and the takeaway")
I("First", "comparing stickers across decades",
  "First: comparing stickers across decades without inflation. Sixty "
  "dollars in two thousand five is not sixty dollars today. It is nearly a "
  "hundred.")
I("Second", "judging the sticker, ignoring the floor",
  "Second: judging the sticker and ignoring the second floor. The eighty is "
  "historically cheap. The eighty plus edition plus pass plus subscription "
  "is not.")
I("Third", "paying for hours you never play",
  "Third: paying for hours you never play. The most expensive game in your "
  "life is almost certainly one you barely opened.")
L("The video in five lines", ["$60 of 2005 = $98.89 today",
                              "Two sticker moves in 20 years",
                              "The rise moved into passes",
                              "Squeeze on the maker side",
                              "Judge by cost per hour"],
  "The recap is on screen. Pause it and steal it. Argue with it in the "
  "comments — with numbers, preferably.")
I("What almost nobody does", "the split",
  "The thing almost nobody does is line two: splitting sticker from second "
  "floor. Do that once and every future purchase gets easier to judge.")
I("What not to do", "argue the sticker in the abstract",
  "One thing not to do: argue about the eighty dollars in the abstract. "
  "Without your hours, the sticker is just a number shouting at other "
  "numbers.")
I("If you do one thing", "run the division",
  "If you do one thing after this video, open your play stats and run the "
  "division on your last three purchases. That is the whole method.")
I("It takes an evening", "not a project",
  "It takes an evening, not a project. Six lines on one screen, and the "
  "first division fits in a coffee break.")
C("Game Money Lab", "count the fun, then buy it",
  "If you ran the numbers, drop your cost per hour in the comments. I am "
  "collecting them for the next video.")
C("Game Money Lab", "count the fun, then buy it",
  "And if you want this same maths on another corner of gaming — "
  "subscriptions, hardware, virtual currency — say which. Most requested "
  "goes first.")

SHORT = [
    {"layout": "titulo", "kicker": "$79.99 vs $98.89", "sub": "the maths is backwards",
     "nar": "GTA Six costs eighty dollars. And the maths behind the outrage "
            "is backwards.", "sem_cap": True},
    {"layout": "item", "kicker": "Your 2005 game", "preco": "$98.89 today",
     "nar": "A sixty dollar game from two thousand five costs ninety eight "
            "eighty nine in today's money. The freeze ate forty percent.",
     "sem_cap": True},
    {"layout": "item", "kicker": "So the price", "preco": "did not rise — it moved",
     "nar": "The real rise moved out of the sticker. Into editions, passes "
            "and subscriptions. The complete game roughly doubled.",
     "sem_cap": True},
    {"layout": "item", "kicker": "The honest metric", "preco": "cost per hour",
     "nar": "And the only honest price is cost per hour played. Eighty "
            "dollars for a hundred hours is eighty cents an hour.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Game Money Lab", "sub": "the full 20-year maths",
     "nar": "The full twenty year maths, and the sheet that prices YOUR "
            "library, is in the long video.", "sem_cap": True},
]


def _copy_existente():
    """Le a copy do .json ao lado, se ja existir com conteudo real."""
    import os
    alvo = "fabrica/specs/game-money-lab-003.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500:
            return c
    return "gerado a partir dos capitulos reais apos o render"


SPEC = {
    "slug": "game-money-lab",
    "pacote": "game-money-lab-003",
    "idioma": "en",
    "voz": "en-GB-RyanNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#131A26", "c1": "#5B2A86", "c2": "#3DDC97",
               "bg": "#F2F0FA"},
    "thumb": {"l1": "$79.99 vs $98.89", "l2": "the price freeze"},
    "longo": CENAS,
    "short": SHORT,
    "copy": _copy_existente(),
}

if __name__ == "__main__":
    p = "fabrica/specs/game-money-lab-003.json"
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
