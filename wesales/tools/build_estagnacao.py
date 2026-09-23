"""A5 - os dois pontos em que um negocio empaca depois da reuniao (W22 adaptado
ao funil de 23/09/2026: o "Sim" do closer acontece em REUNIAO DE DIAGNOSTICO e o
closer move para NEGOCIAR ao apresentar a proposta).

1. "Proposta Pendente": `Reunião foi qualificada` virou Sim -> 3 dias -> se o
   lead ainda esta em REUNIAO (tag etapa-reuniao) -> tag `proposta-pendente`,
   aviso ao gestor, nota. Portao de aviso unico pela tag (o closer pode editar
   o veredito varias vezes).
2. "Negociação Estagnada": oportunidade movida para NEGOCIAR -> 5 dias -> se
   ainda em NEGOCIAR e aberta -> tag `negociacao-estagnada`, aviso ao gestor,
   tarefa [CLOSER] Decidir a negociacao, nota. Na entrada tira as duas tags
   (nova rodada; e a proposta deixou de estar pendente).

Uso: python build_estagnacao.py [--so-montar]
     TESTE=1 python build_estagnacao.py  -> copias ZZ com esperas de 2 min
"""
import io
import os
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

TESTE = os.environ.get("TESTE") == "1"
SO = "--so-montar" in sys.argv
QUALIF = "c470gqXWCkwqE9yVrcEi"      # Reunião foi qualificada
JANELA = {"days": [1, 2, 3, 4, 5], "startHour": 8, "startMinute": 30, "endHour": 18, "endMinute": 30}
AQUI = os.path.dirname(os.path.abspath(__file__))


def espera(dias):
    return g.wait_step(2, "minutes") if TESTE else g.wait_step(dias, "days")


def tag(t):
    return g.cond("contact_detail", "tags", "index-of-true", [t])


def sem_tag(t):
    return g.cond("contact_detail", "tags", "index-of-false", [t])


def tarefa(titulo, corpo):
    return {"id": g.uid(), "name": "Add Task", "type": "task-notification",
            "attributes": {"title": titulo,
                           "body": '<p style="margin:0px; padding-left: 0px!important;">' + corpo + "</p>",
                           "assignedTo": "contact.assigned_user", "type": "task_notification",
                           "dueDate": "0", "__customInputs__": {"dueDate": "duration-picker"}}}


def proposta_pendente():
    alerta = [g.tag_step(["proposta-pendente"]),
              g.notify_user_step("Proposta parada",
                                 "{{contact.name}} foi aprovado na reunião de diagnóstico há 3 dias e a "
                                 "proposta ainda não foi apresentada (continua em REUNIÃO DE DIAGNÓSTICO)."),
              g.note_step("Alerta de saúde", "Qualificado pelo closer há 3 dias e sem proposta apresentada.")]
    return [g.Branch("Veredito é Sim?", [g.cond("contact_detail", QUALIF, "==", "Sim")],
                     sim=[espera(3),
                          g.Branch("Ainda em REUNIÃO, sem aviso anterior?",
                                   [tag("etapa-reuniao"), sem_tag("proposta-pendente"),
                                    g.cond("contact_detail", QUALIF, "==", "Sim")],
                                   sim=alerta, nao=[])],
                     nao=[])]


def negociacao_estagnada():
    alerta = [g.tag_step(["negociacao-estagnada"]),
              g.notify_user_step("Negociação parada",
                                 "{{contact.name}} está em NEGOCIAR há 5 dias sem ganho nem perda. "
                                 "Cobrar do closer uma decisão."),
              tarefa("[CLOSER] Decidir a negociação",
                     "A proposta está em NEGOCIAR há 5 dias sem decisão. Ligue para o lead e registre: "
                     "fechou (mover para FORMALIZAR + Ganho) ou perdeu (Perdido + motivo)."),
              g.note_step("Alerta de saúde", "NEGOCIAR há 5 dias sem decisão do closer.")]
    return [g.tag_step(["proposta-pendente", "negociacao-estagnada"], remove=True),
            espera(5),
            g.Branch("Ainda em NEGOCIAR e aberta?",
                     [g.cond("opportunities", "pipelineStageId", "==", g.STAGES["NEGOCIAR"]),
                      g.cond("opportunities", "status", "==", "open")],
                     sim=alerta, nao=[])]


def gat_qualif():
    return {"status": "draft", "schedule_config": {}, "type": "contact_changed", "masterType": "highlevel",
            "name": "Reunião foi qualificada alterada", "active": True, "triggersChanged": True,
            "location_id": g.LOC,
            "conditions": [{"operator": "has-changed", "field": "contact." + QUALIF,
                            "title": "Reunião foi qualificada", "type": "select", "id": QUALIF}]}


def gat_negociar():
    return {"status": "draft", "schedule_config": {}, "type": "pipeline_stage_updated",
            "masterType": "highlevel", "name": "Movido para NEGOCIAR", "active": True,
            "triggersChanged": True, "location_id": g.LOC,
            "conditions": [{"operator": "==", "field": "opportunity.pipelineId", "value": g.PIPELINE,
                            "title": "No pipeline", "type": "select"},
                           {"operator": "==", "field": "opportunity.pipelineStageId",
                            "value": g.STAGES["NEGOCIAR"], "title": "Movido para o estágio",
                            "type": "select", "id": "moved-to-stage"}]}


PECAS = [("Proposta Pendente", proposta_pendente(), gat_qualif()),
         ("Negociação Estagnada", negociacao_estagnada(), gat_negociar())]
c = None if SO else g.client()
if c:
    for t in ("proposta-pendente", "negociacao-estagnada"):
        c.create_location_tag(t)
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
for nome, passos, gat in PECAS:
    nome = ("ZZ TESTE " + nome) if TESTE else nome
    if SO:
        tpl = g.montar(passos)
    else:
        wf = ids.get(nome) or g.create_workflow(c, nome)
        g.preencher(c, wf, nome, passos, [gat], allow_reentry=True, stop_on_response=False,
                    janela=None if TESTE else JANELA)
        tpl = g.export(c, wf, os.path.join(AQUI, "..", "workflows-json", nome + ".json"))["workflow"]["workflowData"]["templates"]
        print("  publicar:", g.publicar(c, wf), wf)
    print("%s: nós=%d %s" % (nome, len(tpl), dict(Counter(s["type"] for s in tpl))))
