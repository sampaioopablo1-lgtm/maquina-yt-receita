"""W11 - Cadencia 12x30 (IMPLEMENTACAO-WORKFLOWS.md, W11).

Monta o NUCLEO da cadencia: no 0 de inicializacao + os 12 toques completos
(esperas, portao de pausa, teto de toques, portao de saida, tarefa, tag de
fila, contadores e roteamento pelo Resultado da tentativa).

O QUE FICA DE FORA, E POR QUE (fallback combinado com o dono em 21/09/2026):
- M1 (split A/B + mensagens M1-a/M1-b), M2 e M3: sao os UNICOS nos que
  enviam texto. Os nos de WhatsApp desta versao exigem `template_id` e
  `from_phone_number` obrigatorios, e nao existe template nem numero
  enquanto o canal nao estiver conectado - nem como rascunho passam.
  Os 12 toques NAO enviam mensagem: sao tarefas de LIGAR (por telefone ou
  por chamada de WhatsApp), entao o nucleo funciona inteiro sem o canal.
- Entrada na IA (2.7a/2.7b): o workflow 'Qualificação por IA no WhatsApp'
  esta vazio; ligar para la agora nao faria nada.

DESVIO CONSCIENTE no no 8: a spec pede `Wait -> Condition` (segue assim que
`Resultado da tentativa` for preenchido, com limite hoje 18:30). O tipo
`condition` existe neste build mas o JS nao expoe o formato dos atributos,
e chutar num no que se repete 12 vezes e caro. Usei `Wait ate 18:30`, que
entrega o limite. Perde-se sair mais cedo quando o SDR registra de manha -
sem impacto visivel, porque quem reage na hora ao resultado e o
Pos-ligacao, nao este workflow. Revisitar quando o formato aparecer.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "Cadência 12x30"
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
TOQUES = C["Toques na semana"]["id"]
SITE = C["Site"]["id"]
INSTA = C["Instagram"]["id"]

# T, espera ATE O PROXIMO toque, canal, tag de fila, titulo da tarefa
#
# POR QUE DURACAO E NAO HORARIO (corrigido em 21/09/2026 depois da
# simulacao): o wait `specific_date` exige `specificDate` e
# `specificTimePeriod`; sem eles o GHL entende "a data ja passou" e SEGUE
# DIRETO. Num teste real o lead atravessou T1 e T2 em 90 segundos. O wait
# `time` com janela de retomada tambem nao vale: o validador passa a exigir
# `Condition` e `Start`. Duracao e o unico tipo comprovado.
# Os intervalos abaixo sao as diferencas entre os horarios da tabela da
# spec, e somam os mesmos ~30 dias.
TOQUES_TAB = [
    (1, (6, "hours"), "telefone", "fila-tel", "[CADENCIA] T1 · Ligar (telefone)"),
    (2, (17, "hours"), "whatsapp", "fila-wa", "[CADENCIA] T2 · Ligar (WhatsApp)"),
    (3, (8, "hours"), "telefone", "fila-tel", "[CADENCIA] T3 · Ligar (telefone)"),
    (4, (2, "days"), "whatsapp", "fila-wa", "[CADENCIA] T4 · Ligar (WhatsApp)"),
    (5, (3, "days"), "whatsapp", "fila-wa", "[CADENCIA] T5 · Ligar (WhatsApp)"),
    (6, (6, "hours"), "telefone", "fila-tel", "[CADENCIA] T6 · Ligar (telefone)"),
    (7, (3, "days"), "whatsapp", "fila-wa", "[CADENCIA] T7 · Ligar (WhatsApp)"),
    (8, (4, "days"), "telefone", "fila-tel", "[CADENCIA] T8 · Ligar (telefone)"),
    (9, (6, "days"), "whatsapp", "fila-wa", "[CADENCIA] T9 · Ligar (WhatsApp)"),
    (10, (10, "days"), "telefone", "fila-tel", "[CADENCIA] T10 · Ligar (telefone)"),
    (11, (7, "hours"), "telefone", "fila-tel", "[CADENCIA] T11 · Ligar (telefone)"),
    (12, None, "whatsapp", "fila-wa", "[CADENCIA] T12 · Ligar (WhatsApp)"),
]

c = g.client()
ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
       if w.get("type") == "workflow"}
WF = ids.get(NOME) or g.create_workflow(c, NOME)
print("workflow: " + WF)


def raiz_id(passos):
    """Id do primeiro no de uma lista (no simples ou Branch)."""
    p0 = passos[0]
    return p0.id if isinstance(p0, g.Branch) else p0["id"]


def campos_step(lista, nome_no="Update contact field"):
    """Update Contact Field com varios campos de uma vez."""
    return {"id": g.uid(), "name": nome_no, "type": "update_contact_field",
            "attributes": {"type": "update_contact_field",
                           "actionType": "update_field_data",
                           "fields": lista}}


def f(campo, titulo, valor, tipo="numerical"):
    return {"field": campo, "value": valor, "title": titulo, "type": tipo,
            "date": ""}


def task_step(titulo, corpo):
    return {"id": g.uid(), "name": "Add Task", "type": "task-notification",
            "attributes": {
                "title": titulo,
                "body": '<p style="margin:0px; padding-left: 0px!important;">'
                        + corpo + "</p>",
                "assignedTo": "contact.assigned_user",
                "type": "task_notification",
                "dueDate": "0",
                "__customInputs__": {"dueDate": "duration-picker"}}}


def sair_da_cadencia():
    """No 3b: limpa a fila, marca para higiene e sai."""
    return [
        g.tag_step(["fila-tel", "fila-wa", "fila-quente"], remove=True),
        g.tag_step(["limpar-tarefas"]),
        {"id": g.uid(), "name": "Remove from Workflow",
         "type": "remove_from_workflow",
         "attributes": {"type": "remove_from_workflow", "workflow_id": [WF]}},
    ]


def corpo_toque(n, espera_prox, tag_fila, titulo, proximo):
    """Nos 5 a 10b de um toque. `proximo` e a lista de passos do toque
    seguinte (ou [] no ultimo)."""
    # 10b: resultado vazio -> marca Nao atendeu e segue; senao segue
    # o proximo toque MORA no ramo 'nao'; o ramo 'sim' salta para ele.
    # duplicar a lista nos dois ramos faria a arvore dobrar a cada toque.
    marcar = [campos_step([f(RESULT, "Resultado da tentativa", "Não atendeu",
                             "select")]),
              g.tag_step(["limpar-tarefas"])]
    if proximo:
        marcar = marcar + [g.goto_step(raiz_id(proximo))]
    b10b = g.Branch(
        "T%d · Sem resposta registrada?" % n,
        [g.cond("contact_detail", RESULT, "has_no_value", None)],
        sim=marcar,
        nao=list(proximo),
    )
    b10 = g.Branch(
        "T%d · Fechou o assunto?" % n,
        [g.cond("contact_detail", RESULT, "==", "Atendeu")],
        sim=[{"id": g.uid(), "name": "Remove from Workflow",
              "type": "remove_from_workflow",
              "attributes": {"type": "remove_from_workflow",
                             "workflow_id": [WF]}}],
        nao=[b10b],
    )
    passos = [
        campos_step([f(RESULT, "Resultado da tentativa", "", "select"),
                     f(TENT, "Tentativa nº", n, "numerical")]),
    ]
    if n == 1:
        passos.append(campos_step([f(PRIMEIRA, "1ª tentativa em", "sim",
                                     "text")]))
        passos.append(g.tag_step(["atraso-1a-tentativa"], remove=True))
    passos += [
        g.tag_step([tag_fila]),
        task_step(titulo, "Tarefa da cadência 12x30, toque %d." % n),
        g.tag_step(["toque"]),
    ]
    if espera_prox:
        passos.append(g.wait_step(espera_prox[0], espera_prox[1]))
    passos += [g.tag_step(["fila-tel", "fila-wa"], remove=True), b10]
    return passos


def bloco_toque(n, espera_prox, canal, tag_fila, titulo, proximo):
    """Um toque inteiro: portao de pausa, teto, portao de saida e corpo.
    A espera fica DEPOIS da tarefa (ver nota na tabela)."""
    corpo = corpo_toque(n, espera_prox, tag_fila, titulo, proximo)

    # portao de saida (no 3)
    conds = [g.cond("opportunities", "pipelineStageId", "==",
                    g.STAGES["CONECTAR"]),
             g.cond("opportunities", "status", "==", "open"),
             g.cond("contact_detail", "tags", "index-of-false",
                    ["nao-perturbe"]),
             g.cond("contact_detail", RESULT, "!=", "Não ligar")]
    if canal == "telefone":
        conds.append(g.cond("contact_detail", "tags", "index-of-false",
                            ["telefone-invalido"]))
    b3 = g.Branch("T%d · Ainda vale ligar?" % n, conds,
                  sim=corpo, nao=sair_da_cadencia())

    # 2.5c teto de toques da semana (laco de 1 dia)
    b25c = g.Branch("T%d · Teto de toques da semana?" % n,
                    [g.cond("contact_detail", TOQUES, ">=", "6")],
                    sim=[], nao=[b3])
    b25c.sim = [g.wait_step(1, "days"), g.goto_step(b25c.id)]

    # 2.5 represado pelo SDR (laco de 1 dia)
    b25 = g.Branch("T%d · Lead pausado?" % n,
                   [g.cond("contact_detail", "tags", "index-of-true",
                           ["pausado"])],
                   sim=[], nao=[b25c])
    b25.sim = [g.wait_step(1, "days"), g.goto_step(b25.id)]

    return [b25]


# monta de tras para frente: o toque n precisa do n+1 pronto
proximo = []
for linha in reversed(TOQUES_TAB):
    proximo = bloco_toque(*linha, proximo=proximo)
cadencia = proximo

# ---------------- no 0: inicializacao ----------------
atribuir = {"id": g.uid(), "name": "Assign user", "type": "assign_user",
            "attributes": {"only_unassigned_contact": False, "total_index": 1,
                           "traffic_split": "equally",
                           "traffic_weightage": {g.USER: 1},
                           "traffic_index": [{"id": g.USER, "indexes": [1]}],
                           "user_list": [g.USER], "type": "assign_user"}}
b07 = g.Branch(
    "Sem dono?",
    [g.cond("contact_detail", "assigned_to", "has_no_value", None)],
    sim=[atribuir, g.goto_step(raiz_id(cadencia))],
    nao=list(cadencia),
)

# a continuacao comum mora no ramo 'nao'; o 'sim' grava o campo e salta
comum = [campos_step([f(PRIOR, "Prioridade", 3, "numerical"),
                      f(ENTRADA, "Entrada em", "sim", "text")]),
         b07]
b04 = g.Branch(
    "Permissão de WhatsApp em branco?",
    [g.cond("contact_detail", PERM_WA, "has_no_value", None)],
    sim=[campos_step([f(PERM_WA, "Permissão WhatsApp", "Não solicitado",
                        "select")]),
         g.goto_step(raiz_id(comum))],
    nao=comum,
)

inicio = [
    campos_step([f(TENT, "Tentativa nº", 0, "numerical"),
                 f(WA_NAO, "WA não atendidas seguidas", 0, "numerical"),
                 f(RESULT, "Resultado da tentativa", "", "select")],
                "Inicializa contadores"),
    b04,
]

# no 0.0: sem telefone nao entra na regua
b00c = g.Branch(
    "Tem site ou Instagram?",
    [g.cond("contact_detail", SITE, "has_value", None),
     g.cond("contact_detail", INSTA, "has_value", None)],
    operador="or",
    sim=[g.opp_step("abandoned", g.STAGES["CONECTAR"]),
         g.tag_step(["nutricao-90d"])],
    nao=[g.opp_step("lost", g.STAGES["CONECTAR"]),
         g.notify_user_step(
             "Lead sem telefone",
             "Lead sem telefone: {{contact.name}} — revisar a fonte da lista "
             "antes de qualquer tentativa.")],
)

sem_telefone = [g.Branch(
    "Contato sem telefone?",
    [g.cond("contact_detail", "phone", "has_no_value", None)],
    sim=[g.tag_step(["telefone-invalido"]), b00c],
    nao=inicio,
)]

# PORTAO DE ENTRADA: esta e a regua OUTBOUND. Lead de inbound ou de
# reengajamento tem regua propria (W12 / W16) e nao pode entrar aqui.
# A spec poe esses dois filtros no gatilho, mas condicao de gatilho combina
# com E e nao aceita 'nao inclui tag' - entao viram o primeiro no.
passos = [g.Branch(
    "É lead de outra régua?",
    [g.cond("contact_detail", "tags", "index-of-true", ["cad-inbound"]),
     g.cond("contact_detail", "tags", "index-of-true",
            ["reengajamento-ativo"])],
    operador="or",
    sim=[],                 # tem regua propria: nao entra
    nao=sem_telefone,
)]

gatilho = {
    "status": "draft", "schedule_config": {},
    "type": "pipeline_stage_updated", "masterType": "highlevel",
    "name": "Etapa Do Funil Alterada", "active": True,
    "triggersChanged": True, "location_id": g.LOC,
    "conditions": [
        {"operator": "==", "field": "opportunity.pipelineId",
         "value": g.PIPELINE, "title": "No pipeline", "type": "select"},
        {"operator": "==", "field": "opportunity.pipelineStageId",
         "value": g.STAGES["CONECTAR"], "title": "Movido para o estágio",
         "type": "select", "id": "moved-to-stage"},
    ],
}

# Allow Re-entry DESLIGADO (D-06) e Stop on Response LIGADO, como a spec pede
g.preencher(c, WF, NOME, passos, [gatilho],
            allow_reentry=False, stop_on_response=True,
            janela={"days": [1, 2, 3, 4, 5], "startHour": 8,
                    "startMinute": 30, "endHour": 18, "endMinute": 30})

doc = g.export(c, WF, os.path.join(JSON_DIR, NOME + ".json"))
w = doc["workflow"]
tpl = (w.get("workflowData") or {}).get("templates") or []
vivos = {s["id"] for s in tpl}
from collections import Counter
print("nos=%d  status=%s  re-entry=%s  stopOnResponse=%s"
      % (len(tpl), w.get("status"), w.get("allowMultiple"),
         w.get("stopOnResponse")))
print(Counter(s["type"] for s in tpl))
quebrados = [s["id"] for s in tpl if s["type"] == "goto"
             and (s.get("attributes") or {}).get("targetNodeId") not in vivos]
print("gotos quebrados: %d" % len(quebrados))
tarefas = [s for s in tpl if s["type"] == "task-notification"]
print("tarefas criadas: %d (esperado 12)" % len(tarefas))
for t in tarefas:
    print("   " + t["attributes"]["title"])
