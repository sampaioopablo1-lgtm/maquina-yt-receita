"""W11 - Cadencia 12x30 MULTICANAL (PLANO-MULTICANAL.md, D2-D14).

Objetivo da etapa CONECTAR: conectar + qualificar + agendar. Esta cadencia
cuida do "conectar": 12 toques em ~30 dias, cada toque e um DIA com roteiro
(ligacao pelo WhatsApp dentro do GHL via Stevo Voice, ligacao normal, e em
alguns toques mensagem de WhatsApp AUTOMATICA). Quem atende sai daqui e vai
para o workflow "Fechar Horario" (fase final de CONECTAR).

Regras novas desta versao (22-23/09/2026, decisoes do dono):
- D6: WhatsApp primeiro. Com 3 ligacoes de WhatsApp seguidas nao atendidas
  (campo `WA nao atendidas seguidas`), o toque passa a comecar pela ligacao
  normal - protege o numero da Stevo.
- D5: mensagem automatica = no `sms` (a Stevo entra no GHL pelo canal de SMS
  e entrega como WhatsApp). Sai 2 h depois da tarefa, so se o lead ainda nao
  conversou. Resposta do lead tira do workflow (Stop on Response) e a
  Interceptacao de Sinal cria "ligar agora".
- D9: Pediu retorno -> a cadencia PAUSA (laco de 1 h) enquanto o resultado
  for "Pediu retorno"; o SDR liga no horario combinado e reclassifica.
- D13: janela seg-sex 08:30-18:30 - nenhuma tarefa nasce no fim de semana.
- D14: tag `sdr-lotado` (posta pela Faxina quando o SDR passa de 100
  toques/dia ou tem 50+ tarefas vencidas) segura o toque em laco de 1 h.
- Relogio: `{{right_now}}` puro grava [object Object] (medido 22/09) - usa
  `{{right_now.date}} {{right_now.time}}`.
- Fim: 12 toques sem conversa -> oportunidade `abandoned` + `nutricao-90d`.

POR QUE DURACAO E NAO HORARIO (21/09/2026): o wait `specific_date` sem data
segue direto; duracao e o unico tipo comprovado.

Teste: W11_NOME="ZZ TESTE 12X30" W11_TAG=teste-12x30 python build_w11.py
monta uma COPIA com gatilho de tag (a real usa etapa CONECTAR).
"""
import io
import json
import os
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = os.environ.get("W11_NOME", "Cadência 12x30")
TAG_TESTE = os.environ.get("W11_TAG")            # so na copia de teste
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
CONEXAO = C["Conexão real"]["id"]
TEMPLATE = C["Template usado"]["id"]
AGORA = "{{right_now.date}} {{right_now.time}}"
MSG_APOS_H = 2          # mensagem sai 2 h depois da tarefa do toque

# ---------------- textos (biblioteca-mensagens.md) ----------------
MSG = {
    "MT1-v1": ("Oi {{contact.first_name}}, aqui é o {{user.first_name}} da "
               "{{location.name}}. Acabei de tentar te ligar sobre o seu cadastro. "
               "Queria te fazer 2 perguntas rápidas sobre como vocês trazem cliente "
               "novo hoje. Qual o melhor horário pra eu te ligar: manhã ou tarde?"),
    "MT4-v1": ("{{contact.first_name}}, tentei te ligar de novo agora. Sei que a "
               "rotina é corrida — se preferir, me responde por aqui mesmo: hoje o "
               "cliente novo de vocês vem mais de indicação ou de anúncio?"),
    "MT8-v1": ("{{contact.first_name}}, tentei falar com você algumas vezes e não "
               "quero ser chato. Uma linha só: hoje vocês trazem cliente novo mais "
               "por indicação ou por anúncio? Me responde por aqui que eu te ligo "
               "no horário que for melhor pra você."),
    "MT11-v1": ("{{contact.first_name}}, última tentativa de te pegar por telefone. "
                "Se captar cliente novo não é prioridade agora, sem problema, me diz "
                "que eu respeito. Se for, 10 minutos de conversa já mostram se faz "
                "sentido a gente ajudar."),
    "MT12-v1": ("{{contact.first_name}}, vou parar de te procurar por aqui. Se um "
                "dia quiser falar sobre trazer mais clientes com anúncio, é só "
                "responder esta mensagem que eu retomo de onde paramos. Sucesso!"),
}

# n, espera ATE o proximo toque (h), codigo da mensagem (ou None), liga?
# D1, D1+4h, D2, D3, D5, D7, D10, D13, D17, D21, D25, D30
TOQUES_TAB = [
    (1, 4, "MT1-v1", True),
    (2, 20, None, True),
    (3, 24, None, True),
    (4, 48, "MT4-v1", True),
    (5, 48, None, True),
    (6, 72, None, True),
    (7, 72, None, True),
    (8, 96, "MT8-v1", True),
    (9, 96, None, True),
    (10, 96, None, True),
    (11, 120, "MT11-v1", True),
    (12, 24, "MT12-v1", False),     # so mensagem de encerramento, sem tarefa
]

SO_MONTAR = "--so-montar" in sys.argv       # valida a arvore sem tocar no CRM
if SO_MONTAR:
    c, WF = None, "00000000-0000-0000-0000-000000000000"
else:
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
           if w.get("type") == "workflow"}
    WF = ids.get(NOME) or g.create_workflow(c, NOME)
print("workflow: %s (%s)" % (NOME, WF))


def raiz_id(passos):
    p0 = passos[0]
    return p0.id if isinstance(p0, g.Branch) else p0["id"]


def campos_step(lista, nome_no="Update contact field"):
    return {"id": g.uid(), "name": nome_no, "type": "update_contact_field",
            "attributes": {"type": "update_contact_field",
                           "actionType": "update_field_data", "fields": lista}}


def f(campo, titulo, valor, tipo="numerical"):
    return {"field": campo, "value": valor, "title": titulo, "type": tipo, "date": ""}


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


def sms_step(codigo):
    """Mensagem de WhatsApp pela Stevo (canal SMS do GHL)."""
    return {"id": g.uid(), "name": "WhatsApp · " + codigo, "type": "sms",
            "attributes": {"type": "sms", "body": MSG[codigo], "attachments": []}}


def sair(motivo_tag=True):
    return {"id": g.uid(), "name": "Remove from Workflow", "type": "remove_from_workflow",
            "attributes": {"type": "remove_from_workflow", "workflow_id": [WF]}}


def sair_da_cadencia():
    return [g.tag_step(["fila-tel", "fila-wa", "fila-quente"], remove=True),
            g.tag_step(["limpar-tarefas"]), sair()]


PARE = ("Atendeu em qualquer passo? Pare o roteiro, converse, qualifique e tente "
        "agendar. Marque <b>Resultado da tentativa</b> e <b>Canal que conectou</b>.")


def tarefa(n, wa_primeiro, codigo):
    wa = "🟢 Ligar pelo WhatsApp (botão <b>Ligar via WhatsApp</b> na conversa)."
    tel = "📞 Ligar pelo telefone (botão de ligar do contato)."
    passos = [wa, tel] if wa_primeiro else [tel, wa]
    if not wa_primeiro:
        passos[1] += " <i>(o lead já ignorou 3 ligações de WhatsApp seguidas: WhatsApp só depois)</i>"
    if codigo:
        passos.append("💬 Marcando <b>Não atendeu</b> ou <b>Caixa Postal</b>, a mensagem "
                      "<b>%s</b> sai sozinha pelo WhatsApp em até %d h — não precisa "
                      "mandar." % (codigo, MSG_APOS_H))
    titulo = "[CADENCIA] T%d · %s" % (n, "WhatsApp → Ligar" if wa_primeiro else "Ligar → WhatsApp")
    corpo = ("Cadência 12x30 — toque %d de 12.%s<br><br>%s"
             % (n, "".join("<br>%d. %s" % (i, p) for i, p in enumerate(passos, 1)), PARE))
    return task_step(titulo, corpo)


def sem_conversa():
    """Condicoes (OU) de 'ainda nao conversou neste toque'."""
    return [g.cond("contact_detail", RESULT, "has_no_value", None),
            g.cond("contact_detail", RESULT, "==", "Não atendeu"),
            g.cond("contact_detail", RESULT, "==", "Caixa Postal")]


def tentou():
    """O SDR registrou que tentou e nao conversou (so entao a mensagem diz
    'tentei te ligar' com verdade)."""
    return [g.cond("contact_detail", RESULT, "==", "Não atendeu"),
            g.cond("contact_detail", RESULT, "==", "Caixa Postal")]


def avaliacao(n, proximo, liga=True):
    """Depois da espera: conta WhatsApp nao atendido, pausa no retorno,
    sai no Atendeu, marca 'Nao atendeu' se ficou vazio e segue."""
    seguir = list(proximo) if proximo else fim_da_cadencia()
    marcar = [campos_step([f(RESULT, "Resultado da tentativa", "Não atendeu", "select")]),
              g.tag_step(["limpar-tarefas"]), g.goto_step(raiz_id(seguir))]
    b_vazio = g.Branch("T%d · Sem resposta registrada?" % n,
                       [g.cond("contact_detail", RESULT, "has_no_value", None)],
                       sim=marcar, nao=seguir)
    b_atendeu = g.Branch("T%d · Atendeu?" % n,
                         [g.cond("contact_detail", RESULT, "==", "Atendeu")],
                         sim=[sair()], nao=[b_vazio])
    b_retorno = g.Branch("T%d · Pediu retorno? (pausa)" % n,
                         [g.cond("contact_detail", RESULT, "==", "Pediu retorno")],
                         sim=[], nao=[b_atendeu])
    b_retorno.sim = [g.wait_step(1, "hours"), g.goto_step(b_retorno.id)]
    if not liga:                       # T12: so mensagem, nada de WhatsApp a contar
        return [b_retorno]
    # D6: conta ligacao de WhatsApp nao atendida (so enquanto WhatsApp vem primeiro)
    conta = g.Branch("T%d · WhatsApp não atendido?" % n, sem_conversa(), operador="or",
                     sim=[g.math_step(WA_NAO, "+", 1), g.goto_step(b_retorno.id)],
                     nao=[b_retorno])
    return [g.Branch("T%d · WhatsApp ainda vem primeiro?" % n,
                     [g.cond("contact_detail", WA_NAO, ">=", "3")],
                     sim=[g.goto_step(b_retorno.id)], nao=[conta])]


def corpo_toque(n, espera_h, codigo, liga, proximo):
    passos = [campos_step([f(RESULT, "Resultado da tentativa", "", "select"),
                           f(TENT, "Tentativa nº", n, "numerical"),
                           f(CONEXAO, "Conexão real", "", "select")])]
    if n == 1:
        passos.append(campos_step([f(PRIMEIRA, "1ª tentativa em", AGORA, "text")]))
        passos.append(g.tag_step(["atraso-1a-tentativa"], remove=True))
    resto = []
    if codigo:
        envia = [sms_step(codigo),
                 campos_step([f(TEMPLATE, "Template usado", codigo, "text")])]
        antes, depois = (MSG_APOS_H, espera_h - MSG_APOS_H) if liga else (0, espera_h)
        pos = [g.wait_step(depois, "hours")] if depois > 0 else []
        pos += avaliacao(n, proximo, liga)
        b_msg = g.Branch("T%d · Tentou e não conversou? (mensagem)" % n,
                         tentou() if liga else sem_conversa(),
                         operador="or", sim=envia + [g.goto_step(raiz_id(pos))], nao=pos)
        resto = ([g.wait_step(antes, "hours")] if antes else []) + [b_msg]
    else:
        resto = [g.wait_step(espera_h, "hours")] + avaliacao(n, proximo, liga)
    fim = [g.tag_step(["fila-tel", "fila-wa"], remove=True)] + resto
    if not liga:
        return passos + fim
    # tarefa: WhatsApp primeiro, salvo 3 nao atendidas seguidas (D6)
    cont = [g.tag_step(["toque"])] + fim
    passos += [g.tag_step(["fila-tel"]),
               g.Branch("T%d · WhatsApp bloqueado para este lead?" % n,
                        [g.cond("contact_detail", WA_NAO, ">=", "3")],
                        sim=[tarefa(n, False, codigo), g.goto_step(raiz_id(cont))],
                        nao=[tarefa(n, True, codigo)] + cont)]
    return passos


def bloco_toque(n, espera_h, codigo, liga, proximo):
    corpo = corpo_toque(n, espera_h, codigo, liga, proximo)
    conds = [g.cond("opportunities", "pipelineStageId", "==", g.STAGES["CONECTAR"]),
             g.cond("opportunities", "status", "==", "open"),
             g.cond("contact_detail", "tags", "index-of-false", ["nao-perturbe"]),
             g.cond("contact_detail", RESULT, "!=", "Não ligar"),
             g.cond("contact_detail", "tags", "index-of-false", ["telefone-invalido"])]
    b3 = g.Branch("T%d · Ainda vale tentar?" % n, conds, sim=corpo, nao=sair_da_cadencia())
    # D14 capacidade do SDR (laco de 1 h)
    b_cap = g.Branch("T%d · SDR lotado?" % n,
                     [g.cond("contact_detail", "tags", "index-of-true", ["sdr-lotado"])],
                     sim=[], nao=[b3])
    b_cap.sim = [g.wait_step(1, "hours"), g.goto_step(b_cap.id)]
    b25c = g.Branch("T%d · Teto de toques da semana?" % n,
                    [g.cond("contact_detail", TOQUES, ">=", "6")], sim=[], nao=[b_cap])
    b25c.sim = [g.wait_step(1, "days"), g.goto_step(b25c.id)]
    b25 = g.Branch("T%d · Lead pausado?" % n,
                   [g.cond("contact_detail", "tags", "index-of-true", ["pausado"])],
                   sim=[], nao=[b25c])
    b25.sim = [g.wait_step(1, "days"), g.goto_step(b25.id)]
    return [b25]


def fim_da_cadencia():
    """12 toques sem conversa: nutricao (a regra da secao 1.2)."""
    return [g.Branch("Fim · Ainda em CONECTAR e aberta?",
                     [g.cond("opportunities", "pipelineStageId", "==", g.STAGES["CONECTAR"]),
                      g.cond("opportunities", "status", "==", "open")],
                     sim=[g.opp_step("abandoned", g.STAGES["CONECTAR"]),
                          g.tag_step(["nutricao-90d"]),
                          g.tag_step(["fila-tel", "fila-wa", "toque"], remove=True),
                          g.note_step("Cadência 12x30",
                                      "12 toques em 30 dias sem conversa — lead foi para nutrição (90 dias).")],
                     nao=[])]


proximo = []
for linha in reversed(TOQUES_TAB):
    proximo = bloco_toque(*linha, proximo=proximo)
cadencia = proximo

# ---------------- no 0: inicializacao (igual a versao anterior) ----------------
atribuir = {"id": g.uid(), "name": "Assign user", "type": "assign_user",
            "attributes": {"only_unassigned_contact": False, "total_index": 1,
                           "traffic_split": "equally",
                           "traffic_weightage": {g.USER: 1},
                           "traffic_index": [{"id": g.USER, "indexes": [1]}],
                           "user_list": [g.USER], "type": "assign_user"}}
b07 = g.Branch("Sem dono?", [g.cond("contact_detail", "assigned_to", "has_no_value", None)],
               sim=[atribuir, g.goto_step(raiz_id(cadencia))], nao=list(cadencia))
comum = [campos_step([f(PRIOR, "Prioridade", 3, "numerical"),
                      f(ENTRADA, "Entrada em", AGORA, "text")]), b07]
b04 = g.Branch("Permissão de WhatsApp em branco?",
               [g.cond("contact_detail", PERM_WA, "has_no_value", None)],
               sim=[campos_step([f(PERM_WA, "Permissão WhatsApp", "Não solicitado", "select")]),
                    g.goto_step(raiz_id(comum))],
               nao=comum)
inicio = [campos_step([f(TENT, "Tentativa nº", 0, "numerical"),
                       f(WA_NAO, "WA não atendidas seguidas", 0, "numerical"),
                       f(RESULT, "Resultado da tentativa", "", "select"),
                       f(CONEXAO, "Conexão real", "", "select")],
                      "Inicializa contadores"), b04]
b00c = g.Branch("Tem site ou Instagram?",
                [g.cond("contact_detail", SITE, "has_value", None),
                 g.cond("contact_detail", INSTA, "has_value", None)], operador="or",
                sim=[g.opp_step("abandoned", g.STAGES["CONECTAR"]), g.tag_step(["nutricao-90d"])],
                nao=[g.opp_step("lost", g.STAGES["CONECTAR"]),
                     g.notify_user_step("Lead sem telefone",
                                        "Lead sem telefone: {{contact.name}} — revisar a fonte "
                                        "da lista antes de qualquer tentativa.")])
sem_telefone = [g.Branch("Contato sem telefone?",
                         [g.cond("contact_detail", "phone", "has_no_value", None)],
                         sim=[g.tag_step(["telefone-invalido"]), b00c], nao=inicio)]
passos = [g.Branch("É lead de outra régua?",
                   [g.cond("contact_detail", "tags", "index-of-true", ["cad-inbound"]),
                    g.cond("contact_detail", "tags", "index-of-true", ["reengajamento-ativo"])],
                   operador="or", sim=[], nao=sem_telefone)]

if TAG_TESTE:
    gatilho = g.tag_trigger("Teste 12x30", TAG_TESTE)
    if not SO_MONTAR:
        c.create_location_tag(TAG_TESTE)
else:
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
if not SO_MONTAR:
    c.create_location_tag("sdr-lotado")

if SO_MONTAR:
    tpl = g.montar(passos)
else:
    g.preencher(c, WF, NOME, passos, [gatilho], allow_reentry=False, stop_on_response=True,
                janela=None if TAG_TESTE else   # copia de teste roda a qualquer hora
                {"days": [1, 2, 3, 4, 5], "startHour": 8, "startMinute": 30,
                 "endHour": 18, "endMinute": 30})
    doc = g.export(c, WF, os.path.join(JSON_DIR, NOME + ".json"))
    tpl = (doc["workflow"].get("workflowData") or {}).get("templates") or []

vivos = {s["id"] for s in tpl}
print("nós=%d" % len(tpl), dict(Counter(s["type"] for s in tpl)))
quebrados = [s["id"] for s in tpl if s["type"] == "goto"
             and (s.get("attributes") or {}).get("targetNodeId") not in vivos]
print("gotos quebrados: %d" % len(quebrados))
tarefas = [s["attributes"]["title"] for s in tpl if s["type"] == "task-notification"]
print("tarefas: %d (esperado 22 = 11 toques x 2 variantes)" % len(tarefas))
print("mensagens:", [s["name"] for s in tpl if s["type"] == "sms"])
print("'sim' no relógio:", sum(1 for s in tpl if s["type"] == "update_contact_field"
                               and any(x.get("value") == "sim" for x in s["attributes"]["fields"])))
