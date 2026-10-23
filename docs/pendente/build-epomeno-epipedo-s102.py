"""Monta a spec do `epomeno-epipedo-s102`.

FAMILIA: o TITULO e uma LINHA do mesmo boletim, e a linha que descreve a sua
mesa esta algumas linhas abaixo — capitulos 18, 20, 25, 26 e 27 do
`os51d8fA0sY` (`epomeno-epipedo-006`), com os 0, 3 e 5 de apoio. Os CINCO
irmaos foram lidos pelo `irmaos_da_origem` e, nos TRES sem o campo da familia
(`s012`, `s063`, `s072`), pela PROSA e pela NARRACAO de cada um, que e de
primeira mao (776).

ZERO numero novo sobre o mundo: o eixo e a PROCEDENCIA do numero dentro do
documento, nao o valor de nada. Nem indice, nem percentual, nem preco, nem nome
de produto, nem mes, nem orgao — e nenhum deles aparece na narracao.
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import guardas_do_construtor as GC
import layouts_do_short as LS
import temas_do_dono as TD

PAC = "epomeno-epipedo-s102"
CANAL = "epomeno-epipedo"
SOND = set(LS.desenham())

short = [
    {"layout": "titulo",
     "kicker": "Ο τίτλος είναι μία γραμμή",
     "sub": "ενός δελτίου με πολλές",
     "nar": "Ο τίτλος είναι μία γραμμή."},
    {"layout": "item",
     "kicker": "Και είναι σωστή",
     "sub": "κανείς δεν λέει ψέματα",
     "nar": "Και είναι σωστή γραμμή."},
    {"layout": "barras",
     "kicker": "Δύο γραμμές, ένα δελτίο",
     "barras": [{"rot": "Ο τίτλος", "v": 100},
                {"rot": "Η λίστα", "v": 100}],
     "nar": "Το δελτίο έχει και άλλες."},
    {"layout": "item",
     "kicker": "Λίγες γραμμές πιο κάτω",
     "sub": "στο ίδιο κείμενο",
     "nar": "Η λίστα είναι πιο κάτω."},
    {"layout": "lista",
     "kicker": "Τι κάνει το καθένα",
     "itens": ["Ο τίτλος συνοψίζει",
               "Η λίστα ονομάζει"],
     "nar": "Αυτός συνοψίζει, αυτή ονομάζει."},
    {"layout": "item",
     "kicker": "Η σύνοψη δεν ψεύδεται",
     "sub": "δεν κρύβει τίποτα",
     "nar": "Η σύνοψη δεν ψεύδεται ποτέ."},
    {"layout": "titulo",
     "kicker": "Αλλά πετάει κάτι",
     "sub": "κάθε σύνοψη πετάει",
     "nar": "Κάθε σύνοψη όμως πετάει κάτι."},
    {"layout": "item",
     "kicker": "Και είναι τυπωμένο",
     "sub": "με όνομα προϊόντος δίπλα",
     "nar": "Το πεταμένο είναι τυπωμένο."},
    {"layout": "lista",
     "kicker": "Δύο στήλες",
     "itens": ["Τι ανέβηκε",
               "Τι κατέβηκε"],
     "nar": "Έχει στήλη πάνω και κάτω."},
    {"layout": "barras",
     "kicker": "Και ο τίτλος ανάμεσα",
     "barras": [{"rot": "Η πάνω στήλη", "v": 100},
                {"rot": "Ο τίτλος", "v": 50},
                {"rot": "Η κάτω στήλη", "v": 0}],
     "nar": "Και ο τίτλος είναι ανάμεσα."},
    {"layout": "item",
     "kicker": "Κανείς δεν μένει εκεί",
     "sub": "κάθε τραπέζι ζει σε μία στήλη",
     "nar": "Κανένα τραπέζι δεν ζει εκεί."},
    {"layout": "titulo",
     "kicker": "Δεν θέλεις άλλη πηγή",
     "sub": "θέλεις να κατεβάσεις το βλέμμα",
     "nar": "Δεν χρειάζεσαι άλλη πηγή."},
    {"layout": "item",
     "kicker": "Άνοιξε το ίδιο δελτίο",
     "sub": "και κατέβα λίγες γραμμές",
     "nar": "Άνοιξε το δελτίο, πιο κάτω."},
    {"layout": "cta",
     "kicker": "Επόμενο Επίπεδο",
     "sub": "κάνε εγγραφή",
     "nar": "Διάβασε τη στήλη, κάνε εγγραφή."},
]

for i, c in enumerate(short):
    assert c["layout"] in SOND, (i, c["layout"], "FORA do conjunto SONDADO")

sp = {
    "slug": PAC,
    "pacote": PAC,
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "longo_existente": "os51d8fA0sY",
    "longo": [],
    "thumb": {"l1": "Μία γραμμή", "l2": "από πολλές"},
    "paleta": TD.paleta_do_canal(CANAL),
    "short": short,
    "copy": open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "copy-" + PAC + ".md"), encoding="utf-8").read(),
}

GC.exige(sp)
print(json.dumps(sp, ensure_ascii=False, indent=1))
