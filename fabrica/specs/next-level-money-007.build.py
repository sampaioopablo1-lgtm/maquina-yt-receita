#!/usr/bin/env python3
"""Monta a spec next-level-money-007.

ALAVANCA ATACADA: A (conversao short -> inscrito).

NUMERO DE PARTIDA: 88 views no canal inteiro, ZERO inscritos, mediana de
1,16 view por dia por short e topo de 2,00. E a pior distribuicao da frota
entre os canais que ainda recebem alguem.

O QUE DEU CERTO: nada que se possa isolar. Nove shorts medidos, nenhum passou
de duas views por dia.

O QUE NAO DEU, e da para nomear com precisao: os tres eixos anteriores sao
AGREGADOS NACIONAIS.

    004  divida de cartao chegou a 1,26 trilhao de dolares
    005  inadimplencia chegou a 12,8 por cento
    006  BNPL chegou a 16 por cento dos adultos

Sao numeros corretos, de fontes boas, e nenhum deles e do espectador. Pelo
aprendizado 504 falta tudo: nao e o dinheiro dele, nao ha escolha dele, e a
conta que o video entrega e sobre o pais, nao sobre ele. O aprendizado 487 diz
a mesma coisa pelo outro lado — o dinheiro tem de ser DELE, em segunda pessoa.

O QUE MUDEI: o dinheiro deste video esta na conta do espectador AGORA, e uma
parte dele pode nao ser dele ainda. A escolha e dupla — quanto ele deposita, e
quando ele sai do emprego — e as duas contas saem de um papel que o
administrador do plano e OBRIGADO a entregar de graca.

OS NUMEROS, e as duas rotas institucionais

  - O que o proprio empregado deposita (elective deferrals), mais o rendimento
    disso, e 100 por cento dele desde o primeiro dia. Nao ha carencia.
  - A contrapartida do empregador PODE estar sujeita a um cronograma de
    aquisicao (vesting): o direito so se torna irrevogavel depois de um tempo.
  - Em planos safe harbor com a contrapartida basica e em SIMPLE 401(k), as
    contribuicoes obrigatorias do empregador sao 100 por cento adquiridas
    sempre.
  - O administrador do plano e obrigado a entregar a Summary Plan Description
    de graca, e ela diz quando o beneficio se torna adquirido.
  - Num plano de contribuicao definida o empregador pode mudar o valor da
    contribuicao futura, e conforme os termos do plano pode ate parar.

    rota 1  IRS (irs.gov) — "Retirement topics - Vesting", "401(k) plan
            overview" e o Issue Snapshot "Vesting schedules for matching
            contributions"
    rota 2  Department of Labor / EBSA (dol.gov) — "What You Should Know About
            Your Retirement Plan" e o "FAQs about Retirement Plans and ERISA"

O QUE FICOU DE FORA, e o video diz em voz alta

  - O LIMITE anual de contribuicao em dolares. Muda todo ano, e um numero de
    hoje deixaria o video errado em janeiro. O plano do espectador e a pagina
    do IRS tem o do ano corrente.
  - Os PRAZOS maximos de vesting em anos (cliff e graduado). Dependem do tipo
    de contribuicao e do plano, e eu nao os confirmei em duas rotas oficiais.
    O video manda ler o cronograma do proprio plano, que e onde o numero que
    vale para o espectador esta escrito.
  - Qualquer formula de contrapartida como se fosse padrao. Ela e do plano.
  - Qualquer conselho sobre sair ou nao sair de um emprego.
  - Isto e dos Estados Unidos. O video abre dizendo isso.
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


# ---------------------------------------- 1. Duas pilhas na mesma conta
T("One balance", "two kinds of money",
  "Your retirement account shows you one balance. Inside that balance there "
  "are two different kinds of money, and only one of them is unconditionally "
  "yours today.",
  cap="One balance, two kinds of money")
I("The first kind", "what you put in",
  "The first kind is what you put in yourself, taken out of your own pay "
  "before you ever saw it, plus whatever that money has earned since.")
I("The second kind", "what your employer added",
  "The second kind is what your employer added on top, the matching "
  "contribution, plus what that has earned.")
T("They look identical", "on the statement",
  "On the statement they look identical. They are added together, they are "
  "invested together, and the app shows you one number.")
T("They are not identical", "in law",
  "In law they are not identical at all, and the difference has a date "
  "attached to it.")
T("And nobody is hiding it", "it is simply not shown",
  "Nobody is hiding this from you, either. It is disclosed in a document, "
  "and the app that shows you the balance was never built to show you the "
  "split.")
T("Say the limit first", "this is the United States",
  "One limit before anything else. This describes retirement plans in the "
  "United States. If you are elsewhere, the rules where you are will be "
  "different.")
I("What you get by the end", "two numbers from your own paperwork",
  "By the end you will have two numbers, both taken from your own plan "
  "documents rather than from anything I say.")
T("And I do not know your plan", "which is the point",
  "I do not know your plan, and that is exactly the point. Every number that "
  "matters here is written in a document you are entitled to have.")

# ---------------------------------------- 2. O que ja e seu
T("Start with the good news", "your own money is yours",
  "Start with the good news, because it is genuinely good. The money you "
  "contribute yourself is one hundred per cent yours from the first day.",
  cap="Your own contributions are always yours")
I("No waiting period", "on your own deferrals",
  "There is no waiting period on it. There is no schedule, no cliff, and no "
  "condition attached to it.")
T("And the earnings too", "not just the deposits",
  "The earnings on that money are yours on the same terms. Not only what you "
  "put in, but what it grew into.")
I("However the job ends", "quit, laid off, or retire",
  "That holds however the job ends. Whether you resign, are laid off, or "
  "retire, your own contributions are untouched by any of it.")
T("So if you left today", "that part travels with you",
  "So if you walked out of that job today, that part of the balance travels "
  "with you. It is not at risk in any version of this.")
T("That is the part people worry about", "and it is the safe part",
  "That is usually the part people worry about, and it is the one part that "
  "was never in question.")
T("It survives a bad exit", "and a bad quarter",
  "It survives a bad exit, a bad quarter, and a company that changes its "
  "mind about the plan. It was never conditional to begin with.")
I("The worry belongs elsewhere", "on the employer's side",
  "The worry belongs on the other side of the balance, on the money your "
  "employer put in.")
T("Because that side", "can have a schedule",
  "Because that side can carry a schedule, and a schedule is a way of saying "
  "not yet.")
T("Which brings the word", "that decides the rest",
  "Which brings us to the one word that decides everything else, and it is a "
  "word most people have read without stopping on it.")

# ---------------------------------------- 3. Vesting
T("The word is vesting", "and it means owning",
  "The word is vesting. It is a dry word for a simple idea: when does this "
  "money stop being conditional and become irrevocably yours.",
  cap="Vesting: the word that decides the rest")
I("Employer contributions", "may be subject to a schedule",
  "Employer contributions can be subject to a vesting schedule. Your right to "
  "them becomes non forfeitable only after a period of time.")
T("Or they may not", "some plans vest immediately",
  "Or they may not be. Some plans vest employer money immediately, and that "
  "is a real difference between two jobs that pay the same salary.")
I("Two kinds of plan", "where it is always immediate",
  "There are plan types where the required employer contributions are one "
  "hundred per cent vested at all times, and safe harbor and SIMPLE plans are "
  "the ones named in the rules.")
T("So which one are you in", "is a real question",
  "So which one are you in is not a rhetorical question. It has an answer, "
  "and the answer is written down somewhere you can reach.")
T("Notice what this is not", "it is not a penalty",
  "Notice what this is not. It is not a penalty and it is not a trick. It is "
  "a condition that was disclosed, and almost nobody read it.")
I("The forfeitable part", "is only the employer side",
  "And remember the boundary: only the employer side can be forfeited. Your "
  "own contributions never enter this conversation.")
T("Now the practical question", "where is it written",
  "So the practical question is simply where this is written, and who has to "
  "give it to you.")

# ---------------------------------------- 4. O documento
T("The document has a name", "and they owe it to you",
  "The document has a name. It is called the Summary Plan Description, and "
  "the plan administrator is obliged to provide it to participants free of "
  "charge.",
  cap="The document they owe you, free")
I("Free of charge", "is the part to remember",
  "Free of charge is the part worth remembering, because asking for it is not "
  "a favour you are requesting.")
L("What it has to tell you", ["when you can join the plan",
                              "how service and benefits are counted",
                              "when benefits become vested"],
  "It tells participants when they can begin to take part, how service and "
  "benefits are calculated, and when benefits become vested.")
T("That third line", "is the one you came for",
  "That third line is the one you came for. It is the schedule, in your own "
  "plan, in writing.")
T("And it is a summary on purpose", "written to be read",
  "It is called a summary because it is meant to be read by people who do "
  "not do this for a living. That is the entire design of the document.")
T("It also covers", "how benefits are paid and claimed",
  "It also covers when and in what form benefits are paid, and how to file a "
  "claim, which matters later and matters less today.")
I("One more thing it will show", "the contribution formula",
  "It will also describe how the employer contribution is worked out, which "
  "is the other number you need.")
T("And one honest caveat", "the future is not promised",
  "One honest caveat while we are here. In a defined contribution plan the "
  "employer may change future contributions, and depending on the plan terms "
  "may stop them.")
T("So this is about", "what is already there",
  "So this calculation is about the money already sitting in the account, not "
  "about a promise stretching into next decade.")

# ---------------------------------------- 5. As duas contas
T("Now the arithmetic", "two numbers, one afternoon",
  "Now the arithmetic. Two numbers, and both come out of that one document in "
  "an afternoon.",
  cap="Two numbers from your own paperwork")
I("Step one", "find the contribution formula",
  "Step one: find the formula. How much does the employer add, and up to what "
  "share of your pay does it keep adding.")
I("Step two", "compare it with what you put in",
  "Step two: compare that threshold with what you are actually contributing "
  "right now, which is on your pay statement.")
T("If you are below the threshold", "that gap has a price",
  "If you are contributing below the point where the employer stops matching, "
  "the difference between those two is money that was available and was not "
  "taken.")
T("Write that number down", "as a yearly figure",
  "Write it down as a yearly figure, not a monthly one. Yearly is the scale "
  "at which it stops feeling small.")
I("A note on that threshold", "it is a share of pay",
  "One note on that threshold. It is usually a share of your pay, so a "
  "raise moves it, and a contribution you set two years ago may no longer "
  "reach it.")
I("Step three", "find the vesting schedule",
  "Step three: find the vesting schedule, and find where you are on it "
  "today, counted in your own service.")
I("Step four", "multiply what is not yours yet",
  "Step four: work out how much of the employer money is not yet "
  "non forfeitable. That is the second number.")
T("Those two", "answer two different questions",
  "Those two numbers answer two different questions. The first is about how "
  "much you contribute. The second is about when you leave.")

# ---------------------------------------- 6. Onde a conta para
T("Now the limits", "and I would rather say them",
  "Now the limits of all of this, and I would rather say them than let you "
  "find them the hard way.",
  cap="Where the arithmetic stops")
T("No dollar limit here", "because it changes every year",
  "I have not given you the annual contribution limit in dollars. It changes "
  "every year, and a number recorded today would make this video wrong by "
  "January.")
I("No year counts either", "because they depend on the plan",
  "I have not given you the maximum vesting periods in years either. They "
  "depend on the kind of contribution and on the plan, and your schedule is "
  "the one that governs you.")
T("And no formula", "presented as standard",
  "And I have not described any matching formula as if it were standard. "
  "There is no standard one. There is the one in your plan.")
T("I also left rollovers alone", "on purpose",
  "I have left rollovers alone entirely as well. Moving an account "
  "elsewhere has its own rules, and mixing them in would make both harder "
  "to follow.")
T("This is not advice", "about your job",
  "None of this is advice about whether to stay in a job or leave one. That "
  "decision has a dozen inputs and this is one of them.")
I("Nor is it tax advice", "or a recommendation",
  "It is not tax advice or an investment recommendation, and it is not about "
  "your particular plan, which I have not read.")
T("What it is", "is the right question",
  "What it is, is the right question asked with your own documents open "
  "instead of from memory.")

# ---------------------------------------- 7. A data
T("Which leaves the date", "and dates cost money",
  "Which leaves one thing, and it is the reason this is worth an afternoon "
  "rather than a shrug.",
  cap="The date that has a price")
T("A schedule is a calendar", "not a mood",
  "A vesting schedule is a calendar. It does not care how well the last "
  "quarter went or how the conversation with your manager felt.")
I("So before you hand in notice", "look at where you are on it",
  "So before anyone hands in notice, the schedule is worth one look. Where "
  "you are on it, and how far the next step is.")
T("Sometimes the answer is nothing", "and that is a fine answer",
  "Sometimes the answer is that nothing is at stake, because the plan vests "
  "immediately. That is a completely fine answer, and now it is a known one.")
T("Sometimes it is a few weeks", "and that is worth knowing",
  "And sometimes the answer is that a few weeks separate you from a number "
  "large enough to be worth a conversation about a start date.")
I("Either way", "you decide with the number",
  "Either way you make the decision holding the number, which is the only "
  "version of this that respects your time.")
T("And the first number", "you can fix this month",
  "The first number, the one about how much you contribute, is not even about "
  "leaving. It is something you can change this month.")
C("Ask for the document today", "and say what you found",
  "Ask your plan administrator for the Summary Plan Description today, and "
  "put in the comments whether your employer money vests immediately or on a "
  "schedule. Subscribe if you want the version of this where the numbers are "
  "yours instead of the country's.")

SHORT = [
    {"layout": "titulo", "kicker": "Your retirement balance",
     "sub": "is two kinds of money",
     "nar": "Your retirement balance is one number made of two kinds of "
            "money, and only one of them is unconditionally yours today.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "What you put in",
     "sub": "is yours from day one",
     "nar": "What you contribute yourself is one hundred per cent yours from "
            "the first day, earnings included.", "sem_cap": True},
    {"layout": "titulo", "kicker": "What your employer added",
     "sub": "can be on a schedule",
     "nar": "What your employer added can be subject to a vesting schedule, "
            "which means not yours yet.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Ask for the Summary Plan Description",
     "sub": "they must give it free",
     "nar": "Ask your plan administrator for the Summary Plan Description. "
            "They have to provide it free of charge, and it says when "
            "benefits vest.", "sem_cap": True},
    {"layout": "cta", "kicker": "Two numbers", "sub": "from your own plan",
     "nar": "The two numbers to pull out of it, and what each one decides, "
            "are in the full video below.", "sem_cap": True},
]

THUMB = {"l1": "One balance", "l2": "two kinds of money"}

COPY = """# The statement adds them up. The law does not.

## TITULO
One Balance, Two Kinds of Money: What Vesting Decides in Your 401(k)

## DESCRICAO
Your retirement account shows you a single balance, and inside it there are two different kinds of money. The first is what you contributed yourself, taken out of your own pay, plus everything it has earned since. The second is what your employer added on top. On the statement they look identical — added together, invested together, one number in the app. In law they are not identical at all, and the difference has a date attached to it.

The good news is genuinely good, and it is the part people worry about for no reason: your own contributions, and the earnings on them, are one hundred per cent yours from the first day. There is no waiting period, no schedule, and no condition. If you left the job today, that part of the balance travels with you.

The employer side is where the word vesting lives. Employer contributions can be subject to a vesting schedule, which means your right to them becomes non forfeitable only after a period of time — or they may vest immediately, which is a real difference between two jobs paying the same salary. There are plan types where required employer contributions are one hundred per cent vested at all times, and safe harbor and SIMPLE plans are the ones the rules name. Which one you are in is not a rhetorical question. It has an answer, and the answer is written down.

It is written in the Summary Plan Description, and the plan administrator is obliged to provide it to participants free of charge. It tells you when you can join, how service and benefits are calculated, and when benefits become vested — that third line is the one you came for. It also describes how the employer contribution is worked out, which is the other number you need.

From those two facts the video builds a calculation in four steps, all of it on your own paperwork: find the matching formula and the pay threshold where it stops, compare it with what you are actually contributing, write the gap down as a yearly figure, then find the vesting schedule and work out how much of the employer money is not yet non forfeitable. Those two numbers answer two different questions — how much you contribute, and when you leave. One of them you can change this month.

There is a chapter on the limits, because they matter: no dollar contribution limit is quoted here, no vesting periods in years, and no matching formula presented as standard — those belong to your plan and to the current year, not to a video.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Do one thing and report back: ask your plan administrator for the Summary Plan Description — they have to give it to you free — and tell me whether your employer contributions vest immediately or on a schedule. I would like to see how that splits, because in the conversations I have had almost nobody knows which of the two they are in, and the ones who guessed guessed wrong about as often as they guessed right.

## HASHTAGS
#Retirement #401k #NextLevelMoney

## TAGS
401k vesting, employer match vesting schedule, summary plan description, elective deferrals vested, erisa participant rights, safe harbor 401k, simple 401k, retirement plan documents, employer matching contributions, non forfeitable benefits, leaving a job 401k, retirement plan basics, personal finance us, next level money, plan administrator

## CONFIGURACAO DE STUDIO
- Language: English (en-US) | Category: Education (27)
- Not made for kids
- Altered or synthetic content disclosure: YES (AI-generated voice)
- Location: United States | Licence: Standard YouTube Licence
- Mid-roll ads: on (runtime over eight minutes)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
Consultado em 26 de agosto de 2026. As afirmacoes vem de DUAS rotas institucionais independentes que se confirmam. (1) IRS (irs.gov): as paginas "Retirement topics - Vesting", "401(k) plan overview" e o Issue Snapshot "Vesting schedules for matching contributions". (2) DEPARTMENT OF LABOR / EBSA (dol.gov): a publicacao "What You Should Know About Your Retirement Plan" e o "FAQs about Retirement Plans and ERISA". As afirmacoes centrais sao quatro: o que o proprio participante contribui, mais o rendimento disso, e cem por cento adquirido desde o primeiro dia; a contrapartida do empregador pode estar sujeita a um cronograma de aquisicao, tornando-se irrevogavel so depois de um periodo; em planos safe harbor com a contrapartida basica e em SIMPLE 401(k) as contribuicoes obrigatorias do empregador sao cem por cento adquiridas sempre; e o administrador do plano e obrigado a fornecer a Summary Plan Description de graca, documento que informa quando os beneficios se tornam adquiridos.

AVISO SOBRE OS NUMEROS — o que foi descartado e por que. (a) O LIMITE anual de contribuicao em dolares nao aparece: ele e reajustado todo ano, e um numero gravado hoje deixaria este video errado em janeiro; o plano do espectador e a pagina corrente do IRS tem o valor que vale para ele. (b) Os PRAZOS maximos de aquisicao em anos, na forma cliff ou graduada, nao aparecem: dependem do tipo de contribuicao e do desenho do plano, eu nao os confirmei nas duas rotas, e o unico cronograma que governa o espectador e o do plano dele. (c) Nenhuma formula de contrapartida e apresentada como padrao, porque nao existe padrao — existe a do plano. (d) Nao ha aqui recomendacao sobre sair ou permanecer num emprego, nem aconselhamento fiscal ou de investimento, nem analise do plano especifico de ninguem. Um plano de contribuicao definida tambem permite ao empregador alterar a contribuicao futura e, conforme os termos, interrompe-la — por isso a conta deste video e sobre o dinheiro que ja esta na conta, e nao sobre promessa futura. Isto descreve regras dos Estados Unidos; fora dali as regras sao outras.
"""

SPEC = {
    "slug": "next-level-money",
    "pacote": "next-level-money-007",
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
                           "next-level-money-007.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
