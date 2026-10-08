"""kolejny-poziom-s007 — quase apontei para um dos 46 duplicados.

ALAVANCA: A (alcance por short). Decimo oitavo short solto, setimo do kolejny.

O QUE DEU CERTO: ir buscar a spec do longo antes de escrever a pauta. Foi isso
que pegou o erro abaixo antes de virar video no ar.

O QUE NAO DEU, e e meu, pela SEGUNDA vez em duas horas: as 11:11 eu listei na
rotina os "melhores longos livres do kolejny" — `_M8t8SPC_f0` (1.152),
`jDa9SM8A7os` (634), `qcY5XC1KtlQ` (594), `SZV9Vk5YFwI` (414), `5gHnniPl0f8`
(323). Ao abrir o primeiro, descobri que os CINCO sao copias do MESMO video: seis
longos com o titulo identico "Emerytura z ZUS: 34,4% pensji w 2050 roku", e cinco
shorts duplicados do mesmo conteudo. Sao exatamente as duplicatas que o
docs/duplicatas-a-apagar.md manda o dono remover, e que o 544 ja havia levantado.
As views que eu usei como proxy de qualidade eram as views dos cinco shorts
DUPLICADOS, espalhadas pelas copias.
O ESTRAGO QUE NAO ACONTECEU: o CTA deste short apontaria para um video marcado
para EXCLUSAO, e a pauta colidiria com cinco shorts ja publicados. A trava de
similaridade talvez pegasse o titulo; o CTA nao passa por trava nenhuma.
O DEFEITO E DO PROXY QUE EU ACABARA DE ESCREVER: "ordene os livres pelo alcance
do short ORIGINAL de cada pacote" PREMIA DUPLICATA, porque duplicata multiplica
pacotes com o mesmo conteudo. Decimo segundo defeito da familia "o instrumento
fabricou a conclusao". Aprendizado 658.

O QUE VOU MUDAR, e corrige o 655: a contagem de estoque passa a ser por TITULO
DISTINTO, excluindo o GRUPO duplicado inteiro — nao basta `row_number() = 1`,
porque a primeira copia tambem vai ser apagada. Conta honesta: epomeno 18 longos
/ 18 titulos, labtreinamento 13 / 13, kolejny 24 longos mas so DEZENOVE titulos.
Livres de verdade: epomeno 12, kolejny 13, labtreinamento 11 — TRINTA E SEIS, nao
quarenta e um.

DE ONDE SAI: `MjI4ZGJAhIo` (kolejny-poziom-007), o melhor livre LIMPO do canal
depois de excluir o grupo duplicado. NUMERO DE PARTIDA: 287 do short original
daquele pacote, e 884 do melhor solto do canal.
O short original (`7vqZHEzRP2A`) diz "a prestacao caiu? nao pare de amortizar".
Este ataca a comparacao que vem ANTES dessa decisao, e e puramente aritmetica:
quem compara a taxa do credito com o rendimento do investimento compara coisas
diferentes, porque o rendimento paga imposto e o juro que voce deixa de pagar
nao. A entrada certa e o rendimento LIQUIDO. Nenhum numero novo e dito — nem
taxa, nem aliquota, nem valor, e o imposto nao e nomeado.

IDENTIDADE: faixa do canal `{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841, bg #F4F1EA}`,
trilha `Wholesome`, voz `pl-PL-MarekNeural` — conferida em sete pacotes.

TENDENCIA: o feed PL/26 foi lido as 06:22 e NAO foi relido nesta rodada; digo em
vez de inventar. Do que ficou: pergunta ou imperativo em segunda pessoa, onze de
quinze. Cena 1 pergunta, cena 5 imperativo.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO. NAO cita taxa de credito, NAO cita rendimento,
# NAO cita aliquota de imposto, NAO cita valor, NAO cita prazo e NAO nomeia o
# imposto nem orgao nenhum. Nao ha numero dito na narracao.
#
# O QUE O VIDEO AFIRMA: que o rendimento de um investimento e tributado e que o
# juro que se deixa de pagar ao amortizar nao e, logo comparar a taxa do credito
# com o rendimento BRUTO compara grandezas diferentes. Isso esta no longo
# `MjI4ZGJAhIo` (kolejny-poziom-007) com as fontes, e a parte aritmetica e
# verificavel sem fonte nova.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) a aliquota do imposto sobre rendimento na Polonia e o nome do imposto —
#       estao no longo com fonte e NAO foram reconferidos hoje em duas fontes;
#   (2) qualquer taxa de credito, rendimento ou valor;
#   (3) se vale amortizar ou investir no caso de cada um — depende de prazo,
#       liquidez e risco, esta no longo, e o short manda para la em vez de dar
#       veredito.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Nadpłacać czy", "sub": "inwestować?",
     "nar": "Porównujesz oprocentowanie kredytu z zyskiem z inwestycji? To "
            "porównanie jest nierówne.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Zysk jest", "sub": "opodatkowany",
     "nar": "Od zysku z inwestycji płacisz podatek. Od odsetek, których nie "
            "zapłacisz, nie płacisz nic.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Odejmij podatek", "sub": "i wtedy porównaj",
     "nar": "Odejmij więc podatek od zysku, i dopiero ten wynik porównaj z "
            "oprocentowaniem kredytu.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Kolejność się", "sub": "potrafi odwrócić",
     "nar": "Po tej poprawce kolejność potrafi się odwrócić, i nadpłata "
            "wychodzi na lepsze.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Policz netto", "sub": "potem decyduj",
     "nar": "Policz zysk netto, a potem decyduj. Cała kalkulacja jest w filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Zysk netto", "l2": "nie brutto"}

COPY = """# kolejny-poziom-s007

## TITULO
Nadpłata czy Inwestycja: Porównuj Zysk po Podatku, a Nie przed Nim

## TITULO SHORT
Porównaj zysk netto, nie brutto

## DESCRICAO
Pytanie „nadpłacać kredyt czy inwestować" prawie zawsze rozbija się o jedną liczbę ustawioną w złym miejscu. Człowiek bierze oprocentowanie kredytu, bierze oczekiwany zysk z inwestycji, stawia je obok siebie i patrzy, co jest większe. Krok jest logiczny i wynik bywa błędny, bo te dwie liczby nie są tego samego rodzaju.

Zysk z inwestycji jest opodatkowany: część tego, co urośnie, oddajesz. Odsetki, których NIE zapłacisz dzięki nadpłacie, nie są przychodem — nie ma od czego pobierać podatku. Więc jedna strona porównania jest „przed", a druga „po". Porównując je bezpośrednio, dajesz inwestycji przewagę, której ona nie ma.

Poprawka jest jedna i prosta: od oczekiwanego zysku odejmij podatek, i DOPIERO ten wynik porównaj z oprocentowaniem kredytu. Nic więcej nie trzeba zmieniać w rachunku. Po tej korekcie kolejność potrafi się odwrócić — i akurat ta odwrotna kolejność jest tą, która zmienia decyzję, bo zwykle obie liczby leżą blisko siebie.

Warto wiedzieć, czego ten rachunek NIE rozstrzyga, bo to nie drobiazg: nie mówi nic o terminie, o płynności ani o ryzyku. Nadpłata jest pewna i nieodwracalna, inwestycja jest niepewna i można z niej wyjść. Dwie liczby po korekcie mówią tylko, która strona jest matematycznie korzystniejsza przy danych założeniach — a nie, która jest mądrzejsza w twojej sytuacji.

Nie ma tu żadnego oprocentowania, żadnej stawki podatku i żadnej kwoty: liczby, które decydują, są w twojej umowie kredytowej i w ofercie, którą rozważasz. Pełna kalkulacja na konkretnym przypadku, gdzie znaleźć każdą liczbę i co zrobić, gdy wyniki wychodzą niemal równe — są w filmie.

## COMENTARIO FIXADO
Najczęstszy błąd w tym porównaniu: stawianie oprocentowania kredytu obok zysku BRUTTO z inwestycji. Zysk jest opodatkowany, a odsetki, których nie zapłacisz dzięki nadpłacie, nie są przychodem — nie ma od czego pobrać podatku. Jedna strona jest „przed", druga „po". Odejmij podatek od zysku i dopiero wtedy porównaj: kolejność potrafi się odwrócić, bo zwykle obie liczby leżą blisko siebie. Czego ten rachunek NIE mówi: nic o terminie, płynności i ryzyku — nadpłata jest pewna i nieodwracalna, inwestycja niepewna i odwracalna. Stawki i kwot tu nie podaję: są w twojej umowie, a pełna kalkulacja w filmie. Jeśli policzysz, napisz tylko, czy po korekcie kolejność się odwróciła — bez kwot.

## HASHTAGS
#Kredyt #Inwestowanie #KolejnyPoziom

## TAGS
nadplata kredytu, inwestowanie, zysk netto, podatek od zyskow, oprocentowanie, kredyt hipoteczny, finanse osobiste, polska, obliczenia, decyzja finansowa, plynnosc, ryzyko, kolejny poziom, porownanie, brutto netto

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
ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita taxa de credito, nao cita rendimento,
nao cita aliquota de imposto, nao cita valor, nao cita prazo e nao nomeia o
imposto nem orgao nenhum. Nao ha numero dito na narracao.

O QUE O VIDEO AFIRMA: que o rendimento de um investimento e tributado e que o
juro que se deixa de pagar ao amortizar nao e, logo comparar a taxa do credito
com o rendimento BRUTO compara grandezas diferentes. Esta no longo
kolejny-poziom-007 (MjI4ZGJAhIo) com as fontes, e a parte aritmetica e
verificavel sem fonte nova.

DESCARTADO, e vai escrito:
  (1) a aliquota do imposto sobre rendimento na Polonia e o nome do imposto —
      estao no longo com fonte e NAO foram reconferidos hoje em duas fontes;
  (2) qualquer taxa de credito, rendimento ou valor;
  (3) se vale amortizar ou investir no caso de cada um — depende de prazo,
      liquidez e risco, esta no longo, e o short manda para la.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-007, MjI4ZGJAhIo) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s007",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "MjI4ZGJAhIo",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/kolejny-poziom-s007.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, piso 30s, mira 33-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
