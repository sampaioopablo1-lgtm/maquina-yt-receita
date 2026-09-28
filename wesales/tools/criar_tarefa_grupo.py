#!/usr/bin/env python3
"""Tarefa "[GRUPO] Criar grupo com o closer" disparada no agendamento (28/09).

Antes era manual: a SDR precisava lembrar de criar o grupo de WhatsApp com o lead e o closer.
Agora, reunião confirmada em qualquer um dos 2 calendários -> tarefa para a SDR, com prazo de
1 hora e o passo a passo do playbook. Concluir a tarefa é o registro de que o grupo foi criado.
Gatilhos copiados do "Pós-agendamento v2" (mesmos 2 calendários), como no criar_capi.py.
"""
import sys
from criar_workflows_27 import Cadeia
from criar_capi import reuniao, criar_varios

SDR = "ML69c5kAJ93cliAGgBj6"   # hoje a única SDR com usuário; ver wesales/equipe.json
NOME = "Grupo com o closer — tarefa da SDR"


def montar():
    c = Cadeia()
    c.add(None, "task-notification", "[GRUPO] tarefa", {
        "title": "[GRUPO] Criar grupo com o closer — {{contact.first_name}}",
        "body": ('<p style="margin:0px; padding-left: 0px!important;">Reunião marcada para '
                 '{{appointment.start_time}}. Crie agora o grupo no WhatsApp da operação: '
                 '<b>{{contact.first_name}} + Pablo + você</b>, nome "OPC | {{contact.first_name}}", '
                 'foto com o logo. Mande a mensagem de boas-vindas e os dois áudios (playbook, '
                 'Passagem para o closer). Orçamento e faturamento nunca no grupo. '
                 'Se o lead não quiser grupo, mande no privado e deixe nota. Concluir esta tarefa = grupo criado.</p>'),
        "assignedTo": SDR, "type": "task_notification",
        "dueDate": {"duration": 0, "unit": "days", "time": 1789851600000, "skipWeekends": False},
        "__customInputs__": {"dueDate": "duration-picker"}})
    nos, _ = c.nos, None
    _, gats = reuniao()
    return nos, gats


if __name__ == "__main__":
    nos, gats = montar()
    print([g["name"] for g in gats])
    criar_varios(NOME, nos, gats, "--seco" in sys.argv)
    if "--seco" not in sys.argv:
        import ghl_interno as g
        w = g.por_nome(NOME); cur = g.ler(w["id"])
        cur["window"] = None
        g.put(cur, cur["workflowData"]["templates"])
        d = g.ler(w["id"])
        print("final:", d["status"], "v%s" % d["version"], "janela", d.get("window"),
              [(t["name"], t.get("active")) for t in g.gatilhos(w["id"])])
