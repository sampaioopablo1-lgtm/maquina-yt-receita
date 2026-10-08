"""kolejny-poziom-s009 — ta sama wplata, inna kolejnosc, inny wynik.

ALAVANCA: A (alcance por short). Nono short solto do kolejny.

O QUE DEU CERTO: a janela larga do 661 ja esta pagando. Duas pecas do kolejny que
eu teria dado por fechadas MOVERAM depois das 12 h: s003 de 72 para 81 as 14,9 h
e s004 de 18 para 32 as 13,9 h. Se eu tivesse usado o piso antigo de 6 h para
dizer "parou", teria errado nas duas. A regra conservadora — 12 h para AFIRMAR
que nao recebeu distribuicao — e a certa.

O QUE NAO DEU, e continua ABERTO em vez de concluido: o `epomeno-s007` esta com
ZERO as 7,9 h e o `s008` com ZERO as 5,9 h. Sao duas pecas do mesmo canal, no
mesmo dia, enquanto as quatro mais velhas dele somam 926 e enquanto o
kolejny-s008 ja tem 4 as 1,9 h e o labtreinamento-s004 tem 25 as 3,7 h. Isso
esta se acumulando na direcao de ser real, MAS o 661 manda esperar 12 h para
afirmar, e o s007 so chega as 12 h por volta das 22:20. NAO afirmo nada hoje:
anoto que as duas seguem em zero e que a leitura vale depois das 22:20.

O QUE VOU MUDAR, e e uma coisa so: nada de novo no instrumento nesta rodada —
a mudanca e de PAUTA e vem do 651 aplicado ao kolejny. Em vez de pegar a origem
livre de maior alcance (criterio que o 658 derrubou), peguei a de perfil
"dinheiro proprio com papel na mao": `ef_oZmfmdz4`, as taxas comendo a
contribuicao mensal. Numero de partida: 86 do short daquele pacote; 81 do melhor
solto maduro do kolejny hoje.

DE ONDE SAI: longo `ef_oZmfmdz4` (kolejny-poziom-004), capitulo "Kolejnosc ma
znaczenie", que o short original daquele pacote NAO toca — ele gasta as cinco
cenas na aritmetica do arrasto das taxas (dois por cento ao ano comendo vinte
anos de transferencias). Este ataca uma entrada errada diferente e tambem
puramente aritmetica: tratar as contas como um balde unico. A ulga conta POR ANO
e o ano que passa sem usar o limite NAO volta — logo a ordem em que o dinheiro
entra muda o resultado com a MESMA wplata.

IDENTIDADE: faixa ATUAL do canal `{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841,
bg #F4F1EA}` com trilha `Wholesome`. O pacote 004 e antigo e NAO ditou a paleta
(601).

TENDENCIA: o feed PL/26 foi lido as 06:22 e NAO foi relido nesta rodada; digo em
vez de inventar. Dele ficou a FORMA: pergunta ou imperativo em segunda pessoa.
Cena 1 pergunta, cena 5 imperativo.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita limite
# anual, nao cita aliquota, nao cita taxa, nao cita valor, nao cita prazo e NAO
# NOMEIA produto nem orgao — por isso a narracao diz "konto z ulga podatkowa" em
# vez do nome da conta. Conferido A MAO campo por campo, porque o portao
# `narracao` conta QUANTIDADES por frase e NAO pega digito cru (640).
#
# O QUE O VIDEO AFIRMA: que o beneficio fiscal e contado POR ANO e que o ano nao
# usado nao se transfere para o seguinte — logo a ORDEM em que a mesma
# contribuicao entra nas contas muda o resultado. E NORMA, nao estatistica, e
# esta no longo kolejny-poziom-004 (`ef_oZmfmdz4`), capitulos "Kolejnosc ma
# znaczenie" e "Co panstwo daje", com as fontes. Declarado aqui conforme a regra
# de fonte unica que e norma.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) o valor do limite anual e qualquer aliquota — estao no longo com fonte e
#       o short nao precisa deles para dizer que ano nao usado nao volta;
#   (2) o nome dos produtos — evitado de proposito, porque nomear produto num
#       short e o que o 609 manda nao fazer;
#   (3) a aritmetica do arrasto das taxas, que e do short original daquele
#       pacote e nao se repete aqui.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Ta sama wpłata", "sub": "ale w jakiej kolejności?",
     "nar": "Wpłacasz tę samą kwotę co miesiąc. Ale wiesz, w jakiej kolejności "
            "trafia ona na twoje konta?",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Kolejność", "sub": "zmienia wynik",
     "nar": "Kolejność zmienia wynik, bo ulga podatkowa liczy się za dany rok, a "
            "nie za całe twoje życie.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Rok niewykorzystany", "sub": "przepada",
     "nar": "Rok, w którym nie wykorzystasz ulgi, przepada. Nie przenosi się na "
            "następny.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Najpierw ulga", "sub": "resztę potem",
     "nar": "Więc najpierw zapełniasz konto z ulgą, a resztę dopiero potem. Ta "
            "sama wpłata, inny wynik.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Sprawdź swoje", "sub": "przelewy z tego roku",
     "nar": "Sprawdź, w jakiej kolejności szły twoje przelewy w tym roku. Cała "
            "kolejność jest w filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Kolejność", "l2": "zmienia wynik"}

COPY = """# kolejny-poziom-s009

## TITULO
Ta Sama Wpłata, Inna Kolejność: Dlaczego Rok Bez Ulgi Już Nie Wróci

## TITULO SHORT
Ta sama wpłata, inna kolejność

## DESCRICAO
Kiedy ktoś odkłada tę samą kwotę co miesiąc, naturalnie myśli o tym jak o jednym strumieniu pieniędzy: wpłacam tyle, odkładam tyle, reszta to szczegóły. I to jest właśnie ta jedna rzecz, która kosztuje — bo pieniądze nie trafiają do jednego worka, a to, do którego worka trafiają pierwsze, zmienia końcowy wynik przy identycznej wpłacie.

Powód nie ma nic wspólnego z prognozowaniem rynku. Ulga podatkowa jest przypisana do ROKU, nie do twojego życia. Jeśli w danym roku nie wykorzystasz jej w całości, ta część nie przechodzi na następny rok i nie wraca później — przepada. To jest zasada, nie przewidywanie, i właśnie dlatego kolejność wpłat jest decyzją, a nie szczegółem technicznym.

Z tego wynika praktyczna reguła, która nie wymaga żadnej liczby z zewnątrz. Najpierw zapełniasz to, co jest ograniczone rocznym limitem i co przepada — czyli konto z ulgą. Dopiero potem to, co zostaje, idzie tam, gdzie limitu nie ma i gdzie nic nie przepada, bo tam ta sama wpłata będzie możliwa również w przyszłym roku. Odwrotna kolejność oznacza, że oddajesz ulgę za ten rok w zamian za coś, co i tak było dostępne później.

Druga konsekwencja jest mniej oczywista. Jeśli w ciągu roku twoje możliwości się zmieniają — pojawia się premia, albo wręcz odwrotnie, miesiąc bez nadwyżki — to kolejność decyduje, na czym ta zmiana się odbije. Przy właściwej kolejności gorszy miesiąc zabiera ci część tego, co i tak można nadrobić. Przy odwrotnej zabiera ci część tego, czego nadrobić już nie będzie można.

Nie ma tu żadnego limitu, żadnej stawki i żadnej kwoty: liczby, które decydują, są w twoich przelewach i w twoim rozliczeniu. Pełna kolejność, co dokładnie daje państwo, trzy rachunki do porównania i cztery liczby do sprawdzenia — są w filmie.

## COMENTARIO FIXADO
Kluczowe zdanie jest jedno: ulga liczy się za ROK, nie za życie. Rok niewykorzystany przepada i nie przenosi się na następny — więc najpierw zapełniasz to, co przepada, a dopiero potem to, co i tak będzie dostępne w przyszłym roku. Odwrotna kolejność to oddanie ulgi za ten rok w zamian za coś, co było dostępne później. Jeśli sprawdzisz swoje przelewy z tego roku, napisz w komentarzu tylko, czy kolejność była właściwa — bez kwot.

## HASHTAGS
#Oszczednosci #Emerytura #KolejnyPoziom

## TAGS
oszczednosci, ulga podatkowa, kolejnosc wplat, roczny limit, rozliczenie, finanse osobiste, polska, planowanie, emerytura, wplata miesieczna, konto emerytalne, podatek, kolejny poziom, limit roczny, przelewy

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita limite anual,
nao cita aliquota, nao cita taxa, nao cita valor, nao cita prazo e NAO NOMEIA
produto nem orgao — a narracao diz "konto z ulga podatkowa" em vez do nome da
conta. Conferido a mao campo por campo, porque o portao `narracao` conta
quantidades por frase e nao pega digito cru (640).

O QUE O VIDEO AFIRMA: que o beneficio fiscal e contado POR ANO e que o ano nao
usado nao se transfere para o seguinte — logo a ORDEM em que a mesma contribuicao
entra nas contas muda o resultado. E NORMA, nao estatistica, e esta no longo
kolejny-poziom-004 (ef_oZmfmdz4), capitulos "Kolejnosc ma znaczenie" e "Co
panstwo daje", com as fontes. Declarado conforme a regra de fonte unica que e
norma.

DESCARTADO, e vai escrito:
  (1) o valor do limite anual e qualquer aliquota — estao no longo com fonte;
  (2) o nome dos produtos — evitado de proposito (609);
  (3) a aritmetica do arrasto das taxas, que e do short original daquele pacote.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-004, ef_oZmfmdz4) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s009",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "ef_oZmfmdz4",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/kolejny-poziom-s009.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, piso 30s, mira 34-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
