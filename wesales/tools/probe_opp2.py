"""Descobre a forma do no 'Update Opportunity' que passa na PUBLICACAO.

O validador de rascunho aceita formas que o de publicacao recusa - por isso
a primeira rodada enganou. Aqui o criterio de sucesso e publicar.
Usa um rascunho descartavel, sem gatilho, entao publicar nao afeta ninguem.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "ZZ TESTE ACOES"
ETAPA = g.STAGES["CONECTAR"]


def cif(*pares):
    return [{"filterField": f, "value": v, "valueFieldType": t}
            for f, v, t in pares]


COMBOS = [
    ("1 so status", {
        "type": "internal_update_opportunity", "allowBackward": False,
        "__customInputs__": {},
        "__customInputFields__": cif(("status", "lost", "select"))}),
    ("2 pipelineId + status", {
        "type": "internal_update_opportunity", "allowBackward": False,
        "__customInputs__": {},
        "__customInputFields__": cif(("pipelineId", g.PIPELINE, "select"),
                                     ("status", "lost", "select"))}),
    ("3 com dataType vazio", {
        "type": "internal_update_opportunity", "allowBackward": False,
        "__customInputs__": {},
        "__customInputFields__": [
            {"filterField": "pipelineId", "value": g.PIPELINE,
             "valueFieldType": "select", "dataType": ""},
            {"filterField": "status", "value": "lost",
             "valueFieldType": "select", "dataType": ""}]}),
    ("4 pipelineId solto + status em cif", {
        "type": "internal_update_opportunity", "allowBackward": False,
        "pipelineId": g.PIPELINE, "__customInputs__": {},
        "__customInputFields__": cif(("status", "lost", "select"))}),
    ("5 tudo solto (camelCase)", {
        "type": "internal_update_opportunity", "allowBackward": False,
        "pipelineId": g.PIPELINE, "pipelineStageId": ETAPA, "status": "lost",
        "__customInputs__": {}, "__customInputFields__": []}),
    ("6 valueFieldType string", {
        "type": "internal_update_opportunity", "allowBackward": False,
        "__customInputs__": {},
        "__customInputFields__": cif(("status", "lost", "string"))}),
    ("7 filterField opportunityStatus", {
        "type": "internal_update_opportunity", "allowBackward": False,
        "__customInputs__": {},
        "__customInputFields__": cif(("opportunityStatus", "lost", "select"))}),
]

c = g.client()
lst = c.request("GET", "/workflow/" + g.LOC)
ja = [w for w in lst if w.get("name") == NOME and w.get("type") == "workflow"]
wf = ja[0]["id"] if ja else g.create_workflow(c, NOME)

for rotulo, attrs in COMBOS:
    no = {"id": g.uid(), "name": "Update Opportunity",
          "type": "internal_update_opportunity", "attributes": attrs,
          "order": 0, "parentKey": None}
    cur = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
    v = cur.get("version", 1)
    salvo = c.request("PUT", "/workflow/" + g.LOC + "/" + wf,
                      {"name": NOME, "status": "draft", "version": v,
                       "workflowData": {"templates": [no]}})
    if salvo and salvo.get("_error"):
        print("  %-34s rascunho RECUSOU" % rotulo)
        continue
    cur = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
    pub = c.request("PUT", "/workflow/" + g.LOC + "/" + wf,
                    {"name": NOME, "status": "published",
                     "version": cur.get("version", 1),
                     "workflowData": {"templates":
                                      cur["workflowData"]["templates"]}})
    if pub and pub.get("_error"):
        m = str(pub.get("message")).split("errorMessage")[-1][:70]
        print("  %-34s publicacao RECUSOU %s" % (rotulo, m))
    else:
        print("  %-34s >>> PUBLICOU <<<" % rotulo)
        volta = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
        print("     salvo como: " + json.dumps(
            volta["workflowData"]["templates"][0], ensure_ascii=False)[:420])
        # devolve para rascunho: e so um workflow de teste
        c.request("PUT", "/workflow/" + g.LOC + "/" + wf,
                  {"name": NOME, "status": "draft",
                   "version": volta.get("version", 1),
                   "workflowData": {"templates":
                                    volta["workflowData"]["templates"]}})
        break
