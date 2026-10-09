"""epomeno-epipedo-s015 — a pergunta nao e quanto custa, e em quantos anos volta.

ALAVANCA desta rodada, uma coisa so, e e no INSTRUMENTO (a regra 5 conta isso):
o contador de CANAL anda em degrau. As 10:15 o `channels.list` devolveu
statistics BYTE A BYTE identicas as de 09:15 nos tres canais — views
10700/12152/8406 e inscritos 67/16/8 — enquanto `videos.list` mostrava peca
individual indo de 0 a 67 na mesma hora. Logo as "nove leituras consecutivas
iguais de inscritos" que eu reportei NAO sao nove observacoes: valem duas ou
tres. Zero movimento continua sendo o que eu vi, mas o instrumento nao resolve
hora a hora e portanto nao sustenta nem "o experimento 37 nao funciona" nem
"funciona". Corrigi o 685 em parcial e escrevi o 686 (critico).
NUMERO DE PARTIDA: inscritos 8 / 16 / 67, e a proxima leitura que vale e so
depois de ~4 h.

ESTA PECA NAO MUDA NADA DO TRATAMENTO, de proposito. O `epomeno-s011` cruza as
12 h as 12:31 e e a PRIMEIRA peca de tratamento novo a ficar comparavel; meter
variavel nova no epomeno antes disso estragaria a unica leitura limpa que eu vou
ter hoje do experimento 38.

O QUE DEU CERTO: mirar o PISO no polones. O `kolejny-s014` saiu em 41,83 reais
contra 41,6 estimados (+0,6%), `PT42S` no contador, contra `PT44S` da peca
anterior que mirou o topo e deu +3,5%. Dois segundos de folga recuperados abaixo
do teto de 45.

O QUE NAO DEU: ZERO peca de tratamento novo passou das 12 h ainda — a mais velha
e o `epomeno-s011` com 9,7 h. O experimento 38 continua SEM veredito, e dizer
qualquer coisa sobre ele agora seria ler em idade fixa um processo de disparo que
vai de 1,9 h a 4,8 h (657).

DE ONDE SAI: longo `jAWKppvjAG8` (epomeno-epipedo-009, os anos ficticios de
seguro), capitulo "Ρώτα πάντα — σε πόσα χρόνια γυρίζει". O short ORIGINAL do
pacote da o CUSTO dos sete anos e a parcela mensal, e PARA ali: nunca faz a
pergunta do RETORNO. A entrada errada e aritmetica e de sequencia — pergunta-se
"quanto custa" e compara-se com a poupanca, quando o que se compra e um AUMENTO
MENSAL, e portanto o que decide e custo dividido pelo aumento, que da o numero de
meses ate voltar.

TITULO EM IMPERATIVO de segunda pessoa, que e o padrao do GR/26 (a pergunta pura
e sinal POLONES, seis de quinze contra dois a tres no GR).
FEED GR NAO RELIDO nesta rodada — lido as 04:1x, seis horas; FORA da janela de
quatro horas e meia do 623, e vai dito que nao foi relido.

IDENTIDADE: faixa ATUAL do canal `{ink #12263A, c1 #2A9D8F, c2 #E8A33D,
bg #F5F2EC}`, trilha `Inspired` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita o custo dos
# anos, nao cita a parcela mensal, nao cita o limite de anos do setor privado nem
# do publico, nao cita data de vigencia e nao nomeia orgao. Conferido A MAO campo
# por campo, porque o portao `narracao` conta QUANTIDADES por frase e NAO pega
# digito cru.
#
# A REGRA (g) MANDA: o custo dos anos ficticios e a parcela mensal sao amarrados
# ao salario minimo e MUDARAM este ano — o proprio longo tem um capitulo so para
# isso ("Το κόστος — άλλαξε φέτος"). Um short com o valor do ano passado fica
# errado e continua no ar. O que NAO envelhece e a PERGUNTA, e e ela que este
# short carrega.
#
# NUMERAIS NA NARRACAO: "dois numeros" e "uma pergunta", que descrevem o
# raciocinio. Uma quantidade por frase; o limite do portao e tres.
#
# O QUE O VIDEO AFIRMA: que o que se compra e um aumento MENSAL, logo a conta que
# decide e o que se paga dividido pelo que se passa a receber a mais por mes, e o
# resultado e o numero de meses ate o dinheiro voltar; e que a pergunta errada e
# "quanto custa". Esta no longo epomeno-epipedo-009 (`jAWKppvjAG8`), capitulos
# "Εκεί — η πράξη γίνεται απλή" e "Ρώτα πάντα — σε πόσα χρόνια γυρίζει".
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) o custo total e a parcela mensal — atados ao salario minimo, mudaram
#       este ano;
#   (2) os limites de anos por setor, que o short ORIGINAL ja usou e que sao de
#       lei;
#   (3) a data de vigencia e a data da solicitacao, de calendario.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Μη ρωτάς πόσο κοστίζει", "sub": "ρώτα πότε γυρίζει",
     "nar": "Ρωτάς πόσο κοστίζουν τα πλασματικά έτη και το συγκρίνεις με τις "
            "οικονομίες σου. Είναι η λάθος ερώτηση.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Τι αγοράζεις", "sub": "μηνιαία αύξηση",
     "nar": "Αυτό που αγοράζεις δεν είναι χρόνια. Είναι μια αύξηση που θα παίρνεις "
            "κάθε μήνα, για όσο ζεις.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Η πράξη", "sub": "δύο νούμερα",
     "nar": "Άρα η πράξη θέλει δύο νούμερα: τι πληρώνεις σήμερα, και πόσο "
            "παραπάνω παίρνεις κάθε μήνα μετά. Διαίρεσε το πρώτο με το δεύτερο.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Το αποτέλεσμα", "sub": "μήνες, όχι ευρώ",
     "nar": "Το αποτέλεσμα δεν είναι ευρώ, είναι μήνες. Είναι ο χρόνος σύνταξης "
            "που χρειάζεσαι για να γυρίσει πίσω το ποσό.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Κάνε εγγραφή", "sub": "για τα επόμενα",
     "nar": "Αν η απάντηση βγει δεκαετίες, το ξανασκέφτεσαι. Κάνε εγγραφή για τα "
            "επόμενα, και η ανάλυση είναι στο βίντεο.",
     "sem_cap": True},
]

THUMB = {"l1": "Πότε", "l2": "γυρίζει"}

COPY = """# epomeno-epipedo-s015

## TITULO
Πλασματικά Έτη: Η Σωστή Ερώτηση Δεν Είναι Πόσο Κοστίζουν αλλά σε Πόσα Χρόνια Επιστρέφουν

## TITULO SHORT
Ρώτα σε πόσα χρόνια γυρίζει

## DESCRICAO
Η πρώτη ερώτηση που κάνει σχεδόν όλος ο κόσμος είναι «πόσο κοστίζουν»; Είναι φυσική ερώτηση, και είναι η λάθος ερώτηση — γιατί το κόστος μόνο του δεν απαντά τίποτα. Το συγκρίνεις με τις οικονομίες σου, βλέπεις αν τα βγάζεις, και η απόφαση παίρνεται χωρίς να μπει στη μέση το νούμερο που μετράει.

Αυτό που αγοράζεις δεν είναι χρόνια. Είναι μια αύξηση που θα παίρνεις κάθε μήνα, για όσο ζεις. Και όταν αυτό που αγοράζεις είναι μηνιαία ροή, η σύγκριση με ένα εφάπαξ ποσό δεν στέκει αριθμητικά — λείπει ο χρόνος.

Η πράξη που λείπει θέλει δύο νούμερα: τι πληρώνεις σήμερα, και πόσο παραπάνω παίρνεις κάθε μήνα μετά. Διαιρείς το πρώτο με το δεύτερο, και το αποτέλεσμα δεν είναι ευρώ — είναι μήνες. Είναι ο χρόνος σύνταξης που χρειάζεσαι για να γυρίσει πίσω αυτό που έδωσες. Αν η απάντηση βγει δεκαετίες, το ξανασκέφτεσαι. Αν βγει λίγα χρόνια, η απόφαση είναι άλλη.

Τίποτα από αυτά δεν είναι επιχείρημα κατά της αναγνώρισης. Είναι το αντίθετο: με τη σωστή πράξη ξέρεις πότε συμφέρει, αντί να το αποφασίζεις με το συναίσθημα. Και πριν πληρώσεις οτιδήποτε, αξίζει να δεις αν υπάρχει χρόνος στον φάκελό σου που αναγνωρίζεται χωρίς πληρωμή — γιατί αυτός μετράει τα ίδια και κοστίζει μηδέν.

Εδώ δεν υπάρχει κόστος, δόση, όριο ετών ούτε ημερομηνία, και είναι σκόπιμο: το κόστος και η δόση είναι δεμένα με τον κατώτατο μισθό και άλλαξαν φέτος, ενώ η ερώτηση δεν αλλάζει. Τα ποσά με πηγή, τα όρια ανά τομέα, οι τρεις περιπτώσεις που συμφέρουν και η ημερομηνία που κλειδώνει την τιμή — είναι στο πλήρες βίντεο.

## COMENTARIO FIXADO
Το λάθος εδώ δεν είναι στην πράξη, είναι στην ερώτηση: ρωτάς «πόσο κοστίζει» και το συγκρίνεις με τις οικονομίες σου. Αυτό που αγοράζεις όμως είναι μηνιαία αύξηση, όχι χρόνια — άρα θέλεις δύο νούμερα και μία διαίρεση: τι πληρώνεις, δια πόσο παραπάνω παίρνεις κάθε μήνα. Το αποτέλεσμα είναι ΜΗΝΕΣ, ο χρόνος σύνταξης μέχρι να γυρίσει το ποσό. Και για να είμαι καθαρός, γιατί το βίντεο δεν είναι κατά της αναγνώρισης: με τη σωστή πράξη ξέρεις πότε συμφέρει. Πριν πληρώσεις, κοίτα και τον χρόνο που αναγνωρίζεται δωρεάν. Όποιος έκανε την πράξη, γράψτε στα σχόλια μόνο αν βγήκε χρόνια ή δεκαετίες — χωρίς ποσά.

## HASHTAGS
#Συνταξη #ΠλασματικαΕτη #EpomenoEpipedo

## TAGS
plasmatika eti, syntaxi, anagnorisi chronou, apodosi, miniaia afxisi, posa chronia gyrizei, asfalistika etoi, oikonomika, syntaxiodotisi, ypologismos, epomeno epipedo, dorean chronos, anergia, asfalisi, prosopika oikonomika

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita custo, dose,
limite de anos, data nem orgao. Conferido a mao campo por campo.

A REGRA (g) MANDA: o custo e a parcela estao atados ao salario minimo e MUDARAM
este ano — o longo tem um capitulo so para isso. A PERGUNTA nao envelhece, e e
ela que este short carrega.

NUMERAIS NA NARRACAO: "dois numeros" e "uma pergunta", que descrevem o
raciocinio.

O QUE O VIDEO AFIRMA: que o que se compra e um aumento MENSAL, logo a conta que
decide e o pago dividido pelo aumento mensal, e o resultado sao MESES ate o
dinheiro voltar; e que "quanto custa" e a pergunta errada. Esta no longo
epomeno-epipedo-009 (jAWKppvjAG8), capitulos "Εκεί — η πράξη γίνεται απλή" e
"Ρώτα πάντα — σε πόσα χρόνια γυρίζει".

DESCARTADO, e vai escrito:
  (1) o custo total e a parcela mensal, atados ao salario minimo;
  (2) os limites de anos por setor, que o short ORIGINAL ja usou;
  (3) a data de vigencia e a data da solicitacao.

## FONTES
O longo de onde este short foi extraido (epomeno-epipedo-009, jAWKppvjAG8) traz
as fontes oficiais e as datas. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s015",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#12263A", "c1": "#2A9D8F", "c2": "#E8A33D",
               "bg": "#F5F2EC"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "jAWKppvjAG8",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short, alvo_short
    grava(SPEC, "fabrica/specs/epomeno-epipedo-s015.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} (TOPO: centro el ~ -3,2%)")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto "
            f"{s*0.937:.1f} a {s*0.991:.1f}")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
