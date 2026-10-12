"""epomeno-epipedo-s018 — MARGINAL contra TOTAL. O bonus nao te faz perder.

ALAVANCA: nenhuma mudanca de forma. Onze cenas, uma frase curta por cena, mira
do canal. Braco de dez-a-onze cenas no epomeno, n=2 antes desta (s016, s017).

DE ONDE SAI, e isto e a regra (h) funcionando de ponta a ponta pela PRIMEIRA
vez: longo `eZ697VNYCPU`, "Μισθός 920€, Καθαρά 772€", publicado em 11/08.
**Ele NAO tem spec no repositorio** — nem por nome nem por conteudo. A origem foi
achada pelo `pauta_viva.py` (playlist de uploads, ao vivo), os capitulos pelo
`capitulos_do_longo.py`, e o TEXTO pela legenda que a propria maquina subiu:
nove capitulos, 75 falas, 9.249 chars.
REGISTRADO: a descricao da os TITULOS dos capitulos e nada mais. Escrever a
partir de titulo de capitulo seria INVENTAR conteudo; o texto vem da legenda.

FAMILIA NOVA. Ja usadas: LIMIAR (s015 kolejny), COMPOSICAO (s016 kolejny),
ORDEM (s017 kolejny), DEFASAGEM NO TEMPO (s018 kolejny), ARITMETICA media
contra produto (s013 labtreinamento) e CONDICAO/ACAO (s017 epomeno, hoje).
Esta e **MARGINAL contra TOTAL**: aplicar a aliquota ao rendimento INTEIRO em
vez de so a fatia acima do limite. E a entrada errada mais caradura que existe
em imposto progressivo, porque faz a pessoa RECUSAR dinheiro — recusar hora
extra, recusar bonus, pedir para receber no ano seguinte.

A regra (f) e respeitada: o `s017` de hoje era CONDICAO/ACAO (reducao que exige
pedido), familia diferente.

TITULO: imperativo de segunda pessoa, a forma medida do GR (09/10).
FEED GR NAO LIDO nesta rodada, e isso vai dito em vez de suposto.

IDENTIDADE: faixa ATUAL do canal, trilha `Inspired` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# O LONGO E FEITO DE NUMERO COM DATA COLADA, e a regra (g) tira TODOS:
#   o salario minimo bruto e liquido, os 148 euros de desconto, a data de
#   vigencia do minimo, os seis degraus da escala e cada aliquota deles, as
#   aliquotas do ano anterior, os limites de cada degrau, as faixas de idade e
#   o imposto zero delas, os liquidos comparados de 772/781/797, a diferenca
#   mensal e anual entre colegas, os ganhos de 100/300/500 euros por faixa de
#   renda, os 8/25/42 euros por mes, os 2.500 em cinco anos, o plano de 90 dias
#   e o limite das despesas eletronicas.
# Todos mudam por lei ou por ato do ministerio. NENHUM entra.
#
# O QUE A PECA CARREGA, e nao envelhece: numa escala progressiva a aliquota do
# degrau novo incide SO na fatia acima do limite, nunca no rendimento inteiro.
# Logo passar de degrau nao faz ninguem receber menos, e o bonus vale sempre —
# so nao vale inteiro. Isso e aritmetica da propria forma do imposto, e esta
# escrito com todas as letras no longo: *"η κλίμακα δεν φορολογεί όλο το
# εισόδημα με έναν συντελεστή. Κάθε κομμάτι πληρώνει το δικό του σκαλοπάτι"* e
# *"το μπόνους αξίζει πάντα, απλώς όχι ολόκληρο"*.
#
# ZERO DIGITO e ZERO NUMERAL na narracao, conferido campo a campo a mao. Nao ha
# nem ordinal de contagem: "το επόμενο σκαλοπάτι" e nao "το δεύτερο".
#
# POR QUE ESTA FAMILIA E A CERTA PARA UM SHORT, e nao e estetica: esta entrada
# errada nao faz a pessoa pagar imposto a mais — faz ela RECUSAR dinheiro.
# Quem acha que o degrau incide no total recusa hora extra e pede para adiar o
# bonus. O custo e invisivel e voluntario, que e o que mantem o erro vivo.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Σου δίνουν μπόνους", "sub": "και φοβάσαι το σκαλοπάτι", "nar": "Σου δίνουν μπόνους και φοβάσαι το σκαλοπάτι.", "sem_cap": True},
    {"layout": "item", "kicker": "Ο φόβος", "preco": "βγαίνει λάθος", "nar": "Ο φόβος λέει πως θα βγεις χαμένος συνολικά.", "sem_cap": True},
    {"layout": "item", "kicker": "Η κλίμακα", "preco": "δεν είναι ένας φόρος", "nar": "Η κλίμακα δεν φορολογεί τα πάντα μαζί.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Κάθε κομμάτι", "sub": "στο δικό του σκαλοπάτι", "nar": "Κάθε κομμάτι πληρώνει το δικό του σκαλοπάτι.", "sem_cap": True},
    {"layout": "item", "kicker": "Άρα", "preco": "μόνο η κορυφή", "nar": "Ακριβαίνει μόνο το κομμάτι πάνω από το όριο.", "sem_cap": True},
    {"layout": "item", "kicker": "Τα από κάτω", "preco": "δεν αγγίζονται", "nar": "Όσα είχες από κάτω μένουν όπως ήταν.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Δηλαδή", "sub": "δεν χάνεις ποτέ", "nar": "Δηλαδή δεν παίρνεις ποτέ λιγότερα από πριν.", "sem_cap": True},
    {"layout": "item", "kicker": "Το μπόνους", "preco": "αξίζει πάντα", "nar": "Το μπόνους αξίζει πάντα να το πάρεις.", "sem_cap": True},
    {"layout": "item", "kicker": "Απλώς", "preco": "όχι ολόκληρο", "nar": "Απλώς δεν φτάνει ολόκληρο στην τσέπη σου.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Μην αρνηθείς", "sub": "υπολόγισε το καθαρό", "nar": "Μην το αρνηθείς. Υπολόγισε το καθαρό του.", "sem_cap": True},
    {"layout": "cta", "kicker": "Επόμενο Επίπεδο", "sub": "κάνε εγγραφή", "nar": "Αν σου έλυσε μια απορία, κάνε εγγραφή.", "sem_cap": True}
]

THUMB = {"l1": "Μόνο η", "l2": "κορυφή"}

COPY = """# epomeno-epipedo-s018

## TITULO
Το Μπόνους Δεν Σε Ζημιώνει: Στην Κλίμακα Ακριβαίνει Μόνο Το Κομμάτι Πάνω Από Το Όριο

## TITULO SHORT
Μην αρνηθείς το μπόνους

## DESCRICAO
Ο φόβος του σκαλοπατιού είναι ο πιο ακριβός παρεξηγημένος κανόνας στη φορολογία μισθωτού — και είναι ακριβός με τον χειρότερο τρόπο, γιατί δεν σου παίρνει χρήματα: σε κάνει να **αρνηθείς** χρήματα.

Η λογική του λάθους είναι απλή και λανθασμένη: «αν περάσω στο επόμενο σκαλοπάτι, όλο το εισόδημά μου θα φορολογηθεί με τον νέο, μεγαλύτερο συντελεστή, άρα μπορεί να βγω χαμένος». Από εκεί προκύπτουν οι αποφάσεις που κοστίζουν: αρνούμαι υπερωρίες, ζητώ να πάρω το μπόνους τον επόμενο χρόνο, διστάζω για μια αύξηση.

**Η κλίμακα δεν δουλεύει έτσι.** Δεν φορολογεί όλο το εισόδημα με έναν συντελεστή. Κάθε κομμάτι του εισοδήματος πληρώνει το δικό του σκαλοπάτι: ό,τι είχες από κάτω μένει ακριβώς όπως ήταν, και ο νέος, μεγαλύτερος συντελεστής πιάνει **μόνο** τη φέτα που ξεπερνά το όριο.

Από αυτό βγαίνει το συμπέρασμα που λύνει το ζήτημα μια και καλή: περνώντας σκαλοπάτι δεν παίρνεις ποτέ λιγότερα απ' ό,τι έπαιρνες πριν. Το μπόνους και η υπερωρία αξίζουν πάντα — απλώς δεν φτάνουν ολόκληρα στην τσέπη, και αυτό είναι άλλο πράγμα από το «βγαίνω χαμένος».

Αυτό το short δεν αναφέρει επίτηδες ούτε συντελεστές, ούτε όρια σκαλοπατιών, ούτε ποσά, ούτε ηλικιακές ομάδες, ούτε ημερομηνίες: όλα αυτά αλλάζουν με νόμο, και είναι στο πλήρες βίντεο μαζί με την πηγή τους. Η αριθμητική της προοδευτικής κλίμακας δεν αλλάζει.

Στο πλήρες βίντεο: τα τρία νούμερα της απόδειξης πληρωμής, η κλίμακα με τα όρια και τους συντελεστές του έτους, γιατί δύο συνάδελφοι με τον ίδιο μισθό παίρνουν άλλα καθαρά, οι τρεις παγίδες που εξανεμίζουν το όφελος, και το σχέδιο για να μη σου γλιστρήσει.

## COMENTARIO FIXADO
Το λάθος αυτό δεν σου παίρνει χρήματα — σε κάνει να αρνηθείς χρήματα, και γι' αυτό επιβιώνει τόσο: κανένα χαρτί δεν σου έρχεται να σου πει τι έχασες. Η αριθμητική σε μία γραμμή: ο νέος συντελεστής πιάνει μόνο τη φέτα πάνω από το όριο, όχι όλο το εισόδημα, άρα περνώντας σκαλοπάτι δεν παίρνεις ποτέ λιγότερα από πριν. Το μπόνους αξίζει πάντα· απλώς δεν φτάνει ολόκληρο. Επίτηδες δεν έβαλα εδώ ούτε συντελεστή ούτε όριο: αλλάζουν με νόμο και είναι στο βίντεο με την πηγή τους — αυτό που δεν αλλάζει είναι ο τρόπος που δουλεύει η κλίμακα. Γράψτε αν σας έτυχε να διστάσετε για υπερωρία ή μπόνους γι' αυτόν τον λόγο: μαζεύω πραγματικά περιστατικά.

## HASHTAGS
#Φόροι #Μισθός #ΕπόμενοΕπίπεδο

## TAGS
forologiki klimaka, oriako skalopati, bonus kai foros, yperories foros, parakratisi forou, apodeixi pliromis, mikto kai kathara, progressive klimaka, foros misthoton, skalopati eisodimatos, epomeno epipedo, oikonomika ellada, misthodosia, arithmitiki tou forou, dilosi eisodimatos

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
Conferido a mao campo por campo. Nem ordinal de contagem entrou: "το επόμενο
σκαλοπάτι" e nao "το δεύτερο", porque ordinal ja e quantidade e o portao
`narracao` conta quantidades por frase sem ver digito cru.

A REGRA (g) MANDA, e o longo e feito de numero com data colada. Ficaram FORA: o
salario minimo bruto e liquido, os 148 euros de desconto, a data de vigencia do
minimo, os seis degraus e cada aliquota deles, as aliquotas do ano anterior, os
limites de cada degrau, as faixas de idade e o imposto zero delas, os liquidos
comparados entre colegas, os ganhos por faixa de renda, os valores mensais, o
acumulado de cinco anos, o plano de noventa dias e o limite das despesas
eletronicas. Todos mudam por lei ou por ato do ministerio.

O QUE A PECA CARREGA, e nao envelhece: numa escala progressiva a aliquota do
degrau novo incide SO na fatia acima do limite, nunca no rendimento inteiro.
Logo passar de degrau nao faz ninguem receber menos, e o bonus vale sempre — so
nao vale inteiro. Esta escrito com todas as letras no longo `eZ697VNYCPU`:
"η κλίμακα δεν φορολογεί όλο το εισόδημα με έναν συντελεστή. Κάθε κομμάτι
πληρώνει το δικό του σκαλοπάτι" e "το μπόνους αξίζει πάντα, απλώς όχι
ολόκληρο".

POR QUE ESTA FAMILIA E A CERTA, e nao e estetica: esta entrada errada nao faz a
pessoa pagar imposto a mais — faz ela RECUSAR dinheiro. Quem acha que o degrau
incide no total recusa hora extra e pede para adiar o bonus. O custo e invisivel
e voluntario, e e isso que mantem o erro vivo.

## FONTES
O longo de onde este short foi extraido (`eZ697VNYCPU`, de 11/08) declara que os
numeros dele vem da lei e dos textos oficiais do ministerio. Este short NAO
introduz numero novo sobre o mundo, entao nao exige fonte institucional nova.

NOTA DE PROCEDENCIA, porque esta origem e a primeira do seu tipo: o longo NAO tem
spec no repositorio. Os capitulos sairam da descricao publicada (regra h) e o
TEXTO saiu da faixa de legenda que a propria maquina subiu — 75 falas, 9.249
caracteres, lidos no run do `capitulos.yml` com `legenda=true`. Nenhuma frase
desta peca foi inferida de titulo de capitulo.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s018",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#16283C", "c1": "#2E7BB4", "c2": "#E0A02E",
               "bg": "#F3F7FA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "eZ697VNYCPU",
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
    grava(SPEC, "fabrica/specs/epomeno-epipedo-s018.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short(SPEC["slug"])
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} | TOPO no grego (residuo -3,2%)")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'}")
    print(f"por plano: {s/len(SHORT):.2f}s | falas de legenda: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
