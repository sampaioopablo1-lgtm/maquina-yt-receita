#!/usr/bin/env python3
"""Diz, numa passada so, TUDO que falta numa spec para ela passar.

POR QUE ISTO EXISTE, medido na noite de 25 para 26/08/2026.

Escrevi cinco specs a mao naquela noite. Nenhuma passou de primeira, e nenhuma
falhou por causa do texto: falharam por TAMANHO. O ciclo era sempre o mesmo,
tres a quatro voltas por spec:

    build -> medir -> "falta 160 s e cinco capitulos estao curtos"
          -> escrever cenas -> build -> medir -> ainda falta -> ...

Cada volta custa uma leitura minha e um `python3` inteiro, e o diagnostico vem
picado: o portao de duracao reclama do total, o de capitulos reclama do
espacamento, e nenhum dos dois diz QUANTOS SEGUNDOS FALTAM ONDE. Eu terminava
adivinhando quantas cenas acrescentar e conferindo depois.

Este arquivo troca a adivinhacao por uma conta. Ele le a spec, olha o veredito
do canal, e imprime o deficit em segundos POR CAPITULO e no total — mais uma
estimativa de quantas cenas isso significa naquela voz. Uma volta em vez de
tres.

Ele NAO escreve nada e NAO relaxa portao nenhum: no fim chama o
`prontidao.avalia` e repete o que ele disser. A conta aqui existe para que a
correcao no TEXTO seja feita de uma vez, nao para dispensar a correcao.

    python3 fabrica/dimensiona.py fabrica/specs/<pacote>.json [--veredito X]
"""

import argparse
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import copy_md                                            # noqa: E402
import prontidao                                          # noqa: E402
from ensaio import (MODELO_VOZ, duracao_estimada,         # noqa: E402
                    duracao_estimada_short)

# Folga sobre o MIN_CAP do copy_md. O portao cobra 60 s entre aberturas, mas
# quem decide na producao sao os tempos dos CLIPES renderizados, nao esta
# estimativa. Cinco segundos de folga foi o que separou, nesta noite, as specs
# que passaram das que voltaram — todas as cinco foram desenhadas para 65 s.
FOLGA_CAP_S = 5.0

# Faixas por veredito, como a rotina define. O alvo e sempre o PISO da faixa:
# o melhor longo da frota tem 687 s e o pior 781 s (aprendizado 483).
FAIXAS = {
    "liberado": (720.0, 900.0),
    "suspenso": (prontidao.PISO_LONGO_S, 900.0),
    "canal frio": (prontidao.PISO_LONGO_S, 900.0),
    "sem dado": (prontidao.PISO_LONGO_S, 900.0),
}


def capitulos(sp, voz):
    """[(nome, duracao_s)] na ordem, medindo cena a cena como o portao faz."""
    longo = sp.get("longo") or []
    tempos = [duracao_estimada([c], voz) for c in longo]
    fora, t, ultimo = [], 0.0, None
    for i, c in enumerate(longo):
        if c.get("cap"):
            if ultimo is not None:
                fora.append((ultimo[0], t - ultimo[1]))
            ultimo = (c["cap"], t)
        t += tempos[i]
    if ultimo is not None:
        fora.append((ultimo[0], t - ultimo[1]))
    return fora


def segundos_por_cena(sp, voz):
    """Media medida NESTA spec — melhor que uma constante do corpus."""
    longo = sp.get("longo") or []
    if not longo:
        return 0.0
    return duracao_estimada(longo, voz) / len(longo)


def relatorio(caminho, veredito):
    sp = json.load(open(caminho, encoding="utf-8"))
    voz = sp.get("voz", "")
    if voz not in MODELO_VOZ:
        print(f"voz {voz!r} sem modelo medido — meca antes de dimensionar")
        return 2

    piso, teto = FAIXAS.get(veredito, FAIXAS["sem dado"])
    d = duracao_estimada(sp.get("longo") or [], voz)
    ds = duracao_estimada_short(sp.get("short") or [], voz)
    spc = segundos_por_cena(sp, voz)
    alvo_cap = copy_md.MIN_CAP + FOLGA_CAP_S

    print(f"{os.path.basename(caminho)}   voz {voz}   veredito {veredito!r}")
    print(f"  {len(sp.get('longo') or [])} cenas, {spc:.1f}s por cena na media desta spec\n")

    print(f"  longo  {d:7.1f}s = {d/60:5.2f} min   alvo {piso:.0f}-{teto:.0f}s (va ao PISO)")
    falta_total = max(0.0, piso - d)
    sobra_total = max(0.0, d - teto)
    if falta_total:
        print(f"         FALTAM {falta_total:.0f}s  ~= {falta_total/spc:.0f} cenas")
    elif sobra_total:
        print(f"         SOBRAM {sobra_total:.0f}s  ~= {sobra_total/spc:.0f} cenas a cortar")
    else:
        print("         dentro da faixa")

    teto_short = prontidao.SHORT_MAX_S / (1 + prontidao.MARGEM_SHORT)
    print(f"  short  {ds:7.1f}s              alvo {prontidao.SHORT_MIN_S:.0f}-{teto_short:.1f}s")
    if ds < prontidao.SHORT_MIN_S:
        print(f"         FALTAM {prontidao.SHORT_MIN_S - ds:.0f}s")
    elif ds > teto_short:
        print(f"         SOBRAM {ds - teto_short:.1f}s — corte repeticao, nao conteudo")

    caps = capitulos(sp, voz)
    print(f"\n  {len(caps)} capitulos (a rotina pede MAIS, nao menos):")
    deficit = 0.0
    for nome, dur in caps:
        falta = max(0.0, alvo_cap - dur)
        deficit += falta
        marca = f"  <-- FALTAM {falta:.0f}s (~{falta/spc:.0f} cenas)" if falta else ""
        print(f"    {dur:6.1f}s  {nome}{marca}")

    print(f"\n  RESUMO: para caber, acrescente pelo menos "
          f"{max(falta_total, deficit):.0f}s no total "
          f"(~{max(falta_total, deficit)/spc:.0f} cenas), "
          f"e distribua respeitando o deficit por capitulo acima.")

    print("\n  --- portoes ---")
    faltas = prontidao.avalia(caminho)
    ruins = {k: v for k, v in faltas.items() if v}
    for k, v in ruins.items():
        print(f"  FALHA {k}")
        for x in v:
            print(f"     {x}")
    if not ruins:
        print("  TODOS LIMPOS")
    return 1 if (ruins or falta_total or sobra_total) else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("spec")
    p.add_argument("--veredito", default="sem dado",
                   choices=sorted(FAIXAS), help="de `v_maquina_licoes`")
    a = p.parse_args()
    return relatorio(a.spec, a.veredito)


if __name__ == "__main__":
    sys.exit(main())
