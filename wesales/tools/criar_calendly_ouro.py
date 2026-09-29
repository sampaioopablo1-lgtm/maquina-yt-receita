#!/usr/bin/env python3
"""Aviso especial à SDR quando o lead marca reunião sozinho pelo Calendly (29/09, pedido do dono).

"Este lead é ouro: já marcou compromisso na minha agenda. Precisa aparecer para a SDR, com
notificação especial, ligação para qualificar e o grupo criado."
O robô `calendly_para_crm.py` grava a reunião, as tarefas e depois põe a tag `calendly-ouro`;
este workflow manda a notificação interna à SDR e tira a tag (remarcação avisa de novo).
"""
import sys
from criar_workflows_27 import Cadeia, criar

SDR = "ML69c5kAJ93cliAGgBj6"
TAG = "calendly-ouro"
NOME = "Calendly — lead ouro (aviso à SDR)"


def montar():
    c = Cadeia()
    a = c.add(None, "internal_notification", "Aviso à SDR", {"type": "notification", "notification": {
        "type": "send_notification", "title": "⭐ LEAD OURO — marcou reunião pelo Calendly",
        "body": "{{contact.name}} ({{contact.phone}}) marcou sozinho reunião com o Pablo. LIGUE AGORA: "
                "confirme a presença, qualifique Q1–Q6 e crie o grupo com o closer. As tarefas já estão "
                "no seu nome.",
        "redirectPage": "contact", "selectedUser": SDR, "userType": "user"}})
    c.add(a, "remove_contact_tag", "Tira a marca (remarcação avisa de novo)", {"tags": [TAG]})
    gat = {"type": "contact_tag", "name": "Calendly ouro", "conditions": [
        {"operator": "index-of-true", "field": "tagsAdded", "value": TAG, "title": "Tag Added",
         "type": "select", "id": "tag-added"}]}
    return c.nos, gat


if __name__ == "__main__":
    nos, gat = montar()
    criar(NOME, nos, gat, "--seco" in sys.argv)
    if "--seco" not in sys.argv:
        import ghl_interno as g
        w = g.por_nome(NOME); cur = g.ler(w["id"])
        cur["window"] = None          # avisa a qualquer hora: lead marca à noite e no fim de semana
        g.put(cur, cur["workflowData"]["templates"])
        d = g.ler(w["id"])
        print("final:", d["status"], "v%s" % d["version"], "janela", d.get("window"),
              [(t["name"], t.get("active")) for t in g.gatilhos(w["id"])])
