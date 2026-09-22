"""Pos-ligacao v2 - conserta os quatro nos que escreviam em campo nenhum.

DEFEITO: o publicado tem 4 `math_operation` com `updateField` VAZIO. Somam
1 ou 0 em lugar algum. Ficam todos dentro do ramo `Resultado da tentativa
== Atendeu`, um par por canal (o If de `fila-wa` separa WhatsApp de
telefone).

O que cada par deveria ser, pela posicao + spec (secao 4) + dado observado:
- `add 1`  -> `Total de conexoes` + 1. E o que explica o dado: `Conexoes
  telefone` chegou a 8 no contato de teste e `Total de conexoes` ficou
  vazio o tempo todo.
- `add 0`  -> zerar `WA nao atendidas seguidas` ao atender. `Math add 0`
  NAO zera nada - soma zero. Vira `update_contact_field` = 0, que e a acao
  certa para "definir valor". Esse campo e lido pelo no 4 da Cadencia 12x30
  para decidir se o toque sai por WhatsApp; sem nunca ser preenchido, a
  decisao roda com o campo vazio.

O resto do workflow e clone fiel do publicado.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g
import clone_workflow as cl

NOME = "Pós-ligação v2"
ORIG = "cf6fa19d-6af8-4fcb-b0dd-6fcfcefde0cc"
C = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"),
                   encoding="utf-8"))
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))
TOTAL_CONEX = C["Total de conexões"]["id"]
WA_NAO = C["WA não atendidas seguidas"]["id"]

c = g.client()
orig = c.request("GET", "/workflow/" + g.LOC + "/" + ORIG)
tpl = cl.remapear(orig["workflowData"]["templates"])

corrigidos = []
for s in tpl:
    if s["type"] != "math_operation":
        continue
    a = s["attributes"]
    if a.get("updateField"):
        continue
    op = (a.get("operators") or [{}])[0]
    if op.get("value") == 1:
        a["selectField"] = TOTAL_CONEX
        a["updateField"] = TOTAL_CONEX
        a["selectFieldtype"] = "numerical"
        a["updateFieldType"] = "numerical"
        s["name"] = "Total de conexões +1"
        corrigidos.append("somar Total de conexões")
    else:
        # 'somar zero' nao zera: vira definir valor = 0
        s["type"] = "update_contact_field"
        s["name"] = "Zera WA não atendidas seguidas"
        s["attributes"] = {
            "type": "update_contact_field",
            "actionType": "update_field_data",
            "fields": [{"field": WA_NAO, "value": 0,
                        "title": "WA não atendidas seguidas",
                        "type": "numerical", "date": ""}]}
        corrigidos.append("zerar WA não atendidas seguidas")

print("nos corrigidos: %d" % len(corrigidos))
for x in corrigidos:
    print("  - " + x)
if len(corrigidos) != 4:
    raise SystemExit("esperava 4 nos quebrados, achei %d - nao sigo"
                     % len(corrigidos))

gatilhos = [t for t in (c.request("GET", "/workflow/" + g.LOC
                                  + "/trigger?workflowId=" + ORIG) or [])
            if not t.get("deleted")]
ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
       if w.get("type") == "workflow"}
wf = ids.get(NOME) or g.create_workflow(c, NOME)
g.guard(wf)

ja = [x for x in (c.request("GET", "/workflow/" + g.LOC
                            + "/trigger?workflowId=" + wf) or [])
      if not x.get("deleted")]
raiz = cl.raiz(tpl)
for i, t in enumerate(gatilhos):
    body = {"status": "draft", "schedule_config": {}, "type": t.get("type"),
            "masterType": "highlevel", "name": t.get("name"), "active": True,
            "triggersChanged": True, "location_id": g.LOC,
            "conditions": t.get("conditions") or [], "workflowId": wf,
            "actions": [{"workflow_id": wf, "type": "add_to_workflow"}]}
    tid = ja[i]["id"] if i < len(ja) else (c.request(
        "POST", "/workflow/" + g.LOC + "/trigger", body) or {}).get("id")
    if tid:
        c.request("PUT", "/workflow/" + g.LOC + "/trigger/" + tid,
                  dict(body, targetActionId=raiz,
                       advanceCanvasMeta={"position": {"x": 57.5, "y": -73}}))

cur = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
r = c.request("PUT", "/workflow/" + g.LOC + "/" + wf,
              {"name": NOME, "status": "draft",
               "version": cur.get("version", 1) if isinstance(cur, dict) else 1,
               "allowMultiple": True, "stopOnResponse": False,
               "workflowData": {"templates": tpl}})
if r and r.get("_error"):
    raise SystemExit("falhou: " + str(r.get("message"))[:200])

doc = g.export(c, wf, os.path.join(JSON_DIR, NOME + ".json"))
t2 = (doc["workflow"].get("workflowData") or {}).get("templates") or []
vazios = [s for s in t2 if s["type"] == "math_operation"
          and not (s["attributes"].get("updateField") or "")]
print("nos=%d | math ainda sem campo: %d" % (len(t2), len(vazios)))
print("nasce RASCUNHO")
