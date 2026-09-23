"""Nutricao (substitui o Reengajamento 90 dias) + Triagem da resposta.

Decisao do dono (23/09/2026): nutricao 100% AUTOMATICA - uma mensagem de
WhatsApp a cada 15 dias. Se o lead responde, sai na hora uma mensagem de
TRIAGEM; a resposta a ela decide:
  1 / quero conversar  -> tag `reengajado`, volta para CONECTAR e para a 12x30
  3 / sem interesse    -> desliga o lead (DND, `nao-perturbe`, perdido)
  2 / agora nao        -> segue na nutricao
  outra coisa          -> tarefa [SINAL] para o SDR ler e decidir

Dois workflows:
- "Nutrição — WhatsApp a cada 15 dias" (reusa o id do Reengajamento, 37eb32e4):
  gatilho tag `nutricao-90d`; 6 mensagens (N1..N6), 15 dias entre elas;
  antes de cada uma confere `status-nutricao` e ausencia de `nao-perturbe`/
  `reengajado`. Stop on Response DESLIGADO: quem responde "2" segue recebendo.
- "Triagem da Nutrição": gatilho resposta do cliente (WhatsApp oficial 19 e
  Stevo 20); so age em quem tem `status-nutricao` (tag do Espelho de Etapa).
Mensagens pela Stevo (no `sms`), janela seg-sex 08:30-18:30.

Uso: python build_nutricao.py --so-montar | python build_nutricao.py (grava rascunhos)
"""
import io
import json
import os
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

AQUI = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(AQUI, "campos.json"), encoding="utf-8"))
TEMPLATE = C["Template usado"]["id"]
JANELA = {"days": [1, 2, 3, 4, 5], "startHour": 8, "startMinute": 30, "endHour": 18, "endMinute": 30}
NUTRI_ID = "37eb32e4-4c21-4c69-bba1-36879ae0886c"
NOME_NUTRI = "Nutrição — WhatsApp a cada 15 dias"
NOME_TRI = "Triagem da Nutrição"

MSG = {
    "N1-v1": ("Oi {{contact.first_name}}, aqui é o {{user.first_name}} da {{location.name}}. "
              "Passando rápido: uma coisa que muda o resultado de anúncio é responder o lead "
              "nos primeiros minutos — depois disso a chance de conversar cai muito. Se quiser, "
              "te mostro como organizar isso aí. É só responder."),
    "N2-v1": ("{{contact.first_name}}, uma pergunta rápida: hoje você sabe quanto custa cada "
              "cliente que chega pelos seus anúncios? Se a resposta for \"mais ou menos\", vale "
              "uma conversa de 10 minutos. Me responde aqui."),
    "N3-v1": ("{{contact.first_name}}, dica curta de tráfego pago: antes de aumentar a verba, "
              "confira se quem chega pelo anúncio está sendo atendido no mesmo dia. Muitas vezes "
              "o gargalo está aí, não no anúncio."),
    "N4-v1": ("{{contact.first_name}}, estou organizando a agenda das próximas semanas. Se trazer "
              "mais clientes com anúncio estiver nos seus planos, me responde que eu separo um "
              "horário pra você."),
    "N5-v1": ("{{contact.first_name}}, você já testou anunciar com uma oferta específica em vez "
              "de \"fale conosco\"? Costuma trazer contato mais qualificado. Se quiser trocar uma "
              "ideia sobre isso, é só responder."),
    "N6-v1": ("{{contact.first_name}}, esta é minha última mensagem por aqui por um tempo. Se um "
              "dia quiser conversar sobre trazer mais clientes com anúncio, é só me responder — "
              "eu retomo de onde paramos."),
    "TRI-1-v1": ("Que bom falar com você, {{contact.first_name}}! Pra eu não te incomodar à toa, "
                 "me responde só com o número:\n1 — quero conversar sobre trazer mais clientes\n"
                 "2 — agora não, me chama mais pra frente\n3 — não tenho interesse"),
}

SO_MONTAR = "--so-montar" in sys.argv


def tag(t):
    return g.cond("contact_detail", "tags", "index-of-true", [t])


def sem_tag(t):
    return g.cond("contact_detail", "tags", "index-of-false", [t])


def disse(txt, op="contain"):
    return {"conditionType": "contact_reply", "conditionSubType": "message.body",
            "conditionOperator": op, "conditionValue": txt, "__conditionId": g.uid(),
            "ifElseNodeId": "", "__customFieldType__": "standard", "isWait": False}


def sms(codigo):
    return [{"id": g.uid(), "name": "WhatsApp · " + codigo, "type": "sms",
             "attributes": {"type": "sms", "body": MSG[codigo], "attachments": []}},
            g.field_step(TEMPLATE, "Template usado", codigo, "text")]


def opp(status, etapa="CONECTAR"):
    return {"id": g.uid(), "name": "Oportunidade → %s" % status, "type": "create_opportunity",
            "attributes": {"fields": [], "type": "create_opportunity", "pipeline_id": g.PIPELINE,
                           "pipeline_stage_id": g.STAGES[etapa], "opportunity_name": "{{contact.name}}",
                           "opportunity_status": status, "opportunity_source": "", "monetary_value": ""}}


def tarefa(titulo, corpo):
    return {"id": g.uid(), "name": "Add Task", "type": "task-notification",
            "attributes": {"title": titulo,
                           "body": '<p style="margin:0px; padding-left: 0px!important;">' + corpo + "</p>",
                           "assignedTo": "contact.assigned_user", "type": "task_notification",
                           "dueDate": "0", "__customInputs__": {"dueDate": "duration-picker"}}}


# ---------------- Nutricao ----------------
def nutricao():
    passos = []
    ultimo = []
    for n in range(6, 0, -1):
        cod = "N%d-v1" % n
        corpo = sms(cod) + ultimo
        gate = g.Branch("N%d · Ainda em nutrição?" % n,
                        # telefone-invalido: "Numero errado" tambem cai em nutricao - nunca
                        # mandar WhatsApp para um numero que nao e do lead
                        [tag("status-nutricao"), sem_tag("nao-perturbe"), sem_tag("reengajado"),
                         sem_tag("telefone-invalido")],
                        sim=corpo, nao=[])
        ultimo = [g.wait_step(15, "days"), gate]
    passos = [g.tag_step(["triagem-enviada", "reengajamento-ativo"], remove=True)] + ultimo
    return passos


# ---------------- Triagem ----------------
def triagem():
    # reabrir a oportunidade parada em CONECTAR nao muda a etapa -> o gatilho de
    # etapa da 12x30 nao dispara. Entra pelo outro gatilho dela, a tag
    # cad-outbound (tirada antes, senao "tag adicionada" nao dispara).
    reengajar = [g.tag_step(["triagem-enviada", "nutricao-90d", "status-nutricao",
                             "reengajamento-ativo", "cad-inbound", "cad-outbound"], remove=True),
                 opp("open"),
                 g.tag_step(["reengajado", "etapa-conectar", "cad-outbound"]),
                 g.notify_owner_step("Lead reengajado pela nutrição",
                                     "{{contact.name}} respondeu à nutrição que quer conversar e voltou "
                                     "para CONECTAR — a cadência 12x30 já criou o 1º toque."),
                 g.note_step("Nutrição", "Respondeu à triagem: quer conversar. Voltou para CONECTAR "
                                         "e para a cadência 12x30.")]
    desligar = [g.tag_step(["nao-perturbe"]),
                g.tag_step(["triagem-enviada", "nutricao-90d", "reengajamento-ativo"], remove=True),
                {"id": g.uid(), "name": "Set Contact DND", "type": "dnd_contact",
                 "attributes": {"type": "dnd_contact", "dnd_direction": "outbound",
                                "dnd_contact": "enable", "specific_channels": []}},
                opp("lost"),
                g.note_step("Nutrição", "Respondeu à triagem: não tem interesse. Lead desligado "
                                        "(DND, nao-perturbe, perdido).")]
    depois = [g.tag_step(["triagem-enviada"], remove=True),
              g.note_step("Nutrição", "Respondeu à triagem: agora não. Segue na nutrição.")]
    ler = [tarefa("[SINAL] Nutrição: respondeu — ler a mensagem e decidir",
                  "O lead em nutrição respondeu à triagem com algo que o sistema não entendeu. "
                  "Leia a conversa: se quer conversar, mova para CONECTAR; se não quer, marque "
                  "<b>Não ligar</b>.")]
    b_pos = g.Branch("Quer conversar?", [disse("1", "=="), disse("sim", "=="), disse("Sim", "=="),
                                         disse("quero conversar"), disse("tenho interesse"),
                                         disse("pode ligar"), disse("pode me ligar"),
                                         disse("vamos conversar")], operador="or",
                     sim=reengajar, nao=ler)
    b_dep = g.Branch("Agora não?", [disse("2", "=="), disse("agora não"), disse("agora nao"),
                                   disse("mais pra frente"), disse("mais para frente"),
                                   disse("outro momento")], operador="or",
                     sim=depois, nao=[b_pos])
    b_neg = g.Branch("Sem interesse?", [disse("3", "=="), disse("não tenho interesse"),
                                       disse("nao tenho interesse"), disse("sem interesse"),
                                       disse("não quero"), disse("nao quero")], operador="or",
                     sim=desligar, nao=[b_dep])
    # espera 2 min e confere o Opt-out: se a 1a resposta foi "pare de me mandar
    # mensagem", o Opt-out ja pos nao-perturbe e a triagem nao responde
    primeira = [g.wait_step(2, "minutes"),
                g.Branch("Triagem · Não pediu para parar?", [sem_tag("nao-perturbe")],
                         sim=sms("TRI-1-v1") + [g.tag_step(["triagem-enviada"]),
                                                g.note_step("Nutrição", "Lead respondeu à nutrição — triagem enviada.")],
                         nao=[])]
    b_tri = g.Branch("Já recebeu a triagem?", [tag("triagem-enviada")], sim=[b_neg], nao=primeira)
    return [g.Branch("Está em nutrição?", [tag("status-nutricao"), sem_tag("nao-perturbe")],
                     sim=[b_tri], nao=[])]


def resposta(canal):
    return {"status": "draft", "schedule_config": {}, "type": "customer_reply",
            "masterType": "highlevel", "name": "Cliente Respondeu" + (" — Stevo" if canal == 20 else ""),
            "active": True, "triggersChanged": True, "location_id": g.LOC,
            "conditions": [{"operator": "==", "field": "message.type", "value": canal,
                            "title": "Canal de resposta", "type": "select"}]}


def resumo(nome, tpl):
    vivos = {s["id"] for s in tpl}
    print("%s: nós=%d %s" % (nome, len(tpl), dict(Counter(s["type"] for s in tpl))))
    print("  gotos quebrados:", sum(1 for s in tpl if s["type"] == "goto"
                                   and (s.get("attributes") or {}).get("targetNodeId") not in vivos),
          "| mensagens:", [s["name"] for s in tpl if s["type"] == "sms"])


pn, pt = nutricao(), triagem()
if SO_MONTAR:
    resumo(NOME_NUTRI, g.montar(pn))
    resumo(NOME_TRI, g.montar(pt))
else:
    c = g.client()
    for t in ("reengajado", "triagem-enviada"):
        c.create_location_tag(t)
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    g.preencher(c, NUTRI_ID, NOME_NUTRI, pn, [g.tag_trigger("Entrou em nutrição", "nutricao-90d")],
                allow_reentry=True, stop_on_response=False, janela=JANELA)
    wf_tri = ids.get(NOME_TRI) or g.create_workflow(c, NOME_TRI)
    g.preencher(c, wf_tri, NOME_TRI, pt, [resposta(19), resposta(20)],
                allow_reentry=True, stop_on_response=False, janela=JANELA)
    for nome, wf in ((NOME_NUTRI, NUTRI_ID), (NOME_TRI, wf_tri)):
        doc = g.export(c, wf, os.path.join(AQUI, "..", "workflows-json", nome + ".json"))
        resumo(nome + " (" + wf[:8] + ")", doc["workflow"]["workflowData"]["templates"])
