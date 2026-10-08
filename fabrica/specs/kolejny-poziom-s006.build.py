"""kolejny-poziom-s006 — o ultimo longo de origem livre da frota.

ALAVANCA: A (alcance por short). Decimo segundo short solto, sexto do kolejny.

O QUE DEU CERTO: a ponte, doze vezes seguidas, e a primeira janela de medicao
acima de 24 h — na verdade 101 h — que finalmente deu prova LIMPA de parada:
`p1uvroDdKvg` 154 -> 154 em 101,00 h, e `lCXwLaqUHJI` 0 -> 0 em 101,00 h, ou
seja um short que recebeu ZERO views em quatro dias. Aprendizado 648.
O QUE ISSO CORRIGE na minha propria rotina: o piso de 24 h do 647 esta certo mas
e GENEROSO. Para dizer que UMA peca parou, prefira 72 h ou mais.
O QUE A DISTRIBUICAO DIZ AGORA: rajada por peca = 0, 154, 285, 356, 498, 884,
1.132, 1.155 — mediana ~420. Nao existe teto comum; existe rajada por peca que
varia por mais de uma ordem de grandeza, e existe peca que nao recebe nada.
A projecao honesta com essa mediana: ~794 mil views em 90 dias contra 3 milhoes
exigidos pela PORTA 1. O gargalo e alcance por peca, nao volume de peca.

POR QUE O KOLEJNY, e e a ULTIMA vez que esta escolha e facil: `nPyVHJmY2HA`
(kolejny-poziom-015) e o ULTIMO longo de origem livre da frota inteira. O epomeno
esta em zero livre; o labtreinamento tem doze livres mas e pior em alcance por
uma ordem de grandeza (149 e 29). Depois deste short a frota so tem SEGUNDO
ANGULO ou PACOTE COMPLETO, e essa escolha vai com o dado na frente — nao por
preferencia de canal. NUMERO DE PARTIDA: mediana da rajada do canal entre 356 e
498; melhor solto do canal, 884.

A FORMA, e NAO e experimento novo (secao 5-d): o gancho do epomeno-s002, o melhor
da frota — ENTRADA ERRADA INVALIDA O TEU NUMERO. Aqui a entrada errada e a LINHA
DA SKLADKA no pasko: ela nao e o que saiu do bolso, porque a contribuicao baixa a
base do imposto. Gancho visual segue cartao de texto nas cinco cenas, para nao
sujar o experimento 33 — e os TRES testes que o 33 trava (b-roll na cena 1, short
de 22-26 s, matar o fade-in de dois quadros pretos do 644) seguem esperando.

DE ONDE SAI: do longo JA PUBLICADO `nPyVHJmY2HA` (kolejny-poziom-015). O short
original daquele longo (`u-vIsXaKjcM`) pergunta "ile to realnie?" e manda para o
longo. Este ataca coisa diferente e mais estreita: a CONFUSAO entre a linha da
contribuicao e o custo real, e o procedimento de dois paskos que resolve. Nao
toca na data de reinscricao nem em percentual nenhum.

IDENTIDADE: faixa conferida em SETE pacotes do canal, todos identicos — paleta
`{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841, bg #F4F1EA}`, trilha `Wholesome`, voz
`pl-PL-MarekNeural`. O 017 segue fora da faixa, de proposito.

TENDENCIA: o feed PL/26 NAO foi lido nesta rodada, e digo em vez de inventar. A
26 e PROXY (a real e a 27, sem chart, 610) e o chart repete catorze de quinze
itens em quatro horas (623). A evidencia mais forte e a medicao da propria frota,
e nesta rodada ela ficou mais forte do que nunca: 101 h de janela.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita percentual de contribuicao, nao cita
# aliquota, nao cita valor, nao cita data de reinscricao e nao nomeia instituicao.
# Os unicos numeros ditos sao "dwa" e "jeden", e sao a aritmetica do procedimento.
#
# O QUE O VIDEO AFIRMA: que a contribuicao do empregado baixa a base sobre a qual
# o imposto e calculado, e que por isso a linha da contribuicao no pasko e MAIOR
# do que o que realmente saiu da wyplata. Isso esta no longo `nPyVHJmY2HA` com as
# fontes, e o short nao acrescenta grandeza nenhuma.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) a data de reinscricao automatica e o fato de a rezygnacja expirar — e
#       afirmacao juridica com data, NAO reconferida hoje em duas fontes; fica no
#       longo, que tem as fontes;
#   (2) qualquer percentual, aliquota, valor ou nome de instituicao;
#   (3) o lado do BENEFICIO — contribuicao do empregador, aporte do Estado e
#       rendimento — que e real e esta FORA desta conta; o longo diz isso, e o
#       short manda para la em vez de insinuar que a conta decide ficar ou sair.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Linia składki?", "sub": "to nie twój koszt",
     "nar": "Patrzysz na linię składki PPK na pasku? To nie jest to, co ubyło "
            "ci z wypłaty.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Składka obniża", "sub": "podstawę podatku",
     "nar": "Składka obniża podstawę podatku, więc część wraca do ciebie "
            "niższym podatkiem.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Dwa paski", "sub": "jeden bez składki",
     "nar": "Weź dwa paski: jeden ze składką, jeden bez niej. Pomiń miesiące "
            "z premią.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Odejmij wypłaty", "sub": "nie brutto",
     "nar": "Od wypłaty bez składki odejmij wypłatę ze składką. Ta różnica to "
            "twój realny koszt.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Policz dziś", "sub": "złote na miesiąc",
     "nar": "Policz to dziś, w złotych na miesiąc. Cały rachunek jest w filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Linia składki", "l2": "to nie koszt"}

COPY = """# kolejny-poziom-s006

## TITULO
Linia Składki PPK na Pasku Nie Jest Twoim Kosztem: Policz Różnicę Dwóch Wypłat

## TITULO SHORT
Linia składki to nie twój koszt

## DESCRICAO
Na pasku wypłaty linia składki PPK stoi wprost, w złotych, i prawie każdy czyta ją jako swój koszt. Nie jest nim. Składka zmienia podstawę, od której liczy się podatek, więc część tego, co wpłacasz, wraca do ciebie niższym podatkiem — i to, co realnie ubyło z twojej wypłaty, jest mniejsze niż ta linia. Decyduje ta druga liczba, bo to ona wychodzi z konta.

Problem jest w tym, że tej drugiej liczby nie ma w żadnej linii paska. Trzeba ją zmierzyć, a nie odczytać. Procedura ma dwa kroki i żadnej mojej liczby. Krok pierwszy: weź dwa paski — jeden z miesiąca ze składką PPK i jeden z miesiąca bez niej, możliwie blisko siebie, pomijając miesiące z premią, nagrodą, wyrównaniem czy trzynastką, bo one zmieniają sumę i zepsują pomiar. Krok drugi: od kwoty do wypłaty z miesiąca bez składki odejmij kwotę do wypłaty z miesiąca ze składką — do wypłaty, nie brutto. Ta różnica to twój realny koszt w złotych na miesiąc.

Potem porównaj ją z linią składki. Będzie mniejsza, i to dokładnie o tyle, ile oddał ci podatek. Odległość między tymi dwiema liczbami jest całą informacją, którą ten pomiar daje — i jest to informacja o twoim pasku, nie o programie.

Zastrzeżenie waży tu więcej niż sam rachunek: ta liczba NIE mówi, czy zostać, czy zrezygnować. Składka pracodawcy, wpłaty od państwa i to, co urośnie, są realne i są poza tym rachunkiem — on mierzy wyłącznie twój koszt, jedną stronę. Nie ma tu żadnego procentu, żadnej stawki podatku i żadnej daty: liczby, które decydują, są na twoich dwóch paskach. Pełny rachunek, co ta liczba przemilcza, trzy błędy pomiaru i decyzja, która wraca sama — są w filmie.

## COMENTARIO FIXADO
Pomiar: weź dwa paski, jeden ze składką PPK i jeden bez, blisko siebie i bez premii ani trzynastki. Od kwoty DO WYPŁATY bez składki odejmij kwotę DO WYPŁATY ze składką — nie brutto. Różnica to twój realny koszt w złotych na miesiąc, i jest mniejsza od linii składki, bo składka obniża podstawę podatku. Ta liczba mierzy jedną stronę: składka pracodawcy, wpłaty od państwa i zyski są realne i są poza nią, więc nie rozstrzyga, czy zostać. Jeśli policzysz, napisz samą różnicę między linią składki a realnym kosztem — bez pensji i bez pracodawcy.

## HASHTAGS
#PPK #Wyplata #KolejnyPoziom

## TAGS
ppk, skladka ppk, realny koszt, pasek wyplaty, kwota do wyplaty, podstawa opodatkowania, podatek, dwa paski, finanse osobiste, polska, obliczenia, wyplata, kolejny poziom, zlote na miesiac, jak czytac pasek

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
ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita percentual de contribuicao, nao cita
aliquota, nao cita valor, nao cita data de reinscricao e nao nomeia instituicao.
Os unicos numeros ditos sao "dwa" e "jeden", e sao a aritmetica do procedimento.

O QUE O VIDEO AFIRMA: que a contribuicao do empregado baixa a base sobre a qual o
imposto e calculado, e que por isso a linha da contribuicao no pasko e MAIOR do
que o que realmente saiu da wyplata. Esta no longo kolejny-poziom-015
(nPyVHJmY2HA) com as fontes.

DESCARTADO, e vai escrito:
  (1) a data de reinscricao automatica e o fato de a rezygnacja expirar — e
      afirmacao juridica com data, NAO reconferida hoje em duas fontes; fica no
      longo;
  (2) qualquer percentual, aliquota, valor ou nome de instituicao;
  (3) o lado do BENEFICIO — contribuicao do empregador, aporte do Estado e
      rendimento — que e real e esta FORA desta conta; o short manda para o longo
      em vez de insinuar que a conta decide ficar ou sair.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-015, nPyVHJmY2HA) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s006",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "nPyVHJmY2HA",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/kolejny-poziom-s006.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, mira 33-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
