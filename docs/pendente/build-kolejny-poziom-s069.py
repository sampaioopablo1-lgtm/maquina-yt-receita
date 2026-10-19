# -*- coding: utf-8 -*-
"""kolejny-poziom-s069 — TERCEIRA familia do longo publicado hoje neste canal.

PAUTA: origem `GtmoaQMr_1c` (o longo `kolejny-poziom-020`, publicado as 13:49Z),
a UNICA origem de um uso so que o `concentracao.py` nomeia hoje aqui como
escrevivel. O short do pacote usou o DENOMINADOR (a stawka netto por hora) e o
`s068` usou QUAL despesa medir primeiro. Esta usa os DOIS ERROS dos capitulos
32 a 39.

FAMILIA DE ENTRADA ERRADA (nova no canal): os dois erros que deixam a conta mais
BONITA — brutto em cima da stawka, e so as horas do contrato embaixo. Nos dois
casos o resultado sai normal e ninguem avisa: a divisao nunca falha, falha
sempre a lista.

ESQUELETO: so layouts que o `svg_cena_retrato` DESENHA. Medido em 19/10 as
19:1x, depois de eu publicar uma cena `numero` num short e ela sair como cartao
em branco — o retrato despacha `titulo`/`cta`, `item`, `lista` e `barras`, e o
resto volta como fundo vazio.

ORCAMENTO: `mira.orcamento` para dez cenas no PISO (772) desta voz. A pinca do
17:2x segue FECHADA aqui por aritmetica — nenhum orcamento poe os dois mundos
dentro de 41,5 a 43,0 — e isso vai declarado na copy.
"""
import json
import os

RAIZ = "/home/user/maquina-yt-receita"
PAC = "kolejny-poziom-s069"

SHORT = [
    dict(layout="titulo", kicker="Dwa błędy", sub="żadnego nie widać",
         nar="Dwa błędy psują ten rachunek, i żadnego nie widać."),
    dict(layout="item", kicker="Pierwszy błąd", preco="brutto u góry",
         nar="Pierwszy błąd: u góry stawki wpisujesz brutto."),
    dict(layout="barras", kicker="Stawka w górę, godziny w dół",
         barras=[{"rotulo": "Brutto", "valor": 3},
                 {"rotulo": "Netto", "valor": 5}],
         nar="Wtedy stawka rośnie, a godzin wychodzi mniej."),
    dict(layout="item", kicker="Drugi błąd", preco="droższy od tego",
         nar="Drugi błąd jest droższy, bo dotyczy dołu."),
    dict(layout="titulo", kicker="W mianowniku", sub="same godziny z umowy",
         nar="W mianowniku zostają same godziny z umowy."),
    dict(layout="lista", kicker="To wypada z rachunku",
         itens=["Dojazd", "Czekanie", "Przebranie", "Dyżur pod telefonem"],
         nar="Dojazd i czekanie po prostu wypadają z rachunku."),
    dict(layout="item", kicker="I w obu razach", preco="wynik wygląda dobrze",
         nar="W obu przypadkach wynik wychodzi normalnie."),
    dict(layout="item", kicker="Nikt nie ostrzeże", preco="liczba jest ładna",
         nar="Nikt ci nie powie, że ta liczba jest za ładna."),
    dict(layout="barras", kicker="Sprawdzenie",
         barras=[{"rotulo": "Stawka × godziny", "valor": 6},
                 {"rotulo": "Wypłata", "valor": 6}],
         nar="Sprawdzasz to, mnożąc stawkę przez swoje godziny."),
    dict(layout="cta", kicker="Co masz w mianowniku", sub="napisz pod spodem",
         nar="Napisz pod spodem, co dokładnie masz w mianowniku."),
]

sp = {
    "slug": PAC,
    "pacote": PAC,
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "longo_existente": "GtmoaQMr_1c",
    "longo": [],
    "short": SHORT,
    "thumb": {"l1": "Ładna liczba", "l2": "zły mianownik"},
    "paleta": {"bg": "#0B0B0C", "ink": "#F2EEE8", "c1": "#E23B3B",
               "c2": "#D9C7A7", "red": "#FF4D4D", "ok": "#7FB77E",
               "panel": "#151517", "mut": "#8F877C", "acc": "#E23B3B"},
    "copy": "",
}

aqui = os.path.dirname(os.path.abspath(__file__))
sp["copy"] = open(os.path.join(aqui, "copy_kp069s.txt"), encoding="utf-8").read()
alvo = os.path.join(RAIZ, "fabrica", "specs", PAC + ".json")
with open(alvo, "w", encoding="utf-8") as fh:
    json.dump(sp, fh, ensure_ascii=False, indent=1)
print("spec gravada:", alvo)
print("cenas:", len(SHORT), "| media de chars:",
      sum(len(c["nar"]) for c in SHORT) // len(SHORT))
print("esqueleto:", "-".join(c["layout"] for c in SHORT))
