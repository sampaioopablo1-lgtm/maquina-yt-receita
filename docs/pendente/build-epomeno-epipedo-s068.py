# -*- coding: utf-8 -*-
"""epomeno-epipedo-s068 — SEGUNDO angulo do longo publicado hoje.

PAUTA: origem `pqTc8jBrq0E` (o longo `epomeno-epipedo-068`, publicado as 12:58Z),
que o contador da como rank 1 do canal e com ZERO shorts declarados. O short que
saiu NO pacote usou a familia do DENOMINADOR (os pagios do mes); este usa outra,
dos capitulos 48 a 55: o ALVO em meses, e a assimetria entre o primeiro e o
decimo mes.

FAMILIA DE ENTRADA ERRADA (nova no canal): tomar o numero de meses que alguem
disse, em vez de o derivar do proprio setor — e perseguir o decimo mes quando o
primeiro e o que muda tudo.

ORCAMENTO: `mira.orcamento` com o acessor consertado nesta rodada da 53
caracteres por cena para 10 cenas no PISO (41,5) da faixa da frota. Mirar o PISO
e a regra de redacao do 772, e neste canal ela vai com a ressalva do 18/10: o
piso NAO reduz o real, aumenta a chance de residuo NEGATIVO.
"""
import json
import os

RAIZ = "/home/user/maquina-yt-receita"
PAC = "epomeno-epipedo-s068"

SHORT = [
    dict(layout="titulo", kicker="Πόσοι μήνες αρκούν", sub="όχι από άλλον",
         nar="Πόσοι μήνες αρκούν δεν απαντιέται από κανέναν."),
    dict(layout="item", kicker="Το νούμερο που άκουσες", preco="απαντάει αλλού",
         nar="Το νούμερο που άκουσες απαντάει στα δικά του πάγια."),
    dict(layout="lista", kicker="Τι ανεβάζει τον στόχο",
         itens=["Ένα εισόδημα στο σπίτι", "Κλάδος που αργεί",
                "Δουλειά με εποχή", "Νέα θέση"],
         nar="Τέσσερα πράγματα ανεβάζουν τον στόχο, όχι ο μισθός."),
    dict(layout="item", kicker="Κανένα δεν κοιτά", preco="πόσα βγάζεις",
         nar="Κανένα από τα τέσσερα δεν κοιτά πόσα βγάζεις εσύ."),
    dict(layout="barras", kicker="Τι κερδίζει κάθε μήνας",
         barras=[{"rotulo": "Πρώτος", "valor": 10},
                 {"rotulo": "Τρίτος", "valor": 5},
                 {"rotulo": "Δέκατος", "valor": 1}],
         nar="Ο πρώτος μήνας αλλάζει περισσότερα από τον δέκατο."),
    dict(layout="titulo", kicker="Ο δέκατος μήνας", sub="δίνει πολύ λίγο",
         nar="Από τους εννιά μήνες στους δέκα κερδίζεις λίγα."),
    dict(layout="item", kicker="Η ερώτηση που μετρά", preco="πόσο αργεί ο κλάδος",
         nar="Ρώτα πόσο αργεί στον κλάδο σου να βρεθεί αντίστοιχη θέση."),
    dict(layout="item", kicker="Δύο εισοδήματα", preco="κατεβάζουν τον στόχο",
         nar="Δύο εισοδήματα στο ίδιο σπίτι κατεβάζουν τον στόχο."),
    dict(layout="item", kicker="Πρώτα η μέτρηση", preco="μετά ο στόχος",
         nar="Πρώτα μέτρα πού είσαι, και μετά βάλε τον στόχο σου."),
    dict(layout="cta", kicker="Γράψε τον στόχο σου", sub="σε μήνες",
         nar="Γράψε από κάτω τον στόχο σου σε μήνες, χωρίς ευρώ."),
]

COPY = """# epomeno-epipedo-s068

## TITULO
Πόσοι Μήνες Αρκούν: Ο Στόχος Βγαίνει από τον Κλάδο Σου, Όχι από Συμβουλή

## TITULO SHORT
Ο στόχος δεν δανείζεται

## DESCRICAO
Κάποιος σου είπε έναν αριθμό μηνών. **Και ο αριθμός του απαντάει στα δικά του πάγια, όχι στα δικά σου.**

Ο στόχος δεν δανείζεται, γιατί δεν είναι ποσό: είναι απάντηση σε μια ερώτηση που είναι δική σου. Η ερώτηση είναι πόσο αργεί, στον δικό σου κλάδο, να βρεθεί κάτι αντίστοιχο. Όσο πιο αργά κινείται ο κλάδος, τόσο πιο ψηλά ο στόχος, και αυτό δεν είναι αισιοδοξία ή απαισιοδοξία — είναι χρόνος.

**Τέσσερα πράγματα ανεβάζουν τον στόχο, και κανένα από τα τέσσερα δεν κοιτά πόσα βγάζεις:** ένα μόνο εισόδημα στο σπίτι, κλάδος που αργεί, δουλειά με εποχικότητα, και θέση που είναι νέα. Αντίστροφα, δύο εισοδήματα στο ίδιο σπίτι κατεβάζουν τον στόχο, γιατί δύσκολα σταματούν και τα δύο την ίδια στιγμή.

Και υπάρχει μια ασυμμετρία που αλλάζει τη σειρά των πραγμάτων. **Από τον ένα μήνα στους δύο κερδίζεις ησυχία. Από τους εννιά στους δέκα κερδίζεις πολύ λίγα.** Το ίδιο ευρώ δεν αγοράζει το ίδιο πράγμα σε κάθε σημείο της διαδρομής, και γι' αυτό ο πρώτος μήνας είναι αυτός που αλλάζει τα περισσότερα.

Από εκεί βγαίνει και η σειρά: **πρώτα μετράς πού είσαι σήμερα, και μετά βάζεις στόχο** — όχι το αντίστροφο. Στόχος που μπήκε πριν από τη μέτρηση είναι ευχή, και ευχή δεν έχει διαιρέτη.

Κανένα νούμερο δικό μου δεν μπαίνει εδώ: ούτε μήνες, ούτε ποσοστά, ούτε μέσος όρος αγοράς. Όλα βγαίνουν από τη δική σου λίστα.

## COMENTARIO FIXADO
Γράψε εδώ κάτω ένα μόνο πράγμα: πόσους μήνες έβγαλες ως στόχο. Χωρίς ποσά και χωρίς όνομα εταιρείας.

## HASHTAGS
#ΟικονομικάΠροσωπικά #Αποθεματικό #ΕπόμενοΕπίπεδο

## TAGS
αποθεματικό, πόσοι μήνες, στόχος αποθεματικού, πάγια έξοδα, κλάδος, δύο εισοδήματα, προσωπικά οικονομικά, κάνε την πράξη, μήνες αντοχής

## CONFIGURACOES DO STUDIO
- Idioma: Grego (el) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Licenca padrao do YouTube

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este short NAO cita nenhum numero meu e NAO faz afirmacao institucional nenhuma.
Nao cita quantos meses sao suficientes, nao cita percentual, nao cita media de
mercado e nao cita prazo de recolocacao. Os quatro fatores que sobem o alvo e os
dois que o descem saem do longo `pqTc8jBrq0E` deste canal, e o alvo em meses sai
da propria situacao de quem assiste. Classe PROCEDIMENTO: a trava de duas fontes
institucionais (600) vale para numero sobre o MUNDO que muda, e aqui nao existe
nenhum. DELIBERADAMENTE DE FORA: qualquer numero de meses como recomendacao, e
qualquer prazo medio de recolocacao por setor.

## FONTES
Origem: `pqTc8jBrq0E` (`epomeno-epipedo-068`, publicado em 19/10/2026 as 12:58Z,
64 cenas de longo). Familia de entrada errada: tomar o alvo em meses de outra
pessoa, e perseguir o decimo mes em vez do primeiro. Capitulos 48 a 55 do longo.
O short que saiu NO pacote usou outra familia — a do DENOMINADOR (os pagios do
mes) —, logo este e SEGUNDO ANGULO e nao repeticao.

## EXPOSICAO
Mirado no PISO da faixa da frota, pela regra de redacao do 772: previsao edge
**41,71** e piper **36,95**. O orcamento do `mira.orcamento` deu **49**
caracteres por cena para o piso e 51 para o meio, e a peca saiu com media 50 —
a primeira peca escrita com o orcamento cobrindo ESTE canal, porque ate as
15:1x ele devolvia `None` fora do labtreinamento, e a primeira em que ele mira
a PREVISAO REAL em vez da estimativa (as duas diferem 1,94 s, que e o fator do
provedor; a versao anterior desta mesma spec saiu 0,4 s ACIMA do topo por isso).
Se o edge narrar, o REAL deve cair entre **40,5 e 45,7 s** pela banda OBSERVADA
(-1,2 a 4,0; n=120), logo PODE encostar no teto de 45 do portao.
E a ressalva deste canal vai declarada: mirar o piso aqui NAO reduz o real — os
cinco residuos negativos da serie sao todos do epomeno e todos com real
exatamente 41 —, o que o piso faz e aumentar a chance de o residuo sair NEGATIVO.
"""

sp = {
    "slug": PAC,
    "pacote": PAC,
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "longo_existente": "pqTc8jBrq0E",
    "longo": [],
    "short": SHORT,
    "thumb": {"l1": "Πόσοι μήνες", "l2": "αρκούν"},
    "paleta": {"bg": "#F4EFE6", "ink": "#1B1A17", "c1": "#C8502A",
               "c2": "#2B6CB0", "red": "#B83227", "ok": "#2E8B57",
               "panel": "#FFFFFF", "mut": "#7A7263", "acc": "#C8502A"},
    "copy": COPY,
}

alvo = os.path.join(RAIZ, "fabrica", "specs", PAC + ".json")
with open(alvo, "w", encoding="utf-8") as fh:
    json.dump(sp, fh, ensure_ascii=False, indent=1)
print("spec gravada:", alvo)
print("cenas:", len(SHORT), "| media de chars:",
      sum(len(c["nar"]) for c in SHORT) // len(SHORT))
print("esqueleto:", "-".join(c["layout"] for c in SHORT))
