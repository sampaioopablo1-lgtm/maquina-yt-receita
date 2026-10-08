"""kolejny-poziom-s005 — a rodada em que eu corrigi a rotina, nao a spec.

ALAVANCA: A (alcance por short). Decimo primeiro short solto, quinto do kolejny.

O QUE DEU CERTO: a ponte, onze vezes seguidas, e o modelo de duracao, cujo
residuo ficou em -0,2% no s004 (a faixa toda vai de +5,2% a -2,8%).
O QUE NAO DEU: eu, pela QUARTA vez, li janela curta e conclui coisa grande. As
04:10 escrevi que o kolejny-019 "saturou em 330", com base em quatro leituras
horarias identicas. As 05:11 ele foi para 356. A serie inteira:
  4 -> 283 -> 330 -> 330 -> 330 -> 330 -> 356.
O degrau do contador publico tem intervalo de PELO MENOS ~4 h. Aprendizado 647.
O QUE VOU MUDAR, e foi na ROTINA e nao na spec: as janelas agora sao DUAS —
12 h para COMPARAR pecas, 24 h ou mais para dizer que UMA peca PAROU. E a secao
0 da rotina passou a listar os quatro erros em ordem, porque a assinatura e
sempre a mesma e eu reincidi quatro vezes.

O QUE SOBREVIVE do 646: o TAMANHO da rajada varia por uma ordem de grandeza entre
pecas (356, 498, 884, 1.132, 1.155) e NAO existe teto comum. Os dois perto de
1.133 andaram +0 e +13 em 19,64 h — esses sim parecem no fim da curva.

POR QUE O KOLEJNY: o epomeno esta sem longo livre (cinco usados) e o proximo la
pede pacote, cujo ritmo e um a cada dois dias. O kolejny tinha dois livres e este
gasta um. NUMERO DE PARTIDA: 884 do melhor solto do canal e a mediana da rajada
do canal, entre 356 e 498.

A FORMA, e NAO e experimento novo (secao 5-d): o gancho do epomeno-s002, o melhor
da frota — ENTRADA ERRADA INVALIDA O TEU NUMERO. Aqui a entrada errada e a
MEDIA: ela esconde o mes de pico, e o pacote tem de cobrir o pico. Gancho visual
segue cartao de texto nas cinco cenas, para nao sujar o experimento 33 — e os
TRES testes que o 33 trava (b-roll na cena 1, short de 22-26 s, e matar o
fade-in de dois quadros pretos do 644) seguem esperando.

DE ONDE SAI: do longo JA PUBLICADO `-5aMrDsxlZE` (kolejny-poziom-014). O short
original ensina a conta do desperdicio — preco por gigabyte vezes gigabytes nao
usados, com a MEDIA de tres meses. Este ataca o capitulo "Kiedy ta liczba myli":
a media esconde o mes de pico, e quem corta o pacote pela media paga excedente
no mes em que viajou. Entrada certa e o MAXIMO dos tres meses — a nao ser que o
excedente seja barato, e isso esta no contrato, nao na memoria.

IDENTIDADE: faixa conferida em SETE pacotes do canal, todos identicos — paleta
`{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841, bg #F4F1EA}`, trilha `Wholesome`, voz
`pl-PL-MarekNeural`. O 017 segue fora da faixa, de proposito.

TENDENCIA: o feed PL/26 NAO foi lido nesta rodada, e digo em vez de inventar. A
26 e PROXY (a real e a 27, sem chart, 610) e o chart repete catorze de quinze
itens em quatro horas (623). A evidencia mais forte e a medicao da propria frota.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita preco de plano, nao cita tamanho de
# pacote, nao cita custo de excedente, nao cita operadora e nao nomeia orgao. Os
# unicos numeros ditos sao "tres" (tres meses) e "um" (uma viagem), e sao a
# aritmetica da propria conta.
#
# O QUE O VIDEO AFIRMA: que a media de tres meses pode ficar abaixo do mes de
# maior consumo, e que por isso dimensionar o pacote pela media expoe ao
# excedente no mes de pico. Isso e aritmetica e esta no longo `-5aMrDsxlZE` com
# as fontes.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) quanto custa o excedente em qualquer operadora polonesa, e se ha
#       limitacao de velocidade em vez de cobranca — NAO reconferido hoje em duas
#       fontes; o short MANDA conferir no contrato em vez de afirmar;
#   (2) qualquer preco, tamanho de pacote ou valor;
#   (3) o que a conta NAO decide — esta no longo, e o short manda para la.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Wziąłeś średnią?", "sub": "to złe wejście",
     "nar": "Wziąłeś średnie zużycie z trzech miesięcy? Do tej decyzji średnia "
            "nie wystarczy.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Pakiet pokrywa", "sub": "miesiąc najwyższy",
     "nar": "Pakiet musi pokryć miesiąc najwyższy, nie przeciętny. Jeden "
            "wyjazd i już przekraczasz.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Weź maksimum", "sub": "nie średnią",
     "nar": "Weź więc maksimum z trzech miesięcy, nie średnią. Do niego "
            "dobieraj pakiet.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Jeden wyjątek", "sub": "tanie przekroczenie",
     "nar": "Jest wyjątek: jeśli przekroczenie jest tanie, średnia wystarczy. "
            "Sprawdź to w umowie.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Porównaj dziś", "sub": "maksimum i pakiet",
     "nar": "Porównaj maksimum z pakietem. Cały rachunek jest w filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Średnia myli", "l2": "weź maksimum"}

COPY = """# kolejny-poziom-s005

## TITULO
Średnia z Trzech Miesięcy Myli: Pakiet Musi Pokryć Miesiąc Najwyższy, nie Przeciętny

## TITULO SHORT
Średnia myli. Weź maksimum

## DESCRICAO
Rachunek na marnowane gigabajty jest prosty i robi się go raz: miesięczną kwotę dzielisz przez wielkość pakietu, co daje cenę gigabajta, a potem od pakietu odejmujesz swoje zużycie i mnożysz jedno przez drugie. Wynik to złote, które każdego miesiąca płacisz za dane, których nie użyłeś. I właśnie w tym drugim składniku — w „swoim zużyciu" — kryje się błąd, który kosztuje.

Bo prawie każdy wstawia tam ŚREDNIĄ z trzech miesięcy. Średnia jest dobrym wejściem, gdy chcesz wiedzieć, ile marnujesz TERAZ. Jest złym wejściem, gdy chcesz na tej podstawie ZMNIEJSZYĆ pakiet, a to jest zwykle prawdziwy cel. Pakiet nie obsługuje miesiąca przeciętnego — obsługuje każdy miesiąc osobno, w tym ten najwyższy. Jeden wyjazd, jeden tydzień pracy zdalnej z innego miasta, jeden miesiąc bez wifi w domu, i zużycie skacze ponad średnią. Jeśli dobrałeś pakiet do średniej, w tym miesiącu wchodzisz w przekroczenie — i oszczędność z poprzednich miesięcy potrafi zniknąć w jednym rachunku.

Uczciwa wersja: weź MAKSIMUM z trzech miesięcy, nie średnią, i do niego dobieraj pakiet. Zachowaj średnią, ale jako osobną liczbę — ona mówi, ile marnujesz; maksimum mówi, czego nie możesz zejść poniżej.

Jest jeden wyjątek i wart sprawdzenia, bo zmienia odpowiedź: jeśli w twojej umowie przekroczenie jest tanie albo kończy się tylko ograniczeniem prędkości, a nie dopłatą, to ryzyko miesiąca szczytowego jest małe i można schodzić do średniej. To trzeba przeczytać w umowie, nie zgadnąć — i dlatego tego tutaj nie podaję.

Nie ma tu żadnej ceny, żadnego rozmiaru pakietu i żadnej nazwy operatora: liczby, które decydują, są na twoim rachunku i w twojej aplikacji. Pełny rachunek, miejsce gdzie te liczby leżą, czego ten rachunek NIE obejmuje i jak przejść od jednego miesiąca do całej umowy — są w filmie.

## COMENTARIO FIXADO
Rachunek: kwota przez pakiet daje cenę gigabajta; pakiet minus zużycie daje nadwyżkę; mnożysz. Haczyk jest w „zużyciu": do ZMNIEJSZENIA pakietu nie wstawiaj średniej z trzech miesięcy, tylko MAKSIMUM — pakiet obsługuje każdy miesiąc osobno, w tym ten, w którym wyjechałeś. Średnią zachowaj jako drugą liczbę: mówi ile marnujesz, nie czego nie możesz zejść poniżej. Wyjątek: jeśli w umowie przekroczenie jest tanie albo to tylko ograniczenie prędkości, średnia wystarczy — ale to przeczytaj, nie zgaduj. Jeśli policzysz, napisz, czy maksimum było dużo wyższe od średniej — bez kwot.

## HASHTAGS
#Telefon #Pakiet #KolejnyPoziom

## TAGS
telefon, pakiet danych, gigabajty, rachunek, srednia, maksimum, przekroczenie, umowa, finanse osobiste, polska, obliczenia, operator, kolejny poziom, oszczedzanie, zuzycie danych

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

## AVISO SOBRE OS NUMEROS
ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita preco de plano, nao cita tamanho de
pacote, nao cita custo de excedente, nao cita operadora e nao nomeia orgao. Os
unicos numeros ditos sao "tres" e "um", e sao a aritmetica da propria conta.

O QUE O VIDEO AFIRMA: que a media de tres meses pode ficar abaixo do mes de maior
consumo, e que por isso dimensionar o pacote pela media expoe ao excedente no mes
de pico. E aritmetica e esta no longo kolejny-poziom-014 (-5aMrDsxlZE) com as
fontes.

DESCARTADO, e vai escrito:
  (1) quanto custa o excedente em qualquer operadora polonesa, e se ha limitacao
      de velocidade em vez de cobranca — NAO reconferido hoje em duas fontes; o
      short MANDA conferir no contrato em vez de afirmar;
  (2) qualquer preco, tamanho de pacote ou valor;
  (3) o que a conta NAO decide — esta no longo, e o short manda para la.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-014, -5aMrDsxlZE) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s005",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "-5aMrDsxlZE",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/kolejny-poziom-s005.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, mira 33-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
