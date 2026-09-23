"""Auditoria ao vivo de todos os publicados (somente leitura).
1 condicao de oportunidade em workflow sem gatilho de oportunidade
2 no apontando para workflow inexistente/desligado
3 relogio errado ('sim' ou {{right_now}} puro) nos campos de data
4 tarefa com prefixo que a Faxina nao reconhece
5 workflow que cria tarefa sem janela
6 mensagem (sms) sem janela
Uso: python auditoria_final.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g
from faxina_tarefas import familia
OPP = {'pipeline_stage_updated', 'opportunity_status_changed', 'opportunity_created', 'opportunity_changed'}
RELOGIO = ("uWUGz5gVGAFmNuk5GXbX", "PKzNljzDoU77O14nHLrV", "uXf6nG2tKQ7EtGCbHkfy")
c = g.client()
todos = {w['id']: w for w in c.request('GET', '/workflow/' + g.LOC)}
prob, n = [], 0
for wid, w in todos.items():
    if w.get('status') != 'published':
        continue
    n += 1
    d = c.request('GET', '/workflow/' + g.LOC + '/' + wid)
    tpl = d['workflowData']['templates']
    trs = {t.get('type') for t in c.request('GET', '/workflow/' + g.LOC + '/trigger?workflowId=' + wid) if not t.get('deleted')}
    so_opp = bool(trs) and trs <= OPP
    for t in tpl:
        a = t.get('attributes') or {}
        if t['type'] == 'if_else' and not so_opp and w['name'] != 'Cadência 12x30':
            if any(x.get('conditionType') == 'opportunities' for b in a.get('branches', []) for sg in b.get('segments', []) for x in sg.get('conditions', [])):
                prob.append('1 condição de oportunidade: %s / %s' % (w['name'], t.get('name')))
        if t['type'] in ('remove_from_workflow', 'add_to_workflow'):
            for x in (a.get('workflow_id') or []):
                if x not in todos:
                    prob.append('2 aponta p/ inexistente: %s → %s' % (w['name'], x))
                elif todos[x].get('status') != 'published' and x != wid:
                    prob.append('2 aponta p/ desligado (inofensivo): %s → %s' % (w['name'], todos[x].get('name')))
        if t['type'] == 'update_contact_field':
            for f in a.get('fields', []):
                if f.get('field') in RELOGIO and f.get('value') in ('sim', '{{right_now}}'):
                    prob.append('3 relógio errado: %s' % w['name'])
        if t['type'] == 'update_contact_field':
            for f in a.get('fields', []):
                if f.get('type') == 'date' and f.get('value') in ('{{right_now.date}}', '{{right_now}}'):
                    prob.append('7 campo de data com formato que dá erro: %s / %s' % (w['name'], f.get('title')))
        if t['type'] == 'task-notification' and familia(a.get('title')) is None:
            prob.append('4 prefixo desconhecido: %s: %s' % (w['name'], a.get('title')))
    if any(t['type'] == 'task-notification' for t in tpl) and not d.get('window'):
        prob.append('5 tarefa sem janela: %s' % w['name'])
    if any(t['type'] == 'sms' for t in tpl) and not d.get('window'):
        prob.append('6 mensagem sem janela: %s' % w['name'])
print('publicados auditados:', n)
for p in sorted(set(prob)):
    print(p)
print('problemas:', len([p for p in set(prob) if 'inofensivo' not in p]))
