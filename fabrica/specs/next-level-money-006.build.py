#!/usr/bin/env python3
"""Monta a spec next-level-money-006.

POR QUE ESTE CANAL

Primeiro da fila que PRODUZ. O topo da fila e `cocina-por-niveles`, com ultimo
pacote em 05/08 — mas `pode_produzir` = false e `token_vivo` = false, porque o
canal nao existe no YouTube. Ele nao pode ser o pacote deste disparo, e ja esta
na lista de acoes do Pablo. O proximo produzivel e este.

O VEREDITO, e o que ele manda fazer

v_maquina_licoes, medido em 20/08: `canal frio`. Oito shorts com mediana de
1,42 views/dia e topo de 2,39; oito longos com mediana ZERO. Oitenta e cinco
views no acervo inteiro.

`canal frio` nao significa trocar de formato. Significa que o problema esta no
gancho ou no eixo — entao o que ja foi ao ar aqui foi medido e nao pegou, e
repetir o angulo seria repetir a medicao.

O ACERVO, lido pelos titulos publicados (dado primario, nao `usado_em`)

Nove linhas de longo com youtube_id, e apenas QUATRO titulos distintos:

  - Dutch East India Company, $7.9 Trillion Myth ....... SEIS linhas
  - Credit Bureaus: You Are the Product ................ uma
  - Credit Card Debt Hit $1.26 Trillion ................ uma
  - Delinquency Hit 12.8% ............................. uma

As seis linhas iguais sao o pacote `nlm-voc` mais cinco `cron` que
republicaram o mesmo video. Isso e parte dos duplicados que estao pendentes de
decisao do Pablo, e esta anotado aqui porque distorce qualquer contagem feita
por linha em vez de por titulo.

Eixos ja gastos: economia historica, bureaus de credito, divida de cartao,
inadimplencia. Tres dos quatro sao a MESMA familia — credito ao consumidor
americano. O canal esta girando em torno de si mesmo.

O EIXO ESCOLHIDO, e por que ele estava livre

`pautas_banco` tem quarenta e sete pautas neste canal e ZERO marcadas como
usadas — o que e falso, porque os pacotes 004 e 005 consumiram `divida de
cartao / recorde`. `usado_em` esta subpreenchido aqui como ja esteve em outros
quatro canais. Por isso a decisao saiu dos titulos publicados.

Por views/dia, os eixos do banco sao:

  - divida de cartao / recorde ...... dez outliers, topo 27.490 v/d — GASTO
  - custo de vida / groceries ....... treze pautas, topo 2.987 v/d — livre
  - buy now pay later ............... tres pautas proprias, topo 219 v/d — livre
  - educacao financeira macro ....... uma pauta, 249.967 v/d — CONTAMINADA

A de 249.967 v/d ("How Money Actually Works") e o mesmo padrao de contaminacao
ja registrado em tres canais: um titulo generico de canal gigante que nao
pertence ao eixo medido. Nao serve de referencia de formato.

A interseccao dos dois eixos livres e uma pauta so, a de numero 503: "39% of
Families Are FINANCING GROCERIES", 312,6 v/d. Buy now pay later aplicado a
supermercado. Esse e o eixo deste pacote.

A DOR DATADA, com duas fontes institucionais que batem

  Board of Governors of the Federal Reserve System, Survey of Household
  Economics and Decisionmaking (SHED), edicao 2025, publicada em 13 de maio de
  2026. Campo de 17 a 28 de outubro de 2025, cerca de treze mil respondentes,
  amostra nacionalmente representativa.

  - uso de BNPL subiu UM ponto percentual, para DEZESSEIS POR CENTO dos adultos
  - ONZE POR CENTO dos usuarios de BNPL tiveram um pagamento disparar taxa de
    overdraft ou de fundos insuficientes no banco, nos doze meses anteriores

  Federal Reserve Bank of Richmond, Economic Brief 26-05, "Buy Now, Pay Later:
  Recent Developments and Implications", fevereiro de 2026.

  - taxa cobrada do LOJISTA pelo BNPL: CINCO A OITO POR CENTO
  - taxa cobrada do lojista pelo cartao de credito: DOIS A TRES POR CENTO
    (a faixa vem de Di Maggio, Katz e Williams, 2022, citada no brief)
  - volume BNPL em 2025: cerca de SETENTA BILHOES de dolares, ou UM VIRGULA UM
    POR CENTO do gasto total em cartao de credito

Duas instituicoes distintas do mesmo sistema, medindo coisas diferentes, sem
se contradizer. Os numeros do Board sao de pesquisa domiciliar; os do Richmond
sao de mercado. Eles se encaixam em vez de se repetir.

O MECANISMO — e o giro do video

O consumidor le "zero por cento". O zero e verdadeiro para ele e falso para a
transacao. O custo nao evapora, ele muda de bolso tres vezes:

  1. do juro do consumidor para a taxa do lojista, que e de duas a tres vezes
     a do cartao;
  2. da taxa do lojista para o preco de prateleira, porque nenhuma loja mantem
     duas etiquetas — quem paga a vista paga a mesma etiqueta;
  3. do preco para a taxa bancaria de quem escorregou na parcela — onze por
     cento dos usuarios.

E o achado que amarra tudo: DEZESSEIS POR CENTO dos adultos movimentando UM
VIRGULA UM POR CENTO do gasto em cartao. Penetracao alta, volume baixo. Isso
nao descreve gente comprando caro. Descreve gente sem folga no mes.

O QUE ESTE VIDEO NAO FAZ

  - nao diz que BNPL e fraude nem que e ilegal: e um produto legal, e para
    parte dos usuarios o parcelamento sem juros e melhor que o rotativo;
  - nao afirma que o repasse ao preco e integral nem mensurado — a literatura
    citada estima a taxa do lojista, nao o repasse; o video diz explicitamente
    que essa parte e inferencia economica, nao medicao;
  - nao usa o numero do LendingTree (vinte e nove por cento usaram para
    mercado) como se fosse institucional. Ele aparece uma vez, nomeado como
    pesquisa privada, e nada no argumento depende dele;
  - nao faz previsao e nao e conselho financeiro.

TAXA DA VOZ. en-US-AndrewNeural, MODELO_VOZ atual: R = 17,12 chars/s,
P = 0,272 s/frase, n = 157 amostras medidas contra os legendas.srt dos pacotes
reais — nao sintetica (aprendizado critico). Vies medido no longo: +3,8%.

ORCAMENTO — e o erro que ele cometeu na primeira passada

Orcei 79 cenas assumindo a densidade historica do canal, 2,67 frases/cena, e
cheguei a 154 caracteres por cena. A medicao do arquivo pronto deu outra coisa:
2,04 frases/cena e 138 caracteres. Minhas frases sairam mais longas e em menor
numero, entao o orcamento de caracteres sobrou e o previsto caiu para 704 s —
11:43, dentro da faixa mas raspando o piso de 12 minutos.

A correcao NAO foi engordar as cenas existentes com enchimento. Foram seis
cenas novas, uma por capitulo, cada uma com um fato que faltava: o formato do
produto (quatro parcelas em seis semanas), por que a taxa do lojista e maior
(aprovacao em segundos e risco de credito), por que a loja nao consegue
recusar (a loja vizinha aceita), que a taxa de overdraft varia por banco, o
recorte de genero do SHED, e a regra de overdraft derrubada no Congresso.

Resultado medido: 85 cenas, 776,9 s previstos, ~806 s reais (13:26) com o vies
de +3,8% do Andrew. Meio da faixa de 12-15 min.

LICAO REGISTRADA: densidade historica do canal e um chute, nao um orcamento.
Medir o arquivo pronto e a unica conta que vale, e ela custa uma linha.

CAPITULOS. Sete, de doze a treze cenas. A ~9,1 s por cena, cada capitulo mede
~110 s: com folga dentro de MIN_CAP 60 e MAX_CAP 150, sem risco de capitulo
silenciosamente descartado (isso ja aconteceu duas vezes). Capitulo abre
sempre em layout `titulo` (aprendizado 388).

CORRECAO DE FATO durante a escrita: uma cena dizia "the same thirty five
dollar overdraft". Fui conferir antes de fechar e o numero nao vale mais como
padrao — a regra do CFPB que limitava a taxa foi finalizada em 2024 e
DERRUBADA no Congresso em 2025 sem nunca entrar em vigor, e os bancos grandes
reagiram cortando para poucos dolares ou zerando, enquanto bancos menores e
cooperativas seguem com valores legados. A cena foi reescrita sem cifra fixa, e
o fato virou uma cena propria no capitulo 6 — porque "quanto custa depende de
qual banco voce usa" e um argumento melhor do que qualquer numero unico.
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


# ------------------------------------------- 1. Two numbers that do not fit
T("Sixteen per cent", "of American adults",
  "Sixteen per cent of American adults used a buy now, pay later loan in the "
  "past year. That is the Federal Reserve's own household survey, published "
  "in May. One adult in six.",
  cap="Two numbers that do not fit")
T("Now the second number", "from a different Fed",
  "Here is a second number, from a different part of the same system. The "
  "Richmond Fed puts the entire buy now, pay later market at about seventy "
  "billion dollars a year.")
I("Seventy billion", "sounds enormous",
  "Seventy billion dollars sounds enormous, and on its own it is. But the "
  "brief puts it next to something, and next to that something it is small.")
I("As a share of card spending", "one point one per cent",
  "Measured against total credit card spending, the whole buy now, pay later "
  "market is one point one per cent. Barely one dollar in every hundred that "
  "moves through a card.")
T("So hold both", "at the same time",
  "So hold both of those at once. One adult in six is using this product. And "
  "the product moves almost no money.")
T("Those do not", "usually go together",
  "Those two things do not usually go together. Products with that much reach "
  "normally carry serious volume behind them.")
L("What that gap means", ["Small purchases",
                          "Repeated often",
                          "By people with no slack"],
  "A gap like that has only one shape. Small amounts, bought often, by people "
  "who need the amount split.")
T("Which is the first clue", "about what this is for",
  "Which is already the first clue about what this product is actually for, "
  "and it is not what the advertising suggests.")
I("The advertising says", "zero per cent",
  "The advertising says zero per cent interest. Four payments, no fee, nothing "
  "added. And for the shopper standing at the checkout, that is true.")
I("The standard shape", "four payments, six weeks",
  "The standard product is four payments across about six weeks. A quarter at "
  "the till, then three more every fortnight, taken automatically. No interest "
  "quoted anywhere in it.")
T("The word doing the work", "is 'for the shopper'",
  "The words doing all the work in that sentence are 'for the shopper'. Zero "
  "for the shopper is not the same as zero for the transaction.")
I("This video", "follows the cost",
  "So this video does one thing. It follows the cost. If the shopper is not "
  "paying it, someone is, and it is worth knowing who.")

# ------------------------------------------------ 2. Who pays the provider
T("The provider", "still gets paid", "Start with the obvious question. The "
  "company lending you the money is a business. It has funding costs, credit "
  "losses and staff. Somebody pays for that.",
  cap="Who pays the provider")
T("Not the borrower", "in the standard product",
  "In the standard four payment product, it is not the borrower. There is no "
  "interest charge in the advertised deal, and that part is genuine.")
I("It is the merchant", "who pays the fee",
  "It is the merchant. The shop that sold you the thing pays a fee to the "
  "provider on every buy now, pay later sale, and keeps the rest.")
T("That is not exotic", "cards work that way too",
  "That arrangement is not exotic. Card networks work the same way. The shop "
  "pays a slice of every card sale and has done for decades.")
I("The card fee", "two to three per cent",
  "For credit cards, that slice usually lands between two and three per cent "
  "of the sale. It is a known, budgeted cost of accepting cards.")
T("Why the gap exists", "speed and risk",
  "That gap exists for a reason worth stating plainly. The provider approves "
  "in seconds, on a light check, and eats the loss if you never pay. Someone "
  "is quoted a price for that risk, and it is the shop.")
B("Merchant fee", ["Card", "Buy now pay later"], [30, 80],
  "For buy now, pay later, the Richmond Fed brief puts it at five to eight per "
  "cent. That is the whole story in one comparison.")
T("Read that again", "it is two to three times",
  "Read that again, because it is the hinge of everything that follows. The "
  "merchant fee on this product runs at roughly two to three times the card "
  "fee.")
I("On a hundred dollar basket", "five to eight dollars",
  "On a shopping basket of one hundred dollars, that is five to eight dollars "
  "leaving the shop, against two to three on a card.")
T("The shop agreed to it", "which is worth explaining",
  "And the shop agreed to this. Nobody forced it. Which raises the obvious "
  "question of why a retailer would volunteer to pay double.")
L("The pitch to retailers", ["Bigger baskets",
                             "Fewer abandoned carts",
                             "Younger customers"],
  "The pitch is straightforward. Shoppers offered instalments buy more, "
  "abandon fewer carts, and skew younger. The provider sells conversion.")
I("So the fee", "is bought deliberately",
  "So the fee is not a trap sprung on the retailer. It is a cost bought "
  "deliberately, in exchange for selling more. Which matters for what happens "
  "next.")

# ------------------------------------------ 3. Where the merchant fee lands
T("Now the harder question", "where does the fee go",
  "Here is the harder question, and the one almost nobody asks. The shop is "
  "paying five to eight per cent. Where does that money come from?",
  cap="Where the merchant fee lands")
T("Only two places", "and they are not equal",
  "There are only two places it can come from. The shop's margin, or the "
  "shop's prices. Those are not the same thing at all.")
I("If it comes from margin", "the shop absorbs it",
  "If it comes out of margin, the shop absorbs it and the customer never sees "
  "it. Profit falls, prices hold, and the cost stops there.")
I("If it comes from prices", "everyone pays it",
  "If it comes out of prices, the picture changes completely, because a shop "
  "does not print two price tags.")
T("There is one shelf price", "for everybody",
  "There is one price on the shelf. The person paying cash sees the same "
  "number as the person splitting it into four.")
T("So a price rise", "cannot be targeted",
  "So if the price moves to cover that fee, it moves for everyone. It cannot "
  "be aimed only at the customers who caused it.")
T("And refusing it", "is not simple either",
  "A shop could of course refuse the whole arrangement. But if the shop across "
  "the street offers instalments and this one does not, some shoppers simply "
  "walk. That is what makes the fee hard to decline.")
L("Who ends up paying", ["The instalment buyer",
                         "The card buyer",
                         "The cash buyer"],
  "Which means the instalment buyer, the card buyer and the cash buyer all pay "
  "the same covering amount, and only one of them used the service.")
T("I have to be careful", "right here",
  "Now I have to be careful, because this is exactly the point where an "
  "argument like this usually overreaches.")
I("What is measured", "is the fee",
  "What the research measures is the fee the merchant pays. Five to eight per "
  "cent. That number is sourced and I will put the brief in the description.")
I("What is not measured", "is the pass through",
  "What is not measured, in anything I could find, is how much of that fee "
  "reaches the shelf price. That share is economic inference, not a figure I "
  "can hand you.")
T("So take it as", "direction, not size",
  "So take this chapter as a direction, not a size. The cost moves toward "
  "prices. How far it travels, nobody has cleanly measured.")

# ------------------------------------------------- 4. The bill at your bank
T("Now the part", "that is measured",
  "Which brings us to the part that is measured, precisely, by the Federal "
  "Reserve, and that almost never appears in coverage of this product.",
  cap="The bill at your bank")
T("The instalments", "come out automatically",
  "The four payments are collected automatically, from a debit card or a bank "
  "account, on a schedule the shopper agreed to at checkout.")
T("Automatic is the feature", "and the risk",
  "Automatic collection is the feature. It is also the risk, because the "
  "payment arrives whether or not the money is there that day.")
I("Eleven per cent of users", "hit an overdraft",
  "In the Fed's survey, eleven per cent of buy now, pay later users had one of "
  "these payments trigger an overdraft or an insufficient funds fee at their "
  "own bank.")
T("Read what that is", "carefully",
  "Look carefully at what that is. The provider charged no interest. It kept "
  "its promise exactly. And the customer paid a fee anyway.")
I("The fee just moved", "to a different company",
  "The fee simply moved to a different company. It is charged by the bank, "
  "not the lender, so it never appears in any comparison of the product.")
T("And the size of it", "depends on your bank",
  "How much that fee costs is not even fixed. Several large banks now charge a "
  "few dollars, or nothing. Smaller banks and credit unions can still charge "
  "legacy amounts many times higher.")
T("One user in nine", "is not a rounding error",
  "Roughly one user in nine. That is not a rare accident at the edge of the "
  "product. It is a regular outcome of how the product collects.")
T("And it lands", "unevenly",
  "And it does not land evenly. An overdraft fee is only possible if the "
  "account was near empty, so it falls hardest on exactly the people who "
  "chose instalments because money was tight.")
L("The full picture", ["No interest to the lender",
                       "A fee to the bank",
                       "A higher shelf price for all"],
  "Put the three together and the zero per cent product has produced a bank "
  "fee for some customers and, plausibly, a higher shelf price for everyone.")
I("None of that", "is fraud",
  "And none of that is fraud, or a hidden clause, or a scandal. Every part of "
  "it is disclosed somewhere. It is just spread across three companies, so no "
  "single statement shows it.")
T("Which is why", "the number stayed hidden",
  "Which is precisely why it took a Federal Reserve household survey to find "
  "it. No lender was ever going to report it, because no lender charged it.")

# --------------------------------------- 5. High reach, low volume, and why
T("Back to the puzzle", "from the opening",
  "Now we can go back to the puzzle from the opening, because it stopped being "
  "a puzzle somewhere in the last few minutes.",
  cap="High reach and low volume")
I("Sixteen per cent of adults", "one point one per cent of card spending",
  "Sixteen per cent of adults use it. It carries one point one per cent of "
  "card spending. Those numbers only fit if the individual purchases are "
  "small.")
T("Small and repeated", "is the shape",
  "Small, and repeated. Not one large purchase split for convenience, but many "
  "modest ones split because the timing of the money is wrong.")
I("A private survey", "points the same way",
  "A private survey by LendingTree, and I flag it as private rather than "
  "official, found twenty nine per cent of users had used instalments to buy "
  "groceries.")
T("Nothing here rests", "on that figure",
  "Nothing in this argument rests on that figure, and I am not going to lean "
  "on it. But it points the same direction the Fed's own numbers already "
  "pointed.")
T("Groceries are the test", "of what a product is for",
  "Groceries are a useful test, because nobody finances food for convenience. "
  "You finance food when the money arrives after the hunger does.")
T("That reframes it", "completely",
  "That reframes the product completely. It is not primarily a way to afford "
  "something bigger. It is a way to move a small amount a few weeks earlier.")
L("Which explains", ["The reach",
                     "The tiny volume",
                     "The overdrafts"],
  "Which explains all three findings at once. Wide reach, tiny volume, and a "
  "bank fee for one user in nine.")
I("The Fed noted", "who uses it",
  "The Fed's survey noted the same thing from the other side. Use is higher "
  "among younger adults, adults without a degree, and people with fewer "
  "financial resources.")
I("Nearly one in five women", "used it last year",
  "Nearly one woman in five used the product in the year measured. Women have "
  "come out higher than men in every edition of this survey that has asked the "
  "question.")
T("That is not a moral claim", "it is a description",
  "That is not a judgement about anyone. It is a description of who a cash "
  "flow product finds, and it is exactly who you would expect it to find.")
T("And it is why", "the fee matters more here",
  "It is also why the fee matters more here than it would elsewhere. A bank "
  "fee is a much larger share of a small budget than of a large one.")
I("Same fee", "different weight",
  "The same flat charge is a rounding error on one income and a genuine "
  "problem on another. The fee does not scale with the account. The pain "
  "does.")

# ------------------------------------------------ 6. What this cannot tell
T("Now the limits", "of everything I just said",
  "Before the useful part, the limits. This is a channel about money, and a "
  "confident story with soft foundations is worse than no story.",
  cap="What this cannot tell you")
I("The Fed survey", "is self reported",
  "The household survey is self reported. People are answering questions about "
  "their own borrowing from memory, and memory about debt runs optimistic.")
T("It is also a snapshot", "of last October",
  "It was also fielded across two weeks of October last year. It describes "
  "that moment, not this one, and the product is moving fast.")
I("The merchant fee range", "is an estimate",
  "The five to eight per cent range is a research estimate, from work cited in "
  "the Richmond brief. It is not a published rate card, and real terms vary by "
  "retailer and by size.")
T("The pass through", "I have already flagged",
  "The step from merchant fee to shelf price I already flagged, and I will "
  "flag it again, because it is the weakest link in the chain.")
I("What is missing entirely", "is a credit picture",
  "And something is missing entirely. Most of this lending still does not "
  "appear in ordinary credit reporting, so nobody can see how many loans one "
  "person holds at once.")
T("That gap has a name", "stacking",
  "That gap has a name. Loan stacking. Four providers, four sets of "
  "instalments, and no single record showing all of them together.")
T("And the other fee", "is not settled in law",
  "The overdraft side is not settled either. A rule capping those fees at large "
  "banks was finalised, then overturned in Congress before it ever took effect. "
  "Which is why the amount depends on your bank and not on the law.")
T("Which means", "nobody knows the total",
  "Which means no institution, including the ones I have quoted all video, can "
  "tell you the true total exposure of an individual household to this "
  "product.")
L("So what is solid", ["Sixteen per cent of adults",
                       "Eleven per cent overdrafted",
                       "Five to eight per cent merchant fee"],
  "So keep the three solid numbers. Sixteen per cent reach, eleven per cent "
  "hitting a bank fee, and a merchant fee of five to eight per cent.")
I("And what is inference", "the shelf price",
  "And hold the shelf price argument as inference. Strong inference, in my "
  "view, but not the same kind of thing as the other three.")
T("Keeping those apart", "is most of the skill",
  "Keeping those two categories apart is most of the skill in reading "
  "financial data, and it is the part that almost never survives a headline.")

# ------------------------------------------------------ 7. What to do with it
T("So what do you do", "with all of this",
  "So what do you actually do with this, whether you use these loans or never "
  "touch them.",
  cap="What to do with it")
T("If you use it", "one thing matters most",
  "If you use instalments, one thing matters more than every comparison of "
  "providers, and it is not the interest rate, because there is not one.")
I("It is the date", "the payment lands",
  "It is the date each payment lands, set against the date your money arrives. "
  "That gap is the entire risk of the product.")
T("Because the failure", "is timing, not affordability",
  "The eleven per cent figure is not a story about people who could not afford "
  "the purchase. It is about people whose payment landed on the wrong day.")
L("Two minutes, before you split", ["Write the four dates down",
                                    "Check each against payday",
                                    "Count what is already scheduled"],
  "Which makes the fix boring and effective. Write the four dates down, check "
  "each against payday, and count what is already scheduled to come out.")
I("That third one", "is the stacking check",
  "The third one is your own stacking check, and you are the only person who "
  "can run it, because no credit file collects it for you.")
T("If you never use it", "you are still in the story",
  "And if you never touch these loans, you are still in the story, because of "
  "the shelf price. You just cannot see your part of it.")
T("That is not a reason", "to be angry at anyone",
  "That is not a reason to be angry at the shopper who splits a grocery bill. "
  "It is a reason to be precise about what the word free is doing.")
I("Free at the till", "is not free in the system",
  "Free at the till is a real fact about the till. It is not a fact about the "
  "system, and those two get quietly merged in almost every advert you will "
  "see for this.")
T("The Fed did not", "merge them",
  "The Federal Reserve did not merge them. It asked the boring question about "
  "overdrafts, and that is why we have a number at all.")
T("Next time", "we follow the merchant",
  "Next time on this channel we take the other end of this: what happens to a "
  "small retailer that accepts a fee of five to eight per cent because the "
  "shop next door already does.")
C("If this was useful", "subscribe for the next one",
  "If following the money through three companies was useful, subscribe, and "
  "tell me in the comments which of the three numbers surprised you most.")


# Budget measured for 36,5 s with 6 scenes at 2,20 sentences each: 530 chars.
SHORT = [
    {"layout": "titulo", "kicker": "Zero per cent", "sub": "for who exactly",
     "nar": "Buy now, pay later charges you zero per cent interest. That part "
            "is true. It is also not the whole sentence.", "sem_cap": True},
    {"layout": "titulo", "kicker": "The shop pays", "sub": "five to eight per cent",
     "nar": "The shop pays the provider five to eight per cent. On a card it "
            "would pay two to three.", "sem_cap": True},
    {"layout": "titulo", "kicker": "One shelf price", "sub": "for everybody",
     "nar": "And a shop only prints one price. So the cash customer covers part "
            "of it too.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Then the Fed", "sub": "asked about banks",
     "nar": "Then the Federal Reserve asked users about their own bank "
            "accounts.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Eleven per cent", "sub": "hit an overdraft",
     "nar": "Eleven per cent had an instalment trigger an overdraft fee. Zero "
            "interest, and a fee anyway.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Where the rest", "sub": "of it goes",
     "nar": "Where the rest of that money goes is on the channel.",
     "sem_cap": True},
]

THUMB = {"l1": "0% interest?", "l2": "someone pays it"}

COPY = """# Zero per cent for the shopper is not zero for the transaction

## TITULO
Buy Now Pay Later Reached 16% of Adults: Who Actually Pays for Zero Interest

## DESCRICAO
In May 2026 the Federal Reserve published its Survey of Household Economics and Decisionmaking for 2025. Buy now, pay later use rose one percentage point to 16% of all American adults — roughly one adult in six. In February 2026 the Federal Reserve Bank of Richmond published an economic brief putting the entire buy now, pay later market at around $70 billion a year, or about 1.1% of total credit card spending.

Those two figures look like they contradict each other. One in six adults, and barely one dollar in a hundred. They only fit if the individual purchases are small and repeated — which turns out to be the most important fact about this product.

This video follows the cost. The advertised zero per cent is genuine for the shopper: in the standard four-payment product there is no interest charge. But the provider still gets paid, and it is paid by the merchant. The Richmond brief puts that merchant fee at 5–8% of the sale, against 2–3% for a credit card — roughly two to three times as much.

A shop does not print two price tags. Whatever share of that fee reaches the shelf price is paid by every customer, including the ones paying cash. That step is economic inference rather than a measured figure, and the video says so explicitly rather than quietly borrowing the authority of the sourced numbers.

The measured part comes from the Fed's survey: 11% of buy now, pay later users had a payment trigger an overdraft or non-sufficient funds fee at their own bank in the prior year. The lender charged no interest and kept its promise exactly; the fee simply appeared at a different company, which is why it shows up in no product comparison anywhere.

The video also states what the data cannot tell you. The survey is self-reported and was fielded over two weeks in October 2025. The 5–8% range is a research estimate, not a published rate card. And most of this lending still does not appear in ordinary credit reporting, so no institution can see how many instalment loans a single household is carrying at once.

Ends with a two-minute routine to run before splitting any payment, and an explicit separation of what is measured from what is inferred.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
The honest gap in this one: I could not find any study measuring how much of the 5–8% merchant fee actually reaches shelf prices, as opposed to being absorbed in margin. If you work in retail pricing and have seen this modelled either way, I would genuinely like to know — it is the one link in the chain I had to argue rather than source.

## HASHTAGS
#BuyNowPayLater #FederalReserve #NextLevelMoney

## TAGS
buy now pay later, bnpl, federal reserve, shed survey, merchant fees, overdraft fees, consumer credit, personal finance, us economy, klarna, afterpay, retail pricing, interchange fees, financial literacy, household debt

## CONFIGURACAO DE STUDIO
- Language: English (en-US) | Category: Education (27)
- Not made for kids
- Altered or synthetic content disclosure: YES (AI-generated voice)
- Location: United States | Licence: Standard YouTube Licence
- Mid-roll ads: on (runtime over eight minutes)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
Two institutional sources, measuring different things, accessed 24 August 2026. (1) Board of Governors of the Federal Reserve System, Report on the Economic Well-Being of U.S. Households in 2025, published 13 May 2026, from the Survey of Household Economics and Decisionmaking: buy now, pay later use rose one percentage point to 16% of adults; 11% of BNPL users had a payment trigger an overdraft or NSF fee from their bank in the prior year. The survey was fielded 17–28 October 2025 with a nationally representative sample of nearly 13,000 respondents, and is self-reported. (2) Federal Reserve Bank of Richmond, Economic Brief 26-05, "Buy Now, Pay Later: Recent Developments and Implications", February 2026: merchant fees of 5–8% for BNPL against 2–3% for credit cards, a range the brief attributes to Di Maggio, Katz and Williams (2022); BNPL transaction value of roughly $70 billion in 2025, about 1.1% of total credit card spending. The 29% grocery figure is from a LendingTree survey conducted by QuestionPro and is identified in the video as private research, not official statistics; no part of the argument depends on it. The claim that merchant fees reach shelf prices is stated in the video as economic inference and not as a measured result. This video makes no forecast, describes no individual household, and is not financial advice.
"""

SPEC = {
    "slug": "next-level-money",
    "pacote": "next-level-money-006",
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
                           "next-level-money-006.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
