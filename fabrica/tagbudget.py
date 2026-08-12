#!/usr/bin/env python3
"""Orcamento real de tags do YouTube.

O limite e 500 caracteres no conjunto TODO, e uma tag que contem espaco entra
na conta entre aspas: custa len(tag)+2. Medir so a soma dos caracteres da
"aprovacao" a listas que o YouTube rejeita com "One or more tags are invalid" —
foi o que derrubou o pacote setiap-level-004 (477 de soma, 542 de custo real).

Uso: python3 tagbudget.py tags.txt [limite]
Sai 0 se cabe, 1 se estoura, e imprime o custo.
"""
import sys

LIMITE = 500
MARGEM = 20   # sobra deliberada: o YouTube nao documenta o arredondamento


def custo(tags):
    if not tags:
        return 0
    return sum(len(t) + (2 if " " in t else 0) for t in tags) + len(tags) - 1


def cabe(tags, limite=LIMITE - MARGEM):
    return custo(tags) <= limite


def podar(tags, limite=LIMITE - MARGEM):
    """Remove as tags mais caras do fim ate caber, preservando a ordem."""
    t = list(tags)
    while t and custo(t) > limite:
        # a ultima e a menos prioritaria por convencao das nossas listas
        t.pop()
    return t


if __name__ == "__main__":
    arq = sys.argv[1]
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else LIMITE - MARGEM
    tags = [l.rstrip("\n") for l in open(arq, encoding="utf-8") if l.strip()]
    c = custo(tags)
    print(f"{len(tags)} tags, custo {c}, limite {lim}")
    if c > lim:
        p = podar(tags, lim)
        print(f"NAO CABE. Poda sugerida: {len(tags) - len(p)} tags, custo {custo(p)}")
        for t in tags[len(p):]:
            print(f"  cortar: {t}")
        sys.exit(1)
    print("cabe")
