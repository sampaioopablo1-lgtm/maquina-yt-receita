"""epomeno-epipedo-s013 — poe os teus juros em ordem, do mais caro.

ALAVANCA desta rodada, uma coisa so: a FORMA DO TITULO, e ela MUDA por canal.
Li o feed GR/26 nesta rodada (200, 15 itens, sem erro) e ele contradiz o que eu
ia fazer. Em grego a PERGUNTA e minoritaria — duas a tres de quinze, contra seis
de quinze no PL e cinco de quinze no BR. O que o GR/26 premia e **imperativo em
segunda pessoa** ("Δοκίμασε...", "Φάε...") e titulo puxado por nome de celebridade,
que nao me serve. Entao NAO estendo a forma de pergunta ao grego: este titula em
IMPERATIVO. A licao e maior que o titulo — eu estava a um passo de generalizar
uma forma medida em dois feeds para um terceiro que nao tinha lido.

O QUE DEU CERTO: `kolejny-poziom-s011`, a peca mais LONGA que esta maquina ja
publicou (43,37 s), esta em ~191 views as 2,8 h, confirmado em duas leituras. E
o `kolejny-poziom-s010` em ~183 as 4,9 h, confirmado em tres. Sao as duas
melhores curvas iniciais do lote novo, e as duas sao kolejny.

O QUE NAO DEU, e e sobre mim: reportei ao dono "epomeno-s011 de 8 para 88 as
2,6 h" com UMA leitura. A serie e 2, 8, 88, 11, 8, 11 — mediana ~10. O 88 era
outlier e eu o usei como prova de que a frota distribuia. Terceira vez em quatro
rodadas que leitura unica entra no relatorio. Testei e REFUTEI a hipotese de que
seria o token do canal: o mesmo video com o mesmo token deu 184 e 183, enquanto
uma leitura com token de outro canal deu 8. Nao e o token; e que uma leitura
qualquer pode errar por fator 23 para baixo e 9 para cima. Aprendizado 678.

NUMERO DE PARTIDA: 386 views do short do pacote de origem; ~178 do melhor solto
do canal as 5,9 h (duas leituras).

DE ONDE SAI: longo `alZ97hpgqXo` (epomeno-epipedo-005, os dois juros da mesma
banca), capitulo "Τέσσερις κινήσεις | με τα δικά σου νούμερα", SEGUNDO movimento:
escrever o juro de cada produto que se tem e ORDENAR do mais caro para o mais
barato — "αυτή η σειρά είναι όλη η στρατηγική". O short ORIGINAL do pacote faz o
contraste dos dois numeros e a distancia entre eles, e termina prometendo
exatamente este capitulo.

FAMILIA, regra (f): hoje no epomeno sairam "leia a linha no seu documento"
(s011) e "o numero medio nao e o seu" (s012). Esta e "voces esta otimizando o
lado errado do seu proprio balanco". Tres entradas erradas diferentes.

IDENTIDADE: faixa ATUAL do canal `{ink #12263A, c1 #2A9D8F, c2 #E8A33D,
bg #F5F2EC}`, trilha `Inspired` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO PERCENTUAL. Nao cita o juro da
# cataderna, nao cita o juro do cartao, nao cita o da aplicacao a prazo, nao cita
# a distancia entre eles e nao nomeia o banco central. Conferido A MAO campo por
# campo, porque o portao `narracao` conta QUANTIDADES por frase e NAO pega digito
# cru.
#
# A REGRA (g) MANDA, e aqui com forca: todos esses sao juros de boletim MENSAL.
# Um short com o numero deste mes fica errado no mes seguinte e continua no ar. E
# o mais importante: o argumento NAO PRECISA deles. "O euro que poes no saldo
# mais caro poupa-te o juro DESSE saldo, e o mesmo euro na cataderna rende o
# juro DELA" e verdadeiro qualquer que seja o par de numeros, e e o numero DO
# ESPECTADOR que decide — o mecanismo do 651.
#
# UNICO NUMERAL NA NARRACAO: "τέσσερις κινήσεις", que e o nome do capitulo do
# longo, nao afirmacao sobre o mundo.
#
# O QUE O VIDEO AFIRMA: que o juro cobrado no cartao e multiplo do pago na
# cataderna na mesma banca; que por isso um euro aplicado ao saldo mais caro
# poupa mais do que o mesmo euro rende numa cataderna; e que a ordenacao dos
# proprios juros, do mais caro ao mais barato, e a estrategia inteira. Esta no
# longo epomeno-epipedo-005 (`alZ97hpgqXo`), capitulos "Δύο νούμερα" e
# "Τέσσερις κινήσεις".
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) todos os percentuais — sao de boletim mensal e envelhecem a peca;
#   (2) a razao entre os dois juros, que muda com eles;
#   (3) a aplicacao a prazo e o aviso sobre o fundo de emergencia, que estao no
#       longo e sao OUTRA decisao — nao se empilham num short de uma conta so.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Ψάχνεις καλύτερο επιτόκιο", "sub": "στη λάθος πλευρά",
     "nar": "Ψάχνεις καλύτερο επιτόκιο για τις καταθέσεις σου, και την ίδια στιγμή "
            "κουβαλάς υπόλοιπο στην κάρτα.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Δύο νούμερα", "sub": "ίδια τράπεζα",
     "nar": "Είναι δύο νούμερα από την ίδια τράπεζα, τον ίδιο μήνα, και αυτό που "
            "σου χρεώνουν είναι πολλαπλάσιο από αυτό που σου δίνουν.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Το ίδιο ευρώ", "sub": "δύο αποτελέσματα",
     "nar": "Το ευρώ που ρίχνεις στο ακριβότερο υπόλοιπο σου γλιτώνει το επιτόκιο "
            "εκείνου. Το ίδιο ευρώ στην κατάθεση κερδίζει μόνο το δικό της.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Βάλ' τα σε σειρά", "sub": "από το ακριβότερο",
     "nar": "Γράψε σε ένα χαρτί το επιτόκιο κάθε προϊόντος που έχεις και βάλ' τα "
            "σε σειρά, από το ακριβότερο. Αυτή η σειρά είναι όλη η στρατηγική.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Κάνε εγγραφή", "sub": "για τα επόμενα",
     "nar": "Δεν είναι επένδυση με ρίσκο, είναι αριθμητική. Κάνε εγγραφή για τα "
            "επόμενα, και οι τέσσερις κινήσεις είναι στο βίντεο.",
     "sem_cap": True},
]

THUMB = {"l1": "Βάλε σε σειρά", "l2": "τα δικά σου"}

COPY = """# epomeno-epipedo-s013

## TITULO
Βάλε τα Επιτόκιά σου σε Σειρά: Η Μία Κίνηση που Αποφασίζει Πού Πάει το Επόμενο Ευρώ

## TITULO SHORT
Βάλε τα επιτόκιά σου σε σειρά

## DESCRICAO
Η πιο συχνή κίνηση όταν κάποιος αποφασίζει να ασχοληθεί με τα οικονομικά του είναι να ψάξει καλύτερο επιτόκιο για τα λεφτά που έχει στην άκρη. Είναι λογική κίνηση και είναι, συνήθως, η λιγότερο αποδοτική από όσες έχει διαθέσιμες — γιατί γίνεται στη μία πλευρά του ισολογισμού του, ενώ το μεγάλο νούμερο κάθεται στην άλλη.

Στην ίδια τράπεζα, τον ίδιο μήνα, υπάρχουν δύο επιτόκια που σε αφορούν: αυτό που σου δίνουν για τα χρήματά σου και αυτό που σου χρεώνουν για τα χρήματα που χρωστάς. Το δεύτερο είναι πολλαπλάσιο του πρώτου, και αυτό δεν είναι ανωμαλία ούτε αδικία — είναι ο τρόπος που δουλεύει το προϊόν. Το χρήσιμο δεν είναι να διαμαρτυρηθείς γι' αυτό, είναι να το χρησιμοποιήσεις στη σειρά των αποφάσεών σου.

Από εκεί βγαίνει η αριθμητική, και δεν χρειάζεται να πιστέψεις τίποτα για να τη δεις. Ένα ευρώ που ρίχνεις στο ακριβότερο υπόλοιπο που έχεις σου γλιτώνει, μέσα σε έναν χρόνο, το επιτόκιο εκείνου του υπολοίπου. Το ίδιο ευρώ, βαλμένο σε κατάθεση, κερδίζει το επιτόκιο της κατάθεσης. Δεν είναι επένδυση με ρίσκο και προοπτική· είναι σύγκριση δύο αριθμών που και οι δύο είναι γραμμένοι στα δικά σου χαρτιά.

Η κίνηση, λοιπόν, είναι μία και παίρνει λίγα λεπτά. Γράψε σε ένα χαρτί κάθε προϊόν που έχεις — κάρτα, δάνειο, κατάθεση — και δίπλα του το επιτόκιό του. Δεν χρειάζεται να τα αναζητήσεις πουθενά: είναι στο μηνιαίο εκκαθαριστικό της κάρτας και στη σύμβαση του δανείου. Μετά βάλ' τα σε σειρά, από το ακριβότερο στο φθηνότερο. Αυτή η σειρά είναι όλη η στρατηγική: το επόμενο ευρώ που περισσεύει πηγαίνει στην πρώτη γραμμή.

Δεν γράφω εδώ κανένα ποσοστό, και είναι σκόπιμο: τα επιτόκια αλλάζουν κάθε μήνα, η σειρά όχι — και τα νούμερα που αποφασίζουν είναι τα δικά σου, όχι τα μέσα. Οι τέσσερις κινήσεις ολόκληρες, τι ΔΕΝ πηγαίνει σε προθεσμιακή, γιατί το απόθεμα για τα απρόοπτα μένει έξω, και τα τέσσερα λάθη που ακυρώνουν τη δουλειά — είναι στο πλήρες βίντεο.

## COMENTARIO FIXADO
Η κίνηση σε τρία βήματα, για όποιον θέλει να το κάνει τώρα: ΕΝΑ, γράψε κάθε προϊόν που έχεις και δίπλα το επιτόκιό του — είναι στο εκκαθαριστικό της κάρτας και στη σύμβαση του δανείου, δεν χρειάζεται να ρωτήσεις κανέναν. ΔΥΟ, βάλ' τα σε σειρά από το ακριβότερο. ΤΡΙΑ, το επόμενο ευρώ που περισσεύει πάει στην πρώτη γραμμή. Το λάθος που κάνουν οι περισσότεροι δεν είναι λάθος λογαριασμού, είναι λάθος ΠΛΕΥΡΑΣ: ψάχνουν δέκατα στην κατάθεση ενώ το ακριβό νούμερο τρέχει στην κάρτα. Όποιος φτιάξει τη λίστα, ας γράψει στα σχόλια μόνο ποιο προϊόν βγήκε πρώτο — χωρίς ποσοστά και χωρίς ποσά.

## HASHTAGS
#Επιτόκια #ΠιστωτικήΚάρτα #ΕπόμενοΕπίπεδο

## TAGS
επιτοκια, πιστωτικη καρτα, καταθεση, εξοφληση καρτας, σειρα προτεραιοτητας, προσωπικα οικονομικα, ελλαδα, εκκαθαριστικο καρτας, συμβαση δανειου, αριθμητικη, πως να, υπολοιπο, επομενο επιπεδο, νοικοκυριο, αποφαση

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO PERCENTUAL. Nao cita juro de cataderna,
de cartao nem de aplicacao a prazo, nao cita a distancia entre eles e nao nomeia
o banco central. Conferido a mao campo por campo.

A REGRA (g) MANDA, e com forca: todos esses sao juros de boletim MENSAL, e um
short com o numero deste mes fica errado no mes seguinte e continua no ar. E o
argumento NAO PRECISA deles: "o euro que poes no saldo mais caro poupa-te o juro
DESSE saldo, e o mesmo euro na cataderna rende o juro DELA" e verdadeiro
qualquer que seja o par, e quem decide e o numero DO ESPECTADOR.

UNICO NUMERAL NA NARRACAO: "τέσσερις κινήσεις", nome do capitulo do longo.

O QUE O VIDEO AFIRMA: que o juro cobrado no cartao e multiplo do pago na
cataderna na mesma banca; que por isso um euro aplicado ao saldo mais caro poupa
mais do que o mesmo euro rende numa cataderna; e que a ordenacao dos proprios
juros, do mais caro ao mais barato, e a estrategia inteira. Esta no longo
epomeno-epipedo-005 (alZ97hpgqXo), capitulos "Δύο νούμερα" e "Τέσσερις κινήσεις".

DESCARTADO, e vai escrito:
  (1) todos os percentuais — boletim mensal, envelhecem a peca;
  (2) a razao entre os dois juros, que muda com eles;
  (3) a aplicacao a prazo e o aviso sobre o fundo de emergencia, que sao OUTRA
      decisao e nao se empilham num short de uma conta so.

## FONTES
O longo de onde este short foi extraido (epomeno-epipedo-005, alZ97hpgqXo) traz
as fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s013",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#12263A", "c1": "#2A9D8F", "c2": "#E8A33D",
               "bg": "#F5F2EC"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "alZ97hpgqXo",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short, alvo_short
    grava(SPEC, "fabrica/specs/epomeno-epipedo-s013.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    INTERROGA = ("?", ";", ";")
    forma = ("pergunta" if tit.rstrip().endswith(INTERROGA) else "imperativo/afirmacao")
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} (uso o TOPO: voz el puxa -)")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto (el) "
          f"{s*0.958:.1f} a {s*0.997:.1f}")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars) | forma: {forma}")
    print(f"aponta para: {SPEC['longo_existente']}")
