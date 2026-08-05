#!/usr/bin/env python3
"""setiap-level-005 — "Gaji Naik Tapi Uang Tetap Habis".

PAUTA. Grupo de pares medido em 2026-08-05: n=38 longos indonesios de financas
dos ultimos 90 dias, mediana 91,25 views/dia, outlier >= 274. Dez outliers.
O topo (10.089 v/d, Rory Asyari) e exatamente o eixo do nosso pacote 004 —
confirma o formato e o queima como assunto. O padrao estrutural que se repete
nos outliers e (pergunta-paradoxo) x (numero de pilares explicito no titulo):
"4 POS", "4 SENI", "4 SUMBER". O eixo ainda aberto e o 4.902 v/d: "Kenapa Gaji
Naik Tetap Terasa Kurang?".

TESE. O aumento e indexado a media. A sua cesta nao e media.

FONTES (duas institucionais que batem, conferidas em 2026-08-05):
  - UMP 2026: +5 a 8% nacional; formula Inflasi + (Pertumbuhan Ekonomi x Indeks
    Alpha) daerah, alpha 0,5-0,9. Kemnaker/SK Gubernur.
  - Inflasi Juni 2026: 3,34% yoy, 0,44% mtm, ytd 1,79%. Transporte contribuiu
    0,28 dos 0,44. BPS.
  - BI-Rate: 5,75% apos alta de 25 bps. Bank Indonesia.
  - Kelas menengah: 57,33 juta (2019) -> 47,85 juta (2024) -> 46,7 juta (2025).
    Estrutura de gasto: hiburan 0,47% -> 0,38%; kendaraan 5,63% -> 3,99%. BPS.

DIMENSIONAMENTO. Pelo modelo medido hoje, nao pela tabela de chars/s:
  duracao = chars/20,58 + n_frases x 0,96
A pausa entre frases domina, entao o ritmo exigido pelo linter de narracao
(frases curtas) ALONGA o video. Alvo 840s.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHARS_POR_S = 20.58
PAUSA_POR_FRASE = 0.96

# ---------------------------------------------------------------------------
# Cada entrada: (layout, kicker, extra, narracao, capitulo_ou_None)
# Capitulo so na PRIMEIRA cena do bloco; as demais levam sem_cap.
# A ultima cena de cada bloco termina em pergunta ou dois-pontos — e o segundo
# em que o espectador decide sair.
# ---------------------------------------------------------------------------
from blocos_005 import BLOCOS

SHORT = [
 ("titulo", "Gajimu naik", "bulanmu sama",
  "Gajimu naik tahun ini. Bulanmu terasa sama."),
 ("item", "Rumusnya", "inflasi rata-rata",
  "Kenaikan upah minimum diindeks ke inflasi rata-rata nasional."),
 ("titulo", "Tapi belanjamu", "bukan rata-rata",
  "Tapi belanjamu bukan rata-rata. Bulan Juni, transportasi menyumbang lebih dari separuh kenaikan harga."),
 ("item", "Dan ongkos", "keluar tiap hari kerja",
  "Dan ongkos keluar setiap hari kerja."),
 ("cta", "Hitungan lengkapnya", "di video panjangnya",
  "Lima pos, semuanya dengan angka dua ribu dua puluh enam. Hitungan lengkapnya ada di video panjangnya."),
]


def montar():
    cenas = []
    for cap, bloco in BLOCOS:
        for i, item in enumerate(bloco):
            lay, kicker, extra, nar = item[0], item[1], item[2], item[3]
            c = {"layout": lay, "kicker": kicker, "nar": nar}
            if lay == "lista":
                c["itens"] = extra
            elif lay == "barras":
                c["itens"], c["alturas"] = extra, item[3]
                c["nar"] = item[4]
            elif lay == "item":
                c["preco"] = extra
            else:
                c["sub"] = extra
            if i == 0:
                c["cap"] = cap
            else:
                c["sem_cap"] = True
            cenas.append(c)
    return cenas


def curtas(cenas):
    out = []
    for lay, kicker, extra, nar in SHORT:
        c = {"layout": lay, "kicker": kicker, "nar": nar}
        if lay == "item":
            c["preco"] = extra
        else:
            c["sub"] = extra
        out.append(c)
    return out


if __name__ == "__main__":
    import re
    cenas = montar()
    spec = {
        "slug": "setiap-level",
        "pacote": "setiap-level-005",
        "voz": "id-ID-ArdiNeural",
        "paleta": {"ink": "#14213D", "c1": "#E5A200", "c2": "#00897B", "bg": "#F7F3E8"},
        "thumb": {"l1": "GAJI NAIK", "l2": "uang tetap habis"},
        "longo": cenas,
        "short": curtas(cenas),
    }
    saida = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "setiap-level-005.json")
    json.dump(spec, open(saida, "w", encoding="utf-8"), ensure_ascii=False)

    chars = sum(len(c["nar"]) for c in cenas)
    nf = sum(len([f for f in re.split(r"(?<=[.!?…])\s+", c["nar"]) if f.strip()])
             for c in cenas)
    est = chars / CHARS_POR_S + nf * PAUSA_POR_FRASE
    caps = sum(1 for c in cenas if c.get("cap"))
    print(f"{len(cenas)} cenas, {caps} capitulos, {chars} chars, {nf} frases")
    print(f"estimativa: {est:.0f}s = {est/60:.1f} min")
    print(f"short: {len(spec['short'])} cenas")
