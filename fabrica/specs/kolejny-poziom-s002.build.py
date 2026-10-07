"""kolejny-poziom-s002 — e a rodada em que eu ABORTEI um experimento meu.

ALAVANCA: A (alcance por short, pela CONCLUSAO). Quinto short solto.

# ---------------------------------------------------------------------------
# O ACHADO DA RODADA, e ele e o pior numero do dia
# ---------------------------------------------------------------------------
Reli o kolejny ao vivo as 14:12, DUAS HORAS depois da leitura das 12:11, e o
delta e que informa:
    short   12:11              14:12              cresceu em 2 h
    017     1.124 (10,5 h)     1.124 (12,5 h)     ZERO
    016       285 (15,5 h)       286 (17,5 h)     +1
    015       138 (27,9 h)       159 (29,9 h)     +21
    019       110 ( 3,7 h)       110 ( 5,7 h)     ZERO
    018        38 ( 7,6 h)        38 ( 9,6 h)     ZERO
Quatro de cinco PARARAM. O de 1.124 ficou exatamente em 1.124. E o 015 crescer
21 na MESMA chamada e na mesma janela e o controle que descarta atraso de
contagem: os zeros sao zeros.

**VIEW DE SHORT E RAJADA QUE MORRE, NAO TAXA** (aprendizado 635). E a aritmetica
que sai disso derruba o que eu mesmo escrevi hoje: se cada short entrega uma
rajada B e depois para, 3 milhoes em 90 dias com 7 shorts/dia (630 shorts) exige
**B = 4.762 em TODO short**. O recorde da frota e 1.124 — e esse morreu. Eu
havia escrito na rotina que "o alvo honesto e a Porta 1 antes de 1 de fevereiro
de 2027". Retratei na propria rotina: a metade dos inscritos fecha em ~33 dias,
a metade das views nao fecha sem destravar CONCLUSAO, e conclusao exige
`yt-analytics.readonly`, que nao tenho.

# ---------------------------------------------------------------------------
# O QUE EU MUDO: NADA. E isso e a decisao.
# ---------------------------------------------------------------------------
ABORTEI O EXPERIMENTO 34 (`titulo-de-short-sem-numero`), que eu mesmo abri tres
horas atras. Motivo: A METRICA NAO MEDIA A HIPOTESE. Operacionalizei "sem
numero" como "sem digito", e o vencedor absoluto do canal diz "przy JEDNYM
dziecku" — numero por extenso, que nenhum regex de digito pega. Experimento com
metrica invalida nao fica aberto acumulando dado que nao responde nada; vai para
`abortado` com o motivo escrito.

E NAO ABRI NADA NO LUGAR. O experimento 33 (`motion-no-short`) precisa de 10
dias ou 15 shorts por canal, e o motion e uma comparacao ANTES/DEPOIS: mexer na
duracao do short agora sujaria o periodo "depois" dele. O teste natural que a
pesquisa aponta — short de 22 a 26 s, que cai na faixa de 65% de retencao em vez
de 50% — fica ESPERANDO, e esta escrito na rotina esperando.
Entao este short nao muda variavel nenhuma: ele COPIA a forma que mediu melhor
no proprio canal (secao 5-d), que e o gancho de ELEGIBILIDADE — uma regra que
so vale para um grupo, obrigando a pessoa a conferir se esta nele. Foi isso que
separou o 017 (1.124 em 10,5 h) do 018 (38 em 7,6 h).
NUMERO DE PARTIDA: 9 views em 1,9 h do kolejny-poziom-s001, que usou o mesmo
gancho duas horas atras e esta rodando no ritmo do 018, nao do 017. Primeiro
sinal contra a copia da forma — cedo demais para concluir, e vai dito.

DE ONDE SAI: do longo JA PUBLICADO `IuBLU-P4Aj8` (kolejny-poziom-016, ZERO view),
cujo short fez 286 e e o segundo do canal. Angulo DIFERENTE: o short do 016
ENSINA a divisao (valor do imposto dividido pelos metros); este ataca o capitulo
"Gdy gmina nie uchwali stawek".

**E AQUI EU QUASE ESCREVI UMA FALSIDADE.** Eu ia titular "Gmina nie uchwalila?
Placisz sufit" — "a comuna nao votou? voce paga o teto" — porque era o que eu
supunha de cabeca. Fui ler o capitulo do proprio longo antes de escrever: o
artigo vigesimo a diz o CONTRARIO. Nao havendo uchwala, **valem as stawki do ano
ANTERIOR**, e nenhuma stawka de ministro entra. O angulo correto e o inverso do
que eu ia publicar: kwota igual a do ano passado NAO e necessariamente erro.
Isto e exatamente a regra da secao 6 — ler o proprio texto na lingua do canal
antes de renderizar — aplicada a um FATO e nao so a gramatica.

IDENTIDADE: faixa do canal sao 018, 019 e o s001 — paleta
`{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841, bg #F4F1EA}`, trilha `Wholesome`, voz
`pl-PL-MarekNeural`. O 017 segue fora da faixa, de proposito.

TENDENCIA: feed PL/26 nao relido nesta rodada e vai dito; a forma vem da medicao
do proprio canal, de minutos antes.

RISCO: canal de SETE inscritos. Este e o segundo short solto dele hoje, com mais
de duas horas entre os dois. Vigiei o teto antes e vou vigiar depois.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# UMA AFIRMACAO NORMATIVA, e ela vem do longo com a fonte: o artigo vigesimo a
# da ustawa o podatkach i oplatach lokalnych determina que, nao havendo uchwala
# da rada gminy para o ano, valem as stawki do ano anterior. Esta no
# `IuBLU-P4Aj8`, que carrega as fontes. Eu NAO a reconferi hoje em duas fontes
# proprias: ela entra porque e a mesma afirmacao do longo publicado, e isso vai
# DITO aqui em vez de passar como se fosse nova.
#
# ZERO CIFRA. O short nao diz valor de imposto, nao diz teto, nao diz
# percentual, nao diz prazo em dias e nao nomeia publicacao oficial.
#
# O NUMERO QUE DECIDE E DO ESPECTADOR: valor do imposto do ano dividido pelos
# metros da MESMA decisao, feito para dois anos e comparado.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) o teto da ustawa e qualquer stawka — estao no longo com a fonte;
#   (2) o prazo de catorze dias — esta no longo; citar prazo num short sem a
#       fonte ao lado e cifra solta;
#   (3) O QUE EU IA PUBLICAR E ERA FALSO: "nao havendo uchwala, paga-se o teto".
#       O artigo vigesimo a diz o oposto. Fica registrado porque o erro era meu
#       e quase foi ao ar.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Ta sama kwota", "sub": "co rok temu",
     "nar": "Kwota podatku od nieruchomości taka sama jak rok temu? To "
            "niekoniecznie błąd w decyzji.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Ustawa to przewiduje",
     "sub": "zostają stawki z poprzedniego roku",
     "nar": "Jeśli rada gminy nie uchwali nowych stawek, obowiązują stawki z "
            "roku poprzedniego. Nic nie znika.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "I odwrotnie",
     "sub": "wzrost nie znaczy stawka",
     "nar": "Wzrost kwoty też nie znaczy, że wzrosła stawka. Mógł się zmienić "
            "opis nieruchomości.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Dlatego dzielisz", "sub": "osobno za każdy rok",
     "nar": "Dlatego dzielenie robisz osobno za każdy rok: kwotę podatku przez "
            "metry z tej samej decyzji.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Porównaj wyniki", "sub": "i wiesz co się zmieniło",
     "nar": "Porównaj wyniki i wiesz, czy zmieniła się stawka, czy metry. Cały "
            "rachunek jest w filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Ta sama kwota?", "l2": "to nie błąd"}

COPY = """# kolejny-poziom-s002

## TITULO
Ta Sama Kwota co Rok Temu? Dlaczego Brak Uchwały Gminy Nie Znaczy Błędu w Decyzji

## TITULO SHORT
Ta sama kwota co rok temu? To nie błąd

## DESCRICAO
Dostajesz decyzję o podatku od nieruchomości, patrzysz na kwotę i jest identyczna jak rok temu. Pierwsza myśl bywa taka, że ktoś się pomylił albo że decyzja jest stara. Niekoniecznie: ustawa przewiduje dokładnie ten przypadek. Jeśli rada gminy nie uchwali stawek na dany rok, obowiązują stawki z roku poprzedniego — nie ma luki, nie ma zera i nie wchodzi tu żadna stawka ogłaszana centralnie. Brak uchwały nie znaczy brak podatku; znaczy, że zostaje dokładnie to, co było.

Z tego wynika coś praktycznego, i działa w obie strony. Kwota, która się nie zmieniła, nie jest dowodem błędu — może po prostu oznaczać gminę, która stawki nie podniosła albo w ogóle nie uchwaliła nowych. I odwrotnie: kwota, która wzrosła, nie jest dowodem, że wzrosła stawka. Mógł się zmienić opis nieruchomości w decyzji, a stawka zostać ta sama. Sama kwota nie rozstrzyga ani w jedną, ani w drugą stronę.

Rozstrzyga dzielenie, i to zrobione dla dwóch lat osobno: kwota podatku za rok podzielona przez metry kwadratowe z TEJ SAMEJ decyzji. Masz wtedy dwie liczby, które możesz porównać, i dopiero to porównanie mówi, czy rozmawiać o stawce, czy o metrach. To jedna z niewielu liczb w tym podatku, którą tylko ty masz — bo tylko ty masz obie decyzje.

Pełny film pokazuje, kto właściwie ustala tę stawkę i gdzie ją przeczytasz, co i kiedy ogłasza minister, skąd bierze się wskaźnik, cztery daty rat oraz termin, który najłatwiej przegapić. Tutaj nie podajemy ani stawek, ani sufitu z ustawy, ani terminów w dniach: te liczby są w pełnym filmie razem ze źródłami.

Treść informacyjna, nie stanowi porady podatkowej ani prawnej.

## COMENTARIO FIXADO
Krótko: brak uchwały rady gminy nie znaczy brak podatku — obowiązują wtedy stawki z roku poprzedniego, więc identyczna kwota dwa lata z rzędu nie jest sama z siebie błędem. Działa to też w drugą stronę: wzrost kwoty nie dowodzi wzrostu stawki, bo mógł się zmienić opis nieruchomości. Jedyne, co rozstrzyga, to dzielenie zrobione OSOBNO za każdy rok: kwota podatku za rok przez metry kwadratowe z tej samej decyzji. Porównujesz dwa wyniki i wiesz, czy rozmawiać o stawce, czy o metrach. Stawki, sufit z ustawy i terminy są w pełnym filmie razem ze źródłami. Jeśli policzysz dla dwóch lat, napisz czy wynik się zmienił — bez podawania kwot.

## HASHTAGS
#PodatekOdNieruchomosci #Gmina #KolejnyPoziom

## TAGS
podatek od nieruchomosci, stawka, gmina, uchwala rady gminy, decyzja podatkowa, metry kwadratowe, dzielenie, dwa lata, porownanie, podatki lokalne, finanse domowe, polska, kolejny poziom, nieruchomosc, rachunek

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
UMA AFIRMACAO NORMATIVA, e ela vem do longo com a fonte: o artigo vigesimo a da
ustawa o podatkach i oplatach lokalnych determina que, nao havendo uchwala da
rada gminy para o ano, valem as stawki do ano anterior. Esta no longo
kolejny-poziom-016 (IuBLU-P4Aj8), que carrega as fontes. Eu NAO a reconferi hoje
em duas fontes proprias: ela entra porque e a mesma afirmacao do longo
publicado, e isso vai dito em vez de passar como se fosse nova.

ZERO CIFRA. O short nao diz valor de imposto, nao diz sufit, nao diz percentual,
nao diz prazo em dias e nao nomeia publicacao oficial.

O NUMERO QUE DECIDE E DO ESPECTADOR: valor do imposto do ano dividido pelos
metros da MESMA decisao, feito para dois anos e comparado.

DESCARTADO, e vai escrito:
  (1) o sufit da ustawa e qualquer stawka — estao no longo com a fonte;
  (2) o prazo de catorze dias — esta no longo; prazo num short sem a fonte ao
      lado e cifra solta;
  (3) O QUE EU IA PUBLICAR E ERA FALSO: "nao havendo uchwala, paga-se o sufit".
      O artigo vigesimo a diz o OPOSTO. Fui ler o capitulo do proprio longo
      antes de escrever e o erro nao foi ao ar. Fica registrado porque era meu.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-016, IuBLU-P4Aj8) traz
as fontes, incluindo o artigo vigesimo a. Este short nao introduz cifra nova.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s002",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "IuBLU-P4Aj8",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/kolejny-poziom-s002.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, mira 33-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
