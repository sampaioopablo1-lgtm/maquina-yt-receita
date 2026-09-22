"""Descobre a forma do no de tarefa que REALMENTE cria tarefa.

O formato copiado do 'Interceptacao de Sinal - Clique' publicado passa na
publicacao mas NAO cria tarefa nenhuma (provado: a Cadencia 12x30 rodou o
T1 inteiro - aplicou fila-tel e toque - e o contato ficou com tasks: []).
Aquele workflow nunca disparou (aponta para link morto), entao o formato
dele nunca foi provado em execucao.

Aqui cada variante vira um workflow de teste publicado, dispara numa tag e
o resultado e lido pela API. Criar tarefa e o produto final da cadencia -
sem isso o SDR nao tem o que fazer.

Uso: python probe_tarefa.py <variante>
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

NOME = "ZZ TESTE TAREFA"
TAG = "teste-tarefa"

VARIANTES = {
    "a": {"nome": "dueDate como duracao '0'",
          "attrs": {"title": "[TESTE] tarefa variante A",
                    "body": "<p>variante A</p>",
                    "assignedTo": "contact.assigned_user",
                    "type": "task_notification", "dueDate": "0",
                    "__customInputs__": {"dueDate": "duration-picker"}}},
    "b": {"nome": "dueDate objeto de duracao",
          "attrs": {"title": "[TESTE] tarefa variante B",
                    "body": "<p>variante B</p>",
                    "assignedTo": "contact.assigned_user",
                    "type": "task_notification",
                    "dueDate": {"type": "days", "value": 0, "when": "after"},
                    "__customInputs__": {"dueDate": "duration-picker"}}},
    "c": {"nome": "sem dueDate",
          "attrs": {"title": "[TESTE] tarefa variante C",
                    "body": "<p>variante C</p>",
                    "assignedTo": "contact.assigned_user",
                    "type": "task_notification"}},
    "d": {"nome": "assignedTo com id do usuario",
          "attrs": {"title": "[TESTE] tarefa variante D",
                    "body": "<p>variante D</p>",
                    "assignedTo": g.USER,
                    "type": "task_notification", "dueDate": "0",
                    "__customInputs__": {"dueDate": "duration-picker"}}},
}

v = sys.argv[1] if len(sys.argv) > 1 else "a"
cfg = VARIANTES[v]
print("variante %s: %s" % (v, cfg["nome"]))

c = g.client()
c.create_location_tag(TAG)
ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
       if w.get("type") == "workflow"}
wf = ids.get(NOME) or g.create_workflow(c, NOME)

no = {"id": g.uid(), "name": "Add Task", "type": "task-notification",
      "attributes": cfg["attrs"]}
g.preencher(c, wf, NOME, [no], [g.tag_trigger("Teste Tarefa", TAG)],
            allow_reentry=True)
print("publicado" if g.publicar(c, wf) else "NAO PUBLICOU")
print("agora dispare a tag '%s' e leia as tarefas do contato" % TAG)
