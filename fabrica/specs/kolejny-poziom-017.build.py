"""kolejny-poziom-017 — o limite de renda existe so para quem tem UM filho.

ALAVANCA ATACADA: A (conversao short -> inscrito), pela FORMA do pacote, e ela
veio de duas leituras que apontam para o mesmo lugar.

NUMERO DE PARTIDA, do proprio canal. A trava do 549 passou nas duas partes:
dezenove longos, todos os deltas da ultima coleta contra o max anterior
POSITIVOS ou zero. O retrato SERVE, nao precisei ler ao vivo.

    longo                                              views   forma
    Krotszy czy Dluzszy Kredyt? Dwa Mnozenia z Twojej    103   escolha binaria
    Ryczalt 2026: Jeden Zloty Ponad Progiem Kosztuje      64   efeito do limiar
    Prad Stanieje w 2026, a Rachunek Urosnie: Policz      63   paradoxo + policz
    Emerytura z ZUS: 34,4% pensji w 2050                  50   projecao
    IKE czy IKZE? Jedna Liczba Rozstrzyga Caly Wybor      47   escolha binaria
    ...
    Ile Placisz za Dane, Ktorych Nie Zuzywasz?            16   panorama
    Jak ulozyc finanse przy sredniej pensji 9233 zl?      11   panorama
    OC najtansze od dwoch lat                              6   noticia

O QUE DEU CERTO: os tres melhores sao ESCOLHA BINARIA ou EFEITO DE LIMIAR, e os
dois primeiros dizem na cara que a conta e do espectador — "duas multiplicacoes
do TEU contrato", "um zloty acima do limite". Os piores sao panorama e noticia.

O QUE NAO DEU: panorama. "Quanto voce paga por dados que nao usa" (16), "como
organizar as financas com o salario medio" (11) e "seguro mais barato em dois
anos" (6) sao os tres piores do canal, e os tres descrevem o mundo em vez de dar
uma conta. Mesmo padrao que o 482 mediu no epomeno.

O QUE VOU MUDAR: juntar as DUAS formas vencedoras num unico pacote. Este tem
efeito de limiar (o teto de renda) E escolha binaria (um filho ou dois), e a
conta que decide e do espectador.

PESQUISA DE TENDENCIA (obrigatoria, feita antes de escrever). YouTube
`chart=mostPopular&regionCode=PL&videoCategoryId=26`, quinze itens, status 200 e
`error` ausente. **A categoria 26 e PROXY e eu digo isso:** a categoria real de
todos os videos da frota e a 27 (Education), que nao tem chart em nenhuma regiao
(aprendizado 610).
O feed polones estava com Zabka, cabeleireiro, trampolim, squishy, cartas e
namorado. Zero financas.
GRAFEI A FORMA, DESCARTEI O ASSUNTO:
  * "Dlaczego ludzie ciagle przegrywaja w te gre barowa" — POR QUE QUASE TODOS
    PERDEM EM X. Virou o eixo: por que tanta gente com um filho perde a ulga.
  * "Ktora zabawka najlepsza dla..." — escolha entre opcoes. Virou a estrutura
    do capitulo tres, um filho contra dois.
Nao grafei Zabka, squishy nem cabeleireiro.

EIXO, e por que ele e novo. Os dezesseis pacotes falam de credito, ryczalt,
prad, emerytura ZUS, IKE/IKZE, obrigacoes do tesouro, o limiar de 120.000,
imposto Belka, amortizar ou investir, capacidade de credito, salario minimo,
dados moveis, salario medio, seguro de carro, PPK e imposto predial. NENHUM fala
de ulga prorodzinna, e nenhum tem a estrutura "o limite existe so para um
subgrupo".

VEREDITO DO CANAL: `suspenso` (v_maquina_licoes, dezenove shorts e dezenove
longos medidos). Piso de oito minutos e o melhor material NO SHORT.

A ESCOLHA DE SETE CAPITULOS: aprendizado 602. Oito capitulos de 64,2 s somam
513,6 s e com margem passam de 550, o que afasta do piso em vez de chegar nele.
Sete de aproximadamente 70 s dao ~490 s, acima do piso de 480 e perto dele.
Nenhum portao foi afrouxado para isso.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# DUAS FONTES INSTITUCIONAIS, e elas sao exatamente o padrao "orgao que aplica +
# publicador do texto". Todos os numeros abaixo batem nas DUAS:
#
#   * PUBLICADOR DO TEXTO: Sejm, API ELI. Ustawa o podatku dochodowym od osob
#     fizycznych, art. 27f. Texto CONSOLIDADO vigente: Dz.U. 2026 poz. 592,
#     obwieszczenie Marszalka Sejmu de 17/04/2026, status `obowiazujacy`.
#   * ORGAO QUE APLICA: Ministerio das Financas, podatki.gov.pl, pagina
#     /ulgi-i-odliczenia/ulga-na-dziecko-pit (200, 24.182 chars de texto).
#
# O QUE BATEU NAS DUAS:
#   92,67 zl/mes no primeiro e no segundo filho (1.112,04 zl/ano cada)
#   166,67 zl/mes no terceiro (2.000,04 zl/ano)
#   225,00 zl/mes no quarto e nos seguintes (2.700,00 zl/ano)
#   teto de 112.000 zl para quem e casado o ano inteiro, somando os conjuges
#   teto de 56.000 zl para quem nao e casado
#   os tetos NAO se aplicam com dois filhos ou mais (art. 27f ust. 2 pkt 2 e 3)
#   os tetos NAO se aplicam a filho unico com deficiencia (ust. 2e)
#   `dochody` sao a renda MENOS as contribuicoes sociais (ust. 2a)
#   a quantia e dos dois pais juntos, em qualquer proporcao que acordarem; sem
#   acordo e com guarda alternada, em partes iguais (ust. 4)
#
# UM DETALHE QUE SO O ORGAO TRAZ, e por isso o par importa: no regime linear
# tambem se descontam as contribuicoes de SAUDE do valor que se compara com o
# teto. A lei remete ao art. 30c; o podatki.gov.pl diz com todas as letras.
#
# NADA FOI DESCARTADO por falta de fonte nesta rodada. O que foi descartado foi
# o CANAL anterior da fila: o epomeno-epipedo era o mais antigo (06/10 19:52) e
# o dado dele pedia um eixo de imposto ou beneficio, mas para a Grecia esse eixo
# NAO TEM FONTE: aade.gr 403, gsis.gr 403, efka.gov.gr e et.gr renderizados por
# JavaScript, minfin.gr 202, oecd.org 403 Cloudflare, e as paginas fiscais da
# Comissao Europeia sao SPA. So indice de preco abre na Grecia (ELSTAT e
# Eurostat), e o pacote 015 ja usou esse eixo. Entao segui a ordem da fila para
# o proximo, que e este canal, onde a API ELI do Sejm abre o pais inteiro.
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


# Links gravados na spec pela busca via `pg_net` dentro do banco, onde a chave do
# Pexels mora. Nenhum destes aparece no kolejny-011, no 016 nem no
# resep-naik-level-012 — clipe repetido em pacotes seguidos fica obvio.
BROLL = {
    # Mae ensinando a filha na licao de casa. O capitulo abre falando de pais
    # com UM filho, e o clipe e exatamente um adulto com uma crianca.
    4297126: ("https://videos.pexels.com/video-files/4297126/4297126-hd_1920_1080_25fps.mp4",
              "August de Richelieu",
              "https://www.pexels.com/video/mother-teaching-her-daughter-on-her-homework-4297126/"),
    # Calculadora de perto. O capitulo e A CONTA, e e so isso que ele e.
    7593891: ("https://videos.pexels.com/video-files/7593891/7593891-hd_1920_1080_25fps.mp4",
              "Pavel Danilyuk",
              "https://www.pexels.com/video/close-up-video-of-a-person-using-calculator-7593891/"),
    # DUAS criancas juntas. O capitulo diz que com dois filhos o teto desaparece;
    # o clipe mostra dois, nao um, e a diferenca e o assunto do capitulo.
    7494652: ("https://videos.pexels.com/video-files/7494652/7494652-hd_1280_720_30fps.mp4",
              "Artem Podrez",
              "https://www.pexels.com/video/two-children-reading-a-book-together-7494652/"),
    # Alguem CIRCULANDO um valor. O capitulo lista as quantias por filho.
    8479056: ("https://videos.pexels.com/video-files/8479056/8479056-hd_1920_1080_25fps.mp4",
              "ArtHouse Studio",
              "https://www.pexels.com/video/encircle-a-value-8479056/"),
    # Dedo apontando um trecho de documento. O capitulo e a EXCECAO do ust. 2e —
    # um paragrafo especifico que desliga o teto.
    7735485: ("https://videos.pexels.com/video-files/7735485/7735485-hd_1920_1080_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/a-person-pointing-on-a-document-7735485/"),
    # Casal conversando sobre papel. O capitulo e o acordo entre os dois pais
    # sobre a proporcao, e o clipe e duas pessoas decidindo juntas.
    6975457: ("https://videos.pexels.com/video-files/6975457/6975457-hd_1366_720_25fps.mp4",
              "T Leish",
              "https://www.pexels.com/video/a-couple-talking-while-reading-newspaper-and-answering-sudoku-6975457/"),
    # Homem preenchendo formulario. O ultimo capitulo termina na declaracao.
    8293306: ("https://videos.pexels.com/video-files/8293306/8293306-hd_1280_720_30fps.mp4",
              "RDNE Stock project",
              "https://www.pexels.com/video/a-man-filling-out-a-form-8293306/"),
}


def B(kicker, sub, nar, q, pexels_id, cap=None):
    link, autor, pagina = BROLL[pexels_id]
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q, "broll_url": link,
         "broll_credito": {"pexels_id": pexels_id, "autor": autor,
                           "url": pagina}}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================
# A resposta concreta — as duas entradas da conta nomeadas, e o aviso de que a
# segunda nao e o salario bruto — esta na abertura do capitulo 2, que a
# estimativa poe perto dos 70 s. O aprendizado 604 diz, com cinco pontos, que a
# estimativa erra para MAIS, ou seja no video pronto ela chega ANTES. Vou medir
# buscando a FRASE no legendas.srt depois do render.
#
# TUDO ABAIXO ESTA ACENTUADO. A primeira versao que eu escrevi tinha 0,0% de
# diacriticos e o portao `ortografia` a reprovou contra os 6,9% da faixa do
# canal — em polones isso nao e cosmetico, muda a pronuncia do TTS. E o mesmo
# buraco do aprendizado 597, que deixou labtreinamento-002 e 003 no ar com
# pronuncia errada.

# ---------------------------- 1 -------------------------------------- ~71 s
B("Limit tylko dla jednych", "nie dla wszystkich rodziców",
  "W uldze na dziecko istnieje limit dochodu, ale on nie dotyczy wszystkich rodziców. Dotyczy tylko części z nich, i to bardzo konkretnej części.",
  "mother helping daughter with homework", 4297126, cap="Limit tylko dla jednych")
T("Liczba dzieci decyduje", "czy limit cię dotyczy",
  "To jedna z niewielu ulg w polskim systemie, w której liczba twoich dzieci decyduje nie o wysokości kwoty, a o tym, czy limit dochodu w ogóle ma do ciebie zastosowanie.")
T("Przy jednym jest", "przy dwojgu go nie ma",
  "Przy jednym dziecku limit istnieje i trzeba go sprawdzić. Przy dwojgu dzieci i więcej nie ma go wcale, niezależnie od tego, ile zarabiasz.")
T("Ten sam dochód", "inne rozstrzygnięcie",
  "Dlatego dwie rodziny z dokładnie tym samym dochodem mogą dostać zupełnie inne rozstrzygnięcie, a cała różnica to liczba dzieci.")
T("Dlaczego tylu traci", "mimo że byli blisko",
  "I dlatego wielu rodziców z jednym dzieckiem rezygnuje z ulgi, nie sprawdzając jej, chociaż mieścili się w limicie.")
T("Bo liczba do porównania", "to nie pensja brutto",
  "Bo liczba, którą porównuje się z limitem, to nie jest twoja pensja brutto. I to jest najczęściej popełniany błąd w tej uldze.")
T("Na koniec policzysz", "swoją własną liczbę",
  "Na koniec tego filmu policzysz swoją własną liczbę i sam zobaczysz, po której stronie limitu stoisz w tym roku.")
T("Bez aplikacji", "dwie rzeczy, które masz",
  "Bez aplikacji i bez zgadywania. Potrzebujesz dwóch rzeczy, które już masz w domu albo w systemie urzędu.")

# ---------------------------- 2 -------------------------------------- ~68 s
B("Twoje dwie liczby", "i jedno odjęcie",
  "Oto rachunek. Bierzesz swój dochód z roku, odejmujesz od niego zapłacone składki na ubezpieczenie społeczne, i to co zostaje porównujesz z limitem.",
  "close up of a person using a calculator", 7593891, cap="Twoje dwie liczby")
T("Pierwsza liczba", "dochód, nie przychód",
  "Pierwsza liczba to dochód za cały rok podatkowy, a nie przychód i nie kwota netto, którą widzisz na pasku wypłaty co miesiąc. Przepis mówi o dochodzie.")
T("Druga liczba", "składki społeczne",
  "Druga liczba to suma składek na ubezpieczenie społeczne, które zapłaciłaś albo zapłaciłeś w tym samym roku podatkowym.")
T("Limit przy małżeństwie", "liczy się oboje razem",
  "Jeśli jesteś w związku małżeńskim przez cały rok, limit wynosi sto dwanaście tysięcy złotych i liczy się wasze dochody razem.")
T("Limit bez małżeństwa", "połowa tej kwoty",
  "Jeśli nie jesteś w związku małżeńskim, limit wynosi pięćdziesiąt sześć tysięcy złotych i liczy tylko twój własny dochód.")
T("Samotny rodzic", "ma wyższy limit",
  "Z jednym wyjątkiem: rodzic samotnie wychowujący dziecko stosuje ten wyższy limit, mimo że nie jest w związku małżeńskim.")
T("Dlaczego brutto myli", "składki to realna kwota",
  "Składki społeczne potrafią zdjąć z tej liczby kilka tysięcy złotych, więc ktoś kto patrzy na brutto może uznać się za przekroczonego bez powodu.")
T("Działalność liniowa", "jeszcze składki zdrowotne",
  "A przy działalności opodatkowanej liniowo odejmujesz dodatkowo składki zdrowotne, które odliczasz od dochodu.")

# ---------------------------- 3 -------------------------------------- ~72 s
B("Przy dwojgu limit znika", "i to nie jest błąd",
  "Przy dwojgu dzieci i więcej limit dochodu nie obowiązuje wcale. To nie jest luka ani błąd w przepisie, to sama konstrukcja ulgi.",
  "two children reading a book together", 7494652, cap="Przy dwojgu limit znika")
T("Co to oznacza", "zarobki przestają mieć znaczenie",
  "Oznacza to, że rodzic dwojga dzieci odlicza ulgę bez względu na to, ile zarobił w roku podatkowym, choć kwota jest ta sama.")
T("Rodzina z jednym", "ta sama kwota, ale z warunkiem",
  "Rodzina z jednym dzieckiem odlicza dokładnie tyle samo na to dziecko, ale tylko wtedy, gdy zmieści się w limicie dochodu.")
T("Dlatego porównanie", "nie dotyczy kwoty",
  "Dlatego porównanie dwóch rodzin nie dotyczy wysokości ulgi. Dotyczy tego, czy trzeba w ogóle sprawdzać dochód.")
T("Warunek przy dwojgu", "jeden dzień wystarczy",
  "Przy dwojgu jest własny warunek, ale łagodny: wystarczy, że przez co najmniej jeden dzień roku sprawowałaś opiekę nad więcej niż jednym dzieckiem.")
T("Kiedy ulga się urywa", "dwie sytuacje",
  "Ulga urywa się od miesiąca, w którym dziecko trafia do instytucji całodobowej na mocy orzeczenia sądu albo wstępuje w związek małżeński.")
T("Dzieci pełnoletnie", "osobne przepisy",
  "Dla dzieci pełnoletnich przepisy stosuje się odpowiednio, gdy utrzymujesz je w związku z ciążącym na tobie obowiązkiem alimentacyjnym albo w związku ze sprawowaniem funkcji rodziny zastępczej.")
T("Wniosek z tej części", "sprawdź, ile masz dzieci",
  "Wniosek jest prosty i warto go zapamiętać: najpierw policz dzieci, a dopiero potem dochód. Odwrotna kolejność traci czas.")

# ---------------------------- 4 -------------------------------------- ~70 s
B("Ile dokładnie odliczasz", "kwoty za każdy miesiąc",
  "Teraz kwoty. Odliczenie liczy się za każdy miesiąc kalendarzowy, w którym sprawowałaś albo sprawowałeś opiekę nad dzieckiem.",
  "a person encircling a value on paper", 8479056, cap="Ile dokładnie odliczasz")
T("Pierwsze i drugie", "ta sama kwota",
  "Na pierwsze dziecko i na drugie dziecko kwota jest ta sama: dziewięćdziesiąt dwa złote i sześćdziesiąt siedem groszy miesięcznie.")
T("Rocznie", "na każde z nich",
  "Rocznie wychodzi z tego tysiąc sto dwanaście złotych i cztery grosze na każde z tych dzieci, jeśli opieka trwała cały rok.")
T("Trzecie dziecko", "wyraźnie więcej",
  "Na trzecie dziecko kwota rośnie do stu sześćdziesięciu sześciu złotych i sześćdziesięciu siedmiu groszy miesięcznie.")
T("Czwarte i kolejne", "najwyższa stawka",
  "Na czwarte dziecko i na każde następne kwota wynosi dwieście dwadzieścia pięć złotych miesięcznie, czyli dwa tysiące siedemset rocznie.")
T("Przykład z trójką", "pierwsze i drugie",
  "Weźmy trójkę dzieci. Na pierwsze i na drugie liczysz po tysiąc sto dwanaście złotych i cztery grosze.")
T("I trzecie", "jedna liczba do zapamiętania",
  "Na trzecie dochodzi dwa tysiące złotych i cztery grosze. Razem daje to cztery tysiące dwieście dwadzieścia cztery złote i dwanaście groszy.")
T("Od podatku", "nie od dochodu",
  "I tyle odejmujesz od podatku, nie od dochodu. Ta różnica jest ważna, bo ulga od podatku działa mocniej niż ta sama kwota od dochodu.")

# ---------------------------- 5 -------------------------------------- ~68 s
B("Wyjątek, który znosi limit", "jeden ustęp przepisu",
  "Jest jeden ustęp, który znosi limit dochodu nawet przy jednym dziecku, i wielu rodziców o nim nie wie.",
  "a person pointing at a line in a document", 7735485, cap="Wyjątek, który znosi limit")
T("Kogo dotyczy", "dziecko z orzeczeniem",
  "Dotyczy rodziców jednego dziecka, które ma orzeczenie o zakwalifikowaniu przez organy orzekające do jednego z trzech stopni niepełnosprawności. Wystarczy jedno z tych orzeczeń.")
T("Albo decyzja rentowa", "trzy rodzaje renty",
  "Albo decyzję przyznającą rentę z tytułu niezdolności do pracy, rentę szkoleniową albo rentę socjalną.")
T("Albo młodsze dziecko", "orzeczenie do szesnastu lat",
  "Albo orzeczenie o niepełnosprawności dziecka, które nie ukończyło szesnastego roku życia, bo dla najmłodszych dzieci orzeczenie wydaje się w innej formie niż stopień.")
T("Co się wtedy dzieje", "limit przestaje istnieć",
  "W każdym z tych przypadków limit dochodu po prostu przestaje cię dotyczyć, dokładnie tak, jakbyś rozliczał ulgę na dwoje dzieci, choć masz jedno.")
T("Dlaczego to ważne", "najczęściej pomijany warunek",
  "To najczęściej pomijany warunek całej ulgi, bo rodzic sprawdza dochód, widzi przekroczenie i kończy sprawdzanie w tym miejscu.")
T("Kolejność sprawdzania", "najpierw orzeczenie",
  "Dlatego kolejność ma znaczenie: najpierw sprawdź orzeczenie, potem liczbę dzieci, a dochód na samym końcu.")
T("Dokumenty", "urząd może poprosić",
  "Urząd może poprosić o dokumenty: odpis aktu urodzenia, zaświadczenie sądu o opiekunie albo zaświadczenie o nauce dziecka pełnoletniego.")

# ---------------------------- 6 -------------------------------------- ~72 s
B("Dwoje rodziców", "jedna kwota do podziału",
  "Ulga należy do obojga rodziców razem, nie do każdego osobno. Jest jedna kwota na dziecko i trzeba ją między sobą podzielić. Za osobę w związku małżeńskim nie uważa się przy tym kogoś po orzeczonej separacji.",
  "a couple talking over a paper together", 6975457, cap="Dwoje rodziców, jedna kwota")
T("Dowolna proporcja", "jeśli się dogadacie",
  "Jeśli się dogadacie, możecie podzielić tę kwotę w dowolnej proporcji, jaką sami ustalicie między sobą.")
T("Całe sto procent", "dla jednego z was",
  "Możecie też ustalić, że cała kwota trafia do jednego z was, i to jest zupełnie dopuszczalne. Przepis nie narzuca tu żadnej proporcji.")
T("Bez porozumienia", "przy pieczy naprzemiennej",
  "Bez porozumienia przepis decyduje za was. Przy pieczy naprzemiennej po rozwodzie kwotę dzieli się w częściach równych.")
T("Ten sam adres", "też po połowie",
  "Tak samo po połowie, gdy miejsce zamieszkania dziecka jest takie samo jak miejsce zamieszkania obojga rodziców.")
T("W pozostałych", "sto procent u jednego",
  "W pozostałych przypadkach całe odliczenie stosuje ten rodzic, u którego dziecko ma miejsce zamieszkania.")
T("Ten sam miesiąc", "liczy się na dni",
  "Gdy w tym samym miesiącu opiekę sprawują oboje, każdy odlicza jedną trzydziestą kwoty miesięcznej za każdy dzień, w którym sprawował pieczę nad dzieckiem.")
T("Dlatego warto ustalić", "zanim złożycie zeznania",
  "Dlatego warto ustalić podział zanim oboje złożycie zeznania, bo poprawianie tego potem jest znacznie bardziej żmudne.")

# ---------------------------- 7 -------------------------------------- ~69 s
B("Cztery kroki", "do zrobienia w tym tygodniu",
  "Cztery kroki, i wszystkie możesz zrobić w tym tygodniu, zanim zasiądziesz do rozliczenia za ten rok podatkowy.",
  "a person filling out a form", 8293306, cap="Cztery kroki")
T("Jeden", "policz dzieci",
  "Pierwszy: policz dzieci, nad którymi sprawowałeś opiekę w roku. Przy dwojgu i więcej limit dochodu cię nie dotyczy.")
T("Dwa", "sprawdź orzeczenie",
  "Drugi: przy jednym dziecku sprawdź, czy ma orzeczenie albo decyzję rentową. Jeśli ma, limit również cię nie dotyczy.")
T("Trzy", "dochód minus składki",
  "Trzeci: dopiero teraz weź swój dochód roczny, odejmij zapłacone składki społeczne i porównaj wynik z limitem.")
T("Cztery", "ustal podział z drugim rodzicem",
  "Czwarty: ustal z drugim rodzicem, w jakiej proporcji dzielicie kwotę, i zapiszcie to, zanim złożycie zeznania.")
T("W zeznaniu", "liczba dzieci i PESEL",
  "W samym zeznaniu podajesz liczbę dzieci i ich numery PESEL, a gdy ich nie ma, imiona, nazwiska i daty urodzenia dzieci.")
T("Jeszcze jedna rzecz", "gdy ulga przewyższa podatek",
  "I ostatnia rzecz, warta zapamiętania: gdy ulga jest wyższa od twojego podatku, różnicę możesz dostać, ale nie więcej niż suma twoich składek.")
C("Napisz swój wynik", "ile dzieci i która strona",
  "Ten film nie jest poradą podatkową. Jeśli policzysz swoją liczbę, napisz w komentarzu ile masz dzieci i po której stronie limitu wyszedłeś.")

# =============================== O SHORT =====================================
# `suspenso` manda O MELHOR MATERIAL NO SHORT, entao o short entrega a regra
# inteira: que o limite so existe com um filho, e as duas entradas da conta. O
# gancho dos dois primeiros segundos grafa "Dlaczego ludzie ciagle przegrywaja",
# que estava no feed de tendencia de hoje.
SHORT = [
    {"layout": "titulo", "kicker": "Dlaczego tylu traci", "sub": "ulgę na jedno dziecko",
     "sem_cap": True,
     "nar": "Dlaczego tyle osób traci ulgę na jedno dziecko? Bo sprawdzają złą liczbę."},
    {"layout": "titulo", "kicker": "Limit tylko przy jednym", "sub": "przy dwojgu go nie ma",
     "sem_cap": True,
     "nar": "Limit dochodu istnieje tylko przy jednym dziecku. Przy dwojgu nie ma go wcale."},
    {"layout": "titulo", "kicker": "Nie brutto", "sub": "dochód minus składki",
     "sem_cap": True,
     "nar": "I porównuje się nie pensję brutto, a dochód po odjęciu składek społecznych."},
    {"layout": "titulo", "kicker": "Dwa limity", "sub": "zależnie od małżeństwa",
     "sem_cap": True,
     "nar": "Sto dwanaście tysięcy w małżeństwie, pięćdziesiąt sześć tysięcy bez niego."},
    {"layout": "cta", "kicker": "Policz dzisiaj", "sub": "najpierw dzieci, potem dochód",
     "sem_cap": True,
     "nar": "Policz najpierw dzieci, a dochód na końcu. Cały rachunek jest w dłuższym filmie."},
]

# Chave `l1`/`l2`, convencao do canal em SEIS pacotes seguidos (011 a 016).
THUMB = {"l1": "Limit?", "l2": "tylko przy jednym"}

# A COPY segue a FAIXA HISTORICA, nao o pacote anterior. Aprendizado 601, setima
# confirmacao: `## CAPITULOS` esta em 011, 012, 013 e 014 e DESAPARECEU no 015 e
# no 016 — e os dois sao meus. O 015 tambem dropou `#KolejnyPoziom`. Aqui a
# secao CAPITULOS volta, a hashtag do canal volta, e `## TITULO SHORT` entra
# porque a rotina passou a exigi-la (548).
COPY = """# kolejny-poziom-017

## TITULO
Ulga na Dziecko: Limit Dochodu Istnieje Tylko przy Jednym — Policz Swoją Liczbę

## TITULO SHORT
Limit tylko przy jednym dziecku

## DESCRICAO
W uldze prorodzinnej istnieje limit dochodu, ale nie dotyczy on wszystkich
rodziców. Dotyczy tylko tych, którzy rozliczają ulgę na jedno dziecko. Przy
dwojgu dzieci i więcej limit nie obowiązuje wcale, niezależnie od wysokości
zarobków. Dlatego dwie rodziny z tym samym dochodem mogą dostać zupełnie inne
rozstrzygnięcie, a cała różnica to liczba dzieci.

Drugi powód, dla którego wielu rodziców rezygnuje z ulgi bez potrzeby: liczba,
którą porównuje się z limitem, to nie pensja brutto. To dochód roczny pomniejszony
o zapłacone składki na ubezpieczenie społeczne, a przy działalności opodatkowanej
liniowo dodatkowo o składki zdrowotne odliczane od dochodu. Składki potrafią zdjąć
z tej liczby kilka tysięcy złotych, więc ktoś kto patrzy na brutto może uznać się
za przekroczonego bez powodu.

Film pokazuje też wyjątek, który znosi limit nawet przy jednym dziecku: orzeczenie
o stopniu niepełnosprawności, decyzja przyznająca rentę z tytułu niezdolności do
pracy, rentę szkoleniową albo socjalną, albo orzeczenie o niepełnosprawności
dziecka poniżej szesnastego roku życia. To najczęściej pomijany warunek całej ulgi.

Dalej: dokładne kwoty na pierwsze, drugie, trzecie oraz czwarte i każde kolejne
dziecko, w ujęciu miesięcznym i rocznym; zasada, że kwota należy do obojga rodziców
razem i można ją podzielić w dowolnej proporcji; co dzieje się bez porozumienia przy
pieczy naprzemiennej; oraz cztery kroki do wykonania przed złożeniem zeznania.

Kolejność, która oszczędza czas: najpierw policz dzieci, potem sprawdź orzeczenie,
a dochód zostaw na sam koniec.

Ten film nie jest poradą podatkową i nie zna Twojej sytuacji.

## CAPITULOS
0:00 Limit tylko dla jednych
1:11 Twoje dwie liczby
2:19 Przy dwojgu limit znika
3:31 Ile dokładnie odliczasz
4:41 Wyjątek, który znosi limit
5:49 Dwoje rodziców, jedna kwota
7:01 Cztery kroki

## COMENTARIO FIXADO
Rachunek jest w pierwszej minucie, więc nie musisz oglądać do końca, żeby go
dostać: dochód roczny minus zapłacone składki społeczne, i dopiero ten wynik
porównujesz z limitem. A limit sprawdzasz tylko wtedy, gdy rozliczasz ulgę na
JEDNO dziecko. Jeśli policzysz swoją liczbę, napisz w komentarzu ile masz dzieci
i po której stronie limitu wyszedłeś — bez kwot, sama strona wystarczy.

## HASHTAGS
#UlgaNaDziecko #PodatkiPL #KolejnyPoziom

## TAGS
ulga na dziecko, ulga prorodzinna, limit dochodu ulga, pit ulga na dzieci, art 27f, rozliczenie pit, podatki polska, ulga na jedno dziecko, dochod minus skladki, odliczenie od podatku, finanse osobiste, kolejny poziom, pit 2026, podzial ulgi miedzy rodzicow, piecza naprzemienna ulga

## CONFIGURACOES DO STUDIO
# NOTA: `categoryId` aqui e DECLARATIVO e o codigo ignora — publicar.py tem 27
# fixo. Escrito 27 porque e o que o video realmente recebe. Aprendizado 610.
privacyStatus: public
defaultLanguage: pl
defaultAudioLanguage: pl
categoryId: 27
madeForKids: false

## MUSICA / LICENCA
Wholesome — Kevin MacLeod (incompetech.com), CC BY 3.0.
B-roll: Pexels, creditos por clipe em broll_creditos.json e abaixo.
August de Richelieu; Pavel Danilyuk; Artem Podrez; ArtHouse Studio;
Mikhail Nilov; T Leish; RDNE Stock project.

## AVISO SOBRE OS NUMEROS
Wszystkie kwoty i limity w tym filmie pochodzą z DWÓCH źródeł instytucjonalnych
i zgadzają się w obu:

1. SEJM, API ELI — ustawa o podatku dochodowym od osób fizycznych, art. 27f,
   tekst JEDNOLITY obowiązujący: Dz.U. 2026 poz. 592, obwieszczenie Marszałka
   Sejmu z dnia 17 kwietnia 2026 r.
2. MINISTERSTWO FINANSÓW — podatki.gov.pl, strona
   /ulgi-i-odliczenia/ulga-na-dziecko-pit.

Zgodne w obu źródłach: 92,67 zł miesięcznie na pierwsze i drugie dziecko
(1112,04 zł rocznie), 166,67 zł na trzecie (2000,04 zł rocznie), 225,00 zł na
czwarte i każde kolejne (2700,00 zł rocznie); limit 112 000 zł dla osoby
pozostającej w związku małżeńskim przez cały rok, liczony łącznie z małżonkiem;
limit 56 000 zł dla osoby niepozostającej w związku małżeńskim; brak limitu przy
dwojgu dzieci i więcej; brak limitu przy jednym dziecku z orzeczeniem; dochód
pomniejszany o składki społeczne.

Szczegół, który podaje tylko strona Ministerstwa: przy działalności opodatkowanej
podatkiem liniowym odejmuje się dodatkowo składki zdrowotne odliczane od dochodu.
Ustawa odsyła w tym miejscu do art. 30c.

Nic nie zostało odrzucone z braku źródła w tym odcinku.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-017",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1F2A37", "c1": "#B23A48", "c2": "#2F6F62", "bg": "#F7F3EC"},
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
    import ensaio
    grava(SPEC, "fabrica/specs/kolejny-poziom-017.json")
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
        t += duracao_cena(c.get("nar", ""), SPEC["voz"]) + ensaio.GAP_CENA_S
    if ult:
        print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s")
