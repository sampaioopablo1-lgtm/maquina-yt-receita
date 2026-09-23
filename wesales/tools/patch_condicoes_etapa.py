"""Troca condicao de OPORTUNIDADE por condicao de TAG de estado (Espelho de Etapa).

Em workflow cujo gatilho nao e de oportunidade (tag, contato, resposta, link,
agendamento), "Pipeline stage is X" le vazio e da sempre falso (registro de
execucao, 23/09/2026). O `Espelho de Etapa` mantem no contato a tag do estado;
aqui cada segmento de If/Else com condicao de oportunidade troca essas
condicoes por UMA condicao de tag equivalente. Demais condicoes ficam.

  etapa == NOVO LEAD              (+ status open) -> tag etapa-novo-lead
  etapa == CONECTAR               (+ status open) -> tag etapa-conectar
  etapa == REUNIAO DE DIAGNOSTICO (+ status open) -> tag etapa-reuniao
  etapa == NEGOCIAR               (+ status open) -> tag etapa-negociar
  etapa == FORMALIZAR             (+ status open) -> tag etapa-formalizar
  status == abandoned                             -> tag status-nutricao
  status == lost                                  -> tag status-perdido
  status == won                                   -> tag status-ganho

As oito tags ja existem e estao publicadas — o dono as criou no commit
`61eb167`, e o `Espelho de Etapa` (publicado, v4) e quem as mantem. Este
script nao cria tag nenhuma, so passa a saber traduzir para as cinco que a
tabela antiga nao cobria (NOVO LEAD, NEGOCIAR, FORMALIZAR, perdido, ganho).
A tabela incompleta nunca traduziu errado: padrao que ela nao conhecia caia
em `falhas`, e `falhas` bloqueia o PUT. Era limite para o futuro, nao bug.

ALVOS deixou de ser lista fixa (23/09/2026). A lista tinha os 10 nomes da
rodada em que o defeito foi descoberto, e os 10 ja estao consertados — 49
condicoes trocadas, medido nos backups de `_antes-patch-condicoes/`. O
problema da lista fixa nao era o passado: era o futuro. Workflow criado
depois, com gatilho de tag e condicao de etapa, nasce com o mesmo defeito
silencioso e a lista nao o ve. Agora o alvo e varrido ao vivo: workflow
publicado que tenha QUALQUER gatilho sem oportunidade e ao menos uma
condicao de oportunidade em `if_else`.

A deteccao tambem roda sem API e sem PC, pelos dumps: veja
`auditoria_condicoes.py` (somente leitura, sai 1 se achar em publicado).

Nao mexe na `Cadência 12x30` (parte 1), e a varredura respeita isso: gatilho
de etapa, ali a condicao funciona e a troca criaria corrida com o Espelho no
instante da entrada. Decisao registrada em 23/09/2026 — a varredura nao a
reverte calada.

Uso: python patch_condicoes_etapa.py [--aplicar] [--incluir-teste] [--alvo NOME]
     sem `--aplicar` so imprime o que faria.
"""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_funil_reuniao import put, g        # put preserva configuracoes

# Gatilhos que entregam a oportunidade no contexto de execucao. Qualquer outro
# nao entrega, e la a condicao de oportunidade le vazio e da sempre falso.
GATILHO_COM_OPORTUNIDADE = {"pipeline_stage_updated", "opportunity_status_changed"}

# Decisao de 23/09/2026 que a varredura NAO reverte: ver docstring.
NUNCA = {"Cadência 12x30"}

ETAPA_TAG = {
    g.STAGES["NOVO LEAD"]: "etapa-novo-lead",
    g.STAGES["CONECTAR"]: "etapa-conectar",
    g.STAGES["REUNIÃO DE DIAGNÓSTICO"]: "etapa-reuniao",
    g.STAGES["NEGOCIAR"]: "etapa-negociar",
    g.STAGES["FORMALIZAR"]: "etapa-formalizar",
}
STATUS_TAG = {"abandoned": "status-nutricao", "lost": "status-perdido",
              "won": "status-ganho"}
BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "workflows-json",
                      "_antes-patch-condicoes")


def tag_equivalente(opp):
    etapas = {x["conditionValue"] for x in opp if x["conditionSubType"] == "pipelineStageId"
              and x["conditionOperator"] == "=="}
    status = {x["conditionValue"] for x in opp if x["conditionSubType"] == "status"
              and x["conditionOperator"] == "=="}
    if len(etapas) == 1 and status <= {"open"}:
        return ETAPA_TAG.get(next(iter(etapas)))
    if not etapas and len(status) == 1:
        return STATUS_TAG.get(next(iter(status)))
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


def tem_condicao_de_oportunidade(tpl):
    for t in tpl:
        if t.get("type") != "if_else":
            continue
        for b in (t.get("attributes") or {}).get("branches") or []:
            for sg in b.get("segments") or []:
                if any(x.get("conditionType") == "opportunities"
                       for x in (sg.get("conditions") or [])):
                    return True
    return False


def varre(c, incluir_teste=False, so=None):
    """[(nome, id)] dos workflows que tem o defeito, lidos ao vivo.

    Defeito = ao menos um gatilho que NAO entrega oportunidade, e ao menos uma
    condicao de oportunidade em `if_else`. Rascunho e `ZZ TESTE*` ficam de fora
    por padrao: rascunho nao roda, e copia de teste existe para exibir o
    defeito — `--incluir-teste` traz os dois.
    """
    alvos, pulados = [], []
    for w in c.request("GET", "/workflow/" + g.LOC):
        nome, wf = w.get("name"), w.get("id")
        if not wf or not nome:
            continue
        if so and nome != so:
            continue
        if nome in NUNCA:
            pulados.append((nome, "decisao registrada (NUNCA)"))
            continue
        if not incluir_teste and (w.get("status") != "published"
                                  or nome.startswith("ZZ TESTE")):
            continue
        gatilhos = {t.get("type") for t in
                    c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + wf)
                    if not t.get("deleted")}
        if gatilhos and gatilhos <= GATILHO_COM_OPORTUNIDADE:
            continue
        cur = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
        if tem_condicao_de_oportunidade((cur.get("workflowData") or {}).get("templates") or []):
            alvos.append((nome, wf, sorted(gatilhos)))
    for nome, porque in pulados:
        print("-- pulado: %s (%s)" % (nome, porque))
    return alvos


def main():
    aplicar = "--aplicar" in sys.argv
    incluir_teste = "--incluir-teste" in sys.argv
    so = None
    if "--alvo" in sys.argv:
        so = sys.argv[sys.argv.index("--alvo") + 1]
    c = g.client()
    os.makedirs(BACKUP, exist_ok=True)
    alvos = varre(c, incluir_teste, so)
    if not alvos:
        print("nenhum workflow com condicao de oportunidade sem gatilho que a carregue.")
        print("(os 10 da rodada de 23/09/2026 ja estao consertados — 49 condicoes trocadas)")
        return
    print("%d workflow(s) com o defeito:\n" % len(alvos))
    for nome, wf, gatilhos in alvos:
        print("== %s  gatilho: %s" % (nome, ", ".join(gatilhos) or "nenhum"))
        cur = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
        tpl = copy.deepcopy((cur.get("workflowData") or {}).get("templates") or [])
        log, falhas = corrigir(tpl)
        if nome == "Reengajamento 90 dias":
            log += reengajamento_sincrono(tpl)
        print("   %d troca(s)%s" % (len(log), " — %d FALHA(S)" % len(falhas) if falhas else ""))
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
