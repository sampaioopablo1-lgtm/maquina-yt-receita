"""Descobre a forma aceita do no 'Update Opportunity' testando varias
combinacoes contra um rascunho descartavel. Cada tentativa e um PUT: a que
salvar sem erro e a certa.
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "ZZ TESTE ACOES"
ETAPA = g.STAGES["CONECTAR"]

COMBOS = [
    ("A tipo=internal_ attrs com type", "internal_update_opportunity",
     {"type": "internal_update_opportunity", "allowBackward": False,
      "__customInputs__": {},
      "__customInputFields__": [{"filterField": "status", "value": "lost",
                                 "valueFieldType": "select"}]}),
    ("B tipo=internal_ attrs SEM type", "internal_update_opportunity",
     {"allowBackward": False, "__customInputs__": {},
      "__customInputFields__": [{"filterField": "status", "value": "lost",
                                 "valueFieldType": "select"}]}),
    ("C tipo=internal_ attrs camelCase", "internal_update_opportunity",
     {"pipelineId": g.PIPELINE, "pipelineStageId": ETAPA, "status": "lost",
      "allowBackward": False}),
    ("D tipo=update_opportunity snake", "update_opportunity",
     {"fields": [], "type": "update_opportunity", "pipeline_id": g.PIPELINE,
      "opportunity_status": "lost"}),
    ("E tipo=update_opportunity camel", "update_opportunity",
     {"pipelineId": g.PIPELINE, "status": "lost", "allowBackward": False}),
    ("F tipo=opportunity", "opportunity",
     {"type": "opportunity", "status": "lost", "pipelineId": g.PIPELINE}),
    ("G tipo=internal_ com meta.key", "internal_update_opportunity",
     {"type": "internal_update_opportunity", "allowBackward": False,
      "meta": {"key": "internal_update_opportunity"},
      "__customInputs__": {},
      "__customInputFields__": [{"filterField": "status", "value": "lost",
                                 "valueFieldType": "select"}]}),
    ("H igual ao create real", "update_opportunity",
     {"fields": [], "type": "update_opportunity", "pipeline_id": g.PIPELINE,
      "pipeline_stage_id": ETAPA, "opportunity_name": "{{contact.name}}",
      "opportunity_status": "lost", "opportunity_source": "",
      "monetary_value": ""}),
]

c = g.client()
lst = c.request("GET", "/workflow/" + g.LOC)
ja = [w for w in lst if w.get("name") == NOME and w.get("type") == "workflow"]
wf = ja[0]["id"] if ja else g.create_workflow(c, NOME)
print("rascunho de teste: " + wf + "\n")

for rotulo, tipo, attrs in COMBOS:
    no = {"id": g.uid(), "name": "Atualizar oportunidade", "type": tipo,
          "attributes": attrs, "order": 0, "parentKey": None}
    r = c.request("PUT", "/workflow/" + g.LOC + "/" + wf,
                  {"name": NOME, "status": "draft", "version": 1,
                   "workflowData": {"templates": [no]}})
    if r and r.get("_error"):
        msg = str(r.get("message"))
        curto = msg.split("errorMessage")[-1][:110]
        print("  %-34s RECUSADO %s" % (rotulo, curto))
    else:
        print("  %-34s >>> ACEITO <<<" % rotulo)
        volta = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
        t = (volta.get("workflowData") or {}).get("templates") or []
        if t:
            import json
            print("     como ficou salvo: "
                  + json.dumps(t[0], ensure_ascii=False)[:400])
        break
