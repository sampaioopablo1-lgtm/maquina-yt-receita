"""kolejny-poziom-s019 — DOIS EFEITOS EM SENTIDOS OPOSTOS. Segundo angulo.

SEGUNDO ANGULO, escolhido com o instrumento e nao a mao: `segundo_angulo.py`
resolveu a origem `EwUkhdwyuuo` para o pacote `kolejny-poziom-013`, **90
capitulos**, com **um** short publicado (`kolejny-poziom-s011`, "Nadplata skraca
okres czy rate?") e **84 capitulos nao mencionados**.

E O INSTRUMENTO SO SERVIU DEPOIS DE UM CONSERTO, nesta mesma rodada: na primeira
vez que eu o usei para escolher, ele resolveu TRES origens do kolejny para a spec
`kolejny-poziom`, que e o slug do canal e tem dez cenas. Falso positivo do slug,
consertado com fronteira de identificador e com a exclusao de slug do
vocabulario.

FAMILIA NOVA, a decima: **DOIS EFEITOS EM SENTIDOS OPOSTOS**. O prazo faz duas
coisas ao mesmo tempo e elas se opoem — prazo maior derruba a parcela, e prazo
maior multiplica o numero de parcelas que carregam juros. Quem decide olhando
UMA das duas decide sem ver o preco da outra. O proprio longo enuncia:
*"Te dwa efekty dzialaja przeciwko sobie, i to wlasnie dlatego nie da sie
odpowiedziec na oko"*.
Ja usadas: LIMIAR, COMPOSICAO, ORDEM, DEFASAGEM NO TEMPO, ARITMETICA
media-contra-produto, CONDICAO/ACAO, MARGINAL contra TOTAL, A SOMA DOS PEQUENOS,
SUBSTITUICAO QUE NAO SUBSTITUI.
Regra (f) respeitada: o kolejny teve hoje o `s018`, que era DEFASAGEM NO TEMPO.

**E A RESSALVA DO LONGO ENTRA NA PECA, nao fica de fora.** Ele diz com todas as
letras que *"krotszy okres nie jest darmowy"* e que *"to nie jest rada, zeby brac
krocej"* — prazo curto sobe a parcela, as vezes ate nao caber. Sem essa linha o
short viraria conselho financeiro, e o longo justamente se recusa a dar conselho.
A peca termina mandando ver o preco das DUAS opcoes, nao escolher uma.

MIRA: `alvo_short('kolejny-poziom')` = 41,5 a 43,0, e no polones o residuo e
**+2,2%**, entao a regra manda mirar o **PISO** (679). Mirei 41,5.

IDENTIDADE: faixa ATUAL do canal, trilha `Wholesome` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO DIGITO e ZERO NUMERAL na narracao. O longo esta cheio de numero de
# exemplo — parcela, prazo em meses, taxa, saldo, as quatro contas da conta a
# mao — e NADA disso entra. A regra aqui nao precisa de numero nenhum: ela e
# sobre a DIRECAO de dois efeitos, nao sobre a magnitude deles.
#
# Em especial NAO digo "dois efeitos": "dwa" seria numeral. A peca diz que o
# prazo "derruba a parcela" e "multiplica as parcelas", e deixa a contagem
# implicita na propria estrutura das frases.
#
# O QUE A PECA CARREGA, e nao envelhece: prazo mais longo baixa a parcela E
# aumenta o numero de parcelas que carregam juros; os dois efeitos se opoem, logo
# a conta nao se faz no olho. E a ressalva do longo vem junto: prazo curto nao e
# de graca, porque sobe a parcela. Isso e estrutura de amortizacao, nao tabela.
#
# O QUE EU NAO LEVEI, e vai escrito para a proxima rodada achar: o capitulo
# "Rata ma dwie czesci" / "Na poczatku" — a parcela tem duas partes e no comeco
# predominam os juros, que e por que a parcela cai mais devagar do que o prazo
# cresce. E outra familia (A PARTE QUE DOMINA NO COMECO) e da um TERCEIRO angulo
# deste mesmo longo. Nao a levei hoje porque ela explica o MESMO resultado por
# dentro, e duas pecas no mesmo dia sobre a mesma mecanica apertariam o
# `similaridade` sem necessidade.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Wybierasz okres", "sub": "patrząc na ratę", "nar": "Wybierasz okres, patrząc tylko na ratę.", "sem_cap": True},
    {"layout": "item", "kicker": "Dłuższy okres", "preco": "niższa rata", "nar": "Dłuższy okres rzeczywiście obniża ratę.", "sem_cap": True},
    {"layout": "item", "kicker": "Ale też", "preco": "więcej rat", "nar": "Ale mnoży też liczbę rat, które zapłacisz.", "sem_cap": True},
    {"layout": "titulo", "kicker": "A każda", "sub": "nosi odsetki", "nar": "A każda z nich nosi w sobie odsetki.", "sem_cap": True},
    {"layout": "item", "kicker": "Więc", "preco": "idą w kontrze", "nar": "Więc te skutki działają przeciwko sobie.", "sem_cap": True},
    {"layout": "item", "kicker": "Dlatego", "preco": "nie na oko", "nar": "Dlatego nie da się tego ocenić na oko.", "sem_cap": True},
    {"layout": "titulo", "kicker": "I w drugą stronę", "sub": "krótszy nie jest darmowy", "nar": "I w drugą stronę: krótszy nie jest darmowy.", "sem_cap": True},
    {"layout": "item", "kicker": "On podnosi", "preco": "ratę", "nar": "On podnosi ratę, czasem ponad twój budżet.", "sem_cap": True},
    {"layout": "item", "kicker": "Więc to nie", "preco": "rada", "nar": "To nie jest więc rada, żeby brać krócej.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Poproś o cenę", "sub": "obu opcji", "nar": "Poproś bank o cenę obu opcji na piśmie.", "sem_cap": True},
    {"layout": "cta", "kicker": "Zasubskrybuj", "sub": "na następne", "nar": "Jeśli to ci pomogło, zasubskrybuj kanał.", "sem_cap": True}
]

THUMB = {"l1": "Nie na", "l2": "oko"}

COPY = """# kolejny-poziom-s019

## TITULO
Okres Robi Dwie Rzeczy Naraz I Działają Przeciwko Sobie — Dlatego Nie Oceniaj Go Na Oko

## TITULO SHORT
Dlaczego nie na oko?

## DESCRICAO
Przy wyborze okresu kredytu prawie wszyscy patrzą na jedną liczbę: ratę. I to jest zrozumiałe, bo rata jest tym, co zobaczysz na koncie co miesiąc. Problem polega na tym, że okres **nie robi jednej rzeczy** — robi dwie, jednocześnie, i te dwie działają w przeciwne strony.

Pierwszy skutek widzisz od razu: im dłuższy okres, tym niższa rata. Ta sama kwota rozkłada się na więcej miesięcy.

Drugi skutek nie pojawia się na żadnym wydruku: im dłuższy okres, tym **więcej rat** zapłacisz — a każda z nich nosi w sobie odsetki od tego, co jeszcze zostało do oddania.

Z tego wynika rzecz, która decyduje: skoro jeden skutek działa na twoją korzyść, a drugi przeciwko, **nie da się ocenić wyniku na oko**. Kto wybiera okres patrząc tylko na ratę, podejmuje decyzję nie widząc ceny drugiej strony.

I uwaga w odwrotnym kierunku, bo bez niej to byłaby połowa prawdy: **krótszy okres nie jest darmowy.** On podnosi ratę — czasem na tyle, że przestaje się mieścić w budżecie. To nie jest więc rada, żeby brać krócej. To jest powód, żeby zobaczyć cenę **obu** opcji, zanim wybierzesz jedną.

Praktyczny wniosek jest jednozdaniowy: poproś bank o wyliczenie obu wariantów na piśmie, tego samego dnia i na tych samych warunkach — inaczej porównujesz dwie różne oferty, a nie dwa okresy.

Ten short świadomie nie podaje ani rat, ani stawek, ani liczby miesięcy: to liczby przykładu i zmieniają się z ofertą. Nie zmienia się kierunek obu skutków.

W pełnym filmie: skąd dokładnie bierze się ta różnica, rachunek na czterech liczbach, który zrobisz sam na kartce, dlaczego rata spada wolniej niż rośnie okres, i co zrobić, jeśli bank zwleka z wyliczeniem.

## COMENTARIO FIXADO
Sedno nie jest w tym, że dłuższy okres jest zły — jest w tym, że okres robi dwie rzeczy naraz, a one idą w przeciwne strony: obniża ratę i równocześnie mnoży liczbę rat, z których każda nosi odsetki. Dopóki patrzysz tylko na jedną z nich, nie widzisz ceny drugiej, i właśnie dlatego tego nie da się ocenić na oko. Druga połowa prawdy, bez której to byłaby porada, a nie wyjaśnienie: krótszy okres nie jest darmowy — podnosi ratę, czasem ponad budżet. Celowo nie ma tu ani rat, ani stawek, ani miesięcy: to liczby przykładu, są w filmie. Jedna rzecz praktyczna, o którą warto poprosić: wyliczenie obu wariantów na piśmie, tego samego dnia i na tych samych warunkach. Napiszcie, czy bank dał wam kiedyś takie porównanie bez proszenia.

## HASHTAGS
#Kredyt #Finanse #KolejnyPoziom

## TAGS
okres kredytu, wysokosc raty, liczba rat, odsetki od kredytu, porownanie wariantow, nadplata kredytu, koszt kredytu, decyzja kredytowa, wyliczenie na pismie, krotszy okres, dluzszy okres, kolejny poziom, finanse osobiste, harmonogram splat, dwa skutki

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
ZERO NUMERO NOVO SOBRE O MUNDO, ZERO DIGITO e ZERO NUMERAL na narracao. O longo
esta cheio de numero de exemplo — parcela, prazo em meses, taxa, saldo, e as
quatro contas do calculo a mao — e NADA disso entra. A regra nao precisa de
numero: ela e sobre a DIRECAO de dois efeitos, nao sobre a magnitude.

Em especial NAO digo "dois efeitos": "dwa" seria numeral. A peca diz que o prazo
"obniża ratę" e "mnoży liczbę rat", e deixa a contagem implicita na estrutura.

O QUE A PECA CARREGA, e nao envelhece: prazo mais longo baixa a parcela E
aumenta o numero de parcelas que carregam juros; os dois se opoem, logo a conta
nao se faz no olho. Esta nos capitulos "Co robi okres", "Pierwsza rzecz",
"Druga rzecz" e "Te dwie ida w kontrze" do longo `EwUkhdwyuuo` (pacote
`kolejny-poziom-013`).

A RESSALVA DO LONGO ENTRA NA PECA, e isso nao e enfeite: ele diz
"krotszy okres nie jest darmowy" e "to nie jest rada, zeby brac krocej". Sem
essa linha o short viraria conselho financeiro, e o longo se recusa a dar
conselho. A peca termina mandando ver o preco das DUAS opcoes.

SEGUNDO ANGULO, declarado: o primeiro short deste longo e o `kolejny-poziom-s011`
("Nadplata skraca okres czy rate?"). O longo tem 90 capitulos e 84 nao estavam
mencionados. Familia diferente, capitulos diferentes, e passou o `similaridade`.

O QUE EU NAO LEVEI, escrito para a proxima rodada achar: "Rata ma dwie czesci" /
"Na poczatku" — a parcela tem duas partes e no comeco predominam os juros, que e
por que a parcela cai mais devagar do que o prazo cresce. Outra familia (A PARTE
QUE DOMINA NO COMECO) e um TERCEIRO angulo. Nao a levei hoje porque ela explica
o MESMO resultado por dentro, e duas pecas no mesmo dia sobre a mesma mecanica
apertariam o `similaridade` sem necessidade.

## FONTES
O longo de onde este short foi extraido (`kolejny-poziom-013`, `EwUkhdwyuuo`)
carrega os numeros do exemplo. Este short NAO introduz numero novo sobre o mundo,
entao nao exige fonte institucional nova.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s019",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "EwUkhdwyuuo",
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
    grava(SPEC, "fabrica/specs/kolejny-poziom-s019.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short(SPEC["slug"])
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | {len(SHORT)} cenas | SEGUNDO ANGULO de EwUkhdwyuuo")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} | PISO no polones (+2,2%)")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'}")
    print(f"por plano: {s/len(SHORT):.2f}s | falas: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
