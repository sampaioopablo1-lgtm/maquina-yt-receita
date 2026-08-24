#!/usr/bin/env python3
"""Monta a spec kolejny-poziom-010.

POR QUE ESTE CANAL, E POR QUE PULEI O ANTERIOR DA FILA

A fila entregou, nesta ordem: cocina-por-niveles (nao existe no YouTube),
sx-educacao (token morto) e kolejny-poziom.

Pulei o sx-educacao DE PROPOSITO, e a razao merece registro porque contraria a
leitura literal da regra. O PLAYBOOK diz que token morto nao impede produzir —
o pacote pode ser renderizado e entregue no Drive esperando reautorizacao, e
foi o que fizemos com o sx-educacao-003. So que o sx-educacao-003 CONTINUA la,
parado desde 20/08, e o conteudo dele expira em 14/09. Produzir um segundo
pacote nao publicavel no mesmo canal nao entrega nada: gasta runner para
engordar uma fila que ja depende de uma acao do Pablo. A regra existe para
nao desperdicar um roteiro pronto, nao para acumular roteiros parados.

PASSO 0A — O QUE O CANAL JA DISSE (regra nova do Pablo, 24/08)

O Pablo mandou, no meio desta rodada, ler os dados do canal ANTES de produzir:
o que deu certo, o que nao deu, e o que muda por causa disso. Fiz isso com o
pacote ja em pe, e o resultado mudou o pacote. As tres frases, na ordem que a
regra pede:

  DEU CERTO: shorts, e um gancho so — perda pessoal datada, expressa como
  porcentagem do dinheiro do PROPRIO espectador. "Emerytura z ZUS: 34,4%
  pensji w 2050 roku" marca 128,00 views/dia. O segundo short DISTINTO do
  canal marca 22,60. E fator 5,7.

  NAO DEU: os longos, todos eles. Mediana ~1,4 views/dia, melhor da historia
  6,17, cinco zerados. O melhor longo do canal tem 37 views em 6 dias; o
  melhor short tem 1.152 em 9. E titulo neutro morre em qualquer formato —
  "Trzy liczby, ktore ustawiaja twoje finanse" e "OC najtansze od dwoch lat"
  estao os dois em 0,00.

  MUDEI: o gancho. O titulo deste pacote — um zloty a mais custa quase quatro
  mil — e da MESMA familia do unico vencedor do canal: perda pessoal, datada,
  numero que assusta, na segunda pessoa. Nao e o assunto do vencedor, e a
  forma dele. E o short leva o numero mais afiado e sai primeiro apontando
  para o longo.

O QUE NAO MUDEI, E POR QUE

Nao encurtei o longo. A tentacao era obvia: se longo nao paga aqui, corta para
o piso de 8 min e economiza. Mas fui olhar se duracao explica alguma coisa
neste canal e ela nao explica nada — o melhor longo tem 777,3 s e um dos
zerados tem 781,1 s, sem qualquer monotonia entre os nove. Encurtar seria
agir por palpite vestido de dado, que e exatamente o que o PASSO 0A existe
para impedir. Fica 13:16, como manda o veredito.

E UMA RESSALVA QUE PRECISA SUBIR PARA O PABLO

O veredito `liberado` deste canal esta apoiado em views duplicadas. Das ~4.029
views do acervo, ~3.100 sao CINCO COPIAS do mesmo short do ZUS, publicadas em
cinco dias seguidos pelo cron. O canal parece o melhor da frota porque o
v_maquina_licoes soma views do canal inteiro; medido por FORMATO, o short esta
liberado e o longo esta suspenso. Registrado como aprendizado 450, status
`candidato` — mexer na view e decisao do Pablo, nao minha.

KOLEJNY-POZIOM E O MELHOR CANAL DA FROTA, E POR MARGEM LARGA

v_maquina_licoes, medido em 24/08 05:39:

  - veredito: `liberado` — o UNICO da frota
  - 14 shorts, mediana 16,81 views/dia, topo 118,61
  - 14 longos, mediana 1,36 views/dia
  - 4.029 views no acervo

Para comparar, os dois canais que produzi hoje: nivel-do-jogo tem 352 views e
next-level-money tem 85. Este canal sozinho vale mais que a soma de varios
outros, e `liberado` libera a faixa inteira de 12 a 15 minutos.

O ACERVO, lido pelos titulos publicados

Nove titulos distintos, e o canal e maduro:

  - Emerytura z ZUS: 34,4% pensji w 2050          (x6 pelo cron)
  - Jak ulozyc finanse przy sredniej pensji 9233 zl
  - Nadplacac Kredyt czy Inwestowac w 2026
  - Oplaty i podatek Belki: 200 zl miesiecznie
  - IKE czy IKZE w 2026
  - Placa Minimalna 2026: Pracodawca Placi 5862 zl
  - Obligacje Skarbowe 2026: Szesc Ofert
  - Zdolnosc Kredytowa 2026: Dwa Banki
  - OC najtansze od dwoch lat

O EIXO ESCOLHIDO, E POR QUE NAO E REPETICAO DO 005

`pautas_banco` tem 86 pautas aqui. O eixo `forma-zatrudnienia` tem TREZE e
nenhuma tinha sido usada:

  [621] ZANIM Wybierzesz Spolke z o.o. ......................... 374,3 v/d
  [622] Z Twojej pracy zostaje Ci tylko 58% .................... 251,3
  [623] Prowadzenie Firmy Podrozeje ........................... 226,8
  [624] MORAWIECKI: jak zaoral 600 tysiecy firm ............... 206,7
  [626] ETAT czy freelance - ile naprawde zostaje na reke ..... 174,0
  ... mais oito

Marquei UMA, a [622], e nao o eixo inteiro — o titulo daqui copia a ESTRUTURA
dela (numero que quantifica perda pessoal do espectador), nao o assunto. As
outras doze seguem livres. Marcar eixo inteiro por ter usado um item ja
queimou 14 pautas boas antes.

Cuidado necessario: o pacote 005 ja tratou "o empregador paga 5862 e voce
recebe X", que e a CUNHA FISCAL sobre um salario fixo. Este aqui e outra
pergunta — nao quanto o sistema tira de um salario dado, e sim como o REGIME
escolhido muda a conta. Similaridade baixa, tema adjacente mas distinto.

A DOR DATADA, e o achado que virou o video

Numeros de 2026, confirmados em fontes independentes que batem (Symfonia,
portal.faktura.pl, gofin, bizky, vatax) e ancorados na regra do ZUS:

  Skladka zdrowotna no RYCZALT, 2026 — tres faixas FIXAS por receita anual:

    ate 60.000 zl ................... 498,35 zl/mes
    de 60.000 a 300.000 zl .......... 830,58 zl/mes
    acima de 300.000 zl ............. 1.495,04 zl/mes

  Base: media do setor empresarial no IV trimestre do ano anterior,
  9.228,64 zl. Deducao: 50% da skladka paga abate a receita.
  Skladka minima na skala podatkowa: 432,54 zl (9% do minimo de 4.806 zl).
  Limite de deducao no liniowy em 2026: 14.100 zl.

  E o detalhe que muda tudo, e que quase passou batido: se a receita cruza um
  limiar DURANTE o ano, a skladka dos meses anteriores e RECALCULADA pela
  faixa em que a receita ANUAL terminou. Nao vale a partir dali — vale para o
  ano inteiro, retroativamente.

  CORRIGI A REDACAO DISSO. A primeira versao dizia "pela aliquota do ultimo
  mes do ano". O efeito economico e o mesmo, porque a receita e cumulativa e a
  faixa do ultimo mes coincide com a faixa do ano — mas o mecanismo real e
  outro, e a diferenca aparece no BOLSO: a cobranca nao chega em dezembro. Ela
  sai no rozliczenie roczne da skladka zdrowotna, declarado no DRA de abril,
  com vencimento em 20 de MAIO do ano seguinte. Descrever como "recalculo do
  ultimo mes" esconde justamente o que dói — cinco meses entre a fatura que
  criou a divida e a conta que a cobra. Virou cena, nao nota de rodape.

O MECANISMO — e por que isso e materia de video e nao curiosidade

Some as duas coisas: faixa fixa mais recalculo retroativo.

  cruzar 60.000 zl por UM zloty:
      (830,58 - 498,35) x 12 = 3.986,76 zl a mais, no ano

  cruzar 300.000 zl por UM zloty:
      (1.495,04 - 830,58) x 12 = 7.973,52 zl a mais, no ano

Ou seja: existe um ponto onde faturar um zloty a mais deixa o empresario com
quase quatro mil zlotys A MENOS no bolso. Aliquota marginal efetiva de
centenas de milhares por cento numa faixa de um zloty de largura.

Isso nao e brecha nem irregularidade: e o desenho da regra, e ele e publico. O
que quase ninguem faz e a conta, porque a regra se le como "tres faixas" e nao
como "dois precipicios".

O QUE ESTE VIDEO NAO FAZ

  - nao diz para sonegar nem para esconder receita: a saida discutida e
    LEGAL e conhecida — a base considera a receita ABATIDA das contribuicoes
    sociais pagas, entao o timing do que se paga e do que se fatura importa;
  - nao diz que ryczalt e pior que skala ou liniowy: diz que a comparacao
    entre eles muda perto dos limiares, que e onde ninguem compara;
  - nao substitui contador, e afirma isso explicitamente. Um erro de faixa
    aqui custa mais do que qualquer honorario;
  - nao usa numero sem fonte: os tres valores da skladka e a base de
    9.228,64 zl aparecem citados, e a regra do recalculo retroativo tambem.

TAXA DA VOZ. pl-PL-MarekNeural: R = 20,07 chars/s — a MAIS RAPIDA da frota —
e P = 1,419 s/frase, a MAIS ALTA. n = 409, a maior amostra do MODELO_VOZ
inteiro. Vies do longo: -1,5%.

A combinacao e traicoeira: com P tao alto, as pausas entre frases sozinhas
valem ~250 s num roteiro de 800 s. Escrever frase curta aqui e queimar
orcamento em silencio. Por isso este roteiro usa frases mais longas e em menor
numero do que os dois anteriores de hoje.

ORCAMENTO (medido no arquivo pronto, nunca antes — aprendizado 436).

  86 cenas, 8 capitulos, 6 cenas no short.
  longo previsto ......... 808,2 s
  longo com vies -1,5% ... 796,0 s  = 13:16, dentro da faixa 12-15
  short previsto ......... 41,9 s   (teto seguro medido: 43,1)

  capitulos, em segundos previstos — todos entre MIN_CAP 60 e MAX_CAP 150:

    114,1  Jeden zloty, prawie cztery tysiace ......... 10 cenas
     73,4  Trzy kwoty na 2026 ......................... 8
    128,1  Pulapka retroaktywna ....................... 13
     94,8  Drugi prog jest gorszy ..................... 11
     78,3  Co naprawde liczy sie do progu ............. 10
    129,0  A co przy innych formach ................... 14
     85,6  Czego te liczby nie mowia .................. 9
    102,7  Co zrobic przed grudniem ................... 11

  A PRIMEIRA MEDICAO DEU 636,8 s — 10:36, quase dois minutos abaixo do piso de
  12 min de um canal `liberado`. Repeti o erro do 436 numa forma nova: nao
  errei a densidade por cena, errei a CONTAGEM — planejei 8 capitulos de 10 e
  escrevi 7. Consertei como manda o 436, com fato que faltava e nao com
  enchimento: de onde saem as tres kwotas (obwieszczenie do GUS de 22/01/2026,
  base 9.228,64 zl, faixas de 60/100/180% dela), quando a diferenca e
  realmente cobrada (20 de maio), e o que a skala NAO deixa deduzir. Sao 16
  cenas a mais, todas com informacao que o roteiro devia ter e nao tinha.

  DOIS PORTOES ME PEGARAM, e os dois estavam certos:

  1. NARRACAO — quatro cenas com 4 e 5 numeros numa frase so, "planilha
     falada". Em polones isso e pior que em qualquer outra lingua da frota,
     porque numero por extenso aqui e enorme: "siedem tysiecy dziewiecset
     siedemdziesiat trzy zlote piecdziesiat dwa grosze" e uma frase inteira
     sozinha. Quebrei as quatro em progressao.
  2. CAPITULOS — ao dividir o capitulo 1, que estava com 16 cenas e 2:44
     contra 1:18-2:08 dos outros, o novo capitulo saiu com 59,3 s e o portao
     cortou: MIN_CAP e 60. Nao arredondei o numero para passar; adicionei a
     cena que faltava — que essas kwotas sao MENSAIS e no ano viram quase seis
     mil zlotys na primeira faixa e quase dezoito mil na terceira.

DEPOIS DO RENDER — o que realmente saiu (medido, nao previsto)

  longo real ............. 808,8 s = 13:28   (previsto cru: 808,2 s)
  short real ............. 39,3 s            (previsto: 41,9 s)

  O modelo CRU errou 0,6 s em 808 — 0,07%. Eu, no entanto, anunciei 13:16,
  porque apliquei por cima o "vies registrado" do Marek, de -1,5%. Esse ajuste
  nao melhorou nada: piorou em 12,8 s.

  E a terceira medicao seguida a dizer a mesma coisa. Antonio previu 530,1 e
  saiu 528,7; Andrew previu 776,9 e saiu 781,0; Marek previu 808,2 e saiu
  808,8. O modelo de dois termos erra no maximo 0,53% em longo, e o vies por
  voz, aplicado por cima, PIORA a previsao em dois dos tres casos. Virou o
  aprendizado 454: em longo, use `duracao_estimada` crua e pare de corrigir.
  O VIES_SHORT continua valendo — aquele foi medido em short, e o short saiu
  6,2% abaixo do previsto, o que e outra conversa.

CAPITULOS abrem sempre em layout `titulo` (aprendizado 388).

ACENTUACAO: o portao de ortografia me pegou no pacote anterior por escrever
portugues sem acento nenhum. Em polones o risco e o mesmo e maior — ą, ć, ę,
ł, ń, ó, ś, ź, ż mudam a palavra, nao so a pronuncia. Escrito com diacritico
desde a primeira linha.
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


# ------------------------------------------------------- 1. Jeden złoty
T("Jeden złoty", "prawie cztery tysiące",
  "Jest w polskim systemie podatkowym punkt, w którym zafakturowanie jednego "
  "złotego więcej kosztuje przedsiębiorcę prawie cztery tysiące złotych. Nie "
  "przenośnia, tylko arytmetyka, i zaraz ją pokażę.",
  cap="Jeden złoty, prawie cztery tysiące")
T("To nie jest luka", "to jest konstrukcja",
  "Zaznaczam od razu: to nie jest luka w przepisach ani nic nielegalnego. To "
  "jest sposób, w jaki przepis został zbudowany, i jest jawny od początku.")
I("Rzecz dotyczy", "składki zdrowotnej na ryczałcie",
  "Chodzi o składkę zdrowotną na ryczałcie od przychodów ewidencjonowanych, "
  "czyli o formę, którą wybiera bardzo wielu jednoosobowych przedsiębiorców.")
T("Powód jest prosty", "składka nie rośnie płynnie",
  "Powód całego zjawiska jest jeden: na ryczałcie składka zdrowotna nie rośnie "
  "razem z przychodem. Ona stoi w miejscu, a potem skacze.")
L("Trzy progi w 2026", ["do 60 000 zł",
                        "od 60 000 do 300 000 zł",
                        "powyżej 300 000 zł"],
  "W dwa tysiące dwudziestym szóstym roku progi są trzy, i wyznacza je "
  "przychód roczny. Pierwszy sięga sześćdziesięciu tysięcy złotych.")
T("Drugi i trzeci", "trzysta tysięcy jest drugą granicą",
  "Drugi ciągnie się od sześćdziesięciu tysięcy do trzystu tysięcy. Trzeci "
  "zaczyna się powyżej trzystu tysięcy i nie ma już górnego końca.")
I("Skąd te kwoty", "9 228,64 zł podstawy",
  "Zanim podam stawki, powiem skąd one się biorą, bo to zmienia sposób "
  "patrzenia na nie. Wszystkie trzy są procentem jednej liczby ogłaszanej "
  "przez Główny Urząd Statystyczny.")
I("Obwieszczenie GUS", "22 stycznia 2026",
  "Tą liczbą jest przeciętne miesięczne wynagrodzenie w sektorze "
  "przedsiębiorstw w czwartym kwartale poprzedniego roku. Dla dwa tysiące "
  "dwudziestego szóstego wyniosło dziewięć tysięcy dwieście dwadzieścia osiem "
  "złotych i sześćdziesiąt cztery grosze.")
L("Podstawa progu", ["I próg — 60% przeciętnego",
                     "II próg — 100%",
                     "III próg — 180%"],
  "Pierwszy próg liczy się od sześćdziesięciu procent tej kwoty, drugi od stu "
  "procent, trzeci od stu osiemdziesięciu. A sama składka to dziewięć procent "
  "tak ustalonej podstawy.")
T("To znaczy jedno", "nikt nie wybiera tych kwot co roku",
  "Warto to zapamiętać, bo wynika z tego coś nieoczywistego. Tych kwot nikt "
  "nie ustala osobno co roku. One same jadą w górę razem ze statystyką płac, "
  "niezależnie od tego, jak idzie twojej firmie.")
T("Skoro znasz podstawę", "oto trzy kwoty",
  "Skoro wiesz już, od czego się to liczy, mogę podać trzy konkretne kwoty. To "
  "jest cała tabela na ten rok, i warto ją znać na pamięć.",
  cap="Trzy kwoty na 2026")
I("Pierwszy próg", "czterysta dziewięćdziesiąt osiem złotych",
  "W pierwszym progu składka wynosi czterysta dziewięćdziesiąt "
  "osiem złotych trzydzieści pięć groszy miesięcznie.")
T("I to bez znaczenia", "czy zarobiłeś dziesięć tysięcy, czy pięćdziesiąt dziewięć",
  "Tyle samo płaci ten, kto zafakturował dziesięć tysięcy w skali roku, i ten, "
  "kto zafakturował pięćdziesiąt dziewięć. Próg nie zna niczego pomiędzy.")
I("Drugi próg", "osiemset trzydzieści złotych",
  "W drugim progu jest to osiemset trzydzieści złotych pięćdziesiąt osiem "
  "groszy miesięcznie, i znowu tyle samo dla całej szerokości progu.")
I("Trzeci próg", "tysiąc czterysta dziewięćdziesiąt pięć złotych",
  "W trzecim progu tysiąc czterysta dziewięćdziesiąt pięć złotych cztery "
  "grosze miesięcznie, i tu już bez górnej granicy przychodu.")
T("To są kwoty miesięczne", "policz je na rok",
  "Pamiętaj tylko, że to są kwoty miesięczne, więc na rok wyglądają zupełnie "
  "inaczej. W pierwszym progu wychodzi z tego blisko sześć tysięcy złotych "
  "rocznie. W trzecim prawie osiemnaście tysięcy.")
T("Zauważ, co to znaczy", "wewnątrz progu nic się nie dzieje",
  "Zwróć uwagę, co z tego wynika. Wewnątrz progu możesz zwiększyć przychód "
  "wielokrotnie i składka nie drgnie ani o złotówkę.")
T("Ale na granicy", "dzieje się wszystko naraz",
  "Ale na samej granicy dzieje się wszystko naraz, i to jest miejsce, w którym "
  "ten film się zaczyna.")

# ------------------------------------------- 2. Pułapka retroaktywna
T("Druga część", "reguła, którą łatwo przeoczyć",
  "Sam skok między progami to jeszcze nie byłby dramat. Dramat robi druga "
  "zasada, którą bardzo łatwo przeoczyć przy pierwszym czytaniu przepisu.",
  cap="Pułapka retroaktywna")
I("Jeśli przekroczysz próg", "w trakcie roku",
  "Jeśli twój przychód przekroczy próg w trakcie roku, składka za miesiące "
  "wcześniejsze nie zostaje taka, jaka była.")
T("Ona jest przeliczana", "według progu z całego roku",
  "Ona zostaje przeliczona według progu, w którym wylądował twój przychód "
  "roczny. Wstecz, za wszystkie dwanaście miesięcy.")
I("I to nie w grudniu", "tylko w rozliczeniu rocznym",
  "Powiem od razu, kiedy to się dzieje, bo tu wielu daje się zaskoczyć. "
  "Różnicy nie dopłacasz w grudniu. Wychodzi ona dopiero w rocznym rozliczeniu "
  "składki zdrowotnej.")
I("Termin", "dwudziesty maja następnego roku",
  "To rozliczenie składasz w deklaracji za kwiecień, z terminem do "
  "dwudziestego maja następnego roku. Wtedy też płacisz to, czego zabrakło.")
T("Zwróć uwagę na odstęp", "faktura w grudniu, rachunek w maju",
  "Zwróć uwagę, co to oznacza w praktyce. Fakturę wystawiasz w grudniu, a "
  "rachunek za nią przychodzi pięć miesięcy później, kiedy tamtych pieniędzy "
  "dawno już nie ma na koncie.")
T("Czyli nie płacisz więcej", "od momentu przekroczenia",
  "Czyli nie jest tak, że od momentu przekroczenia płacisz więcej. Jest tak, "
  "że płacisz więcej za cały rok, łącznie z miesiącami, w których przychód był "
  "jeszcze niski.")
I("I dlatego", "grudzień decyduje o styczniu",
  "I właśnie dlatego to, co zafakturujesz w grudniu, decyduje o tym, ile "
  "kosztował cię styczeń. W normalnym rozumieniu czasu to nie ma prawa działać, "
  "a jednak działa.")
T("Policzmy pierwszy próg", "sześćdziesiąt tysięcy",
  "Policzmy więc pierwszy próg. Załóżmy, że przez jedenaście miesięcy twój "
  "przychód idzie w stronę pięćdziesięciu dziewięciu tysięcy.")
I("Płacisz przez cały rok", "czterysta dziewięćdziesiąt osiem złotych",
  "Płacisz czterysta dziewięćdziesiąt osiem złotych trzydzieści pięć groszy "
  "miesięcznie i wszystko się zgadza.")
T("I w grudniu", "wystawiasz jedną fakturę",
  "I w grudniu wystawiasz jedną fakturę, która przenosi cię o jeden złoty za "
  "próg sześćdziesięciu tysięcy.")
B("Rok wcześniej i po", ["498,35", "830,58"], [33, 55],
  "Od tej chwili cały rok liczy się po osiemset trzydzieści złotych "
  "pięćdziesiąt osiem groszy. Różnica to trzysta trzydzieści dwa złote "
  "dwadzieścia trzy grosze na każdym z dwunastu miesięcy.")
I("Razem", "trzy tysiące dziewięćset osiemdziesiąt sześć złotych",
  "Razem trzy tysiące dziewięćset osiemdziesiąt sześć złotych siedemdziesiąt "
  "sześć groszy. Za jednego złotego przychodu.")

# --------------------------------------------- 3. Drugi próg jest gorszy
T("A teraz drugi próg", "i on jest gorszy",
  "A teraz zróbmy dokładnie to samo na drugiej granicy, bo tam ta sama "
  "mechanika daje liczbę dwa razy większą.",
  cap="Drugi próg jest gorszy")
I("Granica", "trzysta tysięcy złotych",
  "Granica to trzysta tysięcy złotych rocznego przychodu, i powyżej niej "
  "składka wynosi tysiąc czterysta dziewięćdziesiąt pięć złotych cztery "
  "grosze miesięcznie.")
T("Różnica na miesiąc", "sześćset sześćdziesiąt cztery złote",
  "Różnica wobec drugiego progu to sześćset sześćdziesiąt cztery złote "
  "czterdzieści sześć groszy miesięcznie.")
I("Razy dwanaście", "siedem tysięcy dziewięćset siedemdziesiąt trzy złote",
  "Pomnóż to przez dwanaście miesięcy. Wychodzi siedem tysięcy dziewięćset "
  "siedemdziesiąt trzy złote i pięćdziesiąt dwa grosze.")
T("Czyli dwa razy tyle", "co na pierwszej granicy",
  "To jest dokładnie dwa razy więcej niż na pierwszej granicy, i z tego samego "
  "powodu: druga podstawa jest o tyle wyższa od pierwszej.")
T("Znowu za jednego złotego", "przychodu ponad próg",
  "Znowu za jednego złotego przychodu ponad próg, jeśli ten złoty pojawi się "
  "pod koniec roku.")
T("Nazwijmy to wprost", "to jest przepaść, nie schodek",
  "Nazwijmy więc rzecz po imieniu. To nie jest schodek w skali. To są dwie "
  "przepaście na drodze, która wygląda na płaską.")
L("Co z tego wynika", ["Przychód rośnie płynnie",
                       "Składka skacze",
                       "Wynik netto potrafi spaść"],
  "Wniosek jest niewygodny: przychód rośnie płynnie, składka skacze, a to "
  "znaczy, że twój wynik na rękę potrafi spaść przy rosnącym przychodzie.")
T("To jest rzadkie", "i dlatego zaskakuje",
  "W podatkach to rzadkie. Zwykle więcej przychodu oznacza więcej podatku, ale "
  "nigdy więcej niż zarobiłeś. Tutaj przez chwilę oznacza mniej pieniędzy.")
I("Szerokość tej strefy", "kilka tysięcy złotych",
  "Strefa, w której to się dzieje, ma szerokość kilku tysięcy złotych "
  "przychodu tuż nad progiem. Wąska, ale bardzo konkretna.")
T("I nikt cię o niej", "nie uprzedzi",
  "I nikt cię o niej nie uprzedzi w momencie wystawiania faktury, bo faktura "
  "nie wie, ile wynosi twój przychód roczny.")

# ------------------------------------------ 4. Co naprawdę liczy się do progu
T("Zanim policzysz swój próg", "sprawdź, co się do niego liczy",
  "Zanim jednak policzysz, gdzie jesteś, musisz wiedzieć jedną rzecz: do progu "
  "nie liczy się dokładnie ten przychód, o którym myślisz.",
  cap="Co naprawdę liczy się do progu")
I("Podstawą jest przychód", "pomniejszony o składki społeczne",
  "Podstawą jest przychód pomniejszony o zapłacone składki na ubezpieczenia "
  "społeczne, jeśli nie zaliczyłeś ich wcześniej do kosztów.")
T("To brzmi jak drobiazg", "a jest dźwignią",
  "Brzmi jak techniczny drobiazg, a jest jedyną dźwignią, jaką masz przy "
  "samej granicy.")
T("Bo to znaczy", "że zapłacone składki obniżają podstawę",
  "Znaczy bowiem, że składki, które faktycznie zapłacisz w danym roku, "
  "obniżają liczbę porównywaną z progiem.")
I("Druga rzecz", "pięćdziesiąt procent składki zdrowotnej",
  "Druga rzecz, osobna: na ryczałcie odliczasz od przychodu połowę zapłaconej "
  "składki zdrowotnej. Nie od podatku, tylko od przychodu.")
T("To dwie różne dźwignie", "i łatwo je pomylić",
  "To dwa różne mechanizmy i łatwo je pomylić, więc mówię wyraźnie: jeden "
  "dotyczy progu, drugi dotyczy podstawy opodatkowania.")
T("Trzecia rzecz", "moment zapłaty",
  "Trzecia rzecz jest najbardziej praktyczna: liczy się moment faktycznej "
  "zapłaty składki, a nie moment jej naliczenia.")
L("Co możesz kontrolować", ["Kiedy płacisz składki",
                            "Kiedy wystawiasz fakturę",
                            "Kiedy klient ją opłaca"],
  "Masz więc trzy rzeczy pod kontrolą: kiedy płacisz składki, kiedy wystawiasz "
  "fakturę, i w pewnym stopniu kiedy klient ją opłaca.")
T("I to wystarczy", "przy samej granicy",
  "I przy samej granicy to zwykle wystarczy, żeby nie wpaść w przepaść, o "
  "której mówiliśmy przed chwilą.")
I("Podkreślam", "to jest legalne planowanie",
  "Podkreślam mocno: mówimy o terminach płatności i fakturowania, czyli o "
  "rzeczach jawnych i legalnych. Nie o ukrywaniu przychodu.")

# ------------------------------------ 5. Jak to wygląda przy innych formach
T("Piąta część", "a co z innymi formami",
  "Skoro ryczałt zachowuje się w ten sposób, naturalne pytanie brzmi: czy na "
  "skali albo na liniowym jest lepiej. Odpowiedź jest: inaczej.",
  cap="A co przy innych formach")
I("Na skali podatkowej", "składka jest procentem dochodu",
  "Na skali podatkowej składka zdrowotna to procent dochodu, więc rośnie "
  "płynnie razem z nim. Nie ma progów i nie ma przepaści.")
I("Minimum na skali", "dziewięć procent płacy minimalnej",
  "Jest za to dolna granica: dziewięć procent minimalnego wynagrodzenia, a "
  "minimalne wynosi w tym roku cztery tysiące osiemset sześć złotych.")
I("Co daje", "czterysta trzydzieści dwa złote miesięcznie",
  "Z tego wychodzi czterysta trzydzieści dwa złote i pięćdziesiąt cztery "
  "grosze miesięcznie, i poniżej tej kwoty nie zejdziesz.")
T("Czyli w słabym miesiącu", "i tak zapłacisz",
  "Czyli nawet w miesiącu bez dochodu zapłacisz to minimum. To jest cena "
  "płynności, o której mało kto mówi, mówiąc że skala jest bezpieczniejsza.")
T("I jest druga cena", "o której mówi się jeszcze rzadziej",
  "Ale przy skali jest jeszcze druga rzecz, o której mówi się najrzadziej, a "
  "która potrafi zaważyć na całym porównaniu.")
I("Na skali", "składki nie odliczysz nigdzie",
  "Skala podatkowa jest jedyną formą, w której składki zdrowotnej nie odliczysz "
  "w żaden sposób. Ani od dochodu, ani od podatku, ani w kosztach.")
T("Porównaj z ryczałtem", "połowa składki wraca",
  "Na ryczałcie połowa zapłaconej składki pomniejsza przychód, na liniowym "
  "odliczysz ją do limitu, a na skali nie wraca nic. To znaczy, że płynność "
  "skali kosztuje więcej, niż wynika z samej stawki.")
I("Na liniowym", "limit odliczenia czternaście tysięcy sto",
  "Na podatku liniowym istnieje osobny limit: w dwa tysiące dwudziestym szóstym "
  "roku odliczysz składkę zdrowotną najwyżej do czternastu tysięcy stu złotych "
  "rocznie.")
T("Powyżej tego limitu", "składka przestaje się odliczać",
  "Powyżej tego limitu składka dalej rośnie, ale przestaje pomniejszać "
  "podstawę. To też jest rodzaj progu, tylko łagodniejszy.")
T("Wniosek nie jest taki", "że ryczałt jest zły",
  "Wniosek z tego nie jest taki, że ryczałt jest zły. Przy stabilnym przychodzie "
  "w środku progu ryczałt bywa najtańszą formą, jaka istnieje.")
I("Wniosek jest inny", "porównanie zmienia się przy granicy",
  "Wniosek jest węższy i ważniejszy: porównanie form opodatkowania zmienia "
  "wynik w pobliżu progu, a właśnie tam prawie nikt go nie powtarza.")
T("Bo formę wybiera się w styczniu", "a próg mija się w listopadzie",
  "Bo formę opodatkowania wybiera się na początku roku, a próg mija się gdzieś "
  "w okolicach listopada, kiedy decyzja jest już nieodwracalna.")
T("I to jest", "prawdziwy problem",
  "I to jest prawdziwy problem tej konstrukcji: decyzja i skutek są od siebie "
  "oddalone o jedenaście miesięcy.")

# ---------------------------------------- 6. Czego te liczby nie mówią
T("Szósta część", "granice tego, co powiedziałem",
  "Zanim przejdziemy do tego, co z tym zrobić, muszę wyraźnie powiedzieć, "
  "czego te liczby nie obejmują. Inaczej byłyby groźniejsze niż pomocne.",
  cap="Czego te liczby nie mówią")
I("Po pierwsze", "to nie jest cała składka ZUS",
  "Po pierwsze, mówiłem wyłącznie o składce zdrowotnej. Składki społeczne to "
  "osobna, duża pozycja i rządzą się własnymi zasadami.")
I("Po drugie", "stawka ryczałtu zależy od branży",
  "Po drugie, sama stawka ryczałtu zależy od rodzaju działalności i waha się "
  "bardzo mocno. Dwie firmy o tym samym przychodzie zapłacą różny podatek.")
T("Po trzecie", "ulgi zmieniają obraz",
  "Po trzecie, ulgi i odliczenia potrafią przesunąć całą kalkulację, a ja tu "
  "policzyłem czysty przypadek bez żadnych ulg.")
I("Po czwarte", "progi są roczne, nie miesięczne",
  "Po czwarte, progi liczą się od przychodu rocznego. Jeden dobry miesiąc "
  "nie przenosi cię do wyższego progu, jeśli rok zamknie się niżej.")
T("I najważniejsze", "to nie zastępuje księgowego",
  "I najważniejsze: to nie zastępuje rozmowy z księgowym. Pomyłka o jeden próg "
  "kosztuje więcej niż jakiekolwiek honorarium za tę rozmowę.")
T("Mówię to serio", "nie z ostrożności",
  "Mówię to nie z ostrożności prawnej, tylko dlatego, że policzyliśmy przed "
  "chwilą, ile kosztuje pomyłka. Prawie cztery tysiące na pierwszym progu.")
L("Co jest pewne", ["Trzy progi i ich kwoty",
                    "Przeliczenie wstecz",
                    "Podstawa po składkach społecznych"],
  "Pewne jest to: trzy progi i ich kwoty, przeliczenie wstecz przy "
  "przekroczeniu, i podstawa liczona po zapłaconych składkach społecznych.")
T("Reszta", "zależy od twojej firmy",
  "Cała reszta zależy od tego, czym się zajmujesz i jak wygląda twój rok. I to "
  "jest dokładnie ta część, której nie zrobię za ciebie w filmie.")

# ------------------------------------------ 7. Co zrobić przed grudniem
T("Siódma część", "co z tym zrobić",
  "Przejdźmy więc do tego, co możesz zrobić, i zacznijmy od tego, kiedy to "
  "trzeba zrobić, bo termin jest tu ważniejszy niż sama czynność.",
  cap="Co zrobić przed grudniem")
I("Termin", "wcześniej niż myślisz",
  "Sprawdzenie ma sens najpóźniej w okolicach października i listopada, kiedy "
  "wiesz już mniej więcej, gdzie rok się zamknie.")
T("W grudniu", "zostają tylko dwie dźwignie",
  "W grudniu zostają ci już tylko dwie dźwignie: data wystawienia faktury i "
  "data zapłaty składek. Wcześniej masz ich więcej.")
L("Trzy kroki", ["Policz przychód po składkach",
                 "Sprawdź odległość od progu",
                 "Zaplanuj grudzień"],
  "Trzy kroki. Policz przychód pomniejszony o zapłacone składki społeczne. "
  "Sprawdź, jak daleko jesteś od progu. I dopiero wtedy zaplanuj grudzień.")
I("Jeśli jesteś tuż pod progiem", "to jest strefa decyzji",
  "Jeśli okaże się, że jesteś kilka tysięcy pod progiem, to jest właśnie ta "
  "strefa, w której warto policzyć, zanim wystawisz kolejną fakturę.")
T("Czasem odpowiedź brzmi", "wystaw w styczniu",
  "Czasem odpowiedź brzmi po prostu: wystaw tę fakturę w styczniu. Ten sam "
  "przychód, inny rok podatkowy, próg nietknięty.")
T("A czasem odpowiedź brzmi", "przekrocz zdecydowanie",
  "A czasem odpowiedź jest odwrotna: jeśli i tak przekroczysz próg, to lepiej "
  "przekroczyć go wyraźnie, bo koszt skoku jest stały, a przychód już nie.")
I("To jest sedno", "koszt skoku jest stały",
  "To jest sedno całej sprawy. Koszt przekroczenia progu jest stały i wynosi "
  "prawie cztery tysiące. Im więcej zarobisz ponad próg, tym mniej boli.")
T("Najgorsze miejsce", "to tuż nad progiem",
  "Najgorsze miejsce na świecie to jeden złoty ponad progiem. Najlepsze to "
  "albo wyraźnie pod nim, albo wyraźnie nad nim.")
T("W następnym odcinku", "składki społeczne",
  "W następnym odcinku wezmę drugą część tej samej opłaty, czyli składki "
  "społeczne, i sprawdzę, ile naprawdę kupujesz za to, co co miesiąc płacisz.")
C("Jeśli to było przydatne", "zostaw subskrypcję",
  "Jeśli ta kalkulacja była przydatna, zostaw subskrypcję, a w komentarzu "
  "napisz, czy trafiłeś kiedyś w ten próg i ile cię to kosztowało.")


# Orçamento medido para ~40 s com 6 cenas na voz Marek.
SHORT = [
    {"layout": "titulo", "kicker": "Jeden złoty", "sub": "prawie cztery tysiące",
     "nar": "Jest punkt, w którym zafakturowanie jednego złotego więcej kosztuje "
            "cię prawie cztery tysiące złotych.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Ryczałt", "sub": "składka nie rośnie płynnie",
     "nar": "Na ryczałcie składka zdrowotna nie rośnie razem z przychodem. Stoi "
            "w miejscu, a potem skacze.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Próg", "sub": "sześćdziesiąt tysięcy",
     "nar": "Przy sześćdziesięciu tysiącach przychodu skacze z czterystu "
            "dziewięćdziesięciu ośmiu złotych na osiemset trzydzieści.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "I liczy się wstecz", "sub": "za cały rok",
     "nar": "A po przekroczeniu progu przeliczasz cały rok wstecz, nie tylko "
            "miesiące od przekroczenia.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Razem", "sub": "trzy tysiące dziewięćset",
     "nar": "Razem trzy tysiące dziewięćset osiemdziesiąt sześć złotych. Za "
            "jednego złotego przychodu.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Co z tym zrobić", "sub": "sprawdź w listopadzie",
     "nar": "Co z tym zrobić i kiedy sprawdzić, tłumaczę na kanale.",
     "sem_cap": True},
]

THUMB = {"l1": "jeden złoty", "l2": "3986 zł kary"}

COPY = """# Składka na ryczałcie nie rośnie płynnie — ona stoi, a potem skacze

## TITULO
Ryczałt 2026: Jeden Złoty Ponad Progiem Kosztuje Prawie 4000 zł

## DESCRICAO
W polskim systemie istnieje punkt, w którym zafakturowanie jednego złotego więcej kosztuje przedsiębiorcę prawie cztery tysiące złotych rocznie. To nie jest luka w przepisach ani nic nielegalnego — to sposób, w jaki przepis został zbudowany, jawny od początku. Rzecz dotyczy składki zdrowotnej na ryczałcie od przychodów ewidencjonowanych.

Powód jest jeden: na ryczałcie składka zdrowotna nie rośnie razem z przychodem. W 2026 roku obowiązują trzy progi liczone od rocznego przychodu — do 60 000 zł składka wynosi 498,35 zł miesięcznie, między 60 000 a 300 000 zł jest to 830,58 zł, a powyżej 300 000 zł — 1 495,04 zł. Wewnątrz progu można zwiększyć przychód wielokrotnie i składka nie drgnie. Na granicy dzieje się wszystko naraz.

Dramat robi druga zasada, łatwa do przeoczenia: jeśli przychód przekroczy próg w trakcie roku, składka za wcześniejsze miesiące zostaje przeliczona według progu, w którym wylądował przychód roczny. Wstecz, za wszystkie dwanaście miesięcy. To, co zafakturujesz w grudniu, decyduje o tym, ile kosztował cię styczeń. Różnicy nie dopłacasz jednak w grudniu — wychodzi ona w rocznym rozliczeniu składki zdrowotnej, składanym w deklaracji za kwiecień, z terminem do 20 maja następnego roku. Między fakturą a rachunkiem mija pięć miesięcy.

Policzmy pierwszy próg. Różnica między 498,35 zł a 830,58 zł to 332,23 zł miesięcznie. Razy dwanaście miesięcy — 3 986,76 zł. Za jednego złotego przychodu. Na drugiej granicy ta sama mechanika daje 664,46 zł miesięcznie, czyli 7 973,52 zł rocznie.

Film pokazuje też, co naprawdę liczy się do progu: podstawą jest przychód pomniejszony o zapłacone składki na ubezpieczenia społeczne, a liczy się moment faktycznej zapłaty, nie naliczenia. To jedyna legalna dźwignia przy samej granicy — mowa o terminach fakturowania i płatności, nie o ukrywaniu przychodu. Osobno omówione jest odliczenie 50% zapłaconej składki zdrowotnej od przychodu.

Dla porównania: na skali podatkowej składka to procent dochodu i rośnie płynnie, ale istnieje minimum — 9% minimalnego wynagrodzenia, czyli przy płacy 4 806 zł daje 432,54 zł miesięcznie nawet w miesiącu bez dochodu. Na podatku liniowym limit odliczenia składki w 2026 roku wynosi 14 100 zł rocznie.

Wniosek nie brzmi „ryczałt jest zły". Przy stabilnym przychodzie w środku progu ryczałt bywa najtańszą formą, jaka istnieje. Wniosek jest węższy: porównanie form opodatkowania zmienia wynik w pobliżu progu — a formę wybiera się w styczniu, gdy próg mija się w listopadzie, kiedy decyzja jest już nieodwracalna.

Na końcu konkretna procedura na październik i listopad oraz wyraźna lista tego, czego ten materiał nie obejmuje.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Pytanie do księgowych i do tych, którzy w ten próg kiedyś trafili: jak często w praktyce udaje się zaplanować grudzień tak, żeby zostać pod progiem, a jak często klient płaci wtedy, kiedy chce, i cała kalkulacja bierze w łeb? To jedyna część tego materiału, której nie da się policzyć — zależy od tego, kto komu wystawia fakturę.

## HASHTAGS
#Ryczałt #SkładkaZdrowotna #KolejnyPoziom

## TAGS
ryczalt 2026, skladka zdrowotna, jdg, dzialalnosc gospodarcza, progi przychodu, zus przedsiebiorcy, podatek liniowy, skala podatkowa, ksiegowosc, finanse firmy, optymalizacja podatkowa, przychod roczny, rozliczenie roczne, jednoosobowa dzialalnosc, podatki w polsce

## CONFIGURACAO DE STUDIO
- Język: polski (pl-PL) | Kategoria: Edukacja (27)
- Nie jest treścią dla dzieci
- Ujawnienie treści zmienionej lub syntetycznej: TAK (głos generowany przez AI)
- Lokalizacja: Polska | Licencja: standardowa licencja YouTube
- Reklamy mid-roll: włączone (czas powyżej ośmiu minut)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
Stan na 24 sierpnia 2026. Wysokości składki zdrowotnej na ryczałcie w 2026 roku — 498,35 zł do 60 000 zł przychodu, 830,58 zł między 60 000 a 300 000 zł oraz 1 495,04 zł powyżej 300 000 zł — potwierdzone w niezależnych źródłach branżowych zgodnych co do kwot. Podstawą wyliczenia jest przeciętne wynagrodzenie w sektorze przedsiębiorstw za IV kwartał roku poprzedniego, wraz z wypłatami z zysku, które wyniosło 9 228,64 zł. Zasada przeliczenia wstecz przy przekroczeniu progu w trakcie roku — składka za wszystkie miesiące według progu właściwego dla rocznego przychodu — jest regułą rozliczenia rocznego, nie interpretacją autora; rozliczenie to składa się w deklaracji za kwiecień, z terminem do 20 maja następnego roku. Podstawa 9 228,64 zł pochodzi z obwieszczenia Prezesa GUS z 22 stycznia 2026 r., a trzy progi to kolejno 60%, 100% i 180% tej kwoty, po 9%. Do progu przyjmuje się przychód pomniejszony o zapłacone składki na ubezpieczenia społeczne; na ryczałcie odliczeniu od przychodu podlega 50% zapłaconej składki zdrowotnej. Minimalna składka na skali podatkowej to 9% minimalnego wynagrodzenia, które w 2026 roku wynosi 4 806 zł, co daje 432,54 zł. Limit odliczenia składki na podatku liniowym w 2026 roku to 14 100 zł. Wyliczenia 3 986,76 zł i 7 973,52 zł to prosta arytmetyka z powyższych kwot pomnożonych przez dwanaście miesięcy, przedstawiona w filmie krok po kroku. Materiał nie obejmuje składek społecznych, nie uwzględnia stawek ryczałtu zależnych od branży ani żadnych ulg, i nie stanowi porady podatkowej — decyzję o formie opodatkowania należy skonsultować z księgowym.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-010",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#14213D", "c1": "#FCA311", "c2": "#E5E5E5", "bg": "#F7F5F0"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "kolejny-poziom-010.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
