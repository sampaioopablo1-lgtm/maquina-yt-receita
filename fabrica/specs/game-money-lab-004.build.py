#!/usr/bin/env python3
"""Monta a spec game-money-lab-004.

POR QUE ESTE CANAL. Primeiro da fila que produz (ultimo pacote 18/08 07:29).

POR QUE ESTE TEMA. O acervo proprio tem so quatro videos, mas ja diz uma coisa:

    GTA 6 Costs $80: The 20-Year Price Freeze...   short  39,9 v/d  (2,3 dias)
    $300 Million Per Game                          short   6,9 v/d  (7,5 dias)
    os dois longos correspondentes                 longo   0,0 v/d

A assinatura e CIFRA EXATA EM DOLAR mais A MATEMATICA POR TRAS DELA, e o de
39,9 tem uma coisa a mais que o de 6,9: esta preso a uma NOTICIA DATADA.

No nicho, os eixos medidos sao `crise da industria` (topo 56.039 v/d),
`preco dos jogos` (51.054 — ja usado pelo canal) e `demissoes` (9.468, 3.905,
3.495, 1.501). DEMISSOES E O EIXO QUE PERFORMA E O CANAL NUNCA USOU.

O que este roteiro NAO copia do nicho e o TOM. Os outliers de demissoes usam
raiva ("BLOODBATH", "Woke Studio"). A rotina manda modelar a ESTRUTURA do
outlier, nao o assunto nem a voz — e a estrutura aqui e cifra mais mecanismo.

O GIRO. Todo mundo noticia o TOTAL. O numero que ninguem acompanha e a REVISAO:
em janeiro a previsao para 2026 era 8.025, e em julho virou 14.259. Setenta e
oito por cento em seis meses, no mesmo ano e no mesmo rastreador.

FONTES, duas que batem:
  ASGC Games Industry Layoffs Tracker, mantido por Amir Satvat (Tencent Games).
  GamesBeat, 30/07/2026, citando o rastreador direto:
    previsao 2026: 8.025 em janeiro -> 14.259 em julho (+78%)
    confirmados: 9.464 -> 9.781 (+317, +3%) desde a previsao anterior
    historico: 2022 = 8.500, 2023 = 10.500, 2024 = 15.631, 2025 = 9.197
    geografia: America do Norte e Europa somam 95%; EUA 48%, Canada 17%,
               Europa 30%
  Os mesmos numeros aparecem em gamedev.net, ixbt.games e Outlook Respawn.

O QUE O ROTEIRO NAO FAZ: nao preve o numero final de 2026, nao atribui culpa a
empresa nenhuma, e nao trata o rastreador como censo — ele conta o que e
publicamente reportado, e isso e um piso, nao um total. O capitulo 6 diz isso.

TAXA DA VOZ. en-GB-RyanNeural: R = 18,92 chars/s (a mais rapida da frota),
P = 1,162 s/frase. Densidade do canal: 2,64 frases/cena no longo, 2,00 no short.
Orcamento: 76 cenas em 810 s = 10.486 caracteres, 138 por cena. Short: 387
caracteres em 6 cenas para 35,9 s.

CAPITULOS abrem SEMPRE em layout `titulo`: o `copy_md.capitulos` so reconhece
`titulo` e `broll` como abertura de secao, e capitulo aberto em `item` some da
descricao publicada — foi o que custou um capitulo na seviye-seviye-004
(aprendizado 388).
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


# ------------------------------------------------------ 1. The number that moved
T("Eight thousand", "and twenty five",
  "In January, the industry's main layoff tracker published a forecast for this "
  "year. Eight thousand and twenty five jobs. That was the number the whole "
  "industry planned around.",
  cap="The number that moved")
I("Six months later", "fourteen thousand two fifty nine",
  "By the end of July the same tracker, run by the same person, using the same "
  "method, was forecasting fourteen thousand two hundred and fifty nine.")
T("That is a jump", "of seventy-eight per cent",
  "That is a jump of seventy-eight per cent. Not year over year. Within a "
  "single year, about a single year.")
T("Almost nobody covered that", "they covered the total",
  "Almost nobody covered the revision. Everybody covered the total. Those are "
  "very different stories, and only one of them tells you where things are going.")
I("The total", "is a photograph",
  "A total is a photograph. It tells you where the number stands on the day "
  "somebody wrote it down.")
I("The revision", "is a direction",
  "A revision is a direction. It tells you which way the estimate has been "
  "moving, and how fast, and that survives the next headline.")
T("So this is not a doom video", "it is a method video",
  "So this is not a video about how bad things are. It is a video about how to "
  "read a number that keeps changing.")
L("Three things", ["How the tracker actually works",
                   "Where every revision has gone",
                   "What it does not predict"],
  "Three things. How the tracker actually works. Where the revisions have gone "
  "so far. And, at the end, what none of this predicts.")
T("One thing up front", "no forecast for you",
  "One thing up front. I will not give you a final figure for this year. "
  "Nobody has one, and a quarter is still open.")
I("What I will give", "the mechanism",
  "What I will give you is the mechanism, so the next revision is something you "
  "can read instead of something that lands on you.")
C("Start with the tracker", "because it is not a census",
  "Start with the tracker itself. Because it is not what most people assume it is.")

# ------------------------------------------------ 2. What the tracker counts
T("It is not a census", "it is a ledger",
  "The tracker is not a census of the industry. Nobody has that. It is a ledger "
  "of publicly reported job losses, assembled from announcements, filings and "
  "confirmed reporting.",
  cap="What the tracker counts")
I("Who runs it", "Amir Satvat",
  "It is maintained by Amir Satvat, a business development director at Tencent "
  "Games, and it is the number the trade press cites when it cites a number.")
T("It has two columns", "and they behave differently",
  "It has two columns that behave completely differently, and mixing them is "
  "where most confusion starts.")
I("Confirmed", "nine thousand seven eighty one",
  "Confirmed. As of late July, nine thousand seven hundred and eighty one "
  "people. These are counted, named events. This column only ever goes up.")
I("Projected", "fourteen thousand two fifty nine",
  "Projected. Fourteen thousand two hundred and fifty nine by year end. This is "
  "the estimate, and this column moves in both directions in principle.")
T("In practice", "it has gone one way",
  "In practice, this year, it has gone one way. And the reason is structural, "
  "not editorial.")
I("Between two updates", "three hundred and seventeen",
  "Between the two most recent updates the confirmed column added three hundred "
  "and seventeen people. Three per cent, in a matter of weeks.")
T("Why that matters", "confirmation lags the event",
  "Here is why that matters. A layoff happens on a Tuesday. It gets confirmed "
  "when somebody reports it, which can be weeks later.")
T("So the ledger", "is always behind reality",
  "So the confirmed column is always behind reality by however long confirmation "
  "takes. Not because it is sloppy. Because that is what confirming means.")
I("Which means", "the floor, not the total",
  "Which means the confirmed number is a floor. The real figure on any given "
  "day is that number or higher, never lower.")
C("Now the history", "and the direction in it",
  "Now let us look at what the last few years actually did.")

# ---------------------------------------------- 3. Where the revisions have gone
T("Five years", "and no straight line",
  "Here are the confirmed totals, year by year, from the same tracker. And the "
  "shape is not the one most people carry in their head.",
  cap="Where the revisions have gone")
B("Confirmed by year", ["2022", "2023", "2024", "2025", "2026*"],
  [0.54, 0.67, 1.0, 0.59, 0.63],
  "Twenty twenty-two, eight thousand five hundred. Twenty twenty-three, ten "
  "thousand five hundred. Twenty twenty-four, fifteen thousand six hundred and "
  "thirty one.")
I("Then it fell", "nine thousand one ninety seven",
  "Then twenty twenty-five came in at nine thousand one hundred and ninety "
  "seven. A real drop, and a lot of people read that as the end of it.")
T("This year", "already past three of those four",
  "This year has already passed twenty twenty-two, twenty twenty-three and "
  "twenty twenty-five on confirmed alone. With a quarter still to run.")
T("The peak still stands", "and that matters",
  "The peak still stands. Twenty twenty-four was worse than what this year is "
  "projected to reach, and saying otherwise would be overselling it.")
I("But the shape changed", "recovery became a pause",
  "But what changed is the shape. Last year looked like a recovery. This year "
  "makes it look more like a pause in the middle of something longer.")
T("And the five-year total", "is the number to sit with",
  "And if you add the five years together, the projection lands near sixty "
  "thousand people. That is the number I would sit with, not any single year.")
T("Because single years argue", "and the sum does not",
  "Single years can be argued about. One studio closing can move a year. The "
  "five-year sum is much harder to explain away.")
I("A caution", "these are not the same people",
  "One caution before we go on. Sixty thousand job losses is not sixty thousand "
  "different people. Some are counted more than once across years.")
T("Nobody publishes that split", "so I will not invent it",
  "Nobody publishes how many. So I am not going to estimate it, and you should "
  "be sceptical of anybody who does.")
C("Next", "where these jobs actually were",
  "Next, the part that changes who this is actually happening to.")

# ------------------------------------------- 4. The geography nobody prices in
T("Ninety-five per cent", "of it is two regions",
  "This is the part that reframes the whole thing for me. North America and "
  "Europe account for ninety-five per cent of all games industry layoffs in "
  "this dataset. Not most of them. Almost all of them.",
  cap="The geography nobody prices in")
I("United States", "forty-eight per cent",
  "The United States alone is forty-eight per cent of this year's total. Canada "
  "adds seventeen. Europe adds thirty.")
T("Which leaves", "five per cent for everywhere else",
  "Which leaves about five per cent for the entire rest of the world. Japan, "
  "Korea, China, India, Brazil, all of it, inside that five.")
T("Now hold on", "because that cuts two ways",
  "Now hold on before you draw the obvious conclusion, because this number cuts "
  "in two directions and only one of them gets said out loud.")
I("The first reading", "western studios are shrinking",
  "The first reading is the popular one. Western studios are contracting, and "
  "development is moving to cheaper places. That reading is not wrong.")
I("The second reading", "the tracker sees in English",
  "The second reading is about the ledger itself. It counts what is publicly "
  "reported, and public reporting of layoffs is far denser in English-language "
  "markets than anywhere else.")
T("A studio that shrinks quietly", "in a market with less trade press",
  "A studio that shrinks quietly in a market with less trade press coverage may "
  "simply not enter this dataset at all. Not hidden. Just never written down.")
T("So how much of ninety-five", "is concentration, how much is visibility",
  "So how much of that ninety-five per cent is real concentration, and how much "
  "is visibility? I do not know, and neither does anybody quoting it at you.")
I("What I can say", "it is a ceiling for the west",
  "What I can say is narrower. For western developers, this figure is not an "
  "overstatement. Whatever the rest of the world's true number is, it does not "
  "subtract from theirs.")
T("That is the honest version", "and it is still bad news",
  "That is the honest version of the geography claim. It is still bad news for "
  "the people in it, and it is a weaker claim than the headline makes.")
C("Now the direction", "and why it keeps going up",
  "Which brings us back to the revision, and why it has only moved one way.")

# ------------------------------------------- 5. Why the direction is not random
T("A guess would be", "the industry got worse",
  "The intuitive explanation for a seventy-eight per cent upward revision is "
  "that things got much worse than expected between January and July. That may "
  "be part of it. It is not the whole thing.",
  cap="Why the direction is not random")
T("Part of it is arithmetic", "of how the forecast is built",
  "Part of it is arithmetic, built into how any forecast of this kind works. "
  "And once you see it, the revisions stop feeling like shocks.")
I("A January forecast", "has almost no year in it",
  "A forecast published in January is built on almost no data from the year it "
  "is forecasting. It leans on last year, and last year was the low one.")
T("So it starts low", "by construction",
  "So it starts low. Not pessimistically or optimistically. By construction.")
I("Each month after", "adds confirmed events",
  "Every month after that adds real confirmed events, and confirmed events only "
  "ever add. There is no mechanism for a confirmed layoff to un-happen.")
T("So the estimate", "walks upward as the year fills in",
  "So the estimate walks upward as the year fills in. It would do that even in "
  "a year that turned out completely normal.")
T("Which is why", "the revision is not the alarm",
  "Which is why the size of the revision, on its own, is not the alarm people "
  "read it as. Some upward drift is the method, not the message.")
I("The real question", "faster or slower than the drift",
  "The real question is whether it is drifting faster than normal. And that you "
  "answer by comparing the same month across years, not by staring at one jump.")
T("I am flagging this", "as reasoning, not data",
  "And I am flagging clearly: that mechanism is my reading of how the forecast "
  "is built. It is not a claim the tracker publishes.")
T("Why say that out loud", "because it changes what you trust",
  "I say it out loud because you should hold it more loosely than the counts. "
  "The counts are sourced. This is an explanation of them.")
C("So what survives", "when you strip the framing",
  "So what actually survives when you strip all the framing off?")

# ---------------------------------------- 6. What this does and does not predict
T("It does not predict", "the final figure",
  "It does not predict where this year lands. A quarter is open, and one large "
  "closure can move the total by a thousand people in an afternoon.",
  cap="What this does and does not predict")
I("It does not say", "which studio is next",
  "It does not tell you which studio is next. Nobody who tells you that knows, "
  "and the ones who claim to are selling something.")
T("It does not measure", "hiring",
  "It does not measure hiring at all. This is a one-sided ledger. A year with "
  "high layoffs and high hiring looks identical here to one with neither.")
I("And it is a floor", "not a total",
  "And the confirmed column is a floor, not a total. What is not publicly "
  "reported is not in it, and there is no way to know how much that is.")
T("So what does it support", "two things, both narrow",
  "So what does it actually support? Two things, and both are narrower than the "
  "headlines built on them.")
L("What survives", ["The direction of the revisions",
                    "The five-year floor",
                    "Where the reported losses are"],
  "The direction the revisions have moved. The five-year floor of roughly sixty "
  "thousand reported losses. And that the reported ones are concentrated in two "
  "regions.")
T("That is enough", "to make a decision with",
  "That is enough to make a career decision with. It is not enough to make a "
  "prediction with, and the difference matters.")
I("If you work in this", "the useful read",
  "If you work in this industry, the useful read is not the total. It is that "
  "the estimate has moved up every time it has been touched this year.")
T("And if you are outside it", "the useful read is different",
  "If you are outside it, the useful read is different again. This is what a "
  "sector looks like while it repricies labour, and the counting lags the event.")
T("Neither of those", "is a headline",
  "Neither of those makes a headline. Both of them are more useful than one.")
C("Last part", "what to watch instead",
  "Last part. What I would actually watch from here.")

# ------------------------------------------ 7. What to watch instead of the total
T("Watch the revision", "not the number",
  "When the next update lands, do not read the total first. Read what the "
  "projection was before it, and what it is now.",
  cap="What to watch instead of the total")
I("The gap", "is the whole signal",
  "The gap between those two is the signal. The total is just where the gap "
  "happens to have arrived.")
L("Three numbers", ["The previous projection",
                    "The new projection",
                    "Confirmed, both times"],
  "Three numbers, thirty seconds. The previous projection. The new one. And the "
  "confirmed column at both dates.")
T("If the projection moves", "and confirmed barely does",
  "If the projection jumps and the confirmed column barely moves, the model "
  "changed its mind. That is worth attention.")
T("If both move together", "the year is filling in",
  "If both move together, the year is simply filling in as expected. Less "
  "dramatic, and much more common.")
I("That distinction", "is invisible in the headline",
  "That distinction is completely invisible in any headline about the total, "
  "and it takes half a minute to check.")
T("One more habit", "compare the same month",
  "One more habit worth having. Compare the same month across years. July to "
  "July tells you something. July to January tells you almost nothing.")
T("Sources are in the description", "check them",
  "The tracker and the reporting are both linked below. Go and look, because "
  "this is a number you will see quoted badly all year.")
I("Next video", "the hiring side",
  "In the next video I want to do the other half of this ledger. What the "
  "hiring side actually shows, and why it is much harder to count.")
C("Because a one-sided ledger", "answers half a question",
  "Because a ledger with only one side answers half a question, and half a "
  "question is how you end up sure about the wrong thing.")

# ---------------------------------------------------------------- the short
# Opens on the revision, which is the result — not on context. Budget measured
# for 35,9 s with 6 scenes at 2,00 sentences each: 387 characters.
SHORT = [
    {"layout": "titulo", "kicker": "January", "sub": "eight thousand and twenty five",
     "nar": "In January the games layoff forecast for this year was eight "
            "thousand and twenty five.", "sem_cap": True},
    {"layout": "titulo", "kicker": "July", "sub": "fourteen thousand two fifty nine",
     "nar": "By July, same tracker, same method: fourteen thousand two hundred "
            "and fifty nine.", "sem_cap": True},
    {"layout": "titulo", "kicker": "That is", "sub": "seventy-eight per cent",
     "nar": "Seventy-eight per cent higher. Same year. Six months apart.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "The story", "sub": "is not the total",
     "nar": "Everyone reported the total. Almost nobody reported the revision.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "A total", "sub": "a revision",
     "nar": "A total is a photograph. A revision is a direction.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Full breakdown", "sub": "on the channel",
     "nar": "The full breakdown, and why it only moves one way, is on the channel.",
     "sem_cap": True},
]

THUMB = {"l1": "8,025 to 14,259", "l2": "in six months"}

COPY = """# The revision, not the total: reading the 2026 games layoff tracker

## TITULO
Gaming Layoffs 2026: The Forecast Was Revised Up 78% in Six Months

## DESCRICAO
In January, the ASGC Games Industry Layoffs Tracker forecast 8,025 games industry job losses for 2026. By the end of July, the same tracker — same maintainer, same method — was projecting 14,259. That is a 78% upward revision inside a single year, about that same year.

Almost every outlet covered the total. Almost none covered the revision. A total is a photograph: it tells you where the number stood the day someone wrote it down. A revision is a direction, and a direction survives the next headline.

What the tracker actually is: not a census of the industry, but a ledger of publicly reported job losses, maintained by Amir Satvat, a business development director at Tencent Games. It has two columns that behave very differently. Confirmed — 9,781 people as of late July, up 317 (+3%) from the previous update — counts named, reported events and only ever rises. Projected is the estimate for year end. Confirmation lags the event by however long reporting takes, which makes the confirmed column a floor, never a total.

The five-year picture, confirmed: 2022 around 8,500; 2023 around 10,500; 2024 the peak at 15,631; 2025 down to 9,197. This year has already passed 2022, 2023 and 2025 on confirmed alone, with a quarter still open — though 2024 remains the worst year on record, and saying otherwise oversells it. Across the five years the projection lands near 60,000 reported losses. That total is not 60,000 distinct people; nobody publishes how much overlap there is, so this video does not estimate it.

Geography: North America and Europe account for 95% of the layoffs in this dataset — the US 48%, Canada 17%, Europe 30%. That figure cuts two ways, and the video takes both seriously. Western studios really are contracting; and the ledger counts what is publicly reported, and public reporting of layoffs is far denser in English-language markets. How much of the 95% is concentration and how much is visibility is not knowable from this data.

On why revisions keep moving up: a January forecast is built on almost no data from the year it forecasts, and every month afterwards adds confirmed events that can only add. Some upward drift is the method, not the message. That explanation is flagged in the video as reasoning, not as something the tracker publishes.

And the limits: this predicts no final figure, names no studio, measures no hiring at all, and counts only what was reported.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
A question for anyone working in the industry: when the next tracker update lands, does your studio's situation show up in it at all — or is it the kind of quiet contraction that never gets publicly reported? I'm trying to get a sense of how much the ledger misses, and that is the one thing the data cannot tell me.

## HASHTAGS
#GameIndustry #Layoffs #GameMoneyLab

## TAGS
game industry layoffs, games industry 2026, video game layoffs, amir satvat, layoffs tracker, game development, aaa games, studio closures, games business, game jobs, industry analysis, gaming economy, tech layoffs, games market, developer jobs

## CONFIGURACAO DE STUDIO
- Language: English (en-GB) | Category: Education (27)
- Not made for kids
- Altered or synthetic content disclosure: YES (AI-generated voice)
- Location: United Kingdom | Licence: Standard YouTube Licence
- Mid-roll ads: on (runtime over eight minutes)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
All figures come from the ASGC Games Industry Layoffs Tracker, maintained by Amir Satvat (business development director at Tencent Games), as reported by GamesBeat on 30 July 2026 and corroborated by gamedev.net, ixbt.games and Outlook Respawn with identical numbers: 2026 forecast revised from 8,025 in January to 14,259 in July (+78%); confirmed losses 9,464 rising to 9,781 (+317, +3%); annual confirmed totals of roughly 8,500 (2022), 10,500 (2023), 15,631 (2024) and 9,197 (2025); and a regional split of 95% North America and Europe, with the US at 48%, Canada 17% and Europe 30%. Accessed 20 August 2026. The tracker counts publicly reported job losses and is therefore a floor, not a census. This video does not forecast the final 2026 figure, does not name or blame any company, does not estimate how many of the five-year total are distinct individuals, and does not measure hiring. The explanation offered for why forecasts drift upward is the presenter's reasoning about how such forecasts are constructed, and is identified as such in the video — it is not a claim published by the tracker.
"""

SPEC = {
    "slug": "game-money-lab",
    "pacote": "game-money-lab-004",
    "idioma": "en",
    "voz": "en-GB-RyanNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#131A26", "c1": "#5B2A86", "c2": "#3DDC97", "bg": "#F2F0FA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "game-money-lab-004.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
