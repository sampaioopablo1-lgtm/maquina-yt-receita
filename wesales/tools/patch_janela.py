"""Poe a janela seg-sex 08:30-18:30 num workflow publicado que cria tarefa e
esta sem janela (regra D13: nada nasce no fim de semana). PUT cirurgico: mesmo
id, mesmos nos; backup em workflows-json/_antes-janela/.
Uso: python patch_janela.py "Nome do workflow" [--aplicar]"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

JANELA = {"days": [1, 2, 3, 4, 5], "startHour": 8, "startMinute": 30, "endHour": 18, "endMinute": 30}
NOME = sys.argv[1]
APLICAR = "--aplicar" in sys.argv
BK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "workflows-json", "_antes-janela")

c = g.client()
alvo = [w for w in c.request("GET", "/workflow/" + g.LOC)
        if w.get("name") == NOME and w.get("status") == "published"]
if len(alvo) != 1:
    sys.exit("esperava 1 publicado com esse nome, achei %d" % len(alvo))
wf = alvo[0]["id"]
f = c.request("GET", "/workflow/" + g.LOC + "/" + wf) or {}
tpl = (f.get("workflowData") or {}).get("templates") or []
print("%s %s: %d nós, janela atual=%s" % (wf[:8], NOME, len(tpl), f.get("window")))
if not tpl or f.get("window") or not APLICAR:
    sys.exit(0)
os.makedirs(BK, exist_ok=True)
with open(os.path.join(BK, NOME + ".json"), "w", encoding="utf-8") as fh:
    json.dump(f, fh, ensure_ascii=False, indent=1)
c.request("PUT", "/workflow/" + g.LOC + "/" + wf,
          {"name": f.get("name"), "status": "published", "version": f.get("version", 1),
           "allowMultiple": f.get("allowMultiple", True),
           "stopOnResponse": f.get("stopOnResponse", False),
           "allowMultipleOpportunity": f.get("allowMultipleOpportunity", False),
           "timezone": f.get("timezone", "account"), "window": JANELA,
           "workflowData": {"templates": tpl}})
d = c.request("GET", "/workflow/" + g.LOC + "/" + wf) or {}
print("  agora: status=%s janela=%s nós=%d" % (d.get("status"), d.get("window"),
                                              len((d.get("workflowData") or {}).get("templates") or [])))
