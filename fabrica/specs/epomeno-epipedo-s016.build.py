"""epomeno-epipedo-s016 — ο φόρος πάει στον μεγαλύτερο των δύο.

ALAVANCA desta rodada: o esqueleto de DEZ CENAS no epomeno, fechando os tres
canais no braco do experimento 40. NUMERO DE PARTIDA: no epomeno o braco de dez
cenas tem n=0 — as cinco pecas de hoje no canal sao de CINCO cenas.
Nada mais muda: mesma voz, topo da faixa (que e seguro no grego, centro -3,2%),
titulo em imperativo de segunda pessoa, que e a forma do GR/26.

O QUE DEU CERTO: o `labtreinamento-s012` subiu com dez cenas e 42,07 s reais
(-1,0% sobre o estimado), e o braco de dez cenas agora tem tres canais.

O QUE NAO DEU, e e um achado sobre o instrumento: a REPLICA ATRASADA pode cair
em QUALQUER das tres leituras. O 688 mediu "todas as seis subiram na terceira" e
eu quase virei isso em regra de ORDEM; nesta rodada a leitura do MEIO foi a velha
em sete pecas de dois canais — 349/345/349, 120/118/120, 115/113/115, 77/76/77,
53/46/53, 14/13/14, 9/8/9 — e os valores do meio sao exatamente os pisos de uma
hora antes. O que sobrevive e so o MAXIMO como PISO; a ordem nao diz nada.
Aprendizado 696.

O QUE VOU MUDAR: o esqueleto, e nada mais.

DE ONDE SAI: longo `h66MCKjwAJ8` (o tekmarto eisodima — a renda que o Estado
PRESUME), capitulos da propria descricao publicada: a mudanca e a fonte dela, a
habitacao, o automovel e "a sua conta em tres passos". **Origem SEM spec local**,
pacote anterior a convencao atual — capitulos lidos pela `videos.list`, como a
regra (h) manda. Terceira vez hoje, e e o caso normal e nao a excecao.

FAMILIA DIFERENTE das cinco pecas de hoje no canal, como a regra (f) exige: o
`s011` era "leia a linha no seu documento", o `s013` era ORDEM (juros do mais
caro primeiro), o `s014` era UNIDADE, o `s015` era RETORNO (em quantos anos
volta). Esta e **MAIOR DOS DOIS** — a entrada errada nao e a conta de nenhum dos
dois numeros, e supor que existe UM: o imposto se calcula sobre o MAIOR entre o
declarado e o presumido, e o presumido nao pergunta quanto voce ganhou.

FEED GR NAO RELIDO nesta rodada — lido as 11:1x, seis horas, fora da janela de
quatro horas e meia do 623, e vai dito que nao foi relido.

IDENTIDADE: faixa ATUAL do canal, trilha do canal (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita valor por
# metro quadrado, nao cita faixa de metragem, nao cita percentual de reducao, nao
# cita gramas de emissao, nao cita cilindrada, nao cita o piso minimo, nao cita
# numero de lei, de FEK nem de artigo, nao cita ano fiscal e nao cita a data de
# corte do registro do veiculo. Conferido A MAO campo por campo, porque o portao
# `narracao` conta QUANTIDADES por frase e NAO pega digito cru.
#
# A REGRA (g) MANDA, e aqui ela e quase o tema: a descricao do longo e feita de
# numeros com data colada — a tabela inteira foi reduzida neste ciclo, por lei
# deste ano, com efeito no ano fiscal anterior. TUDO isso envelhece, e envelhece
# junto. Citar qualquer valor desses seria publicar hoje um short que fica errado
# na proxima reforma.
#
# O QUE NAO ENVELHECE, e e o que a peca carrega: existem DOIS numeros, o
# declarado e o presumido; o presumido nao pergunta quanto voce ganhou, e sim
# onde voce mora e o que voce dirige; ele se le nos seus proprios documentos; e o
# imposto se calcula sobre o MAIOR dos dois, na diferenca.
#
# NUMERAIS NA NARRACAO: "deuteros" e "ton dyo" — segundo e dos dois, que
# descrevem a ESTRUTURA do calculo e nao um valor do mundo. Uma quantidade por
# frase; o limite do portao e tres.
#
# O QUE FOI DESCARTADO, e vai escrito:
#   (1) a tabela de habitacao e as proporcoes de zona — mudaram neste ciclo;
#   (2) os limiares de emissao e de cilindrada e os valores por grama — idem, e
#       dependem da data de registro do veiculo;
#   (3) o piso minimo e a isencao dos dependentes com renda propria — numeros de
#       vigencia;
#   (4) a data de corte do registro do veiculo, que decide QUAL das duas tabelas
#       se aplica: e vigencia, e o short diz em vez disso que o numero esta no
#       proprio documento do carro.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Δήλωσες", "sub": "και περιμένεις τον φόρο", "nar": "Δήλωσες το εισόδημά σου και περιμένεις ήσυχος τον φόρο.", "sem_cap": True},
    {"layout": "item", "kicker": "Όμως", "preco": "δεύτερος αριθμός", "nar": "Υπάρχει όμως και ένας δεύτερος αριθμός εκεί.", "sem_cap": True},
    {"layout": "item", "kicker": "Το τεκμαρτό", "preco": "άλλη ερώτηση", "nar": "Λέγεται τεκμαρτό, και δεν ρωτά καθόλου πόσα βγάζεις.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Ρωτά", "sub": "πού μένεις, τι οδηγείς", "nar": "Ρωτά σε πόσα τετραγωνικά μένεις και τι οδηγείς.", "sem_cap": True},
    {"layout": "item", "kicker": "Η κατοικία", "preco": "τα τετραγωνικά", "nar": "Βγαίνει από τα τετραγωνικά της κύριας κατοικίας σου.", "sem_cap": True},
    {"layout": "item", "kicker": "Το όχημα", "preco": "από την άδεια", "nar": "Και από τον αριθμό στην άδεια του αυτοκινήτου.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Ο φόρος", "sub": "στον μεγαλύτερο", "nar": "Και ο φόρος πάει πάντα στον μεγαλύτερο των δύο.", "sem_cap": True},
    {"layout": "item", "kicker": "Αν υπερβεί", "preco": "το δηλωμένο", "nar": "Αν το τεκμαρτό υπερβεί το δηλωμένο εισόδημα,", "sem_cap": True},
    {"layout": "item", "kicker": "Τότε", "preco": "στη διαφορά", "nar": "τότε πληρώνεις τον φόρο πάνω στη διαφορά.", "sem_cap": True},
    {"layout": "cta", "kicker": "Κάνε εγγραφή", "sub": "για το επόμενο", "nar": "Υπολόγισέ το μόνος πριν δηλώσεις. Κάνε εγγραφή.", "sem_cap": True}
]

THUMB = {"l1": "Δύο αριθμοί", "l2": "ένας φόρος"}

COPY = """# epomeno-epipedo-s016

## TITULO
Υπολόγισε Το Τεκμαρτό Σου Πριν Δηλώσεις: Ο Φόρος Πάει Στον Μεγαλύτερο Των Δύο Αριθμών

## TITULO SHORT
Υπολόγισε το τεκμαρτό σου

## DESCRICAO
Οι περισσότεροι περιμένουν τον φόρο κοιτώντας έναν αριθμό: το εισόδημα που δήλωσαν. Υπάρχει όμως και δεύτερος, και δεν ρωτά πόσα βγάλατε.

Λέγεται **τεκμαρτό εισόδημα** και βγαίνει από πράγματα που έχετε, όχι από πράγματα που κερδίσατε: τα τετραγωνικά της κατοικίας και το αυτοκίνητο — ο αριθμός του οποίου είναι γραμμένος στην ίδια την άδεια. Το ουσιώδες είναι η σύγκριση: ο φόρος δεν υπολογίζεται στο δηλωμένο ούτε στο τεκμαρτό, αλλά στον **μεγαλύτερο των δύο**. Αν το τεκμαρτό βγει μεγαλύτερο, πληρώνετε πάνω στη διαφορά.

Αυτό αλλάζει τη σειρά των ενεργειών. Το τεκμήριο δεν μειώνεται δηλώνοντας λιγότερα — μειώνεται μόνο αν αλλάξουν τα δικά του δεδομένα, δηλαδή η κατοικία και το όχημα. Και επειδή είναι σύγκριση και όχι άθροισμα, αξίζει να το υπολογίσετε **πριν** υποβάλετε, όχι αφού δείτε το αποτέλεσμα: μετά δεν υπάρχει τίποτα να διορθώσετε.

Σε αυτό το short δεν υπάρχει ούτε ένας αριθμός, και είναι σκόπιμο. Οι συντελεστές, οι κλίμακες, τα όρια εκπομπών και τα κυβικά άλλαξαν σε αυτόν τον κύκλο, ισχύουν με ημερομηνία και θα ξανααλλάξουν — ενώ ο κανόνας «δύο αριθμοί, πληρώνεις στον μεγαλύτερο» δεν αλλάζει. Για τον ίδιο λόγο δεν αναφέρουμε ποια ημερομηνία ταξινόμησης κρίνει ποιον πίνακα χρησιμοποιεί το όχημά σας: ο αριθμός που μετράει είναι στο έγγραφο που έχετε στο χέρι.

Ολόκληρος ο πίνακας, η πηγή της αλλαγής και ο υπολογισμός σε τρία βήματα, με χαρτί και στυλό, είναι στο πλήρες βίντεο του καναλιού.

## COMENTARIO FIXADO
Το λάθος εδώ δεν είναι στην αριθμητική, είναι στην υπόθεση ότι υπάρχει ΕΝΑΣ αριθμός. Υπάρχουν δύο — το δηλωμένο και το τεκμαρτό — και ο φόρος πάει στον μεγαλύτερο, στη διαφορά. Γι' αυτό το τεκμήριο δεν μειώνεται δηλώνοντας λιγότερα: μειώνεται μόνο αν αλλάξουν τα δεδομένα του, η κατοικία και το όχημα. Να είμαστε δίκαιοι με όσους εκπλήσσονται: δεν είναι απροσεξία, είναι ότι ο δεύτερος αριθμός δεν φαίνεται πουθενά μέχρι να βγει μεγαλύτερος. Σκόπιμα δεν έβαλα ούτε έναν συντελεστή εδώ — οι κλίμακες και τα όρια άλλαξαν σε αυτόν τον κύκλο και θα ξανααλλάξουν, ο κανόνας όχι. Όποιος το υπολόγισε με χαρτί, γράψτε στα σχόλια μόνο αν το τεκμαρτό βγήκε μεγαλύτερο ή μικρότερο — χωρίς ποσά.

## HASHTAGS
#Τεκμήρια #Φορολογία #ΕπόμενοΕπίπεδο

## TAGS
tekmarto eisodima, tekmiria diaviosis, forologiki dilosi, antikeimeniki dapani, megalytero ton dyo, texnika tekmiria, katoikia tetragonika, adeia aftokinitou, forologia eisodimatos, ypologismos tekmiriou, dilosi eisodimatos, epomeno epipedo, oikonomika, forotechnika, diafora forou

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
ZERO NUMERO NOVO SOBRE O MUNDO, e ZERO DIGITO NA NARRACAO. Nao cita valor por
metro quadrado, faixa de metragem, percentual de reducao, gramas de emissao,
cilindrada, piso minimo, numero de lei, de FEK ou de artigo, ano fiscal nem a
data de corte do registro do veiculo. Conferido a mao campo por campo.

A REGRA (g) MANDA, e aqui ela e quase o tema: a descricao do longo e feita de
numeros com data colada, e a tabela inteira foi reduzida neste ciclo. Citar
qualquer um deles seria publicar um short que fica errado na proxima reforma.

O QUE NAO ENVELHECE, e e o que a peca carrega: existem DOIS numeros, o declarado
e o presumido; o presumido nao pergunta quanto voce ganhou, e sim onde mora e o
que dirige; le-se nos proprios documentos; e o imposto vai sobre o MAIOR dos
dois, na diferenca.

NUMERAIS NA NARRACAO: "deuteros" e "ton dyo", que descrevem a estrutura do
calculo.

DESCARTADO, e vai escrito:
  (1) tabela de habitacao e proporcoes de zona;
  (2) limiares de emissao e cilindrada e valores por grama;
  (3) piso minimo e isencao de dependentes com renda propria;
  (4) a data de corte do registro, que decide qual tabela se aplica — o short diz
      em vez disso que o numero esta no documento do proprio carro.

## FONTES
O longo de onde este short foi extraido (h66MCKjwAJ8) traz a lei, o FEK, o artigo
do KFE e a tabela com as datas. Este short nao introduz numero novo sobre o mundo.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s016",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "h66MCKjwAJ8",
    "copy": COPY,
}

if __name__ == "__main__":
    import json
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    # paleta e trilha ATUAIS do canal, lidas da ultima spec dele (601)
    ant = json.load(open("fabrica/specs/epomeno-epipedo-s015.json", encoding="utf-8"))
    SPEC["paleta"] = ant["paleta"]
    SPEC["trilha"] = ant["trilha"]
    from grava_spec import grava
    from ensaio import duracao_estimada_short, alvo_short
    import legenda as LG
    import variedade
    grava(SPEC, "fabrica/specs/epomeno-epipedo-s016.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short()
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | {len(SHORT)} cenas | paleta {SPEC['paleta']} "
          f"| trilha {SPEC['trilha']}")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} | TOPO no el")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'} | real previsto "
          f"{s*0.957:.1f} a {s*0.999:.1f}")
    print(f"por plano: {s/len(SHORT):.2f}s | falas de legenda: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
