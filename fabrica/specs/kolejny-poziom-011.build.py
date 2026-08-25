#!/usr/bin/env python3
"""Monta a spec kolejny-poziom-011.

ALAVANCA ATACADA: **B — os primeiros 200 segundos**. E esta e a PRIMEIRA spec
escrita sob a versao corrigida da regra, porque o dado derrubou a anterior
(aprendizado 483, critico).

O QUE DEU CERTO. Este e o canal de melhor retencao da frota. Cinco longos
entre 24,6% e 31,3%, e o melhor deles tem NOVE capitulos.

O QUE NAO DEU. A duracao. Medido em 25/08/2026, com `duracao_media_s` de
`metricas`, os SEGUNDOS REALMENTE VISTOS nao acompanham a duracao:

    687s -> 31,3% -> 215s vistos   (9 capitulos)
    773s -> 28,4% -> 219s vistos
    756s -> 26,3% -> 198s vistos
    803s -> 26,2% -> 210s vistos
    839s -> 17,4% -> 145s vistos
    781s ->  4,8% ->  37s vistos   (89 cenas, o mais picado)

Os cinco melhores ficam entre 191 e 219 segundos, de 687s a 803s de duracao.
As pessoas veem tres minutos e meio e saem, e alongar o video NAO soma
exibicao — so derruba a retencao, porque retencao e essencialmente
duzentos dividido pela duracao.

O QUE VOU MUDAR POR CAUSA DISSO, e sao tres coisas concretas:

  1. DURACAO NO PISO. O veredito e `liberado`, faixa de 12 a 15 min. Vou ao
     PISO e nao ao teto. O melhor video do canal tem 11:27; o pior, 13:01.
     Ate hoje eu mirava o meio da faixa por habito, nao por medida.
     FICOU EM 12:21, e nao nos 12:00 exatos, e o motivo importa: com dez
     capitulos, o piso de 60 s do `copy_md.capitulos` impoe 600 s so de
     capitulo, e apertar ate 12:00 derrubaria capitulo. Entre perder capitulo
     e gastar 21 segundos, os 21 segundos custam menos — retencao aqui e ~200
     dividido pela duracao, e 21 s valem meio ponto percentual.

  2. A RESPOSTA DENTRO DOS PRIMEIROS 200 SEGUNDOS. O numero, as duas faixas e
     o metodo de se localizar nelas terminam em 2:13 — o resto dos primeiros
     200 s ja e a proposta de 2027. Quem sai aos 3,5 min sai sabendo fazer a
     conta. Os capitulos seguintes aprofundam para quem fica, nao revelam.

  3. MAIS CAPITULOS: DEZ. O de melhor retencao tem nove e o de pior, sete.
     CENA NAO E A VARIAVEL, e eu tinha escrito que era. Conferindo: o melhor
     tem 76 cenas em 687 s (9,0 s/cena) e o pior tem 89 em 781 s (8,8 s/cena)
     — a densidade e a MESMA nos dois, entao "menos cenas" nao separa nada.
     O que separa e capitulo. Ficaram 77 cenas, e isso nao e concessao: e a
     variavel que nao move o resultado.

  4. E O QUE ESTA MUDANCA REVELOU. Dez capitulos desenhados produziriam CINCO:
     `copy_md.capitulos` so abre capitulo 60 s depois do anterior, e capitulos
     de 56 a 58 s sumiam calados. O `prontidao._gate_capitulos` nao acusou
     porque so opinava entre 6 e 8 — ou seja, calava-se exatamente na faixa
     que a rotina passou a pedir. Portao corrigido no mesmo commit, com teto
     12 e mensagem que nomeia a DISTANCIA em vez do layout.

--------------------------------------------------------------------- A PAUTA

Eixo: a escala de imposto de renda pessoal. NUNCA usado neste canal — os
anteriores sao OC, zdolnosc kredytowa, obligacje, placa minimalna, IKE/IKZE,
podatek Belki, emerytura ZUS, nadplacanie e a media salarial de 9233 zl.

E e METODO por natureza, que e a forma que converte (aprendizado 482): o
espectador pega o proprio salario, multiplica por doze, e se localiza.

FONTES INSTITUCIONAIS, tres, que se confirmam:

  1. ESCALA ATUAL — biznes.gov.pl, portal oficial do governo:
       kwota wolna od podatku .............. 30.000 zl
       kwota zmniejszajaca podatek ......... 3.600 zl  (= 30.000 x 12%)
       ate 120.000 zl ...................... 12% menos 3.600 zl
       acima de 120.000 zl ................. 10.800 zl + 32% do excedente

  2. REFORMA PROPOSTA para 2027 — gov.pl/web/premier, Chancelaria do
     Primeiro-Ministro:
       I prog sobe para .................... 130.000 zl, ainda a 12%
       nova faixa intermediaria ............ 24% de 130.000 a 150.000 zl
       32% passa a valer .................... acima de 150.000 zl
       beneficiados ........................ 3,5 milhoes de contribuintes,
                                             sobretudo empregados
       economia maxima anual ............... ate 3.600 zl
       fatia que paga 32% .................. cai de 14% para 7,2%

  3. MECANICA DA SKALA — podatki.gov.pl e gov.pl/web/finanse, Ministerio das
     Financas, mais biznes.gov.pl. Tres coisas que nenhuma das duas primeiras
     cobre, e que sao METODO e nao curiosidade:
       wspolne rozliczenie ................. imposto = 2 x imposto(metade da
                                             renda somada do casal). Na
                                             pratica o prog do casal se
                                             comporta como 240.000 zl.
       PIT-2 / kwota zmniejszajaca ......... 1/12 de 3.600 = 300 zl por mes,
                                             aplicados pelo platnik SO se o
                                             oswiadczenie tiver sido entregue;
                                             divisivel em 150+150 ou 100x3,
                                             nunca somando mais de 300.
       aliquota no contracheque ............ o platnik usa 12% enquanto a
                                             renda acumulada do ano fica sob o
                                             prog, e 32% A PARTIR DO MES em
                                             que ele e ultrapassado.
       historico do prog ................... 85.528 zl de 2009 ate 2021, sem
                                             mexer; 120.000 zl a partir de
                                             2022. Uma unica mudanca.

A CONFERENCIA QUE VALEU A PENA. O capitulo 5 nao repete o "ate 3.600 zl" da
fonte 2 — ele DERIVA. A 150.000 zl: hoje 10.800 + 32% x 30.000 = 20.400 zl;
com a proposta 12% x 130.000 - 3.600 = 12.000, mais 24% x 20.000 = 4.800,
total 16.800 zl. Diferenca: 3.600 zl exatos. E acima de 150.000 as duas
escalas correm na mesma aliquota, entao a diferenca congela ali — o "ate" da
fonte e um TETO, e o teto e alcancado em 150.000. Duas rotas independentes
chegando ao mesmo numero e o motivo de o video afirma-lo.

CUIDADO QUE O VIDEO TOMA: a escala de 2026 e LEI; a de 2027 e PROPOSTA. O
video diz isso em voz alta e nao trata a segunda como certa. Numero que ainda
nao virou lei nao vira promessa.

A ANCORA CONCRETA vem do proprio acervo do canal: a media salarial polonesa
de 9.233 zl que este canal ja publicou da 110.796 zl por ano — LOGO ABAIXO do
primeiro degrau. Ou seja, o polones medio esta a um aumento de distancia do
prog, e nao sabe.

O QUE O VIDEO NAO FAZ: nao e aconselhamento fiscal, nao entra em ulgas e
odliczenia (sao dezenas e mudam o resultado caso a caso), e nao afirma que a
reforma vai ser aprovada.

ACENTOS. Polones com todos os diacriticos: a, c, e, l, n, o, s, z com kreska
e z com kropka.
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


# ============================ OS PRIMEIROS 200 SEGUNDOS ======================
# Tudo o que o espectador precisa para fazer a conta esta nos capitulos 1 a 3.
# Quem sair aos 3,5 min sai sabendo. O resto aprofunda, nao revela.

# ------------------------------------------------------------------- cap 1
T("Jedna liczba", "dzieli twoją pensję na dwie części",
  "Jest jedna liczba, która dzieli twoją roczną pensję na dwie części "
  "opodatkowane zupełnie inaczej. Dziś podam ci ją od razu.",
  cap="Liczba, która dzieli pensję")
I("Ta liczba", "sto dwadzieścia tysięcy",
  "To sto dwadzieścia tysięcy złotych rocznie. Poniżej płacisz dwanaście "
  "procent. Powyżej, od nadwyżki, trzydzieści dwa.")
I("Nie od całości", "tylko od nadwyżki",
  "I to jest pierwsze nieporozumienie: wyższa stawka nie dotyczy całej "
  "pensji. Dotyczy wyłącznie tego, co jest ponad próg.")
I("Skąd bierze się strach", "z nieporozumienia",
  "Wiele osób słyszy o progu i wyobraża sobie, że po jego przekroczeniu cała "
  "pensja jest opodatkowana wyżej. Tak to nie działa, i za chwilę zobaczysz "
  "na liczbach, o ile mniej to boli.")
I("Kwota wolna", "trzydzieści tysięcy",
  "Do tego kwota wolna od podatku wynosi trzydzieści tysięcy złotych, i "
  "stąd bierze się kwota zmniejszająca podatek: trzy tysiące sześćset.")
I("Dwa wzory", "i to są wszystkie",
  "Poniżej progu podatek to dwanaście procent podstawy minus trzy tysiące "
  "sześćset złotych. Powyżej progu to dziesięć tysięcy osiemset złotych plus "
  "trzydzieści dwa procent od nadwyżki.")
I("To są całe zasady", "reszta to szczegóły",
  "To są całe zasady skali. Wszystko inne to już tylko szczegóły i "
  "przykłady.")

# ------------------------------------------------------------------- cap 2
T("Gdzie jesteś", "jedno mnożenie",
  "Teraz najważniejsze: jak sprawdzić, po której stronie progu jesteś.",
  cap="Gdzie jesteś na skali")
I("Krok pierwszy", "brutto razy dwanaście",
  "Weź swoją miesięczną pensję brutto i pomnóż przez dwanaście. To twój "
  "roczny przychód.")
I("Krok drugi", "odejmij składki",
  "Odejmij od tego zapłacone składki na ubezpieczenie społeczne: emerytalną, "
  "rentową i chorobową. Znajdziesz je na pasku wypłaty albo w rocznym "
  "zestawieniu od pracodawcy. Zostaje podstawa opodatkowania.")
I("Krok trzeci", "porównaj ze stem dwudziestoma",
  "Porównaj tę podstawę ze stem dwudziestoma tysiącami. Jeśli jest niżej, "
  "cała twoja pensja jest w pierwszej stawce.")
I("Średnia krajowa", "9233 złote",
  "Konkret: przy średniej pensji dziewięć tysięcy dwieście trzydzieści trzy "
  "złote miesięcznie wychodzi sto dziesięć tysięcy siedemset dziewięćdziesiąt "
  "sześć złotych rocznie. Czyli poniżej progu, ale niewiele.")
B("Ile brakuje", ["Średnia roczna", "Próg"], [92, 100],
  "Od średniej pensji do progu brakuje mniej niż dziesięć tysięcy złotych "
  "rocznie. To jedna podwyżka.")
I("Dlatego to nie jest", "temat dla bogatych",
  "Dlatego to nie jest temat dla bogatych. To temat dla osoby, która właśnie "
  "dostała podwyżkę.")

# ------------------------------------------------------------------- cap 3
T("Co się zmienia", "propozycja na 2027",
  "I tu dochodzimy do powodu, dla którego robię ten film teraz.",
  cap="Propozycja zmian od 2027")
I("Rząd zapowiedział", "trzy progi",
  "Kancelaria Prezesa Rady Ministrów przedstawiła propozycję zmiany skali "
  "podatkowej. Zamiast dwóch stawek mają być trzy.")
I("Pierwszy próg", "sto trzydzieści tysięcy",
  "Pierwszy próg ma zostać podniesiony do stu trzydziestu tysięcy złotych, "
  "wciąż ze stawką dwanaście procent.")
I("Nowa stawka", "dwadzieścia cztery procent",
  "Powyżej stu trzydziestu tysięcy, aż do stu pięćdziesięciu, ma pojawić się "
  "nowa, pośrednia stawka: dwadzieścia cztery procent.")
I("Trzydzieści dwa", "dopiero powyżej 150",
  "A trzydzieści dwa procent ma dotyczyć dopiero dochodów powyżej stu "
  "pięćdziesięciu tysięcy złotych.")
I("Od kiedy", "nie w tym roku",
  "Zmiana miałaby wejść w życie dopiero od kolejnego roku podatkowego, a nie "
  "w rozliczeniu, które składasz teraz. Twój najbliższy PIT liczy się według "
  "obecnej skali.")
I("To jest propozycja", "nie jest ustawą",
  "I mówię to wyraźnie: to jest projekt i zapowiedź. Nie jest to jeszcze "
  "obowiązujące prawo, i tak trzeba to traktować.")
I("Kogo dotyczy", "trzy i pół miliona",
  "Według rządu skorzystałoby na tym ponad trzy i pół miliona podatników, "
  "przede wszystkim pracowników. Ci, którzy zyskają najwięcej, "
  "zaoszczędziliby rocznie nawet trzy tysiące sześćset złotych.")

# ============ do aqui, ~200 segundos. O que segue aprofunda. ================

# ------------------------------------------------------------------- cap 4
T("Dlaczego coraz więcej", "próg, który stał w miejscu",
  "Zostawmy na chwilę propozycję i zobaczmy, co działo się do tej pory. To "
  "wyjaśnia, skąd ta zmiana w ogóle się wzięła.",
  cap="Dlaczego coraz więcej osób płaci 32%")
I("Stary próg", "85 528 złotych",
  "Przez lata drugi próg wynosił osiemdziesiąt pięć tysięcy pięćset "
  "dwadzieścia osiem złotych. Ta sama liczba, rok po roku, od dwa tysiące "
  "dziewiątego aż do końca dwa tysiące dwudziestego pierwszego.")
I("Jedyna zmiana", "dopiero potem",
  "Dopiero potem podniesiono go do stu dwudziestu tysięcy złotych. To była "
  "jedyna zmiana tego progu w kilkunastu latach.")
I("Pensje nie stały", "próg tak",
  "W tym samym czasie pensje nominalnie rosły, a próg się nie ruszał. "
  "Nazywa się to pełzaniem progów, i skutek jest mechaniczny: coraz więcej "
  "osób wpada do wyższej stawki, choć w ustawie nikt niczego nie zmienił.")
I("Prognoza bez zmian", "czternaście procent",
  "Bez nowych parametrów odsetek podatników płacących trzydzieści dwa "
  "procent miał urosnąć do czternastu procent.")
B("Odsetek w drugiej stawce", ["Bez zmian", "Po zmianie"], [100, 51],
  "Po zmianie parametrów miałby wynieść siedem i dwie dziesiąte procent. To "
  "mniej więcej połowa tej grupy.")
I("Dlatego to nie prezent", "to korekta",
  "Dlatego podniesienie progu nie jest prezentem. Jest odwróceniem "
  "mechanizmu, który działał kilkanaście lat i nikogo o zdanie nie pytał.")

# ------------------------------------------------------------------- cap 5
T("Policzmy", "trzy podstawy",
  "Policzmy to teraz na trzech konkretnych podstawach, w złotówkach, a nie "
  "w procentach.",
  cap="Trzy przykłady w złotówkach")
I("Pierwsza podstawa", "sto tysięcy",
  "Podstawa sto tysięcy złotych. Dwanaście procent z tej kwoty daje "
  "dwanaście tysięcy złotych. Odejmujemy kwotę zmniejszającą podatek i "
  "zostaje osiem tysięcy czterysta złotych, dziś i po zmianie tyle samo.")
I("Druga podstawa", "sto trzydzieści pięć tysięcy",
  "Podstawa sto trzydzieści pięć tysięcy złotych. Nadwyżka ponad dzisiejszy "
  "próg to piętnaście tysięcy, więc podatek wynosi dziesięć tysięcy osiemset "
  "plus trzydzieści dwa procent od tej nadwyżki. Razem piętnaście tysięcy "
  "sześćset złotych.")
I("Ta sama podstawa po zmianie", "trzynaście tysięcy dwieście",
  "Po zmianie pierwszy próg sięga stu trzydziestu tysięcy, więc do tej kwoty "
  "liczymy dwanaście procent. Reszta wpada w stawkę dwadzieścia cztery "
  "procent. Wychodzi trzynaście tysięcy dwieście złotych.")
I("Różnica", "dwa tysiące czterysta",
  "Różnica na tej jednej podstawie to dwa tysiące czterysta złotych rocznie. "
  "To realna kwota, a nie punkt procentowy.")
I("Trzecia podstawa", "sto sześćdziesiąt tysięcy",
  "Podstawa sto sześćdziesiąt tysięcy złotych. Dziś podatek wynosi "
  "dwadzieścia trzy tysiące sześćset złotych, a po zmianie dwadzieścia "
  "tysięcy. Różnica to trzy tysiące sześćset.")
I("I tu jest sufit", "wyżej już nie rośnie",
  "Na tym różnica się zatrzymuje. Powyżej stu pięćdziesięciu tysięcy obie "
  "skale mają tę samą stawkę, więc oszczędność przestaje rosnąć.")
I("To zgadza się ze źródłem", "ta sama liczba",
  "Rząd podaje oszczędność do trzech tysięcy sześciuset złotych rocznie. Ta "
  "sama liczba wychodzi z samego rachunku, i właśnie dlatego jej ufam.")
I("Zasada", "zawsze od nadwyżki",
  "W każdym z tych przypadków wyższa stawka dotyczy tylko nadwyżki ponad "
  "próg, nigdy całej pensji. Dlatego nie ma sensu odmawiać podwyżki ze "
  "strachu przed progiem: po jego przekroczeniu zawsze zostaje ci więcej.")

# ------------------------------------------------------------------- cap 6
T("Dwoje ludzi", "jeden rachunek",
  "Jest jeszcze jedna rzecz, która potrafi zmienić to, po której stronie "
  "progu jesteś. I nie ma z nią nic wspólnego wysokość twojej pensji.",
  cap="Dwoje ludzi, jeden próg")
I("Wspólne rozliczenie", "z małżonkiem",
  "Chodzi o wspólne rozliczenie z małżonkiem. To prawo, a nie obowiązek, i "
  "wniosek składa się w zeznaniu rocznym.")
I("Jak liczy się podatek", "od połowy, razy dwa",
  "Podatek ustala się wtedy w podwójnej wysokości podatku obliczonego od "
  "połowy łącznych dochodów obojga małżonków.")
I("Co to daje", "próg działa jak podwójny",
  "W praktyce dla pary próg zachowuje się tak, jakby był dwa razy wyższy niż "
  "dla jednej osoby.")
I("Konkret", "dwieście czterdzieści tysięcy",
  "Jeśli łączna podstawa pary nie przekracza dwustu czterdziestu tysięcy "
  "złotych, całość mieści się w pierwszej stawce.")
I("Kiedy to działa", "gdy dochody się różnią",
  "Efekt jest największy wtedy, gdy jedno z małżonków zarabia dużo, a drugie "
  "mało albo wcale. Jeśli oboje są nisko i zarabiają podobnie, wynik bywa "
  "taki sam jak przy rozliczeniu osobnym.")
I("Warunki", "cały rok i wspólność",
  "Trzeba pozostawać w małżeństwie i we wspólności majątkowej przez cały rok "
  "podatkowy. Są też wyłączenia dla niektórych form opodatkowania.")
I("Dlaczego o tym mówię", "bo przenosi przez próg",
  "Mówię o tym, bo to jedyna rzecz z tego filmu, która potrafi przenieść "
  "cię na drugą stronę progu bez żadnej zmiany pensji.")

# ------------------------------------------------------------------- cap 7
T("Trzysta złotych", "co miesiąc",
  "Teraz coś, co dotyczy twojej wypłaty co miesiąc, a nie raz w roku.",
  cap="Trzysta złotych miesięcznie")
I("Skąd ta kwota", "jedna dwunasta",
  "Kwota zmniejszająca podatek wynosi trzy tysiące sześćset złotych rocznie. "
  "Jedna dwunasta z tego to trzysta złotych, i tę część stosuje płatnik przy "
  "obliczaniu miesięcznej zaliczki.")
I("Ale nie sam z siebie", "trzeba oświadczenia",
  "Nie robi tego jednak z automatu. Musisz złożyć oświadczenie na formularzu "
  "PIT dwa, a bez niego zaliczka jest liczona bez pomniejszenia i wypłata na "
  "rękę jest niższa przez cały rok.")
I("Czy pieniądze przepadają", "nie przepadają",
  "Pieniądze nie znikają. Wracają w zwrocie po rozliczeniu rocznym, tylko "
  "rok później i bez odsetek.")
I("Można podzielić", "między płatników",
  "Przy kilku źródłach tę część można podzielić: po sto pięćdziesiąt złotych "
  "u dwóch płatników albo po sto u trzech. Łącznie w miesiącu i tak nie "
  "zejdzie poniżej trzystu złotych pomniejszenia.")
I("Drugi mechanizm", "od miesiąca przekroczenia",
  "Jest jeszcze druga rzecz, którą widać na pasku. Płatnik liczy zaliczkę "
  "stawką dwanaście procent dopóki twój dochód od początku roku mieści się "
  "pod progiem.")
I("A potem", "wyższa stawka od razu",
  "Od miesiąca, w którym próg zostaje przekroczony, zaliczka idzie już "
  "wyższą stawką. Dlatego jesienna wypłata potrafi być niższa od wiosennej "
  "przy tej samej umowie.")
I("To nie jest błąd kadr", "to jest skala",
  "To nie pomyłka w kadrach i nie kara za dobry rok. To ta sama skala, tylko "
  "widziana miesiąc po miesiącu, a nie raz na dwanaście miesięcy.")
I("Co z tym zrobić", "sprawdź w tym tygodniu",
  "Rzecz do sprawdzenia od razu: czy twój pracodawca ma od ciebie to "
  "oświadczenie, i w którym miesiącu przekraczasz próg.")

# ------------------------------------------------------------------- cap 8
T("Czego tu nie ma", "ulgi i odliczenia",
  "Teraz uczciwie o tym, czego ta prosta wersja nie obejmuje.",
  cap="Czego ten rachunek nie obejmuje")
I("Kto nie płaci nic", "kwota wolna",
  "Najpierw dół skali: jeśli podstawa nie przekracza kwoty wolnej, podatek "
  "wychodzi zero, bo kwota zmniejszająca zjada go w całości.")
I("Ulgi", "jest ich kilkanaście",
  "Dalej ulgi. Skala daje prawo do kilkunastu ulg i odliczeń: ulga na "
  "dziecko, ulga dla rodzin cztery plus, odliczenie składek i wiele innych. "
  "Każda zmienia podstawę albo sam podatek.")
I("IKZE", "też odliczasz",
  "Odliczyć można też wpłaty na Indywidualne Konto Zabezpieczenia "
  "Emerytalnego. Robiliśmy o tym osobny film.")
I("Składka zdrowotna", "to osobna pozycja",
  "Drugie zastrzeżenie: ten rachunek dotyczy wyłącznie podatku dochodowego. "
  "Składka zdrowotna jest osobną pozycją i nie wchodzi do tego wzoru, "
  "chociaż na twojej wypłacie widzisz obie naraz.")
I("Nie każdy jest na skali", "liniowy i ryczałt",
  "Ten film dotyczy skali podatkowej. Kto rozlicza się liniowo albo "
  "ryczałtem, ma inne zasady i tego progu u siebie nie zobaczy.")
I("Dlatego traktuj to", "jako punkt startu",
  "Potraktuj tę pracę domową jako punkt startu, a nie jako rozliczenie. Do "
  "rozliczenia jest księgowa albo doradca podatkowy.")

# ------------------------------------------------------------------- cap 9
T("Skąd te liczby", "trzy źródła",
  "Skąd wziąłem te liczby, bo to jest pytanie, które powinno paść zawsze.",
  cap="Skąd pochodzą liczby")
I("Pierwsze źródło", "portal rządowy",
  "Obowiązująca skala pochodzi z rządowego portalu informacyjnego dla "
  "przedsiębiorców. Tam stoi tabela, kwota zmniejszająca podatek i zasada "
  "wyższej stawki od miesiąca przekroczenia progu.")
I("Drugie źródło", "Kancelaria Premiera",
  "Propozycja zmian pochodzi ze strony Kancelarii Prezesa Rady Ministrów, z "
  "opisu proponowanego pakietu podatkowego.")
I("Trzecie źródło", "Ministerstwo Finansów",
  "Zasady wspólnego rozliczenia i oświadczenia PIT dwa pochodzą z serwisu "
  "podatkowego Ministerstwa Finansów.")
I("Jak to sprawdzić samemu", "dwa hasła",
  "Możesz to sprawdzić bez mojego pośrednictwa. Wystarczą dwa hasła: skala "
  "podatkowa na portalu dla przedsiębiorców, i pakiet podatkowy na stronie "
  "Kancelarii Premiera.")
I("Prawo i projekt", "to nie to samo",
  "I jedna rzecz, o którą warto pytać przy każdym materiale o podatkach: czy "
  "to jest obowiązujące prawo, czy dopiero projekt. To rozróżnienie zmienia "
  "wszystko, a znika w nagłówkach.")
I("Czego nie użyłem", "kalkulatorów z sieci",
  "Nie użyłem żadnego kalkulatora ani portalu z poradami. Jeśli liczba nie "
  "stoi w źródle urzędowym, nie wchodzi do tego filmu. Przy podatku pomyłka "
  "nie jest ciekawostką.")

# ------------------------------------------------------------------ cap 10
T("Co zrobić dziś", "cztery rzeczy i podsumowanie",
  "Cztery rzeczy, które możesz zrobić dziś wieczorem, każda na jednej "
  "kartce.",
  cap="Co zrobić dziś wieczorem")
I("Pierwsza", "policz swoją podstawę",
  "Policz swoją roczną podstawę: miesięczne brutto razy dwanaście, minus "
  "zapłacone składki społeczne.")
I("Druga", "zapisz odległość od progu",
  "Zapisz, ile złotych dzieli cię od stu dwudziestu tysięcy. To liczba, "
  "która mówi, czy próg w ogóle cię dotyczy.")
I("Trzecia", "sprawdź oświadczenie",
  "Sprawdź, czy twój pracodawca ma od ciebie oświadczenie PIT dwa. To "
  "pytanie na jedno zdanie do działu kadr.")
L("Czwarta", ["Ile jestem od progu dziś",
              "Ile byłbym po zmianie",
              "Ile z podwyżki zostaje mi w kieszeni"],
  "I zapisz trzy zdania: gdzie jestem dziś, gdzie byłbym po zmianie, i ile z "
  "kolejnej podwyżki naprawdę zostaje.")
I("Po co to ostatnie", "bo podwyżka to decyzja",
  "To ostatnie zdanie jest najważniejsze, bo podwyżka albo dodatkowe "
  "zlecenie to decyzja, a decyzję podejmuje się na liczbach.")
I("Podsumowanie", "dwa zdania",
  "Dziś próg to sto dwadzieścia tysięcy rocznej podstawy, a wyższa stawka "
  "dotyczy wyłącznie nadwyżki. Propozycja trzech progów to projekt, a nie "
  "prawo, i wracamy do tematu, kiedy będzie ustawa.")
C("Kolejny Poziom", "policz swoją odległość",
  "Zrób dziś jedną rzecz: policz, ile złotych dzieli cię od progu, i zapisz "
  "tę liczbę. Tutaj bierzemy jedną liczbę z twojego życia i zamieniamy ją w "
  "działanie, które robisz sam. Jeśli tego szukasz, zasubskrybuj.")


# -------------------------------------------------------------------- short
#
# O short TAMBEM entrega a conta (aprendizado 482): as tres faixas e o
# mnozenie, em menos de quarenta segundos.
SHORT = [
    {"layout": "titulo", "kicker": "Sto dwadzieścia tysięcy",
     "sub": "próg, którego nie widać",
     "nar": "Sto dwadzieścia tysięcy złotych rocznie. To liczba, która dzieli "
            "twoją pensję na dwie części.", "sem_cap": True},
    {"layout": "item", "kicker": "Poniżej", "preco": "dwanaście procent",
     "nar": "Poniżej płacisz dwanaście procent minus trzy tysiące sześćset.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Powyżej", "preco": "trzydzieści dwa",
     "nar": "Powyżej trzydzieści dwa procent, ale tylko od nadwyżki, nigdy od "
            "całości.", "sem_cap": True},
    {"layout": "item", "kicker": "Policz teraz", "preco": "brutto razy 12",
     "nar": "Pomnóż brutto przez dwanaście, odejmij składki i porównaj ze "
            "stem dwudziestoma tysiącami.", "sem_cap": True},
    {"layout": "cta", "kicker": "Kolejny Poziom", "sub": "twoja odległość",
     "nar": "Zapisz, ile złotych dzieli cię od progu. Tu każda liczba staje "
            "się działaniem, które robisz sam.", "sem_cap": True},
]

COPY = """# Próg podatkowy: 120 000 zł i propozycja trzech stawek

## TITULO
Próg Podatkowy 120 000 zł: Gdzie Jesteś na Skali i Co Zmienia Propozycja na 2027

## DESCRICAO
Jest jedna liczba, która dzieli twoją roczną pensję na dwie części opodatkowane zupełnie inaczej: 120 000 zł podstawy opodatkowania. Poniżej płacisz 12%, powyżej 32% — ale wyłącznie od nadwyżki, nigdy od całości. Podaję tę liczbę od razu, razem z metodą, która pozwala sprawdzić, po której stronie progu jesteś. Reszta to przykłady i zastrzeżenia.

OBOWIĄZUJĄCA SKALA (źródło: rządowy portal informacyjny)

Kwota wolna od podatku wynosi 30 000 zł, i stąd bierze się kwota zmniejszająca podatek: 30 000 × 12% = 3 600 zł. Do 120 000 zł podstawy podatek wynosi 12% minus 3 600 zł. Powyżej 120 000 zł: 10 800 zł + 32% nadwyżki ponad 120 000 zł.

JAK SPRAWDZIĆ, GDZIE JESTEŚ (trzy kroki)

1) Miesięczne brutto × 12 = roczny przychód. 2) Odejmij zapłacone składki na ubezpieczenie społeczne — zostaje podstawa opodatkowania. 3) Porównaj podstawę ze 120 000 zł.

Konkret: przy średniej pensji 9 233 zł miesięcznie roczny przychód to 110 796 zł — poniżej progu, ale niewiele. Od średniej krajowej do progu brakuje mniej niż 10 000 zł rocznie, czyli mniej więcej jedna podwyżka. Dlatego to nie jest temat dla bogatych; to temat dla osoby, która właśnie dostała podwyżkę.

PROPOZYCJA ZMIAN OD 2027 (źródło: Kancelaria Prezesa Rady Ministrów)

Propozycja zakłada trzy progi zamiast dwóch: I próg podniesiony do 130 000 zł ze stawką 12%; nowa stawka 24% od 130 000 zł do 150 000 zł; stawka 32% dopiero powyżej 150 000 zł. Według rządu skorzystałoby ponad 3,5 mln podatników, przede wszystkim pracowników, a zyskujący najwięcej zaoszczędziliby rocznie nawet 3 600 zł. Odsetek płacących 32% spadłby do 7,2% zamiast przewidywanych 14%.

TO JEST PROPOZYCJA, NIE USTAWA. Mówię to w filmie i powtarzam tutaj: opisane zmiany to zapowiedź i projekt, nie obowiązujące prawo. Liczby na 2026 rok są prawem; liczby na 2027 rok są propozycją.

DLACZEGO ODSETEK ROSŁ: progi stały w miejscu, a pensje nominalnie rosły, więc coraz więcej osób wpadało do wyższej stawki bez żadnej zmiany w ustawie. Drugi próg wynosił 85 528 zł od 2009 r. do końca 2021 r. — trzynaście lat bez ruchu — i dopiero potem podniesiono go do 120 000 zł. Podniesienie progu jest odwróceniem tego mechanizmu, a nie prezentem.

DWOJE LUDZI, JEDEN PRÓG (wspólne rozliczenie z małżonkiem)

Przy wspólnym rozliczeniu podatek ustala się w podwójnej wysokości podatku obliczonego od połowy łącznych dochodów małżonków. W praktyce dla pary próg działa tak, jakby był dwa razy wyższy: przy łącznej podstawie do 240 000 zł całość mieści się w pierwszej stawce. Efekt jest największy, gdy dochody bardzo się różnią. Warunek: małżeństwo i wspólność majątkowa przez cały rok podatkowy, z wyłączeniami dla niektórych form opodatkowania. To jedyna rzecz z tego materiału, która przenosi cię na drugą stronę progu bez zmiany pensji.

300 ZŁ MIESIĘCZNIE I OŚWIADCZENIE PIT-2

Kwota zmniejszająca podatek to 3 600 zł rocznie, a 1/12 z tego to 300 zł miesięcznie. Tę część stosuje płatnik przy obliczaniu zaliczki — ale nie z automatu: trzeba złożyć oświadczenie PIT-2. Bez niego zaliczka jest liczona bez pomniejszenia, a wypłata na rękę jest niższa przez cały rok (pieniądze wracają dopiero w zwrocie po rozliczeniu rocznym). Przy kilku źródłach 300 zł można podzielić: po 150 zł u dwóch płatników albo po 100 zł u trzech, ale łącznie w miesiącu nigdy więcej niż 300 zł.

DRUGI MECHANIZM WIDOCZNY NA PASKU: płatnik liczy zaliczkę stawką 12% w miesiącach, w których dochód od początku roku nie przekracza 120 000 zł, a stawką 32% od miesiąca, w którym ten limit zostaje przekroczony. Dlatego jesienna wypłata bywa niższa od wiosennej przy tej samej umowie. To nie pomyłka kadr — to ta sama skala, widziana miesiąc po miesiącu.

CZEGO TEN RACHUNEK NIE OBEJMUJE: przy podstawie do kwoty wolnej podatek wychodzi 0 zł. Rachunek dotyczy wyłącznie podatku dochodowego — składka zdrowotna to osobna pozycja i nie wchodzi do wzoru. Dotyczy też wyłącznie skali: kto rozlicza się liniowo albo ryczałtem, tego progu u siebie nie zobaczy. Poza tym skala daje prawo do kilkunastu ulg i odliczeń (ulga na dziecko, ulga dla rodzin 4+, odliczenie składek społecznych, wpłaty na IKZE i inne). Każda z nich zmienia podstawę albo sam podatek, więc realny wynik bywa inny niż z gołego wzoru. Potraktuj tę pracę domową jako punkt startu, nie jako rozliczenie — do rozliczenia jest księgowa albo doradca podatkowy. To nie jest porada podatkowa ani prawna.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Policz swoją roczną podstawę i napisz w komentarzu jedną liczbę: ile złotych dzieli cię od 120 000 zł. Nie pensję — samą odległość. Najbardziej interesuje mnie, ilu z was jest w zasięgu jednej podwyżki od progu, bo to jest dokładnie ta grupa, o której nikt nie mówi.

## HASHTAGS
#PodatkiPL #PrógPodatkowy #KolejnyPoziom

## TAGS
prog podatkowy, skala podatkowa, pit 2026, 120000 zl, kwota wolna od podatku, kwota zmniejszajaca podatek, 32 procent podatku, druga stawka pit, podatek dochodowy, reforma podatkowa 2027, stawka 24 procent, srednia krajowa, podwyzka a podatek, finanse osobiste, rozliczenie roczne

## CONFIGURACOES DO STUDIO
- Idioma: Polones (pl) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Polonia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Os numeros vem de TRES fontes institucionais que se confirmam. (1) A ESCALA EM VIGOR, do portal oficial do governo polones para empreendedores: kwota wolna 30.000 zl, kwota zmniejszajaca podatek 3.600 zl (30.000 x 12%), ate 120.000 zl o imposto e 12% menos 3.600 zl, e acima de 120.000 zl e 10.800 zl mais 32% do excedente. (2) A PROPOSTA PARA 2027, da pagina da Kancelaria Prezesa Rady Ministrow: primeiro degrau elevado a 130.000 zl com 12%, nova faixa intermediaria de 24% entre 130.000 e 150.000 zl, e 32% apenas acima de 150.000 zl; mais de 3,5 milhoes de contribuintes beneficiados, sobretudo empregados; economia anual de ate 3.600 zl para quem mais ganha; e queda da fatia que paga 32% de 14% para 7,2%. (3) A MECANICA DA SKALA, do serviço de impostos do Ministerio das Financas (podatki.gov.pl e gov.pl/web/finanse) e do mesmo portal biznes.gov.pl: no rozliczenie wspolne o imposto e o DOBRO do imposto calculado sobre METADE da renda somada do casal, o que faz o prog do casal se comportar como 240.000 zl; a kwota zmniejszajaca chega ao contracheque como 300 zl por mes (1/12 de 3.600), aplicados pelo platnik SO se o oswiadczenie PIT-2 tiver sido entregue, divisiveis em 150+150 ou 100x3 e nunca somando mais de 300 no mes; e o platnik usa 12% enquanto a renda acumulada do ano fica sob o prog, passando a 32% A PARTIR DO MES em que ele e ultrapassado. O HISTORICO DO PROG — 85.528 zl de 2009 ate o fim de 2021 e 120.000 zl a partir de 2022 — vem das paginas do Ministerio das Financas sobre as aliquotas de anos anteriores. O TETO DE 3.600 zl FOI DERIVADO, nao copiado: a 150.000 zl a escala atual cobra 20.400 zl e a proposta cobra 16.800 zl, diferenca de 3.600 zl exatos, e acima de 150.000 as duas correm na mesma aliquota, entao a diferenca congela ali. Duas rotas independentes no mesmo numero. A DISTINCAO E DITA NO PROPRIO VIDEO: a escala de 2026 e lei, a de 2027 e proposta e projeto, e nao foi tratada como certa. A ancora dos 9.233 zl mensais (110.796 zl anuais) vem da media salarial que este mesmo canal ja publicou. NAO foi usado nenhum calculador ou portal de dicas: numero que nao esta em fonte oficial nao entrou. O video nao cobre ulgas e odliczenia, que mudam o resultado caso a caso, e nao e aconselhamento fiscal ou juridico.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/kolejny-poziom-011.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-011",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#14213D", "c1": "#FCA311", "c2": "#E5E5E5",
               "bg": "#F7F5F0"},
    "thumb": {"l1": "120 000 zł", "l2": "gdzie jesteś"},
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
    grava(SPEC, "fabrica/specs/kolejny-poziom-011.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
