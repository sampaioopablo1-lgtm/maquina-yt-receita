"""W7 - Registro de Comparecimento (IMPLEMENTACAO-WORKFLOWS.md, W7).

Gatilho: Appointment Status -> calendario 'Reunião com closer' / Showed
  1 If/Else 'Data compareceu' esta vazio -> segue ; senao FIM
  2 Update  'Data compareceu' = data atual
  3 Update  'Nº de no-shows' = 0
  4 Note    Compareceu a reuniao
Sem mudanca de etapa. Re-entry ligado, sem janela. Nasce RASCUNHO.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "Registro de Comparecimento"
CALENDARIO = "3uNQFjCEDe7b4gKZJuOZ"   # 'Reunião com closer' (lido do Pós-agendamento)
CAMPOS = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"),
                        encoding="utf-8"))
COMPARECEU = CAMPOS["Data compareceu"]
NOSHOWS = CAMPOS["Nº de no-shows"]
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))

passos = [g.Branch(
    "Ainda sem data de comparecimento?",
    [g.cond("contact_detail", COMPARECEU["id"], "has_no_value", None)],
    sim=[
        g.field_step(COMPARECEU["id"], "Data compareceu",
                     "{{right_now.date}}", "date"),
        g.field_step(NOSHOWS["id"], "Nº de no-shows", 0, "numerical"),
        g.note_step("Compareceu à reunião",
                    "Compareceu à reunião · " + g.token("right_now")),
    ],
    nao=[],
)]

gatilho = {
    "status": "draft", "schedule_config": {},
    "type": "appointment", "masterType": "highlevel",
    "name": "Status Do Agendamento", "active": True,
    "triggersChanged": True, "location_id": g.LOC,
    "conditions": [
        {"operator": "==", "field": "appointment.eventType", "value": "normal",
         "title": "Tipo de evento", "type": "select"},
        {"operator": "==", "field": "calendar.id", "value": CALENDARIO,
         "title": "In calendar", "type": "select", "id": g.uid()},
        {"operator": "==", "field": "appointment.status", "value": "showed",
         "title": "Appointment status is", "type": "select", "id": g.uid()},
        {"operator": "is-any-of", "field": "contactMode", "value": ["contact"],
         "type": "input"},
    ],
}

c = g.client()
existentes = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
              if w.get("type") == "workflow"}
if NOME in existentes:
    wf = existentes[NOME]
    atual = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
    n = len(((atual or {}).get("workflowData") or {}).get("templates") or [])
    if n:
        print("ja existe com %d nos - nao mexo" % n)
    else:
        g.preencher(c, wf, NOME, passos, [gatilho])
        print("rascunho vazio preenchido: " + wf)
else:
    wf = g.build(c, NOME, passos, [gatilho],
                 allow_reentry=True, stop_on_response=False)
    print("criado: " + wf)

doc = g.export(c, wf, os.path.join(JSON_DIR, NOME + ".json"))
w = doc["workflow"]
tpl = (w.get("workflowData") or {}).get("templates") or []
print("status=%s re-entry=%s nos=%d" % (w.get("status"), w.get("allowMultiple"),
                                        len(tpl)))
for s in tpl:
    a = s.get("attributes") or {}
    det = ""
    if s.get("nodeType") == "condition-node":
        cs = a["branches"][0]["segments"][0]["conditions"]
        det = " E ".join("%s %s %s" % (x["conditionSubType"],
                                       x["conditionOperator"],
                                       x["conditionValue"]) for x in cs)
    elif s["type"] == "update_contact_field":
        f = a["fields"][0]
        det = "%s = %s" % (f["title"], f["value"])
    print("  %-16s %s" % (s.get("nodeType") or s["type"], det))
for t in (doc["triggers"] if isinstance(doc["triggers"], list) else []):
    print("  GATILHO %s -> %s" % (t.get("type"),
          [x.get("value") for x in (t.get("conditions") or [])]))
print("URL: https://app.wesalescrm.com/v2/location/" + g.LOC
      + "/automation/workflow/" + wf)
