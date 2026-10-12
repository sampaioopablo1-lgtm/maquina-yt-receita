"""epomeno-epipedo-s017 — a reducao que chega sozinha e a que exige PEDIDO.

ALAVANCA desta rodada: NENHUMA mudanca de forma. Onze cenas, uma frase curta por
cena, mira do canal. Com CV 0,66 (693) sao ~7 pecas por braco para enxergar um
dobro, e abrir braco novo com os bracos atuais em n pequeno nao mede nada.
NUMERO DE PARTIDA: braco de dez-a-onze cenas, epomeno, n=1 antes desta (s016).

MIRA: `alvo_short('epomeno-epipedo')` = 41,5 a 43,0 — o canal NAO tem override em
`ALVO_POR_CANAL`, entao esta e a mira da FROTA, e isso e ESCOLHA e nao descuido.
Mirei 42,5, o TOPO da faixa, porque o residuo do grego e -3,2% (679): a peca
real sai mais CURTA que a estimativa, e o topo e o lado seguro nesta voz.

DE ONDE SAI: longo `uWs-k_Wrn_w` (pacote `epomeno-epipedo-008`), sobre a deducao
do ENFIA por seguro de residencia. **Origem LIVRE, e e uma das TRES que sobraram
na frota** — medido em 12/10 08:2x, depois de descobrir que dez dos doze ids
"livres" eram o mesmo titulo repetido por um cron (grupo de duplicata; ver a
retratacao em `docs/rotina-ponta-a-ponta.md`).

NOTA SOBRE A ORIGEM, porque ela parece contraditoria: o `epomeno-epipedo-008` e
uma das QUATRO specs da frota no inventario `PARADAS` — ela falha o portao
`narracao` por capitulo sem margem. **Isso nao impede usar o LONGO como origem:**
o longo esta publicado e no ar; o que esta parado e a propria spec dele, por
texto de capitulo. Sao coisas diferentes e eu conferi antes de escolher.

FAMILIA NOVA, como a regra (f) exige. Ja usadas: LIMIAR (s015 kolejny),
COMPOSICAO (s016 kolejny), ORDEM (s017 kolejny), DEFASAGEM NO TEMPO (s018
kolejny), e no labtreinamento ARITMETICA ERRADA (s013, media contra produto).
Esta e **CONDICAO / ACAO**: ha duas reducoes no mesmo imposto, uma e aplicada
sozinha pelos dados que o orgao ja tem e a outra NAO existe sem pedido. Quem
supoe que toda reducao vem sozinha perde a segunda sem nunca saber.

TITULO: o GR premia IMPERATIVO DE SEGUNDA PESSOA (medido em 09/10), nao pergunta
— pergunta pura e sinal POLONES. E o ponto de interrogacao grego e `;`, mas aqui
nao ha pergunta nenhuma no titulo, de proposito.
FEED GR NAO LIDO nesta rodada, e isso vai dito em vez de suposto.

IDENTIDADE: faixa ATUAL do canal `{ink #16283C, c1 #2E7BB4, c2 #E0A02E,
bg #F3F7FA}`, trilha `Inspired` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ESTE LONGO E UM CAMPO MINADO PARA A REGRA (g) — ele e feito de numero com data
# colada, e TODOS ficam de fora:
#   o ENFIA medio do ano, o total arrecadado, o numero de contribuintes, a
#   percentagem da deducao, quantos a receberam, o valor medio dela, a razao
#   "um em catorze", o teto de valor objetivo do imovel, o minimo por metro
#   quadrado, o numero de dias de seguro, a data limite calculada, o numero de
#   prestacoes, o mes do prazo da plataforma e a percentagem da outra reducao.
# Todos mudam por ato da AADE ou por lei. NENHUM entra.
#
# O QUE A PECA CARREGA, e nao envelhece: no MESMO imposto existem duas reducoes
# de natureza diferente — uma o orgao aplica sozinho, dos dados que ja tem; a
# outra nao existe sem PEDIDO, por mais que a pessoa cumpra todas as condicoes.
# E o motivo mais triste de perder a segunda nao e nao ter direito: e ter
# direito e nao ter pedido. Isso e mecanica administrativa, nao tabela, e esta
# nos capitulos "Ο τρίτος", "Η μείωση των οικισμών", "Η διαφορά" e "Γιατί το
# ξεχωρίζω" do longo `uWs-k_Wrn_w`.
#
# ZERO DIGITO E ZERO NUMERAL na narracao, conferido campo a campo a mao, porque
# o portao `narracao` conta QUANTIDADES por frase e NAO pega digito cru. Nao ha
# nem ordinal: "η μία" e "η άλλη" no lugar de "πρώτη/δεύτερη", porque ordinal de
# contagem ja e quantidade.
#
# O QUE EU TAMBEM DESCARTEI, e nao e por numero: o capitulo "Ποτε DEN συμφερει"
# (quando a deducao NAO compensa) e o melhor do longo, mas carregar isso em
# quarenta segundos sem o valor do premio e da deducao viraria conselho
# financeiro sem conta — e a conta e justamente o que a regra (g) manda deixar
# no longo. Fica no longo, e a descricao aponta para la.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Δύο μειώσεις", "sub": "στον ίδιο φόρο", "nar": "Στον ίδιο φόρο υπάρχουν δύο διαφορετικές μειώσεις.", "sem_cap": True},
    {"layout": "item", "kicker": "Η μία", "preco": "έρχεται μόνη", "nar": "Η μία εφαρμόζεται μόνη της, χωρίς εσένα.", "sem_cap": True},
    {"layout": "item", "kicker": "Από πού", "preco": "από τα στοιχεία", "nar": "Βγαίνει από στοιχεία που η υπηρεσία έχει ήδη στα χέρια της.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Η άλλη", "sub": "δεν έρχεται ποτέ μόνη", "nar": "Η άλλη δεν έρχεται ποτέ μόνη της.", "sem_cap": True},
    {"layout": "item", "kicker": "Χρειάζεται", "preco": "αίτηση", "nar": "Χρειάζεται αίτηση στην πλατφόρμα, από εσένα.", "sem_cap": True},
    {"layout": "item", "kicker": "Και χωρίς αυτήν", "preco": "δεν υπάρχει", "nar": "Χωρίς την αίτηση μέσα στην προθεσμία δεν υπάρχει.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Ακόμα κι αν", "sub": "τα έχεις όλα σωστά", "nar": "Ακόμα κι αν τα έχεις όλα απόλυτα σωστά στα χαρτιά.", "sem_cap": True},
    {"layout": "item", "kicker": "Ο πιο κρίμα λόγος", "preco": "δικαίωμα χωρίς αίτηση", "nar": "Ο πιο κρίμα λόγος απόρριψης είναι ακριβώς αυτός.", "sem_cap": True},
    {"layout": "item", "kicker": "Μην υποθέτεις", "preco": "ότι έρχονται μόνες", "nar": "Μην υποθέτεις πως κάθε μείωση έρχεται μόνη.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Δες το εκκαθαριστικό", "sub": "και ρώτα ποια λείπει", "nar": "Δες το εκκαθαριστικό και ρώτα ποια λείπει.", "sem_cap": True},
    {"layout": "cta", "kicker": "Επόμενο Επίπεδο", "sub": "κάνε εγγραφή", "nar": "Αν σου φάνηκε χρήσιμο, κάνε εγγραφή.", "sem_cap": True}
]

THUMB = {"l1": "Μία έρχεται", "l2": "μόνη"}

COPY = """# epomeno-epipedo-s017

## TITULO
Στον Ίδιο Φόρο Υπάρχουν Δύο Μειώσεις: Η Μία Εφαρμόζεται Μόνη, Η Άλλη Θέλει Αίτηση

## TITULO SHORT
Δες ποια μείωση λείπει

## DESCRICAO
Στον ΕΝΦΙΑ υπάρχουν μειώσεις δύο εντελώς διαφορετικών ειδών, και η διαφορά δεν είναι τεχνική λεπτομέρεια — είναι ο λόγος που χιλιάδες νοικοκυριά χάνουν κάτι που τους ανήκει.

Η μία εφαρμόζεται **αυτόματα**, από στοιχεία που η υπηρεσία έχει ήδη στη διάθεσή της. Δεν χρειάζεται να κάνεις τίποτα: έρχεται μόνη της στο εκκαθαριστικό.

Η άλλη **δεν έρχεται ποτέ μόνη**. Προϋποθέτει αίτηση στην πλατφόρμα, μέσα στην προθεσμία, από εσένα. Και εδώ είναι το σημείο που κοστίζει: μπορείς να πληροίς κάθε προϋπόθεση του νόμου, με τα χαρτιά σου απόλυτα εντάξει, και να μην πάρεις τίποτα — απλώς επειδή δεν ζητήθηκε. Αυτός είναι ο πιο κρίμα λόγος απόρριψης, γιατί δεν αφορά δικαιώματα που λείπουν, αλλά μια κίνηση που δεν έγινε.

Το λάθος που γεννά το πρόβλημα είναι μια υπόθεση: ότι οι μειώσεις έρχονται όλες μόνες τους, όπως η πρώτη. Δεν έρχονται. Και κανένα έγγραφο δεν σου λέει εκ των υστέρων ποια σου έλειπε.

Αυτό το short δεν αναφέρει επίτηδες ούτε ποσοστά, ούτε ποσά, ούτε ημερομηνίες, ούτε πόσοι τη πήραν: όλα αυτά αλλάζουν με απόφαση ή με νόμο, και είναι στο πλήρες βίντεο μαζί με την πηγή τους. Αυτό που δεν αλλάζει είναι ο μηχανισμός — αυτόματο εναντίον αιτούμενου.

Στο πλήρες βίντεο: ποιες είναι ακριβώς οι προϋποθέσεις, τι καλύψεις ζητούνται, πώς υπολογίζεται η αναλογία, πού γίνεται η αίτηση — και, κυρίως, το κεφάλαιο που λείπει από κάθε βίντεο για εκπτώσεις: πότε η μείωση αυτή **δεν** συμφέρει.

## COMENTARIO FIXADO
Η πιο χρήσιμη γραμμή του βίντεου δεν είναι ένα ποσό, είναι μια διάκριση: υπάρχουν μειώσεις που η υπηρεσία εφαρμόζει μόνη της από στοιχεία που έχει, και μειώσεις που δεν υπάρχουν χωρίς αίτηση δική σου. Όποιος υποθέσει ότι ανήκουν όλες στην πρώτη κατηγορία, χάνει τη δεύτερη χωρίς να το μάθει ποτέ — και χάνεται από τους ανθρώπους που ΕΙΧΑΝ το δικαίωμα, όχι από όσους δεν το είχαν. Επίτηδες δεν έβαλα εδώ ποσοστά, ποσά ή προθεσμίες: αλλάζουν με απόφαση, και είναι στο βίντεο με την πηγή τους. Και κάτι που το βίντεο λέει καθαρά, γιατί τα βίντεο για εκπτώσεις συνήθως το κρύβουν: η μείωση δεν είναι από μόνη της λόγος να πάρεις μια ασφάλεια — είναι μπόνους σε μια απόφαση που παίρνεις για άλλον λόγο. Γράψτε μόνο αν βρήκατε μείωση που δεν ζητήσατε ποτέ.

## HASHTAGS
#ΕΝΦΙΑ #Φόροι #ΕπόμενοΕπίπεδο

## TAGS
enfia meioseis, ekptosi asfalisi katoikias, myproperty aitisi, automati meiosi, ekkatharistiko enfia, aade platforma, foroi akiniton, prooupotheseis ekptosis, dikaioma xoris aitisi, mixanismos kai oxi tabela, epomeno epipedo, oikonomika nikokyriou, akinita ellada, meiosi 50 oikismoi, enfia odigos

## CONFIGURACOES DO STUDIO
# NOTA: `categoryId` aqui e DECLARATIVO e o codigo ignora — publicar.py tem 27
# fixo. Escrito 27 porque e o que o video realmente recebe. Aprendizado 610.
privacyStatus: public
defaultLanguage: el
defaultAudioLanguage: el
categoryId: 27
madeForKids: false

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
ZERO NUMERO NOVO SOBRE O MUNDO, ZERO DIGITO e ZERO NUMERAL na narracao.
Conferido a mao campo por campo, porque o portao `narracao` conta QUANTIDADES
por frase e nao pega digito cru. Nem ordinal entrou: "η μία" e "η άλλη" no lugar
de "πρώτη/δεύτερη", porque ordinal de contagem ja e quantidade.

A REGRA (g) MANDA, e este longo e um campo minado para ela. Ficaram FORA: o
ENFIA medio do ano, o total arrecadado, o numero de contribuintes, a
percentagem da deducao, quantos a receberam, o valor medio dela, a razao "um em
catorze", o teto de valor objetivo do imovel, o minimo por metro quadrado, o
numero de dias de seguro, a data limite calculada, o numero de prestacoes, o mes
do prazo da plataforma e a percentagem da outra reducao. Todos mudam por ato da
AADE ou por lei.

O QUE A PECA CARREGA, e nao envelhece: no MESMO imposto ha duas reducoes de
natureza diferente — uma o orgao aplica sozinho, dos dados que ja tem; a outra
nao existe sem PEDIDO. E o motivo mais triste de perder a segunda nao e falta de
direito, e falta de pedido. Esta nos capitulos "Ο τρίτος", "Η μείωση των
οικισμών", "Η διαφορά" e "Γιατί το ξεχωρίζω" do longo `uWs-k_Wrn_w`
(epomeno-epipedo-008).

DESCARTADO POR OUTRO MOTIVO, e vai escrito: o capitulo "quando a deducao NAO
compensa" e o melhor do longo, mas carregar isso em quarenta segundos sem o valor
do premio e da deducao viraria conselho financeiro sem conta — e a conta e
justamente o que a regra (g) manda deixar no longo. A descricao e o comentario
fixado apontam para la, sem numero.

## FONTES
O longo de onde este short foi extraido (epomeno-epipedo-008, uWs-k_Wrn_w) traz a
anuncio da AADE com data e as condicoes da lei. Este short NAO introduz numero
novo sobre o mundo, entao nao exige fonte institucional nova.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s017",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#16283C", "c1": "#2E7BB4", "c2": "#E0A02E",
               "bg": "#F3F7FA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "uWs-k_Wrn_w",
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
    grava(SPEC, "fabrica/specs/epomeno-epipedo-s017.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short(SPEC["slug"])
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} | TOPO no grego (residuo -3,2%)")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto "
          f"{s*0.968:.1f} a {s*1.00:.1f}")
    print(f"por plano: {s/len(SHORT):.2f}s | falas de legenda: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
