"""W6 - Loop do closer v2 (IMPLEMENTACAO-WORKFLOWS.md, W6).

O `Post-Meeting Closer Loop` que a IA montou fica intocado; este e o refazer,
com o nome que o dono pediu.

Gatilho: Contact Changed -> 'Reunião foi qualificada' foi alterado
  1 If/Else  veredito vazio -> FIM ; senao segue
  2 Update   'Data do veredito do closer' = data atual
  3 Note     veredito + motivo + nota
  4 veredito = Sim      -> nada
    veredito = Parcial  -> oportunidade abandoned + tag nutricao-90d
    veredito = Nao      -> 4b: motivo 'Timing errado' ? abandoned+tag : lost
  5 nota >= 70 E veredito = Nao  -> notifica gestor
  6 nota <  45 E veredito = Sim  -> notifica gestor
Os ramos do 4 convergem no 5 por goto; o 5 cai no 6. Nenhum ramo muda a
ETAPA - so o status. Nasce RASCUNHO.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "ZZ TESTE W6"
CAMPOS = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"),
                        encoding="utf-8"))
VEREDITO = CAMPOS["Reunião foi qualificada"]
MOTIVO = CAMPOS["Motivo da desqualificação"]
NOTA = CAMPOS["Nota de qualificação"]
DATA_VER = CAMPOS["Data do veredito do closer"]
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))


def abandonar():
    return [g.tag_step(["zz-placeholder-ab"]), g.tag_step(["nutricao-90d"])]


# --- nos 5 e 6 (o 4 converge neles) -------------------------------------
b6 = g.Branch(
    "Nota baixa mas closer aprovou?",
    [g.cond("contact_detail", NOTA["id"], "<", "45"),
     g.cond("contact_detail", VEREDITO["id"], "==", "Sim")],
    sim=[g.notify_user_step(
        "Régua pode estar descartando lead bom",
        "Nota baixa ({{contact.nota_de_qualificao}}) mas o closer marcou Sim "
        "— a régua pode estar descartando lead bom. Revisar "
        "{{contact.name}}.")],
    nao=[],
)

b5 = g.Branch(
    "Nota alta mas closer reprovou?",
    [g.cond("contact_detail", NOTA["id"], ">=", "70"),
     g.cond("contact_detail", VEREDITO["id"], "==", "Não")],
    sim=[g.notify_user_step(
        "Nota alta reprovada pelo closer",
        "Nota {{contact.nota_de_qualificao}} mas o closer marcou Não "
        "({{contact.motivo_da_desqualificao}}) — revisar a régua da seção 9 "
        "com {{contact.name}}."),
        g.goto_step(b6.id)],
    nao=[b6],
)

# --- no 4 e 4b ----------------------------------------------------------
# b5 MORA aqui, no fim do caminho 'lost'; todos os outros ramos saltam para
# ele com goto (um no so pode existir uma vez na arvore)
b4b = g.Branch(
    "Motivo é Timing errado?",
    [g.cond("contact_detail", MOTIVO["id"], "==", "Timing errado")],
    sim=abandonar() + [g.goto_step(b5.id)],
    nao=[g.tag_step(["zz-placeholder-lost"]), b5],
)

b4_parcial = g.Branch(
    "Veredito é Parcial?",
    [g.cond("contact_detail", VEREDITO["id"], "==", "Parcial")],
    sim=abandonar() + [g.goto_step(b5.id)],
    nao=[b4b],
)

b4 = g.Branch(
    "Veredito é Sim?",
    [g.cond("contact_detail", VEREDITO["id"], "==", "Sim")],
    sim=[g.goto_step(b5.id)],
    nao=[b4_parcial],
)

# --- no 1: sem veredito, nao faz nada -----------------------------------
passos = [g.Branch(
    "Veredito está vazio?",
    [g.cond("contact_detail", VEREDITO["id"], "has_no_value", None)],
    sim=[],
    nao=[
        g.field_step(DATA_VER["id"], "Data do veredito do closer",
                     "{{right_now.date}}", "date"),
        g.note_step("Veredito do closer",
                    "Veredito do closer: " + g.token("contact.reunio_foi_qualificada")
                    + " · motivo: " + g.token("contact.motivo_da_desqualificao")
                    + " · nota do SDR/IA na hora: "
                    + g.token("contact.nota_de_qualificao")),
        b4,
    ],
)]

gatilho = {
    "status": "draft", "schedule_config": {},
    "type": "contact_changed", "masterType": "highlevel",
    "name": "Contato Alterado", "active": True, "triggersChanged": True,
    "location_id": g.LOC,
    "conditions": [{"operator": "has-changed",
                    "field": "contact." + VEREDITO["id"],
                    "title": "Reunião foi qualificada", "type": "select",
                    "id": VEREDITO["id"]}],
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
    elif s["type"] == "goto":
        det = "-> %s" % ("OK" if a.get("targetNodeId") in vivos else "ALVO INEXISTENTE")
    elif s["type"] == "internal_update_opportunity":
        det = "status=%s etapa=%s" % (a.get("status"), a.get("pipelineStageId"))
    elif s["type"] == "update_contact_field":
        f = a["fields"][0]
        det = "%s = %s" % (f["title"], f["value"])
    elif s["type"] in ("add_contact_tag", "remove_contact_tag"):
        det = str(a.get("tags"))
    print("  %-26s %s" % (s.get("nodeType") or s["type"], det))
print("URL: https://app.wesalescrm.com/v2/location/" + g.LOC
      + "/automation/workflow/" + wf)
