#!/usr/bin/env python3
"""Disposição do discador -> Registro da ligação (29/09, pedido do dono).

A SDR escolhe a disposição no discador ao desligar (1 clique). Um workflow por disposição
(gatilho "Call Details" com filtro "Custom Disposition") grava `Registro da ligação`, que o
workflow `Registro da ligação — 1 campo` converte em Canal + Resultado (Pós-ligação v3).

    python criar_disposicoes_registro.py            # cria os 7 rascunhos (sem gatilho)
"""
import sys
import ghl_interno as g
from criar_workflows_27 import Cadeia

REGISTRO = "2iqHW8jbd41AI6fZJr6P"
MAPA = [  # disposição (id no CRM) -> valor do Registro da ligação
    ("Não atendeu", "6ab5d7aba2286db93dbe0919", "Telefone · Não atendeu"),
    ("Caixa postal", "6ab5d7aba2286db93dbe091a", "Telefone · Caixa postal"),
    ("Pediu retorno", "6ab5d7aba2286db93dbe091b", "Telefone · Pediu retorno"),
    ("Atendeu", "6ab5d7aba2286db93dbe091c", "Telefone · Atendeu"),
    ("Não ligar", "6ab5d7aba2286db93dbe091d", "Não ligar"),
    ("Número errado", "6ab5d7aba2286db93dbe091e", "Telefone · Número errado"),
    ("Desqualificado", None, "Desqualificado"),
]


def nome(d):
    return "Disposição → Registro · " + d


def main():
    ex = {w["name"]: w["id"] for w in g.listar()}
    for d, _, valor in MAPA:
        if nome(d) in ex:
            print("já existe:", nome(d), ex[nome(d)]); continue
        c = Cadeia()
        c.add(None, "update_contact_field", "Registro da ligação = " + valor,
              {"type": "update_contact_field", "actionType": "update_field_data",
               "fields": [{"field": REGISTRO, "value": valor, "title": "Registro da ligação", "type": "select", "date": ""}]})
        wid = g.pedir("POST", "/workflow/%s" % g.LOC, {"name": nome(d)})["id"]
        cur = g.ler(wid); cur["allowMultiple"] = True
        g.put(cur, c.nos)
        d2 = g.ler(wid); print("criado", nome(d), wid, d2["status"], len(d2["workflowData"]["templates"]), "nó")


if __name__ == "__main__" and "--publicar" not in sys.argv:
    main()


def gatilho(disp):
    """Formato lido do editor (CallStatusFilter): valor = NOME da disposição, não o id."""
    return {"type": "call_status", "name": "Disposição = " + disp, "conditions": [
        {"operator": "contains-any", "field": "custom_disposition", "value": [disp],
         "title": "Custom disposition", "type": "multiselect", "id": "custom_disposition"}]}


def publicar():
    ex = {w["name"]: w["id"] for w in g.listar()}
    for d, _, valor in MAPA:
        wid = ex[nome(d)]
        cur = g.ler(wid); nos = cur["workflowData"]["templates"]
        if g.gatilhos(wid):
            print("já tem gatilho:", nome(d)); continue
        cur["status"] = "published"; cur["allowMultiple"] = True
        g.put(cur, nos)
        gat = gatilho(d)
        corpo = {"status": "published", "workflowId": wid, "schedule_config": {}, "conditions": gat["conditions"],
                 "type": gat["type"], "masterType": "highlevel", "name": gat["name"],
                 "actions": [{"workflow_id": wid, "type": "add_to_workflow"}], "active": True,
                 "triggersChanged": True, "location_id": g.LOC}
        tr = g.pedir("POST", "/workflow/%s/trigger" % g.LOC, corpo)
        g.pedir("PUT", "/workflow/%s/trigger/%s" % (g.LOC, tr["id"]),
                {**corpo, "targetActionId": nos[0]["id"], "advanceCanvasMeta": {"position": {"x": 57.5, "y": -73}}})
        d2 = g.ler(wid); ts = g.gatilhos(wid)
        print("publicado", nome(d), d2["status"], [(t["name"], t.get("active"), t["conditions"][0]["value"]) for t in ts])


if __name__ == "__main__" and "--publicar" in sys.argv:
    publicar()
