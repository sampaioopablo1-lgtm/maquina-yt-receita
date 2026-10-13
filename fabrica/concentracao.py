#!/usr/bin/env python3
"""Quanto a pauta de um canal está CONCENTRADA numa origem só.

POR QUE ISTO EXISTE, e é um hábito meu que eu só vi ao contar. Em 13/10/2026,
às 04:0x, o `labtreinamento` tinha **dez** shorts tirados do MESMO longo
(`ntrMxq89I4o`) enquanto **nove** das suas treze origens tinham sido usadas
**uma vez só** — e há doze specs de longo no canal, com 55 a 87 capítulos cada.
Eu vinha minerando um longo por rodada porque era o que estava aberto na minha
cabeça, e chamei isso de "a unidade de pauta é (LONGO x FAMÍLIA)" — que é
verdade, e não é licença para ficar num longo só.

**O risco não é estético.** O portão `similaridade` (<= 0,65 contra o mesmo
canal) existe por causa do conteúdo INAUTÊNTICO do YPP: *"the substance of each
video should be materially varied"*. Logo concentração de origem ataca
exatamente o portão que estamos tentando passar, e ela cresce devagar — por isso
precisa de contador, não de memória.

**O que este módulo NÃO faz:** não reprova nada e não escolhe pauta. Ele conta e
diz onde a concentração está, com a lista das origens pouco usadas ao lado — que
é a informação que a rodada precisa para trocar. Limiar de ALERTA é observado e
declarado: o dobro da segunda origem mais usada, porque é a forma mais simples
de dizer "uma origem está carregando o canal" sem inventar número.
"""
from __future__ import annotations

import collections
import glob
import json
import os
import sys

RAIZ = os.path.dirname(__file__)


def contagem(canal: str, raiz: str = None) -> dict[str, int]:
    """{origem: quantos shorts} para um canal, lendo `longo_existente`."""
    base = raiz or os.path.join(RAIZ, "specs")
    c: collections.Counter = collections.Counter()
    for f in glob.glob(os.path.join(base, f"{canal}-s*.json")):
        with open(f, encoding="utf-8") as fh:
            o = json.load(fh).get("longo_existente")
        if o:
            c[o] += 1
    return dict(c)


def analise(contagens: dict[str, int]) -> dict:
    """Quem domina, por quanto, e quais origens estão pouco usadas.

    `dominante` é a origem mais usada. `alerta` é True quando ela tem mais que o
    DOBRO da segunda — limiar observado, não importado: com uma origem no dobro
    da seguinte, a variedade do canal passa a depender de um texto só.
    """
    if not contagens:
        return {"total_shorts": 0, "origens": 0, "dominante": None,
                "alerta": False, "motivo": "nenhum short com origem declarada"}
    ordem = sorted(contagens.items(), key=lambda kv: (-kv[1], kv[0]))
    top, n_top = ordem[0]
    n_seg = ordem[1][1] if len(ordem) > 1 else 0
    total = sum(contagens.values())
    uma_vez = sorted(o for o, n in contagens.items() if n == 1)
    return {
        "total_shorts": total,
        "origens": len(contagens),
        "dominante": top,
        "n_dominante": n_top,
        "n_segunda": n_seg,
        "fracao_dominante": round(n_top / total, 3),
        "usadas_uma_vez": uma_vez,
        "alerta": n_top > 2 * n_seg,
        "motivo": (f"{top} carrega {n_top} de {total} shorts, mais que o dobro "
                   f"da segunda ({n_seg}). O portao `similaridade` e de "
                   f"MONETIZACAO, e concentracao de origem ataca ele."
                   if n_top > 2 * n_seg else
                   f"{top} lidera com {n_top}, contra {n_seg} da segunda — "
                   "dentro do dobro."),
    }


def relato(canal: str, raiz: str = None) -> str:
    c = contagem(canal, raiz)
    a = analise(c)
    if not a["total_shorts"]:
        return f"PAUTA de {canal}: {a['motivo']}"
    linhas = [f"PAUTA de {canal}: {a['total_shorts']} shorts sobre "
              f"{a['origens']} origens.",
              f"  dominante {a['dominante']} com {a['n_dominante']} "
              f"({a['fracao_dominante']*100:.0f}%), segunda com {a['n_segunda']}."]
    if a["alerta"]:
        linhas.append("  >> ALERTA: " + a["motivo"])
    if a["usadas_uma_vez"]:
        linhas.append(f"  origens usadas UMA vez ({len(a['usadas_uma_vez'])}), "
                      "e e daqui que a proxima peca deveria sair: "
                      + ", ".join(a["usadas_uma_vez"]))
    linhas.append("  (isto CONTA, nao reprova: a escolha de origem segue a "
                  "regra (a) da rotina e a consulta de estoque.)")
    return "\n".join(linhas)


def main() -> int:
    canais = sys.argv[1:] or ["labtreinamento", "epomeno-epipedo",
                              "kolejny-poziom"]
    for c in canais:
        print(relato(c))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
