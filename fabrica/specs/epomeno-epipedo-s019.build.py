"""epomeno-epipedo-s019 — A SOMA DOS PEQUENOS. O que nenhum papel te manda.

ALAVANCA: nenhuma mudanca de forma. Onze cenas, uma frase curta por cena, mira
do canal. Braco de dez-a-onze cenas no epomeno, n=3 antes desta.

DE ONDE SAI: longo `GwNkPfM9pSY`, "Το σύστημα 6 μηνών ... με μισθό 900€", de
12/08. **Sem spec no repositorio**, e um caso mais duro que o anterior: a
descricao dele nao tem capitulo NENHUM — sao 600 caracteres de resumo. O texto
saiu inteiro da faixa de legenda (dezesseis blocos), pelo `capitulos_do_longo.py`
com `legenda=true`.
E ISSO SO FUNCIONOU DEPOIS DE UM CONSERTO, nesta mesma rodada: o ramo "nenhum
capitulo marcado" tinha um `return 0` antes da leitura da legenda, entao o
instrumento falhava exatamente no caso que ele existe para resolver.

FAMILIA NOVA: **A SOMA DOS PEQUENOS**. Cada parcelinha parece desprezivel
isolada, e a pessoa as julga UMA A UMA porque e assim que elas aparecem. O
agregado nunca chega num papel so. Ja usadas: LIMIAR, COMPOSICAO, ORDEM,
DEFASAGEM NO TEMPO, ARITMETICA media-contra-produto, CONDICAO/ACAO e MARGINAL
contra TOTAL. Esta e a oitava, e a regra (f) e respeitada: o epomeno teve hoje
CONDICAO/ACAO (s017) e MARGINAL contra TOTAL (s018), familias diferentes desta.

POR QUE ELA VALE UM SHORT, e nao e estetica: a entrada errada aqui nao e de
conta, e de UNIDADE DE OBSERVACAO. Quem soma acerta a aritmetica; quem olha
parcela por parcela nem chega a fazer a conta. O proprio longo nomeia o
mecanismo — "αόρατα αγκίστρια" — e diz que o conjunto delas retira mais do que
qualquer uma sugere.

TITULO: imperativo de segunda pessoa, a forma medida do GR (09/10).
FEED GR NAO LIDO nesta rodada, e isso vai dito.

IDENTIDADE: faixa ATUAL do canal, trilha `Inspired` (601).

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# A REGRA (g) tira TUDO deste longo, e ele e quase todo numero: o salario de
# referencia, a reparticao 675/175/50, os 180 dias, os seis meses, o saldo e a
# taxa de cada divida do exemplo, a parcela mensal, os 300 de liquidez extra, os
# 40 por semana de mercado, os 30 de troca de fornecedor, a parcela que sobe
# para 205, as 10 horas e os 150 a 200 de trabalho extra, os 60% no quarto mes,
# os tres salarios de reserva e os 2.700 do fundo. Todos sao do exemplo ou
# mudam com preco, taxa e salario.
#
# O QUE A PECA CARREGA, e nao envelhece: varias obrigacoes pequenas somam uma
# grande, e a pessoa as avalia UMA A UMA porque e assim que elas chegam —
# nenhum documento mostra o agregado. Logo a primeira acao nao e pagar, e
# LISTAR. Isso e aritmetica e unidade de observacao, nao tabela.
#
# ZERO DIGITO e ZERO NUMERAL na narracao, conferido campo a campo. Em especial
# NAO digo quantas parcelas sao nem quanto somam — seria inventar numero, porque
# o longo da isso como exemplo e nao como regra. "πολλές μικρές" e "μία μία"
# descrevem a forma, nao a quantidade.
#
# E EU NAO LEVEI o capitulo mais forte do longo, de proposito: a consolidacao de
# dividas que "so funciona se voce cancelar os cartoes e NAO esticar o prazo".
# Ele e bom e e regra, mas carregar isso em quarenta segundos sem taxa e sem
# prazo viraria conselho de credito sem conta — e fica perto demais do
# MARGINAL contra TOTAL que o mesmo canal publicou hoje. Fica para outra peca,
# em outro dia, e vai escrito aqui para a proxima rodada achar.
#
# =============================================================================
"""

CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Νομίζεις", "sub": "πως δεν έχεις χρέος", "nar": "Νομίζεις πως δεν έχεις κανένα χρέος.", "sem_cap": True},
    {"layout": "item", "kicker": "Έχεις όμως", "preco": "πολλές μικρές", "nar": "Έχεις όμως πολλές μικρές δόσεις ανοιχτές.", "sem_cap": True},
    {"layout": "item", "kicker": "Καμία", "preco": "δεν φαίνεται βάρος", "nar": "Καμία τους δεν φαίνεται πραγματικό βάρος μόνη της.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Εδώ είναι", "sub": "όλο το κόλπο", "nar": "Και εδώ κρύβεται ακριβώς όλο το κόλπο.", "sem_cap": True},
    {"layout": "item", "kicker": "Τις κρίνεις", "preco": "μία μία", "nar": "Τις κρίνεις μία μία, γιατί έτσι ακριβώς έρχονται.", "sem_cap": True},
    {"layout": "item", "kicker": "Μαζί όμως", "preco": "μία δόση μεγάλη", "nar": "Μαζί όμως κάνουν μία δόση αρκετά μεγάλη.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Το άθροισμα", "sub": "δεν σου έρχεται ποτέ", "nar": "Το άθροισμα δεν σου έρχεται σε κανένα χαρτί.", "sem_cap": True},
    {"layout": "item", "kicker": "Άρα", "preco": "μένει αόρατο", "nar": "Έτσι το ποσό μένει αόρατο για μήνες ολόκληρους.", "sem_cap": True},
    {"layout": "item", "kicker": "Η πρώτη κίνηση", "preco": "δεν είναι να πληρώσεις", "nar": "Γι αυτό η πρώτη κίνηση δεν είναι να πληρώσεις.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Γράψ' τις", "sub": "όλες σε μία λίστα", "nar": "Γράψε τις όλες μαζί σε μία λίστα, σήμερα.", "sem_cap": True},
    {"layout": "cta", "kicker": "Επόμενο Επίπεδο", "sub": "κάνε εγγραφή", "nar": "Αν σου άνοιξε τα μάτια, κάνε εγγραφή.", "sem_cap": True}
]

THUMB = {"l1": "Μία μία", "l2": "μικρές"}

COPY = """# epomeno-epipedo-s019

## TITULO
Γράψε Τις Όλες Σε Μία Λίστα: Οι Μικρές Δόσεις Κρίνονται Χωριστά Και Πληρώνονται Μαζί

## TITULO SHORT
Γράψε τις όλες σε μία λίστα

## DESCRICAO
Υπάρχει ένα είδος χρέους που οι άνθρωποι ειλικρινά δεν θεωρούν χρέος: οι πολλές μικρές δόσεις. Μια συσκευή σε άτοκες δόσεις, μια συνδρομή, ένα «πλήρωσε αργότερα» στο ταμείο, ένα μικροδάνειο που τελειώνει «σε λίγους μήνες».

Ο λόγος που περνούν απαρατήρητες δεν είναι η αμέλεια — είναι η **μονάδα παρατήρησης**. Κάθε μία εμφανίζεται χωριστά: χωριστή ημερομηνία, χωριστό ποσό, χωριστό μήνυμα. Έτσι την κρίνεις χωριστά, και χωριστά κάθε μία είναι πράγματι αμελητέα.

Μαζί δεν είναι. Μαζί συνθέτουν μία δόση μεγάλη, που θα την αναγνώριζες αμέσως ως βάρος αν σου εμφανιζόταν σε μία γραμμή. **Και δεν σου εμφανίζεται ποτέ σε μία γραμμή:** κανένα έγγραφο, από κανέναν πάροχο, δεν υπολογίζει το άθροισμα των υποχρεώσεών σου προς τρίτους. Γι' αυτό το ποσό μένει αόρατο για μήνες — όχι επειδή κρύβεται, αλλά επειδή κανείς δεν έχει λόγο να το συγκεντρώσει.

Από αυτό βγαίνει η πρώτη κίνηση, και δεν είναι να πληρώσεις: είναι να **καταγράψεις**. Μία λίστα, όλες μαζί, με ποσό και ημερομηνία. Η αριθμητική μετά είναι εύκολη· το δύσκολο ήταν να δεις το σύνολο.

Αυτό το short δεν αναφέρει επίτηδες ούτε πόσες δόσεις, ούτε ποσά, ούτε επιτόκια, ούτε μισθό: όλα αυτά είναι του παραδείγματος ή αλλάζουν. Αυτό που δεν αλλάζει είναι ότι πολλές μικρές υποχρεώσεις κρίνονται χωριστά και πληρώνονται μαζί.

Στο πλήρες βίντεο: η αυστηρή κατανομή του εισοδήματος, η σειρά με την οποία πεθαίνουν τα χρέη, η αυτοματοποίηση των πληρωμών, η διαπραγμάτευση με την τράπεζα, και γιατί η συγκέντρωση χρεών μπορεί να σε βλάψει αν επιμηκύνει τη διάρκεια.

## COMENTARIO FIXADO
Το ύπουλο εδώ δεν είναι το επιτόκιο, είναι η μονάδα παρατήρησης: κάθε μικρή δόση φτάνει χωριστά — χωριστή ημερομηνία, χωριστό μήνυμα — άρα την κρίνεις χωριστά, και χωριστά είναι πράγματι αμελητέα. Το άθροισμα δεν σου έρχεται ποτέ σε μία γραμμή, γιατί κανένας πάροχος δεν έχει λόγο να υπολογίσει τι χρωστάς σε όλους τους άλλους. Δεν κρύβεται· απλώς δεν συγκεντρώνεται από κανέναν εκτός από εσένα. Γι' αυτό η πρώτη κίνηση είναι καταγραφή και όχι πληρωμή: η αριθμητική μετά είναι εύκολη. Επίτηδες δεν έβαλα ούτε πόσες δόσεις ούτε ποσά — αυτά είναι του παραδείγματος, και είναι στο βίντεο. Γράψτε πόσες ανοιχτές δόσεις βρήκατε όταν τις βάλατε σε μία λίστα· νομίζω ότι ο αριθμός θα εκπλήξει κι εσάς.

## HASHTAGS
#Χρέη #Οικονομικά #ΕπόμενοΕπίπεδο

## TAGS
mikres doseis, atokes doseis, buy now pay later, syndromes, aorata chrei, lista chreon, katagrafi ypochreoseon, diacheirisi chreous, oikonomika nikokyriou, methodos chionostivadas, epomeno epipedo, mikrodaneia, pistotiki karta, prosopikos proypologismos, monada paratirisis

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
ZERO NUMERO NOVO SOBRE O MUNDO, ZERO DIGITO e ZERO NUMERAL na narracao.
Conferido campo a campo. Em especial NAO digo quantas parcelas sao nem quanto
somam: seria inventar numero, porque o longo da isso como EXEMPLO e nao como
regra. "πολλές μικρές" e "μία μία" descrevem a forma, nao a quantidade.

A REGRA (g) tira tudo, e este longo e quase todo numero: o salario de
referencia, a reparticao 675/175/50, os 180 dias, os seis meses, o saldo e a
taxa de cada divida do exemplo, a parcela mensal, os 300 de liquidez extra, os
40 por semana de mercado, os 30 da troca de fornecedor, a parcela que sobe para
205, as 10 horas e os 150 a 200 de trabalho extra, os 60% no quarto mes, os tres
salarios de reserva e os 2.700 do fundo.

O QUE A PECA CARREGA, e nao envelhece: varias obrigacoes pequenas somam uma
grande, e a pessoa as avalia UMA A UMA porque e assim que elas chegam. Nenhum
documento mostra o agregado — nao porque esteja escondido, mas porque nenhum
fornecedor tem motivo para somar o que voce deve aos outros. Logo a primeira
acao e LISTAR, nao pagar. O proprio longo nomeia o mecanismo: "αόρατα
αγκίστρια".

O QUE EU NAO LEVEI, de proposito, e vai escrito para a proxima rodada achar: o
capitulo da consolidacao de dividas, que "so funciona se voce cancelar os
cartoes e NAO esticar o prazo". E bom e e regra, mas em quarenta segundos sem
taxa e sem prazo viraria conselho de credito sem conta — e fica perto demais do
MARGINAL contra TOTAL que este mesmo canal publicou hoje.

## FONTES
O longo de onde este short foi extraido (`GwNkPfM9pSY`, de 12/08) carrega os
numeros do exemplo. Este short NAO introduz numero novo sobre o mundo, entao nao
exige fonte institucional nova.

NOTA DE PROCEDENCIA: o longo NAO tem spec no repositorio e **a descricao dele nao
tem capitulo nenhum** — sao 600 caracteres de resumo. O texto saiu inteiro da
faixa de legenda que a propria maquina subiu, em dezesseis blocos, pelo
`capitulos_do_longo.py` com `legenda=true`. Nenhuma frase desta peca foi
inferida de resumo nem de titulo.
"""

SPEC = {
    "slug": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s019",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#16283C", "c1": "#2E7BB4", "c2": "#E0A02E",
               "bg": "#F3F7FA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "longo_existente": "GwNkPfM9pSY",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short, alvo_short
    import legenda as LG
    import variedade
    grava(SPEC, "fabrica/specs/epomeno-epipedo-s019.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    lo, hi = alvo_short(SPEC["slug"])
    tit = COPY.split("## TITULO SHORT\n")[1].split("\n")[0]
    print(f"SHORT SOLTO | {len(SHORT)} cenas")
    print(f"estimativa: {s:.1f}s | ALVO {lo}-{hi} | TOPO no grego")
    print(f"na mira? {'SIM' if lo <= s <= hi else 'NAO'}")
    print(f"por plano: {s/len(SHORT):.2f}s | falas: "
          f"{sum(len(LG.pedacos(c['nar'])) for c in SHORT)}")
    print(f"gancho: {len(variedade.primeira_frase(SHORT[0]['nar']).split())} palavras")
    print(f"thumb: {len((THUMB['l1'] + ' ' + THUMB['l2']).split())} palavras")
    print(f"titulo: {tit!r} ({len(tit)} chars)")
