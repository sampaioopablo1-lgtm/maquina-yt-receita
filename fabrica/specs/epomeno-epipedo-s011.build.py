"""epomeno-epipedo-s011 — a diferenca pessoal esta ESCRITA no teu extrato.

ALAVANCA DESTA RODADA: **conversao em inscrito, nao alcance.** Primeira vez que
tenho o DENOMINADOR. Medido nesta rodada, com o cliente OAuth certo por canal
(667): labtreinamento 67 subs / 10.673 views, epomeno 16 / 10.988,
kolejny 8 / 7.494.

O 6,3 por mil do labtreinamento parece conversao 4x melhor e NAO E: o canal
reporta 71 videos e o banco tem 33 da maquina, logo 38 sao anteriores e trazem
plateia pre-existente. **O instrumento produziu o achado e eu o descarto.** A
comparacao limpa e epomeno (43 no canal / 43 da maquina) contra kolejny (55/57),
os dois iniciados em 11/08: **1,5 e 1,1 inscrito por 1.000 views** (668).

Consequencia aritmetica, e e dura: a 1,3 por mil, 500 inscritos pedem ~385.000
views POR CANAL. A frota faz ~2.300 views/dia. **Mais view nao resolve.** O que
resolve, se resolver, e converter melhor a view que ja existe.

O QUE VOU MUDAR, uma coisa so: o CTA do short gasta o unico pedido que tem
apontando para o LONGO (493) e **nunca pediu inscricao**. Faz sentido para as
4.000 h; nao faz para o portao de inscritos, que e o mais distante (8 e 16, nao
400). Aqui o kicker do CTA pede a inscricao e a DESCRICAO mantem o caminho para
o longo, para nao trocar um portao pelo outro. Experimento 37.

FRAQUEZA DECLARADA DO EXPERIMENTO 37: sem `yt-analytics.readonly` eu NAO meco
inscrito por peca, so por canal. Entao o sinal e inscrito/1.000 views do CANAL
ao longo de dias, com todas as outras pecas dentro — e nao vou poder atribuir um
salto a esta peca. Se o dono liberar o escopo, isso passa a ser mensuravel por
video e o experimento fecha em horas em vez de semanas.

NUMERO DE PARTIDA: 600 views do short do pacote de origem (o melhor da lista
livre do canal); 415 as 6,6 h do melhor solto de hoje, epomeno-s009.

DE ONDE SAI: longo `TJZcjE-uv8E` (epomeno-epipedo-007, a aumento das
aposentadorias), capitulo "Το εκκαθαριστικό — εκεί είναι γραμμένο". O short
original do pacote NAO faz esse capitulo: ele explica a diferenca pessoal e
termina dizendo "onde achar no teu extrato esta no video completo". Esta peca faz
a acao que aquele prometeu — achar a linha e comparar dois meses.

IDENTIDADE: faixa ATUAL do canal `{ink #12263A, c1 #2A9D8F, c2 #E8A33D,
bg #F5F2EC}`, trilha `Inspired`. O pacote 007 nao dita a paleta (601).

TENDENCIA: o feed GR/26 NAO foi lido nesta rodada, e digo em vez de inventar.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita o percentual do aumento, nao cita o
# ano em que o mecanismo termina, nao cita quantas pessoas estao em cada lado,
# nao cita valor e nao nomeia orgao. Conferido A MAO campo por campo, porque o
# portao `narracao` conta QUANTIDADES por frase e NAO pega digito cru.
#
# UNICO NUMERAL NA NARRACAO: "δύο διαδοχικούς μήνες" (dois meses seguidos). E
# INSTRUCAO DE PROCEDIMENTO, nao afirmacao sobre o mundo — e quantos extratos o
# espectador precisa por lado a lado para ver o acerto. Uma quantidade na frase,
# limite do portao e tres.
#
# O QUE O VIDEO AFIRMA: que a diferenca pessoal aparece como LINHA NOMEADA no
# extrato da aposentadoria; que a ausencia dessa linha significa ter recebido o
# aumento inteiro; e que comparar dois meses seguidos mostra o que foi acertado.
# Esta no longo epomeno-epipedo-007 (`TJZcjE-uv8E`), capitulos
# "Το εκκαθαριστικό — εκεί είναι γραμμένο" e "Η προσωπική διαφορά".
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) o percentual do aumento do ano e o ano de fim do mecanismo — estao no
#       longo com fonte, e mudam por decisao de politica;
#   (2) quantos aposentados estao em cada lado da linha — numero do longo, e
#       nao foi reconferido nesta rodada em duas fontes;
#   (3) quanto o espectador vai receber, que depende do extrato dele.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Η αύξηση ανακοινώθηκε", "sub": "έφτασε σε εσένα;",
     "nar": "Ξέρεις ότι η σύνταξη αυξήθηκε, αλλά όχι αν η αύξηση έφτασε ολόκληρη "
            "σε εσένα.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Δεν το μαντεύεις", "sub": "είναι γραμμένο",
     "nar": "Δεν το μαντεύεις. Είναι γραμμένο, με το όνομά του, στο εκκαθαριστικό "
            "της σύνταξης.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Ψάξε τη γραμμή", "sub": "προσωπική διαφορά",
     "nar": "Μπες στο εκκαθαριστικό και ψάξε τη γραμμή της προσωπικής διαφοράς. "
            "Αν δεν υπάρχει καθόλου, την πήρες ολόκληρη.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Αν υπάρχει", "sub": "βάλε τους δίπλα δίπλα",
     "nar": "Αν υπάρχει, κατέβασε δύο διαδοχικούς μήνες και βάλε τους δίπλα δίπλα. "
            "Η γραμμή που κουνήθηκε σου λέει τι συμψηφίστηκε.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Κάνε εγγραφή", "sub": "για τα επόμενα",
     "nar": "Κάνε το στο δικό σου χαρτί. Κάνε εγγραφή για τα επόμενα, και η πλήρης "
            "διαδρομή είναι στο βίντεο.",
     "sem_cap": True},
]

THUMB = {"l1": "Είναι γραμμένο", "l2": "στο εκκαθαριστικό"}

COPY = """# epomeno-epipedo-s011

## TITULO
Προσωπική Διαφορά: Πώς Βλέπεις στο Εκκαθαριστικό αν Πήρες Ολόκληρη την Αύξηση

## TITULO SHORT
Βρες τη γραμμή: πήρες ολόκληρη την αύξηση;

## DESCRICAO
Η αύξηση ανακοινώνεται μία φορά και είναι ίδια για όλους. Το ποσό που φτάνει στον καθένα δεν είναι. Και η διαφορά δεν είναι εικασία ούτε θέμα τύχης: είναι γραμμένη, με το όνομά της, σε ένα χαρτί που μπορείς να κατεβάσεις μόνος σου.

Το χαρτί είναι το εκκαθαριστικό της σύνταξης, και η γραμμή που ψάχνεις είναι η προσωπική διαφορά. Από εκεί η διαδρομή είναι απλή και δεν χρειάζεται κανένα νούμερο από έξω. Πρώτο ενδεχόμενο: η γραμμή δεν υπάρχει καθόλου. Τότε δεν υπάρχει τίποτα να συμψηφιστεί και η αύξηση έφτασε σε εσένα ολόκληρη. Δεύτερο ενδεχόμενο: η γραμμή υπάρχει. Τότε ένα μέρος της αύξησης πηγαίνει να μειώσει αυτή τη γραμμή και δεν το βλέπεις στο ποσό που εισπράττεις.

Για να το δεις με τα δικά σου μάτια και όχι σε παράδειγμα, κατέβασε δύο διαδοχικούς μήνες και βάλε τους δίπλα δίπλα. Κοίτα τι έκανε η γραμμή της προσωπικής διαφοράς από τον έναν μήνα στον άλλον, και κοίτα τι έκανε το τελικό πληρωτέο. Η σύγκριση των δύο σελίδων σου δείχνει ακριβώς τι συμψηφίστηκε — κάτι που κανένα γενικό άρθρο δεν μπορεί να σου πει, γιατί το νούμερο που αποφασίζει είναι στο δικό σου χαρτί.

Μια προσοχή, γιατί είναι η πιο συχνή παρεξήγηση: η προσωπική διαφορά δεν είναι ποινή και δεν είναι λάθος της υπηρεσίας. Είναι μια γέφυρα από παλαιότερο καθεστώς υπολογισμού, και ο μηχανισμός που τη μειώνει είναι ο λόγος που δύο συνταξιούχοι με την ίδια ανακοινωμένη αύξηση βλέπουν άλλο ποσό στον λογαριασμό τους.

Εδώ δεν υπάρχει ποσοστό, ούτε έτος, ούτε πλήθος δικαιούχων: αυτά είναι στο πλήρες βίντεο, μαζί με το πώς βγαίνει το ποσοστό κάθε χρόνο, τι αλλάζει όταν ο μηχανισμός ολοκληρωθεί, πού ακριβώς πατάς για να βρεις το χαρτί και τα τέσσερα λάθη που κάνουν οι περισσότεροι όταν το διαβάζουν.

## COMENTARIO FIXADO
Η διαδρομή με δύο ενδεχόμενα, για να μην τη χάσει κανείς: κατεβάζεις το εκκαθαριστικό, ψάχνεις τη γραμμή «προσωπική διαφορά». ΔΕΝ υπάρχει η γραμμή; Πήρες την αύξηση ολόκληρη. ΥΠΑΡΧΕΙ η γραμμή; Μέρος της αύξησης πήγε να τη μειώσει. Και το κρίσιμο: βάλε δύο διαδοχικούς μήνες δίπλα δίπλα — η κίνηση της γραμμής είναι η απόδειξη, όχι η εξήγηση κανενός. Αν βρήκες τη γραμμή, γράψε στα σχόλια μόνο αν υπήρχε ή όχι, χωρίς ποσά.

## HASHTAGS
#Σύνταξη #ΠροσωπικήΔιαφορά #ΕπόμενοΕπίπεδο

## TAGS
προσωπικη διαφορα, εκκαθαριστικο συνταξης, αυξηση συνταξεων, κυριες συνταξεις, συμψηφισμος, συνταξιουχοι, ελλαδα, πως το βρισκω, εκκαθαριστικο, συνταξη, προσωπικα οικονομικα, επομενο επιπεδο, πληρωτεο, ελεγχος συνταξης, δυο μηνες

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
ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita o percentual do aumento, nao cita o ano
de fim do mecanismo, nao cita quantas pessoas estao em cada lado, nao cita valor
e nao nomeia orgao. Conferido a mao campo por campo.

UNICO NUMERAL NA NARRACAO: "δύο διαδοχικούς μήνες". E instrucao de
procedimento — quantos extratos por lado a lado — nao afirmacao sobre o mundo.

O QUE O VIDEO AFIRMA: que a diferenca pessoal aparece como linha nomeada no
extrato da aposentadoria; que a ausencia dessa linha significa ter recebido o
aumento inteiro; e que comparar dois meses seguidos mostra o que foi acertado.
Esta no longo epomeno-epipedo-007 (TJZcjE-uv8E), capitulos
"Το εκκαθαριστικό — εκεί είναι γραμμένο" e "Η προσωπική διαφορά".

DESCARTADO, e vai escrito:
  (1) o percentual do aumento e o ano de fim do mecanismo — estao no longo com
      fonte, e mudam por decisao de politica;
  (2) quantos aposentados estao em cada lado da linha — numero do longo, nao
      reconferido nesta rodada em duas fontes;
  (3) quanto o espectador vai receber, que depende do extrato dele.

## FONTES
O longo de onde este short foi extraido (epomeno-epipedo-007, TJZcjE-uv8E) traz
as fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s011",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#12263A", "c1": "#2A9D8F", "c2": "#E8A33D",
               "bg": "#F5F2EC"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "TJZcjE-uv8E",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/epomeno-epipedo-s011.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, piso 30s, mira 35-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
