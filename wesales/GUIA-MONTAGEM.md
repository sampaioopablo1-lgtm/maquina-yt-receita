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
- [x] **Fase 2 — Campos personalizados** (42 campos) — concluída; os 2 que faltavam (`WA não atendidas seguidas`, `Permissão WhatsApp`) foram criados e o tipo errado (`Conexões telefone`) foi corrigido para Numérico, confirmado via `locations_get-custom-fields`
- [ ] **Fase 3 — Calendário do closer + formulário de qualificação** — próxima
- [ ] **Fase 4 — Trigger Link "Agendar com o closer"**
- [ ] **Fase 5 — Os ~14 workflows**, na ordem da seção "Ordem de montagem" do `build-wesales.md`
- [ ] **Fase 6 — Listas inteligentes** (~18)
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
- [ ] **Seção 2 e subseções 2.1–2.17 (Cadência 12x30 e vizinhas)** —
      maior bloco: todo gatilho `Opportunity Stage Changed` e toda saída
      "mover para `Nutrição`/`Descartado`" (mais concentrado nas seções
      2.4, 2.10, 2.12) precisa virar filtro em `CONECTAR` + `Update
      Opportunity` (status), pela tabela 1.0
- [ ] **Seção 3 (Mestre de saída)**
- [ ] **Seção 4 (Pós-ligação)** — o ramo que hoje diz "mover para
      `Nutrição`" nas 12 tentativas esgotadas é o mais citado por outras
      seções (R-01, R-02, F-01), migrar com atenção a quem aponta para ele
- [ ] **Seção 5 e 5.1–5.4 (Pós-agendamento, Loop do closer, Comparecimento,
      No-show)** — inclui o achado já registrado na seção 1.2 desta
      migração: "descartar oportunidade" no no-show 2x (R-12) precisa virar
      `status = lost` dentro de `NEGOCIAR`, não mover para uma etapa
      `Descartado` que não existe mais
- [ ] **Seção 6 (Qualificação por IA no WhatsApp)**
- [ ] **Seção 8 (Listas inteligentes)** — qualquer lista com filtro de
      etapa `Retorno agendado`/`Nutrição`/`Descartado` precisa trocar para
      filtro de campo/status
- [ ] **Seção 9 (Nota de qualificação e Prioridade)**

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
"P" maiúsculo; `build-wesales.md` escreve `Caixa postal` (minúsculo) em
todas as menções. Não é um bug funcional: quem montar o workflow vai
selecionar a opção que existe de verdade no dropdown da tela, não digitar
o texto do documento — registrado só para quem for revisar o texto não
estranhar a diferença de caixa.

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
- [x] 42 campos no total confirmados (`locations_get-custom-fields`,
      `query_model=contact`) — todos os C-01 a C-24, Q-01 a Q-18 mais
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
