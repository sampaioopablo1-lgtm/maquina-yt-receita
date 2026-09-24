"""`Pós-ligação v3` — reconstrução limpa (auditoria de 23/09/2026).

O v2 (146 nós) era clone de clone com remendos. Defeitos medidos ao vivo:
  - Caixa Postal tratada como Atendeu (ramo copiado: fechar-horario, tarefa
    de qualificar, nota "Atendeu", Conexões +1) -> o lead recebia MFH1 "foi bom
    falar com você" sem ter falado;
  - Desqualificado não existia no seletor -> lead sem fit seguia sendo ligado;
  - Não ligar só tirava da 12x30 (Fechar Horário/Inbound/Nutrição seguiam);
  - Total de conexões +1 e "zera WA seguidas" no ramo Não atendeu (patch caiu
    no ramo errado); ~40 nós mortos (if de canal duplicado);
  - tarefas vencendo "hoje 08:00" (nasciam vencidas); Pediu retorno ignorava
    a data/hora combinadas e jogava o lead em fila-quente.

Desenho (um seletor só; canal decidido uma vez):
  Resultado vazio -> fim
  Total de ligações +1; canal (tag fila-wa) -> Tentativas WhatsApp|telefone +1
  Atendeu        -> Conexões (canal) +1, Canal que conectou, Total de conexões
                    +1, WA seguidas = 0, Data conectado, +conectado-hoje
                    +fechar-horario, -filas, sai das cadências, tarefa
                    [FECHAR HORÁRIO] (vence hoje 18:00), nota
  Não atendeu / Caixa Postal -> (WhatsApp: WA seguidas +1) -filas +limpar-tarefas
  Pediu retorno  -> -filas; com Data de retorno: tarefa [RETORNO] no horário
                    combinado; sem data: tarefa [RETORNO] preencher data/hora
  Não ligar      -> nao-perturbe + DND (saída), -filas/fechar-horario/
                    retorno-vencido, sai de TODOS os workflows, perdido, nota
  Número errado  -> telefone-invalido, -filas, sai das cadências; com e-mail ou
                    Instagram: abandonado + aviso "ache outro contato"; sem: perdido
  Desqualificado -> -filas, sai das cadências, perdido, nota com o motivo;
                    motivo vazio -> aviso para preencher
Sem janela: reage ao clique do SDR (Não ligar às 18:40 de sexta não pode
esperar segunda). Tarefas nascem por ação humana, não por agenda.

Uso: python build_posligacao_v3.py [--so-montar] [--publicar]
"""
import copy, io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "Pós-ligação v3"
F = {"resultado": "nPafc9c0JdSSptdPhUlF", "tot_lig": "JUBhmz0DGQMvjLCxSNrk",
     "tent_wa": "5j9SerJeZ6ngfZCPb2Wg", "tent_tel": "wCzdqF7uLQwtrZ1JyZRn",
     "con_wa": "Og1CkI9x9OztsV242nIM", "con_tel": "LB11ao0AdSI1QSHyZBOP",
     "tot_con": "tQ7Fzo6cWeBDmEoaTBIZ", "wa_seg": "FnphiGDVkijSNDEP53c3",
     "canal": "TxJmoWdkA8rTqC1uEsMW", "data_con": "uJnePU1Tl1Zr1fTxYKIz",
     "data_ret": "IBOMNQecWtIUruHpNAs1", "motivo": "5L0RMR1HZVQ7IevyjOQX",
     "instagram": "2tLo2m4KLTcP6fTEq3LG"}
WF = {"12x30": "c64a808b-3040-431e-8015-642a265e1022",
      "12x30p2": "17e6dc19-3eca-42e8-83ff-e25a9d5c28e8",
      "inbound": "c2375e2f-b4cb-4947-8377-7c1e0529ba82",
      "fechar": "82dd1fad-1bdd-44f7-8214-3a685521e2b4"}
HOJE_18H = 1789851600000          # só a hora conta: 18:00 BRT
FILAS = ["fila-tel", "fila-wa", "fila-quente"]


def cd(sub, op, val=None):
    return g.cond("contact_detail", sub, op, val)


def conta(campo, nome):
    return {"id": g.uid(), "name": nome, "type": "math_operation",
            "attributes": {"type": "math_operation", "selectField": F[campo], "selectFieldtype": "numerical",
                           "sourceCustomValueId": "", "updateField": F[campo], "updateFieldType": "numerical",
                           "operators": [{"operator": "add", "__id": g.uid(), "value": 1}]}}


def campos(nome, *pares):
    fs = []
    for campo, titulo, valor, tipo in pares:
        f = {"field": F[campo], "value": valor, "title": titulo, "type": tipo, "date": ""}
        if tipo == "date":
            f["date"] = "customDate"
        fs.append(f)
    return {"id": g.uid(), "name": nome, "type": "update_contact_field",
            "attributes": {"type": "update_contact_field", "actionType": "update_field_data", "fields": fs}}


def tarefa(titulo, corpo):
    return {"id": g.uid(), "name": "Tarefa · " + titulo[:40], "type": "task-notification",
            "workflowsActionType": "INTERNAL",
            "attributes": {"title": titulo, "body": "<p>%s</p>" % corpo, "assignedTo": "contact.assigned_user",
                           "dueDate": {"duration": 0, "unit": "days", "time": HOJE_18H, "skipWeekends": True},
                           "type": "task_notification", "__customInputs__": {}}}


def aviso(titulo, corpo):
    return {"id": g.uid(), "name": "Aviso · " + titulo[:40], "type": "internal_notification",
            "attributes": {"type": "notification", "notification": {
                "type": "send_notification", "title": titulo, "body": corpo, "userType": "assign",
                "assignedOwners": ["contact_owner"], "redirectPage": "contact"}}}


def oportunidade(status, nome):
    return {"id": g.uid(), "name": nome, "type": "create_opportunity",
            "attributes": {"fields": [], "type": "create_opportunity", "pipeline_id": g.PIPELINE,
                           "opportunity_status": status, "opportunity_name": "",
                           "opportunity_source": "", "monetary_value": ""}}


def tira(*chaves):
    return {"id": g.uid(), "name": "Sai das cadências", "type": "remove_from_workflow",
            "attributes": {"type": "remove_from_workflow", "workflow_id": [WF[k] for k in chaves]}}


def nota(txt):
    return g.note_step("Nota", txt)


# ---- ramos -------------------------------------------------------------------
a2 = [conta("tot_con", "Total de conexões +1"),
      campos("Zera WA seguidas + Data conectado",
             ("wa_seg", "WA não atendidas seguidas", 0, "numerical"),
             ("data_con", "Data conectado", "{{right_now.year}}-{{right_now.month}}-{{right_now.day}}", "date")),
      g.tag_step(["conectado-hoje", "fechar-horario"]),
      g.tag_step(FILAS, remove=True),
      tira("12x30", "12x30p2", "inbound"),
      tarefa("[FECHAR HORÁRIO] Qualificar e agendar a reunião de diagnóstico",
             "O lead atendeu e ainda não tem reunião. Hoje: confirme a dor principal, preencha o "
             "formulário de qualificação e marque no calendário \"Reunião com closer\" (60 min). "
             "Se marcar, o resto sai sozinho."),
      nota("Atendeu · canal {{contact.canal_que_conectou}} · Fechar Horário ativo")]
ATENDEU = [g.Branch("Atendeu pelo WhatsApp?", [cd("tags", "index-of-true", ["fila-wa"])],
                    [conta("con_wa", "Conexões WhatsApp +1"),
                     campos("Canal = Ligação WhatsApp", ("canal", "Canal que conectou", "Ligação WhatsApp", "select")),
                     g.goto_step(a2[0]["id"])],
                    [conta("con_tel", "Conexões telefone +1"),
                     campos("Canal = Ligação normal", ("canal", "Canal que conectou", "Ligação normal", "select"))] + a2)]

b2 = [g.tag_step(["fila-tel", "fila-wa"], remove=True), g.tag_step(["limpar-tarefas"])]
NAO_ATENDEU = [g.Branch("Não atendeu pelo WhatsApp?", [cd("tags", "index-of-true", ["fila-wa"])],
                        [conta("wa_seg", "WA não atendidas seguidas +1"), g.goto_step(b2[0]["id"])], b2)]

RETORNO = [g.tag_step(["fila-tel", "fila-wa"], remove=True),
           g.Branch("Data de retorno preenchida?", [cd(F["data_ret"], "has_value")],
                    [tarefa("[RETORNO] Ligar no horário combinado: {{contact.data_de_retorno}} às {{contact.hora_do_retorno}}",
                            "O lead pediu para você ligar neste horário. Ligue e marque o novo Resultado da tentativa.")],
                    [tarefa("[RETORNO] Preencher Data e Hora do retorno",
                            "O lead pediu retorno, mas a data não foi preenchida. Preencha \"Data de retorno\" e "
                            "\"Hora do retorno\" com o que foi combinado — senão ninguém é avisado.")])]

NAO_LIGAR = [g.tag_step(["nao-perturbe"]),
             {"id": g.uid(), "name": "DND de saída", "type": "dnd_contact",
              "attributes": {"type": "dnd_contact", "dnd_direction": "outbound", "dnd_contact": "enable",
                             "specific_channels": []}},
             g.tag_step(FILAS + ["fechar-horario", "retorno-vencido"], remove=True),
             {"id": g.uid(), "name": "Sai de todas as réguas", "type": "remove_from_all_workflows",
              "attributes": {"type": "remove_from_all_workflows", "includeCurrent": False}},
             oportunidade("lost", "Perdido (não ligar)"),
             nota("Não ligar — pedido do lead na ligação. DND de saída ligado e fora de todas as réguas.")]

NUMERO_ERRADO = [g.tag_step(["telefone-invalido"]),
                 g.tag_step(FILAS + ["fechar-horario"], remove=True),
                 tira("12x30", "12x30p2", "inbound", "fechar"),
                 g.Branch("Tem outro contato (e-mail ou Instagram)?",
                          [cd("email", "has_value"), cd(F["instagram"], "has_value")],
                          [oportunidade("abandoned", "Abandonado (achar outro contato)"),
                           aviso("Número errado — ache outro contato",
                                 "Número errado: {{contact.name}} · {{contact.phone}} · origem {{contact.source}}. "
                                 "Procure outro contato (e-mail/Instagram/site) e corrija o telefone. "
                                 "Se achar, mova de volta para CONECTAR.")],
                          [oportunidade("lost", "Perdido (número errado, sem outro contato)"),
                           aviso("Número errado — perdido",
                                 "Número errado e sem outro contato: {{contact.name}} · {{contact.phone}}. "
                                 "Marcado como perdido.")], operador="or")]

DESQUALIFICADO = [g.tag_step(FILAS + ["fechar-horario"], remove=True),
                  tira("12x30", "12x30p2", "inbound", "fechar"),
                  oportunidade("lost", "Perdido (desqualificado)"),
                  nota("Desqualificado pelo SDR — motivo: {{contact.motivo_da_desqualificao}}"),
                  g.Branch("Motivo preenchido?", [cd(F["motivo"], "has_value")], [],
                           [aviso("Preencha o motivo da desqualificação",
                                  "{{contact.name}} foi marcado como Desqualificado sem motivo. Preencha "
                                  "\"Motivo da desqualificação\" — é o que mostra onde o funil perde.")])]


def res(v):
    return cd(F["resultado"], "==", v)


SELETOR = g.Branch("Atendeu?", [res("Atendeu")], ATENDEU, [
    g.Branch("Não atendeu ou caixa postal?", [res("Não atendeu"), res("Caixa Postal")], NAO_ATENDEU, [
        g.Branch("Pediu retorno?", [res("Pediu retorno")], RETORNO, [
            g.Branch("Não ligar?", [res("Não ligar")], NAO_LIGAR, [
                g.Branch("Número errado?", [res("Número errado")], NUMERO_ERRADO, [
                    g.Branch("Desqualificado?", [res("Desqualificado")], DESQUALIFICADO, [])])])])],
        operador="or")])

passos = [g.Branch("Resultado vazio?", [cd(F["resultado"], "has_no_value")], [], [
    conta("tot_lig", "Total de ligações +1"),
    g.Branch("Ligação pelo WhatsApp?", [cd("tags", "index-of-true", ["fila-wa"])],
             [conta("tent_wa", "Tentativas WhatsApp +1"), g.goto_step(SELETOR.id)],
             [conta("tent_tel", "Tentativas telefone +1"), SELETOR])])]

if __name__ == "__main__":
    nos = g.montar(copy.deepcopy(passos))
    ids = {n["id"] for n in nos}
    ruins = [n["name"] for n in nos if n["type"] == "goto" and n["attributes"]["targetNodeId"] not in ids]
    print(len(nos), "nós | ids únicos:", len(ids) == len(nos), "| goto quebrado:", ruins)
    if "--so-montar" in sys.argv:
        sys.exit(0)
    c = g.client()
    todos = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    modelo = [t for t in c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + todos["Pós-ligação v2"])
              if not t.get("deleted")][0]
    gat = {k: copy.deepcopy(modelo[k]) for k in ("type", "conditions", "masterType") if k in modelo}
    gat.update({"status": "draft", "schedule_config": {}, "name": "Resultado da tentativa mudou",
                "active": True, "triggersChanged": True, "location_id": g.LOC})
    wf = todos.get(NOME) or g.create_workflow(c, NOME)
    g.preencher(c, wf, NOME, passos, [gat], allow_reentry=True, stop_on_response=False)
    g.export(c, wf, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "workflows-json", NOME + ".json"))
    print("rascunho:", wf, NOME)
    if "--publicar" in sys.argv:
        print("publicar:", g.publicar(c, wf))
