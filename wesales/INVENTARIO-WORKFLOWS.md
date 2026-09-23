# Inventário dos workflows publicados (ao vivo)

Gerado por `tools/inventario.py`. Só leitura.

## Alerta de Speed-to-lead

`0ce8937d-f994-4a5d-9551-442c3299cf03` · 12 nós

- **Gatilho** `pipeline_stage_updated` (ativo): No pipeline == 0Fo2xbeayE4EP6yuSUtq; Movido para o estágio == CONECTAR
- `if_else` É inbound? —  tag:cad-inbound
- `if_else` Ainda sem 1ª tentativa? —  etapa:CONECTAR tag:pausado
- `add_contact_tag` Add Tag —  tag:atraso-1a-tentativa

## CONECTAR Estagnado

`249232e3-e9e3-4338-8956-5f6ea0776af1` · 20 nós

- **Gatilho** `contact_changed` (ativo): Tentativa nº == 0

## Cadência 12x30

`c64a808b-3040-431e-8015-642a265e1022` · 381 nós

- **Gatilho** `pipeline_stage_updated` (ativo): No pipeline == 0Fo2xbeayE4EP6yuSUtq; Movido para o estágio == CONECTAR
- **Gatilho** `contact_tag` (ativo): Tag Added index-of-true cad-outbound
- `if_else` É lead de outra régua? —  tag:cad-inbound tag:reengajamento-ativo
- `add_contact_tag` Add Tag —  tag:telefone-invalido
- `create_opportunity` Update Opportunity — oportunidade etapa:CONECTAR
- `add_contact_tag` Add Tag —  tag:nutricao-90d
- `create_opportunity` Update Opportunity — oportunidade etapa:CONECTAR
- `update_contact_field` Inicializa contadores —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº campo:WA não atendidas seguidas
- `if_else` T1 · Lead pausado? —  tag:pausado
- `if_else` T1 · Ainda vale tentar? —  campo:Resultado da tentativa tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `remove_contact_tag` Remove Tag —  tag:atraso-1a-tentativa
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` T1 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] T1 · Ligar → WhatsApp 
- `task-notification` Add Task — tarefa: [CADENCIA] T1 · WhatsApp → Ligar 
- `add_contact_tag` Add Tag —  tag:toque
- `if_else` T1 · Tentou e não conversou? (mensagem) —  campo:Resultado da tentativa
- `sms` WhatsApp · MT1-v1 — mensagem 
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` T1 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` T1 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` T1 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` T1 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 
- `if_else` T1 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` T2 · Lead pausado? —  tag:pausado
- `if_else` T2 · Ainda vale tentar? —  campo:Resultado da tentativa tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` T2 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] T2 · Ligar → WhatsApp 
- `task-notification` Add Task — tarefa: [CADENCIA] T2 · WhatsApp → Ligar 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` T2 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` T2 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` T2 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` T2 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 
- `if_else` T2 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` T3 · Lead pausado? —  tag:pausado
- `if_else` T3 · Ainda vale tentar? —  campo:Resultado da tentativa tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` T3 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] T3 · Ligar → WhatsApp 
- `task-notification` Add Task — tarefa: [CADENCIA] T3 · WhatsApp → Ligar 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` T3 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` T3 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` T3 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` T3 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 
- `if_else` T3 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` T4 · Lead pausado? —  tag:pausado
- `if_else` T4 · Ainda vale tentar? —  campo:Resultado da tentativa tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` T4 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] T4 · Ligar → WhatsApp 
- `task-notification` Add Task — tarefa: [CADENCIA] T4 · WhatsApp → Ligar 
- `add_contact_tag` Add Tag —  tag:toque
- `if_else` T4 · Tentou e não conversou? (mensagem) —  campo:Resultado da tentativa
- `sms` WhatsApp · MT4-v1 — mensagem 
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` T4 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` T4 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` T4 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` T4 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 
- `if_else` T4 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` T5 · Lead pausado? —  tag:pausado
- `if_else` T5 · Ainda vale tentar? —  campo:Resultado da tentativa tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` T5 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] T5 · Ligar → WhatsApp 
- `task-notification` Add Task — tarefa: [CADENCIA] T5 · WhatsApp → Ligar 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` T5 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` T5 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` T5 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` T5 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 
- `if_else` T5 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` T6 · Lead pausado? —  tag:pausado
- `if_else` T6 · Ainda vale tentar? —  campo:Resultado da tentativa tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` T6 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] T6 · Ligar → WhatsApp 
- `task-notification` Add Task — tarefa: [CADENCIA] T6 · WhatsApp → Ligar 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` T6 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` T6 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` T6 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` T6 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 
- `if_else` T6 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 

## Cadência 12x30 — parte 2

`17e6dc19-3eca-42e8-83ff-e25a9d5c28e8` · 347 nós

- **Gatilho** `contact_tag` (ativo): Tag Added index-of-true cadencia-12x30-p2
- `if_else` T7 · Lead pausado? —  tag:pausado
- `if_else` T7 · Ainda vale tentar? —  campo:Resultado da tentativa tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` T7 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] T7 · Ligar → WhatsApp 
- `task-notification` Add Task — tarefa: [CADENCIA] T7 · WhatsApp → Ligar 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` T7 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` T7 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` T7 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` T7 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 — parte 2 
- `if_else` T7 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` T8 · Lead pausado? —  tag:pausado
- `if_else` T8 · Ainda vale tentar? —  campo:Resultado da tentativa tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` T8 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] T8 · Ligar → WhatsApp 
- `task-notification` Add Task — tarefa: [CADENCIA] T8 · WhatsApp → Ligar 
- `add_contact_tag` Add Tag —  tag:toque
- `if_else` T8 · Tentou e não conversou? (mensagem) —  campo:Resultado da tentativa
- `sms` WhatsApp · MT8-v1 — mensagem 
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` T8 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` T8 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` T8 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` T8 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 — parte 2 
- `if_else` T8 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` T9 · Lead pausado? —  tag:pausado
- `if_else` T9 · Ainda vale tentar? —  campo:Resultado da tentativa tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` T9 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] T9 · Ligar → WhatsApp 
- `task-notification` Add Task — tarefa: [CADENCIA] T9 · WhatsApp → Ligar 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` T9 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` T9 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` T9 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` T9 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 — parte 2 
- `if_else` T9 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` T10 · Lead pausado? —  tag:pausado
- `if_else` T10 · Ainda vale tentar? —  campo:Resultado da tentativa tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` T10 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] T10 · Ligar → WhatsApp 
- `task-notification` Add Task — tarefa: [CADENCIA] T10 · WhatsApp → Ligar 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` T10 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` T10 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` T10 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` T10 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 — parte 2 
- `if_else` T10 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` T11 · Lead pausado? —  tag:pausado
- `if_else` T11 · Ainda vale tentar? —  campo:Resultado da tentativa tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` T11 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] T11 · Ligar → WhatsApp 
- `task-notification` Add Task — tarefa: [CADENCIA] T11 · WhatsApp → Ligar 
- `add_contact_tag` Add Tag —  tag:toque
- `if_else` T11 · Tentou e não conversou? (mensagem) —  campo:Resultado da tentativa
- `sms` WhatsApp · MT11-v1 — mensagem 
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` T11 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` T11 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` T11 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` T11 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 — parte 2 
- `if_else` T11 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` T12 · Lead pausado? —  tag:pausado
- `if_else` T12 · Ainda vale tentar? —  campo:Resultado da tentativa tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `if_else` T12 · Tentou e não conversou? (mensagem) —  campo:Resultado da tentativa
- `sms` WhatsApp · MT12-v1 — mensagem 
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` T12 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` T12 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 — parte 2 
- `if_else` T12 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `create_opportunity` Update Opportunity — oportunidade etapa:CONECTAR
- `add_contact_tag` Add Tag —  tag:nutricao-90d
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 — parte 2 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 — parte 2 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 — parte 2 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 — parte 2 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 — parte 2 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30 — parte 2 

## Cadência Inbound

`c2375e2f-b4cb-4947-8377-7c1e0529ba82` · 272 nós

- **Gatilho** `pipeline_stage_updated` (ativo): No pipeline == 0Fo2xbeayE4EP6yuSUtq; Movido para o estágio == CONECTAR
- `if_else` É lead de inbound? —  tag:cad-inbound
- `add_contact_tag` Add Tag —  tag:telefone-invalido
- `create_opportunity` Update Opportunity — oportunidade etapa:CONECTAR
- `add_contact_tag` Add Tag —  tag:nutricao-90d
- `create_opportunity` Update Opportunity — oportunidade etapa:CONECTAR
- `update_contact_field` Inicializa contadores —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº campo:WA não atendidas seguidas
- `sms` WhatsApp · MI-0 — mensagem 
- `add_contact_tag` Add Tag —  tag:fila-quente
- `if_else` TI1 · Lead pausado? —  tag:pausado
- `if_else` TI1 · Ainda vale ligar? —  campo:Resultado da tentativa etapa:CONECTAR tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `remove_contact_tag` Remove Tag —  tag:atraso-1a-tentativa
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` TI1 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] TI1 · Ligar → WhatsApp — Inbound 
- `task-notification` Add Task — tarefa: [CADENCIA] TI1 · WhatsApp → Ligar — Inbound 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` TI1 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` TI1 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` TI1 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` TI1 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência Inbound 
- `if_else` TI1 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` TI2 · Lead pausado? —  tag:pausado
- `if_else` TI2 · Ainda vale ligar? —  campo:Resultado da tentativa etapa:CONECTAR tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` TI2 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] TI2 · Ligar → WhatsApp — Inbound 
- `task-notification` Add Task — tarefa: [CADENCIA] TI2 · WhatsApp → Ligar — Inbound 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` TI2 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` TI2 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` TI2 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` TI2 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência Inbound 
- `if_else` TI2 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` TI3 · Lead pausado? —  tag:pausado
- `if_else` TI3 · Ainda vale ligar? —  campo:Resultado da tentativa etapa:CONECTAR tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` TI3 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] TI3 · Ligar → WhatsApp — Inbound 
- `task-notification` Add Task — tarefa: [CADENCIA] TI3 · WhatsApp → Ligar — Inbound 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` TI3 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` TI3 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` TI3 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` TI3 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência Inbound 
- `if_else` TI3 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` TI4 · Lead pausado? —  tag:pausado
- `if_else` TI4 · Ainda vale ligar? —  campo:Resultado da tentativa etapa:CONECTAR tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` TI4 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] TI4 · Ligar → WhatsApp — Inbound 
- `task-notification` Add Task — tarefa: [CADENCIA] TI4 · WhatsApp → Ligar — Inbound 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` TI4 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` TI4 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` TI4 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` TI4 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência Inbound 
- `if_else` TI4 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` TI5 · Lead pausado? —  tag:pausado
- `if_else` TI5 · Ainda vale ligar? —  campo:Resultado da tentativa etapa:CONECTAR tag:nao-perturbe tag:telefone-invalido
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `if_else` TI5 · WhatsApp bloqueado para este lead? —  campo:WA não atendidas seguidas
- `task-notification` Add Task — tarefa: [CADENCIA] TI5 · Ligar → WhatsApp — Inbound 
- `task-notification` Add Task — tarefa: [CADENCIA] TI5 · WhatsApp → Ligar — Inbound 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` TI5 · WhatsApp ainda vem primeiro? —  campo:WA não atendidas seguidas
- `if_else` TI5 · WhatsApp não atendido? —  campo:Resultado da tentativa
- `math_operation` Math operation —  campo:WA não atendidas seguidas
- `if_else` TI5 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `if_else` TI5 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência Inbound 
- `if_else` TI5 · Sem resposta registrada? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `sms` WhatsApp · MIF-v2 — mensagem 
- `remove_contact_tag` Remove Tag —  tag:cad-inbound
- `add_contact_tag` Add Tag —  tag:cad-outbound
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência Inbound 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência Inbound 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência Inbound 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência Inbound 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência Inbound 
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência Inbound 

## Contador de Toques

`f0e8a0f8-d18e-4f0e-86ef-75315b5fa616` · 4 nós

- **Gatilho** `contact_tag` (ativo): Tag Added index-of-true toque
- `remove_contact_tag` Remove Tag —  tag:toque

## Espelho de Etapa

`2b1667a4-e289-4d27-b6cf-824b93971b32` · 36 nós

- **Gatilho** `opportunity_status_changed` (ativo): No pipeline == 0Fo2xbeayE4EP6yuSUtq; Movido para o status == open
- **Gatilho** `opportunity_status_changed` (ativo): No pipeline == 0Fo2xbeayE4EP6yuSUtq; Movido para o status == won
- **Gatilho** `opportunity_status_changed` (ativo): No pipeline == 0Fo2xbeayE4EP6yuSUtq; Movido para o status == abandoned
- **Gatilho** `opportunity_status_changed` (ativo): No pipeline == 0Fo2xbeayE4EP6yuSUtq; Movido para o status == lost
- **Gatilho** `pipeline_stage_updated` (ativo): No pipeline == 0Fo2xbeayE4EP6yuSUtq
- `if_else` É NOVO LEAD? —  etapa:NOVO LEAD
- `if_else` É CONECTAR? —  etapa:CONECTAR
- `if_else` É REUNIÃO DE DIAGNÓSTICO? —  etapa:REUNIÃO DE DIAGNÓSTICO
- `if_else` É NEGOCIAR? —  etapa:NEGOCIAR
- `if_else` É FORMALIZAR? —  etapa:FORMALIZAR

## Fechar Horário

`82dd1fad-1bdd-44f7-8214-3a685521e2b4` · 41 nós

- **Gatilho** `contact_tag` (ativo): Tag Added index-of-true fechar-horario
- `remove_from_workflow` Sai das cadências de tentativa — remove_from_workflow → Cadência 12x30, Cadência Inbound, Reengajamento 90 dias, Cadência 12x30 — parte 2 
- `if_else` FH2 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `sms` WhatsApp · MFH1-v1 — mensagem 
- `task-notification` Add Task — tarefa: [FECHAR HORÁRIO] FH2 · WhatsApp → Ligar para marcar a reunião 
- `if_else` FH3 · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `sms` WhatsApp · MFH2-v1 — mensagem 
- `task-notification` Add Task — tarefa: [FECHAR HORÁRIO] FH3 · WhatsApp → Ligar para marcar a reunião 
- `if_else` Fim · Pediu retorno? (pausa) —  campo:Resultado da tentativa
- `create_opportunity` Update Opportunity — oportunidade etapa:CONECTAR
- `add_contact_tag` Add Tag —  tag:nutricao-90d

## Fila Travada

`23c33803-c760-49fd-a189-8d1a86bf3d9e` · 8 nós

- **Gatilho** `contact_tag` (ativo): Tag Added index-of-true fila-tel
- **Gatilho** `contact_tag` (ativo): Tag Added index-of-true fila-wa
- `if_else` Fila ainda presa? —  tag:fila-tel tag:fila-wa

## Interceptação de Sinal — Clique v2

`30b5fc0d-a955-4a80-8b28-a43a37475f83` · 15 nós

- **Gatilho** `trigger_link` (ativo): Link de acionamento == vSUOvEbVZfxBlWFlTvDV
- `if_else` yes —  tag:nao-perturbe
- `add_contact_tag` Add Tag —  tag:fila-quente
- `task-notification` Sinal clique — tarefa: [CADENCIA] Sinal: clicou no link — ligar agora 

## Interceptação de Sinal — Resposta v2

`42bfaf59-ba56-455d-bb4c-8ecd39efbcd1` · 18 nós

- **Gatilho** `customer_reply` (ativo): Canal de resposta == 20
- **Gatilho** `customer_reply` (ativo): Canal de resposta == 19
- `if_else` yes —  tag:nao-perturbe
- `add_contact_tag` Add Tag —  tag:fila-quente
- `task-notification` Sinal clique — tarefa: [CADENCIA] Sinal: respondeu mensagem — ligar agora 

## Lead Esquecido em NOVO LEAD

`60268916-7522-4a32-b9ee-0f00993988fb` · 7 nós

- **Gatilho** `pipeline_stage_updated` (ativo): No pipeline == 0Fo2xbeayE4EP6yuSUtq; Movido para o estágio == NOVO LEAD
- `if_else` Ainda em NOVO LEAD e aberta? —  etapa:NOVO LEAD

## Loop do closer v2

`db2f9531-39e4-4107-ad65-33666ab0fd35` · 31 nós

- **Gatilho** `contact_changed` (ativo): Reunião foi qualificada has-changed None
- `if_else` Veredito está vazio? —  campo:Reunião foi qualificada
- `if_else` Veredito é Sim? —  campo:Reunião foi qualificada
- `if_else` Veredito é Parcial? —  campo:Reunião foi qualificada
- `create_opportunity` Update Opportunity — oportunidade etapa:REUNIÃO DE DIAGNÓSTICO
- `add_contact_tag` Add Tag —  tag:nutricao-90d
- `create_opportunity` Update Opportunity — oportunidade etapa:REUNIÃO DE DIAGNÓSTICO
- `add_contact_tag` Add Tag —  tag:nutricao-90d
- `create_opportunity` Update Opportunity — oportunidade etapa:REUNIÃO DE DIAGNÓSTICO
- `if_else` Nota alta mas closer reprovou? —  campo:Reunião foi qualificada
- `if_else` Nota baixa mas closer aprovou? —  campo:Reunião foi qualificada

## Mestre de saída v2

`c616e2d7-a618-4581-94f4-7eefbcef8047` · 10 nós

- **Gatilho** `opportunity_status_changed` (ativo): No pipeline == 0Fo2xbeayE4EP6yuSUtq; Movido para o status == lost
- **Gatilho** `pipeline_stage_updated` (ativo): No pipeline == 0Fo2xbeayE4EP6yuSUtq
- **Gatilho** `opportunity_status_changed` (ativo): No pipeline == 0Fo2xbeayE4EP6yuSUtq; Movido para o status == abandoned
- `if_else` Acabou de chegar em NOVO LEAD? —  etapa:NOVO LEAD
- `if_else` yes —  etapa:CONECTAR
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Interceptação de Sinal — Clique v2 
- `remove_contact_tag` Remove Tag —  tag:atraso-1a-tentativa tag:fila-quente tag:fila-tel tag:fila-wa tag:pausado tag:reengajamento-ativo
- `add_contact_tag` Add Tag —  tag:limpar-tarefas

## Monitor de Capacidade

`63cbb270-5fc8-4c04-8c30-e5ebeaa2eb6d` · 1 nós

- **Gatilho** `scheduler_trigger` (ativo): Intervalo == cron; Expressão Cron == 0 11,15 * * 1-5

## Opt-out por Palavra-chave

`849051a8-31c2-44f1-8968-b94dcc5f5fe6` · 14 nós

- **Gatilho** `customer_reply` (ativo): Canal de resposta == 19
- **Gatilho** `customer_reply` (ativo): Canal de resposta == 20
- `add_contact_tag` Add Tag —  tag:nao-perturbe
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `create_opportunity` Update Opportunity — oportunidade etapa:CONECTAR

## Porta de Entrada

`e08a1580-975b-4c0f-934e-582fc6a0dbaa` · 1 nós

- **Gatilho** `contact_created` (ativo): 
- `create_opportunity` Criar ou atualizar oportunidade — oportunidade etapa:NOVO LEAD

## Pós-agendamento v2

`81815fcc-ff4f-4b72-8a1f-7dbf44ce6911` · 180 nós

- **Gatilho** `appointment` (ativo): Tipo de evento == normal; In calendar == 3uNQFjCEDe7b4gKZJuOZ; Appointment status is == confirmed; contactMode is-any-of ['contact']
- `create_opportunity` Criar/Atualizar Oportunidade em REUNIÃO  — oportunidade etapa:REUNIÃO DE DIAGNÓSTICO
- `remove_from_workflow` Remover dos Workflows Paralelos — remove_from_workflow → Cadência 12x30, Qualificação por IA no WhatsApp, Recuperação de No-show, SLA do Closer — No-show, Cadência Inbound, Reengajamento 90 dias, Fechar Horário, Cadência 12x30 — parte 2 

## Pós-ligação v2

`0e82d852-15f4-4219-9d0d-da0cccf11826` · 142 nós

- **Gatilho** `contact_changed` (ativo): Resultado da tentativa has-changed None
- `if_else` yes —  campo:Resultado da tentativa
- `if_else` yes —  tag:fila-wa
- `if_else` yes —  campo:Resultado da tentativa
- `if_else` yes —  tag:fila-wa
- `update_contact_field` Update contact field —  campo:WA não atendidas seguidas
- `add_contact_tag` Add Tag —  tag:conectado-hoje
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `create_opportunity` Criar ou atualizar oportunidade — oportunidade etapa:CONECTAR
- `task-notification` Add task — tarefa: [FECHAR HORÁRIO] Qualificar e agendar a reunião de diagnóstico 
- `if_else` yes —  tag:fila-wa
- `update_contact_field` Update contact field —  campo:WA não atendidas seguidas
- `add_contact_tag` Add Tag —  tag:conectado-hoje
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `create_opportunity` Criar ou atualizar oportunidade — oportunidade etapa:CONECTAR
- `task-notification` Add task — tarefa: [FECHAR HORÁRIO] Qualificar e agendar a reunião de diagnóstico 
- `if_else` yes —  tag:fila-wa
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `update_contact_field` Zera WA não atendidas seguidas —  campo:WA não atendidas seguidas
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:fila-quente
- `task-notification` Add task — tarefa: [RETORNO] Ligar de volta 
- `add_contact_tag` Add Tag —  tag:nao-perturbe
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30, Qualificação por IA no WhatsApp, Cadência 12x30 — parte 2 
- `create_opportunity` Criar ou atualizar oportunidade — oportunidade 
- `add_contact_tag` Add Tag —  tag:telefone-invalido
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `create_opportunity` Criar ou atualizar oportunidade — oportunidade 
- `add_contact_tag` Add Tag —  tag:nutricao-90d
- `create_opportunity` Criar ou atualizar oportunidade — oportunidade 
- `if_else` yes —  campo:Resultado da tentativa
- `if_else` yes —  tag:fila-wa
- `update_contact_field` Update contact field —  campo:WA não atendidas seguidas
- `add_contact_tag` Add Tag —  tag:conectado-hoje
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `create_opportunity` Criar ou atualizar oportunidade — oportunidade etapa:CONECTAR
- `task-notification` Add task — tarefa: [FECHAR HORÁRIO] Qualificar e agendar a reunião de diagnóstico 
- `update_contact_field` Update contact field —  campo:WA não atendidas seguidas
- `add_contact_tag` Add Tag —  tag:conectado-hoje
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `create_opportunity` Criar ou atualizar oportunidade — oportunidade etapa:CONECTAR
- `task-notification` Add task — tarefa: [FECHAR HORÁRIO] Qualificar e agendar a reunião de diagnóstico 
- `if_else` yes —  tag:fila-wa
- `update_contact_field` Update contact field —  campo:WA não atendidas seguidas
- `add_contact_tag` Add Tag —  tag:conectado-hoje
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `create_opportunity` Criar ou atualizar oportunidade — oportunidade etapa:CONECTAR
- `task-notification` Add task — tarefa: [FECHAR HORÁRIO] Qualificar e agendar a reunião de diagnóstico 
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` yes —  tag:fila-wa
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `update_contact_field` Zera WA não atendidas seguidas —  campo:WA não atendidas seguidas
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:fila-quente
- `task-notification` Add task — tarefa: [RETORNO] Ligar de volta 
- `add_contact_tag` Add Tag —  tag:nao-perturbe
- `remove_contact_tag` Remove Tag —  tag:fila-quente tag:fila-tel tag:fila-wa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Cadência 12x30, Qualificação por IA no WhatsApp, Cadência 12x30 — parte 2 
- `create_opportunity` Criar ou atualizar oportunidade — oportunidade 
- `add_contact_tag` Add Tag —  tag:telefone-invalido
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `create_opportunity` Criar ou atualizar oportunidade — oportunidade 
- `add_contact_tag` Add Tag —  tag:nutricao-90d
- `create_opportunity` Criar ou atualizar oportunidade — oportunidade 

## Qualidade da Conexão

`5fbb2e5d-88f5-4d84-a7ec-4c87c7078198` · 8 nós

- **Gatilho** `transcript_generated` (ativo): Type == call; Direction == outbound
- `update_contact_field` 4. Conexão real = Sim (falou 60s ou mais —  campo:Conexão real
- `update_contact_field` 5. Conexão real = Não (menos de 60s) —  campo:Conexão real

## Recuperação de No-show

`050052db-5ae8-43fe-8e94-b0f747563d57` · 40 nós

- **Gatilho** `appointment` (ativo): Tipo de evento == normal; In calendar == 3uNQFjCEDe7b4gKZJuOZ; Appointment status is == noshow; contactMode is-any-of ['contact']
- `remove_contact_tag` Remove Tag —  tag:fila-tel
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `create_opportunity` Update Opportunity — oportunidade etapa:REUNIÃO DE DIAGNÓSTICO
- `add_contact_tag` Add Tag —  tag:fila-tel
- `task-notification` Add Task — tarefa: [CADENCIA] NS1 · Ligar (telefone) — Recuperação de no-show 
- `add_contact_tag` Add Tag —  tag:toque
- `if_else` NS1 · Ainda vale recuperar? —  tag:nao-perturbe tag:pausado
- `add_contact_tag` Add Tag —  tag:fila-tel
- `task-notification` Add Task — tarefa: [CADENCIA] NS2 · Ligar (telefone) — Recuperação de no-show 
- `add_contact_tag` Add Tag —  tag:toque
- `if_else` NS2 · Ainda vale recuperar? —  tag:nao-perturbe tag:pausado
- `add_contact_tag` Add Tag —  tag:fila-tel
- `task-notification` Add Task — tarefa: [CADENCIA] NS3 · Ligar (telefone) — Recuperação de no-show 
- `add_contact_tag` Add Tag —  tag:toque
- `if_else` NS3 · Ainda vale recuperar? —  tag:nao-perturbe tag:pausado
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `remove_contact_tag` Remove Tag —  tag:fila-tel
- `add_contact_tag` Add Tag —  tag:nutricao-90d
- `create_opportunity` Update Opportunity — oportunidade etapa:REUNIÃO DE DIAGNÓSTICO
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Recuperação de No-show 
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Recuperação de No-show 
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Recuperação de No-show 

## Reengajamento 90 dias

`37eb32e4-4c21-4c69-bba1-36879ae0886c` · 105 nós

- **Gatilho** `contact_tag` (ativo): Tag Added index-of-true nutricao-90d
- `if_else` Ainda em nutrição e sem opt-out? —  tag:nao-perturbe tag:nutricao-90d
- `update_contact_field` Zera contadores da nova rodada —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº campo:WA não atendidas seguidas
- `remove_contact_tag` Remove Tag —  tag:nutricao-90d
- `add_contact_tag` Add Tag —  tag:reengajamento-ativo
- `remove_contact_tag` Remove Tag —  tag:cad-inbound
- `add_contact_tag` Add Tag —  tag:cad-outbound
- `create_opportunity` Update Opportunity — oportunidade etapa:CONECTAR
- `if_else` TR1 · Ainda vale ligar? —  campo:Resultado da tentativa tag:nao-perturbe
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `remove_contact_tag` Remove Tag —  tag:atraso-1a-tentativa
- `add_contact_tag` Add Tag —  tag:fila-tel
- `task-notification` Add Task — tarefa: [CADENCIA] TR1 · Ligar (telefone) — Reengajamento 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` TR1 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Reengajamento 90 dias 
- `if_else` TR1 · Sem resposta? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` TR2 · Ainda vale ligar? —  campo:Resultado da tentativa tag:nao-perturbe
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `task-notification` Add Task — tarefa: [CADENCIA] TR2 · Ligar (telefone) — Reengajamento 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` TR2 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Reengajamento 90 dias 
- `if_else` TR2 · Sem resposta? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` TR3 · Ainda vale ligar? —  campo:Resultado da tentativa tag:nao-perturbe
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `task-notification` Add Task — tarefa: [CADENCIA] TR3 · Ligar (telefone) — Reengajamento 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` TR3 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Reengajamento 90 dias 
- `if_else` TR3 · Sem resposta? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `if_else` TR4 · Ainda vale ligar? —  campo:Resultado da tentativa tag:nao-perturbe
- `update_contact_field` Update contact field —  campo:Conexão real campo:Resultado da tentativa campo:Tentativa nº
- `add_contact_tag` Add Tag —  tag:fila-tel
- `task-notification` Add Task — tarefa: [CADENCIA] TR4 · Ligar (telefone) — Reengajamento 
- `add_contact_tag` Add Tag —  tag:toque
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `if_else` TR4 · Atendeu? —  campo:Resultado da tentativa
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Reengajamento 90 dias 
- `if_else` TR4 · Sem resposta? —  campo:Resultado da tentativa
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `update_contact_field` Update contact field —  campo:Resultado da tentativa
- `remove_contact_tag` Remove Tag —  tag:reengajamento-ativo
- `add_contact_tag` Add Tag —  tag:nutricao-90d
- `create_opportunity` Update Opportunity — oportunidade etapa:CONECTAR
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Reengajamento 90 dias 
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Reengajamento 90 dias 
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Reengajamento 90 dias 
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Reengajamento 90 dias 
- `remove_contact_tag` Remove Tag —  tag:fila-tel tag:fila-wa
- `add_contact_tag` Add Tag —  tag:limpar-tarefas
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Reengajamento 90 dias 
- `remove_from_workflow` Remove from Workflow — remove_from_workflow → Reengajamento 90 dias 

## Registro de Comparecimento

`2bec8c21-7da5-4641-842e-c256360a434e` · 6 nós

- **Gatilho** `appointment` (ativo): Tipo de evento == normal; In calendar == 3uNQFjCEDe7b4gKZJuOZ; Appointment status is == showed; contactMode is-any-of ['contact']

## Retorno Vencido

`70ca5354-18e8-4d17-b929-b13d4e71aacf` · 11 nós

- **Gatilho** `contact_changed` (ativo): Data de retorno has-changed None
- `if_else` A data ainda é a mesma? —  campo:Data de retorno
- `if_else` Promessa vencida sem reclassificar? —  campo:Resultado da tentativa

## SLA do Closer — No-show

`b83870d3-5d3f-4eec-9447-4be1392c061c` · 12 nós

- **Gatilho** `appointment` (ativo): Tipo de evento == normal; In calendar == 3uNQFjCEDe7b4gKZJuOZ; Appointment status is == noshow; contactMode is-any-of ['contact']
