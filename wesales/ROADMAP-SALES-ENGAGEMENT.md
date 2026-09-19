# O que falta para virar Reev/Meetime de verdade

O alvo do projeto não é "ter uma cadência no GHL". Os blocos 1 a 5 são a
distância até a **paridade** com Reev e Meetime — e paridade é o **piso**, não
a chegada. O bloco 6 é o que faz a operação ficar fora da curva: coisas que a
maioria das operações de SDR não faz, e que nem as plataformas de prateleira
entregam bem.

**É o backlog que a rotina horária trabalha.** Um item por execução, de cima
para baixo, respeitando o `APROVADO.md`.

## O que já está desenhado

Cadência multicanal de 12 tentativas, filas por tag em listas inteligentes,
régua de qualificação com nota, roteamento por resultado, saída limpa, rotina
de higiene de tarefas. Isso é o **motor**.

O que falta abaixo é quase tudo **instrumentação e cadências vizinhas** — que
é justamente onde Reev e Meetime ganham de um CRM configurado na mão.

**Nota de 18/09/2026 sobre os "Resumo" abaixo:** vários itens fechados dizem
"campo personalizado não sai por API" como se fosse limitação da HighLevel.
Não é — é limitação só do conector `GHL CRM` conectado nesta sessão; a API
oficial permite criar campo e calendário por API (não permite pipeline,
workflow nem formulário, esses sim são limitação de plataforma). Detalhe,
fontes e o que fazer a respeito: `APRENDIZADOS-CRM.md`. As frases originais
abaixo ficam como estavam no dia em que cada item fechou — não foram
reescritas uma a uma para não inflar o diff sem necessidade.

---

## Bloco 0 — Pré-requisito (antes de tudo)

Descoberto em 19/09/2026, depois de todos os blocos 1 a 5 e a maior parte do
6 já estarem desenhados: um buraco na base que faz cada um deles, sozinho,
não valer nada até ser fechado. Fica antes do Bloco 1 porque é anterior em
sentido literal — nenhum gatilho `Opportunity Stage Changed` de nenhum
workflow já especificado tem o que disparar sem isto.

### G-01 · Porta de entrada — nada cria oportunidade (lacunas L-09/L-09b) — **FEITO em 19/09/2026**
**Por quê:** toda a máquina (cadência, interceptação de sinal, dashboard,
tudo) é construída em cima de etapa de oportunidade. `grep "Create
Opportunity"` no `build-wesales.md` inteiro dava zero até esta rodada —
nenhum nó cria o registro, só leem ou movem etapa. Não é hipótese: nesta
execução a subconta tinha **40 contatos** (a maioria leads reais do Meta
Lead Ads, `source: Facebook`, `attributions` confirmando `adSource:
facebook` — ad pago gerando lead de verdade) e **0 oportunidades**
(`opportunities_search-opportunity`, status `all`). Descoberto ao vivo
rodando a Interceptação de Sinal contra o contato `andre` (lacuna L-09,
`briefing-sdr.md`), e generalizado ao notar que o mesmo vale para toda
origem, não só Meta (L-09b).
**Como:** workflow "Porta de Entrada" — gatilho `Contact Created` (sem
filtro, cobre manual/formulário/API/integração), ação nativa
`Create/Update Opportunity` para `FUNIL DE VENDAS` → `NOVO LEAD`.
**Pronto quando:** todo contato novo, de qualquer origem, ganha oportunidade
em `NOVO LEAD` sozinho, sem depender de um toggle por integração.

**Resumo:** especificado nó a nó em `build-wesales.md`, seção 1.3 — um
único nó (`Create/Update Opportunity`, `Allow Duplicate Opportunities`
desligado, comportamento nativo de atualizar em vez de duplicar quando já
existe oportunidade do contato naquele pipeline). Pesquisado antes de
escolher o gatilho: `Contact Created` cobre toda origem, incluindo Meta
Lead Ads (confirmado em fontes da HighLevel e de terceiros, que usam esse
mesmo gatilho com filtro de `Lead Source Tag` para pegar a fatia do
Facebook) — rejeitado o gatilho específico `Facebook Lead Form Submitted`
por cobrir só uma origem, e `Tag Added` por depender de uma tag que
nenhum fluxo aplica na entrada. Dois limites documentados na seção 1.3:
importação em massa por CSV não dispara `Contact Created` (confirmado por
pesquisa — proteção da própria HighLevel contra automação em massa
acidental), e os **40 contatos já existentes não são pegos
retroativamente** — os dois resolvidos pelo mesmo contorno manual, a ação
em massa nativa `Add to Workflow` rodada uma vez depois de publicar.
Zero campo e zero tag novos — não depende de `APROVADO.md`. Cruza com
L-07 (`briefing-sdr.md`), que continua em aberto de propósito: este item
só cria a oportunidade em `NOVO LEAD`, a promoção para `CONECTAR` (que
liga a Cadência 12x30 de verdade) continua decisão manual do SDR. Falta
só a criação manual na tela — workflow não sai por API; `GUIA-MONTAGEM.md`
ganhou uma Fase 1.5 marcando este item como furando a fila de montagem, à
frente da Fase 3, porque cada hora sem ele é lead pago do Meta acumulando
sem nunca entrar em etapa nenhuma.

### G-02 · Migração de nomes de etapa em `build-wesales.md` ainda incompleta — **em andamento**
**Por quê:** quando o pipeline virou as 5 etapas reais (`NOVO LEAD`/
`CONECTAR`/`AGENDAR`/`NEGOCIAR`/`FORMALIZAR`, decisão ao vivo de
18/09/2026) em vez das 7 do plano original, boa parte do
`build-wesales.md` ficou com gatilho, portão ou nó citando etapa ou
pipeline que não existe mais na tela (`Em cadência`, `Nutrição`,
`Retorno agendado`, `Descartado`, `Pré-vendas`). Um gatilho ou `If/Else`
que compara contra etapa inexistente nunca casa — mesma classe de bug
silencioso que R-16 já achou para rótulo de opção, aqui em nome de
etapa/pipeline, e mais caro: não é nota errada, é o workflow inteiro
nunca disparando. Descoberto ao notar que `GUIA-MONTAGEM.md` já rastreava
essa migração seção por seção desde 18/09/2026, mas boa parte das caixas
seguia `[ ]`.
**Como:** seguir a tabela de tradução (`build-wesales.md`, seção 1.0)
seção por seção, trocando gatilho/portão/nó para etapa real ou status
nativo (`abandoned`/`lost`), sem mudar comportamento nenhum — é tradução,
não redesenho. `GUIA-MONTAGEM.md`, dentro da Fase 1, é quem rastreia o
checklist linha a linha; este item só existe para o trabalho não ficar
invisível a quem lê só o roadmap.
**Pronto quando:** todo `[ ]` do checklist de migração em
`GUIA-MONTAGEM.md` (Fase 1) vira `[x]` — o que equivale a
`grep -n "Em cadência\|Nutrição\|Descartado\|Pré-vendas" wesales/build-wesales.md`
só retornar linha da tabela de tradução (1.0) ou de trecho citando o plano
histórico de propósito (nunca um gatilho, portão ou nó ativo).

**Resumo (19/09/2026):** fechada a seção 2.12 (Reengajamento 90 dias) — o
maior pedaço que restava, sinalizado como tal no próprio
`GUIA-MONTAGEM.md`. Gatilho trocado de `Opportunity Stage Changed →
Nutrição` (que não existe mais) para `Contact Tag Added → nutricao-90d`,
como a tabela 1.0 já previa; portão do nó 2 trocado de "etapa é Nutrição"
para "status é abandoned"; nó de reentrada migrado para `CONECTAR`.
Achado durante a migração, não estava na tabela 1.0: o nó de reentrada
precisou ganhar um reset explícito de `status` para `open` junto com a
etapa — sem isso o lead reativado chegaria a `CONECTAR` ainda com
`status = abandoned` da rodada anterior, e o portão do Mestre de saída
(seção 3, "`CONECTAR` e `open`") leria a chegada como saída e disparia a
limpeza no momento errado (o oposto do "no-op" que o desenho original
pressupunha). Seção 2.2 também tinha uma menção solta a `"Em cadência"`,
corrigida junto por ser trivial. Zero campo, zero tag: item de
documentação pura, não depende de `APROVADO.md`.

**Resumo (19/09/2026, segunda rodada):** fechada a seção 2.10 (Cadência
Inbound) — tradução mecânica seguindo a mesma tabela 1.0, sem achado novo:
gatilho `Pré-vendas`/`Em cadência` → `FUNIL DE VENDAS`/`CONECTAR`, nó 0.0b
de "mover etapa" para `Update Opportunity status = abandoned/lost`
(espelhando o 0.0b da 2.3, já migrado), portão da tentativa para
`CONECTAR`.

**Resumo (19/09/2026, terceira rodada):** fechada a seção 2.11 (Alerta de
Speed-to-lead) — gatilho migrado (`Pré-vendas`/`Em cadência` → `FUNIL DE
VENDAS`/`CONECTAR`), e o portão (nó 2) ganhou um achado que a tradução
mecânica sozinha não pegava: checar só "etapa é `CONECTAR`" deixaria um
lead descartado por falta de telefone (nó 0.0b da seção 2.3, que muda
`status` para `abandoned`/`lost` sem tirar a oportunidade de `CONECTAR`)
disparar um alarme de speed-to-lead falso, porque a etapa continua batendo
e `1ª tentativa em` nunca vai ser preenchida para esse lead. Portão
corrigido para "`CONECTAR` **e** `status é open`" — a mesma condição
composta que a seção 3 (Mestre de saída) já usa, e o mesmo tipo de achado
que a reentrada da 2.12 já tinha documentado, agora numa terceira seção.
Zero campo, zero tag: item de documentação pura, não depende de
`APROVADO.md`.

**Conferência da mesma rodada (19/09/2026):** a regra que ela generalizou
valia para mais três portões, e só um tinha sido corrigido. Entraram
`status é open` no nó 3 da seção 2.4 e no nó 2 da seção 2.10, e — o achado
que pesa — os nós 2b/2c no Mestre de saída (seção 3), que removia o lead de
**uma** régua quando já existem três: um lead inbound descartado seguia
recebendo TI2 a TI5. O nó 2 da Interceptação de Sinal (2.9.2/2.9.3) ganhou
`status não é lost` em vez de `é open`, de propósito — clique de lead em
nutrição é sinal, não ruído (nota na própria seção). Duas dessas peças já
estão publicadas na tela: os retoques estão na tabela de
`GUIA-MONTAGEM.md`, "Estado da montagem em 19/09/2026".

**Segue aberto:** 2.13 a 2.17, seção 5 e 5.1-5.4, seção 6,
listas 8.5 em diante, seção 9 e o checklist de teste (seção 10) — todos
listados item a item em `GUIA-MONTAGEM.md`, dentro da Fase 1.

---

## Bloco 1 — Medição (a maior lacuna)

Hoje a máquina executa e não se mede. Um SDR sem medição é um SDR com opinião.

### R-01 · Métricas de cadência por tentativa e por canal — **FEITO em 18/09/2026**
**Por quê:** a pergunta que paga a operação é "a T7 ainda vale a pena?". Sem
taxa de conexão por tentativa, a cadência de 12 é fé, não desenho.
**Como:** campos contadores por canal (`Tentativas telefone`,
`Tentativas WhatsApp`, `Conexões telefone`, `Conexões WhatsApp`) alimentados
pelo Pós-ligação, e listas inteligentes agrupando por `Tentativa nº`.
**Pronto quando:** dá para responder "qual tentativa conecta mais" sem planilha.

**Resumo:** campos C-09 a C-12 especificados em `campos-e-tags.md`, nós do
Pós-ligação atualizados em `build-wesales.md` (seção 4) e lista inteligente
`Conexão por Tentativa` criada (seção 8.6) — falta só a criação manual dos 4
campos na tela (a subconta segue com 0 campos e 0 contatos, confirmado por
`locations_get-custom-fields`/`contacts_get-contacts` nesta execução).

### R-02 · Speed-to-lead — **FEITO em 18/09/2026**
**Por quê:** é a métrica nº 1 de inbound na literatura de vendas, e a que mais
move conversão. Ninguém mede porque ninguém guarda o par de horários.
**Como:** carimbos `Entrada em` e `1ª tentativa em`, ambos **`TEXT` no formato
`AAAA-MM-DD HH:MM`** — e não `DATE`. Medido em 18/09/2026: campo `DATE` do GHL
descarta a hora, e speed-to-lead medido em minutos entre duas datas sem hora dá
zero no mesmo dia. A diferença entre os dois carimbos é a métrica.
**Pronto quando:** existe lista "leads com mais de 1h sem primeira tentativa".

**Resumo:** campos C-18/C-19 especificados em `campos-e-tags.md`; nó 0.6 e o
par 5c/5d (só na T1) especificados em `build-wesales.md` (seção 2.4); como
campo `TEXT` não aceita filtro relativo de data em lista inteligente, o "mais
de 1h" saiu de um workflow-relógio, não de um filtro — `Alerta de
Speed-to-lead` (seção 2.11) espera 1h e marca a tag `atraso-1a-tentativa`, que
a lista `Atraso na 1ª Tentativa` (8.8) só lê. **Falta só a criação
manual dos 2 campos** (campo personalizado não sai por API) — a tag nova,
`atraso-1a-tentativa` (12ª, fora do lote das 11 autorizadas por nome),
foi aprovada ao vivo em chat e **criada em 18/09/2026** via
`contacts_add-tags`. Subconta reconfirmada nesta
execução via `locations_get-custom-fields`/`contacts_get-contacts`/
`opportunities_get-pipelines`: segue em 0 campos, 0 contatos, só o
`FUNIL DE VENDAS` pré-existente — nada mudou desde a auditoria.

### R-03 · Funil do SDR por período — **FEITO em 18/09/2026**
**Por quê:** entraram / conectaram / agendaram / compareceram é o funil que o
gestor olha. Hoje só existe o estado atual, não o fluxo.
**Como:** campos de data por marco (`Data conectado`, `Data agendado`,
`Data compareceu`) + listas filtradas por período.
**Pronto quando:** dá para dizer a taxa de conexão do mês sem contar na mão.

**Resumo:** campos C-20 a C-22 especificados em `campos-e-tags.md`; nó novo
no ramo `Atendeu` do Pós-ligação (seção 4) e no Pós-agendamento (seção 5)
grava `Data conectado`/`Data agendado`; workflow novo `Registro de
Comparecimento` (seção 5.2) grava `Data compareceu` a partir do status
`Showed` do calendário. Pesquisado antes de desenhar: o filtro nativo do GHL
`Last Stage Change Date` só reflete a etapa atual e subcontaria quem já
avançou — carimbo próprio por marco não tem esse defeito. O quarto marco,
"entraram" (lista 8.9), não ganhou campo novo: usa o `Data de criação`
nativo da oportunidade, que também não muda com o avanço de etapa. As
quatro listas (8.9 a 8.12) ficam em `build-wesales.md`, seção 8. Falta só a
criação manual dos 3 campos na tela — campo personalizado não sai por API;
subconta reconfirmada nesta execução via
`locations_get-custom-fields`/`contacts_get-contacts`/
`opportunities_get-pipelines`: 0 campos, 0 contatos, só o `FUNIL DE VENDAS`
pré-existente.

---

## Bloco 2 — Conteúdo que se mede

### R-04 · Biblioteca de mensagens versionada — **FEITO em 18/09/2026**
**Por quê:** em Reev/Meetime o template é objeto de primeira classe, com
desempenho próprio. Aqui as mensagens estão soltas dentro do workflow.
**Como:** campo `Template usado` preenchido junto com cada envio, e os textos
num documento versionado com código (`M1-a`, `M1-b`, `M2-a`...).
**Pronto quando:** dá para dizer qual abertura teve mais resposta.

**Resumo:** campo C-23 (`TEXT`, não `SINGLE_OPTIONS` — evita reabrir o campo
na tela a cada versão nova) especificado em `campos-e-tags.md`; nó de escrita
em cada mensagem automática (M1/M2/M3) especificado em `build-wesales.md`
(seção 2.6); textos movidos para `biblioteca-mensagens.md`, novo, único dono
do conteúdo e da regra de versionamento (nunca editar em vigor, sempre nova
linha com código novo); lista inteligente `Resposta por Template` criada
(seção 8.13), cruzando o sinal de resposta já gravado pelo F-01 com o código
do template — sem campo de contagem novo. Pesquisado antes de desenhar: os
textos viviam só dentro do build, duplicá-los na biblioteca seria a mesma
armadilha de número repetido que o projeto já corrigiu para contagem — por
isso o build passou a referenciar a biblioteca em vez de repetir o texto.
Falta só a criação manual do campo — campo personalizado não sai por API; a
subconta segue com 0 campos e 0 contatos, reconfirmado nesta execução via
`locations_get-custom-fields`/`contacts_get-contacts`/
`opportunities_get-pipelines`, só o `FUNIL DE VENDAS` pré-existente.

### R-05 · Teste A/B da abertura — **FEITO em 18/09/2026**
**Por quê:** a M1 decide se existe cadência. É o único texto que merece teste.
**Como:** If/Else alternando duas versões da M1 e gravando qual em
`Template usado`.
**Pronto quando:** duas versões rodando e a comparação sai da lista inteligente.

**Resumo:** o desenho trocou If/Else-por-alternância pela ação nativa
**Split** do GHL (sorteio aleatório por percentual, com permanência do
contato no caminho sorteado) — é como o Outreach.io faz A/B de step de
sequência, e evita correlacionar a variante com a ordem de entrada do lead,
que é o viés que um If/Else alternado introduziria. Nós especificados em
`build-wesales.md` (seção 2.6.1); `M1-a` (controle, texto idêntico ao antigo
`M1-v1`) e `M1-b` (gancho de dor do segmento, variando só o gancho de
abertura) escritos em `biblioteca-mensagens.md`, que também marca `M1-v1`
como substituído sem apagar a linha. Nenhum campo ou tag novo: reaproveita
`Template usado` (C-23) e a lista `Resposta por Template` (8.13) do R-04 —
por isso este item não depende de criação manual nem de `APROVADO.md`.
Subconta reconfirmada nesta execução via `locations_get-custom-fields`/
`contacts_get-contacts`/`opportunities_get-pipelines`: segue em 0 campos, 0
contatos, só o `FUNIL DE VENDAS` pré-existente — nada mudou desde a
auditoria.

### R-06 · Script de ligação e playbook de objeções — **FEITO em 18/09/2026**
**Por quê:** o SDR liga 100 vezes por dia. Sem script, cada ligação é
improviso, e o que funciona não vira repertório do time.
**Como:** documento com abertura, pergunta de diagnóstico, ponte para o
agendamento e as 8 objeções mais comuns com respostas.
**Pronto quando:** um SDR novo liga no segundo dia.

**Resumo:** escrito em `script-de-ligacao.md`, novo — o par falado de
`biblioteca-mensagens.md`. Pesquisado antes de escrever: em Reev, Meetime,
Outreach e Salesloft o script da ligação e o formulário de qualificação são
dois objetos separados, preenchido o segundo de memória depois de desligar.
Aqui as perguntas de diagnóstico seguem a mesma ordem e agrupamento dos
blocos de pontuação da seção 9.1 do `build-wesales.md` (Fit → Mídia → BANT),
então o SDR preenche a régua enquanto fala, não depois. Cobre abertura,
recado de caixa postal, 10 perguntas mapeadas aos campos `Q-04` a `Q-17`
(`campos-e-tags.md`), ponte para o agendamento e as 8 objeções, e estende ao
SDR humano a mesma regra de ouro que já valia só para o bot de WhatsApp
(`build-wesales.md`, seção 6): nunca prometer preço, desconto ou garantia.
Item de conteúdo puro — nenhum campo, tag ou nó de workflow novo; não
depende do conector nem de `APROVADO.md`.

---

## Bloco 3 — Cadências vizinhas

### R-07 · Cadência inbound (lacuna L-04) — **FEITO em 18/09/2026**
**Por quê:** as tags `cad-inbound`/`cad-outbound` existem e só há cadência
outbound. Inbound com cadência de 30 dias é lead perdido: a régua é em minutos.
**Como:** cadência própria — tentativa em 5 min, 30 min, 2h, 1 dia, 3 dias.
**Pronto quando:** formulário preenchido dispara ligação em minutos.

**Resumo:** workflow novo `Cadência Inbound` especificado em
`build-wesales.md`, seção 2.10 — mesmo gatilho da Cadência 12x30 (Opportunity
Stage Changed → `Em cadência`), separado por um filtro de tag oposto nos dois
gatilhos (`cad-inbound` presente/ausente, seção 2.1), sem If/Else de portão
decidindo isso dentro do fluxo. Esperas por `Wait → Time Delay` relativo
(não horário fixo, que não faz sentido numa régua de minutos); lead entra
com `Prioridade` = 5 e tag `fila-quente` de saída, e uma mensagem automática
imediata (`MI-0`, `biblioteca-mensagens.md`) confirma o recebimento antes da
1ª ligação. Sem conexão ao fim da TI5, handoff por `Add to Workflow` para a
Cadência 12x30 (mensagem `MI-F`) — pesquisado e confirmado que essa ação
entra direto na sequência do workflow de destino sem reavaliar o filtro do
gatilho, o mesmo mecanismo que a Qualificação por IA (seção 2.7) já usa. A
tag `cad-inbound` nunca é removida: é origem do lead, não fila. O alerta de
speed-to-lead (R-02, seção 2.11) ganhou um relógio mais curto (15 min em vez
de 1h) quando a origem é inbound, reaproveitando a mesma tag
`atraso-1a-tentativa` e a mesma lista 8.8 — zero campo e zero tag novos
neste item. Pesquisado antes de desenhar: o benchmark do Meetime (64% de
conexão respondendo em até 10 min, SLA recomendado de 5 min para inbound
direto) e a estatística de conversão até 21x maior respondendo nos primeiros
5 minutos validam os degraus do roadmap; Outreach e Salesloft são desenhados
para outbound e não têm régua nativa em minutos para lead entrante — é a
lacuna que este item fecha usando só workflow nativo do GHL. Zero criação
no CRM (nenhum campo ou tag nova): não depende de `APROVADO.md`.

### R-08 · Reengajamento dos 90 dias — **FEITO em 18/09/2026**
**Por quê:** `nutricao-90d` marca a saída e nada traz de volta. Nutrição sem
retorno é arquivo morto.
**Como:** workflow que, aos 90 dias, devolve para `Novo lead` com tag
`cad-outbound` e uma abertura diferente da primeira rodada.
**Pronto quando:** o lead de hoje volta à fila em dezembro, sozinho.

**Resumo:** workflow novo `Reengajamento 90 dias` especificado em
`build-wesales.md` (seção 2.12) — dispara ao entrar em `Nutrição`, espera
90 dias, troca `cad-inbound` por `cad-outbound` (a reativação é sempre
outbound, mesmo para quem nasceu inbound — a origem histórica cede lugar
ao roteamento correto, ver seção 2.12) e roda uma régua própria de 4
tentativas em 10 dias (TR1-TR4), mais curta que a original de propósito:
lead reciclado não merece a mesma intensidade de quem está chegando agora,
é o padrão que a literatura de reengajamento já trata como piso. Sem
resposta ao fim, volta para `Nutrição` sozinho e o próprio workflow
dispara de novo 90 dias depois — o ciclo se repete indefinidamente, sem
depender de ninguém abrir uma lista, o que nem Reev nem Meetime fazem
nativamente (os dois tratam isso como relatório manual). Pesquisado e
resolvido antes de montar: reaproveitar a Cadência 12x30 diretamente para
a reativação esbarraria no `Allow Re-entry` desligado dela (D-06,
`briefing-sdr.md`) — um workflow próprio, isolado, com sua própria
configuração de reentrada, resolve sem tocar numa decisão já fechada.
Tag nova `reengajamento-ativo` (T-13, `campos-e-tags.md`) blinda o
gatilho da Cadência 12x30 (seção 2.1) contra entrada dupla de um lead
reativado que nunca tinha passado por aquele workflow específico — a
Cadência Inbound (seção 2.10) já fica de fora sozinha, porque o mesmo nó
que soma `cad-outbound` também remove `cad-inbound`, e é isso que o
filtro dela exige presente. Mensagens `RE-1`/`RE-2` novas em
`biblioteca-mensagens.md`. Zero campo novo — reaproveita `Tentativa nº`,
`Entrada em`, `1ª tentativa em`, `Prioridade` e `Template usado`, todos já
existentes; a tag T-13 foi aprovada ao vivo em chat e **criada em
18/09/2026** via `contacts_add-tags`. Nova lacuna registrada dentro da
seção 2.12:
**L-07 — promoção automática de `Novo lead` → `Em cadência`**, descoberta
ao notar que "devolver para `Novo lead`" (como o roadmap pedia
literalmente) deixaria o lead reativado parado para sempre, porque essa
transição ainda não tem gatilho nenhum — o workflow deste item move direto
para `Em cadência` para não herdar essa lacuna. Subconta reconfirmada
nesta execução via `locations_get-custom-fields`/`contacts_get-contacts`/
`opportunities_get-pipelines`: 0 campos, 0 contatos, só o
`FUNIL DE VENDAS` pré-existente — nada mudou desde a auditoria.

### R-09 · Regras de pausa — **FEITO em 18/09/2026**
**Por quê:** cadência que dispara em feriado ou com o SDR de férias queima
lead e credibilidade.
**Como:** tag `pausado` checada no portão, e calendário de feriados na janela
do workflow.
**Pronto quando:** o Natal não gera 120 tarefas.

**Resumo:** dois mecanismos para dois problemas de tamanho diferente,
especificados em `build-wesales.md` (seção 2.13). Pesquisado antes de
montar: o GHL não tem calendário de feriados dentro da janela de envio de
um workflow (pedido em aberto na base de ideias da HighLevel), mas tem um
recurso de conta separado — **Pausar Workflows em Datas Específicas**
(Automação → Global Workflow Settings) — que pausa workflows publicados
por intervalo de data, com opção `Annually` para feriado fixo e até 15
intervalos de até 15 dias cada; confirmado que ele represa a próxima ação
real (tarefa, mensagem) de qualquer contato que a encontrar durante a
pausa, não só quem entra pelo gatilho no período — por isso resolve
"feriado" e "SDR de férias" de graça, sem workflow novo nem tag em massa.
Substitui a metade "calendário" do desenho original do roadmap por essa
configuração nativa (melhor que reconstruir, mesmo raciocínio do Split do
R-05); o calendário de feriados fixos do Brasil (`build-wesales.md`, seção
2.13) já vem pronto para marcar `Annually` uma vez. A tag `pausado` (T-14,
`campos-e-tags.md`) sobrevive só para o problema que o calendário não
cobre — represar **um** lead específico sem ser opt-out — checada num
portão próprio (nó 2.5 da seção 2.4, nó 1.5 da seção 2.10) que espera em
laço em vez de tirar o lead do workflow, porque pausa é diferente de saída;
o Mestre de saída (seção 3) limpa a tag na saída real e o Alerta de
Speed-to-lead (seção 2.11) para de soar falso alarme em quem está pausado
de propósito. Lista `Pausados Individualmente` (8.15) nova. A tag T-14 foi
aprovada ao vivo em chat e **criada em 18/09/2026** via `contacts_add-tags`
— falta só a configuração da pausa nativa na tela, que só existe depois dos
workflows publicados. Subconta reconfirmada
nesta execução via `locations_get-custom-fields`/`contacts_get-contacts`/
`opportunities_get-pipelines`: 0 campos, 0 contatos, só o `FUNIL DE VENDAS`
pré-existente — nada mudou desde a auditoria.

---

## Bloco 4 — Operação com mais de um SDR

### R-10 · Distribuição de leads — **FEITO em 18/09/2026**
**Por quê:** o desenho atual assume um SDR. No segundo, sem regra, os dois
ligam para o mesmo lead.
**Como:** round robin na atribuição da tarefa + campo `SDR responsável`, com
as listas inteligentes filtrando por usuário logado.
**Pronto quando:** dois SDRs trabalham sem colidir.

**Resumo:** especificado em `build-wesales.md`, seção 2.14 nova. O round
robin (ação nativa `Assign to User`) sorteia o **dono do lead uma vez**, no
nó 0 de quem primeiro recebe o lead (0.7b na Cadência 12x30, seção 2.3; 0.8b
na Cadência Inbound, seção 2.10, mesmo grupo de usuários nas duas) — não a
cada tarefa, como o texto literal do roadmap sugeria. Todo `Add Task` da
máquina (seção 2.4 nó 7, seção 2.9.2/2.9.3, seção 2.10 nó 6, seção 4 ramos
`Atendeu` e `Pediu retorno`) passou a atribuir a `Contact Owner`, dinâmico,
seguindo o dono sorteado — é a diferença entre um round robin que um
concorrente copia olhando a tela (sortear a cada tarefa) e um que não copia
(decidir *onde* sortear, para o lead manter um único dono do início ao fim
da cadência de 30 dias, prática que a literatura de sales engagement
recomenda e que sortear por tarefa quebraria). Pesquisado antes de desenhar
e decidido não criar o campo `SDR responsável` do roadmap: o GHL já expõe
nativamente o dono do contato (`Assigned User`) em filtro de lista e em ação
de workflow — um campo espelhado divergiria na primeira reatribuição feita
direto na tela. Achado que limita a segunda metade do "Como" do roadmap:
Smart List do GHL não tem filtro dinâmico "Atribuído a = usuário atual"
(pedido em aberto na base de ideias da HighLevel) — "listas inteligentes
filtrando por usuário logado" não existe como lista única; a alternativa
documentada é duplicar `Fila Quente`/`Fila Telefone Hoje`/`Fila WhatsApp
Hoje` (8.1-8.3) uma vez por SDR quando o segundo entrar, cada cópia com o
nome fixado no filtro — não antes, porque com 1 usuário não há o que
filtrar. Checklist de teste ganhou o item 28, que só valida de verdade com
2+ usuários na subconta — hoje ela tem só o dono. Zero campo e zero tag
novos: não depende de `APROVADO.md`. Subconta reconfirmada nesta execução
via `locations_get-custom-fields`/`contacts_get-contacts`/
`opportunities_get-pipelines`: 0 campos, 0 contatos, só o `FUNIL DE VENDAS`
pré-existente — nada mudou desde a auditoria.

### R-11 · Alerta de capacidade (lacuna L-05) — **FEITO em 18/09/2026**
**Por quê:** 10 leads/dia × 12 tentativas dá ~120 tarefas/dia em regime, acima
da meta de 100. A fila estoura silenciosamente.
**Como:** lista inteligente de tarefas abertas do dia + notificação ao gestor
acima do limite.
**Pronto quando:** o gestor sabe da fila cheia antes do SDR desistir dela.

**Resumo:** lista inteligente `Fila do Dia — Total` criada (`build-wesales.md`,
seção 8.16, nova) somando `fila-tel` e `fila-wa` sem duplicar ninguém — vale
como total de tarefas abertas hoje porque o bloco padrão de qualquer cadência
do projeto (seção 2.4 e as que a espelham) nunca aplica as duas tags ao mesmo
contato ao mesmo tempo. Pesquisado antes de desenhar e confirmado por
ausência: o motor de workflow do GHL não expõe, dentro de um workflow,
"quantos contatos passam por este filtro agora" — "métricas do dashboard como
custom value" segue como pedido em aberto na base de ideias da HighLevel —,
o que descarta um alerta condicionado de verdade ao limite ser cruzado.
Solução de três peças em vez de uma (seção 2.15, novo, do `build-wesales.md`):
a lista 8.16 para a contagem exata; uma métrica personalizada `Estouro da
Fila` (Reporting → Custom Metrics, se o plano da subconta expuser) que já
subtrai a meta de 100 para o gestor não fazer a conta de cabeça — um
concorrente olhando a tela vê a contagem crua, não o alarme embutido; e um
workflow contactless via gatilho nativo **Scheduler** (confirmado que roda
sem contato em contexto e não coexiste com outro tipo de gatilho) avisando o
gestor 2x por dia útil, em vez de um alerta condicional que a API não permite
construir. Limite documentado na seção 2.15: o aviso é por horário fixo, não
por limite cruzado de verdade — é a troca honesta que a plataforma impõe.
Zero campo e zero tag novos: reaproveita `fila-tel`/`fila-wa`, já aprovadas.
Checklist ganhou o item 29. Subconta reconfirmada nesta execução via
`locations_get-custom-fields`/`contacts_get-contacts`/
`opportunities_get-pipelines`: 0 campos, 1 contato (o `ZZ TESTE ESTRUTURA`
do R-anterior), só o `FUNIL DE VENDAS` pré-existente — nada mudou desde a
última checagem.

### R-12 · Handoff e no-show — **FEITO em 18/09/2026**
**Por quê:** reunião agendada que não acontece é o vazamento mais caro do
funil, e hoje o desenho termina no agendamento.
**Como:** gatilho de status `No-show` → volta para cadência com régua curta;
SLA do closer para dar retorno.
**Pronto quando:** no-show vira nova tentativa, não silêncio.

**Resumo:** dois workflows novos especificados em `build-wesales.md` — seção
5.3 (`Recuperação de No-show`) e seção 5.4 (`SLA do Closer — No-show`) —,
ambos no gatilho nativo `Appointment Status = No Show`, a mesma família do
`Showed` que já fecha o R-03. A régua curta (NS1-NS3, telefone, 4 dias)
gera a tarefa `NS1` no mesmo dia do no-show, e a seção 5.4 cobra do closer
um retorno em 2h com escalonamento ao gestor se ele não agir — a metade
"SLA do closer" do "Como" do roadmap. Aprendendo com o preço que o
Reengajamento 90 dias (R-08) pagou pelo `Allow Re-entry` desligado da
Cadência 12x30 (D-06), este item não tenta voltar o lead para `Em
cadência`: a oportunidade fica em `Reunião agendada`, o contador `Nº de
no-shows` (C-24, `campos-e-tags.md`) mora no contato, e uma lista própria
(8.17) mostra quem está na régua — **zero tag nova**. Diferencial sobre
Reev/Meetime/Outreach/Salesloft, pesquisado antes de desenhar: as quatro
tratam no-show repetido como métrica de relatório; aqui o 2º no-show
seguido descarta a oportunidade sozinho (proteção de agenda do closer),
decisão automática que nenhuma delas embute nativamente. Checklist ganhou o
item 30. Falta só a criação manual do campo C-24 — campo personalizado não
sai por API;
subconta reconfirmada nesta execução via
`locations_get-custom-fields`/`contacts_get-contacts`/
`opportunities_get-pipelines`: 0 campos, 6 contatos (o de estrutura + os 5
fictícios do checklist), só o `FUNIL DE VENDAS` pré-existente — nada mudou
desde a última rodada.

---

## Bloco 5 — Qualidade e confiança

### R-13 · Higiene de base — **FEITO em 18/09/2026**
**Por quê:** base suja infla métrica e queima SDR. A subconta bloqueia
duplicata por e-mail e telefone, o que ajuda, mas não cobre número inválido
nem lead sem telefone.
**Como:** lista inteligente de contatos sem telefone válido; rotina de
marcação, nunca de exclusão.
**Pronto quando:** a fila do SDR não tem lead impossível de ligar.

**Resumo:** portão novo (nó 0.0/0.0b, `build-wesales.md` seções 2.3 e 2.10)
na entrada da Cadência 12x30 **e** da Cadência Inbound — contato sem
telefone nunca chega a gastar as 12 tentativas: sai direto para `Nutrição`
(com e-mail/Instagram) ou `Descartado`, com a mesma tag `telefone-invalido`
(T-09) e o mesmo critério que o ramo reativo `Número errado` (seção 4) já
usa — zero campo e zero tag novos. Pesquisado antes de desenhar: o portão
por tentativa (nó 3, seção 2.4) já bloqueava telefone quando essa tag está
presente, mas não bloqueava WhatsApp — e neste projeto WhatsApp também
depende do número de telefone do contato (`briefing-sdr.md`), então um lead
sem telefone nenhum passaria pela T1 inteira antes de qualquer verificação
rodar; o novo portão resolve antes da primeira tentativa existir. Lista
inteligente `Higiene — Sem Telefone Válido` criada (seção 8.18), juntando
os dois jeitos de ficar "impossível de ligar" (nasceu sem número, ou foi
invalidado depois) — a peça de marcação (nunca exclusão) que o "Como" do
roadmap pedia. Peça complementar e opcional (seção 2.16): o recurso nativo
**Number Validation** do GHL, que fecha o caso que o portão 0.0 não cobre —
telefone presente mas com formato ruim ou linha desligada —, pesquisado e
registrado com nível de confiança médio (documentação oficial bloqueada
pelo proxy deste ambiente; achado só por busca) e desenhado para ser
dispensável se o plano da subconta não expuser o recurso. Falta só a
criação manual dos nós na tela (workflow não sai por API) — subconta
reconfirmada nesta execução via `locations_get-custom-fields`/
`contacts_get-contacts`/`opportunities_get-pipelines`: 0 campos, 6
contatos, só o `FUNIL DE VENDAS` pré-existente — nada mudou desde a última
rodada.

### R-14 · Auditoria de compliance
**Por quê:** `nao-perturbe` e DND são a linha entre prospecção e perseguição.
Precisa ser verificável, não confiável.
**Como:** rotina que confere se algum contato com DND recebeu mensagem, e se
algum envio saiu fora da janela.
**Pronto quando:** existe relatório que prova que ninguém foi incomodado
indevidamente.

### R-15 · Dashboard do gestor — **FEITO em 18/09/2026**
**Por quê:** todo o resto acima morre se depender de alguém abrir seis listas.
**Como:** dashboard nativo com ligações/dia, conexões/dia, agendamentos,
taxa por tentativa, fila em atraso.
**Pronto quando:** o gestor abre uma tela e sabe se o dia foi bom.

**Resumo:** dashboard `Painel do Gestor — Pré-vendas` especificado em
`build-wesales.md` (seção 2.17) com quatro peças nativas: widget
"Appointment Report" (agendamentos, lendo o calendário da seção 7.1),
widget "Opportunities" (funil ao vivo do pipeline `Pré-vendas`, diferente
dos totais mensais das listas 8.9-8.12), widget "Tasks" (proxy do volume
de ligações do dia) e quatro Custom Metrics — `Estouro da Fila` (já do
R-11) mais três novas: `Atrasos de Speed-to-lead`, `Taxa de Conexão —
Telefone` e `Taxa de Conexão — WhatsApp`. Pesquisado antes de desenhar:
Smart List não pode virar widget de Dashboard no GHL (pedido em aberto na
base de ideias da HighLevel) — descarta pinar as listas 8.1-8.18 direto,
o dashboard aponta para elas em vez de repeti-las; e Custom Metrics aceita
`Sum`/`Min`/`Max`/`Average` sobre campo numérico, não só contagem de tag —
achado que deixou os contadores do R-01 (C-09 a C-12) virarem métrica sem
campo novo. Limite documentado na seção 2.17: os contadores do R-01 são
cumulativos (nunca resetam, de propósito — mesma razão do R-01), então
"ligações/dia" e "conexões/dia" **literais** não têm caminho nativo com os
campos atuais; o dashboard entrega taxa de conexão acumulada (mesma
granularidade da lista 8.6) e o volume de tarefas do dia como proxy, não a
contagem exata por dia — a mesma classe de troca honesta que o R-11 já
aceitou. Zero campo e zero tag novos: as três Custom Metrics novas
reaproveitam C-09 a C-12 (R-01) e a tag `atraso-1a-tentativa` (T-12,
R-02). Falta só a montagem manual na tela — dashboard e Custom Metrics não
saem por API; Custom Metrics é recurso de plano pago (mesma cautela já
registrada para o R-11), então os dois primeiros widgets (nativos,
qualquer plano) sozinhos já cobrem metade do "Pronto quando" se o plano
não incluir o recurso. Subconta reconfirmada nesta execução via
`locations_get-custom-fields`/`contacts_get-contacts`/
`opportunities_get-pipelines`: 0 campos, 6 contatos, só o
`FUNIL DE VENDAS` pré-existente — nada mudou desde a última rodada.

### R-16 · Régua de nota com rótulo que não existe na tela — **FEITO em 19/09/2026**
**Por quê:** lacuna achada nesta rodada, não prevista nas anteriores. Quem
montou os 46 campos na tela (Fase 2 do `GUIA-MONTAGEM.md`) trocou o rótulo
de opção de nove campos de qualificação em relação ao que
`campos-e-tags.md` sugeria — e `CONFERENCIA-CAMPOS.md` já tinha catalogado
isso em 18-19/09, mas a correção ficou só catalogada: a régua de nota
(`build-wesales.md`, seção 9.1) continuava comparando contra os rótulos
antigos. Um `If/Else` que compara texto contra opção que não existe mais
nunca casa — a nota de qualificação (que decide `Prioridade`, fila quente e
o corte para nutrição/descarte) sairia errada em produção sem nenhum erro
visível, a mesma classe de bug silencioso que o achado de `fieldKey` já
descreveu para merge field, aplicada aqui a valor de opção.
**Como:** reler `locations_get-custom-fields`, comparar contra
`campos-e-tags.md` e `build-wesales.md` seção 9.1, e corrigir os dois para
usar o rótulo real da tela em vez do sugerido.
**Pronto quando:** nenhum `If/Else` da régua de nota compara contra um
rótulo que a tela não tem.

**Resumo:** nove campos corrigidos em `campos-e-tags.md` (Q-01, Q-04, Q-06,
Q-08, Q-10, Q-12, Q-15, Q-17, Q-18) e a seção 9.1 do `build-wesales.md`
reescrita com os rótulos reais — detalhe completo, incluindo por que só
`Tem time comercial` precisou de um remapeamento de pontuação de verdade
(as outras faixas bateram degrau a degrau, só o texto mudou), em
`CONFERENCIA-CAMPOS.md`, seção G. `GUIA-MONTAGEM.md` e
`script-de-ligacao.md` também tinham as mesmas citações desatualizadas,
corrigidos junto. Lição registrada em `APRENDIZADOS-CRM.md`: um arquivo de
auditoria que lista "ajustar o documento" documenta o achado, não a
correção — quem pegar o próximo item precisa conferir se a edição foi
feita de verdade, não assumir que aparecer no arquivo de auditoria
significa resolvido. **Segue aberto, sem mudança nesta rodada:** o tipo
errado de `Plataformas de anúncio` (`SINGLE_OPTIONS`, devia ser
`MULTIPLE_OPTIONS` — perda de função de verdade, não só rótulo), a criação
de `Hora do retorno`, e a decisão sobre os campos duplicados `Necessidade`/
`Urgência` — nenhum dos três é ajuste de texto: os dois primeiros pedem
ação manual na tela, o terceiro pede decisão do dono.

---

## Bloco 6 — fora da curva

Aqui não é paridade. É o que separa uma operação boa de uma operação que os
concorrentes não conseguem copiar olhando de fora.

### F-01 · Cadência que reage a sinal, não só a calendário — **FEITO em 18/09/2026**
**Por quê:** uma régua por dia trata igual quem abriu a mensagem três vezes e
quem nunca viu. O lead **dá sinal** — clica, responde, volta ao site — e a
cadência segue no D7 como se nada tivesse acontecido. É o desperdício mais caro
de qualquer operação de prospecção.
**Como:** link de gatilho nas mensagens; `Trigger Link Clicked` e
`Customer Replied` como gatilhos de um workflow de interceptação que põe
`Prioridade` = 5, aplica `fila-quente` e cria tarefa para agora, furando a fila
do dia.
**Pronto quando:** lead que clicou às 14h é ligado às 14h10, não no D7.

**Resumo:** seção 2.9 do `build-wesales.md` especifica o Trigger Link
`Agendar com o closer` embutido em M2/M3 e os dois workflows curtos
("— Clique" e "— Resposta") que fazem a interceptação; campos C-13/C-14
especificados em `campos-e-tags.md` — falta só a criação manual (Trigger Link
e campos não saem por API; a subconta segue com 0 campos e 0 contatos,
reconfirmado nesta execução via `locations_get-custom-fields`/
`contacts_get-contacts`).

### F-02 · Melhor horário aprendido, por segmento — **FEITO em 19/09/2026**
**Por quê:** a tabela de horários das 12 tentativas é a mesma para todo mundo.
Mas dentista atende às 14h e obra atende às 7h. A operação descobre isso depois
de trezentas ligações — e não usa.
**Como:** gravar `Hora da conexão` sempre que o resultado for `Atendeu`;
comparar por `Segmento`; ajustar os horários das tentativas por faixa.
**Pronto quando:** o horário da T3 de um segmento é diferente do de outro, e a
diferença veio de evidência, não de palpite.

**Resumo:** campo C-25 (`Hora da conexão`, `TEXT` só a hora, formato `HH`)
especificado em `campos-e-tags.md`; nós 7b/7c novos no ramo `Atendeu` do
Pós-ligação (`build-wesales.md`, seção 4) gravam a hora com o `Date/Time
Formatter`; lista `Conexão por Segmento e Horário` (seção 8.19) cruza
`Segmento` com a hora, ordenada para o gestor ver o agrupamento sem
planilha nem Custom Metric (Smart List não agrupa nem tira média, mesmo
achado já registrado para o R-11). Pesquisado antes de desenhar: a
literatura de outbound converge em janelas médias de mercado (manhã e fim
de tarde) e o Rhythm da Salesloft faz send-time optimization só para
e-mail — nenhuma fonte encontrada aprende horário de **ligação** por
segmento a partir da conexão real do próprio cliente, o diferencial que
este item fecha sem depender de IA de terceiro. Novo mecanismo
especificado na seção 2.18 (`build-wesales.md`) para o dia em que a
lista 8.19 mostrar padrão: um `If/Else` por `Segmento` antes do nó 2
("Aguardar horário") do bloco padrão de tentativa (seção 2.4), com a
tabela 2.5 atual como `senão`. **Decisão de bloqueio, não lacuna
esquecida:** o `If/Else` em si não foi construído nesta rodada — com 0
conexões reais na subconta (reconfirmado nesta execução), qualquer ramo
por segmento agora seria palpite, o oposto do "Pronto quando" do item;
falta a criação manual do campo (campo personalizado não sai por API
neste conector) e, depois disso, volume real para o padrão aparecer.
Escopo documentado: o mecanismo cobre só a Cadência 12x30 (horário de
relógio fixo) — a Cadência Inbound (seção 2.10) usa espera relativa em
minutos, onde "horário aprendido" não se aplica pela própria natureza da
régua. Checklist ganhou o item 33. Subconta reconfirmada nesta execução
via `locations_get-custom-fields`/`opportunities_search-opportunity`/
`opportunities_get-pipelines`: 46 campos (nenhum deles o C-25 ainda), 0
oportunidades, pipeline `FUNIL DE VENDAS` com as mesmas 5 etapas desde
18/09/2026.

### F-03 · Loop do closer de volta para o SDR — **FEITO em 18/09/2026**
**Por quê:** este é o defeito mais comum e mais caro em pré-vendas. O SDR
agenda e **nunca descobre se agendou bem**. Sem isso, a nota de qualificação
nunca se calibra: ela é uma opinião que ninguém conferiu.
**Como:** campos `Reunião foi qualificada` (Sim / Não / Parcial) e
`Motivo da desqualificação`, preenchidos pelo closer no pós-reunião; relatório
cruzando a nota que o SDR deu com o veredito do closer.
**Pronto quando:** dá para dizer "nota ≥ 70 acerta X%" — e corrigir a régua da
seção 9 com dado, não com achismo.

**Resumo:** campos C-15 a C-17 especificados em `campos-e-tags.md`; workflow
`Loop do closer` especificado em `build-wesales.md` (seção 5.1), roteando por
veredito e motivo para `Nutrição`/`Descartado` sem tocar em `FUNIL DE VENDAS`;
lista inteligente `Calibração da Régua` criada (seção 8.7). Diferencial sobre
Reev/Meetime/Outreach/Salesloft, que fecham este loop só em relatório
agregado: dois nós de alerta em tempo real (nota ≥ 70 com veredito `Não`, ou
nota < 45 com veredito `Sim`) avisam o gestor no dia da reunião, não no
relatório do mês. Falta só a criação manual dos 3 campos na tela — campo
personalizado não sai por API; subconta reconfirmada nesta execução via
`locations_get-custom-fields`/`contacts_get-contacts`/
`opportunities_get-pipelines`: 0 campos, 0 contatos, só o `FUNIL DE VENDAS`
pré-existente.

### F-04 · Teto de toques por semana — **FEITO em 19/09/2026**
**Por quê:** lead em duas cadências recebe o dobro de toques, e ninguém percebe
até o opt-out chegar. Frequência é o que transforma prospecção em perseguição.
**Como:** campo `Toques na semana`, incrementado a cada envio e cada ligação,
zerado semanalmente, checado no portão de toda tentativa.
**Pronto quando:** nenhum lead recebe mais que N toques por semana, venha de
onde vier.

**Resumo:** campo C-26 e workflow novo "Contador de Toques" especificados em
`build-wesales.md`, seção 2.19. Achado ao desenhar: a frase original do
roadmap ("duas cadências") não é o risco real deste projeto — as réguas
vizinhas já têm blindagem de tag uma-ou-outra (R-07/R-08); quem não tem
nenhum teto é a Interceptação de Sinal (F-01, seção 2.9), que roda em
paralelo com `Allow Re-entry` ligado e pode empilhar tarefa+aviso sem limite
a cada clique ou resposta do mesmo lead. Pesquisado antes de desenhar: o
Outreach.io resolve o caso citado no roadmap com **Sequence Exclusivity**
(trava de admissão — não deixa entrar em duas sequências), não com um
contador de frequência; nenhuma fonte encontrada descreve um teto rolante
por contato somando telefone, WhatsApp e sinal no mesmo número, o desenho
escolhido aqui. Contador **`NUMERICAL`, janela móvel de 7 dias corridos**
(soma no toque, desconta 7 dias depois pelo próprio workflow, sem depender
de zerar numa data fixa) reaproveita a tag `toque` (T-15, `campos-e-tags.md`,
criada nesta rodada) como pulso de evento — mesma ideia da Interceptação de
Sinal, sem precisar de aritmética de data sobre campo `TEXT` (a mesma
armadilha que o R-02 já documentou). Teto escolhido: 6/semana, acima do
pico real da Cadência 12x30 sozinha (4, D1+D2) e dentro da faixa "3 a 5-8"
que a literatura de outbound trata como segura contra fadiga do prospect.
**Escopo desta rodada, decisão e não lacuna esquecida:** a tag `toque` e o
portão de teto foram ligados nos dois pontos de maior risco (Cadência
12x30, seção 2.4, e as duas Interceptações de Sinal, seção 2.9.2/2.9.3) —
Cadência Inbound, Reengajamento 90 dias e Recuperação de No-show reaproveitam
o mesmo campo/tag/workflow sem precisar de nada novo, só falta ligar o nó
`Add Contact Tag: toque` em cada uma, registrado como pendência explícita em
`build-wesales.md` seção 2.19. Falta a criação manual do campo (campo
personalizado não sai por API) e da tag na tela do workflow (workflow não
sai por API); a tag T-15 em si já saiu por API: `contacts_add-tags` no
contato de estrutura, confirmado por `contacts_get-contact` — 15 tags do
projeto agora na subconta, `dateUpdated` 19/09/2026 04:15 UTC. Checklist
ganhou o item 35.

### F-05 · Monitor de saúde da operação
**Por quê:** automação falha **em silêncio**. Tag que não saiu, lead parado numa
etapa, workflow que parou de disparar — descobre-se pelo número caindo, semanas
depois, quando o estrago já aconteceu.
**Como:** rotina que confere invariantes e denuncia violação: contato com
`fila-tel` há mais de 24h, lead em `Em cadência` sem tentativa há 7 dias, tarefa
vencida sem resultado, contato com `nao-perturbe` ainda dentro de workflow ativo.
**Pronto quando:** a operação avisa que quebrou antes de o gestor perguntar.

**Adição de 18/09/2026, ao aplicar o "tempo de estagnação" do Sales Model
Canvas (Thiago Reis) etapa a etapa (seção 1 do `build-wesales.md`):** duas
invariantes novas para quando este item for construído, que a lista acima
não cobria — `Conectado` sem mover para `Retorno agendado`/`Reunião
agendada` em mais de 24h (o SDR atendeu e não fechou o loop) e `Retorno
agendado` com `Data do retorno` (S-01) vencida sem nova classificação (o
retorno combinado não aconteceu). As duas são o mesmo tipo de "estrago
silencioso" que motivou o item, só em etapas que a primeira versão do
"Como" não olhava.

### F-06 · Qualidade da conexão, não a contagem
**Por quê:** `Atendeu` empacota na mesma célula a ligação de 8 segundos e a de 8
minutos. A métrica que importa não é alô, é conversa.
**Como:** duração da ligação vinda do call tracking; campo `Conexão real` = 
atendeu **e** durou mais de 60s. A taxa de conexão do relatório passa a usar
esse campo.
**Pronto quando:** "taxa de conexão" no relatório significa conversa, e o SDR
não consegue inflar o número desligando rápido.

---

## Ordem sugerida

**Bloco 0 (G-01) fechado em 19/09/2026, antes de tudo o resto desta seção:**
não é item de fila, é pré-requisito — nenhum bloco abaixo importa enquanto
nenhuma oportunidade nasce sozinha. Descoberto depois dos blocos 1 a 5 e
quase todo o 6 já estarem prontos, mas listado primeiro porque é anterior
em sentido literal, não por ordem de descoberta.

**G-02, em andamento desde 19/09/2026, roda em paralelo aos blocos abaixo,
não antes deles:** ao contrário do G-01, uma seção de `build-wesales.md`
ainda com nome de etapa antigo não impede nenhum outro item de fazer
sentido — só faz aquela seção específica falhar quando alguém tentar
montá-la na tela. Por isso não bloqueia a fila; é trabalho de fundo,
pedaço por pedaço, cada vez que uma sessão automática não tem item de
volume/mensagem real para avançar nos blocos 1-6.

Medição primeiro (R-01, R-02, R-03), porque sem ela as decisões seguintes são
chute. Depois conteúdo (R-04, R-05, R-06), que é o que mais move resultado por
hora investida. Só então as cadências vizinhas e a operação com mais gente.

Com R-06 fechado em 18/09/2026, o bloco 2 (conteúdo) está completo. Com R-07,
R-08 e R-09 fechados na mesma data, o bloco 3 (cadências vizinhas) está
completo — a régua de reengajamento e todas as outras já respeitam feriado e
pausa individual antes de a operação rodar volume de verdade. Com R-10
fechado em 18/09/2026, o primeiro ponto que quebraria ao contratar o
segundo SDR (dois ligando para o mesmo lead) já está resolvido antes de
existir segundo SDR. Com R-11 fechado em 18/09/2026, o bloco 4 (operação com
mais de um SDR) está completo — a fila que R-10 distribui agora também avisa
quando estoura. Com R-12 fechado em 18/09/2026, o bloco 5 (qualidade e
confiança) começou a andar: reunião agendada que não acontece já tem tratamento,
do vazamento ao SLA do closer. Com R-13 fechado em 18/09/2026, base suja
já tem tratamento antes do primeiro lead de verdade entrar: contato sem
telefone nunca gasta as 12 tentativas, e o formato ruim mas presente tem
plano desenhado assim que o recurso nativo estiver ligado.

Com R-15 fechado em 18/09/2026, todo o resto que os blocos 1 a 4 e o R-13
já constroem tem onde ser visto numa tela só, em vez de morrer atrás de
seis listas que ninguém abre. **R-14 (auditoria de compliance)** é o único
item numerado (R/F) que resta no bloco 5 e no roadmap inteiro fora do
bloco 6 — fica fora de ordem por decisão de conteúdo, não de posição: sobe
para o topo no dia em que a operação começar a mandar mensagem de verdade.
Antes disso, não há a quem incomodar. (G-02, Bloco 0, é diferente dos
dois: não é item de fila que espera sua vez, é dívida de documentação que
se paga em paralelo, pedaço por pedaço — ver nota no início desta seção.)

F-01, F-03, F-02 e F-04 já saíram do bloco 6 fora da ordem normal, cada um na
rodada em que foi feito: sinal ignorado e nota não calibrada são dívidas que
não se pagam retroativamente — os dados que faltaram não voltam, calendário
nenhum devolve. F-02 é o mesmo tipo de dívida: cada dia sem `Hora da conexão`
sendo gravada é uma conexão que nunca vai ajudar a calibrar horário nenhum,
mesma razão que tirou F-01/F-03 da fila normal antes dele. F-04 saiu fora de
ordem por um motivo diferente dos outros três: não é dívida que se acumula
com o tempo, é uma exposição real já desenhada e sem teto (a Interceptação de
Sinal, F-01, empilhando toque sem limite) — corrigi-la antes da operação
rodar volume de verdade custa uma especificação; corrigi-la depois custaria
explicar a um lead por que ele recebeu seis avisos no mesmo dia. Restam dois
itens no bloco 6, e nenhum pede prioridade fora da ordem agora: os dois
pedem volume para fazer sentido. F-06 precisa de call tracking ligado; F-05
só morde quando há mais de uma cadência no ar.

**Não há mais "ordem normal" a retomar.** Esta frase dizia, desde a primeira
rodada, que o bloco 1 de medição terminaria e só então o bloco 2 entraria na
fila; os dois fecharam em 18/09/2026, junto com os blocos 3 e 4 e o R-13 do
bloco 5. O que resta entre os itens numerados não espera posição na fila,
espera a operação existir: R-14 quando a máquina começar a mandar mensagem
de verdade, e os dois itens que restam no bloco 6 quando houver volume.
Enquanto isso, o trabalho que sobra é de dois tipos: montar na tela o que
já está especificado (pipeline, campos, workflows, calendário e
formulário, pelo `build-wesales.md`) — trabalho manual, ao vivo com o
dono — e fechar o G-02 (migração de nomes de etapa), que uma sessão
automática consegue avançar sozinha, sem depender de tela nem de volume.
