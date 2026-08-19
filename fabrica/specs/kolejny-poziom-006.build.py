#!/usr/bin/env python3
"""Monta a spec kolejny-poziom-006 — seis ofertas, uma perde para a inflacao.

PAUTA, medida em 19/08/2026. Doze videos poloneses de 90 dias sobre onde
guardar dinheiro, mediana 34,2 v/d:

    Czy Polacy przestaja wierzyc w nieruchomosci?          1682,8 v/d  *
    Gdzie trzymac pieniadze w 2026? Ranking 5 opcji         217,9
    Dlaczego ceny nie spadly, mimo spadku inflacji           71,9
    Mieszkania znowu drozeja                                 54,7
    Dokad Przeniesc Pieniadze Na Krotko                      36,3
    Inflacja zjada gotowke na koncie                         32,1
    Obligacje Skarbowe 2026: Jak Kupic, Ktore Wybrac         14,6
    Czym sa obligacje skarbowe?                               5,3

    * 1,7 dia de vida — fora da leitura pela regra das 48h. Fica no banco,
      marcado, para reconferir depois de 21/08.

O outlier valido e o RANKING de cinco opcoes com aviso ("jedna cie ZDRADZI"),
217,9 v/d, seis vezes a mediana. E o par dentro do mesmo eixo repete o que ja
medi tres vezes hoje: o TUTORIAL de obrigacoes ("jak kupic, ktore wybrac")
fez 14,6, e o "czym sa obligacje" fez 5,3 — quinze e quarenta vezes menos que
a comparacao com veredito. Quarta medicao, quarto eixo: comparar e decidir
bate explicar.

Modelo a ESTRUTURA do outlier — N opcoes enfileiradas com um aviso de qual
falha — e nao o assunto, que la era um ranking generico de lugares.

O ACHADO, e ele e aritmetica de duas subtracoes. O Ministerio das Financas
publica a taxa NOMINAL. Antes de sobrar alguma coisa acontecem duas coisas:
o imposto Belka leva 19% dos juros, e a inflacao leva o resto do poder de
compra. Com a inflacao de julho em 3,0%, o limiar para EMPATAR e

    3,0 dividido por 0,81  =  3,70% nominal

Abaixo disso o dinheiro encolhe mesmo rendendo. E a obrigacao de tres meses,
a mais curta e a que parece mais segura, rende 2,00% — ou seja, 1,62% depois
do imposto, contra 3,0% de inflacao. Perde por quase um ponto e meio ao ano,
com o selo do Tesouro.

NUMEROS VERIFICADOS. Oferta de agosto de 2026, do proprio Ministerio das
Financas (gov.pl) e reproduzida com os mesmos valores por strefainwestorow.pl
(acesso 19/08/2026):

    OTS  3 meses   2,00% fixo
    ROR  1 ano     4,00% no primeiro mes, depois taxa de referencia do NBP,
                   margem 0,00%
    DOR  2 anos    4,15% no primeiro periodo, margem 0,15%
    TOS  3 anos    4,40% fixo
    COI  4 anos    4,75% no primeiro ano, depois inflacao + 1,50%
    EDO  10 anos   5,35% no primeiro ano, depois inflacao + 2,00%
    troca (zamiana): titulo novo a 99,90 zl em vez de 100, menos a OTS
    venda de junho: 8,6 bilhoes de zloty, recorde em mais de um ano

Inflacao CPI de julho de 2026, GUS: 3,0% no ano, mais 0,8% no mes — puxada
por combustivel depois da volta do IVA de 23%. Imposto Belka: 19%.

SIMILARIDADE vs os seis longos distintos do canal (aposentadoria do ZUS,
plano com salario medio, amortizar vs investir, taxas e Belka em aporte
mensal, IKE vs IKZE, custo do empregador vs liquido): o video da Belka
tratava de EROSAO de um aporte mensal em 30 anos; este trata de ESCOLHA
entre seis instrumentos para um valor parado. Horizonte diferente, decisao
diferente, instrumentos que o canal nunca nomeou.

A ponte com o video de ontem aparece uma vez: la a diferenca era entre custo
e liquido, aqui entre taxa e o que sobra. Mesmo musculo, documento diferente.

SEM BROLL: o Pexels da TimeoutError a partir do runner.

DIMENSIONAMENTO. pl-PL-MarekNeural = 19,93 chars/s + 1,477 s/frase.
Validado ontem: previu 12,5 e saiu 12,2. Alvo no MEIO da janela: ~13,2 min.
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
T("Sześć ofert", "jedna przegrywa",
  "Ministerstwo Finansów wystawiło w sierpniu sześć rodzajów obligacji "
  "oszczędnościowych. Pięć z nich chroni twoje pieniądze. Jedna nie.",
  cap="Sześć ofert, jedna przegrywa")
I("Która", "ta najkrótsza",
  "I to nie jest ta, którą byś obstawił. Przegrywa ta najkrótsza, "
  "trzymiesięczna. Czyli ta, która wygląda najbezpieczniej.")
I("Dlaczego", "dwa odejmowania",
  "Powód nie jest w ofercie. Jest w dwóch odejmowaniach, które dzieją się "
  "po niej.")
I("Pierwsze", "podatek Belki",
  "Pierwsze odejmowanie to podatek Belki. Dziewiętnaście procent od "
  "odsetek, pobierane automatycznie.")
I("Drugie", "inflacja",
  "Drugie to inflacja. W lipcu wyniosła trzy procent w skali roku, według "
  "GUS.")
I("Po obu", "zostaje mniej niż widzisz",
  "Dopiero po obu wiadomo, ile naprawdę zostało. I to jest zawsze mniej, "
  "niż mówi tabelka.")
I("Jest próg", "trzy przecinek siedemdziesiąt",
  "Z tych dwóch liczb wychodzi jeden próg. Żeby wyjść na zero, obligacja "
  "musi dać co najmniej trzy przecinek siedemdziesiąt procent.")
I("Poniżej niego", "tracisz, mimo odsetek",
  "Poniżej tego progu tracisz siłę nabywczą, mimo że dostajesz odsetki. "
  "Rachunek rośnie, a zakupy się kurczą.")
I("Dla kogo to jest", "dla każdego, kto ma odłożone",
  "I dotyczy każdego, kto ma cokolwiek odłożone na koncie. Nie trzeba mieć "
  "dużo, żeby ta arytmetyka działała przeciwko tobie.")
L("Co zobaczymy", ["Czym są obligacje oszczędnościowe",
                   "Sześć ofert sierpnia, po kolei",
                   "Dwa odejmowania i próg 3,70%",
                   "Która przegrywa i o ile",
                   "Jak wybrać: horyzont, nie oprocentowanie"],
  "Pięć części. Czym te obligacje są. Sześć ofert po kolei. Dwa odejmowania "
  "i próg. Która przegrywa i o ile. I jak wybierać, żeby nie patrzeć na samo "
  "oprocentowanie.")
I("Jedno od razu", "to nie jest rekomendacja",
  "Jedno od razu. To nie jest rekomendacja zakupu i nie namawiam do niczego. "
  "Czytamy ofertę i liczymy.")
I("Zasada kanału", "liczby ze źródłem",
  "I obowiązuje zasada kanału. Liczby ze źródłem i datą, a czego nie da się "
  "zmierzyć, tego nie mówimy.")
T("Zaczynamy", "czym one w ogóle są?",
  "Zacznijmy od podstawy, bo bez niej reszta nie ma sensu. Czym te "
  "obligacje w ogóle są?")

# ------------------------------------------------------------------ cap 2
T("Obligacja", "pożyczasz państwu",
  "Kupując obligację oszczędnościową, pożyczasz pieniądze państwu na "
  "określony czas. Państwo płaci ci odsetki i oddaje kapitał.",
  cap="Czym one są")
I("Cena", "sto złotych za sztukę",
  "Jedna obligacja kosztuje sto złotych. Możesz kupić jedną albo tysiąc.")
I("Gdzie", "przez internet albo w banku",
  "Kupuje się przez internet, telefonicznie albo w oddziale. Sprzedaż "
  "prowadzą PKO Bank Polski i Pekao.")
I("Czym różni się od lokaty", "to nie bank ci płaci",
  "Od lokaty różni się jedną rzeczą, którą warto zrozumieć. Tu nie bank "
  "jest twoim dłużnikiem, tylko Skarb Państwa.")
I("Jest limit zakupu", "ale wysoki",
  "Jest też limit, choć rzadko kogo dotyczy. Na jedną emisję można kupić "
  "określoną liczbę sztuk, i dla zwykłego oszczędzającego on nie stanowi "
  "przeszkody.")
I("Można wyjść wcześniej", "za opłatą",
  "I nie jesteś zamknięty do końca. Możesz złożyć dyspozycję "
  "przedterminowego wykupu i dostać pieniądze wcześniej, z potrąceniem.")
I("Dwie rodziny", "stałe i indeksowane",
  "Ofert jest sześć, ale rodziny są dwie. Jedne mają oprocentowanie "
  "ustalone z góry. Drugie doganiają inflację.")
I("Te pierwsze", "wiesz dokładnie ile",
  "W tych pierwszych wiesz od razu, ile dostaniesz. To wygoda, ale i "
  "ryzyko, jeśli inflacja przyspieszy.")
I("Te drugie", "inflacja plus marża",
  "W tych drugich, od drugiego roku, dostajesz inflację powiększoną o "
  "marżę. Nie wiesz ile, ale wiesz, że nie zostaniesz w tyle.")
I("To jest cała różnica", "pewność albo ochrona",
  "I to jest cała różnica między nimi. Pewność kwoty albo ochrona wartości. "
  "Jedno kosztuje drugie.")
I("Sierpniowa ciekawostka", "zamiana taniej",
  "W sierpniu jest jeszcze jedna rzecz. Kto ma obligacje wykupywane w tym "
  "miesiącu, może je wymienić na nowe po dziewięćdziesiąt dziewięć złotych "
  "dziewięćdziesiąt groszy zamiast stu.")
I("Ile to daje", "dziesięć groszy na sztukę",
  "To dziesięć groszy taniej na każdej sztuce, i nie dotyczy tych "
  "trzymiesięcznych. Drobiazg, ale darmowy.")
T("Dobra", "to teraz konkretne liczby",
  "Skoro wiemy, czym one są, przejdźmy do konkretów. Ile dokładnie płaci "
  "każda z sześciu?")

# ------------------------------------------------------------------ cap 3
T("Sześć ofert", "sierpień dwa tysiące dwadzieścia sześć",
  "Oto sierpniowa oferta, w kolejności od najkrótszej do najdłuższej. "
  "Ministerstwo zostawiło oprocentowanie bez zmian wobec lipca.",
  cap="Sześć ofert sierpnia")
I("Trzy miesiące", "dwa procent",
  "Trzymiesięczne OTS. Dwa procent w skali roku, stałe. Najkrótsza i "
  "najprostsza.")
I("Rok", "cztery procent",
  "Roczne ROR. Cztery procent w pierwszym miesiącu, potem podąża za stopą "
  "referencyjną NBP. Marża zero.")
I("Dwa lata", "cztery przecinek piętnaście",
  "Dwuletnie DOR. Cztery przecinek piętnaście na start, marża zero "
  "przecinek piętnaście.")
I("Trzy lata", "cztery przecinek czterdzieści",
  "Trzyletnie TOS. Cztery przecinek czterdzieści, i to jest stałe przez "
  "cały okres.")
I("Cztery lata", "cztery przecinek siedemdziesiąt pięć",
  "Czteroletnie COI. Cztery przecinek siedemdziesiąt pięć w pierwszym roku, "
  "potem inflacja plus marża półtora procenta.")
I("Dziesięć lat", "pięć przecinek trzydzieści pięć",
  "Dziesięcioletnie EDO. Pięć przecinek trzydzieści pięć w pierwszym roku, "
  "potem inflacja plus dwa procent.")
B("Sześć ofert", ["OTS", "ROR", "DOR", "TOS", "COI", "EDO"],
  [0.37, 0.75, 0.78, 0.82, 0.89, 1.0],
  "Tak wyglądają obok siebie. Widać jedną regułę: im dłużej, tym więcej.")
I("Dlaczego tak", "płacą ci za czas",
  "To nie jest przypadek. Płacą ci za to, że oddajesz dostęp do pieniędzy "
  "na dłużej.")
I("Są jeszcze rodzinne", "dla pobierających 800 plus",
  "Są też dwie obligacje rodzinne, dostępne dla osób pobierających "
  "świadczenie osiemset plus. Sześcioletnia i dwunastoletnia.")
I("Mają wyższe marże", "dwa i dwa i pół",
  "Ich marże są wyższe. Dwa procent przy sześcioletniej i dwa i pół przy "
  "dwunastoletniej.")
I("Kiedy poznajesz nową ofertę", "co miesiąc, z góry",
  "Warto wiedzieć, kiedy patrzeć. Ministerstwo ogłasza ofertę na kolejny "
  "miesiąc jeszcze przed jego początkiem, więc porównanie robi się "
  "spokojnie, bez pośpiechu.")
I("Polacy kupują", "rekord w czerwcu",
  "I nie jest to nisza. W czerwcu Polacy kupili obligacji za osiem i sześć "
  "dziesiątych miliarda złotych, rekord od ponad roku.")
T("Mamy tabelkę", "ale ile z tego zostaje?",
  "Mamy więc tabelkę. Tylko że tabelka pokazuje kwotę brutto. Ile z tego "
  "naprawdę zostaje?")

# ------------------------------------------------------------------ cap 4
T("Dwa odejmowania", "Belka i inflacja",
  "Między oprocentowaniem a twoim realnym zyskiem stoją dwie rzeczy. "
  "Zawsze te same, zawsze w tej kolejności.",
  cap="Dwa odejmowania i próg")
I("Najpierw Belka", "dziewiętnaście procent od odsetek",
  "Najpierw podatek Belki. Dziewiętnaście procent, ale uwaga: nie od "
  "kapitału, tylko od samych odsetek.")
I("Jak to działa", "zostaje osiemdziesiąt jeden procent",
  "Praktycznie oznacza to, że z każdej złotówki odsetek zostaje ci "
  "osiemdziesiąt jeden groszy.")
I("Przykład", "cztery procent staje się",
  "Weźmy cztery procent. Po podatku zostaje trzy przecinek dwadzieścia "
  "cztery.")
I("Potem inflacja", "trzy procent w lipcu",
  "Potem wchodzi inflacja. Według GUS w lipcu ceny były o trzy procent "
  "wyższe niż rok wcześniej.")
I("Co ona robi", "zjada resztę",
  "Ona nie pobiera niczego z konta. Robi coś gorszego. Sprawia, że ta sama "
  "kwota kupuje mniej.")
I("Stąd próg", "trzy przecinek siedemdziesiąt",
  "Z tych dwóch liczb wychodzi próg. Dzielisz trzy przez zero osiemdziesiąt "
  "jeden i dostajesz trzy przecinek siedemdziesiąt.")
I("Co on znaczy", "tyle trzeba na zero",
  "To jest oprocentowanie, przy którym wychodzisz dokładnie na zero. Ani "
  "nie zyskujesz, ani nie tracisz.")
I("Policz to sam", "jedno dzielenie",
  "I to jest liczba, którą możesz przeliczyć sam w dziesięć sekund. "
  "Aktualna inflacja podzielona przez zero osiemdziesiąt jeden.")
I("Uwaga na jedną rzecz", "inflacja to przeszłość",
  "I jedno zastrzeżenie do samego progu. Inflacja GUS opisuje ostatnie "
  "dwanaście miesięcy, a twoja obligacja dotyczy przyszłych. Próg jest "
  "punktem odniesienia, nie prognozą.")
I("Ona się zmienia", "razem z inflacją",
  "Próg nie jest stały. Rośnie i spada razem z inflacją, więc warto go "
  "przeliczać, a nie zapamiętywać.")
T("Mamy próg", "to kto go nie przechodzi?",
  "Mamy próg i mamy sześć ofert. Kto go nie przechodzi?")

# ------------------------------------------------------------------ cap 5
T("Przegrywa jedna", "trzymiesięczna",
  "Wracamy do tabelki, tym razem z progiem. I odpada dokładnie jedna "
  "pozycja: trzymiesięczna OTS.",
  cap="Która przegrywa i o ile")
I("Jej liczba", "dwa procent",
  "Ona daje dwa procent. Po podatku Belki zostaje jeden przecinek "
  "sześćdziesiąt dwa.")
I("Wobec inflacji", "trzy procent",
  "A inflacja wynosi trzy. Różnica działa przeciwko tobie.")
I("Realnie", "minus prawie półtora",
  "Realnie tracisz około jednego przecinek trzydzieści osiem procent "
  "rocznie. Z pieczątką Skarbu Państwa na dokumencie.")
I("To nie jest oszustwo", "to jest krótki termin",
  "I to nie jest żadne oszustwo. Za trzy miesiące płynności nikt nie płaci "
  "premii. Płacisz za to, że możesz wyjść szybko.")
I("Reszta przechodzi", "wszystkie pozostałe pięć",
  "Pozostałe pięć przechodzi próg. Roczna z czterema procentami wychodzi "
  "na lekki plus.")
I("Im dłużej", "tym większy zapas",
  "A im dłuższy termin, tym większy zapas nad progiem. Dziesięcioletnia ma "
  "go najwięcej.")
I("Ale uwaga na indeksowane", "one zmieniają się po roku",
  "Tylko pamiętaj o jednym. W czteroletniej i dziesięcioletniej podane "
  "oprocentowanie dotyczy PIERWSZEGO roku.")
I("Potem", "inflacja plus marża",
  "Od drugiego roku liczy się inflacja powiększona o marżę. To znaczy, że "
  "one z definicji zostają nad progiem.")
I("I działa też odwrotnie", "gdy inflacja spada",
  "Działa to zresztą w obie strony. Jeśli inflacja spadnie, stała stawka "
  "nagle staje się bardzo dobra, a indeksowana się kurczy. Nikt nie wie z "
  "góry, która wygra.")
I("A stałe?", "ryzyko idzie w drugą stronę",
  "W tych o stałym oprocentowaniu ryzyko jest odwrotne. Jeśli inflacja "
  "wróci wyżej, twoja stawka zostanie w miejscu.")
T("Wiemy już wszystko", "to jak wybrać?",
  "Wiemy, ile płacą i ile zostaje. To jak w końcu wybrać?")

# ------------------------------------------------------------------ cap 6
T("Wybieraj horyzontem", "nie oprocentowaniem",
  "Najważniejsza zasada tego filmu jest jedna. Zacznij od pytania KIEDY "
  "będziesz potrzebować tych pieniędzy, a nie od tabelki.",
  cap="Jak wybrać")
I("Dlaczego tak", "wcześniejszy wykup kosztuje",
  "Bo przedterminowy wykup kosztuje. Wybierasz obligację dłuższą niż twój "
  "horyzont i płacisz karę za własną decyzję.")
I("Pieniądze na pół roku", "krótki termin, świadomie",
  "Jeśli pieniądze są potrzebne za pół roku, krótki termin jest właściwy — "
  "nawet wiedząc, że przegrywa z inflacją.")
I("Bo alternatywa", "konto osobiste to zero",
  "Bo prawdziwa alternatywa dla nich to nie dziesięciolatka. To konto "
  "osobiste, na którym leżą prawie bez oprocentowania.")
I("Pieniądze na lata", "indeksowane mają sens",
  "Jeśli horyzont to lata, a nie miesiące, sprawa wygląda inaczej. "
  "Obligacje indeksowane inflacją robią wtedy dokładnie to, po co "
  "istnieją.")
I("Drugi krok", "policz próg na dziś",
  "Drugi krok to przeliczyć próg na dziś. Sprawdź inflację GUS i podziel "
  "przez zero osiemdziesiąt jeden.")
I("Trzeci krok", "porównaj z lokatą tak samo",
  "Trzeci: porównując z lokatą, licz ją tak samo. Też po Belce. Inaczej "
  "porównujesz brutto z netto.")
I("Czwarty krok", "sprawdź zamianę",
  "Czwarty, jeśli masz obligacje wykupywane w tym miesiącu. Sprawdź "
  "zamianę, bo daje niższą cenę zakupu bez żadnej opłaty.")
I("Piąty krok, opcjonalny", "rozłóż na terminy",
  "Jest jeszcze piąty krok, dla tych, którzy nie chcą zgadywać. Rozłożyć "
  "kwotę na różne terminy, zamiast stawiać wszystko na jeden. Wtedy żadna "
  "zmiana stóp nie trafia w całość.")
I("Ile to zajmuje", "kwadrans",
  "Wszystkie cztery to kwadrans z kalkulatorem. Żaden nie wymaga rozmowy z "
  "doradcą.")
T("Plan gotowy", "co może go zepsuć?",
  "Plan jest gotowy. Co może go zepsuć?")

# ------------------------------------------------------------------ cap 7
T("Cztery błędy", "które psują rachunek",
  "Pierwszy błąd to porównywanie oprocentowania brutto z inflacją. Między "
  "nimi stoi jeszcze podatek, i to on decyduje o progu.",
  cap="Cztery błędy")
I("Drugi błąd", "brać pierwszy rok za cały okres",
  "Drugi to traktowanie oprocentowania z pierwszego roku jak stawki na "
  "cały okres. W indeksowanych to tylko start.")
I("Trzeci błąd", "kupować dłużej niż horyzont",
  "Trzeci to kupowanie na dłużej, niż naprawdę możesz czekać. Kara za "
  "wcześniejszy wykup potrafi zjeść cały zysk z krótkiego trzymania.")
I("Czwarty błąd", "mylić bezpieczne z zyskownym",
  "I czwarty, najczęstszy w tym temacie. Mylenie bezpieczeństwa kapitału z "
  "ochroną wartości. To dwie różne rzeczy.")
I("Co to znaczy", "sto złotych wraca zawsze",
  "Twoje sto złotych wróci. Pytanie brzmi, ile będzie wtedy warte.")
I("Jedno zastrzeżenie", "oferta zmienia się co miesiąc",
  "I jedno uczciwe zastrzeżenie. Ta oferta dotyczy sierpnia. Ministerstwo "
  "ogłasza nową co miesiąc, więc liczby sprawdzaj u źródła.")
L("Podsumowanie", ["Sześć ofert, od 2,00% do 5,35%",
                   "Belka zabiera 19% odsetek",
                   "Inflacja GUS: 3,0%",
                   "Próg wyjścia na zero: 3,70%",
                   "Wybieraj horyzontem"],
  "Pięć rzeczy do zapamiętania. Sześć ofert i ich rozpiętość. Że Belka "
  "zabiera dziewiętnaście procent odsetek. Aktualna inflacja. Próg wyjścia "
  "na zero. I że wybiera się horyzontem.")
I("Jeśli zrobisz jedną rzecz", "policz próg",
  "Jeśli po tym filmie zrobisz jedną rzecz, policz dzisiejszy próg. "
  "Inflacja podzielona przez zero osiemdziesiąt jeden.")
I("Dlaczego akurat to", "działa na wszystko",
  "Bo ta jedna liczba działa nie tylko na obligacje. Działa na lokatę i na "
  "konto oszczędnościowe. Na wszystko, co obiecuje ci procent.")
C("Kolejny Poziom", "na liczbach, nie na wrażeniach",
  "To wszystko. Kolejny Poziom, na liczbach i źródłach, nie na wrażeniach.")

SHORT = [
    {"layout": "titulo", "kicker": "2,00%", "sub": "przegrywa z inflacją",
     "nar": "Obligacja trzymiesięczna daje dwa procent. Inflacja wynosi "
            "trzy. To już przegrana.", "sem_cap": True},
    {"layout": "item", "kicker": "A jeszcze", "preco": "podatek Belki",
     "nar": "A przed inflacją wchodzi jeszcze Belka. Dziewiętnaście procent "
            "od odsetek.", "sem_cap": True},
    {"layout": "item", "kicker": "Zostaje", "preco": "1,62%",
     "nar": "Z dwóch procent zostaje jeden przecinek sześćdziesiąt dwa.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Próg", "preco": "3,70%",
     "nar": "Żeby wyjść na zero, potrzebujesz trzy przecinek siedemdziesiąt.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Policz sam", "preco": "inflacja ÷ 0,81",
     "nar": "Aktualna inflacja podzielona przez zero osiemdziesiąt jeden. "
            "Jedno dzielenie.", "sem_cap": True},
    {"layout": "cta", "kicker": "Sześć ofert", "sub": "na kanale",
     "nar": "Wszystkie sześć ofert sierpnia i która przechodzi próg, w "
            "pełnym filmie.", "sem_cap": True},
]

COPY = """# Obligacje skarbowe sierpień 2026: sześć ofert, jedna przegrywa z inflacją

## TYTUŁ
Obligacje Skarbowe 2026: Sześć Ofert, Jedna Przegrywa z Inflacją

## OPIS
Ministerstwo Finansów wystawiło w sierpniu 2026 sześć powszechnie dostępnych obligacji oszczędnościowych i zostawiło oprocentowanie bez zmian wobec lipca. Pięć z nich chroni realną wartość pieniędzy. Jedna nie — i akurat ta, która wygląda najbezpieczniej, czyli najkrótsza, trzymiesięczna.

Powodu nie widać w tabelce, bo tabelka pokazuje kwoty brutto. Między oprocentowaniem a twoim realnym zyskiem stoją dwa odejmowania: podatek Belki, który zabiera 19% od samych odsetek, oraz inflacja, która według GUS wyniosła w lipcu 3,0% rok do roku. Z tych dwóch liczb wychodzi jeden próg: żeby wyjść dokładnie na zero, obligacja musi dać co najmniej 3,70% w skali roku. To wynik dzielenia 3,0 przez 0,81 — działanie, które przeliczysz sam w dziesięć sekund i które warto powtarzać, bo próg zmienia się razem z inflacją.

W filmie przechodzimy przez wszystkie sześć ofert po kolei: trzymiesięczne OTS z 2,00%, roczne ROR z 4,00% i marżą zero, dwuletnie DOR z 4,15%, trzyletnie TOS ze stałymi 4,40%, czteroletnie COI z 4,75% w pierwszym roku oraz dziesięcioletnie EDO z 5,35% w pierwszym roku. Wyjaśniamy różnicę, która decyduje o wszystkim: obligacje o stałym oprocentowaniu dają pewność kwoty, a indeksowane od drugiego roku płacą inflację powiększoną o marżę — czyli z definicji zostają nad progiem. Pokazujemy też, ile realnie traci trzymiesięczna: po podatku zostaje z niej 1,62%, co przy inflacji 3,0% oznacza około -1,38% rocznie.

Na koniec cztery kroki do wyboru, wszystkie do zrobienia w kwadrans z kalkulatorem. Najważniejszy z nich jest pierwszy i wcale nie dotyczy oprocentowania: zacznij od pytania, KIEDY będziesz potrzebować tych pieniędzy. Przedterminowy wykup kosztuje, więc obligacja dłuższa niż twój horyzont to kara za własną decyzję. Wspominamy również o sierpniowej zamianie, w której nowe obligacje kupuje się po 99,90 zł zamiast 100 zł.

To nie jest rekomendacja zakupu ani porada inwestycyjna. Czytamy publiczną ofertę i liczymy.

## ROZDZIAŁY
{CAPITULOS}

## KOMENTARZ
Jedno pytanie, bo odpowiedź dzieli ludzi na pół: liczyłeś kiedyś swoje oszczędności PO podatku Belki i PO inflacji, czy patrzyłeś tylko na oprocentowanie? Bez oceniania — zbieram odpowiedzi do następnego materiału. A jeśli chcesz ten sam rachunek zrobiony dla lokat albo dla konta oszczędnościowego, napisz który; najczęściej wskazany idzie pierwszy.

## HASHTAG
#ObligacjeSkarbowe #PodatekBelki #KolejnyPoziom

## TAGI
obligacje skarbowe, obligacje 2026, podatek belki, inflacja gus, oszczedzanie, lokata czy obligacje, edo, coi, ots, ror, ministerstwo finansow, finanse osobiste, polska, realna stopa zwrotu, kolejny poziom

## USTAWIENIA STUDIO
- Język: polski (pl) | Kategoria: Edukacja (27)
- Nie jest przeznaczone dla dzieci
- Deklaracja treści syntetycznej: TAK (głos AI)
- Lokalizacja: Polska | Licencja: standardowa licencja YouTube
- Reklamy mid-roll: włączone (powyżej 8 minut)

## MUZYKA / LICENCJA
{TRILHA}

## ŹRÓDŁA
Oprocentowanie obligacji pochodzi z oferty oszczędnościowych obligacji skarbowych na sierpień 2026, opublikowanej przez Ministerstwo Finansów na gov.pl i zreferowanej z tymi samymi wartościami przez strefainwestorow.pl (dostęp 19.08.2026): OTS 3-miesięczne 2,00% stałe; ROR 1-roczne 4,00% w pierwszym miesiącu, następnie stopa referencyjna NBP, marża 0,00%; DOR 2-letnie 4,15% w pierwszym okresie, marża 0,15%; TOS 3-letnie 4,40% stałe; COI 4-letnie 4,75% w pierwszym roku, następnie inflacja + 1,50%; EDO 10-letnie 5,35% w pierwszym roku, następnie inflacja + 2,00%. Obligacje rodzinne dla beneficjentów świadczenia 800+: 6-letnie z marżą 2,00% i 12-letnie z marżą 2,50%. Zamiana obligacji wykupywanych w sierpniu: cena 99,90 zł za sztukę zamiast 100 zł, z wyłączeniem OTS. Sprzedaż obligacji w czerwcu 2026: 8,6 mld zł. Inflacja CPI: dane GUS za lipiec 2026, 3,0% rok do roku i 0,8% miesiąc do miesiąca. Podatek od dochodów kapitałowych (tzw. podatek Belki): 19% od odsetek. Próg 3,70% jest naszym wyliczeniem, nie danymi urzędowymi: to iloraz 3,0 i 0,81, czyli oprocentowanie nominalne potrzebne do wyjścia na zero po podatku przy tej inflacji — sprawdź je samodzielnie i przelicz, gdy inflacja się zmieni. Oferta obligacji zmienia się co miesiąc, więc aktualne wartości weryfikuj u źródła. Materiał edukacyjny; nie stanowi rekomendacji inwestycyjnej ani porady finansowej.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-006",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    # identidade sonora do canal: canais.trilha diz Wholesome, e as specs
    # 002, 003 e 004 usam Wholesome. Eu errei isto no 005, que ja foi ao ar.
    "trilha": "Wholesome",
    "paleta": {"ink": "#14213D", "c1": "#C1121F", "c2": "#457B9D", "bg": "#F1F0EA"},
    "thumb": {"l1": "PRÓG: 3,70%", "l2": "jedna nie przechodzi"},
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p = "fabrica/specs/kolejny-poziom-006.json"
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
