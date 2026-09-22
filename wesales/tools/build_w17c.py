"""W17c - CONECTAR Estagnado (IMPLEMENTACAO-WORKFLOWS.md, W17c).

Gatilho: Contact Changed -> campo 'Tentativa nº' igual a 0
  1 Update  Checkpoint - Tentativa n = {{contact.tentativa_n}}
  2 Wait 14 dias                                  <- alvo dos dois lacos
  3 If/Else etapa==CONECTAR E status==open   nao -> FIM
  4 If/Else Tentativa n != Checkpoint
       sim (a regua andou) -> 5 Remove tag + regrava checkpoint -> volta ao 2
       nao (parado)        -> 6
  6 If/Else Tags nao inclui conectar-estagnado
       sim -> 7 Add tag + notifica gestor -> 8 Note -> 9
       nao -> salta para 9
  9 Update checkpoint -> volta ao 2
Re-entry ligado, sem janela. Nasce RASCUNHO.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "CONECTAR Estagnado"
TAG = "conectar-estagnado"
CAMPOS = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"),
                        encoding="utf-8"))
TENT = CAMPOS["Tentativa nº"]
CHK = CAMPOS["Checkpoint — Tentativa nº"]
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))

VAL_TENT = "{{contact." + TENT["chave"].split(".", 1)[1] + "}}"


def grava_checkpoint():
    return g.field_step(CHK["id"], "Checkpoint — Tentativa nº", VAL_TENT,
                        "numerical")


espera = g.wait_step(14, "days")          # no 2 - alvo dos lacos
no9 = grava_checkpoint()                  # no 9 - vive no ramo sim do 6

b6 = g.Branch(
    "Já foi alertado?",
    [g.cond("contact_detail", "tags", "index-of-false", [TAG])],
    sim=[
        g.tag_step([TAG]),
        g.notify_user_step(
            "CONECTAR sem avanço",
            "{{contact.name}} está em CONECTAR sem tentativa nova há pelo "
            "menos 14 dias. Tentativa nº atual: " + VAL_TENT + "."),
        g.note_step("Alerta de saúde",
                    "Alerta de saúde: CONECTAR sem avanço em 14 dias · "
                    + g.token("right_now")),
        no9,
        g.goto_step(espera["id"]),
    ],
    nao=[g.goto_step(no9["id"])],
)

b4 = g.Branch(
    "A régua andou?",
    [g.cond("contact_detail", CHK["id"], "!=", VAL_TENT)],
    sim=[g.tag_step([TAG], remove=True), grava_checkpoint(),
         g.goto_step(espera["id"])],
    nao=[b6],
)

b3 = g.Branch(
    "Ainda em CONECTAR e aberta?",
    [g.cond("opportunities", "pipelineStageId", "==", g.STAGES["CONECTAR"]),
     g.cond("opportunities", "status", "==", "open")],
    sim=[b4], nao=[],
)

passos = [grava_checkpoint(), espera, b3]

gatilho = {
    "status": "draft", "schedule_config": {},
    "type": "contact_changed", "masterType": "highlevel",
    "name": "Contato Alterado", "active": True, "triggersChanged": True,
    "location_id": g.LOC,
    "conditions": [{"operator": "==", "field": "contact." + TENT["id"],
                    "value": 0, "title": "Tentativa nº", "type": "select",
                    "id": TENT["id"]}],
}

c = g.client()
existentes = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
              if w.get("type") == "workflow"}
c.create_location_tag(TAG)
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
    elif s["type"] == "goto":
        alvo = a.get("targetNodeId")
        det = "-> %s" % ("OK" if alvo in vivos else "ALVO INEXISTENTE")
    elif s["type"] == "update_contact_field":
        f = a["fields"][0]
        det = "%s = %s" % (f["title"], f["value"])
    elif s["type"] in ("add_contact_tag", "remove_contact_tag"):
        det = str(a.get("tags"))
    elif s["type"] == "wait":
        det = str(a.get("startAfter"))
    print("  %-16s %s" % (s.get("nodeType") or s["type"], det))
for t in (doc["triggers"] if isinstance(doc["triggers"], list) else []):
    print("  GATILHO %s %s target=%s" % (t.get("type"), t.get("conditions"),
          "OK" if t.get("targetActionId") in vivos else "ORFAO"))
print("URL: https://app.wesalescrm.com/v2/location/" + g.LOC
      + "/automation/workflow/" + wf)
