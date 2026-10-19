# -*- coding: utf-8 -*-
"""Monta a spec do `kolejny-poziom-020` — o SEGUNDO longo com trilho, no canal
que o contador escolheu (minimo absoluto, 7 pecas na janela de 24 h).

Classe de conteudo: PROCEDIMENTO. Nenhum numero do mundo entra — todos os
numeros sao do PROPRIO espectador (o pasek wyplaty dele, as horas dele, os
rachunki dele). Logo a trava de duas fontes institucionais (600) nao se aplica.
"""
import json
import os
import sys

RAIZ = "/home/user/maquina-yt-receita"
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

L = []


def cena(**k):
    L.append(k)


# ---------------------------------------------------------------- CAPITULO 1
cena(layout="titulo", kicker="Bez jednostki", sub="dlatego cena nic nie mówi",
     cap="Cena bez jednostki",
     nar="Widzisz kwotę na rachunku i wiesz, ile to złotych. Nie wiesz, ile to dla ciebie znaczy, bo brakuje drugiej liczby.")
cena(layout="item", kicker="Nie pytamy ile kosztuje", preco="pytamy ile zajmuje",
     nar="To nagranie nie pyta, ile coś kosztuje w złotych. Pyta, ile twojego czasu trzeba przepracować, żeby to opłacić.", sem_cap=True)
cena(layout="item", kicker="Ta sama kwota", preco="dwa różne życia",
     nar="Ta sama kwota u dwóch osób nie znaczy tego samego. Dla jednej to pół dnia pracy, dla drugiej prawie trzy dni.", sem_cap=True)
cena(layout="erro", codigo="#DZIEL/0!", causa="Dzielenie bez mianownika",
     saida="Policz najpierw swoją stawkę netto",
     nar="Jeśli wpiszesz kwotę u góry, a dół zostawisz pusty, działanie nie wychodzi wcale. Ekran nie pokazuje złej liczby, pokazuje żadnej.", sem_cap=True)
cena(layout="item", kicker="Nikt tego nie liczy", preco="ani sprzedawca",
     nar="Sklep podaje cenę w złotych, bo złote sprzedaje. Na godziny nikt ci tego nie przelicza, bo mianownik jest twój własny.", sem_cap=True)
cena(layout="numero", valor="÷", legenda="liczba, której brakuje",
     nota="bez niej kwota jest tylko kwotą", escala=1.0,
     nar="Całe nagranie jest o tym jednym znaku. Kreska dzielenia, i kwota zamienia się w czas.", sem_cap=True)
cena(layout="item", kicker="Czas, nie pieniądze", preco="to naprawdę płacisz",
     nar="Za każdą rzecz płacisz czasem, który trzeba było przepracować. Złote są tylko pokwitowaniem tego czasu.", sem_cap=True)
cena(layout="item", kicker="Dane już masz", preco="i są twoje",
     nar="Nie potrzebujesz niczego, czego nie masz w domu. Jeden pasek wypłaty z jednej strony i twoje godziny z drugiej.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 2
cena(layout="titulo", kicker="Co to netto", sub="i czym ono nie jest",
     cap="Co to znaczy netto za godzinę",
     nar="Mianownik to nie pensja i nie stawka z umowy. To ile zostaje ci w kieszeni za jedną godzinę, którą faktycznie oddajesz pracy.")
cena(layout="divisor", parte="1", titulo="Mianownik",
     nar="Część pierwsza: zbudujemy dolną liczbę, bo to ona jest trudna, a nie samo dzielenie.", sem_cap=True)
cena(layout="lista", kicker="Godziny, które oddajesz",
     itens=["Godziny z umowy", "Nadgodziny", "Dojazd w dwie strony", "Przerwa niepłatna", "Praca w domu"],
     nar="Do dolnej liczby wchodzą wszystkie godziny, których nie masz dla siebie z powodu tej pracy, a nie tylko te z umowy.", sem_cap=True)
cena(layout="item", kicker="Dojazd się liczy", preco="w dwie strony",
     nar="Dojazd wchodzi, bo bez tej pracy byś go nie robił. Godzina w autobusie nie jest twoja, choć nikt ci jej nie płaci.", sem_cap=True)
cena(layout="comparar",
     esq={"titulo": "Poza mianownikiem", "itens": ["Twoje hobby", "Sen", "Weekend bez pracy", "Urlop"]},
     dir={"titulo": "W mianowniku", "itens": ["Godziny z umowy", "Nadgodziny", "Dojazd", "Praca po godzinach"]},
     nar="Linia między jednym i drugim jest prosta: czy oddałbyś tę godzinę, gdyby ta praca zniknęła jutro.", sem_cap=True)
cena(layout="item", kicker="Góra to netto", preco="nie brutto",
     nar="Na górze stawki stoi kwota z przelewu, a nie z umowy. Brutto nigdy nie trafiło na twoje konto, więc nie może być dzielone.", sem_cap=True)
cena(layout="item", kicker="Premia tak", preco="ale średnia z roku",
     nar="Premie i dodatki wchodzą, ale jako średnia z całego roku. Jeden dobry miesiąc podniósłby stawkę, której nie masz przez resztę roku.", sem_cap=True)
cena(layout="item", kicker="Raz na zawsze", preco="potem już stoi",
     nar="Tę stawkę liczysz raz. Zmienia się tylko wtedy, gdy zmieni się umowa albo liczba godzin, a nie co miesiąc.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 3
cena(layout="titulo", kicker="Dwie liczby", sub="i jedno dzielenie",
     cap="Działanie: jedno dzielenie",
     nar="Teraz, kiedy mianownik istnieje, działanie jest jedno i robi się je w głowie. Nie potrzebujesz arkusza ani aplikacji.")
cena(layout="formula", formula="godziny = kwota ÷ stawka netto za godzinę",
     notas=["kwota: to, co widzisz na rachunku albo na cenie",
            "stawka: wypłata z przelewu przez wszystkie oddane godziny",
            "godziny: jedyny wynik, który coś ci mówi"],
     nar="U góry kwota, u dołu twoja stawka netto. Wynik wychodzi w godzinach, i to jest całe działanie.", sem_cap=True)
cena(layout="item", kicker="Zrób to raz dla stawki", preco="potem tylko dzielisz",
     nar="Stawkę liczysz jeden raz, a potem każdą cenę dzielisz przez tę samą liczbę. Drugie dzielenie zajmuje kilka sekund.", sem_cap=True)
cena(layout="numero", valor="godziny", legenda="jednostka wyniku",
     nota="nie złote — jednostka to połowa odpowiedzi", escala=0.5,
     nar="Zwróć uwagę na jednostkę. Jeśli wynik wychodzi w złotych, coś poszło nie tak w działaniu.", sem_cap=True)
cena(layout="item", kicker="Zaokrąglaj w górę", preco="zawsze w górę",
     nar="Jeśli wyjdzie dwie i pół godziny, zapisz trzy. Przy własnym czasie optymizm w drugim miejscu po przecinku nic nie daje.", sem_cap=True)
cena(layout="barras", kicker="Ten sam abonament",
     barras=[{"rotulo": "Stawka niska", "valor": 7}, {"rotulo": "Stawka średnia", "valor": 4}, {"rotulo": "Stawka wysoka", "valor": 2}],
     nar="Trzymasz górną liczbę w miejscu i zmieniasz tylko dolną. Godziny zmieniają się trzykrotnie, choć cena jest ta sama.", sem_cap=True)
cena(layout="item", kicker="Dwie drogi", preco="jeden wynik",
     nar="Z tego wynika, że godzin ubywa na dwa sposoby: albo rośnie stawka, albo maleje kwota. Drugi jest zwykle szybszy.", sem_cap=True)
cena(layout="item", kicker="To nie jest ocena", preco="to jest miara",
     nar="Wynik nie mówi, że wydajesz źle. Mówi tylko, ile czasu stoi za tą kwotą, i to jest informacja, nie wyrok.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 4
cena(layout="titulo", kicker="Papiery", sub="wszystkie już masz",
     cap="Z jakich papierów to wychodzi",
     nar="Żadnej z dwóch liczb nie zgadujesz. Obie są zapisane na papierach, które leżą u ciebie w domu albo w telefonie.")
cena(layout="divisor", parte="2", titulo="Papiery",
     nar="Część druga: gdzie dokładnie patrzysz, linijka po linijce, żeby nie wpisać liczby z pamięci.", sem_cap=True)
cena(layout="lista", kicker="Trzy źródła i koniec",
     itens=["Pasek wypłaty, trzy miesiące", "Umowa i grafik", "Rachunki za ostatni miesiąc"],
     nar="Trzy źródła wystarczą. Pasek daje wypłatę, grafik daje godziny, rachunki dają kwoty do podzielenia.", sem_cap=True)
cena(layout="item", kicker="Trzy miesiące", preco="jeden kłamie",
     nar="Weź trzy paski, a nie ostatni. Jeden miesiąc ukrywa premie, nadgodziny i wszystko, co nie wraca regularnie.", sem_cap=True)
cena(layout="item", kicker="Godziny z grafiku", preco="nie z umowy",
     nar="Godziny bierzesz z grafiku albo z własnych zapisków, nie z umowy. Umowa mówi, co uzgodniono, a nie co się stało.", sem_cap=True)
cena(layout="item", kicker="Dojazd z telefonu", preco="on już to zapisał",
     nar="Czas dojazdu masz w telefonie, w historii tras albo w rozkładzie. Nie musisz go mierzyć od nowa przez tydzień.", sem_cap=True)
cena(layout="item", kicker="Kwoty z rachunków", preco="te stałe najpierw",
     nar="Na początek weź tylko rachunki, które wracają co miesiąc. Jednorazowy wydatek policzysz później, kiedy stawka już stoi.", sem_cap=True)
cena(layout="item", kicker="Pół godziny", preco="i stawka gotowa",
     nar="Cała robota to pół godziny i robi się ją raz na całe życie tej stawki. Potem każde przeliczenie zajmuje kilka sekund.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 5
cena(layout="titulo", kicker="Dwa błędy", sub="oba dają zwykłą liczbę",
     cap="Dwa błędy, które dają liczbę",
     nar="Dwa błędy psują to działanie, i żaden z nich nie widać w wyniku. Właśnie dlatego warto je znać zawczasu.")
cena(layout="erro", codigo="#ARG!", causa="W liczniku stanęło brutto",
     saida="Wstaw kwotę z przelewu",
     nar="Pierwszy błąd: na górze stawki stawiasz brutto. Wtedy stawka rośnie, godzin wychodzi mniej, i wszystko wydaje się tańsze.", sem_cap=True)
cena(layout="item", kicker="Drugi kosztuje więcej", preco="i jest częstszy",
     nar="Drugi błąd, ten droższy: w mianowniku zostawiasz tylko godziny z umowy. Stawka znowu rośnie, i to podwójnie.", sem_cap=True)
cena(layout="item", kicker="Oba dają liczbę", preco="żaden nie daje błędu",
     nar="W obu przypadkach działanie wychodzi normalnie. Nikt ci nie powie, że dolna albo górna liczba była nie ta.", sem_cap=True)
cena(layout="formula", formula="sprawdzenie = stawka × godziny ≟ wypłata",
     notas=["jeśli się nie zgadza, błąd jest w jednej z dwóch liczb",
            "zrób działanie w drugą stronę, jeden raz",
            "dwie minuty, i łapie oba błędy"],
     nar="Sprawdzenie polega na odwróceniu działania. Mnożysz stawkę przez oddane godziny i musi wyjść twoja wypłata z przelewu.", sem_cap=True)
cena(layout="item", kicker="Drugie sprawdzenie", preco="to jedno pytanie",
     nar="I drugie sprawdzenie, prostsze: czy oddałbym tę godzinę, gdyby ta praca zniknęła. Jeśli nie, nie wchodzi do mianownika.", sem_cap=True)
cena(layout="item", kicker="Zapisz stawkę", preco="obok wyniku",
     nar="Trzymaj zapisaną stawkę obok wyniku w godzinach. Bez niej po trzech miesiącach nie będziesz wiedzieć, co policzyłeś.", sem_cap=True)
cena(layout="item", kicker="Błąd nie jest w dzieleniu", preco="jest w liczbach",
     nar="W całym tym działaniu dzielenie nigdy nie zawodzi. Zawodzą zawsze dwie liczby, i tylko je warto sprawdzać powtórnie.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 6
cena(layout="titulo", kicker="Ten rachunek", sub="i całkiem inne godziny",
     cap="Ten sam rachunek, inne godziny",
     nar="Tutaj widać, dlaczego sama kwota nic nie mówi. Dwie osoby z tym samym rachunkiem nie płacą za niego tyle samo.")
cena(layout="comparar",
     esq={"titulo": "Cena w złotych", "itens": ["Porównuje cię z innymi", "Nie mówi, ile to czasu", "Wygląda tak samo dla wszystkich"]},
     dir={"titulo": "Cena w godzinach", "itens": ["Porównuje cię z tobą", "Mówi, ile oddajesz", "Jest inna dla każdego"]},
     nar="Cena w złotych stawia cię w porównaniu z innymi. Cena w godzinach stawia cię w porównaniu z twoim własnym dniem.", sem_cap=True)
cena(layout="item", kicker="Jeden z dojazdem", preco="drugi z domu",
     nar="Dwie osoby z tą samą wypłatą, jedna z godziną dojazdu, druga z domu, mają inną stawkę i inne godziny za ten sam rachunek.", sem_cap=True)
cena(layout="numero", valor="×2", legenda="pół stawki, dwa razy więcej godzin",
     nota="ta sama cena, żadnej zmiany w wydatkach", escala=0.8,
     nar="Jeśli ktoś ma o połowę niższą stawkę, płaci za to samo dwa razy więcej godzin. Kwota na rachunku nie drgnęła.", sem_cap=True)
cena(layout="item", kicker="Dlatego się nie przenosi", preco="żadna liczba",
     nar="Dlatego żadna liczba usłyszana od kogoś innego nie pasuje do ciebie. Jego wynik odpowiada na jego stawkę, nie twoją.", sem_cap=True)
cena(layout="item", kicker="Ani średnia krajowa", preco="ona nie ma mianownika",
     nar="To samo dotyczy każdej średniej, która krąży w rozmowach. To kwota bez mianownika, czyli błąd z pierwszej części.", sem_cap=True)
cena(layout="barras", kicker="Ten sam rachunek, trzy osoby",
     barras=[{"rotulo": "Bez dojazdu", "valor": 2}, {"rotulo": "Godzina dojazdu", "valor": 4}, {"rotulo": "Dwie i nadgodziny", "valor": 7}],
     nar="Trzy osoby, jeden rachunek, trzy różne odpowiedzi. Różnica nie siedzi w tym, ile zarabiają na papierze.", sem_cap=True)
cena(layout="item", kicker="Wynik jest twój", preco="i nie pożycza się",
     nar="Wynik tego działania nie porównuje się z nikim i nie pożycza od nikogo. Jest twój, tak jak twój jest mianownik.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 7
cena(layout="titulo", kicker="Ile godzin", sub="odpowiedź nie jest liczbą",
     cap="Ile godzin to za dużo",
     nar="Zostaje trudne pytanie: ile godzin to już za dużo. I tu nie ma liczby, która pasuje do wszystkich.")
cena(layout="divisor", parte="3", titulo="Granica",
     nar="Część trzecia: jak wyznaczasz własną granicę, z własnych danych, a nie z czyjejś rady.", sem_cap=True)
cena(layout="item", kicker="Porównaj z tym", preco="co dostajesz w zamian",
     nar="Granica wychodzi z jednego porównania, i nikt go za ciebie nie zrobi: czy to, co dostaję w zamian, jest warte tych godzin, które za to oddaję każdego miesiąca.", sem_cap=True)
cena(layout="lista", kicker="Tu liczba zwykle boli",
     itens=["Abonamenty, których nie używasz", "Dojazd do pracy", "Odsetki od rat", "Opłaty za konto"],
     nar="Cztery rzeczy wychodzą w godzinach znacznie gorzej, niż wyglądają w złotych, i żadna z nich nie jest wielkim wydatkiem.", sem_cap=True)
cena(layout="item", kicker="Małe i stałe", preco="boli najbardziej",
     nar="Najgorzej wychodzi to, co małe i comiesięczne, bo mnoży się przez dwanaście miesięcy i wraca każdego roku bez pytania, a w złotych wygląda na drobną pozycję.", sem_cap=True)
cena(layout="numero", valor="1", legenda="pierwsza godzina",
     nota="jedna odzyskana godzina wraca co miesiąc", escala=1.0,
     nar="I jeśli granica wydaje się daleko, pierwsza odzyskana godzina zmienia najwięcej, bo wraca co miesiąc sama.", sem_cap=True)
cena(layout="item", kicker="Dziesiąta godzina", preco="zmienia mniej",
     nar="Od jednej godziny do dwóch zyskujesz spokój. Od dziewiątej do dziesiątej dużo mniej, przy tym samym wysiłku.", sem_cap=True)
cena(layout="item", kicker="Dlatego najpierw licz", preco="a potem decyduj",
     nar="Dlatego kolejność jest taka, a nie odwrotna: najpierw liczysz w godzinach, gdzie dzisiaj jesteś, i tylko potem decydujesz, co z tym zrobić i czy w ogóle warto.", sem_cap=True)

# ---------------------------------------------------------------- CAPITULO 8
cena(layout="titulo", kicker="Dzisiaj", sub="jedno działanie i jedna linijka",
     cap="Jedna liczba na dzisiaj",
     nar="Jeśli masz z tego zapamiętać jedną rzecz, zapamiętaj działanie. Kwota przez twoją stawkę netto, jeden raz.")
cena(layout="item", kicker="Zapisz stawkę", preco="gdzieś, gdzie wróci",
     nar="Zapisz stawkę netto za godzinę tam, gdzie ją jeszcze zobaczysz. Obok niej liczbę oddanych godzin, z której wyszła.", sem_cap=True)
cena(layout="item", kicker="Policz jeden rachunek", preco="ten największy",
     nar="Potem przelicz jeden rachunek, najlepiej ten największy, i zobacz, ile godzin za nim stoi. Jeden wystarczy na początek.", sem_cap=True)
cena(layout="item", kicker="Znowu za rok", preco="nie co tydzień",
     nar="Stawkę przeliczasz raz w roku albo przy zmianie umowy, a nie co tydzień. To, co zmienia się wolno, nie wymaga częstego mierzenia.", sem_cap=True)
cena(layout="item", kicker="Jeśli zmieni się dojazd", preco="zmienia się wynik",
     nar="Jeden wyjątek: jeśli zmieni się dojazd albo liczba godzin, policz od nowa od razu. Mianownik się zmienił, więc i odpowiedź.", sem_cap=True)
cena(layout="item", kicker="Liczba nie ocenia", preco="tylko pokazuje",
     nar="I jaka by nie wyszła, to nie jest ocena twoich wyborów. To twoje miejsce dzisiaj, potrzebne, żeby z niego ruszyć.", sem_cap=True)
cena(layout="item", kicker="Duża liczba", preco="to przydatna liczba",
     nar="Jeśli wyjdzie dużo godzin, nie kasuj tego. Duża liczba, którą znasz, jest lepsza niż mała, którą sobie wyobrażasz.", sem_cap=True)
cena(layout="cta", kicker="Ile godzin wyszło", sub="napisz pod spodem",
     nar="Policz jeden rachunek i napisz pod spodem jedną rzecz: ile godzin wyszło. Bez kwot i bez nazw.", sem_cap=True)

# ------------------------------------------------------------------- O SHORT
# UMA frase por cena, porque P e por FRASE e no polones ele e o maior (1,419 s).
SHORT = [
    dict(layout="titulo", kicker="Cena nic nie mówi", sub="brakuje mianownika",
         nar="Wiesz, ile kosztuje, ale nie ile to dla ciebie jest."),
    dict(layout="item", kicker="Nie ile kosztuje", preco="ile godzin zajmuje",
         nar="Pytanie nie jest o złote, tylko o twoje godziny pracy."),
    dict(layout="barras", kicker="Ten sam rachunek, trzy osoby",
         barras=[{"rotulo": "Bez dojazdu", "valor": 2}, {"rotulo": "Z dojazdem", "valor": 4}, {"rotulo": "Z nadgodzinami", "valor": 7}],
         nar="Ten sam rachunek to u trzech osób inne godziny."),
    dict(layout="item", kicker="Działanie jest jedno", preco="kwota przez stawkę",
         nar="Kwotę dzielisz przez stawkę netto za godzinę."),
    dict(layout="titulo", kicker="Netto, nie brutto", sub="i wszystkie godziny",
         nar="Na górze kwota z przelewu, nie ta z umowy."),
    dict(layout="lista", kicker="Te godziny oddajesz",
         itens=["Z umowy", "Nadgodziny", "Dojazd", "Praca w domu"],
         nar="W mianowniku są też nadgodziny i dojazd."),
    dict(layout="item", kicker="Drogi błąd", preco="tylko godziny z umowy",
         nar="Same godziny z umowy zaniżają wynik podwójnie."),
    dict(layout="barras", kicker="Ta sama cena, inna stawka",
         barras=[{"rotulo": "Wysoka", "valor": 2}, {"rotulo": "Średnia", "valor": 4}, {"rotulo": "Niska", "valor": 7}],
         nar="Niższa stawka to więcej godzin za tę samą cenę."),
    dict(layout="item", kicker="Zaokrąglaj w górę", preco="i zapisz to",
         nar="Dwie i pół godziny znaczy trzy, i zapisz tę liczbę."),
    dict(layout="cta", kicker="Ile godzin wyszło", sub="napisz pod spodem",
         nar="Przelicz rachunek i napisz tylko godziny."),
]

COPY = """# Twoja godzina jako jednostka ceny: ile godzin kosztuje każdy rachunek

## TITULO
Twoja Godzina jako Jednostka Ceny: Ile Godzin Kosztuje Każdy Rachunek

## DESCRICAO
Widzisz kwotę na rachunku i wiesz, ile to złotych. Nie wiesz, ile to dla ciebie znaczy — i powód nie leży w cenie, tylko w tym, że brakuje drugiej liczby. Kwota bez mianownika nic nie mówi, bo ta sama kwota u dwóch osób to pół dnia pracy u jednej i prawie trzy dni u drugiej.

W tym nagraniu robimy jedno działanie: kwota podzielona przez twoją stawkę netto za godzinę. Wynik nie wychodzi w złotych, wychodzi w godzinach — i to jest jedyna liczba, która mówi, ile swojego czasu oddajesz za daną rzecz.

Nie ma tu ani jednej mojej liczby. Żadnego procentu, żadnej średniej krajowej, żadnej stawki podatku i żadnej rady w stylu „tyle powinno wystarczyć". Wszystkie liczby działania są twoje: wypłata z twojego przelewu i godziny z twojego grafiku.

Jeden rozdział buduje mianownik, bo to on jest trudny, a nie samo dzielenie. Do godzin wchodzi wszystko, czego nie masz dla siebie z powodu tej pracy: godziny z umowy, nadgodziny, dojazd w dwie strony, niepłatna przerwa i praca po godzinach w domu. Nie wchodzi sen, weekend bez pracy ani urlop, a sprawdzenie jest jednym pytaniem: czy oddałbym tę godzinę, gdyby ta praca zniknęła jutro.

Jeden rozdział pokazuje, z jakich trzech papierów wychodzą obie liczby, linijka po linijce: pasek wypłaty z trzech miesięcy, a nie z jednego, bo jeden ukrywa premie i nadgodziny; umowa razem z grafikiem, bo umowa mówi, co uzgodniono, a nie co się stało; i rachunki za ostatni miesiąc. Czas dojazdu masz już zapisany w telefonie.

Jeden rozdział mówi o dwóch błędach, które dają zupełnie normalny wynik i oba są błędne: brutto w liczniku, które nigdy nie trafiło na twoje konto, oraz same godziny z umowy w mianowniku. Oba zawyżają stawkę, więc oba sprawiają, że wszystko wygląda taniej. Dlatego jest sprawdzenie: pomnóż stawkę przez oddane godziny i musi wyjść twoja wypłata.

I jeden rozdział o granicy, która nie jest liczbą z porady. Wychodzi z porównania tego, co dostajesz, z godzinami, które oddajesz — a najgorzej wypada to, co małe i comiesięczne, bo mnoży się przez dwanaście i wraca każdego roku.

Policz jeden rachunek i napisz w komentarzu jedną rzecz: ile godzin wyszło. Bez kwot.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Przelicz jeden rachunek i napisz pod spodem jedną rzecz: ile godzin wyszło. Bez kwot i bez nazw. Chcę zobaczyć, jak bardzo ta liczba różni się między ludźmi, którzy myślą, że są w tym samym miejscu.

## HASHTAGS
#FinanseOsobiste #TwójCzas #KolejnyPoziom

## TAGS
finanse osobiste, stawka godzinowa, netto za godzine, koszt czasu, dojazd do pracy, pasek wyplaty, nadgodziny, budzet domowy, abonamenty, policz sam, ile kosztuje twoj czas, oplaty stale, wartosc godziny, rachunki

## CONFIGURACOES DO STUDIO
- Idioma: Polones (pl) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Polonia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita percentual, nao cita salario medio, nao cita aliquota, nao cita valor de abonamento e nao recomenda "tantas horas". Todos os numeros da conta saem do proprio pasek wyplaty e do proprio grafico de horas de quem assiste, e por isso nao ha numero meu que possa envelhecer nem que dependa do pais, da regiao ou do ano. Este video e da classe PROCEDIMENTO: a trava de duas fontes institucionais (600) se aplica a numero sobre o MUNDO que muda, e aqui nao existe nenhum. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA: qualquer comparacao com salario medio e qualquer limite de "quantas horas e demais". O primeiro mudaria a conta de quem assiste por uma referencia que nao e dele; o segundo depende do que a pessoa recebe em troca, e cita-lo tornaria o video um conselho em vez de uma medida. O video tambem nao diz que trabalhar menos e sempre melhor, nao recomenda demitir-se, nao indica produto nem instituicao e nao e aconselhamento financeiro.
"""

sp = {
    "slug": "kolejny-poziom",          # em PACOTE o slug e o CANAL
    "pacote": "kolejny-poziom-020",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",             # NUNCA copie trilha de outro canal (601)
    "thumb": {"l1": "Nie złote", "l2": "godziny"},
    "longo": L,
    "short": SHORT,
    "copy": COPY,
}

import temas_do_dono as TD
sp["paleta"] = TD.paleta_do_canal("kolejny-poziom")

import trilho
n = trilho.aplica_no_longo(sp["longo"])

destino = os.path.join(RAIZ, "fabrica", "specs", "kolejny-poziom-020.json")
with open(destino, "w", encoding="utf-8") as f:
    json.dump(sp, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(f"gravado {destino}")
print(f"longo {len(L)} cenas | short {len(SHORT)} | trilho {n} capitulos")
