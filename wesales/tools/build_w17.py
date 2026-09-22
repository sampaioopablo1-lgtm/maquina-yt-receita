"""W17 - Lead Esquecido em NOVO LEAD  e  W17d - AGENDAR Estagnado.

Mesma forma nos dois (IMPLEMENTACAO-WORKFLOWS.md, W17 e W17d):
  gatilho Opportunity Stage Changed -> FUNIL DE VENDAS / <etapa>
  1 Wait 24 horas
  2 If/Else  etapa ainda == <etapa> E status == open
       sim -> Add Tag <tag> -> Notificacao ao gestor -> Add Note
       nao -> FIM
Re-entry ligado, sem janela, Stop on Response desligado. Nascem RASCUNHO.
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))


def stage_trigger(nome: str, etapa_id: str) -> dict:
    return {
        "status": "draft", "schedule_config": {},
        "type": "pipeline_stage_updated", "masterType": "highlevel",
        "name": nome, "active": True, "triggersChanged": True,
        "location_id": g.LOC,
        "conditions": [
            {"operator": "==", "field": "opportunity.pipelineId",
             "value": g.PIPELINE, "title": "No pipeline", "type": "select"},
            {"operator": "==", "field": "opportunity.pipelineStageId",
             "value": etapa_id, "title": "Movido para o estágio",
             "type": "select", "id": "moved-to-stage"},
        ],
    }


def monitor(nome, etapa, tag, titulo_notif, corpo_notif, texto_nota):
    """Monta um dos monitores de estagnacao de 24h."""
    etapa_id = g.STAGES[etapa]
    passos = [
        g.wait_step(24, "hours"),
        g.Branch(
            "Ainda em " + etapa + " e aberta?",
            [g.cond("opportunities", "pipelineStageId", "==", etapa_id),
             g.cond("opportunities", "status", "==", "open")],
            sim=[
                g.tag_step([tag]),
                g.notify_user_step(titulo_notif, corpo_notif),
                g.note_step("Alerta de saúde", texto_nota),
            ],
            nao=[],
        ),
    ]
    return passos, [stage_trigger("Etapa Do Funil Alterada", etapa_id)]


ALVOS = [
    ("Lead Esquecido em NOVO LEAD", "NOVO LEAD", "novo-lead-estagnado",
     "Lead parado em NOVO LEAD",
     "{{contact.name}} está há mais de 24h em NOVO LEAD sem revisão. "
     "Origem: {{contact.source}}.",
     "Alerta de saúde: NOVO LEAD sem revisão em 24h · "
     + g.token("right_now")),
    ("AGENDAR Estagnado", "AGENDAR", "agendar-estagnado",
     "Lead parado em AGENDAR",
     "{{contact.name}} atendeu e está há mais de 24h em AGENDAR sem reunião "
     "marcada nem desqualificação. Conectado em: {{contact.data_conectado}}.",
     "Alerta de saúde: AGENDAR sem fechar o loop em 24h · "
     + g.token("right_now")),
]

c = g.client()
existentes = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
              if w.get("type") == "workflow"}

for nome, etapa, tag, tit, corpo, nota in ALVOS:
    print("\n########## " + nome + " ##########")
    passos, gatilhos = monitor(nome, etapa, tag, tit, corpo, nota)
    c.create_location_tag(tag)
    if nome in existentes:
        wf = existentes[nome]
        atual = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
        n = len(((atual or {}).get("workflowData") or {}).get("templates") or [])
        if n:
            print("ja existe COM %d nos (%s) - nao mexo" % (n, wf))
        else:
            g.preencher(c, wf, nome, passos, gatilhos,
                        allow_reentry=True, stop_on_response=False)
            print("rascunho vazio preenchido: " + wf)
    else:
        wf = g.build(c, nome, passos, gatilhos,
                     allow_reentry=True, stop_on_response=False)
        print("criado: " + wf + "  (tag '" + tag + "' garantida)")

    doc = g.export(c, wf, os.path.join(JSON_DIR, nome + ".json"))
    w = doc["workflow"]
    print("status=%s  re-entry=%s  window=%s"
          % (w.get("status"), w.get("allowMultiple"), w.get("window")))
    for s in (w.get("workflowData") or {}).get("templates") or []:
        rot = s.get("nodeType") or s["type"]
        det = ""
        a = s.get("attributes") or {}
        if s["type"] == "add_contact_tag":
            det = str(a.get("tags"))
        elif s["type"] == "wait":
            det = str(a.get("startAfter"))
        elif s.get("nodeType") == "condition-node":
            cs = a["branches"][0]["segments"][0]["conditions"]
            det = " E ".join("%s %s %s" % (x["conditionSubType"],
                                           x["conditionOperator"],
                                           x["conditionValue"]) for x in cs)
        elif s["type"] == "internal_notification":
            det = (a.get("notification") or {}).get("title", "")
        print("   %-16s %s" % (rot, det))
    for t in (doc["triggers"] if isinstance(doc["triggers"], list) else []):
        print("   GATILHO %s -> %s" % (t.get("type"),
              [x.get("value") for x in (t.get("conditions") or [])]))
    print("   URL: https://app.wesalescrm.com/v2/location/" + g.LOC
          + "/automation/workflow/" + wf)
