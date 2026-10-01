
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

## 30/09 noite — por que NENHUMA mensagem automática saía desde 28/09

- **Causa provada: janela de horário do workflow + envio de mensagem = trava para sempre.** Com `window` preenchido, o passo de SMS/WhatsApp espera a janela e nunca é retomado — mesmo dentro do horário (leads de segunda 14:45 BRT presos). Passos de nota/campo NÃO são afetados (o "Registro da ligação" gravava nota fora da janela dele).
- Prova: a MI-0 (`02511c72`) tinha 16 leads parados em "Espera 2 min" (status `wait_finished`). Janela retirada às 20:36 → o lead seguinte recebeu a MI-0 às 20:37 e respondeu às 20:38. Antes disso, renumerar o `order` dos nós (hipótese 1) NÃO resolveu: o contato de teste ficou preso igual.
- **Janela retirada dos 19 workflows publicados que a tinham** (backups `bkp_janela/` no scratchpad da sessão). O horário comercial do WhatsApp de prospecção segue garantido pelo `wa_governador.py` (só libera `wa-liberado` 08:30–18:30 seg–sex). Mensagens fora do governador (lembretes, MI-0, nutrição) agora podem sair a qualquer hora.
- **REGRA: nunca pôr `window` em workflow pela API.** Se precisar de horário, use o governador ou um passo de espera/condição de horário.
- **Histórico de inscrições pela API:** `GET backend.leadconnectorhq.com/workflows/status/search/workflow-with-filter?workflowId=&locationId=&action=first&limit=100` e `/workflows/status/search/count-per-step?...`. Exigem os headers da sessão da tela (capturar no Playwright com `storage-state.json`); o cliente `ghl_api` recebe vazio. Status úteis: `wait_finished` parado após espera, `step` parado num passo, `finished`.
- `wa-liberado` pendurado em 20 contatos (o Promover põe de propósito para a 1ª mensagem; a Inbound travada não tirava) — retirado.
- Logs das 312 rodadas antigas dos robôs do CRM apagados no Actions (expunham dados de lead antes do `privacidade.py`).
- Leads presos antes da correção NÃO foram reenviados (a MI-0 diz "recebi seu cadastro agora"); seguem com a SDR.

## 01/10 — "Confirmar reunião" sai da Minha fila quando a SDR registra "Atendeu"

- **Problema:** o lead de nível 10 "Confirmar reunião" seguia no topo depois de confirmado. A tag `confirmar-reuniao` só saía no `ordem_fila.py` (seg–sex 07:30–21:00) e o `reunioes_robo.py` a recolocava a cada rodada, porque só olhava se a tarefa existia, não se estava concluída.
- **Correção:** `finalizar_tarefas.py` tira a tag na mesma hora em que fecha a tarefa de confirmação (ligação de 25 s ou mais, ou Registro da ligação "Atendeu"), a qualquer hora. `reunioes_robo.py` não recoloca a tag quando a tarefa da reunião já está concluída.
- **Tarefa de confirmação de reunião que já começou** (ou saiu de "confirmed") fecha sozinha no `reunioes_robo.py`: a ação não tem mais como ser feita e a tarefa ficava aberta para sempre.
- **Medido:** ligação de confirmação de 24 s registrada como "Caixa postal"/"Pediu retorno" NÃO confirma. Para o lead sair, o registro tem de ser "Atendeu". Prazo: até 30 min (uma rodada do relógio).

## 01/10 — Minha fila só mostra quem tem ligação a fazer hoje (pedido do dono)

- **Medido:** 25 leads na lista; 12 estavam em dia de toque por WhatsApp (`fila-wa`) e apareciam mesmo assim, porque a lista aceitava `fila-quente` — que todo lead recebe na entrada (Promover) e quase nunca perde — e a regra "2+ tentativas sem conexão". A SDR podia ligar antes do dia do toque.
- **Filtro novo da lista (`jB9TeEuL9X7mupxwJqde`):** em CONECTAR, sem `status-perdido`/`nao-perturbe`/`falou-hoje`, e com `fila-tel` OU `fechar-horario` OU `retorno-vencido`; mais os grupos `confirmar-reuniao` e `fila-noshow`. Saíram `fila-quente` e a regra das tentativas. Backup em `.local/minha-fila-antes-01-10.json`.
- **`atuador_filas.py` (fila-tel completa):** a trava de 2 h virou "no máximo 1 ligação por dia"; `fila-quente` sozinha só vira ligação se ninguém ligou ainda ou se o lead respondeu/ligou depois da última ligação. Teto de 12 tentativas.
- **`ordem_fila.py` (toque pendente):** a Cadência Inbound tira `fila-tel` 25 min depois do toque. Quem tem tarefa de ligação aberta e sem ligação depois dela volta para a fila até a ligação ser feita (mesma regra do `finalizar_tarefas.py`). A coluna Próxima ação só diz "Fechar horário" para quem tem `fechar-horario`.
- **Cadência Inbound v31:** retirado o "Não atendeu" automático (10 nós: gravar Resultado + `limpar-tarefas`) dos toques TI1–TI5. A cadência segue andando; o resultado e a tarefa passam a depender de ligação real.
- **Lembretes da Reunião v3 (v6):** as 4 mensagens "H-3 dor" ganharam o link da reunião.
- **Leads presos de antes da retirada da janela:** 6 parados em "WA · limpar marcas" da Inbound receberam `sem-cadencia` (ligação diária pelo atuador, sem WhatsApp automático) e saíram da inscrição travada. Os 34 `queued_to_continue` de 24/09 já eram `sem-cadencia`.
- **Histórico de inscrições dos 55 publicados lido** (rota da tela, `st.js`): fora Inbound e MI-0, só 1 inscrição presa (Reunião Cancelada, contato já perdido).
- **Remarcação no Calendly (corrigida):** antes, o robô criava a reunião nova e cancelava a antiga na mesma rodada; a "Reunião Cancelada" tirava o contato dos Lembretes (inclusive da nova) e mandava "vi que a reunião foi cancelada". Agora `calendly_para_crm.py` cancela ANTES de criar; se o Calendly marca o convidado cancelado como `rescheduled`, põe a tag `calendly-remarcou` antes do cancelamento e só cria a reunião nova na rodada seguinte (tirando a tag). A "Reunião Cancelada" (`37ee2c13`, v9, 26 nós) ganhou a guarda "Lead só remarcou pelo Calendly?": com a tag, sai dos lembretes antigos e para, sem WhatsApp, tarefa ou nota. Testado com Calendly e CRM simulados (2 rodadas); falta ver uma remarcação real.

## 01/10 — CRM sem Supabase (regra do dono: rotina do CRM fica no GitHub)

- Único ponto do CRM que ainda apontava para o Supabase: o envio do `log_eventos.py` para `opc.crm_eventos` (função `crm-eventos`). Retirado. A tabela nunca recebeu linha (a cota barrava).
- O log vive só no repositório PRIVADO `opc-crm-dados` (`eventos/AAAA-MM-DD.jsonl.gz`), gravado pelo `wesales-log.yml`. O histórico de 17/09 a 28/09, que estava só no PC, foi enviado para lá: 15 dias no total.
- Nenhum outro robô ou workflow do CRM lê ou grava no Supabase (busca em `wesales/` e nos `wesales-*.yml`).
- **Removido do Supabase (01/10, a pedido do dono):** tabela `opc.crm_eventos` apagada (0 linhas, sem dependentes); funções `crm-eventos` e `painel-sdr` (painel externo aposentado em 27/09; 0 chamadas em 24 h) trocadas por uma resposta 410 com JWT obrigatório — o conector não apaga função, isso só se faz no painel do Supabase. Token local `_opc_log_token.txt` apagado.
- **Toque já feito sai da fila (01/10 tarde):** a Cadência Inbound deixa `fila-tel` por 22 h a 2 dias depois do toque; sem Resultado registrado, o lead ligado ontem reaparecia hoje. `ordem_fila.py` (`solta_toque_feito`) tira `fila-tel` de quem já recebeu ligação e não tem tarefa de ligação pendente, não voltou a falar, não é fechar horário/retorno vencido; lead `sem-cadencia` sai se a ligação tem menos de 24 h (o atuador devolve depois). Decisão do dono: NÃO criar bloco de "reforço" para bater 100 ligações agora; a base passa de 100 leads em ~2 dias e a lista do dia cresce sozinha. Reavaliar então (ideia guardada: reforço no fim da lista, teto de 2 ligações/dia por lead com 4 h de intervalo).
