"""`Reunião Cancelada` — nenhum workflow tratava cancelamento (auditoria 23/09/2026).

Sem isto, quem cancela fica em REUNIÃO com `etapa-reuniao` e os Lembretes v3
seguem até o "Começamos em 10 minutos" de uma reunião que não existe.

Gatilho: reunião do calendário "Reunião com closer" com status cancelled.
  1. sai dos Lembretes v3 e do Pós-agendamento v2 (e tira a marca lr-conf-agora);
  2. se pode receber mensagem (sem nao-perturbe): WhatsApp oferecendo remarcar;
  3. tarefa [NO-SHOW] para o SDR remarcar (família que a Faxina mantém em REUNIÃO);
  4. nota.
Janela seg-sex 08:30-18:30 (mensagem e tarefa).

Uso: python build_reuniao_cancelada.py [--so-montar] [--publicar]
"""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "Reunião Cancelada"
LEMBRETES = "10065adb-aad7-4d12-92df-6941f05d130c"
POS_AGEND = "81815fcc-ff4f-4b72-8a1f-7dbf44ce6911"
HOJE_18H = 1789851600000
JANELA = {"days": [1, 2, 3, 4, 5], "startHour": 8, "startMinute": 30, "endHour": 18, "endMinute": 30}

passos = [
    {"id": g.uid(), "name": "Sai dos lembretes e do pós-agendamento", "type": "remove_from_workflow",
     "attributes": {"type": "remove_from_workflow", "workflow_id": [LEMBRETES, POS_AGEND]}},
    g.tag_step(["lr-conf-agora"], remove=True),
    g.Branch("Pode receber mensagem?", [g.cond("contact_detail", "tags", "index-of-false", ["nao-perturbe"])],
             [{"id": g.uid(), "name": "WhatsApp · CANC-1", "type": "sms",
               "attributes": {"type": "sms", "attachments": [], "body":
                              "Oi! Vi que a nossa reunião de diagnóstico foi cancelada. Sem problema — "
                              "quer que eu te mande outros horários? É só responder aqui."}}],
             []),
]
# a tarefa e a nota valem nos dois ramos: ficam depois do Branch via goto não é
# possível (Branch encerra a linha) -> duplicamos no ramo NÃO.
tarefa = {"id": g.uid(), "name": "Tarefa · remarcar", "type": "task-notification", "workflowsActionType": "INTERNAL",
          "attributes": {"title": "[NO-SHOW] Reunião cancelada — remarcar com o lead",
                         "body": "<p>O lead cancelou a reunião de diagnóstico. Ligue ou responda no WhatsApp e "
                                 "marque um novo horário no calendário \"Reunião com closer\". Se ele desistiu, "
                                 "marque a oportunidade como perdida com o motivo.</p>",
                         "assignedTo": "contact.assigned_user",
                         "dueDate": {"duration": 0, "unit": "days", "time": HOJE_18H, "skipWeekends": True},
                         "type": "task_notification", "__customInputs__": {}}}
nota = g.note_step("Nota", "Reunião cancelada pelo lead · lembretes interrompidos · tarefa de remarcar criada")
passos[-1].sim += [tarefa, nota]
passos[-1].nao += [dict(copy.deepcopy(tarefa), id=g.uid()), dict(copy.deepcopy(nota), id=g.uid())]

if __name__ == "__main__":
    nos = g.montar(copy.deepcopy(passos))
    print(len(nos), "nós | ids únicos:", len({n["id"] for n in nos}) == len(nos))
    if "--so-montar" in sys.argv:
        sys.exit(0)
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    modelo = [t for t in c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + POS_AGEND)
              if not t.get("deleted")][0]
    gat = {k: copy.deepcopy(modelo[k]) for k in ("type", "conditions", "masterType") if k in modelo}
    for cnd in gat["conditions"]:
        if cnd.get("field") == "appointment.status":
            cnd["value"] = "cancelled"
    gat.update({"status": "draft", "schedule_config": {}, "name": "Reunião cancelada",
                "active": True, "triggersChanged": True, "location_id": g.LOC})
    wf = ids.get(NOME) or g.create_workflow(c, NOME)
    g.preencher(c, wf, NOME, passos, [gat], allow_reentry=True, stop_on_response=False, janela=JANELA)
    g.export(c, wf, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "workflows-json", NOME + ".json"))
    print("rascunho:", wf, NOME)
    if "--publicar" in sys.argv:
        print("publicar:", g.publicar(c, wf))
