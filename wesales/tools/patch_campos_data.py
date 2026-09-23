"""Campo do tipo DATA recebendo {{right_now.date}} ("23/09/2026") da ERRO e
nao grava (medido 23/09/2026 no Loop do closer). O formato que funciona e
"{{right_now.year}}-{{right_now.month}}-{{right_now.day}}" (grava 2026-09-23).
Troca em todo no update_contact_field de tipo date dos publicados.
Uso: python patch_campos_data.py [--aplicar]"""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_funil_reuniao import put, g
BOM = "{{right_now.year}}-{{right_now.month}}-{{right_now.day}}"
RUINS = ("{{right_now.date}}", "{{right_now}}")
aplicar = "--aplicar" in sys.argv
c = g.client()
for w in c.request("GET", "/workflow/" + g.LOC):
    if w.get("status") != "published":
        continue
    cur = c.request("GET", "/workflow/" + g.LOC + "/" + w["id"])
    tpl = copy.deepcopy(cur["workflowData"]["templates"])
    mud = []
    for t in tpl:
        if t.get("type") != "update_contact_field":
            continue
        for f in t["attributes"].get("fields") or []:
            if f.get("type") == "date" and f.get("value") in RUINS:
                f["value"] = BOM
                mud.append(f.get("title"))
    if not mud:
        continue
    print("== %s: %s" % (w["name"], mud))
    if aplicar:
        put(c, cur, tpl)
        v = c.request("GET", "/workflow/" + g.LOC + "/" + w["id"])
        resto = sum(1 for t in v["workflowData"]["templates"] if t.get("type") == "update_contact_field"
                    for f in t["attributes"].get("fields") or [] if f.get("type") == "date" and f.get("value") in RUINS)
        print("   conferido: status=%s restantes=%d ids iguais=%s" % (v.get("status"), resto,
              [x["id"] for x in v["workflowData"]["templates"]] == [x["id"] for x in tpl]))
