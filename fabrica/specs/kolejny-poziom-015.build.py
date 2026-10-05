"""kolejny-poziom-015 — ile naprawdę kosztuje cię twoja składka PPK.

ALAVANCA ATACADA: A (travessia short -> longo). E este canal e a SEGUNDA
confirmacao independente do aprendizado 577, com dezenove pacotes — e aqui o
efeito e ainda mais cru que no epomeno-epipedo.

O NUMERO DE PARTIDA, lado a lado:

    pacote  short  longo   o que o longo responde
    013       27    103    emprestimo curto ou longo? duas multiplicacoes do
                           SEU contrato  <- MELHOR LONGO DO CANAL
    010       72     64    ryczalt: um zloty acima do limite custa quase 4000
    012       42     63    a luz baixa e a conta sobe: calcule o SEU preco
    003       47     47    IKE ou IKZE? um numero resolve a escolha inteira
    006      172     42    seis ofertas de titulo, uma perde da inflacao
    011       68     39    limite de 120 mil: onde voce esta na escala
    004       86     27    taxas e imposto Belki sobre 200 zl por mes
    007      287     21    amortizar ou investir?  <- MAIOR SHORT DO CANAL
    008       34     17    mesma renda, dois bancos, duas respostas
    005        0     17    salario minimo: o empregador paga 5862, voce recebe
    014        0     16    quanto paga por dados que nao usa
    009       69      6    seguro OC mais barato em dois anos

O ACHADO: o MAIOR short do canal (287 views, pacote 007) entregou 21 views de
longo. O MELHOR longo do canal (103 views, pacote 013) veio de um short de 27
views — um decimo do alcance, cinco vezes o resultado. Igual ao epomeno (1.614
-> 110 contra 540 -> 431), em outro idioma, outro assunto, outra amostra.

E o que o 013 tem: "duas multiplicacoes do SEU contrato". O 010 tem um limite
com consequencia em zlotys. O 003 tem uma escolha que um numero resolve. O pior
longo do canal, o 009, entrega CONSTATACAO datada que nao e do espectador: o
seguro OC esta mais barato em dois anos.

O QUE DEU CERTO: decisao do espectador, com a conta feita nos papeis dele.
O QUE NAO DEU: alcance de short, e constatacao sobre o mercado.
O QUE VOU MUDAR: a pauta e uma decisao com DATA que se repete por lei, e os dois
numeros vem do contracheque do proprio espectador.

EIXO, e por que ele e novo. Os dezenove anteriores falam de emprestimo (tres
vezes), de IKE e IKZE, de titulos do tesouro, de ryczalt, de limite de imposto,
de seguro OC, de luz, de salario minimo, de dados moveis, de taxas e de ZUS.
Nenhum fala do PPK — que e o terceiro pilar, distinto do ZUS do
kp-emerytura e do IKE/IKZE do 003. E o PPK tem a propriedade que o 008 do
epomeno mostrou valer mais que qualquer alcance: uma DATA. A renuncia expira e o
reinscricao automatica volta, entao a decisao tem prazo por desenho da lei, nao
por conjuntura.

ATENCAO AO VEREDITO: `suspenso` (v_maquina_licoes, 04/10/2026). Logo, piso de
oito minutos E o melhor material no SHORT. As duas coisas foram obedecidas: o
longo fica logo acima do minimo aritmetico dos oito capitulos, e o short carrega
a conta inteira — nao a manchete.

ALAVANCA B: a resposta dentro dos duzentos segundos, medida no legendas.srt, e
posicionada pela estimativa CORRIGIDA (aprendizado 575). A `pl-PL-MarekNeural`
tem residuo de menos um virgula cinco por cento, n=409 — residuo NEGATIVO, ou
seja o real vem mais curto que a estimativa, o que aqui joga a favor. A conta
foi feita de todo jeito, porque foi nao fazer que custou dois virgula dois
segundos no seja-mais-magra-009.

TITULO PROPRIO DO SHORT: tem, e a estrutura imita o 013 e o 010 — a decisao mais
a consequencia em zlotys. Similaridade maxima contra o corpus de cento e
quarenta e seis titulos: zero virgula trezentos e cinquenta e seis.

DOIS SHORTS DESTE CANAL ESTAO COM ZERO VIEWS (005 e 014, e o 014 e o mais
recente, de primeiro de setembro). Isso nao e travessia ruim, e short que nao
foi entregue a ninguem. Fica dito aqui porque dois zeros em dezenove merecem
olhar do dono quando ele tiver o Analytics.
"""

import json

CENAS = []

# Resolvidos por `pg_net` dentro do Postgres (aprendizado 574).
BROLL = {
    7490379: ("https://videos.pexels.com/video-files/7490379/7490379-hd_1280_720_30fps.mp4",
              "RDNE Stock project",
              "https://www.pexels.com/video/person-affixing-her-signature-7490379/"),
    8661806: ("https://videos.pexels.com/video-files/8661806/8661806-hd_1280_720_25fps.mp4",
              "Adrian Frentescu",
              "https://www.pexels.com/video/person-placing-coin-on-stacks-8661806/"),
    7735903: ("https://videos.pexels.com/video-files/7735903/7735903-hd_1280_720_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/a-person-calculating-family-budget-7735903/"),
    6975457: ("https://videos.pexels.com/video-files/6975457/6975457-hd_1366_720_25fps.mp4",
              "T Leish",
              "https://www.pexels.com/video/a-couple-talking-while-reading-6975457/"),
}


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def B(kicker, sub, nar, q, pexels_id=None, cap=None):
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q}
    if pexels_id and pexels_id in BROLL:
        link, autor, pagina = BROLL[pexels_id]
        c["broll_url"] = link
        c["broll_credito"] = {"pexels_id": pexels_id, "autor": autor,
                              "url": pagina}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ================== PIERWSZE DWIEŚCIE SEKUND ================================

# -------------------------------------------------------------------- cap 1
T("Dwie liczby", "na tym samym pasku",
  "Na twoim pasku wypłaty są dwie liczby dotyczące PPK. Jedna to twoja "
  "składka, druga to ile naprawdę ubyło ci z wypłaty. Nie są równe.",
  cap="Twoja składka i to, co faktycznie ubyło z wypłaty")
T("Nikt nic nie ukrywa", "pasek jest poprawny",
  "Pasek nie jest błędny i nikt nic nie ukrywa. Pokazuje sumy, a sumy tej "
  "różnicy nie pokazują.")
T("Pierwsza jest łatwa", "stoi wprost na pasku",
  "Pierwszą znajdziesz od razu: to linia składki pracownika, podana w "
  "złotych. To liczba brutto.")
B("Druga nie stoi nigdzie", "trzeba ją policzyć",
  "Drugiej nie ma na pasku w żadnej linii. Trzeba ją policzyć, i to ona "
  "decyduje, bo to ona realnie wychodzi z twojego konta.",
  "person holding a paper document and pen", 7490379)
T("Czemu nie są równe", "bo składka zmienia podatek",
  "Nie są równe, bo twoja składka zmienia podstawę, od której liczy się "
  "podatek. Część tego, co wpłacasz, wraca do ciebie niższym podatkiem.")
T("Co to kosztuje", "decyzję, nie złotówki",
  "Kosztuje cię decyzję: patrzysz na brutto, bierzesz je za cenę i "
  "rezygnujesz z czegoś tańszego, niż myślałeś.")
T("Albo odwrotnie", "zostajesz nie wiedząc ile płacisz",
  "Albo odwrotnie: zostajesz, nie wiedząc ile płacisz miesięcznie — i to też "
  "jest decyzja bez liczby.")
T("Żadnej mojej liczby", "w całym materiale",
  "Nie ma tu żadnej mojej liczby: ani stawki, ani progu. Oba numery są na "
  "twoich paskach.")
T("Termin też jest twój", "data ponownego zapisu",
  "Termin też jest twój: rezygnacja z PPK wygasa i zapis wraca automatycznie. "
  "Data jest w ustawie, więc decyzja ma termin z definicji.")

# -------------------------------------------------------------------- cap 2
T("Co wychodzi", "i co wpływa",
  "Warto rozdzielić trzy rzeczy, bo mieszanie ich jest powodem, dla którego "
  "większość ludzi nie wie, ile ten program ich kosztuje.",
  cap="Co wychodzi z wypłaty, a co wpływa na konto")
T("Pierwsza", "twoja składka",
  "Pierwsza to twoja składka. Wychodzi z twojej wypłaty i trafia na twoje "
  "konto PPK.")
T("Druga", "składka pracodawcy",
  "Druga to składka pracodawcy. Nie wychodzi z twojej wypłaty i też trafia na "
  "twoje konto — ale podnosi twoją podstawę podatkową.")
B("Trzecia", "wpłaty od państwa",
  "Trzecia to wpłaty od państwa. Nie wychodzą z twojej wypłaty, trafiają na "
  "twoje konto i nie zależą od tego, ile zarabiasz.",
  "person placing coin on stacks", 8661806)
T("Dlaczego to miesza", "bo wszystkie trzy są na jednym koncie",
  "Mieszają się, bo wszystkie trzy lądują na tym samym koncie. Patrzysz na "
  "saldo i widzisz sumę, która nie mówi nic o twoim koszcie.")
T("Twój koszt", "to tylko pierwsza, minus podatek",
  "Twój koszt to wyłącznie pierwsza z tych trzech, i to jeszcze pomniejszona "
  "o podatek, którego nie zapłaciłeś.")
T("A twoja korzyść", "to pozostałe dwie",
  "Twoja korzyść to pozostałe dwie, plus to, co urośnie. Ale korzyść i koszt "
  "liczy się osobno, inaczej jedno zasłania drugie.")
T("Dziś liczymy koszt", "bo on jest pewny",
  "Dzisiaj liczymy koszt, nie korzyść. Koszt jest pewny i już się wydarzył, a "
  "korzyść zależy od rynku i od lat.")
T("Co teraz", "rachunek w dwóch krokach",
  "Teraz rachunek. Dwa kroki, dwa paski wypłaty i nic poza tym, co już masz w "
  "szufladzie.")

# -------------------------------------------------------------------- cap 3
T("Krok pierwszy", "dwa miesiące do porównania",
  "Krok pierwszy: znajdź dwa paski. Jeden z miesiąca ze składką PPK i jeden z "
  "miesiąca bez niej, możliwie blisko siebie.",
  cap="Rachunek: dwa paski i jedno odejmowanie")
T("Bez premii", "i bez wyrównań",
  "Omijaj miesiące z premią, nagrodą, wyrównaniem czy trzynastką. One zmieniają "
  "sumę i różnica przestaje dotyczyć składki.")
T("Jeśli nie masz miesiąca bez", "weź pasek z pierwszego miesiąca",
  "Nie masz miesiąca bez PPK? Weź pasek z miesiąca, w którym składka ruszyła "
  "w połowie.")
T("Krok drugi", "różnica w kwocie do wypłaty",
  "Krok drugi: odejmij kwotę do wypłaty z miesiąca ze składką od kwoty do "
  "wypłaty z miesiąca bez niej. Do wypłaty, nie brutto.")
T("To jest twój koszt", "miesięcznie, w złotych",
  "Ta różnica to twój realny koszt PPK na miesiąc, w złotych. To ona wychodzi "
  "z twojego konta, i to ona powinna stać w każdej twojej decyzji.")
T("Teraz porównaj", "z linią składki",
  "Teraz porównaj tę różnicę z linią twojej składki na pasku. Różnica będzie "
  "mniejsza, i to o tyle, ile oddał ci podatek.")
T("Odległość", "to jest ta informacja",
  "Odległość między tymi dwiema liczbami jest całą informacją. Linia składki "
  "mówi, ile wpłacasz; różnica mówi, ile cię to kosztuje.")
T("Zapisz obie", "nie tylko jedną",
  "Zapisz obie, nie tylko koszt. Bez linii składki nie będziesz wiedział "
  "później, która z dwóch się zmieniła.")
T("Jedna uwaga", "to nie jest zysk",
  "Jedna uwaga od razu: to, że koszt jest mniejszy od składki, nie jest "
  "zyskiem. To tylko znaczy, że cena jest inna niż ta na pasku.")

# ========================= PO ODPOWIEDZI ====================================

# -------------------------------------------------------------------- cap 4
T("Dlaczego koszt", "a nie procent",
  "Powód, dla którego liczymy złote na miesiąc, a nie procent, jest prosty: "
  "procent jest taki sam dla wszystkich, a złote są twoje.",
  cap="Dlaczego złote na miesiąc, a nie procent")
T("Ten sam procent", "dwie różne kwoty",
  "Ten sam procent daje dwie różne kwoty u dwóch osób z różną pensją, i trzecią "
  "u osoby, która w tym roku przeszła próg podatkowy.")
T("I u ciebie też", "inny w styczniu, inny w listopadzie",
  "I u ciebie też bywa inny w styczniu niż w listopadzie, bo dochód narastająco "
  "przesuwa się w skali przez cały rok.")
B("Procent nie da się porównać", "z ratą ani z rachunkiem",
  "A procentu nie da się porównać z niczym, co faktycznie płacisz. Złote na "
  "miesiąc porównasz z ratą, z rachunkiem, z czymkolwiek.",
  "calculator on top of documents", 7735903)
T("To nie jest niesprawiedliwość", "to jest skala",
  "To nie jest niesprawiedliwość ani błąd. To skala, a skala znaczy, że liczba "
  "zależy od miejsca, w którym stoisz.")
T("Co zyskujesz", "porównywalną cenę",
  "Zyskujesz cenę, którą można porównać. Dopiero wtedy pytanie, czy warto, ma "
  "sens, bo wcześniej nie wiedziałeś, o jakiej kwocie mówisz.")
T("I działa w drugą stronę", "znajduje też tanie lata",
  "Działa też w drugą stronę: w roku, w którym twój koszt wychodzi niski, "
  "rezygnacja oszczędza mniej, niż się wydaje.")
T("Liczba nie ocenia", "programu ani ciebie",
  "Ta liczba nie ocenia programu i nie ocenia ciebie. Mówi, ile to kosztuje "
  "teraz, u ciebie.")
T("Dalej", "decyzja i jej data",
  "Zostaje decyzja i jej data, bo ta data wraca sama, bez twojego udziału.")

# -------------------------------------------------------------------- cap 5
T("Decyzja ma termin", "i on się powtarza",
  "Decyzja o PPK ma tę rzadką cechę, że wraca sama. Rezygnacja nie jest "
  "wieczna i zapis wraca automatycznie, w dacie zapisanej w ustawie.",
  cap="Decyzja, która wraca sama: jak ją czytać")
T("Co to znaczy", "że milczenie jest wyborem",
  "Znaczy to, że milczenie też jest wyborem. Jeśli nic nie zrobisz, program "
  "wraca, a twój koszt wraca razem z nim.")
T("Dwa warunki", "oba muszą zagrać",
  "Dwa warunki, i oba muszą zagrać, żeby decyzja była policzona, a nie "
  "odruchowa.")
T("Pierwszy", "koszt mieści się w twoim miesiącu",
  "Pierwszy: twój koszt w złotych mieści się w twoim miesiącu bez zmiany "
  "niczego innego. To ty wiesz, czy się mieści.")
T("Drugi", "policzyłeś go w tym roku",
  "Drugi: liczba jest z tego roku, nie z poprzedniego. Przy zmianie pensji albo "
  "progu stary rachunek nie obowiązuje.")
T("Kiedy koszt jest mały", "zostanie jest tanie",
  "Kiedy koszt wychodzi mały, zostanie w programie jest tańsze, niż sugeruje "
  "linia składki, i rezygnacja oszczędza mniej, niż się wydawało.")
T("Kiedy jest duży", "wtedy warto policzyć drugi raz",
  "Kiedy wychodzi duży, warto policzyć drugi raz w innym miesiącu, bo mogłeś "
  "trafić na miesiąc z czymś dodatkowym w środku.")
T("Czego nie robić", "nie decyduj z salda konta",
  "Czego nie robić: nie decyduj, patrząc na saldo konta PPK. Tam leżą trzy "
  "wpłaty, a tylko jedna jest twoim kosztem.")
T("I nie porównuj", "z kolegą z biurka obok",
  "I nie porównuj swojego kosztu z kolegą obok. Ta sama składka procentowo "
  "daje inny koszt w złotych u każdego z was.")

# -------------------------------------------------------------------- cap 6
T("Trzy błędy", "które ten rachunek ujawnia",
  "Z liczbą na papierze trzy zwykłe błędy stają się widoczne. Wszystkie trzy "
  "to jedno pomylenie: brutto w miejscu kosztu.",
  cap="Trzy błędy, które ten rachunek ujawnia")
T("Błąd pierwszy", "czytać linię składki jako cenę",
  "Błąd pierwszy: czytać linię składki jako cenę. To kwota wpłaty, a nie to, "
  "co ubyło ci z konta.")
T("Błąd drugi", "liczyć z salda PPK",
  "Błąd drugi: liczyć z salda konta PPK. Saldo rośnie też od pieniędzy, które "
  "nie są twoje, i zawyża wszystko.")
T("Błąd trzeci", "jeden miesiąc",
  "Błąd trzeci: wnioskować z jednego miesiąca. Jeden pasek nie ma w sobie "
  "porównania, a rachunek potrzebuje dwóch.")
T("Żaden z trzech", "to nie naiwność",
  "Żaden z tych trzech to nie naiwność. To błąd pomiaru, więc naprawia się go "
  "pomiarem, a nie poradą.")
B("Najdroższy przypadek", "rezygnacja bez liczby",
  "Najdroższy przypadek to rezygnacja podjęta na podstawie linii składki, bo "
  "realny koszt był niższy i decyzja oparła się na złej kwocie.",
  "couple reading papers at a table", 6975457)
T("I odwrotnie", "zostanie bez liczby",
  "Odwrotnie też boli: zostanie w programie przez lata bez policzenia kosztu, "
  "w roku, w którym był on akurat wysoki.")
T("I jeszcze jeden", "porównywać się z saldem kolegi",
  "Jest jeszcze czwarty, rzadszy: porównywać swoje saldo z saldem kolegi, "
  "który jest w programie dłużej. Saldo rośnie z czasem i z trzech źródeł, "
  "więc taka różnica nie mówi nic o koszcie żadnego z was.")
T("Ta sama liczba", "rozstrzyga oba",
  "Ta sama liczba rozstrzyga oba przypadki, i dlatego warte jest tych pięciu "
  "minut.")

# -------------------------------------------------------------------- cap 7
T("Co zapisać", "i w jakiej formie",
  "Forma zapisu decyduje o tym, czy rachunek przyda ci się jeszcze za rok, gdy "
  "data wróci.",
  cap="Co zapisać, i dlaczego dwie liczby, a nie jedna")
T("Dwie liczby", "i miesiąc",
  "Zapisz dwie liczby i miesiąc: linię składki, realny koszt i to, z jakiego "
  "miesiąca pochodzą.")
T("Miesiąc nie jest ozdobą", "to miejsce w roku",
  "Miesiąc nie jest ozdobą. To miejsce w roku, a miejsce w roku jest połową "
  "powodu, dla którego liczba wyszła taka, a nie inna.")
T("Nie zapisuj procentu", "zapisz złote",
  "Nie zapisuj procentu. Zapisz złote na miesiąc, bo procent wygląda "
  "porównywalnie między ludźmi, nie będąc porównywalnym.")
T("Kartka wystarczy", "i notatka w telefonie też",
  "Kartka wystarczy. Notatka w telefonie wystarczy. Byleby widać było liczby i "
  "miesiąc, a nie tylko sumę na koniec roku.")
T("Dwa pomiary", "początek i koniec roku",
  "Dwa pomiary w roku wystarczą: jeden na początku i jeden blisko końca, bo "
  "wtedy dochód narastająco jest najwyżej.")
T("Jeśli różnica skacze", "to też informacja",
  "Jeśli odległość między składką a kosztem mocno się zmieni między pomiarami, "
  "to też informacja: przesunąłeś się w skali.")
T("Jedna kolumna więcej", "ile wynosiła pensja",
  "Jeśli chcesz jedną kolumnę więcej, dopisz pensję brutto z tego miesiąca. "
  "Dwa pomiary z różną pensją pokazują, jak mocno twój koszt zależy od miejsca "
  "w skali, a to jest najużyteczniejsza informacja z całej tabelki.")
T("Nic z tego", "nie wymaga zakupu",
  "I nic z tego nie wymaga aplikacji, subskrypcji ani doradcy. Wymaga dwóch "
  "pasków i jednego odejmowania.")

# -------------------------------------------------------------------- cap 8
T("Zastrzeżenie", "i liczy się bardziej niż rachunek",
  "Zostaje zastrzeżenie, i liczy się ono bardziej niż sam rachunek.",
  cap="Czego ten rachunek NIE mówi")
T("Nie mówi", "czy zostać czy zrezygnować",
  "Ten rachunek nie mówi, czy zostać w PPK, czy zrezygnować. Mówi, ile to "
  "kosztuje miesięcznie u ciebie. Decyzja ma w sobie więcej niż cenę.")
T("Nie liczy korzyści", "ani przyszłej wartości",
  "Nie liczy też korzyści. Składka pracodawcy, wpłaty od państwa i to, co "
  "urośnie, są poza tym rachunkiem, i są realne.")
T("Nie jest doradztwem", "ani podatkowym, ani inwestycyjnym",
  "Nie jest to doradztwo podatkowe ani inwestycyjne. To pomiar na dwóch "
  "kartkach, które już masz.")
T("I nie sprawdza", "czy pasek jest poprawny",
  "I nie sprawdza, czy twój pasek jest poprawny. Jeśli podejrzewasz błąd w "
  "składkach, to inna rozmowa i inna osoba.")
T("Co ci zostaje", "kwota na miesiąc",
  "Zostaje ci kwota w złotych na miesiąc, policzona z twoich papierów, na twój "
  "rok — i data, w której pytanie wróci samo.")
T("Zacznij od szuflady", "dwa paski",
  "Zacznij od szuflady: dwa paski, jeden ze składką i jeden bez, zanim data "
  "wróci sama.")
C("Napisz kwotę niżej", "tylko złote na miesiąc",
  "W komentarzu napisz samą kwotę: złote na miesiąc, realny koszt. Nie pensję, "
  "nie pracodawcę. Chcę zobaczyć, jak daleko od siebie wypadają ludzie z "
  "podobnym paskiem.")

# ================================== SHORT ====================================

# Veredito `suspenso` manda o MELHOR material no short. Entao o short carrega a
# conta INTEIRA — os dois paskow, a subtracao e o que o numero significa — e o
# longo abre outra pergunta: a data que volta sozinha (aprendizado 563).
# Quarenta segundos, no teto util do canal.

SHORT = [
    {"layout": "titulo", "kicker": "Dwie liczby", "sub": "na tym samym pasku",
     "nar": "Linia twojej składki PPK i to, co faktycznie ubyło z wypłaty, to "
            "dwie różne liczby. Druga jest mniejsza i to ona jest ceną.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Pierwsze", "sub": "dwa paski",
     "nar": "Weź dwa paski: miesiąc ze składką i miesiąc bez. Bez premii i bez "
            "wyrównań.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Drugie", "sub": "odejmij do wypłaty",
     "nar": "Odejmij kwotę do wypłaty jednego od kwoty do wypłaty drugiego. Do "
            "wypłaty, nie brutto.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "To jest koszt", "sub": "złote na miesiąc",
     "nar": "Ta różnica to twój realny koszt na miesiąc. Będzie mniejsza od "
            "linii składki, bo część wróciła niższym podatkiem.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Data wraca sama", "sub": "w materiale",
     "nar": "Rezygnacja wygasa i zapis wraca automatycznie. Co z tym zrobić "
            "jest w materiale.",
     "sem_cap": True},
]

THUMB = {"l1": "Ile naprawdę", "l2": "płacisz"}

COPY = """# Realny koszt składki PPK, policzony z dwóch pasków wypłaty

## TITULO
PPK: Ile Kosztuje Cię Naprawdę Twoja Składka — i Data Ponownego Zapisu

## TITULO SHORT
Twoja składka PPK: ile to realnie?

## DESCRICAO
Na twoim pasku wypłaty są dwie liczby dotyczące PPK. Pierwsza stoi wprost: linia składki pracownika, w złotych. Drugiej nie ma w żadnej linii — to kwota, która faktycznie ubyła ci z wypłaty. Nie są równe, bo składka zmienia podstawę, od której liczy się podatek, więc część tego, co wpłacasz, wraca do ciebie niższym podatkiem. Decyduje druga, bo to ona realnie wychodzi z konta.

Warto najpierw rozdzielić trzy strumienie, bo ich mieszanie jest powodem, dla którego większość ludzi nie wie, ile ten program ich kosztuje: twoja składka (wychodzi z twojej wypłaty), składka pracodawcy (nie wychodzi, ale podnosi twoją podstawę podatkową) i wpłaty od państwa (nie wychodzą i nie zależą od pensji). Wszystkie trzy lądują na tym samym koncie, więc saldo pokazuje sumę, która nie mówi nic o twoim koszcie. Twój koszt to wyłącznie pierwszy strumień, pomniejszony o podatek, którego nie zapłaciłeś.

Rachunek ma dwa kroki i żadnej mojej liczby. Krok pierwszy: dwa paski — jeden z miesiąca ze składką PPK i jeden bez niej, możliwie blisko siebie, z pominięciem miesięcy z premią, nagrodą, wyrównaniem czy trzynastką, bo one zmieniają sumę. Krok drugi: odejmij kwotę do wypłaty z miesiąca ze składką od kwoty do wypłaty z miesiąca bez niej — do wypłaty, nie brutto. Ta różnica to twój realny koszt w złotych na miesiąc. Porównaj ją z linią składki: będzie mniejsza, i to o tyle, ile oddał ci podatek. Odległość między tymi dwiema liczbami jest całą informacją.

Materiał zamyka rachunek w pierwszych trzech minutach, a potem pokazuje, co z tą liczbą zrobić: dlaczego złote na miesiąc, a nie procent; jak czytać decyzję, która wraca sama, bo rezygnacja wygasa i zapis wraca automatycznie w dacie z ustawy; trzy błędy pomiaru, które liczba ujawnia; i co zapisać, żeby rachunek przydał się jeszcze raz, gdy data wróci.

Zastrzeżenie, które liczy się bardziej niż sam rachunek: to nie mówi, czy zostać, czy zrezygnować, i nie liczy korzyści — składka pracodawcy, wpłaty od państwa i to, co urośnie, są poza tym rachunkiem i są realne. Nie jest to doradztwo podatkowe ani inwestycyjne, i nie sprawdza, czy twój pasek jest poprawny.

CAPITULOS
{CAPITULOS}

W komentarzu napisz samą kwotę: złote na miesiąc, realny koszt. Nie pensję, nie pracodawcę. Chcę zobaczyć, jak daleko od siebie wypadają ludzie z podobnym paskiem.

## DISCLOSURE
Narracja i grafika w tym materiale są wygenerowane komputerowo. Scenariusz jest oryginalny, a treść ma charakter informacyjny i nie jest doradztwem podatkowym ani inwestycyjnym.

## HASHTAGS
#ppk #wyplata #pasek

## TAGS
ppk, skladka ppk, realny koszt ppk, pasek wyplaty, kwota do wyplaty, rezygnacja z ppk, ponowny zapis ppk, ile kosztuje ppk, podstawa opodatkowania, skladka pracodawcy, wplaty od panstwa, jak czytac pasek, zlote na miesiac, prog podatkowy, dochod narastajaco

## COMENTARIO FIXADO
Cały rachunek w dwóch linijkach: weź dwa paski — miesiąc ze składką PPK i miesiąc bez (bez premii i wyrównań). Odejmij kwotę do wypłaty jednego od kwoty do wypłaty drugiego. Ta różnica to twój realny koszt na miesiąc, i będzie mniejsza od linii składki. Napisz tutaj samą tę kwotę — nie pensję.

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita a aliquota da contribuicao do empregado nem do empregador, nao cita o valor das wplaty do Estado, nao cita o prazo exato da reinscricao automatica, nao cita progressao de imposto e nao cita nome de instituicao financeira. Os dois numeros da conta sao do proprio espectador: as kwoty do wyplaty de dois paskow dele. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA, e por que: (1) as aliquotas legais do PPK e o calendario exato da reinscricao automatica, porque sao numeros institucionais que eu NAO conferi em duas fontes oficiais dentro desta rodada — e o video nao precisa deles para a conta fechar, porque a subtracao entre dois paskow nao depende de saber a aliquota; o video afirma apenas que a rezygnacja expira e o zapis volta, que e o desenho do programa e nao um numero; (2) qualquer valor de retorno futuro, porque custo e beneficio se contam separados e o beneficio depende de mercado e de anos; (3) qualquer juizo sobre ficar ou sair — o video diz explicitamente que a conta nao decide, so precifica. ESTE EIXO SUBSTITUI O NUMERO INSTITUCIONAL DE PROPOSITO, e a decisao vem do dado deste canal: o MAIOR short do canal (287 views) entregou vinte e uma views de longo, enquanto o MELHOR longo (cento e tres views) veio de um short de vinte e sete — um decimo do alcance e cinco vezes o resultado. E o pior longo do canal entregava constatacao datada sobre o mercado, nao do espectador: o seguro OC esta mais barato em dois anos, seis views de longo.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/kolejny-poziom-015.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-015",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
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
    from ensaio import duracao_estimada, duracao_estimada_short, duracao_cena
    grava(SPEC, "fabrica/specs/kolejny-poziom-015.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
    t, ult = 0.0, None
    for c in CENAS:
        if c.get("cap"):
            if ult:
                print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s")
            ult = (c["cap"], t)
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
    if ult:
        print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s")
    RESIDUO = 0.985   # pl-PL-MarekNeural, -1,5% no ensaio.py, n=409
    t = 0.0
    for i, c in enumerate(CENAS):
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
        if "twój realny koszt PPK na miesiąc" in (c.get("nar") or ""):
            print(f"  a resposta fecha em {t:.1f}s cru -> "
                  f"{t * RESIDUO:.1f}s corrigido (cena {i})")
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: "
                  f"{c['broll_q']}")
