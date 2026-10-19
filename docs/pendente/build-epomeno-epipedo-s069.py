# -*- coding: utf-8 -*-
"""epomeno-epipedo-s069 — TERCEIRO angulo do longo publicado hoje neste canal.

PAUTA: origem `pqTc8jBrq0E` (o longo `epomeno-epipedo-068`, publicado as
12:58:55Z), rank 1 e a UNICA origem escrevivel de um uso so que o
`concentracao.py` nomeia hoje neste canal. O short do pacote usou o
DENOMINADOR e o `s068` usou o ALVO em meses (capitulos 48 a 55). Este usa a
UNIDADE do resultado, capitulos 20, 21 e 40 a 47.

FAMILIA DE ENTRADA ERRADA (nova no canal): reportar a reserva como VALOR em
euros em vez de MESES. Valor te compara com gente que tu nao conheces; mes te
compara com o teu proprio mes. Mesmo saldo, tres respostas diferentes.

ORCAMENTO: `mira.orcamento` da 51 caracteres por cena para dez cenas no MEIO da
faixa da frota. Esta peca mira o PISO (772), com 50 — e o instrumento avisa, de
19/10 as 17:2x, que NENHUM orcamento poe os dois mundos dentro de 41,5 a 43,0:
a razao piper/edge e 0,886 e o vao entre os mundos vale ~4,7 s contra 1,5 s de
faixa. A pinca esta FECHADA aqui por aritmetica, e vai declarada na copy.
"""
import json
import os

RAIZ = "/home/user/maquina-yt-receita"
PAC = "epomeno-epipedo-s069"

SHORT = [
    dict(layout="titulo", kicker="Ίδιο ποσό",
         sub="άλλη απάντηση",
         nar="Το ίδιο ποσό δίνει δύο εντελώς διαφορετικές απαντήσεις."),
    dict(layout="numero", kicker="Η μονάδα",
         valor="μήνες", sub="όχι ευρώ",
         nar="Το λάθος δεν είναι στην πράξη, είναι στη μονάδα της."),
    dict(layout="item", kicker="Αν βγει σε ευρώ",
         preco="κάτι πήγε λάθος",
         nar="Αν το αποτέλεσμα βγαίνει σε ευρώ, κάτι πήγε λάθος."),
    dict(layout="lista", kicker="Τα ευρώ σε συγκρίνουν",
         itens=["Με τον γείτονα",
                "Με μέσους όρους",
                "Με άρθρα",
                "Με κανέναν δικό σου"],
         nar="Τα ευρώ σε συγκρίνουν με ανθρώπους που δεν ξέρεις."),
    dict(layout="item", kicker="Οι μήνες",
         preco="μόνο με εσένα",
         nar="Οι μήνες σε συγκρίνουν μόνο με τον δικό σου μήνα."),
    dict(layout="barras", kicker="Ίδιο υπόλοιπο",
         barras=[{"rotulo": "Α", "valor": 9},
                 {"rotulo": "Β", "valor": 5},
                 {"rotulo": "Γ", "valor": 2}],
         nar="Τρεις άνθρωποι, ίδιο υπόλοιπο, τρεις απαντήσεις."),
    dict(layout="titulo", kicker="Τα πάγια",
         sub="αυτά αλλάζουν",
         nar="Αυτό που αλλάζει είναι μόνο τα πάγια του κάθε μήνα."),
    dict(layout="item", kicker="Μισά πάγια",
         preco="διπλοί μήνες",
         nar="Με τα μισά πάγια βγαίνουν ακριβώς οι διπλοί μήνες."),
    dict(layout="item", kicker="Το ποσό άλλου",
         preco="δεν σου κάνει",
         nar="Κανένα ποσό που ακούς από άλλον δεν σου κάνει εδώ."),
    dict(layout="cta", kicker="Πόσοι μήνες",
         sub="γράψε από κάτω",
         nar="Γράψε από κάτω πόσους μήνες βγάζεις εσύ σήμερα."),
]

sp = {
    "slug": PAC,
    "pacote": PAC,
    "idioma": "el",
    "voz": "el-GR-NestorasNeural",
    "trilha": "Inspired",
    "longo_existente": "pqTc8jBrq0E",
    "longo": [],
    "short": SHORT,
    "thumb": {"l1": "Ίδιο ποσό",
              "l2": "άλλοι μήνες"},
    "paleta": {"bg": "#F4EFE6", "ink": "#1B1A17", "c1": "#C8502A",
               "c2": "#2B6CB0", "red": "#B83227", "ok": "#2E8B57",
               "panel": "#FFFFFF", "mut": "#7A7263", "acc": "#C8502A"},
    "copy": "",
}

aqui = os.path.dirname(os.path.abspath(__file__))
sp["copy"] = open(os.path.join(aqui, "copy_ep069s.txt"), encoding="utf-8").read()
alvo = os.path.join(RAIZ, "fabrica", "specs", PAC + ".json")
with open(alvo, "w", encoding="utf-8") as fh:
    json.dump(sp, fh, ensure_ascii=False, indent=1)
print("spec gravada:", alvo)
print("cenas:", len(SHORT), "| media de chars:",
      sum(len(c["nar"]) for c in SHORT) // len(SHORT))
print("esqueleto:", "-".join(c["layout"] for c in SHORT))
