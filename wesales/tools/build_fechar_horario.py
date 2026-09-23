"""Fechar Horario - fase final de CONECTAR (PLANO-MULTICANAL.md, D2/D3).

Quem ATENDEU mas nao agendou na mesma ligacao fica em CONECTAR ate marcar a
reuniao de diagnostico. A Pos-ligacao v2 (no "Atendeu") cria a tarefa
[FECHAR HORARIO] e poe a tag `fechar-horario`, que dispara este workflow:

  0  tira o lead das cadencias de tentativa (12x30, Inbound, Reengajamento)
  FH2  +1 dia sem reuniao: tarefa + mensagem automatica MFH1-v1
  FH3  +1 dia: tarefa + mensagem automatica MFH2-v1
  fim  +1 dia sem reuniao: nutricao (abandoned + nutricao-90d) com nota

Sai sozinho quando a reuniao e marcada (Pos-agendamento move para REUNIAO DE
DIAGNOSTICO e o portao de cada passo exige CONECTAR aberta). "Pediu retorno"
pausa (laco de 1 h), como na 12x30. Substitui o W17d "AGENDAR Estagnado".
Janela seg-sex 08:30-18:30 (D13).

Uso: python build_fechar_horario.py --so-montar   (valida sem tocar no CRM)
     python build_fechar_horario.py               (grava rascunho; publicar a parte)
"""
import io
import json
import os
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = os.environ.get("FH_NOME", "Fechar Horário")
TAG = os.environ.get("FH_TAG", "fechar-horario")
C = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"), encoding="utf-8"))
RESULT = C["Resultado da tentativa"]["id"]
TEMPLATE = C["Template usado"]["id"]
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "workflows-json"))
CADENCIAS = ["c64a808b-3040-431e-8015-642a265e1022",    # Cadência 12x30
             "c2375e2f-b4cb-4947-8377-7c1e0529ba82",    # Cadência Inbound
             "37eb32e4-4c21-4c69-bba1-36879ae0886c"]    # Reengajamento 90 dias

MSG = {
    "MFH1-v1": ("{{contact.first_name}}, foi bom falar com você! Pra gente seguir, "
                "qual o melhor dia e horário para a nossa reunião de diagnóstico "
                "(30 minutos)? Pode me responder por aqui mesmo."),
    "MFH2-v1": ("{{contact.first_name}}, passando pra fechar a nossa reunião de "
                "diagnóstico. Tenho horários amanhã de manhã e à tarde — qual fica "
                "melhor pra você?"),
}

SO_MONTAR = "--so-montar" in sys.argv
if SO_MONTAR:
    c, WF = None, "00000000-0000-0000-0000-000000000001"
else:
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
           if w.get("type") == "workflow"}
    WF = ids.get(NOME) or g.create_workflow(c, NOME)
print("workflow: %s (%s)" % (NOME, WF))


def raiz_id(p):
    return p[0].id if isinstance(p[0], g.Branch) else p[0]["id"]


def task_step(titulo, corpo):
    return {"id": g.uid(), "name": "Add Task", "type": "task-notification",
            "attributes": {"title": titulo,
                           "body": '<p style="margin:0px; padding-left: 0px!important;">'
                                   + corpo + "</p>",
                           "assignedTo": "contact.assigned_user", "type": "task_notification",
                           "dueDate": "0", "__customInputs__": {"dueDate": "duration-picker"}}}


def sms_step(codigo):
    return {"id": g.uid(), "name": "WhatsApp · " + codigo, "type": "sms",
            "attributes": {"type": "sms", "body": MSG[codigo], "attachments": []}}


def campo(cid, titulo, valor, tipo):
    return {"id": g.uid(), "name": "Update contact field", "type": "update_contact_field",
            "attributes": {"type": "update_contact_field", "actionType": "update_field_data",
                           "fields": [{"field": cid, "value": valor, "title": titulo,
                                       "type": tipo, "date": ""}]}}


def ainda_sem_reuniao(nome, sim):
    """Portao: CONECTAR aberta; 'Pediu retorno' pausa em laco de 1 h."""
    b_ret = g.Branch(nome + " · Pediu retorno? (pausa)",
                     [g.cond("contact_detail", RESULT, "==", "Pediu retorno")],
                     sim=[], nao=sim)
    b_ret.sim = [g.wait_step(1, "hours"), g.goto_step(b_ret.id)]
    return [g.Branch(nome + " · Ainda em CONECTAR, sem reunião?",
                     [g.cond("opportunities", "pipelineStageId", "==", g.STAGES["CONECTAR"]),
                      g.cond("opportunities", "status", "==", "open")],
                     sim=[b_ret], nao=[g.tag_step([TAG], remove=True)])]


def passo(n, codigo, seguir):
    corpo = ("Fechar horário — tentativa %d de 3. O lead já conversou com você e ainda não "
             "marcou a reunião de diagnóstico.<br>1. 🟢 Ligar pelo WhatsApp (botão <b>Ligar via "
             "WhatsApp</b>).<br>2. 📞 Se não atender, ligar pelo telefone.<br>3. 💬 A mensagem "
             "<b>%s</b> já saiu sozinha agora.<br><br>Marcou? Agende no calendário do closer — o "
             "lead sai daqui sozinho." % (n, codigo))
    return ainda_sem_reuniao("FH%d" % n, [
        sms_step(codigo), campo(TEMPLATE, "Template usado", codigo, "text"),
        task_step("[FECHAR HORÁRIO] FH%d · WhatsApp → Ligar para marcar a reunião" % n, corpo),
        g.wait_step(1, "days")] + seguir)


fim = ainda_sem_reuniao("Fim", [
    g.opp_step("abandoned", g.STAGES["CONECTAR"]),
    g.tag_step(["nutricao-90d"]), g.tag_step([TAG], remove=True),
    g.note_step("Fechar Horário",
                "Atendeu, mas não marcou a reunião em 3 dias úteis de tentativa — "
                "lead foi para nutrição (90 dias).")])
fh3 = passo(3, "MFH2-v1", fim)
fh2 = passo(2, "MFH1-v1", fh3)
passos = [{"id": g.uid(), "name": "Sai das cadências de tentativa",
           "type": "remove_from_workflow",
           "attributes": {"type": "remove_from_workflow", "workflow_id": CADENCIAS}},
          g.wait_step(1, "days")] + fh2

gatilho = g.tag_trigger("Atendeu — fechar horário", TAG)

if SO_MONTAR:
    tpl = g.montar(passos)
else:
    c.create_location_tag(TAG)
    g.preencher(c, WF, NOME, passos, [gatilho], allow_reentry=True, stop_on_response=False,
                janela={"days": [1, 2, 3, 4, 5], "startHour": 8, "startMinute": 30,
                        "endHour": 18, "endMinute": 30})
    doc = g.export(c, WF, os.path.join(JSON_DIR, NOME + ".json"))
    tpl = (doc["workflow"].get("workflowData") or {}).get("templates") or []

vivos = {s["id"] for s in tpl}
print("nós=%d" % len(tpl), dict(Counter(s["type"] for s in tpl)))
print("gotos quebrados: %d" % sum(1 for s in tpl if s["type"] == "goto"
                                 and (s.get("attributes") or {}).get("targetNodeId") not in vivos))
print("tarefas:", [s["attributes"]["title"] for s in tpl if s["type"] == "task-notification"])
