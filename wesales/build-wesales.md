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
10. Workflows "Recuperação de No-show" e "SLA do Closer — No-show" (seção
    5.3/5.4, R-12) — mesmo calendário e status `No Show`; o nó 3 do Pós-
    agendamento (passo 7) precisa já remover destes dois workflows antes de
    publicá-los, senão um reagendamento no meio de uma recuperação não limpa
    nada
11. Workflow "Qualificação por IA no WhatsApp" (seção 6)
12. Workflow "Cadência 12x30" (seção 2) — por último entre os principais,
    porque chama os outros e usa o Trigger Link do passo 4 nas mensagens M2/M3;
    textos das mensagens em `biblioteca-mensagens.md`, não neste documento.
    Do passo 12 em diante o gatilho da seção 2.1 já leva o filtro novo do
    R-07 (tag `cad-inbound` ausente) — monte-o com o filtro desde o início,
    não depois. O bloco padrão de tentativa (seção 2.4) já leva o nó 2.5 de
    pausa individual (R-09) desde a primeira montagem, não como retrofit.
    O nó 0 já leva o par 0.7/0.7b de distribuição de leads (R-10, seção
    2.14) desde o início — defina a lista de round robin no nó 0.7b mesmo
    com um único SDR hoje — e o portão 0.0/0.0b de higiene de telefone
    (R-13, seção 2.3) na frente de tudo, antes do 0.1
13. Workflow "Cadência Inbound" (seção 2.10) — depois da 12x30 porque o
    handoff do fim da cadência inbound entra nela por Add to Workflow (seção
    2.10, último nó); precisa da 12x30 já montada para apontar para algo.
    Também já leva o nó 1.5 de pausa individual (R-09) desde o início, o
    par 0.8/0.8b de distribuição de leads (R-10) apontando para a **mesma**
    lista de round robin do nó 0.7b do passo 12, e o mesmo portão 0.0/0.0b
    de higiene de telefone (R-13) do passo 12
14. Workflows "Interceptação de Sinal — Clique" e "— Resposta" (seção 2.9)
15. Workflow "Alerta de Speed-to-lead" (seção 2.11) — usa a mesma tag nova de
    monitoramento que a lista 8.8 filtra; do R-07 em diante o nó 1 bifurca
    o tempo de espera por origem (`cad-inbound` presente = 15 min, senão 1h);
    do R-09 em diante o nó 2 já ignora quem está com a tag `pausado`
16. Workflow "Reengajamento 90 dias" (seção 2.12) — por último entre os que
    tocam cadência: reaproveita o bloco padrão da 12x30 (passo 12) nó a nó,
    nó 2.5 incluído, e exige que o gatilho do passo 12 já tenha o filtro
    `reengajamento-ativo` ausente (R-08) — monte-o com o filtro desde o
    início se ainda não montou, não depois
17. Listas inteligentes (seção 8), incluindo `Fila do Dia — Total` (8.16),
    `Recuperação de No-show` (8.17, R-12) e `Higiene — Sem Telefone Válido`
    (8.18, R-13)
18. Workflow "Monitor de Capacidade" e métrica `Estouro da Fila` (seção
    2.15) — depende da lista 8.16 do passo 17 já montada
19. Teste com os 5 contatos fictícios (seção 10) **antes** de publicar
20. Pausar Workflows em Datas Específicas (seção 2.13, R-09) — por último de
    todos: o recurso só lista workflows **publicados**, então precisa dos
    passos 12, 13, 16 e 18 já publicados para aparecerem no seletor
21. Ativar Number Validation (Configurações → Telefone, agência e depois
    subconta) e montar o workflow "Higiene de Número — Validação Automática"
    (seção 2.16, R-13) — opcional, por último de todos: o gatilho **Number
    Validation** só existe depois de o recurso estar ligado, e o portão
    0.0/0.0b dos passos 12/13 já cobre o caso mais comum (sem telefone
    nenhum) sem depender disso
22. Dashboard "Painel do Gestor — Pré-vendas" e as Custom Metrics novas
    (seção 2.17, R-15) — por último de todos: cada widget aponta para uma
    peça já montada nos passos anteriores (calendário do passo 3, pipeline
    do passo 2, métrica `Estouro da Fila` do passo 18, tarefas das
    cadências dos passos 12/13); montar antes disso deixaria widget
    apontando para nada

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
| Tempo de estagnação | Já coberto: F-05 (roadmap) monitora "sem tentativa há 7 dias"; a 1ª tentativa tem relógio próprio (Alerta de Speed-to-lead, seção 2.11). O antigo gap "retorno vencido sem nova ligação" (que dependia de S-01, `Data do retorno`/`Hora do retorno` — o primeiro já existe como campo, o segundo não, ver `GUIA-MONTAGEM.md`) continua valendo aqui dentro, não em etapa separada |
| Motivos de perda | `Número errado` (→ `telefone-invalido`), `Não ligar` (→ opt-out, DND) — saem da etapa via `Update Opportunity` para `status = lost`; 12 tentativas esgotadas sem conexão → `status = abandoned` **+** tag `nutricao-90d`, **sem sair de `CONECTAR`** (era "→ `Nutrição`" no plano de 7; agora é status, não movimento de etapa) — os três ramos do Pós-ligação, seção 4 |
| Taxa de conversão esperada | ~35% conectam ou saem antes das 12 tentativas (L-05, `briefing-sdr.md`) — mesma hipótese que já dimensiona o volume de entrada |
| Meta de avanço | 100 ligações/dia é a meta do SDR (briefing); quantos *leads* avançam por dia é `Total de conexões` (C-07) somado, lido na lista `Conexão por Tentativa` (8.6, R-01) |

#### Etapa 2 — `AGENDAR`

| Bloco | Conteúdo |
|---|---|
| Objetivo | Qualificar e agendar com o closer na mesma ligação (briefing-sdr.md, "A máquina") |
| Validação de passagem | Formulário `Qualificação SDR` preenchido + agendamento no calendário `Reunião com closer` (dispara o Pós-agendamento, seção 5) |
| Ferramentas | Calendário + formulário (seção 7), tarefa `[CONECTADO] Qualificar e agendar` |
| Tempo de estagnação | **Gap encontrado ao preencher este bloco, sem monitor ainda:** nenhum relógio hoje mede "atendeu e não agendou em X horas". Registrado como adição ao F-05 (roadmap, ainda no bloco 6 — sem volume não vale construir agora): 24h sem sair de `AGENDAR` |
| Motivos de perda | **Segundo gap encontrado:** hoje não existe caminho de desqualificação instantânea nesta etapa — o Pós-ligação sempre cria a tarefa de agendar, mesmo quando a conversa já mostrou que não há fit. Registrado como lacuna nova, **L-08** (`briefing-sdr.md`) |
| Taxa de conversão esperada | Depende do L-08 ser resolvido para medir separado de "não conseguiu horário"; hoje mistura os dois motivos numa métrica só |
| Meta de avanço | Ligado à meta de conexões da etapa anterior — sem meta própria adicional |

#### Etapa 3 — `NEGOCIAR` (absorve `Reunião agendada` + a negociação do closer)

| Bloco | Conteúdo |
|---|---|
| Objetivo | Comparecimento + veredito de qualificação real do closer, e a negociação em si (proposta, condições) até a decisão de compra — a metade "negociação" não existia no plano de 7 etapas, que a mandava para fora do pipeline |
| Validação de passagem | `Reunião foi qualificada` preenchida pelo closer (Loop do closer, seção 5.1) para a metade "comparecimento"; para a metade "negociação", decisão do closer registrada como `status = won` (→ `FORMALIZAR`) ou `status = lost` (permanece em `NEGOCIAR` com o status marcado, não some da tela) |
| Ferramentas | Calendário, Registro de Comparecimento (5.2), Loop do closer (5.1), SLA do Closer — No-show (5.4, R-12); a negociação em si (proposta/condições) é conduzida pelo closer fora dos workflows deste documento |
| Tempo de estagnação | A metade "comparecimento" já está coberta — é literalmente o R-12: SLA do closer com escalonamento ao gestor (seção 5.4). A metade "negociação" (depois do `Reunião foi qualificada = Sim`) **não tem monitor ainda** — gap novo, mesma classe dos dois já registrados nas etapas anteriores; candidato a entrar no F-05 quando ele for construído |
| Motivos de perda | No-show 2x seguido (R-12: hoje descarta a oportunidade — com `Descartado` sem ser mais etapa, isso deve virar `status = lost` mantendo a oportunidade em `NEGOCIAR`, não um "mover para `Descartado`" — a seção 5.3/5.4 ainda usa a redação antiga e entra na fila de migração), `Reunião foi qualificada` = `Não` (→ roteamento da seção 5.1, mesma troca de "mover etapa" por "mudar status") |
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
dias (seção 2.12, ainda escrita em cima do nome antigo `Nutrição` — tradução
em 1.0) montado: um lead pode chegar a `status = abandoned` sem nunca ter
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
| Allow Re-entry | **Desligado** (decisão D-06) | Com reentrada ligada, o lead que volta para "Em cadência" ganha tentativas duplicadas |
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
| 2.5 | **Pausa individual (R-09)** | If/Else | tag `pausado` presente → ramo 2.5b. Senão → segue para o Portão (nó 3) |
| 2.5b | Ramo da pausa individual | Wait → Time Delay 1 dia → **volta para o nó 2.5** | Não cria tag de fila, não cria tarefa, não avança `Tentativa nº`. Reconsulta a tag uma vez por dia até o SDR remover — a tentativa fica represada no mesmo lugar, não é descartada nem reagendada |
| 3 | **Portão** | If/Else — condições **E** | Etapa da oportunidade **é** `CONECTAR` · tag `nao-perturbe` **não** presente · `Resultado da tentativa` **não é** `Não ligar` · (só em tentativa de telefone) tag `telefone-invalido` **não** presente |
| 3b | Ramo falso do portão | Remove Contact Tag `fila-tel`, `fila-wa`, `fila-quente` → Add Contact Tag `limpar-tarefas` → **Remove from Workflow: este** | Saída limpa. Sem isso, sobra tag e tarefa órfã |
| 4 | **Seletor de canal** | If/Else (só em tentativa de WhatsApp) | Ramo WA: `Permissão WhatsApp` **é** `Sim` **E** `WA não atendidas seguidas` **<** 2. Ramo senão: vira telefone (decisão D-04 + regra das 2 seguidas) |
| 5 | **Limpar resultado** | Update Contact Field | `Resultado da tentativa` = vazio · `Tentativa nº` = `{n}` |
| 6 | **Adicionar tag de fila** | Add Contact Tag | `fila-tel` (telefone) ou `fila-wa` (WhatsApp) |
| 7 | **Criar tarefa** | Add Task | Título: `[CADENCIA] T{n} · Ligar (telefone)` ou `[CADENCIA] T{n} · Ligar (WhatsApp)` · Vence: hoje no horário da tentativa · Atribuir: `Contact Owner` (dinâmico — segue o `Assigned User` do nó 0.7b, R-10, seção 2.14) |
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
| Janela de envio | **Sem restrição, 24/7** — decisão do dono ao vivo, 19/09/2026: nenhum dos 8 nós manda mensagem pro lead (só atualização de campo, tag, tarefa e aviso interno); travar numa janela de expediente perde exatamente a vantagem de interceptar o sinal na hora. Não confundir com a janela 08:30–18:30 da Cadência 12x30 (seção 2), que continua valendo lá porque aquela liga/manda mensagem de verdade |
| Allow Re-entry | Ligado (cada clique é um sinal novo) |
| Stop on Response | Desligado |

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Portão de etapa | If/Else | Etapa da oportunidade **é** `Em cadência` → segue. Senão → **encerra** (quem já saiu de cadência não precisa furar fila; já está tratado por outro caminho) |
| 2 | Portão de silêncio | If/Else | tag `nao-perturbe` presente → **encerra**. Senão → segue |
| 3 | Prioridade | Update Contact Field | `Prioridade` = 5 |
| 4 | Registro do sinal | Update Contact Field | `Sinal recebido` = `Clique em link` · `Data e hora do sinal` = `{{right_now}}` (nome real do campo na tela; ver `campos-e-tags.md`) |
| 5 | Fila | Add Contact Tag | `fila-quente` |
| 6 | Tarefa | Add Task | Título: `[CADENCIA] Sinal: clicou no link — ligar agora` · Vence: agora · Atribuir: `Contact Owner` (dinâmico, R-10 — o sinal fura a fila, mas continua com o mesmo dono do lead) |
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
| 0.0b | Ramo sem telefone | Add Contact Tag `telefone-invalido` → If/Else: `Site` **ou** `Instagram` preenchido → Mover oportunidade → `Nutrição` + Add Contact Tag `nutricao-90d`. Senão → Mover oportunidade → `Descartado` → Internal Notification para o gestor: `Lead inbound sem telefone: {{contact.name}} — revisar o formulário de origem` → **Remove from Workflow: este** |
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
| 6 | Tarefa | Add Task | Título: `[CADENCIA] TI{n} · Ligar (canal) — Inbound` · Vence: agora · Atribuir: `Contact Owner` (dinâmico, R-10) |
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

`reengajamento-ativo`, especificada em `campos-e-tags.md`. Seguiu o mesmo
caminho de `atraso-1a-tentativa` (T-12, R-02): nasceu fora do lote das 11
tags já aprovadas por nome em `APROVADO.md`, com linha própria — aprovada
ao vivo em chat e **criada em 18/09/2026** via `contacts_add-tags`.

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

## 2.14 Distribuição de leads — R-10

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

## 2.15 Monitor de Capacidade — R-11

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

## 2.16 Higiene de Número — Validação Automática (opcional) — R-13

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
quem já saiu de `Em cadência`, porque um número pode ser invalidado a
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
| 2 | If/Else: etapa da oportunidade **é uma de** `Novo lead`, `Em cadência`, `Retorno agendado` → segue. Senão (já `Conectado`, `Reunião agendada`, `Nutrição` ou `Descartado`) → só marca a tag e avisa (nó 4), sem mexer na etapa — um contato que já avançou por trabalho humano não retrocede por uma validação automática chegando atrasada |
| 3 | (só se o nó 2 seguiu) If/Else: `Site` ou `Instagram` preenchido → Mover oportunidade → `Nutrição` + Add Contact Tag `nutricao-90d`. Senão → Mover oportunidade → `Descartado` |
| 4 | Internal Notification para o gestor: `Telefone inválido (validação automática): {{contact.name}} — revisar a fonte da lista` |

Mesmo desenho de saída do nó 0.0b e do ramo `Número errado` da seção 4 —
mesma tag, mesmo critério de Nutrição vs. Descartado. Mover a etapa aciona
o Mestre de saída (seção 3) sozinho: nenhuma limpeza extra precisa ser
escrita aqui.

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

## 2.17 Dashboard do Gestor — R-15

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

Nenhuma das quatro é campo ou tag nova: as três novas reaproveitam C-09 a
C-12 (R-01) e a tag `atraso-1a-tentativa` (T-12, R-02) — o mesmo
raciocínio de "não duplicar o que o projeto já expõe" que fechou o R-10 e
o R-13 em `campos-e-tags.md`. Se o plano da subconta não incluir Custom
Metrics, as duas primeiras linhas continuam cobertas pela lista 8.16 e
8.8 (sem entrar no dashboard) e as duas últimas pela lista 8.6 — o
dashboard perde a tela única, não perde o dado.

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
| 1 | If/Else | Etapa da oportunidade **é** `CONECTAR` **E** `status` **é** `open` → **encerra aqui** (não limpa nada). Senão, segue |
| 2 | Remove from Workflow | `Cadência 12x30` |
| 3 | Remove from Workflow | `Qualificação por IA no WhatsApp` |
| 4 | Remove Contact Tag | `fila-quente`, `fila-tel`, `fila-wa`, `fila-linkedin`, `atraso-1a-tentativa` (R-02), `reengajamento-ativo` (R-08), `pausado` (R-09) |
| 5 | Add Contact Tag | `limpar-tarefas` |
| 6 | Add Note | `Saída de cadência · etapa: {{opportunity.pipeline_stage}} · status: {{opportunity.status}} · tentativa {{contact.tentativa_no}} · resultado {{contact.resultado_da_tentativa}}` |

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
| 6 | Mover oportunidade → `AGENDAR` (dispara o Mestre de saída pelo gatilho de etapa, que faz a limpeza) |
| 7 | Update Contact Field `Data conectado` = `{{right_now}}` (R-03 — só marca; não repete se já preenchido, mas escrever de novo é barato e não quebra nada) |
| 7b | Date/Time Formatter | Entrada `{{right_now}}` · "To Format" = `HH` (só a hora, 00–23) — mecanismo de horário aprendido por segmento, seção 2.18, F-02 |
| 7c | Update Contact Field | `Hora da conexão` = saída do nó 7b |
| 8 | Add Task `[CONECTADO] Qualificar e agendar` · vence hoje · Atribuir: `Contact Owner` (dinâmico, R-10) |
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
| 4 | Add Task `[RETORNO] Ligar de volta` · vence: `Data do retorno` (campo S-01) ou hoje+1 se vazio · Atribuir: `Contact Owner` (dinâmico, R-10) |

Sem o campo `Data do retorno` (lacuna L-01) este ramo funciona, mas a tarefa
vence sempre em hoje+1 e a lista "Retornos" não sabe o que é de hoje. Não há
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
| 4 | Remove from Workflow: `Cadência 12x30` e `Qualificação por IA no WhatsApp` |
| 5 | Update Opportunity `status` = `lost` |
| 6 | Add Note `Opt-out registrado em {{right_now}}` |

Etapa também fica em `CONECTAR` aqui — só o `status` muda. O nó 4 já tira o
contato dos dois workflows na hora (não depende de esperar o Mestre de saída
reagir ao `status`), então o opt-out é imediato mesmo se o gatilho de
`Opportunity Status Changed` atrasar.

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
| 3 | Remove from Workflow | `Cadência 12x30`, `Qualificação por IA no WhatsApp`, `Recuperação de No-show`, `SLA do Closer — No-show` (R-12 — este gatilho também dispara num **reagendamento** depois de um no-show; sem remover os dois workflows daqui, uma recuperação em curso continuaria mandando NS2/NS3 para um lead que já remarcou. `Remove from Workflow` de um contato que não está no workflow não faz nada — chamar sempre é seguro) |
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
| 3 | Update Contact Field | `Nº de no-shows` = 0 (R-12 — comparecer de verdade reinicia a contagem; a regra de descarte automático da seção 5.3 é sobre no-show **consecutivo**, não sobre o histórico de vida do lead) |
| 4 | Add Note | `Compareceu à reunião · {{right_now}}` |

Não mexo em etapa aqui: comparecer não move a oportunidade (quem decide o
destino é o veredito do closer, seção 5.1). Este workflow só marca o carimbo
que a seção 8 lê.

**Pronto quando (compõe o R-03 no roadmap):** existe carimbo de "compareceu"
tão confiável quanto os de "conectou" e "agendou" — os três lidos pelas
listas 8.10 a 8.12.

---

## 5.3 Workflow "Recuperação de No-show" — R-12

A seção 5 fecha o agendamento e a 5.2 confirma o comparecimento; nenhuma das
duas trata o meio-termo, que é o vazamento mais caro do funil: reunião
marcada, closer de agenda reservada, lead que simplesmente não aparece. Hoje
isso morre em silêncio — a oportunidade fica parada em `Reunião agendada`
para sempre, e ninguém tenta de novo.

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
no-show seguido do mesmo lead, a oportunidade vai direto para `Descartado`,
sem gerar nenhuma tarefa nova — regra de proteção da agenda do closer. Reev,
Meetime, Outreach e Salesloft tratam no-show repetido como métrica de
relatório ("taxa de no-show por rep"), nunca como gatilho de decisão
automática. Aqui vira decisão porque o custo de ligar uma terceira vez para
quem já furou duas reuniões marcadas é maior que o valor esperado do lead —
e ninguém precisa lembrar de aplicar esse corte na mão.

### Por que fica em `Reunião agendada`, não volta para `Em cadência`

O Reengajamento 90 dias (seção 2.12, R-08) já pagou o preço de aprender que
devolver um lead para `Em cadência` esbarra no `Allow Re-entry` desligado da
Cadência 12x30 (D-06) — um contato que já passou por aquele workflow uma vez
fica bloqueado de entrar de novo nele para sempre, gatilho ou `Add to
Workflow`, e resolver isso exigiu tag de blindagem (`reengajamento-ativo`) e
mudar a origem do lead. Este item não paga esse preço porque não tenta
reentrar na 12x30 de jeito nenhum: a oportunidade nunca sai de `Reunião
agendada`, o contador `Nº de no-shows` mora no contato (não numa etapa nova)
e a régua de recuperação roda num workflow próprio, pequeno, do mesmo jeito
que já separou a Cadência Inbound (2.10) e o Reengajamento (2.12) da 12x30.
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
| 1 | Portão de sanidade | If/Else — etapa da oportunidade **é** `Reunião agendada` → segue. Senão → **encerra** (o compromisso já não reflete o estado atual do lead; evita reabrir um no-show velho de uma oportunidade que já foi resolvida por outro caminho) |
| 2 | Contador | Math Operation — `Nº de no-shows` + 1 |
| 3 | Portão de repetição | If/Else — `Nº de no-shows` ≥ 2 → **ramo Descarte** (abaixo). Senão → **ramo Recuperação** (abaixo) |

#### Ramo Descarte (2º no-show seguido, ou mais)

| # | Ação |
|---|---|
| 1 | Remove Contact Tag `fila-tel` (idempotente, mesmo se ausente) |
| 2 | Add Contact Tag `limpar-tarefas` |
| 3 | Mover oportunidade → `Descartado` (aciona o Mestre de saída, que faz o resto da limpeza) |
| 4 | Add Note `Descartado após {{contact.n_de_no_shows}}º no-show seguido sem reagendar — regra de proteção de agenda do closer (R-12)` |
| 5 | Internal Notification ao gestor `{{contact.name}} descartado automaticamente após {{contact.n_de_no_shows}}º no-show — nenhuma ação necessária, é a regra de proteção de agenda` |

#### Ramo Recuperação (1º no-show)

| # | Ação | Configuração |
|---|---|---|
| 1 | Send WhatsApp (SMS fallback) | Texto `NS-1` (`biblioteca-mensagens.md`) |
| 2 | Update Contact Field | `Template usado` = `NS-1` |
| 3 | Add Contact Tag | `fila-tel` |
| 4 | Add Task | `[CADENCIA] NS1 · Ligar (telefone) — Recuperação de no-show` · vence hoje · Atribuir: `Contact Owner` (dinâmico, R-10) |
| 5 | Aguardar | Wait → Until specific time · D1 10:00 |
| 6 | Portão | If/Else — etapa ainda `Reunião agendada` **E** `nao-perturbe` ausente **E** `pausado` ausente → segue. Senão → **Remove from Workflow: este** |
| 7 | Add Contact Tag | `fila-tel` |
| 8 | Add Task | `[CADENCIA] NS2 · Ligar (telefone) — Recuperação de no-show` · vence hoje · Atribuir: `Contact Owner` |
| 9 | Aguardar | Wait → Until specific time · D3 15:00 |
| 10 | Portão | Mesmo do nó 6 |
| 11 | Add Contact Tag | `fila-tel` |
| 12 | Add Task | `[CADENCIA] NS3 · Ligar (telefone) — Recuperação de no-show` · vence hoje · Atribuir: `Contact Owner` |
| 13 | Aguardar | Wait → Time Delay 1 dia (folga para o SDR classificar a NS3) |
| 14 | Portão | If/Else — etapa ainda `Reunião agendada` → segue (ninguém reagendou nem descartou). Senão → **Remove from Workflow: este** |
| 15 | Send WhatsApp (SMS fallback) | Texto `NS-2` |
| 16 | Update Contact Field | `Template usado` = `NS-2` |
| 17 | Update Contact Field | `Resultado da tentativa` = vazio |
| 18 | Remove Contact Tag | `fila-tel` |
| 19 | Add Contact Tag | `nutricao-90d` |
| 20 | Mover oportunidade | → `Nutrição` (aciona o Mestre de saída **e**, 90 dias depois, o próprio Reengajamento 90 dias — seção 2.12 — reativa o lead sozinho, sem workflow novo para o caminho "desistiu") |

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

## 5.4 Workflow "SLA do Closer — No-show" — R-12

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
| 1 | Portão | If/Else — etapa da oportunidade **é** `Reunião agendada` → segue. Senão → **encerra** |
| 2 | Portão | If/Else — `Nº de no-shows` ≥ 2 → **encerra** (a seção 5.3 já decidiu descartar; cobrar retorno do closer aqui seria alertar para uma decisão que já foi tomada) |
| 3 | Alerta imediato | Internal Notification ao closer `{{contact.name}} não compareceu à reunião de {{appointment.start_time}}. A recuperação automática (NS1) já dispara em instantes — se preferir reagendar você mesmo agora, é mais rápido para o lead e evita o SDR ligar à toa.` |
| 4 | Aguardar | Wait → Time Delay 2h corridas |
| 5 | Portão | If/Else — etapa da oportunidade ainda **é** `Reunião agendada` → segue (ninguém reagendou nem descartou nesse meio-tempo). Senão → **encerra** |
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

### 8.4 `Retornos` — migrado para as 5 etapas reais em 18/09/2026
| Item | Configuração |
|---|---|
| Filtros | `Resultado da tentativa` = `Pediu retorno` **E** `nao-perturbe` ausente |
| Colunas | Nome · `Empresa` · Telefone · `Data do retorno` · `Prioridade` · `Nota de qualificação` · Tarefas abertas |
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
em `Reunião agendada`, não em `Em cadência`.

### 8.17 `Recuperação de No-show` — R-12
| Item | Configuração |
|---|---|
| Filtros | `Nº de no-shows` ≥ 1 **E** etapa da oportunidade = `Reunião agendada` **E** `nao-perturbe` ausente |
| Colunas | Nome · `Empresa` · Telefone · `Nº de no-shows` · `Template usado` · Última atividade · Tarefas abertas |
| Ordenação | `Nº de no-shows` desc, depois Última atividade asc |

Filtra por campo numérico direto, sem tag nova — mesmo raciocínio já usado
na 8.6 (`Total de conexões` ≥ 1). Não aparece em 8.2/8.3 porque a etapa
continua `Reunião agendada`, de propósito (seção 5.3, "por que fica em
Reunião agendada"): esta lista é a única visão de quem está na régua NS1-NS3,
igual a 8.14 já ser a única visão de quem está na régua TR1-TR4.

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
| 28 | Distribuição de leads (R-10) | Com pelo menos 2 usuários cadastrados na subconta de teste: mova o Teste Atendeu para `Em cadência` e confira que o nó 0.7 sorteia um `Assigned User` (seção 2.3); mova o Teste Não Atende também e confira que o sorteio alternou para o outro usuário (round robin de verdade, não o mesmo sempre); confira que a tarefa `[CADENCIA] T1` de cada um nasce atribuída ao respectivo dono, não a quem criou o teste — é aqui que se confirma se `Add Task` aceita `Contact Owner` como destino dinâmico ou se é preciso o valor personalizado (seção 2.14); repita a entrada de um dos dois num segundo teste (rodada manual, decisão D-06) e confirme que o nó 0.7 **não** sorteia de novo (Assigned User já não está vazio) | |
| 29 | Monitor de Capacidade (R-11) | Com os 5 contatos de teste em `fila-tel`/`fila-wa` ao mesmo tempo, confira que a lista `Fila do Dia — Total` (8.16) soma os dois grupos sem duplicar ninguém; confirme se o plano da subconta expõe Custom Metrics e, se sim, que `Estouro da Fila` mostra `5 − 100` (negativo, dia normal); rode o Scheduler do "Monitor de Capacidade" manualmente (ou aguarde o horário) e confira que o Internal Notification chega ao gestor nos dois horários configurados | |
| 30 | Handoff e no-show (R-12) | No Teste Atendeu já em `Reunião agendada`, reduza os Waits das seções 5.3/5.4 para minutos e marque o agendamento como `No Show`: `Nº de no-shows` vai a 1, o closer recebe o alerta imediato (nó 3 da 5.4), `fila-tel` é aplicada e a tarefa `[CADENCIA] NS1` nasce; confirme NS2/NS3 nascendo nos horários reduzidos e, sem resposta a nenhuma, `Template usado` = `NS-2`, `nutricao-90d` aplicada e etapa de volta a `Nutrição`. Não deixe passar as 2h reduzidas do nó 4 da 5.4 sem reagendar: confirme o Internal Notification de escalonamento ao gestor (nó 6). Repita o `No Show` uma segunda vez no mesmo contato (rodada manual): `Nº de no-shows` chega a 2, a oportunidade vai direto para `Descartado`, sem tarefa nova e sem alerta de SLA ao closer (nó 2 da 5.4 encerra sozinho). Por fim, num terceiro contato, marque `No Show` e reagende pelo link do calendário antes do fim da régua: confirme que nenhuma tarefa `NS2`/`NS3` nasce depois do reagendamento (nó 3 do Pós-agendamento removeu os dois workflows do R-12) e que marcar `Showed` depois zera `Nº de no-shows` (nó 3 da seção 5.2) | |
| 31 | Higiene de base (R-13) | Antes de os 5 contatos de teste ganharem telefone, mova o Teste Não Atende para `Em cadência` sem preencher `Phone`: o nó 0.0 aplica `telefone-invalido`; como o contato não tem `Site` (Q-02) nem `Instagram` (Q-03) preenchidos — o caso normal de lead outbound, porque esses dois só se preenchem na qualificação —, a oportunidade vai direto para `Descartado` (se algum dos dois estiver preenchido, vai para `Nutrição` + `nutricao-90d` — confira o ramo certo para o cadastro que estiver testando) e nenhuma tarefa `[CADENCIA] T1` nasce; o gestor recebe o aviso do nó 0.0b. Repita com um lead `cad-inbound` para confirmar o mesmo comportamento no nó 0.0 da Cadência Inbound (seção 2.10). Se a seção 2.16 tiver sido montada, valide também: um contato com telefone claramente fixo dispara o gatilho `Number Validation` como `Landline` e `Permissão WhatsApp` vira `Não` sem o lead sair de cadência | |
| 32 | Dashboard do Gestor (R-15) | Com pelo menos o Teste Atendeu em `Reunião agendada` e algum dos 5 em `Em cadência`, abra `Painel do Gestor — Pré-vendas`: o widget "Appointment Report" mostra o agendamento do calendário `Reunião com closer`; o widget "Opportunities" mostra o Teste Atendeu na etapa certa do funil ao vivo; o widget "Tasks" mostra a(s) tarefa(s) `[CADENCIA]` criada(s) hoje. Se o plano expuser Custom Metrics, confira as quatro métricas da seção 2.17 — `Estouro da Fila` negativo com só 5 contatos, `Atrasos de Speed-to-lead` em 0 (nenhum atrasou de propósito no teste), e as duas de `Taxa de Conexão` refletindo `Conexões telefone`/`Tentativas telefone` e o par de WhatsApp dos contatos de teste que já passaram por uma tentativa | |
| 33 | Horário aprendido por segmento (F-02) | No Teste Atendeu, preencha `Segmento` antes de mover para `Em cadência` e deixe atender na T1: confira que `Hora da conexão` (C-25) grava só a hora, formato `HH`, no mesmo instante em que `Data conectado` grava; confirme que a lista `Conexão por Segmento e Horário` (8.19) mostra a linha, ordenada por `Segmento` e depois por `Hora da conexão`. Repita com um segundo contato de teste em segmento diferente e confirme que as duas linhas não se confundem na lista | |

Depois do teste, **apague as 5 oportunidades e desative os 5 contatos** (não
exclua contatos, pela regra 1) e restaure os Waits e a janela de envio.

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
| Workflows | Não | **Não** (só `GET /workflows/` existe; sem POST em nenhuma versão do spec) | Seções 2, 2.9, 2.11, 2.15, 3 a 6, 5.1, 5.2 — sem alternativa por API |
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
