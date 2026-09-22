"""W14 - Opt-out por Palavra-chave (IMPLEMENTACAO-WORKFLOWS.md, W14).

Gatilho: Customer Replied (WhatsApp)
  1 If/Else  corpo da mensagem CONTEM qualquer uma das 17 frases (OU)
       nao -> FIM
       sim -> 2 Add tag nao-perturbe
              3 DND ligado
              4 Remove fila-tel / fila-wa / fila-quente
              5 Remove de todos os workflows
              6 If/Else etapa==CONECTAR E status==open
                   sim -> oportunidade = lost -> salta para 6b
                   nao -> 6b
              6b Notificacao ao dono (sempre)
              7  Note

Duas decisoes conscientes, com o porque:
- o gatilho combina condicoes com E, entao as 17 frases nao cabem nele;
  ficam num If/Else com OU logo no primeiro no. Efeito identico ao da spec.
- a spec pede um `Find opportunity` no no 1 so para deixar a oportunidade
  visivel ao no 6, e manda os dois ramos dele seguirem para o mesmo lugar.
  As condicoes de oportunidade ja leem a oportunidade do contato direto
  (e o que W15/W17 fazem, testado) - o no vira ruido e foi omitido.

NUNCA remove tag de estado nem apaga nada: so acrescenta DND e opt-out.
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "Opt-out por Palavra-chave"
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))

# lista exata da spec (W14). NUNCA 'pare', 'stop' ou 'nao quero mais' soltos:
# casam com "parece otimo".
FRASES = [
    "pare de", "pare com", "para de mandar", "para de me mandar",
    "não quero mais mensagem", "não quero mais contato",
    "não quero receber mensagem", "não quero receber mais",
    "remove meu contato", "tira meu número", "descadastr",
    "cancelar inscri", "não me liga mais", "não me mande mais",
    "sai da lista", "me tira da lista", "unsubscribe",
]


def dnd_step():
    return {"id": g.uid(), "name": "Set Contact DND", "type": "dnd_contact",
            "attributes": {"type": "dnd_contact", "dnd_direction": "outbound",
                           "dnd_contact": "enable", "specific_channels": []}}


def remove_todos_workflows():
    return {"id": g.uid(), "name": "Remove from Workflows",
            "type": "remove_from_all_workflows",
            "attributes": {"type": "remove_from_all_workflows",
                           "includeCurrent": False}}


aviso = g.notify_owner_step(
    "Opt-out por palavra-chave",
    "Opt-out por palavra-chave: {{contact.name}} — DND ligado e saiu de "
    "todas as réguas. Mensagem que disparou: revisar no histórico. Se foi "
    "falso positivo, desligar o DND na mão é a única volta.")

b6 = g.Branch(
    "Ainda em CONECTAR e aberta?",
    [g.cond("opportunities", "pipelineStageId", "==", g.STAGES["CONECTAR"]),
     g.cond("opportunities", "status", "==", "open")],
    sim=[g.opp_step("lost", g.STAGES["CONECTAR"]), g.goto_step(aviso["id"])],
    nao=[aviso,
         g.note_step("Opt-out por palavra-chave",
                     "Opt-out por palavra-chave detectado em "
                     + g.token("right_now") + " · DND ligado · removido de "
                     "todas as réguas automáticas")],
)

passos = [g.Branch(
    "Pediu para parar?",
    [g.cond("contact_reply", "message.body", "contain", f) for f in FRASES],
    operador="or",
    sim=[
        g.tag_step(["nao-perturbe"]),
        dnd_step(),
        g.tag_step(["fila-tel", "fila-wa", "fila-quente"], remove=True),
        remove_todos_workflows(),
        b6,
    ],
    nao=[],
)]

gatilho = {
    "status": "draft", "schedule_config": {},
    "type": "customer_reply", "masterType": "highlevel",
    "name": "Cliente Respondeu", "active": True, "triggersChanged": True,
    "location_id": g.LOC,
    "conditions": [{"operator": "==", "field": "message.type", "value": 19,
                    "title": "Canal de resposta", "type": "select"}],
}

c = g.client()
existentes = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
              if w.get("type") == "workflow"}
if NOME in existentes:
    wf = existentes[NOME]
    g.preencher(c, wf, NOME, passos, [gatilho])
    print("rascunho existente preenchido: " + wf)
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
        seg = a["branches"][0]["segments"][0]
        cs = seg["conditions"]
        det = "%s de %d condicoes (%s ...)" % (
            seg["operator"].upper(), len(cs), cs[0]["conditionValue"])
    elif s["type"] == "goto":
        det = "-> %s" % ("OK" if a.get("targetNodeId") in vivos else "ALVO SUMIU")
    elif s["type"] in ("add_contact_tag", "remove_contact_tag"):
        det = str(a.get("tags"))
    elif s["type"] == "create_opportunity":
        det = "status=%s" % a.get("opportunity_status")
    print("  %-26s %s" % (s.get("nodeType") or s["type"], det))
print("PUBLICANDO")
print("  publicado" if g.publicar(c, wf) else "  NAO publicou")
print("URL: https://app.wesalescrm.com/v2/location/" + g.LOC
      + "/automation/workflow/" + wf)
