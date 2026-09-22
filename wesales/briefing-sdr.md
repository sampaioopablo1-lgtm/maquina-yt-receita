# Briefing — operação de SDR na WeSales

Instruções guardadas em 18/09/2026. Fonte da verdade do projeto: quando algo
aqui divergir de um documento de execução, este arquivo manda.

## Contexto

Operação de SDR (pré-vendas B2B) na **WeSales**, white-label do
**GoHighLevel**. Objetivo: chegar o mais perto possível de uma plataforma de
sales engagement (Reev/Meetime) usando apenas recursos nativos do GHL.

Trabalhar sempre na subconta indicada pelo dono. Havendo mais de uma,
perguntar antes de agir.

## A máquina

- Cadência de **12 tentativas em 30 dias**, 3 canais: ligação por telefone,
  ligação por WhatsApp e mensagem de WhatsApp.
- Entrada: ~10 leads novos/dia. Meta do SDR: 100 ligações/dia.
- Filas do SDR são **listas inteligentes filtradas por TAG**, não por tarefa.
- Workflow adiciona a tag no dia/horário da tentativa e remove após o
  resultado. Antes de cada tentativa, verifica se o lead ainda está na etapa
  "Em cadência".
- Quando o lead atende, o SDR abre o link do calendário do closer (com
  formulário de qualificação anexado), qualifica e agenda na mesma tela.
- Mensagens de WhatsApp são automáticas (IA). O SDR só liga e classifica.
- Regra encadeada: telefone não atendido -> tarefa/tag de ligação por
  WhatsApp -> se não atender -> mensagem automática.

## Distribuição da cadência

| Dia | Canais |
|---|---|
| D1 | telefone + mensagem (com pedido de permissão de ligação) + WhatsApp |
| D2 | telefone + WhatsApp |
| D4 | WhatsApp |
| D7 | telefone + WhatsApp |
| D10 | telefone + mensagem |
| D14 | WhatsApp |
| D20 | telefone |
| D30 | telefone + WhatsApp + mensagem de encerramento |

Regras:
- Sem permissão de WhatsApp -> vira telefone.
- 2 ligações de WhatsApp seguidas sem atender -> vira telefone.
- Respondeu/atendeu em qualquer canal -> sai da cadência.

## Regras de trabalho (invioláveis)

1. **NUNCA** excluir contatos, campos, tags ou workflows existentes.
2. Antes de qualquer criação ou alteração em massa, listar o que será feito e
   pedir confirmação.
3. Campo ou tag com nome parecido já existente: avisar e perguntar se
   reaproveita, em vez de criar duplicado.
4. Operação não suportada pelo MCP: dizer claramente e incluir o passo a
   passo manual no documento.
5. Trabalhar em etapas, mostrando o resultado de cada uma antes de seguir.
6. Responder em português do Brasil, com tabelas quando ajudar.

## Etapas do projeto

| Etapa | O que é | Estado |
|---|---|---|
| 1 | Auditoria somente leitura (pipelines, campos, tags, workflows, calendários, formulários) | **Entregue** — plano em `auditoria-etapa1.md`, resultado em `auditoria-resultado.md` |
| 2 | Criar campos personalizados que faltam | **Só na tela, com este conector** — a API oficial da HighLevel tem endpoint de criação (`APRENDIZADOS-CRM.md`), o conector `GHL CRM` não o expõe. Lista com tipo e opções em `campos-e-tags.md` |
| 3 | Criar as tags | **Entregue por API em 18/09/2026** — as tags do projeto (`campos-e-tags.md`) estão na subconta |
| 4 | Especificação do que é manual (`build-wesales.md`) | **Entregue** |
| 5 | Prompt da rotina horária de manutenção | **Entregue** (`rotina-limpar-tarefas.md`) |

## Decisões tomadas por mim (revise, são reversíveis)

Numeradas para você responder só o número que quiser mudar.

**D-01 — Quais são as 12 tentativas.** Contei como tentativa apenas o que o
SDR faz (ligação por telefone ou por WhatsApp). As 3 mensagens automáticas
(D1, D10, D30) não entram na contagem. Isso fecha exatamente 12 tentativas
nos dias do briefing e é coerente com "o SDR só liga e classifica".

**D-02 — Horários.** Janela 08:30–18:30, dias úteis, fuso da subconta.
Alternei manhã e tarde entre tentativas do mesmo lead. Tabela completa em
`build-wesales.md`.

**D-03 — Ordem no D1.** Mensagem primeiro (08:45), depois telefone (10:30),
depois ligação por WhatsApp (16:10). Motivo: a mensagem é que pede permissão
de ligação, então ela precisa vir antes.

**D-04 — "Sem permissão de WhatsApp".** Interpretei a regra como valendo para
a *ligação* por WhatsApp: só liga por WhatsApp se `Permissão WhatsApp = Sim`;
com `Não` ou `Não solicitado`, a tentativa vira telefone. As *mensagens*
continuam saindo (salvo `nao-perturbe`). **Atenção:** se "Não solicitado"
também bloquear, quase toda a cadência vira telefone, porque a permissão só
chega depois da resposta do lead. Confirme.

**D-05 — Nota de qualificação.** Escala 0–100 em 3 blocos (Fit 30, Maturidade
de mídia 25, BANT 45). Regras em `build-wesales.md`, seção 9.

**D-06 — Reentrada no workflow de cadência.** Desligada, com rodada 2 manual.
Reentrada ligada duplica tentativas quando o lead volta para "Em cadência".

## Lacunas que encontrei no desenho (não criei nada)

| # | Lacuna | Por que importa | Sugestão |
|---|---|---|---|
| L-01 | ~~Não existe campo de **data/hora do retorno**~~ — **campos criados; virou fiação em 22/09/2026** | A lista inteligente "Retornos" não tinha como ordenar nem filtrar "retorno de hoje"; a tarefa `[RETORNO]` não tinha vencimento correto | **Os dois campos existem na tela:** `Data de retorno` (`DATE`, 18/09) e `Hora do retorno` (`TEXT`, `HH:MM`, 21/09 23:18) — `CONFERENCIA-CAMPOS.md`, Tabela K. Resta ligar: o nó 4/4b do ramo `Pediu retorno` (`build-wesales.md`, seção 4) e a ordenação da lista `Retornos` (seção 8.4) |
| L-02 | ~~`Segmento` é lista, mas as opções não foram definidas~~ — **resolvida sozinha** | Não consigo criar o campo sem os valores | **Fechada:** quem montou os campos na tela (Fase 2) criou `Segmento` como `TEXT` livre em vez de lista fechada — não precisa mais de opções definidas (`campos-e-tags.md`, Q-01) |
| L-03 | Tag `fila-linkedin` existe no escopo, mas LinkedIn não está nos 3 canais da cadência | Ou a cadência tem um 4º canal, ou a tag nasce órfã | Confirmar se é reserva para depois |
| L-04 | `cad-inbound` / `cad-outbound` sem cadência inbound especificada | Inbound pede cadência mais curta e mais rápida (minutos, não dias) | Definir depois; a tag já separa |
| L-05 | Volume: 10 leads/dia × 12 tentativas = ~120 tentativas/dia em regime, acima da meta de 100 | Com saída antecipada (~35% conectam ou saem antes), cai para ~78–90/dia | Para bater 100 ligações/dia com folga, a entrada precisa ser ~11–13 leads/dia |
| L-06 | Não há campo de **origem/lista** do lead além das tags de cadência | Dificulta diagnosticar qual fonte converte | Opcional: `Origem do lead` (lista) |
| L-07 | Não existe gatilho que promova `NOVO LEAD` → `CONECTAR` | Hoje é decisão manual do SDR ao revisar a fila; descoberta ao fechar o R-08 (reengajamento), que por isso move o lead reativado direto para `CONECTAR` em vez de parar em `NOVO LEAD` | **Escalado em 21/09/2026 (`ROADMAP-SALES-ENGAGEMENT.md`, G-03): o volume já chegou** — 47 oportunidades reais paradas em `NOVO LEAD` — **envelhecendo, não crescendo**: medido em 22/09/2026, zero lead novo em mais de 22 horas e subindo (F-10 no roadmap; o número original do F-10 dizia ~46h por erro de conta, corrigido no mesmo dia). Três opções escritas para o dono escolher; nenhuma executada ainda |
| L-08 | ~~Etapa `Conectado` não tem caminho para desqualificação **na hora**~~ — **resolvida em 21/09/2026** | Descoberta ao aplicar o bloco "Motivos de Perda" do Sales Model Canvas etapa a etapa (seção 1); sem esse caminho, o SDR ou força um agendamento sem fit (polui a agenda do closer) ou improvisa uma saída manual que a régua de nota (seção 9) não registra como perda | **Fechada:** `ROADMAP-SALES-ENGAGEMENT.md`, R-18 — nova opção `Desqualificado` em `Resultado da tentativa` (C-02) e ramo próprio no Pós-ligação (`build-wesales.md`, seção 4), que sai por `status` sem passar por `AGENDAR` nem abrir tarefa de agendamento. Falta só a criação manual na tela (opção de campo + ramo de workflow não saem por API) |
| L-09 | ~~Lead nativo do Meta Lead Ads vira **contato**, mas não vira **oportunidade** em `FUNIL DE VENDAS`~~ — **resolvido em 19/09/2026** | Toda a máquina (cadência, interceptação de sinal, tudo) é construída em cima de etapa de oportunidade | **Fechado:** workflow "Porta de Entrada" (`build-wesales.md`, seção 1.3) montado e publicado na tela; confirmado por `opportunities_search-opportunity` que `FUNIL DE VENDAS` foi de 0 para **40 oportunidades, todas em `NOVO LEAD`** — os 40 contatos existentes (backfill) e qualquer novo dali pra frente |
| L-09b | ~~Nada na especificação criava oportunidade~~ — **resolvido em 19/09/2026** | — | **Fechado junto com o L-09.** Continua cruzando com L-07 (promoção `NOVO LEAD` → `CONECTAR`), que "Porta de Entrada" não resolve de propósito — isso segue aberto |

## Estado do acesso

**Desatualizado — mantido por histórico.** Escrito antes da primeira
conexão real; hoje o conector `GHL CRM` (MCP oficial da LeadConnector, 36
ferramentas) está presente e é o que a rotina usa desde `auditoria-resultado.md`.
Cobertura de leitura/escrita medida nele: `auditoria-resultado.md`.

O caminho **HighLevel via Composio**, cogitado aqui na primeira rodada,
segue não testado — nenhuma conta HighLevel está conectada por Composio
nesta sessão (confirmado em 18/09/2026, `APRENDIZADOS-CRM.md`). Ele voltou
a importar por outro motivo: a API oficial da HighLevel permite criar campo
personalizado e calendário (o conector `GHL CRM` atual não implementa
essas duas chamadas), e o toolkit Composio é a rota mais provável para
fechar esse gap sem esperar a HighLevel mudar nada — mas conectar exige um
fluxo de OAuth que só o dono da conta autoriza, então fica registrado como
opção, não como ação já tomada.
