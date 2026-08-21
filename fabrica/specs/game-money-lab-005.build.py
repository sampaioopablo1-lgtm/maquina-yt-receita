#!/usr/bin/env python3
"""Monta a spec game-money-lab-005.

CANAL. Veredito `sem dado`: 2 longos e 2 shorts medidos, longo a 0,00 v/d e
short a 19,37. A regra manda seguir a memoria do NICHO, e o nicho aqui e
grande — os outliers do banco medem de 9,4 mil a 56 mil views/dia. Faixa
inteira de 12 a 15 min autorizada.

EIXO. Os quatro titulos publicados sao: 300 milhoes por jogo (duas vezes,
longo e short), demissoes de 2026 com previsao revisada em 78%, e GTA 6 a
oitenta dolares. O banco lista tres eixos com ZERO usados — `preco dos jogos`,
`crise da industria` e `demissoes` — e os TRES ja foram cobertos por esses
titulos.

  QUARTA vez em tres horas que o `usado_em` mente. No labtreinamento faltava
  marcacao, no seviye-seviye tambem, e aqui outra vez. O campo nao serve como
  prova em direcao nenhuma (aprendizado 421); o que decide e a lista de
  titulos publicados. Pauta veio de pesquisa nova.

A PAUTA, datada, institucional, e sobre DINHEIRO — que e o assunto do canal.

  Em 16 de junho de 2026 a Comissao Europeia respondeu formalmente a
  iniciativa de cidadaos "Stop Destroying Videogames". O documento e o
  C(2026) 4110 final e esta hospedado no proprio portal da UE.

    assinaturas verificadas ..... 1.294.188
    limiar que obriga resposta ... 1.000.000
    decisao ..................... nao pode propor obrigacao legal de manter
                                  jogos jogaveis apos o fim do suporte
                                  comercial, "nesta etapa"
    motivos ..................... propriedade intelectual e direitos autorais,
                                  e onus desproporcional
    o que ofereceu no lugar ..... ate o FIM DE 2026, abrir dialogo com a
                                  industria e representantes de consumidores
                                  para redigir um CODIGO DE CONDUTA sobre o
                                  fim de vida dos jogos; mais campanha de
                                  conscientizacao sobre direitos ja existentes
    o codigo trataria de ........ rotulagem transparente indicando possivel
                                  descontinuacao, e possiveis parcerias com
                                  instituicoes de patrimonio cultural
    proximo alvo da campanha .... incluir os conceitos no Digital Fairness Act

  Conferido em duas passagens com veiculos independentes que batem, e a fonte
  primaria e institucional: a pagina de resposta da Comissao no
  citizens-initiative.europa.eu, mais analise do escritorio Lewis Silkin.

A TESE, e ela e economica e nao politica: 1,29 milhao de assinaturas produziu
um CODIGO VOLUNTARIO, nao uma lei. Para o canal, a pergunta certa nao e se
isso e justo — e o que muda no balanco de uma editora quando a exigencia e
voluntaria em vez de legal. Obrigacao legal entra como passivo provisionado;
codigo de conduta entra como custo de reputacao. Sao linhas diferentes, e
decidem coisas diferentes.

FORMATO. Os tres outliers do proprio canal tem a mesma estrutura: cifra
concreta, dois pontos, e o mecanismo. "$300 Million Per Game: The Math That
Broke AAA". O titulo daqui segue isso com o numero de assinaturas.

O QUE O VIDEO NAO FAZ: nao diz se a decisao foi certa ou errada, nao preve o
conteudo do codigo (ele nao existe ainda) e nao promete o que o Digital
Fairness Act vai conter.
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
T("One point two nine million", "and the answer was no",
  "One million two hundred ninety four thousand one hundred eighty eight "
  "verified signatures. The answer was no.",
  cap="The number, and the answer")
I("What was asked", "keep games playable",
  "The ask was narrow. Stop publishers from making purchased games permanently "
  "unplayable once they switch the servers off.")
I("Who answered", "the European Commission",
  "The answer came from the European Commission, on the sixteenth of June this "
  "year.")
I("Why they had to answer", "the one million threshold",
  "They had to answer. A European citizens' initiative that clears one million "
  "verified signatures obliges Brussels to respond formally.")
I("And it cleared it", "by nearly three hundred thousand",
  "This one cleared the threshold by nearly three hundred thousand.")
I("The wording matters", "at this stage",
  "The reply says the Commission cannot propose a legal obligation, and it "
  "adds three words that most coverage dropped: at this stage.")
I("Why those words matter", "it is not a permanent no",
  "Those three words are the difference between a door closed and a door "
  "closed for now. They do not promise anything, but they do not foreclose "
  "anything either.")
I("What it is not", "not a vote",
  "One clarification, because the framing gets this wrong constantly: this was "
  "not a vote and nobody was outvoted. A citizens' initiative obliges a formal "
  "reply, not a particular answer.")
T("What this video is", "the balance sheet, not the politics",
  "Now, what this channel is for.")
I("Not whether it was fair", "not the argument",
  "I am not going to argue whether that decision was fair. That argument is "
  "everywhere and it does not need me.")
I("The question here", "what changes on the books",
  "The question here is narrower and it is the one nobody asks: what actually "
  "changes on a publisher's books when the requirement is voluntary instead of "
  "legal.")
L("What is coming", ["What was actually decided",
                     "Why a code is not a law, in accounting terms",
                     "What the code would cover",
                     "What happens next"],
  "What was decided, why a code and a law land in different columns, what the "
  "code would cover, and what happens next.")
I("One promise", "no guessing",
  "And one promise: no guessing. The code of conduct does not exist yet, so I "
  "will not tell you what is in it.")
I("Start with the decision", "word for word",
  "Start with what was actually decided:")

# ------------------------------------------------------------------- cap 2
T("Cannot propose", "the two stated reasons",
  "The Commission gave two reasons for not proposing a legal obligation, and "
  "both are worth understanding because both are about cost.",
  cap="What was actually decided")
I("Reason one", "intellectual property",
  "The first is intellectual property and copyright. A rule forcing a "
  "publisher to keep something running touches what the rightsholder owns and "
  "controls.")
I("Reason two", "disproportionate burden",
  "The second is proportionality. The Commission judged the burden of such a "
  "rule to be disproportionate to the problem it solves.")
I("What proportionality means here", "cost against benefit",
  "Proportionality in this context is a cost test. The cost of compliance is "
  "weighed against the harm being prevented.")
I("Who carries that cost", "every publisher, not the big ones",
  "And here is the part that decides these arguments: a server-keeping "
  "obligation is cheap for a company running hundreds of titles and expensive "
  "for one running two.")
B("Same rule, different weight", ["Large publisher", "Small studio"],
  [22, 100],
  "The same obligation is a rounding error for one and a structural cost for "
  "the other. Regulators weigh that, and it usually decides the outcome.")
I("What they offered instead", "a code of conduct",
  "What the Commission offered instead is a code of conduct, to be drawn up "
  "with the industry and with consumer representatives.")
I("And a deadline", "before the end of this year",
  "With a deadline attached: the exchange starts before the end of this year.")
I("Plus one more thing", "an awareness campaign",
  "Plus an awareness campaign about consumer rights that already exist. That "
  "part is easy to dismiss and I will come back to it.")
I("Now the accounting", "the actual difference",
  "Now the part this channel exists for:")

# ------------------------------------------------------------------- cap 3
T("Two different columns", "liability against reputation",
  "A legal obligation and a voluntary code do not sit in the same place on a "
  "balance sheet. That is the whole difference.",
  cap="Why a code is not a law, in accounting terms")
I("A legal obligation", "becomes a provision",
  "A legal obligation to keep something running is a future cost you can be "
  "forced to pay. Accounting treats that as a provision — money set aside "
  "against a liability.")
I("What a provision does", "it reduces reported profit",
  "Setting aside a provision reduces reported profit in the period you set it "
  "aside, before a single dollar is spent.")
I("And it is visible", "auditors see it",
  "It is also visible. Auditors test it, and it appears in the accounts every "
  "year until it is settled.")
I("There is a second effect", "it changes decisions upstream",
  "There is a second effect that matters more than the accounting entry. A "
  "provisionable duty changes what gets greenlit in the first place.")
I("How", "the shutdown cost moves forward",
  "If ending a game carries a known future cost, that cost belongs in the "
  "business case at the start — not at the end, when the decision is already "
  "made.")
I("That is the real lever", "not the money, the timing",
  "That is the real lever people miss. The point of a legal duty is rarely the "
  "money itself. It is that the money appears early enough to change the "
  "decision.")
I("A voluntary code", "no provision required",
  "A voluntary code creates no such liability. There is nothing enforceable to "
  "provision against, so nothing hits the balance sheet.")
B("Where each one lands", ["Legal duty: provision", "Code: no entry"],
  [100, 12],
  "One changes the numbers. The other changes the press release.")
I("Does that mean the code is nothing", "no, and here is why",
  "Does that make the code worthless? No, and I want to be careful here.")
I("Codes do bite", "through other channels",
  "Codes bite through other channels: platform requirements, retailer terms, "
  "and consumer-protection cases that cite the code as the accepted standard.")
I("That last one matters", "the standard becomes evidence",
  "That last route is the strongest. Once an industry agrees a standard, "
  "falling below it becomes evidence in a dispute — even without a specific "
  "law.")
I("So the honest summary", "weaker, not empty",
  "So the honest summary is: weaker than a law, not the same as nothing. And "
  "which one it ends up closer to depends on what gets written.")
I("One more difference", "who it binds",
  "And one difference that decides a lot: a law binds everyone in the market. "
  "A code binds whoever signs it.")
I("Which creates a gap", "the ones who do not sign",
  "Which means the publishers most likely to shut a game down without warning "
  "are also the ones least likely to sign. Voluntary standards tend to be "
  "adopted by those who already comply.")
I("Is that fatal", "not necessarily",
  "That is not necessarily fatal — platform terms can make a code effectively "
  "mandatory for anyone selling through a major store. But that is the "
  "platform enforcing it, not the regulator.")

# ------------------------------------------------------------------- cap 4
T("What the code would cover", "two named things",
  "The reply names two things the code would aim at. Both are cheap to "
  "implement, and that is not an accident.",
  cap="What the code would cover")
I("First", "transparent labelling",
  "The first is transparent labelling: telling buyers, at the point of sale, "
  "that a game may be discontinued.")
I("Why that is cheap", "it is a string of text",
  "That costs almost nothing to implement. It is a line of text on a store "
  "page.")
I("But there is a catch", "who writes the wording",
  "The catch is the wording. A label saying this game requires an online "
  "connection tells you almost nothing. A label saying support may end and the "
  "game will then be unplayable tells you everything.")
I("Same cost, different value", "one sentence apart",
  "Both cost the same to implement. That is why the drafting matters more "
  "than the existence of the label.")
I("But cheap is not useless", "it moves the decision",
  "Cheap does not mean useless. A disclosure at the point of sale moves the "
  "decision to before the purchase, which is where it belongs.")
I("Second", "heritage institutions",
  "The second is possible partnerships between publishers and cultural "
  "heritage institutions — museums, archives, libraries.")
I("What that solves", "preservation, not access",
  "Be precise about what that solves. It is about preserving the work for the "
  "record. It is not about keeping your copy running.")
I("Those are different problems", "and get conflated",
  "Those two get conflated constantly. Preservation is a heritage question. "
  "Continued access is a consumer question. The reply answers the first more "
  "than the second.")
T("The awareness campaign", "the part everyone dismissed",
  "Now back to the piece I said I would return to.")
I("Existing rights", "already on the books",
  "The Commission also committed to raising awareness of consumer rights that "
  "already exist in EU law.")
I("Why that is not filler", "unused rights",
  "It sounds like filler. It is not entirely. An unused right and a "
  "nonexistent right produce the same outcome, and only one of them is fixable "
  "without new legislation.")
I("The catch", "enforcement is individual",
  "The catch is that enforcing an existing right usually falls to the "
  "individual buyer, one complaint at a time. That is slow, and most people "
  "never start.")
I("And the amounts are small", "which is the point",
  "The amounts also work against it. A single game purchase is small enough "
  "that pursuing it costs more time than it returns, which is exactly why "
  "collective mechanisms exist elsewhere.")
I("Worth knowing anyway", "the right exists",
  "Still worth knowing the right exists. A refusal is much harder to sustain "
  "against a buyer who cites the specific rule than against one who is simply "
  "annoyed.")

# ------------------------------------------------------------------- cap 5
T("Why servers get switched off", "the cost that never appears in the ask",
  "Before the next steps, the piece the petition side rarely puts a number "
  "against — and this channel should.",
  cap="Why servers get switched off at all")
I("The naive view", "servers are cheap now",
  "The common argument is that hosting is cheap now, and for raw compute that "
  "is broadly true.")
I("But hosting is not the cost", "it is the smallest part",
  "Hosting is usually the smallest line. The expensive parts are the ones that "
  "need people.")
I("First", "security and patching",
  "First, security. A live service holding accounts and payment data has to be "
  "patched for as long as it is up, and that requires engineers who understand "
  "that codebase.")
I("Second", "platform certification",
  "Second, platform requirements change. Console and store operators update "
  "their rules, and a game that stays online has to keep being recertified.")
I("Third", "licences expire", 
  "Third, and this is the one that surprises people: licensed content. Music, "
  "likenesses, sports rosters and branded items are licensed for a term, and "
  "terms end.")
I("That last one is structural", "you cannot just keep serving it",
  "That last one cannot be solved by goodwill. Once a music licence lapses, "
  "continuing to serve that track is not generosity — it is infringement.")
B("Where the money goes", ["Hosting", "People and licences"], [16, 100],
  "So the honest picture is that keeping a game alive is mostly a staffing and "
  "rights problem, not a server problem.")
I("Why this matters here", "it explains the reply",
  "This is why the Commission's proportionality reasoning is not just a "
  "brush-off. The cost being weighed is real, and it is recurring.")
I("But it cuts both ways", "the offline question",
  "It cuts both ways though. Most of those costs apply to keeping a game "
  "ONLINE. They do not obviously apply to leaving behind a version that runs "
  "without the company.")
I("And that is the actual ask", "not perpetual servers",
  "And that is closer to what the initiative asked for: not perpetual "
  "servers, but not deliberately breaking what people bought.")
I("Which is why the code matters", "that distinction can be written down",
  "Which is exactly the distinction a code of conduct could write down — and "
  "the reason it is worth watching who drafts it.")
T("What happens next", "two tracks",
  "Two things run in parallel from here, and they move at very different "
  "speeds.",
  cap="What happens next")
I("Track one", "the code itself",
  "Track one is the code. The exchange with industry and consumer groups is "
  "meant to start before the end of this year.")
I("What to watch there", "who is at the table",
  "The thing to watch is not the announcement. It is who sits at the table, "
  "because a code written mostly by one side reads like that side.")
I("Track two", "the Digital Fairness Act",
  "Track two is legislative. The campaign has said its next target is folding "
  "these ideas into the Digital Fairness Act.")
I("Why that route", "different vehicle, same goal",
  "That is a different vehicle for the same goal — and it does not need the "
  "Commission to have agreed with them in June.")
B("Two speeds", ["Code of conduct", "Legislation"], [100, 30],
  "A code can exist within a year. Legislation moves in years, and the "
  "difference in speed is itself a reason regulators reach for codes.")
I("What I will not predict", "either outcome",
  "I am not going to predict either one. The code has not been drafted and the "
  "Act has not been finalised.")
T("What to actually watch", "three checkable things",
  "So here is what to actually watch, and all three are checkable rather than "
  "arguable.")
I("One", "does the exchange start on time",
  "One: does the exchange actually begin before the end of this year. That is "
  "a date, and dates either happen or do not.")
I("Two", "does labelling appear at point of sale",
  "Two: does discontinuation labelling start showing up on store pages. You "
  "will see that before any document is published.")
I("Three", "does anyone cite the code",
  "Three: does the code get cited in a consumer dispute. That is the moment a "
  "voluntary standard starts behaving like a rule.")
C("Game Money Lab", "the numbers, not the noise",
  "If you buy games in the EU, the useful thing today is small: check whether "
  "the store page says anything about discontinuation. If this was worth your "
  "time, subscribe.")


# -------------------------------------------------------------------- short
SHORT = [
    {"layout": "titulo", "kicker": "1,294,188 signatures",
     "sub": "the EU said no",
     "nar": "One point two nine million verified signatures asked the EU to "
            "stop publishers killing games. The answer was no.",
     "sem_cap": True},
    {"layout": "item", "kicker": "The reason", "preco": "IP and proportionality",
     "nar": "The Commission said it cannot propose a legal obligation, citing "
            "intellectual property and disproportionate burden.",
     "sem_cap": True},
    {"layout": "item", "kicker": "What they offered",
     "preco": "a voluntary code",
     "nar": "Instead: a code of conduct, drawn up with industry, starting "
            "before the end of this year.", "sem_cap": True},
    {"layout": "item", "kicker": "Why that matters",
     "preco": "no provision, no entry",
     "nar": "A legal duty becomes a provision on the balance sheet. A "
            "voluntary code creates no liability, so nothing hits the books.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Game Money Lab", "sub": "weaker, not empty",
     "nar": "Codes still bite through disputes, once they become the accepted "
            "standard.", "sem_cap": True},
]

COPY = """# 1,294,188 signatures, and the EU chose a code of conduct

## TITULO
1,294,188 Signatures: Why the EU Chose a Code of Conduct Over a Law

## DESCRICAO
1,294,188 verified signatures asked the European Commission to stop publishers making purchased games permanently unplayable. On 16 June 2026 the Commission formally replied: it cannot, at this stage, propose a legal obligation to keep games playable after they stop being provided commercially.

This video is not about whether that was fair — that argument is everywhere and doesn't need me. It's about the question nobody asks: what actually changes on a publisher's books when a requirement is voluntary instead of legal.

WHAT WAS DECIDED

A European citizens' initiative that clears 1,000,000 verified signatures obliges Brussels to respond formally. This one cleared it by nearly 300,000. The reply gave two reasons for declining a legal obligation: intellectual property and copyright constraints, and proportionality — the burden being disproportionate to the problem. Proportionality is a cost test, and it usually decides these outcomes: a server-keeping obligation is a rounding error for a company running hundreds of titles and a structural cost for one running two.

WHY A CODE IS NOT A LAW, IN ACCOUNTING TERMS

A legal obligation to keep something running is a future cost you can be forced to pay — accounting treats that as a PROVISION, money set aside against a liability. Setting aside a provision reduces reported profit in the period, before a single dollar is spent, and auditors test it every year until it's settled.

A voluntary code creates no such liability. There is nothing enforceable to provision against, so nothing hits the balance sheet. One changes the numbers; the other changes the press release.

Does that make the code worthless? No — and I'm careful here. Codes bite through other channels: platform requirements, retailer terms, and consumer-protection cases that cite the code as the accepted standard. That last route is the strongest: once an industry agrees a standard, falling below it becomes evidence in a dispute even without a specific law. Honest summary — weaker than a law, not the same as nothing.

WHAT THE CODE WOULD COVER

Two named things, both cheap to implement, which is not an accident. First, transparent labelling: telling buyers at the point of sale that a game may be discontinued — a line of text on a store page, and cheap doesn't mean useless, because it moves the decision to before the purchase. Second, possible partnerships with cultural heritage institutions. Be precise about that one: it's about preserving the work for the record, not about keeping your copy running. Preservation is a heritage question; continued access is a consumer question, and the reply answers the first more than the second.

The Commission also committed to an awareness campaign about consumer rights that ALREADY exist. It sounds like filler and isn't entirely: an unused right and a nonexistent right produce the same outcome, and only one is fixable without new legislation. The catch is that enforcing an existing right usually falls to the individual buyer, one complaint at a time.

WHAT HAPPENS NEXT — AND THREE CHECKABLE THINGS

Two tracks run in parallel. The code: the exchange with industry and consumer groups is meant to start before the end of 2026 — watch who sits at the table, because a code written mostly by one side reads like that side. And legislation: the campaign has said its next target is folding these ideas into the Digital Fairness Act, a different vehicle for the same goal.

I predict neither. Instead, three things you can check rather than argue about: (1) does the exchange actually begin before the end of this year; (2) does discontinuation labelling start appearing on store pages; (3) does the code get cited in a consumer dispute — that's the moment a voluntary standard starts behaving like a rule.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
A question I genuinely want answered by people who buy in the EU: have you seen ANY store page that already tells you a game may be discontinued? Screenshot it if you have. That labelling is the first of the three checkable things in this video, and it will show up on storefronts long before any document is published.

## HASHTAGS
#StopKillingGames #GameIndustry #GameMoneyLab

## TAGS
stop killing games, european commission, game preservation, video game industry, digital fairness act, citizens initiative, game economics, publishers, code of conduct, consumer rights, eu regulation, live service games, server shutdown, gaming business, game industry analysis

## CONFIGURACOES DO STUDIO
- Idioma: Ingles (en) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Resposta da Comissao Europeia a iniciativa de cidadaos "Stop Destroying Videogames", de 16 de junho de 2026 (documento C(2026) 4110 final): 1.294.188 assinaturas verificadas contra o limiar de 1.000.000 que obriga resposta formal; a Comissao afirma que "nesta etapa" nao pode propor obrigacao legal de manter jogos jogaveis apos o fim da oferta comercial, citando propriedade intelectual/direitos autorais e onus desproporcional; em vez disso, compromete-se a iniciar ate o fim de 2026 um dialogo com a industria e representantes de consumidores para redigir codigo de conduta sobre o fim de vida dos jogos, com rotulagem transparente de possivel descontinuacao e possiveis parcerias com instituicoes de patrimonio cultural, alem de campanha sobre direitos ja existentes. Conferido em duas passagens de busca com veiculos independentes coincidentes; a fonte primaria e a pagina de resposta no citizens-initiative.europa.eu, portal oficial da UE. O video NAO avalia se a decisao foi correta, NAO preve o conteudo do codigo (que ainda nao foi redigido) e NAO afirma o que constara do Digital Fairness Act. A explicacao contabil sobre provisao e principio geral de reconhecimento de passivo, nao analise das demonstracoes de nenhuma empresa especifica.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/game-money-lab-005.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "game-money-lab",
    "pacote": "game-money-lab-005",
    "idioma": "en",
    "voz": "en-GB-RyanNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#12161F", "c1": "#2F7FD1", "c2": "#D9A13B",
               "bg": "#F3F5F8"},
    "thumb": {"l1": "1,294,188", "l2": "no law"},
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
    grava(SPEC, "fabrica/specs/game-money-lab-005.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
