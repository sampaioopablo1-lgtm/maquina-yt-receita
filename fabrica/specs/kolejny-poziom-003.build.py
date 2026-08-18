#!/usr/bin/env python3
"""Reconstroi a spec kolejny-poziom-003 — de parada a publicavel.

HISTORIA: a -003 (IKE vs IKZE) ficou no inventario PARADAS por dois motivos
medidos: copy em bilhete de 49 chars ("gerado a partir dos capitulos reais
apos o render") que o publicar.py aborta, e 16,6 min no Marek recalibrado
(19,93 chars/s + 1,477 s/frase, n=74) — acima do teto de 15. O roteiro em si
estava certo: os limites de 2026 conferem (IKE 28.260 = 3x 9.420; IKZE
11.304 = 1,2x; JDG 16.956 = 1,8x; ano anterior 26.019/10.407,60 bate),
confirmados em 18/08/2026 por Analizy.pl, BDO e PZU. Progi 12%/32% em
120.000 zl, ryczalt 10%, Belka 19% — tudo vigente.

O CONSERTO (aprendizado 297: spec parada e o pacote mais barato):
  * 88 -> 74 cenas: cairam transicoes puras (21, 32, 43, 54, 65, 76), o
    hedge duplicado (5, 7, 75), a comparacao com o ano anterior (16, 17),
    redundancias (31 repete 30; 45 repete 9; 42 se auto-anula) e uma
    obviedade (74 dobrada em 73).
  * ~14.500 -> ~10.600 chars com apara nas cenas mais longas, mirando o
    MEIO da janela (aprendizado 302: voz com agregado de um pacote so tem
    ruido de ±5% — alvo 13,0-13,5 min, nunca a borda).
  * copy completa em polones (era o bilhete).
  * short [s4] deixou de ser trailer: agora entrega o werdykt inteiro e
    aponta o longo como continuacao opcional (regra "short que so aponta
    para o longo e trailer, nao short").

PAUTA (banco, medicao de 11/08, mediana do nicho 88,3 v/d): IKE/IKZE e o
eixo de otimizacao fiscal do terceiro filar — evergreen anual, validade ate
dezembro/2026. O canal esta a UM longo da meta de dez (9/10); este pacote
fecha a meta.

SIMILARIDADE vs publicados do canal: Emerytura z ZUS 34,4% / Oplaty i
podatek Belki / Nadplacac kredyt czy inwestowac / Jak ulozyc finanse 9233 zl
— eixo IKE/IKZE inedito no canal (conferido em videos por titulo, 18/08).
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


# ---------------------------------------------------------------- cap 1
T("IKE czy IKZE", "zle postawione pytanie",
  "Prawie kazdy material na ten temat konczy sie zdaniem: to zalezy od "
  "twojej sytuacji. Prawdziwe i bezuzyteczne, bo nie mowi od czego zalezy.",
  cap="Pytanie postawione odwrotnie")
I("Zalezy", "od jednej liczby",
  "A zalezy od jednej liczby: twojego progu podatkowego. Oplaty, fundusze i "
  "wygoda aplikacji sa przy niej drugorzedne.")
T("Dwa konta", "ta sama ulga, inny moment",
  "Oba konta daja ulge podatkowa i sluza temu samemu celowi. Roznia sie "
  "momentem: jedno oddaje pieniadze juz w przyszlym roku, drugie po "
  "kilkudziesieciu latach.")
I("IKZE", "ulga teraz",
  "Wplata na indywidualne konto zabezpieczenia emerytalnego zmniejsza "
  "podstawe opodatkowania za biezacy rok. Czesc kwoty wraca przelewem z "
  "urzedu skarbowego wiosna.")
I("IKE", "zero potem",
  "Wplata na indywidualne konto emerytalne nie daje dzis nic. Za to wyplata "
  "po szescdziesiatce jest wolna od podatku od zyskow — calkowicie, nie "
  "czesciowo.")
L("Co policzymy", ["Limity wplat", "Ulga w pierwszym progu",
                   "Ulga w drugim progu", "Warunek, ktory wszystko zmienia"],
  "Policzymy po kolei cztery rzeczy: aktualne limity wplat, realna wartosc "
  "ulgi w pierwszym progu, te sama wartosc w drugim, oraz warunek, bez "
  "ktorego przewaga IKZE znika.")
I("Uczciwe zastrzezenie", "to nie porada",
  "Uczciwe zastrzezenie na wstepie: to nie jest porada inwestycyjna ani "
  "podatkowa. To arytmetyka na publicznych stawkach, ktora sprawdzisz "
  "samodzielnie w kwadrans.")
I("Zalozenie", "te same aktywa",
  "Zakladamy przez caly material, ze w obu kontach trzymasz te same aktywa "
  "i wplacasz te same kwoty. Porownujemy opakowania podatkowe, nie "
  "strategie.")
T("Zacznijmy", "od skali",
  "Zacznijmy od pytania najbardziej praktycznego: ile w ogole mozesz "
  "wplacic w tym roku. To wyznacza skale calej reszty.")

# ---------------------------------------------------------------- cap 2
T("Limity", "wynikaja z prognozy plac",
  "Limity wplat nie sa negocjowane co roku. Wynikaja z prognozowanego "
  "przecietnego wynagrodzenia, ktore na ten rok wynosi dziewiec tysiecy "
  "czterysta dwadziescia zlotych miesiecznie.",
  cap="Limity na ten rok")
I("IKE", "trzykrotnosc podstawy",
  "Limit na IKE to trzykrotnosc tej kwoty, czyli dwadziescia osiem tysiecy "
  "dwiescie szescdziesiat zlotych na osobe rocznie. Malzonkowie maja po "
  "tyle samo, kazde osobno.")
I("IKZE na etacie", "jeden i dwie dziesiate",
  "Limit na IKZE przy umowie o prace to jeden i dwie dziesiate tej "
  "podstawy, czyli jedenascie tysiecy trzysta cztery zlote. Niecala polowa "
  "tego, co miesci IKE.")
I("IKZE na dzialalnosci", "mnoznik wyzszy",
  "Przy dzialalnosci gospodarczej mnoznik to jeden i osiem dziesiatych, "
  "czyli szesnascie tysiecy dziewiecset piecdziesiat szesc zlotych. Ta "
  "roznica wroci w werdykcie.")
B("Limity roczne", ["IKE", "IKZE etat", "IKZE JDG"], [100, 40, 60],
  "Proporcje wygladaja tak: IKE daje prawie trzy razy wiecej miejsca niz "
  "IKZE na etacie, a samozatrudniony miesci na IKZE okolo polowy IKE.")
I("Rok temu", "limity byly nizsze",
  "Rok wczesniej limity byly zauwazalnie nizsze. To nie hojnosc panstwa, "
  "tylko mechaniczne przeliczenie prognozy plac: place rosna, limity rosna "
  "razem z nimi.")
I("Oba naraz", "bez wykluczenia",
  "Mozesz prowadzic oba konta jednoczesnie. Na etacie to razem prawie "
  "czterdziesci tysiecy zlotych rocznie, na dzialalnosci ponad czterdziesci "
  "piec tysiecy.")
I("Limit sie nie kumuluje", "grudzien kasuje",
  "I rzecz, ktora zaskakuje najwiecej osob: limit nie przechodzi na kolejny "
  "rok. Czego nie wplacisz do konca grudnia, przepada bezpowrotnie.")
I("Wniosek praktyczny", "styczen bije grudzien",
  "Dlatego ta sama decyzja podjeta w grudniu jest gorsza niz w styczniu. "
  "Zostaje mniej miesiecy na rozlozenie wplaty i mniej czasu pracy "
  "pieniedzy.")

# ---------------------------------------------------------------- cap 3
T("Mechanika IKZE", "odliczenie od podstawy",
  "IKZE odlicza sie od podstawy opodatkowania, nie od samego podatku. "
  "Brzmi jak formalnosc, a przesadza o tym, ile realnie odzyskujesz.",
  cap="IKZE: ulga teraz, podatek potem")
I("Skutek", "zwrot rowny stawce",
  "Kiedy odliczasz od podstawy, wartosc odliczenia jest rowna twojej "
  "stawce podatkowej. Ta sama wplata daje wiec rozny zwrot roznym osobom.")
I("Pierwszy prog", "dwanascie procent",
  "W pierwszym progu, do stu dwudziestu tysiecy zlotych dochodu rocznie, "
  "stawka wynosi dwanascie procent. Zlotowka wplacona wraca jako dwanascie "
  "groszy zwrotu.")
I("Drugi prog", "trzydziesci dwa procent",
  "Powyzej progu stawka rosnie do trzydziestu dwoch procent. Ta sama "
  "zlotowka zwraca trzydziesci dwa grosze — prawie trzy razy wiecej za te "
  "sama czynnosc.")
I("Pelny limit na etacie", "zwrot w pierwszym progu",
  "Na pelnym limicie: jedenascie tysiecy trzysta cztery zlote wplacone w "
  "pierwszym progu daja okolo tysiaca trzystu piecdziesieciu szesciu "
  "zlotych zwrotu.")
I("Ta sama wplata", "zwrot w drugim progu",
  "Ta sama wplata w drugim progu zwraca okolo trzech tysiecy szesciuset "
  "siedemnastu zlotych. Identyczna kwota na koncie, zupelnie inny przelew "
  "z urzedu.")
I("Zwrot to nie prezent", "to twoj podatek",
  "Warto to nazwac po imieniu: zwrot to nie prezent od panstwa, tylko twoj "
  "wlasny podatek, ktory wraca. Panstwo oddaje dzis, zeby pobrac potem.")
T("Polowa historii", "IKZE tylko przesuwa podatek",
  "To jednak dopiero przyjemniejsza polowa historii. IKZE nie jest "
  "zwolnione z podatku — ono go przesuwa w czasie i zmienia stawke.")
I("Na wyjsciu", "ryczalt dziesiec procent",
  "Przy wyplacie po szescdziesiatym piatym roku zycia placisz ryczalt "
  "dziesiec procent. Mniej niz dziewietnascie procent Belki, ale nie zero.")
I("I tu jest sedno", "od calosci, nie od zysku",
  "I tu jest sedno, ktore przesadza o werdykcie: te dziesiec procent liczy "
  "sie od CALEJ wyplacanej kwoty. Od wplat i zyskow razem, nie od samych "
  "zyskow.")

# ---------------------------------------------------------------- cap 4
T("Mechanika IKE", "nic teraz",
  "IKE nie daje zadnej ulgi na wejsciu. Wplacasz z pieniedzy juz "
  "opodatkowanych i w rozliczeniu rocznym nie zmienia sie nic.",
  cap="IKE: nic teraz, zero potem")
I("Za to na wyjsciu", "zero",
  "Za to na wyjsciu, po szescdziesiatce i przy spelnieniu warunku wplat, "
  "nie placisz nic. Ani podatku Belki, ani ryczaltu.")
I("Zero od calosci", "zysk i kapital twoje",
  "Zero od zysku i zero od kapitalu. Cala wypracowana kwota jest twoja, "
  "niezaleznie od tego, jak duzy zysk urosl przez te lata.")
I("Punkt odniesienia", "Belka na zwyklym rachunku",
  "Punktem odniesienia jest podatek Belki: dziewietnascie procent od "
  "zyskow, ktore zaplacilbys na zwyklym rachunku maklerskim.")
I("Wiek wyplaty", "szescdziesiat kontra szescdziesiat piec",
  "Rozni sie tez wiek: szescdziesiat lat przy IKE, szescdziesiat piec przy "
  "IKZE. Piec lat, ktore przy planowaniu nie sa drobiazgiem.")
T("Elastycznosc", "zasady wczesniejszego wyjscia",
  "Roznia sie tez zasady wczesniejszego wyjscia — argument rzadko "
  "wspominany, a bywa decydujacy.")
I("Wyjscie z IKE", "jak zwykly rachunek",
  "Jesli wycofasz srodki z IKE przed czasem, placisz dziewietnascie "
  "procent od zysku. Jak na zwyklym rachunku, ani grosza wiecej.")
I("Wyjscie z IKZE", "wedlug skali, od calosci",
  "Przy IKZE wczesniejszy zwrot dolicza sie do dochodu i idzie wedlug "
  "skali. Potencjalnie trzydziesci dwa procent, od calej kwoty.")
I("Dziedziczenie", "argument sie znosi",
  "W obu przypadkach srodki sa dziedziczone i nie wchodza do masy "
  "spadkowej na zasadach ogolnych. Ten argument sie wiec znosi i nie "
  "rozstrzyga niczego.")
I("Charakter produktow", "elastyczne kontra sztywne",
  "To zmienia charakter obu produktow. IKE jest elastyczne, IKZE sztywne — "
  "a sztywnosc ma cene, nawet jesli nie widac jej w tabelce.")

# ---------------------------------------------------------------- cap 5
T("Pierwszy prog", "wiekszosc pracujacych",
  "Zaczynamy od osoby w pierwszym progu, z dochodem ponizej stu dwudziestu "
  "tysiecy zlotych rocznie. To zdecydowana wiekszosc pracujacych.",
  cap="Wyliczenie: pierwszy prog")
I("Wariant IKZE", "dwanascie procent teraz",
  "W wariancie IKZE dostajesz zwrot rowny dwunastu procentom wplaty. Przy "
  "pelnym limicie etatowym to okolo tysiaca trzystu piecdziesieciu szesciu "
  "zlotych.")
I("Na wyjsciu", "dziesiec procent calosci",
  "Na wyjsciu oddajesz dziesiec procent calej zgromadzonej kwoty. Nie "
  "wplat — tego, co konto bedzie warte na koncu.")
I("Wariant IKE", "nic i nic",
  "W wariancie IKE nie dostajesz nic na wejsciu i nie oddajesz nic na "
  "wyjsciu. Sto procent koncowej wartosci zostaje u ciebie.")
T("Zderzenie", "dwa punkty na papierze",
  "Zderzmy to wprost. IKZE daje dwanascie procent teraz i zabiera dziesiec "
  "procent calosci potem. IKE nie daje nic i nie zabiera nic.")
I("Bez wzrostu", "dwa punkty roznicy",
  "Gdyby pieniadze w ogole nie pracowaly, przewaga IKZE wynioslaby "
  "dokladnie dwa punkty procentowe. Dwanascie minus dziesiec.")
I("Ale pieniadze pracuja", "ryczalt rosnie z zyskiem",
  "Ale pieniadze pracuja dekadami. Zwrot dostajesz od wplaty, a ryczalt "
  "placisz od wplaty powiekszonej o caly zysk.")
I("Efekt", "przewaga topnieje",
  "Im dluzszy horyzont i wyzsza stopa zwrotu, tym bardziej ta dwupunktowa "
  "przewaga topnieje. Przy dlugim horyzoncie schodzi praktycznie do zera.")
B("Pierwszy prog", ["IKZE", "IKE"], [51, 50],
  "Praktyczny wniosek dla pierwszego progu brzmi zaskakujaco: to jest "
  "remis. Roznica jest za mala, zeby decydowac o wyborze.")

# ---------------------------------------------------------------- cap 6
I("Skoro remis", "decyduja oplaty",
  "A skoro podatkowo jest remis, o wyniku decyduje to, co zwykle: oplaty "
  "instytucji i to, co w koncie trzymasz. Nudne rzeczy wygrywaja.")
T("Drugi prog", "inna arytmetyka",
  "Teraz osoba w drugim progu, z dochodem powyzej stu dwudziestu tysiecy "
  "zlotych. Tu arytmetyka wyglada zupelnie inaczej.",
  cap="Wyliczenie: drugi prog")
I("Zwrot", "trzydziesci dwa procent",
  "Zwrot wynosi trzydziesci dwa procent wplaty. Przy pelnym limicie "
  "etatowym to okolo trzech tysiecy szesciuset siedemnastu zlotych w "
  "jednym rozliczeniu.")
I("Na dzialalnosci", "jeszcze wiecej",
  "Przy dzialalnosci i wyzszym limicie ta sama stawka daje okolo pieciu "
  "tysiecy czterystu dwudziestu szesciu zlotych zwrotu rocznie.")
I("Koszt wyjscia", "bez zmian",
  "A koszt wyjscia sie nie zmienia. Nadal dziesiec procent, bo ryczalt nie "
  "zalezy od progu, w ktorym byles przy wplacaniu.")
T("Asymetria", "wchodzisz drogo, wychodzisz tanio",
  "I to jest cala tajemnica tego produktu. Wchodzisz przy swojej wysokiej "
  "stawce, a wychodzisz przy niskiej, ustalonej z gory.")
I("Roznica stawek", "dwadziescia dwa punkty",
  "Roznica miedzy trzydziestoma dwoma a dziesiecioma procentami to "
  "dwadziescia dwa punkty procentowe. To nie niuans — to cala teza tego "
  "materialu.")
I("Nawet po latach", "przewaga zostaje",
  "I nawet po dekadach wzrostu, kiedy ryczalt obejmie tez zyski, ta "
  "przewaga sie nie zeruje. Zmniejsza sie, ale zostaje wyrazna.")
B("Drugi prog", ["IKZE", "IKE"], [100, 62],
  "W drugim progu IKZE wygrywa wyraznie. To jedyny moment tego porownania, "
  "w ktorym da sie powiedziec cos jednoznacznego.")
I("Kolejnosc", "najpierw IKZE",
  "Dlatego dla osoby w drugim progu kolejnosc jest prosta: najpierw "
  "wypelnij limit IKZE, dopiero nadwyzke kieruj na IKE.")
I("Bo limit IKZE", "wyczerpiesz szybko",
  "Zwlaszcza ze limit IKZE jest niski. Jedenascie tysiecy trzysta cztery "
  "zlote wyczerpiesz szybciej, niz sadzisz, a IKE zostaje na reszte.")

# ---------------------------------------------------------------- cap 7
T("Warunek", "zwrot musi wrocic",
  "Cala przewaga IKZE opiera sie na zalozeniu, ktore prawie nigdy nie pada "
  "na glos: ze otrzymany zwrot podatku rowniez zostanie zainwestowany.",
  cap="Warunek, o ktorym sie nie mowi")
I("Jesli wydasz zwrot", "korzysc znika, koszt zostaje",
  "Jesli zwrot z urzedu wladujesz w wakacje albo telefon, zostaje samo "
  "konto obciazone dziesiecioma procentami przy wyplacie.")
I("Wtedy IKZE przegrywa", "o dziesiec procent calosci",
  "Wtedy IKZE nie tylko nie wygrywa z IKE — ono przegrywa, o cale dziesiec "
  "procent koncowej wartosci konta.")
I("To nie teoria", "pieniadze z nieba",
  "I to nie jest przypadek teoretyczny. Zwrot wplywa wiosna, w glowie jest "
  "oznaczony jako pieniadze z nieba, i bywa wydawany dokladnie tak.")
I("Wniosek techniczny", "zawroc zwrot",
  "Wniosek jest prosty: zwrot z IKZE powinien od razu trafic na IKE albo "
  "na IKZE w kolejnym roku. Bez tego ruchu konstrukcja sie sypie.")
I("Druga pulapka", "prog moze sie zmienic",
  "Druga pulapka dotyczy progu. Liczysz przewage przy trzydziestu dwoch "
  "procentach, ale prog moze sie zmienic ze zmiana pracy albo utrata "
  "premii.")
I("Wtedy wracasz", "do remisu",
  "Jesli spadniesz do pierwszego progu, korzysc z przyszlych wplat wraca "
  "do dwoch punktow, czyli do remisu. Wczesniejsze wplaty zachowuja swoje.")
I("Trzecia rzecz", "stawki to przepisy",
  "I uczciwie: ryczalt dziesiec procent to stawka na dzis, a zero podatku "
  "w IKE to tez tylko przepis. Ryzyko zmiany zasad dotyczy obu kont tak "
  "samo.")

# ---------------------------------------------------------------- cap 8
I("Czwarta rzecz", "musi byc co odliczac",
  "I czwarta rzecz, praktyczna: ulga z IKZE dziala tylko wtedy, gdy masz "
  "od czego ja odliczyc. Bez podatku do zaplacenia w danym roku zwrot nie "
  "ma zrodla.")
T("Werdykt", "dwa zdania",
  "Werdykt brzmi tak. W drugim progu podatkowym IKZE wygrywa wyraznie i "
  "powinno byc pierwsze. W pierwszym progu jest remis, wiec decyduje "
  "elastycznosc.",
  cap="Werdykt i kolejnosc")
I("Pierwszy prog", "wybierz IKE",
  "Konkretnie: w pierwszym progu wybierz IKE. Nie dlatego, ze jest "
  "korzystniejsze podatkowo — przy remisie wygrywa produkt latwiejszy do "
  "opuszczenia.")
I("Drugi prog", "najpierw IKZE, zwrot wraca",
  "W drugim progu wypelnij najpierw IKZE do limitu, nadwyzke kieruj na "
  "IKE. A zwrot podatku potraktuj jak czesc wplaty, nie jak premie.")
I("Dzialalnosc", "kolejnosc jeszcze mocniejsza",
  "Przy dzialalnosci gospodarczej ta kolejnosc jest jeszcze mocniejsza, bo "
  "wyzszy limit IKZE to wiecej pieniedzy odliczonych po wysokiej stawce.")
L("Kolejnosc dzialan", ["Sprawdz prog", "Wybierz konto",
                        "Wplata miesieczna", "Zawroc zwrot"],
  "Kolejnosc dzialan jest czterostopniowa: sprawdz swoj prog, wybierz "
  "konto zgodnie z nim, ustaw wplate miesieczna, i skieruj zwrot z "
  "powrotem do systemu.")
I("Dlaczego miesiecznie", "bez jednej zlej daty",
  "Miesiecznie, a nie raz w roku, z tego samego powodu co zawsze: nie ma "
  "wtedy jednej daty, ktora moze zepsuc caly rok.")
I("Czego nie robic", "nie czekaj",
  "Czego nie robic: nie czekaj na idealny moment. Limit nie przechodzi na "
  "kolejny rok, wiec czekanie kosztuje caly roczny limit.")
I("I nie zakladaj obu", "ponizej limitu",
  "I nie zakladaj obu kont naraz, jesli nie wypelniasz nawet jednego "
  "limitu. Dwa konta ponizej limitu to dwie oplaty i zero korzysci.")
I("Co zostaje", "liczba i nawyk",
  "Zostaje jedna liczba do sprawdzenia, twoj prog, i jeden nawyk, "
  "zawracanie zwrotu. Reszta to konsekwencja.")
I("Ostatnia uwaga", "konto to opakowanie",
  "I ostatnia uwaga: oba konta to tylko opakowania. To, co do nich "
  "wlozysz, decyduje o wyniku mocniej niz podatek.")
I("Most na koniec", "co wlozyc do srodka",
  "A skoro konto to opakowanie, nastepne naturalne pytanie brzmi: co "
  "wlozyc do srodka przy polskiej pensji. To temat na osobny material z "
  "tego kanalu.")
C("Kolejny Poziom", "licz, nie zgaduj",
  "Zostaw komentarz, w ktorym progu jestes — zobaczymy, jak rozklada sie "
  "to wsrod ogladajacych. A najczesciej pytany temat robimy nastepny.")

SHORT = [
    {"layout": "titulo", "kicker": "IKE czy IKZE?",
     "sub": "jedna liczba decyduje",
     "nar": "Nie odpowiadaj na to pytanie, dopoki nie sprawdzisz jednej "
            "liczby: swojego progu podatkowego.", "sem_cap": True},
    {"layout": "item", "kicker": "Drugi prog", "preco": "22 punkty przewagi",
     "nar": "Powyzej stu dwudziestu tysiecy zlotych odliczasz po "
            "trzydziestu dwoch procentach, a wyplacasz po dziesieciu. "
            "Dwadziescia dwa punkty roznicy.", "sem_cap": True},
    {"layout": "item", "kicker": "Pierwszy prog", "preco": "remis",
     "nar": "Ponizej progu odliczasz po dwunastu i oddajesz po dziesieciu "
            "od calosci. To remis — wybierz IKE, bo jest elastyczniejsze.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Warunek", "preco": "zawroc zwrot",
     "nar": "I warunek: zwrot podatku musi wrocic na konto. Wydany zwrot "
            "znaczy, ze IKZE przegrywa o dziesiec procent koncowej kwoty.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Kolejny Poziom", "sub": "caly rachunek",
     "nar": "To caly werdykt: prog decyduje, zwrot wraca. Napisz w "
            "komentarzu, w ktorym progu jestes.", "sem_cap": True},
]

COPY = """# Prog podatkowy rozstrzyga wybor miedzy IKE a IKZE

## TYTUL
IKE czy IKZE w 2026? Jedna Liczba Rozstrzyga Caly Wybor

## OPIS
Prawie kazdy material o IKE i IKZE konczy sie zdaniem "to zalezy od twojej sytuacji" — prawdziwym i bezuzytecznym. Ten film mowi, od czego konkretnie zalezy: od twojego progu podatkowego. I robi caly rachunek na liczbach z tego roku.

LIMITY NA 2026. Limity wplat wynikaja z prognozowanego przecietnego wynagrodzenia (9 420 zl miesiecznie): IKE to trzykrotnosc, czyli 28 260 zl rocznie na osobe; IKZE przy umowie o prace to 11 304 zl, a przy dzialalnosci gospodarczej 16 956 zl. Oba konta mozna prowadzic jednoczesnie — i limit NIE przechodzi na kolejny rok: czego nie wplacisz do 31 grudnia, przepada.

MECHANIKA. IKZE odlicza sie od podstawy opodatkowania, wiec zwrot jest rowny twojej stawce: 12% w pierwszym progu (do 120 000 zl dochodu), 32% w drugim. Na pelnym limicie etatowym to odpowiednio ok. 1 356 zl albo ok. 3 617 zl zwrotu (na dzialalnosci nawet ok. 5 426 zl). Ale przy wyplacie po 65. roku zycia placisz ryczalt 10% — liczony od CALEJ kwoty, wplat i zyskow razem. IKE dziala odwrotnie: zero ulgi dzis, zero podatku po szescdziesiatce — pelne zwolnienie z 19% podatku Belki. Rozni sie tez wczesniejsze wyjscie: z IKE placisz po prostu 19% od zysku jak na zwyklym rachunku; z IKZE zwrot dolicza sie do dochodu wedlug skali.

WYLICZENIE. W pierwszym progu przewaga IKZE to na papierze 2 punkty procentowe (12 minus 10) — a poniewaz ryczalt rosnie razem z zyskiem, przy dlugim horyzoncie ta przewaga topnieje praktycznie do zera. Werdykt: remis, decyduje elastycznosc, czyli IKE. W drugim progu roznica stawek to 22 punkty procentowe (32 na wejsciu, 10 na wyjsciu) — IKZE wygrywa wyraznie i powinno byc pierwsze, a nadwyzka idzie na IKE.

WARUNEK, O KTORYM SIE NIE MOWI: cala przewaga IKZE zaklada, ze zwrot podatku wraca do systemu. Zwrot wydany na wakacje znaczy, ze IKZE przegrywa z IKE o cale 10% koncowej wartosci konta.

Kolejnosc dzialan: sprawdz prog, wybierz konto, ustaw wplate miesieczna, zawroc zwrot.

## ROZDZIALY
{CAPITULOS}

## KOMENTARZ
Jedno pytanie, bo od tego zalezy caly werdykt: w ktorym progu podatkowym jestes — pierwszym czy drugim? Zbieram odpowiedzi, zeby wiedziec, dla kogo liczyc nastepne materialy. A jesli jest temat z trzeciego filaru, ktory mam rozlozyc na liczby, napisz jaki — najczesciej pytany robimy pierwszy.

## HASHTAGI
#IKZE #IKE #KolejnyPoziom

## TAGI
ike czy ikze, limity ike 2026, limit ikze 2026, ikze zwrot podatku, konto emerytalne, trzeci filar, oszczedzanie na emeryture, podatek belki, ulga podatkowa, prog podatkowy, emerytura, finanse osobiste, ike ikze roznice, jak oszczedzac na emeryture, kolejny poziom

## USTAWIENIA STUDIO
- Jezyk: Polski (pl) | Kategoria: Edukacja (27)
- Nie dla dzieci
- Ujawnienie tresci syntetycznych: TAK (glos generowany przez AI)
- Lokalizacja: Polska | Licencja: standardowa licencja YouTube
- Reklamy mid-roll: wlaczone (dlugosc powyzej 8 minut)

## MUZYKA / LICENCJA
{TRILHA}

## ZRODLA
Limity wplat na 2026 rok (IKE 28 260 zl; IKZE 11 304 zl na etacie i 16 956 zl przy dzialalnosci gospodarczej) wynikaja z prognozowanego przecietnego miesiecznego wynagrodzenia 9 420 zl przyjetego w projekcie ustawy budzetowej i zostaly ogloszone w obwieszczeniu; potwierdzone zgodnie m.in. przez Analizy.pl, BDO i PZU (18/08/2026). Stawki skali podatkowej 12% i 32% z progiem 120 000 zl, ryczalt 10% przy wyplacie z IKZE po 65. roku zycia, zwolnienie wyplat z IKE po 60. roku zycia z 19% podatku od zyskow kapitalowych (podatek Belki) oraz zasady wczesniejszego zwrotu — stan prawny na sierpien 2026. Kwoty zwrotow (ok. 1 356 zl, 3 617 zl, 5 426 zl) to prosta arytmetyka stawki razy limit, zaokraglona. Ten material jest trescia edukacyjna o arytmetyce podatkowej obu kont; nie jest porada inwestycyjna ani podatkowa, a przepisy moga sie zmienic — przed decyzja sprawdz aktualne stawki albo skonsultuj sie z doradca.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-003",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#15202B", "c1": "#2A6F97", "c2": "#E8A33D", "bg": "#F0EDE6"},
    "thumb": {"l1": "IKE CZY IKZE", "l2": "decyduje prog"},
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p = "fabrica/specs/kolejny-poziom-003.json"
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
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
