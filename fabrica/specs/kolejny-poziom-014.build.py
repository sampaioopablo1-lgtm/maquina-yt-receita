#!/usr/bin/env python3
"""Monta a spec kolejny-poziom-014.

ALAVANCA ATACADA: **A — conversao short -> inscrito**, com a pauta escolhida
pelo aprendizado 543 e o short carregando o experimento 26.

NUMERO DE PARTIDA, medido em 01/09/2026 video a video (36 videos):

    kolejny-poziom .... 5 inscritos, 4.504 views, 36 videos
                        short: mediana 7,71 views/dia, topo 64,92
                        longo: mediana 1,14 views/dia
                        veredito: `liberado` (12-15 min)
                        ONZE DUPLICATAS no ar do mesmo titulo

O QUE DEU CERTO: o melhor longo do canal e "Prad Stanieje w 2026" com onze
virgula nove views/dia — e ele veio de um short de oito virgula tres, abaixo
da mediana do canal. Depois dele vem "Ryczalt" com seis virgula seis, tambem
de um short mediano. Os dois pedem que o espectador calcule com o papel dele:
a fatura de luz num, o limite do regime no outro.

O QUE NAO DEU: os tres MAIORES shorts do canal. "Nadplacac kredyt" fez
catorze virgula dois views/dia e o longo dele parou em zero virgula noventa e
nove; "Obligacje Skarbowe" fez onze virgula oito e o longo parou em dois
virgula quatro; "Prog Podatkowy" fez nove virgula cinco e parou em dois virgula
quatro tambem. Alcance de short nao puxa longo — replicado hoje em quatro
canais e quatro linguas (aprendizado 543).

E O QUE PRECISA SER DITO SOBRE O NUMERO DESTE CANAL: das quatro mil e
quinhentas views dele, **tres mil duzentas e quarenta e seis vem de onze videos
DUPLICADOS** do mesmo titulo sobre a emerytura — setenta e dois por cento. O
alcance real do canal e cerca de mil duzentas e sessenta views, nao quatro mil
e quinhentas. Isso nao muda a pauta desta rodada, mas muda como o numero deste
canal deve ser lido daqui pra frente (aprendizado 545). A remocao das copias
esta com o Pablo: apagar video publicado nao e reversivel e nao esta no meu
mandato.

O QUE MUDO POR CAUSA DISSO:
1. **A PAUTA** copia a forma do que venceu — conta na fatura dele, com prazo —
   e nao a expectativa de alcance do short.
2. **O SHORT** entrega a conta fechada E pede a inscricao (experimento 26,
   sexto braco).

--------------------------------------------------------------- DIMENSIONAMENTO

Veredito `liberado` => faixa de doze a quinze minutos, e a alavanca B manda o
PISO: **doze minutos**. NOVE capitulos, porque o video de melhor retencao da
frota tem nove e o pior tem sete.

REGISTRO DE UMA TENSAO, para quem ler depois: os dezessete longos deste canal
ja estao todos entre onze e catorze minutos, e a mediana deles e um virgula
catorze views/dia — enquanto os longos de oito a nove minutos do
epomeno-epipedo fazem sete a vinte e um. Eu sigo o veredito porque a rotina
manda seguir o portao e corrigir o texto, nunca o portao; mas se o proximo
`liberado` deste canal repetir um virgula um, o portao merece ser reexaminado
com o numero na mao.

Cada capitulo com ~80s. A resposta fecha na PRIMEIRA METADE do capitulo 3 e o
tempo real vai ser conferido no `legendas.srt` do artefato.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO: **quanto voce paga por dados de celular que nao usa**. Os eixos ja
publicados aqui sao credito, luz, limite de imposto, ryczalt, seguro de carro,
capacidade de credito, titulos publicos, salario minimo, IKE/IKZE, taxas e
imposto Belki, amortizar credito e emerytura. Conta de telefone nunca foi ao ar.

AS TRES CONDICOES DO APRENDIZADO 504:
1. os numeros sao DELE — a fatura e a tela de consumo do proprio aparelho;
2. e ESCOLHA COM PRAZO — o contrato tem data de renovacao;
3. o SHORT entrega a conta — a divisao fechada, e depois pede a inscricao.

FONTES: este video NAO faz nenhuma afirmacao institucional e NAO cita nenhum
numero meu. Nao cita preco de plano, nao cita operadora, nao cita media de
consumo de ninguem e nao compara ofertas. Os dois numeros saem da fatura e da
tela de consumo do proprio espectador. Nao ha numero meu para certificar em
duas fontes, e por isso nao ha numero meu que possa envelhecer.

O QUE O VIDEO NAO FAZ: nao recomenda operadora nem plano, nao diz que plano
grande e ruim, nao promete economia e nao e aconselhamento financeiro.
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
T("Płacisz co miesiąc", "za coś, czego nie zużywasz",
  "Co miesiąc płacisz rachunek za telefon. I bardzo prawdopodobne, że część "
  "tej kwoty idzie za gigabajty, których nigdy nie tkniesz.",
  cap="Rachunek, którego nie sprawdzasz")
I("To nie jest atak na operatorów", "to jest twój rachunek",
  "To nie jest wideo o tym, że operatorzy oszukują. To wideo o tym, ile "
  "kosztuje twój własny pakiet — a to zupełnie inne pytanie.")
I("I ma termin", "koniec umowy",
  "Ma też termin, który znasz: koniec umowy albo miesiąc, w którym możesz ją "
  "zmienić. Wtedy ta liczba się przydaje.")
I("Dwie liczby", "obie już masz",
  "Potrzebujesz dwóch liczb i obie już masz. Jedna jest na rachunku, druga w "
  "telefonie, w ustawieniach transmisji danych.")
I("Nikt tego nie liczy", "operator też nie",
  "Nikt tego za ciebie nie policzy. Operator pokazuje wielkość pakietu, bo to "
  "sprzedaje. Nie pokazuje ceny gigabajta, którego nie użyłeś.")
I("Nic nie trzeba instalować", "wszystko już jest",
  "Nie musisz niczego instalować ani zaczynać notować. Telefon liczy to od "
  "miesięcy, a rachunek masz w skrzynce.")
I("Co dalej", "jedno dzielenie",
  "Za chwilę policzysz to sam. Jedno dzielenie i jedno odejmowanie, na "
  "liczbach, które już istnieją.")

# -------------------------------------------------------------------- cap 2
T("Dwie strony", "pakiet i zużycie",
  "Rachunek ma dwie strony i najczęstszy błąd to patrzeć tylko na pierwszą.",
  cap="Pakiet i rzeczywiste zużycie")
I("Strona pierwsza", "co płacisz miesięcznie",
  "Pierwsza strona to kwota, którą płacisz miesięcznie. Ta z rachunku, nie ta "
  "z reklamy sprzed dwóch lat.")
I("Sprawdź, co jest w środku", "nie tylko dane",
  "Sprawdź, co obejmuje: rozmowy, SMS-y i dane. Jeśli rozmowy i tak są bez "
  "limitu, cena dotyczy głównie danych.")
I("Strona druga", "ile naprawdę zużyłeś",
  "Druga strona to zużycie. W telefonie jest ekran, który pokazuje transmisję "
  "danych za ostatni okres rozliczeniowy.")
I("Weź trzy miesiące", "nie jeden",
  "Weź trzy ostatnie miesiące, nie jeden. Jeden miesiąc prawie zawsze miał coś "
  "nietypowego — wyjazd, remont, chorobę.")
I("I policz średnią", "z tych trzech",
  "Policz z nich średnią. To twoje normalne zużycie, a nie twoje wyobrażenie "
  "o nim — a różnica między jednym a drugim bywa spora.")
I("Nie licz z pamięci", "ekran to pokazuje",
  "Nie licz z pamięci. Prawie wszyscy zaniżają swoje zużycie, bo pamiętają "
  "miesiące, w których coś ściągali, a nie te zwykłe.")
I("Teraz są porównywalne", "złote i gigabajty",
  "Z ceną po jednej stronie i gigabajtami po drugiej, to przestaje być "
  "wrażenie, a staje się arytmetyką.")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA — os passos na PRIMEIRA METADE do capitulo.
T("Rachunek", "jedno dzielenie",
  "Więc liczymy. Jedno dzielenie, potem jedno odejmowanie.",
  cap="Rachunek: jedno dzielenie")
I("Krok pierwszy", "cena przez pakiet",
  "Krok pierwszy: podziel miesięczną kwotę przez wielkość pakietu. To cena "
  "gigabajta, którą płacisz na papierze.")
I("Krok drugi", "cena przez zużycie",
  "Krok drugi: podziel tę samą kwotę przez swoje średnie zużycie. To cena "
  "gigabajta, którego naprawdę używasz.")
I("Krok trzeci", "porównaj dwie liczby",
  "Krok trzeci: porównaj obie. Jeśli druga jest znacznie wyższa, płacisz za "
  "pojemność, której nie ruszasz.")
I("I jeszcze jedno", "ile zostaje niewykorzystane",
  "Możesz to zobaczyć jeszcze prościej: odejmij zużycie od pakietu. To "
  "gigabajty, które co miesiąc przepadają.")
I("Pomnóż to", "przez cenę z kroku pierwszego",
  "Pomnóż je przez cenę z kroku pierwszego. Tyle złotych miesięcznie płacisz "
  "za nic — i to jest odpowiedź.")
I("Zapisz obie liczby", "obok siebie",
  "Zapisz obie ceny gigabajta obok siebie, zanim je porównasz. Sam widok "
  "dwóch liczb obok siebie zmienia to, co rozumiesz.")
I("Rachunek się skończył", "reszta to dlaczego",
  "Rachunek się tu kończy i możesz zrobić swój. Reszta wideo to gdzie te "
  "liczby leżą, czego nie obejmują i kiedy mylą.")

# ================== DEPOIS DA RESPOSTA — POR QUE CONTINUAR ===================

# -------------------------------------------------------------------- cap 4
T("Gdzie leżą liczby", "w telefonie i na rachunku",
  "Teraz część praktyczna: gdzie dokładnie te dwie liczby są.",
  cap="Gdzie leżą te liczby")
I("Rachunek", "w aplikacji operatora",
  "Rachunek jest w aplikacji operatora albo w mailu. Weź kwotę faktycznie "
  "pobraną, nie cennikową.")
I("Uwaga na promocje", "które się kończą",
  "Uważaj na promocje czasowe. Jeśli twoja rata za chwilę rośnie, licz tą "
  "wyższą — to ona będzie obowiązywać.")
I("Zużycie", "w ustawieniach telefonu",
  "Zużycie znajdziesz w ustawieniach telefonu, w sekcji transmisji danych. "
  "Warto ustawić tam początek okresu rozliczeniowego.")
I("Albo w aplikacji operatora", "też to pokazuje",
  "Aplikacja operatora zwykle też to pokazuje, i często z historią kilku "
  "miesięcy — to wygodniejsze niż liczenie z telefonu.")
I("Wi-Fi się nie liczy", "to nie ten pakiet",
  "Pamiętaj, że dane przez Wi-Fi to nie ten pakiet. Liczy się tylko "
  "transmisja komórkowa.")
I("Dwa numery w domu", "licz osobno",
  "Jeśli macie w domu kilka numerów na jednej umowie, policz każdy osobno. "
  "Zwykle jeden numer zużywa prawie wszystko, a reszta prawie nic.")
I("Okres rozliczeniowy", "rzadko zaczyna się pierwszego",
  "Zwróć uwagę na okres rozliczeniowy. Rzadko zaczyna się pierwszego dnia "
  "miesiąca, a licznik w telefonie domyślnie liczy właśnie od pierwszego.")
I("Jeśli daty się nie zgadzają", "licz z aplikacji operatora",
  "Jeśli daty się rozjeżdżają, weź zużycie z aplikacji operatora, bo ona "
  "liczy dokładnie w twoim okresie.")
I("Stary telefon", "kasuje historię",
  "Po zmianie telefonu historia zwykle znika. Wtedy zacznij od dzisiaj i wróć "
  "do tego za trzy miesiące — to nadal jest ta sama liczba, tylko później.")
I("W razie wątpliwości", "zaniż zużycie",
  "A w razie wątpliwości zaniż zużycie. Jeśli liczba nadal boli przy "
  "ostrożnym liczeniu, to boli naprawdę.")

# -------------------------------------------------------------------- cap 5
T("Czego rachunek nie obejmuje", "i warto to powiedzieć",
  "Są rzeczy, których ten rachunek nie łapie, i uczciwiej je nazwać niż "
  "przemilczeć.",
  cap="Czego ten rachunek nie obejmuje")
I("Zapas na wszelki wypadek", "ma wartość",
  "Pierwsza: zapas. Świadomość, że nie skończą ci się dane w podróży, ma "
  "wartość, nawet jeśli nie wychodzi z portfela.")
I("Ale zapas ma cenę", "i teraz ją znasz",
  "Ten rachunek nie mówi, że zapas jest zły. Mówi, ile on kosztuje — żebyś "
  "wybierał świadomie, a nie z przyzwyczajenia.")
I("Druga rzecz", "miesiąc nietypowy",
  "Druga: miesiąc nietypowy. Wakacje albo praca zdalna potrafią podwoić "
  "zużycie, a to nie jest twoja norma.")
I("Dlatego trzy miesiące", "a nie jeden",
  "Dlatego bierzemy trzy miesiące. Jeśli jeden odstaje mocno, zapisz go "
  "osobno i zobacz, jak często takie miesiące wracają.")
I("Trzecia rzecz", "to, co jest w pakiecie oprócz danych",
  "Trzecia: w cenie bywa coś więcej niż dane. Sprzęt na raty, usługa "
  "dodatkowa, roaming poza Unią.")
I("Jeśli tak", "wydziel to",
  "Jeśli tak jest u ciebie, wydziel te pozycje z kwoty, zanim podzielisz. "
  "Inaczej policzysz cenę danych, która nie jest ceną danych.")
I("Czwarta rzecz", "rodzina na jednej umowie",
  "Czwarta: umowa rodzinna. Wtedy pytanie nie brzmi, czy pakiet jest za duży, "
  "tylko czy jest za duży u tej jednej osoby, która go nie rusza.")
I("Piąta", "zasięg tam, gdzie mieszkasz",
  "Piąta nie jest liczbą: jakość zasięgu tam, gdzie faktycznie jesteś. "
  "Tańszy pakiet u operatora, który u ciebie nie działa, nie jest tańszy.")
I("Tego rachunek nie widzi", "a ty widzisz",
  "Tego żaden rachunek nie pokaże, a ty wiesz to z codziennego używania. "
  "Dołóż to do decyzji, ale dopiero po policzeniu.")

# -------------------------------------------------------------------- cap 6
T("Kiedy liczba myli", "pakiet, który ledwo wystarcza",
  "Teraz przypadek, który myli prawie wszystkich.",
  cap="Kiedy ta liczba myli")
I("Zużywasz prawie cały pakiet", "wygląda idealnie",
  "Jeśli zużywasz prawie cały pakiet, wygląda to na idealne dopasowanie. I "
  "często jest.")
I("Ale sprawdź jedno", "czy oszczędzasz dane",
  "Sprawdź jednak jedno: czy pod koniec okresu nie oszczędzasz świadomie. "
  "Jeśli tak, pakiet nie jest dopasowany — ty się do niego dopasowujesz.")
I("To też ma cenę", "tylko nie w złotych",
  "To również ma cenę, tylko nie w złotych. Płacisz ją niewygodą, a ona nie "
  "pojawia się na żadnym rachunku.")
I("Odwrotny przypadek", "pakiet ledwo ruszony",
  "Odwrotny przypadek to pakiet ruszony w jednej trzeciej. Tam liczba z kroku "
  "trzeciego bywa większa niż cała reszta rachunku.")
I("Jest jeszcze trzeci przypadek", "pakiet bez limitu",
  "Jest jeszcze trzeci przypadek: pakiet bez limitu. Tam dzielenie przez "
  "wielkość pakietu nie ma sensu, bo pakietu nie ma.")
I("Wtedy licz tylko drugą liczbę", "cena przez zużycie",
  "Wtedy zostaje druga liczba: kwota podzielona przez to, ile naprawdę "
  "zużywasz. I to jest jedyna cena gigabajta, jaką płacisz.")
I("Porównaj ją", "z ofertą z limitem",
  "Porównaj ją z ceną gigabajta w ofercie z limitem, która pokryłaby twoje "
  "zużycie. Bez limitu bywa tańsze, bywa dużo droższe.")
I("I jeszcze jedna rzecz o bez limitu", "wolniej po progu",
  "Wiele ofert bez limitu zwalnia po jakimś progu. Wtedy masz pakiet, tylko "
  "nazwany inaczej, i warto sprawdzić, gdzie ten próg leży.")
I("Sprawdź go w umowie", "nie w reklamie",
  "Ten próg jest w umowie, nie w reklamie. Jeśli go znajdziesz, użyj go jako "
  "wielkości pakietu w kroku pierwszym.")
I("Obie odpowiedzi są dobre", "twoja liczba decyduje",
  "Duży pakiet i mały pakiet są jednakowo uzasadnione i żaden nie jest lepszy "
  "z zasady. Lepszy jest ten, na który wskazuje twoja liczba. Złe jest tylko "
  "przedłużanie umowy bez spojrzenia.")

# -------------------------------------------------------------------- cap 7
T("Od miesiąca", "do umowy",
  "Teraz krok, który pokazuje skalę.",
  cap="Od miesiąca do całej umowy")
I("Jeden miesiąc", "wygląda na drobiazg",
  "Jeden miesiąc wygląda na drobiazg, jakakolwiek by nie była ta liczba. I "
  "dlatego przechodzi bez zatrzymania.")
I("Pomnóż przez dwanaście", "i przez lata umowy",
  "Pomnóż przez dwanaście, a potem przez liczbę lat, przez które masz tę samą "
  "umowę. To samo zachowanie, zsumowane.")
I("Potem spójrz do przodu", "umowa wraca",
  "Potem spójrz w przód, bo umowa wraca w konkretnym miesiącu, i ta sama "
  "liczba wraca razem z nią.")
I("Porównaj z czymś znanym", "żeby poczuć rozmiar",
  "Żeby poczuć rozmiar, porównaj z czymś, co znasz: z jednym rachunkiem za "
  "prąd, albo z miesiącem innego abonamentu.")
I("Może wyjść mało", "to też odpowiedź",
  "Może wyjść niewiele i nic nie trzeba zmieniać. To pełna odpowiedź, i teraz "
  "jest policzona zamiast wyobrażona.")
I("I policz jeszcze jedno", "ile lat płacisz to samo",
  "Policz jeszcze jedną rzecz: ile lat masz ten sam pakiet. Jeśli więcej niż "
  "trzy, to prawie na pewno pakiet z innej epoki twojego telefonu.")
I("Zużycie rośnie z czasem", "pakiet zwykle nie",
  "Zużycie zwykle rośnie z latami, a pakiet zostaje ten sam. To znaczy, że ta "
  "liczba mogła być kiedyś duża, a dziś być mała — albo odwrotnie.")
I("Dlatego licz teraz", "nie pamiętaj",
  "Dlatego licz na dzisiejszych trzech miesiącach, a nie na tym, co "
  "pamiętasz z momentu podpisywania umowy.")
I("I sprawdź drugą stronę", "czy pakiet się nie zmienił",
  "Sprawdź też, czy sam pakiet nie zmieniał się po drodze. Operatorzy czasem "
  "powiększają go bez zmiany ceny, i wtedy twoja stara liczba jest nieaktualna "
  "w drugą stronę.")
I("Dobra strona", "decyzja wraca",
  "Dobra strona jest taka, że ta decyzja wraca przy każdym przedłużeniu, cała. "
  "Jeden zły rok nie zobowiązuje następnego.")

# -------------------------------------------------------------------- cap 8
T("Co z tą liczbą zrobić", "zanim zadzwonisz",
  "Zanim cokolwiek zmienisz, dwie rzeczy warto wiedzieć.",
  cap="Co zrobić z tą liczbą")
I("Nie zaczynaj od zmiany operatora", "zacznij od swojego",
  "Nie zaczynaj od zmiany operatora. Zacznij od własnego: mniejszy pakiet u "
  "tego samego zwykle jest najprostszą zmianą.")
I("Miej liczbę przy sobie", "gdy dzwonisz",
  "Gdy dzwonisz, miej tę liczbę przy sobie. Rozmowa o twoim zużyciu wygląda "
  "inaczej niż rozmowa o ofertach.")
I("Zmieniaj jedno", "nie wszystko naraz",
  "I zmieniaj jedną rzecz naraz: albo pakiet, albo operatora. Obie zmiany "
  "jednocześnie oznaczają, że nie dowiesz się, która zadziałała.")
I("Zapytaj o jedno", "co dostaniesz przy mniejszym pakiecie",
  "W rozmowie zapytaj konkretnie: ile kosztuje ten sam abonament z mniejszym "
  "pakietem. To pytanie z liczbą, a nie prośba o obniżkę.")
I("I zapytaj o drugie", "co się zmienia poza pakietem",
  "I zapytaj, co jeszcze zmienia się przy tej opcji: zasięg, roaming, "
  "priorytet w sieci. Czasem różnica jest tylko w cenie, czasem nie.")
I("Nie musisz decydować od razu", "masz datę",
  "Nie musisz decydować w trakcie rozmowy. Masz zapisaną datę końca umowy i "
  "masz swoją liczbę — to wystarcza, żeby wrócić do tego spokojnie.")
I("A jeśli zostajesz", "to też jest decyzja",
  "A jeśli po tym wszystkim zostajesz przy swoim pakiecie, to również jest "
  "decyzja, tylko teraz podjęta z liczbą zamiast z przyzwyczajenia.")
I("Sprawdź po trzech miesiącach", "raz",
  "Sprawdź ponownie po trzech miesiącach, jeden raz. Wcześniej to jeszcze nie "
  "dane, tylko szum.")

# -------------------------------------------------------------------- cap 9
T("Co zrobić dzisiaj", "trzy kroki",
  "Kończymy tym, co można zrobić dzisiaj, w trzech krokach.",
  cap="Co zrobić dzisiaj")
L("Trzy kroki",
  ["Weź kwotę z rachunku", "Sprawdź zużycie z trzech miesięcy",
   "Podziel i odejmij"],
  "Pierwszy: weź kwotę faktycznie pobraną z rachunku. Drugi: sprawdź zużycie "
  "danych z trzech ostatnich miesięcy i policz średnią. Trzeci: podziel kwotę "
  "przez pakiet, potem przez zużycie, i porównaj.")
I("Zapisz też datę", "końca umowy",
  "Zapisz obok datę końca umowy. Ta jedna linijka zamienia ciekawą liczbę w "
  "liczbę użyteczną.")
I("Nic dziś nie zmieniaj", "wystarczy wiedzieć",
  "Dziś nie musisz nic zmieniać. Sama świadomość tej liczby to cały krok.")
# EXPERIMENTO 26 — o pedido do longo tambem fecha em conta.
I("Zrób to raz", "nie rób z tego rutyny",
  "Zrób to raz. To nie jest tabelka do prowadzenia co miesiąc, tylko jedna "
  "liczba, którą się poznaje i zapamiętuje.")
I("Jedna kartka wystarczy", "cztery linijki",
  "Cztery linijki na kartce wystarczą: kwota, pakiet, zużycie i data końca "
  "umowy. Ostatnia linijka jest tą, która sprawia, że reszta się przydaje.")
I("Zrób to też dla drugiego numeru", "jeśli jest",
  "Jeśli w domu jest drugi numer na tej samej umowie, zrób to samo dla niego. "
  "Bardzo często cała różnica siedzi w jednym z nich.")
I("I zostaw to na tym", "dziś nic więcej",
  "I na tym dziś poprzestań. Reszta zdarzy się sama, w miesiącu, w którym "
  "umowa wróci.")
C("Napisz swoją liczbę", "w komentarzu",
  "Jeśli policzysz, napisz pod spodem jedną rzecz: ile złotych miesięcznie "
  "płacisz za niewykorzystane gigabajty. Bez nazwy operatora, bez kwoty "
  "rachunku. Ciekawi mnie, jak bardzo te liczby się różnią.")

# =============================== O SHORT =====================================
# EXPERIMENTO 26, sexto braco.

SHORT = [
    {"layout": "titulo", "kicker": "Twój rachunek za telefon",
     "sub": "ile idzie w nic?",
     "nar": "Ile z twojego rachunku za telefon idzie za gigabajty, których nie "
            "zużywasz? Dwie liczby, obie już masz.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Pierwsza", "sub": "kwota przez pakiet",
     "nar": "Pierwsza: miesięczną kwotę podziel przez wielkość pakietu. To "
            "cena gigabajta.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Druga", "sub": "pakiet minus zużycie",
     "nar": "Druga: od pakietu odejmij swoje średnie zużycie z trzech "
            "miesięcy. To gigabajty, które przepadają.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Pomnóż", "sub": "to twoja odpowiedź",
     "nar": "Pomnóż jedno przez drugie. Tyle złotych miesięcznie płacisz za "
            "nic. Razy dwanaście — i masz rok.", "sem_cap": True},
    {"layout": "cta", "kicker": "Jeśli się przydało",
     "sub": "subskrybuj — jedno liczenie tygodniowo",
     "nar": "Jeśli się przydało, subskrybuj. Jedno takie liczenie tygodniowo, "
            "na twoich własnych liczbach.", "sem_cap": True},
]

THUMB = {"l1": "Ile płacisz", "l2": "za nic"}

COPY = """# Ile złotych miesięcznie płacisz za gigabajty, których nie zużywasz

## TITULO
Ile Płacisz za Dane, Których Nie Zużywasz? Policz z Własnego Rachunku

## DESCRICAO
Co miesiąc płacisz rachunek za telefon, i bardzo prawdopodobne, że część tej kwoty idzie za gigabajty, których nigdy nie tkniesz. To nie jest wideo o tym, że operatorzy oszukują — to wideo o tym, ile kosztuje twój własny pakiet, a to zupełnie inne pytanie. Ma też termin, który znasz: koniec umowy albo miesiąc, w którym możesz ją zmienić.

Nie ma tu ani jednej mojej liczby. Żadnej ceny planu, żadnego operatora, żadnej średniej zużycia. Obie liczby są twoje i obie już istnieją: jedna na rachunku, druga w ustawieniach transmisji danych w telefonie.

Rachunek to jedno dzielenie i jedno odejmowanie. Podziel miesięczną kwotę przez wielkość pakietu — to cena gigabajta na papierze. Potem podziel tę samą kwotę przez swoje średnie zużycie z trzech ostatnich miesięcy — to cena gigabajta, którego naprawdę używasz. Jeśli druga liczba jest znacznie wyższa, płacisz za pojemność, której nie ruszasz. Można to zobaczyć jeszcze prościej: odejmij zużycie od pakietu i pomnóż przez cenę gigabajta. Tyle złotych miesięcznie płacisz za nic.

Bierzemy trzy miesiące, nie jeden, bo jeden prawie zawsze miał coś nietypowego.

Jeden rozdział pokazuje, gdzie te liczby leżą: kwota faktycznie pobrana w aplikacji operatora (uwaga na promocje, które się kończą), zużycie w ustawieniach telefonu albo w aplikacji operatora z historią kilku miesięcy. Dane przez Wi-Fi się nie liczą. Jeśli na jednej umowie jest kilka numerów, policz każdy osobno.

Jeden rozdział mówi, czego ten rachunek nie obejmuje: zapas na wszelki wypadek, który ma wartość, choć nie wychodzi z portfela; miesiąc nietypowy; i to, co bywa w cenie oprócz danych — sprzęt na raty, usługa dodatkowa, roaming poza Unią, które trzeba wydzielić przed dzieleniem.

I jeden rozdział o przypadku, który myli: jeśli zużywasz prawie cały pakiet, wygląda to na idealne dopasowanie — ale sprawdź, czy pod koniec okresu nie oszczędzasz świadomie. Wtedy to nie pakiet jest dopasowany do ciebie, tylko ty do niego, a ta cena nie pojawia się na żadnym rachunku.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Policz i napisz pod spodem jedną rzecz: ile złotych miesięcznie płacisz za niewykorzystane gigabajty. Bez nazwy operatora, bez kwoty rachunku, sama liczba. Ciekawi mnie, jak bardzo te liczby różnią się między ludźmi z podobnym telefonem.

## HASHTAGS
#FinanseOsobiste #Abonament #KolejnyPoziom

## TAGS
rachunek za telefon, abonament komorkowy, ile place za internet w telefonie, transmisja danych, zuzycie danych, pakiet gigabajtow, koniec umowy, zmiana abonamentu, finanse osobiste, domowy budzet, oszczedzanie na abonamencie, cena gigabajta, operator komorkowy, policz sam, staly wydatek

## CONFIGURACOES DO STUDIO
- Idioma: Polones (pl) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Polonia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita preco de plano, nao cita operadora, nao cita media de consumo de ninguem, nao cita tamanho tipico de pacote e nao compara ofertas entre si. As duas unicas fontes sao o rachunek do proprio espectador e a tela de transmissao de dados do aparelho dele. Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa da operadora ou do plano dele. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA: qualquer preco de abonamento ou tamanho de pacote. Esses valores mudam por operadora, por promocao e por mes, e citar um so deles tornaria a conta errada para a maioria de quem assiste. O video tambem nao recomenda operadora nem plano, nao diz que pacote grande e ruim — as duas respostas dependem do numero de cada um —, nao promete economia e nao e aconselhamento financeiro.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/kolejny-poziom-014.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-014",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841", "bg": "#F4F1EA"},
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
    grava(SPEC, "fabrica/specs/kolejny-poziom-014.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
