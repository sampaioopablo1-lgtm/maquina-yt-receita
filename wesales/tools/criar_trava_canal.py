#!/usr/bin/env python3
"""Trava de canal — "falou hoje" (pedido do dono, 28/09).

Problema: a lista "Ligar pelo WhatsApp" só tirava o lead quando a SDR marcava Resultado =
Atendeu (contador Conexões telefone). Lead que atendeu no Power Dialer continuava na lista até
a marcação — e podia receber, logo depois, uma ligação pelo WhatsApp. O inverso também:
quem atendeu pelo WhatsApp podia ser discado de novo pelo discador no mesmo dia.

Solução: tag `falou-hoje` por 12 h, aplicada sem depender da SDR:
  - gatilho nativo "Call Status" = completed, direção saída (ligação atendida no discador);
  - Resultado da tentativa mudou para "Atendeu" ou "Pediu retorno" (qualquer canal).
A lista "Ligar pelo WhatsApp", a "Fila do dia — SDR" e a tag `fila-sdr` (atuador_filas.py)
excluem `falou-hoje`.
"""
import sys
import ghl_interno as g
from criar_workflows_27 import Cadeia, criar, RESULTADO

TAG = "falou-hoje"
NOME = "Trava de canal — falou hoje"


def espera_horas(h):
    return {"type": "time", "startAfter": {"type": "hours", "value": h, "when": "after"},
            "name": "Wait %d Hours" % h, "cat": "", "isHybridAction": True, "hybridActionType": "wait",
            "convertToMultipath": False, "transitions": []}


def montar():
    c = Cadeia()
    t = c.add(None, "add_contact_tag", "Falou hoje (trava de canal)", {"tags": [TAG]})
    w = c.add(t, "wait", "Wait 12 Hours", espera_horas(12))
    c.add(w, "remove_contact_tag", "Fim da trava", {"tags": [TAG]})
    gats = [
        {"type": "call_status", "name": "Ligação do discador atendida", "conditions": [
            {"operator": "contains-any", "field": "call_status", "value": ["completed"], "title": "Call status",
             "type": "multiselect", "id": "call_status"},
            {"operator": "==", "field": "message.direction", "value": "outbound", "title": "Call direction",
             "type": "select"}]},
        {"type": "contact_changed", "name": "Resultado = Atendeu", "conditions": [
            {"operator": "==", "field": "contact." + RESULTADO, "value": "Atendeu", "title": "Resultado da tentativa",
             "type": "select", "id": RESULTADO}]},
        {"type": "contact_changed", "name": "Resultado = Pediu retorno", "conditions": [
            {"operator": "==", "field": "contact." + RESULTADO, "value": "Pediu retorno",
             "title": "Resultado da tentativa", "type": "select", "id": RESULTADO}]},
    ]
    return c.nos, gats


if __name__ == "__main__":
    from criar_capi import criar_varios
    nos, gats = montar()
    criar_varios(NOME, nos, gats, "--seco" in sys.argv)
