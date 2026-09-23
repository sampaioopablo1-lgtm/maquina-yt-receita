"""Passa para rascunho (draft) os workflows cujo nome comeca com "ZZ TESTE" e
estao publicados. Nao exclui nada. Uso: python desligar_zz.py [--aplicar]"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

APLICAR = "--aplicar" in sys.argv
c = g.client()
for w in c.request("GET", "/workflow/" + g.LOC):
    if not (w.get("name") or "").startswith("ZZ TESTE") or w.get("status") != "published":
        continue
    f = c.request("GET", "/workflow/" + g.LOC + "/" + w["id"]) or {}
    tpl = (f.get("workflowData") or {}).get("templates") or []
    print("%s %s (%d nós)" % (w["id"][:8], w["name"], len(tpl)), end="")
    if not APLICAR or not tpl:
        print("  -> só relatório" if tpl else "  -> vazio, pulei")
        continue
    c.request("PUT", "/workflow/" + g.LOC + "/" + w["id"],
              {"name": f.get("name"), "status": "draft", "version": f.get("version", 1),
               "allowMultiple": f.get("allowMultiple", True),
               "stopOnResponse": f.get("stopOnResponse", False),
               "allowMultipleOpportunity": f.get("allowMultipleOpportunity", False),
               "timezone": f.get("timezone", "account"), "window": f.get("window"),
               "workflowData": {"templates": tpl}})
    novo = (c.request("GET", "/workflow/" + g.LOC + "/" + w["id"]) or {}).get("status")
    print("  -> agora:", novo)
