"""kolejny-poziom-018 — rata rowna czy malejaca, medido na kwocie do espectador.

ALAVANCA ATACADA: A (conversao short -> inscrito), pela FORMA, com a forma
tirada do que ESTE canal mediu e nao do que eu acho.

NUMERO DE PARTIDA, do proprio canal, LIDO AO VIVO em 07/10 04:15 pelo
`videos.list` (part=statistics,status) nos 44 ids — nao pelo `metricas`. Por que
ao vivo: a parte 2 da trava do 549 deu o pior delta em -14 views num short de
165 com 128 coletas, e -14 esta na fronteira entre "arredondamento" e "dezenas".
Em vez de decidir na fronteira, reli a fonte. O retrato abaixo e o ao vivo.

    pacote  assunto                       short  longo  travessia
    013     Krotszy czy Dluzszy Kredyt        27    103      381%
    012     Prad stanieje, rachunek rosnie    42     63      150%
    003     IKE czy IKZE                      47     47      100%
    010     Ryczalt: jeden zloty ponad progu  72     64       89%
    011     Prog podatkowy 120 000 zl         68     39       57%
    008     Zdolnosc kredytowa                34     17       50%
    004     Oplaty i podatek Belki            86     27       31%
    006     Obligacje: szesc ofert            172     42       24%
    009     OC najtansze od dwoch lat         69      6        9%
    007     Rata spadla? Nie przestawaj       287     21        7%

O QUE DEU CERTO: os cinco melhores sao TODOS escolha binaria ou paradoxo
resolvido por um numero que a pessoa tem em casa — "krotszy czy dluzszy",
"stanieje mas o rachunek sobe", "IKE czy IKZE", "um zloty acima do limite".

O QUE NAO DEU: fato de mercado e ranking de produto. O 009 ("o seguro mais
barato em dois anos") e o 006 ("seis ofertas, uma perde") deram 9% e 24%, e o
007 teve o SHORT MAIS VISTO DO CANAL — duzentos e oitenta e sete views — com a
PIOR travessia, 7%. O titulo do short do 007 e uma ORDEM ("nao pare de
sobrepagar"), nao uma conta.

O QUE VOU MUDAR: paradoxo aritmetico, do tipo do 012, sobre um numero que esta
escrito na oferta do banco do espectador. E o short NAO leva ordem nenhuma.

PESQUISA DE TENDENCIA (obrigatoria). YouTube
`chart=mostPopular&regionCode=PL&videoCategoryId=26`, quinze itens, status 200 e
`error` ausente. **A 26 e PROXY e eu digo isso:** a categoria real de todos os
canais da frota e a 27 (Education), que nao tem chart em regiao nenhuma
(aprendizado 610).
O feed polones estava com trote, cabeleireiro, squishy, trampolim, drift e jogo
de bar. Zero financas, zero credito.
GRAFEI A FORMA, DESCARTEI O ASSUNTO: "Dlaczego ludzie ciagle przegrywaja w te
gre barowa" (POR QUE AS PESSOAS PERDEM NUMA ESCOLHA QUE PARECE JUSTA) virou o
gancho da cena 1. Nao grafei trote, squishy nem drift.

EIXO, e por que ele e novo. Os quinze pacotes do canal falam de IKE/IKZE,
podatek Belki, placa minimalna, obligacje, nadplata contra inwestowanie,
zdolnosc kredytowa, OC, ryczalt, prog podatkowy, prad, PRAZO do credito, dane
komorkowe, PPK, podatek od nieruchomosci e ulga na dziecko. NENHUM trata do
TIPO DE RATA. O 013 tratou do PRAZO — o que muda e o numero de meses; aqui o
prazo e o mesmo nos dois lados e o que muda e a FORMA da rata. Similaridade
medida contra os dez titulos do canal no corpus: 0,36, teto 0,65.

IDENTIDADE — UMA CORRECAO MINHA, e vai escrita porque e exatamente o buraco do
aprendizado 601. A faixa do canal em SEIS pacotes (012 a 016) e
`ink #1B3A5C / c2 #F5B841 / bg #F4F1EA`. O kolejny-poziom-017, que eu escrevi
na madrugada de hoje, saiu com `#1F2A37 / #B23A48 / #2F6F62 / #F7F3EC` — paleta
que nenhum outro pacote do canal usa. Se eu tivesse copiado "o pacote anterior"
teria repetido o desvio e ele viraria a convencao. Volto a faixa. Trilha
`Wholesome`, unanime nos oito.

VEREDITO DO CANAL: `suspenso` (v_maquina_licoes, dezenove shorts e dezenove
longos medidos, mediana de views/dia do longo 0,55 contra 1,66 do short). Piso
de oito minutos e o melhor material NO SHORT. Pela colisao do aprendizado 602,
SETE capitulos de ~71 s, nao oito.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ESTE VIDEO NAO AFIRMA NADA SOBRE O MUNDO, e por isso nao tem fonte a citar.
#
# O que ele afirma e ARITMETICA, e so ela:
#
#   * na rata malejaca a parte do capital e a mesma todo mes: kwota dividida
#     pela liczba rat. A primeira rata e essa parte MAIS kwota vezes o
#     oprocentowanie mensal;
#   * a soma dos juros da malejaca e oprocentowanie mensal vezes kwota vezes
#     (liczba rat mais um), dividido por dois. Isso sai da soma dos saldos, que
#     e uma progressao aritmetica — nao e regra de banco, e conta de escola;
#   * na rata rowna a soma do que se devolve e liczba rat vezes A RATA QUE O
#     BANCO ESCREVEU NA OFERTA. Essa rata nao se calcula a mao, e nao precisa:
#     ela esta no papel da pessoa.
#
# AS DUAS ENTRADAS SAO DO ESPECTADOR: a kwota, a liczba rat e o oprocentowanie
# estao na oferta dele; a rata rowna tambem. Nao ha numero meu no resultado.
#
# O EXEMPLO DO CAPITULO CINCO E HIPOTETICO E ESTA DITO ASSIM NO PROPRIO VIDEO:
# trzysta tysiecy zlotych, dwadziescia lat, siedem procent. Nao e taxa de
# mercado, nao e oferta de banco nenhum e nao foi medido em lugar nenhum — e um
# numero redondo para a conta ficar visivel. A rata rowna do exemplo entra como
# DADA, do mesmo jeito que entraria do papel.
#
# O QUE FOI DESCARTADO, e o descarte vai escrito porque e a regra da casa:
#   (1) qualquer afirmacao sobre o que os bancos poloneses fazem, oferecem ou
#       preferem — nao tenho fonte e nao vou citar de memoria;
#   (2) qualquer afirmacao sobre o que a MAIORIA das pessoas escolhe: o titulo
#       chegou a ser "porque quase todo mundo escolhe a mais cara" e caiu, por
#       ser afirmacao sobre uma maioria que eu nao medi;
#   (3) o efeito da rata malejaca na zdolnosc kredytowa, que depende do banco e
#       de regulamento, e que eu nao consigo fechar em duas fontes;
#   (4) qualquer taxa, WIBOR, marza ou indice vigente.
#
# E O QUE O VIDEO DIZ QUE A CONTA **NAO** DECIDE, no capitulo seis inteiro: a
# malejaca comeca mais alta, e isso e risco de caixa real no comeco. Quem nao
# aguenta a primeira rata nao esta "escolhendo errado" — esta escolhendo outra
# coisa. O video nao recomenda nenhum dos dois.
#
# =============================================================================
"""

CENAS = []


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


# Links gravados pela busca via `pg_net`, onde a chave do Pexels mora. NENHUM
# repete pacote anterior deste canal: os quatorze ja usados (4297126, 4693665,
# 6615523, 6975457, 7430218, 7490379, 7494652, 7593891, 7735485, 7735903,
# 8293306, 8479056, 8661806, 9057678) foram lidos das specs 015, 016 e 017 antes
# da escolha, nao so do ultimo pacote.
#
# TODOS COM TREZE SEGUNDOS OU MAIS, de proposito: no labtreinamento-011 de hoje
# um clipe de nove segundos saiu "cortado invalido" e a cena foi para o fallback
# de lower-third sobre preto. Cena de ~9,5 s pede ~12,5 s de footage.
BROLL = {
    7732810: ("https://videos.pexels.com/video-files/7732810/7732810-hd_1280_720_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/man-and-woman-reading-a-contract-7732810/"),
    6101321: ("https://videos.pexels.com/video-files/6101321/6101321-hd_1366_720_30fps.mp4",
              "KATRIN BOLOVTSOVA",
              "https://www.pexels.com/video/lawyer-writing-on-a-document-6101321/"),
    7732868: ("https://videos.pexels.com/video-files/7732868/7732868-hd_1280_720_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/people-looking-at-document-7732868/"),
    34596756: ("https://videos.pexels.com/video-files/34596756/14661003_1280_720_25fps.mp4",
               "Jakub Zerdzicki",
               "https://www.pexels.com/video/managing-finances-counting-cash-from-wallet-34596756/"),
    8478946: ("https://videos.pexels.com/video-files/8478946/8478946-hd_1280_720_25fps.mp4",
              "ArtHouse Studio",
              "https://www.pexels.com/video/person-writing-on-paper-8478946/"),
    7735495: ("https://videos.pexels.com/video-files/7735495/7735495-hd_1280_720_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/making-a-presentation-to-a-couple-7735495/"),
    5311423: ("https://videos.pexels.com/video-files/5311423/5311423-hd_1280_720_25fps.mp4",
              "olia danilevich",
              "https://www.pexels.com/video/person-signing-a-documents-5311423/"),
}


def B(kicker, sub, nar, q, pexels_id, cap=None):
    link, autor, pagina = BROLL[pexels_id]
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q, "broll_url": link,
         "broll_credito": {"pexels_id": pexels_id, "autor": autor, "url": pagina}}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub, "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================
# A resposta — os DOIS rachunkos inteiros, com as entradas nomeadas — abre o
# capitulo 2, que a estimativa poe perto dos 71 s e fecha perto dos 142 s. Vou
# medir a FRASE no legendas.srt depois do render, nao a abertura de capitulo
# (aprendizado 537: a abertura erra de +42 a +49 s).

# ---------------------------- 1 -------------------------------------- ~71 s
B("Dwie oferty", "ta sama kwota",
  "Dwie oferty na ten sam kredyt. W jednej miesięczna rata jest niższa, i prawie każdy patrzy właśnie na tę liczbę.",
  "man and woman reading a contract", 7732810, cap="Dwie oferty, ta sama kwota")
T("A ona mówi najmniej", "bo rata to nie koszt",
  "Tylko że rata to nie koszt. Koszt to suma wszystkiego, co oddasz bankowi do ostatniego miesiąca. Rata mówi, ile zapłacisz w tym miesiącu, i ani złotówki więcej.")
T("Dwie liczby", "idą w różne strony",
  "I te dwie liczby nie idą w tę samą stronę: niższa rata na starcie potrafi oznaczać większą sumę na końcu.")
T("Gdzie jest różnica", "nie w negocjacji",
  "Różnica nie siedzi w banku ani w negocjacji. Siedzi w kształcie raty, a ten kształt wybierasz ty przy podpisie.")
T("Dwa kształty", "i oba mają nazwy",
  "Kształty są dwa. Rata równa, taka sama od pierwszego do ostatniego miesiąca, i rata malejąca.")
T("Jak maleje", "i dlaczego właśnie tak",
  "W malejącej każda kolejna rata jest trochę mniejsza, bo odsetki liczy się od tego, co jeszcze zostało do spłaty. Im mniej zostało do oddania, tym mniejsza kolejna rata.")
T("Czego tu nie będzie", "żadnej stawki",
  "Nie usłyszysz tu żadnej stawki, żadnego wskaźnika i żadnej oferty banku. Niczego takiego nie potrzebujemy.")
T("Zaczynamy od rachunków", "bo reszta z nich wynika",
  "Zaczynamy od dwóch rachunków, bo wszystko inne jest tylko ich konsekwencją.")

# ---------------------------- 2 -------------------------------------- ~71 s
B("Dwa rachunki", "jeden krótki, drugi w dwóch krokach",
  "Pierwszy rachunek dotyczy raty równej i jest najkrótszy z możliwych: liczba rat pomnożona przez ratę z twojej oferty.",
  "lawyer writing on a document", 6101321, cap="Dwa rachunki")
T("To cała suma", "a odsetki to resztka",
  "To cała suma, którą oddasz. Odejmij od niej kwotę kredytu i zostają same odsetki. Ta resztka jest tym, ile kredyt rzeczywiście kosztował.")
T("Skąd ta rata", "nie ode mnie",
  "Zwróć uwagę, skąd wzięła się ta rata: ja jej nie policzyłem. Jest napisana na papierze, który już masz.")
T("Drugi rachunek", "najpierw kapitał",
  "Drugi rachunek dotyczy malejącej i ma dwa kroki. Najpierw część kapitałowa: kwota podzielona przez liczbę rat.")
T("Ta część jest stała", "zmieniają się odsetki",
  "Ta część jest stała, co miesiąc dokładnie taka sama. Zmieniają się tylko odsetki, bo maleje to, od czego się je liczy.")
T("Potem oprocentowanie", "miesięczne, nie roczne",
  "Potem miesięczne oprocentowanie: roczne podzielone przez dwanaście. Też z oferty, nie ode mnie. Jeśli w ofercie stoi roczne, dziel; jeśli miesięczne, nie dziel.")
T("I suma odsetek", "trzy mnożenia i dzielenie",
  "Suma odsetek malejącej to miesięczne oprocentowanie razy kwota razy liczba rat plus jeden, podzielone przez dwa.")
T("To nie reguła banku", "to szkolny ciąg",
  "Ten wzór nie jest regułą żadnego banku. Wychodzi z sumy sald, która jest zwykłym ciągiem ze szkoły.")

# ---------------------------- 3 -------------------------------------- ~71 s
B("Gdzie to przeczytać", "wszystko na jednym papierze",
  "Do obu rachunków potrzebujesz trzech liczb, i wszystkie trzy stoją w jednym dokumencie: w ofercie albo w umowie.",
  "people looking at a document", 7732868, cap="Gdzie to przeczytać")
T("Pierwsza liczba", "kwota kredytu",
  "Pierwsza to kwota kredytu. Nie cena mieszkania i nie wkład własny, a dokładnie tyle, ile pożycza bank. Wkład własny został już wpłacony i odsetek nie generuje.")
T("Druga liczba", "miesiące, nie lata",
  "Druga to liczba rat, czyli miesiące. Dwadzieścia lat zapisuje się jako dwieście czterdzieści rat.")
T("Trzecia liczba", "oprocentowanie roczne",
  "Trzecia to oprocentowanie roczne. Szukaj liczby opisanej jako oprocentowanie, nie jako całkowity koszt kredytu.")
T("Te dwie bywają mylone", "a to nie to samo",
  "Bywają mylone, a to nie to samo: całkowity koszt ma już w sobie prowizję i ubezpieczenia, i do wzoru nie wchodzi.")
T("Czwarta liczba", "do porównania, nie do wzoru",
  "I czwarta liczba, która nie wchodzi do wzoru, tylko do porównania: rata równa, wpisana w ofercie. Bez niej nie porównasz drugiej strony rachunku.")
T("Jeśli jest", "zapisz też pierwszą malejącą",
  "Jeśli oferta podaje także pierwszą ratę malejącą, zapisz ją. Sprawdzisz nią własny rachunek.")
T("Masz wszystko", "i nic więcej nie wejdzie",
  "Masz cztery liczby z jednego papieru. Nic więcej nie będzie potrzebne, i nic więcej tu nie wejdzie.")

# ---------------------------- 4 -------------------------------------- ~71 s
B("Pierwsza rata myli", "i myli najbardziej",
  "Teraz rzecz, która myli najbardziej. Pierwsza rata malejąca jest wyższa od równej, i to zawsze, nie czasami.",
  "counting cash from a wallet", 34596756, cap="Dlaczego pierwsza rata myli")
T("Dlaczego wyższa", "wprost ze wzoru",
  "Wychodzi to wprost ze wzoru: część kapitałowa plus odsetki od pełnej kwoty, bo w pierwszym miesiącu nic jeszcze nie spłaciłeś. Odsetki od pełnej kwoty są największe, jakie w ogóle zapłacisz.")
T("Równa jest niższa", "ale nie za darmo",
  "Równa jest w tym miesiącu niższa, bo bank rozłożył kapitał inaczej. Na starcie spłacasz go mniej.")
T("Mniej kapitału", "dłużej większy dług",
  "Mniej kapitału na starcie znaczy, że dłużej zostaje większy dług. A odsetki liczy się właśnie od długu.")
T("Nie ma sprzeczności", "to ta sama rzecz",
  "Dlatego niższa pierwsza rata i wyższa suma odsetek to nie sprzeczność. To ta sama rzecz widziana z dwóch stron.")
T("Na końcu odwrotnie", "ostatnia rata malejąca",
  "Na końcu jest odwrotnie: ostatnia rata malejąca jest znacznie niższa od równej, bo dług już prawie nie istnieje. Pod koniec okresu płacisz już niemal wyłącznie kapitał.")
T("Co właściwie porównujesz", "najgorszy miesiąc z każdym",
  "Patrząc tylko na pierwszą ratę, porównujesz najgorszy miesiąc malejącej z każdym miesiącem równej.")
T("Dlatego suma", "i zaraz ją zobaczysz",
  "Dlatego rachunek z poprzedniego rozdziału patrzy na sumę, a nie na jeden miesiąc. Zobaczmy ją na liczbach.")

# ---------------------------- 5 -------------------------------------- ~71 s
B("Przykład", "liczby wymyślone, i mówię to wprost",
  "Przykład, i mówię to wprost: liczby są wymyślone, żeby rachunek był widoczny. To nie jest żadna oferta.",
  "person writing on paper", 8478946, cap="Przykład na okrągłych liczbach")
T("Trzy dane", "kwota, okres, oprocentowanie",
  "Kwota: trzysta tysięcy złotych. Okres: dwadzieścia lat. Oprocentowanie: siedem procent w roku. Trzy dane, i tyle wystarczy obu rachunkom.")
T("Miesięczne oprocentowanie", "roczne przez dwanaście",
  "Miesięczne oprocentowanie to roczne podzielone przez dwanaście. Wychodzi niecałe sześć dziesiątych procenta.")
T("Część kapitałowa", "stała przez cały okres",
  "Część kapitałowa: trzysta tysięcy podzielone przez dwieście czterdzieści rat daje tysiąc dwieście pięćdziesiąt złotych.")
T("Odsetki pierwszego miesiąca", "od pełnej kwoty",
  "Odsetki pierwszego miesiąca to kwota razy to oprocentowanie, czyli około tysiąca siedmiuset pięćdziesięciu złotych.")
T("Pierwsza rata malejąca", "suma dwóch części",
  "Pierwsza rata malejąca to suma tych dwóch części. Wychodzi około trzech tysięcy złotych. To najwyższa rata w całym harmonogramie, i dalej jest tylko taniej.")
T("Mnożnik sumy", "liczba rat plus jeden przez dwa",
  "Teraz mnożnik: liczba rat plus jeden, podzielone przez dwa. Daje sto dwadzieścia i pół.")
T("Suma odsetek malejącej", "jedno mnożenie",
  "Odsetki pierwszego miesiąca razy sto dwadzieścia i pół to około dwustu dziesięciu tysięcy złotych.")

# ---------------------------- 6 -------------------------------------- ~71 s
B("Druga strona", "rata równa jako dana",
  "Druga strona przykładu. Ratę równą przyjmuję jako daną, tak jak wziąłbyś ją z papieru: dwa tysiące trzysta dwadzieścia pięć złotych.",
  "making a presentation to a couple", 7735495, cap="Druga strona przykładu")
T("Nie liczę jej", "i nie trzeba",
  "Nie liczę jej, bo na kartce się jej nie policzy. I nie trzeba: bank wpisuje ją w ofercie. Wzór na nią wymaga potęgowania, a oferta policzyła go za ciebie.")
T("Suma oddana", "liczba rat razy rata",
  "Suma to liczba rat razy rata, czyli dwieście czterdzieści razy dwa tysiące trzysta dwadzieścia pięć.")
T("Ile to jest", "zanim odejmiemy kwotę",
  "Wychodzi około pięciuset pięćdziesięciu ośmiu tysięcy złotych oddanych do banku. Prawie dwa razy tyle, ile w ogóle pożyczyłeś.")
T("Same odsetki", "po odjęciu kwoty",
  "Odejmij kwotę kredytu i zostają odsetki: blisko dwustu pięćdziesięciu ośmiu tysięcy złotych.")
T("Teraz obok siebie", "dwie sumy odsetek",
  "Postaw to obok malejącej: dwieście dziesięć tysięcy przeciw dwustu pięćdziesięciu ośmiu tysiącom.")
T("Różnica", "przy tej samej kwocie",
  "Różnica w tym przykładzie to blisko pięćdziesiąt tysięcy złotych, przy tej samej kwocie i tym samym okresie.")
T("A co oddałeś w zamian", "to jest cała wymiana",
  "A pierwsza rata malejąca była wyższa o jakieś sześćset siedemdziesiąt pięć złotych. To jest cała ta wymiana. Wyżej na starcie, niżej w sumie, i to jest cała treść wyboru.")

# ---------------------------- 7 -------------------------------------- ~71 s
B("Czego to nie rozstrzyga", "i to jest najważniejsze",
  "I teraz rzecz najważniejsza: ten rachunek nie mówi, co wybrać. Mówi tylko, ile kosztuje każdy z wyborów.",
  "person signing documents", 5311423, cap="Czego ten rachunek nie rozstrzyga")
T("Wyższy start", "to prawdziwe ryzyko",
  "Malejąca startuje wyżej, a wyższy start to prawdziwe ryzyko w domowym budżecie pierwszych lat. Dochód pierwszego roku musi ją unieść co miesiąc, bez wyjątku.")
T("Nie wybiera źle", "wybiera coś innego",
  "Kto nie udźwignie pierwszej raty, nie wybiera źle. Wybiera coś innego: niższy start zamiast niższej sumy.")
T("Czego nie powiem", "bo nie mam źródła",
  "Nie powiem ci też, co robią polskie banki ani co wybiera większość. Nie mam na to źródła i nie będę zgadywał.")
T("Krok pierwszy", "wypisz trzy liczby",
  "Cztery kroki, wszystkie na jednym papierze. Zacznij od wypisania kwoty, liczby rat i oprocentowania.")
T("Krok drugi", "wariant równy",
  "Drugi: pomnóż liczbę rat przez ratę równą z oferty i odejmij kwotę. Masz odsetki wariantu równego.")
T("Krok trzeci", "wariant malejący",
  "Trzeci: policz miesięczne oprocentowanie, pomnóż przez kwotę, a potem przez mnożnik z piątego rozdziału.")
C("Krok czwarty", "i napisz tylko stronę",
  "Czwarty: porównaj obie sumy i obie pierwsze raty. Napisz w komentarzu, która strona wyszła, bez podawania kwot. Ciekawe, u ilu osób wyjdzie inaczej niż w moim przykładzie.")


# =============================== O SHORT =====================================
# `suspenso` manda o MELHOR MATERIAL para o short, e aqui o melhor material e o
# paradoxo com as duas contas. O short NAO leva ordem nenhuma: o pacote 007 deu
# o short mais visto do canal (287 views) com a PIOR travessia (7%), e o titulo
# dele e uma ordem — "nao pare de sobrepagar". Este titula o paradoxo.
SHORT = [
    {"layout": "titulo", "kicker": "Dwie oferty", "sub": "ten sam kredyt",
     "nar": "Dwie oferty na ten sam kredyt. W jednej rata jest niższa, i to ona "
            "mówi najmniej.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Rata to nie koszt", "sub": "koszt to suma",
     "nar": "Bo rata to nie koszt. Koszt to suma wszystkiego, co oddasz do "
            "ostatniego miesiąca.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Wariant równy", "sub": "jedno mnożenie",
     "nar": "Policz: liczba rat razy rata równa z oferty, minus kwota kredytu. "
            "To twoje odsetki.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Wariant malejący", "sub": "i to też z oferty",
     "nar": "W malejącej: miesięczne oprocentowanie razy kwota razy liczba rat "
            "plus jeden, przez dwa.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Niższa rata", "sub": "większa suma",
     "nar": "Niższa pierwsza rata potrafi oznaczać większą sumę. Oba warianty "
            "są policzone w filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Niższa rata", "l2": "większa suma"}

COPY = """# kolejny-poziom-018

## TITULO
Twoja Pierwsza Rata Jest Niższa, a Oddajesz Bankowi Więcej: Policz Oba Warianty na Swojej Kwocie

## TITULO SHORT
Niższa rata, większa suma? Policz oba

## DESCRICAO
Dwie oferty na ten sam kredyt, ta sama kwota i ten sam okres. W jednej miesięczna rata jest niższa — i prawie każdy patrzy właśnie na tę liczbę. Tylko że rata to nie koszt. Koszt to suma wszystkiego, co oddasz bankowi do ostatniego miesiąca, a te dwie liczby nie idą w tę samą stronę: niższa rata na starcie potrafi oznaczać wyraźnie większą sumę na końcu. Różnica nie siedzi w banku ani w negocjacji — siedzi w kształcie raty, a ten kształt wybierasz ty przy podpisie.

Film pokazuje dwa rachunki i oba policzysz na własnej kwocie. Pierwszy, dla raty równej, jest najkrótszy z możliwych: liczba rat pomnożona przez ratę, którą bank wpisał w twojej ofercie; odejmij kwotę kredytu i zostają same odsetki. Zwróć uwagę, skąd bierze się ta rata — nikt jej tu nie liczy, bo na kartce się jej nie policzy, a nie trzeba: jest napisana na papierze, który już masz. Drugi rachunek, dla raty malejącej, ma dwa kroki: część kapitałowa to kwota podzielona przez liczbę rat i jest stała przez cały okres, a suma odsetek to miesięczne oprocentowanie razy kwota razy liczba rat plus jeden, podzielone przez dwa. Ten wzór nie jest regułą żadnego banku — wychodzi z sumy sald, która jest zwykłym ciągiem arytmetycznym ze szkoły.

Cały rozdział idzie na to, co myli najbardziej: pierwsza rata malejąca jest zawsze wyższa od równej, i wynika to wprost ze wzoru, bo w pierwszym miesiącu odsetki liczy się od pełnej kwoty. Rata równa jest wtedy niższa, bo bank rozłożył kapitał inaczej i na starcie spłacasz go mniej — a mniej kapitału na starcie znaczy, że dłużej zostaje większy dług. Dlatego niższa pierwsza rata i wyższa suma odsetek to nie sprzeczność, a ta sama rzecz widziana z dwóch stron. Patrząc tylko na pierwszą ratę, porównujesz najgorszy miesiąc malejącej z każdym miesiącem równej.

Dalej jest przykład na okrągłych liczbach — i mówię w filmie wprost, że są wymyślone, żeby rachunek był widoczny, a nie wzięte z jakiejkolwiek oferty. Na koniec rozdział o tym, czego ten rachunek NIE rozstrzyga: malejąca startuje wyżej, a wyższy start to prawdziwe ryzyko w budżecie pierwszych lat. Kto nie udźwignie pierwszej raty, nie wybiera źle — wybiera coś innego: niższy start zamiast niższej sumy. Film nie poleca żadnego z wariantów i nie mówi, co robią polskie banki ani co wybiera większość, bo na to nie ma tu źródła.

Materiał informacyjny, nie jest doradztwem finansowym ani ofertą.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Oba rachunki są w pierwszych dwóch minutach, więc nie musisz oglądać całości, żeby je mieć. Wariant równy: liczba rat razy rata równa z twojej oferty, minus kwota kredytu — to odsetki. Wariant malejący: miesięczne oprocentowanie, czyli roczne przez dwanaście, razy kwota, razy liczba rat plus jeden podzielone przez dwa. Trzy liczby do obu rachunków są w jednym dokumencie: kwota kredytu, liczba rat i oprocentowanie roczne. Uwaga na pułapkę: oprocentowanie to nie całkowity koszt kredytu, bo ten ma już w sobie prowizję i ubezpieczenia. I rzecz, która myli najbardziej: pierwsza rata malejąca jest wyższa od równej zawsze, nie czasami — to nie znaczy, że malejąca jest droższa. Jeśli policzysz, napisz w komentarzu tylko, która strona wyszła. Bez kwot.

## HASHTAGS
#RataMalejąca #KredytHipoteczny #KolejnyPoziom

## TAGS
rata malejaca, rata rowna, rata annuitetowa, kredyt hipoteczny, suma odsetek, czesc kapitalowa, oprocentowanie roczne, jak policzyc odsetki, pierwsza rata, zdolnosc kredytowa, kolejny poziom, finanse osobiste, kredyt na mieszkanie, porownanie ofert, liczba rat

## CONFIGURACOES DO STUDIO
# NOTA: `categoryId` aqui e DECLARATIVO e o codigo ignora — publicar.py tem 27
# fixo. Escrito 27 porque e o que o video realmente recebe. Aprendizado 610.
privacyStatus: public
defaultLanguage: pl
defaultAudioLanguage: pl
categoryId: 27
madeForKids: false

## MUSICA / LICENCA
{TRILHA}
B-roll: Pexels, creditos por clipe em broll_creditos.json e abaixo.
Mikhail Nilov; KATRIN BOLOVTSOVA; Jakub Zerdzicki; ArtHouse Studio;
olia danilevich.

## AVISO SOBRE OS NUMEROS
ZERO AFIRMACAO SOBRE O MUNDO, e por isso nao ha fonte a citar.

O QUE O VIDEO AFIRMA E ARITMETICA, e so ela:
  * na rata malejaca a parte do capital e a mesma todo mes — kwota dividida
    pela liczba rat — e a primeira rata e essa parte MAIS kwota vezes o
    oprocentowanie mensal;
  * a soma dos juros da malejaca e oprocentowanie mensal vezes kwota vezes
    (liczba rat mais um), dividido por dois. Isso sai da soma dos saldos, que e
    uma progressao aritmetica: conta de escola, nao regra de banco;
  * na rata rowna a soma devolvida e liczba rat vezes A RATA QUE O BANCO
    ESCREVEU NA OFERTA. Essa rata nao se calcula a mao e nao precisa: esta no
    papel da pessoa.

AS ENTRADAS SAO TODAS DO ESPECTADOR: kwota, liczba rat e oprocentowanie estao
na oferta dele, e a rata rowna tambem. Nao ha numero meu no resultado.

O EXEMPLO DO CAPITULO CINCO E HIPOTETICO E O VIDEO DIZ ISSO NA PROPRIA CENA DE
ABERTURA DELE: trzysta tysiecy zlotych, dwadziescia lat, siedem procent. Nao e
taxa de mercado, nao e oferta de banco nenhum, nao foi medido em lugar nenhum —
e numero redondo para a conta ficar visivel. A rata rowna do exemplo entra como
DADA, do mesmo jeito que entraria do papel.

O QUE FOI DESCARTADO, e o descarte vai escrito porque e a regra da casa:
  (1) qualquer afirmacao sobre o que os bancos poloneses fazem, oferecem ou
      preferem — nao tenho fonte e nao cito de memoria;
  (2) qualquer afirmacao sobre o que a MAIORIA escolhe: o titulo chegou a ser
      "porque quase todo mundo escolhe a mais cara" e CAIU, por ser afirmacao
      sobre uma maioria que eu nao medi;
  (3) o efeito da rata malejaca na zdolnosc kredytowa, que depende do banco e
      de regulamento e que eu nao fecho em duas fontes;
  (4) qualquer taxa, indice de referencia, marza ou valor vigente.

E O QUE A CONTA NAO DECIDE esta no capitulo sete inteiro: a malejaca comeca
mais alta, e isso e risco de caixa real nos primeiros anos. Quem nao aguenta a
primeira rata nao esta escolhendo errado — esta escolhendo outra coisa. O video
nao recomenda nenhum dos dois lados.

## FONTES
NENHUMA FONTE NORMATIVA OU ESTATISTICA E CITADA, e isso e deliberado: o video
nao faz afirmacao sobre o mundo. As unicas "fontes" sao os documentos do
proprio espectador — a oferta ou a umowa, de onde saem kwota, liczba rat,
oprocentowanie roczne e a rata rowna.
B-roll: Pexels, licenca Pexels, creditos por clipe em broll_creditos.json.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-018",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    # Faixa do canal em SEIS pacotes (012 a 016). O 017, meu, saiu fora dela.
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada, duracao_estimada_short, duracao_cena
    grava(SPEC, "fabrica/specs/kolejny-poziom-018.json")
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
    t = 0.0
    for i, c in enumerate(CENAS):
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
        if "sumy sald" in (c.get("nar") or ""):
            print(f"  a resposta fecha em {t:.1f}s (cena {i})")
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: "
                  f"{c['broll_q']}")
    import unicodedata
    campos = []
    for c in CENAS + SHORT:
        campos += [c.get("nar", ""), c.get("kicker", ""), c.get("sub", ""), c.get("cap", "")]
    txt = "".join(campos)
    letras = [ch for ch in txt if ch.isalpha()]
    acent = [ch for ch in letras if len(unicodedata.normalize("NFD", ch)) > 1 or ch in "łŁ"]
    print(f"diacriticos: {100*len(acent)/max(len(letras),1):.2f}% "
          f"({len(acent)} de {len(letras)} letras)")
