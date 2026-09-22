"""W1 - Contador de Toques (IMPLEMENTACAO-WORKFLOWS.md, W1).

Gatilho: Contact Tag Added -> toque
  1 Remove Contact Tag  'toque'
  2 Math  Toques na semana + 1
  3 Wait  7 dias
  4 Math  Toques na semana - 1
Allow Re-entry ligado, Stop on Response desligado, sem janela.
Nasce RASCUNHO.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "Contador de Toques"
CAMPOS = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"),
                        encoding="utf-8"))
TOQUES = CAMPOS["Toques na semana"]["id"]

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                   "workflows-json", NOME + ".json"))

c = g.client()

# nunca duplicar: se ja existe, reaproveita o id
ja = [w for w in c.request("GET", "/workflow/" + g.LOC)
      if w.get("name") == NOME and w.get("type") == "workflow"]
if ja:
    print("ja existe '" + NOME + "' (" + ja[0]["id"] + ") - nao recrio")
    wf = ja[0]["id"]
else:
    passos = [
        g.tag_step(["toque"], remove=True),
        g.math_step(TOQUES, "add", 1),
        g.wait_step(7, "days"),
        g.math_step(TOQUES, "subtract", 1),
    ]
    wf = g.build(c, NOME, passos,
                 [g.tag_trigger("Toque", "toque")],
                 allow_reentry=True, stop_on_response=False)
    print("criado: " + wf)

doc = g.export(c, wf, OUT)
w = doc["workflow"]
print("\n== LEITURA DE VOLTA ==")
print("nome=%s  status=%s" % (w.get("name"), w.get("status")))
print("allowMultiple(re-entry)=%s  stopOnResponse=%s  window=%s"
      % (w.get("allowMultiple"), w.get("stopOnResponse"), w.get("window")))
for s in (w.get("workflowData") or {}).get("templates") or []:
    a = s.get("attributes") or {}
    extra = ""
    if s["type"] in ("add_contact_tag", "remove_contact_tag"):
        extra = str(a.get("tags"))
    elif s["type"] == "math_operation":
        op = (a.get("operators") or [{}])[0]
        extra = "%s %s em %s" % (op.get("operator"), op.get("value"),
                                 a.get("updateField"))
    elif s["type"] == "wait":
        extra = str(a.get("startAfter"))
    print("  %-22s %s" % (s["type"], extra))
for t in (doc["triggers"] if isinstance(doc["triggers"], list) else []):
    print("  GATILHO %s  %s  target=%s" % (t.get("type"), t.get("conditions"),
                                           t.get("targetActionId")))
print("\nJSON: " + OUT)
print("URL: https://app.wesalescrm.com/v2/location/" + g.LOC
      + "/automation/workflow/" + wf)
