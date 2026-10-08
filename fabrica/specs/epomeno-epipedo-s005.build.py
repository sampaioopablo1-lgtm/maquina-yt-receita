"""epomeno-epipedo-s005 — a rodada em que o contador se revelou um degrau.

ALAVANCA: A (alcance por short). Oitavo short solto, quinto do epomeno.

O QUE DEU CERTO: o short solto segue o formato de melhor medicao da frota e o
mais barato em cota (~1.600 unidades contra ~2.100 do pacote).
O QUE NAO DEU: a minha leitura horaria. Entre 00:10 e 01:12 o kolejny-015 fez
+59 e o 019 +47; entre 01:12 e 02:11, MESMA janela e MESMOS ids, os dois fizeram
ZERO. O `viewCount` publico nao e continuo, e LATCHED: atualiza em DEGRAU. Logo
janela curta mede o calendario do contador, nao o trafego — e isso explica o erro
do 635 melhor do que a explicacao que eu dei no 636. O piso de 12 h agora tem
MOTIVO, nao so observacao. Aprendizado 645.
O QUE VOU MUDAR: nada na spec. A previsao do 643 (se o 015 e o 019 cruzam 1.100)
segue ABERTA e so se decide com leitura de 12 h.

POR QUE O EPOMENO: criterio inalterado e reforcado pelo dado de 14,3 h — melhor
dos tres em alcance por short (1.155 e 1.039) E em inscrito (+2, o dobro dos
outros). NUMERO DE PARTIDA: 1.155 e 1.039 dos irmaos; e o short do proprio longo
de origem (`_c8gF9urN8M`, 237 views com +226 em 16 h).

A FORMA, e NAO e experimento novo (secao 5-d): o gancho do s002, que e o melhor
da frota — ENTRADA ERRADA INVALIDA O TEU NUMERO. Aqui: "a subtracao deu zero,
mas havia uma linha de despesas fora das prestacoes". Gancho visual segue cartao
de texto nas cinco cenas, para nao sujar o experimento 33 — e vale lembrar o
aprendizado 644: o video abre com dois quadros pretos e um fade-in, e matar esse
fade e teste que ESPERA o 33 fechar.

DE ONDE SAI: do longo JA PUBLICADO `nttW9fR8wyY` (epomeno-epipedo-017), o ultimo
longo do canal ainda nao usado como origem. O short original dele ensina a
SUBTRACAO (soma das prestacoes menos preco a dinheiro); este ataca o capitulo
"Τα έξοδα στη σύγκριση" — a subtracao quebra quando existe despesa de processo,
seguro ou anuidade de cartao FORA do total das prestacoes.

IDENTIDADE: faixa do canal conferida em TRES pacotes (015, 017 e o s004) —
paleta `{ink #12263A, c1 #2A9D8F, c2 #E8A33D, bg #F5F2EC}`, trilha `Inspired`,
voz `el-GR-NestorasNeural`. O 016 segue fora da faixa, de proposito.

TENDENCIA: feed GR/26 lido as 00:15 (a 26 e PROXY; a real e a 27, sem chart em
regiao nenhuma). Veio fofoca, pizza, gadgets. NAO GRAFEI ASSUNTO, e nao reli o
feed porque o chart repete catorze de quinze itens em quatro horas (623). A
evidencia mais forte desta rodada e a medicao da propria frota; declaro a troca.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita taxa de juro, nao cita TAEG, nao cita
# valor de despesa, nao cita percentual e nao nomeia banco nem orgao. Os unicos
# numeros que ele diz sao "zero" e "duas", e sao a ARITMETICA da conta.
#
# O QUE O VIDEO AFIRMA: que despesa de processo, seguro e anuidade de cartao
# podem ficar FORA do total das prestacoes, e que por isso a subtracao precisa
# incluir tudo o que se paga para obter o credito. Isso esta no longo
# `nttW9fR8wyY` com as fontes.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) QUAIS despesas a lei grega permite cobrar e em que limite — NAO
#       reconferido hoje em duas fontes; o short diz apenas "se existir a linha";
#   (2) qualquer valor ou percentual de despesa, juro ou seguro;
#   (3) o que a conta NAO decide, que esta no longo e para la o short manda.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Βγήκε μηδέν;", "sub": "κοίτα τα έξοδα",
     "nar": "Η αφαίρεση έβγαλε μηδέν και είπες ότι είναι άτοκες; Κοίτα αν "
            "υπάρχει γραμμή εξόδων.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Μένουν έξω", "sub": "από τις δόσεις",
     "nar": "Τα έξοδα φακέλου δεν μπαίνουν στις δόσεις. Πληρώνονται χώρια, "
            "και το μηδέν σου δεν τα είδε.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Βάλ' τα μέσα", "sub": "και ξανακάνε",
     "nar": "Πρόσθεσέ τα στο σύνολο των δόσεων. Μετά ξανακάνε την αφαίρεση "
            "με την τιμή μετρητοίς.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Και τα άλλα", "sub": "ασφάλεια, κάρτα",
     "nar": "Το ίδιο για ασφάλεια ή συνδρομή κάρτας. Ό,τι πληρώνεις για να "
            "πάρεις τις δόσεις, μπαίνει.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Πριν υπογράψεις", "sub": "με τα έξοδα μέσα",
     "nar": "Ξανακάνε την αφαίρεση με τα έξοδα μέσα. Η πλήρης πράξη είναι "
            "στο βίντεο.",
     "sem_cap": True},
]

THUMB = {"l1": "Βγήκε μηδέν;", "l2": "κοίτα τα έξοδα"}

COPY = """# epomeno-epipedo-s005

## TITULO
Βγήκε Μηδέν και Είπες Άτοκες; Η Γραμμή των Εξόδων Μένει Έξω από τις Δόσεις

## TITULO SHORT
Βγήκε μηδέν; Κοίτα τα έξοδα

## DESCRICAO
Ο έλεγχος για το αν μια προσφορά με δόσεις είναι πράγματι άτοκη είναι δύο πράξεις: πολλαπλασιάζεις τον αριθμό των δόσεων με το ποσό της δόσης, και από το σύνολο αφαιρείς την τιμή μετρητοίς. Αν μείνει μηδέν, οι δόσεις δεν σου κόστισαν τίποτα παραπάνω. Αν μείνει θετικός αριθμός, αυτό είναι το κόστος της διευκόλυνσης, σε ευρώ, όχι σε ποσοστό.

Υπάρχει όμως ένα σημείο όπου το μηδέν σου μπορεί να είναι ψεύτικο, και δεν είναι λάθος στην αριθμητική: είναι ό,τι μένει ΕΞΩ από το σύνολο των δόσεων. Τα έξοδα φακέλου, όπου υπάρχουν, δεν πληρώνονται μέσα στη δόση — πληρώνονται χωριστά, συχνά στην αρχή, και η αφαίρεσή σου δεν τα είδε ποτέ. Το ίδιο ισχύει για ασφάλεια που συνοδεύει τη χρηματοδότηση και για συνδρομή ή ανανέωση κάρτας που η προσφορά απαιτεί. Ο κανόνας είναι απλός και δεν χρειάζεται γνώσεις: ό,τι πληρώνεις ΓΙΑ ΝΑ πάρεις τις δόσεις, μπαίνει στο σύνολο.

Η διορθωμένη πράξη, λοιπόν: σύνολο δόσεων, συν κάθε έξοδο που ζητά η συγκεκριμένη προσφορά, μείον η τιμή μετρητοίς. Αυτό που μένει είναι το πραγματικό κόστος, και είναι ο αριθμός με τον οποίο συγκρίνεις δύο προσφορές μεταξύ τους — ή τη δόση με το να περιμένεις και να πληρώσεις μετρητοίς.

Δύο πράγματα που αυτός ο έλεγχος ΔΕΝ κάνει. Δεν σου λέει αν αξίζει το προϊόν, και δεν σου λέει αν αντέχεις τη δόση στον μηνιαίο προϋπολογισμό σου· αυτά είναι άλλη απόφαση. Σου λέει μόνο πόσο κοστίζει η διευκόλυνση, με δικά σου νούμερα, από το χαρτί που κρατάς πριν υπογράψεις.

Εδώ δεν αναφέρεται επιτόκιο, δεν αναφέρεται ποσοστό, δεν αναφέρεται ποσό εξόδων και δεν αναφέρεται τράπεζα: ο αριθμός που αποφασίζει βγαίνει από τη δική σου προσφορά. Το πλήρες βίντεο έχει όλη την πράξη, πού βρίσκεις τα νούμερα στο χαρτί, τι σημαίνει άτοκες, και πού ο υπολογισμός δεν φτάνει.

Ενημερωτικό περιεχόμενο, δεν αποτελεί οικονομική, νομική ή επενδυτική συμβουλή.

## COMENTARIO FIXADO
Η πράξη: δόσεις επί ποσό δόσης, συν κάθε έξοδο που ζητά η προσφορά, μείον η τιμή μετρητοίς. Το κρίσιμο είναι το «συν κάθε έξοδο»: τα έξοδα φακέλου, η ασφάλεια που συνοδεύει τη χρηματοδότηση και η συνδρομή κάρτας πληρώνονται ΧΩΡΙΑ από τη δόση, κι αν δεν τα βάλεις μέσα το μηδέν σου είναι ψεύτικο. Κανόνας: ό,τι πληρώνεις για να πάρεις τις δόσεις, μπαίνει στο σύνολο. Αν κάνεις τον έλεγχο, γράψε αν η προσφορά σου είχε γραμμή εξόδων ή όχι — χωρίς να γράψεις ποσά.

## HASHTAGS
#Δόσεις #ΈξοδαΦακέλου #EpomenoEpipedo

## TAGS
δοσεις, ατοκες, εξοδα φακελου, τιμη μετρητοις, αφαιρεση, ασφαλεια, συνδρομη καρτας, προσωπικα οικονομικα, ελλαδα, υπολογισμος, προσφορα, κοστος, επομενο επιπεδο, χρηματοδοτηση, συγκριση

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
ZERO NUMERO NOVO SOBRE O MUNDO. Nao cita taxa de juro, nao cita TAEG, nao cita
valor de despesa, nao cita percentual e nao nomeia banco nem orgao. Os unicos
numeros ditos sao "zero" e "duas", e sao a aritmetica da propria conta.

O QUE O VIDEO AFIRMA: que despesa de processo, seguro e anuidade de cartao podem
ficar FORA do total das prestacoes, e que por isso a subtracao precisa incluir
tudo o que se paga para obter o credito. Esta no longo epomeno-epipedo-017
(nttW9fR8wyY) com as fontes.

DESCARTADO, e vai escrito:
  (1) QUAIS despesas a lei grega permite cobrar e em que limite — nao reconferido
      hoje em duas fontes; o short diz apenas "se existir a linha";
  (2) qualquer valor ou percentual de despesa, juro ou seguro;
  (3) o que a conta NAO decide — esta no longo, e o short manda para la.

## FONTES
O longo de onde este short foi extraido (epomeno-epipedo-017, nttW9fR8wyY) traz
as fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s005",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#12263A", "c1": "#2A9D8F", "c2": "#E8A33D",
               "bg": "#F5F2EC"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "nttW9fR8wyY",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/epomeno-epipedo-s005.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s (teto 43.1s, mira 33-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
