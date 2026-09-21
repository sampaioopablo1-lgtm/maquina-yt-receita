# Etapas 2 e 3 — campos e tags para confirmar antes de criar

**Nada aqui foi criado.** Esta é a lista que eu executo depois da auditoria e
da sua confirmação, item por item. A auditoria pode cortar linhas desta lista
(campo que já existe é reaproveitado, nunca duplicado).

## Etapa 2 — Campos personalizados (44 + 1 sugerido)

> **Onde mora a contagem.** Só este título conta campos, e só ele. Os títulos
> de seção perderam o número de propósito: eram quatro lugares para errar cada
> vez que um campo nasce, e já erraram. Quem quiser saber quantos tem numa
> seção, conta as linhas da tabela — que é a verdade, não um resumo dela.

Todos no objeto **contato**. Tipo é o `dataType` da API do GHL.

### Controle da cadência

| # | Nome | Tipo | Opções | Quem escreve |
|---|---|---|---|---|
| C-01 | Tentativa nº | NUMERICAL | — | Workflow |
| C-02 | Resultado da tentativa | SINGLE_OPTIONS | Atendeu, Caixa Postal, Não atendeu, Número errado, Pediu retorno, Não ligar | SDR |
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
| C-25 | Hora da conexão | TEXT | `HH`, 00 a 23 | Workflow (F-02) |
| C-26 | Toques na semana | NUMERICAL | — | Workflow (F-04) |

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
`TEXT` no formato `AAAA-MM-DD HH:MM`, e `Data de retorno` (S-01, nome real
da tela) virou par: `DATE` para filtrar e vencer tarefa, `TEXT` para a hora
combinada.

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

C-26 fecha o teto de toques por semana (`build-wesales.md`, seção 2.19, F-04
do roadmap): conta, numa janela móvel de 7 dias corridos, quantos toques
(tarefa de ligação criada ou mensagem automática enviada) o lead recebeu —
somado por um nó `Math +1` a cada toque e descontado por um `Math -1` 7 dias
depois pelo workflow "Contador de Toques". `NUMERICAL`, mesmo raciocínio já
usado em C-06/C-07/C-09 a C-12: é contado por `Math`, não lido por SDR nem
por IA, então uma tag "presente/ausente" não bastaria — o portão de
frequência (seção 2.4, nó 2.5c) compara contra um número, não contra
presença.

C-25 fecha o horário aprendido por segmento (`build-wesales.md`, seção 2.18,
F-02 do roadmap): grava só a **hora** (não o carimbo completo) em que o lead
`Atendeu`, para cruzar com `Segmento` (Q-01) numa lista e enxergar se um
segmento conecta mais de manhã e outro à tarde. **`TEXT` de duas casas
(`HH`), não `NUMERICAL` nem o carimbo `AAAA-MM-DD HH:MM` que C-14/C-18/C-19
usam:** aqui ninguém mede minutos entre dois eventos (o que pediria
`TEXT` completo, R-02) nem soma o valor (o que pediria `NUMERICAL`, como
C-06 a C-12) — o campo só precisa ser lido e comparado por um humano numa
lista, por segmento, e uma string de duas casas evita o risco que o próprio
projeto já registrou com `Conexões telefone` (C-11): um `NUMERICAL` criado
errado na tela quebra a ação `Math` sem avisar; um `TEXT` não tem esse jeito
de quebrar porque nenhum nó soma nele.

**R-10 (distribuição de leads) não abre campo novo.** O roadmap sugeria um
campo `SDR responsável`; a especificação (`build-wesales.md`, seção 2.14)
reaproveita o campo nativo `Assigned User` (dono do contato), que o GHL já
expõe em filtro de Smart List e em ação de workflow (`Assign to User`) — um
campo personalizado espelhando a mesma informação divergiria na primeira
reatribuição feita direto na tela, o mesmo problema de "campo com dois
donos" que este documento já evita desde C-01 a C-23.

**R-13 (higiene de base) não abre campo nem tag nova.** O portão 0.0/0.0b
das seções 2.3 e 2.10 e o workflow opcional da seção 2.16 (`build-wesales.md`)
reaproveitam `telefone-invalido` (T-09, já existente) e o campo nativo
`Phone` — o mesmo raciocínio de "não duplicar o que o GHL já expõe" do
parágrafo do R-10 acima, agora aplicado a tag em vez de campo: a tag já
significava "não dá para ligar nesse número", e cobrir "não tem número
nenhum" com a mesma tag é extensão de significado, não invenção de um
segundo estado.

### Qualificação — BANT + diagnóstico

| # | Nome | Tipo | Opções |
|---|---|---|---|
| Q-01 | Segmento | TEXT | livre — **resolve a L-02**: a tela criou como texto livre em vez de esperar a lista fechada de segmentos |
| Q-02 | Site | TEXT (URL) | — |
| Q-03 | Instagram | TEXT | — |
| Q-04 | Clientes novos por mês | SINGLE_OPTIONS | 10, 11-30, 31-100, +101 |
| Q-05 | Investe em anúncios | SINGLE_OPTIONS | Sim, Já investiu e parou, Nunca |
| Q-06 | Investimento mensal em anúncios | SINGLE_OPTIONS | Até 1k, 1k a 5k, 5k a 10k, Acima de 10k |
| Q-07 | Plataformas de anúncio | SINGLE_OPTIONS **— deveria ser MULTIPLE_OPTIONS** | Meta, Google, Tiktok, Outros — tipo errado ainda não corrigido na tela, ver `CONFERENCIA-CAMPOS.md` Tabela A |
| Q-08 | Já teve agência? | SINGLE_OPTIONS | Tem hoje, Já teve, Nunca teve |
| Q-09 | Experiência com agência | TEXT | — |
| Q-10 | Tem time comercial | SINGLE_OPTIONS | Só dono, 1-5, 6-10, +10 |
| Q-11 | Quem atende os leads | SINGLE_OPTIONS | Dono, Vendedor, SDR, Ninguém fixo |
| Q-12 | Usa CRM | SINGLE_OPTIONS | Sim, Não |
| Q-13 | Canal principal de venda | SINGLE_OPTIONS | WhatsApp, Telefone, Loja, Online |
| Q-14 | Budget | SINGLE_OPTIONS | Tem, Precisa aprovar, Não tem |
| Q-15 | Decisor | SINGLE_OPTIONS | Sim, Influencia, Não decide |
| Q-16 | Dor principal | TEXT | — |
| Q-17 | Prazo | SINGLE_OPTIONS | Pra ontem, Espera 30 dias, Este ano, Sem prazo |
| Q-18 | Qualificação | SINGLE_OPTIONS | SDR, IA Whatsapp, Vendedor |

Observações de tipo:
- **Q-02 Site**: o GHL não tem `dataType` URL. Vai como TEXT com placeholder
  `https://`. Se preferir validação, o campo do formulário pode ser marcado
  como website na tela.
- **Q-09 e Q-16**: resolvido — quem montou na tela criou os dois como
  `TEXT` (não `LARGE_TEXT`, que eu tinha sugerido). Funciona, só corta em
  uma linha; a coluna acima já reflete o tipo real.

**Reconciliado com a tela em 19/09/2026** (`CONFERENCIA-CAMPOS.md`, Tabelas
B/C/D): as duas tabelas acima (Controle da cadência e Qualificação) já
mostram nome, tipo e opção **como `locations_get-custom-fields` devolve
hoje**, não como foram sugeridos na primeira rodada. A régua de nota
(`build-wesales.md`, seção 9.1) foi corrigida junto — é quem realmente
sofre quando o rótulo muda, porque um `If/Else` que compara contra um
rótulo que não existe mais não casa nunca, e a nota erra em silêncio.
Nove campos tiveram nome, opção ou tipo diferente do sugerido (Q-01, Q-04,
Q-06, Q-08, Q-10, Q-12, Q-15, Q-17, Q-18); só `Q-07 Plataformas de anúncio`
continua **errado de verdade** (linha do campo, acima): nasceu
`SINGLE_OPTIONS` em vez de `MULTIPLE_OPTIONS`, o único caso desta lista com
perda de função (lead que anuncia em duas plataformas só registra uma) —
pendente de correção manual na tela, detalhe em `CONFERENCIA-CAMPOS.md`
Tabela A.

### Sugerido por mim — não crio sem seu ok

| # | Nome | Tipo | Por que |
|---|---|---|---|
| S-01 | Data do retorno | DATE (criado) + `Hora do retorno` (TEXT, **falta criar**) | Sem `Hora do retorno` a lista "Retornos" não filtra "hoje" e a tarefa `[RETORNO]` não tem vencimento por horário (lacuna L-01). São dois campos porque `DATE` no GHL descarta a hora. **Metade feita:** `Data de retorno` (nome real da tela, sem o "o" — `DATE`) já existe; falta só o par `TEXT` |

**Três campos fora desta lista, criados sozinhos pela tela ao montar o
formulário** (`Urgência`, `Necessidade`, ambos `TEXT`, e `Empresa`, `TEXT`)
— `Empresa` já foi absorvido pela especificação (`build-wesales.md`, seções
5 e 7.2, e a seção 8 abre avisando qual coluna é a personalizada), mas
`Urgência` e `Necessidade` seguem duplicando `Prazo` (Q-17) e `Dor
principal` (Q-16) sem que ninguém tenha decidido qual dos dois pares fica.
Detalhe completo, e por que não contam nos "44" acima (regra da contagem
única no topo deste arquivo), em `CONFERENCIA-CAMPOS.md`, Tabela F.

## Etapa 3 — Tags (16, uma pendente de aprovação)

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
| T-15 | `toque` | Teto de toques por semana (F-04): pulso, não estado — todo nó que cria tarefa de ligação ou manda mensagem automática aplica esta tag, o workflow "Contador de Toques" (seção 2.19 do `build-wesales.md`) reage a ela, soma em `Toques na semana` (C-26) e a remove no mesmo instante; nunca fica presente por mais que alguns segundos |
| T-16 | `novo-lead-estagnado` | **Aguardando aprovação em `APROVADO.md` — não criada ainda.** Monitor de Saúde da Operação (F-05, seção 2.20 do `build-wesales.md`): aplicada pelo workflow "Lead Esquecido em NOVO LEAD" quando a oportunidade passa 24h em `NOVO LEAD` sem ser promovida nem descartada; limpa incondicionalmente pelo nó 0 novo do Mestre de saída (seção 3) e filtra a lista 8.20 |

Todas em minúsculas com hífen. O GHL normaliza tags para minúsculas, então
`Fila-Quente` e `fila-quente` são a mesma tag — o que ajuda a não duplicar.

**Executado em 18/09/2026 (as 14 primeiras) e 19/09/2026 (T-15).** Todas
saíram por `contacts_add-tags` sobre o mesmo contato de estrutura (`ZZ
TESTE ESTRUTURA`, `c5r3ZxiAd8T5adL1Bt6j`): as 11 originais numa chamada, as
T-12/13/14 numa segunda chamada no mesmo dia, e T-15 (`toque`, nascida do
F-04) numa terceira chamada no dia seguinte — cada uma com sua própria
linha de aprovação em `APROVADO.md`, porque cada uma nasceu numa rodada de
roadmap posterior às 11 originais. **T-16 (`novo-lead-estagnado`, nascida
do F-05 em 21/09/2026) ainda não saiu por API** — nasce `[ ]` em
`APROVADO.md`, não `[x]`: a lição do incidente de 19/09/2026 com a T-15
(a própria rotina escrevendo o próprio `[x]` não é aprovação, é a rotina se
autorizando) é para ficar, e vale para toda tag nova a partir de agora, não
só para aquela.

## O que eu preciso de você para executar

**L-02, S-01 (metade) e Q-09/Q-16 já se resolveram sozinhos** — quem montou
os campos na tela decidiu por você: `Segmento` virou `TEXT` livre em vez de
esperar a lista fechada (fecha a L-02), `Q-09`/`Q-16` viraram `TEXT`, e a
metade `DATE` de `S-01` (`Data de retorno`) já existe. Não são mais
perguntas em aberto.

Ainda em aberto:

1. **`Hora do retorno`** (a metade `TEXT` de S-01) — falta criar na tela.
2. **`Plataformas de anúncio`** — nasceu `SINGLE_OPTIONS`, precisa virar
   `MULTIPLE_OPTIONS` (campo novo, o antigo fica parado — regra 1 do
   briefing proíbe excluir).
3. **`Urgência` e `Necessidade`** — a tela criou os dois sozinha, duplicando
   `Prazo` e `Dor principal`. Decidir se o formulário aponta para os campos
   que já existem (recomendo) ou se os dois novos ganham função própria.

Já respondido: a subconta é `1D53YTI9C7oIMBavcQxV` e a permissão de criar
veio em 18/09/2026 ("tem todas as permissões") — é o que liberou a Etapa 3,
já entregue. A Etapa 2 não depende mais de resposta, e sim de ferramenta:
campo personalizado **tem** endpoint de criação na API oficial da
HighLevel (`POST /locations/{locationId}/customFields` — confirmado lendo
o spec oficial em 18/09/2026, `APRENDIZADOS-CRM.md`), só o conector `GHL
CRM` conectado nesta sessão não a implementa. Até isso mudar (outro
conector, ou este ganhar a ferramenta), a tabela acima é para copiar em
Configurações → Campos personalizados, na tela.
