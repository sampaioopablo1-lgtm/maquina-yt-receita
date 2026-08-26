#!/usr/bin/env python3
"""Monta a spec kolejny-poziom-012.

ALAVANCA ATACADA: A (conversao short -> inscrito).

NUMERO DE PARTIDA, medido neste canal e nao herdado de outro:

    kolejny-poziom-009       short    70 views   1 insc   1,429%   ret 48,0%
    kp-plan-9233-20260811    short   164 views   1 insc   0,610%   ret 38,5%
    cron-2026-08-17          short   412 views   2 insc   0,485%   ret 35,7%
    cron-2026-08-15          short  1152 views   0 insc   0,000%   ret 43,7%
    kolejny-poziom-006       short   134 views   0 insc   0,000%   ret 62,2%

O QUE DEU CERTO: o 009. Titulo "OC najtansze od dwoch lat. Zobacz to, zanim
odnowisz" — uma DECISAO COM PRAZO sobre o dinheiro de quem assiste.

O QUE NAO DEU: o short mais visto do canal inteiro, com mil cento e cinquenta
e duas views, converteu ZERO. Ele conta uma estatistica sobre o futuro do
sistema de aposentadoria — fato sobre o mundo, nao decisao de ninguem. E o
006, com a MELHOR RETENCAO do canal (62,2%), tambem converteu zero: retencao
alta nao preve conversao, e isso e um corolario novo (aprendizado 502).

O QUE EU VOU MUDAR POR CAUSA DISSO: o pacote copia a forma do 009 — uma conta
que o espectador faz num documento que ele JA TEM na mao, a fatura de luz — e
para de repetir a forma do cron, que e recitar um numero sobre o pais.

VEREDITO `liberado` (12-15 min), e a alavanca B manda ir ao PISO da faixa: 12
min, nao 15. O melhor longo deste canal tem 687 s com nove capitulos; o pior
tem 781 s com 89 cenas. Entao: menos cenas, mais capitulos — DEZ capitulos.

OS NUMEROS, e as duas rotas institucionais

  Taryfy de energia eletrica para 2026, aprovadas pelo Presidente da URE:
  media de 495,16 zl/MWh na venda, abaixo de 2025; para um domicilio que
  consome 1,8 MWh, a conta mensal sobe cerca de 3%.

    rota 1  URE — comunicado "Prezes Urzedu Regulacji Energetyki zatwierdzil
            taryfy na sprzedaz i dystrybucje energii elektrycznej na 2026 r."
            e o BIP da URE com as taryfy publicadas em 2026
    rota 2  Ministerstwo Energii (gov.pl/web/energia) e a pagina de
            prioridades P29 do governo sobre estabilizacao do preco de energia

O QUE FICOU DE FORA, e o video diz isso em voz alta

  - SE o congelamento em 500 zl/MWh vale ou nao em 2026, e ate quando. Uma
    pagina da URE se chama "Mrozenie cen energii elektrycznej - 2025", e o
    buscador CONCLUIU dai que o mecanismo acabou em 31/12/2025 — mas isso e
    inferencia do buscador, nao afirmacao de orgao nenhum. Nao achei o texto
    institucional que diga a vigencia em 2026, e conclusao de buscador nao e
    fonte. Fica de fora, e e justamente por causa dessa lacuna que o video
    ensina a LER A PROPRIA FATURA em vez de confiar na manchete.
  - A taryfa de distribuicao do operador de cada regiao. Sao varias, mudam por
    OSD, e o video manda o espectador olhar a dele em vez de citar uma media
    que nao serve para ninguem em particular.

O EIXO — como a conta de luz e formada e como se le a propria — nao aparece em
nenhum dos titulos no ar do canal, que sao sobre OC, obrigacoes do tesouro,
ryczalt, IKE e IKZE, credito, salario minimo e ZUS.
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


# ------------------------------------------- 1. Rachunek ma dwie polowy
T("Twój rachunek", "ma dwie połowy",
  "Twój rachunek za prąd składa się z dwóch osobnych części. W wiadomościach "
  "mówią prawie wyłącznie o jednej z nich, i to nie zawsze o tej większej.",
  cap="Rachunek ma dwie połowy")
L("Dwie części", ["Sprzedaż energii — to, co zużyłeś",
                  "Dystrybucja — to, że w ogóle dojechała",
                  "Do tego podatki i opłaty stałe"],
  "Pierwsza to sprzedaż samej energii. Druga to dystrybucja, czyli opłata za "
  "to, że ta energia w ogóle dojechała do twojego gniazdka.")
T("Obie zatwierdza", "ten sam urząd",
  "Obie zatwierdza ten sam urząd — Prezes Urzędu Regulacji Energetyki. I obie "
  "mają własną taryfę, ustalaną osobno.")
T("Dlatego nagłówek", "nie mówi ci wszystkiego",
  "Dlatego nagłówek o tym, że prąd tanieje, może być prawdziwy, a twój "
  "rachunek i tak urośnie. To nie jest sprzeczność. To są dwie różne liczby.")
T("Zacznijmy od pytania", "na które mało kto umie odpowiedzieć",
  "Zanim przejdziemy dalej, zadaj sobie pytanie: ile dokładnie płacisz za "
  "jedną kilowatogodzinę? Nie za miesiąc, tylko za jednostkę.")
T("Prawie nikt nie wie", "i to nie jest niczyja wina",
  "Prawie nikt nie zna tej liczby, i to nie jest lenistwo. Faktura jej wprost "
  "nie podaje, bo składa się z pozycji, które trzeba dopiero zsumować.")
I("Czego się tu nauczysz", "policzyć własną cenę za megawatogodzinę",
  "Pod koniec będziesz umiał wyliczyć własną cenę za megawatogodzinę z "
  "faktury, którą już masz w domu. Nie z mojej średniej — ze swojej.")

# ------------------------------------------ 2. Ile zatwierdzono na 2026
T("Zacznijmy od liczby", "którą właśnie zatwierdzono",
  "Zacznijmy od konkretu, bo bez niego reszta to opowieść. Prezes URE "
  "zatwierdził taryfy na sprzedaż i dystrybucję energii elektrycznej na "
  "dwa tysiące dwudziesty szósty rok.",
  cap="Ile zatwierdzono na 2026")
I("Średnia cena sprzedaży", "czterysta dziewięćdziesiąt pięć złotych",
  "Średnia zatwierdzona cena sprzedaży energii to czterysta dziewięćdziesiąt "
  "pięć złotych i szesnaście groszy za megawatogodzinę.")
T("I to jest mniej", "niż rok wcześniej",
  "I ta liczba jest niższa niż w roku poprzednim. To nie jest podwyżka ceny "
  "samej energii — to obniżka.")
I("A mimo to rachunek", "rośnie o około trzy procent",
  "A mimo to przeciętny rachunek rośnie. Dla gospodarstwa zużywającego "
  "jeden i osiem dziesiątych megawatogodziny wzrost wynosi około trzech "
  "procent miesięcznie.")
T("Ta jedna sprzeczność", "jest całym tematem",
  "Cena energii spada, a rachunek rośnie. Ta pozorna sprzeczność jest właśnie "
  "całym tematem tego filmu, i wyjaśnia ją druga połowa rachunku.")
T("Zwróć uwagę na słowo", "średnia",
  "Zwróć uwagę na jedno słowo: średnia. To jest średnia po zatwierdzonych "
  "taryfach, a nie cena, którą zobaczysz na swojej fakturze.")
T("Twoja może być inna", "w obie strony",
  "Twoja może być inna, i to w obie strony. Za chwilę pokażę, od czego to "
  "zależy i jak sprawdzić, po której stronie tej średniej jesteś.")
T("Trzy procent", "to nie jest dużo",
  "Trzy procent to mniej więcej tyle, ile wynosi ogólny wzrost cen. Czyli "
  "prąd nie drożeje szybciej niż reszta twojego życia. To dobra wiadomość.")

# ------------------------------------------- 3. Dystrybucja, druga polowa
T("Druga połowa", "ta cichsza",
  "Przejdźmy do drugiej połowy, tej cichszej. Dystrybucja to nie jest opłata "
  "za prąd. To opłata za sieć, którą on płynie.",
  cap="Dystrybucja, ta cichsza połowa")
L("Za co dokładnie", ["Za utrzymanie linii i stacji",
                      "Za straty energii po drodze",
                      "Za moc, którą masz zamówioną"],
  "Płacisz za utrzymanie linii i stacji, za energię, która ginie po drodze, "
  "oraz za moc, którą masz przypisaną do przyłącza.")
T("Ta opłata", "nie zależy od tego, ile zużyjesz",
  "I tu jest sedno: spora część tej opłaty nie zależy od tego, ile prądu "
  "zużyjesz. Zapłacisz ją nawet wtedy, gdy wyjedziesz na miesiąc.")
I("Dlatego oszczędzanie", "działa tylko na połowę rachunku",
  "Dlatego gaszenie światła obniża tylko jedną połowę twojego rachunku. "
  "Druga stoi w miejscu, niezależnie od twoich starań.")
T("Pomyśl o tym", "jak o dostawie",
  "Najprościej myśleć o tym jak o zakupach z dostawą. Osobno płacisz za "
  "towar, osobno za to, że ktoś go przywiózł pod drzwi.")
T("Towar potaniał", "kurier niekoniecznie",
  "Towar w tym roku potaniał. Czy kurier też — to zupełnie osobna umowa, "
  "z osobnym cennikiem, zatwierdzanym w osobnej decyzji.")
T("Twoja taryfa dystrybucyjna", "zależy od regionu",
  "Twoja taryfa dystrybucyjna zależy od operatora, który obsługuje twój "
  "region. Nie ma jednej wspólnej dla kraju, więc nie podam ci tu jednej "
  "liczby, bo byłaby nieprawdziwa dla większości słuchających.")
T("Podam coś lepszego", "sposób na własną",
  "Podam ci coś praktyczniejszego niż średnia: sposób, żebyś odczytał swoją "
  "własną. Zajmie ci to jedną kartkę i dwie minuty.")

# ------------------------------------------- 4. Jak policzyc swoja cene
T("Weź fakturę", "i jeden długopis",
  "Weź ostatnią fakturę za prąd. Papierową albo z aplikacji, obojętnie. "
  "Potrzebujesz z niej dokładnie trzech liczb.",
  cap="Jak policzyć swoją cenę")
L("Trzy liczby", ["Kwota do zapłaty, razem z podatkiem",
                  "Zużycie w kilowatogodzinach",
                  "Liczba dni okresu rozliczeniowego"],
  "Kwota do zapłaty razem z podatkiem. Zużycie w kilowatogodzinach. I liczba "
  "dni, których dotyczy ten rachunek.")
I("Pierwsze działanie", "kwota podzielona przez zużycie",
  "Podziel kwotę przez zużycie. Wynik to twoja rzeczywista cena za jedną "
  "kilowatogodzinę, ze wszystkim w środku.")
I("Drugie działanie", "razy tysiąc",
  "Pomnóż wynik przez tysiąc. Teraz masz swoją cenę za megawatogodzinę — tę "
  "samą jednostkę, w której podaje się taryfy.")
T("Porównaj", "z zatwierdzoną ceną sprzedaży",
  "Porównaj to z zatwierdzoną ceną sprzedaży. Twoja liczba będzie wyraźnie "
  "wyższa, i to jest normalne — bo zawiera też dystrybucję, opłaty stałe i "
  "podatek.")
T("Różnica między nimi", "to twoja druga połowa",
  "Ta różnica to właśnie twoja druga połowa rachunku, wyrażona w złotówkach. "
  "Pierwszy raz widzisz ją jako konkretną liczbę, a nie jako pojęcie.")
T("Uwaga na okres", "faktury bywają dwumiesięczne",
  "Uwaga na jedną pułapkę: część faktur obejmuje dwa miesiące, a część "
  "zawiera prognozę zamiast odczytu. Sprawdź, którą trzymasz w ręku.")
I("Licz zawsze z odczytu", "nie z prognozy",
  "Licz zawsze z faktury rozliczeniowej, opartej na rzeczywistym odczycie. "
  "Prognoza pokaże ci cenę wymyśloną, a nie zapłaconą.")
T("Zrób to raz", "i wracaj do tej liczby",
  "Zrób to raz, zapisz wynik z datą, i wracaj do tej liczby przy każdej "
  "kolejnej fakturze. To jedyny sposób, żeby zauważyć zmianę wcześniej niż "
  "po roku.")

# --------------------------------------- 5. Taryfa a oferta sprzedawcy
T("Taryfa to nie to samo", "co oferta",
  "Teraz rzecz, która myli najwięcej osób. Zatwierdzona taryfa i oferta "
  "twojego sprzedawcy to dwie różne rzeczy.",
  cap="Taryfa to nie oferta")
T("Taryfa", "jest zatwierdzana z urzędu",
  "Taryfa jest zatwierdzana przez regulatora i obowiązuje tych, którzy nie "
  "podpisali nic innego. To jest ustawienie domyślne.")
T("Oferta", "jest umową, którą podpisałeś",
  "Oferta to umowa, którą podpisałeś sam — często na dwa albo trzy lata, "
  "często z ceną gwarantowaną, czasem przez telefon.")
I("I dlatego", "możesz płacić więcej mimo obniżki",
  "I dlatego możesz płacić więcej, mimo że zatwierdzona cena spadła. Twoja "
  "umowa po prostu nie jest do niej przypięta.")
T("Sprawdź na fakturze", "nazwę swojej taryfy",
  "Na fakturze jest nazwa twojej taryfy albo produktu. Jeśli widzisz nazwę "
  "handlową zamiast symbolu taryfy, jesteś na ofercie, nie na taryfie.")
T("Sprawdź też datę", "końca umowy",
  "Poszukaj na fakturze albo w umowie daty jej zakończenia. To jest jedyny "
  "moment, w którym możesz odejść bez kosztów.")
I("Zapisz tę datę", "w kalendarzu, z wyprzedzeniem",
  "Zapisz ją w kalendarzu z miesięcznym wyprzedzeniem. Umowy, które nikt nie "
  "pilnuje, przedłużają się same, i zwykle nie na twoją korzyść.")
T("To nie znaczy", "że oferta jest zła",
  "To nie znaczy, że oferta jest zła. Znaczy tylko, że obniżka z nagłówka "
  "ciebie nie dotyczy, i że warto o tym wiedzieć przed końcem umowy.")

# ---------------------------------------- 6. Czego tu nie powiem
T("Teraz uczciwie", "czego wam nie powiem",
  "Teraz część, którą większość materiałów pomija. Powiem wam, czego NIE "
  "wiem, bo to zmienia sposób, w jaki powinniście korzystać z tego filmu.",
  cap="Czego tu nie powiem")
T("Był mechanizm", "mrożenia ceny",
  "Przez ostatnie lata działał mechanizm mrożenia ceny energii dla "
  "gospodarstw domowych, na poziomie pięciuset złotych za megawatogodzinę.")
I("Czy działa w 2026", "tego nie potwierdziłem",
  "Czy on obowiązuje w tym roku i do kiedy — tego nie potwierdziłem w źródle "
  "instytucjonalnym. Znalazłem stronę opisującą rok poprzedni, i to nie jest "
  "to samo.")
T("Mogłem zgadnąć", "i nie zgadłem",
  "Mogłem wyciągnąć wniosek z tego, że zatwierdzona cena jest niższa niż "
  "próg mrożenia. Ale wniosek to nie jest źródło, a wy zasługujecie na "
  "różnicę między jednym a drugim.")
T("Mówię o tym głośno", "bo to zmienia użycie",
  "Mówię o tym wprost, bo to zmienia sposób, w jaki powinieneś użyć tego "
  "filmu. Metoda liczenia z faktury działa niezależnie od tego, czy jakiś "
  "mechanizm nadal obowiązuje.")
T("Liczba z nagłówka", "starzeje się szybciej niż metoda",
  "Liczba z nagłówka starzeje się w kilka miesięcy. Sposób odczytania "
  "własnego rachunku nie starzeje się wcale.")
T("Dlatego cały ten film", "prowadzi do twojej faktury",
  "I właśnie dlatego cały ten film prowadzi cię do twojej własnej faktury. "
  "Dokument, który masz w domu, wie o twoim rachunku więcej niż każdy "
  "nagłówek, łącznie z moim.")

# ------------------------------------------ 7. Zuzycie, jedyna dzwignia
T("Jedna liczba", "na którą masz wpływ",
  "Z całego rachunku jest dokładnie jedna liczba, na którą masz realny wpływ. "
  "Nie jest to cena i nie jest to taryfa. To zużycie.",
  cap="Zużycie, jedyna dźwignia")
T("Ceny ustala regulator", "umowę podpisałeś kiedyś",
  "Cenę ustala regulator. Umowę podpisałeś kiedyś tam. Dystrybucja zależy od "
  "regionu. Zostaje ci zużycie, i tylko ono.")
I("Zacznij od licznika", "dwa odczyty, tydzień odstępu",
  "Zacznij prosto: spisz stan licznika dzisiaj i za tydzień. Różnica podzielona "
  "przez siedem to twoje realne zużycie dobowe.")
T("Teraz masz punkt odniesienia", "swój, nie cudzy",
  "Teraz masz punkt odniesienia. Każda zmiana w domu — nowe urządzenie, inne "
  "nawyki, inna pora grzania wody — jest mierzalna wobec tej liczby.")
T("Bez tego", "oszczędzasz na wyczucie",
  "Bez tego oszczędzasz na wyczucie, a rachunek przychodzi raz na dwa "
  "miesiące i nie mówi ci, co konkretnie zadziałało.")
T("Największe pozycje", "zwykle grzeją albo chłodzą",
  "W większości mieszkań największe pozycje to urządzenia, które grzeją albo "
  "chłodzą. Nie te, które świecą.")
T("Zacznij pomiar od nich", "a nie od żarówek",
  "Więc jeśli masz zmierzyć wpływ jednej zmiany, zacznij od nich. Efekt "
  "będzie widoczny w tygodniowym odczycie, a nie po roku.")
I("I pamiętaj o proporcji", "połowa rachunku nie drgnie",
  "I pamiętaj o proporcji z wcześniejszego rozdziału: nawet duża oszczędność "
  "zużycia rusza tylko jedną połowę rachunku.")

# ------------------------------------- 8. Kiedy zmiana sprzedawcy ma sens
T("Zmiana sprzedawcy", "kiedy naprawdę się opłaca",
  "Skoro oferta bywa droższa od taryfy, to czy zmieniać sprzedawcę? "
  "Odpowiedź brzmi: tylko po policzeniu, i tylko na jednej podstawie.",
  cap="Kiedy zmiana ma sens")
T("Porównuj cenę końcową", "nie hasło reklamowe",
  "Porównuj wyłącznie cenę końcową za kilowatogodzinę, tę policzoną wcześniej "
  "z faktury. Nigdy hasła w reklamie.")
L("Sprawdź też trzy rzeczy", ["Czy jest opłata handlowa co miesiąc",
                              "Na ile lat wiąże cię umowa",
                              "Ile kosztuje wcześniejsze zerwanie"],
  "Sprawdź, czy dochodzi stała opłata handlowa co miesiąc, na ile lat wiąże "
  "cię umowa, i ile kosztuje wcześniejsze zerwanie.")
I("Bardzo częsty błąd", "niższa cena, wyższy rachunek",
  "Bardzo częsty błąd wygląda tak: cena za kilowatogodzinę niższa, opłata "
  "handlowa doliczona, i rachunek wychodzi wyższy niż był.")
T("Policz w złotówkach", "na cały rok",
  "Zamień różnicę cen na złotówki w skali roku. Grosze przy kilowatogodzinie "
  "wyglądają nieistotnie, dopóki nie pomnożysz ich przez roczne zużycie.")
T("Dopiero wtedy widać", "czy to warte podpisu",
  "Dopiero ta kwota mówi, czy warto podpisywać kolejną wieloletnią umowę. "
  "Czasem wychodzi tyle, co jedna kolacja na mieście.")
I("Sprawdź jeszcze jedno", "czy cena jest gwarantowana",
  "Sprawdź też, czy cena jest gwarantowana na cały okres, czy tylko na "
  "pierwszy rok. To jest najczęstsza różnica między ofertą, która się opłaca, "
  "a taką, która wygląda, że się opłaca.")
T("Dystrybucja się nie zmienia", "cokolwiek podpiszesz",
  "I jeszcze jedno: zmieniając sprzedawcę nie zmieniasz operatora sieci. "
  "Druga połowa rachunku zostaje dokładnie taka sama.")

# ------------------------------------------------- 9. Co zrobic w tygodniu
T("Plan na ten tydzień", "cztery kroki",
  "Zbierzmy to w plan na ten tydzień. Cztery kroki, wszystkie krótkie, i "
  "wszystkie na twoich liczbach.",
  cap="Plan na ten tydzień")
L("Krok pierwszy i drugi", ["Policz swoją cenę końcową z faktury",
                            "Sprawdź, czy jesteś na taryfie czy na ofercie"],
  "Pierwszy: policz swoją cenę końcową z ostatniej faktury. Drugi: sprawdź na "
  "niej, czy jesteś na taryfie, czy na ofercie handlowej.")
L("Krok trzeci i czwarty", ["Spisz licznik dziś i za tydzień",
                            "Zapisz obie liczby razem z datą"],
  "Trzeci: spisz stan licznika dziś i za tydzień. Czwarty: zapisz obie liczby "
  "razem z datą, w jednym miejscu, do którego wrócisz.")
T("Wszystko na jednej kartce", "albo w jednej notatce",
  "Trzymaj to w jednym miejscu: kartka na lodówce albo jedna notatka w "
  "telefonie. Cztery liczby i cztery daty, nic więcej.")
T("To zajmie", "kwadrans w sumie",
  "Cały ten plan zajmuje razem najwyżej kwadrans. To mało jak na jedyny "
  "stały rachunek, którego wysokości większość ludzi nie zna.")
T("Nie musisz nic zmieniać", "żeby to zrobić",
  "Zwróć uwagę, że żaden z tych kroków nie wymaga, żebyś cokolwiek zmieniał, "
  "podpisywał ani anulował. Wszystkie cztery to samo mierzenie.")
T("Decyzja przychodzi później", "i z liczbą w ręku",
  "Decyzja przychodzi dopiero potem, i przychodzi z liczbą w ręku zamiast z "
  "przeczuciem. To jest cała zmiana, którą ten film ma zrobić.")
T("Za dwa miesiące", "będziesz mieć porównanie",
  "Przy następnej fakturze powtórzysz pierwszy krok i po raz pierwszy "
  "zobaczysz kierunek zmiany, zamiast zgadywać z nagłówków.")
T("To jest cała różnica", "między wiedzą a wrażeniem",
  "To jest cała różnica między wiedzą o swoim rachunku a wrażeniem, że "
  "chyba drożeje.")

# ------------------------------------------------------- 10. Zamkniecie
T("Na koniec", "jedno zdanie do zapamiętania",
  "Na koniec jedno zdanie, które warto zapamiętać nawet jeśli zapomnisz "
  "wszystkich liczb z tego filmu.",
  cap="Jedno zdanie na koniec")
T("Cena energii spadła", "rachunek i tak może rosnąć",
  "Zatwierdzona cena energii spadła, a rachunek i tak może rosnąć, bo "
  "składa się z dwóch części, i tylko o jednej mówią głośno.")
T("Średnia krajowa", "nie płaci twojego rachunku",
  "Średnia krajowa jest ciekawa, ale to nie ona przychodzi do ciebie co dwa "
  "miesiące. Twoją fakturę płacisz ty, i ona ma własne liczby.")
T("A dwie połowy", "trzeba oglądać osobno",
  "I ostatnia rzecz: te dwie połowy trzeba oglądać osobno. Zsumowane w jedną "
  "kwotę ukrywają dokładnie to, co chciałbyś zobaczyć.")
I("Sprawdzaj u siebie", "nie w nagłówku",
  "Więc sprawdzaj u siebie, nie w nagłówku. Twoja faktura jest jedynym "
  "źródłem, które dotyczy dokładnie ciebie.")
T("Jeżeli zapamiętasz jedno", "niech to będzie działanie",
  "A jeżeli masz zapamiętać dokładnie jedną rzecz, niech to nie będzie "
  "czterysta dziewięćdziesiąt pięć złotych. Niech to będzie dzielenie kwoty "
  "przez zużycie.")
T("Bo liczba się zmieni", "a działanie zostanie",
  "Bo tamta liczba zmieni się za rok. To działanie będzie działać dalej, "
  "przy każdej fakturze i przy każdej taryfie.")
C("Policz to dzisiaj", "i napisz, ile ci wyszło",
  "Policz swoją cenę końcową dzisiaj i napisz w komentarzu, ile ci wyszło. "
  "Jeśli takie liczenie ci się przydaje, zostaw subskrypcję — tu każda liczba "
  "zamienia się w działanie, które robisz sam.")


# ---------------------------------------------------------------------------
# O SHORT copia a forma do 009 (o unico que converteu neste canal) e, pelo
# aprendizado 493, NAO fecha sozinho: entrega a conta e manda o resto ao longo.
SHORT = [
    {"layout": "titulo", "kicker": "Cena prądu spadła", "sub": "a rachunek rośnie",
     "nar": "Zatwierdzona cena prądu na ten rok spadła. A twój rachunek i tak "
            "rośnie. To nie pomyłka.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Bo rachunek", "sub": "ma dwie połowy",
     "nar": "Bo rachunek ma dwie połowy: sprzedaż energii i dystrybucję. "
            "Nagłówki mówią tylko o pierwszej.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Druga połowa", "sub": "nie zależy od zużycia",
     "nar": "Druga nie zależy od tego, ile zużyjesz. Zapłacisz ją nawet "
            "wyjeżdżając na miesiąc.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Twoja własna cena",
     "sub": "kwota podzielona przez zużycie",
     "nar": "Weź fakturę. Podziel kwotę do zapłaty przez zużycie w "
            "kilowatogodzinach. To twoja prawdziwa cena.", "sem_cap": True},
    {"layout": "cta", "kicker": "Reszta liczb", "sub": "w pełnym filmie",
     "nar": "Co z tą liczbą zrobić, i jak sprawdzić, czy jesteś na taryfie czy "
            "na ofercie, pokazuję w pełnym filmie pod linkiem niżej.",
     "sem_cap": True},
]

THUMB = {"l1": "cena spadła", "l2": "rachunek rośnie"}

COPY = """# Cena energii spadła i rachunek urósł — bo to są dwie różne liczby

## TITULO
Prąd Stanieje w 2026, a Rachunek Urośnie: Policz Swoją Cenę z Własnej Faktury

## DESCRICAO
Prezes Urzędu Regulacji Energetyki zatwierdził taryfy na sprzedaż i dystrybucję energii elektrycznej na 2026 rok. Średnia zatwierdzona cena sprzedaży energii wynosi 495,16 zł/MWh i jest niższa niż rok wcześniej. Mimo to przeciętny rachunek rośnie: dla gospodarstwa domowego zużywającego 1,8 MWh wzrost wynosi około 3% miesięcznie, czyli mniej więcej tyle, co ogólny wzrost cen.

Cena spada, a rachunek rośnie — i to nie jest sprzeczność. Rachunek za prąd składa się z dwóch osobnych części, zatwierdzanych osobno przez ten sam urząd: sprzedaży samej energii oraz dystrybucji, czyli opłaty za to, że energia dojechała do gniazdka. Nagłówki mówią prawie wyłącznie o pierwszej.

Druga połowa ma własność, która zmienia sposób oszczędzania: spora jej część nie zależy od zużycia. Zapłacisz ją nawet wtedy, gdy wyjedziesz na miesiąc. Dlatego gaszenie światła obniża tylko jedną połowę rachunku, a druga stoi w miejscu niezależnie od starań.

Film prowadzi do rachunku widza, nie do średniej krajowej. Z faktury, którą masz w domu, potrzebujesz trzech liczb: kwoty do zapłaty z podatkiem, zużycia w kilowatogodzinach i liczby dni okresu rozliczeniowego. Kwota podzielona przez zużycie daje rzeczywistą cenę za kilowatogodzinę ze wszystkim w środku; razy tysiąc — cenę za megawatogodzinę, czyli tę samą jednostkę, w której podaje się taryfy. Różnica wobec zatwierdzonej ceny sprzedaży to twoja druga połowa rachunku, wyrażona w złotówkach.

Osobny rozdział wyjaśnia różnicę między taryfą a ofertą: taryfa jest zatwierdzana przez regulatora i obowiązuje tych, którzy nie podpisali nic innego; oferta to umowa podpisana samodzielnie, często na kilka lat i z ceną gwarantowaną. Dlatego obniżka z nagłówka może ciebie nie dotyczyć — a na fakturze widać, po której stronie jesteś.

Na koniec: plan na tydzień w czterech krokach, oraz warunki, przy których zmiana sprzedawcy naprawdę się opłaca — z ostrzeżeniem o stałej opłacie handlowej, która potrafi podnieść rachunek mimo niższej ceny za kilowatogodzinę.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Policz swoją cenę końcową z ostatniej faktury i napisz tu, ile ci wyszło — razem z regionem, bo taryfa dystrybucyjna zależy od operatora. Ciekawi mnie, jak duży jest naprawdę rozrzut między regionami, bo to jedyna część tej układanki, której nie da się podać jedną liczbą dla całego kraju.

## HASHTAGS
#RachunekZaPrąd #EnergiaElektryczna #KolejnyPoziom

## TAGS
rachunek za prad, cena energii 2026, taryfa ure, dystrybucja energii, jak obliczyc cene pradu, zmiana sprzedawcy energii, oplata handlowa, licznik energii, oszczedzanie pradu, taryfa g11, faktura za prad, urzad regulacji energetyki, koszty energii w domu, finanse osobiste, kolejny poziom

## CONFIGURACAO DE STUDIO
- Idioma: Polski (pl) | Categoria: Educação (27)
- Não é conteúdo para crianças
- Divulgação de conteúdo alterado ou sintético: SIM (voz gerada por IA)
- Local: Polônia | Licença: Licença padrão do YouTube
- Anúncios mid-roll: ligado (duração acima de oito minutos)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
Sprawdzone 26 sierpnia 2026 r. Liczby w tym filmie pochodzą z dwóch niezależnych źródeł instytucjonalnych: (1) Urząd Regulacji Energetyki — komunikat o zatwierdzeniu taryf na sprzedaż i dystrybucję energii elektrycznej na 2026 r. oraz BIP URE z taryfami opublikowanymi w 2026 r.: średnia zatwierdzona cena sprzedaży 495,16 zł/MWh, niższa niż rok wcześniej, przy wzroście przeciętnego rachunku o około 3% miesięcznie dla gospodarstwa zużywającego 1,8 MWh; (2) Ministerstwo Energii na gov.pl oraz rządowa strona priorytetu dotyczącego stabilizacji cen energii elektrycznej dla gospodarstw domowych.

CZEGO W TYM FILMIE NIE MA I DLACZEGO. (a) Nie twierdzę, czy mechanizm mrożenia ceny na poziomie 500 zł/MWh obowiązuje w 2026 r. ani do kiedy. Znalazłem stronę URE opisującą rok 2025, a to nie jest to samo. Z faktu, że zatwierdzona cena jest niższa od progu mrożenia, można wyciągnąć wniosek — ale wniosek nie jest źródłem, i film mówi to wprost zamiast zgadywać. Właśnie ta luka jest powodem, dla którego cały materiał prowadzi do odczytania własnej faktury, a nie do zaufania nagłówkowi. (b) Nie podaję jednej stawki dystrybucyjnej: zależy ona od operatora obsługującego dany region, więc średnia krajowa nie opisywałaby rachunku żadnego konkretnego widza. Zamiast niej film podaje sposób wyliczenia własnej stawki z faktury. (c) Nazwy i warunki ofert handlowych zmieniają się w trakcie roku — film opisuje różnicę między taryfą a ofertą, nie ocenia konkretnych produktów. Nie ma tu porady inwestycyjnej ani rekomendacji wyboru sprzedawcy.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-012",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#E4572E", "c2": "#F5B841", "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "kolejny-poziom-012.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
