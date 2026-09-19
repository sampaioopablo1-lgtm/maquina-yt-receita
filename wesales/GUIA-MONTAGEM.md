# Guia de montagem manual — passo a passo

Documento vivo. Cada fase é ensinada em detalhe **na hora em que chega a
vez dela** — não adianta ler a fase 5 antes de terminar a 1, porque cada
uma referencia o que a anterior criou. Marque `[x]` conforme for fazendo;
é o jeito de saber, numa olhada, onde a montagem manual parou (a rotina
automática só mexe em tag/contato/oportunidade via API — o que está aqui é
só o que exige clique na tela).

Fonte de toda a especificação: `build-wesales.md`. Este guia não repete o
conteúdo dele — só organiza a ordem e detalha o clique que o outro
documento não detalha.

## Visão geral das fases

- [x] **Fase 1 — Pipeline** — concluída, mas com 5 etapas (`NOVO LEAD`/`CONECTAR`/`AGENDAR`/`NEGOCIAR`/`FORMALIZAR`), não as 7 originais — decisão do dono ao vivo, ver seção abaixo
- [x] **Fase 1.5 — Workflow "Porta de Entrada" (`build-wesales.md`, seção
      1.3) — concluída em 19/09/2026, e era o furo de fila certo.** Nada na
      especificação criava oportunidade, então nenhum lead — nem os que já
      tinham chegado pelo Meta Lead Ads — entrava em etapa nenhuma. Workflow
      publicado e backfill rodado: `opportunities_search-opportunity` foi de
      0 para 40 oportunidades, todas em `NOVO LEAD`, com telefone e atribuição
      de anúncio preservados (conferido por API às 02:2x UTC). O elo seguinte,
      `NOVO LEAD` → `CONECTAR`, é o L-07 e segue aberto: os 40 estão no funil,
      ainda não em cadência
- [x] **Fase 2 — Campos personalizados** — concluída; os 2 que faltavam (`WA não atendidas seguidas`, `Permissão WhatsApp`) foram criados e o tipo errado (`Conexões telefone`) foi corrigido para Numérico, confirmado via `locations_get-custom-fields`
- [ ] **Antes da Fase 5 (cadência), resolver `{{right_now}}`** — 17 nós gravam
      data/hora em campo de texto (`Entrada em`, `1ª tentativa em`), e o achado
      da seção 2.9.2 do `build-wesales.md` diz que o GHL não oferece data/hora
      atual para campo de texto. Abra `Update Contact Field` → `Entrada em` e
      veja se existe "Right Now"/"Current date and time" no seletor de valor.
      Não existindo, a seção 2.9.2 já traz o plano B (marca fixa em vez de
      carimbo, hora exata vindo da criação da tarefa/nota) — é decisão de 1
      minuto na tela que evita montar 17 nós errados
- [x] **Fase 3 — Calendário do closer + formulário de qualificação** —
      concluída em 19/09/2026 (não verifiquei por API: o conector não lista
      calendário nem formulário, então isto é o que os commits do dia
      registram — link público do calendário testado, duração fixada em 1h, e
      o formulário mapeado para o campo `Empresa` personalizado, porque o
      construtor não oferece o nativo). **Pendência aberta dentro dela:** o
      construtor criou `Necessidade` e `Urgência` sozinho, duplicando
      `Dor principal` e `Prazo` — decidir antes de o formulário receber lead
      de verdade (`CONFERENCIA-CAMPOS.md`, seção F)
- [ ] **Fase 4 — Trigger Link "Agendar com o closer"** — em andamento em
      19/09/2026; a Interceptação de Sinal foi montada na tela e rendeu dois
      achados que mudaram a especificação (`Find opportunity` obrigatório antes
      do `If/Else`, e data/hora atual indisponível em campo de texto — seção
      2.9.2)
- [ ] **Fase 5 — Os workflows restantes**, na ordem da seção "Ordem de montagem" do `build-wesales.md`
- [ ] **Fase 6 — Listas inteligentes** (~19)
- [ ] **Fase 7 — Teste com os 5 contatos fictícios** (já existem no CRM, seção 10)
- [ ] **Fase 8 — Pausar Workflows em Datas Específicas** (feriados/férias)
- [ ] **Fase 9 — Number Validation** (opcional)
- [ ] **Fase 10 — Dashboard + Custom Metrics**

---

## Fase 1 — Pipeline "Pré-vendas" (reaproveitando o `FUNIL DE VENDAS`)

**Mudou em 18/09/2026:** não é mais criar um pipeline novo. O dono decidiu
reaproveitar o `FUNIL DE VENDAS` que já existe, trocando as etapas dele
pelas 7 daqui. Detalhe da decisão e por quê: `build-wesales.md`, seção 1
("Migração de arquitetura") e `APROVADO.md`.

### Onde clicar

No menu lateral esquerdo da WeSales: **Configurações** (ícone de
engrenagem, fica perto do fim da lista, abaixo de "Reputação") →
**Pipelines** (pode aparecer como "Funis" ou "Estágios de negócio",
dependendo da tradução da tela) → abra **`FUNIL DE VENDAS`** → **Editar**.

Você **não** está mexendo em Oportunidades → Funil (aquela tela só mostra
os cartões); é em Configurações que se edita a lista de etapas em si.

### O que existe hoje nesse pipeline (14 etapas) e o que fazer com cada uma

| Etapa atual | O que fazer |
|---|---|
| `ENTROU EM CONTATO` | Renomear para `Novo lead` |
| `RESPONDEU O PRIMEIRO CONTATO` | Renomear para `Em cadência` |
| `NÃO RESPONDEU` | Renomear para `Conectado` |
| `CONVERSA EM ANDAMENTO` | Renomear para `Retorno agendado` |
| `EM FOLLOW UP` | Renomear para `Reunião agendada` |
| `COTAÇÃO REALIZADA` | Renomear para `Nutrição` |
| `DOCUMENTOS ENVIADOS` | Renomear para `Descartado` |
| `PAGAMENTO FEITO` | **Excluir** |
| `NÃO FECHOU PÓS COTAÇÃO` | **Excluir** |
| `ATIVAR FOLLOW UP AUTOMATIZADO` | **Excluir** |
| `Geladeira 30D` | **Excluir** |
| `Geladeira 60D` | **Excluir** |
| `Geladeira 90D` | **Excluir** |
| `NÃO TEM INTERESSE` | **Excluir** |

Renomear em vez de apagar-e-recriar preserva a posição (ordem) sem
trabalho extra — é por isso que a tabela casa a 1ª etapa antiga com a 1ª
etapa nova, a 2ª com a 2ª, e assim por diante, nas 7 primeiras. As 7
últimas (que sobram) só se apagam depois de confirmar que estão mesmo
sem oportunidade nenhuma dentro — confirmado por aqui, via
`opportunities_search-opportunity`: **0 oportunidades no pipeline
inteiro**, em qualquer status. Pode apagar sem medo de perder negócio
real.

### Configuração completa, etapa por etapa

Cada etapa, na tela de edição, tem 4 campos além do nome: **probabilidade
de ganho** (%), **cor**, e dois toggles — **mostrar no funil** e **mostrar
no gráfico de pizza**. Preencha assim, na ordem final (de cima para
baixo):

| Ordem | Etapa | Probabilidade de ganho | Cor | Mostrar no funil | Mostrar no gráfico de pizza |
|---|---|---|---|---|---|
| 1 | `Novo lead` | 5% | Azul (`#2563EB`) | Sim | Sim |
| 2 | `Em cadência` | 15% | Laranja (`#F59E0B`) | Sim | Sim |
| 3 | `Conectado` | 30% | Ciano (`#0EA5E9`) | Sim | Sim |
| 4 | `Retorno agendado` | 35% | Laranja escuro (`#F97316`) | Sim | Sim |
| 5 | `Reunião agendada` | 50% | Verde (`#16A34A`) | Sim | Sim |
| 6 | `Nutrição` | 10% | Rosa (`#DB2777`) | Sim | Sim |
| 7 | `Descartado` | 0% | Cinza (`#374151`) | Sim | Sim |

**Por que estes números e não outros:**
- **Probabilidade:** não é a progressão automática de 6,67% em 6,67% que
  estava lá antes (o bug que a auditoria achou — "NÃO TEM INTERESSE" com
  93% de chance de ganho). Aqui `Nutrição` (10%) é **mais baixa** que
  `Reunião agendada` (50%), não mais alta — nutrição é "ainda não", não
  "quase lá". Nenhum destes números é medido ainda; são ponto de partida
  razoável, não meta — a régua de qualificação (seção 9 do
  `build-wesales.md`) é o que decide de verdade se um lead é "quente".
- **Cor:** segue o mesmo código de cores que a régua de qualificação já
  usa em espírito — quente (laranja/verde) sobe, frio (cinza/rosa) desce.
  Se a tela não deixar digitar o hex exato, escolha a cor mais próxima do
  preset dela — a cor exata não afeta nenhum workflow, é só leitura visual
  para o gestor.
- **Mostrar no funil / gráfico de pizza:** deixe as duas ligadas em todas
  as 7 — é o padrão, e nenhuma etapa daqui tem motivo para ficar escondida
  do relatório nativo.

### Outras configurações do pipeline (mesma tela)

- **Visibilidade:** restrinja a quem faz parte da operação (SDR, closer,
  gestor).
- **Nome da oportunidade:** deixe no padrão (nome do contato).
- Confirme que **`Novo lead`** fica marcada como etapa de entrada para
  qualquer formulário/importação nova.

### Por que estas 7 e não menos

`Em cadência` precisa ser uma etapa própria porque é ela que todo
workflow da cadência consulta antes de disparar uma tentativa — sem essa
etapa exata, o mecanismo de segurança da máquina inteira não tem o que
checar. Raciocínio completo, etapa por etapa (objetivo, quando avança, o
que bloqueia, taxa esperada): `build-wesales.md`, seções 1.1 e 1.2.

### Como saber que terminou certo

- [ ] O pipeline (ainda chamado `FUNIL DE VENDAS` na tela, é o mesmo
      objeto) tem exatamente 7 etapas, na ordem da tabela acima
- [ ] Nenhuma das 7 antigas (cotação, documentos, pagamento, follow up,
      geladeiras, não tem interesse) sobrou
- [ ] Visibilidade restrita configurada

Quando terminar esta fase, me avise — eu confirmo lendo o pipeline pelo
conector (`opportunities_get-pipelines`) e ensino a Fase 2 (campos
personalizados) em seguida, com a lista pronta para copiar direto de
`campos-e-tags.md`.

### Resolvido ao vivo em chat, 18/09/2026 ~21h-22h UTC — Fase 1 concluída, arquitetura mudou

As "duas hipóteses" abaixo (histórico, não apague) ficaram respondidas: foi
a **hipótese 1**, decisão do dono ao vivo em chat, não acidente nem
snapshot de agência. Ele optou por **5 etapas**, não 7, recusando
explicitamente a tabela original desta seção. Decisão final, confirmada
por `opportunities_get-pipelines` nesta mesma conversa:

| Posição | Etapa (nome real na tela) | Prob. | Cor |
|---|---|---|---|
| 0 | `NOVO LEAD` | 30% | `#2563EB` |
| 1 | `CONECTAR` | 40% | `#8B5CF6` |
| 2 | `AGENDAR` | 50% | `#2DD4BF` |
| 3 | `NEGOCIAR` | 60% | `#D97706` |
| 4 | `FORMALIZAR` | 70% | `#059669` |

**Mapeamento acordado com o dono** (substitui a tabela de 7 etapas cravada
acima — aquela tabela é histórico do plano abandonado, não apague, mas não
siga por ela):

| Etapa real (5) | Papel no motor original (7) |
|---|---|
| `NOVO LEAD` | = `Novo lead` (sem mudança) |
| `CONECTAR` | = `Em cadência` — é aqui que o portão de toda tentativa (nó 3, seção 2.4 do `build-wesales.md`) passa a checar |
| `AGENDAR` | = `Conectado` — atendeu, qualificando/marcando reunião |
| `NEGOCIAR` | = `Reunião agendada` **+** a negociação do closer (que no plano de 7 etapas ficava fora do pipeline) |
| `FORMALIZAR` | Fechamento/contrato — não existia no plano de 7 etapas; equivale a "Ganho" |

**O que não tem etapa própria mais** (`Retorno agendado`, `Nutrição`,
`Descartado`) — substituído por tag + campo nativo **status da
oportunidade** (`open`/`won`/`lost`/`abandoned`, independente da etapa):
- **Retorno agendado**: sem mudança de etapa nem tag nova — o lead sai do
  workflow (nó 10, `Pediu retorno` já remove do workflow) e fica em
  `CONECTAR` mesmo; a lista `Retornos` (8.4) filtra só por `Resultado da
  tentativa = Pediu retorno`, sem precisar mais do OR com etapa.
- **Nutrição**: fica na etapa em que estava, status vira `abandoned`,
  tag `nutricao-90d` continua. Gatilho do Reengajamento 90 dias (seção
  2.12) muda de "Opportunity Stage Changed → Nutrição" para **"Contact Tag
  Added → `nutricao-90d`"** (gatilho nativo já usado em outro lugar do
  projeto, sem depender de etapa que não existe mais).
- **Descartado**: status vira `lost`, etapa fica como estava.

**Isto abriu uma tarefa de documentação grande, em andamento entre
rodadas:** todo o `build-wesales.md` foi escrito em cima das 7 etapas
antigas (~150 menções a `Em cadência`/`Conectado`/`Retorno agendado`/
`Reunião agendada`/`Nutrição`/`Descartado` em gatilhos, portões e ramos de
saída). Reescrever isso nó a nó para o modelo de 5 etapas + tag/status é
grande demais para uma rodada só — quebrada em pedaços fechados um de cada
vez, cada um marcado aqui assim que sai de `build-wesales.md` para valer:

- [x] **Seção 1 (Pipeline)** — reescrita em 18/09/2026: tabela das 5
      etapas reais, seção 1.0 nova com a tradução completa nome-antigo →
      etapa/estado-real (inclusive `Retorno agendado`/`Nutrição`/
      `Descartado` virando campo/status, não etapa), 1.1 (frameworks de
      mercado) e 1.2 (canvas operacional) reescritas para as 5 etapas.
- [ ] **Seção 2 — subseções 2.1–2.17 (Cadência 12x30 e vizinhas)** —
      maior bloco, quebrado abaixo por subseção (não é mais uma caixa só):
  - [x] **2.1 (Gatilho)** — migrada em 18/09/2026: `Pré-vendas` →
        `FUNIL DE VENDAS`, `Em cadência` → `CONECTAR`
  - [x] **2.2 (Configurações do workflow)** — migrada em 19/09/2026: tinha
        uma menção sobrevivente a `"Em cadência"` na linha do `Allow
        Re-entry`, trocada para `CONECTAR`
  - [x] **2.3 nó 0.0b (portão sem telefone)** — migrado em 18/09/2026:
        "mover para `Nutrição`/`Descartado`" virou `Update Opportunity
        status = abandoned/lost`, sem sair de `CONECTAR`
  - [x] **2.4 nó 3 (portão de cada tentativa)** — migrado em 18/09/2026:
        `Em cadência` → `CONECTAR`
  - [ ] 2.5 (tabela das 12 tentativas) — sem nome de etapa, não deveria
        precisar de mudança; conferir na hora de montar
  - [x] **2.6 fim (depois de M3, 12 tentativas esgotadas)** — migrado em
        18/09/2026: "mover para `Nutrição`" virou `status = abandoned`,
        permanece em `CONECTAR`
  - [ ] 2.6.1, 2.7, 2.8, 2.9–2.9.4 (Split A/B, entrada na IA, interceptação
        de sinal) — ainda não conferidas linha a linha nesta migração;
        risco baixo (não parecem citar nome de etapa antigo nas leituras
        feitas até aqui, mas não foi grep dedicado)
  - [x] **2.10 (Cadência Inbound)** — migrada em 19/09/2026: gatilho trocado
        de `Pré-vendas`/`Em cadência` para `FUNIL DE VENDAS`/`CONECTAR`
        (nota explicando que são o mesmo objeto, igual à 2.1); nó 0.0b
        trocado de "Mover oportunidade → `Nutrição`/`Descartado`" para
        `Update Opportunity status = abandoned/lost`, espelhando o 0.0b já
        migrado da 2.3; portão da tentativa (nó 2) trocado para
        `CONECTAR`. Zero achado novo na migração em si: era tradução
        mecânica, a mesma tabela 1.0 já previa cada troca. **Achado
        posterior, na varredura de 19/09/2026** (conferência da rodada que
        fechou a 2.11): o portão do nó 2 ganhou `status é open`, e o Mestre
        de saída ganhou o nó 2b (`Remove from Workflow: Cadência Inbound`)
        — sem os dois, um lead inbound descartado pelo portão de higiene
        seguia recebendo TI2 a TI5, porque a limpeza só conhecia a
        `Cadência 12x30`
  - [x] **2.11 (Alerta de Speed-to-lead)** — migrada em 19/09/2026: gatilho
        trocado de `Pré-vendas`/`Em cadência` para `FUNIL DE
        VENDAS`/`CONECTAR`. Achado novo, não previsto na tabela 1.0: o
        portão (nó 2) não podia virar só "etapa é `CONECTAR`" — ganhou
        também `status é open`, porque o nó 0.0b (seção 2.3) pode descartar
        um lead sem telefone (`status = abandoned`/`lost`) sem tirá-lo de
        `CONECTAR`, antes de qualquer tentativa rodar. Sem o `status`, esse
        lead dispararia um alarme de speed-to-lead falso (a mesma classe de
        bug que a seção 3 e a 2.12 já documentaram, aqui em rótulo de
        alarme em vez de limpeza de fila). Detalhe completo na seção 2.11
        do `build-wesales.md`.
  - [x] **2.12 (Reengajamento 90 dias)** — migrada em 19/09/2026, era o
        maior pedaço que sobrava: gatilho trocado de `Opportunity Stage
        Changed → Nutrição` para `Contact Tag Added → nutricao-90d` (a
        tradução já estava anotada na tabela 1.0, linha `Nutrição`); nó 5
        ("Reentrada no funil") e o nó final de TR4 esgotada migrados para
        `CONECTAR`/`status`. Achado novo durante a migração, não previsto
        na tabela 1.0: o nó 5 agora reseta `status` para `open` junto com
        a etapa — sem isso o lead reativado chegaria a `CONECTAR` ainda
        com `status = abandoned`, e o portão do Mestre de saída (seção 3,
        "`CONECTAR` e `open`") leria a chegada como saída e disparia a
        limpeza no momento errado. Detalhe completo na seção 2.12 do
        `build-wesales.md`.
  - [ ] 2.13 (Regras de pausa) — conferir se cita etapa antiga
  - [ ] 2.14 (Distribuição de leads), 2.15 (Monitor de Capacidade), 2.16
        (Higiene de Número) — 2.16 nó 2 cita `Novo lead`/`Em cadência`/
        `Retorno agendado` num If/Else de lista, precisa virar
        `NOVO LEAD`/`CONECTAR` (sem `Retorno agendado`, que não é etapa)
  - [ ] 2.17 (Dashboard do Gestor) — cita pipeline `Pré-vendas`
- [x] **Seção 3 (Mestre de saída)** — migrada em 18/09/2026: mudança
      estrutural, não só nome — ganhou um segundo gatilho
      (`Opportunity Status Changed`, para `Lost`/`Abandoned`) porque, no
      modelo novo, a maioria das saídas de cadência (12 tentativas
      esgotadas, número errado, não ligar) não move mais etapa, só muda
      `status`; o portão (nó 1) trocou de "etapa é `Em cadência`" para
      "etapa é `CONECTAR` **e** `status` é `open`", que cobre os dois
      gatilhos com uma condição só. Detalhe do raciocínio e dos casos
      testados mentalmente: `build-wesales.md`, seção 3.
      **Corrigida de novo em 19/09/2026 (varredura da rodada da 2.11):** o
      nó 2 removia de **uma** régua (`Cadência 12x30`), e hoje são três —
      entraram os nós 2b (`Cadência Inbound`, seção 2.10) e 2c
      (`Reengajamento 90 dias`, seção 2.12). O portão do nó 1 estava certo;
      quem estava incompleto era a limpeza que vem depois dele, e o efeito
      era pior que o alarme falso da 2.11: régua continuando a ligar para
      quem já saiu.
- [x] **Seção 4 (Pós-ligação)** — migrada em 18/09/2026, junto com a
      seção 3 (são acopladas: é o Pós-ligação que decide se a saída é
      `status` ou movimento de etapa). Ramo `Atendeu` → `AGENDAR` (etapa,
      sem mudança de lógica). Ramos `Número errado` e `Não ligar` →
      `Update Opportunity status` (`abandoned`/`lost`), permanecem em
      `CONECTAR`. Ramo `Pediu retorno` perdeu o nó de mudança de etapa —
      `Retorno agendado` não existe mais, o lead fica em `CONECTAR` e a
      lista `Retornos` (8.4) já filtra só pelo campo.
- [x] **Seção 5 (Pós-agendamento)** — migrada em 19/09/2026: nó 1 trocado de
      "mover para `Reunião agendada`" para "mover para `NEGOCIAR`" (tabela
      1.0). **Publicado e ativo na tela antes desta migração de doc** (3
      inscritos, 3 ativos, confirmado por leitura de tela em 19/09/2026) —
      quem montou já usou o nome de etapa real; só a especificação escrita
      estava desatualizada.
  - [x] **5.1 (Loop do closer)** — migrada em 19/09/2026: os três ramos que
        saem da reunião (`Parcial`, `Não`/Timing errado, `Não`/outro motivo)
        trocaram "mover etapa" por `Update Opportunity status`
        (`abandoned`/`abandoned`/`lost`), permanecendo em `NEGOCIAR` — o
        ramo `Sim` não mexe em etapa nem status, é o closer que avança para
        `FORMALIZAR` por fora deste workflow. Achado: diferente da maioria
        das saídas de cadência (que mudam status dentro de `CONECTAR`),
        aqui a saída acontece depois do avanço para `NEGOCIAR` — o Mestre
        de saída não reage a isto de propósito, a limpeza de fila já rodou
        no momento da conexão (seção 4). Ainda não publicado na tela.
  - [x] **5.2 (Registro de Comparecimento)** — conferida em 19/09/2026: não
        cita etapa nenhuma ("não mexo em etapa aqui", já no próprio texto
        original) — nada para migrar, só o registro de que foi conferida.
  - [x] **5.3 (Recuperação de No-show) e 5.4 (SLA do Closer — No-show)** —
        migradas em 19/09/2026. `Reunião agendada` → `NEGOCIAR` em todos os
        portões; "descartar oportunidade" (ramo Descarte, 2º no-show) virou
        `Update Opportunity status = lost`; "mover para Nutrição" (fim do
        ramo Recuperação) virou `status = abandoned` — os dois sem sair de
        `NEGOCIAR`, exatamente o achado já previsto na seção 1.2. **Achado
        novo, não previsto:** todo portão de sanidade destas duas seções
        (5.3 nó 1, ramo Recuperação nós 6/10/14, 5.4 nós 1/5) checava só
        "etapa é `Reunião agendada`" — insuficiente pela mesma razão já
        documentada para a 2.11 e o Mestre de saída: o Loop do closer
        (seção 5.1) pode fechar o veredito (`status = abandoned`/`lost`)
        **sem tirar a oportunidade de `NEGOCIAR`**, e sem checar `status`
        também um `No Show` chegando depois reabriria a recuperação (NS1
        a NS3) ou repetiria o SLA do closer num lead cujo destino já foi
        decidido. Todos os portões ganharam `status é open` junto com a
        etapa. `Recuperação de No-show` já existe na tela como rascunho
        (não publicado); `SLA do Closer — No-show` ainda não existe.
- [ ] **Seção 6 (Qualificação por IA no WhatsApp)**
- [ ] **Seção 8 (Listas inteligentes)** — qualquer lista com filtro de
      etapa `Retorno agendado`/`Nutrição`/`Descartado` precisa trocar para
      filtro de campo/status
  - [x] **8.1 `Fila Quente`, 8.2 `Fila Telefone Hoje`, 8.3 `Fila WhatsApp
        Hoje`, 8.4 `Retornos`** — migradas em 18/09/2026 (`Em cadência` →
        `CONECTAR`, `Conectado` → `AGENDAR`, `Retorno agendado` caiu do
        filtro de 8.1 por já estar coberto por `CONECTAR`, e caiu de 8.4
        por a lista já filtrar só pelo campo `Resultado da tentativa`)
  - [ ] 8.5 em diante (`Sem resultado ontem`, 8.6–8.18) — ainda não
        conferidas linha a linha nesta migração
- [ ] **Seção 9 (Nota de qualificação e Prioridade)**
- [x] **`rotina-limpar-tarefas.md` (fora de `build-wesales.md`, achado em
      19/09/2026)** — este checklist só rastreava `build-wesales.md`; o
      prompt autocontido da rotina de manutenção de tarefas buscava
      oportunidades no pipeline `"Pré-vendas"` (nome que não existe na tela
      — é `FUNIL DE VENDAS`) e mapeava prefixo de tarefa pelas 7 etapas
      antigas, incluindo `Retorno agendado` como etapa própria (não é mais).
      Corrigido: PASSO 2 agora busca no pipeline real e também lê o
      `status` da oportunidade (não só a etapa) — sem isso, um lead que
      esgotou as 12 tentativas (`status = abandoned`, mas segue parado em
      `CONECTAR`) teria suas tarefas `[CADENCIA]` tratadas como válidas
      para sempre, porque etapa sozinha não diferencia "ainda na régua" de
      "saiu da régua sem mudar de etapa". PASSO 3 ganhou a tabela nova
      (etapa + status + `Resultado da tentativa`), incluindo `NEGOCIAR`
      aceitando `[CADENCIA]` para as tarefas de recuperação de no-show
      (seção 5.3, que mantém a oportunidade em `NEGOCIAR`). Achado ao
      revisar coerência entre documentos, não por relato de erro em
      produção — a rotina nunca chegou a rodar com o pipeline real, porque
      nenhuma oportunidade existe ainda na subconta.

**Não assuma que uma lista de seções já migradas está completa só porque
apareceu num commit anterior** — a lista muda a cada rodada que fecha mais
um pedaço (2.2 e 2.12, por exemplo, fecharam numa rodada automática em
19/09/2026, bem depois do commit que originou este aviso). Confie no
`[x]`/`[ ]` do checklist logo acima ("Seção 2 — subseções 2.1–2.17"), não em
qualquer lista fixa escrita em prosa — inclusive esta mesma frase, que por
isso não repete os números de seção pendentes.

**Não assuma que uma seção já reflete a mudança só porque outra foi
migrada** — verifique o `[x]` desta lista antes de confiar em qualquer
nome de etapa lido em `build-wesales.md`. Enquanto uma seção não estiver
marcada, todo nome de etapa antigo nela se traduz pela tabela 1.0 de
`build-wesales.md`.

**Fase 1 (pipeline em si) dá-se por concluída** — o pipeline está no
estado final decidido pelo dono, não pendente de correção. A tarefa que
continua aberta é só a de **documentação** (a lista acima), não a de
construção na tela.

---

## Fase 2 — Campos personalizados (verificação do que já foi criado)

**A Fase 1 acima segue sem checkbox marcado — pela ordem deste guia, a
Fase 2 nem deveria ter começado.** Mesmo assim, esta execução encontrou
**24 campos personalizados já criados na tela** via
`locations_get-custom-fields` (nenhum existia até a rodada em que o R-15
fechou, poucas horas atrás — todos com `dateAdded` entre 20:18 e 21:01
UTC de 18/09/2026). Como o trabalho manual já avançou fora da ordem
sugerida, esta seção registra o que foi conferido campo a campo contra
`campos-e-tags.md`, não um passo a passo de criação.

### O que bate com a especificação

22 dos 24 campos existentes batem em nome e tipo com `campos-e-tags.md`:
C-01, C-02, C-05 até C-24 (o intervalo pula C-03/C-04, ver abaixo), mais
Q-02 (`Site`) e Q-03 (`Instagram`). As opções de todo campo
`SINGLE_OPTIONS` conferido batem uma a uma com a tabela, com uma exceção
só cosmética (última seção abaixo).

### Dois campos que ainda faltam

`campos-e-tags.md` lista 24 linhas em "Controle da cadência" (C-01 a
C-24); só 22 dessas 24 estão na tela. Faltam:

- **C-03 · `WA não atendidas seguidas`** (`NUMERICAL`) — o seletor de
  canal (`build-wesales.md`, nós 0.2 e 3/4 do Pós-ligação, lista 8.1) lê e
  grava este contador para decidir quando 2 ligações de WhatsApp seguidas
  sem atender viram telefone (regra D-04 do `briefing-sdr.md`). Sem ele a
  Fase 5 não tem onde gravar esse contador.
- **C-04 · `Permissão WhatsApp`** (`SINGLE_OPTIONS`: Sim, Não, Não
  solicitado) — é a condição mais referenciada do projeto depois de
  `Tentativa nº`/`Resultado da tentativa`: aparece em pelo menos 14
  pontos do `build-wesales.md` (seletor de canal, reset de rodada,
  cadência inbound, reengajamento, mensagem MI-1, lista 8.1). A Fase 5
  não pode nascer sem ele.

### Um campo com o tipo errado

**C-11 · `Conexões telefone`** foi criado como **`PHONE`**, não
`NUMERICAL` (confirmado por `locations_get-custom-fields`:
`"dataType": "PHONE"`, `fieldKey: contact.conexes_telefone`). O
Pós-ligação (`build-wesales.md`, seção 4, ramo `Atendeu`, nó 1) grava
nele com `Math: Conexões telefone + 1` — um campo `PHONE` não tem ação
matemática de incremento, só guarda string de telefone formatada. Se a
Fase 5 montar esse nó em cima do campo como está hoje, a ação não vai
nem aparecer como opção válida na tela.

**Pesquisado nesta execução:** a HighLevel não permite trocar o
`dataType` de um campo depois de criado, em nenhuma tela — é apagar e
recriar, não editar (fontes de busca, `help.gohighlevel.com` segue
bloqueado pelo proxy deste ambiente, mesma limitação já registrada desde
o R-09; confiança média, mas convergente em várias fontes independentes:
`leadsflex.com`, `ghlbuilds.com`, `growthable.io`). **Isto não é uma
exclusão que esta rotina vai fazer** — regra 1 do projeto proíbe excluir
campo, e o conector `GHL CRM` desta sessão nem tem ferramenta de
apagar/criar campo. É uma decisão para quem está montando manualmente:
`contacts_get-contacts` confirma 0 contatos com esse campo preenchido
nesta subconta (a base inteira tem 6 contatos, nenhum com `customFields`
não vazio), então apagar e recriar como `NUMERICAL` não perde dado
nenhum — mas confirme isso ao vivo antes de apagar, é o tipo de ação que
a regra 2 do `briefing-sdr.md` pede para confirmar antes de fazer.

### Diferença cosmética, não bloqueia nada

A opção `Caixa Postal` de C-02 (`Resultado da tentativa`) foi criada com
"P" maiúsculo. **Corrigido em 19/09/2026:** `build-wesales.md`,
`campos-e-tags.md` e `script-de-ligacao.md` escreviam `Caixa postal`
(minúsculo) em todas as menções — ajustados para bater com a grafia real
da tela (`CONFERENCIA-CAMPOS.md`, Tabela C). Nunca foi um bug funcional
(quem monta o workflow seleciona a opção do dropdown, não digita o texto
do documento), só ficou registrado para não confundir quem lê.

### Resolvido ao vivo em chat, 18/09/2026 ~22h UTC

- [x] C-03 e C-04 criados — confirmado por `locations_get-custom-fields`:
      `WA não atendidas seguidas` (`NUMERICAL`) e `Permissão WhatsApp`
      (`SINGLE_OPTIONS`: Sim, Não, Não solicitado) existem, nome e tipo
      batendo com a especificação.
- [x] C-11 corrigido — `Conexões telefone` relido, `dataType` agora
      `NUMERICAL` (era `PHONE`). Quem estava montando editou o campo
      direto na tela em vez de apagar/recriar — funcionou, o tipo mudou.
      **Atualiza o achado anterior desta seção** ("não permite trocar o
      `dataType` depois de criado"): valeu a pena tentar editar antes de
      assumir que só apagando resolvia.
- [x] Confirmados por `locations_get-custom-fields` (`query_model=contact`)
      todos os C-01 a C-24 e Q-01 a Q-18, mais
      `Segmento` (criado como `TEXT`, decisão registrada em
      `campos-e-tags.md` por causa da resposta "diversos nichos" do dono)
      e `Data de retorno` (`DATE`, sem o par `Hora do retorno` — pendência
      menor, ver abaixo).

**Fase 2 dá-se por concluída.**

### Pendências que sobraram, baixa prioridade — não bloqueiam nada agora

Vários campos `SINGLE_OPTIONS` saíram com rótulos de opção diferentes dos
sugeridos em `campos-e-tags.md` (ex.: `Prazo` ficou "Pra ontem/Espera 30
dias/Este ano/Sem prazo" em vez de "Agora/Até 30 dias/1-3 meses/Sem
prazo"; `Tem time comercial`, `Investimento mensal em anúncios`,
`Decisor` e `Qualificação` — renomeado de "Qualificação preenchida por",
com opção `Automático` trocada por `Vendedor` — também mudaram). Nenhum
precisa ser recriado: a régua de qualificação (`build-wesales.md`, seção
9.1) é que precisa ser reescrita para usar os rótulos reais em vez dos
sugeridos — tarefa de documentação ainda pendente, registrada aqui para
não se perder. `Plataformas de anúncio` também saiu como `SINGLE_OPTIONS`
em vez de `MULTIPLE_OPTIONS` sugerido — decisão de quem montou, aceitável
(cliente só terá 1 plataforma principal registrada em vez de todas).
`Hora do retorno` (a segunda metade de S-01) não foi criada — sem ela a
lista `Retornos` ordena só por dia, não por horário exato; criar depois se
o volume de retornos justificar.

**Resolvido em 19/09/2026:** a régua de qualificação (seção 9.1 do
`build-wesales.md`) foi reescrita com os rótulos reais — era a "tarefa de
documentação ainda pendente" citada acima. Detalhe completo, e o que ainda
segue pendente (o tipo de `Plataformas de anúncio` e os três campos que a
tela criou sozinha), em `campos-e-tags.md` e `CONFERENCIA-CAMPOS.md`.

## Estado da montagem em 19/09/2026 (sessão ao vivo em chat)

**Publicados e testados:** `Porta de Entrada` (seção 1.3 — 40 oportunidades
criadas, L-09/L-09b fechados), `Mestre de saída` (seção 3 — falta só
apontar os "Remove from Workflow" para as quatro réguas: `Cadência 12x30`,
`Cadência Inbound`, `Reengajamento 90 dias` e `Qualificação por IA no
WhatsApp`, quando cada uma existir; as criadas até agora estão vazias, só
nome), `Interceptação de Sinal — Clique` e `— Resposta`
(seção 2.9, Trigger Link "Agendar com o closer" criado).

**Dois retoques de tela pendentes nessas peças já publicadas** (achados na
varredura de 19/09/2026, detalhe em `build-wesales.md`):

| Onde | O que mudar na tela | Por quê |
|---|---|---|
| `Mestre de saída`, depois do nó 2 | Acrescentar dois `Remove from Workflow`: `Cadência Inbound` e `Reengajamento 90 dias` — **os dois só entram quando esses workflows existirem na tela** (hoje nenhum dos dois existe, nem como rascunho: ver a lista lida ao vivo mais abaixo); a hora certa é no mesmo dia em que cada um for criado, não depois | A limpeza conhecia só a régua original; as outras duas continuariam ligando para quem já saiu. Este é o retoque que se esquece sozinho, porque só vira possível semanas depois do achado |
| `Interceptação de Sinal — Clique` e `— Resposta`, nó 2 | No If/Else, somar à condição de etapa: `status` da oportunidade **não é** `lost` | Um clique de quem pediu `Não ligar` (ou de número errado) virava tarefa `ligar agora`. `abandoned` continua passando de propósito — é o lead em nutrição esquentando, ver a nota na seção 2.9.2 |

**Em andamento, incompleto:** `Pós-ligação` (seção 4). Primeira tentativa
via IA generativa do construtor de workflow ("Construa usando IA") saiu
malformada — gatilho sem filtro, condição de vazio olhando campo errado,
6 ramos sem nenhuma ação dentro — abandonada. Reconstruído **manual, nó a
nó**, ao vivo em chat, mesmo dia. Estado atual:

- Gatilho `Contact Changed` com filtro `Resultado da tentativa` alterado — ok.
- Nó 1 (checagem de vazio) — ok, vazio encerra sem incrementar.
- Nó 2 (`fila-wa` → `Tentativas WhatsApp`/`Tentativas telefone`) — ok, os
  dois lados (Branch e None) incrementam certo. **Testado via API em
  contato sem tag: confirmado que incrementa `Tentativas telefone`.**
- Nó 3 (`Total de ligações` +1) — ok, duplicado nos dois lados do nó 2.
- **Defeito real encontrado e confirmado por teste:** o `Condition` de 6
  ramos (`Resultado da tentativa` = Atendeu/Caixa Postal/Não atendeu/
  Número errado/Pediu retorno/Não ligar), com todas as ações dos 6 ramos já
  montadas dentro (Atendeu com 9 ações; Caixa Postal e Não atendeu
  idênticos, duplicados um do outro; Número errado, Pediu retorno e Não
  ligar cada um com sua sequência própria) — **esse bloco de condição
  inteiro só existe do lado "Branch" (tem `fila-wa`, ou seja, tentativa por
  WhatsApp) do nó 2.** O lado "None" (tentativa por telefone, a maioria dos
  casos reais) só incrementa `Tentativas telefone` e termina — nunca chega
  nos 6 ramos. **Confirmado ao vivo:** contato de teste sem tag, `Resultado
  da tentativa = Atendeu`, ganhou `Total de ligações`/`Tentativas
  telefone`, mas nunca ganhou `Conexões telefone`, tag `conectado-hoje`,
  tarefa nem nota.
- **Atualização, mesmo dia, mais tarde:** o dono conseguiu conectar o lado
  "None" (telefone) ao `Condition` de 6 ramos (por duplicar+colar, depois
  de várias tentativas). Teste real confirmou que passou a funcionar até
  um ponto: `Conexões telefone` (dentro do ramo Atendeu) passou a
  incrementar certo pelo telefone também. Mas a cadeia **quebra logo
  depois** — os passos seguintes do ramo Atendeu (`Total de conexões`,
  `WA não atendidas seguidas`, tag `conectado-hoje`, remoção de tag,
  mudança de etapa pra `AGENDAR`, `Data conectado`, tarefa, nota) foram
  adicionados manualmente pelo dono (mesma receita de 8 passos da cópia
  WhatsApp), mas o teste seguinte **continuou parando no mesmo lugar**
  (`Conexões telefone` incrementa, nada depois disso) — ou os 8 nós não
  salvaram a conexão entre si corretamente, ou há um nó solto/mal ligado
  entre `Conexões telefone` e `Total de conexões` nessa cópia específica.
  Também foi notado, sem confirmar, um terceiro "Branch" (deveria ter só
  2: `Branch`/`None`) no `If/Else` de `fila-wa` interno do Atendeu nessa
  cópia — pode ser resíduo do processo de duplicar, vale conferir primeiro
  na próxima sessão.
- **Resolvido, mesmo dia, madrugada:** o método de diagnóstico nó-a-nó
  (testar via API trocando `Resultado da tentativa`, depois ler o log de
  `Registros de execução` pra ver exatamente onde parou) achou e corrigiu
  **3 buracos separados** na cópia telefone, todos do mesmo tipo — a
  duplicação colava o nó de entrada de cada sub-ramo mas perdia a conexão
  logo depois do primeiro `Math operation`:
  - Ramo `Atendeu`: parava em `Conexões telefone`, faltavam os 7 passos
    seguintes (`Total de conexões`, `WA não atendidas seguidas`, tag
    `conectado-hoje`, `Remove Tag`, mudança de etapa pra `AGENDAR`,
    `Data conectado`, tarefa, nota) — corrigido, testado via API: etapa
    moveu pra `AGENDAR`, tags e notas certas (a tarefa aparece como
    "skipped" no log só porque o contato de teste não tem dono atribuído —
    não é bug, é esperado o distribuidor de leads atribuir dono antes
    disso em produção).
  - Ramo `Número errado`: na verdade **não estava quebrado** — o log
    mostrou que rodou até o fim (`Criar ou atualizar oportunidade`
    executado), só pareceu travado porque o status já estava `lost` de um
    teste anterior (`Não ligar`), sem mudança visível.
  - Ramo `Caixa Postal`: parava em `WA não atendidas seguidas`, faltavam
    `Remove Tag` (`fila-tel`/`fila-wa`) e `Add Tag` (`limpar-tarefas`) —
    corrigido e confirmado.
  - Ramo `Não atendeu` (duplicado do Caixa Postal): estava **vazio por
    dentro**, terminava direto ao entrar no `Branch` — reconstruído do
    zero com a mesma receita de 3 passos do Caixa Postal, confirmado pelo
    log.
  - Ramos `Pediu retorno` e `Não ligar`: confirmados funcionando sem
    nenhuma correção (tag `fila-quente`/`Prioridade=5` e DND completo +
    status `lost` + nota "Opt-out registrado", respectivamente).
  **Os 6 ramos do lado telefone estão confirmados, um por um, via log de
  execução real.** Descoberta lateral: trocar o valor de teste rápido
  demais (menos de ~5s) faz o GHL pular o disparo inteiro ("Add to
  workflow: skipped" ou nem chega a logar) — espaçar os testes evita
  perder tempo interpretando resultado de execução que nunca rodou.
- **Falta só publicar** (toggle "Publicar", ainda em rascunho no fim desta
  sessão) antes de seguir pro próximo da fila (seção 5, "Pós-agendamento").

## Estado da montagem em 19/09/2026, mais tarde (lista de workflows lida ao vivo em chat)

O dono colou a lista de workflows da tela (`Automação → Fluxos de
trabalho`), que este conector não lê por API — é a fonte mais confiável
disponível para o estado real de publicação. Estado por nome, ordem
alfabética da própria tela:

| Workflow | Status | Inscritos (total / ativos) |
|---|---|---|
| Cadência 12x30 | **Rascunho** | 0 / 0 |
| Interceptação de Sinal — Clique | Publicado | 3 / 0 |
| Interceptação de Sinal — Resposta | Publicado | 1 / 0 |
| Mestre de saída | Publicado | 5 / 0 |
| Porta de Entrada | Publicado | 80 / 0 |
| **Pós-agendamento** | **Publicado** | **3 / 3** |
| Pós-ligação | Publicado | 24 / 0 |
| Qualificação por IA no WhatsApp | **Rascunho** | 0 / 0 |
| Recuperação de No-show | **Rascunho** | 0 / 0 |

**Não aparecem na lista — ainda não criados na tela, nem como rascunho:**
Alerta de Speed-to-lead (2.11), Cadência Inbound (2.10), Contador de
Toques (2.19), Loop do closer (5.1), Monitor de Capacidade (2.15),
Reengajamento 90 dias (2.12), Registro de Comparecimento (5.2), SLA do
Closer — No-show (5.4). A lista está em ordem alfabética por nome; se
qualquer um destes existisse, apareceria intercalado entre os que
aparecem (ex.: "Alerta..." antes de "Cadência...", "Loop..." entre as duas
"Interceptação..." e "Mestre...") — ausência na posição esperada é
evidência de que não existem, não só de estarem fora desta página.

**Achado que muda a prioridade do que montar a seguir:** `Pós-ligação` e
`Mestre de saída` estão publicados (a seção anterior deste arquivo já
tinha essa dúvida em aberto — resolvida: os dois foram publicados depois
daquela sessão). Mas **`Cadência 12x30` — o motor principal do projeto —
segue em rascunho**, com 0 inscritos. Isso significa que nenhum dos 40
leads já em `NOVO LEAD` (Porta de Entrada) está de fato rodando as 12
tentativas ainda, mesmo com Pós-ligação e Mestre de saída prontos para
recebê-los quando a cadência começar a alimentá-los. `Qualificação por IA
no WhatsApp` segue rascunho — não confirmado ainda se é o placeholder vazio
original (criado só para o Mestre de saída ter o que apontar, ver seção
anterior) ou se já ganhou o prompt de IA por dentro.

**Ordem prática a partir daqui**, dado que a seção 5 (Pós-agendamento) já
está publicada e ativa: montar 5.1 (Loop do closer) e 5.2 (Registro de
Comparecimento), que não existem ainda; depois 5.3/5.4 (a `Recuperação de
No-show` já existe como rascunho, falta o `SLA do Closer` par dela e
publicar as duas juntas); só depois disso publicar `Cadência 12x30` — ela
já emite a tag `toque` (F-04) desde o primeiro nó, então o ideal é o
`Contador de Toques` (passo 2 da "Ordem de montagem") existir antes dela
ir ao ar, senão a tag acumula sem o contador para reagir (não quebra nada,
só atrasa o benefício do F-04).
