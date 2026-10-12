"""kolejny-poziom-s018 — a RETROATIVIDADE, nao a quantia e nao a ordem.

ALAVANCA desta rodada: NENHUMA mudanca de forma. Esta e a QUARTA peca do braco
de dez a onze cenas no kolejny (s015, s016, s017, esta), mesmo esqueleto e mesma
mira. O aprendizado 693 mediu CV 0,66 DENTRO do mesmo tratamento e canal, e com
esse CV sao ~7 pecas por braco para enxergar um DOBRO. Abrir braco novo agora
deixaria todos com n pequeno.
NUMERO DE PARTIDA: braco de dez-a-onze cenas no kolejny com n=3. Esta e a quarta.

MIRA: `alvo_short('kolejny-poziom')` devolve 41,5 a 43,0 — a mira LONGA, que e a
que o proprio canal mediu como vencedora na janela casada de 4 a 8 h
(aprendizado 701: 209/117/115/83 na mira nova contra 17/13/4/0 na antiga). NAO
e a mira do labtreinamento, que mediu o OPOSTO (698). Mira e por canal.

O QUE EU NAO RELI nesta rodada, de proposito: inscrito e view DE CANAL. A ultima
leitura valida e a do `medir.yml` das 07:08 de hoje, e o 686 exige >= ~4 h entre
leituras comparaveis.

DE ONDE SAI: longo `kDkagIf2isA` (pacote `kolejny-poziom-010`), "Ryczalt 2026:
Jeden Zloty Ponad Progiem". Origem LIVRE — conferido contra o `longo_existente`
de todas as specs e contra o retrato `fabrica/ponte/videos.json`: nenhuma spec a
usa. Os capitulos foram lidos da propria spec local, campos 18 a 25.

FAMILIA DIFERENTE das tres ultimas do canal, como a regra (f) exige: `s015` era
LIMIAR (aritmetica de faixa), `s016` COMPOSICAO (duas metades da fatura), `s017`
ORDEM (a sequencia dos filares), e esta e DEFASAGEM NO TEMPO — a causa e o efeito
estao separados por meses, e a pessoa decide no momento em que nao ve o preco.

TITULO EM PERGUNTA, a forma do PL/26.

IDENTIDADE: faixa ATUAL do canal `{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841,
bg #F4F1EA}`, trilha `Wholesome` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ESTA ORIGEM E A MAIS PERIGOSA DA PAUTA para a regra (g), e por isso o aviso vem
# antes do roteiro. O longo inteiro e feito de numero que MUDA: tres progs de
# receita anual, tres valores de contribuicao mensal, o obwieszczenie do GUS que
# os reajusta sozinho todo ano, o salario minimo, o limite de deducao do
# liniowy, e o prazo da declaracao. NADA DISSO entra no short.
#
# O QUE O SHORT CARREGA, e nao envelhece: a contribuicao NAO sobe a partir do mes
# em que o prog e passado — o ano INTEIRO e recalculado para tras, inclusive os
# meses ja pagos e fechados, e a diferenca so aparece no acerto, meses depois da
# fatura que a causou. Isso e a MECANICA da norma, nao a tabela dela. Se o GUS
# reajustar as tres faixas amanha, esta peca continua verdadeira.
#
# ZERO DIGITO NA NARRACAO, e conferido campo a campo a mao, porque o portao
# `narracao` conta QUANTIDADES por frase e nao pega digito cru. Nao ha nem
# ordinal de valor: "caly rok wstecz" entrou no lugar de "cala dwunastka" de
# proposito, para nao haver numeral nenhum.
#
# DESCARTADO, e vai escrito:
#   (1) os tres progs e as tres contribuicoes mensais — o proprio longo diz que
#       sao percentuais de uma base que o obwieszczenie do GUS publica todo ano;
#   (2) a conta de "quase quatro mil" e a de "quase oito mil" — saem das tabelas
#       acima e envelhecem com elas;
#   (3) o prazo da declaracao (mes e dia) — data de vigencia, muda por ato;
#   (4) o salario minimo e o limite de deducao no liniowy, pela mesma razao;
#   (5) a comparacao entre formas de tributacao — depende da tabela do ano.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Faktura z grudnia", "sub": "zmienia twój styczeń", "nar": "Faktura z grudnia zmienia twój styczeń.", "sem_cap": True},
    {"layout": "item", "kicker": "Na ryczałcie", "preco": "składka stoi", "nar": "Na ryczałcie składka stoi w miejscu.", "sem_cap": True},
    {"layout": "item", "kicker": "Stoi", "preco": "do progu", "nar": "Stoi, dopóki nie minie próg przychodu.", "sem_cap": True},
    {"layout": "titulo", "kicker": "I wtedy", "sub": "nie od tego miesiąca", "nar": "I wtedy nie rośnie od tego miesiąca.", "sem_cap": True},
    {"layout": "item", "kicker": "Przeliczenie", "preco": "cały rok wstecz", "nar": "Przeliczany jest cały rok wstecz.", "sem_cap": True},
    {"layout": "item", "kicker": "Także", "preco": "miesiące zamknięte", "nar": "Także miesiące już zapłacone i zamknięte.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Dopłatę widzisz", "sub": "dopiero w rozliczeniu", "nar": "Dopłatę widzisz dopiero w rozliczeniu.", "sem_cap": True},
    {"layout": "item", "kicker": "Czyli", "preco": "miesiące później", "nar": "Czyli długo po tej jednej fakturze.", "sem_cap": True},
    {"layout": "item", "kicker": "A faktura", "preco": "nie zna roku", "nar": "A faktura nie zna twojego rocznego przychodu.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Policz próg", "sub": "zanim wystawisz", "nar": "Policz próg, zanim ją wystawisz.", "sem_cap": True},
    {"layout": "cta", "kicker": "Zasubskrybuj", "sub": "na następne", "nar": "Sprawdź to w grudniu. Zasubskrybuj.", "sem_cap": True}
]

THUMB = {"l1": "Grudzień", "l2": "zmienia styczeń"}

COPY = """# kolejny-poziom-s018

## TITULO
Przekroczenie Progu Przelicza Cały Rok Wstecz, Także Miesiące Już Zapłacone

## TITULO SHORT
Dlaczego grudzień zmienia styczeń?

## DESCRICAO
Na ryczałcie składka zdrowotna nie rośnie razem z przychodem — stoi w miejscu wewnątrz progu. Dlatego łatwo pomyśleć, że w najgorszym razie od momentu przekroczenia zacznie się płacić więcej. Tak to nie działa, i to jest cała rzecz w tym filmie.

Jeśli roczny przychód przekroczy próg, składka za **miesiące wcześniejsze** nie zostaje taka, jaka była. Cały rok zostaje przeliczony według progu, w którym ostatecznie wylądował przychód — wstecz, razem z miesiącami już zapłaconymi i uznanymi za zamknięte. Różnicy nie dopłacasz w tym samym miesiącu: wychodzi ona w rozliczeniu rocznym, czyli wiele miesięcy po fakturze, która ją spowodowała.

I właśnie tu jest pułapka, która nie ma nic wspólnego z żadną kwotą: decyzja i jej skutek są od siebie oddalone w czasie. W momencie wystawiania faktury nie widać ceny, bo faktura nie wie, ile wynosi twój roczny przychód. Cena pojawia się później, kiedy nie można już nic zmienić.

Ten short świadomie nie podaje ani progów, ani stawek, ani terminu rozliczenia. Te liczby zmieniają się — progi są procentem kwoty, którą GUS ogłasza co roku, a terminy zmieniają się ustawą. To, co się nie zmienia, to mechanika: przeliczenie idzie wstecz, a rachunek przychodzi później. Konkretne liczby, z datą i źródłem, są w pełnym filmie.

Pełne wyliczenie — trzy progi, kwoty na ten rok, obie granice policzone co do grosza i porównanie z innymi formami opodatkowania — jest w filmie na kanale.

## COMENTARIO FIXADO
Najdroższy błąd w tej konstrukcji nie jest rachunkowy, jest czasowy. Ludzie zakładają, że przekroczenie progu działa jak schodek: od tego miesiąca płacę więcej. A ono działa wstecz — cały rok liczy się od nowa, razem z miesiącami, które były już zapłacone i uznane za zamknięte. Do tego dopłata nie wychodzi od razu, tylko w rozliczeniu rocznym, więc fakturę wystawiasz w jednym miesiącu, a rachunek za nią widzisz długo później, kiedy nic już nie da się przestawić. Celowo nie ma tu ani jednej liczby: progi są procentem kwoty ogłaszanej co roku przez GUS, a terminy zmieniają się ustawą — pełne wyliczenie z datą i źródłem jest w filmie. Napiszcie tylko, czy sprawdzacie swój przychód przed wystawieniem grudniowej faktury, czy po.

## HASHTAGS
#Ryczalt #SkladkaZdrowotna #KolejnyPoziom

## TAGS
ryczalt skladka zdrowotna, prog przychodu, przeliczenie wstecz, rozliczenie roczne skladki, faktura w grudniu, moment wystawienia faktury, dzialalnosc gospodarcza, jdg podatki, skladka zdrowotna ryczalt zasady, przekroczenie progu, mechanika a nie tabela, kolejny poziom, finanse firmowe, planowanie przychodu, rok podatkowy

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Conferido a mao campo
por campo, porque o portao `narracao` conta QUANTIDADES por frase e nao pega
digito cru. Nao ha nem numeral por extenso: "caly rok wstecz" entrou no lugar de
"cala dwunastka" de proposito.

A REGRA (g) MANDA, e esta origem e a mais perigosa da pauta para ela: o longo
inteiro e feito de numero que MUDA — tres progs anuais, tres contribuicoes
mensais, o obwieszczenie do GUS que reajusta a base todo ano, o salario minimo, o
limite de deducao do liniowy e o prazo da declaracao.

O QUE A PECA CARREGA, e nao envelhece: a contribuicao nao sobe a partir do mes em
que o prog e passado — o ano INTEIRO e recalculado para tras, inclusive meses ja
pagos, e a diferenca aparece no acerto anual, meses depois da fatura que a
causou. E a MECANICA da norma, nao a tabela dela. Se o GUS reajustar as faixas
amanha, a peca continua verdadeira.

Esta nos capitulos "Jesli przekroczysz prog", "Ona jest przeliczana", "I to nie w
grudniu", "Zwroc uwage na odstep" e "I dlatego" do longo `kDkagIf2isA`
(kolejny-poziom-010).

DESCARTADO, e vai escrito:
  (1) os tres progs e as tres contribuicoes mensais — percentuais de uma base
      que o obwieszczenie do GUS publica todo ano;
  (2) as contas de "quase quatro mil" e "quase oito mil" — saem das tabelas
      acima e envelhecem com elas;
  (3) o prazo da declaracao, mes e dia — data de vigencia, muda por ato;
  (4) o salario minimo e o limite de deducao no liniowy, pela mesma razao;
  (5) a comparacao entre formas de tributacao — depende da tabela do ano.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-010, kDkagIf2isA) traz as
fontes oficiais e as datas. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s018",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "kDkagIf2isA",
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
    grava(SPEC, "fabrica/specs/kolejny-poziom-s018.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short(SPEC["slug"])
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} (por canal) | PISO no pl")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto "
          f"{s*1.004:.1f} a {s*1.044:.1f}")
    print(f"por plano: {s/len(SHORT):.2f}s | falas de legenda: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
