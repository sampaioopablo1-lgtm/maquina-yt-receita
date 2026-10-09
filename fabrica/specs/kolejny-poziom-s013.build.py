"""kolejny-poziom-s013 — quanto te custa NAO fazer nada?

ALAVANCA: setimo ponto do 38, terceiro no piso da faixa com a voz de pior caso.
Os tres pontos em pl deram +4,4%, +3,5% e −0,9%, logo o piso continua sendo a
escolha certa — nao por vies conhecido, mas pela dispersao de ~5 pontos (679).
Quarta peca com titulo em PERGUNTA, e aqui a forma e do CANAL: o PL/26 e o unico
dos tres feeds em que a pergunta domina (seis de quinze, contra dois a tres no BR
e no GR).

O QUE DEU CERTO: primeira rodada da noite em que as TRES leituras concordaram em
TODAS as pecas (min igual a max em todas as quinze). A discordancia de replica do
680 nao e constante, e isso e bom saber antes de culpar a API por tudo.
Com mediana de tres: `epomeno-s011` 303 as 5,7 h, `kolejny-s011` 256 as 4,8 h,
`epomeno-s012` 221 as 3,9 h.

O QUE NAO DEU, e e o candidato a pior do dia: `labtreinamento-s008` tem **9 views
as 5,5 h**. O par dele no mesmo canal, o s007, fez 144 as 9,9 h. NAO concluo
nada: as idades diferem (5,5 contra 9,9) e nenhuma das duas passou dos 12 h que a
rotina exige para COMPARAR. Mas registro a suspeita, porque ela tem candidato:
as cinco origens livres do labtreinamento sao todas conformidade corporativa, e o
651 mediu esse perfil como ~30x pior. Se o s008 continuar nesse patamar as 12 h,
e a terceira confirmacao do 651 e muda o calendario do canal.

O QUE VOU MUDAR: uma coisa so — nada na peca. A mudanca desta rodada e de MEDICAO:
passo a tirar as tres leituras na MESMA chamada de rodada e a reportar a mediana
com a faixa ao lado, sempre, inclusive na linha de movimento. Foi o que faltou
quatro vezes hoje.
NUMERO DE PARTIDA: 69 views do short do pacote de origem; 459 do melhor solto do
canal as 11,9 h, tres leituras concordantes.

DE ONDE SAI: longo `wb1RGIx7OJI` (kolejny-poziom-009, o seguro obrigatorio mais
barato em dois anos), capitulo "Piec wierszy | i decyzja robi sie sama", QUARTA
linha: a diferenca entre a melhor oferta de hoje e a proposta de renovacao da
propria seguradora — "to sa pieniadze, ktore kosztuje cie nierobienie niczego".
O short ORIGINAL do pacote cita as tres medias de mercado e manda conferir a data
de fim da apolice; nao faz a conta da quarta linha nem menciona a armadilha.

FAMILIA, regra (f): hoje no kolejny sairam "qual dos dois efeitos a sua acao tem"
(s011) e "o numero que o outro lado ve nao e o que voce disse" (s012). Esta e
"nao fazer nada tem preco, e da para calcular". Tres entradas erradas diferentes.

IDENTIDADE: faixa ATUAL do canal `{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841,
bg #F4F1EA}`, trilha `Wholesome` (601).

TENDENCIA: o PL/26 foi lido as 01:1x e NAO foi relido — o chart repete 14 de 15
em quatro horas, e em 09/10 eu confirmei isso num intervalo de 4,5 h no BR/26.
Cinco horas depois ja estaria no limite; digo que nao reli em vez de fingir.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita a media de
# premio, nao cita a media de sinistro, nao cita os percentuais de variacao, nao
# cita "mais barato em dois anos" e nao nomeia orgao nem associacao. Conferido A
# MAO campo por campo, porque o portao `narracao` conta QUANTIDADES por frase e
# NAO pega digito cru.
#
# A REGRA (g) MANDA: todas essas sao estatisticas de mercado de um trimestre. Um
# short que diz "mais barato em dois anos" fica errado no trimestre seguinte e
# continua no ar — e o proprio longo trata essa frase como AVISO sobre o passado,
# nao promessa. O short fica com o METODO, que nao envelhece.
#
# UNICO NUMERAL NA NARRACAO: "trzy liczby" (tres numeros), que e o tamanho da
# receita. Uma quantidade na frase; o limite do portao e tres.
#
# O QUE O VIDEO AFIRMA: que a apolice obrigatoria se renova sozinha; que a
# diferenca entre a melhor oferta obtida hoje e a proposta de renovacao da
# seguradora atual e o custo monetario de nao fazer nada; e que no obrigatorio o
# AMBITO e legal e identico entre seguradoras, mas a forma de liquidar o sinistro
# nao e — logo a posicao mais barata da lista nao e automaticamente a escolha.
# Esta no longo kolejny-poziom-009 (`wb1RGIx7OJI`), capitulos "Piec wierszy" e
# "Czego NIE robic".
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) media de premio, media de sinistro e os percentuais — trimestrais;
#   (2) o resultado tecnico do ramo, que e do periodo e vem de supervisao;
#   (3) a faixa de economia tipica em zlotys, que esta no longo e depende do
#       perfil do condutor.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Wznawia się sama", "sub": "i to ma cenę",
     "nar": "Twoja polisa wznawia się sama, i ta wygoda ma cenę. Umiesz ją "
            "policzyć?",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Trzy liczby", "sub": "wszystkie twoje",
     "nar": "Weź trzy liczby: ile zapłaciłeś rok temu, najlepszą ofertę jaką "
            "dostajesz dzisiaj, i kwotę, którą proponuje twoja obecna firma.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Odejmij", "sub": "to jest cena bezwładu",
     "nar": "Odejmij ofertę od propozycji wznowienia. To, co zostaje, są "
            "pieniądze, które kosztuje cię nierobienie niczego.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Ale uwaga", "sub": "nie bierz najtańszej",
     "nar": "I nie bierz automatycznie najtańszej pozycji z listy. Zakres jest "
            "ustawowy, ale sposób likwidacji szkody już nie.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Subskrybuj", "sub": "na kolejne",
     "nar": "Sprawdź dziś datę końca polisy i wpisz ją w kalendarz. Subskrybuj, a "
            "cała tabela jest w filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Nierobienie", "l2": "ma cenę"}

COPY = """# kolejny-poziom-s013

## TITULO
Cena Bezwładu: Jak Policzyć, Ile Kosztuje Cię Automatyczne Wznowienie Polisy

## TITULO SHORT
Ile kosztuje cię nierobienie niczego?

## DESCRICAO
Obowiązkowa polisa ma jedną właściwość, która działa przeciwko tobie, choć wygląda jak udogodnienie: wznawia się sama. Nie musisz nic robić, i właśnie dlatego większość kierowców nic nie robi — a kwota wznowienia wygrywa przez bezwład, nie przez porównanie.

Ta wygoda ma cenę i można ją policzyć dokładnie, trzema liczbami, z których dwie już masz. Pierwsza: ile zapłaciłeś rok temu — jest na polisie albo na wyciągu. Druga: najlepsza oferta, jaką dostajesz dzisiaj, po sprawdzeniu w co najmniej trzech miejscach. Trzecia: kwota, którą proponuje ci twoja obecna firma na wznowienie.

I teraz jedno odejmowanie, które jest całym sensem tego materiału: odejmij drugą liczbę od trzeciej. To, co zostaje, nie jest oszczędnością hipotetyczną ani obietnicą marketingową — to są pieniądze, które kosztuje cię nierobienie niczego, w tym jednym roku, na tej jednej pozycji budżetu. Za kwadrans pracy raz w roku.

Jest jedna rzecz, której robić nie warto, choć kusi: nie bierz automatycznie pierwszej, najtańszej pozycji z listy. W obowiązkowym ubezpieczeniu zakres jest ustawowy i rzeczywiście identyczny u wszystkich — ale to jest jedyny element, który jest identyczny. Różni się to, jak firma likwiduje szkodę: ile czeka się na oględziny, czy dostaniesz auto zastępcze, czy kosztorys liczą po częściach oryginalnych czy po zamiennikach. Tego nie widzisz w kolumnie z ceną, a zobaczysz dokładnie wtedy, kiedy będziesz tego potrzebować.

Nie ma tu żadnej średniej rynkowej ani statystyki, i to jest celowe: tamte liczby opisują miliony kierowców i zmieniają się co kwartał, a twoja tabela porównuje ciebie z tobą sprzed roku. Pełna tabela, piąty wiersz z datą do kalendarza, co właściwie dzieje się dziś na rynku i dlaczego to jest ostrzeżenie, a nie prezent — są w filmie.

## COMENTARIO FIXADO
Rachunek w jednym odejmowaniu, dla każdego kto chce to zrobić teraz: najlepsza oferta z dziś MINUS kwota wznowienia od twojej obecnej firmy. Wynik to cena bezwładu — pieniądze, które tracisz nie robiąc nic. Dwie uwagi, bo bez nich rachunek jest niekompletny. PIERWSZA: sprawdź w co najmniej trzech miejscach, bo jedna oferta nie jest rynkiem. DRUGA, i to jest pułapka: w obowiązkowym OC zakres jest ustawowy i identyczny, ale likwidacja szkody NIE jest — czas oględzin, auto zastępcze, części oryginalne czy zamienniki. Najtańsza pozycja z listy nie jest automatycznie najlepszym wyborem. Kto policzy, niech napisze w komentarzu tylko czy różnica wyszła większa czy mniejsza, niż się spodziewał — bez kwot.

## HASHTAGS
#OC #Ubezpieczenia #KolejnyPoziom

## TAGS
wznowienie polisy, cena bezwladu, porownanie ofert oc, ubezpieczenie obowiazkowe, likwidacja szkody, auto zastepcze, czesci zamienne, finanse osobiste, polska, jak policzyc, kalendarz polisy, oszczednosci, kolejny poziom, polisa samochodowa, trzy oferty

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita media de
premio, media de sinistro, percentuais de variacao nem "mais barato em dois
anos", e nao nomeia orgao nem associacao. Conferido a mao campo por campo.

A REGRA (g) MANDA: todas essas sao estatisticas de mercado de um trimestre, e o
proprio longo trata a frase "mais barato em dois anos" como AVISO sobre o passado
e nao promessa. O short fica com o METODO, que nao envelhece.

UNICO NUMERAL NA NARRACAO: "trzy liczby", o tamanho da receita.

O QUE O VIDEO AFIRMA: que a apolice obrigatoria se renova sozinha; que a
diferenca entre a melhor oferta de hoje e a proposta de renovacao da seguradora
atual e o custo de nao fazer nada; e que no obrigatorio o ambito e legal e
identico, mas a liquidacao do sinistro nao e — logo a posicao mais barata nao e
automaticamente a escolha. Esta no longo kolejny-poziom-009 (wb1RGIx7OJI),
capitulos "Piec wierszy" e "Czego NIE robic".

DESCARTADO, e vai escrito:
  (1) media de premio, media de sinistro e os percentuais — trimestrais;
  (2) o resultado tecnico do ramo, que e do periodo e vem de supervisao;
  (3) a faixa de economia tipica em zlotys, que depende do perfil do condutor.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-009, wb1RGIx7OJI) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s013",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "wb1RGIx7OJI",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short, alvo_short
    grava(SPEC, "fabrica/specs/kolejny-poziom-s013.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    INTERROGA = ("?", ";", ";")
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} (PISO: pl disperso ~5 pontos)")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto (pl) "
          f"{s*0.982:.1f} a {s*1.044:.1f} | teto 45")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo: {tit!r} ({len(tit)} chars) | pergunta? "
          f"{'SIM' if tit.rstrip().endswith(INTERROGA) else 'NAO'}")
    print(f"aponta para: {SPEC['longo_existente']}")
