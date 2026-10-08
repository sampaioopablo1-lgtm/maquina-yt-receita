"""kolejny-poziom-s008 — stawka krotka i stawka dluga to nie ta sama liczba.

ALAVANCA: A (alcance por short). Oitavo short solto do kolejny.

O QUE DEU CERTO: a regra do 660, escrita na rodada anterior, ja esta valendo —
esta rodada coletou ANTES de ler idade contra views, e a leitura foi limpa.
O epomeno esta todo em PLATO: 159->161, 211->213, 343->345, 197->198 numa hora.
Delta de um ou dois e RUIDO pela faixa de oscilacao do 650, entao nao digo
"cresceu".

O QUE NAO DEU, e vai ANOTADO em vez de concluido: as duas pecas mais novas do
epomeno estao em ZERO — s007 as 5,9 h e s008 as 3,9 h — enquanto as quatro mais
velhas do canal todas dispararam ate ~4,8 h. Isso TEM a forma do 656, o erro que
me custou uma rodada: ler peca jovem numa idade fixa. O s007 esta a 0,1 h do piso
de 6 h. Entao NAO e achado nesta rodada: e item de vigilancia para a proxima, com
a pergunta certa — o degrau aconteceu, sim ou nao, depois das 6 h.
E segue sem par legivel no kolejny: 72 / 24 / 18 / 14 em idades parecidas, mesma
forma nas quatro (cinco cartoes de texto, mesma estrutura). A diferenca e pauta,
e "assunto" e resposta recusada pelo 2-B.3.

O QUE VOU MUDAR, e e uma coisa so: a mira de duracao sobe para ~35 s estimados
tambem no polones. Residuos medidos em pl: +2,5% e -1,3%; em pt-BR os dois de
hoje deram -6,5% e -6,8% com narracao mais longa. Como a hipotese e que o residuo
cresce com o tamanho da narracao, e o polones tem P alto (1,419 s por frase),
mirar 35 deixa margem dos dois lados.
NUMERO DE PARTIDA: 172 do short do pacote de origem; 72 do melhor solto maduro
do canal hoje.

DE ONDE SAI: longo `Rj7beZkOeYo` (kolejny-poziom-006, obrigacoes do tesouro),
origem VIRGEM e LIMPA — conferida nesta rodada por consulta que exclui o grupo
duplicado inteiro (658). Perfil 651: dinheiro da propria pessoa com papel na mao
(a tabela de ofertas). O short ORIGINAL daquele pacote ja usou o limiar
"inflacao dividida por zero oitenta e um", entao este ataca outra entrada errada,
tambem aritmetica e nao usada: comparar a taxa de um titulo CURTO com a de um
titulo LONGO como se fossem o mesmo produto. A taxa curta voce so mantem por um
trimestre e precisa RENOVAR, e na renovacao a taxa e outra; a longa voce mantem
pelo prazo inteiro. Antes de comparar, conte quantas renovacoes seriam
necessarias para chegar ao fim do titulo longo.

IDENTIDADE: faixa ATUAL do canal `{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841,
bg #F4F1EA}` com trilha `Wholesome`. O pacote 006 usa a paleta antiga
`{#14213D, #C1121F, #457B9D, #F1F0EA}` e eu NAO a copiei, mesmo sendo dele que
vem a pauta — o 601 manda comparar com a faixa historica, e esse erro ja apareceu
tres vezes em 08/10.

TENDENCIA: o feed PL/26 foi lido as 06:22 e NAO foi relido nesta rodada; digo em
vez de inventar. Dele ficou a FORMA: pergunta ou imperativo em segunda pessoa,
onze de quinze. Cena 1 pergunta, cena 5 imperativo.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita
# oprocentowanie, nao cita inflacao, nao cita aliquota, nao cita prazo em meses
# ou anos, nao cita valor e nao nomeia emissor nem orgao. Conferido A MAO campo
# por campo, porque o portao `narracao` conta QUANTIDADES por frase e NAO pega
# digito cru (640).
#
# O QUE O VIDEO AFIRMA: que a taxa de um titulo curto vale so pelo periodo do
# titulo e precisa ser renovada, enquanto a do titulo longo vale pelo prazo
# inteiro — logo comparar as duas diretamente compara coisas diferentes, e a
# conta que falta e quantas renovacoes cabem no prazo do longo. Esta no longo
# kolejny-poziom-006 (`Rj7beZkOeYo`), capitulos "Czym one sa", "Jak wybrac" e
# "Cztery bledy", com as fontes.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) qualquer taxa, a inflacao e a aliquota sobre os juros — estao no longo com
#       fonte, e o short nao precisa delas para dizer que prazos diferentes nao se
#       comparam direto;
#   (2) qual oferta ganha hoje — e preco que muda a cada emissao e NAO foi
#       reconferido nesta rodada em duas fontes;
#   (3) o limiar "inflacao dividida por zero oitenta e um", que e do short
#       original daquele pacote e nao se repete aqui.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Porównujesz stawki?", "sub": "to nie ten sam produkt",
     "nar": "Porównujesz stawkę obligacji krótkiej ze stawką obligacji długiej, "
            "jakby to był ten sam produkt?",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Krótka", "sub": "trzeba ją odnawiać",
     "nar": "Stawkę krótkiej trzymasz tylko do wykupu. Potem musisz ją odnowić, a "
            "wtedy stawka jest już inna.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Długa", "sub": "trzyma stawkę do końca",
     "nar": "Długa trzyma swoją stawkę przez cały okres, więc liczysz ją raz i "
            "wiesz, co dostaniesz na końcu.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Policz odnowienia", "sub": "zanim porównasz",
     "nar": "Zanim porównasz, policz ile razy musiałbyś odnowić krótką, żeby dojść "
            "do wykupu długiej.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Zrób to na swojej", "sub": "ofercie",
     "nar": "Policz tę liczbę na ofercie, którą masz przed sobą. Pełne porównanie "
            "jest w filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Krótka czy", "l2": "długa?"}

COPY = """# kolejny-poziom-s008

## TITULO
Obligacje Krótkie czy Długie: Policz Odnowienia, Zanim Porównasz Stawki

## TITULO SHORT
Krótka czy długa? Policz odnowienia

## DESCRICAO
Najczęstszy sposób wybierania obligacji wygląda rozsądnie: patrzysz na listę ofert, szukasz najwyższej stawki i bierzesz tę. Problem polega na tym, że na tej liście stoją obok siebie produkty, których stawki znaczą zupełnie różne rzeczy — i porównanie samych liczb pomija to, co właśnie decyduje.

Stawka obligacji krótkiej obowiązuje tylko do jej wykupu. Jeśli twój cel jest dalszy niż ten termin, to po wykupie musisz coś z tymi pieniędzmi zrobić: kupić kolejną, po stawce, która będzie obowiązywać wtedy, a nie dziś. Nie wiesz dziś, jaka ona będzie. Stawka obligacji długiej obowiązuje natomiast przez cały jej okres — liczysz ją raz i wiesz, z czym dojdziesz do końca. To są więc dwie różne rzeczy: jedna liczba, którą masz pewną na krótko, i jedna liczba, którą masz pewną na długo.

Dlatego porównanie, które coś mówi, wygląda inaczej. Najpierw policz, ile razy musiałbyś odnowić krótką, żeby dojść do wykupu długiej. Ta liczba to liczba momentów, w których stawka może się zmienić na twoją niekorzyść — i jednocześnie liczba momentów, w których może zmienić się na korzyść. Dopiero wtedy wiesz, co właściwie wybierasz: wyższą liczbę teraz plus niepewność kilka razy, albo niższą liczbę teraz i spokój do końca.

Z tej jednej liczby wynika też prosta wskazówka, która nie wymaga prognozowania niczego. Jeśli odnowień wychodzi dużo, to wyższa stawka krótkiej kupuje ci mniej, niż wygląda, bo większość twojego okresu i tak zależy od stawek, których jeszcze nie znasz. Jeśli odnowień wychodzi mało albo żadne — bo twój cel jest blisko — to długa nie daje ci nic, za co warto zapłacić niższą stawką.

Nie ma tu żadnej stawki, żadnej inflacji i żadnego terminu: liczby, które decydują, są w ofercie, którą masz przed sobą. Pełne porównanie wszystkich ofert, próg, od którego oferta przegrywa, i cztery najczęstsze błędy — są w filmie.

## COMENTARIO FIXADO
Cała różnica siedzi w jednym pytaniu: ile razy musiałbyś odnowić krótką, żeby dojść do wykupu długiej. Ta liczba mówi, jaka część twojego okresu zależy od stawek, których dziś nie znasz. Dużo odnowień — wyższa stawka krótkiej kupuje mniej, niż wygląda. Zero odnowień, bo cel jest blisko — długa nie daje nic, za co warto płacić. Policz tę liczbę na swojej ofercie i napisz w komentarzu tylko, czy wyszło dużo czy mało — bez kwot i bez stawek.

## HASHTAGS
#Obligacje #Oszczednosci #KolejnyPoziom

## TAGS
obligacje skarbowe, obligacje krotkie, obligacje dlugie, odnowienie, wykup, stawka, oszczednosci, finanse osobiste, polska, jak wybrac obligacje, oprocentowanie, horyzont inwestycyjny, kolejny poziom, liczenie, oferta

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita
oprocentowanie, nao cita inflacao, nao cita aliquota, nao cita prazo em meses ou
anos, nao cita valor e nao nomeia emissor nem orgao. Conferido a mao campo por
campo, porque o portao `narracao` conta quantidades por frase e nao pega digito
cru (640).

O QUE O VIDEO AFIRMA: que a taxa de um titulo curto vale so pelo periodo do
titulo e precisa ser renovada, enquanto a do titulo longo vale pelo prazo inteiro
— logo comparar as duas diretamente compara coisas diferentes, e a conta que
falta e quantas renovacoes cabem no prazo do longo. Esta no longo
kolejny-poziom-006 (Rj7beZkOeYo), capitulos "Czym one sa", "Jak wybrac" e "Cztery
bledy", com as fontes.

DESCARTADO, e vai escrito:
  (1) qualquer taxa, a inflacao e a aliquota sobre os juros — estao no longo com
      fonte;
  (2) qual oferta ganha hoje — preco que muda a cada emissao e NAO foi
      reconferido nesta rodada em duas fontes;
  (3) o limiar "inflacao dividida por zero oitenta e um", que e do short original
      daquele pacote e nao se repete aqui.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-006, Rj7beZkOeYo) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s008",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "Rj7beZkOeYo",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/kolejny-poziom-s008.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, piso 30s, mira 34-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
