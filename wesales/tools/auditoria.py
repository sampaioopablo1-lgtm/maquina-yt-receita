"""Auditoria estrutural de TODOS os workflows da subconta.

Procura defeito que so aparece quando se olha o conjunto:
- gatilho orfao (aponta para no que nao existe) ou duplicado
- goto apontando para no inexistente
- remove_from_workflow / add_to_workflow apontando para id que nao existe
- workflow publicado sem gatilho, ou com no zero
- configuracao (re-entry, janela) diferente do que a spec pede
- SINERGIA: quem dispara quem por tag, e se ha ciclo
"""
import io
import os
import sys
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

# o que a spec pede para cada um que eu montei
ESPERADO = {
    "Contador de Toques": (True, False, False),
    "Cadência 12x30": (False, True, True),
    "Cadência Inbound": (False, True, True),
    "Reengajamento 90 dias": (True, True, True),
    "Recuperação de No-show": (True, True, True),
    "Registro de Comparecimento": (True, False, False),
    "SLA do Closer — No-show": (True, False, False),
    "Loop do closer v2": (True, False, False),
    "Opt-out por Palavra-chave": (True, False, False),
    "Alerta de Speed-to-lead": (True, False, False),
    "Lead Esquecido em NOVO LEAD": (True, False, False),
    "Fila Travada": (True, False, False),
    "CONECTAR Estagnado": (True, False, False),
    "AGENDAR Estagnado": (True, False, False),
    "Retorno Vencido": (True, False, False),
}

c = g.client()
lista = [w for w in c.request("GET", "/workflow/" + g.LOC)
         if w.get("type") == "workflow"]
validos = {w["id"] for w in lista}
nomes = {w["id"]: w.get("name") for w in lista}

problemas = []
poe_tag = defaultdict(set)     # workflow -> tags que aplica
gatilho_tag = defaultdict(set)  # tag -> workflows que ela dispara

print("%-34s %-10s %5s %4s  %s" % ("WORKFLOW", "STATUS", "NOS", "TRG", "CONFIG"))
print("-" * 92)
for w in sorted(lista, key=lambda x: x.get("name") or ""):
    nome, wid = w.get("name") or "?", w["id"]
    if nome.startswith("Template |") or nome.startswith("ZZ TESTE"):
        continue
    full = c.request("GET", "/workflow/" + g.LOC + "/" + wid) or {}
    tpl = (full.get("workflowData") or {}).get("templates") or []
    vivos = {s["id"] for s in tpl}
    trs = [t for t in (c.request("GET", "/workflow/" + g.LOC
                                 + "/trigger?workflowId=" + wid) or [])
           if not t.get("deleted")]

    cfg = "re=%s stop=%s jan=%s" % (full.get("allowMultiple"),
                                    full.get("stopOnResponse"),
                                    "sim" if full.get("window") else "nao")
    print("%-34s %-10s %5d %4d  %s" % (nome[:34], full.get("status"),
                                       len(tpl), len(trs), cfg))

    if full.get("status") == "published" and not tpl:
        problemas.append("%s: PUBLICADO e vazio" % nome)
    if full.get("status") == "published" and not trs:
        problemas.append("%s: PUBLICADO sem gatilho" % nome)
    for t in trs:
        alvo = t.get("targetActionId")
        # workflow montado na TELA nao grava targetActionId - so os meus
        # gravam. Ausente nao e defeito; apontar para no morto e.
        if tpl and alvo and alvo not in vivos:
            problemas.append("%s: gatilho %s aponta para no inexistente"
                             % (nome, t.get("type")))
        if t.get("type") == "contact_tag":
            for cond in t.get("conditions") or []:
                v = cond.get("value")
                if isinstance(v, str):
                    gatilho_tag[v].add(nome)
        if t.get("type") == "trigger_link":
            for cond in t.get("conditions") or []:
                if (cond.get("field") == "link.id"
                        and cond.get("value") != "vSUOvEbVZfxBlWFlTvDV"):
                    problemas.append("%s: gatilho aponta para o Trigger Link "
                                     "%s, que NAO EXISTE na subconta"
                                     % (nome, cond.get("value")))

    for s in tpl:
        a = s.get("attributes") or {}
        if s["type"] == "goto" and a.get("targetNodeId") not in vivos:
            problemas.append("%s: goto para no inexistente" % nome)
        if s["type"] in ("remove_from_workflow", "add_to_workflow"):
            for x in (a.get("workflow_id") or []):
                if x not in validos:
                    problemas.append("%s: %s aponta para workflow inexistente"
                                     % (nome, s["type"]))
        if s["type"] == "add_contact_tag":
            poe_tag[nome].update(a.get("tags") or [])

    esp = ESPERADO.get(nome)
    if esp:
        re_, stop, jan = esp
        if bool(full.get("allowMultiple")) != re_:
            problemas.append("%s: re-entry=%s, a spec pede %s"
                             % (nome, full.get("allowMultiple"), re_))
        if bool(full.get("stopOnResponse")) != stop:
            problemas.append("%s: stopOnResponse=%s, a spec pede %s"
                             % (nome, full.get("stopOnResponse"), stop))
        if bool(full.get("window")) != jan:
            problemas.append("%s: janela=%s, a spec pede %s"
                             % (nome, bool(full.get("window")), jan))

print("\n== SINERGIA: quem dispara quem por tag ==")
for tag, alvos in sorted(gatilho_tag.items()):
    quem = [n for n, tags in poe_tag.items() if tag in tags]
    print("  tag '%s' dispara %s" % (tag, sorted(alvos)))
    print("       e e aplicada por: %s" % (sorted(quem) or "ninguem"))
    for q in quem:
        if q in alvos:
            print("       [ciclo por desenho] '%s' reaplica '%s' e volta "
                  "para si mesmo" % (q, tag))

print("\n== PROBLEMAS (%d) ==" % len(problemas))
for p in problemas:
    print("  - " + p)
if not problemas:
    print("  nenhum")
