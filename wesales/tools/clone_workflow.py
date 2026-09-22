"""Clona um workflow publicado para uma copia ' v2' em RASCUNHO.

Regra do dono: workflow publicado nunca se edita. As correcoes viram copia.
O clone remapeia TODOS os ids (no, ramo, sibling, alvo de goto) para que os
dois grafos nao se cruzem, e permite pendurar a copia inteira dentro do ramo
'nao' de um portao novo (usado para adicionar um filtro na frente).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g


def remapear(templates: list) -> list:
    """Devolve copia dos nos com ids novos e todas as referencias ajustadas."""
    novo_id = {s["id"]: g.uid() for s in templates}

    def tr(v):
        return novo_id.get(v, v)

    out = []
    for s in templates:
        s = dict(s)
        s["id"] = tr(s["id"])
        for k in ("parent", "parentKey"):
            if s.get(k):
                s[k] = tr(s[k])
        if isinstance(s.get("next"), list):
            s["next"] = [tr(x) for x in s["next"]]
        elif s.get("next"):
            s["next"] = tr(s["next"])
        if isinstance(s.get("sibling"), list):
            s["sibling"] = [tr(x) for x in s["sibling"]]
        a = dict(s.get("attributes") or {})
        if a.get("targetNodeId"):
            a["targetNodeId"] = tr(a["targetNodeId"])
        if isinstance(a.get("branches"), list):
            a["branches"] = [dict(b, id=tr(b["id"])) if b.get("id") else b
                             for b in a["branches"]]
        s["attributes"] = a
        # meta de canvas do original nao serve na copia
        s.pop("advanceCanvasMeta", None)
        out.append(s)
    return out


def pendurar_em(templates: list, parent_id: str) -> list:
    """Reparenta as raizes do grafo clonado para dentro de um ramo."""
    ids = {s["id"] for s in templates}
    out = []
    for s in templates:
        s = dict(s)
        if not s.get("parentKey") or s["parentKey"] not in ids:
            s["parentKey"] = parent_id
        if not s.get("parent") or s["parent"] not in ids:
            s["parent"] = parent_id
        out.append(s)
    return out


def raiz(templates: list) -> str:
    """Id do primeiro no do grafo (o que ninguem aponta)."""
    apontados = set()
    for s in templates:
        n = s.get("next")
        if isinstance(n, list):
            apontados.update(n)
        elif n:
            apontados.add(n)
    for s in templates:
        if s["id"] not in apontados:
            return s["id"]
    return templates[0]["id"]
