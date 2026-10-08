"""kolejny-poziom-s003 — a rodada em que o epomeno ficou sem longo livre.

ALAVANCA: A (alcance por short). Nono short solto, terceiro do kolejny.

O QUE DEU CERTO: o short solto, oito publicados em dois dias, formato de melhor
medicao da frota e o mais barato em cota.
O QUE NAO DEU: o esforco marginal nao pode mais ir ao epomeno. Com o s005 os
CINCO longos daquele canal estao todos usados como origem (eimuyGaCor8,
h04-UVlVevs, opFSah50OWo, 9U2h4HuAzLs, nttW9fR8wyY). Novo short solto no epomeno
pede longo NOVO, ou seja pacote completo, e o ritmo do canal e um pacote a cada
dois dias — o 017 saiu em 07/10. Logo esta rodada vai ao KOLEJNY, que e o
segundo em alcance por short (884, 481, 330, 307) e tem quatro longos livres.
O QUE VOU MUDAR: nada na spec. A restricao e de estoque de pauta, nao de forma.

DADO DESTA RODADA, e ele confirma o degrau do 645: o kolejny-015 foi de 455 para
481 numa hora (+26), depois de ter ficado em 455 por uma hora inteira. O contador
anda em degrau, e o delta de 17,64 h contra a base de 09:31 e +348. Nenhuma
conclusao nova sobre teto: a previsao do 643 segue aberta.

NUMERO DE PARTIDA: 330 do short do proprio longo de origem (`SguKk8lMR0s`, com
+326 em 16 h) e 884 do s002, que e o melhor solto do canal.

A FORMA, e NAO e experimento novo (secao 5-d): o gancho do s002 do epomeno, que
e o melhor da frota — ENTRADA ERRADA INVALIDA O TEU NUMERO. Aqui a entrada errada
e O MES: comparar aluguel com os juros do PRIMEIRO mes favorece o aluguel, porque
e nesse mes que os juros sao maiores. Gancho visual segue cartao de texto nas
cinco cenas, para nao sujar o experimento 33, e o 644 lembra que o video abre com
dois quadros pretos mais fade-in, cujo teste tambem espera o 33 fechar.

DE ONDE SAI, E E O PRIMEIRO SEGUNDO ANGULO DA FROTA: do longo JA PUBLICADO
`GUiq15usizw` (kolejny-poziom-019), do qual JA existe um short (`SguKk8lMR0s`).
O short original diz "compare o aluguel com os juros do primeiro mes, nao com a
prestacao inteira". Este CORRIGE aquele por dentro: os juros caem a cada
prestacao, logo o primeiro mes e o caso mais favoravel ao aluguel e a comparacao
honesta usa os juros DO MES EM QUE VOCE ESTA, lidos no cronograma. Nao e o mesmo
angulo nem contradiz o longo: refina o que o short irmao simplificou.
**POR SER SEGUNDO ANGULO, a similaridade foi conferida contra o CANAL INTEIRO
pelo portao, nao so contra o short irmao.**

IDENTIDADE: faixa do canal conferida em SETE pacotes (014, 015, 016, 018, 019,
s001 e s002), todos identicos — paleta `{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841,
bg #F4F1EA}`, trilha `Wholesome`, voz `pl-PL-MarekNeural`. O 017 segue com paleta
fora da faixa, de proposito.

TENDENCIA: o feed PL/26 NAO foi lido nesta rodada, e digo em vez de inventar. A
26 e PROXY (a real e a 27, sem chart em regiao nenhuma, 610) e o chart repete
catorze de quinze itens em quatro horas (623). A evidencia mais forte e a
medicao da propria frota, de minutos antes: declaro a troca.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita taxa de juro, nao cita prestacao, nao
# cita aluguel, nao cita percentual e nao nomeia banco nem orgao. O unico numero
# dito e "pierwszym" (primeiro mes), e e referencia de posicao na propria conta.
#
# O QUE O VIDEO AFIRMA: que numa prestacao de credito a parte de juros e maior no
# inicio e diminui a cada prestacao, enquanto a de capital cresce. Isso e
# aritmetica de amortizacao e esta no longo `GUiq15usizw` com as fontes.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) QUAL sistema de amortizacao o banco polones aplica por padrao e como isso
#       muda a curva — NAO reconferido hoje em duas fontes; o short so diz que os
#       juros caem, o que vale nos dois sistemas correntes;
#   (2) qualquer taxa, prestacao ou valor de aluguel;
#   (3) o que a conta NAO decide — esta no longo, e o short manda para la.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Których odsetek?", "sub": "to się zmienia",
     "nar": "Porównałeś czynsz z odsetkami? Dobrze. Ale z odsetkami którego "
            "miesiąca?",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Najwyższe na starcie", "sub": "potem maleją",
     "nar": "Odsetki są najwyższe w pierwszym miesiącu i maleją z każdą ratą. "
            "Kapitał rośnie.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Więc nie jest", "sub": "porównanie neutralne",
     "nar": "Więc porównanie z pierwszego miesiąca jest najlepsze dla najmu, "
            "a nie neutralne.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Weź harmonogram", "sub": "twój miesiąc",
     "nar": "Weź harmonogram i odczytaj odsetki z miesiąca, w którym jesteś. "
            "Tę liczbę porównujesz z czynszem.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Sprawdź dziś", "sub": "cały rachunek",
     "nar": "Sprawdź harmonogram dziś. Cały rachunek jest w filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Których odsetek?", "l2": "to się zmienia"}

COPY = """# kolejny-poziom-s003

## TITULO
Porównałeś Czynsz z Odsetkami? Odsetki Maleją z Każdą Ratą, Więc Liczy się Miesiąc

## TITULO SHORT
Odsetki z którego miesiąca?

## DESCRICAO
Porównanie najmu z własnością psuje się na jednej rzeczy: prawie każdy stawia czynsz obok CAŁEJ raty kredytu. To nie jest jedno porównanie, bo w racie siedzą dwie różne rzeczy. Odsetki to koszt — zostają w banku i nie wracają do ciebie. Kapitał to twoje oszczędzanie — zmniejsza dług i zostaje u ciebie. Wrzucając całą ratę do kosztów, wliczasz własne oszczędzanie do rachunku i wychodzi, że własność jest droższa, niż jest.

Dlatego porównuje się czynsz z CZĘŚCIĄ ODSETKOWĄ. Ale jest drugi krok, o którym prawie nikt nie mówi, i on decyduje: część odsetkowa nie jest stała. Jest najwyższa w pierwszym miesiącu i maleje z każdą kolejną ratą, a kapitałowa w tym samym czasie rośnie. Suma zostaje ta sama, proporcje nie.

Konsekwencja jest prosta i niewygodna: porównanie zrobione na odsetkach z pierwszego miesiąca jest najkorzystniejszym możliwym porównaniem DLA NAJMU. Nie jest neutralne. Jeżeli kredyt trwa już kilka lat, twoje dzisiejsze odsetki są wyraźnie niższe niż te z pierwszej raty, a więc dzisiejszy rachunek wypada inaczej niż ten, który zrobiłeś na starcie. Uczciwa wersja: weź harmonogram spłat, znajdź miesiąc, w którym faktycznie jesteś, i odczytaj część odsetkową z tego wiersza. Ta liczba porównuje się z czynszem.

Po stronie własności dolicz jeszcze podatek od nieruchomości, ubezpieczenie i fundusz remontowy, bo najemca ich nie płaci osobno. Po stronie najmu pamiętaj, że czynsz rośnie w czasie, a rata w kredycie o stałym oprocentowaniu nie.

Tutaj nie podaję żadnej stawki, żadnej raty i żadnej kwoty czynszu: liczba, która decyduje, wychodzi z twojego harmonogramu i twojej umowy. Pełny rachunek, miejsce gdzie odczytać odsetki i to, czego ten rachunek NIE rozstrzyga, są w filmie.

## COMENTARIO FIXADO
Dwa kroki, nie jeden. Pierwszy: porównuj czynsz z częścią ODSETKOWĄ raty, nie z całą ratą — kapitał to twoje oszczędzanie, nie koszt. Drugi, ten pomijany: odsetki maleją z każdą ratą, więc rachunek zrobiony na pierwszym miesiącu jest najkorzystniejszy dla najmu i nie jest neutralny. Weź harmonogram, znajdź miesiąc, w którym jesteś, i odczytaj odsetki z tego wiersza. Po stronie własności dolicz podatek, ubezpieczenie i fundusz remontowy. Jeśli policzysz, napisz, czy odsetki z twojego miesiąca były wyższe czy niższe od czynszu — bez podawania kwot.

## HASHTAGS
#Kredyt #Najem #KolejnyPoziom

## TAGS
kredyt, najem, odsetki, kapital, harmonogram splat, rata, wynajem czy kredyt, finanse osobiste, polska, obliczenia, amortyzacja, podatek od nieruchomosci, kolejny poziom, mieszkanie, porownanie

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
ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita taxa de juro, nao cita prestacao, nao
cita aluguel, nao cita percentual e nao nomeia banco nem orgao. O unico numero
dito e "primeiro mes", e e referencia de posicao na propria conta.

O QUE O VIDEO AFIRMA: que numa prestacao de credito a parte de juros e maior no
inicio e diminui a cada prestacao, enquanto a de capital cresce. E aritmetica de
amortizacao e esta no longo kolejny-poziom-019 (GUiq15usizw) com as fontes.

DESCARTADO, e vai escrito:
  (1) QUAL sistema de amortizacao o banco polones aplica por padrao — nao
      reconferido hoje em duas fontes; o short so diz que os juros caem, o que
      vale nos dois sistemas correntes;
  (2) qualquer taxa, prestacao ou valor de aluguel;
  (3) o que a conta NAO decide — esta no longo, e o short manda para la.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-019, GUiq15usizw) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s003",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "GUiq15usizw",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/kolejny-poziom-s003.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, mira 33-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
