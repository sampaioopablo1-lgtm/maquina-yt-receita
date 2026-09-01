#!/usr/bin/env python3
"""Monta a spec epomeno-epipedo-013.

ALAVANCA ATACADA: **A — conversao short -> inscrito.** E esta rodada e a
primeira a usar o aprendizado 543, medido e replicado ontem em quatro canais.

NUMERO DE PARTIDA, medido em 01/09/2026 video a video (25 videos):

    epomeno-epipedo ... 14 inscritos (eram 8 em 25/08 — mais 75% em 7 dias)
                        7.227 views, 25 videos
                        short: mediana 41,04 views/dia, topo 113,42
                        longo: mediana 2,05 views/dia
                        veredito: `suspenso`
                        ZERO duplicatas — o unico dos tres canais de sinal
                        que nao tem grupo repetido no ar

Este e o canal que anda. Ele tem quase tres vezes os inscritos do segundo
colocado e e o unico com trajetoria de crescimento.

O QUE DEU CERTO, e agora com o numero certo na mao. Os dois melhores longos
do canal sao "Tekmiria" (vinte virgula oito views/dia) e "Sintaxi 2026"
(catorze virgula tres). Os dois vieram de shorts colados na MEDIANA do canal
— quarenta e quatro virgula tres e quarenta e um virgula seis.

O QUE NAO DEU: os dois MAIORES shorts do canal. O do IVA fez cento e treze
virgula quatro views/dia e o longo dele parou em sete virgula um; o do salario
minimo fez noventa e nove virgula dois e o longo parou em quatro virgula nove.
Alcance de short nao puxa longo — medido aqui, e replicado no polones, no turco
e no portugues (aprendizado 543, quatro canais, cento e trinta videos).

E o que separa os dois vencedores dos dois maiores: os vencedores respondem
**de que lado eu estou e quanto isso me custa**, com prazo. O do IVA e conta
sem consequencia; o do salario minimo compara dois paises, nao o espectador.

O QUE MUDO POR CAUSA DISSO — e sao duas coisas, uma em cada formato:

1. **O LONGO** deixa de ser escolhido pela expectativa de alcance do short e
   passa a ser escolhido pela forma do assunto: escolha binaria, dinheiro dele,
   prazo real. E o assunto sai da regra do Estado e vai para uma decisao que ele
   toma sozinho.
2. **O SHORT** entrega a conta fechada E pede a inscricao, amarrada ao metodo
   (experimento 26, aberto ontem e ja rodando em quatro canais). Este e o
   quinto braco, e o primeiro num canal que ja converte.

--------------------------------------------------------------- DIMENSIONAMENTO

Veredito `suspenso` => PISO de oito minutos, e o melhor material no short. E o
proprio canal confirma o piso: os quatro longos mais curtos dele (oito
minutos e quarenta e quatro a nove minutos e dezesseis) fazem em media onze
virgula um views/dia, contra tres virgula nove dos oito mais longos. Declaro o
confundimento: os curtos sao tambem os mais recentes, e views/dia decai com a
idade — por isso trato isto como consistente com o piso, nao como prova dele.

Oito capitulos, cada um com ~64s NA ESTIMATIVA e nunca 60 (aprendizado 537).
Os tres passos da conta ficam na PRIMEIRA METADE do capitulo 3, e a posicao da
resposta vai ser conferida no `legendas.srt` do artefato — nao pela abertura do
capitulo seguinte, que erra por quarenta e poucos segundos.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO: **quanto custa cada quilometro do teu carro, pelas tuas proprias
aposdeixeis**. Os eixos publicados aqui sao tekmiria, pensao, ENFIA, anos
ficticios, IVA, conta de luz, cor do tarifario, inflacao, juros, salario
liquido, casa propria, salario minimo e sistema de dividas. Custo de uso do
carro nunca foi ao ar, e e a despesa que o grego medio paga sem nunca somar.

AS TRES CONDICOES DO APRENDIZADO 504:
1. o dinheiro e DELE — combustivel, seguro, taxa de circulacao e manutencao do
   ano dele, e os quilometros do proprio conta-quilometros;
2. e ESCOLHA COM PRAZO — a taxa de circulacao e a renovacao do seguro tem data,
   e e antes dela que a conta serve;
3. o SHORT entrega a conta — a divisao fechada, com o resultado, e depois pede
   a inscricao.

FONTES: este video NAO faz nenhuma afirmacao institucional e NAO cita nenhum
numero meu. Nao cita preco de combustivel, nao cita valor de taxa de
circulacao, nao cita premio de seguro, nao cita consumo medio e nao cita marca
nem modelo. Os numeros da conta saem todos das aposdeixeis e do
conta-quilometros do proprio espectador. Nao ha numero meu para certificar em
duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa
do carro dele.

O QUE O VIDEO NAO FAZ: nao diz que ter carro e bom ou ruim, nao recomenda
vender nada, nao compara com transporte publico como se fosse sempre possivel,
nao promete economia e nao e aconselhamento financeiro.
"""
import json

CENAS = []


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def I(kicker, preco, nar):
    CENAS.append({"layout": "item", "kicker": kicker, "preco": preco,
                  "nar": nar, "sem_cap": True})


def L(kicker, itens, nar):
    CENAS.append({"layout": "lista", "kicker": kicker, "itens": itens,
                  "nar": nar, "sem_cap": True})


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================

# -------------------------------------------------------------------- cap 1
T("Πληρώνεις κάθε μήνα", "χωρίς να το αθροίζεις",
  "Το αυτοκίνητό σου σου κοστίζει κάθε μήνα. Λίγο εδώ, λίγο εκεί, ποτέ σε ένα "
  "νούμερο. Και γι' αυτό δεν το έχεις δει ποτέ ολόκληρο.",
  cap="Το ποσό που δεν αθροίζεις")
I("Δεν είναι κατά του αυτοκινήτου", "είναι για να ξέρεις",
  "Αυτό το βίντεο δεν λέει ότι το αυτοκίνητο είναι κακό. Λέει πόσο κοστίζει "
  "το δικό σου, που είναι άλλο ερώτημα και πολύ πιο χρήσιμο.")
I("Και έχει προθεσμία", "τέλη και ασφάλεια",
  "Έχει και προθεσμία που την ξέρεις: τα τέλη και η ανανέωση της ασφάλειας "
  "έχουν ημερομηνία. Πριν από εκείνη χρειάζεσαι το νούμερο.")
I("Τα στοιχεία υπάρχουν", "και είναι δικά σου",
  "Όλα τα στοιχεία υπάρχουν ήδη και είναι δικά σου. Οι αποδείξεις από τη μια, "
  "και το χιλιομετρητή σου από την άλλη.")
I("Κανείς δεν το αθροίζει", "ούτε το πρατήριο",
  "Κανείς δεν κάνει αυτή την πράξη για σένα. Το πρατήριο δείχνει την τιμή του "
  "λίτρου, γιατί αυτή πουλάει. Το κόστος ανά χιλιόμετρο δεν το δείχνει κανείς.")
I("Δεν χρειάζεται αρχείο", "ούτε εφαρμογή",
  "Δεν χρειάζεσαι εφαρμογή ούτε να κρατάς αρχείο από δω και πέρα. Όλα έχουν "
  "ήδη καταγραφεί κάπου, και το μόνο που κάνεις είναι να τα μαζέψεις μία "
  "φορά.")
I("Τι έρχεται", "μία διαίρεση",
  "Σε λίγα λεπτά θα την κάνεις μόνος σου. Είναι μία πρόσθεση και μία "
  "διαίρεση, με νούμερα που ήδη έχεις.")

# -------------------------------------------------------------------- cap 2
T("Οι δύο πλευρές", "τα ευρώ και τα χιλιόμετρα",
  "Η πράξη έχει δύο πλευρές, και το συνηθισμένο λάθος είναι να κοιτάς μόνο "
  "την πρώτη.",
  cap="Τα ευρώ και τα χιλιόμετρα")
I("Πρώτη πλευρά", "όλα όσα πλήρωσες",
  "Η πρώτη πλευρά είναι όλα όσα πλήρωσες για το αυτοκίνητο μέσα σε δώδεκα "
  "μήνες. Όχι μόνο τα καύσιμα.")
I("Μαζί η ασφάλεια", "και τα τέλη",
  "Μαζί η ασφάλεια, τα τέλη κυκλοφορίας και το τεχνικό έλεγχο, αν έπεσε μέσα "
  "στη χρονιά.")
I("Μαζί το σέρβις", "και τα λάστιχα",
  "Μαζί το σέρβις και τα λάστιχα. Αυτά δεν έρχονται κάθε μήνα, αλλά έρχονται, "
  "και είναι μέρος του κόστους.")
I("Και οι σταθμεύσεις", "και τα διόδια",
  "Μαζί και η στάθμευση και τα διόδια, αν τα πληρώνεις τακτικά. Ό,τι δεν θα "
  "πλήρωνες χωρίς αυτό το αυτοκίνητο, μπαίνει.")
I("Δεύτερη πλευρά", "τα χιλιόμετρα",
  "Η δεύτερη πλευρά είναι τα χιλιόμετρα που έκανες στους ίδιους δώδεκα μήνες. "
  "Από τον χιλιομετρητή, όχι από τη μνήμη.")
I("Ίδιοι δώδεκα μήνες", "και στις δύο πλευρές",
  "Χρησιμοποίησε τους ίδιους δώδεκα μήνες και στις δύο πλευρές. Ένας χρόνος "
  "καυσίμων με έναν μήνα χιλιομέτρων δεν βγάζει τίποτα.")
I("Και αν άλλαξες αυτοκίνητο", "μέτρα μόνο το τωρινό",
  "Αν άλλαξες αυτοκίνητο μέσα στη χρονιά, μέτρα μόνο την περίοδο του τωρινού. "
  "Δύο αυτοκίνητα μαζί δίνουν νούμερο που δεν ισχύει για κανένα από τα δύο.")
I("Τώρα συγκρίνονται", "ευρώ προς χιλιόμετρο",
  "Με τα ευρώ από τη μια και τα χιλιόμετρα από την άλλη, αυτό παύει να είναι "
  "εντύπωση και γίνεται αριθμητική.")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA — os tres passos na PRIMEIRA METADE do capitulo.
T("Η πράξη", "μία διαίρεση",
  "Λοιπόν, η πράξη. Μία πρόσθεση και μία διαίρεση.",
  cap="Η πράξη: μία διαίρεση")
I("Βήμα ένα", "πρόσθεσε τα ευρώ",
  "Βήμα πρώτο: πρόσθεσε όλα όσα πλήρωσες μέσα στους δώδεκα μήνες. Γράψ' το.")
I("Βήμα δύο", "βρες τα χιλιόμετρα",
  "Βήμα δεύτερο: βρες τα χιλιόμετρα της ίδιας περιόδου. Γράψε και αυτό.")
I("Βήμα τρία", "διαίρεσε",
  "Βήμα τρίτο: διαίρεσε τα ευρώ με τα χιλιόμετρα. Αυτό είναι το κόστος κάθε "
  "χιλιομέτρου που κάνεις.")
I("Αυτή είναι η απάντηση", "σε ευρώ",
  "Αυτή είναι η απάντηση, και είναι σε ευρώ ανά χιλιόμετρο. Όχι ποσοστό, όχι "
  "γνώμη.")
I("Και τώρα σύγκρινε", "με μια διαδρομή που ξέρεις",
  "Τώρα πολλαπλασίασέ το με μια διαδρομή που κάνεις συχνά. Αυτό είναι το "
  "πραγματικό κόστος εκείνης της διαδρομής, και μπορείς να το βάλεις δίπλα σε "
  "ό,τι θα πλήρωνες αλλιώς.")
I("Γράψ' τα δίπλα δίπλα", "δύο γραμμές",
  "Γράψε τα δύο νούμερα δίπλα δίπλα πριν διαιρέσεις. Και μόνο που τα βλέπεις "
  "μαζί αλλάζει αυτό που καταλαβαίνεις.")
I("Και κράτα το αποτέλεσμα", "με ημερομηνία",
  "Κράτα το αποτέλεσμα με την ημερομηνία που το έβγαλες, για να ξέρεις "
  "αργότερα σε τι αναφέρεται.")
I("Η πράξη τελείωσε", "τα υπόλοιπα είναι το γιατί",
  "Η πράξη τελείωσε εδώ και μπορείς να κάνεις τη δική σου. Τα υπόλοιπα είναι "
  "πού βρίσκεις τα νούμερα και πότε η πράξη σε ξεγελάει.")

# ================== DEPOIS DA RESPOSTA — POR QUE CONTINUAR ===================

# -------------------------------------------------------------------- cap 4
T("Πού τα βρίσκεις", "χωρίς να κρατάς αρχείο",
  "Το πρακτικό πρόβλημα είναι ότι σχεδόν κανείς δεν κρατάει αρχείο. "
  "Ανασυντίθεται, και με καλή ακρίβεια.",
  cap="Πού βρίσκεις τα νούμερα")
I("Η κάρτα", "δείχνει τα πρατήρια",
  "Ξεκίνα από τις κινήσεις της κάρτας. Τα πρατήρια φαίνονται με ημερομηνία "
  "και ποσό.")
I("Η ασφάλεια", "μία φορά τον χρόνο",
  "Η ασφάλεια και τα τέλη είναι μία πληρωμή τον χρόνο η καθεμία. Εύκολα "
  "εντοπίζονται και δύσκολα ξεχνιούνται μόλις τα ψάξεις.")
I("Το συνεργείο", "κρατάει ιστορικό",
  "Το συνεργείο κρατάει ιστορικό επισκέψεων, και συνήθως θυμάται καλύτερα "
  "από εσένα πότε άλλαξες τι.")
I("Τα χιλιόμετρα", "από δύο σημεία",
  "Για τα χιλιόμετρα, χρειάζεσαι δύο ενδείξεις: μία παλιά και τη σημερινή. Η "
  "παλιά είναι συχνά γραμμένη στο δελτίο του τεχνικού ελέγχου ή σε παλιό "
  "τιμολόγιο σέρβις.")
I("Αν δεν βρεις παλιά", "μέτρα από σήμερα",
  "Αν δεν βρεις καμία, γράψε τη σημερινή ένδειξη και ξαναδές την σε τρεις "
  "μήνες. Πολλαπλασίασε επί τέσσερα.")
I("Μία ώρα φτάνει", "για όλη τη χρονιά",
  "Για μια κανονική χρονιά αυτό είναι περίπου μία ώρα δουλειάς, και η "
  "περισσότερη είναι ξεφύλλισμα. Δεν υπολογίζεις τίποτα μέχρι το τέλος.")
I("Στην αμφιβολία", "μέτρα λιγότερα ευρώ",
  "Και στην αμφιβολία, βάλε λιγότερα ευρώ στη μία πλευρά. Αν το νούμερο "
  "ενοχλεί ακόμη και έτσι, ενοχλεί στ' αλήθεια.")

# -------------------------------------------------------------------- cap 5
T("Τι δεν πιάνει", "και είναι δίκαιο να ειπωθεί",
  "Υπάρχουν πράγματα που αυτή η πράξη δεν πιάνει, και είναι πιο τίμιο να "
  "ειπωθούν παρά να αποσιωπηθούν.",
  cap="Τι δεν πιάνει η πράξη")
I("Η αξία που χάνει", "δεν είναι απόδειξη",
  "Το πρώτο: το αυτοκίνητο χάνει αξία με τον χρόνο, και αυτό δεν έχει "
  "απόδειξη. Δεν μπαίνει εδώ, αλλά υπάρχει.")
I("Το δεύτερο", "ο χρόνος σου",
  "Το δεύτερο πάει αντίστροφα: το αυτοκίνητο σου γλιτώνει χρόνο, και ο χρόνος "
  "σου έχει αξία, ακόμη κι αν δεν βγαίνει από την τσέπη.")
I("Το τρίτο", "όσα δεν γίνονται αλλιώς",
  "Το τρίτο δεν είναι νούμερο: κάποιες διαδρομές απλώς δεν γίνονται αλλιώς. "
  "Αυτό δεν το ακυρώνει τίποτα.")
I("Η πράξη δεν κρίνει", "δείχνει το μέγεθος",
  "Η πράξη δεν λέει ότι πρέπει να αλλάξεις κάτι. Δείχνει το μέγεθος ενός "
  "ποσού που δεν το έβλεπες ολόκληρο.")
I("Το τέταρτο", "όσα δεν πλήρωσες φέτος",
  "Υπάρχει και ένα τέταρτο: κάτι που δεν χρειάστηκε φέτος αλλά θα χρειαστεί "
  "του χρόνου. Ένα μεγάλο σέρβις που δεν έπεσε μέσα στη χρονιά κάνει το "
  "νούμερο πιο μικρό απ' ό,τι είναι.")
I("Γι' αυτό δύο χρονιές", "αν μπορείς",
  "Αν έχεις στοιχεία για δύο χρονιές, κάν' την και στις δύο. Η διαφορά τους "
  "σου λέει πόσο ανομοιόμορφα είναι τα έξοδα.")
I("Και τα σταθερά", "δεν μειώνονται με τα χιλιόμετρα",
  "Ένα τελευταίο: τα τέλη και η ασφάλεια πληρώνονται ίδια είτε κάνεις πολλά "
  "είτε λίγα χιλιόμετρα. Γι' αυτό το κόστος ανά χιλιόμετρο πέφτει όσο "
  "οδηγείς περισσότερο.")

# -------------------------------------------------------------------- cap 6
T("Πότε σε ξεγελάει", "το δεύτερο αυτοκίνητο",
  "Τώρα η περίπτωση που ξεγελάει σχεδόν τους πάντες.",
  cap="Πότε σε ξεγελάει")
I("Λίγα χιλιόμετρα", "ακριβό χιλιόμετρο",
  "Όποιος κάνει λίγα χιλιόμετρα βγάζει πολύ ακριβό χιλιόμετρο, επειδή τα "
  "σταθερά μοιράζονται σε λίγα.")
I("Αυτό δεν λέει", "ότι οδηγείς λάθος",
  "Αυτό δεν σημαίνει ότι κάνεις κάτι λάθος. Σημαίνει ότι πληρώνεις κυρίως για "
  "τη διαθεσιμότητα, όχι για τη χρήση.")
I("Και είναι θεμιτό", "αν το ξέρεις",
  "Και η διαθεσιμότητα είναι θεμιτός λόγος. Το ζήτημα είναι να ξέρεις πόσο "
  "κοστίζει, όχι να την υπερασπίζεσαι στα τυφλά.")
I("Το αντίστροφο", "πολλά χιλιόμετρα",
  "Το αντίστροφο ισχύει επίσης: όποιος κάνει πολλά χιλιόμετρα βγάζει φθηνό "
  "χιλιόμετρο, και μπορεί να νομίζει ότι ξοδεύει λίγα ενώ ξοδεύει πολλά "
  "συνολικά.")
I("Γι' αυτό δύο νούμερα", "όχι ένα",
  "Γι' αυτό κράτα και τα δύο: το σύνολο του χρόνου και το κόστος ανά "
  "χιλιόμετρο. Το ένα χωρίς το άλλο σε παραπλανά.")
I("Και υπάρχει τρίτη περίπτωση", "το δεύτερο αυτοκίνητο",
  "Και υπάρχει μια τρίτη περίπτωση που ξεγελάει ακόμη περισσότερο: το δεύτερο "
  "αυτοκίνητο του σπιτιού. Εκείνο κάνει τα λιγότερα χιλιόμετρα και πληρώνει "
  "τα ίδια σταθερά, οπότε βγάζει το ακριβότερο χιλιόμετρο μακράν.")
I("Καμία απάντηση δεν είναι λάθος", "το νούμερό σου αποφασίζει",
  "Δεν υπάρχει σωστή απάντηση γενικά. Σωστή είναι αυτή που δείχνει το δικό "
  "σου νούμερο. Λάθος είναι μόνο να πληρώνεις χωρίς να το έχεις δει.")

# -------------------------------------------------------------------- cap 7
T("Από τον χρόνο", "στα χρόνια",
  "Τώρα το βήμα που κάνει το μέγεθος να φανεί.",
  cap="Από τον χρόνο στα χρόνια")
I("Ένας χρόνος", "φαίνεται λογικός",
  "Ένας χρόνος φαίνεται λογικός, όποιο κι αν είναι το νούμερο. Γι' αυτό "
  "περνάει κάθε φορά χωρίς να το κοιτάξεις.")
I("Πολλαπλασίασε", "με τα χρόνια που το έχεις",
  "Πολλαπλασίασε με τα χρόνια που έχεις αυτό το αυτοκίνητο. Ίδια συμπεριφορά, "
  "αθροισμένη.")
I("Και κοίτα μπροστά", "η προθεσμία επιστρέφει",
  "Μετά κοίτα μπροστά: τα τέλη και η ασφάλεια επιστρέφουν σε ημερομηνία, και "
  "το ίδιο νούμερο μαζί τους.")
I("Σύγκρινε με κάτι", "που ξέρεις",
  "Για να το νιώσεις, σύγκρινέ το με κάτι γνωστό. Με πόσους μήνες ενοίκιο, ή "
  "με πόσα χρόνια τελών.")
I("Και μπορεί να είναι μικρό", "κι αυτό απάντηση",
  "Μπορεί να βγει μικρό και να μη χρειάζεται να αλλάξει τίποτα. Είναι "
  "ολόκληρη απάντηση, και τώρα είναι μετρημένη αντί για υποτιθέμενη.")
I("Και δοκίμασε κάτι", "μία διαδρομή",
  "Δοκίμασε και κάτι πιο συγκεκριμένο: πάρε μία διαδρομή που κάνεις κάθε "
  "εβδομάδα και πολλαπλασίασε το κόστος του χιλιομέτρου με τα χιλιόμετρά της, "
  "επί πενήντα δύο.")
I("Εκείνο το νούμερο", "μιλάει πιο δυνατά",
  "Εκείνο το νούμερο μιλάει πιο δυνατά από το ετήσιο σύνολο, γιατί αφορά μία "
  "συνήθεια και όχι ολόκληρη τη ζωή σου.")
I("Το καλό", "η απόφαση επιστρέφει",
  "Το καλό είναι ότι η απόφαση επιστρέφει κάθε χρόνο, ολόκληρη. Μια κακή "
  "χρονιά δεν δεσμεύει την επόμενη.")

# -------------------------------------------------------------------- cap 8
T("Τι κάνεις σήμερα", "τρία βήματα",
  "Κλείνουμε με το τι μπορείς να κάνεις σήμερα, σε τρία βήματα.",
  cap="Τι κάνεις σήμερα")
L("Τρία βήματα",
  ["Πρόσθεσε τα ευρώ", "Βρες τα χιλιόμετρα", "Διαίρεσε"],
  "Πρώτο: πρόσθεσε ό,τι πλήρωσες σε δώδεκα μήνες. Δεύτερο: βρες τα χιλιόμετρα "
  "της ίδιας περιόδου. Τρίτο: διαίρεσε το ένα με το άλλο.")
I("Κάν' το μία φορά", "όχι κάθε μήνα",
  "Κάν' το μία φορά. Δεν είναι κάτι που κρατάς κάθε μήνα, είναι ένα νούμερο "
  "που το βρίσκεις και το κρατάς.")
I("Γράψε την ημερομηνία", "των τελών",
  "Γράψε δίπλα και την ημερομηνία των τελών. Αυτή η γραμμή είναι που κάνει το "
  "νούμερο χρήσιμο αντί για ενδιαφέρον.")
I("Και μην αλλάξεις τίποτα", "σήμερα",
  "Και μη βιαστείς να αλλάξεις κάτι σήμερα. Το να το ξέρεις είναι ολόκληρο το "
  "βήμα.")
# EXPERIMENTO 26: o pedido do longo tambem fecha em conta.
I("Και αν θέλεις ένα δεύτερο", "το κόστος της διαθεσιμότητας",
  "Αν θέλεις ένα δεύτερο νούμερο: πρόσθεσε μόνο τα σταθερά — ασφάλεια και "
  "τέλη — και διαίρεσέ τα με δώδεκα. Αυτό πληρώνεις κάθε μήνα ακόμη κι αν δεν "
  "βγάλεις το αυτοκίνητο από τη θέση του.")
I("Τα δύο μαζί", "λένε την ιστορία",
  "Τα δύο νούμερα μαζί λένε ολόκληρη την ιστορία: τι κοστίζει η χρήση και τι "
  "κοστίζει απλώς να το έχεις.")
C("Γράψε το νούμερό σου", "στα σχόλια",
  "Αν την κάνεις, γράψε από κάτω ένα μόνο πράγμα: το κόστος ανά χιλιόμετρο. "
  "Χωρίς μάρκα, χωρίς ποσά. Θέλω να δω πόσο διαφέρει μεταξύ ανθρώπων που "
  "οδηγούν παρόμοια.")

# =============================== O SHORT =====================================
# EXPERIMENTO 26, quinto braco — e o primeiro num canal que JA converte.
# Entrega a divisao FECHADA e gasta o pedido na INSCRICAO.

SHORT = [
    {"layout": "titulo", "kicker": "Το αυτοκίνητό σου",
     "sub": "πόσο ανά χιλιόμετρο;",
     "nar": "Πόσο σου κοστίζει κάθε χιλιόμετρο που κάνεις; Δύο νούμερα, και τα "
            "δύο τα έχεις ήδη.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Πρώτο", "sub": "όλα τα ευρώ του χρόνου",
     "nar": "Πρώτο: όλα όσα πλήρωσες σε δώδεκα μήνες. Καύσιμα, ασφάλεια, τέλη, "
            "σέρβις, λάστιχα.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Δεύτερο", "sub": "τα χιλιόμετρα",
     "nar": "Δεύτερο: τα χιλιόμετρα της ίδιας περιόδου, από τον χιλιομετρητή.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Διαίρεσε", "sub": "αυτό είναι το κόστος σου",
     "nar": "Διαίρεσε τα ευρώ με τα χιλιόμετρα. Αυτό κοστίζει κάθε χιλιόμετρο. "
            "Πολλαπλασίασέ το με μια διαδρομή που κάνεις συχνά και θα δεις τι "
            "πληρώνεις πραγματικά.", "sem_cap": True},
    {"layout": "cta", "kicker": "Αν σου φάνηκε χρήσιμο",
     "sub": "κάνε εγγραφή",
     "nar": "Αν σου φάνηκε χρήσιμο, κάνε εγγραφή. Μία πράξη την εβδομάδα, με "
            "τα δικά σου νούμερα.", "sem_cap": True},
]

THUMB = {"l1": "Πόσο κοστίζει", "l2": "το χιλιόμετρο"}

COPY = """# Το κόστος ανά χιλιόμετρο του δικού σου αυτοκινήτου, από τις δικές σου αποδείξεις

## TITULO
Πόσο Κοστίζει Πραγματικά το Χιλιόμετρό σου; Η Πράξη με τις Δικές σου Αποδείξεις

## DESCRICAO
Το αυτοκίνητό σου σου κοστίζει κάθε μήνα — λίγο εδώ, λίγο εκεί, ποτέ σε ένα νούμερο. Και γι' αυτό δεν το έχεις δει ποτέ ολόκληρο. Αυτό το βίντεο δεν λέει ότι το αυτοκίνητο είναι κακό· λέει πόσο κοστίζει το δικό σου, που είναι άλλο ερώτημα και πολύ πιο χρήσιμο. Έχει και προθεσμία που την ξέρεις: τα τέλη και η ανανέωση της ασφάλειας έχουν ημερομηνία.

Δεν υπάρχει ούτε ένα δικό μου νούμερο σε αυτό το βίντεο. Καμία τιμή καυσίμου, κανένα ποσό τελών, κανένα ασφάλιστρο, καμία μέση κατανάλωση, καμία μάρκα και κανένα μοντέλο. Όλα τα στοιχεία της πράξης βγαίνουν από τις αποδείξεις σου και από τον χιλιομετρητή σου.

Η πράξη είναι μία πρόσθεση και μία διαίρεση. Πρόσθεσε όλα όσα πλήρωσες για το αυτοκίνητο μέσα σε δώδεκα μήνες — όχι μόνο τα καύσιμα, αλλά και την ασφάλεια, τα τέλη, τον τεχνικό έλεγχο, το σέρβις, τα λάστιχα, τη στάθμευση και τα διόδια αν τα πληρώνεις τακτικά. Βρες τα χιλιόμετρα της ίδιας περιόδου από τον χιλιομετρητή, όχι από τη μνήμη. Διαίρεσε το ένα με το άλλο: αυτό κοστίζει κάθε χιλιόμετρο που κάνεις. Πολλαπλασίασέ το με μια διαδρομή που κάνεις συχνά και θα δεις το πραγματικό της κόστος.

Ένα κεφάλαιο δείχνει πού βρίσκεις τα νούμερα χωρίς να κρατάς αρχείο: οι κινήσεις της κάρτας δείχνουν τα πρατήρια, η ασφάλεια και τα τέλη είναι μία πληρωμή τον χρόνο η καθεμία, το συνεργείο κρατάει ιστορικό, και για τα χιλιόμετρα χρειάζεσαι δύο ενδείξεις — η παλιά είναι συχνά γραμμένη στο δελτίο του τεχνικού ελέγχου.

Ένα κεφάλαιο λέει τι ΔΕΝ πιάνει η πράξη, γιατί είναι πιο τίμιο από το να αποσιωπηθεί: την αξία που χάνει το αυτοκίνητο με τον χρόνο, τον χρόνο που σου γλιτώνει, και τις διαδρομές που απλώς δεν γίνονται αλλιώς. Η πράξη δεν κρίνει· δείχνει το μέγεθος ενός ποσού που δεν το έβλεπες ολόκληρο.

Και ένα κεφάλαιο για την περίπτωση που ξεγελάει: όποιος κάνει λίγα χιλιόμετρα βγάζει πολύ ακριβό χιλιόμετρο, επειδή τα σταθερά μοιράζονται σε λίγα — πληρώνει κυρίως για τη διαθεσιμότητα, που είναι θεμιτός λόγος αρκεί να ξέρεις πόσο κοστίζει.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Κάνε την πράξη και γράψε από κάτω ένα μόνο πράγμα: το κόστος ανά χιλιόμετρο. Χωρίς μάρκα, χωρίς ποσά, μόνο το νούμερο. Θέλω να δω πόσο διαφέρει μεταξύ ανθρώπων που οδηγούν παρόμοια.

## HASHTAGS
#ΠροσωπικάΟικονομικά #Αυτοκίνητο #ΕπόμενοΕπίπεδο

## TAGS
κοστος ανα χιλιομετρο, κοστος αυτοκινητου, τελη κυκλοφοριας, ασφαλεια αυτοκινητου, καυσιμα, σερβις αυτοκινητου, προσωπικα οικονομικα, οικογενειακος προυπολογισμος, ποσο κοστιζει το αυτοκινητο, χιλιομετρητης, εξοδα μεταφορας, υπολογισε μονος σου, μηνιαια εξοδα, διοδια, λαστιχα

## CONFIGURACOES DO STUDIO
- Idioma: Grego (el) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Grecia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita preco de combustivel, nao cita valor de tele kykloforias, nao cita premio de seguro, nao cita consumo medio, nao cita marca nem modelo e nao compara veiculos entre si. Todos os numeros da conta saem das aposdeixeis e do conta-quilometros do proprio espectador. Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa do carro, da regiao ou do ano dele. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA: qualquer preco de combustivel ou valor de taxa. Esses valores mudam por semana, por regiao e por cilindrada, e citar um so deles tornaria a conta errada para a maioria de quem assiste. O video tambem nao diz que ter carro e bom ou ruim — a resposta depende do numero de cada um —, nao recomenda vender nada, nao trata o transporte publico como se fosse sempre alternativa possivel, nao promete economia e nao e aconselhamento financeiro.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/epomeno-epipedo-013.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-013",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#12263A", "c1": "#2A9D8F", "c2": "#E8A33D", "bg": "#F5F2EC"},
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
    from ensaio import duracao_estimada, duracao_estimada_short
    grava(SPEC, "fabrica/specs/epomeno-epipedo-013.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
