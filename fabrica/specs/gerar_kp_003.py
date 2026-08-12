#!/usr/bin/env python3
"""Gera a spec do kolejny-poziom-003 — IKE czy IKZE w 2026.

Fonte da pauta (PASSO 0, 05/08/2026, n=15 videos em polones de 90 dias,
financas pessoais, regiao PL):
  mediana do grupo ............ 44,6 views/dia   (corte de outlier: 133,9)
  outlier replicavel .......... 2422 v/d — Marcin Iwuc,
    "Inwestowac czy nadplacac kredyt hipoteczny - SPRAWDZAM, co sie bardziej
     oplaca? [KALKULATOR]"
  outlier nao replicavel ...... 2128 v/d — horyzonty (entrevista)
  formato morto ............... 4,3 v/d — Bernard,
    "Gdzie trzymac oszczednosci? Lokata vs obligacje"

O que separa o outlier do morto NAO e "comparar duas opcoes" — o morto tambem
compara. E comparar com VEREDITO CALCULADO: o vencedor faz a conta e declara o
resultado, o morto so lista pros e contras. Entao o que este pacote copia e a
ESTRUTURA (A contra B, com numero e decisao), nunca o assunto.

Eixo nao usado: o pacote 002 do canal foi stopa zastapienia do ZUS, e a Raman
Voranau publicou o mesmo eixo em 22/07 (73 v/d). Este vai para a arbitragem
fiscal entre os dois veiculos privados, que o canal ainda nao tocou.

Ancoras 2026, todas conferidas em fonte institucional (ING TFI e KupFundusz,
que batem entre si; a finwire.pl divergia com numeros do ano anterior):
  IKE ....................... 28 260 zl   (era 26 019 em 2025)
  IKZE, umowa o prace ....... 11 304 zl   (era 10 407,60)
  IKZE, JDG ................. 16 956 zl
  base: prognozowane przecietne wynagrodzenie 9 420 zl — 3x, 1,2x e 1,8x
  progi PIT ................. 12% ate 120 000 zl, 32% acima
  kwota wolna ............... 30 000 zl; kwota zmniejszajaca 3 600 zl
  IKZE na saida ............. 10% ryczalt depois dos 65
  IKE na saida .............. zero, sem os 19% podatku Belki, depois dos 60

A tese que sustenta o veredito, e que quase nenhum video polones faz: o ryczalt
de dez por cento do IKZE incide sobre o VALOR TOTAL sacado, capital mais lucro,
enquanto o IKE zera tudo. Logo a ulga da entrada so compensa se for reinvestida.
No primeiro degrau da 12% e da praticamente empate; no segundo degrau da 32% e o
IKZE ganha com folga. O veredito depende do degrau — e da condicao que ninguem
menciona.

Taxa da voz MEDIDA antes de dimensionar (regra do PLAYBOOK): pl-PL-MarekNeural
faz 20,02 chars/s com numeros por extenso — a voz mais rapida do portfolio, bem
acima dos 14,5 que eu teria assumido. Com o padrao errado este roteiro sairia
com nove minutos e meio em vez de treze.

Numeros por extenso, sem digitos: digito cru faz o TTS soletrar errado em polones.
"""
import json, os

VOZ = "pl-PL-MarekNeural"
PALETA = {"ink": "#15202B", "c1": "#2A6F97", "c2": "#E8A33D", "bg": "#F0EDE6"}

CAPS = []


def cap(titulo, cenas):
    CAPS.append((titulo, cenas))


# ============================ 1 ============================
cap("Pytanie postawione odwrotnie", [
 ("titulo", "IKE czy IKZE", "zle postawione pytanie", "Prawie kazdy material na ten temat konczy sie tym samym zdaniem: to zalezy od twojej sytuacji. To zdanie jest prawdziwe i zupelnie bezuzyteczne, bo nie mowi od czego konkretnie zalezy ani jak to sprawdzic w pietnascie sekund."),
 ("item", "Zalezy", "ale od jednej liczby", "A zalezy od jednej liczby, i ta liczba to twoj prog podatkowy. Wszystko inne w tym porownaniu — oplaty, dostepne fundusze, wygoda aplikacji — jest przy niej drugorzedne, a mimo to prawie nikt nie zaczyna wlasnie od niej."),
 ("titulo", "Dwa konta", "dwa momenty ulgi", "Oba konta daja ulge podatkowa i oba sluza temu samemu celowi. Roznia sie momentem, w ktorym ta ulga do ciebie trafia: jedno oddaje ci pieniadze juz w przyszlym roku, drugie dopiero po kilkudziesieciu latach."),
 ("item", "IKZE", "ulga dzisiaj", "Wplata na indywidualne konto zabezpieczenia emerytalnego zmniejsza podstawe opodatkowania za biezacy rok. Czesc wplaconej kwoty wraca do ciebie przelewem z urzedu skarbowego, zwykle wiosna nastepnego roku."),
 ("item", "IKE", "ulga na koncu", "Wplata na indywidualne konto emerytalne nie daje dzis absolutnie nic. Za to wyplata po ukonczeniu szescdziesieciu lat jest wolna od podatku od zyskow kapitalowych — i to jest zwolnienie calkowite, nie czesciowe."),
 ("titulo", "Haczyk", "jest w slowie w calosci", "I wlasnie tu jest haczyk, ktory rozstrzyga cale porownanie. Zapamietaj slowo calkowite, bo za chwile okaze sie, ze IKZE takiej wlasciwosci nie ma, i ze to jedna roznica przesadza o wszystkim."),
 ("lista", "Co policzymy", ["Limity na ten rok", "Ulga w pierwszym progu", "Ulga w drugim progu", "Warunek, ktory decyduje"], "Policzymy po kolei cztery rzeczy: aktualne limity wplat, realna wartosc ulgi w pierwszym progu, ta sama wartosc w drugim progu, oraz warunek, bez ktorego cala przewaga IKZE znika co do grosza."),
 ("item", "Bez wodolejstwa", "same liczby", "Bez ogolnikow o dywersyfikacji i o tym, ze po prostu warto oszczedzac. Same liczby, jedna tabela w glowie i jeden wniosek na koncu, ktory da sie zapisac w dwoch zdaniach i zapamietac."),
 ("item", "Uczciwe zastrzezenie", "to nie porada inwestycyjna", "Uczciwe zastrzezenie na wstepie: to nie jest porada inwestycyjna ani podatkowa. To arytmetyka na publicznie oglaszanych stawkach i limitach, ktora mozesz w calosci sprawdzic samodzielnie w kwadrans."),
 ("item", "Zalozenie", "te same aktywa w obu", "Zakladamy tez przez caly material, ze w obu kontach trzymasz dokladnie te same aktywa i wplacasz dokladnie te same kwoty. Inaczej porownywalibysmy strategie inwestycyjne, a nie opakowania podatkowe."),
 ("titulo", "Zacznijmy", "od limitow", "Zacznijmy wiec od pytania najbardziej praktycznego: ile w ogole mozesz wplacic na kazde z tych kont w tym roku. To wyznacza skale calej reszty rozwazan."),
])

# ============================ 2 ============================
cap("Limity na ten rok", [
 ("titulo", "Limity", "rosna razem z placa", "Limity wplat nie sa ustalane recznie ani negocjowane co roku. Wynikaja wprost z prognozowanego przecietnego wynagrodzenia w gospodarce narodowej, ktore na ten rok wynosi dziewiec tysiecy czterysta dwadziescia zlotych miesiecznie."),
 ("item", "IKE", "trzykrotnosc", "Limit na indywidualne konto emerytalne to trzykrotnosc tej kwoty, czyli dwadziescia osiem tysiecy dwiescie szescdziesiat zlotych na osobe w ciagu roku. Malzonkowie maja po tyle samo, kazde na swoim koncie."),
 ("item", "IKZE na etacie", "jeden i dwie dziesiate", "Limit na konto zabezpieczenia emerytalnego przy umowie o prace to jeden i dwie dziesiate tej samej podstawy, czyli jedenascie tysiecy trzysta cztery zlote. To niecala polowa tego, co daje IKE."),
 ("item", "IKZE na dzialalnosci", "jeden i osiem dziesiatych", "Przy dzialalnosci gospodarczej mnoznik jest wyrazne wyzszy, jeden i osiem dziesiatych, co daje szesnascie tysiecy dziewiecset piecdziesiat szesc zlotych. Ta roznica bedzie miala znaczenie w werdykcie."),
 ("barras", "Limity roczne", ["IKE", "IKZE JDG", "IKZE etat"], [100, 60, 40], "Proporcje wygladaja wiec tak: IKE daje prawie trzy razy wiecej miejsca niz IKZE na etacie, a samozatrudniony miesci na IKZE mniej wiecej polowe tego, co miesci na IKE."),
 ("item", "Rok temu", "bylo zauwazalnie mniej", "Rok wczesniej limity byly zauwazalnie nizsze: dwadziescia szesc tysiecy dziewietnascie zlotych na IKE oraz dziesiec tysiecy czterysta siedem zlotych i szescdziesiat groszy na IKZE przy umowie o prace."),
 ("item", "Wzrost", "to nie hojnosc", "Ten wzrost to nie hojnosc panstwa ani zadna nowa ulga, tylko mechaniczne przeliczenie prognozy plac. Jesli place rosna, limity rosna razem z nimi, automatycznie i bez zadnej decyzji politycznej."),
 ("item", "Oba naraz", "prawie czterdziesci tysiecy", "Mozesz prowadzic oba konta jednoczesnie, i nie ma tu zadnego wykluczenia. Na etacie daje to razem prawie czterdziesci tysiecy zlotych rocznie, a na dzialalnosci ponad czterdziesci piec tysiecy."),
 ("item", "Limit sie nie kumuluje", "niewykorzystany przepada", "I rzecz, ktora zaskakuje najwiecej osob: limit nie przechodzi na kolejny rok. Czego nie wplacisz do trzydziestego pierwszego grudnia, to przepada bezpowrotnie i nigdy juz nie wroci."),
 ("item", "Wniosek praktyczny", "grudzien jest za pozno", "Dlatego ta sama decyzja podjeta w grudniu jest gorsza niz podjeta w styczniu. Nie z powodow podatkowych, tylko dlatego, ze zostaje mniej miesiecy na rozlozenie wplaty i mniej czasu na prace pieniedzy."),
 ("titulo", "Skoro znamy skale", "zobaczmy mechanike", "Skoro znamy juz skale calego zjawiska, zobaczmy jak dokladnie dziala ulga w kazdym z tych kont. Zaczniemy od tego, ktore placi od razu, bo to ono wywoluje wiecej nieporozumien."),
])

# ============================ 3 ============================
cap("IKZE: ulga teraz, podatek potem", [
 ("titulo", "Mechanika IKZE", "odliczasz od podstawy", "IKZE odlicza sie od podstawy opodatkowania, a nie od samego podatku. To rozroznienie brzmi jak formalnosc, a decyduje o tym, ile realnie odzyskujesz — i dlatego dwie osoby z ta sama wplata dostaja rozne kwoty."),
 ("item", "Odliczenie od podstawy", "wartosc zalezy od stawki", "Kiedy odliczasz od podstawy, wartosc odliczenia jest zawsze rowna twojej stawce podatkowej. Ta sama wplata daje wiec zupelnie inny zwrot osobie w pierwszym progu i osobie w drugim, przy identycznym wysilku."),
 ("item", "Pierwszy prog", "dwanascie procent", "W pierwszym progu, czyli do stu dwudziestu tysiecy zlotych dochodu rocznie, stawka wynosi dwanascie procent. Kazda zlotowka wplacona na IKZE wraca do ciebie jako dwanascie groszy zwrotu."),
 ("item", "Drugi prog", "trzydziesci dwa procent", "Powyzej stu dwudziestu tysiecy zlotych stawka rosnie do trzydziestu dwoch procent. Ta sama zlotowka zwraca juz trzydziesci dwa grosze, czyli prawie trzy razy wiecej za dokladnie te sama czynnosc."),
 ("item", "Maksymalna wplata na etacie", "w pierwszym progu", "Policzmy to na pelnym limicie. Jedenascie tysiecy trzysta cztery zlote wplacone przez osobe w pierwszym progu daja zwrot okolo tysiaca trzystu piecdziesieciu szesciu zlotych, jednorazowo."),
 ("item", "Ta sama wplata", "w drugim progu", "Ta sama wplata przez osobe w drugim progu daje zwrot okolo trzech tysiecy szesciuset siedemnastu zlotych. Roznica siega dwoch tysiecy dwustu szescdziesieciu zlotych, przy identycznej kwocie na koncie."),
 ("titulo", "Ale to polowa historii", "jest jeszcze wyjscie", "To jednak dopiero polowa historii, i to ta przyjemniejsza. IKZE nie jest bowiem zwolnione z podatku — ono go wylacznie przesuwa w czasie i zmienia stawke na nizsza."),
 ("item", "Na wyjsciu", "dziesiec procent ryczaltu", "Przy wyplacie po ukonczeniu szescdziesieciu pieciu lat placisz zryczaltowany podatek w wysokosci dziesieciu procent. To istotnie mniej niz dziewietnascie procent podatku Belki, ale to nadal nie jest zero."),
 ("item", "I tu jest sedno", "od calosci, nie od zysku", "I tu jest sedno calego porownania, punkt, ktory przesadza o werdykcie: te dziesiec procent liczy sie od calej wyplacanej kwoty. Od wplat i od wypracowanych zyskow razem, a nie od samych zyskow."),
 ("item", "Konsekwencja", "im dluzej, tym drozej", "Konsekwencja jest niewygodna i rzadko wypowiadana. Im dluzej oszczedzasz i im wiekszy zysk wypracujesz, tym wieksza kwota wpada pod te dziesiec procent — sukces inwestycyjny podnosi rachunek."),
 ("titulo", "Zapamietaj to", "wracamy do tego w liczbach", "Zapamietaj to jedno zdanie, bo wrocimy do niego przy obu wyliczeniach. Najpierw jednak drugie konto, ktore zbudowano dokladnie odwrotnie, punkt po punkcie."),
])

# ============================ 4 ============================
cap("IKE: nic teraz, zero potem", [
 ("titulo", "Mechanika IKE", "zadnej ulgi na wejsciu", "IKE nie daje zadnej ulgi na wejsciu. Wplacasz z pieniedzy juz opodatkowanych i w rozliczeniu rocznym nie zmienia sie nic."),
 ("item", "Za to na wyjsciu", "zero podatku", "Za to na wyjsciu, po ukonczeniu szescdziesieciu lat i przy spelnieniu warunku wplat, nie placisz nic. Ani podatku Belki, ani ryczaltu."),
 ("item", "Zero od zysku", "i zero od kapitalu", "Zero od zysku i zero od kapitalu. Cala wypracowana kwota jest twoja, niezaleznie od tego, jak duzy zysk udalo sie osiagnac przez te wszystkie lata."),
 ("item", "Punkt odniesienia", "dziewietnascie procent", "Punktem odniesienia jest tu podatek Belki, dziewietnascie procent od zyskow kapitalowych, ktore zaplacilbys na zwyklym rachunku maklerskim."),
 ("item", "Wiek wyplaty", "szescdziesiat kontra szescdziesiat piec", "Rozni sie tez wiek: szescdziesiat lat przy IKE, szescdziesiat piec przy IKZE. Piec lat roznicy, ktore przy planowaniu emerytury nie sa drobiazgiem."),
 ("titulo", "Elastycznosc", "tu tez sa roznice", "Roznia sie rowniez zasady wczesniejszego wyjscia, i to jest argument, ktory rzadko pojawia sie w porownaniach, a bywa decydujacy."),
 ("item", "Wczesniejszy zwrot z IKE", "placisz Belke od zysku", "Jesli wycofasz srodki z IKE przed czasem, placisz po prostu dziewietnascie procent od wypracowanego zysku. Tak jak na zwyklym rachunku, ani grosza wiecej."),
 ("item", "Wczesniejszy zwrot z IKZE", "dolicza sie do dochodu", "Przy IKZE wczesniejszy zwrot dolicza sie do dochodu i jest opodatkowany wedlug skali. Czyli potencjalnie trzydziestoma dwoma procentami, od calej kwoty."),
 ("item", "To zmienia charakter", "IKZE jest sztywniejsze", "To zmienia charakter obu produktow. IKE jest elastyczne, IKZE jest sztywne — a sztywnosc ma swoja cene, nawet jesli nie widac jej w tabelce."),
 ("item", "Dziedziczenie", "oba przechodza na bliskich", "W obu przypadkach srodki sa dziedziczone i w obu przypadkach nie wchodza do masy spadkowej na zasadach ogolnych, wiec ten argument sie znosi."),
 ("titulo", "Mamy oba mechanizmy", "czas policzyc", "Mamy oba mechanizmy. Teraz najciekawsza czesc: co wychodzi, kiedy podstawimy realne liczby."),
])

# ============================ 5 ============================
cap("Wyliczenie: pierwszy prog", [
 ("titulo", "Pierwszy prog", "dwanascie procent", "Zaczynamy od osoby w pierwszym progu, czyli z dochodem ponizej stu dwudziestu tysiecy zlotych rocznie. To zdecydowana wiekszosc pracujacych w tym kraju."),
 ("item", "Zalozenie", "ta sama kwota w obu", "Zakladamy te sama wplate w obu wariantach i te same aktywa w srodku. Interesuje nas wylacznie roznica podatkowa, nic wiecej."),
 ("item", "Wariant IKZE", "dostajesz dwanascie procent", "W wariancie IKZE dostajesz zwrot rowny dwunastu procentom wplaty. Przy pelnym limicie etatowym to okolo tysiaca trzystu piecdziesieciu szesciu zlotych na reke."),
 ("item", "Na wyjsciu", "oddajesz dziesiec procent calosci", "Na wyjsciu oddajesz dziesiec procent calej zgromadzonej kwoty. Nie dziesiec procent wplat — dziesiec procent tego, co konto bedzie warte na koncu."),
 ("item", "Wariant IKE", "nie dostajesz nic", "W wariancie IKE nie dostajesz nic na wejsciu, ale na wyjsciu nie oddajesz nic. Sto procent koncowej wartosci zostaje u ciebie."),
 ("titulo", "Zderzenie", "dwanascie kontra dziesiec", "Zderzmy to wprost. IKZE daje ci dwanascie procent teraz i zabiera dziesiec procent calosci potem. IKE nie daje nic i nie zabiera nic."),
 ("item", "Gdyby nie bylo wzrostu", "przewaga wynosi dwa punkty", "Gdyby pieniadze w ogole nie pracowaly, przewaga IKZE wynioslaby dokladnie dwa punkty procentowe. Dwanascie minus dziesiec, i tyle."),
 ("item", "Ale pieniadze pracuja", "i to zmienia proporcje", "Ale pieniadze pracuja przez kilkadziesiat lat. Zwrot dostajesz od wplaty, natomiast ryczalt placisz od wplaty powiekszonej o caly zysk."),
 ("item", "Efekt", "przewaga topnieje", "Efekt jest taki, ze im dluzszy horyzont i im wyzsza stopa zwrotu, tym bardziej ta dwupunktowa przewaga topnieje. Przy dlugim horyzoncie schodzi praktycznie do zera."),
 ("barras", "Pierwszy prog", ["IKE", "IKZE"], [100, 100], "Praktyczny wniosek dla pierwszego progu brzmi wiec zaskakujaco: to jest remis. Roznica jest na tyle mala, ze nie powinna decydowac o wyborze."),
 ("titulo", "Skoro remis", "zdecyduje co innego", "Skoro w liczbach wychodzi remis, decyduje co innego: elastycznosc, wiek wyplaty i to, czy w ogole zamierzasz wykorzystac zwrot. Ale najpierw drugi prog."),
])

# ============================ 6 ============================
cap("Wyliczenie: drugi prog", [
 ("titulo", "Drugi prog", "trzydziesci dwa procent", "Teraz osoba w drugim progu, z dochodem powyzej stu dwudziestu tysiecy zlotych. Tu cala arytmetyka wyglada zupelnie inaczej."),
 ("item", "Zwrot", "trzydziesci dwa procent wplaty", "Zwrot wynosi trzydziesci dwa procent wplaty. Przy pelnym limicie etatowym to okolo trzech tysiecy szesciuset siedemnastu zlotych w jednym rozliczeniu."),
 ("item", "Na dzialalnosci", "jeszcze wiecej", "Przy dzialalnosci gospodarczej i wyzszym limicie ta sama stawka daje okolo pieciu tysiecy czterystu dwudziestu szesciu zlotych zwrotu rocznie."),
 ("item", "Koszt wyjscia", "nadal dziesiec procent", "A koszt wyjscia sie nie zmienia. Nadal dziesiec procent, bo ryczalt nie zalezy od tego, w ktorym progu bylas w momencie wplacania."),
 ("titulo", "I tu jest asymetria", "wchodzisz drozej, wychodzisz taniej", "I to jest cala tajemnica tego produktu. Wchodzisz przy swojej wysokiej stawce, a wychodzisz przy niskiej, ustalonej z gory."),
 ("item", "Roznica stawek", "dwadziescia dwa punkty", "Roznica miedzy trzydziestoma dwoma a dziesiecioma procentami to dwadziescia dwa punkty procentowe. To nie jest niuans, to jest cala teza tego materialu."),
 ("item", "Nawet po latach wzrostu", "przewaga zostaje", "I nawet po kilkudziesieciu latach wzrostu, kiedy ryczalt obejmie tez zyski, ta przewaga sie nie zeruje. Zmniejsza sie, ale zostaje wyrazna."),
 ("barras", "Drugi prog", ["IKZE", "IKE"], [100, 78], "W drugim progu IKZE wygrywa wyraznie, i to jest jedyny moment w tym porownaniu, w ktorym mozna powiedziec cos jednoznacznego."),
 ("item", "Kolejnosc", "najpierw wypelnij IKZE", "Dlatego dla osoby w drugim progu kolejnosc jest prosta: najpierw wypelnij limit IKZE, dopiero nadwyzke kieruj na IKE."),
 ("item", "Bo limit IKZE", "jest niski", "Zwlaszcza ze limit IKZE jest niski. Jedenascie tysiecy trzysta cztery zlote wyczerpiesz szybciej, niz sadzisz, a IKE zostaje na reszte."),
 ("titulo", "Zostal warunek", "bez ktorego to nie dziala", "Zostal jeden warunek. Bez niego wszystko, co wlasnie policzylismy dla drugiego progu, przestaje byc prawda."),
])

# ============================ 7 ============================
cap("Warunek, o ktorym sie nie mowi", [
 ("titulo", "Warunek", "zwrot musi wrocic", "Cala przewaga IKZE opiera sie na zalozeniu, ktore prawie nigdy nie pada na glos w zadnym porownaniu: ze otrzymany zwrot podatku rowniez zostanie zainwestowany, a nie po prostu wydany."),
 ("item", "Jesli wydasz zwrot", "przewaga znika", "Jesli zwrot z urzedu skarbowego wladujesz w wakacje albo w nowy telefon, zostaje ci samo konto obciazone dziesiecioma procentami przy wyplacie. Korzysc zostala skonsumowana, koszt zostal."),
 ("item", "Wtedy IKZE przegrywa", "i to wyraznie", "Wtedy IKZE nie tylko nie wygrywa z IKE — ono przegrywa, i to o cale dziesiec procent koncowej wartosci konta. Ulga wydana to z punktu widzenia emerytury ulga, ktorej nigdy nie bylo."),
 ("item", "To nie jest teoria", "tak dziala wiekszosc", "I to nie jest przypadek czysto teoretyczny. Zwrot podatku wplywa na konto wiosna, w glowie jest oznaczony jako pieniadze z nieba, i jest wydawany dokladnie tak, jak sie go nazywa."),
 ("titulo", "Wniosek techniczny", "zwrot ma trafic na konto", "Wniosek techniczny jest wiec bardzo prosty: zwrot z IKZE powinien od razu trafic na IKE albo z powrotem na IKZE w kolejnym roku. Bez tego jednego ruchu cala konstrukcja sie sypie."),
 ("item", "Druga pulapka", "prog moze sie zmienic", "Druga pulapka dotyczy samego progu. Liczysz przewage przy trzydziestu dwoch procentach, ale prog moze sie zmienic, jesli zmienisz prace, przejdziesz na dzialalnosc albo stracisz premie."),
 ("item", "Wtedy wracasz", "do remisu", "Jesli spadniesz do pierwszego progu, korzysc z przyszlych wplat wraca do dwoch punktow procentowych, czyli do remisu. Wczesniejsze wplaty zachowuja swoja wartosc, ale przyszle juz nie."),
 ("item", "Trzecia", "ryczalt to dzisiejsza stawka", "Trzecia rzecz, o ktorej trzeba powiedziec uczciwie: dziesiec procent to stawka obowiazujaca dzisiaj. Nikt nie zagwarantowal, ze bedzie taka za trzydziesci lat, bo to zwykly przepis ustawowy."),
 ("item", "Symetrycznie", "zero w IKE tez jest przepisem", "Symetrycznie jednak zero podatku w IKE to rowniez tylko przepis, ktory mozna zmienic. Rzetelnie jest wiec powiedziec, ze ryzyko zmiany zasad dotyczy obu kont w tym samym stopniu."),
 ("item", "Czego nie robimy", "nie zgadujemy przyszlosci", "Dlatego nie bedziemy tu zgadywac przyszlosci ani straszyc. Liczymy na zasadach, ktore obowiazuja w tym roku, bo to jedyna metoda, ktora da sie sprawdzic i powtorzyc."),
 ("titulo", "Mamy wszystko", "czas na werdykt", "Mamy juz komplet: limity, mechanike obu kont, dwa wyliczenia i trzy uczciwe zastrzezenia. Czas na werdykt, i zmiescimy go w dwoch zdaniach plus kolejnosci dzialan."),
])

# ============================ 8 ============================
cap("Werdykt i kolejnosc", [
 ("titulo", "Werdykt", "zalezy od progu", "Werdykt brzmi tak. W drugim progu podatkowym IKZE wygrywa wyraznie i powinno byc pierwsze. W pierwszym progu jest remis, wiec decyduje elastycznosc."),
 ("item", "Pierwszy prog", "wybierz IKE", "Konkretnie: w pierwszym progu wybierz IKE. Nie dlatego, ze jest korzystniejsze podatkowo, tylko dlatego, ze przy remisie wygrywa produkt latwiejszy do opuszczenia."),
 ("item", "Drugi prog", "IKZE do limitu, potem IKE", "W drugim progu wypelnij najpierw IKZE do limitu, a nadwyzke kieruj na IKE. I zwrot podatku potraktuj jak czesc wplaty, a nie jak premie."),
 ("item", "Dzialalnosc gospodarcza", "limit jest wyzszy", "Przy dzialalnosci gospodarczej ta kolejnosc jest jeszcze mocniejsza, bo wyzszy limit IKZE oznacza wiecej pieniedzy odliczonych po wysokiej stawce."),
 ("lista", "Kolejnosc dzialan", ["Sprawdz swoj prog", "Wybierz konto wedlug progu", "Ustaw wplate miesieczna", "Zwrot kieruj z powrotem"], "Kolejnosc dzialan jest czterostopniowa: sprawdz swoj prog, wybierz konto zgodnie z nim, ustaw wplate miesieczna zamiast jednorazowej, i skieruj zwrot z powrotem do systemu."),
 ("item", "Dlaczego miesiecznie", "nie ma jednej daty", "Miesiecznie, a nie raz w roku, z tego samego powodu co zawsze: nie ma wtedy jednej daty, ktora moze zepsuc caly rok."),
 ("item", "Czego nie robic", "nie czekaj na idealny moment", "Czego nie robic: nie czekaj na idealny moment ani na obnizke stop. Limit nie przechodzi na kolejny rok, wiec czekanie kosztuje caly roczny limit."),
 ("item", "I nie zakladaj obu naraz", "jesli nie wypelnisz jednego", "I nie zakladaj obu kont naraz, jesli nie jestes w stanie wypelnic nawet jednego limitu. Dwa konta ponizej limitu to dwie oplaty i zadnej dodatkowej korzysci."),
 ("item", "Co zostaje", "jedna liczba i jeden nawyk", "Zostaje wiec jedna liczba do sprawdzenia, twoj prog, i jeden nawyk do wyrobienia, zawracanie zwrotu. Reszta to juz tylko konsekwencja."),
 ("item", "I ostatnia uwaga", "to nadal jest opakowanie", "I ostatnia uwaga, bo bez niej to porownanie wprowadza w blad: oba konta to tylko opakowania. To, co w nie wlozysz, decyduje o wyniku duzo mocniej niz podatek."),
 ("cta", "Kolejny Poziom", "policz swoj prog", "Jesli ten material byl przydatny, zostaw komentarz z informacja, w ktorym progu jestes. Zobaczymy, jak rozklada sie to wsrod ogladajacych."),
])


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
 cena(("titulo", "IKE czy IKZE", "jedna liczba decyduje", "Nie odpowiadaj na to pytanie, dopoki nie sprawdzisz jednej liczby: swojego progu podatkowego. Wszystko inne jest drugorzedne."), False, ""),
 cena(("item", "Drugi prog", "IKZE wygrywa", "Powyzej stu dwudziestu tysiecy zlotych odliczasz po trzydziestu dwoch procentach, a wyplacasz po dziesieciu. Dwadziescia dwa punkty roznicy."), False, ""),
 cena(("item", "Pierwszy prog", "to remis", "Ponizej tego progu odliczasz po dwunastu i wyplacasz po dziesieciu. Dwa punkty, ktore znikaja przy dlugim horyzoncie."), False, ""),
 cena(("item", "Warunek", "zwrot musi wrocic", "I warunek, o ktorym sie nie mowi: jesli wydasz zwrot podatku, IKZE przegrywa z IKE o cale dziesiec procent koncowej kwoty."), False, ""),
 cena(("cta", "Kolejny Poziom", "cale wyliczenie", "Cale wyliczenie, z limitami na ten rok, jest w dluzszym materiale."), False, ""),
]
for c in short:
    c.pop("sem_cap", None)

spec = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-003",
    "voz": VOZ,
    "paleta": PALETA,
    "thumb": {"l1": "IKE CZY IKZE", "l2": "decyduje prog"},
    "longo": longo,
    "short": short,
    "copy": "gerado a partir dos capitulos reais apos o render",
}

if __name__ == "__main__":
    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "kolejny-poziom-003.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False)
    nl = sum(len(c["nar"]) for c in longo)
    ns = sum(len(c["nar"]) for c in short)
    assert not any(ch.isdigit() for c in longo + short for ch in c["nar"]), \
        "digito cru no roteiro: o TTS polones soletra errado"
    print(f"cenas longo ....... {len(longo)}")
    print(f"capitulos ......... {len(CAPS)}")
    print(f"chars narracao .... {nl}")
    # 20,02 chars/s medidos para pl-PL-MarekNeural com numeros por extenso
    for taxa in (18.5, 20.02, 21.5):
        s = nl / taxa + len(longo) * 0.5
        print(f"  a {taxa} chars/s .. {s:.0f}s = {s/60:.1f} min")
    print(f"short ............. {len(short)} cenas, {ns} chars, "
          f"~{ns/20.02 + len(short)*0.5:.0f}s")
    print(f"bytes ............. {os.path.getsize(destino)}")
