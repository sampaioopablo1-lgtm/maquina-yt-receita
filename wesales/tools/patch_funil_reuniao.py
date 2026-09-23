"""Ajuste cirurgico da mudanca de etapa (PLANO-MULTICANAL.md, D1-D4).

AGENDAR virou REUNIAO DE DIAGNOSTICO (mesmo id); CONECTAR vai ate a reuniao
marcada; o closer move para NEGOCIAR ao apresentar a proposta. Muda so
valores dentro dos workflows publicados: mesmo id de workflow, mesmos ids de
no, configuracoes preservadas (mesmo PUT do patch_relogio_cadencias.py).

Uso: python patch_funil_reuniao.py            -> so lista o que mudaria
     python patch_funil_reuniao.py --aplicar  -> backup + PUT + confere
"""
import copy
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g


def put(c, cur, templates):
    """Mesmo corpo do g.publicar (preserva allowMultiple etc.).

    **Levanta `RuntimeError` se a conta recusar o PUT.** Nao devolve erro em
    silencio, de proposito: em 23/09/2026 o `patch_portao_inbound.py` religou
    `parentKey` e esqueceu `next`, a conta respondeu 400, e como quem chamava
    esta funcao nao lia a resposta, o script seguiu adiante e imprimiu um
    resumo de sucesso. Nove dos dezessete pontos de chamada nao conferiam o
    retorno; conferir em cada um seria esquecer de novo no proximo patch, e
    quem esquece nao ve. Aqui ninguem esquece.

    Quem precisa seguir apesar da recusa (varredura de varios workflows, por
    exemplo) captura a excecao — mas ai a escolha esta escrita no codigo.
    """
    r = c.request("PUT", "/workflow/" + g.LOC + "/" + cur["id"],
                  {"name": cur.get("name"), "status": "published",
                   "version": cur.get("version", 1),
                   "allowMultiple": cur.get("allowMultiple", True),
                   "stopOnResponse": cur.get("stopOnResponse", False),
                   "allowMultipleOpportunity": cur.get("allowMultipleOpportunity", False),
                   "timezone": cur.get("timezone", "account"),
                   "window": cur.get("window"),
                   "workflowData": {"templates": templates}})
    if not isinstance(r, dict) or r.get("_error"):
        raise RuntimeError(
            "PUT RECUSADO pela conta em %r (%s nos enviados): %s"
            % (cur.get("name"), len(templates),
               json.dumps(r, ensure_ascii=False)[:400] if r is not None else "sem resposta"))
    return r

AQUI = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(AQUI, "..", "workflows-json", "_antes-patch-funil")
CONECTAR = g.STAGES["CONECTAR"]
REUNIAO = g.STAGES["REUNIÃO DE DIAGNÓSTICO"]
NEGOCIAR = g.STAGES["NEGOCIAR"]
INBOUND = "c2375e2f-b4cb-4947-8377-7c1e0529ba82"
REENG = "37eb32e4-4c21-4c69-bba1-36879ae0886c"


def troca_str(obj, velho, novo):
    """Troca uma string em todo o objeto (so valores). Devolve quantas."""
    n = 0
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and v == velho:
                obj[k] = novo
                n += 1
            else:
                n += troca_str(v, velho, novo)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str) and v == velho:
                obj[i] = novo
                n += 1
            else:
                n += troca_str(v, velho, novo)
    return n


def pos_agendamento(tpl, extra_remover):
    log = []
    for t in tpl:
        a = t.get("attributes") or {}
        if t["type"] == "create_opportunity":
            k = troca_str(t, NEGOCIAR, REUNIAO)
            if k:
                t["name"] = "Criar/Atualizar Oportunidade em REUNIÃO DE DIAGNÓSTICO"
                log.append("%s: reunião marcada → REUNIÃO DE DIAGNÓSTICO" % t["id"][:8])
        if t["type"] == "remove_from_workflow":
            alvo = a.get("workflow_id") or []
            falta = [x for x in [INBOUND, REENG] + extra_remover if x not in alvo]
            if falta:
                a["workflow_id"] = alvo + falta
                log.append("%s: também remove de %d cadência(s)" % (t["id"][:8], len(falta)))
    return log


def troca_etapa(nome_log):
    def f(tpl, _extra):
        log = []
        for t in tpl:
            k = troca_str(t, NEGOCIAR, REUNIAO)
            if k:
                if "NEGOCIAR" in (t.get("name") or ""):
                    t["name"] = t["name"].replace("NEGOCIAR", "REUNIÃO DE DIAGNÓSTICO")
                log.append("%s %s: NEGOCIAR → REUNIÃO (%d)" % (t["id"][:8], t["type"], k))
        return log
    return f


def pos_ligacao(tpl, _extra):
    log = []
    for t in tpl:
        a = t.get("attributes") or {}
        if t["type"] == "create_opportunity" and troca_str(t, REUNIAO, CONECTAR):
            log.append("%s: Atendeu não move mais de etapa (fica em CONECTAR)" % t["id"][:8])
        if t["type"] == "task-notification" and (a.get("title") or "").startswith("[CONECTADO]"):
            a["title"] = "[FECHAR HORÁRIO] Qualificar e agendar a reunião de diagnóstico"
            log.append("%s: tarefa [CONECTADO] → [FECHAR HORÁRIO]" % t["id"][:8])
        if t["type"] == "add_contact_tag" and "conectado-hoje" in (a.get("tags") or []) \
                and "fechar-horario" not in a["tags"]:
            a["tags"] = a["tags"] + ["fechar-horario"]
            log.append("%s: + tag fechar-horario" % t["id"][:8])
    return log


ALVOS = [
    ("Pós-agendamento v2", pos_agendamento),
    ("Loop do closer v2", troca_etapa("closer")),
    ("Recuperação de No-show", troca_etapa("no-show")),
    ("SLA do Closer — No-show", troca_etapa("sla")),
    ("Pós-ligação v2", pos_ligacao),
]


def main():
    aplicar = "--aplicar" in sys.argv
    extra = [x for x in sys.argv[1:] if len(x) == 36]     # ids extras a remover (Fechar Horário)
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    os.makedirs(BACKUP, exist_ok=True)
    for nome, fn in ALVOS:
        wf = ids[nome]
        cur = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
        tpl = (cur.get("workflowData") or {}).get("templates") or []
        novos = copy.deepcopy(tpl)
        log = fn(novos, extra)
        print("== %s (%s) status=%s nós=%d mudanças=%d" % (nome, wf[:8], cur.get("status"),
                                                          len(tpl), len(log)))
        for l in log:
            print("   " + l)
        if not aplicar or not log:
            continue
        g.export(c, wf, os.path.join(BACKUP, nome + ".json"))
        r = put(c, cur, novos)
        if r and r.get("_error"):
            print("   FALHA no PUT: " + str(r.get("message"))[:200])
            continue
        volta = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
        vt = (volta.get("workflowData") or {}).get("templates") or []
        resto = fn(copy.deepcopy(vt), extra)
        tr = c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + wf)
        print("   conferido: status=%s nós=%d ids iguais=%s pendências=%d allowMultiple=%s→%s gatilhos=%s"
              % (volta.get("status"), len(vt), [t["id"] for t in vt] == [t["id"] for t in tpl],
                 len(resto), cur.get("allowMultiple"), volta.get("allowMultiple"),
                 [t.get("active") for t in tr if not t.get("deleted")]))
        g.export(c, wf, os.path.join(AQUI, "..", "workflows-json", nome + ".json"))


if __name__ == "__main__":
    main()
