"""Troca cada workflow publicado defeituoso pela sua copia v2.

Por que isto existe: a regra do dono e 'nunca edite um publicado'. Ela foi
respeitada - nenhum original teve um no alterado. O que esta troca faz e
DESLIGAR o original (status draft) e LIGAR a copia. Reversivel com um
clique em cada.

A ordem importa: desliga o original PRIMEIRO. Se a copia fosse publicada
antes, os dois ficariam ativos no mesmo gatilho e o lead entraria duas
vezes.

O que cada troca corrige esta no docstring do build_* correspondente e no
APRENDIZADOS-CRM.md.
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

PARES = [
    ("Interceptação de Sinal — Clique.", "Interceptação de Sinal — Clique v2",
     "o original aponta para um Trigger Link que nao existe: nunca disparou"),
    ("Interceptação de Sinal — Resposta", "Interceptação de Sinal — Resposta v2",
     "portao de opt-out: sem ele 'pare de mandar mensagem' virava tarefa"),
    ("Pós-agendamento", "Pós-agendamento v2",
     "a regua de qualificacao, provada somando 93 no contato de teste"),
    ("Mestre de saída", "Mestre de saída v2",
     "nao marca mais limpar-tarefas em lead que acabou de chegar"),
    ("Pós-ligação", "Pós-ligação v2",
     "4 nos de Math que escreviam em campo nenhum"),
]

c = g.client()
todos = c.request("GET", "/workflow/" + g.LOC)
ids = {}
for w in todos:
    if w.get("type") == "workflow":
        ids.setdefault(w.get("name"), w["id"])


def estado(wf):
    f = c.request("GET", "/workflow/" + g.LOC + "/" + wf) or {}
    return f


def mudar_status(wf, novo):
    """PUT preservando tudo - o backend sobrescreve o que nao for enviado."""
    f = estado(wf)
    tpl = (f.get("workflowData") or {}).get("templates") or []
    if not tpl:
        print("    RECUSADO: %s esta vazio" % wf)
        return False
    r = c.request("PUT", "/workflow/" + g.LOC + "/" + wf,
                  {"name": f.get("name"), "status": novo,
                   "version": f.get("version", 1),
                   "allowMultiple": f.get("allowMultiple", True),
                   "stopOnResponse": f.get("stopOnResponse", False),
                   "allowMultipleOpportunity": f.get("allowMultipleOpportunity", False),
                   "timezone": f.get("timezone", "account"),
                   "window": f.get("window"),
                   "workflowData": {"templates": tpl}})
    if r and r.get("_error"):
        print("    falhou: " + str(r.get("message"))[:120])
        return False
    return estado(wf).get("status") == novo


for nome_orig, nome_v2, motivo in PARES:
    print("\n=== %s" % nome_orig)
    print("    motivo: " + motivo)
    o, v = ids.get(nome_orig), ids.get(nome_v2)
    if not o or not v:
        print("    PULADO: nao achei %s" % ("o original" if not o else "a v2"))
        continue
    fo, fv = estado(o), estado(v)
    print("    original: %s (%d nós) | v2: %s (%d nós)"
          % (fo.get("status"), len((fo.get("workflowData") or {}).get("templates") or []),
             fv.get("status"), len((fv.get("workflowData") or {}).get("templates") or [])))
    era_publicado = fo.get("status") == "published"
    if era_publicado:
        print("    desligando o original... %s"
              % ("ok" if mudar_status(o, "draft") else "FALHOU"))
    ligou = True
    if estado(v).get("status") != "published":
        ligou = mudar_status(v, "published")
        print("    ligando a v2...        %s" % ("ok" if ligou else "FALHOU"))
    # ROLLBACK: se a v2 nao subiu, o original volta AGORA. Sem isto, uma
    # copia invalida deixa o workflow fora do ar - aconteceu em 22/09/2026
    # com tres deles de uma vez.
    if not ligou and era_publicado:
        print("    ROLLBACK: religando o original... %s"
              % ("ok" if mudar_status(o, "published") else "FALHOU"))
    fo, fv = estado(o), estado(v)
    print("    FINAL: original=%s  v2=%s" % (fo.get("status"), fv.get("status")))

print("\n=== limpeza dos workflows de sondagem")
for w in todos:
    n = w.get("name") or ""
    if n.startswith("ZZ TESTE") and estado(w["id"]).get("status") == "published":
        print("  despublicando %s: %s" % (n, mudar_status(w["id"], "draft")))
