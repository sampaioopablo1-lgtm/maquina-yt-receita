"""Pos-agendamento v2 - com a regua de qualificacao que nunca foi montada.

DEFEITO CORRIGIDO: o `Pós-agendamento` publicado nao tem NENHUM no de
calculo - so uma nota de texto com o titulo 'Nota de qualificação'. O campo
numerico nunca foi escrito (vazio nos 3 leads em NEGOCIAR, ja registrado no
GUIA-MONTAGEM.md). Consequencia em cadeia: os nos 5 e 6 do Loop do closer
leem essa nota para cobrar o closer e, sem ela, NUNCA disparam. A regua
inteira da secao 9.1 estava morta.

Esta copia clona o publicado e insere a regua (Math Operation em serie)
antes da nota, exatamente onde a spec manda (secao 5, no 4).

RESSALVA G-04, que a propria spec levanta: o Meta Lead Ads grava em
`Investimento mensal em anúncios` textos que NAO sao opcao do campo
('Abaixo de 5k', 'Até R$ 1.000', 'Não invisto nada ainda'). Lead vindo do
Meta perde os 12 pontos desse bloco ate o dono decidir o G-04. Lead
preenchido por gente pontua certo. Montar assim e melhor que nao pontuar:
hoje a nota e sempre vazia.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g
import clone_workflow as cl

NOME = "Pós-agendamento v2"
ORIG = "94a837d0-d87a-438e-95f1-c620d55f1a7f"
C = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"),
                   encoding="utf-8"))
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))
NOTA = C["Nota de qualificação"]["id"]

# (campo, rotulo, [(valor exato na tela, pontos)]) - secao 9.1
REGUA = [
    ("Clientes novos por mês", [("10", 3), ("11-30", 6), ("31-100", 8),
                                ("+101", 10)]),
    ("Tem time comercial", [("Só dono", 3), ("1-5", 7), ("6-10", 9),
                            ("+10", 10)]),
    ("Quem atende os leads", [("Ninguém fixo", 10), ("Dono", 7),
                              ("Vendedor", 5), ("SDR", 3)]),
    ("Investe em anúncios", [("Sim", 13), ("Já investiu e parou", 9),
                             ("Nunca", 4)]),
    ("Investimento mensal em anúncios", [("Acima de 10k", 12),
                                         ("5k a 10k", 10), ("1k a 5k", 6),
                                         ("Até 1k", 2)]),
    ("Budget", [("Tem", 15), ("Precisa aprovar", 9), ("Não tem", 0)]),
    ("Decisor", [("Sim", 15), ("Influencia", 8), ("Não decide", 2)]),
    ("Prazo", [("Pra ontem", 15), ("Espera 30 dias", 11), ("Este ano", 6),
               ("Sem prazo", 2)]),
]


def pontuar(rotulo, campo_id, opcoes, proximo, fim_id):
    """Cadeia de If/Else de um campo.

    Cada opcao mora no ramo 'nao' da anterior; casou, soma e SALTA para o
    proximo campo. O proximo campo MORA no ramo 'nao' da ultima opcao - nao
    pode ser so alvo de goto, senao fica fora do grafo (erro cometido na
    primeira tentativa: 5 gotos para nos inexistentes)."""
    destino = (proximo[0].id if isinstance(proximo[0], g.Branch)
               else proximo[0]["id"]) if proximo else fim_id
    atual = list(proximo) if proximo else [g.goto_step(fim_id)]
    for valor, pts in reversed(opcoes):
        sim = []
        if pts:
            sim.append(g.math_step(NOTA, "add", pts))
        sim.append(g.goto_step(destino))
        atual = [g.Branch("%s = %s?" % (rotulo, valor),
                          [g.cond("contact_detail", campo_id, "==", valor)],
                          sim=sim, nao=atual)]
    return atual


c = g.client()
orig = c.request("GET", "/workflow/" + g.LOC + "/" + ORIG)
tpl = cl.remapear(orig["workflowData"]["templates"])

# onde entrar: logo antes da nota 'Nota de qualificação'
alvo = None
for s in tpl:
    if (s["type"] == "add_notes"
            and (s.get("attributes") or {}).get("title") == "Nota de qualificação"):
        alvo = s
if not alvo:
    raise SystemExit("nao achei a nota 'Nota de qualificação' no original")
antes = [s for s in tpl if s.get("next") == alvo["id"]]
if not antes:
    raise SystemExit("nao achei quem aponta para a nota")
antes = antes[0]
print("insiro a régua entre '%s' e a nota" % antes.get("name"))

# monta de tras para frente: o ultimo campo salta para a nota
arvore = []
for rotulo, opcoes in reversed(REGUA):
    arvore = pontuar(rotulo, C[rotulo]["id"], opcoes, arvore, alvo["id"])

zera = g.field_step(NOTA, "Nota de qualificação", 0, "numerical")
regua = g.montar([zera] + arvore, parent=antes.get("parent"),
                 parent_key=antes["id"])
antes["next"] = zera["id"]
# a nota deixou de vir logo depois de `antes`: agora ela e alcancada pelos
# gotos da regua. O parentKey dela tem de apontar para um predecessor real,
# senao a publicacao recusa ("parentKey points to ...").
# no alcancado SO por goto nao tem pai na cadeia: goto nao pode ser pai
# ("parentKey points to ... (Go To)") e o antecessor antigo agora aponta
# para a regua.
alvo.pop("parentKey", None)
alvo.pop("parent", None)

novo = tpl + regua
gat = [{"status": "draft", "schedule_config": {}, "type": "appointment",
        "masterType": "highlevel", "name": "Status Do Agendamento",
        "active": True, "triggersChanged": True, "location_id": g.LOC,
        "conditions": (orig and [t for t in
                                 (c.request("GET", "/workflow/" + g.LOC
                                            + "/trigger?workflowId=" + ORIG) or [])
                                 if not t.get("deleted")][0]["conditions"])}]

ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
       if w.get("type") == "workflow"}
wf = ids.get(NOME) or g.create_workflow(c, NOME)
g.guard(wf)

for t in gat:
    body = dict(t, workflowId=wf, location_id=g.LOC,
                actions=[{"workflow_id": wf, "type": "add_to_workflow"}])
    ja = [x for x in (c.request("GET", "/workflow/" + g.LOC
                                + "/trigger?workflowId=" + wf) or [])
          if not x.get("deleted")]
    tid = ja[0]["id"] if ja else (c.request(
        "POST", "/workflow/" + g.LOC + "/trigger", body) or {}).get("id")
    if tid:
        c.request("PUT", "/workflow/" + g.LOC + "/trigger/" + tid,
                  dict(body, targetActionId=cl.raiz(tpl),
                       advanceCanvasMeta={"position": {"x": 57.5, "y": -73}}))

cur = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
r = c.request("PUT", "/workflow/" + g.LOC + "/" + wf,
              {"name": NOME, "status": "draft",
               "version": cur.get("version", 1) if isinstance(cur, dict) else 1,
               "allowMultiple": True, "stopOnResponse": False,
               "workflowData": {"templates": novo}})
if r and r.get("_error"):
    raise SystemExit("falhou: " + str(r.get("message"))[:200])

doc = g.export(c, wf, os.path.join(JSON_DIR, NOME + ".json"))
w = doc["workflow"]
t2 = (w.get("workflowData") or {}).get("templates") or []
vivos = {s["id"] for s in t2}
somas = [s for s in t2 if s["type"] == "math_operation"]
print("nos=%d (original %d + régua %d)" % (len(t2), len(tpl), len(regua)))
print("somas na régua: %d | pontos máximos: %d"
      % (len(somas), sum((s["attributes"]["operators"][0]["value"]) for s in somas)))
print("gotos quebrados:", sum(1 for s in t2 if s["type"] == "goto"
                              and (s.get("attributes") or {}).get("targetNodeId") not in vivos))
print("nasce RASCUNHO: trocar pelo publicado é decisão do dono")
