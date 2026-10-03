#!/usr/bin/env python3
"""Fotografia da CONFIGURAÇÃO do CRM WeSales (02/10, pedido do dono: se a conta for desativada, dá para remontar
tudo numa contratação futura sem começar do zero). Só configuração — nenhum lead.

    python3 backup_config.py <pasta>      # grava <pasta>/AAAA-MM-DD/...

Workflows (publicados e rascunhos, com gatilhos) e listas inteligentes saem pela API interna (bearer da sessão,
ghl_interno); o resto pelo PIT (GHL_PIT). O que falhar fica em ERROS.txt, sem derrubar o resto.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

import atuador_filas as a
import ghl_interno as g
import listas

LOC = a.LOC


def main() -> int:
    base = os.path.join(sys.argv[1] if len(sys.argv) > 1 else ".", dt.date.today().isoformat())
    os.makedirs(base, exist_ok=True)
    erros, resumo = [], {}

    def grava(nome, dados):
        cam = os.path.join(base, nome)
        os.makedirs(os.path.dirname(cam), exist_ok=True)
        with open(cam, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=1)

    def pit(nome, caminho, chave=None):
        try:
            r = a.pedir("GET", caminho)
            grava(nome, r)
            v = r.get(chave) if chave else r
            resumo[nome] = len(v) if isinstance(v, list) else "ok"
        except BaseException as e:  # pedir() sai com SystemExit
            erros.append("%s: %s" % (nome, str(e)[:200]))

    pit("conta/location.json", "/locations/%s" % LOC)
    pit("campos/custom_fields.json", "/locations/%s/customFields" % LOC, "customFields")
    pit("campos/custom_values.json", "/locations/%s/customValues" % LOC, "customValues")
    pit("campos/tags.json", "/locations/%s/tags" % LOC, "tags")
    pit("funil/pipelines.json", "/opportunities/pipelines?locationId=%s" % LOC, "pipelines")
    pit("agenda/calendars.json", "/calendars/?locationId=%s" % LOC, "calendars")
    pit("agenda/groups.json", "/calendars/groups?locationId=%s" % LOC, "groups")
    pit("equipe/users.json", "/users/?locationId=%s" % LOC, "users")
    pit("formularios/forms.json", "/forms/?locationId=%s&limit=50" % LOC, "forms")
    pit("formularios/surveys.json", "/surveys/?locationId=%s&limit=50" % LOC, "surveys")
    pit("mensagens/templates.json", "/locations/%s/templates?originId=%s&limit=100" % (LOC, LOC), "templates")
    pit("telefonia/numeros.json", "/phone-system/numbers/location/%s" % LOC)

    # formulários completos (campos, lógica, estilo) pela rota da tela
    try:
        for fm in json.load(open(os.path.join(base, "formularios/forms.json"), encoding="utf-8")).get("forms") or []:
            r = g.pedir("GET", "/forms/%s" % fm["id"])
            grava("formularios/%s.json" % fm["id"], r)
    except BaseException as e:
        erros.append("formularios completos: %s" % str(e)[:200])

    # listas inteligentes (visões de Contatos), com filtro, colunas e compartilhamento
    try:
        st, r = listas.sl("GET", "/contacts/smartlist/search?locationId=%s&userId=%s&globals=true" % (LOC, "JdvhvOTEBTvUyRi0BXU8"))
        sls = (r.get("smartLists") or []) if isinstance(r, dict) else []
        for s in sls:
            st2, full = listas.sl("GET", "/contacts/smartlist/%s" % s["id"])
            grava("listas/%s.json" % s["id"], full if isinstance(full, dict) else s)
        resumo["listas"] = len(sls)
    except BaseException as e:
        erros.append("listas: %s" % str(e)[:200])

    # workflows: todos, com gatilhos
    try:
        wfs = g.listar()
        grava("workflows/_indice.json", [{k: w.get(k) for k in ("id", "name", "status", "version", "updatedAt", "parentId")} for w in wfs])
        n = 0
        for w in wfs:
            if w.get("type") == "directory":
                continue
            try:
                g.exportar(w["id"], os.path.join(base, "workflows", "%s__%s.json" % (w.get("status"), w["id"])))
                n += 1
            except BaseException as e:
                erros.append("workflow %s %s: %s" % (w["id"], w.get("name"), str(e)[:150]))
        resumo["workflows"] = n
    except BaseException as e:
        erros.append("workflows: %s" % str(e)[:200])

    grava("RESUMO.json", resumo)
    with open(os.path.join(base, "ERROS.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(erros) or "nenhum")
    print("backup em", base, resumo, "| erros:", len(erros))
    for e in erros:
        print("  ERRO", e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
