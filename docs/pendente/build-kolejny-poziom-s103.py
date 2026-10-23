#!/usr/bin/env python3
"""kolejny-poziom-s103 — short solto, 13 cenas.

CANAL do `passo_zero` (10/9/7 na janela de 24 h, kolejny-poziom o MINIMO UNICO).
PAUTA do `pauta_do_momento`: IuBLU-P4Aj8 (kolejny-poziom-016), 4 usos — empate de
CINCO origens desempatado pela MAIOR reserva, 52 livres de 64 e 41 SEM declaracao
de irmao; as duas leituras CONCORDAM e nenhuma cai no maximo do canal por TEXTO.
CONTAGEM pela chave `por_cadencia_servivel`: 14 e a melhor cadencia e saiu
NOMEADA, recusada pela FOLGA (23 caracteres, a DOIS do piso OBSERVADO); 12 e 11
repetem os tamanhos das duas ultimas do canal. Treze tem folga +7.
FORMA do `sugere_forma`: a mistura de MAIOR folga em treze cenas (41.575 de
41.580 ordens livres).
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAIZ = "/home/user/maquina-yt-receita"
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

SHORT = [
    dict(layout="titulo", kicker="Trzy osoby", sub="jeden podatek",
         nar="Trzy osoby, jeden podatek."),
    dict(layout="lista", kicker="Co robi każdy",
         itens=["Dzieli kwotę na trzy", "Płaci swoją część"],
         nar="Każdy dzieli kwotę na trzy."),
    dict(layout="item", kicker="I to się zgadza", preco="co do złotówki",
         nar="Suma zgadza się z decyzją."),
    dict(layout="item", kicker="Nikt nie dostaje pisma", preco="więc nic nie boli",
         nar="Nikt nie dostaje pisma z gminy."),
    dict(layout="lista", kicker="Ale ustawa mówi inaczej",
         itens=["Nie po równo", "Solidarnie"],
         nar="Ustawa mówi tu jedno słowo."),
    dict(layout="barras", kicker="Ile może żądać gmina",
         barras=[{"rotulo": "Twoja część", "valor": 3},
                 {"rotulo": "Może żądać", "valor": 9}],
         nar="Solidarnie, czyli całość."),
    dict(layout="item", kicker="Od każdego z was", preco="osobno",
         nar="Od każdego z was osobno."),
    dict(layout="titulo", kicker="Twoja część", sub="to umowa między wami",
         nar="Twoja część to wasza umowa."),
    dict(layout="barras", kicker="Czy to limit dla gminy",
         barras=[{"rotulo": "Wobec siebie", "valor": 8},
                 {"rotulo": "Wobec gminy", "valor": 8}],
         nar="Dla gminy nie jest limitem."),
    dict(layout="item", kicker="Dopóki wszyscy płacą", preco="podział opisuje wszystko",
         nar="Gdy wszyscy płacą, nic nie boli."),
    dict(layout="item", kicker="Koszt wraca w jednym dniu", preco="i nie dzieli się",
         nar="Jeden nie zapłaci i wraca całość."),
    dict(layout="titulo", kicker="Trafia w tego", sub="kogo gmina sięgnie pierwsza",
         nar="Trafia w tego, kto zapłacił."),
    dict(layout="cta", kicker="Czyje nazwiska?", sub="sprawdź swoją decyzję",
         nar="Sprawdź nazwiska w decyzji."),
]

COPY = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "copy-kolejny-poziom-s103.md"), encoding="utf-8").read()

sp = {
    "slug": "kolejny-poziom-s103",      # em SHORT SOLTO a convencao nova e o PACOTE
    "pacote": "kolejny-poziom-s103",
    "idioma": "pl",
    "voz": "pl-PL-MarekNeural",
    "trilha": "Wholesome",
    "thumb": {"l1": "Jeden podatek", "l2": "trzy osoby"},
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
    RAIZ, "fabrica", "specs", "kolejny-poziom-s103.json")
with open(destino, "w", encoding="utf-8") as f:
    json.dump(sp, f, ensure_ascii=False, indent=1)
print("gravado %s" % destino)
print("short %d cenas | media %.2f caracteres"
      % (len(SHORT), sum(len(c["nar"]) for c in SHORT) / len(SHORT)))
