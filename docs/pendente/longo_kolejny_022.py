# -*- coding: utf-8 -*-
"""As 64 cenas do longo `kolejny-poziom-022`, em SETE capitulos.

CLASSE PROCEDIMENTO: o espectador faz a conta com os PROPRIOS documentos, logo a
trava 600 (duas fontes institucionais) nao se aplica — ZERO numero meu sobre o
mundo. As quantidades faladas sao a estrutura do proprio procedimento (tres
colunas, duas ofertas, doze meses).
"""

CAPS = ["Dwie oferty", "Co jest stałe", "Co od zużycia", "Co warunkowe",
        "Którą parę", "To samo okno", "Twoja kartka"]


def T(kicker, sub, cap, nar):
    return dict(layout="titulo", kicker=kicker, sub=sub, cap=cap, nar=nar)


def I(kicker, preco, nar):
    return dict(layout="item", kicker=kicker, preco=preco, sem_cap=True, nar=nar)


def L(kicker, itens, nar):
    return dict(layout="lista", kicker=kicker, itens=itens, sem_cap=True, nar=nar)


def B(kicker, pares, nar):
    return dict(layout="barras", kicker=kicker,
                barras=[{"rotulo": r, "valor": v} for r, v in pares],
                sem_cap=True, nar=nar)


def N(valor, legenda, nota, nar):
    return dict(layout="numero", valor=valor, legenda=legenda, nota=nota,
                escala=1.0, sem_cap=True, nar=nar)


def C(esq_t, esq_i, dir_t, dir_i, nar):
    return dict(layout="comparar", esq={"titulo": esq_t, "itens": esq_i},
                dir={"titulo": dir_t, "itens": dir_i}, sem_cap=True, nar=nar)


def F(formula, notas, nar):
    return dict(layout="formula", formula=formula, notas=notas,
                sem_cap=True, nar=nar)


def E(codigo, causa, saida, nar):
    return dict(layout="erro", codigo=codigo, causa=causa, saida=saida,
                sem_cap=True, nar=nar)


def D(parte, titulo, nar):
    return dict(layout="divisor", parte=parte, titulo=titulo,
                sem_cap=True, nar=nar)


LONGO = [
    # ---------------------------------------------- 1. Dwie oferty
    T("Dwie oferty", "jedna kartka", "Dwie oferty",
      "Masz przed sobą dwie oferty na to samo: prąd, telefon, internet albo "
      "ubezpieczenie. Obie wyglądają na policzalne i obie mają w środku liczby, "
      "które da się dodać."),
    I("To nagranie nie wybiera za ciebie", "pokazuje, jak ułożyć kartkę",
      "To nagranie nie powie ci, która oferta jest lepsza, bo tego nie wiem. "
      "Pokaże jedno: jak rozłożyć obie na trzy kolumny, żeby twoja własna liczba "
      "wyszła taka sama za każdym razem."),
    I("Dlaczego kolumny", "bo każda linijka pyta o inną operację",
      "Powód jest prosty i nie ma nic wspólnego z ceną. Linijki w ofercie nie są "
      "tego samego rodzaju: jedne się dodaje, drugie mnoży, a trzecich nie "
      "wpisuje się do rachunku wcale."),
    L("Trzy kolumny",
      ["Stałe: dodajesz", "Od zużycia: mnożysz", "Warunkowe: zapisujesz datę"],
      "Trzy kolumny i trzy operacje. Stałe dodajesz, zależne od zużycia mnożysz "
      "przez swoją liczbę, a warunkowe nie wchodzą do wyniku — trafiają do "
      "kalendarza."),
    I("Co dostajesz na końcu", "jedną liczbę na miesiąc, dla każdej oferty",
      "Na końcu masz dwie liczby i jedną datę. Dwie liczby porównujesz, a data "
      "mówi ci, kiedy ten rachunek przestaje być prawdziwy."),
    E("#MIX!", "Wszystkie linijki w jednej kolumnie",
      "Rozdziel linijki po rodzaju, zanim cokolwiek dodasz",
      "Najczęstszy błąd jest właśnie taki: wszystko ląduje w jednym worku, "
      "dodaje się po kolei, wynik wychodzi i wygląda na odpowiedź. Rachunek się "
      "zgadza, tylko opisuje coś innego niż myślisz."),
    D("1", "Co jest stałe",
      "Zacznijmy od kolumny, która jest najłatwiejsza i dlatego najczęściej "
      "wypełniana źle."),

    # ---------------------------------------------- 2. Co jest stałe
    T("Co jest stałe", "płacisz, nawet nie używając", "Co jest stałe",
      "Stała linijka to taka, którą zapłacisz nawet wtedy, gdy przez cały "
      "miesiąc nie zużyjesz niczego. Nie zależy od licznika, od minut ani od "
      "gigabajtów."),
    I("Test jednej minuty", "wyjeżdżam na miesiąc — co i tak zapłacę?",
      "Test jest jednozdaniowy: wyobraź sobie, że wyjeżdżasz na cały miesiąc i "
      "nie włączasz niczego. To, co i tak przyjdzie do zapłaty, jest stałe."),
    L("Gdzie siedzą stałe",
      ["Opłata abonamentowa", "Opłata handlowa", "Opłata za licznik",
       "Opłata za konto albo kartę"],
      "W fakturach te linijki mają swoje nazwy i rzadko są duże. Opłata "
      "abonamentowa, opłata handlowa, opłata za układ pomiarowy, opłata za "
      "prowadzenie konta."),
    I("Dlaczego je się pomija", "są małe i nie zmieniają się",
      "Pomija się je z dwóch powodów naraz: są małe i nigdy nie drgają. Oko "
      "szuka tego, co się rusza, a stała linijka się nie rusza."),
    N("12", "razy w roku, każda z nich",
      "mała linijka razy dwanaście przestaje być mała",
      "Tylko że każda z nich wraca dwanaście razy w roku. Mała linijka "
      "pomnożona przez dwanaście przestaje być mała, a w porównaniu dwóch ofert "
      "to często ta część, która decyduje."),
    I("Jak je wpisać", "suma, bez mnożenia przez zużycie",
      "Do kolumny pierwszej wpisujesz je po prostu zsumowane, w ujęciu "
      "miesięcznym. Żadnego mnożenia przez zużycie: one o twoim zużyciu nic nie "
      "wiedzą."),
    I("Jedna pułapka", "część stałych jest roczna",
      "Jedna pułapka: niektóre stałe przychodzą raz w roku, nie raz w miesiącu. "
      "Te dzielisz przez dwanaście, zanim wpiszesz, żeby obie oferty były w tej "
      "samej jednostce."),
    F("kolumna stałych = suma miesięcznych + suma rocznych ÷ 12",
      ["miesięczne: wracają w każdym rachunku",
       "roczne: wracają raz, więc dzielisz",
       "wynik: ile płacisz, nic nie zużywając"],
      "Kolumna pierwsza to suma linijek miesięcznych plus suma linijek rocznych "
      "podzielona przez dwanaście. To twoja podłoga: tyle płacisz, nie zużywając "
      "niczego."),
    E("#BRAK!", "Oferta pokazuje tylko cenę za jednostkę",
      "Poproś o rozbicie na stałe i zmienne — to część oferty, nie tajemnica",
      "Jeśli oferta pokazuje tylko cenę za jednostkę i ani słowa o opłatach "
      "stałych, to nie jest oferta kompletna. Rozbicie na stałe i zmienne jest "
      "częścią warunków, nie tajemnicą handlową."),
    I("Po co ta kolumna", "bo tylko ona jest wspólna",
      "Ta kolumna ma jeszcze jedną wartość: jest jedyną, której nie trzeba "
      "szacować. Tu nie ma twojego zużycia, więc nie ma miejsca na zgadywanie."),
    D("2", "Co od zużycia",
      "Druga kolumna jest ta, w której wchodzi twoja własna liczba — i to ona "
      "zmienia wynik najmocniej."),

    # ---------------------------------------------- 3. Co od zużycia
    T("Co od zużycia", "cena razy twoja liczba", "Co od zużycia",
      "Druga kolumna to linijki, które zależą od tego, ile zużywasz. Cena za "
      "jednostkę razy liczba jednostek — i ta liczba musi być twoja, nie "
      "przykładowa."),
    I("Skąd bierzesz swoją liczbę", "z własnych rachunków, nie z pamięci",
      "Swoją liczbę bierzesz z własnych rachunków za ostatni rok, nie z pamięci "
      "i nie z przykładu w ofercie. Przykład w ofercie opisuje kogoś, kogo nie "
      "znasz."),
    I("Ile rachunków", "dwanaście, jeśli masz",
      "Najlepiej dwanaście rachunków, bo zużycie bywa sezonowe. Jeśli masz "
      "mniej, policz z tego, co jest, i dopisz na kartce, z ilu miesięcy to "
      "wyszło."),
    B("Jeden miesiąc czy dwanaście",
      [("Jeden miesiąc", 3), ("Pół roku", 6), ("Cały rok", 10)],
      "Im więcej miesięcy, tym mniej przypadku w twojej liczbie. Jeden miesiąc "
      "to zdjęcie jednej pory roku, a nie twój rok."),
    I("Dlaczego nie średnia z internetu", "bo liczy zbiór, a nie ciebie",
      "Średnie zużycie podane w artykule opisuje zbiór ludzi. Twoja faktura "
      "opisuje ciebie, a to są dwie różne liczby i tylko jedna z nich wchodzi "
      "do twojego rachunku."),
    F("kolumna zużycia = cena za jednostkę × twoje jednostki w miesiącu",
      ["cena: z oferty", "jednostki: z twoich rachunków",
       "ta sama liczba jednostek po obu stronach"],
      "Kolumna druga to cena za jednostkę razy twoje jednostki. I uwaga na "
      "rzecz, która łatwo ucieka: po obu stronach wstawiasz tę samą liczbę "
      "jednostek, bo porównujesz oferty, nie dwa różne życia."),
    E("#DWA!", "Dwa różne zużycia w dwóch kolumnach",
      "Jedna liczba jednostek, obie oferty",
      "Jeśli w jednej kolumnie wpiszesz zużycie z zimy, a w drugiej z lata, "
      "wynik pokaże różnicę pór roku, nie różnicę ofert. To ten sam błąd, co "
      "ważenie się na dwóch różnych wagach."),
    I("Gdy oferta ma progi", "policz swoje miesiące osobno",
      "Jeśli cena ma progi albo pakiet z nadwyżką, nie wstawiaj średniej. "
      "Policz osobno miesiące, w których jesteś pod progiem, i te, w których go "
      "przekraczasz."),
    I("Dlaczego nie średnia", "średnia nie trafia w żaden twój miesiąc",
      "Przy progach średnia daje wynik, którego nie produkuje żaden twój "
      "miesiąc. Rachunek wychodzi gładki, a żadna twoja faktura tak nie "
      "wygląda."),
    I("Jednostki muszą się zgadzać", "kilowatogodziny, gigabajty, minuty",
      "Sprawdź jeszcze, czy jednostki są te same. Cena za kilowatogodzinę i "
      "cena za megawatogodzinę różnią się o tysiąc, a wyglądają podobnie na "
      "papierze."),
    D("3", "Co warunkowe",
      "Trzecia kolumna jest najkrótsza i jedyna, która nie wchodzi do wyniku."),

    # ---------------------------------------------- 4. Co warunkowe
    T("Co warunkowe", "obowiązuje, dopóki coś jest spełnione", "Co warunkowe",
      "Trzecia kolumna to linijki, które obowiązują tylko pod warunkiem. "
      "Rabat na dwanaście miesięcy, cena przy zgodzie na e-fakturę, zniżka za "
      "płatność automatyczną, upust przy umowie na czas."),
    I("Co je łączy", "każda ma warunek i każda ma datę",
      "Łączy je jedno: każda ma warunek, a warunek ma koniec. Czasem koniec "
      "jest datą, czasem zdarzeniem, ale zawsze istnieje."),
    I("Dlaczego nie wchodzą do wyniku", "bo wynik miałby datę ważności",
      "Nie wpisujesz ich do wyniku, bo wtedy twoja jedna liczba przestaje być "
      "jedną liczbą: staje się liczbą ważną do pewnego dnia, bez tego dnia "
      "zapisanego nigdzie."),
    C("Do rachunku", ["Opłaty stałe", "Cena za jednostkę"],
      "Do kalendarza", ["Rabat na czas", "Zniżka za warunek"],
      "Pierwsze dwie kolumny idą do rachunku. Trzecia idzie do kalendarza, i to "
      "nie jest ucieczka od liczenia: to miejsce, w którym ta informacja "
      "faktycznie działa."),
    I("Jak to zapisać", "data i co się stanie, gdy minie",
      "Zapisujesz dwie rzeczy: datę, w której warunek się kończy, i to, co "
      "wtedy wraca. Zwykle wraca cena podstawowa, która w ofercie też jest "
      "podana."),
    N("2", "liczby na kartce, jedna data obok",
      "data nie jest kosztem, jest terminem ponownego liczenia",
      "Na kartce masz więc dwie liczby i co najmniej jedną datę. Data nie jest "
      "kosztem. Jest terminem, w którym ten rachunek trzeba zrobić jeszcze raz."),
    I("Druga oferta też ją ma", "porównaj daty, nie tylko kwoty",
      "Druga oferta zwykle ma własny warunek i własną datę. Porównanie dat bywa "
      "ważniejsze niż porównanie kwot, bo krótszy warunek znaczy, że wrócisz do "
      "tej kartki szybciej."),
    E("#WARUNEK!", "Rabat czasowy policzony jak cena stała",
      "Przenieś go do trzeciej kolumny i dopisz datę",
      "Policzenie rabatu czasowego jak ceny stałej to najkosztowniejszy z tych "
      "błędów, bo on nie boli od razu. Boli w miesiącu, w którym warunek "
      "wygasa, a wtedy nikt już nie pamięta, skąd była ta liczba."),
    I("Co jeszcze tu trafia", "kaucje i opłaty za wyjście",
      "Do tej kolumny trafiają też kaucje i opłaty za wcześniejsze zakończenie. "
      "Nie są kosztem miesięcznym, ale są warunkiem, pod którym twoja liczba "
      "jest prawdziwa."),
    D("4", "Którą parę",
      "Teraz najważniejsza część, i ona nie dotyczy żadnej kolumny. Dotyczy "
      "tego, co z czym zestawiasz."),

    # ---------------------------------------------- 5. Którą parę
    T("Którą parę", "porównujesz z czym", "Którą parę",
      "Masz ułożone kolumny i możesz liczyć. Zostaje pytanie, które decyduje o "
      "wyniku bardziej niż którakolwiek linijka: którą parę właściwie "
      "porównujesz?"),
    I("Co zwykle robi człowiek", "nową ofertę kontra własny rachunek",
      "Odruch jest jeden: bierzesz nową ofertę, którą ktoś ci pokazał, i "
      "stawiasz ją obok swojego ostatniego rachunku. Dwie liczby, jedna "
      "większa, decyzja wydaje się zrobiona."),
    C("Nowa oferta", ["Cena dla nowego klienta", "Rabat na start"],
      "Twój rachunek", ["Cena po rabacie, który minął", "Bez żadnej zniżki"],
      "Tylko że te dwie liczby nie są z tej samej półki. Po jednej stronie masz "
      "cenę przygotowaną dla kogoś, kto jeszcze nie jest klientem. Po drugiej "
      "swoją, z której rabat już dawno zniknął."),
    I("Dlaczego to nie jest para", "jedna jest najlepsza, druga najgorsza",
      "To nie jest porównanie dwóch ofert. To porównanie najlepszej ceny, jaką "
      "ktoś daje na wejściu, z najgorszą, jaką masz po wygaśnięciu warunku. "
      "Wynik jest przewidywalny, zanim cokolwiek policzysz."),
    N("3", "liczby istnieją, a porównujesz dwie",
      "trzecia to oferta dla ciebie jako klienta, który zostaje",
      "Liczb jest trzy, nie dwie. Cena dla nowego, twoja obecna, i cena dla "
      "ciebie jako kogoś, kto zostaje. Tej trzeciej nie ma na żadnym papierze, "
      "który dostałeś — dlatego nie wchodzi do porównania."),
    I("Skąd ją wziąć", "pytasz u siebie, zanim porównasz",
      "Trzecią liczbę zdobywa się jednym pytaniem u swojego dostawcy, zanim "
      "zrobisz porównanie. Pytasz o aktualną ofertę dla obecnego klienta i o to, "
      "czy twoja taryfa ma wersję, której nie masz."),
    I("Co to zmienia w kartce", "trzecia kolumna liczb, ten sam szablon",
      "W kartce nic się nie psuje: dokładasz trzecią kolumnę liczb i liczysz ją "
      "tym samym szablonem. Stałe dodane, zużycie pomnożone, warunki z datą "
      "obok."),
    E("#PARA!", "Oferta dla nowego kontra twój rachunek po wygaśnięciu",
      "Zdobądź trzecią liczbę i porównaj trzy, nie dwie",
      "Jeśli porównujesz tylko dwie, wynik mówi ci, że trzeba zmienić dostawcę "
      "— i może to prawda, a może nie. Z trzema liczbami widzisz, czy zmiana "
      "jest potrzebna, czy wystarczy prośba."),
    I("Jeszcze jedna para, której unikaj", "twoja kwota kontra kwota sąsiada",
      "I jeszcze jedna para, która nie daje nic: twoja kwota obok kwoty kogoś "
      "innego. Inne zużycie, inna umowa, inna taryfa. Z takiego zestawienia nie "
      "wynika żadna decyzja."),
    D("5", "To samo okno",
      "Przed podsumowaniem jedna rzecz techniczna, która psuje poprawnie "
      "zrobione rachunki."),

    # ---------------------------------------------- 6. To samo okno
    T("To samo okno", "miesiąc do miesiąca, rok do roku", "To samo okno",
      "Obie liczby muszą dotyczyć tego samego okna czasu. Miesiąc do miesiąca "
      "albo rok do roku, nigdy jedno z drugim."),
    I("Dlaczego to łatwo pomylić", "oferty podają różne okresy",
      "Mylisz się łatwo, bo oferty same podają różne okresy. Jedna mówi o "
      "cenie miesięcznej, druga o rocznej, trzecia o cenie za okres "
      "rozliczeniowy, który nie jest ani jednym, ani drugim."),
    I("Okres rozliczeniowy", "sprawdź, ile ma miesięcy",
      "Sprawdź, ile miesięcy ma twój okres rozliczeniowy. Jeśli rozliczasz się "
      "co dwa miesiące, kwota z faktury nie jest kwotą miesięczną i nie wolno "
      "jej porównać z ceną miesięczną."),
    F("okno roczne = kwota miesięczna × 12",
      ["albo: kwota dwumiesięczna × 6",
       "roczne stałe wchodzą bez dzielenia",
       "jedno okno po obu stronach"],
      "Najprościej policzyć wszystko w oknie rocznym: kwotę miesięczną razy "
      "dwanaście, a pozycje roczne wpisać bez dzielenia. W oknie rocznym nic "
      "się nie dzieli i nic nie ucieka."),
    I("Dlaczego rok jest wygodniejszy", "bo sezony i roczne opłaty same wchodzą",
      "Rok jest wygodniejszy z dwóch powodów: sezonowe zużycie mieści się w nim "
      "całe, a opłaty roczne nie wymagają dzielenia. Mniej dzieleń to mniej "
      "miejsc na pomyłkę."),
    E("#OKNO!", "Cena miesięczna obok kwoty z faktury za dwa miesiące",
      "Doprowadź obie do jednego okna, zanim porównasz",
      "Zestawienie ceny miesięcznej z kwotą za okres dwumiesięczny daje różnicę "
      "rzędu dwóch, która nie ma nic wspólnego z ofertą. I nic w rachunku tego "
      "nie zgłasza."),
    I("Na koniec sprawdzenie", "podstaw swój ostatni rachunek",
      "Jest proste sprawdzenie całej kartki: podstaw do kolumny swojej obecnej "
      "taryfy liczby z ostatniego rachunku. Jeśli wynik nie zgadza się z kwotą "
      "na fakturze, gdzieś brakuje linijki."),
    I("Co wtedy", "najczęściej brakuje opłaty stałej",
      "Najczęściej brakuje właśnie opłaty stałej, bo była mała. Wtedy wracasz "
      "do pierwszej kolumny i czytasz fakturę linijka po linijce."),
    D("6", "Twoja kartka",
      "Zbierzmy to w jedną rzecz do zrobienia, bo cała ta kartka prowadzi do "
      "dwóch liczb i jednej daty."),

    # ---------------------------------------------- 7. Twoja kartka
    T("Twoja kartka", "dwie liczby i data", "Twoja kartka",
      "Weź jedną kartkę i podziel ją na trzy kolumny w poprzek i tyle wierszy, "
      "ile masz ofert do porównania. Nic więcej nie jest potrzebne."),
    L("Co wpisujesz w wiersz",
      ["Suma stałych w oknie", "Cena × twoje zużycie",
       "Warunek i jego data"],
      "W każdym wierszu trzy pola: suma stałych w wybranym oknie, cena razy "
      "twoje zużycie w tym samym oknie, i warunek z datą."),
    I("Twoje zużycie wpisz raz", "ta sama liczba we wszystkich wierszach",
      "Twoje zużycie wpisujesz raz, na górze kartki, i używasz tej samej liczby "
      "we wszystkich wierszach. To ono trzyma porównanie uczciwym."),
    I("Wierszy jest trzy, nie dwa", "nowa, obecna, i dla pozostających",
      "Wierszy jest trzy: nowa oferta, twoja obecna taryfa i oferta dla "
      "obecnego klienta. Trzeciego nie wpiszesz, póki o niego nie zapytasz."),
    B("Co decyduje w porównaniu",
      [("Cena za jednostkę", 7), ("Opłaty stałe", 7), ("Warunek i data", 7)],
      "Nie da się z góry powiedzieć, która kolumna zdecyduje. Przy małym "
      "zużyciu decydują opłaty stałe, przy dużym cena jednostki, a przy krótkim "
      "warunku decyduje data."),
    I("Dlatego nie ma jednej odpowiedzi", "liczba jest twoja, nie moja",
      "Dlatego nie podaję tu żadnej ceny i nie mówię, co wybrać. Odpowiedź "
      "zależy od twojego zużycia i twojego okna, a oba masz w dokumentach, "
      "które już są w domu."),
    I("Ile to zajmuje", "jeden wieczór, raz",
      "Cała kartka to jeden wieczór przy stole, raz. Potem wracasz do niej "
      "tylko w dacie z trzeciej kolumny, i wtedy zmieniasz jedną liczbę."),
    I("Co zyskujesz", "porównanie, które powtórzysz",
      "Zyskujesz porównanie, które wychodzi tak samo za rok i które umiesz "
      "powtórzyć. Liczba z internetu nie ma tej własności."),
    I("Jedna rzecz na dziś", "znajdź opłatę stałą na swojej fakturze",
      "Jeśli masz zrobić dziś jedną rzecz, zrób tę: znajdź na swojej fakturze "
      "linijkę, która nie zależy od zużycia, i zapisz jej kwotę. To pierwsze "
      "pole pierwszej kolumny."),
    dict(layout="cta", kicker="Trzy kolumny, trzy operacje",
         sub="zrób swoją kartkę i zasubskrybuj",
         nar="Trzy kolumny i trzy operacje: dodać, pomnożyć, zapisać datę. Zrób "
             "swoją kartkę i zasubskrybuj, jeśli chcesz kolejne takie rachunki."),
]
