#!/usr/bin/env python3
"""Monta a spec kolejny-poziom-013.

ALAVANCA ATACADA: **A — conversao (FORMA)**, e a rodada tem um numero novo que
mexe com a premissa da propria rotina.

NUMERO DE PARTIDA, medido em 31/08/2026 sobre o pacote 012 (4,1 dias no ar):

    kolejny-poziom-012 LONGO  ... 54 views = 13,1 views/dia
    kolejny-poziom-012 SHORT  ... 39 views =  9,5 views/dia
    mediana historica do canal:   longo 1,23 vd  |  short 9,48 vd

O QUE DEU CERTO, e contraria a rotina: o LONGO bateu o short, primeira vez
neste canal. E o longo fez DEZ VEZES a mediana de longo do canal enquanto o
short ficou na mediana dele. A rotina trata longo como "o formato que quase
ninguem assiste"; aqui ele foi o formato que puxou.

RESSALVA, e ela e grande: sao 54 views e um pacote so. Isso nao derruba
aprendizado nenhum, e por isso NAO estou invalidando nada. O que faz e apontar
uma hipotese que o proximo dado resolve, e o proximo dado e este pacote.

O QUE MUDO POR CAUSA DISSO: nada na estrutura — mudar duas coisas de uma vez
tornaria o 013 ilegivel contra o 012. O 013 repete deliberadamente a forma do
012 (escolha binaria, conta com os numeros do proprio espectador, longo no piso
da faixa) em outro EIXO. Se o longo repetir, sao dois; se nao repetir, o 012
era ruido e isso tambem fica sabido.

O QUE NAO DEU: o short do 012 nao andou — 9,5 vd contra 50,1 vd do short do
011 e 20,0 vd do short do 006. O short deste pacote volta ao gancho seco de
numero na primeira frase, que e o que aqueles dois tinham.

E o que eu NAO consigo medir, dito na cara: segundos vistos e inscritos por
video. Os tokens da frota nao tem `yt-analytics.readonly` e a Composio nao
expoe Analytics (aprendizados 528 e 522). As linhas do 012 em `metricas` tem
retencao ZERO por AUSENCIA DE FONTE, nao por serem zero.

--------------------------------------------------------------- DIMENSIONAMENTO

`v_maquina_licoes` da `liberado` (12-15 min) — o unico canal da frota nessa
faixa. Alavanca B manda ir ao PISO: **720 segundos**, e nao aos quinze minutos.
O 012, que foi o melhor longo do canal, tem 777 s; o 011 tem 742 s; e o pior
longo com retencao medida (008, 4,75%) tem 781 s.

Nove capitulos. A RESPOSTA — os dois multiplicadores e a subtracao — fecha no
capitulo 3, dentro dos primeiros duzentos segundos.

--------------------------------------------------------------------- A PAUTA

Pauta 1063 do `pautas_banco`. Eixo **okres-kredytu**, nunca usado. O canal ja
cobriu nadplata/inwestycje, IKE/IKZE, obligacje, ZUS, ryczalt, OC, placa
minimalna, podatek Belki, prog podatkowy, zdolnosc kredytowa e prad.

ESTRUTURA copiada dos outliers poloneses de maior tracao, que sao todos escolha
binaria com calculadora: "Inwestowac czy nadplacac kredyt hipoteczny -
SPRAWDZAM [KALKULATOR]" (2.164 views/dia) e "Bank chce zlowic Cie na 30 lat"
(785 views/dia). Assunto NAO copiado.

AS TRES CONDICOES DO APRENDIZADO 504:
1. o dinheiro e DELE — o credito dele;
2. e ESCOLHA, com consequencia — o prazo muda a parcela e o total, e ele decide
   na assinatura ou na renegociacao;
3. o SHORT entrega a conta — dois prazos, duas parcelas, a diferenca em zlotys.

--------------------------------------------------- O TITULO MUDOU, E POR QUE

A pauta foi bancada como "Dwadziescia piec czy trzydziesci piec lat". Esse
titulo NAO pode ser usado: os numeros 25 e 35 foram DESCARTADOS em 27/08 por
falta de segunda fonte institucional, e o descarte veio com armadilha — o "35"
aparece no gov.pl significando LIMITE DE IDADE do programa `#naStart`, nao
prazo maximo de credito. Titulo que carrega numero descartado e numero
descartado que entrou no video pela porta dos fundos.

O titulo novo nao tem numero nenhum, e os dois prazos da conta saem do CONTRATO
DO ESPECTADOR.

FONTES: este video NAO faz nenhuma afirmacao institucional e nao cita nenhum
numero meu. Nao cita lei, nao cita taxa, nao cita RRSO, nao cita regra de
prazo maximo, nao cita banco. Todos os numeros da conta sao do proprio
espectador — as duas parcelas saem da simulacao que o banco lhe deu ou do
harmonograma que ele ja tem em casa. Nao ha numero meu para certificar, e por
isso nao ha numero meu que possa envelhecer.

O QUE O VIDEO NAO FAZ: nao diz qual prazo e melhor, nao recomenda banco, nao
promete economia, nao calcula a parcela (isso e o banco que faz e entrega
escrito), e nao e aconselhamento financeiro.
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


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================

# -------------------------------------------------------------------- cap 1
T("W twojej umowie", "jest jedna liczba, którą wybrałeś",
  "W umowie kredytu jest liczba, którą wybrałeś sam, i prawdopodobnie "
  "poświęciłeś jej najmniej uwagi ze wszystkich. To okres spłaty.",
  cap="Liczba, którą wybrałeś sam")
I("Nie narzuca jej nikt", "to twoja decyzja",
  "Tej liczby nie narzuca ci ustawa ani rynek. To decyzja, którą podejmujesz "
  "przy podpisie, i którą czasem można zmienić później.")
I("Na czym się skupiłeś", "na racie",
  "Przy podpisie prawie każdy patrzy na jedno: na wysokość raty. Rata musi się "
  "zmieścić w budżecie i to zamyka temat.")
I("Czego nie widać", "sumy wszystkich rat",
  "Czego się nie widzi, to sumy wszystkich rat. Ona nie jest wypisana obok "
  "raty i nikt jej przy tobie nie mnoży.")
I("A różnica jest tam", "nie w racie",
  "A cała różnica między krótszym a dłuższym kredytem siedzi właśnie w tej "
  "sumie, nie w racie.")
I("Sąsiad obok", "ten sam kredyt, inny okres",
  "Sąsiad z takim samym mieszkaniem i takim samym kredytem, ale z innym "
  "okresem, zapłaci w sumie zupełnie inną kwotę.")
I("Pytanie tego filmu", "ile dokładnie",
  "Pytanie brzmi więc: ile dokładnie, w złotych, kosztuje cię twój okres. Nie "
  "w procentach i nie ogólnie.")
I("Czego się zaraz nauczysz", "dwa mnożenia",
  "Za chwilę policzysz to sam, dwoma mnożeniami i jednym odejmowaniem, na "
  "papierach, które już masz w domu.")

# -------------------------------------------------------------------- cap 2
T("Co robi okres", "dwie rzeczy naraz",
  "Najpierw co okres w ogóle robi, bo robi dwie rzeczy jednocześnie i one idą "
  "w przeciwne strony.",
  cap="Co okres robi z ratą")
I("Pierwsza rzecz", "dłuższy okres, niższa rata",
  "Pierwsza: im dłuższy okres, tym niższa rata. Ta sama kwota rozkłada się na "
  "więcej miesięcy.")
I("Druga rzecz", "dłuższy okres, więcej rat",
  "Druga: im dłuższy okres, tym więcej rat zapłacisz. I każda z nich zawiera "
  "odsetki.")
I("Te dwie idą w kontrze", "i tu robi się ciekawie",
  "Te dwa efekty działają przeciwko sobie, i to właśnie dlatego nie da się "
  "odpowiedzieć na oko.")
I("Dlaczego nie na oko", "bo rata nie spada proporcjonalnie",
  "Nie da się na oko, bo rata nie spada proporcjonalnie do wydłużenia okresu. "
  "Spada zawsze wolniej.")
I("Co to znaczy", "wydłużenie kosztuje",
  "To znaczy, że wydłużenie okresu obniża ratę o mniej, niż podnosi liczbę "
  "rat. Suma rośnie.")
I("Ale nie zawsze tak samo", "zależy od twojego kredytu",
  "O ile rośnie, zależy od twojej kwoty, twojego oprocentowania i twoich "
  "dwóch okresów. Dlatego to musi być twój rachunek, nie mój.")
I("Krótszy nie jest darmowy", "on podnosi ratę",
  "I uwaga w drugą stronę: krótszy okres nie jest darmowy. On podnosi ratę, "
  "czasem tak, że przestaje się mieścić.")
I("Więc to nie jest rada", "to jest miara",
  "Dlatego to nie jest rada, żeby brać krócej. To jest sposób, żeby zobaczyć "
  "cenę obu opcji, zanim wybierzesz.")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA.
T("Rachunek", "dwa mnożenia i jedno odejmowanie",
  "Teraz rachunek. Dwa mnożenia i jedno odejmowanie, i potrzebujesz do niego "
  "czterech liczb.",
  cap="Rachunek: dwa mnożenia")
I("Pierwsza para", "rata i liczba miesięcy",
  "Pierwsza para: rata przy pierwszym okresie i liczba miesięcy tego okresu.")
I("Mnożysz", "rata razy miesiące",
  "Pomnóż jedno przez drugie. Wynik to suma wszystkiego, co oddasz przy tym "
  "okresie.")
I("Druga para", "rata i miesiące drugiego okresu",
  "Druga para: rata przy drugim okresie i liczba miesięcy tego drugiego "
  "okresu.")
I("Mnożysz znowu", "ta sama operacja",
  "Ta sama operacja. Rata razy miesiące. Druga suma.")
I("Odejmujesz", "i to jest twoja liczba",
  "Odejmij mniejszą sumę od większej. To, co zostaje, jest w złotych i jest "
  "ceną różnicy między tymi dwoma okresami — nie szacunkiem, nie procentem, "
  "tylko kwotą, którą albo zapłacisz, albo nie.")
I("Dlaczego to działa", "kwota kredytu się nie zmienia",
  "Działa, bo kwota kredytu jest w obu przypadkach ta sama. Zmieniasz tylko "
  "okres, więc różnica pokazuje wyłącznie jego koszt.")
I("Ile miesięcy", "lata razy dwanaście",
  "Liczbę miesięcy dostajesz mnożąc lata przez dwanaście. To jedyna liczba, "
  "którą wyliczasz sam.")
I("I to cały rachunek", "reszta to gdzie szukać",
  "To jest cały rachunek. Wszystko, co dalej, to gdzie znaleźć te cztery "
  "liczby i czego ten rachunek nie obejmuje.")

# ===================== DEPOIS DOS 200 SEGUNDOS ==============================

# -------------------------------------------------------------------- cap 4
T("Skąd te cztery liczby", "z papierów, które masz",
  "Cztery liczby, i żadnej nie musisz szacować. Wszystkie są w dokumentach.",
  cap="Skąd wziąć cztery liczby")
I("Rata, którą płacisz", "z harmonogramu",
  "Ratę, którą płacisz dzisiaj, masz w harmonogramie spłat. To ten sam "
  "dokument, w którym widzisz kolejne terminy.")
I("Okres, który masz", "z umowy",
  "Okres, na który wziąłeś kredyt, jest w umowie. Zwykle podany w latach albo "
  "w liczbie rat.")
I("Rata przy innym okresie", "to bank ma policzyć",
  "Raty przy innym okresie nie licz sam. Poproś bank o symulację dla tego "
  "drugiego okresu — to on ma kalkulator i to on ją policzy.")
I("Poproś o pisemną", "nie o rozmowę",
  "I poproś o wersję pisemną, nie o liczbę podaną przez telefon. Do rachunku "
  "potrzebujesz czegoś, co możesz przeczytać dwa razy.")
I("Jeśli jeszcze bierzesz kredyt", "poproś o dwie symulacje",
  "Jeśli jeszcze nie podpisałeś, to jest najprostszy moment: poproś o dwie "
  "symulacje, na dwa różne okresy, i porównaj je tym rachunkiem.")
I("Ten sam dzień", "obie liczby",
  "Weź obie raty z tego samego dnia. Rata z dzisiaj kontra rata sprzed roku to "
  "nie jest porównanie, tylko błąd.")
I("Te same warunki", "poza okresem",
  "I pilnuj, żeby wszystko poza okresem było takie samo: ta sama kwota, ta "
  "sama marża, ten sam rodzaj oprocentowania.")
I("Bo inaczej", "mierzysz coś innego",
  "Jeśli zmieni się coś jeszcze, twoja różnica przestaje być ceną okresu, a "
  "staje się mieszanką kilku rzeczy naraz.")
I("Jeśli bank zwleka", "masz prawo pytać",
  "Jeśli bank zwleka z symulacją, pytaj dalej. To jest liczba, na podstawie "
  "której masz podjąć decyzję na kilkanaście albo kilkadziesiąt lat.")
I("A jeśli dostaniesz tabelę", "szukaj dwóch kolumn",
  "Czasem dostaniesz całą tabelę wariantów. Wtedy szukaj tylko dwóch kolumn: "
  "raty i liczby rat. Reszta ci w tym rachunku nie jest potrzebna.")
I("To jedyna zasada", "jedna zmienna",
  "Cała rzetelność tego rachunku sprowadza się do jednej zasady: zmieniasz "
  "jedną rzecz na raz.")

# -------------------------------------------------------------------- cap 5
T("Dlaczego rata spada wolniej", "warto to zobaczyć",
  "Warto zrozumieć, dlaczego rata spada wolniej, niż rośnie okres. To wyjaśnia "
  "cały wynik.",
  cap="Dlaczego rata spada wolniej")
I("Rata ma dwie części", "kapitał i odsetki",
  "Każda rata składa się z dwóch części: kawałka pożyczonej kwoty i odsetek od "
  "tego, co jeszcze zostało do oddania.")
I("Na początku", "przeważają odsetki",
  "Na początku kredytu przeważają odsetki, bo zostało do oddania najwięcej.")
I("Pod koniec", "przeważa kapitał",
  "Pod koniec jest odwrotnie: prawie cała rata to już spłata kwoty, bo odsetek "
  "prawie nie ma od czego liczyć.")
I("Co robi dłuższy okres", "przedłuża początek",
  "Dłuższy okres wydłuża tę pierwszą fazę. Dłużej jesteś w części, w której "
  "płacisz głównie odsetki.")
I("Dlatego", "rata spada mniej niż byś oczekiwał",
  "Dlatego wydłużenie o kilka lat nie obniża raty tak, jak podpowiada "
  "intuicja. Odsetki nie znikają, tylko się rozciągają.")
I("A liczba rat", "rośnie wprost",
  "A liczba rat rośnie wprost proporcjonalnie. Więcej miesięcy to po prostu "
  "więcej rat, jeden do jednego.")
I("Stąd wynik", "suma rośnie",
  "Stąd suma zawsze rośnie przy wydłużeniu. Pytanie brzmi wyłącznie o ile, i "
  "właśnie to liczysz.")
I("Sprawdź to na sobie", "w swoim harmonogramie",
  "Możesz to zobaczyć u siebie w minutę: otwórz harmonogram i porównaj, jaka "
  "część pierwszej raty to odsetki, a jaka część ostatniej.")
I("Ta różnica", "to cały mechanizm",
  "Ta różnica między pierwszą a ostatnią ratą jest całym mechanizmem, o którym "
  "mówimy. Nie musisz mi wierzyć na słowo, masz to na papierze.")
I("I dlatego liczysz sam", "nikt nie policzy tego za ciebie",
  "I dlatego to musi być twoja liczba. Przy twojej kwocie i twoim "
  "oprocentowaniu wyjdzie inaczej niż u kogokolwiek innego.")

# -------------------------------------------------------------------- cap 6
T("Czego ten rachunek nie łapie", "to jest ważne",
  "Teraz część, bez której ten rachunek robi się niebezpieczny: czego on nie "
  "obejmuje.",
  cap="Czego rachunek nie łapie")
I("Oprocentowanie zmienne", "rata się zmieni",
  "Po pierwsze: przy oprocentowaniu zmiennym rata nie zostanie taka sama przez "
  "cały okres. Twoje mnożenie zakłada, że zostanie.")
I("Co z tym zrobić", "to jest zdjęcie, nie prognoza",
  "Traktuj więc wynik jako zdjęcie dzisiejszych warunków, a nie prognozę. To "
  "porównanie dwóch okresów przy dzisiejszej stawce.")
I("I to wystarcza", "bo obie strony są tak samo obarczone",
  "I do porównania to wystarcza, bo obie strony rachunku są obciążone tym "
  "samym założeniem.")
I("Ubezpieczenia", "bywają doliczane obok",
  "Po drugie: ubezpieczenia i inne opłaty bywają doliczane obok raty. Sprawdź, "
  "czy twoja rata je zawiera, czy nie.")
I("Sprawdź to raz", "w harmonogramie",
  "Sprawdź to raz w harmonogramie i użyj tej samej wersji po obu stronach — "
  "albo obie z ubezpieczeniem, albo obie bez.")
I("Prowizja i koszty na starcie", "są jednorazowe",
  "Po trzecie: prowizja i koszty początkowe są jednorazowe. Nie zależą od "
  "okresu, więc w tej różnicy się skracają.")
I("Nadpłata zmienia wszystko", "i nie jest w rachunku",
  "Po czwarte, i to największe: jeśli zamierzasz nadpłacać, faktyczny okres "
  "będzie inny niż ten z umowy. Rachunek tego nie widzi.")
I("Wcześniejsza spłata", "sprawdź warunki",
  "Sprawdź też, na jakich warunkach możesz spłacić wcześniej. To bywa zapisane "
  "osobno i potrafi zmienić opłacalność całego wyboru.")
I("Zmiana okresu w trakcie", "to nowa umowa albo aneks",
  "Po piąte: zmiana okresu w trakcie spłaty zwykle wymaga aneksu albo nowej "
  "umowy, a to bywa osobnym kosztem. Zapytaj o niego, zanim policzysz zysk.")
I("Wniosek", "to rząd wielkości",
  "Ten rachunek daje ci rząd wielkości, a nie ostateczną kwotę. To początek "
  "decyzji, nie jej dowód.")
I("Ale rząd wielkości wystarcza", "żeby przestać zgadywać",
  "I rząd wielkości w zupełności wystarcza, żeby przestać wybierać okres na "
  "wyczucie.")

# -------------------------------------------------------------------- cap 7
T("Trzecia opcja", "której nikt nie liczy",
  "Jest jeszcze trzecia opcja, o której prawie nikt nie myśli przy podpisie.",
  cap="Trzecia opcja: nadpłata")
I("Dłuższy okres i nadpłata", "razem",
  "Możesz wziąć dłuższy okres, a potem nadpłacać. Wtedy niższa rata jest "
  "twoim marginesem bezpieczeństwa, a nie kosztem.")
I("Co to daje", "elastyczność",
  "Dostajesz elastyczność: w gorszym miesiącu płacisz niską ratę, w lepszym "
  "nadpłacasz i skracasz kredyt.")
I("Czego to wymaga", "konsekwencji",
  "Wymaga to jednak konsekwencji przez lata. Jeśli nadpłata się nie wydarzy, "
  "zostaje sam dłuższy okres i jego koszt.")
I("Jak to policzyć", "tym samym rachunkiem",
  "Policzysz to tym samym rachunkiem: potraktuj okres, do którego realnie "
  "skrócisz kredyt, jako drugi okres w mnożeniu.")
I("I porównaj trzy", "nie dwie",
  "Wtedy masz trzy liczby zamiast dwóch: krótki okres, długi okres, i długi "
  "okres z nadpłatą.")
I("Uwaga na warunki", "nadpłata bywa ograniczona",
  "Zanim na tym oprzesz decyzję, sprawdź w umowie, czy nadpłata jest możliwa "
  "bez ograniczeń i bez dodatkowych kosztów.")
I("I co skraca", "okres czy ratę",
  "Sprawdź też, co dokładnie skraca twoja nadpłata: okres kredytu czy "
  "wysokość raty. To dwie różne rzeczy i wybiera się je świadomie.")
I("Bo tylko jedno", "zmniejsza sumę mocno",
  "Skracanie okresu zabiera więcej odsetek niż obniżanie raty. Jeśli celujesz "
  "w sumę, to jest kierunek.")
I("I policz obie wersje", "zanim zdecydujesz",
  "Zanim wybierzesz, policz obie wersje nadpłaty tym samym rachunkiem. To ta "
  "sama operacja, tylko z innym drugim okresem.")
I("Ale to twoja decyzja", "nie moja",
  "Który wariant wybierzesz, zależy od tego, czy bardziej potrzebujesz "
  "bezpieczeństwa w miesiącu, czy niższej sumy na końcu.")

# -------------------------------------------------------------------- cap 8
T("Od miesiąca do całego kredytu", "tu widać skalę",
  "I teraz liczba, która najczęściej zmienia zdanie.",
  cap="Od raty do całości")
I("Różnica w racie", "wygląda mało",
  "Różnica w samej racie między dwoma okresami wygląda niepozornie. To zwykle "
  "kwota, o której się nie myśli.")
I("Różnica w sumie", "wygląda inaczej",
  "Ta sama decyzja w sumie rat wygląda zupełnie inaczej, i to jest dokładnie "
  "ta liczba, którą przed chwilą policzyłeś.")
I("Porównaj ją z czymś", "co znasz",
  "Żeby ją poczuć, porównaj ją z czymś, co znasz. Z rocznym dochodem, z ceną "
  "samochodu, z wkładem własnym.")
I("Dlaczego to działa", "bo skala staje się realna",
  "Działa to dlatego, że liczba w złotych bez odniesienia jest abstrakcją, a z "
  "odniesieniem staje się decyzją.")
I("I to się nie powtarza", "wybierasz raz",
  "Pamiętaj też, że okres wybierasz raz, na wiele lat. To nie jest decyzja, "
  "którą poprawiasz co miesiąc.")
I("Dlatego licz przed", "nie po",
  "Dlatego rachunek robi się przed podpisem, a nie po pierwszym roku spłaty.")
I("A jeśli już spłacasz", "wciąż warto",
  "A jeśli już spłacasz, i tak warto go zrobić: pokaże ci, ile realnie daje "
  "skrócenie okresu, gdybyś je rozważał.")
I("I zrób to raz w roku", "warunki się zmieniają",
  "Warto powtórzyć ten rachunek raz w roku. Twoja rata, twój pozostały okres i "
  "warunki na rynku nie stoją w miejscu.")
I("To ta sama liczba", "z drugiej strony",
  "To dokładnie ta sama liczba, tylko oglądana z drugiej strony umowy.")

# -------------------------------------------------------------------- cap 9
T("Co robisz dzisiaj", "trzy kroki",
  "Kończymy tym, co możesz zrobić dzisiaj, w trzech krokach.",
  cap="Co robisz dzisiaj")
L("Trzy kroki",
  ["Znajdź swoją ratę", "Poproś o drugą symulację", "Pomnóż i odejmij"],
  "Pierwszy: znajdź swoją ratę i swój okres. Drugi: poproś bank o symulację "
  "dla innego okresu. Trzeci: pomnóż obie i odejmij.")
I("Pierwszy krok", "harmonogram i umowa",
  "Pierwszy krok to dwa dokumenty, które już masz: harmonogram spłat i umowa. "
  "Nic nie musisz nigdzie zakładać.")
I("Drugi krok", "jedno pytanie do banku",
  "Drugi krok to jedno pytanie do banku, zadane na piśmie. O symulację dla "
  "innego okresu, przy tej samej kwocie.")
I("Trzeci krok", "kartka i kalkulator",
  "Trzeci krok to kartka i kalkulator w telefonie. Dwa mnożenia, jedno "
  "odejmowanie, dwie minuty. Nie potrzebujesz do tego żadnej aplikacji ani "
  "żadnego porównywarki.")
I("Zapisz wynik z datą", "będziesz go potrzebował",
  "Zapisz wynik razem z datą. Za pół roku będziesz chciał wiedzieć, jakie "
  "warunki obowiązywały, kiedy decydowałeś, a pamięć tego nie odtworzy.")
I("Czego to nie jest", "to nie jest porada",
  "I na koniec jasno: nic z tego nie jest poradą finansową ani rekomendacją "
  "banku. To metoda liczenia.")
C("Kolejny Poziom", "policz to dzisiaj",
  "Jeśli dotarłeś tutaj, zrób ten rachunek dzisiaj, na swojej własnej umowie. "
  "I napisz w komentarzu samą różnicę, którą ci wyszła.")


# =============================== O SHORT ====================================
# Gancho seco na primeira frase — a forma dos dois shorts que mais andaram
# neste canal (50,1 e 20,0 views/dia). E ele entrega a conta inteira.
SHORT = [
    {"layout": "titulo", "kicker": "Twój okres kredytu",
     "sub": "ma cenę w złotych",
     "nar": "Okres twojego kredytu ma cenę, i nikt ci jej nie wypisuje.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Cztery liczby", "preco": "dwie raty, dwa okresy",
     "nar": "Potrzebujesz czterech liczb: twojej raty i twojego okresu, oraz "
            "raty i okresu przy innym terminie spłaty.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Dwa mnożenia", "preco": "rata razy miesiące",
     "nar": "Pomnóż każdą ratę przez liczbę miesięcy. Lata razy dwanaście daje "
            "miesiące.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Odejmij", "preco": "to jest ta cena",
     "nar": "Odejmij jedną sumę od drugiej. To, co zostaje, jest w złotych i "
            "jest ceną twojego okresu.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Kolejny Poziom", "sub": "skąd wziąć te liczby",
     "nar": "Gdzie znaleźć każdą z czterech liczb i czego ten rachunek nie "
            "obejmuje — w pełnym filmie pod spodem.",
     "sem_cap": True},
]

THUMB = {"l1": "Okres", "l2": "ma cenę"}

COPY = """# Ile kosztuje okres twojego kredytu

## TITULO
Krótszy czy Dłuższy Kredyt? Dwa Mnożenia z Twojej Umowy Pokazują Różnicę w Złotych

## DESCRICAO
W umowie kredytu jest liczba, którą wybrałeś sam i której poświęciłeś najmniej uwagi: okres spłaty. Nie narzuca jej ustawa ani rynek — to twoja decyzja, podejmowana przy podpisie i czasem możliwa do zmiany później. Przy podpisie prawie każdy patrzy tylko na wysokość raty, bo rata musi zmieścić się w budżecie. Czego się nie widzi, to sumy wszystkich rat — a cała różnica między krótszym a dłuższym kredytem siedzi właśnie tam.

DLACZEGO NIE DA SIĘ NA OKO

Okres robi dwie rzeczy naraz i idą one w przeciwne strony: dłuższy okres obniża ratę, ale zwiększa liczbę rat. Rata nie spada proporcjonalnie do wydłużenia okresu — spada wolniej, bo dłuższy okres przedłuża fazę, w której płacisz głównie odsetki. Liczba rat rośnie natomiast wprost, jeden do jednego. Dlatego suma zawsze rośnie przy wydłużeniu; pytanie brzmi wyłącznie o ile, i to zależy od twojej kwoty, twojego oprocentowania i twoich dwóch okresów.

RACHUNEK (dwa mnożenia i jedno odejmowanie)

Weź ratę przy pierwszym okresie i liczbę miesięcy tego okresu — pomnóż. Weź ratę przy drugim okresie i liczbę miesięcy drugiego okresu — pomnóż. Odejmij mniejszą sumę od większej. Wynik jest w złotych i jest ceną różnicy między tymi dwoma okresami. Działa, bo kwota kredytu jest w obu przypadkach ta sama — zmieniasz tylko okres. Liczbę miesięcy dostajesz mnożąc lata przez dwanaście.

SKĄD CZTERY LICZBY: ratę, którą płacisz, masz w harmonogramie spłat; okres — w umowie. Raty przy innym okresie nie licz sam: poproś bank o symulację, najlepiej pisemną. Obie raty z tego samego dnia, wszystko poza okresem identyczne — ta sama kwota, ta sama marża, ten sam rodzaj oprocentowania. Jedna zmienna na raz.

CZEGO RACHUNEK NIE ŁAPIE: przy oprocentowaniu zmiennym rata nie zostanie taka sama (traktuj wynik jak zdjęcie dzisiejszych warunków — do porównania wystarcza, bo obie strony są obciążone tym samym założeniem); ubezpieczenia doliczane obok raty (użyj tej samej wersji po obu stronach); prowizja i koszty początkowe (jednorazowe, więc w różnicy się skracają); i nadpłata, która zmienia faktyczny okres — sprawdź w umowie, czy jest możliwa bez ograniczeń i czy skraca okres, czy ratę.

Nic z tego nie jest poradą finansową ani rekomendacją banku. To metoda liczenia.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Zrób ten rachunek na własnej umowie i napisz tu jedną liczbę: samą różnicę w złotych. Bez banku, bez kwoty kredytu, bez oprocentowania — tylko różnica. Ciekawi mnie, jak bardzo te różnice rozjadą się między sobą przy podobnych kredytach.

## HASHTAGS
#Kredyt #FinanseOsobiste #KolejnyPoziom

## TAGS
okres kredytu, kredyt hipoteczny, rata kredytu, harmonogram splat, suma rat, nadplata kredytu, skrocenie okresu, symulacja kredytu, oprocentowanie zmienne, calkowity koszt kredytu, wczesniejsza splata, wybor okresu, finanse osobiste, budzet domowy, kalkulator kredytowy

## CONFIGURACOES DO STUDIO
- Idioma: Polones (pl) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Polonia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita lei, taxa, RRSO, prazo maximo de credito nem nome de banco. Todos os numeros da conta sao do proprio espectador: as duas parcelas saem da simulacao que o banco lhe entrega ou do harmonograma que ele ja tem, e a contagem de meses sai de anos vezes doze. Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer. O QUE FOI DESCARTADO, e o descarte e a razao de este video existir nesta forma: a pauta foi bancada em 27/08/2026 com o par de prazos VINTE E CINCO e TRINTA E CINCO anos, vindo da Rekomendacja S da KNF. Esse par NAO entrou, porque as duas pecas que o sustentam (a recomendacao de 2011 e a novelizacao de junho de 2023) sao da MESMA instituicao, e a regra desta maquina pede duas instituicoes que batam. A busca restrita a nbp.pl, gov.pl, uokik.gov.pl e bfg.pl nao devolveu confirmacao de outra instituicao — e devolveu uma ARMADILHA que fica registrada aqui: o numero TRINTA E CINCO aparece no gov.pl, mas significa LIMITE DE IDADE do programa `kredyt mieszkaniowy #naStart`, nao prazo maximo de credito. Dois numeros iguais, significados diferentes. O titulo original da pauta carregava esse par e foi trocado por um sem numero nenhum: numero descartado no titulo e numero descartado entrando no video pela porta dos fundos. A conta funciona sem ele, porque os dois prazos comparados sao os do contrato do espectador.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/kolejny-poziom-013.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-013",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#E4572E", "c2": "#F5B841", "bg": "#F4F1EA"},
    "thumb": THUMB,
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
    grava(SPEC, "fabrica/specs/kolejny-poziom-013.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get("cap")]))
