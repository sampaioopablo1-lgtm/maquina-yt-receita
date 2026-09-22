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
2. Workflow "Contador de Toques" (seção 2.19, F-04) — só depende do campo
   `Toques na semana` e da tag `toque` do passo 1; monte cedo porque os
   passos 14 e 16 (Cadência 12x30 e Interceptação de Sinal) já aplicam a tag
   `toque` desde a primeira montagem, e o contador precisa existir para
   reagir a ela
3. Pipeline "Pré-vendas" (seção 1)
4. **Workflow "Porta de Entrada" (seção 1.3, L-09/L-09b)** — só depende do
   pipeline do passo 3; monte e publique antes de qualquer outro workflow,
   e rode o backfill manual dos contatos já existentes (seção 1.3) assim
   que publicar — é a única peça que faz uma oportunidade existir, sem ela
   nenhum gatilho `Opportunity Stage Changed` do resto desta lista tem o
   que disparar
5. Calendário do closer + formulário (seção 7)
6. Trigger Link "Agendar com o closer" (seção 2.9) — precisa da URL do
   calendário do passo 5
7. Workflow "Mestre de saída" (seção 3)
8. Workflow "Pós-ligação" (seção 4) — retoque desta rodada (R-18): já
   publicado com 6 ramos; acrescente a opção `Desqualificado` em `Resultado
   da tentativa` (passo 1) e o 7º ramo (D1-D7) antes de montar do zero
9. Workflow "Pós-agendamento" (seção 5)
10. Workflow "Loop do closer" (seção 5.1) — usa os campos do closer criados
    no passo 1
11. Workflow "Registro de Comparecimento" (seção 5.2) — usa o mesmo
    calendário do passo 5, gatilho por status de agendamento
12. Workflows "Recuperação de No-show" e "SLA do Closer — No-show" (seção
    5.3/5.4, R-12) — mesmo calendário e status `No Show`; o nó 3 do Pós-
    agendamento (passo 9) precisa já remover destes dois workflows antes de
    publicá-los, senão um reagendamento no meio de uma recuperação não limpa
    nada
13. Workflow "Qualificação por IA no WhatsApp" (seção 6)
14. Workflow "Cadência 12x30" (seção 2) — por último entre os principais,
    porque chama os outros e usa o Trigger Link do passo 6 nas mensagens M2/M3;
    textos das mensagens em `biblioteca-mensagens.md`, não neste documento.
    Do passo 14 em diante o gatilho da seção 2.1 já leva o filtro novo do
    R-07 (tag `cad-inbound` ausente) — monte-o com o filtro desde o início,
    não depois. O bloco padrão de tentativa (seção 2.4) já leva o nó 2.5 de
    pausa individual (R-09) e o nó 2.5c de teto de toques (F-04) desde a
    primeira montagem, não como retrofit. O nó 0 já leva o par 0.7/0.7b de
    distribuição de leads (R-10, seção 2.14) desde o início — defina a lista
    de round robin no nó 0.7b mesmo com um único SDR hoje — e o portão
    0.0/0.0b de higiene de telefone (R-13, seção 2.3) na frente de tudo,
    antes do 0.1. Os quatro nós `Send WhatsApp` (M1-a, M1-b, M2-v1, M3-v1)
    já levam a guarda de janela de 24h (G-05, seção 2.6.2) desde a primeira
    montagem — sem ela, a mensagem livre é recusada pela API assim que o
    lead estiver fora da janela, o caso comum desta operação
15. Workflow "Cadência Inbound" (seção 2.10) — depois da 12x30 porque o
    handoff do fim da cadência inbound entra nela por Add to Workflow (seção
    2.10, último nó); precisa da 12x30 já montada para apontar para algo.
    Também já leva o nó 1.5 de pausa individual (R-09) desde o início, o
    par 0.8/0.8b de distribuição de leads (R-10) apontando para a **mesma**
    lista de round robin do nó 0.7b do passo 14, e o mesmo portão 0.0/0.0b
    de higiene de telefone (R-13) do passo 14
16. Workflows "Interceptação de Sinal — Clique" e "— Resposta" (seção 2.9)
    — já levam o nó 3c de teto de toques (F-04) desde a primeira montagem.
    Monte o "Opt-out por Palavra-chave" (seção 2.9.5, R-17) **junto** com o
    "— Resposta": os dois precisam nascer com o filtro cruzado por frase já
    aplicado (`Contains`/`Doesn't Contain`, mesma lista de palavras-chave
    nos dois lados) — montar um sem o outro deixa uma resposta de opt-out
    disparando os dois workflows ao mesmo tempo
17. Workflow "Alerta de Speed-to-lead" (seção 2.11) — usa a mesma tag nova de
    monitoramento que a lista 8.8 filtra; do R-07 em diante o nó 1 bifurca
    o tempo de espera por origem (`cad-inbound` presente = 15 min, senão 1h);
    do R-09 em diante o nó 2 já ignora quem está com a tag `pausado`
18. Workflow "Reengajamento 90 dias" (seção 2.12) — por último entre os que
    tocam cadência: reaproveita o bloco padrão da 12x30 (passo 14) nó a nó,
    nó 2.5 incluído, e exige que o gatilho do passo 14 já tenha o filtro
    `reengajamento-ativo` ausente (R-08) — monte-o com o filtro desde o
    início se ainda não montou, não depois
19. Listas inteligentes (seção 8), incluindo `Fila do Dia — Total` (8.16),
    `Recuperação de No-show` (8.17, R-12) e `Higiene — Sem Telefone Válido`
    (8.18, R-13)
20. Workflow "Monitor de Capacidade" e métrica `Estouro da Fila` (seção
    2.15) — depende da lista 8.16 do passo 19 já montada
21. Teste com os 5 contatos fictícios (seção 10) **antes** de publicar
22. Pausar Workflows em Datas Específicas (seção 2.13, R-09) — por último de
    todos: o recurso só lista workflows **publicados**, então precisa dos
    passos 14, 15, 18 e 20 já publicados para aparecerem no seletor
23. Ativar Number Validation (Configurações → Telefone, agência e depois
    subconta) e montar o workflow "Higiene de Número — Validação Automática"
    (seção 2.16, R-13) — opcional, por último de todos: o gatilho **Number
    Validation** só existe depois de o recurso estar ligado, e o portão
    0.0/0.0b dos passos 14/15 já cobre o caso mais comum (sem telefone
    nenhum) sem depender disso
24. Dashboard "Painel do Gestor — Pré-vendas" e as Custom Metrics novas
    (seção 2.17, R-15) — por último de todos: cada widget aponta para uma
    peça já montada nos passos anteriores (calendário do passo 5, pipeline
    do passo 3, métrica `Estouro da Fila` do passo 20, tarefas das
    cadências dos passos 14/15); montar antes disso deixaria widget
    apontando para nada
25. Workflow "Lead Esquecido em NOVO LEAD" (seção 2.20, F-05) — só depende
    do pipeline do passo 3; o nó 0 novo do Mestre de saída (passo 7) já sai
    junto se você montar o Mestre de saída a partir desta versão do
    documento, então a ordem entre os dois não importa. Depois de publicar,
    rode `Add to Workflow` em massa pela lista de oportunidades em
    `NOVO LEAD` (mesmo mecanismo do backfill do passo 4) para cobrir quem já
    está parado hoje — o gatilho não varre sozinho quem já está na etapa
26. Workflow "Fila Travada" (seção 2.21, F-05 peça 2) — retoque desta rodada:
    faltava nesta lista desde que a seção foi escrita. Só depende do bloco
    padrão de tentativa (passos 14/15) já aplicar `fila-tel`/`fila-wa`;
    publique a qualquer momento depois deles
27. Workflow "Cadência Sem Avanço" (seção 2.22, F-05 peça 3) — retoque desta
    rodada, mesmo motivo do passo acima. Depende do campo
    `Checkpoint — Tentativa nº` (passo 1) e do reset de `Tentativa nº` que a
    Cadência 12x30/Inbound/Reengajamento (passos 14/15/18) já fazem
28. Workflow "AGENDAR Estagnado" (seção 2.23, F-05 peça 5) — só depende do
    pipeline do passo 3; o nó 0 do Mestre de saída (passo 7), atualizado
    nesta rodada, já sai junto se você montar o Mestre de saída a partir
    desta versão do documento
29. Workflow "Retorno Vencido" (seção 2.24, F-05 peça 6) — depende do campo
    `Checkpoint — Data de retorno` (passo 1) e do campo `Data de retorno`
    (S-01, já existente na tela). O nó 3c novo do Pós-ligação (passo 8) e o
    nó 4 do Mestre de saída (passo 7), os dois atualizados nesta rodada, já
    saem junto se você montar as duas peças a partir desta versão do
    documento
30. Workflow "Qualidade da Conexão" (seção 2.27, F-06) — por último de
    todos, condicionado a uma confirmação que ainda não existe: **as
    ligações desta operação saem por LC Phone?** (mesma pendência sem
    resposta do F-08/F-09). Se sim, ligue transcrição em Configurações →
    Telefone antes de montar — sem ela o gatilho `Transcript Generated`
    nunca dispara. Depende dos campos `Duração da ligação`/`Conexão real`
    (passo 1). Corrige só a métrica de conexão; não bloqueia nenhum passo
    anterior desta lista, e nenhum passo anterior depende dele

---

## 1. Pipeline "Pré-vendas" (hoje o `FUNIL DE VENDAS`, 5 etapas reais)

**Arquitetura real, decidida ao vivo em chat, 18/09/2026 — já construída,
não pendente.** O plano original desta seção (e a recomendação da
auditoria) era 7 etapas novas, criadas trocando as 14 antigas do `FUNIL DE
VENDAS` (`0Fo2xbeayE4EP6yuSUtq`). O dono recusou essa tabela ao vivo e
decidiu outra coisa: **5 etapas**, com nomes, probabilidade e cor
próprios, confirmadas na tela por `opportunities_get-pipelines` e
reconferidas sem mudança a cada rodada desde então. Autorização e decisão
completa: `APROVADO.md`; detalhe da resolução: `GUIA-MONTAGEM.md`, "Fase
1". **Esta seção documenta o que existe de verdade na tela, não mais um
plano de construção** — não há "O que fazer na tela" aqui, porque já foi
feito.

| Ordem | Etapa (nome real) | Prob. de ganho | Cor |
|---|---|---|---|
| 0 | `NOVO LEAD` | 30% | `#2563EB` |
| 1 | `CONECTAR` | 40% | `#8B5CF6` |
| 2 | `AGENDAR` | 50% | `#2DD4BF` |
| 3 | `NEGOCIAR` | 60% | `#D97706` |
| 4 | `FORMALIZAR` | 70% | `#059669` |

**Consequência para todo o resto deste documento:** onde qualquer seção
ainda disser "Pipeline: `Pré-vendas`" dentro de um gatilho de workflow,
configure o nó apontando para o pipeline **`FUNIL DE VENDAS`** — é o mesmo
objeto, só de nome diferente na tela. `Pré-vendas` continua sendo como
este documento **chama** o processo — não é mais o nome de um pipeline
separado no GHL, e nunca chegou a ser (o dono preferiu 1 pipeline a 2,
ver `APROVADO.md`).

### 1.0 Tradução: nome antigo (plano de 7) → etapa/estado real (5 + tag/status)

**Leia isto antes de qualquer seção 2 em diante.** As seções 2 a 9 deste
documento ainda foram escritas em cima do plano de 7 etapas — reescrevê-las
nó a nó é trabalho grande, em andamento (ver checklist em
`GUIA-MONTAGEM.md`, "Fase 1"). Até cada seção ser migrada, todo nome de
etapa antigo que aparecer nela se traduz por esta tabela:

| Nome antigo (plano de 7) | Vira, na tela real | Como |
|---|---|---|
| `Novo lead` | `NOVO LEAD` | Mesma etapa, só o nome mudou |
| `Em cadência` | `CONECTAR` | Mesma etapa — é aqui que o portão de toda tentativa (nó 3, seção 2.4) passa a checar |
| `Conectado` | `AGENDAR` | Mesma etapa |
| `Retorno agendado` | **continua em `CONECTAR`** | Deixou de ser etapa própria — "pediu retorno" não move a oportunidade, só grava `Resultado da tentativa = Pediu retorno`. Todo gatilho `Opportunity Stage Changed → Retorno agendado` vira **sem gatilho de etapa nenhum**: o lead nunca sai de `CONECTAR`, e a lista `Retornos` (8.4) filtra só pelo campo |
| `Reunião agendada` | `NEGOCIAR` | Absorve também a negociação do closer (proposta, condições), que no plano de 7 ficava fora do pipeline — agora está dentro, porque o dono optou por 1 pipeline só |
| `Nutrição` | **status da oportunidade = `abandoned`**, etapa fica como estava | Todo gatilho `Opportunity Stage Changed → Nutrição` vira **`Contact Tag Added → nutricao-90d`** (gatilho nativo já usado em outro lugar do projeto) — a tag continua sendo o sinal de quem está nutrição, o status só formaliza isso no campo nativo do GHL |
| `Descartado` | **status da oportunidade = `lost`**, etapa fica como estava | Todo gatilho `Opportunity Stage Changed → Descartado` vira uma ação `Update Opportunity` mudando o `status`, não a etapa |
| *(não existia)* | `FORMALIZAR` | Etapa nova, fechamento/contrato — equivale a `status = won`. Fora do escopo dos workflows de SDR deste documento (é o closer fechando), citada aqui só para a tabela ficar completa |

**Por que isso é simplificação, não perda:** `CONECTAR` continua etapa
própria porque é o único estado que um portão de workflow *precisa*
consultar antes de disparar uma tentativa — é o mecanismo de segurança da
cadência inteira. `Retorno agendado`, `Nutrição` e `Descartado` nunca
precisaram desse tipo de consulta por um workflow de tentativa; um campo
(`Resultado da tentativa`) e o status nativo da oportunidade (que o GHL já
oferece de graça, sem campo novo) bastam. Cinco etapas reais + dois
atributos nativos (status, campo) cobrem o mesmo terreno que as 7 etapas
do plano original cobriam, com menos peça para manter sincronizada.

### 1.1 Mapeamento com os frameworks de mercado — atualizado 18/09/2026

Pedido do dono: ajustar o funil usando o que o mercado já documenta sobre
Inside Sales (funil genérico de RD Station/Salesforce/Meetime — prospecção
→ qualificação → apresentação → fechamento) e o **Sales Model Canvas**
(Thiago Reis / Growth Machine — 4 etapas macro, preenchidas por 7 blocos
operacionais cada).

**Mudança relevante desde a primeira versão desta tabela:** ali, "Proposta,
Negociação, Ganho/Perdido" ficava marcado como fora deste pipeline,
porque o plano original prometia um pipeline `Pré-vendas` que parava no
agendamento. Isso mudou quando o dono decidiu reaproveitar o `FUNIL DE
VENDAS` como pipeline único (`APROVADO.md`) — a negociação e o fechamento
agora **vivem dentro** deste mesmo pipeline, nas etapas `NEGOCIAR` e
`FORMALIZAR`.

| Framework de mercado | Nossa etapa/estado correspondente | Por que a granularidade difere |
|---|---|---|
| Topo do funil — Prospecção / Não contatado | `NOVO LEAD` | Igual — é o mesmo conceito |
| Meio do funil — Qualificação (pré-venda) / Contato-Abordagem | `CONECTAR` (inclui quem pediu retorno) e `AGENDAR` | O genérico trata como 1-2 fases; aqui seguem 2 estados **porque cada um é o que um workflow consulta** (seção 2.4, nó 3) — "tentando conectar (ou cumprindo retorno combinado)" e "conectado, ainda sem reunião marcada" precisam de portão próprio, senão a régua de 12 tentativas não sabe quando parar |
| Fundo do funil — Apresentação/Demonstração | `NEGOCIAR` (metade "comparecimento e veredito") | É o ponto de handoff: o SDR agenda, o **closer** apresenta |
| Fundo do funil — Proposta, Negociação, Ganho/Perdido | `NEGOCIAR` (metade "negociação") → `FORMALIZAR` (`status = won`) ou saída com `status = lost` | Agora dentro deste pipeline (ver "Mudança relevante" acima) — administrado pelo closer, mas sem pipeline separado para administrar |
| — (nenhum framework genérico tem isto) | Status `abandoned` (tag `nutricao-90d`), etapa como estava | É onde o Sales Model Canvas simplifica demais: o binário "Ganho ou Perdido" não tem espaço para "sem fit **agora**, mas com fit daqui a 90 dias". A reativação automática (R-08) trata isso como terceiro estado — nenhuma das fontes citadas pelo dono documenta isso como etapa própria, só como "relatório de nutrição vencida" manual |
| Fundo do funil — Perdido | Status `lost`, etapa como estava | Igual em espírito, mas sem etapa própria — o status nativo do GHL já resolve isso sem etapa dedicada |

### 1.2 Canvas operacional por etapa (7 blocos, Sales Model Canvas)

**Preenchido para as 5 etapas reais.** Onde o plano de 7 tinha uma etapa
que virou tag/status (`Retorno agendado`, `Nutrição`, `Descartado`), o
conteúdo correspondente entra como sub-nota dentro da etapa em que esse
estado de fato vive agora, não como bloco próprio. Convenção dos blocos,
na ordem do framework: **Objetivo** (a meta central) → **Validação** (o
que precisa ser verdade para avançar) → **Ferramentas** (o que já existe
no projeto, sem inventar nada novo) → **Tempo de estagnação** (o alarme de
"isto emperrou") → **Motivos de perda** (os jeitos documentados de sair
sem avançar) → **Taxa de conversão esperada** (hipótese a calibrar, nunca
meta imposta) → **Meta de avanço** (volume que sustenta a operação).

#### Etapa 0 — `NOVO LEAD`

| Bloco | Conteúdo |
|---|---|
| Objetivo | Confirmar que o lead tem telefone e está pronto para entrar na régua — não é etapa de conversa |
| Validação de passagem | Telefone existe e a tag `telefone-invalido` está ausente. Hoje a promoção para `CONECTAR` é **decisão manual do SDR** (lacuna L-07, `briefing-sdr.md`) |
| Ferramentas | Formulário/importação de lista → `NOVO LEAD` nativo do pipeline |
| Tempo de estagnação | Mesmo relógio do speed-to-lead (R-02/R-07): 15 min se a origem é inbound, 1h se é outbound — um lead parado em `NOVO LEAD` além disso já perdeu a janela que a seção 2.11 mede a partir de `CONECTAR`, então **o relógio ideal começa aqui, não lá** (ver nota abaixo) |
| Motivos de perda | Telefone claramente inválido já na entrada (não chega a rodar 12 tentativas) |
| Taxa de conversão esperada | ~90-95% deveria avançar para `CONECTAR` — hipótese, a calibrar com a lista `Higiene — Sem Telefone Válido` (8.18, R-13) depois de volume real |
| Meta de avanço | 10-13 leads/dia (L-05, `briefing-sdr.md`) para sustentar 100 ligações/dia com folga |

**Nota sobre o tempo de estagnação desta etapa:** o R-02 mede speed-to-lead
a partir de `Entrada em`, carimbado só ao entrar em `CONECTAR` (seção
2.3, nó 0.6) — ou seja, o relógio de verdade só liga **depois** da
promoção manual da L-07 acontecer, não em `NOVO LEAD`. Enquanto a L-07
não for resolvida, um lead pode ficar horas em `NOVO LEAD` sem que
nenhuma métrica deste projeto perceba. Não é bug novo — é a mesma lacuna
L-07 já registrada, só que agora com o efeito colateral dela em cima de
uma métrica que achávamos fechada (R-02). Registrado aqui para quem for
priorizar L-07 saber que ela também é a métrica de estagnação desta etapa.

#### Etapa 1 — `CONECTAR` (absorve o antigo `Retorno agendado`)

| Bloco | Conteúdo |
|---|---|
| Objetivo | Conseguir uma conexão real (`Atendeu`) dentro das 12 tentativas em 30 dias — inclui quem já foi contatado e pediu para ligar depois: esse lead não sai da etapa, só muda o que `Resultado da tentativa` guarda |
| Validação de passagem | `Resultado da tentativa` = `Atendeu` (→ `AGENDAR`) — nó 10 do bloco padrão, seção 2.4. `Pediu retorno` **não muda mais etapa**: o lead fica em `CONECTAR`, e a lista `Retornos` (8.4) filtra só pelo valor do campo, sem OR com etapa nenhuma |
| Ferramentas | Workflows Cadência 12x30/Inbound/Reengajamento, listas `Fila Telefone Hoje`/`Fila WhatsApp Hoje` (8.2/8.3), lista `Retornos` (8.4), `script-de-ligacao.md` |
| Tempo de estagnação | Já coberto: F-05 (roadmap, peça 3 — seção 2.22) monitora `CONECTAR` sem avanço; a 1ª tentativa tem relógio próprio (Alerta de Speed-to-lead, seção 2.11). O antigo gap "retorno vencido sem nova ligação" (que dependia de S-01, `Data de retorno`/`Hora do retorno` — **os dois já existem na tela desde 21/09/2026**, `CONFERENCIA-CAMPOS.md` Tabela K) continua valendo aqui dentro, não em etapa separada |
| Motivos de perda | `Número errado` (→ `telefone-invalido`), `Não ligar` (→ opt-out, DND) — saem da etapa via `Update Opportunity` para `status = lost`; 12 tentativas esgotadas sem conexão → `status = abandoned` **+** tag `nutricao-90d`, **sem sair de `CONECTAR`** (era "→ `Nutrição`" no plano de 7; agora é status, não movimento de etapa) — os três ramos do Pós-ligação, seção 4 |
| Taxa de conversão esperada | ~35% conectam ou saem antes das 12 tentativas (L-05, `briefing-sdr.md`) — mesma hipótese que já dimensiona o volume de entrada |
| Meta de avanço | 100 ligações/dia é a meta do SDR (briefing); quantos *leads* avançam por dia é `Total de conexões` (C-07) somado, lido na lista `Conexão por Tentativa` (8.6, R-01) |

#### Etapa 2 — `AGENDAR`

| Bloco | Conteúdo |
|---|---|
| Objetivo | Qualificar e agendar com o closer na mesma ligação (briefing-sdr.md, "A máquina") |
| Validação de passagem | Formulário `Qualificação SDR` preenchido + agendamento no calendário `Reunião com closer` (dispara o Pós-agendamento, seção 5) |
| Ferramentas | Calendário + formulário (seção 7), tarefa `[CONECTADO] Qualificar e agendar` |
| Tempo de estagnação | Já coberto: F-05 (roadmap, peça 5 — seção 2.23) monitora 24h sem sair de `AGENDAR` depois de atender. Esta linha dizia "sem monitor ainda" até 22/09/2026 — ficou parada desde antes de a peça 5 fechar; a mesma ressalva que a linha de `CONECTAR` já dá logo acima |
| Motivos de perda | ~~**Segundo gap encontrado:** hoje não existe caminho de desqualificação instantânea nesta etapa~~ — **L-08 fechada em 21/09/2026 (R-18):** o ramo `Desqualificado` do Pós-ligação (seção 4) sai por `status` antes de chegar em `AGENDAR`, então a maioria dos "sem fit na ligação" nem entra mais nesta etapa. O que resta em `AGENDAR` sem agendar é só "atendeu, era fit, não fechou horário" — o gap de medição da linha abaixo |
| Taxa de conversão esperada | Com o L-08 fechado, a métrica de `AGENDAR` já mede só "não conseguiu horário" — o motivo "sem fit" saiu antes, pelo ramo `Desqualificado` |
| Meta de avanço | Ligado à meta de conexões da etapa anterior — sem meta própria adicional |

#### Etapa 3 — `NEGOCIAR` (absorve `Reunião agendada` + a negociação do closer)

| Bloco | Conteúdo |
|---|---|
| Objetivo | Comparecimento + veredito de qualificação real do closer, e a negociação em si (proposta, condições) até a decisão de compra — a metade "negociação" não existia no plano de 7 etapas, que a mandava para fora do pipeline |
| Validação de passagem | `Reunião foi qualificada` preenchida pelo closer (Loop do closer, seção 5.1) para a metade "comparecimento"; para a metade "negociação", decisão do closer registrada como `status = won` (→ `FORMALIZAR`) ou `status = lost` (permanece em `NEGOCIAR` com o status marcado, não some da tela) |
| Ferramentas | Calendário, Registro de Comparecimento (5.2), Loop do closer (5.1), SLA do Closer — No-show (5.4, R-12); a negociação em si (proposta/condições) é conduzida pelo closer fora dos workflows deste documento |
| Tempo de estagnação | A metade "comparecimento" já está coberta — é literalmente o R-12: SLA do closer com escalonamento ao gestor (seção 5.4). A metade "negociação" (depois do `Reunião foi qualificada = Sim`) ficou sem monitor até 22/09/2026: F-05 fechou com seis peças sem incorporar este gap, apesar de citado aqui como candidato desde a etapa ser escrita. Fechado como item próprio, F-13 (roadmap), seção 2.28 abaixo |
| Motivos de perda | No-show 2x seguido (R-12: `status = lost` mantendo a oportunidade em `NEGOCIAR`, não um "mover para `Descartado`" — migrado nas seções 5.3 e 5.4 em 19/09/2026; este parágrafo dizia "ainda usa a redação antiga e entra na fila" até 21/09, quando a fila já não existia), `Reunião foi qualificada` = `Não` (→ roteamento da seção 5.1, mesma troca de "mover etapa" por "mudar status") |
| Taxa de conversão esperada | "nota ≥ 70 acerta X%" é exatamente o que a lista `Calibração da Régua` (8.7, F-03) mede |
| Meta de avanço | Função da nota de qualificação (seção 9.1) e do volume que chega de `AGENDAR` |

#### Etapa 4 — `FORMALIZAR` (novo, não existia no plano de 7)

| Bloco | Conteúdo |
|---|---|
| Objetivo | Fechamento/contrato assinado — equivale ao `status = won` da oportunidade |
| Validação de passagem | Contrato assinado, registrado pelo closer |
| Ferramentas | Fora do escopo dos workflows de SDR deste documento — é o closer fechando, sem automação da cadência envolvida |

Sem os outros blocos do canvas: é estado terminal de sucesso administrado
pelo closer, não uma etapa de progresso que a máquina de SDR gerencia ou
monitora — citada aqui só para o mapeamento da seção 1.0 ficar completo.

#### Estados que não são mais etapa — `Nutrição` (status `abandoned`) e `Descartado` (status `lost`)

Não recebem canvas próprio porque não são etapas: são **status da
oportunidade**, sobrepostos a qualquer etapa em que o lead já estava
(normalmente `CONECTAR` ou `NEGOCIAR`) — ver tabela 1.0. "Tempo de
estagnação" e "meta de avanço" não fazem sentido para eles do jeito que
fazem para as etapas de progresso.

- **`abandoned` (ex-`Nutrição`)**: ficar marcado assim **é o comportamento
  correto** por até 90 dias — o Reengajamento (R-08, seção 2.12) é o
  próprio relógio, não uma falha a alarmar. Único ponto que vale medir: %
  de leads que reativam e conectam na segunda rodada, contra a régua
  original — hipótese de métrica nova, sem lista dedicada ainda (poderia
  entrar como adição à 8.14 `Reengajamento em Curso` numa rodada futura,
  não construída agora).
- **`lost` (ex-`Descartado`)**: fim de linha, sem reentrada automática de
  propósito. O "motivo de perda" já é o motivo de estar aqui —
  `telefone-invalido`, opt-out (`nao-perturbe`), no-show 2x, ou `Reunião
  foi qualificada` = `Não`. Proporção de descartes por telefone inválido é
  diagnóstico de **qualidade da lista de entrada**, não da cadência (liga
  direto com R-13, higiene de base).

### 1.3 Workflow "Porta de Entrada" — fecha L-09/L-09b

**Por que este workflow existe:** `grep "Create.*Opportunity"` neste
documento inteiro dava zero até esta seção — todo nó lê etapa ou move
etapa, nenhum cria o registro que tem etapa. Contato que nasce de
formulário, API, importação, digitação manual ou integração (Meta Lead Ads
incluído) fica sem oportunidade, logo sem etapa, logo fora de toda a
máquina (cadência, interceptação de sinal, tudo — todos os gatilhos são
`Opportunity Stage Changed`). Não é mais hipótese: reconfirmado nesta
execução via `opportunities_search-opportunity`/`contacts_get-contacts`
— **40 contatos** na subconta (subiu de 6/7 na última checagem, quase
todos com `source: Facebook` e `attributions` confirmando `adSource:
facebook`, entrada real de anúncio pago) e **0 oportunidades**. São leads
reais parados, não um cenário de teste.

**Gatilho: Contact Created**, sem filtro. Pesquisado antes de decidir entre
três opções: `Contact Created` genérico, o gatilho específico `Facebook
Lead Form Submitted`, e `Tag Added` de `cad-inbound`/`cad-outbound`.
Confirmado que `Contact Created` dispara para toda origem de contato —
manual, formulário nativo, API e integrações como Facebook/Instagram Lead
Ads (a documentação da HighLevel e guias de terceiros mostram esse gatilho
usado com filtro de `Lead Source Tag` justamente para pegar a fatia do
Meta, o que prova que ele enxerga essa origem também) — enquanto o gatilho
`Facebook Lead Form Submitted` só cobre a origem Meta, e `Tag Added`
dependeria de alguém aplicar a tag primeiro, o que nenhum fluxo hoje faz na
entrada. `Contact Created` é o único gatilho que cobre "toda origem" sem
depender de nada acontecer antes — mesma lógica que já levou o L-09b a
rejeitar o caminho do toggle da integração (`briefing-sdr.md`): resolver
**dentro da máquina**, não fatia por fatia.

**Configurações do workflow**

| Configuração | Valor | Por que |
|---|---|---|
| Janela de envio / dias / fuso | Não se aplica | O único nó é uma escrita instantânea no CRM, não uma mensagem — não há o que respeitar janela |
| Stop on Response | Não se aplica | Nenhuma mensagem sai daqui |
| Allow Re-entry | Não se aplica | `Contact Created` não dispara duas vezes para o mesmo contato — não existe "reentrada" possível neste gatilho |
| Contatos em múltiplos workflows | Permitido | É o primeiro de todos; o contato ainda vai entrar em Cadência 12x30/Inbound depois |

### Nó único

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | **Criar oportunidade** | Create/Update Opportunity | Pipeline: `FUNIL DE VENDAS` · Etapa: `NOVO LEAD` · Nome da oportunidade: `{{contact.name}}` · Status: `open` · **Allow Duplicate Opportunities: desligado** |

Um nó só, de propósito — qualquer coisa a mais aqui (tag de origem,
atribuição de dono, verificação de telefone) já tem lugar certo mais à
frente na máquina (nó 0 da Cadência 12x30, seção 2.3) e duplicaria lógica
em vez de reaproveitar. Pesquisado antes de fechar em `Allow Duplicate
Opportunities: desligado`: é o padrão nativo da ação — encontrando uma
oportunidade existente do mesmo contato nesse pipeline, ela **atualiza**
em vez de duplicar. É o que torna este workflow seguro mesmo se algum dia
outro fluxo tentar criar oportunidade de novo para o mesmo contato: sem
isso ligado, cada tentativa criaria uma cópia nova.

### Limite conhecido — importação em massa não dispara `Contact Created`

Pesquisado e confirmado: contato criado por importação de CSV **não**
dispara `Contact Created` — é proteção da própria HighLevel contra
disparar automação em massa sem querer, a mesma razão pela qual este
projeto nunca usou esse gatilho para a Cadência (seção 2.1). Consequência
prática: lead que entrar por importação de lista continua precisando do
mesmo contorno manual documentado abaixo, não é bug deste workflow.

### Backfill dos contatos já existentes — ação manual urgente, não automática

`Contact Created` só dispara para contato **criado depois** de o workflow
publicado existir — os contatos já cadastrados na subconta (a maioria
leads reais do Meta, `source: Facebook`, ver o número exato reconfirmado
na seção 1.3 acima) não vão ganhar oportunidade sozinhos quando este
workflow for publicado. Mesma classe de limite do parágrafo acima, mesmo
contorno: depois de publicar, em Contatos, selecione todos e rode a ação
em massa **Add to Workflow** apontando para `Porta de Entrada` uma única
vez — seguro por ser idempotente (o nó único não duplica, ver acima).
**Prioridade sobre o resto do `GUIA-MONTAGEM.md`:** este workflow não
depende de calendário nem de campo novo, só do pipeline (Fase 1, já
concluída) — pode e deve ser montado antes da Fase 3, porque cada hora sem
ele é lead pago do Meta acumulando sem nunca entrar em etapa nenhuma.

### O que este item não resolve — L-07 continua aberto

Este workflow só cria a oportunidade em `NOVO LEAD`. A promoção `NOVO
LEAD` → `CONECTAR` (que é o que de fato liga a Cadência 12x30, seção 2.1)
continua decisão manual do SDR — lacuna L-07 (`briefing-sdr.md`), não
tocada aqui de propósito: resolver as duas juntas misturaria "o lead
existe no funil" com "o lead está pronto para ser trabalhado", que são
validações diferentes (a segunda depende de telefone confirmado, a
primeira não).

---

### 1.4 Workflow "Reentrada por Formulário" — F-11

**Por quê:** um lead que já saiu do funil (`status` `abandoned` ou `lost` —
12 tentativas esgotadas, número errado, desqualificado) e depois **preenche
de novo** o mesmo formulário de um anúncio do Meta é o sinal de reengajamento
mais forte que existe: dinheiro pago de novo, de propósito, pela mesma
pessoa. Hoje esse sinal é invisível para a máquina inteira. A Porta de
Entrada (G-01, seção 1.3) só reage a `Contact Created`, e a HighLevel
deduplica contato por e-mail/telefone — uma resubmissão de um contato que
já existe **atualiza** o registro, não recria, então `Contact Created` nunca
dispara de novo (pesquisado: comportamento de deduplicação nativo,
confirmado por página oficial da HighLevel citada em duas buscas com termos
diferentes — mesmo padrão de confiança já usado no G-05). O único caminho de
volta hoje é o Reengajamento 90 dias (R-08, seção 2.12), que só cobre quem
saiu **pela via `nutricao-90d`** e só reage **90 dias depois**, não no
instante em que o lead literalmente acabou de levantar a mão de novo. É
exatamente o tipo de dívida que o F-01 já descreveu para outro sinal ("sinal
ignorado é dívida que não se paga retroativamente") — aqui o sinal nem chega
a ser ignorado, ele nunca é lido. E é o tipo de vantagem que "faça melhor,
não igual" pede: Reev, Meetime, Outreach e Salesloft não enxergam a
resubmissão de um anúncio — só recebem o que alguém empurra para eles via
integração, uma vez. Aqui o CRM **é** a plataforma de anúncio, então o dado
já está disponível nativamente; nenhuma das quatro plataformas de sales
engagement tem como copiar isso olhando só a tela delas.

**Como:** workflow novo e pequeno, símile do G-05/R-08 ("não dá para caber
dentro do workflow que já existe, um workflow curto e próprio resolve sem
tocar em nada publicado").

**Gatilho: `Facebook Lead Form Submitted`**, sem filtro de formulário
específico — pesquisado: diferente do que motivou o G-01 a **rejeitar** este
gatilho para a entrada nova ("só cobre a origem Meta", o oposto de "toda
origem" que aquele caso pedia), aqui a origem já é conhecida de propósito —
é reentrada de quem **já** veio do Meta, e não da entrada genérica que a
Porta de Entrada cobre. A documentação e guias de terceiros confirmam que o
gatilho aceita filtro por página + formulário específico, mas não deixam
claro se "sem filtro" cobre todos os formulários conectados de uma vez —
**confiança média**, não testado nesta subconta. Se a tela exigir escolher
um formulário por vez, a saída é a mesma do G-04 (Opção A): uma cópia deste
workflow por formulário — hoje são 8 (`ROADMAP-SALES-ENGAGEMENT.md`, G-04) —,
registrada aqui como pendência explícita, não como bloqueio: o primeiro
formulário já vale a pena montado sozinho.

**Configurações do workflow**

| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | Cada resubmissão do formulário é um evento novo e genuíno — mesmo raciocínio já usado no R-08 (seção 2.12) para a tag `nutricao-90d`: sem reentrada ligada, o lead só reativaria uma vez na vida e a segunda resubmissão cairia no vazio |
| Janela de envio / Stop on Response | Não se aplica | O único trabalho aqui é reabrir a oportunidade e (no ramo de exceção) avisar o gestor — nenhuma mensagem sai deste workflow, mesmo raciocínio da Porta de Entrada (seção 1.3) |
| Contatos em múltiplos workflows | Permitido | O contato pode estar (raramente) noutra régua ao mesmo tempo; este workflow só mexe na etapa/status da oportunidade, não compete por tarefa ou tag de fila |

### Nós

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | **Portão de estado** | If/Else | `status` da oportunidade no `FUNIL DE VENDAS` **é** `abandoned` **ou** `lost` → nó 2. Senão (nenhuma oportunidade ainda, ou já `open`) → **Remove from Workflow: este** |
| 2 | **Portão de consentimento** | If/Else | tag `nao-perturbe` presente → nó 2b. Senão → nó 3 |
| 2b | Ramo do opt-out | Internal Notification para o gestor: `{{contact.name}} reenviou um formulário do Meta, mas está marcado nao-perturbe — decisão manual sobre reabrir a oportunidade` → **Remove from Workflow: este** | Mesmo padrão do nó 0.0b (seção 2.3): achado ambíguo não se resolve sozinho, vai para o gestor decidir |
| 3 | Reabertura | Update Opportunity | Etapa → `NOVO LEAD` · `status` → `open` |
| 4 | Limpeza de estado antigo | Remove Contact Tag | `nutricao-90d` (idempotente, mesmo se ausente — mesma linguagem já usada no nó 4 do R-08, seção 2.12) |
| 5 | Registro | Add Note | `Oportunidade reaberta em {{right_now}} — lead reenviou o formulário do Meta. Reentrada automática (F-11), etapa reiniciada em NOVO LEAD para nova triagem do SDR.` |

**Por que volta para `NOVO LEAD` e não direto para `CONECTAR` (ao contrário
do R-08, que reativa direto em `CONECTAR`):** o R-08 sabe que o lead já
passou pela triagem uma vez (12 tentativas completas). Aqui não — o motivo
da saída pode ter sido `Número errado` ou uma desqualificação por falta de
fit, e mandar direto para `CONECTAR` puxaria a cadência de novo sem
ninguém olhar. `NOVO LEAD` é o mesmo ponto de entrada que todo lead
genuinamente novo usa (G-01) — reaproveita a mesma decisão manual do SDR
(L-07/G-03) em vez de abrir uma terceira porta com regra própria.

**Por que o nó 1 não precisa distinguir "nenhuma oportunidade" de
"oportunidade já `open`":** nos dois casos a ação certa é a mesma — não
fazer nada. Contato realmente novo já está coberto pela Porta de Entrada
(que dispara por `Contact Created`, evento diferente, sem corrida entre os
dois: este workflow só age quando encontra `abandoned`/`lost`, condição que
um contato novíssimo nunca tem). Lead já `open` está correndo alguma
cadência agora — reabrir de novo duplicaria régua, o mesmo erro que o
`Allow Re-entry` desligado da 12x30 (D-06) já existe para evitar.

**Por que checar `nao-perturbe` e não o DND nativo direto:** todo outro
portão deste documento (nó 3 da seção 2.4, nó 2 do R-08, nó 0.0b) usa a tag
como fonte da verdade para "não procurar este lead", nunca o DND nativo
isolado — e o ramo `Não ligar` do Pós-ligação (seção 4) sempre aplica os
dois juntos, então checar a tag cobre o mesmo caso sem inventar uma segunda
fonte de verdade só para este workflow.

**Interação com o R-08 (Reengajamento 90 dias) — verificada, não montada às
cegas:** o nó 2 do R-08 (seção 2.12) já checa `status` **ao vivo** ("Status
da oportunidade é `abandoned`") antes de reativar, com exatamente esta nota
no próprio item: "não reativa quem já mudou de estado por conta própria".
Se este workflow reabrir o lead antes do relógio de 90 dias do R-08 vencer,
quando o `Wait` dele terminar o portão vai encontrar `status = open` (não
mais `abandoned`) e sair pelo ramo 2b, um no-op limpo — nenhuma tentativa
duplicada, nenhuma mudança necessária no R-08. É o mesmo tipo de garantia
que a migração do G-02 já deixou espalhada pelo documento (checar estado ao
vivo, não confiar em quando um evento aconteceu).

#### Conferência do F-11, 22/09/2026 (mesma rodada): falta o reset que o R-08 tem, e a tag que ninguém remove

O desenho está certo onde importa — o portão do nó 1 resolve a corrida com a
Porta de Entrada sem precisar distinguir "sem oportunidade" de "já `open`", e a
interação com o R-08 foi conferida contra o portão real dele, não suposta. Três
acréscimos.

**1. A dúvida do "sem filtro" se resolve, e a favor de um workflow só.** A
ressalva de confiança média sobre `Facebook Lead Form Submitted` cobrir todos os
formulários de uma vez tem resposta na própria recomendação de boas práticas que
a pesquisa desta rodada trouxe: *evite um gatilho que aceite todo formulário do
Facebook de toda oferta **a menos que todos pertençam ao mesmo pipeline e
etapa***. Isso (a) implica que o gatilho **aceita** ficar sem filtro, senão não
haveria o que evitar, e (b) descreve a exceção que é exatamente este caso — os
oito formulários desta subconta alimentam **o mesmo** pipeline (`FUNIL DE
VENDAS`) e **a mesma** etapa (`NOVO LEAD`). Então a pendência das "8 cópias"
provavelmente não existe: monte **um** workflow sem filtro de formulário. Se a
tela exigir escolher um, aí sim as cópias — mas não planeje para isso.

**2. Falta o reset de rodada, e o R-08 já tem o nó pronto para copiar.** O nó 3
reabre a oportunidade e o nó 4 tira `nutricao-90d`, mas **nenhum campo de
contador é zerado.** O lead volta para `NOVO LEAD` carregando o estado do fim da
régua anterior:

| Campo, como fica | Efeito quando o SDR promover para `CONECTAR` |
|---|---|
| `Tentativa nº` = 12 | A cadência pode encerrar na entrada — a régua tem 12 tentativas, e ele já está na 12ª |
| `WA não atendidas seguidas` ≥ 2 | O seletor de canal (nó 4 da 2.4) manda direto para telefone, **do primeiro toque**, porque o contador ainda está estourado |
| `Resultado da tentativa` = valor antigo (`Não atendeu`, `Número errado`…) | O nó 10 decide pelo valor velho; e o Pós-ligação pode não disparar na primeira classificação nova, se o SDR escolher o **mesmo** valor que já está lá (gatilho é *mudança* de campo) |
| `Prioridade` = 1 ou 2 (rebaixada no fim da régua) | O lead que acabou de levantar a mão entra no fim da fila |

Ou seja: **o lead que deu o sinal mais forte que existe recebe o pior tratamento
da máquina.** O R-08, que faz a mesma coisa (reativar um lead que saiu), já
resolve isso no nó 3 dele (seção 2.12) — copie literalmente:

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 3b | Reset de rodada | Update Contact Field | `Tentativa nº` = 0 · `WA não atendidas seguidas` = 0 · `Resultado da tentativa` = vazio · `Prioridade` = 3 · `Entrada em` = `{{right_now}}` · `1ª tentativa em` = vazio |

Mesmos seis campos, mesmo motivo, e entra **entre** os nós 3 e 4 — antes de o
lead ficar visível na fila do SDR.

**3. `telefone-invalido` é aplicada em dois lugares e removida em nenhum — e
esta é a resubmissão mais provável de todas.** `grep` confirma: a tag nasce no
nó 0.0b da 2.4 e da 2.10, e **nenhum** nó do documento a remove. Agora junte com
o caso de uso: **por que um lead reenviaria o formulário?** O motivo número um é
que o telefone estava errado e ele corrigiu. A resubmissão traz telefone novo,
que a HighLevel escreve no contato existente — e no mesmo instante a tag
`telefone-invalido` passa a ser **factualmente falsa**, num contato que ela
ainda marca, alimentando a lista de higiene do R-13.

O nó 4 é o único lugar do projeto que pode limpá-la:

| # | Nó | Ação |
|---|---|---|
| 4 | Limpeza de estado antigo | Remove Contact Tag: `nutricao-90d` **e `telefone-invalido`** |

**O trade-off, declarado em vez de escondido:** se o telefone reenviado for o
mesmo número errado, remover a tag perde a informação. Recomendo remover de todo
jeito, porque o sistema se autocorrige — a próxima tentativa classificada como
`Número errado` reaplica a tag pelo caminho normal — enquanto uma tag "inválido"
grudada num contato cujo telefone acabou de ser atualizado não se corrige nunca e
contamina a higiene. É uma escolha, não um fato; se o dono preferir o contrário,
é uma linha a menos.

**`nao-perturbe` continua fora dessa limpeza, de propósito** — é o portão de
consentimento do nó 2, e apagá-la aqui transformaria uma resubmissão de
formulário em revogação automática de opt-out, que não é o que um clique em
anúncio significa.

**Zero campo, zero tag novos:** reaproveita `status`, etapa, `nao-perturbe`
e `nutricao-90d`, todos já existentes. Não depende de `APROVADO.md` para a
especificação; a montagem na tela (workflow não sai por API) segue a mesma
fila manual dos demais.

**Pronto quando:** todo lead com oportunidade `abandoned`/`lost` que
reenviar um formulário do Meta sem estar marcado `nao-perturbe` volta para
`NOVO LEAD`/`open` sozinho, pronto para nova triagem do SDR — sem esperar o
relógio de 90 dias do R-08 nem depender de alguém abrir uma lista para
notar que o lead voltou.

---

## 2. Workflow "Cadência 12x30"

### 2.1 Gatilho — migrado para as 5 etapas reais em 18/09/2026

**Opportunity Stage Changed** (Etapa da oportunidade alterada)
- Pipeline: `FUNIL DE VENDAS` (é o mesmo objeto que este documento chama de
  `Pré-vendas` — seção 1)
- Para a etapa: `CONECTAR`
- Filtro adicional (R-07): tag `cad-inbound` **ausente**
- Filtro adicional (R-08): tag `reengajamento-ativo` **ausente**

Não use "Contact Tag Added" como gatilho: a tag é consequência da cadência,
não causa dela. E não use "Contact Created", senão o lead entra antes de ter
telefone validado.

O filtro do R-08 existe por um caso que só aparece com o Reengajamento 90
dias (seção 2.12, migrada para as 5 etapas reais em 19/09/2026) montado: um
lead pode chegar a `status = abandoned` sem nunca ter
entrado de verdade nesta cadência 12x30 — por exemplo, um lead inbound que
recebeu `Número errado` ainda dentro da Cadência Inbound (seção 2.10, antes
do handoff da TI5) e tinha e-mail cadastrado cai direto em `abandoned` pelo
ramo `Número errado` do Pós-ligação (seção 4), sem nunca ter passado pelas
tentativas T1-T12 desta cadência. 90 dias depois, o Reengajamento reativa
esse lead: `Allow Re-entry` desligado (D-06) não bloquearia a entrada dele
aqui, porque "bloquear" só vale para quem já tem histórico *neste workflow
específico*, e ele nunca teve — sem o filtro, ele entraria de verdade,
duplicando a régua que o Reengajamento já está rodando na TR{n} dele.
`reengajamento-ativo` fecha esse buraco sem depender de reconstruir a
história do contato.

O filtro de tag é o que separa este workflow do "Cadência Inbound" (seção
2.10, R-07 do roadmap): os dois escutam o mesmo evento — entrar em
`CONECTAR` — e cada um pega a fatia que é sua, sem If/Else nenhum decidindo
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
| Allow Re-entry | **Desligado** (decisão D-06) | Com reentrada ligada, o lead que volta para `CONECTAR` ganha tentativas duplicadas |
| Contatos em múltiplos workflows | Permitido | O lead fica também no de IA |

### 2.3 Nó 0 — inicialização (uma vez, antes da T1)

| Nó | Ação | Configuração |
|---|---|---|
| 0.0 | If/Else (R-13) | Campo nativo `Phone` **está vazio** → ramo 0.0b. Senão → segue para 0.1 |
| 0.0b | Ramo sem telefone | Add Contact Tag `telefone-invalido` → If/Else: `Site` **ou** `Instagram` preenchido → Update Opportunity `status` = `abandoned` + Add Contact Tag `nutricao-90d`. Senão → Update Opportunity `status` = `lost` → Internal Notification para o gestor: `Lead sem telefone: {{contact.name}} — revisar a fonte da lista antes de qualquer tentativa` → **Remove from Workflow: este** |
| 0.1 | Update Contact Field | `Tentativa nº` = 0 |
| 0.2 | Update Contact Field | `WA não atendidas seguidas` = 0 |
| 0.3 | Update Contact Field | `Resultado da tentativa` = vazio |
| 0.4 | If/Else | `Permissão WhatsApp` está vazio → Update: `Não solicitado` |
| 0.5 | Update Contact Field | `Prioridade` = 3 (padrão; a seção 9 recalcula) |
| 0.6 | Update Contact Field | `Entrada em` = `{{right_now}}` (R-02 — carimbo de speed-to-lead) |
| 0.7 | If/Else (R-10) | campo nativo `Assigned User` está vazio → segue para 0.7b. Senão → pula 0.7b (contato já tem dono; ver seção 2.14) |
| 0.7b | Assign to User → modo `Round Robin` | Lista de SDRs ativos, configurada na tela do nó (seção 2.14) |

**Por que o portão de higiene (0.0/0.0b) vem antes de qualquer outro nó, e
não dentro do portão da tentativa (nó 3, seção 2.4) — R-13:** o bloqueio
duplicidade da subconta (e-mail e telefone) não cobre o contato que nasce
**sem** telefone nenhum — só duplicata. Sem o 0.0, esse lead entraria nas 12
tentativas normalmente: as tentativas de telefone falhariam sempre, e as de
WhatsApp também, porque WhatsApp neste projeto é sempre ligação/mensagem
**pelo número de telefone** do contato (seção "A máquina",
`briefing-sdr.md`) — sem número, os 3 canais falham, não só 1. O portão do
nó 3 já bloqueia telefone quando `telefone-invalido` está presente, mas
**não** bloqueia WhatsApp por essa tag — o desenho dele assume que
`telefone-invalido` só nasce depois de uma ligação de verdade confirmar
"número errado" (ramo da seção 4), quando o lead já está saindo de cadência
de qualquer forma. Um portão dentro do nó 3 chegaria tarde: o lead ainda
gastaria a T1 inteira (mensagem + telefone + WhatsApp do D1) antes de
qualquer verificação rodar. O nó 0.0 resolve antes da primeira tentativa
existir, reaproveitando a mesma tag (`telefone-invalido`, T-09) e o mesmo
desenho de saída (e-mail/Instagram → `abandoned`, senão → `lost`) que
o ramo `Número errado` da seção 4 já usa — zero tag e zero campo novos.

### 2.4 O bloco padrão de uma tentativa (9 nós)

Este é o molde. Repita 12 vezes trocando dia, horário, canal e número. `{n}` é
o número da tentativa.

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | **Aguardar dia** | Wait → Time Delay | Dias corridos até o dia da tentativa (delta em relação à tentativa anterior — tabela 2.5) |
| 2 | **Aguardar horário** | Wait → Until specific time | O horário da tabela 2.5. A janela do 2.2 empurra para o próximo dia útil se cair fora |
| 2.5 | **Pausa individual (R-09)** | If/Else | tag `pausado` presente → ramo 2.5b. Senão → segue para o nó 2.5c |
| 2.5b | Ramo da pausa individual | Wait → Time Delay 1 dia → **volta para o nó 2.5** | Não cria tag de fila, não cria tarefa, não avança `Tentativa nº`. Reconsulta a tag uma vez por dia até o SDR remover — a tentativa fica represada no mesmo lugar, não é descartada nem reagendada |
| 2.5c | **Portão de frequência (F-04)** | If/Else | `Toques na semana` **≥** 6 → ramo 2.5d. Senão → segue para o Portão (nó 3) |
| 2.5d | Ramo do teto de toques | Wait → Time Delay 1 dia → **volta para o nó 2.5c** | Mesmo mecanismo do 2.5/2.5b, teto em vez de pausa: represa sem consumir `Tentativa nº`, tag de fila ou tarefa. Some sozinho quando o Contador de Toques (seção 2.19) decrementar o campo abaixo de 6 — nenhuma ação manual precisa remover nada, ao contrário da pausa individual |
| 3 | **Portão** | If/Else — condições **E** | Etapa da oportunidade **é** `CONECTAR` · `status` da oportunidade **é** `open` · tag `nao-perturbe` **não** presente · `Resultado da tentativa` **não é** `Não ligar` · (só em tentativa de telefone) tag `telefone-invalido` **não** presente |
| 3b | Ramo falso do portão | Remove Contact Tag `fila-tel`, `fila-wa`, `fila-quente` → Add Contact Tag `limpar-tarefas` → **Remove from Workflow: este** | Saída limpa. Sem isso, sobra tag e tarefa órfã |
| 4 | **Seletor de canal** | If/Else (só em tentativa de WhatsApp) | Ramo WA: `Permissão WhatsApp` **é** `Sim` **E** `WA não atendidas seguidas` **<** 2. Ramo senão: vira telefone (decisão D-04 + regra das 2 seguidas) |
| 5 | **Limpar resultado** | Update Contact Field | `Resultado da tentativa` = vazio · `Tentativa nº` = `{n}` |
| 6 | **Adicionar tag de fila** | Add Contact Tag | `fila-tel` (telefone) ou `fila-wa` (WhatsApp) |
| 7 | **Criar tarefa** | Add Task | Título: `[CADENCIA] T{n} · Ligar (telefone)` ou `[CADENCIA] T{n} · Ligar (WhatsApp)` · Vence: hoje no horário da tentativa · Atribuir: `Contact Owner` (dinâmico — segue o `Assigned User` do nó 0.7b, R-10, seção 2.14) · Depois: Add Contact Tag `toque` (F-04, seção 2.19 — cada tarefa criada é um toque, alimenta o Contador) |
| 8 | **Aguardar resultado** | Wait → Condition, com tempo limite | Condição: `Resultado da tentativa` **não está vazio**. Tempo limite: até **18:30 do mesmo dia**. Se a sua versão não tiver Wait por condição, use Wait → Until 18:30 e um If/Else checando o campo — mesmo efeito |
| 9 | **Remover tag de fila** | Remove Contact Tag | `fila-tel` e `fila-wa` (remova as duas, sempre — barato e evita tag presa) |
| 10 | **Condição por resultado** | If/Else | `Atendeu` ou `Pediu retorno` → **Remove from Workflow: este** (quem move etapa é o Pós-ligação, seção 4) · `Número errado`, `Não ligar` ou `Desqualificado` (R-18) → **Remove from Workflow: este** · qualquer outro / tempo limite → segue para a próxima tentativa. **Só `Caixa Postal` e `Não atendeu` continuam a régua** — a lista é fechada de propósito, ver nota abaixo |
| 10b | Ramo do tempo limite | Update Contact Field | `Resultado da tentativa` = `Não atendeu` · Add Contact Tag `limpar-tarefas` (a tarefa do dia não foi feita; a rotina horária fecha) |

**Por que o nó 10 lista os resultados que encerram, em vez de listar os que
continuam (e por que `Desqualificado` entrou nele em 21/09/2026):** o nó
manda para a próxima tentativa tudo que não reconhece — "qualquer outro".
Isso faz dele um portão que **erra para o lado de insistir**: toda opção nova
em `Resultado da tentativa` nasce, por omissão, significando "continue
ligando". O R-18 criou a opção `Desqualificado`, e sem esta linha um lead que
o SDR acabou de desqualificar na conversa receberia a tentativa seguinte no
dia seguinte — exatamente o contrário do que o item foi desenhado para
resolver. O Mestre de saída (seção 3) acabaria removendo o contato, porque o
ramo novo muda `status`, mas só depois da janela assíncrona de sempre, e o
texto do nó continuaria dizendo a coisa errada para quem monta na tela.

**Regra para a próxima opção nova:** hoje só `Caixa Postal` e `Não atendeu`
continuam a régua. Ao acrescentar uma sétima, oitava opção em `Resultado da
tentativa`, decida explicitamente em qual dos dois lados ela cai **antes** de
criá-la na tela — e, se o padrão "qualquer outro → insiste" ficar arriscado
demais, inverta o nó: liste `Caixa Postal` e `Não atendeu` como os únicos que
seguem, e mande todo o resto encerrar. A inversão é mais segura por
construção; ficou como opção registrada, não aplicada, porque mexer num nó
de uma régua que ainda não foi publicada é barato, mas mudar a forma do
portão sem necessidade não é.

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

**Por que o teto de toques (nó 2.5c) é o mesmo laço de 1 dia, e não um
`Remove from Workflow` — F-04:** a régua de 12 tentativas não fez nada errado
quando um lead esbarra no teto — o excesso normalmente vem de **fora** dela
(sinal clicado várias vezes, uma segunda régua que devia estar bloqueada mas
não bloqueou). Tirar o lead da Cadência 12x30 puniria a régua certa pelo
excesso causado por outra coisa, e ainda esbarraria no mesmo `Allow Re-entry`
desligado que o R-08 já pagou caro (`APRENDIZADOS-CRM.md`). Represar copia o
padrão do 2.5/2.5b, com uma diferença: a pausa individual só sai quando o SDR
tira a tag `pausado` à mão; o teto sai sozinho, porque o Contador de Toques
(seção 2.19) decrementa `Toques na semana` 7 dias depois de cada toque — o
lead retoma sem ninguém precisar lembrar de destravar nada.

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

Nós de envio (**Send WhatsApp, sem fallback de SMS** — decisão do dono em
19/09/2026: SMS não é canal de contato com lead neste projeto, e um fallback
que contradiz a decisão é pior que nenhum, porque dispara justamente quando
ninguém está olhando. WhatsApp fora do ar não vira SMS: vira
`Internal Notification` para o gestor e a régua segue pelo telefone, que é o
canal que não depende de provedor de texto), posicionados no fluxo conforme a
tabela 2.5. Cada um precedido do
mesmo **portão** do nó 3 (sem a checagem de `telefone-invalido`) e com a
condição extra `nao-perturbe` ausente, **e do portão de janela de 24h da
seção 2.6.2 (G-05) — sem ele, a mensagem livre é recusada pelo WhatsApp
Business API na maioria dos envios**, e seguido de dois nós **Update Contact
Field** `Template usado` = o código da mensagem (R-04 — sem esse carimbo não
dá para saber depois qual abertura gerou a resposta) e **Add Contact Tag**
`toque` (F-04, seção 2.19 — mensagem automática também é toque; M2 e M3 não
passam pelo portão de frequência do nó 2.5c porque só disparam depois da T8 e
da T12, quando o teto semanal já não é o risco real). M1 é exceção: em vez de
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
`nutricao-90d` → Update Opportunity `status` = `abandoned` (a oportunidade
**permanece** em `CONECTAR` — 12 tentativas esgotadas não é mais um
movimento de etapa, é status, ver tabela 1.0) → fim do workflow. A mudança
de status aciona o Mestre de saída (seção 3, gatilho `Opportunity Status
Changed`), que limpa o resto.

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
| M1.3a (Caminho A) | **Guarda de janela (seção 2.6.2, G-05)** → Send WhatsApp | Dentro da janela: texto livre `M1-a` · Fora da janela: Template Meta `M1-a`, `biblioteca-mensagens.md` |
| M1.4a (Caminho A) | Update Contact Field → Add Contact Tag | `Template usado` = `M1-a` → `toque` (F-04, seção 2.19) |
| M1.3b (Caminho B) | **Guarda de janela (seção 2.6.2, G-05)** → Send WhatsApp | Dentro da janela: texto livre `M1-b` · Fora da janela: Template Meta `M1-b`, `biblioteca-mensagens.md` |
| M1.4b (Caminho B) | Update Contact Field → Add Contact Tag | `Template usado` = `M1-b` → `toque` (F-04, seção 2.19) |

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

### 2.6.2 Guarda de janela de atendimento (24h) antes de cada mensagem livre — G-05

**Por quê:** o WhatsApp Business API só aceita mensagem de **texto livre**
quando o contato está dentro da **janela de atendimento de 24h** — que abre
quando o **cliente** manda mensagem primeiro, não quando a operação inicia o
contato, e fecha 24h depois do último toque dele. Fora dela, só um
**Template** pré-aprovado pela Meta pode ser enviado. Nenhum lead desta base
jamais escreveu no WhatsApp da subconta antes de M1 (vêm de Meta Lead Ads e
formulário) — a primeira mensagem de todo lead já nasce fora da janela por
definição, e M2 (D10) e M3 (D30) quase sempre também, porque a maioria dos
leads nunca responde nada entre uma mensagem e a próxima. Sem esta guarda, o
texto livre de `M1-a`/`M1-b`/`M2-v1`/`M3-v1` seria recusado pela API na
maioria dos envios assim que a `Cadência 12x30` publicar — silenciosamente,
do mesmo jeito que motivou o F-05 (roadmap).

**Como (pesquisado via `WebSearch`, confiança média — página de suporte
oficial da HighLevel confirmada por citação direta e idêntica em duas
buscas com termos diferentes, não testada nesta subconta, domínio bloqueado
pelo proxy deste ambiente):** o GHL tem a ação nativa
**`WhatsApp: Customer Service Window Check`**, que confere se o contato
está dentro da janela, e a ação **`Send WhatsApp`** aceita um modo
**Template** (em vez de "None – Manual Text") que envia uma mensagem
pré-aprovada pela Meta — funciona dentro **e** fora da janela, diferente do
texto livre, que só funciona dentro.

| Nó | Ação | Configuração |
|---|---|---|
| G.1 | **`WhatsApp: Customer Service Window Check`** | Confere o contato disparando o envio |
| G.2 (dentro da janela) | segue | para o nó `Send WhatsApp` já especificado, texto livre, sem mudar nada |
| G.3 (fora da janela) | `Send WhatsApp`, modo **Template** | Template Meta equivalente ao texto livre (tabela abaixo) |

Insira `G.1` imediatamente antes de cada nó `Send WhatsApp` de texto livre já
especificado neste documento, e ligue o ramo "fora da janela" ao mesmo
destino que o texto livre segue hoje (ex.: `M1.4a`) — a guarda não muda o
resto do fluxo, só decide qual dos dois envios sai.

| Código (texto livre) | Template Meta equivalente | Status |
|---|---|---|
| `M1-a` | `m1_a` (nome sugerido, a confirmar na submissão) | A submeter pelo dono no Meta Business Manager |
| `M1-b` | `m1_b` | A submeter pelo dono no Meta Business Manager |
| `M2-v1` | `m2_v1` | A submeter pelo dono no Meta Business Manager |
| `M3-v1` | `m3_v1` | A submeter pelo dono no Meta Business Manager |

Os merge fields do texto livre (`{{contact.first_name}}`,
`{{contact.segmento}}`, `{{user.first_name}}`, `{{location.name}}`) viram
variáveis posicionadas do Template na submissão à Meta — mapeamento exato a
confirmar na tela do Business Manager, não sai por API. O Trigger Link
`[Agendar com o closer]` (citado em `M2-v1`/`M3-v1`) provavelmente precisa
virar um botão CTA de URL do Template em vez de texto inline — Template tem
formatação mais restrita que mensagem livre; a confirmar na tela antes de
submeter.

**Limite documentado, não escondido:** aprovação de Template pela Meta leva
até 48h e é decisão/ação do dono (Business Manager, fora deste conector) —
esta guarda não desbloqueia sozinha, só evita que o texto livre seja
recusado enquanto o Template não existe (o ramo "fora da janela" fica sem
efeito até o Template ser aprovado e configurado no nó `G.3`).

**Cobertura, conferida em 22/09/2026 — o G-05 está fechado:** esta peça
cobriu os quatro envios da Cadência 12x30 (M1-a, M1-b, M2-v1, M3-v1); a
peça 2 cobriu `MI-0`/`MI-F` (Cadência Inbound, 2.10), `RE-1`/`RE-2`
(Reengajamento, 2.12), `NS-1`/`NS-2` (Recuperação de No-show, 5.3) e a
confirmação mais os três lembretes do Pós-agendamento (seção 5, nós 7-10,
que ganharam código e texto naquela rodada porque não tinham); o G-06 cobriu
a entrada da Qualificação por IA (6.0) e as 8 perguntas do Caminho B.
Verificado nó a nó: **todo `Send WhatsApp` de texto livre deste documento
tem guarda de janela antes dele.** O parágrafo anterior aqui dizia o
contrário e ficou desatualizado por duas rodadas — corrigido.

**Como conferir de novo, e o cuidado que essa conferência exige:** a guarda
aparece escrita de **três formas diferentes** ao longo do documento —
`WhatsApp: Customer Service Window Check` (o nome da ação), `Guarda de
janela (seção 2.6.2, G-05)` (a referência curta) e `Send WhatsApp, modo
Template` (só o ramo de fora). Procurar apenas pelo nome da ação encontra 5
lugares e dá a impressão de que o resto está descoberto; é preciso procurar
as três. O jeito que não erra é listar os envios e olhar as linhas
anteriores a cada um:

```
python3 - <<'EOF'
L=open('wesales/build-wesales.md').read().split('\n')
for i,l in enumerate(L):
    if 'Send WhatsApp' in l and ('exto livre' in l or 'pergunta' in l):
        ctx='\n'.join(L[max(0,i-7):i+1])
        ok = ('uarda de janela' in ctx) or ('Window Check' in ctx) or ('modo Template' in ctx)
        print('OK ' if ok else 'SEM', i+1, l[:80])
EOF
```

**Pronto quando (desta peça):** M1.3a/M1.3b/M2.2/M3.2 (`IMPLEMENTACAO-WORKFLOWS.md`)
têm o `Customer Service Window Check` antes deles e os dois ramos
especificados.

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

**A assimetria de `Permissão WhatsApp` entre este portão e o nó 4 da seção
2.4 é deliberada — conferida e documentada em 22/09/2026 para ninguém
"consertar" um dos dois lados sem querer:**

| Onde | Condição | Efeito |
|---|---|---|
| Nó 4 do bloco padrão (2.4) — **tentativa por ligação de WhatsApp** | `Permissão WhatsApp` **é** `Sim` | lista de permissão: só quem autorizou expressamente |
| Nó `a` aqui — **mensagem de texto da IA** | `Permissão WhatsApp` **≠** `Não` | lista de recusa: entra também quem está em `Não solicitado` |

Não é descuido de um dos dois: **ligação de WhatsApp toca o telefone da
pessoa**, e o `Sim` é justamente o que o SDR pede numa ligação anterior
(seção 6, roteiro); **mensagem de texto é a fricção mais baixa que existe**,
e o convite `QI-1` da guarda 6.0 é literalmente o pedido de consentimento —
exigir consentimento para poder pedir consentimento fecharia o caminho em si
mesmo. Um lead vindo de Meta Lead Ads nasce `Não solicitado` e deu o telefone
num formulário: pode receber mensagem, não pode receber chamada.

**O que continua valendo para os dois:** `Não` bloqueia tudo, e a tag
`nao-perturbe` bloqueia tudo por um caminho independente (o nó 3 do Mestre de
saída remove o contato deste workflow, seção 3). Se o dono quiser a régua
mais estrita — só `Sim` também para mensagem —, o lugar é este nó `a`, e o
custo é que a IA nunca alcança lead nenhum que não tenha atendido uma ligação
antes, o que esvazia o item.

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

Um terceiro workflow desta família, 2.9.5, tem efeito **oposto** aos dois
acima — não fura fila, cala a régua — e existe por um achado desta rodada:
o 2.9.3 abaixo trata **toda** resposta de WhatsApp como sinal quente, sem
olhar o conteúdo. Detalhe no próprio 2.9.5 (R-17 do roadmap).

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
| Janela de envio | **Sem restrição, 24/7** — decisão do dono ao vivo, 19/09/2026: nenhum dos 8 nós manda mensagem pro lead (só atualização de campo, tag, tarefa e aviso interno); travar numa janela de expediente perde exatamente a vantagem de interceptar o sinal na hora. Não confundir com a janela 08:30–18:30 da Cadência 12x30 (seção 2), que continua valendo lá porque aquela liga/manda mensagem de verdade |
| Allow Re-entry | Ligado (cada clique é um sinal novo) |
| Stop on Response | Desligado |

**Achado ao vivo em chat, 19/09/2026, montando isto na tela:** um gatilho
`Trigger Link Clicked` não carrega a oportunidade do contato no contexto do
workflow — o If/Else não enxerga a categoria "Opportunities" até existir uma
ação `Find opportunity` antes dele (o GHL mostra um aviso pedindo isso). E o
GHL não expõe "data/hora atual" como valor inserível num campo de contato de
texto (só Custom Values fixos e outros campos) — por isso `Data e hora do
sinal` saiu da lista de nós; Tarefa e Nota já carimbam a própria data de
criação nativamente, o que cobre a mesma necessidade de auditoria sem
duplicar em campo. A tabela abaixo é a sequência real, não a original.

**Consequência ainda não resolvida, e ela é grande:** se "data/hora atual" não
entra em campo de texto, `{{right_now}}` — usado em **17 nós** deste documento
para carimbar `Entrada em` (C-18), `1ª tentativa em` (C-19) e o reset da
reativação — não existe também, e aí o R-02 (speed-to-lead) e o relógio da
reativação do R-08 não se montam como estão escritos. Ou o achado acima é mais
estreito do que parece (o seletor pode oferecer data/hora atual em campo do tipo
`DATE`, ou sob outro nome que não "Custom Value"), ou esses 17 nós estão
errados. **Confira na tela antes de montar a seção 2.3:** abra
`Update Contact Field` → campo `Entrada em` → veja se o seletor de valor
oferece algo como "Right Now"/"Current date and time".

Se não oferecer, o caminho desenhado é este, e ele não perde o que importa: o
Alerta de Speed-to-lead (seção 2.11) nunca precisou da hora exata — ele é um
relógio que espera 1h e pergunta se `1ª tentativa em` continua vazio. Então
`1ª tentativa em` e `Entrada em` viram **marca**, não carimbo: grave um valor
fixo (`sim`) em vez de data/hora, e a hora exata fica onde o GHL já carimba de
graça — a criação da tarefa e da nota. Perde-se o "quantos minutos", mantém-se
o "furou 1h ou não", que é a pergunta que a operação responde. Os nomes dos
campos continuam valendo; só o que se escreve neles muda.

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Buscar oportunidade | Find opportunity | Pipeline: `FUNIL DE VENDAS` · "Most recently created opportunity" → ramo **Opportunity Not Found**: encerra (vazio) · ramo **Opportunity Found**: segue |
| 2 | Portão de etapa e status | If/Else | `Pipeline stage` é `[FUNIL DE VENDAS] - CONECTAR` **E** `status` da oportunidade **não é** `lost` → ramo verdadeiro (Branch): segue · ramo falso (None): **encerra** (quem já saiu de cadência por etapa não precisa furar fila, e quem saiu como `lost` pediu para não ser procurado ou tem telefone errado — ver nota abaixo sobre o `abandoned`) |
| 3 | Portão de silêncio | If/Else | Tags inclui `nao-perturbe` → ramo verdadeiro (Branch): **encerra** · ramo falso (None): segue |
| 3c | Portão de frequência (F-04) | If/Else | `Toques na semana` **≥** 6 → ramo verdadeiro: pula direto para o nó 9 · ramo falso: segue para o nó 4 |
| 4 | Prioridade | Update Contact Field | `Prioridade` = 5 |
| 5 | Registro do sinal | Update Contact Field | `Sinal recebido` = `Clique em link` |
| 6 | Fila | Add Contact Tag | `fila-quente` |
| 7 | Tarefa | Add Task | Título: `[CADENCIA] Sinal: clicou no link — ligar agora` · Vence: agora · Atribuir: `Contact Owner` (dinâmico, R-10 — o sinal fura a fila, mas continua com o mesmo dono do lead) → Depois: Add Contact Tag `toque` (F-04, seção 2.19) |
| 8 | Aviso | Internal Notification | Para o SDR: `{{contact.first_name}} clicou no link de agendar agora. Prioridade 5.` |
| 9 | Registro | Add Note | `Sinal: clique em link` — se veio do nó 3c (teto batido), o texto muda para `Sinal: clique em link (teto de toques da semana batido — sem tarefa nova, ver Toques na semana)`, para o SDR entender pela nota por que não apareceu tarefa |

**Por que o nó 2 olha `status`, e por que `abandoned` continua passando
(19/09/2026):** o portão original só olhava a etapa, e no modelo real de 5
etapas isso deixa passar todo mundo que saiu de cadência sem sair de
`CONECTAR` (tabela 1.0) — inclusive quem foi marcado `Não ligar` ou
`Número errado`, que viram `status = lost`. Um clique no link de um lead
desses geraria tarefa `ligar agora` e aviso interno para alguém que a
operação já se comprometeu a não procurar; daí o `não é lost`.

`abandoned` **passa de propósito** — não é esquecimento: é o lead que
esgotou as 12 tentativas e está em nutrição, e um clique no link de agendar
é exatamente o sinal que o Reengajamento 90 dias (seção 2.12) não consegue
enxergar, porque ele é um relógio de 90 dias, não um sensor. Interceptar
aqui é a única forma nativa de o SDR saber que a nutrição esquentou no dia
em que esquentou. **Decisão do dono se quiser o contrário:** trocar
`não é lost` por `é open` faz o clique de um lead em nutrição virar só a
nota do nó 9, sem tarefa nem aviso.

**Por que o teto (nó 3c) pula para a nota e não encerra puro, F-04:** um sinal
que não vira tarefa ainda é informação — perdê-lo silenciosamente seria pior
que não ter o teto. Só a tarefa nova e o aviso empurrando a fila é que
custam caro quando empilham sem limite; a nota é barata e fica no histórico
do contato para o SDR ver na próxima ligação já agendada por outro toque.
**É este workflow, não a Cadência 12x30, que motivou o F-04 nesta rodada:**
com `Allow Re-entry` ligado de propósito ("cada clique é um sinal novo"), um
lead que clica o link várias vezes no mesmo dia — ou responde fora de hora
mais de uma vez — cria uma tarefa `[CADENCIA]... ligar agora` **e** um aviso
interno a cada vez, sem limite nenhum antes deste item. A Cadência 12x30
sozinha dificilmente chega perto do teto (pico real é 4 toques em D1+D2,
seção 2.5); é a soma com a Interceptação de Sinal — que roda em paralelo, sem
saber quantos toques a cadência principal já gastou naquela semana — que
gera o "dobro de toques" que o roadmap descrevia de forma mais genérica.

### 2.9.3 Workflow "Interceptação de Sinal — Resposta"

Idêntico ao 2.9.2, trocando o gatilho, o filtro do gatilho e os dois textos
marcados.

**Gatilho:** `Customer Replied` — Canal: **WhatsApp**. Decisão ao vivo do
dono, 19/09/2026: SMS nunca foi canal real da cadência (só telefone, ligação
por WhatsApp e mensagem de WhatsApp — `briefing-sdr.md`), e o dono confirmou
que não usa SMS em nenhum canal de contato com lead. O plano original media
"WhatsApp e SMS" errado, como se fossem os dois canais de texto — não eram.

**Filtro do gatilho, acrescentado em 21/09/2026 (R-17 — ver 2.9.5):** uma
linha `Doesn't Contain` por frase da lista canônica do 2.9.5 — `pare de`, `pare com`, `para de mandar`, `para de me mandar`, `não quero mais mensagem`, `não quero mais contato`, `não quero receber mensagem`, `não quero receber mais`, `remove meu contato`, `tira meu número`, `descadastr`, `cancelar inscri`, `não me liga mais`, `não me mande mais`, `sai da lista`, `me tira da lista`, `unsubscribe` —, combinadas em E (a lista
nasceu com `pare`, `não quero mais`, `não quero receber` e `stop` soltos;
saíram no mesmo dia porque `Contains` casa pedaço de palavra e "parece
ótimo" carregava `pare` — o raciocínio completo está no 2.9.5, e **as duas
listas têm que continuar idênticas**), combinadas em E — pesquisado
nesta rodada (`Customer Replied Trigger: Improved Message Filters`, changelog
oficial da HighLevel): o gatilho aceita filtro por corpo da mensagem com os
operadores `Contains`/`Doesn't Contain`/`Exact Match`, além de canal, tag e
tipo de intenção. **Sem este filtro, uma resposta de opt-out dispara os dois
workflows ao mesmo tempo** — este (que grita "ligar agora, prioridade 5") e o
2.9.5 (que aplica DND) — e o SDR vê uma tarefa mandando ligar para quem
acabou de pedir silêncio.

Mesma tabela de nós da 2.9.2 (incluindo o nó 1 `Find opportunity`, que este
gatilho também precisa — `Customer Replied` também não carrega oportunidade
no contexto sozinho), com estas trocas:
- Nó 5: `Sinal recebido` = `Resposta de mensagem`
- Nó 7: Título da tarefa `[CADENCIA] Sinal: respondeu mensagem — ligar agora` ·
  Descrição: `Lead respondeu mensagem fora do fluxo normal da cadência. Ligar
  imediatamente, prioridade 5.`
- Nó 8: `{{contact.first_name}} respondeu agora fora do fluxo normal.
  Prioridade 5.`
- Nó 9: `Sinal: resposta de mensagem` (a 2.9.2 usava "Sinal: clique em link" —
  esquecido na primeira versão desta lista de trocas, corrigido em 19/09/2026
  montando na tela)

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

### 2.9.5 Workflow "Opt-out por Palavra-chave" — R-17

**Achado desta rodada, lendo o 2.9.3 com atenção ao invés de só migrar nome
de etapa:** o gatilho `Customer Replied` do 2.9.3 não olha o **conteúdo** da
resposta — só que o canal é WhatsApp. Um lead que responde "pare, não me
manda mais mensagem" cai no mesmo lugar que um lead que responde "sim, tenho
interesse": `Prioridade` = 5, tag `fila-quente`, tarefa `[CADENCIA] Sinal:
respondeu mensagem — ligar agora`. A operação inteira existe para não tratar
pedido de silêncio como oportunidade — e este workflow, sozinho, fazia
exatamente isso, sem que nenhum item do roadmap tivesse notado. Diferença
para o ramo `Não ligar` do Pós-ligação (seção 4, o nó que este documento já
trata como "não-negociável"): aquele só dispara depois que o SDR classifica
uma **ligação de telefone**. Uma resposta de **texto** nunca passa por lá —
não existe ligação para classificar. Sem este item, o único jeito de um
opt-out por WhatsApp virar DND é o SDR ler a mensagem sozinho e lembrar de ir
até o contato desligar tudo na mão, depois de já ter recebido (por causa do
2.9.3) uma tarefa dizendo o oposto: "ligar agora".

**Pesquisado antes de desenhar:** Reev, Meetime, Outreach e Salesloft tratam
opt-out como estado de contato/lista (unsubscribe, "não contatar"), não como
uma régua por palavra — porque o canal principal deles é e-mail, com
cabeçalho de unsubscribe padronizado, e SMS nos EUA já tem "STOP" reservado
por lei (TCPA) e filtrado pela operadora antes de chegar à plataforma. Nenhum
dos quatro documenta detecção de palavra-chave em **WhatsApp** — não existe
"STOP" reservado nesse canal, e a LGPD não define uma palavra obrigatória
como o TCPA define. A lacuna que este item fecha não tem receita pronta para
copiar: o próprio "Como" abaixo (gatilho global por frase + filtro de
exclusão espelhado no vizinho, 2.9.3) é montado a partir de duas peças
nativas do GHL que nenhuma das quatro plataformas citadas precisa combinar,
porque nenhuma delas roda cadência de **ligação por WhatsApp** — só mensagem.

**Como:**

**Gatilho:** `Customer Replied` — Canal: **WhatsApp** — `Contains Phrase`,
esta lista (**a lista canônica do projeto — o filtro do 2.9.3 tem que ser
idêntica a ela, palavra por palavra**):

`pare de`, `pare com`, `para de mandar`, `para de me mandar`, `não quero mais mensagem`, `não quero mais contato`, `não quero receber mensagem`, `não quero receber mais`, `remove meu contato`, `tira meu número`, `descadastr`, `cancelar inscri`, `não me liga mais`, `não me mande mais`, `sai da lista`, `me tira da lista`, `unsubscribe`

(**Confirme na tela** se o campo aceita a lista inteira numa linha só,
combinada em OU — se não aceitar, o mesmo efeito sai com uma linha de filtro
por frase, todas apontando para este workflow, o mesmo padrão de "vários
gatilhos, um efeito" que a seção 2.9 já usa entre 2.9.2 e 2.9.3.)

**Por que `pare` sozinho saiu da lista, e por que isso não é preciosismo
(conferido em 21/09/2026):** `Contains` casa **pedaço de palavra**, não
palavra inteira. `pare` está dentro de *parece*, *aparelho*, *comparecer*,
*preparei*, *separado*, *transparente*, *reparei*. A resposta mais positiva
que um lead brasileiro manda — **"parece ótimo, me liga"** — contém `pare`.
Com a lista antiga, essa resposta produzia, de uma vez: DND em todos os
canais, tag `nao-perturbe`, saída de todas as réguas, `status = lost` na
oportunidade **e** (pelo filtro espelhado do 2.9.3) nenhuma tarefa de sinal
quente. O lead mais quente do dia viraria o lead mais morto do CRM, em
silêncio — ninguém recebe alerta de DND aplicado, e nenhuma automação
desfaz DND.

O mesmo cuidado tirou `não quero mais` e `não quero receber` soltos: neste
negócio o lead descreve a dor com exatamente essas palavras ("**não quero
mais** perder cliente", "**não quero receber** lead ruim"). Ficaram só com o
complemento que fecha o sentido (`mensagem`, `contato`, `mais`). E `stop`
saiu: em WhatsApp brasileiro ele não é palavra reservada como o TCPA faz no
SMS americano, então só traria falso positivo de texto em inglês sem
compensar nada.

**Regra de manutenção:** esta lista e a do filtro do 2.9.3 são **a mesma
lista**. Mexer numa sem mexer na outra reabre exatamente o bug que o 2.9.5
existe para fechar (os dois workflows disparando na mesma mensagem) ou o
inverso (opt-out que não silencia). Antes de mudar qualquer palavra, teste-a
contra a pergunta: *ela aparece dentro de alguma palavra comum do
português?* Se sim, use a frase, nunca o pedaço.

| Configuração | Valor |
|---|---|
| Janela de envio | Sem restrição, 24/7 — mesmo motivo do 2.9.2: nenhum nó manda mensagem para o lead, e DND atrasado por causa de janela de expediente é o oposto do que este item existe para evitar |
| Allow Re-entry | Ligado — uma segunda mensagem de opt-out do mesmo lead não pode ser ignorada só porque a primeira já rodou; todas as ações abaixo são idempotentes |
| Stop on Response | Desligado |

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Buscar oportunidade | Find opportunity | Pipeline: `FUNIL DE VENDAS` · "Most recently created opportunity" — mesmo motivo do 2.9.2/2.9.3: `Customer Replied` não carrega oportunidade no contexto sozinho. Ramo **Opportunity Not Found**: segue mesmo assim para o nó 2 (DND é do contato, não da oportunidade — não pode depender de achar uma) |
| 2 | Silêncio | Add Contact Tag | `nao-perturbe` |
| 3 | DND | **Set Contact DND** = ligado, todos os canais | Mesmo nó que a seção 4 (ramo `Não ligar`) já trata como não-negociável deste documento inteiro — aqui pela primeira vez, disparado por texto em vez de classificação do SDR |
| 4 | Sair das filas | Remove Contact Tag | `fila-tel`, `fila-wa`, `fila-quente` |
| 5 | Sair das réguas | **Remove Workflows** | Opção **All Except Current Workflow** (F-05, achado de 21/09/2026, nota na seção 3 — substitui a lista antiga de seis nomes, que já era a mais longa do documento e ainda assim precisava ser mantida igual às outras duas na mão). Continua sendo o único ponto de saída do documento que não depende de esperar a oportunidade mudar de `status` primeiro (nó 6 abaixo é condicional; isto não pode ser) |
| 6 | Fechar o negócio, com cautela | If/Else | Achou oportunidade no nó 1 **E** etapa é `CONECTAR` **E** `status` é `open` → Update Opportunity `status` = `lost` (aciona o Mestre de saída pelo gatilho de status, seção 3 — redundante com o nó 5 acima, inofensivo, mesmo raciocínio já usado na seção 3). Senão → Internal Notification para `Contact Owner`: `Opt-out por palavra-chave: {{contact.name}} pediu para parar, oportunidade já em {{opportunity.pipeline_stage}}/{{opportunity.status}} — DND ligado, revisar se o negócio segue antes de qualquer novo contato` |
| 6b | **Aviso, sempre** | Internal Notification | Para `Contact Owner`: `Opt-out por palavra-chave: {{contact.name}} — DND ligado e saiu de todas as réguas. Mensagem que disparou: revisar no histórico. Se foi falso positivo, desligar o DND na mão é a única volta.` **Este nó roda em todos os caminhos**, inclusive quando o nó 6 fechou a oportunidade — ver nota abaixo |
| 7 | Registro | Add Note | `Opt-out por palavra-chave detectado em {{right_now}} · DND ligado · removido de todas as réguas automáticas` |

**Por que o nó 6b avisa sempre, e não só no ramo "senão" do nó 6
(acrescentado em 21/09/2026):** na versão original, o único caminho que
gerava aviso era o do lead que **não** estava em `CONECTAR`/`open` — ou
seja, o caso raro. O caso comum (lead em cadência responde, vira DND e
`lost`) produzia apenas uma nota no histórico do contato, que ninguém abre
sem motivo. Isso deixava o falso positivo da lista de palavras **invisível**:
nenhuma automação desfaz DND, nenhuma lista mostra "DND aplicado hoje", e o
lead simplesmente para de aparecer. Um aviso por opt-out é barato — são
poucos por dia, por definição — e é a única chance de alguém dizer "esse aí
não pediu para sair, ele disse *parece ótimo*". Aviso que chega demais se
ignora; DND errado que não avisa ninguém não se descobre.

**Por que o nó 6 não move sozinho quem já passou de `CONECTAR`:** um lead em
`NEGOCIAR` que responde "pare" pode estar pedindo para parar de receber
mensagem automática, não cancelando a negociação em andamento com o closer —
os dois são pedidos diferentes, e só um humano sabe qual é. O DND (nó 3) e a
saída de todas as réguas automáticas (nó 5) valem para os dois casos sem
ambiguidade; mudar o `status` da oportunidade sozinho, não.

**Por que este workflow não depende do 2.9.3 nem o substitui:** os dois
escutam o mesmo evento (`Customer Replied`, WhatsApp) e por isso precisam do
filtro cruzado descrito no 2.9.3 acima — sem ele, uma resposta de opt-out
dispararia os dois ao mesmo tempo, e o SDR veria "ligar agora, prioridade 5"
e "DND ligado" na mesma tela. Com o filtro, são mutuamente exclusivos: toda
resposta de WhatsApp cai num dos dois, nunca nos dois.

**Limite conhecido, documentado em vez de escondido:** este workflow protege
contra a resposta de opt-out virar sinal quente (2.9.3) e contra a cadência
principal continuar tentando (Stop on Response da seção 2.2 já resolvia
isso, mas sem DND nem limpeza das outras réguas). Não protege contra uma
mensagem que **já estava saindo no mesmo instante** por outro workflow em
execução (ex.: a próxima pergunta da corrente de nós do Caminho B, seção 6,
que não checa o conteúdo da resposta antes de mandar a pergunta seguinte) —
é uma janela de corrida entre dois workflows assíncronos, não um bug deste
item. O Caminho A (Conversation AI, seção 6) já tem uma instrução de prompt
("pare imediatamente... não faça mais perguntas") que cobre a mesma janela
por outro caminho; o Caminho B não tem nada equivalente hoje — fica
registrado como lacuna nova, pequena e sem cadência de mensagem alta o
bastante ainda para valer uma rodada própria.

**Zero campo e zero tag novos:** reaproveita `nao-perturbe` (T-06) e o DND
nativo, ambos já existentes desde a Etapa 3. Falta só a criação manual do
workflow e do filtro cruzado no 2.9.3 — nenhum dos dois sai por API.

**Pronto quando:** um lead que responde "pare" (ou qualquer frase da lista)
no WhatsApp sai de toda cadência automática e fica com DND ligado no mesmo
minuto — nunca mais chega a gerar a tarefa "ligar agora" que o 2.9.3
geraria antes deste item.

---

## 2.10 Workflow "Cadência Inbound" — R-07 — migrado para as 5 etapas reais em 19/09/2026

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

**Opportunity Stage Changed** — Pipeline `FUNIL DE VENDAS` (é o mesmo objeto
que este documento chama de `Pré-vendas` — seção 1) · Para a etapa:
`CONECTAR` · Filtro adicional: tag `cad-inbound` **presente**

Espelha o gatilho da Cadência 12x30 (seção 2.1) com o filtro de tag
invertido. Os dois disparam do mesmo evento; o filtro decide qual dos dois
processa aquele lead — não há nó de portão fazendo essa escolha dentro do
fluxo.

**Por que este gatilho não precisa do filtro `reengajamento-ativo` do R-08
(seção 2.1 precisa, este não):** o nó 4 do Reengajamento 90 dias (seção
2.12) remove `cad-inbound` **antes** de mover a etapa para `CONECTAR` —
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

Espelha 2.3, com duas diferenças próprias (linhas 0.5 e 0.7), o mesmo par
de distribuição de leads que 2.3 ganhou no R-10 (0.7/0.7b lá, 0.8/0.8b
aqui — numeração diferente só porque cada bloco já tinha nós até um número
distinto antes dele entrar) e o mesmo portão de higiene de telefone do R-13
(0.0/0.0b, idêntico ao de 2.3 — um formulário sem campo de telefone
obrigatório é a fonte mais provável deste caso aqui, não menos provável que
no outbound):

| Nó | Ação | Configuração |
|---|---|---|
| 0.0 | If/Else (R-13) | Campo nativo `Phone` **está vazio** → ramo 0.0b. Senão → segue para 0.1 |
| 0.0b | Ramo sem telefone | Add Contact Tag `telefone-invalido` → If/Else: `Site` **ou** `Instagram` preenchido → Update Opportunity `status` = `abandoned` + Add Contact Tag `nutricao-90d`. Senão → Update Opportunity `status` = `lost` → Internal Notification para o gestor: `Lead inbound sem telefone: {{contact.name}} — revisar o formulário de origem` → **Remove from Workflow: este** |
| 0.1 | Update Contact Field | `Tentativa nº` = 0 |
| 0.2 | Update Contact Field | `WA não atendidas seguidas` = 0 |
| 0.3 | Update Contact Field | `Resultado da tentativa` = vazio |
| 0.4 | If/Else | `Permissão WhatsApp` está vazio → Update: `Não solicitado` |
| 0.5 | Update Contact Field | `Prioridade` = 5 (não 3: todo lead inbound nasce no topo da fila — é a resposta rápida que a régua de degraus só cumpre se o SDR também priorizar certo) |
| 0.6 | Update Contact Field | `Entrada em` = `{{right_now}}` (mesmo campo do R-02 — a métrica de speed-to-lead nasceu para o outbound e serve de graça aqui, sem custo nenhum) |
| 0.7 | Add Contact Tag | `fila-quente` (assim o lead aparece na lista `Fila Quente`, 8.1, sem lista nova) |
| 0.8 | If/Else (R-10) | campo nativo `Assigned User` está vazio → segue para 0.8b. Senão → pula 0.8b |
| 0.8b | Assign to User → modo `Round Robin` | Mesma lista de SDRs do nó 0.7b da Cadência 12x30 (seção 2.3) — um único grupo de round robin para toda a operação, não um por cadência, senão o mesmo SDR poderia ganhar dois leads simultâneos por entrar em réguas diferentes na mesma rodada da roleta |

### MI-0 — mensagem automática imediata

Antes da T1, sem esperar nada: **Guarda de janela de atendimento (seção
2.6.2, G-05)** → dentro da janela, Send WhatsApp texto livre `MI-0`
(`biblioteca-mensagens.md`) · fora da janela (o caso de praticamente todo
lead, que nunca escreveu no WhatsApp da subconta antes), Send WhatsApp modo
**Template** `MI-0` (a submeter — `biblioteca-mensagens.md`) — confirmando o
recebimento e avisando que a ligação vem em minutos — o equivalente ao
"notificar o SDR independente de onde ele esteja" que o Meetime documenta,
só que do lado do lead: ele sabe que foi ouvido antes mesmo do telefone
tocar. Os dois ramos convergem no mesmo Update `Template usado` = `MI-0`.

### O bloco padrão de uma tentativa inbound (mirror de 2.4, com espera relativa)

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Aguardar | Wait → Time Delay | Delta da tabela abaixo, relativo ao fim do bloco anterior (não horário fixo) |
| 1.5 | Pausa individual (R-09) | If/Else | tag `pausado` presente → ramo 1.5b. Senão → segue para o Portão (nó 2) |
| 1.5b | Ramo da pausa individual | Wait → Time Delay 30 min → **volta para o nó 1.5** | Mesmo mecanismo do nó 2.5 da 12x30 (seção 2.4), com relógio de 30 min em vez de 1 dia — a régua inbound é medida em minutos, e um retry diário aqui devolveria o lead numa velocidade que já não é mais inbound de verdade |
| 2 | Portão | If/Else — condições **E** | Etapa da oportunidade **é** `CONECTAR` · `status` da oportunidade **é** `open` · tag `nao-perturbe` **não** presente · `Resultado da tentativa` **não é** `Não ligar` · (só em tentativa de telefone) tag `telefone-invalido` **não** presente |
| 2b | Ramo falso do portão | Remove Contact Tag `fila-tel`, `fila-wa`, `fila-quente` → Add Contact Tag `limpar-tarefas` → **Remove from Workflow: este** | Mesma saída limpa do nó 3b da 12x30 |
| 3 | Seletor de canal | If/Else (só nas tentativas de WhatsApp) | Ramo WA: `Permissão WhatsApp` **é** `Sim` **E** `WA não atendidas seguidas` **<** 2. Senão → telefone |
| 4 | Limpar resultado | Update Contact Field | `Resultado da tentativa` = vazio · `Tentativa nº` = `{n}` |
| 5 | Fila | Add Contact Tag | `fila-tel` ou `fila-wa` |
| 6 | Tarefa | Add Task | Título: `[CADENCIA] TI{n} · Ligar (canal) — Inbound` · Vence: agora · Atribuir: `Contact Owner` (dinâmico, R-10) |
| 7 | Aviso | Internal Notification | Para o SDR: `Lead inbound {{contact.name}} aguardando retorno — TI{n}.` Diferencial sobre o bloco padrão outbound (2.4): lá a fila espera ser vista; aqui o SDR é avisado na hora, o mesmo padrão do F-01 (seção 2.9) e do que o Meetime chama de notificação "independente de onde o SDR esteja" |
| 8 | Aguardar resultado | Wait → Condition, tempo limite | Condição: `Resultado da tentativa` **não está vazio**. Tempo limite: o delta até a tentativa seguinte da tabela abaixo — não 18:30 fixo, porque numa régua de minutos "esperar até o fim do dia" descaracterizaria a velocidade |
| 9 | Remover tag de fila | Remove Contact Tag | `fila-tel` e `fila-wa` |
| 10 | Condição por resultado | If/Else | `Atendeu` ou `Pediu retorno` → **Remove from Workflow: este** (o Pós-ligação, seção 4, cuida do resto — é canal-agnóstico, já reaproveitado sem alteração) · `Número errado`, `Não ligar` ou `Desqualificado` (R-18) → **Remove from Workflow: este** · qualquer outro / tempo limite → próxima tentativa (ou handoff, na TI5) |
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
| 0 | Guarda de janela de atendimento (seção 2.6.2, G-05) | Dentro da janela → 1 · Fora da janela → 1T |
| 1 | Send WhatsApp | Texto livre `MI-F`, `biblioteca-mensagens.md` — avisa que a tentativa continua, agora na régua normal → 2 |
| 1T | Send WhatsApp, modo Template | Template Meta `MI-F` (a submeter — `biblioteca-mensagens.md`) → 2 |
| 2 | Update Contact Field | `Template usado` = `MI-F` (os dois ramos acima convergem aqui) |
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
depois da entrada em `CONECTAR`, dentro da janela de expediente.

---

## 2.11 Alerta de Speed-to-lead — R-02 — migrado para as 5 etapas reais em 19/09/2026

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
**Opportunity Stage Changed** — Pipeline `FUNIL DE VENDAS` (é o mesmo objeto
que este documento chama de `Pré-vendas` — seção 1) · Para a etapa:
`CONECTAR` (o mesmo gatilho da Cadência 12x30, seção 2.1 — os dois disparam
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
| 2 | Portão | If/Else | Etapa da oportunidade **é** `CONECTAR` **E** `status` **é** `open` **E** `1ª tentativa em` está vazio **E** tag `pausado` **ausente** (R-09) → segue. Senão → **encerra** (T1 já rodou, o lead já saiu de cadência — por movimento de etapa ou por `status`, ver nota abaixo —, ou está pausado de propósito — nenhum dos três é atraso) |
| 3 | Fila | Add Contact Tag | `atraso-1a-tentativa` |
| 4 | Aviso | Internal Notification | Para o gestor: `{{contact.name}} está há mais de 1h em cadência sem a 1ª tentativa. Entrada: {{contact.entrada_em}}.` |
| 5 | Registro | Add Note | `Alerta speed-to-lead: sem 1ª tentativa 1h após a entrada · {{right_now}}` |

A limpeza é dupla, de propósito: o nó 5d da T1 (seção 2.4) remove a tag no
caminho feliz (T1 rodou dentro da hora), e o nó 4 do Mestre de saída (seção 3)
remove no caminho de saída (lead saiu de cadência antes de qualquer um dos
dois — por movimento de etapa, como `Atendeu`, ou só por `status`, como
`Número errado`/`Não ligar`/12 tentativas esgotadas). Tag presa custa uma
lista suja; os dois pontos de remoção custam duas linhas.

**Pronto quando (herdado do R-02 no roadmap):** existe lista "leads com mais
de 1h sem primeira tentativa" — é a 8.8, filtrando `atraso-1a-tentativa`.

**Por que o nó 2 ganhou `status é open`, não só `etapa é CONECTAR` (achado
desta migração):** no plano de 7 etapas, todo jeito de sair de cadência
movia a oportunidade para fora de `Em cadência` — checar só a etapa bastava.
No modelo real de 5 etapas, o portão de higiene do nó 0.0b (seção 2.3) pode
descartar um lead sem telefone (`status = abandoned`/`lost`) **sem tirá-lo de
`CONECTAR`**, e isso acontece antes de qualquer tentativa rodar — exatamente
a janela que este alerta observa. Sem o `status é open`, um lead assim
dispararia um alarme de speed-to-lead falso: ele já saiu de cadência (nunca
vai receber a T1), mas a condição "etapa é `CONECTAR` e `1ª tentativa em`
vazio" continuaria verdadeira, e o nó 3 aplicaria `atraso-1a-tentativa` num
lead que não está atrasado, só descartado. Mesma classe de bug que a seção 3
(Mestre de saída) e a seção 2.12 (reentrada do Reengajamento) já documentaram
para este modelo — checar só a etapa não basta onde saída e status andam
separados.

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
futura em "CONECTAR" — inclusive um erro de clique do SDR — passaria a
duplicar tentativas para leads que nunca deveriam repetir a régua. Um
workflow próprio, pequeno, com seu próprio `Allow Re-entry` **ligado** de
propósito (só ele, isolado), resolve sem tocar no D-06. É o mesmo
raciocínio que já separou a Cadência Inbound (seção 2.10) da 12x30: dois
workflows curtos, cada um com a configuração que sua régua pede, batem um
workflow só com `if` decidindo por dentro qual configuração vale.

### Gatilho — migrado para as 5 etapas reais em 19/09/2026

**Contact Tag Added** — tag: `nutricao-90d`. O gatilho original
(`Opportunity Stage Changed` → `Nutrição`) não existe mais: `Nutrição`
deixou de ser etapa própria na tela real de 5 etapas, virou
`status = abandoned` da oportunidade, com a etapa permanecendo onde estava
(tabela 1.0, seção 1). A tradução já estava anotada lá desde a migração da
seção 2.1 — "todo gatilho `Opportunity Stage Changed → Nutrição` vira
`Contact Tag Added → nutricao-90d`" —, só não tinha sido aplicada aqui
ainda.

### Configurações

| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | Ao contrário da 12x30 (D-06), aqui *toda* aplicação da tag `nutricao-90d` é uma rodada legítima e nova — o mesmo raciocínio já usado no Alerta de Speed-to-lead (seção 2.11): "uma rodada 2 manual é uma nova entrada de verdade e merece seu próprio relógio". Sem isso, o lead reativaria uma vez e nunca mais — o "por quê" deste item ("nutrição sem retorno é arquivo morto") voltaria a valer na segunda rodada |
| Janela de envio | 08:30 às 18:30, segunda a sexta, fuso da subconta | Mesma janela da 12x30 — reativação não é urgência, é rotina |
| Stop on Response | Ligado | Respondeu em qualquer canal, sai da régua de reativação |

### Nós

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Aguardar | Wait → Time Delay | 90 dias corridos |
| 2 | Portão | If/Else — condições **E** | Status da oportunidade **é** `abandoned` · tag `nutricao-90d` presente · tag `nao-perturbe` ausente |
| 2b | Ramo falso do portão | **Remove from Workflow: este** | O lead já saiu do estado de nutrição por outro caminho (voltou a `CONECTAR` na mão e converteu — `status` deixou de ser `abandoned` —, ou foi descartado, `status = lost`) ou pediu para não ser mais procurado — não reativa quem já mudou de estado por conta própria. Nada para limpar aqui: nenhuma tag de fila foi tocada ainda |
| 3 | Reset de rodada | Update Contact Field | `Tentativa nº` = 0 · `WA não atendidas seguidas` = 0 · `Resultado da tentativa` = vazio · `Prioridade` = 3 · `Entrada em` = `{{right_now}}` · `1ª tentativa em` = vazio |
| 4 | Troca de origem | Remove Contact Tag `nutricao-90d` → Remove Contact Tag `cad-inbound` (idempotente, mesmo se ausente) → Add Contact Tag `cad-outbound` → Add Contact Tag `reengajamento-ativo` | Ver "A troca de origem" abaixo |
| 5 | Reentrada no funil | Update Opportunity — Etapa → `CONECTAR` **e** `status` → `open` | O reset explícito de `status` é achado desta migração: o desenho original não tinha campo `status` separado de etapa, então "mover para `Em cadência`" bastava. Hoje, sem zerar `status`, o lead chegaria a `CONECTAR` ainda com `status = abandoned` da rodada anterior, e o portão do Mestre de saída (seção 3, nó 1: "`CONECTAR` **e** `open`") ficaria falso — a chegada seria lida como saída, e a limpeza (tirar das filas, apagar tag de fila) rodaria no instante em que o lead está *entrando* de novo na cadência, não saindo. Com o reset, dispara o Mestre de saída em no-op de verdade (nó 1 encerra sem limpar) e o Alerta de Speed-to-lead (seção 2.11) com relógio novo, porque `1ª tentativa em` acabou de ser esvaziado no nó 3 — a reativação ganha sua própria medição de speed-to-lead de graça, sem campo novo |
| 6 | Guarda de janela de atendimento (seção 2.6.2, G-05) | If/Else nativo | Dentro da janela → 6b · Fora da janela → 6c |
| 6b | Mensagem de reabertura | Send WhatsApp | Texto livre `RE-1` (`biblioteca-mensagens.md`) → 6d |
| 6c | Mensagem de reabertura (fora da janela) | Send WhatsApp, modo Template | Template Meta `RE-1` (a submeter — `biblioteca-mensagens.md`) → 6d |
| 6d | Carimbo | Update Contact Field | `Template usado` = `RE-1` (os dois ramos acima convergem aqui) |
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
`AGENDAR` ou mudando `status` para `abandoned`/`lost` sem sair de
`CONECTAR` (tabela 1.0). `reengajamento-ativo` sai sozinho nesse caminho: é
o Mestre de saída (seção 3, nó 4) que limpa, porque qualquer um desses
resultados tira a oportunidade da condição `CONECTAR` **e** `open`.

### Sem resposta ao fim da TR4

Se a TR4 chega ao nó 10 do bloco padrão pelo ramo "tempo limite" (as 4
tentativas esgotaram sem conexão), em vez de "próxima tentativa":

| # | Ação | Configuração |
|---|---|---|
| 0 | Guarda de janela de atendimento (seção 2.6.2, G-05) | Dentro da janela → 1 · Fora da janela → 1T |
| 1 | Send WhatsApp | Texto livre `RE-2` (`biblioteca-mensagens.md`) → 2 |
| 1T | Send WhatsApp, modo Template | Template Meta `RE-2` (a submeter — `biblioteca-mensagens.md`) → 2 |
| 2 | Update Contact Field | `Template usado` = `RE-2` (os dois ramos acima convergem aqui) |
| 3 | Update Contact Field | `Resultado da tentativa` = vazio |
| 4 | Add Contact Tag | `nutricao-90d` |
| 5 | Update Opportunity | `status` = `abandoned` (etapa fica onde estava, `CONECTAR` — tabela 1.0; não é mais "mover para `Nutrição`", que não existe como etapa) |

O nó 4 é quem fecha o círculo agora: como o gatilho deste workflow é
`Contact Tag Added → nutricao-90d` (migrado nesta rodada), aplicar a tag de
novo dispara este mesmo workflow do zero, porque `Allow Re-entry` está
ligado — outro relógio de 90 dias começa a contar sozinho. O nó 5 cuida da
outra metade: `status = abandoned` tira a oportunidade da condição
`CONECTAR` **e** `open`, o que aciona o Mestre de saída (que limpa
`reengajamento-ativo`, entre outras). É a régua que se repete para sempre
até o lead conectar, pedir para não ser mais procurado, ou virar
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
`Novo lead`" — nome do plano original de 7 etapas, que na tela real virou
`NOVO LEAD` (tabela 1.0: mesma etapa, só o nome mudou). O espírito — o lead
sai do arquivo morto e reaparece na fila do SDR — está mantido; o destino
técnico mudou para `CONECTAR` diretamente, por dois motivos concretos, não
por preferência:

1. Não existe, em nenhum lugar deste documento, um gatilho que promova
   `NOVO LEAD` → `CONECTAR` automaticamente (é uma lacuna que já
   existia antes deste item — hoje essa transição é manual, decisão do
   SDR ao revisar a fila). Se este workflow parasse em `NOVO LEAD`, o
   lead reativado ficaria parado ali para sempre, o oposto do "Pronto
   quando" deste item ("o lead... volta à fila... sozinho").
2. Passar por `NOVO LEAD` de propósito, mesmo que por um instante,
   aciona o Mestre de saída (seção 3, gatilho 1, "qualquer etapa de
   destino") nesse destino intermediário — ele rodaria a limpeza inteira
   (incluindo aplicar `limpar-tarefas` e gravar a nota "Saída de cadência"
   num contato que não estava, de fato, saindo de cadência nenhuma) antes
   mesmo de a tarefa `TR1` existir. É ruído no histórico do contato e um
   risco de corrida real, ainda que pequeno, com a rotina horária de
   manutenção (`rotina-limpar-tarefas.md`), que lê `limpar-tarefas` a
   cada hora.

Registrar como lacuna nova para uma rodada futura: **L-07 — promoção
automática de `NOVO LEAD` → `CONECTAR`**. Hoje isso é decisão do SDR ao
revisar a fila; se o volume crescer, vale um gatilho (por exemplo,
`Contact Tag Added` numa tag de "telefone validado") que faça essa
promoção sozinha — o mesmo buraco que este item contornou indo direto
para `CONECTAR` afeta igualmente todo lead novo, não só o reativado.

### Nova tag — T-13

`reengajamento-ativo`, especificada em `campos-e-tags.md`. Seguiu o mesmo
caminho de `atraso-1a-tentativa` (T-12, R-02): nasceu fora do lote das 11
tags já aprovadas por nome em `APROVADO.md`, com linha própria — aprovada
ao vivo em chat e **criada em 18/09/2026** via `contacts_add-tags`.

**Pronto quando (do roadmap):** o lead de hoje volta à fila em dezembro,
sozinho — a tarefa `[CADENCIA] TR1` nasce e o lead aparece nas listas
`Fila Telefone Hoje`/`Fila WhatsApp Hoje` (seções 8.2/8.3, que já filtram
por etapa `CONECTAR` + tag de fila, sem precisar de lista nova) 90 dias
depois da tag `nutricao-90d` ser aplicada, sem qualquer ação humana entre
as duas datas.

---

## 2.13 Regras de pausa — R-09 — conferida para as 5 etapas reais em 19/09/2026, um retoque

`nao-perturbe` já resolve "este lead nunca mais" e a etapa `CONECTAR`
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
`atraso-1a-tentativa` (T-12) e `reengajamento-ativo` (T-13): nasceu fora do
lote das 11 tags já aprovadas por nome em `APROVADO.md`, com linha própria
— aprovada ao vivo em chat e **criada em 18/09/2026** via
`contacts_add-tags`.

**Pronto quando (do roadmap):** o Natal não gera 120 tarefas — os três
workflows que tocam o lead ficam pausados pelo recurso nativo da conta
durante o intervalo cadastrado, represando qualquer tarefa/mensagem que
tentaria disparar nesses dias; e um lead específico pode ser represado sem
depender de calendário nenhum, via `pausado`, sem perder a posição na régua.

---

## 2.14 Distribuição de leads — R-10 — conferida para as 5 etapas reais em 19/09/2026, sem achado

O desenho inteiro até aqui (seções 2 a 2.13) assume um único SDR. No
segundo, sem regra, os dois abrem a mesma `Fila Telefone Hoje` (8.2) e ligam
para o mesmo lead ao mesmo tempo — pior que nenhuma distribuição, porque
parece organizado e não é.

Pesquisado antes de desenhar: o GHL tem uma ação de workflow nativa,
**Assign to User**, com quatro modos — `Contact Owner` (mantém quem já é
dono), `Selected User` (um usuário fixo), `Any User` (qualquer usuário
elegível) e `Round Robin` (roda entre os usuários escolhidos, distribuição
igual por padrão). É o mesmo mecanismo que Reev, Meetime, Outreach e
Salesloft vendem como "lead routing" — aqui sai de graça, dentro do
workflow, sem módulo adicional. **Nível de confiança:** médio-alto — veio de
busca (não de leitura direta; os domínios de suporte da HighLevel seguem
bloqueados neste ambiente, ver `APRENDIZADOS-CRM.md`), mas é o tipo de
recurso básico de automação que teria aparecido em múltiplas fontes
independentes se não existisse, e apareceu.

### A decisão que separa isto de uma cópia de tela

O roadmap pede "round robin **na atribuição da tarefa**". Segui o espírito,
não a letra: o round robin sorteia o **dono do lead**, uma vez, no primeiro
nó de inicialização que o lead encontra (0.7b na Cadência 12x30, seção 2.3;
0.8b na Cadência Inbound, seção 2.10) — não sorteia de novo a cada uma das
12 tentativas. Todo `Add Task` daqui em diante (seção 2.4 nó 7, seção 2.9.2
nó 6 — e 2.9.3, que a espelha —, seção 2.10 nó 6, seção 4 nós `[CONECTADO]`
e `[RETORNO]`) atribui a `Contact Owner`: segue o dono que o sorteio já
decidiu, em vez de rodar a roleta de novo.

Rodar a roleta por tarefa, como o texto literal do roadmap sugere, é o
desenho que um concorrente copia olhando a tela — "ativei round robin no nó
de criar tarefa" é um clique. O que não se vê de fora é a razão de **não**
fazer isso: um lead trabalhado por SDRs diferentes a cada uma das 12
tentativas em 30 dias perde o que a literatura de sales engagement chama de
continuidade de relacionamento — o SDR da T7 não sabe o que o da T3
prometeu, e o lead sente. Reev e Meetime não documentam isso como
"limitação resolvida"; documentam como prática recomendada — dono único por
lead, do início ao fim da cadência. A escolha de onde colocar o nó (uma vez,
na entrada) em vez de qual ação usar (`Round Robin`, óbvia) é o que não
aparece numa captura de tela do workflow.

### Nós novos

| Onde | Nó | Ação | Configuração |
|---|---|---|---|
| Seção 2.3, nó 0 | 0.7 / 0.7b | If/Else → Assign to User | Ver seção 2.3 |
| Seção 2.10, nó 0 | 0.8 / 0.8b | If/Else → Assign to User | Ver seção 2.10 |

O If/Else que precede cada sorteio (`Assigned User` vazio?) é o que faz a
lógica ser idempotente: a Cadência Inbound (2.10) roda seu próprio sorteio
na entrada; se o lead não responde em 3 dias, o handoff da TI5 (seção 2.10,
"Handoff ao fim da TI5") entra na Cadência 12x30 por `Add to Workflow`, que
**executa o nó 0 dela de novo** (é o mesmo mecanismo que já zera `Tentativa
nº` no handoff, documentado ali). Sem o portão 0.7, o lead sorteado para o
SDR A na entrada trocaria de dono para o SDR B só por atravessar o handoff —
o oposto de "dono único". Pelo mesmo motivo, o Reengajamento 90 dias (seção
2.12) não ganhou sorteio próprio: todo lead que chega lá já passou por 2.3
ou 2.10 antes (é assim que ele chegou a `Nutrição`), então `Assigned User`
já não está vazio — o dono da primeira rodada continua sendo o dono da
reativação, sem precisar de nó novo ali.

**Por que um grupo de round robin só, não um por cadência (nó 0.8b aponta
para a mesma lista do 0.7b):** um lead inbound e um outbound entrando na
mesma hora em cadências diferentes ainda competem pela agenda do mesmo SDR.
Duas listas de round robin independentes rodando em paralelo podem mandar
os dois leads para o mesmo SDR na mesma rodada — dois grupos sincronizados
por acidente não são round robin nenhum, são coincidência. Um grupo único,
referenciado pelos dois nós, é o que garante alternância de verdade entre
os SDRs, qualquer que seja a porta de entrada do lead.

### O que fazer se `Add Task` não tiver a opção `Contact Owner`

Não testei em subconta com mais de um usuário (a atual só tem o dono, ver
"Estado da subconta" abaixo) — é o item 28 do checklist da seção 10. Se a
tela do nó `Add Task` não oferecer `Contact Owner` como destino dinâmico do
campo "Atribuir a", o GHL costuma liberar o mesmo campo por **valor
personalizado** (ícone `{}` ao lado do seletor) — insira o merge field do
usuário atribuído do contato ali. Não crie um segundo mecanismo de round
robin no nó `Add Task` como saída alternativa: isso reabriria exatamente o
problema que a seção anterior evita (sorteio por tarefa em vez de por
lead). Se nem o valor personalizado funcionar, registre o bloqueio em
`APRENDIZADOS-CRM.md` — não existe hoje um terceiro caminho nativo
identificado.

### Listas inteligentes por SDR — o limite que decide o resto

Pesquisado antes de desenhar: os fóruns de ideias da própria HighLevel têm
mais de um pedido em aberto pedindo um filtro dinâmico "Atribuído a = usuário
atual" para Smart Lists — hoje **não existe**. O filtro "Atribuído a" só
aceita um usuário fixo, escolhido na hora de montar a lista. Uma lista
inteligente compartilhada que se adapte sozinha a quem está logado (o que o
roadmap pede ao dizer "listas inteligentes filtrando por usuário logado")
não é possível hoje — é limitação da plataforma, não deste desenho.

**Consequência prática, só quando o segundo SDR entrar (não antes — hoje é
1 usuário, e uma lista fixa por um único nome não filtra nada de útil):**
duplicar `Fila Quente` (8.1), `Fila Telefone Hoje` (8.2) e `Fila WhatsApp
Hoje` (8.3) uma vez por SDR, acrescentando o filtro `Atribuído a = <nome do
SDR>` em cada cópia — ex. `Fila Telefone Hoje — Ana`, `Fila Telefone Hoje —
Bruno`. É trabalho manual repetido a cada contratação, não uma vez só; por
isso fica registrado aqui como procedimento, não como lista já criada na
seção 8 (criar as cópias agora, com um usuário só, não tem o que filtrar).

### Estado da subconta

Confirmado nesta execução via `locations_get-custom-fields`/
`contacts_get-contacts`/`opportunities_get-pipelines`: 0 campos, 0
contatos, só o `FUNIL DE VENDAS` pré-existente — sem mudança desde a
auditoria. A subconta segue com um único usuário conhecido (o dono), então
o grupo de round robin dos nós 0.7b/0.8b nasce, na prática, com uma pessoa
só — o mecanismo já fica pronto para quando o segundo SDR entrar, sem
precisar tocar nos workflows de novo: basta adicionar o novo usuário à
mesma lista nos dois nós.

**Nenhum campo ou tag novo.** Reaproveita o campo nativo `Assigned User`
(dono do contato), que o GHL já expõe em filtro de Smart List e em ação de
workflow — criar um campo personalizado `SDR responsável` para guardar a
mesma informação seria o mesmo campo com dois donos que este projeto evita
desde o Pós-ligação (seção 4): o nativo já faz o trabalho, e um campo
espelhado diverge na primeira vez que alguém reatribuir manualmente pela
tela sem lembrar de atualizar os dois lugares. Por isso este item não
depende de `APROVADO.md` nem de criação manual de campo — só de
configuração dos nós novos e, quando houver segundo SDR, da duplicação de
listas descrita acima.

**Pronto quando (do roadmap):** dois SDRs trabalham sem colidir — cada lead
tem um dono sorteado uma vez na entrada, toda tarefa da cadência nasce para
esse dono, e a filas do dia (8.1-8.3), quando duplicadas por SDR, mostram a
cada um só o que é dele.

---

## 2.15 Monitor de Capacidade — R-11 — conferida para as 5 etapas reais em 19/09/2026, sem achado

**Por quê (herdado da lacuna L-05 do briefing):** 10 leads/dia × 12
tentativas dá ~120 tarefas/dia em regime, acima da meta de 100 do briefing —
mesmo com a saída antecipada (quem conecta ou some antes da T12) derrubando
isso para ~78-90/dia na prática, um dia de pico pode estourar sem que
ninguém perceba até o SDR desistir da fila.

Pesquisado antes de desenhar: o motor de workflow do GHL executa **por
contato** — não existe ação nativa que leia "quantos contatos estão numa
lista agora" e ramifique um `If/Else` em cima disso, e a própria base de
ideias da HighLevel confirma isso por ausência: "trazer métricas do
dashboard como custom value" ainda é pedido em aberto, não recurso
existente. Isso descarta de saída a ideia óbvia — injetar a contagem viva
numa mensagem de workflow — e explica por que Reev, Meetime, Outreach e
Salesloft resolvem capacidade com dashboard olhado por alguém, não com
alarme automático de limite. A diferença que dá para construir aqui, só
com nativo, não é o alarme automático (a plataforma não expõe o dado para
isso); é não depender de ninguém *lembrar* de abrir o dashboard, e não
obrigar o gestor a fazer a conta contra a meta toda vez que olhar.

### O desenho: três peças, cada uma cobrindo o limite da anterior

1. **Lista inteligente `Fila do Dia — Total`** (seção 8.16) — a contagem
   exata de tarefas abertas hoje, disponível em qualquer plano.
2. **Métrica personalizada `Estouro da Fila`** — o mesmo número, já
   comparado contra a meta de 100, para o gestor não fazer a conta de
   cabeça (Reporting → Custom Metrics — **confirme que o plano da
   subconta inclui métricas personalizadas antes de montar**; sem isso, a
   lista 8.16 sozinha já cobre o essencial).
3. **Workflow "Monitor de Capacidade"**, gatilho **Scheduler** (contactless,
   nativo) — não conta nada; só lembra o gestor de olhar, duas vezes por
   dia útil, para tirar a dependência de memória.

### Métrica personalizada `Estouro da Fila`

Reporting → Custom Metrics → Nova métrica → fórmula:

`(Contagem de contatos com tag "fila-tel" OU "fila-wa") − 100`

O "− 100" é de propósito, não decoração: em vez da contagem crua — que
obriga o gestor a lembrar a meta do briefing toda vez que olha —, a métrica
já devolve o excesso pronto: 0 ou negativo é dia normal, qualquer número
positivo é "estourou por N tarefas hoje". Um concorrente olhando a tela
por fora vê só "quantos contatos têm essa tag"; o alarme embutido na conta
não aparece de fora. Adicionar ao Dashboard da subconta como widget de
número único, visível na tela em que qualquer usuário loga.

A contagem em si — "quantos contatos com `fila-tel` OU `fila-wa`" — é
exatamente o total da lista 8.16: a métrica não lê nada que a lista já não
mostre, só faz a subtração que a lista sozinha não faz.

### Workflow "Monitor de Capacidade"

#### Gatilho
**Scheduler** — contactless: não amarra a nenhum evento de contato, e por
isso não pode dividir o mesmo workflow com outro tipo de gatilho (limite
nativo do recurso). Duas execuções por dia útil: **11:00** (o lote de T1 do
dia já entrou nas filas — ver a tabela de horários da seção 2.5) e **15:00**
(ainda sobra tempo de o gestor agir — remanejar SDR, segurar entrada de
lead novo — antes do fim do expediente, 18:30).

#### Configurações
| Configuração | Valor | Por que |
|---|---|---|
| Dias | Segunda a sexta | Fim de semana não tem SDR discando |
| Fuso | O da subconta (`America/Sao_Paulo`) | Mesmo padrão do resto do projeto |
| Allow Re-entry | Não se aplica | Gatilho contactless não usa este campo |

#### Nós
| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Aviso | Internal Notification | Para o gestor: "Confira `Estouro da Fila` no dashboard (ou a lista `Fila do Dia — Total`) — a meta é 100 tarefas/dia." Link direto para a lista 8.16 |

Um nó só, de propósito: sem ação nativa para ler o valor da métrica ou o
total da lista dentro do próprio workflow, um segundo nó de `If/Else` não
teria condição nenhuma para checar — o alarme de verdade mora na métrica do
dashboard (para onde o link do nó 1 aponta), não neste workflow.

### Limite conhecido

O aviso é **fixo em dois horários**, não condicionado à fila ter realmente
estourado — porque a plataforma não expõe, dentro de um workflow, "quantos
contatos passam neste filtro agora" (a mesma ausência que a pesquisa acima
confirmou). A distância entre isso e "notificação só quando passar do
limite" (o "Como" original do roadmap) é o gestor olhar a métrica duas
vezes por dia em vez de ser avisado só no dia em que ela vira positiva —
troca aceitável: o alarme fica embutido na conta (o "− 100" da métrica), e
o hábito forçado do aviso substitui a detecção automática que a API não
permite construir.

**Pronto quando (do roadmap):** o gestor sabe da fila cheia antes do SDR
desistir dela — cumprido pelo hábito de olhar 2x/dia mais o alarme
embutido na métrica, não por detecção automática de limite (a plataforma
não expõe o dado que isso exigiria).

---

## 2.16 Higiene de Número — Validação Automática (opcional) — R-13 — migrada para as 5 etapas reais em 19/09/2026

O portão 0.0/0.0b (seções 2.3 e 2.10) resolve o caso mais barato e mais
comum: contato sem telefone nenhum. Não resolve o outro caso que o roadmap
descreve ("número inválido") — um telefone **presente**, mas com formato
quebrado, DDD inexistente ou linha desligada, que só se descobre hoje
depois de o SDR discar de verdade e marcar `Número errado` (ramo da seção
4). Pesquisado antes de desenhar: o GHL tem um recurso nativo de conta,
separado de qualquer workflow — **Number Validation** (Configurações →
Telefone, habilitado por agência e depois por subconta) — que roda uma
checagem de operadora/formato/alcançabilidade num serviço de inteligência
de número (a documentação de terceiros cita Veriphone como provedor) a um
custo por checagem (referências de mercado apontam ~US$0,005/validação) e
expõe um gatilho de workflow próprio, **Number Validation**, que dispara
com o resultado (`Valid`, `Invalid`, `Landline`, entre outros status,
conforme a versão do produto). É o mesmo tipo de "verificação de número"
que Reev e Meetime deixam para integração de terceiro (ex.: serviços de
verificação de telefone cobrados à parte) — aqui sai nativo, sem sair do
GHL.

**Por que isto é item separado, e não parte do portão 0.0 acima:** o
portão 0.0 é `If/Else` sobre o campo `Phone` — nativo, gratuito, sem
depender de nenhuma configuração de conta. Este workflow depende de um
recurso pago e de uma ativação manual que pode não estar disponível no
plano/trial da subconta (mesma cautela já registrada para o Custom Metrics
do R-11) — por isso não é pré-requisito do R-13, é o complemento que fecha
a lacuna que o portão 0.0 deixa aberta (telefone presente, mas ruim).

### Ativação (manual, na tela — não sai por API)

Configurações → Telefone → **Number Validation** → ativar na agência e,
depois, na subconta `1D53YTI9C7oIMBavcQxV`. **Confirme o custo por
validação e se o plano da WeSales cobre o recurso antes de ligar** — sem
isso, este item para aqui e o portão 0.0 continua sendo a única defesa,
o que já cumpre a parte estrutural do "Pronto quando" do roadmap.

### Gatilho

**Number Validation** — contato, sem filtro de pipeline (roda também para
quem já saiu de `CONECTAR`, porque um número pode ser invalidado a
qualquer momento do ciclo de vida do contato, não só na entrada).

### Configurações

| Configuração | Valor | Por quê |
|---|---|---|
| Allow Re-entry | Ligado | O mesmo contato pode ser revalidado mais de uma vez (nova importação, correção manual do número) |
| Janela de envio | Sem janela | Marcação interna, não manda mensagem |

### Nós

| # | Ação | Configuração |
|---|---|---|
| 1 | If/Else | Status da validação **é** `Invalid` → ramo A. Senão → nó 2 |
| 2 | If/Else | Status da validação **é** `Landline` → ramo B. Senão → encerra (`Valid`/celular: nada a fazer) |

#### Ramo A — `Invalid`

| # | Ação |
|---|---|
| 1 | Add Contact Tag `telefone-invalido` |
| 2 | If/Else: etapa da oportunidade **é uma de** `NOVO LEAD`, `CONECTAR` **e** `status` **é** `open` → segue. Senão (já `AGENDAR`, `NEGOCIAR`, ou `status` já `abandoned`/`lost`) → só marca a tag e avisa (nó 4), sem mexer na etapa — um contato que já avançou por trabalho humano não retrocede por uma validação automática chegando atrasada |
| 3 | (só se o nó 2 seguiu) If/Else: `Site` ou `Instagram` preenchido → Update Opportunity `status` = `abandoned` + Add Contact Tag `nutricao-90d`. Senão → Update Opportunity `status` = `lost` |
| 4 | Internal Notification para o gestor: `Telefone inválido (validação automática): {{contact.name}} — revisar a fonte da lista` |

Mesmo desenho de saída do nó 0.0b e do ramo `Número errado` da seção 4 —
mesma tag, mesmo critério de `abandoned` vs. `lost` (tabela 1.0). Mudar o
`status` aciona o Mestre de saída (seção 3, gatilho 2 — `Opportunity
Status Changed`) sozinho: nenhuma limpeza extra precisa ser escrita aqui.
Achado desta migração, mesmo padrão já registrado para as seções 2.4/2.10/
2.11/2.12/5.3/5.4: o nó 2 original comparava só contra nome de etapa —
sem o `status é open` acrescentado aqui, um lead que já tivesse saído de
`CONECTAR` por `abandoned`/`lost` (mesma etapa, status diferente) passaria
pelo nó 2 como se ainda estivesse ativo, e o nó 3 tentaria mudar `status`
de novo num lead que a `Mestre de saída` já tinha processado — inofensivo
por ser idempotente, mas o motivo de checar é o mesmo: etapa sozinha não
basta para saber se o lead ainda está de verdade correndo cadência.

#### Ramo B — `Landline`

| # | Ação |
|---|---|
| 1 | If/Else: `Permissão WhatsApp` está vazio ou `Não solicitado` → Update Contact Field `Permissão WhatsApp` = `Não`. Senão → encerra |

Linha fixa não recebe WhatsApp (nem mensagem, nem ligação por WhatsApp) —
diferente de `Invalid`, o número **funciona**, então o lead não sai de
cadência nem ganha `telefone-invalido`; só deixa de queimar uma tentativa
de WhatsApp que nunca teria chance de conectar. O seletor de canal (nó 4 da
seção 2.4) já lê `Permissão WhatsApp` — este nó só adianta uma resposta que
o lead nunca daria sozinho.

### Limite conhecido

Nível de confiança médio: a existência do gatilho **Number Validation** e
dos status citados veio de busca (blogs especializados em GHL, não da
documentação oficial — `help.gohighlevel.com` segue bloqueado pelo proxy
deste ambiente, mesma limitação já registrada para R-09/R-10/R-11/R-12);
os nomes exatos dos status e se `Landline` existe como valor distinto de
`Invalid` **precisam ser confirmados na tela** antes de montar os nós 1/2.
Se o recurso não existir no plano da subconta, ou se o custo por validação
não for aprovado, este item fica em espera indefinida sem prejudicar o
resto do R-13 — é desenhado para ser dispensável, não para ser bloqueante.

**Pronto quando (parte do roadmap que só este item fecha):** um telefone
com formato ruim ou linha desligada é sinalizado **antes** do SDR gastar
uma ligação nele, não só depois — a distância que separa o portão 0.0
(cobre "não tem telefone") de fechar também "tem telefone, mas é ruim".

---

## 2.17 Dashboard do Gestor — R-15 — conferida para as 5 etapas reais em 19/09/2026, sem achado (usa `Pré-vendas` só como apelido do pipeline, ver seção 1)

**Por quê (herdado do roadmap):** todo o resto que os blocos 1 a 5 constroem
morre se depender de alguém abrir seis listas inteligentes por hora. O
gestor precisa de uma tela só.

Pesquisado antes de montar: Reev e Meetime embutem o dashboard no próprio
produto porque são eles quem gera o dado (dialer próprio, sequência
própria) — aqui o dado nasce nos campos e listas que este projeto já
construiu (R-01, R-02, R-03, R-11), e a pergunta certa não é "criar um
dashboard do zero", é "que tipo de widget nativo do GHL consegue ler o que
já existe". Três achados decidiram o desenho:

1. **Smart List não vira widget de Dashboard.** É pedido em aberto na base
   de ideias pública da HighLevel ("Add option to put smart lists on
   dashboards", sem previsão) — confirmado por busca, não por tentativa na
   tela (a subconta ainda não tem pipeline nem workflow publicado para
   gerar dado de verdade). Isso descarta de saída a ideia mais óbvia:
   pinar as listas 8.1 a 8.18 direto numa tela. O dashboard não repete as
   listas — aponta para elas.
2. **Custom Metrics soma campo numérico, não só conta tag.** Achado que
   muda o alcance deste item sobre o que o R-11 já tinha mapeado: o
   Formula Editor de Custom Metrics aceita agregação **Soma/Mín/Máx/Média**
   sobre campo `NUMERICAL`/`MONETARY`, além de "contagem de contatos com
   tag" — então os contadores do R-01 (C-09 a C-12) viram métrica de
   dashboard sem campo novo. Mesma cautela já registrada para o R-11: o
   recurso Custom Metrics é de plano pago (referências de mercado
   apontam a partir de planos $497+) — **confirme na tela antes de montar
   os itens 3 e 4 abaixo**; sem ele, os itens 1 e 2 (nativos, qualquer
   plano) já entregam metade do "Pronto quando".
3. **Os contadores do R-01 são cumulativos, não diários.** C-09 a C-12
   nunca zeram (é o desenho de propósito da seção 2.4/4 — um contador que
   reseta por dia teria dois donos escrevendo o mesmo campo em horários
   diferentes, o problema que este projeto evita desde o nó do contador de
   WhatsApp). Consequência honesta: "ligações/dia" e "conexões/dia", como o
   roadmap pede ao pé da letra, não saem de um `Sum` sobre esses campos —
   isso dá o total acumulado desde sempre, não o de hoje. O "Como" do
   roadmap vira o que a plataforma permite de verdade: taxa de conexão
   **acumulada** (mesma granularidade que a lista 8.6 já usa) mais o
   volume de **tarefas** do dia (evento com timestamp próprio, diferente
   de um contador sem histórico) — ver item 3 e o Limite conhecido no
   fim desta seção.

### O desenho: quatro peças nativas, uma tela

Reporting → Dashboards → **Novo dashboard** → nome `Painel do Gestor —
Pré-vendas`.

**1. Widget "Appointment Report"** (nativo, qualquer plano) — filtrado pelo
calendário `Reunião com closer` (seção 7.1). Cobre "agendamentos" do
"Como" do roadmap direto: booked, cancelado, no-show, taxa de
comparecimento — sem depender de nenhum campo deste projeto, porque lê o
agendamento em si.

**2. Widget "Opportunities"** (nativo, qualquer plano) — funil ao vivo do
pipeline `Pré-vendas`, por etapa, snapshot do momento em que o gestor abre
a tela. Complementa, não repete, o funil mensal das listas 8.9 a 8.12
(R-03): aquelas dizem "quantos entraram/conectaram/agendaram/compareceram
**este mês**"; este widget diz "quantos estão em cada etapa **agora**" —
perguntas diferentes, mesma fonte de dado.

**3. Widget "Tasks"** (nativo, qualquer plano, criadas/concluídas/
vencidas) — sem filtro por prefixo de título confirmado na tela (ver
Limite conhecido), é a aproximação mais próxima que a plataforma nativa dá
de "ligações/dia": toda tentativa da Cadência 12x30 e da Cadência Inbound
cria uma tarefa `[CADENCIA]` (seções 2.4 e 2.10), então o volume de
tarefas criadas/concluídas num dia é, no pior caso, um proxy do volume de
ligações daquele dia — no melhor caso (se o filtro de título existir),
o número exato.

**4. Widgets de Custom Metrics** (plano pago — confirme antes de montar):

| Métrica | Fórmula | O que cobre do "Como" do roadmap |
|---|---|---|
| `Estouro da Fila` (já existe, R-11 — seção 2.15) | `(Contagem de contatos com tag "fila-tel" OU "fila-wa") − 100` | Fila em atraso — capacidade |
| `Atrasos de Speed-to-lead` (nova) | `Contagem de contatos com tag "atraso-1a-tentativa"` | Fila em atraso — SLA da 1ª tentativa (a mesma tag que a lista 8.8 já filtra) |
| `Taxa de Conexão — Telefone` (nova) | `(Soma de "Conexões telefone" ÷ Soma de "Tentativas telefone") × 100` | Taxa por tentativa — telefone, acumulada |
| `Taxa de Conexão — WhatsApp` (nova) | `(Soma de "Conexões WhatsApp" ÷ Soma de "Tentativas WhatsApp") × 100` | Taxa por tentativa — WhatsApp, acumulada |
| `Taxa de Conexão Real — Telefone` (nova, F-06, peça 2) | `(Soma de "Conexões reais telefone" ÷ Soma de "Ligações com transcrição") × 100` | **Das chamadas que dá para medir**, quantas duraram mais de 60s — sem depender do julgamento do SDR. O denominador **não** é `Tentativas telefone`: os dois lados precisam da mesma população, ver "Conferência da peça 2" na seção 2.27 |
| `Leads novos hoje` (nova, F-10) | `Contagem de contatos com "Date Created" = hoje` | **Entrada do dia** — o único indicador que piora quando a operação para de receber lead, e o único que nenhum monitor do F-05 cobre. Zero às 12h já é sinal. Usa a contagem de contatos por filtro (achado 2 desta seção), que aqui é a unidade certa |
| `Leads novos — 7 dias` (nova, F-10) | `Contagem de contatos com "Date Created" nos últimos 7 dias` | Tendência de entrada: separa "dia fraco" de "parou". **Leia contra o maior intervalo já observado** (15h06 nesta base) e não contra um total de horas — hora absoluta não se calibra, e foi por isso que a abertura do F-10 publicou um número errado que "soava plausível". Medido em 22/09: mais de 22h sem lead novo (número corrigido — a abertura do F-10 tinha escrito ~46h por erro de conta, ver `ROADMAP-SALES-ENGAGEMENT.md`), e nenhum alerta existia para dizer isso |
| `Cobertura da Medição — Telefone` (nova, F-06, peça 2) | `(Soma de "Ligações com transcrição" ÷ Soma de "Tentativas telefone") × 100` | Quanto da operação de telefone está instrumentada (LC Phone + transcrição ligada). Abaixo de ~90%, a linha acima merece ressalva; abaixo de ~50%, o F-06 está medindo outra operação |

A quinta linha é a que fecha o "Pronto quando" do F-06 no dashboard: por
que não reaproveita `Conexão real` direto na fórmula, e por que precisou
de um campo novo (`Conexões reais telefone`, C-31, `NUMERICAL`) em vez de
só trocar o nome do campo na conta acima, está registrado em
`build-wesales.md`, seção 2.27 ("Peça 2") e `campos-e-tags.md` (C-31) —
resumo: Custom Metrics só soma `NUMERICAL`/`MONETARY`, `Conexão real` é
`SINGLE_OPTIONS`, e contar contatos no estado atual misturaria unidade
diferente da de `Tentativas telefone` (soma cumulativa de tentativas, não
de contatos). Convive com a linha `Taxa de Conexão — Telefone` acima —
nenhuma substitui a outra, cada uma responde uma pergunta diferente
(conectou vs. conversou).

Nenhuma das cinco é campo ou tag nova além do já registrado: as três
"Taxa" reaproveitam C-09/C-10 (Tentativas) e C-11/C-12/C-31 (Conexões,
incluindo a nova C-31 do F-06) — o mesmo raciocínio de "não duplicar o
que o projeto já expõe" que fechou o R-10 e o R-13 em `campos-e-tags.md`.
Se o plano da subconta não incluir Custom Metrics, as duas primeiras
linhas continuam cobertas pela lista 8.16 e 8.8 (sem entrar no dashboard)
e as três últimas pela lista 8.6, que já ganhou a coluna `Conexão real`
na mesma peça — o dashboard perde a tela única, não perde o dado. As duas
últimas linhas (F-10) têm o mesmo fallback: as **duas** listas da seção
8.25 (`Entrada — últimas 24h` e `Entrada — últimos 7 dias`), que fazem a
mesma pergunta por filtro de data **relativo** sem depender do plano pago —
só perdem o total pronto, que sem Custom Metrics vira contar linha na tela.
São duas listas salvas de propósito: trocar o filtro de uma só muda a view
para todo mundo que a usa.

**5. Seção "Compliance" (nova, R-14):** referência às duas listas da
seção 8.26/8.27 (`Auditoria — tag sem DND nativo` e `Auditoria — DND sem
tag`) — não widget de Custom Metric por padrão, porque a métrica de
"contagem de contatos com tag" descrita na pesquisa desta seção (achado 2
acima) filtra por tag/pipeline/owner/metric-level, sem citar DND; combinar
tag **e** filtro de DND numa única fórmula não está confirmado como
possível. Se a tela confirmar que dá, as duas viram Custom Metric (`Sem
DND — Contagem` / `Sem tag — Contagem`, meta zero); se não, as duas Smart
Lists sozinhas já cumprem o "relatório que prova" do R-14 sem depender de
plano pago — mesmo raciocínio de fallback das outras quatro peças desta
seção.

**6. Reporting → Pipeline (nativo, F-12, 22/09/2026):** a pergunta "por que
estamos perdendo" não tinha widget nem lista aqui — Custom Metrics não
agrega por valor de `SINGLE_OPTIONS` (achado 2 desta seção), então
`Motivo da desqualificação` (C-16) nunca teve para onde ir. Não é mais
lacuna: o relatório nativo de Pipeline do GHL já quebra oportunidades
perdidas por `Lost Reason`, o campo nativo de oportunidade que a seção 4.1
passou a alimentar com o mesmo valor de C-16. Não é widget deste dashboard
— é uma tela própria do Reporting nativo — mas fecha a pergunta sem
depender de Custom Metrics nem de plano pago. Detalhe completo, incluindo o
que ainda não está confirmado na tela, em `build-wesales.md`, seção 4.1.

### Limite conhecido

"Ligações/dia" e "conexões/dia" literais — a contagem de um dia
específico, separada do total acumulado — não têm caminho nativo neste
desenho, pela razão do achado 3 acima: os únicos contadores do projeto
não têm timestamp por evento, só um valor corrente. Resolver isso de
verdade pediria um campo por-dia resetado por um Scheduler, o mesmo tipo
de contador-com-dois-donos que este documento evita desde a seção 2.4 —
não vale o risco por uma métrica que o widget de Tasks já aproxima. Se o
volume da operação um dia justificar o gasto, a saída correta é um
sistema de telefonia com log de chamada nativo (LC Phone da própria
HighLevel, ou um dialer de terceiro) alimentando o widget "Calls by
outcome or user" que o Dashboard já suporta — fora do escopo deste item
porque a operação hoje disca por fora do GHL.

Nível de confiança médio para os três achados desta seção: vieram de
busca (`ghlexperts.com`, `consultevo.com`, `help.gohighlevel.com` nos
resultados de busca, ainda bloqueado por leitura direta pelo proxy deste
ambiente — mesma limitação já registrada para R-09 a R-13), não de teste
na tela. Confirme os nomes exatos dos widgets e a disponibilidade de
"Sum" no Formula Editor antes de montar.

**Pronto quando (do roadmap):** o gestor abre uma tela e sabe se o dia foi
bom — cumprido pelos widgets 1 e 2 (sempre disponíveis) mais o volume de
tarefas do widget 3; os widgets 4, se o plano cobrir, somam taxa de
conexão e fila em atraso sem o gestor abrir lista nenhuma. O que fica de
fora, documentado acima, é a contagem exata por dia — troca aceita pelo
mesmo motivo que o R-11 aceitou o aviso em horário fixo em vez de alarme
condicionado: a plataforma nativa não expõe o dado que a versão literal
do roadmap pediria.

---

## 2.18 Horário aprendido por segmento — mecanismo (F-02)

**Por quê:** a tabela 2.5 tem um horário fixo por tentativa, igual para todo
mundo. Dentista atende às 14h, obra atende às 7h — a operação só descobre
isso depois de centenas de ligações, e hoje não guarda o dado que provaria a
diferença.

**Pesquisado antes de desenhar:** a literatura de outbound (Gong.io, HubSpot,
citada em busca) converge em manhã tarde (10h-11h) e fim de tarde (16h-17h)
como janelas médias de melhor conexão — mas é média de mercado, não da base
desta operação. Salesloft anuncia send-time optimization (recurso "Rhythm")
para e-mail, e a documentação de Outreach fala em "segment-level analysis"
para mensagem — nenhuma das duas fontes encontradas descreve uma janela de
**ligação** aprendida por segmento a partir dos dados do próprio cliente, só
médias agregadas do produto ou otimização de e-mail. É a lacuna que este
item fecha: horário por segmento vindo da conexão real desta base, não de
benchmark de mercado nem de caixa-preta de IA de terceiro — o tipo de coisa
que um concorrente não replica só olhando a tela, porque o dado é nosso.

**O que este item entrega agora:** a captura do dado e o lugar para
enxergar o padrão. **O que ele não entrega ainda, e não poderia:** o
"Pronto quando" do roadmap ("o horário da T3 de um segmento é diferente do
de outro, e a diferença veio de evidência") só se cumpre depois que
conexões de verdade acontecerem — com a subconta em 0 contatos reais
(reconfirmado nesta execução), qualquer horário por segmento agora seria
palpite disfarçado de dado, o oposto do que o item pede.

### Captura — nós novos no Pós-ligação (seção 4, ramo `Atendeu`)

Nós 7b/7c, logo depois do carimbo `Data conectado` (nó 7): `Date/Time
Formatter` reformata `{{right_now}}` para só a hora (`HH`, 00–23), e
`Update Contact Field` grava em `Hora da conexão` (C-25, `campos-e-tags.md`).
**Nível de confiança médio** no formato exato do "To Format" do Date/Time
Formatter: achado só por busca (`growthable.io`, `consultevo.com`,
`gohighlevele.com`) — `help.gohighlevel.com` segue bloqueado pelo proxy
deste ambiente para leitura direta, mesma limitação registrada desde o
R-09. Confirme o token de hora isolada (`HH` ou equivalente da tela) antes
de montar; se a ação não suportar extrair só a hora, o caminho alternativo
é gravar `{{right_now}}` completo (como C-14/C-18/C-19 já fazem) e recortar
os dois dígitos da hora na leitura da lista 8.19 — mais trabalho manual
para o gestor, mesmo dado.

### Visualização — lista 8.19

Especificada na seção 8 (`Conexão por Segmento e Horário`). Nenhuma conta
nova: GHL não agrupa nem tira média dentro de uma Smart List (mesmo achado
já registrado no R-11 para Custom Metrics) — a lista só filtra e ordena, o
padrão sai do gestor olhando a coluna `Hora da conexão` agrupada visualmente
por `Segmento`.

### O que fica pronto para quando a evidência existir

A tabela 2.5 (seção 2.5) continua única e compartilhada — é o "senão" de
qualquer ajuste futuro. O ponto exato onde um ajuste por segmento entraria,
se e quando a lista 8.19 mostrar um padrão real, é o nó 2 do bloco padrão de
tentativa (seção 2.4, "Aguardar horário"): um `If/Else` por `Segmento` antes
dele, com um ramo por segmento que tiver padrão comprovado e a tabela 2.5
atual como `senão`. **Não construído nesta rodada de propósito:** com 0
conexões reais, não há segmento com volume para justificar um ramo — criar
o `If/Else` agora seria condicionar a régua a um palpite travestido de dado,
exatamente o que o "Pronto quando" do item proíbe. Fica registrado como
decisão de bloqueio, não como lacuna esquecida: quando a lista 8.19 mostrar
um segmento com **volume suficiente para não ser ruído** (o gestor decide o
número — este documento não inventa uma casa decimal de confiança
estatística para uma amostra que ainda não existe), o `If/Else` é a mudança
mínima, num nó já mapeado, não uma reforma da cadência.

Este mecanismo cobre só a Cadência 12x30 (horário de relógio fixo, tabela
2.5). A Cadência Inbound (seção 2.10) usa espera **relativa** (minutos desde
a entrada, não horário de relógio) — "horário aprendido por segmento" não
se aplica a ela pela própria natureza da régua, não por lacuna deste item.

---

## 2.19 Teto de toques por semana — F-04

**Por quê:** lead em duas cadências recebe o dobro de toques, e ninguém
percebe até o opt-out chegar — a frase original do roadmap. Achado ao
desenhar este item, mais preciso que a frase: a Cadência 12x30 sozinha
dificilmente aproxima do problema (pico real é 4 toques em D1+D2, tabela
2.5), e as réguas vizinhas (Inbound, Reengajamento) já têm blindagem de tag
uma-ou-outra (R-07, R-08). Quem **não** tem nenhum limite é a Interceptação
de Sinal (seção 2.9, F-01): com `Allow Re-entry` ligado de propósito, um
lead que clica o link de agendar (ou responde fora do fluxo) várias vezes no
mesmo dia gera uma tarefa `ligar agora` e um aviso ao SDR a cada clique, sem
teto nenhum. É o mesmo tipo de "estrago silencioso" que o F-05 (monitor de
saúde) persegue, só que aqui dá para prevenir antes de precisar de um
monitor perceber.

**Pesquisado antes de desenhar:** o Outreach.io resolve o caso de duas
cadências com **Sequence Exclusivity** — um prospect marcado como exclusivo
de uma sequência não pode ser adicionado a outra até sair da primeira
(`support.outreach.io`, "Sequence Exclusivity Settings"). É uma trava de
**admissão** (impede a entrada), não de **frequência** — não ajuda contra o
caso real encontrado aqui, que não é duas cadências ao mesmo tempo, é uma
cadência mais um workflow de sinal disparando em paralelo por natureza (não
é bug, é o desenho do F-01). A literatura de outbound (`martal.ca`,
`woodpecker.co`, achada por `WebSearch`) converge em 3 a 5 toques por semana
como faixa segura contra fadiga do prospect antes do opt-out. Um teto fixo
por contato, contado numa janela **móvel** de 7 dias corridos (não um
"zerar toda segunda-feira", que deixa passar sábado+segunda como se fossem
semanas diferentes) é o desenho que nenhuma das duas plataformas de
prateleira do enunciado expõe pronto — Outreach trava admissão, não
frequência; nenhuma fonte encontrada descreve um contador rolante por
contato que soma telefone, WhatsApp e sinal no mesmo teto.

**Teto escolhido: 6 por semana.** Acima do pico real de uso normal da
Cadência 12x30 sozinha (4, D1+D2) com folga para 1-2 toques extra de sinal
sem bloquear o fluxo saudável, e dentro da faixa "até 5-8" que a pesquisa
de mercado trata como segura para não queimar a base. O gestor pode ajustar
o número direto no `If/Else` do nó 2.5c/3c sem precisar de outro campo.

### Campo novo

`Toques na semana` (C-26, `campos-e-tags.md`), `NUMERICAL`, começa em 0 no
nó 0 de cada cadência (a inicialização de cada workflow já zera outros
contadores por lead novo, seção 2.3 nó 0.1 — este seria o mesmo tipo de nó,
uma vez publicado o campo).

### Workflow novo — "Contador de Toques"

Gatilho comum, com contato em contexto (`Contact Tag Added`) — não confundir
com o `Scheduler` contactless do R-11 (seção 2.15), que roda sem nenhum
contato associado. Aqui cada execução já sabe de quem é o toque: é o mesmo
contato que ganhou a tag `toque` em outro workflow.

| Configuração | Valor |
|---|---|
| Gatilho | `Contact Tag Added` — Tag: `toque` |
| Allow Re-entry | **Ligado** — cada toque é um evento novo, mesmo motivo do F-01 (seção 2.9.2): sem isso, o segundo toque da semana não reabre o workflow e o contador para de subir |
| Stop on Response | Desligado (este workflow não manda mensagem, não há resposta para parar) |

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Limpar o pulso | Remove Contact Tag | `toque` — a tag é só o gatilho, não um estado; sem remover, ela se acumula como tag "presente" sem significar nada depois do primeiro toque |
| 2 | Somar | Update Contact Field — Math | `Toques na semana` `+ 1` |
| 3 | Esperar a janela | Wait → Time Delay | 7 dias |
| 4 | Descontar | Update Contact Field — Math | `Toques na semana` `- 1` |

Cada toque abre sua própria instância deste workflow (`Allow Re-entry`
ligado permite isso — mesmo raciocínio já registrado em
`APRENDIZADOS-CRM.md` para a Interceptação de Sinal: múltiplos sinais do
mesmo contato rodam em paralelo, não substituem um ao outro). Um toque no
dia 1 soma no dia 1 e desconta no dia 8; um segundo toque no dia 3 soma no
dia 3 e desconta no dia 10 — o campo reflete sempre "quantos toques nos
últimos 7 dias corridos", uma janela que desliza com o tempo, não um balde
que zera numa data fixa. É o desenho que a pergunta "venha de onde vier" do
"Pronto quando" do roadmap pede: o contador não sabe nem precisa saber qual
workflow gerou o toque.

### Onde o toque é emitido — nesta rodada

`Add Contact Tag: toque` foi ligado nos dois pontos de maior risco real,
identificados acima — não em todo o documento, decisão de escopo explicada
abaixo:

| Onde | Nó | Já editado nesta rodada? |
|---|---|---|
| Cadência 12x30 — cada tentativa | seção 2.4, nó 7 (Criar tarefa) | Sim |
| Cadência 12x30 — M1 (as duas variantes do Split) | seção 2.6.1, nós M1.4a/M1.4b | Sim |
| Cadência 12x30 — M2/M3 | seção 2.6, parágrafo de abertura | Sim |
| Interceptação de Sinal — Clique | seção 2.9.2, nó 7 | Sim |
| Interceptação de Sinal — Resposta | seção 2.9.3 (herda a tabela da 2.9.2) | Sim |
| Cadência Inbound | seção 2.10, nó 6 | **Não** — deferido, ver abaixo |
| Reengajamento 90 dias (TR1-TR4) | seção 2.12 | **Não** — deferido |
| Recuperação de No-show (NS1-NS3) | seção 5.3 | **Não** — deferido |

### Onde o teto é checado — nesta rodada

`Toques na semana` **≥** 6 checado em dois portões, os mesmos dois pontos
de emissão de maior risco:

- Cadência 12x30: nó 2.5c/2.5d (seção 2.4) — represa 1 dia e reconsulta,
  mesmo padrão da pausa individual (nó 2.5).
- Interceptação de Sinal (Clique e Resposta): nó 3c — pula a tarefa e o
  aviso, mas ainda registra a nota (seção 2.9.2). **Não** usa o padrão de
  represar-e-reconsultar da 12x30 aqui de propósito: o sinal já aconteceu
  (o lead já clicou ou respondeu), não há "dia certo" para reagendar como
  há numa tentativa da régua — represar um sinal por 1 dia destruiria
  exatamente a vantagem de minutos que o F-01 existe para entregar.

**Decisão de escopo, não lacuna esquecida:** a Cadência Inbound (seção
2.10), o Reengajamento (seção 2.12) e a Recuperação de No-show (seção 5.3)
reaproveitam o mesmo campo, a mesma tag e o mesmo workflow "Contador de
Toques" sem precisar de nada novo — só falta ligar `Add Contact Tag: toque`
no nó de tarefa de cada um e, na Inbound, decidir a variante do portão
(represar 1 dia quebraria a SLA de minutos do R-07, então o padrão certo lá
é o mesmo "pula e registra" da Interceptação de Sinal, não o da 12x30).
Nenhuma delas soma perto do teto sozinha no desenho atual (Inbound: 5
toques em 3 dias; Reengajamento: 4 em 10 dias; No-show: 4 em 4 dias) — o
risco real identificado nesta rodada está nos dois pontos já ligados.
Fechar as três réguas restantes é a próxima fatia deste mesmo item, não um
item novo.

### Limite conhecido

Mesmo aviso já registrado na seção 2.8 para a Cadência 12x30: se o workflow
"Contador de Toques" for editado e republicado enquanto contatos estão
parados no Wait de 7 dias (nó 3), o GHL pode reposicionar essas instâncias
— o desconto de um toque antigo pode se perder. Baixo risco na prática
(este workflow não deve precisar de edição frequente depois de publicado),
mas vale conferir `Toques na semana` manualmente se ele for republicado com
contatos em trânsito.

**Pronto quando (do roadmap):** "nenhum lead recebe mais que N toques por
semana, venha de onde vier" — cumprido para os dois canais de maior volume
e maior risco (Cadência 12x30 e Interceptação de Sinal); "venha de onde
vier" por completo depende de ligar os três pontos deferidos acima.

---

## 2.20 Monitor de Saúde da Operação — F-05 (peça 1 de N: lead esquecido em `NOVO LEAD`)

**Por quê:** automação falha em silêncio, e este projeto já viveu o caso
real: G-03 (`ROADMAP-SALES-ENGAGEMENT.md`) só existe porque uma sessão
automática *percebeu, olhando o número na mão*, que 47 oportunidades pagas
estavam paradas em `NOVO LEAD` há mais de 24h — nada na máquina avisou
sozinho. Qualquer que seja a opção que o dono escolher para o G-03
(promoção automática, com ou sem janela, ou destravar o estoque de hoje),
nenhuma delas impede a **próxima** estagnação — um formulário que para de
disparar a Porta de Entrada, um SDR de férias sem substituto revisando a
fila, um filtro que passa a excluir gente por engano. G-03 resolve o
estoque de hoje; este item é o sensor que evita depender de outra sessão
notar o número por acaso.

Pesquisado antes de desenhar: nenhuma das quatro plataformas do enunciado
do projeto (Reev, Meetime, Outreach, Salesloft) expõe um alarme proativo
para "lead parado numa etapa" — o padrão do mercado é monitorar métricas de
**saída** (taxa de resposta, taxa de aceite) que podem ficar estáveis
enquanto o funcionamento por trás já quebrou (achado equivalente,
`heyreach.io/blog/why-automation-fails`, sobre sequências de outbound: as
equipes olham o resultado agregado e não o comportamento por trás dele, e
o funil "silencia" antes de qualquer métrica de saída se mexer). A saída
nativa aqui é o mesmo padrão de relógio por evento que já validou o R-02
(Alerta de Speed-to-lead, seção 2.11) e o SLA do Closer (seção 5.4): um
`Wait` marcando um prazo, e um portão que confere se o prazo estourou de
verdade antes de avisar.

**Escopo desta rodada, decisão e não lacuna esquecida:** o "Como" original
do F-05 listava seis invariantes: `fila-tel`/`fila-wa` presente há mais de
24h, `CONECTAR` sem tentativa há 7 dias, tarefa vencida sem resultado,
`nao-perturbe` ainda dentro de workflow ativo, `Conectado` sem fechar o
loop em 24h, `Retorno agendado` vencido. Nenhuma delas ganhou workflow
nesta rodada — nem a de `NOVO LEAD`, que não estava na lista original e
entrou por conta própria (achado do G-03, motivo acima). Ao ler as seis com
calma antes de escolher a próxima, achei que **"tarefa vencida sem
resultado", como está escrita, já não é um risco não coberto**: o nó 10b do
bloco padrão (seção 2.4) já define `Resultado da tentativa = Não atendeu` e
aplica `limpar-tarefas` sozinho quando o `Wait` do nó 8 estoura às 18:30 sem
resposta do SDR — não existe "tarefa vencida sem resultado" pendente para
sempre, ela vira "Não atendeu" classificado automaticamente no mesmo dia, e
a lista 8.5 (`Sem resultado ontem`) já mostra esse volume para quem quiser
olhar. **Não confundir com `fila-tel`/`fila-wa` presente há mais de 24h**
(a primeira invariante da lista): essa continua um risco de verdade e
diferente — se `fila-tel` ainda está lá depois de 24h, o próprio nó 9 (que
remove a tag sempre, todo dia) não rodou, o que é sinal de workflow
travado ou instância perdida, não de SDR lento. As quatro invariantes
restantes (`fila-tel`/`fila-wa` há 24h, `CONECTAR` sem tentativa há 7 dias,
`nao-perturbe` em workflow ativo, `Conectado`/`Retorno agendado` vencidos)
seguem de pé, pedem mais desenho (a última, por exemplo, depende de
"esperar até uma data dinâmica", não testado neste conector) e ficam para a
próxima peça deste mesmo item, não um item novo. `NOVO LEAD` esquecido foi
a primeira porque é a única com evidência de produção real (G-03) e a mais
simples de desenhar com confiança.

### Workflow "Lead Esquecido em NOVO LEAD"

#### Gatilho
**Opportunity Stage Changed** — Pipeline `FUNIL DE VENDAS` · Para a etapa:
`NOVO LEAD` (dispara tanto na entrada da Porta de Entrada, seção 1.3,
quanto em qualquer reentrada futura em `NOVO LEAD` que ninguém previu hoje)

#### Configurações
| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | Cada entrada em `NOVO LEAD` merece seu próprio relógio, mesmo motivo do R-02 (seção 2.11) |
| Janela de envio | Sem janela, 24/7 | É aviso interno ao gestor, não mensagem ao lead — travar numa janela de expediente só atrasaria a detecção, mesmo raciocínio do F-01 (seção 2.9.2) |
| Stop on Response | Desligado | Não há mensagem ao lead aqui |

#### Nós
| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Aguardar | Wait → Time Delay | 24 horas corridas |
| 2 | Portão | If/Else | Etapa da oportunidade **ainda é** `NOVO LEAD` **E** `status` **é** `open` → segue (ninguém revisou o lead neste 1 dia). Senão → **encerra** (já foi promovido para `CONECTAR` ou descartado — nada para avisar) |
| 3 | Fila | Add Contact Tag | `novo-lead-estagnado` |
| 4 | Aviso | Internal Notification | Para o gestor: `{{contact.name}} está há mais de 24h em NOVO LEAD sem revisão. Origem: {{contact.source}}.` |
| 5 | Registro | Add Note | `Alerta de saúde: NOVO LEAD sem revisão em 24h · {{right_now}}` |

**Por que 24h e não outro prazo:** é o mesmo limite que o próprio G-03 usou
para chamar o estoque de "crescendo, grave" — abaixo disso um lead pode só
estar esperando o SDR abrir a fila do dia; acima, já é o oposto exato do
que a Porta de Entrada e o R-02 foram construídos para garantir.

**Limpeza da tag, achado ao desenhar (mesma classe de bug que o Mestre de
saída já documentou para outras réguas):** o Mestre de saída (seção 3) só
limpa tag quando a oportunidade **sai** de `CONECTAR`/`open` — seu nó 1
encerra em no-op exatamente na transição `NOVO LEAD` → `CONECTAR`, que é a
forma normal de resolver este alerta. Colocar `novo-lead-estagnado` na
lista de remoção do nó 4 do Mestre de saída (como as outras tags de fila)
não bastaria: aquele nó nunca é alcançado nesta transição específica.
Por isso a limpeza entra como um nó novo, incondicional, **antes** do
portão do Mestre de saída — ver seção 3, nó 0, abaixo. `Remove Contact Tag`
de quem não tem a tag não faz nada (mesmo raciocínio já usado para
`Remove from Workflow` na entrada da seção 3), então rodar sempre é seguro
mesmo para a maioria dos leads que nunca chegou a ficar estagnado.

**Limite conhecido, o mesmo já registrado para o G-01 e para o G-03:**
publicar este workflow **não varre os 47 leads que já estão parados
hoje** — o gatilho dispara no instante da mudança de etapa, não ao ligar o
workflow. Rodar `Add to Workflow` em massa pela lista de oportunidades em
`NOVO LEAD` depois de publicar cobre o estoque atual; dali em diante, todo
lead novo (ou reativado) já nasce com o relógio ligado sozinho.

**Pronto quando (peça 1 do F-05):** um lead parado em `NOVO LEAD` por mais
de 24h gera aviso ao gestor sozinho, sem depender de outra sessão notar o
número na mão — o que faltou até o G-03 ser achado manualmente.

---

## 2.21 Monitor de Saúde da Operação — F-05 (peça 2 de N: `fila-tel`/`fila-wa` presa)

**Por quê:** a segunda das quatro invariantes que ficaram para depois na
peça 1 (seção 2.20) — e, das quatro, a única que **não** é "SDR não decidiu
a tempo": se `fila-tel` ou `fila-wa` ainda está no contato mais de um dia
depois de aplicada, é porque o nó 9 do bloco padrão (seção 2.4, "remova as
duas, sempre") **não rodou** — instância de workflow perdida, travada ou
alguma falha do motor do GHL, não lentidão humana. É o mesmo tipo de
"estrago silencioso" da peça 1, só que aqui o sintoma é o oposto: em vez de
um lead nunca entrar em fila, é uma fila que nunca some — o SDR liga
achando que a tarefa ainda vale, ou a lista `Fila Telefone Hoje`/`Fila
WhatsApp Hoje` (8.2-8.3) mostra um contato que já devia ter saído dela há
dias.

Pesquisa de mercado: a mesma da peça 1 vale aqui, mesma classe de
invariante (saúde do motor, não do funil) — nenhuma das quatro plataformas
do enunciado do projeto expõe alarme proativo para isso; é reporting de
engenharia interna, não recurso de sales engagement.

**Achado ao desenhar — por que este workflow não espera 24h fixas a partir
do momento em que a tag foi aplicada, ao contrário da peça 1 e do R-02:**
a primeira versão deste desenho fazia exatamente isso (`Wait` 24h desde o
gatilho, depois checava se a tag ainda estava lá) e tinha um bug real de
falso positivo. A tabela 2.5 encaixa mais de uma tentativa no mesmo dia e
em dias consecutivos (T1 D1 10:30 e T3 D2 09:20, por exemplo, ficam a 22h50
uma da outra — menos de 24h). Um relógio de 24h disparado pela T1 checaria
o contato às 10:30 de D2, quando a T3 já pode estar com `fila-tel` aplicada
de novo, a menos de 1h de vida, sem nada de errado — o alerta da T1
confundiria a fila **nova e saudável** da T3 com a fila **velha e travada**
que ele deveria estar medindo. Como o nó 9 do bloco padrão sempre roda
**até 18:30 do mesmo dia** em que a tag foi aplicada (nó 8, mesmo tempo
limite), a checagem certa não é "24h depois do gatilho", é "depois das
18:30 de hoje" — ancorada no relógio do dia, não numa contagem relativa a
partir do disparo. Isso elimina a janela de confusão entre tentativas
vizinhas sem precisar de campo novo para guardar "qual tentativa disparou
este alerta" (uma alternativa cogitada e descartada: um campo de
`NUMERICAL` copiando `Tentativa nº` no gatilho tem o mesmo problema de
"contador com dois donos" já documentado na seção 2.4 — duas instâncias
deste workflow rodando ao mesmo tempo, uma por tentativa próxima,
sobrescreveriam o campo uma da outra antes da comparação final).

### Gatilhos
1. **Contact Tag Added** — `fila-tel`
2. **Contact Tag Added** — `fila-wa`

(dois gatilhos no mesmo workflow, em OR — o mesmo recurso já usado e
confirmado no Mestre de saída, seção 3: "GHL aceita mais de um gatilho no
mesmo workflow, cada um em OR")

### Configurações
| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | Cada tentativa que aplica a tag merece seu próprio relógio, mesmo raciocínio do R-02 (seção 2.11) e da peça 1 (seção 2.20) |
| Janela de envio | Sem janela, 24/7 | Aviso interno ao gestor, não mensagem ao lead |
| Stop on Response | Desligado | Não há mensagem ao lead aqui |

### Nós
| # | Nó | Ação | Configuração |
|---|---|---|---|
| 0 | Limpeza preventiva | Remove Contact Tag | `fila-travada` — barato mesmo se ausente (mesmo raciocínio do nó 3b/5d da seção 2.4). Se este gatilho disparou de novo é porque uma tentativa nova aplicou `fila-tel`/`fila-wa`, prova de que a cadência não está mais parada no ciclo que gerou um alerta anterior, se houve algum |
| 1 | Aguardar | Wait → Until specific time | 19:00 do mesmo dia (30 min de folga depois das 18:30, o prazo do nó 8 da seção 2.4 — nenhuma tentativa da tabela 2.5 aplica a tag depois das 17:20, então "hoje às 19:00" nunca cai no passado quando o gatilho dispara) |
| 2 | Portão | If/Else | Tag `fila-tel` **presente** OU tag `fila-wa` **presente** → segue (o nó 9 da tentativa que disparou este relógio não rodou até o fim do próprio dia). Senão → **encerra** (a fila foi limpa a tempo — caminho feliz) |
| 3 | Fila | Add Contact Tag | `fila-travada` |
| 4 | Aviso | Internal Notification | Para o gestor: `{{contact.name}} está com fila-tel/fila-wa presa desde antes de hoje às 18:30 — o nó 9 da cadência não rodou. Tentativa nº {{contact.tentativa_n}}.` |
| 5 | Registro | Add Note | `Alerta de saúde: fila-tel/fila-wa travada, nó 9 não removeu até 18:30 · {{right_now}}` |

**Limpeza:** dupla, do mesmo jeito que o R-02 já usa (seção 2.11) — o nó 0
deste próprio workflow limpa no caminho em que a cadência volta a andar (uma
tentativa nova dispara o gatilho de novo), e o nó 4 do Mestre de saída
(seção 3, atualizado nesta rodada) limpa no caminho em que o lead sai de
`CONECTAR`/`open` de vez, pela via normal (o gestor resolve a instância
travada movendo o lead, ou ele sai por outro motivo enquanto isso). **Caso
não coberto por nenhum dos dois, documentado e não escondido:** se o
gestor remover `fila-tel`/`fila-wa` na mão sem o lead nunca mais gerar
tentativa nova nem sair de `CONECTAR`/`open` — ou seja, a instância travada
morreu de vez e ninguém tirou o lead da etapa —, `fila-travada` fica presa
para sempre, sem afetar mais nada (não é checada em nenhum portão da
cadência, só filtra a lista 8.21). Esse cenário-limite é exatamente o que a
peça 3 (seção 2.22), `CONECTAR` sem avanço, existe para pegar — cadência
realmente morta, não só uma tentativa travada.

**Pronto quando (peça 2 do F-05):** `fila-tel`/`fila-wa` presente depois do
fim do dia em que foi aplicada gera aviso ao gestor sozinho, sem depender
de alguém abrir a fila do dia e notar um contato que não devia mais estar
lá.

---

## 2.22 Monitor de Saúde da Operação — F-05 (peça 3 de N: `CONECTAR` sem avanço)

**Por quê:** a terceira das quatro invariantes que ficaram para depois na
peça 1 (seção 2.20) — e a que a própria peça 2 (seção 2.21, "Caso não
coberto por nenhum dos dois") já apontava como sua vizinha natural:
`fila-tel`/`fila-wa` presa pega a instância que trava **dentro** de uma
tentativa; esta pega a instância que se perde **entre** duas tentativas —
o lead segue em `CONECTAR`/`open`, sem nenhuma tag de fila presa (a peça 2
não acusa nada), e mesmo assim nenhuma tentativa nova nasce. É o sintoma
mais silencioso dos três: nenhuma tag errada, nenhuma tarefa vencida, só um
relógio que parou de bater. Mesma pesquisa de mercado das peças 1 e 2 —
nenhuma das quatro plataformas do enunciado expõe alarme proativo para
"cadência que parou de avançar"; é reporting de engenharia interna.

**Achado ao desenhar — por que "7 dias", o número literal do roadmap, é a
condição errada:** a tabela 2.5 (a régua das 12 tentativas) tem um degrau de
**10 dias corridos** entre T10 (D20) e T11 (D30) — o maior intervalo
planejado da régua inteira, e o único que já passa dos "7 dias" do
enunciado original. Um alerta disparando literalmente aos 7 dias sem
tentativa nova acusaria **todo** lead que chega saudável até o D20, no meio
exato do intervalo mais comprido e mais normal da cadência — o oposto de
"cadência morta". A mesma classe de erro que a peça 2 já cometeu e corrigiu
(relógio relativo confundindo intervalo legítimo com trava real), aqui
achada *antes* de publicar, não depois. Corrigido para **14 dias**: acima do
maior degrau real (10) com folga para o empurrão de dia útil que a seção 2.5
já documenta (janela de expediente pode adiar um `Wait` que cai em fim de
semana), sem chegar perto o bastante de um segundo intervalo real para
confundir os dois.

**Achado de desenho, o segundo — por que o gatilho não é `Opportunity Stage
Changed → CONECTAR`, ao contrário do instinto de copiar a peça 1:** essa
tradução mecânica pareceria óbvia (é o mesmo evento que abre a Cadência
12x30 e a Cadência Inbound, seção 2.1/2.10), mas fica cega para exatamente
o caso do Reengajamento 90 dias (seção 2.12): o nó 5 daquele workflow faz
`Update Opportunity — Etapa → CONECTAR`, só que a oportunidade **já estava**
em `CONECTAR` — por desenho, 12 tentativas esgotadas nunca tiram a
oportunidade da etapa, só mudam `status` (tabela 1.0). Não há fonte
confirmando se o GHL dispara `Opportunity Stage Changed` quando uma ação de
workflow escreve o mesmo valor que o campo já tinha (pesquisado via
`WebSearch`; a documentação oficial descreve o gatilho como reagindo a
"opportunity moves from one stage to another", sem cobrir o caso de
"mesma etapa, escrita de novo" — **nível de confiança baixo o bastante para
não apostar nele**). Se o GHL suprimir o evento nesse caso (cenário mais
provável, e o que a redação da documentação sugere), todo lead reativado
ficaria sem monitor nenhum — o pior resultado possível para uma peça que
existe justamente para pegar o que mais ninguém vê.
**Como:** gatilho por `Tentativa nº` voltando a `0`, não por etapa —
`Tentativa nº` é zerado exatamente nos três pontos em que uma rodada nova de
verdade começa (nó 0.1 da Cadência 12x30, nó 0.1 da Cadência Inbound, nó 3
do Reengajamento), inclusive a reativação. Pesquisado via `WebSearch`
(`help.gohighlevel.com/.../workflow-trigger-contact-changed`): o gatilho
nativo **Contact Changed**, com filtro por **Custom Field**, aceita a
condição "campo igual a um valor" — cobre `Tentativa nº` **igual a** `0`
sem depender de `Opportunity Stage Changed` nem do caso não confirmado
acima. **Nível de confiança médio** (documentação oficial confirma o filtro
por custom field com operador de igualdade; não testado nesta subconta — a
especificação abaixo não muda se o operador exato for "equals" ou
"changed to").

### Gatilho
**Contact Changed** — filtro: Custom Field `Tentativa nº` **igual a** `0`

### Configurações
| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | Cada rodada nova (entrada inicial em `CONECTAR`, handoff do fim da TI5, reativação do Reengajamento) zera `Tentativa nº` e merece seu próprio relógio — mesmo raciocínio já usado no R-02 e nas peças 1 e 2 |
| Janela de envio | Sem janela, 24/7 | Aviso interno ao gestor, mesmo raciocínio das peças 1 e 2 |
| Stop on Response | Desligado | Não há mensagem ao lead aqui |

### Nós
| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Checkpoint | Update Contact Field | `Checkpoint — Tentativa nº` = `{{contact.tentativa_n}}` (o valor no instante do gatilho) |
| 2 | Aguardar | Wait → Time Delay | 14 dias corridos |
| 3 | Portão — ainda em cadência? | If/Else | Etapa da oportunidade **é** `CONECTAR` **E** `status` **é** `open` → segue. Senão → **encerra** (saiu por um caminho normal — nada a avisar) |
| 4 | Portão — avançou? | If/Else | `Tentativa nº` **é diferente de** `Checkpoint — Tentativa nº` → segue para o nó 5 (uma tentativa nova rodou nos últimos 14 dias — régua viva). Senão → segue para o nó 6 (parado) |
| 5 | Novo ciclo — a régua voltou a andar | Remove Contact Tag `conectar-estagnado` → Update Contact Field `Checkpoint — Tentativa nº` = `{{contact.tentativa_n}}` → **voltar para o nó 2** (mesmo padrão de laço já usado nos nós 2.5b/2.5d da seção 2.4 — represa sem sair do workflow, reconsulta 14 dias depois). A remoção da tag é o que tira da lista 8.22 o lead que **se recuperou** — ver nota abaixo |
| 6 | Portão de aviso único | If/Else | tag `conectar-estagnado` **ausente** → segue para o nó 7 (é o primeiro alerta desta parada). **Presente** → pula direto para o nó 9 (já avisado; mantém o laço sem repetir o aviso) |
| 7 | Fila e aviso | Add Contact Tag `conectar-estagnado` → Internal Notification para o gestor: `{{contact.name}} está em CONECTAR sem tentativa nova há pelo menos 14 dias. Tentativa nº atual: {{contact.tentativa_n}}.` |
| 8 | Registro | Add Note | `Alerta de saúde: CONECTAR sem avanço em 14 dias · {{right_now}}` |
| 9 | Continuar vigiando | Update Contact Field | `Checkpoint — Tentativa nº` = `{{contact.tentativa_n}}` → **voltar para o nó 2** |

**Por que o caminho do alerta também volta ao nó 2, e por que o nó 5 remove
a tag (correção de 21/09/2026, antes de montar):** a primeira redação desta
seção terminava no nó 8 — avisava uma vez e encerrava a instância. Isso
deixava a tag `conectar-estagnado` sem nenhuma saída a não ser o nó 4 do
Mestre de saída, que só roda quando o lead **sai de cadência de verdade**.
Consequência: um lead que trava 14 dias, é alertado, e depois volta a
receber tentativas (o SDR retomou, a pausa acabou, o workflow destravou)
ficaria marcado como estagnado **para sempre**, e a lista `Saúde — CONECTAR
Estagnado` (8.22) mostraria uma régua saudável como parada. É a mesma classe
da tag `fila-quente` (seção 4, nó 3b): **aplicada no caminho ruim e removida
só na saída, nunca no caminho da recuperação** — a lista de diagnóstico
apodrece e o gestor para de confiar nela, que é o pior fim possível para um
monitor de saúde.

Com o laço fechado, os três estados ficam corretos sem aviso repetido: parou
→ tag e um aviso (nó 6 garante que é um só); continua parado → nó 6 desvia
para o 9 e o laço segue em silêncio; voltou a andar → nó 5 tira a tag, some
da lista, e o monitor continua vigiando a partir do novo checkpoint. O nó 4
do Mestre de saída continua na lista de limpeza como rede — a tag ainda
precisa sair quando o lead deixa a cadência sem ter se recuperado.

**Por que a comparação por `Checkpoint — Tentativa nº` não repete o erro
"campo com dois donos" que este documento já evitou várias vezes (F-04,
Contador de Toques; a peça 2 descartou explicitamente um campo assim):**
lá o risco era **várias instâncias concorrentes do mesmo workflow**
escrevendo no mesmo campo compartilhado quase ao mesmo tempo (um toque a
cada poucos minutos). Aqui o gatilho só dispara quando `Tentativa nº` volta
a `0` — no máximo três vezes na vida de um lead (entrada inicial, handoff
do fim da TI5, uma reativação), cada disparo bem espaçado dos outros (dias
ou semanas, nunca minutos) — então a escrita do nó 1/5 de uma instância não
compete de verdade com a de outra. **Limite conhecido, documentado e não
escondido:** o handoff do fim da TI5 (seção 2.10) *também* dispara este
gatilho (a 12x30 zera `Tentativa nº` no seu próprio nó 0.1 ao receber o
lead via `Add to Workflow`), então um lead inbound que não responde em 3
dias abre uma **segunda** instância deste monitor além da que já rodava
desde a entrada inbound. Na pior hipótese, a instância mais antiga acorda
14 dias depois do seu próprio início, lê `Checkpoint` já reescrito pela
instância mais nova e conclui "avançou" mesmo sem ter sido ela quem
avançou — um falso "tudo bem" isolado, que **encerra a instância antiga em
silêncio, mas nunca silencia o problema**: a instância mais nova (a que
corresponde ao regime atual do lead, pós-handoff) continua seu próprio
laço de 14 dias, tomando checkpoints corretos a partir do seu próprio
início. Nenhuma trava real de leitura acaba escondida — o pior caso é uma
instância redundante saindo cedo, nunca os dois monitores saindo ao mesmo
tempo sem avisar.

### Campo novo
`Checkpoint — Tentativa nº` (C-27, `campos-e-tags.md`), `NUMERICAL` — existe
só para este workflow comparar consigo mesmo; nenhum outro nó do projeto lê
ou escreve nele, então não herda o risco de "contador com dois donos" que
motivou C-26 a ser tratado com cuidado.

### Limpeza da tag
`conectar-estagnado` se resolve numa saída de cadência de verdade — a
mesma transição que o nó 4 do Mestre de saída (seção 3) já alcança pela via
normal (diferente de `novo-lead-estagnado`, peça 1, que precisou do nó 0
incondicional porque seu caminho de resolução cai no ramo de no-op do nó 1).
Basta somar a tag à lista existente do nó 4 — ver seção 3, abaixo.

**Limite conhecido, o mesmo já citado na peça 2 como o cenário que só esta
peça pega:** se o gestor mover a oportunidade para fora de `CONECTAR`/`open`
na mão sem nenhuma tentativa nova ter rodado, ou se o lead ficar
literalmente esquecido para sempre em `CONECTAR`, esta peça é quem primeiro
denuncia — é o sensor de "cadência realmente morta" que a peça 2 (sensor de
"uma tentativa travada") explicitamente não cobre.

**Escopo depois desta peça:** das seis invariantes originais do "Como" do
F-05 (mais as duas adições de 18/09/2026), três já têm workflow
(`NOVO LEAD` estagnado, `fila-tel`/`fila-wa` presa, `CONECTAR` sem avanço) e
uma foi descartada por já estar coberta (tarefa vencida sem resultado —
peça 1). Restam duas: `nao-perturbe` ainda dentro de workflow ativo e
`Conectado`/`Retorno agendado` vencidos — a última segue dependendo de
"esperar até uma data dinâmica", não testado neste conector; a primeira é
candidata à peça 4.

**Pronto quando (peça 3 do F-05):** uma oportunidade em `CONECTAR`/`open`
sem tentativa nova em 14 dias corridos gera aviso ao gestor sozinho, sem
depender de outra sessão notar o número na mão — o mesmo tipo de estrago
silencioso que o G-03 só foi achado porque alguém olhou o dado direto.

---

## 2.23 Monitor de Saúde da Operação — F-05 (peça 5 de 6: `AGENDAR` sem fechar o loop) — F-05 fechado

**Por quê:** a invariante que a "Adição de 18/09/2026" do roadmap
acrescentou ao F-05 original, ao aplicar o tempo de estagnação do Sales
Model Canvas etapa a etapa: `Conectado` (hoje `AGENDAR`, tabela 1.0) sem
avançar para `Reunião agendada` (`NEGOCIAR`) em mais de 24h — o SDR atendeu
o lead, ganhou a tarefa `[CONECTADO] Qualificar e agendar` (seção 4, ramo
`Atendeu`, nó 8), e nunca fechou o loop: não agendou, não descartou. É a
mesma classe de estrago silencioso das peças 1-3 (nada avisa sozinho), aqui
na etapa em que L-08 (`briefing-sdr.md`) já tinha achado que falta caminho
de saída para "sem fit" — este monitor não fecha essa lacuna sozinho (quem
fechou foi o ramo `Desqualificado` do Pós-ligação, R-18, 21/09/2026, que
tira a maioria dos "sem fit" **antes** de chegar aqui), só garante que quem
ainda assim ficar parado em `AGENDAR` (fit real, sem horário fechado, ou
desqualificado na mão já dentro da etapa) não fica sem ninguém saber.

Mesma pesquisa de mercado das peças 1-3: nenhuma das quatro plataformas do
enunciado do projeto (Reev, Meetime, Outreach, Salesloft) expõe alarme
proativo para "lead conectado sem próximo passo fechado" — é reporting de
engenharia interna, não recurso de sales engagement.

**Desenho:** mesmo padrão de relógio por evento já validado em R-02 e na
peça 1 (seção 2.20) — gatilho de chegada, `Wait` de 24h, portão que confere
se o lead ainda está preso antes de avisar. `AGENDAR` só é alcançada uma vez
por ciclo (o Pós-ligação, seção 4, ramo `Atendeu`, nó 6, é o único nó que
move uma oportunidade para lá), então não tem o risco de eventos repetidos
em menos de 24h que motivou o relógio ancorado por horário fixo da peça 2 —
o `Wait` relativo de 24h, o mesmo mecanismo da peça 1, basta.

### Gatilho
**Opportunity Stage Changed** — Pipeline `FUNIL DE VENDAS` · Para a etapa:
`AGENDAR`

### Configurações
| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | Cada entrada em `AGENDAR` merece seu próprio relógio, mesmo raciocínio da peça 1 |
| Janela de envio | Sem janela, 24/7 | Aviso interno ao gestor, não mensagem ao lead |
| Stop on Response | Desligado | Não há mensagem ao lead aqui |

### Nós
| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Aguardar | Wait → Time Delay | 24 horas corridas |
| 2 | Portão | If/Else | Etapa da oportunidade **ainda é** `AGENDAR` **E** `status` **é** `open` → segue (24h depois de atender, ninguém fechou o loop). Senão → **encerra** (agendou, foi descartado na mão, ou saiu por outro caminho — nada a avisar) |
| 3 | Fila | Add Contact Tag | `agendar-estagnado` |
| 4 | Aviso | Internal Notification | Para o gestor: `{{contact.name}} atendeu e está há mais de 24h em AGENDAR sem reunião marcada nem desqualificação. Conectado em: {{contact.data_conectado}}.` |
| 5 | Registro | Add Note | `Alerta de saúde: AGENDAR sem fechar o loop em 24h · {{right_now}}` |

**Limpeza da tag — por que entra no nó 0 do Mestre de saída (incondicional),
não só na lista nomeada do nó 4 (achado ao desenhar):** o caminho normal de
saída de `AGENDAR` (o Pós-agendamento move para `NEGOCIAR`, seção 5, nó 1)
já aciona o nó 4 do Mestre de saída pela via comum — `NEGOCIAR` não está na
lista de no-op do nó 1 ("`status` é `open` **e** etapa é uma de `NOVO LEAD`,
`CONECTAR`"), então bastaria somar a tag à lista existente, como
`fila-travada` e `conectar-estagnado` já fazem. Mas L-08 (`briefing-sdr.md`)
registra que hoje não existe caminho formal de desqualificação a partir de
`AGENDAR` — se algum dia alguém arrastar a oportunidade de volta para
`CONECTAR` na mão (o único jeito manual de "desistir" sem esse caminho), a
condição do nó 1 volta a ser verdadeira (`CONECTAR`/`open`) e o Mestre de
saída trataria essa transição como no-op, a mesma classe de bug que já
motivou o nó 0 incondicional para `novo-lead-estagnado` (seção 2.20).
Somar `agendar-estagnado` ao nó 0 (em vez de só ao nó 4) cobre os dois
caminhos de uma vez, sem custo: `Remove Contact Tag` de quem não tem a tag
não faz nada, e o Mestre de saída já roda a cada mudança de etapa ou status.

**Pronto quando (peça 5 do F-05):** um lead atendido que fica mais de 24h em
`AGENDAR` sem virar reunião marcada nem sair por outro caminho gera aviso ao
gestor sozinho.

---

## 2.24 Monitor de Saúde da Operação — F-05 (peça 6 de 6: retorno prometido e vencido) — F-05 fechado

**Por quê:** a segunda invariante da mesma "Adição de 18/09/2026" — `Retorno
agendado` (hoje: oportunidade em `CONECTAR` com `Resultado da tentativa` =
`Pediu retorno`, tabela 1.0) com `Data de retorno` (S-01) vencida sem nova
classificação. É a promessa mais fácil de esquecer da operação: o SDR marca
`Pediu retorno`, a tarefa `[RETORNO]` nasce (seção 4, ramo `Pediu retorno`,
nó 4), e se ninguém abrir a lista `Retornos` (8.4) no dia certo, a data passa
em silêncio — o lead mais alto em `Prioridade` (5) da operação vira o mais
esquecido, mesma classe de risco que a lição do `fila-quente`
(`APRENDIZADOS-CRM.md`, "Conte onde a tag é aplicada e onde é removida") já
descreveu para fila que não expira.

**Isto era o único bloqueio real do F-05 até esta rodada — resolvido:** as
peças 1-3 usaram relógio por evento (`Wait` relativo ou até horário fixo do
dia); esta invariante precisa de "esperar até uma data que muda por lead",
registrada como não testada neste conector desde a peça 1. Pesquisado via
`WebSearch` nesta rodada (documentação oficial da HighLevel bloqueada pelo
proxy deste ambiente, como sempre — a pesquisa lê o resultado de IA sobre a
página de suporte, não a página em si): o nó `Wait` do GHL tem uma opção
**Dynamic** (ao lado de **Standard**, valor fixo) que "lê a data de um campo
do contato em tempo de execução" — o texto aparece **idêntico, palavra por
palavra**, em duas buscas independentes (mesma citação do artigo oficial
"Workflow Wait Action Setup and Options"), reforçado por um changelog da
própria HighLevel ("Wait Action: Major Revamp") anunciando a funcionalidade
e por um guia de terceiro (`consultevo.com`, não acessível para ler o corpo
inteiro — proxy bloqueia o domínio, mas aparece na busca). **Nível de
confiança médio-alto:** mais alto que o padrão "uma fonte de IA sobre
documentação" já usado neste projeto (peça 3, R-17) porque a citação bateu
palavra por palavra em buscas diferentes, sinal de que é o texto real do
artigo e não uma paráfrase; ainda médio, não alto, porque nenhuma tela desta
subconta confirmou o comportamento.

### Gatilho
**Contact Changed** — filtro: Custom Field `Data de retorno` **alterado**
(qualquer valor novo, não um valor fixo — diferente da peça 3, que comparava
`Tentativa nº` contra `0`). **Por que este operador, e por que a confiança
aqui é maior que a da peça 3 para o mesmo tipo de dúvida ("dispara quando
escreve o mesmo valor?"):** o Pós-ligação (seção 4) já usa exatamente este
tipo de filtro — "`Resultado da tentativa` foi alterado" — **em produção,
com 24 execuções confirmadas** (`APRENDIZADOS-CRM.md`, "Diagnóstico por
contador vizinho"). Diferente daquele campo (`SINGLE_OPTIONS`, um SDR pode
em tese escrever o mesmo resultado duas vezes seguidas), `Data de retorno`
é uma data escolhida pelo SDR a cada nova ligação de retorno — reescrever o
**mesmo dia exato** numa promessa renovada é a mesma classe de coincidência
rara que a peça 3 já aceitou como limite conhecido, não um caso comum a
proteger.

### Configurações
| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | Cada nova data de retorno (a primeira promessa, ou uma renovada depois de o SDR ligar de novo) merece seu próprio relógio |
| Janela de envio | Sem janela, 24/7 | Aviso interno ao gestor |
| Stop on Response | Desligado | Não há mensagem ao lead aqui |

### Nós
| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Checkpoint | Update Contact Field | `Checkpoint — Data de retorno` = `{{contact.data_de_retorno}}` (o valor no instante do gatilho) |
| 2 | Aguardar | Wait → Until specific time, **Dynamic** | Data = `{{contact.checkpoint__data_de_retorno}}` (**dois** underscores — o campo foi criado na tela em 21/09/2026 23:33 e o travessão do nome virou nada, deixando os dois espaços como dois underscores; ver nota abaixo) · horário `19:00` (mesma folga de 30 min depois do fim do expediente, 18:30, já usada na peça 2 — dá o dia inteiro para o SDR ligar antes do alerta) |
| 3 | Portão — a promessa ainda é a mesma? | If/Else | `Data de retorno` (valor atual) **é igual a** `Checkpoint — Data de retorno` → segue (ninguém renovou a promessa desde que este relógio começou). Senão → **encerra** (o gatilho já disparou de novo com a data nova — outra instância está vigiando o valor certo) |
| 4 | Portão — ainda pendente? | If/Else | `Resultado da tentativa` **é** `Pediu retorno` **E** etapa **é** `CONECTAR` **E** `status` **é** `open` → segue (a data passou sem reclassificação). Senão → **encerra** (o SDR já ligou de volta e classificou por outro caminho, ou o lead saiu de cadência) |
| 5 | Fila | Add Contact Tag | `retorno-vencido` |
| 6 | Aviso | Internal Notification | Para o gestor: `{{contact.name}} tinha retorno prometido para {{contact.data_de_retorno}} e ainda não foi reclassificado.` |
| 7 | Registro | Add Note | `Alerta de saúde: retorno vencido sem nova classificação · {{right_now}}` |

**Chave real dos dois campos Checkpoint, lida do CRM em 22/09/2026 — não
adivinhe pelo nome:**

| Nome na tela | `fieldKey` real |
|---|---|
| `Checkpoint — Tentativa nº` | `contact.checkpoint__tentativa_n` |
| `Checkpoint — Data de retorno` | `contact.checkpoint__data_de_retorno` |

O GHL **remove** o travessão (`—`) em vez de transliterar, e os dois espaços
que o cercavam sobram como **dois underscores seguidos**. É a mesma mecânica
que já tinha comido os acentos (`conexão` → `conexo`, `anúncios` → `anncios`
— `APRENDIZADOS-CRM.md`), agora com pontuação. Esta seção nasceu com
`checkpoint_data_de_retorno`, um underscore, escrita antes de o campo existir
na tela; corrigido em 22/09 pela auditoria de merge field órfão. **Nome com
travessão, dois pontos ou parêntese: crie na tela primeiro, leia o
`fieldKey` por API, e só então escreva o merge field no documento.**

**Por que o Checkpoint compara valor, não usa o campo vivo direto no
portão do nó 3 (mesma lição da peça 3, `Checkpoint — Tentativa nº`):** entre
o gatilho e o dia do vencimento, o SDR pode ter ligado de novo e renovado a
promessa para uma data mais distante — a instância antiga, se comparasse o
campo vivo, leria a data nova e concluiria "ainda pendente" no dia errado. O
Checkpoint congela o valor que **esta** instância deve vigiar; se o campo
vivo já é outro, uma instância mais nova (disparada pelo mesmo gatilho
quando a data mudou) está cuidando do valor certo, e esta encerra em
silêncio.

**Por que a recorrência do campo não repete o risco de "contador com dois
donos" (F-04, e a peça 2 descartando um desenho parecido):** `Data de
retorno` muda no máximo poucas vezes na vida de um lead (uma promessa, e
raramente uma renovação), sempre espaçada por dias — não escrita dezenas de
vezes por dia como `toque`. Mesmo raciocínio já generalizado na peça 3
(`APRENDIZADOS-CRM.md`, "Nem todo campo compartilhado é um 'contador com
dois donos'").

### Campo novo
`Checkpoint — Data de retorno` (C-28, `campos-e-tags.md`), `DATE` — existe só
para este workflow comparar consigo mesmo, mesmo raciocínio de C-27 (peça 3):
nenhum outro nó do projeto lê ou escreve nele.

### Limpeza da tag — dois caminhos, porque o caminho comum de recuperação nunca muda de etapa
**Achado ao desenhar, o mais importante desta peça:** o caminho mais comum
pelo qual esta invariante se resolve é o SDR ligar de volta e marcar
`Resultado da tentativa` de novo — `Atendeu`, `Não atendeu`, `Número
errado`, `Não ligar`, ou até um novo `Pediu retorno` com data futura. Três
desses cinco (`Não atendeu`/ramo idêntico, `Pediu retorno` de novo) **não
mudam etapa nem `status`** (o lead continua em `CONECTAR`/`open` — seção 4,
ramos `Caixa Postal`/`Não atendeu` e `Pediu retorno`) — o que significa que
o Mestre de saída **nunca dispara** nesse caminho, porque seu gatilho é
`Opportunity Stage Changed`/`Opportunity Status Changed`, nenhum dos dois
acontece aqui. Somar `retorno-vencido` só à lista do nó 4 do Mestre de
saída (o mesmo tratamento de `fila-travada`/`conectar-estagnado`) deixaria a
tag presa para sempre no caso mais comum de recuperação.

**Resolvido com um nó novo no Pós-ligação, não no Mestre de saída:** o
próprio gatilho do Pós-ligação (`Resultado da tentativa` alterado) é a
definição operacional de "o SDR agiu sobre o lead" — mesmo raciocínio já
usado para a limpeza de `fila-quente` no nó 3b daquele workflow
(`APRENDIZADOS-CRM.md`, "Conte onde a tag é aplicada e onde é removida").
Um nó novo, **3c**, logo depois do 3b e antes do nó 4 (a ramificação pelos 6
resultados) — `Remove Contact Tag: retorno-vencido`, incondicional, roda
qualquer que seja o resultado novo, inclusive um `Pediu retorno` renovado
(a tag sai e, se a data mudou, uma instância nova deste monitor já está
vigiando o valor novo desde o nó 1). O nó 4 do Mestre de saída continua
com `retorno-vencido` na lista, como rede de segurança para o caso raro em
que o lead sai de `CONECTAR`/`status open` por um caminho que não passa pelo
Pós-ligação (ex.: movimento manual de etapa na tela).

**Retoque de tela, os dois — Pós-ligação e Mestre de saída estão
publicados:** linhas novas na tabela de `GUIA-MONTAGEM.md`.

**Escopo depois desta peça — F-05 fechado:** das seis invariantes originais
do "Como" do F-05 (mais as duas adições de 18/09/2026), todas têm tratamento
agora: `fila-tel`/`fila-wa` presa (peça 2), `CONECTAR` sem avanço em 14 dias
(peça 3), tarefa vencida sem resultado (descartada — já coberta pelo nó 10b
da seção 2.4), `nao-perturbe` em workflow ativo (peça 4, por prevenção em vez
de detecção), `AGENDAR` sem fechar o loop em 24h (peça 5) e retorno vencido
sem reclassificação (esta peça). Mais `NOVO LEAD` esquecido (peça 1, achada
fora da lista original via G-03). Não sobra invariante do F-05 sem
workflow — o item fica fechado como bloco, não só peça a peça.

**Pronto quando (peça 6 do F-05, e do F-05 inteiro):** um retorno prometido
que vence sem o SDR ligar de volta gera aviso ao gestor sozinho, sem
depender de alguém abrir a lista `Retornos` (8.4) no dia certo.

---

## 2.25 Proteção de reputação do número de WhatsApp — F-07

**Por quê:** todo o desenho de mensagem desta operação (G-05, G-06)
protege a **entrega** de cada mensagem — janela de 24h, Template aprovado.
Nenhum item protege o **número** que envia. A Meta atribui a todo número do
WhatsApp Business API uma **Quality Rating** (Verde/Amarela/Vermelha,
calculada sobre bloqueios, denúncias de spam e baixo engajamento dos
últimos 30 dias) e um **Tier de mensagens** (teto de clientes únicos
contactados por uma janela rolante de 24h — número novo nasce no Tier 1,
250 clientes únicos, e só sobe consumindo metade do teto atual dentro de 7
dias com qualidade aceitável). Uma rajada de bloqueios ou denúncias derruba
a nota para Amarela/Vermelha, trava a subida de Tier e pode **throttlar ou
recusar** mensagens mesmo dentro da janela de 24h e mesmo com Template
aprovado — o mesmo "estrago silencioso" que motivou o F-05 e o G-05/G-06,
aqui na camada mais funda: se o número perder reputação, toda a
especificação de mensagem do projeto (M1-a/M1-b/M2/M3, MI-0/MI-F, RE-1/
RE-2, NS-1/NS-2, os quatro lembretes do Pós-agendamento, QI-1 e o
Caminho B da Qualificação por IA) para de entregar ao mesmo tempo, sem
nenhum erro visível numa tela de workflow — o nó roda, "envia", e a Meta
descarta ou atrasa do outro lado. É o equivalente, para WhatsApp, do que
"aquecimento de domínio"/monitoramento de spam score é para e-mail em
Outreach/Salesloft — nenhuma das duas ferramentas de sales engagement
citadas neste projeto lida com WhatsApp Business API como canal principal,
então aqui o risco é maior do que a paridade com elas sugere, não menor.
**Pesquisado (`WebSearch`, confiança média-alta — mecânica confirmada por
múltiplas fontes de terceiros e pela documentação de suporte da própria
HighLevel, cujo domínio segue bloqueado pelo proxy deste ambiente, citada
por resultado de busca, não lida direto):** o artigo "WhatsApp Quality
Rating, Status Changes, and Messaging Limits" do HighLevel Support Portal
confirma que a mecânica de Meta se aplica sem alteração dentro do GHL —
não é um risco só de quem usa a API da Meta direto.

**O que este item NÃO é, para não duplicar outro:** não é o teto de fadiga
do F-04 (`Toques na semana`), que protege o **lead** de receber toque
demais — um número pode ter reputação perfeita e ainda assim cansar um
lead, e um número pode respeitar o teto de F-04 lead a lead e ainda
acumular denúncia suficiente para cair de nota, porque a Quality Rating
soma bloqueios de **todos** os leads, não de um só. Também não é a higiene
de telefone do R-13 (`telefone-invalido`), que filtra número que não existe
— aqui o número do **lead** está certo, o risco é a reação dele à
mensagem. É uma peça nova, na mesma família do F-05 (monitor de saúde),
mas de infraestrutura do canal, não de lead individual.

**Como — e por que não é um workflow:** pesquisado explicitamente se existe
gatilho, ação ou Custom Value nativo do GHL que leia Quality Rating ou Tier
em tempo de execução (para um workflow reagir sozinho, no espírito do F-05)
— **não encontrado**. A tela nativa (`Settings → WhatsApp → Manage` no
número conectado, "Quality rating" dos últimos 30 dias, com os motivos de
bloqueio ao passar o mouse quando a nota cai) é a única superfície, e o
conector `GHL CRM` desta sessão não a expõe (sem ferramenta de leitura de
canal/número — confirmado pela lista de ferramentas disponíveis). Isto não
é lacuna deste item, é limite de plataforma/conector como qualquer outro
já registrado no projeto (campo e workflow por API, por exemplo) — a saída
correta não é inventar um workflow que a tela não sustenta, é registrar a
checagem como rotina manual do gestor, com gatilho por evento (quando
olhar) em vez de por calendário fixo:

| Quando olhar | Por quê |
|---|---|
| **Antes de publicar os 4 nós de envio da Cadência 12x30 pela primeira vez com volume real** (G-05, passo 4 da tabela da seção G-05 no roadmap) | É o salto de volume mais brusco da operação — de zero para o regime diário de uma hora para a outra; se a nota já não é Verde antes disso, o salto piora rápido |
| **Semanalmente enquanto o volume crescer** (10-13 leads novos/dia entrando, mais Reengajamento 90 dias, mais Cadência Inbound) | O teto de Tier 1 (250 clientes únicos/24h) tem folga larga no volume atual do projeto — o risco não é estourar o teto, é a nota cair antes de precisar subir de Tier |
| **Depois de qualquer pico visível na lista `Opt-out por Palavra-chave` (R-17, seção 2.9.5)** | Quem digita "pare" na conversa é o mesmo tipo de reação que gera denúncia/bloqueio no WhatsApp — um pico na lista de opt-out por texto é sinal antecedente barato de checar a nota antes que ela caia sozinha |

**O risco concreto que este projeto tem hoje, e que os três gatilhos acima
não pegam (achado em 22/09/2026, ao cruzar este item com o G-03):** o estoque
do G-03 são **47 leads parados**, e a opção 3 daquele item é promovê-los **de
uma vez**. Some isso a um número de WhatsApp recém-ativado e ao primeiro dia
da `Cadência 12x30` no ar: a M1 sairia como Template para ~47 pessoas que
nunca escreveram para este número, **todas no mesmo dia, sem nenhum
histórico de conversa no número**. Não é problema de Tier (47 cabe folgado no
teto inicial); é o pior começo possível de **Quality Rating** — burst frio de
mensagem business-initiated é exatamente o padrão que gera bloqueio e
denúncia, e bloqueio nos primeiros dias pesa mais, porque a nota é calculada
sobre os últimos 30 dias e não há volume bom para diluir.

**A correção é de graça e já está no briefing:** o regime normal da operação
é **~10-13 leads novos por dia** (`briefing-sdr.md`, entrada e L-05). Promover
o estoque em lotes desse tamanho — em vez de 47 de uma vez — espalha o
primeiro volume de Template por 4 dias, é o mesmo ritmo que o SDR vai ter
quando a régua estabilizar, e não exige mecanismo nenhum: é a ordem em que o
dono clica. Quem promover os 47 de uma vez ganha um dia de fila cheia e
arrisca o canal inteiro pelas 4 semanas seguintes.

**Se a nota cair para Amarela/Vermelha (mitigação com o que o projeto já
tem, sem desenho novo):** (1) parar de promover leads novos para a
Cadência 12x30 até a nota normalizar não é necessário — os quatro nós de
envio já têm a guarda de janela (G-05/G-06): a maioria dos envios já sai
como Template, que a Meta trata com mais tolerância que texto livre; (2)
revisar os motivos de bloqueio que a tela mostra por cima da nota — se
apontarem para um Template específico (ex.: `M1-b`, a variante do R-05/
teste A/B), pausar só aquela variante no Split em vez do canal inteiro;
(3) conferir se o pico de opt-out (gatilho da linha acima) aponta para um
segmento ou origem específica, e se sim, tratar a causa (ex.: formulário do
Meta mal configurado, G-04) em vez de só a reputação, porque a nota volta a
cair de novo enquanto a causa não for corrigida.

**Zero campo, zero tag, zero workflow, zero escrita no CRM:** item de
documentação e rotina manual pura — não depende de `APROVADO.md`. Não
entra na "Ordem de montagem" (não há nó para montar) nem no checklist de
teste da seção 10 (não há objeto de CRM para simular reputação de número
com contato fictício).

**Pronto quando:** o gestor sabe, sem perguntar a ninguém, os três
momentos em que precisa olhar `Settings → WhatsApp → Manage` antes que a
nota caia em silêncio — e o que fazer, com as peças que o projeto já tem,
se ela cair.

---

## 2.26 Proteção de reputação do número de telefone — F-08

**Por quê:** o F-07 fechou a proteção de infraestrutura para o WhatsApp
(Quality Rating da Meta); o canal **majoritário** da cadência — ligação por
telefone, tabela 2.5, que carrega 8 dos 12 toques e é o único canal que o
SDR controla direto — segue sem proteção nenhuma de reputação de número. E
o risco deixou de ser hipótese exatamente na semana em que esta rodada
roda: desde agosto/2026 a Anatel obriga toda operadora brasileira a
oferecer, **grátis e ativado por padrão** para todo cliente, um sistema
próprio de bloqueio de chamadas "abusivas" — cada operadora escolhe a
tecnologia, mas o critério que a norma manda considerar é **quantidade e
duração das chamadas** (`WebSearch`, confiança média-alta: a mesma
descrição — "quantidade e duração", "gratuito e ativado por padrão" —
apareceu em várias matérias independentes cobrindo a mesma normativa de
agosto/2026, sinal de que estão citando o texto oficial da Anatel, não
parafraseando cada uma à sua maneira; domínio `gov.br/anatel` não testado
direto neste ambiente, mesma limitação de proxy já registrada para
`help.gohighlevel.com`). **Meta do SDR: 100 ligações/dia** (`briefing-sdr.md`,
"A máquina") de um número que, quando não atende, gera uma tentativa curta
e sem duração — exatamente o par "muita quantidade, pouca duração" que o
próprio critério da norma aponta como sinal de abuso, não a exceção.

**Por que este item não é "aplicar a mesma solução do F-07 num canal
diferente" — achado ao pesquisar antes de desenhar, como o próprio roadmap
manda:** a saída óbvia, copiada de mercado americano (Reev/Meetime não
cobrem isso — nenhuma das quatro plataformas de referência deste projeto
trata reputação de número de voz como funcionalidade própria, mesma lacuna
de repertório já registrada para o F-07), seria o recurso nativo do
HighLevel para isto, **Voice Integrity** (`Settings → Phone Numbers →
Trust Center`), que registra o número junto a empresas de análise de
identificador de chamada (First Orion, Hiya, TNS) para remover rótulo de
"Spam Likely". **Ele não serve aqui:** a própria documentação de suporte da
HighLevel e cobertura de terceiros são explícitas — "Voice Integrity
(Labs, **US only**)", e o pré-requisito é registro **SHAKEN/STIR**, um
framework da FCC americana com EIN, que não existe para número brasileiro.
Copiar a receita americana sem checar a letra miúda teria produzido uma
especificação que nunca funcionaria para esta subconta — o mesmo tipo de
erro que motivou registrar, em `APRENDIZADOS-CRM.md`, a regra de nunca
supor rótulo ou campo sem confirmar contra a fonte certa.

**Um segundo caminho pesquisado e também descartado, para não ser
retentado à toa numa rodada futura:** o "Não Me Perturbe" da Anatel (a
plataforma nacional de opt-out por CNPJ) **não se aplica a este negócio**.
Fontes independentes convergem: a obrigatoriedade de adesão, inclusive a
ampliação de agosto/2025–2026, alcança **só prestadoras de serviço de
telecomunicações** — cerca de 32% das ligações indesejadas do país; os
outros dois terços, de outros setores econômicos (o desta operação
incluído, uma agência vendendo serviço de marketing), ficam fora do
alcance daquela plataforma especificamente. Não confundir com o
`nao-perturbe` interno do projeto (tag e campo `Permissão WhatsApp`, DND
por contato, R-14/R-17) — são mecanismos diferentes, o interno continua
valendo e não muda com este achado.

**Como — e por que também não é um workflow, mesmo motivo do F-07:**
nenhuma API pública de operadora brasileira nem do GHL expõe "este número
foi rotulado/bloqueado por algum cliente" para um workflow ler — o
bloqueio acontece no aparelho ou na rede do lead, não em nada que a
subconta enxergue. Vira checklist do gestor, não automação:

| Ação | Por quê |
|---|---|
| **Cadastrar o(s) número(s) usado(s) para ligar no portal gratuito "Qual Empresa Me Ligou?" da Anatel** (`qualempresameligou.com.br`, associa o número ao CNPJ) | Equivalente brasileiro real do Branded Caller ID/CNAM — quando o lead pesquisa o número desconhecido antes de decidir atender, encontra o nome e o CNPJ da empresa em vez de nada, reduzindo a chance de ele ignorar ou denunciar por puro desconhecimento |
| **Antes de escalar volume** (promover o estoque do G-03, ou ao entrar o 2º SDR do R-10) — **distribuir as ligações entre mais de um número**, em vez de concentrar 100/dia num só | A norma não publica um limiar numérico próprio ainda (cada operadora escolhe a tecnologia); a referência de mercado (fora do Brasil, adaptada com cautela) fica em torno de 50-75 chamadas/dia por número antes do risco de rótulo subir — a meta desta operação, sozinha, já está no teto ou acima dele |
| **Se a taxa de atendimento de um número cair de forma abrupta e sem explicação de horário/segmento** (o mesmo tipo de sinal que o F-06, quando destravar, vai medir por duração de chamada) | É o sintoma prático de bloqueio silencioso — a norma de agosto/2026 não obriga a operadora a avisar o autor da ligação, só o destinatário |
| **Usar o canal de contestação que a norma de agosto/2026 passa a exigir de toda operadora** ("procedimento específico para usuários que tiveram chamadas bloqueadas solicitarem revisão") | Existe agora um caminho formal para reverter um bloqueio de número legítimo — antes de agosto/2026 isso dependia só de boa vontade da operadora |

**Pendência que este item não resolve, registrada em vez de inventada:**
não há confirmação em nenhum documento do projeto se as 100 ligações/dia
saem por **LC Phone** (telefonia nativa do GHL, back-end Twilio) ou pela
linha própria do SDR — `grep` por `LC Phone`/`Twilio`/`discador` em todo o
`wesales/` só encontra uma menção lateral (seção 2.17, sobre call tracking
do F-06), nunca uma afirmação do canal real. A mitigação muda: número
provisionado pelo GHL é o dono técnico registrar; linha própria do SDR
exige registro pelo próprio SDR ou pela operadora dele. Confirmar isso é
pré-requisito prático do primeiro item da tabela acima, não deste item
inteiro — o achado da norma e a exclusão do "Não Me Perturbe" valem
independente da resposta. **Evidência indireta reavaliada em 22/09/2026, mesma data — o CRM não
responde esta pergunta:** `locations_get-location` mostra
`saasSettings.twilioRebilling = { enabled: true, markup: 20 }`, mas o markup
do rebilling é definido **global na agência** (SaaS Configurator), com
override opcional por subconta — o valor lido aqui é compatível com o global
herdado, igual em subconta que nunca ligou, então **não é sinal de número
provisionado nesta**. E a evidência direta, lida na mesma rodada, aponta para
o outro lado: **zero registro de chamada** nas 50 conversas da subconta
(41 atividade de CRM, 9 DM de Instagram, nenhum `TYPE_CALL`) — o contato de
teste com `Tentativas telefone` = 24 tem **uma** mensagem, "Opportunity
created". Os 24 são escritas de campo por classificação manual, não ligações.
A ausência não desempata (pode não haver número, ou haver e nunca ter sido
usado), mas **elimina o CRM como fonte**: é pergunta para o dono, e nenhuma
rodada deve gastar mais tempo procurando por API. Detalhe em
`APRENDIZADOS-CRM.md`, "O CRM não pode responder a pergunta do LC Phone".

**Zero campo, zero tag, zero workflow, zero escrita no CRM:** item de
documentação e rotina manual pura — não depende de `APROVADO.md`. Não
entra na "Ordem de montagem" (não há nó para montar) nem no checklist de
teste da seção 10 (não há objeto de CRM para simular bloqueio de operadora
com contato fictício) — mesmo tratamento do F-07.

**Pronto quando:** o(s) número(s) reais da operação estão cadastrados no
"Qual Empresa Me Ligou?"; o gestor sabe que não pode copiar o Voice
Integrity da HighLevel (US only) nem contar com o "Não Me Perturbe" (não
alcança este setor) como proteção; e sabe, antes de escalar volume, que
concentrar 100 ligações/dia num único número é o próprio risco que a norma
de agosto/2026 existe para pegar.

### Correção do F-08, 22/09/2026 (mesma rodada, verificação): SHAKEN/STIR **existe** no Brasil, e a asfixia do canal está dentro da própria cadência

Três coisas mudaram depois de conferir as fontes uma a uma. A conclusão
prática do F-08 ("o telefone não tem proteção de reputação neste projeto")
continua certa; duas das premissas, não.

**1. A premissa "SHAKEN/STIR não existe para número brasileiro" está
errada.** Existe, e em produção: chama-se **`Origem Verificada`**, é a
implementação brasileira de STIR/SHAKEN + RCD, gerida pela ABR Telecom pelo
**Portal AIA** (Autoridade de Identificação e Autenticação), com **52+
prestadoras** aderidas (Vivo, Claro, Oi, TIM entre elas) e cerca de **6
bilhões de chamadas autenticadas por mês em agosto/2026 — ~30% do tráfego
nacional**. O que ela faz é exatamente o que o F-08 disse não existir por
aqui: mostra **nome, logo e motivo da chamada** na tela de quem recebe, com
selo de autenticidade.

O erro de conclusão que isso causou: o F-08 apresenta o portal **"Qual
Empresa Me Ligou?"** como "equivalente brasileiro real do Branded Caller
ID". Não é o equivalente — é o plano B. Ele depende de o lead **procurar** o
número desconhecido antes de decidir; a `Origem Verificada` entrega a
identificação **antes** da decisão, na própria tela da chamada. Os dois
continuam valendo, em ordem invertida: a `Origem Verificada` é o alvo, o
"Qual Empresa Me Ligou?" é o que dá para fazer hoje de graça.

| O que é | Vale para esta operação? |
|---|---|
| **Obrigatória** para quem origina **mais de 500 mil chamadas/mês** (bancos, call centers, recuperação de crédito, grande varejo) | **Não.** 100 ligações/dia ≈ **2.200/mês** — três ordens de grandeza abaixo |
| Obrigação geral para todos, com prazo de três anos | Alvo em torno de **outubro/2028**: dá tempo, mas a data existe |
| Contratação: pelo site `origemverificada.com.br`, assinando os Termos de Acesso e o pedido de acesso ao Portal AIA; informa CNPJ, dados cadastrais, representantes legais e faturamento; documentos (cartão CNPJ, inscrição estadual, termo de acesso); **ABR Telecom responde em 5 dias úteis** | O caminho é documentado e a papelada é de porte pequeno |
| **Ressalva medida:** nesta fase inicial a contratação é descrita como aberta a **empresas de grande volume de chamadas** | **Pode ser recusada por volume.** Vale pedir de todo jeito — é um formulário e 5 dias úteis, e um "não" hoje já dá a data para voltar |

`Voice Integrity` da HighLevel segue descartada, e pelo motivo certo: ela
registra em First Orion/Hiya/TNS com SHAKEN/STIR **americano** (EIN, FCC),
e é `US only` na própria documentação. O que não vale é a generalização —
"não há SHAKEN/STIR para o Brasil" — que vinha embutida.

**2. O critério da norma é mais largo que "quantidade e duração", e é aí que
a cadência deste projeto se encaixa mal.** O ato é o **Despacho Decisório nº
82/2026/RCTS/SRC, de 17/08/2026**. Além de volume e duração, ele autoriza a
prestadora a considerar:

| Critério da norma | O que a cadência 12x30 produz |
|---|---|
| **Proporção de chamadas de curtíssima duração** | `Não atendeu` e `Caixa Postal` são, por definição, chamadas curtíssimas — e são os **dois únicos** resultados que o nó 10 (seções 2.4 e 2.10) manda **insistir** |
| **Duração média das chamadas** | Puxada para baixo pelo mesmo motivo, em toda tentativa que não conecta |
| **Taxa de completamento** | 8 toques de telefone por lead numa base fria derrubam esta taxa por desenho |
| **CNAE de quem origina** | Agência vendendo serviço de marketing. Nada a fazer, mas é entrada do cálculo — vale saber |
| Volume de chamadas | O que o F-08 já tratou (a linha dos 50-75/dia por número) |

Ou seja: a norma não mede só **quantas** ligações saem, mede **como elas
terminam**. E o "como terminam" é decisão de cadência, não de infraestrutura.

**3. O achado que fecha o item — a proteção já existe neste projeto, só não
para o telefone.** O seletor de canal (nó 4 da seção 2.4; nó 3 da 2.10) tem
esta condição:

> Ramo WA: `Permissão WhatsApp` é `Sim` **E** `WA não atendidas seguidas` **< 2**

Isto é uma proteção de canal: duas mensagens de WhatsApp seguidas sem
resposta e o lead **sai** daquele canal. **Não existe gêmeo de telefone.**
Conferido por `grep` em todo o `wesales/`: `WA não atendidas seguidas` é o
único contador de "seguidas" do projeto, e nenhum campo, nó ou portão conta
ligações não atendidas consecutivas. O resultado é a assimetria exata ao
contrário do risco:

| Canal | Toques na régua | Protege-se depois de… |
|---|---|---|
| WhatsApp | 4 dos 12 | **2** sem resposta seguidas |
| Telefone | **8** dos 12 | nada — `Caixa Postal`/`Não atendeu` insistem até o fim |

O canal com o dobro dos toques, o único com regulador olhando, e o único
sem freio. E o remédio não é novo: é o **mesmo padrão já provado no outro
canal** — um contador de não atendidas seguidas no telefone, e um portão
que desvie para WhatsApp (ou encerre a régua mais cedo) ao estourar. Isso
melhora justamente as três razões que a norma cita — proporção de curtas,
duração média, taxa de completamento — e de graça, sem número novo, sem
cadastro e sem esperar a `Origem Verificada` aceitar a subconta.

**Não especifico o nó aqui, de propósito.** Criar o contador exige campo
novo (`Tel não atendidas seguidas`, NUMERICAL) e mexer no seletor de canal
e no nó 10 das duas cadências — decisão de régua, que muda quantas
ligações/dia a operação faz de verdade e por isso conversa direto com a
meta de 100/dia do `briefing-sdr.md`. É pergunta para o dono, registrada
como **F-09** no roadmap, não escolha de rodada automática. O que esta
correção fecha é o diagnóstico: o F-08 procurou a proteção fora do CRM e
ela também faltava dentro.

**4. O prefixo `0303`, que o F-08 não mencionou.** Obrigatório para
telemarketing ativo de junho/2022 até **agosto/2025**, quando a Anatel o
tornou **facultativo**. O MPF recomendou em seguida que a obrigatoriedade
volte, justamente porque a `Origem Verificada` ainda não alcança toda a
população. Para esta operação: **não adote por conta própria** — o motivo
declarado da revogação é que o `0303` virou estigma e passou a ser rejeitado
automaticamente, o que bate de frente com a taxa de atendimento que esta
operação persegue. Mas é item de vigilância: se voltar a ser obrigatório,
alcança venda ativa por telefone, que é exatamente isto aqui.

**Confiança das fontes:** média-alta. Tudo acima vem de busca — `gov.br` e
`teletime.com.br` estão **bloqueados pelo proxy deste ambiente** (testados
nesta rodada, `EGRESS_BLOCKED`), mesma limitação já registrada para
`help.gohighlevel.com`. O número do despacho, a lista de critérios, o
limiar de 500 mil chamadas/mês, o prazo de 2028, os 5 dias úteis da ABR
Telecom e as datas do `0303` apareceram de forma convergente em fontes
independentes, que é o teste que este projeto usa quando a fonte primária
não abre. Nada aqui foi escrito por dedução.


---

## 2.27 Qualidade da Conexão — F-06 (fechado em 22/09/2026, duas peças)

Destrava o item errado como "esperando volume" desde a primeira versão do
roadmap: `Atendeu` empacota, na mesma célula do relatório, a ligação de 8
segundos e a de 8 minutos, e os contadores de conexão (`Conexões
telefone`/`Conexões WhatsApp`/`Total de conexões`, seção 4) vêm do
julgamento do SDR no calor da discagem, não de conversa de verdade.

**O achado que destrava, e por que a rodada de 21/09/2026 não o tinha
achado:** aquela rodada perguntou "existe duração de chamada nativa no
GHL" e concluiu que não — sem entrada própria em `APRENDIZADOS-CRM.md`,
sinal de busca rasa, a mesma classe de premissa negativa que o F-08 já
cometeu duas vezes na mesma semana (`APRENDIZADOS-CRM.md`, "Premissa
negativa..."). Três buscas desta rodada, com termos diferentes, convergem
numa resposta que aquela pergunta não achou: o gatilho de workflow
**`Transcript Generated`** dispara quando a transcrição de uma chamada fica
pronta e carrega duração, direção e horário como dado do próprio evento —
funciona para chamadas de **Voice AI, IVR e LC Phone** (a telefonia nativa
do GHL, back-end Twilio). Este projeto não usa Voice AI nem IVR (seção 6 é
WhatsApp, não voz), então toda ocorrência do gatilho nesta subconta só pode
vir de LC Phone. Pré-requisito citado pela fonte: transcrição precisa
estar **ligada em Configurações → Telefone** para chamadas LC Phone (em
Voice AI já vem ligada por padrão) — ação de tela, não de API, mesma classe
de pendência que o Number Validation (seção 2.16) já tem.

**A mesma pendência que o F-08/F-09 já registraram, herdada aqui sem
solução nova:** nenhum documento do projeto confirma se as 100 ligações/dia
da operação saem por LC Phone ou por linha própria do SDR (`grep` por `LC
Phone`/`Twilio`/`discador` em todo o `wesales/` confirma: a seção 2.26 já
registrou a mesma lacuna). Se for LC Phone, este item funciona como
especificado abaixo; se for linha própria, `Transcript Generated` nunca
dispara para essas chamadas e o item volta a depender de call tracking
externo, do zero. Uma resposta só resolve as três pendências (F-06, F-08,
F-09) ao mesmo tempo. **Evidência indireta reavaliada em 22/09/2026, mesma data — o CRM não
responde esta pergunta:** `locations_get-location` mostra
`saasSettings.twilioRebilling = { enabled: true, markup: 20 }`, mas o markup
do rebilling é definido **global na agência** (SaaS Configurator), com
override opcional por subconta — o valor lido aqui é compatível com o global
herdado, igual em subconta que nunca ligou, então **não é sinal de número
provisionado nesta**. E a evidência direta, lida na mesma rodada, aponta para
o outro lado: **zero registro de chamada** nas 50 conversas da subconta
(41 atividade de CRM, 9 DM de Instagram, nenhum `TYPE_CALL`) — o contato de
teste com `Tentativas telefone` = 24 tem **uma** mensagem, "Opportunity
created". Os 24 são escritas de campo por classificação manual, não ligações.
A ausência não desempata (pode não haver número, ou haver e nunca ter sido
usado), mas **elimina o CRM como fonte**: é pergunta para o dono, e nenhuma
rodada deve gastar mais tempo procurando por API. Detalhe em
`APRENDIZADOS-CRM.md`, "O CRM não pode responder a pergunta do LC Phone".

**Confiança:** média — a descrição do gatilho ("duration... direction...
across Voice AI, IVR, and LC Phone calls") apareceu de forma consistente em
buscas diferentes, mas `help.gohighlevel.com` segue bloqueado pelo proxy
deste ambiente (lido só por citação de busca) e nada foi testado nesta
subconta. Um filtro de duração **no próprio gatilho** apareceu numa busca;
outra busca, sobre um gatilho diferente (`Call Status`), afirma que filtro
nativo de duração ainda não existe na plataforma — sem fonte que resolvesse
a contradição para o `Transcript Generated` especificamente, o desenho
abaixo **não depende dela**: lê a duração como dado do próprio gatilho e
decide no `If/Else`, caminho que funciona com ou sem filtro nativo de
duração no gatilho.

### Gatilho
**`Transcript Generated`**, filtro Direção = `Outbound` se o gatilho
oferecer (senão o nó 1 abaixo faz o mesmo por `If/Else` — não é redundância
inútil, é rede de segurança caso o filtro nativo não exista, mesmo
raciocínio do parágrafo de confiança acima).

### Configurações
| Configuração | Valor |
|---|---|
| Allow Re-entry | **Ligado** (uma chamada pode gerar uma transcrição por vez, mas o mesmo lead liga de novo em tentativas futuras) |
| Janela de envio | Sem janela |

### Nós
| # | Ação | Configuração |
|---|---|---|
| 1 | If/Else | Direção da chamada é `Outbound` → 2 · Senão → FIM (chamada recebida não é tentativa da cadência) |
| 2 | Update Contact Field | `Duração da ligação` = duração da chamada (merge field exato do gatilho — **confirmar na tela**, nome não testado nesta subconta) |
| 3 | If/Else | `Duração da ligação` **é maior ou igual a** `60` → 4 · Senão → 5 |
| 4 | Update Contact Field | `Conexão real` = `Sim` → 6 |
| 5 | Update Contact Field | `Conexão real` = `Não` → fim |
| 6 | Math | `Conexões reais telefone` (C-31) + 1 → fim |

Não toca nos contadores existentes (`Conexões telefone`/`Conexões
WhatsApp`/`Total de conexões`, escritos pelo Pós-ligação a partir do
julgamento do SDR, seção 4) — os dois convivem, e a diferença entre eles é
o próprio dado que expõe quando o SDR marca `Atendeu` numa ligação curta
demais para ser conversa.

**Peça 2, fechada no mesmo dia — por que a lista e o dashboard não apontam
direto para `Conexão real`:** o plano original da peça 1 ("apontar os dois
para `Conexão real = Sim`") não sobrevive à leitura dos dois destinos.

- **Lista `Conexão por Tentativa` (8.6, R-01):** pode sim filtrar/mostrar
  `Conexão real` direto — Smart List aceita igualdade sobre qualquer tipo
  de campo. Resolvido na própria seção 8.6, abaixo.
- **Widgets de Taxa de Conexão do Dashboard (2.17, R-15):** não podem. O
  achado 2 daquela seção já registra que o Formula Editor de Custom
  Metrics só agrega **Soma/Mín/Máx/Média sobre campo `NUMERICAL`/
  `MONETARY`** (ou contagem de contatos por filtro) — `Conexão real` é
  `SINGLE_OPTIONS`, não é campo que a fórmula some. Contar contatos com
  `Conexão real = Sim` (o recurso mais novo de filtro por metric-level,
  pesquisado nesta rodada) também não serve: devolveria quantos contatos
  estão **agora** nesse estado, não quantas chamadas bateram o limiar ao
  longo do tempo — unidade diferente da que o outro lado da razão
  (`Tentativas telefone`, uma soma cumulativa) usa. E `Conexão real` tem o
  próprio estado vencido já registrado abaixo (um `Sim` da T3 sobrevive a
  T4-T8 sem transcrição): usá-lo num widget acumulado herdaria esse
  defeito para o relatório.

A saída é o nó 6 acima: `Conexões reais telefone` (C-31, `NUMERICAL`),
incrementado uma vez por chamada que bate o limiar, nunca sobrescrito —
mesmo padrão de `Conexões telefone`/`Conexões WhatsApp`/`Total de conexões`
(C-06/C-07/C-11/C-12) e pelo mesmo motivo que eles existem: uma razão
cumulativa pede dois lados cumulativos. Detalhe da comparação em
`campos-e-tags.md` (C-31).

**Pronto quando (cumprido):** todo `Send Call`/discagem feita por LC Phone
grava duração real e `Conexão real` sem depender do julgamento do SDR no
calor da ligação, e "taxa de conexão" tem uma versão no relatório (lista
8.6, nova coluna) e no dashboard (2.17, novo widget) que só conta chamada
que durou mais de 60s — o SDR não consegue mais inflar esse número
desligando rápido. O relatório antigo (`Atendeu`) continua existindo, sem
ser substituído — os dois convivem, cada um respondendo uma pergunta
diferente.

**Zero escrita no CRM:** os três campos (`Duração da ligação`, `Conexão
real`, `Conexões reais telefone`) nascem propostos em `campos-e-tags.md`
(C-29, C-30, C-31) e `[ ]` em `APROVADO.md` — campo personalizado não sai
por API, mesma regra de sempre.

#### Conferência da peça 2, 22/09/2026 (mesma rodada): os dois lados da razão são cumulativos, mas não são da mesma população

O raciocínio de unidade está certo — contador cumulativo de um lado exige
contador cumulativo do outro, e é por isso que C-31 precisou existir. Falta a
pergunta seguinte, que é sobre **quem** cada lado conta:

| Lado da razão | Conta o quê | Escrito por |
|---|---|---|
| `Conexões reais telefone` (C-31) | chamadas **de LC Phone** que **geraram transcrição** e bateram 60s | o workflow desta seção, no nó 6 |
| `Tentativas telefone` (C-09) | **toda** tentativa de telefone que o SDR classificou | o Pós-ligação (seção 4), a partir de `Resultado da tentativa` |

Os dois somam, os dois são cumulativos, e ainda assim a razão entre eles não
é uma taxa — é uma comparação entre dois conjuntos diferentes. Três caminhos
levam ao mesmo erro, e nenhum deles é um bug, é o desenho:

1. **Ligação por linha própria do SDR.** A pendência aberta de LC Phone
   (mesma do F-08/F-09) não é binária na prática: uma operação pode discar
   por LC Phone e o SDR ligar do celular quando está fora. Toda chamada
   assim entra no denominador (o SDR classifica) e **não pode** entrar no
   numerador (sem LC Phone não há transcrição).
2. **Transcrição desligada, ou ligada depois.** Tudo que foi discado antes de
   alguém marcar a caixa em Configurações → Sistema de Telefonia conta no
   denominador e não no numerador — para sempre, porque os dois campos são
   acumulados e ninguém volta atrás.
3. **Chamada sem transcrição a gerar.** Ring que ninguém atendeu pode não
   produzir transcrição nenhuma (o mesmo fato que criou o estado vencido do
   `Conexão real`, registrado acima). Entra no denominador, nunca no
   numerador.

**Por que isto é pior do que ruído:** a razão não fica imprecisa, fica
**enviesada para baixo de forma sistemática**, e o widget vai se chamar "Taxa
de Conexão Real". Quem olhar um número baixo vai ler "o SDR não está
conversando com ninguém" — quando a explicação pode ser inteiramente "metade
das ligações não é medida". É exatamente a métrica que o F-06 existe para
consertar (`Atendeu` inflado pelo julgamento do SDR) trocada por outra
enganosa na direção oposta. E a mais difícil de pegar depois, porque o
número **parece** certo: não dá erro, não fica vazio, só mente.

**A correção é um nó no caminho que já existe.** O nó 2 roda para **toda**
transcrição, antes do teste dos 60s — é o ponto exato onde "esta chamada é
medível" fica conhecido:

| # | Ação | Configuração |
|---|---|---|
| 2b | Math | `Ligações com transcrição` (C-32, NUMERICAL) **+ 1** → segue para o nó 3 |

E a fórmula do widget (seção 2.17) passa a dividir populações iguais:

> `Taxa de Conexão Real — Telefone` = (Soma de `Conexões reais telefone` ÷
> Soma de **`Ligações com transcrição`**) × 100

Lê-se: **das chamadas que dá para medir, quantas foram conversa.** Não é uma
taxa menos ambiciosa que a anterior — é a única das duas que responde a
pergunta do F-06 sem depender de quanto da operação está instrumentada.

**Brinde, e não é pequeno:** `Ligações com transcrição` ÷ `Tentativas
telefone` passa a ser um **medidor de cobertura da medição**. Se der 95%, o
número de cima é confiável; se der 40%, o dono descobre — sem abrir a tela de
telefonia — que a maior parte da operação está fora do LC Phone ou sem
transcrição. É o mesmo método de "contador vizinho" que este projeto já usou
para achar nó silencioso (`APRENDIZADOS-CRM.md`): duas somas que deveriam
andar juntas, e a distância entre elas é o diagnóstico. Sem C-32 essa
distância existe, mas fica invisível — misturada dentro da taxa, indistinguível
de desempenho ruim do SDR.

**Sugestão de widget, junto com o outro:**

| Widget | Fórmula | O que responde |
|---|---|---|
| `Cobertura da Medição — Telefone` | `(Soma de "Ligações com transcrição" ÷ Soma de "Tentativas telefone") × 100` | Quanto da operação de telefone está instrumentada. Abaixo de ~90%, a taxa acima merece ressalva; abaixo de ~50%, o F-06 está medindo outra operação |

**Não altero o nó nem a fórmula, pelo mesmo motivo de sempre:** C-32 é campo
novo, nasce `[ ]` em `APROVADO.md`, e campo personalizado não sai por API.
Enquanto os quatro campos do F-06 não existirem na tela, a seção 2.17 pode
manter a linha antiga — que **ainda não está montada** em nenhum widget, então
não há número errado circulando hoje. O que esta conferência garante é que a
primeira versão montada já nasça com os dois lados da mesma população, em vez
de ser corrigida depois de alguém tomar uma decisão com ela.

### Conferência do F-06, 22/09/2026 (mesma rodada): o gatilho existe, mas só existe para chamada **gravada** — e isso traz um custo, uma obrigação legal e um campo que nunca se apaga

A descoberta do `Transcript Generated` confere, e a ressalva de confiança
acima estava bem colocada. Três coisas que a especificação ainda não diz, e
que mudam o que precisa acontecer antes do primeiro lead passar.

**1. Transcrição não é um item de configuração — é gravação de chamada.** A
dependência não pára em "ligar a transcrição em Configurações → Telefone": a
transcrição **exige gravação de chamada habilitada** para o número. Sem
gravação não há transcrição, e sem transcrição **este workflow nunca
dispara** — o gatilho não tem outro caminho de entrada. A frase correta do
pré-requisito é, então, mais forte do que a que está escrita acima:

> Para o F-06 funcionar, **toda ligação de saída da operação passa a ser
> gravada**.

Isso não é detalhe de implementação. É uma decisão sobre a operação, e ela
nunca foi tomada: `grep -rn "gravaç\|LGPD\|consentimento"` em todo o
`wesales/` não encontra **uma única** menção a gravação de chamada, aviso de
gravação ou base legal. O `script-de-ligacao.md` abre direto na abordagem,
sem aviso de gravação em nenhuma das versões.

**2. Consequência legal, do mesmo tipo que a janela de 24h do WhatsApp
(G-05) — uma regra externa que não deixa rastro até o primeiro evento
real.** Gravar ligação com lead no Brasil, numa operação de venda ativa
B2B, é tratamento de dado pessoal sob a LGPD e pede, no mínimo, **aviso ao
interlocutor no início da chamada** e uma base legal declarada. O padrão de
mercado é uma frase fixa nos primeiros segundos ("esta ligação está sendo
gravada para fins de qualidade"). Duas observações que fazem isso valer a
pena escrever agora e não depois:

- O aviso entra exatamente no ponto do script onde hoje começa a abordagem
  — e **muda a abordagem**, porque consome os primeiros segundos, que são o
  ativo mais escasso de uma ligação fria. É decisão de script, não de
  workflow: pertence ao `script-de-ligacao.md`, não a esta seção.
- É o mesmo padrão já aprendido no G-05 e registrado em
  `APRENDIZADOS-CRM.md`: regra de plataforma (ou de lei) que ainda não foi
  testada nenhuma vez **não deixa rastro nenhum** para uma auditoria de
  dados achar. Tem de ser lida contra a regra, antes do primeiro envio — ou,
  aqui, antes da primeira gravação.

**Não sou a fonte jurídica disto e não escrevo a frase do aviso por
dedução** — a redação e a base legal (legítimo interesse vs. consentimento)
são do dono ou de quem o assessora. O que esta conferência entrega é que a
pergunta existe e está no caminho crítico do F-06, não depois dele.

**3. Custo, nunca calculado em nenhum documento do projeto.** A transcrição
é um add-on pago de **Voice Intelligence**, a **US$ 0,024 por minuto
gravado**, cobrado **por cima** da tarifa de gravação de chamada (e do
armazenamento das gravações, que o HighLevel cobra separadamente). Com a
meta de 100 ligações/dia:

| Premissa (declarada, não medida) | Conta |
|---|---|
| ~20% conectam, ~3 min cada | 60 min/dia |
| ~80% morrem curtas, ~20 s cada | ~27 min/dia |
| Total | **~87 min/dia ≈ 1.900 min/mês** |
| Só a transcrição | **≈ US$ 45/mês**, mais gravação e armazenamento |

Ordem de grandeza modesta, e vale dizer: **não é argumento contra o item.**
Mas tem uma ironia que o dono deveria ver antes de ligar a chave — paga-se
para transcrever principalmente os ~80% de chamadas que **não** são
conversa, só para descobrir que não eram. Se o custo incomodar, existe saída
barata sem abandonar o F-06: o `Resultado da tentativa` do SDR já separa
`Atendeu` do resto, e gravar/transcrever **só** o que ele marcou como
`Atendeu` cortaria a maior parte do volume — ao preço de perder exatamente a
medição que o F-06 existe para fazer (pegar o `Atendeu` que durou 8
segundos). É um trade-off para o dono, não uma escolha de rodada automática.

**4. O `Conexão real` nunca é apagado — e um lead pode carregar um `Sim`
vencido por várias tentativas.** Este é um defeito de desenho, não de
pesquisa. Os nós 4 e 5 escrevem `Sim` ou `Não`; nada, em lugar nenhum,
devolve o campo ao vazio. Combine isso com o item 1 e aparece o caso ruim:

> Uma chamada que **ninguém atendeu** pode não gerar transcrição nenhuma —
> não há o que transcrever. Então o workflow **não roda**, e o campo fica
> com o valor da tentativa **anterior**.

Lead que conversou de verdade na T3 (`Conexão real = Sim`) e depois teve
T4, T5, T6 e T7 no vazio continua lendo `Sim` na ficha e em qualquer lista
que filtre por ele. O campo deixa de significar "esta tentativa foi
conversa" e passa a significar "alguma tentativa, em algum momento, foi
conversa" — que é outra métrica, e não a que o F-06 pede. É a mesma classe
de estado vencido que este projeto já catalogou três vezes
(`APRENDIZADOS-CRM.md`: o contador que não zera, a tag que não sai, o portão
que lê etapa sem `status`).

**Onde o reset pertence, e por que não é no Pós-ligação:** a transcrição
chega **minutos depois** da chamada, enquanto o SDR classifica na hora.
Zerar o campo no Pós-ligação (gatilho `Resultado da tentativa` alterado)
disputaria com a escrita desta seção — o clássico "campo com dois donos" já
registrado. O ponto sem ambiguidade é **antes** da ligação existir: o nó de
cada tentativa que cria a tarefa de ligação (seções 2.4 e 2.10) acrescenta
`Update Contact Field: Conexão real = vazio`. A ordem passa a ser sempre
tarefa criada (limpa) → ligação → SDR classifica → transcrição escreve, sem
dois nós disputando o mesmo campo no mesmo instante.

**Não altero o nó aqui:** mexer nas seções 2.4/2.10 é mexer na régua das
duas cadências, e os dois campos ainda nascem `[ ]` em `APROVADO.md` —
enquanto não existirem na tela, não há o que zerar. Fica registrado como
pré-requisito do "Pronto quando" desta seção, junto com a gravação e o
aviso: **o F-06 não está pronto com os nós 1-6 sozinhos.**

**Confiança das fontes:** média-alta para os fatos de plataforma
(transcrição exige gravação; add-on Voice Intelligence a US$ 0,024/min
gravado; caminho Configurações → Sistema de Telefonia → Voz → Transcrição
de Chamadas) — convergentes em fontes independentes, com
`help.gohighlevel.com` ainda bloqueado pelo proxy, lido só por citação. A
conta de custo é **minha, com as premissas declaradas na tabela**, não uma
medição. O ponto 4 não depende de fonte externa nenhuma: sai da leitura dos
próprios nós.

---

## 2.28 Monitor de Saúde da Operação — extensão à negociação — F-13

**Por quê:** achado ao conferir a Etapa 3 (`NEGOCIAR`) deste documento, seção
1.1 acima — a linha "Tempo de estagnação" registrava, desde antes de F-05
existir, que a metade "comparecimento" tem monitor (R-12, SLA do closer) mas
a metade "negociação" não. F-05 fechou em 21/09/2026 com seis peças
(`NOVO LEAD`, `fila-tel`/`fila-wa`, `CONECTAR`, `nao-perturbe` em workflow
ativo, `AGENDAR`, retorno vencido) e nunca chegou a incorporar esta — o
"candidato a entrar no F-05" nunca virou peça. O buraco é o mesmo tipo dos
outros seis: o Loop do closer (seção 5.1,
ramo `Sim`) registra o veredito e **não move etapa nem status** — "é o
closer, fora deste workflow, que leva a `FORMALIZAR` quando fechar" (seção
5.1, ramos do nó 4). Um lead qualificado que o closer nunca mais toca fica
parado em `NEGOCIAR`/`open` para sempre, sem que nada avise: mesma classe de
"estrago silencioso" que abriu as seis peças do F-05, aqui na única
transição da operação (comparecimento → decisão) que sobrou sem relógio.

Mesma pesquisa das peças anteriores: nenhuma das quatro plataformas do
enunciado (Reev, Meetime, Outreach, Salesloft) expõe alarme proativo para
"reunião qualificada sem decisão do closer" — todas tratam isso como
relatório de pipeline (dias em estágio, olhado por quem abre o dashboard),
não como notificação disparada pelo tempo. Continua sendo engenharia
interna, não recurso de sales engagement de prateleira.

**Prazo escolhido, e por quê 3 dias e não 24h como a peça 5:** as peças 1, 3
e 5 usam 24h porque medem passos que dependem só do SDR (revisar fila,
insistir, fechar horário) — o mesmo dia deveria bastar. Aqui quem decide é o
**closer**, sobre uma proposta que o próprio lead também precisa avaliar; a
régua de No-show (seção 5.3) já reconhece esse ritmo mais lento ao dar 4
tentativas em 4 dias corridos para uma reunião remarcar, e a maioria dos
leads desta base marca `Urgência` = `Pra ontem` (G-04), o que pesa a favor de
um prazo curto, não longo. 3 dias corridos fica entre os dois: mais que o
ciclo de um único dia de trabalho do SDR, menos que o horizonte de 4 dias já
aceito pela régua mais lenta do projeto. É escolha desta rodada, não medição
— ajustável na tela sem redesenho (é um único `Wait`), e de baixo risco por
ser aviso interno ao gestor, não mensagem ao lead (a mesma razão que já
deixou as peças 1, 3 e 5 decidirem sozinhas, sem esperar o dono, diferente de
G-03/G-04/F-09, que mudam comportamento visível para o lead ou o volume de
ligação).

### Workflow "Negociação Estagnada"

#### Gatilho
**Contact Changed** — filtro: Custom Field `Reunião foi qualificada`
**alterado**. Mesmo gatilho do Loop do closer (seção 5.1) — os dois reagem
ao mesmo evento, um registra e roteia na hora, o outro só liga um relógio.

#### Configurações
| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | O closer pode corrigir o veredito mais de uma vez; cada alteração para `Sim` merece seu próprio relógio, mesmo motivo do 5.1 |
| Janela de envio | Sem janela, 24/7 | Aviso interno ao gestor, não mensagem ao lead |
| Stop on Response | Desligado | Não há mensagem ao lead aqui |

#### Nós
| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Portão — vale a pena vigiar? | If/Else | `Reunião foi qualificada` **é** `Sim` → segue. Senão (vazio, `Não`, `Parcial`) → **encerra** (os outros três vereditos já saem de `open` na hora, seção 5.1 — nada a esperar) |
| 2 | Aguardar | Wait → Time Delay | 3 dias corridos |
| 3 | Portão — ainda pendente? | If/Else | Etapa da oportunidade **é** `NEGOCIAR` **E** `status` **é** `open` **E** `Reunião foi qualificada` **é** `Sim` → segue (3 dias depois do "Sim", o closer não fechou nem descartou, e o veredito não mudou). Senão → **encerra** (fechou `won`, saiu por `lost`/`abandoned`, ou o veredito foi corrigido — os três já passam pelo Mestre de saída, seção 3) |
| 3b | **Portão de aviso único** | If/Else | tag `negociacao-estagnada` **ausente** → segue para o nó 4 (é o primeiro alerta desta parada). **Presente** → **encerra** (outro relógio já avisou). Acrescentado na conferência de 22/09 — ver nota abaixo |
| 4 | Fila | Add Contact Tag | `negociacao-estagnada` |
| 5 | Aviso | Internal Notification | Para o gestor: `{{contact.name}} foi qualificado pelo closer (Sim) há mais de 3 dias e segue em NEGOCIAR sem fechar nem perder. Veredito em: {{contact.data_do_veredito_do_closer}}.` |
| 6 | Registro | Add Note | `Alerta de saúde: NEGOCIAR sem decisão do closer em 3 dias · {{right_now}}` |

#### Por que o nó 3b existe — conferência de 22/09/2026

`Allow Re-entry` **ligado** (decisão certa: o closer pode corrigir o veredito)
mais um gatilho que dispara a **cada alteração** do campo produzem instâncias
simultâneas, e o nó 3 não olha a tag. O caminho:

| Momento | O que acontece |
|---|---|
| T0 | closer marca `Sim` → **instância A** começa o `Wait` de 3 dias |
| T0+1h | closer corrige para `Parcial` → instância B nasce e **morre no nó 1** (não é `Sim`) ✔ |
| T0+2h | closer volta para `Sim` → **instância C** começa o próprio `Wait` |
| T0+3d | nó 3 da A: `NEGOCIAR` + `open` + `Sim` → tag + **aviso nº 1** |
| T0+3d+2h | nó 3 da C: **mesmo estado** → **aviso nº 2, do mesmo lead** |

A tag do nó 4 é idempotente; a **notificação do nó 5 não é**. Dois avisos para
a mesma parada é como um canal de alerta começa a ser ignorado — e este
projeto já resolveu exatamente isso, com exatamente este nó: a seção 2.22 tem
um "**Portão de aviso único**" (nó 6) que checa a tag ausente antes de alertar,
pelo mesmo motivo, só que lá a repetição vem do laço em vez da reentrada.
Mesmo sintoma, mesmo remédio, e assim as duas peças ficam consistentes.

**Diferença de desenho em relação ao 2.22, de propósito:** lá o portão
**desvia** para o fim do laço (o workflow continua vigiando); aqui ele
**encerra**, porque não há laço — a instância A já está de olho, e quem mantém
o lead na lista 8.28 é a tag, não a instância.

**Por que não precisa de tratamento incondicional no Mestre de saída, ao
contrário de `novo-lead-estagnado`/`agendar-estagnado` (peças 1 e 5):**
aquelas duas tags marcam estagnação numa etapa que o nó 1 do Mestre de saída
trata como no-op (`NOVO LEAD`/`CONECTAR`, junto com `status = open`) — a
transição normal de saída delas nunca alcança o nó 4. `NEGOCIAR` não está
nessa lista: toda saída real (fechar `won` → `FORMALIZAR`, mudar `status`
para `lost`/`abandoned` sem sair da etapa, ou o próprio veredito sendo
corrigido de `Sim` para outra coisa, que também muda `status` pela seção
5.1) já é uma transição que o Mestre de saída enxerga pela via normal — basta
somar a tag à lista já existente do nó 4 (seção 3, abaixo), mesmo tratamento
de `fila-travada`/`conectar-estagnado`/`retorno-vencido`.

**Limite conhecido:** se o closer corrigir o veredito de `Sim` para `Não`
sem que isso mude `status` nem etapa — não deveria acontecer, os três ramos
do nó 4 da seção 5.1 sempre mudam `status` — a tag sobreviveria até a
próxima saída real. Mesma classe de limite que `retorno-vencido` já aceitou
(rede de segurança, não garantia absoluta) para uma coincidência tão rara
quanto essa.

**Pronto quando (F-13):** uma reunião qualificada pelo closer (`Sim`) que
passa 3 dias em `NEGOCIAR`/`open` sem virar `won` nem `lost` gera aviso ao
gestor sozinho — a única linha "Tempo de estagnação" da seção 1.1 (etapas
`NOVO LEAD` a `FORMALIZAR`) que ainda dizia "sem monitor" agora tem um.

---

## 3. Workflow "Mestre de saída" — migrado para as 5 etapas reais em 18/09/2026

O guarda-costas da operação: garante que sair de `CONECTAR` limpa tudo.

**Mudança estrutural desta migração, não só troca de nome:** no plano de 7
etapas, toda saída de cadência (conectou, número errado, não ligar, 12
tentativas esgotadas) era um movimento de etapa — um `Opportunity Stage
Changed` cobria os quatro casos. Na tela real, só o primeiro continua sendo
movimento de etapa (`CONECTAR` → `AGENDAR`); os outros três viraram `status`
da oportunidade (`abandoned`/`lost`) **sem sair de `CONECTAR`** (tabela 1.0).
Um gatilho só de `Opportunity Stage Changed` deixaria de disparar para eles —
a limpeza nunca aconteceria para o caminho mais comum de saída (12
tentativas esgotadas). Por isso este workflow passa a ter **dois gatilhos**
(GHL aceita mais de um gatilho no mesmo workflow, cada um em OR — pesquisado
nesta migração), e o portão (nó 1) troca de "etapa de destino" por uma
condição que cobre os dois:

### Gatilhos
1. **Opportunity Stage Changed** — Pipeline `FUNIL DE VENDAS`, qualquer
   etapa de destino.
2. **Opportunity Status Changed** — Pipeline `FUNIL DE VENDAS`, para o
   status `Lost` **ou** `Abandoned` (não filtra `Won`/`Open`: nenhum dos
   dois é saída de cadência que precise de limpeza — `Won` é `FORMALIZAR`,
   já coberto pelo gatilho 1 como mudança de etapa).

### Configurações
| Configuração | Valor |
|---|---|
| Allow Re-entry | **Ligado** (precisa disparar em toda mudança de etapa ou de status) |
| Janela de envio | Sem janela (é limpeza interna, não manda mensagem) |
| Stop on Response | Desligado |

### Nós
| # | Ação | Configuração |
|---|---|---|
| 0 | Remove Contact Tag | `novo-lead-estagnado` (F-05, seção 2.20), `agendar-estagnado` (F-05, seção 2.23) — **incondicional, antes do portão do nó 1** |
| 1 | If/Else | `status` **é** `open` **E** etapa da oportunidade **é uma de** `NOVO LEAD`, `CONECTAR` → **encerra aqui** (não limpa nada). Senão, segue |
| 2 | Remove from Workflow | `Cadência 12x30` |
| 2b | Remove from Workflow | `Cadência Inbound` (seção 2.10, quando existir) |
| 2c | Remove from Workflow | `Reengajamento 90 dias` (seção 2.12, quando existir) |
| 3 | Remove from Workflow | `Qualificação por IA no WhatsApp` |
| 4 | Remove Contact Tag | `fila-quente`, `fila-tel`, `fila-wa`, `fila-linkedin`, `atraso-1a-tentativa` (R-02), `reengajamento-ativo` (R-08), `pausado` (R-09), `fila-travada` (F-05, seção 2.21), `conectar-estagnado` (F-05, seção 2.22), `retorno-vencido` (F-05, seção 2.24 — rede de segurança; a limpeza normal roda no nó 3c do Pós-ligação, seção 4), `negociacao-estagnada` (F-13, seção 2.28) |
| 5 | Add Contact Tag | `limpar-tarefas` |
| 6 | Add Note | `Saída de cadência · etapa: {{opportunity.pipeline_stage}} · status: {{opportunity.status}} · tentativa {{contact.tentativa_n}} · resultado {{contact.resultado_da_tentativa}}` |

**Por que o nó 0 é incondicional, e não mais uma linha do nó 4 (achado de
21/09/2026, F-05, seção 2.20):** `novo-lead-estagnado` marca um lead parado
em `NOVO LEAD`, uma etapa **anterior** a `CONECTAR` — o portão do nó 1
("`CONECTAR` e `open` → encerra sem limpar") trata a transição normal
`NOVO LEAD` → `CONECTAR` como no-op, então nunca alcança o nó 4 nesse
caminho, que é exatamente o caminho em que este alerta se resolve. Rodar a
remoção antes do portão, sem condição, resolve sem duplicar o portão para
uma tag só: `Remove Contact Tag` de quem não tem a tag não faz nada, mesmo
raciocínio já usado para `Remove from Workflow` nos nós seguintes.

**F-05, peça 5 (21/09/2026) — `agendar-estagnado` entrou no mesmo nó 0, por
precaução, não porque o caminho normal precise dele:** a saída comum de
`AGENDAR` (Pós-agendamento move para `NEGOCIAR`) já cai fora da lista de
no-op do nó 1 e alcançaria o nó 4 sozinha, como `fila-travada`/
`conectar-estagnado`. Mas L-08 (`briefing-sdr.md`) registra que hoje não
existe caminho formal de desqualificar a partir de `AGENDAR` — se um dia
alguém arrastar a oportunidade de volta para `CONECTAR` na mão (o único
"desistir" manual possível sem esse caminho), a condição do nó 1 volta a
ser verdadeira e trataria essa transição como no-op, repetindo a classe de
bug que já motivou este nó 0 para `novo-lead-estagnado`. Somar a tag aqui
custa nada (mesmo raciocínio do parágrafo acima) e cobre os dois caminhos de
uma vez — detalhe completo na seção 2.23.

**F-05, peça 4 (21/09/2026) — a lista dos nós 2/2b/2c/3 virou um só nó, e o
motivo é o mesmo que motivou a peça 4 do "Como" original do F-05 ("`nao-
perturbe` ainda dentro de workflow ativo"):** o "Como" do roadmap descrevia
essa invariante como algo para **detectar** — uma rotina que audita e avisa
depois do vazamento. Pesquisado antes de desenhar o monitor: o GHL não tem
filtro nativo de Smart List "ativo em qualquer workflow" (só "ativo neste
workflow específico", pedido em aberto na base de ideias da HighLevel — a
**Por que este workflow — e só ele — continua com a lista nomeada, em vez do
`All Except Current Workflow` (correção de 21/09/2026, no mesmo dia da
troca):** a ação nova é melhor e ficou nos outros três lugares (nó 3 do
Pós-agendamento, ramo `Não ligar` da seção 4, e o Opt-out da 2.9.5). Aqui ela
tem um efeito colateral que os outros três não têm, e é grave.

O Mestre de saída quase nunca é disparado por uma ação do lead: ele é
disparado **por outro workflow mexendo na etapa ou no status**, enquanto esse
outro workflow **ainda está rodando**. Dois casos reais do próprio
documento:

| Quem dispara | O que ainda faltava rodar nele | O que `All Except Current` mataria |
|---|---|---|
| Pós-agendamento, nó 1 (`move para NEGOCIAR`) | nós 4 a 10: a `Nota de qualificação`, a confirmação no WhatsApp e os **três lembretes** (24h, 3h, 30min antes da reunião) | os lembretes de **toda reunião agendada** — o ativo mais caro do funil |
| Pós-ligação, ramo `Atendeu`, nó 6 (`move para AGENDAR`) | nós 7 a 9: `Data conectado`, `Hora da conexão` (C-25), a tarefa `[CONECTADO] Qualificar e agendar` e a nota | a **próxima tarefa do SDR** depois de uma conexão — o lead atende e desaparece da fila |

E como o Mestre roda como workflow separado, o corte chegaria em momentos
diferentes a cada vez: às vezes depois do lembrete, às vezes antes. Bug não
determinístico, que é o pior tipo de bug para uma operação diagnosticar.

O raciocínio que evitou `All Workflows` ("cortaria a própria execução deste
workflow") estava certo e parou um passo antes do necessário: **`All Except
Current` protege o workflow atual e corta o de quem o chamou.** Exatamente a
pergunta que este projeto já aprendeu a fazer — *quem mais passa por aqui?*
(`APRENDIZADOS-CRM.md`, "Quando a previsão do bug está escrita").

Nos outros três lugares a ação é segura porque o workflow **atual** é o que
quer silêncio, e ninguém depende do que foi cortado: o Pós-agendamento
protege os próprios lembretes (ele é o `Current`), e o opt-out e o
`Não ligar` **querem** matar tudo que estiver pendente, lembrete incluído.

A lista nomeada aqui volta com o custo conhecido — precisa ganhar uma linha
quando nascer régua nova — e com a regra de manutenção já registrada
(`APRENDIZADOS-CRM.md`, "Conte onde a tag é aplicada e onde é removida" e o
grep de `Remove from Workflow`). É o custo menor dos dois.

mesma classe de limite já documentada para R-10/R-11), então um monitor de
verdade precisaria de um filtro por workflow, o mesmo problema de lista que
já causou o furo duas vezes (a lista nasceu com um nome só, ganhou dois em
19/09/2026 — nota abaixo —, e a de 2.9.5, seção 2.9.5, já é uma terceira
cópia, maior, da mesma lista). Encontrada uma ação nativa melhor que
detectar: **Remove Workflows**, com quatro opções (`Current Workflow`,
`Another Workflow`, `All Except Current Workflow`, `All Workflows` —
pesquisado via `WebSearch`, confiança média, documentação oficial da
HighLevel bloqueada pelo proxy deste ambiente, confirmado por três fontes de
terceiros independentes: um changelog da própria HighLevel referenciado por
elas e dois guias). `All Except Current Workflow` (não `All Workflows` —
teria removido este próprio Mestre de saída no meio da própria execução,
cortando os nós 4/5/6 abaixo antes de rodarem, o mesmo tipo de corte que a
seção 5.4 já documenta para `Remove from Workflow` cancelando um `Wait`
pendente) tira o contato de **toda** régua automática ativa, existente ou
futura, sem precisar nomear nenhuma — o vazamento que a peça 4 do F-05 foi
desenhada para detectar deixa de poder acontecer, em vez de só ficar mais
visível quando acontece. Zero campo, zero tag, zero escrita no CRM: item de
documentação pura, não depende de `APROVADO.md`. Mesma troca aplicada nos
outros dois lugares que tinham a mesma lista manual — seção 4 (ramo `Não
ligar`) e seção 2.9.5 (`Opt-out por Palavra-chave`) — sempre com `All Except
Current Workflow`, nunca `All Workflows`, porque as três têm nó depois na
mesma régua.

**Por que os nós 2b e 2c existiam, contexto que a mudança acima não apaga
(achado de 19/09/2026, mesma classe do 2.11):** quando este workflow foi
escrito havia **uma** régua rodando —
`Cadência 12x30` —, e tirar o lead dela era tirar o lead da cadência. Hoje
são três (`Cadência 12x30`, `Cadência Inbound` da seção 2.10 e
`Reengajamento 90 dias` da seção 2.12), e as duas novas reaproveitam o bloco
padrão da 2.4 sem se remover sozinhas. Com o nó 2 sozinho, um lead inbound
descartado pelo portão de higiene (`status` = `abandoned`/`lost` **sem sair
de `CONECTAR`**) continuava recebendo as tentativas TI2 a TI5 — tarefa,
mensagem e tudo — porque o único workflow que a limpeza conhecia não era o
que estava rodando. O mesmo valia para um lead em reengajamento marcado como
perdido na mão pelo SDR no meio das TR1-TR4. `Remove from Workflow` é
idempotente para quem não está no workflow, então os três nós rodam sempre,
sem If/Else de origem.

**Por que o portão do nó 3 da seção 2.4 também ganhou `status é open`
(mesma rodada):** os nós 2/2b/2c são a limpeza *correta*, mas ela é
assíncrona — depende do gatilho 2 disparar e do `Remove from Workflow`
chegar antes do próximo `Wait` da régua vencer. O portão dentro do bloco
padrão é o cinto de segurança: mesmo que a remoção atrase, a tentativa
seguinte lê `status` e encerra pelo ramo 3b (que já limpa fila e tarefa).
Um dos dois sozinho deixa janela; os dois juntos, não.

**Por que `NOVO LEAD` entrou no nó 1 em 21/09/2026 — o dado de produção
cobrou uma consequência que este documento já tinha escrito:** a auditoria
dos 50 contatos (`APRENDIZADOS-CRM.md`, "Os dados de produção são a terceira
auditoria") achou que **os 10 leads nascidos depois deste workflow ir ao ar
chegaram com a tag `limpar-tarefas`** — leads que nunca entraram em cadência
nenhuma. A causa é este nó: o gatilho 1 é `Opportunity Stage Changed` para
**qualquer** etapa de destino, a Porta de Entrada (seção 1.3) cria a
oportunidade em `NOVO LEAD`, e o portão só encerrava para `CONECTAR`/`open`.
Resultado: todo lead novo rodava a limpeza inteira na chegada — ganhava
`limpar-tarefas` e uma nota "Saída de cadência" dizendo que saiu de uma
régua em que nunca esteve.

O mais instrutivo é que **a seção 2.12 já havia previsto exatamente isso**,
por escrito, como motivo para o Reengajamento não passar por `NOVO LEAD`
("ele rodaria a limpeza inteira… num contato que não estava, de fato, saindo
de cadência nenhuma… risco de corrida real com a rotina horária"). O
raciocínio estava certo e ficou local: usado para desviar **um** workflow,
nunca aplicado ao caminho por onde entra **todo** lead da operação. Mesma
classe das outras listas incompletas deste documento — a diferença é que
aqui a previsão do bug estava escrita antes do bug acontecer.

`NOVO LEAD` **e** `open` nunca é saída de cadência: é chegada (ou um
retrocesso manual para o topo do funil). O único caso que essa condição passa
a não limpar é o lead arrastado de `CONECTAR` de volta para `NOVO LEAD` na
mão, que mantém tag de fila — e esse cai no monitor de lead esquecido (seção
2.20) em 24h, que avisa o gestor; tratar o caso raro valeria menos que sujar
o histórico de todo lead novo.

**Por que a condição do nó 1 é "CONECTAR E open", não só "CONECTAR":** as
duas coisas precisam ser verdade ao mesmo tempo para o lead estar *de
verdade* correndo a cadência ainda. Entrar em `CONECTAR` (`status` nasce
`open`) bate as duas → encerra, correto (é chegada, não saída — sem isso,
mover o lead *para* a cadência acionaria a limpeza e mataria a cadência no
nascimento, o mesmo raciocínio do nó 1 original). 12 tentativas esgotadas,
número errado, não ligar ou o portão de higiene do nó 0.0b mudam o `status`
para `abandoned`/`lost` **sem sair de `CONECTAR`** — `status` deixa de ser
`open`, a condição fica falsa, e a limpeza roda mesmo com a etapa igual.
Atendeu move para `AGENDAR` — etapa deixa de ser `CONECTAR`, a condição já
fica falsa por esse lado sozinho. Progressões seguintes (`AGENDAR` →
`NEGOCIAR` → `FORMALIZAR`) também disparam o gatilho 1 e reexecutam a
limpeza — redundante (as tags já não estão mais lá, as ações são
idempotentes) mas inofensivo, e já era assim no desenho original com
"qualquer etapa de destino".

Não removo `conectado-hoje`, `nao-perturbe`, `telefone-invalido`,
`nutricao-90d`, `cad-inbound` e `cad-outbound`: são estado do lead, não fila.
`pausado` (R-09, seção 2.13) entra no nó 4 mesmo sendo estado individual, não
fila — porque, diferente de `nao-perturbe`, ela só tem sentido **dentro** de
`CONECTAR` (represar uma tentativa que ainda vai acontecer). Uma vez que o
lead sai de cadência por um motivo real (conectou, número errado, não
ligar), a pausa perdeu o objeto: não sobra tentativa nenhuma para represar, e
manter a tag viva só confundiria uma reativação futura pelo Reengajamento
90 dias (seção 2.12), que já teria um SDR pausando um lead que nem está mais
correndo régua nenhuma.
`reengajamento-ativo` (R-08, seção 2.12) entrou na lista do nó 4 porque ela
**é** fila, só que da régua de reengajamento em vez da 12x30 — o mesmo
motivo de `fila-tel`/`fila-wa` estarem lá: nasce ao entrar em `CONECTAR`
pela reativação e não tem por que sobreviver a uma saída dela, qualquer que
seja o resultado (conectou, número errado, não ligar ou esgotou as 4
tentativas).
`fila-travada` (F-05, seção 2.21) entrou no nó 4 por um motivo diferente de
`novo-lead-estagnado` (que precisou do nó 0 incondicional, acima): o alerta
de fila travada se resolve quando o lead sai de `CONECTAR`/`open` de
verdade — exatamente a transição que este nó 4 já alcança pela via normal,
ao contrário do caso de `NOVO LEAD` → `CONECTAR`, que o portão do nó 1 trata
como no-op. Não precisa de nó extra: a limpeza cai na lista existente.

---

## 4. Workflow "Pós-ligação" — migrado para as 5 etapas reais em 18/09/2026

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
| 3b | Remove Contact Tag | `fila-quente` — **incondicional, e depois do nó 2 de propósito** (o nó 2 lê `fila-wa` para decidir o contador; tag de fila só pode sair depois dessa leitura). Ver nota abaixo |
| 3c | Remove Contact Tag | `retorno-vencido` (F-05, seção 2.24) — **incondicional, qualquer resultado novo**. Ver nota abaixo |
| 4 | If/Else múltiplo | Ramifica por todos os valores de `Resultado da tentativa` (campos-e-tags.md, C-02), abaixo — inclui `Desqualificado`, novo nesta rodada (R-18) |

O nó 2 repete de propósito a mesma checagem de canal que já existe no ramo
`Caixa Postal`/`Não atendeu`, em vez de calcular uma vez só e guardar num
campo: são dois pontos do fluxo que precisam saber o canal, e mais um campo
"canal desta tentativa" só para não repetir uma condição de uma linha é troca
ruim (R-01, feito em 18/09/2026).

**Por que o nó 3b existe (achado em 21/09/2026, ao conferir a peça 2 do
F-05):** `fila-quente` é aplicada em **quatro** lugares — Interceptação de
Sinal por clique (2.9.2, nó 6) e por resposta (2.9.3), entrada da Cadência
Inbound (2.10, nó 0.7) e a régua da IA quando a nota passa de 45 (seção 9) —
e era **removida em apenas dois**: o ramo falso do portão da tentativa (nó 3b
da seção 2.4) e o nó 4 do Mestre de saída, que só roda em saída de verdade da
cadência.

Faltava a remoção do caso normal: o sinal **foi atendido**. Um lead que clica
no link, ganha a tarefa "ligar agora", é ligado e marca `Não atendeu`
continua em `CONECTAR`/`open` — então nada remove a tag, e ele fica na lista
`Fila Quente` (8.1) para sempre, misturado com quem deu sinal agora. A fila
mais prioritária da operação é justamente a que apodrece primeiro, porque
nada nela expira. Já acontece: um contato carrega `fila-quente` hoje.

Este é o lugar certo para a remoção, e não um relógio como o da 2.21: o
gatilho deste workflow é `Resultado da tentativa` **alterado**, que é a
definição operacional de "alguém agiu sobre o lead". O sinal se consome
quando é trabalhado, não quando o dia acaba. Se o lead clicar de novo depois,
a Interceptação reaplica a tag (`Allow Re-entry` ligado) — é sinal novo,
merece fila nova.

**Retoque de tela:** o Pós-ligação está publicado (24 execuções). A linha
está na tabela de retoques do `GUIA-MONTAGEM.md`.

**Por que o nó 3c existe (F-05, peça 6, seção 2.24):** mesma classe de
achado do nó 3b, aplicada a `retorno-vencido` em vez de `fila-quente` — o
caminho mais comum de recuperação (o SDR liga de volta e reclassifica) não
muda etapa nem `status` na maioria dos resultados possíveis, então o Mestre
de saída nunca dispara para limpar. O gatilho deste workflow já é "alguém
agiu sobre o lead"; um `Remove Contact Tag` incondicional aqui, antes da
ramificação do nó 4, fecha o caminho de recuperação sem depender de etapa
mudar. Detalhe completo na seção 2.24.

#### Ramo `Atendeu`
| # | Ação |
|---|---|
| 1 | If/Else | A tentativa foi de WhatsApp? (mesma checagem do nó 2) → Math: `Conexões WhatsApp` + 1. Senão → Math: `Conexões telefone` + 1 |
| 2 | Math: `Total de conexões` + 1 |
| 3 | Update: `WA não atendidas seguidas` = 0 |
| 4 | Add Contact Tag `conectado-hoje` |
| 5 | Remove Contact Tag `fila-tel`, `fila-wa` |
| 6 | Mover oportunidade → `AGENDAR` (dispara o Mestre de saída pelo gatilho de etapa, que faz a limpeza) |
| 7 | Update Contact Field `Data conectado` = `{{right_now}}` (R-03 — só marca; não repete se já preenchido, mas escrever de novo é barato e não quebra nada) |
| 7b | Date/Time Formatter | Entrada `{{right_now}}` · "To Format" = `HH` (só a hora, 00–23) — mecanismo de horário aprendido por segmento, seção 2.18, F-02 |
| 7c | Update Contact Field | `Hora da conexão` = saída do nó 7b |
| 8 | Add Task `[CONECTADO] Qualificar e agendar` · vence hoje · Atribuir: `Contact Owner` (dinâmico, R-10) |
| 9 | Add Note `Atendeu na T{{contact.tentativa_n}}` |

O nó 6 move **toda** ligação atendida para `AGENDAR`, sem olhar se a conversa
já mostrou que não há fit — é a lacuna **L-08** (`briefing-sdr.md`), fechada
nesta rodada pelo ramo `Desqualificado` abaixo (R-18): quem atende e claramente
não serve não deveria abrir tarefa de agendamento nenhuma.

#### Ramo `Desqualificado` — novo nesta rodada, fecha L-08 (R-18)

O SDR atendeu a ligação (é uma conexão real, conta como tal), mas a própria
conversa já descartou o lead — sem fit, sem budget, é concorrente, já é
cliente, não fala com decisor. Hoje o único caminho para esse resultado é
classificar como `Atendeu` mesmo assim, o que cria a tarefa `[CONECTADO]
Qualificar e agendar` e empurra o lead para `AGENDAR` — o SDR então tem que
desfazer isso na mão (não agendar, e sair explicando por fora por que a
oportunidade não avança), ou pior, força uma reunião sem fit só para a
tarefa fechar, poluindo a agenda do closer. Nenhum dos dois é registrado
como perda em lugar nenhum — a nota de qualificação (seção 9) nunca vê esse
lead, e o funil (R-03) mostra "conectou" sem nunca mostrar "descartado".

| # | Ação |
|---|---|
| D1 | If/Else | A tentativa foi de WhatsApp? (mesma checagem do nó 2) → Math: `Conexões WhatsApp` + 1. Senão → Math: `Conexões telefone` + 1 — **é conexão real, conta igual ao ramo `Atendeu`** |
| D2 | Math: `Total de conexões` + 1 |
| D3 | Update: `WA não atendidas seguidas` = 0 |
| D4 | Add Contact Tag `conectado-hoje` |
| D5 | Remove Contact Tag `fila-tel`, `fila-wa` |
| D6 | If/Else múltiplo (Condition) | por `Motivo da desqualificação` — ver a tabela completa de ramos na seção 4.1 (F-12): `Timing errado` sai por `abandoned`+`nutricao-90d` como antes; os outros cinco valores saem por `lost` **e** agora também gravam o `Lost Reason` nativo da oportunidade com o mesmo valor |
| D7 | Add Note `Desqualificado na T{{contact.tentativa_n}} — motivo: {{contact.motivo_da_desqualificao}}` |

Sem nó de mudança de etapa: a oportunidade **fica em `CONECTAR`** (mesmo
padrão do ramo `Número errado`, que também sai só por `status`) — o Mestre
de saída (seção 3) já dispara pelo `Opportunity Status Changed` para
`lost`/`abandoned` e limpa o resto. O critério do D6 é o mesmo já usado pelo
Loop do closer (seção 5.1, ramos `Parcial`/`Não, Timing errado` vs. `Não`,
qualquer outro motivo) — reaproveitado de propósito, para o SDR e o closer
nunca decidirem "isso é reciclável" por réguas diferentes. `Motivo da
desqualificação` (C-16) é o mesmo campo do F-03, escrito pelo SDR aqui
**antes** da reunião existir — não há conflito porque só um dos dois
(SDR ou closer) preenche por oportunidade nesta passagem pela cadência: quem
vira `Desqualificado` aqui nunca chega ao Loop do closer, e quem chega ao
Loop do closer nunca passou por este ramo na mesma tentativa.

**Pronto quando:** um "atendeu, mas claramente não serve" vira `status`
`lost`/`abandoned` na hora, sem gerar `[CONECTADO] Qualificar e agendar` e
sem abrir horário na agenda do closer.

#### Ramo `Caixa Postal` e ramo `Não atendeu` (idênticos)
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
| 3 | If/Else: o contato tem e-mail ou Instagram? → Update Opportunity `status` = `abandoned` + tag `nutricao-90d`. Senão → Update Opportunity `status` = `lost` |
| 4 | Internal Notification para o gestor: `Telefone inválido: {{contact.name}} — revisar a fonte da lista` |

Número errado não é culpa do lead: se há outro canal, ele vira nutrição em vez
de lixo. A oportunidade **permanece** em `CONECTAR` nos dois casos (tabela
1.0) — é o `status`, não a etapa, que muda; o gatilho `Opportunity Status
Changed` do Mestre de saída (seção 3) dispara a limpeza mesmo sem movimento
de etapa.

#### Ramo `Pediu retorno`
| # | Ação |
|---|---|
| 1 | Update: `Prioridade` = 5 |
| 2 | Remove Contact Tag `fila-tel`, `fila-wa` |
| 3 | Add Contact Tag `fila-quente` |
| 4 | Add Task `[RETORNO] Ligar de volta` · vence: `Data de retorno` (S-01, `DATE`, **já existe na tela** — `contact.data_de_retorno`) ou hoje+1 se vazio · Atribuir: `Contact Owner` (dinâmico, R-10) |
| 4b | No corpo da tarefa, incluir `Horário combinado: {{contact.hora_do_retorno}}` — o par `TEXT` de S-01 existe desde 21/09/2026 23:18 (placeholder `HH:MM`) |

**A lacuna L-01 deixou de ser falta de campo — atualizado em 22/09/2026.** Os
dois campos de S-01 existem na tela: `Data de retorno` (`DATE`) desde 18/09 e
`Hora do retorno` (`TEXT`, placeholder `HH:MM`) desde 21/09 23:18. O que
sobrou é fiação, e uma pergunta de tela: o seletor de vencimento do `Add
Task` aceita a **data** de um campo personalizado, mas **não está verificado**
se aceita hora vinda de um `TEXT`. Por isso o nó 4b põe o horário no corpo da
tarefa, que funciona sempre — o SDR lê `Horário combinado: 15:30` ao abrir a
tarefa mesmo que o vencimento fique no dia. Se a tela aceitar hora dinâmica,
o 4b passa a ser redundante e pode sair; até alguém conferir, ele é o
caminho garantido. A lista "Retornos" (8.4) ordena o dia por
`Hora do retorno` de qualquer jeito, que era a outra metade da L-01. Não há
mais nó de mudança de etapa aqui: `Retorno agendado` deixou de ser etapa
própria (tabela 1.0) — o lead **fica em `CONECTAR`**, e a lista `Retornos`
(8.4) filtra só pelo valor de `Resultado da tentativa`, sem OR de etapa. Por
ficar em `CONECTAR` com `status` ainda `open`, este ramo **não** aciona o
Mestre de saída — correto: pedir retorno não é sair de cadência, é continuar
nela com prioridade alta.

#### Ramo `Não ligar`
| # | Ação |
|---|---|
| 1 | Add Contact Tag `nao-perturbe` |
| 2 | **Set Contact DND** = ligado (todos os canais) |
| 3 | Remove Contact Tag `fila-tel`, `fila-wa`, `fila-quente` |
| 4 | **Remove Workflows** — opção **All Except Current Workflow** (F-05, achado de 21/09/2026 — mesma troca da seção 3, ver a nota lá; substitui a lista antiga `Cadência 12x30`/`Cadência Inbound`/`Reengajamento 90 dias`/`Qualificação por IA no WhatsApp`, que também nunca cobriu as Interceptações de Sinal) |
| 5 | Update Opportunity `status` = `lost` |
| 6 | Add Note `Opt-out registrado em {{right_now}}` |

**Por que o nó 4 está aqui, e não só no Mestre de saída:** o nó 5 muda
`status` para `lost` e isso aciona o Mestre de saída, que já remove o
contato de toda régua ativa (seção 3, nó 2, mesma ação `Remove Workflows`) —
mas entre o nó 4 e a limpeza do Mestre de saída chegar existe uma janela de
segundos, e o que pode cair nela é uma mensagem ou uma tarefa de ligação
para alguém que **acabou de pedir para não ser procurado**. É o erro mais
caro da operação inteira (o DND do nó 2 cobre o canal, não a tarefa que o
SDR já vê na tela).

Etapa também fica em `CONECTAR` aqui — só o `status` muda. O nó 4 já tira o
contato de toda régua ativa na hora (não depende de esperar o Mestre de
saída reagir ao `status`), então o opt-out é imediato mesmo se o gatilho de
`Opportunity Status Changed` atrasar.

O DND nativo é o que impede qualquer canal de mandar mensagem. **Até
21/09/2026** este parágrafo dizia que a tag sozinha não segurava, porque
"workflow novo que ninguém lembrou de filtrar volta a incomodar o lead" —
esse risco específico (lista de nomes desatualizada) não existe mais desde
a troca para `Remove Workflows`/`All Except Current Workflow` (nota da
seção 3): um workflow novo nunca precisa ser adicionado a lugar nenhum para
ser coberto aqui. O nó continua não-negociável mesmo assim — é a única
linha de defesa contra uma mensagem que já estava saindo no mesmo instante
por outro workflow em execução (a mesma janela de corrida que a seção 2.9.5
documenta como limite conhecido, não deste nó).

---

## 4.1 Motivo de perda — espelhando no `Lost Reason` nativo da oportunidade (F-12)

**Por quê:** `Motivo da desqualificação` (C-16) existe desde 18/09/2026 e é
preenchido por SDR e closer (R-18, F-03), mas nada no projeto agrega esse
valor — a seção 9.1 e a lista 8.5 do Loop do closer só o exibem coluna a
coluna, contato por contato. O Dashboard do Gestor (seção 2.17, R-15) já
tinha documentado por quê: Custom Metrics só agrega por **tag** ou por soma
de campo `NUMERICAL`/`MONETARY` — nunca por valor de um `SINGLE_OPTIONS`.
Resultado: a pergunta que todo gestor de pré-vendas faz ("por que estamos
perdendo, na maioria das vezes?") não tem resposta sem abrir oportunidade
por oportunidade e contar na mão — o mesmo problema que R-01/R-03/F-06 já
resolveram para outras perguntas, nunca para esta.

Pesquisado antes de desenhar (o mesmo hábito que já achou o `Transcript
Generated` do F-06 e o `Customer Service Window Check` do G-05): o GHL **já
tem** um objeto nativo para isto, **em nível de oportunidade**, chamado
`Lost Reason` — configurado em Settings → Custom Fields → `Lost Reason` →
Bulk Actions → Edit (é um campo reservado da plataforma, por isso não
aparece na listagem de `locations_get-custom-fields`, que só traz os 51
campos de verdade personalizados). Confirmado por convergência de fontes
independentes (`WebSearch`, domínios de suporte da HighLevel bloqueados
pelo proxy deste ambiente como sempre — achado por citação, confiança
média, não testado nesta subconta): a plataforma expõe, de graça, o que
este projeto reinventou parcialmente sem o alcance completo —

1. **Relatório nativo** de quebra por motivo de perda (Reporting → Pipeline)
   e **coluna própria na exportação** de oportunidades — a agregação que a
   seção 2.17 já tinha descartado por falta de recurso nativo existia, só
   não no lugar que o projeto tinha olhado (Custom Metrics, não Pipeline
   Report).
2. **Filtro de gatilho** — `Lost Reason` está disponível como condição em
   `Opportunity Created/Changed`, `Opportunity Status Changed`,
   `Stale Opportunities` e `Pipeline Stage Changed`, e como valor de
   `If/Else`. Nenhuma automação deste projeto usa isso hoje — é capacidade
   nova, não uma peça faltando (ver "O que isto abre" abaixo).
3. **Ação nativa** — a ação de workflow `Create/Update Opportunity` aceita
   gravar `Lost Reason` no mesmo nó que muda `status`, o mesmo padrão já
   usado neste documento para `status`/etapa juntos.

**Por que não é substituir `Motivo da desqualificação` por `Lost Reason`, e
sim espelhar os dois:** `Motivo da desqualificação` é campo de **contato**,
lido pelo script de ligação (`script-de-ligacao.md`) e pela nota do D7/do
nó 3 da seção 5.1 — e regra 1 do projeto proíbe excluir campo já em uso.
`Lost Reason` é de **oportunidade**, existe só para desbloquear relatório e
gatilho nativos. Os dois convivem: o SDR/closer continua preenchendo um
campo só (`Motivo da desqualificação`), e o workflow, no mesmo nó que já
muda `status` para `lost`, espelha o valor no `Lost Reason` — zero campo
extra para quem opera, zero decisão dupla.

**Como (a tabela completa de ramos que a seção 4 e a seção 5.1 referenciam):**

| `Motivo da desqualificação` | Ação |
|---|---|
| `Timing errado` | Update Opportunity `status` = `abandoned` + Add Contact Tag `nutricao-90d` — **sem** `Lost Reason`: a oportunidade nunca chega a `lost` por este ramo, e o campo nativo é da plataforma para "perdido", não para "nutrição" |
| `Sem fit` | Update Opportunity `status` = `lost` **+ Lost Reason** = `Sem fit` |
| `Sem budget` | Update Opportunity `status` = `lost` **+ Lost Reason** = `Sem budget` |
| `Não é decisor` | Update Opportunity `status` = `lost` **+ Lost Reason** = `Não é decisor` |
| `Concorrente` | Update Opportunity `status` = `lost` **+ Lost Reason** = `Concorrente` |
| `Duplicado ou já cliente` | Update Opportunity `status` = `lost` **+ Lost Reason** = `Duplicado ou já cliente` |
| (vazio) | Update Opportunity `status` = `lost`, sem `Lost Reason` — nada para espelhar; mesmo comportamento de hoje |

Esta é a tabela que o D6 (seção 4, ramo `Desqualificado` do Pós-ligação) e o
ramo `Não`/qualquer motivo do nó 4 (seção 5.1, Loop do closer) usam — cinco
valores, não os seis do campo, porque `Timing errado` nunca chega a `lost`
(tabela acima). **Pré-requisito de tela, fora de qualquer API:** os cinco
valores precisam existir em Settings → Custom Fields → `Lost Reason` antes
de montar os nós — mesma classe de trabalho manual que criar opção em
campo personalizado (nunca sai por API, `APROVADO.md` não se aplica porque
não é escrita neste conector).

**A confirmar na tela, honestamente não testado nesta subconta:** (a) se o
seletor de `Lost Reason` dentro da ação `Update Opportunity` aceita ser
preenchido por um valor fixo por ramo (o desenho acima assume isso, do
mesmo jeito que `Pipeline Stage` já exige seleção fixa em vez de merge
field neste projeto) — se a tela expuser um jeito de ler o valor
dinamicamente de `Motivo da desqualificação` em vez de um ramo por valor, o
desenho colapsa para um único nó, mais simples que o daqui; (b) se
`Lost Reason` é gravável quando o `status` do mesmo nó é `abandoned` — a
tabela acima assume que não (é recurso de "perdido", não de "nutrição") e
por isso não tenta.

#### Conferência do F-12, 22/09/2026 (mesma rodada): a dúvida (a) é mais séria do que "a confirmar", e há dois fatos novos

**1. Existe fonte contrária à premissa central, e ela precisa estar escrita
aqui.** A pesquisa desta conferência achou, no próprio canal de ideias da
HighLevel, um pedido aberto de usuários para **poder referenciar `Lost Reason`
em automações e usá-lo como gatilho**, com a observação de que isso **não está
disponível**. Isso não refuta o desenho — pedidos envelhecem, e outra fonte da
mesma busca menciona um recurso já entregue de *editar* `Lost Reason` em
Settings → Custom Fields —, mas muda o peso da dúvida (a): a possibilidade de o
seletor de `Lost Reason` **não existir de jeito nenhum** dentro da ação
`Update Opportunity` deixa de ser remota. Consequência prática: **escreva o
plano B como caminho de verdade, não como nota de pé de página.**

| Se a tela… | Então |
|---|---|
| oferecer `Lost Reason` com valor **fixo** na ação | o desenho acima vale como está (cinco ramos) |
| oferecer com valor **dinâmico** | colapsa para um nó só, melhor |
| **não oferecer** `Lost Reason` na ação | **plano B:** o `Lost Reason` passa a ser escolha **manual** de quem marca `lost` na tela — SDR no Pós-ligação, closer no Loop —, e o par `Motivo da desqualificação` (campo de contato, gravado pela régua) + `Lost Reason` (objeto de oportunidade, escolhido na mão) convivem. O relatório de quebra por motivo continua funcionando; o que se perde é a garantia de que os dois sempre batem, e aí a auditoria do item 3 abaixo passa a ser obrigatória, não opcional |

Esta terceira linha também desmente, por precaução, a afirmação de que
`Lost Reason` está "disponível como condição em quatro gatilhos de workflow":
não encontrei confirmação disso, e encontrei o oposto no pedido acima. Tratar
como **não confirmado** até alguém abrir a tela — e o item "o que isto abre"
abaixo (diferenciar o Reengajamento por motivo) depende justamente desse filtro
de gatilho, então ele é mais especulativo do que parecia.

**2. `Lost Reason` criado nunca pode ser apagado.** A mesma pesquisa: *once a
Lost Reason is created, it cannot be deleted and will remain in the dropdown
list forever.* Consequência direta para o pré-requisito de tela: os cinco
valores têm de nascer **com o texto exato** de `Motivo da desqualificação`
(C-16) na primeira vez — `Sem fit`, `Sem budget`, `Não é decisor`,
`Concorrente`, `Duplicado ou já cliente`. Errar o rótulo aqui não se corrige,
só se abandona, e o dropdown fica com o errado e o certo lado a lado para
sempre. É a regra 1 do briefing ("nunca exclua") imposta pela própria
plataforma, e vale escrever antes de alguém digitar às pressas.

**3. Assimetria de API medida agora, e ela torna o item auditável sem tela.**
O `lostReasonId` **vem** na resposta de `opportunities_search-opportunity` (já
apareceu, como `null`, nas leituras de oportunidade desta sessão). E o schema de
`opportunities_update-opportunity` **não tem** nenhum parâmetro de `lostReason`
(conferido campo a campo: `name`, `pipelineId`, `pipelineStageId`, `status`,
`monetaryValue`, `assignedTo`, `customFields`). Ou seja:

> **legível por API, não gravável por este conector.**

A metade "não gravável" confirma o que o item já dizia. A metade **legível** é
nova e útil: o "Pronto quando" desta seção depende hoje de olhar
Reporting → Pipeline na tela, e passa a ter uma verificação automática —
`opportunities_search-opportunity` filtrando `status = lost` e conferindo que
**todo** resultado tem `lostReasonId` preenchido. Uma oportunidade `lost` com
`lostReasonId: null` é exatamente a divergência que o item existe para impedir,
e agora dá para achá-la de fora, em qualquer rodada, sem depender de ninguém
abrir a tela. Vale ainda mais no plano B acima, onde o preenchimento é manual e
portanto esquecível.

**O que isto abre, sem construir agora (registrado para não se perder, não
é parte do "Pronto quando" desta rodada):** com `Lost Reason` alimentado, o
Reengajamento 90 dias (seção 2.12) poderia um dia diferenciar a régua por
motivo — um lead perdido por `Concorrente` provavelmente não vale
reativação automática de conteúdo, um perdido por `Sem budget` talvez valha
um ciclo mais longo — usando o filtro nativo de `Lost Reason` no gatilho em
vez de reler o campo de contato. Não desenhado: é otimização sobre uma
régua que já existe e funciona, não lacuna aberta.

**Pronto quando:** todo lead que sai por `lost` com `Motivo da
desqualificação` preenchido (D6 da seção 4, nó 4 da seção 5.1) também tem o
`Lost Reason` nativo da oportunidade gravado com o mesmo valor, e o
Reporting → Pipeline do GHL mostra a quebra por motivo sem precisar abrir
oportunidade por oportunidade.

---

## 5. Workflow "Pós-agendamento" — migrado para as 5 etapas reais em 19/09/2026

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
| 1 | Mover oportunidade → `NEGOCIAR` | Aciona o Mestre de saída (a etapa muda de `CONECTAR`/`AGENDAR` para `NEGOCIAR` — tabela 1.0) |
| 2 | Update Contact Field | `Data agendado` = `{{right_now}}` (R-03 — marca o instante em que o SDR agendou, não o horário da reunião) |
| 3 | **Remove Workflows** — opção **All Except Current Workflow** (F-05, achado de 21/09/2026 — mesma troca da seção 3; substitui a lista antiga de seis nomes, incluindo `Recuperação de No-show`/`SLA do Closer — No-show`, R-12: este gatilho também dispara num **reagendamento** depois de um no-show, e sem remover os dois workflows de no-show daqui uma recuperação em curso continuaria mandando NS2/NS3 para um lead que já remarcou — a opção `All Except Current` cobre os dois sem precisar sabê-los pelo nome) |
| 4 | Math Operations em série | Calcula `Nota de qualificação` (seção 9.1) |
| 5 | Update Contact Field | `Prioridade` = 5 |
| 6 | Add Note | Resumo da qualificação (modelo abaixo) |
| 7 | Guarda de janela (G-05) → Send WhatsApp | Confirmação imediata ao lead — dentro da janela: texto livre `PA-CONF` · fora da janela: Template Meta `PA-CONF` (`biblioteca-mensagens.md`) → Update `Template usado` = `PA-CONF` |
| 8 | Wait até 24h antes → Guarda de janela (G-05) → Send WhatsApp | Lembrete — dentro da janela: texto livre `PA-R24` · fora da janela: Template Meta `PA-R24` → Update `Template usado` = `PA-R24` |
| 9 | Wait até 3h antes → Guarda de janela (G-05) → Send WhatsApp | Lembrete — dentro da janela: texto livre `PA-R3H` · fora da janela: Template Meta `PA-R3H` → Update `Template usado` = `PA-R3H` |
| 10 | Wait até 30min antes → Guarda de janela (G-05) → Send WhatsApp | Lembrete curto — dentro da janela: texto livre `PA-R30` · fora da janela: Template Meta `PA-R30` → Update `Template usado` = `PA-R30` |

**Guarda de janela nos nós 7-10 (G-05, peça 2):** mesmo mecanismo da seção
2.6.2 — `WhatsApp: Customer Service Window Check` antes de cada envio, ramo
dentro da janela segue com o texto livre já especificado, ramo fora da
janela usa `Send WhatsApp` modo Template. Diferença destes quatro para os
pontos de envio já cobertos: nenhum dos quatro tinha código nem texto
versionado em `biblioteca-mensagens.md` antes desta rodada — a confirmação
(nó 7) já tinha texto solto no modelo abaixo, sem código; os três lembretes
(nós 8-10) não tinham texto nenhum. Os quatro ganharam código (`PA-CONF`,
`PA-R24`, `PA-R3H`, `PA-R30`) e texto nesta rodada, porque não dá para
montar o ramo Template de uma guarda sem saber qual texto livre ele
substitui fora da janela.

**Por que o nó 3 existe, e por que virou `Remove Workflows` em vez de lista
(19/09/2026, atualizado 21/09/2026):** o nó 1 move a etapa para `NEGOCIAR` e
isso aciona o Mestre de saída, que já remove o contato de toda régua ativa
(seção 3, nó 2) — mas o Mestre roda como workflow separado, e o nó 3 existe
justamente para fechar a janela de segundos entre "agendou" e "a limpeza
chegou". Um lead que agenda no meio de qualquer régua (inbound, no-show,
reengajamento) podia receber uma tentativa nesse intervalo. Até 21/09/2026
esta lista tinha o mesmo problema documentado na seção 3: nasceu com uma
régua, precisou de dois nomes a mais em 19/09/2026, e ainda não cobria as
Interceptações de Sinal. A troca para `Remove Workflows`/`All Except
Current Workflow` (nota da seção 3) fecha isso pelo mesmo motivo: nenhum
nome para esquecer. **Retoque de tela:** este workflow está publicado e
ativo — a troca de nó é retoque na tela (ver a tabela de retoques no
`GUIA-MONTAGEM.md`).
| 11 | Assign to User | Closer dono do horário |
| 12 | Internal Notification | E-mail + SMS para o closer — **este SMS é para a sua equipe, não para o lead**, então a decisão "sem SMS" de 19/09/2026 não o alcança; se preferir só e-mail, é trocar aqui |

Nos nós 8–10 use Wait → "relativo ao início do compromisso" (Appointment Start
Date), não delay fixo: reagendamento move os lembretes junto.

**Modelo da nota (nó 6)**

Merge tags corrigidos em 19/09/2026 contra o fieldKey real (lido por
`locations_get-custom-fields`): o GHL não transliteral o nome pro fieldKey,
ele **remove** a letra acentuada inteira (ex.: "anúncios" → `anncios`, não
`anuncios`; "qualificação" → `qualificao`). A versão anterior deste modelo
usava a transliteração "limpa", que não bate com nada e faria a nota sair com
os placeholders em branco. `Empresa` também trocou de nativo para
personalizado — ver nota da seção 7.2.
```
REUNIÃO AGENDADA · nota {{contact.nota_de_qualificao}}/100
Agendado por: {{user.name}} · Para: {{appointment.start_time}}

Empresa: {{contact.empresa}} · Segmento: {{contact.segmento}}
Site: {{contact.site}} · IG: {{contact.instagram}}

BANT
Budget: {{contact.budget}} · Decisor: {{contact.decisor}} · Prazo: {{contact.prazo}}

Diagnóstico
Clientes novos/mês: {{contact.clientes_novos_por_ms}}
Anúncios: {{contact.investe_em_anncios}} · Investimento: {{contact.investimento_mensal_em_anncios}}
Plataformas: {{contact.plataformas_de_anncio}}
Agência: {{contact.j_teve_agncia}} — {{contact.experincia_com_agncia}}
Time: {{contact.tem_time_comercial}} · Atende leads: {{contact.quem_atende_os_leads}}
CRM: {{contact.usa_crm}} · Canal principal: {{contact.canal_principal_de_venda}}

Dor principal: {{contact.dor_principal}}
Preenchido por: {{contact.qualificao}}
Histórico: {{contact.total_de_ligaes}} ligações, {{contact.total_de_conexes}} conexões, atendeu na T{{contact.tentativa_n}}
```

**Mensagens dos nós 7-10 — `PA-CONF`/`PA-R24`/`PA-R3H`/`PA-R30`:** texto,
código e histórico de versão moram em `biblioteca-mensagens.md` (mesma regra
da seção 2.6, "texto duplicado em dois documentos diverge na primeira
edição") — não repetidos aqui.

**Limite conhecido, não escondido (achado nesta rodada, G-05 peça 2):**
`PA-CONF` promete "vou te mandar o link aqui mesmo 30 min antes", mas este
documento não especifica nenhum merge field nem nó que grave ou leia um
link de reunião — nem `{{appointment}}` nem os campos personalizados da
seção 0.3 (`IMPLEMENTACAO-WORKFLOWS.md`) têm um. `PA-R30` (nó 10, o "30 min
antes" que a promessa cita) por isso não afirma anexar link nenhum no
texto — só confirma o horário. A entrega do link em si continua dependendo
do e-mail de confirmação automática do calendário (seção 7.1, "Confirmação
automática: Ligada") ou de o SDR/closer mandar manualmente; nenhum dos dois
é workflow, então nenhum sai por API. Lacuna pré-existente a este item, não
criada por ele — registrada aqui por ter sido notada só agora, ao escrever
o texto de verdade para os quatro nós.

---

## 5.1 Workflow "Loop do closer — veredito pós-reunião" — F-03 — migrado para as 5 etapas reais em 19/09/2026

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
| 3 | Registro | Add Note | `Veredito do closer: {{contact.reunio_foi_qualificada}} · motivo: {{contact.motivo_da_desqualificao}} · nota do SDR/IA na hora: {{contact.nota_de_qualificao}}` |
| 4 | Roteamento | If/Else múltiplo por `Reunião foi qualificada` | ver ramos abaixo |
| 5 | **Alerta de calibração (alta)** | If/Else | `Nota de qualificação` ≥ 70 **E** `Reunião foi qualificada` = `Não` → Internal Notification ao gestor: `Nota {{contact.nota_de_qualificao}} mas o closer marcou Não ({{contact.motivo_da_desqualificao}}) — revisar a régua da seção 9 com {{contact.name}}.` |
| 6 | **Alerta de calibração (baixa)** | If/Else | `Nota de qualificação` < 45 **E** `Reunião foi qualificada` = `Sim` → Internal Notification ao gestor: `Nota baixa ({{contact.nota_de_qualificao}}) mas o closer marcou Sim — a régua pode estar descartando lead bom. Revisar {{contact.name}}.` |

Os cortes 70 e 45 dos nós 5 e 6 não são novos: são as mesmas fronteiras das
faixas A/B da seção 9.1. Reaproveitar evita uma segunda régua para a régua.

#### Ramos do nó 4
| Veredito | Ação |
|---|---|
| `Sim` | Nenhuma mudança de etapa **nem de status**. A oportunidade segue `open` em `NEGOCIAR` — é o closer, fora deste workflow, que a leva a `FORMALIZAR` quando fechar |
| `Parcial` | Update Opportunity `status` = `abandoned` (sem sair de `NEGOCIAR` — tabela 1.0, `Nutrição` não é etapa própria) + Add Contact Tag `nutricao-90d` |
| `Não`, motivo = `Timing errado` | Mesma ação da linha `Parcial`: `status` = `abandoned` + tag `nutricao-90d` (sem fit **agora** não é sem fit nunca) |
| `Não`, qualquer outro motivo | Update Opportunity `status` = `lost` (sem sair de `NEGOCIAR` — tabela 1.0, `Descartado` não é etapa própria) **+ Lost Reason** = mesmo valor de `Motivo da desqualificação`, mesmo mapeamento da tabela da seção 4.1 (F-12) — SDR (D6, seção 4) e closer decidem por réguas diferentes quando é `lost`, mas o motivo nativo grava pelo mesmo critério nos dois lugares |

**Achado desta migração:** nenhum destes três ramos move a oportunidade
para fora de `NEGOCIAR` — só o `status` muda. Isso é diferente da maioria
das outras saídas de cadência (que mudam status **dentro de `CONECTAR`**):
aqui o "sair" acontece depois de já ter avançado para `NEGOCIAR` pelo Pós-
agendamento (seção 5, nó 1). O Mestre de saída (seção 3) não reage a isto —
seu portão só olha `CONECTAR`+`open` — e não deveria mesmo: a limpeza de
fila (`fila-tel`/`fila-wa`) já rodou quando o lead conectou (seção 4, ramo
`Atendeu`), não há fila para limpar de novo aqui.

O motivo só decide o destino quando o veredito é `Não`; `Parcial` já é
tratado como nutrição direto, sem olhar o motivo — é o mesmo critério do ramo
`Não`/`Timing errado`, então não duplico a checagem.

**Pronto quando (herdado do F-03 no roadmap):** dá para dizer "nota ≥ 70
acerta X%" sem planilha (lista 8.7), e o gestor sabe de uma nota mal calibrada
no dia da reunião, não no fechamento do mês.

---

## 5.2 Workflow "Registro de Comparecimento" — R-03 — conferido para as 5 etapas reais em 19/09/2026, sem mudança

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
| 3 | Update Contact Field | `Nº de no-shows` = 0 (R-12 — comparecer de verdade reinicia a contagem; a regra de descarte automático da seção 5.3 é sobre no-show **consecutivo**, não sobre o histórico de vida do lead) |
| 4 | Add Note | `Compareceu à reunião · {{right_now}}` |

Não mexo em etapa aqui: comparecer não move a oportunidade (quem decide o
destino é o veredito do closer, seção 5.1). Este workflow só marca o carimbo
que a seção 8 lê.

**Pronto quando (compõe o R-03 no roadmap):** existe carimbo de "compareceu"
tão confiável quanto os de "conectou" e "agendou" — os três lidos pelas
listas 8.10 a 8.12.

---

## 5.3 Workflow "Recuperação de No-show" — R-12 — migrado para as 5 etapas reais em 19/09/2026

A seção 5 fecha o agendamento e a 5.2 confirma o comparecimento; nenhuma das
duas trata o meio-termo, que é o vazamento mais caro do funil: reunião
marcada, closer de agenda reservada, lead que simplesmente não aparece. Hoje
isso morre em silêncio — a oportunidade fica parada em `NEGOCIAR` para
sempre, e ninguém tenta de novo.

Pesquisado antes de desenhar: Outreach e Salesloft resolvem isso via
integração com uma ferramenta de agendamento de terceiro (Chili Piper é o
exemplo mais citado), que dispara a sequência de recuperação quando o status
do compromisso muda — nenhum dos dois faz isso nativamente, sozinho. A
literatura de operação de vendas recomenda uma mensagem automática de "sentimos
sua falta" imediata, e escalar para contato pessoal de um closer/AE dentro de
1 hora útil quando o lead vale a pena. O GHL tem o gatilho nativo
`Appointment Status = No Show` desde a primeira versão testada neste projeto
(mesma família do `Showed` da seção 5.2) — dá para replicar o miolo do que um
Chili Piper faz, sem ferramenta de terceiro nenhuma.

**A decisão que um concorrente não copia olhando a tela:** depois do 2º
no-show seguido do mesmo lead, o `status` da oportunidade vira `lost` (sem
sair de `NEGOCIAR` — seção abaixo), sem gerar nenhuma tarefa nova — regra
de proteção da agenda do closer. Reev,
Meetime, Outreach e Salesloft tratam no-show repetido como métrica de
relatório ("taxa de no-show por rep"), nunca como gatilho de decisão
automática. Aqui vira decisão porque o custo de ligar uma terceira vez para
quem já furou duas reuniões marcadas é maior que o valor esperado do lead —
e ninguém precisa lembrar de aplicar esse corte na mão.

### Por que fica em `NEGOCIAR`, não volta para `CONECTAR`

O Reengajamento 90 dias (seção 2.12, R-08) já pagou o preço de aprender que
devolver um lead para `CONECTAR` esbarra no `Allow Re-entry` desligado da
Cadência 12x30 (D-06) — um contato que já passou por aquele workflow uma vez
fica bloqueado de entrar de novo nele para sempre, gatilho ou `Add to
Workflow`, e resolver isso exigiu tag de blindagem (`reengajamento-ativo`) e
mudar a origem do lead. Este item não paga esse preço porque não tenta
reentrar na 12x30 de jeito nenhum: a oportunidade nunca sai de `NEGOCIAR`,
o contador `Nº de no-shows` mora no contato (não numa etapa nova) e a régua
de recuperação roda num workflow próprio, pequeno, do mesmo jeito que já
separou a Cadência Inbound (2.10) e o Reengajamento (2.12) da 12x30.
Resultado: **zero tag nova e zero etapa nova** para este item — só o contador
`Nº de no-shows` (C-24, `campos-e-tags.md`).

### Por que dois workflows, não um

Mesmo raciocínio já registrado na seção 5.2 ("são dois eventos... em
momentos diferentes... misturar os dois faria o segundo gatilho reabrir
nós que já rodaram") — aqui os dois eventos são **simultâneos**, não
sequenciais, e o motor de workflow do GHL não bifurca um nó em dois
caminhos que continuam em paralelo (só via `If/Else`/`Split`, que escolhem
**um** caminho, nunca os dois ao mesmo tempo). A régua de recuperação (este
workflow) e o SLA do closer (seção 5.4) têm relógios diferentes e não podem
disputar o mesmo fio de execução — a saída nativa, já usada pela seção
5/5.1/5.2 para o mesmo problema, é dois workflows curtos escutando o mesmo
gatilho.

### Gatilho

**Appointment Status** — Calendário: `Reunião com closer` · Status: `No Show`

### Configurações

| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | Um reagendamento pode gerar um novo `No Show` no futuro — mesmo motivo da seção 5.2 |
| Janela de envio | 08:30 às 18:30, segunda a sexta, fuso da subconta | A tarefa e a mensagem ao lead não devem nascer fora do expediente do SDR |
| Stop on Response | **Ligado** | Respondeu em qualquer canal encerra a recuperação — o SDR assume dali, mesma regra da cadência principal |

### Nós

| # | Ação | Configuração |
|---|---|---|
| 1 | Portão de sanidade | If/Else — etapa da oportunidade **é** `NEGOCIAR` **E** `status` **é** `open` → segue. Senão → **encerra** (o compromisso já não reflete o estado atual do lead; evita reabrir um no-show velho de uma oportunidade que já foi resolvida por outro caminho — inclusive pelo Loop do closer, seção 5.1, que pode ter marcado `status = abandoned/lost` **sem sair de `NEGOCIAR`**, e nesse caso um `No Show` chegando depois não deveria reabrir nada) |
| 2 | Contador | Math Operation — `Nº de no-shows` + 1 |
| 3 | Portão de repetição | If/Else — `Nº de no-shows` ≥ 2 → **ramo Descarte** (abaixo). Senão → **ramo Recuperação** (abaixo) |

#### Ramo Descarte (2º no-show seguido, ou mais)

| # | Ação |
|---|---|
| 1 | Remove Contact Tag `fila-tel` (idempotente, mesmo se ausente) |
| 2 | Add Contact Tag `limpar-tarefas` |
| 3 | Update Opportunity `status` = `lost` (sem sair de `NEGOCIAR` — tabela 1.0; aciona o Mestre de saída pelo gatilho 2 dele, `Opportunity Status Changed`, que não filtra por etapa e por isso faz o resto da limpeza mesmo com a etapa continuando `NEGOCIAR`) |
| 4 | Add Note `Descartado após {{contact.n_de_noshows}}º no-show seguido sem reagendar — regra de proteção de agenda do closer (R-12)` |
| 5 | Internal Notification ao gestor `{{contact.name}} descartado automaticamente após {{contact.n_de_noshows}}º no-show — nenhuma ação necessária, é a regra de proteção de agenda` |

#### Ramo Recuperação (1º no-show)

| # | Ação | Configuração |
|---|---|---|
| 0 | Guarda de janela de atendimento (seção 2.6.2, G-05) | Dentro da janela → 1 · Fora da janela → 1T |
| 1 | Send WhatsApp | Texto livre `NS-1` (`biblioteca-mensagens.md`) → 2 |
| 1T | Send WhatsApp, modo Template | Template Meta `NS-1` (a submeter — `biblioteca-mensagens.md`) → 2 |
| 2 | Update Contact Field | `Template usado` = `NS-1` (os dois ramos acima convergem aqui) |
| 3 | Add Contact Tag | `fila-tel` |
| 4 | Add Task | `[CADENCIA] NS1 · Ligar (telefone) — Recuperação de no-show` · vence hoje · Atribuir: `Contact Owner` (dinâmico, R-10) |
| 5 | Aguardar | Wait → Until specific time · D1 10:00 |
| 6 | Portão | If/Else — etapa ainda `NEGOCIAR` **E** `status` ainda `open` **E** `nao-perturbe` ausente **E** `pausado` ausente → segue. Senão → **Remove from Workflow: este** |
| 7 | Add Contact Tag | `fila-tel` |
| 8 | Add Task | `[CADENCIA] NS2 · Ligar (telefone) — Recuperação de no-show` · vence hoje · Atribuir: `Contact Owner` |
| 9 | Aguardar | Wait → Until specific time · D3 15:00 |
| 10 | Portão | Mesmo do nó 6 |
| 11 | Add Contact Tag | `fila-tel` |
| 12 | Add Task | `[CADENCIA] NS3 · Ligar (telefone) — Recuperação de no-show` · vence hoje · Atribuir: `Contact Owner` |
| 13 | Aguardar | Wait → Time Delay 1 dia (folga para o SDR classificar a NS3) |
| 14 | Portão | If/Else — etapa ainda `NEGOCIAR` **E** `status` ainda `open` → segue (ninguém reagendou nem descartou). Senão → **Remove from Workflow: este** |
| 14b | Guarda de janela de atendimento (seção 2.6.2, G-05) | Dentro da janela → 15 · Fora da janela → 15T |
| 15 | Send WhatsApp | Texto livre `NS-2` → 16 |
| 15T | Send WhatsApp, modo Template | Template Meta `NS-2` (a submeter — `biblioteca-mensagens.md`) → 16 |
| 16 | Update Contact Field | `Template usado` = `NS-2` (os dois ramos acima convergem aqui) |
| 17 | Update Contact Field | `Resultado da tentativa` = vazio |
| 18 | Remove Contact Tag | `fila-tel` |
| 19 | Add Contact Tag | `nutricao-90d` |
| 20 | Update Opportunity | `status` = `abandoned` (sem sair de `NEGOCIAR` — tabela 1.0; aciona o Mestre de saída pelo gatilho 2 dele, e 90 dias depois o próprio Reengajamento 90 dias — seção 2.12 — reativa o lead sozinho, sem workflow novo para o caminho "desistiu") |

Canal só telefone, de propósito: quem já demonstrou interesse suficiente
para marcar reunião com o closer merece o canal de maior esforço direto, não
a alternância WhatsApp/telefone da cadência fria — por isso este ramo não
usa `WA não atendidas seguidas` nem verifica `Permissão WhatsApp`.

Reaproveito o portão de pausa individual (R-09) e o de `nao-perturbe` nos
nós 6/10, mesmo raciocínio da seção 2.4: um lead pausado ou que pediu para
não ser mais procurado não deve receber NS2/NS3 só porque não-showou uma
reunião.

**Pronto quando (do roadmap):** um no-show gera a tarefa `[CADENCIA] NS1` no
mesmo dia — nova tentativa, não silêncio.

---

## 5.4 Workflow "SLA do Closer — No-show" — R-12 — migrado para as 5 etapas reais em 19/09/2026

O ramo Recuperação da seção 5.3 cobre o lado do SDR. Falta o lado do closer:
é quem tinha o horário reservado, quem mais rápido consegue julgar se vale a
pena insistir, e hoje nada cobra dele um retorno. Reev e Meetime tratam isso
como relatório mensal de "reuniões perdidas por closer" — o mesmo padrão que
o Loop do closer (seção 5.1, F-03) já rejeitou para o veredito pós-reunião,
por escolha deliberada de alertar no dia, não no relatório do mês. Este item
aplica o mesmo princípio ao no-show: um SLA com prazo, e uma cobrança visível
se ele estourar.

### Gatilho

Mesmo evento da seção 5.3 — **Appointment Status** — Calendário: `Reunião
com closer` · Status: `No Show`

### Configurações

| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | Mesmo motivo da seção 5.3 |
| Janela de envio | Sem janela | É aviso interno ao closer e ao gestor, não mensagem ao lead |
| Stop on Response | Desligado | Não há mensagem ao lead aqui |

### Nós

| # | Ação | Configuração |
|---|---|---|
| 1 | Portão | If/Else — etapa da oportunidade **é** `NEGOCIAR` **E** `status` **é** `open` → segue. Senão → **encerra** (mesmo raciocínio da seção 5.3, nó 1: um veredito já registrado pelo Loop do closer muda `status` sem tirar a oportunidade de `NEGOCIAR`) |
| 2 | Portão | If/Else — `Nº de no-shows` ≥ 2 → **encerra** (a seção 5.3 já decidiu descartar; cobrar retorno do closer aqui seria alertar para uma decisão que já foi tomada) |
| 3 | Alerta imediato | Internal Notification ao closer `{{contact.name}} não compareceu à reunião de {{appointment.start_time}}. A recuperação automática (NS1) já dispara em instantes — se preferir reagendar você mesmo agora, é mais rápido para o lead e evita o SDR ligar à toa.` |
| 4 | Aguardar | Wait → Time Delay 2h corridas |
| 5 | Portão | If/Else — etapa da oportunidade ainda **é** `NEGOCIAR` **E** `status` ainda `open` → segue (ninguém reagendou nem descartou nesse meio-tempo). Senão → **encerra** |
| 6 | Escalonamento | Internal Notification ao gestor `Closer não deu retorno em 2h após o no-show de {{contact.name}} ({{appointment.start_time}}) — a recuperação automática (NS1) já está tentando reconectar, mas vale conferir com o closer.` |

O nó 4 usa horas corridas, não úteis: como uma reunião só existe dentro da
janela de atendimento do closer (é o próprio calendário que a limita), o
gatilho `No Show` já nasce dentro do horário comercial — 2h corridas a
partir daí raramente cruzam a virada do dia. Não vale o custo de um relógio
de horário comercial para um caso de borda raro.

Se o lead reagendar dentro dessas 2h, o nó 3 do Pós-agendamento (seção 5)
já removeu este contato dos dois workflows do R-12 antes do nó 5 rodar — o
`Remove from Workflow` cancela qualquer `Wait` pendente, então o nó 6 nunca
dispara para quem já resolveu sozinho. Não preciso comparar "o valor de
`Nº de no-shows` mudou desde o nó 1": a remoção do workflow já resolve isso
sem campo auxiliar nenhum.

**Pronto quando (do roadmap, metade "SLA do closer"):** o gestor sabe de um
no-show sem retorno do closer em 2h, não no relatório do mês seguinte —
mesmo padrão de alerta em tempo real que a seção 5.1 já validou para o
veredito pós-reunião.

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

### 6.0 Guarda de janela na entrada — G-06

**Por quê:** a entrada deste workflow (seção 2.7) dispara pelo resultado de
uma tentativa de **ligação** (`Tentativa nº` ≥ 2 e `Resultado da tentativa`
≠ `Atendeu`), não por uma mensagem do lead no WhatsApp — nada garante que a
janela de atendimento de 24h (G-05, seção 2.6.2) já esteja aberta quando a
IA entra em cena. O G-05 fechou a guarda em todo `Send WhatsApp` de texto
livre da operação, mas a varredura que fechou aquele item nunca chegou
aqui: os textos deste workflow nunca entraram em `biblioteca-mensagens.md`
(o R-04 que criou aquele documento é de 18/09/2026, dois dias antes de o
G-05 existir), e sem linha na tabela de templates não havia o que a
varredura pudesse conferir — o mesmo padrão de "achado por ausência" que já
fechou outras lacunas deste projeto.

O Caminho A (recomendado, abaixo) é o caso mais exposto, não o mais seguro:
`Conversation AI` também entrega por WhatsApp Business API — pesquisado via
`WebSearch` (confiança média, mesma limitação de proxy contra domínios de
suporte da HighLevel já registrada no G-05): a ação nativa manda "a single
AI-generated message to a contact" ao ser usada em workflow, e nenhuma fonte
lida sugere que ela seja isenta da janela — mas, diferente de `M1-a` ou
`MI-0`, o texto que a IA manda é **gerado no momento da conversa**, então
não existe um texto fixo para pré-aprovar como Template Meta (que exige
conteúdo estático). Sem guarda, a primeira mensagem da IA cairia fora da
janela na maioria dos casos e a Meta recusaria em silêncio — nem o lead
recebe nada, nem o SDR fica sabendo, porque essa falha não gera tarefa nem
aviso nenhum.

**Como:** a mesma guarda do G-05 (`WhatsApp: Customer Service Window
Check`), com uma saída diferente por não existir texto livre para
pré-aprovar aqui: em vez de um "Template equivalente ao texto de M1", a
guarda manda um convite fixo e curto (`QI-1`, novo, `biblioteca-mensagens.md`)
pedindo para o lead responder por ali — a resposta **reabre a janela** (é o
cliente escrevendo primeiro) e só então a IA assume a conversa:

| Nó | Ação | Configuração |
|---|---|---|
| G.1 | `WhatsApp: Customer Service Window Check` | Confere o contato ao entrar no workflow |
| G.2 (dentro da janela) | segue | direto para o nó 1 (Conversation AI), sem mudar nada |
| G.3 (fora da janela) | `Send WhatsApp`, modo **Template** → `Update Contact Field` | Template Meta `qi_1` (`QI-1`, `biblioteca-mensagens.md`) → `Template usado` = `QI-1` |
| G.4 | `Wait → Contact Replied`, tempo limite 24h | Respondeu: segue para o nó 1 (Conversation AI, agora dentro da janela que a própria resposta reabriu) |
| G.5 (sem resposta no prazo) | `Add Note` | `IA de qualificação: sem resposta ao convite de reabertura — segue só pela cadência de ligação` → fim do workflow. Não remove de nenhum outro workflow: a Cadência 12x30 principal não passa por aqui, continua sozinha |

Fora do escopo desta guarda, de propósito: marcar `QI-1` como um `toque`
(F-04, seção 2.19) — aquela seção já trata Cadência Inbound, Reengajamento e
Recuperação de No-show como pendência deferida pelo mesmo motivo (nenhuma
delas chega perto do teto sozinha); QI-1 entra na mesma fila, não é lacuna
nova desta rodada.

**Caminho B, fechado nesta rodada (peça 2):** tinha o mesmo problema em
**cada uma** das 8 perguntas, não só na primeira — o desenho original
assumia que, sem resposta em 24h, a pergunta seguinte saía de qualquer
forma (`pula para a pergunta seguinte`), e essa tentativa cairia fora da
janela de novo se a anterior nunca tivesse reaberto. Das duas saídas
cogitadas (Template por pergunta — 8 novos, inviável para um fluxo pensado
como conversa — ou reestruturar para só avançar depois de resposta de
verdade), a segunda venceu: cada bloco agora encerra o workflow em vez de
insistir sem garantia de janela. Detalhe nó a nó na seção "B — Sem
Conversation AI" abaixo.

**Pronto quando (cumprido):** todo envio de WhatsApp deste workflow —
Caminho A e Caminho B — tem guarda de janela, do mesmo jeito que o G-05 já
garante para o resto da operação.

### Estrutura
Duas formas de montar. Recomendo a **A**, agora precedida pela guarda 6.0.

**A — Conversation AI (Bot nativo), modo perguntas + agendamento**

Depois da guarda 6.0 (nós G.1-G.5), o nó 1 abaixo é o destino de G.2 e de
G.4 quando o lead responde:

Um nó `Conversation AI` com:
- Canal: WhatsApp
- Modo: Query + Appointment Booking
- Calendário: `Reunião com closer`
- Mapeamento de campos: cada pergunta grava no campo correspondente
- Limite: **uma pergunta por mensagem**, máximo 8 perguntas na conversa
- Ao fim (ou quando o lead demonstrar interesse): oferece o link do calendário
- Nó seguinte: Update `Qualificação` = `IA Whatsapp` (nome e opção reais da
  tela — `CONFERENCIA-CAMPOS.md`, Q-18: o campo nasceu `Qualificação`, não
  `Qualificação preenchida por`, e a opção é `IA Whatsapp`, com "W"
  minúsculo)

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
   -> Clientes novos por mês: 10 / 11-30 / 31-100 / +101 (rótulos reais da
      tela — `CONFERENCIA-CAMPOS.md`, Q-04)
3. Vocês investem em anúncio hoje?
   -> Investe em anúncios: Sim / Já investiu e parou / Nunca
4. Se sim: quanto mais ou menos por mês? -> Investimento mensal em anúncios
   E em quais plataformas? -> Plataformas de anúncio
5. Já trabalhou com agência? Como foi?
   -> Já teve agência? + Experiência com agência
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

**B — Sem Conversation AI (só nós) — guarda de janela fechada (G-06)**

Corrente de 8 blocos: `Send WhatsApp (pergunta)` → `Wait → Contact Replied,
tempo limite 24h` → `Update Contact Field` (com a resposta) → próxima
pergunta. Funciona sem Conversation AI contratado, mas não interpreta
resposta livre — você acaba tendo que ler as conversas na mão.

**No tempo limite (sem resposta), o bloco encerra o workflow — nunca "pula
para a pergunta seguinte".** Era essa a metade do G-06 que ficou pendente
na peça 1 (guarda 6.0 acima cobre só a entrada). O motivo é o mesmo em
cada uma das 8 perguntas, não só na primeira: a guarda 6.0 garante que a
**pergunta 1** parte de dentro da janela (direto, ou reaberta pela resposta
ao convite `QI-1`) — mas cada pergunta seguinte só herda essa garantia
porque a pergunta anterior **recebeu resposta**, e é a resposta do lead
(não o envio nosso) que reabre a janela de 24h. "Pular para a próxima
pergunta" sem resposta manda texto livre com a janela já fechada, exatamente
o defeito que a peça 1 corrigiu na entrada — só que oito vezes, uma por
pergunta, e sem Template equivalente para nenhuma delas (8 Templates novos
para um fluxo pensado como conversa foi avaliado e descartado desde a
primeira redação deste item). Terminar em silêncio, em vez de insistir sem
garantia de janela, é o mesmo "lado barato de errar" que a lição do R-18 já
registrou para outro portão do projeto — o lead segue coberto pela
Cadência 12x30 principal (ligação), que não passa por aqui.

| # | Ação | Configuração exata |
|---|---|---|
| B.1 | Send WhatsApp | texto livre, pergunta 1 (prompt da seção 6, item 1) |
| B.2 | Wait → Contact Replied | tempo limite 24h |
| B.2 (respondeu) | Update Contact Field | grava a resposta no campo da pergunta 1 → segue para B.3 (pergunta 2), dentro da janela que a própria resposta reabriu |
| B.2 (sem resposta) | Add Note | `IA de qualificação (Caminho B): sem resposta na pergunta 1 — encerra, segue só pela cadência de ligação` → fim do workflow |

Repita o par (`Send WhatsApp` → `Wait → Contact Replied` com o mesmo
desvio "respondeu segue / sem resposta encerra") para as 7 perguntas
restantes, cada uma citando seu próprio número na nota de saída.

### Saída
| # | Ação |
|---|---|
| 1 | Update `Qualificação` = `IA Whatsapp` (rótulo real — mesma nota do nó "Estrutura" acima) |
| 2 | Math: recalcula `Nota de qualificação` (seção 9.1) |
| 3 | If/Else: nota ≥ 45 → Add Contact Tag `fila-quente` + Update `Prioridade` = 5 + Internal Notification para o SDR: "lead qualificado pela IA, ligar hoje" |
| 4 | If/Else: nota < 25 **e** `Budget` = `Não tem` → Update Opportunity `status` = `abandoned` (etapa fica onde estava — tabela 1.0, `Nutrição` não é etapa própria) + tag `nutricao-90d` |

---

## 7. Calendário do closer + formulário de qualificação

### 7.1 Calendário `Reunião com closer`

Calendários → Novo → **Round Robin** (se houver mais de um closer) ou Simple.

| Configuração | Valor | Por que |
|---|---|---|
| Duração | 1 hora | Reunião de diagnóstico — sugerido 45 min, dono preferiu manter 1h ao vivo em chat, 18/09/2026: não é referenciado por nenhuma condição de workflow, então a mudança é livre |
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

**Campo `Empresa` (linha 4): use o personalizado, não o nativo.** O plano
original apontava para o campo nativo `Company Name`
(`{{contact.company_name}}`). Na tela, o construtor de formulário (aba
"Adição rápida" e aba "Adicionar campos de objeto", Contato) não lista
`Company Name` — nativo não aparece nesse seletor. Confirmado em
19/09/2026, ao vivo em chat. Caminho aceito: campo personalizado `Empresa`
(`contact.empresa`, criado em 18/09/2026), já usado na linha 4 abaixo e no
modelo de nota da seção 5.

| Ordem | Campo do formulário | Mapeado para | Obrigatório |
|---|---|---|---|
| 1 | Nome | `first_name` / `last_name` | Sim |
| 2 | Telefone | `phone` | Sim |
| 3 | E-mail | `email` | Sim |
| 4 | Empresa | `Empresa` (personalizado, `contact.empresa`) | Sim |
| 5 | Segmento | `Segmento` | Sim |
| 6 | Site | `Site` | Não |
| 7 | Instagram | `Instagram` | Não |
| 8 | Clientes novos por mês | `Clientes novos por mês` | Sim |
| 9 | Investe em anúncios | `Investe em anúncios` | Sim |
| 10 | Investimento mensal | `Investimento mensal em anúncios` | Não |
| 11 | Plataformas | `Plataformas de anúncio` | Não |
| 12 | Já teve agência? | `Já teve agência?` | Sim |
| 13 | Experiência com agência | `Experiência com agência` | Não |
| 14 | Tem time comercial | `Tem time comercial` | Sim |
| 15 | Quem atende os leads | `Quem atende os leads` | Sim |
| 16 | Usa CRM | `Usa CRM` | Não |
| 17 | Canal principal de venda | `Canal principal de venda` | Não |
| 18 | Budget | `Budget` | Sim |
| 19 | Decisor | `Decisor` | Sim |
| 20 | Dor principal | `Dor principal` | Sim |
| 21 | Prazo | `Prazo` | Sim |
| 22 | Qualificação | `Qualificação` (renomeado de "Qualificação preenchida por"; opção `Automático` virou `Vendedor`) | Sim, valor padrão `SDR` |
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

**A coluna `Empresa` destas listas é o campo personalizado**
(`contact.empresa`), não a coluna padrão de empresa do GHL. O seletor de
colunas mostra as duas com nome parecido, e a padrão vai ficar vazia: desde
19/09/2026 o formulário grava no personalizado, porque o construtor de
formulário não oferece o nativo (seção 7.2). Escolher a errada faz o SDR abrir
a fila e ver empresa em branco em todas as listas de uma vez.

### 8.1 `Fila Quente` — migrado para as 5 etapas reais em 18/09/2026
| Item | Configuração |
|---|---|
| Filtros | tag `fila-quente` presente **E** tag `nao-perturbe` ausente **E** etapa da oportunidade em (`CONECTAR`, `AGENDAR`) — `Retorno agendado` some da lista de etapas porque não é mais etapa própria (tabela 1.0): quem pediu retorno já está em `CONECTAR`, coberto |
| Colunas | Nome · `Empresa` · Telefone · `Prioridade` · `Tentativa nº` · `Resultado da tentativa` · `Nota de qualificação` · Última atividade |
| Ordenação | `Prioridade` desc, depois `Tentativa nº` asc |

### 8.2 `Fila Telefone Hoje` — migrado para as 5 etapas reais em 18/09/2026
| Item | Configuração |
|---|---|
| Filtros | tag `fila-tel` presente **E** `nao-perturbe` ausente **E** `telefone-invalido` ausente **E** `conectado-hoje` ausente **E** etapa = `CONECTAR` |
| Colunas | Nome · `Empresa` · Telefone · `Tentativa nº` · `Prioridade` · `Resultado da tentativa` · Tarefas abertas |
| Ordenação | `Prioridade` desc, depois `Tentativa nº` asc |

Ordenar por tentativa crescente é de propósito: lead na T1 tem muito mais
chance de atender do que o da T11. A fila devolve primeiro o que converte.

### 8.3 `Fila WhatsApp Hoje` — migrado para as 5 etapas reais em 18/09/2026
| Item | Configuração |
|---|---|
| Filtros | tag `fila-wa` presente **E** `nao-perturbe` ausente **E** `conectado-hoje` ausente **E** `Permissão WhatsApp` = `Sim` **E** etapa = `CONECTAR` |
| Colunas | Nome · `Empresa` · Telefone · `Tentativa nº` · `WA não atendidas seguidas` · `Prioridade` |
| Ordenação | `Prioridade` desc, depois `WA não atendidas seguidas` asc |

### 8.4 `Retornos` — migrado para as 5 etapas reais em 18/09/2026, ordenação fechada em 22/09/2026
| Item | Configuração |
|---|---|
| Filtros | `Resultado da tentativa` = `Pediu retorno` **E** `nao-perturbe` ausente |
| Colunas | Nome · `Empresa` · Telefone · `Data de retorno` · `Hora do retorno` · `Prioridade` · `Nota de qualificação` · Tarefas abertas |
| Ordenação | `Data de retorno` asc, depois `Hora do retorno` asc (mesmo padrão de dois níveis de 8.1/8.2/8.3) |

Os dois campos de S-01 (`Data de retorno`, `Hora do retorno`) existem na tela
desde 21/09/2026 23:18 — a versão anterior desta seção ainda descrevia o
estado de antes deles existirem ("sem o campo S-01: Última atividade asc —
pior, mas funciona"), contradizendo a nota do ramo `Pediu retorno` (acima,
nó 4/4b) que já dava a lista como atualizada. Fechado agora: quem venceu há
mais tempo aparece primeiro, e dentro do mesmo dia o SDR vê o horário
combinado pela coluna.

#### ⚠️ Duas ressalvas sobre esta ordenação, levantadas em 22/09/2026 — e a primeira vale para **sete** listas, não para esta

**1. "Mesmo padrão de 8.1/8.2/8.3" não é verificação, é repetição.** A
justificativa da ordenação de dois níveis aqui foi que as outras listas já
fazem assim. Mas nenhuma delas foi testada na tela: `grep "^| Ordenação | .*,
depois "` acha **sete** listas com dois níveis (8.1, 8.2, 8.3, 8.4, 8.16,
8.18, 8.19). Se a Smart List do GHL **não** aceitar ordenação secundária, o
desenho está errado em sete lugares de uma vez — e a consistência entre eles
esconde isso, em vez de denunciar. Pesquisa desta rodada: a documentação
descreve ordenação e gestão de colunas como recursos da Smart List, mas **não
achei confirmação de ordenação por mais de uma coluna** (e há pedido aberto de
usuários sobre limitação de ordenação em lista de contato). **Não afirmo que
não existe** — afirmo que ninguém verificou, e que a justificativa usada não
verifica nada.

**Regra:** "já fazemos assim em outros N lugares" é consistência, não
evidência. Quando a capacidade da plataforma nunca foi testada, repetir o
padrão multiplica o risco em vez de reduzi-lo — e o número de lugares afetados
é exatamente o que o `grep` devolve.

**Plano B, se a tela só aceitar uma coluna** (uma linha por lista, sem
redesenho):

| Lista | Ordenar por | O que o segundo nível vira |
|---|---|---|
| 8.4 `Retornos` | `Data de retorno` asc | `Hora do retorno` já é **coluna** — o SDR lê o horário sem ordenar por ele |
| 8.1 / 8.2 / 8.3 / 8.16 | `Prioridade` desc | o desempate (`Tentativa nº` / `WA não atendidas seguidas`) vira coluna visível |
| 8.18 | `Nº de no-shows` desc | idem |
| 8.19 | `Segmento` asc | idem |

Em todas, o primeiro nível é o que importa para a decisão; o segundo é
refinamento que a coluna entrega de graça.

**2. `Hora do retorno` é `TEXT`, e `TEXT` ordena por letra, não por hora.** Com
`HH:MM` zero-padded (`09:30`, `14:00`) a ordem alfabética coincide com a
cronológica — é por isso que o placeholder do campo é `HH:MM` e não `H:MM`.
Mas nada impede o SDR de digitar `9:30`, e aí a linha vai parar **depois** de
`14:00` na lista, porque `'9'` > `'1'`. Não é defeito de desenho, é
característica do tipo: a única defesa é o placeholder (que já está certo na
tela, conferido por API) e o SDR saber disso. Vale uma linha no
`script-de-ligacao.md`, seção 2 — quem anota o horário é quem digita.

### 8.5 Sugerida por mim: `Sem resultado ontem`
| Item | Configuração |
|---|---|
| Filtros | tag `limpar-tarefas` presente **E** tag `fila-tel`/`fila-wa` ausentes |
| Para quê | É o buraco de gestão: tentativas que venceram sem o SDR classificar. Se esta lista cresce, a operação está mentindo nos números |

### 8.6 `Conexão por Tentativa` — R-01, coluna de qualidade acrescentada pelo F-06 (peça 2, 22/09/2026)
| Item | Configuração |
|---|---|
| Filtros | `Total de conexões` ≥ 1 |
| Colunas | Nome · `Tentativa nº` · `Total de ligações` · `Total de conexões` · `Tentativas telefone` · `Conexões telefone` · `Tentativas WhatsApp` · `Conexões WhatsApp` · `Conexão real` (nova) |
| Ordenação | `Tentativa nº` asc |

Funciona sem um campo extra de "tentativa em que conectou": ao registrar
`Atendeu`, o nó 10 da cadência (seção 2.4) remove o contato do workflow —
`Tentativa nº` para de mudar exatamente no valor em que ele conectou. Filtrar
por quem já conectou e ordenar por essa tentativa responde "qual tentativa
conecta mais" olhando a lista ordenada, sem planilha — é o "Pronto quando" do
R-01 do roadmap.

**Coluna `Conexão real` (F-06):** não troca o filtro — continua mostrando
todo `Atendeu`, de propósito, porque é a lista que compara os dois números,
não a que escolhe um. Olhando a coluna nova ao lado de `Conexões telefone`,
o gestor vê direto quais dessas conexões marcadas pelo SDR duraram menos de
60s (`Conexão real = Não` ou vazio — sem gravação habilitada, ou chamada
ainda sem transcrição) — a mesma pergunta do "Pronto quando" do F-06 ("o SDR
não consegue inflar o número desligando rápido"), respondida linha a linha
em vez de por uma taxa só. Filtro extra opcional para quem quiser isolar só
as reais: `Conexão real = Sim` — funciona aqui porque é leitura pontual por
contato, sem somar nada (diferente do widget de dashboard, seção 2.17, que
precisa de campo cumulativo — ver C-31 em `campos-e-tags.md`).

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
| Colunas | Nome · `Empresa` · Telefone · `Entrada em` · `1ª tentativa em` (sempre vazio nesta lista) · Tarefas abertas |
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
| Colunas | Nome · `Empresa` · Etapa atual · `Data de criação` |
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
| Colunas | Nome · `Empresa` · `Data conectado` · `Tentativa nº` |
| Ordenação | `Data conectado` desc |

### 8.11 `Funil — Agendaram no Mês` — R-03
| Item | Configuração |
|---|---|
| Filtros | `Data agendado` dentro do mês atual |
| Colunas | Nome · `Empresa` · `Data agendado` · `Nota de qualificação` |
| Ordenação | `Data agendado` desc |

### 8.12 `Funil — Compareceram no Mês` — R-03
| Item | Configuração |
|---|---|
| Filtros | `Data compareceu` dentro do mês atual |
| Colunas | Nome · `Empresa` · `Data compareceu` · `Reunião foi qualificada` |
| Ordenação | `Data compareceu` desc |

As quatro listas (8.9 a 8.12) respondem "a taxa de conexão do mês" sem
contar na mão: cada uma mostra, no topo, o total de contatos que bateram
naquele filtro — dividir o total de 8.10 pelo de 8.9 é a taxa de conexão do
mês, sem abrir planilha nem somar linha por linha. É o "Pronto quando" do
R-03. Cada campo `DATE` novo (C-20 a C-22) grava o marco na hora em que ele
acontece pela primeira vez e não muda depois, então a oportunidade continua
contando no mês em que **cruzou** aquele marco mesmo depois de avançar para
a etapa seguinte — diferente de filtrar pela etapa atual, que subcontaria
quem já foi para `NEGOCIAR` ou saiu do pipeline (`status` ≠ `open`).

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
| Colunas | Nome · `Empresa` · Telefone · `Tentativa nº` · `Prioridade` · `Template usado` · Tarefas abertas |
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
| Colunas | Nome · `Empresa` · Telefone · `Tentativa nº` · Etapa atual · Última atividade |
| Ordenação | Última atividade asc (quem está pausado há mais tempo aparece primeiro) |

O laço da seção 2.13 (nó 2.5/1.5) represa a tentativa sozinho, sem tarefa
nem tag de fila — sem esta lista, um lead pausado literalmente some da
visão do gestor até o SDR lembrar de tirar a tag. Ordenar por quem está
parado há mais tempo é o mesmo raciocínio da 8.8: quem está represado há
mais tempo é quem mais precisa de alguém decidir "tira a pausa" ou "descarta
de vez".

### 8.16 `Fila do Dia — Total` — R-11
| Item | Configuração |
|---|---|
| Filtros | tag `fila-tel` presente **OU** tag `fila-wa` presente **E** `nao-perturbe` ausente |
| Colunas | Nome · `Empresa` · Telefone · `Tentativa nº` · canal (`fila-tel` ou `fila-wa`) · `Prioridade` |
| Ordenação | `Prioridade` desc, depois `Tentativa nº` asc |

O total desta lista **é** o total de tarefas `[CADENCIA]` abertas hoje —
não soma 8.2 com 8.3 na mão porque um contato nunca carrega as duas tags ao
mesmo tempo (nó 6 do bloco padrão, seção 2.4, aplica uma por vez, e vale
para todo bloco que o espelha: 2.10, 2.12). Alimenta a métrica `Estouro da
Fila` e o aviso do Monitor de Capacidade (seção 2.15, R-11).

Este total agora também inclui as tarefas `NS1`/`NS2`/`NS3` da Recuperação de
No-show (seção 5.3, R-12) de graça: o filtro é só por tag, sem etapa — a
tag `fila-tel` aplicada pela seção 5.3 conta aqui mesmo com a oportunidade
em `NEGOCIAR`, não em `CONECTAR`.

### 8.17 `Recuperação de No-show` — R-12 — migrado para as 5 etapas reais em 21/09/2026
| Item | Configuração |
|---|---|
| Filtros | `Nº de no-shows` ≥ 1 **E** etapa da oportunidade = `NEGOCIAR` **E** `nao-perturbe` ausente |
| Colunas | Nome · `Empresa` · Telefone · `Nº de no-shows` · `Template usado` · Última atividade · Tarefas abertas |
| Ordenação | `Nº de no-shows` desc, depois Última atividade asc |

Filtra por campo numérico direto, sem tag nova — mesmo raciocínio já usado
na 8.6 (`Total de conexões` ≥ 1). Não aparece em 8.2/8.3 porque a etapa
continua `NEGOCIAR`, de propósito (seção 5.3, "Por que fica em `NEGOCIAR`,
não volta para `CONECTAR`"): esta lista é a única visão de quem está na
régua NS1-NS3, igual a 8.14 já ser a única visão de quem está na régua
TR1-TR4.

### 8.18 `Higiene — Sem Telefone Válido` — R-13
| Item | Configuração |
|---|---|
| Filtros | Campo nativo `Phone` **vazio** **OU** tag `telefone-invalido` presente |
| Colunas | Nome · `Empresa` · E-mail · `Site` · `Instagram` · Etapa da oportunidade · Data de criação |
| Ordenação | Data de criação asc (quem está parado há mais tempo aparece primeiro) |

A visão que fecha o "Como" do roadmap ("lista inteligente de contatos sem
telefone válido"): junta os dois jeitos de um contato virar "impossível de
ligar" neste projeto — nasceu sem telefone (portão 0.0/0.0b, seções 2.3 e
2.10) ou teve o número invalidado durante uma ligação de verdade (ramo
`Número errado`, seção 4) ou por validação automática (seção 2.16, se
ativada). É rotina de **marcação**, não de exclusão — a regra 1 do projeto
não muda: ninguém aqui é apagado, só sinalizado para alguém corrigir a
fonte da lista ou completar o cadastro manualmente. Ordenar pelo mais
antigo é o mesmo raciocínio já usado em 8.8 e 8.15: quem está represado há
mais tempo é quem mais precisa de alguém decidir.

### 8.19 `Conexão por Segmento e Horário` — F-02
| Item | Configuração |
|---|---|
| Filtros | `Hora da conexão` não vazio |
| Colunas | Nome · `Segmento` · `Hora da conexão` · `Data conectado` · `Tentativa nº` |
| Ordenação | `Segmento` asc, depois `Hora da conexão` asc |

Não faz conta nenhuma — GHL não agrupa nem tira média dentro de uma Smart
List (mesmo achado do R-11 sobre Custom Metrics). Ordenar por `Segmento` e
depois por `Hora da conexão` deixa as conexões do mesmo segmento juntas e
crescentes por hora, para o gestor ver o agrupamento visualmente sem
planilha — o que a lista pode fazer sozinha, do "Pronto quando" do F-02
(seção 2.18). A decisão de ajustar a régua por segmento, quando o padrão
aparecer, é manual: mecanismo completo em 2.18.

### 8.20 `Saúde — NOVO LEAD Estagnado` — F-05
| Item | Configuração |
|---|---|
| Filtros | tag `novo-lead-estagnado` presente |
| Colunas | Nome · `Empresa` · Telefone · Origem (`source`) · Data de criação da oportunidade · Etapa atual |
| Ordenação | Data de criação asc (quem está parado há mais tempo aparece primeiro) |

Mesmo raciocínio de ordenação já usado em 8.8/8.15/8.18: quem está
estagnado há mais tempo é quem mais precisa de alguém decidir promover ou
descartar. A tag só existe porque o workflow da seção 2.20 (F-05) já
esperou 24h e conferiu de novo antes de aplicá-la — a lista não faz
conta nenhuma, só lê a marca.

### 8.21 `Saúde — Fila Travada` — F-05
| Item | Configuração |
|---|---|
| Filtros | tag `fila-travada` presente |
| Colunas | Nome · Telefone · Etapa atual · `Tentativa nº` · `Resultado da tentativa` |
| Ordenação | Nenhuma especial — a lista deve ficar vazia na maior parte do tempo; quando tiver linha, é para o gestor abrir agora, não para priorizar entre várias |

A tag só existe porque o workflow da seção 2.21 (F-05, peça 2) já esperou
até o fim do dia da tentativa e conferiu de novo antes de aplicá-la — a
lista, como a 8.20, não faz conta nenhuma, só lê a marca. Diferente de
8.1-8.3 (filas normais, esperadas ter contato todo dia), esta lista é um
sensor de defeito: qualquer linha aqui é uma tentativa cujo nó 9 (seção
2.4) não rodou.

### 8.22 `Saúde — CONECTAR Estagnado` — F-05
| Item | Configuração |
|---|---|
| Filtros | tag `conectar-estagnado` presente |
| Colunas | Nome · Telefone · Etapa atual · `Tentativa nº` · `Entrada em` · Origem (`cad-inbound`/`cad-outbound`) |
| Ordenação | Nenhuma especial — mesma lógica da 8.21: a lista deve ficar vazia na maior parte do tempo, e qualquer linha é para o gestor abrir agora |

A tag só existe porque o workflow da seção 2.22 (F-05, peça 3) já esperou
14 dias corridos desde a última tentativa e conferiu de novo antes de
aplicá-la. Diferente da 8.21 (uma tentativa travada dentro do próprio dia),
esta lista é o sensor da cadência **parada de vez** — o cenário-limite que
a peça 2 já citava como fora do seu próprio alcance.

### 8.23 `Saúde — AGENDAR Estagnado` — F-05
| Item | Configuração |
|---|---|
| Filtros | tag `agendar-estagnado` presente |
| Colunas | Nome · Telefone · `Data conectado` · Tarefas abertas |
| Ordenação | `Data conectado` asc (quem atendeu há mais tempo sem fechar o loop aparece primeiro) |

A tag só existe porque o workflow da seção 2.23 (F-05, peça 5) já esperou
24h desde a conexão e conferiu de novo antes de aplicá-la — mesmo
raciocínio de ordenação da 8.20 (quem espera há mais tempo precisa de
decisão primeiro).

### 8.24 `Saúde — Retorno Vencido` — F-05
| Item | Configuração |
|---|---|
| Filtros | tag `retorno-vencido` presente |
| Colunas | Nome · Telefone · `Data de retorno` · `Prioridade` · Tarefas abertas |
| Ordenação | `Data de retorno` asc (quem venceu há mais tempo aparece primeiro) |

A tag só existe porque o workflow da seção 2.24 (F-05, peça 6) já esperou
até depois do horário combinado e conferiu de novo, comparando contra o
`Checkpoint — Data de retorno` congelado no instante do gatilho, antes de
aplicá-la — mesma garantia de "não é palpite" que as outras quatro listas de
saúde (8.20-8.23) já seguem.

### 8.28 `Saúde — Negociação Estagnada` — F-13
| Item | Configuração |
|---|---|
| Filtros | tag `negociacao-estagnada` presente |
| Colunas | Nome · `Empresa` · `Nota de qualificação` · `Data do veredito do closer` |
| Ordenação | `Data do veredito do closer` asc (quem foi qualificado há mais tempo sem decisão aparece primeiro) |

A tag só existe porque o workflow da seção 2.28 (F-13) já esperou 3 dias
corridos desde o veredito `Sim` e conferiu de novo (etapa, `status` e o
próprio veredito) antes de aplicá-la — mesma garantia de "não é palpite" que
as listas de saúde 8.20-8.24 já seguem.

### 8.25 `Entrada do Dia` — F-10

**Conferido na tela conceitual em 22/09/2026 (pesquisa, `help.gohighlevel.com`
bloqueado pelo proxy — lido por citação):** Smart List do GHL **tem** filtro de
data **relativa** (`Is` → `In the Last`, com janela em dias) e a lista é
dinâmica de verdade — reavalia em tempo real e o contato entra e sai sozinho.
Então esta lista funciona. Mas o filtro precisa ser escrito como **relativo**,
e não como igualdade contra uma data: se quem monta escolher `Data de criação`
`is` e então **picar um dia no calendário**, a lista congela naquela data e
para de atualizar amanhã, em silêncio — o mesmo tipo de armadilha do rótulo de
etapa que nunca casa. **É o detalhe que faz a lista servir ou não servir.**

**São duas listas salvas, não uma com o filtro trocado.** Smart List é uma
view salva; alternar o filtro de 1 para 7 dias e de volta muda a view **para
todo mundo** que a usa, e é o tipo de edição que alguém esquece desfeita.
Duas listas custam o mesmo e não disputam:

| Lista | Filtro | Colunas | Ordenação |
|---|---|---|---|
| **`Entrada — últimas 24h`** | `Data de criação` **`In the Last`** `1 dia` (relativo, **não** igualdade a uma data) | Nome · Telefone · Origem (`source`) · Data de criação | Data de criação desc |
| **`Entrada — últimos 7 dias`** | `Data de criação` **`In the Last`** `7 dias` | idem | idem |

**Estas duas são as únicas listas do documento que dá para montar hoje, sem
esperar decisão nenhuma — e são a mais urgente da casa.** Acrescentado em
22/09/2026, por dois motivos que se somam:

1. **Não dependem da Tabela J.** A coluna `Empresa` saiu da definição acima (a
   versão anterior a trazia por hábito): ela está vazia para 100% da base e o
   trabalho destas listas é **contar chegada**, não qualificar lead. Sem
   `Empresa`, não há o que decidir — as outras sete listas esperam a Tabela J
   porque nelas a coluna morta atrapalha a leitura do SDR; aqui não existe.
2. **Respondem, de graça, a pergunta de ordenação que trava as outras sete.**
   A ordenação destas duas é de **um nível só** (`Data de criação` desc), então
   elas se montam inteiras de qualquer jeito — mas quem as montar está com a
   tela de Smart List aberta e pode olhar, em dez segundos, se o construtor
   oferece um segundo critério (`, depois`). **É a primeira oportunidade real
   de responder aquilo**, e ela chega antes da Fase 6.

**Ordem sugerida, portanto:** monte a `Entrada — últimas 24h` primeiro, de
todas as listas do projeto. Ela é o único monitor de entrada que existe
(F-10 — e a entrada está parada há mais de 1,9× o maior intervalo já
observado), não espera ninguém, e responde de lambuja a dúvida que decide o
desenho das outras sete. Anote o resultado da ordenação em
`APRENDIZADOS-CRM.md` — é a verificação que nenhuma pesquisa deste projeto
conseguiu fazer.

**"Últimas 24h" não é "hoje", e a diferença importa na leitura:** `In the
Last 1 dia` é janela **rolante** (conta para trás a partir de agora); "hoje" é
desde a meia-noite. Para o F-10 a rolante é a **melhor** das duas — é
literalmente a mesma grandeza do gap que mede a anormalidade (o maior
intervalo já observado nesta base é 15h06, `ROADMAP-SALES-ENGAGEMENT.md`,
F-10), então "zero linha nas últimas 24h" já significa "passamos do pior caso
histórico". Mas não chame de "hoje" no nome nem na conversa: às 09h da manhã a
lista mostra o que entrou desde as 09h de ontem, e quem ler "hoje" vai
interpretar errado.

**Nome exato do campo: confirmar na tela.** A documentação usa `Created On` /
`Date Added` em inglês; a tela em português desta subconta pode trazer `Data de
criação` ou `Data de adição`. Este projeto já perdeu tempo com `Data de
retorno` vs `Data do retorno` — escolha pelo seletor, não pelo que está escrito
aqui.

Equivalente, para quem não tem Custom Metrics no plano, dos dois widgets
`Leads novos hoje`/`Leads novos — 7 dias` da seção 2.17 (ROADMAP-SALES-
ENGAGEMENT.md, F-10) — mesmo padrão de fallback que 8.6/8.8/8.16 já cobrem
para as outras métricas do dashboard: o gestor perde a tela única, não
perde o dado. Diferente das outras listas de saúde (8.20-8.24), que
esperam alguém estar parado, esta é a única que vigia o lado oposto —
**nenhuma linha nova entrando**: as seis peças do Monitor de Saúde (F-05)
ficam todas verdes justamente quando a entrada para (achado que abriu o
F-10, `APRENDIZADOS-CRM.md`), então zero linha com `Data de criação = hoje`
antes do meio-dia já é sinal de olhar, mesmo com a lista vazia — o oposto
de toda outra lista deste documento, onde vazia é o estado bom. Para o
número de 7 dias (tendência), a mesma lista trocando o filtro para
"últimos 7 dias" e contando as linhas na tela é o substituto manual do
segundo widget — sem Custom Metrics não há cálculo automático de
tendência, e essa é a mesma limitação já registrada no "Limite conhecido"
da seção 2.17.

Esta é a peça que faltava para o F-10 fechar a especificação por inteiro:
a seção 2.17 já tinha os dois widgets (`Leads novos hoje`/`Leads novos — 7
dias`), mas a Smart List equivalente, citada só em prosa no roadmap
("Smart List `Entrada do dia`, filtro `Date Created` = hoje, ordenada por
criação"), nunca tinha ganhado uma entrada própria aqui — a fonte que a
Fase 6 do `GUIA-MONTAGEM.md` realmente consulta. Fechado nesta rodada
(22/09/2026), documentação pura, zero campo e zero tag novos.

### 8.26 `Auditoria — tag sem DND nativo` — R-14

| Item | Configuração |
|---|---|
| Filtros | tag `nao-perturbe` presente **E** (`Calls & Voicemails DND` = Disabled **OU** `WhatsApp DND` = Disabled) |
| Colunas | Nome · Telefone · Tags · `Resultado da tentativa` · Etapa/status da oportunidade |
| Ordenação | Data de criação do contato, desc (o mais recente primeiro — é o mais provável de ainda estar "quente" numa régua) |

Lista de exceção, não de volume: o alvo é sempre zero linha. Existe porque
`Set Contact DND` e `Add Contact Tag: nao-perturbe` nascem no mesmo nó em
quatro lugares diferentes do documento (2.9.5, seção 4 ramo `Não ligar`,
seção 6 nó 3, opt-out por palavra-chave do R-17) — um deles aplicando só a
tag sem o DND nativo é o caso que realmente arrisca reincomodar o lead,
porque a tag sozinha não bloqueia nada na plataforma; é convenção interna
lida por filtro de lista, o DND é quem impede o próximo envio de sair.
Uma linha aqui é bug a corrigir na hora (falta de `Set Contact DND` num nó
que já tem a tag), não estatística a acompanhar.

**Correção de lógica, 22/09/2026 — o filtro nasceu com `E` onde precisa de
`OU`.** Estava escrito `tag presente E Calls DND = Disabled E WhatsApp DND =
Disabled`, que só pega quem está desprotegido **nos dois** canais. Um contato
com a tag, `Calls DND` ligado e `WhatsApp DND` **desligado** escapava da
lista — e é exatamente um lead que pediu para não ser procurado e ainda pode
receber WhatsApp. Pior: **proteção parcial é o defeito mais provável** dos
dois, porque basta um nó chamar `Set Contact DND` num canal só. Com `E`, "zero
linha" não provava o que o R-14 diz provar. Note que a 8.27 já usava `OU`
corretamente — as duas são espelhos, e espelho de "algum canal ligado" é
"algum canal desligado", não "todos desligados".

#### ⚠️ O filtro `WhatsApp DND` pode não existir nesta subconta hoje — e isso é mais que um detalhe de montagem

Pesquisa desta rodada, na mesma fonte que confirmou os nomes dos filtros: as
preferências de DND de **WhatsApp, Facebook Messenger e GMB só aparecem depois
que o app correspondente está integrado à subconta.** Esta subconta **não tem
WhatsApp integrado** (é a razão pela qual o R-14 esperava "volume real de
mensagem" e pela qual não existe uma única mensagem de WhatsApp aqui). Duas
consequências, e a segunda é de compliance, não de montagem:

1. **Hoje as duas listas se montam só pela metade** — com `Calls & Voicemails
   DND`. A cláusula de WhatsApp entra quando o canal for integrado. Monte
   assim mesmo: meia auditoria já pega o caso de tag sem nenhum bloqueio.
2. ~~O `Set Contact DND` "todos os canais" não pode estar ligando DND de um
   canal que não existe na subconta.~~ **MEDIDO E REFUTADO no mesmo dia, ~1h
   depois — a suposição era minha e estava errada.** Leitura de
   `contacts_get-contact` em `Teste Atendeu` (`Lj96CIFYaGKPiC0opzbc`):

   ```
   dndSettings: {
     Call:     { status: "active", message: "Updated from workflow_cf6fa19d-…" }
     Email:    { status: "active", … }   SMS: { status: "active", … }
     FB:       { status: "active", … }   GMB: { status: "active", … }
     WhatsApp: { status: "active", message: "Updated from workflow_cf6fa19d-…" }
   }
   ```

   **`WhatsApp` está lá, `active`, escrito por um workflow**, numa subconta que
   não tem WhatsApp integrado. Então o `Set Contact DND` grava a flag dos seis
   canais independentemente de integração, quem pede silêncio **fica** protegido
   em WhatsApp, e não existe problema de retroatividade nenhum.

   **Onde eu errei, e é uma distinção que vale guardar:** a fonte diz que as
   *preferências* de DND de WhatsApp/Messenger/GMB "só aparecem depois que o app
   está integrado". Isso é sobre **o que a tela mostra e o que o filtro
   oferece** — ou seja, sobre **ler**. Eu li como se fosse sobre **escrever**, e
   concluí que a proteção não era aplicada. São coisas diferentes: a flag é
   gravável por workflow mesmo quando a interface não a expõe.

**O que sobra da ressalva, agora no tamanho certo:** só a metade de
*auditabilidade*. Se o filtro `WhatsApp DND` não aparecer na Smart List desta
subconta enquanto o canal não estiver integrado, as listas 8.26/8.27 se montam
apenas com a cláusula de ligação — a **proteção** está inteira, a **conferência
dela** é que fica parcial. Uma conferência, não duas, e sem prazo de véspera:

| Conferir | Por quê |
|---|---|
| O filtro `WhatsApp DND` aparece na Smart List hoje? | Se sim, montar as duas listas completas já. Se não, montar só com `Calls & Voicemails DND` e completar no dia da integração |

**Brinde da mesma leitura, e é uma ferramenta nova de diagnóstico:**
`dndSettings[canal].message` carrega **o id do workflow que ligou aquele DND**
(`Updated from workflow_cf6fa19d-6af8-4fcb-b0dd-6fcfcefde0cc`). Dá para
descobrir *quem* silenciou um contato sem abrir a tela — útil exatamente para a
8.27 (`DND sem tag`), cujo propósito é achar o caminho não documentado que
ligou DND. Se o `message` disser `workflow_…`, foi régua; se disser outra
coisa, foi clique ou API.

### 8.27 `Auditoria — DND sem tag` — R-14

| Item | Configuração |
|---|---|
| Filtros | (`Calls & Voicemails DND` = Enabled **OU** `WhatsApp DND` = Enabled) **E** tag `nao-perturbe` ausente |
| Colunas | Nome · Telefone · Tags · Etapa/status da oportunidade |
| Ordenação | Data de criação do contato, desc |

Espelho da 8.26, risco menor: o DND nativo já bloqueia o canal, então o
lead está protegido — mas a divergência ainda importa, porque aponta um
caminho que ligou DND sem passar pelo registro do projeto (ação manual na
tela, ou um nó de opt-out que este documento ainda não cobre). Uma linha
aqui não é emergência como na 8.26, é pista para achar o nó ou o clique
que a especificação atual não previu.

**As duas juntas são o "relatório que prova que ninguém foi incomodado
indevidamente" do R-14** (`ROADMAP-SALES-ENGAGEMENT.md`): zero linha na
8.26 é a prova em si, a 8.27 é a rede de segurança que pega o que a 8.26
sozinha não veria. Nomes exatos dos dois filtros de DND a confirmar na
tela — a documentação consultada (`WebSearch`, `help.gohighlevel.com`/
`consultevo.com`/`growthable.io`) está em inglês, a tela desta subconta é
em português; mesma ressalva já registrada para outros filtros nativos do
projeto (F-10, seção 8.25). Zero campo e zero tag novos: reaproveita
`nao-perturbe` (T-06) e os filtros de DND nativos do contato — não depende
de `APROVADO.md`. Referenciadas na seção 2.17 (Painel do Gestor), seção
"Compliance".

---

## 9. Nota de qualificação e Prioridade

### 9.1 `Nota de qualificação` (0 a 100)

Montada com nós **Math Operation** em série no Pós-agendamento (seção 5, nó 4)
e na saída da IA (seção 6). Comece zerando o campo e some bloco a bloco.

**Rótulos de opção — corrigidos em 19/09/2026.** As tabelas abaixo usavam os
rótulos *sugeridos* na primeira rodada, não os que ficaram na tela quando
alguém montou os campos na Fase 2 do `GUIA-MONTAGEM.md` (18/09/2026). Um
`If/Else` que compara texto contra um rótulo que não existe mais nunca casa —
a régua inteira ficaria pontuando errado sem nenhum erro visível, o mesmo
risco de merge field órfão já registrado em `APRENDIZADOS-CRM.md` para
`fieldKey`. Achado e catalogado em `CONFERENCIA-CAMPOS.md` (Tabela C), que
também sinalizava a correção como pendente — aplicada agora. Regra daqui pra
frente: rótulo de opção citado neste documento é sempre o que
`locations_get-custom-fields` devolve, nunca o que pareceu razoável sugerir.

**Bloco A — Fit (30 pontos)**
| Campo | Valor | Pontos |
|---|---|---|
| Clientes novos por mês | 10 / 11-30 / 31-100 / +101 | 3 / 6 / 8 / 10 |
| Tem time comercial | Só dono / 1-5 / 6-10 / +10 | 3 / 7 / 9 / 10 |
| Quem atende os leads | Ninguém fixo / Dono / Vendedor / SDR | 10 / 7 / 5 / 3 |

"Ninguém fixo" vale mais que "SDR" de propósito: é a dor mais fácil de
resolver e a que mais precisa de nós.

**`Tem time comercial` é o único remapeamento de verdade, não só relabel:**
a tela juntou os dois degraus baixos do plano original (`1-2 pessoas`=6 e
`3-5`=8) num só, `1-5`. Fica com 7 — a média dos dois, arredondada para cima
porque "1-5" inclui o caso de 5 pessoas, mais perto do antigo degrau de 8 que
do de 6. As outras três linhas de opção deste documento (`Clientes novos por
mês`, `Investimento mensal`, `Prazo`) só trocaram o texto do rótulo: a
ordem e a quantidade de degraus na tela bateram exatamente com o plano
original, então a pontuação de cada degrau **não mudou**, só o texto que o
`If/Else` compara.

**Bloco B — Maturidade de mídia (25 pontos)**
| Campo | Valor | Pontos |
|---|---|---|
| Investe em anúncios | Sim / Já investiu e parou / Nunca | 13 / 9 / 4 |
| Investimento mensal | Acima de 10k / 5k a 10k / 1k a 5k / Até 1k | 12 / 10 / 6 / 2 |
| ⚠ *(21/09/2026)* | *Os valores que o Meta Lead Ads **grava** neste campo são `Acima de 10k` / `Abaixo de 5k` / `Até R$ 1.000` / `Não invisto nada ainda` — só o primeiro é opção da tela; os outros três nunca casam num `If/Else`. E `Prazo` chega vazio do Meta: a resposta cai em `Urgência`. Não monte o nó 4 do Pós-agendamento contra esta tabela antes de o dono decidir o G-04 (`ROADMAP-SALES-ENGAGEMENT.md`; opções em `CONFERENCIA-CAMPOS.md`, Tabela H)* | — |

**Bloco C — BANT (45 pontos)**
| Campo | Valor | Pontos |
|---|---|---|
| Budget | Tem / Precisa aprovar / Não tem | 15 / 9 / 0 |
| Decisor | Sim / Influencia / Não decide | 15 / 8 / 2 |
| Prazo | Pra ontem / Espera 30 dias / Este ano / Sem prazo | 15 / 11 / 6 / 2 |

`Prazo` parece o mais arriscado dos três — "Este ano" soa bem mais largo que
o antigo "1-3 meses" — mas a ordem de urgência não inverteu: `Pra ontem` é
mais urgente que `Espera 30 dias`, que é mais urgente que `Este ano`, que é
mais urgente que `Sem prazo`. Mesma ordem, mesmos 4 degraus, pontuação
herdada sem mudança.

Máximo: 30 + 25 + 45 = **100**.

**Faixas**
| Nota | Leitura | Consequência automática |
|---|---|---|
| 70–100 | A — agenda e avisa o closer sênior | `Prioridade` = 5, tag `fila-quente` |
| 45–69 | B — agenda normal | `Prioridade` = 4 |
| 25–44 | C — nutrição | `Prioridade` = 2, tag `nutricao-90d`, `status` = `abandoned` (etapa fica onde estava — tabela 1.0, `Nutrição` não é etapa própria) |
| 0–24 | D — descarta | `Prioridade` = 1, `status` = `lost` (etapa fica onde estava — tabela 1.0, `Descartado` não é etapa própria) |

**Corte independente da nota:** `Budget` = `Não tem` **e** `Prazo` = `Sem
prazo` → nutrição, qualquer que seja a nota. Empresa grande sem dinheiro e sem
pressa soma pontos de fit e engana a régua.

### 9.2 `Prioridade` (1 a 5)

Recalcule nestes 4 momentos: entrada na cadência (2.3), cada Pós-ligação
(seção 4), saída da IA (seção 6), reativação de 90 dias (seção 2.12, nó 3).
Primeira regra que casar, ganha.

**Migrado para as 5 etapas reais em 21/09/2026:** a regra 1 comparava também
contra `etapa = "Retorno agendado"` — etapa que não existe mais (tabela 1.0,
seção 1.0): "pediu retorno" não move a oportunidade, ela fica em `CONECTAR`
só com `Resultado da tentativa = Pediu retorno` gravado. O `ou` nunca casava
sozinho, mas também nunca fazia falta: todo lead que pede retorno já bate na
primeira metade da condição. Removido para não deixar um `If/Else` comparando
contra opção inexistente na tela — mesma classe de bug silencioso já
documentada para a lista `Retornos` (8.4), que já filtra só pelo campo.

| Ordem | Condição | Prioridade |
|---|---|---|
| 1 | `Resultado da tentativa` = `Pediu retorno` | 5 |
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
| 1 | Teste Atendeu | Atende na T1 | `Atendeu` → etapa `AGENDAR` → agenda → etapa `NEGOCIAR` |
| 2 | Teste Não Atende | Nunca atende, vai até o fim | 12 tentativas → `status` `abandoned` (etapa fica em `CONECTAR` — tabela 1.0) + `nutricao-90d` |
| 3 | Teste Retorno | Pede retorno na T3 | `Pediu retorno` → permanece em `CONECTAR` (não é etapa própria — tabela 1.0), Prioridade 5 |
| 4 | Teste Número Errado | Número errado na T1 | `telefone-invalido` → `status` `abandoned` ou `lost` (etapa fica onde estava) |
| 5 | Teste Não Ligar | Pede para não ligar na T2 | `nao-perturbe` + **DND ligado** → `status` `lost` (etapa fica onde estava), nenhuma mensagem depois |

### Verificações, uma por linha
| # | O que testar | Como | Passou? |
|---|---|---|---|
| 1 | Entrada na cadência | Mover para `CONECTAR` cria tag `fila-tel` e tarefa `[CADENCIA] T1` | |
| 2 | Portão de etapa | Mover para `AGENDAR` no meio da espera: a tentativa seguinte **não** dispara | |
| 3 | Portão `nao-perturbe` | Aplicar a tag na mão: próxima tentativa não dispara | |
| 4 | Portão `telefone-invalido` | Aplicar a tag: tentativa de telefone não dispara, de WhatsApp sim | |
| 5 | Limpeza do resultado | Na T2, `Resultado da tentativa` chega vazio (não herda o da T1) | |
| 6 | `Atendeu` | Registrar: conexões +1, `conectado-hoje` aplicada, etapa `AGENDAR`, tarefa `[CONECTADO]` criada, saiu da cadência | |
| 7 | `Caixa Postal` em WhatsApp | `WA não atendidas seguidas` vai a 1; repetir vai a 2 | |
| 8 | Regra das 2 seguidas | Com o contador em 2, a próxima tentativa de WhatsApp sai como **telefone** | |
| 9 | Reset do contador | Uma tentativa de telefone não atendida zera `WA não atendidas seguidas` | |
| 10 | Sem permissão | Com `Permissão WhatsApp` = `Não`, toda tentativa de WhatsApp vira telefone | |
| 11 | `Número errado` | `telefone-invalido` aplicada, `status` muda para `abandoned`/`lost` (etapa fica em `CONECTAR` — tabela 1.0), gestor notificado | |
| 12 | `Pediu retorno` | Prioridade 5, permanece em `CONECTAR`, tarefa `[RETORNO]` criada | |
| 13 | `Não ligar` | Tag + **DND ligado**; mandar mensagem de teste pelo workflow: **não** deve sair | |
| 14 | Tempo limite | Não classificar uma tentativa: às 18:30 vira `Não atendeu`, tag de fila removida, `limpar-tarefas` aplicada | |
| 15 | Mestre de saída | Qualquer mudança de etapa **ou de `status`**: nenhuma tag `fila-*` sobra e o contato sai dos 3 workflows de cadência (`Cadência 12x30`, `Cadência Inbound`, `Reengajamento 90 dias`) | |
| 16 | Mestre de saída não se morde | Mover **para** `CONECTAR` (com `status` = `open`) não aciona a limpeza | |
| 17 | Agendamento manual | SDR agenda pelo link: o Pós-agendamento dispara (é o teste do gatilho `Appointment Status`) | |
| 18 | Sticky Contact | Agendar 2 leads seguidos na mesma aba: o 2º **não** herda dados do 1º | |
| 19 | Nota | Preencher a qualificação completa e conferir a nota na mão contra a seção 9.1 | |
| 20 | Lembretes | Reagendar a reunião: os 3 lembretes se movem junto | |
| 21 | Listas inteligentes | Cada uma das 4 listas mostra exatamente os contatos esperados | |
| 22 | Rotina de manutenção | Rodar `rotina-limpar-tarefas.md`: tarefas fora do prefixo são **concluídas**, nunca excluídas, e a tag sai | |
| 23 | Volume | Simular 10 leads/dia por 5 dias e contar as tarefas geradas por dia (lacuna L-05) | |
| 24 | Loop do closer | No Teste Atendeu já em `NEGOCIAR`, simular `Nota de qualificação` ≥ 70 e preencher `Reunião foi qualificada` = `Não` com um motivo diferente de `Timing errado`: `status` vira `lost` (permanece em `NEGOCIAR` — seção 5.1), `Data do veredito do closer` grava e o gestor recebe o alerta de calibração alta (seção 5.1, nó 5) | |
| 25 | Funil por marco | No Teste Atendeu: `Data conectado` grava ao entrar em `AGENDAR`, `Data agendado` grava ao agendar, e marcar o agendamento como `Showed` grava `Data compareceu` — os três aparecem nas listas 8.10 a 8.12 no mês corrente | |
| 26 | Cadência Inbound (R-07) | Aplique `cad-inbound` num dos 5 contatos de teste antes de mover para `CONECTAR` de novo (rodada manual, decisão D-06): a Cadência Inbound dispara, **não** a 12x30 (confira que nenhuma tarefa `[CADENCIA] T1` da régua de dias nasce); `Prioridade` vira 5 e a tag `fila-quente` é aplicada na entrada; a tarefa `[CADENCIA] TI1` nasce após o Wait reduzido de teste; a mensagem `MI-0` sai antes da TI1. Deixando sem resposta até a TI5, confira o handoff: mensagem `MI-F` sai e a Cadência 12x30 assume (a tarefa `[CADENCIA] T1` da régua de dias nasce só agora) | |
| 27 | Reengajamento 90 dias (R-08) | Reduza o Wait do nó 1 (seção 2.12) para o teste. No Teste Não Atende, já com `nutricao-90d` aplicada e `status` `abandoned` em `CONECTAR` (fim natural do teste 2), aguarde o Wait reduzido: `cad-outbound` aparece, `cad-inbound` some (se esse contato tiver as duas na memória de um teste anterior), `nutricao-90d` some, `reengajamento-ativo` aparece, etapa/`status` voltam para `CONECTAR`/`open`, mensagem `RE-1` sai, e a tarefa `[CADENCIA] TR1 · … — Reengajamento` nasce depois do Wait de 2h (também reduzido) sem resposta. Confirme que a Cadência 12x30 (seção 2.1) **não** dispara uma segunda vez (nenhuma tarefa `[CADENCIA] T1` nova) — é o filtro `reengajamento-ativo` ausente fazendo o trabalho. Deixando sem resposta até a TR4, confira: mensagem `RE-2` sai, `reengajamento-ativo` some, `nutricao-90d` volta, `status` volta a `abandoned` (etapa permanece `CONECTAR`), e o próprio workflow dispara de novo (Allow Re-entry ligado) — inicia outro Wait de 90 dias sozinho | |
| 28 | Distribuição de leads (R-10) | Com pelo menos 2 usuários cadastrados na subconta de teste: mova o Teste Atendeu para `CONECTAR` e confira que o nó 0.7 sorteia um `Assigned User` (seção 2.3); mova o Teste Não Atende também e confira que o sorteio alternou para o outro usuário (round robin de verdade, não o mesmo sempre); confira que a tarefa `[CADENCIA] T1` de cada um nasce atribuída ao respectivo dono, não a quem criou o teste — é aqui que se confirma se `Add Task` aceita `Contact Owner` como destino dinâmico ou se é preciso o valor personalizado (seção 2.14); repita a entrada de um dos dois num segundo teste (rodada manual, decisão D-06) e confirme que o nó 0.7 **não** sorteia de novo (Assigned User já não está vazio) | |
| 29 | Monitor de Capacidade (R-11) | Com os 5 contatos de teste em `fila-tel`/`fila-wa` ao mesmo tempo, confira que a lista `Fila do Dia — Total` (8.16) soma os dois grupos sem duplicar ninguém; confirme se o plano da subconta expõe Custom Metrics e, se sim, que `Estouro da Fila` mostra `5 − 100` (negativo, dia normal); rode o Scheduler do "Monitor de Capacidade" manualmente (ou aguarde o horário) e confira que o Internal Notification chega ao gestor nos dois horários configurados | |
| 30 | Handoff e no-show (R-12) | No Teste Atendeu já em `NEGOCIAR`, reduza os Waits das seções 5.3/5.4 para minutos e marque o agendamento como `No Show`: `Nº de no-shows` vai a 1, o closer recebe o alerta imediato (nó 3 da 5.4), `fila-tel` é aplicada e a tarefa `[CADENCIA] NS1` nasce; confirme NS2/NS3 nascendo nos horários reduzidos e, sem resposta a nenhuma, `Template usado` = `NS-2`, `nutricao-90d` aplicada e `status` `abandoned` (permanece em `NEGOCIAR` — seção 5.3). Não deixe passar as 2h reduzidas do nó 4 da 5.4 sem reagendar: confirme o Internal Notification de escalonamento ao gestor (nó 6). Repita o `No Show` uma segunda vez no mesmo contato (rodada manual): `Nº de no-shows` chega a 2, `status` vai direto para `lost` (permanece em `NEGOCIAR`), sem tarefa nova e sem alerta de SLA ao closer (nó 2 da 5.4 encerra sozinho). Por fim, num terceiro contato, marque `No Show` e reagende pelo link do calendário antes do fim da régua: confirme que nenhuma tarefa `NS2`/`NS3` nasce depois do reagendamento (nó 3 do Pós-agendamento removeu os dois workflows do R-12) e que marcar `Showed` depois zera `Nº de no-shows` (nó 3 da seção 5.2) | |
| 31 | Higiene de base (R-13) | Antes de os 5 contatos de teste ganharem telefone, mova o Teste Não Atende para `CONECTAR` sem preencher `Phone`: o nó 0.0 aplica `telefone-invalido`; como o contato não tem `Site` (Q-02) nem `Instagram` (Q-03) preenchidos — o caso normal de lead outbound, porque esses dois só se preenchem na qualificação —, `status` vai direto para `lost` (etapa fica em `CONECTAR` — tabela 1.0; se algum dos dois estiver preenchido, `status` vai para `abandoned` + `nutricao-90d` — confira o ramo certo para o cadastro que estiver testando) e nenhuma tarefa `[CADENCIA] T1` nasce; o gestor recebe o aviso do nó 0.0b. Repita com um lead `cad-inbound` para confirmar o mesmo comportamento no nó 0.0 da Cadência Inbound (seção 2.10). Se a seção 2.16 tiver sido montada, valide também: um contato com telefone claramente fixo dispara o gatilho `Number Validation` como `Landline` e `Permissão WhatsApp` vira `Não` sem o lead sair de cadência | |
| 32 | Dashboard do Gestor (R-15) | Com pelo menos o Teste Atendeu em `NEGOCIAR` e algum dos 5 em `CONECTAR`, abra `Painel do Gestor — Pré-vendas`: o widget "Appointment Report" mostra o agendamento do calendário `Reunião com closer`; o widget "Opportunities" mostra o Teste Atendeu na etapa certa do funil ao vivo; o widget "Tasks" mostra a(s) tarefa(s) `[CADENCIA]` criada(s) hoje. Se o plano expuser Custom Metrics, confira as quatro métricas da seção 2.17 — `Estouro da Fila` negativo com só 5 contatos, `Atrasos de Speed-to-lead` em 0 (nenhum atrasou de propósito no teste), e as duas de `Taxa de Conexão` refletindo `Conexões telefone`/`Tentativas telefone` e o par de WhatsApp dos contatos de teste que já passaram por uma tentativa | |
| 33 | Horário aprendido por segmento (F-02) | No Teste Atendeu, preencha `Segmento` antes de mover para `CONECTAR` e deixe atender na T1: confira que `Hora da conexão` (C-25) grava só a hora, formato `HH`, no mesmo instante em que `Data conectado` grava; confirme que a lista `Conexão por Segmento e Horário` (8.19) mostra a linha, ordenada por `Segmento` e depois por `Hora da conexão`. Repita com um segundo contato de teste em segmento diferente e confirme que as duas linhas não se confundem na lista | |
| 34 | Porta de Entrada (L-09/L-09b) | Crie um 6º contato de teste, fora dos 5 fictícios, só com nome e telefone (sem passar por `Add Contact` de dentro de um workflow): confirme que uma oportunidade nasce sozinha em `FUNIL DE VENDAS` → `NOVO LEAD` em segundos, sem precisar mover etapa na mão; edite qualquer campo desse mesmo contato e confirme que **não** nasce uma segunda oportunidade (Allow Duplicate Opportunities desligado). Rode o backfill manual (seção 1.3) sobre os 5 contatos fictícios existentes e confirme que os 5 ganham oportunidade em `NOVO LEAD` sem duplicar nada | |
| 35 | Teto de toques por semana (F-04) | Reduza o Wait de 7 dias do "Contador de Toques" (seção 2.19) para minutos, no ambiente de teste. Force `Toques na semana` para 5 no Teste Atendeu (Update Contact Field manual) e deixe a T1 disparar: o nó 7 aplica `toque`, o Contador soma 1 (campo chega a 6) e agenda o desconto; confirme que a T2 seguinte cai no portão 2.5c/2.5d e fica represada, sem consumir `Tentativa nº` nem criar tarefa nova, até o Wait reduzido do Contador descontar e o campo cair abaixo de 6. Repita clicando o Trigger Link do Teste Retorno 3 vezes seguidas com o campo já em 6: confirme que a 3ª Interceptação de Sinal pula direto para a nota (nó 3c → 9) sem criar tarefa nem aviso ao SDR, mas a nota `Sinal: clique em link (teto...)` aparece no contato | |
| 36 | Desqualificação instantânea (R-18) | Num 7º contato de teste em `CONECTAR`, classifique `Resultado da tentativa` = `Desqualificado` + `Motivo da desqualificação` = `Sem fit`: confirme `Conexões telefone`/`Total de conexões` subindo (é conexão real), `conectado-hoje` aplicada, `fila-tel`/`fila-wa` removidas, `status` indo para `lost` **sem** a oportunidade sair de `CONECTAR` (não vai para `AGENDAR`) e **nenhuma** tarefa `[CONECTADO] Qualificar e agendar` nascendo. Repita com `Motivo da desqualificação` = `Timing errado`: confirme `status` `abandoned` + tag `nutricao-90d` em vez de `lost` | |

Depois do teste, **marque as 5 oportunidades como `status = lost` e desative
os 5 contatos** (nunca excluir contato nem oportunidade — regra 1 do
projeto) e restaure os Waits e a janela de envio.

### O que este checklist **não** testa, medido em 22/09/2026

Todo item acima exercita o CRM do mesmo jeito: escrevendo campo (quase sempre
`Resultado da tentativa`) e vendo o workflow reagir. Isso cobre tudo o que é
disparado por mudança de campo, tag ou etapa — e **não cobre nada que dependa
de um evento de telefonia real.** A diferença nunca esteve escrita, e ela
importa porque o telefone é o canal majoritário da régua (8 dos 12 toques).

Medido nesta data: as **50 conversas** da subconta não têm **um único**
registro de chamada (41 são atividade de CRM, 9 são DM de Instagram; nenhum
`TYPE_CALL` nem `TYPE_VOICEMAIL`). O contato `ZZ TESTE ESTRUTURA`, com
`Tentativas telefone` = 24, tem **uma** mensagem na conversa: "Opportunity
created". Os 24 são escritas de campo por classificação manual — o
Pós-ligação rodou 24 vezes e **o telefone nunca tocou nesta subconta.** Como
teste de workflow está correto; como evidência de telefonia, é zero.

| Item | Testável por mudança de campo? | Por quê |
|---|---|---|
| Tudo de 1 a 36 acima | **Sim** | Gatilho é campo, tag ou etapa |
| **F-06 / seção 2.27** (`Duração da ligação`, `Conexão real`, C-31, C-32) | **Não** | O gatilho é `Transcript Generated`: exige chamada **discada e gravada**. Não existe campo que simule uma transcrição |
| **F-08 / seção 2.26** (reputação do número) | **Não** | Bloqueio de operadora acontece na rede ou no aparelho do lead; não há objeto de CRM para simular |
| **F-09** (freio de telefone, quando o dono escolher o limiar) | **Parcial** | O contador e o portão se testam por campo; a duração real das chamadas que alimentam a decisão, não |

**Consequência prática, que é uma dependência nova:** o F-06 só pode ser
testado depois de existir uma ligação real por LC Phone, com gravação e
transcrição ligadas. Isso encadeia três pendências que os documentos tratavam
como independentes — a confirmação de canal (LC Phone vs. linha própria), a
decisão de gravar (aviso LGPD + custo) e a criação dos campos C-29 a C-32 —
e coloca a confirmação de canal como **primeira** delas, não como detalhe
lateral. Nenhuma pode ser marcada `[x]` por leitura de CRM: todas passam pela
tela e pelo dono.

---

## 11. O que o MCP não faz (resumo)

**Atualizado em 18/09/2026 — distinção que não existia até aqui.** Pesquisa
direta na especificação OpenAPI oficial da HighLevel (repositório público
`github.com/GoHighLevel/highlevel-api-docs`, lido arquivo por arquivo, não
só busca) confirmou que "não sai por API" tinha dois motivos diferentes
misturados numa frase só, e a tabela agora separa os dois:

| Item | Este conector (`GHL CRM`) | API oficial da HighLevel | Manual |
|---|---|---|---|
| Campos personalizados | Não | **Sim** — `POST /locations/{locationId}/customFields`, escopo `locations/customFields.write`, `model: contact\|opportunity` decide o tipo | Cria na tela; lista com tipo e opções em `campos-e-tags.md` — **ou** via API, se o conector ganhar essa ferramenta (ver nota abaixo) |
| Tags | Cria | Sim | — |
| Pipeline e etapas | Não | **Não** (confirmado: só `GET /opportunities/pipelines` existe no spec; `opportunities.write` não cobre pipeline; issue aberta nº 248 no repo oficial pedindo exatamente isso, sem endpoint ainda) | Seção 1 — sem alternativa por API, de ninguém |
| Workflows | Não | **Não** (só `GET /workflows/` existe; sem POST em nenhuma versão do spec) | Seções 1.3, 2, 2.9, 2.11, 2.15, 2.19, 3 a 6, 5.1, 5.2 — sem alternativa por API |
| Calendário | Lê | **Sim** — `POST /calendars/`, escopo `calendars.write`, corpo com `locationId`+`name` obrigatórios e dezenas de campos opcionais (disponibilidade, buffers, confirmação automática) | Cria e configura: seção 7.1 — **ou** via API, se o conector ganhar essa ferramenta |
| Formulário | Não (nem lê, neste toolkit) | **Não** (só leitura/submissions/upload de arquivo; sem endpoint de criação da estrutura) | Seção 7.2 — sem alternativa por API |
| Listas inteligentes | Não | Não documentado como recurso de API pública | Seção 8 |
| Métrica personalizada (dashboard) | Não | Não documentado como recurso de API pública | Cria na tela: seção 2.15 (R-11), seção 2.17 (R-15) |
| Number Validation (ativação) | Não | Recurso de conta, não de API | Ativa na tela, Configurações → Telefone: seção 2.16 (R-13) |
| Dashboard nativo | Não | Não documentado como recurso de API pública | Cria na tela: seção 2.17 (R-15) |
| Conversation AI | Não | — | Seção 6 |
| Concluir tarefa em massa | Sim | Sim | É a rotina da seção 5 do projeto |

**O que isso muda na prática:** pipeline, workflow e formulário continuam
100% manuais — não é limitação de ferramenta, é a própria HighLevel não
expor esse endpoint para ninguém. Campo personalizado e calendário são
diferentes: a plataforma permite criar os dois por API, só que o conector
`GHL CRM` conectado nesta sessão (36 ferramentas, focado em contato/tag/
oportunidade/conversa) não implementa essas duas chamadas. Fechar esse gap
não depende de esperar a HighLevel lançar nada — depende de anexar um
conector com cobertura maior (por exemplo, o toolkit HighLevel do Composio,
citado como caminho alternativo desde `briefing-sdr.md`, "Estado do
acesso") ou de pedir para quem administra este conector adicionar as duas
ferramentas que faltam (`locations_create-custom-field`,
`calendars_create-calendar`, nomeação hipotética). Detalhe completo,
endpoint por endpoint, com todas as fontes: `APRENDIZADOS-CRM.md`.
