"""epomeno-epipedo-s004 — a rodada em que a minha propria funcao ia me enganar.

ALAVANCA: A (alcance por short). Setimo short solto, quarto do epomeno.

# ---------------------------------------------------------------------------
# O LOOP DE CORRECAO (2-B): O FURO ESTAVA NA CORRECAO DE DUAS HORAS ANTES
# ---------------------------------------------------------------------------
Em 07/10 23:20 eu criei `grava_metricas` para que nao exista ler sem gravar
(aprendizado 637). A funcao comparava contra a coleta MAIS RECENTE do mesmo id.
Parecia certo. Nao era: a rotina roda de HORA EM HORA, logo a coleta mais recente
tem sempre UMA hora, e o `delta` devolvido seria sempre de uma hora — a mesma
janela curta que produziu o aprendizado 635 errado e que o 636 proibiu. **A minha
correcao reproduziria o meu erro, sozinha, para sempre, e em silencio.**
Achado em 08/10 01:12 ANTES de produzir dano. Agora existe
`grava_metricas_janela(req_id, min_horas default 12)`, que grava sempre mas
compara contra a coleta mais recente com PELO MENOS doze horas, e devolve
`base_em` para que a rodada veja contra QUANDO comparou em vez de confiar.
Provado na primeira chamada: ela PULOU a coleta de 00:10 e usou a de 09:31,
16,01 h atras.

NAO REMOVI as versoes antigas — o sistema de permissao desta sessao recusou o
DROP, e recusou tambem o UPDATE que anotaria a correcao dentro do registro 636.
Entao fiz por ADICAO: funcao nova com nome novo, e as antigas marcadas como
OBSOLETAS no proprio `comment`. Fica declarado em vez de parecer limpo.

O QUE A LEITURA NOVA TROUXE, e corrige NUMERO MEU de duas horas antes:
  * A TAXA ESTAVA SUBESTIMADA. Entre 00:10 e 01:12, uma hora:
        kolejny-015  396 -> 455   (+59/h)
        kolejny-019  283 -> 330   (+47/h)
    Eu havia escrito "15 a 20 views/hora" no 636. Chega a 59, e esses dois estao
    ACELERANDO.
  * LOGO O TETO DE 1.150 E EVIDENCIA FRACA: saiu de TRES pontos vizinhos (1.155,
    1.133, 1.132) e pode ser coincidencia de amostra. A 47-59 views/hora o 015 e
    o 019 cruzam 1.100 em ~14 h. **PREVISAO VERIFICAVEL:** se PARAREM perto de
    1.150 o teto existe; se PASSAREM, o teto era artefato e a conta dos tres
    milhoes muda de novo, para melhor. Rebaixei o 636 para `observado` ate la.
  * O QUE SEGUE MEDIDO: os dois do topo estao parados de fato — labtreinamento-007
    com +0 e kolejny-017 com +13 em 16,01 h.

POR QUE ESTE SHORT E DO EPOMENO: o criterio nao mudou e o dado de hoje reforcou.
O epomeno e o melhor dos tres nas DUAS metades — alcance (os soltos dele sao o
primeiro e o quarto da frota, 1.155 e 1.039) e inscrito (+2 em 14,3 h, o dobro
dos outros dois). O labtreinamento e o pior em alcance por uma ordem de grandeza.

NUMERO DE PARTIDA: 1.155 e 1.039 dos irmaos s002 e s001; e o short do proprio
longo de origem (`t8onUf29ukQ`, 366 views e ainda subindo +49 em 16 h).

A FORMA, e NAO e experimento novo (secao 5-d): copio DUAS coisas que mediram
melhor. Primeira, o gancho do s002, que e o melhor da frota — ENTRADA ERRADA
INVALIDA O TEU NUMERO; aqui e "o numero oficial nao mede o teu cesto". Segunda,
a leitura medida da secao 5: os dois melhores longos do canal irmao rodam sobre
PAPEL QUE O ESPECTADOR JA TEM NA MAO, e este short roda inteiro sobre as
aproveis dele. Gancho visual segue CARTAO DE TEXTO nas cinco cenas, igual aos
seis irmaos, porque mexer nisso sujaria o experimento 33.

O QUE DEU CERTO: o short solto, formato de melhor medicao e mais barato em cota.
O QUE NAO DEU: a minha primeira versao do `grava_metricas`, que embutia a janela
curta que eu mesmo acabara de proibir.
O QUE VOU MUDAR: nada na spec. A mudanca da rodada foi a janela da funcao.

DE ONDE SAI: do longo JA PUBLICADO `9U2h4HuAzLs` (epomeno-epipedo-015). O short
original dele ensina a DISTINGUIR os dois indices oficiais; este ataca o
capitulo "Το δικό σου καλάθι, από τις αποδείξεις σου" — construir o indice
PROPRIO a partir das aproveis, que e o numero que de fato decide para quem
assiste.

IDENTIDADE: faixa do canal conferida em TRES pacotes (013, 015 e o s003) —
paleta `{ink #12263A, c1 #2A9D8F, c2 #E8A33D, bg #F5F2EC}`, trilha `Inspired`,
voz `el-GR-NestorasNeural`. O 016 segue fora da faixa, de proposito.

TENDENCIA: feed GR/26 lido as 00:15 desta madrugada — e a 26 e PROXY, a real e a
27 (Education), que nao tem chart `mostPopular` em regiao nenhuma (610). Veio
fofoca, pizza, gadgets e vaping. NAO GRAFEI ASSUNTO. O chart repete catorze de
quinze itens em quatro horas (623), logo nao o reli uma hora depois; a evidencia
mais forte desta rodada e a medicao da propria frota, de minutos antes, e eu
declaro a troca.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO. Este short nao cita taxa de inflacao, nao cita
# indice, nao cita ano-base, nao cita percentual e nao nomeia orgao — nem ELSTAT,
# nem Eurostat, nem BCE. Os unicos numeros que ele diz sao "cinco" (cinco itens)
# e "dois" (dois totais), e sao a ARITMETICA da conta.
#
# O QUE O VIDEO AFIRMA: que o indice oficial mede um cesto medio e nao o cesto de
# quem assiste, e que dividir o total de agora pelo total do mesmo mes do ano
# passado da a variacao do cesto PROPRIO. A primeira parte esta no longo
# `9U2h4HuAzLs` com as fontes; a segunda e aritmetica.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) QUAL dos dois indices oficiais entra em qual contrato, e o ano-base de
#       cada um — esta no longo, com fonte, e o short NAO repete de memoria;
#   (2) qualquer percentual de inflacao, de qualquer mes;
#   (3) a ressalva do BCE sobre habitacao propria e a mudanca de janeiro de 2026
#       — estao no longo; citar de memoria seria numero novo sem reconferencia.
#
# FONTE UNICA ACEITAVEL: nenhuma e necessaria. Short extraido de longo ja
# publicado que nao introduz numero novo sobre o mundo (secao 5), e o longo que
# carrega as fontes e o `9U2h4HuAzLs`.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Όχι το καλάθι σου", "sub": "ένα μέσο καλάθι",
     "nar": "Ο επίσημος πληθωρισμός δεν μετράει το δικό σου καλάθι. "
            "Μετράει ένα μέσο καλάθι.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Οι αποδείξεις", "sub": "πέντε πράγματα",
     "nar": "Το δικό σου βγαίνει από τις αποδείξεις σου. Διάλεξε πέντε "
            "πράγματα που αγοράζεις κάθε μήνα.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Δύο σύνολα", "sub": "ίδιος μήνας, πέρυσι",
     "nar": "Βρες πόσο κόστιζαν τον ίδιο μήνα πέρυσι. Κρατάς δύο σύνολα: του "
            "τότε και του τώρα.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Μία διαίρεση", "sub": "τώρα διά τότε",
     "nar": "Διαίρεσε το τώρα με το τότε. Αυτός είναι ο πληθωρισμός σου, και "
            "δεν συμφωνεί πάντα με τις ειδήσεις.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Φτιάξε τη λίστα", "sub": "απόψε",
     "nar": "Φτιάξε τη λίστα σου απόψε. Η πλήρης πράξη είναι στο βίντεο.",
     "sem_cap": True},
]

THUMB = {"l1": "Το καλάθι σου", "l2": "όχι το μέσο"}

COPY = """# epomeno-epipedo-s004

## TITULO
Ο Πληθωρισμός σου Βγαίνει από τις Αποδείξεις σου, Όχι από το Μέσο Καλάθι

## TITULO SHORT
Ο πληθωρισμός σου, από τις αποδείξεις

## DESCRICAO
Ο επίσημος δείκτης τιμών δεν είναι λάθος, αλλά δεν μετράει εσένα: μετράει ένα μέσο καλάθι, φτιαγμένο ώστε να αντιπροσωπεύει ένα σύνολο νοικοκυριών. Αν εσύ δεν έχεις αυτοκίνητο, αν δεν καπνίζεις, αν τρως έξω κάθε μέρα ή αν δεν τρως έξω ποτέ, το καλάθι σου έχει άλλο βάρος σε κάθε κατηγορία — και άρα άλλη μεταβολή. Γι' αυτό μπορείς να διαφωνείς με τον επίσημο αριθμό χωρίς να διαφωνείς με τη μέτρηση.

Η πράξη για το δικό σου είναι απλή και δεν χρειάζεται κανέναν δείκτη. Διάλεξε πέντε πράγματα που αγοράζεις κάθε μήνα, σταθερά, από αυτά που θα αγόραζες είτε ακρίβυναν είτε όχι. Βρες πόσο σου κόστιζαν τον ίδιο μήνα πέρυσι — από απόδειξη, από το ιστορικό της κάρτας ή από την εφαρμογή του σουπερμάρκετ, όχι από μνήμη. Κράτα δύο σύνολα: του τότε και του τώρα. Διαίρεσε το τώρα με το τότε, και αυτό που βγαίνει είναι η μεταβολή του δικού σου καλαθιού.

Τρεις κανόνες για να μη σε ξεγελάσει η πράξη. Πρώτον, ίδιος μήνας με ίδιο μήνα: οι τιμές έχουν εποχικότητα και η σύγκριση Δεκεμβρίου με Ιούνιο δεν μετράει τίποτα. Δεύτερον, ίδια ποσότητα και ίδια συσκευασία — αν το πακέτο μίκρυνε και η τιμή έμεινε, εσύ πλήρωσες ακριβότερα και η πράξη πρέπει να το δει. Τρίτον, μη διαλέγεις ό,τι ακρίβυνε περισσότερο· τότε δεν μετράς το καλάθι σου, μετράς τον θυμό σου.

Αυτός ο αριθμός δεν αντικαθιστά τον επίσημο, και δεν μπαίνει σε συμβόλαιο. Κάνει κάτι άλλο: σου λέει πόσο μεγάλωσε ο δικός σου λογαριασμός, με δικά σου στοιχεία, και σου δίνει βάση να αποφασίσεις — τι να αλλάξεις, τι να ζητήσεις, πού να κοιτάξεις. Το πλήρες βίντεο έχει ποιοι επίσημοι δείκτες υπάρχουν, ποιος μπαίνει στο χαρτί σου, τι μένει έξω από τη μέτρηση και πού τα διαβάζεις μόνος σου.

Ενημερωτικό περιεχόμενο, δεν αποτελεί οικονομική, φορολογική ή νομική συμβουλή.

## COMENTARIO FIXADO
Η πράξη: πέντε πράγματα που αγοράζεις σταθερά κάθε μήνα, σύνολο τώρα διά σύνολο τον ίδιο μήνα πέρυσι. Τρεις κανόνες για να μη σε ξεγελάσει — ίδιος μήνας με ίδιο μήνα λόγω εποχικότητας, ίδια ποσότητα και συσκευασία γιατί το μικρότερο πακέτο στην ίδια τιμή είναι αύξηση, και μη διαλέγεις μόνο ό,τι ακρίβυνε περισσότερο. Τα στοιχεία βγαίνουν από αποδείξεις, από το ιστορικό της κάρτας ή από την εφαρμογή του σουπερμάρκετ, όχι από μνήμη. Αν την κάνεις, γράψε πόσα από τα πέντε κατάφερες να βρεις πέρυσι — χωρίς να γράψεις ποσά.

## HASHTAGS
#Πληθωρισμός #ΤοΚαλάθιΣου #EpomenoEpipedo

## TAGS
πληθωρισμος, καλαθι, αποδειξεις, δεικτης τιμων, σουπερμαρκετ, προσωπικα οικονομικα, ελλαδα, υπολογισμος, εποχικοτητα, συσκευασια, μεσο καλαθι, διαιρεση, επομενο επιπεδο, τιμες, νοικοκυριο

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
ZERO NUMERO NOVO SOBRE O MUNDO. Este short nao cita taxa de inflacao, nao cita
indice, nao cita ano-base, nao cita percentual e nao nomeia orgao — nem ELSTAT,
nem Eurostat, nem BCE. Os unicos numeros que ele diz sao "cinco" (cinco itens) e
"dois" (dois totais), e sao a aritmetica da conta.

O QUE O VIDEO AFIRMA: que o indice oficial mede um cesto medio e nao o de quem
assiste, e que dividir o total de agora pelo total do mesmo mes do ano passado da
a variacao do cesto proprio. A primeira parte esta no longo epomeno-epipedo-015
(9U2h4HuAzLs) com as fontes; a segunda e aritmetica.

DESCARTADO, e vai escrito:
  (1) QUAL dos dois indices oficiais entra em qual contrato e o ano-base de cada
      um — esta no longo, com fonte, e o short nao repete de memoria;
  (2) qualquer percentual de inflacao, de qualquer mes;
  (3) a ressalva do BCE sobre habitacao propria e a mudanca de janeiro de 2026 —
      estao no longo; citar de memoria seria numero novo sem reconferencia.

## FONTES
O longo de onde este short foi extraido (epomeno-epipedo-015, 9U2h4HuAzLs) traz
as fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s004",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#12263A", "c1": "#2A9D8F", "c2": "#E8A33D",
               "bg": "#F5F2EC"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "9U2h4HuAzLs",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/epomeno-epipedo-s004.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa short: {s:.1f}s (teto do portao 43.1s, mira 33-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f} chars, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para o longo: {SPEC['longo_existente']}")
