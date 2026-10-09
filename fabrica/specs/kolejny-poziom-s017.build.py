"""kolejny-poziom-s017 — a ordem, nao a quantia.

ALAVANCA desta rodada: NENHUMA mudanca de forma, e isso continua sendo a
decisao. Esta e a TERCEIRA peca do braco de dez cenas (s015, s016, esta), mesmo
esqueleto e piso polones, porque o aprendizado 693 mediu CV 0,66 DENTRO do mesmo
tratamento e canal — epomeno 218-445, kolejny 96-462, labtreinamento 41-162 — e
com esse CV sao ~7 pecas por braco para enxergar um DOBRO, 28 para 50% e ~109
para 25%. Comecar um quarto braco agora deixaria todos com n pequeno.
NUMERO DE PARTIDA: braco de dez cenas com n=2. Esta e a terceira.

O QUE EU NAO RELI nesta rodada, de proposito: inscrito e view DE CANAL. A ultima
leitura valida foi as 14:09 e o aprendizado 686 diz que `channels.list` devolve
statistics byte a byte identicas dentro de ~1 h. Comparar so com >= ~4 h.

DE ONDE SAI, e isto resolveu um problema de processo: longo `Xgt32iH8Ft8`
(pacote `kp-plan-9233-20260811`, de 11/08), o plano completo para a pensao media.
O pacote e ANTERIOR a convencao de nome atual e NAO tem spec em
`fabrica/specs/` — nem por nome de arquivo nem por conteudo. Os capitulos foram
lidos da DESCRICAO PUBLICADA, pela `videos.list`, e sao: poduszka
bezpieczenstwa, dlugi pod kontrola, oszczednosci kontra inflacja, dlugi
horyzont, plan na jednej kartce.
REGISTRADO PARA A PROXIMA VEZ: origem livre pode nao ter spec local; a descricao
publicada e a fonte de capitulos nesse caso, e nao e motivo para trocar de
origem.

FAMILIA DIFERENTE das duas pecas de hoje no mesmo canal, como a regra (f) exige:
o `s015` era LIMIAR (aritmetica de faixa), o `s016` era COMPOSICAO (duas metades
da fatura), e esta e ORDEM — a entrada errada nao e a quantia de cada filar, e a
SEQUENCIA deles. Quem comeca pelo horizonte longo ou pela divida antes do bufor
volta ao zero na primeira avaria, e isso nao depende de nenhum numero do mundo.

TITULO EM PERGUNTA, a forma do PL/26.
FEED PL NAO RELIDO — lido as 11:1x, dentro da janela do 623.

IDENTIDADE: faixa ATUAL do canal `{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841,
bg #F4F1EA}`, trilha `Wholesome` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita a pensao
# media, nao cita inflacao, nao cita stopa referencyjna, nao cita oprocentowanie
# de obligacje, nao cita quantos meses de bufor e nao nomeia instrumento.
# Conferido A MAO campo por campo, porque o portao `narracao` conta QUANTIDADES
# por frase e NAO pega digito cru.
#
# A REGRA (g) MANDA, e a propria descricao do longo prova: ela esta cheia de
# numeros com data colada — "II kwartal 2026", "sierpien 2026", "najnizej od
# czterech lat". Todos envelhecem por ato do GUS, do NBP ou do Ministerio. O que
# NAO envelhece e a ORDEM dos filares, que e metodo.
#
# NUMERAIS NA NARRACAO: apenas ORDINAIS de metodo — "najpierw", "pierwszy",
# "ostatnie". Descrevem a sequencia, nao um valor do mundo. Uma quantidade por
# frase; o limite do portao e tres.
#
# O QUE O VIDEO AFIRMA: que a ordem dos filares importa mais que a quantia de
# cada um; que sem bufor uma avaria devolve a pessoa a divida; que a divida mais
# cara sai primeiro; e que o horizonte longo e o ultimo e nao o primeiro. Tudo
# isto esta nos capitulos "Filar 1: poduszka bezpieczenstwa", "Filar 2: dlugi pod
# kontrola" e "Filar 4: dlugi horyzont" do longo `Xgt32iH8Ft8`.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) a pensao media bruta e na mao — numero do GUS com trimestre colado;
#   (2) inflacao, stopa referencyjna e o oprocentowanie das obligacje, que o
#       proprio longo datou em agosto de 2026;
#   (3) quantos meses de bufor e qual instrumento usar — o primeiro varia com a
#       estabilidade da renda e o segundo e recomendacao, nao metodo.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Masz plan", "sub": "i wciąż nie masz poduszki", "nar": "Masz rozpisany plan na pensję, a wciąż bez poduszki.", "sem_cap": True},
    {"layout": "item", "kicker": "Problem", "preco": "nie w kwocie", "nar": "Kolejność kroków jest ważniejsza niż kwota.", "sem_cap": True},
    {"layout": "item", "kicker": "Najpierw", "preco": "bufor", "nar": "Najpierw bufor na awarie, potem wszystko inne.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Bez bufora", "sub": "plan się rozsypie", "nar": "Bo bez bufora każdy taki plan się rozsypie.", "sem_cap": True},
    {"layout": "item", "kicker": "Awaria", "preco": "wraca dług", "nar": "Jedna awaria w domu i wracasz do długu.", "sem_cap": True},
    {"layout": "item", "kicker": "I wtedy", "preco": "od zera", "nar": "I wtedy całe oszczędzanie zaczynasz od zera.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Dopiero potem", "sub": "bierzesz się za długi", "nar": "Dopiero po buforze bierzesz się za długi.", "sem_cap": True},
    {"layout": "item", "kicker": "Zasada", "preco": "najdroższy pierwszy", "nar": "Najdroższy dług schodzi tu pierwszy.", "sem_cap": True},
    {"layout": "item", "kicker": "Inwestowanie", "preco": "na końcu", "nar": "A inwestowanie jest ostatnie, nie pierwsze.", "sem_cap": True},
    {"layout": "cta", "kicker": "Zasubskrybuj", "sub": "na następne", "nar": "To kolejność robi robotę. Zasubskrybuj.", "sem_cap": True}
]

THUMB = {"l1": "Kolejność", "l2": "nie kwota"}

COPY = """# kolejny-poziom-s017

## TITULO
Kolejność Filarów, Nie Kwoty: Dlaczego Plan Na Pensję Rozsypuje Się Przy Pierwszej Awarii

## TITULO SHORT
Od czego zacząć z pensją?

## DESCRICAO
Prawie każdy plan na pensję wygląda tak samo: tyle na życie, tyle na oszczędności, tyle na przyszłość. I prawie każdy rozsypuje się w tym samym miejscu — przy pierwszej awarii, bo zaczął od złej strony.

Rzecz, która decyduje, nie jest w kwotach. Jest w **kolejności**. Dopóki nie ma buforu, każda nieprzewidziana rzecz wraca długiem, a oszczędzanie zaczyna się od zera — i tak w kółko, niezależnie od tego, ile odkładasz miesięcznie.

Dlatego bufor jest pierwszy, nie drugi i nie trzeci. Dopiero po nim ma sens brać się za długi, a wśród długów pierwszy schodzi ten najdroższy, bo on rośnie najszybciej. Inwestowanie i długi horyzont są na końcu tej listy nie dlatego, że są mniej ważne, ale dlatego, że bez dwóch poprzednich kroków zostaną przerwane w najgorszym momencie.

To jest cała metoda i ona nie starzeje się razem z liczbami. Ten short świadomie nie podaje ani średniej pensji, ani inflacji, ani stopy referencyjnej, ani oprocentowania obligacji — te liczby zmieniają się co kwartał i są w pełnym filmie razem z datą i źródłem. Nie podaje też, ile dokładnie miesięcy ma mieć bufor, bo to zależy od stabilności twojego dochodu.

Pełny plan — cztery filary, trzy koszyki, konkretne liczby i automat, który tego pilnuje — jest w filmie na kanale.

## COMENTARIO FIXADO
Najczęstszy błąd nie jest w kwotach, jest w kolejności: ludzie zaczynają od inwestowania albo od spłaty, a bufor zostawiają na koniec. I wtedy pierwsza awaria wraca długiem, a oszczędzanie startuje od zera — niezależnie od tego, ile odkładali. Dlatego bufor jest pierwszy, potem długi (najdroższy schodzi pierwszy, bo rośnie najszybciej), a długi horyzont jest ostatni. Żeby było jasno, bo film tego nie mówi: inwestowanie nie jest złe ani mniej ważne — jest po prostu kruche, dopóki nie ma czym złapać awarii. Celowo nie ma tu ani jednej liczby: średnia pensja, inflacja i oprocentowanie zmieniają się co kwartał, a kolejność nie. Napiszcie w komentarzach tylko, od którego filaru zaczynaliście — bez kwot.

## HASHTAGS
#Finanse #Oszczedzanie #KolejnyPoziom

## TAGS
kolejnosc filarow, poduszka bezpieczenstwa, plan na pensje, splata dlugow, najdrozszy dlug pierwszy, budzet domowy, oszczedzanie od zera, finanse osobiste, dlugi horyzont, od czego zaczac oszczedzanie, bufor finansowy, kolejny poziom, plan finansowy, awaria i dlug, metoda a nie liczby

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita pensao
media, inflacao, stopa referencyjna, oprocentowanie de obligacje, quantos meses
de bufor, nem nomeia instrumento. Conferido a mao campo por campo.

A REGRA (g) MANDA, e a descricao do proprio longo prova: ela traz "II kwartal
2026", "sierpien 2026" e "najnizej od czterech lat" — numeros com data colada,
que envelhecem por ato do GUS, do NBP ou do Ministerio. O que nao envelhece e a
ORDEM dos filares, e e ela que este short carrega.

NUMERAIS NA NARRACAO: apenas ordinais de metodo — "najpierw", "pierwszy",
"ostatnie".

O QUE O VIDEO AFIRMA: que a ordem importa mais que a quantia; que sem bufor uma
avaria devolve a pessoa a divida; que a divida mais cara sai primeiro; e que o
horizonte longo e o ultimo. Esta nos capitulos "Filar 1", "Filar 2" e "Filar 4"
do longo `Xgt32iH8Ft8` (kp-plan-9233-20260811).

DESCARTADO, e vai escrito:
  (1) a pensao media bruta e na mao, numero do GUS com trimestre colado;
  (2) inflacao, stopa referencyjna e oprocentowanie das obligacje, datados de
      agosto de 2026 no proprio longo;
  (3) quantos meses de bufor e qual instrumento — o primeiro varia com a renda,
      o segundo e recomendacao e nao metodo.

## FONTES
O longo de onde este short foi extraido (kp-plan-9233-20260811, Xgt32iH8Ft8) traz
as fontes oficiais — GUS, NBP, Ministerstwo Finansow — e as datas. Este short nao
introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s017",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "Xgt32iH8Ft8",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short, alvo_short
    import legenda as LG
    import variedade
    grava(SPEC, "fabrica/specs/kolejny-poziom-s017.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} | PISO no pl")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto "
          f"{s*1.004:.1f} a {s*1.044:.1f}")
    print(f"por plano: {s/len(SHORT):.2f}s | falas de legenda: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
