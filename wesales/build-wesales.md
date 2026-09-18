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
    textos das mensagens em `biblioteca-mensagens.md`, não neste documento
12. Workflows "Interceptação de Sinal — Clique" e "— Resposta" (seção 2.9)
13. Workflow "Alerta de Speed-to-lead" (seção 2.11) — usa a mesma tag nova de
    monitoramento que a lista 8.8 filtra
14. Listas inteligentes (seção 8)
15. Teste com os 5 contatos fictícios (seção 10) **antes** de publicar

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

Não use "Contact Tag Added" como gatilho: a tag é consequência da cadência,
não causa dela. E não use "Contact Created", senão o lead entra antes de ter
telefone validado.

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
| 1 | Aguardar | Wait → Time Delay | 1 hora |
| 2 | Portão | If/Else | Etapa da oportunidade **é** `Em cadência` **E** `1ª tentativa em` está vazio → segue. Senão → **encerra** (T1 já rodou, ou o lead já saiu de cadência — não é atraso) |
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
| 4 | Remove Contact Tag | `fila-quente`, `fila-tel`, `fila-wa`, `fila-linkedin`, `atraso-1a-tentativa` (R-02) |
| 5 | Add Contact Tag | `limpar-tarefas` |
| 6 | Add Note | `Saída de cadência · etapa: {{opportunity.pipeline_stage}} · tentativa {{contact.tentativa_no}} · resultado {{contact.resultado_da_tentativa}}` |

O nó 1 existe porque o gatilho é "qualquer etapa": sem ele, mover o lead
*para* a cadência acionaria a limpeza e mataria a cadência no nascimento.

Não removo `conectado-hoje`, `nao-perturbe`, `telefone-invalido`,
`nutricao-90d`, `cad-inbound` e `cad-outbound`: são estado do lead, não fila.

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

A tag só existe porque o workflow da seção 2.11 a aplicou depois de 1h de
espera sem `1ª tentativa em` preenchido — a lista não faz conta nenhuma, só
lê a marca que o relógio já fez. É o "Pronto quando" do R-02: dá para apontar
o lead que já passou de 1h sem SDR ligar, sem abrir planilha.

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

Recalcule nestes 3 momentos: entrada na cadência (2.3), cada Pós-ligação
(seção 4), saída da IA (seção 6). Primeira regra que casar, ganha.

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
