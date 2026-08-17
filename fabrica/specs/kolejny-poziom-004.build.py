#!/usr/bin/env python3
"""kolejny-poziom-004 — ile z 200 zl miesiecznie zjadaja oplaty i podatek.

PAUTA (PASSO 0, 17/08/2026). O `pautas_banco` do canal tem doze outliers de
financas pessoais em polones; o maior e "W co inwestowac 200 zl miesiecznie?
KONKRETY" com 5.755,7 views/dia — quatro vezes acima do segundo colocado no
mesmo eixo. A ESTRUTURA copiada e a dele: quantia mensal pequena e concreta,
pergunta direta, promessa de conta feita ate o fim. O ASSUNTO nao: ele responde
ONDE por o dinheiro, e este responde QUANTO do dinheiro nao chega.

EIXO NAO USADO. O canal ja publicou tres eixos:
  * Xgt32iH8Ft8 — plano de financas com a pensja media de 9.233 zl
  * YLGwalTND7M — emerytura z ZUS, 34,4% da ultima pensja em 2050
  * MjI4ZGJAhIo — nadplacac kredyt czy inwestowac
Os tres falam de QUANTO acumular. Nenhum fala do vazamento: a oplata za
zarzadzanie e o podatek Belki saem antes de o capital existir, e nao aparecem em
nenhum extrato como despesa.

NUMEROS — duas fontes que batem em cada um:
  * Limit IKE 2026 = 28.260 zl. Obwieszczenie MRPiPS de 17/11/2025 (Monitor
    Polski). Confirmado por PAP Biznes e pela Analizy.pl.
  * Limit IKZE 2026 = 11.304 zl, e 16.956 zl para quem tem dzialalnosc.
    Obwieszczenie MRPiPS de 10/11/2025. Confirmado por PAP Biznes e BDO.
  * Podatek Belki = 19% dos ganhos de capital, cobrado na venda.
  * Limite legal da oplata za zarzadzanie = 2% ao ano do ativo, desde
    01/01/2022 (rozporzadzenie MF). Historico confirmado por Analizy.pl e SII:
    3,5% em 2019, 3% em 2020, 2,5% em 2021, 2% a partir de 2022.
  * Ulga w PIT pela wplata no IKZE: cerca de 1.356 zl no primeiro escalao (12%)
    e cerca de 3.617 zl no segundo (32%), sobre o limite de 11.304 zl.

A CONTA do video (200 zl/mies, 30 anos, 5% real bruto) esta feita no rodape
deste arquivo e sai de juros compostos mensais — nenhum numero foi arredondado
para caber na narracao.

DIMENSIONAMENTO. Voz medida hoje, nao a de laboratorio: pl-PL-MarekNeural com
R = 23,58 chars/s e P = 1,428 s/frase, ajuste por minimos quadrados sobre oito
amostras de comprimento deliberadamente desigual (17 a 214 caracteres) — com
uma so distribuicao o ajuste nao separa a taxa da pausa. O laboratorio dizia
R = 22,75 e P = 1,291.
"""
import json
import os

SLUG = "kolejny-poziom"
PACOTE = "kolejny-poziom-004"

PALETA = {"bg": "#F4F6FB", "c1": "#1D3557", "c2": "#E63946", "ink": "#14213D"}


def t(kicker, sub, nar, cap=None, sem_cap=False):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    if sem_cap:
        c["sem_cap"] = True
    return c


def i(kicker, preco, nar, cap=None, sem_cap=False):
    c = {"layout": "item", "kicker": kicker, "preco": preco, "nar": nar}
    if cap:
        c["cap"] = cap
    if sem_cap:
        c["sem_cap"] = True
    return c


def li(kicker, itens, nar, cap=None, sem_cap=False):
    c = {"layout": "lista", "kicker": kicker, "itens": itens, "nar": nar}
    if cap:
        c["cap"] = cap
    if sem_cap:
        c["sem_cap"] = True
    return c


def b(kicker, itens, alturas, nar, cap=None, sem_cap=False):
    c = {"layout": "barras", "kicker": kicker, "itens": itens,
         "alturas": alturas, "nar": nar}
    if cap:
        c["cap"] = cap
    if sem_cap:
        c["sem_cap"] = True
    return c


def cta(kicker, sub, nar):
    return {"layout": "cta", "kicker": kicker, "sub": sub, "nar": nar,
            "sem_cap": True}


LONGO = [
    # ---------- 1. przelew, ktory wychodzi ----------
    t("DWIESCIE ZLOTYCH", "co miesiac, przez trzydziesci lat",
      "Odkladasz dwiescie zlotych miesiecznie. Robisz to przez trzydziesci lat, "
      "bez jednej przerwy. Na koniec patrzysz na rachunek i liczba jest mniejsza, "
      "niz powinna byc.",
      cap="Przelew, ktory wychodzi"),
    i("Ile wplacasz", "siedemdziesiat dwa tysiace",
      "Zacznijmy od tego, co wychodzi z twojego konta. Dwiescie zlotych razy "
      "trzysta szescdziesiat miesiecy to siedemdziesiat dwa tysiace zlotych "
      "wlasnych pieniedzy."),
    i("Ile powinno urosnac", "sto szescdziesiat szesc tysiecy",
      "Przy piecioprocentowej realnej stopie zwrotu te wplaty rosna do okolo "
      "stu szescdziesieciu szesciu tysiecy zlotych. Tak wyglada wykres, ktory "
      "pokazuja ci przy podpisywaniu umowy."),
    t("A TERAZ PRAWDA", "ten wykres nic nie odejmuje",
      "Tylko ze ten wykres nic nie odejmuje. Nie ma w nim oplaty za zarzadzanie "
      "ani podatku od zysku. Oba istnieja i oba pobiera sie automatycznie.",
      sem_cap=True),
    li("Co ten wykres pomija",
       ["oplata za zarzadzanie", "podatek od zysku", "kolejnosc obu"],
       "Ten film liczy trzy rzeczy. Ile zabiera roczna oplata za zarzadzanie. "
       "Ile zabiera podatek od zysku. I dlaczego kolejnosc, w jakiej sie je "
       "placi, zmienia wynik bardziej niz sama stawka."),
    i("Zasada calego filmu", "liczby, nie opinie",
      "Nie bede ci mowil, w co inwestowac. Pokaze konkretne liczby i zrodla, a "
      "decyzje podejmiesz sam, znajac koszt."),

    # ---------- 2. oplata, ktorej nie widac ----------
    t("PIERWSZY UBYTEK", "oplata za zarzadzanie",
      "Zacznijmy od oplaty za zarzadzanie. To procent, ktory fundusz pobiera co "
      "roku od calego twojego kapitalu — nie od zysku, od calosci.",
      cap="Oplata, ktorej nie widac"),
    i("Od czego jest liczona", "od calego kapitalu",
      "Ta roznica jest wieksza, niz brzmi. Podatek placisz od zysku, wiec w "
      "zlym roku placisz mniej. Oplate placisz zawsze, takze w roku, w ktorym "
      "stracilies."),
    i("Gdzie ja widzisz", "nigdzie",
      "I nie zobaczysz jej na zadnym przelewie. Jest juz odjeta w wycenie "
      "jednostki, ktora ogladasz. Rachunek pokazuje ci kwote po oplacie i "
      "wyglada to jak twoj prawdziwy stan."),
    b("Gorny limit oplaty w Polsce",
      ["dwa tysiace dziewietnascie", "dwa tysiace dwadziescia jeden",
       "od dwa tysiace dwudziestego drugiego"],
      [35, 25, 20],
      "Panstwo uznalo, ze bylo za drogo, i limit obnizano etapami. W dwa "
      "tysiace dziewietnastym roku gorna granica wynosila trzy i pol procent. W "
      "dwa tysiace dwudziestym pierwszym dwa i pol. Od pierwszego stycznia dwa "
      "tysiace dwudziestego drugiego roku maksimum to dwa procent wartosci "
      "aktywow w skali roku."),
    i("Zrodlo tej liczby", "rozporzadzenie ministra",
      "To nie jest branzowa plotka. Limit ustanowilo rozporzadzenie ministra "
      "finansow, a obnizke kosztow polskich funduszy opisaly niezaleznie "
      "Analizy kropka pl i Stowarzyszenie Inwestorow Indywidualnych."),
    i("Dlaczego to zrobiono", "bylismy powyzej sredniej",
      "Powod podano wprost. Koszty inwestowania w Polsce byly znaczaco wyzsze "
      "od sredniej europejskiej, a roznice place uczestnik, nie fundusz."),
    t("UWAGA NA SLOWO MAKSIMUM", "limit to sufit, nie cena",
      "Tylko uwazaj na slowo maksimum. Dwa procent to sufit ustawowy, a nie "
      "cena, ktora musisz zaplacic. Sa produkty za znacznie mniej i to ty "
      "wybierasz, ktory bierzesz.",
      sem_cap=True),
    li("Co sklada sie na twoj koszt",
       ["oplata za zarzadzanie", "oplata zmienna za wynik",
        "koszty transakcyjne"],
       "I jeszcze jedno: sama oplata za zarzadzanie to nie caly koszt. Do niej "
       "dochodzi oplata zmienna za wynik oraz koszty transakcyjne funduszu. "
       "Dlatego porownuj sume kosztow rocznych, a nie jedna pozycje."),
    i("Zmiana od tego roku", "piec lat zamiast jednego",
      "Oplata zmienna wlasnie zmienila zasady. W dwa tysiace dwudziestym drugim "
      "roku fundusz musial pobic swoj punkt odniesienia w ciagu jednego roku, "
      "zeby ja pobrac. Od tego roku liczy sie okres pieciu lat."),
    i("Co to dla ciebie znaczy", "trudniej o premie",
      "To zmiana na twoja korzysc. Jeden dobry rok po czterech slabych przestaje "
      "wystarczac do premii dla zarzadzajacego."),
    t("DWA PROCENT", "brzmi jak nic",
      "Dwa procent rocznie brzmi jak zaokraglenie. Zaraz zobaczysz, co dwa "
      "procent robia przez trzydziesci lat z twoimi dwustu zlotymi.",
      sem_cap=True),

    # ---------- 3. co robi dwa procent przez trzydziesci lat ----------
    t("TA SAMA WPLATA", "dwa rachunki, jedna roznica",
      "Bierzemy dwa identyczne rachunki. Ta sama wplata dwustu zlotych, ten sam "
      "okres trzydziestu lat, ta sama stopa zwrotu piec procent. Rozni je tylko "
      "oplata.",
      cap="Co robia dwa procent"),
    b("Kapital po trzydziestu latach",
      ["bez oplaty", "przy jednym procencie", "przy dwoch procentach"],
      [166, 139, 117],
      "Bez oplaty konczysz z okolo stu szescdziesiecioma szescioma tysiacami "
      "zlotych. Przy jednym procencie rocznie zostaje okolo stu trzydziestu "
      "dziewieciu tysiecy. Przy dwoch procentach — okolo stu siedemnastu tysiecy."),
    i("Roznica miedzy skrajnymi", "piecdziesiat tysiecy",
      "Miedzy rachunkiem bez oplaty a rachunkiem z dwoma procentami jest okolo "
      "piecdziesieciu tysiecy zlotych roznicy. To wiecej niz dwie trzecie "
      "wszystkiego, co sam wplaciles."),
    i("Ile to twoich wplat", "dwadziescia jeden lat",
      "Sprobuj przelozyc to na przelewy. Piecdziesiat tysiecy przy wplacie "
      "dwustu zlotych to dwiescie piecdziesiat miesiecy oszczedzania — ponad "
      "dwadziescia lat przelewow, ktore poszly na oplate."),
    t("DLACZEGO TAK DUZO", "oplata tez sie sklada",
      "Powod jest ten sam, dla ktorego twoj kapital rosnie. Procent skladany "
      "dziala w obie strony: to, co fundusz zabral w piatym roku, nie pracuje "
      "przez pozostalych dwadziescia piec lat.",
      sem_cap=True),
    i("Rok pierwszy", "prawie nic",
      "W pierwszym roku dwa procent od malego kapitalu to kilkadziesiat "
      "zlotych. Nie czujesz tego i dlatego nie reagujesz."),
    i("Rok trzydziesty", "ponad dwa tysiace",
      "W trzydziestym roku te same dwa procent liczone sa juz od stu "
      "kilkunastu tysiecy i kosztuja ponad dwa tysiace zlotych rocznie. Stawka "
      "sie nie zmienila, zmienila sie podstawa."),
    i("Sprawdzmy to na polowie drogi", "po pietnastu latach",
      "Zobaczmy jeszcze polowe drogi. Po pietnastu latach roznica miedzy "
      "rachunkiem bez oplaty a rachunkiem z dwoma procentami to okolo osmiu "
      "tysiecy zlotych. Wydaje sie do zniesienia."),
    i("A w drugiej polowie", "czterdziesci dwa tysiace",
      "Cala reszta, czyli okolo czterdziestu dwoch tysiecy, narasta w drugiej "
      "polowie. Koszt oplaty nie rozklada sie rowno w czasie — czeka na koniec, "
      "kiedy juz nie mozesz go cofnac."),
    t("STAD BIERZE SIE BLAD", "wczesnie nie boli",
      "Stad bierze sie najczestszy blad. Oceniasz produkt po pierwszych latach, "
      "kiedy oplata jest niewidoczna, i zostajesz w nim na trzydziesci.",
      sem_cap=True),
    li("Co z tego wynika",
       ["oplata rosnie z kapitalem", "placisz ja takze na stracie",
        "sprawdzasz ja raz"],
       "Trzy wnioski. Oplata rosnie razem z twoim kapitalem. Placisz ja rowniez "
       "w latach stratnych. I sprawdzasz ja raz, przy wyborze produktu, a skutki "
       "ponosisz przez trzydziesci lat."),

    # ---------- 4. podatek Belki ----------
    t("DRUGI UBYTEK", "podatek od zysku",
      "Teraz drugi ubytek. Od zysku kapitalowego w Polsce placi sie "
      "dziewietnascie procent — potocznie podatek Belki.",
      cap="Podatek od zysku"),
    i("Od czego jest liczony", "tylko od zysku",
      "Tu podstawa jest inna niz przy oplacie. Dziewietnascie procent liczy sie "
      "od zysku, a nie od calego kapitalu. Wlasnych wplat nikt nie opodatkowuje "
      "drugi raz."),
    i("Kiedy sie go placi", "przy sprzedazy",
      "Placisz go w momencie sprzedazy. Dopoki nie sprzedajesz, podatek nie "
      "istnieje na twoim rachunku — i to jest wazniejsze, niz wyglada."),
    b("Sto szesnascie tysiecy po podatku",
      ["twoje wplaty", "zysk przed podatkiem", "zysk po podatku"],
      [72, 44, 36],
      "Wroc do rachunku z dwoma procentami oplaty. Ze stu szesnastu tysiecy "
      "siedemdziesiat dwa tysiace to twoje wlasne wplaty, a okolo czterdziestu "
      "czterech tysiecy to zysk. Dziewietnascie procent od tego zysku to okolo "
      "osmiu tysiecy czterystu zlotych podatku."),
    i("Zostaje ci", "okolo stu osmiu tysiecy",
      "Po podatku zostaje okolo stu osmiu tysiecy zlotych. Zaczynalismy od stu "
      "szescdziesieciu czterech na wykresie sprzedawcy."),
    li("Czego podatek nie zabiera",
       ["wlasnych wplat", "zysku, ktorego nie zrealizowales",
        "straty, ktora odliczysz"],
       "Warto wiedziec, czego podatek nie dotyka. Nie dotyka twoich wlasnych "
       "wplat. Nie dotyka zysku, dopoki nie sprzedasz. A strate z jednego roku "
       "mozesz rozliczyc z zyskiem w kolejnych latach."),
    i("Praktyczny wniosek", "kazda sprzedaz kosztuje",
      "Praktycznie wynika z tego jedno. Kazde przelozenie pieniedzy z produktu "
      "do produktu realizuje zysk i uruchamia podatek, ktory do tej pory "
      "pracowal dla ciebie."),
    i("Dlatego czesta zmiana boli", "podatek plus oplata",
      "Dlatego czesta zmiana funduszu kosztuje podwojnie: placisz podatek "
      "wczesniej, niz musiales, i zwykle wchodzisz w kolejna oplate."),
    t("PODSUMOWANIE POLOWY", "piecdziesiat szesc tysiecy",
      "Oplata i podatek razem zabraly okolo piecdziesieciu szesciu tysiecy "
      "zlotych z tego samego planu, tej samej wplaty i tej samej stopy zwrotu.",
      sem_cap=True),

    # ---------- 5. kolejnosc ma znaczenie ----------
    t("TERAZ WAZNE", "kolejnosc, nie stawka",
      "I tu dochodzimy do rzeczy, ktora zmienia wynik bardziej niz sama stawka: "
      "kolejnosc, w jakiej te dwa koszty sie pojawiaja.",
      cap="Kolejnosc ma znaczenie"),
    i("Oplata", "co roku",
      "Oplate placisz co roku, z kapitalu, ktory mial pracowac. Zabrana zlotowka "
      "nigdy juz nie zarobi."),
    i("Podatek", "raz, na koncu",
      "Podatek placisz raz, przy wyplacie, od zysku, ktory juz sie zdarzyl. Do "
      "tego momentu cala kwota pracuje dla ciebie."),
    li("Dlaczego to nie to samo",
       ["oplata rozklada sie na trzydziesci lat",
        "podatek spada raz na koncu",
        "tylko jedno z tego zatrzymuje wzrost"],
       "Dlatego dwa procent oplaty rocznie kosztuja cie wiecej niz "
       "dziewietnascie procent podatku jednorazowo. Procent zabierany co roku "
       "wycina takze przyszly wzrost. Podatek zabiera plaster z tortu, ktory juz "
       "urosl."),
    b("Ile kosztuje kazdy z nich",
      ["oplata przez trzydziesci lat", "podatek raz na koncu"],
      [50, 8],
      "Zestawmy to wprost. Oplata dwuprocentowa zabrala okolo piecdziesieciu "
      "tysiecy zlotych. Podatek zabral okolo osmiu i pol tysiaca. Stawka "
      "podatku jest prawie dziesiec razy wyzsza, a kosztuje szesc razy mniej."),
    i("Skad ta odwrotnosc", "z czasu, nie ze stawki",
      "Ta odwrotnosc nie bierze sie ze stawek, tylko z czasu. Oplata dziala "
      "trzysta szescdziesiat razy, podatek jeden raz."),
    i("Wniosek praktyczny", "najpierw oplata",
      "Praktycznie znaczy to tyle: jesli masz porownac dwa produkty, najpierw "
      "porownaj oplate roczna, a dopiero potem zastanawiaj sie nad podatkiem."),
    t("I JESZCZE JEDNO", "to dziala tez w druga strone",
      "I zapamietaj, ze to dziala tez w druga strone. Kazdy obnizony punkt "
      "procentowy oplaty pracuje dla ciebie przez wszystkie trzydziesci lat, "
      "bez zadnego ryzyka.",
      sem_cap=True),

    # ---------- 6. co panstwo daje za darmo ----------
    t("JEST OBEJSCIE", "i jest legalne",
      "Na podatek istnieje legalne obejscie, wpisane w ustawe. Nazywa sie IKE i "
      "IKZE, i wiekszosc ludzi go nie uzywa.",
      cap="Co panstwo daje"),
    i("IKE — limit na rok", "dwadziescia osiem tysiecy",
      "Limit wplat na indywidualne konto emerytalne w dwa tysiace dwudziestym "
      "szostym roku wynosi dwadziescia osiem tysiecy dwiescie szescdziesiat "
      "zlotych. Ta kwota pochodzi z obwieszczenia ministra rodziny z "
      "siedemnastego listopada dwa tysiace dwudziestego piatego roku."),
    i("Co daje IKE", "zero podatku po szescdziesiatce",
      "Po ukonczeniu szescdziesiatego roku zycia wyplata z IKE jest wolna od "
      "podatku od zysku. Nie odroczona — zwolniona."),
    i("IKZE — limit na rok", "jedenascie tysiecy trzysta cztery",
      "Limit na indywidualne konto zabezpieczenia emerytalnego to jedenascie "
      "tysiecy trzysta cztery zlote. Kto prowadzi dzialalnosc gospodarcza, ma "
      "szesnascie tysiecy dziewiecset piecdziesiat szesc."),
    b("Zwrot z PIT za wplate na IKZE",
      ["prog dwunastoprocentowy", "prog trzydziestodwuprocentowy"],
      [1356, 3617],
      "IKZE dziala inaczej niz IKE: wplate odliczasz od dochodu w tym samym "
      "roku. Przy pierwszym progu podatkowym to okolo tysiaca trzystu "
      "piecdziesieciu szesciu zlotych zwrotu, przy drugim okolo trzech tysiecy "
      "szesciuset siedemnastu."),
    i("Koszt IKZE na koncu", "dziesiec procent",
      "Za to przy wyplacie po szescdziesiatym piatym roku zycia placisz "
      "dziesiecioprocentowy ryczalt. Dziesiec procent zamiast dziewietnastu, i "
      "to od kwoty, ktora rosla bez podatku po drodze."),
    li("Warunek, o ktorym sie zapomina",
       ["wplaty w pieciu latach kalendarzowych",
        "szescdziesiat lat przy IKE",
        "szescdziesiat piec lat przy IKZE"],
       "Oba konta maja ten sam warunek wstepny: wplaty w co najmniej pieciu "
       "roznych latach kalendarzowych. Dlatego male konto zalozone dzisiaj jest "
       "warte wiecej niz duze konto zalozone za cztery lata."),
    i("Twoje dwiescie zlotych", "miesci sie z zapasem",
      "Twoje dwiescie zlotych miesiecznie to dwa tysiace czterysta zlotych "
      "rocznie. To okolo dziewieciu procent limitu IKE. Limit nie jest twoim "
      "problemem."),
    t("KTORE WYBRAC", "to zalezy od jednej liczby",
      "Zostaje pytanie, ktore z dwoch kont wybrac. Odpowiedz zalezy od jednej "
      "liczby: twojego progu podatkowego dzisiaj.",
      sem_cap=True),
    i("Jesli jestes w drugim progu", "IKZE zwraca wiecej",
      "Jesli placisz trzydziesci dwa procent, IKZE oddaje ci co roku okolo "
      "trzech tysiecy szesciuset siedemnastu zlotych, a przy wyplacie zabiera "
      "dziesiec. Kupujesz roznice dwudziestu dwoch punktow procentowych."),
    i("Jesli jestes w pierwszym progu", "IKE bywa prostsze",
      "Jesli placisz dwanascie procent, zwrot jest mniejszy, a IKE ma te "
      "przewage, ze na koncu nie placisz nic i nie musisz czekac do "
      "szescdziesiatego piatego roku zycia."),
    li("Trzy roznice do zapamietania",
       ["ulga teraz albo zero na koncu", "szescdziesiat albo szescdziesiat piec",
        "limit wiekszy albo mniejszy"],
       "Trzy roznice wystarczy zapamietac. IKZE daje ulge teraz, IKE daje zero "
       "podatku na koncu. IKE od szescdziesiatki, IKZE od szescdziesiatego "
       "piatego roku. I limit IKE jest ponad dwa i pol raza wiekszy."),
    i("Nie musisz wybierac", "mozesz miec oba",
      "I nie musisz wybierac jednego. Ustawa pozwala miec oba konta naraz, a "
      "limity licza sie osobno."),
    i("A jesli bede musial wyplacic", "zwrot jest mozliwy",
      "Czesta obawa brzmi: a jesli bede potrzebowal tych pieniedzy wczesniej. "
      "Mozesz je wyplacic w kazdej chwili — tracisz wtedy tylko preferencje "
      "podatkowa, nie same pieniadze."),

    # ---------- 7. ta sama wplata, trzy scenariusze ----------
    t("TRZY RACHUNKI", "ta sama wplata, trzy wyniki",
      "Policzmy teraz to samo dwiescie zlotych w trzech wariantach, przez te "
      "same trzydziesci lat.",
      cap="Trzy rachunki"),
    b("Ile zostaje w kieszeni",
      ["dwa procent i podatek", "pol procent i podatek",
       "pol procent w IKE"],
      [108, 137, 151],
      "Wariant pierwszy, dwa procent oplaty i podatek na koncu: okolo stu osmiu "
      "tysiecy. Wariant drugi, tani produkt za pol procenta i ten sam podatek: "
      "okolo stu trzydziestu siedmiu tysiecy. Wariant trzeci, ten sam tani "
      "produkt wewnatrz IKE: okolo stu piecdziesieciu jeden tysiecy."),
    i("Roznica pierwsza", "sama oplata",
      "Miedzy pierwszym a drugim wariantem jest okolo dwudziestu dziewieciu "
      "tysiecy zlotych, i cala ta roznica bierze sie z jednej decyzji — z "
      "wyboru taniego produktu."),
    i("Roznica druga", "sam rachunek",
      "Miedzy drugim a trzecim jest okolo pietnastu tysiecy, i tu decyzja jest "
      "jeszcze prostsza: ten sam produkt, tylko trzymany na koncie IKE zamiast "
      "na zwyklym."),
    i("Razem", "czterdziesci cztery tysiace",
      "Razem dwie decyzje, ktore nie wymagaja przewidzenia rynku, warte okolo "
      "czterdziestu czterech tysiecy zlotych."),
    t("CZEGO TU NIE MA", "zadnej prognozy",
      "Zwroc uwage, czego w tej liczbie nie ma. Nie ma trafienia w dobra spolke "
      "ani przewidzenia kryzysu. Stopa zwrotu byla taka sama we wszystkich "
      "trzech wariantach.",
      sem_cap=True),

    # ---------- 8. co z tym zrobic ----------
    t("CO SPRAWDZIC", "cztery liczby",
      "Zostawiam cie z czterema liczbami do sprawdzenia w twoim wlasnym "
      "produkcie.",
      cap="Cztery liczby do sprawdzenia"),
    li("Pierwsza i druga",
       ["laczna oplata roczna", "czy masz IKE"],
       "Pierwsza: laczna oplata roczna twojego produktu, wszystkie skladniki "
       "razem. Druga: czy w ogole masz zalozone IKE albo IKZE, choc na male "
       "kwoty."),
    li("Trzecia i czwarta",
       ["w ilu latach byly wplaty", "twoj prog podatkowy"],
       "Trzecia: w ilu roznych latach kalendarzowych zrobiles juz wplate, bo "
       "licza sie lata, nie kwoty. Czwarta: w ktorym progu podatkowym jestes, "
       "bo to zmienia oplacalnosc IKZE wobec IKE."),
    i("Gdzie szukac oplaty", "kluczowe informacje",
      "Oplate znajdziesz w dokumencie z kluczowymi informacjami dla inwestora. "
      "Szukaj sumy kosztow rocznych, a nie samej oplaty za zarzadzanie."),
    i("Ile to zajmuje", "jedno popoludnie",
      "Sprawdzenie tych czterech liczb zajmuje jedno popoludnie. Skutek "
      "sprawdzenia trwa trzydziesci lat, i widzielismy juz, ile jest wart."),
    t("CZEGO TU NIE PADLO", "zadna nazwa produktu",
      "Zwroc uwage, ze nie padla nazwa zadnego funduszu ani zadnej platformy. "
      "To nie jest przypadek — koszt umiesz policzyc sam, a rekomendacji nie "
      "potrzebujesz.",
      sem_cap=True),
    i("Co zrobic z ta wiedza", "jedna decyzja",
      "Jesli mialbys zrobic tylko jedna rzecz po tym filmie, niech to bedzie "
      "sprawdzenie lacznego kosztu rocznego produktu, ktory juz masz. Reszta "
      "wynika z tej liczby."),
    t("JEDNO ZDANIE", "koszt jest jedyna pewna liczba",
      "Jesli masz zapamietac jedno zdanie, niech to bedzie to: stopy zwrotu nie "
      "znasz, a koszt znasz dzisiaj, co do drugiego miejsca po przecinku.",
      sem_cap=True),
    cta("KOLEJNY POZIOM", "sprawdz swoja oplate w ten weekend",
        "Sprawdz swoja oplate w ten weekend, zanim zrobisz kolejny przelew. "
        "Jesli takie liczenie ma dla ciebie sens, zasubskrybuj kanal."),
]

SHORT = [
    {"layout": "titulo", "kicker": "DWA PROCENT",
     "sub": "piecdziesiat tysiecy mniej",
     "nar": "Dwa procent oplaty rocznie kosztuja cie piecdziesiat tysiecy zlotych "
            "przez trzydziesci lat."},
    {"layout": "item", "kicker": "Ta sama wplata", "preco": "dwiescie zlotych",
     "nar": "Dwiescie zlotych miesiecznie, trzydziesci lat, piec procent zwrotu."},
    {"layout": "barras", "kicker": "Kapital po trzydziestu latach",
     "itens": ["bez oplaty", "przy dwoch procentach"], "alturas": [166, 117],
     "nar": "Bez oplaty sto szescdziesiat szesc tysiecy. Przy dwoch procentach "
            "sto siedemnascie."},
    {"layout": "item", "kicker": "To twoje przelewy", "preco": "dwadziescia jeden lat",
     "nar": "Ta roznica to ponad dwadziescia lat twoich wlasnych przelewow."},
    {"layout": "item", "kicker": "Dlaczego tyle", "preco": "oplata tez sie sklada",
     "nar": "Powod jest prosty. To, co fundusz zabral w piatym roku, nie pracuje "
            "przez pozostalych dwadziescia piec."},
    {"layout": "cta", "kicker": "PELNA KONCOWKA", "sub": "razem z podatkiem i IKE",
     "nar": "Cala konta, razem z podatkiem i kontem IKE, jest w dlugim filmie na "
            "kanale."},
]

COPY = """# Oplaty i podatek: ile ubywa z dwustu zlotych miesiecznie

## TYTUL
Oplaty i podatek Belki: ile zjadaja z 200 zl miesiecznie przez 30 lat

## OPIS
Odkladasz 200 zl miesiecznie przez 30 lat. Wykres przy podpisywaniu umowy
pokazuje okolo 166 tys. zl. W kieszeni zostaje okolo 108 tys. Ten film pokazuje,
gdzie znika reszta — i ile z tego mozesz zatrzymac bez zmiany stopy zwrotu.

Liczby, ktore padaja w filmie:

• Gorny limit oplaty za zarzadzanie w Polsce to 2% wartosci aktywow rocznie, od
1 stycznia 2022 r. Wczesniej bylo 3,5% (2019), 3% (2020) i 2,5% (2021). Limit
ustanowilo rozporzadzenie Ministra Finansow.

• Przy tej samej wplacie i tej samej stopie zwrotu roznica miedzy rachunkiem bez
oplaty a rachunkiem z 2% oplaty rocznej wynosi okolo 50 tys. zl — wiecej niz
dwie trzecie wszystkiego, co sam wplaciles.

• Podatek od zysku kapitalowego wynosi 19% i liczony jest od zysku, nie od
calego kapitalu. Placisz go dopiero przy sprzedazy.

• Limit wplat na IKE w 2026 r. to 28 260 zl (obwieszczenie MRPiPS z 17 listopada
2025 r.). Limit na IKZE to 11 304 zl, a przy dzialalnosci gospodarczej 16 956 zl.

• Wplata na IKZE daje odliczenie od dochodu: okolo 1 356 zl zwrotu przy progu
12% i okolo 3 617 zl przy progu 32%. Wyplata z IKZE po 65. roku zycia jest
opodatkowana ryczaltem 10% zamiast 19%.

• Oba konta wymagaja wplat w co najmniej pieciu roznych latach kalendarzowych.
Dlatego male konto zalozone dzisiaj bywa warte wiecej niz duze zalozone pozniej.

Glowna mysl filmu dotyczy kolejnosci, a nie stawki. Oplata pobierana jest co
roku z kapitalu, ktory mial pracowac, wiec wycina takze przyszly wzrost. Podatek
pobierany jest raz, na koncu, od zysku, ktory juz sie zdarzyl. Dlatego 2%
rocznie kosztuje wiecej niz 19% jednorazowo — i dlatego przy porownywaniu
produktow oplata jest pierwsza liczba do sprawdzenia, a nie ostatnia.

Na koncu sa cztery liczby do sprawdzenia we wlasnym produkcie: laczna oplata
roczna, czy masz zalozone IKE lub IKZE, w ilu latach kalendarzowych byly juz
wplaty, i w ktorym progu podatkowym jestes.

To nie jest doradztwo inwestycyjne ani rekomendacja konkretnego produktu. To
rachunek, ktory mozesz powtorzyc na wlasnych danych.

Jesli takie liczenie ma dla ciebie sens, zasubskrybuj kanal.

## ROZDZIALY
{CAPITULOS}

## KOMENTARZ
Cztery liczby do sprawdzenia w ten weekend: 1) laczna oplata roczna twojego
produktu, 2) czy masz zalozone IKE albo IKZE, 3) w ilu roznych latach
kalendarzowych zrobiles juz wplate, 4) w ktorym progu podatkowym jestes. Napisz
w komentarzu, ktora z nich cie zaskoczyla.

## HASHTAGI
#finanseosobiste #IKE #oszczedzanie

## TAGI
oplata za zarzadzanie, podatek Belki, IKE, IKZE, limity IKE 2026, finanse osobiste, oszczedzanie na emeryture, procent skladany, fundusze inwestycyjne, koszty inwestowania, ulga podatkowa, inwestowanie dla poczatkujacych, 200 zl miesiecznie, emerytura, TFI

## USTAWIENIA STUDIO
Kategoria 27 (Edukacja). Jezyk polski, sciezka dzwiekowa polska. Nie dla dzieci.
Zawiera tresci syntetyczne — zadeklarowane przy publikacji. Napisy z pliku SRT.

## MUZYKA / LICENCJA
Wholesome — YouTube Audio Library, bez obowiazku oznaczania autorstwa. Poziom
minus dwadziescia osiem decybeli wzgledem narracji.

## ZRODLA
Obwieszczenie MRPiPS z 17.11.2025 (limit IKE 2026, Monitor Polski) i z
10.11.2025 (limit IKZE 2026). Rozporzadzenie Ministra Finansow w sprawie
maksymalnej wysokosci wynagrodzenia stalego towarzystwa za zarzadzanie
funduszem. Analizy.pl oraz Stowarzyszenie Inwestorow Indywidualnych — przebieg
obnizki limitu z 3,5% do 2%.
"""

TAGS = [
    "oplata za zarzadzanie", "podatek Belki", "IKE", "IKZE",
    "limity IKE 2026", "finanse osobiste", "oszczedzanie na emeryture",
    "procent skladany", "fundusze inwestycyjne", "koszty inwestowania",
    "ulga podatkowa", "inwestowanie dla poczatkujacych",
    "200 zl miesiecznie", "emerytura", "TFI",
]

SPEC = {
    "slug": SLUG,
    "pacote": PACOTE,
    "voz": "pl-PL-MarekNeural",
    "idioma": "pl",
    "trilha": "Wholesome",
    "paleta": PALETA,
    "thumb": {"l1": "2% ROCZNIE", "l2": "50 TYS. MNIEJ"},
    "longo": LONGO,
    "short": SHORT,
    "copy": COPY,
    "tags": TAGS,
    "fonte_pauta": "W co inwestowac 200 zl miesiecznie? KONKRETY (5755,7 v/d)",
}


def _conta(wplata=200.0, anos=30, bruto=0.05, oplata=0.0):
    """Juros compostos mensais, capital ao fim. E a conta que o video narra.

    Vive aqui e nao num comentario para que qualquer um possa refaze-la: a
    rotina exige numero verificavel, e numero narrado nao se confere de ouvido.
    """
    r = (bruto - oplata) / 12
    n = anos * 12
    return wplata * (((1 + r) ** n - 1) / r)


if __name__ == "__main__":
    sem = _conta()
    um = _conta(oplata=0.01)
    dois = _conta(oplata=0.02)
    meio = _conta(oplata=0.005)
    aporte = 200.0 * 30 * 12
    liq = lambda c: aporte + (c - aporte) * 0.81
    print(f"  sem oplata      {sem:10,.0f}")
    print(f"  1%              {um:10,.0f}")
    print(f"  2%              {dois:10,.0f}   diferenca p/ sem: {sem-dois:,.0f}")
    print(f"  0,5%            {meio:10,.0f}")
    print(f"  2% liquido      {liq(dois):10,.0f}")
    print(f"  0,5% liquido    {liq(meio):10,.0f}")
    print(f"  0,5% em IKE     {meio:10,.0f}")

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           f"{PACOTE}.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{destino}: {len(LONGO)} cenas, short {len(SHORT)}")
