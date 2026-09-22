"""W13 v2 - copias corrigidas dos dois Interceptacao de Sinal PUBLICADOS.

Regra do dono: workflow publicado nunca se edita -> as correcoes viram
copia ' v2' em RASCUNHO, e ele decide quando trocar.

O que cada copia corrige:
- CLIQUE v2: o gatilho do publicado aponta para o Trigger Link
  HUdfNRzzEAQJJBMFfeCy, que NAO EXISTE MAIS na subconta (a tela lista
  0 links). Ou seja, o publicado nao tem como disparar. A copia aponta
  para o link novo 'Agendar com o closer' (vSUOvEbVZfxBlWFlTvDV).
- RESPOSTA v2: o publicado dispara em QUALQUER resposta de WhatsApp, sem
  filtro de opt-out. Hoje "pare de mandar mensagem" vira tarefa "ligar
  agora" - o oposto do que o lead pediu (retoque R-17 da spec). A copia
  ganha um portao na frente: se a mensagem contem qualquer frase da lista
  de opt-out, encerra.
  A spec pede o filtro 'Doesn't Contain' no gatilho; aqui ele virou um
  If/Else no primeiro no, porque o operador 'contain' em
  contact_reply/message.body e o unico comprovado nesta subconta e porque
  condicao de gatilho combina com E (17 frases nao caberiam).
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g
import clone_workflow as cl

LINK = json.load(open(os.path.join(os.path.dirname(__file__), "links.json"),
                      encoding="utf-8"))["Agendar com o closer"]["id"]
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))

CLIQUE = "ea0a49b7-f3a9-4d8a-8acd-802975d6db03"
RESPOSTA = "7a1b4e6b-7e6e-4ed8-8ff4-cd98b88cdcff"

FRASES = [
    "pare de", "pare com", "para de mandar", "para de me mandar",
    "não quero mais mensagem", "não quero mais contato",
    "não quero receber mensagem", "não quero receber mais",
    "remove meu contato", "tira meu número", "descadastr",
    "cancelar inscri", "não me liga mais", "não me mande mais",
    "sai da lista", "me tira da lista", "unsubscribe",
]

c = g.client()
ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
       if w.get("type") == "workflow"}


def cria_ou_reescreve(nome, templates, gatilhos):
    if nome in ids:
        wf = ids[nome]
        g.guard(wf)
    else:
        wf = g.create_workflow(c, nome)
    # os templates ja vem montados: grava direto, sem passar por montar()
    for t in gatilhos:
        body = dict(t, workflowId=wf, location_id=g.LOC,
                    actions=[{"workflow_id": wf, "type": "add_to_workflow"}])
        ja = c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + wf)
        ja = [x for x in ja if not x.get("deleted")] if isinstance(ja, list) else []
        if ja:
            tid = ja[0]["id"]
        else:
            r = c.request("POST", "/workflow/" + g.LOC + "/trigger", body)
            tid = (r or {}).get("id")
        if tid:
            c.request("PUT", "/workflow/" + g.LOC + "/trigger/" + tid,
                      dict(body, targetActionId=cl.raiz(templates),
                           advanceCanvasMeta={"position": {"x": 57.5, "y": -73}}))
    cur = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
    r = c.request("PUT", "/workflow/" + g.LOC + "/" + wf,
                  {"name": nome, "status": "draft",
                   "version": cur.get("version", 1) if isinstance(cur, dict) else 1,
                   "allowMultiple": True, "stopOnResponse": False,
                   "workflowData": {"templates": templates}})
    if r and r.get("_error"):
        print("  FALHOU: " + str(r.get("message"))[:200])
        return None
    print("  gravado: " + wf + " (%d nos)" % len(templates))
    g.export(c, wf, os.path.join(JSON_DIR, nome + ".json"))
    return wf


# ---------- CLIQUE v2: so troca o link do gatilho ----------
print("########## Interceptação de Sinal — Clique v2")
orig = c.request("GET", "/workflow/" + g.LOC + "/" + CLIQUE)
tpl = cl.remapear(orig["workflowData"]["templates"])
gat = [{"status": "draft", "schedule_config": {}, "type": "trigger_link",
        "masterType": "highlevel", "name": "Link De Acionamento Clicado",
        "active": True, "triggersChanged": True, "location_id": g.LOC,
        "conditions": [{"operator": "==", "field": "link.id", "value": LINK,
                        "title": "Link de acionamento", "type": "select"}]}]
cria_ou_reescreve("Interceptação de Sinal — Clique v2", tpl, gat)
print("  link do gatilho: " + LINK + " (o publicado usa um id que nao existe)")

# ---------- RESPOSTA v2: portao de opt-out na frente ----------
print("\n########## Interceptação de Sinal — Resposta v2")
orig2 = c.request("GET", "/workflow/" + g.LOC + "/" + RESPOSTA)
corpo = cl.remapear(orig2["workflowData"]["templates"])

portao = g.Branch(
    "Pediu para parar?",
    [g.cond("contact_reply", "message.body", "contain", f) for f in FRASES],
    operador="or",
    sim=[],            # pediu opt-out -> encerra aqui
    nao=[],            # o fluxo original inteiro entra abaixo
)
armacao = g.montar([portao])
no_nao = [s for s in armacao if s.get("nodeType") == "branch-no"][0]
corpo = cl.pendurar_em(corpo, no_nao["id"])
no_nao["next"] = cl.raiz(corpo)
tpl2 = armacao + corpo

gat2 = [{"status": "draft", "schedule_config": {}, "type": "customer_reply",
         "masterType": "highlevel", "name": "Cliente Respondeu",
         "active": True, "triggersChanged": True, "location_id": g.LOC,
         "conditions": [{"operator": "==", "field": "message.type",
                         "value": 19, "title": "Canal de resposta",
                         "type": "select"}]}]
cria_ou_reescreve("Interceptação de Sinal — Resposta v2", tpl2, gat2)
print("  portao de opt-out com %d frases na frente do fluxo original" % len(FRASES))
print("\nAs duas nascem RASCUNHO: trocar pelo publicado e decisao do dono.")
