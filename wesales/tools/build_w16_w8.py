"""W16 - Reengajamento 90 dias  e  W8 - Recuperacao de No-show.

Fora dos dois, por falta do canal de WhatsApp: RE-1/RE-2 (W16) e
NS-1/NS-2 (W8). Sao os unicos nos de texto; o resto da regua e tarefa.

SINERGIA CORRIGIDA no W16: o handoff do W12 fez a Cadencia 12x30 ganhar um
gatilho `Contact Tag Added: cad-outbound`. O no 4 do W16 tambem poe
`cad-outbound` - se entrasse antes de `reengajamento-ativo`, a 12x30
dispararia e o lead cairia em DUAS reguas ao mesmo tempo (o portao de
entrada da 12x30 barra `reengajamento-ativo`, mas so se a tag ja estiver
la). Por isso aqui `reengajamento-ativo` entra PRIMEIRO.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

C = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"),
                   encoding="utf-8"))
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))
TENT = C["Tentativa nº"]["id"]
RESULT = C["Resultado da tentativa"]["id"]
WA_NAO = C["WA não atendidas seguidas"]["id"]
PRIOR = C["Prioridade"]["id"]
ENTRADA = C["Entrada em"]["id"]
PRIMEIRA = C["1ª tentativa em"]["id"]
NOSHOWS = C["Nº de no-shows"]["id"]
CALENDARIO = "3uNQFjCEDe7b4gKZJuOZ"

c = g.client()
ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
       if w.get("type") == "workflow"}


def raiz_id(p):
    return p[0].id if isinstance(p[0], g.Branch) else p[0]["id"]


def campos_step(lista, nome="Update contact field"):
    return {"id": g.uid(), "name": nome, "type": "update_contact_field",
            "attributes": {"type": "update_contact_field",
                           "actionType": "update_field_data", "fields": lista}}


def f(campo, titulo, valor, tipo="numerical"):
    return {"field": campo, "value": valor, "title": titulo, "type": tipo,
            "date": ""}


def task_step(titulo, corpo):
    return {"id": g.uid(), "name": "Add Task", "type": "task-notification",
            "attributes": {"title": titulo,
                           "body": '<p style="margin:0px; padding-left: 0px!important;">'
                                   + corpo + "</p>",
                           "assignedTo": "contact.assigned_user",
                           "type": "task_notification",
                           "dueDate": "0",
                           "__customInputs__": {"dueDate": "duration-picker"}}}


def rm_wf(wf):
    return {"id": g.uid(), "name": "Remove from Workflow",
            "type": "remove_from_workflow",
            "attributes": {"type": "remove_from_workflow",
                           "workflow_id": [wf]}}


def entrega(nome, passos, gatilhos, **cfg):
    wf = ids.get(nome) or g.create_workflow(c, nome)
    g.preencher(c, wf, nome, passos, gatilhos, **cfg)
    doc = g.export(c, wf, os.path.join(JSON_DIR, nome + ".json"))
    w = doc["workflow"]
    tpl = (w.get("workflowData") or {}).get("templates") or []
    vivos = {s["id"] for s in tpl}
    quebrados = sum(1 for s in tpl if s["type"] == "goto"
                    and (s.get("attributes") or {}).get("targetNodeId") not in vivos)
    tarefas = [s["attributes"]["title"] for s in tpl
               if s["type"] == "task-notification"]
    print("  nos=%d gotos_quebrados=%d janela=%s" % (len(tpl), quebrados,
                                                     bool(w.get("window"))))
    for t in tarefas:
        print("    " + t)
    print("  " + ("PUBLICADO" if g.publicar(c, wf) else "NAO PUBLICOU"))
    return wf


# ===================== W16 - Reengajamento 90 dias =====================
print("########## Reengajamento 90 dias (W16)")
NOME16 = "Reengajamento 90 dias"
WF16 = ids.get(NOME16) or g.create_workflow(c, NOME16)
ids[NOME16] = WF16

# espera ATE O PROXIMO toque (duracao, nao horario - ver nota no W11)
TR = [(1, (3, "days"), "fila-tel", "telefone"),
      (2, (4, "days"), "fila-tel", "telefone"),
      (3, (3, "days"), "fila-tel", "telefone"),
      (4, None, "fila-tel", "telefone")]


def encerrar_re():
    """Fim da TR4 sem resposta: reabre o relogio de 90 dias."""
    return [campos_step([f(RESULT, "Resultado da tentativa", "", "select")]),
            g.tag_step(["reengajamento-ativo"], remove=True),
            g.tag_step(["nutricao-90d"]),
            g.opp_step("abandoned", g.STAGES["CONECTAR"]),
            rm_wf(WF16)]


def bloco_tr(n, espera_prox, tag_fila, rotulo, proximo):
    depois = proximo if proximo else encerrar_re()
    marcar = [campos_step([f(RESULT, "Resultado da tentativa", "Não atendeu",
                             "select")]),
              g.tag_step(["limpar-tarefas"]), g.goto_step(raiz_id(depois))]
    b10b = g.Branch("TR%d · Sem resposta?" % n,
                    [g.cond("contact_detail", RESULT, "has_no_value", None)],
                    sim=marcar, nao=list(depois))
    b10 = g.Branch("TR%d · Atendeu?" % n,
                   [g.cond("contact_detail", RESULT, "==", "Atendeu")],
                   sim=[rm_wf(WF16)], nao=[b10b])
    corpo = [campos_step([f(RESULT, "Resultado da tentativa", "", "select"),
                          f(TENT, "Tentativa nº", n, "numerical")])]
    if n == 1:
        corpo.append(campos_step([f(PRIMEIRA, "1ª tentativa em", "sim", "text")]))
        corpo.append(g.tag_step(["atraso-1a-tentativa"], remove=True))
    corpo += [g.tag_step([tag_fila]),
              task_step("[CADENCIA] TR%d · Ligar (%s) — Reengajamento"
                        % (n, rotulo), "Régua de reengajamento, toque %d de 4."
                        % n),
              g.tag_step(["toque"])]
    if espera_prox:
        corpo.append(g.wait_step(espera_prox[0], espera_prox[1]))
    corpo += [g.tag_step(["fila-tel", "fila-wa"], remove=True), b10]
    b3 = g.Branch("TR%d · Ainda vale ligar?" % n,
                  [g.cond("opportunities", "pipelineStageId", "==",
                          g.STAGES["CONECTAR"]),
                   g.cond("opportunities", "status", "==", "open"),
                   g.cond("contact_detail", "tags", "index-of-false",
                          ["nao-perturbe"]),
                   g.cond("contact_detail", RESULT, "!=", "Não ligar")],
                  sim=corpo,
                  nao=[g.tag_step(["fila-tel", "fila-wa"], remove=True),
                       g.tag_step(["limpar-tarefas"]), rm_wf(WF16)])
    return [b3]


prox = []
for linha in reversed(TR):
    prox = bloco_tr(*linha, proximo=prox)
regua = prox

reativar = [
    campos_step([f(TENT, "Tentativa nº", 0, "numerical"),
                 f(WA_NAO, "WA não atendidas seguidas", 0, "numerical"),
                 f(RESULT, "Resultado da tentativa", "", "select"),
                 f(PRIOR, "Prioridade", 3, "numerical"),
                 f(ENTRADA, "Entrada em", "sim", "text"),
                 f(PRIMEIRA, "1ª tentativa em", "", "text")],
                "Zera contadores da nova rodada"),
    g.tag_step(["nutricao-90d"], remove=True),
    # reengajamento-ativo ANTES de cad-outbound: ver nota no topo
    g.tag_step(["reengajamento-ativo"]),
    g.tag_step(["cad-inbound"], remove=True),
    g.tag_step(["cad-outbound"]),
    g.opp_step("open", g.STAGES["CONECTAR"]),
] + regua

passos16 = [
    g.wait_step(90, "days"),
    g.Branch("Ainda em nutrição e sem opt-out?",
             [g.cond("opportunities", "status", "==", "abandoned"),
              g.cond("contact_detail", "tags", "index-of-true",
                     ["nutricao-90d"]),
              g.cond("contact_detail", "tags", "index-of-false",
                     ["nao-perturbe"])],
             sim=reativar, nao=[rm_wf(WF16)]),
]
entrega(NOME16, passos16, [g.tag_trigger("Nutricao 90d", "nutricao-90d")],
        allow_reentry=True, stop_on_response=True,
        janela={"days": [1, 2, 3, 4, 5], "startHour": 8, "startMinute": 30,
                "endHour": 18, "endMinute": 30})

# ===================== W8 - Recuperacao de No-show =====================
print("\n########## Recuperação de No-show (W8)")
NOME8 = "Recuperação de No-show"
WF8 = ids.get(NOME8) or g.create_workflow(c, NOME8)
ids[NOME8] = WF8


def em_negociar():
    return [g.cond("opportunities", "pipelineStageId", "==",
                   g.STAGES["NEGOCIAR"]),
            g.cond("opportunities", "status", "==", "open")]


def toque_ns(n, esperas, proximo):
    corpo = [g.tag_step(["fila-tel"]),
             task_step("[CADENCIA] NS%d · Ligar (telefone) — Recuperação de "
                       "no-show" % n, "Lead nao compareceu. Tentativa %d de 3."
                       % n),
             g.tag_step(["toque"])]
    passos = list(corpo)
    for e in esperas:
        passos.append(e)
    if proximo:
        passos.append(g.Branch("NS%d · Ainda vale recuperar?" % n,
                               em_negociar()
                               + [g.cond("contact_detail", "tags",
                                         "index-of-false", ["nao-perturbe"]),
                                  g.cond("contact_detail", "tags",
                                         "index-of-false", ["pausado"])],
                               sim=list(proximo), nao=[rm_wf(WF8)]))
    return passos


fim_ns = [campos_step([f(RESULT, "Resultado da tentativa", "", "select")]),
          g.tag_step(["fila-tel"], remove=True),
          g.tag_step(["nutricao-90d"]),
          g.opp_step("abandoned", g.STAGES["NEGOCIAR"])]
ns3 = toque_ns(3, [g.wait_step(1, "days")], fim_ns)
ns2 = toque_ns(2, [g.wait_step(2, "days")], ns3)
ns1 = toque_ns(1, [g.wait_step(1, "days")], ns2)

descarte = [g.tag_step(["fila-tel"], remove=True),
            g.tag_step(["limpar-tarefas"]),
            g.opp_step("lost", g.STAGES["NEGOCIAR"]),
            g.note_step("Descartado por no-show",
                        "Descartado após o 2º no-show seguido sem reagendar — "
                        "regra de proteção de agenda do closer (R-12)"),
            g.notify_user_step(
                "Descarte automático por no-show",
                "{{contact.name}} descartado automaticamente após o 2º "
                "no-show — nenhuma ação necessária, é a regra de proteção "
                "de agenda.")]

passos8 = [
    g.Branch("Em NEGOCIAR e aberta?", em_negociar(),
             sim=[g.math_step(NOSHOWS, "add", 1),
                  g.Branch("Já é o segundo no-show?",
                           [g.cond("contact_detail", NOSHOWS, ">=", "2")],
                           sim=descarte, nao=ns1)],
             nao=[]),
]
gat8 = [{"status": "draft", "schedule_config": {}, "type": "appointment",
         "masterType": "highlevel", "name": "Status Do Agendamento",
         "active": True, "triggersChanged": True, "location_id": g.LOC,
         "conditions": [
             {"operator": "==", "field": "appointment.eventType",
              "value": "normal", "title": "Tipo de evento", "type": "select"},
             {"operator": "==", "field": "calendar.id", "value": CALENDARIO,
              "title": "In calendar", "type": "select", "id": g.uid()},
             {"operator": "==", "field": "appointment.status",
              "value": "noshow", "title": "Appointment status is",
              "type": "select", "id": g.uid()},
             {"operator": "is-any-of", "field": "contactMode",
              "value": ["contact"], "type": "input"}]}]
entrega(NOME8, passos8, gat8, allow_reentry=True, stop_on_response=True,
        janela={"days": [1, 2, 3, 4, 5], "startHour": 8, "startMinute": 30,
                "endHour": 18, "endMinute": 30})
