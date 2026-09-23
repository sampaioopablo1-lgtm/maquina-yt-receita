"""Espelho de Etapa - a etapa/status da oportunidade vira TAG no contato.

Achado de 23/09/2026 (registro de execucao da ZZ TESTE 12X30): num workflow
disparado por TAG, a condicao "Pipeline stage is CONECTAR" le valor VAZIO e
da falso - a oportunidade nao esta no contexto. O mesmo vale para gatilho de
contato, resposta, link e agendamento. 11 workflows publicados testavam etapa
assim (Reengajamento, No-show, SLA, Retorno Vencido, Interceptacao, Opt-out,
CONECTAR Estagnado, 12x30 parte 2, Fechar Horario...).

Este workflow tem gatilho de OPORTUNIDADE (onde a condicao funciona) e mantem
exatamente uma tag de estado no contato:
  open + etapa X  -> etapa-novo-lead | etapa-conectar | etapa-reuniao |
                     etapa-negociar | etapa-formalizar
  abandoned       -> status-nutricao
  lost            -> status-perdido
  won             -> status-ganho
Os outros workflows testam a TAG (funciona com qualquer gatilho).
Sem janela: tem de refletir na hora. Re-entrada ligada.

Uso: python build_espelho_etapa.py --so-montar | (sem argumento: grava rascunho)
"""
import io
import os
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "Espelho de Etapa"
ETAPAS = [("NOVO LEAD", "etapa-novo-lead"), ("CONECTAR", "etapa-conectar"),
          ("REUNIÃO DE DIAGNÓSTICO", "etapa-reuniao"), ("NEGOCIAR", "etapa-negociar"),
          ("FORMALIZAR", "etapa-formalizar")]
STATUS = [("abandoned", "status-nutricao"), ("lost", "status-perdido"), ("won", "status-ganho")]
TODAS = [t for _, t in ETAPAS] + [t for _, t in STATUS]

SO_MONTAR = "--so-montar" in sys.argv
if SO_MONTAR:
    c, WF = None, "00000000-0000-0000-0000-000000000002"
else:
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
           if w.get("type") == "workflow"}
    WF = ids.get(NOME) or g.create_workflow(c, NOME)
print("workflow: %s (%s)" % (NOME, WF))


def cadeia(itens, cond_de, fim):
    """If/Else encadeado: o primeiro que casar poe a tag e termina."""
    if not itens:
        return fim
    chave, tag = itens[0]
    return [g.Branch("É %s?" % chave, [cond_de(chave)], sim=[g.tag_step([tag])],
                     nao=cadeia(itens[1:], cond_de, fim))]


por_etapa = cadeia(ETAPAS, lambda e: g.cond("opportunities", "pipelineStageId", "==",
                                             g.STAGES[e]), [])
por_status = cadeia(STATUS, lambda s: g.cond("opportunities", "status", "==", s), [])
passos = [g.tag_step(TODAS, remove=True),
          g.Branch("Oportunidade aberta?", [g.cond("opportunities", "status", "==", "open")],
                   sim=por_etapa, nao=por_status)]


def gat(tipo, nome, extra):
    return {"status": "draft", "schedule_config": {}, "type": tipo, "masterType": "highlevel",
            "name": nome, "active": True, "triggersChanged": True, "location_id": g.LOC,
            "conditions": [{"operator": "==", "field": "opportunity.pipelineId",
                            "value": g.PIPELINE, "title": "No pipeline", "type": "select"}] + extra}


gatilhos = [gat("pipeline_stage_updated", "Etapa Do Funil Alterada", [])] + [
    gat("opportunity_status_changed", "Status Da Oportunidade Alterado",
        [{"operator": "==", "field": "opportunity.status", "value": s,
          "title": "Movido para o status", "type": "select", "id": "moved-to-status"}])
    for s in ("open", "won", "lost", "abandoned")]

if SO_MONTAR:
    tpl = g.montar(passos)
else:
    for t in TODAS:
        c.create_location_tag(t)
    g.preencher(c, WF, NOME, passos, gatilhos, allow_reentry=True, stop_on_response=False)
    doc = g.export(c, WF, os.path.join(os.path.dirname(__file__), "..", "workflows-json",
                                       NOME + ".json"))
    tpl = (doc["workflow"].get("workflowData") or {}).get("templates") or []
    print("gatilhos:", len([t for t in doc["triggers"] if not t.get("deleted")]))
print("nós=%d" % len(tpl), dict(Counter(s["type"] for s in tpl)))
