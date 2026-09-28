#!/usr/bin/env python3
"""F-27 (rotina "construção contínua", branch claude/amazing-johnson-mclksg) publicado em versão
enxuta em 28/09, a pedido do dono ("veja melhorias e publique se achar necessário").

Lead que liga de volta e ninguém atende hoje não gera nada. Agora: chamada recebida não
atendida (Call Status: no-answer/busy/canceled/voicemail, direção entrada) de um lead ativo
(oportunidade aberta, sem `nao-perturbe`) -> Prioridade 5 (topo da "Minha fila"), `fila-quente`
e tarefa "[LIGAR AGORA] Retornar ligação perdida" para o dono do lead.

Fora desta versão (dependem de decisão/tela): a mensagem automática MRC-1 (template Meta) e a
opção nova "Retornou ligação" no campo Sinal recebido (edição de campo).
"""
import sys
from criar_workflows_27 import Cadeia
from criar_capi import criar_varios
import ghl_interno as g

NOME = "Retorno de chamada perdida (F-27)"


def montar():
    c = Cadeia()
    sim, _ = c.se(None, "Lead ativo e sem não perturbe?", [
        ("contact_detail", "tags", "index-of-false", ["nao-perturbe"]),
        ("opportunities", "status", "==", "open")])
    p = c.add(sim, "update_contact_field", "Prioridade 5 (topo da Minha fila)", {
        "type": "update_contact_field", "actionType": "update_field_data",
        "fields": [{"field": "chuJMRlKzY0Uq1f0lSkX", "value": 5, "title": "Prioridade", "type": "numerical", "date": ""}]})
    t = c.add(p, "add_contact_tag", "Fila quente", {"tags": ["fila-quente"]})
    c.add(t, "task-notification", "[LIGAR AGORA] retorno", {
        "title": "[LIGAR AGORA] Retornar ligação perdida — {{contact.first_name}}",
        "body": ('<p style="margin:0px; padding-left: 0px!important;">{{contact.first_name}} ligou para a '
                 'O Próximo Cliente e ninguém atendeu. Lead que liga de volta é o mais quente que existe: '
                 'retorne agora (telefone; se não atender, WhatsApp) e registre Canal e Resultado.</p>'),
        "assignedTo": "contact.assigned_user", "type": "task_notification",
        "dueDate": {"duration": 0, "unit": "days", "time": 1789851600000, "skipWeekends": False},
        "__customInputs__": {"dueDate": "duration-picker"}})
    gat = {"type": "call_status", "name": "Chamada recebida não atendida", "conditions": [
        {"operator": "contains-any", "field": "call_status", "value": ["no-answer", "busy", "canceled", "voicemail"],
         "title": "Call status", "type": "multiselect", "id": "call_status"},
        {"operator": "==", "field": "message.direction", "value": "inbound", "title": "Call direction", "type": "select"}]}
    return c.nos, [gat]


if __name__ == "__main__":
    nos, gats = montar()
    seco = "--seco" in sys.argv
    criar_varios(NOME, nos, gats, seco)
    if not seco:
        w = g.por_nome(NOME); cur = g.ler(w["id"])
        cur["window"] = None; cur["allowMultiple"] = True
        g.put(cur, cur["workflowData"]["templates"])
        d = g.ler(w["id"])
        print("final:", w["id"], d["status"], "v%s" % d["version"], "janela", d.get("window"), "reentrada", d.get("allowMultiple"),
              [(t["name"], t.get("active")) for t in g.gatilhos(w["id"])])
