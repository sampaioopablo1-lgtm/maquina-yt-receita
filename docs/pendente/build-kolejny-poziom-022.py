#!/usr/bin/env python3
"""kolejny-poziom-022 — PACOTE: longo de 68 cenas (7 capitulos) + short de 12.

CANAL do `passo_zero` (9/9/8 na janela de 24 h, kolejny-poziom o MINIMO UNICO) —
e a decisao de fazer PACOTE e do instrumento criado na rodada anterior, o
`longo_por_canal`: este canal estava **43,4 h sem longo** e com **0L/8S** na
janela de 24 h, o MAIOR vao da frota, contra 1L em cada um dos outros dois. E a
segunda metade do pedido do dono de 16/10, que ate 23/10 as 21:3x nao tinha
instrumento nenhum.

CLASSE PROCEDIMENTO, logo a trava 600 nao se aplica: ZERO numero meu sobre o
mundo, e as quantidades faladas sao a estrutura do proprio procedimento.

CONTAGEM do short pela chave `por_cadencia_servivel`: 12 cenas, folga +12 — 11 e
13 repetem os tamanhos das duas ultimas do canal (`s104` e `s103`), e o teto
MEDIDO da voz e 14. MISTURA do `sugere_forma`: a de MAIOR folga em doze cenas
(7.541 de 7.560 ordens livres).
"""
import json
import os
import sys

RAIZ = "/home/user/maquina-yt-receita"
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from longo_kolejny_022 import LONGO            # noqa: E402

SHORT = [
    dict(layout="titulo", kicker="Dwie liczby", sub="z dwóch różnych półek",
         nar="Dwie liczby z dwóch półek."),
    dict(layout="item", kicker="Nowa oferta", preco="cena dla nowego",
         nar="Nowa oferta: cena dla nowego."),
    dict(layout="item", kicker="Twój rachunek", preco="rabat już minął",
         nar="Twój rachunek: rabat już minął."),
    dict(layout="barras", kicker="Co z czym zestawiasz",
         barras=[{"rotulo": "Ich najlepsza", "valor": 4},
                 {"rotulo": "Twoja najgorsza", "valor": 9}],
         nar="Ich najlepsza obok twojej najgorszej."),
    dict(layout="titulo", kicker="Wynik znasz", sub="zanim cokolwiek policzysz",
         nar="Wynik znasz, zanim policzysz."),
    dict(layout="lista", kicker="Ile liczb istnieje",
         itens=["Cena dla nowego", "Twoja obecna", "Dla pozostających"],
         nar="A liczb jest trzy, nie dwie."),
    dict(layout="item", kicker="Trzecia", preco="cena dla pozostających",
         nar="Trzecia to cena dla pozostających."),
    dict(layout="barras", kicker="Gdzie ona jest",
         barras=[{"rotulo": "Na twoim papierze", "valor": 0},
                 {"rotulo": "U dostawcy", "valor": 8}],
         nar="Nie ma jej na papierze, który masz."),
    dict(layout="item", kicker="Dlatego", preco="nie wchodzi do porównania",
         nar="Dlatego nie wchodzi do porównania."),
    dict(layout="item", kicker="Jak ją zdobyć", preco="jedno pytanie u siebie",
         nar="Zdobywasz ją jednym pytaniem."),
    dict(layout="lista", kicker="Wtedy kartka ma",
         itens=["Trzy wiersze", "Jedno twoje zużycie"],
         nar="Wtedy liczysz trzy wiersze, nie dwa."),
    dict(layout="cta", kicker="Zapytaj o swoją", sub="cenę dla obecnych",
         nar="Zapytaj o cenę dla obecnych i zasubskrybuj."),
]

COPY = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "copy-kolejny-poziom-022.md"), encoding="utf-8").read()

sp = {
    "slug": "kolejny-poziom",               # em PACOTE a convencao MEDIDA e o CANAL
    "pacote": "kolejny-poziom-022",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "thumb": {"l1": "Trzy kolumny", "l2": "trzy operacje"},
    "longo": LONGO,
    "short": SHORT,
    "copy": COPY,
}

import temas_do_dono as TD                      # noqa: E402
sp["paleta"] = TD.paleta_do_canal("kolejny-poziom")

# O TRILHO de capitulos e DERIVADO da propria spec — eu nao escrevo o campo em
# cena nenhuma (19/10 as 09:2x). Ele RECUSA quando nao cabe, em vez de encolher
# a fonte.
import trilho as TR                             # noqa: E402
n_caps = TR.aplica_no_longo(sp["longo"])   # muta as cenas no lugar

import guardas_do_construtor as GC              # noqa: E402
GC.exige(sp)

import layouts_do_short as LS                   # noqa: E402
desenham = LS.desenham()
for i, c in enumerate(SHORT):
    assert c["layout"] in desenham, (
        "cena %d do SHORT: layout %r fora do conjunto SONDADO %s — foi assim "
        "que eu publiquei um cartao em branco em 19/10 as 18:18Z"
        % (i, c["layout"], sorted(desenham)))

destino = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    RAIZ, "fabrica", "specs", "kolejny-poziom-022.json")
with open(destino, "w", encoding="utf-8") as f:
    json.dump(sp, f, ensure_ascii=False, indent=1)
print("gravado %s" % destino)
print("longo %d cenas | short %d cenas | media do short %.2f caracteres"
      % (len(sp["longo"]), len(SHORT),
         sum(len(c["nar"]) for c in SHORT) / len(SHORT)))
