#!/usr/bin/env python3
"""Monta a spec game-money-lab-007.

ALAVANCA ATACADA: A (conversao short -> inscrito).

NUMERO DE PARTIDA:

    game-money-lab-002  short  52 views  0 insc  ret 78,85%
    game-money-lab-003  short  91 views  0 insc  ret 54,79%
    game-money-lab-004  short  21 views  0 insc  ret 35,37%
    game-money-lab-005  short   6 views  0 insc  ret 27,43%

    canal inteiro: 171 views, ZERO inscritos
    os longos: 0, 1, 0 e 0 view. O short e o unico que recebe alguem.

O QUE DEU CERTO: a retencao do 002, 78,85%, e a distribuicao do 003, 91 views.

O QUE NAO DEU: converter. Quatro shorts, zero inscritos, e o topo da serie
esta CAINDO — 52, 91, 21, 6.

O QUE MUDEI. Os eixos anteriores sao todos sobre o dinheiro DOS OUTROS:
quanto a GTA 6 cobra, quantos foram demitidos, quantas assinaturas a peticao
juntou. Pelo aprendizado 504 nenhum deles converte, porque o dinheiro nao e do
espectador e nao ha escolha dele em lugar nenhum. O 006 ja tinha corrigido
metade disso (a moeda do jogo e o dinheiro dele), e este vai ao fim: alem de
ser o dinheiro dele, existe uma ESCOLHA com prazo, e a conta e feita no
historico de compras dele.

O eixo: o direito de retratacao de catorze dias, e as tres condicoes que
precisam valer JUNTAS para que ele se perca em conteudo digital. O botao de
reembolso da loja e uma politica que a loja escreve; o direito e outra coisa.

OS NUMEROS, e as duas rotas institucionais

  - Prazo de catorze dias para contratos a distancia, sem precisar justificar.
  - Em conteudo digital nao fornecido em suporte material, o direito so se
    perde se TRES coisas valerem ao mesmo tempo: consentimento previo expresso
    para comecar a execucao, reconhecimento de que com isso o direito se perde,
    e confirmacao disso entregue pelo fornecedor.
  - A excecao e de interpretacao estrita.

    rota 1  EUR-Lex — Diretiva 2011/83/UE, artigo 16, alinea (m), com o
            artigo 8(7) (confirmacao do contrato, incluindo a confirmacao do
            consentimento e do reconhecimento) e o artigo 9(1) (catorze dias)
    rota 2  Comissao Europeia, portal Your Europe (europa.eu/youreurope) —
            "Returns and the right of withdrawal", que enumera as mesmas tres
            condicoes cumulativas

O QUE FICOU DE FORA, e o video diz em voz alta

  - A politica de reembolso de QUALQUER loja, com as horas e os dias dela.
    Isso e uma fonte comercial so, muda quando a empresa quiser, e nao passa
    na regra das duas rotas. O video manda o espectador ler a da loja dele.
  - Qualquer valor em dinheiro. Depende da compra de cada um.
  - Qualquer promessa de que o dinheiro volta. O video descreve o direito
    publicado e a conta; nao promete resultado, e diz isso.
  - Fora da UE e do EEE nada disto se aplica, e o video abre dizendo isso.
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


# ---------------------------------------- 1. The button is not the right
T("The refund button", "and the right",
  "Every store has a refund button. It has rules, and the store wrote those "
  "rules. That is a policy.",
  cap="The button is not the right")
T("If you bought in Europe", "there is also a law",
  "If you bought from a seller in the European Union or the wider European "
  "Economic Area, there is also a right. A law wrote that one.")
I("They are not the same", "and the gap is money",
  "They are not the same thing, and the difference between them is worth "
  "money to you.")
T("A policy can change", "a right cannot",
  "A company can rewrite its policy next Tuesday and owes you no warning. It "
  "cannot rewrite the law that way.")
T("And you already have both", "most people use only one",
  "You almost certainly have both of these available to you. Most people "
  "only ever reach for the one with the button on it.")
T("Say the limit first", "outside Europe this is not yours",
  "One limit before anything else. Outside the Union and the Economic Area "
  "none of this applies to you, and the store policy is what you have.")
I("What you get by the end", "your own purchase list, sorted",
  "By the end you will be able to open your own purchase history and say "
  "which purchases are still inside the window and which are not.")
T("Not from my numbers", "from yours",
  "Not from my numbers. From your dates, on your account, in about ten "
  "minutes.")
T("And the rule is not about the game", "it is about how you bought it",
  "And notice what the rule is not about. It is not about the game. It is "
  "about how and when you bought it.")

# ---------------------------------------- 2. Fourteen days
T("Fourteen days", "and no reason needed",
  "The right is the right of withdrawal on distance contracts. Fourteen days, "
  "and you do not have to give a reason.",
  cap="Fourteen days, and when they start")
T("No reason needed", "is the part people skip",
  "No reason needed is the part almost everyone skips. You are not required "
  "to justify anything, or to have a complaint.")
I("For digital content", "the clock starts at the contract",
  "For a service or for digital content, the clock starts when the contract "
  "is concluded. That is the purchase, not the play session.")
I("For a boxed copy", "the clock starts at delivery",
  "For physical goods it starts at delivery instead. A boxed edition follows "
  "the parcel, not the download.")
T("So write the receipt date", "not the day you played",
  "So the first thing to write down is the date on the receipt. Not the day "
  "you got round to playing it.")
T("Fourteen days is short", "most of a library is outside it",
  "Fourteen days is short. Most of a library falls outside the window "
  "immediately, and that is fine.")
T("But sales cluster", "and so do purchases",
  "But purchases are not spread evenly through the year. They cluster around "
  "sales, and a sale is exactly when people buy things they never open.")
I("First number", "how many in fourteen days",
  "So the first number in this calculation is simply how many purchases you "
  "made in the last fourteen days.")

# ---------------------------------------- 3. As tres condicoes
T("Now the part that matters", "the right can be lost",
  "Now the part that decides everything. For digital content, this right can "
  "be lost.",
  cap="Three conditions, all at once")
I("But only if", "three things are all true",
  "But it is lost only if three separate things are true at the same time. "
  "Not one of them. All three.")
L("The first two", ["you consented to start immediately",
                    "you acknowledged losing the right"],
  "One: you gave express consent for performance to begin immediately, inside "
  "the fourteen days. Two: you acknowledged that you would lose the right by "
  "doing so.")
L("And the third", ["the trader confirmed it to you",
                    "in the confirmation of the contract"],
  "Three: the trader gave you confirmation of that consent and that "
  "acknowledgement, in the confirmation of the contract.")
T("All three", "not two of three",
  "All three, together. Two out of three does not close the door, and that is "
  "the whole reason this is worth ten minutes of your time.")
T("And it is read strictly", "which matters when it is close",
  "There is one more thing worth knowing. This exception is meant to be read "
  "strictly, which matters when a case sits near the line.")
I("So the question is never", "did I download it",
  "So the question is never just whether you downloaded something. It is what "
  "you were shown, what you agreed to, and what you were sent afterwards.")
T("Three questions", "with three answers you can check",
  "Three questions, and every one of them has an answer sitting in your own "
  "account or your own inbox.")

# ---------------------------------------- 4. A palavra que decide
T("One word decides", "started",
  "Everything turns on one word. Whether performance started, and whether you "
  "agreed to it starting.",
  cap="The word that decides: started")
I("Never downloaded", "never launched, never streamed",
  "A purchase you never downloaded, never launched and never streamed is the "
  "clean case. Performance did not start.")
T("And that pile is bigger", "than people expect",
  "That pile is bigger than people expect. A sale purchase nobody opened is "
  "one of the most ordinary things in this hobby.")
I("A pre-order counts too", "if nothing has been supplied",
  "A pre-order for something not released yet is worth checking for the same "
  "reason. Nothing has been supplied.")
T("The messy case", "the ten minutes you played",
  "The messy case is the one you launched for ten minutes and closed. There "
  "the store policy is usually where you end up.")
T("Ten minutes of play is not nothing", "it is just not this case",
  "Ten minutes of play is not nothing. It is simply not the case this "
  "right was written for, and pretending otherwise helps nobody.")
T("Which is why", "the two are kept apart here",
  "Which is exactly why these two are kept apart here instead of being sold "
  "to you as one thing.")
L("So make two piles", ["opened", "never opened"],
  "So sort your purchases into two piles. Opened, and never opened.")
I("The second pile", "is the one worth an email",
  "The second pile is the one worth writing an email about.")

# ---------------------------------------- 5. A conta
T("Ten minutes", "on your own account",
  "Here is the whole calculation. It runs on your own account, and it takes "
  "about ten minutes.",
  cap="Your own library, in ten minutes")
I("Step one", "the last fourteen days",
  "Step one: open your purchase history and look only at the last fourteen "
  "days. Everything older is outside the window.")
I("Step two", "date, and did you launch it",
  "Step two: for each purchase, write two things. The purchase date, and "
  "whether you ever launched it.")
I("Step three", "find the confirmation email",
  "Step three: search your inbox for the confirmation the seller sent after "
  "that purchase.")
L("Read it for two lines", ["consent to start immediately",
                            "acknowledgement that you lose withdrawal"],
  "Read that email for two lines: one where you consented to immediate "
  "performance, and one saying you lose the right of withdrawal because of it.")
I("Write down its date too", "a dated document beats a memory",
  "Write down the date on that email as well. It is dated, and a dated "
  "document beats a memory every single time.")
T("If both are there and you started it", "the store policy is your route",
  "If both lines are there and you did start it, the exception applies, and "
  "the store policy is the route you have.")
T("If you never started it", "the fourteen days are still running",
  "If you never started it, nothing was performed, and those fourteen days "
  "are still running.")
T("And if nothing ever arrived", "that is the third condition",
  "And if no confirmation ever arrived, that is the third condition, and it "
  "is not satisfied.")

# ---------------------------------------- 6. Onde isto para
T("Now the limits", "and they are real",
  "Now the limits, because they are real and I would rather you hear them "
  "from me.",
  cap="Where this stops")
T("Europe only", "and I am not describing anywhere else",
  "This is the Union and the Economic Area. Elsewhere you have the store "
  "policy and your local law, and I am not describing those.")
I("Details differ by country", "your consumer authority has yours",
  "The details differ from country to country. Your national consumer "
  "authority publishes the version that applies where you live.")
T("And there is a case I am skipping", "a seller outside, selling in",
  "There is also the seller based elsewhere who sells into the Union, and "
  "that one is genuinely complicated. I am leaving it alone here.")
T("A right existing", "is not a store agreeing",
  "A right existing does not mean a seller agrees with you on the first "
  "email. Dispute routes exist, and they take time.")
I("Expect it to be slow", "and keep one thread",
  "Expect a slow exchange rather than a quick answer, and keep every "
  "message in a single thread while it happens.")
T("None of this is legal advice", "and none of it is your contract",
  "None of this is legal advice, and none of it is about your particular "
  "contract, which I have not read.")
I("If the money is large", "talk to someone who does this",
  "If the amount is large enough to matter, talk to someone who does this "
  "professionally before you rely on any of it.")
T("What you get here", "is the right question",
  "What this gives you is the correct question, asked with the dates in front "
  "of you instead of from memory.")

# ---------------------------------------- 7. O recibo
T("Back to the third one", "because nobody checks it",
  "Back to the third condition, because it is the one almost nobody checks.",
  cap="The receipt you should have")
I("The trader must confirm", "the consent and the acknowledgement",
  "The trader has to give you confirmation of the contract, including the "
  "confirmation of your consent and your acknowledgement.")
T("That is an obligation", "not a courtesy",
  "That is an obligation on them. It is not a courtesy, and it is not "
  "something you have to ask nicely for.")
T("So the receipt is not clutter", "it is the document",
  "So the receipt sitting in your inbox is not clutter. It is the document "
  "that decides which of the two routes you are on.")
I("Keep them", "one folder, no effort",
  "Keep them. One folder, one filter rule, and the work is done for every "
  "purchase you make from now on.")
T("And before the next sale", "read the checkbox",
  "And before the next sale, read the box you are ticking instead of clicking "
  "past it on the way to the download.")
T("Because that tick", "is the choice",
  "Because that tick is the choice. It is the moment the right goes away, and "
  "it was worth something.")
C("Do it on one purchase", "and say what you found",
  "Run this on one purchase today and put in the comments what the "
  "confirmation email actually said. Subscribe if this is the kind of thing "
  "you want done with your own numbers instead of somebody else's.")

SHORT = [
    {"layout": "titulo", "kicker": "Bought it and never opened it",
     "sub": "in the last fourteen days",
     "nar": "If you bought a game in the last fourteen days and never "
            "launched it, you may still be able to withdraw.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Not the refund button",
     "sub": "in Europe this is a right",
     "nar": "That is not the store's refund button. In the European Union it "
            "is a right, and it works differently.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Open your purchase history",
     "sub": "and list what you never opened",
     "nar": "Open your purchase history. Write down every purchase from the "
            "last fourteen days that you never opened.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Nothing was performed",
     "sub": "so the exception does not apply",
     "nar": "For those, performance never started, so the exception that "
            "kills the right does not apply.", "sem_cap": True},
    {"layout": "cta", "kicker": "Three conditions",
     "sub": "and the receipt that decides them",
     "nar": "The three conditions, and the receipt that decides them, are in "
            "the full video below.", "sem_cap": True},
]

THUMB = {"l1": "The refund button", "l2": "is not the right"}

COPY = """# A policy is written by the store. A right is written by a law.

## TITULO
The Refund Button Is Not the Right: Fourteen Days, and Three Conditions

## DESCRICAO
Every store has a refund button, and the store wrote its rules. If you bought from a seller in the European Union or the wider European Economic Area, there is also something else: a right of withdrawal on distance contracts, fourteen days long, and you do not have to give a reason for using it. A company can rewrite its policy next Tuesday and owe you no warning. It cannot rewrite a law that way, and the gap between the two is worth money.

This video is about how and when you bought something, not about the game itself. The clock matters: for digital content the fourteen days run from the conclusion of the contract, which is the purchase, not the play session. For physical goods they run from delivery, so a boxed edition follows the parcel and not the download. That single distinction is the first thing to write down, and most people write down the wrong date.

Then the part that decides everything. For digital content not supplied on a tangible medium, this right can be lost — but only if three things are all true at the same time. One: you gave express consent for performance to begin immediately, inside the fourteen days. Two: you acknowledged that you would lose the right of withdrawal by doing so. Three: the trader gave you confirmation of that consent and acknowledgement in the confirmation of the contract. All three, together. Two out of three does not close the door, and the exception is meant to be read strictly.

So the calculation runs on your own account, in about ten minutes: open your purchase history, look only at the last fourteen days, write the purchase date and whether you ever launched it, then search your inbox for the confirmation the seller sent. A purchase you never downloaded, never launched and never streamed is the clean case — performance never started. A sale purchase nobody opened is one of the most ordinary things in this hobby, and a pre-order for an unreleased game is worth checking for the same reason.

There is a chapter on the limits, because they are real: outside the Union and the Economic Area none of this applies, national implementations differ, a right existing does not mean a seller agrees on the first email, and none of this is legal advice about your particular contract.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Do one thing and put the result here: open the confirmation email for your most recent purchase and tell me whether it actually contains the two lines — the consent to immediate performance, and the acknowledgement that you lose the right of withdrawal because of it. I am curious how often the third condition is simply missing, because in the receipts I have looked at it is far less consistent than you would expect from something a seller is obliged to send.

## HASHTAGS
#ConsumerRights #GameMoneyLab #DigitalPurchases

## TAGS
right of withdrawal, eu consumer rights, digital content refund, 14 day withdrawal period, distance contract, consumer rights directive, game refunds explained, pre order refund, digital purchase rights, eu consumer law games, refund policy vs law, purchase history check, game money lab, gaming economics, european economic area

## CONFIGURACOES DO STUDIO
- Idioma: Ingles (en) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Reino Unido | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Consultado em 26 de agosto de 2026. As afirmacoes vem de DUAS rotas institucionais independentes que se confirmam. (1) EUR-LEX (eur-lex.europa.eu): a Diretiva 2011/83/UE, com o prazo de catorze dias do artigo 9(1), a excecao do artigo 16, alinea (m), para conteudo digital nao fornecido em suporte material, e a obrigacao do artigo 8(7) de o fornecedor entregar a confirmacao do contrato incluindo a confirmacao do consentimento previo expresso e do reconhecimento. (2) COMISSAO EUROPEIA, portal Your Europe (europa.eu/youreurope), pagina "Returns and the right of withdrawal", que enumera as mesmas tres condicoes como CUMULATIVAS: consentimento para iniciar a execucao, reconhecimento da perda do direito, e confirmacao entregue pelo fornecedor. As duas rotas tambem registram que a excecao e de interpretacao estrita.

O QUE FOI DESCARTADO, e por que. (a) A politica de reembolso de qualquer loja especifica, com as horas de jogo e os dias que ela exige: e uma fonte comercial unica, muda quando a empresa decidir, e nao passa na regra das duas rotas oficiais — o video manda o espectador ler a politica da propria loja em vez de repetir numeros que envelhecem. (b) Qualquer valor em dinheiro: depende inteiramente da compra de cada pessoa, e quem tem esse numero e o espectador, no proprio historico. (c) Qualquer promessa de que o dinheiro volta: o video descreve o direito publicado e ensina a conta, e diz em voz alta que um direito existir nao significa que o vendedor concorde no primeiro contato. Isto e material educativo, nao aconselhamento juridico, e nao trata do contrato especifico de ninguem; as implementacoes nacionais diferem e a autoridade de consumo de cada pais publica a versao que vale ali.
"""

SPEC = {
    "slug": "game-money-lab",
    "pacote": "game-money-lab-007",
    "idioma": "en",
    "voz": "en-GB-RyanNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#181C2A", "c1": "#7C3AED", "c2": "#22D3EE", "bg": "#F4F4F8"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "game-money-lab-007.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
