"""epomeno-epipedo-s010 — a desconto cai na LINHA da energia, nao na pagina.

ALAVANCA: A (alcance por short). Decimo short solto do epomeno.

O QUE DEU CERTO: as duas pecas escolhidas pelo PERFIL do 651 sao as duas
melhores curvas iniciais da frota hoje — epomeno-s009 com 326 as 4,9 h e
kolejny-s009 com 344 as 3,9 h. Ambas tem tambem as 15 tags repostas a mao, e por
isso o experimento 36 existe com a fraqueza declarada: nao da para separar pauta
de tag nessas duas.

O QUE NAO DEU, e e grave: **sao TRES pecas mortas hoje, nao duas.** Conferindo
`part=status,contentDetails` em TODAS as pecas do dia, a `kolejny-poziom-s007`
(`ylsKfJ5Kv4s`, 8,8 h) tambem esta `uploaded`/`P0D` com zero view — eu a vinha
contando como zero normal. E o padrao e TEMPORAL: as tres foram publicadas em
sequencia, entre 10:18 e 13:22, atravessam DOIS canais, e as SETE publicadas de
14:28 em diante processaram todas normalmente, nos tres canais. Isso aponta falha
transitoria do lado do YouTube naquela janela, nao defeito da fabrica — mas
**retrata a minha afirmacao das 20:16 de que os 7/dia foram entregues nos tres
canais.** O numero REAL, contando so peca `processed`: epomeno 5, kolejny 6,
labtreinamento 7. Dezoito, nao vinte e um. Aprendizado 666.

O QUE VOU MUDAR, e e consequencia direta: esta peca existe para levar o epomeno
de 5 para 6 pecas VIVAS, nao para passar de sete. Publicar agora tambem testa se
a janela de falha fechou — a decima peca seguida processada seria a confirmacao.
NUMERO DE PARTIDA: 301 do short do pacote de origem; 326 do melhor solto do canal
hoje, as 4,9 h.

DE ONDE SAI: longo `P2q6w9y7j88` (epomeno-epipedo-004, a conta de luz), capitulo
"Το φύλλο τεσσάρων γραμμών", que o short original NAO usa — ele mostra a faixa
do que nao e energia e para ali. A entrada errada atacada aqui vem DEPOIS dessa:
receber a promessa de desconto e aplica-la ao TOTAL da pagina. O desconto cai so
na linha da energia, logo a conta certa e aplicar na linha e so depois olhar a
diferenca no total — e o mesmo percentual rende diferente em cada conta, porque a
energia nao pesa igual em todas.

IDENTIDADE: faixa ATUAL do canal `{ink #12263A, c1 #2A9D8F, c2 #E8A33D,
bg #F5F2EC}`, trilha `Inspired`. O pacote 004 e antigo e nao ditou a paleta (601).

TENDENCIA: o feed GR/26 NAO foi lido nesta rodada, e digo em vez de inventar.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita a faixa do
# que nao e energia, nao cita percentual de desconto, nao cita imposto, nao cita
# valor e nao nomeia fornecedor nem orgao. Conferido A MAO campo por campo,
# porque o portao `narracao` conta QUANTIDADES por frase e NAO pega digito cru.
#
# O QUE O VIDEO AFIRMA: que o desconto de fornecedor incide sobre a linha da
# ENERGIA e nao sobre o total da conta, e que por isso o mesmo percentual rende
# diferente em cada fatura. Esta no longo epomeno-epipedo-004 (`P2q6w9y7j88`),
# capitulos "Τι αλλάζει με τον πάροχο" e "Το φύλλο τεσσάρων γραμμών".
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) a faixa de quanto da conta nao e energia e as cinco rubricas — estao no
#       longo com fonte, e aqui o numero e o DA FATURA do espectador;
#   (2) qualquer percentual de desconto de mercado, que muda por oferta e NAO foi
#       reconferido nesta rodada em duas fontes;
#   (3) se vale ou nao trocar de fornecedor, que depende do perfil de consumo.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Έκπτωση στο ρεύμα;", "sub": "πού την υπολόγισες",
     "nar": "Σου υποσχέθηκαν έκπτωση στο ρεύμα και την υπολόγισες πάνω στο τελικό "
            "ποσό του λογαριασμού;",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Πέφτει στη γραμμή", "sub": "όχι στη σελίδα",
     "nar": "Η έκπτωση πέφτει μόνο στη γραμμή της ενέργειας. Στα υπόλοιπα της "
            "σελίδας δεν αγγίζει τίποτα.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Η σωστή σειρά", "sub": "πρώτα η γραμμή",
     "nar": "Βρες τη γραμμή της ενέργειας, βάλε την έκπτωση εκεί, και μετά δες τη "
            "διαφορά στο τελικό ποσό.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Ίδιο ποσοστό", "sub": "άλλο κέρδος",
     "nar": "Το ίδιο ποσοστό δίνει άλλο κέρδος σε κάθε λογαριασμό, γιατί η "
            "ενέργεια δεν ζυγίζει ίδια παντού.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Κάνε την πράξη", "sub": "στη δική σου φατούρα",
     "nar": "Κάνε την πράξη στον δικό σου λογαριασμό πριν υπογράψεις. Η πλήρης "
            "πράξη είναι στο βίντεο.",
     "sem_cap": True},
]

THUMB = {"l1": "Στη γραμμή,", "l2": "όχι στο σύνολο"}

COPY = """# epomeno-epipedo-s010

## TITULO
Έκπτωση Ρεύματος: Πέφτει στη Γραμμή της Ενέργειας, Όχι στο Τελικό Ποσό

## TITULO SHORT
Η έκπτωση πέφτει στη γραμμή, όχι στο σύνολο

## DESCRICAO
Όταν κάποιος ακούει «έκπτωση στο ρεύμα», ο υπολογισμός που κάνει στο κεφάλι του είναι σχεδόν πάντα ο ίδιος: παίρνει το ποσό που πληρώνει κάθε μήνα και του αφαιρεί το ποσοστό. Είναι ο λογικός υπολογισμός και είναι ο λάθος υπολογισμός, γιατί εφαρμόζει το ποσοστό σε βάση που δεν το δέχεται.

Ο λογαριασμός δεν είναι ένα πράγμα. Μέσα του υπάρχει η γραμμή της ενέργειας — αυτή που ο πάροχος πουλάει και τιμολογεί — και υπάρχουν όλα τα υπόλοιπα, που δεν τα ορίζει ο πάροχος: δίκτυα, ρυθμιζόμενες χρεώσεις, φόροι και τέλη. Η έκπτωση που σου υπόσχονται αφορά τη γραμμή της ενέργειας. Στα υπόλοιπα δεν αγγίζει τίποτα, όποιον και να διαλέξεις.

Από αυτό βγαίνει η σωστή σειρά των πράξεων, και δεν χρειάζεται κανένα νούμερο από έξω. Πρώτα βρίσκεις στη σελίδα τη γραμμή της ενέργειας. Μετά εφαρμόζεις την έκπτωση εκεί και μόνο εκεί. Και τέλος κοιτάς τη διαφορά σε σχέση με το τελικό ποσό που πληρώνεις σήμερα. Αυτό είναι το πραγματικό κέρδος της προσφοράς — και είναι συστηματικά μικρότερο από αυτό που βγάζει ο υπολογισμός «ποσοστό επί του συνόλου».

Υπάρχει και μια δεύτερη συνέπεια, που εξηγεί γιατί δύο γείτονες με την ίδια προσφορά βγάζουν διαφορετικό συμπέρασμα. Η ενέργεια δεν ζυγίζει το ίδιο σε κάθε λογαριασμό: σε κάποιον με μεγάλη κατανάλωση είναι μεγαλύτερο κομμάτι της σελίδας, σε κάποιον με μικρή είναι μικρότερο. Άρα το ίδιο ποσοστό έκπτωσης δίνει άλλο κέρδος στον καθένα — και η σύγκριση προσφορών δεν μεταφέρεται από το ένα νοικοκυριό στο άλλο.

Δεν υπάρχει εδώ ούτε ποσοστό, ούτε φόρος, ούτε ποσό: οι αριθμοί που αποφασίζουν είναι στη δική σου φατούρα. Το φύλλο των τεσσάρων γραμμών, οι πέντε επιβαρύνσεις, τι αλλάζει πραγματικά με τον πάροχο και τα τέσσερα συνηθισμένα λάθη — είναι στο βίντεο.

## COMENTARIO FIXADO
Η σειρά των πράξεων είναι το παν: πρώτα βρίσκεις τη γραμμή της ενέργειας, μετά βάζεις την έκπτωση ΕΚΕΙ, και μόνο στο τέλος κοιτάς τη διαφορά στο τελικό ποσό. Αν αφαιρέσεις το ποσοστό από το σύνολο, βγάζεις κέρδος που δεν υπάρχει. Και προσοχή στο δεύτερο: η ενέργεια δεν ζυγίζει ίδια σε κάθε λογαριασμό, άρα η σύγκριση του γείτονα δεν ισχύει για σένα. Όποιος κάνει την πράξη, ας γράψει στα σχόλια μόνο αν βγήκε μεγαλύτερο ή μικρότερο απ' όσο περίμενε — χωρίς ποσά.

## HASHTAGS
#Ρεύμα #Λογαριασμοί #ΕπόμενοΕπίπεδο

## TAGS
λογαριασμος ρευματος, εκπτωση ρευματος, γραμμη ενεργειας, παροχος ρευματος, ρυθμιζομενες χρεωσεις, συγκριση προσφορων, προσωπικα οικονομικα, ελλαδα, υπολογισμος, καταναλωση, φατουρα, νοικοκυριο, επομενο επιπεδο, αλλαγη παροχου, ποσοστο

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita a faixa do
que nao e energia, nao cita percentual de desconto, nao cita imposto, nao cita
valor e nao nomeia fornecedor nem orgao. Conferido a mao campo por campo.

O QUE O VIDEO AFIRMA: que o desconto de fornecedor incide sobre a linha da
ENERGIA e nao sobre o total da conta, e que por isso o mesmo percentual rende
diferente em cada fatura. Esta no longo epomeno-epipedo-004 (P2q6w9y7j88),
capitulos "Τι αλλάζει με τον πάροχο" e "Το φύλλο τεσσάρων γραμμών".

DESCARTADO, e vai escrito:
  (1) a faixa de quanto da conta nao e energia e as cinco rubricas — estao no
      longo com fonte; aqui o numero e o DA FATURA do espectador;
  (2) qualquer percentual de desconto de mercado — muda por oferta e NAO foi
      reconferido nesta rodada em duas fontes;
  (3) se vale ou nao trocar de fornecedor, que depende do perfil de consumo.

## FONTES
O longo de onde este short foi extraido (epomeno-epipedo-004, P2q6w9y7j88) traz
as fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s010",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#12263A", "c1": "#2A9D8F", "c2": "#E8A33D",
               "bg": "#F5F2EC"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "P2q6w9y7j88",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/epomeno-epipedo-s010.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, piso 30s, mira 35-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
