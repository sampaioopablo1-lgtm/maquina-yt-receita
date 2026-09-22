"""W12 - Cadencia Inbound (IMPLEMENTACAO-WORKFLOWS.md, W12).

Regua curta e rapida para quem chegou por formulario: 5 toques em ~2 dias,
e no fim o lead passa para a Cadencia 12x30.

Fora, por falta do canal de WhatsApp: MI-0 (abertura) e MI-F (handoff) -
os dois unicos nos de texto. Os toques sao tarefas de LIGAR.

DESVIO CONSCIENTE: a spec separa o no 8 (esperar o resultado, com limite =
delta ate a proxima tentativa) do no 1 da tentativa seguinte (esperar esse
mesmo delta). Como o `Wait -> Condition` nao tem formato conhecido neste
build, os dois viraram UMA espera do tamanho do delta - senao o lead
esperaria o dobro. O efeito pratico e o mesmo: a proxima tarefa nasce na
hora certa.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "Cadência Inbound"
C = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"),
                   encoding="utf-8"))
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))
TENT = C["Tentativa nº"]["id"]
RESULT = C["Resultado da tentativa"]["id"]
WA_NAO = C["WA não atendidas seguidas"]["id"]
PERM_WA = C["Permissão WhatsApp"]["id"]
PRIOR = C["Prioridade"]["id"]
ENTRADA = C["Entrada em"]["id"]
PRIMEIRA = C["1ª tentativa em"]["id"]
SITE = C["Site"]["id"]
INSTA = C["Instagram"]["id"]

# TI, espera ate o proximo toque, canal, tag de fila, rotulo do canal
TOQUES = [
    (1, (25, "minutes"), "telefone", "fila-tel", "telefone"),
    (2, (90, "minutes"), "telefone", "fila-tel", "telefone"),
    (3, (22, "hours"), "whatsapp", "fila-wa", "WhatsApp"),
    (4, (2, "days"), "whatsapp", "fila-wa", "WhatsApp"),
    (5, None, "telefone", "fila-tel", "telefone"),
]
ESPERA_INICIAL = (5, "minutes")

c = g.client()
ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
       if w.get("type") == "workflow"}
WF = ids.get(NOME) or g.create_workflow(c, NOME)
W11 = ids.get("Cadência 12x30")
print("workflow: %s | Cadencia 12x30: %s" % (WF, W11))


def raiz_id(p):
    return p[0].id if isinstance(p[0], g.Branch) else p[0]["id"]


def campos_step(lista, nome_no="Update contact field"):
    return {"id": g.uid(), "name": nome_no, "type": "update_contact_field",
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
                           "dueDate": "{{right_now.date}}",
                           "__customInputs__": {"dueDate": "duration-picker"}}}


def sair():
    return [g.tag_step(["fila-tel", "fila-wa", "fila-quente"], remove=True),
            g.tag_step(["limpar-tarefas"]),
            {"id": g.uid(), "name": "Remove from Workflow",
             "type": "remove_from_workflow",
             "attributes": {"type": "remove_from_workflow",
                            "workflow_id": [WF]}}]


def handoff():
    """Fim da TI5 sem resposta: passa o bastao para a Cadencia 12x30.

    A spec pede um `Add to Workflow`. Esse no exige `input_trigger_params`,
    cujo formato nao aparece em lugar nenhum (nem no catalogo, nem no JS do
    builder) e nenhuma das formas testadas passou na publicacao.
    Troquei por algo mais simples e mais no espirito do projeto: o handoff
    vira TAG. Tira `cad-inbound`, poe `cad-outbound`, e a 12x30 ganhou um
    segundo gatilho `Contact Tag Added: cad-outbound`. Efeito igual, com
    nos ja provados - e de quebra qualquer lead marcado como outbound entra
    na regua, venha de onde vier.
    """
    return [
        g.tag_step(["cad-inbound"], remove=True),
        g.tag_step(["cad-outbound"]),
        {"id": g.uid(), "name": "Remove from Workflow",
         "type": "remove_from_workflow",
         "attributes": {"type": "remove_from_workflow",
                        "workflow_id": [WF]}},
    ]


def bloco(n, espera_prox, canal, tag_fila, rotulo, proximo):
    depois = proximo if proximo else handoff()

    marcar = [campos_step([f(RESULT, "Resultado da tentativa", "Não atendeu",
                             "select")]),
              g.tag_step(["limpar-tarefas"]),
              g.goto_step(raiz_id(depois))]
    b10b = g.Branch("TI%d · Sem resposta registrada?" % n,
                    [g.cond("contact_detail", RESULT, "has_no_value", None)],
                    sim=marcar, nao=list(depois))
    b10 = g.Branch("TI%d · Atendeu?" % n,
                   [g.cond("contact_detail", RESULT, "==", "Atendeu")],
                   sim=[{"id": g.uid(), "name": "Remove from Workflow",
                         "type": "remove_from_workflow",
                         "attributes": {"type": "remove_from_workflow",
                                        "workflow_id": [WF]}}],
                   nao=[b10b])

    corpo = [campos_step([f(RESULT, "Resultado da tentativa", "", "select"),
                          f(TENT, "Tentativa nº", n, "numerical")])]
    if n == 1:
        corpo.append(campos_step([f(PRIMEIRA, "1ª tentativa em", "sim",
                                    "text")]))
        corpo.append(g.tag_step(["atraso-1a-tentativa"], remove=True))
    corpo += [
        g.tag_step([tag_fila]),
        task_step("[CADENCIA] TI%d · Ligar (%s) — Inbound" % (n, rotulo),
                  "Lead inbound: retorno rapido. Toque %d de 5." % n),
        g.tag_step(["toque"]),
        g.notify_owner_step(
            "Lead inbound aguardando retorno",
            "Lead inbound {{contact.name}} aguardando retorno — TI%d." % n),
    ]
    if espera_prox:
        corpo.append(g.wait_step(espera_prox[0], espera_prox[1]))
    corpo += [g.tag_step(["fila-tel", "fila-wa"], remove=True), b10]

    conds = [g.cond("opportunities", "pipelineStageId", "==",
                    g.STAGES["CONECTAR"]),
             g.cond("opportunities", "status", "==", "open"),
             g.cond("contact_detail", "tags", "index-of-false",
                    ["nao-perturbe"]),
             g.cond("contact_detail", RESULT, "!=", "Não ligar")]
    if canal == "telefone":
        conds.append(g.cond("contact_detail", "tags", "index-of-false",
                            ["telefone-invalido"]))
    b3 = g.Branch("TI%d · Ainda vale ligar?" % n, conds,
                  sim=corpo, nao=sair())

    # pausa individual: laco de 30 min (nao 1 dia, como no outbound)
    b15 = g.Branch("TI%d · Lead pausado?" % n,
                   [g.cond("contact_detail", "tags", "index-of-true",
                           ["pausado"])],
                   sim=[], nao=[b3])
    b15.sim = [g.wait_step(30, "minutes"), g.goto_step(b15.id)]
    return [b15]


proximo = []
for linha in reversed(TOQUES):
    proximo = bloco(*linha, proximo=proximo)
cadencia = [g.wait_step(*ESPERA_INICIAL)] + proximo

# ---------------- no 0 ----------------
atribuir = {"id": g.uid(), "name": "Assign user", "type": "assign_user",
            "attributes": {"only_unassigned_contact": False, "total_index": 1,
                           "traffic_split": "equally",
                           "traffic_weightage": {g.USER: 1},
                           "traffic_index": [{"id": g.USER, "indexes": [1]}],
                           "user_list": [g.USER], "type": "assign_user"}}
b08 = g.Branch("Sem dono?",
               [g.cond("contact_detail", "assigned_to", "has_no_value", None)],
               sim=[atribuir, g.goto_step(raiz_id(cadencia))],
               nao=list(cadencia))

comum = [campos_step([f(PRIOR, "Prioridade", 5, "numerical"),
                      f(ENTRADA, "Entrada em", "sim", "text")]),
         g.tag_step(["fila-quente"]),
         b08]
b04 = g.Branch("Permissão de WhatsApp em branco?",
               [g.cond("contact_detail", PERM_WA, "has_no_value", None)],
               sim=[campos_step([f(PERM_WA, "Permissão WhatsApp",
                                   "Não solicitado", "select")]),
                    g.goto_step(raiz_id(comum))],
               nao=comum)

inicio = [campos_step([f(TENT, "Tentativa nº", 0, "numerical"),
                       f(WA_NAO, "WA não atendidas seguidas", 0, "numerical"),
                       f(RESULT, "Resultado da tentativa", "", "select")],
                      "Inicializa contadores"),
          b04]

b00c = g.Branch("Tem site ou Instagram?",
                [g.cond("contact_detail", SITE, "has_value", None),
                 g.cond("contact_detail", INSTA, "has_value", None)],
                operador="or",
                sim=[g.opp_step("abandoned", g.STAGES["CONECTAR"]),
                     g.tag_step(["nutricao-90d"])],
                nao=[g.opp_step("lost", g.STAGES["CONECTAR"]),
                     g.notify_user_step(
                         "Lead inbound sem telefone",
                         "Lead inbound sem telefone: {{contact.name}} — "
                         "revisar o formulário de origem.")])

sem_tel = [g.Branch("Contato sem telefone?",
                    [g.cond("contact_detail", "phone", "has_no_value", None)],
                    sim=[g.tag_step(["telefone-invalido"]), b00c],
                    nao=inicio)]

# so entra quem tem cad-inbound (a spec poe no gatilho; gatilho combina com E)
passos = [g.Branch("É lead de inbound?",
                   [g.cond("contact_detail", "tags", "index-of-true",
                           ["cad-inbound"])],
                   sim=sem_tel, nao=[])]

gatilho = {"status": "draft", "schedule_config": {},
           "type": "pipeline_stage_updated", "masterType": "highlevel",
           "name": "Etapa Do Funil Alterada", "active": True,
           "triggersChanged": True, "location_id": g.LOC,
           "conditions": [
               {"operator": "==", "field": "opportunity.pipelineId",
                "value": g.PIPELINE, "title": "No pipeline", "type": "select"},
               {"operator": "==", "field": "opportunity.pipelineStageId",
                "value": g.STAGES["CONECTAR"], "title": "Movido para o estágio",
                "type": "select", "id": "moved-to-stage"}]}

g.preencher(c, WF, NOME, passos, [gatilho],
            allow_reentry=False, stop_on_response=True,
            janela={"days": [1, 2, 3, 4, 5], "startHour": 8,
                    "startMinute": 30, "endHour": 18, "endMinute": 30})

doc = g.export(c, WF, os.path.join(JSON_DIR, NOME + ".json"))
w = doc["workflow"]
tpl = (w.get("workflowData") or {}).get("templates") or []
vivos = {s["id"] for s in tpl}
from collections import Counter
print("nos=%d janela=%s" % (len(tpl), w.get("window")))
print(Counter(s["type"] for s in tpl))
print("gotos quebrados:", sum(1 for s in tpl if s["type"] == "goto"
                              and (s.get("attributes") or {}).get("targetNodeId") not in vivos))
print("tarefas:", [s["attributes"]["title"] for s in tpl
                   if s["type"] == "task-notification"])
print("PUBLICADO" if g.publicar(c, WF) else "NAO PUBLICOU")
