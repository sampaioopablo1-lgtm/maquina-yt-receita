#!/usr/bin/env python3
"""Monta a spec kolejny-poziom-009.

CANAL. Veredito `liberado` — o unico da frota. Short mediana 39,76 v/d (topo
201,69), longo 3,30 v/d, 3.871 views no acervo. `liberado` autoriza a faixa
inteira de 12 a 15 min. Escalonamento NAO se aplica: retencao medida do longo e
25,7% (185 s assistidos), abaixo dos 40% que a rotina exige, e a mediana do
canal esta abaixo da mediana do nicho (88,3 v/d).

EIXO. Os oito titulos ja publicados cobrem ZUS, IKE/IKZE, kredyt hipoteczny,
obligacje, podatek Belki, placa minimalna e zdolnosc kredytowa. UBEZPIECZENIA
nunca foi usado, e o `pautas_banco` tem outlier nesse eixo (`ulgi-podatkowe-oc`,
1.386,5 v/d).

FORMATO. O que performa aqui nao e "explicacao": e AVISO ANTES DE AGIR. O
outlier do Marcin Iwuc — "Obejrzyj to, zanim zaplacisz kolejna rate kredytu
hipotecznego" — mede 1.986,2 v/d, e o topo da lista inteira e
"pergunta + aviso de custo dobrado" com 6.564,6. A ESTRUTURA copiada e essa:
"veja isto ANTES de fazer X". O assunto e outro.

A PAUTA — e ela nasce de uma contradicao entre duas fontes oficiais.

  A imprensa de agosto/2026 esta publicando "OC mais barato em dois anos".
  Os comparadores cotam cerca de seiscentos e cinquenta zlotys para quem
  compra agora. E os dados institucionais dizem o contrario do que a manchete
  sugere:

  PIU (Polska Izba Ubezpieczen), relatorio do I trimestre de 2026,
  publicado em meados de junho de 2026:
    media da apolice OC ......... 551 zl   (-4 zl, -0,7% em doze meses)
    media do sinistro OC ........ 11,6 mil zl  (+6,4%)
    apolices OC ................. 8,8 mln  (+4%, mais 320 mil)
    apolices AC ................. 2,3 mln  (+6%)
    mercado inteiro ............. 23,9 mld zl (+7%)

  KNF (Komisja Nadzoru Finansowego), mesmos tres meses, grupo 10 —
  o OC obrigatorio de veiculos:
    resultado tecnico ........... -18,92 mln zl
    um ano antes ................ +43,2 mln zl
    premio arrecadado ........... 4,8 mld zl (+3%)
    indenizacoes pagas .......... +9%

  Duas fontes independentes, as duas oficiais, e elas concordam no diagnostico:
  o preco caiu 0,7% enquanto o sinistro subiu 6,4% e a linha virou de lucro
  para prejuizo. Isso nao se sustenta.

A TESE, que e o video inteiro: "mais barato em dois anos" nao e presente, e o
fim do ciclo. Quem trata a manchete como oportunidade de esperar mais um pouco
esta lendo o numero certo na direcao errada.

O QUE O VIDEO NAO FAZ: nao promete que o preco vai subir X por cento em tal
mes. Ninguem sabe isso, e a diferenca entre "a conta nao fecha" e "vai subir
vinte por cento em outubro" e a diferenca entre analise e chute.

ACENTOS. O canal acentua 6,9% das letras e duas specs dele foram ao ar em ASCII
(kolejny-poziom-003 e -004, ambas no inventario). Esta escreve polones com os
diacriticos todos — o portao de ortografia cobra, e o TTS le errado sem eles.
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


# ------------------------------------------------------------------ cap 1
T("Najtańsze od dwóch lat", "i to jest ostrzeżenie",
  "Twoje OC jest dziś najtańsze od dwóch lat. Brzmi jak dobra wiadomość, "
  "i właśnie dlatego warto obejrzeć to, zanim odnowisz polisę.",
  cap="Najtańsze od dwóch lat — i dlaczego to ostrzeżenie")
I("Co mówią nagłówki", "spadek ceny",
  "Nagłówki z tego lata mówią jedno: ceny OC spadły. To prawda. Sprawdziłem "
  "liczby i one się zgadzają.")
I("Co mówi druga liczba", "szkoda w górę",
  "Tylko że obok ceny stoi druga liczba, z tego samego raportu. Średnia "
  "szkoda z OC wzrosła. I to ona decyduje o tym, co będzie dalej.")
I("Kto to policzył", "PIU i KNF",
  "Dane są z dwóch niezależnych źródeł. Polska Izba Ubezpieczeń i Komisja "
  "Nadzoru Finansowego. Obie instytucje, oba raporty za pierwszy kwartał "
  "tego roku.")
B("Dwie strzałki", ["Składka", "Szkoda"], [12, 100],
  "I te dwie strzałki idą w przeciwne strony. Składka lekko w dół, szkoda "
  "wyraźnie w górę. Tak wygląda rachunek, który się nie spina.")
T("Czym to NIE jest", "nie przewiduję podwyżki",
  "Zanim pójdziemy dalej, jedna rzecz. Nie powiem ci, że polisa zdrożeje o "
  "konkretny procent w konkretnym miesiącu. Nikt tego nie wie.")
I("Co powiem", "pokażę rachunek",
  "Powiem coś węższego i sprawdzalnego. Pokażę rachunek ubezpieczycieli i "
  "to, że w tej chwili on nie domyka się. Wniosek wyciągniesz sam.")
L("Po kolei", ["Ile naprawdę kosztuje średnie OC",
                           "O ile urosła średnia szkoda",
                           "Rachunek, który się nie spina",
                           "Dlaczego cena jeszcze nie poszła w górę",
                           "Co zrobić przed odnowieniem"],
  "Po kolei. Ile kosztuje średnie OC, o ile urosła szkoda, dlaczego rachunek "
  "się nie spina, czemu cena jeszcze nie poszła w górę i co z tym zrobić "
  "przed odnowieniem.")
I("Jedno zastrzeżenie", "średnia to nie twoja cena",
  "I jedno zastrzeżenie na cały film. Średnia rynkowa to nie jest twoja "
  "cena. Twoja zależy od wieku, miasta, auta i historii szkód.")
I("Po co więc średnia", "pokazuje kierunek",
  "Średnia służy do czegoś innego. Ona nie mówi, ile zapłacisz. Ona pokazuje, "
  "w którą stronę idzie cały rynek — a rynek prędzej czy później dogania "
  "twoją polisę.")
I("Zaczynamy od ceny", "od tego, co widzisz",
  "Zaczynamy od tego, co widzisz jako pierwsze: od ceny.")

# ------------------------------------------------------------------ cap 2
T("Pięćset pięćdziesiąt jeden", "średnia składka OC",
  "Średnia składka za OC komunikacyjne wyniosła pięćset pięćdziesiąt jeden "
  "złotych. To dane Polskiej Izby Ubezpieczeń za pierwszy kwartał tego roku.",
  cap="Ile naprawdę kosztuje średnie OC")
I("O ile mniej", "cztery złote",
  "Rok wcześniej było o cztery złote więcej. Spadek o siedem dziesiątych "
  "procenta. Realnie: prawie nic.")
I("Dlaczego mówią o dwóch latach", "poziom sprzed dwóch lat",
  "Skąd więc nagłówek o najtańszej polisie od dwóch lat? Stąd, że po serii "
  "podwyżek średnia wróciła mniej więcej tam, gdzie była dwa lata temu.")
I("A porównywarki", "sześćset pięćdziesiąt",
  "Jeśli sprawdzasz cenę w porównywarce, zobaczysz raczej około sześciuset "
  "pięćdziesięciu złotych. To nie jest sprzeczność, tylko inna liczba.")
I("Dlaczego się różnią", "portfel kontra oferta",
  "Izba liczy średnią ze wszystkich czynnych polis, także tych kupionych "
  "dawno i tanio. Porównywarka pokazuje ofertę na dziś, dla kierowcy, który "
  "kupuje teraz.")
B("Dwa różne pytania", ["Średnia z portfela", "Oferta na dziś"], [85, 100],
  "To są odpowiedzi na dwa różne pytania, i mylenie ich jest najczęstszym "
  "błędem w rozmowie o cenach polis.")
I("Która jest ważniejsza", "zależy po co",
  "Która się liczy? Do twojej decyzji — ta z porównywarki. Do zrozumienia, "
  "co się stanie z rynkiem — ta z Izby. Interesuje nas teraz ta druga.")
I("Ile jest tych polis", "osiem milionów osiemset tysięcy",
  "Warto wiedzieć, na czym liczona jest ta średnia. Na koniec kwartału "
  "czynnych polis OC było osiem milionów osiemset tysięcy. To nie jest "
  "badanie na próbce — to cały rynek policzony co do sztuki.")
I("I ich przybywa", "cztery procent więcej",
  "I jest ich coraz więcej: o cztery procent w skali roku, czyli o jakieś "
  "trzysta dwadzieścia tysięcy sztuk.")
I("Co to znaczy dla składki", "więcej klientów, ta sama cena",
  "Zapamiętaj to, bo wrócimy do tego w rozdziale o konkurencji. Klientów "
  "przybywa, a cena stoi. To nie jest przypadek.")
I("Teraz druga liczba", "ta z drugiej strony rachunku",
  "Cena to jedna strona rachunku. Teraz druga, i to ona jest tu ważniejsza:")

# ------------------------------------------------------------------ cap 3
T("Jedenaście tysięcy sześćset", "średnia szkoda",
  "Średnia szkoda wypłacana z OC komunikacyjnego to dziś jedenaście tysięcy "
  "sześćset złotych. Rok wcześniej była o sześć procent niższa.",
  cap="O ile urosła średnia szkoda")
I("Skala porównania", "dwadzieścia jeden razy składka",
  "Zestaw to ze składką. Jedna średnia szkoda kosztuje ubezpieczyciela mniej "
  "więcej tyle, ile dwadzieścia jeden średnich polis przynosi.")
I("Dlaczego szkody drożeją", "części i robocizna",
  "Powody nie są tajemnicze i żaden z nich nie jest chwilowy. Części drożeją, "
  "robocizna w warsztacie drożeje, a auta mają w sobie coraz więcej "
  "elektroniki. Te trzy rzeczy działają razem i wszystkie w tę samą stronę.")
I("Konkretny przykład", "zderzak z czujnikami",
  "Weź zderzak. Dekadę temu to był kawałek plastiku i godzina pracy. Dziś w "
  "tym samym zderzaku siedzą czujniki parkowania i radar, a po wymianie "
  "trzeba to jeszcze skalibrować na stanowisku. Ta sama stłuczka, zupełnie "
  "inny kosztorys.")
I("Drugi powód", "więcej zgłoszeń",
  "Do tego doszła druga rzecz: zgłoszeń jest po prostu więcej niż rok temu. "
  "I te dwie rzeczy się mnożą, a nie dodają. Więcej szkód razy droższa szkoda "
  "to podwójny ruch w tę samą stronę, i dlatego suma wypłat rośnie szybciej "
  "niż sam koszt naprawy.")
B("Wypłaty w górę", ["Rok temu", "Teraz"], [92, 100],
  "Efekt widać w wypłatach. Ubezpieczyciele wypłacili o dziewięć procent "
  "więcej niż w tym samym kwartale rok wcześniej.")
T("Zestaw trzy liczby", "i wszystko się wyjaśnia",
  "I teraz zestaw trzy liczby z tego samego kwartału, bo dopiero razem one "
  "coś znaczą.")
I("Pierwsza", "składka minus zero siedem",
  "Składka: minus siedem dziesiątych procenta.")
I("Druga", "szkoda plus sześć i cztery",
  "Średnia szkoda: plus sześć i cztery dziesiąte procenta.")
I("Trzecia", "wypłaty plus dziewięć",
  "Suma wypłat: plus dziewięć procent.")
I("Wniosek", "wpływy stoją, wydatki rosną",
  "Wpływy stoją w miejscu, wydatki rosną w dwóch wymiarach naraz. To nie jest "
  "opinia — to trzy liczby z raportów. Zobaczmy, ile to kosztuje:")

# ------------------------------------------------------------------ cap 4
T("Z zysku na stratę", "w dwanaście miesięcy",
  "Komisja Nadzoru Finansowego liczy to samo od strony wyniku. W grupie "
  "dziesiątej, czyli w obowiązkowym OC posiadaczy pojazdów, wynik techniczny "
  "zmienił znak.",
  cap="Rachunek, który się nie spina")
I("Rok temu", "czterdzieści trzy miliony zysku",
  "Rok temu ta linia dała czterdzieści trzy miliony dwieście tysięcy złotych "
  "zysku.")
I("Teraz", "prawie dziewiętnaście milionów straty",
  "W pierwszym kwartale tego roku dała osiemnaście milionów dziewięćset "
  "dwadzieścia tysięcy złotych straty.")
B("Zmiana znaku", ["Rok temu", "Teraz"], [100, -44],
  "To nie jest spadek zysku. To przejście na drugą stronę zera, i to w "
  "dwanaście miesięcy.")
I("Ile wpłynęło", "cztery miliardy osiemset milionów",
  "A przecież przypis składki wcale nie spadł. Wyniósł cztery miliardy "
  "osiemset milionów złotych, o trzy procent więcej niż rok temu.")
I("Czyli", "więcej wpływów, i strata",
  "Czyli wpłynęło więcej pieniędzy niż rok temu, a linia i tak wyszła na "
  "minus. Cała różnica siedzi po stronie kosztów.")
T("Co to jest wynik techniczny", "bez inwestycji",
  "Jedno wyjaśnienie, żeby ta liczba nie brzmiała groźniej niż jest.")
I("Definicja", "sama działalność ubezpieczeniowa",
  "Wynik techniczny to sam rachunek ubezpieczeniowy: składki minus szkody "
  "minus koszty. Nie obejmuje tego, co firma zarobi, inwestując pieniądze "
  "klientów.")
I("Dlaczego to ważne", "firma nie bankrutuje",
  "Ubezpieczyciel ze stratą techniczną nie bankrutuje — zwykle nadrabia to "
  "na inwestycjach. Ale to jest sygnał, że sama cena polis przestała "
  "pokrywać ryzyko.")
I("Jak firmy reagują", "podnoszą cenę",
  "A kiedy cena przestaje pokrywać ryzyko, firmy robią jedną z dwóch rzeczy: "
  "podnoszą składkę albo zaostrzają kryteria. Zwykle obie naraz, tylko w "
  "innym tempie — kryteria zmienia się z dnia na dzień, cennik wolniej.")
I("Skoro tak", "czemu jeszcze nie",
  "Skoro rachunek nie domyka się od kwartału, pojawia się oczywiste pytanie: "
  "dlaczego cena jeszcze nie poszła w górę?")

# ------------------------------------------------------------------ cap 5
T("Bo trwa walka o klienta", "i ona ma koniec",
  "Odpowiedź jest prosta i ma datę ważności. Trwa walka o udział w rynku, a "
  "w takiej walce nikt nie chce podnieść ceny pierwszy.",
  cap="Dlaczego cena jeszcze nie poszła w górę")
I("Dowód", "portfel rośnie",
  "Dowód jest w liczbie polis, o której mówiłem wcześniej. Portfel urósł o "
  "cztery procent — firmy nadal zdobywają klientów, nie tracą ich.")
I("Jak się zdobywa klienta", "ceną",
  "A klienta w OC zdobywa się prawie wyłącznie ceną, bo produkt jest z "
  "definicji taki sam. Zakres obowiązkowego OC ustala ustawa, nie firma.")
I("Rola porównywarek", "sortowanie po cenie",
  "Porównywarki tylko to wzmacniają. Kierowca sortuje po cenie i wybiera "
  "pierwszą pozycję z listy, więc podniesienie składki o kilkadziesiąt "
  "złotych oznacza wypadnięcie z pierwszego ekranu. A z drugiego ekranu "
  "praktycznie nikt nie kupuje.")
B("Ta sama polisa", ["Zakres OC", "Cena"], [100, 100],
  "Dlatego przy identycznym zakresie cała konkurencja przenosi się na jedno "
  "pole. I dlatego cena trzyma się nisko dłużej, niż wynikałoby z kosztów.")
T("Ale to nie jest wieczne", "co przerywa taki cykl",
  "Tyle że taki układ nigdy nie trwa długo, i wiadomo, co go zwykle "
  "przerywa.")
I("Pierwszy scenariusz", "ktoś podnosi pierwszy",
  "Pierwszy scenariusz: jedna duża firma podnosi stawki, przyjmuje na siebie "
  "utratę części klientów, a reszta rynku idzie za nią w kilka miesięcy.")
I("Drugi scenariusz", "cicha selekcja",
  "Drugi jest cichszy i dlatego groźniejszy. Cena z reklamy zostaje na "
  "miejscu, ale zaostrzają się kryteria. Młody kierowca, starsze auto albo "
  "jedna szkoda w historii — i nagle twoja konkretna oferta jest zupełnie "
  "inna niż ta, którą widziałeś w nagłówku. Statystyka rynkowa dalej "
  "wygląda spokojnie, bo średnia się nie rusza.")
I("Który jest bardziej prawdopodobny", "nie zgaduję",
  "Nie będę zgadywał, który przyjdzie pierwszy. To już byłoby wróżenie, a "
  "obiecałem trzymać się rachunku.")
I("Co jest pewne", "koszt nie cofnie się",
  "Pewne jest co innego, i to wystarczy. Koszt naprawy nie wróci do poziomu "
  "sprzed dwóch lat, bo części i robocizna nie tanieją, a elektroniki w "
  "autach nie ubywa. Skoro koszt zostaje na górze, cena prędzej czy później "
  "musi się z nim spotkać.")
I("Więc co robić", "korzystać z okna",
  "Z tego wynika coś praktycznego, i to jest właściwa część roboty:")

# ------------------------------------------------------------------ cap 6
T("Cztery rzeczy", "przed odnowieniem",
  "Cztery rzeczy do zrobienia przed odnowieniem polisy. Żadna z nich nie "
  "wymaga wiedzy ubezpieczeniowej, każda zajmuje kilkanaście minut.",
  cap="Co zrobić przed odnowieniem")
I("Pierwsza", "sprawdź datę końca polisy",
  "Po pierwsze: sprawdź, kiedy kończy się twoja polisa. Brzmi banalnie, a to "
  "jedyna data, która daje ci wybór — po niej wybór robi się za ciebie.")
I("Dlaczego to ważne", "automatyczne wznowienie",
  "Bo OC wznawia się samo, jeśli nie wypowiesz go na dzień przed końcem. "
  "Wznowione automatycznie jest zwykle droższe niż to samo OC kupione od "
  "nowa w tej samej firmie.")
I("Druga", "policz cenę teraz, nie w ostatnim tygodniu",
  "Po drugie: sprawdź ofertę już teraz, a nie w ostatnim tygodniu. Kalkulacja "
  "nic nie kosztuje i nie zobowiązuje, a daje ci punkt odniesienia.")
I("Co z tym punktem", "porównasz za rok",
  "Zapisz tę kwotę razem z datą, choćby w notatkach w telefonie. Za rok "
  "będziesz mieć własny pomiar zamiast wrażenia. To jest jedyny sposób, żeby "
  "wiedzieć, czy podwyżka dotknęła właśnie ciebie, czy tylko czytałeś o niej "
  "w nagłówkach.")
I("Trzecia", "sprawdź, za co płacisz",
  "Po trzecie: sprawdź, co masz w pakiecie poza obowiązkowym OC. Assistance, "
  "ochrona zniżek, ubezpieczenie szyb. Część z tego bywa dopisana "
  "automatycznie przy wznowieniu i zostaje na kolejne lata, bo nikt tego nie "
  "czyta drugi raz.")
I("Uwaga", "nie tnij w ciemno",
  "Ale nie tnij wszystkiego w ciemno. Assistance za kilkadziesiąt złotych "
  "przy jednej awarii zwraca się z nawiązką. Chodzi o to, żeby wiedzieć, za "
  "co płacisz, a nie żeby płacić jak najmniej.")
I("Czwarta", "sprawdź zniżki i przebieg",
  "Po czwarte: sprawdź dane, na podstawie których liczą ci cenę. Roczny "
  "przebieg, miejsce garażowania, kto jeszcze jeździ autem. Nieaktualne dane "
  "potrafią kosztować.")
T("Czego NIE robić", "jedna pułapka",
  "I jedna rzecz, której robić nie warto, choć kusi.")
I("Pułapka", "najtańsza oferta z listy",
  "Nie bierz automatycznie pierwszej pozycji z listy. W obowiązkowym OC "
  "zakres jest ustawowy i faktycznie identyczny, ale to jest jedyny element, "
  "który jest identyczny.")
I("Co się różni", "likwidacja szkody",
  "Różni się to, jak firma likwiduje szkodę. Ile czeka się na oględziny, czy "
  "dostaniesz auto zastępcze, czy kosztorys liczą po częściach oryginalnych, "
  "czy po zamiennikach. Tego nie widać w kolumnie z ceną, a widać dokładnie "
  "wtedy, kiedy polisa ma zadziałać.")
I("Przejdźmy do liczb", "twoich, nie średnich",
  "Zostaje ostatnia część, i jest najbardziej twoja: zamiana tego wszystkiego "
  "na własną tabelę.")

# ------------------------------------------------------------------ cap 7
T("Pięć wierszy", "i decyzja robi się sama",
  "Pięć wierszy w arkuszu. Każdy to liczba, którą albo już masz, albo "
  "zdobędziesz w kwadrans.",
  cap="Twoja własna tabela")
I("Wiersz pierwszy", "składka z zeszłego roku",
  "Wiersz pierwszy: ile zapłaciłeś za OC rok temu. Znajdziesz to na polisie "
  "albo na wyciągu z konta.")
I("Wiersz drugi", "najlepsza oferta na dziś",
  "Wiersz drugi: najlepsza oferta, jaką dostajesz dzisiaj, po sprawdzeniu w "
  "co najmniej trzech miejscach.")
I("Wiersz trzeci", "oferta na wznowienie",
  "Wiersz trzeci: kwota, którą proponuje ci twoja obecna firma na wznowienie. "
  "To jest ten numer, który najczęściej wygrywa przez bezwładność.")
I("Wiersz czwarty", "różnica w złotych",
  "Wiersz czwarty: różnica między drugim a trzecim. To są pieniądze, które "
  "kosztuje cię nierobienie niczego.")
I("Wiersz piąty", "data następnego końca polisy",
  "Wiersz piąty: data, kiedy kończy się nowa polisa, minus trzydzieści dni. "
  "Wpisz to od razu w kalendarz.")
B("Co pokaże tabela", ["Wznowienie", "Najlepsza oferta"], [100, 78],
  "U większości kierowców czwarty wiersz wychodzi kilkadziesiąt albo "
  "kilkaset złotych. Za kwadrans pracy raz w roku.")
I("Jak to czytać za rok", "porównanie z sobą",
  "A rok później ta sama tabela robi coś, czego żaden raport rynkowy nie "
  "zrobi: porównuje ciebie z tobą sprzed roku, a nie ze średnią całego "
  "kraju. Średnia opisuje osiem milionów kierowców, z których żaden nie "
  "jeździ twoim autem.")
I("Wracając do początku", "najtańsze od dwóch lat",
  "I wtedy zdanie z początku filmu ustawia się na swoim miejscu. "
  "Najtańsze od dwóch lat opisuje przeszłość, nie obietnicę.")
I("Jedno zdanie", "jeśli masz zapamiętać jedno",
  "Jeśli masz zapamiętać jedno zdanie, niech to będzie to: składka spadła o "
  "siedem dziesiątych procenta, a szkoda urosła o sześć i cztery dziesiąte. "
  "Reszta wynika z tych dwóch liczb.")
C("Kolejny Poziom", "konkretne liczby, co tydzień",
  "Sprawdź dziś datę końca swojej polisy i zapisz ją w kalendarzu. To "
  "zajmuje minutę. A jeśli ten film oszczędził ci pieniądze — zostaw "
  "subskrypcję.")

# ------------------------------------------------------------------ short
#
# Entrega sozinho: as duas liquidas do lado oposto, o resultado que virou de
# sinal e a acao concreta. O longo e continuacao opcional, nunca condicao.
SHORT = [
    {"layout": "titulo", "kicker": "OC najtańsze od 2 lat",
     "sub": "i to jest ostrzeżenie",
     "nar": "OC jest najtańsze od dwóch lat. To nie prezent, tylko koniec "
            "cyklu.", "sem_cap": True},
    {"layout": "item", "kicker": "Składka", "preco": "551 zł, minus 0,7%",
     "nar": "Średnia składka to pięćset pięćdziesiąt jeden złotych, o siedem "
            "dziesiątych procenta mniej niż rok temu.", "sem_cap": True},
    {"layout": "item", "kicker": "Szkoda", "preco": "11 600 zł, plus 6,4%",
     "nar": "A średnia szkoda urosła do jedenastu tysięcy sześciuset złotych. "
            "Dane Izby Ubezpieczeń.", "sem_cap": True},
    {"layout": "item", "kicker": "Wynik", "preco": "z zysku na stratę",
     "nar": "Efekt według Komisji Nadzoru: obowiązkowe OC przeszło z zysku na "
            "stratę w dwanaście miesięcy.", "sem_cap": True},
    {"layout": "item", "kicker": "Co zrobić", "preco": "sprawdź datę",
     "nar": "Sprawdź dziś, kiedy kończy się twoja polisa. OC wznawia się samo "
            "i wznowione bywa droższe.", "sem_cap": True},
    {"layout": "cta", "kicker": "Kolejny Poziom", "sub": "zanim odnowisz",
     "nar": "Policz ofertę teraz i zapisz kwotę z datą.", "sem_cap": True},
]


def _copy_existente():
    """Le a copy do .json ao lado, se ele ja existir. A copy real nasce depois
    do render, com os tempos de capitulo medidos; reconstruir daqui a apagaria.
    """
    import os
    alvo = "fabrica/specs/kolejny-poziom-009.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


COPY = """# OC najtańsze od dwóch lat — i dlaczego to jest ostrzeżenie

## TITULO
OC najtańsze od dwóch lat. Zobacz to, zanim odnowisz polisę

## DESCRICAO
Twoje OC jest dziś najtańsze od dwóch lat. Brzmi jak dobra wiadomość — i właśnie dlatego warto obejrzeć ten film, zanim odnowisz polisę.

Dane pochodzą z dwóch niezależnych źródeł, obu oficjalnych, za ten sam pierwszy kwartał 2026 roku.

Polska Izba Ubezpieczeń: średnia składka za OC komunikacyjne wyniosła 551 zł, czyli o 4 zł (0,7%) mniej niż rok wcześniej. W tym samym czasie średnia szkoda wypłacana z OC wzrosła o 6,4% i wyniosła 11,6 tys. zł. Czynnych polis OC było 8,8 mln — o 4% (320 tys.) więcej niż rok wcześniej. Cały rynek ubezpieczeń urósł o 7%, do 23,9 mld zł.

Komisja Nadzoru Finansowego, ta sama grupa 10 (obowiązkowe OC posiadaczy pojazdów): wynik techniczny to strata 18,92 mln zł, wobec 43,2 mln zł ZYSKU rok wcześniej. Przypis składki wzrósł o 3%, do 4,8 mld zł, a wypłacone odszkodowania o 9%.

Dwa raporty, dwie instytucje, jeden wniosek: cena spadła o 0,7%, a koszt szkody urósł o 6,4%. To się nie spina.

O CZYM JEST TEN FILM:

Dlaczego średnia z raportu (551 zł) różni się od tego, co widzisz w porównywarce (ok. 650 zł) — i która z tych liczb odpowiada na TWOJE pytanie. Izba liczy średnią ze wszystkich czynnych polis, także kupionych dawno i tanio; porównywarka pokazuje ofertę na dziś.

Dlaczego szkody drożeją i dlaczego to nie cofnie się: części, robocizna i elektronika w aucie. Zderzak sprzed dekady był kawałkiem plastiku; dziś siedzą w nim czujniki i radar, które po wymianie trzeba skalibrować.

Co znaczy „wynik techniczny" i dlaczego strata w tej pozycji NIE oznacza, że ubezpieczyciel bankrutuje — ale oznacza, że sama cena polis przestała pokrywać ryzyko.

Dlaczego cena mimo to jeszcze nie poszła w górę: trwa walka o udział w rynku, a przy ustawowo identycznym zakresie OC konkurencja przenosi się wyłącznie na cenę. Portfel urósł o 4%, więc firmy nadal zdobywają klientów — i nikt nie chce podnieść stawek pierwszy.

Dwa scenariusze wyjścia z tego układu: głośny (jedna duża firma podnosi stawki, reszta idzie za nią) i cichy, groźniejszy (cena z reklamy zostaje, ale zaostrzają się kryteria — młody kierowca, starsze auto, szkoda w historii).

Cztery rzeczy do zrobienia przed odnowieniem: sprawdzić datę końca polisy (OC wznawia się samo, a wznowione bywa droższe), policzyć ofertę już teraz i zapisać kwotę z datą, sprawdzić co siedzi w pakiecie, i zaktualizować dane, na podstawie których liczą cenę.

Tabela pięciu wierszy, która zamienia to wszystko w twoją własną decyzję — i która za rok porówna CIEBIE z TOBĄ, a nie ze średnią kraju.

CZEGO W TYM FILMIE NIE MA: nie przewiduję, że polisa zdrożeje o X procent w konkretnym miesiącu. Nikt tego nie wie. Pokazuję rachunek i to, że w tej chwili on się nie domyka.

JEŚLI ZROBISZ TYLKO JEDNĄ RZECZ: sprawdź dziś datę końca swojej polisy i wpisz do kalendarza przypomnienie 30 dni wcześniej.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Dwa pytania do was, bo odpowiedzi różnią się dużo bardziej niż średnia sugeruje: ile zapłaciliście za OC w tym roku, i o ile to więcej lub mniej niż rok temu? Zbieram te liczby do kolejnego materiału — interesuje mnie zwłaszcza to, czy podwyżka trafia równo, czy tylko w niektóre grupy kierowców.

## HASHTAGS
#OC #Ubezpieczenia #KolejnyPoziom

## TAGS
oc komunikacyjne, ubezpieczenie samochodu, cena oc 2026, polisa oc, ubezpieczenia, finanse osobiste, oszczedzanie, porownywarka oc, skladka oc, szkoda komunikacyjna, knf, piu, wznowienie polisy, ac autocasco, kierowcy

## CONFIGURACOES DO STUDIO
- Idioma: Polski (pl) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Polonia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao > 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Wszystkie liczby pochodzą z raportów za I kwartał 2026 r. Średnia składka OC (551 zł, −4 zł / −0,7% r/r), średnia szkoda z OC (11,6 tys. zł, +6,4%), liczba polis OC (8,8 mln, +4%) i AC (2,3 mln, +6%) oraz wielkość rynku (23,9 mld zł, +7%) — dane Polskiej Izby Ubezpieczeń, raport opublikowany w połowie czerwca 2026 r. Wynik techniczny grupy 10 (obowiązkowe OC posiadaczy pojazdów mechanicznych): strata 18,92 mln zł wobec 43,2 mln zł zysku rok wcześniej, przypis 4,8 mld zł (+3%), odszkodowania +9% — dane Komisji Nadzoru Finansowego za ten sam okres. Kwota ok. 650 zł to typowa oferta z porównywarek dla kierowcy kupującego polisę teraz i nie jest tą samą wielkością co średnia z portfela — różnicę tłumaczę w filmie. Średnia rynkowa nie jest twoją ceną: twoja zależy od wieku, miejsca zamieszkania, auta i historii szkód. Film nie przewiduje wysokości ani terminu przyszłych podwyżek — pokazuje rachunek, który dziś się nie domyka. To materiał edukacyjny o finansach osobistych, nie jest to doradztwo ubezpieczeniowe ani rekomendacja konkretnej oferty.
"""


SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-009",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#12233A", "c1": "#1F6FB2", "c2": "#E8A33D",
               "bg": "#F2F6FA"},
    "thumb": {"l1": "551 zł", "l2": "szkoda 11 600"},
    "longo": CENAS,
    "short": SHORT,
    "copy": _copy_existente(),
}

if __name__ == "__main__":
    p = "fabrica/specs/kolejny-poziom-009.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=1)
        f.write("\n")
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ensaio import duracao_estimada, duracao_estimada_short
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
