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

> **Aviso de 23/09/2026 (G-14, `ROADMAP-SALES-ENGAGEMENT.md`) — este
> documento não é a foto mais recente da conta.** As seções "Estado da
> montagem"/"Estado final" abaixo descrevem a subconta até 22/09/2026. No
> dia seguinte o dono aplicou `PLANO-MULTICANAL.md` inteiro ao vivo (D1-D14):
> a etapa `AGENDAR` foi renomeada para `REUNIÃO DE DIAGNÓSTICO` (mesmo id),
> o ramo `Atendeu` deixou de mover para lá (G-13 — agora fica em `CONECTAR`,
> fase "fechar horário"), o workflow `AGENDAR Estagnado`/W17d foi
> despublicado, e mais de 20 workflows foram criados ou reformulados pela
> API interna (`wesales/tools/`, fora do que este MCP alcança). Antes de
> seguir qualquer célula com "AGENDAR" ou qualquer linha "dá para fazer
> HOJE" das seções abaixo como instrução válida para hoje, leia
> `PLANO-MULTICANAL.md` (estado da obra mais recente) e confira contra a
> tela — este arquivo não foi reescrito depois de 22/09, só remendado nos
> pontos abaixo que davam instrução ativamente errada.

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
- [ ] **Fase 5 — Os workflows restantes**, na ordem da seção "Ordem de montagem" do `build-wesales.md` — **configuração exata de cada nó (ação, campo, operador, valor) em `IMPLEMENTACAO-WORKFLOWS.md`** (Parte 2; a Parte 1 cobre campos, tags, calendário, formulário e listas, e a Parte 3 a operação diária), escrito em 21/09/2026 para montar à mão, sem "Construir com IA"
- [ ] **Fase 6 — Listas inteligentes** (todas as da seção 8 do
      `build-wesales.md`, contagem cresce com o roadmap — não fixar número
      aqui, é a mesma armadilha que este projeto já corrigiu para campo e
      tag) — **antes de montar, decida a coluna `Empresa`:** ela aparece em
      vários lugares do `build-wesales.md` e está **vazia em todos os 50
      contatos** (nem o campo nativo nem o personalizado têm dado — nada a
      montante coleta nome de empresa). Montar as listas agora significa
      montar com uma coluna morta em cada uma. Candidatas com dado hoje e a
      recomendação: `CONFERENCIA-CAMPOS.md`, Tabela J. **Teste de 10 segundos
      antes de configurar a ordenação das 8.1, 8.2, 8.3, 8.4, 8.16, 8.18 e
      8.19:** a tela permite um segundo critério de ordenação (`, depois`)?
      Ninguém verificou isso ainda (achado de 22/09/2026 em `build-wesales.md`,
      seção 8.4, e em `APRENDIZADOS-CRM.md`) — se a tela só aceitar uma
      coluna, use o Plano B já escrito ali (ordena pelo primeiro nível, o
      segundo fica como coluna visível) em vez de forçar ou deixar a lista
      pela metade. Registre o resultado (aceita ou não) em
      `APRENDIZADOS-CRM.md` assim que descobrir — é a única forma de
      verificação que este projeto não conseguiu fazer por pesquisa.
      **E não espere a Fase 6 para isso:** as duas listas do F-10 (`Entrada —
      últimas 24h` / `— 7 dias`, seção 8.25 do `build-wesales.md`) **não
      dependem da decisão da coluna `Empresa`** — foram redefinidas sem ela em
      22/09 —, montam com ordenação de um nível só e portanto podem ser feitas
      **hoje**. Monte a `Entrada — últimas 24h` primeiro de todas as listas do
      projeto: é o único monitor de entrada que existe (e a entrada está
      parada), não espera ninguém, e com a tela aberta você responde de lambuja
      a pergunta que decide o desenho das outras sete
- [ ] **Fase 7 — Teste com os 5 contatos fictícios** (já existem no CRM, seção 10)
- [ ] **Fase 8 — Pausar Workflows em Datas Específicas** (feriados/férias)
- [ ] **Fase 9 — Number Validation** (opcional)
- [ ] **Fase 10 — Dashboard + Custom Metrics**

---

## Fase 1 — Pipeline "Pré-vendas" (reaproveitando o `FUNIL DE VENDAS`)

> ### ⛔ FASE CONCLUÍDA — NÃO EXECUTE NADA DESTA SEÇÃO
>
> **Lida em 21/09/2026.** O pipeline real tem **5 etapas** (`NOVO LEAD`,
> `CONECTAR`, `AGENDAR`, `NEGOCIAR`, `FORMALIZAR`), decisão do dono em
> 18/09 — a tabela de 7 etapas mais abaixo foi **recusada** por ele e
> está aqui só como histórico. A seção "Resolvido ao vivo em chat" ao
> final traz o estado verdadeiro.
>
> **Duas instruções desta seção ficaram perigosas com o tempo:**
>
> 1. **"Excluir" 7 etapas.** A justificativa escrita era uma medição de
>    18/09: *"0 oportunidades no pipeline inteiro… pode apagar sem medo"*.
>    Isso **venceu**: em 21/09/2026 o pipeline tem **50 oportunidades**
>    (47 em `NOVO LEAD`, 3 em `NEGOCIAR`), lidas por
>    `opportunities_search-opportunity`. Excluir etapa com oportunidade
>    dentro é exatamente o que a regra 1 do projeto proíbe.
> 2. **Renomear para os 7 nomes antigos.** Hoje isso desfaria as etapas
>    reais e quebraria todo workflow publicado, que consulta `CONECTAR` e
>    `NEGOCIAR` pelo nome.
>
> **Lição, e o motivo de este aviso existir:** um número medido dentro de
> uma instrução ("hoje são 0") é verdade com data de validade, e a
> instrução que depende dele não avisa quando vence. Instrução destrutiva
> justificada por medição precisa ser refeita na hora de executar, nunca
> lida de um documento escrito dias antes.

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

*(Checklist histórico, da versão de 7 etapas que o dono recusou — o que
vale hoje está na seção "Resolvido ao vivo em chat" logo abaixo.)*

- [ ] ~~O pipeline tem exatamente 7 etapas, na ordem da tabela acima~~ —
      **tem 5**, e é o correto
- [ ] ~~Nenhuma das 7 antigas sobrou~~
- [ ] Visibilidade restrita configurada — este item continua valendo

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
  - [x] **2.6.1, 2.7, 2.8, 2.9–2.9.4 (Split A/B, entrada na IA, interceptação
        de sinal)** — conferidas em 21/09/2026, `grep` dedicado (linhas
        615-853 de `build-wesales.md`): zero nome de etapa antigo. As
        quatro já tinham sido escritas ou corrigidas direto contra as 5
        etapas reais em rodadas anteriores (2.9.2/2.9.3 já usam
        `CONECTAR`/`status não é lost`, achado ao vivo em chat de
        19/09/2026) — nada a migrar, só faltava marcar aqui.
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
  - [x] **2.13 (Regras de pausa)** — conferida em 19/09/2026: uma menção
        sobrevivente ("a etapa `Em cadência` resolve...", texto corrido, não
        nó) trocada para `CONECTAR`. Nada mais a migrar — a seção já falava
        só em tag `pausado` e no recurso nativo de pausa por data.
  - [x] **2.14 (Distribuição de leads)** — conferida em 19/09/2026: zero
        nome de etapa antigo em nó ativo. A única citação a `Nutrição` é
        narrativa ("é assim que ele chegou a `Nutrição`", explicando por que
        o Reengajamento não precisa de sorteio próprio de dono) — mesmo uso
        informal que a 2.12 e a seção 1.2 já fazem para o status `abandoned`,
        não um gatilho ou portão comparando contra etapa inexistente.
  - [x] **2.15 (Monitor de Capacidade)** — conferida em 19/09/2026: sem
        nome de etapa nenhum, antigo ou novo — a seção inteira gira em torno
        de tag de fila (`fila-tel`/`fila-wa`) e Custom Metric, nada a migrar.
  - [x] **2.16 (Higiene de Número)** — migrada em 19/09/2026: o gatilho
        ("roda também para quem já saiu de `Em cadência`") e o nó 2 do Ramo
        A (`Novo lead`/`Em cadência`/`Retorno agendado` vs. `Conectado`/
        `Reunião agendada`/`Nutrição`/`Descartado`) trocados para
        `NOVO LEAD`/`CONECTAR` **e** `status é open` vs. `AGENDAR`/
        `NEGOCIAR` ou `status` já `abandoned`/`lost` — mesmo reforço de
        `status` que a 2.11, o Mestre de saída, a 2.12 e a família 5.3/5.4
        já precisaram. O nó 3 ("Mover oportunidade → `Nutrição`/
        `Descartado`") virou `Update Opportunity status = abandoned/lost`,
        espelhando o 0.0b já migrado da 2.3/2.10. Detalhe completo na seção
        2.16 do `build-wesales.md`.
  - [x] **2.17 (Dashboard do Gestor)** — conferida em 19/09/2026: as citações
        a `Pré-vendas` (nome do dashboard, filtro do widget "Opportunities")
        são o apelido documentado do pipeline na seção 1, não um nome de
        etapa órfão — nada a migrar. Zero nome de etapa antigo na seção.
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
- [x] **Seção 6 (Qualificação por IA no WhatsApp)** — migrada em
      21/09/2026: o nó 4 da saída ("Como nota < 25 e `Budget` = `Não tem`
      → mover para `Nutrição`") virou `Update Opportunity status =
      abandoned` (etapa fica onde estava — tabela 1.0), + tag
      `nutricao-90d`, espelhando o mesmo achado já aplicado em toda saída
      de cadência (2.3, 2.10, 2.16, Loop do closer). Único nó ativo da
      seção com nome de etapa antigo.
- [x] **Seção 8 (Listas inteligentes)** — fechada em 21/09/2026, qualquer
      lista com filtro de etapa `Retorno agendado`/`Nutrição`/`Descartado`
      já trocou para filtro de campo/status
  - [x] **8.1 `Fila Quente`, 8.2 `Fila Telefone Hoje`, 8.3 `Fila WhatsApp
        Hoje`, 8.4 `Retornos`** — migradas em 18/09/2026 (`Em cadência` →
        `CONECTAR`, `Conectado` → `AGENDAR`, `Retorno agendado` caiu do
        filtro de 8.1 por já estar coberto por `CONECTAR`, e caiu de 8.4
        por a lista já filtrar só pelo campo `Resultado da tentativa`)
  - [x] **8.5 a 8.15, 8.18, 8.19** — conferidas em 21/09/2026: zero nome de
        etapa antigo em filtro ativo. 8.9-8.12 tinham uma frase narrativa
        comparando contra `Reunião agendada` como hipótese descartada
        (explicando por que **não** usar filtro de etapa) — atualizada
        para `NEGOCIAR` só por precisão, sem mudar nenhum filtro real.
  - [x] **8.16 `Fila do Dia — Total`** — migrada em 21/09/2026: a
        comparação narrativa "oportunidade em `Reunião agendada`, não em
        `Em cadência`" virou `NEGOCIAR`/`CONECTAR`.
  - [x] **8.17 `Recuperação de No-show`** — migrada em 21/09/2026: o
        filtro ativo "etapa da oportunidade = `Reunião agendada`" (nome
        que não existe mais na tela — bug real, não só narrativa) virou
        `NEGOCIAR`, e a explicação abaixo da tabela também.
- [x] **Seção 9 (Nota de qualificação e Prioridade)** — migrada em
      21/09/2026: as faixas C/D de 9.1 ("etapa `Nutrição`"/"etapa
      `Descartado`") viraram `status abandoned`/`status lost` (etapa fica
      onde estava — tabela 1.0); a regra 1 de 9.2 comparava também contra
      `etapa = "Retorno agendado"` (nome inexistente na tela) num `ou` que
      nunca fazia diferença — removida, sobrando só `Resultado da
      tentativa = Pediu retorno`, mesmo raciocínio já aplicado à lista 8.4.
- [x] **Checklist de teste (Seção 10)** — migrado em 21/09/2026: os
      cenários e as verificações citavam etapa antiga em vários pontos
      (`Em cadência`, `Conectado`, `Reunião agendada`, `Retorno agendado`,
      `Nutrição`, `Descartado`) — reescritos com o nome real e, onde o
      destino é `status` e não etapa (item 12, `Pediu retorno`; itens
      2/4/24/27/30/31, saída por `status`), com a distinção explícita
      entre os dois, para quem rodar o teste não confundir "mudou etapa"
      com "mudou status" no meio de uma verificação manual.
      Achado à parte, fora do escopo de nome de etapa: a frase final do
      checklist mandava **apagar** as 5 oportunidades de teste — viola a
      regra 1 do projeto (nunca excluir oportunidade). Corrigida para
      marcar `status = lost` em vez de excluir.
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

**Resolvido em 22/09/2026:** `Hora do retorno` foi criada na tela em
21/09/2026 23:18 (o parágrafo acima ficou desatualizado no dia seguinte à
sua própria escrita) — a lista `Retornos` (seção 8.4 do `build-wesales.md`)
já ordena por `Data de retorno` e depois por `Hora do retorno`, fechando a
L-01 do `briefing-sdr.md` por inteiro. Falta só a montagem manual na tela.

## Estado da montagem em 19/09/2026 (sessão ao vivo em chat)

**Publicados e testados:** `Porta de Entrada` (seção 1.3 — 40 oportunidades
criadas, L-09/L-09b fechados), `Mestre de saída` (seção 3 — o nó 2 trocou de
quatro `Remove from Workflow` nomeados para um só `Remove Workflows` → `All
Except Current Workflow`, F-05, 21/09/2026: não depende mais de nenhuma
régua existir antes, dá para fazer hoje — ver retoque abaixo),
`Interceptação de Sinal — Clique` e `— Resposta`
(seção 2.9, Trigger Link "Agendar com o closer" criado).

**Retoques de tela pendentes nessas peças já publicadas** (achados nas
varreduras de 19 e 21/09/2026, detalhe em `build-wesales.md` — a lista cresce
a cada achado, então não vale contar aqui; a fonte é esta tabela). A coluna
"Quando" separa o que dá para fazer **hoje** do que espera um workflow que
ainda não existe:

| Onde | O que mudar na tela | Por quê |
|---|---|---|
| **`Pós-ligação`, ramo `Atendeu`, nó 2 — FALTANDO na tela, dá para fazer HOJE** | Inserir o `Math: Total de conexões + 1` que a especificação já pede, logo depois do If/Else que incrementa `Conexões WhatsApp`/`Conexões telefone` | **Provado pelo dado, não suposto:** no contato "teste atendeu", `Conexões telefone` = 8 e `Total de conexões` **vazio**. O nó 1 do ramo roda (8 conexões contadas), o nó 2 não existe ou não grava. O par vizinho fecha certo (`Tentativas telefone` = 24 e `Total de ligações` = 24), o que prova que o mecanismo de Math funciona — o que falta é este nó. **Nota de 23/09/2026 (G-18):** o dump de `Pós-ligação v2` confirma que o caminho "cópia 1, telefone" (alcançável só quando `fila-wa` está presente, herdado de antes de `d52e61d`) é mesmo um beco sem saída — mas hoje é código morto, porque a régua 100% telefone nunca deixa `fila-wa` presente nesse ponto; o caminho que roda de verdade (`fila-wa` ausente) já tem este Math completo. Corrigir esta linha continua barato e não tem contraindicação, só não é mais urgente — detalhe em `ROADMAP-SALES-ENGAGEMENT.md`, G-18 |
| **`Pós-agendamento`, nó 4 (Math em série da `Nota de qualificação`) — dá para fazer HOJE** | Abrir o nó e conferir campo de origem e de destino de cada Math da série; refazer clicando campo por campo, sem o assistente de IA | **Provado pelo dado:** os 3 leads em `NEGOCIAR` têm `Investimento mensal`, `Decisor`, `Budget` e `Prazo` **preenchidos** (não é falta de entrada) e `Nota de qualificação` **vazia** — e têm `Prioridade` = 5, que é o nó **5**. O fluxo passou pelo nó 4 e saiu sem escrever: Math com campo não selecionado, o mesmo defeito que o assistente de IA já produziu no Pós-ligação (`APRENDIZADOS-CRM.md`) |
| **`Pós-ligação`, novo nó 3b — dá para fazer HOJE** | Depois do nó 3 (`Total de ligações`), inserir `Remove Contact Tag` de `fila-quente`. Tem de ser **depois** do nó 2, que lê `fila-wa` para escolher o contador | `fila-quente` é aplicada em 4 lugares e removida em 2, nenhum deles o caso normal ("o sinal foi trabalhado"). Lead que clica, é ligado e não atende fica na `Fila Quente` (8.1) para sempre — a fila mais prioritária é a que apodrece primeiro. Já tem 1 contato assim |
| **`Mestre de saída`, nó 1 — dá para fazer HOJE, e é o mais urgente da tabela** | Trocar a condição de `CONECTAR` **e** `open` para: `status` é `open` **e** etapa é **uma de** `NOVO LEAD`, `CONECTAR` → encerra | Medido no dado (21/09): **os 10 leads nascidos depois deste workflow ir ao ar chegaram com `limpar-tarefas`** e uma nota "Saída de cadência" — porque a Porta de Entrada cria em `NOVO LEAD`, o gatilho pega qualquer etapa de destino, e o portão não reconhecia chegada. Suja o histórico de todo lead novo e disputa com a rotina horária de limpeza |
| **`Mestre de saída`, novo nó 0 — dá para fazer HOJE** | Inserir, **antes** do If/Else que hoje é o primeiro nó, um `Remove Contact Tag` de `novo-lead-estagnado` (F-05, seção 2.20) | Achado em 21/09 ao desenhar o Monitor de Saúde: o portão do nó 1 encerra em no-op exatamente na transição `NOVO LEAD` → `CONECTAR`, que é como este alerta se resolve — pôr a tag na lista do nó 4 não funcionaria, porque aquele nó nunca é alcançado nessa transição. Não depende de nenhum workflow novo: é o único retoque desta tabela que não espera nada |
| **`Mestre de saída`, nó 4 — dá para fazer HOJE, mas depende do workflow novo existir para valer algo** | Somar `fila-travada` à lista de `Remove Contact Tag` do nó 4 (F-05, seção 2.21) | Achado em 21/09 ao desenhar a peça 2 do Monitor de Saúde: diferente de `novo-lead-estagnado`, este alerta se resolve numa saída de cadência de verdade — a mesma transição que o nó 4 já alcança pela via normal —, então basta somar à lista existente. A edição em si não depende do workflow novo `Fila Travada` (seção 2.21) estar publicado, mas só limpa alguma coisa depois que ele existir e começar a aplicar a tag |
| **`Mestre de saída`, nó 4 — dá para fazer HOJE, mesma condição da linha acima** | Somar `conectar-estagnado` à lista de `Remove Contact Tag` do nó 4 (F-05, seção 2.22) | Achado em 21/09 ao desenhar a peça 3 do Monitor de Saúde: mesmo raciocínio da linha `fila-travada` — este alerta também se resolve numa saída de cadência de verdade, então basta somar à lista existente. Só limpa alguma coisa depois que o workflow novo `Cadência Sem Avanço` (seção 2.22) existir e começar a aplicar a tag |
| ~~`Mestre de saída`, nó 2 — trocar pela ação `All Except Current`~~ **CANCELADO no mesmo dia** | **Não faça esta troca.** Os nós 2/2b/2c/3 nomeados continuam valendo neste workflow (`build-wesales.md`, seção 3, nota "Por que este workflow — e só ele") | `All Except Current Workflow` protege o workflow atual e corta o de **quem o chamou** — e o Mestre de saída é disparado justamente por outro workflow mexendo na etapa, ainda em execução. Mataria os três lembretes de toda reunião agendada (Pós-agendamento, nós 8-10) e a tarefa `[CONECTADO]` de toda conexão (Pós-ligação, nós 7-9), em momentos diferentes a cada vez. A ação continua certa nos outros três lugares desta tabela |
| `Mestre de saída`, nó 6 (nota) | Trocar `{{opportunity.pipeline_stage}}` pelo token real de "Pipeline Stage" do seletor `{}` | A nota gravada renderiza a etapa em branco (`Saída de cadência · etapa:  · status: open`) — o token documentado não é o que o GHL usa; `{{opportunity.status}}` renderiza certo |
| `Pós-ligação`, ramo `Atendeu`, nó A2 | Conferir/recriar o `Math: Total de conexões + 1` | 24 execuções de teste: `Conexões telefone` = 8, `Total de conexões` vazio — o nó não existe ou grava em outro campo |
| **`Resultado da tentativa` (C-02) — workflow novo, dá para fazer quando alguém abrir a tela** | Acrescentar a opção `Desqualificado` no campo (Configurações → Campos personalizados), e no `Condition` do nó 4 do `Pós-ligação` acrescentar o 7º ramo `Desqualificado` com as ações D1-D7 (`build-wesales.md`, seção 4; `IMPLEMENTACAO-WORKFLOWS.md`, W4) | Fecha a lacuna L-08 (`briefing-sdr.md`, R-18 no roadmap): hoje `Atendeu` é a única saída de uma ligação atendida, e o ramo sempre cria a tarefa `[CONECTADO] Qualificar e agendar` mesmo quando a conversa já mostrou que não há fit — poluindo a agenda do closer ou obrigando o SDR a desfazer na mão. Opção nova e ramo novo, nenhum dos dois sai por API |
| `Loop do closer` (`Post-Meeting Closer Loop`) | **Refazer do zero, manual** (`IMPLEMENTACAO-WORKFLOWS.md`, W6); apagar os nós da IA | Teste por API em 21/09 18:44 UTC não disparou (rascunho); as condições da IA comparam `Tags`, `Rescheduled`, `score`, `Last appointment at` — nenhum existe |
| **`Lost Reason` (Settings → Custom Fields) — pré-requisito de F-12, dá para fazer HOJE, antes ou junto do ramo `Desqualificado` acima** | Criar os 5 valores (`Sem fit`, `Sem budget`, `Não é decisor`, `Concorrente`, `Duplicado ou já cliente` — os mesmos de `Motivo da desqualificação`, C-16, menos `Timing errado`) | Sem os 5 valores existirem, o D6 do `Pós-ligação` e o nó 4 do `Loop do closer` não têm o que selecionar no `Lost Reason` da ação `Update Opportunity` (`build-wesales.md`, seção 4.1, F-12) — campo reservado da plataforma, não aparece em `locations_get-custom-fields`, não sai por API |
| **`Pós-ligação`, ramo `Não ligar`, nó 4 — dá para fazer HOJE** | Trocar o `Remove from Workflow` nomeado por `Remove Workflows` → `All Except Current Workflow` (`build-wesales.md`, seção 4, ramo `Não ligar`, nó 4) | O mais caro dos quatro lugares com esta lista: na janela entre o nó 4 e a limpeza do Mestre de saída, cai tarefa de ligação para quem acabou de pedir para não ser procurado. F-05, achado de 21/09/2026 — mesmo motivo e mesma troca da linha do `Mestre de saída` acima, e **também não depende de nenhum workflow novo existir** |
| **`Pós-agendamento`, nó 3 — dá para fazer HOJE** | Trocar o `Remove from Workflow` nomeado (seis réguas, incluindo `Recuperação de No-show`/`SLA do Closer — No-show`) por `Remove Workflows` → `All Except Current Workflow` (`build-wesales.md`, seção 5, nó 3) | Mesma lista incompleta do Mestre de saída, um nível abaixo, e a mais longa das quatro. F-05, achado de 21/09/2026: cobre `Recuperação de No-show`/`SLA do Closer — No-show` (R-12) e qualquer régua futura sem precisar nomear nenhuma — também não depende de nenhum workflow novo existir |
| `Interceptação de Sinal — Clique` e `— Resposta`, nó 2 | No If/Else, somar à condição de etapa: `status` da oportunidade **não é** `lost` | Um clique de quem pediu `Não ligar` (ou de número errado) virava tarefa `ligar agora`. `abandoned` continua passando de propósito — é o lead em nutrição esquentando, ver a nota na seção 2.9.2 |
| `Interceptação de Sinal — Resposta`, gatilho — achado em 21/09/2026 (R-17) | Acrescentar filtro `Doesn't Contain` (uma linha por frase de opt-out) e criar o workflow novo `Opt-out por Palavra-chave` (`build-wesales.md`, seção 2.9.5) | Este workflow **já está publicado** (1 inscrito, tabela abaixo) e hoje trata qualquer resposta de WhatsApp — incluindo "pare, não me manda mais mensagem" — como sinal quente, gerando tarefa `ligar agora` para quem pediu silêncio. Baixa exposição enquanto a `Cadência 12x30` segue em rascunho; cresce sozinha quando ela publicar — priorize antes disso |
| ~~`Mestre de saída`, nó 0 — dá para fazer HOJE~~ **NÃO FAÇA — premissa superada (G-14, 23/09/2026)** | ~~Somar `agendar-estagnado` à lista de `Remove Contact Tag` do nó 0~~ | Linha escrita em 21/09 para a tag `agendar-estagnado`/T-19 (F-05 peça 5), que o G-13 já marcou "não recomendada para aprovação" em `campos-e-tags.md` e `APROVADO.md`: o workflow que a aplicaria (`AGENDAR Estagnado`/W17d) foi despublicado em 23/09 porque `REUNIÃO DE DIAGNÓSTICO` só é alcançada com reunião marcada — "24h em AGENDAR sem reunião" não pode mais acontecer. T-19 segue `[ ]`; se algum dia for aprovada, é com o desenho revisado (`build-wesales.md`, seção 2.23), não este |
| **`Mestre de saída`, nó 4 — dá para fazer HOJE, mas depende do workflow novo existir para valer algo** | Somar `retorno-vencido` à lista de `Remove Contact Tag` do nó 4 (F-05, seção 2.24) | Achado em 21/09 ao desenhar a peça 6 do Monitor de Saúde: rede de segurança para quando o lead sai de `CONECTAR`/`open` por um caminho que não passa pelo Pós-ligação — a limpeza principal é o nó 3c do Pós-ligação (linha abaixo) |
| **`Pós-ligação`, novo nó 3c — dá para fazer HOJE** | Depois do nó 3b (`Remove Contact Tag: fila-quente`), inserir `Remove Contact Tag: retorno-vencido`, incondicional, antes da ramificação do nó 4 (F-05, seção 2.24) | Achado em 21/09 ao desenhar a peça 6: o caminho mais comum de recuperação (o SDR liga de volta e reclassifica `Resultado da tentativa`) não muda etapa nem `status` na maioria dos resultados — o Mestre de saída nunca dispara para limpar. O gatilho deste workflow (`Resultado da tentativa` alterado) já é a definição de "alguém agiu sobre o lead", mesmo raciocínio já usado para o nó 3b |
| **`Pós-agendamento`, nós 7-10 — dá para fazer HOJE se o número de WhatsApp já existir na subconta, senão espera o passo 1 do G-05** | Inserir `WhatsApp: Customer Service Window Check` antes de cada um dos quatro `Send WhatsApp` e ramificar (dentro da janela: texto livre já publicado; fora da janela: modo Template) + um `Update Contact Field: Template usado` (`PA-CONF`/`PA-R24`/`PA-R3H`/`PA-R30`) depois de cada envio (`build-wesales.md`, seção 5; `IMPLEMENTACAO-WORKFLOWS.md`, W5) | G-05, peça 2 (22/09/2026): os quatro envios são texto livre sem guarda, publicados e ativos (3 inscritos) — quase todo lead cai fora da janela de 24h do WhatsApp Business API, e sem a guarda a Meta recusa o envio em silêncio. Os quatro textos (`PA-CONF`/`PA-R24`/`PA-R3H`/`PA-R30`) também não tinham código nem versão até esta rodada; escritos em `biblioteca-mensagens.md` |
| **`Pós-ligação`, ramo `Pediu retorno`, nós 4 e 4b — dá para fazer HOJE** | No nó 4, apontar o vencimento da tarefa `[RETORNO] Ligar de volta` para o campo `Data de retorno` (e não para hoje+1 fixo). Depois, inserir o nó 4b: no **corpo** da tarefa, `Horário combinado: {{contact.hora_do_retorno}}`. **Enquanto estiver com a tela aberta, confira uma coisa e anote:** o seletor de vencimento do `Add Task` oferece hora vinda de campo personalizado `TEXT`? Se oferecer, use `Hora do retorno` ali e o nó 4b fica opcional | L-01 deixou de ser falta de campo em 21/09 23:18, quando `Hora do retorno` (`TEXT`, `HH:MM`) foi criado na tela — o par `DATE`+`TEXT` de S-01 está completo (`CONFERENCIA-CAMPOS.md`, Tabela K). O que sobrou é fiação: hoje a tarefa vence sempre em hoje+1 e o horário combinado com o lead não chega a quem vai ligar. O corpo da tarefa funciona com certeza; hora dinâmica no vencimento é a única parte não verificada, e é por isso que a conferência vai junto |
| **`Negociação Estagnada` — workflow novo, dá para fazer quando alguém abrir a tela** | Montar o workflow inteiro (`build-wesales.md`, seção 2.28; F-13, `ROADMAP-SALES-ENGAGEMENT.md`) e a Smart List `Saúde — Negociação Estagnada` (seção 8.28) | Fecha a única transição do funil (`NOVO LEAD` → `FORMALIZAR`) que ficou sem monitor: reunião qualificada pelo closer (`Sim`) sem virar `won` nem `lost` em 3 dias. Depende da tag `negociacao-estagnada` (T-21) existir na tela — mesma fila das outras cinco tags do F-05, ainda `[ ]` em `APROVADO.md` |
| **`Mestre de saída`, nó 4 — dá para fazer HOJE, mas depende do workflow novo existir para valer algo** | Somar `negociacao-estagnada` à lista de `Remove Contact Tag` do nó 4 (F-13, seção 2.28) | Achado em 22/09 ao desenhar o F-13: mesmo raciocínio das linhas `fila-travada`/`conectar-estagnado`/`retorno-vencido` — este alerta também se resolve numa saída de cadência de verdade (fechar `won`, sair por `lost`/`abandoned`, ou o veredito ser corrigido), que o nó 4 já alcança pela via normal. Não precisa do tratamento incondicional do nó 0 que `novo-lead-estagnado`/`agendar-estagnado` exigem — `NEGOCIAR` não está na lista de no-op do nó 1 |
| **`Interceptação de Sinal — Clique v2` e `— Resposta v2` (publicados, 15/18 nós), novo nó 5b — dá para fazer HOJE** | Depois do nó 5 (`Update Contact Field: Sinal recebido`), inserir `Update Contact Field: Data e hora do sinal = {{right_now}}` (`build-wesales.md`, seção 2.9.2) | Restaurado em 22/09/2026: o campo tinha sido descartado em 19/09 por um limite do **seletor da tela** (não parecia oferecer data/hora atual em campo `TEXT`) — mas a montagem destes dois workflows já saiu pela API interna, que grava o valor direto, e `Entrada em` (mesmo tipo `TEXT`) prova que `{{right_now}}` funciona nesse caminho. Sem este nó, a lista `Resposta por Template` (8.13, R-04) sempre mostra a coluna `Data e hora do sinal` vazia, e uma futura auditoria do F-05 perde o único carimbo de "quando o sinal chegou" que não depende da hora nativa de uma tarefa |
| **`Resgate por E-mail — Sem Telefone` — workflow novo, dá para fazer quando alguém abrir a tela** | Montar o workflow inteiro (`build-wesales.md`, seção 2.30; `IMPLEMENTACAO-WORKFLOWS.md`, W23; F-15, `ROADMAP-SALES-ENGAGEMENT.md`), primeiro workflow deste projeto a usar o canal e-mail | Fecha o ciclo em que um lead sem telefone (9 de 50 contatos, `ESTADO-E-PLANO.md`) recicla de 90 em 90 dias pelo Reengajamento (R-08) sem nunca receber tentativa nenhuma — a operação é 100% telefone e nenhuma régua usa e-mail. Depende dos dois templates `EM-1`/`EM-2` existirem (via `emails_create-template`, `[ ]` em `APROVADO.md`) e de confirmar na tela que a subconta tem domínio de e-mail verificado para envio transacional |
| **`Opt-out por Palavra-chave — E-mail` — workflow novo, dá para fazer junto do `Resgate por E-mail` acima** | Montar o workflow inteiro (`build-wesales.md`, seção 2.9.6; `IMPLEMENTACAO-WORKFLOWS.md`, W24; G-07, `ROADMAP-SALES-ENGAGEMENT.md`) | O `Resgate por E-mail` (W23, linha acima) só sabe notificar o gestor quando o lead responde — não distingue "tenho interesse" de "pare de me mandar e-mail". Mesmo defeito que o R-17 já corrigiu para WhatsApp, achado no canal mais novo do projeto. Não depende de campo ou tag novos |
| **Smart Lists `Auditoria — tag sem DND nativo` e `Auditoria — DND sem tag` (R-14, se já montadas) — acrescentar cláusula, dá para fazer HOJE** | Somar `OU Email DND = Disabled` (8.26) / `OU Email DND = Enabled` (8.27) ao filtro existente (`build-wesales.md`, seções 8.26/8.27; G-07) | As duas listas foram montadas cobrindo só `Calls`/`WhatsApp` — o e-mail nasceu como canal depois (F-15, mesmo dia). Sem a cláusula nova, um lead com `Email DND` desligado (ou ligado sem a tag) não aparece em nenhuma das duas |
| **`Interceptação de Sinal — Resposta` (publicado, tabela abaixo) e `Opt-out por Palavra-chave` (W14, publicado, 14 nós) — gatilho, dá para fazer HOJE, prioridade alta** | No filtro `Reply Channel`/Canal do gatilho `Customer Replied` dos dois workflows, acrescentar **SMS** ao lado de **WhatsApp** (aditivo, não trocar) — `build-wesales.md`, seções 2.9.3/2.9.5; G-09, `ROADMAP-SALES-ENGAGEMENT.md` | O único WhatsApp desta subconta (Stevo, QR, conectado 22/09/2026) entrega mensagem como `TYPE_CUSTOM_SMS`, confirmado por API na conversa de um contato de teste — se o filtro "WhatsApp" da tela reconhece só o canal nativo, os dois workflows **já publicados** nunca disparam para uma resposta pela Stevo, e um opt-out por esse número não aciona DND sozinho. **Ao abrir a tela, confira e anote:** qual rótulo de canal aparece para uma resposta já recebida pela Stevo — decide se o aditivo vira definitivo ou se dá para trocar por um filtro mais preciso |

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

## Estado da montagem em 21/09/2026 (lido por API — o que os workflows publicados já fizeram de verdade)

Leitura completa da subconta por `contacts_get-contacts` (50 contatos),
`opportunities_search-opportunity` (50 oportunidades),
`conversations_search-conversation` (50 conversas), `contacts_get-all-tasks`
nos três leads em `NEGOCIAR` e `calendars_get-calendar-events` pelo usuário
dono deles. O conector não lista workflows, então isto é o **rastro** que
cada workflow deixou nos dados — a única auditoria de "está funcionando?"
possível sem a tela.

| Workflow (tela em 19/09) | Rastro nos dados em 21/09 | Leitura |
|---|---|---|
| Porta de Entrada (publicado) | 50 oportunidades para 50 contatos, 10 delas criadas depois do backfill (19/09 22:50 → 21/09 09:17), todas em `NOVO LEAD` | **Funciona.** ~5 leads/dia entrando sozinhos |
| Pós-agendamento (publicado, 3 ativos) | `Daniel`, `Genilson \| Bombeiro`, `Teste Atendeu`: em `NEGOCIAR`, `Prioridade` = 5, `Data agendado` gravada, BANT/Fit preenchidos (nós 2 e 5 rodaram) — mas **`Nota de qualificação` vazia nos três** | **Funciona pela metade:** o nó 4 (Math Operations em série, seção 9.1) não grava. Ou não foi montado, ou grava em campo errado. Conferir no Registro de execução antes de publicar o Loop do closer, que lê essa nota nos nós 5/6 |
| Pós-ligação (publicado) | `Teste Atendeu`: `Total de ligações` 24, `Tentativas telefone` 24, `Conexões telefone` 8, `Data conectado` gravada — **`Total de conexões` vazio**. Um lead real (`carolfigueiredo`) com `Total de ligações` = 1 | **Funciona**, com um nó faltando: o "Math: `Total de conexões` + 1" do ramo `Atendeu` (seção 4, nó 2) nunca escreveu, mesmo com `Conexões telefone` chegando a 8. Provável nó ausente/desligado na cópia telefone |
| Mestre de saída (publicado) | Os **10 leads criados depois de 19/09 ~23h nasceram com a tag `limpar-tarefas`**; os 40 do backfill não têm (só quem passou por teste) | **Efeito colateral real:** algo aplica `limpar-tarefas` na chegada em `NOVO LEAD`. Hipótese mais provável: o portão do nó 1 ("é `CONECTAR` e `open` → encerra; senão segue") lê a *criação* da oportunidade em `NOVO LEAD` como saída e roda a limpeza inteira (nó 5 = `limpar-tarefas`). Inofensivo hoje (não há tarefa `[CADENCIA]` para a rotina apagar), mas polui a tag para quando houver. Confirmar no Registro de execução; correção provável: nó 0/1 encerrar também quando etapa é `NOVO LEAD` |
| Interceptação de Sinal — Clique/Resposta (publicados) | Nenhum contato com `fila-quente` ou `Sinal recebido` fora do contato de estrutura | Sem disparo real ainda (esperado: nenhuma mensagem com link saiu) |
| Cadência 12x30, Qualificação por IA, Recuperação de No-show (rascunho) | Nenhuma tag `fila-tel`/`fila-wa`/`toque`, nenhuma tarefa `[CADENCIA]`, `Tentativa nº` vazio em todo lead real | Confirmado: **nada de cadência rodou para nenhum lead** |
| Mensagens | 50 conversas; **zero WhatsApp ou SMS enviado pela operação**. As únicas mensagens reais são 5 DMs de Instagram (leads sem telefone: `dkw.oficial`, `nathalia.ggss`, `thiagoreis`, `Carla X. Sampaio`, `TINTIM`) | R-14 (compliance) segue sem o que auditar — a régua ainda não mandou mensagem a ninguém |
| Calendário `Reunião com closer` | `calendars_get-calendar-events` pelo `userId` dono das 3 oportunidades: **vazio** (15/09 a 15/10) — mas `Data agendado` foi gravada nos três pelo gatilho `Appointment Status` | Não conclusivo: a busca por usuário pode não enxergar evento de calendário sem responsável, e o conector não lista calendários para buscar por `calendarId`. Conferir na tela se os 3 agendamentos existem |
| Tarefas | `contacts_get-all-tasks` vazio em `Teste Atendeu`, `Daniel` e `Genilson` | Coerente: Pós-agendamento não cria tarefa, e a tarefa `[CONECTADO]` do teste de 19/09 foi registrada como "skipped" (contato sem dono na hora) |

**Dois achados de dado que não são de workflow (detalhe em
`CONFERENCIA-CAMPOS.md`, Tabela H):** o formulário do Meta grava em
`Urgência`/`Necessidade` (39/34 contatos), não em `Prazo`/`Dor principal`
que a régua lê; e grava em `Investimento mensal em anúncios` quatro textos
dos quais só um é opção do campo — a nota de qualificação de todo lead do
Meta nasce com o Bloco B zerado, independente de o nó 4 do Pós-agendamento
ser consertado.

**Estado bruto para a próxima leitura comparar — 19/09/2026 (linha de base
original):** 46 campos · 5 etapas · 50 contatos (38 com telefone; 12 sem: 5
DMs de Instagram, 5 fictícios, o de estrutura e 1 `<test lead>` do Meta) · 50
oportunidades (47 `NOVO LEAD` + 3 `NEGOCIAR`, todas `open`, 47 sem
responsável, 3 com `JdvhvOTEBTvUyRi0BXU8`) · 1 contato com DND (`Teste Não
Ligar`) · fuso da subconta `America/Sao_Paulo`, plano `trialing`.

**Relido em 22/09/2026 12:50 UTC — o que mudou desde aquela linha de base:**

| O quê | 19/09 | 22/09 12:50 |
|---|---|---|
| Campos personalizados | 46 | **51** (os 5 criados em 21/09 23:15–23:33, `CONFERENCIA-CAMPOS.md` Tabela K) |
| Contatos / oportunidades | 50 / 50 | **50 / 50** (sem lead novo desde 21/09 09:17 — F-10) |
| Oportunidades por etapa | 47 `NOVO LEAD` + 3 `NEGOCIAR`, todas `open` | 47 `NOVO LEAD` + 3 `NEGOCIAR`; **3 `lost`** (2 em `CONECTAR`, 1 em `NEGOCIAR`), 47 `open` |
| `CONECTAR` já recebeu oportunidade? | nunca | **sim** — duas de teste passaram por ali em 22/09 12:00–12:08 |
| Contatos com DND | 1 | **3** (`Teste Atendeu`, `Teste Número Errado`, `Teste Retorno`) — todos nos **6 canais**, por workflow (`message: Updated from workflow_cf6fa19d-…`) |
| Tags na subconta | 15 do projeto | **16** — a nova é `teste-regua`, criada pelo dono na tela, fora de todo documento (`campos-e-tags.md`) |
| `lostReasonId` nas `lost` | — | **`null` nas três** — linha de base do F-12 é 0% preenchido |

**O dono estava executando o checklist da seção 10 durante esta leitura** —
escritas às 11:59, 12:05, 12:06, 12:08 e 12:38. Detalhe contato por contato em
`APRENDIZADOS-CRM.md` ("O dono está executando o checklist na tela agora").
Estado de tela muda sem aviso: se a próxima leitura divergir desta tabela, a
causa mais provável é o checklist continuando, não defeito.

## Como montar mais rápido sem clicar tudo de novo (pesquisado em 21/09/2026)

Não existe endpoint público para criar workflow e este ambiente não alcança
nem a tela nem a API interna da HighLevel. O que a comunidade usa, em ordem
de preferência para nós (detalhe e fontes em `APRENDIZADOS-CRM.md`, entrada
"Como a comunidade cria workflow sem clicar"):

1. **Montar um modelo na tela e clonar por JSON** com a extensão Chrome
   "GHL Workflows JSON Exporter" (ou "GHL Workflow Backup & Audit", que
   declara suporte a white-label). Exporta o workflow aberto, edita texto,
   espera e tag no JSON, importa as cópias. Alvo ideal: os 12 toques da
   Cadência 12x30 e os workflows de estagnação do Monitor de Saúde (F-05/F-13).
   Guardar cada JSON exportado em `wesales/workflows-json/`.
2. **Snapshot da subconta** quando a montagem fechar: backup e replicação.
3. **API interna** (`backend.leadconnectorhq.com`, projetos
   `gojc31/gohighlevel-cli` e `drleadflow/ghl-automation-builder`): 100%
   programático, mas não documentado e com risco de termos de uso. Só com
   decisão do dono, rodando na máquina dele, com
   `IMPLEMENTACAO-WORKFLOWS.md` como spec.

## Estado da montagem em 21/09/2026, noite (montado pela API interna, do PC do dono)

Primeira montagem programática do projeto. Caminho: Playwright abre
`app.wesalescrm.com` com o dono logado, o bearer do `backend.leadconnectorhq.com`
é capturado do tráfego da própria tela e renovado sozinho (headless, ~10 s);
os workflows saem por `POST/PUT /workflow/{loc}`. Formato de cada tipo de nó
foi **lido de workflows reais desta subconta**, não de schema de terceiro.
Ferramentas em `wesales/tools/`, JSON e PNG de cada workflow em
`wesales/workflows-json/`. Todo workflow nasce `draft`; publicação é do dono.

| Workflow | Estado | Conferência |
|---|---|---|
| `ZZ TESTE API` | rascunho, 1 nó (descartável) | prova de vida: gatilho `Contact Tag Added` (`teste-api`) → `Add Note`. Lido de volta pela API e conferido no canvas |
| `Contador de Toques` (W1) | rascunho, 4 nós | bate nó a nó com a W1: `Remove Tag toque` → Math `Toques na semana +1` → `Wait 7 Days` → Math `-1`. Re-entry ligado, Stop on Response desligado, sem janela |

| `CONECTAR Estagnado` (W17c) | rascunho, 20 nós | os dois laços de volta ao Wait de 14 dias fechados por `goto`; a tela confirma `If "Checkpoint — Tentativa nº" não é igual a "{{contact.tentativa_n}}"` e `If "Tags" não inclui "conectar-estagnado"` |
| `Alerta de Speed-to-lead` (W15) | rascunho, 12 nós | os Waits de 15 min e 1 h convergem no mesmo portão por `goto` |
| `AGENDAR Estagnado` (W17d) | **publicado em seguida, despublicado em 23/09/2026 (G-13) — não republicar** | igual ao W17, etapa `AGENDAR`; a premissa ("atendeu e ficou em AGENDAR sem reunião") deixou de poder ocorrer quando o ramo `Atendeu` parou de mover para lá (D3). Substituto: `Fechar Horário` |
| `Lead Esquecido em NOVO LEAD` (W17) | rascunho, 7 nós | preencheu um rascunho vazio que já existia |
| `Registro de Comparecimento` (W7) | rascunho, 6 nós | gatilho `Appointment Status` = `showed` no calendário `Reunião com closer` (`3uNQFjCEDe7b4gKZJuOZ`) |

| `SLA do Closer — No-show` (W9) | **publicado**, 12 nós | preencheu rascunho vazio; notifica o closer, espera 2 h, cobra o gestor |
| `Opt-out por Palavra-chave` (W14) | **publicado**, 14 nós | OU das 17 frases num If/Else (o gatilho só combina com E); DND + saída de todas as réguas exceto a atual |

| `Cadência 12x30` (W11) | **publicado**, 430 nós | nó 0 + 12 toques completos; janela 08:30–18:30, re-entry desligado, Stop on Response ligado; 2 gatilhos (etapa→CONECTAR e tag `cad-outbound`) |
| `Cadência Inbound` (W12) | **publicado**, 172 nós | 5 toques rápidos; handoff para a 12x30 por tag |
| `Reengajamento 90 dias` (W16) | **publicado**, 113 nós | TR1–TR4; `reengajamento-ativo` entra antes de `cad-outbound` (sinergia) |
| `Recuperação de No-show` (W8) | **publicado**, 41 nós | NS1–NS3 + descarte automático no 2º no-show |
| `Interceptação de Sinal — Clique v2` | **rascunho**, 15 nós | aponta para o Trigger Link novo; o publicado aponta para um id morto |
| `Interceptação de Sinal — Resposta v2` | **rascunho**, 18 nós | portão de opt-out com 17 frases na frente do fluxo (retoque R-17) |

| `SLA do Closer — No-show` (W9) / `Opt-out` (W14) | **publicados** | 12 e 14 nós |
| `Pós-agendamento v2` | **rascunho**, 160 nós | a régua da 9.1 que nunca existiu: 28 somas, máximo 100 |
| `Mestre de saída v2` | **rascunho**, 10 nós | portão que encerra em `NOVO LEAD`, para não marcar `limpar-tarefas` em lead que chega |

**Testado de ponta a ponta, com rastro lido pela API:** `Contador de Toques`
(tag removida, campo = 1), `Loop do closer v2` (nos dois ramos: `Parcial` →
`abandoned`, `Não` → `lost`, etapa intacta) e a **`Cadência 12x30` completa**
— lead movido para `CONECTAR` resultou em dono atribuído, `Prioridade` 3,
`Entrada em`, contadores zerados, tag `fila-tel`, `Tentativa nº` = 1 (parou
no T1, sem correr) e a tarefa `[CADENCIA] T1 · Ligar (telefone)` criada para
o dono, vencendo hoje.

**Pré-requisitos resolvidos nesta sessão:** os 5 campos da tabela 1.2
(`Toques na semana` `c1xuCuLyJheHOQoJ3grH`, `Hora da conexão`
`5hU72B0HuoMApZvO1Qk7`, `Hora do retorno` `IHXNFnguTPyNj5Q59ea2`,
`Checkpoint — Tentativa nº` `BRcN6IGXtDr0u52QtfiF`, `Checkpoint — Data de
retorno` `el7xNMvPE8ZiyfysRff9`), todos em `Contato` / pasta `Additional
Info`. Mapa completo nome→id→chave em `wesales/tools/campos.json`.


## Estado final em 22/09/2026 — o que está no ar

**20 workflows publicados.** 15 montados nesta sessão pela API interna e 5
cópias corrigidas que substituíram os originais defeituosos (os originais
ficaram em rascunho, sem nenhum nó alterado — reversível com um clique).

| No ar | Nós | |  No ar | Nós |
|---|---|---|---|---|
| `Cadência 12x30` | 410 | | `Opt-out por Palavra-chave` | 14 |
| `Cadência Inbound` | 172 | | `Alerta de Speed-to-lead` | 12 |
| `Pós-agendamento v2` | 180 | | `SLA do Closer — No-show` | 12 |
| `Pós-ligação v2` | 142 | | `Retorno Vencido` | 11 |
| `Reengajamento 90 dias` | 105 | | `Mestre de saída v2` | 10 |
| `Recuperação de No-show` | 40 | | `Fila Travada` | 8 |
| `Loop do closer v2` | 31 | | `Lead Esquecido` / ~~`AGENDAR Estagnado`~~ (despublicado 23/09, G-13) | 7 + 7 |
| `CONECTAR Estagnado` | 20 | | `Registro de Comparecimento` | 6 |
| `Interceptação — Resposta v2` | 18* | | `Contador de Toques` | 4 |
| `Interceptação — Clique v2` | 15* | | `Porta de Entrada` | 1 |

*Contagem de 22/09/2026, antes do retoque do nó 5b (`Data e hora do sinal`,
tabela de retoques acima) — a tela ainda tem 15/18, sobe para 16/19 quando
alguém aplicar o retoque.

**Provado rodando, com rastro lido pela API:** `Contador de Toques`,
`Loop do closer v2` (nos dois ramos), a `Cadência 12x30` inteira (nó 0 →
tarefa `[CADENCIA] T1` criada para o dono) e a régua de qualificação
(93 por `Prazo`, 15 pelo bloco de reserva `Urgência`).

**Fora do ar de propósito:** `Qualificação por IA no WhatsApp` (vazio,
precisa de Conversation AI), `Post-Meeting Closer Loop` (substituído pelo
`Loop do closer v2`) e os 5 originais trocados.

**Não montados, e por quê:** W10 (Conversation AI), W18 (gatilho Scheduler
sem formato conhecido neste build) e W19 (Number Validation desligado — ~~e
ver a ressalva de `country=US` abaixo~~; **a ressalva de `country` caiu em
22/09, item 2 abaixo: a subconta é `BR`**. O que sustenta "não montado"
continua sendo só o gatilho desligado / sem exemplo capturado).

### Decisões que continuam com o dono

1. ~~**WhatsApp desconectado.** Os nós de envio exigem `template_id` e
   `from_phone_number`; sem o canal não passam nem como rascunho. Faltam
   M1/M2/M3, MI-0/MI-F, RE-1/RE-2 e NS-1/NS-2 — o resto de cada régua está
   montado e funcionando.~~
   **Deixou de valer 39 minutos depois de ser escrito.** Este item é de
   `329c9b1` (10:09); em `d52e61d` (10:48) o dono decidiu que as réguas são
   **100% telefone**. Numa operação só de ligação esses nós não existem, então
   não "faltam": as quatro réguas estão **inteiras**. A decisão está registrada
   na seção 2.5 do `build-wesales.md`. Mantido riscado porque a diferença entre
   "falta montar" e "não existe" é o que decide se alguém vai tentar montar.
2. ~~**`country` da subconta está `US`** com fuso `America/Sao_Paulo`, moeda
   `BRL` e telefone `+55`. Afeta o W19: Number Validation checaria número
   brasileiro contra regra americana. Não mexi porque `country` toca
   telefonia e faturamento (`saasSettings`, `twilioRebilling` ativos).~~
   **Medido e refutado em 22/09/2026, 16:25 UTC** (`locations_get-location`,
   e a rodada das 16:13 mediu o mesmo independentemente): a subconta está
   **`country: "BR"`**, `locale: "pt_BR"`, São José dos Campos / São Paulo,
   CEP 12216-200, `currency: "BRL"`, fuso `America/Sao_Paulo`. Nada a
   arrumar, e **nada aqui bloqueia o W19**.

   O `US` existe, mas em outro objeto: é o **`country` dos contatos** que
   entram pelo formulário do Meta — `country: "US"` e `timezone: null`,
   documentado na Tabela L do `CONFERENCIA-CAMPOS.md` e reconfirmado hoje em
   `Carlos Andrade` (`7ECnj1bSeEIm5P58Ifd9`). Subconta e contato são campos
   diferentes com o mesmo nome, e a diferença muda o conserto: **não se
   mexe em `saasSettings`, mexe-se no mapeamento do formulário** (terreno do
   G-04). E para o W19 a preocupação até aumenta, em vez de desaparecer —
   `Number Validation` valida o telefone **do contato**, e é o contato que
   está marcado como americano com número `+55`.
3. **Linha "Mensagens" do `APROVADO.md`** continua `[ ]`: falta o número
   completo para os testes de envio.
4. **Push bloqueado:** a credencial git desta máquina é de outra conta.

## Conferência da nuvem em 22/09/2026, 16:10 UTC

Li o merge `3cc1c4b` (os 27 commits do PC) e conferi contra a API. Três coisas
para a próxima pessoa que abrir este repositório.

### 1. Os 22 arquivos de `workflows-json/` não dizem o que está no ar

> **Atualizado em 23/09/2026:** depois do refresh ao vivo (`482de1f`) os dumps
> passaram a mostrar `status: published` em 24 de 26 — então o `draft` era
> mesmo artefato de fotografia, e hoje o arquivo **responde** "está no ar?".
> O que **não** mudou: `triggers: []` em todos os 26, mesmo refeitos. O gatilho
> não entra nesta exportação. Detalhe na seção 6 do `ESTADO-E-PLANO.md`.

Todos os 22 dumps trazem `status: draft` e `triggers: []` — **os 22, sem
exceção**. Isso não significa que nada está publicado: significa que o dump é
a fotografia do payload **antes** de publicar, e que o gatilho é gravado por
outra chamada e nunca entrou no arquivo. A prova de que os workflows estão no
ar é a tabela dos 20 logo acima, com rastro lido pela API.

A regra que fica: **`workflows-json/` serve para conferir nó, tag e campo —
nunca para responder "isto está ligado?" nem "em que gatilho?".** Quem quiser
responder isso hoje precisa da tela: a API pública (MCP) não tem endpoint de
workflow, então a sessão da nuvem não consegue verificar publicação nem
gatilho de jeito nenhum. É o maior ponto cego do projeto neste momento.

### 2. O lead mais novo da base nunca foi tocado

`Carlos Andrade` (`7ECnj1bSeEIm5P58Ifd9`), lead pago do Facebook, campanha
`LEADS I FORM I FS1`:

| | |
|---|---|
| Entrou | 21/09 09:17:23 |
| Oportunidade criada | 21/09 09:17:26 (3 s — a Porta de Entrada funciona) |
| Última alteração no contato | 21/09 09:17:30 (7 s depois de entrar) |
| Etapa agora | `NOVO LEAD`, `status: open`, `lastStageChangeAt` 21/09 09:17:26 |
| Tags agora | só `limpar-tarefas` — a tag de **saída limpa** |
| Campos de cadência | vazios (só as 3 respostas do formulário) |

Ele entrou, foi ejetado em 7 segundos pelo portão da régua que estava no ar
naquela manhã, e **está parado há 30h49min sem um único toque**. Não atribuo
isso ao que o dono publicou ontem à noite: a ejeção é de 09:17, e o primeiro
commit do PC é de 19:50. O que estava no ar na manhã de 21/09 eu não consigo
ler pela API, então **não sei qual portão o ejetou** — só que foi ejetado.

O que importa para a operação é o que vem depois: workflow publicado age em
quem **entra**, não em quem já está parado. Carlos não vai ser re-enrolado
sozinho. E o monitor que existe exatamente para isso — `Lead Esquecido em
NOVO LEAD` — só o alcança se o gatilho dele pegar lead já parado na etapa; se
for gatilho de mudança de etapa, Carlos é invisível para ele. **Isso é uma
pergunta para a tela**, pelo ponto cego do item 1.

### 3. Seis tags estão no ar com a linha ainda `[ ]` no `APROVADO.md`

`novo-lead-estagnado`, `fila-travada`, `conectar-estagnado`,
`agendar-estagnado`, `retorno-vencido` e `negociacao-estagnada` aparecem nos
workflows publicados, e as seis linhas continuam `[ ]`. **Não marquei
nenhuma** — `[x]` quer dizer "o dono aprovou", e quem aprova é o dono, não
quem mede. Registro aqui só para o `APROVADO.md` não virar ficção: se elas já
estão no ar por decisão de quem manda, o certo é ele marcar as seis; se alguma
entrou sem querer, este é o aviso.

## Conferência da nuvem em 22/09/2026, ~23h UTC — retoque pendente no `Reengajamento 90 dias`

Achado ao fechar o G-08 (`ROADMAP-SALES-ENGAGEMENT.md`): o nó 2 (portão) do
workflow `Reengajamento 90 dias` — **já publicado**, tabela "Estado final em
22/09/2026" acima, 105 nós — reativa hoje qualquer oportunidade
`abandoned`+`nutricao-90d` sem checar se o lead tem telefone válido. Um lead
que nunca teve telefone (a maioria vem de DM do Instagram) voltaria para
`CONECTAR` a cada 90 dias, sem nenhum canal capaz de alcançá-lo, para
sempre. Corrigido na especificação (`build-wesales.md`, seção 2.12;
`IMPLEMENTACAO-WORKFLOWS.md`, W16): o nó 2 ganha a condição **E** `Tags` não
inclui `telefone-invalido`.

**Retoque pendente na tela, mesma classe do nó 5b já registrado acima:**
adicionar essa quarta condição ao `If/Else` do nó 2, na mesma configuração
do workflow já no ar — patch cirúrgico de uma condição, mesmo padrão que o
`tools/patch_relogio_cadencias.py` já usou para o relógio no mesmo dia
(`APRENDIZADOS-CRM.md`). Não é urgente hoje: a base tem **zero** oportunidade
`abandoned` no momento desta conferência (53 oportunidades, todas
`NOVO LEAD`/`CONECTAR`/`NEGOCIAR`) — o ciclo só dispara quando G-03 for
decidido e um lead sem telefone esgotar a cadência a partir de `CONECTAR`.
Aproveitar quando alguém for aplicar o próximo patch cirúrgico neste
workflow, ou quando o primeiro lead real chegar perto de esgotar as 4
tentativas do reengajamento, o que vier primeiro.

**Junto, mesmo nó vizinho, achado de coerência:** o nó 3 (reset de rodada)
ainda documentava `Entrada em` = `{{right_now}}` nos dois arquivos de
especificação, mas a tela já usa `{{right_now.date}} {{right_now.time}}`
desde o mesmo patch cirúrgico do relógio — a doc estava um passo atrás do
que já está publicado. Corrigida nos dois arquivos junto com o retoque
acima; não muda nada na tela, só põe a spec de volta batendo com a
realidade.

