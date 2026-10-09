"""kolejny-poziom-s012 — quando pedes aumento, que numero ve o outro lado?

ALAVANCA: quinto ponto do experimento 38, e o SEGUNDO no piso da faixa com a voz
de pior caso. O `kolejny-poziom-s011` saiu em 43,37 s reais contra 41,9
estimados (+3,5%), confirmando o residuo positivo da `pl-PL-Marek`. Miro 41,5 a
42,0 outra vez, para ter DOIS pontos na mesma voz e no mesmo extremo da faixa —
um ponto so nao distingue calibracao de sorte. Terceira peca com titulo em
PERGUNTA.

O QUE DEU CERTO, e e o movimento desta hora: `epomeno-epipedo-s010` foi de 2 para
166 views as 4,9 h, `kolejny-poziom-s010` de 8 para 70 as 3,9 h, e o
`epomeno-epipedo-s011` de 8 para 88 as 2,6 h. A frota esta distribuindo.

O QUE NAO DEU: nada que eu possa concluir. As QUATRO pecas de 09/10 tem 0,9 a
2,6 h e peca abaixo de 6 h nao serve NEM para confirmar NEM para refutar (664).
O experimento 37 (CTA pedindo inscricao) continua SEM leitura valida, e os
inscritos nao se moveram: 8 / 16 / 67. Digo isso em vez de ler um sinal.

O QUE VOU MUDAR: uma coisa so, e e o CANAL da rodada. Nao faco labtreinamento
agora: as CINCO origens livres dele sao todas conformidade corporativa, o perfil
que o 651 mediu como ~30x pior, e o kolejny tem SETE do perfil que funciona. Isso
nao resolve o labtreinamento — a saida dele e pacote completo, que pede janela do
dono — mas gastar a rodada no estoque ruim quando existe estoque bom e escolher
pior de proposito.
NUMERO DE PARTIDA: zero views no short do pacote de origem (nunca saiu short
dele); 459 do melhor solto do canal as 8,9 h.

DE ONDE SAI: longo `34SgUG7rf0U` (kolejny-poziom-005, o custo do empregador
contra o liquido), capitulo "Cztery ruchy | dziesiec minut", TERCEIRO movimento:
quando se pede aumento em bruto, a empresa ve o aumento ampliado pelos encargos
dela. O short ORIGINAL do pacote faz o contraste dos tres numeros e as quatro
deducoes, e termina prometendo exatamente este capitulo — "Caly rozklad i cztery
ruchy na kartke, w pelnym filmie". Esta peca FAZ o que aquele prometeu.

FAMILIA, regra (f): o `kolejny-s011` de hoje foi "qual dos dois efeitos a sua
acao tem" (prazo ou prestacao). Esta e "o numero que o outro lado ve nao e o que
voce disse". Entradas erradas diferentes.

IDENTIDADE: faixa ATUAL do canal `{ink #1B3A5C, c1 #2A9D8F, c2 #F5B841,
bg #F4F1EA}`, trilha `Wholesome` (601).

TENDENCIA: o feed PL/26 foi lido as 01:1x desta madrugada e NAO foi relido agora
— o chart repete 14 de 15 em quatro horas (623), entao reler em duas horas seria
gastar chamada para ver a mesma lista. O que vale dela: seis de quinze em
PERGUNTA, dois imperativos em segunda pessoa, zero educacional.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita o
# percentual dos encargos, nao cita salario minimo, nao cita bruto, nao cita
# liquido e nao nomeia orgao. Conferido A MAO campo por campo, porque o portao
# `narracao` conta QUANTIDADES por frase e NAO pega digito cru.
#
# E A REGRA (g) AQUI TEM RAZAO DUPLA. Primeiro, o percentual dos encargos muda
# por lei. Segundo, e mais forte: ele NAO E UM NUMERO SO. O proprio capitulo do
# longo diz que a stawka wypadkowa "potrafi sie roznic kilkukrotnie miedzy
# branzami" — varia VARIAS VEZES entre setores. Citar "cerca de vinte por cento"
# daria ao espectador um numero que pode nao ser o dele. O short manda calcular
# o MULTIPLICADOR PROPRIO, que e exatamente o mecanismo do 651: o numero e dele,
# com o papel na mao.
#
# O QUE O VIDEO AFIRMA: que o custo do empregador e maior que o bruto porque
# inclui as contribuicoes da empresa; que por isso um pedido de aumento em bruto
# chega ampliado ao outro lado; e que o multiplicador se obtem dividindo o custo
# do empregador pelo bruto, com a taxa de acidente da propria empresa conferida.
# Esta no longo kolejny-poziom-005 (`34SgUG7rf0U`), capitulos "Ponad brutto" e
# "Cztery ruchy".
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) o percentual dos encargos — muda por lei E varia por setor;
#   (2) os valores de salario minimo, bruto e liquido do longo, que sao do ano e
#       envelhecem a peca;
#   (3) a comparacao etat contra B2B, que esta no longo e e OUTRA familia de
#       entrada errada — fica para outra peca, nao se empilha aqui.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Prosisz o podwyżkę", "sub": "co widzi firma?",
     "nar": "Prosisz o podwyżkę brutto. Ale jaką liczbę widzi osoba, która ją "
            "zatwierdza?",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Ty myślisz w brutto", "sub": "ona nie",
     "nar": "Ty myślisz w brutto. Firma widzi swój koszt, wyższy o jej własne "
            "składki, których na twoim pasku w ogóle nie ma.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Dociera powiększona", "sub": "twoja prośba",
     "nar": "Więc twoja prośba dociera do niej powiększona. Nie proś o mniej — "
            "wiedz, co ona widzi.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Policz swój mnożnik", "sub": "nie średni",
     "nar": "Policz swój mnożnik: podziel koszt pracodawcy przez brutto. I "
            "sprawdź stawkę wypadkową swojej firmy, bo potrafi się różnić "
            "kilkukrotnie.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Subskrybuj", "sub": "na kolejne",
     "nar": "Zrób to na swoim pasku wypłaty, nie na średniej. Subskrybuj, a cały "
            "rozkład jest w filmie.",
     "sem_cap": True},
]

THUMB = {"l1": "Twoje brutto", "l2": "jej koszt"}

COPY = """# kolejny-poziom-s012

## TITULO
Rozmowa o Podwyżce: Dlaczego Druga Strona Widzi Większą Liczbę niż Ta, Którą Powiedziałeś

## TITULO SHORT
Ile widzi firma, gdy prosisz o podwyżkę?

## DESCRICAO
Rozmowa o podwyżce prawie zawsze toczy się w dwóch różnych jednostkach, i żadna ze stron tego nie mówi na głos. Ty myślisz i mówisz w brutto, bo to jest liczba z twojej umowy. Osoba po drugiej stronie myśli w koszcie pracodawcy, bo to jest liczba, która stoi w budżecie obok twojego nazwiska. Te dwie liczby nie są tą samą liczbą, i różnica między nimi nie jest mała.

Dlaczego się różnią: do brutto dochodzą składki, które płaci firma, a nie ty — i one nie pojawiają się nigdzie na twoim pasku jako coś, co dostajesz. Dlatego twój koszt dla firmy jest wyższy od twojego brutto, a każda prośba o podwyżkę brutto dociera do drugiej strony powiększona o ten sam narzut. To wyjaśnia reakcję, która często wygląda na nieproporcjonalną: nie jest nieproporcjonalna do liczby, którą widzi twój rozmówca.

Z tego nie wynika, że masz prosić o mniej. Wynika, że warto wiedzieć, jaką liczbę słyszy druga strona, bo wtedy przestajesz się dziwić i możesz rozmawiać o właściwej wielkości.

A policzyć swój narzut możesz sam, i to jest cała arytmetyka: podziel koszt pracodawcy przez swoje brutto. Wynik jest twoim mnożnikiem. Jedno sprawdzenie jest tu konieczne i jest to jedyna pozycja z całej listy, która potrafi się różnić kilkukrotnie między branżami — stawka wypadkowa obowiązująca w twojej firmie. Dlatego nie podaję tu żadnego gotowego procentu: liczba, która ma znaczenie, to twoja, a nie średnia.

Nie ma tu ani kwot, ani stawek, i to jest celowe — przepisy się zmieniają, a metoda nie. Pełny rozkład od kosztu pracodawcy do kwoty na koncie, cztery ruchy na jedną kartkę w dziesięć minut, różnica między etatem a B2B i cztery błędy, które psują ten rachunek — są w filmie.

## COMENTARIO FIXADO
Arytmetyka w jednym zdaniu: koszt pracodawcy podzielony przez twoje brutto daje twój mnożnik, i to jest liczba, o którą powiększa się każda prośba o podwyżkę brutto. Zanim policzysz, sprawdź stawkę wypadkową swojej firmy — to jedyna pozycja, która potrafi się różnić kilkukrotnie między branżami, i dlatego żaden gotowy procent z internetu nie jest twój. Jeszcze jedno, bo to najczęstszy błąd w całym temacie: NIE porównuj brutto z etatu do kwoty z faktury B2B. To dwa różne poziomy tej samej drabiny — uczciwe porównanie zestawia koszt pracodawcy z kwotą na fakturze. Kto policzy swój mnożnik, niech napisze w komentarzu tylko, czy wyszedł wyżej czy niżej, niż się spodziewał — bez kwot.

## HASHTAGS
#Podwyżka #KosztPracodawcy #KolejnyPoziom

## TAGS
koszt pracodawcy, podwyzka brutto, pasek wyplaty, skladki pracodawcy, stawka wypadkowa, rozmowa o podwyzce, brutto netto, finanse osobiste, polska, jak policzyc, mnoznik, etat, kolejny poziom, wynagrodzenie, negocjacje placowe

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita percentual
de encargos, salario minimo, bruto, liquido nem orgao. Conferido a mao.

A REGRA (g) AQUI TEM RAZAO DUPLA. O percentual dos encargos muda por lei; e, mais
forte, ele NAO E UM NUMERO SO — o proprio longo diz que a stawka wypadkowa varia
VARIAS VEZES entre setores. Citar "cerca de vinte por cento" daria ao espectador
um numero que pode nao ser o dele. O short manda calcular o MULTIPLICADOR
PROPRIO, que e o mecanismo do 651.

O QUE O VIDEO AFIRMA: que o custo do empregador e maior que o bruto porque inclui
as contribuicoes da empresa; que por isso um pedido de aumento em bruto chega
ampliado ao outro lado; e que o multiplicador se obtem dividindo o custo do
empregador pelo bruto, com a taxa de acidente da propria empresa conferida. Esta
no longo kolejny-poziom-005 (34SgUG7rf0U), capitulos "Ponad brutto" e
"Cztery ruchy".

DESCARTADO, e vai escrito:
  (1) o percentual dos encargos — muda por lei E varia por setor;
  (2) os valores de salario minimo, bruto e liquido do longo, que sao do ano;
  (3) a comparacao etat contra B2B, que e OUTRA familia de entrada errada e fica
      para outra peca — nao se empilha aqui.

## FONTES
O longo de onde este short foi extraido (kolejny-poziom-005, 34SgUG7rf0U) traz as
fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "kolejny-poziom",
    "pacote": "kolejny-poziom-s012",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A5C", "c1": "#2A9D8F", "c2": "#F5B841",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "34SgUG7rf0U",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short, alvo_short
    grava(SPEC, "fabrica/specs/kolejny-poziom-s012.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    INTERROGA = ("?", ";", ";")
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} (uso o PISO: voz pl puxa +)")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto (pl) "
          f"{s*0.982:.1f} a {s*1.044:.1f}  | teto 45")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars) | pergunta? "
          f"{'SIM' if tit.rstrip().endswith(INTERROGA) else 'NAO'}")
    print(f"aponta para: {SPEC['longo_existente']}")
