#!/usr/bin/env python3
"""Registro da ligação em UM campo (29/09, pedido do dono: menos cliques para a SDR).

A SDR marca só `Registro da ligação` ("Telefone · Não atendeu", "WhatsApp · Atendeu"...).
Este workflow traduz para os dois campos de sempre — `Canal da tentativa` e `Resultado da
tentativa` — e limpa o campo novo. A mudança do Resultado dispara o Pós-ligação v3 como
antes: nada do Pós-ligação muda. Os dois campos antigos continuam valendo na mão (reserva).

    python criar_registro_1_campo.py --seco   # só monta e confere o grafo
    python criar_registro_1_campo.py          # cria e publica
"""
import copy, sys
import ghl_interno as g
from criar_workflows_27 import Cadeia, criar, uid

REGISTRO = "2iqHW8jbd41AI6fZJr6P"
CANAL = "AsZMGmsKVu1xEp36hyLb"
RESULTADO = "nPafc9c0JdSSptdPhUlF"
NOME = "Registro da ligação — 1 campo"
MAPA = [  # opção do campo novo -> (canal ou None, resultado)
    ("Telefone · Atendeu", "Telefone", "Atendeu"),
    ("Telefone · Não atendeu", "Telefone", "Não atendeu"),
    ("Telefone · Caixa postal", "Telefone", "Caixa Postal"),
    ("Telefone · Pediu retorno", "Telefone", "Pediu retorno"),
    ("Telefone · Número errado", "Telefone", "Número errado"),
    ("WhatsApp · Atendeu", "WhatsApp", "Atendeu"),
    ("WhatsApp · Não atendeu", "WhatsApp", "Não atendeu"),
    ("WhatsApp · Pediu retorno", "WhatsApp", "Pediu retorno"),
    ("Não ligar", None, "Não ligar"),
    ("Desqualificado", None, "Desqualificado"),
]


def campo(fid, titulo, valor):
    return {"field": fid, "value": valor, "title": titulo, "type": "select", "date": ""}


def condicao_modelo():
    """Condição 'campo == valor' copiada de um nó real do Pós-ligação (formato aceito pela conta)."""
    t = g.ler("8b86e5cb-97ae-4c84-ae3a-6fa11f9fe1a4")["workflowData"]["templates"]
    n = [x for x in t if x.get("name") == "Atendeu?"][0]
    return n["attributes"]["branches"][0]["segments"][0]["conditions"][0]


def montar():
    import criar_workflows_27 as base
    base.MODELO_COND = condicao_modelo()
    c = Cadeia()
    pai = None
    for opcao, canal, res in MAPA:
        sim, nao = c.se(pai, opcao, [(base.MODELO_COND["conditionType"], REGISTRO, "==", opcao)])
        fs = ([campo(CANAL, "Canal da tentativa", canal)] if canal else []) + [campo(RESULTADO, "Resultado da tentativa", res)]
        up = c.add(sim, "update_contact_field", "Grava " + opcao,
                   {"type": "update_contact_field", "actionType": "update_field_data", "fields": fs})
        c.add(up, "update_contact_field", "Limpa Registro da ligação",
              {"type": "update_contact_field", "actionType": "update_field_data",
               "fields": [campo(REGISTRO, "Registro da ligação", "")]})
        pai = nao
    gat = {"type": "contact_changed", "name": "Registro da ligação mudou", "conditions": [
        {"operator": "has-changed", "field": "contact." + REGISTRO, "title": "Registro da ligação",
         "type": "select", "id": REGISTRO}]}
    return c.nos, gat


if __name__ == "__main__":
    criar(NOME, *montar(), "--seco" in sys.argv)
