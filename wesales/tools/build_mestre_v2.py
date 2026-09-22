"""Mestre de saida v2 - nao trata lead que ACABOU DE CHEGAR como saida.

DEFEITO CORRIGIDO: o portao do publicado pergunta "etapa == CONECTAR E
status == open?". Quando uma oportunidade NASCE em NOVO LEAD a resposta e
nao, e ele cai no ramo de limpeza: remove tags de fila e aplica
`limpar-tarefas`. Por isso os 10 leads criados depois de 19/09 nasceram
com essa tag (ja registrado no GUIA-MONTAGEM.md como 'efeito colateral
real').

Era inofensivo enquanto nao havia tarefa de cadencia. Deixou de ser: a
Cadencia 12x30 esta publicada e cria tarefas [CADENCIA], e `limpar-tarefas`
e exatamente a tag que autoriza a rotina de higiene a fechar tarefa
[CADENCIA] vencida. Um lead que chega marcado assim pode ter a tarefa da
propria cadencia apagada.

A correcao e um portao na frente: se a etapa e NOVO LEAD, nao ha nada para
limpar - encerra. O resto do fluxo fica identico ao publicado.
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g
import clone_workflow as cl

NOME = "Mestre de saída v2"
ORIG = "30da2c98-5f84-4af9-9ed2-71f628dc7c1e"
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))

c = g.client()
orig = c.request("GET", "/workflow/" + g.LOC + "/" + ORIG)
corpo = cl.remapear(orig["workflowData"]["templates"])

portao = g.Branch(
    "Acabou de chegar em NOVO LEAD?",
    [g.cond("opportunities", "pipelineStageId", "==", g.STAGES["NOVO LEAD"])],
    sim=[],        # chegou agora: nao ha saida de cadencia para limpar
    nao=[],        # o fluxo original entra aqui
)
armacao = g.montar([portao])
no_nao = [s for s in armacao if s.get("nodeType") == "branch-no"][0]
corpo = cl.pendurar_em(corpo, no_nao["id"])
no_nao["next"] = cl.raiz(corpo)
tpl = armacao + corpo

gatilhos = [t for t in (c.request("GET", "/workflow/" + g.LOC
                                  + "/trigger?workflowId=" + ORIG) or [])
            if not t.get("deleted")]
print("gatilhos do original: %d" % len(gatilhos))

ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
       if w.get("type") == "workflow"}
wf = ids.get(NOME) or g.create_workflow(c, NOME)
g.guard(wf)

ja = [x for x in (c.request("GET", "/workflow/" + g.LOC
                            + "/trigger?workflowId=" + wf) or [])
      if not x.get("deleted")]
for i, t in enumerate(gatilhos):
    body = {"status": "draft", "schedule_config": {}, "type": t.get("type"),
            "masterType": "highlevel", "name": t.get("name"), "active": True,
            "triggersChanged": True, "location_id": g.LOC,
            "conditions": t.get("conditions") or [],
            "workflowId": wf,
            "actions": [{"workflow_id": wf, "type": "add_to_workflow"}]}
    tid = ja[i]["id"] if i < len(ja) else (c.request(
        "POST", "/workflow/" + g.LOC + "/trigger", body) or {}).get("id")
    if tid:
        c.request("PUT", "/workflow/" + g.LOC + "/trigger/" + tid,
                  dict(body, targetActionId=portao.id,
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
w = doc["workflow"]
t2 = (w.get("workflowData") or {}).get("templates") or []
vivos = {s["id"] for s in t2}
print("nos=%d (original %d + portao 3)" % (len(t2), len(corpo)))
print("gotos quebrados:", sum(1 for s in t2 if s["type"] == "goto"
                              and (s.get("attributes") or {}).get("targetNodeId") not in vivos))
trs = [t for t in (c.request("GET", "/workflow/" + g.LOC
                             + "/trigger?workflowId=" + wf) or [])
       if not t.get("deleted")]
print("gatilhos: %d | todos ligados: %s"
      % (len(trs), all(t.get("targetActionId") in vivos for t in trs)))
print("nasce RASCUNHO")
