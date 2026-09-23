"""Inventario ao vivo (somente leitura) de todo workflow PUBLICADO.

Para cada workflow: gatilhos, e cada no que toca em etapa do funil, no
`Resultado da tentativa`, em tag de fila/estado, cria tarefa, manda mensagem
(SMS = WhatsApp pela Stevo; whatsapp = API oficial) ou mexe em outro workflow.
Redumpa o JSON de cada um em workflows-json/ e escreve INVENTARIO-WORKFLOWS.md.

Uso: python inventario.py
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

AQUI = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(AQUI, "campos.json"), encoding="utf-8"))
ID2CAMPO = {v["id"]: k for k, v in C.items()}
ETAPA = {v: k for k, v in g.STAGES.items()}
TAGS = {"fila-tel", "fila-wa", "fila-quente", "toque", "limpar-tarefas", "pausado",
        "conectado-hoje", "nutricao-90d", "nao-perturbe", "telefone-invalido",
        "cad-inbound", "cad-outbound", "reengajamento-ativo", "atraso-1a-tentativa"}
MSG = {"sms", "whatsapp", "send_whatsapp", "email", "send_email"}


def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def nomeia(v):
    if isinstance(v, list):
        return [nomeia(x) for x in v]
    if isinstance(v, str):
        return ETAPA.get(v, ID2CAMPO.get(v, v))
    return v


def achados(obj):
    s = json.dumps(obj, ensure_ascii=False)
    out = []
    for sid, nome in ETAPA.items():
        if sid in s:
            out.append("etapa:" + nome)
    for fid, nome in ID2CAMPO.items():
        if fid in s and nome in ("Resultado da tentativa", "Tentativa nº",
                                 "Canal que conectou", "Data de retorno",
                                 "Hora do retorno", "WA não atendidas seguidas",
                                 "Reunião foi qualificada", "Conexão real"):
            out.append("campo:" + nome)
    for t in TAGS:
        if '"' + t + '"' in s:
            out.append("tag:" + t)
    return out


def main():
    c = g.client()
    ws = [w for w in c.request("GET", "/workflow/" + g.LOC)
          if w.get("status") == "published"]
    nomes = {w["id"]: w.get("name") for w in c.request("GET", "/workflow/" + g.LOC)}
    linhas = ["# Inventário dos workflows publicados (ao vivo)", "",
              "Gerado por `tools/inventario.py`. Só leitura.", ""]
    for w in sorted(ws, key=lambda x: x.get("name", "")):
        doc = g.export(c, w["id"], os.path.join(AQUI, "..", "workflows-json",
                                                 w["name"] + ".json"))
        tpl = (doc["workflow"].get("workflowData") or {}).get("templates") or []
        linhas += ["## " + w["name"], "",
                   "`%s` · %d nós" % (w["id"], len(tpl)), ""]
        for t in doc["triggers"] if isinstance(doc["triggers"], list) else []:
            conds = "; ".join("%s %s %s" % (x.get("title") or x.get("field"),
                                              x.get("operator"),
                                              nomeia(x.get("value")))
                              for x in t.get("conditions") or [])
            linhas.append("- **Gatilho** `%s` (%s): %s" % (t.get("type"),
                          "ativo" if t.get("active") else "INATIVO", conds))
        for n in tpl:
            tipo = n.get("type")
            a = n.get("attributes") or {}
            info = achados(n) if tipo != "if_else" else achados(a)
            extra = ""
            if tipo == "task-notification":
                extra = "tarefa: " + (a.get("title") or "")
            elif tipo in MSG or (tipo == "internal_notification" and False):
                extra = "mensagem"
            elif tipo in ("remove_from_workflow", "add_to_workflow"):
                alvo = a.get("workflow_id")
                alvo = alvo if isinstance(alvo, list) else [alvo]
                extra = tipo + " → " + ", ".join(nomes.get(x, "?" + str(x)) for x in alvo)
            elif tipo in ("create_opportunity", "update_opportunity"):
                extra = "oportunidade"
            if info or extra:
                linhas.append("- `%s` %s — %s %s" % (tipo, (n.get("name") or "")[:40],
                              extra, " ".join(sorted(set(info)))))
        linhas.append("")
    p = os.path.join(AQUI, "..", "INVENTARIO-WORKFLOWS.md")
    open(p, "w", encoding="utf-8").write("\n".join(linhas))
    print("workflows publicados:", len(ws))
    print("escrito:", p)


if __name__ == "__main__":
    main()
