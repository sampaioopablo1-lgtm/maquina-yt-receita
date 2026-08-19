#!/usr/bin/env python3
"""Mede R e P de cada voz nos videos que JA FORAM AO AR.

Existe por um erro que durou ate 17/08/2026: o `MODELO_VOZ` era calibrado com
duas amostras sinteticas por voz — uma de duas frases longas, outra de doze
curtas — e as NOVE vozes com dados de producao subestimavam a duracao, de +6,6%
a +18,0%. Nove de nove para o mesmo lado e viés, nao ruido: duas amostras nao
cobrem a distribuicao de tamanho de frase de um roteiro de oitenta cenas.

O preco foi o resep-naik-level-003: dimensionado para 14,2 min, aprovado pelo
portao (teto 15,0) e publicado com 16:14.

A CORRECAO NAO E MEDIR MELHOR EM LABORATORIO, E PARAR DE MEDIR EM LABORATORIO.
Todo pacote publicado deixa um `legendas.srt` no bucket, e o .srt tem o tempo
real de cada cena. Cruzando com a spec (que tem o texto de cada cena) sai a
duracao real por (chars, frases) — centenas de pontos, de graca, do material
que foi ao ar. Uma voz nova entra com o valor de laboratorio e e recalibrada
aqui assim que o primeiro pacote dela sobe.

O ajuste e minimos quadrados sobre

    duracao_da_cena = chars/R + frases * P

resolvido em (1/R, P), que e linear e nao precisa de chute inicial.

Uso:
    python3 fabrica/calibra_voz.py <dir_com_srt> [--specs fabrica/specs]

O <dir_com_srt> tem um `<pacote>.srt` por pacote, casando com
`<specs>/<pacote>.json`. Pacote cujo numero de cenas nao bate entre .srt e spec
e PULADO com aviso, nunca ajustado pela metade: no bucket ha .srt gravado sob o
nome de outro pacote, e casar texto errado com tempo certo envenena o ajuste
sem levantar erro.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

from ensaio import GAP_CENA_S, MODELO_VOZ  # noqa: E402
from narracao import frases  # noqa: E402


def _seg(t: str) -> float:
    h, m, resto = t.split(":")
    s, ms = resto.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def tempos(caminho: str) -> list[tuple[float, float]]:
    """(inicio, fim) de cada legenda, na ordem do arquivo."""
    fora = []
    for bloco in open(caminho, encoding="utf-8").read().strip().split("\n\n"):
        linhas = bloco.strip().split("\n")
        if len(linhas) < 3:
            continue
        ini, fim = linhas[1].split(" --> ")
        fora.append((_seg(ini), _seg(fim)))
    return fora


def ajusta(C, F, D):
    """(R, P) por minimos quadrados. None quando o sistema e degenerado.

    Degenera quando todas as cenas tem a mesma razao chars/frases — ai os dois
    termos sao indistinguiveis e qualquer par (R, P) sobre a reta serve.
    """
    Scc = sum(c * c for c in C)
    Sff = sum(f * f for f in F)
    Scf = sum(c * f for c, f in zip(C, F))
    Scd = sum(c * d for c, d in zip(C, D))
    Sfd = sum(f * d for f, d in zip(F, D))
    det = Scc * Sff - Scf * Scf
    if det == 0:
        return None
    x = (Scd * Sff - Sfd * Scf) / det       # 1/R
    y = (Scc * Sfd - Scf * Scd) / det       # P
    if x <= 0:
        return None
    return 1 / x, y


def coleta(dir_srt: str, dir_specs: str):
    """(por_voz, gaps, pulados) a partir dos pares .srt + spec que casam."""
    por_voz, gaps, pulados = {}, [], []
    for caminho in sorted(glob.glob(os.path.join(dir_srt, "*.srt"))):
        pacote = os.path.basename(caminho)[:-4]
        spec = os.path.join(dir_specs, f"{pacote}.json")
        if not os.path.exists(spec):
            pulados.append((pacote, "sem spec"))
            continue
        sp = json.load(open(spec, encoding="utf-8"))
        t, cenas = tempos(caminho), sp["longo"]
        if len(t) != len(cenas):
            pulados.append((pacote, f"srt={len(t)} spec={len(cenas)}"))
            continue
        gaps += [round(t[i + 1][0] - t[i][1], 3) for i in range(len(t) - 1)]
        v = por_voz.setdefault(sp["voz"], {"C": [], "F": [], "D": [], "pac": []})
        v["pac"].append(pacote)
        for (ini, fim), c in zip(t, cenas):
            v["C"].append(len(c["nar"]))
            v["F"].append(len(frases(c["nar"], sp.get("idioma"))))
            v["D"].append(fim - ini)
    return por_voz, gaps, pulados


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("dir_srt", help="diretorio com <pacote>.srt")
    p.add_argument("--specs", default=os.path.join(RAIZ, "fabrica", "specs"))
    args = p.parse_args()

    por_voz, gaps, pulados = coleta(args.dir_srt, args.specs)
    for pacote, motivo in pulados:
        print(f"  pulado {pacote}: {motivo}", file=sys.stderr)
    if not por_voz:
        print("nenhum par .srt+spec casou — nada a medir", file=sys.stderr)
        return 2

    if gaps:
        unicos = sorted(set(gaps))
        print(f"gap de montagem: {len(gaps)} amostras, valores {unicos[:4]}"
              f"{'...' if len(unicos) > 4 else ''} (codigo usa {GAP_CENA_S})")

    print(f"\n{'voz':34} {'n':>5} {'R hoje':>7} {'R real':>7} "
          f"{'P hoje':>7} {'P real':>7} {'erro':>7}")
    linhas = []
    for voz, v in sorted(por_voz.items()):
        r = ajusta(v["C"], v["F"], v["D"])
        n = len(v["C"])
        if r is None:
            print(f"{voz:34} {n:5}  ajuste degenerado")
            continue
        R, P = r
        R0, P0 = MODELO_VOZ.get(voz, (float("nan"), float("nan")))
        previsto = sum(c / R0 + f * P0 for c, f in zip(v["C"], v["F"]))
        erro = (sum(v["D"]) / previsto - 1) * 100 if previsto else float("nan")
        print(f"{voz:34} {n:5} {R0:7.2f} {R:7.2f} {P0:7.3f} {P:7.3f} {erro:+6.1f}%")
        linhas.append(f'    "{voz}": ({R:.2f}, {P:.3f}),   # n={n}')

    print("\ncole em ensaio.MODELO_VOZ (so as vozes acima; as outras nao foram medidas):")
    print("\n".join(linhas))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
