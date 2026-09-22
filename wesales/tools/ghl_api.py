"""WeSales - helpers da API interna do GHL (backend.leadconnectorhq.com).

Formatos de no e de gatilho foram lidos de workflows REAIS desta subconta
(Mestre de saida, 21/09/2026), nao inventados. Todo workflow nasce RASCUNHO:
nenhuma funcao aqui publica.
"""
from __future__ import annotations

import json
import os
import sys
import time
import uuid

LOC = "1D53YTI9C7oIMBavcQxV"          # UNICA subconta permitida
PIPELINE = "0Fo2xbeayE4EP6yuSUtq"
STAGES = {
    "NOVO LEAD": "7ae9c950-9bcf-4e60-8bc5-cb7388c87b7d",
    "CONECTAR": "deb60542-a5cd-43ae-b875-b467b120a72c",
    "AGENDAR": "3d26fcd1-220d-49ed-8325-705dfe9055b1",
    "NEGOCIAR": "cbcf0229-5e19-4fdb-8c50-6c641b78b3bb",
    "FORMALIZAR": "b8485ec0-98e8-459f-b990-f40a5e3bd25b",
}
USER = "JdvhvOTEBTvUyRi0BXU8"

_HERE = os.path.dirname(os.path.abspath(__file__))
BEARER_FILE = os.path.join(_HERE, "..", ".local", "_ghl_bearer.txt")
CLI_PATH = os.path.abspath(os.path.join(_HERE, "..", "..", "gohighlevel-cli"))

# workflows PUBLICADOS: nunca editar (regra inviolavel do dono)
PUBLICADOS = {
    "e08a1580-975b-4c0f-934e-582fc6a0dbaa": "Porta de Entrada",
    "30da2c98-5f84-4af9-9ed2-71f628dc7c1e": "Mestre de saida",
    "cf6fa19d-6af8-4fcb-b0dd-6fcfcefde0cc": "Pos-ligacao",
    "94a837d0-d87a-438e-95f1-c620d55f1a7f": "Pos-agendamento",
    "ea0a49b7-f3a9-4d8a-8acd-802975d6db03": "Interceptacao de Sinal - Clique.",
    "7a1b4e6b-7e6e-4ed8-8ff4-cd98b88cdcff": "Interceptacao de Sinal - Resposta",
}


NODE_PATH_GLOBAL = r"C:\Users\sampa\AppData\Roaming\npm\node_modules"


def _minutos_restantes(tok: str) -> float:
    import base64
    try:
        p = tok.split(".")[1]
        p += "=" * (-len(p) % 4)
        exp = json.loads(base64.urlsafe_b64decode(p)).get("exp", 0)
        return (float(exp) - time.time()) / 60.0
    except Exception:
        return -1.0


def renovar_bearer() -> bool:
    """Roda o renew.js (headless, perfil ja logado) e recarrega o token."""
    import subprocess
    env = dict(os.environ, NODE_PATH=NODE_PATH_GLOBAL)
    r = subprocess.run(["node", os.path.join(_HERE, "renew.js")],
                       capture_output=True, text=True, timeout=420,
                       cwd=_HERE, env=env)
    ok = r.returncode == 0
    print("  [bearer] renovacao " + ("ok" if ok else "FALHOU: " + r.stdout[-300:]))
    return ok


def client(min_minutos: float = 8.0):
    """Cliente da API interna, renovando o bearer se estiver perto de vencer."""
    if CLI_PATH not in sys.path:
        sys.path.insert(0, CLI_PATH)
    tok = open(BEARER_FILE, encoding="utf-8").read().strip()
    if _minutos_restantes(tok) < min_minutos:
        print("  [bearer] faltam %.1f min - renovando" % _minutos_restantes(tok))
        if renovar_bearer():
            tok = open(BEARER_FILE, encoding="utf-8").read().strip()
    os.environ["GHL_BACKEND_BEARER"] = tok
    from cli_anything.gohighlevel.utils.ghl_internal_client import (
        TokenManager, InternalGHLClient)
    return InternalGHLClient(TokenManager(), LOC)


def uid() -> str:
    return str(uuid.uuid4())


def guard(wf_id: str) -> None:
    if wf_id in PUBLICADOS:
        raise SystemExit(
            "RECUSADO: " + wf_id + " e o workflow PUBLICADO '"
            + PUBLICADOS[wf_id] + "'. Regra do dono: nunca editar.")


# -- nos (formato lido de workflow real) ---------------------------------

def token(var: str) -> str:
    """Merge field no formato que a tela grava (span data-cv-variable)."""
    return ('<span data-cv-variable="' + var + '" data-cv-token="true">'
            + "{{" + var + "}}" + "</span>")


def note_step(title: str, html_body: str, color: str = "#FEF0C7") -> dict:
    return {
        "id": uid(), "name": "Note", "type": "add_notes",
        "attributes": {
            "html": '<p style="padding-left: 0px!important;">' + html_body + "</p>",
            "color": color, "type": "add_notes", "title": title,
        },
    }


def tag_step(tags: list, remove: bool = False) -> dict:
    return {
        "id": uid(),
        "name": "Remove Tag" if remove else "Add Tag",
        "type": "remove_contact_tag" if remove else "add_contact_tag",
        "attributes": {"tags": tags},
    }


def wait_step(value: int, unit: str = "days") -> dict:
    api_unit = {"minutes": "minutes", "hours": "hour", "hour": "hour",
                "days": "days"}.get(unit, unit)
    label = {"minutes": "Minutes", "hour": "Hour", "hours": "Hours",
             "days": "Days"}.get(unit, unit.title())
    disp = "Wait " + str(value) + " " + label
    return {
        "id": uid(), "name": disp, "type": "wait", "cat": "",
        "attributes": {
            "type": "time",
            "startAfter": {"type": api_unit, "value": value, "when": "after"},
            "name": disp, "cat": "", "isHybridAction": True,
            "hybridActionType": "wait", "convertToMultipath": False,
            "transitions": [],
        },
    }


def math_step(campo_id: str, operador: str, valor, tipo: str = "numerical") -> dict:
    """Operacao matematica sobre um campo (formato lido do Pos-ligacao)."""
    return {
        "id": uid(), "name": "Math operation", "type": "math_operation",
        "attributes": {
            "selectField": campo_id, "selectFieldtype": tipo,
            "sourceCustomValueId": "",
            "updateField": campo_id, "updateFieldType": tipo,
            "targetCustomValueId": "",
            "operators": [{"operator": operador, "__id": uid(), "value": valor}],
        },
    }


def field_step(campo_id: str, titulo: str, valor, tipo: str = "numerical",
               data: str = "") -> dict:
    """Update Contact Field (formato lido da Interceptacao de Sinal)."""
    return {
        "id": uid(), "name": "Update contact field",
        "type": "update_contact_field",
        "attributes": {
            "type": "update_contact_field", "actionType": "update_field_data",
            "fields": [{"field": campo_id, "value": valor, "title": titulo,
                        "type": tipo, "date": data}],
        },
    }


def notify_user_step(titulo: str, corpo: str, usuario: str = USER) -> dict:
    """Notificacao interna para UM usuario (o gestor), nao para o dono do
    contato - o dono pode estar vazio justamente nos casos que os monitores
    de saude pegam. Formato lido do template 'Alerta de SLA Atrasado'."""
    return {
        "id": uid(), "name": "Internal Notification",
        "type": "internal_notification",
        "attributes": {
            "type": "notification",
            "notification": {
                "type": "send_notification", "body": corpo, "title": titulo,
                "redirectPage": "contact", "selectedUser": usuario,
                "userType": "user",
            },
        },
    }


def notify_step(html_body: str, canal: str = "whatsapp",
                para: str = "contact_owner") -> dict:
    """Internal Notification (formato lido da Interceptacao de Sinal)."""
    return {
        "id": uid(), "name": "Internal Notification",
        "type": "internal_notification",
        "attributes": {
            "type": canal,
            canal: {
                "body": '<p style="padding-left: 0px!important;">' + html_body,
                "userType": "assign", "assignedOwners": [para],
            },
        },
    }


def link(steps: list) -> list:
    """Encadeia nos lineares com order/parentKey/next."""
    out = []
    for i, s in enumerate(steps):
        s = dict(s)
        s["order"] = i
        s["parentKey"] = steps[i - 1]["id"] if i > 0 else None
        if i < len(steps) - 1:
            s["next"] = steps[i + 1]["id"]
        out.append(s)
    return out


# -- condicoes e ramificacao (formato lido do Mestre de saida) ------------

_NESTED = ["inboundWebhookRequest", "sheet", "datetime_formatter",
           "custom_webhook", "array_functions", "ivr_gather",
           "ivr_connect_call", "custom_code", "ai_agent",
           "task-notification", "event"]
_ALLOWIS = ["contact_reply", "inboundWebhookRequest", "custom_webhook",
            "custom_code", "ai_agent", "contact_detail", "array_functions",
            "appointment", "service_booking", "rental_booking"]


def cond(tipo: str, subtipo: str, operador: str, valor,
         cf_tipo: str = "standard") -> dict:
    """Uma condicao de If/Else.

    tipo/subtipo usados neste projeto:
      ('opportunities','pipelineStageId')  ('opportunities','status')
      ('contact','tags')                   ('custom_field', <id do campo>)
    """
    return {
        "conditionType": tipo, "conditionSubType": subtipo,
        "conditionOperator": operador, "conditionValue": valor,
        "__conditionId": uid(), "ifElseNodeId": "",
        "__customFieldType__": cf_tipo, "isWait": False,
        "nestedDropdownTypes": list(_NESTED),
        "allowIsOperatorTypes": list(_ALLOWIS),
    }


def opp_step(status: str = None, etapa_id: str = None,
             nome_no: str = "Update Opportunity") -> dict:
    """Atualiza a oportunidade (status e/ou etapa).

    Nenhum workflow desta subconta usava este no; o tipo veio do schema do
    ghl-automation-builder (`internal_update_opportunity`) e foi conferido
    na tela depois de criado.
    """
    # 'Update opportunity' e acao de marketplace (workflowsActionType
    # INTERNAL, key internal_update_opportunity), lida do catalogo que o
    # proprio builder baixa. Os valores nao vao soltos nos atributos: vao em
    # __customInputFields__, o mesmo padrao do find_opportunity real da conta.
    campos = []
    if status:
        campos.append({"filterField": "status", "value": status,
                       "valueFieldType": "select"})
    if etapa_id:
        campos.append({"filterField": "pipelineStageId", "value": etapa_id,
                       "valueFieldType": "select"})
    at = {"type": "internal_update_opportunity", "allowBackward": False,
          "__customInputs__": {}, "__customInputFields__": campos}
    return {"id": uid(), "name": nome_no,
            "type": "internal_update_opportunity", "attributes": at}


def goto_step(alvo: str) -> dict:
    """Salta para outro no. E o que permite dois ramos convergirem no mesmo
    no e o que fecha os lacos (W17c, W17e). Formato lido de template real."""
    return {"id": uid(), "name": "Go To", "type": "goto",
            "attributes": {"targetNodeId": alvo, "type": "goto"}}


class Branch:
    """Marcador de If/Else dentro de uma lista de passos.

    Em GHL um If/Else encerra a linha: tudo que vem depois mora dentro de
    um dos ramos. Por isso um Branch so pode ser o ULTIMO item de uma lista.

    `id` pode ser fixado de fora quando outro ramo precisa saltar para esta
    condicao (convergencia ou laco) - o alvo do goto e o id do no de condicao.
    """

    def __init__(self, nome: str, condicoes: list, sim: list, nao: list,
                 operador: str = "and", id: str = None):
        self.nome = nome
        self.condicoes = condicoes
        self.sim = sim
        self.nao = nao
        self.operador = operador
        self.id = id or str(uuid.uuid4())


def montar(passos: list, parent=None, parent_key=None) -> list:
    """Transforma uma lista de nos (com Branch opcional no fim) na lista
    plana de templates que a API espera, com parent/parentKey/next/order."""
    out = []
    prev = parent_key

    def encadeia():
        """Liga os nos simples ja acumulados em sequencia."""
        for j in range(len(out) - 1):
            out[j]["next"] = out[j + 1]["id"]

    for i, p in enumerate(passos):
        if isinstance(p, Branch):
            if i != len(passos) - 1:
                raise SystemExit("Branch tem de ser o ultimo item da lista")
            cid, yid, nid = p.id, uid(), uid()
            filhos_sim = montar(p.sim, yid, yid) if p.sim else []
            filhos_nao = montar(p.nao, nid, nid) if p.nao else []
            no_cond = {
                "id": cid, "order": i, "name": p.nome, "type": "if_else",
                "cat": "conditions", "next": [yid, nid], "comments": [],
                "nodeType": "condition-node",
                # o validador exige operator/if/conditionName no no de
                # condicao quando 'else' nao e true (erro 400, 21/09/2026)
                "attributes": {
                    "currentRecipeType": "CUSTOM",
                    "branches": [{
                        "id": yid, "name": "Branch",
                        "segments": [{"__segmentId": uid(),
                                      "operator": p.operador,
                                      "conditions": p.condicoes}],
                        "operator": p.operador,
                        "showErrors": False, "branchNameError": False,
                    }],
                    "operator": p.operador, "if": True,
                    "conditionName": "Condition", "version": 2,
                    "noneBranchName": "None",
                },
            }
            if parent:
                no_cond["parent"] = parent
            if prev:
                no_cond["parentKey"] = prev
            no_sim = {"id": yid, "parent": cid, "parentKey": cid, "order": i + 1,
                      "name": "Branch", "type": "if_else", "cat": "conditions",
                      "sibling": [nid], "comments": [], "nodeType": "branch-yes",
                      "attributes": {"if": False, "conditionName": "Condition",
                                     "operator": p.operador, "branches": []}}
            no_nao = {"id": nid, "parent": cid, "parentKey": cid, "order": i + 1,
                      "name": "None", "type": "if_else", "cat": "conditions",
                      "sibling": [yid], "comments": [], "nodeType": "branch-no",
                      "attributes": {"else": True}}
            if filhos_sim:
                no_sim["next"] = filhos_sim[0]["id"]
            if filhos_nao:
                no_nao["next"] = filhos_nao[0]["id"]
            # liga os simples que vieram antes e aponta o ultimo para a condicao
            out.append(no_cond)
            encadeia()
            out.pop()
            if len(out):
                out[-1]["next"] = cid
            return out + [no_cond, no_sim, no_nao] + filhos_sim + filhos_nao
        s = dict(p)
        s["order"] = i
        if parent:
            s["parent"] = parent
        s["parentKey"] = prev
        # o proximo e resolvido depois de saber quem vem a seguir
        out.append(s)
        prev = s["id"]
    encadeia()
    return out


def tag_trigger(name: str, tag: str) -> dict:
    return {
        "status": "draft", "schedule_config": {},
        "conditions": [{"operator": "index-of-true", "field": "tagsAdded",
                        "value": tag, "title": "Tag Added", "type": "select",
                        "id": "tag-added"}],
        "type": "contact_tag", "masterType": "highlevel", "name": name,
        "active": True, "triggersChanged": True, "location_id": LOC,
    }


# -- montagem ------------------------------------------------------------

def create_workflow(c, name: str) -> str:
    r = c.request("POST", "/workflow/" + LOC, {"name": name})
    if not r or r.get("_error") or not r.get("id"):
        raise SystemExit("falha ao criar workflow '" + name + "': " + str(r))
    return r["id"]


def build(c, name: str, steps: list, triggers: list,
          tags_to_create=None, allow_reentry: bool = True,
          stop_on_response: bool = False) -> str:
    """Cria workflow RASCUNHO com nos e gatilhos. Devolve o id."""
    wf = create_workflow(c, name)
    return preencher(c, wf, name, steps, triggers, tags_to_create,
                     allow_reentry, stop_on_response)


def preencher(c, wf: str, name: str, steps: list, triggers: list,
              tags_to_create=None, allow_reentry: bool = True,
              stop_on_response: bool = False) -> str:
    """Preenche um workflow EXISTENTE (rascunho vazio) com nos e gatilhos.

    Recusa se o id for de um workflow publicado (regra do dono).
    """
    guard(wf)
    steps = montar(steps)

    for t in (tags_to_create or []):
        c.create_location_tag(t)

    # Gatilhos ja existentes sao REAPROVEITADOS (PUT), nunca duplicados: uma
    # tentativa que falha depois de criar o gatilho deixaria um orfao
    # apontando para um no que nao existe mais (aconteceu em 21/09/2026).
    ja = c.request("GET", "/workflow/" + LOC + "/trigger?workflowId=" + wf)
    ja = [t for t in ja if not t.get("deleted")] if isinstance(ja, list) else []
    if len(ja) > len(triggers):
        print("  ! %d gatilhos na tela para %d esperados - conferir orfaos"
              % (len(ja), len(triggers)))

    saved = []
    for i, tdef in enumerate(triggers):
        body = dict(tdef)
        body["workflowId"] = wf
        body["location_id"] = LOC
        body["actions"] = [{"workflow_id": wf, "type": "add_to_workflow"}]
        if i < len(ja):
            tid = ja[i]["id"]
        else:
            tr = c.request("POST", "/workflow/" + LOC + "/trigger", body)
            if not tr or tr.get("_error") or not tr.get("id"):
                print("  ! gatilho '" + str(tdef.get("name")) + "' falhou: "
                      + str(tr))
                continue
            tid = tr["id"]
        c.request("PUT", "/workflow/" + LOC + "/trigger/" + tid,
                  dict(body, targetActionId=steps[0]["id"],
                       advanceCanvasMeta={"position": {"x": 57.5, "y": -73}}))
        saved.append(dict(body, id=tid))

    # a versao TEM de ser a corrente: um workflow que ja existe (tentativa
    # anterior, rascunho vazio) tem versao > 1 e o PUT com 1 e recusado
    # ('Your version is outdated').
    antes = c.request("GET", "/workflow/" + LOC + "/" + wf)
    ver_atual = antes.get("version", 1) if isinstance(antes, dict) else 1
    put = c.request("PUT", "/workflow/" + LOC + "/" + wf,
                    {"name": name, "status": "draft", "version": ver_atual,
                     "workflowData": {"templates": steps}})
    if not put or put.get("_error"):
        raise SystemExit("falha ao salvar nos de '" + name + "': " + str(put))

    cur = c.request("GET", "/workflow/" + LOC + "/" + wf)
    now = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    tl = []
    for t in saved:
        t = dict(t, workflow_id=wf, location_id=LOC, belongs_to="workflow",
                 deleted=False, date_added=now, date_updated=now,
                 advanceCanvasMeta={"position": {"x": 57.5, "y": -73}})
        for k in ("company_id", "company_age", "triggersChanged",
                  "workflowId", "status"):
            t.pop(k, None)
        tl.append(t)
    meta = (cur.get("meta") or {}) if isinstance(cur, dict) else {}
    meta["advanceCanvasMeta"] = {"enabled": True, "enabledAt": now}
    swm = []
    for i, s in enumerate(steps):
        s = dict(s, advanceCanvasMeta={"position": {"x": 400 + i * 300, "y": 0}})
        s.setdefault("cat", "")
        swm.append(s)
    ver = cur.get("version", 2) if isinstance(cur, dict) else 2
    # status='draft' e OBRIGATORIO: sem ele o workflow existe na API mas nao
    # aparece na lista da tela (a lista filtra por status). Descoberto no
    # PASSO 1, 21/09/2026. 'draft' nunca publica.
    c.request("PUT", "/workflow/" + LOC + "/" + wf,
              {"name": name, "status": "draft", "version": ver, "meta": meta,
               "allowMultiple": allow_reentry,
               "stopOnResponse": stop_on_response,
               "workflowData": {"templates": swm},
               "triggersChanged": bool(tl), "oldTriggers": tl,
               "newTriggers": tl})
    return wf


def publicar(c, wf_id: str) -> bool:
    """Tira do rascunho. So com autorizacao explicita do dono (21/09/2026:
    ele escolheu 'eu publico tudo sozinho ao terminar cada um').
    Recusa workflow publicado de antes - esses nao se tocam."""
    guard(wf_id)
    cur = c.request("GET", "/workflow/" + LOC + "/" + wf_id)
    if not isinstance(cur, dict) or cur.get("_error"):
        print("  nao consegui ler o workflow: " + str(cur))
        return False
    r = c.request("PUT", "/workflow/" + LOC + "/" + wf_id,
                  {"name": cur.get("name"), "status": "published",
                   "version": cur.get("version", 1),
                   "workflowData": {"templates":
                                    (cur.get("workflowData") or {}).get("templates") or []}})
    if r and r.get("_error"):
        print("  falha ao publicar: " + str(r.get("message"))[:160])
        return False
    volta = c.request("GET", "/workflow/" + LOC + "/" + wf_id)
    st = volta.get("status") if isinstance(volta, dict) else None
    print("  status agora: " + str(st))
    return st == "published"


def export(c, wf_id: str, path: str) -> dict:
    """Le workflow + gatilhos de volta e grava o JSON completo."""
    wf = c.request("GET", "/workflow/" + LOC + "/" + wf_id)
    tr = c.request("GET", "/workflow/" + LOC + "/trigger?workflowId=" + wf_id)
    doc = {"workflow": wf, "triggers": tr}
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    return doc
