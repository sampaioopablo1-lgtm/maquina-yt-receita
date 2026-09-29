#!/usr/bin/env python3
"""Lead escreveu = alguém responde (29/09, pedido do dono).

O log de 14 dias: metade das mensagens de lead (21 de 42) ficou sem nenhuma ação humana; a
mediana de resposta foi 44 min. O fluxo "Interceptação de Sinal — Resposta v2" só cobre lead em
CONECTAR, e avisava pelo canal "WhatsApp" do CRM (WhatsApp oficial, não conectado: não chega).

  1. "Lead respondeu — [RESPONDER]" (novo): resposta de lead FORA de CONECTAR (reunião, lead novo,
     sem etapa) -> tarefa [RESPONDER] para a SDR + notificação do app. Pula não perturbe.
  2. "Resposta atrasada — aviso ao Pablo" (novo): tag `resposta-atrasada` (posta pelo robô
     finalizar_tarefas.py quando a tarefa passa de 30 min aberta no horário) -> notificação do app
     ao Pablo e troca a tag por `resposta-atrasada-avisada` (não avisa de novo).
  3. Interceptação v2: o aviso passa de "WhatsApp" para notificação do app (formato testado no
     lead ouro).

    python criar_responder.py --seco
    python criar_responder.py
"""
import copy, sys
import ghl_interno as g
import criar_workflows_27 as base
from criar_workflows_27 import Cadeia, criar

SDR = "ML69c5kAJ93cliAGgBj6"
PABLO = "JdvhvOTEBTvUyRi0BXU8"
INTERCEPTA = "42bfaf59-ba56-455d-bb4c-8ecd39efbcd1"


def aviso(titulo, corpo, usuario):
    return {"type": "notification", "notification": {
        "type": "send_notification", "title": titulo, "body": corpo,
        "redirectPage": "contact", "selectedUser": usuario, "userType": "user"}}


def modelo_tag():
    t = g.ler(INTERCEPTA)["workflowData"]["templates"]
    for n in t:
        for br in (n.get("attributes") or {}).get("branches") or []:
            for seg in br.get("segments") or []:
                for c in seg.get("conditions") or []:
                    if c.get("conditionSubType") == "tags":
                        return c
    raise SystemExit("PAROU: sem modelo de condição de tag")


def responder():
    base.MODELO_COND = modelo_tag()
    c = Cadeia()
    _, nao1 = c.se(None, "Está em CONECTAR? (a Interceptação cuida)",
                   [("contact_detail", "tags", "index-of-true", ["etapa-conectar"])])
    _, nao = c.se(nao1, "Não perturbe?", [("contact_detail", "tags", "index-of-true", ["nao-perturbe"])])
    t = c.add(nao, "task-notification", "[RESPONDER] tarefa", {
        "title": "[RESPONDER] {{contact.first_name}} escreveu no WhatsApp — responda",
        "body": "<p>O lead mandou mensagem. Responda no WhatsApp ou ligue em até 5 min. "
                "A tarefa fecha sozinha quando você responder ou ligar.</p>",
        "assignedTo": SDR, "type": "task_notification", "dueDate": "{{right_now.date}}",
        "__customInputs__": {"dueDate": "duration-picker"}})
    c.add(t, "internal_notification", "Aviso à SDR", aviso(
        "💬 {{contact.name}} escreveu no WhatsApp",
        "{{contact.name}} ({{contact.phone}}) mandou mensagem. Responda ou ligue em até 5 min.", SDR))
    gat = {"type": "customer_reply", "name": "Lead respondeu", "conditions": []}
    return c.nos, gat


def atrasada():
    c = Cadeia()
    a = c.add(None, "internal_notification", "Aviso ao Pablo", aviso(
        "⏰ Lead sem resposta há 30 min",
        "{{contact.name}} ({{contact.phone}}) escreveu e ninguém respondeu nem ligou em 30 min.", PABLO))
    b = c.add(a, "remove_contact_tag", "Tira a marca", {"tags": ["resposta-atrasada"]})
    c.add(b, "add_contact_tag", "Marca como avisado", {"tags": ["resposta-atrasada-avisada"]})
    gat = {"type": "contact_tag", "name": "Resposta atrasada", "conditions": [
        {"operator": "index-of-true", "field": "tagsAdded", "value": "resposta-atrasada", "title": "Tag Added",
         "type": "select", "id": "tag-added"}]}
    return c.nos, gat


def corrigir_intercepta(seco):
    cur = g.ler(INTERCEPTA)
    novo = copy.deepcopy(cur["workflowData"]["templates"])
    n = [x for x in novo if x["type"] == "internal_notification"]
    if len(n) != 1:
        raise SystemExit("PAROU: esperava 1 aviso na Interceptação, achei %d" % len(n))
    if (n[0]["attributes"] or {}).get("type") == "notification":
        print("Interceptação: aviso já é do app"); return
    n[0]["attributes"] = aviso("💬 {{contact.name}} respondeu",
                               "{{contact.name}} ({{contact.phone}}) respondeu. Ligue ou responda em até 5 min.", SDR)
    print("Interceptação v%s: aviso WhatsApp -> app%s" % (cur["version"], " (seco)" if seco else ""))
    if not seco:
        g.put(cur, novo)
        d = g.ler(INTERCEPTA)
        print("  relido: %s v%s, aviso=%s" % (d["status"], d["version"],
              [x["attributes"].get("type") for x in d["workflowData"]["templates"] if x["type"] == "internal_notification"]))


if __name__ == "__main__":
    seco = "--seco" in sys.argv
    criar("Lead respondeu — [RESPONDER]", *responder(), seco)
    criar("Resposta atrasada — aviso ao Pablo", *atrasada(), seco)
    corrigir_intercepta(seco)
