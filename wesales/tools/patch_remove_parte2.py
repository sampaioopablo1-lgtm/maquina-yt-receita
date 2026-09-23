"""Todo no `remove_from_workflow` que tira da Cadencia 12x30 passa a tirar
tambem da parte 2 (a 12x30 foi dividida em 23/09/2026). Varre TODOS os
publicados. Uso: python patch_remove_parte2.py [--aplicar]"""
import copy, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g
from patch_funil_reuniao import put
P1, P2 = "c64a808b-3040-431e-8015-642a265e1022", "17e6dc19-3eca-42e8-83ff-e25a9d5c28e8"
aplicar = "--aplicar" in sys.argv
c = g.client()
for w in c.request("GET", "/workflow/" + g.LOC):
    if w.get("status") != "published" or w["id"] in (P1, P2):
        continue
    cur = c.request("GET", "/workflow/" + g.LOC + "/" + w["id"])
    tpl = copy.deepcopy((cur.get("workflowData") or {}).get("templates") or [])
    n = 0
    for t in tpl:
        a = t.get("attributes") or {}
        alvo = a.get("workflow_id")
        if t.get("type") == "remove_from_workflow" and isinstance(alvo, list) and P1 in alvo and P2 not in alvo:
            a["workflow_id"] = alvo + [P2]; n += 1
    if not n:
        continue
    print("%s: %d nó(s)" % (w["name"], n))
    if aplicar:
        g.export(c, w["id"], os.path.join("..", "workflows-json", "_antes-patch-parte2", w["name"] + ".json"))
        put(c, cur, tpl)
        v = c.request("GET", "/workflow/" + g.LOC + "/" + w["id"])
        ok = sum(1 for t in v["workflowData"]["templates"] if t.get("type") == "remove_from_workflow"
                 and P2 in ((t.get("attributes") or {}).get("workflow_id") or []))
        print("   conferido: status=%s nós=%d com parte 2=%d" % (v.get("status"), len(v["workflowData"]["templates"]), ok))
