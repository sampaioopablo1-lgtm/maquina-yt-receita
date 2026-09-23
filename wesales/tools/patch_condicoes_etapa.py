"""Troca condicao de OPORTUNIDADE por condicao de TAG de estado (Espelho de Etapa).

Em workflow cujo gatilho nao e de oportunidade (tag, contato, resposta, link,
agendamento), "Pipeline stage is X" le vazio e da sempre falso (registro de
execucao, 23/09/2026). O `Espelho de Etapa` mantem no contato a tag do estado;
aqui cada segmento de If/Else com condicao de oportunidade troca essas
condicoes por UMA condicao de tag equivalente. Demais condicoes ficam.

  etapa == CONECTAR (+ status open)              -> tag etapa-conectar
  etapa == REUNIAO DE DIAGNOSTICO (+ status open) -> tag etapa-reuniao
  status == abandoned                             -> tag status-nutricao

Nao mexe na `Cadência 12x30` (parte 1): gatilho de etapa, e ali a condicao
funciona e evita corrida com o Espelho no instante da entrada.

Uso: python patch_condicoes_etapa.py [--aplicar]
"""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_funil_reuniao import put, g        # put preserva configuracoes

ALVOS = ["CONECTAR Estagnado", "Cadência 12x30 — parte 2", "Fechar Horário",
         "Interceptação de Sinal — Clique v2", "Interceptação de Sinal — Resposta v2",
         "Opt-out por Palavra-chave", "Recuperação de No-show", "Reengajamento 90 dias",
         "Retorno Vencido", "SLA do Closer — No-show"]
CONECTAR, REUNIAO = g.STAGES["CONECTAR"], g.STAGES["REUNIÃO DE DIAGNÓSTICO"]
BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "workflows-json",
                      "_antes-patch-condicoes")


def tag_equivalente(opp):
    etapas = {x["conditionValue"] for x in opp if x["conditionSubType"] == "pipelineStageId"
              and x["conditionOperator"] == "=="}
    status = {x["conditionValue"] for x in opp if x["conditionSubType"] == "status"
              and x["conditionOperator"] == "=="}
    if etapas == {CONECTAR} and status <= {"open"}:
        return "etapa-conectar"
    if etapas == {REUNIAO} and status <= {"open"}:
        return "etapa-reuniao"
    if not etapas and status == {"abandoned"}:
        return "status-nutricao"
    return None


def corrigir(tpl):
    log, falhas = [], []
    for t in tpl:
        if t.get("type") != "if_else":
            continue
        for b in (t.get("attributes") or {}).get("branches") or []:
            for sg in b.get("segments") or []:
                cs = sg.get("conditions") or []
                opp = [x for x in cs if x.get("conditionType") == "opportunities"]
                if not opp:
                    continue
                tag = tag_equivalente(opp)
                if not tag:
                    falhas.append("%s: padrão desconhecido %s" % (t["id"][:8], [(x["conditionSubType"], x["conditionValue"]) for x in opp]))
                    continue
                if sg.get("operator", "and") != "and" and len(cs) > len(opp):
                    falhas.append("%s: segmento OR misto — não troco" % t["id"][:8])
                    continue
                novo = g.cond("contact_detail", "tags", "index-of-true", [tag])
                novo["ifElseNodeId"] = opp[0].get("ifElseNodeId", "")
                i = cs.index(opp[0])
                sg["conditions"] = [x for x in cs[:i] if x not in opp] + [novo] + \
                                   [x for x in cs[i:] if x not in opp]
                log.append("%s %s: %d condição(ões) de oportunidade → tag %s"
                           % (t["id"][:8], (t.get("name") or "")[:34], len(opp), tag))
    return log, falhas


def reengajamento_sincrono(tpl):
    """O Reengajamento reabre a oportunidade e testa a etapa no no seguinte:
    o Espelho (assincrono) pode chegar depois. Os nos de tag que ja existem
    antes do TR1 passam a gravar o estado na hora."""
    log = []
    for t in tpl:
        a = t.get("attributes") or {}
        tags = a.get("tags") or []
        if t["type"] == "add_contact_tag" and tags == ["reengajamento-ativo"]:
            a["tags"] = tags + ["etapa-conectar"]
            log.append("%s: + tag etapa-conectar junto com reengajamento-ativo" % t["id"][:8])
        if t["type"] == "remove_contact_tag" and tags == ["nutricao-90d"]:
            a["tags"] = tags + ["status-nutricao"]
            log.append("%s: tira status-nutricao junto com nutricao-90d" % t["id"][:8])
    return log


def main():
    aplicar = "--aplicar" in sys.argv
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    os.makedirs(BACKUP, exist_ok=True)
    for nome in ALVOS:
        wf = ids[nome]
        cur = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
        tpl = copy.deepcopy((cur.get("workflowData") or {}).get("templates") or [])
        log, falhas = corrigir(tpl)
        if nome == "Reengajamento 90 dias":
            log += reengajamento_sincrono(tpl)
        print("== %s: %d troca(s)%s" % (nome, len(log), " — %d FALHA(S)" % len(falhas) if falhas else ""))
        for l in log + falhas:
            print("   " + l)
        if not aplicar or not log or falhas:
            continue
        g.export(c, wf, os.path.join(BACKUP, nome + ".json"))
        put(c, cur, tpl)
        v = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
        vt = v["workflowData"]["templates"]
        resto, _ = corrigir(copy.deepcopy(vt))
        trs = [t.get("active") for t in c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + wf)
               if not t.get("deleted")]
        print("   conferido: status=%s nós=%d ids iguais=%s restantes=%d gatilhos=%s"
              % (v.get("status"), len(vt), [x["id"] for x in vt] == [x["id"] for x in tpl],
                 len(resto), trs))
        g.export(c, wf, os.path.join(BACKUP, "..", nome + ".json"))


if __name__ == "__main__":
    main()
