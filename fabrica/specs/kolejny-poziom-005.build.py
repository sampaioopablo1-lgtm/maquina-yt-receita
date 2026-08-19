#!/usr/bin/env python3
"""Monta a spec kolejny-poziom-005 — quanto voce custa e quanto voce recebe.

POR QUE ESTE CANAL AGORA. O kolejny-poziom marcava 10 de 10 e estava dado por
pronto. Nao estava: seis das dez linhas eram o MESMO video ("Emerytura z ZUS"),
republicado todo dia de 11 a 17/08 pelo cron. Sao CINCO longos distintos, e o
canal continua devendo cinco. A contagem do orquestra.estado foi corrigida na
mesma passada para contar video distinto em vez de linha.

E ele e o canal certo entre os disponiveis: dos doze tokens, tres respondem, e
os outros dois vivos sao o epomeno-epipedo (ja em tres pacotes hoje, no teto) e
o setiap-level (dez longos DISTINTOS, meta cumprida de verdade). Alem disso o
kolejny rende 0,71 v/d no longo contra 0,13 do setiap — cinco vezes mais no
unico formato que conta para o YPP.

PAUTA, medida em 19/08/2026. Rodei dois eixos poloneses ineditos para o canal
(forma de contrato e encargos). Dezesseis videos de 90 dias, mediana 72,3 v/d:

    ZANIM Wybierzesz Spolke z o.o. (Mecenas Biznesu)          374,3 v/d
    Z Twojej pracy zostaje Ci tylko 58%. Reszte zabiera...    251,3
    Prowadzenie Firmy Podrozeje                              226,8
    ETAT czy freelance - POLICZYLEM ile naprawde zostaje      174,0
    NAJWIEKSZE KLAMSTWO O ETACIE i B2B                        11,3

Os dois ultimos defendem a MESMA tese e estao a quinze vezes de distancia. A
diferenca esta no verbo: um diz "policzylem" e poe a conta na tela; o outro
anuncia uma mentira e argumenta. E a terceira vez no mesmo dia que a medicao
diz isso — no eixo grego de credito (280,6 contra 2,4) e no da acrivia (88,3
contra 3,3). Demonstrar bate afirmar, e agora sao tres eixos, tres idiomas.

Modelo a ESTRUTURA do video de 251,3: uma afirmacao direta com UM numero e a
pergunta "para onde vai o resto". Nao modelo o assunto — spolka z o.o. e
empreendedorismo, nao folha de pagamento.

NUMEROS VERIFICADOS (2026, duas fontes que batem — podatnik.info e
zarobkistatystyki.pl, as duas citando ZUS e Ministerio das Financas; a folha
minima confirmada tambem por levantamento de salario minimo):

  LADO DO EMPREGADO, sobre o bruto:
    emerytalna 9,76% · rentowa 1,50% · chorobowa 2,45%  = 13,71%
    zdrowotna 9% sobre (bruto menos ZUS)
  LADO DO EMPREGADOR, ACIMA do bruto, cerca de 20,48%:
    emerytalna 9,76% · rentowa 6,50% · wypadkowa 1,67% (referencia, faixa
    0,67 a 3,33) · Fundusz Pracy e Solidarnosciowy 2,45% · FGSP 0,10%
    PPK: mais 1,50% quando o empregado nao desiste

  SALARIO MINIMO 2026: bruto 4.806 zl · liquido cerca de 3.605 zl ·
    custo do empregador 5.862,37 zl · hora minima 31,40 zl
  MEDIA (przecietne) 2026: cerca de 9.420 zl bruto, custo 11.349,22 zl
  MEDIANA (fevereiro 2026): 7.690,82 zl — mais de 20% abaixo da media
  Teto anual de contribuicao (30-krotnosc) 2026: 282.600 zl

O ACHADO: no salario minimo, o empregador desembolsa 5.862 e o trabalhador
recebe 3.605. Sao 61,5% do que foi gasto. Os dois numeros sao institucionais —
nao precisei calcular nenhum dos dois, o que e mais forte do que uma conta
minha.

SIMILARIDADE vs os cinco longos distintos do canal (aposentadoria do ZUS,
plano com salario medio de 9.233, amortizar vs investir, taxas e imposto
Belka, IKE vs IKZE): todos sao sobre o que fazer com o dinheiro DEPOIS que
ele chega. Este e sobre o caminho ANTES de chegar. Eixo novo.

A ponte com o video do salario medio aparece uma vez e de proposito: aquele
usou 9.233 zl, e a media de 2026 subiu para cerca de 9.420. Continuidade sem
repeticao.

SEM BROLL: o Pexels da TimeoutError a partir do runner.

DIMENSIONAMENTO. pl-PL-MarekNeural = 19,93 chars/s + 1,477 s/frase, n=74.
Alvo no MEIO da janela: ~13,2 min.
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
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub, "nar": nar,
                  "sem_cap": True})


# ------------------------------------------------------------------ cap 1
T("Trzy liczby", "jedna umowa",
  "Trzy liczby opisują tę samą umowę o pracę. Prawie nikt nie zna "
  "pierwszej.",
  cap="Trzy liczby, jedna umowa")
I("Pierwsza", "co wydaje pracodawca",
  "Pierwsza to kwota, którą pracodawca faktycznie wydaje na to stanowisko "
  "każdego miesiąca.")
I("Druga", "brutto z umowy",
  "Druga to brutto zapisane w umowie. Tę znasz, bo ją podpisałeś.")
I("Trzecia", "co wpływa na konto",
  "Trzecia to kwota, która wpływa na konto. Tę znasz najlepiej, bo to ona "
  "kupuje zakupy.")
I("Przy najniższej krajowej", "brutto cztery osiemset sześć",
  "Weźmy najniższą krajową dwa tysiące dwadzieścia sześć. Brutto to cztery "
  "tysiące osiemset sześć złotych.")
I("Na rękę", "około trzy sześćset pięć",
  "Na rękę zostaje z tego około trzy tysiące sześćset pięć złotych.")
I("A koszt pracodawcy", "pięć osiemset sześćdziesiąt dwa",
  "A pracodawca wydaje na to samo stanowisko pięć tysięcy osiemset "
  "sześćdziesiąt dwa złote i trzydzieści siedem groszy.")
B("Ta sama umowa", ["Koszt", "Brutto", "Na rękę"], [1.0, 0.82, 0.615],
  "Ta sama umowa, trzy słupki. Z lewej to, co wychodzi z firmy. Z prawej "
  "to, co wchodzi do ciebie.")
I("Różnica", "sześćdziesiąt jeden procent",
  "Do ciebie trafia około sześćdziesięciu jeden procent tego, co zostało "
  "wydane. Reszta nie znika. Ma nazwy, i zaraz je wypiszemy.")
I("Jedno od razu", "to nie jest film polityczny",
  "Jedno od razu i wyraźnie. To nie jest film polityczny i nikogo tu nie "
  "oskarżamy. Czytamy przepisy i liczymy.")
I("Zasada kanału", "liczby ze źródłem",
  "I obowiązuje zasada kanału. Liczby ze źródłem i datą, a czego nie da się "
  "zmierzyć, tego nie mówimy.")
I("Dla kogo to jest", "dla każdego na etacie",
  "I dotyczy to każdego na umowie o pracę, niezależnie od kwoty. Zmienia się "
  "wysokość, nie mechanizm.")
L("Co zobaczymy", ["Co dopłaca pracodawca ponad brutto",
                   "Co znika z brutto zanim zobaczysz",
                   "Ta sama liczba przy średniej krajowej",
                   "Dlaczego to nie jest to samo co B2B",
                   "Co z tym zrobić"],
  "Pięć części. Co pracodawca dopłaca ponad brutto. Co znika z brutto, zanim "
  "je zobaczysz. Jak to wygląda przy średniej krajowej. Dlaczego to nie jest "
  "to samo co B2B. I co z tym zrobić.")
T("Zaczynamy", "co dopłaca pracodawca?",
  "Zacznijmy od strony, której nie widać na pasku. Co dokładnie dopłaca "
  "pracodawca?")

# ------------------------------------------------------------------ cap 2
T("Ponad brutto", "około dwadzieścia procent",
  "Ponad kwotę brutto pracodawca dokłada jeszcze około dwudziestu procent. "
  "To pięć pozycji, i każda ma swoją nazwę.",
  cap="Co dopłaca pracodawca")
I("Emerytalna", "dziewięć siedemdziesiąt sześć",
  "Składka emerytalna po stronie pracodawcy to dziewięć i siedemdziesiąt "
  "sześć setnych procent podstawy.")
I("Ta sama liczba u ciebie", "składka jest dzielona",
  "Dokładnie tyle samo płacisz ty. Ta składka jest dzielona po połowie, i "
  "to jedyna, która tak działa.")
I("Rentowa", "sześć i pół",
  "Rentowa po stronie pracodawcy to sześć i pół procenta. Po twojej stronie "
  "tylko półtora.")
I("Wypadkowa", "około jeden sześćdziesiąt siedem",
  "Wypadkowa to około jeden i sześćdziesiąt siedem setnych procenta. Płaci "
  "ją wyłącznie pracodawca.")
I("Ona się zmienia", "od branży",
  "I to jedyna, która zależy od branży. Waha się mniej więcej od zera "
  "sześćdziesiąt siedem do trzech trzydziestu trzech setnych.")
I("Fundusz Pracy", "dwa czterdzieści pięć",
  "Fundusz Pracy razem z Funduszem Solidarnościowym to dwa i czterdzieści "
  "pięć setnych procenta.")
I("FGŚP", "dziesięć setnych",
  "I najmniejsza pozycja na liście. Fundusz Gwarantowanych Świadczeń "
  "Pracowniczych, dziesięć setnych procenta.")
I("Razem", "dwadzieścia i pół",
  "Razem daje to około dwudziestu i pół procenta ponad brutto. Nie zobaczysz "
  "tego na pasku, bo to nie jest twoja wypłata.")
I("A PPK", "jeszcze półtora",
  "A jeśli jesteś w PPK i nie zrezygnowałeś, pracodawca dokłada jeszcze "
  "półtora procenta. Wtedy koszt rośnie do tych pięciu tysięcy ośmiuset "
  "sześćdziesięciu dwóch.")
I("Jedna rzecz, której tu nie ma", "koszty okołopłacowe",
  "I jedna rzecz, której w tych procentach nie ma. Płatny urlop i szkolenia "
  "to osobny koszt. Sprzęt i miejsce pracy również. Prawdziwy koszt "
  "stanowiska jest więc jeszcze wyższy.")
I("Dlaczego to ważne", "to jest twoja cena",
  "To ma znaczenie z jednego powodu. Kiedy firma liczy, ile kosztujesz, "
  "liczy tę kwotę. Nie brutto.")
T("Dobra", "a co znika z brutto?",
  "Wiemy już, co jest nad brutto. A co znika spod niego?")

# ------------------------------------------------------------------ cap 3
T("Pod brutto", "trzy potrącenia",
  "Z brutto schodzą trzy rzeczy, w tej kolejności. ZUS, zdrowotna, podatek.",
  cap="Co znika z brutto")
I("Najpierw ZUS", "trzynaście siedemdziesiąt jeden",
  "Najpierw twoje składki społeczne. Trzynaście i siedemdziesiąt jeden "
  "setnych procenta brutto.")
L("Z czego się składa", ["Emerytalna 9,76%", "Rentowa 1,50%",
                         "Chorobowa 2,45%"],
  "Emerytalna, rentowa i chorobowa. Chorobowa to ta, dzięki której masz "
  "płatne zwolnienie.")
I("Potem zdrowotna", "dziewięć procent",
  "Potem składka zdrowotna, dziewięć procent. I tu jest szczegół, który "
  "myli prawie wszystkich.")
I("Od czego liczona", "nie od brutto",
  "Zdrowotna nie jest liczona od brutto. Jest liczona od brutto pomniejszonego "
  "o składki społeczne.")
I("Dlaczego to istotne", "kolejność ma znaczenie",
  "Dlatego kolejność ma znaczenie. Każde potrącenie zmienia podstawę dla "
  "następnego.")
I("Na końcu podatek", "od tego, co zostało",
  "Na końcu podatek dochodowy. Liczy się go od tego, co zostało, i "
  "pomniejsza o kwotę wolną rozłożoną na miesiące.")
I("Kwota wolna", "trzysta złotych miesięcznie",
  "Warto znać jeszcze jeden mechanizm, bo działa co miesiąc. Kwota wolna od "
  "podatku jest rozłożona na dwanaście części i zmniejsza zaliczkę o "
  "trzysta złotych miesięcznie.")
I("Efekt", "trzy tysiące sześćset pięć",
  "Efekt przy najniższej krajowej znasz z początku filmu. Trzy tysiące "
  "sześćset pięć złotych na konto.")
I("Policzmy dystans", "od pięciu ośmiuset do trzech sześciuset",
  "Policzmy więc cały dystans. Firma wydaje pięć tysięcy osiemset "
  "sześćdziesiąt dwa. Ty dostajesz trzy tysiące sześćset pięć.")
I("To nie jest oskarżenie", "to jest mapa",
  "I jeszcze raz: to nie jest oskarżenie. To mapa. Część tych pieniędzy "
  "wróci do ciebie w emeryturze i w zwolnieniu lekarskim.")
I("Ale warto ją znać", "bo zmienia rozmowę",
  "Warto ją jednak znać, bo zmienia jedną konkretną rozmowę. Tę o "
  "podwyżce.")
T("Zobaczmy wyżej", "a przy średniej krajowej?",
  "To była najniższa krajowa. A jak to wygląda przy średniej?")

# ------------------------------------------------------------------ cap 4
T("Średnia krajowa", "około dziewięć tysięcy czterysta",
  "Przeciętne wynagrodzenie w dwa tysiące dwadzieścia sześć to około "
  "dziewięciu tysięcy czterystu złotych brutto.",
  cap="Przy średniej krajowej")
I("Mały przypis", "w zeszłym filmie było mniej",
  "Mały przypis do naszego filmu o planie finansowym. Wtedy liczyliśmy przy "
  "dziewięciu tysiącach dwustu trzydziestu trzech. Średnia od tego czasu "
  "urosła.")
I("Koszt pracodawcy", "jedenaście trzysta czterdzieści dziewięć",
  "Przy tej pensji koszt pracodawcy to jedenaście tysięcy trzysta "
  "czterdzieści dziewięć złotych.")
I("Proporcja się trzyma", "około sześćdziesiąt procent",
  "Proporcja trzyma się bardzo podobnie. Do ciebie trafia mniej więcej "
  "sześćdziesiąt procent tego wydatku.")
I("I tu wchodzi mediana", "siedem sześćset dziewięćdziesiąt",
  "Ale jest jeszcze jedna liczba, ważniejsza od średniej. Mediana "
  "wynagrodzeń w lutym to siedem tysięcy sześćset dziewięćdziesiąt złotych.")
I("Ponad dwadzieścia procent niżej", "od średniej",
  "To ponad dwadzieścia procent poniżej średniej. I to mediana, a nie "
  "średnia, opisuje typowego pracownika.")
I("Gdzie mieszka mediana", "zależy od wielkości firmy",
  "Mediana też nie jest jedna. W dużych firmach potrafi sięgać dziewięciu "
  "tysięcy, a w najmniejszych schodzi do samej płacy minimalnej.")
I("Dlaczego średnia zawyża", "kilka bardzo wysokich pensji",
  "Średnią windują nieliczne bardzo wysokie pensje. Mediana jest odporna na "
  "to, bo dzieli ludzi na pół.")
I("Co z tego wynika", "porównuj się z medianą",
  "Praktyczny wniosek jest prosty. Jeśli porównujesz swoją pensję do "
  "średniej krajowej, porównujesz się z rozkładem, a nie z ludźmi.")
I("Jest jeszcze sufit", "trzydziestokrotność",
  "Jest też sufit, o którym mało kto wie. Roczna podstawa składek "
  "emerytalnej i rentowej ma limit, w tym roku dwieście osiemdziesiąt dwa "
  "tysiące sześćset złotych.")
I("Co się dzieje powyżej", "składki się zatrzymują",
  "Powyżej tego limitu te dwie składki przestają być naliczane do końca "
  "roku. Dlatego wysokie pensje mają inną proporcję niż twoja.")
T("Skoro tak", "to może B2B?",
  "Skoro etat kosztuje tyle, to nasuwa się jedno pytanie. Może B2B?")

# ------------------------------------------------------------------ cap 5
T("Etat i B2B", "to nie są te same liczby",
  "I tu popełnia się najczęstszy błąd w całym temacie. Porównuje się brutto "
  "z etatu do kwoty z faktury.",
  cap="Dlaczego to nie to samo co B2B")
I("Dlaczego to źle", "różne poziomy",
  "To dwa różne poziomy tej samej drabiny. Brutto z etatu nie zawiera "
  "składek pracodawcy. Kwota z faktury zawiera wszystko.")
I("Właściwe porównanie", "koszt do faktury",
  "Uczciwe porównanie jest inne. Zestaw koszt pracodawcy z kwotą na "
  "fakturze. Dopiero te dwie liczby stoją na tym samym poziomie.")
I("Przy najniższej", "pięć osiemset sześćdziesiąt dwa",
  "Czyli przy najniższej krajowej punktem odniesienia nie jest cztery "
  "osiemset sześć. Jest pięć osiemset sześćdziesiąt dwa.")
I("Co dochodzi po drugiej stronie", "urlop i chorobowe",
  "A po stronie B2B trzeba dodać rzeczy, których faktura nie pokazuje. "
  "Urlop, który sam sobie płacisz. Chorobowe, którego może nie być.")
I("I jeszcze emerytura", "składki budują kapitał",
  "Jest też różnica, której nie widać przez kilka lat. Składki emerytalne z "
  "etatu budują kapitał na twoim koncie w ZUS. Na najniższych składkach z "
  "działalności ten kapitał rośnie wolniej.")
I("I księgowość", "koszt stały",
  "Dochodzi też księgowość, własne ubezpieczenie i czas na formalności. To "
  "nie są duże kwoty osobno, ale są stałe.")
I("Nie mówię, że B2B jest gorsze", "mówię, że liczy się inaczej",
  "Nie twierdzę, że B2B jest gorsze. Twierdzę, że wymaga innego rachunku, i "
  "że większość porównań w internecie porównuje niewłaściwe liczby.")
I("Test na trzy pytania", "zanim policzysz",
  "Zanim policzysz, odpowiedz sobie na trzy rzeczy. Ile dni urlopu bierzesz "
  "rocznie. Ile razy chorowałeś. I jak stabilny jest ten jeden klient.")
T("Mamy mapę", "co z nią zrobić?",
  "Mamy komplet liczb. Co z nimi zrobić w praktyce?")

# ------------------------------------------------------------------ cap 6
T("Cztery ruchy", "dziesięć minut",
  "Cztery ruchy, wszystkie na jedną kartkę, wszystkie w dziesięć minut.",
  cap="Co z tym zrobić")
I("Pierwszy", "znajdź swój koszt",
  "Pierwszy. Policz swój koszt pracodawcy. Weź brutto i dodaj do niego około "
  "dwudziestu i pół procenta.")
I("Po co", "to jest twoja cena rynkowa",
  "To jest liczba, którą firma widzi obok twojego nazwiska. I to od niej "
  "zaczyna się każda decyzja o twoim stanowisku.")
I("Drugi", "policz swoją proporcję",
  "Drugi. Podziel to, co masz na koncie, przez ten koszt. Dostaniesz swoją "
  "własną proporcję, w procentach.")
I("I sprawdź stawkę wypadkową", "jest na deklaracji",
  "Sprawdź też, jaka stawka wypadkowa obowiązuje w twojej firmie. To jedyna "
  "pozycja z całej listy, która potrafi się różnić kilkukrotnie między "
  "branżami.")
I("Trzeci", "przelicz podwyżkę w kosztach",
  "Trzeci, i ten zmienia rozmowy o pieniądzach. Kiedy prosisz o podwyżkę "
  "brutto, firma widzi wzrost powiększony o te dwadzieścia procent.")
I("Co z tego wynika", "wiesz, o czym rozmawiacie",
  "Nie znaczy to, że masz prosić o mniej. Znaczy, że wiesz, jaką liczbę "
  "widzi druga strona. I przestajesz się dziwić jej reakcji.")
I("Czwarty", "sprawdź PPK świadomie",
  "Czwarty. Sprawdź, czy jesteś w PPK, i zdecyduj świadomie. To jedyna "
  "pozycja z tej listy, o której naprawdę decydujesz.")
I("Ile to zajmuje", "dziesięć minut",
  "Wszystkie cztery razem to dziesięć minut z paskiem wypłaty. Żaden nie "
  "wymaga rozmowy z nikim.")
T("Kartka gotowa", "co może to zepsuć?",
  "Kartka jest gotowa. Co może ją zepsuć?")

# ------------------------------------------------------------------ cap 7
T("Cztery błędy", "które psują rachunek",
  "Pierwszy błąd to mylenie kosztu pracodawcy z twoim brutto. To dwie różne "
  "liczby i różnią się o jedną piątą.",
  cap="Cztery błędy")
I("Drugi błąd", "liczyć zdrowotną od brutto",
  "Drugi to liczenie zdrowotnej od brutto. Ona jest liczona od podstawy "
  "pomniejszonej o składki społeczne.")
I("Trzeci błąd", "brać wypadkową jak stałą",
  "Trzeci to traktowanie składki wypadkowej jak stałej. Ona zależy od "
  "branży i potrafi się różnić kilkukrotnie.")
I("Czwarty błąd", "mylić średnią z medianą",
  "I czwarty, najczęstszy poza tym tematem. Mylenie średniej z medianą. "
  "Mediana jest ponad dwadzieścia procent niżej.")
I("Jedno zastrzeżenie", "to są liczby typowe",
  "I jedno uczciwe zastrzeżenie. Wszystkie te liczby to wartości typowe, a "
  "nie twoja umowa. Ulgi, wiek i forma zatrudnienia potrafią je zmienić.")
I("Czego to NIE mówi", "nie mówi, czy zarabiasz mało",
  "I na koniec, uczciwie. Ta kartka nie mówi ci, czy zarabiasz mało, ani czy "
  "składki są za wysokie. Mówi tylko, gdzie dokładnie są twoje pieniądze.")
L("Podsumowanie", ["Koszt 5862, na rękę 3605",
                   "Pracodawca dopłaca ~20,5% ponad brutto",
                   "Zdrowotna nie od brutto",
                   "Mediana 7690, nie średnia",
                   "B2B porównuj do kosztu"],
  "Pięć rzeczy do zapamiętania. Dystans między kosztem a kontem. Że "
  "pracodawca dopłaca około jednej piątej ponad brutto. Że zdrowotna nie jest "
  "liczona od brutto. Że mediana jest niżej niż średnia. I że B2B porównuje "
  "się do kosztu, nie do brutto.")
I("Jeśli zrobisz jedną rzecz", "policz swój koszt",
  "Jeśli po tym filmie zrobisz jedną rzecz, policz swój koszt pracodawcy. "
  "Brutto plus jedna piąta.")
I("Dlaczego akurat to", "zmienia następną decyzję",
  "Bo od momentu, w którym znasz tę liczbę, każda następna rozmowa o "
  "pieniądzach wygląda inaczej.")
C("Kolejny Poziom", "na liczbach, nie na wrażeniach",
  "To wszystko. Kolejny Poziom, na liczbach i źródłach, nie na wrażeniach.")

SHORT = [
    {"layout": "titulo", "kicker": "5862 zł", "sub": "i 3605 zł",
     "nar": "Pracodawca wydaje pięć tysięcy osiemset sześćdziesiąt dwa "
            "złote. Ty dostajesz trzy tysiące sześćset pięć.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Ta sama", "preco": "umowa",
     "nar": "Ta sama umowa. Najniższa krajowa dwa tysiące dwadzieścia sześć.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Do ciebie", "preco": "61 procent",
     "nar": "Do ciebie trafia około sześćdziesięciu jeden procent tego "
            "wydatku.", "sem_cap": True},
    {"layout": "item", "kicker": "Reszta", "preco": "ma nazwy",
     "nar": "Reszta nie znika. Emerytalna, rentowa, zdrowotna, podatek.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Źródło", "preco": "ZUS i MF",
     "nar": "Stawki z ZUS i Ministerstwa Finansów, rok bieżący.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Cały rozkład", "sub": "na kanale",
     "nar": "Cały rozkład i cztery ruchy na kartkę, w pełnym filmie.",
     "sem_cap": True},
]

COPY = """# Koszt pracodawcy 5862 zł, na rękę 3605 zł: gdzie znika reszta

## TYTUŁ
Płaca Minimalna 2026: Pracodawca Płaci 5862 zł, a Ty Dostajesz 3605 zł

## OPIS
Trzy liczby opisują tę samą umowę o pracę, a większość ludzi zna tylko dwie. Przy najniższej krajowej w 2026 roku brutto wynosi 4806 zł, na konto wpływa około 3605 zł, a całkowity koszt po stronie pracodawcy to 5862,37 zł miesięcznie. Oznacza to, że do pracownika trafia mniej więcej 61% tego, co realnie zostało wydane na jego stanowisko.

Ten film nie jest materiałem politycznym i nikogo nie oskarża. Reszta tych pieniędzy nie znika — ma konkretne nazwy, konkretne stawki i częściowo wraca do ciebie w postaci emerytury czy płatnego zwolnienia. Chodzi o to, żeby wiedzieć, gdzie dokładnie jest ta różnica i jak ją policzyć na własnym pasku.

Rozkładamy obie strony. Ponad kwotą brutto pracodawca dopłaca około 20,5%: emerytalną 9,76%, rentową 6,50%, wypadkową około 1,67% (stawka zależy od branży i waha się od 0,67% do 3,33%), Fundusz Pracy z Funduszem Solidarnościowym 2,45% oraz FGŚP 0,10%. Do tego dochodzi 1,5% wpłaty do PPK, jeśli pracownik nie zrezygnował. Pod kwotą brutto znikają natomiast twoje składki społeczne w wysokości 13,71%, składka zdrowotna 9% — i tu ważny szczegół, którego prawie nikt nie liczy poprawnie: zdrowotna naliczana jest nie od brutto, tylko od podstawy pomniejszonej o składki społeczne — a na końcu podatek dochodowy.

Pokazujemy też, jak te same proporcje wyglądają przy średniej krajowej, gdzie przy około 9420 zł brutto koszt pracodawcy sięga 11 349,22 zł. I dlaczego znacznie ważniejsza od średniej jest mediana wynagrodzeń, która w lutym 2026 wyniosła 7690,82 zł — ponad 20% mniej niż średnia. Wyjaśniamy, dlaczego to mediana, a nie średnia, opisuje typowego pracownika.

Na koniec najczęstszy błąd w porównaniach etatu z B2B: zestawianie brutto z etatu z kwotą na fakturze. To dwa różne poziomy tej samej drabiny. Uczciwe porównanie to koszt pracodawcy kontra faktura — i pokazujemy, co jeszcze trzeba doliczyć po stronie działalności. Wychodzisz z filmu z czterema ruchami na jedną kartkę, do zrobienia w dziesięć minut.

## ROZDZIAŁY
{CAPITULOS}

## KOMENTARZ
Jedno pytanie, bo odpowiedź zmienia się z branży na branżę: znałeś swój koszt pracodawcy przed tym filmem, czy widzisz tę liczbę pierwszy raz? Bez wstydu — zbieram odpowiedzi do następnego materiału. A jeśli chcesz ten sam rozkład dla B2B albo dla umowy zlecenia, napisz którą; najczęściej wskazana idzie pierwsza.

## HASHTAG
#PłacaMinimalna #KosztPracodawcy #KolejnyPoziom

## TAGI
placa minimalna 2026, koszt pracodawcy, skladki zus, wynagrodzenie brutto netto, zus 2026, skladka zdrowotna, na reke, etat czy b2b, mediana wynagrodzen, srednia krajowa, ppk, finanse osobiste, polska, podatki, kolejny poziom

## USTAWIENIA STUDIO
- Język: polski (pl) | Kategoria: Edukacja (27)
- Nie jest przeznaczone dla dzieci
- Deklaracja treści syntetycznej: TAK (głos AI)
- Lokalizacja: Polska | Licencja: standardowa licencja YouTube
- Reklamy mid-roll: włączone (powyżej 8 minut)

## MUZYKA / LICENCJA
{TRILHA}

## ŹRÓDŁA
Stawki składek na 2026 rok pochodzą z zestawień powołujących się na ZUS i Ministerstwo Finansów, zgodnych między sobą co do wartości (podatnik.info, „Całkowity koszt zatrudnienia pracownika w 2026 roku", oraz zarobkistatystyki.pl, „Składki ZUS 2026 — stawki, tabela i koszt pracodawcy"), dostęp 19.08.2026. Konkretnie: po stronie pracownika emerytalna 9,76%, rentowa 1,50% i chorobowa 2,45%, razem 13,71%, oraz zdrowotna 9% liczona od podstawy pomniejszonej o składki społeczne; po stronie pracodawcy emerytalna 9,76%, rentowa 6,50%, wypadkowa około 1,67% (zakres 0,67%–3,33% zależnie od branży), Fundusz Pracy i Fundusz Solidarnościowy 2,45% oraz FGŚP 0,10%, łącznie około 20,48% ponad brutto, plus 1,5% wpłaty podstawowej pracodawcy do PPK. Płaca minimalna 2026: 4806 zł brutto, minimalna stawka godzinowa 31,40 zł, około 3605 zł netto, całkowity koszt zatrudnienia 5862,37 zł. Przeciętne wynagrodzenie 2026: około 9420 zł brutto przy koszcie pracodawcy 11 349,22 zł. Mediana wynagrodzeń, luty 2026: 7690,82 zł. Roczny limit podstawy wymiaru składek emerytalnej i rentowej (trzydziestokrotność) w 2026 roku: 282 600 zł. Wszystkie kwoty są wartościami typowymi dla standardowych założeń i NIE stanowią wyliczenia dla konkretnej umowy — ulgi podatkowe, wiek, forma zatrudnienia i stawka wypadkowa danej branży zmieniają wynik. To materiał edukacyjny o czytaniu paska wypłaty; nie jest poradą podatkową ani prawną.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-005",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    # CORRIGIDO depois da publicacao. Eu declarei Deliberate_Thought e o video
    # foi ao ar assim; a identidade do canal e Wholesome (canais.trilha e as
    # specs 002-004). O video publicado mantem a faixa antiga — republicar so
    # por causa dela criaria a duplicata que passei a manha consertando. A
    # spec fica certa para qualquer render futuro.
    "trilha": "Wholesome",
    "paleta": {"ink": "#14213D", "c1": "#C1121F", "c2": "#457B9D", "bg": "#F1F0EA"},
    "thumb": {"l1": "5862 CZY 3605?", "l2": "ta sama umowa"},
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p = "fabrica/specs/kolejny-poziom-005.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=1)
        f.write("\n")
    from ensaio import MODELO_VOZ, duracao_estimada  # noqa: E402
    R, P = MODELO_VOZ[SPEC["voz"]]
    dl = duracao_estimada(CENAS, SPEC["voz"])
    ds = duracao_estimada(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"voz {SPEC['voz']}: {R} chars/s + {P} s/frase")
    print(f"longo: {sum(len(c['nar']) for c in CENAS)} chars -> {dl/60:.1f} min")
    print(f"short: {sum(len(c['nar']) for c in SHORT)} chars -> {ds:.0f} s")
