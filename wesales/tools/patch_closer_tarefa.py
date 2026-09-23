"""A4: o closer nao recebia NENHUMA tarefa. No Loop do closer v2, ramo
"Veredito e Sim?", entra a tarefa [CLOSER] Apresentar proposta antes do salto
para as checagens de calibracao. Insercao cirurgica: os outros nos ficam iguais.
Uso: python patch_closer_tarefa.py [--aplicar]"""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_funil_reuniao import put, g
aplicar = "--aplicar" in sys.argv
c = g.client()
wf = [w['id'] for w in c.request('GET', '/workflow/' + g.LOC) if w.get('name') == 'Loop do closer v2'][0]
cur = c.request('GET', '/workflow/' + g.LOC + '/' + wf)
T = copy.deepcopy(cur['workflowData']['templates'])
by = {t['id']: t for t in T}
if any((t.get('attributes') or {}).get('title', '').startswith('[CLOSER]') for t in T):
    sys.exit('ja tem tarefa [CLOSER] - nada a fazer')
sim_if = next(t for t in T if t.get('name') == 'Veredito é Sim?')
ramo = next(t for t in T if t.get('parent') == sim_if['id'] and t.get('name') == 'Branch')
prox = by[ramo['next']]                       # o goto que hoje e o 1o no do ramo
tarefa = {"id": g.uid(), "name": "Tarefa do closer — apresentar proposta", "type": "task-notification",
          "parent": ramo['id'], "parentKey": ramo['id'], "next": prox['id'], "order": 0, "cat": "",
          "attributes": {"title": "[CLOSER] Apresentar proposta",
                         "body": '<p style="margin:0px; padding-left: 0px!important;">Reunião de diagnóstico '
                                 'qualificada. Monte e apresente a proposta. Ao apresentar, mova o lead para '
                                 '<b>NEGOCIAR</b> — esta tarefa sai sozinha quando ele mudar de etapa.</p>',
                         "assignedTo": "contact.assigned_user", "type": "task_notification",
                         "dueDate": "0", "__customInputs__": {"dueDate": "duration-picker"}},
          "advanceCanvasMeta": prox.get('advanceCanvasMeta')}
ramo['next'] = tarefa['id']
prox['parentKey'] = tarefa['id']
prox['order'] = 1
T.insert(T.index(prox), tarefa)
print('ramo', ramo['id'][:8], '-> tarefa', tarefa['id'][:8], '-> goto', prox['id'][:8], '| nos', len(T))
if aplicar:
    g.export(c, wf, os.path.join('..', 'workflows-json', '_antes-patch-closer', 'Loop do closer v2.json'))
    put(c, cur, T)
    v = c.request('GET', '/workflow/' + g.LOC + '/' + wf)
    vt = v['workflowData']['templates']
    print('conferido: status=%s nos=%d tarefa=%s gatilhos=%s' % (v.get('status'), len(vt),
          any(x.get('attributes', {}).get('title') == '[CLOSER] Apresentar proposta' for x in vt),
          [t.get('active') for t in c.request('GET', '/workflow/' + g.LOC + '/trigger?workflowId=' + wf) if not t.get('deleted')]))
    g.export(c, wf, os.path.join('..', 'workflows-json', 'Loop do closer v2.json'))
