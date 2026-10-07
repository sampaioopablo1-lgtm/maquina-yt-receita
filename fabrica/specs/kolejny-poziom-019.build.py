"""kolejny-poziom-019 — aluguel contra a parte de JUROS, nao contra a parcela inteira.

ALAVANCA ATACADA: A (conversao short -> inscrito), pela FORMA. Mas o numero que
manda esta rodada e outro, e e desconfortavel.

NUMERO DE PARTIDA, lido AO VIVO em 07/10 08:12 pelo `videos.list` nos 46 ids.
Vigilancia do teto 7 na mesma chamada: 105/105 vivos nos tres canais.

    pacote  short            longo   obs
    017        907 views        0     publicado ha ~6,5 h
    016        277 views        0     publicado ha ~1,3 dia
    015        108 views        1     publicado ha ~1,9 dia
    018         18 views        0     publicado ha ~3,5 h

O QUE DEU CERTO: o short do 017 saltou de 372 para 907 views em QUATRO HORAS. E
o segundo maior short da historia do canal e o alcance de short esta melhor do
que nunca.

O QUE NAO DEU, e e o ponto: os longos desses mesmos quatro pacotes estao em 0,
0, 1 e 0. **E eu NAO vou concluir disso que a travessia morreu**, porque a
regra da casa e nao concluir desempenho com menos de 48 h e nenhum dos quatro
fechou essa janela — o 015 esta em 45,6 h, quase. O que da para dizer com o
dado que existe: o alcance do short nao esta comprando longo NESTES quatro, e
se o 015 continuar em um view quando passar de 48 h, isso vira medicao.

O QUE VOU MUDAR: os quatro melhores longos historicos do canal (103, 64, 63,
47) sao todos escolha binaria resolvida por um numero do papel do espectador.
Mantenho a forma e troco o eixo — e desta vez escolhi a pergunta binaria MAIS
pesada que existe em financas pessoais na Polonia, porque pergunta grande puxa
longo melhor que pergunta pequena.

PESQUISA DE TENDENCIA (obrigatoria), e com uma observacao que vale registrar.
YouTube `chart=mostPopular&regionCode=PL&videoCategoryId=26`, quinze itens,
status 200 e `error` ausente. **A 26 e PROXY e eu digo isso** (aprendizado 610).
**CATORZE DOS QUINZE ITENS SAO OS MESMOS DA LEITURA DAS 04:09, quatro horas
antes.** O chart da regiao se move devagar, entao reler a mesma regiao na mesma
manha nao traz informacao nova — digo isso em vez de fingir grafagem nova.
O unico item novo e "Ktora zabawka najlepsza dla Podatniczki Juniorki?" — QUAL
DESTES E MELHOR PARA O SEU CASO. Grafei essa forma: a resposta depende dos
numeros de quem assiste, e o video nao escolhe por ele. Nao grafei o assunto
(brinquedo, trote, squishy, drift).

EIXO, e por que ele e novo. Os dezesseis pacotes falam de IKE/IKZE, podatek
Belki, placa minimalna, obligacje, nadplata contra inwestowanie, zdolnosc
kredytowa, OC, ryczalt, prog podatkowy, prad, prazo do credito, dane komorkowe,
PPK, podatek od nieruchomosci, ulga na dziecko e tipo de rata. NENHUM trata de
ALUGAR CONTRA COMPRAR. Similaridade 0,42 contra os onze titulos do canal no
corpus, teto 0,65.

FRAQUEZA DECLARADA, e vai aqui porque esconder seria pior: o CAMINHO
ALTERNATIVO deste pacote — calcular os juros do primeiro mes como kwota vezes
oprocentowanie mensal — e a MESMA conta que o kolejny-poziom-018 usou ontem a
noite. Por isso o caminho PRINCIPAL aqui e outro: ler a linha `odsetki` do
harmonograma que o banco entrega. A multiplicacao entra so como plano B, para
quem nao tem o harmonograma, e esta declarada como repeticao no proprio video.

IDENTIDADE: faixa do canal conferida em TRES pacotes (014, 015, 016) — paleta
`{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841, bg #F4F1EA}` e trilha `Wholesome`. O 017
saiu fora dessa faixa e o 018 ja voltou (aprendizado 617).

VEREDITO DO CANAL: `suspenso` — piso de oito minutos e o melhor material NO
SHORT. Pela colisao do aprendizado 602, SETE capitulos.

PISO DE CARACTERES, calculado ANTES da primeira cena (aprendizado 616):
`piso_de_caracteres('pl-PL-MarekNeural', n_cenas=56)` da 110 caracteres por
narracao para o total fechar 480 s. Escrevi para ~127, mirando ~500 s.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO AFIRMACAO SOBRE O MUNDO. Nao ha fonte a citar porque nao ha afirmacao a
# sustentar: o video nao cita preco de imovel, nao cita valor de aluguel de
# mercado, nao cita taxa, nao cita indice, nao cita norma e nao diz o que
# compensa na Polonia.
#
# O QUE O VIDEO AFIRMA E ARITMETICA, e e uma SEPARACAO, nao uma previsao:
#   * a parcela do credito tem duas partes, juros e capital, e o banco separa as
#     duas no harmonograma que ele mesmo entrega;
#   * so a parte de JUROS e custo comparavel ao aluguel; a parte de CAPITAL
#     troca dinheiro por patrimonio e por isso nao entra na comparacao de custo;
#   * do lado da propriedade somam-se os custos que tambem nao viram patrimonio:
#     imposto, seguro e fundo de reforma, quando existirem no papel da pessoa;
#   * do lado do aluguel entra o que vai para o proprietario.
#
# AS ENTRADAS SAO TODAS DO ESPECTADOR: o aluguel que ele paga ou cotou, e a
# linha de juros do harmonograma ou da oferta dele. Nenhum numero meu entra no
# resultado.
#
# O EXEMPLO DO CAPITULO CINCO E HIPOTETICO E O VIDEO DIZ ISSO NA CENA QUE O
# ABRE: quatrocentos mil de credito, trinta anos, sete por cento, parcela de
# dois mil seiscentos e sessenta e dois que entra como DADA do papel, e aluguel
# de dois mil e quinhentos. Nao e preco de nada e nao foi medido em lugar nenhum.
#
# O QUE FOI DESCARTADO, e o descarte vai escrito:
#   (1) qualquer afirmacao sobre o que compensa, porque depende de precos que eu
#       nao tenho e de um futuro que ninguem tem;
#   (2) valorizacao do imovel e inflacao do aluguel — as duas sao PREVISAO, e o
#       video diz isso em vez de escolher um numero;
#   (3) o custo de oportunidade do wklad wlasny, que depende de uma taxa de
#       retorno que eu teria de inventar. O capitulo sete diz que ele existe e
#       que a conta nao o cobre;
#   (4) regras de imposto, de credito ou de aluguel, porque sao norma.
#
# E O QUE A CONTA NAO DECIDE esta no capitulo sete inteiro: ela compara CUSTO
# MENSAL hoje, e nada mais. Nao e recomendacao, nao prevê, e o capital que
# entra em patrimonio tambem nao e dinheiro livre — e poupanca de baixa
# liquidez, o que e diferente de dinheiro no bolso.
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


# Links gravados pela busca via `pg_net`. NENHUM repete pacote anterior deste
# canal: os vinte e um ja usados foram lidos de TODAS as specs do canal antes
# da escolha. Todos com catorze segundos ou mais (a cena fica em ~9,2 s e o
# preparo pede ~12,2 s).
BROLL = {
    7816382: ("https://videos.pexels.com/video-files/7816382/7816382-hd_1280_720_25fps.mp4",
              "Pavel Danilyuk",
              "https://www.pexels.com/video/realtor-giving-the-key-of-new-house-to-clients-7816382/"),
    31400388: ("https://videos.pexels.com/video-files/31400388/13397556_1280_720_25fps.mp4",
               "Jakub Zerdzicki",
               "https://www.pexels.com/video/hand-holding-keys-over-money-and-mini-house-model-31400388/"),
    8293010: ("https://videos.pexels.com/video-files/8293010/8293010-hd_1280_720_30fps.mp4",
              "RDNE Stock project",
              "https://www.pexels.com/video/people-holding-keys-8293010/"),
    4554460: ("https://videos.pexels.com/video-files/4554460/4554460-hd_1366_720_50fps.mp4",
              "cottonbro studio",
              "https://www.pexels.com/video/a-man-and-woman-are-looking-at-a-laptop-4554460/"),
    4553206: ("https://videos.pexels.com/video-files/4553206/4553206-hd_1366_720_50fps.mp4",
              "cottonbro studio",
              "https://www.pexels.com/video/a-man-and-woman-are-standing-in-front-of-a-door-4553206/"),
    7647714: ("https://videos.pexels.com/video-files/7647714/7647714-hd_1280_720_24fps.mp4",
              "Anastasia Shuraeva",
              "https://www.pexels.com/video/couple-putting-a-seal-on-their-box-7647714/"),
    7647717: ("https://videos.pexels.com/video-files/7647717/7647717-hd_1280_720_24fps.mp4",
              "Anastasia Shuraeva",
              "https://www.pexels.com/video/couple-unpacking-their-things-7647717/"),
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
# A separacao — juros contra capital, com as entradas nomeadas — abre o capitulo
# 2 e fecha perto dos 140 s. Vou medir a FRASE no legendas.srt depois do render.

# ---------------------------- 1 -------------------------------------- ~71 s
B("Wynajem czy kredyt", "i dlaczego porównanie wychodzi źle",
  "Wynajem czy kredyt. Prawie każdy porównuje czynsz najmu z całą ratą kredytu, i to jedno porównanie przekręca cały wynik.",
  "realtor giving the key of a new house", 7816382, cap="Wynajem czy kredyt")
T("Bo rata to dwie rzeczy", "a czynsz jedna",
  "Bo rata to dwie rzeczy w jednej liczbie: odsetki i kapitał. Czynsz najmu to jedna rzecz, i cała idzie do właściciela.")
T("Odsetki to koszt", "wracają do banku i znikają",
  "Odsetki są kosztem w czystej postaci: płacisz je za to, że pożyczyłeś, i nigdy ich nie widzisz z powrotem. Są ceną czasu, w którym pieniądz banku jest u ciebie.")
T("Kapitał to nie koszt", "zmienia się w majątek",
  "Kapitał nie jest kosztem. To ta sama twoja złotówka, która przestaje być gotówką i zaczyna być mieszkaniem.")
T("Dlatego porównanie", "musi być koszt do kosztu",
  "Dlatego porównanie uczciwe to koszt do kosztu: czynsz najmu kontra ODSETKI, nie kontra cała rata.")
T("Różnica jest duża", "i zmienia odpowiedź",
  "Różnica nie jest drobna. Na początku kredytu odsetki to prawie cała rata, ale prawie nie znaczy cała, i to prawie decyduje. I właśnie dlatego warto ją policzyć raz, dokładnie.")
T("Czego tu nie będzie", "żadnej prognozy",
  "Nie usłyszysz tu prognozy wzrostu cen mieszkań ani wzrostu czynszów. Tego nie wiem, i nikt nie wie.")
T("Co zrobimy", "jedno odjęcie i jedno dodanie",
  "Zrobimy jedno rozdzielenie, jedno dodanie i jedno porównanie, z liczbami, które są na twoich własnych papierach. Bez kalkulatora kredytowego i bez żadnej aplikacji.")

# ---------------------------- 2 -------------------------------------- ~71 s
B("Rachunek", "dwie strony, te same jednostki",
  "Strona najmu: czynsz, który płacisz właścicielowi. To wszystko, co z tej strony jest kosztem bezpowrotnym.",
  "keys over money and a house model", 31400388, cap="Rachunek")
T("Strona własności", "zaczyna od odsetek",
  "Strona własności zaczyna się od odsetek pierwszego miesiąca. To liczba z harmonogramu, który bank wydaje razem z ofertą.")
T("I dodaje to", "co też nie wraca",
  "Do odsetek dodajesz koszty własności, które też nie wracają: podatek od nieruchomości, ubezpieczenie i fundusz remontowy. Te trzy liczby bywają małe, ale nie są zerem.")
T("Tylko jeśli są na papierze", "nie z głowy",
  "Dodajesz je tylko jeśli są na twoim papierze, w twojej kwocie. Nie z pamięci i nie ze średniej z internetu.")
T("Porównanie", "dwie liczby, jeden znak",
  "Teraz porównujesz: czynsz najmu kontra suma ze strony własności. Jeden znak, i masz koszt mieszkania w obu wariantach.")
T("Co zostaje poza", "część kapitałowa",
  "Poza porównaniem zostaje część kapitałowa raty. Ona nie zniknęła: po prostu nie jest kosztem, jest oszczędzaniem.")
T("Ile to jest", "odejmij od raty",
  "Ile dokładnie? Odejmij odsetki od całej raty i masz kapitał. Te dwie liczby zawsze się do raty sumują. Nic tu nie trzeba szacować: to zwykłe odejmowanie.")
T("Dlatego dwa rachunki", "koszt osobno, oszczędzanie osobno",
  "Dlatego są dwa rachunki, nie jeden: koszt mieszkania i kwota, którą odkładasz. Mieszanie ich daje odpowiedź bez sensu.")

# ---------------------------- 3 -------------------------------------- ~71 s
B("Gdzie przeczytać odsetki", "harmonogram, nie kalkulator",
  "Odsetki pierwszego miesiąca przeczytasz w harmonogramie spłat. Bank podaje go do oferty, i jest tam kolumna odsetki.",
  "people holding keys", 8293010, cap="Gdzie przeczytać odsetki")
T("To najlepsze źródło", "bo nic nie liczysz",
  "To najlepsze źródło, bo nic nie szacujesz: bierzesz liczbę z pierwszego wiersza i przepisujesz ją do swojego rachunku.")
T("Jeśli nie masz harmonogramu", "jest plan B",
  "Jeśli harmonogramu jeszcze nie masz, jest plan B: kwota kredytu razy oprocentowanie roczne podzielone przez dwanaście. Harmonogram możesz też poprosić przed podpisaniem umowy.")
T("I mówię wprost", "ten sam rachunek co ostatnio",
  "Mówię wprost: to ta sama operacja, którą policzyliśmy w poprzednim odcinku o ratach. Tu jest tylko planem awaryjnym.")
T("Druga liczba", "czynsz najmu",
  "Druga liczba to czynsz najmu, ten, który płacisz właścicielowi. Nie licz do niego mediów ani czynszu administracyjnego.")
T("Dlaczego nie media", "są w obu wariantach",
  "Media i czynsz administracyjny zostawiamy poza rachunkiem, bo płacisz je i tak, w najmie i we własności. Skracają się. Każda liczba obecna po obu stronach wypada z porównania.")
T("Trzy małe liczby", "po stronie własności",
  "Zostają trzy małe liczby ze strony własności: podatek od nieruchomości, ubezpieczenie i fundusz remontowy, jeśli je masz.")
T("Masz wszystko", "pięć liczb, może cztery",
  "To wszystko: pięć liczb, a u wielu osób cztery. Pozostaje zrozumieć, dlaczego cała rata wprowadza w błąd.")

# ---------------------------- 4 -------------------------------------- ~71 s
B("Dlaczego cała rata myli", "i myli w jedną stronę",
  "Porównanie czynszu z całą ratą zawsze przechyla wynik w stronę najmu, bo do kosztu dolicza twoje własne oszczędzanie.",
  "a couple looking at a laptop", 4554460, cap="Dlaczego cała rata myli")
T("To jak policzyć", "wpłatę na lokatę jako wydatek",
  "To tak, jakbyś do kosztów miesiąca doliczył przelew na własną lokatę. Pieniądz wyszedł z konta, ale nie zniknął.")
T("Na początku jednak", "kapitał jest malutki",
  "Trzeba to powiedzieć uczciwie: na początku długiego kredytu część kapitałowa jest naprawdę mała, więc błąd też jest mały. Przy trzydziestu latach to kilkaset złotych z całej raty.")
T("I rośnie z czasem", "rok po roku",
  "Ale rośnie co miesiąc, a po kilku latach już nie jest mały. Ta sama rata, coraz mniej kosztu i coraz więcej majątku.")
T("Dlatego rachunek", "robi się na dziś",
  "Dlatego ten rachunek robi się na dziś, z pierwszym wierszem harmonogramu, i powtarza po roku, bo wynik się przesuwa.")
T("Czego nie dodaję", "wzrostu czynszów",
  "Nie dodaję do niego wzrostu czynszów ani wzrostu cen mieszkań. Oba mogą się zdarzyć, i żadnego nie umiem przewidzieć. Dwie prognozy w jednym rachunku dają dwa razy większy błąd.")
T("Ani spadku", "w drugą stronę też nie",
  "I nie zakładam spadku. Rachunek, który zakłada przyszłość, przestaje być rachunkiem i staje się opinią w cyfrach.")
T("Teraz liczby", "i są wymyślone",
  "Teraz liczby, żeby to było widać. Są wymyślone przeze mnie, i mówię to w scenie, która otwiera przykład.")

# ---------------------------- 5 -------------------------------------- ~71 s
B("Przykład", "liczby wymyślone, i mówię to wprost",
  "Liczby, które teraz usłyszysz, są wymyślone, żeby rachunek był widoczny. To nie jest cena żadnego mieszkania.",
  "a couple standing in front of a door", 4553206, cap="Przykład na okrągłych liczbach")
T("Kredyt", "kwota, okres, oprocentowanie",
  "Kredyt: czterysta tysięcy złotych, trzydzieści lat, siedem procent w roku. Trzy dane, wszystkie z oferty.")
T("Rata z oferty", "nie liczę jej",
  "Rata z oferty: dwa tysiące sześćset sześćdziesiąt dwa złote. Nie liczę jej — bank ją wpisał, ja ją przepisuję.")
T("Odsetki pierwszego miesiąca", "z harmonogramu",
  "Odsetki pierwszego miesiąca: dwa tysiące trzysta trzydzieści trzy złote. To pierwszy wiersz kolumny odsetki. Ta kwota rośnie w każdym kolejnym miesiącu, co do złotówki.")
T("Czyli kapitał", "to resztka",
  "Odejmij jedno od drugiego i kapitał wychodzi około trzystu trzydziestu złotych. Tyle w tym miesiącu odkładasz.")
T("Koszty własności", "trzy małe liczby",
  "Dodaj podatek czterdzieści, ubezpieczenie czterdzieści i fundusz remontowy sto dwadzieścia. Razem dwieście złotych.")
T("Strona własności", "suma kosztu",
  "Strona własności: dwa tysiące trzysta trzydzieści trzy plus dwieście, czyli dwa tysiące pięćset trzydzieści trzy.")
T("I najem", "jedna liczba",
  "Strona najmu: czynsz dwa tysiące pięćset złotych. Różnica to trzydzieści trzy złote, czyli praktycznie remis.")

# ---------------------------- 6 -------------------------------------- ~71 s
B("Co się właśnie stało", "porównanie się odwróciło",
  "Zobacz, co się stało. Przy całej racie kredyt wyglądał na sto sześćdziesiąt dwa złote droższy od najmu miesięcznie.",
  "couple sealing a box", 7647714, cap="Co się właśnie stało")
T("Po rozdzieleniu", "remis",
  "Po rozdzieleniu odsetek od kapitału wychodzi remis, i dodatkowo odkładasz trzysta trzydzieści złotych miesięcznie.")
T("To nie znaczy", "że kredyt wygrał",
  "To nie znaczy, że kredyt wygrał. Znaczy, że pierwsze porównanie odpowiadało na inne pytanie niż to, które zadałeś.")
T("Co jeszcze dodać", "jeśli jest na papierze",
  "Jeśli twoja oferta ma prowizję albo ubezpieczenie kredytu w ratach, dolicz je do strony własności. Są kosztem. Reguła jest ta sama: wchodzi tylko to, co jest zapisane.")
T("A po stronie najmu", "też jest linia",
  "Po stronie najmu też bywa linia dodatkowa: kaucja nie jest kosztem, bo wraca, ale prowizja dla biura już jest.")
T("Jak je rozłożyć", "na miesiące",
  "Koszty jednorazowe rozłóż na tyle miesięcy, ile planujesz tam mieszkać. Inaczej jedna liczba zniekształca cały rachunek.")
T("Czego nie dodaję", "swojego czasu",
  "Nie dodaję remontów, których jeszcze nie było, ani swojego czasu. Istnieją, ale nie porównują się z niczym na papierze.")
T("Zostaje najważniejsze", "czego rachunek nie rozstrzyga",
  "Zostaje rzecz najważniejsza, i jest nią to, czego ten rachunek nie rozstrzyga. O tym cały następny rozdział.")

# ---------------------------- 7 -------------------------------------- ~71 s
B("Czego nie rozstrzyga", "i to jest uczciwa część",
  "Ten rachunek porównuje koszt mieszkania DZISIAJ. Nie mówi, co się opłaca przez trzydzieści lat, i nie udaje, że mówi.",
  "couple unpacking their things", 7647717, cap="Czego rachunek nie rozstrzyga")
T("Kapitał nie jest gotówką", "i to nie drobiazg",
  "Kapitał, który odkładasz w mieszkaniu, to oszczędzanie o niskiej płynności. Nie wyjmiesz go w miesiąc, gdy będzie trzeba.")
T("Wkład własny", "ma swój koszt",
  "Wkład własny też ma koszt: to pieniądz, który mógł pracować gdzie indziej. Nie wliczam go, bo musiałbym zgadnąć stopę.")
T("Najem ma swoją wartość", "i nie jest zerowa",
  "A najem daje coś, czego rachunek nie wycenia: możesz się wyprowadzić w miesiąc. Dla części osób to warte więcej niż różnica. Rachunek tego nie liczy, a ty możesz to wycenić sam.")
T("Krok pierwszy", "weź dwie liczby",
  "Cztery kroki. Pierwszy: wypisz czynsz najmu i odsetki pierwszego miesiąca z harmonogramu swojej oferty.")
T("Krok drugi", "dodaj to, co na papierze",
  "Drugi: dodaj do odsetek podatek, ubezpieczenie i fundusz remontowy — tylko te, które masz zapisane w swoich kwotach.")
T("Krok trzeci", "porównaj i zapisz kapitał",
  "Trzeci: porównaj obie strony, a potem osobno zapisz, ile wynosi część kapitałowa. To twoje oszczędzanie, nie koszt.")
C("Krok czwarty", "i napisz tylko stronę",
  "Czwarty: powtórz po roku, bo wynik się przesuwa. Napisz w komentarzu, która strona wyszła taniej — bez kwot.")


# =============================== O SHORT =====================================
# `suspenso` manda o MELHOR MATERIAL para o short, e aqui o melhor material e a
# separacao: comparar com a parcela inteira inclui a sua propria poupanca no
# custo. O short entrega isso em duas frases e NAO da ordem nenhuma.
SHORT = [
    {"layout": "titulo", "kicker": "Wynajem czy kredyt", "sub": "złe porównanie",
     "nar": "Prawie każdy porównuje czynsz najmu z całą ratą kredytu. To jedno "
            "porównanie przekręca wynik.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Rata to dwie rzeczy", "sub": "odsetki i kapitał",
     "nar": "W racie są odsetki i kapitał. Odsetki znikają w banku, a kapitał "
            "zostaje u ciebie jako majątek.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Więc porównaj", "sub": "czynsz z odsetkami",
     "nar": "Porównuj czynsz najmu z odsetkami pierwszego miesiąca, nie z całą "
            "ratą. Liczba jest w harmonogramie.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "I dodaj", "sub": "to, co też nie wraca",
     "nar": "Po stronie własności dodaj podatek, ubezpieczenie i fundusz "
            "remontowy — jeśli masz je na papierze.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Z całą ratą", "sub": "liczysz własne oszczędzanie",
     "nar": "Licząc całą ratę, wrzucasz własne oszczędzanie do kosztów. Cały "
            "przykład jest w filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Czynsz", "l2": "czy odsetki?"}

COPY = """# kolejny-poziom-019

## TITULO
Wynajem czy Kredyt? Porównaj Czynsz z Odsetkami, Nie z Całą Ratą — Policz na Swoich Liczbach

## TITULO SHORT
Czynsz porównaj z odsetkami, nie z ratą

## DESCRICAO
Wynajem czy kredyt. Prawie każdy porównuje czynsz najmu z całą ratą kredytu — i to jedno porównanie przekręca cały wynik, zawsze w tę samą stronę. Powód jest prosty: rata to dwie różne rzeczy zapisane w jednej liczbie. Odsetki są kosztem w czystej postaci, płacisz je za to, że pożyczyłeś, i nigdy ich nie widzisz z powrotem. Kapitał kosztem nie jest: to ta sama twoja złotówka, która przestaje być gotówką i zaczyna być mieszkaniem. Porównanie uczciwe to koszt do kosztu, czyli czynsz najmu kontra ODSETKI.

Film pokazuje rachunek na pięciu liczbach, a u wielu osób na czterech, i wszystkie są na papierach, które już masz. Strona najmu to czynsz, który płacisz właścicielowi. Strona własności zaczyna się od odsetek pierwszego miesiąca — liczby z harmonogramu spłat, który bank wydaje razem z ofertą, z kolumny „odsetki", pierwszy wiersz. Do tego dodajesz koszty własności, które też nie wracają: podatek od nieruchomości, ubezpieczenie i fundusz remontowy — ale tylko te, które masz zapisane w swoich kwotach, nigdy ze średniej z internetu. Media i czynsz administracyjny zostają poza rachunkiem, bo płacisz je i tak, w obu wariantach, więc się skracają.

Przykład na okrągłych liczbach — wymyślonych przeze mnie i zadeklarowanych jako wymyślone w scenie, która go otwiera — pokazuje, jak porównanie się odwraca. Przy całej racie kredyt wygląda na wyraźnie droższy od najmu. Po rozdzieleniu odsetek od kapitału wychodzi praktycznie remis, a kapitał, który co miesiąc odkładasz, zostaje jako osobna liczba: twoje oszczędzanie, nie koszt. Jest też rozdział o tym, dlaczego cała rata myli zawsze w stronę najmu, i dlaczego na początku długiego kredytu ten błąd jest mały, ale rośnie co miesiąc — dlatego rachunek robi się na dziś i powtarza po roku.

I rozdział najważniejszy: czego ten rachunek NIE rozstrzyga. Porównuje koszt mieszkania dzisiaj i nic więcej. Nie mówi, co się opłaca przez trzydzieści lat, nie zakłada wzrostu ani spadku cen mieszkań i czynszów — tego nie wiem i nikt nie wie, a rachunek, który zakłada przyszłość, przestaje być rachunkiem. Kapitał odkładany w mieszkaniu to oszczędzanie o niskiej płynności: nie wyjmiesz go w miesiąc. Wkład własny ma swój koszt, bo mógł pracować gdzie indziej. A najem daje coś, czego rachunek nie wycenia: możliwość wyprowadzki w miesiąc, co dla części osób jest warte więcej niż cała różnica.

Materiał informacyjny, nie jest doradztwem finansowym ani rekomendacją.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Rachunek jest w pierwszych dwóch minutach, więc nie musisz oglądać całości. Strona najmu: czynsz, który płacisz właścicielowi. Strona własności: odsetki pierwszego miesiąca z harmonogramu, plus podatek od nieruchomości, ubezpieczenie i fundusz remontowy — tylko te, które masz zapisane. Media i czynsz administracyjny pomijasz, bo są w obu wariantach i się skracają. Część kapitałowa raty (cała rata minus odsetki) NIE jest kosztem — zapisz ją osobno, to twoje oszczędzanie. Dwie pułapki: porównanie czynszu z całą ratą zawsze przechyla wynik w stronę najmu, bo dolicza do kosztu twoje własne odkładanie; a koszty jednorazowe (prowizja, opłaty) rozłóż na tyle miesięcy, ile planujesz tam mieszkać. Powtórz rachunek po roku, bo wynik się przesuwa. Jeśli policzysz, napisz w komentarzu tylko, która strona wyszła taniej — bez kwot.

## HASHTAGS
#WynajemCzyKredyt #KredytHipoteczny #KolejnyPoziom

## TAGS
wynajem czy kredyt, odsetki czy rata, czesc kapitalowa, harmonogram splat, koszt mieszkania, kredyt hipoteczny, najem mieszkania, podatek od nieruchomosci, fundusz remontowy, finanse osobiste, kolejny poziom, jak policzyc, oszczedzanie w mieszkaniu, plynnosc, wklad wlasny

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
Pavel Danilyuk; Jakub Zerdzicki; RDNE Stock project; cottonbro studio;
Anastasia Shuraeva.

## AVISO SOBRE OS NUMEROS
ZERO AFIRMACAO SOBRE O MUNDO, e por isso nao ha fonte a citar: o video nao cita
preco de imovel, nao cita aluguel de mercado, nao cita taxa, indice nem norma, e
nao diz o que compensa na Polonia.

O QUE O VIDEO AFIRMA E ARITMETICA, e e uma SEPARACAO, nao uma previsao:
  * a parcela tem duas partes, juros e capital, e o banco separa as duas no
    harmonograma que ele mesmo entrega;
  * so a parte de JUROS e custo comparavel ao aluguel; a parte de CAPITAL troca
    dinheiro por patrimonio, e por isso nao entra na comparacao de custo;
  * do lado da propriedade somam-se os custos que tambem nao viram patrimonio:
    imposto, seguro e fundo de reforma, quando existirem no papel da pessoa;
  * media e condominio ficam FORA dos dois lados, porque se pagam igual nos
    dois e portanto se cancelam.

AS ENTRADAS SAO TODAS DO ESPECTADOR: o aluguel que ele paga ou cotou, e a linha
de juros do harmonograma da oferta dele. Nenhum numero meu entra no resultado.

O EXEMPLO DO CAPITULO CINCO E HIPOTETICO E O VIDEO DIZ ISSO NA CENA QUE O ABRE:
quatrocentos mil de credito, trinta anos, sete por cento, parcela de dois mil
seiscentos e sessenta e dois que entra como DADA do papel, juros de dois mil
trezentos e trinta e tres, e aluguel de dois mil e quinhentos. Nao e preco de
nada e nao foi medido em lugar nenhum.

O QUE FOI DESCARTADO, e o descarte vai escrito:
  (1) qualquer afirmacao sobre o que compensa, porque depende de precos que eu
      nao tenho e de um futuro que ninguem tem;
  (2) valorizacao do imovel e inflacao do aluguel — as duas sao PREVISAO, e o
      video diz isso em vez de escolher um numero;
  (3) o custo de oportunidade do wklad wlasny, que exigiria inventar uma taxa de
      retorno. O capitulo sete diz que ele existe e que a conta nao o cobre;
  (4) regras de imposto, de credito ou de aluguel, porque sao norma.

FRAQUEZA DECLARADA, que vale mais escrita que escondida: o PLANO B deste pacote
— juros do primeiro mes como kwota vezes oprocentowanie mensal — e a MESMA
operacao do kolejny-poziom-018, publicado horas antes. Por isso o caminho
principal aqui e LER a linha do harmonograma, e o video declara a repeticao em
voz alta na cena que apresenta o plano B.

E O QUE A CONTA NAO DECIDE esta no capitulo sete inteiro: ela compara custo
mensal hoje e nada mais. O capital que entra em patrimonio nao e dinheiro livre
— e poupanca de baixa liquidez. E o aluguel entrega mobilidade, que a conta nao
precifica e que para parte das pessoas vale mais que a diferenca.

## FONTES
NENHUMA FONTE NORMATIVA, DE MERCADO OU ESTATISTICA E CITADA, e isso e
deliberado. As unicas "fontes" sao os documentos do proprio espectador: o
contrato ou a oferta de aluguel, e o harmonograma de pagamentos da oferta de
credito dele.
B-roll: Pexels, licenca Pexels, creditos por clipe em broll_creditos.json.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-019",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
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
    from ensaio import (duracao_estimada, duracao_estimada_short, duracao_cena,
                        piso_de_caracteres)
    grava(SPEC, "fabrica/specs/kolejny-poziom-019.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    piso = piso_de_caracteres(SPEC["voz"], n_cenas=len(CENAS), cenas_por_cap=8)
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"piso por cena: {piso['min_por_cena']} ({piso['manda']}) | "
          f"media real: {sum(len(c.get('nar','')) for c in CENAS)/len(CENAS):.0f}")
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
        if "jeden znak, i masz koszt" in (c.get("nar") or ""):
            print(f"  a resposta fecha em {t:.1f}s (cena {i})")
    import unicodedata
    campos = []
    for c in CENAS + SHORT:
        campos += [c.get("nar",""), c.get("kicker",""), c.get("sub",""), c.get("cap","")]
    txt = "".join(campos); letras=[ch for ch in txt if ch.isalpha()]
    ac=[ch for ch in letras if len(unicodedata.normalize("NFD",ch))>1 or ch in "łŁ"]
    print(f"diacriticos: {100*len(ac)/max(len(letras),1):.2f}%")
