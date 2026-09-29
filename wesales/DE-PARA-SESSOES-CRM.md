
## 28-29/09 — Calendly → CRM

- O dono mantém o Calendly (plano grátis, integrado às campanhas; criativo "V11 — CALENDLY F3").
- `wesales/tools/calendly_para_crm.py` lê a API v2 com token pessoal (segredo do GitHub **`CALENDY`**, sem L) — funciona no plano grátis, sem webhook.
- Reunião nova → agenda "Reunião com closer" (título com `calendly:<uuid>`, evita duplicar), tags `calendly` + `fila-quente`, Prioridade 5, tarefa "[LIGAR AGORA]" para a SDR.
- Cancelou/remarcou no Calendly → a reunião antiga é cancelada no CRM (PR #127).
- Roda no relógio (`wesales-relogio.yml`) a cada 30 min, a qualquer hora e dia; manual: ação "WeSales - Calendly para o CRM" (dry-run por padrão).
- 1º caso: Robson Luiz Rufino de Sá, 29/09 20:00 — gravado e conferido.
- **29/09 manhã — mesmo link do Meet:** o Calendly e o CRM usam a mesma agenda do Google e cada um gerava o seu Meet (salas diferentes). Agora a reunião no CRM leva o link do convite do Calendly (`calendly.com/events/<uuid>/google_meet`), e as já gravadas são corrigidas a cada rodada. Robson e Ana Lucia corrigidos (HTTP 200).
- **29/09 — aviso especial à SDR (lead ouro):** workflow `Calendly — lead ouro (aviso à SDR)` (`41e97756`, `criar_calendly_ouro.py`), gatilho tag `calendly-ouro` que o robô põe depois de gravar; manda notificação interna à Andreyna (ligar, qualificar Q1–Q6, criar grupo) e tira a tag. Sem janela de horário. Disparado para Robson e Ana Lucia.
- Ana Lucia da Costa (reunião 29/09 18:00) entrou só com e-mail, sem telefone: não dá para ligar.
- **29/09 — fluxo real do lead (dono):** o lead preenche o formulário da Meta (nome, telefone, e-mail) e, na última etapa, marca no Calendly, que não pede telefone. No Calendly ele pode digitar outro e-mail → o robô criava contato duplicado sem telefone (Ana Lucia). Agora, sem e-mail/telefone igual, o robô casa pelo primeiro nome com o contato do Facebook criado nas 12 h antes do agendamento (só se for único; PR #130). Ana corrigida à mão: reunião no contato verdadeiro `Vzkkc1fBw0EeNbLl0nYo` (+55 21 99231-3658); duplicado `jSb91oLvb09rfOZbNmJY` com DND, `duplicado-calendly`, reunião cancelada, oportunidade abandoned, tarefas concluídas.
