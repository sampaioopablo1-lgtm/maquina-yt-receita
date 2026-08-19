#!/usr/bin/env python3
"""Monta a spec kolejny-poziom-008 — o mesmo pedido, duas respostas.

POR QUE 008 E NAO 007. O nome kolejny-poziom-007 ja pertencia a "Nadplacac
Kredyt czy Inwestowac", publicado em 12/08/2026. A numeracao deste canal
nunca foi sequencial — 007 e de 11/08, 003 e de 18/08 — e eu escolhi o
numero contando longos distintos em vez de olhar os nomes ja usados. A
trava do publicar.py pegou, mas so depois de 89 cenas renderizadas.

PAUTA, medida em 19/08/2026. Medi TRES eixos nesta rodada, e a comparacao
entre eles e o achado antes mesmo do roteiro:

    zdolnosc kredytowa / hipoteka    mediana 369,3 v/d   (n=14)
    forma zatrudnienia (usado no 005) mediana  72,3      (n=16)
    oszczednosci (usado no 006)       mediana  34,2      (n=12)
    ulgi podatkowe e OC                mediana   1,4      (n=14)  <- MORTO

O eixo de deducoes fiscais e seguro de carro esta 265 vezes abaixo do de
credito imobiliario. Nao construi nada nele, e fica gravado como medido-e-
morto para nao ser tentado de novo.

Outliers do eixo escolhido (>= 1108,0):

    Kupujesz mieszkanie? Mozesz przeplacic dwa razy       6564,6 v/d
    Obejrzyj to, zanim zaplacisz kolejna rate kredytu     1986,2
    Zdolnosc kredytowa, wklad wlasny i rata               1566,1

E o que mais interessa esta logo abaixo, com 893,0: "JDG ryczalt - jaki
kredyt hipoteczny przy 20 000 zl?", cuja descricao diz "tens 20 mil de
receita e achas que essa e a tua capacidade? O banco ve outra coisa
completamente". E a espinha deste canal, aplicada ao documento que quase
todo polones assina uma vez na vida.

Modelo a ESTRUTURA do topo — pergunta seguida de aviso de custo dobrado — e
nao o assunto, que la e ranking mensal de ofertas.

NUMEROS VERIFICADOS (duas fontes que batem: finwire.pl, citando NBP e GPW
Benchmark, e bankowynet.pl; acesso 19/08/2026):

    stopa referencyjna NBP   3,75%  desde 05/03/2026 (corte de 25 pb)
    lombardowa 4,25% · depozytowa 3,25% · redyskontowa 3,80%
    WIBOR 1M 3,81% · 3M 3,84% · 6M 3,84% · 12M 3,84%
    RPP manteve as taxas em abril, maio, junho e julho
    WIBOR sera substituido pelo POLSTR; nenhum contrato novo em WIBOR a
    partir de janeiro de 2028

O QUE NAO ENTRA: o video de 893 v/d cita "420 mil num banco e quase menos
noutro". Esse numero e do criador, nao de fonte institucional, entao o
roteiro descreve o FENOMENO (mesmo pedido, bancos diferentes, valores
materialmente diferentes) sem cravar cifra que eu nao possa sustentar.

SIMILARIDADE vs os sete longos distintos do canal: o mais proximo e
"Nadplacac kredyt czy inwestowac", que trata de um emprestimo que JA existe.
Este trata de quanto o banco empresta e por que a resposta varia — decisao
anterior, outro documento, outras variaveis.

SEM BROLL: o Pexels da TimeoutError a partir do runner.

TRILHA: Wholesome, a identidade do canal, agora conferida pelo portao
(aprendizado 324 — o 005 foi ao ar com a faixa errada).

DIMENSIONAMENTO. pl-PL-MarekNeural = 19,93 chars/s + 1,477 s/frase.
Alvo no MEIO da janela: ~13,2 min. Entregue: 9.804 chars em 89 cenas,
13,2 min medidos, 7 capitulos entre 93 e 123 s cada.
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
T("Ten sam wniosek", "dwie różne kwoty",
  "Ta sama osoba, ten sam dochód, ten sam miesiąc. Dwa banki i dwie zupełnie "
  "różne kwoty kredytu.",
  cap="Ten sam wniosek, dwie kwoty")
I("To nie pomyłka", "tak działa system",
  "To nie jest pomyłka ani złośliwość jednego z nich. Tak po prostu działa "
  "liczenie zdolności kredytowej.")
I("Dlaczego to boli", "planujesz na złej liczbie",
  "Problem jest praktyczny. Jeśli planujesz zakup na podstawie własnego "
  "dochodu, planujesz na liczbie, której bank nigdy nie użyje.")
I("Bank nie liczy dochodu", "liczy nadwyżkę",
  "Bank nie pyta, ile zarabiasz. Pyta, ile ci zostaje po wszystkim. To dwie "
  "różne liczby.")
I("I nie dzisiejszej raty", "tylko wyższej",
  "I nie sprawdza raty przy dzisiejszym oprocentowaniu. Sprawdza ją przy "
  "wyższym, na wypadek gdyby stopy wróciły w górę.")
I("Dziś stopa NBP", "trzy przecinek siedemdziesiąt pięć",
  "Dla kontekstu: stopa referencyjna NBP wynosi trzy przecinek siedemdziesiąt "
  "pięć procent i trzyma się na tym poziomie od marca.")
I("A WIBOR", "trzy przecinek osiemdziesiąt cztery",
  "WIBOR trzymiesięczny, od którego zależy większość rat, jest przy trzech "
  "przecinek osiemdziesięciu czterech.")
I("Ale bank liczy wyżej", "to jest bufor",
  "Bank i tak policzy twoją ratę przy stawce wyższej niż ta. I to jest "
  "pierwszy powód, dla którego twoja zdolność jest niższa, niż liczysz.")
I("Ile to zmienia", "całą listę mieszkań",
  "Różnica między jedną kwotą a drugą to nie jest szczegół w tabelce. "
  "To inna lista mieszkań, na które w ogóle patrzysz.")
L("Co zobaczymy", ["Co bank liczy zamiast dochodu",
                   "Bufor, czyli test przy wyższej stopie",
                   "Co obniża zdolność, choć o tym nie myślisz",
                   "Co ją realnie podnosi",
                   "Jak się przygotować przed wnioskiem"],
  "Pięć części. Co bank liczy zamiast dochodu. Czym jest bufor. Co obniża "
  "zdolność, choć nikt o tym nie myśli. Co ją realnie podnosi. I jak "
  "przygotować się przed złożeniem wniosku.")
I("Jedno od razu", "to nie jest doradztwo",
  "Jedno od razu. To nie jest doradztwo kredytowe i nie polecam żadnego "
  "banku. Opisujemy mechanizm.")
I("Zasada kanału", "liczby ze źródłem",
  "I obowiązuje zasada kanału. Liczby ze źródłem i datą, a czego nie da się "
  "zmierzyć, tego nie mówimy.")
T("Zaczynamy", "co bank liczy zamiast dochodu?",
  "Zacznijmy od pierwszej różnicy, bo z niej wynika reszta. Co bank liczy "
  "zamiast twojego dochodu?")

# ------------------------------------------------------------------ cap 2
T("Nadwyżka", "to, co zostaje",
  "Bank liczy nadwyżkę. Bierze twój dochód netto i odejmuje od niego "
  "wszystko, co musisz płacić co miesiąc.",
  cap="Co bank liczy zamiast dochodu")
I("Pierwsze odjęcie", "koszty utrzymania",
  "Pierwsze odjęcie to koszty utrzymania. Bank nie pyta, ile wydajesz. "
  "Przyjmuje własną kwotę na osobę w gospodarstwie.")
I("Dlatego rodzina zmienia wynik", "każda osoba kosztuje",
  "Dlatego dwie osoby o tym samym dochodzie, ale z inną liczbą dzieci, "
  "dostają różne kwoty. Każda osoba w domu ma swój koszt w tabeli banku.")
I("Drugie odjęcie", "twoje raty",
  "Drugie odjęcie to twoje obecne raty. Kredyt samochodowy albo ratalny "
  "telefon. Wszystko, co widać w rejestrze.")
I("I tu już się rozjeżdża", "każdy bank ma własną tabelę",
  "I tu zaczyna się rozjazd między bankami. Przyjmowane koszty utrzymania "
  "są wewnętrzną zasadą każdego z nich i nie są takie same.")
I("Trzecie odjęcie", "limity, nawet niewykorzystane",
  "Trzecie odjęcie zaskakuje najczęściej. Limit na karcie i debet w koncie "
  "liczą się nawet wtedy, gdy ich nie używasz.")
I("Dlaczego", "bank liczy to, co MOŻESZ wydać",
  "Bo bank nie liczy tego, co wydałeś. Liczy to, co możesz wydać jutro, bez "
  "pytania go o zgodę.")
I("A twoja umowa", "typ zatrudnienia waży",
  "Waży też forma zatrudnienia. Umowa o pracę na czas nieokreślony jest dla "
  "banku najprostsza do policzenia.")
I("Działalność", "liczona inaczej",
  "Przy własnej działalności bank nie patrzy na przychód, tylko na dochód, i "
  "często uśrednia go z kilkunastu miesięcy.")
I("Stąd ta różnica", "przychód to nie zdolność",
  "I stąd bierze się najczęstsze rozczarowanie w całym temacie. Wysoki "
  "przychód z faktur nie jest wysoką zdolnością.")
I("Zlecenie i dzieło", "liczone ostrożniej",
  "Umowa zlecenie i umowa o dzieło są liczone ostrożniej. Bank patrzy, "
  "jak długo trwają i czy powtarzają się co miesiąc.")
I("Ryczałt jeszcze inaczej", "przyjmowany procent",
  "A przy ryczałcie część banków przyjmuje ustalony procent przychodu jako "
  "dochód. Każdy bank ma tu własny procent, i to jedno z miejsc, gdzie "
  "wyniki się rozjeżdżają.")
I("Liczy się też staż", "jak długo, nie tylko ile",
  "Waży również to, jak długo masz obecny dochód. Bank chce zobaczyć "
  "historię, a nie jeden dobry miesiąc.")
T("Mamy nadwyżkę", "to skąd bufor?",
  "Wiemy już, co bank odejmuje. Ale dlaczego liczy ratę wyższą niż dzisiejsza?")

# ------------------------------------------------------------------ cap 3
T("Bufor", "test przy wyższej stopie",
  "Bank nie sprawdza, czy stać cię na dzisiejszą ratę. Sprawdza, czy będzie "
  "cię stać, jeśli stopy wzrosną.",
  cap="Bufor: test przy wyższej stopie")
I("Skąd to się wzięło", "z doświadczenia rynku",
  "Ten wymóg nie jest kaprysem banku. Jest odpowiedzią nadzoru na to, co "
  "działo się z ratami, gdy stopy szły ostro w górę.")
I("Jak to wygląda", "doliczają punkty",
  "W praktyce bank dolicza do dzisiejszego oprocentowania kilka punktów "
  "procentowych i dopiero z tego liczy ratę do testu.")
I("Efekt", "rata testowa jest wyższa",
  "Efekt jest taki, że rata w kalkulatorze banku jest wyższa niż ta, którą "
  "faktycznie zapłacisz w pierwszym miesiącu.")
I("I dlatego", "zdolność spada",
  "A skoro rata testowa jest wyższa, to zdolność wychodzi niższa. To nie "
  "błąd kalkulatora, to jego cel.")
I("Skala jest odczuwalna", "to nie jest zaokrąglenie",
  "To nie jest kosmetyka na końcu wyliczenia. Kilka punktów doliczonych "
  "do oprocentowania przesuwa ratę testową na tyle, że zmienia całą kwotę.")
I("Bufor bywa różny", "bank od banku",
  "Wysokość bufora bywa różna w różnych bankach i przy różnych typach "
  "oprocentowania. To kolejny powód, dla którego wyniki się rozjeżdżają.")
I("Stałe oprocentowanie", "zwykle liczone łagodniej",
  "Przy oprocentowaniu okresowo stałym bufor bywa mniejszy, bo przez kilka "
  "pierwszych lat rata z definicji się nie zmienia.")
I("To ma konsekwencję", "ten sam wniosek, dwie ścieżki",
  "Ta sama osoba może więc dostać różne kwoty w jednym banku, zależnie od "
  "tego, czy wybiera stałe czy zmienne.")
I("Warto to wiedzieć wcześniej", "zanim wybierzesz",
  "Warto o tym wiedzieć przed rozmową, a nie po. To pytanie, które możesz "
  "zadać sam.")
I("I jeszcze jedno", "WIBOR odchodzi",
  "I jeszcze jedna rzecz na horyzoncie. WIBOR ma zostać zastąpiony wskaźnikiem "
  "POLSTR, a nowe umowy przestaną się na nim opierać od stycznia dwa tysiące "
  "dwudziestego ósmego roku.")
I("Bufor działa też dla ciebie", "margines, nie kara",
  "Bufor bywa odbierany jako utrudnienie. Ale to jest margines na "
  "wypadek, gdyby rata wzrosła. A płacić będziesz ty.")
T("Rozumiemy bufor", "to co jeszcze obniża zdolność?",
  "Rozumiemy już mechanizm. Co jeszcze potrafi obniżyć zdolność, choć nikt "
  "o tym nie myśli?")

# ------------------------------------------------------------------ cap 4
T("Ciche obciążenia", "cztery rzeczy",
  "Są cztery rzeczy, które obniżają zdolność, a prawie nikt o nich nie myśli "
  "przed złożeniem wniosku.",
  cap="Co obniża zdolność")
I("Pierwsza", "karta z wysokim limitem",
  "Pierwsza to karta kredytowa z wysokim limitem, której nie używasz. Sam "
  "limit jest liczony jako możliwe zadłużenie.")
I("Druga", "debet w koncie",
  "Druga to debet w koncie osobistym. Ta sama logika i ten sam skutek.")
I("Trzecia", "raty na sprzęt",
  "Trzecia to raty na sprzęt, nawet zerowe. Zero procent dla ciebie wciąż "
  "jest zobowiązaniem w rejestrze.")
I("Czwarta", "częste zapytania",
  "Czwarta jest subtelniejsza. Wiele wniosków kredytowych złożonych w krótkim "
  "czasie zostawia ślad w rejestrze.")
I("Co z tego wynika", "porządki przed wnioskiem",
  "Wniosek praktyczny jest prosty. Porządki w zobowiązaniach robi się PRZED "
  "wnioskiem, nie w jego trakcie.")
I("Ile to trwa", "zamknięcie limitu nie jest natychmiastowe",
  "I warto zacząć wcześniej, bo zamknięcie limitu i aktualizacja rejestru "
  "potrzebują czasu.")
I("Jest jeszcze cudzy kredyt", "poręczenie to zobowiązanie",
  "Jest też coś, o czym łatwo zapomnieć. Kredyt, który poręczyłeś albo "
  "podpisałeś z kimś, obciąża również twoją zdolność.")
I("Jest też odwrotna strona", "historia się liczy",
  "Jest też druga strona tej samej monety. Brak jakiejkolwiek historii "
  "kredytowej też nie pomaga, bo bank nie ma czego oceniać.")
I("Czyli nie chodzi o zero", "chodzi o porządek",
  "Nie chodzi więc o to, żeby nie mieć nic. Chodzi o to, żeby twoje "
  "zobowiązania były spłacane w terminie i nie zajmowały miejsca bez powodu.")
I("I stałe płatności", "alimenty, leasing",
  "Dochodzą do tego stałe płatności spoza rejestru. Alimenty czy leasing "
  "też są odejmowane, bo co miesiąc wychodzą z konta.")
T("To jasne", "a co ją podnosi?",
  "Wiemy, co obniża. A co realnie podnosi zdolność?")

# ------------------------------------------------------------------ cap 5
T("Cztery dźwignie", "i ich koszt",
  "Są cztery sposoby, żeby podnieść zdolność. Każdy działa, i każdy ma "
  "cenę, o której warto wiedzieć.",
  cap="Co realnie ją podnosi")
I("Pierwsza", "dłuższy okres",
  "Pierwsza to wydłużenie okresu kredytowania. Rata spada, więc zdolność "
  "rośnie.")
I("Cena", "więcej odsetek w sumie",
  "Cena jest jednak realna. Przy dłuższym okresie zapłacisz więcej odsetek w "
  "całym kredycie, nawet jeśli miesięcznie jest lżej.")
I("Policz to na swoim przypadku", "suma odsetek, nie rata",
  "Wydłużenie okresu wygląda kusząco w kalkulatorze. Policz jednak sumę "
  "odsetek w obu wariantach, zanim uznasz to za wygraną.")
I("Druga", "wyższy wkład własny",
  "Druga to wyższy wkład własny. Mniejszy kredyt to mniejsza rata i często "
  "lepsza marża.")
I("Dlaczego marża spada", "mniejsze ryzyko banku",
  "Marża spada, bo bank ryzykuje mniej, gdy pożycza mniejszą część wartości "
  "nieruchomości.")
I("Trzecia", "współkredytobiorca",
  "Trzecia to dołączenie współkredytobiorcy. Dwa dochody liczą się razem.")
I("Ale uwaga", "to zobowiązanie na lata",
  "Tylko że to nie jest formalność. Współkredytobiorca odpowiada za dług tak "
  "samo jak ty, przez cały okres.")
I("Czwarta", "porządek w zobowiązaniach",
  "Czwarta to ta z poprzedniej części. Zamknięcie limitów i spłacenie "
  "drobnych rat potrafi zmienić wynik bez zmiany dochodu.")
I("Uwaga przy dwóch osobach", "jego raty też się liczą",
  "Przy dwóch osobach bank liczy oba dochody, ale też oba zestawy "
  "zobowiązań. Jeśli druga osoba ma własne raty, zysk bywa mniejszy.")
I("Co NIE działa", "podwyżka tuż przed wnioskiem",
  "A co zwykle nie działa tak, jak się liczy? Podwyżka na miesiąc przed "
  "wnioskiem. Bank chce zobaczyć dochód w dłuższym okresie.")
I("Ani zmiana pracy", "nawet na lepszą",
  "Ani zmiana pracy tuż przed wnioskiem, nawet na lepiej płatną. Świeży okres "
  "próbny jest dla banku ryzykiem, a nie awansem.")
I("Ani premia raz w roku", "liczona ostrożnie",
  "Nie działa też liczenie na premię czy nadgodziny. Dochód nieregularny "
  "bank przyjmuje częściowo albo pomija.")
T("Mamy dźwignie", "to jak się przygotować?",
  "Mamy komplet mechanizmów. Jak się z tym praktycznie przygotować?")

# ------------------------------------------------------------------ cap 6
T("Pięć kroków", "przed wnioskiem",
  "Pięć kroków, wszystkie do zrobienia zanim w ogóle wejdziesz do banku.",
  cap="Jak się przygotować")
I("Pierwszy", "pobierz swój raport",
  "Pierwszy. Pobierz własny raport z rejestru kredytowego i zobacz to, co "
  "widzi bank. Masz do niego prawo.")
I("Po co", "żeby nie było niespodzianek",
  "Nie po to, żeby coś ukryć, tylko żeby nie dowiedzieć się o starym limicie "
  "dopiero przy wniosku.")
I("Drugi", "policz swoją nadwyżkę",
  "Drugi. Policz własną nadwyżkę tak, jak liczy ją bank. Dochód netto minus "
  "koszty utrzymania minus wszystkie raty.")
I("Trzeci", "dolicz bufor sam",
  "Trzeci. Do dzisiejszego oprocentowania dolicz kilka punktów i policz ratę "
  "z tej wyższej stawki. To będzie bliżej wyniku banku.")
I("Czwarty", "sprawdź w kilku bankach",
  "Czwarty, i najważniejszy w tym temacie. Sprawdź zdolność w kilku bankach, "
  "bo to jedyny sposób, żeby zobaczyć rozrzut na własnym przypadku.")
I("I poproś o wyliczenie", "z zapisanymi założeniami",
  "Poproś też o wyliczenie z zapisanymi założeniami. Wtedy masz co "
  "porównać, zamiast pamiętać dwie kwoty z rozmowy.")
I("Piąty", "zapytaj o bufor i o stałe",
  "Piąty. Zapytaj wprost o dwie rzeczy: jaki bufor stosują i jak zmienia się "
  "kwota przy oprocentowaniu stałym.")
I("Jedna zasada przy porównaniu", "te same założenia",
  "I jedna zasada przy porównywaniu. Pytaj wszędzie o ten sam okres i ten "
  "sam wkład własny. Inaczej porównujesz dwie różne sprawy.")
I("Ile to zajmuje", "kilka dni, nie miesięcy",
  "Wszystkie pięć to kwestia kilku dni, nie miesięcy. A różnica w wyniku bywa "
  "większa niż wszystko, co ugrasz negocjując marżę.")
T("Plan gotowy", "co może go zepsuć?",
  "Plan jest gotowy. Co może go zepsuć?")

# ------------------------------------------------------------------ cap 7
T("Cztery błędy", "które psują wniosek",
  "Pierwszy błąd to traktowanie kalkulatora z internetu jak decyzji banku. To "
  "orientacja, nie wynik.",
  cap="Cztery błędy")
I("Drugi błąd", "brać pierwszą kwotę za ostateczną",
  "Drugi to przyjęcie pierwszej otrzymanej kwoty jako ostatecznej. To wynik "
  "jednego banku, przy jednym zestawie założeń.")
I("Trzeci błąd", "maksymalna zdolność jako cel",
  "Trzeci jest najdroższy. Traktowanie maksymalnej zdolności jako celu. To "
  "jest granica, a nie rekomendacja.")
I("Dlaczego", "na granicy nie ma miejsca",
  "Bo kredyt na granicy zdolności nie zostawia miejsca na remont, na "
  "przeprowadzkę ani na miesiąc bez premii.")
I("Czwarty błąd", "porządki w trakcie wniosku",
  "I czwarty. Robienie porządków w zobowiązaniach dopiero po złożeniu "
  "wniosku, gdy rejestr jeszcze ich nie widzi.")
I("Wspólny mianownik", "wszystkie cztery to pośpiech",
  "Wszystkie cztery mają ten sam mianownik. Pośpiech. Każdy z nich znika, "
  "jeśli zaczniesz kilka tygodni wcześniej.")
I("Jedno zastrzeżenie", "każdy bank ma własne zasady",
  "I jedno uczciwe zastrzeżenie. Konkretne progi, bufory i koszty utrzymania "
  "są wewnętrzne dla każdego banku i zmieniają się w czasie.")
L("Podsumowanie", ["Bank liczy nadwyżkę, nie dochód",
                   "Rata liczona przy wyższej stopie",
                   "Limity liczą się nawet nieużywane",
                   "Stopa NBP 3,75%, WIBOR 3M 3,84%",
                   "Sprawdź w kilku bankach"],
  "Pięć rzeczy do zapamiętania. Że bank liczy nadwyżkę, nie dochód. Że ratę "
  "testuje przy wyższej stopie. Że limity liczą się nawet nieużywane. "
  "Dzisiejsze wskaźniki. I że rozrzut widać dopiero w kilku bankach.")
I("Jeśli zrobisz jedną rzecz", "policz nadwyżkę",
  "Jeśli po tym filmie zrobisz jedną rzecz, policz własną nadwyżkę. Dochód "
  "netto minus koszty utrzymania minus raty.")
I("Dlaczego akurat to", "to jest liczba, którą widzi bank",
  "Bo to jest jedyna liczba z twojego budżetu, na którą bank naprawdę patrzy. "
  "Reszta to szczegóły wokół niej.")
I("I jedno na koniec", "pytanie kosztuje najmniej",
  "I jedno na koniec. Sprawdzenie zdolności w drugim banku kosztuje kilka "
  "godzin. Różnica, którą pokazuje, bywa największa w całym procesie.")
C("Kolejny Poziom", "na liczbach, nie na wrażeniach",
  "To wszystko. Kolejny Poziom, na liczbach i źródłach, nie na wrażeniach.")

SHORT = [
    {"layout": "titulo", "kicker": "Ten sam dochód", "sub": "dwie kwoty",
     "nar": "Ta sama osoba, ten sam dochód, dwa banki. I dwie zupełnie różne "
            "kwoty kredytu.", "sem_cap": True},
    {"layout": "item", "kicker": "Bo bank", "preco": "nie liczy dochodu",
     "nar": "Bank nie liczy tego, ile zarabiasz. Liczy to, ile ci zostaje.",
     "sem_cap": True},
    {"layout": "item", "kicker": "I testuje", "preco": "wyższą ratę",
     "nar": "A ratę sprawdza przy stopie wyższej niż dzisiejsza. To się "
            "nazywa bufor.", "sem_cap": True},
    {"layout": "item", "kicker": "Dziś", "preco": "NBP 3,75%",
     "nar": "Dziś stopa referencyjna NBP to trzy przecinek siedemdziesiąt "
            "pięć procent.", "sem_cap": True},
    {"layout": "item", "kicker": "I limity", "preco": "liczą się zawsze",
     "nar": "A nieużywany limit na karcie liczy się tak, jakbyś go wydał.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Pięć kroków", "sub": "na kanale",
     "nar": "Pięć kroków przed wnioskiem, w pełnym filmie.", "sem_cap": True},
]

COPY = """# Zdolność kredytowa 2026: ten sam dochód, dwa banki, dwie różne kwoty

## TYTUŁ
Zdolność Kredytowa 2026: Ten Sam Dochód, Dwa Banki, Dwie Różne Kwoty

## OPIS
Ta sama osoba, ten sam dochód, ten sam miesiąc — i dwie zupełnie różne kwoty kredytu w dwóch bankach. To nie jest pomyłka ani złośliwość jednego z nich. Tak działa liczenie zdolności kredytowej, a różnica potrafi być na tyle duża, że zmienia plan zakupu mieszkania.

Źródło nieporozumienia jest jedno: bank nie pyta, ile zarabiasz. Pyta, ile ci zostaje. Od dochodu netto odejmuje przyjęte przez siebie koszty utrzymania — własną kwotę na każdą osobę w gospodarstwie domowym — a potem wszystkie twoje raty. I jeszcze limity: karta kredytowa i debet w koncie liczą się nawet wtedy, gdy ich nie używasz, bo bank liczy nie to, co wydałeś, ale to, co możesz wydać jutro bez pytania go o zgodę.

Druga rzecz, która zaskakuje, to bufor. Bank nie sprawdza, czy stać cię na dzisiejszą ratę, tylko czy będzie cię stać przy wyższym oprocentowaniu. Dla kontekstu: stopa referencyjna NBP wynosi 3,75% i obowiązuje od 5 marca 2026, a WIBOR 3M jest w okolicach 3,84%. Bank i tak policzy twoją ratę wyżej — i dlatego wynik jego kalkulatora jest niższy, niż wychodzi z twojego. Wysokość bufora bywa różna między bankami i między oprocentowaniem stałym a zmiennym, co jest kolejnym powodem, dla którego wyniki się rozjeżdżają.

W filmie przechodzimy przez cztery ciche obciążenia, które obniżają zdolność, choć prawie nikt o nich nie myśli przed wnioskiem, oraz przez cztery dźwignie, które ją realnie podnoszą — każda z ceną, o której warto wiedzieć zawczasu. Pokazujemy też, dlaczego przy własnej działalności wysoki przychód z faktur nie jest wysoką zdolnością, a przy ryczałcie każdy bank przyjmuje własny procent przychodu jako dochód. Na koniec pięć kroków do zrobienia zanim w ogóle wejdziesz do banku, w kilka dni, nie miesięcy.

To nie jest doradztwo kredytowe i nie polecamy żadnego banku. Konkretne progi, bufory i przyjmowane koszty utrzymania są wewnętrznymi zasadami każdego banku i zmieniają się w czasie — dlatego jedyny sposób, żeby zobaczyć rozrzut na własnym przypadku, to sprawdzić zdolność w kilku miejscach.

## ROZDZIAŁY
{CAPITULOS}

## KOMENTARZ
Jedno pytanie, bo odpowiedzi bywają zaskakujące: sprawdzałeś kiedyś zdolność w więcej niż jednym banku — i jak duża była różnica? Nie musisz podawać kwot, wystarczy rząd wielkości. Zbieram odpowiedzi do następnego materiału. A jeśli chcesz ten sam rozkład zrobiony dla działalności albo dla ryczałtu, napisz który; najczęściej wskazany idzie pierwszy.

## HASHTAG
#ZdolnośćKredytowa #KredytHipoteczny #KolejnyPoziom

## TAGI
zdolnosc kredytowa, kredyt hipoteczny, wklad wlasny, bufor, wibor, stopa referencyjna nbp, rata kredytu, bik, limit na karcie, wspolkredytobiorca, jdg kredyt, ryczalt kredyt, finanse osobiste, polska, kolejny poziom

## USTAWIENIA STUDIO
- Język: polski (pl) | Kategoria: Edukacja (27)
- Nie jest przeznaczone dla dzieci
- Deklaracja treści syntetycznej: TAK (głos AI)
- Lokalizacja: Polska | Licencja: standardowa licencja YouTube
- Reklamy mid-roll: włączone (powyżej 8 minut)

## MUZYKA / LICENCJA
{TRILHA}

## ŹRÓDŁA
Wskaźniki rynkowe pochodzą z zestawień powołujących się na NBP i GPW Benchmark, zgodnych między sobą co do wartości (finwire.pl oraz bankowynet.pl, dostęp 19.08.2026): stopa referencyjna NBP 3,75% obowiązująca od 5 marca 2026 po obniżce o 25 punktów bazowych, przy czym RPP utrzymała stopy bez zmian na posiedzeniach w kwietniu, maju, czerwcu i lipcu 2026; stopa lombardowa 4,25%, depozytowa 3,25%, redyskontowa 3,80%; WIBOR 1M 3,81%, WIBOR 3M 3,84%, WIBOR 6M 3,84%, WIBOR 12M 3,84%. Informacja o zastąpieniu WIBOR wskaźnikiem POLSTR i o tym, że nowe umowy przestaną opierać się na WIBOR od stycznia 2028, pochodzi z tych samych źródeł. Opis mechanizmu liczenia zdolności — nadwyżka zamiast dochodu, przyjmowane koszty utrzymania na osobę, doliczanie bufora do oprocentowania przy teście raty, traktowanie limitów i debetu jako zobowiązań — jest opisem ZASADY, a nie parametrów konkretnego banku: progi, wysokość bufora i przyjmowane koszty są wewnętrznymi zasadami każdej instytucji, różnią się między nimi i zmieniają w czasie. Nie podajemy w tym materiale żadnej konkretnej kwoty przyznanego kredytu, ponieważ takie liczby zależą od kompletu parametrów indywidualnej sprawy. Materiał edukacyjny; nie stanowi doradztwa kredytowego, rekomendacji banku ani porady inwestycyjnej.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-008",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",  # identidade do canal, conferida pelo portao
    "paleta": {"ink": "#14213D", "c1": "#C1121F", "c2": "#457B9D", "bg": "#F1F0EA"},
    "thumb": {"l1": "TEN SAM DOCHÓD", "l2": "dwie różne kwoty"},
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p = "fabrica/specs/kolejny-poziom-008.json"
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
