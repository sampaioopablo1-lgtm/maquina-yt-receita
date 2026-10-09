"""epomeno-epipedo-s014 — antes de comparar tarifas, olha a UNIDADE.

ALAVANCA: o PAR de 09/10 apareceu nesta rodada e esta registrado no 681. As duas
pecas do tratamento novo que passaram das 6 h divergiram por fator 30:
`epomeno-s011` com mediana 303 as 6,7 h e `labtreinamento-s008` com 9 as 6,5 h.
O canal NAO explica — o `labtreinamento-s007`, tratamento antigo e mesmo canal,
fez 144 as 10,9 h, comparavel ao `epomeno-s010` (176 as 8,9 h). Logo o s008 e
anomalo ate para o proprio canal.

Restam duas causas que eu controlo, e nao sei qual: PERFIL da origem (651:
dinheiro proprio contra conformidade corporativa) e FORMA DO TITULO (o s008 e a
UNICA peca do lote novo titulada como aforismo declarativo). O TESTE QUE SEPARA
as duas JA ESTA NO AR: o `labtreinamento-s009` tem a mesma origem de perfil ruim
e titulo de ENDERECO DIRETO. Se o perfil manda, fica junto do s008; se a forma
manda, sobe. **Nao abro peca nova para isso e nao decido antes das 12 h de
ambos** — 12:40 e 17:18.

O QUE DEU CERTO: o epomeno esta distribuindo bem o lote novo — s011 303 as 6,7 h,
s012 265 as 4,9 h, s013 109 as 2,8 h, todas com tres leituras.

O QUE NAO DEU: o `kolejny-poziom-s012` esta em 32 as 3,9 h, faixa 6 a 32, contra
256 do s011 do mesmo canal as 5,8 h. Pode ser idade, pode ser a peca. Nao decido.

O QUE VOU MUDAR: uma coisa so, a FAMILIA da entrada errada — e escolhi a que o
feed GR premia na forma. Titulo em IMPERATIVO com endereco direto, que e o padrao
do GR/26 lido as 04:1x (duas a tres perguntas em quinze, contra imperativos e
nome proprio).
NUMERO DE PARTIDA: 1 view no short do pacote de origem (praticamente nao
distribuiu); 303 do melhor solto do canal as 6,7 h.

DE ONDE SAI: longo `wUHuwyO2HYo` (epomeno-epipedo-012, a cor do teu tarifario),
capitulo "Οι τιμές | από επίσημη πηγή, όχι από διαφήμιση", item "Πρόσεξε τη
μονάδα", mais "Πάρε την ίδια ημερομηνία" e "Το ίδιο νούμερο, δύο φορές". O short
ORIGINAL do pacote faz as quatro cores e as duas multiplicacoes, e NAO toca em
nenhuma das tres condicoes que fazem a conta valer.

A ENTRADA ERRADA, e e aritmetica pura: a comparacao falha na UNIDADE, nao na
conta. Preco em euro por kilowatt-hora contra preco em centimos por kilowatt-hora
e o MESMO preco escrito com numero cem vezes diferente. Quem nao repara acha que
achou uma pechincha de fator cem.

FAMILIA, regra (f): hoje no epomeno sairam "leia a linha no seu documento"
(s011), "o numero medio nao e o seu" (s012) e "voce otimiza o lado errado do seu
balanco" (s013). Esta e "a sua comparacao esta errada antes da conta comecar".

IDENTIDADE: faixa ATUAL do canal `{ink #12263A, c1 #2A9D8F, c2 #E8A33D,
bg #F5F2EC}`, trilha `Inspired` (601).

TENDENCIA: o GR/26 foi lido as 04:1x e NAO foi relido — tres horas, dentro da
janela de repeticao do 623, que eu confirmei em 4,5 h no BR/26. Digo em vez de
fingir leitura nova.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO PRECO. Nao cita tarifa, nao cita o
# valor do termo fixo, nao cita desconto, nao nomeia fornecedor nem a autoridade
# reguladora, e nao diz qual cor e mais barata. Conferido A MAO campo por campo,
# porque o portao `narracao` conta QUANTIDADES por frase e NAO pega digito cru.
#
# UNICO NUMERAL NA NARRACAO: "εκατό φορές" (cem vezes). NAO e numero sobre o
# mundo — e a razao entre euro e centimo, que e definicao de unidade e nao muda
# nunca. E justamente ela o conteudo da peca.
#
# A REGRA (g) MANDA o resto para fora: tarifa, termo fixo e desconto mudam por
# oferta e por mes, e um short com o preco deste mes fica errado no proximo e
# continua no ar. O short fica com as tres CONDICOES da comparacao, que nao
# envelhecem.
#
# O QUE O VIDEO AFIRMA: que o preco por kilowatt-hora aparece escrito em euro ou
# em centimos, e que as duas escritas diferem por fator cem para o mesmo preco;
# que as duas tarifas comparadas tem de ser lidas na MESMA data; e que o MESMO
# numero de consumo tem de entrar nos dois lados da conta. Esta no longo
# epomeno-epipedo-012 (`wUHuwyO2HYo`), capitulo "Οι τιμές", itens "Πρόσεξε τη
# μονάδα", "Πάρε την ίδια ημερομηνία" e "Το ίδιο νούμερο, δύο φορές".
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) todos os precos e o termo fixo — mudam por oferta e por mes;
#   (2) o nome da ferramenta oficial de comparacao e da autoridade, que estao no
#       longo e cuja disponibilidade NAO foi reconferida nesta rodada;
#   (3) as outras cinco armadilhas do capitulo "Τι δεν πιάνει η πράξη" (termo
#       fixo, desconto de pontualidade, prazo de fidelizacao, oferta de boas
#       vindas, clausula de revisao) — sao OUTRA peca, nao se empilham aqui.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Η διαφορά σου φάνηκε", "sub": "τεράστια;",
     "nar": "Βρήκες την τιμή ενός άλλου τιμολογίου και η διαφορά σου φάνηκε "
            "τεράστια. Κοίτα πρώτα τη μονάδα.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Ευρώ ή λεπτά", "sub": "ίδια τιμή",
     "nar": "Η τιμή γράφεται σε ευρώ ανά κιλοβατώρα, και μερικές φορές σε λεπτά "
            "ανά κιλοβατώρα — εκατό φορές άλλο νούμερο για το ίδιο πράγμα.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Ίδια ημέρα", "sub": "και τις δύο",
     "nar": "Πάρε και τις δύο τιμές την ίδια ημέρα, και ποτέ από διαφήμιση. Τιμή "
            "από σήμερα εναντίον τιμής από πέρσι δεν είναι σύγκριση.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Ίδια κατανάλωση", "sub": "στις δύο πλευρές",
     "nar": "Και βάλε το ίδιο ακριβώς νούμερο κατανάλωσης στις δύο πλευρές της "
            "πράξης. Όλο το κόλπο της σύγκρισης είναι αυτό.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Κάνε εγγραφή", "sub": "για τα επόμενα",
     "nar": "Και δεν συγκρίνεις εταιρείες, συγκρίνεις τιμολόγια. Κάνε εγγραφή για "
            "τα επόμενα, και η πράξη είναι στο βίντεο.",
     "sem_cap": True},
]

THUMB = {"l1": "Κοίτα", "l2": "τη μονάδα"}

COPY = """# epomeno-epipedo-s014

## TITULO
Σύγκριση Τιμολογίων Ρεύματος: Οι Τρεις Προϋποθέσεις που Κάνουν την Πράξη να Ισχύει

## TITULO SHORT
Σύγκρινες τιμές; Κοίτα τη μονάδα

## DESCRICAO
Η πράξη για να συγκρίνεις το τιμολόγιό σου με ένα άλλο είναι απλή: κιλοβατώρες επί τιμή, δύο φορές, και αφαίρεση. Το δύσκολο δεν είναι η πράξη — είναι να βάλεις μέσα τα σωστά νούμερα. Και υπάρχουν τρεις προϋποθέσεις που, αν τις παραβλέψεις, κάνουν το αποτέλεσμα όχι ανακριβές αλλά άσχετο.

Η πρώτη είναι η μονάδα, και είναι η πιο ύπουλη. Η τιμή ανά κιλοβατώρα γράφεται άλλοτε σε ευρώ και άλλοτε σε λεπτά. Είναι ακριβώς το ίδιο πράγμα γραμμένο με νούμερο εκατό φορές διαφορετικό. Αν πάρεις τη δική σου τιμή σε ευρώ και τη σύγκρινες με μια τιμή σε λεπτά, δεν βρήκες προσφορά — βρήκες λάθος ανάγνωση. Πριν από οτιδήποτε άλλο, κοίτα τι γράφει δίπλα στο νούμερο.

Η δεύτερη είναι η ημερομηνία. Πάρε και τις δύο τιμές την ίδια ημέρα. Η δική σου τιμή είναι στη σύμβαση και επαναλαμβάνεται στον λογαριασμό, στην ανάλυση της χρέωσης ενέργειας· η τιμή του άλλου τιμολογίου υπάρχει σε επίσημο εργαλείο σύγκρισης και είναι δημόσια. Τιμή από σήμερα εναντίον τιμής που θυμάσαι από πέρσι δεν είναι σύγκριση. Και μην παίρνεις τιμή από διαφήμιση: η διαφήμιση δείχνει την καλύτερη περίπτωση, σχεδόν πάντα υπό προϋποθέσεις.

Η τρίτη είναι η πιο απλή και η πιο ξεχασμένη: το ίδιο ακριβώς νούμερο κατανάλωσης μπαίνει στις δύο πλευρές. Δεν συγκρίνεις δύο λογαριασμούς δύο διαφορετικών μηνών ούτε δύο διαφορετικών σπιτιών — συγκρίνεις τι θα πλήρωνες εσύ, για τη δική σου κατανάλωση, με δύο διαφορετικούς κανόνες τιμολόγησης.

Και μια διευκρίνιση που μπερδεύει πολλούς: δεν συγκρίνεις εταιρείες, συγκρίνεις τιμολόγια. Ο ίδιος πάροχος έχει πολλά, με διαφορετικούς κανόνες. Ποια είναι τα τέσσερα χρώματα και τι υπόσχεται το καθένα, γιατί στο δυναμικό η απλή πράξη δεν αρκεί, τι ΔΕΝ πιάνει η πράξη — πάγιο, εκπτώσεις συνέπειας, δέσμευση, προσφορές εισαγωγής — και πώς πας από τον μήνα στον χρόνο, είναι στο πλήρες βίντεο.

## COMENTARIO FIXADO
Οι τρεις προϋποθέσεις, για να μην χαθεί καμία. ΠΡΩΤΗ, η μονάδα: ευρώ ανά κιλοβατώρα ή λεπτά ανά κιλοβατώρα — ίδιο πράγμα, νούμερο εκατό φορές διαφορετικό. Αν συγκρίνεις ευρώ με λεπτά, το αποτέλεσμα δεν είναι ανακριβές, είναι άσχετο. ΔΕΥΤΕΡΗ, η ημερομηνία: και οι δύο τιμές την ίδια ημέρα, και ΠΟΤΕ τιμή από διαφήμιση — η διαφήμιση δείχνει την καλύτερη περίπτωση υπό προϋποθέσεις. ΤΡΙΤΗ, η κατανάλωση: το ίδιο ακριβώς νούμερο στις δύο πλευρές. Και το πιο συχνό μπέρδεμα: δεν συγκρίνεις εταιρείες, συγκρίνεις τιμολόγια — ο ίδιος πάροχος έχει πολλά. Όποιος κάνει την πράξη, ας γράψει στα σχόλια μόνο αν η μονάδα του ήταν σε ευρώ ή σε λεπτά — χωρίς τιμές.

## HASHTAGS
#Ρεύμα #Τιμολόγια #ΕπόμενοΕπίπεδο

## TAGS
συγκριση τιμολογιων, τιμη κιλοβατωρας, ευρω ανα κιλοβατωρα, λεπτα ανα κιλοβατωρα, μοναδα μετρησης, λογαριασμος ρευματος, αναλυση χρεωσης, προσωπικα οικονομικα, ελλαδα, πως συγκρινω, καταναλωση, συμβαση ρευματος, επομενο επιπεδο, παροχος ρευματος, τιμολογιο

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO PRECO. Nao cita tarifa, termo fixo nem
desconto, nao nomeia fornecedor nem a autoridade reguladora, e nao diz qual cor e
mais barata. Conferido a mao campo por campo.

UNICO NUMERAL NA NARRACAO: "εκατό φορές". NAO e numero sobre o mundo — e a razao
entre euro e centimo, definicao de unidade, que nao muda nunca. E ela e o
conteudo da peca.

A REGRA (g) MANDA o resto para fora: tarifa, termo fixo e desconto mudam por
oferta e por mes. O short fica com as tres CONDICOES da comparacao.

O QUE O VIDEO AFIRMA: que o preco por kilowatt-hora aparece em euro ou em
centimos, e que as duas escritas diferem por fator cem para o mesmo preco; que as
duas tarifas comparadas tem de ser lidas na MESMA data, e nunca de publicidade;
e que o MESMO numero de consumo entra nos dois lados. Esta no longo
epomeno-epipedo-012 (wUHuwyO2HYo), capitulo "Οι τιμές", itens "Πρόσεξε τη
μονάδα", "Πάρε την ίδια ημερομηνία" e "Το ίδιο νούμερο, δύο φορές".

DESCARTADO, e vai escrito:
  (1) todos os precos e o termo fixo — mudam por oferta e por mes;
  (2) o nome da ferramenta oficial e da autoridade, NAO reconferidos nesta rodada;
  (3) as outras cinco armadilhas do capitulo "Τι δεν πιάνει η πράξη" — sao OUTRA
      peca e nao se empilham aqui.

## FONTES
O longo de onde este short foi extraido (epomeno-epipedo-012, wUHuwyO2HYo) traz
as fontes. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s014",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#12263A", "c1": "#2A9D8F", "c2": "#E8A33D",
               "bg": "#F5F2EC"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "wUHuwyO2HYo",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short, alvo_short
    grava(SPEC, "fabrica/specs/epomeno-epipedo-s014.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    tam = [len(c["nar"]) for c in SHORT]
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | short: {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} (TOPO: centro el ~ -2,9%)")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto (el) "
          f"{s*0.944:.1f} a {s*0.998:.1f}")
    print(f"narracao: media {sum(tam)/len(tam):.0f}, menor {min(tam)}, maior {max(tam)}")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
    print(f"aponta para: {SPEC['longo_existente']}")
