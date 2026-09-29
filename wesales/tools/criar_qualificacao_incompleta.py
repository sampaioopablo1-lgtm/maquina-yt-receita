#!/usr/bin/env python3
"""Qualificação incompleta na reunião (28/09, pedido do dono).

A ficha do contato substituiu o formulário externo: a SDR qualifica no bloco Q1–Q6 e marca
a reunião pelo ícone de calendário da própria ficha. Isto garante que o closer receba a ficha
completa: 10 min depois de uma reunião marcada (agenda do closer ou "Agendamento pela SDR"),
se faltar qualquer uma das 6 perguntas, a SDR recebe a tarefa de completar antes da reunião.

A tarefa vai para a SDR fixa (o Pós-agendamento passa o contato para o closer). Com a 2ª SDR,
trocar `SDR` ou ler o campo "SDR responsável".

    python criar_qualificacao_incompleta.py --seco
    python criar_qualificacao_incompleta.py
"""
import sys

from criar_workflows_27 import Cadeia
from criar_capi import criar_varios

NOME = "Qualificação incompleta na reunião"
SDR = "ML69c5kAJ93cliAGgBj6"
Q = [("qmIKSSDVYNLl5E8vnr3f", "Q1 Dor principal"), ("wmod0p91VuukwWDwKCgi", "Q2 Clientes novos por mês"),
     ("xjEcIFfdt2h29wBaKMQO", "Q3 Quem atende os leads"), ("SZVgh0Y5HRcWWZG4fO9V", "Q4 Budget"),
     ("3dphGCPCoFcYXEQC2jeB", "Q5 Decisor"), ("lAqbaJE9K4LDkq3t2zzc", "Q6 Prazo")]
AGENDAS = ["3uNQFjCEDe7b4gKZJuOZ", "oOfR9ADPJM0WyVyHRgKE"]


def montar():
    c = Cadeia()
    w = c.add(None, "wait", "Espera 10 min (SDR termina a ficha)", {
        "type": "time", "startAfter": {"type": "minutes", "value": 10, "when": "after"},
        "name": "Wait 10 Minutes", "cat": "", "isHybridAction": True, "hybridActionType": "wait",
        "convertToMultipath": False, "transitions": []})
    sim, _ = c.se(w, "Falta alguma das 6 perguntas?", [("contact_detail", fid, "has_no_value", None) for fid, _ in Q])
    se = c.nos[-3]
    se["attributes"]["branches"][0]["segments"][0]["operator"] = "or"   # qualquer uma vazia
    c.add(sim, "task-notification", "[COMPLETAR QUALIFICAÇÃO]", {
        "title": "[COMPLETAR QUALIFICAÇÃO] {{contact.first_name}} — antes da reunião",
        "body": ('<p style="margin:0px; padding-left: 0px!important;">A reunião de {{contact.first_name}} foi marcada, '
                 'mas a ficha está incompleta. Abra a ficha e complete o bloco <b>Q1–Q6</b> (' +
                 " · ".join(n for _, n in Q) + '). O closer entra na reunião lendo isso. Se precisar, mande '
                 'uma mensagem curta ao lead para confirmar o que faltou.</p>'),
        "assignedTo": SDR, "type": "task_notification",
        "dueDate": {"duration": 0, "unit": "days", "time": 1789851600000, "skipWeekends": False},
        "__customInputs__": {"dueDate": "duration-picker"}})
    gats = [{"type": "appointment", "name": "Reunião marcada" + ("" if i == 0 else " (agenda SDR)"), "conditions": [
        {"operator": "==", "field": "appointment.eventType", "value": "normal", "title": "Tipo de evento", "type": "select"},
        {"operator": "==", "field": "calendar.id", "value": cal, "title": "In calendar", "type": "select"},
        {"operator": "==", "field": "appointment.status", "value": "confirmed", "title": "Appointment status is", "type": "select"},
        {"operator": "is-any-of", "field": "contactMode", "value": ["contact"], "type": "input"}]}
        for i, cal in enumerate(AGENDAS)]
    return c.nos, gats


if __name__ == "__main__":
    nos, gats = montar()
    criar_varios(NOME, nos, gats, "--seco" in sys.argv)
