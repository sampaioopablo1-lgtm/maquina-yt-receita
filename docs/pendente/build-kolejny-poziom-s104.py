#!/usr/bin/env python3
"""kolejny-poziom-s104 — short solto, 11 cenas.

CANAL do `passo_zero` (9/9/8 na janela de 24 h, kolejny-poziom o MINIMO UNICO).
PAUTA do `pauta_do_momento`: IuBLU-P4Aj8 (kolejny-poziom-016), 4 usos — empate de
CINCO origens desempatado pela MAIOR reserva, 52 livres de 64 e 41 SEM declaracao
de irmao; as duas leituras CONCORDAM e nenhuma cai no maximo do canal por TEXTO.
CONTAGEM pela chave `por_cadencia_servivel`: 14 e a melhor cadencia E o teto
MEDIDO da voz, e saiu NOMEADA e recusada pela FOLGA (23 caracteres, a DOIS do piso
OBSERVADO); 13 e 12 repetem os tamanhos das duas ultimas do canal. Onze tem folga
+18.
FORMA do `sugere_forma`: a mistura de MAIOR folga em onze cenas (3.776 de 3.780
ordens livres).
"""
import json
import os
import sys

RAIZ = "/home/user/maquina-yt-receita"
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

SHORT = [
    dict(layout="titulo", kicker="Liczba z ustawy", sub="to nie twoja stawka",
         nar="Liczba z ustawy to nie twoja stawka."),
    dict(layout="barras", kicker="Czym ona jest",
         barras=[{"rotulo": "Sufit z ustawy", "valor": 10},
                 {"rotulo": "Twoja stawka", "valor": 6}],
         nar="To sufit, najwyższa dopuszczalna granica."),
    dict(layout="item", kicker="Kto wybrał twoją", preco="rada twojej gminy",
         nar="Twoją liczbę wybrała rada twojej gminy."),
    dict(layout="lista", kicker="Zrobiła to uchwałą",
         itens=["Mogła wybrać inną", "Niżej albo wyżej"],
         nar="Zrobiła to uchwałą i mogła wybrać inną."),
    dict(layout="item", kicker="A kto nie", preco="minister ani skarbówka",
         nar="Nie minister i nie urząd skarbowy."),
    dict(layout="titulo", kicker="Dlatego to ciche", sub="sufit ci nie zaprzeczy",
         nar="Dlatego sufit nigdy ci nie zaprzeczy."),
    dict(layout="item", kicker="Twoja kwota", preco="zawsze siedzi pod nim",
         nar="Twoja kwota zawsze siedzi pod nim."),
    dict(layout="barras", kicker="Te same metry",
         barras=[{"rotulo": "Gmina A", "valor": 5},
                 {"rotulo": "Gmina B", "valor": 8}],
         nar="Te same metry, dwie gminy, inna stawka."),
    dict(layout="item", kicker="Skutek", preco="szukasz w złym dokumencie",
         nar="Więc szukasz w niewłaściwym dokumencie."),
    dict(layout="lista", kicker="Gdzie jest twoja",
         itens=["W uchwale rady gminy", "Jest publikowana"],
         nar="Twoja jest w uchwale rady twojej gminy."),
    dict(layout="cta", kicker="Jest publiczna", sub="przeczytaj swoją",
         nar="Przeczytaj uchwałę swojej gminy i zasubskrybuj."),
]

COPY = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "copy-kolejny-poziom-s104.md"), encoding="utf-8").read()

sp = {
    "slug": "kolejny-poziom-s104",      # em SHORT SOLTO a convencao nova e o PACOTE
    "pacote": "kolejny-poziom-s104",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "longo_existente": "IuBLU-P4Aj8",
    "thumb": {"l1": "Sufit", "l2": "to nie stawka"},
    "longo": [],                        # AUSENCIA DE CHAVE NAO E VALOR VAZIO (18/10)
    "short": SHORT,
    "copy": COPY,
}

import temas_do_dono as TD
sp["paleta"] = TD.paleta_do_canal("kolejny-poziom")

import guardas_do_construtor as GC
GC.exige(sp)

import layouts_do_short as LS
desenham = LS.desenham()
for i, c in enumerate(SHORT):
    assert c["layout"] in desenham, (
        "cena %d: layout %r fora do conjunto SONDADO %s — foi assim que eu "
        "publiquei um cartao em branco em 19/10 as 18:18Z"
        % (i, c["layout"], sorted(desenham)))

destino = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    RAIZ, "fabrica", "specs", "kolejny-poziom-s104.json")
with open(destino, "w", encoding="utf-8") as f:
    json.dump(sp, f, ensure_ascii=False, indent=1)
print("gravado %s" % destino)
print("short %d cenas | media %.2f caracteres"
      % (len(SHORT), sum(len(c["nar"]) for c in SHORT) / len(SHORT)))
