"""epomeno-epipedo-s003 — a rodada em que o meu INSTRUMENTO derrubou dois achados meus.

ALAVANCA: A (alcance por short). Sexto short solto da frota, terceiro do epomeno.

# ---------------------------------------------------------------------------
# O LOOP DE CORRECAO (2-B): A MUDANCA DESTA RODADA FOI A MEDICAO, E ELA
# INVALIDOU DUAS COISAS QUE EU MESMO TINHA ESCRITO HORAS ANTES
# ---------------------------------------------------------------------------
PRIMEIRO, O FURO: em 07/10 a tabela `metricas` recebeu DUAS coletas (113 linhas)
enquanto eu lia a API ao vivo QUATRO vezes sem gravar nenhuma. O achado mais
importante daquele dia saiu de numeros que estavam na conversa e nao no banco.
A correcao nao foi lembrar de gravar: foi tornar impossivel ler sem gravar.
`grava_metricas(jsonb)` e `grava_metricas(bigint)` inserem em `metricas` e
DEVOLVEM a leitura com `delta` e `horas_desde`. O retorno da funcao E o dado que
decide. Aprendizado 637.

SEGUNDO, O QUE A PRIMEIRA LEITURA PELA FUNCAO FEZ COM O MEU ACHADO: ela
INVALIDOU o aprendizado 635. Eu havia escrito "view de short e rajada que
morre", medindo com janela de DUAS horas. Com 14,4 h entre coletas, sobre
quarenta ids:
    kolejny-019      4 -> 283   (+279)
    epomeno-017     11 -> 237   (+226)
    kolejny-015    133 -> 396   (+263)
    kolejny-018     38 -> 113   (+75)
    labtreinam.-009 12 ->  75   (+63)
  e o TOPO, esse sim, parado:
    kolejny-017  1.119 -> 1.132 (+13)
    labtr.-007   1.133 -> 1.133 (+0)
O short NAO morre: ACUMULA a ~15-20 views/hora e SATURA entre 1.100 e 1.160.
A vinte views/hora, duas horas cabem em quarenta views — eu li zero como morte
quando era falta de resolucao do instrumento. **O erro era meu, nao do mundo.**
JANELA MINIMA DE LEITURA AGORA: 12 h. Aprendizado 636.

TERCEIRO, e e o pior dos tres: `viewCount` de `channels.list` NAO CONTA VIEWS DE
SHORTS. No epomeno a soma dos deltas por video deu ~332 views em 14,3 h e o
`viewCount` do canal subiu SETE. No kolejny subiu UMA enquanto os shorts dele
cresciam centenas. Logo a minha conta "converte 0,65% das views do canal em
inscrito, faltam 435, ~33 dias" estava invalida nos DOIS fatores. Projecao de
inscrito agora sai do delta de `subscriberCount` e de nada mais. Aprendizados
638 e 639: a ~0,29 inscrito por video publicado, o epomeno pede ~144 dias para
os 500 e nao 33.

POR QUE ESTE SHORT E DO EPOMENO: pelo dado de 14,4 h ele e o melhor dos tres nas
DUAS metades — alcance por short (os soltos dele sao o primeiro e o quarto da
frota, 1.155 e 1.039) e inscrito (+2 em 14,3 h, o dobro dos outros dois). O
labtreinamento, que eu tratava como favorito, e o pior em alcance por uma ordem
de grandeza (149 e 29).

NUMERO DE PARTIDA: 1.155 views do s002 e 1.039 do s001, que sao os dois melhores
soltos da frota; e a mediana de ~280 apos um dia. Este short tem de ficar na
faixa dos irmaos dele, nao na mediana.

A FORMA, e NAO e experimento novo (secao 5-d): copio o gancho do s002, que e o
que mediu melhor na frota inteira — ENTRADA ERRADA INVALIDA O TEU NUMERO. O s002
dizia "fizeste a conta no mes errado?"; este diz "a tua divisao saiu barata
porque faltam os pneus dentro dos doze meses". Mesma familia de gancho, assunto
outro. Isso NAO conta como mudanca nova, e o experimento 33 (motion no short)
segue intacto — nao mexi no gancho VISUAL, que continua cartao de texto nas
cinco cenas, exatamente como nos cinco irmaos.

O QUE DEU CERTO: o short solto, que e o formato de melhor medicao da frota e o
mais barato em cota (~1.600 unidades contra ~2.100 do pacote).
O QUE NAO DEU: a minha janela de leitura, duas vezes, e o meu denominador.
O QUE VOU MUDAR: nada na spec. A mudanca da rodada foi o instrumento, e ela
sozinha reescreveu a secao 1 da rotina.

DE ONDE SAI: do longo JA PUBLICADO `opFSah50OWo` (epomeno-epipedo-013), que com
47 views e o MELHOR longo recente da frota inteira. O short original dele
(`p1uvroDdKvg`, 154 views e parado em 154) ENSINA a divisao: euros a dividir por
quilometros. O angulo deste e outro e ataca o capitulo "Ποτε σε ξεγελαει": a
MESMA divisao devolve numero diferente conforme os doze meses escolhidos
engolirem ou nao a despesa grande que nao vem todo ano.

IDENTIDADE: faixa do canal conferida em TRES pacotes (013, 015 e o s002) —
paleta `{ink #12263A, c1 #2A9D8F, c2 #E8A33D, bg #F5F2EC}`, trilha `Inspired`,
voz `el-GR-NestorasNeural`. O 016 segue fora da faixa, de proposito.

TENDENCIA: feed GR/26 lido em 08/10 00:15 — e a 26 e PROXY, a categoria real e a
27 (Education), que nao tem chart `mostPopular` em regiao nenhuma (610). Os
quinze itens eram fofoca de celebridade, pizza, gadgets e vaping. NAO GRAFEI
ASSUNTO. A unica forma aproveitavel era o imperativo em segunda pessoa com
recompensa imediata, e ela ja e a forma da casa. A evidencia mais forte desta
rodada e a medicao da propria frota, de minutos antes, e eu declaro a troca.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO. Este short nao cita preco de combustivel, nao
# cita valor de pneu, nao cita taxa, nao cita aliquota e nao nomeia orgao. Os
# unicos numeros que ele diz sao "doze" (doze meses) e "dois" (dois servicos), e
# sao a ARITMETICA da conta, nao afirmacao sobre o mundo.
#
# O QUE O VIDEO AFIRMA: que pneu e revisao grande nao ocorrem todo ano, e que
# por isso a escolha dos doze meses muda o resultado da divisao. Isso e
# aritmetica da propria conta e esta no longo `opFSah50OWo` com as fontes.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) de quantos em quantos quilometros se troca pneu, e de quanto em quanto
#       tempo se faz a revisao grande — NAO reconferido hoje em duas fontes; o
#       short diz apenas "nao vem todo ano" sem numero;
#   (2) qualquer valor em euros de pneu, combustivel, seguro ou imposto de
#       circulacao;
#   (3) as tres situacoes em que a conta engana, que estao no longo — o short
#       manda para la em vez de listar de memoria.
#
# FONTE UNICA ACEITAVEL: nenhuma e necessaria. Short extraido de longo ja
# publicado que nao introduz numero novo sobre o mundo (secao 5), e o longo que
# carrega as fontes e o `opFSah50OWo`.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Βγήκε φθηνό;", "sub": "λείπουν τα λάστιχα",
     "nar": "Έκανες τη διαίρεση και βγήκε φθηνό; Δες αν μέσα στους δώδεκα "
            "μήνες υπάρχουν λάστιχα.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Γιατί χαλάει", "sub": "δεν έρχονται κάθε χρόνο",
     "nar": "Τα λάστιχα και το μεγάλο σέρβις δεν έρχονται κάθε χρόνο. Αν "
            "έπεσαν έξω, το κόστος βγαίνει μικρότερο.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Τι διορθώνεις", "sub": "κλείσε τον κύκλο",
     "nar": "Πάρε δώδεκα μήνες που περιέχουν την τελευταία αλλαγή. Ή μοίρασε "
            "το ποσό στα χρόνια ζωής τους.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Και αντίστροφα", "sub": "βγαίνει ακριβότερο",
     "nar": "Ισχύει και αντίστροφα. Δώδεκα μήνες με δύο σέρβις δείχνουν "
            "κόστος μεγαλύτερο από το αληθινό.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Ξανακάνε το", "sub": "με κλειστό κύκλο",
     "nar": "Ξανακάνε τη διαίρεση με κλειστό κύκλο. Η πλήρης πράξη είναι στο "
            "βίντεο.",
     "sem_cap": True},
]

THUMB = {"l1": "Βγήκε φθηνό;", "l2": "λείπουν λάστιχα"}

COPY = """# epomeno-epipedo-s003

## TITULO
Βγήκε Φθηνό το Χιλιόμετρο; Έλεγξε αν τα Λάστιχα Έπεσαν Έξω από τους Δώδεκα Μήνες

## TITULO SHORT
Βγήκε φθηνό; Λείπουν τα λάστιχα

## DESCRICAO
Η πράξη που δείχνει πόσο σου κοστίζει κάθε χιλιόμετρο είναι μία διαίρεση: παίρνεις όλα όσα πλήρωσες για το αυτοκίνητο σε δώδεκα μήνες και τα διαιρείς με τα χιλιόμετρα της ίδιας περιόδου. Το αποτέλεσμα είναι το κόστος ανά χιλιόμετρο, και με αυτό κρίνεις αν αξίζει μια διαδρομή, αν αξίζει το ταξί, αν αξίζει η μετακόμιση πιο κοντά στη δουλειά.

Υπάρχει όμως ένα σημείο όπου η πράξη σε ξεγελάει, και δεν είναι η διαίρεση: είναι η ΕΠΙΛΟΓΗ των δώδεκα μηνών. Τα λάστιχα και το μεγάλο σέρβις δεν έρχονται κάθε χρόνο. Αν ο κύκλος που διάλεξες έπεσε ακριβώς ανάμεσα σε δύο αλλαγές, η μεγάλη δαπάνη έμεινε έξω και το κόστος σου βγαίνει μικρότερο από το αληθινό — και με αυτόν τον μικρότερο αριθμό αποφασίζεις σαν να είναι φθηνότερο το αυτοκίνητο από ό,τι είναι.

Δύο τρόποι να το διορθώσεις. Ο πρώτος: πάρε δώδεκα μήνες που περιέχουν την τελευταία αλλαγή λάστιχων, ώστε ο κύκλος να κλείνει. Ο δεύτερος, που είναι και ο σωστότερος όταν έχεις τα στοιχεία: μοίρασε το ποσό της μεγάλης δαπάνης σε όσα χρόνια πραγματικά κρατάει, και βάλε στη διαίρεση μόνο το μέρος που αναλογεί στη χρονιά.

Ισχύει και αντίστροφα, και αυτό το ξεχνάμε: δώδεκα μήνες που έτυχε να έχουν δύο σέρβις μαζί δείχνουν κόστος πιο ακριβό από το αληθινό. Η πράξη δεν είναι λάθος σε καμία από τις δύο περιπτώσεις — λάθος είναι το παράθυρο.

Εδώ δεν αναφέρεται τιμή καυσίμου, δεν αναφέρεται ποσό για λάστιχα, δεν αναφέρεται τέλος κυκλοφορίας και δεν αναφέρεται συντελεστής: ο αριθμός που αποφασίζει βγαίνει από τις δικές σου αποδείξεις και από τον δικό σου χιλιομετρητή. Το πλήρες βίντεο έχει όλη την πράξη, το πού βρίσκεις τα νούμερα, τις τρεις στιγμές που η πράξη σε ξεγελάει, και το τι ΔΕΝ πιάνει αυτή η διαίρεση.

Ενημερωτικό περιεχόμενο, δεν αποτελεί φορολογική, νομική ή οικονομική συμβουλή.

## COMENTARIO FIXADO
Η πράξη είναι μία διαίρεση: όλα όσα πλήρωσες για το αυτοκίνητο σε δώδεκα μήνες, διά τα χιλιόμετρα της ίδιας περιόδου. Το κρίσιμο είναι η ΕΠΙΛΟΓΗ του παραθύρου: τα λάστιχα και το μεγάλο σέρβις δεν έρχονται κάθε χρόνο, κι αν έπεσαν έξω το κόστος βγαίνει ψεύτικα μικρό. Διόρθωσέ το με δύο τρόπους — είτε πάρε δώδεκα μήνες που περιέχουν την τελευταία αλλαγή, είτε μοίρασε τη μεγάλη δαπάνη σε όσα χρόνια κρατάει. Και θυμήσου ότι ισχύει και αντίστροφα: δύο σέρβις στο ίδιο παράθυρο δείχνουν κόστος ακριβότερο από το αληθινό. Αν κάνεις την πράξη, γράψε αν ο κύκλος σου έκλεινε ή όχι — χωρίς να γράψεις ποσά.

## HASHTAGS
#ΚόστοςΑνάΧιλιόμετρο #Αυτοκίνητο #EpomenoEpipedo

## TAGS
κοστος ανα χιλιομετρο, αυτοκινητο, λαστιχα, σερβις, διαιρεση, δωδεκα μηνες, χιλιομετρητης, προσωπικα οικονομικα, ελλαδα, υπολογισμος, παραθυρο, μεγαλη δαπανη, επομενο επιπεδο, καυσιμα, αποσβεση

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
ZERO NUMERO NOVO SOBRE O MUNDO. Este short nao cita preco de combustivel, nao
cita valor de pneu, nao cita taxa de circulacao, nao cita aliquota e nao nomeia
orgao. Os unicos numeros que ele diz sao "doze" (doze meses) e "dois" (dois
servicos), e sao a aritmetica da propria conta.

O QUE O VIDEO AFIRMA: que pneu e revisao grande nao ocorrem todo ano, e que por
isso a escolha dos doze meses muda o resultado da divisao. Isso e aritmetica da
conta e esta no longo epomeno-epipedo-013 (opFSah50OWo) com as fontes.

DESCARTADO, e vai escrito:
  (1) de quantos em quantos quilometros se troca pneu e de quanto em quanto tempo
      se faz a revisao grande — NAO reconferido hoje em duas fontes; o short diz
      apenas "nao vem todo ano", sem numero;
  (2) qualquer valor em euros de pneu, combustivel, seguro ou imposto;
  (3) as tres situacoes em que a conta engana — estao no longo, e o short manda
      para la em vez de listar de memoria.

## FONTES
O longo de onde este short foi extraido (epomeno-epipedo-013, opFSah50OWo) traz
as fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s003",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#12263A", "c1": "#2A9D8F", "c2": "#E8A33D",
               "bg": "#F5F2EC"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "opFSah50OWo",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/epomeno-epipedo-s003.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa short: {s:.1f}s (teto do portao 43.1s, mira 33-37)")
    print(f"narracao: media {sum(tam)/len(tam):.0f} chars, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo do short: {tit!r} ({len(tit)} chars)")
    print(f"aponta para o longo: {SPEC['longo_existente']}")
