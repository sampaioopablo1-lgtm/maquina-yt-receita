"""W9 - SLA do Closer - No-show (IMPLEMENTACAO-WORKFLOWS.md, W9).

Gatilho: Appointment Status -> 'Reunião com closer' / No Show
  1 If/Else etapa==NEGOCIAR E status==open      nao -> FIM
  2 If/Else 'Nº de no-shows' >= 2  -> FIM ; senao segue
  3 Notificacao ao CLOSER (dono do contato)
  4 Wait 2 horas
  5 If/Else igual ao 1                          nao -> FIM
  6 Notificacao ao GESTOR
Re-entry ligado, Stop on Response desligado, sem janela. Nasce RASCUNHO e
so e publicado depois de conferido.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "SLA do Closer — No-show"
CALENDARIO = "3uNQFjCEDe7b4gKZJuOZ"
CAMPOS = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"),
                        encoding="utf-8"))
NOSHOWS = CAMPOS["Nº de no-shows"]
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))


def em_negociar_aberta():
    return [g.cond("opportunities", "pipelineStageId", "==",
                   g.STAGES["NEGOCIAR"]),
            g.cond("opportunities", "status", "==", "open")]


b5 = g.Branch(
    "Ainda em NEGOCIAR e aberta?", em_negociar_aberta(),
    sim=[g.notify_user_step(
        "Closer não retornou após no-show",
        "Closer não deu retorno em 2h após o no-show de {{contact.name}} "
        "({{appointment.start_time}}) — a recuperação automática (NS1) já "
        "está tentando reconectar, mas vale conferir com o closer.")],
    nao=[],
)

b2 = g.Branch(
    "Já teve 2 ou mais no-shows?",
    [g.cond("contact_detail", NOSHOWS["id"], ">=", "2")],
    sim=[],
    nao=[
        g.notify_owner_step(
            "No-show na sua reunião",
            "{{contact.name}} não compareceu à reunião de "
            "{{appointment.start_time}}. A recuperação automática (NS1) já "
            "dispara em instantes — se preferir reagendar você mesmo agora, "
            "é mais rápido para o lead e evita o SDR ligar à toa."),
        g.wait_step(2, "hours"),
        b5,
    ],
)

passos = [g.Branch("Em NEGOCIAR e aberta?", em_negociar_aberta(),
                   sim=[b2], nao=[])]

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
        {"operator": "==", "field": "appointment.status", "value": "noshow",
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
    g.preencher(c, wf, NOME, passos, [gatilho])
    print("rascunho existente preenchido (%d nos antes): %s" % (n, wf))
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
    elif s["type"] == "wait":
        det = str(a.get("startAfter"))
    elif s["type"] == "internal_notification":
        n_ = a.get("notification") or {}
        det = "%s -> %s" % (n_.get("title"), n_.get("userType"))
    print("  %-16s %s" % (s.get("nodeType") or s["type"], det))
print("PUBLICANDO")
print("  publicado" if g.publicar(c, wf) else "  NAO publicou")
print("URL: https://app.wesalescrm.com/v2/location/" + g.LOC
      + "/automation/workflow/" + wf)
