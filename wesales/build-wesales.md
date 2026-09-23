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
31. Workflow "Resgate por E-mail — Sem Telefone" (seção 2.30, F-15) — não
    depende de nenhum passo anterior além dos campos/tags do passo 1 (todos
    já existentes); monte a qualquer momento depois do R-08 (passo 18)
    estar publicado, porque os dois escutam o mesmo gatilho (`Contact Tag
    Added: nutricao-90d`) e a leitura fica mais fácil comparando os dois
    lado a lado. Confirme antes de montar: a subconta tem domínio de
    e-mail verificado para envio transacional (não checável por este
    conector)

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
| 2 | `REUNIÃO DE DIAGNÓSTICO` (renomeada de `AGENDAR` em 23/09/2026, mesmo `id`) | 50% | `#2DD4BF` |
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
| `Conectado` | `REUNIÃO DE DIAGNÓSTICO` (nome na tela até 22/09/2026: `AGENDAR`, mesmo `id` — ver nota abaixo) | Mesma etapa |
| `Retorno agendado` | **continua em `CONECTAR`** | Deixou de ser etapa própria — "pediu retorno" não move a oportunidade, só grava `Resultado da tentativa = Pediu retorno`. Todo gatilho `Opportunity Stage Changed → Retorno agendado` vira **sem gatilho de etapa nenhum**: o lead nunca sai de `CONECTAR`, e a lista `Retornos` (8.4) filtra só pelo campo |
| `Reunião agendada` | `NEGOCIAR` | Absorve também a negociação do closer (proposta, condições), que no plano de 7 ficava fora do pipeline — agora está dentro, porque o dono optou por 1 pipeline só |
| `Nutrição` | **status da oportunidade = `abandoned`**, etapa fica como estava | Todo gatilho `Opportunity Stage Changed → Nutrição` vira **`Contact Tag Added → nutricao-90d`** (gatilho nativo já usado em outro lugar do projeto) — a tag continua sendo o sinal de quem está nutrição, o status só formaliza isso no campo nativo do GHL |
| `Descartado` | **status da oportunidade = `lost`**, etapa fica como estava | Todo gatilho `Opportunity Stage Changed → Descartado` vira uma ação `Update Opportunity` mudando o `status`, não a etapa |
| *(não existia)* | `FORMALIZAR` | Etapa nova, fechamento/contrato — equivale a `status = won`. Fora do escopo dos workflows de SDR deste documento (é o closer fechando), citada aqui só para a tabela ficar completa |

> **Segunda renomeação, 23/09/2026 — `AGENDAR` também já não é o nome na
> tela.** Fora do plano de 7 desta tabela: o dono decidiu, em
> `wesales/PLANO-MULTICANAL.md` (D1/E2), renomear a etapa `AGENDAR` para
> `REUNIÃO DE DIAGNÓSTICO` — **mesmo `id`**
> (`3d26fcd1-220d-49ed-8325-705dfe9055b1`), confirmado por
> `opportunities_get-pipelines` de novo em 23/09/2026, sessão seguinte
> (`dateUpdated` ainda 2026-09-23T00:59Z, sem mudança). Todo workflow
> publicado que decide por `pipelineStageId` (não por nome) continua
> funcionando sem tocar em nada — é o caso de todos os já montados. O que
> fica desatualizado é só texto. **Atualização desta rodada:** o código já
> não está mais desatualizado — `wesales/tools/ghl_api.py` (`STAGES`) já
> tem as duas chaves, `"AGENDAR"` e `"REUNIÃO DE DIAGNÓSTICO"`, apontando
> para o mesmo `id`, com comentário explicando o apelido — feito por fora
> desta sessão, entre a rodada que escreveu este parágrafo e esta. Migração
> de **texto puro**, promovida a item próprio em
> `ROADMAP-SALES-ENGAGEMENT.md`, G-12, **está completa desde 23/09/2026
> (peça 2):** a tabela desta seção (1) e a linha `Conectado` da tabela acima
> saíram na peça 1; as seções 2 em diante deste documento e todo
> `ROADMAP-SALES-ENGAGEMENT.md` saíram na peça 2 — nenhuma delas trata mais
> `AGENDAR` como etapa corrente. Nomes próprios publicados na tela com "AGENDAR" no texto (o
> workflow `AGENDAR Estagnado`, a lista `Saúde — AGENDAR Estagnado`) **não**
> entram nesta migração — são o nome real do objeto, trocar o texto aqui
> sem renomear o objeto na tela criaria uma divergência nova, pior que a
> atual. Detalhe da régua (o que migra, o que fica) em G-12.

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
| Meio do funil — Qualificação (pré-venda) / Contato-Abordagem | `CONECTAR` (inclui quem pediu retorno) e `REUNIÃO DE DIAGNÓSTICO` (`AGENDAR` até 22/09/2026) | O genérico trata como 1-2 fases; aqui seguem 2 estados **porque cada um é o que um workflow consulta** (seção 2.4, nó 3) — "tentando conectar (ou cumprindo retorno combinado)" e "conectado, ainda sem reunião marcada" precisam de portão próprio, senão a régua de 12 tentativas não sabe quando parar |
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

#### Etapa 1 — `CONECTAR` (absorve o antigo `Retorno agendado` **e**, desde 23/09/2026, a fase "fechar horário" — ver aviso abaixo, G-13)

> **Correção de 23/09/2026 (G-13):** as linhas "Validação de passagem" e
> "Motivos de perda" abaixo diziam que `Atendeu` move a oportunidade para
> `REUNIÃO DE DIAGNÓSTICO`. Isso valia até a D3 do `PLANO-MULTICANAL.md`
> (22/09/2026, publicada em 23/09): hoje `Atendeu` **fica** em `CONECTAR`,
> numa fase própria ("fechar horário": tag `fechar-horario`, workflow
> `Fechar Horário`, até 3 dias reengajando por mensagem antes de cair em
> nutrição). Só o agendamento de fato (`Pós-agendamento v2`) move a
> oportunidade para `REUNIÃO DE DIAGNÓSTICO`. Detalhe em `build-wesales.md`
> seção 4 (ramo `Atendeu`) e `ROADMAP-SALES-ENGAGEMENT.md`, G-13.

| Bloco | Conteúdo |
|---|---|
| Objetivo | Conseguir uma conexão real (`Atendeu`) dentro das 12 tentativas em 30 dias, **e então** fechar o horário da reunião de diagnóstico — inclui quem já foi contatado e pediu para ligar depois: esse lead não sai da etapa, só muda o que `Resultado da tentativa` guarda |
| Validação de passagem | `Resultado da tentativa` = `Atendeu` **não** muda mais etapa (nó A6 do ramo `Atendeu`, seção 4) — o lead fica em `CONECTAR`, fase "fechar horário". Só sai para `REUNIÃO DE DIAGNÓSTICO` quando a reunião é de fato marcada no calendário (`Pós-agendamento v2`, seção 5, nó 1). `Pediu retorno` também **não muda etapa**: o lead fica em `CONECTAR`, e a lista `Retornos` (8.4) filtra só pelo valor do campo, sem OR com etapa nenhuma |
| Ferramentas | Workflows Cadência 12x30/Inbound/Reengajamento, listas `Fila Telefone Hoje`/`Fila WhatsApp Hoje` (8.2/8.3), lista `Retornos` (8.4), `script-de-ligacao.md`; **fase "fechar horário":** tag `fechar-horario`, tarefa `[FECHAR HORÁRIO] Qualificar e agendar a reunião de diagnóstico`, workflow `Fechar Horário` (mensagens `MFH1-v1`/`MFH2-v1`) |
| Tempo de estagnação | Já coberto: F-05 (roadmap, peça 3 — seção 2.22) monitora `CONECTAR` sem avanço na fase de tentativa; a 1ª tentativa tem relógio próprio (Alerta de Speed-to-lead, seção 2.11). A fase "fechar horário" tem o próprio relógio dentro do workflow `Fechar Horário` (3 dias até nutrição) — não tem alerta ao gestor ainda, pendência aberta no G-13. O antigo gap "retorno vencido sem nova ligação" (S-01, `Data de retorno`/`Hora do retorno`, na tela desde 21/09/2026) continua valendo aqui dentro |
| Motivos de perda | `Número errado` (→ `telefone-invalido`), `Não ligar` (→ opt-out, DND) — saem da etapa via `Update Opportunity` para `status = lost`; 12 tentativas esgotadas sem conexão → `status = abandoned` **+** tag `nutricao-90d`, **sem sair de `CONECTAR`**; conectado e sem fechar horário em 3 dias → mesmo destino (`abandoned` + `nutricao-90d`), pelo `Fechar Horário` — todas sem movimento de etapa (era "→ `Nutrição`" no plano de 7) |
| Taxa de conversão esperada | ~35% conectam ou saem antes das 12 tentativas (L-05, `briefing-sdr.md`) — mesma hipótese que já dimensiona o volume de entrada; taxa de quem conecta e **fecha horário** dentro dos 3 dias ainda não medida (canal novo, G-13) |
| Meta de avanço | 100 ligações/dia é a meta do SDR (briefing); quantos *leads* avançam por dia é `Total de conexões` (C-07) somado, lido na lista `Conexão por Tentativa` (8.6, R-01) |

#### Etapa 2 — `REUNIÃO DE DIAGNÓSTICO` (nome na tela até 22/09/2026: `AGENDAR`, mesmo `id`) — **entrada mudou em 23/09/2026, ver aviso na Etapa 1 (G-13)**

| Bloco | Conteúdo |
|---|---|
| Objetivo | Reunião marcada; qualificação (formulário do closer) e fechamento de horário já aconteceram **antes** de entrar aqui, dentro de `CONECTAR` (D2 do `PLANO-MULTICANAL.md`) — esta etapa é a espera até a reunião acontecer e o veredito do closer |
| Validação de passagem | Agendamento no calendário `Reunião com closer`, feito pelo SDR ainda em `CONECTAR` — dispara o `Pós-agendamento v2` (seção 5), que move para cá |
| Ferramentas | Calendário + confirmação/lembretes (`Pós-agendamento v2`, seção 5) |
| Tempo de estagnação | **Não coberto mais por monitor nenhum** (peça 5 do F-05/W17d foi despublicada, premissa impossível — `build-wesales.md` seção 2.23, G-13). Como a entrada aqui já exige reunião marcada, o relógio relevante é o `No-show`/`SLA do Closer` (seção 5.3/5.4), não um "ficou parado" genérico |
| Motivos de perda | O ramo `Desqualificado` do Pós-ligação (R-18, seção 4) já tira a maioria dos "sem fit na ligação" **antes** de chegar aqui, ainda em `CONECTAR`. O que chega em `REUNIÃO DE DIAGNÓSTICO` tem reunião marcada; perda a partir daqui é veredito do closer (Loop do closer, seção 5.1) ou no-show |
| Taxa de conversão esperada | Reunião realizada vs. agendada (no-show) — não é mais "sem fit", que sai antes |
| Meta de avanço | Ligado à meta de conexões que fecham horário (etapa anterior) — sem meta própria adicional |

#### Etapa 3 — `NEGOCIAR` (absorve `Reunião agendada` + a negociação do closer)

| Bloco | Conteúdo |
|---|---|
| Objetivo | Comparecimento + veredito de qualificação real do closer, e a negociação em si (proposta, condições) até a decisão de compra — a metade "negociação" não existia no plano de 7 etapas, que a mandava para fora do pipeline |
| Validação de passagem | `Reunião foi qualificada` preenchida pelo closer (Loop do closer, seção 5.1) para a metade "comparecimento"; para a metade "negociação", decisão do closer registrada como `status = won` (→ `FORMALIZAR`) ou `status = lost` (permanece em `NEGOCIAR` com o status marcado, não some da tela) |
| Ferramentas | Calendário, Registro de Comparecimento (5.2), Loop do closer (5.1), SLA do Closer — No-show (5.4, R-12); a negociação em si (proposta/condições) é conduzida pelo closer fora dos workflows deste documento |
| Tempo de estagnação | A metade "comparecimento" já está coberta — é literalmente o R-12: SLA do closer com escalonamento ao gestor (seção 5.4). A metade "negociação" (depois do `Reunião foi qualificada = Sim`) ficou sem monitor até 22/09/2026: F-05 fechou com seis peças sem incorporar este gap, apesar de citado aqui como candidato desde a etapa ser escrita. Fechado como item próprio, F-13 (roadmap), seção 2.28 abaixo |
| Motivos de perda | No-show 2x seguido (R-12: `status = lost` mantendo a oportunidade em `NEGOCIAR`, não um "mover para `Descartado`" — migrado nas seções 5.3 e 5.4 em 19/09/2026; este parágrafo dizia "ainda usa a redação antiga e entra na fila" até 21/09, quando a fila já não existia), `Reunião foi qualificada` = `Não` (→ roteamento da seção 5.1, mesma troca de "mover etapa" por "mudar status") |
| Taxa de conversão esperada | "nota ≥ 70 acerta X%" é exatamente o que a lista `Calibração da Régua` (8.7, F-03) mede |
| Meta de avanço | Função da nota de qualificação (seção 9.1) e do volume que chega de `REUNIÃO DE DIAGNÓSTICO` |

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
| 0.6 | Update Contact Field | `Entrada em` = `{{right_now.date}} {{right_now.time}}` (`{{right_now}}` puro grava `[object Object]` — medido em 22/09/2026) (R-02 — carimbo de speed-to-lead) |
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
| 5c | Carimbo | Update Contact Field | `1ª tentativa em` = `{{right_now.date}} {{right_now.time}}` (`{{right_now}}` puro grava `[object Object]` — medido em 22/09/2026) |
| 5d | Limpeza preventiva | Remove Contact Tag | `atraso-1a-tentativa` (barato mesmo se ausente — ver seção 2.11) |

Não repita 5c/5d nas tentativas 2 a 12: T1 é sempre a primeira do molde (delta
0d, sem tentativa antes dela), então `1ª tentativa em` só precisa de uma
escrita — a mesma lógica de "Total de conexões" ter um dono só (seção 4).

O contador `WA não atendidas seguidas` **não** é mexido aqui — quem soma e
zera é o Pós-ligação (seção 4), que é o único lugar que sabe qual foi o canal
e o resultado. Um contador com dois donos sempre diverge.

### 2.5 As 12 tentativas

> **Decisão do dono em 22/09/2026 — as réguas são 100% telefone.** O canal
> "Ligação WhatsApp" saiu do jogo. As quatro réguas foram remontadas e
> publicadas assim (commit `d52e61d`): **12x30 com 12 toques de telefone**,
> **Inbound com 5**, **Reengajamento com 4**, **No-show com 3** (esta já era).
> Medido no payload publicado, não deduzido do commit: a `Cadência 12x30` tem
> 12 nós `add_contact_tag` com `fila-tel` e **nenhum** nó que adicione
> `fila-wa` — a tag só sobrevive em 24 nós `remove_contact_tag`, como limpeza
> defensiva de quem carregava a tag da versão anterior.
>
> **A tabela abaixo é o registro histórico da régua alternada e não descreve
> mais o que está no ar.** Onde ela diz `Ligação WhatsApp` / `fila-wa`, leia
> `Telefone` / `fila-tel`. A contagem de toques não mudou: continuam 12 em 30
> dias. O que desapareceu foram os nós de mensagem (M1/M2/M3) — numa operação
> só de ligação eles não existem, e é por isso que as réguas deixaram de estar
> incompletas.
>
> **Consequência que não está nas tabelas:** `fila-wa` virou uma tag que nada
> mais aplica. Toda lista, widget ou gatilho deste documento que dependa dela
> passou a ser letra morta — os pontos onde isso é carregante estão corrigidos
> no lugar (métrica `Estouro da Fila`, seções 2.15 e 2.17; gatilhos do F-05
> peça 2, seção 2.21). Se aparecer outro, é bug de propagação desta decisão,
> não regra nova.
>
> **Efeito colateral a considerar, não medido:** com o WhatsApp fora, o volume
> de ligações por lead aproximadamente dobra. Os critérios do Despacho
> Decisório nº 82/2026 (volume, proporção de chamadas muito curtas, duração
> média, taxa de completamento) passam a ser avaliados sobre esse volume
> maior. Não é motivo para voltar atrás; é motivo para a aplicação ao
> `Origem Verificada` subir de prioridade.

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
texto pelo seletor da tela (só Custom Values fixos e outros campos) — por
isso `Data e hora do sinal` **chegou a sair** da lista de nós naquele dia
(**revertido em 22/09/2026, ver nota logo abaixo — o nó 5b da tabela volta a
gravá-lo**). Tarefa e Nota continuam carimbando a própria data de criação
nativamente, o que já cobria parte da mesma necessidade de auditoria mesmo
sem o campo. A tabela abaixo é a sequência real, não a original.

**Consequência que parecia grande em 19/09/2026, e por que não travou nada —
achado revendo o item em 22/09/2026:** esta seção chegou a descartar
`Data e hora do sinal` (C-14) da lista de nós porque, montando ao vivo na
tela naquele dia, o seletor de valor de `Update Contact Field` não parecia
oferecer "data/hora atual" para um campo `TEXT`. A dúvida ficou registrada
como aberta (`APRENDIZADOS-CRM.md`, "Pesquisa que corrobora (não fecha) o
`{{right_now}}`") porque só quem tem a tela aberta fecharia — e ninguém tinha
motivo para reabrir, já que nenhum destes dois workflows tinha sido publicado.

O motivo de reabrir agora: a montagem deste projeto **deixou de ser só clique
manual** depois de 19/09/2026 — passou a sair também pela API interna
(`wesales/tools/`, `GUIA-MONTAGEM.md`, "Estado da montagem em 21/09/2026"),
que grava o valor do campo direto no payload, sem depender do que o seletor
visual oferece na tela. E essa mesma API **já provou, rodando de verdade**,
que `{{right_now}}` escreve num campo `TEXT` de contato: `Entrada em` (C-18,
mesmo tipo `TEXT` de C-14) foi carimbado com sucesso ao promover um contato de
teste para `CONECTAR` (`GUIA-MONTAGEM.md`, "Testado de ponta a ponta, com
rastro lido pela API"). A limitação de 19/09 era do **seletor clicável**, não
do campo nem do token — e o caminho de montagem que a operação usa hoje não
passa mais por aquele seletor. Os 17 nós que já contavam com
`{{right_now}}` em campo `TEXT` (inclusive `Entrada em`/`1ª tentativa em`, R-02)
estavam certos o tempo todo; **`Data e hora do sinal` é quem estava descartado
sem precisar** — restaurado abaixo, nó 5b.

~~A fallback "marca, não carimbo" (gravar `sim` em vez da hora) que esta seção
chegou a desenhar como plano B nunca foi necessária e não é mais o caminho:
nenhum nó deste documento usa esse formato hoje, `Entrada em`/`1ª tentativa
em` gravam `{{right_now}}` completo desde a primeira versão (seção 2.3, nó
0.6, e os resets da seção 2.4/2.10), e é isso que está publicado e testado.~~

> **Medido em 22/09/2026, 18:30 UTC, e é o contrário disto.** Li os campos
> pela API nos contatos que os têm preenchidos:
>
> | Contato | `Entrada em` (C-18, TEXT) | `1ª tentativa em` (C-19, TEXT) |
> |---|---|---|
> | `Teste Número Errado` (`qkHSdIMPJTB2JK5ECGrY`) | `"sim"` | `"sim"` |
> | `Teste Retorno` (`vrwdERfR24ax6GylG6No`) | `"sim"` | `"sim"` |
> | todos os demais, inclusive `Carlos Andrade` | vazio | vazio |
>
> **Nenhum contato da base tem hora nesses campos.** Os dois únicos que têm
> qualquer coisa têm a string literal `sim` — exatamente o formato "marca,
> não carimbo" que o parágrafo riscado diz que nunca foi usado. A frase "e é
> isso que está publicado e testado" descreve o inverso do que está no CRM.
>
> **O que isso derruba e o que não derruba.** Não derruba o nó 5b, e **não
> apaguei o nó**: apagar agora repetiria o erro ao contrário — decidir sem
> medir. Derruba a **justificativa**: não existe, em lugar nenhum desta base,
> evidência de que `{{right_now}}` renderize em campo `TEXT`. A prova citada
> para restaurar o nó é de um carimbo que não está lá.
>
> **Consequência maior que o C-14, e é por isso que esta nota está aqui e não
> num rodapé:** o R-02 (speed-to-lead) e toda comparação de "`Entrada em` há
> mais de 1h" (seção 2.3 e a lista da seção 8) dependem desses dois campos
> terem hora. Se o que a régua publicada grava for `sim`, essas medições não
> estão erradas por pouco — **não estão medindo nada**, e nunca dão erro.
>
> **O teste que fecha isso custa um minuto e só se faz na tela** (a API
> pública não lê nó de workflow): abrir o nó 0.6 da Cadência 12x30 e ver o
> que está no campo — `{{right_now}}` ou `sim`. Alternativa sem abrir o
> builder: promover um lead de teste e reler `Entrada em` pela API. Enquanto
> não for feito, tratar o formato de C-18/C-19 como **desconhecido**, e o
> "formato igual ao de C-18/C-19" do nó 5b abaixo como o que é: uma
> referência a um formato que ninguém confirmou.

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Buscar oportunidade | Find opportunity | Pipeline: `FUNIL DE VENDAS` · "Most recently created opportunity" → ramo **Opportunity Not Found**: encerra (vazio) · ramo **Opportunity Found**: segue |
| 2 | Portão de etapa e status | If/Else | `Pipeline stage` é `[FUNIL DE VENDAS] - CONECTAR` **E** `status` da oportunidade **não é** `lost` → ramo verdadeiro (Branch): segue · ramo falso (None): **encerra** (quem já saiu de cadência por etapa não precisa furar fila, e quem saiu como `lost` pediu para não ser procurado ou tem telefone errado — ver nota abaixo sobre o `abandoned`) |
| 3 | Portão de silêncio | If/Else | Tags inclui `nao-perturbe` → ramo verdadeiro (Branch): **encerra** · ramo falso (None): segue |
| 3c | Portão de frequência (F-04) | If/Else | `Toques na semana` **≥** 6 → ramo verdadeiro: pula direto para o nó 9 · ramo falso: segue para o nó 4 |
| 4 | Prioridade | Update Contact Field | `Prioridade` = 5 |
| 5 | Registro do sinal | Update Contact Field | `Sinal recebido` = `Clique em link` |
| 5b | Carimbo do sinal | Update Contact Field | `Data e hora do sinal` = `{{right_now}}` — restaurado em 22/09/2026, ver nota acima; formato igual ao de C-18/C-19 |
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

**Gatilho:** `Customer Replied` — Canal: **WhatsApp e SMS**. Decisão ao vivo
do dono, 19/09/2026: SMS nunca foi canal real da cadência (só telefone,
ligação por WhatsApp e mensagem de WhatsApp — `briefing-sdr.md`), e o dono
confirmou que não usa SMS em nenhum canal de contato com lead. O plano
original media "WhatsApp e SMS" errado, como se fossem os dois canais de
texto — não eram, e isso continua valendo: SMS não é canal de contato deste
projeto. **O SMS entrou de volta no filtro por um motivo técnico, não
estratégico (G-09, 23/09/2026):** o único WhatsApp conectado nesta subconta
é a integração não-oficial Stevo (QR), que entrega mensagem como
`TYPE_CUSTOM_SMS` por baixo do capô (confirmado por API — a conversa do
contato de teste `Francisca` traz esse tipo, não `TYPE_WHATSAPP`), com um
script que só troca o rótulo "SMS" por "WhatsApp QR" na tela. Se o filtro
"Canal: WhatsApp" reconhece só o tipo nativo, nenhuma resposta pela Stevo
dispara este gatilho — o canal que o filtro precisa escutar de verdade é
esse, mesmo chamando "WhatsApp" na intenção do projeto. Filtro aditivo
(WhatsApp **e** SMS, não WhatsApp trocado por SMS) para cobrir os dois
cenários sem depender de qual rótulo a tela confirmar — detalhe e fontes no
G-09.

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

**Gatilho:** `Customer Replied` — Canal: **WhatsApp e SMS** (o SMS entrou
pelo mesmo motivo técnico do 2.9.3, não por decisão de canal — a Stevo
entrega o único WhatsApp desta subconta como `TYPE_CUSTOM_SMS`; detalhe e
fontes no G-09) — `Contains Phrase`,
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

### 2.9.6 Workflow "Opt-out por Palavra-chave — E-mail" — G-07

**Por quê:** o 2.9.5 (acima) só escuta `Customer Replied` no canal WhatsApp
— o único canal de texto que existia no projeto quando o R-17 foi escrito
(21/09/2026). O F-15 (seção 2.30, mesmo dia 22/09/2026) abriu o primeiro
canal novo desde então, e-mail, e o único ponto que manda e-mail
(`Resgate por E-mail — Sem Telefone`) trata **toda** resposta do mesmo jeito
que o 2.9.3 tratava toda resposta de WhatsApp antes do R-17: o nó 4/7
daquele workflow (`Wait → Contact Replied`, canal e-mail) não olha o
conteúdo — uma resposta "pare de me mandar e-mail" cai no mesmo ramo que uma
resposta "tenho interesse, me liga": `Internal Notification` ao gestor
pedindo decisão manual, sem tag `nao-perturbe` nem DND aplicados sozinhos.
Não é o mesmo bug do R-17 (nenhuma tarefa "ligar agora" nasce daqui — o ramo
já é cauteloso, só notifica), mas é a mesma classe de defeito que o R-17
documentou como inaceitável para WhatsApp: **"o único jeito de um opt-out
virar DND é alguém ler a mensagem e lembrar de desligar tudo na mão"** —
aqui, literalmente a mesma frase, trocando SDR por gestor e WhatsApp por
e-mail. Achado ao reler o 2.30 depois de ler o R-17 com atenção: o próprio
"Como" do R-17 já dizia que Reev/Meetime/Outreach/Salesloft tratam opt-out
"como estado de contato/lista (unsubscribe...)" porque o canal principal
deles é e-mail — e justamente por isso é o canal onde o projeto tem menos
desculpa para deixar a mesma lacuna aberta.
**O que já está protegido, e não precisa de nada novo (pesquisado antes de
desenhar, `WebSearch`):** todo e-mail enviado pela plataforma nativa do GHL
já sai com um link de descadastro automático (`{{unsubscribe}}`, inserido no
rodapé mesmo sem configuração extra) — clicar nele já aplica opt-out sem
depender de workflow nenhum, o mesmo papel que o link de Trigger cumpre para
recurso mais avançado. Isso cobre LGPD (art. 18, direito de revogar
consentimento a qualquer momento — o descadastro por clique já entrega isso)
e cobre quem simplesmente clica em vez de responder por escrito. **O que não
está protegido é a resposta por texto** — o mesmo ponto cego que o WhatsApp
tinha antes do R-17, porque nem todo lead usa o link; alguns respondem o
e-mail como se fosse uma conversa, do mesmo jeito que respondem WhatsApp.
**Como:** mesmo padrão do 2.9.5, canal trocado — workflow novo, separado do
`Resgate por E-mail — Sem Telefone` (mesma razão já registrada em
`APRENDIZADOS-CRM.md` para não empilhar duas responsabilidades num workflow
só: este é um listener global por conteúdo, aquele é uma régua de 2 e-mails
com relógio próprio; a convivência dos dois no mesmo contato, quando ambos
reagem à mesma resposta, é tratada abaixo).

**Gatilho:** `Customer Replied` — Canal: **E-mail** — `Contains Phrase`, a
mesma lista canônica do 2.9.5/2.9.3 (`pare de`, `pare com`, `para de mandar`,
`para de me mandar`, `não quero mais mensagem`, `não quero mais contato`,
`não quero receber mensagem`, `não quero receber mais`, `remove meu
contato`, `tira meu número`, `descadastr`, `cancelar inscri`, `não me liga
mais`, `não me mande mais`, `sai da lista`, `me tira da lista`,
`unsubscribe`) — reaproveitada sem alteração, de propósito: ao contrário do
par 2.9.3/2.9.5 (que **precisam** ser idênticas porque escutam o mesmo canal
e concorrem pelo mesmo evento), este workflow escuta um canal diferente e
não tem esse risco — reaproveitar a lista existente só evita manter uma
terceira versão do mesmo texto sem necessidade. `pare`/`stop`/`não quero
mais` soltos continuam de fora pelo mesmo motivo do 2.9.5 (`Contains` casa
pedaço de palavra — "parece ótimo" também vale em e-mail).

| Configuração | Valor |
|---|---|
| Janela de envio | Sem restrição, 24/7 — mesmo motivo do 2.9.5: nenhum nó manda mensagem, DND atrasado é o oposto do que o item existe para evitar |
| Allow Re-entry | Ligado — mesmo motivo do 2.9.5 |
| Stop on Response | Desligado |

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Buscar oportunidade | Find opportunity | Pipeline: `FUNIL DE VENDAS` · "Most recently created opportunity" — os dois ramos seguem, mesmo motivo do 2.9.5 |
| 2 | Silêncio | Add Contact Tag | `nao-perturbe` |
| 3 | DND | Set Contact DND = ligado, todos os canais | Mesmo nó do 2.9.5 — já medido nesta subconta que grava a flag dos seis canais (inclusive canais não integrados), seção 8.26 |
| 4 | Sair das filas | Remove Contact Tag | `fila-tel`, `fila-wa`, `fila-quente` |
| 5 | Sair das réguas | Remove Workflows | `All Except Current Workflow` — inclui o `Resgate por E-mail — Sem Telefone`, então o nó 4/7 daquele workflow deixa de esperar (ver nota abaixo sobre o aviso duplicado) |
| 6 | Fechar o negócio, com cautela | If/Else | Achou oportunidade **E** etapa é `CONECTAR` **E** `status` é `open` → Update Opportunity `status` = `lost`. Senão → Internal Notification ao `Contact Owner`, mesmo texto do 2.9.5 trocando "WhatsApp" por "e-mail" |
| 6b | Aviso, sempre | Internal Notification | Mesmo texto do 2.9.5, mesma troca de canal |
| 7 | Registro | Add Note | `Opt-out por palavra-chave (e-mail) detectado em {{right_now}} · DND ligado · removido de todas as réguas automáticas` |

**Redundância aceita, não escondida:** quando a resposta de opt-out chega
enquanto o lead está dentro do `Resgate por E-mail — Sem Telefone` (esperando
no nó 4 ou 7), os dois workflows reagem ao mesmo evento — este aplica DND e
remove o lead de todas as réguas (nó 5, que inclui o próprio Resgate), e o
nó 4b/7b do Resgate dispara em paralelo com sua notificação genérica
("respondeu, decisão manual"). O gestor recebe dois avisos do mesmo evento
em vez de um. Diferente do 2.9.3/2.9.5 (onde o filtro cruzado é
obrigatório porque um dos dois manda uma tarefa **errada** — "ligar agora"
para quem pediu silêncio), aqui os dois avisos dizem coisas compatíveis
(um diz "DND aplicado", o outro diz "revisar manualmente") — nenhum dos
dois instrui uma ação incorreta. Corrigir a duplicação exigiria o mesmo
filtro cruzado do 2.9.3 dentro do nó 4/7 do 2.30, que é um `Wait`, não um
gatilho — **não confirmado na tela** se o nó `Wait → Contact Replied`
aceita o mesmo filtro de conteúdo que a trigger `Customer Replied` aceita;
registrado como retoque de segunda ordem, não bloqueia este item.

**Zero campo e zero tag novos:** reaproveita `nao-perturbe` (T-06) e o DND
nativo, mesmos do 2.9.5. Falta só a criação manual do workflow — não sai
por API; não depende de `APROVADO.md`.

**Pronto quando:** um lead que responde pedindo para parar de receber
e-mail sai de toda cadência automática e fica com DND ligado no mesmo
minuto, sem depender de o gestor ler a notificação genérica do 2.30 e agir
na tela — mesmo padrão que o R-17 já garante para WhatsApp.

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
| 0.6 | Update Contact Field | `Entrada em` = `{{right_now.date}} {{right_now.time}}` (`{{right_now}}` puro grava `[object Object]` — medido em 22/09/2026) (mesmo campo do R-02 — a métrica de speed-to-lead nasceu para o outbound e serve de graça aqui, sem custo nenhum) |
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
| 2 | Portão | If/Else — condições **E** | Status da oportunidade **é** `abandoned` · tag `nutricao-90d` presente · tag `nao-perturbe` ausente · tag `telefone-invalido` ausente (G-08, 22/09/2026 — ver nota abaixo) |
| 2b | Ramo falso do portão | **Remove from Workflow: este** | Três motivos possíveis, nenhum reativa: o lead já saiu do estado de nutrição por outro caminho (voltou a `CONECTAR` na mão e converteu — `status` deixou de ser `abandoned` —, ou foi descartado, `status = lost`); pediu para não ser mais procurado; ou nunca teve telefone válido (`telefone-invalido`, aplicada no nó 6 da Cadência 12x30/nó 0.0b da Cadência Inbound) — reativar sem telefone só queima mais 90 dias sem produzir nenhuma tentativa real, porque a operação é 100% telefone (`d52e61d`) e nenhuma régua automática deste workflow fala outro canal. Nada para limpar aqui: nenhuma tag de fila foi tocada ainda |
| 3 | Reset de rodada | Update Contact Field | `Tentativa nº` = 0 · `WA não atendidas seguidas` = 0 · `Resultado da tentativa` = vazio · `Prioridade` = 3 · `Entrada em` = `{{right_now.date}} {{right_now.time}}` (`{{right_now}}` puro grava `[object Object]` — medido em 22/09/2026, mesma correção já aplicada nas seções 2.3/2.10) · `1ª tentativa em` = vazio |
| 4 | Troca de origem | Remove Contact Tag `nutricao-90d` → Remove Contact Tag `cad-inbound` (idempotente, mesmo se ausente) → Add Contact Tag `cad-outbound` → Add Contact Tag `reengajamento-ativo` | Ver "A troca de origem" abaixo |
| 5 | Reentrada no funil | Update Opportunity — Etapa → `CONECTAR` **e** `status` → `open` | O reset explícito de `status` é achado desta migração: o desenho original não tinha campo `status` separado de etapa, então "mover para `Em cadência`" bastava. Hoje, sem zerar `status`, o lead chegaria a `CONECTAR` ainda com `status = abandoned` da rodada anterior, e o portão do Mestre de saída (seção 3, nó 1: "`CONECTAR` **e** `open`") ficaria falso — a chegada seria lida como saída, e a limpeza (tirar das filas, apagar tag de fila) rodaria no instante em que o lead está *entrando* de novo na cadência, não saindo. Com o reset, dispara o Mestre de saída em no-op de verdade (nó 1 encerra sem limpar) e o Alerta de Speed-to-lead (seção 2.11) com relógio novo, porque `1ª tentativa em` acabou de ser esvaziado no nó 3 — a reativação ganha sua própria medição de speed-to-lead de graça, sem campo novo |
| 6 | Guarda de janela de atendimento (seção 2.6.2, G-05) | If/Else nativo | Dentro da janela → 6b · Fora da janela → 6c |
| 6b | Mensagem de reabertura | Send WhatsApp | Texto livre `RE-1` (`biblioteca-mensagens.md`) → 6d |
| 6c | Mensagem de reabertura (fora da janela) | Send WhatsApp, modo Template | Template Meta `RE-1` (a submeter — `biblioteca-mensagens.md`) → 6d |
| 6d | Carimbo | Update Contact Field | `Template usado` = `RE-1` (os dois ramos acima convergem aqui) |
| 7 | Aguardar resposta | Wait → Contact Replied | Tempo limite 2h — mesmo padrão do pós-M1 (seção 2.6): se respondeu, `Stop on Response` tira da régua |

> **G-08, 22/09/2026 — o nó 2 reativaria para sempre um lead sem telefone
> válido, sem nunca produzir uma tentativa real.** Achado ao aprofundar o
> F-15 (seção 2.30): o texto daquela seção já tinha identificado o problema
> ("o nó 1 do R-08 precisa distinguir por que o lead virou `abandoned`") mas
> nunca virou mudança neste nó — ficou registrado e não aplicado, o mesmo
> padrão de "achado em rodapé nunca promovido" que este projeto já viveu
> antes (F-12, F-13). Reconferido por API nesta rodada, e a conta mudou: **a
> base tem 0 oportunidades `abandoned` agora** (53 oportunidades reais, 48
> `NOVO LEAD` + 2 `CONECTAR` `lost` + 2 `NEGOCIAR` `open` + 1 `NEGOCIAR`
> `lost`) — os 5 leads reais do Instagram sem telefone que o F-15 mediu
> continuam em `NOVO LEAD`, sem nenhum campo de cadência preenchido, porque
> ainda não foram promovidos para `CONECTAR` (G-03, aguardando o dono) e
> portanto nunca passaram pelo portão 0.0b que aplicaria `telefone-invalido`
> e `nutricao-90d`. **O ciclo ainda não é um estrago ativo hoje — é uma
> armadilha armada, não disparada:** no instante em que G-03 for decidido e
> esses leads (ou qualquer lead futuro sem telefone) entrarem em `CONECTAR`,
> o portão 0.0b (seções 2.3/2.10) os manda para `abandoned` + `nutricao-90d`
> depois de esgotar o que a cadência sem telefone conseguir tentar, e sem
> este nó 2 corrigido o Reengajamento 90 dias os reativaria de volta para
> `CONECTAR` a cada 90 dias, correndo o bloco TR1-TR4 (que hoje é só
> WhatsApp/telefone — a operação não fala mais WhatsApp desde `d52e61d`, e
> quem chegou sem telefone continua sem telefone) até voltar para
> `abandoned` + `nutricao-90d` de novo, reabrindo o relógio sozinho, sem
> fim. A tag `telefone-invalido` já existe (T-09, R-13) e já é aplicada por
> quem detecta a falta de telefone — o nó 2 só precisava lê-la antes de
> reativar, e agora lê. **Não é o mesmo problema do F-15** (que resolve quem
> tem e-mail, canal que os 5 do Instagram não têm) — é o problema mais
> barato de fechar: parar de agendar uma tentativa que a própria régua sabe
> de antemão que não vai acontecer. Zero campo, zero tag novos — reaproveita
> `telefone-invalido`, que já existe na base desde a R-13. Zero escrita no
> CRM nesta rodada: item de especificação pura, não depende de
> `APROVADO.md` (nenhuma tag ou campo novo nasce). **O que isto não
> resolve:** é correção de spec, não de dado — precisa ser aplicada como
> retoque no workflow `Reengajamento 90 dias`, já **publicado** na tela
> (`GUIA-MONTAGEM.md`, "Estado final em 22/09/2026"), o mesmo tipo de patch
> cirúrgico já usado para o relógio (`APRENDIZADOS-CRM.md`,
> `tools/patch_relogio_cadencias.py`) — não sai por este conector (sem
> endpoint de workflow) nem pela API interna desta sessão (sem bearer local).
> Detalhe completo: `ROADMAP-SALES-ENGAGEMENT.md`, G-08.

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
`REUNIÃO DE DIAGNÓSTICO` (antiga `AGENDAR`) ou mudando `status` para `abandoned`/`lost` sem sair de
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

`(Contagem de contatos com tag "fila-tel") − 100`

> Corrigido em 22/09/2026: a fórmula somava `fila-tel` **OU** `fila-wa`. Com a decisão de 100% telefone (seção 2.5) nada mais aplica `fila-wa`, e o termo a mais não é inofensivo — ele continua contando quem carrega a tag antiga por resíduo, inflando a fila e podendo disparar o alarme de capacidade sem fila nenhuma. Antes: ~~`OU "fila-wa"`~~.

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
| 2 | If/Else: etapa da oportunidade **é uma de** `NOVO LEAD`, `CONECTAR` **e** `status` **é** `open` → segue. Senão (já `REUNIÃO DE DIAGNÓSTICO` (antiga `AGENDAR`), `NEGOCIAR`, ou `status` já `abandoned`/`lost`) → só marca a tag e avisa (nó 4), sem mexer na etapa — um contato que já avançou por trabalho humano não retrocede por uma validação automática chegando atrasada |
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
| `Estouro da Fila` (já existe, R-11 — seção 2.15) | `(Contagem de contatos com tag "fila-tel") − 100` | Fila em atraso — capacidade |
| `Atrasos de Speed-to-lead` (nova) | `Contagem de contatos com tag "atraso-1a-tentativa"` | Fila em atraso — SLA da 1ª tentativa (a mesma tag que a lista 8.8 já filtra) |
| `Taxa de Conexão — Telefone` (nova) | `(Soma de "Conexões telefone" ÷ Soma de "Tentativas telefone") × 100` | Taxa por tentativa — telefone, acumulada |
| `Taxa de Conexão — WhatsApp` (nova) | `(Soma de "Conexões WhatsApp" ÷ Soma de "Tentativas WhatsApp") × 100` | Taxa por tentativa — WhatsApp, acumulada |
| `Taxa de Conexão Real — Telefone` (nova, F-06, peça 2) | `(Soma de "Conexões reais telefone" ÷ Soma de "Ligações com transcrição") × 100` | **Das chamadas que dá para medir**, quantas duraram mais de 60s — sem depender do julgamento do SDR. O denominador **não** é `Tentativas telefone`: os dois lados precisam da mesma população, ver "Conferência da peça 2" na seção 2.27 |
| `Leads novos hoje` (nova, F-10) | `Contagem de contatos com "Date Created" = hoje` | **Entrada do dia** — o único indicador que piora quando a operação para de receber lead, e o único que nenhum monitor do F-05 cobre. Zero às 12h já é sinal. Usa a contagem de contatos por filtro (achado 2 desta seção), que aqui é a unidade certa |
| `Leads novos — 7 dias` (nova, F-10) | `Contagem de contatos com "Date Created" nos últimos 7 dias` | Tendência de entrada: separa "dia fraco" de "parou". **Leia contra o maior intervalo já observado** (15h06 nesta base) e não contra um total de horas — hora absoluta não se calibra, e foi por isso que a abertura do F-10 publicou um número errado que "soava plausível". O tempo sem lead novo só sobe a cada rodada (última leitura em `ROADMAP-SALES-ENGAGEMENT.md`, F-10 — número fixo só lá, para não desatualizar aqui) e nenhum alerta existia para dizer isso |
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
2. ~~**Contact Tag Added** — `fila-wa`~~ — **removido em 22/09/2026.** Nada mais adiciona `fila-wa` (seção 2.5), então este gatilho nunca dispararia. Fica riscado porque a justificativa do OR logo abaixo foi escrita para dois gatilhos: com um só, o recurso de multi-gatilho deixa de ser **necessário aqui** — não deixa de existir, e não é a regra que mudou.

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

## 2.23 Monitor de Saúde da Operação — F-05 (peça 5 de 6: `REUNIÃO DE DIAGNÓSTICO` (antiga `AGENDAR`) sem fechar o loop) — F-05 fechado, **premissa superada em 23/09/2026 (G-13)**

> **Este desenho parou de poder acontecer.** A premissa do gatilho abaixo é
> que `REUNIÃO DE DIAGNÓSTICO` é alcançada por uma conexão (`Atendeu`) que
> ainda não fechou horário. Com a D3 do `PLANO-MULTICANAL.md` (23/09/2026),
> `Atendeu` deixou de mover a oportunidade — ela **só** entra em `REUNIÃO DE
> DIAGNÓSTICO` quando a reunião é marcada (`Pós-agendamento v2`, D4). Não há
> mais como estar nessa etapa **sem** reunião marcada, então o portão do nó 2
> (`etapa é REUNIÃO DE DIAGNÓSTICO E status é open`) nunca mais vê o caso que
> o alerta existia para pegar. O dono já tinha chegado à mesma conclusão por
> outro caminho e despublicado o workflow desta seção (`W17d`,
> `PLANO-MULTICANAL.md` E8, 23/09/2026) antes de qualquer documento registrar
> o motivo.
>
> **O que substitui esta peça, e o que ela não cobre.** `Fechar Horário`
> (`tools/build_fechar_horario.py`, publicado) monitora a fase nova —
> conectado, ainda em `CONECTAR`, tag `fechar-horario` — com um relógio de 3
> dias: dia 1 tarefa + mensagem automática `MFH1-v1`, dia 2 tarefa + `MFH2-v1`,
> dia 3 sem reunião → `abandoned` + `nutricao-90d`. Sai sozinho quando a
> reunião é marcada. **A diferença real com esta peça 5:** o novo workflow
> reengaja o lead por mensagem, mas **não avisa o gestor** em nenhum passo —
> o `Internal Notification` do nó 4 abaixo não tem equivalente em
> `Fechar Horário`. Se a visibilidade do gestor sobre "conectou e não fechou
> horário" ainda é necessária, é decisão de desenho nova (somar um aviso ao
> `Fechar Horário`, não ressuscitar esta peça — a etapa que ela vigiava não
> aceita mais o estado que ela procurava).
>
> **Consequência para T-19 (`agendar-estagnado`, `campos-e-tags.md`):**
> continua `[ ]` em `APROVADO.md`, nunca criada — e não deveria ser aprovada
> como está especificada aqui, porque o workflow que a aplicaria (nó 3 abaixo)
> foi despublicado. Detalhe completo, e o que fica em aberto, em
> `ROADMAP-SALES-ENGAGEMENT.md`, G-13. O texto abaixo fica como registro do
> desenho original — não é para montar.
>
> **Pronto quando:** decisão do dono sobre se `Fechar Horário` precisa de um
> aviso ao gestor equivalente ao nó 4 abaixo; se sim, especificar o nó novo
> nesta seção; se não, marcar esta peça como retirada (mesmo tratamento que a
> seção 2.32 já deu ao F-17) e considerar T-19 encerrada sem criação.

**Por quê (desenho original, 18/09/2026 — não monte, ver aviso acima):** a invariante que a "Adição de 18/09/2026" do roadmap
acrescentou ao F-05 original, ao aplicar o tempo de estagnação do Sales
Model Canvas etapa a etapa: `Conectado` (hoje `REUNIÃO DE DIAGNÓSTICO`, tabela 1.0) sem
avançar para `Reunião agendada` (`NEGOCIAR`) em mais de 24h — o SDR atendeu
o lead, ganhou a tarefa `[CONECTADO] Qualificar e agendar` (seção 4, ramo
`Atendeu`, nó 8), e nunca fechou o loop: não agendou, não descartou. É a
mesma classe de estrago silencioso das peças 1-3 (nada avisa sozinho), aqui
na etapa em que L-08 (`briefing-sdr.md`) já tinha achado que falta caminho
de saída para "sem fit" — este monitor não fecha essa lacuna sozinho (quem
fechou foi o ramo `Desqualificado` do Pós-ligação, R-18, 21/09/2026, que
tira a maioria dos "sem fit" **antes** de chegar aqui), só garante que quem
ainda assim ficar parado em `REUNIÃO DE DIAGNÓSTICO` (fit real, sem horário fechado, ou
desqualificado na mão já dentro da etapa) não fica sem ninguém saber.

Mesma pesquisa de mercado das peças 1-3: nenhuma das quatro plataformas do
enunciado do projeto (Reev, Meetime, Outreach, Salesloft) expõe alarme
proativo para "lead conectado sem próximo passo fechado" — é reporting de
engenharia interna, não recurso de sales engagement.

**Desenho:** mesmo padrão de relógio por evento já validado em R-02 e na
peça 1 (seção 2.20) — gatilho de chegada, `Wait` de 24h, portão que confere
se o lead ainda está preso antes de avisar. `REUNIÃO DE DIAGNÓSTICO` só é alcançada uma vez
por ciclo (o Pós-ligação, seção 4, ramo `Atendeu`, nó 6, é o único nó que
move uma oportunidade para lá), então não tem o risco de eventos repetidos
em menos de 24h que motivou o relógio ancorado por horário fixo da peça 2 —
o `Wait` relativo de 24h, o mesmo mecanismo da peça 1, basta.

### Gatilho
**Opportunity Stage Changed** — Pipeline `FUNIL DE VENDAS` · Para a etapa:
`REUNIÃO DE DIAGNÓSTICO`

### Configurações
| Configuração | Valor | Por que |
|---|---|---|
| Allow Re-entry | **Ligado** | Cada entrada em `REUNIÃO DE DIAGNÓSTICO` merece seu próprio relógio, mesmo raciocínio da peça 1 |
| Janela de envio | Sem janela, 24/7 | Aviso interno ao gestor, não mensagem ao lead |
| Stop on Response | Desligado | Não há mensagem ao lead aqui |

### Nós
| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Aguardar | Wait → Time Delay | 24 horas corridas |
| 2 | Portão | If/Else | Etapa da oportunidade **ainda é** `REUNIÃO DE DIAGNÓSTICO` **E** `status` **é** `open` → segue (24h depois de atender, ninguém fechou o loop). Senão → **encerra** (agendou, foi descartado na mão, ou saiu por outro caminho — nada a avisar) |
| 3 | Fila | Add Contact Tag | `agendar-estagnado` |
| 4 | Aviso | Internal Notification | Para o gestor: `{{contact.name}} atendeu e está há mais de 24h em REUNIÃO DE DIAGNÓSTICO sem reunião marcada nem desqualificação. Conectado em: {{contact.data_conectado}}.` |
| 5 | Registro | Add Note | `Alerta de saúde: REUNIÃO DE DIAGNÓSTICO sem fechar o loop em 24h · {{right_now}}` |

**Limpeza da tag — por que entra no nó 0 do Mestre de saída (incondicional),
não só na lista nomeada do nó 4 (achado ao desenhar):** o caminho normal de
saída de `REUNIÃO DE DIAGNÓSTICO` (o Pós-agendamento move para `NEGOCIAR`, seção 5, nó 1)
já aciona o nó 4 do Mestre de saída pela via comum — `NEGOCIAR` não está na
lista de no-op do nó 1 ("`status` é `open` **e** etapa é uma de `NOVO LEAD`,
`CONECTAR`"), então bastaria somar a tag à lista existente, como
`fila-travada` e `conectar-estagnado` já fazem. Mas L-08 (`briefing-sdr.md`)
registra que hoje não existe caminho formal de desqualificação a partir de
`REUNIÃO DE DIAGNÓSTICO` — se algum dia alguém arrastar a oportunidade de volta para
`CONECTAR` na mão (o único jeito manual de "desistir" sem esse caminho), a
condição do nó 1 volta a ser verdadeira (`CONECTAR`/`open`) e o Mestre de
saída trataria essa transição como no-op, a mesma classe de bug que já
motivou o nó 0 incondicional para `novo-lead-estagnado` (seção 2.20).
Somar `agendar-estagnado` ao nó 0 (em vez de só ao nó 4) cobre os dois
caminhos de uma vez, sem custo: `Remove Contact Tag` de quem não tem a tag
não faz nada, e o Mestre de saída já roda a cada mudança de etapa ou status.

**Pronto quando (peça 5 do F-05):** um lead atendido que fica mais de 24h em
`REUNIÃO DE DIAGNÓSTICO` sem virar reunião marcada nem sair por outro caminho gera aviso ao
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
de detecção), `REUNIÃO DE DIAGNÓSTICO` (antiga `AGENDAR`) sem fechar o loop em 24h (peça 5) e retorno vencido
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
| **Seguir a rampa de aquecimento por semana** (seção 2.29/F-14) em vez de partir direto para 100/dia — o número desta operação nunca discou de verdade (zero registro de chamada, `APRENDIZADOS-CRM.md`), então é "novo" para efeito de reputação mesmo já existindo na subconta | "Distribuir entre números" (linha acima) não diz quanto por dia em qual semana; a rampa escreve o teto que falta |
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

### Terceiro caminho pesquisado e descartado, 23/09/2026 — Presença Local (DDD): recurso nativo é US/Canada only, mas o equivalente manual já dá para fazer hoje, de graça

Pesquisado seguindo o mesmo mandato do roadmap (checar o que Reev, Meetime,
Outreach e Salesloft fazem antes de desenhar): as quatro plataformas de
outbound americanas tratam **Local Presence Dialing** — mostrar ao lead um
número com o mesmo DDD/área dele, prática documentada por aumentar taxa de
atendimento — como recurso central (Outreach, Salesloft, Kixie, Aircall
têm isso nativo). Vale checar se o HighLevel tem o mesmo antes de propor
algo próprio.

**Tem, nativo — e não serve para este número.** `WebSearch` confirma:
`Local Presence Dialing` do HighLevel escolhe automaticamente, a cada
ligação de saída, o número da própria subconta com o DDD mais próximo do
contato (hierarquia: DDD exato → região → padrão), configurado em
`Settings → Phone Numbers → Voice → Other Settings → Outbound Call →
Default Phone Number for Outbound Calls`. A própria documentação de
suporte da HighLevel e cobertura de terceiros convergem: **suportado só
para números dos EUA e Canadá** — não compra número novo sozinho (exige já
possuir números nos DDDs alvo) e não há confirmação de expansão para
número brasileiro. Mesmo formato de descarte do Voice Integrity (item 1
acima): recurso real, documentado, e **US only** — não copiar a receita
americana sem checar a letra miúda de novo.

**O que não é US only, e resolve a mesma fatia do problema sem automação:**
o **Web App Softphone** do HighLevel deixa o usuário escolher manualmente,
num dropdown "Calling From", qual dos números da subconta usar antes de
discar — recurso confirmado por documentação de suporte e por terceiros,
sem restrição de país citada em lugar nenhum. **Não precisa de item de
roadmap próprio nem de nó novo:** é a mesma tabela deste F-08 já em vigor
— "distribuir as ligações entre mais de um número" (linha 2 da tabela
acima) já manda comprar mais de um número antes de escalar volume; o único
acréscimo é **qual** número escolher no dropdown a cada ligação — o de DDD
igual ou mais próximo do lead, quando a subconta tiver mais de um. Zero
custo adicional (mesmos números que o F-08 já recomenda comprar por
reputação), zero engenharia (escolha manual, sem workflow): é rotina de
SDR, não configuração de tela — acrescentada em `GUIA-SDR.md`.

**Por que isto é o tipo de vantagem que a instrução deste roadmap pede**
("escolha o que um concorrente não consegue copiar olhando a tela de
fora"): qualquer concorrente que abra esta subconta vê os mesmos números
comprados por reputação (F-08) — não vê a disciplina de **qual** número o
SDR escolhe em cada ligação, porque isso não é configuração, é hábito
registrado só aqui e no guia do SDR.

**Confiança das fontes:** média — os mesmos domínios oficiais
(`help.gohighlevel.com`) seguem bloqueados pelo proxy deste ambiente
(`EGRESS_BLOCKED`, mesma limitação já registrada acima); a descrição do
comportamento (hierarquia DDD → região → padrão, caminho de configuração,
restrição US/Canada, dropdown "Calling From" no softphone) apareceu
convergente em busca por ângulos diferentes, sem fonte única. Não muda o
"Pronto quando" do F-08 (já cumprido) — é acréscimo à mesma tabela, não
item novo.

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

> **Publicado em 23/09/2026 com um desenho diferente do especificado
> abaixo — o texto original fica como registro do raciocínio, não como
> retrato do que está no ar.** O dono construiu e testou os dois alertas
> pelo próprio caminho (`tools/build_estagnacao.py`, `PLANO-MULTICANAL.md`
> item A5, ids `53334baa`/`14fdf9fa`) antes de qualquer sessão cruzar
> `GUIA-CLOSER.md` contra este documento (G-23, `ROADMAP-SALES-
> ENGAGEMENT.md`). Três diferenças do real para o desenho abaixo:
>
> 1. **`Negociação Estagnada` usa 5 dias, não 3** — o dono ajustou o prazo
>    na hora de montar.
> 2. **O gatilho real é `Opportunity Stage Changed → NEGOCIAR`**, não
>    `Contact Changed` em `Reunião foi qualificada` — dispara na entrada em
>    `NEGOCIAR`, não na resposta do closer.
> 3. **Existe um segundo workflow, "Proposta Pendente"** (tag
>    `proposta-pendente`, T-22 em `campos-e-tags.md`), cobrindo exatamente o
>    buraco que o nó 3 abaixo deixava: closer marca `Sim` e nunca move a
>    oportunidade para `NEGOCIAR`. Gatilho `Contact Changed` em `Reunião foi
>    qualificada`, 3 dias, condiciona pela tag `etapa-reuniao` (Espelho de
>    Etapa) em vez de ler a etapa da oportunidade direto — mesmo motivo já
>    registrado no G-08 (condição `Pipeline stage is …` lê vazio num
>    workflow cujo gatilho não é de oportunidade).
>
> Fonte primária: `wesales/tools/build_estagnacao.py` (no repo, lido nó a
> nó) — mais confiável que reconstruir de memória. Detalhe completo,
> inclusive o que isso muda em `campos-e-tags.md`/`APROVADO.md`/
> `IMPLEMENTACAO-WORKFLOWS.md`, em G-23.

**Por quê (desenho original, 22/09/2026 — mantido como registro do
raciocínio que levou ao alerta; ver publicado real acima):** achado ao
conferir a Etapa 3 (`NEGOCIAR`) deste documento, seção
1.1 acima — a linha "Tempo de estagnação" registrava, desde antes de F-05
existir, que a metade "comparecimento" tem monitor (R-12, SLA do closer) mas
a metade "negociação" não. F-05 fechou em 21/09/2026 com seis peças
(`NOVO LEAD`, `fila-tel`/`fila-wa`, `CONECTAR`, `nao-perturbe` em workflow
ativo, `REUNIÃO DE DIAGNÓSTICO` (antiga `AGENDAR`), retorno vencido) e nunca chegou a incorporar esta — o
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
**Cumprido, pelo desenho publicado (5 dias, `Opportunity Stage Changed`),
não pelo desenho acima — ver o aviso no topo desta seção.**

**Pronto quando (G-23):** uma reunião qualificada pelo closer (`Sim`) que
passa 3 dias em `REUNIÃO DE DIAGNÓSTICO`/`open` sem ser movida para
`NEGOCIAR` também gera aviso ao gestor sozinho. **Já cumprido** pelo
workflow "Proposta Pendente" (tag `proposta-pendente`), publicado no mesmo
pacote da T-21 — o buraco que motivou G-23 já estava fechado antes de a
sessão que abriu o item saber disso; o trabalho de G-23 foi achar e
documentar, não desenhar.

---

## 2.29 Rampa de aquecimento do número de telefone — F-14

> **Decidido por ação em 23/09 (commit `9020079`), e a decisão foi a que concentra
> a segunda.** O dono aplicou a janela seg-sex em 4 workflows de tarefa
> (`Pós-ligação v2`, as duas `Interceptação de Sinal` e o `Monitor de
> Capacidade`) **mantendo a régua em dias corridos** — ou seja, a combinação
> exata cuja aritmética está medida abaixo: em regime, a segunda carrega ~3/7 da
> semana em vez de 1/5, e com o lote conservador de 6/dia bate 120 ligações
> contra a meta de 100/dia.
>
> No mesmo commit veio o `Monitor de Capacidade` (publicado), e ele é **1 nó,
> `internal_notification`** — avisa o gestor. ⚠️ **Eu usei isso para dizer que a
> regra de capacidade não é aplicada, e estava errado** (correção na §2.33.6): o
> Monitor nunca foi o ponto de aplicação. Quem aplica é a `faxina_tarefas.py`
> (linhas 197-213), que liga a tag `sdr-lotado` por SDR, e a `Cadência 12x30`
> parte 1 e parte 2, que têm **6 nós cada** condicionando nessa tag — o laço de
> espera de 1 h. A capacidade **é** represada na 12x30. O que **não** tem portão é
> a `Cadência Inbound` (0 nós), que é por onde os leads entram hoje — e esse é o
> achado de verdade, na §2.33.6.
>
> Então a aritmética abaixo continua valendo inteira, e a pergunta que sobra não
> é mais "dias úteis ou corridos" — é **se o lote de entrada vai ser calibrado
> pela segunda-feira em vez de pela média**. Com lote 6/dia a segunda já passa da
> capacidade; com 12/dia são 240. Nada disso está acontecendo hoje: zero lead em
> cadência.

> **Conta nova de 23/09/2026 — a regra D13 ("nenhuma tarefa nasce no fim de
> semana") concentra a segunda-feira em +82%, e é a segunda que vira o teto.**
>
> A regra está certa e o comportamento também: a janela seg–sex **segura** a
> tarefa até a janela abrir, não a descarta. O efeito colateral é de
> distribuição, não de perda — e é exatamente o tipo de coisa que só aparece
> multiplicando.
>
> Modelo: entrada de lote todo dia útil, régua de 12 toques nos dias corridos
> D1·D1·D2·D2·D4·D7·D7·D10·D14·D20·D30·D30, todo toque que cai em sábado ou
> domingo adiado para a segunda seguinte. Regime (janelas já sobrepostas):
>
> | Lote/dia útil | Terça a sexta | **Segunda** | Pico sem a regra |
> |---|---|---|---|
> | **6** | 48 a 66 | **120** | 66 |
> | **12** | 96 a 132 | **240** | 132 |
>
> Some 360 toques/semana nos dois casos (6 × 5 × 12), então **o total não
> muda** — muda quem carrega. A segunda absorve os dois dias parados e fica
> com ~3/7 do volume da semana em vez de 1/5.
>
> **Por que isso decide o lote:** a meta de capacidade do SDR é **100
> ligações/dia** (`briefing-sdr.md`, e a própria D14 do plano do dono
> repete). Com o lote conservador de 6/dia, **a segunda já bate 120** — 20%
> acima da capacidade, em regime, sem nenhum imprevisto. O lote de 12/dia põe
> 240 numa segunda, que é 2,4× a capacidade.
>
> **Estado, para não confundir armadilha com incêndio:** isto é aritmética
> sobre parâmetros declarados, não medição do sistema rodando — hoje há **zero
> lead em cadência**, então nada disso está acontecendo. É conta de projeto, e
> por isso dá para consertar antes de doer.
>
> **Quatro saídas, em ordem de elegância:**
>
> | Saída | O que muda | Custo |
> |---|---|---|
> | **Régua em dias úteis** em vez de dias corridos (D1, D2, D4… contados em dia útil) | nenhum toque cai em fim de semana, por construção | a régua de 30 dias vira ~42 dias corridos |
> | **Espalhar o represado** entre segunda e terça | segunda cai para ~93 | um nó a mais decidindo o destino |
> | **Adiar para sexta** em vez de segunda (antecipar) | sexta sobe de 48 para ~102, segunda fica em 42 | toque chega antes, não depois |
> | **Baixar o lote** | segunda proporcional | mais tempo para escoar o estoque |
>
> A primeira é a que as plataformas de sales engagement usam, e some com o
> problema em vez de administrá-lo.
> **Conferido em 22/09/2026, 23:35 UTC — a proposta multicanal (caminho B)
> não alivia esta rampa, e é fácil supor que alivia.**
>
> Os textos de WhatsApp/e-mail do caminho B (`biblioteca-mensagens.md`) são
> **aditivos**, não substitutivos: MT1 diz "acabei de tentar te ligar", MT4 diz
> "tentei te ligar de novo agora", MT11 diz "última tentativa de te pegar por
> telefone". Cada mensagem acompanha um toque de telefone que continua
> existindo. **Os 12 toques de telefone continuam 12.**
>
> Então a conta desta seção **não muda**: lote de ~12/dia continua levando o
> pico a 58 ligações/dia, 2,3× o teto da semana 1; lote de ~6/dia continua
> sendo o que cabe.
>
> **O efeito de segunda ordem existe, mas no lugar errado para ajudar aqui.**
> Mais canais aumentam a chance de conexão por lead, e lead que responde sai
> da régua — menos discagem ao longo dos 30 dias. Só que a rampa não é
> limitada pelo **total**, é limitada pelo **pico**, e o pico acontece nos
> dias 1 e 2, quando ninguém ainda teve tempo de responder e todo mundo segue
> na régua. Multicanal ajuda a cauda, não o pico.
>
> Dito de outro jeito: se alguém adotar o caminho B esperando que ele resolva
> o conflito F-14 × G-03, vai descobrir no dia 2 que não resolveu.
> **Conferência de 22/09/2026, 16:30 UTC — a rampa foi calibrada para uma
> régua que não existe mais, e o lote do G-03 passou a estourá-la.**
>
> O F-14 (`93ad877`) foi escrito antes de a sessão incorporar a decisão de
> 100% telefone (`d52e61d`). Ele diz, com todas as letras, que o telefone
> carrega "**8 de 12**" toques. Não carrega mais: carrega **12 de 12**. Os
> toques por dia de régua dobraram exatamente onde a rampa é mais apertada —
> D1 passou de 1 para 2 ligações, D2 de 1 para 2, D7 de 1 para 2.
>
> | Dia de régua | D1 | D2 | D4 | D7 | D10 | D14 | D20 | D30 |
> |---|---|---|---|---|---|---|---|---|
> | Ligações — régua alternada | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 1 |
> | Ligações — 100% telefone | **2** | **2** | **1** | **2** | 1 | **1** | 1 | **2** |
>
> **O efeito sobre o plano do G-03** (47 leads parados, lotes de ~12/dia por
> 4 dias, que é o plano real e finito — não um lote por dia para sempre):
>
> | Dia | Ligações na régua alternada | Ligações hoje | Teto da semana 1 |
> |---|---|---|---|
> | 1 | 12 | 24 | ~20-25 |
> | 2 | 24 | **48** | ~20-25 — estoura |
> | 3 | 24 | **48** | ~20-25 — estoura |
> | 4 | 23 | **58** | ~20-25 — estoura |
> | 5 | 11 | **34** | ~20-25 — estoura |
>
> Com a régua alternada, a rampa do F-14 e o lote do G-03 **cabiam um no
> outro** — 12, 24, 24, 23, 11 encosta no teto e não passa. Com o telefone
> sozinho, o pico vai a 58, **2,3× o teto da própria semana 1**, e no dia 2,
> não no fim da rampa. Nenhum dos dois itens está errado isolado: eles foram
> escritos com meio dia de diferença e a decisão de canal passou entre os
> dois.
>
> **Isto é decisão do dono, não conserto automático**, porque os dois lados
> são metas dele: o lote de 10-13/dia veio do Quality Rating do WhatsApp
> (F-07), e o teto da semana 1 veio da faixa de aquecimento do mercado. As
> saídas que a aritmética permite:
>
> | Saída | O que custa |
> |---|---|
> | **Lote de ~6/dia** em vez de 10-13 | devolve a curva exata da coluna "régua alternada" acima. O estoque de 47 leva ~8 dias em vez de 4 |
> | Manter 10-13 e **aceitar a semana 1 em ~50/dia** | é a faixa "agressiva" que as fontes citam (75-150/dia), não fora do mundo — mas joga fora a margem que a rampa existia para ter, num número que nunca discou |
> | Segurar a fila quando bater o teto | já está no checklist do gestor abaixo; a diferença é que agora isso vai acontecer **todo dia da semana 1**, não como exceção |
>
> A tabela de tetos por semana mais abaixo **continua válida** — ela vem das
> fontes de mercado, não da régua. O que venceu foi a coluna "como se atinge
> com os lotes do G-03", e a frase de que "10-13 ligações no dia 1 já está
> dentro da faixa conservadora": no dia 1 agora são 24.
**Por quê:** o F-08 (seção 2.26) protegeu a reputação do número de telefone
com um checklist — cadastro no "Qual Empresa Me Ligou?", `Origem Verificada`,
vigiar queda de atendimento — mas o único item sobre **volume** ficou como
"distribuir entre mais de um número **antes de escalar**", sem nunca escrever
quanto por dia em qual semana. É a mesma lacuna que o F-07 já tinha fechado
para o WhatsApp com um objeto próprio: número novo nasce **Tier 1** (250
contatos únicos), só sobe "consumindo metade do teto atual dentro de 7 dias
com qualidade aceitável" (seção 2.25). O telefone nunca ganhou o equivalente,
apesar de carregar o dobro dos toques (8 de 12, contra 4 de 12 do WhatsApp) e
de já estar, pela própria conta do F-08, **acima** da referência internacional
de segurança (50-75/dia) na meta de regime (100/dia).

**E o canal está, hoje, tecnicamente "novo" mesmo sem ser recente na
subconta:** `APRENDIZADOS-CRM.md` ("O CRM não pode responder a pergunta do
LC Phone") mediu **zero registro de chamada** nas 50 conversas da subconta —
nenhuma tocou ainda. Para efeito de reputação de operadora, um número que
nunca discou e um número criado ontem são a mesma coisa: sem histórico de uso
legítimo, o primeiro dia de volume alto é o que os provedores de identificação
de chamada usam para decidir se marcam "Spam Likely". `WebSearch` (Kixie,
Tendril, PhoneBurner, Salesloft, Aircall, SalesHive — convergência de fontes
de mercado independentes, nenhuma vendendo o mesmo produto): o padrão do
setor é aquecer **2 semanas antes de qualquer campanha de volume**, com teto
diário explícito por número no início (as fontes variam entre 20-50/dia numa
janela conservadora e 75-150/dia numa mais agressiva, sempre **crescente**, e
nunca a meta plena no primeiro dia) — e o mesmo veredito do F-08 aparece nas
fontes de mercado sobre o produto americano equivalente: o "Voice Integrity"
do **Outreach** também é descrito como valendo só para número comprado nos
EUA, o mesmo limite que já descartou o "Voice Integrity" da HighLevel — sinal
de que a plataforma de origem não é o motivo do limite, é o próprio recurso.

**A conexão que faltava, e que é o motivo deste item não ser genérico:** o
G-03 (Bloco 0) já decidiu, no cruzamento com o F-07, promover o estoque de 47
leads parados em **lotes de 10-13/dia** — mas só para proteger o Quality
Rating do WhatsApp. Nenhuma das três opções do G-03 nem aquele cruzamento
menciona telefone. Só que o mesmo lote que protege o WhatsApp também é,
por construção, quem determina o volume de telefone do primeiro dia (cada
lead promovido gera uma tentativa de telefone em D1, tabela 2.5) — a notícia
boa é que 10-13 ligações no dia 1 já está dentro da faixa conservadora de
aquecimento; a notícia que falta escrever é que isso só vale enquanto os
lotes não se **empilham**: a partir da segunda semana, cada dia soma o lote
novo às reentradas D2/D4/D7 dos lotes anteriores (tabela 2.5), e sem um teto
explícito o volume cresce mais rápido que a rampa do setor recomenda —
exatamente o tipo de "queima silenciosa" que o F-07 já preveniu para o
WhatsApp e que aqui não tinha nenhum guarda-corpo escrito.

**Como:** rampa de referência, calibrada com os dois lados (a faixa do
mercado e o teto de regime já decidido de 100/dia por número, `briefing-sdr.md`):

| Semana | Teto de ligações/dia (por número) | Como se atinge com os lotes do G-03 |
|---|---|---|
| 1 | ~20-25 | 1 lote/dia (10-13 leads × ~1-2 toques de telefone/dia no início da régua) |
| 2 | ~40-50 | lotes seguem entrando, e as reentradas D2/D4/D7 do lote 1 já somam — é aqui que o teto pode estourar sem aviso |
| 3 | ~75 | ainda abaixo da meta de regime |
| 4+ | 100 (meta de regime, `briefing-sdr.md`) | volume pleno, só depois do número ter 3 semanas de uso real |

Sem gatilho nativo para ler "quantas ligações este número já fez hoje" (mesmo
limite de plataforma do F-06/F-07/F-08 — nenhum objeto do GHL soma tentativa
por dia por número, só `Tentativas telefone`, que é cumulativo desde sempre e
por contato, não por dia nem por número) — vira checklist do gestor, mesmo
tratamento do F-07/F-08, não um nó novo:

| Ação | Por quê |
|---|---|
| Nas primeiras 3 semanas após o primeiro dia de ligação real, conferir o teto da tabela acima **antes** de liberar o lote seguinte do G-03 | O lote controla quem entra; só o gestor sabe, olhando a fila do dia (`fila-tel`), se o total já bateu o teto da semana |
| Se o teto for atingido antes do fim do dia, **segurar** o restante da fila `fila-tel` para o dia seguinte em vez de discar tudo | É a mesma folga que a cadência já assume em outros pontos (Wait Dynamic do F-05, janela de 24h do G-05) — atrasar um dia custa menos que queimar o número |
| Se a operação escalar para 2º número antes da rampa terminar (R-10, novo SDR) | O número novo começa a própria rampa do zero — a experiência do primeiro número não "empresta" reputação para o segundo |
| Vigiar queda abrupta de atendimento (mesmo sintoma do F-08) com atenção redobrada nas 3 primeiras semanas | É a janela em que o número está mais vulnerável a rótulo, pela própria natureza da rampa |

**Por que não é um workflow, mesmo motivo do F-07/F-08:** a pergunta que o
gatilho precisaria responder — "quantas ligações este número específico já
discou hoje" — não existe como evento nem como contador nativo no GHL, e
`Tentativas telefone` (C-09) mistura os dois números do dia que a operação
tiver, além de nunca zerar por dia. Inventar esse contador exigiria um campo
novo por número e um reset diário, engenharia desproporcional ao problema
quando a operação ainda tem **um** número e o gestor já olha a fila todo dia
(mesma folga que o F-10 aceitou não ter alarme automático de ausência de
lead, por proporção parecida de custo × benefício).

**Pendência que este item não resolve, e por quê:** a mesma de sempre —
confirmar se as ligações saem por LC Phone ou linha própria do SDR muda quem
executa o cadastro do F-08, mas não muda a rampa em si: os provedores de
identificação de chamada (que decidem "Spam Likely") observam o número que
discou, não o sistema que o discou.

**Zero campo, zero tag, zero workflow, zero escrita no CRM:** item de
documentação e rotina manual pura, mesmo tratamento do F-07/F-08 — não
depende de `APROVADO.md`, não entra na "Ordem de montagem" nem no checklist
de teste da seção 10 (não há objeto de CRM para simular volume de discagem
com contato fictício).

**Pronto quando:** a rampa de 4 semanas está escrita com teto por semana; o
checklist do F-08 (seção 2.26) referencia esta seção; e o G-03
(`ROADMAP-SALES-ENGAGEMENT.md`) ganha uma nota dizendo que o mesmo cuidado de
lote que protege o WhatsApp (cruzamento com o F-07) também é, por
construção, quem paga a rampa de telefone — e que isso só segura até os
lotes começarem a se empilhar na segunda semana.

---

## 2.30 Resgate por E-mail — Sem Telefone (F-15)

> **Medido em 22/09/2026, 21:25 UTC — o ciclo é real, e o e-mail não o fecha.**
>
> Conferi o payload publicado e o ciclo existe exatamente como descrito: nó 3
> da `Cadência 12x30` (`contact_detail / phone / has_no_value`) → nó 10
> (`status = abandoned`) → nó 11 (tag `nutricao-90d`); e o nó 1 do
> `Reengajamento 90 dias` recicla em `opportunities / status == abandoned`.
> Quem não tem telefone volta, bate no mesmo portão e volta ao mesmo lugar.
> **O diagnóstico está certo.**
>
> **A solução é que não alcança ninguém.** O "78% da base tem e-mail" é
> verdade sobre a base **inteira** — e a base inteira tem telefone. Cruzando
> as duas populações, contato por contato:
>
> | | |
> |---|---|
> | Contatos sem telefone | 9 |
> | Desses, **com** e-mail | **1** — e é `<test lead: dummy data…>`, lead de teste do Meta |
> | Desses, **sem** e-mail | **8** |
> | Leads reais do Instagram sem telefone **e** sem e-mail | **5** |
>
> O `F-15` resgataria **zero lead real**. E não é azar: é estrutural. O
> formulário do Meta coleta telefone **e** e-mail juntos, então quem veio por
> ali tem os dois; quem não tem telefone veio por **DM de Instagram**, que não
> coleta nenhum dos dois. As duas populações são quase disjuntas por
> construção do canal de origem.
>
> **O que fica valendo, separado em duas coisas que estavam juntas:**
>
> 1. **Fechar o ciclo** continua necessário e não depende de e-mail. O nó 1 do
>    R-08 precisa distinguir **por que** o lead virou `abandoned`: se foi o
>    portão de telefone (tag `telefone-invalido`, aplicada no nó 6 da 12x30),
>    reciclar não produz tentativa — é só queimar 90 dias e repetir. Portão
>    novo no R-08, antes de reativar: `telefone-invalido` **presente** →
>    encerra sem reciclar, pela saída limpa do nó 3b.
> 2. **E-mail continua uma boa ideia — para outro público.** Os 39 contatos
>    **com** e-mail são justamente os que têm telefone: ali o e-mail é canal
>    **adicional** (toque barato que não consome o teto da rampa F-14), não
>    resgate. Vale manter `EM-1`/`EM-2`, mudando o público-alvo declarado.
> 3. **Quem realmente precisa de rota são os 5 do Instagram**, e o único canal
>    que os alcança é o **DM do Instagram** — conectado e vivo na subconta
>    (página `O Próximo Cliente`). Isso é decisão de operação (quem responde e
>    em quanto tempo), não workflow de e-mail.

**Por quê:** o portão 0.0/0.0b (seções 2.3 e 2.10) manda quem não tem
telefone, mas tem `Site` ou `Instagram` preenchido, para `status = abandoned`
+ tag `nutricao-90d` — a mesma saída branda que qualquer lead com telefone
recebe depois de 12 tentativas esgotadas. A diferença é que o Reengajamento
90 dias (R-08, seção 2.12) reativa **todos** eles de volta para `CONECTAR`
sem distinguir os dois casos — e um lead sem telefone bate no mesmo portão
0.0/0.0b de novo, sem telefone ainda, e volta para `abandoned`+`nutricao-90d`
no mesmo instante. O resultado, medido em `ESTADO-E-PLANO.md` (22/09/2026):
**9 dos 50 contatos reais não têm telefone**, e numa operação 100% telefone
(decisão registrada no topo deste roadmap) eles reciclam de 90 em 90 dias
para sempre sem jamais receber uma tentativa de contato de verdade — nenhuma
ligação (não têm número), nenhuma mensagem (`grep -c "Send Email"
build-wesales.md` = 0, nenhuma régua deste projeto usa e-mail). Não é o
mesmo problema do G-03 (ninguém entra na régua): aqui o lead entra, é
avaliado e sai decidido, ciclicamente, sem nunca ser procurado. `E-mail`
está preenchido em 39 dos 50 contatos (78%, `ESTADO-E-PLANO.md`, seção 2) —
o canal existe, nunca foi usado, e é o único dos três (telefone, WhatsApp,
e-mail) que não disputa a rampa de aquecimento do F-14 nem a janela de 24h
do G-05/G-06 (e-mail transacional do GHL não tem essa restrição de
WhatsApp Business API).

**Pesquisado antes de desenhar** (`WebSearch`, sem acesso a
`help.gohighlevel.com`, bloqueado pelo proxy deste ambiente — mesma
limitação já registrada no G-05): a literatura de sales engagement
(Zendesk, Highspot, Salesforce) converge que cadência multicanal supera
cadência de canal único, e cita ganho de resposta ao somar e-mail a uma
régua de ligação; nenhuma das quatro plataformas do enunciado (Reev,
Meetime, Outreach, Salesloft) documenta publicamente uma rota de resgate
automática **especificamente** para o subconjunto "sem telefone" de uma
cadência phone-first — o que existe na literatura é o **breakup e-mail**
genérico (`myphoner.com`): mensagem de encerramento sem pressão, medida em
30–40% de reabertura de negócios "mortos" em alguns contextos. O nó 5
abaixo usa esse padrão. `WebSearch` também confirma (confiança média, via
página de suporte oficial citada por terceiros, não acessada direto) que o
gatilho nativo **Customer Replied** do GHL aceita restringir por canal,
incluindo e-mail — a mesma capacidade que a seção 2.12 (R-08) já usa para
WhatsApp via `Wait → Contact Replied`; **não confirmado na tela** se o nó
`Wait` (em vez do gatilho de workflow) aceita o mesmo filtro de canal —
registrar ao montar.

**Por que não é dentro do R-08:** o nó 6 do Reengajamento 90 dias (guarda
de janela de WhatsApp, G-05) já ramifica por canal, mas as duas saídas são
WhatsApp (livre ou Template) — não há onde encaixar "manda e-mail em vez
disso" sem reescrever a régua toda para quem tem telefone também. Um
workflow pequeno e separado, do mesmo jeito que a Cadência Inbound (seção
2.10) e o Reengajamento (seção 2.12) já são workflows próprios em vez de um
`If` dentro da 12x30, resolve sem tocar em nada que já funciona.

**Campo novo:** nenhum — reaproveita `Phone`, `Email` (nativos) e `Template
usado` (C-23, já existente, `campos-e-tags.md`). **Tag nova:** nenhuma —
reaproveita `nutricao-90d` e `nao-perturbe`. **Zero escrita no CRM nesta
rodada:** item de especificação pura.

### Workflow novo — "Resgate por E-mail — Sem Telefone"

| Configuração | Valor | Por quê |
|---|---|---|
| Gatilho | `Contact Tag Added` — Tag: `nutricao-90d` | Mesmo gatilho do R-08 (seção 2.12) — os dois workflows rodam em paralelo, cada um cuidando do canal que sabe atender |
| Allow Re-entry | **Ligado** | Toda reaplicação de `nutricao-90d` (inclusive a cada ciclo de 90 dias que o R-08 reabre e fecha de novo para quem segue sem telefone) é uma rodada nova e legítima — mesmo raciocínio do R-08 |
| Janela de envio | 08:30 às 18:30, segunda a sexta, fuso da subconta | Mesma cortesia usada em toda mensagem ao lead deste projeto — e-mail não tem a restrição de API do WhatsApp (G-05), mas não é motivo para mandar de madrugada |
| Stop on Response | Ligado | Respondeu por e-mail em qualquer ponto da régua, sai — mesmo padrão do R-08 |

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Portão de elegibilidade | If/Else — condições **E** | Status da oportunidade **é** `abandoned` · `Phone` vazio · `Email` preenchido · tag `nao-perturbe` ausente |
| 1b | Ramo falso | **Remove from Workflow: este** | A maioria de quem ganha `nutricao-90d` tem telefone (12 tentativas esgotadas, nota baixa, timing errado, no-show — grep confirma 6 origens diferentes da tag) — esses o R-08 já atende sozinho por telefone/WhatsApp. Este workflow existe só para o subconjunto sem telefone nenhum (nó 0.0b) |
| 2 | 1º resgate | Send Email — Template `EM-1` | Texto em `biblioteca-mensagens.md` |
| 3 | Carimbo | Update Contact Field | `Template usado` = `EM-1` |
| 4 | Aguardar resposta | Wait → Contact Replied — canal E-mail (a confirmar na tela, ver pesquisa acima) | Tempo limite 5 dias corridos |
| 4b | Ramo respondeu | Internal Notification para o gestor: `{{contact.name}} respondeu ao resgate por e-mail (sem telefone) — pedir telefone/WhatsApp ou seguir por e-mail/Instagram, decisão manual` → **Remove from Workflow: este** | O lead voltou a dar sinal; não há régua automática pronta para um canal que a operação nunca usou, decisão fica com o SDR |
| 5 | 2º resgate ("breakup") | Send Email — Template `EM-2` | Só se o nó 4 não recebeu resposta no prazo |
| 6 | Carimbo | Update Contact Field | `Template usado` = `EM-2` |
| 7 | Aguardar resposta | Wait → Contact Replied — canal E-mail | Tempo limite 5 dias corridos |
| 7b | Ramo respondeu | Internal Notification (mesmo texto do nó 4b) → **Remove from Workflow: este** | |
| 8 | Fim natural | — | Sem resposta em nenhum dos dois e-mails, o contato segue `abandoned`+`nutricao-90d` exatamente como hoje — o R-08 recicla em 90 dias e este workflow dispara de novo nesse ciclo (`Allow Re-entry` ligado), tentando de novo em vez de nunca mais tentar |

### O que este item não resolve

**Retroativo aos 9 contatos de hoje.** Publicar o workflow cobre quem entrar
em `nutricao-90d` sem telefone **a partir de agora**; os 9 já parados
precisam do mesmo backfill manual que o G-01 e o F-05 já usaram (`Add to
Workflow` em massa pela lista filtrada) — ação em massa em dado de
produção, regra 2 do briefing pede listar e confirmar antes, então não
executa sozinha.

**Domínio de e-mail verificado.** Não há ferramenta neste conector para
conferir se a subconta tem remetente/domínio configurado para envio
transacional — pendência a checar na tela antes de publicar, mesma classe
de "confirmar na tela" já registrada para Number Validation (R-13) e
Voice Intelligence (F-06).

**Resposta de opt-out por texto não vira DND sozinha.** O nó 4b/7b acima
trata toda resposta como "decisão manual" — inclusive uma pedindo para
parar. Fechado como item próprio, G-07 (`ROADMAP-SALES-ENGAGEMENT.md`,
seção 2.9.6 acima): workflow separado, mesmo padrão do R-17 aplicado ao
canal e-mail.

**Checklist do gestor — reputação e compliance do canal e-mail (G-07),
antes do primeiro envio real:** nenhum item do projeto tinha protegido a
reputação do canal e-mail até aqui (F-07 protege o número de WhatsApp,
F-08 o de telefone) — checklist, não workflow, mesmo motivo do F-07/F-08:
não existe gatilho nativo para ler taxa de rejeição, denúncia de spam ou
status de autenticação de domínio por workflow.

| Conferir | Por quê |
|---|---|
| Domínio de envio tem SPF, DKIM e DMARC configurados (Configurações → E-mail) | Sem os três, provedores como Gmail/Outlook classificam o e-mail como spam ou rejeitam — e um domínio que nunca mandou e-mail em volume é "novo" para reputação, mesmo raciocínio que já fundamentou o F-14 (rampa de aquecimento do telefone) para outro canal |
| O template criado por `emails_create-template` manteve o link `{{unsubscribe}}` (ou o link de descadastro nativo do GHL) no rodapé | A API deste conector grava o HTML exatamente como enviado — se o texto de `biblioteca-mensagens.md` for colado sem o merge field, o e-mail sai sem descadastro de um clique, o mínimo exigido pela LGPD (art. 18) e o que evita denúncia de spam que derruba reputação de domínio mais rápido que qualquer outro fator |
| Volume dos dois primeiros dias de `EM-1`/`EM-2` fica pequeno (mesma lógica do lote de 10-13/dia do G-03/F-14, mesmo sem rampa formal desenhada para e-mail) | Um domínio novo mandando dezenas de e-mails no mesmo dia é o padrão que provedores associam a spam — o volume real aqui é baixo por natureza (F-15 mede zero lead real resgatável hoje), então o risco é menor que o do WhatsApp/telefone, mas não é zero se o backfill dos 9 contatos (acima) sair de uma vez |

**Pronto quando:** todo contato que cai em `abandoned`+`nutricao-90d` sem
telefone e com e-mail recebe ao menos uma tentativa de contato real pelo
canal que ele de fato tem, em vez de reciclar indefinidamente sem nunca ser
procurado; os dois templates (`EM-1`, `EM-2`) existem em
`biblioteca-mensagens.md` (feito nesta rodada) e o workflow está publicado
na tela.

---

## 2.31 "Atendeu fica em CONECTAR" transformou `conectado-hoje` em mudo permanente — F-16

Achado desta rodada, conferindo o commit `1d04af2` que chegou do PC do dono
(mudança de etapa aplicada ao vivo em 5 workflows). A mudança está certa no
que ela quer fazer. O problema nasce do encontro dela com uma contradição
antiga que, até hoje, era inofensiva.

**A cadeia, elo por elo:**

| # | Fato | Onde conferi |
|---|---|---|
| 1 | `conectado-hoje` é aplicada pelo `Pós-ligação v2` em **5 ramos** (nós 13, 26, 77, 86, 97), todos `add_contact_tag` | dump ao vivo, `status: published`, versão 4 |
| 2 | **Nenhum** dos 29 dumps tem `remove_contact_tag` com `conectado-hoje`. Nenhum documento de `wesales/` especifica reset diário, de 24h ou de fim de dia | varredura dos 29 dumps + `grep` em `wesales/`. Refeita **depois** da reescrita multicanal da 12x30 (`23db864`): a régua nova também não removeu. Três dumps estão pré-patch (seção 2.31.3), mas aquele patch só edita listas `workflow_id` de nós `remove_from_workflow` — não há como uma remoção de tag estar escondida neles |
| 3 | A função declarada da tag é "tira o lead das filas **do dia** após conexão" | `campos-e-tags.md`, T-05 |
| 4 | A classificação declarada da mesma tag é família **Estado** — "sobrevive à saída de cadência" | `IMPLEMENTACAO-WORKFLOWS.md`, seção da tabela das três famílias |
| 5 | (3) e (4) se contradizem: "do dia" é pulso, "sobrevive" é estado. A conta ao vivo implementa a versão permanente | consequência de (2) |
| 6 | Até 22/09 a contradição não doía: o ramo `Atendeu` movia a oportunidade **para fora** de `CONECTAR` (ia para `3d26fcd1`), e as duas filas do SDR também exigem `etapa = CONECTAR`. Quem excluía o lead da fila era a cláusula de etapa; `conectado-hoje` era redundante | `_antes-patch-funil/Pós-ligação v2.json` vs. filtros 8.2/8.3 |
| 7 | `1d04af2` faz o `Atendeu` **ficar** em `CONECTAR` (`deb60542`). A cláusula de etapa para de excluir, e `conectado-hoje` — que nunca sai — fica sendo a única cláusula de pé | diff do dump, nós do ramo `Atendeu` |

**O que isso produz:** um lead que o SDR alcança uma vez e que **não** fecha
horário na mesma ligação sai de `Fila Telefone Hoje` e `Fila WhatsApp Hoje`
**para sempre** — enquanto a oportunidade continua aberta em `CONECTAR` e a
cadência continua criando tarefa para ele. O trabalho não desaparece: ele
some das duas listas de onde o SDR trabalha e reaparece só na lista de
tarefas cruas. É o pior formato de vazamento: silencioso e com a
oportunidade parecendo saudável no funil.

Os dois filtros afetados, literais:

| Lista | Filtro hoje | O que a cláusula de etapa fazia até 22/09 |
|---|---|---|
| 8.2 `Fila Telefone Hoje` | `fila-tel` **E** não `nao-perturbe` **E** não `telefone-invalido` **E** não `conectado-hoje` **E** etapa = `CONECTAR` | excluía o lead que atendeu, porque ele saía de `CONECTAR` |
| 8.3 `Fila WhatsApp Hoje` | `fila-wa` **E** não `nao-perturbe` **E** não `conectado-hoje` **E** `Permissão WhatsApp` = `Sim` **E** etapa = `CONECTAR` | idem |

**Estado declarado, para não confundir armadilha com incêndio:** medi a conta
nesta rodada. `conectado-hoje` está em **2 contatos**, os dois do próprio
projeto (`teste atendeu` e `ZZ TESTE ESTRUTURA`). **Zero lead real.** Não está
acontecendo com ninguém — dá para consertar antes de doer. O que torna isso
urgente não é o dano de hoje, é que o primeiro lote que entrar em cadência
começa a produzir o vazamento a partir da primeira conexão.

**Quatro saídas, e a recomendação:**

| # | Saída | Custo | Efeito colateral |
|---|---|---|---|
| A | Dar à tag o reset que o nome dela promete: dentro do `Pós-ligação v2`, depois de cada `Add Tag`, um `Wait 24h` → `Remove Tag conectado-hoje` | edição em 5 ramos de **um** workflow que já está sendo editado | nenhum workflow novo; o nome da tag passa a ser verdade |
| B | Trocar a cláusula das filas: em vez de não `conectado-hoje`, usar não `fechar-horario` (o estado novo "conectado, fechando horário") | edição de 2 listas inteligentes | depende do `Fechar Horário` publicado; `conectado-hoje` fica sem função e deve sair da família Estado |
| C | Um workflow recorrente de meia-noite que remove `conectado-hoje` de todo mundo | workflow novo + o MCP não cria workflow | mais uma peça para manter |
| D | Aceitar a tag como permanente e tirar a cláusula das duas filas | edição de 2 listas | perde o efeito "já falei com ele hoje" — o SDR volta a ver na fila quem ele acabou de ligar |

> **Atualização de 23/09 04:40 — o dono executou, e com uma variante melhor que a
> minha em dois pontos.** Ele fez a saída A **em workflow à parte** (`tag adicionada
> → espera 1 dia → remove`, `build_limpa_conectado.py`, `allowMultiple: true`) em
> vez de dentro do `Pós-ligação v2`, que era o que eu recomendei. Melhor: não
> acrescenta cinco ramos de `Wait` num workflow de 130 nós, e a re-entrada fica
> explícita. A cópia `ZZ TESTE Limpa conectado-hoje (24 h)` (espera 2 min) foi
> testada e **conferi por medição que a tag saiu** — `conectado-hoje` em 2 contatos,
> os dois de 01:55, nenhum é o 9940.
>
> **E ele achou uma saída que eu não tinha visto, que é melhor que a A para o
> filtro:** `Fila Telefone Hoje = fila-tel + etapa-conectar`, **dispensando
> `conectado-hoje` na lista** — porque a 12x30 põe e tira `fila-tel` a cada toque
> (conferido: `Cadência 12x30` adiciona nos nós 48/108/161/214/274/327 e remove nos
> 64/117/170/230/283/336). Se `fila-tel` só existe enquanto a tentativa está
> liberada, ele já carrega a informação que a cláusula `não conectado-hoje` tentava
> **Estado confirmado em 23/09 04:55:** a real `Limpa conectado-hoje (24 h)`
> (`e3c012bf`) está **no ar** com `startAfter: {"type":"days","value":1}`, e a cópia
> `ZZ TESTE` (espera 2 min) fica em **rascunho** — o dono mediu o teste antes de mim
> (tag posta no 9940 às 04:32:29, saiu às 04:34:31) e minha leitura foi confirmação
> independente, não a resposta a um item aberto. Ele registrou também o detalhe de
> gatilho que vale reter: **contatos que já carregavam a tag não disparam** o
> removedor, porque gatilho de tag dispara na aplicação e a tag já estava lá — hoje
> são só os de teste, e saem na limpeza do A9. É a mesma mecânica do
> `fechar-horario` (§2.31.1), aplicada certo.
>
> dar. Minha saída A trata o sintoma (a tag não expirava); a dele tira a cláusula da
> equação. **As duas juntas são o certo:** a tag passa a expirar (higiene do estado)
> e a lista deixa de depender dela (o filtro fica com uma cláusula em vez de duas —
> e cláusula que não existe não pode virar dependência escondida, que é a lição do
> F-16).

**Recomendo A.** ⚠️ **A saída B caiu** — eu a tinha escrito como alternativa
limpa e ela não sobrevive à conferência: a seção 2.31.2 mostra que o
removedor de `fechar-horario` mora dentro do `Fechar Horário` e **não é
alcançado pelo caminho de quem agenda** (o `Pós-agendamento v2` arranca o
contato do workflow no nó 4, e as saídas dele não rodam). B trocaria uma
exclusão permanente por outra. B só volta a valer se o nó 4 do
`Pós-agendamento v2` também remover a tag. Nenhuma das saídas é aplicável por
este MCP (edição de workflow e de lista inteligente não têm ferramenta) — é
tela ou `wesales/tools/`.

### 2.31.1 A tag `fechar-horario` nasceu com o consumidor em rascunho — janela fechada limpa em 23/09

Quando abri este achado, `Pós-ligação v2` (publicado) já aplicava
`fechar-horario` e o único que a remove, o `Fechar Horário`, estava em
**rascunho** — com gatilho na própria tag. Gatilho de tag dispara no *evento*
de aplicação, e aplicar tag já presente não gera evento: todo lead que
conectasse na janela ficaria invisível ao workflow para sempre.

**Fechado no `23db864`, do PC do dono, ainda nesta rodada:** o `Fechar Horário`
foi publicado (v4, `status: published`). Remedi depois da publicação:
`fechar-horario` em **0 contatos**. A janela fechou sem nenhum lead dentro
dela. Não há nada a corrigir e nada a limpar.

**A regra fica, porque o caso vai repetir:** sempre que um workflow novo é
gatilhado por tag, conferir se quem *aplica* a tag já está publicado antes
dele. Par "aplicador no ar + consumidor em rascunho" numa tag que ninguém
remove produz exclusão permanente e silenciosa. A ordem certa é publicar o
consumidor primeiro, ou o aplicador por último.

### 2.31.2 `remove_from_workflow` pula os nós de saída — e isso derruba uma das minhas quatro saídas

Conferindo como `fechar-horario` sai do contato, achei que a remoção dela mora
**dentro** do `Fechar Horário`, nos 4 nós de saída dele (36, 38, 39, 40, os
quatro `Remove Tag`). Só que o caminho mais importante não passa por esses nós:

| Caminho | Quem conduz | Passa pelos nós 36/38/39/40? |
|---|---|---|
| lead desiste / vira nutrição | o próprio `Fechar Horário` | sim — a tag sai |
| **lead agenda a reunião** | `Pós-agendamento v2`, nó 4, `remove_from_workflow` → `Fechar Horário` | **não** — o contato é arrancado do workflow e as saídas dele não rodam |

`remove_from_workflow` cancela os passos pendentes do contato no workflow
alvo; os nós de limpeza do alvo não são executados. Logo **todo lead que
agenda fica com `fechar-horario` para sempre** — e é justamente o lead que a
`Recuperação de No-show` pode devolver ao trabalho ativo (ela reaplica
`fila-tel` nos nós 12, 19 e 26).

**Consequência direta para a decisão da seção 2.31:** a saída **B** (trocar a
cláusula das filas de `não conectado-hoje` para `não fechar-horario`) **não
serve como está escrita.** Ela troca uma exclusão permanente por outra: parece
limpa porque `fechar-horario` tem removedor, mas o removedor não é alcançado
pelo caminho de quem agenda. B só passa a valer se o nó 4 do
`Pós-agendamento v2` também remover a tag, ao lado do `remove_from_workflow`.
Recomendação revisada, em uma frase: **quem arranca o contato de um workflow
precisa limpar, no mesmo nó, as tags que as saídas daquele workflow
limpariam.** No caso concreto é um `Remove Tag fechar-horario` no nó 4 do
`Pós-agendamento v2` — uma peça, um workflow.

**Exposição geral desta classe, medida nos 29 dumps.** Descontando as
auto-remoções (workflow que se remove no fim do próprio ramo, onde a limpeza
roda antes e está correta), sobram 5 alvos arrancados por terceiros com
limpeza de tag nos próprios nós:

| Alvo (publicado) | Tags que ele limpa nas saídas | Arrancado por |
|---|---|---|
| `Cadência 12x30` | `atraso-1a-tentativa`, `fila-quente`, `fila-tel`, `fila-wa` | `Fechar Horário` (nó 0), `Pós-agendamento v2` (nó 4), `Pós-ligação v2` (nós 54 e 127) |
| `Cadência Inbound` | `atraso-1a-tentativa`, `cad-inbound`, `fila-quente`, `fila-tel`, `fila-wa` | `Fechar Horário` (nó 0), `Pós-agendamento v2` (nó 4) |
| `Reengajamento 90 dias` | `atraso-1a-tentativa`, `cad-inbound`, `fila-tel`, `fila-wa`, `nutricao-90d`, `reengajamento-ativo` | `Fechar Horário` (nó 0), `Pós-agendamento v2` (nó 4) |
| `Fechar Horário` | `fechar-horario` | `Pós-agendamento v2` (nó 4) |
| `Recuperação de No-show` | `fila-tel` | `Pós-agendamento v2` (nó 4) |

Nem toda linha é bug: várias dessas tags são limpas **também** pelo Mestre de
saída, que é justamente a rede de segurança para este caso, e as de fila são
reaplicadas na tentativa seguinte. O que a tabela diz é onde olhar — e
`fechar-horario` é a única da lista que **não** tem segunda rede: quem limpa
ela é só o `Fechar Horário`. Conferir tag por tag contra o Mestre de saída
antes de mexer em qualquer outra linha.

### 2.31.3 O dump de 3 workflows ficou descrevendo a conta pré-patch — corrigido na ferramenta

Enquanto conferia a parte 2 da 12x30, li nos dumps que as listas de
`remove_from_workflow` **não** citam a `Cadência 12x30 — parte 2` — nem no
`Fechar Horário` (nó 0), nem no `Pós-agendamento v2` (nó 4), nem no
`Pós-ligação v2` (nós 54 e 127). Ia registrar isso como achado grave: lead que
agenda sairia da parte 1 e continuaria recebendo toque automático da parte 2.

**Não registro, porque o dump não pode responder isso.** Comparei os três
arquivos com os backups `_antes-patch-parte2/` e eles são idênticos em
`version` e `updatedAt`. A causa está na ferramenta:

| Script | Exporta o backup | Aplica | **Re-exporta o estado novo** |
|---|---|---|---|
| `patch_funil_reuniao.py` | linha 137 | linha 138 | **sim**, linha 150 |
| `patch_remove_parte2.py` | linha 26 | linha 27 | **não existia** |

Por isso os 5 workflows do patch de funil têm dump fresco e correto, e os 3 do
patch da parte 2 têm dump congelado no estado de antes. O `workflows-json/`
passou a descrever uma conta que a conta já deixou — e de um jeito silencioso,
porque `version` e `updatedAt` também são do arquivo antigo, então nenhuma
checagem de frescor pega.

**Corrigido nesta rodada, na ferramenta e não no arquivo:**
`patch_remove_parte2.py` ganhou o `g.export` depois do `put`, espelhando a
linha 150 do script irmão, e os dois caminhos de export passaram a ser
relativos ao script (`DUMPS`) em vez de ao diretório de execução — o backup
antes só caía no lugar certo se o script fosse rodado de dentro de
`wesales/tools/`. Nada disso toca a conta; é o repositório voltando a contar a
verdade na próxima execução.

**O que continua em aberto, e o tamanho certo dele.** Depois de escrever o
parágrafo acima fui ler o assunto do commit `23db864` e ele diz, na própria
linha de título: *"parte 2 nas remoções"*. Ou seja, **há evidência de que o
dono rodou o script com `--aplicar`** — o que falta não é o conserto, é a
confirmação de quantos nós ele pegou. Deixo o item registrado nesse tamanho, e
não maior: não é um defeito provável, é uma confirmação pendente.

Por que ainda vale confirmar: o script só acrescenta a parte 2 aos nós que já
citam a parte 1, e varre apenas os **publicados** — um workflow que estivesse
em rascunho na hora da execução ficou de fora. E a consequência, se algum nó
tiver ficado para trás, é a pior possível numa máquina de pré-venda: o lead que
agenda continua recebendo toque **automático** da segunda metade da régua.

Nem o dump nem o MCP respondem isso — o dump é o pré-patch (acima) e o
`GHL CRM` não tem ferramenta de workflow. Resolve em um comando, no PC, que não
escreve nada: `python patch_remove_parte2.py` **sem** `--aplicar`. Ele lista
quantos nós ainda faltam por workflow; **zero nó listado = confirmado, nada a
fazer**.

---

## 2.32 Eu errei este achado: o Espelho de Etapa já estava publicado — F-17, **retirado**

Achado conferindo o `61eb167`, do PC do dono. O achado **dele** é excelente e
maior que o meu: num workflow cujo gatilho **não é oportunidade** (tag, contato,
resposta, link, agendamento), a condição `Pipeline stage is …` lê **valor vazio**
e dá falso — sem erro nenhum, o lead só segue pelo "não". Ele mediu isso no
registro de execução da `ZZ TESTE 12X30` e achou **11 workflows publicados**
testando etapa às cegas. A solução dele é certa: um workflow `Espelho de Etapa`,
esse sim com gatilho de oportunidade, que mantém no contato exatamente uma tag de
estado (`etapa-novo-lead`, `etapa-conectar`, `etapa-reuniao`, `etapa-negociar`,
`etapa-formalizar`, `status-nutricao`, `status-perdido`, `status-ganho`), e os
outros passam a testar a **tag**, que funciona com qualquer gatilho.

### Correção, escrita minutos depois de eu ter publicado o achado

**O achado abaixo está errado e eu o retiro.** Escrevi que o `Espelho de Etapa`
estava em rascunho com 8 consumidores publicados. Medi isso lendo
`workflows-json/Espelho de Etapa.json`, que dizia `status: draft`, v3,
`updatedAt` **01:53:09**. A conta tinha o workflow **publicado** (v4) às
**01:53:13** — quatro segundos depois daquele export. O dump que li já nascia
velho; o defeito nunca existiu na conta, só na fotografia.

Pior: eu tinha acabado de escrever, na seção 2.31.3 e no `APRENDIZADOS-CRM.md`,
a regra de comparar o dump com o backup irmão antes de afirmar qualquer coisa —
e não a apliquei. A regra, do jeito que eu a escrevi, também não teria salvado:
o `Espelho de Etapa` é **novo**, não tem backup irmão em `_antes-*/`, e eu tratei
ausência de backup como sinal de frescor. **Segunda perna da regra, que faltava:
dump sem backup irmão não é por isso recente.** Para um `status: draft`
especialmente, o valor é "no momento do export", nunca "agora" — e `draft` é o
estado natural de um workflow nos segundos entre montar e publicar, que é
exatamente a janela em que os scripts de `wesales/tools/` exportam.

**Como conferir de verdade, da próxima vez:** `status: draft` num dump só vira
achado depois de (a) comparar o `updatedAt` do dump com o horário do commit que
o trouxe, e (b) confirmar o estado por uma fonte que não seja o arquivo — a tela,
ou uma medição ao vivo do efeito (contatos com a tag, por exemplo). Sem isso, o
que existe é uma pergunta, não um defeito.

**O que sobrevive, e é o motivo de eu não apagar a seção:** a regra de ordem
(produtor antes de consumidor) continua certa e tem um caso real, medido ao
vivo, na §2.31.1 — a `fechar-horario`. O que não sobrevive é esta instância. E
sobrevive também o registro das 8 tags novas em `campos-e-tags.md`, que é fato
independente do erro.

**Estado real, conferido depois da correção:** `Espelho de Etapa` publicado (v4,
36 nós), aplicando as tags; os 11 consumidores publicados. A ordem está certa.
Fica valendo a pergunta de tela que a §2.32.1 já levantava e que nenhum dump
responde: **o gatilho de oportunidade etiqueta o acervo ou só mudança futura?**
Se for só futura, as 45 oportunidades paradas em `NOVO LEAD` não recebem
`etapa-novo-lead` e seguem invisíveis às condições. Isso continua aberto.

---

O texto original do achado fica abaixo, riscado pelo parágrafo acima, para a
rodada seguinte ver o erro e não repeti-lo.

**~~O problema é a ordem de publicação, e é a terceira vez nesta mesma noite:~~**

| Papel | Peça | Estado ao vivo |
|---|---|---|
| **produtor** — único que aplica as 8 tags (16 nós) | `Espelho de Etapa` | **`draft`**, v3, 36 nós |
| **consumidores** — já testam as tags | `CONECTAR Estagnado`, `Fechar Horário`, `Interceptação de Sinal — Clique v2`, `Interceptação de Sinal — Resposta v2`, `Opt-out por Palavra-chave`, `Recuperação de No-show`, `Reengajamento 90 dias`, `Retorno Vencido`, `SLA do Closer — No-show` | **`published`**, os 8 (9 peças, `Reengajamento` conta uma vez) |
| consumidor ainda em rascunho | `Cadência 12x30 — parte 2` | `draft` |

Enquanto o Espelho estiver em rascunho, os 8 publicados testam uma tag que
**ninguém aplica**. A condição lê tag ausente e vai pelo "não" — que é
exatamente o mesmo desvio silencioso que o patch foi feito para consertar. Antes
lia etapa vazia e ia pelo "não"; agora lê tag ausente e vai pelo "não". **O
comportamento não mudou; só mudou o motivo.** O conserto está escrito e não está
no ar.

Uma exceção parcial, para a tabela não exagerar: o `Reengajamento 90 dias`
(publicado) aplica `etapa-conectar` no nó 6 e remove `status-nutricao` no nó 5 por
conta própria. É um aplicador local de um ramo, não o espelho — não cobre os
outros 7 nem os outros estados.

**Medido ao vivo, para separar armadilha de incêndio:** `etapa-conectar` está em
**1 contato** — `teste não atende`, o contato de teste do dono (carrega
`teste-12x30`, `dateUpdated` 23/09 02:00), e chegou lá pelo nó 6 do
`Reengajamento`, não pelo espelho. **Zero lead real.** Como nas outras duas,
armadilha e não incêndio — e a janela fecha com um clique.

**O que fazer, e é ordem e não decisão:** publicar o `Espelho de Etapa` **antes**
de ligar a esteira, e de preferência antes de qualquer teste novo nos 8. Como o
espelho tem gatilho de oportunidade e re-entrada ligada, publicá-lo com as 50
oportunidades já existentes deve etiquetar o acervo — conferir isso ao publicar,
porque se o gatilho só pegar mudança futura de etapa, as 45 oportunidades paradas
em `NOVO LEAD` nunca recebem `etapa-novo-lead` e continuam invisíveis às
condições. **Essa é a pergunta a fazer na tela**, e é a única parte que o dump não
responde (gatilho não entra nesta exportação — seção 6 do `ESTADO-E-PLANO.md`).

**As 8 tags novas estão fora do `APROVADO.md`.** Entraram por ação do dono, no
próprio commit — não são criação minha e não estou desfazendo nada. Ficam
registradas em `campos-e-tags.md` e sinalizadas no `APROVADO.md`, na mesma
convenção do `teste-regua` e do `fechar-horario`, só para a contagem do gate parar
de divergir da conta. Com elas, a conta tem mais tags que as 21 do projeto —
contagem exata (e a correção de 23/09/2026, G-20, que achou esta mesma soma
errada aqui) em `campos-e-tags.md`, Etapa 3.

### 2.32.1 A regra que já custou três achados na mesma noite

| Ordem | Produtor | Consumidor | Resultado |
|---|---|---|---|
| errada | rascunho | publicado | consumidor testa/espera algo que ninguém produz, e vai pelo ramo errado **sem erro** |
| certa | publicado | publicado ou rascunho | consumidor que entra depois já encontra o estado montado |

Uma instância real em uma noite: `fechar-horario` (§2.31.1, fechada pelo dono no
mesmo dia), mais a família vizinha da tag cuja limpeza mora dentro de um
workflow (§2.31.2). A instância das 8 tags do espelho **não conta** — foi erro
meu de leitura de dump, corrigido no topo desta seção.

**Checagem barata, para entrar em toda rodada:** para cada tag que apareça em
condição de workflow publicado, procurar quem a aplica e conferir o `status` de
quem aplica. Se o aplicador está em `draft` e o consumidor em `published`, é
defeito ativo e silencioso. O comando que achou este caso está no
`APRENDIZADOS-CRM.md`, na entrada desta data.

---

## 2.33 `auditoria_tags.py` — as duas perguntas que acharam defeito hoje viraram auditoria, e a terceira apareceu sozinha

As checagens de tag que fiz à mão nesta noite acharam coisa real duas vezes.
Viraram `wesales/tools/auditoria_tags.py` (somente leitura, sai com 1 na
pergunta 1), para não depender de eu lembrar de rodar o heredoc certo. Ela
responde três perguntas, e a terceira nasceu da própria varredura.

**Pergunta 1 — a limpeza da tag é alcançada?** `remove_from_workflow` cancela os
passos pendentes do contato no alvo: os nós de saída do alvo não rodam. Tag cuja
limpeza mora dentro de um workflow é permanente para quem sai por remoção
externa. O relatório só acusa quando **nenhum** removedor está livre de ser
arrancado — se algum está, a tag tem por onde sair. Isso é o que separa alarme de
achado: o `toque`, por exemplo, é limpo pelo `Contador de Toques`, que ninguém
arranca, e por isso **não** entra na lista.

Três tags entram, e as três são reais:

| Tag | Limpa só em | Arrancado por | O que sobra no contato |
|---|---|---|---|
| `fechar-horario` | `Fechar Horário` | `Pós-agendamento v2` (nó 4) | quem **agenda** fica marcado como "fechando horário" para sempre (§2.31.2) |
| `nutricao-90d` | `Reengajamento 90 dias` | `Fechar Horário` (nó 0), `Pós-agendamento v2` (nó 4) | lead reativado que agenda ou volta a fechar horário continua marcado como nutrição |
| `cadencia-12x30-p2` | `Cadência 12x30 — parte 2` | `Fechar Horário`, `Pós-agendamento v2`, `Pós-ligação v2` | lead fica marcado como "está na parte 2" para sempre — e a parte 1 passou a ter **portão por tag** (`9020079`), então isso pode barrar a reentrada dele |

As três têm a mesma correção, a mesma da §2.31.2: **quem arranca o contato limpa,
no mesmo nó, as tags que as saídas do alvo limpariam.** Três `Remove Tag` em dois
workflows resolvem as três.

**Pergunta 2 — o aplicador está no ar antes de quem testa?** Hoje: nenhuma
pergunta aberta. Esta pergunta nunca muda o código de saída, de propósito — foi
lendo `status: draft` num dump exportado 4 segundos antes da publicação que eu
registrei o F-17 errado (§2.32). No script está escrito por quê.

**Pergunta 3 — tag só removida, nunca aplicada.** Não é defeito de workflow: é
peça do desenho antigo que sobrou, e cada linha é uma decisão sua.

| Tag | Situação | Leitura |
|---|---|---|
| `fila-wa` | removida em **75 nós**, em 8 workflows; aplicada em **nenhum** | a `Fila WhatsApp Hoje` (lista 8.3) **nunca pode encher**. E não é bug: o `PLANO-MULTICANAL.md` (D5/D6) fez o WhatsApp virar parte do próprio toque — ligação Stevo e mensagem automática — em vez de fila separada do SDR. A tag ficou sem produtor **por decisão**, e os 75 nós são no-op. O que está desatualizado é a lista 8.3, não a cadência |
| `fila-linkedin` | removida em 1 nó; aplicada em nenhum | já era conhecida e deliberada — T-04, "reserva, hoje sem canal na cadência" (lacuna L-03). Fica |

Decisão que falta para o `fila-wa`: **apagar a lista 8.3 e tirar os 75 nós**, ou
**devolver ao WhatsApp uma fila própria**. Recomendo a primeira: o plano novo já
resolveu o canal de outro jeito, e manter 75 nós que não fazem nada é custo de
leitura em todo patch futuro. Nenhuma das duas sai por este MCP.

Rodar junto com as outras duas, toda rodada:

```
python3 wesales/tools/auditoria_refs.py     # referência para workflow arquivado
python3 wesales/tools/auditoria_tags.py     # ciclo de vida das tags de estado
```

Limite que vale para as duas: leem os dumps, e dump pode estar defasado da conta.
Comparar com o backup irmão em `_antes-*/` antes de concluir — e, para `draft`,
não concluir nada sem confirmar fora do arquivo.

### 2.33.3 Três dos cinco achados desta auditoria já estavam resolvidos quando eu os reportei

Correção do registro, e é a mais séria da noite porque eu levei dado velho ao dono
duas vezes. Datas medidas:

| Quando | O que |
|---|---|
| 22/09 16:27 | `updatedAt` do dump de `Mestre de saída v2` que eu estava auditando |
| 23/09 03:24 | `Triagem da Nutrição` **publicada** — ela remove `cad-inbound` e `nutricao-90d` |
| 23/09 04:35 e 04:55 | **eu reportei os 5 achados como abertos** |
| 23/09 05:05 | o dono re-exportou os dumps; meu `auditoria_tags.py` foi a **0** |

Ou seja: das 5 linhas, **3** (`cad-inbound` em dois lugares e `nutricao-90d`) já
estavam resolvidas na conta **uma hora antes** de eu reportá-las — o dump dizia
`draft` na `Triagem` porque foi exportado antes da publicação. As outras 2
(`fechar-horario`, `cadencia-12x30-p2`) o `Mestre de saída v2` já limpava no backup
`_antes-patch-mestre`, mas o dump que eu tinha era de 22/09 16:27 e não as
continha; **não consigo datar o momento em que entraram**, então não afirmo que
estavam abertas nem que estavam fechadas quando eu as reportei.

**O que isso custou:** as pendências 9a e 9b do `ESTADO-E-PLANO.md`, apresentadas
ao dono como trabalho a fazer, eram trabalho já feito. Nenhuma escrita errada no
CRM — só ruído na fila dele, que é exatamente o que uma auditoria deveria reduzir.

**Conserto na ferramenta, não no texto.** O `auditoria_tags.py` ganhou uma
**guarda de frescor**: para cada dump, compara o `updatedAt` dele com o do backup
`_antes-*` mais novo do mesmo workflow. Se o backup for mais novo, o arquivo
principal não foi re-exportado depois de um patch, e a auditoria imprime um aviso
em bloco dizendo que qualquer achado envolvendo aquele workflow pode já estar
resolvido. Hoje o aviso não aparece — os dumps estão frescos — mas teria aparecido
ontem à noite e eu não teria reportado nada como aberto.

As três auditorias ganharam também guarda de `BrokenPipeError`, pelo mesmo motivo
da §2.34: `... | head` morria com traceback e `exit=1`, que parece falha de
auditoria.

**A regra, agora com três instâncias:** esta família de auditoria lê fotografia, e
fotografia deste repositório fica velha em minutos quando alguém está trabalhando
na conta. Achado tirado de dump só vira item para o dono depois de confirmação ao
vivo — e a confirmação ao vivo, neste projeto, é a `auditoria_final.py` (que lê a
API) ou uma medição de efeito pelo MCP. Da nuvem eu tenho a segunda; a primeira
precisa do PC.

### 2.33.4 A guarda de frescor não pegava dump sem irmão — e havia um `published` velho de 28 h

A guarda que eu pus na §2.33.3 compara cada dump com o backup `_antes-*` do
mesmo workflow. Boa, e **cega para dump que não tem irmão** — que é a maioria.
Achei o caso concreto conferindo o G-13 do dono:

| Fonte | Diz |
|---|---|
| `workflows-json/AGENDAR Estagnado.json`, `updatedAt` **22/09 00:45** | `status: published` |
| commit `23db864` do dono, 23/09 ~01:47, no assunto | "**W17d despublicado**" |

O dump está **28 h atrás da conta** e afirma `published` sobre um workflow que o
dono já tinha despublicado. Não tem backup `_antes-*`, então a guarda imprimiu 0.
Se eu tivesse tirado um achado dali, seria o quarto dado velho levado ao dono.

**Segunda guarda, heurística e declarada como tal:** o `auditoria_tags.py` agora
compara o `updatedAt` de cada dump com o **mais novo da pasta** e lista os que
estão 12 h ou mais atrás. Não prova defasagem — a pasta pode ter workflow que
ninguém tocou há dias, e é isso mesmo. O que ela faz é nomear o que **precisa de
confirmação ao vivo antes de virar item**. Hoje lista 7:

```
ZZ TESTE API                31 h     Contador de Toques            28 h
ZZ TESTE W6                 29 h     Lead Esquecido em NOVO LEAD   28 h
AGENDAR Estagnado           28 h     Fila Travada                  27 h
Alerta de Speed-to-lead     28 h
```

Quatro deles são os monitores do F-05 (`Alerta de Speed-to-lead`, `Contador de
Toques`, `Lead Esquecido em NOVO LEAD`, `Fila Travada`) — ou seja, **exatamente a
parte da máquina sobre a qual eu tenho menos informação fresca**. Qualquer coisa
que eu disser sobre os monitores a partir de dump, daqui pra frente, sai com esse
rótulo.

E um bug meu no caminho, pego porque rodei com `| head` e vi o traceback: as duas
guardas usavam `nome` como variável de laço, sombreando a lambda `nome()` que
resolve id → nome do workflow. A auditoria morria com `'str' object is not
callable` **depois** de imprimir os avisos — ou seja, falhava exatamente na parte
que importa, e o cabeçalho bonito dava a impressão de que tinha rodado.
Corrigido; lição pequena e velha: em script de relatório, nome de variável de
laço não pode colidir com nome de função auxiliar.

### 2.33.5 Auditei os quatro monitores do F-05 — o candidato não virou achado, e o que sobrou foi uma lacuna no `patch_condicoes_etapa.py`

Fui olhar os quatro monitores justamente porque são os dumps mais velhos que eu
tenho (28 h, §2.33.4) — onde o cuidado tem de ser maior, não menor. Dois deles
testam **etapa de oportunidade**, que é exatamente o que o G-13 mostrou que lê
vazio quando o gatilho não é de oportunidade:

| Monitor | Nó | Testa |
|---|---|---|
| `Alerta de Speed-to-lead` | 6, "Ainda sem 1ª tentativa?" | etapa = `CONECTAR`, `conditionType: opportunities` |
| `Lead Esquecido em NOVO LEAD` | 1, "Ainda em NOVO LEAD e aberta?" | etapa = `NOVO LEAD`, `conditionType: opportunities` |

E nenhum dos dois está em `_antes-patch-condicoes/`, ou seja, o patch não passou
por eles.

**Não registro isso como defeito, e o motivo é a regra da §2.33.3 funcionando.**
Se esses dois tivessem condição de oportunidade com gatilho que não é de
oportunidade, a `auditoria_final.py` do dono — que lê **a API, inclusive o
gatilho** — teria acusado, e ela reportou **0 problemas**. Fonte ao vivo vence
dump de 28 h. A leitura mais provável é que os dois têm gatilho de oportunidade
(faz sentido: "lead esquecido em NOVO LEAD" nasce de oportunidade criada), e aí a
condição funciona e não havia o que patchear. **Candidato, não item.**

**O que sobra é certo, porque está no código e não depende do estado ao vivo — e
são duas lacunas do `patch_condicoes_etapa.py`:**

1. **`ALVOS` é lista fixa de 10 nomes.** Quem não está na lista nunca foi
   examinado — inclusive os dois monitores acima. Ou seja, a cobertura do patch é
   uma **lista**, não uma varredura. Quem varre é a `auditoria_final.py`; é ela
   que precisa continuar rodando, e é ela que pega o que a lista não viu.
2. **O tradutor cobre 3 dos 5 estados.** `traduz()` mapeia só
   `CONECTAR → etapa-conectar`, `REUNIÃO DE DIAGNÓSTICO → etapa-reuniao` e
   `abandoned → status-nutricao`. **Não há entrada para `NOVO LEAD`, `NEGOCIAR`
   nem `FORMALIZAR`**, embora o Espelho de Etapa produza `etapa-novo-lead`,
   `etapa-negociar` e `etapa-formalizar`. Então, se a varredura um dia apontar um
   workflow que testa essas três etapas com gatilho que não é de oportunidade, o
   patch devolve `None` e **deixa a condição como estava, em silêncio**.

Hoje nenhuma das duas dói: os dois monitores têm gatilho compatível (pela
evidência acima) e nenhum workflow publicado testa `NEGOCIAR`/`FORMALIZAR` com
gatilho de tag. A (2) é a que vai morder primeiro — o `Lead Esquecido em NOVO
LEAD` é o candidato natural a ganhar gatilho de tag algum dia, e nesse dia o
patch não vai saber traduzir a etapa dele.

**Correção sugerida, pequena:** acrescentar as três entradas que faltam em
`traduz()` (uma linha cada) e trocar `ALVOS` por "todos os publicados, menos a
`Cadência 12x30` parte 1", que é a única exceção que o próprio docstring
justifica. Não faço porque o script escreve na conta e roda no PC — é edição do
dono.

### 2.33.6 A `Cadência Inbound` não tem o portão de capacidade — e eu havia lido o `Monitor de Capacidade` errado

Fui conferir se os guias (`GUIA-SDR.md`, escritos às 01:19) envelheceram com o
que entrou no ar depois. Envelheceram menos do que eu esperava, e o que apareceu
foi outra coisa.

**Primeiro, a correção de uma leitura minha.** Eu escrevi, na §2.29 e em várias
rodadas de check-in, que o `Monitor de Capacidade` "avisa, **não represa**" — e
usei isso para dizer que a regra de capacidade da D14 não é aplicada. O fato é
verdadeiro (o Monitor é 1 nó de `internal_notification`) e **a implicação era
falsa**: o Monitor nunca foi o ponto de aplicação. A regra é aplicada em dois
lugares que eu não tinha olhado:

| Peça | Papel |
|---|---|
| `faxina_tarefas.py` (linhas 197-213) | conta, **por SDR**, vencidas abertas e toques de hoje; liga e desliga a tag `sdr-lotado` nos leads em `CONECTAR` daquele SDR |
| `Cadência 12x30` parte 1 e parte 2 | **6 nós cada** condicionando em `sdr-lotado` — é o laço de espera de 1 h que represa o toque |

Ou seja: a capacidade **é** represada, e o guia está certo quando promete isso ao
SDR. Eu tinha um fato certo e tirei dele uma conclusão errada, por não ter
procurado o mecanismo fora do workflow que tem "Capacidade" no nome.

**Segundo, o achado que isso destravou:**

| Cadência | Nós condicionando em `sdr-lotado` |
|---|---|
| `Cadência 12x30` | **6** |
| `Cadência 12x30 — parte 2` | **6** |
| **`Cadência Inbound`** (272 nós, publicada) | **0** |

**A `Cadência Inbound` não tem portão de capacidade nenhum.** E ela é justamente
a cadência que carrega os leads agora: o "só inbound" do `bff2514` marcou **49
leads** com `cad-inbound`, e o nó 0 da Inbound é o portão que os admite. Então a
D14 — "com 50 ou mais tarefas vencidas, nenhuma tarefa nova de cadência é criada
para ele" — vale para a 12x30 e **não vale para o caminho por onde os leads
entram hoje**.

Pior detalhe: a Faxina **põe** a tag nos leads em `CONECTAR` do SDR lotado,
inclusive nos inbound. A tag é aplicada e a Inbound **não a lê**. O freio existe,
está engatado, e a roda que gira não está ligada nele.

**Consequência prática, e é a que o guia promete ao SDR:** o `GUIA-SDR.md` diz,
sem ressalva, "se você passar de 100 toques no dia ou tiver 50 ou mais tarefas
vencidas, o sistema segura os toques novos". Para um lead que entrou pela Inbound,
não segura. Com a régua concentrando a segunda-feira em +82% (§2.29), é
exatamente aí que o teto deveria valer.

**Correção sugerida:** portar os 6 nós de portão da 12x30 para a `Cadência
Inbound` — mesmo padrão, mesma tag, mesmo laço de 1 h. É edição de workflow
(tela ou `wesales/tools/`), não sai por este MCP. Enquanto não for, o guia
precisaria dizer "vale para a cadência outbound" — mas a correção certa é o
portão, não a ressalva.

### 2.33.7 `Canal que conectou` é campo de preenchimento manual — minha §2.34 leu a D10 errado

Na §2.34 eu escrevi que `Canal que conectou` "existe e ninguém escreve nele", e
que por isso "a pergunta que o multicanal existe para responder nunca vai ter
resposta". A primeira metade é verdadeira para **workflow**; a segunda é falsa, e
o `GUIA-SDR.md` mostra por quê:

> **Canal que conectou** (quando atendeu): Ligação WhatsApp, Ligação normal ou
> Mensagem. É assim que a gente descobre qual canal funciona melhor.

Ele está na mesma família de `Resultado da tentativa`: **o SDR preenche na tela**.
A D10 diz "marcado junto com o resultado" — e quem marca o resultado é o humano,
não o workflow. Logo "junto com o resultado" significa *o SDR marca os dois*, que
é o que o guia instrui. Minha leitura de que a D10 pedia escrita automática foi
invenção minha.

**O que isso muda na pendência 9c:** deixa de ser lacuna e volta a ser **decisão**
— manual (como está documentado e instruído) ou automático (um
`update_contact_field` por ramo no `Pós-ligação v2`, que tiraria uma marcação da
mão do SDR e garantiria o dado). Há argumento para os dois: manual capta o que só
o humano sabe (ele ligou pelo WhatsApp e a pessoa respondeu por texto); automático
não depende de disciplina. Recomendo **automático onde o ramo já sabe** (o nó que
trata "atendeu no WhatsApp" pode gravar `Ligação WhatsApp` sozinho) e manual só
onde o ramo não sabe. Mas é escolha do dono, e o estado atual não é defeito.

### 2.33.1 A `auditoria_final.py` do dono diz "0 problemas" e isso não cobre estes achados

O `beebd23` trouxe `wesales/tools/auditoria_final.py` com o resultado "26
publicados, 0 problemas". As duas auditorias não se contradizem: **fazem
perguntas diferentes.** Registro o cruzamento para ninguém ler "0 problemas"
como "nada a corrigir".

| Pergunta | Onde está |
|---|---|
| condição de oportunidade em workflow sem gatilho de oportunidade | `auditoria_final.py` (1) |
| nó apontando para workflow inexistente ou desligado | `auditoria_final.py` (2) e `auditoria_refs.py` |
| relógio errado (`sim` ou `{{right_now}}` puro) nos campos de data | `auditoria_final.py` (3) |
| tarefa com prefixo que a Faxina não reconhece | `auditoria_final.py` (4) |
| workflow que cria tarefa sem janela; mensagem sem janela | `auditoria_final.py` (5, 6) |
| **limpeza de tag pulada por `remove_from_workflow`** | **`auditoria_tags.py` (1) — só aqui** |
| **tag só removida, nunca aplicada** | **`auditoria_tags.py` (3) — só aqui** |

**E a dele tem uma vantagem que a minha não tem:** lê **ao vivo pela API**
(`GET /workflow/...` e `GET /workflow/.../trigger`), não os dumps. Ou seja, ela
não sofre da defasagem que me fez errar o F-17, **e vê o gatilho** — que é
exatamente o dado que falta para fechar a pergunta 1 do `auditoria_tags.py` com
certeza. Caminho de melhoria, quando alguém estiver no PC: mover as duas
perguntas do `auditoria_tags.py` para dentro do `auditoria_final.py`, ou dar ao
`auditoria_tags.py` a mesma fonte. Da nuvem eu não consigo — não há ferramenta de
workflow no MCP.

### 2.33.2 Dois consertos na minha própria auditoria, e o segundo era um defeito de verdade

**1. O `cad-inbound` mudou de papel, e meu julgamento sobre ele venceu.** Eu o
havia excluído da pergunta 1 raciocinando "marcador de origem que persiste não é
defeito". No `bff2514` o **nó 0 da `Cadência Inbound` passou a ser um `if_else`
que testa `cad-inbound`**: a tag virou o **portão** da cadência, e o nó 254 a
remove na saída. Remoção de portão pulada não é inofensiva — um lead que sai pelo
`Fechar Horário` ou pelo `Pós-agendamento v2` fica com o portão aberto. É o F-16
outra vez: **quando o papel de uma tag muda, todo julgamento antigo sobre ela
vence.** Tirei da lista de exceções.

**2. O script contava workflow em `draft` como rede de segurança.** Foi assim que
ele deixou de acusar `nutricao-90d` e `cad-inbound`: quem as limpa livre de
arranco é a `Triagem da Nutrição`, que está em **rascunho**. Rede que não está
publicada não salva ninguém, e o efeito foi a auditoria ficar **permissiva** — o
pior jeito de errar, porque silencia em vez de gritar. Corrigido: a rede tem de
estar `published`, e o relatório agora diz qual rascunho viraria rede.

Nota sobre `draft` nas duas correções: aqui ele **não** serve para acusar (essa é
a armadilha do F-17), só para **não creditar** uma rede. Direção segura.

**O relatório depois dos dois consertos — 5 achados, e 3 saem com um clique:**

| Tag | Limpa em | Resolve com |
|---|---|---|
| `nutricao-90d` | `Reengajamento 90 dias` | **publicar a `Triagem da Nutrição`** |
| `cad-inbound` | `Reengajamento 90 dias` e `Cadência Inbound` | **publicar a `Triagem da Nutrição`** |
| `fechar-horario` | `Fechar Horário` | `Remove Tag` no nó 4 do `Pós-agendamento v2` |
| `cadencia-12x30-p2` | `Cadência 12x30 — parte 2` | `Remove Tag` nos três que arrancam |

Ou seja: **publicar a `Triagem da Nutrição` fecha 3 dos 5**, e sobram os dois
`Remove Tag` que a §2.31.2 já pedia.

---


## 2.34 `auditoria_campos.py` — mapa de quem escreve e quem lê cada campo, e a lacuna que ele achou

Nasceu do `d880870`, onde o dono achou **à mão** "4 campos de data que nunca
gravavam". A pergunta generaliza, então virou script:
`wesales/tools/auditoria_campos.py`, somente leitura, **sai sempre com 0 de
propósito**. Ele não é alarme, é mapa — e a razão de não ser alarme é a regra
que este projeto aprendeu hoje: auditoria que grita sobre o que é intencional
treina a gente a ignorar auditoria. Aqui a maior parte do resultado é
intencional:

| Coluna | Quantos | Como ler |
|---|---|---|
| **só lido**, ninguém escreve | 23 | é o **normal** dos campos de qualificação: quem preenche `Budget`, `Decisor`, `Dor principal`, `Segmento`, `Urgência`, `Motivo da desqualificação`, `Reunião foi qualificada` é o SDR ou o closer na tela. Workflow lê o que o humano classificou |
| **só escrito**, ninguém lê | 13 | quase sempre significa **"a lista que leria ainda não existe"**. `Prioridade`, `Tentativas telefone`, `Conexões telefone` existem para ordenar e mostrar nas listas inteligentes (seções 8.x), e **lista inteligente não aparece em nenhum dump** — o script não vê listas, logo não pode chamar isso de órfão. É, aliás, a checklist do que o **A7** vai precisar consumir |
| **nem escrito nem lido** | **4** | é a coluna que vale olhar |

Os quatro, cruzados um por um com `campos-e-tags.md` — e só o primeiro é
lacuna:

| Campo | O que o documento diz | Veredito |
|---|---|---|
| **`Canal que conectou`** | D10 do `PLANO-MULTICANAL.md`: "campo novo, **marcado junto com o resultado**" | ⚠️ **lacuna real.** Quem marca o resultado é o `Pós-ligação v2`, publicado — e ele **não escreve** este campo. O id `TxJmoWdkA8rTqC1uEsMW` não aparece em **nenhum** dos 33 dumps. Ou seja: a pergunta que o multicanal existe para responder — *qual canal conectou?* — nunca vai ter resposta, porque ninguém grava a resposta |
| `Hora da conexão` | C-25, preenchido por "Workflow (F-02)" | especificado, não montado. Consistente |
| `Hora do retorno` | S-01/L-01: existe na tela, fiação especificada, "falta só a montagem manual" | especificado, não montado. Consistente |
| `Necessidade` | veio do formulário e "segue duplicando `Dor principal`" | duplicata declarada de desenho antigo. Não é lacuna |

**A correção do `Canal que conectou` é pequena e cabe onde o dono já está
mexendo:** no `Pós-ligação v2`, nos mesmos nós que gravam `Resultado da
tentativa`, acrescentar um `update_contact_field` com `Canal que conectou` =
`Ligação WhatsApp` / `Ligação normal` / `Mensagem`, conforme o ramo. Sem isso, a
decisão D6 ("WhatsApp primeiro, ligação normal como segunda tentativa; com 3
ligações de WhatsApp não atendidas o lead passa a ter a ligação normal primeiro")
fica sem dado para ser avaliada depois — o projeto vai poder dizer que trocou de
canal, mas não qual canal funcionou.

> **Atualização de 23/09/2026 (G-21):** esta sugestão ficou incompleta depois
> que a §2.33.7 corrigiu a leitura da D10 (o campo é preenchimento manual do
> SDR, não lacuna de workflow) e o dono decidiu a pendência 9c. **Não aplicar
> este parágrafo ao pé da letra** — a versão atual, com o patch já escrito e
> a razão de ele não tocar o `Pós-ligação v2` ainda (sequenciamento com o
> `patch_remove_atendeu.py`/G-18, que mexe nos mesmos ramos `Atendeu`), está
> na §2.41. "Pronto quando" e acompanhamento: `ROADMAP-SALES-ENGAGEMENT.md`,
> G-21.

Rodar as três juntas:

```
python3 wesales/tools/auditoria_refs.py     # referência para workflow arquivado  (falha em achado)
python3 wesales/tools/auditoria_tags.py     # ciclo de vida das tags de estado    (falha em achado)
python3 wesales/tools/auditoria_campos.py   # mapa de escrita/leitura de campo    (nunca falha)
```

---

## 3. Workflow "Mestre de saída" — migrado para as 5 etapas reais em 18/09/2026

O guarda-costas da operação: garante que sair de `CONECTAR` limpa tudo.

**Mudança estrutural desta migração, não só troca de nome:** no plano de 7
etapas, toda saída de cadência (conectou, número errado, não ligar, 12
tentativas esgotadas) era um movimento de etapa — um `Opportunity Stage
Changed` cobria os quatro casos. Na tela real, só o primeiro continua sendo
movimento de etapa (`CONECTAR` → `REUNIÃO DE DIAGNÓSTICO` (antiga `AGENDAR`)); os outros três viraram `status`
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
| 4 | Remove Contact Tag | `fila-quente`, `fila-tel`, `fila-wa`, `fila-linkedin`, `atraso-1a-tentativa` (R-02), `reengajamento-ativo` (R-08), `pausado` (R-09), `fila-travada` (F-05, seção 2.21), `conectar-estagnado` (F-05, seção 2.22), `retorno-vencido` (F-05, seção 2.24 — rede de segurança; a limpeza normal roda no nó 3c do Pós-ligação, seção 4), `negociacao-estagnada` (F-13, seção 2.28), `proposta-pendente` (G-23, seção 2.28) |
| 5 | Add Contact Tag | `limpar-tarefas` |
| 6 | Add Note | `Saída de cadência · etapa: {{opportunity.pipeline_stage}} · status: {{opportunity.status}} · tentativa {{contact.tentativa_n}} · resultado {{contact.resultado_da_tentativa}}` |

**Nó 4, divergência conhecida do publicado (G-23, 23/09/2026):** o `Mestre
de saída v2` (`tools/patch_mestre_tags.py`, `PLANO-MULTICANAL.md` item A8)
já está no ar com uma lista maior que a linha acima — soma também
`cad-outbound`, `cadencia-12x30-p2`, `fechar-horario` e `toque`. Reconciliar
a lista inteira desta seção com o que está publicado é trabalho maior que
o achado de G-23 (que só cobria os dois alertas do closer); fica registrado
aqui para a próxima varredura de coerência que passar por este nó não
precisar redescobrir.

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
`REUNIÃO DE DIAGNÓSTICO` (Pós-agendamento move para `NEGOCIAR`) já cai fora da lista de
no-op do nó 1 e alcançaria o nó 4 sozinha, como `fila-travada`/
`conectar-estagnado`. Mas L-08 (`briefing-sdr.md`) registra que hoje não
existe caminho formal de desqualificar a partir de `REUNIÃO DE DIAGNÓSTICO` — se um dia
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
| ~~Pós-ligação, ramo `Atendeu`, nó 6 (`move para REUNIÃO DE DIAGNÓSTICO`)~~ — **exemplo retirado em 23/09/2026 (G-13):** desde a D3 do `PLANO-MULTICANAL.md`, o ramo `Atendeu` não move mais etapa (seção 4) — deixou de existir este segundo caso. A linha acima (Pós-agendamento) já sustenta sozinha a decisão de manter a lista nomeada em vez de `All Except Current Workflow` | — | — |

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
Atendeu move para `REUNIÃO DE DIAGNÓSTICO` — etapa deixa de ser `CONECTAR`, a condição já
fica falsa por esse lado sozinho. Progressões seguintes (`REUNIÃO DE DIAGNÓSTICO` →
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

#### Ramo `Atendeu` — reescrito em 23/09/2026 (G-13): a D3 do `PLANO-MULTICANAL.md` mudou o que este ramo faz, e esta seção nunca tinha acompanhado

> **O que havia aqui até 23/09/2026** dizia que o nó 6 movia a oportunidade
> para `REUNIÃO DE DIAGNÓSTICO` (antiga `AGENDAR`). Isso descrevia o desenho
> de 18/09/2026, anterior à decisão D3 do dono (`PLANO-MULTICANAL.md`,
> 22/09/2026: *"`Atendeu` não move mais de etapa. O lead fica em `CONECTAR`
> na fase 'fechar horário'... até agendar"*), executada e publicada em
> 23/09/2026 (E5-E7). A própria seção 2.31/F-16 deste arquivo já tinha
> auditado o comportamento novo por dump ao vivo (`Pós-ligação v2`, nós
> 13/26/77/86/97) e registrado a tag `fechar-horario` — só esta tabela
> continuava descrevendo o nó antigo. Contradição dentro do mesmo documento:
> quem lesse só esta seção montaria o ramo errado. Fonte da correção: a
> auditoria da seção 2.31 (dump `status: published`, versão 4) e
> `PLANO-MULTICANAL.md` E5-E7.

| # | Ação |
|---|---|
| 1 | If/Else | A tentativa foi de WhatsApp? (mesma checagem do nó 2) → Math: `Conexões WhatsApp` + 1. Senão → Math: `Conexões telefone` + 1 |
| 2 | Math: `Total de conexões` + 1 |
| 3 | Update: `WA não atendidas seguidas` = 0 |
| 4 | Add Contact Tag `conectado-hoje` |
| 5 | Add Contact Tag `fechar-horario` (estado "conectou, fechando o horário da reunião de diagnóstico" — seção 2.31/T-05 do `campos-e-tags.md`) |
| 6 | Remove Contact Tag `fila-tel`, `fila-wa` |
| 7 | Update/Create Opportunity → etapa **permanece** `CONECTAR` (sem mudança de etapa — é o que a D3 pede; confirmado no dump como `create_opportunity ... etapa:CONECTAR`, não como movimento para `REUNIÃO DE DIAGNÓSTICO`) |
| 8 | Update Contact Field `Data conectado` = `{{right_now}}` (R-03 — só marca; não repete se já preenchido, mas escrever de novo é barato e não quebra nada) |
| 8b | Date/Time Formatter | Entrada `{{right_now}}` · "To Format" = `HH` (só a hora, 00–23) — mecanismo de horário aprendido por segmento, seção 2.18, F-02 |
| 8c | Update Contact Field | `Hora da conexão` = saída do nó 8b |
| 9 | Add Task `[FECHAR HORÁRIO] Qualificar e agendar a reunião de diagnóstico` · vence hoje · Atribuir: `Contact Owner` (dinâmico, R-10) — título trocado do antigo `[CONECTADO] Qualificar e agendar`, confirmado no dump ao vivo |
| 10 | Add Note `Atendeu na T{{contact.tentativa_n}}` |

**O que este ramo não faz mais, e por quê:** não dispara mais o Mestre de
saída por mudança de etapa (§3, gatilho 1) — porque não há mudança de etapa.
A oportunidade só entra em `REUNIÃO DE DIAGNÓSTICO` pelo `Pós-agendamento v2`
quando a reunião é de fato marcada (D4). **Era pendência em aberto, não
resolvida por esta correção — precisada e fechada em G-18
(`ROADMAP-SALES-ENGAGEMENT.md`):** a `Cadência 12x30` já se auto-remove no
caso comum (nó 10 do próprio molde, `remove_from_workflow: este`, enquanto o
`Aguardar resultado` daquela tentativa ainda está ativo) — o que faltava era
a segunda linha de defesa que o ramo `Não ligar` já tem no `Pós-ligação v2`
(o dump não mostrava `remove_from_workflow` no ramo `Atendeu`), para o caso
em que a classificação chega fora da janela da tentativa ativa. Patch
escrito e validado por dump (não aplica sozinho — edição de workflow
publicado não sai por este conector): `wesales/tools/patch_remove_atendeu.py`,
`--dump` → `exit 0`. Falta só o dono rodar `--aplicar` ou aplicar pela
tela; detalhe completo em G-18.

O nó 9 (task) nasce para **toda** ligação atendida, sem olhar se a conversa
já mostrou que não há fit — é a lacuna **L-08** (`briefing-sdr.md`), fechada
pelo ramo `Desqualificado` abaixo (R-18): quem atende e claramente não serve
não deveria abrir tarefa de fechamento de horário nenhuma.

#### Ramo `Desqualificado` — novo nesta rodada, fecha L-08 (R-18)

O SDR atendeu a ligação (é uma conexão real, conta como tal), mas a própria
conversa já descartou o lead — sem fit, sem budget, é concorrente, já é
cliente, não fala com decisor. Hoje o único caminho para esse resultado é
classificar como `Atendeu` mesmo assim, o que cria a tarefa `[CONECTADO]
Qualificar e agendar` e empurra o lead para `REUNIÃO DE DIAGNÓSTICO` — o SDR então tem que
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
| 1 | Mover oportunidade → `NEGOCIAR` | Aciona o Mestre de saída (a etapa muda de `CONECTAR`/`REUNIÃO DE DIAGNÓSTICO` (antiga `AGENDAR`) para `NEGOCIAR` — tabela 1.0) |
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

## 5.5 Deduplicação entre canais (G-15) — por que isto **não** é um workflow

O Meta Lead Ads grava telefone; a `Qualificação por IA no WhatsApp`/Instagram
(seção 6) não tem telefone nem e-mail no perfil do contato. Um lead que
preencheu o formulário há meses, esfriou (`nutricao-90d`) e volta pelo
Instagram vira um **segundo contato**, com uma **segunda cadência**, sem
ninguém perceber que é a mesma pessoa — a fusão automática nativa (R-13, seção
1.3) só age na criação de um contato novo, nunca revisitando dois que já
existem separados.

**Por que não dá para resolver com um nó de workflow:** o GHL tem uma ação
nativa, `Merge Contact`, que funde duplicatas por Telefone, E-mail ou os dois
— mas o único gatilho do projeto que reage a mudança de campo, `Contact
Changed` (usado em 2.4/2.9/4.1/5.1), filtra hoje só por Usuário atribuído,
DND, Tag, Custom Field, Endereço e Website. **Telefone e e-mail não estão na
lista de campos filtráveis** — pedido em aberto no board de ideias da própria
HighLevel, sem previsão (`ideas.gohighlevel.com`, achado por citação repetida
em buscas com termos diferentes, mesmo padrão de confiança do G-05/R-14). Sem
esse gatilho, nada dispara o `Merge Contact` no momento em que um contato do
Instagram ganha telefone (ou vice-versa) — não é falta de desenho, é limite
de plataforma. Não tente resenhar isto como workflow numa próxima rodada.

**O que fazer em vez disso** (ferramenta nativa + rotina humana, mesmo padrão
de R-11/R-14 para o que workflow não alcança):
1. Tela → Configurações → Contatos → **Duplicate Management & Merge Tool**:
   agrupa por Nome, Telefone ou E-mail, funde até 10 de uma vez. Para um
   contato sem telefone nem e-mail (todo lead que só existe via Instagram), o
   único critério que serve é **Nome** — passível de falso-positivo (dois
   donos de negócio homônimos), então a fusão por Nome é revisada, nunca em
   lote automático.
2. SDR (`GUIA-SDR.md`): antes de tratar um handoff vindo do Instagram como
   "lead novo", buscar o nome/empresa na busca de contatos.
3. Gestor: rodar a Duplicate Management & Merge Tool por Nome uma vez por
   semana.

Zero campo, zero tag, zero workflow — item de rotina manual, não sai por API.

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
| Filtros | tag `fila-quente` presente **E** tag `nao-perturbe` ausente **E** etapa da oportunidade em (`CONECTAR`, `REUNIÃO DE DIAGNÓSTICO` (antiga `AGENDAR`)) — `Retorno agendado` some da lista de etapas porque não é mais etapa própria (tabela 1.0): quem pediu retorno já está em `CONECTAR`, coberto |
| Colunas | Nome · `Empresa` · Telefone · `Prioridade` · `Tentativa nº` · `Resultado da tentativa` · `Nota de qualificação` · Última atividade |
| Ordenação | `Prioridade` desc, depois `Tentativa nº` asc |

### 8.2 `Fila Telefone Hoje` — migrado para as 5 etapas reais em 18/09/2026
| Item | Configuração |
|---|---|
| Filtros | tag `fila-tel` presente **E** `nao-perturbe` ausente **E** `telefone-invalido` ausente **E** `conectado-hoje` ausente **E** etapa = `CONECTAR` ⚠️ **F-16 (seção 2.31): `conectado-hoje` nunca é removida e o `Atendeu` agora fica em `CONECTAR` — esta cláusula virou exclusão permanente. Não construir com o filtro como está.** |
| Colunas | Nome · `Empresa` · Telefone · `Tentativa nº` · `Prioridade` · `Resultado da tentativa` · Tarefas abertas |
| Ordenação | `Prioridade` desc, depois `Tentativa nº` asc |

Ordenar por tentativa crescente é de propósito: lead na T1 tem muito mais
chance de atender do que o da T11. A fila devolve primeiro o que converte.

### 8.3 `Fila WhatsApp Hoje` — migrado para as 5 etapas reais em 18/09/2026
| Item | Configuração |
|---|---|
| Filtros | tag `fila-wa` presente **E** `nao-perturbe` ausente **E** `conectado-hoje` ausente **E** `Permissão WhatsApp` = `Sim` **E** etapa = `CONECTAR` ⚠️ **Mesmo problema da 8.2 — F-16, seção 2.31.** |
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
as listas de saúde 8.20-8.24 já seguem. **Divergência conhecida do publicado
(G-23):** o workflow real espera 5 dias, não 3 — ver o aviso no topo da
seção 2.28. Esta lista ainda não foi montada na tela (só o workflow e a
tag saíram do papel, `PLANO-MULTICANAL.md` A5).

### 8.29 `Saúde — Proposta Pendente` — G-23
| Item | Configuração |
|---|---|
| Filtros | tag `proposta-pendente` presente |
| Colunas | Nome · `Empresa` · `Nota de qualificação` · `Data do veredito do closer` |
| Ordenação | `Data do veredito do closer` asc (quem foi qualificado há mais tempo sem ser movido para NEGOCIAR aparece primeiro) |

Espelho da 8.28: esta lista pega quem o closer qualificou (`Sim`) e não
moveu para `NEGOCIAR` em 3 dias; a 8.28 pega quem já está em `NEGOCIAR` e
não fecha. A tag só existe porque o workflow "Proposta Pendente"
(`tools/build_estagnacao.py`, seção 2.28) já esperou 3 dias e conferiu de
novo (tag `etapa-reuniao`, veredito) antes de aplicá-la. Ainda não montada
na tela — mesma pendência da 8.28.

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
(F-10 — e o silêncio de entrada já passa, por uma margem grande e crescente
a cada rodada, o maior intervalo que esta base já teve; número exato só na
leitura mais recente do F-10 em `ROADMAP-SALES-ENGAGEMENT.md`, para não
desatualizar aqui), não espera ninguém, e responde de lambuja a dúvida que
decide o desenho das outras sete. Anote o resultado da ordenação em
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
| Filtros | tag `nao-perturbe` presente **E** (`Calls & Voicemails DND` = Disabled **OU** `WhatsApp DND` = Disabled **OU** `Email DND` = Disabled) |
| Colunas | Nome · Telefone · Tags · `Resultado da tentativa` · Etapa/status da oportunidade |
| Ordenação | Data de criação do contato, desc (o mais recente primeiro — é o mais provável de ainda estar "quente" numa régua) |

**`Email DND` acrescentado em 22/09/2026 (G-07):** até aqui a lista só
cobria os dois canais que existiam quando o R-14 foi escrito — o e-mail só
virou canal real no F-15, no mesmo dia, e ninguém tinha voltado para
atualizar esta lista até agora. Mesmo raciocínio da correção de `E`→`OU`
abaixo: um contato com a tag e `Email DND` desligado (mas `Calls`/`WhatsApp`
ligados) é exatamente quem já foi protegido nos outros canais e continua
exposto no mais novo — o mesmo padrão "protegido num canal, exposto no
vizinho" que o G-06 e o F-14 já registraram para outras combinações.

Lista de exceção, não de volume: o alvo é sempre zero linha. Existe porque
`Set Contact DND` e `Add Contact Tag: nao-perturbe` nascem no mesmo nó em
quatro lugares diferentes do documento (2.9.5 — opt-out por palavra-chave no
WhatsApp, R-17; 2.9.6 — o mesmo para e-mail, G-07; seção 4 ramo `Não ligar`;
seção 6 nó 3 — a lista dizia "quatro" antes desta rodada citando "opt-out
por palavra-chave do R-17" como item **separado** do 2.9.5, quando são o
mesmo lugar; corrigido ao contar de novo para acrescentar o 2.9.6 de
verdade) — um deles aplicando só a
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
que o app correspondente está integrado à subconta.** Esta subconta **não
tinha WhatsApp integrado até 21/09/2026** (era a razão pela qual o R-14
esperava "volume real de mensagem" e pela qual não existia uma única
mensagem de WhatsApp aqui). **Desde 22/09/2026 tem** — a integração
não-oficial Stevo (QR), que o dono conectou e já gerou tráfego de teste real
(`APRENDIZADOS-CRM.md`; G-09 no roadmap). Se essa conexão faz o app
"WhatsApp" da subconta aparecer como integrado para o GHL (e portanto libera
o filtro `WhatsApp DND` na Smart List) é a mesma pendência de tela do item 1
abaixo — a Stevo não é o app nativo de WhatsApp do GHL, então não é certo
que conte. Duas consequências, e a segunda é de compliance, não de
montagem:

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
| O filtro `WhatsApp DND` aparece na Smart List hoje? | Se sim, montar as duas listas completas já. Se não, montar só com `Calls & Voicemails DND`/`Email DND` e completar a cláusula de WhatsApp no dia da integração |
| O filtro `Email DND` aparece na Smart List hoje? (acrescentado em 22/09/2026, G-07) | A mesma fonte que restringiu WhatsApp/Messenger/GMB a "depois da integração" não lista e-mail entre os três — é canal nativo do GHL, não um app conectável à parte, então o filtro deveria estar disponível desde sempre. **Não confirmado na tela** (mesma classe de "a fonte fala de outra plataforma, a palavra certa é da tela" já registrada no F-10/8.25) — se não aparecer, montar as duas listas só com `Calls`/`WhatsApp` e completar quando confirmado |

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
| Filtros | (`Calls & Voicemails DND` = Enabled **OU** `WhatsApp DND` = Enabled **OU** `Email DND` = Enabled) **E** tag `nao-perturbe` ausente |
| Colunas | Nome · Telefone · Tags · Etapa/status da oportunidade |
| Ordenação | Data de criação do contato, desc |

Espelho da 8.26, risco menor: o DND nativo já bloqueia o canal, então o
lead está protegido — mas a divergência ainda importa, porque aponta um
caminho que ligou DND sem passar pelo registro do projeto (ação manual na
tela, ou um nó de opt-out que este documento ainda não cobre). Uma linha
aqui não é emergência como na 8.26, é pista para achar o nó ou o clique
que a especificação atual não previu. **`Email DND` acrescentado em
22/09/2026 (G-07)**, mesmo motivo da 8.26: um lead que clicou no link de
descadastro nativo do GHL (o `{{unsubscribe}}` que todo e-mail da
plataforma já carrega) liga `Email DND` sem passar por nenhum workflow
deste projeto — exatamente o "caminho não documentado" que esta lista
existe para achar, e que a versão anterior (só Calls/WhatsApp) não tinha
como ver.

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
| ⚠ *(atualizado em 22/09/2026)* | *`Prazo` chega vazio do Meta — a resposta cai em `Urgência` — mas isso **não bloqueia mais o nó 4**: o Pós-agendamento v2 (montado no PC do dono, `dec3a20`) ganhou um bloco de reserva que lê `Urgência` com a mesma tabela de pontos sempre que `Prazo` vier vazio, e está publicado e provado rodando (`GUIA-MONTAGEM.md`, "93 por `Prazo`, 15 pelo bloco de reserva `Urgência`"). O que **segue** bloqueado, e é a metade real do G-04 que falta: `Investimento mensal em anúncios` recebe do Meta `Acima de 10k` / `Abaixo de 5k` / `Até R$ 1.000` / `Não invisto nada ainda` — só o primeiro é opção da tela, e os outros três nunca casam num `If/Else`, essa linha da tabela acima ainda soma 0 para 3 de cada 4 leads do Meta. Decisão do dono continua em aberto só para esta linha (`ROADMAP-SALES-ENGAGEMENT.md`, G-04; opções em `CONFERENCIA-CAMPOS.md`, Tabela H)* | — |

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
| 1 | Teste Atendeu | Atende na T1 | `Atendeu` → etapa `REUNIÃO DE DIAGNÓSTICO` (antiga `AGENDAR`) → agenda → etapa `NEGOCIAR` |
| 2 | Teste Não Atende | Nunca atende, vai até o fim | 12 tentativas → `status` `abandoned` (etapa fica em `CONECTAR` — tabela 1.0) + `nutricao-90d` |
| 3 | Teste Retorno | Pede retorno na T3 | `Pediu retorno` → permanece em `CONECTAR` (não é etapa própria — tabela 1.0), Prioridade 5 |
| 4 | Teste Número Errado | Número errado na T1 | `telefone-invalido` → `status` `abandoned` ou `lost` (etapa fica onde estava) |
| 5 | Teste Não Ligar | Pede para não ligar na T2 | `nao-perturbe` + **DND ligado** → `status` `lost` (etapa fica onde estava), nenhuma mensagem depois |

### Verificações, uma por linha
| # | O que testar | Como | Passou? |
|---|---|---|---|
| 1 | Entrada na cadência | Mover para `CONECTAR` cria tag `fila-tel` e tarefa `[CADENCIA] T1` | |
| 2 | Portão de etapa | Mover para `REUNIÃO DE DIAGNÓSTICO` no meio da espera: a tentativa seguinte **não** dispara | |
| 3 | Portão `nao-perturbe` | Aplicar a tag na mão: próxima tentativa não dispara | |
| 4 | Portão `telefone-invalido` | Aplicar a tag: tentativa de telefone não dispara, de WhatsApp sim | |
| 5 | Limpeza do resultado | Na T2, `Resultado da tentativa` chega vazio (não herda o da T1) | |
| 6 | `Atendeu` | Registrar: conexões +1, `conectado-hoje` aplicada, etapa `REUNIÃO DE DIAGNÓSTICO`, tarefa `[CONECTADO]` criada, saiu da cadência | |
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
| 25 | Funil por marco | No Teste Atendeu: `Data conectado` grava ao entrar em `REUNIÃO DE DIAGNÓSTICO`, `Data agendado` grava ao agendar, e marcar o agendamento como `Showed` grava `Data compareceu` — os três aparecem nas listas 8.10 a 8.12 no mês corrente | |
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
| 36 | Desqualificação instantânea (R-18) | Num 7º contato de teste em `CONECTAR`, classifique `Resultado da tentativa` = `Desqualificado` + `Motivo da desqualificação` = `Sem fit`: confirme `Conexões telefone`/`Total de conexões` subindo (é conexão real), `conectado-hoje` aplicada, `fila-tel`/`fila-wa` removidas, `status` indo para `lost` **sem** a oportunidade sair de `CONECTAR` (não vai para `REUNIÃO DE DIAGNÓSTICO`) e **nenhuma** tarefa `[CONECTADO] Qualificar e agendar` nascendo. Repita com `Motivo da desqualificação` = `Timing errado`: confirme `status` `abandoned` + tag `nutricao-90d` em vez de `lost` | |

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
tela e pelo dono. **Duas das três já resolveram (22/09/2026):** o dono
confirmou ao vivo que as ligações saem por LC Phone (`APRENDIZADOS-CRM.md`,
"Resposta do dono à pré-condição do W20"), e os quatro campos já existem na
tela (`APRENDIZADOS-CRM.md`, "Os 4 campos do W20"). **Só a decisão de
gravar segue sem `[x]`** — é ela, sozinha, que trava o teste deste item e a
montagem do W20 agora.

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

---

## 2.35 `_frescor.py` — a guarda de dump velho estava em uma das três auditorias, e as três leem os mesmos dumps

Em 23/09/2026 a `auditoria_tags.py` ganhou duas guardas de frescor, depois de
ela ter reportado 5 achados lendo um dump de 22/09 16:27 — e 3 deles já
estavam resolvidos na conta havia uma hora. A correção funcionou, mas ficou
onde o erro tinha acontecido, e não onde ele pode acontecer:

| auditoria | lê dumps de `wesales/workflows-json/` | avisava de dump velho |
|---|---|---|
| `auditoria_tags.py` | sim | sim |
| `auditoria_refs.py` | sim | **não** |
| `auditoria_campos.py` | sim | **não** |

As três respondem perguntas diferentes sobre exatamente o mesmo material. Um
dump 28 h atrasado engana a `refs` ("este workflow aponta para um arquivado")
e engana a `campos` ("ninguém escreve neste campo") do mesmo jeito que enganou
a `tags`. Quem rodasse só uma das duas sem aviso não tinha como saber.

As duas funções saíram da `auditoria_tags.py` para o módulo
`wesales/tools/_frescor.py`, e as três auditorias passaram a chamar
`aviso(DUMPS)` como primeira linha do `main()`:

1. **`backup_mais_novo`** — prova direta: existe backup irmão em `_antes-*/`
   com `updatedAt` mais novo que o arquivo principal? Então alguém aplicou
   patch na conta e não re-exportou. Só enxerga workflow que tem backup irmão.
2. **`muito_atras`** — heurística: o arquivo está 12 h ou mais atrás do mais
   novo da pasta? Não prova nada (workflow que ninguém toca há dias aparece
   aqui, e é correto que apareça), mas pega o caso que a (1) não vê. Foi assim
   que apareceu o `AGENDAR Estagnado`, dizendo `published` com dump de 28 h
   antes, depois de o dono já tê-lo despublicado.

Saída de hoje, idêntica nas três: 7 dumps possivelmente defasados (`ZZ TESTE
API` 31 h, `ZZ TESTE W6` 29 h, `AGENDAR Estagnado`, `Alerta de Speed-to-lead`,
`Contador de Toques` e `Lead Esquecido em NOVO LEAD` 28 h, `Fila Travada`
27 h), e 0 com backup irmão mais novo.

Nenhum resultado de auditoria mudou com a refatoração: `tags` continua sem tag
de limpeza pulada sem segunda rede, `refs` sem referência para arquivado, e
`campos` com os mesmos 4 campos nem escritos nem lidos (`Canal que conectou`,
`Hora da conexão`, `Hora do retorno`, `Necessidade`). As três continuam
saindo com código 0.

A lição que o módulo carrega no próprio docstring, para não se perder de novo:
**achado tirado de dump é CANDIDATO, não item** — só vira item depois de
confirmação ao vivo, pela API ou medindo o efeito.

---

## 2.36 A pendência 9d estava superestimada: os 10 alvos já estavam consertados, e o que faltava era o guarda

A pendência que eu vinha reportando como "3 linhas no `traduz()` e trocar o
`ALVOS` fixo por varredura" sugeria defeito vivo. Fui medir antes de mexer, e
não havia:

| o que eu afirmava | o que a medição mostra |
|---|---|
| a lista fixa de 10 pode estar escondendo workflow com o defeito | os 10 já estão consertados: **49 condições em 28 segmentos**, zero restantes, provado pelos backups de `_antes-patch-condicoes/` |
| a tabela de tradução incompleta é um bug | ela **nunca traduziu errado**: padrão desconhecido cai em `falhas`, e `falhas` bloqueia o `PUT` — era limite para o futuro |
| a varredura acharia coisa hoje | acha **um**: `ZZ TESTE 12X30`, rascunho, a cópia de teste que existe justamente para exibir o defeito |

Os 7 workflows publicados que ainda testam condição de oportunidade têm
gatilho `pipeline_stage_updated` ou `opportunity_status_changed` — ali a
condição funciona e está certo estar ali.

### O que era problema de verdade

Não o passado, o futuro. Workflow criado amanhã, com gatilho de tag e
condição de etapa, nasce com o mesmo defeito **silencioso** — o ramo nunca
roda, não dá erro, não aparece em lugar nenhum — e uma lista de 10 nomes
escrita ontem não o vê. Faltava o guarda, não o conserto.

### `auditoria_condicoes.py` — a quarta auditoria

Somente leitura, roda sem API e sem PC, pelos dumps. Classifica cada workflow
que testa condição de oportunidade em `if_else`:

| classe | critério | código de saída |
|---|---|---|
| **defeito** | `published`, não-`ZZ TESTE`, com algum gatilho que não carrega oportunidade | **1** |
| aviso | mesmo padrão em `draft` ou `ZZ TESTE*` | 0 |
| correto | todos os gatilhos carregam oportunidade | 0 |

Isto desfaz uma afirmação errada que eu havia registrado: **os dumps carregam
os gatilhos**. O `g.export` grava `{"workflow": ..., "triggers": ...}`, e eu
tinha anotado `triggers: []` em todo dump. A classificação de gatilho desta
auditoria não é chute — é leitura.

Saída de hoje: 38 dumps, 9 testam condição de oportunidade, **0 defeitos em
publicado**, 1 aviso (`ZZ TESTE 12X30`, rascunho, 6 segmentos), 8 corretos.

### `patch_condicoes_etapa.py` — varredura no lugar da lista

`ALVOS` saiu. O alvo passa a ser varrido ao vivo: workflow publicado com
algum gatilho sem oportunidade e ao menos uma condição de oportunidade em
`if_else`. `--incluir-teste` traz rascunho e `ZZ TESTE*`; `--alvo NOME`
restringe a um; sem `--aplicar` só imprime.

A `Cadência 12x30` (parte 1) ficou num conjunto `NUNCA` explícito, com o
motivo registrado: gatilho de etapa, a condição funciona e a troca criaria
corrida com o Espelho no instante da entrada. A varredura imprime que a
pulou — decisão tomada não se reverte calada.

A tabela de tradução passou de 3 para 8 padrões:

| condição | tag do Espelho |
|---|---|
| etapa == `NOVO LEAD` (+ status open) | `etapa-novo-lead` |
| etapa == `CONECTAR` | `etapa-conectar` |
| etapa == `REUNIÃO DE DIAGNÓSTICO` | `etapa-reuniao` |
| etapa == `NEGOCIAR` | `etapa-negociar` |
| etapa == `FORMALIZAR` | `etapa-formalizar` |
| status == `abandoned` | `status-nutricao` |
| status == `lost` | `status-perdido` |
| status == `won` | `status-ganho` |

**Nenhuma tag nova.** As oito já existem e estão publicadas — o dono as criou
no `61eb167`, e o `Espelho de Etapa` (publicado, v4) é quem as mantém. Por
isso esta mudança não precisa de linha no `APROVADO.md`: o script sabe
traduzir para mais coisas, e não cria nada.

### Regressão medida, não deduzida

Rodei a tabela nova contra os 10 backups pré-patch, offline:

| | resultado |
|---|---|
| trocas | 28 segmentos, 49 condições — idêntico ao patch original |
| falhas | 0 |
| condições de oportunidade restantes | 0 em todos os 10 |
| segmento com duas etapas | devolve `None`, cai em `falhas`, não troca |

Zero escrita na conta: o patch não foi executado, e sem `--aplicar` ele não
escreve. O que vai para a conta continua sendo decisão do dono.

---

## 2.37 O portão de capacidade da `Cadência Inbound` — patch escrito e validado, esperando o dono (9e / F-05)

O `GUIA-SDR.md`, linhas 74–76, promete ao SDR **sem ressalva**: "se você
passar de 100 toques no dia ou tiver 50 ou mais tarefas vencidas, o sistema
segura os toques novos". Na `Cadência 12x30` isso é verdade. Na `Cadência
Inbound` é falso — e lead de anúncio é justamente quem mais entra.

### Contado nó a nó, não estimado

| portão | 12x30 p1 | 12x30 p2 | Inbound |
|---|---|---|---|
| `Teto de toques da semana?` (campo `c1xuCuLyJheHOQoJ3grH` ≥ 6) | 6 | 6 | **0** |
| `SDR lotado?` (tag `sdr-lotado`) | 6 | 6 | **0** |

Os 5 toques da Inbound (TI1–TI5) têm `Lead pausado?` e `Ainda vale ligar?`,
mas **nada que olhe capacidade**. A `faxina_tarefas.py` (197-213) aplica
`sdr-lotado` e a Inbound nunca lê a tag.

**Correção de um número meu:** eu vinha dizendo "portar os 6 nós". Errado. São
2 portões × 5 toques = **10 portões lógicos**, e cada portão lógico são **5
nós** (`if_else` + `Branch` + `None` + `wait` + `goto`, o `goto` voltando ao
próprio portão — é o `wait`+`goto` que *segura* o toque). São **50 nós**, de
272 para 322. Por isso isto é script, não clique.

### `patch_portao_inbound.py`

Não monta nó à mão: **clona** o grupo de 5 nós que já existe e já funciona na
`Cadência 12x30 — parte 2`, remapeando todo uuid que aparece dentro do grupo
(`id`, `next`, `parent`, `parentKey`, `branches[].id`, `__segmentId`,
`__conditionId`, `goto.targetNodeId`). Os atributos vão byte a byte iguais ao
que o GHL já aceitou — nenhum `nestedDropdownTypes` inventado, nenhum campo
faltando. É a lição do `build_*` aplicada ao contrário: em vez de reproduzir a
especificação, copiar o que a plataforma já validou.

Ordem resultante em cada toque, igual à do 12x30:

```
Lead pausado?  ->  Teto de toques da semana?  ->  SDR lotado?  ->  Ainda vale ligar?
```

### Validado antes de existir aprovação

O modo `--dump` roda em qualquer máquina, **sem token e sem rede**: lê
`wesales/workflows-json/`, monta o resultado em memória e passa pelas mesmas
conferências do caminho ao vivo. Medido em 23/09/2026:

| conferência | resultado |
|---|---|
| nós | 272 → 322 (+50, exatamente 10 por toque) |
| ids repetidos | nenhum |
| `parentKey` órfão | nenhum |
| `goto` apontando para nó inexistente | nenhum |
| cada portão aparece | 5× |
| cadeia por toque | a ordem acima, nos 5 toques |
| condição dos clones vs. doador | idêntica nos 10 |
| uuid do doador vazado para o alvo | nenhum |

### A única escolha de desenho, que é sua

Os parâmetros foram copiados do 12x30: teto semanal `≥ 6` esperando **1 dia**,
`sdr-lotado` esperando **1 hora**. O `Lead pausado?` da Inbound espera 30 min
— a Inbound é mais apertada de propósito, e não mexi nele. Copiei o tempo do
12x30 nos dois portões novos porque o que eles esperam é o mesmo: um contador
de semana e uma sobrecarga de dia. Se a Inbound deve ter teto próprio (mais
folgado, porque lead que acabou de levantar a mão esfria mais rápido), é aí
que muda.

### Não precisa de `APROVADO.md`, mas precisa de você

Nenhuma tag nova, nenhum campo novo — `sdr-lotado` e `c1xuCuLyJheHOQoJ3grH` já
existem e o 12x30 já os lê. Mas isto **altera um workflow publicado que toca
lead real**, então `--aplicar` só roda depois de você ver o plano. E **não sai
por MCP**: o conector não cria nem edita workflow. São dois caminhos:

**Caminho A, o script (recomendado).** Do seu PC, na pasta `wesales/tools/`:

```
python patch_portao_inbound.py --dump      # confere sem rede, deve dar 272 -> 322
python patch_portao_inbound.py             # mesmo plano, agora contra a conta ao vivo
python patch_portao_inbound.py --aplicar   # grava, com backup em _antes-portao-inbound/
```

O `--aplicar` faz backup antes, grava, relê da API e imprime status, contagem
de nós, gatilhos ativos e quantas vezes cada portão aparece ao vivo. Se
qualquer conferência falhar, ele não grava.

**Caminho B, na tela.** Possível, mas são 50 nós — 10 repetições de cinco
cliques. Para cada toque TI1…TI5, no ramo **Não** (`None`) do `TI{n} · Lead
pausado?`, antes do `TI{n} · Ainda vale ligar?`:

1. **Condição** `TI{n} · Teto de toques da semana?` → campo personalizado
   `Toques na semana` **maior ou igual a** `6`.
2. No ramo **Sim** dela: **Esperar** `1 dia` → **Ir para** essa mesma condição.
3. No ramo **Não** dela: **Condição** `TI{n} · SDR lotado?` → tag
   `sdr-lotado` **está presente**.
4. No ramo **Sim** dela: **Esperar** `1 hora` → **Ir para** essa mesma condição.
5. O ramo **Não** dela segue para o `TI{n} · Ainda vale ligar?` que já existia.

Repetido 5 vezes. O `Ir para` apontando para o próprio portão é o que segura o
lead sem perdê-lo — sem ele, o toque é descartado em vez de adiado.

Zero escrita na conta nesta seção: o patch não foi executado, e sem
`--aplicar` ele não escreve.

---

## 2.38 O 9e não era um caso, eram três — e o pior deles ignora a pausa do próprio SDR

Escrevi o patch do §2.37 e então fiz a pergunta que devia ter vindo antes:
**achei o 9e à mão, então o que mais está lá que eu não olhei?** A resposta são
duas cadências além da Inbound.

### A invariante, não a comparação

A tentação era comparar cadência com cadência ("a Inbound tem menos portões que
a 12x30"). Isso daria alarme falso em cada diferença legítima de desenho. A
pergunta certa é uma invariante:

> **Se um toque coloca o lead na fila (`fila-tel` / `fila-wa`) ou conta `toque`,
> ele consome capacidade do SDR — logo a cadência tem de ler os três portões.**

| portão | lê |
|---|---|
| `Lead pausado?` | tag `pausado` |
| `SDR lotado?` | tag `sdr-lotado` |
| `Teto de toques da semana?` | campo `c1xuCuLyJheHOQoJ3grH` |

### O que a invariante achou

| cadência | toques | marca | `pausado` | `sdr-lotado` | teto semanal |
|---|---|---|---|---|---|
| `Cadência 12x30` | 6 | fila-tel, fila-wa, toque | 6/6 | 6/6 | 6/6 |
| `Cadência 12x30 — parte 2` | 6 | fila-tel, fila-wa, toque | 6/6 | 6/6 | 6/6 |
| **`Cadência Inbound`** | 5 | fila-tel, fila-wa, toque | 5/5 | **0** | **0** |
| **`Recuperação de No-show`** | 3 | fila-tel, toque | ok¹ | **0** | **0** |
| **`Reengajamento 90 dias`** | 4 | fila-tel, fila-wa, toque | **0** | **0** | **0** |
| `Nutrição — WhatsApp 15 dias` | 6 | — não consome | — | — | — |
| `Fechar Horário` | 2 | — não consome | — | — | — |

¹ lê `pausado` dentro do `NS{n} · Ainda vale recuperar?`, nos 3 toques. Ler é o
que importa; o nome do nó é rótulo.

O `Reengajamento 90 dias` é o pior: publicado, 105 nós, e as strings `pausado`,
`sdr-lotado` e `c1xuCuLyJheHOQoJ3grH` aparecem **0 vezes em todo o workflow** —
nem por toque, nem no portão de entrada (que checa `status-nutricao`,
`nutricao-90d` e `nao-perturbe`). Seus 4 toques fazem
`add_contact_tag ['fila-tel']` e `add_contact_tag ['toque']`.

Duas consequências, e a segunda é mais feia que a primeira:

1. **O `pausado` do SDR não vale ali.** É a pausa que o SDR aplica à mão; a
   cadência que mais mexe com lead frio é a única que não a lê.
2. **Enche o contador que trava os outros.** Cada toque marca `toque`, que
   alimenta o `c1xuCuLyJheHOQoJ3grH` que os portões da 12x30 leem. O
   Reengajamento **gasta** a cota semanal sem nunca **respeitá-la** — ele
   aperta o freio dos outros e passa livre.

### `auditoria_portoes.py`

Somente leitura, roda sem API, verifica a invariante. Detecção por **conteúdo**,
não por nome de nó — foi o que evitou acusar o `Recuperação de No-show`
injustamente. Cobertura por toque entra como informação; portão em 0 de N é o
que falha. `published` e não-`ZZ` falha com código 1; rascunho e teste são
aviso. Hoje: **3 cadências publicadas em falha**, exit 1.

A primeira versão dava um alarme falso próprio — imprimia "portão em 0/3
toques" para o `Recuperação de No-show`, que lê `pausado` sob outro nome.
Consertado antes de virar item: auditoria que grita sobre o que está certo
treina a gente a ignorar auditoria, e isso valia para ela mesma.

### O que isto muda no que está pendente

A pendência 9e cresceu e mudou de forma. Não é "portar 2 portões para 1
cadência", é **decidir a regra** e aplicá-la a três:

| cadência | o que falta |
|---|---|
| `Cadência Inbound` | `sdr-lotado` + teto — patch pronto e validado, §2.37 |
| `Recuperação de No-show` | `sdr-lotado` + teto (o `pausado` já está) |
| `Reengajamento 90 dias` | os três |

E há uma pergunta de desenho que é sua, porque as duas respostas são
defensáveis: **no-show e reengajamento devem respeitar o teto semanal, ou são
prioritários sobre lead novo?** Quem marcou reunião e não apareceu é mais
quente que lead de anúncio — pode fazer sentido que furem a fila de propósito.
Se for isso, o conserto não é portar portão: é **tirar o `add_contact_tag
['toque']`** dessas cadências, para elas não gastarem uma cota que não
respeitam. São desenhos opostos e eu não escolho por você.

`patch_portao_inbound.py` cobre só a Inbound. Estendê-lo para as outras duas é
mecânico depois de a regra estar decidida — os `TOQUES` e o `ALVO` são
parâmetro.

Nada foi escrito na conta: as duas auditorias são somente leitura e o patch não
foi executado. Achado tirado de dump é **candidato**: confirma-se lendo os três
workflows ao vivo, ou medindo — contato com `pausado` que ainda recebe
`fila-tel`.

---

## 2.39 `auditoria_tudo.py` — o alarme falso tem um gêmeo, e ele também treina a ignorar

São cinco auditorias, cada uma com seu comando, e nenhuma sabe das outras.
Duas dores, e a segunda é a que importa.

**Rodar 3 de 5.** Rodada que esquece uma auditoria não percebe que esqueceu.

**Repetir o que já foi dito.** Em 23/09 eu reportei 5 achados de tag como
trabalho novo e 3 já estavam resolvidos havia uma hora — o `_frescor.py`
consertou esse lado. Mas existe o lado oposto, e ele é igualmente corrosivo:
**achado real, já reportado, já na fila do dono, reapresentado a cada rodada
como se fosse novidade.** Isso treina o dono a ignorar o relatório tão bem
quanto o alarme falso treina. As cinco auditorias, rodadas de hora em hora,
iam reimprimir os mesmos 4 campos e as mesmas 3 cadências para sempre.

### A linha de base

`auditoria-base.json` guarda, por auditoria, **quantos achados existem hoje e
por quê**. O relatório compara:

| comparação | leitura |
|---|---|
| contagem `==` base | conhecido, já na fila do dono — não é novidade |
| contagem `>` base | **NOVO** — o único caso que pede atenção, exit 1 |
| contagem `<` base | **CONSERTADO** — notícia boa, exit 2, e manda atualizar a base |

A base é commitada de propósito. Quando o dono decide e alguém conserta, a
base muda **no mesmo commit do conserto**, e quem lê o diff vê as duas coisas
juntas. Base que ninguém atualiza vira mentira — por isso o exit 2 quando a
contagem cai: o script cobra a atualização em vez de aceitar silenciosamente.

O campo `porque` é o que transforma um número em informação. Hoje:

| auditoria | achados | por quê |
|---|---|---|
| `refs` | 0 | — |
| `tags` | 0 | — |
| `campos` | 4 | `Canal que conectou` (é a 9c), `Hora da conexão`, `Hora do retorno`, `Necessidade` — os três últimos o SDR preenche na tela |
| `condicoes` | 0 | — |
| `portoes` | 3 | as três cadências do §2.38, aguardando **uma** decisão do dono |

### Verificado nos três caminhos

Não confiei em ler o código: mexi na base e conferi o comportamento.

| cenário | resultado |
|---|---|
| base `portoes=1`, real 3 | `*** NOVO: 2 a mais que a base ***`, exit **1** |
| base `portoes=5`, real 3 | `CONSERTADO: 2 a menos`, manda gravar base, exit **2** |
| base igual ao real | `conhecido, já na fila do dono`, exit **0** |

O aviso de frescor também foi consolidado: em vez de repetir o bloco cinco
vezes, o relatório resume numa linha (hoje: 7 dumps possivelmente defasados, 0
com backup irmão mais novo), porque o `_frescor.py` imprime o mesmo nas cinco.

### Consequência prática

O check-in horário passa a rodar **um** comando em vez de listar auditorias que
podem ficar desatualizadas na lista:

```
python3 wesales/tools/auditoria_tudo.py
```

Exit 0 significa literalmente "nada novo desde a última vez que o dono foi
informado". Exit 1 é a única coisa que merece interromper alguém.

---

## 2.40 Um terço do meu achado do §2.38 era sobre um workflow morto — e a falha que deixou passar não é a que o `_frescor.py` pega

O dono decidiu o G-17 na **opção (A)**: no-show e reengajamento respeitam o
teto semanal. E na mesma rodada apareceu que **o `Reengajamento 90 dias` não
existe mais** — foi substituído pela Nutrição em 22/09, e o dump foi para
`_arquivo/` no commit `5659ac2`.

Então o pior dos três casos que eu reportei no §2.38 era sobre um workflow que
não roda. Eu escrevi que "a cadência publicada que mais mexe com lead frio é a
única que não lê a pausa do SDR". **Os números estavam certos e a conclusão
estava errada:** as três strings realmente apareciam 0 vezes naqueles 105 nós,
mas nenhum lead passava por lá.

### Por que o guarda de frescor não pegou

Esta é a parte que vale guardar, porque é uma classe nova. O
`_frescor.py` compara **datas**: dump velho contra backup irmão, dump velho
contra o mais novo da pasta. O `Reengajamento 90 dias` **não estava velho** —
estava aposentado. Um workflow substituído não envelhece o arquivo dele.

| o que o dump dizia | o que era verdade |
|---|---|
| `status: published` | o workflow foi trocado pela Nutrição em 22/09 |
| `updatedAt` recente | o arquivo não era antigo; o workflow é que morreu |
| estava em `workflows-json/` | ninguém tinha movido para `_arquivo/` ainda |

**A regra que faltava:** as auditorias tratam "arquivo na pasta viva" como
"workflow vivo". A única marca do projeto para o contrário é a pasta
`_arquivo/`, e ela depende de alguém mover o arquivo na hora em que
desativa o workflow — o que é justamente o passo que se esquece.

A `auditoria_refs.py` já sabia disso (ela existe para achar referência a
workflow arquivado). As outras quatro não sabiam. Depois que o `5659ac2` moveu
o arquivo, a `auditoria_portoes.py` parou de reportá-lo sozinha, porque ela
varre `workflows-json/*.json` e não desce em `_arquivo/`. O conserto de fundo,
que exige API e não sai daqui, é cruzar a lista de dumps com a lista de
workflows da conta: dump que diz `published` e não aparece na conta é dump
aposentado, e nenhuma data revela isso.

### O que a linha de base fez

Ela funcionou como desenhada, e vale registrar porque foi o primeiro uso real:
a contagem de `portoes` caiu de 3 para 2, e o `auditoria_tudo.py` **não aceitou
em silêncio** — saiu com código 2, imprimiu `CONSERTADO: 1 a menos que a base`
e cobrou `--gravar-base` no mesmo commit. Sem isso, a base ficaria dizendo 3
para sempre e a próxima queda real passaria como "conhecido".

Base atualizada neste commit: `portoes` 3 → **2**.

### O que sobrou do §2.38, medido de novo

| cadência | situação |
|---|---|
| `Cadência Inbound` | falta `sdr-lotado` + teto — `patch_portao_inbound.py`, validado, espera `--aplicar` |
| `Recuperação de No-show` | falta `sdr-lotado` + teto — `patch_portao_noshow.py` (escrito pela sessão paralela), validado, espera `--aplicar` |
| ~~`Reengajamento 90 dias`~~ | **morto desde 22/09**, arquivado; não é achado |

A invariante do §2.38 segue válida e os outros dois casos seguem reais. O que
muda é o tamanho: **dois**, não três, e os dois já têm patch pronto.

### E o 9c saiu decidido junto

**Automático onde o ramo já sabe, manual no resto.** Falta o patch no
`Pós-ligação v2` e nos ramos de resposta do WhatsApp. Até ele entrar, o
`Canal que conectou` continua aparecendo na `auditoria_campos.py` — o que está
certo, e agora está escrito no `porque` da base para ninguém reportar como
novidade.

---

## 2.41 `patch_canal_conectou.py` — a metade automática do 9c, e por que ela para antes do `Pós-ligação v2`

Você decidiu o 9c: **automático onde o ramo já sabe, manual no resto.** Este é
o patch da parte automática que não depende de mais nada.

O campo `Canal que conectou` (`TxJmoWdkA8rTqC1uEsMW`, `SINGLE_OPTIONS`:
`Ligação WhatsApp` / `Ligação normal` / `Mensagem`) existe desde 23/09 01:06 e
**nenhum workflow escreve nele** — é por isso que ele aparece na
`auditoria_campos.py` como "nem escrito nem lido".

### Onde grava, e só aqui

| workflow | ramo | grava |
|---|---|---|
| `Interceptação de Sinal — Resposta v2` | sinal quente | `Mensagem` |
| `Triagem da Nutrição` | `Quer conversar?` ("1") | `Mensagem` |

### O que fica fora, de propósito

Isto é a parte que importa, porque a tentação é gravar em tudo que tem gatilho
de resposta:

- **`Opt-out por Palavra-chave`** também é `customer_reply`, mas "pare de me
  mandar mensagem" **não é conexão comercial**. Contar isso encheria justamente
  a métrica que o campo existe para responder.
- **`Triagem`, ramos "2 agora não" e "3 sem interesse"**: são respostas, não
  conexões que levam a conversa. O "3" já liga o DND. Somar os três inflaria a
  conta pelo mesmo motivo do opt-out.

### E o `Pós-ligação v2`, que sabe o canal e ficou de fora

Ele **entra** na parte automática — o ramo sabe: testa `fila-wa` logo depois do
`Resultado da tentativa`, e presente significa ligação por WhatsApp, ausente
ligação normal. Mas ficou para depois **por sequenciamento, não por dúvida**:

> a sessão paralela tem o `patch_remove_atendeu.py` ainda sem `--aplicar`,
> inserindo nos **mesmos ramos `Atendeu`**. Dois patches montados a partir de
> leituras diferentes se atropelam — um sobrescreve o outro.

Ordem correta: aplicar o `patch_remove_atendeu.py`, re-exportar o dump, depois
estender este patch. Registrado no docstring para quem pegar isto depois.

### Por que quase não cria nó

30 nós deste projeto já gravam **vários** campos num único
`update_contact_field` (a `Cadência 12x30 — parte 2` grava três de uma vez),
logo a forma é aceita pelo GHL. Onde o ramo já tem um `update_contact_field`,
o patch **só acrescenta o campo ao array `fields` que existe**: zero nó novo,
zero religação de cadeia, zero risco de quebrar o fluxo. Só cria nó onde o ramo
não tem nenhum — hoje, um caso.

| workflow | como | nós |
|---|---|---|
| `Resposta v2` | campo acrescentado ao nó `003eb01e`, que já gravava `Sinal recebido` | 18 → **18** |
| `Triagem da Nutrição` | nó novo depois do `add_contact_tag` do `reengajado` | 37 → **38** |

### Medido, incluindo o que eu afirmei sobre ele

| conferência | resultado |
|---|---|
| `--dump` nos dois | conferência ok, exit 0 |
| campo gravado por workflow | exatamente **1x** |
| `next` quebrado / `parentKey` órfão | nenhum / nenhum |
| **idempotência** (aplicar 2x) | 2ª passada não faz nada: mesmos nós, campo 1x |
| forma do campo | `{"field": "TxJmoWdkA8rTqC1uEsMW", "value": "Mensagem", "title": "Canal que conectou", "type": "select", "date": ""}` |

A idempotência não ficou só afirmada no docstring — rodei duas vezes e conferi
que a segunda não duplica nem mexe na contagem de nós. Importa porque edição de
workflow publicado costuma ser rodada mais de uma vez, entre tentativas.

Zero escrita na conta: sem `--aplicar` o patch não escreve, e ele não foi
executado. O campo continua contando na `auditoria_campos.py` até você rodar.

## 2.42 O L-07 medido lead por lead: os 48 nunca entraram na cadência, e a tag `cad-inbound` diz o contrário

**Isto não é achado novo.** A lacuna já tem nome desde o `briefing-sdr.md`
(**L-07**, "não existe gatilho que promova `NOVO LEAD` → `CONECTAR`") e item
próprio no `ROADMAP-SALES-ENGAGEMENT.md` (**G-03**, 47 leads medidos em
22/09/2026, *aguardando decisão do dono*). O que esta seção acrescenta é
medição ao vivo pela API — não mais leitura de dump — e uma correção de
mecanismo: o que eu e os documentos dizíamos estava certo no efeito e **errado
no motivo**.

### O que eu media antes, e o que medi agora

| antes (22/09, dump + contagem) | agora (23/09 21:29 UTC, API) |
|---|---|
| "47 leads parados em `NOVO LEAD`, envelhecendo" | **49** — entraram 2 depois (nenhum de anúncio) |
| "ainda não em cadência" | **nunca entraram na cadência**, e a razão é o gatilho, não o portão |
| nada dito sobre o que aconteceu com cada um | **zero tarefa, zero mensagem** nos 3 conferidos um por um |

### O mecanismo, exato

O gatilho da `Cadência Inbound` (`jecAUagw3f4V4Lujd4rG`, ativo) não é "lead de
inbound chegou". É:

```
type: pipeline_stage_updated
  opportunity.pipelineId      == 0Fo2xbeayE4EP6yuSUtq   (FUNIL DE VENDAS)
  opportunity.pipelineStageId == deb60542-…              ("Movido para o estágio" = CONECTAR)
```

E a `Porta de Entrada` cria a oportunidade em `NOVO LEAD`:

```
create_opportunity  pipeline_stage_id: 7ae9c950-…  (NOVO LEAD)  status: open
```

Varri os 38 dumps procurando quem move oportunidade de etapa: os únicos
`create_opportunity` da `Cadência Inbound` que apontam para `CONECTAR` são as
**saídas** dela (`status: abandoned` → nutrição, `status: lost`). **Nenhum
workflow da subconta move `NOVO LEAD` → `CONECTAR` com `status: open`.**

Consequência: o lead que entra pela porta fica numa etapa que nenhum gatilho
escuta. Não é que a cadência o pegou e o portão o barrou — **a cadência nunca
foi acionada para ele.** Os cinco `TIn · Ainda vale ligar?` também exigem
`pipelineStageId == CONECTAR` (segmento com `operator: and`, primeira condição),
mas isso é *coerente* com o gatilho, não um segundo defeito.

### A tag que mente

Os 48 carregam `cad-inbound`. O nome se lê como "está na Cadência Inbound"; o
que ela significa é "entrou pela porta de inbound" — ela é aplicada pela `Porta
de Entrada` e **lida** pelo primeiro `if_else` da cadência (`É lead de
inbound?`). Um lead com `cad-inbound` e sem toque nenhum não é contradição: é o
estado normal enquanto a L-07 estiver aberta. Foi por isso que a contagem de
tags não delatou o problema antes — `fila-tel`, `fila-wa` e `fila-quente`
aparecem **1x cada** entre os 49, e eu poderia ter lido isso como "filas
consumidas normalmente".

### Medido, contato por contato

| contato | entrou | tags | tarefas | mensagens | parado há |
|---|---|---|---|---|---|
| `Andre` (Facebook, form "O PROXIMO CLIENTE FORMS v1") | 19/09 02:18 | `etapa-novo-lead`, `cad-inbound` | **0** | **0** | **4d 19h** |
| `Neid` (Facebook) | 19/09 02:18 | idem | — | **0** | **4d 19h** |
| `Carlos Andrade` (Facebook, o último do anúncio) | 21/09 09:17 | + `limpar-tarefas` | **0** | **0** | **2d 12h** |

"Mensagens 0" quer dizer: a única entrada no histórico da conversa é a
atividade de sistema `Opportunity created` (`type: 28`,
`TYPE_ACTIVITY_OPPORTUNITY`). Nenhuma mensagem de saída, nunca.

O `Andre` respondeu no formulário do anúncio, em três campos: urgência **"Pra
ontem"**, "Já faço anúncios e quero melhorar meus resultados", "Não invisto nada
ainda". Está esperando há **4 dias e 19 horas**. É o custo da L-07 em uma linha,
e é a única coisa nesta seção que o dono não podia saber antes: o item G-03
dizia *quantos*, não o que estava dentro de um deles.

### A entrada, agora medida na conta e não inferida

| | |
|---|---|
| oportunidades com `source = Facebook` | 37 de 49 |
| a mais nova delas | `Carlos Andrade`, **21/09 09:17:26** |
| desde então | **60 h sem um único lead de anúncio** |
| criadas em 22/09 e 23/09 | 4, todas sem `source` (manuais/teste: `Francisca`, `O Próximo Cliente`, `Sem Nome`, um número) + 1 `ZZ Teste` |

Isto é o **F-10** deixando de ser suspeita: a porta está fechada há 60 h, e a
conta confirma. Os 49 não estão crescendo — estão só envelhecendo, como o G-03
já dizia em 22/09.

### Limite honesto

Conferi **3 dos 48** um por um (tarefas + histórico de conversa + campos do
contato). A afirmação sobre os outros 45 não vem de medição individual, vem da
estrutura: eles estão todos em `NOVO LEAD`, e o gatilho da cadência só escuta
`CONECTAR`. A estrutura cobre os 48; as 3 amostras servem para confirmar que a
estrutura se comporta como se lê. O MCP não expõe o registro de execução de
workflow, então "nunca foi acionada" é inferência do gatilho + ausência de
qualquer rastro (tarefa, mensagem, `Tentativa nº`, `1ª tentativa em`), não
leitura de log.

### O que isto muda na fila

**Nada para aplicar.** A L-07/G-03 é decisão do dono e continua sendo: promover
automaticamente (e sob qual regra) é escolha de operação, não de código. O que
mudou é o peso do item — e que quando a decisão vier, quem for montar já sabe
que o elo que falta é **uma ação** (`create_opportunity` → `CONECTAR`,
`status: open`), não um workflow novo, e que ela cai dentro da própria `Porta de
Entrada` ou num promotor separado, conforme a regra que o dono escolher.

## 2.43 Os portões entraram no ar — e o que o `--aplicar` mostrou sobre a minha conferência

Em 23/09/2026, entre 21:40 e 21:46 UTC, o dono rodou os quatro `--aplicar` que
estavam na fila (commit `5904feb`). Medido nos dumps re-exportados pelo próprio
patch, 2 a 6 minutos depois da escrita:

| workflow | antes | depois | o quê |
|---|---|---|---|
| `Cadência Inbound` | 272 | **322** | G-17 (A): 2 portões × 5 toques × 5 nós |
| `Recuperação de No-show` | 41 | **61** | G-17 (A) |
| `Pós-ligação v2` | 142 | **146** | G-18 |
| `Canal que conectou` | 0 pontos | **5 pontos** | 9c completo: `Resposta v2` (1), `Pós-ligação v2` (3), `Triagem` (1) |

`auditoria_portoes.py` agora lê `sdr-lotado` e o teto `c1xuCuLyJheHOQoJ3grH` em
**todos** os toques das duas cadências. Base atualizada no mesmo commit desta
seção: **`portoes` 2 → 0**, **`campos` 4 → 3**.

### O bug era meu, e a minha conferência não podia pegá-lo

O `patch_portao_inbound.py` religava `parent`/`parentKey` dos nós clonados e
**nunca acertava os `next`**. O GHL valida `next`. A conta respondeu **400** — e
o script seguiu adiante e imprimiu resumo de sucesso, porque o `put()`
compartilhado **devolvia a resposta e ninguém a lia**.

Duas falhas, e a segunda é a grave:

1. A `confere()` checava ids únicos, pais inexistentes, `goto` quebrado e
   vazamento de uuid. Não checava encadeamento de `next` — logo **não tinha como
   falhar exatamente no que estava errado.** Conferência que eu mesmo escrevo só
   pega o defeito que eu imaginei.
2. O `--aplicar` não tinha como distinguir sucesso de recusa. O §2.37 desta
   página diz que o patch estava "validado"; era verdade sobre as invariantes que
   eu escrevi e **mudo** sobre a única resposta que não se engana: a da conta.

### O conserto ficou na fonte, não em cada chamador

`put()` (em `patch_funil_reuniao.py`, importado por nove scripts) agora
**levanta `RuntimeError`** quando a conta recusa:

```
PUT RECUSADO pela conta em 'Cadência Inbound' (322 nos enviados): {"_error": true, …}
```

Contei: dos 17 pontos de chamada de `put`, **9 não conferiam o retorno**
(`patch_campos_data`, `patch_canal_conectou`, `patch_closer_tarefa`,
`patch_condicoes_etapa`, `patch_mestre_tags`, `patch_noshow_ns1`,
`patch_remove_atendeu`, `patch_remove_parte2`, `patch_textos_marca`). Consertar
um por um seria esquecer de novo no próximo patch — e quem esquece não vê.
Testado nos três caminhos: recusa 400 → levanta; resposta vazia → levanta;
sucesso → passa e devolve.

### E a minha auditoria deu alarme falso no mesmo minuto

Com os portões no ar, `auditoria_portoes.py` passou a imprimir
`PARCIAL: 'SDR lotado?' em 2 de 3 toques` na `Recuperação de No-show`. Fui
conferir o `NS3` antes de reportar: o ramo dele limpa `Resultado da tentativa`,
**remove** `fila-tel`, aplica `nutricao-90d` e move a oportunidade. **`NS3` não
é um toque — é a saída da cadência.** Portão de capacidade ali adiaria a *saída*
de um lead porque o SDR está cheio.

O achado era da auditoria, não da cadência. A invariante no docstring sempre
falou de **toque que consome**; a implementação contava toque por prefixo de
nome. Agora `toque_consome()` desce a árvore do toque (parando quando entra no
território de outro) e só exige portão de quem **adiciona** `fila-tel` /
`fila-wa` / `toque` — remover não conta. O conserto não é um caso especial do
`NS3`: a `Cadência 12x30 — parte 2` também tem 6 toques dos quais 5 gastam fila,
e teria produzido o mesmo alarme falso no dia em que faltasse um portão nela.

Depois do conserto: **nenhum `PARCIAL` em nenhuma cadência**, nenhuma grave,
`auditoria_tudo.py` exit 0.

### O que isto não resolve

Os três portões agora protegem uma cadência que **nenhum lead alcança**. O
gatilho da `Cadência Inbound` só escuta `CONECTAR`, e os 49 leads continuam em
`NOVO LEAD` — §2.42. O G-17 no ar cumpre a promessa do `GUIA-SDR.md` linhas
74-76 e a precondição do **lote de 6/dia**; não cumpre nem substitui a L-07.

## 2.44 O G-16 previu e aconteceu 4h45 depois — e a causa raiz pode ser mais larga do que ele escreveu

O G-16 (`ROADMAP-SALES-ENGAGEMENT.md`, **FEITO em 23/09/2026**) resgatou a
`Francisca` e escreveu a previsão: *"Qualquer outra pessoa da vida pessoal do dono
que mandar mensagem para esse número recebe o mesmo tratamento: vira oportunidade
em `NOVO LEAD`, ganha `cad-inbound`."*

Às **21:54:22 UTC de 23/09** — 4 h 45 min depois de a `Francisca` ter sido posta em
`abandoned` — apareceu o segundo caso. Medido por API no check-in das 21:54:

| | |
|---|---|
| oportunidade | `JudIT5DF7JinFbBqcwYU`, `NOVO LEAD`/`open`, criada **21:54:22** |
| contato | `d0ZJyFlxl1GZNDUiICnt`, nome = o próprio número (`554791548812`) |
| tags | `cad-inbound`, `etapa-novo-lead` |
| `assignedTo` | `JdvhvOTEBTvUyRi0BXU8` — o mesmo do `O Próximo Cliente` |
| fio | 6 mensagens pela Stevo (`type 20`), 21:54:20 a 21:54:59 |

O conteúdo do fio não é de lead: *"Não estou tendo certo, sucesso com o suporte.
Pode me ajudar?"*, *"Comprei o número telefônico"*, *"E também sobre 20 dias a mais
do teste, não habilitou"*, *"Se poder checar"*, mais uma imagem. É o dono falando
com **suporte/fornecedor**, não alguém perguntando sobre anúncios.

`NOVO LEAD` foi de 49 para **50**. Nada foi escrito por mim: nenhuma linha
disto está `[x]` no `APROVADO.md`.

### O que isto muda no G-16

Duas coisas, e a segunda é candidata, não item:

1. **O G-16 está `FEITO` e a classe não está.** O que fechou foi o resgate da
   `Francisca` e o passo preventivo no `GUIA-SDR.md` (ler o fio antes de tratar a
   `TI1` como prospect). O filtro estrutural o próprio G-16 declarou impossível
   para um workflow decidir sozinho. Então um segundo caso **não é achado novo** —
   é a previsão do G-16 se cumprindo, e a medida que sobra é aquele passo do guia
   funcionar. Quem ler "FEITO" sem ler o corpo vai achar que a porta foi
   consertada.
2. **CANDIDATO, a confirmar na tela:** o G-16 diz que o gatilho dispara "para
   qualquer primeira mensagem **recebida**". Neste fio, as 6 mensagens que a API
   devolve são **todas `outbound`** (`from: Pablo Santos's Account`), e a mais
   antiga é 2 s anterior à criação da oportunidade, com `nextPage: false`. Se a
   porta também dispara em conversa que o **dono inicia**, o alcance é maior do
   que o G-16 escreveu: todo fornecedor e todo suporte que o dono contatar por
   aquele aparelho entra como lead. Não afirmo: mensagem inbound pode não estar
   sincronizada ou pode não vir nesse endpoint. Confirma-se lendo o fio na tela,
   ou vendo se existe mensagem inbound antes de 21:54:20.

### O que segura o dano hoje, e por que isso não é consolo

Nenhuma mensagem automática vai para esse contato — porque a `Cadência Inbound`
só escuta `CONECTAR` e ele está em `NOVO LEAD` (§2.42), e a `Triagem da Nutrição`
exige `status-nutricao`, que só chega no fim da cadência. **É o funil quebrado
protegendo o contato.** No dia em que a L-07 for resolvida, esta proteção
acidental cai junto — e aí o passo do `GUIA-SDR.md` é a única rede.

### Confirmado às 22:07: é a suporte da própria WeSales, e a limpeza A9 não a tirou

O contato ganhou nome às 22:07:33 — **`Rafaela de Paula - We Sales`**. Não é
"fornecedor" genérico: é a atendente da plataforma em que este CRM roda. O dono
pedindo ajuda ao suporte da WeSales entrou no funil de vendas dele como lead
atribuído.

E ela **continua lá depois da faxina**. A `A9` (commit `994c97e`, 22:0x) limpou a
fila de `NOVO LEAD` de 7 contatos de casa/teste; medido às 22:1x, `NOVO LEAD` tem
**42 oportunidades `open`** e a mais nova de todas ainda é a
`JudIT5DF7JinFbBqcwYU`, com `cad-inbound` + `etapa-novo-lead` e `assignedTo`. A
faxina pegou o que era obviamente de teste e não tinha como pegar esta: o nome
só apareceu depois, e antes dele o contato era um número solto — indistinguível
de um lead de WhatsApp.

Continua valendo o que a seção diz: **eu não escrevo nada** sem `[x]`. A decisão
é de uma linha — resgatar como a `Francisca` (tirar as duas tags, oportunidade
para `abandoned`) ou deixar e confiar no passo do `GUIA-SDR.md`.
