"""W15 - Alerta de Speed-to-lead (IMPLEMENTACAO-WORKFLOWS.md, W15).

Gatilho: Opportunity Stage Changed -> FUNIL DE VENDAS / CONECTAR
  0  If/Else  Tags inclui cad-inbound
       sim -> Wait 15 min  -> goto(no 2)
       nao -> Wait 1 hora  -> no 2
  2  If/Else  etapa==CONECTAR E status==open E '1a tentativa em' vazio
              E Tags nao inclui 'pausado'
       sim -> Add Tag atraso-1a-tentativa -> Notificacao ao gestor -> Note
       nao -> FIM
Os dois Waits caem no MESMO no 2: o ramo curto salta com um goto.
Re-entry ligado, sem janela, Stop on Response desligado. Nasce RASCUNHO.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "Alerta de Speed-to-lead"
CAMPOS = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"),
                        encoding="utf-8"))
PRIMEIRA = CAMPOS["1ª tentativa em"]["id"]
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))

# o portao (no 2) precisa de id fixo: o ramo inbound salta para ele
portao = g.Branch(
    "Ainda sem 1ª tentativa?",
    [g.cond("opportunities", "pipelineStageId", "==", g.STAGES["CONECTAR"]),
     g.cond("opportunities", "status", "==", "open"),
     g.cond("contact_detail", PRIMEIRA, "has_no_value", None),
     g.cond("contact_detail", "tags", "index-of-false", ["pausado"])],
    sim=[
        g.tag_step(["atraso-1a-tentativa"]),
        g.notify_user_step(
            "Speed-to-lead estourado",
            "{{contact.name}} está há mais de 1h em cadência sem a 1ª "
            "tentativa. Entrada: {{contact.entrada_em}}."),
        g.note_step("Alerta speed-to-lead",
                    "Alerta speed-to-lead: sem 1ª tentativa 1h após a "
                    "entrada · " + g.token("right_now")),
    ],
    nao=[],
)

passos = [
    g.Branch(
        "É inbound?",
        [g.cond("contact_detail", "tags", "index-of-true", ["cad-inbound"])],
        sim=[g.wait_step(15, "minutes"), g.goto_step(portao.id)],
        nao=[g.wait_step(1, "hours"), portao],
    ),
]

gatilho = {
    "status": "draft", "schedule_config": {},
    "type": "pipeline_stage_updated", "masterType": "highlevel",
    "name": "Etapa Do Funil Alterada", "active": True,
    "triggersChanged": True, "location_id": g.LOC,
    "conditions": [
        {"operator": "==", "field": "opportunity.pipelineId",
         "value": g.PIPELINE, "title": "No pipeline", "type": "select"},
        {"operator": "==", "field": "opportunity.pipelineStageId",
         "value": g.STAGES["CONECTAR"], "title": "Movido para o estágio",
         "type": "select", "id": "moved-to-stage"},
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
vivos = {s["id"] for s in tpl}
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
    elif s["type"] == "wait":
        det = str(a.get("startAfter"))
    elif s["type"] == "goto":
        alvo = a.get("targetNodeId")
        det = "-> %s %s" % (alvo, "OK" if alvo in vivos else "ALVO INEXISTENTE")
    elif s["type"] == "add_contact_tag":
        det = str(a.get("tags"))
    print("  %-16s %s" % (s.get("nodeType") or s["type"], det))
for t in (doc["triggers"] if isinstance(doc["triggers"], list) else []):
    alvo = t.get("targetActionId")
    print("  GATILHO %s target=%s" % (t.get("type"),
                                      "OK" if alvo in vivos else "ORFAO"))
print("URL: https://app.wesalescrm.com/v2/location/" + g.LOC
      + "/automation/workflow/" + wf)
