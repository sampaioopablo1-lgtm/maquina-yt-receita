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

- [ ] **Fase 1 — Pipeline "Pré-vendas"** (editar as 14 etapas do `FUNIL DE VENDAS` para as 7 novas) — abaixo, pronta para seguir agora
- [ ] **Fase 2 — Campos personalizados** (~24 campos) — em andamento fora de ordem, ver verificação abaixo: faltam 2, 1 com tipo errado
- [ ] **Fase 3 — Calendário do closer + formulário de qualificação**
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

### Verificação em 18/09/2026, ~20h UTC — não risque o checkbox ainda

Rotina horária releu o pipeline (`opportunities_get-pipelines`) depois de
commitar este guia às 19:52 UTC. O `FUNIL DE VENDAS` **mudou** —
`dateUpdated` marca 19:56 UTC, 4 minutos depois — mas não para as 7
etapas da tabela acima. O que está na tela agora:

| Posição | Etapa encontrada | Prob. encontrada | Cor encontrada |
|---|---|---|---|
| 0 | `NOVO LEAD` | 30% | `#2563EB` (igual ao azul pedido p/ `Novo lead`) |
| 1 | `CONECTAR` | 40% | `#8B5CF6` |
| 2 | `AGENDAR` | 50% | `#2DD4BF` |
| 3 | `NEGOCIAR` | 60% | `#D97706` |
| 4 | `FORMALIZAR` | 70% | `#059669` |

Só 5 etapas, não 7, e a partir da posição 1 nenhum nome bate com a tabela
deste guia (`Em cadência`, `Conectado`, `Retorno agendado`, `Reunião
agendada`, `Nutrição`, `Descartado` — as duas últimas nem existem na
tela). As probabilidades também não batem (30/40/50/60/70, progressão
redonda de 10 em 10 — o mesmo cheiro de template automático que a
`auditoria-resultado.md` já flagrou nas 14 etapas antigas, que também
vieram de `originId` de snapshot). **Não é o bug de progressão original
voltando**: é uma configuração nova, diferente da antiga e diferente da
pedida aqui.

**Confirmado por `opportunities_search-opportunity` (status `all`) na
mesma checagem: 0 oportunidades no pipeline.** Nenhum dado de negócio foi
perdido nessa troca, venha ela de onde vier.

**Duas hipóteses, nenhuma confirmada — registrar qual é a certa quando
souber, não escolher uma sem confirmação:**
1. Início manual desta fase, com nomes/cores próprios em vez de copiar a
   tabela — a posição 0 bate exatamente em nome (`Novo lead` → `NOVO
   LEAD`) e em cor (`#2563EB`), o que é compatível com alguém tendo
   começado a seguir o guia e depois preenchido o resto no estilo dele.
2. Reaplicação de um snapshot/template da agência por fora deste projeto
   (a mesma origem que criou as 14 etapas antigas) — compatível com a
   progressão redonda de 10 em 10 e com o pipeline ter menos de um dia de
   vida.

**Por isso este item continua com o checkbox vazio, e a Fase 2 não deve
começar assumindo que os nomes da Fase 1 já existem na tela** — todo
gatilho `Opportunity Stage Changed` do `build-wesales.md` procura pelo
nome exato `Em cadência`/`Reunião agendada`/etc., e nenhum desses existe
hoje no pipeline. Antes de seguir: confirme com quem mexeu no pipeline se
foi isto (hipótese 1, e falta terminar as 2 etapas que sobraram e
corrigir os 4 nomes) ou se é outra coisa (hipótese 2, e a Fase 1 recomeça
do zero). A rotina horária reconfere a cada execução futura e atualiza
esta seção assim que o estado mudar de novo.

**Reconferido nesta execução (18/09/2026, ~21h UTC): sem mudança.**
`opportunities_get-pipelines` devolve o mesmo `dateUpdated` de 19:56 UTC e
as mesmas 5 etapas da tabela acima — ninguém mexeu no pipeline desde a
última rodada. As duas hipóteses seguem em aberto.

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

### Como saber que terminou certo

- [ ] C-03 e C-04 criados
- [ ] C-11 recriado como `NUMERICAL` (confirmar antes se apagar é
      necessário ou se a tela oferece outro caminho)
- [ ] `locations_get-custom-fields` relido confirma cada uma das 24
      linhas de `campos-e-tags.md` mais Q-02/Q-03, nome e tipo batendo
      um a um — não só a contagem total

Só depois disso marque `[x]` na Fase 2 na visão geral acima.
