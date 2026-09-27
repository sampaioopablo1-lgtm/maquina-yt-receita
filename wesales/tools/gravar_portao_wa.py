#!/usr/bin/env python3
"""Portão do governador de WhatsApp antes de cada WhatsApp automático de prospecção.

Contrato com `wa_governador.py` (regra do dono, 27/09 21:00: no máximo ~15 WhatsApp
automáticos por dia, espalhados; o resto vira WhatsApp manual da SDR):

    ... -> [+ tag wa-aguardando] -> <tem wa-liberado?>
              sim -> [- wa-aguardando, - wa-liberado] -> WhatsApp -> (resto da cadência)
              não -> <tem wa-manual?>
                       sim -> [- wa-aguardando, - wa-manual] -> tarefa [WHATSAPP MANUAL] <código>
                              (texto exato no corpo, vence hoje) -> Go To (nó seguinte ao WhatsApp)
                       não -> Wait 15 min -> Go To <tem wa-liberado?>

Por que um laço e não o "Wait até condição com timeout": em 27/09 nenhum dos 70
workflows da conta usa esse tipo de espera (só tempo, agendamento e resposta), e gravar
um formato não observado num workflow publicado na véspera da abertura é aposta. O laço
usa só nós que a conta já roda (o Fechar Horário tem o mesmo desenho). O timeout de 4 h
fica com o governador: ele aplica `wa-manual` a quem espera há 4 h ou ao fim da janela.

Nada é apagado; o WhatsApp e tudo depois dele ficam iguais, só passam a ficar dentro do
ramo "liberado". Preserva `status`. Relê e confere o grafo.

    python gravar_portao_wa.py --wf inbound --seco
    python gravar_portao_wa.py --wf inbound
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
import uuid

import ghl_interno as g
from gravar_copy_whatsapp import WF, BKP

ESCOPO = ["inbound", "12x30", "12x30p2", "nutricao", "fechar", "noshow", "cancelada"]
AGUARDA, LIBERADO, MANUAL = "wa-aguardando", "wa-liberado", "wa-manual"
ESPERA_MIN = 15


def uid() -> str:
    return str(uuid.uuid4())


def codigo(nome: str) -> str:
    # "WhatsApp · MI-0" -> "MI-0"; "WhatsApp · MT1-v1" -> "MT1"; "NS-1 (remarcar)" -> "NS-1"
    c = (nome or "").split("·")[-1].strip()
    c = re.sub(r"\s*\(.*\)$", "", c)
    return re.sub(r"-v\d+$", "", c)


def cond_tag(tag: str) -> dict:
    return {
        "conditionType": "contact_detail", "conditionSubType": "tags",
        "conditionOperator": "index-of-true", "conditionValue": [tag],
        "__conditionId": uid(), "ifElseNodeId": "", "__customFieldType__": "standard",
        "isWait": False,
        "nestedDropdownTypes": ["inboundWebhookRequest", "sheet", "datetime_formatter",
                                "custom_webhook", "array_functions", "ivr_gather",
                                "ivr_connect_call", "custom_code", "ai_agent",
                                "task-notification", "event"],
        "allowIsOperatorTypes": ["contact_reply", "inboundWebhookRequest", "custom_webhook",
                                 "custom_code", "ai_agent", "contact_detail",
                                 "array_functions", "appointment", "service_booking",
                                 "rental_booking"],
    }


def se_tag(nome, tag, parent, pkey, order):
    """Nó if_else + os dois filhos (Branch / None). Devolve (if, sim, nao)."""
    i, s, n = uid(), uid(), uid()
    no_if = {
        "id": i, "order": order, "name": nome, "type": "if_else", "cat": "conditions",
        "parent": parent, "parentKey": pkey, "next": [s, n], "comments": [],
        "nodeType": "condition-node",
        "attributes": {"currentRecipeType": "CUSTOM", "branches": [{
            "id": s, "name": "Branch", "segments": [{
                "__segmentId": uid(), "operator": "and", "conditions": [cond_tag(tag)]}],
            "operator": "and", "showErrors": False, "branchNameError": False}],
            "operator": "and", "if": True, "conditionName": "Condition", "version": 2,
            "noneBranchName": "None"},
    }
    sim = {"id": s, "parent": i, "parentKey": i, "order": order + 1, "name": "Branch",
           "type": "if_else", "cat": "conditions", "sibling": [n], "comments": [],
           "nodeType": "branch-yes",
           "attributes": {"if": False, "conditionName": "Condition", "operator": "and",
                          "branches": []}}
    nao = {"id": n, "parent": i, "parentKey": i, "order": order + 1, "name": "None",
           "type": "if_else", "cat": "conditions", "sibling": [s], "comments": [],
           "nodeType": "branch-no", "attributes": {"else": True}}
    return no_if, sim, nao


def acao(tipo, nome, attrs, parent, pkey, order):
    return {"id": uid(), "name": nome, "type": tipo, "attributes": attrs, "order": order,
            "parent": parent, "parentKey": pkey, "cat": ""}


def inserir(t: list, sms: dict) -> list:
    """Insere o portão antes de `sms`, no lugar. Devolve os nós novos."""
    by = {n["id"]: n for n in t}
    pais = [n for n in t if n.get("next") == sms["id"]]
    if len(pais) > 1 or (not pais and sms.get("parent")):
        raise SystemExit("PAROU: %s tem %d antecessores lineares" % (sms["name"], len(pais)))
    pai = pais[0] if pais else {"id": None}   # WhatsApp como primeiro nó do workflow
    chave = sms.get("parentKey")
    base = int(sms.get("order") or 0)
    seguinte = sms.get("next") if isinstance(sms.get("next"), str) else None
    cod = codigo(sms["name"])

    # Regra validada pelo GHL ao publicar (27/09): o `parentKey` de um nó é o id do nó
    # cujo `next` aponta para ele. A cadeia depois do WhatsApp não muda.
    a = acao("add_contact_tag", "WA · aguardar governador", {"tags": [AGUARDA]},
             pai["id"], pai["id"], base)
    g1, g1s, g1n = se_tag("WA · %s liberado?" % cod, LIBERADO, a["id"], a["id"], base + 1)
    a["next"] = g1["id"]
    if pai["id"]:
        pai["next"] = a["id"]
    r1 = acao("remove_contact_tag", "WA · limpar marcas", {"tags": [AGUARDA, LIBERADO]},
              g1s["id"], g1s["id"], 0)
    g1s["next"] = r1["id"]
    r1["next"] = sms["id"]
    sms["parent"] = r1["id"]
    sms["parentKey"] = r1["id"]

    g2, g2s, g2n = se_tag("WA · %s virou manual?" % cod, MANUAL, g1n["id"], g1n["id"], 0)
    g1n["next"] = g2["id"]
    r2 = acao("remove_contact_tag", "WA · limpar marcas", {"tags": [AGUARDA, MANUAL]},
              g2s["id"], g2s["id"], 0)
    g2s["next"] = r2["id"]
    texto = (sms["attributes"].get("body") or "").replace("\n", "<br>")
    tarefa = acao("task-notification", "Add Task", {
        "title": "[WHATSAPP MANUAL] %s" % cod,
        "body": ('<p style="margin:0px; padding-left: 0px!important;">O limite diário de '
                 'WhatsApp automático foi atingido. Envie hoje, pela conversa do contato, '
                 'exatamente este texto:<br><br>%s</p>' % texto),
        "assignedTo": "contact.assigned_user", "type": "task_notification",
        "dueDate": {"duration": 0, "unit": "days", "time": 1789851600000,
                    "skipWeekends": True},
        "__customInputs__": {"dueDate": "duration-picker"}}, r2["id"], r2["id"], 1)
    r2["next"] = tarefa["id"]
    novos = [a, g1, g1s, g1n, r1, g2, g2s, g2n, r2, tarefa]
    if seguinte:
        j = acao("goto", "Go To", {"targetNodeId": seguinte, "type": "goto"},
                 tarefa["id"], tarefa["id"], 2)
        tarefa["next"] = j["id"]
        novos.append(j)
    w = acao("wait", "Wait %d Minutes" % ESPERA_MIN, {
        "type": "time", "startAfter": {"type": "minutes", "value": ESPERA_MIN, "when": "after"},
        "name": "Wait %d Minutes" % ESPERA_MIN, "cat": "", "isHybridAction": True,
        "hybridActionType": "wait", "convertToMultipath": False, "transitions": []},
        g2n["id"], g2n["id"], 0)
    g2n["next"] = w["id"]
    j2 = acao("goto", "Go To", {"targetNodeId": g1["id"], "type": "goto"},
              w["id"], w["id"], 1)
    w["next"] = j2["id"]
    novos += [w, j2]
    if not pai["id"]:
        a.pop("parent"); a.pop("parentKey")
    t.extend(novos)
    return novos


def grafo_ok(t: list) -> list:
    ids = {n["id"] for n in t}
    by_ = {n["id"]: n for n in t}
    erros = []
    for n in t:
        nx = n.get("next")
        for k in (nx if isinstance(nx, list) else [nx] if nx else []):
            if k not in ids:
                erros.append("%s -> next inexistente %s" % (n["id"][:8], k[:8]))
            elif by_[k].get("parentKey") != n["id"]:
                erros.append("%s -> %s com parentKey errado" % (n["id"][:8], k[:8]))
        if n["type"] == "goto" and n["attributes"].get("targetNodeId") not in ids:
            erros.append("goto %s -> alvo inexistente" % n["id"][:8])
    return erros


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wf", required=True, choices=ESCOPO)
    ap.add_argument("--seco", action="store_true")
    a = ap.parse_args()
    wid = WF[a.wf]
    if g.minutos_restantes() < 5:
        raise SystemExit("PAROU: bearer vence em menos de 5 min")
    cur = g.ler(wid)
    t = cur["workflowData"]["templates"]
    if cur.get("status") != "published":
        raise SystemExit("PAROU: não publicado")
    if any(AGUARDA in json.dumps(n.get("attributes", {})) for n in t):
        print("%s já tem portão — nada a fazer" % cur["name"])
        return 0
    os.makedirs(BKP, exist_ok=True)
    json.dump(cur, open(os.path.join(BKP, "%s-antes-portao-v%s.json" % (a.wf, cur["version"])),
                        "w", encoding="utf-8"), ensure_ascii=False)
    novo = copy.deepcopy(t)
    alvos = [n for n in novo if n["type"] == "sms"]
    for s in alvos:
        inserir(novo, s)
    erros = grafo_ok(novo)
    print("%s v%s: %d WhatsApp, %d -> %d nós" % (cur["name"], cur["version"], len(alvos),
                                                 len(t), len(novo)))
    for s in alvos:
        print("    portão antes de", s["name"])
    if erros:
        print("GRAFO INVÁLIDO:", erros)
        return 1
    if a.seco:
        return 0
    g.put(cur, novo)
    dep = g.ler(wid)
    td = dep["workflowData"]["templates"]
    esperado = {n["id"]: n for n in novo}
    dif = [n["id"][:8] for n in td if n != esperado.get(n["id"])]
    print("gravado: v%s -> v%s, %s, %d nós, grafo %s, difs %s"
          % (cur["version"], dep.get("version"), dep.get("status"), len(td),
             "ok" if not grafo_ok(td) else grafo_ok(td), dif or "nenhuma"))
    return 0 if (not dif and len(td) == len(novo) and dep.get("status") == "published"
                 and dep.get("version") != cur.get("version")) else 1


if __name__ == "__main__":
    sys.exit(main())
