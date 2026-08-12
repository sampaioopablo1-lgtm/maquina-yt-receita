#!/usr/bin/env python3
"""Gera a spec do next-level-money-003 — The Economics Behind Your Credit Score.

Fonte da pauta (PASSO 0, 05/08/2026, n=43 videos em ingles de 90 dias, grupo de
pares de canais do MESMO porte que praticam o formato "The Economics of X"):
  mediana do grupo ............ 4 views/dia
  formato que performa ........ "The Economics Behind [instituicao] Explained"
    Private Military Companies .. 100 v/d
    Border Security .............. 88 v/d
    Private Prisons .............. 61 v/d
    the Police ................... 48 v/d
    Insurance .................... 33 v/d
  familia fraca ............... "The Economics of Owning a X" — 27, 7, 4, 2, 1, 0

A divisao nao e o tema, e a direcao do poder: instituicao que age SOBRE o
espectador performa; negocio que ele poderia possuir, nao. O nicho do canal esta
cadastrado como "economia, dinheiro e poder" — o formato campeao e exatamente o
que o canal promete e ainda nao tinha entregue.

Eixo nao usado: pacote 1 foi lifestyle creep (morto no grupo), pacote 2 foi a
VOC (empresa historica). Este e a instituicao que precifica a vida do espectador
hoje, e na qual ele e o produto, nao o cliente.

Ancoras 2026: guidance de receita da Equifax de 6,66 a 6,78 bilhoes de dolares;
Experian com receita TTM de ~7,52 bilhoes no H1 FY2026; a FICO passando a vender
score direto a credores hipotecarios, contornando os bureaus, e a Equifax
respondendo com o VantageScore.

Numeros por extenso, sem digitos — convencao do pacote anterior, que funcionou
com a en-US-AndrewNeural (16,54 chars/s medidos, a voz mais rapida do portfolio).
"""
import json, os

VOZ = "en-US-AndrewNeural"
PALETA = {"ink": "#1A1A1A", "c1": "#E4572E", "c2": "#F2B134", "bg": "#F2ECDF"}

CAPS = []


def cap(titulo, cenas):
    CAPS.append((titulo, cenas))


# ============================ 1 ============================
cap("You are not the customer", [
 ("titulo", "Not a customer", "a product", "There is a company that holds a file on you. You never signed up for it, you cannot delete it, and you are not its customer. You are its inventory."),
 ("titulo", "Three companies", "one file each", "Three of them, actually. Equifax, Experian and TransUnion. Between them they hold a file on nearly every adult in the country."),
 ("item", "The file decides", "far more than loans", "That file decides whether you get an apartment, what you pay for insurance in many states, and in some cases whether you get the job at all."),
 ("item", "And yet", "you are not the buyer", "And yet nobody in that transaction is buying anything from you. The lender is the customer. The landlord is the customer. You are the thing being sold."),
 ("barras", "Revenue, billions", ["Experian", "Equifax"], [100, 89], "Experian reported trailing revenue of about seven point five two billion dollars in its first half of fiscal twenty twenty-six. Equifax guided to between six point six six and six point seven eight billion for the year."),
 ("item", "That is the size", "of a data business", "Together with TransUnion, that is well over fifteen billion dollars a year, built almost entirely on information that people hand over without ever deciding to."),
 ("titulo", "This video", "follows the money", "This video follows that money. Not how to raise your score — there are ten thousand videos on that. How the business underneath it actually works."),
 ("lista", "What we cover", ["What the file holds", "Who buys it", "Why the score is a separate business", "What it costs you"], "Four parts: what is actually in the file, who buys it and why, why the score itself is a completely separate business, and what all of it costs you in real money."),
 ("item", "One thing first", "this is not a scam story", "One thing up front. This is not a story about a scam. Everything here is legal, disclosed, and regulated. That is exactly what makes it worth understanding."),
 ("item", "The system works", "just not for you", "The system works. It is efficient, it prices risk well, and it lets strangers lend to strangers. It simply was not designed with you as the beneficiary."),
 ("titulo", "Start here", "what is in the file", "So let us start with the thing itself. What is actually written in your file?"),
])

# ============================ 2 ============================
cap("What the file actually holds", [
 ("lista", "Four categories", ["Who you are", "What you owe", "How you pay", "Who has looked"], "Four categories. Identifying information, the accounts you hold, your payment behaviour on each, and a log of everyone who has requested the file."),
 ("item", "Identity", "thinner than you think", "The identity section is thinner than people expect. Name, current and former addresses, date of birth, and in most cases a social security number."),
 ("item", "Accounts", "the bulk of the file", "The accounts section is the bulk of it. Every credit card, loan, mortgage and line of credit, with its limit, balance and age."),
 ("titulo", "Payment history", "month by month", "Payment history is recorded month by month, for years. Not a summary — a grid, with a mark for every billing cycle you have ever had."),
 ("item", "Why the grid", "patterns price better", "The grid matters because lenders are not really pricing whether you paid. They are pricing the pattern. A single miss four years ago reads very differently from three misses last spring."),
 ("item", "The inquiry log", "who asked about you", "The last section is the inquiry log: every company that pulled your file, and when. It is the part almost nobody reads, and it quietly reveals a lot about the business."),
 ("titulo", "What is not there", "and this surprises people", "Now the part that surprises people. Several things you would expect to be in the file simply are not."),
 ("lista", "Not in the file", ["Your income", "Your savings", "Your job title", "Your assets"], "Your income is not in there. Neither are your savings, your job title, or anything you own outright. The file describes your debt, not your wealth."),
 ("item", "So a person", "with no debt looks blank", "Which produces an odd result. A person who has never borrowed, who pays cash and owns their home, can look almost invisible to the system."),
 ("item", "That is not a bug", "it is the design", "That is not a flaw in the data. It is the design. The file exists to describe how you handle borrowed money, and nothing else."),
 ("titulo", "Which raises", "who is asking", "Which brings us to the question that actually explains the revenue. Who is asking to see it?"),
])

# ============================ 3 ============================
cap("Who buys the file", [
 ("titulo", "Lenders", "the obvious buyer", "The obvious buyer is the lender. A bank deciding on a card or a mortgage pulls the file, and pays for it. That is the business everyone assumes."),
 ("item", "But lending", "is not the whole story", "But lending is nowhere near the whole story, and the other buyers are where the interesting money is."),
 ("lista", "Also buying", ["Landlords", "Insurers", "Employers", "Utilities", "Debt collectors"], "Landlords screening tenants. Insurers in many states. Employers running background checks. Utility companies. And debt collectors deciding who is worth pursuing."),
 ("item", "Insurance", "the one people miss", "The insurance one catches people off guard. In many states an insurer may use a credit-based score to help set your premium, on the argument that it predicts claims."),
 ("item", "So a thin file", "can cost you twice", "Which means a thin or damaged file can raise what you pay for car insurance, in a transaction that has nothing to do with borrowing at all."),
 ("titulo", "Prescreening", "sold in bulk", "Then there is the part that explains the mailbox. Bureaus sell lists, in bulk, before anyone has applied for anything."),
 ("item", "How it works", "criteria, then names", "A card issuer describes the customer it wants — a score band, an age range, a region. The bureau returns a list of people who match, and the issuer mails them."),
 ("item", "That is why", "the offers find you", "That is why offers arrive addressed to you for products you never looked at. You were not targeted by accident. You were selected, and someone paid for the selection."),
 ("item", "You can opt out", "and almost nobody does", "You can opt out of that specific use. The mechanism exists, it is free, and almost nobody uses it, because almost nobody knows the list exists."),
 ("titulo", "And finally", "they sell to you", "And there is one more buyer, the one that closes the loop. They sell it back to you."),
 ("item", "Monitoring", "the consumer product", "Credit monitoring, score tracking, identity alerts — subscription products, sold to the person the file is about, describing the file they already own."),
 ("item", "Legally", "you are entitled to it", "You are legally entitled to your reports for free. The paid product sells convenience and alerts on top of information you can already get."),
])

# ============================ 4 ============================
cap("The score is a different business", [
 ("titulo", "Two businesses", "not one", "Here is where most explanations go wrong. The file and the score are two different products, made by two different kinds of company."),
 ("item", "The bureau", "holds the data", "The bureau holds the data. That is one business: collect, store, verify, sell access."),
 ("item", "The model", "turns data into a number", "The score is a model that turns that data into a number. Building that model is a separate business, with a separate owner, taking a separate cut."),
 ("titulo", "FICO", "licenses the formula", "The best known of those models comes from Fair Isaac. The bureaus license the formula, run your data through it, and resell the result along with the file."),
 ("item", "So one pull", "pays two companies", "Which means a single credit pull often pays two companies. One for the data, one for the number calculated from it."),
 ("item", "And that", "is a fragile arrangement", "That arrangement works right up until one side decides it would rather have the whole margin."),
 ("titulo", "Twenty twenty-six", "the arrangement cracked", "Which is roughly what happened. Fair Isaac moved to sell scores directly to mortgage lenders and resellers, going around the bureaus."),
 ("item", "The response", "push the alternative", "Equifax responded by pushing VantageScore more aggressively into mortgage — a competing model, built by the bureaus themselves."),
 ("item", "Read plainly", "a fight over the cut", "Stripped of the press releases, that is a fight over who keeps the margin on a number describing you, in which you have no seat and no vote."),
 ("item", "And note", "there is no single score", "It also explains something confusing: there is no single score. Different models, different bureaus, different versions, all producing different numbers about the same person."),
 ("titulo", "So when someone", "quotes you a number", "So when an app shows you a score, the honest question is which model, which bureau, and which version — because a lender may be looking at a different one entirely."),
])

# ============================ 5 ============================
cap("Why disputes work the way they do", [
 ("titulo", "You can dispute", "and it does work", "You have a legal right to dispute anything in the file, and disputes genuinely do get things removed. But the shape of the process tells you something."),
 ("item", "The burden", "starts with you", "The burden starts with you. You must find the error, in a file you did not compile, describing accounts opened by companies you may not remember."),
 ("item", "Then the bureau", "asks the furnisher", "The bureau then asks the company that reported the item whether it is correct. That company is the bureau's customer."),
 ("item", "Which is why", "confirmations are common", "Which is why a dispute is frequently returned as confirmed. The check is real, but it is a check with the party that supplied the information in the first place."),
 ("titulo", "Volume", "explains the rest", "Volume explains most of the rest. With files on nearly every adult, disputes arrive in enormous numbers, and the process is built to run at that scale."),
 ("item", "Automation", "is not malice", "So it is heavily automated. That is not malice; it is arithmetic. But automation is why a nuanced dispute and a simple one can come back looking the same."),
 ("item", "The practical read", "be specific", "The practical consequence is that specific, documented disputes do far better than general ones. Name the account, the date, the exact field, and attach proof."),
 ("titulo", "Medical debt", "a special case", "Medical debt has become its own category, because it behaves differently from borrowing: it arrives without a decision, often without a price known in advance."),
 ("item", "Rules have moved", "and keep moving", "The rules on how medical debt appears have moved repeatedly in recent years. If you have any on file, it is worth checking what currently applies rather than what applied last time you looked."),
 ("item", "Same for", "old negative items", "The same is true of old negative items. Most fall off after a defined period, and items that should have aged off sometimes do not, on their own."),
 ("titulo", "Now", "the cost", "Which leaves the question that actually matters to your money. What does all of this cost you?"),
])

# ============================ 6 ============================
cap("What it costs you in real money", [
 ("titulo", "A mortgage", "the biggest number", "The clearest place to see it is a mortgage, because the loan is large and it runs for decades."),
 ("barras", "Rate by score band", ["Top band", "Middle", "Lower"], [55, 75, 100], "Between the top score band and a lower one, the rate difference on the same loan is routinely more than a full percentage point."),
 ("item", "On a long loan", "that compounds", "On a thirty-year loan, a difference of one point can mean tens of thousands of dollars in additional interest, for the identical house and identical borrower."),
 ("item", "Same borrower", "different price", "Same person, same income, same job. The only variable is the file — and the file mostly measures how long you have been borrowing and how consistently you repaid."),
 ("titulo", "Then the small ones", "which add up", "Then there are the smaller charges, which are easier to ignore and land more often."),
 ("lista", "Where else it shows up", ["Car insurance premiums", "Rental deposits", "Phone and utility deposits", "Card interest rates"], "Insurance premiums in many states. Larger rental deposits. Deposits for phone and utility service. And the rate on any card you carry a balance on."),
 ("item", "Each one small", "the pattern is not", "Each one is small enough to shrug at. The pattern is not: the same file makes the same person more expensive in a dozen unrelated places at once."),
 ("titulo", "And the reverse", "compounds too", "The reverse compounds as well, which is the genuinely encouraging part of this."),
 ("item", "Improving the file", "pays in many places", "Improving the file does not just lower one rate. It lowers several prices at once, in transactions you were not thinking about when you made the change."),
 ("item", "The mechanism", "is boring on purpose", "And the mechanism is deliberately boring: pay on time, keep balances well below limits, and let accounts age. There is no clever move, because the model is mostly measuring time."),
 ("titulo", "Which is", "the honest answer", "That is the honest answer to how you improve it, and it is why the improvement videos all end up saying roughly the same thing."),
])

# ============================ 7 ============================
cap("What you can actually do", [
 ("lista", "Free and worth doing", ["Pull all three reports", "Opt out of prescreened offers", "Freeze the file", "Fix specific errors"], "Four things that cost nothing: pull all three reports, opt out of prescreened offers, freeze the file, and dispute specific errors with documentation."),
 ("item", "All three", "because they differ", "Pull all three, not one. The bureaus receive different data from different companies, and an error often exists on only one of them."),
 ("titulo", "The freeze", "the strongest tool", "The freeze is the strongest tool most people never use. It blocks new accounts from being opened against your file until you lift it."),
 ("item", "It is free", "and reversible", "It is free by law, reversible in minutes, and it does not affect your score or your existing accounts at all."),
 ("item", "The trade-off", "one extra step", "The trade-off is one extra step whenever you genuinely apply for something. For most people that is a few minutes a year against a permanent reduction in exposure."),
 ("titulo", "Opting out", "stops the list sales", "Opting out of prescreened offers stops your name being sold into those bulk marketing lists. It is one form, and it does not affect anything else."),
 ("item", "And it is", "the clearest lever", "It is also the one place in this entire system where you can directly remove yourself from a revenue stream, which makes it worth doing on principle alone."),
 ("titulo", "What not to pay for", "in most cases", "And one thing worth being blunt about: what is usually not worth paying for."),
 ("item", "Repair services", "do what you can do", "Credit repair companies mostly perform disputes you can file yourself, at no cost, using the same process and the same evidence."),
 ("item", "Nobody", "can remove accurate items", "And no service can remove an accurate item. If a claim to do so is made, that alone tells you what kind of company it is."),
 ("titulo", "Everything else", "is time", "Everything else is just time. Which is unsatisfying, and also true."),
])

# ============================ 8 ============================
cap("What this is really about", [
 ("titulo", "Step back", "the pattern", "Step back from the mechanics and there is a pattern worth naming, because it is not unique to credit."),
 ("item", "A record about you", "sold to decide about you", "A record is compiled about you without your involvement, sold to institutions that make decisions about you, and then sold back to you as a subscription."),
 ("item", "That shape", "appears everywhere", "That shape shows up in tenant screening, in employment background checks, in insurance rating. Credit is simply the oldest and most refined version of it."),
 ("titulo", "The lesson", "not outrage", "The useful reaction is not outrage. Systems like this exist because the alternative — lending only to people you personally know — was far worse and far smaller."),
 ("item", "The lesson is", "know you are in it", "The useful reaction is knowing you are inside a market you did not enter, and using the few levers that market gives you."),
 ("lista", "Three to remember", ["You are the product, not the client", "The file measures debt, not wealth", "Time does most of the work"], "Three things to carry: you are the product and not the client. The file measures debt, not wealth. And time does most of the work, in both directions."),
 ("item", "The first", "changes how you read offers", "The first one changes how you read every offer that arrives unsolicited: someone paid to put your name on that list."),
 ("item", "The second", "explains the blank file", "The second explains why paying cash for everything can leave you looking invisible, and why that is not a compliment."),
 ("cta", "Next Level Money", "money, and who holds it", "If this was useful, tell me in the comments which institution you want taken apart next. The most requested one gets made first."),
 ("cta", "Next Level Money", "money, and who holds it", "And if you have ever had something removed from your file, say what actually worked. Specifics help more people than general advice does."),
 ("cta", "Next Level Money", "money, and who holds it", "Thanks for watching to the end. See you in the next one, here on Next Level Money."),
])


# ===================== montagem =====================
def cena(t, primeira, titulo_cap):
    lay, kicker = t[0], t[1]
    c = {"layout": lay, "kicker": kicker}
    if lay == "barras":
        c["itens"], c["alturas"], nar = t[2], t[3], t[4]
    elif lay == "lista":
        c["itens"], nar = t[2], t[3]
    elif lay == "item":
        c["preco"], nar = t[2], t[3]
    else:
        c["sub"], nar = t[2], t[3]
    c["nar"] = nar
    if primeira:
        c["cap"] = titulo_cap
    else:
        c["sem_cap"] = True
    return c


longo = []
for titulo_cap, cenas in CAPS:
    for i, t in enumerate(cenas):
        longo.append(cena(t, i == 0, titulo_cap))

short = [
 cena(("titulo", "Not a client", "the product", "Three companies hold a file on you. You never signed up, you cannot delete it, and you are not their customer."), False, ""),
 cena(("item", "The file", "measures debt, not wealth", "Your income is not in it. Neither are your savings. It describes how you handle borrowed money, and nothing else."), False, ""),
 cena(("titulo", "Two products", "data and score", "And the score is a separate business. One pull often pays two companies: one for the data, one for the number."), False, ""),
 cena(("item", "Free lever", "freeze and opt out", "Freezing the file and opting out of prescreened offers are both free, and almost nobody does either."), False, ""),
 cena(("cta", "Next Level Money", "the full breakdown", "The full economics, and what it actually costs you, are in the long video."), False, ""),
]
for c in short:
    c.pop("sem_cap", None)

spec = {
    "slug": "next-level-money",
    "pacote": "next-level-money-003",
    "voz": VOZ,
    "paleta": PALETA,
    "thumb": {"l1": "YOU ARE THE PRODUCT", "l2": "credit, explained"},
    "longo": longo,
    "short": short,
    "copy": "gerado a partir dos capitulos reais apos o render",
}

if __name__ == "__main__":
    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "next-level-money-003.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False)
    nl = sum(len(c["nar"]) for c in longo)
    ns = sum(len(c["nar"]) for c in short)
    print(f"cenas longo ....... {len(longo)}")
    print(f"capitulos ......... {len(CAPS)}")
    print(f"chars narracao .... {nl}")
    for taxa in (15.0, 16.54, 17.5):
        s = nl / taxa + len(longo) * 0.5
        print(f"  a {taxa} chars/s .. {s:.0f}s = {s/60:.1f} min")
    print(f"short ............. {len(short)} cenas, {ns} chars, "
          f"~{ns/16.54 + len(short)*0.5:.0f}s")
    print(f"bytes ............. {os.path.getsize(destino)}")
