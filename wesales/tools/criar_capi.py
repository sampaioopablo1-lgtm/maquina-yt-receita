#!/usr/bin/env python3
"""Eventos de servidor (Conversions API) para o Pixel "O PRÓXIMO CLIENTE" (1600846091439175).

Pedido do dono (27/09): registrar no Meta os marcos do funil para acelerar o aprendizado e
trazer lead mais qualificado. Em setembro o Pixel recebeu só 3 eventos (1 CONTATO, 2
SubmitApplication) e o servidor não envia nada desde 14/09.

Três workflows independentes (não tocam os fluxos da operação), com a ação nativa
`facebook_conversion_api` no formato do modelo da conta ("Template | Conversão API Meta"),
usando a integração do Facebook já conectada (`connection_type: INTEGRATION`, sem token):
  - Contato  : Resultado da tentativa = Atendeu      -> Contact
  - Reunião  : reunião confirmada (2 calendários)    -> Schedule
  - Venda    : oportunidade ganha no FUNIL DE VENDAS -> Purchase
`Lead` fica de fora: o formulário instantâneo do Meta já registra o lead; repetir duplicaria.
"""
import copy
import json
import sys

import ghl_interno as g
from criar_workflows_27 import Cadeia, criar, RESULTADO, PIPE

PX = "1600846091439175"


def capi(evento):
    return {"type": "facebook_conversion_api", "event_type": "funnel_event", "event_name": evento,
            "pixel_id": PX, "currency": "BRL", "connection_type": "INTEGRATION",
            # o token fica num valor personalizado que o dono preenche; nunca passa pelo código
            "access_token": "{{custom_values.meta_capi_token}}"}


def contato():
    c = Cadeia()
    s, _ = c.se(None, "Atendeu?", [("contact_detail", RESULTADO, "==", "Atendeu")])
    c.add(s, "facebook_conversion_api", "Meta CAPI · Contact", capi("Contact"))
    return c.nos, [{"type": "contact_changed", "name": "Resultado da tentativa mudou", "conditions": [
        {"operator": "has-changed", "field": "contact." + RESULTADO, "title": "Resultado da tentativa",
         "type": "select", "id": RESULTADO}]}]


def reuniao():
    c = Cadeia()
    c.add(None, "facebook_conversion_api", "Meta CAPI · Schedule", capi("Schedule"))
    base = [t for t in g.gatilhos("81815fcc-ff4f-4b72-8a1f-7dbf44ce6911") if t["type"] == "appointment"]
    return c.nos, [{"type": "appointment", "name": t["name"], "conditions": copy.deepcopy(t["conditions"])}
                   for t in base]


def venda():
    c = Cadeia()
    c.add(None, "facebook_conversion_api", "Meta CAPI · Purchase", capi("Purchase"))
    return c.nos, [{"type": "opportunity_status_changed", "name": "Oportunidade ganha", "conditions": [
        {"operator": "==", "field": "opportunity.pipelineId", "value": PIPE, "title": "No pipeline", "type": "select"},
        {"operator": "==", "field": "opportunity.status", "value": "won", "title": "Movido para o status",
         "type": "select", "id": "moved-to-status"}]}]


def criar_varios(nome, nos, gats, seco):  # cur_window_none: CAPI sem janela (evento sai na hora)
    """criar() aceita um gatilho; aqui o primeiro vai por ele e os demais são acrescentados."""
    criar(nome, nos, gats[0], seco)
    if seco or len(gats) == 1:
        return
    wid = [w for w in g.listar() if w.get("name") == nome][0]["id"]
    for gat in gats[1:]:
        corpo = {"status": "published", "workflowId": wid, "schedule_config": {}, "conditions": gat["conditions"],
                 "type": gat["type"], "masterType": "highlevel", "name": gat["name"] + " (2)",
                 "actions": [{"workflow_id": wid, "type": "add_to_workflow"}], "active": True,
                 "triggersChanged": True, "location_id": g.LOC}
        tr = g.pedir("POST", "/workflow/%s/trigger" % g.LOC, corpo)
        g.pedir("PUT", "/workflow/%s/trigger/%s" % (g.LOC, tr["id"]),
                {**corpo, "targetActionId": nos[0]["id"], "advanceCanvasMeta": {"position": {"x": 57.5, "y": -73}}})
    print("  gatilhos:", [(t["name"], t.get("active")) for t in g.gatilhos(wid)])


if __name__ == "__main__":
    seco = "--seco" in sys.argv
    criar_varios("Meta CAPI — Contato (atendeu)", *contato(), seco)
    criar_varios("Meta CAPI — Reunião marcada", *reuniao(), seco)
    criar_varios("Meta CAPI — Venda ganha", *venda(), seco)
