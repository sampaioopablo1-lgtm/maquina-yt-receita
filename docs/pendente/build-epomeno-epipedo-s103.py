#!/usr/bin/env python3
"""epomeno-epipedo-s103 — short solto, 12 cenas.

CANAL do `passo_zero` (10/8/8 na janela de 24 h, empate desempatado pelo que esta
ha mais tempo sem publicar). PAUTA do `pauta_do_momento`: wUHuwyO2HYo
(epomeno-epipedo-012), 5 usos — empate de CATORZE origens desempatado pela MAIOR
reserva (69 livres de 90, 57 sem declaracao). AS DUAS LEITURAS DIVERGEM e a
rodada SEGUIU a regra escrita, com o vao MEDIDO em UM capitulo (2%) — longe dos
62% em que a rodada de 22/10 as 17:3x desviou e igual ao caso de 3% em que ela
seguiu. CONTAGEM pela chave `por_cadencia_servivel` (12 cenas, folga +16); o teto
MEDIDO da voz (15) saiu NOMEADO, recusado pela FOLGA. FORMA do `sugere_forma`:
a mistura de maior folga em doze cenas (7.542 de 7.560 ordens livres).
"""
import json
import os
import sys

RAIZ = "/home/user/maquina-yt-receita"
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

SHORT = [
    dict(layout="titulo", kicker="Η αλλαγή τιμολογίου", sub="δεν σβήνει το ρεύμα",
         nar="Η αλλαγή δεν σβήνει το ρεύμα."),
    dict(layout="titulo", kicker="Το δίκτυο", sub="μένει το ίδιο",
         nar="Το δίκτυο που σε τροφοδοτεί μένει το ίδιο."),
    dict(layout="item", kicker="Αλλάζει ο αποστολέας", preco="του λογαριασμού",
         nar="Αλλάζει ποιος στέλνει τον λογαριασμό."),
    dict(layout="lista", kicker="Και τι άλλο αλλάζει",
         itens=["Ο κανόνας της χρέωσης", "Τίποτα τεχνικό"],
         nar="Και αλλάζει ο κανόνας της χρέωσης."),
    dict(layout="barras", kicker="Τι αγγίζεται",
         barras=[{"rotulo": "Στο χαρτί", "valor": 9},
                 {"rotulo": "Στο καλώδιο", "valor": 0}],
         nar="Το καλώδιο και η παροχή δεν αγγίζονται."),
    dict(layout="item", kicker="Ούτε μία ώρα", preco="χωρίς ρεύμα",
         nar="Δεν μένεις ούτε μία ώρα χωρίς ρεύμα."),
    dict(layout="item", kicker="Άρα η σύγκριση", preco="δεν κρύβει ρίσκο",
         nar="Άρα η σύγκριση δεν κρύβει ρίσκο."),
    dict(layout="item", kicker="Το ρίσκο είναι άλλο", preco="να μην την κάνεις",
         nar="Το ρίσκο είναι να μην την κάνεις ποτέ."),
    dict(layout="item", kicker="Και δεν σε ειδοποιεί", preco="κανείς γι' αυτό",
         nar="Και κανείς δεν σε ειδοποιεί."),
    dict(layout="lista", kicker="Τι ισχύει στο μεταξύ",
         itens=["Η επιλογή που άφησες", "Κάθε μήνα, μόνη της"],
         nar="Η επιλογή που άφησες ισχύει κάθε μήνα."),
    dict(layout="barras", kicker="Και κάθε χρόνο",
         barras=[{"rotulo": "Φέτος", "valor": 7},
                 {"rotulo": "Και πέρσι", "valor": 7}],
         nar="Και ξανά κάθε χρόνο, χωρίς να κάνεις τίποτα."),
    dict(layout="cta", kicker="Πότε λήγει;", sub="δες τη σύμβασή σου",
         nar="Δες την ημερομηνία λήξης στη σύμβασή σου."),
]

COPY = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "copy-epomeno-epipedo-s103.md"), encoding="utf-8").read()

sp = {
    "slug": "epomeno-epipedo-s103",     # em SHORT SOLTO a convencao nova e o PACOTE
    "pacote": "epomeno-epipedo-s103",
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "thumb": {"l1": "Δεν σβήνει", "l2": "το ρεύμα"},
    "longo": [],                        # AUSENCIA DE CHAVE NAO E VALOR VAZIO (18/10)
    "short": SHORT,
    "copy": COPY,
}

import temas_do_dono as TD
sp["paleta"] = TD.paleta_do_canal("epomeno-epipedo")

import guardas_do_construtor as GC
GC.exige(sp)

import layouts_do_short as LS
desenham = LS.desenham()
for i, c in enumerate(SHORT):
    assert c["layout"] in desenham, (
        "cena %d: layout %r fora do conjunto SONDADO %s"
        % (i, c["layout"], sorted(desenham)))

destino = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    RAIZ, "fabrica", "specs", "epomeno-epipedo-s103.json")
with open(destino, "w", encoding="utf-8") as f:
    json.dump(sp, f, ensure_ascii=False, indent=1)
print("gravado %s" % destino)
print("short %d cenas | media %.2f caracteres"
      % (len(SHORT), sum(len(c["nar"]) for c in SHORT) / len(SHORT)))
