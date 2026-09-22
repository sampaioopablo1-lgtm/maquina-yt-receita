"""Baixa TODOS os workflows da subconta + campos personalizados para um
corpus local. Serve para ler o formato REAL de cada tipo de no antes de
montar qualquer coisa (em vez de confiar em schema de terceiro).
Somente leitura.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

OUT = os.path.join(os.environ.get("SCRATCH", os.path.dirname(__file__)), "corpus")
os.makedirs(OUT, exist_ok=True)

c = g.client()
lst = c.request("GET", "/workflow/" + g.LOC)
tipos = {}
for w in lst:
    if w.get("type") != "workflow":
        continue
    wid = w["id"]
    full = c.request("GET", "/workflow/" + g.LOC + "/" + wid)
    trg = c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + wid)
    safe = "".join(ch if ch.isalnum() or ch in " -_" else "_" for ch in w.get("name", wid))
    with open(os.path.join(OUT, safe + ".json"), "w", encoding="utf-8") as f:
        json.dump({"workflow": full, "triggers": trg}, f, ensure_ascii=False, indent=2)
    for s in ((full or {}).get("workflowData") or {}).get("templates") or []:
        tipos.setdefault(s.get("type"), []).append(w.get("name"))
    for t in (trg if isinstance(trg, list) else []):
        tipos.setdefault("TRIGGER:" + str(t.get("type")), []).append(w.get("name"))

print("== TIPOS DE NO/GATILHO JA PRESENTES NA SUBCONTA ==")
for k in sorted(tipos):
    print("  %-34s %dx  (ex: %s)" % (k, len(tipos[k]), tipos[k][0]))
print("\ncorpus em: " + OUT)
