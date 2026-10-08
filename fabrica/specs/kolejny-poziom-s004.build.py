"""kolejny-poziom-s004 — a rodada em que o meu "teto" virou distribuicao.

ALAVANCA: A (alcance por short). Decimo short solto, quarto do kolejny.

O QUE DEU CERTO: o short solto, nove publicados em dois dias, e a ponte, que
fechou nove vezes seguidas sem falha.
O QUE NAO DEU: a minha previsao do 643, e ela caiu com clareza. Eu disse que o
kolejny-015 e o 019, a 47-59 views/hora, cruzariam 1.100 em ~14 h. Serie real do
019: 4 -> 283 -> 330 -> 330 -> 330 -> 330. QUATRO leituras horarias identicas: ele
saturou em 330. O 015 foi 133 -> 396 -> 455 -> 455 -> 481 -> 491, subindo mas
DESACELERANDO.
O QUE VOU MUDAR, e e conceito e nao numero: **nao existe teto de 1.150.** Existe
uma RAJADA POR PECA cujo tamanho varia por uma ordem de grandeza (330, 491, 884,
1.132, 1.155) e que decai em ~um dia. Os 1.155 eram o TOPO DA AMOSTRA, e eu
confundi maximo observado com lei. A conta dos tres milhoes muda de FORMA: quem
decide e a MEDIANA da rajada, nao um teto. Com mediana de 300 a 500, 1.890 shorts
em noventa dias dao de 567 mil a 945 mil — segue fora de alcance, e a alavanca
segue sendo a CONCLUSAO, que e o que determina o tamanho da rajada. Aprendizado
646; corrige o 643 e refina o 636 e o 642.

POR QUE O KOLEJNY: o epomeno esta sem longo livre (os cinco usados) e o proximo
la pede pacote, cujo ritmo e um a cada dois dias. O labtreinamento foi AUDITADO
nesta rodada e tem DOZE longos livres, mas e o pior em alcance por uma ordem de
grandeza (149 e 29). O kolejny e o segundo em alcance e tem tres livres.

NUMERO DE PARTIDA: 113 do short irmao do mesmo longo (`o5TKvVRzJ_Q`, +75 em 16 h)
e 884 do melhor solto do canal. A mediana da rajada do canal esta entre 330 e 491.

A FORMA, e NAO e experimento novo (secao 5-d): o gancho do epomeno-s002, o melhor
da frota — ENTRADA ERRADA INVALIDA O TEU NUMERO. Aqui a entrada errada e o
HORIZONTE: quem pretende amortizar antes do fim nao decide pela soma ate a ultima
prestacao. Gancho visual segue cartao de texto nas cinco cenas, para nao sujar o
experimento 33, e o 644 lembra que o video abre com dois quadros pretos mais
fade-in, cujo teste tambem espera o 33 fechar.

DE ONDE SAI: do longo JA PUBLICADO `QiaGg03WSR0` (kolejny-poziom-018). O short
original dele ensina que prestacao menor nao e custo menor, e soma tudo ate a
ultima prestacao. Este ataca o capitulo "Czego ten rachunek nie rozstrzyga": a
soma ate o fim so decide para quem vai ate o fim. Quem planeja fechar antes
compara os juros ATE O MES DO FECHAMENTO, e a oferta mais barata no total pode
ser a mais cara nesse horizonte.

IDENTIDADE: faixa conferida em SETE pacotes do canal, todos identicos — paleta
`{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841, bg #F4F1EA}`, trilha `Wholesome`, voz
`pl-PL-MarekNeural`. O 017 segue fora da faixa, de proposito.

TENDENCIA: o feed PL/26 NAO foi lido nesta rodada, e digo em vez de inventar. A
26 e PROXY (a real e a 27, sem chart em regiao nenhuma, 610) e o chart repete
catorze de quinze itens em quatro horas (623). A evidencia mais forte e a medicao
da propria frota, de minutos antes: declaro a troca.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita taxa, nao cita prestacao, nao cita
# valor de credito, nao cita percentual e nao nomeia banco nem orgao. Os unicos
# numeros ditos sao "duas" (duas ofertas) e "ultima" (ultima prestacao), e sao
# referencia de posicao na propria conta.
#
# O QUE O VIDEO AFIRMA: que juros que nao chegam a ser pagos nao entram no custo,
# e que por isso quem fecha o credito antes do fim deve comparar os juros ate o
# mes do fechamento. Isso e aritmetica e esta no longo `QiaGg03WSR0` com as
# fontes.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) se, quando e quanto o banco polones pode cobrar por amortizacao
#       antecipada — NAO reconferido hoje em duas fontes; o short NAO afirma que
#       e gratuito e manda conferir no contrato;
#   (2) qualquer taxa, prestacao ou valor;
#   (3) o que a conta NAO decide — esta no longo, e o short manda para la.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Spłacisz wcześniej?", "sub": "suma nic nie mówi",
     "nar": "Zamierzasz spłacić wcześniej? Wtedy suma do ostatniej raty nic ci "
            "nie mówi.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Niezapłacone", "sub": "to nie koszt",
     "nar": "Odsetki, których nie zapłacisz, nie są twoim kosztem. Liczy się "
            "to, co oddasz do dnia zamknięcia.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Do twojego miesiąca", "sub": "nie do końca",
     "nar": "Weź harmonogram i zsumuj odsetki tylko do miesiąca, w którym "
            "planujesz zamknąć.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Zrób to dwa razy", "sub": "obie oferty",
     "nar": "Zrób to dla obu ofert. Tańsza do końca potrafi być droższa do "
            "tego miesiąca.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "I sprawdź umowę", "sub": "koszt nadpłaty",
     "nar": "Sprawdź też, co umowa mówi o nadpłacie. Cały rachunek jest w "
            "filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Spłacisz wcześniej?", "l2": "suma nic nie mówi"}

COPY = """# kolejny-poziom-s004

## TITULO
Spłacisz Kredyt Wcześniej? Wtedy Suma do Ostatniej Raty Nie Jest Twoim Kosztem

## TITULO SHORT
Spłacisz wcześniej? Suma nic nie mówi

## DESCRICAO
Porównanie dwóch ofert kredytu robi się na KOSZCIE, nie na racie: suma wszystkiego, co oddasz, minus kwota kredytu. Niższa rata potrafi oznaczać większą sumę, bo niższa rata zwykle znaczy dłuższy czas albo inny sposób naliczania. To jest pierwszy krok i on zostaje.

Ale ten rachunek ma założenie, o którym prawie nikt nie mówi: że pójdziesz do OSTATNIEJ raty. Jeżeli planujesz nadpłacić i zamknąć kredyt wcześniej — po trzech latach, po pięciu, kiedykolwiek — to suma do końca opisuje scenariusz, który nie nastąpi. Odsetki, do których nigdy nie dojdziesz, nie są twoim kosztem. Koszt to to, co faktycznie oddasz do dnia zamknięcia.

Uczciwa wersja jest tak samo prosta jak pierwsza. Weź harmonogram spłat każdej z ofert. Znajdź miesiąc, w którym realistycznie planujesz zamknąć. Zsumuj część odsetkową od pierwszej raty do tego miesiąca — i to te dwie liczby porównujesz ze sobą. Wynik potrafi się odwrócić: oferta tańsza w sumie do końca bywa droższa w horyzoncie, który naprawdę cię dotyczy, bo w wariancie o wyższym oprocentowaniu i krótszym czasie odsetki są skoncentrowane na początku.

Zostaje jedna rzecz do sprawdzenia w umowie, i nie zgaduj jej: zasady nadpłaty. Sprawdź, czy i w jakim okresie przewidziana jest prowizja za przedterminową spłatę, i czy nadpłata skraca czas, czy zmniejsza ratę — bo to dwa różne skutki i tylko pierwszy obniża odsetki wyraźnie.

Tutaj nie podaję żadnego oprocentowania, żadnej raty i żadnej kwoty: liczby, które decydują, są w twoich dwóch harmonogramach i w twojej umowie. Pełny rachunek, oba warianty naliczania, miejsce gdzie to przeczytać i to, czego ten rachunek NIE rozstrzyga, są w filmie.

## COMENTARIO FIXADO
Dwa kroki. Pierwszy: porównuj KOSZT, nie ratę — suma wszystkiego minus kwota kredytu. Drugi, ten pomijany: ta suma zakłada, że dojdziesz do ostatniej raty. Jeśli planujesz nadpłacić, zsumuj odsetki tylko do miesiąca, w którym zamykasz, i porównaj te dwie liczby — wynik potrafi się odwrócić, bo przy krótszym czasie odsetki są skoncentrowane na początku. I sprawdź w umowie zasady nadpłaty: czy jest prowizja i czy nadpłata skraca okres, czy obniża ratę. Jeśli policzysz, napisz, czy wynik się odwrócił — bez podawania kwot.

## HASHTAGS
#Kredyt #Nadpłata #KolejnyPoziom

## TAGS
kredyt, nadplata, przedterminowa splata, odsetki, harmonogram splat, koszt kredytu, rata, dwie oferty, finanse osobiste, polska, obliczenia, umowa kredytowa, kolejny poziom, porownanie ofert, prowizja

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
ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita taxa, nao cita prestacao, nao cita valor
de credito, nao cita percentual e nao nomeia banco nem orgao. Os unicos numeros
ditos sao "duas" e "ultima", e sao referencia de posicao na propria conta.

O QUE O VIDEO AFIRMA: que juros que nao chegam a ser pagos nao entram no custo, e
que por isso quem fecha o credito antes do fim compara os juros ate o mes do
fechamento. E aritmetica e esta no longo kolejny-poziom-018 (QiaGg03WSR0) com as
fontes.

DESCARTADO, e vai escrito:
  (1) se, quando e quanto o banco polones pode cobrar por amortizacao antecipada
      — NAO reconferido hoje em duas fontes; o short NAO afirma que e gratuito e
      manda conferir no contrato;
  (2) qualquer taxa, prestacao ou valor;
  (3) o que a conta NAO decide — esta no longo, e o short manda para la.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-018, QiaGg03WSR0) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s004",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "QiaGg03WSR0",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/kolejny-poziom-s004.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, mira 33-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
