"""epomeno-epipedo-017 — duas tirmas na mesma oferta decidem se as parcelas eram sem juro.

ALAVANCA ATACADA: A (conversao short -> inscrito), pela FORMA — e a forma vem
do que ESTE canal mediu, lido AO VIVO em 07/10 05:10 pelo `videos.list`
(part=statistics,status) nos 33 ids, nao pelo `metricas`.

    pacote  assunto                              short  longo  travessia
    008     ENFIA: o desconto de 20% que 1 em 14 pega   540    431     80%
    010     Tekmiria: o Estado SUPOE a sua renda        311    186     60%
    007     Sintaxi: por que 300.000 pegam tudo         593    352     59%
    009     Anos ficticios: voce compra 7, o outro...   427    133     31%
    013     Quanto custa de verdade o seu quilometro    154     46     30%
    011     IVA: quanto voce paga em cada recibo        541     70     13%
    006     Inflacao 3,4% e carne 14,3%                 191     20     10%
    005     Juros 2026: 0,03% no deposito                385     36      9%
    003     Salario minimo: Grecia ou Holanda          1407    117      8%
    002     A Grecia e no1 em casas proprias           1614    110      7%
    004     Conta de luz                                301     18      6%

O QUE DEU CERTO, e e o padrao mais forte de qualquer canal da frota: os QUATRO
melhores longos (431, 352, 186, 133) sao todos "EXISTE UMA REGRA QUE SEPARA
quem recebe de quem nao". O que nao deu: os dois shorts GIGANTES (1.614 e
1.407) deram as duas PIORES travessias, 7% e 8%.

O QUE VOU MUDAR, e aqui esta a dificuldade real desta rodada: o aprendizado 611
diz que esse eixo de REGRA nao tem fonte grega — oito hosts fiscais testados
dao 403, JavaScript ou timeout. Entao a regra deste pacote NAO e uma norma: e a
comparacao entre DUAS TIRMAS que estao impressas na propria oferta do
espectador. A promessa fica com a forma que mede melhor e o numero que decide
continua sendo dele.

O QUE EU TENTEI PRIMEIRO E DESCARTEI, e vai escrito porque foi trabalho feito:
o Eurostat ABRE (aprendizado 614) e o dataset `ilc_lvho07a` entregou, com
`updated` de 17/09/2026, numeros fortes para 2025 — a parcela de domicilios que
o indicador oficial conta como sobrecarregados pelo custo de habitacao e 26,4%
na Grecia contra 7,7% na UE, e partido pelo lado da linha de pobreza da 82,6%
contra 12,7%. Era pauta pronta e com a forma certa. CAIU porque o indicador se
define por um LIMIAR (custo de habitacao acima de uma fracao da renda) e esse
limiar eu NAO consegui na fonte: baixei o proprio arquivo de metadados SDMX do
Eurostat (`metadata/ilc_sieusilc.sdmx.zip`, HTTP 200, 2,25 MB) e a definicao nao
esta nele. Sem o limiar o espectador nao se coloca de um lado nem do outro, e o
limiar de memoria nao entra. Fica anotado para quando a fonte do limiar abrir.

PESQUISA DE TENDENCIA (obrigatoria). YouTube
`chart=mostPopular&regionCode=GR&videoCategoryId=26`, quinze itens, status 200 e
`error` ausente. **A 26 e PROXY e eu digo isso:** a categoria real de todos os
canais da frota e a 27 (Education), que nao tem chart em regiao nenhuma
(aprendizado 610).
O feed grego estava com fofoca de celebridade, culinaria, DIY de carro e um
clipe politico. Zero financas.
GRAFEI A FORMA, DESCARTEI O ASSUNTO: "Πως να μαγειρέψεις το συκώτι αν μισείς
την μυρωδιά του" — COMO FAZER X SE A OBJECAO OBVIA SE APLICA A VOCE. Virou o
gancho: como saber se as parcelas eram sem juro MESMO QUE a loja tenha dito que
eram. Nao grafei fofoca, culinaria nem carro.

EIXO, e por que ele e novo. Os quinze pacotes falam de casa propria, salario
minimo, conta de luz, juros de deposito, inflacao, aposentadoria, ENFIA, anos
ficticios, tekmiria, IVA, cor do tarifario, custo por quilometro, hora extra,
dois indices de inflacao e limiar de pobreza. NENHUM trata de CREDITO AO
CONSUMO. E o 016, publicado ha tres horas, e "mesma renda, duas casas" — este
NAO repete esse enquadramento: lá o que variava era a composicao do domicilio,
aqui o que varia e a forma de pagamento do MESMO objeto.

IDENTIDADE — OUTRA CORRECAO MINHA, a segunda em duas rodadas. A faixa do canal
em TRES pacotes (013, 014, 015) e `ink #12263A / c1 #2A9D8F / c2 #E8A33D /
bg #F5F2EC`, e o 012 difere so no c1. O epomeno-epipedo-016, que eu escrevi
esta noite, saiu com `#1C2B36 / #1F6FB2 / #C8622A / #F6F2E9` — paleta que
nenhum outro pacote do canal usa. E o kolejny-poziom-017, tambem meu, fez o
MESMO no canal polones. Dois canais, duas noites, o mesmo desvio: nao e
acidente, e um habito meu de redesenhar a paleta ao escrever a spec. Volto a
faixa nos dois. Trilha `Inspired`, unanime nos cinco. Aprendizado 617.

VEREDITO DO CANAL: `liberado` (v_maquina_licoes, treze shorts e catorze longos
medidos, mediana de views/dia do longo 1,54 contra 7,86 do short). `liberado` =
12 a 15 min, e a rotina manda dimensionar para o PISO da faixa: 720 s.

PISO DE CARACTERES, calculado ANTES da primeira cena (aprendizado 616, e foi
escrito por causa do pacote de ontem que precisou de tres reconstrucoes):
`ensaio.piso_de_caracteres('el-GR-NestorasNeural', n_cenas=81)` diz que o custo
fixo de 81 cenas de duas frases e 230 s, e que cada narracao precisa de pelo
menos 127 caracteres para o total fechar os 720 s. Escrevi para ~128.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO AFIRMACAO SOBRE O MUNDO. Nao ha fonte a citar porque nao ha afirmacao a
# sustentar: o video nao diz o que as lojas gregas fazem, nao diz o que a
# maioria escolhe, nao cita taxa, nao cita indice e nao cita norma.
#
# O QUE O VIDEO AFIRMA E ARITMETICA:
#   * o total do parcelamento e numero de parcelas vezes o valor da parcela;
#   * o custo da facilidade e esse total, MAIS as despesas que estiverem
#     escritas no papel do espectador, MENOS o preco a vista do mesmo papel;
#   * se der zero, era sem juro de verdade;
#   * o percentual e essa diferenca dividida pelo preco a vista.
#
# AS ENTRADAS SAO TODAS DO ESPECTADOR, e sao quatro, todas da MESMA folha:
# preco a vista, numero de parcelas, valor da parcela e a linha de despesas, se
# existir. Nenhum numero meu entra no resultado.
#
# O EXEMPLO DO CAPITULO CINCO E HIPOTETICO E O VIDEO DIZ ISSO NA CENA QUE O
# ABRE: seiscentos euros a vista, doze parcelas de cinquenta e cinco, vinte
# euros de despesa. Nao e preco de produto nenhum e nao foi medido em lugar
# nenhum — e numero redondo para a conta ficar visivel.
#
# O QUE FOI DESCARTADO, e o descarte vai escrito:
#   (1) o que os comercios gregos cobram ou oferecem — sem fonte, sem citacao;
#   (2) o que a maioria das pessoas escolhe;
#   (3) o custo efetivo de cartao de credito e de parcelamento bancario, que
#       depende de contrato e de regulamento e que eu nao fecho em duas fontes;
#   (4) a pauta do Eurostat sobre sobrecarga de custo de habitacao, que estava
#       pronta e caiu por falta do LIMIAR na fonte (ver o docstring).
#
# E O QUE A CONTA NAO DECIDE esta no capitulo oito inteiro: parcelar nao e
# errado. Dinheiro hoje vale mais que dinheiro em doze meses, e quem parcela
# para nao ficar sem reserva esta comprando algo real. A conta diz QUANTO custa
# essa escolha, nao se ela e certa.
#
# =============================================================================
"""

CENAS = []


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


# Links gravados pela busca via `pg_net`, onde a chave do Pexels mora. NENHUM
# repete pacote anterior deste canal: os quinze ja usados (5103988, 5827788,
# 5981290, 6305034, 6963972, 7263305, 7490517, 7947401, 8440643, 8478746,
# 8478753, 8661806, 8731555, 8960547, 19228172) foram lidos das specs 014, 015 e
# 016 antes da escolha, nao so do ultimo pacote.
#
# TODOS COM CATORZE SEGUNDOS OU MAIS: a cena fica em ~8,7 s e o preparo pede
# ~11,7 s. No labtreinamento-011 de hoje um clipe de nove segundos saiu
# "cortado invalido" e a cena caiu no fallback de lower-third sobre preto.
BROLL = {
    6114652: ("https://videos.pexels.com/video-files/6114652/6114652-hd_1366_720_25fps.mp4",
              "cottonbro studio",
              "https://www.pexels.com/video/black-friday-sale-advertisement-and-tags-6114652/"),
    6117602: ("https://videos.pexels.com/video-files/6117602/6117602-hd_1366_720_25fps.mp4",
              "cottonbro studio",
              "https://www.pexels.com/video/salesman-filling-the-receipt-6117602/"),
    5836824: ("https://videos.pexels.com/video-files/5836824/5836824-hd_1280_720_30fps.mp4",
              "Gustavo Fring",
              "https://www.pexels.com/video/person-holding-a-tag-5836824/"),
    5644247: ("https://videos.pexels.com/video-files/5644247/5644247-hd_1366_720_25fps.mp4",
              "kaboompics.com",
              "https://www.pexels.com/video/a-red-card-for-price-discount-5644247/"),
    5889461: ("https://videos.pexels.com/video-files/5889461/5889461-hd_1280_720_25fps.mp4",
              "Max Fischer",
              "https://www.pexels.com/video/a-printed-sale-tag-5889461/"),
    3970164: ("https://videos.pexels.com/video-files/3970164/3970164-hd_1280_720_30fps.mp4",
              "Gustavo Fring",
              "https://www.pexels.com/video/a-cashier-using-cash-register-monitor-for-payment-transaction-3970164/"),
    4121754: ("https://videos.pexels.com/video-files/4121754/4121754-hd_1280_720_50fps.mp4",
              "Jack Sparrow",
              "https://www.pexels.com/video/couple-paying-at-the-counter-in-the-grocery-4121754/"),
    35042443: ("https://videos.pexels.com/video-files/35042443/14844586_1280_720_30fps.mp4",
               "Michael Takahashi",
               "https://www.pexels.com/video/busy-retail-checkout-during-super-friday-event-35042443/"),
    7457422: ("https://videos.pexels.com/video-files/7457422/7457422-hd_1280_720_30fps.mp4",
              "Max Medyk",
              "https://www.pexels.com/video/man-doing-self-checkout-in-supermarket-7457422/"),
}


def B(kicker, sub, nar, q, pexels_id, cap=None):
    link, autor, pagina = BROLL[pexels_id]
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q, "broll_url": link,
         "broll_credito": {"pexels_id": pexels_id, "autor": autor, "url": pagina}}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub, "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================
# A resposta — a conta inteira, com as quatro entradas nomeadas — abre o
# capitulo 2, que a estimativa poe perto dos 80 s e fecha perto dos 160 s. Vou
# medir a FRASE no legendas.srt depois do render, nao a abertura de capitulo
# (aprendizado 537: a abertura erra de +42 a +49 s).

# ---------------------------- 1 -------------------------------------- ~80 s
B("Δύο τιμές", "στο ίδιο χαρτί",
  "Κάθε προσφορά με δόσεις έχει πάνω της δύο τιμές. Σχεδόν κανείς δεν τις βάζει δίπλα δίπλα, και εκεί κρύβεται όλη η απάντηση.",
  "black friday sale tags", 6114652, cap="Δύο τιμές στο ίδιο χαρτί")
T("Η πρώτη", "αυτή που βλέπεις",
  "Η πρώτη είναι η τιμή μετρητοίς, αυτή που θα πλήρωνες σήμερα. Είναι τυπωμένη, είναι μεγάλη και την προσέχεις αμέσως. Είναι και η μόνη τιμή που θα πλήρωνες χωρίς καμία άλλη συμφωνία.")
T("Η δεύτερη", "δεν γράφεται ποτέ ολόκληρη",
  "Η δεύτερη είναι το σύνολο των δόσεων, και αυτό δεν το τυπώνει σχεδόν κανείς. Τυπώνεται μόνο το ποσό της κάθε δόσης.")
T("Γιατί το ποσό της δόσης", "είναι ο αριθμός που πείθει",
  "Και το ποσό της δόσης είναι ο αριθμός που σε κάνει να πεις ναι, επειδή είναι μικρός και χωράει άνετα στον μισθό του μήνα.")
T("Η λέξη άτοκες", "μπαίνει δίπλα στον μικρό αριθμό",
  "Η λέξη άτοκες μπαίνει πάντα δίπλα σε αυτόν τον μικρό αριθμό, και το μυαλό διαβάζει ότι δεν πληρώνεις τίποτα παραπάνω. Μπαίνει εκεί επειδή εκεί κοιτάζει το μάτι, και όχι στο σύνολο.")
T("Μπορεί να ισχύει", "μπορεί και όχι",
  "Αυτό μπορεί να ισχύει απόλυτα. Μπορεί και όχι, και το χαρτί που κρατάς στο χέρι το λέει μόνο του, με μία αφαίρεση.")
T("Τι δεν θα σου πω", "και γιατί",
  "Δεν θα σου πω τι κάνουν τα καταστήματα ούτε τι επιλέγει η πλειονότητα. Δεν έχω πηγή για αυτά και δεν μιλάω από μνήμη.")
T("Ούτε αν είναι καλό", "αυτό δεν το κρίνει ο υπολογισμός",
  "Ούτε θα σου πω αν οι δόσεις είναι καλή ή κακή επιλογή. Αυτό εξαρτάται από πράγματα που μόνο εσύ μπορείς να ζυγίσεις. Το απόθεμα και οι ανάγκες σου δεν γράφονται σε κανένα χαρτί.")
T("Τι θα σου δείξω", "δύο γραμμές και τέσσερις αριθμούς",
  "Θα σου δείξω έναν υπολογισμό δύο γραμμών, και μετά πού ακριβώς βρίσκεις κάθε αριθμό του μέσα στη δική σου προσφορά.")

# ---------------------------- 2 -------------------------------------- ~80 s
B("Ο υπολογισμός", "και είναι μία αφαίρεση",
  "Η πρώτη γραμμή: αριθμός δόσεων επί το ποσό της δόσης. Αυτό είναι το σύνολο που θα δώσεις αν πληρώσεις με δόσεις.",
  "salesman filling the receipt", 6117602, cap="Ο υπολογισμός")
T("Η δεύτερη γραμμή", "η αφαίρεση",
  "Η δεύτερη γραμμή: από αυτό το σύνολο αφαιρείς την τιμή μετρητοίς του ίδιου χαρτιού. Ό,τι μένει είναι το κόστος. Δύο πράξεις συνολικά, και καμία δεν θέλει κομπιουτεράκι.")
T("Αν μείνει μηδέν", "ήταν πράγματι άτοκες",
  "Αν μείνει μηδέν, οι δόσεις ήταν πράγματι άτοκες και δεν πλήρωσες τίποτα για τη διευκόλυνση. Τελείωσε εδώ ο έλεγχος.")
T("Αν μείνει θετικό", "αυτό είναι η τιμή της διευκόλυνσης",
  "Αν μείνει θετικός αριθμός, αυτό είναι όσο κόστισε η διευκόλυνση, όποιο όνομα κι αν έχει πάνω στο χαρτί.")
T("Το ποσοστό", "για να συγκρίνεις προσφορές",
  "Για να συγκρίνεις δύο προσφορές, διαίρεσε αυτή τη διαφορά με την τιμή μετρητοίς. Βγαίνει ένα ποσοστό, και συγκρίνεται. Το όνομα της γραμμής δεν αλλάζει το ποσό που φεύγει.")
T("Προσοχή στη λέξη", "επιτόκιο δεν είναι",
  "Το ποσοστό αυτό δεν είναι επιτόκιο και δεν το λέω επιτόκιο. Είναι απλώς πόσο παραπάνω έδωσες, σε σχέση με την τιμή.")
T("Γιατί όχι επιτόκιο", "ο χρόνος λείπει",
  "Δεν είναι επιτόκιο επειδή δεν περιέχει τον χρόνο: δώδεκα μήνες και είκοσι τέσσερις μήνες βγάζουν το ίδιο νούμερο.")
T("Και πάλι χρησιμεύει", "συγκρίνει ίδιες διάρκειες",
  "Χρησιμεύει όμως όταν συγκρίνεις δύο προσφορές με την ίδια διάρκεια, που είναι και η πιο συχνή περίπτωση στο κατάστημα. Η λέξη επιτόκιο έχει νομικό περιεχόμενο που εδώ δεν ισχύει.")
T("Τέσσερις αριθμοί", "και όλοι από ένα χαρτί",
  "Όλος ο υπολογισμός θέλει τέσσερις αριθμούς, και όλοι βρίσκονται στο ίδιο χαρτί. Πάμε να δούμε πού είναι ο καθένας.")

# ---------------------------- 3 -------------------------------------- ~80 s
B("Πού τα βρίσκεις", "στην προσφορά ή στη σύμβαση",
  "Ο πρώτος αριθμός είναι η τιμή μετρητοίς. Ψάξε τη λέξη μετρητοίς, ή την τιμή που δίνεται χωρίς καμία αναφορά σε δόσεις.",
  "person holding a price tag", 5836824, cap="Πού τα βρίσκεις στο χαρτί")
T("Μην μπερδευτείς", "η αρχική τιμή δεν είναι αυτή",
  "Μην την μπερδέψεις με την αρχική τιμή πριν την έκπτωση. Θέλεις αυτή που θα πλήρωνες όντως σήμερα, μετά την έκπτωση. Η αρχική τιμή υπάρχει στο χαρτί για να φαίνεται η έκπτωση.")
T("Ο δεύτερος αριθμός", "πόσες δόσεις",
  "Ο δεύτερος είναι ο αριθμός των δόσεων. Γράφεται συνήθως μαζί με τη λέξη άτοκες, και είναι ο ευκολότερος να βρεις.")
T("Ο τρίτος", "το ποσό κάθε δόσης",
  "Ο τρίτος είναι το ποσό της κάθε δόσης. Αν η προσφορά δίνει μόνο αυτό και όχι το σύνολο, τότε το σύνολο το φτιάχνεις εσύ.")
T("Ο τέταρτος", "και είναι ο πιο κρυμμένος",
  "Ο τέταρτος είναι η γραμμή των εξόδων, αν υπάρχει. Έξοδα φακέλου, διαχειριστικά, δαπάνες σύμβασης: τα ονόματα αλλάζουν. Αν τα βρεις, κράτα και το ακριβές όνομα της γραμμής.")
T("Αν δεν υπάρχει", "βάζεις μηδέν",
  "Αν τέτοια γραμμή δεν υπάρχει στο χαρτί σου, βάζεις μηδέν και προχωράς. Δεν υποθέτεις έξοδα που δεν είναι γραμμένα.")
T("Δύο λέξεις", "που δεν είναι το ίδιο",
  "Προσοχή σε δύο λέξεις που μοιάζουν: συνολικό ποσό πληρωμής και συνολικό κόστος. Η μία περιέχει το κεφάλαιο, η άλλη όχι.")
T("Αν βρεις το σύνολο", "ακόμα καλύτερα",
  "Αν η προσφορά γράφει κάπου το συνολικό ποσό πληρωμής, χρησιμοποίησέ το αυτούσιο. Σου γλιτώνει τον πρώτο πολλαπλασιασμό. Διάβασε ποια από τις δύο περιέχει το κεφάλαιο, και κράτα εκείνη.")
T("Τώρα το ερώτημα", "γιατί άτοκες και όχι ίδια τιμή",
  "Έχεις τέσσερα νούμερα και μία αφαίρεση. Μένει να δούμε γιατί η λέξη άτοκες δεν υπόσχεται ποτέ την ίδια τελική τιμή.")

# ---------------------------- 4 -------------------------------------- ~80 s
B("Τι σημαίνει άτοκες", "και τι δεν σημαίνει",
  "Η λέξη άτοκες αφορά μία γραμμή: τον τόκο. Λέει ότι δεν χρεώνεται τόκος πάνω στο ποσό, και αυτό μπορεί να είναι ακριβές.",
  "a red card for price discount", 5644247, cap="Τι σημαίνει άτοκες")
T("Δεν αφορά", "τις άλλες γραμμές",
  "Δεν λέει όμως τίποτα για τις υπόλοιπες γραμμές του χαρτιού, ούτε για το ποια τιμή μπήκε ως βάση του παραστατικού. Ο τόκος είναι μία γραμμή, και το σύνολο είναι όλες μαζί.")
T("Η βάση μπορεί να διαφέρει", "και αυτό είναι το σημείο",
  "Και η βάση μπορεί να διαφέρει: η τιμή που μπαίνει στις δόσεις δεν είναι υποχρεωτικά ίδια με την τιμή μετρητοίς.")
T("Δεν λέω ότι συμβαίνει", "λέω ότι το χαρτί το δείχνει",
  "Δεν σου λέω ότι αυτό συμβαίνει, γιατί δεν έχω πηγή για το τι συμβαίνει. Σου λέω ότι η αφαίρεση το δείχνει αμέσως.")
T("Γι' αυτό η σύγκριση", "είναι σύνολο με σύνολο",
  "Γι' αυτό η σύγκριση γίνεται σύνολο με σύνολο, και όχι λέξη με λέξη. Οι λέξεις περιγράφουν γραμμές, το σύνολο κρίνει. Δύο σύνολα, ένα πρόσημο, και η απάντηση είναι εκεί.")
T("Η αντίρρηση", "μου το είπαν στο κατάστημα",
  "Θα πεις: μου το είπαν στο κατάστημα, είναι άτοκες. Μπορεί και να είναι, και τότε η αφαίρεσή σου θα βγάλει μηδέν.")
T("Αυτό είναι το καλό", "ο έλεγχος δεν μαλώνει",
  "Αυτό είναι το καλό με αυτόν τον έλεγχο: δεν αντιλέγει σε κανέναν. Επιβεβαιώνει ή δεν επιβεβαιώνει, με δύο αριθμούς.")
T("Και τον κάνεις πριν", "όχι μετά",
  "Και τον κάνεις πριν υπογράψεις, όρθιος, στο ταμείο. Δεν χρειάζεται εφαρμογή, δεν χρειάζεται σύνδεση, δεν χρειάζεται άδεια. Το μόνο που χρειάζεσαι είναι το χαρτί και μισό λεπτό.")
T("Πάμε σε νούμερα", "και είναι επίτηδες στρογγυλά",
  "Για να φανεί καθαρά, πάμε σε νούμερα. Είναι επίτηδες στρογγυλά, και στην επόμενη σκηνή λέω ακριβώς από πού βγαίνουν.")

# ---------------------------- 5 -------------------------------------- ~80 s
B("Παράδειγμα", "και οι αριθμοί είναι επινοημένοι",
  "Το λέω πρώτο και καθαρά: οι αριθμοί που ακολουθούν είναι επινοημένοι από εμένα για να φαίνεται ο υπολογισμός.",
  "a printed sale tag", 5889461, cap="Παράδειγμα με στρογγυλούς αριθμούς")
T("Δεν είναι προσφορά", "κανενός καταστήματος",
  "Δεν είναι τιμή κανενός προϊόντος, δεν είναι προσφορά κανενός καταστήματος και δεν μετρήθηκαν πουθενά. Είναι παράδειγμα. Τα βάζω στρογγυλά για να μπορείς να τα ακολουθήσεις στο μυαλό.")
T("Η τιμή μετρητοίς", "ο πρώτος αριθμός",
  "Έστω τιμή μετρητοίς εξακόσια ευρώ. Αυτός είναι ο αριθμός με τον οποίο θα συγκριθεί όλο το υπόλοιπο του υπολογισμού.")
T("Οι δόσεις", "πόσες και πόσο",
  "Έστω δώδεκα δόσεις των πενήντα πέντε ευρώ. Αυτά είναι τα δύο νούμερα που σχεδόν πάντα είναι τυπωμένα στην προσφορά.")
T("Ο πολλαπλασιασμός", "η πρώτη γραμμή",
  "Δώδεκα επί πενήντα πέντε μας δίνει εξακόσια εξήντα ευρώ. Αυτό είναι το σύνολο των δόσεων, και δεν ήταν τυπωμένο πουθενά. Αυτός είναι ο αριθμός που κανένα χαρτί δεν σου έδωσε έτοιμο.")
T("Η γραμμή των εξόδων", "αν υπάρχει",
  "Έστω ότι το χαρτί γράφει και είκοσι ευρώ έξοδα. Τα προσθέτουμε, και το σύνολο γίνεται εξακόσια ογδόντα ευρώ.")
T("Η αφαίρεση", "και η απάντηση",
  "Αφαιρούμε την τιμή μετρητοίς από αυτό το σύνολο. Μένουν ογδόντα ευρώ, και αυτά είναι το κόστος της διευκόλυνσης.")
T("Το ποσοστό", "για σύγκριση",
  "Ογδόντα δια εξακόσια είναι κάτι πάνω από δεκατρία τοις εκατό της τιμής μετρητοίς, για διευκόλυνση ενός έτους.")
T("Και αν τα έξοδα", "ήταν μηδέν",
  "Αν η γραμμή των εξόδων δεν υπήρχε, θα έμεναν εξήντα ευρώ αντί για ογδόντα. Η γραμμή αυτή αλλάζει μόνη της το αποτέλεσμα.")

# ---------------------------- 6 -------------------------------------- ~80 s
B("Τα έξοδα", "η γραμμή που αλλάζει το αποτέλεσμα",
  "Η γραμμή των εξόδων αξίζει δικό της κεφάλαιο, γιατί είναι η μόνη που μπορεί να γυρίσει ένα μηδέν σε θετικό αριθμό.",
  "cashier using a cash register", 3970164, cap="Τα έξοδα στη σύγκριση")
T("Πρώτος κανόνας", "μπαίνει ό,τι είναι γραμμένο",
  "Ο κανόνας είναι απλός και μονόδρομος: στη σύγκριση μπαίνει ό,τι είναι γραμμένο στο χαρτί σου, και τίποτα άλλο. Ό,τι δεν είναι γραμμένο δεν μπαίνει, ούτε ως υπόθεση.")
T("Δεύτερος κανόνας", "μία φορά το καθένα",
  "Και μπαίνει μία φορά. Αν τα έξοδα είναι ήδη μέσα στο ποσό της δόσης, δεν τα προσθέτεις ξανά από πάνω.")
T("Πώς το καταλαβαίνεις", "με τον πολλαπλασιασμό",
  "Το καταλαβαίνεις από τον πολλαπλασιασμό: αν δόσεις επί ποσό βγάζει ήδη το συνολικό ποσό πληρωμής, τα έξοδα είναι μέσα. Αυτή η επαλήθευση παίρνει δέκα δευτερόλεπτα και κόβει το λάθος.")
T("Αν δεν βγάζει", "τότε είναι έξω",
  "Αν ο πολλαπλασιασμός βγάζει λιγότερα από το συνολικό ποσό πληρωμής, η διαφορά είναι ακριβώς τα έξοδα που μπαίνουν έξω.")
T("Τα ασφάλιστρα", "ίδια λογική",
  "Την ίδια λογική κάνεις και με ασφάλιστρα ή εγγυήσεις που μπήκαν στη σύμβαση: γραμμένα μπαίνουν, άγραφα δεν υπάρχουν. Το κριτήριο είναι ένα: γράφεται στη σελίδα που υπογράφεις.")
T("Τι δεν μετράς", "τον χρόνο σου",
  "Δεν μετράς τον χρόνο σου, τη βενζίνη ή τη διάθεσή σου. Αυτά υπάρχουν, αλλά δεν συγκρίνονται με τίποτα στο χαρτί.")
T("Γιατί όχι", "για να μένει ελέγξιμο",
  "Τα κρατάμε έξω για να παραμένει ο υπολογισμός ελέγξιμος: δύο άνθρωποι με το ίδιο χαρτί πρέπει να βγάλουν το ίδιο νούμερο. Αν δύο άνθρωποι βγάζουν άλλο νούμερο, κάποιος πρόσθεσε υπόθεση.")
T("Τώρα τα όρια", "πού ο υπολογισμός δεν φτάνει",
  "Μένει να πω πού αυτός ο υπολογισμός δεν φτάνει, γιατί υπάρχουν τρεις περιπτώσεις που δεν τις καλύπτει καθόλου.")

# ---------------------------- 7 -------------------------------------- ~80 s
B("Πού δεν φτάνει", "τρεις περιπτώσεις",
  "Πρώτη περίπτωση: η τιμή μετρητοίς δεν αναγράφεται πουθενά. Τότε δεν έχεις δεύτερη τιμή, και η αφαίρεση δεν γίνεται.",
  "couple paying at the counter", 4121754, cap="Πού δεν φτάνει ο υπολογισμός")
T("Τι κάνεις τότε", "ρωτάς, δεν υποθέτεις",
  "Τότε ρωτάς ποια είναι η τιμή μετρητοίς, πριν συζητήσεις δόσεις. Δεν την υποθέτεις και δεν τη βρίσκεις στο διαδίκτυο. Η ερώτηση είναι μία και είναι θεμιτή σε κάθε κατάστημα.")
T("Γιατί όχι στο διαδίκτυο", "άλλη τιμή, άλλο χαρτί",
  "Η τιμή άλλου καταστήματος είναι άλλο χαρτί. Ο έλεγχος δουλεύει μόνο όταν οι δύο τιμές είναι στην ίδια προσφορά.")
T("Δεύτερη περίπτωση", "οι δόσεις από κάρτα",
  "Δεύτερη περίπτωση: οι δόσεις δεν είναι του καταστήματος αλλά της κάρτας σου. Τότε το χαρτί είναι η σύμβαση της κάρτας.")
T("Γιατί αλλάζει", "άλλες γραμμές, άλλο έγγραφο",
  "Αλλάζει επειδή οι γραμμές ζουν σε άλλο έγγραφο, με δικούς του όρους. Η αριθμητική είναι ίδια, η πηγή των αριθμών όχι. Ίδια πράξη, άλλη πηγή: αυτό είναι όλη η διαφορά.")
T("Τι δεν θα πω εδώ", "ούτε μία λέξη",
  "Για τους όρους των καρτών δεν θα πω ούτε μία λέξη: εξαρτώνται από σύμβαση και από κανονισμό, και δεν έχω πηγή.")
T("Τρίτη περίπτωση", "διαφορετικές διάρκειες",
  "Τρίτη περίπτωση: συγκρίνεις δύο προσφορές με διαφορετικό αριθμό δόσεων. Τότε το ποσοστό των δύο δεν συγκρίνεται άμεσα.")
T("Τι συγκρίνεται", "το ευρώ, πάντα",
  "Αυτό που συγκρίνεται πάντα είναι το ευρώ: πόσα παραπάνω δίνεις στη μία και πόσα στην άλλη, σε απόλυτο νούμερο.")
T("Και μετά", "το πιο σημαντικό κεφάλαιο",
  "Μένει ένα κεφάλαιο, και είναι το πιο σημαντικό: τι από όλα αυτά δεν αποφασίζει ο υπολογισμός για λογαριασμό σου.")

# ---------------------------- 8 -------------------------------------- ~80 s
B("Τι δεν αποφασίζει", "και είναι σκόπιμο",
  "Αυτός ο υπολογισμός δεν λέει ότι οι δόσεις είναι λάθος. Λέει μόνο πόσο κοστίζει η επιλογή, και η επιλογή είναι δική σου.",
  "busy retail checkout", 35042443, cap="Τι δεν αποφασίζει")
T("Το ρευστό αξίζει", "και αυτό είναι αληθινό",
  "Τα χρήματα σήμερα δεν είναι ίδια με τα χρήματα σε δώδεκα μήνες. Όποιος κρατά ρευστό αγοράζει κάτι πραγματικό με αυτό. Αυτό δεν είναι γνώμη μου, είναι ο λόγος που υπάρχουν οι δόσεις.")
T("Το απόθεμα", "ο λόγος που μετρά περισσότερο",
  "Και υπάρχει ο πιο σοβαρός λόγος: να μη μείνεις χωρίς απόθεμα για μια βλάβη ή μια ανάγκη που δεν ρωτά πότε έρχεται.")
T("Αν αυτό ισχύει", "τα ογδόντα ευρώ είναι τιμή",
  "Αν αυτό ισχύει για εσένα, το κόστος της διευκόλυνσης δεν είναι σπατάλη. Είναι η τιμή μιας ασφάλειας που αγοράζεις.")
T("Αν δεν ισχύει", "τότε είναι δώρο",
  "Αν όμως τα χρήματα υπάρχουν και κάθονται, τότε το ίδιο ποσό είναι απλώς δώρο που δίνεις χωρίς να πάρεις τίποτα πίσω. Και τότε το χαρτί σου λέει ακριβώς πόσο μεγάλο είναι το δώρο.")
T("Η διαφορά", "δεν είναι στο νούμερο",
  "Η διαφορά μεταξύ των δύο δεν είναι στο νούμερο. Το νούμερο είναι το ίδιο, και αλλάζει μόνο τι αγοράζεις με αυτό.")
T("Γι' αυτό δεν συστήνω", "ούτε το ένα ούτε το άλλο",
  "Γι' αυτό δεν συστήνω ούτε μετρητά ούτε δόσεις. Δεν ξέρω το απόθεμά σου, και χωρίς αυτό καμία σύσταση δεν στέκει.")
T("Αυτό που κερδίζεις", "είναι η επίγνωση",
  "Αυτό που κερδίζεις από τον υπολογισμό είναι να ξέρεις το ποσό πριν το δώσεις, αντί να το μάθεις στην τελευταία δόση.")
T("Και τέσσερα βήματα", "όλα στο ταμείο",
  "Κλείνουμε με τέσσερα βήματα που γίνονται όρθιος στο ταμείο, σε λιγότερο από ένα λεπτό, με το χαρτί στο χέρι.")

# ---------------------------- 9 -------------------------------------- ~80 s
B("Βήμα πρώτο", "βρες τη τιμή μετρητοίς",
  "Βήμα πρώτο: βρες στο χαρτί την τιμή μετρητοίς, μετά την έκπτωση. Αν δεν υπάρχει, ζήτα τη πριν συζητήσεις δόσεις.",
  "man doing self checkout", 7457422, cap="Τέσσερα βήματα")
T("Βήμα δεύτερο", "κάνε τον πολλαπλασιασμό",
  "Βήμα δεύτερο: πολλαπλασίασε τον αριθμό των δόσεων με το ποσό της δόσης, και κράτα το αποτέλεσμα στο χαρτί ή στο κινητό. Κράτα το γραμμένο, γιατί θα το χρειαστείς στην αφαίρεση.")
T("Βήμα τρίτο", "πρόσθεσε μόνο τα γραμμένα",
  "Βήμα τρίτο: πρόσθεσε τα έξοδα, αλλά μόνο αν είναι γραμμένα και μόνο αν δεν είναι ήδη μέσα στο ποσό της δόσης.")
T("Βήμα τέταρτο", "η αφαίρεση",
  "Βήμα τέταρτο: αφαίρεσε την τιμή μετρητοίς. Ό,τι μένει είναι το κόστος, και αν μένει μηδέν ήταν πράγματι άτοκες.")
T("Μία προειδοποίηση", "για το μηδέν",
  "Μία προειδοποίηση για το μηδέν: αν βγει αρνητικός αριθμός, κάτι διάβασες λάθος. Έλεγξε αν πήρες την αρχική τιμή. Αρνητικό νούμερο δεν σημαίνει κέρδος, σημαίνει λάθος ανάγνωση.")
T("Πόσο παίρνει", "λιγότερο από ένα λεπτό",
  "Όλα αυτά παίρνουν λιγότερο από ένα λεπτό, και παίρνουν ακόμα λιγότερο τη δεύτερη φορά που θα τα κάνεις.")
T("Πότε το κάνεις", "πριν την υπογραφή",
  "Το σωστό σημείο είναι πριν την υπογραφή. Μετά την υπογραφή ο ίδιος υπολογισμός σου λέει το ίδιο νούμερο, αλλά αργά.")
T("Το κέρδος", "δεν είναι να μην πληρώσεις",
  "Και το κέρδος δεν είναι να μην πληρώσεις ποτέ. Είναι να μην πληρώνεις ποτέ χωρίς να ξέρεις τι ακριβώς πληρώνεις. Η διαφορά ανάμεσα στα δύο είναι όλη η ουσία.")
C("Γράψε μόνο ένα", "χωρίς ποσά και χωρίς καταστήματα",
  "Αν κάνεις την αφαίρεση, γράψε στα σχόλια μόνο αν βγήκε μηδέν ή όχι. Χωρίς ποσά, χωρίς προϊόντα, χωρίς καταστήματα.")


# =============================== O SHORT =====================================
# `liberado` nao manda o melhor material para o short, mas o short TAMBEM
# entrega a conta — e aqui ela cabe inteira em duas frases. Nenhuma sigla de
# orgao e nenhuma cifra oficial no titulo: o pacote 002 e o 003 tem os dois
# shorts mais vistos do canal (1.614 e 1.407) e as duas piores travessias.
SHORT = [
    {"layout": "titulo", "kicker": "Δύο τιμές", "sub": "στο ίδιο χαρτί",
     "nar": "Κάθε προσφορά με δόσεις έχει δύο τιμές πάνω της. Σχεδόν κανείς "
            "δεν τις βάζει δίπλα δίπλα.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Η μία τυπώνεται", "sub": "η άλλη όχι",
     "nar": "Η τιμή μετρητοίς είναι τυπωμένη. Το σύνολο των δόσεων δεν είναι: "
            "το φτιάχνεις εσύ.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Μία γραμμή", "sub": "δόσεις επί ποσό",
     "nar": "Πολλαπλασίασε τον αριθμό των δόσεων με το ποσό της δόσης, και "
            "πρόσθεσε τα γραμμένα έξοδα.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Μία αφαίρεση", "sub": "και η απάντηση",
     "nar": "Αφαίρεσε την τιμή μετρητοίς. Αν μείνει μηδέν, ήταν πράγματι "
            "άτοκες. Αν μείνει κάτι, αυτό κόστισαν.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Πριν υπογράψεις", "sub": "όχι μετά",
     "nar": "Ο έλεγχος δεν αντιλέγει σε κανέναν: επιβεβαιώνει ή όχι. Όλος ο "
            "υπολογισμός είναι στο βίντεο.",
     "sem_cap": True},
]

THUMB = {"l1": "Άτοκες;", "l2": "δύο τιμές"}

COPY = """# epomeno-epipedo-017

## TITULO
Άτοκες Δόσεις: Δύο Τιμές στο Ίδιο Χαρτί Λένε Αν Ήταν Πράγματι Άτοκες — Υπολόγισέ το Μόνος

## TITULO SHORT
Άτοκες; Δύο τιμές στο χαρτί σου

## DESCRICAO
Κάθε προσφορά με δόσεις έχει πάνω της δύο τιμές, και σχεδόν κανείς δεν τις βάζει δίπλα δίπλα. Η πρώτη είναι η τιμή μετρητοίς: τυπωμένη, μεγάλη, την προσέχεις αμέσως. Η δεύτερη είναι το σύνολο των δόσεων — και αυτό δεν το τυπώνει σχεδόν κανείς. Τυπώνεται μόνο το ποσό της κάθε δόσης, που είναι και ο αριθμός που σε κάνει να πεις ναι, επειδή είναι μικρός και χωράει άνετα στον μισθό του μήνα. Η λέξη «άτοκες» μπαίνει πάντα δίπλα σε αυτόν τον μικρό αριθμό, και το μυαλό διαβάζει ότι δεν πληρώνεις τίποτα παραπάνω.

Μπορεί να ισχύει απόλυτα. Μπορεί και όχι — και το χαρτί που κρατάς στο χέρι το λέει μόνο του, με μία αφαίρεση. Ο υπολογισμός είναι δύο γραμμές: αριθμός δόσεων επί το ποσό της δόσης δίνει το σύνολο που θα δώσεις, και από αυτό αφαιρείς την τιμή μετρητοίς του ίδιου χαρτιού. Αν μείνει μηδέν, οι δόσεις ήταν πράγματι άτοκες και ο έλεγχος τελείωσε. Αν μείνει θετικός αριθμός, αυτό είναι όσο κόστισε η διευκόλυνση, όποιο όνομα κι αν έχει πάνω στο χαρτί. Για να συγκρίνεις δύο προσφορές, διαίρεσε τη διαφορά με την τιμή μετρητοίς — και πρόσεξε ότι το ποσοστό αυτό ΔΕΝ είναι επιτόκιο, γιατί δεν περιέχει τον χρόνο: δώδεκα και είκοσι τέσσερις μήνες βγάζουν το ίδιο νούμερο.

Το βίντεο δείχνει πού βρίσκεις κάθε έναν από τους τέσσερις αριθμούς μέσα στη δική σου προσφορά: την τιμή μετρητοίς (όχι την αρχική τιμή πριν την έκπτωση), τον αριθμό των δόσεων, το ποσό της κάθε δόσης και τη γραμμή των εξόδων — αν υπάρχει. Αν δεν υπάρχει, βάζεις μηδέν: δεν υποθέτεις έξοδα που δεν είναι γραμμένα. Ένα ολόκληρο κεφάλαιο πάει στα έξοδα, επειδή είναι η μόνη γραμμή που μπορεί να γυρίσει ένα μηδέν σε θετικό αριθμό, και στο πώς καταλαβαίνεις αν είναι ήδη μέσα στη δόση ή έξω από αυτή.

Ένα άλλο κεφάλαιο λέει πού ο υπολογισμός ΔΕΝ φτάνει, και είναι τρεις περιπτώσεις: όταν η τιμή μετρητοίς δεν αναγράφεται πουθενά, όταν οι δόσεις είναι της κάρτας και όχι του καταστήματος, και όταν συγκρίνεις προσφορές με διαφορετικό αριθμό δόσεων.

Και το τελευταίο κεφάλαιο είναι το πιο σημαντικό: τι ΔΕΝ αποφασίζει αυτός ο υπολογισμός. Δεν λέει ότι οι δόσεις είναι λάθος. Τα χρήματα σήμερα δεν είναι ίδια με τα χρήματα σε δώδεκα μήνες, και όποιος κρατά απόθεμα για μια βλάβη που δεν ρωτά πότε έρχεται αγοράζει κάτι πραγματικό. Αν αυτό ισχύει για εσένα, το κόστος της διευκόλυνσης είναι η τιμή μιας ασφάλειας. Αν τα χρήματα υπάρχουν και κάθονται, το ίδιο ποσό είναι δώρο χωρίς αντάλλαγμα. Το νούμερο είναι το ίδιο· αλλάζει μόνο τι αγοράζεις με αυτό. Γι' αυτό το βίντεο δεν συστήνει ούτε μετρητά ούτε δόσεις.

Υλικό πληροφόρησης, δεν αποτελεί οικονομική συμβουλή.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Ο υπολογισμός είναι στα πρώτα δύο λεπτά, οπότε δεν χρειάζεται να δεις όλο το βίντεο για να τον πάρεις: αριθμός δόσεων επί το ποσό της δόσης, συν τα έξοδα αν είναι γραμμένα, μείον την τιμή μετρητοίς του ίδιου χαρτιού. Αν μείνει μηδέν, ήταν πράγματι άτοκες. Αν μείνει κάτι, αυτό κόστισε η διευκόλυνση. Τέσσερις αριθμοί, όλοι από την ίδια σελίδα — και πρόσεξε δύο παγίδες: η τιμή μετρητοίς δεν είναι η αρχική τιμή πριν την έκπτωση, και τα έξοδα μπαίνουν μία φορά (αν ο πολλαπλασιασμός βγάζει ήδη το συνολικό ποσό πληρωμής, είναι μέσα). Αν βγει αρνητικός αριθμός, κάτι διαβάστηκε λάθος. Αν το κάνεις, γράψε στα σχόλια μόνο αν βγήκε μηδέν ή όχι — χωρίς ποσά, χωρίς προϊόντα, χωρίς καταστήματα.

## HASHTAGS
#ΆτοκεςΔόσεις #ΠροσωπικάΟικονομικά #ΕπόμενοΕπίπεδο

## TAGS
ατοκες δοσεις, τιμη μετρητοις, συνολικο ποσο πληρωμης, εξοδα φακελου, κοστος διευκολυνσης, προσωπικα οικονομικα, πως υπολογιζω, δοσεις ή μετρητα, καταναλωτικη πιστη, συγκριση προσφορων, επομενο επιπεδο, οικονομικα σπιτιου, αγορες με δοσεις, ποσοστο επι την τιμη, ελεγχος προσφορας

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
B-roll: Pexels, creditos por clipe em broll_creditos.json e abaixo.
cottonbro studio; Gustavo Fring; kaboompics.com; Max Fischer; Jack Sparrow;
Michael Takahashi; Max Medyk.

## AVISO SOBRE OS NUMEROS
ZERO AFIRMACAO SOBRE O MUNDO, e por isso nao ha fonte a citar: o video nao diz
o que as lojas gregas fazem, nao diz o que a maioria escolhe, nao cita taxa,
indice nem norma.

O QUE O VIDEO AFIRMA E ARITMETICA, e so ela:
  * o total do parcelamento e numero de parcelas vezes o valor da parcela;
  * o custo da facilidade e esse total, MAIS as despesas que estiverem
    escritas no papel do espectador, MENOS o preco a vista do mesmo papel;
  * se der zero, era sem juro de verdade;
  * o percentual e essa diferenca dividida pelo preco a vista — e o video DIZ
    que esse percentual NAO e taxa de juro, porque nao contem o tempo.

AS ENTRADAS SAO TODAS DO ESPECTADOR, e sao quatro, todas da MESMA folha: preco
a vista, numero de parcelas, valor da parcela e a linha de despesas, se
existir. Nenhum numero meu entra no resultado.

O EXEMPLO DO CAPITULO CINCO E HIPOTETICO E O VIDEO DIZ ISSO NA CENA QUE O ABRE:
seiscentos euros a vista, doze parcelas de cinquenta e cinco, vinte euros de
despesa. Nao e preco de produto nenhum, nao e oferta de loja nenhuma e nao foi
medido em lugar nenhum.

O QUE FOI DESCARTADO, e o descarte vai escrito porque e a regra da casa:
  (1) o que os comercios gregos cobram ou oferecem;
  (2) o que a maioria das pessoas escolhe;
  (3) os termos de cartao de credito e de parcelamento bancario, que dependem
      de contrato e de regulamento e que eu nao fecho em duas fontes — o
      capitulo sete diz isso com todas as letras e se recusa a falar deles;
  (4) UMA PAUTA INTEIRA, e esta vale registrar: o Eurostat ABRIU e o dataset
      `ilc_lvho07a` entregou numeros fortes para 2025 (26,4% na Grecia contra
      7,7% na UE, e 82,6% contra 12,7% pelos dois lados da linha de pobreza,
      com `updated` de 17/09/2026). Caiu porque o indicador se define por um
      LIMIAR que eu NAO achei na fonte: baixei o proprio `ilc_sieusilc.sdmx.zip`
      do Eurostat (HTTP 200, 2,25 MB) e a definicao nao esta nele. Sem o limiar
      o espectador nao se coloca de lado nenhum, e limiar de memoria nao entra.

E O QUE A CONTA NAO DECIDE esta no capitulo oito inteiro: parcelar nao e
errado. Dinheiro hoje nao e igual a dinheiro em doze meses, e quem parcela para
nao ficar sem reserva compra algo real. O numero e o mesmo nos dois casos; muda
so o que se compra com ele. Por isso o video nao recomenda nem a vista nem
parcelado.

## FONTES
NENHUMA FONTE NORMATIVA OU ESTATISTICA E CITADA, e isso e deliberado. As unicas
"fontes" sao os documentos do proprio espectador: a oferta ou a sumbasi, de onde
saem o preco a vista, o numero de parcelas, o valor da parcela e a linha de
despesas.
B-roll: Pexels, licenca Pexels, creditos por clipe em broll_creditos.json.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-017",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    # Faixa do canal em TRES pacotes (013, 014, 015). O 016, meu, saiu fora.
    "paleta": {"ink": "#12263A", "c1": "#2A9D8F", "c2": "#E8A33D",
               "bg": "#F5F2EC"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import (duracao_estimada, duracao_estimada_short, duracao_cena,
                        piso_de_caracteres)
    grava(SPEC, "fabrica/specs/epomeno-epipedo-017.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    piso = piso_de_caracteres(SPEC["voz"], n_cenas=len(CENAS), cenas_por_cap=9)
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"piso por cena: {piso['min_por_cena']} (manda o {piso['manda']}) | "
          f"media real: {sum(len(c.get('nar','')) for c in CENAS)/len(CENAS):.0f}")
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
    t = 0.0
    for i, c in enumerate(CENAS):
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
        if "Ό,τι μένει είναι το κόστος" in (c.get("nar") or ""):
            print(f"  a resposta fecha em {t:.1f}s (cena {i})")
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: {c['broll_q']}")
