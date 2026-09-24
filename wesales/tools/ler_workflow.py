"""Transforma cada workflow PUBLICADO em um roteiro legível (somente leitura).

Para auditoria humana: árvore de condições (com nomes de campo/etapa em vez de
ids), esperas, textos exatos de mensagem/tarefa/nota/notificação, tags, gotos,
janela e gatilhos. Grava `wesales/auditoria-roteiros/<nome>.txt`.

Uso: python ler_workflow.py [trecho-do-nome]
"""
import io, json, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "..", "auditoria-roteiros")
ETAPAS = {v: k for k, v in g.STAGES.items()}


def limpa(s):
    s = re.sub(r"<br\s*/?>|</p>", "\n", s or "")
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def nome_campo(cid, campos):
    return campos.get(cid, cid)


def cond_txt(c, campos):
    sub, op, val = c.get("conditionSubType"), c.get("conditionOperator"), c.get("conditionValue")
    if sub == "pipelineStageId":
        val = ETAPAS.get(val, val)
    return "%s %s %s" % (nome_campo(sub, campos), op, json.dumps(val, ensure_ascii=False) if val is not None else "")


def resumo(t, campos, workflows):
    a = t.get("attributes") or {}
    ty = t["type"]
    if ty == "wait":
        if a.get("type") == "appointment":
            s = a.get("appointmentStartAfter") or {}
            return "ESPERA até %s %s %s da reunião (%s)" % (s.get("value"), s.get("type"), s.get("when"), a.get("appointmentCondition"))
        s = a.get("startAfter") or {}
        if s:
            return "ESPERA %s %s" % (s.get("value"), s.get("type"))
        return "ESPERA " + json.dumps({k: v for k, v in a.items() if k not in ("transitions", "cat")}, ensure_ascii=False)[:160]
    if ty == "sms":
        return "WHATSAPP → lead:\n" + "\n".join("        │ " + l for l in limpa(a.get("body")).split("\n"))
    if ty == "email":
        return "E-MAIL → lead | assunto: %s\n%s" % (a.get("subject"), "\n".join("        │ " + l for l in limpa(a.get("html")).split("\n")))
    if ty == "task-notification":
        return "TAREFA: %s | %s | vence: %s" % (a.get("title"), limpa(a.get("body") or a.get("description") or "")[:200], a.get("dueDate") or a.get("due") or json.dumps({k: a[k] for k in a if "due" in k.lower()}, ensure_ascii=False))
    if ty in ("add_contact_tag", "remove_contact_tag"):
        return ("+TAG " if ty.startswith("add") else "-TAG ") + ", ".join(a.get("tags") or [])
    if ty == "add_notes":
        return "NOTA: " + limpa(a.get("html") or a.get("body"))[:300].replace("\n", " / ")
    if ty == "internal_notification":
        k = a.get("type")
        corpo = (a.get(k) or {}) if isinstance(a.get(k), dict) else {}
        corpo = corpo or (a.get("notification") or {})
        return "AVISO INTERNO (%s): %s" % (k, limpa(corpo.get("body") or corpo.get("html") or "")[:300].replace("\n", " / "))
    if ty == "update_contact_field":
        return "CAMPO: " + "; ".join("%s = %s" % (f.get("title") or nome_campo(f.get("field"), campos), f.get("value")) for f in a.get("fields") or [])
    if ty == "create_opportunity":
        return "OPORTUNIDADE → etapa %s, status %s" % (ETAPAS.get(a.get("pipeline_stage_id"), a.get("pipeline_stage_id")), a.get("opportunity_status") or "(mantém)")
    if ty == "remove_from_workflow":
        ids = a.get("workflow_id") or []
        return "TIRA DE: " + ", ".join(workflows.get(i, i[:8] + "(?)") for i in (ids if isinstance(ids, list) else [ids]))
    if ty == "add_to_workflow":
        return "PÕE EM: " + str(workflows.get(a.get("workflow_id"), a.get("workflow_id")))
    if ty == "goto":
        return "VAI PARA → %s" % a.get("targetNodeId", "")[:8]
    if ty == "math_operation":
        return "CONTA: " + json.dumps({k: a[k] for k in a if k not in ("type",)}, ensure_ascii=False)[:160]
    if ty == "dnd_contact":
        return "DND " + json.dumps(a, ensure_ascii=False)[:120]
    if ty == "assign_user":
        return "ATRIBUI dono " + json.dumps(a, ensure_ascii=False)[:120]
    return ty.upper() + " " + json.dumps(a, ensure_ascii=False)[:160]


def arvore(tpl, campos, workflows):
    by = {t["id"]: t for t in tpl}
    filhos = {}
    for t in tpl:
        filhos.setdefault(t.get("parentKey"), []).append(t)
    linhas, vistos = [], set()

    def anda(no, ind):
        while no and no["id"] not in vistos:
            vistos.add(no["id"])
            a = no.get("attributes") or {}
            pre = "  " * ind + "[%s] " % no["id"][:8]
            if no["type"] == "if_else" and a.get("branches"):
                segs = a["branches"][0]["segments"][0]
                conds = (" %s " % segs["operator"].upper()).join(cond_txt(c, campos) for c in segs["conditions"])
                linhas.append(pre + "SE «%s»: %s" % (no.get("name"), conds))
                nx = no.get("next") or []
                for rot, alvo in zip(("SIM", "NÃO"), nx):
                    linhas.append("  " * (ind + 1) + rot + ":")
                    b = by.get(alvo)
                    anda(by.get(b.get("next")) if b and b.get("next") else None, ind + 2)
                return
            if no["type"] == "transition":
                linhas.append(pre + "RAMO «%s»" % no.get("name"))
            elif no["type"] == "find_opportunity":
                linhas.append(pre + "ACHA OPORTUNIDADE «%s»" % no.get("name"))
            else:
                linhas.append(pre + "%s  «%s»" % (resumo(no, campos, workflows), no.get("name")) if no["type"] not in ("sms", "email") else pre + resumo(no, campos, workflows))
            nx = no.get("next")
            if isinstance(nx, list):            # nó com ramos (transições)
                for alvo in nx:
                    anda(by.get(alvo), ind + 1)
                return
            no = by.get(nx) if isinstance(nx, str) else None
    raiz = [t for t in tpl if not t.get("parentKey")]
    for r in raiz:
        anda(r, 0)
    return linhas


def main():
    filtro = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    c = g.client()
    ws = c.request("GET", "/workflow/" + g.LOC)
    workflows = {w["id"]: "%s[%s]" % (w["name"], w.get("status")) for w in ws}
    campos = {}
    try:
        for f in json.load(open(os.path.join(AQUI, "..", "workflows-json", "_campos.json"), encoding="utf-8")):
            campos[f["id"]] = f["name"]
    except Exception:
        pass
    os.makedirs(SAIDA, exist_ok=True)
    for w in ws:
        if w.get("status") != "published" or filtro not in w["name"].lower():
            continue
        v = c.request("GET", "/workflow/" + g.LOC + "/" + w["id"])
        tpl = (v.get("workflowData") or {}).get("templates") or []
        trs = [t for t in c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + w["id"]) or [] if not t.get("deleted")]
        cab = ["# %s  (%s, %d nós)" % (w["name"], w["id"], len(tpl)),
               "janela: %s" % json.dumps(v.get("window"), ensure_ascii=False),
               "reentrada: %s | para ao responder: %s" % (v.get("allowMultiple"), v.get("stopOnResponse"))]
        for t in trs:
            cab.append("GATILHO %s (ativo=%s): %s" % (t.get("type"), t.get("active"), "; ".join(
                "%s %s %s" % (x.get("field"), x.get("operator"), ETAPAS.get(x.get("value"), x.get("value")) if isinstance(x.get("value"), str) else x.get("value")) for x in t.get("conditions") or [])))
        txt = "\n".join(cab + [""] + arvore(tpl, campos, workflows)) + "\n"
        with open(os.path.join(SAIDA, re.sub(r'[\\/:*?"<>|]', "-", w["name"]) + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(txt)
        print("%-50s %4d nós  %6d chars" % (w["name"][:50], len(tpl), len(txt)))


if __name__ == "__main__":
    main()
