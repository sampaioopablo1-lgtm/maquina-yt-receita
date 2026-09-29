#!/usr/bin/env python3
"""MI-0 — 1ª mensagem do lead de formulário (28/09, pedido do dono).

Todo lead novo de formulário recebe uma mensagem no WhatsApp para abrir a conversa, focada na
dor, sem pedir licença para ligar. Sai na hora, todos os dias, das 08:30 às 22:00 (janela do
workflow); fora disso, espera o próximo 08:30. Antes vivia dentro da Cadência Inbound, que só
roda seg–sex 08:30–21:00, e atrás do laço do governador, que travava (DE-PARA, 28/09).

Não manda quando:
  - o lead já escreveu (campo "Sinal recebido", preenchido pela Interceptação de Sinal) — a
    SDR responde a conversa dele;
  - o lead já recebeu alguma mensagem ("Template usado" preenchido) — evita repetir quando a
    oportunidade volta para CONECTAR;
  - `nao-perturbe` ou sem telefone.
Espera 2 min antes de decidir, para a mensagem de quem clicou no WhatsApp do anúncio chegar.

    python criar_mi0.py --seco   # só monta e valida o grafo
    python criar_mi0.py          # cria e publica
"""
import sys

import ghl_interno as g
from criar_workflows_27 import Cadeia, criar, PIPE, CONECTAR

NOME = "MI-0 — 1ª mensagem do lead de formulário"
SINAL, TEMPLATE, TEL_OK = "jfQgrZFnxhbn1qmCeFDC", "StguwRaz0AVlQqzaAoFh", "phone"
TEXTO = ("Oi, {{contact.first_name}}! Aqui é {{user.first_name}}, da O Próximo Cliente. Recebi seu "
         "cadastro agora. Quase todo dono de negócio que fala com a gente vive o mesmo aperto: mês bom, "
         "mês fraco, porque o cliente novo depende de indicação. Hoje, o que mais trava a entrada de "
         "clientes novos aí? Me conta em uma frase que eu já te mostro o caminho.")


def montar():
    c = Cadeia()
    w = c.add(None, "wait", "Espera 2 min (mensagem do anúncio chegar)", {
        "type": "time", "startAfter": {"type": "minutes", "value": 2, "when": "after"},
        "name": "Wait 2 Minutes", "cat": "", "isHybridAction": True, "hybridActionType": "wait",
        "convertToMultipath": False, "transitions": []})
    sim, _ = c.se(w, "Lead de formulário que ainda não conversou?", [
        ("contact_detail", "tags", "index-of-true", ["cad-inbound"]),
        ("contact_detail", "tags", "index-of-false", ["nao-perturbe"]),
        ("contact_detail", TEL_OK, "has_value", None),
        ("contact_detail", SINAL, "has_no_value", None),
        ("contact_detail", TEMPLATE, "has_no_value", None)])
    m = c.add(sim, "sms", "WhatsApp · MI-0 (dor)", {"type": "sms", "body": TEXTO, "attachments": []})
    c.add(m, "update_contact_field", "Template usado = MI-0", {
        "type": "update_contact_field", "actionType": "update_field_data",
        "fields": [{"field": TEMPLATE, "value": "MI-0", "title": "Template usado", "type": "text", "date": ""}]})
    gat = {"type": "pipeline_stage_updated", "name": "Entrou em CONECTAR", "conditions": [
        {"operator": "==", "field": "opportunity.pipelineId", "value": PIPE, "title": "No pipeline", "type": "select"},
        {"operator": "==", "field": "opportunity.pipelineStageId", "value": CONECTAR, "title": "Movido para o estágio",
         "type": "select", "id": "moved-to-stage"}]}
    return c.nos, gat


if __name__ == "__main__":
    nos, gat = montar(); seco = "--seco" in sys.argv
    criar(NOME, nos, gat, seco)
    if not seco:
        w = g.por_nome(NOME); cur = g.ler(w["id"])
        cur.update({"window": {"days": [0, 1, 2, 3, 4, 5, 6], "startHour": 8, "startMinute": 30, "endHour": 22,
                               "endMinute": 0}, "allowMultiple": False, "stopOnResponse": True})
        g.put(cur, cur["workflowData"]["templates"]); d = g.ler(w["id"])
        print("final:", w["id"], d["status"], "v%s" % d["version"], d.get("window"), d.get("allowMultiple"),
              [(t["name"], t.get("active")) for t in g.gatilhos(w["id"])])
