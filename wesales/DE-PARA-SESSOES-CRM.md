
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

## 29/09 manhã — menos cliques para a SDR + log de eventos

- **Registro da ligação em 1 campo:** campo novo `Registro da ligação` (`2iqHW8jbd41AI6fZJr6P`, primeiro da pasta da ficha), opções "Telefone · Atendeu" … "Desqualificado". O workflow `Registro da ligação — 1 campo` (`9f70fac2`, 50 nós, `tools/criar_registro_1_campo.py` na branch abertura) grava Canal + Resultado e limpa o campo; o Pós-ligação v3 dispara como antes. Testado no contato ZZ TESTE: em 20 s o Resultado virou "Não atendeu" e Tentativas WhatsApp foi de 0 para 1. Canal/Resultado à mão seguem valendo como reserva.
- **Pasta de campo por API interna FUNCIONA:** `PUT backend…/locations/{loc}/customFields/{id}` com `parentId` + `position` (sem `picklistOptions`, com `options`). Corrige a conclusão de `pastas_de_campo.py`, que só testou a API pública.
- **Qualificação pré-preenchida:** `tools/preencher_qualificacao.py` no relógio (a qualquer hora). Urgência → Q6 Prazo, Investimento → Investe em anúncios, Necessidade → Q1 Dor. Vocabulário fechado, só campo vazio. A derivação de 27/09 tinha sido única: 13 leads novos estavam sem ela. 47 contatos preenchidos (PR #133).
- **Log de eventos:** `tools/log_eventos.py` (PR #134) lê o log de auditoria do CRM (`services…/audit/search/v2`, só com token de SESSÃO; o PIT dá 401) e as ligações/mensagens (PIT). Normaliza origem pessoa/workflow/robo/sistema/lead, sem texto de mensagem. Guarda em `.local/eventos/` (fora do git: o repositório é PÚBLICO) e envia para `opc.crm_eventos` pela função `crm-eventos` (token em `.local/_opc_log_token.txt`). Série desde 17/09, com ~3,6 mil eventos.
- **Bloqueios:** (1) a organização do Supabase está com `exceed_storage_size_quota`: funções retornam 402 nos dois projetos, então o envio ao banco espera; (2) o log de auditoria na nuvem precisa do segredo `GHL_STORAGE_STATE` + `OPC_LOG_TOKEN`. Até lá, coletar do PC; o CRM guarda 60 dias.
- **Achado do log:** de 17/09 a 29/09, nenhum Resultado da tentativa foi marcado por pessoa (todos vieram de workflow/robô), e as conversas mostram 2 ligações registradas, ambas do dono. A SDR quase não aparece no log. Conferir com ela como está ligando e registrando.
