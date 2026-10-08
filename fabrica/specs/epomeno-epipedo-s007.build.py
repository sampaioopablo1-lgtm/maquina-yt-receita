"""epomeno-epipedo-s007 — descobri que o estoque de origem nunca esteve zerado.

ALAVANCA: A (alcance por short). Decimo sexto short solto, setimo do epomeno.

O QUE DEU CERTO: a regra do 650 (mediana, nao ultima leitura) e as coletas
horarias ja acumuladas deram, juntas, o achado de metodo mais util do dia.
TRAJETORIA INICIAL dos quatro ultimos soltos do epomeno, por hora de vida:
  s004  0,4h=0   1,4h=1   2,4h=2    3,4h=58   4,4h=141
  s005  0,9h=8   1,9h=8   2,9h=130  3,9h=211
  s003  1,2h=2   1,8h=2   2,8h=2    3,8h=2
  s006  0,8h=1   1,8h=0   2,8h=1
Nos dois primeiros o contador fica em UM DIGITO por duas a tres horas e SALTA
para 58-130 em uma hora. E o lote semeado do 629 visivel no contador: a peca sai
do lote ou nao sai. E o degrau PREVE — o s003, que nao saltou ate 3,8 h, terminou
em 132, o pior dos tres maduros. Aprendizado 653. Da para ler destino em ~4 h
perguntando SE o degrau aconteceu, em vez de esperar 20 h. LIMITES: n=4, um canal,
e a hora do degrau varia (1,9 a 3,4 h) — o s006 com um digito as 2,8 h NAO esta
reprovado.

O QUE NAO DEU, e e o maior erro meu desta sequencia: o "ESTOQUE DE ORIGEM ZERO"
do epomeno estava ERRADO. O canal tem DEZOITO longos com id. Os cinco que eu
tratava como "os usados" sao os dos pacotes 013 a 017, os MAIS RECENTES. Os
pacotes 002 a 012, mais dois longos sem pacote, estao INTOCADOS: ONZE a TREZE
livres, nao zero. Aprendizado 652.
E CUSTOU QUALIDADE, nao so ritmo: os DOIS melhores shorts da frota inteira saem
de longos que eu nunca usei — `481Zgd4IhsE` (002) com 1.614 e `9Hg5A3H1Qe4` (003)
com 1.407, os dois ACIMA do md5oLwZqXew (1.155) que eu vinha chamando de melhor
da frota. Durante varias rodadas fiz segundo e TERCEIRO angulo do mesmo longo
dizendo que nao havia alternativa, e havia onze longos virgens.
A ASSINATURA DO ERRO e a de sempre: eu enumerei os longos a partir dos pacotes
RECENTES, e esse metodo produz "estoque zero" quando o livre esta nos ANTIGOS.
Decimo defeito com essa assinatura. A regra nova: estoque se mede com UMA consulta
sobre TODOS os longos do canal, nunca de memoria.

O QUE VOU MUDAR, e e uma coisa so: este short sai do `481Zgd4IhsE`, o longo de
MAIOR alcance que a frota tem, e virgem como origem de solto.
NUMERO DE PARTIDA: 1.614 do short original daquele pacote; mediana da rajada do
canal entre 263 e 1.155.

DE ONDE SAI: o short original do 002 ensina o paradoxo (sete em dez tem casa
propria e nao se acha aluguel) e cita a devolucao de um aluguel por ano. Este
ataca coisa diferente e puramente ARITMETICA, do capitulo "Τι σημαινει για σενα":
a devolucao tem TETO, e teto e valor FIXO, nao percentual — logo ela cobre uma
fatia MAIOR de um aluguel barato do que de um caro, e quem compara dois alugueis
pelo valor mensal compara o numero errado. Nenhum valor e dito.

IDENTIDADE: usei a FAIXA do canal — `{ink #12263A, c1 #2A9D8F, c2 #E8A33D,
bg #F5F2EC}`, trilha `Inspired`, voz `el-GR-NestorasNeural`. O 002 usa paleta
antiga `{#1A1A1A, #2E86AB, #E4572E, #F4F7F9}` e eu NAO a copiei, mesmo sendo dele
que vem a pauta — o 601 manda comparar com a faixa historica, nao com o pacote de
origem. Mesma decisao que no labtreinamento-s003.

TENDENCIA: o feed GR/26 NAO foi lido nesta rodada, e digo em vez de inventar. Do
PL/26 lido as 06:22 ficou a FORMA: pergunta ou imperativo em segunda pessoa. Cena
1 pergunta, cena 5 imperativo.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO. NAO cita o valor do teto da devolucao, NAO cita
# aluguel, NAO cita percentual, NAO cita data e NAO nomeia orgao. Os unicos
# numeros ditos sao "dois" e "uma", e sao a aritmetica da comparacao.
#
# O QUE O VIDEO AFIRMA: que a devolucao de aluguel tem um teto, que teto e valor
# fixo e nao percentual, e que por isso ela cobre fatia maior de um aluguel
# barato do que de um caro. A primeira parte esta no longo `481Zgd4IhsE`
# (epomeno-002) com as fontes; a segunda e aritmetica.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) o VALOR do teto e quem tem direito — esta no longo com fonte, e NAO foi
#       reconferido hoje em duas fontes;
#   (2) qualquer aluguel, percentual ou data de pedido;
#   (3) se vale mudar de casa por causa disso — nao e o que a conta decide.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Συγκρίνεις ενοίκια;", "sub": "λάθος αριθμός",
     "nar": "Συγκρίνεις δύο ενοίκια με το μηνιαίο ποσό; Αυτός ο αριθμός δεν "
            "είναι ο τελικός.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Κάτι επιστρέφεται", "sub": "μία φορά τον χρόνο",
     "nar": "Ένα μέρος του ενοικίου επιστρέφεται μία φορά τον χρόνο, και έχει "
            "ανώτατο όριο.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Το όριο", "sub": "δεν μεγαλώνει μαζί",
     "nar": "Το όριο δεν μεγαλώνει μαζί με το ενοίκιο, όσο ακριβό κι αν είναι. "
            "Είναι σταθερό ποσό, όχι ποσοστό.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Άρα μετράει", "sub": "πιο πολύ στο φθηνό",
     "nar": "Άρα η επιστροφή καλύπτει μεγαλύτερο μέρος σε φθηνό ενοίκιο παρά σε "
            "ακριβό.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Σύγκρινε τη χρονιά", "sub": "μετά την επιστροφή",
     "nar": "Σύγκρινε λοιπόν τη χρονιά μετά την επιστροφή, για το ένα και για "
            "το άλλο. Η πλήρης πράξη είναι στο βίντεο.",
     "sem_cap": True},
]

THUMB = {"l1": "Σύγκρινε", "l2": "τη χρονιά"}

COPY = """# epomeno-epipedo-s007

## TITULO
Η Επιστροφή Ενοικίου Έχει Οροφή: Γιατί Μετράει Πιο Πολύ σε Φθηνό Σπίτι

## TITULO SHORT
Σύγκρινε τη χρονιά, όχι τον μήνα

## DESCRICAO
Όταν διαλέγεις ανάμεσα σε δύο σπίτια, ο αριθμός που κοιτάς σχεδόν πάντα είναι το μηνιαίο ενοίκιο. Είναι ο πιο εύκολος αριθμός και είναι ο λάθος αριθμός, γιατί δεν είναι αυτό που τελικά φεύγει από την τσέπη σου μέσα στη χρονιά.

Ένα μέρος του ενοικίου επιστρέφεται, μία φορά τον χρόνο — και εδώ είναι το σημείο που αλλάζει τη σύγκριση: η επιστροφή έχει ΟΡΟΦΗ. Οροφή σημαίνει σταθερό ποσό, όχι ποσοστό. Δεν μεγαλώνει μαζί με το ενοίκιο. Οπότε το ίδιο ποσό που επιστρέφεται καλύπτει μεγαλύτερο κομμάτι ενός φθηνού ενοικίου και μικρότερο κομμάτι ενός ακριβού.

Η συνέπεια είναι πρακτική και δεν είναι προφανής: δύο σπίτια που φαίνονται να απέχουν ένα συγκεκριμένο ποσό τον μήνα, απέχουν ΑΛΛΟ ποσό μέσα στη χρονιά, και η διαφορά μετά την επιστροφή είναι πάντα μεγαλύτερη από τη διαφορά πριν — γιατί το φθηνό κερδίζει αναλογικά περισσότερο από το ίδιο όφελος. Αν η σύγκρισή σου ήταν στο όριο, αυτό μπορεί να την γυρίσει.

Η σωστή είσοδος είναι η ΧΡΟΝΙΑ, όχι ο μήνας: πόσο πληρώνεις σε δώδεκα μήνες, μείον ό,τι επιστρέφεται, για το ένα σπίτι και για το άλλο. Δύο αριθμοί, μία αφαίρεση, και η απόφαση γίνεται πάνω σε κάτι που υπάρχει.

Δεν υπάρχει εδώ ούτε ποσό οροφής, ούτε ενοίκιο, ούτε ποσοστό, ούτε ημερομηνία: οι αριθμοί που αποφασίζουν είναι στο μισθωτήριό σου. Πόσο είναι η οροφή, ποιος έχει δικαίωμα, τι χαρτιά θέλει και πού αλλιώς πιάνει — είναι στο βίντεο.

## COMENTARIO FIXADO
Το κλειδί είναι ότι η επιστροφή έχει ΟΡΟΦΗ, δηλαδή σταθερό ποσό και όχι ποσοστό: δεν μεγαλώνει μαζί με το ενοίκιο. Άρα καλύπτει μεγαλύτερο κομμάτι σε φθηνό σπίτι και μικρότερο σε ακριβό, και η διαφορά δύο σπιτιών ΜΕΤΑ την επιστροφή είναι πάντα μεγαλύτερη από τη διαφορά πριν. Μη συγκρίνεις μηνιαία ενοίκια: υπολόγισε τη χρονιά — δώδεκα μήνες μείον ό,τι επιστρέφεται — για το ένα και για το άλλο. Αν η σύγκριση ήταν στο όριο, αυτό την γυρίζει. Πόσο είναι η οροφή και ποιος έχει δικαίωμα δεν τα βάζω εδώ: είναι στο βίντεο με τις πηγές. Αν το υπολογίσεις, γράψε μόνο αν η απόφαση άλλαξε ή όχι — χωρίς ποσά.

## HASHTAGS
#Ενοίκιο #Σπίτι #ΕπόμενοΕπίπεδο

## TAGS
ενοικιο, επιστροφη ενοικιου, οροφη, μισθωτηριο, συγκριση σπιτιων, προσωπικα οικονομικα, ελλαδα, υπολογισμος, χρονια, μηνιαιο ενοικιο, φθηνο ενοικιο, κατοικια, επομενο επιπεδο, νοικι, προυπολογισμος

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
ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita o valor do teto da devolucao, nao cita
aluguel, nao cita percentual, nao cita data e nao nomeia orgao. Os unicos numeros
ditos sao "dois" e "uma", e sao a aritmetica da comparacao.

O QUE O VIDEO AFIRMA: que a devolucao de aluguel tem um teto, que teto e valor
fixo e nao percentual, e que por isso ela cobre fatia maior de um aluguel barato
do que de um caro. A primeira parte esta no longo epomeno-epipedo-002
(481Zgd4IhsE) com as fontes; a segunda e aritmetica.

DESCARTADO, e vai escrito:
  (1) o VALOR do teto e quem tem direito — esta no longo com fonte, e NAO foi
      reconferido hoje em duas fontes;
  (2) qualquer aluguel, percentual ou data de pedido;
  (3) se vale mudar de casa por causa disso — nao e o que a conta decide.

## FONTES
O longo de onde este short foi extraido (epomeno-epipedo-002, 481Zgd4IhsE) traz
as fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s007",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#12263A", "c1": "#2A9D8F", "c2": "#E8A33D",
               "bg": "#F5F2EC"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "481Zgd4IhsE",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/epomeno-epipedo-s007.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, piso 30s, mira 33-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
