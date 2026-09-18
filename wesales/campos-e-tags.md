# Etapas 2 e 3 — campos e tags para confirmar antes de criar

**Nada aqui foi criado.** Esta é a lista que eu executo depois da auditoria e
da sua confirmação, item por item. A auditoria pode cortar linhas desta lista
(campo que já existe é reaproveitado, nunca duplicado).

## Etapa 2 — Campos personalizados (37 + 1 sugerido)

> **Onde mora a contagem.** Só este título conta campos, e só ele. Os títulos
> de seção perderam o número de propósito: eram quatro lugares para errar cada
> vez que um campo nasce, e já erraram. Quem quiser saber quantos tem numa
> seção, conta as linhas da tabela — que é a verdade, não um resumo dela.

Todos no objeto **contato**. Tipo é o `dataType` da API do GHL.

### Controle da cadência

| # | Nome | Tipo | Opções | Quem escreve |
|---|---|---|---|---|
| C-01 | Tentativa nº | NUMERICAL | — | Workflow |
| C-02 | Resultado da tentativa | SINGLE_OPTIONS | Atendeu, Caixa postal, Não atendeu, Número errado, Pediu retorno, Não ligar | SDR |
| C-03 | WA não atendidas seguidas | NUMERICAL | — | Workflow |
| C-04 | Permissão WhatsApp | SINGLE_OPTIONS | Sim, Não, Não solicitado | IA / SDR |
| C-05 | Prioridade | NUMERICAL | 1 a 5 | Workflow |
| C-06 | Total de ligações | NUMERICAL | — | Workflow |
| C-07 | Total de conexões | NUMERICAL | — | Workflow |
| C-08 | Nota de qualificação | NUMERICAL | 0 a 100 | Workflow |
| C-09 | Tentativas telefone | NUMERICAL | — | Workflow (R-01) |
| C-10 | Tentativas WhatsApp | NUMERICAL | — | Workflow (R-01) |
| C-11 | Conexões telefone | NUMERICAL | — | Workflow (R-01) |
| C-12 | Conexões WhatsApp | NUMERICAL | — | Workflow (R-01) |
| C-13 | Sinal recebido | SINGLE_OPTIONS | Clique em link, Resposta de mensagem | Workflow (F-01) |
| C-14 | Data e hora do sinal | TEXT | `AAAA-MM-DD HH:MM` | Workflow (F-01) |
| C-15 | Reunião foi qualificada | SINGLE_OPTIONS | Sim, Não, Parcial | Closer (F-03) |
| C-16 | Motivo da desqualificação | SINGLE_OPTIONS | Sem fit, Sem budget, Timing errado, Não é decisor, Concorrente, Duplicado ou já cliente | Closer (F-03) |
| C-17 | Data do veredito do closer | DATE | — | Workflow (F-03) |
| C-18 | Entrada em | TEXT | `AAAA-MM-DD HH:MM` | Workflow (R-02) |
| C-19 | 1ª tentativa em | TEXT | `AAAA-MM-DD HH:MM` | Workflow (R-02) |

C-09 a C-12 abrem `Total de ligações`/`Total de conexões` (C-06/C-07) por
canal — sem eles não dá para responder "a T7 do telefone conecta mais que a
do WhatsApp?", que é a pergunta do R-01 do roadmap. Escritos pelo Pós-ligação
(`build-wesales.md`, seção 4, nós 2 e o ramo `Atendeu`); a lista inteligente
que os lê é a 8.6.

C-13 e C-14 alimentam a interceptação de sinal (`build-wesales.md`, seção 2.9,
F-01 do roadmap): registram que tipo de sinal furou a fila e quando, para o
SDR ver na nota do contato e para uma futura auditoria (bloco F-05) conseguir
provar que o sinal foi atendido a tempo. **Atenção de tipo:** como o campo
**Medido em 18/09/2026:** campo `DATE` do GHL guarda **só a data** — a hora é
descartada até quando se envia ISO completo pela API, e não existe tipo
DateTime para campo de contato. Por isso `Data e hora do sinal` (C-14) é
`TEXT` no formato `AAAA-MM-DD HH:MM`, e `Data do retorno` (S-01) virou par:
`DATE` para filtrar e vencer tarefa, `TEXT` para a hora combinada.

C-15 e C-16 fecham o loop do closer (`build-wesales.md`, seção 5.1, F-03 do
roadmap): o closer registra se a reunião que o SDR agendou tinha fit de
verdade, e por quê quando não teve. É o único par deste documento preenchido
por um papel que a coluna "Quem escreve" ainda não tinha: nem SDR, nem
workflow, nem IA.
C-17 é `DATE`, não `TEXT`: nada aqui mede minutos (diferente de C-14), só
"em que dia o closer deu o veredito", então a granularidade de dia do `DATE`
basta e evita outro par de campos como o de C-14/S-01.

C-18 e C-19 medem speed-to-lead (`build-wesales.md`, seção 2.11, R-02 do
roadmap): `Entrada em` grava quando o lead entra em `Em cadência` (nó 0.6 da
Cadência 12x30), `1ª tentativa em` grava quando a T1 dispara de verdade (nó
5c, só na primeira tentativa). Mesmo motivo de C-14: `TEXT` porque a métrica
é em minutos e `DATE` descarta a hora.

### Qualificação — BANT + diagnóstico

| # | Nome | Tipo | Opções |
|---|---|---|---|
| Q-01 | Segmento | SINGLE_OPTIONS | **pendente — L-02, preciso da lista** |
| Q-02 | Site | TEXT (URL) | — |
| Q-03 | Instagram | TEXT | — |
| Q-04 | Clientes novos por mês | SINGLE_OPTIONS | Até 10, 11-30, 31-100, 100+ |
| Q-05 | Investe em anúncios | SINGLE_OPTIONS | Sim, Já investiu e parou, Nunca |
| Q-06 | Investimento mensal em anúncios | SINGLE_OPTIONS | Até 1 mil, 1-5 mil, 5-15 mil, 15 mil+ |
| Q-07 | Plataformas de anúncio | MULTIPLE_OPTIONS | Meta, Google, TikTok, Outras |
| Q-08 | Já teve agência | SINGLE_OPTIONS | Tem hoje, Já teve, Nunca |
| Q-09 | Experiência com agência | LARGE_TEXT | — |
| Q-10 | Tem time comercial | SINGLE_OPTIONS | Só o dono, 1-2 pessoas, 3-5, 6+ |
| Q-11 | Quem atende os leads | SINGLE_OPTIONS | Dono, Vendedor, SDR, Ninguém fixo |
| Q-12 | Usa CRM | TEXT | — |
| Q-13 | Canal principal de venda | SINGLE_OPTIONS | WhatsApp, Telefone, Loja, Online |
| Q-14 | Budget | SINGLE_OPTIONS | Tem, Precisa aprovar, Não tem |
| Q-15 | Decisor | SINGLE_OPTIONS | É o decisor, Influencia, Não decide |
| Q-16 | Dor principal | LARGE_TEXT | — |
| Q-17 | Prazo | SINGLE_OPTIONS | Agora, Até 30 dias, 1-3 meses, Sem prazo |
| Q-18 | Qualificação preenchida por | SINGLE_OPTIONS | SDR, IA WhatsApp, Automático |

Observações de tipo:
- **Q-02 Site**: o GHL não tem `dataType` URL. Vai como TEXT com placeholder
  `https://`. Se preferir validação, o campo do formulário pode ser marcado
  como website na tela.
- **Q-09 e Q-16**: você pediu "texto". Usei LARGE_TEXT porque é resposta de
  entrevista e TEXT corta em uma linha. Diga se prefere TEXT.

### Sugerido por mim — não crio sem seu ok

| # | Nome | Tipo | Por que |
|---|---|---|---|
| S-01 | Data do retorno | DATE + `Hora do retorno` (TEXT) | Sem ele a lista "Retornos" não filtra "hoje" e a tarefa `[RETORNO]` não tem vencimento (lacuna L-01). São dois campos porque `DATE` no GHL descarta a hora |

## Etapa 3 — Tags (11 + 1 sugerida)

| # | Tag | Função na máquina |
|---|---|---|
| T-01 | `fila-quente` | Lista inteligente Fila Quente (Prioridade ≥ 4) |
| T-02 | `fila-tel` | Tentativa de telefone liberada hoje |
| T-03 | `fila-wa` | Tentativa de ligação por WhatsApp liberada hoje |
| T-04 | `fila-linkedin` | Reserva — hoje sem canal na cadência (lacuna L-03) |
| T-05 | `conectado-hoje` | Tira o lead das filas do dia após conexão |
| T-06 | `nao-perturbe` | Portão de segurança em toda tentativa |
| T-07 | `limpar-tarefas` | Fila da rotina horária de manutenção |
| T-08 | `nutricao-90d` | Saída branda, volta depois |
| T-09 | `telefone-invalido` | Portão das tentativas de telefone |
| T-10 | `cad-inbound` | Origem: inbound |
| T-11 | `cad-outbound` | Origem: outbound |

Todas em minúsculas com hífen. O GHL normaliza tags para minúsculas, então
`Fila-Quente` e `fila-quente` são a mesma tag — o que ajuda a não duplicar.

### Sugerida por mim — não crio sem seu ok

| # | Tag | Função na máquina |
|---|---|---|
| T-12 | `atraso-1a-tentativa` | Alerta de speed-to-lead (R-02): aplicada pelo workflow da seção 2.11 do `build-wesales.md` quando o lead passa 1h em `Em cadência` sem a T1 disparar; filtra a lista 8.8 |

T-12 não está na lista das 11 aprovadas em `APROVADO.md` — criação por API
fica parada até você trocar `[ ]` por `[x]` numa linha própria para ela (o
formato do arquivo já reserva espaço para isso: uma linha por tag/lote,
como as 11 originais). Tag criada sem aprovação explícita quebraria a regra
2 do briefing, mesmo sendo tecnicamente igual de simples que as outras 11.

## O que eu preciso de você para executar

1. **Subconta**: qual (se houver mais de uma, eu listo e você escolhe).
2. **L-02**: as opções do campo `Segmento`.
3. **S-01**: crio `Data do retorno`? (recomendo sim)
4. **Q-09/Q-16**: LARGE_TEXT ou TEXT?
5. Confirmação de que posso criar o que a auditoria mostrar que não existe.

Com isso, Etapas 2 e 3 saem numa rodada, e eu te devolvo a tabela do que foi
criado, do que foi reaproveitado e do que falhou.
