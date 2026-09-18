# build-wesales.md — o que só dá para montar na tela

Especificação nó a nó do que o MCP **não** cria: pipeline, workflows,
calendário, formulário e listas inteligentes. Campos e tags saem por API
(Etapas 2 e 3), então aqui eles são pré-requisito, não tarefa.

Convenções deste documento:
- `Campo` = campo personalizado de contato criado na Etapa 2.
- `tag` = tag criada na Etapa 3.
- Prefixos de tarefa: `[CADENCIA]`, `[CONECTADO]`, `[RETORNO]`. A rotina de
  manutenção depende deles; não invente um quarto prefixo sem atualizar
  `rotina-limpar-tarefas.md`.
- Fuso: o da subconta (confirme que é `America/Sao_Paulo`).

## Ordem de montagem

Monte nesta ordem, senão os nós não encontram o que referenciar.

1. Campos e tags (Etapas 2 e 3, por API)
2. Pipeline "Pré-vendas" (seção 1)
3. Calendário do closer + formulário (seção 7)
4. Trigger Link "Agendar com o closer" (seção 2.9) — precisa da URL do
   calendário do passo 3
5. Workflow "Mestre de saída" (seção 3)
6. Workflow "Pós-ligação" (seção 4)
7. Workflow "Pós-agendamento" (seção 5)
8. Workflow "Loop do closer" (seção 5.1) — usa os campos do closer criados
   no passo 1
9. Workflow "Registro de Comparecimento" (seção 5.2) — usa o mesmo
   calendário do passo 3, gatilho por status de agendamento
10. Workflow "Qualificação por IA no WhatsApp" (seção 6)
11. Workflow "Cadência 12x30" (seção 2) — por último entre os principais,
    porque chama os outros e usa o Trigger Link do passo 4 nas mensagens M2/M3;
    textos das mensagens em `biblioteca-mensagens.md`, não neste documento.
    Do passo 11 em diante o gatilho da seção 2.1 já leva o filtro novo do
    R-07 (tag `cad-inbound` ausente) — monte-o com o filtro desde o início,
    não depois. O bloco padrão de tentativa (seção 2.4) já leva o nó 2.5 de
    pausa individual (R-09) desde a primeira montagem, não como retrofit
12. Workflow "Cadência Inbound" (seção 2.10) — depois da 12x30 porque o
    handoff do fim da cadência inbound entra nela por Add to Workflow (seção
    2.10, último nó); precisa da 12x30 já montada para apontar para algo.
    Também já leva o nó 1.5 de pausa individual (R-09) desde o início
13. Workflows "Interceptação de Sinal — Clique" e "— Resposta" (seção 2.9)
14. Workflow "Alerta de Speed-to-lead" (seção 2.11) — usa a mesma tag nova de
    monitoramento que a lista 8.8 filtra; do R-07 em diante o nó 1 bifurca
    o tempo de espera por origem (`cad-inbound` presente = 15 min, senão 1h);
    do R-09 em diante o nó 2 já ignora quem está com a tag `pausado`
15. Workflow "Reengajamento 90 dias" (seção 2.12) — por último entre os que
    tocam cadência: reaproveita o bloco padrão da 12x30 (passo 11) nó a nó,
    nó 2.5 incluído, e exige que o gatilho do passo 11 já tenha o filtro
    `reengajamento-ativo` ausente (R-08) — monte-o com o filtro desde o
    início se ainda não montou, não depois
16. Listas inteligentes (seção 8)
17. Teste com os 5 contatos fictícios (seção 10) **antes** de publicar
18. Pausar Workflows em Datas Específicas (seção 2.13, R-09) — por último de
    todos: o recurso só lista workflows **publicados**, então precisa dos
    passos 11, 12 e 15 já publicados para aparecerem no seletor

---

## 1. Pipeline "Pré-vendas"

Oportunidades → Configurações → Pipelines → Adicionar pipeline.

| Ordem | Etapa | Significado operacional | Prefixo de tarefa válido |
|---|---|---|---|
| 1 | Novo lead | Entrou, ainda não foi para a cadência | — |
| 2 | Em cadência | Nas 12 tentativas | `[CADENCIA]` |
| 3 | Conectado | Atendeu, conversa em andamento, sem reunião marcada | `[CONECTADO]` |
| 4 | Retorno agendado | Pediu para ligar depois | `[RETORNO]` |
| 5 | Reunião agendada | Agendou com o closer | — |
| 6 | Nutrição | Sem fit agora, volta em 90 dias | — |
| 7 | Descartado | Número errado, não ligar, sem fit definitivo | — |

Configurações do pipeline:
- Visibilidade: apenas SDR + closer + gestor.
- "Nome da oportunidade" = nome do contato (padrão).
- Deixe a etapa **Novo lead** como entrada de qualquer importação/formulário.

Por que 7 etapas e não 5: "Em cadência" precisa ser uma etapa própria porque
**é ela que o portão de cada tentativa consulta**. Se o lead sai dela, a
cadência para sozinha. Esse é o mecanismo de segurança da máquina inteira.

---

## 2. Workflow "Cadência 12x30"

### 2.1 Gatilho

**Opportunity Stage Changed** (Etapa da oportunidade alterada)
- Pipeline: `Pré-vendas`
- Para a etapa: `Em cadência`
- Filtro adicional (R-07): tag `cad-inbound` **ausente**
- Filtro adicional (R-08): tag `reengajamento-ativo` **ausente**

Não use "Contact Tag Added" como gatilho: a tag é consequência da cadência,
não causa dela. E não use "Contact Created", senão o lead entra antes de ter
telefone validado.

O filtro do R-08 existe por um caso que só aparece com o Reengajamento 90
dias (seção 2.12) montado: um lead pode chegar a `Nutrição` sem nunca ter
entrado de verdade nesta cadência 12x30 — por exemplo, um lead inbound que
recebeu `Número errado` ainda dentro da Cadência Inbound (seção 2.10, antes
do handoff da TI5) e tinha e-mail cadastrado cai direto em `Nutrição` pelo
ramo `Número errado` do Pós-ligação (seção 4), sem nunca ter passado pelas
tentativas T1-T12 desta cadência. 90 dias depois, o Reengajamento reativa
esse lead: `Allow Re-entry` desligado (D-06) não bloquearia a entrada dele
aqui, porque "bloquear" só vale para quem já tem histórico *neste workflow
específico*, e ele nunca teve — sem o filtro, ele entraria de verdade,
duplicando a régua que o Reengajamento já está rodando na TR{n} dele.
`reengajamento-ativo` fecha esse buraco sem depender de reconstruir a
história do contato.

O filtro de tag é o que separa este workflow do "Cadência Inbound" (seção
2.10, R-07 do roadmap): os dois escutam o mesmo evento — entrar em `Em
cadência` — e cada um pega a fatia que é sua, sem If/Else nenhum decidindo
isso dentro do fluxo. Pesquisado antes de desenhar: a documentação da
HighLevel confirma que a ação **Add to Workflow** entra direto na sequência
de ações de um workflow **sem reavaliar o filtro do gatilho** — é o mesmo
mecanismo que a seção 2.7 já usa para a Qualificação por IA. Isso é o que
permite ao "Cadência Inbound" (seção 2.10) devolver um lead sem resposta
para esta cadência normal ao fim das 5 tentativas rápidas, mesmo com a tag
`cad-inbound` continuando presente (ela é o registro de origem do lead, e
o Mestre de saída — seção 3 — nunca a remove). A única exceção documentada
a essa permanência é o Reengajamento 90 dias (seção 2.12, R-08), que troca
`cad-inbound` por `cad-outbound` de propósito na reativação — não por
acidente nem por um segundo lugar decidindo a mesma coisa.

### 2.2 Configurações do workflow

| Configuração | Valor | Por que |
|---|---|---|
| Janela de envio (Send Window) | 08:30 às 18:30 | Nada dispara de madrugada |
| Dias | Segunda a sexta | Tentativa que cai no sábado escorrega para segunda |
| Fuso | Da subconta | Não use fuso do contato: o SDR trabalha no fuso dele |
| Stop on Response | **Ligado** | "Respondeu em qualquer canal -> sai da cadência" |
| Allow Re-entry | **Desligado** (decisão D-06) | Com reentrada ligada, o lead que volta para "Em cadência" ganha tentativas duplicadas |
| Contatos em múltiplos workflows | Permitido | O lead fica também no de IA |

### 2.3 Nó 0 — inicialização (uma vez, antes da T1)

| Nó | Ação | Configuração |
|---|---|---|
| 0.1 | Update Contact Field | `Tentativa nº` = 0 |
| 0.2 | Update Contact Field | `WA não atendidas seguidas` = 0 |
| 0.3 | Update Contact Field | `Resultado da tentativa` = vazio |
| 0.4 | If/Else | `Permissão WhatsApp` está vazio → Update: `Não solicitado` |
| 0.5 | Update Contact Field | `Prioridade` = 3 (padrão; a seção 9 recalcula) |
| 0.6 | Update Contact Field | `Entrada em` = `{{right_now}}` (R-02 — carimbo de speed-to-lead) |

### 2.4 O bloco padrão de uma tentativa (9 nós)

Este é o molde. Repita 12 vezes trocando dia, horário, canal e número. `{n}` é
o número da tentativa.

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | **Aguardar dia** | Wait → Time Delay | Dias corridos até o dia da tentativa (delta em relação à tentativa anterior — tabela 2.5) |
| 2 | **Aguardar horário** | Wait → Until specific time | O horário da tabela 2.5. A janela do 2.2 empurra para o próximo dia útil se cair fora |
| 2.5 | **Pausa individual (R-09)** | If/Else | tag `pausado` presente → ramo 2.5b. Senão → segue para o Portão (nó 3) |
| 2.5b | Ramo da pausa individual | Wait → Time Delay 1 dia → **volta para o nó 2.5** | Não cria tag de fila, não cria tarefa, não avança `Tentativa nº`. Reconsulta a tag uma vez por dia até o SDR remover — a tentativa fica represada no mesmo lugar, não é descartada nem reagendada |
| 3 | **Portão** | If/Else — condições **E** | Etapa da oportunidade **é** `Em cadência` · tag `nao-perturbe` **não** presente · `Resultado da tentativa` **não é** `Não ligar` · (só em tentativa de telefone) tag `telefone-invalido` **não** presente |
| 3b | Ramo falso do portão | Remove Contact Tag `fila-tel`, `fila-wa`, `fila-quente` → Add Contact Tag `limpar-tarefas` → **Remove from Workflow: este** | Saída limpa. Sem isso, sobra tag e tarefa órfã |
| 4 | **Seletor de canal** | If/Else (só em tentativa de WhatsApp) | Ramo WA: `Permissão WhatsApp` **é** `Sim` **E** `WA não atendidas seguidas` **<** 2. Ramo senão: vira telefone (decisão D-04 + regra das 2 seguidas) |
| 5 | **Limpar resultado** | Update Contact Field | `Resultado da tentativa` = vazio · `Tentativa nº` = `{n}` |
| 6 | **Adicionar tag de fila** | Add Contact Tag | `fila-tel` (telefone) ou `fila-wa` (WhatsApp) |
| 7 | **Criar tarefa** | Add Task | Título: `[CADENCIA] T{n} · Ligar (telefone)` ou `[CADENCIA] T{n} · Ligar (WhatsApp)` · Vence: hoje no horário da tentativa · Atribuir: SDR (round-robin se houver mais de um) |
| 8 | **Aguardar resultado** | Wait → Condition, com tempo limite | Condição: `Resultado da tentativa` **não está vazio**. Tempo limite: até **18:30 do mesmo dia**. Se a sua versão não tiver Wait por condição, use Wait → Until 18:30 e um If/Else checando o campo — mesmo efeito |
| 9 | **Remover tag de fila** | Remove Contact Tag | `fila-tel` e `fila-wa` (remova as duas, sempre — barato e evita tag presa) |
| 10 | **Condição por resultado** | If/Else | `Atendeu` ou `Pediu retorno` → **Remove from Workflow: este** (quem move etapa é o Pós-ligação, seção 4) · `Número errado` ou `Não ligar` → **Remove from Workflow: este** · qualquer outro / tempo limite → segue para a próxima tentativa |
| 10b | Ramo do tempo limite | Update Contact Field | `Resultado da tentativa` = `Não atendeu` · Add Contact Tag `limpar-tarefas` (a tarefa do dia não foi feita; a rotina horária fecha) |

Detalhe que costuma passar batido: o nó 5 **limpa** `Resultado da tentativa`
antes de criar a tarefa. Sem isso, o nó 8 vê o resultado da tentativa anterior
e passa direto.

**Por que a pausa individual (nó 2.5) é um portão separado do nó 3, e não mais
uma condição dentro dele (R-09):** o ramo falso do nó 3 (3b) tira o contato do
workflow — é saída, não pausa. Colar `pausado` ausente na mesma condição **E**
do nó 3 faria um lead pausado perder a régua inteira (`Tentativa nº` zerado na
prática, porque saindo do workflow ele só volta por uma rodada 2 manual,
decisão D-06) em vez de retomar de onde parou quando o SDR remover a tag. O
nó 2.5 resolve isso represando o contato num laço de 1 dia, sem tocar em fila,
tarefa ou contador — a especificação inteira da seção 2.13 explica a régua de
pausa completa, incluindo por que a pausa de calendário (feriado, férias do
SDR) **não** usa esse mesmo mecanismo.

**Só no bloco da tentativa 1 (T1)**, entre os nós 5 e 6, some mais dois (R-02
— speed-to-lead):

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 5c | Carimbo | Update Contact Field | `1ª tentativa em` = `{{right_now}}` |
| 5d | Limpeza preventiva | Remove Contact Tag | `atraso-1a-tentativa` (barato mesmo se ausente — ver seção 2.11) |

Não repita 5c/5d nas tentativas 2 a 12: T1 é sempre a primeira do molde (delta
0d, sem tentativa antes dela), então `1ª tentativa em` só precisa de uma
escrita — a mesma lógica de "Total de conexões" ter um dono só (seção 4).

O contador `WA não atendidas seguidas` **não** é mexido aqui — quem soma e
zera é o Pós-ligação (seção 4), que é o único lugar que sabe qual foi o canal
e o resultado. Um contador com dois donos sempre diverge.

### 2.5 As 12 tentativas

Tentativa = ação do SDR (decisão D-01). As mensagens automáticas são nós de
envio no meio do fluxo e não contam como tentativa.

| T | Dia | Horário | Canal | Delta do Wait (nó 1) | Tag | Título da tarefa |
|---|---|---|---|---|---|---|
| M1 | D1 | 08:45 | Mensagem (automática) | — | — | — |
| 1 | D1 | 10:30 | Telefone | 0 d | `fila-tel` | `[CADENCIA] T1 · Ligar (telefone)` |
| 2 | D1 | 16:10 | Ligação WhatsApp | 0 d | `fila-wa` | `[CADENCIA] T2 · Ligar (WhatsApp)` |
| 3 | D2 | 09:20 | Telefone | 1 d | `fila-tel` | `[CADENCIA] T3 · Ligar (telefone)` |
| 4 | D2 | 17:20 | Ligação WhatsApp | 0 d | `fila-wa` | `[CADENCIA] T4 · Ligar (WhatsApp)` |
| 5 | D4 | 11:00 | Ligação WhatsApp | 2 d | `fila-wa` | `[CADENCIA] T5 · Ligar (WhatsApp)` |
| 6 | D7 | 09:00 | Telefone | 3 d | `fila-tel` | `[CADENCIA] T6 · Ligar (telefone)` |
| 7 | D7 | 15:30 | Ligação WhatsApp | 0 d | `fila-wa` | `[CADENCIA] T7 · Ligar (WhatsApp)` |
| 8 | D10 | 11:40 | Telefone | 3 d | `fila-tel` | `[CADENCIA] T8 · Ligar (telefone)` |
| M2 | D10 | 13:30 | Mensagem (automática) | — | — | — |
| 9 | D14 | 16:40 | Ligação WhatsApp | 4 d | `fila-wa` | `[CADENCIA] T9 · Ligar (WhatsApp)` |
| 10 | D20 | 10:15 | Telefone | 6 d | `fila-tel` | `[CADENCIA] T10 · Ligar (telefone)` |
| 11 | D30 | 09:40 | Telefone | 10 d | `fila-tel` | `[CADENCIA] T11 · Ligar (telefone)` |
| 12 | D30 | 17:00 | Ligação WhatsApp | 0 d | `fila-wa` | `[CADENCIA] T12 · Ligar (WhatsApp)` |
| M3 | D30 | 17:45 | Mensagem de encerramento | — | — | — |

Confere com o briefing: D1 tel+msg+WA · D2 tel+WA · D4 WA · D7 tel+WA ·
D10 tel+msg · D14 WA · D20 tel · D30 tel+WA+msg.

Os dias são corridos e a janela de dias úteis empurra o que cai em fim de
semana. Isso significa que "D30" na prática cai por volta do dia 41 do
calendário. Se você quer 30 dias corridos exatos, desligue "dias úteis" para
as mensagens e mantenha para as ligações.

### 2.6 As 3 mensagens automáticas

Nós de envio (Send WhatsApp; SMS como fallback se o provedor não estiver
ativo), posicionados no fluxo conforme a tabela 2.5. Cada um precedido do
mesmo **portão** do nó 3 (sem a checagem de `telefone-invalido`) e com a
condição extra `nao-perturbe` ausente, e seguido de um nó **Update Contact
Field** `Template usado` = o código da mensagem (R-04 — sem esse carimbo não
dá para saber depois qual abertura gerou a resposta). M1 é exceção: em vez de
um envio único, testa duas versões em paralelo — nó a nó em 2.6.1.

Textos, código e histórico de versão moram em `biblioteca-mensagens.md`, não
aqui: texto duplicado em dois documentos diverge na primeira edição. Versão
vigente nesta rodada:

| Mensagem | Código | Posição no fluxo | `Template usado` grava |
|---|---|---|---|
| M1 — abertura, D1 08:45 | `M1-a` / `M1-b` (teste A/B — 2.6.1) | Início do fluxo, junto da T1 | `M1-a` ou `M1-b`, conforme o caminho sorteado |
| M2 — reforço, D10 13:30 | `M2-v1` | Após a T8 | `M2-v1` |
| M3 — encerramento, D30 17:45 | `M3-v1` | Após a T12 | `M3-v1` |

Depois de M1 (os dois caminhos do teste A/B convergem no mesmo nó — 2.6.1),
adicione um nó **Wait → Contact Replied (tempo limite 2h)**. Se respondeu, o
Stop on Response tira da cadência e o lead cai na seção 6.

`[Agendar com o closer]`, citado no texto de M2-v1 e M3-v1 em
`biblioteca-mensagens.md`, é o Trigger Link da seção 2.9, não texto literal —
insira pelo ícone `{}` da caixa de mensagem, em Custom Values → Trigger Links.
M1 fica sem link de propósito: é a mensagem que pergunta permissão de ligar, e
um link ali compete com a pergunta em vez de reforçá-la.

Depois de M3: Update `Resultado da tentativa` = vazio → Add Contact Tag
`nutricao-90d` → mover oportunidade para `Nutrição` → fim do workflow. A
mudança de etapa aciona o Mestre de saída, que limpa o resto.

### 2.6.1 Teste A/B da abertura (M1) — R-05

**Por quê:** M1 é a única mensagem que todo lead recebe antes de qualquer
outro sinal existir sobre ele — decide se a cadência gera resposta ou não, e
é a única mensagem que compensa testar (as outras já reagem a um resultado
anterior, que muda o texto certo caso a caso).

Pesquisado antes de desenhar: o A/B de step de sequência do Outreach.io
sorteia **aleatoriamente** qual variante cada contato recebe e mantém o
contato no mesmo caminho se ele reentrar no mesmo step — não alterna por
ordem de chegada. O GHL tem a mesma peça pronta: a ação nativa **Split**,
sorteio por percentual com a mesma regra de permanência (quem já foi
sorteado para um caminho não é sorteado de novo se passar pelo Split outra
vez). Usar isso em vez de um If/Else alternando por paridade de ID evita
correlacionar a variante com a ordem/horário de entrada do lead — que é
exatamente o viés que sorteio aleatório existe para evitar.

**O que varia entre as versões:** só o gancho de abertura. Saudação, menção a
`{{contact.segmento}}`, ausência de link e a pergunta de fechamento ("Posso
te ligar hoje ou prefere por aqui?") são idênticos nas duas — regra de teste
A/B de variar um elemento por vez, para a diferença de resposta poder ser
atribuída a uma causa só. Textos completos em `biblioteca-mensagens.md`.

| Nó | Ação | Configuração |
|---|---|---|
| M1.1 | **Portão** | Mesmo portão do nó 3 (seção 2.4), sem a checagem de `telefone-invalido`, com `nao-perturbe` ausente |
| M1.2 | **Split — Teste A/B abertura** | Ação nativa Split, sorteio aleatório: Caminho A 50% · Caminho B 50% |
| M1.3a (Caminho A) | Send WhatsApp (SMS fallback) | Texto `M1-a`, `biblioteca-mensagens.md` |
| M1.4a (Caminho A) | Update Contact Field | `Template usado` = `M1-a` |
| M1.3b (Caminho B) | Send WhatsApp (SMS fallback) | Texto `M1-b`, `biblioteca-mensagens.md` |
| M1.4b (Caminho B) | Update Contact Field | `Template usado` = `M1-b` |

Depois de M1.4a e M1.4b, **conecte os dois caminhos ao mesmo nó seguinte**
(Wait → Contact Replied, 2h, citado em 2.6) — o Split do GHL não rejunta
sozinho, as duas pontas precisam apontar manualmente para o mesmo destino.

**Sobre o percentual:** 50/50 por padrão. Com ~10 leads/dia entrando e M1
disparando uma vez por lead, cada variante recebe ~5/dia — juntar volume que
signifique alguma coisa na lista `Resposta por Template` (seção 8.13) leva
semanas, não dias. É o custo aceito de testar dentro do volume real da
operação em vez de esperar um lote maior parado sem testar nada.

**Quando declarar vencedor:** quando uma das linhas de `Resposta por
Template` (8.13) acumular volume visivelmente maior que a outra por um
período sustentado — o GHL não tem teste de significância nativo, então o
critério é humano, não estatístico. Ao declarar, edite o percentual do Split
para 100/0 (a variante perdedora para de receber tráfego, mas o histórico
fica) e registre a decisão em `biblioteca-mensagens.md` (regra de
versionamento: marcar a linha perdedora como encerrada, nunca apagar).

**Pronto quando (do roadmap):** "duas versões rodando e a comparação sai da
lista inteligente" — cumprido. M1-a e M1-b rodam ao mesmo tempo pelo Split, e
`Resposta por Template` (8.13) já cruza `Sinal recebido` com `Template
usado`, sem lista nova.

### 2.7 Entrada na qualificação por IA

Logo após o nó 10 da **tentativa 4** (D2, fim do dia), insira:

| Nó | Ação | Configuração |
|---|---|---|
| a | If/Else | `Tentativa nº` ≥ 2 **E** `Resultado da tentativa` ≠ `Atendeu` **E** `Permissão WhatsApp` ≠ `Não` |
| b | Add to Workflow | `Qualificação por IA no WhatsApp` |

O briefing diz "entra após 2 tentativas sem atendimento". Coloquei no fim do
D2 (que é a T4) porque aí já houve 4 tentativas reais em 2 dias — o lead teve
chance de atender antes de a IA entrar. Se preferir literalmente após a T2,
mova o par de nós para o fim do bloco da T2.

### 2.8 Alternativa que eu recomendo avaliar (Opção B)

O bloco da 2.4 mantém o contato **parado dentro do workflow** esperando o
resultado (nó 8). Funciona, é o que você pediu, e tem uma fragilidade: se o
workflow for editado ou republicado, contatos parados em Wait podem ser
reposicionados, e você perde tentativas no meio.

A alternativa nativa é dividir: a Cadência só **agenda** (tag + tarefa) e
segue para o próximo Wait sem esperar; quem reage ao resultado é o
Pós-ligação, que também remove a tag. Fica mais robusto a edições e mais
difícil de depurar. Sugiro: sobe na 2.4 (mais legível, mais fácil de testar),
e se você começar a editar a cadência com volume em produção, migra para B.

---

## 2.9 Interceptação de sinal — F-01

A cadência de 2.4 trata toda tentativa igual: dispara no dia certo, olha o
calendário, não o lead. Mas o lead **dá sinal** fora do calendário — clica num
link, responde fora de hora — e hoje isso só some silenciosamente dentro do
Stop on Response ou não tem lugar nenhum para ir (clique em link não é
rastreado). É a lacuna F-01 do roadmap: paridade não basta, o que separa da
concorrência é reagir ao sinal em minutos, não no próximo dia agendado.

Dois workflows curtos, gatilho diferente, mesmo efeito: fura a fila e avisa o
SDR agora. Não são um workflow só com dois gatilhos porque cada um precisa
gravar de forma confiável **qual** sinal foi — e o GHL não expõe de forma
segura, dentro dos nós, qual dos vários gatilhos de um mesmo workflow disparou.

### 2.9.1 Trigger Link "Agendar com o closer"

Marketing → Trigger Links → Novo. Destino: a URL pública do calendário
`Reunião com closer` (seção 7.1). Nome do link: `Agendar com o closer` — é o
nome que aparece no seletor de gatilho `Trigger Link Clicked` e no menu
`{}` → Custom Values → Trigger Links das mensagens.

Por que apontar para o calendário e não para uma landing page nova: a página
já existe (é pré-requisito da seção 7), o link fica pronto sem depender de
criar site, e clicar nele já é a maior demonstração de interesse possível —
maior que abrir um artigo. Um concorrente copiando a tela de fora vê "manda
link do calendário"; não vê que o link virou sensor.

### 2.9.2 Workflow "Interceptação de Sinal — Clique"

**Gatilho:** `Trigger Link Clicked` — Link: `Agendar com o closer`

| Configuração | Valor |
|---|---|
| Janela de envio | 08:30 às 18:30, segunda a sexta, fuso da subconta |
| Allow Re-entry | Ligado (cada clique é um sinal novo) |
| Stop on Response | Desligado |

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Portão de etapa | If/Else | Etapa da oportunidade **é** `Em cadência` → segue. Senão → **encerra** (quem já saiu de cadência não precisa furar fila; já está tratado por outro caminho) |
| 2 | Portão de silêncio | If/Else | tag `nao-perturbe` presente → **encerra**. Senão → segue |
| 3 | Prioridade | Update Contact Field | `Prioridade` = 5 |
| 4 | Registro do sinal | Update Contact Field | `Sinal recebido` = `Clique em link` · `Data do sinal` = `{{right_now}}` |
| 5 | Fila | Add Contact Tag | `fila-quente` |
| 6 | Tarefa | Add Task | Título: `[CADENCIA] Sinal: clicou no link — ligar agora` · Vence: agora · Atribuir: SDR |
| 7 | Aviso | Internal Notification | Para o SDR: `{{contact.name}} clicou no link de agendar agora. Prioridade 5.` |
| 8 | Registro | Add Note | `Sinal: clique em link · {{right_now}}` |

### 2.9.3 Workflow "Interceptação de Sinal — Resposta"

Idêntico ao 2.9.2, trocando o gatilho e os dois textos marcados.

**Gatilho:** `Customer Replied` — Canais: WhatsApp e SMS (os dois canais de
texto da cadência)

Mesma tabela de nós da 2.9.2, com estas trocas:
- Nó 4: `Sinal recebido` = `Resposta de mensagem`
- Nó 6: Título da tarefa `[CADENCIA] Sinal: respondeu mensagem — ligar agora`
- Nó 7: `{{contact.name}} respondeu agora fora do fluxo normal. Prioridade 5.`

O Stop on Response da Cadência 12x30 (seção 2.2) já tira o lead das tentativas
futuras quando ele responde — isso continua acontecendo, sem mudança. O que
faltava é o que este workflow cobre: ninguém avisava o SDR **agora**, e o lead
respondido ficava com a mesma prioridade de antes até a próxima tentativa
classificá-lo.

### 2.9.4 Limite conhecido

Allow Re-entry ligado significa que um lead respondendo várias mensagens
seguidas em minutos gera uma tarefa por resposta. É a troca certa: melhor uma
tarefa a mais para o SDR fechar do que um sinal perdido por deduplicação. Se
isso virar ruído em volume, o ajuste nativo é um filtro de frequência no
próprio gatilho `Customer Replied` (o GHL permite limitar por janela de tempo)
— não crie campo contador novo para isso antes de o volume provar que precisa.

**Pronto quando:** lead que clicou às 14h é ligado às 14h10, não no D7 —
`Prioridade` = 5 e a tarefa `Sinal: ...` aparecem na `Fila Quente` (lista 8.1)
no minuto do clique ou da resposta, dentro da janela de expediente.

---

## 2.10 Workflow "Cadência Inbound" — R-07

A Cadência 12x30 (seção 2) mede a régua em dias porque foi desenhada para
outbound: o lead não pediu nada, então não há pressa que se perca ficando um
dia sem notícia. Inbound é o oposto — o lead preencheu um formulário ou
respondeu um anúncio, e cada minuto de espera é conversão que evapora.
Pesquisado antes de desenhar: o benchmark do Meetime aponta 64% de taxa de
ligação conectada quando o retorno sai em até 10 minutos, e recomenda SLA de
até 5 minutos para lead inbound direto; a literatura de mercado (Velocify/
InsideSales, citada em vários blogs de speed-to-lead) fala em conversão até
21x maior respondendo nos primeiros 5 minutos contra responder depois de 30.
Outreach e Salesloft, por desenho, são ferramentas de cadência **outbound**
— nenhum dos dois tem uma régua nativa em minutos para lead entrante, o que
sobra para relatório manual ou automação por fora. A tabela de degraus do
roadmap (5 min, 30 min, 2h, 1 dia, 3 dias) já cobre exatamente a janela que
a pesquisa aponta como a que decide a conversa: os três primeiros degraus
cabem dentro da 1ª hora, que é onde o SLA se ganha ou se perde.

Por que não é o mesmo workflow da Cadência 12x30 com um `If/Else` trocando
os tempos de espera: os nós de espera de 2.4 são `Wait → Until specific
time` (horário fixo do relógio), porque a régua em dias precisa cair sempre
no mesmo horário do dia. A régua em minutos precisa do oposto — `Wait →
Time Delay` relativo ao instante da entrada — e misturar os dois tipos de
espera dentro do mesmo bloco padrão (2.4) tornaria o molde ilegível para as
17 tentativas somadas. Dois workflows curtos, cada um com o tipo de espera
que sua régua pede, são mais fáceis de auditar que um só com um `if` interno
decidindo qual tipo de nó usar a cada passo.

### Gatilho

**Opportunity Stage Changed** — Pipeline `Pré-vendas` · Para a etapa:
`Em cadência` · Filtro adicional: tag `cad-inbound` **presente**

Espelha o gatilho da Cadência 12x30 (seção 2.1) com o filtro de tag
invertido. Os dois disparam do mesmo evento; o filtro decide qual dos dois
processa aquele lead — não há nó de portão fazendo essa escolha dentro do
fluxo.

**Por que este gatilho não precisa do filtro `reengajamento-ativo` do R-08
(seção 2.1 precisa, este não):** o nó 4 do Reengajamento 90 dias (seção
2.12) remove `cad-inbound` **antes** de mover a etapa para `Em cadência` —
então, no instante em que este gatilho avalia o evento, `cad-inbound` já
está ausente para qualquer lead reativado, sempre. O filtro `cad-inbound`
**presente** já exclui a reativação sozinho, sem precisar de reforço.

### Configurações

| Configuração | Valor | Por quê |
|---|---|---|
| Janela de envio | 08:30 às 18:30, segunda a sexta, fuso da subconta | A mesma da 12x30. Velocidade não é motivo para ligar de madrugada — é o mesmo limite que Meetime documenta como "tempo de resposta em horário comercial", não tempo de relógio corrido |
| Allow Re-entry | Desligado | Mesmo motivo do D-06 na 12x30: reentrada duplicaria tentativa |
| Stop on Response | Ligado | Respondeu em qualquer canal, sai — igual à 12x30 |

**Limite conhecido:** um formulário preenchido às 19h de sexta só dispara a
T1 na segunda às 08:30 — a janela de expediente vale mais que os "5 minutos"
literais. Os 5/30/2h contam a partir do momento em que a janela está aberta,
não a partir do clique. É o mesmo trade-off que Meetime e Reev aceitam ao
medir "tempo de resposta em horário comercial": não existe operação de SDR
ligando à 1h da manhã, e forçar isso queimaria o lead em vez de convertê-lo.

### Nó 0 — inicialização (uma vez, ao entrar)

Espelha 2.3, com duas diferenças (linhas 0.5 e 0.7, novas):

| Nó | Ação | Configuração |
|---|---|---|
| 0.1 | Update Contact Field | `Tentativa nº` = 0 |
| 0.2 | Update Contact Field | `WA não atendidas seguidas` = 0 |
| 0.3 | Update Contact Field | `Resultado da tentativa` = vazio |
| 0.4 | If/Else | `Permissão WhatsApp` está vazio → Update: `Não solicitado` |
| 0.5 | Update Contact Field | `Prioridade` = 5 (não 3: todo lead inbound nasce no topo da fila — é a resposta rápida que a régua de degraus só cumpre se o SDR também priorizar certo) |
| 0.6 | Update Contact Field | `Entrada em` = `{{right_now}}` (mesmo campo do R-02 — a métrica de speed-to-lead nasceu para o outbound e serve de graça aqui, sem custo nenhum) |
| 0.7 | Add Contact Tag | `fila-quente` (assim o lead aparece na lista `Fila Quente`, 8.1, sem lista nova) |

### MI-0 — mensagem automática imediata

Antes da T1, sem esperar nada: Send WhatsApp (SMS fallback), texto `MI-0`
(`biblioteca-mensagens.md`) confirmando o recebimento e avisando que a
ligação vem em minutos — o equivalente ao "notificar o SDR independente de
onde ele esteja" que o Meetime documenta, só que do lado do lead: ele sabe
que foi ouvido antes mesmo do telefone tocar. Seguido de Update `Template
usado` = `MI-0`.

### O bloco padrão de uma tentativa inbound (mirror de 2.4, com espera relativa)

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Aguardar | Wait → Time Delay | Delta da tabela abaixo, relativo ao fim do bloco anterior (não horário fixo) |
| 1.5 | Pausa individual (R-09) | If/Else | tag `pausado` presente → ramo 1.5b. Senão → segue para o Portão (nó 2) |
| 1.5b | Ramo da pausa individual | Wait → Time Delay 30 min → **volta para o nó 1.5** | Mesmo mecanismo do nó 2.5 da 12x30 (seção 2.4), com relógio de 30 min em vez de 1 dia — a régua inbound é medida em minutos, e um retry diário aqui devolveria o lead numa velocidade que já não é mais inbound de verdade |
| 2 | Portão | If/Else — condições **E** | Etapa da oportunidade **é** `Em cadência` · tag `nao-perturbe` **não** presente · `Resultado da tentativa` **não é** `Não ligar` · (só em tentativa de telefone) tag `telefone-invalido` **não** presente |
| 2b | Ramo falso do portão | Remove Contact Tag `fila-tel`, `fila-wa`, `fila-quente` → Add Contact Tag `limpar-tarefas` → **Remove from Workflow: este** | Mesma saída limpa do nó 3b da 12x30 |
| 3 | Seletor de canal | If/Else (só nas tentativas de WhatsApp) | Ramo WA: `Permissão WhatsApp` **é** `Sim` **E** `WA não atendidas seguidas` **<** 2. Senão → telefone |
| 4 | Limpar resultado | Update Contact Field | `Resultado da tentativa` = vazio · `Tentativa nº` = `{n}` |
| 5 | Fila | Add Contact Tag | `fila-tel` ou `fila-wa` |
| 6 | Tarefa | Add Task | Título: `[CADENCIA] TI{n} · Ligar (canal) — Inbound` · Vence: agora · Atribuir: SDR |
| 7 | Aviso | Internal Notification | Para o SDR: `Lead inbound {{contact.name}} aguardando retorno — TI{n}.` Diferencial sobre o bloco padrão outbound (2.4): lá a fila espera ser vista; aqui o SDR é avisado na hora, o mesmo padrão do F-01 (seção 2.9) e do que o Meetime chama de notificação "independente de onde o SDR esteja" |
| 8 | Aguardar resultado | Wait → Condition, tempo limite | Condição: `Resultado da tentativa` **não está vazio**. Tempo limite: o delta até a tentativa seguinte da tabela abaixo — não 18:30 fixo, porque numa régua de minutos "esperar até o fim do dia" descaracterizaria a velocidade |
| 9 | Remover tag de fila | Remove Contact Tag | `fila-tel` e `fila-wa` |
| 10 | Condição por resultado | If/Else | `Atendeu` ou `Pediu retorno` → **Remove from Workflow: este** (o Pós-ligação, seção 4, cuida do resto — é canal-agnóstico, já reaproveitado sem alteração) · `Número errado` ou `Não ligar` → **Remove from Workflow: este** · qualquer outro / tempo limite → próxima tentativa (ou handoff, na TI5) |
| 10b | Ramo do tempo limite | Update Contact Field | `Resultado da tentativa` = `Não atendeu` · Add Contact Tag `limpar-tarefas` |

Só na T1 (aqui, TI1), repita o par 5c/5d da seção 2.4 (`1ª tentativa em` =
`{{right_now}}` e limpeza preventiva de `atraso-1a-tentativa`) — mesmo
campo do R-02, mesmo motivo: é a primeira tentativa de verdade do lead,
independente de a cadência ser inbound ou outbound.

### As 5 tentativas (degraus do roadmap)

| TI | Delta desde a entrada | Delta do Wait (nó 1) | Canal | Tarefa |
|---|---|---|---|---|
| MI0 | imediato | — | Mensagem (automática) | — |
| 1 | 5 min | 5 min | Telefone | `[CADENCIA] TI1 · Ligar (telefone) — Inbound` |
| 2 | 30 min | 25 min (desde TI1) | Telefone | `[CADENCIA] TI2 · Ligar (telefone) — Inbound` |
| 3 | 2h | 1h30 (desde TI2) | Ligação WhatsApp (seletor) | `[CADENCIA] TI3 · Ligar (WhatsApp) — Inbound` |
| 4 | 1 dia | 22h (desde TI3) | Telefone + WhatsApp (seletor) | `[CADENCIA] TI4 · Ligar (canal) — Inbound` |
| 5 | 3 dias | 2 dias (desde TI4) | Telefone | `[CADENCIA] TI5 · Ligar (telefone) — Inbound` |

Canal majoritariamente telefone, de propósito: é o canal que o SDR controla
sem depender de `Permissão WhatsApp` (que um lead recém-chegado quase nunca
já respondeu) — o seletor de WhatsApp só entra nas tentativas 3 e 4, quando
já houve tempo de a permissão ter sido concedida numa ligação anterior.

**Limite conhecido, o mesmo do R-01:** `Tentativa nº` é o mesmo campo (C-01)
usado pela 12x30, então a lista `Conexão por Tentativa` (8.6) passa a
misturar "T1" de 5 minutos com "T1" de um dia — o número é o mesmo, o
significado não. Não vale criar um segundo contador só para diferenciar:
quem olhar a lista já sabe filtrar por `cad-inbound`/`cad-outbound` se
precisar separar as duas réguas, e um contador espelhado é exatamente o tipo
de campo com dois donos que este projeto evita (seção 2.4, nó do contador de
WhatsApp).

### Handoff ao fim da TI5 (sem resposta)

Se a TI5 chega ao nó 10 pelo ramo "qualquer outro / tempo limite" (3 dias
esgotados sem conexão), em vez de "próxima tentativa" (não há):

| # | Ação | Configuração |
|---|---|---|
| 1 | Send WhatsApp (SMS fallback) | Texto `MI-F`, `biblioteca-mensagens.md` — avisa que a tentativa continua, agora na régua normal |
| 2 | Update Contact Field | `Template usado` = `MI-F` |
| 3 | Add to Workflow | `Cadência 12x30` |
| 4 | Remove from Workflow | Este (`Cadência Inbound`) |

O nó 3 funciona apesar de o gatilho da 12x30 (seção 2.1) filtrar `cad-inbound`
ausente: `Add to Workflow` entra direto na sequência de ações, sem reavaliar
o gatilho de destino — documentado pela HighLevel e já usado sem alteração
pela Qualificação por IA (seção 2.7). A tag `cad-inbound` continua no
contato (é origem, não fila — ver seção 3, com a única exceção
documentada na seção 2.12, R-08): o lead vira "inbound que não respondeu
rápido e caiu para a régua normal", não "outbound". A 12x30 zera `Tentativa nº` no seu próprio nó 0.1 ao ser
entrado — a T1 da régua de 30 dias é uma tentativa nova, não uma
continuação numerada da TI5. Pelo mesmo motivo, o nó 0.6 da 12x30 também
regrava `Entrada em` = `{{right_now}}` no instante do handoff — é a mesma
lógica de "rodada nova" da decisão D-06 (`briefing-sdr.md`), não um bug:
o R-02 mede a partir da entrada na régua vigente, e a régua vigente mudou.

**Pronto quando (do roadmap):** formulário preenchido dispara ligação em
minutos — a tarefa `[CADENCIA] TI1` nasce e o SDR é avisado (nó 7) 5 minutos
depois da entrada em `Em cadência`, dentro da janela de expediente.

---

## 2.11 Alerta de Speed-to-lead — R-02

Speed-to-lead é a métrica nº 1 de inbound na literatura de vendas (Reev,
Meetime, Outreach e Salesloft medem todos), mas nenhum deles resolve com
lista estática: eles rodam um relógio de SLA por trás e só mostram o atraso
quando ele já virou alarme. Aqui o relógio é um workflow de 1 nó de espera —
sem dashboard pago, sem app externo.

Por que não dá para responder isso só com uma lista inteligente filtrando
`Entrada em` "há mais de 1h": os dois carimbos (`Entrada em`, `1ª tentativa
em`) são `TEXT`, não `DATE` (a razão está em `APRENDIZADOS-CRM.md` — `DATE`
descarta a hora, e aqui a hora é o que importa). Filtro de lista inteligente
não faz aritmética de data sobre campo `TEXT`. A saída nativa é um workflow
que espera 1h e **marca** o atraso com uma tag — daí a lista (8.8) vira
trivial: filtra presença de tag, sem comparar data nenhuma.

### Gatilho
**Opportunity Stage Changed** — Pipeline `Pré-vendas` · Para a etapa:
`Em cadência` (o mesmo gatilho da Cadência 12x30, seção 2.1 — os dois disparam
juntos, um mede e cadencia, o outro só mede)

### Configurações
| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | Uma rodada 2 manual (decisão D-06) é uma nova entrada de verdade e merece seu próprio relógio |
| Janela de envio | Sem janela | O atraso conta em tempo real, inclusive fora do expediente — é exatamente o que o alerta precisa capturar |
| Stop on Response | Desligado | Não manda mensagem ao lead |

### Nós
| # | Nó | Ação | Configuração |
|---|---|---|---|
| 0 | Bifurcação por origem (R-07) | If/Else | Tag `cad-inbound` presente → Wait 15 minutos (nó 1a). Senão → Wait 1 hora (nó 1b). Os dois caminhos convergem no nó 2 |
| 1a/1b | Aguardar | Wait → Time Delay | 15 min (inbound) ou 1 hora (outbound), conforme o nó 0 |
| 2 | Portão | If/Else | Etapa da oportunidade **é** `Em cadência` **E** `1ª tentativa em` está vazio **E** tag `pausado` **ausente** (R-09) → segue. Senão → **encerra** (T1 já rodou, o lead já saiu de cadência, ou está pausado de propósito — nenhum dos três é atraso) |
| 3 | Fila | Add Contact Tag | `atraso-1a-tentativa` |
| 4 | Aviso | Internal Notification | Para o gestor: `{{contact.name}} está há mais de 1h em cadência sem a 1ª tentativa. Entrada: {{contact.entrada_em}}.` |
| 5 | Registro | Add Note | `Alerta speed-to-lead: sem 1ª tentativa 1h após a entrada · {{right_now}}` |

A limpeza é dupla, de propósito: o nó 5d da T1 (seção 2.4) remove a tag no
caminho feliz (T1 rodou dentro da hora), e o nó 4 do Mestre de saída (seção 3)
remove no caminho de saída (lead mudou de etapa antes de qualquer um dos
dois). Tag presa custa uma lista suja; os dois pontos de remoção custam duas
linhas.

**Pronto quando (herdado do R-02 no roadmap):** existe lista "leads com mais
de 1h sem primeira tentativa" — é a 8.8, filtrando `atraso-1a-tentativa`.

**Por que o nó 0 (R-07):** 1 hora é o limite certo para outbound (ninguém
prometeu nada ao lead) e um limite inútil para inbound, cuja própria régua
(seção 2.10) já dispara a TI1 em 5 minutos — esperar 1h para alertar um
atraso que devia estourar em 15 seria alarme tarde demais para o SLA que o
Meetime documenta como "boa prática" (abaixo de 10 minutos). Em vez de um
segundo workflow e uma segunda tag só para essa diferença, o mesmo alerta
(mesma tag `atraso-1a-tentativa`, mesma lista 8.8) ganha um relógio mais
curto quando a origem é inbound — zero campo novo, zero tag nova.

---

## 2.12 Workflow "Reengajamento 90 dias" — R-08

`nutricao-90d` marca a saída branda desde o primeiro dia do projeto, e até
aqui nada lia essa tag para trazer o lead de volta — ela virava carimbo de
arquivo morto. Reev e Meetime tratam isso como relatório: alguém abre uma
lista de "nutrição vencida" e decide manualmente se recicla. Nenhum dos
dois dispara a reativação sozinho. Fazer o CRM reciclar o lead sem
depender de ninguém abrir uma lista é o que este item entrega, e é
justamente o tipo de coisa "que um concorrente não consegue copiar olhando
a tela de fora" — não tem UI para configurar isso em nenhuma das duas
plataformas, é comportamento nativo do workflow do GHL usado fora do
manual delas.

Pesquisado antes de desenhar: a régua de reativação não repete a
intensidade da régua de entrada. A literatura de reengajamento (a mesma
categoria que trata lead reciclado como "aged lead" ou "recycled lead") é
consistente em um ponto — um lead que já passou pela cadência cheia e não
respondeu não merece as mesmas 12 tentativas de quem está chegando agora;
o toque certo é mais curto e mais espaçado, senão o reengajamento vira
assédio de quem já disse "agora não". Por isso a régua abaixo tem 4
tentativas em 10 dias, não 12 em 30.

### Por que não é a Cadência 12x30 com um `If/Else` de origem

Cogitei reaproveitar o workflow da seção 2 inteiro, entrando o lead
reativado pela mesma porta. Não dá: `Allow Re-entry` da Cadência 12x30 é
**desligado** por decisão D-06 (`briefing-sdr.md`), e essa configuração
vale para o histórico do contato **naquele workflow específico** — um
contato que já passou pela 12x30 uma vez (a rodada original, antes de cair
em Nutrição) fica bloqueado de entrar de novo nela para sempre, reentrada
automática ou por `Add to Workflow` (o comportamento documentado em
`APRENDIZADOS-CRM.md`: `Add to Workflow` ignora o filtro do gatilho de
destino, mas **não** ignora `Allow Re-entry`). Reduzir a régua de
reativação para caber dentro da 12x30 exigiria ligar `Allow Re-entry` lá,
o que reabre exatamente o risco que o D-06 fechou: qualquer entrada
futura em "Em cadência" — inclusive um erro de clique do SDR — passaria a
duplicar tentativas para leads que nunca deveriam repetir a régua. Um
workflow próprio, pequeno, com seu próprio `Allow Re-entry` **ligado** de
propósito (só ele, isolado), resolve sem tocar no D-06. É o mesmo
raciocínio que já separou a Cadência Inbound (seção 2.10) da 12x30: dois
workflows curtos, cada um com a configuração que sua régua pede, batem um
workflow só com `if` decidindo por dentro qual configuração vale.

### Gatilho

**Opportunity Stage Changed** — Pipeline `Pré-vendas` · Para a etapa:
`Nutrição`

### Configurações

| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | Ao contrário da 12x30 (D-06), aqui *toda* entrada em `Nutrição` é uma rodada legítima e nova — o mesmo raciocínio já usado no Alerta de Speed-to-lead (seção 2.11): "uma rodada 2 manual é uma nova entrada de verdade e merece seu próprio relógio". Sem isso, o lead reativaria uma vez e nunca mais — o "por quê" deste item ("nutrição sem retorno é arquivo morto") voltaria a valer na segunda rodada |
| Janela de envio | 08:30 às 18:30, segunda a sexta, fuso da subconta | Mesma janela da 12x30 — reativação não é urgência, é rotina |
| Stop on Response | Ligado | Respondeu em qualquer canal, sai da régua de reativação |

### Nós

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Aguardar | Wait → Time Delay | 90 dias corridos |
| 2 | Portão | If/Else — condições **E** | Etapa da oportunidade **é** `Nutrição` · tag `nutricao-90d` presente · tag `nao-perturbe` ausente |
| 2b | Ramo falso do portão | **Remove from Workflow: este** | O lead já saiu de `Nutrição` por outro caminho (voltou a `Em cadência` na mão, converteu, foi descartado) ou pediu para não ser mais procurado — não reativa quem já mudou de estado por conta própria. Nada para limpar aqui: nenhuma tag de fila foi tocada ainda |
| 3 | Reset de rodada | Update Contact Field | `Tentativa nº` = 0 · `WA não atendidas seguidas` = 0 · `Resultado da tentativa` = vazio · `Prioridade` = 3 · `Entrada em` = `{{right_now}}` · `1ª tentativa em` = vazio |
| 4 | Troca de origem | Remove Contact Tag `nutricao-90d` → Remove Contact Tag `cad-inbound` (idempotente, mesmo se ausente) → Add Contact Tag `cad-outbound` → Add Contact Tag `reengajamento-ativo` | Ver "A troca de origem" abaixo |
| 5 | Reentrada no funil | Update Opportunity Stage → `Em cadência` | Dispara o Mestre de saída em no-op (destino é `Em cadência`, nó 1 encerra sem limpar) e o Alerta de Speed-to-lead (seção 2.11) com relógio novo, porque `1ª tentativa em` acabou de ser esvaziado no nó 3 — a reativação ganha sua própria medição de speed-to-lead de graça, sem campo novo |
| 6 | Mensagem de reabertura | Send WhatsApp (SMS fallback) | Texto `RE-1` (`biblioteca-mensagens.md`) → Update `Template usado` = `RE-1` |
| 7 | Aguardar resposta | Wait → Contact Replied | Tempo limite 2h — mesmo padrão do pós-M1 (seção 2.6): se respondeu, `Stop on Response` tira da régua |

### O bloco padrão de uma tentativa de reengajamento (TR1 a TR4)

Idêntico ao bloco padrão da Cadência 12x30 (seção 2.4) — inclusive o nó 2.5
de pausa individual (R-09) e os ramos 3b e 10b —, mesmo tipo de espera
(`Wait → Until specific time`, não relativo: reativação não tem urgência de
minuto, é a mesma lógica da 12x30, não da Cadência Inbound). Três diferenças
apenas:

1. `{n}` vira `TR{n}` no título da tarefa, que ganha o sufixo
   `— Reengajamento` (ex.: `[CADENCIA] TR1 · Ligar (telefone) —
   Reengajamento`) — mesmo prefixo `[CADENCIA]`, a rotina de manutenção
   (`rotina-limpar-tarefas.md`) não precisa de um quarto prefixo.
2. Só existem 4 tentativas, na tabela abaixo, em vez de 12.
3. Só na **TR1**, entre os nós 5 e 6 do bloco padrão, repita o par 5c/5d
   da seção 2.4 (`1ª tentativa em` = `{{right_now}}` · limpeza preventiva
   de `atraso-1a-tentativa`) — é a primeira tentativa de verdade *desta*
   rodada, mesmo raciocínio de T1 valer para a rodada original.

| TR | Dia | Horário | Canal | Delta do Wait (nó 1 do bloco) | Tag | Título da tarefa |
|---|---|---|---|---|---|---|
| 1 | D0 (dia da reativação) | 14:00 | Telefone | 0 d, a partir do fim do nó 7 acima | `fila-tel` | `[CADENCIA] TR1 · Ligar (telefone) — Reengajamento` |
| 2 | D3 | 10:00 | Ligação WhatsApp | 3 d | `fila-wa` | `[CADENCIA] TR2 · Ligar (WhatsApp) — Reengajamento` |
| 3 | D7 | 15:30 | Telefone | 4 d | `fila-tel` | `[CADENCIA] TR3 · Ligar (telefone) — Reengajamento` |
| 4 | D10 | 11:00 | Telefone | 3 d | `fila-tel` | `[CADENCIA] TR4 · Ligar (telefone) — Reengajamento` |

Canal majoritariamente telefone, mesmo motivo da Cadência Inbound (seção
2.10): `Permissão WhatsApp` de um lead que passou 90 dias sem contato
raramente ainda é `Sim`, então o seletor de canal do bloco padrão (nó 4 de
2.4) já desvia a maioria para telefone sozinho — a tabela só reforça o que
o portão faria de qualquer forma.

Reaproveitar o nó 10 do bloco padrão (2.4) sem alteração significa que
`Atendeu`, `Pediu retorno`, `Número errado` e `Não ligar` já removem o
contato deste workflow e entregam para o Pós-ligação (seção 4, que é
canal-agnóstico e não precisa saber que a tentativa veio do reengajamento)
exatamente como fariam na régua original — inclusive movendo etapa para
`Conectado`/`Retorno agendado`/`Descartado`. `reengajamento-ativo` sai
sozinho nesse caminho: é o Mestre de saída (seção 3, nó 4) que limpa,
porque qualquer um desses resultados tira a oportunidade de `Em cadência`.

### Sem resposta ao fim da TR4

Se a TR4 chega ao nó 10 do bloco padrão pelo ramo "tempo limite" (as 4
tentativas esgotaram sem conexão), em vez de "próxima tentativa":

| # | Ação | Configuração |
|---|---|---|
| 1 | Send WhatsApp (SMS fallback) | Texto `RE-2` (`biblioteca-mensagens.md`) |
| 2 | Update Contact Field | `Template usado` = `RE-2` |
| 3 | Update Contact Field | `Resultado da tentativa` = vazio |
| 4 | Add Contact Tag | `nutricao-90d` |
| 5 | Mover oportunidade | → `Nutrição` |

O nó 5 fecha o círculo: mover para `Nutrição` aciona o Mestre de saída
(que limpa `reengajamento-ativo`, entre outras) **e** dispara este mesmo
workflow de novo, do zero, porque `Allow Re-entry` está ligado — outro
relógio de 90 dias começa a contar sozinho. É a régua que se repete para
sempre até o lead conectar, pedir para não ser mais procurado, ou virar
oportunidade em outra etapa — nenhum destino é "arquivo morto" outra vez.

### A troca de origem (nó 4)

O roadmap pede "tag `cad-outbound`" na reativação. `cad-inbound` e
`cad-outbound` (seção 3) são documentados como "estado do lead, não fila"
— nunca removidos pelo Mestre de saída, porque registram a **origem**
histórica do lead. Este workflow é a única exceção deliberada a essa
regra, e por um motivo específico: origem histórica ("como este lead
chegou da primeira vez") e regra de roteamento ("qual cadência ele deve
correr agora") são coisas diferentes que essas duas tags fazem de uma vez
só, e aqui elas divergem — um lead que chegou por formulário (inbound) 90
dias atrás não é mais urgente hoje; tratá-lo como inbound de novo faria o
gatilho da seção 2.10 disparar a régua de minutos (5min a 3 dias) para um
contato que está frio há três meses, o oposto do que a reativação quer.
Por isso o nó 4 remove `cad-inbound` antes de somar `cad-outbound`: a
partir da reativação, o lead é tratado como outbound para fins de
roteamento, o que é verdade — está sendo abordado outbound, iniciativa
nossa, não dele. O preço é perder o registro de que ele nasceu inbound; é
um preço que vale pagar, porque é exatamente essa remoção que impede a
Cadência Inbound (seção 2.10) de disparar para um lead reativado: o filtro
dela (`cad-inbound` presente) já não casa com ninguém que passou por este
nó, sem precisar de reforço nenhum ali.

Isso resolve a Cadência Inbound, mas não resolve sozinho a Cadência 12x30
(seção 2.1): lá o filtro é o oposto (`cad-inbound` **ausente**), e a
reativação bate exatamente nesse filtro depois do nó 4 — é um problema
diferente, não o mesmo. `reengajamento-ativo` (nó 4, e o filtro somado à
seção 2.1) existe só para esse segundo caso: um lead reativado que nunca
tinha passado de verdade pela 12x30 (por exemplo, um inbound que só correu
a Cadência Inbound antes de cair em Nutrição) entraria nela de verdade —
`Allow Re-entry` desligado (D-06) só bloqueia quem já tem histórico
*naquele workflow específico*, e esse contato não tem. Duas proteções,
para dois gatilhos com filtros opostos, cada uma resolvendo o problema que
o seu gatilho de fato tem.

### Por que não literalmente `Novo lead`, como o roadmap descreve

O texto do roadmap (`ROADMAP-SALES-ENGAGEMENT.md`, R-08) diz "devolve para
`Novo lead`". O espírito — o lead sai do arquivo morto e reaparece na fila
do SDR — está mantido; o destino técnico mudou para `Em cadência`
diretamente, por dois motivos concretos, não por preferência:

1. Não existe, em nenhum lugar deste documento, um gatilho que promova
   `Novo lead` → `Em cadência` automaticamente (é uma lacuna que já
   existia antes deste item — hoje essa transição é manual, decisão do
   SDR ao revisar a fila). Se este workflow parasse em `Novo lead`, o
   lead reativado ficaria parado ali para sempre, o oposto do "Pronto
   quando" deste item ("o lead... volta à fila... sozinho").
2. Passar por `Novo lead` de propósito, mesmo que por um instante,
   aciona o Mestre de saída (seção 3, gatilho "qualquer etapa de
   destino") nesse destino intermediário — ele rodaria a limpeza inteira
   (incluindo aplicar `limpar-tarefas` e gravar a nota "Saída de cadência"
   num contato que não estava, de fato, saindo de cadência nenhuma) antes
   mesmo de a tarefa `TR1` existir. É ruído no histórico do contato e um
   risco de corrida real, ainda que pequeno, com a rotina horária de
   manutenção (`rotina-limpar-tarefas.md`), que lê `limpar-tarefas` a
   cada hora.

Registrar como lacuna nova para uma rodada futura: **L-07 — promoção
automática de `Novo lead` → `Em cadência`**. Hoje isso é decisão do SDR ao
revisar a fila; se o volume crescer, vale um gatilho (por exemplo,
`Contact Tag Added` numa tag de "telefone validado") que faça essa
promoção sozinha — o mesmo buraco que este item contornou indo direto
para `Em cadência` afeta igualmente todo lead novo, não só o reativado.

### Nova tag — T-13

`reengajamento-ativo`, especificada em `campos-e-tags.md`. Segue o mesmo
caminho de `atraso-1a-tentativa` (T-12, R-02): não está no lote das 11
tags já aprovadas por nome em `APROVADO.md`, então fica com linha própria,
ainda `[ ]`, até o dono trocar por `[x]`.

**Pronto quando (do roadmap):** o lead de hoje volta à fila em dezembro,
sozinho — a tarefa `[CADENCIA] TR1` nasce e o lead aparece nas listas
`Fila Telefone Hoje`/`Fila WhatsApp Hoje` (seções 8.2/8.3, que já filtram
por etapa `Em cadência` + tag de fila, sem precisar de lista nova) 90 dias
depois de entrar em `Nutrição`, sem qualquer ação humana entre as duas
datas.

---

## 2.13 Regras de pausa — R-09

`nao-perturbe` já resolve "este lead nunca mais" e a etapa `Em cadência`
resolve "este lead está correndo a régua". Falta o meio-termo: "não toque em
*ninguém* por alguns dias" (feriado, o SDR de férias) e "não toque *neste*
lead por alguns dias" (ele pediu, sem ser opt-out). São dois problemas de
tamanho diferente, e cada um usou a peça certa em vez de uma peça só fazendo
as duas coisas mal.

### Por que não é uma tag `pausado` aplicada a todo mundo antes do feriado

Foi o desenho literal do roadmap: uma tag checada no portão, e um "calendário
de feriados na janela do workflow". Pesquisado antes de montar: o GHL **não**
tem calendário de feriados dentro da janela de envio (Send Window) de um
workflow — é um Wait de dias-da-semana + hora, sem exceção de data (é pedido
em aberto na base de ideias pública da HighLevel, "Automation - Time Window -
turn off messaging during holidays", ainda não implementado). Reconstruir
isso com tag exigiria um workflow-relógio aplicando `pausado` em toda a base
ativa antes de cada feriado e removendo depois — um sistema novo, com
superfície de bug (tag que não sai a tempo prende o SDR seguinte), para
duplicar algo que o GHL **já** faz de graça pela tela.

O GHL tem, fora da janela de envio, um recurso de conta separado:
**Pausar Workflows em Datas Específicas** (Automação → Configurações →
Global Workflow Settings → Pause Workflow). Pesquisado na documentação da
HighLevel: você escolhe um intervalo de datas, marca quais workflows
publicados pausam nele, e opcionalmente marca "Annually" para o mesmo
intervalo se repetir todo ano — sem precisar reconfigurar em 2027. Limites:
até 15 intervalos cadastrados, cada intervalo com no máximo 15 dias de
diferença entre início e fim. O comportamento que importa aqui: contato que
estava **parado num nó de espera** quando a pausa começa não passa direto —
ele segue esperando até acabar o Wait normalmente, mas a **próxima ação de
verdade** (criar tarefa, mandar mensagem) que ele encontrar enquanto a
pausa está ativa fica represada até a pausa terminar, não só quem entra
pelo gatilho durante a janela. É o efeito que o "Pronto quando" pede —
nenhuma tarefa nova nasce durante o feriado — e cobre outbound, inbound e
reengajamento com a mesma configuração, sem tocar em node nenhum dos três
workflows. **Nível de confiança e como testar antes de confiar de vez:**
`APRENDIZADOS-CRM.md` — a leitura veio só de busca, os domínios de suporte
da HighLevel estão bloqueados para leitura direta neste ambiente.

**Isso não é preguiça de não construir; é o mesmo raciocínio do R-05 (Split
nativo em vez de If/Else alternado) e do R-02 (tag-alarme em vez de filtro
de data):** entre reconstruir um mecanismo e usar o que a plataforma já
oferece pronto, mais barato ganha quando os dois resolvem o mesmo problema —
e aqui o nativo resolve **melhor**, porque segura ações em qualquer ponto do
fluxo, não só na entrada.

### Configuração (manual, na tela — não sai por API)

Automação → Configurações → Global Workflow Settings → Pause Workflow →
Adicionar intervalo.

Workflows a marcar em todo intervalo: `Cadência 12x30`, `Cadência Inbound`,
`Reengajamento 90 dias` — os três únicos que criam tarefa ou mandam
mensagem para o lead. Não marque `Mestre de saída`, `Pós-ligação`,
`Pós-agendamento`, `Registro de Comparecimento`, `Loop do closer` nem
`Alerta de Speed-to-lead`: são registro/roteamento interno, não toque no
lead, e pausá-los deixaria o funil de métricas (R-01/R-03) cego durante o
feriado sem motivo — a métrica de quem conectou ou agendou continua valendo
mesmo com a operação de discagem parada.

Feriados nacionais fixos — marque `Annually`, uma vez, e nunca mais mexa:

| Data | Feriado |
|---|---|
| 01/01 | Confraternização Universal |
| 21/04 | Tiradentes |
| 01/05 | Dia do Trabalho |
| 07/09 | Independência |
| 12/10 | Nossa Senhora Aparecida |
| 02/11 | Finados |
| 15/11 | Proclamação da República |
| 25/12 | Natal |

Feriados móveis — Carnaval (2 dias), Sexta-feira Santa e Corpus Christi —
não têm data fixa (dependem da Páscoa), então `Annually` não serve: cadastre
o intervalo do ano corrente à mão, uma vez por ano, quando o calendário
sair. Férias do SDR: mesmo caminho, intervalo avulso (sem `Annually`), com
as datas informadas por quem está de fato saindo — se passar de 15 dias,
cadastre em blocos de até 15 (o limite é por intervalo, não por ano).

**Limite conhecido:** Reev, Meetime, Outreach e Salesloft (os três últimos,
por serem ferramentas de vendas puras) têm calendário de feriados integrado
ao schedule da sequência, recalculado automaticamente ano a ano — o GHL não
tem isso nativamente (é pedido aberto na base de ideias deles). O preço de
usar o recurso de conta em vez de um relógio próprio é esse: feriado móvel
exige uma revisão anual manual de 3 datas. Vale o preço: é 3 datas por ano
contra um workflow inteiro de tag em massa para manter.

### Pausa individual — a tag `pausado`

Para o caso que o calendário não cobre: **um** lead pediu para não ser
procurado esta semana (viagem, "me liga mês que vem"), sem isso ser opt-out
— `nao-perturbe` seria overkill e ligaria o DND nativo, que é permanente por
desenho (seção 4, ramo `Não ligar`). Tag nova, `pausado` (T-14,
`campos-e-tags.md`), aplicada manualmente pelo SDR e removida manualmente
quando o lead volta a valer a pena tentar.

Checada num portão próprio, separado do portão principal (nó 2.5 da seção
2.4 e nó 1.5 da seção 2.10, detalhados ali): represa a tentativa num laço de
espera curta em vez de tirar o lead do workflow, porque pausa é "espera",
não "saída" — a diferença que justifica não reaproveitar o nó 3/3b
existente, que já significa saída definitiva. O Mestre de saída (seção 3,
nó 4) limpa a tag se o lead sair de cadência por um motivo real enquanto
pausado, e o Alerta de Speed-to-lead (seção 2.11, nó 2) ignora quem está
pausado, para não soar alarme de atraso num lead parado de propósito.

Nova lista inteligente `Pausados Individualmente` (seção 8.15) para o gestor
não esquecer quem está represado.

### Nova tag — T-14

`pausado`, especificada em `campos-e-tags.md`. Mesmo caminho de
`atraso-1a-tentativa` (T-12) e `reengajamento-ativo` (T-13): fora do lote
das 11 tags já aprovadas por nome em `APROVADO.md`, linha própria, ainda
`[ ]`.

**Pronto quando (do roadmap):** o Natal não gera 120 tarefas — os três
workflows que tocam o lead ficam pausados pelo recurso nativo da conta
durante o intervalo cadastrado, represando qualquer tarefa/mensagem que
tentaria disparar nesses dias; e um lead específico pode ser represado sem
depender de calendário nenhum, via `pausado`, sem perder a posição na régua.

---

## 3. Workflow "Mestre de saída"

O guarda-costas da operação: garante que sair de "Em cadência" limpa tudo.

### Gatilho
**Opportunity Stage Changed** — Pipeline `Pré-vendas`, qualquer etapa de
destino.

### Configurações
| Configuração | Valor |
|---|---|
| Allow Re-entry | **Ligado** (precisa disparar em toda mudança de etapa) |
| Janela de envio | Sem janela (é limpeza interna, não manda mensagem) |
| Stop on Response | Desligado |

### Nós
| # | Ação | Configuração |
|---|---|---|
| 1 | If/Else | Etapa de destino **é** `Em cadência` → **encerra aqui** (não limpa nada). Senão, segue |
| 2 | Remove from Workflow | `Cadência 12x30` |
| 3 | Remove from Workflow | `Qualificação por IA no WhatsApp` |
| 4 | Remove Contact Tag | `fila-quente`, `fila-tel`, `fila-wa`, `fila-linkedin`, `atraso-1a-tentativa` (R-02), `reengajamento-ativo` (R-08), `pausado` (R-09) |
| 5 | Add Contact Tag | `limpar-tarefas` |
| 6 | Add Note | `Saída de cadência · etapa: {{opportunity.pipeline_stage}} · tentativa {{contact.tentativa_no}} · resultado {{contact.resultado_da_tentativa}}` |

O nó 1 existe porque o gatilho é "qualquer etapa": sem ele, mover o lead
*para* a cadência acionaria a limpeza e mataria a cadência no nascimento.

Não removo `conectado-hoje`, `nao-perturbe`, `telefone-invalido`,
`nutricao-90d`, `cad-inbound` e `cad-outbound`: são estado do lead, não fila.
`pausado` (R-09, seção 2.13) entra no nó 4 mesmo sendo estado individual, não
fila — porque, diferente de `nao-perturbe`, ela só tem sentido **dentro** de
`Em cadência` (represar uma tentativa que ainda vai acontecer). Uma vez que o
lead sai de cadência por um motivo real (conectou, número errado, não
ligar), a pausa perdeu o objeto: não sobra tentativa nenhuma para represar, e
manter a tag viva só confundiria uma reativação futura pelo Reengajamento
90 dias (seção 2.12), que já teria um SDR pausando um lead que nem está mais
correndo régua nenhuma.
`reengajamento-ativo` (R-08, seção 2.12) entrou na lista do nó 4 porque ela
**é** fila, só que da régua de reengajamento em vez da 12x30 — o mesmo
motivo de `fila-tel`/`fila-wa` estarem lá: nasce ao entrar em `Em cadência`
pela reativação e não tem por que sobreviver a uma saída dela, qualquer que
seja o resultado (conectou, número errado, não ligar ou esgotou as 4
tentativas).

---

## 4. Workflow "Pós-ligação"

Traduz a classificação do SDR em consequência. É o único lugar que mexe nos
contadores.

### Gatilho
**Contact Changed** com filtro `Resultado da tentativa` foi alterado.
(Se a sua versão não tiver filtro de campo alterado no gatilho: use
**Contact Tag Added → `resultado-registrado`** e faça o SDR aplicar a tag; ou
crie 6 links de gatilho, um por resultado. O primeiro caminho é o limpo.)

### Configurações
| Configuração | Valor |
|---|---|
| Allow Re-entry | **Ligado** (um disparo por tentativa) |
| Janela de envio | Sem janela |

### Nós
| # | Ação | Configuração |
|---|---|---|
| 1 | If/Else | `Resultado da tentativa` está vazio → encerra (foi a limpeza do nó 5 da cadência que disparou, não o SDR) |
| 2 | If/Else | A tentativa foi de WhatsApp? (`fila-wa` presente **ou** a tarefa aberta tem `(WhatsApp)` no título) → Math: `Tentativas WhatsApp` + 1. Senão → Math: `Tentativas telefone` + 1 |
| 3 | Math Operation | `Total de ligações` = `Total de ligações` + 1 |
| 4 | If/Else múltiplo | Ramifica pelos 6 resultados, abaixo |

O nó 2 repete de propósito a mesma checagem de canal que já existe no ramo
`Caixa postal`/`Não atendeu`, em vez de calcular uma vez só e guardar num
campo: são dois pontos do fluxo que precisam saber o canal, e mais um campo
"canal desta tentativa" só para não repetir uma condição de uma linha é troca
ruim (R-01, feito em 18/09/2026).

#### Ramo `Atendeu`
| # | Ação |
|---|---|
| 1 | If/Else | A tentativa foi de WhatsApp? (mesma checagem do nó 2) → Math: `Conexões WhatsApp` + 1. Senão → Math: `Conexões telefone` + 1 |
| 2 | Math: `Total de conexões` + 1 |
| 3 | Update: `WA não atendidas seguidas` = 0 |
| 4 | Add Contact Tag `conectado-hoje` |
| 5 | Remove Contact Tag `fila-tel`, `fila-wa` |
| 6 | Mover oportunidade → `Conectado` (dispara o Mestre de saída, que faz a limpeza) |
| 7 | Update Contact Field `Data conectado` = `{{right_now}}` (R-03 — só marca; não repete se já preenchido, mas escrever de novo é barato e não quebra nada) |
| 8 | Add Task `[CONECTADO] Qualificar e agendar` · vence hoje · SDR |
| 9 | Add Note `Atendeu na T{{contact.tentativa_no}}` |

#### Ramo `Caixa postal` e ramo `Não atendeu` (idênticos)
| # | Ação |
|---|---|
| 1 | If/Else: a tentativa foi de WhatsApp? (`fila-wa` presente **ou** a tarefa aberta tem `(WhatsApp)` no título) → Math: `WA não atendidas seguidas` + 1. Senão → Update: `WA não atendidas seguidas` = 0 |
| 2 | Remove Contact Tag `fila-tel`, `fila-wa` |
| 3 | Add Contact Tag `limpar-tarefas` |
| 4 | **Nada de mudança de etapa** — o lead continua em cadência |

O reset no ramo "senão" é o que faz a regra "2 seguidas vira telefone" se
comportar como *seguidas* e não como *acumuladas no total*.

#### Ramo `Número errado`
| # | Ação |
|---|---|
| 1 | Add Contact Tag `telefone-invalido` |
| 2 | Remove Contact Tag `fila-tel`, `fila-wa` |
| 3 | If/Else: o contato tem e-mail ou Instagram? → mover para `Nutrição` + tag `nutricao-90d`. Senão → mover para `Descartado` |
| 4 | Internal Notification para o gestor: `Telefone inválido: {{contact.name}} — revisar a fonte da lista` |

Número errado não é culpa do lead: se há outro canal, ele vira nutrição em vez
de lixo.

#### Ramo `Pediu retorno`
| # | Ação |
|---|---|
| 1 | Update: `Prioridade` = 5 |
| 2 | Remove Contact Tag `fila-tel`, `fila-wa` |
| 3 | Add Contact Tag `fila-quente` |
| 4 | Mover oportunidade → `Retorno agendado` |
| 5 | Add Task `[RETORNO] Ligar de volta` · vence: `Data do retorno` (campo S-01) ou hoje+1 se vazio · SDR |

Sem o campo `Data do retorno` (lacuna L-01) este ramo funciona, mas a tarefa
vence sempre em hoje+1 e a lista "Retornos" não sabe o que é de hoje.

#### Ramo `Não ligar`
| # | Ação |
|---|---|
| 1 | Add Contact Tag `nao-perturbe` |
| 2 | **Set Contact DND** = ligado (todos os canais) |
| 3 | Remove Contact Tag `fila-tel`, `fila-wa`, `fila-quente` |
| 4 | Remove from Workflow: `Cadência 12x30` e `Qualificação por IA no WhatsApp` |
| 5 | Mover oportunidade → `Descartado` |
| 6 | Add Note `Opt-out registrado em {{right_now}}` |

O DND nativo é o que impede qualquer workflow futuro de mandar mensagem. Tag
sozinha não segura: workflow novo que ninguém lembrou de filtrar volta a
incomodar o lead. Este é o único nó deste documento que eu trataria como
não-negociável.

---

## 5. Workflow "Pós-agendamento"

### Gatilho
**Appointment Status** — Calendário: `Reunião com closer` · Status:
`Confirmed` (e `Booked`/`New`, se a sua versão listar separado).

**Não use "Customer Booked Appointment"**: ele só dispara quando o próprio lead
agenda pelo link. No nosso desenho é o SDR que agenda na tela junto com o
lead, e esse gatilho não dispara em agendamento manual — a operação inteira
ficaria muda.

### Nós
| # | Ação | Configuração |
|---|---|---|
| 1 | Mover oportunidade → `Reunião agendada` | Aciona o Mestre de saída |
| 2 | Update Contact Field | `Data agendado` = `{{right_now}}` (R-03 — marca o instante em que o SDR agendou, não o horário da reunião) |
| 3 | Remove from Workflow | `Cadência 12x30`, `Qualificação por IA no WhatsApp` |
| 4 | Math Operations em série | Calcula `Nota de qualificação` (seção 9.1) |
| 5 | Update Contact Field | `Prioridade` = 5 |
| 6 | Add Note | Resumo da qualificação (modelo abaixo) |
| 7 | Send WhatsApp | Confirmação imediata ao lead |
| 8 | Wait até 24h antes | → Send WhatsApp lembrete |
| 9 | Wait até 3h antes | → Send WhatsApp lembrete |
| 10 | Wait até 30min antes | → Send WhatsApp lembrete curto |
| 11 | Assign to User | Closer dono do horário |
| 12 | Internal Notification | E-mail + SMS para o closer |

Nos nós 8–10 use Wait → "relativo ao início do compromisso" (Appointment Start
Date), não delay fixo: reagendamento move os lembretes junto.

**Modelo da nota (nó 6)**
```
REUNIÃO AGENDADA · nota {{contact.nota_de_qualificacao}}/100
Agendado por: {{user.name}} · Para: {{appointment.start_time}}

Empresa: {{contact.company_name}} · Segmento: {{contact.segmento}}
Site: {{contact.site}} · IG: {{contact.instagram}}

BANT
Budget: {{contact.budget}} · Decisor: {{contact.decisor}} · Prazo: {{contact.prazo}}

Diagnóstico
Clientes novos/mês: {{contact.clientes_novos_por_mes}}
Anúncios: {{contact.investe_em_anuncios}} · Investimento: {{contact.investimento_mensal_em_anuncios}}
Plataformas: {{contact.plataformas_de_anuncio}}
Agência: {{contact.ja_teve_agencia}} — {{contact.experiencia_com_agencia}}
Time: {{contact.tem_time_comercial}} · Atende leads: {{contact.quem_atende_os_leads}}
CRM: {{contact.usa_crm}} · Canal principal: {{contact.canal_principal_de_venda}}

Dor principal: {{contact.dor_principal}}
Preenchido por: {{contact.qualificacao_preenchida_por}}
Histórico: {{contact.total_de_ligacoes}} ligações, {{contact.total_de_conexoes}} conexões, atendeu na T{{contact.tentativa_no}}
```

**Mensagem de confirmação (nó 7)**
> {{contact.first_name}}, reunião confirmada para
> {{appointment.start_time}}. Vou te mandar o link aqui mesmo 30 min antes. Se
> precisar remarcar, responde esta mensagem.

---

## 5.1 Workflow "Loop do closer — veredito pós-reunião" — F-03

A seção 5 fecha o que o SDR controla: agendou, o closer recebeu a nota e o
resumo. O que o SDR **nunca** descobre é se agendou bem — e sem isso a nota de
qualificação da seção 9 é uma opinião que ninguém conferiu. Reev, Meetime,
Outreach e Salesloft fecham esse loop do mesmo jeito: um campo de resultado da
reunião que alimenta um relatório agregado, olhado semana ou mês depois. Aqui
o preenchimento do closer **é** o gatilho: o workflow compara a nota que o SDR
(ou a IA) deu com o veredito do closer no instante em que ele é registrado, e
só interrompe o gestor quando os dois discordam. Um concorrente olhando a tela
vê "o closer marca um select"; não vê que aquele clique dispara uma
comparação imediata, não um relatório do mês seguinte.

### Gatilho
**Contact Changed** com filtro `Reunião foi qualificada` foi alterado.
(Sem filtro de campo alterado na sua versão: mesma saída da seção 4 —
Contact Tag Added `veredito-registrado`, aplicada pelo closer junto com o
campo.)

### Configurações
| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | O closer pode corrigir o veredito depois; cada alteração reavalia |
| Janela de envio | Sem janela | É registro e alerta interno, não mensagem ao lead |
| Stop on Response | Desligado | Não há mensagem ao lead aqui |

### Nós
| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Portão | If/Else | `Reunião foi qualificada` está vazio → **encerra** (evita disparo por outra edição de campo que não seja o veredito) |
| 2 | Carimbo | Update Contact Field | `Data do veredito do closer` = `{{right_now}}` |
| 3 | Registro | Add Note | `Veredito do closer: {{contact.reuniao_foi_qualificada}} · motivo: {{contact.motivo_da_desqualificacao}} · nota do SDR/IA na hora: {{contact.nota_de_qualificacao}}` |
| 4 | Roteamento | If/Else múltiplo por `Reunião foi qualificada` | ver ramos abaixo |
| 5 | **Alerta de calibração (alta)** | If/Else | `Nota de qualificação` ≥ 70 **E** `Reunião foi qualificada` = `Não` → Internal Notification ao gestor: `Nota {{contact.nota_de_qualificacao}} mas o closer marcou Não ({{contact.motivo_da_desqualificacao}}) — revisar a régua da seção 9 com {{contact.name}}.` |
| 6 | **Alerta de calibração (baixa)** | If/Else | `Nota de qualificação` < 45 **E** `Reunião foi qualificada` = `Sim` → Internal Notification ao gestor: `Nota baixa ({{contact.nota_de_qualificacao}}) mas o closer marcou Sim — a régua pode estar descartando lead bom. Revisar {{contact.name}}.` |

Os cortes 70 e 45 dos nós 5 e 6 não são novos: são as mesmas fronteiras das
faixas A/B da seção 9.1. Reaproveitar evita uma segunda régua para a régua.

#### Ramos do nó 4
| Veredito | Ação |
|---|---|
| `Sim` | Nenhuma mudança de etapa. A venda continua no `FUNIL DE VENDAS`, fora deste pipeline e fora desta automação — não é este workflow que move o lead para lá |
| `Parcial` | Mover oportunidade → `Nutrição` + Add Contact Tag `nutricao-90d` |
| `Não`, motivo = `Timing errado` | Mover oportunidade → `Nutrição` + Add Contact Tag `nutricao-90d` (sem fit **agora** não é sem fit nunca) |
| `Não`, qualquer outro motivo | Mover oportunidade → `Descartado` |

O motivo só decide o destino quando o veredito é `Não`; `Parcial` já é
tratado como nutrição direto, sem olhar o motivo — é o mesmo critério do ramo
`Não`/`Timing errado`, então não duplico a checagem.

**Pronto quando (herdado do F-03 no roadmap):** dá para dizer "nota ≥ 70
acerta X%" sem planilha (lista 8.7), e o gestor sabe de uma nota mal calibrada
no dia da reunião, não no fechamento do mês.

---

## 5.2 Workflow "Registro de Comparecimento" — R-03

A seção 5 marca `Data agendado` no instante em que o SDR reserva o horário.
Falta o terceiro marco do funil: a reunião **aconteceu**. Sem ele, "compareceu"
vira algo que só existe na cabeça do closer, e o funil do roadmap (R-03:
entraram / conectaram / agendaram / compareceram) perde a última perna.

### Gatilho
**Appointment Status** — Calendário: `Reunião com closer` · Status: `Showed`

Workflow curto e separado do Pós-agendamento de propósito: são dois eventos
do mesmo agendamento, em momentos diferentes (reservar vs. comparecer), e
misturar os dois num workflow só faria o segundo gatilho reabrir todos os nós
de lembrete da seção 5, que já rodaram.

### Configurações
| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | Reagendamento gera um novo `Showed` no futuro |
| Janela de envio | Sem janela | É registro interno, não manda mensagem ao lead |
| Stop on Response | Desligado | Não há mensagem ao lead aqui |

### Nós
| # | Ação | Configuração |
|---|---|---|
| 1 | If/Else | `Data compareceu` está vazio → segue (evita sobrescrever se o status oscilar) |
| 2 | Update Contact Field | `Data compareceu` = `{{right_now}}` |
| 3 | Add Note | `Compareceu à reunião · {{right_now}}` |

Não mexo em etapa aqui: comparecer não move a oportunidade (quem decide o
destino é o veredito do closer, seção 5.1). Este workflow só marca o carimbo
que a seção 8 lê.

**Pronto quando (compõe o R-03 no roadmap):** existe carimbo de "compareceu"
tão confiável quanto os de "conectou" e "agendou" — os três lidos pelas
listas 8.10 a 8.12.

---

## 6. Workflow "Qualificação por IA no WhatsApp"

### Entrada
Só por `Add to Workflow` vindo da Cadência (seção 2.7). Sem gatilho próprio —
assim você nunca tem IA conversando com lead que não passou pelo portão.

### Configurações
| Configuração | Valor |
|---|---|
| Janela de envio | 08:30–20:00, seg–sáb |
| Stop on Response | **Desligado** (aqui a resposta é o objetivo, não a saída) |
| Allow Re-entry | Desligado |

### Estrutura
Duas formas de montar. Recomendo a **A**.

**A — Conversation AI (Bot nativo), modo perguntas + agendamento**

Um nó `Conversation AI` com:
- Canal: WhatsApp
- Modo: Query + Appointment Booking
- Calendário: `Reunião com closer`
- Mapeamento de campos: cada pergunta grava no campo correspondente
- Limite: **uma pergunta por mensagem**, máximo 8 perguntas na conversa
- Ao fim (ou quando o lead demonstrar interesse): oferece o link do calendário
- Nó seguinte: Update `Qualificação preenchida por` = `IA WhatsApp`

Prompt do bot:
```
Você é assistente de pré-vendas da {{location.name}}. Fala português do Brasil,
informal e curto — no máximo 2 linhas por mensagem, como uma pessoa digitando
no WhatsApp. Nunca use bullet points, emoji em excesso ou texto de vendedor.

REGRA DE OURO: uma pergunta por mensagem. Espere a resposta antes da próxima.
Nunca faça duas perguntas juntas. Nunca repita uma pergunta já respondida.

Ordem das perguntas (pule a que já estiver preenchida no contato):
1. Permissão: "posso te ligar rapidinho ou prefere resolver por aqui?"
   -> grava Permissão WhatsApp (Sim se autorizar ligação, Não se recusar)
2. Quantos clientes novos vocês fecham por mês hoje?
   -> Clientes novos por mês: Até 10 / 11-30 / 31-100 / 100+
3. Vocês investem em anúncio hoje?
   -> Investe em anúncios: Sim / Já investiu e parou / Nunca
4. Se sim: quanto mais ou menos por mês? -> Investimento mensal em anúncios
   E em quais plataformas? -> Plataformas de anúncio
5. Já trabalhou com agência? Como foi?
   -> Já teve agência + Experiência com agência
6. Quem atende os leads que chegam hoje? -> Quem atende os leads
7. Qual o maior problema hoje na captação? -> Dor principal
8. Isso é algo para resolver agora ou está mais no radar? -> Prazo

Se o lead responder algo que já mata a qualificação ("não tenho interesse",
"não me manda mais mensagem"), pare imediatamente, agradeça em uma linha e
não faça mais perguntas.

Quando tiver respondido pelo menos as perguntas 2, 3 e 8, ou quando o lead
demonstrar interesse, ofereça o agendamento: "quer que eu já reserve 30 min com
um especialista nosso? Me diz um dia e horário que eu te mando a confirmação."

Nunca prometa preço, desconto, prazo de resultado ou garantia. Nunca invente
caso de cliente. Se o lead perguntar preço, diga que depende do diagnóstico e
que é exatamente o assunto da reunião.
```

**B — Sem Conversation AI (só nós)**

Corrente de 8 blocos: `Send WhatsApp (pergunta)` → `Wait → Contact Replied,
tempo limite 24h` → `Update Contact Field` (com a resposta) → próxima. No
tempo limite, pula para a pergunta seguinte ou encerra. Funciona sem
Conversation AI contratado, mas não interpreta resposta livre — você acaba
tendo que ler as conversas na mão.

### Saída
| # | Ação |
|---|---|
| 1 | Update `Qualificação preenchida por` = `IA WhatsApp` |
| 2 | Math: recalcula `Nota de qualificação` (seção 9.1) |
| 3 | If/Else: nota ≥ 45 → Add Contact Tag `fila-quente` + Update `Prioridade` = 5 + Internal Notification para o SDR: "lead qualificado pela IA, ligar hoje" |
| 4 | If/Else: nota < 25 **e** `Budget` = `Não tem` → mover para `Nutrição` + tag `nutricao-90d` |

---

## 7. Calendário do closer + formulário de qualificação

### 7.1 Calendário `Reunião com closer`

Calendários → Novo → **Round Robin** (se houver mais de um closer) ou Simple.

| Configuração | Valor | Por que |
|---|---|---|
| Duração | 45 min | Reunião de diagnóstico |
| Intervalo entre slots | 15 min | Closer respira e anota |
| Aviso mínimo | 2 horas | O SDR consegue agendar para o mesmo dia |
| Máximo por dia | Conforme o closer | Evita dia impossível |
| Disponibilidade | Seg–sex, horário comercial | |
| Confirmação automática | Ligada | |
| Fuso | Do contato | Aqui sim: o lead vê o horário dele |
| **Sticky Contact** | **DESLIGADO** | Crítico. Ligado, o formulário pré-enche com o último contato daquele navegador — e o SDR, agendando um lead atrás do outro na mesma aba, sobrescreve os dados de um no cadastro do outro |
| Permitir reagendamento pelo lead | Ligado | |
| Adicionar convidados | Desligado | |

Na aba Notificações: confirmação por e-mail para o lead e para o closer. Os
lembretes de WhatsApp saem do workflow da seção 5, não daqui — assim você não
tem dois sistemas mandando lembrete.

### 7.2 Formulário `Qualificação SDR`

Sites → Formulários → Novo. Anexe ao calendário em
**Calendário → Formulários → Formulário personalizado**.

| Ordem | Campo do formulário | Mapeado para | Obrigatório |
|---|---|---|---|
| 1 | Nome | `first_name` / `last_name` | Sim |
| 2 | Telefone | `phone` | Sim |
| 3 | E-mail | `email` | Sim |
| 4 | Empresa | `company_name` | Sim |
| 5 | Segmento | `Segmento` | Sim |
| 6 | Site | `Site` | Não |
| 7 | Instagram | `Instagram` | Não |
| 8 | Clientes novos por mês | `Clientes novos por mês` | Sim |
| 9 | Investe em anúncios | `Investe em anúncios` | Sim |
| 10 | Investimento mensal | `Investimento mensal em anúncios` | Não |
| 11 | Plataformas | `Plataformas de anúncio` | Não |
| 12 | Já teve agência | `Já teve agência` | Sim |
| 13 | Experiência com agência | `Experiência com agência` | Não |
| 14 | Tem time comercial | `Tem time comercial` | Sim |
| 15 | Quem atende os leads | `Quem atende os leads` | Sim |
| 16 | Usa CRM | `Usa CRM` | Não |
| 17 | Canal principal de venda | `Canal principal de venda` | Não |
| 18 | Budget | `Budget` | Sim |
| 19 | Decisor | `Decisor` | Sim |
| 20 | Dor principal | `Dor principal` | Sim |
| 21 | Prazo | `Prazo` | Sim |
| 22 | Qualificação preenchida por | `Qualificação preenchida por` | Sim, valor padrão `SDR` |
| 23 | Consentimento de contato | checkbox | Sim |

Configurações do formulário:
- **Sticky Contact: desligado** (repetindo porque é onde mais se erra).
- "Atualizar campos vazios apenas": **desligado** — o SDR corrige informação
  errada durante a ligação e precisa que sobrescreva.
- Sem captcha (atrasa o SDR; o formulário não é público).
- Layout de uma coluna, todos os campos na mesma tela, sem paginação: o SDR
  preenche ouvindo o lead e não pode perder tempo navegando.

O SDR abre esse link, preenche enquanto conversa, escolhe o horário e envia. O
envio cria o agendamento e dispara a seção 5. O que o SDR fala enquanto
preenche — abertura, perguntas na ordem dos campos deste formulário, ponte
para o agendamento e objeções — está em `script-de-ligacao.md` (R-06).

---

## 8. Listas inteligentes

Contatos → Filtros → salvar como lista inteligente. Marque como favorita para
aparecer na barra lateral do SDR.

### 8.1 `Fila Quente`
| Item | Configuração |
|---|---|
| Filtros | tag `fila-quente` presente **E** tag `nao-perturbe` ausente **E** etapa da oportunidade em (`Em cadência`, `Conectado`, `Retorno agendado`) |
| Colunas | Nome · Empresa · Telefone · `Prioridade` · `Tentativa nº` · `Resultado da tentativa` · `Nota de qualificação` · Última atividade |
| Ordenação | `Prioridade` desc, depois `Tentativa nº` asc |

### 8.2 `Fila Telefone Hoje`
| Item | Configuração |
|---|---|
| Filtros | tag `fila-tel` presente **E** `nao-perturbe` ausente **E** `telefone-invalido` ausente **E** `conectado-hoje` ausente **E** etapa = `Em cadência` |
| Colunas | Nome · Empresa · Telefone · `Tentativa nº` · `Prioridade` · `Resultado da tentativa` · Tarefas abertas |
| Ordenação | `Prioridade` desc, depois `Tentativa nº` asc |

Ordenar por tentativa crescente é de propósito: lead na T1 tem muito mais
chance de atender do que o da T11. A fila devolve primeiro o que converte.

### 8.3 `Fila WhatsApp Hoje`
| Item | Configuração |
|---|---|
| Filtros | tag `fila-wa` presente **E** `nao-perturbe` ausente **E** `conectado-hoje` ausente **E** `Permissão WhatsApp` = `Sim` **E** etapa = `Em cadência` |
| Colunas | Nome · Empresa · Telefone · `Tentativa nº` · `WA não atendidas seguidas` · `Prioridade` |
| Ordenação | `Prioridade` desc, depois `WA não atendidas seguidas` asc |

### 8.4 `Retornos`
| Item | Configuração |
|---|---|
| Filtros | etapa = `Retorno agendado` **OU** `Resultado da tentativa` = `Pediu retorno`; **E** `nao-perturbe` ausente |
| Colunas | Nome · Empresa · Telefone · `Data do retorno` · `Prioridade` · `Nota de qualificação` · Tarefas abertas |
| Ordenação | `Data do retorno` asc (sem o campo S-01: "Última atividade" asc — pior, mas funciona) |

### 8.5 Sugerida por mim: `Sem resultado ontem`
| Item | Configuração |
|---|---|
| Filtros | tag `limpar-tarefas` presente **E** tag `fila-tel`/`fila-wa` ausentes |
| Para quê | É o buraco de gestão: tentativas que venceram sem o SDR classificar. Se esta lista cresce, a operação está mentindo nos números |

### 8.6 `Conexão por Tentativa` — R-01
| Item | Configuração |
|---|---|
| Filtros | `Total de conexões` ≥ 1 |
| Colunas | Nome · `Tentativa nº` · `Total de ligações` · `Total de conexões` · `Tentativas telefone` · `Conexões telefone` · `Tentativas WhatsApp` · `Conexões WhatsApp` |
| Ordenação | `Tentativa nº` asc |

Funciona sem um campo extra de "tentativa em que conectou": ao registrar
`Atendeu`, o nó 10 da cadência (seção 2.4) remove o contato do workflow —
`Tentativa nº` para de mudar exatamente no valor em que ele conectou. Filtrar
por quem já conectou e ordenar por essa tentativa responde "qual tentativa
conecta mais" olhando a lista ordenada, sem planilha — é o "Pronto quando" do
R-01 do roadmap.

### 8.7 `Calibração da Régua` — F-03
| Item | Configuração |
|---|---|
| Filtros | `Reunião foi qualificada` não vazio |
| Colunas | Nome · `Nota de qualificação` · `Reunião foi qualificada` · `Motivo da desqualificação` · `Data do veredito do closer` |
| Ordenação | `Nota de qualificação` desc |

Cruza, reunião a reunião, a nota que o SDR ou a IA deram com o veredito do
closer. Contar visualmente quantos `Sim` e `Não` caem acima de 70 responde
"nota ≥ 70 acerta X%" sem planilha — o "Pronto quando" do F-03. O alerta em
tempo real da seção 5.1 (nós 5 e 6) avisa o gestor de um erro no dia; esta
lista mostra o padrão acumulado quando ele quiser olhar.

### 8.8 `Atraso na 1ª Tentativa` — R-02
| Item | Configuração |
|---|---|
| Filtros | tag `atraso-1a-tentativa` presente |
| Colunas | Nome · Empresa · Telefone · `Entrada em` · `1ª tentativa em` (sempre vazio nesta lista) · Tarefas abertas |
| Ordenação | Última atividade asc (quem está parado há mais tempo aparece primeiro) |

A tag só existe porque o workflow da seção 2.11 a aplicou depois do tempo de
espera daquele relógio (o prazo varia por origem — R-07 — e é a seção 2.11
que guarda o valor certo) sem `1ª tentativa em` preenchido — a lista não faz
conta nenhuma, só lê a marca que o relógio já fez. É o "Pronto quando" do
R-02: dá para apontar o lead atrasado sem SDR ligar, sem abrir planilha.

### 8.9 `Funil — Entraram no Mês` — R-03
| Item | Configuração |
|---|---|
| Filtros | Pipeline = `Pré-vendas` **E** `Data de criação` da oportunidade dentro do mês atual (filtro nativo "Este mês", sem campo novo) |
| Colunas | Nome · Empresa · Etapa atual · `Data de criação` |
| Ordenação | `Data de criação` desc |

Se a sua versão do construtor de lista de contatos não expuser filtro por
data de criação da **oportunidade** (só por data de criação do contato), use
a Lista Inteligente de Oportunidades dentro do próprio pipeline `Pré-vendas`
— ali o filtro `Data de criação` é nativo. Por que não um campo novo: data de
criação da oportunidade não muda quando o lead avança de etapa, então não
tem o defeito do `Last Stage Change Date` (que só reflete a etapa atual) —
pesquisado antes de desenhar C-20/C-21/C-22 abaixo.

### 8.10 `Funil — Conectaram no Mês` — R-03
| Item | Configuração |
|---|---|
| Filtros | `Data conectado` dentro do mês atual (filtro relativo nativo de campo `DATE`) |
| Colunas | Nome · Empresa · `Data conectado` · `Tentativa nº` |
| Ordenação | `Data conectado` desc |

### 8.11 `Funil — Agendaram no Mês` — R-03
| Item | Configuração |
|---|---|
| Filtros | `Data agendado` dentro do mês atual |
| Colunas | Nome · Empresa · `Data agendado` · `Nota de qualificação` |
| Ordenação | `Data agendado` desc |

### 8.12 `Funil — Compareceram no Mês` — R-03
| Item | Configuração |
|---|---|
| Filtros | `Data compareceu` dentro do mês atual |
| Colunas | Nome · Empresa · `Data compareceu` · `Reunião foi qualificada` |
| Ordenação | `Data compareceu` desc |

As quatro listas (8.9 a 8.12) respondem "a taxa de conexão do mês" sem
contar na mão: cada uma mostra, no topo, o total de contatos que bateram
naquele filtro — dividir o total de 8.10 pelo de 8.9 é a taxa de conexão do
mês, sem abrir planilha nem somar linha por linha. É o "Pronto quando" do
R-03. Cada campo `DATE` novo (C-20 a C-22) grava o marco na hora em que ele
acontece pela primeira vez e não muda depois, então a oportunidade continua
contando no mês em que **cruzou** aquele marco mesmo depois de avançar para
a etapa seguinte — diferente de filtrar pela etapa atual, que subcontaria
quem já foi para `Reunião agendada` ou saiu do pipeline.

### 8.13 `Resposta por Template` — R-04
| Item | Configuração |
|---|---|
| Filtros | `Sinal recebido` = `Resposta de mensagem` |
| Colunas | Nome · `Template usado` · `Data e hora do sinal` · Etapa atual |
| Ordenação | `Template usado` asc |

Agrupar visualmente por `Template usado` responde "qual abertura teve mais
resposta" (Pronto quando do R-04) sem campo de contagem novo: a
interceptação de sinal do F-01 (seção 2.9.3) já grava toda resposta fora do
fluxo via `Customer Replied`; esta lista só cruza esse registro com o código
gravado pela seção 2.6. Detalhes de versionamento e o limite conhecido do
campo `Sinal recebido` (sobrescrito por sinal mais recente) estão em
`biblioteca-mensagens.md`.

### 8.14 `Reengajamento em Curso` — R-08
| Item | Configuração |
|---|---|
| Filtros | tag `reengajamento-ativo` presente |
| Colunas | Nome · Empresa · Telefone · `Tentativa nº` · `Prioridade` · `Template usado` · Tarefas abertas |
| Ordenação | `Tentativa nº` asc |

Separa quem está na régua TR1-TR4 (seção 2.12) de quem está numa rodada
nova de verdade — as filas do dia (8.2/8.3) já mostram os dois juntos
porque compartilham etapa e tags de fila; esta lista é só para o gestor
que quer ver, à parte, quanto volume o reengajamento está gerando e como
essa fatia responde — o mesmo raciocínio de `cad-inbound`/`cad-outbound`
já valer para separar régua na lista 8.6, sem lista nova até agora ter
sido necessária lá.

### 8.15 `Pausados Individualmente` — R-09
| Item | Configuração |
|---|---|
| Filtros | tag `pausado` presente |
| Colunas | Nome · Empresa · Telefone · `Tentativa nº` · Etapa atual · Última atividade |
| Ordenação | Última atividade asc (quem está pausado há mais tempo aparece primeiro) |

O laço da seção 2.13 (nó 2.5/1.5) represa a tentativa sozinho, sem tarefa
nem tag de fila — sem esta lista, um lead pausado literalmente some da
visão do gestor até o SDR lembrar de tirar a tag. Ordenar por quem está
parado há mais tempo é o mesmo raciocínio da 8.8: quem está represado há
mais tempo é quem mais precisa de alguém decidir "tira a pausa" ou "descarta
de vez".

---

## 9. Nota de qualificação e Prioridade

### 9.1 `Nota de qualificação` (0 a 100)

Montada com nós **Math Operation** em série no Pós-agendamento (seção 5, nó 4)
e na saída da IA (seção 6). Comece zerando o campo e some bloco a bloco.

**Bloco A — Fit (30 pontos)**
| Campo | Valor | Pontos |
|---|---|---|
| Clientes novos por mês | Até 10 / 11-30 / 31-100 / 100+ | 3 / 6 / 8 / 10 |
| Tem time comercial | Só o dono / 1-2 pessoas / 3-5 / 6+ | 3 / 6 / 8 / 10 |
| Quem atende os leads | Ninguém fixo / Dono / Vendedor / SDR | 10 / 7 / 5 / 3 |

"Ninguém fixo" vale mais que "SDR" de propósito: é a dor mais fácil de
resolver e a que mais precisa de nós.

**Bloco B — Maturidade de mídia (25 pontos)**
| Campo | Valor | Pontos |
|---|---|---|
| Investe em anúncios | Sim / Já investiu e parou / Nunca | 13 / 9 / 4 |
| Investimento mensal | 15 mil+ / 5-15 mil / 1-5 mil / Até 1 mil | 12 / 10 / 6 / 2 |

**Bloco C — BANT (45 pontos)**
| Campo | Valor | Pontos |
|---|---|---|
| Budget | Tem / Precisa aprovar / Não tem | 15 / 9 / 0 |
| Decisor | É o decisor / Influencia / Não decide | 15 / 8 / 2 |
| Prazo | Agora / Até 30 dias / 1-3 meses / Sem prazo | 15 / 11 / 6 / 2 |

Máximo: 30 + 25 + 45 = **100**.

**Faixas**
| Nota | Leitura | Consequência automática |
|---|---|---|
| 70–100 | A — agenda e avisa o closer sênior | `Prioridade` = 5, tag `fila-quente` |
| 45–69 | B — agenda normal | `Prioridade` = 4 |
| 25–44 | C — nutrição | `Prioridade` = 2, tag `nutricao-90d`, etapa `Nutrição` |
| 0–24 | D — descarta | `Prioridade` = 1, etapa `Descartado` |

**Corte independente da nota:** `Budget` = `Não tem` **e** `Prazo` = `Sem
prazo` → nutrição, qualquer que seja a nota. Empresa grande sem dinheiro e sem
pressa soma pontos de fit e engana a régua.

### 9.2 `Prioridade` (1 a 5)

Recalcule nestes 4 momentos: entrada na cadência (2.3), cada Pós-ligação
(seção 4), saída da IA (seção 6), reativação de 90 dias (seção 2.12, nó 3).
Primeira regra que casar, ganha.

| Ordem | Condição | Prioridade |
|---|---|---|
| 1 | `Resultado da tentativa` = `Pediu retorno` **ou** etapa = `Retorno agendado` | 5 |
| 2 | `Nota de qualificação` ≥ 70 | 5 |
| 3 | Respondeu mensagem (tem conversa de entrada) **ou** `Permissão WhatsApp` = `Sim` | 4 |
| 4 | `Nota de qualificação` entre 45 e 69 | 4 |
| 5 | `Tentativa nº` ≤ 2 | 4 |
| 6 | `Tentativa nº` entre 3 e 7 | 3 |
| 7 | `Tentativa nº` ≥ 8 **e** `Total de conexões` = 0 | 2 |
| 8 | tag `nutricao-90d` **ou** `telefone-invalido` presente | 1 |

Regra 5 (lead novo com prioridade alta) é o que mantém a fila do SDR
produtiva: a taxa de atendimento cai a cada tentativa, então lead fresco vale
mais que lead velho de mesma nota.

---

## 10. Checklist de teste — 5 contatos fictícios

Crie os 5 antes de publicar, com **seu próprio número** em 2 deles (para
checar mensagem de verdade) e números inválidos nos outros. Rode com a janela
de envio temporariamente aberta (00:00–23:59) e os Waits da cadência reduzidos
para minutos; **volte os valores reais antes de publicar**.

### Contatos
| # | Nome | Cenário | Caminho esperado |
|---|---|---|---|
| 1 | Teste Atendeu | Atende na T1 | `Atendeu` → `Conectado` → agenda → `Reunião agendada` |
| 2 | Teste Não Atende | Nunca atende, vai até o fim | 12 tentativas → `Nutrição` + `nutricao-90d` |
| 3 | Teste Retorno | Pede retorno na T3 | `Pediu retorno` → `Retorno agendado`, Prioridade 5 |
| 4 | Teste Número Errado | Número errado na T1 | `telefone-invalido` → `Nutrição` ou `Descartado` |
| 5 | Teste Não Ligar | Pede para não ligar na T2 | `nao-perturbe` + **DND ligado** → `Descartado`, nenhuma mensagem depois |

### Verificações, uma por linha
| # | O que testar | Como | Passou? |
|---|---|---|---|
| 1 | Entrada na cadência | Mover para `Em cadência` cria tag `fila-tel` e tarefa `[CADENCIA] T1` | |
| 2 | Portão de etapa | Mover para `Conectado` no meio da espera: a tentativa seguinte **não** dispara | |
| 3 | Portão `nao-perturbe` | Aplicar a tag na mão: próxima tentativa não dispara | |
| 4 | Portão `telefone-invalido` | Aplicar a tag: tentativa de telefone não dispara, de WhatsApp sim | |
| 5 | Limpeza do resultado | Na T2, `Resultado da tentativa` chega vazio (não herda o da T1) | |
| 6 | `Atendeu` | Registrar: conexões +1, `conectado-hoje` aplicada, etapa `Conectado`, tarefa `[CONECTADO]` criada, saiu da cadência | |
| 7 | `Caixa postal` em WhatsApp | `WA não atendidas seguidas` vai a 1; repetir vai a 2 | |
| 8 | Regra das 2 seguidas | Com o contador em 2, a próxima tentativa de WhatsApp sai como **telefone** | |
| 9 | Reset do contador | Uma tentativa de telefone não atendida zera `WA não atendidas seguidas` | |
| 10 | Sem permissão | Com `Permissão WhatsApp` = `Não`, toda tentativa de WhatsApp vira telefone | |
| 11 | `Número errado` | `telefone-invalido` aplicada, etapa muda, gestor notificado | |
| 12 | `Pediu retorno` | Prioridade 5, etapa `Retorno agendado`, tarefa `[RETORNO]` criada | |
| 13 | `Não ligar` | Tag + **DND ligado**; mandar mensagem de teste pelo workflow: **não** deve sair | |
| 14 | Tempo limite | Não classificar uma tentativa: às 18:30 vira `Não atendeu`, tag de fila removida, `limpar-tarefas` aplicada | |
| 15 | Mestre de saída | Qualquer mudança de etapa: nenhuma tag `fila-*` sobra e o contato sai dos 2 workflows | |
| 16 | Mestre de saída não se morde | Mover **para** `Em cadência` não aciona a limpeza | |
| 17 | Agendamento manual | SDR agenda pelo link: o Pós-agendamento dispara (é o teste do gatilho `Appointment Status`) | |
| 18 | Sticky Contact | Agendar 2 leads seguidos na mesma aba: o 2º **não** herda dados do 1º | |
| 19 | Nota | Preencher a qualificação completa e conferir a nota na mão contra a seção 9.1 | |
| 20 | Lembretes | Reagendar a reunião: os 3 lembretes se movem junto | |
| 21 | Listas inteligentes | Cada uma das 4 listas mostra exatamente os contatos esperados | |
| 22 | Rotina de manutenção | Rodar `rotina-limpar-tarefas.md`: tarefas fora do prefixo são **concluídas**, nunca excluídas, e a tag sai | |
| 23 | Volume | Simular 10 leads/dia por 5 dias e contar as tarefas geradas por dia (lacuna L-05) | |
| 24 | Loop do closer | No Teste Atendeu já em `Reunião agendada`, simular `Nota de qualificação` ≥ 70 e preencher `Reunião foi qualificada` = `Não` com um motivo diferente de `Timing errado`: etapa vira `Descartado`, `Data do veredito do closer` grava e o gestor recebe o alerta de calibração alta (seção 5.1, nó 5) | |
| 25 | Funil por marco | No Teste Atendeu: `Data conectado` grava ao entrar em `Conectado`, `Data agendado` grava ao agendar, e marcar o agendamento como `Showed` grava `Data compareceu` — os três aparecem nas listas 8.10 a 8.12 no mês corrente | |
| 26 | Cadência Inbound (R-07) | Aplique `cad-inbound` num dos 5 contatos de teste antes de mover para `Em cadência` de novo (rodada manual, decisão D-06): a Cadência Inbound dispara, **não** a 12x30 (confira que nenhuma tarefa `[CADENCIA] T1` da régua de dias nasce); `Prioridade` vira 5 e a tag `fila-quente` é aplicada na entrada; a tarefa `[CADENCIA] TI1` nasce após o Wait reduzido de teste; a mensagem `MI-0` sai antes da TI1. Deixando sem resposta até a TI5, confira o handoff: mensagem `MI-F` sai e a Cadência 12x30 assume (a tarefa `[CADENCIA] T1` da régua de dias nasce só agora) | |
| 27 | Reengajamento 90 dias (R-08) | Reduza o Wait do nó 1 (seção 2.12) para o teste. No Teste Não Atende, já com `nutricao-90d` aplicada e etapa `Nutrição` (fim natural do teste 2), aguarde o Wait reduzido: `cad-outbound` aparece, `cad-inbound` some (se esse contato tiver as duas na memória de um teste anterior), `nutricao-90d` some, `reengajamento-ativo` aparece, etapa volta para `Em cadência`, mensagem `RE-1` sai, e a tarefa `[CADENCIA] TR1 · … — Reengajamento` nasce depois do Wait de 2h (também reduzido) sem resposta. Confirme que a Cadência 12x30 (seção 2.1) **não** dispara uma segunda vez (nenhuma tarefa `[CADENCIA] T1` nova) — é o filtro `reengajamento-ativo` ausente fazendo o trabalho. Deixando sem resposta até a TR4, confira: mensagem `RE-2` sai, `reengajamento-ativo` some, `nutricao-90d` volta, etapa volta para `Nutrição`, e o próprio workflow dispara de novo (Allow Re-entry ligado) — inicia outro Wait de 90 dias sozinho | |

Depois do teste, **apague as 5 oportunidades e desative os 5 contatos** (não
exclua contatos, pela regra 1) e restaure os Waits e a janela de envio.

---

## 11. O que o MCP não faz (resumo)

| Item | MCP | Manual |
|---|---|---|
| Campos personalizados | Não | Cria na tela; lista com tipo e opções em `campos-e-tags.md` |
| Tags | Cria | — |
| Pipeline e etapas | Não | Seção 1 |
| Workflows | Não | Seções 2, 2.9, 2.11, 3 a 6, 5.1, 5.2 |
| Calendário | Lê | Cria e configura: seção 7.1 |
| Formulário | Não (nem lê, neste toolkit) | Seção 7.2 |
| Listas inteligentes | Não | Seção 8 |
| Conversation AI | Não | Seção 6 |
| Concluir tarefa em massa | Sim | É a rotina da seção 5 do projeto |
