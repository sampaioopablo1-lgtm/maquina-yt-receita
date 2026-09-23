#!/usr/bin/env python3
"""Condicao de OPORTUNIDADE em workflow que o gatilho nao carrega (somente leitura).

O defeito que esta auditoria vigia foi medido no registro de execucao da
`ZZ TESTE 12X30` em 23/09/2026: em workflow cujo gatilho NAO e de oportunidade
(tag, contato, resposta, link, agendamento, agenda), a condicao
"Pipeline stage is X" le vazio e da **sempre falso**. Nao da erro, nao aparece
em lugar nenhum — o ramo simplesmente nunca roda. Foi por isso que nasceu o
`Espelho de Etapa`, que mantem a etapa/status da oportunidade como tag no
contato, e o `patch_condicoes_etapa.py`, que trocou 49 condicoes em 10
workflows.

Por que uma auditoria e nao so o patch: o patch tinha uma lista fixa de 10
nomes. Workflow criado depois, com gatilho de tag e condicao de etapa, nasce
com o mesmo defeito e a lista nao o ve. O defeito e silencioso por natureza —
so um varredor pega.

Gatilho que CARREGA oportunidade (condicao funciona, esta certo estar ali):
`pipeline_stage_updated`, `opportunity_status_changed`. Qualquer outro nao
carrega.

Achado em workflow `published` e falha (codigo 1). Em `draft` e em `ZZ TESTE*`
e aviso: rascunho nao roda, e copia de teste existe justamente para exibir o
defeito. Auditoria que grita sobre o que e intencional treina a gente a
ignorar auditoria.

Limite honesto: le os dumps de `wesales/workflows-json/`, fotografia que pode
estar defasada — o aviso de frescor do `_frescor.py` diz quais. Estes dumps
CARREGAM os gatilhos (o `g.export` grava `{"workflow": ..., "triggers": ...}`),
entao a classificacao de gatilho aqui nao e chute; mas gatilho mexido na tela
depois do dump so aparece no proximo export.

Uso:  python3 wesales/tools/auditoria_condicoes.py
Sai com codigo 1 se algum workflow PUBLICADO tiver o defeito.
"""
import glob
import json
import os
import sys

from _frescor import aviso

AQUI = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(AQUI, "..", "workflows-json")

# Gatilhos que entregam a oportunidade no contexto de execucao.
GATILHO_COM_OPORTUNIDADE = {"pipeline_stage_updated", "opportunity_status_changed"}

# id -> nome legivel, para o achado dizer QUAL etapa o ramo testa.
ETAPAS = {
    "7ae9c950-9bcf-4e60-8bc5-cb7388c87b7d": "NOVO LEAD",
    "deb60542-a5cd-43ae-b875-b467b120a72c": "CONECTAR",
    "3d26fcd1-220d-49ed-8325-705dfe9055b1": "REUNIÃO DE DIAGNÓSTICO",
    "cbcf0229-5e19-4fdb-8c50-6c641b78b3bb": "NEGOCIAR",
    "b8485ec0-98e8-459f-b990-f40a5e3bd25b": "FORMALIZAR",
}


def carrega():
    """[(nome, status, {tipos de gatilho}, [(no, [(subtipo, valor)])])] por dump."""
    saida = []
    for caminho in sorted(glob.glob(os.path.join(DUMPS, "*.json"))):
        try:
            with open(caminho, encoding="utf-8") as fh:
                dado = json.load(fh)
        except (ValueError, OSError):
            continue
        wf = dado.get("workflow") or {}
        if not wf.get("id"):
            continue
        nome = wf.get("name") or os.path.basename(caminho)[:-5]
        gatilhos = {t.get("type") for t in (dado.get("triggers") or [])
                    if not t.get("deleted")}
        segmentos = []
        for t in (wf.get("workflowData") or {}).get("templates") or []:
            if t.get("type") != "if_else":
                continue
            for b in (t.get("attributes") or {}).get("branches") or []:
                for sg in b.get("segments") or []:
                    opp = [x for x in (sg.get("conditions") or [])
                           if x.get("conditionType") == "opportunities"]
                    if opp:
                        segmentos.append((t["id"][:8], [
                            (x.get("conditionSubType"),
                             ETAPAS.get(x.get("conditionValue"), str(x.get("conditionValue"))))
                            for x in opp]))
        saida.append((nome, wf.get("status"), gatilhos, segmentos))
    return saida


def main():
    aviso(DUMPS)
    tudo = carrega()
    if not tudo:
        print("nenhum dump encontrado em %s" % DUMPS)
        return 0

    com_condicao = [x for x in tudo if x[3]]
    print("%d workflows com dump; %d testam condicao de oportunidade em if_else\n"
          % (len(tudo), len(com_condicao)))

    graves, avisos, corretos = [], [], []
    for nome, status, gatilhos, segmentos in com_condicao:
        # Sem gatilho nenhum no dump: nao da para classificar, entra como aviso.
        if gatilhos and gatilhos <= GATILHO_COM_OPORTUNIDADE:
            corretos.append((nome, status, gatilhos, segmentos))
        elif status == "published" and not nome.startswith("ZZ TESTE"):
            graves.append((nome, status, gatilhos, segmentos))
        else:
            avisos.append((nome, status, gatilhos, segmentos))

    print("DEFEITO EM WORKFLOW PUBLICADO — o ramo nunca roda e ninguem avisa")
    if not graves:
        print("  nenhum (no que os dumps mostram)\n")
    for nome, status, gatilhos, segmentos in graves:
        print("  %s  [%s]  gatilho: %s" % (nome, status, ", ".join(sorted(gatilhos)) or "nenhum"))
        for no, conds in segmentos:
            print("      no %s  %s" % (no, conds))
        print("      conserto: `patch_condicoes_etapa.py` troca por tag do Espelho de Etapa")
    print()

    if avisos:
        print("MESMO PADRAO, MAS NAO E FALHA — rascunho ou copia de teste")
        for nome, status, gatilhos, segmentos in avisos:
            print("  %-38s [%s]  gatilho: %s  (%d segmento(s))"
                  % (nome[:38], status, ", ".join(sorted(gatilhos)) or "nenhum", len(segmentos)))
        print("  Rascunho nao roda; `ZZ TESTE*` existe para exibir o defeito.\n")

    if corretos:
        print("CORRETO — gatilho carrega a oportunidade, a condicao funciona ali")
        for nome, status, gatilhos, segmentos in corretos:
            print("  %-38s [%s]  %d segmento(s)  %s"
                  % (nome[:38], status, len(segmentos), ", ".join(sorted(gatilhos))))
        print()

    return 1 if graves else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        sys.exit(0)
