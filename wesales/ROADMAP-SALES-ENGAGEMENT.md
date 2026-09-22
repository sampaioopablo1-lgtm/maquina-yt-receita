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

### G-02 · Migração de nomes de etapa em `build-wesales.md` ainda incompleta — **FEITO em 21/09/2026**
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

**Resumo (19/09/2026, quarta rodada):** fechadas as seções 5, 5.1, 5.2, 5.3
e 5.4 (Pós-agendamento, Loop do closer, Registro de Comparecimento,
Recuperação de No-show, SLA do Closer — No-show) — a família inteira do
pós-agendamento. `Reunião agendada` → `NEGOCIAR` em todo portão; os dois
destinos que existiam como etapa própria (`Nutrição`/`Descartado` — Loop do
closer, seção 5.1, e Recuperação de No-show, seção 5.3) viraram `status`
(`abandoned`/`lost`) sem sair de `NEGOCIAR`. Achado novo: o portão de
sanidade de 5.3 e 5.4 ("a oportunidade ainda reflete este compromisso?")
checava só a etapa — quinta peça a precisar do mesmo reforço `status é
open` que 2.11, o Mestre de saída, a reentrada de 2.12 e a conferência
acima já tinham exigido, aqui pelo motivo mais direto até agora: o Loop do
closer (5.1) já pode ter fechado o veredito sem sair de `NEGOCIAR`, e sem
checar `status` um `No Show` tardio reabriria uma recuperação ou repetiria
um SLA de um lead cujo destino já foi decidido. Zero campo, zero tag:
documentação pura.
**Achado à parte, fora da migração:** o dono confirmou ao vivo o estado real
da tela de workflows — `Pós-agendamento` publicado e ativo (3 inscritos),
mas `Cadência 12x30` (motor principal) e `Qualificação por IA no WhatsApp`
seguem em rascunho, e oito workflows do roadmap ainda não existem nem como
rascunho. A tentativa de montar `Loop do closer` usando o assistente
"Construir com IA" do GHL falhou três vezes seguidas, cada vez trocando um
campo inventado por outro (`Tags`, `Rescheduled`, `Opportunity status`,
`score`, `Last appointment at` — nenhum existe no projeto) em vez de usar os
campos reais (`Reunião foi qualificada`, `Motivo da desqualificação`, `Nota
de qualificação`) — mesma classe de falha já registrada para o Pós-ligação.
Detalhe completo: `APRENDIZADOS-CRM.md`.

**Resumo (19/09/2026, quinta rodada):** fechadas as seções 2.13 a 2.17
(Regras de pausa, Distribuição de leads, Monitor de Capacidade, Higiene de
Número, Dashboard do Gestor) — o pedaço de tamanho certo para uma execução
depois da família do pós-agendamento ter fechado a rodada anterior. Achado
real só na 2.16: o Ramo A (`Invalid`) tinha um nó ativo comparando etapa da
oportunidade contra `Novo lead`/`Em cadência`/`Retorno agendado` (segue) vs.
`Conectado`/`Reunião agendada`/`Nutrição`/`Descartado` (não segue) — nomes
que não existem mais na tela, e a "senão" misturava duas coisas diferentes
(etapa avançada e status de saída) que a tabela 1.0 já separa. Corrigido
para `NOVO LEAD`/`CONECTAR` **e** `status é open` (segue) vs. `AGENDAR`/
`NEGOCIAR` ou `status` já `abandoned`/`lost` (não segue) — sexta vez que
este mesmo reforço de `status` aparece numa migração (depois de 2.4, 2.10,
2.11, 2.12, Mestre de saída e a família 5.3/5.4), e sempre pelo mesmo
motivo: nome de etapa sozinho não diz se o lead ainda está de verdade
correndo a régua. O nó seguinte ("mover oportunidade → `Nutrição`/
`Descartado`") virou `Update Opportunity status = abandoned/lost`,
espelhando o 0.0b já migrado. As outras quatro subseções (2.13, 2.14, 2.15,
2.17) não tinham nó ativo com nome de etapa antigo — só uma menção solta em
texto corrido na 2.13 (`Em cadência` → `CONECTAR`) e referências
informais/de apelido (`Nutrição` em prosa na 2.14, `Pré-vendas` como nome do
pipeline na 2.17, ambas já documentadas como uso esperado desde a seção 1).
Zero campo, zero tag: item de documentação pura, não depende de
`APROVADO.md`. Detalhe completo em `build-wesales.md` (cabeçalhos das cinco
seções) e `GUIA-MONTAGEM.md` (checklist da Fase 1).

**Resumo (21/09/2026, sexta rodada) — G-02 fechado:** conferidas e fechadas
as últimas peças do checklist: 2.6.1/2.7/2.8/2.9–2.9.4 (zero achado — já
tinham sido escritas ou corrigidas contra as 5 etapas reais em rodadas
anteriores, só faltava marcar), seção 6 (Qualificação por IA — um nó ativo
migrado, "mover para `Nutrição`" → `status = abandoned`), seção 8 completa
(8.5–8.19; achado real na 8.17, `Recuperação de No-show`, cujo filtro
comparava contra `Reunião agendada`, nome que não existe mais — sétima
ocorrência da mesma classe de bug silencioso desde a seção 3), seção 9
(faixas C/D da nota de qualificação citavam etapa `Nutrição`/`Descartado`
em vez de `status`, e a regra 1 de `Prioridade` tinha um `ou etapa =
"Retorno agendado"` que nunca casava e nunca fazia falta — removido, mesmo
raciocínio já usado na lista 8.4) e o checklist de teste inteiro (seção 10,
vários pontos corrigidos nos cenários e nas verificações). `grep -n "Em
cadência\|Nutrição\|Retorno agendado\|Descartado\|Pré-vendas"
wesales/build-wesales.md` confirma: toda ocorrência restante é da tabela de
tradução (1.0) ou prosa histórica explicando a migração — nenhum gatilho,
portão ou nó ativo compara contra nome que a tela não tem. **Achado fora do
escopo de nome de etapa, corrigido junto por estar no mesmo checklist:** a
última linha da seção 10 mandava apagar as 5 oportunidades de teste ao
final — viola a regra 1 do projeto (nunca excluir oportunidade); corrigida
para marcar `status = lost`. Detalhe completo em `build-wesales.md` e
`GUIA-MONTAGEM.md` (checklist da Fase 1, agora com todas as caixas `[x]`).
Zero escrita no CRM: item de documentação pura, não depende de
`APROVADO.md`.

**Pronto quando (cumprido):** todo `[ ]` do checklist de migração em
`GUIA-MONTAGEM.md` (Fase 1) virou `[x]`.

### G-03 · L-07 deixou de ser lacuna teórica — 47 leads reais parados em `NOVO LEAD`, **envelhecendo** (não mais crescendo, medido em 22/09) — **aguarda decisão do dono**
**Por quê:** `briefing-sdr.md` já registrava a L-07 ("não existe gatilho que
promova `NOVO LEAD` → `CONECTAR`, hoje é decisão manual do SDR") desde
18/09/2026, com a nota "definir depois; se o volume crescer, resolve". O
volume cresceu: `opportunities_search-opportunity` em 21/09/2026 confirma
**47 oportunidades reais em `NOVO LEAD`** (a maioria Facebook Ads pago, de
verdade — nomes, telefone, e-mail e atribuição de campanha reais, não teste),
contra 40 em 19/09 — a Porta de Entrada (G-01) está trazendo lead novo todo
dia (~5-7/dia, batendo com a estimativa de "10 leads/dia" do `briefing-sdr.md`)
e **nenhum** chega a `CONECTAR` sozinho. O mais antigo visível já tem mais de
24h parado sem qualquer tentativa — o oposto do que R-02 (speed-to-lead) e
G-01 foram construídos para garantir, e o dinheiro do anúncio já foi gasto
para gerar esses 47 contatos. Diferença para as frentes que o roadmap trata
como "espera volume" (R-14/F-06 — **F-05 saiu dessa lista na mesma rodada,
como consequência direta deste achado**, ver seção do Bloco 6): aqui o
volume **já chegou** e o que falta não é uma métrica ficar interessante, é
o lead ser tocado.
**Como (três opções, nenhuma escolhida — decisão do dono, mesma régua da
L-02/D-04):**
1. **Promoção automática na entrada.** Workflow novo, gatilho `Opportunity
   Stage Changed` → `NOVO LEAD`, ação única `Update Opportunity` → etapa
   `CONECTAR`, sem espera. Seguro mesmo sem triagem humana: o portão de
   higiene de telefone que já existe na entrada da Cadência 12x30 (nó 0.0/
   0.0b, seção 2.3) roda de qualquer forma assim que a oportunidade chega em
   `CONECTAR` e já filtra quem não tem telefone válido — a promoção automática
   não pula essa proteção, só para de esperar um clique manual antes dela.
   Risco: lead duplicado, spam ou fora de perfil entra na régua de 12
   tentativas sem ninguém olhar antes.
2. **Promoção automática com janela de revisão.** Mesmo workflow do item 1,
   mas com `Wait` de X horas antes do `Update Opportunity` — dá ao SDR uma
   janela para tirar da fila manualmente (`status = lost`) um lead
   claramente ruim antes que ele gaste tentativa. Mais fiel ao espírito atual
   ("SDR revisa antes"), mas ainda fecha a lacuna de quem nunca é revisado.
3. **Ação manual em massa, uma vez, para destravar os 47 de hoje** —
   mesmo mecanismo que já resolveu o backfill do G-01 (ação nativa em massa
   na lista de oportunidades, mover para `CONECTAR`), sem workflow novo.
   Resolve o estoque parado agora; não resolve os próximos leads, que
   voltam a se acumular no dia seguinte sem o item 1 ou 2 também.
**Precondição que vale para as três opções, achada ao conferir este item em
21/09/2026 — a ordem não é livre:** o gatilho da Cadência 12x30 é
`Opportunity Stage Changed → CONECTAR` (seção 2.1), um **evento**, não um
estado. E a `Cadência 12x30` está **em rascunho** na tela (0 inscritos,
lista de workflows lida em 21/09). Promover os 47 antes de publicar a
cadência gasta o evento no vácuo: eles chegam em `CONECTAR`, nenhum
workflow está escutando, e **publicar a cadência depois não os inscreve** —
workflow do GHL inscreve na hora do gatilho, não varre quem já está na
etapa. Os 47 ficariam num limbo pior que o de hoje: fora de `NOVO LEAD` (e
portanto fora da lista de "leads que precisam de triagem") e fora da
cadência.

Recuperável, mas ao preço de tocar dado de produção duas vezes: ou
`Add to Workflow` em massa pela lista de contatos, ou tirar e recolocar a
etapa (o que gera evento novo; o `Allow Re-entry` desligado da D-06 não
bloquearia, porque ele só vale para quem já tem histórico *neste* workflow,
como a própria seção 2.1 explica). **Então a ordem certa é: publicar a
`Cadência 12x30` primeiro, conferir com 1 ou 2 leads, e só depois promover
o estoque.** Vale igual para a opção 3 (ação manual em massa), que é a mais
tentadora justamente por parecer não depender de nada.

**Cruzamento com o F-07 (22/09/2026) — promova em lotes, não os 47 de uma
vez:** qualquer das três opções acima, feita em bloco no primeiro dia da
cadência no ar, manda a M1 como Template para ~47 pessoas que nunca
escreveram para o número, tudo num dia, num número sem histórico. É o pior
começo possível de Quality Rating (F-07, seção 2.25 do `build-wesales.md`) —
e o remédio não custa nada: lotes de **10-13 leads/dia**, que é o regime
normal do briefing (L-05) e o mesmo ritmo que o SDR terá depois. Quatro dias
de promoção em vez de um.

**Cruzamento com o G-05 (21/09/2026):** a precondição acima ("publicar a
`Cadência 12x30` primeiro") ganhou um detalhe que vem do G-05 — publique-a
**sem os quatro nós de envio de WhatsApp**, que dependem de Template
aprovado pela Meta. As 12 tarefas de ligação, que são o motivo do item,
funcionam sem eles. Esperar a aprovação da Meta para publicar deixaria estes
47 leads sem ligação por mais dois dias sem ganho nenhum. A ordem completa
está na tabela do G-05.

**Por que não decidi sozinho:** mover 47 oportunidades reais de etapa é ação
em massa em dado de produção — regra 2 do briefing pede listar e confirmar
antes, e a régua de fila hoje é decisão deliberada do SDR (não bug), então
trocá-la por automática é mudança de processo, não correção de bug. Nenhuma
das três opções foi executada nem virou `[x]` em `APROVADO.md`.
**Pronto quando:** o dono escolhe uma opção (ou combina 3 com 1/2), ela vira
especificação em `build-wesales.md` e `[x]` em `APROVADO.md` antes de
qualquer escrita no CRM.

### G-04 · O formulário do Meta grava em campo que a régua não lê, e grava valor que o campo não aceita — **aguarda decisão do dono**
**Por quê:** lidos os 50 contatos em 21/09/2026 (`contacts_get-contacts`,
base inteira): as respostas do Meta Lead Ads caem em `Urgência` (39) e
`Necessidade` (34) — não em `Prazo` e `Dor principal`, que são os campos que
a régua de nota (seção 9.1) e o script de ligação leem. E `Investimento
mensal em anúncios` (`SINGLE_OPTIONS`) recebe `Não invisto nada ainda`,
`Até R$ 1.000`, `Abaixo de 5k` — três textos que não são opção do campo; a
integração grava mesmo assim. Consequência: para 37 dos 50 leads (todos do
Meta), o Bloco B da `Nota de qualificação` sai zerado em silêncio, e o SDR
pergunta ao telefone o que o lead já respondeu no anúncio. Não é hipótese
de documento — é o valor gravado hoje, lead por lead (`CONFERENCIA-CAMPOS.md`,
Tabela H). Descoberto ao auditar os dados em vez do texto: a Tabela F
esperava "decisão sobre `Necessidade`/`Urgência`" há dois dias enquanto os
dois campos enchiam.
**Como:** duas opções em `CONFERENCIA-CAMPOS.md`, Tabela H — (A) apontar o
formulário do Meta para `Prazo`/`Dor principal` e trocar as opções de
`Investimento mensal` pelos quatro textos exatos do anúncio, com a 9.1
reponderada; ou (B) a 9.1 passa a ler `Urgência`/`Necessidade` por
`Contains`. Em qualquer uma, os 34/39 valores antigos precisam de cópia em
massa para o campo certo (workflow `Update Contact Field` lendo outro campo,
a confirmar na tela) ou ficam fora da nota.
**Medido depois, e muda a conta (21/09/2026):** `attributions[].mediumId`
mostra **oito formulários de Lead Ads distintos** alimentando a subconta (42
/ 16 / 14 / 2 / 1 / 1 / 1 / 1 atribuições) — então a Opção A é trabalho de
tela **oito vezes**, e todo formulário novo nasce errado até alguém lembrar;
a Opção B se aplica uma vez e cobre os oito. E valendo para as duas: a régua
precisa ler `Necessidade` **e** `Dor principal` em OU (34 leads num, 5 no
outro, porque o mapeamento trocou no meio) — ler só um lado está errado para
parte da base durante toda a transição. Detalhe em `CONFERENCIA-CAMPOS.md`,
Tabela H.
**Por que não decidi sozinho:** muda a nota do lead (D-05) e o formulário do
anúncio — decisão de negócio, e nenhuma das duas sai por API.
**Pronto quando:** o dono escolhe A ou B; `campos-e-tags.md` (Q-06, Q-16,
Q-17) e a seção 9.1 refletem os valores que o Meta grava de verdade; um lead
novo do Meta chega com `Prazo`/`Dor principal`/`Investimento mensal`
preenchidos e a nota calculada.

### G-05 · Mensagens automáticas de WhatsApp especificadas como texto livre, sem checar a janela de 24h — pode falhar em silêncio assim que a cadência publicar
**Por quê:** todo nó `Send WhatsApp` da operação (M1-a/M1-b/M2-v1/M3-v1 na
Cadência 12x30, `build-wesales.md` seção 2.6; `MI-0`/`MI-F` na Cadência
Inbound, seção 2.10; `RE-1`/`RE-2` no Reengajamento, seção 2.12; `NS-1`/
`NS-2` na Recuperação de No-show, seção 5.3; a confirmação e os três
lembretes do Pós-agendamento, seção 5, nós 7-10) está especificado como
texto livre, sem checar se
o lead está dentro da **janela de atendimento de 24h** do WhatsApp Business
API. Pesquisado via `WebSearch` (domínios de suporte da HighLevel seguem
bloqueados pelo proxy deste ambiente — achado por citação de página
oficial, não pela página em si): essa janela só abre quando o **cliente**
manda mensagem primeiro, e fecha 24h depois do último contato dele; fora
dela, a API recusa mensagem de texto livre e só aceita **Template**
pré-aprovado pela Meta. Nenhum lead desta operação jamais mandou mensagem de
WhatsApp antes (vêm de Meta Lead Ads e formulário, não de WhatsApp), e a
maioria dos envios da régua sai dias ou semanas depois do anterior (D1,
D10, D30, 90 dias de reengajamento) — então **praticamente todo envio desta
operação cai fora da janela**, o oposto do que o desenho atual assume. Sem
correção, a `Cadência 12x30` publica, o WhatsApp passa a recusar (ou cobrar
taxa extra de conversa, a depender do provedor) cada mensagem automática, e
ninguém percebe — a mesma classe de "estrago silencioso" que motivou o
F-05, aqui no canal inteiro em vez de um caso isolado. Confirmado por
ausência: nenhum documento do projeto (`briefing-sdr.md`,
`build-wesales.md`, `biblioteca-mensagens.md`, `campos-e-tags.md`) menciona
janela de atendimento, Template Meta ou risco de recusa — a régua foi
desenhada como se WhatsApp fosse texto livre sem restrição, que não é o
caso da API oficial que uma integração white-label do GHL usa.
**Como:** o GHL expõe duas peças nativas para isto (`WebSearch`, confiança
média — página de suporte oficial confirmada por citação direta em duas
buscas com termos diferentes, não testada nesta subconta): a ação
**`WhatsApp: Customer Service Window Check`**, que confere se o contato
está dentro da janela, e a ação **`Send WhatsApp`** com modo **Template**
(em vez de "None – Manual Text"), que envia uma mensagem pré-aprovada pela
Meta e funciona dentro **e** fora da janela. Padrão: antes de cada nó de
envio livre já especificado, inserir o `Customer Service Window Check` e
ramificar — dentro da janela, segue para o texto livre já desenhado, sem
mudar nada; fora da janela, desvia para `Send WhatsApp` com o Template
correspondente. Cada um dos 11 textos de `biblioteca-mensagens.md` precisa
de um Template Meta equivalente, submetido pelo dono no Meta Business
Manager (aprovação de até 48h, fora do alcance deste conector) — os merge
fields (`{{contact.first_name}}`, `{{contact.segmento}}`,
`{{user.first_name}}`, `{{location.name}}`) viram variáveis posicionadas do
Template, e o Trigger Link `[Agendar com o closer]` provavelmente vira um
botão CTA de URL do Template em vez de texto inline (a confirmar na tela —
Template tem formatação mais restrita que mensagem livre).
**O que este item NÃO bloqueia, e vale dizer antes que alguém leia como
"não publique nada" (acrescentado em 21/09/2026, ao conferir o item):** a
`Cadência 12x30` são **12 tarefas de ligação** (telefone e ligação por
WhatsApp) e **4 envios de texto** (`M1-a`/`M1-b`, `M2-v1`, `M3-v1`). O que
paga a operação — a fila de ligação do SDR, os contadores, o roteamento por
resultado, a saída limpa — não depende de Template nenhum. Publicar a régua
com os quatro nós de envio **desativados** (ou com o portão já montado, ramo
livre vazio) entrega o motor inteiro hoje e deixa só a mensagem esperando a
Meta.

A ordem que sai daqui, e que nenhum item dizia inteira num lugar só:

| # | Passo | Depende de |
|---|---|---|
| 1 | Número de telefone e canal de WhatsApp na subconta | decisão do dono (pendência antiga do R-14) |
| 2 | Publicar a `Cadência 12x30` **sem os 4 nós de envio**, testar com 1-2 leads | nada além do passo 1 para as tarefas |
| 3 | Promover o estoque de `NOVO LEAD` (G-03) | passo 2 publicado, porque o gatilho é evento e não varre quem já está na etapa |
| 4 | Submeter os Templates à Meta (até 48h) e ligar o portão nos 4 nós | passo 1, e só isso |

Inverter 2 e 3 gasta o evento no vácuo (nota do G-03); esperar o passo 4
para fazer o 2 deixa 47 leads pagos sem ligação por mais 48h sem nenhum
ganho.

**Pronto quando:** todo nó `Send WhatsApp` da operação tem o
`Customer Service Window Check` antes dele e os dois ramos (livre/Template)
especificados; os textos de `biblioteca-mensagens.md` têm Template Meta
aprovado e mapeado.

**Resumo (21/09/2026):** especificado o primeiro pedaço — o motor
principal, Cadência 12x30 (`M1-a`, `M1-b`, `M2-v1`, `M3-v1`), em
`build-wesales.md` (seção 2.6.2, nova) e `IMPLEMENTACAO-WORKFLOWS.md` (nós
`M1.3a`/`M1.3b`/`M2.2`/`M3.2` reescritos com o portão e os dois ramos).
`biblioteca-mensagens.md` ganhou uma tabela nova marcando os quatro textos
como "a submeter no Meta Business Manager" — decisão e execução do dono,
não sai por API. **Escopo desta rodada, decisão e não lacuna esquecida:**
faltam os pontos de envio abaixo para o mesmo tratamento — `MI-0`/`MI-F`
(Cadência Inbound, seção 2.10), `RE-1`/`RE-2` (Reengajamento, seção 2.12),
`NS-1`/`NS-2` (Recuperação de No-show, seção 5.3) e a confirmação mais os
três lembretes do Pós-agendamento (seção 5, nós 7-10, que nem têm texto
versionado em `biblioteca-mensagens.md` ainda — pendência a mais, achada só
ao contar os nós com atenção) — mesmo padrão desta peça, próxima peça deste
mesmo item. Zero campo e zero tag novos, zero escrita no CRM: item de
especificação pura, não depende de `APROVADO.md`. Subconta reconfirmada
nesta execução via `opportunities_search-opportunity`/
`opportunities_get-pipelines`/`locations_get-custom-fields`: mesmas 5
etapas do `FUNIL DE VENDAS`, 46 campos, 50 oportunidades (47 `NOVO LEAD` +
3 `NEGOCIAR`, todas `open`) — sem mudança desde a última rodada; G-03/G-04
seguem aguardando o dono.

**Resumo (22/09/2026, segunda rodada) — pendência de guarda zerada:** os
seis pontos de envio que a peça 1 tinha deixado de fora ganharam o mesmo
tratamento (guarda + os dois ramos) em `build-wesales.md` (seções 2.10,
2.12, 5, 5.3) e `IMPLEMENTACAO-WORKFLOWS.md` (W5, W8, W12, W16): `MI-0`/
`MI-F` (Cadência Inbound), `RE-1`/`RE-2` (Reengajamento 90 dias), `NS-1`/
`NS-2` (Recuperação de No-show) — os seis já tinham texto versionado em
`biblioteca-mensagens.md`, só faltava a guarda — e a confirmação mais os
três lembretes do Pós-agendamento (seção 5, nós 7-10), que não tinham nem
texto: ganharam código e texto novos (`PA-CONF`/`PA-R24`/`PA-R3H`/`PA-R30`)
nesta rodada, porque não dá para montar o ramo Template de uma guarda sem
saber que texto livre ele substitui fora da janela. Achado ao escrever o
texto de `PA-CONF` (herdado, não introduzido por esta rodada): a mensagem
promete "vou te mandar o link aqui mesmo 30 min antes", e nenhum documento
do projeto especifica um merge field ou nó que grave/leia link de reunião
— registrado como limite conhecido em `build-wesales.md`, seção 5, sem
inventar um campo que a tela não tem (a mesma classe de erro que motivou
o achado do `fieldKey`/rótulo de opção em rodadas anteriores). O
Pós-agendamento está **publicado e ativo** (3 inscritos) — a guarda nos
nós 7-10 entrou também na tabela de retoques do `GUIA-MONTAGEM.md`, como
qualquer edição em peça já no ar; os outros três workflows (Cadência
Inbound, Reengajamento, Recuperação de No-show) ainda não existem na tela
ou existem só como rascunho, então a mudança ali é só na especificação que
vai orientar a montagem. Zero campo e zero tag novos, zero escrita no CRM:
item de especificação pura, não depende de `APROVADO.md`. Subconta
reconfirmada nesta execução via `opportunities_search-opportunity`/
`locations_get-custom-fields`: **51 campos** (5 novos desde a última
leitura — `Hora da conexão`, `Toques na semana`, `Checkpoint — Tentativa
nº`, `Checkpoint — Data de retorno` e `Hora do retorno`, todos já
especificados em `campos-e-tags.md`, C-25 a C-28 e S-01 — sinal de que a
montagem manual na tela avançou desde 21/09/2026, fora desta sessão), 50
oportunidades (47 `NOVO LEAD` + 3 `NEGOCIAR`, todas `open`, sem mudança) —
G-03/G-04 seguem aguardando o dono. **O que falta para fechar o G-05 por
inteiro:** a submissão dos Templates ao Meta Business Manager (ação do
dono, até 48h) e a montagem manual de cada guarda na tela quando cada
workflow for construído/editado — nenhuma das duas sai por API.

### G-06 · A guarda de janela do G-05 nunca chegou à `Qualificação por IA no WhatsApp` — o ponto de envio mais exposto de todos ficou sem ela — **FEITO em 22/09/2026**
**Por quê:** o G-05 fechou a guarda de janela de 24h em todo `Send WhatsApp`
de texto livre **catalogado em `biblioteca-mensagens.md`** — mas os envios
do workflow `Qualificação por IA no WhatsApp` (`build-wesales.md`, seção 6)
nunca entraram naquele documento. O R-04, que criou a biblioteca, fechou em
18/09/2026, dois dias antes de o G-05 sequer existir (21/09/2026); a
varredura que fechou o G-05 conferiu texto por texto da tabela "Templates
ativos" e nunca teve como olhar para um workflow ausente dela. Achado ao
perguntar, nesta rodada, "todo `Send WhatsApp` do documento tem guarda?" em
vez de "todo código da biblioteca tem guarda?" — `grep -n "Send WhatsApp"
build-wesales.md` aponta a linha 3909, dentro da seção 6, sem nenhuma
guarda por perto. É o ponto mais exposto da operação, não um caso a mais:
a entrada deste workflow (seção 2.7) dispara pelo resultado de uma
**ligação** sem resposta, não por uma mensagem do lead — o WhatsApp quase
nunca trocou palavra com ele antes daqui, e o Caminho A recomendado
(`Conversation AI`) é pior que os outros porque gera o texto **no momento
da conversa**: não dá para pré-aprovar como Template Meta um conteúdo que
não existe até a hora do envio, a única saída de fábrica que a Meta aceita
fora da janela.
**Como:** guarda de entrada (`WhatsApp: Customer Service Window Check`)
antes do Caminho A: dentro da janela, segue direto para a `Conversation AI`
já especificada; fora dela, manda um convite fixo e curto (`QI-1`, novo,
`biblioteca-mensagens.md`) pedindo para o lead responder ali — a resposta
reabre a janela (é o cliente escrevendo primeiro) e só então a IA assume.
Sem resposta em 24h, o workflow encerra sozinho sem tocar na Cadência
12x30 principal, que continua ligando por fora. Detalhe nó a nó em
`build-wesales.md`, seção 6.0, e em `IMPLEMENTACAO-WORKFLOWS.md`, W10.
**Pronto quando (cumprido):** todo envio de WhatsApp deste workflow —
Caminho A e Caminho B — tem guarda de janela, do mesmo jeito que o G-05 já
garante para o resto da operação.

**Resumo (22/09/2026):** fechado o Caminho A (o recomendado pelo próprio
documento): guarda especificada em `build-wesales.md` (seção 6.0, nova) e
`IMPLEMENTACAO-WORKFLOWS.md` (W10), template novo `QI-1` escrito e
versionado em `biblioteca-mensagens.md` — a única mensagem da biblioteca
que não é "equivalente de um texto livre já em uso", porque o texto livre
correspondente (o que a IA diria dentro da janela) não existe até a
conversa acontecer; registrado assim no próprio documento para o próximo
leitor não estranhar a assimetria. **Escopo desta rodada, pendência
explícita e não lacuna esquecida:** o Caminho B (8 blocos `Send WhatsApp`
manuais) tem o mesmo problema em cada uma das 8 perguntas, não só na
primeira, e guardar as 8 exigiria 8 Templates novos ou reestruturar o
caminho para só avançar depois de resposta de verdade — nenhuma das duas
desenhada agora; quem montar isto na tela deve montar só o Caminho A, que
já está seguro e é o recomendado. Zero campo e zero tag novos — a
proposta de marcar `QI-1` como `toque` (F-04) foi avaliada e descartada
pelo mesmo raciocínio que já deferiu Cadência Inbound/Reengajamento/
Recuperação de No-show naquela seção: nenhum chega perto do teto sozinho.
Zero escrita no CRM: item de especificação pura, não depende de
`APROVADO.md`. Subconta reconfirmada nesta execução via
`locations_get-custom-fields`/`opportunities_search-opportunity`: 51
campos, 50 oportunidades (47 `NOVO LEAD` + 3 `NEGOCIAR`, todas `open`),
sem mudança desde 22/09/2026 (primeira peça do G-05) — G-03/G-04 seguem
aguardando o dono. Conferido também nesta rodada, premissa técnica
reaberta e ainda sem novidade: o toolkit HighLevel via Composio (cogitado
desde `briefing-sdr.md`, "Estado do acesso", como rota alternativa para
criar campo/calendário por API) segue **sem conta conectada**
(`COMPOSIO_MANAGE_CONNECTIONS`, ação `list`, 0 contas ativas) — mesma
conclusão de 18/09/2026, conectar continua exigindo OAuth que só o dono
autoriza.

**Resumo (22/09/2026, segunda rodada) — G-06 fechado por inteiro:** fechado
o Caminho B, a pendência que a peça 1 tinha deixado explícita. Das duas
saídas que o próprio item já cogitava, a escolhida foi reestruturar o
caminho, não multiplicar Template: cada um dos 8 blocos `Send WhatsApp` só
avança para a pergunta seguinte quando o lead **responde de verdade** (a
resposta é o que reabre a janela de 24h, não o nosso envio) — sem resposta
no prazo, o bloco grava uma nota e encerra o workflow, no lugar de "pular
para a pergunta seguinte" (o desenho original), que mandaria texto livre
com a janela já fechada. Mesmo raciocínio da peça 1, generalizado: uma
guarda na entrada garante a **primeira** mensagem dentro da janela, não as
sete seguintes — cada uma delas só herda a garantia da anterior ter
recebido resposta. Perder a resposta agora significa parar de perguntar em
vez de insistir sem garantia, o mesmo "lado barato de errar" que o R-18 já
tinha registrado para outro portão do projeto — o lead segue coberto pela
Cadência 12x30 (ligação), que não passa por este workflow. Detalhe nó a nó
em `build-wesales.md`, seção 6 ("B — Sem Conversation AI"), e
`IMPLEMENTACAO-WORKFLOWS.md`, W10. Zero campo e zero tag novos, zero
escrita no CRM: item de especificação pura, não depende de `APROVADO.md`.
Subconta reconfirmada nesta execução via `opportunities_search-opportunity`/
`locations_get-custom-fields`/`opportunities_get-pipelines`: mesmas 5
etapas do `FUNIL DE VENDAS`, 51 campos, 50 oportunidades (47 `NOVO LEAD` +
3 `NEGOCIAR`, uma agora com `status = lost` — o contato de teste do
checklist da seção 10, R-18 — sem mudança de volume real) — G-03/G-04
seguem aguardando o dono.

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

### R-14 · Auditoria de compliance — especificação fechada em 22/09/2026, execução aguarda mensagem real
**Por quê:** `nao-perturbe` e DND são a linha entre prospecção e perseguição.
Precisa ser verificável, não confiável.
**Como:** rotina que confere se algum contato com DND recebeu mensagem, e se
algum envio saiu fora da janela.
**Pronto quando:** existe relatório que prova que ninguém foi incomodado
indevidamente.

**Resumo (22/09/2026):** único item numerado do roadmap inteiro, fora dos
quatro que aguardam decisão do dono (G-03/G-04/F-09/F-10), que continuava
com um "Como" de três linhas e zero nó desenhado — todos os outros já
tinham especificação nó a nó em `build-wesales.md` mesmo os que ainda
esperam volume ou decisão. A releitura do "por quê estamos esperando"
(mandato do fim desta seção) achou que a espera valia só para a
**execução**, não para o **desenho**: dava para especificar agora, do
mesmo jeito que o G-05 especificou Template antes da aprovação da Meta.

A metade "janela de envio" do "Como" já estava coberta sem item próprio:
toda seção de `build-wesales.md` que manda mensagem para o lead já declara
`Janela de envio` na própria tabela de configuração do workflow (08:30 às
18:30, segunda a sexta, ou "sem janela" com justificativa explícita para
aviso interno) — `grep -c "Janela de envio" build-wesales.md` retorna 21
ocorrências, uma por workflow/seção (algumas seções têm mais de uma tabela
de configuração), nenhuma pendência nova. Provar que o
Send Window foi de fato ligado na tela (não só documentado) é montagem,
não desenho — mesmo tipo de verificação manual que o resto do
`GUIA-MONTAGEM.md` já cobre, sem precisar de item próprio.

A metade que faltava de verdade é a auditoria DND ↔ tag `nao-perturbe`.
Achado ao ler `build-wesales.md` (linha 4160) antes de desenhar: os dois
mecanismos que hoje protegem o lead já são nativos e já **impedem** o
envio — `Set Contact DND` bloqueia todo canal na hora que é ligado, e o
Send Window bloqueia o disparo fora de horário no nível do workflow. O
"Pronto quando" não pede um terceiro mecanismo de bloqueio, pede **prova**:
achar o nó que aplicou a tag sem acionar o DND nativo (ou o inverso) — os
dois nascem juntos em quatro lugares diferentes do documento (2.9.5, seção
4 ramo `Não ligar`, seção 6 nó 3, opt-out por palavra-chave do R-17), e
divergência entre eles é sintoma de nó quebrado, mesma classe de "estrago
silencioso" que motivou o F-05.

Pesquisado antes de desenhar (`WebSearch`, `help.gohighlevel.com`/
`consultevo.com`/`growthable.io`, confiança média — página oficial citada
em buscas com termos diferentes, proxy deste ambiente bloqueia leitura
direta, mesmo padrão de confiança já usado no G-05/F-05): Smart List do
GHL tem filtro nativo por canal de DND (`Calls & Voicemails DND`,
`WhatsApp DND`, entre outros), com opção Enabled/Disabled — o mesmo tipo de
filtro booleano que já sustenta as seis listas de saúde do F-05. Decide o
desenho: **duas Smart Lists**, não um workflow novo — comparar duas
condições diferentes entre contatos é o mesmo limite de "workflow não
compara contagem" que o F-05/R-11 já bateram (`APRENDIZADOS-CRM.md`,
entrada do `Scheduler`/Custom Metrics).

Duas listas novas, especificadas em `build-wesales.md`, seção 8 (8.26,
8.27):

| Lista | Filtro | O que denuncia |
|---|---|---|
| `Auditoria — tag sem DND nativo` | tag `nao-perturbe` presente **E** `Calls & Voicemails DND` = Disabled **E** `WhatsApp DND` = Disabled | O caso perigoso: a marca interna existe, mas o bloqueio de plataforma que de fato impede o próximo envio não está ligado — se algum nó de mensagem ainda não alinhado ignorar a tag, a mensagem sai |
| `Auditoria — DND sem tag` | (`Calls & Voicemails DND` = Enabled **OU** `WhatsApp DND` = Enabled) **E** tag `nao-perturbe` ausente | O caso menos perigoso (a prevenção nativa já bloqueia), mas aponta um caminho que ligou DND sem passar pelo registro do projeto — nó não documentado ou ação manual na tela |

Zero campo novo, zero tag nova — reaproveita `nao-perturbe` (T-06,
`campos-e-tags.md`) e os filtros nativos de DND. Nome exato dos filtros a
confirmar na tela (a documentação consultada está em inglês; a tela desta
subconta é em português — mesma ressalva já registrada para outros
filtros nativos do projeto, F-10/seção 8.25).

As duas listas entram como referência numa seção nova "Compliance" do
`Painel do Gestor — Pré-vendas` (R-15, `build-wesales.md` seção 2.17),
mesmo padrão de fallback que 8.6/8.16/8.25 já usam: **se** o plano tiver
Custom Metrics e o Formula Editor aceitar combinar "contagem de tag" com
um filtro de DND — não confirmado, os relatos de mercado descrevem a
métrica de contagem por tag/pipeline/owner/metric-level (mesmo achado já
registrado na "Conferência da peça 2" do F-06), sem citar DND —, as duas
viram widget numérico; senão, as duas Smart Lists sozinhas já cumprem o
"Pronto quando" (zero linha = nada a provar) sem depender de plano pago,
mesmo raciocínio do F-10.

**Por que não fecha ainda:** as duas listas só têm o que auditar depois
que a `Cadência 12x30` publicar e o primeiro `nao-perturbe`/DND real
acontecer. Reconfirmado nesta rodada via `conversations_search-conversation`
(50 conversas, `total` sem mudança): as 4 conversas outbound da subconta
continuam sendo DMs pessoais de Instagram — zero mensagem de cadência
automática enviada, zero DND real aplicado ainda. Diferente de antes: a
partir de agora existe o que montar assim que o volume chegar, não mais
um "Como" de três linhas sem nó nenhum. Zero escrita no CRM, zero campo e
zero tag novos — item de especificação pura, não depende de `APROVADO.md`.
Subconta reconfirmada nesta execução via `opportunities_search-opportunity`/
`locations_get-custom-fields`: mesmas 5 etapas do `FUNIL DE VENDAS`, 51
campos, 50 oportunidades (47 `NOVO LEAD` + 2 `NEGOCIAR` + 1 `lost`, sem
mudança) — G-03/G-04/F-09/F-10 seguem aguardando o dono.

**Pronto quando:** as duas listas existirem na tela e, quando a operação
já estiver mandando mensagem de verdade, `Auditoria — tag sem DND nativo`
estiver **sempre vazia** — divergência ali é bug a corrigir na hora, não
estatística a monitorar.

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

### R-17 · Resposta de opt-out tratada como sinal quente — **FEITO em 21/09/2026**
**Por quê:** lacuna nova, achada nesta rodada ao ler o 2.9.3
(`build-wesales.md`) com atenção em vez de só conferir nome de etapa. O
workflow "Interceptação de Sinal — Resposta" (F-01, seção 2.9.3) dispara em
**toda** resposta de WhatsApp, sem olhar o conteúdo — um lead que responde
"pare, não me manda mais mensagem" recebe o mesmo tratamento de quem
responde "sim, tenho interesse": `Prioridade` = 5, tag `fila-quente`,
tarefa `[CADENCIA] ... ligar agora`. O ramo `Não ligar` do Pós-ligação
(seção 4, já tratado como não-negociável neste documento) só existe para
**ligação de telefone** classificada pelo SDR — uma resposta de texto nunca
passa por lá. Sem correção, o pedido mais explícito que um lead pode fazer
("me deixa em paz") virava, na prática, uma tarefa dizendo ao SDR para
ligar imediatamente. **Não é hipótese de tela apagada:** `GUIA-MONTAGEM.md`
("Estado da montagem em 19/09/2026, mais tarde") registra `Interceptação de
Sinal — Resposta` como **Publicado**, 1 inscrito — o workflow com o defeito
já está ativo na subconta, mesmo com a `Cadência 12x30` (motor principal)
ainda em rascunho. A exposição de hoje é baixa porque pouco envio automático
está rodando ainda, mas cresce sozinha assim que a 12x30 publicar — por
isso o item entrou nesta rodada em vez de esperar a vez do bloco 6.
**Como:** workflow novo `Opt-out por Palavra-chave` (`build-wesales.md`,
seção 2.9.5) — gatilho `Customer Replied`/WhatsApp filtrado por frases de
opt-out, aplica `nao-perturbe` + DND nativo + remove de todas as réguas
automáticas (a lista mais longa do documento) + fecha a oportunidade só se
ainda estiver em `CONECTAR`/`open` (fora disso, avisa o dono do contato em
vez de decidir sozinho). O 2.9.3 ganhou o filtro espelhado (`Doesn't
Contain` as mesmas frases) para os dois nunca dispararem ao mesmo tempo
para a mesma mensagem.
**Pronto quando:** um lead que responde uma frase de opt-out no WhatsApp
sai de toda cadência com DND ligado no mesmo minuto, sem nunca gerar a
tarefa "ligar agora" que o 2.9.3 geraria antes deste item.

**Resumo:** pesquisado antes de desenhar (Reev/Meetime/Outreach/Salesloft
não precisam de detecção por palavra-chave em WhatsApp — o canal deles é
e-mail com unsubscribe padronizado ou SMS com "STOP" reservado por lei nos
EUA; nenhum dos quatro roda ligação por WhatsApp, o que torna esta
combinação de gatilho global + filtro cruzado uma peça sem receita pronta
para copiar). Zero campo e zero tag novos — reaproveita `nao-perturbe`
(T-06, já existente) e o DND nativo. **Limite documentado, não escondido:**
não cobre a janela de corrida com uma mensagem que já estava saindo no
mesmo instante por outro workflow (ex.: a corrente de nós do Caminho B da
Qualificação por IA, seção 6, que não olha o conteúdo da resposta antes de
mandar a próxima pergunta — o Caminho A já tem uma instrução de prompt para
a mesma janela, o B não tem nada equivalente ainda; registrado como lacuna
pequena, sem volume que justifique rodada própria agora). Falta só a
criação manual do workflow novo e do filtro cruzado no 2.9.3 — nenhum dos
dois sai por API; subconta reconfirmada nesta execução via
`opportunities_get-pipelines`/`locations_get-custom-fields`: 46 campos, as
mesmas 5 etapas do `FUNIL DE VENDAS`, 47 oportunidades em `NOVO LEAD` (G-03
segue aguardando o dono, sem mudança).

### R-18 · L-08 fechada — desqualificação instantânea no Pós-ligação, antes de poluir a agenda do closer — **FEITO em 21/09/2026**
**Por quê:** `briefing-sdr.md` registrava a L-08 desde 18/09/2026 ("etapa
`Conectado` não tem caminho para desqualificação na hora") como lacuna
opcional, sem nunca virar item rastreado do roadmap — diferente de L-01,
L-04, L-05, L-07 e L-09, que já tinham item próprio. Achada de novo, por um
caminho diferente, ao reconferir a peça 5 do F-05 (`AGENDAR` sem fechar o
loop, seção 2.23): aquele monitor cita a L-08 como precaução, mas nunca a
resolve — só avisa que alguém ficou parado, não evita a tarefa nascer
errada. O ramo `Atendeu` do Pós-ligação (`build-wesales.md`, seção 4) move
**toda** ligação atendida para `AGENDAR` e cria `[CONECTADO] Qualificar e
agendar`, mesmo quando a própria conversa já mostrou que não há fit — o SDR
então força uma reunião sem fit (polui a agenda do closer) ou desfaz na mão
por fora do sistema, e nenhum dos dois caminhos é registrado como perda em
lugar nenhum: a nota de qualificação (seção 9) nunca vê esse lead, e o funil
do R-03 mostra "conectou" sem nunca mostrar "descartado". O workflow já está
publicado e rodando (`IMPLEMENTACAO-WORKFLOWS.md`, W4, 24 execuções) — não é
hipótese de tela apagada, é o caminho que toda ligação atendida passa hoje.
**Como:** nova opção `Desqualificado` em `Resultado da tentativa` (C-02,
`campos-e-tags.md`) e um 7º ramo no `If/Else múltiplo` do Pós-ligação
(`build-wesales.md`, seção 4; `IMPLEMENTACAO-WORKFLOWS.md`, W4): conta como
conexão real (mesmos contadores do ramo `Atendeu`), mas sai por `status`
(`abandoned` se `Motivo da desqualificação` = `Timing errado`, `lost` para
qualquer outro motivo — o mesmo critério que o Loop do closer, seção 5.1, já
usa para o veredito pós-reunião) sem passar por `AGENDAR` e sem criar tarefa
de agendamento.
**Pronto quando:** um "atendeu, mas claramente não serve" vira `status`
`lost`/`abandoned` na hora, sem gerar `[CONECTADO] Qualificar e agendar` e
sem abrir horário na agenda do closer.

**Resumo:** pesquisado antes de desenhar — nenhuma das quatro plataformas do
enunciado (Reev, Meetime, Outreach, Salesloft) separa "atendeu e desqualificou
na ligação" de "atendeu e vai agendar" como resultado de primeira classe da
tentativa; todas tratam isso como nota livre dentro de um CRM genérico,
perdendo a chance de o dado virar filtro/lista sozinho. Reaproveitado de
propósito o campo `Motivo da desqualificação` (C-16), já existente para o
F-03 (veredito do closer pós-reunião) — sem duplicar campo, e sem colisão de
uso: quem vira `Desqualificado` no Pós-ligação nunca chega ao Loop do closer
na mesma passagem pela cadência, e vice-versa. `script-de-ligacao.md` ganhou
a seção 3a, ensinando o SDR a reconhecer o momento (sem confundir com
`Pediu retorno`/`Timing errado`, que continua reciclável) e a não forçar a
ponte da seção 4 quando não há fit. Zero campo novo, zero tag nova — só uma
opção nova num campo já existente e um ramo novo num workflow já publicado;
falta a criação manual dos dois na tela (opção de picklist e ramo de
workflow não saem por API). Detalhe completo em `build-wesales.md` (seção
4), `IMPLEMENTACAO-WORKFLOWS.md` (W4) e `GUIA-MONTAGEM.md` (tabela de
retoques). Subconta reconfirmada nesta execução via
`opportunities_get-pipelines`/`opportunities_search-opportunity`/
`locations_get-custom-fields`/`conversations_search-conversation`: mesmas 5
etapas do `FUNIL DE VENDAS`, 46 campos, 50 oportunidades (47 `NOVO LEAD` + 3
`NEGOCIAR`, sem mudança desde a última rodada — G-03/G-04 seguem aguardando
o dono), e nenhuma mensagem automática de cadência ainda saiu de verdade
(as únicas conversas outbound reais na subconta são DMs pessoais de
Instagram, não tráfego da máquina) — confirma que R-14 continua
corretamente bloqueada por falta de volume de mensagem, sem mudança de
estado a registrar ali.

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

### F-05 · Monitor de saúde da operação — FEITO em 21/09/2026 (seis peças: lead esquecido em `NOVO LEAD`, `fila-tel`/`fila-wa` presa, `CONECTAR` sem avanço, `nao-perturbe` ainda em workflow ativo, `AGENDAR` sem fechar o loop, retorno vencido sem reclassificação)
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

**Resumo (21/09/2026, primeira peça):** o gatilho para tirar este item da
espera não foi volume — foi o próprio G-03 acontecer. G-03 só existe porque
uma sessão automática notou, olhando o número na mão, que 47 oportunidades
pagas estavam paradas em `NOVO LEAD` há mais de 24h; nada na máquina avisou
sozinho. Isso é exatamente o "estrago silencioso" que motiva o F-05, e é
independente de qual opção o dono escolher para o G-03 — nenhuma delas
impede a próxima estagnação. Workflow "Lead Esquecido em NOVO LEAD"
especificado em `build-wesales.md` (seção 2.20): mesmo padrão de relógio
por evento que já validou o R-02 (Alerta de Speed-to-lead) e o SLA do
Closer (seção 5.4) — `Wait` de 24h desde a entrada em `NOVO LEAD`, portão
confere se a oportunidade ainda está lá e `open`, tag `novo-lead-estagnado`
(T-16, `campos-e-tags.md`) + aviso ao gestor. Lista `Saúde — NOVO LEAD
Estagnado` criada (seção 8.20). Achado ao desenhar a limpeza: o Mestre de
saída (seção 3) só limpa tag quando a oportunidade **sai** de
`CONECTAR`/`open` — a transição `NOVO LEAD` → `CONECTAR` (onde este alerta
se resolve) cai no ramo de no-op dele e nunca alcança a lista de remoção de
tags; corrigido com um nó 0 novo, incondicional, antes do portão do Mestre
de saída.

**Escopo desta rodada, decisão e não lacuna esquecida:** das seis
invariantes do "Como"/das duas adições de 18/09, só a de `NOVO LEAD`
(que nem estava na lista original — entrou por conta do G-03) ganhou
workflow nesta peça, por ser a única com evidência de produção real e a
mais simples de desenhar com confiança. Achado que evita retrabalho
futuro, e que exige cuidado para não confundir duas invariantes parecidas:
"tarefa vencida sem resultado" **já não é risco** como está escrita — o nó
10b do bloco padrão (seção 2.4) já classifica sozinho `Resultado da
tentativa = Não atendeu` quando o prazo do dia estoura sem o SDR agir, e a
lista 8.5 já mostra esse volume. **Diferente** de `fila-tel`/`fila-wa`
presente há mais de 24h, que continua um risco de verdade: se a tag ainda
está lá depois de 24h, é o nó 9 (que remove a tag sempre, todo dia) que não
rodou — sinal de workflow travado, não de SDR lento. As quatro invariantes
restantes (`fila-tel`/`fila-wa` há 24h, `CONECTAR` sem tentativa há 7 dias,
`nao-perturbe` em workflow ativo, `Conectado`/`Retorno agendado` vencidos)
seguem de pé e pedem mais desenho (a última, por exemplo, depende de
"esperar até uma data dinâmica" — não testado neste conector) — próxima
peça deste mesmo item, não item novo.
Falta só a criação manual do workflow e da tag na tela — nenhum dos dois
sai por API; subconta reconfirmada nesta execução via
`opportunities_get-pipelines`/`opportunities_search-opportunity`/
`locations_get-custom-fields`: mesmas 5 etapas do `FUNIL DE VENDAS`, 46
campos, 50 oportunidades (47 `NOVO LEAD` + 3 `NEGOCIAR`) — sem mudança
desde a última rodada, G-03 segue aguardando o dono.

**Resumo (21/09/2026, peça 2 — mesma rodada da peça 1):** a próxima
invariante da lista de quatro, `fila-tel`/`fila-wa` presente depois do fim
do dia em que foi aplicada — a única das quatro que mede saúde do **motor**
(instância de workflow perdida), não decisão humana atrasada. Workflow
"Fila Travada" especificado em `build-wesales.md` (seção 2.21), tag
`fila-travada` (T-17, `campos-e-tags.md`), lista `Saúde — Fila Travada`
criada (seção 8.21). **Achado ao desenhar, que mudou o mecanismo do "Como"
original:** a primeira versão copiava o relógio da peça 1 (`Wait` 24h a
partir do gatilho) e tinha um falso positivo real — a tabela 2.5 encaixa
tentativas a menos de 24h uma da outra (T1 D1 10:30 → T3 D2 09:20, 22h50 de
distância), então o relógio de 24h da T1 podia checar bem no meio da janela
em que a T3 já tinha reaplicado a mesma tag, de forma legítima e recente, e
confundir fila nova com fila travada. Corrigido ancorando a espera num
horário fixo do dia (19:00, 30 min depois do prazo das 18:30 que o nó 9 do
bloco padrão já respeita) em vez de um delta relativo ao gatilho — elimina
a janela de sobreposição sem precisar de um campo novo para guardar "qual
tentativa disparou este alerta" (a alternativa cogitada, copiar `Tentativa
nº` para um campo próprio no gatilho, esbarraria no mesmo "contador com
dois donos" que a seção 2.4 já documenta, porque duas instâncias deste
workflow disparadas por tentativas próximas sobrescreveriam o campo uma da
outra). Limpeza dupla, mesmo padrão do R-02: o nó 0 do próprio workflow
(preventivo, roda a cada nova tentativa) e o nó 4 do Mestre de saída
(seção 3, atualizado nesta rodada — aqui a tag entrou direto na lista
existente, sem precisar do nó 0 incondicional que a peça 1 exigiu, porque
o alerta de fila travada se resolve numa saída de cadência real, que o nó 4
já alcança). Limite documentado, não escondido: se o gestor remover
`fila-tel`/`fila-wa` na mão sem o lead nunca gerar tentativa nova nem sair
de cadência, `fila-travada` fica presa para sempre sem afetar mais nada —
cenário que a peça 3 (`CONECTAR` sem avanço) é quem pega de verdade
(cadência morta, não só uma tentativa travada). Zero
escrita no CRM: tag nasce `[ ]` em `APROVADO.md`, mesma regra da T-16.
Subconta reconfirmada nesta execução, sem mudança: mesmas 5 etapas do
`FUNIL DE VENDAS`, 46 campos, 50 oportunidades — G-03 segue aguardando o
dono.

**Resumo (21/09/2026, peça 3 — mesma rodada das peças 1 e 2):** a invariante
que a própria peça 2 já apontava como sua vizinha natural (seção "Caso não
coberto por nenhum dos dois" do `build-wesales.md`) — `CONECTAR`/`open` sem
nenhuma tentativa nova por tempo demais, o sintoma de uma cadência **morta**,
não só uma tentativa travada. **Achado que corrigiu o próprio enunciado do
roadmap antes de publicar:** o "7 dias" original da lista de invariantes
falharia contra a régua real — a tabela 2.5 tem um degrau de **10 dias
corridos** entre T10 (D20) e T11 (D30), então um alarme aos 7 dias soaria
para todo lead saudável passando por esse intervalo, o exato oposto de
"cadência morta". Corrigido para 14 dias (acima do maior degrau real, com
folga para o empurrão de dia útil que a seção 2.5 já documenta). **Segundo
achado, de mecanismo:** o gatilho não é `Opportunity Stage Changed →
CONECTAR` (a tradução mecânica da peça 1) — o Reengajamento 90 dias (seção
2.12) reescreve a oportunidade para a **mesma** etapa em que ela já estava
(12 tentativas esgotadas nunca move de `CONECTAR`, só muda `status`), e não
há fonte confirmando se o GHL dispara o evento de mudança de etapa quando o
valor escrito é igual ao valor anterior — apostar nisso arriscava deixar
todo lead reativado sem monitor. Resolvido com um gatilho pesquisado via
`WebSearch` (nível de confiança médio, documentação oficial confirma mas não
testado nesta subconta): **Contact Changed**, filtrando por Custom Field
`Tentativa nº` **igual a** `0` — o valor que os três pontos de início de
rodada (Cadência 12x30, Cadência Inbound, Reengajamento) já escrevem, sem
exceção. Workflow "Cadência Sem Avanço" especificado em `build-wesales.md`
(seção 2.22): checkpoint de `Tentativa nº` num campo novo (C-27,
`campos-e-tags.md`), laço de 14 em 14 dias comparando o valor atual contra o
checkpoint (mesmo padrão de laço já usado nos nós 2.5b/2.5d da seção 2.4),
tag `conectar-estagnado` (T-18) na régua realmente parada. Limite
documentado, não escondido: o handoff do fim da Cadência Inbound também
zera `Tentativa nº`, então um lead inbound sem resposta abre uma segunda
instância deste monitor — na pior hipótese, a instância mais antiga sai em
silêncio achando "avançou" (leu um checkpoint que na verdade a instância
mais nova escreveu), mas a mais nova continua o laço corretamente a partir
do seu próprio início; nunca os dois saem ao mesmo tempo sem avisar. Falta
só a criação manual do workflow, do campo e da tag na tela — nenhum sai por
API; subconta reconfirmada nesta execução via
`opportunities_get-pipelines`/`locations_get-custom-fields`/
`opportunities_search-opportunity`: mesmas 5 etapas do `FUNIL DE VENDAS`, 46
campos, 50 oportunidades (47 `NOVO LEAD` + 3 `NEGOCIAR`, status `open` em
todas) — sem mudança desde a última rodada, G-03/G-04 seguem aguardando o
dono.

**Resumo (21/09/2026, peça 4 — mesma rodada das peças 1 a 3):** a candidata
que a própria peça 3 já apontava. Pesquisado antes de desenhar o monitor que
o "Como" original descrevia ("rotina que confere invariantes e denuncia
violação"): o GHL não tem filtro nativo de Smart List "contato ativo em
**qualquer** workflow", só "ativo **neste** workflow específico" (pedido em
aberto na base de ideias da HighLevel, mesma classe de limite já documentada
para R-10/R-11) — um monitor de verdade precisaria de um filtro por
workflow, exatamente a lista manual que `APRENDIZADOS-CRM.md` já tinha
flagrado vazando quatro vezes (`build-wesales.md`: seção 3, seção 4 ramo
`Não ligar`, seção 5 nó 3, seção 2.9.5) — **detectar o vazamento com a
mesma peça que vaza não fecha o buraco, documenta ele**. **Achado que trocou
detecção por prevenção:** pesquisada uma ação nativa melhor —
**`Remove Workflows`**, com a opção **`All Except Current Workflow`**
(pesquisado via `WebSearch`, confiança média — documentação oficial da
HighLevel bloqueada pelo proxy deste ambiente, confirmado por três fontes de
terceiros independentes) — que tira o contato de **toda** régua ativa,
existente ou futura, sem precisar nomear nenhuma. Substituiu a lista manual
nos quatro lugares que a tinham: o vazamento que a peça 4 do "Como" original
foi desenhada para **detectar** deixa de poder **acontecer**. Cuidado
documentado: a opção certa é sempre `All Except Current Workflow`, nunca
`All Workflows` — as quatro peças têm nó depois na própria régua, e
`All Workflows` cortaria a própria execução no meio (mesmo efeito que a
seção 5.4 do `build-wesales.md` já documenta para `Remove from Workflow`
cancelando um `Wait` pendente). Zero campo, zero tag, zero escrita no CRM:
documentação pura, não depende de `APROVADO.md`. Três dos quatro lugares
(`Mestre de saída`, ramo `Não ligar` do `Pós-ligação`, nó 3 do
`Pós-agendamento`) já estão publicados e ativos na subconta — a troca virou
retoque de tela "dá para fazer hoje" em `GUIA-MONTAGEM.md`, não mais
bloqueado por workflow que ainda não existe. Detalhe completo:
`build-wesales.md` (seções 3, 4, 5 e 2.9.5), `IMPLEMENTACAO-WORKFLOWS.md`
(W3/W4/W5/W14), `GUIA-MONTAGEM.md` (retoques) e `APRENDIZADOS-CRM.md`
(lição original marcada como superada, não apagada).

**Escopo depois das quatro peças daquela rodada:** das seis invariantes
originais do "Como" (mais as duas adições de 18/09), três tinham workflow
(`NOVO LEAD` estagnado, `fila-tel`/`fila-wa` presa e `CONECTAR` sem avanço),
uma foi descartada por já estar coberta (tarefa vencida sem resultado) e a
de `nao-perturbe` em workflow ativo foi resolvida na raiz em vez de por
monitor (acima). Restava uma: `Conectado`/`Retorno agendado` vencidos —
seguia dependendo de "esperar até uma data dinâmica", não testado neste
conector.

**Resumo (21/09/2026, peças 5 e 6 — mesmo dia, sessão automática seguinte
— F-05 fechado):** o próprio roadmap (nota no fim deste arquivo) mandava
reconferir se essa dependência ainda valia antes de procurar lacuna nova.
Pesquisado via `WebSearch` (documentação oficial da HighLevel segue
bloqueada pelo proxy deste ambiente): o nó `Wait` do GHL tem uma opção
**Dynamic** que lê a data de um custom field em tempo de execução — achado
com confiança médio-alta (a mesma citação do artigo oficial apareceu
palavra por palavra em duas buscas independentes, reforçada por um
changelog da própria HighLevel anunciando a funcionalidade). A dependência
caiu, e as duas invariantes que faltavam ganharam workflow:

- **Peça 5 — `AGENDAR` sem fechar o loop em 24h** (`Conectado` no plano
  original): workflow "AGENDAR Estagnado" (`build-wesales.md`, seção 2.23),
  mesmo padrão de relógio por evento da peça 1 — gatilho `Opportunity Stage
  Changed → AGENDAR`, `Wait` de 24h, portão, tag `agendar-estagnado` (T-19)
  e aviso ao gestor. Limpa pelo nó 0, incondicional, do Mestre de saída —
  por precaução contra a lacuna L-08 (`briefing-sdr.md`, "`AGENDAR` não tem
  caminho formal de desqualificação"), não porque o caminho normal precise.
- **Peça 6 — retorno prometido e vencido sem reclassificação** (`Retorno
  agendado` no plano original): workflow "Retorno Vencido" (`build-wesales.md`,
  seção 2.24) — o que dependia da data dinâmica. Gatilho `Contact Changed`
  filtrando `Data de retorno` alterado (o mesmo tipo de filtro que o
  Pós-ligação já usa em produção, 24 execuções confirmadas —
  `APRENDIZADOS-CRM.md`), checkpoint do valor no instante do gatilho (mesmo
  padrão da peça 3, campo novo `Checkpoint — Data de retorno`, C-28), `Wait`
  Dynamic até esse valor às 19:00, dois portões (a promessa não foi renovada
  E ainda está pendente) antes de marcar `retorno-vencido` (T-20). **Achado
  ao desenhar a limpeza, o mais importante das duas peças:** o caminho mais
  comum de recuperação (o SDR liga de novo e reclassifica) não muda etapa
  nem `status` na maioria dos resultados possíveis — o Mestre de saída
  nunca dispara nesse caminho. Resolvido com um nó novo, incondicional, no
  próprio Pós-ligação (nó 3c, mesmo raciocínio já usado para `fila-quente`
  no nó 3b daquele workflow), com o nó 4 do Mestre de saída como rede de
  segurança, não como limpeza principal.

**F-05 fechado como bloco:** as seis invariantes originais do "Como" (mais
a de `NOVO LEAD`, achada via G-03) têm tratamento agora — três por
detecção com relógio (peças 1, 2, 3), uma por prevenção (peça 4), duas por
detecção com checkpoint (peças 5, 6). Nenhuma pendência restante dentro do
item. Zero escrita no CRM nesta rodada: as duas tags (T-19/T-20) e o campo
novo (C-28) nascem propostos, não criados — mesma regra de todo `[ ]` desde
o incidente da T-15. Subconta reconfirmada: mesmas 5 etapas do `FUNIL DE
VENDAS`, 46 campos, 50 oportunidades — G-03/G-04 seguem aguardando o dono,
sem mudança.

### F-06 · Qualidade da conexão, não a contagem — **FEITO em 22/09/2026, duas peças, mesmo dia** (com duas conferências, também no dia)

> **Segunda conferência, sobre a peça 2** (`build-wesales.md`, "Conferência da
> peça 2"): o raciocínio de unidade está certo (contador cumulativo de um lado
> pede contador cumulativo do outro — é por isso que C-31 existe), mas os dois
> lados da razão **não são da mesma população**. `Conexões reais telefone`
> (C-31) só conta chamada de **LC Phone que gerou transcrição**; `Tentativas
> telefone` (C-09) conta **toda** tentativa que o SDR classificou. Ligação pelo
> celular do SDR, período com transcrição desligada e ring sem transcrição a
> gerar entram no denominador e nunca no numerador — a razão fica enviesada
> **para baixo, de forma sistemática**, num widget chamado "Taxa de Conexão
> Real". Um número baixo seria lido como "o SDR não conversa com ninguém"
> quando a causa pode ser inteiramente "metade das ligações não é medida": a
> métrica que o F-06 existe para consertar, trocada por outra enganosa na
> direção oposta, e mais difícil de pegar porque não dá erro nem fica vazia.
> **Correção:** nó 2b (`Math: Ligações com transcrição + 1`), no caminho que já
> existe, e o denominador do widget passa a ser C-32 em vez de C-09 — "das
> chamadas que dá para medir, quantas foram conversa". De brinde, `C-32 ÷ C-09`
> vira o widget `Cobertura da Medição — Telefone`, que expõe quanto da operação
> está instrumentada em vez de esconder isso dentro da taxa. C-32 nasce `[ ]`.


> **Conferido no mesmo dia** (`build-wesales.md`, "Conferência do F-06"): o
> gatilho `Transcript Generated` confere, mas a dependência é mais funda do
> que "ligar a transcrição". **Transcrição exige gravação de chamada** — sem
> gravação não há transcrição e o workflow nunca dispara. Então ligar o F-06 é
> decidir que **toda ligação de saída passa a ser gravada**, o que traz três
> pré-requisitos que não estavam no item: (a) **aviso de gravação** no início
> da ligação, por LGPD — lugar reservado em `script-de-ligacao.md`, seção 2,
> redação e base legal do dono, e ele **concorre com o gancho** que o R-05 vai
> otimizar; (b) **custo**: add-on Voice Intelligence a US$ 0,024/minuto
> gravado, acima da gravação e do armazenamento (~US$ 45/mês pela conta da
> seção 2.27, premissas declaradas) — e paga-se principalmente por transcrever
> os ~80% de chamadas que não são conversa; (c) **um reset**: `Conexão real`
> nunca é apagado, e chamada não atendida pode não gerar transcrição nenhuma,
> então um `Sim` da T3 sobrevive a T4-T8 e o campo passa a significar "alguma
> tentativa foi conversa" em vez de "esta foi". O reset vai no nó que cria a
> tarefa de cada tentativa (2.4/2.10), antes da ligação, não no Pós-ligação.
> **O F-06 não está pronto com os nós 1-6 sozinhos** — gravação, aviso e
> custo continuam decisão do dono, pendência registrada, não lacuna
> esquecida (mesmo padrão do F-08/F-09 abaixo, marcados `FEITO` com
> pendência declarada em vez de escondida).

**Por quê:** `Atendeu` empacota na mesma célula a ligação de 8 segundos e a de 8
minutos. A métrica que importa não é alô, é conversa.
**Como:** duração da ligação vinda do call tracking; campo `Conexão real` = 
atendeu **e** durou mais de 60s. A taxa de conexão do relatório passa a usar
esse campo.
**Pronto quando (cumprido):** "taxa de conexão" no relatório significa
conversa, e o SDR não consegue inflar o número desligando rápido — a lista
8.6 ganhou a coluna `Conexão real` e o dashboard (2.17) ganhou o widget
`Taxa de Conexão Real — Telefone`, os dois convivendo com o relatório
antigo em vez de substituí-lo.

**Achado que destrava o item — corrige a rodada de 21/09/2026 (a mesma que
fechou o R-18), que tinha lido este item como "premissa técnica (call
duration nativo) confirmou que a plataforma ainda não oferece isso, sem
destravar nada":** essa conclusão veio de uma busca rasa, sem entrada própria
em `APRENDIZADOS-CRM.md` — exatamente a classe de erro que o próprio F-08
cometeu duas vezes na mesma semana e que já tem regra escrita contra ela
("premissa negativa é a mais barata de conferir e a mais cara de errar").
Três buscas desta rodada, com termos diferentes, convergem: o GHL tem um
gatilho de workflow chamado **`Transcript Generated`**, que dispara quando a
transcrição de uma chamada fica pronta e carrega duração, direção e horário
como dado do próprio evento — e funciona para chamadas de **Voice AI, IVR e
LC Phone** (a telefonia nativa do GHL). Este projeto não usa Voice AI nem
IVR, então toda ocorrência do gatilho nesta subconta só pode vir de LC
Phone. Pré-requisito citado pela fonte: transcrição precisa estar **ligada
em Configurações → Telefone** para chamadas LC Phone (em Voice AI já vem
ligada por padrão) — ação de tela, não de API, mesma classe de pendência que
o Number Validation (seção 2.16) já tem.

**A mesma pendência que o F-08/F-09 já registraram, herdada aqui sem
solução nova:** nenhum documento do projeto confirma se as 100 ligações/dia
da operação saem por LC Phone ou por linha própria do SDR. Se for LC Phone,
este item funciona como especificado abaixo; se for linha própria,
`Transcript Generated` nunca dispara para essas chamadas e o item volta a
depender de call tracking externo, do zero. Uma resposta só resolve as três
pendências (F-06, F-08, F-09) ao mesmo tempo — não é desenhada aqui de novo.

**Confiança:** média — a descrição do gatilho ("duration... direction...
across Voice AI, IVR, and LC Phone calls") apareceu de forma consistente em
buscas diferentes, mas `help.gohighlevel.com` segue bloqueado pelo proxy
deste ambiente (lido só por citação de busca, mesma limitação de sempre) e
nada foi testado nesta subconta. Um filtro de duração **no próprio gatilho**
apareceu numa busca; outra busca, sobre um gatilho diferente (`Call
Status`), afirma que filtro nativo de duração ainda não existe na
plataforma — sem fonte que resolvesse a contradição para o `Transcript
Generated` especificamente, o desenho abaixo não depende dela: lê a duração
como dado do gatilho e decide no `If/Else`, caminho que funciona com ou sem
filtro nativo.

**Resumo (22/09/2026, peça 1 — especificação do workflow):** workflow novo
"Qualidade da Conexão" especificado nó a nó em `build-wesales.md`, seção
2.27, e `IMPLEMENTACAO-WORKFLOWS.md`, W20 — grava a duração real e decide
`Conexão real` por um limiar de 60s, **sem** tocar nos contadores existentes
(`Conexões telefone`/`Conexões WhatsApp`/`Total de conexões`, que continuam
vindo do julgamento do SDR no Pós-ligação): os dois convivem, e a diferença
entre eles é o próprio dado que expõe quando o SDR marca `Atendeu` numa
ligação curta demais para ser conversa. Dois campos novos propostos —
`Duração da ligação` (C-29, NUMERICAL, segundos) e `Conexão real` (C-30,
SINGLE_OPTIONS: Sim, Não) — em `campos-e-tags.md` e `APROVADO.md`, nascendo
`[ ]`, mesma regra de todo campo desde o incidente da T-15.

**Peça 2, mesmo dia — o plano da peça 1 ("apontar os dois para `Conexão
real`") não sobrevivia à leitura dos dois destinos, então mudou.** A lista
`Conexão por Tentativa` (8.6) podia mesmo ganhar `Conexão real` direto —
Smart List filtra/mostra qualquer tipo de campo — e ganhou, como coluna
nova ao lado dos contadores antigos, sem trocar o filtro (a lista continua
comparando os dois números, não escolhendo um). O dashboard (2.17) não
podia: o próprio achado 2 daquela seção, já registrado antes do F-06
existir, diz que o Formula Editor de Custom Metrics só agrega Soma sobre
campo `NUMERICAL`/`MONETARY` — `Conexão real` é `SINGLE_OPTIONS`. Pesquisado
nesta rodada se a plataforma ganhou desde então um jeito de contar contatos
por valor de campo personalizado (metric-level filters, recurso mais novo
que o achado 2 não conhecia): existe para tag/pipeline/owner, mas mesmo
que cobrisse campo personalizado, contaria contatos no estado **atual**,
não chamadas ao longo do tempo — unidade errada para dividir por
`Tentativas telefone`, que é soma cumulativa de tentativas. Também herdaria
para o relatório o próprio estado vencido que a peça 1 já flagrou em
`Conexão real` (um `Sim` da T3 sobrevive a T4-T8 sem transcrição nova).
Terceiro campo, então: `Conexões reais telefone` (C-31, NUMERICAL),
incrementado por `Math +1` uma vez por chamada que bate o limiar — mesmo
padrão de `Conexões telefone`/`Conexões WhatsApp`/`Total de conexões`
(C-06/C-07/C-11/C-12), nunca sobrescrito, então sem o defeito que motivou
trocar o plano. Nasce `[ ]` como os outros dois. `build-wesales.md`, seção
2.27 (nó 6 novo) e seção 8.6/2.17; `campos-e-tags.md` C-31;
`IMPLEMENTACAO-WORKFLOWS.md` W20.

Zero escrita no CRM nesta rodada (as duas peças). Subconta reconfirmada via
`opportunities_search-opportunity`/`locations_get-custom-fields`/
`opportunities_get-pipelines`/`conversations_search-conversation`: mesmas 5
etapas do `FUNIL DE VENDAS`, 51 campos (sem mudança — os três novos deste
item ainda não saem da proposta), 50 oportunidades (47 `NOVO LEAD` + 3
`NEGOCIAR`, 1 `lost` de teste, 49 `open`), zero conversa de WhatsApp/SMS
real (só DMs de Instagram e o rastro de no-show dos contatos fictícios) —
G-03/G-04 seguem aguardando o dono. Pendência que continua aberta e
registrada, não nova: confirmar se as ligações saem por LC Phone ou linha
própria do SDR (mesma do F-08/F-09) e a decisão do dono sobre gravar toda
ligação de saída (custo, aviso LGPD) — nenhuma das duas bloqueava o
trabalho desta rodada, que era desenho, não execução.

### F-07 · Proteção de reputação do número de WhatsApp — **FEITO em 22/09/2026**
**Por quê:** G-05/G-06 protegem a **entrega** de cada mensagem individual
(janela de 24h, Template aprovado). Nada no projeto protegia o **número**
que envia: a Meta atribui a todo número do WhatsApp Business API uma
Quality Rating (Verde/Amarela/Vermelha, por bloqueios/denúncias/engajamento
dos últimos 30 dias) e um Tier de mensagens que trava de subir e pode
throttlar ou recusar envio se a nota cair — inclusive dentro da janela e
com Template aprovado. Se isso acontecer, toda a especificação de mensagem
do projeto (M1 a NS-2, os lembretes do Pós-agendamento, QI-1) para de
entregar ao mesmo tempo, sem erro visível em nenhum workflow — o mesmo tipo
de "estrago silencioso" que motivou o F-05 e o G-05, aqui na camada de
infraestrutura do canal, não de lead individual (não duplica F-04, que
protege o lead de excesso de toque, nem R-13, que valida o telefone do
lead, não a reputação do nosso número). Achado seguindo a própria instrução
deste roadmap: pesquisar como Reev/Meetime/Outreach/Salesloft resolvem
antes de desenhar — nenhuma das quatro trata WhatsApp Business API como
canal principal, o que deixa este risco fora do repertório usual de sales
engagement e mais alto aqui do que a paridade sugeriria.
**Como:** sem gatilho nativo do GHL para ler Quality Rating/Tier em tempo
de execução (pesquisado, não encontrado) — não é workflow, é checklist
manual do gestor em `Settings → WhatsApp → Manage`, com três gatilhos por
evento (antes de publicar os 4 nós de envio da 12x30 com volume real;
semanalmente enquanto o volume crescer; depois de qualquer pico na lista de
Opt-out do R-17) e mitigação com as peças que o projeto já tem (Template
já é a maioria dos envios por G-05/G-06; pausar só a variante do Split
apontada como causa; tratar a origem do pico de opt-out, ex. G-04, em vez
de só a nota). Detalhe nó a nó — na verdade linha a linha, já que não há nó
— em `build-wesales.md`, seção 2.25.
**Pronto quando (cumprido):** o gestor sabe os três momentos de checar a
nota antes que ela caia em silêncio, e o que fazer se cair, com o que o
projeto já tem — sem esperar um workflow que a plataforma não sustenta.

**Resumo:** especificado em `build-wesales.md`, seção 2.25 (nova, entre a
peça 6 do F-05 e o Mestre de saída). Zero campo, zero tag, zero workflow,
zero escrita no CRM — item de documentação e rotina manual pura, não
depende de `APROVADO.md`, não entra na "Ordem de montagem" (não há nó) nem
no checklist de teste da seção 10 (não há objeto de CRM para simular
reputação de número com contato fictício). Subconta reconfirmada nesta
execução via agente de leitura dedicado (`opportunities_search-opportunity`/
`locations_get-custom-fields`/`contacts_get-contacts`/
`conversations_search-conversation`): mesmas 5 etapas do `FUNIL DE VENDAS`,
51 campos, 50 oportunidades (47 `NOVO LEAD` + 3 `NEGOCIAR`, uma `lost` de
teste) — sem mudança desde a última leitura; confirmado também que a
subconta segue sem qualquer conversa de WhatsApp/SMS real da operação (só
DMs pessoais de Instagram), o que faz deste item um item "antes de ligar o
motor", não uma correção depois de já ter sofrido dano de reputação — G-03/
G-04 seguem aguardando o dono.

### F-08 · Proteção de reputação do número de telefone — **FEITO em 22/09/2026, com correção no mesmo dia**

> **Corrigido em 22/09/2026, na conferência da mesma rodada** (detalhe em
> `build-wesales.md`, "Correção do F-08"): a conclusão do item está certa, duas
> premissas não. (a) **SHAKEN/STIR existe no Brasil** — é a `Origem
> Verificada` (ABR Telecom / Portal AIA, 52+ prestadoras, ~6 bi de chamadas
> autenticadas/mês em agosto/2026, ~30% do tráfego), que mostra nome, logo e
> motivo na tela de quem recebe; obrigatória só acima de **500 mil
> chamadas/mês** (esta operação faz ~2.200), obrigação geral em ~outubro/2028,
> contratação documentada em `origemverificada.com.br` com resposta da ABR
> Telecom em 5 dias úteis — **mas descrita como aberta a empresas de grande
> volume nesta fase inicial**, então pode ser recusada por porte. Vale pedir:
> é um formulário. O "Qual Empresa Me Ligou?" não é o equivalente brasileiro,
> é o plano B — depende de o lead procurar o número. (b) O ato é o **Despacho
> Decisório nº 82/2026/RCTS/SRC, de 17/08/2026**, e o critério é mais largo que
> "quantidade e duração": inclui **proporção de chamadas de curtíssima
> duração, duração média, taxa de completamento e CNAE de quem origina** — ou
> seja, a norma mede **como as ligações terminam**, que é decisão de cadência,
> não de infraestrutura. (c) O `0303`, não mencionado no item, é facultativo
> desde agosto/2025 (com recomendação do MPF para voltar a ser obrigatório):
> **não adotar por conta própria** — virou estigma e derruba a taxa de
> atendimento —, mas vigiar. A correção também gerou o **F-09** abaixo.

**Por quê:** o F-07 protegeu a infraestrutura do canal WhatsApp; o canal
**majoritário** da cadência — ligação por telefone, 8 dos 12 toques da
tabela 2.5 — seguia sem proteção nenhuma de reputação de número, e o risco
deixou de ser hipótese na própria semana desta rodada: desde agosto/2026 a
Anatel obriga toda operadora brasileira a oferecer bloqueio de chamada
"abusiva" **grátis e ativado por padrão** para todo cliente, com critério
declarado de **quantidade e duração de chamadas** — exatamente o padrão da
meta do SDR (100 ligações/dia, tentativa curta quando não atende).
**Como:** pesquisado antes de desenhar (mandato do próprio roadmap) —
duas saídas óbvias, as duas descartadas por pesquisa e não por suposição:
(1) o recurso nativo do HighLevel para isto, **Voice Integrity**, é
explicitamente **US only** (exige registro SHAKEN/STIR com EIN americano),
não serve para número brasileiro; (2) o "Não Me Perturbe" da Anatel não se
aplica a este negócio — a obrigatoriedade alcança só prestadoras de
telecomunicações (~32% das ligações indesejadas do país), não uma agência
de marketing. Sem gatilho nativo para ler bloqueio de operadora (mesmo
limite de plataforma do F-07): virou checklist do gestor — cadastrar o(s)
número(s) no portal gratuito "Qual Empresa Me Ligou?" da Anatel (equivalente
brasileiro ao Branded Caller ID/CNAM), distribuir volume entre mais de um
número antes de escalar (100/dia num só número já bate ou passa a
referência internacional de 50-75/dia), vigiar queda abrupta de atendimento
como sintoma de bloqueio silencioso, e usar o canal de contestação que a
norma de agosto/2026 passa a exigir de toda operadora se isso acontecer.
Detalhe nó a nó — checklist, não há nó — em `build-wesales.md`, seção 2.26.
**Pronto quando (cumprido):** o(s) número(s) reais estão cadastrados no
"Qual Empresa Me Ligou?"; o gestor sabe que Voice Integrity e "Não Me
Perturbe" não protegem este número; e sabe, antes de escalar volume, que
concentrar 100 ligações/dia num único número é o próprio risco que a norma
existe para pegar.

**Resumo:** especificado em `build-wesales.md`, seção 2.26 (nova, logo após
a 2.25/F-07). Pendência registrada e não resolvida: nenhum documento do
projeto confirma se as ligações saem por LC Phone (telefonia nativa do
GHL) ou por linha própria do SDR — a mitigação de "quem cadastra o número"
muda com a resposta; o achado da norma e a exclusão do Voice Integrity/Não
Me Perturbe valem independente dela. Zero campo, zero tag, zero workflow,
zero escrita no CRM — item de documentação e rotina manual pura, mesmo
tratamento do F-07, não depende de `APROVADO.md`, não entra na "Ordem de
montagem" nem no checklist de teste da seção 10. Subconta reconfirmada
nesta execução (`opportunities_get-pipelines`/
`opportunities_search-opportunity`/`locations_get-custom-fields`): mesmas 5
etapas do `FUNIL DE VENDAS`, 51 campos (sem mudança), 50 oportunidades (47
`NOVO LEAD` + 3 `NEGOCIAR`, 1 `lost` de teste, 49 `open`) — sem mudança
desde a última leitura (F-07, mesma data) — G-03/G-04 seguem aguardando o
dono.

---

### F-09 · O telefone não tem freio de canal, e o WhatsApp tem — **aguarda decisão do dono** (aberto em 22/09/2026)

**Por quê:** achado ao conferir o F-08. O seletor de canal (nó 4 da seção
2.4; nó 3 da 2.10) só manda pelo WhatsApp se `WA não atendidas seguidas` for
**< 2** — duas sem resposta seguidas e o lead sai daquele canal. Não existe
equivalente no telefone: conferido por `grep` em todo o `wesales/`, `WA não
atendidas seguidas` é o **único** contador de "seguidas" do projeto, e o nó
10 das duas cadências manda `Caixa Postal` e `Não atendeu` **insistirem**
até o fim da régua.

| Canal | Toques dos 12 | Freio próprio |
|---|---|---|
| WhatsApp | 4 | 2 sem resposta seguidas → troca de canal |
| Telefone | **8** | **nenhum** |

O canal com o dobro dos toques, o único com regulador olhando (Despacho
Decisório nº 82/2026/RCTS/SRC — F-08), e o único sem freio. Pior: os
critérios que a norma manda a operadora considerar são **proporção de
chamadas de curtíssima duração, duração média e taxa de completamento** — as
três pioradas exatamente pelas tentativas que insistem sem conectar. É a
mitigação mais barata do F-08: não custa número novo, cadastro nem esperar a
`Origem Verificada` aceitar a subconta.

**Como (proposta, não executada):** campo novo `Tel não atendidas seguidas`
(NUMERICAL), somado no ramo `Não atendeu`/`Caixa Postal` do Pós-ligação e
zerado em toda conexão real — espelho exato do que o nó C1 (`IMPLEMENTACAO-
WORKFLOWS.md`, W4) já faz para o WhatsApp; depois um portão, no seletor de
canal e/ou no nó 10, que ao estourar desvie para WhatsApp ou encerre a régua
mais cedo.

**Por que não executo sozinho:** o limiar **é** a régua. Cortar o telefone
na 2ª não atendida seguida, como o WhatsApp faz, reduziria os 8 toques de
telefone a talvez 2-3 por lead — mexe direto na meta de 100 ligações/dia do
`briefing-sdr.md` e na conta de volume da L-05. Pode ser exatamente o que se
quer (menos discagem morta, mais tempo em lead que atende), ou o oposto
(insistir é o jeito de furar base fria). É decisão de negócio, e a regra do
briefing é não criar campo nem mexer em régua em massa sem confirmação.

**Três opções para o dono escolher — nenhuma aplicada:**

**Evidência indireta reavaliada em 22/09/2026, mesma data — o CRM não
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

| Opção | Limiar | Efeito |
|---|---|---|
| **A — espelhar o WhatsApp** | 2 não atendidas seguidas → sai do telefone | Mais protetora; corta mais fundo os 8 toques |
| **B — meio caminho** (recomendo começar aqui) | 4 não atendidas seguidas → desvia para WhatsApp; se WhatsApp também estourar, encerra | Mantém boa parte da insistência e ainda melhora as três razões da norma; reversível |
| **C — só medir** | contador criado, nenhum portão | Zero risco de régua, e em duas semanas há número real para decidir A ou B com dado em vez de palpite |

**Pronto quando:** o dono escolher A, B ou C; o campo `Tel não atendidas
seguidas` nascer em `APROVADO.md` com `[x]` **dele**, não meu; e o portão
escolhido estar escrito nó a nó nas seções 2.4/2.10/4.

---

### F-10 · Nenhum monitor olha a **entrada** — mais de 22 horas sem lead novo e nada avisou — **aguarda decisão do dono** (aberto em 22/09/2026)

> **Correção (22/09/2026, sessão automática seguinte):** a rodada que abriu
> este item errou a conta — escreveu "~46 horas" quando as próprias duas
> datas da tabela abaixo (21/09 09:17 → 22/09 ~07:30) dão ~22h13min, quase a
> metade. O erro se espalhou para o título deste item, `APRENDIZADOS-CRM.md`,
> `briefing-sdr.md` (correção da L-07) e `build-wesales.md` (F-10 na tabela
> de Custom Metrics) — os quatro corrigidos no mesmo commit. A conclusão do
> item **não muda** (a entrada segue parada, os seis monitores do F-05
> continuam cegos para isso), só a magnitude. Detalhe da regra generalizável
> em `APRENDIZADOS-CRM.md`.

**O que foi medido**, na conferência da rodada de `b7ae300` (leitura por API, nada
suposto), e reconfirmado nesta rodada (leitura por API às 22/09 ~08:05 UTC):

| Fato | Valor |
|---|---|
| Contatos na subconta | **50** (sem mudança) |
| Oportunidades | **50** — um para um, a Porta de Entrada (G-01) está funcionando |
| Lead mais novo (contato) | `Carlos Andrade`, **21/09 09:17:23 UTC**, `source: Facebook` — ainda o mesmo, nenhum lead novo entrou |
| Oportunidade dele | 21/09 09:17:**26** UTC — 3 segundos depois, é o G-01 disparando num lead real |
| Agora | 22/09 ~08:05 UTC |
| **Tempo sem lead novo** | **~22h47min e subindo** (correto: 21/09 09:17 → 22/09 08:05; a rodada anterior tinha escrito ~46h por engano — ver correção acima) |

O padrão de chegada antes disso, pelos `dateAdded`: 9 leads entre 19/09 22:50 e
20/09 18:11 (~19h), 1 em 21/09 09:17, e **nada desde então**. Todos os 50
carregam atribuição de Meta Lead Ads viva (`LEADS I FORM I FS1`, anúncio
`120247453176830766`, criativo `V16 — copy impulsionou`).

**A medida que torna isto interpretável — e que o erro de conta da abertura
teria evitado, acrescentada em 22/09:** horas absolutas não se calibram (foi o
que deixou "~46h" passar: soava plausível). O intervalo entre chegadas
consecutivas, na própria base, se calibra:

| Gap entre chegadas | |
|---|---|
| Os 8 primeiros | de **9 min** a **3h06** |
| 20/09 07:32 → 17:47 | **10h15** |
| 20/09 18:11 → 21/09 09:17 | **15h06** ← maior já observado nesta subconta |
| 21/09 09:17 → agora | **23h02 e subindo** ← **1,53× o maior já visto** |

**Atualização 22/09 09:36 UTC — a marca de 24h foi cruzada:** gap agora em
**24h19min = 1,61× o maior já observado**, e nenhum lead novo (reconferido:
`meta.total` = 50, o mais recente segue sendo `Carlos Andrade` de 21/09
09:17:23). Consequência prática: a lista `Entrada — últimas 24h` (seção 8.25
do `build-wesales.md`), se já estivesse montada, estaria **vazia agora** — o
limiar "zero linha na janela rolante" deixou de ser hipótese e está valendo
neste momento. O widget `Leads novos hoje` também marcaria zero.

É assim que o número vira sinal em vez de curiosidade: o silêncio atual já
passou de metade além do maior silêncio que esta operação jamais teve. E é
a comparação que qualquer widget do F-10 deve mostrar, não o total de horas —
um "23h" sozinho não diz a ninguém se é normal; "1,5× o maior intervalo já
visto" diz.

**Um segundo número, mais desconfortável, do mesmo cálculo:** na janela em que
a entrada *funcionou* (19/09 22:50 → 21/09 09:17, ~34h30), chegaram **10
leads** — cerca de **7 leads/dia**, contra a premissa de **~10/dia** do
`briefing-sdr.md`. Amostra pequena (10 leads, uma janela, e os outros 40
contatos são backfill sem data de chegada real), então **não é conclusão** —
mas é a primeira medição de entrada que o projeto tem, e ela vem abaixo da
meta que dimensiona a régua inteira (a conta da L-05: 10/dia × 12 tentativas).
Se confirmar com mais dados, o gargalo da operação não é a cadência, é o
funil de aquisição antes dela.
**Não é falha de workflow.** Contatos = oportunidades, e o G-01 fecha em 3
segundos no lead real mais recente. Se o Meta entregasse, o CRM registraria. O
que parou está **antes** do CRM: campanha pausada, orçamento esgotado,
formulário do anúncio com problema, ou reprovação de criativo. Nenhuma dessas
coisas o CRM enxerga.

**O gap, e é estrutural:** o Monitor de Saúde da Operação (F-05) tem **seis**
peças — `NOVO LEAD` estagnado, fila travada, `CONECTAR` sem avanço, `AGENDAR`
estagnado, retorno vencido, teto de toques. Todas as seis vigiam lead que
**ficou parado**. **Nenhuma vigia lead que nunca chegou.**

E essa é a falha mais consequente que esta operação pode ter, porque é a única
que faz **todos** os outros indicadores melhorarem:

| Com a entrada parada | O que o painel mostra |
|---|---|
| Fila de ligação | esvazia (bom sinal) |
| `NOVO LEAD` estagnado | para de crescer (bom sinal) |
| Toques na semana | cai abaixo do teto (bom sinal) |
| Alerta de speed-to-lead | silencia — não há 1ª tentativa atrasada se não há lead |
| Taxa de conexão | sobe, porque só sobram os leads já trabalhados |

Seis monitores, todos verdes, e a máquina passando fome. É o oposto exato do
que os alertas foram desenhados para pegar — eles medem congestionamento, e
isto é inanição.

**Como fazer, e é barato — usando a capacidade que o F-06 peça 2 rejeitou:**
o Formula Editor de Custom Metrics **conta contatos por filtro** (achado da
seção 2.17, reconfirmado na peça 2 do F-06). Ali aquilo era a unidade errada,
porque o outro lado da razão era cumulativo. Aqui é exatamente a unidade certa
— a pergunta é "quantos contatos nasceram hoje", que é uma contagem de
contatos por filtro e nada mais:

| Widget | Definição | Lê-se |
|---|---|---|
| `Leads novos hoje` | contagem de contatos com `Date Created` = hoje | Entrada do dia. Zero às 12h já é sinal |
| `Leads novos — 7 dias` | contagem de contatos com `Date Created` nos últimos 7 dias | Tendência: separa "dia fraco" de "parou" |

E a lista equivalente, para quem não tiver Custom Metrics no plano —
especificada como seção **8.25** do `build-wesales.md`, e **conferida em
22/09** com duas correções que decidem se ela serve:

- O filtro tem de ser **relativo** (`Data de criação` `In the Last` `1 dia`),
  não igualdade contra uma data picada no calendário: Smart List do GHL tem
  filtro de data relativa e é dinâmica de verdade, mas quem escolher um dia
  fixo congela a lista e ela para de atualizar amanhã, em silêncio.
- **Duas listas salvas** (24h e 7 dias), não uma com o filtro trocado: Smart
  List é view compartilhada, e alternar o filtro muda para todos os usuários.

E a leitura: `In the Last 1 dia` é janela **rolante**, não "hoje" — que para o
F-10 é melhor, porque é a mesma grandeza do gap (maior já observado: 15h06),
mas não deve ser chamada de "hoje" ou alguém lê errado às 9 da manhã.

**O que eu não sei fazer nativo, e digo em vez de inventar:** um **alerta**
automático de ausência de entrada. Workflow do GHL vê um contato por vez
(limite já registrado em `APRENDIZADOS-CRM.md`) e não existe gatilho "nenhum
contato foi criado em 24h" — não há contato para o workflow enrolar. As saídas
são (a) o widget/lista acima, que depende de alguém olhar, ou (b) um contato
sentinela fixo, num workflow com `Wait 24h` em laço, comparando um campo de
checkpoint que todo lead novo atualiza — funciona, mas é engenhoca, custa um
contato de serviço e um campo, e só vale se o dono quiser alarme de verdade e
não um número no painel. **Não especifico a (b) sem ele escolher.**

**Consequência para o G-03, e é uma correção de fato:** o item diz que os 47
parados estão "crescendo todo dia". **Não estão** — o estoque está estático em
47 há mais de 22 horas (e subindo). Isso não torna o G-03 menos importante (47
leads pagos sem cadência continuam sendo 47 leads pagos sem cadência), mas
troca o argumento:
a pressão não é o crescimento, é o **envelhecimento**. Lead de Meta Lead Ads
esfria por hora, não por semana — e o mais velho do estoque já tem três dias.

**Pronto quando:** existe um número de entrada do dia visível sem abrir o
Gerenciador de Anúncios (widget ou lista), o dono sabe que os seis monitores
do F-05 não cobrem entrada, e ele decidiu se quer só o número ou também o
alarme da opção (b).

**Resumo (22/09/2026, sessão automática seguinte) — especificação
fechada, decisão do dono ainda em aberto:** a peça que faltava era a
Smart List `Entrada do dia` — os dois widgets de Custom Metrics já
tinham entrada própria na seção 2.17 do `build-wesales.md` desde a
abertura do item, mas a lista só existia como frase solta aqui no
roadmap ("Smart List `Entrada do dia`, filtro `Date Created` = hoje,
ordenada por criação"), nunca como seção numerada em "8. Listas
inteligentes" — a fonte que `GUIA-MONTAGEM.md` (Fase 6) de fato consulta,
por instrução própria dele ("este guia não repete o conteúdo, só organiza
a ordem"). Achado ao conferir se a Fase 6 encontraria a lista partindo só
do `build-wesales.md`: não encontraria. Fechada como seção 8.25, com
referência cruzada nova na 2.17 (mesmo padrão de fallback "sem Custom
Metrics" que as outras linhas do dashboard já usam). CRM reconfirmado sem
mudança via API: 51 campos, 50 oportunidades (47 `NOVO LEAD` + 3
`NEGOCIAR`), lead mais novo ainda `Carlos Andrade` (21/09 09:17:26 UTC) —
agora **quase 24h** sem entrada nova (23h47min no momento desta leitura,
09:04 UTC de 22/09), confirmando que o silêncio segue e que o item de
alarme (opção b) continua tão relevante quanto na abertura. G-03/G-04
seguem aguardando o dono; a opção (b) deste item também. Zero campo, zero
tag, zero escrita no CRM: item de especificação pura, não depende de
`APROVADO.md`.

---

## Ordem sugerida

**Bloco 0 (G-01) fechado em 19/09/2026, antes de tudo o resto desta seção:**
não é item de fila, é pré-requisito — nenhum bloco abaixo importa enquanto
nenhuma oportunidade nasce sozinha. Descoberto depois dos blocos 1 a 5 e
quase todo o 6 já estarem prontos, mas listado primeiro porque é anterior
em sentido literal, não por ordem de descoberta.

**G-02 fechado em 21/09/2026** — o checklist de migração de nomes de etapa
(`GUIA-MONTAGEM.md`, Fase 1) está com todas as caixas `[x]`; `grep -n "Em
cadência\|Nutrição\|Retorno agendado\|Descartado\|Pré-vendas"
wesales/build-wesales.md` só retorna tabela de tradução (1.0) ou prosa
histórica. Não sobra mais trabalho de fundo deste tipo para uma sessão
automática sem item de volume/mensagem real avançar — ver nota no fim
desta seção sobre o que resta.

**G-04 aberto em 21/09/2026, aguardando o dono** — a leitura dos dados
(não do texto) mostrou o Meta Lead Ads gravando em `Urgência`/`Necessidade`
e enchendo `Investimento mensal em anúncios` com valores fora da lista de
opções: a nota de qualificação de todo lead do Meta nasce zerada no Bloco
B. Junto com G-03, é o que separa "workflow publicado" de "operação
funcionando" — os dois esperam decisão, nenhum sai por API.

**G-03 aberto em 21/09/2026, aguardando o dono** — mesma varredura que
fechou o G-02 (reconferir a subconta antes de encerrar sem commit) achou
que a L-07 (`briefing-sdr.md`), registrada como lacuna teórica desde
18/09, virou problema real: 47 oportunidades pagas paradas em `NOVO LEAD`
sem cadência. (O "crescendo todo dia" de 21/09 **não vale mais**: medido em 22/09, zero lead novo em mais de 22 horas e subindo — o estoque está estático em 47 e o que pressiona agora é o envelhecimento, não o crescimento. Ver F-10, que corrige também o número de horas escrito na abertura do item.) Três opções escritas para o dono
escolher — nenhuma executada, nenhuma vira `[x]` sozinha.

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
Antes disso, não há a quem incomodar. (G-02, Bloco 0, fechou em
21/09/2026 — ver nota no início desta seção.)

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
explicar a um lead por que ele recebeu seis avisos no mesmo dia. F-05 saiu
fora de ordem em 21/09/2026 pelo mesmo motivo geral de F-04, não por
volume: **esta frase dizia até 21/09/2026 que "F-05 só morde quando há mais
de uma cadência no ar" — estava errada.** As invariantes do F-05 (lead
parado numa etapa, tarefa vencida) não dependem de quantas réguas existem;
dependem de ter lead de verdade na subconta, e G-03 (Bloco 0) mostrou que
isso já é fato — 47 leads pagos parados em `NOVO LEAD`, achados só porque
uma sessão olhou o número na mão. Restou só o F-06 pedindo volume de
verdade: precisa de call tracking ligado, que ninguém tem motivo para
ligar antes da `Cadência 12x30` sair do rascunho e gerar ligação de
verdade para medir.

**Não há mais "ordem normal" a retomar.** Esta frase dizia, desde a primeira
rodada, que o bloco 1 de medição terminaria e só então o bloco 2 entraria na
fila; os dois fecharam em 18/09/2026, junto com os blocos 3 e 4 e o R-13 do
bloco 5. O F-05 (bloco 6) fechou por inteiro em 21/09/2026 — não sobra peça
represada nele. O que resta entre os itens numerados não espera posição na
fila, espera a operação existir: R-14 quando a máquina começar a mandar
mensagem de verdade, e o F-06 quando houver volume de ligação real.

**Com G-02 fechado em 21/09/2026 e o F-05 inteiro (seis peças) fechado na
mesma data, não sobra item de documentação pura óbvio esperando uma sessão
sem tela nem volume — mas isso não é permanente, como o próprio F-05
acabou de mostrar seis vezes na mesma rodada, a última (peças 5 e 6) só
depois de uma dependência que parecia fechada ("esperar até uma data
dinâmica, não testado neste conector") se resolver sozinha por uma busca
melhor.** O que resta é de três tipos: (1) montar na tela o que já está
especificado (pipeline, campos, workflows, calendário e formulário, pelo
`build-wesales.md`) — trabalho manual, ao vivo com o dono, e as peças 5/6
do F-05 acrescentaram mais retoques "dá para fazer hoje" a essa fila
(`GUIA-MONTAGEM.md`), além de completar duas lacunas antigas da própria
"Ordem de montagem" (as peças 2 e 3 do F-05 nunca tinham entrado nela) —,
(2) esperar volume/mensagem real para R-14 e F-06, e (3) G-03/G-04, que
esperam decisão do dono, não desenho. Não sobra peça do F-05 represada por
premissa técnica. Uma sessão automática sem acesso à tela e sem (2)
desbloqueado não deve inventar trabalho para preencher a rodada: o próximo
passo honesto é a varredura de coerência entre documentos (a mesma que
fechou G-02 e a peça 4 — grep por nome antigo, merge field órfão, contagem
duplicada, lista manual que devia ter virado ação nativa) e, se ela não
achar nada, reler os itens represados por "premissa técnica não testada"
como esta rodada acabou de fazer com o F-05 (a razão de esperar pode ter
vencido sem ninguém notar) e, só depois, procurar uma lacuna nova que
nenhum item aqui cobre ainda (o mesmo raciocínio que criou G-01, G-02, a
peça 4 do F-05 e o bloco 6 inteiro) antes de encerrar sem commit.

**R-18 fechado em 21/09/2026, mesmo dia, sessão automática seguinte —
achado exatamente por esse último caminho.** A varredura de coerência não
achou nome de etapa órfão nem contagem duplicada nova; a releitura de
premissa técnica (call duration nativo para o F-06) confirmou que a
plataforma ainda não oferece isso, sem destravar nada. A lacuna nova veio
de conferir se cada lacuna do `briefing-sdr.md` (L-01 a L-09) tinha item
correspondente no roadmap: L-08 não tinha — ficou como "opcional" desde
18/09/2026 e nunca foi promovida, diferente de L-01/L-04/L-05/L-07/L-09.
Confirmado antes de fechar que ainda valia a pena: `opportunities_search-
opportunity` segue em 50 (47 `NOVO LEAD` + 3 `NEGOCIAR`, sem mudança —
G-03/G-04 continuam aguardando o dono) e `conversations_search-conversation`
confirma que nenhuma mensagem de cadência automática saiu de verdade ainda
(as 4 conversas outbound da subconta são DMs pessoais de Instagram, não
tráfego da máquina) — R-14 corretamente segue bloqueada. Conferidas as nove
lacunas do briefing (L-01 a L-09) uma a uma nesta rodada: L-02 também
estava sem marcação de fechamento no `briefing-sdr.md` apesar de já
resolvida sozinha (Fase 2 criou `Segmento` como `TEXT` livre), corrigido
junto por ser trivial. L-03 (`fila-linkedin`, reserva) e L-06 (`Origem do
lead`, opcional) continuam sem item de roadmap **de propósito** — são
decisão registrada e melhoria opcional sem urgência, não bug à espera de
alguém notar, a diferença que justificou promover L-08 e não as outras
duas. Com isso, nenhuma lacuna do briefing original que se comporta como
bug ainda represado ficou sem item próprio no roadmap; o que resta segue
sendo os mesmos três tipos do parágrafo acima.

**G-05 aberto em 21/09/2026, sessão automática seguinte, mesmo dia —
lacuna nova, achada seguindo a própria instrução deste roadmap ("procurar
lacuna nova que nenhum item aqui cobre ainda" antes de encerrar sem
commit).** CRM reconfirmado sem mudança (46 campos, 50 oportunidades, G-03/
G-04 ainda aguardando o dono) — nada para o sweep de coerência de sempre
corrigir. A lacuna veio de uma pergunta que nenhuma rodada tinha feito
ainda: toda mensagem de WhatsApp da operação está especificada como texto
livre, e o WhatsApp Business API recusa texto livre fora da janela de 24h
de atendimento — janela que só abre quando o cliente escreve primeiro, o
que nenhum lead desta base jamais fez. Especificado o primeiro pedaço (a
Cadência 12x30, motor principal) — faltam os demais pontos de envio para o
mesmo tratamento, registrados como pendência explícita dentro do próprio
item.

**G-05, segunda peça, 22/09/2026, sessão automática seguinte — pendência de
guarda zerada.** CRM reconfirmado: 50 oportunidades sem mudança, mas os
campos personalizados subiram de 46 para 51 — os 5 novos (`Hora da
conexão`, `Toques na semana`, dois `Checkpoint —`, `Hora do retorno`) já
estavam especificados em `campos-e-tags.md` desde rodadas anteriores
(C-25 a C-28, S-01), então a montagem manual na tela avançou por fora
desta sessão, sem gerar achado novo de coerência. A pendência que a peça 1
tinha deixado explícita (`MI-0`/`MI-F`, `RE-1`/`RE-2`, `NS-1`/`NS-2` e os
quatro nós do Pós-agendamento) está fechada — todo `Send WhatsApp` da
operação já tem a guarda de janela e os dois ramos especificados. O que
resta do G-05 não é mais desenho: é a submissão dos Templates à Meta
(ação do dono) e a montagem manual de cada guarda na tela — o mesmo tipo
de trabalho que já espera em outras peças do projeto, não uma lacuna nova.

**G-06 aberto e peça 1 fechada em 22/09/2026, sessão automática seguinte —
o parágrafo acima estava incompleto no dia em que foi escrito.** "Todo
`Send WhatsApp` da operação" queria dizer "todo `Send WhatsApp` catalogado
em `biblioteca-mensagens.md`" sem dizer isso explicitamente — e o workflow
`Qualificação por IA no WhatsApp` nunca entrou naquele documento (fechou em
18/09/2026, antes de o G-05 existir), então a varredura que fechou a peça 2
não tinha como alcançá-lo. Achado ao trocar a pergunta "todo código da
biblioteca tem guarda?" (já respondida) por "todo `Send WhatsApp` do
`build-wesales.md` tem guarda?" — `grep -n "Send WhatsApp"` aponta um uso
sem guarda dentro da seção 6, o ponto de entrada mais exposto de todos:
dispara depois de uma ligação sem resposta, não de uma mensagem do lead, e
o Caminho A recomendado usa `Conversation AI`, que gera texto na hora e por
isso não tem como pré-aprovar Template do jeito que M1/M2/M3 têm. Fechado o
Caminho A (guarda + template novo `QI-1`); Caminho B (8 perguntas manuais,
mesmo problema em cada uma) fica pendência explícita, registrada dentro do
próprio G-06 — não bloqueia o Caminho A, que é o recomendado. CRM
reconfirmado sem mudança (51 campos, 50 oportunidades, G-03/G-04 ainda
aguardando o dono); Composio/HighLevel reconferido e ainda sem conta
conectada (0 contas ativas). Detalhe completo no próprio G-06, acima.

**G-06, segunda peça, 22/09/2026, sessão automática seguinte — item
fechado por inteiro.** A pendência que a peça 1 deixou explícita (Caminho
B, mesmo problema da janela em cada uma das 8 perguntas) tinha duas saídas
cogitadas e nenhuma escolhida; esta rodada escolheu reestruturar o caminho
em vez de multiplicar Template — cada bloco só avança para a pergunta
seguinte quando o lead responde de verdade, e sem resposta encerra em vez
de insistir fora da janela. Não sobra mais nenhum `Send WhatsApp` da
operação sem guarda. CRM reconfirmado sem mudança (51 campos, 50
oportunidades — a única variação frente à última leitura é um registro de
teste com `status = lost`, não volume real; G-03/G-04 ainda aguardando o
dono). Com G-06 fechado, o Bloco 0 inteiro está resolvido ou aguardando
decisão do dono (G-01, G-02, G-05 peças de especificação e G-06, todos
`FEITO`; só G-03 e G-04 restam, e nenhum dos dois sai por trabalho de
documentação — precisam de escolha do dono).

**F-07 aberto e fechado em 22/09/2026, sessão automática seguinte — lacuna
nova, achada pela pesquisa de concorrência que este roadmap sempre manda
fazer antes de desenhar.** CRM reconfirmado sem mudança (51 campos, 50
oportunidades, zero conversa de WhatsApp/SMS real ainda — G-03/G-04
seguem aguardando o dono): sweep de coerência de sempre não achou nada
novo em texto (nomes de etapa, merge field, contagem duplicada — a lista
manual do Mestre de saída, seção 3, foi conferida de novo e continua
correta *de propósito*, não é a mesma lista das outras três seções: o
achado do F-05 peça 4 já registra por que só ali `Remove Workflows`/`All
Except Current Workflow` teria cortado lembrete e tarefa de um workflow
ainda em execução). A lacuna veio de perguntar "como Reev/Meetime/
Outreach/Salesloft protegem o canal de envio, e o que eles não cobrem
porque não usam WhatsApp Business API como canal principal" — nenhuma das
quatro lida com Quality Rating/Tier de mensagens, e nada no projeto (F-04
protege o lead da frequência, R-13 valida o telefone do lead, G-05/G-06
protegem a janela de 24h) protegia a reputação do **nosso** número, que
pode cair mesmo com toques dentro do teto, telefone válido e Template
aprovado. Sem gatilho nativo para ler isso por workflow (pesquisado, não
achado): virou checklist manual do gestor com três gatilhos por evento,
não um workflow novo — `build-wesales.md`, seção 2.25. É item para checar
**antes** de a `Cadência 12x30` sair do rascunho com volume real, não
depois de a nota já ter caído.

**F-08 aberto e fechado em 22/09/2026, sessão automática seguinte — mesmo
método do F-07, canal diferente.** CRM reconfirmado sem mudança (51
campos, 50 oportunidades — G-03/G-04 ainda aguardando o dono): sweep de
coerência de sempre limpo (grep por nome de etapa antigo confirma que toda
ocorrência restante é da tabela 1.0 ou prosa histórica; merge fields de
`build-wesales.md`, `biblioteca-mensagens.md`, `IMPLEMENTACAO-WORKFLOWS.md`,
`script-de-ligacao.md` e `GUIA-MONTAGEM.md` batem 1:1 contra os 51
`fieldKey` reais, incluindo o falso positivo deliberado já documentado do
`checkpoint_data_de_retorno`). A lacuna veio de perguntar a mesma pergunta
do F-07 para o canal que ele não cobriu: telefone carrega 8 dos 12 toques
da cadência e não tinha proteção de reputação de número nenhuma. A
pesquisa quase copiou a resposta errada duas vezes — o recurso nativo do
HighLevel para isto (**Voice Integrity**) é **US only** (SHAKEN/STIR com
EIN americano), e o mecanismo brasileiro que mais parece resolver
("Não Me Perturbe" da Anatel) **não alcança este setor** (só prestadoras
de telecomunicações, confirmado por múltiplas fontes convergindo no mesmo
número, ~32% das ligações indesejadas do país) — as duas descartadas por
pesquisa, não por suposição, evitando a mesma classe de erro que motivou
guardar a regra de nunca supor rótulo/campo sem checar a fonte certa. O
risco real e atual: desde agosto/2026 toda operadora brasileira é obrigada
a oferecer bloqueio de chamada "abusiva" grátis e ativado por padrão, com
critério declarado de quantidade e duração de chamada — a meta desta
operação (100 ligações/dia) já bate ou passa a referência internacional de
segurança (50-75/dia por número). Virou checklist do gestor, mesmo motivo
do F-07 (sem gatilho nativo para ler bloqueio de operadora) —
`build-wesales.md`, seção 2.26. Pendência registrada, não resolvida: o
projeto não documenta se a ligação sai por LC Phone ou linha própria do
SDR — não bloqueia o item, muda só qual mitigação da tabela se aplica
primeiro.

**F-06, peça 1, 22/09/2026, sessão automática seguinte — item destravado,
não fechado por inteiro naquele momento (fechado na peça 2, mesmo dia, ver
abaixo).** CRM reconfirmado sem mudança (51 campos, 50
oportunidades, zero conversa de WhatsApp/SMS real — G-03/G-04 ainda
aguardando o dono) e sweep de coerência de sempre limpo. Seguindo a própria
instrução deste roadmap ("reler o 'por quê estamos esperando' de todo item
represado", o mesmo caminho que já destravou o F-05 em 21/09/2026), reli o
F-06 — o único item numerado do roadmap inteiro, fora do R-14, ainda
etiquetado como "esperando volume real". A razão registrada não era bem
essa: `WebSearch` achou o gatilho nativo `Transcript Generated` (duração de
chamada, LC Phone incluído), que a rodada de 21/09/2026 não tinha achado —
correção da mesma classe da premissa negativa que o F-08 já cometeu duas
vezes na mesma semana. Isso não fecha o item: falta confirmar se a operação
liga por LC Phone (mesma pendência sem resposta do F-08/F-09) e falta
apontar a lista/dashboard de taxa de conexão para o campo novo — as duas
registradas como pendência explícita dentro do próprio F-06, não como lacuna
esquecida. Detalhe completo na entrada acima.

**F-06, peça 2, 22/09/2026, sessão automática seguinte, mesmo dia — item
fechado, e o plano da peça 1 não sobreviveu à execução.** CRM reconfirmado
sem mudança (51 campos, 50 oportunidades, zero conversa de WhatsApp/SMS
real — G-03/G-04 ainda aguardando o dono) e sweep de coerência de sempre
limpo (`grep` por nome de etapa antigo e pelos nomes tocados nesta rodada
— `Conexão real`, `Conexões reais telefone`, seção 8.6, seção 2.17 — em
todo o `wesales/`: toda ocorrência batia com a edição feita). A pendência
que a peça 1 tinha deixado explícita ("apontar a lista/dashboard para
`Conexão real`") não fechou como planejada: a lista 8.6 aceitou o campo
direto, mas o dashboard não — Custom Metrics soma `NUMERICAL`/`MONETARY`,
`Conexão real` é `SINGLE_OPTIONS`, achado que já estava registrado na
própria seção 2.17 desde antes do F-06 existir e que a peça 1 não tinha
cruzado. Pesquisado se um recurso mais novo (filtro por metric-level em
Custom Metrics, lançado depois daquele achado) resolvia sem campo novo:
não — filtra por tag/pipeline/owner, e mesmo que cobrisse campo
personalizado, contaria contatos no estado atual, unidade diferente da
soma cumulativa do outro lado da razão. Saída: terceiro campo,
`Conexões reais telefone` (C-31, `NUMERICAL`, `campos-e-tags.md`),
incrementado por `Math +1` (nó 6 novo em `build-wesales.md`, seção 2.27) —
mesmo padrão dos contadores C-06/C-07/C-11/C-12, e sem o estado vencido que
`Conexão real` sozinho carrega. É a mesma lição que o G-06 já tinha deixado
(reestruturar em vez de multiplicar Template) num formato diferente:
diante de um plano que não serve para os dois destinos, tratar cada um
pela regra que se aplica a ele, não forçar os dois pelo mesmo campo. Com
isso, o F-06 fecha por inteiro — as pendências que restam (gravação/LGPD/
custo, decisão do dono; LC Phone confirmado ou não, mesma do F-08/F-09)
são pré-requisito de operação, não de desenho, e já estavam registradas
antes desta rodada. Com F-06 fechado, todo o bloco 6 (F-01 a F-09) está
`FEITO` ou aguardando decisão do dono (só F-09) — nenhum item numerado
(G/R/F) resta sem dono claro fora de G-03, G-04, F-09 (decisão) e R-14
(volume real de mensagem).

**F-10 aberto em 22/09/2026, sessão automática seguinte — lacuna nova, achada
seguindo a mesma instrução de sempre ("reler o 'por quê estamos esperando'" e,
sem nada represado para destravar, "procurar lacuna nova").** Com o bloco 6
inteiro fechado ou aguardando o dono, a pergunta que sobrou foi generalizar o
próprio F-05: se seis monitores cobrem "lead que ficou parado", existe alguma
falha que nenhum deles cobre? Sim — "lead que nunca chegou", achada ao medir
por API que a subconta estava, naquele momento, ~22h sem nenhum contato novo
(a rodada de abertura escreveu por engano "~46h"; conta corrigida na sessão
seguinte, junto com um registro novo em `APRENDIZADOS-CRM.md` sobre a classe
de erro — aritmética manual sobre datas, não fonte externa). Especificados
dois widgets de Custom Metrics e uma Smart List equivalente, todos usando
contagem de contatos por filtro (a mesma capacidade que a peça 2 do F-06
tinha rejeitado para outro uso). O alerta automático de ausência (opção "b")
não foi especificado — é engenhoca com custo próprio, decisão do dono. Zero
campo, zero tag, zero escrita no CRM: item de especificação pura.

**Sessão automática seguinte, mesma data — correção de aritmética, não de
desenho:** conferido de novo por API (50 contatos, 50 oportunidades, mesmo
`Carlos Andrade` como lead mais novo — a entrada segue parada, agora mais de
22h e subindo), a rodada recalculou o intervalo entre as duas datas que a
própria tabela do F-10 já trazia e achou que "~46 horas" não batia com elas
— o correto era ~22h13min no momento em que foi escrito. Corrigido nos quatro
arquivos onde o número errado tinha se propagado (aqui, `APRENDIZADOS-CRM.md`,
`briefing-sdr.md`, `build-wesales.md`). A conclusão do item não muda: a
entrada continua parada e nenhum monitor cobre isso — só a magnitude do
"há quanto tempo" estava errada.

Com isso, nenhum item numerado (G/R/F) resta sem dono claro fora de G-03,
G-04, F-09 e F-10 (todos aguardando decisão do dono) e R-14 (volume real de
mensagem).

**F-10, sessão automática seguinte, mesma data (22/09/2026) — especificação
fechada por inteiro, item continua aguardando o dono.** Reler o "por quê
estamos esperando" de F-10 (a própria instrução desta seção) achou que a
espera não era total: os dois widgets do dashboard já estavam prontos, mas
a Smart List equivalente — citada só em prosa aqui, nunca como seção
numerada em `build-wesales.md` — não existia onde a Fase 6 do
`GUIA-MONTAGEM.md` de fato procura. Fechada como seção 8.25, com
referência cruzada na 2.17. Não muda a fila: o que falta em F-10 continua
sendo só a decisão do dono sobre o alarme (opção b), a mesma pendência que
G-03, G-04 e F-09 já têm. CRM reconfirmado sem mudança (51 campos, 50
oportunidades) — a entrada segue parada, agora com quase 24h de silêncio
(era ~22h47min na conferência anterior).

**R-14, sessão automática seguinte, mesma data (22/09/2026) — especificação
fechada, execução segue esperando volume real.** CRM reconfirmado sem
mudança via API (51 campos, 50 oportunidades — 47 `NOVO LEAD` + 2
`NEGOCIAR` + 1 `lost` de teste; `conversations_search-conversation`
confirma as mesmas 4 conversas outbound de sempre, DMs pessoais de
Instagram, zero mensagem de cadência real) — nada para o sweep de
coerência de sempre corrigir, e G-03/G-04/F-09/F-10 seguem parados
esperando o dono, sem novidade. Seguindo a própria instrução desta seção
("reler o 'por quê estamos esperando' de todo item represado"), a releitura
caiu sobre o único item do roadmap que ainda não tinha nó nenhum desenhado
— R-14, que dizia "espera volume real" desde a primeira versão do
documento sem nunca separar o que da espera é **execução** (precisa de
mensagem real para auditar) do que é **desenho** (não precisa). A segunda
metade não precisava esperar nada, e não tinha sido feita. Fechada agora:
duas Smart Lists novas (`build-wesales.md`, seções 8.26/8.27) cruzando a
tag `nao-perturbe` com os filtros nativos de DND por canal (`Calls &
Voicemails DND`, `WhatsApp DND`) — achado de pesquisa desta rodada, nunca
citado em nenhum documento do projeto antes. A metade "janela de envio" do
"Como" original já estava coberta sem item próprio (toda seção que manda
mensagem já declara `Janela de envio` na sua tabela de configuração,
conferido por `grep`). Zero campo, zero tag, zero escrita no CRM: item de
especificação pura, não depende de `APROVADO.md`. Detalhe completo na
entrada do R-14 acima.

Com isso, nenhum item numerado (G/R/F) resta sem especificação nem sem
dono claro: G-03, G-04, F-09 e F-10 esperam decisão do dono; R-14 tem
desenho completo e espera a operação mandar a primeira mensagem real para
executar o que já está pronto na documentação.
