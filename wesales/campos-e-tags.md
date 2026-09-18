# Etapas 2 e 3 — campos e tags para confirmar antes de criar

**Nada aqui foi criado.** Esta é a lista que eu executo depois da auditoria e
da sua confirmação, item por item. A auditoria pode cortar linhas desta lista
(campo que já existe é reaproveitado, nunca duplicado).

## Etapa 2 — Campos personalizados (42 + 1 sugerido)

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
| C-20 | Data conectado | DATE | — | Workflow (R-03) |
| C-21 | Data agendado | DATE | — | Workflow (R-03) |
| C-22 | Data compareceu | DATE | — | Workflow (R-03) |
| C-23 | Template usado | TEXT | código do template, ex. `M1-a` | Workflow (R-04) |
| C-24 | Nº de no-shows | NUMERICAL | — | Workflow (R-12) |

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

C-20 a C-22 fecham o funil por marco (`build-wesales.md`, seções 4, 5 e 5.2,
R-03 do roadmap): cada campo grava a data em que a oportunidade cruzou aquele
marco pela primeira vez — `Data conectado` no Pós-ligação, `Data agendado` no
Pós-agendamento, `Data compareceu` no comparecimento confirmado pelo
calendário. Pesquisado antes de desenhar: o GHL tem filtro nativo `Last Stage
Change Date`, mas ele só reflete a **etapa atual** — assim que o lead avança
para a etapa seguinte, o dado de quando ele passou pela etapa anterior se
perde, e o funil do mês subconta quem já avançou. Um carimbo próprio por
marco sobrevive ao avanço. `DATE` basta aqui (diferente de C-14/C-18/C-19):
a métrica é contagem por mês, não velocidade em minutos, e o filtro relativo
"neste mês" já existe nativamente para campo `DATE`. O quarto marco do
funil, "entraram", não ganha campo novo: usa o filtro nativo `Data de
criação` da oportunidade, que não muda quando o lead avança — o mesmo
problema do `Last Stage Change Date` não existe aqui porque criação é
imutável.

C-23 fecha a biblioteca de mensagens versionada (`build-wesales.md`, seção
2.6, R-04 do roadmap): grava o código do template que acabou de sair (ex.:
`M1-a`) toda vez que M1, M2 ou M3 dispara. **`TEXT`, não `SINGLE_OPTIONS`,
de propósito:** uma lista de opções fixa exige reabrir o campo na tela toda
vez que nasce uma versão nova — e o R-05 (teste A/B da M1, seção 2.6.1 do
`build-wesales.md`) já criou `M1-a`/`M1-b`, escritos pelos dois caminhos do
Split sem tocar no campo. `TEXT` deixa o workflow escrever qualquer código
novo sem depender de edição manual do campo; o custo é não ter validação de
valor digitado, que aqui é baixo porque só o workflow escreve neste campo,
nunca o SDR. Textos e códigos completos, versionados, ficam em
`biblioteca-mensagens.md`.

C-24 fecha o handoff de no-show (`build-wesales.md`, seções 5.3/5.4, R-12 do
roadmap): conta quantos no-shows seguidos o lead acumulou desde o último
comparecimento de verdade — a seção 5.2 zera este campo ao confirmar
`Showed`, e a seção 5.3 o incrementa a cada `No Show`, descartando a
oportunidade automaticamente a partir do 2º seguido (proteção de agenda do
closer). **`NUMERICAL`, não uma tag:** a lista 8.17 (`build-wesales.md`)
filtra direto pelo valor do campo, mesmo raciocínio já usado em C-06/C-07 —
uma tag só valeria a pena se algum portão precisasse checar "presente/
ausente" sem importar a contagem, o que não é o caso aqui.

**R-10 (distribuição de leads) não abre campo novo.** O roadmap sugeria um
campo `SDR responsável`; a especificação (`build-wesales.md`, seção 2.14)
reaproveita o campo nativo `Assigned User` (dono do contato), que o GHL já
expõe em filtro de Smart List e em ação de workflow (`Assign to User`) — um
campo personalizado espelhando a mesma informação divergiria na primeira
reatribuição feita direto na tela, o mesmo problema de "campo com dois
donos" que este documento já evita desde C-01 a C-23.

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

## Etapa 3 — Tags (14, todas criadas)

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
| T-12 | `atraso-1a-tentativa` | Alerta de speed-to-lead (R-02/R-07): aplicada pelo workflow da seção 2.11 do `build-wesales.md` quando o lead passa o tempo daquele relógio (varia por origem, seção 2.11 tem o valor certo) em `Em cadência` sem a T1 disparar; filtra a lista 8.8 |
| T-13 | `reengajamento-ativo` | Reengajamento 90 dias (R-08): aplicada pelo workflow da seção 2.12 do `build-wesales.md` enquanto o lead reativado roda a régua TR1-TR4; blinda o gatilho da Cadência 12x30 (seção 2.1) contra entrada dupla e filtra a lista 8.14 |
| T-14 | `pausado` | Regras de pausa (R-09): aplicada manualmente pelo SDR para represar as tentativas de **um** lead sem ser opt-out; checada no nó 2.5 (seção 2.4) e 1.5 (seção 2.10) do `build-wesales.md`, limpa pelo Mestre de saída (seção 3) e filtra a lista 8.15 |

Todas em minúsculas com hífen. O GHL normaliza tags para minúsculas, então
`Fila-Quente` e `fila-quente` são a mesma tag — o que ajuda a não duplicar.

**Executado em 18/09/2026.** As 14 saíram em duas chamadas de
`contacts_add-tags` sobre o mesmo contato de estrutura (`ZZ TESTE
ESTRUTURA`, `c5r3ZxiAd8T5adL1Bt6j`): as 11 originais na primeira rodada, e
T-12/13/14 nesta, depois de aprovadas ao vivo em chat (`APROVADO.md`) — não
tinham sido criadas antes porque tinham nascido em rodadas de roadmap
posteriores às 11 originais, cada uma numa linha própria de aprovação.

## O que eu preciso de você para executar

Ainda em aberto:

1. **L-02**: as opções do campo `Segmento`.
2. **S-01**: entra `Data do retorno` na lista? (recomendo sim)
3. **Q-09/Q-16**: LARGE_TEXT ou TEXT?

Já respondido: a subconta é `1D53YTI9C7oIMBavcQxV` e a permissão de criar
veio em 18/09/2026 ("tem todas as permissões") — é o que liberou a Etapa 3,
já entregue. A Etapa 2 não depende mais de resposta e sim da tela: campo
personalizado não sai por API, então a tabela acima é para copiar em
Configurações → Campos personalizados.
