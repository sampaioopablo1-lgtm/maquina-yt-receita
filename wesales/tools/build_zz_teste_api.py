"""PASSO 1 - prova de vida da API interna.

ZZ TESTE API (rascunho):
  gatilho Contact Tag Added (teste-api) -> Add Note
  "criado pela API interna em {{right_now}}"
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ghl_api as g

NOME = "ZZ TESTE API"
TAG = "teste-api"
OUT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "workflows-json", NOME + ".json"))

c = g.client()

existentes = c.request("GET", "/workflow/" + g.LOC)
ja = [w for w in existentes if w.get("name") == NOME]
if ja:
    print("ja existe '" + NOME + "' id=" + ja[0]["id"] + " - nao recrio.")
    wf = ja[0]["id"]
else:
    nota = g.note_step(
        "ZZ TESTE API",
        "criado pela API interna em " + g.token("right_now"))
    wf = g.build(c, NOME, [nota],
                 [g.tag_trigger("Teste Api", TAG)],
                 tags_to_create=[TAG])
    print("criado: " + wf)

doc = g.export(c, wf, OUT)
w = doc["workflow"]
print("")
print("== LEITURA DE VOLTA PELA API ==")
print("nome:   " + str(w.get("name")))
print("status: " + str(w.get("status")))
tpl = (w.get("workflowData") or {}).get("templates") or []
print("nos:    " + str(len(tpl)))
for s in tpl:
    print("  - " + str(s.get("type")) + " | " + str(s.get("name")))
    if s.get("type") == "add_notes":
        print("    html: " + str(s["attributes"].get("html")))
trs = doc["triggers"] if isinstance(doc["triggers"], list) else []
print("gatilhos: " + str(len(trs)))
for t in trs:
    print("  - tipo=" + str(t.get("type")) + " cond=" + str(t.get("conditions"))
          + " target=" + str(t.get("targetActionId")))
print("")
print("JSON salvo em: " + OUT)
print("URL: https://app.wesalescrm.com/v2/location/" + g.LOC
      + "/automation/workflows/" + wf)
