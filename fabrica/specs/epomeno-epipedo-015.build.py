"""epomeno-epipedo-015 — δύο επίσημοι δείκτες τιμών, και ποιος αγγίζει το χαρτί σου.

ALAVANCA ATACADA: A (travessia short -> longo). NUMERO DE PARTIDA: a melhor
travessia do canal e 79,8% (pacote 008, 540 short -> 431 longo) e a mediana dos
treze lidos e 29,9%. O 014 abriu o experimento 30 e AINDA NAO TEM LEITURA — as
metricas pararam em 04/10/2026 01:09 e ele foi publicado em 05/10 18:36.

POR QUE ESTE PACOTE OBEDECE A FAIXA DE 12 MIN, e nao os ~556 s que o 008 usou
para fazer 79,8%: porque o aprendizado 599 registrou que duracao esta
PERFEITAMENTE CONFUNDIDA com data neste canal, e o experimento aberto para
desconfundir e o 30 — que esta aberto e sem leitura. Baixar a duracao agora
seria AFROUXAR uma regra escrita (`liberado`: 12 a 15 min) antes do dado que
poderia justificar. A rotina e explicita: apertar um portao por dado novo e
desejavel, afrouxar nao. Entao este pacote fica no piso, 9 capitulos, ~730 s,
igual ao 014 — e o braco de comparacao em nove minutos sai DEPOIS que o 014 for
lido, nao antes.

EIXO, e por que ele e novo. Os catorze anteriores falam de moradia, salario
minimo, conta de luz (duas vezes), juros, inflacao (uma vez, pacote 006: "3,4%
e carne 14,3%"), pensao, ENFIA, anos ficticios, tekmiria, IVA, custo por
quilometro e hora extra. O 006 citou UM numero de inflacao e fez 10,5% de
travessia. Este pacote nao cita NENHUM: o assunto nao e quanto e a inflacao, e
que para a Grecia existem DOIS indices oficiais de preco no mesmo mes, com
bases diferentes, conteudos diferentes e usos legais diferentes — e so um deles
entra no papel que o espectador tem na gaveta.

A DECISAO COM PRAZO (o padrao das tres melhores travessias do canal, 79,8%,
59,8% e 58,8%): o mes de aniversario do contrato de aluguel. A ELSTAT publica
toda vez, junto do indice nacional, a `Ανακοίνωση Αναπροσαρμογής Μισθωμάτων`.
O numero que decide nao e meu: e o do mes que esta escrito no contrato DELE.

POR QUE ESTE CANAL PODIA SER FEITO ESTA RODADA, depois de eu ter deixado ele na
cabeca da fila as 18:09 por falta de fonte. O `docs/publicar-pela-sandbox.md`
diz que a Grecia nao tem o par "orgao que aplica + publicador do texto", porque
`efka.gov.gr` e `et.gr` sao apps JavaScript e `aade.gr` da 403. Isso continua
verdade — e eu medi mais quatro hosts nesta rodada, todos reprovados:
`bankofgreece.gr` 403, `ypergasias.gov.gr` e `minfin.gr` 202 (pagina de
desafio), `dypa.gov.gr` timeout, `hdigf.gr` (o TEKE) timeout. O par que fechou
NAO e grego-grego, e statistics.gr + ec.europa.eu:

    ELSTAT (statistics.gr)        -> publica o indice NACIONAL, base 2020=100,
                                     e com ele a anuncio de reajuste de aluguel
    Eurostat (ec.europa.eu)       -> define o HARMONIZADO, base 2025=100,
                                     Regulamento (UE) 2016/792, e publica a
                                     lista do que fica FORA
    BCE (ecb.europa.eu)           -> usa o harmonizado como medida do objetivo
                                     E ADMITE, na propria pagina, que incluir o
                                     custo da casa propria representaria melhor
                                     a inflacao das familias

A terceira e a mais forte que eu consegui hoje: o furo que a Eurostat registra
como CATEGORIA EXCLUIDA (04.2, alugueis imputados) o BCE registra como
RESSALVA. Dois orgaos independentes, a mesma admissao, cada um na sua pagina.

O QUE EU NAO AFIRMO, e e deliberado: que a ELSTAT publica tambem o
harmonizado. A pagina DKT88 abriu 200 mas voltou com a descricao VAZIA, so
navegacao — entao eu nao tenho isso medido e nao entra no video. Fica anotado
para quem pegar o canal com rota melhor.

ALAVANCA B: resposta dentro dos primeiros duzentos segundos. Ela fecha na cena
14 (o passo dois da conta: abrir o anuncio do mes da escritura), e a estimativa
corrigida pelo residuo da voz (aprendizado 575) esta impressa no rodape deste
arquivo. A `el-GR-NestorasNeural` tem residuo de -0,1% com n=519.

TITULO PROPRIO DO SHORT: tem (aprendizado 548).
"""

import json

CENAS = []

# Resolvidos por `pg_net` dentro do Postgres (aprendizado 574): `net.http_get`
# para api.pexels.com com a chave lida do `config` na mesma consulta, entao ela
# nao atravessa a sandbox nem o chat.
#
# QUATRO b-rolls, e cada um esta debaixo da frase que ele literalmente mostra.
# O 5103988 e um caixa de supermercado comum, NAO um turista: o capitulo 5 diz
# que o indice mede toda compra feita no territorio, inclusive de quem nao mora
# aqui, e um caixa de supermercado mostra "compra feita no territorio" sem eu
# afirmar que aquela pessoa e turista. Clipe que diz mais do que a narracao e
# tao ruim quanto clipe que nao casa.
BROLL = {
    7263305: ("https://videos.pexels.com/video-files/7263305/7263305-hd_1280_720_25fps.mp4",
              "MART PRODUCTION",
              "https://www.pexels.com/video/a-man-reading-newspaper-7263305/"),
    8960547: ("https://videos.pexels.com/video-files/8960547/8960547-hd_1280_720_25fps.mp4",
              "Ivan S",
              "https://www.pexels.com/video/person-reading-a-contract-8960547/"),
    5103988: ("https://videos.pexels.com/video-files/5103988/5103988-hd_1280_720_30fps.mp4",
              "Gustavo Fring",
              "https://www.pexels.com/video/woman-getting-things-out-of-grocery-basket-at-billing-counter-5103988/"),
    5981290: ("https://videos.pexels.com/video-files/5981290/5981290-hd_1366_720_25fps.mp4",
              "https://kaboompics.com/",
              "https://www.pexels.com/video/a-woman-recording-her-receipts-in-a-planner-5981290/"),
}


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def B(kicker, sub, nar, q, pexels_id=None, cap=None):
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q}
    if pexels_id and pexels_id in BROLL:
        link, autor, pagina = BROLL[pexels_id]
        c["broll_url"] = link
        c["broll_credito"] = {"pexels_id": pexels_id, "autor": autor,
                              "url": pagina}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ==================== ΤΑ ΠΡΩΤΑ ΔΙΑΚΟΣΙΑ ΔΕΥΤΕΡΟΛΕΠΤΑ ========================

# -------------------------------------------------------------------- cap 1
B("Δύο αριθμοί", "για τον ίδιο μήνα",
  "Διαβάζεις στις ειδήσεις ότι ο πληθωρισμός στην Ελλάδα είναι ένα ποσοστό. "
  "Για την ίδια χώρα και τον ίδιο μήνα όμως υπάρχουν δύο επίσημα ποσοστά.",
  "person reading newspaper at a table", 7263305,
  cap="Δύο επίσημοι δείκτες για τον ίδιο μήνα")
T("Κανένας δεν είναι λάθος", "μετρούν άλλα πράγματα",
  "Δεν είναι λάθος κανένα από τα δύο. Μετρούν διαφορετικά πράγματα, τα βγάζουν "
  "διαφορετικοί φορείς, και έχουν διαφορετική χρήση μέσα στον νόμο.")
T("Ο πρώτος", "ο εθνικός δείκτης",
  "Ο ένας λέγεται Εθνικός Δείκτης Τιμών Καταναλωτή. Τον βγάζει η Ελληνική "
  "Στατιστική Αρχή, και είναι ο δείκτης της χώρας για τη δική της χρήση.")
T("Ο δεύτερος", "ο εναρμονισμένος",
  "Ο άλλος λέγεται Εναρμονισμένος Δείκτης Τιμών Καταναλωτή. Τον ορίζει "
  "ευρωπαϊκός κανονισμός, ώστε τα κράτη μέλη να συγκρίνονται μεταξύ τους.")
T("Το γράφει η Eurostat", "στα μεταδεδομένα",
  "Η Eurostat το γράφει ρητά στα μεταδεδομένα του εναρμονισμένου δείκτη: οι "
  "μέθοδοι και τα αποτελέσματα μπορεί να διαφέρουν από τους εθνικούς δείκτες.")
T("Δεν είναι υποσημείωση", "είναι το θέμα",
  "Αυτό δεν είναι υποσημείωση. Σημαίνει ότι όταν δύο άνθρωποι μαλώνουν για τον "
  "πληθωρισμό, μπορεί και οι δύο να κρατούν επίσημο χαρτί στο χέρι τους.")
T("Και κάτι πιο πρακτικό", "ένας μόνο σε αγγίζει",
  "Σημαίνει όμως και κάτι πιο πρακτικό. Μόνο ο ένας από τους δύο αγγίζει χαρτί "
  "που έχεις εσύ στο συρτάρι σου, και σε αυτόν θα μείνουμε πρώτα.")
T("Τι δεν θα ακούσεις", "κανένα ποσοστό",
  "Το βίντεο δεν θα σου πει κανένα ποσοστό πληθωρισμού, ούτε ένα. Θα σου πει "
  "ποιος δείκτης σε αφορά, πού ακριβώς τον διαβάζεις, και για ποιον μήνα.")

# -------------------------------------------------------------------- cap 2
B("Το χαρτί", "το μισθωτήριο",
  "Αν νοικιάζεις, ή νοικιάζεις σε άλλον, το χαρτί είναι το μισθωτήριο. Πολλά "
  "μισθωτήρια έχουν όρο αναπροσαρμογής που δένεται με δείκτη τιμών.",
  "person reading a contract on a table", 8960547,
  cap="Ποιος δείκτης μπαίνει στο μισθωτήριο")
T("Ποιος μπαίνει εκεί", "ο εθνικός",
  "Ο δείκτης που χρησιμοποιείται εκεί είναι ο εθνικός, της ΕΛΣΤΑΤ. Και η "
  "ΕΛΣΤΑΤ βγάζει κάθε μήνα, μαζί με τον δείκτη, ανακοίνωση αναπροσαρμογής "
  "μισθωμάτων.")
T("Είναι ελεγχόμενο", "στη σελίδα του δείκτη",
  "Αυτό είναι η απάντηση του βίντεο και είναι ελεγχόμενη. Η ανακοίνωση "
  "δημοσιεύεται στη σελίδα του Εθνικού Δείκτη Τιμών Καταναλωτή, κάθε μήνα.")
T("Πρώτο βήμα", "ο μήνας της επετείου",
  "Η πράξη έχει δύο βήματα και κανένα δεν ζητάει αριθμό από εμένα. Πρώτο βήμα: "
  "βρες στο μισθωτήριό σου τον μήνα της επετείου του.")
T("Δεύτερο βήμα", "η ανακοίνωση εκείνου του μήνα",
  "Δεύτερο βήμα: άνοιξε την ανακοίνωση αναπροσαρμογής μισθωμάτων της ΕΛΣΤΑΤ "
  "που αντιστοιχεί σε αυτόν τον μήνα, και διάβασε το ποσοστό εκεί μέσα.")
T("Τελείωσε", "το λέει ο φορέας",
  "Τελείωσε. Το ποσοστό δεν το λέω εγώ, δεν το λέει το συμβόλαιο και δεν το "
  "λέει ο άλλος. Το λέει ο φορέας που βγάζει τον δείκτη, για τον μήνα σου.")
T("Η ημερομηνία", "ζυγίζει πιο πολύ",
  "Γι' αυτό η ημερομηνία μετράει περισσότερο από το ποσοστό. Ο ίδιος όρος, με "
  "άλλον μήνα επετείου, δίνει άλλον αριθμό στο ίδιο ακριβώς ακίνητο.")
T("Και ο άλλος", "δεν μπαίνει εδώ",
  "Και γι' αυτό ο εναρμονισμένος δείκτης, όσο κι αν τον ακούς στις ειδήσεις, "
  "δεν είναι αυτός που μπαίνει σε αυτή τη γραμμή του μισθωτηρίου.")

# ======================== ΜΕΤΑ ΤΗΝ ΑΠΑΝΤΗΣΗ =================================

# -------------------------------------------------------------------- cap 3
T("Τότε γιατί", "τον λένε στο δελτίο",
  "Τότε γιατί οι ειδήσεις λένε τον άλλον; Επειδή τον χρησιμοποιεί η Ευρωπαϊκή "
  "Κεντρική Τράπεζα, και οι αποφάσεις της αφορούν και την Ελλάδα.",
  cap="Γιατί οι ειδήσεις λένε τον άλλον")
T("Το γράφει η ΕΚΤ", "στη σελίδα της",
  "Η ΕΚΤ γράφει στη σελίδα της για τη σταθερότητα των τιμών ότι θεωρεί τον "
  "εναρμονισμένο δείκτη κατάλληλο μέτρο για τον στόχο της.")
T("Μεσοπρόθεσμα", "όχι σε έναν μήνα",
  "Ο στόχος της είναι διατυπωμένος μεσοπρόθεσμα, δηλαδή δεν κρίνεται σε έναν "
  "μήνα. Αυτό από μόνο του εξηγεί γιατί ένας μήνας δεν αλλάζει τίποτα.")
T("Για ποιον φτιάχτηκε", "όχι για το συρτάρι σου",
  "Άρα ο δείκτης που ακούς στο δελτίο δεν είναι φτιαγμένος για το συρτάρι σου. "
  "Είναι φτιαγμένος για να συγκρίνονται κράτη και για να παίρνονται αποφάσεις.")
T("Η νομική βάση", "Κανονισμός 2016/792",
  "Η νομική του βάση είναι ο Κανονισμός της Ευρωπαϊκής Ένωσης 2016 κάθετος "
  "792, του Ευρωπαϊκού Κοινοβουλίου και του Συμβουλίου, της ενδεκάτης Μαΐου.")
T("Τι αντικατέστησε", "έναν του 1995",
  "Αυτός ο κανονισμός αντικατέστησε παλαιότερο του 1995 και είναι η βάση για "
  "την εναρμονισμένη μεθοδολογία σε όλα ανεξαιρέτως τα κράτη μέλη.")
T("Κρατάς δύο πράγματα", "δύο χρήσεις",
  "Κρατάς λοιπόν δύο πράγματα. Ο εθνικός δείκτης έχει εθνική χρήση, στα δικά "
  "σου τα χαρτιά. Ο εναρμονισμένος έχει ευρωπαϊκή χρήση, στις αποφάσεις.")
T("Τρεις διαφορές", "και η τρίτη βαραίνει",
  "Από εδώ και κάτω το βίντεο δείχνει τρεις συγκεκριμένες διαφορές ανάμεσα "
  "στους δύο, και την τρίτη την παραδέχεται η ίδια η Κεντρική Τράπεζα.")

# -------------------------------------------------------------------- cap 4
T("Πρώτη διαφορά", "η βάση",
  "Η πρώτη διαφορά είναι η πιο αθόρυβη και η πιο εύκολη να σε μπερδέψει. Οι "
  "δύο δείκτες δεν μετρούν πάνω στην ίδια βάση.",
  cap="Δύο βάσεις: 2020 και 2025")
T("Ο εθνικός", "βάση 2020 ίσον εκατό",
  "Η ΕΛΣΤΑΤ δημοσιεύει τον εθνικό δείκτη με βάση το 2020 ίσον εκατό. Αυτό το "
  "γράφει μέσα στον τίτλο κάθε πίνακα που βγάζει για αυτόν τον δείκτη.")
T("Ο εναρμονισμένος", "βάση 2025 ίσον εκατό",
  "Η Eurostat δημοσιεύει τον εναρμονισμένο με βάση το 2025 ίσον εκατό, και το "
  "γράφει στη μονάδα μέτρησης, μέσα στα μεταδεδομένα του δείκτη.")
T("Τι σημαίνει βάση", "ποια χρονιά παίρνει το εκατό",
  "Βάση σημαίνει ποια χρονιά παίρνει την τιμή εκατό. Δεν αλλάζει τον "
  "πληθωρισμό, αλλάζει όμως κάθε απόλυτο νούμερο δείκτη που θα δεις γραμμένο.")
T("Το μπέρδεμα", "ίδιος μήνας, άλλο νούμερο",
  "Άρα δύο άρθρα μπορούν να γράψουν άλλο νούμερο δείκτη για την ίδια χώρα και "
  "τον ίδιο μήνα, χωρίς να διαφωνεί το ένα με το άλλο.")
T("Γιατί συμβαίνει", "άλλη βάση, άλλη κλίμακα",
  "Το ένα το μέτρησε πάνω στη μία βάση και το άλλο πάνω στην άλλη. Η διαφορά "
  "είναι η κλίμακα της μέτρησης, δεν είναι η τιμή των πραγμάτων.")
T("Τι δεν χαλάει", "η ετήσια μεταβολή",
  "Η σύγκριση που δεν χαλάει είναι η ετήσια μεταβολή, γιατί η βάση φεύγει στη "
  "διαίρεση. Η σύγκριση που χαλάει είναι δείκτης με δείκτη, επίπεδο με επίπεδο.")
T("Πρακτικός κανόνας", "μεταβολές, όχι επίπεδα",
  "Πρακτικός κανόνας: μην συγκρίνεις ποτέ δύο επίπεδα δείκτη από δύο "
  "διαφορετικές πηγές. Σύγκρινε μεταβολές, και πάντα μέσα στην ίδια σειρά.")
T("Αυτή ήταν η κλίμακα", "τώρα το περιεχόμενο",
  "Αυτή ήταν η διαφορά της κλίμακας, και είναι η πιο αθώα από τις τρεις. Η "
  "επόμενη είναι διαφορά περιεχομένου, και είναι σοβαρότερη.")

# -------------------------------------------------------------------- cap 5
B("Δεύτερη διαφορά", "ποιον μετρά",
  "Η δεύτερη διαφορά είναι ποιον μετρά ο δείκτης. Και η απάντηση για τον "
  "εναρμονισμένο είναι γραμμένη με τα ίδια τα λόγια της Eurostat.",
  "customer at a supermarket checkout counter", 5103988,
  cap="Μέσα μετριέται κάθε αγορά στο έδαφος")
T("Η πρώτη μισή φράση", "όλα τα προϊόντα",
  "Ο εναρμονισμένος δείκτης περιλαμβάνει όλα τα προϊόντα και τις υπηρεσίες που "
  "αγοράζονται με χρηματικές συναλλαγές από νοικοκυριά.")
T("Η δεύτερη μισή", "κάτοικα και μη κάτοικα",
  "Και η φράση που μετράει είναι η επόμενη: από νοικοκυριά, κάτοικα και μη "
  "κάτοικα, μέσα στο έδαφος της χώρας. Αυτό λέγεται εγχώρια έννοια.")
T("Μη κάτοικα", "άνθρωποι που δεν ζουν εδώ",
  "Μη κάτοικα νοικοκυριά σημαίνει ανθρώπους που δεν ζουν εδώ. Οι αγορές που "
  "κάνουν μέσα στη χώρα μετριούνται κανονικά μέσα στον δείκτη.")
T("Για την Ελλάδα", "δεν είναι λεπτομέρεια",
  "Για μια χώρα με τον τουρισμό της Ελλάδας αυτό δεν είναι λεπτομέρεια. "
  "Σημαίνει ότι στο καλάθι υπάρχουν τιμές που δεν τις πληρώνεις εσύ ποτέ.")
T("Δεν είναι λάθος", "είναι ορισμός",
  "Δεν σημαίνει ότι ο δείκτης είναι λάθος. Σημαίνει ότι μετρά τις τιμές σε ένα "
  "έδαφος, όχι τις τιμές που πληρώνει ένα συγκεκριμένο νοικοκυριό.")
T("Τι εξηγεί αυτό", "και οι δύο έχουν δίκιο",
  "Και εξηγεί κάτι που ακούγεται συνεχώς: ότι ο επίσημος αριθμός δεν μοιάζει "
  "με αυτό που νιώθει ο κόσμος. Και οι δύο πλευρές μπορεί να έχουν δίκιο.")
T("Η τρίτη", "αφορά τη στέγη",
  "Η τρίτη διαφορά είναι βαρύτερη από αυτή, γιατί αφορά το μεγαλύτερο έξοδο "
  "της ζωής σου, και αυτό είναι η στέγη.")

# -------------------------------------------------------------------- cap 6
T("Τι μένει έξω", "υπάρχει λίστα",
  "Ο εναρμονισμένος δείκτης δεν καλύπτει όλες τις κατηγορίες κατανάλωσης. Η "
  "Eurostat δημοσιεύει ονομαστικά τη λίστα με αυτές που μένουν έξω.",
  cap="Το ενοίκιο που δεν μετριέται")
T("Ο κωδικός", "μηδέν τέσσερα κόμμα δύο",
  "Μέσα σε αυτή τη λίστα υπάρχει η κατηγορία με κωδικό μηδέν τέσσερα, κόμμα, "
  "δύο: τα τεκμαρτά ενοίκια κατοικίας. Δεν καλύπτονται από τον δείκτη.")
T("Τι είναι τεκμαρτό", "λογιστικό, όχι πληρωμή",
  "Τεκμαρτό ενοίκιο είναι το ενοίκιο που θα πλήρωνε κάποιος που μένει σε σπίτι "
  "δικό του, αν το νοίκιαζε. Είναι λογιστικό μέγεθος, δεν είναι πληρωμή.")
T("Τι σημαίνει πρακτικά", "για τον ιδιοκάτοικο",
  "Για τον ιδιοκτήτη που μένει μέσα στο σπίτι του, το κόστος της στέγης δεν "
  "περνάει από τον εναρμονισμένο δείκτη με αυτόν τον τρόπο.")
T("Στην Ελλάδα", "όχι μικρή μειονότητα",
  "Στην Ελλάδα, όπου η ιδιοκατοίκηση είναι πολύ διαδεδομένη, αυτό το κενό δεν "
  "αφορά μια μικρή μειονότητα νοικοκυριών. Αφορά πάρα πολλά νοικοκυριά.")
T("Δεν είναι αμέλεια", "το γράφει η Eurostat",
  "Και δεν είναι παράλειψη από αμέλεια. Η Eurostat γράφει ότι κάποιες "
  "κατηγορίες μένουν έξω επειδή δεν υπάρχει ακόμη εναρμονισμένη μέθοδος.")
T("Αναγνωρισμένο", "στα δικά της μεταδεδομένα",
  "Δηλαδή το πρόβλημα είναι αναγνωρισμένο και καταγεγραμμένο από τον ίδιο τον "
  "φορέα που φτιάχνει τον δείκτη, μέσα στα δικά του τα μεταδεδομένα.")
T("Και κάποιος ακόμη", "που δεν τον περιμένεις",
  "Και στο επόμενο κεφάλαιο το ίδιο πράγμα το λέει και κάποιος ακόμη, που δεν "
  "τον περιμένεις καθόλου να το λέει.")

# -------------------------------------------------------------------- cap 7
T("Η ΕΚΤ", "δύο πράγματα στη σειρά",
  "Η Ευρωπαϊκή Κεντρική Τράπεζα, στη σελίδα της για τη σταθερότητα των τιμών, "
  "γράφει δύο πράγματα το ένα μετά το άλλο.",
  cap="Το παραδέχεται η ίδια η ΕΚΤ")
T("Πρώτο", "κατάλληλο μέτρο",
  "Πρώτο: θεωρεί τον εναρμονισμένο δείκτη το κατάλληλο μέτρο για να κρίνει αν "
  "επιτυγχάνεται ο στόχος της για τη σταθερότητα των τιμών.")
T("Δεύτερο", "και εδώ είναι το βάρος",
  "Δεύτερο, και αυτό είναι το σημαντικό: αναγνωρίζει ότι η συμπερίληψη του "
  "κόστους της ιδιοκατοίκησης θα αντιπροσώπευε καλύτερα τον πληθωρισμό των "
  "νοικοκυριών.")
T("Με απλά λόγια", "το λέει μόνη της",
  "Με απλά λόγια, ο φορέας που παίρνει τις αποφάσεις λέει μόνος του ότι ο "
  "δείκτης που χρησιμοποιεί δεν είναι ο πληθωρισμός του νοικοκυριού. Δεν το "
  "λέει κάποιος επικριτής· το λέει η ίδια, στη δική της τη σελίδα.")
T("Και προσθέτει", "το εξετάζουν",
  "Και προσθέτει ότι το Ευρωπαϊκό Στατιστικό Σύστημα εξετάζει με ποιον τρόπο "
  "θα μπορούσαν να μπουν αυτά τα κόστη μέσα στη μέτρηση του πληθωρισμού.")
T("Η σταύρωση", "κατηγορία και επιφύλαξη",
  "Αυτή είναι η πιο καθαρή σταύρωση που μπορεί να έχει αυτό το βίντεο. Το κενό "
  "το γράφει η Eurostat ως κατηγορία, και η ΕΚΤ ως επιφύλαξη δική της.")
T("Δύο θεσμοί", "η ίδια παραδοχή",
  "Δύο ανεξάρτητοι θεσμοί, η ίδια παραδοχή, σε δύο δικές τους σελίδες. Αυτό "
  "δεν είναι άποψη δική μου και δεν χρειάζεται καθόλου να με πιστέψεις.")
T("Μένει ένα", "άλλαξε πρόσφατα",
  "Μένει ένα τελευταίο πράγμα που άλλαξε πρόσφατα, και χαλάει συγκρίσεις που "
  "φαίνονται εντελώς αθώες όταν τις κάνεις.")

# -------------------------------------------------------------------- cap 8
T("Η ταξινόμηση", "με το ακρωνύμιο ECOICOP",
  "Ο εναρμονισμένος δείκτης κατατάσσει τα προϊόντα με μια ευρωπαϊκή "
  "ταξινόμηση ατομικής κατανάλωσης κατά σκοπό, με το ακρωνύμιο ECOICOP.",
  cap="Από τον Ιανουάριο του 2026 άλλαξε")
T("Άλλαξε", "κανονισμός του 2024",
  "Αυτή η ταξινόμηση άλλαξε. Με βάση ευρωπαϊκό κανονισμό του 2024, "
  "εφαρμόζεται αναθεωρημένη έκδοση, η δεύτερη, σε όλη τη σειρά των στοιχείων.")
T("Πότε ξεκινά", "στοιχεία Ιανουαρίου 2026",
  "Η Eurostat γράφει ότι η εφαρμογή ξεκινά με τη δημοσίευση των στοιχείων του "
  "Ιανουαρίου του 2026. Δηλαδή είναι αλλαγή της φετινής χρονιάς, όχι παλιά.")
T("Δεκατρείς", "αντί για δώδεκα",
  "Οι βασικές κατηγορίες προϊόντων είναι τώρα δεκατρείς, ενώ στην προηγούμενη "
  "έκδοση ήταν δώδεκα. Αλλάζει η αρίθμηση, όχι μόνο τα ονόματα.")
T("Το ενοίκιο", "κρατάει τον κωδικό του",
  "Γι' αυτό και οι κωδικοί που ακούς αλλάζουν θέση. Τα τεκμαρτά ενοίκια "
  "κρατούν τον κωδικό μηδέν τέσσερα, κόμμα, δύο, και μένουν και πάλι έξω.")
T("Άλλα μετακινούνται", "υπάρχει αντιστοίχιση",
  "Αλλά άλλα μετακινούνται. Η Eurostat δημοσιεύει πίνακα αντιστοίχισης "
  "ανάμεσα στις δύο εκδόσεις της ταξινόμησης, στον διακομιστή ταξινομήσεων.")
T("Το συμπέρασμα", "έλεγξε πρώτα",
  "Το πρακτικό συμπέρασμα είναι ένα. Αν συγκρίνεις υποκατηγορία με "
  "υποκατηγορία ανάμεσα σε παλιά και νέα δημοσίευση, έλεγξε πρώτα την "
  "αντιστοίχιση.")
T("Και τώρα", "το μόνο σίγουρο καλάθι",
  "Και τώρα το μόνο καλάθι που είναι σίγουρα δικό σου, και δεν το ορίζει "
  "κανένας κανονισμός και κανένας φορέας.")

# ------------------------------------------------------------------- cap 9
T("Τι άλλο λείπει", "η λίστα συνεχίζεται",
  "Τα τεκμαρτά ενοίκια δεν είναι το μόνο που μένει έξω. Η λίστα της Eurostat "
  "έχει και άλλες κατηγορίες, και μία από αυτές άλλαξε στρατόπεδο φέτος.",
  cap="Τι άλλο μένει έξω, και τι μπήκε φέτος")
T("Μένουν έξω", "και παραμένουν έξω",
  "Εκτός κάλυψης μένουν τα ναρκωτικά και η εκπόρνευση. Μένουν έξω και στην "
  "παλιά και στη νέα έκδοση της ταξινόμησης, με αλλαγμένο μόνο τον κωδικό.")
T("Οι ασφάλειες", "ζωής και υγείας",
  "Εκτός μένουν επίσης η ασφάλιση ζωής και η δημόσια ασφάλιση που συνδέεται "
  "με την υγεία, καθώς και κατηγορία χρηματοοικονομικών υπηρεσιών.")
T("Αυτό μπέρδεψε κόσμο", "ασφάλιστρα και δείκτης",
  "Αυτό εξηγεί κάτι που ξενίζει: μπορεί τα ασφάλιστρα ζωής να ανέβουν αισθητά "
  "και ο εναρμονισμένος δείκτης να μην το δείξει με αυτόν τον τρόπο.")
T("Και η αλλαγή", "τα τυχερά παιχνίδια",
  "Και εδώ είναι η αλλαγή της χρονιάς. Τα τυχερά παιχνίδια ήταν εκτός κάλυψης "
  "μέχρι το 2025. Από το 2026 η Eurostat τα σημειώνει ως συμπεριλαμβανόμενα.")
T("Τι σημαίνει", "νέο είδος στο καλάθι",
  "Σημαίνει ότι ένα είδος δαπάνης που δεν μετριόταν, τώρα μετριέται. Το "
  "καλάθι δεν είναι σταθερό αντικείμενο· είναι απόφαση που αναθεωρείται.")
T("Γιατί το λέω", "για τις συγκρίσεις",
  "Το λέω για έναν πρακτικό λόγο. Όταν συγκρίνεις σειρές που περνούν πάνω από "
  "αυτή την αλλαγή, δεν συγκρίνεις πάντα το ίδιο ακριβώς περιεχόμενο.")
T("Και όλα αυτά", "είναι δημοσιευμένα",
  "Και τίποτα από αυτά δεν είναι κρυφό. Είναι γραμμένα, κατηγορία προς "
  "κατηγορία, μέσα στα δημόσια μεταδεδομένα του δείκτη.")
# -------------------------------------------------------------------- cap 10
B("Κανένας δεν είναι εσύ", "είναι μέσοι όροι",
  "Κανένας από τους δύο επίσημους δείκτες δεν είναι το καλάθι σου, και δεν "
  "προσπαθεί να είναι. Είναι σταθμισμένοι μέσοι όροι για ένα σύνολο.",
  "woman writing receipts into a planner", 5981290,
  cap="Το δικό σου καλάθι, από τις αποδείξεις σου")
T("Από πού βγαίνει", "από τις αποδείξεις",
  "Το δικό σου καλάθι βγαίνει από τις δικές σου τις αποδείξεις, και η πράξη "
  "είναι αρκετά απλή ώστε να γίνει μέσα σε ένα απόγευμα.")
T("Τρεις στοίβες", "όχι δώδεκα",
  "Κράτα τις αποδείξεις ενός μήνα και χώρισέ τις σε τρεις στοίβες: στέγη και "
  "λογαριασμοί, τρόφιμα, όλα τα άλλα. Τρεις στοίβες, όχι δώδεκα κατηγορίες.")
T("Ο ίδιος μήνας", "της προηγούμενης χρονιάς",
  "Κάνε το ίδιο με τον ίδιο μήνα της προηγούμενης χρονιάς, αν έχεις χαρτιά. Αν "
  "δεν έχεις, κράτα τον φετινό μήνα και περίμενε δώδεκα μήνες.")
T("Η πράξη", "μεταβολή επί βάρος",
  "Η αλλαγή σε κάθε στοίβα, πολλαπλασιασμένη με το πόσο ζυγίζει η στοίβα στο "
  "σύνολό σου, είναι ο δικός σου πληθωρισμός. Κανενός άλλου ανθρώπου.")
T("Θα διαφέρει", "και δεν λέει ψέματα κανείς",
  "Θα βγει διαφορετικός από τους δύο επίσημους, και αυτό δεν σημαίνει ότι "
  "κάποιος λέει ψέματα. Σημαίνει ότι μετράτε δύο διαφορετικά καλάθια.")
T("Η μόνη στιγμή", "με νομικό βάρος",
  "Και η μόνη στιγμή που ο επίσημος δείκτης μπαίνει στη ζωή σου με νομικό "
  "βάρος είναι η γραμμή αναπροσαρμογής του μισθωτηρίου, με τον μήνα της "
  "επετείου.")
C("Στα σχόλια", "μόνο τον μήνα",
  "Γράψε στα σχόλια μόνο τον μήνα της επετείου του μισθωτηρίου σου. Όχι το "
  "ποσό, όχι τη διεύθυνση. Θέλω να δω πόσο σκορπισμένοι είστε μέσα στο έτος.")

# ================================== SHORT ====================================

SHORT = [
    {"layout": "titulo", "kicker": "Δύο αριθμοί", "sub": "τον ίδιο μήνα",
     "nar": "Για τον πληθωρισμό στην Ελλάδα υπάρχουν δύο επίσημοι αριθμοί τον "
            "ίδιο μήνα. Δεν είναι λάθος κανένας από τους δύο.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Ο εθνικός", "sub": "στο μισθωτήριό σου",
     "nar": "Ο ένας είναι ο εθνικός δείκτης της ΕΛΣΤΑΤ. Αυτός μπαίνει στη "
            "γραμμή αναπροσαρμογής του μισθωτηρίου σου.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Ο εναρμονισμένος", "sub": "τον λέει η ΕΚΤ",
     "nar": "Ο άλλος είναι ο εναρμονισμένος, που χρησιμοποιεί η ΕΚΤ. Αυτός δεν "
            "καλύπτει τα τεκμαρτά ενοίκια κατοικίας.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Και το παραδέχεται", "sub": "η ίδια η ΕΚΤ",
     "nar": "Και το παραδέχεται η ίδια: γράφει ότι η ιδιοκατοίκηση θα "
            "αντιπροσώπευε καλύτερα τον πληθωρισμό των νοικοκυριών.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Ποιος σε αγγίζει", "sub": "και πού",
     "nar": "Ποιος από τους δύο αγγίζει το χαρτί σου, και πού τον διαβάζεις "
            "για τον δικό σου μήνα, είναι στο βίντεο.",
     "sem_cap": True},
]

THUMB = {"l1": "Δύο δείκτες", "l2": "ποιος σε αφορά"}

COPY = """# Δύο επίσημοι δείκτες τιμών για την Ελλάδα, και ποιος από τους δύο αγγίζει το χαρτί σου

## TITULO
Πληθωρισμός: Δύο Επίσημοι Δείκτες για τον Ίδιο Μήνα — και Μόνο ο Ένας Μπαίνει στο Μισθωτήριό σου

## TITULO SHORT
Δύο επίσημοι δείκτες: ποιος σε αφορά;

## DESCRICAO
Για τον πληθωρισμό στην Ελλάδα δεν υπάρχει ένας επίσημος αριθμός. Υπάρχουν δύο, για τον ίδιο μήνα, και κανένας από τους δύο δεν είναι λάθος: ο Εθνικός Δείκτης Τιμών Καταναλωτή που βγάζει η ΕΛΣΤΑΤ, και ο Εναρμονισμένος Δείκτης που ορίζει ευρωπαϊκός κανονισμός. Μετρούν διαφορετικά πράγματα και έχουν διαφορετική χρήση.

Το βίντεο δεν λέει κανένα ποσοστό πληθωρισμού, ούτε ένα. Λέει ποιος δείκτης αγγίζει χαρτί που έχεις εσύ στο συρτάρι — και η απάντηση είναι ο εθνικός, μέσα από την ανακοίνωση αναπροσαρμογής μισθωμάτων που η ΕΛΣΤΑΤ δημοσιεύει κάθε μήνα μαζί με τον δείκτη. Η πράξη έχει δύο βήματα: βρες στο μισθωτήριό σου τον μήνα της επετείου του, και άνοιξε την ανακοίνωση εκείνου του μήνα. Το ποσοστό δεν το λέω εγώ.

Μετά την απάντηση, τρεις διαφορές ανάμεσα στους δύο δείκτες, η κάθε μία με την πηγή της, και στο τέλος τι άλλο μένει έξω από το καλάθι — με ένα είδος δαπάνης που ήταν εκτός κάλυψης μέχρι το 2025 και από το 2026 σημειώνεται ως συμπεριλαμβανόμενο. Η βάση: 2020 ίσον εκατό για τον εθνικό, 2025 ίσον εκατό για τον εναρμονισμένο — γι' αυτό δύο άρθρα μπορούν να γράψουν άλλο νούμερο για τον ίδιο μήνα. Η εγχώρια έννοια: ο εναρμονισμένος μετρά αγορές νοικοκυριών, κάτοικων και μη κάτοικων, μέσα στο έδαφος της χώρας. Και το κενό της στέγης: η κατηγορία 04.2, τα τεκμαρτά ενοίκια κατοικίας, δεν καλύπτεται — κάτι που η Eurostat γράφει ως εξαιρούμενη κατηγορία και η ΕΚΤ γράφει ως δική της επιφύλαξη, στις δύο σελίδες τους.

Μία επιφύλαξη που μετράει: αυτό δεν είναι νομική ούτε φορολογική συμβουλή, δεν ερμηνεύει τον όρο αναπροσαρμογής του δικού σου συμβολαίου και δεν υπολογίζει πόσο θα ανέβει το ενοίκιό σου. Αν ο όρος του συμβολαίου σου είναι διατυπωμένος αλλιώς, ή αν υπάρχει διαφωνία, αυτό θέλει δικηγόρο και όχι βίντεο. Και δεν αφορά όποιον δεν έχει μισθωτήριο: χωρίς συμβόλαιο δεν υπάρχει μήνας επετείου.

CAPITULOS
{CAPITULOS}

Στα σχόλια γράψε μόνο τον μήνα της επετείου του μισθωτηρίου σου. Όχι το ποσό, όχι τη διεύθυνση, όχι την πόλη. Θέλω να δω πόσο σκορπισμένοι είστε μέσα στο έτος.

## DISCLOSURE
Η αφήγηση και τα γραφικά αυτού του βίντεο είναι δημιουργημένα από υπολογιστή. Το κείμενο είναι πρωτότυπο και το περιεχόμενο είναι πληροφοριακό, δεν αποτελεί νομική, φορολογική ή επενδυτική συμβουλή.

## HASHTAGS
#πληθωρισμος #ενοικιο #ΕΛΣΤΑΤ

## TAGS
πληθωρισμος, δεικτης τιμων καταναλωτη, εθνικος δεικτης, εναρμονισμενος δεικτης, ΕΛΣΤΑΤ, Eurostat, αναπροσαρμογη μισθωματων, ενοικιο αναπροσαρμογη, μισθωτηριο, τεκμαρτα ενοικια, ιδιοκατοικηση, ΕΚΤ στοχος, βαση 2020 ισον εκατο, ECOICOP, προσωπικος πληθωρισμος

## COMENTARIO FIXADO
Όλη η απάντηση σε δύο γραμμές: ο δείκτης που μπαίνει στη γραμμή αναπροσαρμογής του μισθωτηρίου είναι ο ΕΘΝΙΚΟΣ Δείκτης Τιμών Καταναλωτή της ΕΛΣΤΑΤ, όχι ο εναρμονισμένος που ακούς στο δελτίο. Βρες στο συμβόλαιό σου τον μήνα της επετείου του και άνοιξε την ανακοίνωση αναπροσαρμογής μισθωμάτων της ΕΛΣΤΑΤ για εκείνον τον μήνα. Το ποσοστό το λέει ο φορέας που βγάζει τον δείκτη, για τον μήνα σου — όχι εγώ και όχι ο άλλος.

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhuma taxa de inflacao, de nenhum mes e de nenhum indice. Os numeros que ele cita sao de QUATRO tipos, e cada um esta no lugar onde a propria instituicao o escreve: (1) as BASES dos dois indices — 2020=100 para o indice nacional, no titulo dos quadros da ELSTAT, e 2025=100 para o harmonizado, na unidade de medida dos metadados da Eurostat; (2) o CODIGO da categoria excluida, 04.2, alugueis imputados de habitacao, na lista de categorias nao cobertas publicada pela Eurostat; (3) a BASE LEGAL, Regulamento (UE) 2016/792 do Parlamento Europeu e do Conselho, de 11 de maio de 2016, que substituiu um de 1995, conforme o item de mandato institucional dos mesmos metadados; (4) a CONTAGEM de divisoes da classificacao, treze na versao 2 contra doze na anterior, aplicada a partir da publicacao dos dados de janeiro de 2026 por regulamento europeu de 2024, tambem nos metadados da Eurostat; (5) os ANOS da mudanca de cobertura dos jogos de azar — fora da cobertura ate 2025, assinalados como incluidos a partir de 2026 — lidos na mesma tabela de categorias nao cobertas, que a Eurostat publica em duas colunas, "ate 2025" e "a partir de 2026". Base, codigo de categoria, numero de regulamento e contagem de divisoes nao sao medicoes: sao identificadores, e a fonte autoritativa de cada um e a instituicao que publica aquele indice. Os 118 e 102 do capitulo 4 sao EXPLICITAMENTE um exemplo aritmetico de como duas bases dao numeros diferentes, nao leituras de nenhum mes — e a narracao diz "αν διαβάσεις", se leres.

A SUSTENTACAO CRUZADA, que e o motivo deste eixo existir: o furo da habitacao propria aparece em DUAS instituicoes independentes, cada uma na sua pagina. A Eurostat registra 04.2 como categoria NAO COBERTA pelo harmonizado e escreve que algumas categorias ficam de fora por ainda nao existir metodo harmonizado. O Banco Central Europeu, na pagina de estabilidade de precos, escreve que considera o harmonizado a medida apropriada do seu objetivo E reconhece que a inclusao dos custos ligados a habitacao propria representaria melhor a inflacao relevante para as familias. Compilador e utilizador do indice, a mesma admissao.

O QUE FOI DESCARTADO, e por que, porque isto custou a rodada passada: (1) QUALQUER taxa de inflacao grega, porque uma taxa precisa bater em duas fontes oficiais e as duas fontes que eu leio publicam indices com DEFINICOES diferentes — bater nao e esperado, e citar uma delas sozinha seria citar numero de fonte unica; (2) a afirmacao de que a ELSTAT publica tambem o harmonizado: a pagina DKT88 respondeu 200 mas voltou com a descricao VAZIA, so navegacao, entao eu nao tenho isso medido e nao entra; (3) o valor numerico do objetivo da ECB, porque so a ECB o define e nao existe segunda fonte independente para ele — o video diz que ela tem um objetivo formulado a medio prazo, sem numero; (4) tudo que viria de orgao grego que a sandbox nao le: `aade.gr` da 403, `efka.gov.gr` e `et.gr` sao aplicacoes JavaScript, e nesta rodada eu medi mais quatro e todos reprovaram — `bankofgreece.gr` 403, `ypergasias.gov.gr` e `minfin.gr` devolvem 202 de pagina de desafio, `dypa.gov.gr` e `hdigf.gr` dao timeout. O par que sustenta este video e `statistics.gr` mais `ec.europa.eu` mais `ecb.europa.eu`, os tres medidos servindo texto legivel nesta rodada.

## FONTES
ΕΛΣΤΑΤ — Δείκτης Τιμών Καταναλωτή (ΔΤΚ), Εθνικός Δείκτης, βάση 2020=100,0, και η Ανακοίνωση Αναπροσαρμογής Μισθωμάτων που δημοσιεύεται μαζί του: statistics.gr
Eurostat — Harmonised index of consumer prices (HICP), reference metadata (ESMS), μονάδα μέτρησης 2025=100, εγχώρια έννοια, κατηγορίες εκτός κάλυψης, Κανονισμός (ΕΕ) 2016/792, ECOICOP έκδοση 2: ec.europa.eu/eurostat
Ευρωπαϊκή Κεντρική Τράπεζα — Price stability, μεσοπρόθεσμος στόχος, ο ΕνΔΤΚ ως κατάλληλο μέτρο και η επιφύλαξη για την ιδιοκατοίκηση: ecb.europa.eu
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/epomeno-epipedo-015.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-015",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#12263A", "c1": "#2A9D8F", "c2": "#E8A33D",
               "bg": "#F5F2EC"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": _copy_existente(),
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada, duracao_estimada_short, duracao_cena
    grava(SPEC, "fabrica/specs/epomeno-epipedo-015.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
    t, ult = 0.0, None
    for c in CENAS:
        if c.get("cap"):
            if ult:
                print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s")
            ult = (c["cap"], t)
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
    if ult:
        print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s")
    RESIDUO = 0.999   # el-GR-NestorasNeural, -0,1% no ensaio.py, n=519
    t = 0.0
    for i, c in enumerate(CENAS):
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
        if "διάβασε το ποσοστό εκεί μέσα" in (c.get("nar") or ""):
            print(f"  a resposta fecha em {t:.1f}s cru -> "
                  f"{t * RESIDUO:.1f}s corrigido (cena {i})")
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: "
                  f"{c['broll_q']}")
