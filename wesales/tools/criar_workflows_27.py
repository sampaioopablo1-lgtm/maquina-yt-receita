#!/usr/bin/env python3
"""Cria dois workflows novos (decisões do dono em 27/09), só com peças que a conta já roda.

1. "Retorno — prazo de 3 dias": Resultado da tentativa = "Pediu retorno" e, 3 dias depois,
   ainda "Pediu retorno" e em CONECTAR -> oportunidade Abandonada + `nutricao-90d` (a Nutrição
   só envia com `status-nutricao`, que o Espelho de Etapa aplica em Abandonado; "Perdido"
   pararia a nutrição) + nota. Mesmo desfecho do "Fim" do Fechar Horário.
2. "Formalização Parada": oportunidade entra em FORMALIZAR e, 7 dias depois, ainda aberta
   lá -> aviso ao closer + tarefa "[CLOSER] Marcar a oportunidade como ganha ou perdida".
   Cópia do mecanismo do "Negociação Estagnada".

Cria em rascunho, publica (o GHL valida o grafo ao publicar), cria o gatilho apontando para
o primeiro nó e relê. Não mexe em nenhum workflow existente.
"""
from __future__ import annotations

import copy
import json
import sys
import uuid

import ghl_interno as g
from gravar_portao_wa import grafo_ok

LOC = g.LOC
PIPE, CONECTAR, FORMALIZAR = ("0Fo2xbeayE4EP6yuSUtq", "deb60542-a5cd-43ae-b875-b467b120a72c",
                              "b8485ec0-98e8-459f-b990-f40a5e3bd25b")
RESULTADO = "nPafc9c0JdSSptdPhUlF"
CLOSER = "JdvhvOTEBTvUyRi0BXU8"
BASE = json.load(open("../.local/bkp-copy-27-09/negociacao-estagnada.json", encoding="utf-8"))
MODELO_COND = next(c for n in BASE["wf"]["workflowData"]["templates"] if n["type"] == "if_else"
                   for b in n["attributes"].get("branches", []) for s in b["segments"]
                   for c in s["conditions"])


def uid():
    return str(uuid.uuid4())


class Cadeia:
    """Monta nós em sequência respeitando a regra do GHL: parentKey = id do nó anterior."""

    def __init__(self):
        self.nos = []

    def add(self, pai, tipo, nome, attrs, **extra):
        n = {"id": uid(), "name": nome, "type": tipo, "attributes": attrs, "order": 0, "cat": "", **extra}
        if pai:
            n["parent"] = n["parentKey"] = pai["id"]
            pai["next"] = n["id"]
        self.nos.append(n)
        return n

    def se(self, pai, nome, conds):
        i, s, nn = uid(), uid(), uid()
        seg = []
        for tipo, sub, op, val in conds:
            c = copy.deepcopy(MODELO_COND)
            c.update({"conditionType": tipo, "conditionSubType": sub, "conditionOperator": op,
                      "conditionValue": val, "__conditionId": uid()})
            seg.append(c)
        no = {"id": i, "order": 0, "name": nome, "type": "if_else", "cat": "conditions", "next": [s, nn],
              "comments": [], "nodeType": "condition-node",
              "attributes": {"currentRecipeType": "CUSTOM", "branches": [{"id": s, "name": "Branch", "segments": [
                  {"__segmentId": uid(), "operator": "and", "conditions": seg}], "operator": "and",
                  "showErrors": False, "branchNameError": False}], "operator": "and", "if": True,
                  "conditionName": "Condition", "version": 2, "noneBranchName": "None"}}
        if pai:
            no["parent"] = no["parentKey"] = pai["id"]
            pai["next"] = i
        sim = {"id": s, "parent": i, "parentKey": i, "order": 1, "name": "Branch", "type": "if_else",
               "cat": "conditions", "sibling": [nn], "comments": [], "nodeType": "branch-yes",
               "attributes": {"if": False, "conditionName": "Condition", "operator": "and", "branches": []}}
        nao = {"id": nn, "parent": i, "parentKey": i, "order": 1, "name": "None", "type": "if_else",
               "cat": "conditions", "sibling": [s], "comments": [], "nodeType": "branch-no",
               "attributes": {"else": True}}
        self.nos += [no, sim, nao]
        return sim, nao


def espera(dias):
    return {"type": "time", "startAfter": {"type": "days", "value": dias, "when": "after"},
            "name": "Wait %d Days" % dias, "cat": "", "isHybridAction": True, "hybridActionType": "wait",
            "convertToMultipath": False, "transitions": []}


def retorno():
    c = Cadeia()
    s1, _ = c.se(None, "Pediu retorno?", [("contact_detail", RESULTADO, "==", "Pediu retorno")])
    w = c.add(s1, "wait", "Wait 3 Days", espera(3))
    s2, _ = c.se(w, "Ainda Pediu retorno e em CONECTAR?", [
        ("contact_detail", RESULTADO, "==", "Pediu retorno"),
        ("contact_detail", "tags", "index-of-true", ["etapa-conectar"])])
    o = c.add(s2, "create_opportunity", "Oportunidade → Abandonada (nutrição)", {
        "fields": [], "type": "create_opportunity", "pipeline_id": PIPE, "pipeline_stage_id": CONECTAR,
        "opportunity_name": "{{contact.name}}", "opportunity_status": "abandoned",
        "opportunity_source": "", "monetary_value": ""})
    t = c.add(o, "add_contact_tag", "Entra na nutrição", {"tags": ["nutricao-90d"]})
    r = c.add(t, "remove_contact_tag", "Sai das filas", {"tags": ["fechar-horario", "fila-tel", "fila-quente"]})
    c.add(r, "add_notes", "Note", {"html": '<p style="padding-left: 0px!important;">Pediu retorno e passou '
          'do prazo de 3 dias sem nova conversa — oportunidade abandonada e lead em nutrição (regra do '
          'dono, 27/09).</p>', "color": "#FEF0C7", "type": "add_notes", "title": "Retorno vencido — 3 dias"})
    gatilho = {"type": "contact_changed", "conditions": [{"operator": "has-changed",
               "field": "contact." + RESULTADO, "title": "Resultado da tentativa", "type": "select",
               "id": RESULTADO}], "name": "Resultado da tentativa mudou"}
    return c.nos, gatilho


def formalizacao():
    c = Cadeia()
    r = c.add(None, "remove_contact_tag", "Remove Tag", {"tags": ["formalizacao-parada"]})
    w = c.add(r, "wait", "Wait 7 Days", espera(7))
    s, _ = c.se(w, "Ainda em FORMALIZAR e aberta?", [
        ("opportunities", "pipelineStageId", "==", FORMALIZAR), ("opportunities", "status", "==", "open")])
    t = c.add(s, "add_contact_tag", "Add Tag", {"tags": ["formalizacao-parada"]})
    a = c.add(t, "internal_notification", "Internal Notification", {"type": "notification", "notification": {
        "type": "send_notification", "body": "{{contact.name}} está em FORMALIZAR há 7 dias sem ganho nem "
        "perda. Marcar a oportunidade como ganha ou perdida.", "title": "Formalização parada",
        "redirectPage": "contact", "selectedUser": CLOSER, "userType": "user"}})
    k = c.add(a, "task-notification", "Add Task", {
        "title": "[CLOSER] Marcar a oportunidade como ganha ou perdida",
        "body": '<p style="margin:0px; padding-left: 0px!important;">A oportunidade está em FORMALIZAR há 7 '
                'dias. Registre o desfecho: <b>Ganha</b> (contrato assinado) ou <b>Perdida</b> (com o motivo).</p>',
        "assignedTo": "contact.assigned_user", "type": "task_notification",
        "dueDate": {"duration": 1, "unit": "days", "time": 1789851600000, "skipWeekends": True},
        "__customInputs__": {"dueDate": "duration-picker"}})
    c.add(k, "add_notes", "Note", {"html": '<p style="padding-left: 0px!important;">FORMALIZAR há 7 dias sem '
          'ganho nem perda.</p>', "color": "#FEF0C7", "type": "add_notes", "title": "Alerta de saúde"})
    gatilho = {"type": "pipeline_stage_updated", "conditions": [
        {"operator": "==", "field": "opportunity.pipelineId", "value": PIPE, "title": "No pipeline", "type": "select"},
        {"operator": "==", "field": "opportunity.pipelineStageId", "value": FORMALIZAR,
         "title": "Movido para o estágio", "type": "select", "id": "moved-to-stage"}], "name": "Entrou em FORMALIZAR"}
    return c.nos, gatilho


def criar(nome, nos, gat, seco):
    erros = grafo_ok(nos)
    print("%s: %d nós, grafo %s" % (nome, len(nos), erros or "ok"))
    if seco or erros:
        return
    if any(w.get("name") == nome for w in g.listar()):
        print("  já existe — nada a fazer")
        return
    wid = g.pedir("POST", "/workflow/%s" % LOC, {"name": nome})["id"]
    base = BASE["wf"]
    cur = g.ler(wid)
    for k in ("allowMultiple", "stopOnResponse", "timezone", "window", "allowMultipleOpportunity"):
        cur[k] = base.get(k)
    cur["status"] = "published"
    g.put(cur, nos)
    corpo = {"status": "published", "workflowId": wid, "schedule_config": {}, "conditions": gat["conditions"],
             "type": gat["type"], "masterType": "highlevel", "name": gat["name"],
             "actions": [{"workflow_id": wid, "type": "add_to_workflow"}], "active": True,
             "triggersChanged": True, "location_id": LOC}
    tr = g.pedir("POST", "/workflow/%s/trigger" % LOC, corpo)
    g.pedir("PUT", "/workflow/%s/trigger/%s" % (LOC, tr["id"]),
            {**corpo, "targetActionId": nos[0]["id"], "advanceCanvasMeta": {"position": {"x": 57.5, "y": -73}}})
    d = g.ler(wid)
    ts = g.gatilhos(wid)
    E = {n["id"]: n for n in nos}
    print("  criado %s: %s v%s, %d nós, difs %s | gatilho: %s" % (
        wid, d["status"], d["version"], len(d["workflowData"]["templates"]),
        [n["id"][:8] for n in d["workflowData"]["templates"] if n != E.get(n["id"])] or "nenhuma",
        [(t["name"], t.get("active"), t.get("targetActionId") == nos[0]["id"]) for t in ts]))


if __name__ == "__main__":
    seco = "--seco" in sys.argv
    criar("Retorno — prazo de 3 dias", *retorno(), seco)
    criar("Formalização Parada", *formalizacao(), seco)
