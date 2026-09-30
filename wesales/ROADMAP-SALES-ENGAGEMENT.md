# O que falta para virar Reev/Meetime de verdade

> ## ⚠️ Alerta de integridade — 27/09/2026, ROADMAP e `build-wesales.md` reconciliados por inteiro (histórico abaixo, mantido para quem chegar depois)
>
> **O que aconteceu:** três commits com o mesmo título ("Add GitHub Action for
> WeSales G03", 24/09/2026 15:22–15:25 BRT) sobrescreveram este arquivo e
> também `build-wesales.md` com uma cópia local desatualizada. Confirmado
> lendo os blobs de cada commit (`git show <hash>:wesales/ROADMAP-SALES-
> ENGAGEMENT.md | wc -l`), não suposto: a truncagem deste arquivo aconteceu
> no commit `33b4ae3` (5.619 → 1.357 linhas — `G-05` a `G-24`, `R-18` e
> `F-07` a `F-15` inteiros desapareceram, e `F-06`/`R-14`/`R-17` voltaram a
> um estado anterior ao próprio fecho real de 22/09/2026); a de
> `build-wesales.md` aconteceu antes, no commit `c2dadb5` (8.580 → 4.349
> linhas). Ninguém notou por 3 dias, e pelo menos uma sessão seguiu editando
> a versão já truncada — a promoção do G-03 (abaixo) é trabalho real feito
> depois do acidente, e só existia nessa cópia curta.
>
> **Reconciliado nesta sessão (27/09/2026), só este arquivo.** Base: commit
> `6821497`, a última versão íntegra (5.619 linhas) imediatamente anterior à
> truncagem. Por cima dela, dois pedaços de trabalho real que só existiam na
> versão truncada: o G-03 promovido/executado (24/09) e o item novo desta
> sessão sobre `monetaryValue`, que nasceu como "F-07" sem saber que o número
> já era de outro item (o de reputação do WhatsApp, agora restaurado) —
> renumerado para **F-18** (F-16 e F-17 já estão em uso em `build-wesales.md`
> e citados em cinco outros documentos). Conferido depois de montar: todo
> cabeçalho `### G-`/`R-`/`F-\d+` deste arquivo aparece uma única vez, sem
> duplicata.
>
> **Atualização de 27/09/2026, sessão seguinte — peça 1 de `build-wesales.md`
> reconciliada; peça 2 continua aberta.** As seções inteiras que tinham
> desaparecido (§2.25 a §2.44 — as specs de F-06 a F-17, dos scripts de
> auditoria e de nove achados técnicos sem número de roadmap próprio, tipo
> `patch_canal_conectou.py` e o alarme falso do portão de capacidade — mais
> §4.1 e §5.5, que a leitura anterior não tinha listado por nome) foram
> coladas de volta a partir do commit `875d8d7` (última versão íntegra) para
> as posições exatas onde ficavam antes da truncagem, e conferidas
> byte-a-byte contra a base depois de coladas — nenhuma delas tinha edição
> real por cima na cópia truncada (`git log 875d8d7..HEAD -- wesales/
> build-wesales.md` só mostra §2.45/§2.46/§2.47 sendo tocadas, todas depois
> do fim de §2.44), então colar de volta aqui não arriscava apagar trabalho
> novo. §2.45 a §2.47 permanecem intactas, no fim do arquivo, como já
> estavam.
>
> **Peça 2, maior do que parecia (achado original, seção 1 já reconciliada
> abaixo):** as seções que "sobreviveram" à truncagem (1, 2, 2.9 a 2.24, 3,
> 4, 5, 5.1 a 5.4, 6, 7, 8, 9, 10, 11) tinham conteúdo interno perdido, de
> quase intacta (seção 11, ~99% do texto original) a mais da metade perdida
> (seção 6, ~39%) — e **não é um corte limpo**: a seção 1 tinha uma colisão
> de verdade, não só perda — a
> base (`875d8d7`) tem "### 1.4 Workflow "Reentrada por Formulário" — F-11"
> (fechado em 22/09/2026); a cópia truncada, editada depois do acidente,
> tinha "### 1.4 G-03 — promoção imediata escolhida pelo dono em 24/09/2026"
> no mesmo número — uma sessão que não sabia que 1.4 já existia (porque a
> cópia truncada não o tinha) reusou o número para um trabalho real e
> diferente.
>
> **Seção 1 reconciliada em 27/09/2026, sessão seguinte.** Diff parágrafo a
> parágrafo (não colagem, por causa da colisão): a seção 1 da base foi colada
> por inteiro — conferido byte a byte, 495 linhas idênticas — e o G-03 (que
> teria sido apagado por uma colagem direta) foi preservado como `### 1.5`,
> logo depois do F-11 restaurado em `1.4`. Nenhum outro documento cita a
> seção 1.4 de `build-wesales.md` referindo-se ao G-03 (conferido por
> `grep -rn "seção 1.4" wesales/` — as duas ocorrências fora deste arquivo já
> apontavam para o F-11); só este alerta precisava de correção, feita no
> mesmo commit. Mesmo tratamento que este roadmap já deu ao F-07→F-18 quando
> achou a mesma classe de colisão de número aqui.
>
> **Peça 3, fechada em 27/09/2026, sessão seguinte — as 13 seções/grupos que
> ainda "sobreviviam" à truncagem (2, 2.9 a 2.24, 3, 4, 5, 5.1 a 5.4, 6, 7, 8,
> 9, 10, 11) foram reconciliadas por inteiro.** Método: split automático de
> `875d8d7` (base íntegra) e do HEAD por cabeçalho `## `, comparação campo a
> campo (não só contagem de linha) para não repetir o erro que a peça 2 quase
> cometeu — quatro seções (2.16, 2.21, 5.1, 9) tinham a **mesma contagem de
> linhas** nas duas versões e ainda assim conteúdo diferente: a cópia truncada
> carregava texto mais antigo que o próprio `875d8d7` (ex.: seção 2.16 ainda
> chamava a etapa de `AGENDAR`, não `REUNIÃO DE DIAGNÓSTICO`), confirmando que
> o acidente de 24/09 não cortou só o final do arquivo — substituiu por uma
> cópia local que já estava desatualizada antes da truncagem. As 29 seções
> divergentes foram coladas inteiras a partir da base; nenhuma tinha edição
> real por cima na cópia truncada (`git log 875d8d7..HEAD -- wesales/
> build-wesales.md` mostra só `ab83d6c`/`145262d`/`7ba708d`/`5fe7110`/
> `2d880c3` tocando este arquivo, e nenhum hunk cai dentro do intervalo de
> linhas destas 13 seções — todos ficam nas seções já reconciliadas ou no
> final do arquivo). Nenhuma colisão de número de subseção nova apareceu
> (`### ` conferido do início ao fim). `build-wesales.md` volta a **8.764
> linhas** (era 8.580 na base, mais o trabalho real de §2.45-§2.47 já
> presente). Sweep de coerência: as referências cruzadas a estas seções em
> `campos-e-tags.md`, `ROADMAP-SALES-ENGAGEMENT.md`, `GUIA-MONTAGEM.md`,
> `CONFERENCIA-CAMPOS.md`, `IMPLEMENTACAO-WORKFLOWS.md`, `briefing-sdr.md`,
> `script-de-ligacao.md`, `AGENTE-IA-CONEXAO.md` e `APRENDIZADOS-CRM.md`
> citam só o número da seção (2.16, 2.21, 5.1, 9/9.1) — nenhuma cola texto
> antigo, então nenhuma ficou inconsistente; a restauração as torna mais
> corretas, não menos, porque agora apontam para conteúdo completo em vez de
> truncado. Zero campo, zero tag, zero escrita no CRM. Com isto, os dois
> documentos que o acidente de 24/09 atingiu (`ROADMAP-SALES-ENGAGEMENT.md`,
> fechado na atualização anterior, e `build-wesales.md`, fechado agora) estão
> reconciliados por inteiro — não sobra trabalho de restauração represado
> desta família.

> **Aviso de 22/09/2026 — o canal WhatsApp saiu do projeto.** Decisão do dono:
> as quatro réguas são 100% telefone, remontadas e publicadas em `d52e61d`.
> As 11 menções a WhatsApp/`fila-wa` abaixo são registro histórico. Dois itens
> deste roadmap mudam de tamanho por causa disso: o que dependia de Templates
> do Meta/WhatsApp deixa de ser caminho crítico, e a aplicação ao
> **`Origem Verificada`** sobe de prioridade, porque tirar um canal dobra
> aproximadamente o volume de ligação por lead — exatamente o que o Despacho
> Decisório nº 82/2026 avalia. Detalhe e medição: seção 2.5 do
> `build-wesales.md`.

> **Atualização de 23/09/2026 — este aviso já não é a última palavra do dono
> sobre canal.** No mesmo dia 22/09, horas depois do aviso acima,
> `wesales/PLANO-MULTICANAL.md` (decidido ao vivo pelo dono, "aplique todas
> as recomendações… ajuste de ponta a ponta") reintroduz o WhatsApp como
> canal de cadência — D5: ligação por WhatsApp (Stevo Voice) e ligação normal
> como os dois canais de toque, D6: WhatsApp primeiro, vira ligação normal
> depois de 3 ligações de WhatsApp seguidas sem atender. O texto do D5 já
> nomeia o mesmo achado técnico que fechou o G-09 abaixo (a mensagem
> automática de WhatsApp sai pela ação "SMS" do GHL via Stevo) — o dono
> decidiu usar esse transporte de propósito, não por engano. `PLANO-
> MULTICANAL.md` também renomeia a etapa `AGENDAR` para `REUNIÃO DE
> DIAGNÓSTICO` (mesmo `id`, confirmado por API em 23/09) e reformula boa
> parte da Cadência 12x30/Pós-ligação/Pós-agendamento (D2–D9). A maior parte
> dessas mudanças segue sem propagar para este roadmap nem para
> `build-wesales.md` — os itens G/R/F já registrados abaixo continuam
> descrevendo o desenho "100% telefone" pré-`PLANO-MULTICANAL`, e a execução
> real (`PLANO-MULTICANAL.md`, checklist E1-E14) está rodando por fora,
> pela API interna (`wesales/tools/`), não pelo `GHL CRM` (MCP) que esta
> rotina usa. Antes de fechar qualquer G/R/F novo que toque canal ou etapa,
> checar `PLANO-MULTICANAL.md` primeiro — é a decisão mais recente do dono,
> não este aviso. **Exceção, fechada em 23/09/2026 (G-12, abaixo):** a
> migração de texto do nome da etapa (`AGENDAR` → `REUNIÃO DE DIAGNÓSTICO`)
> está completa — `build-wesales.md` (seção 1 na peça 1, seções 2 em diante
> na peça 2) e este roadmap não tratam mais `AGENDAR` como etapa corrente em
> nenhuma citação nova; toda ocorrência que resta é nota histórica datada
> (descrevendo o nome como era no momento em que o item foi escrito) ou nome
> próprio publicado na tela (o workflow `AGENDAR Estagnado`, a lista
> `Saúde — AGENDAR Estagnado`).

> ## ✅ G-25 — risco de disparo em massa na abertura, resolvido pelo dono ao vivo (27/09/2026, ver detalhe abaixo)
>
> **36-37 execuções da `Cadência Inbound` estavam paradas no nó 24 (`WhatsApp ·
> MI-0`) e disparariam juntas quando a janela do workflow abrisse — próxima
> abertura segunda 28/09 08:30 `America/Sao_Paulo` (11:30 UTC).** O dono
> resolveu ao vivo, entre 27/09 ~20h e ~21h UTC, por uma sessão com acesso a
> navegador logado (branch `abertura-operacao-dnd-n7dnjv`, fora deste
> histórico de sessões automáticas): não pela janela do workflow, e sim
> liberando os 31 contatos protegidos (`dnd` para `false`) e recalculando a
> `Prioridade` deles para 4, o que o governador de envio (fila por
> prioridade, mesmo campo do C-05) já respeita — a mesma proteção de volume
> por outro mecanismo. Confirmado por leitura independente desta sessão
> (`contacts_get-contact` em 14 dos 31 contatos, todos com `dnd: false` e
> `Prioridade: 4`, `dateUpdated` entre 21:04:39 e 21:04:50 UTC de 27/09).
> Detalhe completo, inclusive a descoberta de que outras três sessões/branches
> trabalham a mesma subconta em paralelo: **G-25**, abaixo.

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

### G-03 · L-07 deixou de ser lacuna teórica — promoção imediata escolhida em 24/09/2026 — **especificação fechada em 24/09/2026, execução agendada para 29/09/2026**
**Agendamento operacional (24/09/2026):** a execução idempotente foi
agendada no Windows para **29/09/2026 às 08:00
(`America/Sao_Paulo`)**. A limpeza de tarefas permanece report-only porque a
API pública não oferece endpoint normal de atualização/conclusão de tarefas.
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
**Decisão escolhida e estado (24/09/2026):** opção 2, promoção imediata,
sem espera. O workflow usa o gatilho `Opportunity Stage Changed` entrando
em `NOVO LEAD` e a ação `Create/Update Opportunity`, com status `open` e
etapa `CONECTAR`. O builder é offline e não houve escrita no CRM. O JSON
está em `workflows-json/Promover NOVO LEAD para CONECTAR.json`; publicar e
promover continuam bloqueados em `APROVADO.md` até a Cadência 12x30 ser
publicada e testada. A ordem obrigatória é: publicar/testar Cadência,
publicar este workflow, promover estoque e conferir T1. O evento não
reprocessa oportunidades existentes; o estoque exige backfill manual.
**Execução real em 24/09/2026:** a Cadência 12x30 foi confirmada como
`published` antes da ação e o backfill oficial foi executado. Das
oportunidades em `NOVO LEAD`, 41 `open` foram promovidas para `CONECTAR`;
9 permaneceram em `NOVO LEAD` por status fechado (8 `abandoned`, 1 `lost`).
Nenhuma oportunidade `closed` foi alterada. A verificação final de
`CONECTAR` totalizou 45 oportunidades (38 `open`, 7 `lost`). O workflow
futuro **Promover NOVO LEAD para CONECTAR** não foi criado, pois a criação
de workflow pela API oficial não foi estabelecida.

**Automação operacional:** o runner está definido em
`.github/workflows/wesales-g03.yml`, no repositório, com execução diária às
08:00 (`America/Sao_Paulo`) e `GHL_PIT` como secret de repositório. Isso
remove a dependência do PC; a execução continua protegida pela janela de
tempo e só muta o CRM em 29/09/2026. Não publicar nem executar agora.
**Histórico — três alternativas consideradas:**
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

**Pronto quando:** a Cadência 12x30 estiver publicada e testada, a
autorização específica virar `[x]` em `APROVADO.md`, e então o workflow for
publicado, o estoque promovido e o T1 conferido.

### G-04 · O formulário do Meta grava em campo que a régua não lê, e grava valor que o campo não aceita — **FEITO: peça 1 (Prazo/Urgência) resolvida em 22/09/2026 sem decisão; peça 2 (Investimento mensal) fechada em 27/09/2026 pelo próprio dono, ver G-33**

> **Atualização de 22/09/2026, sessão automática — o item se dividiu em duas
> peças de tamanho e urgência diferentes, e só uma segue bloqueada.** No PC do
> dono (`dec3a20`), ao montar o Pós-agendamento v2, a metade `Prazo`/`Urgência`
> deste item foi resolvida sem esperar a escolha entre Opção A e Opção B: como
> os rótulos de `Prazo` e `Urgência` são **idênticos**, a régua ganhou um bloco
> de reserva que lê `Urgência` com a mesma tabela de pontos sempre que `Prazo`
> vier vazio — sem remapear os 8 formulários do Meta, sem decisão de negócio,
> só estrutura (`wesales/tools/regua_qualificacao.py`). Publicado e provado
> rodando: **93 leads pontuaram por `Prazo`, 15 pelo bloco de reserva
> `Urgência`** (`GUIA-MONTAGEM.md`, "Estado final em 22/09/2026"). Isso fecha
> o Bloco C (BANT) do item — a régua não perde mais os 15 pontos de `Prazo`
> para lead do Meta. **O que resta é só a linha `Investimento mensal em
> anúncios`, Bloco B**, que o mesmo mecanismo não resolve: os valores que o
> Meta grava (`Abaixo de 5k`, `Até R$ 1.000`, `Não invisto nada ainda`) não são
> os rótulos das opções da tela (`5k a 10k`, `1k a 5k`, `Até 1k`) — não é um
> problema de "campo errado" como `Prazo`/`Urgência` era, é valor fora da
> lista, e só se resolve mudando a opção do campo (Opção A) ou comparando por
> texto parcial em vez de igualdade (Opção B), as duas decisão do dono. Detalhe
> em `build-wesales.md`, seção 9.1, Bloco B.

> **Evidência nova em 22/09, e ela reforça a Opção B** (`CONFERENCIA-CAMPOS.md`,
> Tabela M): o contato de teste que o Meta injeta guarda o **texto literal de
> cada pergunta** como placeholder, no campo que ela alimenta. O formulário maior
> (`2412763482587375`, 42 atribuições, `formName` real **`O PROXIMO CLIENTE FORMS
> v1`**) pergunta `quando_você_pretende_resolver_isso?` → grava em `Urgência`, e
> `o_que_você_busca_hoje?` → grava em `Necessidade`. Pelo texto, as duas **são**
> `Prazo` e `Dor principal` — os campos que a régua lê e que o script manda o SDR
> preencher. Ou seja: não é um formulário mal configurado, é a nomenclatura de
> quem montou os oito, e por isso corrigir na origem custa oito vezes (e o nono
> nasce errado) enquanto fazer a régua ler onde o dado já cai resolve de uma vez.
> Bônus de método: `attributionSource.formName` vem em todo contato, então dá para
> nomear os outros sete formulários sem abrir o Gerenciador de Anúncios.

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
**Pronto quando (revisado em 28/09/2026 — as duas peças fecharam, nenhuma
segue aberta):** `Prazo`/`Urgência` fecharam sem decisão em 22/09/2026
(peça 1, acima — bloco de reserva publicado e provado). A peça 2
(`Investimento mensal em anúncios`) fechou em 27/09/2026, mas não pela
Opção A nem pela Opção B que este item chegou a desenhar — o dono aplicou
uma terceira saída direto no `Pós-agendamento v2` (v17→v18, fora deste
conector): ramos extras por igualdade exata com o texto literal que o Meta
grava (`Abaixo de 5k` pontua como `1k a 5k`, `Até R$ 1.000` como `Até 1k`,
os três valores pagos de `Investe em anúncios` como `Sim`), sem remapear
os 8 formulários (Opção A) nem trocar a régua inteira para `Contains`
(Opção B). Detalhe completo em **G-33**, achado por reconciliação de
branch irmã, não por resposta direta às opções A/B — por isso um lead novo
do Meta já pontua o Bloco B inteiro sem depender de qual dos quatro textos
o anúncio grava, sem que `campos-e-tags.md` (Q-06) nem a tabela de opções
da seção 9.1 precisassem mudar (as opções da tela continuam as mesmas
quatro; o que mudou foi a régua aceitar também o texto do Meta como
sinônimo). G-04 sai por inteiro da lista de decisões sem prazo fixo que
esperam o dono — ver G-33 e **G-40** (achado de coerência que corrigiu as
referências a esta decisão que ainda ficaram desatualizadas em outros
documentos).

### G-05 · Mensagens automáticas de WhatsApp especificadas como texto livre, sem checar a janela de 24h — pode falhar em silêncio assim que a cadência publicar — **especificação fechada em 22/09/2026, execução aguarda Templates aprovados pela Meta**
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

### G-07 · O e-mail (canal novo do F-15) herdou a régua de compliance a zero — resposta de opt-out por texto não vira DND sozinha, e a auditoria do R-14 nunca aprendeu a olhar para o canal — **FEITO em 22/09/2026**
**Por quê:** mesmo padrão do G-06 (a guarda de um item mais velho nunca
alcançou o canal mais novo), aqui aplicado a dois itens mais velhos ao
mesmo tempo. (1) O R-17 (21/09/2026) ensinou o projeto a nunca tratar
resposta de texto como sinal cego — antes dele, qualquer resposta de
WhatsApp virava "ligar agora, prioridade 5", incluindo quem respondia
"pare, não me manda mais mensagem". O F-15 (22/09/2026, mesmo dia deste
item) abriu o primeiro canal de texto novo desde então — e-mail — e o
único ponto que manda e-mail (`Resgate por E-mail — Sem Telefone`, seção
2.30) repete a mesma lacuna que o R-17 fechou para WhatsApp: o nó 4/7
(`Wait → Contact Replied`) não olha o conteúdo da resposta, só notifica o
gestor para decidir na mão — sem `nao-perturbe` nem DND aplicados
sozinhos. Não é o mesmo bug (nenhuma tarefa errada nasce daqui), mas é a
mesma classe: "o único jeito de um opt-out virar DND é alguém ler a
mensagem e lembrar de desligar tudo", a frase exata que o R-17 já tinha
usado para justificar por que isso é inaceitável. (2) O R-14 (Auditoria de
compliance, fechado mais cedo no mesmo dia 22/09/2026) criou duas Smart
Lists (8.26/8.27) cruzando a tag `nao-perturbe` com o DND nativo por
canal — mas só cobria `Calls & Voicemails DND` e `WhatsApp DND`, os dois
canais que existiam quando foi escrito. O e-mail nasceu depois, no mesmo
dia, e ninguém tinha voltado para atualizar a auditoria: um lead com
`Email DND` desligado (a única exposição real que falta fechar) passaria
pelas duas listas sem aparecer em nenhuma.
**O que já estava protegido, e não precisou de nada novo (pesquisado antes
de desenhar, `WebSearch`):** todo e-mail enviado pela plataforma nativa do
GHL já sai com um link de descadastro automático no rodapé
(`{{unsubscribe}}`), que aplica opt-out num clique sem depender de nenhum
workflow — cobre LGPD art. 18 (direito de revogar consentimento a
qualquer momento) para quem usa o link. A lacuna real é só a resposta por
**texto**, o mesmo ponto cego que o WhatsApp tinha antes do R-17.
**Como:** especificado nó a nó em `build-wesales.md`. (1) Workflow novo
"Opt-out por Palavra-chave — E-mail" (seção 2.9.6) — mesmo padrão do 2.9.5/
R-17, canal e lista de frases trocados (a mesma lista canônica, reaproveitada
sem alteração porque este workflow não concorre pelo mesmo evento que o
2.9.3/2.9.5, então não precisa da mirror obrigatória que aqueles dois
precisam entre si). (2) Smart Lists 8.26/8.27 (R-14) ganharam a terceira
cláusula, `Email DND`, no mesmo `OU` que já cobria Calls/WhatsApp. (3)
Checklist novo do gestor na seção 2.30: confirmar SPF/DKIM/DMARC do domínio
de envio antes do primeiro disparo real (mesma lógica do F-07/F-08 —
reputação de canal, sem gatilho nativo para ler por workflow) e confirmar
que o template criado por `emails_create-template` manteve o link de
descadastro no rodapé.
**Pesquisado antes de desenhar:** nenhuma das quatro plataformas do
enunciado (Reev, Meetime, Outreach, Salesloft) precisa resolver isto do
jeito que este projeto precisa — o canal principal delas é e-mail desde o
primeiro dia, com unsubscribe padronizado por lei/convenção de mercado
havia anos; aqui o e-mail chegou por último, depois de três canais já
maduros, e herdou menos proteção que os outros três justamente por ser o
mais novo. É a mesma inversão que o G-06 já registrou para a Qualificação
por IA no WhatsApp: o canal mais novo de uma operação tende a ser o menos
protegido, não porque seja mais simples, mas porque as guardas anteriores
foram escritas antes dele existir.
**Zero campo e zero tag novos:** reaproveita `nao-perturbe` (T-06) e o DND
nativo (`Email DND`, já comprovado gravável nesta subconta mesmo antes de
qualquer integração — mesma evidência que a 8.26 já registrou para
WhatsApp). Zero escrita no CRM: item de especificação pura, não depende de
`APROVADO.md` — nem o workflow novo, nem a edição das duas Smart Lists
saem por API. Subconta reconfirmada nesta execução via
`opportunities_search-opportunity`/`locations_get-custom-fields`/
`contacts_get-contacts`/`conversations_search-conversation`: 55 campos, 50
oportunidades (45 `NOVO LEAD` open + 2 `NEGOCIAR` open + 1 `NEGOCIAR` lost
+ 2 `CONECTAR` lost de teste), 50 contatos, `Carlos Andrade` (21/09 09:17)
ainda o lead mais novo — entrada seguia parada há ~36h47min no momento da
leitura, zero mensagem de cadência automática real — G-03, G-04 (peça 2),
F-09 e F-10 seguem aguardando o dono, sem novidade.
**Pronto quando (cumprido):** um lead que responde pedindo para parar de
receber e-mail sai de toda cadência automática com DND ligado no mesmo
minuto, sem depender de o gestor ler uma notificação genérica e agir na
tela; e as duas Smart Lists de compliance do R-14 enxergam os três canais
que a operação de fato usa, não só os dois que existiam quando foram
escritas.

### G-08 · O achado do F-15 apontava uma correção no R-08 e nunca virou mudança nele — nó 2 reativaria lead sem telefone para sempre — **FEITO em 22/09/2026 (especificação)**
**Por quê:** ao medir o F-15 (seção 2.30 do `build-wesales.md`), esta mesma
rodada já tinha escrito a correção que faltava: *"1. Fechar o ciclo continua
necessário e não depende de e-mail. O nó 1 do R-08 precisa distinguir por
que o lead virou `abandoned`: se foi o portão de telefone (tag
`telefone-invalido`)... Portão novo no R-08, antes de reativar."* Isso ficou
registrado dentro do texto do F-15 e nunca virou edição no nó real do R-08
(seção 2.12) — o mesmo padrão de "achado em rodapé, nunca promovido a item
próprio" que este roadmap já viveu duas vezes (F-12, com `Motivo da
desqualificação`; F-13, com o monitor de `NEGOCIAR`). Sem a correção, o nó 2
do Reengajamento 90 dias reativava **qualquer** oportunidade `abandoned` +
`nutricao-90d` sem olhar se o lead tinha telefone — um lead que nunca teve
telefone (a maioria vinda de DM do Instagram, que não coleta telefone nem
e-mail) voltaria para `CONECTAR` a cada 90 dias, rodaria o bloco TR1-TR4
sem nenhum canal capaz de alcançá-lo (a operação é 100% telefone desde
`d52e61d`) e voltaria para `abandoned` + `nutricao-90d` no fim, reabrindo o
relógio sozinho, para sempre — a régua fingindo tentar contato onde já
sabia de antemão que não há como.
**Conferido por API antes de escrever, para não repetir o erro que este
item corrige (agir sobre uma leitura antiga sem reconferir):** a subconta
tem hoje **53 oportunidades reais** (48 `NOVO LEAD` open + 2 `CONECTAR`
lost + 2 `NEGOCIAR` open + 1 `NEGOCIAR` lost) e **zero em `abandoned`** — os
5 leads reais do Instagram que o F-15 mediu como "presos no ciclo" ainda
estão em `NOVO LEAD`, sem nenhum campo de cadência preenchido, porque G-03
(promoção `NOVO LEAD` → `CONECTAR`) segue aguardando o dono e eles nunca
passaram pelo portão 0.0b que aplicaria `telefone-invalido`/`nutricao-90d`.
**O ciclo não é estrago ativo hoje — é uma armadilha armada, ainda não
disparada:** dispara no instante em que G-03 for decidido e um lead sem
telefone (destes 5 ou de qualquer origem futura, inclusive a nova integração
de WhatsApp não oficial que já criou 3 contatos de teste nesta mesma
sessão) entrar em `CONECTAR` e esgotar o que a cadência sem telefone
conseguir tentar. Corrigir agora, antes do primeiro lead real cair nesse
buraco, é mais barato que corrigir depois de um lead já ter dado três voltas
de 90 dias sem nenhuma tentativa — o mesmo raciocínio que já tirou F-04 e
F-05 da fila normal.
**Como:** especificado nó a nó em `build-wesales.md`, seção 2.12 — o nó 2
(portão) ganhou a quarta condição **E** `tag telefone-invalido ausente`; o
nó 2b (ramo falso) ganhou o terceiro motivo na explicação. Espelhado em
`IMPLEMENTACAO-WORKFLOWS.md`, W16. **Achado à parte, corrigido junto por
estar na mesma linha:** o nó 3 (reset de rodada) ainda escrevia `Entrada em`
= `{{right_now}}`, o valor que grava `[object Object]` em campo `TEXT`
(`APRENDIZADOS-CRM.md`) — só que o workflow **já foi corrigido ao vivo**
para `{{right_now.date}} {{right_now.time}}` por um patch cirúrgico do PC do
dono (`tools/patch_relogio_cadencias.py`, mesmo dia), e a documentação nunca
foi atualizada para bater com o que está publicado. Os dois arquivos agora
refletem o valor real em produção.
**Pesquisado antes de desenhar:** nenhuma das quatro plataformas do
enunciado (Reev, Meetime, Outreach, Salesloft) documenta publicamente uma
proteção equivalente — o cenário "cadência de reativação corre para sempre
sobre um lead que a própria plataforma já sabe ser incontatável por aquele
canal" é específico de uma régua 100% telefone com canal de entrada que não
garante telefone (DM do Instagram), combinação que nenhuma delas assume por
padrão.
**Zero campo, zero tag novos:** reaproveita `telefone-invalido` (T-09), já
criada desde a R-13. Zero escrita no CRM: item de especificação pura, não
depende de `APROVADO.md`.
**O que este item não resolve:** é correção de spec, não de dado — o
workflow `Reengajamento 90 dias` já está **publicado** na tela
(`GUIA-MONTAGEM.md`, "Estado final em 22/09/2026", 105 nós), então a
correção do nó 2 precisa do mesmo tipo de patch cirúrgico já usado para o
relógio; não sai por este conector (sem endpoint de workflow) nem pela API
interna desta sessão (sem bearer local — `wesales/tools/ghl_api.py` exige
`.local/_ghl_bearer.txt`, ausente nesta sessão da nuvem). Fica registrado
como retoque pendente, mesmo padrão já usado para o nó 5b da Interceptação
de Sinal.
**Pronto quando (cumprido, na especificação):** o nó 2 do R-08 não reativa
mais nenhuma oportunidade `abandoned`+`nutricao-90d` que carregue
`telefone-invalido` — falta só aplicar o mesmo patch cirúrgico ao workflow
já publicado, mesma fila de retoques manuais do resto do projeto.

### G-09 · O único WhatsApp que esta subconta tem entrega mensagem como SMS por baixo — e todo gatilho que protege o lead (R-17) escuta "Canal: WhatsApp" — **FEITO em 23/09/2026 (especificação)**

> **Conferido em 23/09/2026 — a medição do G-09 tem uma segunda consequência,
> e ela é de decisão do dono, não de gatilho.**
>
> O G-09 resolve o lado técnico (o filtro precisa escutar SMS além de
> WhatsApp). O lado que ficou sem puxar: **o canal reconectado como "WhatsApp"
> é, por baixo, o mesmo canal que o dono removeu do projeto.**
>
> `APROVADO.md`, linha de Mensagens: *"SMS saiu por decisão do dono em
> 19/09/2026 — **não é canal de contato com lead neste projeto**"*, e a linha
> segue `[ ]` até hoje. A integração Stevo entrega `TYPE_CUSTOM_SMS` e só
> troca o rótulo na tela. Então, na prática:
>
> | O que a tela mostra | O que sai | O que o dono decidiu sobre isso |
> |---|---|---|
> | "WhatsApp QR, conectado" | SMS | removido do projeto em 19/09, linha ainda `[ ]` |
>
> **Três coisas dependem disso, e nenhuma é óbvia olhando a tela:**
>
> 1. **A régua multicanal (caminho B).** Os textos `MT1`/`MT4`/`MT11` foram
>    escritos como "WhatsApp (SDR envia)". Se saem por esse canal, o SDR está
>    mandando **SMS** — canal excluído por decisão, e com tarifa de SMS
>    (`twilioRebilling` ativo na subconta), não de WhatsApp.
> 2. **O agente de IA (`AGENTE-IA-CONEXAO.md`).** O desenho supõe conversa de
>    WhatsApp/DM. Se o canal da IA v2 for esse, o agente conversa **por SMS**:
>    outra experiência, outro custo por mensagem e outras regras de
>    consentimento. A pergunta que o G-09 levantou — se o filtro "WhatsApp" da
>    IA v2 reconhece `TYPE_CUSTOM_SMS` — decide também **em que canal o agente
>    fala**, não só quais gatilhos disparam.
> 3. **O risco de banimento que registramos ontem muda de natureza.** "API não
>    oficial de WhatsApp pode banir o número" vale para tráfego de WhatsApp.
>    Se o tráfego é SMS, o risco de banimento do WhatsApp não se aplica — mas
>    entram no lugar as regras de SMS (custo por segmento, opt-out por STOP,
>    e o fato de SMS ter sido descartado como canal).
>
> **Não é conserto automático: é decisão.** Ou o dono reabre o SMS como canal
> (e a linha do `APROVADO.md` vira `[x]`, com a tarifa aceita), ou o caminho B
> e o agente precisam de um canal que não seja este. O que não dá é seguir com
> a tela dizendo "WhatsApp" e a operação mandando o canal que ele tirou.
**Por quê:** reconferindo a base por API nesta rodada (23/09/2026, ~00h UTC):
**54 oportunidades** (49 `NOVO LEAD` open + 2 `CONECTAR` lost + 2 `NEGOCIAR`
open + 1 `NEGOCIAR` lost), 55 campos de contato, mesmas 5 etapas do `FUNIL DE
VENDAS` — e **4 contatos novos** desde a última leitura registrada
(`APRENDIZADOS-CRM.md`, "GHL não-oficial (QR) já está recebendo mensagem real
de teste", 22/09 22h56 UTC, que tinha contado 3): `Sem Nome` (22:34:40 UTC),
`O Próximo Cliente` (22:54:09), `Pablo Sampaio` (22:56:02) e, o que aquela
nota ainda não tinha, `Francisca` (23:34:36) — os quatro com `createdBy.source
= INTEGRATION`, `channel = OAUTH`, mesmo `sourceId`
`682cd9287059b4173d8b17bd-mawx7is9` (a integração Stevo/QR que o dono
conectou em 22/09/2026), os quatro sem `source` nem atribuição de anúncio
(diferente de todo lead do Meta), e os quatro com oportunidade própria em
`NOVO LEAD`, criada pela Porta de Entrada (G-01) em segundos — confirmando de
novo, com um caso a mais, que o portão "qualquer origem" continua pegando
tráfego que não existia quando foi desenhado. Isso já estava registrado como
aprendizado; o que esta rodada acrescenta é o motivo técnico de um risco
maior escondido atrás do mesmo fato. A conversa do contato `Francisca`
(`conversations_search-conversation`, id `5Iy866hqiTZ4TFe34Bew`) mostra
`lastMessageType: TYPE_CUSTOM_SMS` — não `TYPE_WHATSAPP` — batendo com o que
`APRENDIZADOS-CRM.md` já tinha achado por outra via ("a conexão da Stevo usa
o canal de SMS do GHL... a Stevo tem um script que só troca o rótulo 'SMS'
por 'WhatsApp QR' na tela"). Ou seja: o único WhatsApp que esta subconta tem
hoje **não é** o tipo nativo que um filtro "Canal: WhatsApp" foi feito para
reconhecer — é SMS por baixo, com rótulo trocado só na tela. E dois
workflows críticos de compliance filtram exatamente esse canal por nome: o
2.9.3 (Interceptação de Sinal — Resposta) e o 2.9.5 (Opt-out por
Palavra-chave, R-17) — ambos `Customer Replied` — **Canal: WhatsApp**.
Pesquisado nesta rodada (`WebSearch`, confiança média — documentação e
blogs de terceiros sobre o gatilho `Customer Replied`, não testado nesta
subconta): a lista de canais do filtro "Reply Channel" é um conjunto fixo —
SMS, Email, Calls, Voicemail, Live Chat, WhatsApp, Facebook, Instagram, GBP —
sem nenhuma categoria própria para "Custom SMS Provider"/canal customizado.
Se "WhatsApp" nesse filtro corresponde ao canal nativo (API oficial da Meta,
`TYPE_WHATSAPP`) e não a `TYPE_CUSTOM_SMS`, então **nenhuma resposta que chega
pela Stevo dispara o 2.9.3 nem o 2.9.5** — e é o único canal de texto
conectado nesta subconta. Consequência prática, se confirmar: um lead que
responder "pare de mandar mensagem" pelo número que o dono conectou não
aciona o DND automático que o R-17 existe para garantir; o único jeito de
virar DND seria o SDR ler a conversa na mão e lembrar de desligar tudo —
exatamente o cenário que o R-17 foi escrito para eliminar, e que o G-06/G-07
já mostraram se repetir toda vez que um canal novo chega depois da guarda
ter sido escrita. Diferente do G-06/G-07 (canal novo que a documentação nunca
tinha visto), aqui é mais estreito: o canal já era WhatsApp na intenção do
projeto o tempo todo — o que mudou é o transporte por baixo dele, que
nenhuma rodada tinha olhado até a Stevo começar a gerar tráfego de verdade.
**Não é certeza de tela** (mesma classe de confiança "média" que o G-05 já
usa para peças do WhatsApp) — falta abrir o construtor de workflow e ver qual
rótulo o filtro `Reply Channel` mostra para uma resposta já recebida pela
Stevo; é a mesma pendência de verificação que o G-05 (Templates Meta) e a
seção 8.26/8.27 (abaixo) já carregam sem bloquear a especificação.
**Como:** correção aditiva, não substitutiva — reduz o risco mesmo se a
suposição acima estiver errada. Em todo `Customer Replied` que hoje filtra só
`Canal: WhatsApp` (2.9.3, 2.9.5, e qualquer nó `Conversation AI`/ação de
canal WhatsApp que a Qualificação por IA — seção 6 — ou o Agente de IA
`Conexão — Inbound` — `AGENTE-IA-CONEXAO.md` — vierem a usar), acrescentar
**SMS** como segundo canal aceito no mesmo filtro, sem tirar WhatsApp: cobre
os dois cenários possíveis (WhatsApp nativo, se um dia for conectado, e
Custom SMS da Stevo, que é o que existe hoje) até a tela confirmar qual
rótulo é o certo. Aplicado nesta rodada aos dois pontos que já existem em
`build-wesales.md` (2.9.3, 2.9.5); a Qualificação por IA (seção 6) e o
Agente de IA ainda não estão publicados nem totalmente especificados quanto
a canal de escuta — ficam com a mesma nota, para quem montar decidir com a
tela na frente. Cruza com o R-14 (seção 8.26/8.27, "O filtro `WhatsApp DND`
pode não existir nesta subconta hoje"): aquele texto parte da premissa "esta
subconta não tem WhatsApp integrado", verdadeira até 21/09/2026 — desde
22/09/2026 tem, via Stevo. Não muda a conclusão prática dali (checar na tela
se o filtro aparece), mas a premissa escrita ficou desatualizada; corrigida
nesta rodada com uma frase, sem reabrir a análise.
**Zero campo, zero tag novos:** é edição de filtro de gatilho, não de dado.
Zero escrita no CRM: item de especificação pura, não depende de
`APROVADO.md` — a edição em si não sai por API (workflow não é editável por
este conector), então o "Como" acima é o que orienta a montagem manual.
**Pronto quando (cumprido, na especificação; montagem manual pendente como
sempre):** 2.9.3 e 2.9.5 escutam WhatsApp **e** SMS no mesmo filtro; a
premissa desatualizada do R-14 sobre WhatsApp não integrado está corrigida;
fica registrada a pendência de confirmar na tela qual rótulo a Stevo usa,
para quem montar decidir sem achismo.

### G-10 · Duas trilhas de execução deste projeto param de se ver — `PLANO-MULTICANAL.md` reformula canal e etapa sem cruzar com o roadmap principal — **FEITO em 23/09/2026 (coerência entre documentos)**
**Por quê:** todo item numerado deste roadmap (G/R/F) estava fechado ou
represado por decisão do dono — nenhum executável hoje por este conector.
Seguindo a própria instrução deste documento para uma sessão sem tela e sem
decisão desbloqueada (varredura de coerência antes de procurar lacuna nova),
o cruzamento entre `git log` e o estado ao vivo da subconta (API) achou uma
segunda trilha de trabalho que nenhum G/R/F cita: `wesales/tools/` (~30
scripts que falam com a **API interna** da HighLevel, não com o MCP `GHL
CRM` que esta sessão usa) e `wesales/PLANO-MULTICANAL.md`, um plano de
reformulação inteiro commitado direto pelo dono em 22/09/2026 ("aplique
todas as recomendações… ajuste de ponta a ponta") — 22 minutos **depois**
do commit que fechou o G-09 acima. O plano novo (D1-D14, checklist E1-E14)
renomeia `AGENDAR` para `REUNIÃO DE DIAGNÓSTICO` (confirmado por API: mesmo
`id`, já renomeado na tela), reintroduz WhatsApp/Stevo como canal (D5/D6 —
resposta de fato à pergunta que o próprio G-09 levantou sobre o transporte
SMS por baixo do Stevo) e reformula Cadência 12x30/Pós-ligação/
Pós-agendamento. Nada disso estava citado aqui nem em `build-wesales.md`:
uma leitura só destes dois documentos concluiria, errado, que o aviso
"100% telefone" (topo deste arquivo) e a etapa `AGENDAR` seguem valendo.
**Como:** sem reescrever nenhum dos dois desenhos por inteiro (trabalho
grande demais para uma rodada, e não é o que este achado pede) — notas
cruzadas datadas: topo deste arquivo (aponta para `PLANO-MULTICANAL.md`
como decisão mais recente), `build-wesales.md` seção 1.0 (segunda
renomeação de etapa, mesmo `id`), `APROVADO.md` (linha do SMS/WhatsApp,
sinalizando que a premissa mudou sem tocar no `[ ]`), `campos-e-tags.md`
(campo `Canal que conectou`, já existente na tela, registrado com id real),
`PLANO-MULTICANAL.md` (E3 confirmado `[x]` por API; E2 marcado parcial — a
etapa já foi renomeada na tela, falta código e docs) e um comentário em
`wesales/tools/ghl_api.py` (`STAGES["AGENDAR"]`, sem renomear a chave para
não quebrar `build_w17.py`). Detalhe completo em `APRENDIZADOS-CRM.md`.
**Zero campo, zero tag novos por esta sessão** (o campo `Canal que conectou`
já existia, criado pela outra trilha); zero escrita no CRM: item de
coerência documental pura, não depende de `APROVADO.md`.
**Pronto quando (cumprido):** as duas trilhas ficam achável uma pela outra —
qualquer sessão que abra `ROADMAP-SALES-ENGAGEMENT.md` ou `build-wesales.md`
encontra a nota que aponta para `PLANO-MULTICANAL.md` antes de tratar o
desenho "100% telefone"/`AGENDAR` como corrente. **O que este item não
resolve:** a reformulação completa de `PLANO-MULTICANAL.md` (E2 por
inteiro, E4-E14) continua em aberto — este item só garante que ela é
visível a partir daqui, não a executa.

---

### G-11 · A mudança de etapa aplicada ao vivo em `1d04af2` deixa três coisas para trás: um filtro que virou exclusão permanente, uma tag que sobrevive a quem agenda, e um dump que parou de contar a verdade — **ABERTO, decisão do dono (23/09/2026)**

> **Nota de coerência, 23/09/2026 — este item é o mesmo achado que
> `campos-e-tags.md` (T-05), `IMPLEMENTACAO-WORKFLOWS.md`, `APRENDIZADOS-CRM.md`
> e `ESTADO-E-PLANO.md` citam como `F-16`.** O commit que abriu os dois
> (`2d6a778`) já escrevia "F-16 / G-11" no próprio assunto, mas só criou
> cabeçalho aqui, em G-11 — `build-wesales.md` ganhou a seção **2.31** com o
> rótulo `F-16` (numeração do Bloco 6) sem nunca ganhar um `### F-16` próprio
> neste roadmap. Quem chegar aqui a partir de uma referência a "F-16": é este
> item, item 1 abaixo. Não crio o cabeçalho `### F-16` separado — duplicaria a
> decisão pendente em dois lugares e o dono teria que revogar/aprovar nos
> dois; a referência cruzada é o suficiente para a busca não bater em vazio.

**Por quê:** o commit `1d04af2` (PC do dono) aplicou a mudança de etapa em 5
workflows ao vivo — `REUNIÃO DE DIAGNÓSTICO` no lugar de `NEGOCIAR` no Loop do
closer, na Recuperação de No-show e no SLA do Closer, e o `Atendeu` passando a
**ficar** em `CONECTAR` no `Pós-ligação v2`. A mudança é coerente com o funil
novo. Conferindo offline, duas consequências que nenhum dos dois desenhos vê:

1. **`conectado-hoje` virou mudo permanente.** Nada remove essa tag (varredura
   nos 26 dumps, nenhum `remove_contact_tag`, nenhum reset em nenhum
   documento). Os filtros das filas 8.2/8.3 têm `não conectado-hoje` **E**
   `etapa = CONECTAR`: enquanto o `Atendeu` saía de `CONECTAR`, a cláusula de
   etapa fazia a exclusão e a da tag era redundante. Agora a da tag é a única
   — e o lead que atende uma vez sem fechar horário some das duas filas do SDR
   para sempre, com a oportunidade aberta e a cadência ainda criando tarefa.
2. **`fechar-horario` sobrevive ao caminho de quem agenda.** A tag nasceu com o
   consumidor (`Fechar Horário`) em rascunho; isso foi fechado no `23db864`, que
   o publicou, e a janela fechou limpa (0 contatos). O que **continua aberto** é
   outro elo: a remoção mora nos 4 nós de saída do `Fechar Horário`, e o lead que
   agenda é arrancado do workflow pelo `Pós-agendamento v2` (nó 4) —
   `remove_from_workflow` não executa as saídas do alvo. Quem agenda fica com a
   tag para sempre, e ela é a única tag da conta **sem** segunda rede no Mestre
   de saída. Correção: um `Remove Tag fechar-horario` ao lado do
   `remove_from_workflow` no nó 4.
3. **O dump de 3 workflows ficou descrevendo a conta pré-patch.**
   `patch_remove_parte2.py` exportava o backup e nunca re-exportava o estado
   novo (o script irmão `patch_funil_reuniao.py` faz isso na linha 150). Corrigi
   a ferramenta nesta rodada. O que fica em aberto é uma **confirmação**, não um
   defeito provável: o assunto do commit `23db864` diz *"parte 2 nas remoções"*,
   logo há evidência de que o script rodou com `--aplicar` — só não dá para
   verificar pelo repositório quantos nós ele pegou, e o script varre apenas os
   publicados (workflow em rascunho na hora ficou de fora). Vale confirmar
   porque, se algum nó ficou para trás, o lead que agenda continua recebendo
   toque **automático** da segunda metade da régua. Um comando no PC, sem
   escrever nada: `python patch_remove_parte2.py` sem `--aplicar`.

**Medido em 23/09:** `conectado-hoje` em 2 contatos (os dois de teste do
projeto), `fechar-horario` em 0 (remedido depois da publicação). **Zero lead
real afetado** — é armadilha, não
incêndio, e por isso dá para consertar antes de ligar a esteira.

**O que falta:** para a (1), decisão sua entre as quatro saídas da seção 2.31 do
`build-wesales.md` — recomendo a **A** (`Wait 24h` → `Remove Tag` dentro do
próprio `Pós-ligação v2`). A saída **B** que eu tinha oferecido como
alternativa limpa **caiu na conferência**, pelo mesmo motivo do item (2): ela
trocaria uma exclusão permanente por outra. Para (2) e (3) não há decisão, só
execução — um nó e um comando. Nada disso é aplicável por este MCP (edição de
workflow e de lista inteligente não têm ferramenta aqui); é tela ou
`wesales/tools/`.

### G-12 · Segunda renomeação de etapa (`AGENDAR` → `REUNIÃO DE DIAGNÓSTICO`) documentada como aviso, nunca virou item — mesma classe do G-02, achado mas represado em rodapé — **FEITO em 23/09/2026 (peça 1: seção 1 de `build-wesales.md`; peça 2: resto do documento e este roadmap)**
**Por quê:** o G-10 já tinha cruzado a existência de `PLANO-MULTICANAL.md`
com este roadmap, e a nota do topo deste arquivo (e uma nota dentro da
seção 1 de `build-wesales.md`, linhas 202-218 antes desta rodada) já
registravam que a etapa `AGENDAR` foi renomeada para `REUNIÃO DE
DIAGNÓSTICO` na tela — mas nenhum dos dois tinha virado item de trabalho
com "pronto quando" próprio, o mesmo padrão de "achado escrito não é
aplicado sozinho" que já motivou promover F-12 e F-13. Reconferido nesta
rodada: `opportunities_get-pipelines` confirma o nome na tela e o `id`
inalterado (`3d26fcd1-220d-49ed-8325-705dfe9055b1`); `grep -c` em
`build-wesales.md` a partir da linha 270 (fora da seção 1, que esta
rodada já fechou) contava **39 ocorrências** de `AGENDAR` como nome de
etapa antes desta rodada, nenhuma delas causando bug funcional — todo
workflow publicado decide por `pipelineStageId`, não por nome, então isto
é dívida de documentação, não de comportamento (diferente do G-02, que
tinha risco real de gatilho nunca disparando). **Achado à parte, que já
saiu do estado "represado" nesta mesma rodada:** o aviso em
`build-wesales.md` dizia que `wesales/tools/ghl_api.py` (`STAGES`) ainda
não tinha o nome novo — checado o arquivo, e já tem: as chaves `"AGENDAR"`
e `"REUNIÃO DE DIAGNÓSTICO"` apontam para o mesmo `id`, com comentário
explicando o apelido, feito por fora desta sessão (provavelmente no mesmo
commit `1d04af2`/`2d6a778` do PC do dono que abriu o G-11). O lado código
deste item já está fechado; só restava o lado texto.
**Como:** find-and-replace supervisionado, seção por seção — mesmo método
do G-02 — trocando `AGENDAR` por `REUNIÃO DE DIAGNÓSTICO` em toda prosa e
tabela que descreve a **etapa**, preservando **sem tocar** todo nome
**próprio** já publicado na tela que contém a palavra "AGENDAR" dentro do
nome (o workflow `AGENDAR Estagnado`, a lista `Saúde — AGENDAR
Estagnado`) — trocar o texto desses sem renomear o objeto na tela criaria
uma divergência nova, pior que a atual. Onde a etapa é citada pela
primeira vez numa seção, anotar "(antiga `AGENDAR`)" uma vez; nas
citações seguintes da mesma seção, só o nome novo.
**Pronto quando:** `grep -n "AGENDAR" wesales/build-wesales.md
wesales/ROADMAP-SALES-ENGAGEMENT.md` só retornar (a) a tabela de tradução
1.0 e as notas históricas que já existem de propósito, e (b) os nomes
próprios publicados na tela (`AGENDAR Estagnado`, `Saúde — AGENDAR
Estagnado`) — nenhuma outra ocorrência tratando `AGENDAR` como etapa
corrente.

**Resumo (23/09/2026) — peça 1:** migrada a seção 1 inteira de
`build-wesales.md` (tabela de etapas, tabela de tradução 1.0, tabela de
frameworks de mercado 1.1, canvas operacional das Etapas 1-3) — 8 pontos
de edição, incluindo a correção da nota que dizia `ghl_api.py` ainda
pendente. **Escopo desta rodada, pendência explícita e não lacuna
esquecida:** as seções 2 em diante de `build-wesales.md` (39 ocorrências
medidas antes desta rodada, a maioria dentro da família F-05 peça 5/seção
2.23, do Pós-ligação/Pós-agendamento, e do checklist de teste, seção 10)
e as ocorrências em `ROADMAP-SALES-ENGAGEMENT.md` seguem chamando a etapa
de `AGENDAR` — próxima peça deste mesmo item, mesmo padrão de "uma seção
por rodada" que fechou o G-02 em seis rodadas. Zero campo, zero tag, zero
escrita no CRM: item de documentação pura, não depende de `APROVADO.md`.

**Resumo (23/09/2026) — peça 2, item fechado por inteiro:** das 39
ocorrências medidas antes da peça 1 (34 em `build-wesales.md` a partir da
seção 2, mais as do próprio roadmap — a contagem original somava os dois
arquivos), 32 tratavam `AGENDAR` como etapa corrente em `build-wesales.md`
e foram trocadas por `REUNIÃO DE DIAGNÓSTICO`, com a anotação "(antiga
`AGENDAR`)" só na primeira citação de cada seção `##` (2.12, 2.16, 2.23,
2.24, 2.28, 3, 4, 5, 8.1, 10), como o "Como" deste item pedia. As duas
sobras (`workflow "AGENDAR Estagnado"`, seção 2.23; a lista `Saúde —
AGENDAR Estagnado`, seção 8.23) são nome próprio já publicado na tela e
ficam de propósito. Conferido em seguida `ROADMAP-SALES-ENGAGEMENT.md`
inteiro: as ~30 ocorrências que restavam pertencem todas a itens já
`FEITO`, datados antes ou no mesmo dia da segunda renomeação (G-02, F-05,
R-18, F-13, F-14, G-10, G-11) — descrevem o nome como ele era no momento em
que cada entrada foi escrita, a mesma categoria de "prosa histórica" que a
tabela de tradução 1.0 já tinha direito de manter (G-02 nunca reescreveu
essas). Reescrever essas entradas para `REUNIÃO DE DIAGNÓSTICO` teria
efeito oposto ao pretendido: um item fechado em 21/09/2026 que dissesse
"REUNIÃO DE DIAGNÓSTICO" estaria mentindo sobre o nome que a tela mostrava
naquele dia. Nenhuma edição no roadmap além do aviso do topo (que apontava
"resto do documento e este roadmap seguem chamando a etapa de AGENDAR" —
corrigido para refletir a migração completa) e deste próprio item. **Pronto
quando, cumprido:** `grep -n "AGENDAR" wesales/build-wesales.md
wesales/ROADMAP-SALES-ENGAGEMENT.md` só retorna a tabela de tradução 1.0,
notas históricas datadas de propósito e os dois nomes próprios — conferido
depois da edição, zero ocorrência tratando `AGENDAR` como etapa corrente.
Zero campo, zero tag, zero escrita no CRM: item de documentação pura, não
depende de `APROVADO.md`. Com isso, G-12 fecha por inteiro.

---

### G-13 · O ramo `Atendeu` mudou de comportamento em 23/09/2026 (D3) e a especificação nunca acompanhou — duas seções de `build-wesales.md` e um workflow inteiro descreviam um nó que já não existe — **FEITO em 23/09/2026 (especificação)**

**Por quê:** o G-12 (acima, peça 2) já tinha passado pela seção 2.23 e pela
seção 4 nesta mesma varredura de nomes e não achou nada errado — porque
procurava **nome** de etapa desatualizado, não **comportamento**
desatualizado, e as duas coisas divergiram aqui de um jeito que só aparece
lendo o que o nó faz, não como ele se chama. A D3 do `PLANO-MULTICANAL.md`
(22/09/2026, executada e publicada em 23/09, E5-E7) mudou o ramo `Atendeu`
do `Pós-ligação v2`: ele deixou de mover a oportunidade para `REUNIÃO DE
DIAGNÓSTICO` — agora fica em `CONECTAR`, ganha a tag `fechar-horario` e a
tarefa `[FECHAR HORÁRIO]`; só o `Pós-agendamento v2` move para lá, quando a
reunião é marcada de fato (D4). A própria seção 2.31/F-16 deste roadmap-irmão
já tinha essa mudança **auditada por dump ao vivo** (`Pós-ligação v2`, nós
13/26/77/86/97) — mas duas outras partes do mesmo `build-wesales.md` nunca
leram esse achado: a seção 4 ("Ramo `Atendeu`", nó 6, "Mover oportunidade →
REUNIÃO DE DIAGNÓSTICO") e a seção 2.23 (F-05 peça 5, todo um workflow —
"AGENDAR Estagnado"/W17d — cujo gatilho passou a vigiar um estado que não
pode mais existir: "atendeu e ficou em REUNIÃO DE DIAGNÓSTICO sem reunião
marcada" é agora uma contradição em termos, porque só se entra ali **com**
reunião marcada). `IMPLEMENTACAO-WORKFLOWS.md` (W4 e W17d) e
`campos-e-tags.md`/`APROVADO.md` (T-19) repetiam a mesma versão velha, cada
um por conta própria. O dono já tinha chegado à mesma conclusão pelo lado da
tela — despublicou o W17d (`PLANO-MULTICANAL.md`, E8) — sem que nenhum
documento registrasse o motivo; quem lesse só a especificação teria montado
o nó errado e reativado um workflow que o próprio dono já tinha desligado de
propósito.

**Como:** corrigidas, sem inventar comportamento novo — só transcrevendo o
que já estava auditado em outro lugar (§2.31, `PLANO-MULTICANAL.md` E5-E7,
`INVENTARIO-WORKFLOWS.md`) ou no próprio código que montou o substituto
(`tools/build_fechar_horario.py`):
- `build-wesales.md`, seção 4, ramo `Atendeu`: nós reescritos (tag
  `fechar-horario`, sem movimento de etapa, tarefa renomeada
  `[FECHAR HORÁRIO]`), com nota explicando a mudança e uma pendência nova
  registrada (o ramo não tira mais o lead da `Cadência 12x30` — nenhum
  documento diz se é intencional).
- `build-wesales.md`, seção 2.23: aviso no topo (não apaguei o desenho
  original — regra 1, e serve de registro) explicando que a premissa caiu,
  que `Fechar Horário` é o substituto publicado, e a diferença real entre os
  dois (`Fechar Horário` reengaja por mensagem; **não avisa o gestor**, ao
  contrário desta peça — decisão de desenho em aberto, não resolvida aqui).
  Mesmo tratamento que a seção 2.32 já deu ao F-17 (retirado sem apagar).
- `build-wesales.md`, seção 3 (Mestre de saída): o exemplo que citava o nó
  velho, corrigido — a conclusão do parágrafo (por que a lista é nomeada e
  não `All Except Current`) continua de pé pelo outro exemplo (Pós-agendamento).
- `build-wesales.md`, seção 1.1 (Sales Model Canvas etapa a etapa): as
  tabelas de `CONECTAR` e `REUNIÃO DE DIAGNÓSTICO` — a raiz que F-05, F-13 e
  outros itens citam como fonte do "tempo de estagnação" de cada etapa —
  reescritas para a fase "fechar horário" dentro de `CONECTAR` e para a
  entrada de `REUNIÃO DE DIAGNÓSTICO` exigir reunião já marcada.
- `IMPLEMENTACAO-WORKFLOWS.md`: W4 (ramo `Atendeu`, A6-A9) reescrito igual;
  W17d marcado "não montar, despublicado"; a linha `AGENDAR`/`CONECTAR` do
  dicionário de nomes (seção 0.1) corrigida para o papel novo das duas
  etapas.
- `campos-e-tags.md` (T-19) e `APROVADO.md` (linha da 19ª tag): avisadas de
  que o desenho que aprovariam está obsoleto — não recomendado aprovar como
  está.

**Pronto quando (cumprido):** `grep -n "Mover oportunidade → REUNIÃO DE
DIAGNÓSTICO\|Etapa → \`AGENDAR\`\|\[CONECTADO\] Qualificar e agendar"
wesales/build-wesales.md wesales/IMPLEMENTACAO-WORKFLOWS.md` não acha mais
nenhuma ocorrência **fora** de nota histórica datada ou do próprio aviso de
correção; as duas specs do ramo `Atendeu` (build-wesales.md §4 e
`IMPLEMENTACAO-WORKFLOWS.md` W4) descrevem o publicado; W17d/§2.23 avisam
claramente para não montar. **Pendências explícitas, não resolvidas por
este item, registradas para quem continuar:**
1. Decisão do dono: `Fechar Horário` precisa de um aviso ao gestor
   equivalente ao antigo nó 4 do W17d, ou a falta de visibilidade é
   aceitável porque o workflow já reengaja o lead sozinho? Se sim, é um nó
   novo (`Internal Notification`) em `Fechar Horário` — não sai por API.
2. O ramo `Atendeu` do `Pós-ligação v2` não remove o contato da `Cadência
   12x30` (confirmado no dump) — ele continua recebendo toques automáticos
   de tentativa **depois** de já ter atendido e estar fechando horário.
   Intencional (a régua serve de lembrete extra) ou vazamento (dobra de
   contato pelo mesmo lead, por dois workflows diferentes, na mesma janela)?
   Não decidido em nenhum documento deste projeto até esta rodada.
3. T-19 (`agendar-estagnado`) segue `[ ]` — se algum dia aprovada, precisa
   ser o desenho revisado (que ainda não existe), não o original.

Zero campo, zero tag novos, zero escrita no CRM: item de documentação e
correção de spec, não depende de `APROVADO.md` (a única interação com ele é
o aviso na linha já existente da 19ª tag, sem mudar `[ ]`/`[x]`).

### G-14 · O G-10/G-13 corrigiram seis documentos e esqueceram os dois que o dono e o SDR mais abrem — `GUIA-MONTAGEM.md`, `rotina-limpar-tarefas.md`, `IMPLEMENTACAO-WORKFLOWS.md` (§3.3) e o índice do `README.md` ainda descreviam a conta de antes de 23/09 — **FEITO em 23/09/2026 (coerência entre documentos)**

**Por quê:** o G-10 listou seis lugares para cruzar `PLANO-MULTICANAL.md`
(topo deste arquivo, `build-wesales.md`, `APROVADO.md`, `campos-e-tags.md`,
`PLANO-MULTICANAL.md` e `wesales/tools/ghl_api.py`) e o G-13 corrigiu
`build-wesales.md`, `IMPLEMENTACAO-WORKFLOWS.md` (W4/W17d/dicionário) e
avisou `campos-e-tags.md`/`APROVADO.md` sobre o T-19 — mas nenhum dos dois
tocou `GUIA-MONTAGEM.md`, o documento que o próprio `IMPLEMENTACAO-
WORKFLOWS.md` define como "a ordem das fases e o **estado** do que já foi
montado". Ele ainda descrevia, sem nenhuma nota, a subconta de 22/09/2026:
uma linha "dá para fazer HOJE" (nó 0 do Mestre de saída) recomendando somar
a tag `agendar-estagnado` — o mesmo desenho que o G-13 já classificou como
"não recomendado" em dois outros documentos — e o inventário de workflows
listava `AGENDAR Estagnado`/W17d como rascunho pendente de publicar, quando
na verdade ele foi publicado e depois **despublicado** (G-13). Um segundo
achado, categoria diferente: `rotina-limpar-tarefas.md` (Etapa 5) é um
prompt para colar numa rotina horária que **conclui** tarefa fora de lugar
pela etapa — e a tabela do PASSO 3 mapeia `AGENDAR`/`open` para
`[CONECTADO]`, prefixo que não existe mais desde a D3 (quem atende fica em
`CONECTAR` com `[FECHAR HORÁRIO]`). Pior que o nome: a filosofia do
documento ("por que concluir e não excluir") é o **oposto** da decisão mais
recente do dono (`PLANO-MULTICANAL.md`, D12 — "concluir inventa histórico
falso", por isso a Faxina exclui). Se alguém colasse este prompt numa
rotina nova hoje, ele concluiria por engano a tarefa `[FECHAR HORÁRIO]` de
todo lead que acabou de ser atendido. `IMPLEMENTACAO-WORKFLOWS.md`, §3.3
(rotina do gestor), ainda apontava para este prompt como o mecanismo "a
cada hora" — quando quem roda de verdade, a cada 10 min, é a Faxina
(`tools/faxina_tarefas.py`, D12), com a tabela de prefixo já corrigida
dentro do próprio script (`validas()`). Por fim, o índice do `README.md`
("O que vive aqui") nunca ganhou uma linha para `PLANO-MULTICANAL.md` desde
que ele existe (22/09/2026) — quem abrisse só o README para se orientar não
saberia que o documento existe.

**Como:** sem reescrever nenhum dos quatro documentos por inteiro (mesma
régua do G-10: "trabalho grande demais para uma rodada, e não é o que este
achado pede"):
- `GUIA-MONTAGEM.md`: aviso datado logo no topo, apontando para
  `PLANO-MULTICANAL.md` como a foto mais recente; a linha "dá para fazer
  HOJE" da tag `agendar-estagnado` riscada com nota "não recomendada,
  premissa superada"; as duas células do inventário de workflows
  (`AGENDAR Estagnado`/W17d) corrigidas para "despublicado em 23/09,
  não republicar".
- `rotina-limpar-tarefas.md`: aviso datado logo no topo explicando as duas
  divergências (prefixo por etapa vencido; filosofia concluir vs. excluir
  substituída pelo D12) e apontando para `tools/faxina_tarefas.py` como o
  mecanismo que roda de verdade hoje. A tabela do PASSO 3 não foi
  reescrita — o aviso já deixa claro que ela é histórico, não instrução.
- `IMPLEMENTACAO-WORKFLOWS.md`, §3.3: a linha "a cada hora (automático)"
  trocada para descrever a Faxina (10 min, exclui, aponta para o script);
  a linha "diário" (listas de saúde 8.20-8.24) ganhou a mesma ressalva do
  T-19 sobre a 8.23.
- `README.md`: nova linha para `PLANO-MULTICANAL.md` no índice, com a nota
  de que ele é o estado mais recente quando divergir de documento mais
  antigo.

**Pronto quando (cumprido):** `grep -rn "AGENDAR" wesales/*.md` não devolve
mais nenhuma instrução ativa (linha "dá para fazer hoje", tabela de rotina
automática ou índice de leitura) descrevendo o desenho anterior à D3/G-13
sem um aviso datado ao lado explicando o que mudou; `PLANO-MULTICANAL.md`
aparece no índice do `README.md`. **Pendência que este item não resolve, e
não tentou:** as seções "Estado da montagem"/"Estado final" do
`GUIA-MONTAGEM.md` continuam descrevendo 22/09/2026 sem incorporar os 20+
workflows criados/reformulados em 23/09 pela API interna — reescrever isso
é a mesma classe de trabalho grande que o G-10 já tinha adiado; o aviso no
topo do arquivo é o que impede a leitura errada até alguém fazer essa
reescrita. Zero campo, zero tag, zero escrita no CRM: item de documentação
e correção de spec, não depende de `APROVADO.md`.

---

### G-15 · Lead que já circulou por telefone reaparece pelo Instagram sem telefone nem e-mail — o GHL nunca compara os dois, e a plataforma não deixa nem tentar por workflow — **FEITO em 23/09/2026 (especificação + achado de limite de plataforma)**

**Por quê:** a fusão automática nativa (R-13, preferências de deduplicação) só
age na **criação**: contato novo com telefone/e-mail igual a um existente
vira atualização, não duplicata. Ela nunca revisita dois contatos que **já
existem separados**. Isso importa porque a base tem dois pontos de entrada
sem identificador em comum: Meta Lead Ads grava telefone; o Instagram (DM
da `Qualificação por IA no WhatsApp`, seção 6) não tem telefone nem e-mail
no perfil. Um lead que preencheu o formulário há 60 dias, esfriou e caiu em
`nutricao-90d`, e meses depois manda DM no Instagram pelo mesmo negócio,
vira um **segundo contato**, com uma **segunda cadência** rodando por cima
da primeira — o SDR liga pela régua antiga enquanto o agente de IA já está
agendando pela conversa nova, e nenhuma tela mostra que é a mesma pessoa.
Mesmo padrão de "estrago silencioso" que motivou o F-05, agora entre
contatos, não dentro de um.

**Pesquisado antes de desenhar** (`WebSearch`, confiança média — página
oficial da HighLevel e o próprio board de ideias da comunidade, citados em
buscas com termos diferentes, mesmo padrão de confiança do G-05/R-14):
existe uma ação nativa de workflow, `Merge Contact`, que funde duplicatas
por Telefone, E-mail ou os dois — pareceria resolver isto sozinha. **Mas o
gatilho que a acionaria não existe:** o `Contact Changed` (o único gatilho
deste projeto que reage a mudança de campo, já usado em várias seções do
`build-wesales.md` com filtro por Custom Field) hoje só filtra por Usuário
atribuído, DND, Tag,
Custom Field, Endereço e Website — **Telefone e E-mail não estão na
lista**, pedido em aberto no board de ideias da própria HighLevel, sem
previsão. Sem esse gatilho não há como disparar o `Merge Contact`
automaticamente no momento em que um contato do Instagram ganha telefone
(ou vice-versa) — a peça que falta não é a ação, é o gatilho que a
chamaria. Registrado em `APRENDIZADOS-CRM.md` para a próxima sessão não
tentar desenhar o mesmo workflow de novo.

**Como:** sem automação (a lacuna é de plataforma, não de desenho), a saída
é a mesma que R-11/R-14 já usaram para o que workflow não alcança —
**ferramenta nativa + rotina humana**, não um workflow novo:
- A tela tem uma **Duplicate Management & Merge Tool** (Configurações →
  Contatos), que agrupa por Nome, Telefone ou E-mail e funde até 10 contatos
  de uma vez — o único critério dela que serve para um contato sem telefone
  nem e-mail é o **Nome**.
- Passo novo no fluxo do SDR (`GUIA-SDR.md`): antes de tratar um handoff
  vindo do Instagram como "lead novo", buscar o nome/empresa na busca de
  contatos — se já existir alguém com o mesmo telefone ou o mesmo negócio,
  é fusão, não lead novo.
- Rotina do gestor: rodar a Duplicate Management & Merge Tool filtrando por
  Nome uma vez por semana, revisando os pares sugeridos antes de fundir (a
  fusão por Nome tem falso-positivo: dois donos de negócio homônimos não são
  a mesma pessoa).

**Pronto quando:** o passo de checagem está escrito no `GUIA-SDR.md` e a
rotina semanal está registrada aqui; nenhuma automação por API é prometida
— a limitação de plataforma (`Contact Changed` sem Telefone/E-mail) fica
documentada para ninguém tentar o mesmo desenho de novo antes que a
HighLevel resolva o pedido em aberto. Zero campo, zero tag, zero escrita no
CRM: item de especificação e achado de limite de plataforma, não depende de
`APROVADO.md`.

---

### G-16 · A Porta de Entrada não distingue lead de contato pessoal do dono — um WhatsApp pessoal virou oportunidade aberta, exposta à cadência automática — **FEITO em 23/09/2026** (aberto e especificado em 23/09/2026, executado na mesma data)

**Por quê:** achado ao seguir a própria regra que o G-10/G-14 deixaram —
"quem mais fala disso?" — mas aplicada a um alvo que nenhuma sessão tinha
cruzado ainda: `ESTADO-E-PLANO.md`, que **nenhuma** das varreduras de
coerência (G-10, G-13, G-14) tocou, embora todas as outras tenham revisado
`GUIA-MONTAGEM.md`, `rotina-limpar-tarefas.md`, `IMPLEMENTACAO-WORKFLOWS.md`
e `README.md`. A seção 8 desse documento tem uma linha (item "0") em aberto
desde 23/09/2026, 02:35 UTC, nunca promovida a item de roadmap: "`Francisca`
(+5512981913254) é você testando ou é gente?" — pergunta que ficou sem
resposta por horas porque quem a escreveu não tinha como confirmar, e
ninguém mais leu aquele documento depois.

Conferido nesta rodada, por API, o que o documento não podia responder:
`contacts_get-contacts` confirma o contato (`9wOSMuznjenFxa3yaep0`) ainda
aberto — `etapa-novo-lead` + `cad-inbound`, sem `assignedTo`, oportunidade
`gwDvzf9FeRDv2LfOVbH9` em `NOVO LEAD`/`open`. `conversations_get-messages`
no fio inteiro (8 mensagens, 22/09 23:34 a 23/09 00:01 UTC) resolve a
pergunta: é pessoa real, e a conversa é **pessoal**, não comercial —
"Oi Pablo, boa noite" (a lead chamando o dono pelo nome), "Te lembrando do
pix", um áudio, "Feito", um número de telefone compartilhado, "E mais uma
vez obrigado pela carona", "Salvou rs". Nenhuma mensagem do fio tem qualquer
sinal de anúncio, agência ou fit comercial. **Não é o mesmo achado do G-15**
(duas cadências para o mesmo lead): aqui não há lead nenhum — é o número de
WhatsApp da operação recebendo tráfego pessoal do próprio dono, e a máquina
tratando isso como prospect.

**Causa raiz, e por que não é só sobre a `Francisca`:** o gatilho que cria
oportunidade a partir de mensagem inbound (Porta de Entrada / `Qualificação
por IA no WhatsApp`, seção 6 do `build-wesales.md`) dispara para **qualquer
primeira mensagem** recebida naquele número — o GHL não tem campo nenhum
para diferenciar "prospect desconhecido" de "contato pessoal do dono
escrevendo por engano no número errado". Qualquer outra pessoa da vida
pessoal do dono que mandar mensagem para esse número recebe o mesmo
tratamento: vira oportunidade em `NOVO LEAD`, ganha `cad-inbound`, e fica
elegível à cadência automática de qualificação assim que a fila rodar.
**Sem dano ainda** — o fio inteiro só tem mensagem pessoal do dono, nenhuma
automática de cadência —, mas o risco fica aberto enquanto as duas tags
continuarem no contato: o próximo toque da `Cadência Inbound` pode mandar
uma mensagem de qualificação de anúncios para uma pessoa que só queria
lembrar o dono de um Pix.

**Como (dois pedaços, riscos diferentes):**

1. **Preventivo, sem escrita no CRM — fechado nesta rodada:** passo novo no
   `GUIA-SDR.md` ("Lead novo inbound que parece contato pessoal do dono"),
   pedindo para ler o fio antes de tratar a tarefa `TI1` como prospect, e
   avisar o gestor em vez de mudar tag/etapa sozinho — mesmo padrão do passo
   do G-15 para Instagram (checar antes de tratar como lead novo), mesma
   razão: o filtro que falta não é algo que um workflow consiga decidir
   sozinho, só leitura humana da conversa resolve.
2. **Corretivo, escreve no CRM — aguarda `[x]`:** remover `etapa-novo-lead`
   e `cad-inbound` do contato `9wOSMuznjenFxa3yaep0` e mover a oportunidade
   `gwDvzf9FeRDv2LfOVbH9` para `abandoned` (não `lost` — nunca houve
   conversa comercial para perder). Não apaga nada (regra 1): o contato e o
   histórico de mensagens continuam intactos, só saem da régua ativa.

**Por que não executo sozinho:** é escrita em contato real, não de teste, e
a regra 2 do briefing e a "Como autorizar" do `APROVADO.md` existem
exatamente para isto — por mais óbvio que pareça pela leitura do fio, quem
decide que um contato real não é lead é o dono, não a rotina. Linha nova
registrada em `APROVADO.md`, nasce `[ ]`.

**Pronto quando:** o dono confirmar (ou corrigir, se for engano meu) que
`Francisca` é pessoal, marcar o `[x]` novo em `APROVADO.md`, e as duas tags
saírem do contato com a oportunidade em `abandoned` — conferido por
`contacts_get-contact` depois, mesmo padrão de leitura de volta que este
projeto já usa em toda escrita. O passo preventivo no `GUIA-SDR.md` já vale
a partir de agora, independente da decisão sobre este contato específico.

**Fechado em 23/09/2026 — o dono autorizou ao vivo em chat (~11:35 BRT,
"sim") e a execução saiu em duas metades, por duas sessões, registradas em
`APROVADO.md`:** 17:06 UTC, tags `etapa-novo-lead`/`cad-inbound` removidas e
`nao-perturbe` aplicada de proteção **antes** da mudança de status — decisão
que se provou certa 3 segundos depois da segunda metade, quando o `Espelho
de Etapa` reagiu à mudança de status e pôs `status-nutricao`: sem a
proteção prévia, o contato ficaria elegível à Triagem da Nutrição (que exige
`status-nutricao` **e** ausência de `nao-perturbe`); com ela, fica de fora.
17:08 UTC, `opportunities_update-opportunity` moveu `gwDvzf9FeRDv2LfOVbH9`
para `abandoned` (`HTTP 200`). Reconfirmado por
`opportunities_search-opportunity`: a composição de `NOVO LEAD` `open` caiu
de 49 para 48 com esta correção — nada apagado (regra 1), o contato e o
histórico de mensagens continuam intactos, só fora da régua ativa. O passo
preventivo no `GUIA-SDR.md` (item 1 do "Como" acima) segue valendo para o
próximo caso do mesmo tipo.

---

### G-17 · O portão de capacidade só protege duas cadências das seis — `Reengajamento 90 dias` gasta a cota semanal sem nunca respeitá-la, e ignora a pausa do próprio SDR — decisão do dono, patch da Inbound já escrito e validado — **FEITO 23/09/2026 ~18:40 BRT** (Inbound 322 + No-show 61 no ar; `auditoria_portoes` 0)

**Por quê:** uma sessão em paralelo (commits fora deste roadmap, ver G-10)
foi corrigir a pendência 9e de `ESTADO-E-PLANO.md` ("portar os 6 nós de
portão de capacidade da `Cadência 12x30` para a `Cadência Inbound`") e, antes
de aplicar, fez a pergunta que faltava: **o que mais está lá que ninguém
olhou?** A resposta não é a Inbound sozinha — é uma invariante que nenhum
item numerado deste roadmap tinha verificado antes: *se um toque coloca o
lead numa fila (`fila-tel`/`fila-wa`) ou marca a tag `toque`, ele consome
capacidade do SDR, logo a cadência tem de ler os três portões* (`Lead
pausado?` → tag `pausado`; `SDR lotado?` → tag `sdr-lotado`; `Teto de toques
da semana?` → campo `Toques na semana`, `c1xuCuLyJheHOQoJ3grH`). Medido nó a
nó nas sete cadências publicadas:

| cadência | toques | marca fila/`toque` | `pausado` | `sdr-lotado` | teto semanal |
|---|---|---|---|---|---|
| `Cadência 12x30` | 6 | sim | 6/6 | 6/6 | 6/6 |
| `Cadência 12x30 — parte 2` | 6 | sim | 6/6 | 6/6 | 6/6 |
| `Cadência Inbound` | 5 | sim | 5/5 | **0** | **0** |
| `Recuperação de No-show` | 3 | sim | ok¹ | **0** | **0** |
| `Reengajamento 90 dias` | 4 | sim | **0** | **0** | **0** |
| `Nutrição — WhatsApp 15 dias` | 6 | não consome | — | — | — |
| `Fechar Horário` | 2 | não consome | — | — | — |

¹ lê `pausado` dentro de `NS{n} · Ainda vale recuperar?`, nos 3 toques —
cobre por conteúdo, não pelo nome do nó.

O `Reengajamento 90 dias` é o pior caso: publicado, 105 nós, e as três
strings (`pausado`, `sdr-lotado`, `c1xuCuLyJheHOQoJ3grH`) não aparecem em
lugar nenhum do workflow, nem por toque nem no portão de entrada. Duas
consequências, a segunda pior que a primeira — (1) a pausa que o SDR aplica
à mão não vale para a cadência que mais mexe com lead frio; (2) cada um dos
4 toques marca `toque`, que **alimenta** o contador que os portões da 12x30
leem para travar — o Reengajamento gasta a cota semanal sem nunca respeitá-
la, apertando o freio dos outros e passando livre ele mesmo. Achado de dump,
tratado como candidato, não como fato: confirma-se lendo os três workflows
ao vivo, ou medindo — contato com a tag `pausado` que ainda assim recebe
`fila-tel`.

**Como:** duas ferramentas novas em `wesales/tools/`, ambas somente leitura
ou validadas sem tocar a conta, documentadas em `build-wesales.md` §2.36 a
§2.39 (`patch_condicoes_etapa.py`, `auditoria_condicoes.py`,
`patch_portao_inbound.py`, `auditoria_portoes.py`, `auditoria_tudo.py`):

- `auditoria_portoes.py` — verifica a invariante acima por conteúdo (não por
  nome de nó) contra os dumps publicados; hoje devolve 3 cadências em falha,
  `exit 1`.
- `patch_portao_inbound.py` — clona o grupo de 5 nós que já existe e já
  funciona na `Cadência 12x30 — parte 2` (10 portões lógicos × 5 nós = 50
  nós novos, de 272 para 322) e remapeia todo uuid interno do clone. Tem
  modo `--dump` que valida sem token e sem rede contra os dumps do
  repositório (medido: 0 id repetido, 0 `parentKey` órfão, 0 `goto` para nó
  inexistente, condição dos 10 clones idêntica à do doador). Cobre hoje só a
  `Cadência Inbound` — estendê-lo às outras duas é mecânico (o `ALVO` e os
  `TOQUES` são parâmetro), mas só depois da decisão abaixo.

Zero tag nova, zero campo novo — `sdr-lotado` e `Toques na semana` já
existem e a `Cadência 12x30` já os lê. Não depende de `[x]` em
`APROVADO.md`: editar workflow publicado não sai por este conector (nem
leitura nem escrita além do `GET`), então a aplicação é script no PC do
dono (`--aplicar`, com backup em `_antes-portao-inbound/`) ou tela, nos dois
casos ação manual dele, mesma classe de G-11 (itens 2/3).

**A decisão que é do dono, não minha:** `Recuperação de No-show` e
`Reengajamento 90 dias` tocam lead mais quente (marcou reunião e não
apareceu, ou já foi lead antes) que a fila de entrada nova — pode ser
desenho de propósito que eles furem a fila em vez de esperar a cota. As
duas saídas são opostas e ambas defensáveis: **(A)** portar os três portões
para as duas cadências, mesma régua da 12x30/Inbound — cada toque delas
passa a respeitar `pausado`/`sdr-lotado`/teto semanal; **(B)** tirar o
`add_contact_tag ['toque']` dessas duas cadências, para elas pararem de
gastar (sem nunca respeitar) uma cota que não é delas — nesse caso não
precisam do portão, precisam de sair do contador alheio. Recomendo (A) para
`Recuperação de No-show` (já lê `pausado`, falta pouco, e não há razão para
ele ignorar `sdr-lotado`) e deixo (A) vs. (B) em aberto para o
`Reengajamento 90 dias`, que é o caso realmente ambíguo.

**Pronto quando:** o dono escolher A ou B para cada uma das duas cadências
restantes (a Inbound já está decidida a favor de A, patch pronto); o script
correspondente rodar com `--aplicar` (ou a tela, Caminho B do §2.37, para
quem preferir clique) nas cadências que precisam de portão novo, e nas que
saem do contador o nó `add_contact_tag ['toque']` for removido; e
`auditoria_portoes.py` voltar a rodar depois, devolvendo `exit 0` — zero
cadência publicada em falha contra a invariante. Detalhe completo em
`build-wesales.md` §2.36 a §2.39 e em `ESTADO-E-PLANO.md`, itens 9d
(resolvido — o "problema" era ausência de guarda para o futuro, já coberto
por `auditoria_condicoes.py`) e 9e (cresceu deste item 1-caso para o G-17
3-casos, tabela atualizada com a referência cruzada).


**Decisão (23/09/2026, dono ao vivo em chat: "siga as suas recomendações").**
Opção **(A)** — portar os portões — para as duas cadências que ainda existem.
E uma correção deste item: **o `Reengajamento 90 dias` não existe mais na
conta.** Foi substituído em 22/09 pela `Nutrição — WhatsApp a cada 15 dias`
(mesmo id `37eb32e4`, 37 nós), 100% automática, sem `toque` e sem `fila-tel`
— não consome capacidade, logo não precisa de portão. O "pior caso" da
tabela acima era um dump morto (`workflows-json/Reengajamento 90 dias.json`,
agora em `_arquivo/`). Lido ao vivo pela lista de workflows da subconta.

- `Cadência Inbound`: `patch_portao_inbound.py` — plano ao vivo ok (272 → 322).
- `Recuperação de No-show`: `patch_portao_noshow.py` (novo) — portões só em
  NS1 e NS2; o toque imediato do no-show fica livre de propósito (lead
  quente, é a ligação que mais recupera reunião) e o NS3 não enfileira.
  Plano ao vivo ok (41 → 61).
- `auditoria_portoes.py` depois do arquivamento: 2 cadências em falha (eram 3).

**Por que não está no ar:** as duas gravações foram negadas pelo classificador
do modo automático do Claude Code (o dono escolheu manter o modo automático).
Aplicar = o dono rodar, na sessão, `! python wesales/tools/patch_portao_inbound.py --aplicar`
e `! python wesales/tools/patch_portao_noshow.py --aplicar` (backup automático).

---

### G-18 · O ramo `Atendeu` do `Pós-ligação v2` é o único ramo de saída sem a segunda linha de defesa que o `Não ligar` já tem — pendência 2 do G-13, nunca promovida a item próprio — patch escrito e validado por dump, falta aplicar na tela — **FEITO em 23/09/2026 (especificação + patch validado por dump)**

**Por quê:** o G-13 (acima) já tinha registrado, como pendência explícita e
não resolvida, que o ramo `Atendeu` do `Pós-ligação v2` não remove o
contato da `Cadência 12x30` — confirmado no dump, ao contrário do ramo
`Não ligar`, que tem `remove_from_workflow` desde a correção do F-05. Essa
pendência ficou dentro do texto do G-13 por dois dias sem ganhar "Pronto
quando" próprio — o mesmo padrão que o G-16/G-17 já descreveram para outros
achados ("achado técnico completo não é a mesma coisa que achado
rastreável"). Reli o G-13 seguindo a própria instrução desta seção (reler
pendência represada antes de procurar lacuna nova) e fui direto ao dump para
confirmar, não deduzir do texto.

**Precisão sobre a gravidade, para não superestimar o achado (conferido no
dump da própria `Cadência 12x30`, não só no do `Pós-ligação v2`):** a
`Cadência 12x30` já tem, publicada, sua própria saída por tentativa — o nó
10 do molde (`build-wesales.md`, seção 2.4; `IMPLEMENTACAO-WORKFLOWS.md`,
linha do nó 10) faz `Remove from Workflow: este` quando `Resultado da
tentativa` é `Atendeu` (entre outros) **enquanto o "Aguardar resultado"
daquela tentativa específica ainda está ativo** (até 18:30 do mesmo dia) —
confirmado no dump: 12 nós `remove_from_workflow` (um por tentativa),
todos apontando para a própria `Cadência 12x30`. Ou seja, **no caso comum
(SDR liga e classifica no mesmo dia, dentro da janela da tentativa), o lead
já sai sozinho.** O que falta é a **segunda linha de defesa** que o ramo
`Não ligar` do `Pós-ligação v2` tem e o ramo `Atendeu` não: se a
classificação `Atendeu` chega **fora** da janela ativa daquela tentativa —
por exemplo, o SDR corrige o resultado depois (de `Não atendeu` para
`Atendeu`, num retorno tardio) enquanto a cadência está no `Wait` de dias
entre tentativas, não no `Aguardar resultado` — o nó 10 daquela tentativa já
passou e não há outro ouvindo o mesmo evento. É exatamente o cenário que
justificou o `remove_from_workflow` do ramo `Não ligar` (proteção
independente de timing) — só que aplicado só lá, nunca ao `Atendeu`. Não é
"todo lead atendido continua sendo chamado para sempre"; é "falta a mesma
rede de segurança que os outros ramos de saída já têm para quando a
classificação não acontece no instante exato em que a régua está olhando".

**Confirmado no `wesales/workflows-json/Pós-ligação v2.json` (version 7),
nó a nó, não por grep de texto:** o switch por `Resultado da tentativa`
existe em **duas cópias** dentro do workflow — uma para cada lado do nó 2
(canal-check por tag `fila-wa`, herdado de quando a régua ainda ligava por
WhatsApp; `d52e61d` tirou o canal mas as duas cópias continuam publicadas).
Dentro do ramo `Atendeu`, cada cópia tem **ainda** um segundo If/Else por
canal (nó 1 da tabela do `build-wesales.md` §4) — quatro caminhos ao todo,
e nenhum termina em `remove_from_workflow`:

| caminho | nó terminal | vale hoje? |
|---|---|---|
| cópia 1 (`fila-wa` presente), ramo WA | `627573c8…` | não — `fila-wa` nunca fica presente na régua atual |
| cópia 1 (`fila-wa` presente), ramo telefone | `a39fe8fc…` | **não — é também um beco sem saída, ver nota abaixo** |
| cópia 2 (`fila-wa` ausente), ramo WA | `ca6a4dba…` | não, mesmo motivo da linha 1 |
| cópia 2 (`fila-wa` ausente), ramo telefone | `b5167da9…` | **sim — é o caminho real, 100% da operação hoje** |

**Nota que quase virou um achado maior, e não é — registrada para quem
revisar não redescobrir o susto:** o caminho `a39fe8fc…` (cópia 1, telefone)
não só carece do `remove_from_workflow` como é um beco sem saída completo —
só `Math: Conexões telefone +1`, sem tag `conectado-hoje`/`fechar-horario`,
sem `[FECHAR HORÁRIO]`, sem nota. Parecia um bug catastrófico (o canal
telefone é 100% da operação) até eu confirmar que este caminho específico
só é alcançado quando `fila-wa` está presente **duas vezes seguidas** (no
nó 2 do workflow e de novo dentro do próprio ramo `Atendeu`) — e a régua
publicada nunca deixa essa tag presente nesse ponto. É código morto pelas
mesmas tags que o levariam até ali, não um caminho que lead real percorre.
O caminho que **de fato** roda para 100% da operação (`fila-wa` ausente nas
duas checagens) é o da última linha da tabela, e esse está completo em tudo
— só falta o `remove_from_workflow`.

**Como:** `wesales/tools/patch_remove_atendeu.py`, novo nesta rodada — clona
a mesma ação que o ramo `Não ligar` já usa (`remove_from_workflow` com a
mesma lista de `workflow_id`: `Cadência 12x30`, `Cadência 12x30 — parte 2`
e um terceiro id sem workflow vivo nos dumps atuais, inofensivo, herdado da
mesma lista) — não "All Except Current Workflow": essa opção removeria o
lead também do `Fechar Horário`, que a mesma execução do ramo `Atendeu`
acabou de inscrever pela tag `fechar-horario` alguns nós antes, e a corrida
entre os dois workflows não é testável por este script (mesma ressalva já
registrada na seção 2.9.5 do `build-wesales.md` para outro par). O nó novo
entra **depois** do último nó de cada um dos quatro caminhos (nunca antes),
para dar ao `Fechar Horário` a maior janela possível para começar a própria
inscrição primeiro. Validado com `--dump` nesta rodada, sem tocar a conta:
142 → 146 nós, ids únicos, nenhum pai órfão, os 4 nós novos com o alvo
certo — `exit 0`.

**Pronto quando:** o dono rodar `patch_remove_atendeu.py --aplicar` no PC
(ou aplicar o mesmo `Remove from Workflow` nos quatro pontos pela tela) e o
script confirmar `status=published` com os 4 nós novos gravados; depois
disso, o ramo `Atendeu` do `Pós-ligação v2` passa a remover o lead da
`Cadência 12x30` **também** quando a classificação chega fora da janela da
tentativa ativa — a mesma rede de segurança que o ramo `Não ligar` já tem,
cobrindo o caso que o nó 10 da própria `Cadência 12x30` (que já resolve o
caso comum, mesmo dia) não alcança. Zero tag nova, zero campo novo, zero
escrita no CRM por este item: não depende de `[x]` em `APROVADO.md`
(edição de workflow publicado não sai por este conector).

---

### G-19 · O agendamento da Faxina (`.github/workflows/faxina-tarefas.yml`) já estava medido em `rotina-limpar-tarefas.md` e `ESTADO-E-PLANO.md` (pendências 11a/11b), nos dois sem "Pronto quando" — dois defeitos, mesmo arquivo, nunca viraram item rastreável — **ABERTO, decisão do dono**

**Por quê:** a Faxina de Tarefas (D12 do `PLANO-MULTICANAL.md`, único
mecanismo real de higiene de tarefa desde que a rotina de agente por prompt
foi aposentada) roda hoje bem mais vezes do que qualquer documento deste
projeto diz que roda, e carrega um risco de quebra silenciosa que nenhum
item numerado (G/R/F) cobre. Achado técnico completo já existia em dois
lugares — `rotina-limpar-tarefas.md` (seção "Mas o agendamento não é o que
este documento especifica", medido por API do Actions, não por `git grep`)
e `ESTADO-E-PLANO.md` (seção 8, pendências 11a/11b) — mesmo padrão que já
motivou G-16/G-17/G-18: achado medido e documentado não é o mesmo que
achado rastreável, e sem "Pronto quando" próprio ele fica represado no
texto até alguém reler o documento certo.

**Defeito 1 — cadência 7× maior que a documentada.** O arquivo tem dois
`cron`, e o GitHub Actions **soma** os dois em vez de escolher um:

```
schedule:
  - cron: "*/10 11-22 * * 1-5"    # a cada 10 min, 11h-22h UTC (08h-19h BRT), seg-sex
  - cron: "0 * * * *"             # de hora em hora, TODOS os dias, sem exceção
```

Confirmado nesta rodada lendo o arquivo direto da branch padrão
(`claude/youtube-publication-next-steps-v7o4el`), não deduzido do texto: os
dois `cron` estão lá, ativos, exatamente como `rotina-limpar-tarefas.md`
mediu.

| | Documentado (`rotina-limpar-tarefas.md`, `PLANO-MULTICANAL.md` D12) | No ar |
|---|---|---|
| dia útil, janela 08–19 BRT | 12 execuções (horária) | **84** |
| sábado e domingo | 0 ("não há tarefa nascendo e não há SDR trabalhando") | **24 por dia** |
| madrugada (fora da janela) | 0 | 1 por hora |

Não é só custo de minuto de Actions: a proteção contra corrida com os
workflows do GHL é a carência de 5 minutos (tarefa criada há menos de 5 min
não é tocada pela Faxina). Desenhada para cadência horária, 5 minutos é
folga grande; com execução a cada 10 minutos essa folga cobre só metade do
intervalo entre execuções — a margem encolheu sem que ninguém tivesse
decidido isso. O teto de 200 tarefas por execução e a trava de "não mexe se
mais da metade das tarefas abertas estão vencidas" (D12) continuam valendo,
então o risco não é destruição — é a mesma classe de "margem que encolheu
sem decisão" que o G-17 já descreveu para o portão de capacidade, aqui para
o intervalo entre execuções em vez de para o volume por execução.

**Defeito 2 — o `checkout` está pinado nesta branch de PR, não na branch
padrão.** O mesmo arquivo tem:

```
- uses: actions/checkout@v4
  with:
    ref: claude/amazing-johnson-mclksg
```

— a branch deste próprio PR. **Correção de 28/09/2026 (G-35): o PR citado
aqui como referência, #93, fechou sem merge em 24/09/2026 — o PR aberto de
verdade para esta branch é outro, e o número muda toda vez que um fecha e
outro abre; ver G-35 para a verificação por API do GitHub.** O risco não
muda: quando o PR aberto desta branch mesclar e a branch for apagada (fluxo
padrão de merge do GitHub), o primeiro `checkout` de toda execução seguinte
falha — a Faxina para de rodar, de madrugada, sem ninguém olhando, e as
tarefas automáticas órfãs voltam a se acumular sem a única rede que hoje as
segura. Diferente do defeito 1 (cadência errada, mas funcionando), este é
"funciona até o dia em que para de funcionar por completo", a mesma classe
de exposição sem teto que já tirou o F-04 da ordem normal.

**Como:** os dois defeitos vivem no mesmo arquivo, fora de `wesales/` —
`.github/workflows/faxina-tarefas.yml` é raiz do repositório, e a regra 5
desta rotina ("só mexa em `wesales/`") impede esta sessão de editá-lo, por
mais mecânico que o conserto seja. `rotina-limpar-tarefas.md` já deixa as
duas correções escritas, prontas para quem tiver escopo de repo-root:

1. Cadência (escolha do dono, as duas são válidas — só não do jeito que
   está, com um documento dizendo uma coisa e o `cron` outra): **(A)** o
   `cron` passa a valer o documentado — `0 11-22 * * 1-5`, horária na
   janela, remove o `0 * * * *`; ou **(B)** o documento (`PLANO-
   MULTICANAL.md` D12, `rotina-limpar-tarefas.md`) passa a descrever a
   cadência de 10 minutos de verdade, e a carência de 5 minutos contra
   corrida é revista para caber num intervalo menor (por exemplo, subir a
   carência ou reduzir a frequência fora da janela comercial).
2. Branch (mecânico, não decisão — fazer no mesmo movimento do merge do PR
   aberto desta branch **hoje** — não o #93, ver G-35): trocar
   `ref: claude/amazing-johnson-mclksg` pela branch padrão
   do repositório (`claude/youtube-publication-next-steps-v7o4el`, medida
   por API do GitHub nesta rodada) ou remover o `ref:` para herdar o
   default do `checkout@v4`.

**Achado relacionado, registrado mas não promovido a item próprio —** a
mesma varredura de `rotina-limpar-tarefas.md` cobre um terceiro ponto (o
Private Integration Token antigo, que apareceu no histórico de chat de uma
sessão anterior): conferido ali que nenhum consumidor deste repositório usa
esse PIT (`ghl_api.py` usa o bearer interno, `faxina_tarefas.py` usa o
`GHL_TOKEN` novo), revogá-lo em Settings → Private Integrations é seguro
**daqui** — decisão pronta, sem "Pronto quando" técnico pendente, mesma
categoria de L-03/L-06 (registrada de propósito sem item de roadmap, ação
do dono quando ele quiser, sem urgência nem dependência de outra coisa).

**Pronto quando:** o `.github/workflows/faxina-tarefas.yml` tem um único
`cron` cuja cadência bate com o que `PLANO-MULTICANAL.md`/
`rotina-limpar-tarefas.md` descrevem (nenhum dos dois documentos precisando
de correção depois), e o `ref` do `checkout` aponta para a branch padrão do
repositório, não para a branch de um PR que vai deixar de existir. Zero
campo, zero tag, zero escrita no CRM: item de coerência entre documentos e
de infraestrutura de repositório, fora do que `APROVADO.md` governa (não é
escrita na subconta) e fora do escopo desta sessão (não é `wesales/`).

### G-20 · A conta "tem 25 tags" em dois documentos e "dez fora da numeração" num terceiro — a própria lista ao lado de cada frase já somava 27 e 12 — **FEITO em 23/09/2026 (coerência entre documentos)**

**Por quê:** CRM reconfirmado por API nesta rodada — 56 oportunidades (mesma
composição da leitura do G-19), 56 campos de contato — G-03, G-04 (peça 2),
F-09, F-10, G-11 (item 1), G-16, G-17 e G-19 seguem aguardando o dono, sem
novidade; PR #93 continua `open`/`draft`, sem merge (a metade "branch" do
G-19 segue aberta). O sweep desta rodada não foi grep por nome de etapa nem
`git log` fora de `wesales/` (G-17/G-19 já tinham esgotado essas duas
veias) — foi conferir, campo a campo e tag a tag, se os **totais** que este
projeto declara batem com a própria enumeração ao lado deles, pergunta que
nenhuma rodada anterior tinha feito para números (só para nomes e
referências). Bateu para campos (o "(50 + 1 sugerido)" de `campos-e-tags.md`
soma certo contra os 56 que `locations_get-custom-fields` devolve, contando
os 4 registrados fora do título de propósito). Não bateu para tags: o
cabeçalho da Etapa 3 dizia "10 na conta fora da numeração" e "Total na
conta hoje: 25", mas a própria frase ao lado já enumerava `teste-regua`,
`fechar-horario`, `cadencia-12x30-p2`, `teste-12x30` e "as 8 do Espelho de
Etapa" — 1+1+1+1+8 = **12**, não 10; com as 15 tags do projeto já criadas
(T-01 a T-15), o total real é **27**, não 25. O mesmo "10" tinha sido
copiado para `APROVADO.md` ("são dez as tags fora desta lista", mesma
enumeração de 12 ao lado) e o mesmo "25" para `build-wesales.md` §2.32
("a conta tem 25 tags: 15 do projeto, `teste-regua`, `fechar-horario`,
`cadencia-12x30-p2`, `teste-12x30` e as 8 do espelho" — a própria frase soma
27 na cara de quem lê, mas o número escrito ficou 25). As tags `T-16` a
`T-21` (ainda `[ ]` em `APROVADO.md`) não entram nesta conta — são tags do
projeto ainda não criadas, não tags "fora da numeração"; nenhuma decisão do
dono muda com esta correção.

**Como aconteceu:** todas as três menções nasceram na mesma noite de
23/09/2026, em rodadas próximas — a primeira (`campos-e-tags.md`, quando só
`teste-regua`/`fechar-horario` existiam) dizia "duas", correta para aquele
momento; quando o commit `61eb167` trouxe as 8 tags do Espelho de Etapa, a
atualização somou 2 (as originais) + 8 (o espelho) = 10 e **esqueceu**
`cadencia-12x30-p2`/`teste-12x30`, que já estavam registradas na mesma
tabela, duas linhas abaixo — cada versão seguinte copiou o "10"/"25" errado
sem resomar a lista. **Regra prática, generalizável, que estende a do G-10
(um achado consertado num lugar não se propaga sozinho) para números em vez
de nomes:** grep acha nome de etapa órfão e merge field trocado, mas não
acha soma errada — uma conferência de coerência que só procura texto
divergente vai deixar passar um total que "parece" atualizado (foi editado
na mesma rodada que acrescentou o dado novo) mas nunca foi resomado contra
a própria enumeração ao lado. A partir daqui, a varredura de toda rodada
que mexer em contagem (campo, tag, etapa) soma a lista antes de aceitar o
número escrito ao lado dela, não só depois de mudar algo.

**Correção aplicada:** `campos-e-tags.md` (Etapa 3) ganhou a mesma
convenção "onde mora a contagem" que a Etapa 2 (campos) já tinha, com os
números certos (12/27) e a data desta correção; `APROVADO.md` e
`build-wesales.md` §2.32 pararam de repetir o número (regra deste roadmap,
"número fixo só na fonte") e passaram a apontar para `campos-e-tags.md`.
Zero campo, zero tag, zero escrita no CRM: item de coerência entre
documentos, não depende de `APROVADO.md`.

### G-21 · A pendência 9c (`Canal que conectou`, decisão do dono já dada) tinha patch escrito e validado desde `dac443f` e nunca virou item rastreável — mesma classe do G-16/G-17/G-18/G-19 — **FEITO em 23/09/2026 (promoção + achado de instrução que fica errada quando o patch completar)**

**Por quê:** CRM reconfirmado por API nesta rodada — 56 oportunidades, mesma
composição da leitura do G-20 (48 `NOVO LEAD` open + 1 abandoned + 1
`REUNIÃO DE DIAGNÓSTICO` open + 1 `CONECTAR` open + 2 `CONECTAR` lost + 2
`NEGOCIAR` open + 1 `NEGOCIAR` lost), 56 campos de contato — G-03, G-04
(peça 2), F-09, F-10, G-11 (item 1) e G-19 seguem aguardando o dono, sem
novidade. O achado não veio de grep por nome nem de contagem: veio de
reler, como o G-16/G-17/G-19 já ensinaram, um documento que mede e nunca
promove — `ESTADO-E-PLANO.md`, seção 8, linha `9c`. O dono já decidiu essa
pendência em 23/09/2026 ("automático onde o ramo já sabe, manual no
resto"), uma sessão em paralelo já escreveu e validou o patch da metade
automática (`dac443f`, `wesales/tools/patch_canal_conectou.py`,
`build-wesales.md` §2.41) — mas a decisão e o patch nunca ganharam item de
roadmap próprio, e a linha 9c de `ESTADO-E-PLANO.md` ainda dizia "falta o
patch", que não é mais verdade (o patch existe; falta **aplicar**, e depois
estender). Mesmo padrão exato do G-19: achado medido e documentado em dois
lugares, sem "Pronto quando" rastreável em nenhum dos dois.

**O que o patch cobre, e o que fica de fora por sequenciamento — resumo do
§2.41 (detalhe completo lá, não repetido aqui):** grava `Canal que
conectou` = `Mensagem` em dois ramos que já sabem a resposta
(`Interceptação de Sinal — Resposta v2`, sinal quente; `Triagem da
Nutrição`, ramo "Quer conversar?"). Fica de fora, por enquanto, o
`Pós-ligação v2` — que também já sabe o canal (testa `fila-wa` logo depois
de gravar `Resultado da tentativa`: presente é WhatsApp, ausente é ligação
normal) — porque a extensão mexeria nos mesmos ramos `Atendeu` que o
`patch_remove_atendeu.py` do G-18 ainda não aplicado vai alterar; aplicar
os dois fora de ordem arrisca um sobrescrever o nó do outro. Ordem
correta, já registrada no próprio §2.41: aplicar o G-18 primeiro,
re-exportar o dump, só então estender este patch ao `Pós-ligação v2`.

**Achado novo desta rodada, que nenhuma das duas leituras anteriores
(9c em `ESTADO-E-PLANO.md`, §2.41 em `build-wesales.md`) tinha escrito:**
`GUIA-SDR.md` (seção "Depois de cada ligação: marque 2 campos") instrui o
SDR a preencher `Canal que conectou` na tela **toda vez que marca
`Atendeu`** — instrução certa **hoje**, porque nada grava esse campo
automaticamente ainda para o caminho do telefone. Mas o `Pós-ligação v2` é
exatamente o ramo que decide `Atendeu`, e é exatamente o ramo que a
extensão do §2.41 vai automatizar quando o G-18 destravar — ou seja, no dia
em que as duas aplicações completarem, `GUIA-SDR.md` passa a pedir ao SDR
um preenchimento manual que o sistema já faz sozinho para todo caso que
existe hoje (a pendência 9c, ao decidir "automático onde o ramo já sabe",
não deixou nenhum caso órfão de "onde não sabe" no telefone — só no
WhatsApp, e esses dois já estão cobertos pelo patch atual). Duplicar não é
neutro: o SDR pode marcar um valor por hábito ou engano que sobrescreve o
que o workflow acabou de gravar corretamente, o mesmo risco de dado que o
G-06 já tratou para outro campo. **Não é para corrigir agora** — corrigir
antes da automação existir deixaria o campo sem preenchimento nenhum,
pior que o duplicado de hoje —, é para não ficar esquecido quando a hora
chegar, mesma razão de existir de todo "Pronto quando" deste roadmap.

**Como:** nada disto sai por este conector — é decisão já dada (não abre
pendência nova para o dono), patch já escrito (não abre trabalho de
especificação novo) e instrução de guia (`GUIA-SDR.md`) que só deve mudar
depois que a automação estiver no ar, não antes. O trabalho desta rodada é
só a ponte que faltava: registrar aqui, com "Pronto quando" próprio, para a
aplicação não ficar represada em três documentos sem nenhum deles apontar
para os outros dois.

**Pronto quando:** (1) `patch_remove_atendeu.py` (G-18) aplicado e
re-exportado; (2) `patch_canal_conectou.py` estendido ao `Pós-ligação v2`
nos mesmos moldes do §2.41 (grava por ramo, sem nó novo onde já existe
`update_contact_field`), validado por `--dump` e aplicado; (3) `GUIA-SDR.md`
atualizado para não pedir mais o preenchimento manual de `Canal que
conectou` nos casos que passaram a ser automáticos — só então o campo
some da lacuna "nem escrito nem lido" da `auditoria_campos.py` de vez, sem
duplicidade. Zero campo, zero tag novos (o campo já existe desde
23/09 01:06); zero escrita no CRM por esta sessão — patch e guia esperam
aplicação manual, mesma classe de F-11/F-12/F-13/F-15/G-07/G-08/G-11
(itens 2/3)/G-18.

**Correção de coerência aplicada nesta rodada, nos três documentos que
falavam do mesmo achado sem se citar:** `ESTADO-E-PLANO.md` (linha 9c)
passou a apontar para este G-21, mesmo padrão de 0→G-16/9e→G-17/
11a-11b→G-19; `campos-e-tags.md` (nota sobre o quarto campo fora da lista,
Etapa 2) parou de dizer "nenhum nó... o lê ou escreve ainda" (falso desde
o `dac443f`) e passou a citar o patch e o G-21; `build-wesales.md` §2.34
(que sugeria a correção direto no `Pós-ligação v2`, sem saber do
sequenciamento com o G-18) ganhou uma nota apontando para o §2.41, para
ninguém implementar a sugestão antiga por cima do patch do G-18.

### G-22 · O agente de IA que existe só para alcançar os 5 leads do Instagram nunca confirmou se alcança — e a "regra do portão" mais importante do próprio desenho depende de um filtro de tela nunca visto — **FEITO em 23/09/2026 (especificação nó a nó completa)**
**Por quê:** `AGENTE-IA-CONEXAO.md` diz da própria razão de existir, na
abertura: "Leads reais do Instagram, sem telefone e sem e-mail: **5**... O
trabalho do agente é esse: ser o canal de quem chega por mensagem e não
tem telefone... Não é 'mais um canal' — é o único caminho para essa fatia
da base" (confirmado pelo F-15: dos 9 contatos sem telefone, 8 também não
têm e-mail, e nenhuma régua de e-mail os alcança). A própria seção 8 do
documento, item 2, registra em aberto desde 22/09/2026: "Se ele só
responde WhatsApp, não alcança os 5 do Instagram — que são o motivo
principal dele existir" — dúvida sobre o único canal que resgata esses 5
leads, nunca promovida a item rastreável (mesma classe de
G-16/G-17/G-19/G-21: achado registrado em documento vizinho, nunca virou
item de roadmap com "Pronto quando"). Mais grave: a seção 1 do mesmo
documento — título do próprio documento para ela, "a regra do portão — a
mais importante" (não deixar o agente responder lead que já está com o
SDR: tags `fila-tel`/`conectado-hoje`/`nao-perturbe`/`pausado`/
`fechar-horario`) — depende de um filtro de tag na aba de configuração do
agente que ninguém confirmou existir; o item 3 da mesma seção 8 já avisa
"se a tela não oferecer filtro por tag... o agente não deve ficar como
Agente Principal até existir". Ou seja: a única proteção contra o SDR e a
IA falando com o mesmo lead ao mesmo tempo pode não existir na tela, e
ninguém saberia até testar ao vivo com lead real.
**Como:** pesquisado antes de decidir (`WebSearch`, confiança média —
documentação oficial da HighLevel e convergência entre buscas com termos
diferentes; `help.gohighlevel.com` bloqueado pelo proxy deste ambiente
para leitura direta via `WebFetch`, mesma limitação já registrada no
G-05/F-08/F-12 — não testado nesta subconta). Duas respostas: uma reduz a
dúvida do item 2, a outra substitui a dúvida do item 1 por um mecanismo
mais confiável, sem esperar tela nenhuma.

1. **Item 2 (alcance) — resposta parcial.** Instagram é canal nativamente
   suportado por Conversation AI Bot Channels ("Manage Conversation AI Bot
   Channels and Routing", HighLevel Support Portal) — a IA v2 não está
   limitada a WhatsApp por design da plataforma. Continua sem confirmação
   de tela **qual canal/página** a aba `IA · proximo-cliente-1` desta
   subconta tem ligada de fato (mesma pendência de tela que o G-09 já
   deixou para WhatsApp/Stevo, agora estendida a Instagram) — a pergunta
   deixa de ser "o produto suporta isto?" (respondida) e vira "esta
   subconta está configurada assim?" (só a tela responde).

2. **Item 1 (portão) — troca de mecanismo.** A mesma documentação descreve
   "Channel Management" como roteamento por página/número/widget **e tag
   de contato**, com a regra "atribuição mais específica vence a mais
   genérica" — é roteamento por **prioridade**, não uma lista de exclusão
   como a seção 1 do `AGENTE-IA-CONEXAO.md` assume ("o agente não responde
   contato que tenha qualquer destas tags"). Usar esse caminho exigiria uma
   combinação de prioridade por tag para cada uma das 5 tags de bloqueio, e
   continua sem confirmação de tela. Existe um caminho mais direto,
   documentado com o mesmo nome em três fontes independentes (HighLevel
   Support Portal, HighLevel Changelog/Ideas, e um tutorial de terceiro
   descrevendo a mesma tela): a ação de workflow nativa **`Update
   Conversation AI Bot and Status`**, que liga/desliga um bot específico
   **por contato** (`Active`/`Inactive`), chamável de **qualquer**
   workflow — mesma classe de ação já usada no projeto inteiro (`Update
   Contact Field`, `Add/Remove Contact Tag`), não uma configuração de tela
   nova. Diferente do filtro da aba `IA`, aqui a garantia não depende de
   nenhuma tela: é o próprio conjunto de tags que já existe que liga e
   desliga o bot.

   **Desenho novo, isolado do que já está publicado — não toca a Cadência
   12x30 nem o Pós-ligação v2 já no ar** (regra de não editar workflow
   publicado por este conector, e de não arriscar automação viva por uma
   peça nova), no mesmo padrão de "removedor em workflow à parte" que o
   dono já escolheu para `conectado-hoje` (`ESTADO-E-PLANO.md`, pendência
   7 — sidecar por tag, gatilho nativo, zero edição em workflow publicado):

   | Workflow novo | Gatilho | Condições | Ação |
   |---|---|---|---|
   | **"Bot IA — Pausar por Fila"** | `Tag Added` — `fila-tel` OU `fila-wa` OU `conectado-hoje` OU `nao-perturbe` OU `pausado` OU `fechar-horario` (confirmar na tela se o gatilho aceita lista "qualquer uma destas" num filtro só, ou se precisa de 6 gatilhos separados no mesmo workflow apontando pro mesmo primeiro nó — o removedor de `conectado-hoje` que o dono já publicou usa `Tag Added`, então o gatilho em si já está testado neste projeto) | — | `Update Conversation AI Bot and Status` → bot `Conexão — Inbound` → `Inactive` |
   | **"Bot IA — Retomar"** | `Tag Removed` — mesma lista de 6 tags | If/Else: nenhuma das 6 tags presente no contato (checar as 6, não só a que disparou o gatilho — remover uma não garante que as outras sumiram) | Verdadeiro → `Update Conversation AI Bot and Status` → bot `Conexão — Inbound` → `Active`. Falso → fim, sem ação (ainda bloqueado por outra tag) |

   Fica valendo em paralelo ao filtro de tag da tela, se ele existir de
   verdade — as duas camadas não competem (a de workflow é a que este item
   garante; a de tela, se existir, só reduz ainda mais a chance de
   sobreposição).

**Zero campo, zero tag novos** (as 6 tags já existem, `campos-e-tags.md`);
**zero escrita no CRM** — as leituras de `locations_get-custom-fields` e
`opportunities_search-opportunity` desta rodada foram conferência de
coerência (56 campos, 56 oportunidades, mesma composição da leitura do
G-21), sem gravar nada: item de pesquisa e especificação, não depende de
`APROVADO.md` — a criação dos dois workflows novos não sai por API (mesma
limitação de sempre), fica para a montagem manual, mesma fila do resto do
projeto.
**Pronto quando:** os dois workflows ("Bot IA — Pausar por Fila", "Bot IA
— Retomar") estão publicados e testados contra um contato de teste
(aplicar cada uma das 6 tags, uma de cada vez, confirmar que o bot vai
para `Inactive`; remover todas, confirmar `Active`); `AGENTE-IA-CONEXAO.md`
§1 e §8 (itens 2 e 3) não descrevem mais o filtro de tela como única
defesa; e a pergunta "esta subconta tem Instagram ligado à aba `IA ·
proximo-cliente-1`?" (item 2) tem resposta de tela, não só de
documentação de produto.

**Resumo:** achado por releitura de documento represado (mesma família de
G-16/G-17/G-19/G-21 — "achado técnico completo num documento vizinho,
nunca promovido a item rastreável"), desta vez sobre
`AGENTE-IA-CONEXAO.md`; a pesquisa de mercado que este roadmap sempre
manda fazer, aplicada desta vez à própria plataforma que Reev/Meetime/
Outreach/Salesloft tentam imitar por fora (não a um concorrente), trocou
uma dependência de tela não confirmada por um mecanismo de workflow
nativo, testável e que não compete com o que já existe.
`AGENTE-IA-CONEXAO.md` (§1, §8) atualizado nesta rodada com o achado e a
tabela acima.

---

### G-23 · O F-13 (`negociacao-estagnada`) já estava publicado com um desenho diferente do especificado, e um segundo alerta (`proposta-pendente`) já cobria um buraco que nenhum documento tinha registrado — achado ao cruzar `GUIA-CLOSER.md`, nunca lido lado a lado com `PLANO-MULTICANAL.md` — **FEITO em 23/09/2026 (coerência entre spec e publicado — a execução já existia)**

**Por quê:** seguindo a instrução de sempre ("variando a fonte da
varredura de coerência a cada vez"), esta rodada cruzou `GUIA-CLOSER.md` —
nenhuma rodada da família G-16/G-17/G-19/G-21/G-22 tinha chegado nele
ainda. Ele descreve dois alertas do gestor: **"Proposta parada"** (Sim do
closer, 3 dias, ainda em REUNIÃO DE DIAGNÓSTICO) e **"Negociação parada"**
(5 dias em NEGOCIAR). A especificação do F-13 (`build-wesales.md`, seção
2.28) só cobre o segundo, e com **3 dias**, não 5 — a primeira reação foi
tratar isso como número desatualizado em `GUIA-CLOSER.md` (mesma classe de
F-09/F-14) e desenhar do zero um workflow novo para o primeiro alerta, que
parecia nunca ter sido especificado.

**As duas coisas estavam erradas, e um `grep` por `PLANO-MULTICANAL.md`
antes de escrever a primeira linha do desenho evitou publicar em cima do
que já existe.** O item A5 daquele documento (23/09 01:10, `tools/
build_estagnacao.py`, lido nó a nó direto do script no repo) mostra que o
**dono já construiu e testou os dois alertas**, com um desenho que diverge
do F-13 em três pontos: (1) `Negociação Estagnada` usa **5 dias**, não 3 —
`GUIA-CLOSER.md` estava certo, a especificação é que ficou para trás; (2)
o gatilho real é `Opportunity Stage Changed → NEGOCIAR`, não `Contact
Changed` em `Reunião foi qualificada`; (3) existe um segundo workflow,
**"Proposta Pendente"** (tag `proposta-pendente`, nunca catalogada em
nenhum documento até este achado), cobrindo exatamente o buraco que o F-13
original deixava — closer marca `Sim` e nunca move a oportunidade para
`NEGOCIAR` — com gatilho `Contact Changed`, 3 dias, condicionando pela tag
`etapa-reuniao` (Espelho de Etapa) em vez de ler a etapa da oportunidade
direto, mesmo motivo já registrado no G-08. As duas tags já existem na
subconta (criadas pelo dono, fora do `[x]` deste projeto) e os dois
workflows já foram testados contra o contato 9940.

Por um instante esta rodada quase repetiu, na prática, o próprio erro que
motivou a "regra do `git fetch`" do G-10/G-16 (reconciliação em paralelo):
a diferença é que aqui não havia commit paralelo para achar com `git
fetch` — o trabalho já publicado vivia num documento (`PLANO-MULTICANAL.md`,
seção "Fila autônoma") que o próprio G-19 já tinha marcado como não lido
por inteiro por nenhuma rodada desta família, e que esta rodada só
consultou depois de já ter escrito um desenho especulativo e precisar
revertê-lo.

**Como:** nenhum workflow novo — reconciliação de seis documentos com o
publicado, usando `wesales/tools/build_estagnacao.py` como fonte primária
(mais confiável que reconstruir de memória ou pela descrição em prosa do
`PLANO-MULTICANAL.md`):

1. `campos-e-tags.md` — T-21 (`negociacao-estagnada`) corrigida (5 dias,
   gatilho real, já criada pelo dono, não `[ ]` pendente); T-22
   (`proposta-pendente`) criada, mesmo tratamento.
2. `APROVADO.md` — nota "Registro, não aprovação" sob a linha da T-21 (mesmo
   padrão de `fechar-horario`/Espelho de Etapa: campo/tag que o dono cria
   pelo próprio caminho não é esta rotina se autorizando) e linha nova para
   a T-22.
3. `build-wesales.md`, seção 2.28 — aviso no topo apontando para o
   publicado real (nós do "Proposta Pendente" incluídos), "Pronto quando"
   do F-13 e do novo item marcados como cumpridos pelo desenho real, nó 4
   do Mestre de saída ganhou `proposta-pendente`, Smart List nova 8.29
   `Saúde — Proposta Pendente` especificada (espelho da 8.28).
4. `IMPLEMENTACAO-WORKFLOWS.md` — tabela de status de tags, registro W22
   (com o desenho publicado real, nó a nó, e a especificação original
   preservada como registro), tabela de Smart Lists (8.29 nova), nó 4 do
   Mestre de saída.
5. `GUIA-MONTAGEM.md` — as duas linhas da "Ordem de montagem" que ainda
   diziam "dá para fazer quando alguém abrir a tela" riscadas como já
   feitas, com nota do que de fato falta (só as duas Smart Lists).

**Divergência que fica registrada, não resolvida nesta rodada:** o
`Mestre de saída v2` publicado (`tools/patch_mestre_tags.py`,
`PLANO-MULTICANAL.md` A8) já limpa quatro tags a mais do que a seção 3 de
`build-wesales.md`/`IMPLEMENTACAO-WORKFLOWS.md` documentam
(`cad-outbound`, `cadencia-12x30-p2`, `fechar-horario`, `toque`) — fora do
escopo do F-13/G-23, registrado nos dois documentos para a próxima rodada
não redescobrir.

**Zero campo, zero tag criados por esta sessão (as duas já existiam antes
de esta rodada começar), zero escrita no CRM: item de coerência entre
especificação e publicado, não depende de `APROVADO.md`.** CRM
reconfirmado por API nesta rodada: 56 oportunidades, mesma composição da
leitura do G-22 (48 `NOVO LEAD` open + 1 `NOVO LEAD` abandoned + 1 `REUNIÃO
DE DIAGNÓSTICO` open + 1 `CONECTAR` open + 2 `CONECTAR` lost + 2 `NEGOCIAR`
open + 1 `NEGOCIAR` lost), 56 campos de contato — `git fetch` limpo
(nenhum commit novo na janela desta leitura): G-03, G-04 (peça 2), F-09,
F-10, G-11 (item 1) e G-19 seguem sendo as seis decisões que esperam o
dono, sem novidade.

**Pronto quando:** feito. Os seis documentos citados em "Como" batem com o
que `tools/build_estagnacao.py` e `PLANO-MULTICANAL.md` A5/A8 já
publicaram; falta só montar as duas Smart Lists na tela (mesma fila manual
do resto do projeto, sem bloqueio novo).

**Resumo:** achado por varredura de coerência sobre um documento nunca
cruzado (`GUIA-CLOSER.md`) — mas, diferente de G-16/G-17/G-19/G-21/G-22
(achado represado que nunca tinha desenho), aqui o desenho, a publicação
**e** o teste já existiam; o trabalho real desta rodada foi perceber isso
antes de duplicar, e só depois reconciliar a documentação com a realidade.
O lembrete que fica: quando um achado parece "buraco nunca especificado",
checar `PLANO-MULTICANAL.md` (seção "Fila autônoma") e `wesales/tools/`
antes de desenhar — a resposta pode já estar publicada.

### G-24 · O próprio G-23 fechou sem o parágrafo de fechamento que todo G-16/G-17/G-19/G-20/G-21/G-22 ganhou nesta seção, e a lista "documentos ainda não cruzados" continuava citando o documento que o G-23 acabara de cruzar — **FEITO em 23/09/2026 (coerência da própria seção "Ordem sugerida")**

**Por quê:** `git fetch` limpo (nenhum commit novo na janela desta leitura);
CRM reconfirmado por API — `opportunities_search-opportunity` (`status:
all`) segue em 56, mesma composição da leitura do G-23 (48 `NOVO LEAD` open
+ 1 `NOVO LEAD` abandoned + 1 `REUNIÃO DE DIAGNÓSTICO` open + 1 `CONECTAR`
open + 2 `CONECTAR` lost + 2 `NEGOCIAR` open + 1 `NEGOCIAR` lost) e
`locations_get-custom-fields` segue em 56 campos de contato: G-03, G-04
(peça 2), F-09, F-10, G-11 (item 1) e G-19 continuam sendo as seis decisões
que esperam o dono, sem novidade.

A lacuna não veio de grep por nome nem de contagem duplicada em prosa — veio
de aplicar a própria regra que fechou G-16/G-17/G-19/G-20/G-21 ("documento
medido não é o mesmo que documento rastreado") **à seção onde essa regra
mora**, não a um documento-irmão. Todo G-item fechado nesta família, de
G-16 a G-23, ganhou um parágrafo de recapitulação no fim da própria "Ordem
sugerida" — é o parágrafo que atualiza a lista de "decisões que esperam o
dono" e a lista de "itens com desenho completo, falta tela/PC" para quem lê
só o fim do arquivo. O G-23 foi o primeiro da família a não ganhar esse
parágrafo (a rodada fechou o item, mas não voltou ao fim do arquivo) — e o
parágrafo do G-22, escrito antes do G-23 existir, continuava dizendo que
`script-de-ligacao.md`, `GUIA-CLOSER.md`, `GUIA-SDR.md` e `conectar.md`
"ainda não passaram por nenhuma rodada desta família", quando `GUIA-CLOSER.md`
já tinha passado — o próprio G-23.

Seguindo a instrução de sempre ("variando a fonte da varredura de coerência
a cada vez"), esta rodada cruzou os três documentos que sobravam da lista —
`script-de-ligacao.md`, `GUIA-SDR.md` e `conectar.md` — contra as decisões
publicadas mais recentes (`PLANO-MULTICANAL.md` D1-D14 e A1-A9,
`tools/build_estagnacao.py`, `tools/patch_closer_tarefa.py`) e não achou
gatilho, campo, tag ou número que divergisse do que os três já descrevem:
`GUIA-SDR.md` já reflete a etapa `REUNIÃO DE DIAGNÓSTICO` (não `AGENDAR`), o
teto de 100 toques/50 tarefas vencidas (D14) com os números certos, e a
tabela de `Resultado da tentativa` com a opção `Desqualificado` (R-18) já
presente; `script-de-ligacao.md` já tem a pendência de gravação/LGPD do F-06
datada e correta (transcrição ligada, gravação por número desligada, medido
22/09 19:00 UTC); `conectar.md` é só infraestrutura de conexão, sem conteúdo
de workflow para divergir. **Achado negativo, não vazio**: os três
documentos batem com o publicado — a varredura serviu para fechar a lista,
não para achar item novo.

**Como:** um parágrafo só, no fim desta seção (abaixo), fazendo o que os
parágrafos de G-16 a G-22 já faziam: recapitular as seis decisões do dono,
confirmar que nada mudou nelas, e substituir a lista de documentos
pendentes por uma vazia — os quatro nomes que o G-22 tinha deixado (um
cruzado pelo G-23, três por este item) saem da lista de "ainda não
cruzados". Nenhum documento fora da seção "Ordem sugerida" foi tocado: o
achado é sobre a própria seção, não sobre `GUIA-CLOSER.md`/
`script-de-ligacao.md`/`GUIA-SDR.md`/`conectar.md`, que continuam corretos
como estavam.

**Zero campo, zero tag, zero escrita no CRM: item de coerência dentro do
próprio roadmap, não depende de `APROVADO.md`.**

**Pronto quando:** feito — este parágrafo e o de fechamento abaixo são o
próprio "Pronto quando".

**Resumo:** o roadmap tem uma seção cujo trabalho é resumir as outras; essa
seção também pode ficar desatualizada, e ninguém a audita porque ela *é* a
auditoria. A partir de agora, todo G-item que fechar nesta família confere,
antes do commit, se o próprio parágrafo de fechamento foi escrito — não só
se o item foi especificado.

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

**Nota de 27/09/2026 (G-27, abaixo):** um campo `SDR responsável` apareceu
na tela — exatamente o nome que este item pesquisou e decidiu não criar.
Não é uma reabertura desta decisão (a pesquisa e o motivo continuam
válidos): é um achado de coerência entre a decisão e a conta, com "Pronto
quando" e a pergunta ao dono no G-27.

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

### R-14 · Auditoria de compliance — especificação fechada em 22/09/2026; primeira medição real feita em 29/09/2026 (tag ⇔ DND global fecha); as listas 8.26/8.27 aguardam montagem na tela, com uma correção de filtro

> **Conferido no mesmo dia** (`build-wesales.md`, 8.26): duas correções. (a) O
> filtro da 8.26 nasceu com `E` onde o espelho dela (8.27) usa `OU` — com `E`
> ela só acusava quem está desprotegido nos **dois** canais, deixando escapar a
> tag com ligação bloqueada e WhatsApp livre, que é o caso perigoso **e** o mais
> provável (basta um nó chamar `Set Contact DND` num canal só). Corrigido: "zero
> linha" só prova o que o item diz provar com `OU`. (b) A documentação diz que as
> preferências de DND de WhatsApp/Messenger/GMB **só aparecem depois que o app
> está integrado**, e daí eu concluí que quem pede silêncio hoje não ficaria
> protegido em WhatsApp. **Medido ~1h depois: errado.** `dndSettings` de
> `Teste Atendeu` tem `WhatsApp: active`, escrito por workflow, nesta subconta
> que **não** tem WhatsApp integrado — a flag é gravável num canal que a tela não
> expõe. Quem pede silêncio **fica** protegido, e não há retroatividade a
> corrigir. O erro foi aplicar à **escrita** uma frase da fonte que era sobre
> **leitura** (o que a tela mostra, o que o filtro oferece). **Sobra só a
> auditabilidade:** se o filtro `WhatsApp DND` não existir sem integração, as
> listas 8.26/8.27 se montam com a cláusula de ligação apenas — a proteção está
> inteira, a conferência dela é que fica parcial, e não há mais ação de véspera.
> **Brinde da mesma leitura:** `dndSettings[canal].message` carrega o **id do
> workflow** que ligou aquele DND (`Updated from workflow_cf6fa19d-…`) — primeira
> rastreabilidade de workflow que o projeto tem sem acesso à tela, e exatamente o
> que a 8.27 (`DND sem tag`) precisava para achar o caminho não documentado.

> **Prova de "ninguém incomodado depois do DND" — medida ao vivo em 29/09/2026
> (segunda metade do "Pronto quando").** Método, só leitura, cabe em qualquer
> sessão com o conector: (1) `contacts_get-contacts` (`query_limit=100`) →
> contatos com `dnd == true`; (2) `conversations_search-conversation`
> (`query_limit=100`) uma vez com `query_lastMessageDirection=outbound` e outra
> com `inbound` → `lastMessageDate` de cada conversa, que é o **teto** de
> qualquer mensagem daquele contato; (3) comparar com o `dateUpdated` do contato
> (o mais perto que a API pública dá de "quando o DND foi ligado").
> **Resultado:** todos os contatos com DND têm `lastMessageDate` **anterior** ao
> `dateUpdated`; zero envio depois do DND. Os contatos `zz teste …` não têm
> conversa nenhuma. Os dois grupos de WhatsApp (`grupo-whatsapp-nao-e-lead`)
> só recebem mensagem **inbound** (o grupo fala, a máquina não responde). O
> único envio automático a contato hoje com DND é o e-mail "Reunião confirmada"
> da Ana Lucia (duplicado do Calendly), enviado 07:38Z, no segundo em que o
> contato nasceu — antes de o duplicado ser marcado.
> **Limite honesto da prova:** `dateUpdated` é cota superior do instante do DND
> (qualquer tag nova o empurra), então a prova é forte para os DND antigos e
> **fraca para os das últimas horas** (Ana Lucia, os dois grupos, `teste não
> atende`, `zz teste estrutura`). Prova forte de verdade só vem de rodar isto
> **periodicamente** e comparar com a rodada anterior: enviado depois da rodada
> em que o contato já constava com DND = violação certa. Falta a rotina que
> grave essa foto (fica para quando houver token no Action — não desenhada aqui
> por não caber em API pública sem segredo). O que se prova hoje é o ponto no
> tempo, não a operação contínua: o item **continua aberto** por esse motivo.

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

**Medição real, 29/09/2026 — a espera por "mensagem real" venceu, e a
medição achou um defeito no próprio desenho.** A operação já manda
mensagem automática (e-mail de confirmação de reunião, áudios da SDR;
`conversations_search-conversation` com `lastMessageAction=automated`), então
o R-14 foi medido ao vivo em vez de esperar as listas na tela. Leitura de
todos os contatos por `contacts_get-contacts`: **tag `nao-perturbe` ⇔ `dnd`
global ligado, sem nenhuma divergência nos dois sentidos**, e zero envio
automático posterior ao DND nos contatos de teste que têm mensagem de saída.
O defeito: a maioria dos contatos com a tag tem `dndSettings` **vazio** — o
DND deles é o global, não a gravação por canal — e a 8.26 lê só filtros por
canal, então nasceria com linhas para sempre e o "sempre vazia" nunca
valeria. Correção (filtro geral primeiro, receita de conferência por MCP que
não depende de tela) em `build-wesales.md`, seção 8.26, "Primeira medição
real". Zero escrita no CRM; não depende de `APROVADO.md`. O que continua
aguardando o dono: montar as duas listas na tela e repetir a medição quando
houver `nao-perturbe` em lead real (hoje só há contatos de teste).

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

**Acréscimo à tabela, 23/09/2026, sessão automática seguinte — Presença
Local (DDD) pesquisada, nativo do HighLevel é US/Canada only, equivalente
manual não tem restrição.** Pesquisado como o roadmap manda (o que
Reev/Meetime/Outreach/Salesloft fazem que este item ainda não cobre):
`Local Presence Dialing` — escolher automaticamente um número da subconta
com o mesmo DDD do lead a cada ligação — é recurso nativo do HighLevel e
prática central de mercado em ferramentas de outbound americanas, mas
`WebSearch` confirma que é **suportado só para números dos EUA e Canadá**
(mesmo formato de descarte do `Voice Integrity`, correção acima). O que
não é US only: o Web App Softphone deixa o usuário escolher manualmente
qual número da subconta usar (dropdown "Calling From") antes de discar —
zero custo além dos números que este item já recomenda comprar por
reputação, zero engenharia. Vira acréscimo de uma linha na tabela já
publicada (`build-wesales.md`, seção 2.26) e instrução nova em
`GUIA-SDR.md`, não item de roadmap próprio — não muda o "Pronto quando"
deste F-08, já cumprido. Zero campo, zero tag, zero escrita no CRM.

---

### F-09 · O telefone não tem freio de canal — e desde a decisão de 100% telefone é o único canal da régua — **aguarda decisão do dono** (aberto em 22/09/2026, corrigido em 22/09/2026)

> **Correção de 22/09/2026, sessão automática seguinte — duas premissas
> venceram no dia em que o item nasceu, e nenhuma das duas tinha sido
> corrigida ainda aqui.** (1) O item foi escrito comparando telefone (8
> toques) contra WhatsApp (4 toques, com freio). A decisão de 100% telefone
> (`d52e61d`, mesma data, seção 2.5) mudou isso para **12 de 12** — o F-14
> (rampa de aquecimento) já recebeu esse mesmo conserto em `4d5bcf6`, cuja
> "regra que fica" (`APRENDIZADOS-CRM.md`) mandava reabrir todo item com
> tabela de toques por canal antes de fechar a rodada; F-09 ficou de fora até
> agora. Não é só o número: as opções A e B abaixo mandavam o telefone
> "desviar para WhatsApp" quando estourasse o limiar — **esse canal não
> aplica mais nenhum toque da régua**, então desviar não é mais uma saída
> possível, só encerrar a régua mais cedo é. (2) O dono já respondeu, ao
> vivo, a pergunta que a seção "Evidência indireta" mais abaixo registrava
> como aberta: as ligações desta operação saem por **LC Phone**
> (`APRENDIZADOS-CRM.md`, "Resposta do dono à pré-condição do W20/F-06/F-08/
> F-09", 22/09/2026 16:13 UTC). Isso não escolhe o limiar por conta própria —
> A/B/C continuam decisão do dono — só fecha a pergunta de infraestrutura que
> a seção abaixo ainda descrevia como sem resposta.

> **Correção de 28/09/2026 (G-38) — a premissa "12 de 12, único canal" já
> não descreve a operação real, e não foi nenhuma sessão deste roadmap que
> mudou isso.** O próprio dono, direto em código (não pela tela nem por
> `APROVADO.md`), publicou o PR #118 (`atuador_filas.py`, branches
> `abertura-operacao-dnd-n7dnjv`/`claude/stoic-hawking-tlxjtf`, commit
> `69e034a`, 28/09/2026 09:27 BRT — autor `Pablo Sampaio`, não sessão
> automática): telefone deixa de carregar os 12 toques e passa a carregar
> **7 dos 12** (toques 1,3,5,7,9,11,12); os toques 2,4,6,8,10 (**5 de 12**)
> viram ligação de WhatsApp, um canal que este item nunca tinha — o F-09 foi
> escrito comparando telefone contra "WhatsApp mensagem", não contra
> "WhatsApp ligação". Confirmado por API, não só pelo código: o campo
> `Canal da tentativa` (`AsZMGmsKVu1xEp36hyLb`, `SINGLE_OPTIONS`
> `Telefone`/`WhatsApp`, já registrado no G-32) e o campo `Canal que
> conectou` (`TxJmoWdkA8rTqC1uEsMW`, opções `Ligação WhatsApp`/`Ligação
> normal`/`Mensagem`, já registrado no G-21) existem na subconta real e
> gravam exatamente essa distinção. **O que isto muda, e o que não muda:**
> não decide nada das opções A/B/C abaixo — o limiar de corte continua
> escolha do dono — mas invalida a conta que a coluna "Efeito" fazia
> ("reduziria os 12 toques de telefone a talvez 2-3"): a base agora é 7, não
> 12, e dois desses 7 (a partir do toque 9) já vêm depois de um toque de
> WhatsApp ter rodado no meio, então "2 não atendidas seguidas de telefone"
> conta uma sequência que a régua real intercala com outro canal. Quem for
> escolher A/B/C precisa reler a tabela olhando para 7 toques de telefone
> intercalados, não para 12 seguidos. **O que também não muda:** a exposição
> regulatória que motivou o item (Despacho 82/2026/RCTS/SRC, F-08) segue
> valendo para os 7 toques de telefone que restam — só ficou menor, não
> zerada. Detalhe completo, achado pela mesma reconciliação entre branches
> que o G-31/G-32/G-33 já tinham deixado como hábito, no `### G-38` da seção
> "Ordem sugerida".

**Por quê:** achado ao conferir o F-08. O seletor de canal (nó 4 da seção
2.4; nó 3 da 2.10) é registro histórico da régua alternada (seção 2.5) — só
mandava pelo WhatsApp se `WA não atendidas seguidas` fosse **< 2**, duas sem
resposta seguidas e o lead saía daquele canal. Não existe equivalente para o
telefone, o único canal que resta: conferido por `grep` em todo o
`wesales/`, `WA não atendidas seguidas` é o **único** contador de "seguidas"
do projeto, e o nó 10 das duas cadências manda `Caixa Postal` e `Não
atendeu` **insistirem** até o fim da régua.

| Canal | Toques dos 12 | Freio próprio |
|---|---|---|
| Telefone | **12** (era 8 antes de 22/09/2026 — seção 2.5) | **nenhum** |

O único canal da régua, o único com regulador olhando (Despacho Decisório nº
82/2026/RCTS/SRC — F-08), e o único sem freio — os três agora coincidem no
mesmo canal, quando antes eram três fatos sobre canais diferentes. Pior: os
critérios que a norma manda a operadora considerar são **proporção de
chamadas de curtíssima duração, duração média e taxa de completamento** — as
três pioradas exatamente pelas tentativas que insistem sem conectar, e o
volume que bate nesses critérios dobrou junto com os toques (seção 2.5,
"Efeito colateral a considerar"). É a mitigação mais barata do F-08: não
custa número novo, cadastro nem esperar a `Origem Verificada` aceitar a
subconta.

**Como (proposta, não executada):** campo novo `Tel não atendidas seguidas`
(NUMERICAL), somado no ramo `Não atendeu`/`Caixa Postal` do Pós-ligação e
zerado em toda conexão real — espelho exato do que o nó C1 (`IMPLEMENTACAO-
WORKFLOWS.md`, W4) já fazia para o extinto contador de WhatsApp; depois um
portão, ~~no seletor de canal e/ou~~ no nó 10, que ao estourar encerre a régua
mais cedo (não há mais canal para desviar).

> **Duas correções de 22/09/2026, 19:20 UTC, sobre este mesmo "Como".**
>
> **1. "Encerra a régua" não pode ser um `Remove from Workflow` seco** — e do
> jeito que está escrito, é o que alguém montaria. Este projeto já tem uma
> saída limpa canônica, o nó 3b da 12x30 (seção 2.4 do `build-wesales.md`):
> **Remove Contact Tag `fila-tel`, `fila-wa`, `fila-quente` → Add Contact Tag
> `limpar-tarefas` → Remove from Workflow: este**. Sem os dois primeiros
> passos, o lead cortado pelo limiar sai da régua **carregando `fila-tel` e
> com tarefa órfã aberta**.
>
> E aí encontra outro item deste roadmap: o **F-05 peça 2 (`Fila Travada`,
> seção 2.21)** dispara exatamente sobre "`fila-tel` ainda presente depois
> das 18:30, porque o nó 9 não rodou". Um portão do F-09 sem saída limpa
> produziria **um alerta falso de fila travada por lead cortado**, todos os
> dias, para sempre — e o gestor aprenderia a ignorar o monitor, que é o
> único aviso de fila parada que a operação tem. Nenhum dos dois itens está
> errado sozinho; é a junção que quebra, e ela só aparece quando se escreve
> **como** a régua encerra, não que ela encerra.
>
> **2. "No seletor de canal" é resíduo da régua alternada.** Com 100%
> telefone não existe mais seletor de canal para pendurar portão nenhum
> (seção 2.5). O lugar é o nó 10, e só. Risquei acima em vez de apagar,
> porque a frase mostra de onde veio.
>
> Nada disso muda as três opções A/B/C abaixo — o limiar continua sendo
> decisão do dono. Muda o que precisa estar desenhado **antes** de qualquer
> uma delas virar `[x]`.

**Por que não executo sozinho:** o limiar **é** a régua. Cortar o telefone
na 2ª não atendida seguida reduziria os 12 toques de telefone a talvez 2-3
por lead — mexe direto na meta de 100 ligações/dia do `briefing-sdr.md` e na
conta de volume da L-05, e mexe mais fundo agora que são 12 toques e não 8.
Pode ser exatamente o que se quer (menos discagem morta, mais tempo em lead
que atende), ou o oposto (insistir é o jeito de furar base fria). É decisão
de negócio, e a regra do briefing é não criar campo nem mexer em régua em
massa sem confirmação.

**Três opções para o dono escolher — nenhuma aplicada:**

**Evidência indireta, registrada em 22/09/2026 e resolvida horas depois no
mesmo dia:** a pergunta "as ligações saem por LC Phone ou por linha própria
do SDR?" não tinha resposta por API — `locations_get-location` mostrava
`saasSettings.twilioRebilling = { enabled: true, markup: 20 }`, mas esse
markup é definido **global na agência** (SaaS Configurator), compatível com
o valor herdado mesmo numa subconta que nunca ligou; e as 50 conversas da
subconta traziam **zero registro de chamada** (`TYPE_CALL`), o que não
desempata (pode não haver número, ou haver e nunca ter sido usado). O dono
respondeu ao vivo horas depois: **LC Phone** (ver banner de correção no
início deste item). A pergunta de infraestrutura está fechada; o limiar
(A/B/C abaixo) continua em aberto. Detalhe da evidência indireta em
`APRENDIZADOS-CRM.md`, "O CRM não pode responder a pergunta do LC Phone".

| Opção | Limiar | Efeito |
|---|---|---|
| **A — mais protetora** | 2 não atendidas seguidas → encerra a régua para aquele lead | Corta mais fundo os 12 toques; menos discagem morta, mais leads saindo da régua sem esgotar as 12 tentativas |
| **B — meio caminho** (recomendo começar aqui) | 4 não atendidas seguidas → encerra a régua para aquele lead | Mantém boa parte da insistência (metade das 12 tentativas garantida) e ainda melhora as três razões da norma; reversível |
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

**Atualização 23/09/2026, sessão automática seguinte — a marca de 48h foi
cruzada, e o recorde da própria base mais que triplicou.** Reconfirmado por
API (`opportunities_search-opportunity`, `status: all`) às 17:07 UTC: 56
oportunidades, mesma composição das leituras de G-16 a G-20 (49 `NOVO LEAD`
open + 1 `REUNIÃO DE DIAGNÓSTICO` open + 1 `CONECTAR` open + 2 `CONECTAR`
lost + 2 `NEGOCIAR` open + 1 `NEGOCIAR` lost) — nenhuma oportunidade nova
desde a última leitura. **Um minuto depois** (17:08 UTC), o G-16 fechou por
inteiro numa sessão em paralelo: a oportunidade da `Francisca` saiu de
`NOVO LEAD`/`open` para `NOVO LEAD`/`abandoned` (detalhe no próprio G-16,
acima) — a composição correta a partir daquele instante é **48** `NOVO LEAD`
open + 1 abandoned, não mais 49 open. O lead com `source: Facebook` mais
novo continua sendo `Carlos Andrade`, `21/09/2026 09:17:26 UTC` — os
contatos criados depois dele (22-23/09: `Sem nome`, `O Próximo Cliente`,
`Pablo Sampaio`, `Francisca`, `156766977421470`, `ZZ Teste Porta Inbound`)
são todos teste do dono ou, no caso da `Francisca`, contato pessoal (G-16),
nenhum com `source: Facebook` — nenhum muda o tempo sem lead **pago** que a
tabela abaixo mede.

| Fato | Valor |
|---|---|
| Agora | 23/09/2026 17:07 UTC (14:07 em `America/Sao_Paulo`, quarta-feira, horário comercial) |
| Tempo sem lead novo pago | **55h50min e subindo** |
| Maior intervalo já observado antes deste episódio (20/09 18:11 → 21/09 09:17) | 15h06 |
| Múltiplo do recorde anterior | **3,7×** — era 1,61× na última leitura registrada deste número (22/09 09:36 UTC) |
| Dias cobertos pelo silêncio | segunda, terça e quarta — três dias **úteis**, não é hiato de fim de semana |

Não é mais "o maior silêncio já visto por uma margem" — é o maior silêncio
por uma margem que **mais que dobrou** desde a última leitura registrada (de
1,61× para 3,7× em cerca de 31h30min). O gap de 22/09 já tinha cruzado o
recorde antigo; este não é o mesmo evento medido de novo, é o mesmo evento
**persistindo** um dia inteiro a mais depois de o item ter sido aberto (F-10
abriu em 22/09; hoje é 23/09, e o silêncio de entrada não teve uma única
exceção entre as duas datas). A cada leitura que reconfirma "sem lead novo",
a hipótese que o item já levantava
("campanha pausada, orçamento esgotado, formulário com problema ou criativo
reprovado") fica mais provável que a alternativa ("dia fraco, vai
normalizar"): a janela em que a entrada funcionava trouxe 10 leads em 34h30;
esta janela sem nenhuma entrada já passa de 55h — mais que o dobro do tempo
sem sequer repetir um décimo do resultado.

**O que isto muda, e o que não muda:** não desbloqueia a opção (b) sozinho —
o alarme automático continua sendo decisão do dono, registrada acima. Muda o
peso do G-03: os leads parados em `NOVO LEAD` (48 na composição atual, depois
da correção do G-16) não estão só "envelhecendo" — estão parados numa
operação cujo próprio funil de
entrada parece ter parado de vez, o que torna a decisão do lote (Etapa A do
`ESTADO-E-PLANO.md`) mais urgente, não menos: é o estoque inteiro da operação
até a entrada voltar, e não há sinal nenhum, três dias depois, de que vá
voltar sozinha. Zero campo, zero tag, zero escrita no CRM: leitura por API,
não depende de `APROVADO.md`.

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

### F-11 · Lead que reenvia o formulário do Meta depois de sair do funil é invisível para a máquina inteira — **FEITO em 22/09/2026**

> **Conferido no mesmo dia** (`build-wesales.md`, "Conferência do F-11"): o
> desenho está certo onde importa (o portão do nó 1 resolve a corrida com a
> Porta de Entrada; a interação com o R-08 foi checada contra o portão real
> dele). Três acréscimos. (a) A dúvida do "sem filtro" se resolve **a favor de
> um workflow só**: a recomendação de boas práticas diz para evitar o gatilho
> sem filtro *"a menos que todos os formulários pertençam ao mesmo pipeline e
> etapa"* — o que implica que sem filtro é possível, e descreve exatamente este
> caso (os oito formulários caem em `FUNIL DE VENDAS`/`NOVO LEAD`). A pendência
> das 8 cópias provavelmente não existe. (b) **Faltava o reset de rodada**: o
> lead voltava para `NOVO LEAD` com `Tentativa nº` = 12, `WA não atendidas
> seguidas` estourado, `Resultado da tentativa` antigo e `Prioridade`
> rebaixada — a régua encerraria na entrada, o WhatsApp nasceria bloqueado e o
> lead que deu o sinal mais forte receberia o pior tratamento. O nó 3 do R-08 já
> tem os seis campos prontos para copiar; entra como nó 3b. (c) **`telefone-
> invalido` é aplicada em dois nós e removida em nenhum** — e a resubmissão mais
> provável é "meu telefone estava errado, corrigi", o que torna a tag falsa no
> instante em que o número novo entra. Entra na limpeza do nó 4; `nao-perturbe`
> fica fora de propósito, é o portão de consentimento.


**Por quê:** um lead com oportunidade `abandoned`/`lost` (12 tentativas
esgotadas, número errado, desqualificado) que **preenche de novo** o mesmo
anúncio do Meta está dando o sinal de reengajamento mais forte que existe —
pagou para levantar a mão de novo. Hoje isso não chega a lugar nenhum:
`Contact Created` (gatilho da Porta de Entrada, G-01) nunca dispara de novo
para um contato que já existe, porque a HighLevel deduplica por e-mail/
telefone e só **atualiza** o registro — pesquisado, comportamento nativo
confirmado por citação de página oficial em duas buscas com termos
diferentes, mesmo padrão de confiança do G-05. O único caminho de volta que
já existe (R-08, Reengajamento 90 dias) só cobre quem saiu por
`nutricao-90d` e só reage **90 dias depois**, não no instante em que o lead
acabou de agir de novo. Verificado por dado, não por suposição: a leitura
de 50 contatos desta rodada (`contacts_get-contacts`) confirma que o
padrão de mapeamento de campo do G-04 (39 leads em `Urgência`, 34 em
`Necessidade`, 25 valores fora da lista em `Investimento mensal`) segue
valendo sem mudança — nenhum lead reabriu sozinho porque nenhum mecanismo
escuta essa resubmissão.
**Como:** workflow novo "Reentrada por Formulário" — gatilho `Facebook
Lead Form Submitted` (rejeitado no G-01 para a entrada nova por cobrir só
o Meta; aqui é exatamente o que se quer, porque a reentrada **é** de quem
já veio do Meta), portão duplo (oportunidade `abandoned`/`lost` **e** sem
`nao-perturbe`) e reabertura em `NOVO LEAD`/`open` — não direto em
`CONECTAR`, para não pular a mesma triagem manual do SDR que toda entrada
nova passa (L-07/G-03). Detalhe nó a nó em `build-wesales.md`, seção 1.4;
clique a clique em `IMPLEMENTACAO-WORKFLOWS.md`, W21.
**Verificado, não suposto:** a interação com o R-08 foi conferida contra o
próprio nó 2 dele (seção 2.12), que já checa `status` ao vivo antes de
reativar — se este workflow reabrir o lead antes do relógio de 90 dias do
R-08 vencer, o portão dele encontra `status = open` e sai em no-op limpo,
sem precisar mudar nada lá. Zero campo, zero tag novos: reaproveita
`status`, etapa e as tags `nao-perturbe`/`nutricao-90d`. Zero escrita no
CRM: item de especificação pura, não depende de `APROVADO.md` — workflow
não sai por API. Pendência explícita, registrada no próprio item: não
confirmado se o gatilho aceita "todos os formulários" de uma vez ou exige
um por vez (se exigir, são 8 cópias, mesma conta do G-04).
**Pronto quando (cumprido):** todo lead com oportunidade `abandoned`/`lost`
que reenviar um formulário do Meta sem `nao-perturbe` volta sozinho para
`NOVO LEAD`/`open`, pronto para nova triagem — sem esperar 90 dias nem
depender de alguém abrir uma lista.

### F-12 · "Por que estamos perdendo?" não tem resposta — o motivo de desqualificação não agrega em lugar nenhum, e o GHL já resolve isso de graça — **FEITO em 22/09/2026**

> **Conferido no mesmo dia** (`build-wesales.md`, "Conferência do F-12"): três
> pontos. (a) A dúvida "o seletor de `Lost Reason` existe na ação `Update
> Opportunity`?" é **mais séria** do que um "a confirmar": há pedido aberto no
> canal de ideias da HighLevel para poder referenciar `Lost Reason` em automações
> e usá-lo como gatilho, com a observação de que **não está disponível**. Não
> refuta (pedidos envelhecem), mas o plano B — `Lost Reason` escolhido **na mão**
> por quem marca `lost` na tela — passa a ser caminho de verdade, não nota de pé
> de página. Pela mesma razão, a afirmação de que `Lost Reason` serve de condição
> em quatro gatilhos fica como **não confirmada**, e com ela a ideia de
> diferenciar o Reengajamento por motivo. (b) **`Lost Reason` criado nunca pode
> ser apagado** — os cinco valores têm de nascer com o texto exato de C-16 na
> primeira vez; errar o rótulo não se corrige, só se abandona, e o dropdown fica
> com os dois para sempre. (c) **Assimetria de API medida:** `lostReasonId` vem
> na resposta de `opportunities_search-opportunity`, e o schema de
> `opportunities_update-opportunity` não tem parâmetro de lost reason — legível,
> não gravável. A metade legível é nova e torna o item **auditável sem tela**:
> buscar `status = lost` e conferir que todo resultado tem `lostReasonId`
> preenchido. Vale ainda mais no plano B, onde o preenchimento é manual.


**Por quê:** `Motivo da desqualificação` (C-16, `campos-e-tags.md`) existe
desde 18/09/2026, preenchido por SDR (R-18) e closer (F-03), mas nunca teve
onde agregar — a seção 9.1 e a lista 8.5 só o mostram coluna a coluna,
oportunidade por oportunidade. O próprio Dashboard do Gestor (R-15, seção
2.17) já tinha registrado por quê ao fechar em 18/09/2026: Custom Metrics
soma campo `NUMERICAL`/`MONETARY` ou conta tag — nunca agrega por valor de
`SINGLE_OPTIONS`. A pergunta que todo gestor de pré-vendas faz primeiro
("por que estamos perdendo, na maioria das vezes?") ficou sem resposta
nativa desde então, sem que nenhuma rodada a tivesse marcado como lacuna —
achada só agora, ao procurar o que Reev/Meetime/Outreach/Salesloft
reportam e este projeto não.
**Como:** pesquisado antes de desenhar (`WebSearch`, domínios de suporte da
HighLevel bloqueados pelo proxy deste ambiente como sempre — achado por
convergência de citação em buscas com termos diferentes, confiança média,
não testado nesta subconta): o GHL já tem um objeto nativo de oportunidade,
`Lost Reason` (configurado em Settings → Custom Fields → `Lost Reason` →
Bulk Actions → Edit — campo reservado da plataforma, por isso nunca
apareceu em `locations_get-custom-fields`), com relatório nativo de quebra
por motivo (Reporting → Pipeline), coluna própria na exportação de
oportunidades, e filtro disponível em quatro gatilhos de workflow mais o
operador `If/Else` — nenhum usado ainda por este projeto. Em vez de
substituir C-16 (seria excluir campo em uso, regra 1), o desenho espelha:
no mesmo nó que já muda `status` para `lost` (D6 da seção 4, Pós-ligação; nó
4 da seção 5.1, Loop do closer), grava também o `Lost Reason` nativo com o
mesmo valor de `Motivo da desqualificação` — cinco dos seis valores, porque
`Timing errado` nunca chega a `lost` (sai por `abandoned`). Tabela completa
de ramos, o pré-requisito de tela (configurar os 5 valores antes de montar
os nós) e o que fica pendente de confirmação (se o seletor de `Lost Reason`
aceita valor dinâmico em vez de ramo fixo; se é gravável junto com
`abandoned`) em `build-wesales.md`, seção 4.1 (nova); nós atualizados em
`IMPLEMENTACAO-WORKFLOWS.md`, W4 e W6; cross-reference em `campos-e-tags.md`
(C-16) e no Dashboard do Gestor (seção 2.17, peça 6 nova). Zero campo, zero
tag novos, zero escrita no CRM: item de especificação pura, não depende de
`APROVADO.md` — `Lost Reason` não sai por API neste conector (confirmado:
`opportunities_update-opportunity` não expõe o parâmetro, mesma classe de
limitação já registrada para custom field e calendário em
`APRENDIZADOS-CRM.md`) nem a configuração dos 5 valores (é criação de opção
em campo reservado, mesma classe de trabalho manual que campo
personalizado).
**Pronto quando (cumprido):** todo lead que sai por `lost` com `Motivo da
desqualificação` preenchido também tem o `Lost Reason` nativo da
oportunidade gravado com o mesmo valor, e o Reporting → Pipeline do GHL
mostra a quebra por motivo sem precisar abrir oportunidade por oportunidade
— o que falta é só a montagem manual na tela, mesma fila dos demais nós já
especificados e ainda não publicados.

---

### F-13 · A última metade de etapa sem relógio — reunião qualificada sem decisão do closer não tem monitor — **FEITO em 22/09/2026**

> **Conferido no mesmo dia:** o desenho passou o checklist inteiro sem
> correção — o portão do nó 3 checa `status is open` (o bug recorrente do
> projeto), a tag entrou na lista do nó 4 do Mestre de saída **nos dois**
> documentos, T-21 nasceu `[ ]`, e o prazo de 3 dias vem argumentado e rotulado
> como escolha, não medição. Uma única adição: **nó 3b, portão de aviso único**.
> `Allow Re-entry` ligado (decisão certa) mais gatilho por alteração de campo
> criam instâncias simultâneas; se o closer editar o veredito duas vezes para
> `Sim`, o gestor recebe **dois avisos da mesma parada**, porque o nó 3 não olha
> a tag. A seção 2.22 já resolve isso com o mesmo nó (o dela é o 6), só que lá a
> repetição vem do laço — mesmo sintoma, mesmo remédio, e agora as duas peças
> ficam consistentes. Também conferido e OK: o merge field
> `{{contact.data_do_veredito_do_closer}}` do aviso renderiza, porque o nó 2 do
> Loop do closer carimba a data **antes** de ramificar, e o `Wait` de 3 dias
> elimina qualquer corrida entre os dois workflows que reagem ao mesmo evento.

**Por quê:** `build-wesales.md`, seção 1.1 (Etapa 3 — `NEGOCIAR`), registrava
desde antes de o F-05 existir que a metade "comparecimento" da etapa tem
monitor (R-12, SLA do closer) mas a metade "negociação" não — nota deixada
como "candidato a entrar no F-05 quando ele for construído". F-05 fechou em
21/09/2026 com seis peças (`NOVO LEAD`, `fila-tel`/`fila-wa`, `CONECTAR`,
`nao-perturbe` em workflow ativo, `AGENDAR`, retorno vencido) e nunca
incorporou esta, que ficou represada
dentro de uma nota de rodapé em vez de virar item — achada só agora, ao
reler a seção 1.1 inteira (`NOVO LEAD` → `FORMALIZAR`) e conferir, linha de
"Tempo de estagnação" por linha, se cada etapa tem relógio. Todas as outras
têm; esta não tinha: o Loop do closer (seção 5.1, ramo `Sim`) registra
o veredito e não move nem etapa nem `status` — "é o closer, fora deste
workflow, que leva a `FORMALIZAR` quando fechar" — e um lead qualificado que
o closer nunca mais toca fica parado em `NEGOCIAR`/`open` sem que nada
avise. Mesma classe de estrago silencioso que abriu as seis peças do F-05,
na única transição da operação que sobrou sem monitor.
**Como:** workflow novo "Negociação Estagnada" — gatilho `Contact Changed`
(`Reunião foi qualificada` alterado, mesmo evento do Loop do closer),
portão para `Sim`, `Wait` de 3 dias corridos, portão de confirmação (etapa
`NEGOCIAR` **e** `status` `open` **e** veredito ainda `Sim`), tag
`negociacao-estagnada` (21ª tag) e aviso ao gestor. Prazo de 3 dias em vez
das 24h que as peças 1/3/5 do F-05 usam: aquelas medem passos que dependem
só do SDR (mesmo dia deveria bastar); aqui quem decide é o closer sobre uma
proposta que o próprio lead também avalia — mais perto do horizonte de 4
dias que a régua de No-show (seção 5.3) já aceita para o mesmo tipo de
decisão mais lenta, e ainda curto porque a maioria dos leads desta base
marca `Urgência` = `Pra ontem` (G-04). Detalhe nó a nó, incluindo por que a
tag não precisa de tratamento incondicional no Mestre de saída (diferente
de `novo-lead-estagnado`/`agendar-estagnado`), em `build-wesales.md`, seção
2.28; Smart List `Saúde — Negociação Estagnada` especificada na seção 8.28.
Pesquisado antes de desenhar: mesma varredura de mercado das peças do F-05 —
nenhuma das quatro plataformas do enunciado (Reev, Meetime, Outreach,
Salesloft) expõe alarme proativo para "reunião qualificada sem decisão do
closer"; todas tratam isso como relatório de pipeline (dias em estágio),
não como notificação disparada pelo tempo.
**Pronto quando (cumprido):** uma reunião qualificada pelo closer (`Sim`)
que passa 3 dias em `NEGOCIAR`/`open` sem virar `won` nem `lost` gera aviso
ao gestor sozinho. Zero escrita no CRM nesta rodada: item de especificação
pura, a tag nasce `[ ]` em `APROVADO.md` (T-21, `campos-e-tags.md`) e só
vira `[x]` quando o dono decidir — mesma regra das cinco tags do F-05 que
ainda esperam aprovação. CRM reconfirmado por API nesta execução:
`opportunities_search-opportunity`/`opportunities_get-pipelines` seguem em
50 oportunidades (45 `NOVO LEAD` `open`, 2 `NEGOCIAR` `open`, 1 `NEGOCIAR`
`lost`, 2 `CONECTAR` `lost` de teste, sem mudança — a soma bate 50; a versão
anterior desta linha somava 52 por engano, corrigido nesta rodada) e
`locations_get-custom-fields` segue em 51 campos — G-03/G-04/F-09/F-10
seguem aguardando o dono, sem novidade; a entrada segue sem lead novo desde
21/09 09:17 (F-10). Duas correções de coerência feitas junto, achadas ao
reler a mesma tabela que abriu este item: a linha "Tempo de estagnação" da
Etapa 2 (`AGENDAR`) ainda dizia "sem monitor ainda" apesar de a peça 5 do
F-05 já cobrir exatamente esse gap desde 21/09/2026 — texto nunca
atualizado quando a peça fechou; corrigida para apontar para a seção 2.23,
como a linha da etapa `CONECTAR` já fazia.

---

### F-14 · A rampa de aquecimento do número de telefone nunca foi escrita — o F-08 disse "distribua antes de escalar" sem dizer quanto por dia — **FEITO em 22/09/2026**

**Por quê:** achado ao reler o F-08 (proteção de reputação do número de
telefone) contra o F-07 (proteção de reputação do número de WhatsApp), os
dois vizinhos diretos. O F-07 criou um objeto específico para número novo —
Tier 1, 250 contatos únicos, só sobe "consumindo metade do teto atual dentro
de 7 dias" (`build-wesales.md`, seção 2.25). O F-08 só disse "distribuir as
ligações entre mais de um número antes de escalar", sem nunca escrever
quanto por dia em qual semana — mesmo canal que carrega o **dobro** dos
toques da régua (8 de 12, contra 4 de 12 do WhatsApp) e que a própria conta
do F-08 já colocava na meta de regime (100/dia) **acima** da referência
internacional de segurança (50-75/dia). E o número está, hoje, tecnicamente
"novo" para efeito de reputação mesmo sem ser recente na subconta:
`APRENDIZADOS-CRM.md` ("O CRM não pode responder a pergunta do LC Phone")
mediu **zero registro de chamada** nas 50 conversas da subconta — o canal
nunca foi exercitado de verdade.
**Como:** pesquisado antes de desenhar (mandato do próprio roadmap) —
`WebSearch` em fontes de mercado sobre discador (Kixie, Tendril, PhoneBurner,
SalesHive, Salesloft, Aircall, Outreach), convergindo num padrão do setor:
aquecer um número novo por **~2 semanas** antes de qualquer campanha de
volume, com teto diário crescente (nunca a meta plena no primeiro dia) — e o
achado extra que fecha o argumento: o "Voice Integrity" do **Outreach**
(concorrente direto citado neste projeto) também vale só para número
comprado nos EUA, o mesmo limite que já tinha descartado o "Voice Integrity"
da HighLevel — confirma que o limite é do próprio recurso, não da
plataforma. Rampa escrita para esta operação (`build-wesales.md`, seção
2.29): semana 1 ~20-25/dia, semana 2 ~40-50/dia, semana 3 ~75/dia, semana 4+
os 100/dia de regime — cruzada com os lotes de 10-13 leads/dia que o G-03 já
decidiu para proteger o WhatsApp (F-07): o mesmo lote também governa o
volume de telefone do dia 1, e cai dentro da faixa conservadora sozinho — a
folga acaba na semana 2, quando os lotes novos somam com as reentradas
D2/D4/D7 dos lotes anteriores sem nenhum teto escrito. Sem gatilho nativo
para contar ligações por dia por número (mesmo limite de plataforma do
F-06/F-07/F-08): vira checklist do gestor, mesmo tratamento dos dois vizinhos
— referenciado dentro do próprio checklist do F-08 (`build-wesales.md`,
seção 2.26) em vez de duplicado.
**Pronto quando (cumprido):** a rampa de 4 semanas está escrita com teto por
semana; o checklist do F-08 referencia a seção 2.29; e o G-03
(`ROADMAP-SALES-ENGAGEMENT.md`, cruzamento acima) registra que o mesmo lote
que protege o WhatsApp também paga a rampa de telefone — só na primeira
semana. Zero campo, zero tag, zero workflow, zero escrita no CRM: item de
documentação e rotina manual pura, não depende de `APROVADO.md`, não entra
na "Ordem de montagem" nem no checklist de teste da seção 10. CRM
reconfirmado por API nesta execução: 50 oportunidades (45 `NOVO LEAD` `open`
+ 2 `NEGOCIAR` `open` + 1 `NEGOCIAR` `lost` + 2 `CONECTAR` `lost` de teste),
51 campos, mesmas 5 etapas do `FUNIL DE VENDAS` — sem mudança de estrutura;
a entrada segue sem lead novo desde 21/09 09:17, agora ~30h47min (F-10) —
G-03/G-04/F-09/F-10 seguem aguardando o dono.

### F-15 · Lead sem telefone recicla de 90 em 90 dias sem nunca ser procurado — a régua é 100% telefone e o canal e-mail (78% da base) nunca foi usado — **FEITO em 22/09/2026 (especificação)**

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

**Por quê:** achado em `ESTADO-E-PLANO.md` (nova leitura completa da
subconta pedida pelo dono, 22/09/2026, commit `cdaef2d`) e aprofundado
nesta rodada. O portão 0.0/0.0b (seções 2.3/2.10 do `build-wesales.md`)
manda quem não tem telefone, mas tem `Site` ou `Instagram`, para
`status = abandoned` + tag `nutricao-90d` — a mesma saída branda de
qualquer lead com telefone que esgota as 12 tentativas. O Reengajamento
90 dias (R-08) reativa todos de volta para `CONECTAR` sem distinguir os
dois casos, e quem não tem telefone bate no mesmo portão de novo e volta
para `nutricao-90d` no mesmo instante — um ciclo fechado de 90 em 90 dias
que nunca produz uma tentativa de contato real, porque toda a operação
fala só por telefone e WhatsApp desde a decisão de 100% telefone
(`d52e61d`). Medido: **9 dos 50 contatos reais não têm telefone**
(`ESTADO-E-PLANO.md`, seção 2); **39 dos 50 (78%) têm e-mail**, e nenhuma
régua deste projeto usa esse canal (`grep -c "Send Email"
wesales/build-wesales.md` = 0, antes desta rodada). Diferente do G-03
("ninguém entra na régua"): aqui o lead entra, é avaliado e sai decidido,
ciclicamente, sem nunca ser procurado — o tipo de "estrago silencioso" que
só uma leitura de dados de produção revela, não uma leitura de texto.
**Conferido antes de escalar como decisão do dono:** ao contrário de
G-03/G-04/F-09/F-10, este item não tem opções concorrentes nem tradeoff de
negócio — é canal ocioso preenchendo uma lacuna que a própria régua já
identificou e nunca tratou, então virou especificação completa nesta
rodada em vez de pergunta em aberto.
**Como:** pesquisado antes de desenhar — literatura de sales engagement
(Zendesk, Highspot, Salesforce, via `WebSearch`) confirma que cadência
multicanal supera canal único; nenhuma das quatro plataformas do
enunciado (Reev, Meetime, Outreach, Salesloft) documenta publicamente uma
rota de resgate específica para o subconjunto "sem telefone" de uma
cadência phone-first — a peça mais próxima é o **breakup e-mail**
genérico (`myphoner.com`), medido em 30–40% de reabertura de negócios
"mortos", usado no segundo dos dois e-mails. Workflow novo "Resgate por
E-mail — Sem Telefone", especificado nó a nó em `build-wesales.md`, seção
2.30: gatilho `Contact Tag Added: nutricao-90d`, portão que filtra só quem
tem `Phone` vazio **e** `Email` preenchido **e** não está `nao-perturbe`
(a maioria de quem ganha a tag tem telefone e o R-08 já atende), dois
e-mails (`EM-1`, `EM-2` — textos em `biblioteca-mensagens.md`, primeiro
código de canal e-mail desta biblioteca) com 5 dias de espera de resposta
entre eles, e aviso ao gestor se o lead responder (decisão manual de como
retomar, sem régua automática pronta para um canal novo). Zero campo, zero
tag novos — reaproveita `Phone`/`Email` nativos, `Template usado` (C-23) e
as tags `nutricao-90d`/`nao-perturbe` já existentes. Zero escrita no CRM
nesta rodada: item de especificação pura, não depende de `APROVADO.md`
para nascer, mas os dois templates de e-mail (`EM-1`/`EM-2`, via
`emails_create-template`, ferramenta que este conector expõe) precisam de
`[x]` antes de saírem por API — linha nova em `APROVADO.md`, nasce `[ ]`.
**O que este item não resolve:** os 9 contatos já parados hoje precisam do
mesmo backfill manual que o G-01/F-05 já usaram (`Add to Workflow` em
massa) — ação em massa em dado de produção, regra 2 do briefing pede
listar e confirmar antes; e não há como confirmar por este conector se a
subconta tem domínio de e-mail verificado para envio transacional,
pendência a checar na tela antes de montar.
**Pronto quando:** os dois templates de e-mail existem
(`biblioteca-mensagens.md`, feito) e o workflow está publicado — todo
contato que cai em `abandoned`+`nutricao-90d` sem telefone e com e-mail
passa a receber ao menos uma tentativa de contato pelo canal que ele de
fato tem, em vez de reciclar para sempre sem nenhuma.

---

### F-18 · `monetaryValue` nasce com um número falso e nada troca pelo valor real quando o negócio fecha — inventário dos módulos do CRM (27/09/2026) — **especificação fechada em 27/09/2026, execução aguarda o primeiro `won`**
**Renumerado de F-07 para F-18 em 27/09/2026, na reconciliação deste arquivo** (ver alerta de integridade no topo): o item nasceu como F-07 sem saber que o número já pertencia a outro item, perdido no acidente de 24/09/2026 e agora restaurado — "Proteção de reputação do número de WhatsApp", acima. F-16 e F-17 também já estão em uso (`build-wesales.md`, §2.31/§2.32, citados em cinco outros documentos); F-18 é o primeiro número livre.
**Por quê:** pedido do dono ("módulos que ainda não tenhamos tocado, tabelas,
funções e recursos do CRM"). Inventariadas as 36 ferramentas do conector `GHL
CRM` ao vivo: `blogs_*` (0 sites na subconta) e `social-media-posting_*` (1
página do Facebook dormente, 0 seguidores, sem relação com os leads pagos do
Meta Lead Ads) não têm nada para construir — checados e descartados, para não
serem reabertos por outra rodada. `payments_*` também está vazio (0
transações, a agência fatura fora do GHL), mas o sintoma que esse módulo
resolveria já é real sem ele: toda oportunidade nasce com `monetaryValue =
5000` (valor padrão da Porta de Entrada) e nada no fluxo publicado troca esse
número pelo valor real do contrato quando o closer marca **Ganho**. Zero
negócio chegou a `won` ainda — a distorção não aconteceu, mas o primeiro
fechamento real vai somar `5000` fixo no dashboard do gestor (R-15) em vez de
receita real, mesma classe de erro silencioso que o F-06 já descreveu para
"taxa de conexão".
**Como:** sem automação nova — o valor do contrato não existe em campo
nenhum hoje, só na cabeça do closer. `GUIA-CLOSER.md` ganhou uma linha: ao
marcar Ganho, trocar o `Valor` da oportunidade pelo valor real
(`opportunities_update-opportunity` aceita `body_monetaryValue`, escrita
trivial pela tela ou por API). Detalhe completo, e os três módulos
verificados um a um, em `build-wesales.md` §2.47.
**Pronto quando:** o primeiro `won` desta operação carrega um `monetaryValue`
diferente de `5000`, e o dashboard do gestor soma receita real, não
contagem de negócios fechados.

### F-19 · A Interceptação de Sinal trata "estou de férias" como "tenho interesse" — e o Stop on Response encerra a cadência do lead no mesmo segundo, em silêncio (27/09/2026) — **FEITO em 27/09/2026 (especificação)**

**Por quê:** pesquisando Reev/Meetime/Outreach/Salesloft antes de considerar
o bloco 6 esgotado (rotina obrigatória de todo item novo deste roadmap),
achado que nenhum dos seis exemplos já fechados (F-01 a F-06) cobre: a
Interceptação de Sinal — Resposta (seção 2.9.3) só filtra opt-out
(2.9.5/R-17); uma resposta automática de ausência (auto-reply do WhatsApp
Business do lead, "fora do horário de atendimento", "estou de férias")
dispara `Prioridade` = 5, `fila-quente` e a tarefa "ligar agora" do mesmo
jeito que um "sim, tenho interesse". Mais caro que o alarme falso: a
Cadência 12x30 e a Inbound têm `Stop on Response` ligado sem filtro de
conteúdo possível (limite nativo, pesquisado) — a mesma auto-resposta
encerra as tentativas restantes do lead pago no mesmo segundo, sem que
ninguém tenha decidido isso. Nem F-05 (vigia lead **parado**) nem G-19
(outro limite de plataforma, na Faxina) cobrem este caso.
**Como:** workflow novo "Resposta Automática — Ausência", gatilho
`Customer Replied` filtrado por uma lista de 19 frases de
ausência/auto-resposta testada frase a frase (não substring, mesma lição do
`pare`/`parece` do 2.9.5); marca a tag de auditoria `resposta-automatica`
(T-23), soma o contador `Respostas automáticas` (C-33) e avisa o gestor —
não tenta reinscrever a cadência sozinho, porque `Allow Re-entry` está
desligado na 12x30/Inbound por decisão D-06 (evitar tentativa duplicada) e a
plataforma não expõe "pausar e retomar" por dentro do próprio workflow, a
mesma classe de limite que a Faxina (G-19) e a abertura da operação
(`ABERTURA.md`) já documentaram. Patch pendente, registrado mas não
aplicado nesta rodada: acrescentar a mesma lista de frases como
`Doesn't Contain` no filtro já publicado da 2.9.3 (mesma mecânica do
2.9.5/R-17) — mecânico, não decisão, próximo passo de quem tiver a tela ou
os scripts `tools/patch_*.py`.
**Pesquisado antes de desenhar:** Outreach detecta OOO por algoritmo sobre
e-mail e pausa o Prospect sem contar como reply; Salesloft lê a data de
retorno e reagenda para "retorno + 1". As duas soluções vivem dentro do
motor de sequência deles — o GHL não expõe equivalente (`Customer Replied`
filtra por `Contains Phrase`/`Exact Match`/tag/`Intent Type`/canal;
`Intent Type` distingue positivo/negativo/reclamação/pergunta, nenhuma
categoria de ausência). Este item não replica os dois — limita o dano com a
peça nativa que o próprio R-17 já usa, e troca silêncio por aviso.
**Pronto quando:** uma resposta com frase de ausência/auto-resposta não gera
`Prioridade` = 5 nem tarefa de sinal quente na 2.9.3, e fica registrada
(tag + contador + aviso ao gestor) em vez de desaparecer sem rastro quando o
`Stop on Response` nativo tirar o contato da cadência. Detalhe nó a nó em
`build-wesales.md`, seção 2.48; tag e campo em `campos-e-tags.md` (T-23,
C-33); ambos nascem `[ ]` em `APROVADO.md`.

---

### F-20 · O próprio F-19 deixou o e-mail de fora do filtro de ausência — o canal onde autorresponder de férias é mais comum, não menos (27/09/2026) — **FEITO em 27/09/2026 (especificação)**

**Por quê:** pesquisando Reev/Meetime/Outreach/Salesloft na sessão automática
seguinte ao F-19 (mesma rotina obrigatória), achado dentro do próprio item
que tinha acabado de fechar: o F-19 escreveu o gatilho do filtro de ausência
como `Customer Replied — Canal: WhatsApp e SMS`, herdando o recorte de canal
da Interceptação de Sinal (2.9.3) que ele estava corrigindo, e nunca chegou
ao e-mail — o único canal de texto que o F-15 abriu depois do R-17/G-06.
**É a mesma classe de lacuna que o G-06/G-07 já fecharam neste projeto**
(a guarda mais nova nunca alcança o canal mais novo), com uma inversão que
piora o caso: aqui a guarda (F-19) já existia havia uma sessão quando
ninguém voltou para estendê-la, e o canal que ficou desprotegido é
justamente aquele em que "fora do escritório" automático é recurso padrão
de qualquer caixa de e-mail — mais comum, não menos comum, que a
auto-resposta de ausência do WhatsApp Business. O `Resgate por E-mail —
Sem Telefone` (seção 2.30, F-15) trata toda resposta do nó 4/7 como
"respondeu, decisão manual", sem filtro de conteúdo — e o segmento que essa
régua atende (leads sem telefone, hoje os 5 reais do Instagram) já é o que
recebe menos atenção da operação: gastar essa atenção escassa perseguindo
um autorresponder de férias é o pior lugar possível para o mesmo erro que
o F-19 encontrou em WhatsApp.
**Como:** workflow-irmão "Resposta Automática — Ausência — E-mail", mesmo
gatilho `Customer Replied` filtrado pela mesma lista de 19 frases do F-19
(reaproveitada sem alteração, mesmo padrão que o 2.9.6/G-07 já usou para
reaproveitar a lista de opt-out em vez de manter uma terceira versão),
trocando só o canal para E-mail. Reaproveita a **mesma** tag
`resposta-automatica` (T-23) e o **mesmo** contador `Respostas automáticas`
(C-33) do F-19 — não cria par novo de campo/tag, porque o evento que se
quer medir ("auto-resposta na base") é o mesmo, só o canal muda. Registra a
mesma redundância aceita que o G-07 já documentou para o par opt-out/2.30
(o nó 4b/7b do `Resgate por E-mail` ainda dispara seu próprio aviso
genérico em paralelo) e a mesma pergunta em aberto (se o `Wait → Contact
Replied` do 2.30 aceita filtro de conteúdo) — não resolvidas aqui pelo
mesmo motivo que não foram resolvidas lá.
**Pesquisado antes de desenhar:** a mesma pesquisa do F-19 já respondia
esta lacuna — Outreach detecta OOO por algoritmo sobre e-mail porque
e-mail é o canal principal deles desde sempre; a ironia é que este projeto
tinha construído a defesa equivalente para o canal onde o problema é
historicamente menos documentado (WhatsApp) e deixado de fora o canal onde
ele é mais documentado e mais comum.
**Pronto quando:** uma resposta ao `Resgate por E-mail` com frase de
ausência/auto-resposta soma em `Respostas automáticas` (C-33) e ganha
`resposta-automatica` (T-23) do mesmo jeito que já acontece em WhatsApp/SMS
(F-19), e o aviso que o gestor recebe para aquele contato deixa claro que é
provável autorresponder antes de qualquer SDR gastar tempo tentando reabrir
contato com quem só está fora do escritório. Detalhe nó a nó em
`build-wesales.md`, seção 2.49. Zero campo, zero tag novos: T-23/C-33
continuam `[ ]` em `APROVADO.md`, mesma linha do F-19 — este item amplia o
motivo de aprovar, não pede aprovação nova.

### F-21 · A própria Interceptação de Sinal nunca ganhou canal e-mail — e copiar o desenho do WhatsApp cegamente aplicaria `fila-quente` a quem a lista que a lê nunca mostra (27/09/2026) — **FEITO em 27/09/2026 (especificação)**

**Por quê:** aplicando a pergunta que o F-20 deixou pronta ("essa guarda
existe em todo canal de texto que a operação usa, ou só no canal que
motivou o achado original?") a um alvo que F-19/F-20 ainda não tinham
testado — a própria Interceptação de Sinal (F-01, 2.9.3), não uma guarda
vizinha dela. G-07/2.9.6 levou o opt-out ao e-mail; F-19/F-20 levaram o
filtro de ausência ao e-mail; a peça original, que aplica `Prioridade` = 5
e a tarefa "ligar agora" quando um lead demonstra interesse real, nunca
ganhou versão e-mail. Hoje uma resposta de interesse ("sim, quero saber
mais") de um lead do `Resgate por E-mail — Sem Telefone` (2.30, F-15) só
aciona a notificação genérica do 2.30 — sem prioridade, sem fila, sem
distinguir de "esfriou" para quem lê os avisos um a um.

**Por que não é só copiar o 2.9.3 trocando o canal — três diferenças que a
cópia cega quebraria em silêncio:** (1) o 2.9.3 levou dois ciclos de
correção (R-17 e depois F-19/F-20) para excluir opt-out e ausência; este
item nasce com as duas listas desde a primeira versão, sem esperar uma
terceira rodada descobrir a mesma lacuna num canal novo; (2) `fila-quente`
é lida só pela lista `Fila Quente` (8.1), filtrada por etapa `CONECTAR`/
`REUNIÃO DE DIAGNÓSTICO` — a população que hoje recebe e-mail (`abandoned`
+ `nutricao-90d`, sem telefone, F-15) não está em nenhuma das duas; aplicar
a tag do jeito do 2.9.3 taguearia um contato que a única lista que a lê
nunca mostra, e a tarefa "ligar agora" instruiria o SDR a fazer a única
coisa que esse lead, por definição, não pode receber (não tem telefone);
(3) o destino correto de um sinal de interesse por e-mail já existe — é o
mesmo que o R-08 (Reengajamento 90 dias, seção 2.12) usa: reabrir a
oportunidade em `CONECTAR`. Fechado como **F-21**: workflow novo
"Interceptação de Sinal — E-mail", especificado nó a nó em
`build-wesales.md`, seção 2.50 — reabre a oportunidade só quando ela está
`abandoned` (não decide sozinho sobre `lost`/`open`), só aplica
`fila-quente`/`Prioridade` quando há telefone (senão avisa o gestor com
instrução que já leva isso em conta), e exclui as duas listas de frases
(opt-out e ausência) desde o nó 1.

**Pesquisado antes de desenhar:** a pesquisa do F-19 já cobre este caso —
nenhuma das quatro plataformas (Reev, Meetime, Outreach, Salesloft)
precisa resolver "sinal quente de lead sem telefone", porque nenhuma roda
cadência de ligação como canal principal.

**O único ajuste em objeto existente que este item pede:** `Sinal
recebido` (C-13) precisa de uma terceira opção, `Resposta de e-mail` — não
sai por API (edição de tela, mesma classe da criação de campo), linha
própria em `APROVADO.md`, nasce `[ ]`. Zero tag nova, zero campo novo.
Detalhe completo, inclusive por que não reaproveitar `Resposta de
mensagem` para economizar essa edição, em `build-wesales.md`, seção 2.50.

**Pronto quando:** uma resposta de e-mail com sinal de interesse real
(sem frase de opt-out nem de ausência) reabre a oportunidade em
`CONECTAR`, grava `Sinal recebido`/`Data e hora do sinal` e avisa o gestor
com instrução que já leva em conta se o lead tem telefone — nunca "ligar
agora" para quem, por definição, não tem número.

### F-22 · O e-mail ganhou disparo real (F-15/F-19/F-20/F-21) e nenhum documento fechou a proteção de reputação do canal — o par que falta ao lado do F-07/F-08/F-14 — **FEITO em 27/09/2026 (documentação, mesmo padrão do F-07)**

**Por quê:** aplicando aos seis pilares do bloco 6 a mesma pergunta que o
F-19/F-20/F-21 já aplicaram às guardas de texto — "esta peça cobre todo
canal que a operação usa, ou só o canal que a motivou?" —, desta vez à
peça de infraestrutura, não à de conteúdo. F-07 protege a reputação do
número de WhatsApp, F-08/F-14 protegem a do número de telefone; nenhum
item protege o e-mail, canal que o F-15 abriu e que F-19/F-20/F-21/G-07 já
constroem lógica em cima — hoje só existe o checklist de G-07 (seção 2.30),
e ele confirma SPF/DKIM/DMARC **uma vez, antes do primeiro disparo real**:
autenticação, não capacidade de envio. É o mesmo ponto cego que o F-07
descreveu para o WhatsApp antes de existir, agora no canal mais novo do
projeto — e, ao contrário de opt-out/ausência/sinal (que herdam o recorte
de canal de uma guarda vizinha já existente), este não tinha nenhuma guarda
vizinha para herdar de errado: simplesmente nunca foi perguntado.

**Pesquisado antes de desenhar (`WebSearch`, confiança média — a
documentação da HighLevel segue bloqueada pelo proxy deste ambiente,
citada por resultado de busca e por artigos de terceiros, não lida direto,
mesma classe de confiança que o F-07 já registrou para o mesmo motivo):**
Outreach e Salesloft não têm rampa automática — os dois recomendam um
processo **manual**: começar em 15-20 e-mails/dia num domínio novo e dobrar
por semana ao longo de 3-6 semanas, autenticar (SPF/DKIM/DMARC) antes de
começar, e ficar de olho em taxa de resposta/abertura para acelerar ou
desacelerar a rampa à mão. O GHL nativo (LC Email) resolve isso **sozinho**
desde 27/04/2026 para domínio compartilhado: todo sub-account novo entra
automaticamente num sistema de graduação por 8 estágios — começa num teto
conservador, sobe sozinho com envio limpo (sem denúncia, sem bounce alto)
até 15.000/dia no estágio 8, e **desce** sozinho se um estágio registrar
pico de bounce, denúncia de spam ou violação de política, ficando marcado
"Stage declined" no histórico. Esta subconta nasceu em 17/09/2026 — depois
da data de corte — e se qualifica para o sistema automaticamente. **Isto
já bate a paridade com Outreach/Salesloft sem precisar de nada novo: a
plataforma faz sozinha a rampa que as duas exigem manual do usuário.** O
que falta não é construir uma rampa (como o F-14 teve que fazer para o
telefone, que não tem equivalente nativo) — é não estragar a que já existe
e saber o que fazer se ela regredir, exatamente a mesma lacuna documental
que o F-07 fechou para o WhatsApp.

**Duas bifurcações que mudam o comportamento, e nenhum documento deste
projeto registrou nenhuma das duas:**
1. **Domínio compartilhado** (o padrão, se ninguém configurou domínio
   próprio para o envio) — rampa automática acima, zero ação do gestor.
2. **Domínio dedicado** (se o envio de `EM-1`/`EM-2` for configurado para
   sair de um domínio próprio, ex. um subdomínio da agência) — o warmup
   **não** é automático para domínio já existente, só para domínio novo
   recém-verificado; precisa de um clique manual (`Configurações da
   Agência → Email Services → SMTP Service → Dedicated Domain and IP →
   domínio → Start Warmup`). Conectar um domínio dedicado sem dar esse
   clique deixa o e-mail **sem proteção nenhuma** — pior que o domínio
   compartilhado, não igual, porque ninguém está olhando o teto subir
   sozinho.

**Achado extra, mesma classe do "estrago silencioso" que motivou o F-05 e
o F-07:** e-mail de campanha/workflow que passa do teto diário **falha e
não é reenfileirado** — diferente de e-mail 1-para-1 do próprio sistema
(confirmação de agendamento, notificação), que continua entregando normal.
Não confirmado com certeza pela pesquisa (mesma classe de dúvida em aberto
que o 2.30 já registra para o próprio `Wait → Contact Replied`) se um
envio disparado por workflow como o `EM-1`/`EM-2` conta como "campanha" ou
como "1-para-1" para este efeito — registrado como pergunta em aberto, não
resolvida aqui. O risco por **volume** é baixo agora (o F-15 atende hoje
uma fração pequena da base, muito abaixo do teto do primeiro estágio); o
risco real é a nota cair por **qualidade** (bounce alto numa lista nunca
limpa, poucas respostas) antes do volume crescer — mesmo padrão que o F-07
já descreveu para o WhatsApp (o teto não é o risco, a nota cair antes de
precisar do teto é).

**Como — e por que não é workflow, mesmo motivo do F-07:** pesquisado se
existe gatilho, ação ou Custom Value nativo que leia o estágio atual ou uma
queda de estágio em tempo de execução — não encontrado (mesmo limite do
F-07: a única superfície é a tela, `Email Services`, com o banner de "Rate
Limited" quando o teto aperta). Não é lacuna deste item, é limite de
plataforma/conector como qualquer outro já registrado — a saída correta é
registrar a checagem como rotina manual do gestor, com gatilho por evento
em vez de calendário fixo, mesmo padrão do F-07:

| Quando olhar | Por quê |
|---|---|
| **Antes do primeiro disparo real de `EM-1`/`EM-2`** | Confirmar qual das duas bifurcações acima se aplica — domínio compartilhado (nada a fazer) ou dedicado (confirmar que o Warmup já foi iniciado) — antes que o primeiro lote saia sem proteção nenhuma |
| **Semanalmente enquanto a base sem telefone crescer** (F-15 recicla a cada 90 dias, R-08 pode devolver mais contatos a essa fila) | O volume de hoje tem folga larga no teto inicial; o risco não é estourar o teto, é a nota cair antes de precisar subir de estágio |
| **Depois de qualquer pico visível de bounce/opt-out no canal e-mail** (mesmo gatilho que o F-07 já usa para o pico de opt-out por texto no WhatsApp) | Bounce alto e denúncia são os dois motivos documentados de "Stage declined" — pico aqui é sinal antecedente barato de checar `Email Services` antes que o estágio caia sozinho |

**Zero campo, zero tag, zero workflow, zero escrita no CRM:** item de
documentação e rotina manual pura, mesmo padrão do F-07 — não depende de
`APROVADO.md`. Não entra na "Ordem de montagem" (não há nó para montar)
nem no checklist de teste da seção 10 (não há objeto de CRM para simular
reputação de domínio com contato fictício).

**Pronto quando:** o gestor sabe, sem perguntar a ninguém, se o e-mail
desta subconta está em domínio compartilhado ou dedicado, se o warmup
dedicado (quando aplicável) já foi iniciado, e os três momentos em que
precisa olhar `Email Services` antes que o teto caia em silêncio — mesmo
padrão de "Pronto quando" do F-07. Detalhe completo em `build-wesales.md`,
seção 2.51.

### F-23 · O próprio F-21 reproduziu o par `Allow Re-entry` + "ligar hoje" que motivou o F-04, e não herdou o teto que o F-04 criou para esse par — **FEITO em 27/09/2026 (especificação)**

**Por quê:** reconferido o CRM antes de desenhar — `opportunities_search-
opportunity` (status `all`) sobe de 64 para **65 oportunidades** (14 `NOVO
LEAD` [3 open + 10 abandoned + 1 lost], 47 `CONECTAR` [39 open + 8 lost], 3
`NEGOCIAR` [2 open + 1 lost], 1 `REUNIÃO DE DIAGNÓSTICO` lost — 1 lead novo
frente à leitura anterior, sem sinal de disparo em massa) e
`locations_get-custom-fields` confirma 56 campos de contato, sem mudança;
`Carlos Andrade` (`7ECnj1bSeEIm5P58Ifd9`) segue `dnd: true`, tag
`atraso-1a-tentativa` presente — G-25 continua sem novidade (detalhe no
próprio G-25, abaixo). Sweep de coerência (`grep -rn` pelos números/nomes
tocados nas últimas rodadas — F-19 a F-22, T-23, G-25/G-26 — em todo o
`wesales/`) não achou nada novo em texto. A lacuna veio de uma pergunta que
ainda não tinha sido feita: não "esta guarda existe em todo canal?"
(F-19→F-20→F-21 já esgotaram essa pergunta para opt-out/ausência/sinal
quente), mas "todo workflow que herdou o motivo original de uma guarda
também herdou a guarda?" — aplicada ao F-21 (2.50), o mais recente dos três
que rodam `Allow Re-entry` ligado sobre uma reação a `Customer Replied`.

A própria seção 2.50 já registrava, no nó do `Allow Re-entry`, "cada
resposta é um evento novo, mesmo raciocínio do 2.9.2" — mas parou nessa
metade da frase. O raciocínio completo, no 2.9.2/2.9.3, tem uma segunda
parte: é exatamente esse par (`Allow Re-entry` ligado + um nó que empurra
compromisso de ligação para o SDR: lá, `Add Task` "ligar agora"; aqui,
`fila-quente`/`Prioridade` = 5 + `Internal Notification` "ligar hoje") que
gera o risco descrito na própria seção 2.19 do `build-wesales.md`, F-04 —
"pode empilhar tarefa+aviso sem limite a cada clique ou resposta do mesmo
lead" — e que motivou o teto de toques por semana em primeiro lugar. O F-21
copiou a causa (`Allow Re-entry` ligado sobre reação a resposta) sem copiar
o remédio (o portão que checa `Toques na semana` antes de empurrar a fila).
Um lead que responde ao `Resgate por E-mail` várias vezes no mesmo dia —
comum quando alguém está negociando por e-mail — geraria `fila-quente` +
aviso "ligar hoje" a cada resposta, sem limite, o mesmo "dobro de toques"
que o F-04 já corrigiu para clique e resposta de WhatsApp/SMS. E mesmo uma
única passagem sem repetição já é um ponto cego: o "Pronto quando" do F-04
promete "nenhum lead recebe mais que N toques por semana, venha de onde
vier" — antes deste item, "vier por e-mail" não estava incluído em "onde
vier".

**Pesquisado antes de desenhar:** a mesma pesquisa do F-07/F-19 já cobre a
pergunta "como as quatro plataformas resolvem fadiga entre canais" (nenhuma
delas soma toque de canais diferentes contra o mesmo teto — Outreach usa
`Sequence Exclusivity`, uma trava de admissão, não um contador cross-canal,
achado já registrado no próprio F-04). Não havia pesquisa nova a fazer: o
achado deste item não é "que solução existe lá fora", é "esta operação já
tinha a solução certa e não a aplicou onde o próprio desenho novo recriou o
problema que ela resolve" — o mesmo tipo de lacuna que o G-06 (peça 1) já
registrou para o `Send WhatsApp` da `Qualificação por IA`, achada a mesma
forma: perguntar não "existe uma guarda?" mas "este ponto novo tem a mesma
forma do ponto que fez a guarda nascer?".

**Como:** `build-wesales.md`, seção 2.50, e `IMPLEMENTACAO-WORKFLOWS.md`,
W27, ganham o nó **6c** (Portão de frequência, F-04: `Toques na semana`
(C-26) ≥ 6 → ramo **6d**, senão → ramo **6a**) inserido entre o portão de
telefone (nó 6) e a fila (agora 6a, só alcançada com telefone **e** teto
livre); 6a ganha, depois de aplicar `fila-quente`/`Prioridade`, o mesmo
`Add Contact Tag: toque` que o nó 7 da 2.9.2 já aplica. O ramo **6d** (teto
batido, com telefone) segue direto para o registro (nós 7-10) sem
fila/aviso, mesmo tratamento que o nó 3c da 2.9.2 já dá ao teto batido — a
nota é barata, empilhar fila/tarefa/aviso sem limite é que custa caro. O
aviso do nó 9 e a nota do nó 10 ganham uma terceira variante de texto
(6a/6b/6d) para o gestor distinguir "sem telefone" de "tem telefone, mas o
teto da semana já foi atingido" — os dois merecem decisão diferente.
`campos-e-tags.md` (T-15, C-26) e `GUIA-MONTAGEM.md` (linha da
`Interceptação de Sinal — E-mail`) atualizados para citar o novo nó; o
"Teste" do W27 em `IMPLEMENTACAO-WORKFLOWS.md` ganhou um terceiro caso
(teto já em 6, confirma que 6a não dispara).

**Zero campo, zero tag, zero workflow novo, zero escrita no CRM:** reaproveita
a tag `toque` (T-15) e o campo `Toques na semana` (C-26) que já existem —
correção de spec pré-publicação (o W27 ainda não foi montado na tela,
`GUIA-MONTAGEM.md`), não depende de `APROVADO.md`.

**Pronto quando (cumprido):** `grep -n "6a\|6c\|6d" wesales/build-wesales.md`
(seção 2.50) e a tabela do W27 em `IMPLEMENTACAO-WORKFLOWS.md` mostram o
portão de frequência e a tag `toque` no mesmo lugar onde a 2.9.2/2.9.3 já
os têm — nenhum ponto de envio/fila que roda `Allow Re-entry` sobre reação
a `Customer Replied` fica de fora do teto de toques por semana.

### G-25 · A janela nativa das cadências vai disparar 36-37 mensagens juntas, um dia antes da abertura combinada — nenhuma sessão automática consegue fechar a janela sozinha (27/09/2026) — **FEITO em 27/09/2026 (resolvido pelo dono, ver fechamento no fim desta seção)**

**Por quê:** seguindo a própria instrução deste roadmap ("reler os itens
represados por informação que pode ter vencido" antes de procurar lacuna
nova), a releitura desta rodada não foi de um G/F antigo — foi do handoff
mais recente do próprio projeto, `wesales/ABERTURA.md` (commits `eaaf007`,
`145262d`, `844f555`, todos de 27/09/2026 madrugada), que nenhuma das dez
sessões seguintes (`c98add1` a `ce2a7ce`, ~9h de trabalho em F-07 a F-20 e
reconciliação de documentos) tinha voltado a conferir. O achado: o backfill
do G-03 (24/09/2026) já moveu 41 oportunidades para `CONECTAR`, e a
`Cadência Inbound` já entrou para 36-37 delas — a execução está **parada**
no nó 24 (`WhatsApp · MI-0`), não fora da cadência, porque a janela do
workflow é `days: [1,2,3,4,5]`, 08:30-18:30 `America/Sao_Paulo`, e a próxima
abertura dessa janela é **segunda 28/09 08:30** (11:30 UTC). Quando ela
abrir, as 36-37 execuções disparam **juntas** — 6x o lote de 6/dia que o
dono decidiu (`ESTADO-E-PLANO.md`, linha 93, "decisão do dono, 23/09
19:00"), um dia antes da própria data de abertura que essa mesma linha
registra ("segunda 28/09/2026"), sem SDR na mesa para atender quem
responder. **Duas decisões do dono seguem sem resposta, e não é omissão —
são duas falas dele em datas diferentes que se contradizem:**
`ESTADO-E-PLANO.md` (23/09, ao vivo) fixa a abertura em segunda 28/09 com
lote de 6; `ABERTURA.md` (27/09, ao vivo) registra que ele disse "terça" no
chat, sem que nenhuma sessão tenha confirmado se isso troca a data ou é só
sobre outro ponto do plano. Nenhum documento deste projeto pode decidir
sozinho qual das duas falas vale.

**Verificado nesta sessão, não presumido:** `opportunities_search-
opportunity` (`status: all`) segue em 64, mesma composição da última
leitura (39 `CONECTAR` open); `locations_get-custom-fields` segue em 56
campos — nada mudou na conta desde o F-20. O contato-prova que o `ABERTURA.md`
cita (`Carlos Andrade`, `7ECnj1bSeEIm5P58Ifd9`) segue exatamente como o
handoff descreveu: `dnd: true`, tag `atraso-1a-tentativa` presente,
`Tentativa nº` = 0 — protegido, mas isso não muda para os outros 35-36 sem
essa proteção. `git fetch` limpo: nenhuma sessão aplicou a correção entre o
handoff e esta leitura.

**Por que nenhuma sessão automática resolve isto sozinha (bloqueio real,
não preguiça de tentar) — três caminhos conferidos, os três batem na mesma
parede:** (1) o MCP `GHL CRM` não edita configuração de workflow (armadilha
já registrada em `CLAUDE.md`); (2) o script que fecharia a janela em uma
linha (`tools/patch_janela_abertura.py --fechar --aplicar`) precisa de um
bearer de sessão logada (`../.local/_ghl_bearer.txt`, renovado por navegador
headless) que só existe no PC do dono — não existe neste contêiner, e os
domínios do GHL estão bloqueados pelo proxy (testado nesta sessão: sem o
arquivo, o próprio script recusa rodar); (3) o `--dump` do mesmo script só
lê fotografia local (`workflows-json/`), não a conta ao vivo — confirma o
desenho, não confirma se a janela já foi fechada. **Como:** o próprio
`ABERTURA.md` já desenhou a correção seguindo o mesmo raciocínio que este
roadmap usa para F-04/F-05 (limitar o dano, não fingir que a plataforma
oferece o que não oferece): `--fechar` deixa `days: [2]` (só terça) nas
duas cadências (`Cadência Inbound`, `Cadência 12x30`) — **seguro para as
duas leituras da data**, porque se a resposta certa for "segunda", fechar
para terça só atrasa um dia (sem disparo em massa sem SDR); se for "terça",
já é a data certa. `--abrir` devolve `[1,2,3,4,5]` depois. Equivalente pela
tela: `Automation → cadência → engrenagem → Execution window`, 2 cliques por
cadência.

**O que esta sessão fez, dado o bloqueio:** reconferiu que o risco segue
vivo e sem mudança desde o handoff (parágrafo "Verificado" acima), abriu
este item para o roadmap parar de tratar F-19/F-20/coerência como a rotina
normal enquanto uma mensagem que não pode ser desfeita está a menos de 26h
de sair errada, e notificou o dono diretamente — é o único que pode escolher
segunda ou terça e o único que tem o bearer para aplicar a correção. Não é
contorno de bloqueio: é a mesma escolha que o próprio `ABERTURA.md` já tinha
registrado ("me diga qual..." é o padrão deste projeto para pendência que só
falta informação, `APROVADO.md`, seção Mensagens) aplicada a um prazo fixo
em vez de um prazo flexível.

**Zero campo, zero tag, zero escrita no CRM: item de escalonamento, não
depende de `APROVADO.md`** — a correção em si (`patch_janela_abertura.py`)
já está escrita e validada em modo `--dump`; falta só quem tem o bearer
rodar `--aplicar`, ou o dono clicar na tela.

**Pronto quando:** a janela das duas cadências estiver confirmada como
`days: [2]` (ou o dono confirmar por outra via que quer manter `[1,2,3,4,5]`
e assumir o disparo de segunda) — o que vier primeiro, confirmado por
releitura do `window` na tela ou por quem tiver o bearer — e este item
puder ser marcado `FEITO` com a data e o resultado. **Enquanto isso não
acontecer, este é o item de maior prioridade do roadmap inteiro**, à frente
de qualquer G/F do Bloco 6: a próxima sessão confere primeiro se a janela
mudou (ou se a data de abertura já passou) antes de voltar à varredura de
coerência ou à pesquisa de concorrência que a "Ordem sugerida" abaixo
descreve como próximo passo padrão.

**Reconferido em 27/09/2026 ~11:05 UTC, sessão automática seguinte —
seguindo a própria instrução do parágrafo acima ("a próxima sessão confere
primeiro se a janela mudou... antes de qualquer outro trabalho").**
`git fetch` limpo; CRM reconfirmado por API: 64 oportunidades, mesma
composição da leitura anterior; `Carlos Andrade` segue `dnd: true`,
protegido. **Nada mudou** — nenhuma correção foi aplicada, nenhum disparo
aconteceu, as duas decisões do dono seguem sem resposta. Faltam ~24h25min
para a janela abrir. Testado um quarto caminho, além dos três já fechados
acima: o toolkit `gohighlevel` do Composio segue sem conta conectada
(`status: "initiated"`, `accounts: []`) — não abriria um atalho mesmo se
conectado agora, porque conectar também depende de o dono clicar num link
de OAuth, o mesmo tipo de ação que fecha a janela direto na tela, só com um
passo a mais. Diferente da sessão anterior, que só registrou a notificação
no texto deste roadmap: **esta sessão enviou um aviso direto ao dono**
(push, fora do chat), com o resumo do risco e o prazo, porque escrever
apenas aqui não garante que alguém leia antes da janela abrir. `ABERTURA.md`
carrega o mesmo registro. Nenhuma mudança na lista de decisões pendentes.

**Reconferido em 27/09/2026 ~12:05 UTC, sessão automática seguinte.**
`opportunities_search-opportunity` segue em 64, mesma composição;
`Carlos Andrade` segue `dnd: true`, protegido. `git fetch` limpo, nenhuma
sessão aplicou a correção. Faltam ~23h25min para a janela abrir. Nada de
novo a registrar — mesmo estado da leitura anterior (~11:05 UTC); sem
notificação nova por não haver fato novo. Detalhe em `ABERTURA.md`.

**Reconferido em 27/09/2026 ~15:05 UTC, sessão automática seguinte —
seguindo de novo a própria instrução do item ("a próxima sessão confere
primeiro se a janela mudou... antes de qualquer outro trabalho").**
`git fetch` limpo (`HEAD` em `9b79c37`, o mesmo commit que fechou o F-22);
`opportunities_search-opportunity` (`status: all`) confirma 64
oportunidades, mesma composição das duas últimas leituras (43 `open`, 11
`lost`, 10 `abandoned`) — inclui a `ZZ TESTE ABERTURA 27-09`
(`1ChWCVzv34ixvIOHtldS`), um teste ponta a ponta que o próprio dono correu
às 01:54 UTC de hoje (contato com `nao-perturbe` desde a criação, tag
`zz-teste-abertura`, fora da numeração deste projeto — mesma classe de
"tag do dono na tela" que `teste-regua`/`fechar-horario` já registram, não
achado novo). `contacts_get-contact` em `Carlos Andrade`
(`7ECnj1bSeEIm5P58Ifd9`) confirma `dnd: true` e a tag `atraso-1a-tentativa`
ainda presente — protegido, igual às quatro leituras anteriores. Faltam
~20h25min para a janela abrir (segunda 28/09 11:30 UTC); nada mudou, sem
disparo, nenhuma correção aplicada por ninguém com o bearer. Sem fato novo
para notificar de novo (mesma regra da reconfirmação anterior). G-25
continua sendo o item de maior prioridade do roadmap enquanto não estiver
`FEITO`.

Com o risco reconferido e sem novidade, a sessão seguiu a varredura de
coerência entre documentos que a própria "Ordem sugerida" (abaixo) indica
como próximo passo quando não há tela nem decisão nova disponível —
achado registrado como **G-26**, logo abaixo.

**Fechado em 27/09/2026 ~21:05 UTC, sessão automática seguinte — seguindo a
própria instrução deste item ("a próxima sessão confere primeiro se a
janela mudou... antes de qualquer outro trabalho"), e a conferência achou o
risco resolvido, não vivo.** `contacts_get-contact` em `Carlos Andrade`
(`7ECnj1bSeEIm5P58Ifd9`) — a mesma leitura que confirmou "protegido" em
cada rodada anterior — voltou `dnd: false` (era `true`), `Prioridade`
(C-05) `= 4` (era ausente/0) e `dateUpdated` `2026-09-27T21:04:39.258Z`,
28 segundos antes desta leitura. Não presumido: amostrado mais 13 dos 30
contatos da lista "Recebe DND" de `ABERTURA.md` (`lqxkp4EdUdBRPr83JYhn`,
`9RLeKfPDe6yE49RLOO7u`, `SxX69gKO2G5AWyVAPOjh`, `YlPqam7AalWJqEpL6emi`,
`0l6KtdWoSpOIMn1CeeAw`, `ossJg7kUN0rrKF59sx0m`, `GhMa7O5TZfIG3CORZNdE`,
`gtufwlEa5yNgrzgu4IKm`, `zN97QTlkYwSMllJYxkCQ`, `OfHQEWxgxjUC1cIurwzO`,
`tNDkZGkMtEDYcw8qxxQW`, `wZabWXgjVzW7AjRYnZ8L`, `3ufCFsY8ASh3BbwRb5Ld`) —
todos com o mesmo par `dnd: false` + `Prioridade: 4`, todos com
`dateUpdated` entre `21:04:39` e `21:04:50` UTC (11 segundos de faixa: uma
escrita em lote, não 14 ações manuais separadas). Os 5 contatos do "Lote 1"
(livre para disparar) que já carregavam `fila-sdr` desde as 18:22 não foram
tocados nesta janela — coerente com já estarem fora de qualquer bloqueio.

**Quem fez, e por quê isto não apareceu em nenhuma leitura anterior deste
roadmap:** existe uma quarta branch neste mesmo repositório,
`claude/abertura-operacao-dnd-n7dnjv`, com sessão de navegador logado (o
bearer que este roadmap registrou repetidamente como "só existe no PC do
dono") — ativa desde 27/09 01:27 UTC, 48h+ de commits, nunca cruzada com
este branch até agora. O próprio arquivo dela,
`wesales/DE-PARA-SESSOES-CRM.md` (lido nesta sessão, não copiado para
aqui — pertence à outra branch), reconcilia quatro sessões trabalhando a
mesma subconta em paralelo e registra, na tabela de recomendações: **"G-25,
G-26, G-28, G-30 — nada a fazer: resolvidos pela sua decisão das
20:10–20:23"**. A decisão do dono, ao vivo, respondeu as duas perguntas que
este item deixou em aberto: (1) a data é **segunda 28/09** (não terça — o
MI-0 já foi regravado com o texto novo para sair segunda 08:30, confirmado
pela mesma sessão); (2) a rampa de 6/dia não se resolve fechando a janela
`days` do workflow (o `patch_janela_abertura.py` que este item preparou
nunca foi executado, e não precisou ser) — resolve-se soltando os 31 leads
protegidos de uma vez (`dnd = false`) e deixando a `Prioridade` (recalculada
para 4 por `recalcula_prioridade.py --aplicar`, script daquela branch)
governar o ritmo de envio pelos portões que o G-04 já usa — um desenho mais
fino do que a correção binária "fecha a janela" que este item chegou a
escrever, porque throttling por prioridade sobrevive à próxima abertura de
janela sem precisar de reabrir/fechar `days` de novo.

**O que isto expõe, e que nenhuma leitura anterior deste roadmap tinha
achado porque nunca olhou fora do próprio branch:** quatro sessões Claude
Code diferentes escreveram nesta mesma subconta nas últimas 48h, cada uma
com seu próprio ROADMAP/APROVADO/documentação, sem nenhum mecanismo que
avise uma sessão que outra já resolveu o que ela está prestes a escalonar
como bloqueado. Este item ficou marcado "item de maior prioridade do
roadmap inteiro" por ~10 horas (das ~11:05 às ~21:05 UTC) depois de já
estar resolvido do lado de quem tinha o bearer — não por lentidão desta
sessão, e sim porque nenhum dos dois lados sabia olhar o outro. Registrado
como lição em `APRENDIZADOS-CRM.md` e como item novo, **G-31**, ao lado dos
demais G deste roadmap — o problema estrutural (quatro fontes de verdade
sem reconciliação) é maior do que este item específico e continuaria
produzindo o mesmo falso bloqueio na próxima vez.

**Pronto quando (cumprido nesta sessão):** a janela das duas cadências
segue `days: [1,2,3,4,5]` (não foi fechada, e não precisou ser) — o "outro
lado" do critério original ("ou o dono confirmar por outra via que quer
manter `[1,2,3,4,5]` e assumir o disparo de segunda") se cumpriu por ação
direta do dono, verificada por leitura independente desta sessão, não por
suposição. Zero campo, zero tag, zero escrita no CRM nesta sessão: item de
escalonamento que se resolveu por leitura, sem precisar de `APROVADO.md`.

---

### G-26 · O gate de contagem de tags voltou a divergir da conta sozinho — a correção do G-20 trocou o número errado por outro número, que também vence (27/09/2026) — **FEITO em 27/09/2026**

**Por quê:** a varredura de coerência desta sessão (`grep -rn` pelos nomes e
números tocados nas últimas rodadas — F-19 a F-22, T-23, G-25 — em todo o
`wesales/`, exigida antes de qualquer commit) achou que `build-wesales.md`,
seção 2.32, ainda dizia "a conta tem mais tags que **as 21 do projeto**" —
um número fixo, escrito em 23/09/2026 quando T-01 a T-21 já existiam. A
T-22 (23/09) e a T-23 (27/09, F-19) elevaram a contagem "do projeto" para
23 sem que ninguém voltasse a esta frase — exatamente o mesmo defeito que
o **G-20** já tinha corrigido nesta mesma linha em 23/09/2026, só que a
correção de então trocou "25" por "21" (um valor, ainda fixo) em vez de
tirar o número — e um valor fixo copiado para fora da fonte sempre vence
assim que a fonte muda de novo. `campos-e-tags.md`, Etapa 3 (a fonte, pela
própria regra "número fixo só na fonte" que este roadmap segue desde o
G-20), já estava correto: "23 numeradas... Total na conta hoje: 29",
contando a T-23 desde que o F-19 a especificou.

**Como:** removido o número fixo da linha de `build-wesales.md` §2.32 —
"as 21 do projeto" virou "as do projeto", a mesma redação sem número que
`campos-e-tags.md` já usa para se referir a si mesmo ("tem mais tags que
as do projeto", linha 365 daquele arquivo) — e registrado, na própria
frase, por que ela voltou a divergir depois do G-20, para a próxima
correção não repetir o mesmo erro de trocar um número fixo por outro.
Nenhum outro arquivo do projeto tinha o mesmo padrão de contagem total de
tags/campos fora de `campos-e-tags.md` (conferido: as demais ocorrências de
"N tags do projeto" em `APROVADO.md` e `APRENDIZADOS-CRM.md` são registro
histórico datado — "as 11 tags do projeto" em 18/09/2026, por exemplo — não
uma contagem viva, e não precisam de correção). Zero campo, zero tag, zero
escrita no CRM: coerência de documentação, não depende de `APROVADO.md`.

**Pronto quando:** `grep -rn "tags que as [0-9]" wesales/*.md` não devolve
nada fora de entrada histórica datada — cumprido nesta mesma rodada.

### G-27 · Um campo `SDR responsável` nasceu na tela — exatamente o campo que o R-10 pesquisou e decidiu não criar, sem nenhum documento saber por quê ele voltou (27/09/2026) — **FEITO em 27/09/2026 (registro + achado)**

**Por quê:** reconferência de rotina do G-25 (`opportunities_search-opportunity`,
status `all`): 65 oportunidades, composição idêntica à última leitura (14
`NOVO LEAD` [3 open + 10 abandoned + 1 lost], 47 `CONECTAR` [39 open + 8
lost], 1 `REUNIÃO DE DIAGNÓSTICO` lost, 3 `NEGOCIAR` [2 open + 1 lost]) —
`Carlos Andrade` (`7ECnj1bSeEIm5P58Ifd9`) segue `dnd: true`, tag
`atraso-1a-tentativa` presente, sem novidade no risco do G-25.
`locations_get-custom-fields` (model `contact`), a mesma chamada de sempre,
subiu de 56 para **57 campos** — o único novo é `SDR responsável` (id
`LoSi8PQCbBRjmkMC8CH8`, `TEXT`, placeholder "nome do SDR que qualificou
(preenchido pelo painel)", `dateAdded` 2026-09-27T16:53:01Z, ~11 minutos
antes desta sessão). Varredura de coerência (os outros 56 nomes contra
`campos-e-tags.md`: as 32 `C-`, as 18 `Q-`, o par `S-01` e os quatro "fora
da lista" — `Urgência`, `Necessidade`, `Empresa`, `Canal que conectou`) não
achou nenhum outro campo órfão; `SDR responsável` é o único sem linha em
documento nenhum. E não é um nome qualquer: é **literalmente** o campo que
o **R-10** (18/09/2026, `FEITO`) pesquisou e decidiu não criar — três
documentos (`ROADMAP-SALES-ENGAGEMENT.md` acima, `build-wesales.md` §2.14,
`CONFERENCIA-CAMPOS.md`, seção F) registram a mesma razão: reaproveitar o
nativo `Assigned User` para não ter "campo com dois donos", que diverge na
primeira reatribuição feita direto na tela. Alguém — só pode ter sido o
dono, campo personalizado não sai por este conector — criou o campo que a
própria pesquisa já tinha desaconselhado, sem nenhum commit ou conversa
deste projeto explicando o porquê.

**O que o placeholder muda, e o que não resolve:** "nome do SDR que
qualificou (preenchido pelo painel)" não é a mesma pergunta que o R-10
respondeu. R-10 rejeitou um campo espelhando **o dono atual do contato**
(`Assigned User`, que muda a cada reatribuição — é aí que "dois donos"
diverge). O placeholder descreve outra coisa: um registro de **quem
qualificou**, no passado, uma vez — o mesmo padrão de C-15/C-16 (`Reunião
foi qualificada`, `Motivo da desqualificação`), que este documento já
trata como seguro porque só um papel escreve, uma vez, sem disputa. Se for
isso, o campo não repete o erro que R-10 evitou; se for um substituto para
o mesmo uso que `Assigned User` já cobre (por exemplo, para a Fase 4 de
`R-10`/round robin ainda sem segundo SDR), repete exatamente o risco
documentado. **Nenhum documento deste projeto decide isso — só o dono sabe
qual das duas intenções é a dele**, e "preenchido pelo painel" cita um
"painel" que não corresponde a nenhum workflow, script ou documento
existente aqui (`grep -rni "painel" wesales/*.md` só encontra o termo
genérico "painel de automação" da interface do GHL, nunca uma ferramenta
própria deste projeto) — pode ser um painel externo ao GHL, fora do
alcance deste conector e desta auditoria.

**Como:** nada sai por API — campo já existe, criado fora deste conector, e
regra 1 (nunca excluir) e regra "Como autorizar" (`APROVADO.md`) não se
aplicam a um campo que o dono criou direto na tela, mesmo tratamento já
dado a `Canal que conectou` (G-21), `fechar-horario` e ao Espelho de Etapa:
registro, não aprovação. O trabalho desta rodada é a ponte de coerência —
apontar os três documentos que registram a decisão do R-10 para este
achado, para a próxima sessão não precisar redescobrir a mesma pesquisa
achando um campo que "não devia existir". Feito nos mesmos três lugares:
`campos-e-tags.md` (Etapa 2, quinto campo "fora da lista", mesmo formato
do quarto), `ROADMAP-SALES-ENGAGEMENT.md` (R-10, acima) e
`CONFERENCIA-CAMPOS.md` (seção F). Zero campo, zero tag, zero escrita no
CRM.

**Pronto quando:** o dono disser qual das duas intenções é a certa — e,
com a resposta, este item ganha peça 2: se for "quem qualificou" (uso
seguro), só falta decidir quem escreve (SDR? closer? o "painel" externo?) e
onde a régua de nota ou o dashboard passam a lê-lo; se for substituto de
`Assigned User`, o item se junta ao mesmo risco que R-10 já documentou, e a
recomendação é reverter para o nativo antes que uma reatribuição manual
faça os dois campos discordarem. Até a resposta, o campo fica vazio e sem
consumidor — nenhum workflow, nenhuma lista, nenhum documento lê ou escreve
nele hoje, confirmado nesta rodada. G-03, G-04 (peça 2), F-09, F-10, G-11
(item 1) e G-19 continuam sendo as seis decisões sem prazo fixo que esperam
o dono, sem novidade nesta sessão; G-25 continua sendo o item de maior
prioridade do roadmap enquanto a janela de 28/09 08:30 `America/Sao_Paulo`
não passar sem disparo.

---

### G-28 · O campo do G-27 já mudou de novo — o dono trocou `SDR responsável` de `TEXT` livre para `SINGLE_OPTIONS` fechado 13 minutos depois, sem que nenhum documento tivesse chegado a registrar o primeiro estado (27/09/2026) — **FEITO em 28/09/2026 (ver G-34)**

**Por quê:** reconferência de rotina do G-25 (a primeira tarefa de toda
sessão enquanto ele não fechar) — `opportunities_search-opportunity`
(status `all`) confirma **65 oportunidades**, mesma composição da última
leitura (14 `NOVO LEAD`, 47 `CONECTAR`, 3 `NEGOCIAR`, 1 `REUNIÃO DE
DIAGNÓSTICO`); `contacts_get-contact` em `Carlos Andrade`
(`7ECnj1bSeEIm5P58Ifd9`) confirma `dnd: true` e a tag `atraso-1a-tentativa`
— protegido, nenhum disparo, `git fetch` limpo (`HEAD` segue em `25e5590`,
o commit do próprio G-27). Sem novidade no risco de prazo fixo, a sessão foi
à varredura de coerência que a "Ordem sugerida" pede quando não há tela nem
decisão nova — e a primeira checagem, no próprio achado da sessão anterior
(G-27), já achou fato novo: `locations_get-custom-fields` (model `contact`)
segue em **57 campos** (nenhum campo a mais), mas o `SDR responsável` que o
G-27 leu às ~16:53 UTC (`TEXT`, placeholder "nome do SDR que qualificou
(preenchido pelo painel)", id `LoSi8PQCbBRjmkMC8CH8`) **não é mais esse
objeto**: às 17:06:31 UTC — 13 minutos depois, antes de o G-27 sequer ser
commitado — o campo virou `SINGLE_OPTIONS` com opções fechadas `Andreyna
Siqueira`/`Pablo Santos`, sem placeholder, e com **id novo**
(`e1n7As703nqjAOpzREHc`). Id diferente, não só tipo diferente: o GHL não
edita um campo existente trocando o `dataType` de `TEXT` para
`SINGLE_OPTIONS` — ele recria o campo (mesmo `fieldKey`
`contact.sdr_responsvel`, novo `id`). O dono não ajustou o campo que o G-27
descreveu; substituiu por outro, na mesma janela de tempo em que a
descrição estava sendo escrita.

**O que isso muda, e o que não muda:** não resolve a pergunta do G-27 (qual
das duas intenções é a real), mas desloca o peso da evidência. Um
`SINGLE_OPTIONS` com as duas pessoas reais desta operação como opção
fechada é o mesmo desenho que C-15/C-16 já usam com segurança — um papel
registra um fato uma vez, sem risco de divergir de nada porque não há
"nativo" concorrente para esse fato divergir. Um campo pensado para
espelhar `Assigned User` ao vivo (a leitura que o R-10 rejeitou) normalmente
nasceria `TEXT` livre ou ligado a atualização automática, não um dropdown
fechado com exatamente os dois nomes do time — fechar as opções é o
oposto do que faria sentido para um campo que precisa acompanhar
reatribuição futura sem exigir nova opção cadastrada a cada SDR novo. Isto
não é uma decisão tomada em nome do dono — é o mesmo achado, com uma dúvida
a menos: a versão atual do campo já não corre o risco de virar texto livre
divergente que preocupava o R-10, seja qual for a intenção final.

**Como:** nada sai por API — campo já existe, editado fora deste conector.
Corrigido nos dois lugares que citavam o id/tipo antigos como fato atual:
`campos-e-tags.md` (Etapa 2, quinto campo "fora da lista") e este item.
`CONFERENCIA-CAMPOS.md` e `IMPLEMENTACAO-WORKFLOWS.md` já apontavam para o
G-27 sem repetir id/tipo — nada para corrigir ali. Zero campo, zero tag,
zero escrita no CRM.

**Pronto quando:** o mesmo do G-27 — o dono disser qual das duas intenções
é a certa. Isto não é peça 2 do G-27, é o mesmo item ganhando um fato novo
antes de qualquer resposta chegar; as duas entradas devem ser lidas juntas.
G-03, G-04 (peça 2), F-09, F-10, G-11 (item 1) e G-19 continuam sendo as
seis decisões sem prazo fixo que esperam o dono, sem novidade nesta sessão;
G-25 continua sendo o item de maior prioridade do roadmap enquanto a janela
de 28/09 08:30 `America/Sao_Paulo` não passar sem disparo.

---

### G-29 · Um sexto campo fora da lista nasceu ao lado do quinto — `B · Quanto pode investir` chegou com as mesmas opções de `Investimento mensal em anúncios`, e o próprio `SDR responsável` perdeu uma opção sem nenhum documento ter registrado quando (27/09/2026) — **ABERTO, decisão do dono**

**Por quê:** reconferência de rotina do G-25 (a primeira tarefa de toda
sessão enquanto ele não fechar) — `contacts_get-contact` em `Carlos Andrade`
(`7ECnj1bSeEIm5P58Ifd9`) confirma `dnd: true` e a tag `atraso-1a-tentativa`,
protegido, nenhum disparo; a janela de 28/09 08:30 `America/Sao_Paulo` segue
a ~16h20min de distância desta sessão. `opportunities_search-opportunity`
(status `all`) mostra **64 oportunidades** (13 `NOVO LEAD` [2 open + 10
abandoned + 1 lost], 47 `CONECTAR` [39 open + 8 lost], 3 `NEGOCIAR` [2 open +
1 lost], 1 `REUNIÃO DE DIAGNÓSTICO` lost) — uma a menos que a última leitura
(G-28, 65: 14 `NOVO LEAD` [**3** open + 10 abandoned + 1 lost]), diferença
inteira num único `open` de `NOVO LEAD` que não reapareceu em nenhuma outra
contagem (`CONECTAR` e os demais recortes de `NOVO LEAD` não mudaram). Não
investigado além disso: esta rotina não tem como distinguir merge de contato
duplicado, remoção feita na tela (fora do alcance desta auditoria — regra 1
é sobre o que **eu** faço, não sobre o que o dono faz) ou artefato de
paginação da própria API — registro do fato, não uma causa.

Sem novidade no risco de prazo fixo, a sessão foi à varredura de coerência
de sempre — e, ao reconferir o próprio achado do G-27/G-28 antes de assumir
que a página de campos estava estável, `locations_get-custom-fields` (model
`contact`) subiu de **57 para 58 campos**. O novo é `B · Quanto pode
investir` (id `GVlTZmL4I4MmpTtN1DY8`, `SINGLE_OPTIONS`, opções `Até 1k`/`1k
a 5k`/`5k a 10k`/`Acima de 10k`, posição 405, mesmo `parentId` — grupo de
tela — de `B · Investimento mensal em anúncios (anúncio)` [posição 400] e
`B · Budget` [posição 430], `dateAdded` 2026-09-27T18:32:49Z, ~32 minutos
antes desta leitura). Nenhum documento deste projeto cita este campo
(`grep -rn "Quanto pode investir\|GVlTZmL4I4MmpTtN1DY8" wesales/*.md` vazio)
— mesmo padrão órfão do G-27, e desta vez com um detalhe que aponta para
duplicação real, não só nome parecido: as quatro opções são **idênticas**,
palavra por palavra, às de `Investimento mensal em anúncios` (Q-06,
`bQithNwReQIBGlZBaNlI`), o campo vizinho de posição. Duas leituras
possíveis, nenhuma decidida por mim: (a) o dono está recriando o mesmo
campo com nome diferente, terceiro caso desta classe depois de `Canal que
conectou` (G-21) e `SDR responsável` (G-27/G-28); ou (b) "quanto pode
investir" é pergunta de qualificação genuinamente distinta de "quanto
investe hoje" (capacidade vs. gasto atual, par que o BANT tradicional
separa) e vai complementar Q-06 no script — `script-de-ligacao.md` (linha
148, pergunta 10, e o bloco de objeções da linha 196) hoje só cobre
orçamento (`Budget`, Q-14) e gasto atual (Q-06), nunca "capacidade de
investir" como pergunta própria.

O mesmo `locations_get-custom-fields` também mostra que `SDR responsável`
(`e1n7As703nqjAOpzREHc`, o objeto `SINGLE_OPTIONS` que o G-28 leu com duas
opções fechadas) segue com o **mesmo id**, mas agora só uma opção:
`["Andreyna Siqueira"]` — `Pablo Santos` não está mais na lista. Id
inalterado (diferente da troca `TEXT`→`SINGLE_OPTIONS` do G-27→G-28, que
trocou o id): editar as opções de um `SINGLE_OPTIONS` já existente preserva
o id, só trocar o `dataType` recria o campo — fato novo sobre o
comportamento da plataforma, útil da próxima vez que este roadmap precisar
decidir se uma mudança de campo é edição ou recriação. Sem `dateUpdated` no
retorno deste endpoint, não há como cravar quando a opção saiu; só que já
não está lá.

**Como:** nada sai por API nos dois casos — os dois campos já existem na
subconta, criados/editados fora deste conector. Regra 1 (nunca excluir) e a
regra "Como autorizar" do `APROVADO.md` não se aplicam: são campos do dono,
não meus. O trabalho desta rodada é o mesmo tipo de ponte que o G-27 já fez
— registrar o achado nos documentos que contam campo, para a próxima sessão
não redescobrir a mesma pesquisa: `campos-e-tags.md` (Etapa 2, sexto campo
"fora da lista", mesmo formato do quinto, com a correção do estado do
quinto embutida) e `build-wesales.md` (seção 2.53). Zero campo, zero tag,
zero escrita no CRM.

**Pronto quando:** o dono disser, para `B · Quanto pode investir`, se é
duplicata de `Investimento mensal em anúncios` (aí a recomendação é a mesma
do R-10/G-27: decidir qual campo fica e não escrever nos dois) ou pergunta
nova (aí falta decidir onde ela entra no script e na régua de nota); e,
para `SDR responsável`, a mesma pergunta que o G-27/G-28 já fizeram (qual
das duas intenções é a certa) segue de pé — a saída de `Pablo Santos` das
opções não a responde, só reduz o campo a um único SDR possível, o que
teoricamente favorece a leitura "registro de quem qualificou" enquanto
houver só uma pessoa qualificando. Até a resposta, os dois campos ficam sem
consumidor (nenhum workflow, lista ou documento lê ou escreve neles hoje,
confirmado nesta rodada). G-04 (peça 2), F-09, F-10, G-11 (item 1),
G-19, G-27/G-28 (qual intenção é a certa para `SDR responsável`) e agora
G-29 (`B · Quanto pode investir` é duplicata ou pergunta nova) continuam
sendo as decisões sem prazo fixo que esperam o dono, sem novidade além do
achado desta sessão; G-25 continua sendo o item de maior prioridade
do roadmap enquanto a janela de 28/09 08:30 `America/Sao_Paulo` não passar
sem disparo.

> **Correção de coerência, sessão do G-32 (27/09/2026):** este parágrafo
> ainda citava `G-03` (decidido e agendado desde a reconciliação de
> 27/09/2026, tirado da lista em quatro outros parágrafos naquela sessão,
> mas não neste) e, junto com o do G-30 logo abaixo, tinha parado de
> carregar G-27/G-28/G-29 na lista de decisões pendentes assim que o G-30
> nasceu — a mesma classe de erro que o G-20 já corrigiu para números fixos
> e a reconciliação de 27/09 corrigiu para o `G-03` nos outros quatro
> parágrafos (copiar o parágrafo anterior sem checar se a lista que estava
> sendo copiada ainda era a correta). Corrigido aqui e no G-30; detalhe em
> `APRENDIZADOS-CRM.md`, achado do G-32.

### G-30 · Um sétimo campo fora da lista nasceu na conta, e este não é da tela — é o rastro de um recurso nativo que ninguém documentou ligar (27/09/2026) — **ABERTO, decisão do dono**

**Por quê:** reconferência de rotina do G-25 (a primeira tarefa de toda
sessão enquanto ele não fechar) — `contacts_get-contact` em `Carlos Andrade`
(`7ECnj1bSeEIm5P58Ifd9`) confirma `dnd: true` e a tag `atraso-1a-tentativa`,
protegido, nenhum disparo; faltam ~15h25min para a janela de 28/09 08:30
`America/Sao_Paulo` (11:30 UTC) a partir desta sessão (~20:05 UTC).
`opportunities_search-opportunity` (`status=all`, lido pelo campo `meta.total`
do retorno, não pela contagem de itens da página — ver nota de ferramenta
abaixo) confirma **64 oportunidades**, composição idêntica à última leitura
(G-29: 13 `NOVO LEAD` [2 open + 10 abandoned + 1 lost], 47 `CONECTAR` [39
open + 8 lost], 3 `NEGOCIAR` [2 open + 1 lost], 1 `REUNIÃO DE DIAGNÓSTICO`
lost) — sem novidade no risco de prazo fixo nem no volume.

**Nota de ferramenta, para não redescobrir:** `opportunities_search-
opportunity` com `status=all` numa conta com 64+ oportunidades e sem
`query_limit` baixo devolve um payload grande demais (159.449 caracteres,
65 mil tokens) porque cada item vem com `contact`, `relations` e
`customFields` embutidos — a chamada falhou por estourar o limite de
tokens da ferramenta. Resposta não é reduzir `query_limit` e paginar (mais
chamadas, mesmo custo agregado): o próprio corpo do erro salva a saída
completa num arquivo local e ensina a ler com `offset`/`limit`/`jq` — mais
barato parsear o JSON salvo uma vez (`python3 -c "import json; ...
d['data']['meta']['total']"` para o total, `Counter` por
`(pipelineStageId, status)` para a composição) do que pedir de novo à
ferramenta. Registrado aqui, não em `APRENDIZADOS-CRM.md`, porque é
comportamento do host de ferramentas desta sessão (arquivo de saída +
instrução de leitura), não do MCP GHL em si — mas quem usar
`opportunities_search-opportunity` de novo com a base neste tamanho cai na
mesma mensagem.

Sem novidade no risco de prazo fixo, a sessão foi à varredura de coerência
de sempre — e, na mesma reconferência de campos que fechou o G-27/G-28/G-29
(nunca presumir que a página de campos ficou parada desde a última leitura),
`locations_get-custom-fields` (`model: contact`) subiu de **58 para 59
campos**. O novo é `Voice AI Reason for Call` (id `pVjiDY9Z2f1nmatwDz9U`,
`LARGE_TEXT`, posição 2750, `parentId` `gabsbU3jsUN7oIXCnYab` — o grupo de
tela dos campos que os workflows escrevem, não o grupo de qualificação
`zHU4yGXKHdxBHnGxUmai` dos três campos das linhas G-27/G-28/G-29), `dateAdded`
2026-09-27T19:29:18Z, ~36 minutos antes desta leitura. `grep -rn "Voice AI
Reason for Call\|pVjiDY9Z2f1nmatwDz9U" wesales/*.md` vazio — nenhum documento
deste projeto cita este campo.

**Diferença que separa este achado dos três anteriores (`Canal que
conectou`, `SDR responsável`, `B · Quanto pode investir`):** aqueles três
têm nome e formato de campo criado à mão na tela de "Custom Fields" (posição
no grupo de qualificação, opções escolhidas por alguém). Este tem nome e
formato de campo **gerado pela plataforma** — `WebSearch` confirma que
"reason for calling" é um dos dados que o recurso nativo **Voice AI / AI
Employee** do HighLevel captura e expõe por Custom Value durante uma
chamada (`help.gohighlevel.com`, artigos de Voice AI Custom Actions e
Custom Values), e o nome do campo bate exatamente com esse rótulo interno
— não é uma pergunta de qualificação que alguém desenhou, é o rastro de
alguém (o dono, ou um teste) tendo ativado o Voice AI/AI Employee nesta
subconta. Isso muda a pergunta que este item faz ao dono: não é "qual das
duas leituras é a certa" (G-27/G-29), é "o Voice AI está ligado nesta
subconta de propósito, e se estiver, ele substitui algum nó da `Cadência
12x30`/`Qualificação por IA no WhatsApp` ou roda em paralelo sem que
nenhum documento saiba?" — pergunta que nenhum item deste roadmap fez
ainda, porque nenhum outro achado até aqui apontava para um recurso nativo
ligado por fora da spec.

**Como:** nada sai por API — o campo já existe na subconta, criado pela
plataforma ao ativar um recurso nativo, não por este conector. Regra 1 e a
regra "Como autorizar" do `APROVADO.md` não se aplicam: não é um campo meu
para criar nem para decidir. O trabalho desta rodada é o mesmo tipo de
ponte que o G-27/G-29 já fizeram — registrar o achado nos documentos que
contam campo, para a próxima sessão não redescobrir a mesma pesquisa:
`campos-e-tags.md` (Etapa 2, sétimo campo "fora da lista", mesmo formato
dos seis anteriores) e este item.

**Pronto quando:** o dono disser se o Voice AI/AI Employee está ativo nesta
subconta de propósito e, se estiver, qual é a intenção (substituir um nó
existente da cadência, rodar como canal extra, ou foi ativado sem querer
num teste). Até a resposta, o campo fica sem consumidor (nenhum workflow,
lista ou documento lê ou escreve nele hoje, confirmado nesta rodada).
G-04 (peça 2), F-09, F-10, G-11 (item 1), G-19, G-27/G-28, G-29 e agora a
pergunta do Voice AI (G-30) continuam sendo as decisões sem prazo fixo que
esperam o dono, sem novidade nesta sessão; G-25 continua sendo o item de
maior prioridade do roadmap enquanto a janela de 28/09 08:30
`America/Sao_Paulo` não passar
sem disparo.

### G-31 · Quatro branches diferentes escrevem na mesma subconta sem se cruzarem — o G-25 ficou "item de maior prioridade" por ~10h depois de já estar resolvido do outro lado (27/09/2026) — **ABERTO, decisão do dono**

**Por quê:** fechando o G-25 nesta sessão (acima), a conferência de rotina
("a janela mudou?") achou o risco já resolvido — mas não por nenhuma
correção que este roadmap ou `ABERTURA.md` tivesse registrado. Investigando
o porquê (`contacts_get-contact` mostrando `dnd: false` e `Prioridade: 4`
em 14 contatos que todas as leituras anteriores confirmavam `dnd: true`,
todos com `dateUpdated` na mesma janela de 11 segundos, 21:04:39–21:04:50
UTC), a causa não estava em nenhum script deste branch (`faxina_tarefas.py`
lido por completo: só conclui/exclui tarefa e liga/desliga `sdr-lotado`,
nunca toca `dnd` — descartado por leitura do código, não por suposição) nem
em nenhum workflow nativo documentado. A causa é externa a este branch:
`git branch -a` e `git cat-file -e <branch>:<arquivo>` (não `git grep` — o
mesmo erro de método que `rotina-limpar-tarefas.md` já registrou para o
`faxina-tarefas.yml`, "o grep vê só a branch local") acharam **quatro**
branches deste mesmo repositório com trabalho de WeSales nas últimas 48h,
cada uma com sua própria árvore de documentos e nenhuma delas citando as
outras três antes de hoje:

| Branch | Janela de atividade | Escreveu no CRM? | Documentação própria |
|---|---|---|---|
| `amazing-johnson-mclksg` (esta, "B") | 26/09 23:52 – em curso | não — a própria B só audita e especifica | `ROADMAP-SALES-ENGAGEMENT.md` (este arquivo), `APROVADO.md`, `build-wesales.md`, `APRENDIZADOS-CRM.md`, `campos-e-tags.md` |
| `abertura-operacao-dnd-n7dnjv` ("A") | 27/09 01:27 – em curso, sessão de navegador logado (tem o bearer que B registra repetidamente como "só no PC do dono") | **sim**, conferido pela própria sessão contato a contato | `ESTADO-27-09.md`, `AUDITORIA-27-09.md`, `DE-PARA-SESSOES-CRM.md`, `COPY-WHATSAPP.md`, entre outros — nenhum arquivo em comum de nome com B |
| `laughing-bohr-ki6ah8` ("C", PC do dono) | 27/09 20:40 – em curso no momento deste fechamento | ainda não, por leitura própria da sessão A | não inspecionado por B nesta sessão |
| `abertura-operacao-dnd-ib6xaz` ("D") | 27/09 17:47–17:58 | não | registrou funções (SDR/closer) e um conserto de Action |

A própria sessão A já tinha notado o problema e criado
`DE-PARA-SESSOES-CRM.md` para reconciliar as quatro — mas essa reconciliação
vive só na branch A; nada nela avisou a branch B (nem o inverso: o G-25, as
descobertas F-19 a F-23 e G-26 a G-30 desta branch não aparecem em nenhum
documento de A antes de hoje, e o próprio `DE-PARA-SESSOES-CRM.md` registra
isso como pendência: "revisar antes: a própria sessão B marca vários como
'decisão do dono'"). O efeito prático, medido, não hipotético: o G-25 ficou
escrito como "item de maior prioridade do roadmap inteiro" desde ~11:05 UTC
até esta sessão (~21:05 UTC) — **quase 10 horas** depois de o dono já ter
resolvido o risco do lado da branch A (decisão dele, entre ~20:10 e ~20:23
no relógio daquela sessão). Nenhuma das duas sessões agiu errado; nenhuma
tinha visibilidade da outra.

**Como (o que esta sessão fez, e o que fica para o dono decidir):**
registrado o achado aqui e em `APRENDIZADOS-CRM.md`, para toda sessão futura
de qualquer uma das quatro branches — antes de escalonar um item como
"esperando o dono" ou "bloqueado, precisa de tela/bearer" — checar primeiro
se outra branch já resolveu, com `git branch -a` seguido de
`git cat-file -e <branch>:<caminho>` para arquivos específicos (nunca
`git grep` sozinho, que só vê o checkout local) e, se existir, ler o
equivalente a `DE-PARA-SESSOES-CRM.md` daquela branch antes de qualquer
outro trabalho. Isto não é uma correção que uma sessão sem acesso a merge
possa aplicar sozinha (decidir qual branch é a fonte de verdade, ou se as
quatro devem convergir para uma, é decisão do dono — o mesmo tipo de escolha
que este roadmap nunca toma por conta própria). Zero campo, zero tag, zero
escrita no CRM: item de processo, não depende de `APROVADO.md`.

**Pronto quando:** o dono escolher uma de duas saídas — (a) consolidar as
branches ativas em uma só antes da próxima rodada de trabalho real, ou (b)
manter branches paralelas mas exigir que toda sessão leia o `DE-PARA`/
equivalente das outras antes de escalonar qualquer item como bloqueado.
Até a escolha, o mitigador é o registrado acima: checar branches irmãs
virou passo obrigatório antes de declarar algo "esperando o dono" neste
roadmap.

### G-32 · Um oitavo campo fora da lista nasceu na conta — e desta vez o hábito que o G-31 deixou achou a explicação de primeira, em vez de mais um mistério para o dono (27/09/2026) — **FEITO em 27/09/2026 (reconciliação)**

**Por quê:** reconferência de rotina depois do G-25/G-31 — antes de
qualquer trabalho novo, `contacts_get-contact` em `Carlos Andrade`
(`7ECnj1bSeEIm5P58Ifd9`) reconfirma `dnd: false` e `Prioridade = 4` (G-25
segue resolvido, sem regressão) e `opportunities_search-opportunity`
(`meta.total`, não a contagem de itens da página — nota de ferramenta do
G-30) confirma **64 oportunidades**, sem mudança de volume.
`locations_get-custom-fields` (model `contact`) mostra um campo que nenhum
documento desta branch cita: `Canal da tentativa`
(`contact.canal_da_tentativa`, id `AsZMGmsKVu1xEp36hyLb`, `SINGLE_OPTIONS`
`Telefone`/`WhatsApp`, posição 595, grupo de qualificação, `dateAdded`
2026-09-27T21:30:52Z) — mesma classe de achado que G-27/G-29/G-30 (campo
fora da lista). Mas desta vez, antes de escrever mais um "registro, pergunta
ao dono", a lição do G-31 (checar `git branch -a`/`git cat-file` e ler o
`DE-PARA` da branch candidata antes de tratar campo sem explicação como
mistério) foi aplicada pela primeira vez desde que virou hábito registrado.

**Como:** `git branch -a` + `git show
origin/claude/abertura-operacao-dnd-n7dnjv:wesales/DE-PARA-SESSOES-CRM.md`
(a mesma branch A que já tinha resolvido o G-25) explicou o campo sem
precisar perguntar nada ao dono: pedido explícito dele, numa sessão do PC
em 27/09/2026 (tabela "Itens 1–4", linha "pedido anterior"), campo criado
para alimentar 3 portões novos no workflow `Pós-ligação v3` (`fila-wa` →
`Canal da tentativa == WhatsApp`, com o canal limpo no fim de 10 ramos),
publicado v6 → v7 e testado no contato de teste daquela branch. Não é
órfão nem duplicata: é peça de um redesenho do seletor de canal — o mesmo
ponto que o F-09 discute — que a branch A está construindo ao vivo, fora
deste conector. Esta sessão verificou por conta própria só a existência e
o formato do campo, por API; a fiação do workflow é relato da outra
branch — registrado como dado, não confirmado nó a nó por aqui. Zero
campo, zero tag, zero escrita no CRM: reconciliação de documentação, não
depende de `APROVADO.md`. Detalhe em `campos-e-tags.md`, Etapa 2 ("oitavo
campo fora da lista").

**Pronto quando:** cumprido nesta rodada — diferente de G-27/G-28/G-29/
G-30, este não é decisão pendente do dono, é lacuna de documentação já
fechada: a explicação já existe e está registrada aqui e em
`campos-e-tags.md`, para nenhuma sessão futura desta branch redescobrir a
mesma pergunta. G-04 (peça 2), F-09, F-10, G-11 (item 1), G-19, G-27/G-28/
G-29 (qual das duas intenções é a certa para `SDR responsável`, e se
`B · Quanto pode investir` duplica `Investimento mensal em anúncios`),
G-30 (Voice AI ativado de propósito?) e G-31 (consolidar branches ou
formalizar a checagem) continuam sendo as decisões sem prazo fixo que
esperam o dono, sem novidade além desta reconciliação.

### G-33 · O próprio hábito que o G-31 deixou e o G-32 usou uma vez fechou dois itens que este roadmap ainda tratava como "esperando o dono" — G-04 (peça 2) e G-30 já estavam resolvidos do outro lado (27/09/2026) — **FEITO em 27/09/2026 (reconciliação)**

**Por quê:** reconferência de rotina, sem novidade — `contacts_get-contact`
em `Carlos Andrade` (`7ECnj1bSeEIm5P58Ifd9`) confirma `dnd: false` e
`Prioridade = 4` (G-25 segue resolvido); `opportunities_search-opportunity`
(`meta.total`) confirma **64 oportunidades**, sem mudança;
`locations_get-custom-fields` (model `contact`) confirma **60 campos**, os
mesmos do fechamento do G-32 (nenhum nono campo órfão apareceu). Sem
achado na varredura de coerência de sempre, esta sessão aplicou de novo o
mitigador que o G-31 registrou e o G-32 usou uma única vez — checar
`git branch -a` e ler o `DE-PARA-SESSOES-CRM.md` da branch candidata antes
de tratar qualquer coisa como "esperando o dono" — mas desta vez não para
um campo novo, para a própria lista de decisões pendentes que este roadmap
vinha carregando adiante a cada parágrafo. `git branch -a` mostra a mesma
branch `abertura-operacao-dnd-n7dnjv` ("A", do G-31/G-32) ainda como a mais
recente com trabalho em `wesales/` fora desta; o `DE-PARA-SESSOES-CRM.md`
dela (atualizado 27/09 20:50, depois da leitura que fechou o G-32) tem duas
tabelas que respondem, sem precisar de resposta nova do dono:

1. **Tabela "Gravado pela sessão do PC em 27-28/09" (já publicado e relido
   pela própria sessão A, não recomendação):** a linha `G-04: 5 portões,
   igualdade exata, pontos iguais` — `Pós-agendamento v2`, v17 → v18 — fecha
   a peça 2 do G-04. Em vez de escolher a Opção A ou B da Tabela H
   (`CONFERENCIA-CAMPOS.md`) como o item previa, a régua ganhou ramos extras
   por igualdade exata com o texto literal que o Meta grava fora da lista de
   opções: campo `Investimento mensal em anúncios` — `Abaixo de 5k` pontua
   como `1k a 5k` (+6), `Até R$ 1.000` como `Até 1k` (+2); campo `Investe em
   anúncios` — os três valores pagos do Meta pontuam como `Sim` (+13),
   `Não invisto nada ainda` como `Nunca` (+4); campo `Urgência` (o bloco de
   reserva que a peça 1 já tinha fechado) — `Posso esperar e ver oque
   acontece` pontua como `Sem prazo` (+2). Resolve exatamente o "Pronto
   quando" do item: um lead novo do Meta pontua o Bloco B sem depender de
   qual dos quatro textos o anúncio grava, sem precisar remapear os 8
   formulários (Opção A) nem trocar a régua inteira para `Contains`
   (Opção B) — uma terceira saída que nenhuma das duas sessões tinha
   escrito antes de o dono aplicá-la direto na tela.
2. **Tabela "Para o dono decidir" (aqui sim, recomendação — mas com uma
   linha que já é fato, não pedido):** a linha `G-25, G-26, G-28, G-30` diz
   "nada a fazer: resolvidos pela sua decisão das 20:10–20:23 ou só registro
   (Voice AI com 0 agentes)". G-25/G-26/G-28 já estavam `FEITO`/sem ação
   pendente neste documento; **G-30 não estava** — a pergunta "o Voice AI
   está ativo nesta subconta de propósito?" segue no próprio G-30. Resposta
   pela leitura da sessão A (20:15, campo de agentes de Voice AI ativos):
   **zero**. Não é "ativado de propósito e substituindo um nó" nem "ativado
   sem querer com efeito colateral" — é um recurso sem nenhum agente
   configurado, então o campo `Voice AI Reason for Call` fica (regra 1,
   nunca excluir) inerte, sem nada disparando nele nem cobrando por ele.
   Fecha o G-30 por completo, não só regista o achado.

**Diferença que importa frente ao G-27/G-28/G-29, para não fechar por
engano:** a mesma tabela "Para o dono decidir" traz uma terceira linha —
`G-27/G-29: SDR responsável e B · Quanto pode investir sem nenhum workflow
lendo | definir que a SDR preenche os dois na ligação e que a nota de
qualificação lê Quanto pode investir; hoje nada lê`. Diferente das duas
linhas acima (que citam uma decisão **já tomada**, `20:10-20:23`, ou um fato
**já lido**, `0 agentes`), esta é recomendação da própria sessão A ainda sem
confirmação do dono — a mesma classe de "registro, não decisão" que este
roadmap já usa para G-27/G-28/G-29. Não fecho os três por isto: registro a
recomendação (aqui e em `campos-e-tags.md`) para quando o dono responder,
sem tratá-la como resposta.

**Ressalva de método, igual à do G-32:** esta sessão confirmou por conta
própria, via API, só o que é diretamente verificável por ela — os campos
`Carlos Andrade`/oportunidades/`locations_get-custom-fields` acima. A versão
publicada do `Pós-agendamento v2` e a contagem de agentes de Voice AI são
relato da sessão A (documento dela, não node a node por este conector);
tratado como dado, não como confirmação própria, mesmo padrão do G-32 para
o `Canal da tentativa`.

**Como:** nada sai por API — os dois fechamentos são reconciliação de
documentação, não escrita no CRM. Atualizados nesta rodada:
`IMPLEMENTACAO-WORKFLOWS.md` (checklist de go-live, a régua BANT e a
"Ordem de montagem" — as três citavam o G-04 como aberto). Zero campo,
zero tag, zero escrita no CRM: não depende de `APROVADO.md`.

**Pronto quando:** cumprido para os dois — G-04 (peça 2) e G-30 saem da
lista de decisões sem prazo fixo que esperam o dono. G-27/G-28/G-29 (agora
com a recomendação da sessão A registrada, ainda sem confirmação), F-09,
F-10, G-11 (item 1), G-19 e G-31 continuam sendo essas decisões.

### G-34 · O próprio G-33 juntou G-28 com G-27/G-29 na mesma recomendação "ainda sem confirmação" — mas a fonte que ele cita separa os três em dois grupos diferentes, e um deles já tem decisão (28/09/2026) — **FEITO**

**Por quê:** reconferência de rotina do G-25 antes de qualquer outra
coisa (já fechado, sem novidade — `git fetch` limpo, `HEAD` de
`abertura-operacao-dnd-n7dnjv` parado no mesmo commit de 20:40:50
`-03:00` da sessão anterior; a janela da MI-0 abre às 11:30 UTC de hoje,
faltando ~11h a esta sessão, 00:08 UTC). Fresh reconferido por API própria,
não presumido: `locations_get-custom-fields` (`model: contact`) mostra o
mesmo campo `SDR responsável` (`e1n7As703nqjAOpzREHc`, `SINGLE_OPTIONS`)
com a mesma opção única `Andreyna Siqueira` que o G-29 já tinha achado —
nenhuma mudança desde então. Relendo o próprio `DE-PARA-SESSOES-CRM.md` da
sessão A (mesmo documento que o G-33 já tinha usado para fechar G-04 peça 2
e G-30) linha a linha, a tabela final separa os achados desta rodada em
**dois** grupos, não um: *"G-25, G-26, G-28, G-30: nada a fazer: resolvidos
pela sua decisão das 20:10–20:23 ou só registro (Voice AI com 0 agentes)"*
— um grupo — e, **linha separada**, *"G-27/G-29: `SDR responsável` e `B ·
Quanto pode investir` sem nenhum workflow lendo → definir que a SDR
preenche os dois na ligação e que a nota de qualificação lê `Quanto pode
investir`; hoje nada lê"* — outro grupo, explicitamente ainda em aberto. O
G-33 leu a segunda linha corretamente (por isso registrou "recomendação,
ainda sem confirmação" para G-27/G-29), mas colou o `G-28` dentro dessa
mesma frase — quando a fonte já tinha posto o G-28 no primeiro grupo,
ao lado do G-25/G-26/G-30 que o próprio G-33 fechou duas linhas antes. Não
é erro de leitura da conta (nenhum dos dois grupos discorda do que
`locations_get-custom-fields` mostra); é erro de agrupar três números numa
frase só sem reconferir se a fonte os tratava do mesmo jeito — a mesma
classe de descuido que o G-20/G-26 já corrigiram para número fixo e o G-32
corrigiu para `G-03` na lista de pendências, agora aplicado a lista de
itens, não a número.

**O que isso resolve, e o que continua em aberto:** o G-28 fechava com "o
dono disser qual das duas intenções é a certa" (mesma pergunta do G-27).
Este documento já registrava, com cautela, que a saída de `Pablo Santos`
das opções **por si só** não responde isso — só favorece a leitura "quem
qualificou" (G-29, penúltimo parágrafo). O que fecha o item não é o
formato do campo, é o relato da sessão A: ela teve sessão de navegador
logado com o dono ativa na mesma janela (27/09, tarde/noite) e registrou,
na própria tabela "Gravado pela sessão do PC", a linha "18:25 | carteira →
Andreyna; `SDR responsável` só com a SDR | ✓" — decisão ao vivo, não
inferência de formato. Mesma classe de evidência (relato em primeira mão
de uma sessão com acesso que esta não tem) já aceita pelo G-33 para fechar
o G-04 peça 2 (conteúdo de workflow) e o G-30 (contagem de agentes Voice
AI) — nenhuma das duas era verificável por este conector também, e
não foram tratadas como exigindo confirmação adicional. Aplicar padrão
diferente ao G-28 sem motivo seria inconsistência nova, não cautela.
**O que isso NÃO fecha:** a pergunta do G-29 é outra — se algum workflow
deveria ler `SDR responsável`/`B · Quanto pode investir`, e se este último
é duplicata de `Investimento mensal em anúncios` — nenhuma linha da tabela
da sessão A resolve isso, ela mesma marca como recomendação, não decisão.
G-27 fica como está (já `FEITO` — registro do achado original; a pergunta
que ele fazia é a mesma do G-28, agora respondida, mas o cabeçalho do G-27
não muda porque "FEITO" ali já se referia ao trabalho de documentação, não
à resposta).

**Como:** nada sai por API — reconciliação de leitura entre dois
documentos deste projeto (o G-33 e a fonte que ele cita), mais uma
reconfirmação própria do campo por API. Corrigido: cabeçalho do G-28
(acima) e `campos-e-tags.md` (linha que dizia "a pergunta... segue sem
resposta" para o par G-27/G-28 — separada da pergunta do G-29, que
continua sem resposta). Zero campo, zero tag, zero escrita no CRM: não
depende de `APROVADO.md`.

**Pronto quando:** cumprido — G-28 sai da lista de decisões sem prazo
fixo que esperam o dono. F-09, F-10, G-11 (item 1), G-19, G-27/G-29
(recomendação da sessão A registrada, ainda sem confirmação) e G-31
continuam sendo essas decisões — seis, uma a menos que a lista do G-33.
G-25 segue fechado; a janela da MI-0 (segunda 28/09 08:30
`America/Sao_Paulo`) não passou ainda nesta sessão.

### G-35 · G-19 aponta o risco do branch para "o PR #93 mesclar" — mas o #93 fechou sem merge há 4 dias, e nenhuma rodada tinha conferido o GitHub para notar (28/09/2026) — **FEITO**

**Por quê:** reconferência de rotina do G-25 antes de qualquer outra
coisa — já fechado, sem novidade (janela da MI-0 abre 11:30 UTC hoje,
~10h15min a esta sessão; `Carlos Andrade` e a amostra dos 31 contatos
seguem `dnd: false` + `Prioridade: 4`, `conversations_search-conversation`
não mostra nenhuma mensagem automática nova para os 6 do lote livre —
nenhum disparo ainda). CRM reconfirmado por API sem mudança desde o G-34
(56 campos de contato). Com o risco de prazo fixo sem novidade e o sweep de
nomes/campos de sempre limpo, esta rodada mudou o alvo de "quem mais fala
disso" de novo: não um campo ou tag, mas uma referência a **estado externo
ao repositório que não é CRM nem `git log`** — o único tipo de fato que as
reconfirmações de rotina deste projeto nunca tinham checado de novo depois
de escrito, porque nem o `git fetch` (só vê branch) nem a API do GHL (só vê
a subconta) enxergam o estado de um Pull Request.

`G-19` (aberto, decisão do dono) cita "PR #93" três vezes como o PR cujo
merge dispara o risco do `checkout` pinado em `.github/workflows/
faxina-tarefas.yml`, e a instrução de "próxima rodada" logo depois do
fecho do G-19 (acima, nesta seção) mandava "conferir se o dono já mesclou
o PR #93". Conferido nesta rodada por `pull_request_read` (GitHub, não
presumido): PR #93 está **`closed`, `merged: false`** — fechado em
24/09/2026 18:18 UTC, **um dia depois** de a instrução acima ter sido
escrita, e nunca chegou a mesclar. Nenhuma das dezenas de rodadas entre
24/09 e hoje (G-20 a G-34, F-18 a F-23, toda a reconciliação dos dois
documentos truncados) voltou a olhar o GitHub para o próprio PR — todas
olharam CRM, `git fetch` de branch, ou texto de `wesales/`, nunca a API de
Pull Request. `search_pull_requests` (`head:claude/amazing-johnson-mclksg`)
mostra o PR que está de fato aberto hoje para esta branch: **#102**
("restaura as 20 seções de `build-wesales.md` perdidas no acidente de
24/09"), criado 27/09/2026, ainda `open`, mesmo par base/head
(`claude/youtube-publication-next-steps-v7o4el` ← `claude/amazing-johnson-
mclksg`) que o #93 tinha.

**O que isso muda, e o que não muda:** o risco em si — `checkout` pinado
numa branch de PR, que quebra se ela sumir — continua exatamente como o
G-19 descreveu; só o número do PR que o dispararia estava errado, e citar
um número fixo nunca teria funcionado como instrução de verificação,
porque o #93 já tinha fechado sem mesclar: esperar por ele mesclar é
esperar por um evento que não vai acontecer. Mesma classe de descuido que
o G-20/G-26 já corrigiram para contagem fixa fora da fonte e o G-32/G-33/
G-34 para lista de pendências não reconferida contra a fonte que a gerou —
aqui aplicada, pela primeira vez neste roadmap, a estado do GitHub em vez
de CRM ou texto interno.

**Como:** nada sai por API do CRM. `pull_request_read`/
`search_pull_requests` (GitHub) confirmaram os dois estados nesta sessão.
Correção nos três trechos de `ROADMAP-SALES-ENGAGEMENT.md` que citavam
"PR #93" como referência corrente (não como registro histórico datado, que
fica intacto): a menção no corpo do G-19 (Defeito 2), a instrução do "Como"
item 2, e uma nota acrescentada logo após a instrução de "próxima rodada"
que o fecho do G-19 tinha deixado. Nenhuma delas vira número fixo de novo —
passam a apontar para "o PR aberto desta branch", verificável a qualquer
momento por `search_pull_requests`, em vez de um número que expira sozinho.
Zero campo, zero tag, zero escrita no CRM: item de coerência entre este
roadmap e o estado real do GitHub, não depende de `APROVADO.md`.

**Pronto quando:** cumprido — as três citações correntes a "PR #93" foram
corrigidas para não fixar número de PR. **Regra prática, generalizável:**
número de PR muda toda vez que um fecha e outro abre para a mesma branch;
citar um PR específico como "o que decide" um risco futuro é o mesmo erro
de número fixo fora da fonte que motivou o G-20/G-26 para contagem — aqui
a fonte é o próprio GitHub, não um documento deste repositório, e por isso
nenhum `grep` em `wesales/` a alcançava. A forma que não expira sozinha é
apontar para "o PR aberto desta branch" e verificar por
`pull_request_read`/`search_pull_requests` quando o risco importar de
novo, não repetir um número visto uma vez. G-19 continua aberto (decisão
do dono + fora do escopo `wesales/`, sem mudança); F-09, F-10, G-11
(item 1), G-27/G-29 (recomendação ainda sem confirmação) e G-31 continuam
sendo as decisões sem prazo fixo que esperam o dono — sem mudança de
estado nesta rodada. G-25 segue fechado; a janela da MI-0 não passou ainda
nesta sessão.

### F-24 · O bloco 6 mede clique em Trigger Link do WhatsApp e resposta de qualquer canal — nunca abertura nem clique de e-mail, o par que Outreach/Salesloft pontuam como sinal de intenção há anos (28/09/2026) — **FEITO em 28/09/2026 (especificação)**

**Por quê:** pesquisa de concorrência de rotina (obrigatória antes de
declarar o bloco 6 esgotado de novo), desta vez aplicada não a uma guarda de
canal (F-19 a F-22 já esgotaram opt-out/ausência/reputação nos três canais)
mas ao próprio conjunto de sinais que a Interceptação de Sinal (F-01)
intercepta: clique em Trigger Link e resposta. O e-mail já manda mensagem
real desde o F-15 (`EM-1`/`EM-2`, 22/09/2026) e a correção registrada na
própria seção 2.30 do `build-wesales.md` mostra que a maioria de quem tem
e-mail **também tem telefone** — o canal hoje é o toque barato de quem já
está sendo trabalhado, não só o resgate de quem não tem número. Nenhum item
deste projeto lê os gatilhos nativos `Email Opened`/`Email Link Clicked` do
GHL (`grep -rn "Email Opened\|Email Link Clicked" wesales/*.md`, vazio antes
desta sessão), embora Outreach/Salesloft pontuem exatamente isso há anos
(framework "1 ponto por abertura, 3 por clique, 10 por resposta", achado na
pesquisa desta rodada) para decidir quem a fila de ligação chama primeiro.

**Por que não é cópia do F-21:** o F-21 reage a resposta de e-mail (sinal
forte, texto, reabre `abandoned`); este item reage a abertura/clique (sinal
passivo, sem texto) de quem já está `open` — não precisa reabrir nada,
precisa fazer a fila de ligação que já existe (`Fila Quente`, seção 8.1)
enxergar mais cedo quem deu sinal silencioso. É o par que faltava ao lado
do F-21, não um substituto.

**Cuidado que a pesquisa exige, e que uma cópia ingênua do F-01 ("todo
sinal é sinal quente") erraria:** abertura de e-mail é inflada por
pré-carregamento de pixel de rastreamento (Apple Mail Privacy Protection,
scanners corporativos) — a mesma classe de alarme falso que o F-19 já
ensinou este projeto a temer para resposta automática. Clique é mais
confiável, mas não é imune a scanner de link corporativo. Por isso este
item nunca aplica `fila-quente`/`Prioridade` = 5 (reservados ao sinal forte
do F-01/F-21) a partir de abertura ou clique, e só escalona no **primeiro**
clique de cada contato — abertura conta, nunca escalona sozinha.

**Como:** dois workflows curtos ("Sinal de E-mail — Abertura" e "— Clique"),
mesmo motivo do F-01 (o GHL não expõe com segurança qual gatilho disparou
quando dois tipos de evento dividem um workflow). Os dois somam
`Pontos de engajamento e-mail` (C-34, novo — abertura +1, clique +3); só o
clique, e só no primeiro de cada contato, aplica a tag `email-engajado`
(T-24, novo, marcador permanente) e sobe `Prioridade` (C-05) para 4 — nunca
para 5, e nunca reduzindo quem já está acima de 4. Reaproveita a fila que já
lê `Prioridade` em vez de inventar mecanismo novo (mesma lição do F-06/G-06:
reestruturar em vez de multiplicar). Não precisa do teto de toques (F-04/
F-23) porque não cria toque nenhum — só reordena a fila existente.

**Pronto quando:** todo contato que abre ou clica um e-mail da operação tem
o evento contado em `Pontos de engajamento e-mail`; o primeiro clique de um
contato sem `email-engajado` sobe `Prioridade` para 4 e avisa o gestor uma
única vez; abertura sozinha nunca vira fila nem aviso. Detalhe nó a nó em
`build-wesales.md`, seção 2.55; campo e tag em `campos-e-tags.md` (C-34,
T-24); ambos nascem `[ ]` em `APROVADO.md`. Zero escrita no CRM nesta
rodada: item de especificação pura.

### F-26 · Toda ligação que cai na caixa postal só soma contador — nenhuma mensagem sai, e o recurso nativo que resolveria isso sem gastar tempo do SDR nunca foi olhado, mas ativá-lo cedo demais empilha sobre um canal que dois itens já mediram perto do limite (28/09/2026) — **FEITO em 28/09/2026 (especificação)**

**Resumo:** Reev/Meetime não têm telefonia própria (abrem para o discador
do usuário) e não cobrem isto; o GHL já tem nativo o **Ringless Voicemail
(Voicemail Drop)** — chamada silenciosa (o "truque de operadora": liga,
desliga, liga de novo enquanto o aparelho está offline, a segunda cai
direto na caixa postal, ~70% de acerto) que deixa um áudio pré-gravado sem
tocar o telefone do lead. Pesquisa via `WebSearch` (`help.gohighlevel.com`,
`ideas.gohighlevel.com`, `consultevo.com` e `n8n.io` bloqueados pelo proxy
deste contêiner, mesma barreira já registrada para outros domínios do GHL
— confiança média, várias fontes convergentes, sem confirmar na
documentação oficial). Hoje, cair em `Caixa Postal`/`Não atendeu`
(`build-wesales.md`, seção 4) só incrementa contador e devolve o lead à
fila — nenhuma mensagem sai, porque isso depende de o SDR ter falado ao
vivo na chamada, o que a régua não garante nem mede.

Especificados os nós 5-9 do ramo `Caixa Postal`/`Não atendeu`
(`build-wesales.md`, seção 4), campo `Voicemails automáticos` (C-36) e tag
`voicemail-enviado` (T-26, dispara uma única vez por lead na régua, não a
cada toque perdido) em `campos-e-tags.md`, áudio proposto `VM-1` em
`biblioteca-mensagens.md`, ambos nascendo `[ ]` em `APROVADO.md` pela regra
de sempre; `IMPLEMENTACAO-WORKFLOWS.md` (W4, C4-C8) e `GUIA-MONTAGEM.md`
atualizados no mesmo commit.

**O que o item não resolve, de propósito:** o mesmo "truque de operadora"
soma pelo menos uma chamada extra por voicemail deixado — exatamente no
canal que F-08 e F-14 já mediram perto ou acima da referência
internacional segura (50-75 chamadas/dia) e sob risco do bloqueio
automático de "chamada abusiva" que toda operadora brasileira oferece,
ligado por padrão, desde agosto/2026. Com ~10-13 leads novos/dia, um drop
por lead soma **~20-40 chamadas curtíssimas extras por dia** no mesmo
número. F-09 (freio de telefone) existe exatamente para conter esse tipo
de acréscimo — por isso este item nasce **especificado, não ativado**: a
montagem na tela espera o F-09 ter decisão do dono, registrado como
dependência explícita em `APROVADO.md`, `campos-e-tags.md`,
`build-wesales.md`, `IMPLEMENTACAO-WORKFLOWS.md` e `GUIA-MONTAGEM.md`.

**Pronto quando:** tag e campo criados na tela, áudio `VM-1` gravado e
aprovado pelo dono, nós 5-9 montados no `Pós-ligação` publicado — e o F-09
já com decisão tomada. Zero escrita no CRM nesta rodada.

### F-25 · Nenhum item marca e-mail que bateu (bounce) como inválido — a cadência de e-mail continua tentando o mesmo endereço morto, e cada tentativa é o próprio risco que o F-22 já mediu (28/09/2026) — **FEITO em 28/09/2026 (especificação)**

**Por quê:** mesma pergunta do R-13 ("a base suja infla métrica e queima
SDR") aplicada ao canal que R-13 nunca cobriu — R-13 fechou a higiene do
**telefone** (`telefone-invalido`, T-09: portão de entrada + tag, 18/09/2026),
mas o e-mail só ganhou disparo real depois (F-15, 22/09/2026) e nenhuma
rodada voltou para perguntar a mesma coisa do canal novo — a mesma classe de
lacuna que G-06/G-07/F-19/F-20/F-21/F-22 já fecharam cada um a seu turno
("a guarda mais velha nunca alcança o canal mais novo"). Hoje um endereço
que bate (`Resgate por E-mail — Sem Telefone`, seção 2.30, F-15) não é
marcado de jeito nenhum: o `Reengajamento 90 dias` (R-08) recicla o contato
de volta para `abandoned`+`nutricao-90d` a cada 90 dias e o `Resgate por
E-mail` (`Allow Re-entry` ligado) tenta `EM-1`/`EM-2` de novo no mesmo
endereço morto, para sempre. Não é só desperdício: o F-22 (2.51) já mediu
que o risco real da rampa de e-mail nativa do GHL não é volume, é
**qualidade** — "bounce alto numa lista nunca limpa" é um dos dois motivos
documentados de a rampa regredir (`Stage declined`) — e hoje nada neste
projeto lê o evento que produz esse risco.

**Pesquisado antes de desenhar (`WebSearch`):** confirmado que o GHL expõe
gatilho nativo para isto — `Email Events` filtrado por `Event = Bounced` —
e a própria HighLevel publica a receita oficial para o caso ("Auto-Enable
Email DND When a Contact's Email Bounces"): gatilho `Email Events` →
`Bounced` seguido de uma ação de DND com escopo `Outbound Email`. A mesma
fonte documenta o limite que este item herda sem poder resolver: o gatilho
**não distingue bounce definitivo (endereço não existe) de temporário**
(caixa cheia, erro momentâneo do servidor) — "nem todo bounce significa
endereço permanentemente inválido", e nenhuma verificação de e-mail desliga
o DND sozinha depois. Outreach pausa o Prospect para revisão manual no
primeiro bounce; Salesloft tolera um bounce definitivo ou dois temporários
antes de marcar; Apollo remove o endereço de circulação no primeiro bounce
definitivo — as três convergem em "não trate todo bounce como igual, mas
não deixe nenhum passar sem registro", exatamente o que a receita nativa (e
este item) fazem com o que o conector permite ler.

**Por que não é `nao-perturbe` (T-06) nem `Set Contact DND` em todos os
canais (2.9.5/R-17):** um bounce é falha de **entrega**, não pedido de
silêncio — reaproveitar `nao-perturbe` confundiria a auditoria de
compliance do R-14 (Smart Lists 8.26/8.27, que leem essa tag como
"consentimento revogado") e desligar DND em todos os canais pararia
telefone e WhatsApp por um motivo que é só do e-mail. Mesmo raciocínio que
já separou `email-invalido` (novo, mirror de `telefone-invalido`/T-09) de
`nao-perturbe`: são dois estados diferentes de um contato, um de
consentimento, outro de alcançabilidade.

**Como:** workflow novo "Higiene de E-mail — Bounce", especificado nó a nó
em `build-wesales.md`, seção 2.56 — soma o contador `Bounces de e-mail`
(C-35, novo), aplica `email-invalido` (T-25, novo), liga `Set Contact DND`
com escopo **só e-mail**, remove o contato do `Resgate por E-mail — Sem
Telefone` (2.30, único workflow que hoje manda `Send Email`) e avisa o
gestor **uma única vez**, no primeiro bounce do contato — bounces
seguintes só somam o contador, mesmo padrão de "não treinar o gestor a
ignorar alarme repetido" já usado no F-24/nó 5 e no G-25. O aviso deixa
explícito o limite documentado acima: nenhuma automação desliga este DND
sozinha, revisão é manual.

**Campo novo:** `Bounces de e-mail` (C-35, `NUMERICAL`, cumulativo — mesmo
padrão de contador de evento que C-06/C-07/C-11/C-12/C-26/C-31/C-32/C-33/
C-34). **Tag nova:** `email-invalido` (T-25, marcador permanente, mesma
classe que `telefone-invalido`/T-09 — sinaliza canal não confiável, nunca
removida automaticamente). Nenhum dos dois sai por API neste conector
(campo é criação de tela; tag nasce `[ ]` em `APROVADO.md` pela regra de
sempre — nenhuma linha nova vira `[x]` sozinha). Zero escrita no CRM nesta
rodada.

**Pronto quando:** um bounce em qualquer envio de e-mail da operação marca
o contato com `email-invalido`, soma `Bounces de e-mail`, desliga o envio
de e-mail (sem tocar telefone/WhatsApp) e tira o contato do `Resgate por
E-mail`, avisando o gestor uma única vez — o segundo bounce do mesmo
contato não repete o aviso, só soma o contador. Detalhe nó a nó em
`build-wesales.md`, seção 2.56; campo e tag em `campos-e-tags.md` (C-35,
T-25); ambos nascem `[ ]` em `APROVADO.md`. Zero escrita no CRM nesta
rodada: item de especificação pura.

### F-27 · Toda chamada `Inbound` cai no vácuo desde a seção 2.27 — inclusive o lead que retorna a própria tentativa de telefone da régua enquanto o SDR está discando outro número, o cenário mais provável desta operação (28/09/2026) — **FEITO em 28/09/2026 (especificação)**

**Por quê:** `grep -n "Call Status\|chamada recebida\|Inbound Call"
wesales/build-wesales.md` confirma que a única linha deste projeto inteiro
que toca numa chamada `Inbound` é o nó 1 da seção 2.27 (F-06) — e ela só
descarta ("chamada recebida não é tentativa da cadência"). A operação roda
Power Dialer outbound com meta de 100 ligações/dia por SDR: o cenário mais
comum para uma chamada `Inbound` aqui não é um desconhecido, é o próprio
lead retornando uma das 8 tentativas de telefone da régua enquanto o SDR
está ao telefone com outra pessoa — ninguém disponível para atender ao
vivo. Pesquisa de concorrência (mesma pergunta do F-07/F-08/F-14/F-22/F-24/
F-25/F-26): o próprio GHL descreve o "Missed Call Text-Back" como a
automação nativa de maior ROI da plataforma — recupera lead que iria para
o concorrente, respondendo em segundos, sem gastar mais anúncio
(`help.gohighlevel.com`, `ideas.gohighlevel.com` e múltiplos blogs
especializados em GHL convergindo no mesmo mecanismo nativo; nenhuma fonte
mostrou Reev, Meetime, Outreach ou Salesloft cobrindo o caso — nenhum dos
quatro é a própria operadora de telefonia). Uma ligação de volta é, no
mínimo, tão quente quanto o clique em link que o F-01 já trata como sinal
máximo; hoje ela é inteiramente invisível: sem tag, sem tarefa, sem
mensagem.

**Como:** workflow novo "Retorno de Chamada Perdida", especificado nó a nó
em `build-wesales.md`, seção 2.58, pelo gatilho nativo `Call Status`
(Direção `Inbound`, Status não atendida — nome exato do valor a confirmar
na tela, `help.gohighlevel.com` bloqueado pelo proxy deste contêiner nesta
sessão, mesma barreira já registrada para outros domínios do GHL em
`APRENDIZADOS-CRM.md`, **confiança média**). Prioriza o lead (`Prioridade`
= 5, tag `fila-quente`, mesmo tratamento máximo do F-01) e cria a tarefa
`[RETORNO]` para o `Contact Owner` — nenhum dos dois depende de campo ou
tag nova. Só a gravação do sinal em si usa uma 4ª opção nova em `Sinal
recebido` (C-13, mesma classe de edição de `SINGLE_OPTIONS` já usada pelo
F-21), e a mensagem automática (`MRC-1`, `biblioteca-mensagens.md`) segue
o teto de toques do F-04/F-23 e o bloqueio de sempre para envio real de
WhatsApp. Desenhado para não repetir o erro que o F-11/G-16 já ensinaram
(tratar todo evento recebido como sinal comercial automático): o nó 2 só
segue se o contato já tiver oportunidade `open`/`abandoned` na operação —
uma chamada de quem nunca foi lead (engano, contato pessoal) não move nada.

**Campo/tag novos:** nenhum — reaproveita `Sinal recebido` (C-13, ganha só
uma opção nova), `Prioridade`, `fila-quente` e `Toques na semana` (C-26),
todos já existentes. A única pendência de tela é a opção nova em C-13,
registrada em `campos-e-tags.md` e como linha própria `[ ]` em
`APROVADO.md` — mesma classe de limite (edição de campo, não sai por API)
já documentada para o F-21. `GUIA-MONTAGEM.md` e
`IMPLEMENTACAO-WORKFLOWS.md` (W31) atualizados no mesmo commit. F-09,
F-10, G-11 (item 1), G-19, G-27/G-29 e G-31 continuam sendo as decisões
sem prazo fixo que esperam o dono, sem novidade nesta sessão.

**Pronto quando:** opção `Retornou ligação` criada em `Sinal recebido` na
tela, workflow publicado, e uma chamada de teste de volta ao número da
operação confirma `Prioridade` = 5, tag `fila-quente` e a tarefa
`[RETORNO]` — sem esperar a mensagem automática, que segue dependente do
bloqueio de sempre. Detalhe nó a nó em `build-wesales.md`, seção 2.58;
texto em `biblioteca-mensagens.md` (MRC-1); campo em `campos-e-tags.md`
(C-13); `APROVADO.md` com a linha nova, `[ ]`. Zero campo novo, zero tag
nova, zero escrita no CRM nesta rodada: item de especificação pura.

### F-28 · O F-03 prometeu "dá pra dizer nota ≥ 70 acerta X%" e nunca calculou — o alerta em tempo real do 5.1 pega o caso isolado, nenhum lugar soma os casos (28/09/2026) — **FEITO em 28/09/2026 (script + primeira leitura real)**

**Por quê:** o próprio "Pronto quando" do F-03 (acima, bloco 6) diz "dá pra
dizer 'nota ≥ 70 acerta X%' — e corrigir a régua da seção 9 com dado, não
com achismo". O workflow 5.1 (`build-wesales.md`) cumpre metade disso: no
instante em que o closer registra o veredito, compara com a nota e avisa o
gestor quando os dois discordam. Mas isso é caso a caso — nenhum lugar deste
projeto soma esses casos ao longo do tempo para responder à própria
pergunta que o F-03 fez. Pesquisa de concorrência antes de desenhar (mesma
pergunta de sempre, agora voltada aos dois pilares do bloco 6 que nunca
tinham ganhado extensão — F-02 e F-03, todos os outros quatro já
estendidos por F-07 a F-27): Meetime descreve o "call review" — reunião
semanal de 30-45min entre SDR e closer para revisar oportunidades e
recalibrar o critério de qualificação — como prática padrão do mercado
brasileiro de pré-vendas; Outreach (Kaia) e Salesloft (scorecards)
resolvem com IA de coaching sobre gravação de chamada, infraestrutura que
este projeto não tem (e que o F-06/F-09 já mostraram custar caro e
disputar o mesmo canal de telefone perto do limite). As três abordagens
têm o mesmo formato: pessoa olhando número, de tempos em tempos. Este item
não substitui a reunião semanal (ela decide o que fazer; dado nenhum
decide sozinho) — automatiza o número que ela hoje calcula na mão ou nem
calcula, e um concorrente olhando a tela nunca veria: não é um card, é um
script que lê o CRM e nunca escreve nele.

**Como:** script novo, só leitura, `wesales/tools/calibracao_regua.py` —
zero escrita no CRM, então não depende do `APROVADO.md`. Busca as
oportunidades do `FUNIL DE VENDAS` nas três etapas onde o closer já pode
ter atuado (`REUNIÃO DE DIAGNÓSTICO`, `NEGOCIAR`, `FORMALIZAR`), lê cada
contato e mantém só quem tem `Data do veredito do closer` preenchida
**e não é contato de teste** — a exclusão de teste não é cautela
hipotética: é o achado real desta mesma rodada (abaixo). Agrupa por faixa
(as mesmas quatro da seção 9.1: A ≥70, B 45-69, C 25-44, D <25), calcula a
taxa de `Sim` por faixa e lista os casos que já dispararam (ou deveriam
disparar) o alerta do 5.1. Roda com `GHL_TOKEN` (Private Integration
Token, mesmo padrão do `faxina_tarefas.py`) — publicar um cron para ele é
`.github/*`, fora de `wesales/`, regra 5 desta rotina; fica pronto para
quem tiver o token rodar a qualquer momento, e o `--escrever` grava o
relatório em `wesales/RELATORIO-CALIBRACAO.md`.

**Achado ao rodar contra a subconta real (não hipótese — as quatro
oportunidades das três etapas foram lidas nesta sessão por
`opportunities_search-opportunity` + `contacts_get-contact`, sem
`GHL_TOKEN` disponível neste ambiente de nuvem, mesma lógica do script
aplicada à mão):** zero vereditos reais hoje. Os dois leads reais em
`NEGOCIAR` (`Daniel`, `Genilson | Bombeiro`, nota 93 os dois) ainda não
têm veredito do closer. O único veredito que existe na subconta agora —
nota 23, `Reunião foi qualificada` = `Sim`, o pior caso possível de
descalibração se fosse real — é do contato de teste "9940"
(`Pablo Sampaio`, `rdaijzR0ZVCmXLAJ6jT2`), usado pelo dono para testar o
`build_estagnacao.py` (G-23, acima). Contar esse dado teria feito o
relatório mentir na primeira leitura — exatamente o motivo de o script
excluir teste por lista fechada de ID **e** por heurística de nome/e-mail,
não confiar em nenhuma tag isolada. `RELATORIO-CALIBRACAO.md` já existe
com esta primeira leitura, incluindo a nota de proveniência (leitura via
MCP desta sessão, não via `GHL_TOKEN`).

**Campo/tag novos:** nenhum — reaproveita `Nota de qualificação`,
`Reunião foi qualificada`, `Motivo da desqualificação` e `Data do veredito
do closer` (C-15 a C-17, todos já criados na tela). Zero linha nova em
`APROVADO.md`: o script nunca escreve no CRM.

**Pronto quando:** o script roda contra a subconta real e devolve a taxa
de acerto por faixa — cumprido nesta mesma rodada, mesmo com amostra zero:
zero é a resposta real de hoje, não falha do mecanismo, e o relatório diz
isso em vez de fingir uma leitura que não existe. Passa a responder de
verdade quando `Daniel`/`Genilson` (ou o próximo lead real) ganhar
veredito do closer — sem exigir nenhuma mudança neste script.

### F-29 · A higiene de base cobre telefone (R-13) e e-mail (F-25), e o WhatsApp — o canal de toda mensagem automática do projeto — nunca ganhou o par (28/09/2026) — **FEITO em 28/09/2026 (especificação)**

**Por quê:** achado aplicando à higiene de base a mesma pergunta que já
abriu F-20/F-21/F-25 — "esta guarda existe em todo canal que a operação
usa, ou só no que motivou o achado original?" `telefone-invalido` (T-09,
R-13, 18/09/2026) para o telefone e `email-invalido` (T-25, F-25, sessão
anterior a esta, mesmo dia) para o e-mail já existem; o WhatsApp — canal
de M1 a M3, MI-0/MI-F, RE-1/RE-2, NS-1/NS-2, os quatro lembretes do
Pós-agendamento, `MRC-1` (F-27) e `QI-1` (G-06) — nunca ganhou o
equivalente. Um número que nunca teve WhatsApp continua recebendo a mesma
mensagem em cada tentativa da régua, para sempre, sem tag nem contador que
marque o número como morto. Pesquisado antes de desenhar: nenhuma das
quatro plataformas (Reev/Meetime/Outreach/Salesloft) precisa resolver
isto — operam sobre WhatsApp Business API/e-mail próprios, com status de
entrega nativo —, mas nenhuma delas tem o motivo real desta subconta ter
o problema: o WhatsApp aqui não sai pelo canal nativo do GHL, sai por um
Custom Conversation Provider (Stevo, QR, 22/09/2026) que entrega toda
mensagem — entrada e saída — tipada como `TYPE_CUSTOM_SMS` (fato já
medido por API, G-09).

**Como:** workflow novo "Higiene de WhatsApp — Número Inválido", gatilho
nativo `Messaging Error Code - SMS` (dispara pelo **tipo** SMS da
mensagem, não pelo provedor — coerente com o único fato que este projeto
já testou ao vivo, não só pesquisou: o G-09 provou que `Customer Replied —
Canal: WhatsApp e SMS` enxerga tráfego de entrada da Stevo exatamente
porque ela se anuncia como SMS). Tag `whatsapp-invalido` (T-27, mirror de
T-09/T-25) e campo `Números de WhatsApp inválidos` (C-37, `NUMERICAL`,
contador cumulativo, mesmo padrão de C-31 a C-36). Detalhe nó a nó em
`build-wesales.md`, seção 2.59.
**Pronto quando:** o workflow publicado, campo e tag criados na tela, o
patch de portão (`tag whatsapp-invalido ausente`) aplicado em todo `Send
WhatsApp`/`Send SMS` da operação, e o primeiro erro real de número
inatingível confirmar as duas pendências que este item regista em vez de
supor: (a) que o código de erro corresponde de fato a "sem WhatsApp", e
(b) que o gatilho de erro de SMS dispara para mensagem transportada pela
Stevo.

**Resumo:** diferente de F-25 (mirror direto de R-13, canal nativo dos
dois lados), este item não pôde copiar o desenho às cegas — a mesma lição
que o F-21 já tinha ensinado para o sinal. Duas pendências de confiança
ficam registradas e não escondidas, mesma classe da dependência LC
Phone/linha própria do F-06/F-08/F-09: (1) quais códigos de
`Messaging Error Code - SMS` a Stevo de fato gera para "nunca teve
WhatsApp" — só o primeiro caso real decide; (2) se a Stevo, como provedor
terceiro, chega a reportar falha de entrega de volta ao GHL pelo webhook
`ProviderOutboundMessage` — se não reportar, o workflow nunca dispara, não
por erro de desenho, por ausência de dado na origem (Stevo), uma camada
abaixo do "o GHL não expõe" já visto em outros itens. Por esse mesmo
motivo, o desenho não usa `Set Contact DND` (diferente do W30/e-mail):
escopar a `WhatsApp` arriscaria não bloquear nada (a Stevo não é o canal
nativo) e escopar a `SMS` bloquearia mais do que o pretendido se este
projeto voltar a usar SMS de verdade — a defesa real é o portão de tag,
mesmo mecanismo que já protege telefone e e-mail. `IMPLEMENTACAO-
WORKFLOWS.md` (W32) e `GUIA-MONTAGEM.md` atualizados no mesmo commit.
Zero campo, zero tag, zero escrita no CRM nesta rodada: `whatsapp-
invalido` (T-27) e `Números de WhatsApp inválidos` (C-37) nascem `[ ]` em
`APROVADO.md`, mesma regra de sempre. F-09, F-10, G-11 (item 1), G-19,
G-27/G-29 e G-31 continuam sendo as decisões sem prazo fixo que esperam o
dono, sem mudança nesta rodada.

### G-36 · O F-29 fechou sem o parágrafo de fechamento que F-24 a F-28 ganharam nesta seção — mesmo lapso que o G-24 já tinha corrigido para o G-23 (28/09/2026) — **FEITO em 28/09/2026 (coerência da própria seção "Ordem sugerida")**

**Por quê:** o G-24 (23/09/2026) tinha deixado uma regra prática depois de
achar o mesmo tipo de buraco: "todo G-item que fechar nesta família
confere, antes do commit, se o parágrafo de recapitulação no fim da 'Ordem
sugerida' foi escrito". A regra pegou — G-25 a G-35 e F-24 a F-28
cumpriram, cada um deixando um parágrafo curto no fim desta seção
recapitulando o que mudou. O F-29 (item acima) fechou o `### F-29` no
corpo do Bloco 6 e foi direto para o `---`, sem voltar ao fim do arquivo:
o parágrafo mais recente ali continuava sendo o do F-28, sem citar o
F-29. Causa provável: a regra do G-24 fala em "G-item" no texto — uma
leitura literal não pega um item que começa com F, e F-24 a F-28
cumpriram por hábito, não por regra escrita que os obrigasse.

**Como:** `git fetch` nas duas branches irmãs
(`abertura-operacao-dnd-n7dnjv`, atualizada 28/09 ~02:53 UTC — o mesmo
commit que o F-29 já tinha lido; `abertura-operacao-dnd-ib6xaz`, sem
commit novo desde 27/09 18:03 UTC) confirma que não há novidade para F-09,
F-10, G-11 (item 1), G-19, G-27/G-29 ou G-31 além do que o F-29 já
registrou. CRM reconfirmado por API antes de fechar:
`opportunities_search-opportunity` (`status: all`) segue em **64**
oportunidades, mesma composição de sempre (39 `CONECTAR` open + 10
`NOVO LEAD` abandoned + 8 `CONECTAR` lost + 2 `NOVO LEAD` open + 2
`NEGOCIAR` open + 1 `NOVO LEAD` lost + 1 `REUNIÃO DE DIAGNÓSTICO` lost + 1
`NEGOCIAR` lost); `locations_get-custom-fields` segue em **60** campos de
contato (`SDR responsável` ainda só com a opção `Andreyna Siqueira`,
`B · Quanto pode investir` sem nenhum workflow lendo — mesmo estado do
G-29/G-34/G-35).

A mesma leitura do `DE-PARA-SESSOES-CRM.md` da branch irmã (commit
`3de2868`) trouxe um dado lido, não hipotético, que vale registrar para a
próxima rodada não reabrir: ela nota que o F-27 especifica o gatilho `Call
Status` para "Retorno de Chamada Perdida" sem saber que já existe,
publicado do outro lado, um workflow parecido ("Trava de canal — falou
hoje", `c4a3aab7-5fb2-4d05-80cf-0364a0a90bc5`) no mesmo tipo de gatilho.
**Checado nó a nó antes de virar achado — não é conflito:** `Trava de
canal` dispara em `Call Status = completed`, direção de saída, ligação
**atendida** pelo Power Dialer; o F-27 especifica `Direção = Inbound` **e**
`Status = No Answer`. Filtros diferentes no mesmo tipo de gatilho não
colidem no GHL. Fica registrado só para não obrigar a próxima rodada a
refazer esta mesma checagem ao ler a mesma nota.

**Zero campo, zero tag, zero escrita no CRM: item de coerência dentro do
próprio roadmap, não depende de `APROVADO.md`.**

**Pronto quando:** feito — este `### G-36` e o parágrafo de recapitulação
no fim da "Ordem sugerida" (abaixo) são o próprio "Pronto quando", como já
valia para o G-24.

**Resumo:** a regra do G-24 falou só em "G-item"; o primeiro item a
quebrá-la foi um F-item, que ela não nomeava. Regra corrigida (detalhe em
`APRENDIZADOS-CRM.md`): o parágrafo de fechamento não é ritual do prefixo
`G-`, é ritual de qualquer item — `F-`, `G-` ou `R-` — que altere a lista
de "decisões que esperam o dono" ou feche citando "sem mudança nesta
rodada".

---

### F-30 · A Interceptação de Sinal só filtra opt-out (R-17) e auto-resposta (F-19/F-20) — um "não tenho interesse" educado ainda vira Prioridade 5 e "ligar agora" (28/09/2026) — **FEITO em 28/09/2026 (especificação)**

**Por quê:** pesquisando Reev/Meetime/Outreach/Salesloft de novo antes de
considerar o bloco 6 esgotado (rotina obrigatória de todo item novo), achado
que o próprio F-19 (`build-wesales.md`, seção 2.48) já tinha citado, sem
usar, a peça que fecha esta lacuna: o gatilho `Customer Replied` filtra por
`Contains Phrase`/`Exact Match`/tag/canal **e** `Intent Type` — filtro nativo
que classifica o sentimento da resposta. O F-19 só perguntou se o `Intent
Type` tinha uma categoria de "ausência" (não tem) e seguiu por lista de
frases; ninguém voltou a perguntar se ele resolve o problema que motivou o
R-17 e o F-19 na origem — separar "sinal quente" de "sinal que não é quente"
— para o caso que nem um nem outro cobre: uma resposta genuína, não
automática, que **recusa educadamente** ("não tenho interesse, obrigado",
"já contratei outra agência", "não é pra mim agora"). Essa frase não bate
nenhuma das 17 frases de opt-out (explícitas demais) nem nenhuma das 19 de
ausência/auto-resposta (não é auto-resposta) — passa direto pela 2.9.3:
`Prioridade` = 5, tag `fila-quente`, tarefa `[CADENCIA] ... ligar agora`. O
SDR liga "agora" para um lead que acabou de dizer que não quer. Mesma classe
de alarme falso que o F-19 corrigiu para ausência, agora para rejeição —
e o mesmo `Stop on Response` nativo (seções 2.2/2.10) encerra a régua de 12
tentativas no mesmo segundo, em silêncio, do jeito que o F-19 já descreveu
para o outro caso.

**Pesquisado antes de desenhar, com uma ressalva de método explícita:** o
proxy deste contêiner bloqueia todos os domínios `gohighlevel.com`
(`ABERTURA.md` já tinha medido isso em 27/09/2026 para outro fim) — não deu
para abrir a documentação oficial ao vivo. A pesquisa saiu por busca externa
(três consultas, fontes independentes: `help.gohighlevel.com` indexado por
terceiros, blogs especializados em HighLevel) e todas convergem: o filtro
`Intent Type` do gatilho `Customer Replied` classifica cada resposta em
`POSITIVE`/`NEGATIVE`/`NONE` por IA nativa, embutido no próprio filtro do
gatilho (não é o nó separado `AI Intent Detection`, que é ação premium
cobrada por execução — o filtro do gatilho é dimensão de trigger, mesma
família de `Contains Phrase`/canal que a 2.9.3/2.9.5 já usam sem custo
extra conhecido). Nenhuma das quatro plataformas de referência (Reev,
Meetime, Outreach, Salesloft) embute classificação de sentimento de graça
no próprio gatilho de reply — quem tem isso paga um add-on de IA à parte ou
constrói regra manual; o GHL oferece de graça, dentro do mesmo filtro que
este projeto já usa desde o R-17, e nunca tinha sido lido até o F-19 citar
de passagem. **Limite documentado, não escondido, do jeito que o F-06/F-29
já registraram para os deles:** (1) é classificador de caixa-preta — não há
como ver a confiança da classificação nem corrigir um falso `NEGATIVE` em
resposta com ironia ou crítica construtiva ("não sei se funciona, mas manda
mais informação"); por isso este item **nunca fecha a oportunidade nem
aplica DND sozinho** — só evita o alarme falso e avisa, mesma filosofia do
F-19, nunca decide por conta própria o que o R-17 decide com uma frase
explícita; (2) não testado ao vivo se `Intent Type` classifica tráfego que
chega como `TYPE_CUSTOM_SMS` (o WhatsApp desta subconta via Stevo, G-09) do
mesmo jeito que classifica WhatsApp/e-mail nativos — o G-09 só confirmou isso
para `Contains Phrase`; (3) custo do filtro por execução não confirmado
(a mesma pesquisa que achou a lista de filtros não achou preço específico do
`Intent Type` como dimensão de trigger, só do nó de ação `AI Intent
Detection`, que é outra coisa) — conferir na tela antes de montar.

**Como — filtro do gatilho, aditivo às duas listas já existentes:**
`Intent Type` **não é** `Negative`, combinado em E com os `Doesn't Contain`
de opt-out (2.9.5/2.9.6, 17 frases) e de ausência/auto-resposta (F-19/F-20,
19 frases, seção 2.48) — nas duas Interceptações de Sinal que já existem
(2.9.3, WhatsApp/SMS, publicada) e na que ainda está só especificada (2.50,
E-mail, F-21, W27 no `IMPLEMENTACAO-WORKFLOWS.md`, ainda não montada).

**Como — workflow novo "Resposta com Intenção Negativa", um só para os três
canais que a operação usa (lição do F-19→F-20 aplicada desde o início, não
depois — mesma lição que o F-21 já citou para si mesmo):**

| Configuração | Valor |
|---|---|
| Gatilho | `Customer Replied` — Canal: WhatsApp, SMS e E-mail — `Intent Type` **é** `Negative` — `Doesn't Contain` as duas listas (opt-out + ausência), combinadas em E: uma resposta que já bate uma das duas listas segue pelo workflow dela (2.9.5/2.9.6/F-19/F-20), nunca duplica aviso aqui |
| Janela de envio | Sem restrição, 24/7 — nenhum nó manda mensagem ao lead, mesmo padrão do 2.9.5/2.48/2.50 |
| Allow Re-entry | Ligado — cada resposta negativa é um evento novo, mesmo raciocínio do 2.9.5/F-19 |
| Stop on Response | Desligado |

| # | Nó | Ação | Configuração |
|---|---|---|---|
| 1 | Buscar oportunidade | Find opportunity | Pipeline `FUNIL DE VENDAS` · "Most recently created opportunity". Ramo **Opportunity Not Found**: segue mesmo assim (auditoria é do contato, mesmo padrão do F-19 nó 1) |
| 2 | Marcar | Add Contact Tag | `resposta-negativa` (T-28, pulso de auditoria — mesma ideia da `toque`/T-15 e da `resposta-automatica`/T-23: registra o evento, nunca vira estado permanente) |
| 3 | Contar | Update Contact Field (Math +1) | `Respostas negativas` (C-38, `NUMERICAL`) — mesmo padrão cumulativo de C-33/C-34/C-35/C-36/C-37: sem contador, "quantas vezes a base recusou sem pedir silêncio" não aparece em lugar nenhum |
| 4 | Registro | Add Note | `Resposta com intenção negativa detectada em {{right_now}} (Intent Type nativo do GHL, POSITIVE/NEGATIVE/NONE) — não é opt-out nem auto-resposta, mas também não é sinal quente; revisar antes de continuar a régua` |
| 5 | Aviso, sempre | Internal Notification | Para `Contact Owner`: `{{contact.name}} respondeu com sinal negativo (classificação nativa do GHL) — não pediu silêncio nem é auto-resposta, mas também não é "quero saber mais". A cadência que ele estava rodando já parou (Stop on Response nativo não distingue o motivo). Decida: desqualificar (Motivo da desqualificação) ou aguardar — não ligar "agora" como se fosse sinal quente.` |

**Patch pendente na 2.9.3 (`Interceptação de Sinal — Resposta v2`, já
publicada, mesma mecânica do patch que o F-19 já deixou pendente para a
lista de ausência):** acrescentar `Intent Type não é Negative` ao filtro do
gatilho — mecânico, não decisão, próximo passo de quem tiver a tela. Na
2.50 (E-mail, F-21), que **ainda não foi montada**, o filtro já nasce com a
condição desde a especificação (`build-wesales.md`, seção 2.50, atualizada
no mesmo commit) — não precisa de patch porque não há nada publicado para
remendar ainda, mesma diferença que o próprio F-21 já registrou para o
2.9.3 versus o W27.

**Zero redesenho dos workflows existentes além do filtro do gatilho:** a
2.9.3 e a 2.50 continuam tratando toda resposta que sobra (positiva, neutra,
ou negativa-mas-já-capturada-por-opt-out/ausência) exatamente como hoje —
este item só tira mais uma fatia do que "sobra" para a 2.9.3/2.50
escalonarem como sinal quente por engano, mesmo papel que o F-19 já cumpriu
para a fatia de ausência.

**Pronto quando:** um lead que responde recusando educadamente (sem opt-out
explícito, sem ser auto-resposta) não gera `Prioridade` = 5 nem tarefa
`ligar agora` na 2.9.3/2.50, e fica registrado (tag + contador + aviso ao
gestor) em vez de virar uma ligação indesejada — e o primeiro caso real
confirma as duas pendências que este item regista em vez de supor: se
`Intent Type` classifica tráfego `TYPE_CUSTOM_SMS` da Stevo, e quanto custa
por execução. Detalhe nó a nó em `build-wesales.md`, seção 2.60; tag e campo
em `campos-e-tags.md` (T-28, C-38); ambos nascem `[ ]` em `APROVADO.md`.
`IMPLEMENTACAO-WORKFLOWS.md` (W33) e `GUIA-MONTAGEM.md` atualizados no
mesmo commit. Zero campo, zero tag, zero escrita no CRM nesta rodada. CRM
reconfirmado por API antes de desenhar: 64 oportunidades, mesma composição
de sempre; 60 campos de contato, sem novidade. F-09, F-10, G-11 (item 1),
G-19, G-27/G-29 e G-31 continuam sendo as decisões sem prazo fixo que
esperam o dono, sem mudança nesta rodada.

---

### F-31 · A tabela do G-05 manda submeter 16 Templates à Meta e nenhum documento diz em qual categoria — a escolha vale 6× de preço e um teto de frequência que nem o F-07 mede (28/09/2026) — **FEITO em 28/09/2026 (especificação)**

**Por quê:** reconciliação de sempre antes de desenhar (hábito do
G-31/G-32/G-33/F-26 a F-30): `git fetch` nas duas branches irmãs
(`abertura-operacao-dnd-n7dnjv`, sem commit novo desde o já lido pelo
F-29/F-30; `abertura-operacao-dnd-ib6xaz`, sem commit novo em `wesales/`)
não achou resposta nova para F-09, F-10, G-11 (item 1), G-19, G-27/G-29 ou
G-31. CRM reconfirmado por API antes de desenhar: `opportunities_search-
opportunity` (status `all`) segue em **64 oportunidades**, mesma
composição (47 `CONECTAR`, 13 `NOVO LEAD`, 3 `NEGOCIAR`, 1 `REUNIÃO DE
DIAGNÓSTICO`); `locations_get-custom-fields` segue em **60 campos de
contato**, sem novidade (`Sinal recebido` ainda só com as duas opções de
sempre — nenhuma das pendências do F-21/F-27/F-30 apareceu na tela ainda).
Sem achado de reconciliação, a sessão foi à pesquisa de concorrência de
sempre — mas desta vez não mirou um sinal, uma guarda de canal ou uma
lacuna de conteúdo (F-19 a F-30 já esgotaram essas três frentes): mirou a
única tabela deste projeto que lista uma ação pendente do dono sem
explicar **como** executá-la — a tabela "Template Meta" do G-05
(`biblioteca-mensagens.md`), 15 códigos "A submeter" mais `MRC-1` (F-27,
16 no total), nenhum com a categoria que a Meta exige na submissão.

**A lacuna, e por que não é o F-07:** o F-07 (seção 2.25) protege a
Quality Rating do nosso número — risco que só existe se **nosso** volume
gerar bloqueio ou denúncia. A categoria do Template (`Utility` ×
`Marketing` × `Authentication`) é um eixo diferente, decidido na
submissão, não em tempo de execução: ela muda o preço por mensagem (achado
de mercado dos EUA, só para ilustrar a proporção: `Utility` ≈ US$ 0,004,
`Marketing` ≈ US$ 0,025, 6×) e expõe o envio a um teto de frequência por
**destinatário** que a Meta aplica somando **todas** as empresas que
escrevem para aquele número (~2 mensagens `Marketing`/dia, dinâmico) —
código de descarte `131049`, do qual `Utility`/`Authentication` são
isentos. Um número com Quality Rating perfeita (F-07 em dia) pode ter uma
mensagem descartada porque o lead já recebeu duas mensagens `Marketing` de
**outros** aplicativos hoje — nada que o checklist do F-07 meça ou
explique, mesma relação de "mesma família, mecanismo novo" que o F-22 já
tem com o F-07/F-08.

**Pesquisado (`WebSearch`, confiança média — `developers.facebook.com` e
`business.whatsapp.com` bloqueados pelo proxy deste contêiner, mesma
barreira do `gohighlevel.com` já registrada no F-08/F-30; convergência de
fontes independentes — `wati.io`, `wanotifier.com`, `chatarmin.com`,
`watease.com`, `customer.io`, `gupshup.ai` — mais um resultado de busca
citando o próprio `developers.facebook.com/.../per-user-limits/`, não lido
direto, e o título de um artigo do `help.gohighlevel.com` confirmando que
o mesmo erro aparece surfaceado dentro do GHL):** `Utility` cobre
atualização ligada a uma transação que a pessoa já iniciou (pedido,
agendamento); `Marketing` cobre conteúdo promocional ou de reengajamento
— mesmo em tom educado, se a mensagem persuade ou cobra algo que a pessoa
não pediu, a Meta trata como `Marketing`. E a categoria **não é decisão
definitiva de quem submete**: a revisão automática da Meta pode
reclassificar um Template aprovado como `Utility` de volta para
`Marketing` se a linguagem ler como promocional depois — achado ao notar
múltiplos guias de terceiros dedicados só a "como evitar que a Meta
reclassifique seu Template".

**Como:** os 16 códigos classificados com categoria candidata, nível de
confiança e razão — usando o **texto** de cada Template em
`biblioteca-mensagens.md` como evidência, não o nome do código. Os quatro
lembretes do Pós-agendamento (`PA-CONF`/`PA-R24`/`PA-R3H`/`PA-R30`) são o
caso de alta confiança em `Utility` (o próprio exemplo canônico da
literatura pesquisada é "lembrete de compromisso"); a cadência fria
(`M1-a`/`M1-b`/`M2-v1`/`M3-v1`) e o reengajamento (`RE-1`/`QI-1`) são
`Marketing` de alta confiança. O caso mais incerto é `NS-1`: atualiza uma
reunião que já existe (argumento a favor de `Utility`) mas convida
ativamente a remarcar com link (argumento a favor de `Marketing`) —
nenhuma fonte desta pesquisa resolveu um formato assim com segurança,
registrado como incerto em vez de forçar uma resposta. Tabela completa,
por código, em `build-wesales.md`, seção 2.61 — reaproveitada como coluna
nova na própria tabela "Template Meta" do G-05 em
`biblioteca-mensagens.md`. Estende a rotina manual do F-07 (três momentos
de checar `Settings → WhatsApp → Manage`) com um quarto hábito: na tela
nativa de Estatísticas por ação `Send WhatsApp` de cada workflow (`Sent`/
`Pending`/`Delivered`/`Read`/`Failed`, GHL), separar `Failed` por queda de
reputação (F-07) de `Failed` por teto de frequência do destinatário (esta
seção) — o segundo é esperado e dinâmico em código `Marketing`, não é
sintoma de nada quebrado.

**Pronto quando (cumprido):** os 16 códigos têm categoria candidata e
razão registradas; quem submeter no Meta Business Manager sabe que a
categoria pode ser reclassificada depois e sabe distinguir, na tela de
Estatísticas do WhatsApp, os dois motivos de `Failed`. Zero campo, zero
tag, zero workflow, zero escrita no CRM — item de documentação pura,
mesmo padrão do F-07/F-08: não depende de `APROVADO.md` (a submissão já
era ação do dono desde o G-05; esta seção só diz qual categoria escolher).
F-09, F-10, G-11 (item 1), G-19, G-27/G-29 e G-31 continuam sendo as
decisões sem prazo fixo que esperam o dono, sem mudança nesta rodada.

---

### G-37 · Sete cabeçalhos de item fechado (F-18 a F-26) nunca ganharam a marca `FEITO` que o próprio parágrafo de fechamento, no fim desta seção, já dava por certa (28/09/2026) — **FEITO em 28/09/2026 (coerência da própria seção "Bloco 6")**

**Por quê:** reconciliação de sempre antes de pegar o item de maior
prioridade da fila (instrução da tarefa desta sessão) — `git fetch` nas
duas branches irmãs sem commit novo além do que o F-31 já tinha lido; CRM
reconfirmado por API sem mudança (64 oportunidades, mesma composição; 60
campos de contato, sem novidade). Antes de desenhar algo novo, a sessão
tentou responder "qual é o item de maior prioridade ainda aberto?" com o
método mais barato: `grep -n "^### [FGR]-[0-9]" ROADMAP-SALES-ENGAGEMENT.md`
— o mesmo comando que resolveu essa pergunta em rodadas anteriores. Sete
cabeçalhos vieram **sem** a marca `FEITO`: F-18, F-19, F-20, F-21, F-24,
F-25 e F-26 — pareciam sete itens abertos, alguns deles (F-19 a F-21) do
bloco mais antigo do roadmap ainda sem trabalho.

**Não eram.** Cada um dos sete já tem parágrafo de fechamento no fim desta
seção ("Fechado como F-19", "F-24 aberto e fechado em 28/09/2026" etc.) e
está referenciado, coerente, em `build-wesales.md` (seções 2.47 a 2.56 e a
seção 4), `campos-e-tags.md` (T-23 a T-26, C-33 a C-36),
`IMPLEMENTACAO-WORKFLOWS.md` (W25 a W30) e `GUIA-MONTAGEM.md` (fila de
montagem manual) — conferido linha a linha nesta sessão, não só por grep de
nome. F-18 é o único caso genuinamente diferente dos outros seis: o texto
desta própria seção (parágrafo de 27/09/2026, logo depois do alerta de
integridade) já registrava "F-18 se soma à lista dos itens que esperam
evento real... porque o primeiro `won` desta operação ainda não aconteceu"
— então **não** leva `FEITO`, leva o mesmo formato que o `R-14` já usa
("especificação fechada em ..., execução aguarda ..."), para não afirmar
uma entrega que o próprio texto já nega.

**Causa provável, mesma classe do G-24/G-36:** os seis primeiros nasceram
em três rodadas diferentes (F-19/F-20/F-21 em 27/09; F-24/F-25/F-26 em
28/09) que escreveram o parágrafo de fechamento no fim da seção — a
obrigação que o G-24 criou — mas nenhuma delas voltou ao próprio `###
cabeçalho` do item, lá no corpo do Bloco 6, para acrescentar a mesma marca
que F-07/F-22/F-23/F-27/F-29/F-30/F-31 carregam. O F-18 já tinha o motivo
registrado por escrito; os outros seis não tinham motivo nenhum — só
faltou o passo mecânico. G-24 e G-36 corrigiram o parágrafo de fechamento
em si (existir ou não); este item corrige o outro lado do mesmo par, o
cabeçalho que ele fecha.

**Como:** `### F-18` recebeu "especificação fechada em 27/09/2026, execução
aguarda o primeiro `won`"; `### F-19`, `F-20`, `F-21` receberam "FEITO em
27/09/2026 (especificação)"; `### F-24`, `F-25`, `F-26` receberam "FEITO
em 28/09/2026 (especificação)" — mesma data que o parágrafo de fechamento
de cada um já registra. Nenhum texto de corpo mudou, só o cabeçalho.

**Regra nova para a próxima rodada, ao lado da que o G-24/G-36 já deixaram:**
o parágrafo de fechamento no fim da "Ordem sugerida" e a marca `FEITO` no
`### cabeçalho` do item são **as duas metades da mesma entrega** — fechar
um sem o outro é o mesmo tipo de item pela metade que a introdução deste
roadmap pede para nunca deixar. `grep -n "^### [FGR]-[0-9]"` sem `FEITO`
nem "aguarda"/"especificação fechada" na mesma linha é o comando que
verifica as duas de uma vez.

**Zero campo, zero tag, zero escrita no CRM: item de coerência dentro do
próprio roadmap, não depende de `APROVADO.md`.**

**Pronto quando:** feito — este `### G-37` e os sete cabeçalhos corrigidos
acima são o próprio "Pronto quando", mesmo padrão que já valia para o
G-24/G-36.

F-09, F-10, G-11 (item 1), G-19, G-27/G-29 e G-31 continuam sendo as
decisões sem prazo fixo que esperam o dono, sem mudança nesta rodada.

---

### F-32 · O F-02 espera conexão real para aprender horário por segmento, mas o próprio `Segmento` nunca teve como nascer preenchido — a campanha já carrega o nicho no nome, e nada lê isso (28/09/2026) — **FEITO em 28/09/2026 (especificação)**

**Por quê:** os seis itens de prazo fixo (F-09, F-10, G-11, G-19, G-27/G-29,
G-31) seguem sem novidade — `git fetch` nas duas branches irmãs não achou
resposta nova, e a reconciliação de sempre (`opportunities_search-
opportunity`/`locations_get-custom-fields`, direto por API nesta sessão,
sem `GHL_TOKEN` neste ambiente, mesmo caminho do F-28) confirma **66
oportunidades** (subiu de 64 — 2 leads novos de verdade entraram durante
esta própria sessão, incluindo `Daniele` às 12:05:29 UTC) e os mesmos 60
campos de contato, sem campo órfão novo além dos já registrados (`B ·
Quanto pode investir`, `SDR responsável`). Sem achado de reconciliação, a
sessão foi ler o próprio F-02 antes de ir à pesquisa de concorrência de
sempre — ele nunca fechou por inteiro: o "Como" promete gravar `Hora da
conexão` e cruzar com `Segmento` assim que houver conexão real, mas o
mecanismo (`If/Else` por segmento, seção 2.18) ficou explicitamente
represado esperando volume. Antes de aceitar "falta volume" como a causa
completa, a sessão conferiu **por dado, não por suposição**, se o outro
lado da conta — `Segmento` chegar preenchido — de fato acontece: **17
contatos reais** (amostra de leads com `source: Facebook`, excluindo os de
teste, cobrindo entradas de 19/09 a 28/09) lidos via `contacts_get-contact`
nesta sessão, **0 com `Segmento` preenchido**. O próprio
`script-de-ligacao.md` (seção 1) diz "Confira `Segmento`... normalmente já
vêm preenchidos da origem do lead" — a frase nunca tinha sido checada
contra a subconta real, e não se confirma: nenhum dos 8 formulários do
Meta que o G-04 já mapeou grava em `Segmento`, e a `Porta de Entrada` (seção
1.3) de propósito não faz nada além de criar a oportunidade.

**A lacuna nova, achada olhando o dado que a API já trazia para outro fim:**
`attributionSource`/`lastAttributionSource` de cada contato carrega
`utmMedium` — e para as campanhas mais novas ("Fase 3"), esse texto já
**nomeia o nicho da campanha**, lido ao vivo nesta sessão: `Ricardo` e
`Andreia` — "LEADS I NICHO ADVOCACIA BR I FASE 3"; `Ana Ruth` — "LEADS I
NICHO CONTABILIDADE BR I FASE 3" (aqui o rótulo da campanha diverge do
negócio real dela, "Especialista em Cabelos" — registrado abaixo como
limite, não escondido). Campanhas mais antigas ou de segmentação ampla
trazem `utmMedium` genérico ("LEADS I INTERESSE BR I FASE 3", "LEADS I
PERSONALIZADO CNAE BR I FASE 3", ou simplesmente `"social"` nas primeiras
campanhas, sem nicho) — não haveria nicho para extrair mesmo se alguém
lesse o campo. Nenhum documento deste projeto cita `utmMedium` ou "NICHO"
antes desta sessão (`grep -rn "utmMedium\|NICHO" wesales/*.md`, vazio).

**Por que isto é mais barato que esperar o SDR perguntar (a saída que
`script-de-ligacao.md` já previa para quando o campo vem vazio) e mais
barato que qualquer coisa que Reev/Meetime/Outreach/Salesloft oferecem:**
as quatro plataformas de referência não têm como ler a campanha de anúncio
de terceiro — quem compra mídia paga é o próprio dono, e o nicho já está
escrito no nome da campanha que ele mesmo criou, de graça, antes de
qualquer ligação acontecer. Aproveitar isso fecha `Segmento` no instante em
que o lead entra na cadência, não depois da Nª conexão — a metade do F-02
que dependia de volume continua dependendo (a hora da conexão só existe
depois de atender), mas a metade do segmento deixa de depender de nada.

**Pesquisado antes de desenhar (`WebSearch`, confiança média — igual
ressalva do F-06/F-08/F-29/F-30: `gohighlevel.com` bloqueado pelo proxy
deste contêiner, três buscas independentes convergindo em fontes de
terceiro e num changelog oficial indexado):** o `If/Else` nativo do GHL
aceita UTM Source/Medium/Campaign/Term/Content/Referrer tanto de "First"
quanto de "Latest Attribution" como campo de condição, com operador
`Contains`/`Doesn't Contain` — o changelog oficial cita explicitamente uma
correção de bug em "if/else branching for UTM Campaign (Last
Attribution)", prova de que o campo existe como condição de verdade, não
só como merge field de texto. **Não confirmado ao vivo nesta subconta:** o
nome exato do campo como aparece no seletor da tela (a busca não decidiu
entre "UTM Medium (First Attribution)" batendo exatamente esse rótulo ou
uma variação) — conferir na montagem manual antes de publicar, mesma
disciplina do F-06 com o Voice Intelligence.

**Como — nó novo 0.8/0.8b dentro do nó de inicialização já existente da
`Cadência 12x30` (seção 2.3, `build-wesales.md`), não um workflow
separado:** é o mesmo lugar que a seção 2.3 já reserva para "qualquer coisa
a mais" que a Porta de Entrada de propósito não faz. Detalhe nó a nó,
lista de nichos conhecidos e os dois limites (campanha ampla não tem nicho
para extrair; rótulo da campanha é candidato, não verdade — o SDR
confirma e corrige na ligação, o campo continua editável) na seção **2.62**
do `build-wesales.md`.

**Zero campo novo, zero tag nova:** reaproveita `Segmento` (Q-01), que já
existe na tela desde 18/09/2026. Não depende de `APROVADO.md`. `campos-e-
tags.md` (Q-01) e `script-de-ligacao.md` (seção 1, a frase que a auditoria
mostrou incompleta) atualizados no mesmo commit; `IMPLEMENTACAO-
WORKFLOWS.md` (W11, nó 0) e `GUIA-MONTAGEM.md` também.

**Pronto quando:** os nós 0.8/0.8b estiverem montados na tela dentro da
`Cadência 12x30` já publicada (430 nós, `GUIA-MONTAGEM.md`); um lead novo
de campanha com "NICHO" no `utmMedium` entrar em `CONECTAR` com `Segmento`
já preenchido, sem o SDR perguntar; e, só então, o próprio F-02 (o
`If/Else` por horário da seção 2.18) deixar de esperar só volume — passa a
esperar volume **e** ter segmento para cruzar, que agora nasce no dia 1 em
vez de nunca.

F-09, F-10, G-11 (item 1), G-19, G-27/G-29 e G-31 continuam sendo as
decisões sem prazo fixo que esperam o dono, sem mudança nesta rodada.

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

**F-11 aberto e fechado em 22/09/2026, sessão automática seguinte — lacuna
nova, achada seguindo a mesma instrução de sempre.** Sweep de coerência
limpo (zero nome de etapa órfão, zero merge field órfão — os 36 merge
fields usados no documento batem 1:1 contra os `fieldKey` reais dos 51
campos; Composio/HighLevel reconferido, ainda 0 contas ativas) e CRM
reconfirmado sem mudança via API (51 campos, 50 oportunidades — 47
`NOVO LEAD` + 2 `NEGOCIAR` + 1 `lost` de teste; lead mais novo ainda
`Carlos Andrade`, 21/09 09:17, entrada agora com quase 26h de silêncio) —
nada para corrigir nem para reler premissa vencida. A lacuna veio de ler
os dados de contato (não só o texto) atrás de outra coisa (reconferir o
G-04) e notar, no meio do caminho, que um contato pode ter oportunidade
`abandoned`/`lost` e mesmo assim reenviar o mesmo formulário pago do Meta
sem que nada no projeto reaja — nem a Porta de Entrada (que só dispara uma
vez por contato), nem o Reengajamento 90 dias (que só reage a quem saiu
por `nutricao-90d`, e só depois de 90 dias). Workflow novo especificado
(`build-wesales.md`, seção 1.4; `IMPLEMENTACAO-WORKFLOWS.md`, W21),
interação com o R-08 verificada contra o portão real dele, não suposta.
Zero campo, zero tag novos, zero escrita no CRM: item de especificação
pura, não depende de `APROVADO.md`. Pendência explícita registrada no
próprio item: não confirmado se o gatilho `Facebook Lead Form Submitted`
aceita "todos os formulários" de uma vez.

Com isso, nenhum item numerado (G/R/F) resta sem especificação nem sem
dono claro: G-03, G-04, F-09 e F-10 esperam decisão do dono; R-14 tem
desenho completo e espera a operação mandar a primeira mensagem real para
executar o que já está pronto na documentação; F-11 tem desenho completo
e não depende de nada — só falta ser montado na tela, mesma fila manual
dos demais workflows ainda não publicados.

**F-12 aberto e fechado em 22/09/2026, sessão automática seguinte — lacuna
nova, achada seguindo a mesma instrução de sempre (procurar o que a
concorrência reporta e este projeto ainda não).** CRM reconfirmado via API
sem mudança de estrutura (51 campos, mesmas 5 etapas do `FUNIL DE VENDAS`)
— a única variação real é de dado, não de desenho: 50 oportunidades seguem
(46 `NOVO LEAD`, 1 `CONECTAR`, 3 `NEGOCIAR`, 1 `lost` de teste — uma
oportunidade avançou de `NOVO LEAD` para `CONECTAR` e outra para `NEGOCIAR`
por fora desta sessão desde a última leitura, G-03/G-04 seguem sem decisão
do dono) — sweep de coerência de sempre limpo (grep por nome de etapa
antigo e pelos merge fields tocados nesta rodada não achou nada órfão). A
lacuna veio de perguntar, pela primeira vez neste projeto, "o que Reev,
Meetime, Outreach e Salesloft reportam sobre motivo de perda, e o que este
projeto nunca respondeu": `Motivo da desqualificação` (C-16) é preenchido
desde 18/09 e nunca teve como agregar — o próprio Dashboard (R-15) já tinha
documentado a razão técnica em 18/09/2026 sem nunca virar item de roadmap
próprio. A resposta não exigiu campo novo nem redesenho: o GHL já tem um
`Lost Reason` nativo em nível de oportunidade, com relatório e filtro de
gatilho de graça — o projeto só nunca tinha olhado para lá. Espelhar C-16
nele, só nos dois nós que já marcam `lost` (D6 do Pós-ligação, nó 4 do Loop
do closer), fecha o item sem tocar em nada que já funciona. Zero campo,
zero tag novos, zero escrita no CRM: item de especificação pura, não
depende de `APROVADO.md` — nem `Lost Reason` sai por API neste conector,
nem a configuração dos 5 valores nativos, mesma classe de trabalho manual
de sempre. Pendência explícita registrada no próprio item: não confirmado
se o seletor de `Lost Reason` na ação `Update Opportunity` aceita valor
dinâmico (colapsaria o desenho para um nó só) ou só fixo por ramo (o que o
desenho assume).

Com isso, nenhum item numerado (G/R/F) resta sem especificação nem sem
dono claro: G-03, G-04, F-09 e F-10 esperam decisão do dono; R-14 tem
desenho completo e espera a operação mandar a primeira mensagem real para
executar o que já está pronto na documentação; F-11 e F-12 têm desenho
completo e não dependem de nada além de serem montados na tela, mesma fila
manual dos demais workflows ainda não publicados.

**Sessão automática seguinte, 22/09/2026 — sem item numerado novo; fechada a
pendência que a conferência de `3fb9b20` deixou em aberto.** CRM reconfirmado
sem mudança via API (51 campos, 50 oportunidades — `Carlos Andrade` segue o
lead mais novo, entrada real ainda parada). Nenhum G/R/F está livre para
avançar (todos aguardam o dono ou volume real, listados acima) — seguindo a
própria instrução desta seção, o passo era reler o "por quê estamos
esperando" do que ficou represado na última rodada, não inventar item novo.
A ressalva sobre ordenação de dois níveis em sete Smart Lists (8.1, 8.2, 8.3,
8.4, 8.16, 8.18, 8.19), levantada pela conferência anterior sem resposta,
foi de fato testada — três caminhos de pesquisa diferentes (`WebFetch` direto
nas páginas oficiais, bloqueado pelo proxy deste ambiente como já era o caso
do G-05; `WebSearch` por vários ângulos; a documentação da API oficial, que
confirma um array de ordenação multi-campo no endpoint `Search Contacts`, mas
não resolve o que o construtor visual da Smart List expõe). Nenhum fechou a
dúvida — a resposta só existe na tela. Em vez de deixar o achado boiando como
nota de rodapé, virou passo acionável: `GUIA-MONTAGEM.md`, Fase 6, ganhou a
instrução de testar as sete listas na hora de montar e aplicar o Plano B (já
escrito em `build-wesales.md`, seção 8.4) se a tela recusar o segundo nível.
Detalhe completo, e por que uma quarta rodada de pesquisa não vale a pena
agora, em `APRENDIZADOS-CRM.md`. Zero campo, zero tag, zero escrita no CRM:
item de documentação pura, não depende de `APROVADO.md`.

**F-13 aberto e fechado em 22/09/2026, sessão automática seguinte — lacuna
nova, achada relendo o próprio `build-wesales.md` em vez de procurar fora.**
CRM reconfirmado sem mudança via API (51 campos, 50 oportunidades — 47
`NOVO LEAD` `open` + 2 `NEGOCIAR` `open` + 1 `NEGOCIAR` `lost` + 2
`CONECTAR` `lost` de teste; entrada segue sem lead novo desde 21/09 09:17,
F-10 sem novidade; G-03/G-04/F-09/F-10 seguem aguardando o dono) — nada para
o sweep de coerência de sempre corrigir a partir daí. A lacuna veio de
reler a seção 1.1 (as cinco etapas do funil, cada uma com sua linha "Tempo
de estagnação") depois de notar que o F-05 fechou citando "seis peças" sem
nunca explicar por que a nota da Etapa 3 (`NEGOCIAR`) sobre "a metade
negociação não tem monitor ainda" nunca tinha virado uma sétima peça. Não
tinha virado porque ninguém tinha voltado a ler aquela nota depois de
escrevê-la — o
mesmo padrão de "achado registrado como rodapé, nunca promovido a item" que
já se repetiu neste documento (F-12 veio do mesmo tipo de releitura, sobre
`Motivo da desqualificação`). Fechado como F-13: workflow "Negociação
Estagnada", tag nova `negociacao-estagnada` (21ª, T-21) e Smart List
`Saúde — Negociação Estagnada` (seção 8.28) — mesmo padrão das seis peças do
F-05, com prazo de 3 dias em vez de 24h porque quem decide aqui é o closer,
não o SDR. Corrigida também, na mesma leitura, a nota irmã da Etapa 2
(`AGENDAR`): dizia "sem monitor ainda" apesar de a peça 5 do F-05 já cobrir
esse gap desde 21/09/2026 — texto nunca atualizado quando a peça fechou.
Zero escrita no CRM: item de especificação pura, a tag nasce `[ ]` em
`APROVADO.md`, mesma regra das cinco tags do F-05 que ainda esperam
aprovação do dono. Detalhe completo no próprio F-13, acima.

**F-14 aberto e fechado em 22/09/2026, sessão automática seguinte — lacuna
nova, achada comparando o F-08 com o vizinho que ele mesmo cita, o F-07.**
CRM reconfirmado por API (51 campos, 50 oportunidades — 45 `NOVO LEAD`
`open` + 2 `NEGOCIAR` `open` + 1 `NEGOCIAR` `lost` + 2 `CONECTAR` `lost` de
teste, a mesma leitura corrigiu uma soma que a entrada do F-13 tinha errado
em 2 — 47+2+1+2 não batia com o total de 50 já escrito na mesma frase;
`grep` confirma que a soma antiga só aparecia naquela linha, sem se
propagar; entrada segue sem lead novo desde 21/09 09:17, agora ~30h47min —
G-03/G-04/F-09/F-10 seguem aguardando o dono) — o achado do dia não veio do
sweep de coerência, veio de perguntar "os dois itens de proteção de número
que fecharam ontem se tratam com a mesma régua?" O F-07 (WhatsApp) tem Tier
de número novo com ramp de 7 dias, objeto próprio da Meta; o F-08 (telefone)
só disse "distribua entre números antes de escalar", sem cronograma — mesmo
canal com o dobro dos toques (8 de 12) e já acima da referência
internacional de segurança na meta de regime. Fechado como F-14: rampa de 4
semanas (`build-wesales.md`, seção 2.29), pesquisada contra fontes de
mercado de discador (Kixie, Tendril, Salesloft, Aircall, Outreach — o
"Voice Integrity" do Outreach tem o mesmo limite US-only que já descartara o
da HighLevel, confirmando que o limite é do recurso, não da plataforma), e
cruzada com o G-03: o mesmo lote de 10-13 leads/dia que protege o Quality
Rating do WhatsApp também governa o volume de telefone do dia 1 — dentro da
faixa segura sozinho, até a segunda semana, quando os lotes se empilham com
as reentradas D2/D4/D7 sem teto nenhum. Zero campo, zero tag, zero
workflow, zero escrita no CRM: item de documentação e rotina manual pura,
mesmo tratamento do F-07/F-08, não depende de `APROVADO.md`. Detalhe
completo no próprio F-14, acima.

Com isso, nenhum item numerado (G/R/F) resta sem especificação nem sem dono
claro: G-03, G-04, F-09 e F-10 esperam decisão do dono; R-14 tem desenho
completo e espera a operação mandar a primeira mensagem real para executar
o que já está pronto na documentação; F-11, F-12 e F-13 têm desenho
completo e não dependem de nada além de serem montados na tela; F-14 é
checklist de gestor, já pronto para uso assim que o número começar a discar
de verdade.

**G-04, sessão automática seguinte, 22/09/2026 — não é item novo, é a
mesma instrução de sempre (reler o "por quê estamos esperando" de todo item
represado) aplicada a um item que ninguém tinha relido desde 21/09.** Entre
esta rodada e a anterior, o dono montou 20 workflows no CRM pelo caminho que
só o PC dele alcança (API interna, `wesales/tools/`) — fora do que esta
sessão na nuvem consegue ver em tempo real, porque a API pública (MCP) não
tem endpoint de workflow (`APRENDIZADOS-CRM.md`, "os 22 arquivos de
`workflows-json/` não dizem o que está no ar"). Um desses commits
(`dec3a20`) resolveu a metade `Prazo`/`Urgência` do G-04 sem esperar a
decisão A/B que este roadmap ainda apresentava como bloqueio único — e o
roadmap, `build-wesales.md` (seção 9.1) e `campos-e-tags.md` continuaram
descrevendo o item inteiro como travado, o que já não era verdade para essa
metade. **Achado por releitura de documento contra `GUIA-MONTAGEM.md`
("Estado final em 22/09/2026"), não por nova pesquisa nem por escrita no
CRM.** Corrigidos os três: a seção 9.1 do `build-wesales.md` (Bloco B), a
entrada do G-04 aqui (que ganhou "Resumo" e "Pronto quando" revisados) e o
item 2 da lista aberta de `campos-e-tags.md`. O que sobrou, de verdade, é só
a linha `Investimento mensal em anúncios` — decisão do dono entre Opção A e
Opção B, sem mudança desde 21/09. Zero campo, zero tag, zero escrita no
CRM: item de documentação pura, não depende de `APROVADO.md`. **Regra
prática, generalizável:** quando parte do trabalho de um item acontece fora
desta sessão (o PC do dono, neste projeto), reler o item antes de assumir
que ele segue do tamanho que tinha na última rodada — o mesmo raciocínio já
valeu para "premissa técnica represada" (F-05, F-06), agora vale também
para "decisão do dono represada", que pode ter sido parcialmente resolvida
por um caminho que não passou pela decisão em si.

**Sessão automática seguinte, 22/09/2026 — sem item numerado novo; corrigido
um merge field órfão achado pela varredura de coerência de sempre, o único
tipo de trabalho que sobrava para uma sessão sem tela e sem G-03/G-04/F-09/
F-10/R-14 desbloqueados.** CRM reconfirmado por API: 55 campos (sem mudança
desde a rodada anterior), pipeline com as mesmas 5 etapas, 50 oportunidades
(45 `NOVO LEAD` `open` + 2 `NEGOCIAR` `open` + 1 `NEGOCIAR` `lost` + 2
`CONECTAR` `lost` de teste — a soma agora bate exata com o total, a mesma
correção que o F-14 já tinha feito para a frase deste roadmap se propagou
sozinha para o dado real), 50 contatos, `Carlos Andrade` (21/09 09:17)
ainda o lead mais novo — entrada segue parada, F-10 sem novidade. O achado
não veio de nome de etapa nem de `fieldKey`: veio de reler, campo por campo,
se cada um dos 55 ainda tinha o mesmo "quem escreve" que `campos-e-tags.md`
promete — `Data e hora do sinal` (C-14) prometia `Workflow (F-01)` desde o
início, mas `build-wesales.md` (seção 2.9.2) tinha descartado o nó que o
escreve em 19/09/2026, por um limite do **seletor da tela** ao montar ao
vivo naquele dia (não parecia oferecer "data/hora atual" para campo `TEXT`).
`IMPLEMENTACAO-WORKFLOWS.md` já registrava isso ("não usado desde 19/09"),
mas `campos-e-tags.md` nunca soube, e a Smart List `Resposta por Template`
(8.13, "Pronto quando" do R-04 já fechado) tinha — e teria para sempre —
uma coluna vazia sem ninguém notar, porque o workflow não quebra, só um
carimbo nunca aparece. **O que destravou a correção, e não é óbvio:** a
premissa de 19/09 era sobre o *seletor clicável* da tela, e a montagem deste
projeto passou a sair também pela API interna a partir de 21/09/2026 — que
grava o valor direto no payload, sem depender do seletor. Essa mesma API já
tinha provado, rodando de verdade, que `{{right_now}}` escreve num campo
`TEXT` de contato (`Entrada em`, C-18, mesmo tipo de C-14, carimbado ao
promover um lead de teste para `CONECTAR` — `GUIA-MONTAGEM.md`, "Testado de
ponta a ponta"). Ninguém tinha cruzado essa prova com a pendência antiga do
C-14 porque as duas viviam em documentos diferentes. Restaurado o nó 5b em
`build-wesales.md` (seção 2.9.2, herdado por 2.9.3), retoque registrado em
`GUIA-MONTAGEM.md` para os dois workflows já publicados (`Interceptação —
Clique v2`/`— Resposta v2`, 15/18 nós na tela, sobe para 16/19 quando
aplicado), e `IMPLEMENTACAO-WORKFLOWS.md` corrigido para não repetir "não
usado". Zero campo novo (C-14 já existe desde 18/09/2026), zero tag, zero
escrita no CRM: item de documentação e retoque de spec, não depende de
`APROVADO.md`. **Regra prática, generalizável:** uma premissa técnica que
travou uma decisão de montagem não é permanente só porque ninguém a
revisitou — o F-05 e o F-06 já tinham mostrado isso para "esperar volume" e
"esperar recurso nativo"; esta rodada mostra que o mesmo vale para "esperar
um caminho de montagem melhor que o que existia no dia em que a premissa
foi escrita".

**F-09, sessão automática seguinte, 22/09/2026 — correção de premissa
vencida, não item novo.** CRM reconfirmado por API sem mudança (55 campos de
contato, mesmas 5 etapas do `FUNIL DE VENDAS`, 50 oportunidades — 45
`NOVO LEAD` `open` + 2 `NEGOCIAR` `open` + 1 `NEGOCIAR` `lost` + 2
`CONECTAR` `lost` de teste; `Carlos Andrade`, 21/09 09:17, segue o lead mais
novo — entrada ainda parada, sem novidade para F-10). Nenhum G/R/F estava
desbloqueado; a "regra que fica" que `4d5bcf6` deixou registrada
(`APRENDIZADOS-CRM.md`: depois de uma decisão mudar uma premissa numérica,
reabrir todo item com tabela de toques por canal) apontava direto para o
F-09, que tem exatamente esse tipo de tabela e não tinha sido reaberto. Não
era só o número (8 de 12 → 12 de 12, mesmo conserto do F-14): as opções A e
B do F-09 mandavam o telefone "desviar para WhatsApp" ao estourar o
limiar — canal que não aplica mais nenhum toque da régua desde `d52e61d`,
então a opção descrevia um comportamento que o motor publicado não pode
mais produzir. Corrigidas as duas para "encerra a régua mais cedo", a
tabela para 12/12, e fechado um segundo loop que o próprio item deixava
aberto: a pergunta "LC Phone ou linha própria?" já tinha resposta do dono ao
vivo (`APRENDIZADOS-CRM.md`, 16:13 UTC) quase 9h antes desta rodada, e o
F-09 ainda dizia "pergunta para o dono, ninguém deve procurar mais". Espelho
da mesma correção aplicado à autorização pendente em `APROVADO.md` (campo
`Tel não atendidas seguidas`), que citava o mesmo número vencido. As opções
A/B/C continuam decisão do dono — nada disso executa sozinho. Zero campo,
zero tag, zero escrita no CRM: item de documentação pura, não depende de
`APROVADO.md`. Detalhe completo no próprio F-09, acima, e em
`APRENDIZADOS-CRM.md`. **Regra prática, refinando a de `4d5bcf6`:** ao
aplicar "reabrir item com tabela de toques por canal", filtrar por "o item
ainda está aberto?" primeiro — um item fechado (F-07, F-08) só documenta o
que já foi decidido, e reescrevê-lo não muda decisão nenhuma; um item aberto
(F-09) alimenta uma decisão que falta tomar, e um número ou uma opção
vencida nele pode levar o dono a escolher algo que a régua publicada não
sabe mais fazer.

Com isso, nenhum item numerado (G/R/F) resta sem especificação nem sem dono
claro: G-03, G-04 (peça 2), F-09 e F-10 esperam decisão do dono; R-14 tem
desenho completo e espera a operação mandar a primeira mensagem real; F-11,
F-12 e F-13 têm desenho completo e só faltam ser montados na tela; F-14 é
checklist de gestor, pronto para uso assim que o número começar a discar de
verdade.

**F-15 aberto e fechado (especificação) em 22/09/2026, sessão automática
seguinte — lacuna nova, achada lendo `ESTADO-E-PLANO.md` (novo documento,
commit `cdaef2d`, fora da lista de leitura padrão deste projeto — corrigido
no `README.md` nesta mesma rodada) em vez de repetir o próprio roadmap.**
Antes de desenhar, duas pistas já registradas em documentos vizinhos
evitaram trabalho duplicado: `CONFERENCIA-CAMPOS.md`, Tabela L, já tinha
medido `country`/`timezone` como não-problema agora (Number Validation
fora por decisão do dono; fuso do contato nunca é lido por nenhum nó) —
por isso este item **não** virou também um item extra sobre país/fuso, que
seria investigar de novo o que a Tabela L já fechou (o número G-07 citado
naquele dia nunca chegou a existir para este assunto — quem usa esse
número hoje é outro item, sobre compliance de e-mail, aberto em
22/09/2026, mais abaixo nesta seção). A lacuna real veio de
cruzar dois fatos que nenhum documento tinha juntado: o portão 0.0/0.0b já
existe desde a Etapa 1, e o Reengajamento 90 dias (R-08) recicla todo
`nutricao-90d` sem checar se a causa foi "sem telefone" — as duas peças
são antigas, o encontro delas é que é novo. CRM reconfirmado por
`ESTADO-E-PLANO.md` na mesma rodada em que este item nasceu (50 contatos,
50 oportunidades, 9 sem telefone, 39 com e-mail) — G-03/G-04/F-09/F-10
seguem aguardando o dono, sem novidade. Detalhe completo no próprio F-15,
acima.

Com isso, nenhum item numerado (G/R/F) resta sem especificação nem sem dono
claro: G-03, G-04 (peça 2), F-09 e F-10 esperam decisão do dono; R-14 tem
desenho completo e espera a operação mandar a primeira mensagem real; F-11,
F-12, F-13 e F-15 têm desenho completo e só faltam ser montados na tela
(F-15 também precisa dos dois templates de e-mail, `[ ]` em `APROVADO.md`);
F-14 é checklist de gestor, pronto para uso assim que o número começar a
discar de verdade.

**G-07 aberto e fechado em 22/09/2026, sessão automática seguinte — lacuna
nova, achada relendo o R-17 logo depois de reler o F-15, no mesmo dia em
que os dois foram escritos.** CRM reconfirmado sem mudança via API (55
campos, 50 oportunidades, 50 contatos, zero mensagem de cadência
automática real — G-03/G-04/F-09/F-10 seguem aguardando o dono, sem
novidade) — nada para o sweep de coerência de sempre corrigir a partir
daí. A lacuna não veio de nome de etapa nem de `fieldKey` órfão: veio de
perguntar, pela primeira vez, se as duas proteções que o projeto já tinha
para "resposta de texto pode ser opt-out disfarçado" (R-17) e "quem está
protegido em cada canal" (R-14, Smart Lists 8.26/8.27) tinham acompanhado
o canal que nasceu por último, e-mail (F-15) — nenhuma das duas tinha,
porque as duas foram escritas antes de o e-mail existir como canal real
neste projeto, ambas no mesmo dia 22/09/2026, só mais cedo. É o mesmo
padrão que o G-06 já registrou para a Qualificação por IA no WhatsApp
("a guarda de um item mais velho nunca alcançou o canal mais novo"),
agora achado numa dobradinha de dois itens em vez de um. Fechado como
G-07: workflow novo `Opt-out por Palavra-chave — E-mail`
(`build-wesales.md`, seção 2.9.6, espelhando o 2.9.5/R-17 sem reabrir a
lista de frases), as duas Smart Lists do R-14 ganharam a cláusula `Email
DND`, e a seção 2.30 ganhou um checklist de reputação/compliance do
canal e-mail (SPF/DKIM/DMARC, preservar o link de descadastro nativo do
GHL ao criar o template por API) — o mesmo tipo de checklist que o F-07/
F-08 já usam para os outros dois canais, e que o e-mail nunca tinha
ganhado por ser o mais novo dos três. Zero campo, zero tag novos, zero
escrita no CRM: item de especificação pura, não depende de `APROVADO.md`.
Detalhe completo no próprio G-07, acima.

Com isso, nenhum item numerado (G/R/F) resta sem especificação nem sem dono
claro: G-03, G-04 (peça 2), F-09 e F-10 esperam decisão do dono; R-14 tem
desenho completo e espera a operação mandar a primeira mensagem real; F-11,
F-12, F-13, F-15 e G-07 têm desenho completo e só faltam ser montados na
tela (F-15 também precisa dos dois templates de e-mail, `[ ]` em
`APROVADO.md`); F-14 é checklist de gestor, pronto para uso assim que o
número começar a discar de verdade.

**G-08 aberto e fechado em 22/09/2026, sessão automática seguinte — lacuna
não é nova, é um achado do próprio F-15 que nunca virou edição no nó que
ele apontava.** CRM reconfirmado por API: 53 oportunidades (48 `NOVO LEAD`
open + 2 `CONECTAR` lost + 2 `NEGOCIAR` open + 1 `NEGOCIAR` lost, **zero**
`abandoned`), 55 campos, 53 contatos — subiu de 50 para 53 contatos e
oportunidades desde a última leitura: os 3 novos vieram da integração de
WhatsApp não oficial que o dono conectou nesta mesma sessão (`stevo`/QR,
`APRENDIZADOS-CRM.md`), mensagens de teste do próprio dono ("fds", "me diz
o nome do seu crm"), não lead real — a Porta de Entrada (G-01) os pegou e
criou oportunidade em `NOVO LEAD` sozinha, confirmando que o portão
"qualquer origem" continua funcionando até para um canal que não existia
quando foi desenhado. Sweep de coerência: nenhum nome de etapa órfão novo;
o achado veio de reler o texto do F-15 (seção 2.30) depois de fechá-lo e
notar que o item 1 da lista "o que fica valendo" ("fechar o ciclo") descrevia
uma mudança de nó que o resto daquela mesma sessão nunca aplicou — o F-15
fechou os nós do workflow de e-mail que inventou, mas não voltou ao nó do
R-08 que sua própria análise mandava corrigir. Antes de escrever, reconferi
que o ciclo é uma armadilha futura, não um estrago já rodando: zero
oportunidade `abandoned` na base agora, porque G-03 (promoção `NOVO LEAD` →
`CONECTAR`) segue represada e os 5 leads do Instagram sem telefone nunca
chegaram ao portão que os marcaria `telefone-invalido`. Fechado como G-08:
quarta condição no portão do nó 2 do R-08 (`build-wesales.md`, seção 2.12;
`IMPLEMENTACAO-WORKFLOWS.md`, W16) — `tag telefone-invalido ausente` — e,
corrigido junto por estar na mesma linha do nó 3, a documentação do valor de
`Entrada em` (ainda `{{right_now}}`, já era `{{right_now.date}}
{{right_now.time}}` na tela desde o patch cirúrgico do relógio, mesmo dia,
`APRENDIZADOS-CRM.md`). Zero campo, zero tag novos, zero escrita no CRM:
item de especificação pura, não depende de `APROVADO.md`. **Regra prática,
generalizável:** um achado escrito dentro do texto de um item fechado
("o que fica valendo, item 1") não é automaticamente aplicado só por estar
escrito — precisa da mesma verificação de "isto virou mudança de verdade?"
que este roadmap já aplica a premissa técnica represada (F-05, F-06) e a
decisão do dono parcialmente resolvida (G-04); aqui o represado era um
parágrafo de intenção dentro do próprio commit que o registrou. Detalhe
completo no próprio G-08, acima.

Com isso, nenhum item numerado (G/R/F) resta sem especificação nem sem dono
claro: G-03, G-04 (peça 2), F-09 e F-10 esperam decisão do dono; R-14 tem
desenho completo e espera a operação mandar a primeira mensagem real; F-11,
F-12, F-13, F-15, G-07 e G-08 têm desenho completo e só faltam ser montados/
aplicados na tela (F-15 também precisa dos dois templates de e-mail, `[ ]`
em `APROVADO.md`; G-08 é um retoque de uma linha num workflow já publicado);
F-14 é checklist de gestor, pronto para uso assim que o número começar a
discar de verdade.

**G-09 aberto e fechado em 23/09/2026, sessão automática seguinte — lacuna
que já estava meio escrita, em dois documentos diferentes, e nunca tinha
sido cruzada.** CRM reconfirmado por API: 54 oportunidades (49 `NOVO LEAD`
open + 2 `CONECTAR` lost + 2 `NEGOCIAR` open + 1 `NEGOCIAR` lost), 55 campos
— 4 contatos a mais desde a última leitura (F-10/G-08), todos da integração
não-oficial Stevo (QR), confirmando que o canal continua ativo e crescendo,
não foi um teste isolado — G-03/G-04 (peça 2)/F-09/F-10 seguem aguardando o
dono, sem novidade. A lacuna veio de perguntar, pela primeira vez, se o
"WhatsApp" que a Stevo entrega é o mesmo "WhatsApp" que os filtros
`Customer Replied — Canal: WhatsApp` do R-17 e do 2.9.3 foram escritos para
reconhecer — não é: a Stevo entrega como `TYPE_CUSTOM_SMS`, confirmado pela
conversa de um dos 4 contatos novos. Corrigido com filtro aditivo
(WhatsApp **e** SMS) nos dois pontos onde isso já estava especificado, e a
premissa desatualizada da 8.26/8.27 ("esta subconta não tem WhatsApp
integrado") corrigida para refletir a Stevo, sem reabrir a análise daquela
seção. Zero campo, zero tag novos, zero escrita no CRM: item de
especificação pura, não depende de `APROVADO.md`. **Regra prática,
generalizável, e diferente das anteriores:** G-06/G-07 acharam canal novo
que a guarda mais velha nunca tinha visto; aqui o canal já era WhatsApp na
intenção do projeto desde sempre — o que mudou, sem ninguém decidir isso
como projeto, foi o transporte por baixo dele. Um filtro por **nome de
canal** pode estar certo na intenção e errado na prática se a integração que
implementa aquele canal não for o que o nome sugere — vale conferir sempre
que uma integração nova ou não-oficial entrar no meio de um canal que já
tinha proteção escrita. Detalhe completo no próprio G-09, acima.

**G-10 aberto e fechado em 23/09/2026, sessão automática seguinte — a
lacuna não era técnica, era entre sessões.** Todo item numerado (G/R/F)
seguia fechado ou represado por decisão do dono; a varredura de coerência
que a própria seção seguinte deste documento pede (passo 1, antes de
procurar lacuna nova) achou que `wesales/PLANO-MULTICANAL.md` — commitado
pelo dono só 22 minutos depois do G-09 acima — já tinha respondido a
pergunta que o G-09 levantou (reintroduz WhatsApp/Stevo como canal de
propósito) e reformulado etapa e cadência, sem que este roadmap ou
`build-wesales.md` citassem isso em lugar nenhum. Fechado com notas
cruzadas datadas nos quatro documentos afetados, sem reescrever nenhum dos
dois desenhos por inteiro — não era o achado, e é trabalho grande demais
para uma rodada. **Regra prática, diferente de G-06/G-07/G-08/G-09 (todas
sobre um nó ou filtro que não acompanhou algo mais novo):** aqui o que não
acompanhou foi o documento inteiro — quando duas sessões automáticas
diferentes commitam na mesma branch, cada uma seguindo seu próprio fluxo de
leitura, um plano decidido ao vivo pelo dono num commit direto pode ficar
invisível para quem só lê o roadmap principal. Verificar `git log` do
diretório `wesales/` (não só os arquivos já conhecidos) deveria entrar na
varredura de coerência de toda rodada a partir de agora, junto com o grep
de nome de etapa e contagem duplicada. Detalhe completo no próprio G-10 e
em `APRENDIZADOS-CRM.md`.

**G-11 aberto em 23/09/2026, do PC do dono (commit `2d6a778`) — não é lacuna
achada por esta seção, é item que já nasceu com cabeçalho e nunca foi
somado à narrativa daqui, porque as sessões que o escreveram e as que
fecharam G-06 a G-10 rodaram em paralelo.** O commit que abriu G-11 aplicou
ao vivo, na tela, a mudança de etapa `AGENDAR` → `REUNIÃO DE DIAGNÓSTICO`
em 5 workflows e fez `Atendeu` passar a **ficar** em `CONECTAR` — e essa
segunda mudança reativou uma contradição antiga e inofensiva (`conectado-hoje`
prometia ser "do dia" mas nunca tinha removedor) transformando-a em exclusão
permanente das duas filas do SDR. **Zero lead real afetado ainda** (medido em
23/09: `conectado-hoje` em 2 contatos, os dois de teste) — é armadilha, não
incêndio. G-11 tem três itens, nenhum executável por este MCP (edição de
workflow e de lista inteligente não têm ferramenta aqui — é tela ou
`wesales/tools/`): item 1 precisa de **decisão do dono** entre quatro saídas
(recomendação: A); itens 2 e 3 já têm a saída escrita, só falta **execução**
manual. Nesta rodada, o trabalho possível era só de coerência: item 1 é o
mesmo achado que `campos-e-tags.md`, `IMPLEMENTACAO-WORKFLOWS.md`,
`APRENDIZADOS-CRM.md` e `ESTADO-E-PLANO.md` citam como `F-16` (mesmo commit
`2d6a778`, que já escrevia "F-16 / G-11" no assunto) — mas só G-11 tinha
cabeçalho aqui, e nenhum dos quatro documentos linkava de volta para ele.
Corrigida a referência cruzada dentro do próprio G-11 (nota no topo do item,
acima), e a linha desta seção (topo do arquivo) que ainda dizia "G-01 a
G-09... F-01 a F-16" como se cada número tivesse cabeçalho próprio —
generalizada para não fixar contagem que já estava errada (G-10 e G-11
existem, F-16 nunca teve cabeçalho separado), a mesma regra de "número fixo
só na fonte" que este roadmap já aplica a campo e tag. CRM reconfirmado por
API nesta rodada: 55 oportunidades (49 `NOVO LEAD` open + 3 `CONECTAR`
[2 lost + 1 open] + 3 `NEGOCIAR` [2 open + 1 lost]), 56 campos de contato —
`Canal que conectou` (`TxJmoWdkA8rTqC1uEsMW`), o campo do D10 do
`PLANO-MULTICANAL.md`, já existe na tela e está documentado em
`campos-e-tags.md`. Zero campo, zero tag novos por esta sessão, zero escrita
no CRM: item de coerência entre documentos, não depende de `APROVADO.md`.
Com isso, G-11 (item 1) entra na mesma fila de decisão do dono que G-03,
G-04 (peça 2), F-09 e F-10; os itens 2 e 3 entram na mesma fila de execução
manual (tela/`wesales/tools/`) que F-11, F-12, F-13, F-15, G-07 e G-08.

**G-12 aberto e peça 1 fechada em 23/09/2026, sessão automática seguinte —
lacuna não é nova, é o mesmo padrão do G-11 (achado que já estava escrito em
nota, nunca virou item com "pronto quando" próprio).** CRM reconfirmado por
API nesta rodada: 56 oportunidades (49 `NOVO LEAD` open + 1 `CONECTAR` open +
2 `CONECTAR` lost de teste + 3 `NEGOCIAR` [2 open + 1 lost]), 56 campos de
contato, pipeline com a mesma etapa `3d26fcd1-...` agora chamada `REUNIÃO DE
DIAGNÓSTICO` na tela (`dateUpdated` 2026-09-23T00:59Z, sem mudança desde a
leitura do G-11) — G-03, G-04 (peça 2), F-09, F-10 e G-11 (item 1) seguem
aguardando o dono, sem novidade. Nenhum G/R/F estava desbloqueado; seguindo a
própria instrução desta seção (reler o "por quê estamos esperando" antes de
procurar lacuna nova), a releitura caiu sobre a nota de 23/09/2026 dentro da
seção 1 de `build-wesales.md` (a mesma que registrou a segunda renomeação de
etapa) — ela descrevia um trabalho de migração de texto e nunca tinha virado
item com dono e "pronto quando" claros, o mesmo buraco que já tinha sido
achado duas vezes antes neste roadmap (F-12, sobre `Motivo da
desqualificação`; F-13, sobre a Etapa 3 sem monitor). Fechada a peça 1: seção
1 inteira de `build-wesales.md` migrada para `REUNIÃO DE DIAGNÓSTICO`, e a
nota corrigida quanto a `wesales/tools/ghl_api.py` (já tinha as duas chaves,
por fora desta sessão — o aviso dizendo "ainda não foi feita" estava
desatualizado só nessa parte). Zero campo, zero tag, zero escrita no CRM:
item de documentação pura, não depende de `APROVADO.md`. Detalhe completo no
próprio G-12, acima.

**G-12, peça 2, 23/09/2026, sessão automática seguinte — item fechado por
inteiro, mesmo `git log` de `wesales/` confirmando que nenhuma sessão
tocou o roadmap principal entre a peça 1 (`d1b1c04`) e esta leitura.** CRM
reconfirmado por API: 56 oportunidades (49 `NOVO LEAD` open + 1 `CONECTAR`
open + 2 `CONECTAR` lost de teste + 1 `REUNIÃO DE DIAGNÓSTICO` open + 2
`NEGOCIAR` open + 1 `NEGOCIAR` lost), 56 campos de contato, pipeline com a
etapa `3d26fcd1-...` inalterada — G-03,
G-04 (peça 2), F-09, F-10 e G-11 (item 1) seguem aguardando o dono, sem
novidade; a oportunidade nova em `REUNIÃO DE DIAGNÓSTICO` é a primeira
desde a segunda renomeação, sinal de que o teste de tela do dono já passou
por essa etapa com o nome novo. Migradas as 32 ocorrências de `AGENDAR`
como etapa corrente nas seções 2 em diante de `build-wesales.md`, com a
anotação "(antiga `AGENDAR`)" só na primeira citação por seção `##`, como
o "Como" original pedia; conferido que `ROADMAP-SALES-ENGAGEMENT.md` não
precisava da mesma troca — toda ocorrência que resta ali é nota histórica
datada (o nome como era no dia em que o item fechou), a mesma classe que a
tabela de tradução 1.0 do G-02 já tinha o direito de manter sem reescrever.
Corrigido também o aviso do topo deste arquivo e a nota-espelho na seção 1
de `build-wesales.md`, os dois ainda dizendo "resto do documento segue
chamando a etapa de `AGENDAR`". Zero campo, zero tag, zero escrita no CRM:
item de documentação pura, não depende de `APROVADO.md`. Detalhe completo
no próprio G-12, acima.

Com isso, nenhum item numerado (G/R/F) resta sem especificação nem sem dono
claro: G-03, G-04 (peça 2), F-09, F-10 e G-11 (item 1) esperam decisão do
dono; R-14 tem desenho completo e espera a operação mandar a primeira
mensagem real; F-11, F-12, F-13, F-15, G-07, G-08 e G-11 (itens 2 e 3) têm
desenho completo e só faltam ser montados/aplicados na tela; F-14 é
checklist de gestor, pronto para uso assim que o número começar a discar de
verdade; G-12 fechou por inteiro (peças 1 e 2). Não sobra item de
documentação pura óbvio esperando uma sessão sem tela nem volume — a
próxima rodada nessas condições volta à varredura de coerência de sempre e,
se ela não achar nada, a uma lacuna nova.

**G-13 aberto e fechado (especificação) em 23/09/2026, sessão automática
seguinte — a varredura de coerência de sempre achou algo, e não era nome de
etapa.** CRM reconfirmado por API: 56 oportunidades (mesma composição da
leitura anterior, sem oportunidade nova), 56 campos de contato, pipeline com
a mesma etapa `3d26fcd1-...`/`REUNIÃO DE DIAGNÓSTICO` — G-03, G-04 (peça 2),
F-09, F-10 e G-11 (item 1) seguem aguardando o dono, sem novidade. O `grep`
por nome de etapa (o mesmo que fechou G-02/G-12) não achou nada novo; o que
achou foi ler `PLANO-MULTICANAL.md` (D3, E5-E7, E8) lado a lado com
`build-wesales.md` seção 4 e perguntar não "o nome bate?" mas "o
**comportamento** bate com o que está publicado?" — não batia: o ramo
`Atendeu` do Pós-ligação ainda estava especificado como no desenho de
18/09/2026, movendo a oportunidade para a etapa que a D3 tirou dessa função
em 23/09/2026. Efeito em cascata: um workflow inteiro (`AGENDAR
Estagnado`/W17d, seção 2.23, F-05 peça 5) tinha a premissa do próprio
gatilho invalidada e ninguém tinha escrito por quê — o dono já tinha
despublicado o workflow na tela antes de qualquer documento explicar o
motivo. Corrigidas as duas seções de `build-wesales.md`, o W4/W17d/dicionário
de `IMPLEMENTACAO-WORKFLOWS.md`, e avisadas `campos-e-tags.md`/`APROVADO.md`
(T-19) para não aprovar o desenho velho. Zero campo, zero tag novos, zero
escrita no CRM: item de documentação e correção de spec, não depende de
`APROVADO.md`. Detalhe completo no próprio G-13, acima. **Regra prática,
generalizável — diferente de G-02/G-12 (que procuravam nome desatualizado):**
depois de uma decisão do dono mudar o **comportamento** de um nó (não só o
nome de uma etapa), a varredura de coerência precisa perguntar duas coisas
separadas — o nome bate? e o nó ainda faz o que a decisão nova manda? — porque
uma sessão pode responder sim à primeira e não notar que a segunda ainda é
não, exatamente o que aconteceu aqui com o próprio G-12.

Com isso, G-13 fecha por inteiro (especificação); as pendências que ele deixa
registradas (aviso ao gestor equivalente no `Fechar Horário`, se o ramo
`Atendeu` deveria sair da `Cadência 12x30`, e T-19 revisada) entram na mesma
fila de decisão do dono que G-03, G-04 (peça 2), F-09, F-10 e G-11 (item 1) —
nenhuma delas executa sozinha nem por este MCP.

**G-14 aberto e fechado em 23/09/2026, sessão automática seguinte — a
varredura de coerência de sempre, desta vez sobre os próprios G-10/G-13.**
CRM reconfirmado por API: 56 oportunidades (mesma composição do G-13, sem
mudança), 56 campos de contato — G-03, G-04 (peça 2), F-09, F-10 e G-11
(item 1) seguem aguardando o dono, sem novidade. O `grep` por "AGENDAR" de
sempre desta vez não parou em `build-wesales.md`/`IMPLEMENTACAO-
WORKFLOWS.md` (já corrigidos pelo G-13) — foi perguntar "quem mais cita a
etapa antiga ou a rotina antiga, e o G-10/G-13 já cruzaram esse arquivo?"
`GUIA-MONTAGEM.md` nunca tinha sido tocado por nenhum dos dois, apesar de
ser o documento que o próprio `IMPLEMENTACAO-WORKFLOWS.md` define como "o
estado do que já foi montado" — tinha uma recomendação "dá para fazer hoje"
para a tag que o G-13 já invalidou em outro lugar, e o inventário de
workflows ainda listava `AGENDAR Estagnado`/W17d como rascunho, não como
despublicado. Achado mais sério, categoria diferente: `rotina-limpar-
tarefas.md` não cita só o nome errado da etapa — sua filosofia inteira
("concluir, nunca excluir") foi trocada pela decisão mais recente do dono
(D12, "concluir inventa histórico falso"), e colar aquele prompt numa
rotina hoje concluiria por engano a tarefa `[FECHAR HORÁRIO]` de todo lead
atendido. `IMPLEMENTACAO-WORKFLOWS.md` (§3.3, rotina do gestor) apontava
para esse prompt como o mecanismo "a cada hora", quando quem roda de
verdade, a cada 10 min, é a Faxina. E o `README.md` nunca ganhou uma linha
para `PLANO-MULTICANAL.md` desde que ele existe (22/09/2026) — o documento
mais recente do projeto ficava invisível para quem só abrisse o índice.
Fechado com avisos datados (não reescrita completa, mesma régua do G-10) nos
quatro documentos — detalhe completo no próprio G-14, acima. **Regra
prática, generalizável — estende a do G-10 (duas trilhas de execução podem
não se ver) para "coerência já feita":** corrigir um achado em alguns
documentos não garante que todos os que citam o mesmo fato foram
encontrados — vale reabrir a pergunta "quem mais fala disso?" depois de
qualquer G-10/G-12/G-13 fechado, não só uma vez. Zero campo, zero tag, zero
escrita no CRM: item de coerência entre documentos, não depende de
`APROVADO.md`.

Com isso, nenhum item numerado (G/R/F) resta sem especificação nem sem dono
claro: G-03, G-04 (peça 2), F-09, F-10 e G-11 (item 1) esperam decisão do
dono; R-14 tem desenho completo e espera a operação mandar a primeira
mensagem real; F-11, F-12, F-13, F-15, G-07, G-08 e G-11 (itens 2 e 3) têm
desenho completo e só faltam ser montados/aplicados na tela; F-14 é
checklist de gestor, pronto para uso assim que o número começar a discar de
verdade; G-12, G-13 e G-14 fecharam por inteiro. A próxima rodada sem tela
nem decisão desbloqueada repete o mesmo caminho: varredura de coerência
primeiro (agora incluindo `GUIA-MONTAGEM.md`, `rotina-limpar-tarefas.md` e
`README.md` na lista de arquivos a cruzar, não só `build-wesales.md`/
`IMPLEMENTACAO-WORKFLOWS.md`/roadmap), e só depois lacuna nova.

**G-15 aberto e fechado em 23/09/2026, sessão automática seguinte — a
varredura de coerência veio limpa de novo, e a lacuna nova desta vez não
veio de nome de etapa nem de documento esquecido.** CRM reconfirmado por
API: 56 oportunidades (mesma composição da leitura do G-14, sem mudança),
mesmos campos de contato — G-03, G-04 (peça 2), F-09, F-10 e G-11 (item 1)
seguem aguardando o dono, sem novidade. `conversations_search-conversation`
(55 conversas, todas as 55 lidas) mostrou que a Cadência Inbound já está
ativa de verdade (contatos reais com tag `cad-inbound`, mensagem automática
saindo para pelo menos um contato de teste do próprio dono) — mas nenhum
lead **real** recebeu mensagem automática ainda, então R-14 e F-06
continuam corretamente bloqueadas por "aguarda volume real", sem mudança de
status. A leitura desses dados ao vivo (não prevista pela varredura de
sempre) foi o que trouxe a pergunta do G-15: com dois canais de entrada sem
identificador em comum (telefone do Meta Lead Ads, sem telefone/e-mail no
Instagram), o que impede o mesmo lead de virar dois contatos com duas
cadências? Pesquisado antes de desenhar (`WebSearch`, GHL): existe ação
nativa `Merge Contact`, mas o gatilho `Contact Changed` não filtra por
Telefone/E-mail — pedido em aberto da comunidade, sem previsão. Sem gatilho,
sem automação; a solução é ferramenta nativa (Duplicate Management & Merge
Tool, por Nome) mais rotina humana, registrada no próprio G-15 e num passo
novo já escrito em `GUIA-SDR.md`. Zero campo, zero tag, zero escrita no CRM:
item de especificação e achado de limite de plataforma, não depende de
`APROVADO.md`. Detalhe completo no próprio G-15, acima.

Com isso, G-15 fecha por inteiro (especificação); nenhum item numerado
segue sem especificação — G-03, G-04 (peça 2), F-09, F-10 e G-11 (item 1)
continuam sendo as cinco decisões que ainda esperam o dono (ver correção de
23/09/2026 logo abaixo: esta lista tinha perdido F-09 e F-10 por várias
rodadas seguidas). A próxima rodada sem tela nem decisão desbloqueada
repete o mesmo caminho: varredura de coerência primeiro, releitura das
premissas técnicas represadas (mensagem real, volume de ligação, plano com
Custom Metrics, número de WhatsApp para teste, domínio de e-mail
verificado) e só depois lacuna nova — a mesma ordem que este roadmap já
segue desde o G-01.

**Sessão automática seguinte, 23/09/2026 — sem item numerado novo; achado
que estende o F-08 em vez de abrir item próprio.** CRM reconfirmado por API:
56 campos de contato (sem mudança), pipeline com as mesmas 5 etapas, 56
oportunidades (53 `open` + 0 `won` + 3 `lost` + 0 `abandoned`) — mesma
composição da leitura do G-15, G-03/G-04 (peça 2)/F-09/F-10/G-11 (item 1)
seguem sem novidade (a lista de cinco só foi restaurada na correção de
coerência de 23/09/2026 mais abaixo — nesta rodada ela já estava incompleta
sem que ninguém tivesse notado). A varredura de coerência (grep por
`AGENDAR` como etapa corrente em todo `wesales/`) não achou nada novo: toda
ocorrência fora de
`build-wesales.md`/`ROADMAP-SALES-ENGAGEMENT.md` (já migrados pelo G-12) é
nota histórica datada (decisão de 18/09/2026, antes da segunda renomeação)
ou nome próprio já publicado na tela (`AGENDAR Estagnado`), a mesma classe
que este roadmap já decidiu não reescrever. Conferido também, por API, se
os dois achados do G-04 ainda reproduzem em dado real (não só em texto): a
metade `Prazo`/`Urgência` segue certa (contatos do Meta recém-lidos trazem
`Prazo` vazio e `Urgência` = valor de `Prazo`, exatamente como o bloco de
reserva do Pós-agendamento v2 já espera); a metade `Investimento mensal em
anúncios` segue quebrada (`Acima de 10k` válido, mas `Abaixo de 5k` e `Não
invisto nada ainda` — lidos ao vivo em dois leads do Meta desta rodada —
continuam fora das 4 opções da tela) — G-04 (peça 2) segue exatamente onde
estava, sem decisão possível sem o dono.

A lacuna nova veio da pesquisa de concorrência que este roadmap sempre
manda fazer: Outreach/Salesloft/Kixie/Aircall tratam **Local Presence
Dialing** (número de saída com o mesmo DDD do lead, para aumentar taxa de
atendimento) como recurso central — nenhum item deste projeto tinha
verificado se o HighLevel tem o mesmo. Tem, nativo — e `WebSearch` confirma
que é **suportado só para números dos EUA e Canadá**, mesmo formato de
descarte do `Voice Integrity` que já fechou o F-08. O que não tem essa
restrição: o Web App Softphone deixa o usuário escolher manualmente qual
número da subconta discar (dropdown "Calling From") — mesmo custo zero,
mesmos números que o F-08 já recomenda comprar por reputação, só muda
**qual** número o SDR escolhe a cada ligação. Fechado como acréscimo à
tabela do F-08 (`build-wesales.md`, seção 2.26) e instrução nova em
`GUIA-SDR.md`, não como item numerado próprio — não tem "Pronto quando"
distinto do que o F-08 já cumpriu. Zero campo, zero tag, zero escrita no
CRM. Detalhe completo no próprio F-08, acima.

**Sessão automática seguinte, 23/09/2026 — sem item numerado novo; corrigida
uma quebra de coerência dentro do próprio roadmap, achada pela varredura de
sempre olhando para um alvo que ela nunca tinha checado antes: o próprio
arquivo.** CRM reconfirmado por API: 56 oportunidades (49 `NOVO LEAD` `open`
+ 1 `CONECTAR` `open` + 2 `CONECTAR` `lost` + 2 `NEGOCIAR` `open` + 1
`NEGOCIAR` `lost` + 1 `REUNIÃO DE DIAGNÓSTICO` `open` — mesma composição da
última leitura, nenhum lead novo) e 56 campos de contato (sem mudança) —
nada de nome de etapa nem merge field órfão para o sweep de sempre corrigir
a partir daí. O achado desta vez não veio de `grep` por nome antigo: veio de
perguntar, pela primeira vez, "os parágrafos que resumem o estado do roadmap
concordam com as próprias entradas que eles resumem?" — não concordavam. O
"Com isso" que fechou o G-15 e o parágrafo final do documento (a última
rodada, sobre o F-08/Local Presence) listavam só G-03, G-04 (peça 2) e G-11
(item 1) como decisões pendentes do dono, mas as entradas do F-09 ("Pronto
quando: o dono escolher A, B ou C") e do F-10 ("decisão do dono ainda em
aberto", a opção (b) do alarme) nunca fecharam — nenhuma das duas foi
decidida entre a rodada que ainda as listava corretamente (G-14) e a
seguinte (G-15), que as deixou cair da lista sem nenhuma linha explicando
por quê. Mesma classe de erro que o G-10/G-14 já corrigiram entre
documentos diferentes (uma correção feita num lugar não se propaga sozinha
para quem cita o mesmo fato); a novidade é que desta vez o par de documentos
era o roadmap contra ele mesmo — um parágrafo de resumo divergiu da fonte
que deveria resumir, e a rodada seguinte (a extensão do F-08, acima) copiou
a lista errada adiante sem checar a fonte, o mesmo erro sobrevivendo por
duas rodadas antes de alguém notar. Corrigidos os dois — o "Com isso" do
G-15 e a menção dentro da extensão do F-08, acima. Zero campo, zero tag,
zero escrita no CRM: item de coerência entre documentos, não depende de
`APROVADO.md`. **Regra prática,
generalizável:** a varredura de coerência de sempre procura nome de etapa e
merge field órfão em documentos vizinhos; nunca tinha testado se os
parágrafos "Com isso" deste roadmap continuam contendo tudo o que o
parágrafo anterior continha, não só o que mudou nesta rodada — quando um
`G-1x`/`F-1x` fecha e reescreve a lista de pendências, conferir a lista nova
contra a lista anterior item a item, não só contra o achado do dia.

Com isso, nenhum item numerado (G/R/F) muda de estado nesta rodada: G-03,
G-04 (peça 2), F-09, F-10 e G-11 (item 1) são as cinco decisões que esperam
o dono — a próxima rodada sem tela nem decisão desbloqueada repete o mesmo
caminho de sempre.

**G-16 aberto e especificado em 23/09/2026, sessão automática seguinte —
CRM reconfirmado sem mudança nenhuma desde a leitura acima (56 oportunidades
na mesma composição, 56 campos de contato, pipeline com as mesmas 5 etapas):
G-03, G-04 (peça 2), F-09, F-10 e G-11 (item 1) seguem exatamente onde
estavam.** A varredura de coerência desta vez não foi grep por nome de
etapa — foi perguntar, seguindo a própria regra generalizável que o
parágrafo anterior acabou de reafirmar ("quem mais fala disso?"), qual
documento de `wesales/` nenhuma das rodadas de coerência (G-10, G-13, G-14)
tinha cruzado ainda. `ESTADO-E-PLANO.md` nunca tinha sido tocado por
nenhuma delas, apesar de ser o documento com a leitura mais recente da base
inteira — e a seção 8 dele carregava uma pergunta em aberto desde 23/09
02:35 UTC, nunca promovida a item de roadmap: se o contato `Francisca`
(criado pelo canal inbound do WhatsApp) era teste do dono ou pessoa real.
Conferido por API nesta rodada (`conversations_get-messages` no fio
inteiro): é pessoa real, e a conversa é pessoal — PIX, carona, áudio —, sem
nenhum sinal comercial. O contato segue com `etapa-novo-lead` e
`cad-inbound`, oportunidade aberta em `NOVO LEAD`, exposto à próxima rodada
da Cadência Inbound. Fechado como **G-16**: passo preventivo já escrito no
`GUIA-SDR.md` (não depende de `[x]`, é orientação de leitura antes de agir,
mesmo padrão do passo do G-15 para Instagram); a correção no contato
específico (tirar as duas tags, mover a oportunidade para `abandoned`) fica
registrada em `APROVADO.md`, nasce `[ ]`, e entra na mesma fila de decisão
do dono que G-03, G-04 (peça 2), F-09, F-10 e G-11 (item 1) — agora **seis**
decisões, não cinco. Zero campo novo, zero escrita no CRM (a leitura do fio
de mensagem não altera nada): item de especificação e achado de coerência
entre documentos, a escrita em si aguarda `[x]`. Detalhe completo no
próprio G-16, acima.

Com isso, G-16 fecha por inteiro quanto à especificação; G-03, G-04 (peça
2), F-09, F-10, G-11 (item 1) e G-16 são as **seis** decisões que esperam o
dono — a próxima rodada sem tela nem decisão desbloqueada repete o mesmo
caminho de sempre, agora também cruzando `ESTADO-E-PLANO.md` na varredura
de coerência (a lista de arquivos a cruzar que o G-14 abriu ainda não o
incluía).

**G-17 aberto em 23/09/2026, sessão automática seguinte — lacuna achada
seguindo `git log` de `wesales/` além do roadmap principal, exatamente a
regra que o G-10 deixou escrita ("verificar o git log deveria entrar na
varredura de coerência de toda rodada").** Entre a leitura do G-16 e esta
rodada, uma sessão em paralelo (commits `ab5f4d5`, `46724a9`, `31206c6`,
`ea16ca3`) trabalhou a pendência 9e de `ESTADO-E-PLANO.md` sem nunca virar
item deste roadmap — o mesmo padrão do G-10 (dois fluxos de leitura, um
plano decidido/achado num não chega ao outro). CRM reconfirmado por API
nesta rodada: 56 oportunidades, mesma composição da leitura do G-16 (49
`NOVO LEAD` open + 1 `REUNIÃO DE DIAGNÓSTICO` open + 1 `CONECTAR` open + 2
`CONECTAR` lost + 2 `NEGOCIAR` open + 1 `NEGOCIAR` lost), 56 campos de
contato — G-03, G-04 (peça 2), F-09, F-10 e G-11 (item 1) seguem aguardando
o dono, sem novidade. O achado em si (três cadências publicadas que não
leem o portão de capacidade, uma delas — `Reengajamento 90 dias` — gastando
a cota semanal sem nunca respeitá-la) já estava medido e documentado em
`build-wesales.md` §2.36–2.39 por essa sessão paralela; o trabalho desta
rodada foi só a promoção a item de roadmap com "Pronto quando" próprio —
sem essa ponte, a próxima leitura que só abrisse este arquivo não saberia
que a pendência existe, mesmo risco que o G-16 já tinha descrito para
`ESTADO-E-PLANO.md` como um todo. Zero campo, zero tag, zero escrita no
CRM: item de coerência entre documentos e especificação de decisão, não
depende de `APROVADO.md` (edição de workflow publicado não sai por este
conector). Detalhe completo no próprio G-17, acima.

Com isso, G-03, G-04 (peça 2), F-09, F-10, G-11 (item 1), G-16 e G-17 são as
**sete** decisões que esperam o dono — a próxima rodada sem tela nem decisão
desbloqueada repete o mesmo caminho de sempre.

**G-18 aberto e fechado em 23/09/2026, sessão automática seguinte — a
pendência 2 do G-13 (o ramo `Atendeu` sem a segunda linha de defesa que o
`Não ligar` já tem contra falha de timing) finalmente ganhou "Pronto quando"
próprio, patch escrito e validado por dump.** Conferido também no dump da
própria `Cadência 12x30` — ela já se auto-remove no caso comum (mesmo dia,
dentro da janela da tentativa); o que faltava era só a rede de segurança
para quando a classificação chega fora dessa janela, não a remoção em si.
CRM reconfirmado por API nesta rodada: 56 oportunidades e 56 campos
de contato, mesma composição da leitura do G-17 — G-03, G-04 (peça 2), F-09,
F-10, G-11 (item 1), G-16 e G-17 seguem aguardando o dono, sem novidade.
Não é lacuna nova: é a mesma instrução de sempre (reler pendência represada
antes de procurar achado novo) aplicada a uma frase que o próprio G-13 já
tinha escrito e ninguém tinha revisitado. A diferença deste item para os
sete acima: **não é decisão do dono** — é patch pronto
(`wesales/tools/patch_remove_atendeu.py`, validado por `--dump`, `exit 0`),
mesma classe de F-11/F-12/F-13/F-15/G-07/G-08/G-11 (itens 2/3): espera só
ser aplicado na tela ou rodado no PC, não uma escolha entre opções. Zero
tag, zero campo, zero escrita no CRM.

Com isso, nenhum item numerado (G/R/F) resta sem especificação nem sem dono
claro: G-03, G-04 (peça 2), F-09, F-10, G-11 (item 1), G-16 e G-17 continuam
sendo as sete decisões que esperam o dono; F-11, F-12, F-13, F-15, G-07,
G-08, G-11 (itens 2/3) e **G-18** têm desenho completo (G-18 com patch já
validado por dump) e só faltam ser montados/aplicados na tela ou no PC; F-14
é checklist de gestor, pronto para uso assim que o número começar a discar
de verdade. A próxima rodada sem tela nem decisão desbloqueada repete o
mesmo caminho de sempre — agora também conferindo se o dono já rodou algum
dos patches represados (G-17, G-18) antes de assumir que continuam abertos.

**G-19 aberto em 23/09/2026, sessão automática seguinte — sweep de
coerência limpo de novo (56 oportunidades, mesma composição da leitura do
G-18; 56 campos de contato), G-03/G-04 (peça 2)/F-09/F-10/G-11 (item
1)/G-16/G-17 sem novidade.** A lacuna não veio de grep por nome de etapa:
veio de olhar o `git log` mais recente de `wesales/` (regra do G-10, "o git
log deveria entrar na varredura de toda rodada") e achar um commit
(`8f1001c`, fora do vocabulário G/F/R — "A1 conferido") apontando para
`PLANO-MULTICANAL.md`, documento que o G-10 já tinha cruzado uma vez mas
cuja seção "Fila autônoma" (protocolo de execução próprio, por fora do
`APROVADO.md`, usando o bearer local que esta sessão na nuvem não tem — não
executável nem replicável aqui) nunca tinha sido lida linha a linha por uma
rodada deste roadmap. Dela não saiu item novo (a pergunta que o próprio A9
carregava, "Francisca é teste ou é gente", já tinha sido promovida ao G-16
por outro caminho) — mas o rastro levou a `rotina-limpar-tarefas.md`, que
tinha o achado completo (dois `cron` que se somam, `checkout` pinado nesta
branch de PR) escrito e medido por API do Actions, replicado em
`ESTADO-E-PLANO.md` (pendências 11a/11b) e nunca promovido a item
rastreável — a mesma classe exata que já rendeu G-16/G-17/G-18. Fechado
como **G-19**: os dois defeitos vivem em `.github/workflows/
faxina-tarefas.yml`, fora de `wesales/` e fora do que `APROVADO.md`
governa, então esta sessão só documenta e não edita — a correção é mecânica
(trocar o `ref:` do `checkout` na branch padrão) mais uma decisão pequena
do dono (qual cadência vale, a do `cron` ou a do documento). Zero campo,
zero tag, zero escrita no CRM: item de coerência entre documentos e de
infraestrutura de repositório, não depende de `APROVADO.md`. Detalhe
completo no próprio G-19, acima.

Com isso, G-03, G-04 (peça 2), F-09, F-10, G-11 (item 1), G-16, G-17 e
**G-19** são as **oito** decisões que esperam o dono; F-11, F-12, F-13,
F-15, G-07, G-08, G-11 (itens 2/3) e G-18 continuam com desenho completo e
patch pronto, só faltando tela ou PC; F-14 é checklist de gestor, pronto
para uso assim que o número começar a discar de verdade. A próxima rodada
sem tela nem decisão desbloqueada repete o mesmo caminho de sempre — agora
também lendo `PLANO-MULTICANAL.md` por inteiro (não só a tabela de decisões
D1-D14, também a "Fila autônoma" no fim) na varredura de coerência, e
conferindo se o dono já mesclou o PR #93 (o que fecharia sozinho a metade
"branch" do G-19, restando só a cadência).

> **Nota de 28/09/2026 (G-35): esta instrução nunca foi cumprida como
> escrita, e não podia ser — o PR #93 fechou sem merge em 24/09/2026, um
> dia depois deste parágrafo, e nenhuma rodada entre 24/09 e 28/09 voltou a
> checar o GitHub para notar. Detalhe e correção em G-35.**

**G-20 aberto e fechado em 23/09/2026, sessão automática seguinte — CRM
reconfirmado sem mudança (56 oportunidades, mesma composição da leitura do
G-19; 56 campos de contato) e PR #93 ainda `open`/`draft`: as oito decisões
acima seguem exatamente onde estavam.** A lacuna não veio de grep por nome
nem de `git log` fora de `wesales/` (as duas veias que renderam G-17/G-19)
— veio de resomar, pela primeira vez, os totais que o projeto declara
contra a própria lista que cada um deveria resumir. Bateu para campos; não
bateu para tags: `campos-e-tags.md` dizia "10 na conta fora da numeração" e
"Total na conta hoje: 25", `APROVADO.md` dizia "são dez as tags fora desta
lista" e `build-wesales.md` §2.32 dizia "a conta tem 25 tags" — as três
frases enumeravam, na sequência seguinte, `teste-regua`, `fechar-horario`,
`cadencia-12x30-p2`, `teste-12x30` e "as 8 do Espelho de Etapa" (1+1+1+1+8 =
12, não 10; com as 15 do projeto, 27, não 25). Corrigidos os três; `campos-
e-tags.md` ganhou a convenção "onde mora a contagem" que a seção de campos
já tinha, e os outros dois pararam de repetir o número. Zero campo, zero
tag, zero escrita no CRM: item de coerência entre documentos, não depende
de `APROVADO.md`. Detalhe completo no próprio G-20, acima. **Regra prática,
generalizável, que estende o "quem mais fala disso?" do G-10/G-14/G-16/G-17
de nomes para números:** uma varredura de coerência que só procura texto
divergente (nome de etapa, merge field órfão) não acha soma errada — um
total pode ter sido editado na mesma rodada que acrescentou o dado novo, e
ainda assim nunca ter sido resomado contra a própria enumeração ao lado.
A partir de agora, toda rodada que mexer em contagem (campo, tag, etapa,
tentativa) resoma a lista antes de aceitar o número escrito perto dela.

Com isso, nenhum item numerado (G/R/F) muda de estado nesta rodada além do
próprio G-20: G-03, G-04 (peça 2), F-09, F-10, G-11 (item 1), G-16, G-17 e
G-19 continuam sendo as oito decisões que esperam o dono — a próxima rodada
sem tela nem decisão desbloqueada repete o mesmo caminho de sempre.

**Sessão automática seguinte, 23/09/2026 — sem item numerado novo; F-10
recebeu a leitura que muda a leitura do próprio F-10, e o G-16 fechou por
inteiro numa sessão em paralelo, encontrada só no `git fetch` antes do
push.** CRM reconfirmado por API às 17:07 UTC: 56 oportunidades, mesma
composição da leitura do G-20 (49 `NOVO LEAD` open + 1 `REUNIÃO DE
DIAGNÓSTICO` open + 1 `CONECTAR` open + 2 `CONECTAR` lost + 2 `NEGOCIAR`
open + 1 `NEGOCIAR` lost), 56 campos de contato — nada para o sweep de
coerência de sempre corrigir nesse momento. O trabalho desta rodada não
veio de grep por nome nem de contagem duplicada: veio de reler, como a
própria seção "Ordem sugerida" instrui quando não há tela nem decisão nova,
os itens represados por informação que pode ter vencido — e o F-10, a
última vez que teve o próprio número atualizado em 22/09 às 09:36 UTC
(24h19min, 1,61× o recorde da base), nunca tinha sido reconferido desde
então. Reconferido agora: o lead pago mais recente continua sendo `Carlos
Andrade`, de 21/09 09:17:26 UTC — o silêncio chegou a **55h50min, 3,7× o
maior intervalo que esta base já teve**, cobrindo três dias de calendário
(segunda a quarta) sem uma única exceção. Não é a mesma leitura republicada:
é a evidência de que a causa (campanha pausada, orçamento esgotado ou
criativo reprovado — as três hipóteses que o item já levantava) segue
ativa, e cada rodada que reconfirma o silêncio torna "vai normalizar
sozinho" uma aposta pior. Detalhe completo dentro do próprio F-10, acima.

**Um minuto depois da leitura acima** (17:08 UTC), outra sessão autorizada
pelo dono ("sim", ~11:35 BRT) fechou o G-16: a oportunidade da `Francisca`
saiu de `NOVO LEAD`/`open` para `abandoned`, com as tags de cadência
removidas e `nao-perturbe` aplicada antes, na ordem certa para não ser
capturada pela Triagem da Nutrição — detalhe completo no próprio G-16,
acima. `git fetch` antes deste push achou os dois commits, e o merge
incorporou a mudança sem conflito (arquivos diferentes). A composição de
`NOVO LEAD` a partir de 17:08 UTC é **48** open + 1 abandoned, não mais 49
open — corrigido nos dois lugares desta rodada que citavam 49 como atual
(o próprio corpo do F-10, acima). Zero campo, zero tag, zero escrita no CRM
por esta sessão: a escrita do G-16 foi de outra sessão, lida de volta e
incorporada por coerência, não repetida.

**Segunda reconciliação, mesma janela — `git fetch` achou um terceiro
commit em paralelo antes deste push completar, e ele também mexe no G-17
acima.** O dono decidiu a opção (A) para as duas cadências restantes,
patches escritos e validados (`patch_portao_inbound.py`,
`patch_portao_noshow.py` — planos ao vivo conferidos), e a correção "o
`Reengajamento 90 dias` não existe mais, foi substituído pela `Nutrição —
WhatsApp 15 dias`" já está registrada no próprio G-17. **O que não mudou: a
aplicação em si.** As duas gravações foram negadas pelo classificador do
modo automático (o dono mantém o modo automático ligado) — G-17 sai da
lista de "decisão do dono" e entra na mesma classe de G-11 (itens 2/3) e
G-18: desenho e decisão completos, patch validado, só falta rodar
`--aplicar` no PC do dono ou aplicar na tela.

Com isso, G-03, G-04 (peça 2), F-09, **F-10**, G-11 (item 1) e G-19 são
agora as **seis** decisões que esperam o dono — duas a menos que no
fechamento do G-20 (G-16 executado, G-17 decidido e só pendente de
aplicação). F-10 chega à próxima rodada com o peso maior do que saiu desta.
A próxima rodada sem tela nem decisão desbloqueada repete o mesmo caminho
de sempre — e, com pelo menos três sessões trabalhando esta subconta na
mesma janela de tempo, vale um `git fetch` antes de qualquer leitura de CRM
que vá virar número escrito no roadmap, não só antes do push: uma leitura
que já nasce velha por 60 segundos ainda é melhor que uma que nasce velha
por não ter conferido se alguém mexeu primeiro.

**G-21 aberto e fechado (promoção + achado de instrução) em 23/09/2026,
sessão automática seguinte — `git fetch` limpo desta vez (nenhum commit
novo na janela desta leitura), CRM reconfirmado sem mudança (56
oportunidades, mesma composição da reconciliação acima; 56 campos de
contato): G-03, G-04 (peça 2), F-09, F-10, G-11 (item 1) e G-19 seguem
exatamente as seis decisões que esperam o dono, sem novidade.** A lacuna
não veio de grep por nome nem de contagem — veio, de novo, de reler
`ESTADO-E-PLANO.md` linha por linha (regra que o G-16/G-17/G-19 já
deixaram escrita: "documento medido não é o mesmo que documento
rastreado") e achar que a pendência `9c` (`Canal que conectou`) tinha
decisão do dono já dada e patch já escrito (`dac443f`,
`patch_canal_conectou.py`, `build-wesales.md` §2.41) desde a rodada
anterior, sem nunca ter virado item de roadmap nem atualizado a própria
linha que a descrevia — o quarto caso exato do mesmo padrão de G-16/
G-17/G-19. Detalhe completo, achado extra sobre `GUIA-SDR.md` ficar
desatualizado no dia em que a automação completar, e as três correções de
coerência aplicadas, no próprio G-21, acima.

Com isso, G-03, G-04 (peça 2), F-09, F-10, G-11 (item 1) e G-19 continuam
sendo as seis decisões que esperam o dono; F-11, F-12, F-13, F-15, G-07,
G-08, G-11 (itens 2/3), G-17, G-18 e agora **G-21** são os itens com
desenho e decisão completos, patch validado, só faltando tela ou PC — a
lista cresceu em um, não porque surgiu trabalho novo, mas porque um
trabalho que já existia (decisão do dono de 23/09, patch de `dac443f`)
finalmente ganhou onde ser visto por quem só abre este roadmap. A próxima
rodada sem tela nem decisão desbloqueada repete o mesmo caminho de
sempre — e, seguindo a mesma regra que abriu G-16/G-17/G-19/G-21, vale
conferir se alguma outra linha de `ESTADO-E-PLANO.md` (ou de
`PLANO-MULTICANAL.md`, que o G-19 já apontou como não lido por inteiro)
tem decisão e patch prontos represados do mesmo jeito, antes de assumir
que a fonte dessa classe de achado secou.

**G-22 aberto e especificado em 23/09/2026, sessão automática seguinte —
`git fetch` limpo (nenhum commit novo na janela desta leitura), CRM
reconfirmado sem mudança (56 oportunidades, mesma composição da leitura
do G-21; 56 campos de contato): as seis decisões do dono e os dez itens
com desenho completo represados por tela/PC seguem exatamente onde
estavam, sem novidade.** A lacuna veio da mesma regra do G-16/G-17/G-19/
G-21 ("documento medido não é o mesmo que documento rastreado"), aplicada
desta vez a `AGENTE-IA-CONEXAO.md` — nunca cruzado por nenhuma rodada de
coerência anterior (G-10/G-13/G-14 cruzaram `PLANO-MULTICANAL.md` e
`ESTADO-E-PLANO.md`; nenhuma tinha chegado neste). O documento já carregava,
desde 22/09/2026, uma dúvida em aberto sobre a própria razão de existir
(seção 8, item 2: "se o agente só responde WhatsApp, não alcança os 5 do
Instagram — que são o motivo principal dele existir") e uma proteção
central sem confirmação de tela (seção 1, "a regra do portão — a mais
importante", que o item 3 da seção 8 já avisava poder não existir na
tela). Diferente dos quatro achados anteriores desta família (que tinham
decisão e patch prontos, só sem ponte para o roadmap), aqui não havia
decisão nem patch — só pesquisa pendente. `WebSearch` (confiança média,
`help.gohighlevel.com` bloqueado pelo proxy como de costume) confirmou que
Instagram é canal nativo do Conversation AI Bot (reduz a dúvida do item 2
a uma pergunta de configuração desta subconta, não de suporte da
plataforma) e achou, em três fontes convergentes, uma ação de workflow
nativa (`Update Conversation AI Bot and Status`) que resolve a proteção do
item 1 sem depender de nenhum filtro de tela nunca confirmado — dois
workflows novos, sidecar por tag no mesmo padrão que o dono já escolheu
para o removedor de `conectado-hoje`, sem tocar a Cadência 12x30 nem o
Pós-ligação v2 publicados. Fechado como **G-22**: especificação nó a nó
completa, zero campo, zero tag, zero escrita no CRM (pesquisa e desenho,
não depende de `APROVADO.md`); `AGENTE-IA-CONEXAO.md` (§1, §8) atualizado
com o achado. Detalhe completo no próprio G-22, acima.

Com isso, G-03, G-04 (peça 2), F-09, F-10, G-11 (item 1) e G-19 continuam
sendo as seis decisões que esperam o dono; F-11, F-12, F-13, F-15, G-07,
G-08, G-11 (itens 2/3), G-17, G-18, G-21 e agora **G-22** são os itens com
desenho completo (a maioria com patch validado; G-22 com dois workflows
novos especificados nó a nó) e só faltam ser montados/aplicados na tela ou
no PC — a lista cresceu em um, desta vez por lacuna de pesquisa nova, não
por releitura de pendência represada como as quatro promoções anteriores.
A próxima rodada sem tela nem decisão desbloqueada repete o mesmo caminho
de sempre — variando a fonte da varredura de coerência a cada vez, para
não esgotar sempre o mesmo documento: `AGENTE-IA-CONEXAO.md` acabou de ser
cruzado; `script-de-ligacao.md`, `GUIA-CLOSER.md`, `GUIA-SDR.md` e
`conectar.md` ainda não passaram por nenhuma rodada desta família.

**G-23 fechado em 23/09/2026, sessão automática seguinte — o F-13
(`negociacao-estagnada`) já estava publicado com um desenho diferente do
especificado (5 dias, não 3; gatilho na mudança de etapa, não no campo), e
um segundo alerta (`proposta-pendente`) já cobria um buraco que nenhum
documento tinha registrado, achado ao cruzar `GUIA-CLOSER.md`.** CRM
reconfirmado sem mudança (56 oportunidades, mesma composição da leitura do
G-22; 56 campos de contato): G-03, G-04 (peça 2), F-09, F-10, G-11 (item 1)
e G-19 seguem sendo as seis decisões que esperam o dono, sem novidade. Zero
campo, zero tag criados por esta sessão (as duas já existiam antes de a
rodada começar): reconciliação de seis documentos (`campos-e-tags.md`,
`APROVADO.md`, `build-wesales.md`, `IMPLEMENTACAO-WORKFLOWS.md`,
`GUIA-MONTAGEM.md`, e o próprio item) contra `tools/build_estagnacao.py` e
`PLANO-MULTICANAL.md` A5/A8. Detalhe completo no próprio G-23, acima.

Com isso, G-03, G-04 (peça 2), F-09, F-10, G-11 (item 1) e G-19 continuam
sendo as seis decisões que esperam o dono; F-11, F-12, F-13, F-15, G-07,
G-08, G-11 (itens 2/3), G-17, G-18, G-21, G-22 e agora **G-23** são os
itens com desenho completo (a maioria com patch validado ou já publicado)
e só faltam ser montados/aplicados na tela ou no PC. `GUIA-CLOSER.md`
acabou de ser cruzado; `script-de-ligacao.md`, `GUIA-SDR.md` e
`conectar.md` seguem na lista de documentos ainda não cruzados por
nenhuma rodada desta família.

**G-24 aberto e fechado em 23/09/2026, sessão automática seguinte — o
próprio G-23 fechou sem o parágrafo de recapitulação que todo G-item desta
família ganha aqui, e a lista de documentos pendentes (parágrafo acima)
ainda citava `GUIA-CLOSER.md` como não cruzado quando o G-23 já o tinha
cruzado.** `git fetch` limpo (nenhum commit novo na janela desta leitura),
CRM reconfirmado sem mudança (56 oportunidades, mesma composição da
leitura do G-23; 56 campos de contato): as seis decisões do dono seguem
exatamente onde estavam. A lacuna veio de aplicar a regra "documento
medido não é o mesmo que documento rastreado" **a esta própria seção**, não
a um documento-irmão — o parágrafo que faltava é o de cima. Cruzados nesta
rodada os três documentos que sobravam da lista do G-22
(`script-de-ligacao.md`, `GUIA-SDR.md`, `conectar.md`) contra as decisões
mais recentes publicadas (`PLANO-MULTICANAL.md` D1-D14/A1-A9): achado
negativo — os três já batem com o publicado (etapa `REUNIÃO DE
DIAGNÓSTICO`, teto de 100 toques/50 vencidas, opção `Desqualificado`,
pendência de gravação/LGPD datada e correta), nenhuma correção necessária
neles. Detalhe completo no próprio G-24, acima.

Com isso, G-03, G-04 (peça 2), F-09, F-10, G-11 (item 1) e G-19 continuam
sendo as seis decisões que esperam o dono; F-11, F-12, F-13, F-15, G-07,
G-08, G-11 (itens 2/3), G-17, G-18, G-21, G-22, G-23 e agora **G-24**
(este último só de coerência da própria seção, não de tela/PC) são os
itens fora das seis decisões. Com o G-24, a lista de documentos "ainda não
cruzados por nenhuma rodada desta família" que o G-22 tinha aberto **fica
vazia** — não porque a varredura de coerência acabou (ela não acaba;
`CONFERENCIA-CAMPOS.md`, `GUIA-MONTAGEM.md`, `INVENTARIO-WORKFLOWS.md`,
`biblioteca-mensagens.md`, `rotina-horaria.md`, `auditoria-etapa1.md` e
`README.md` nunca tiveram uma rodada dedicada desta família nomeando-os um
a um), mas porque a lista explícita que vinha sendo citada por nome
esgotou. A próxima rodada sem tela nem decisão desbloqueada repete o
mesmo caminho de sempre — escolhendo a próxima fonte entre os sete
documentos do parágrafo anterior, ou voltando a reler os itens represados
por premissa técnica (mesmo caminho que já destravou F-05 e F-06), antes
de procurar lacuna genuinamente nova.


**Atualização de 27/09/2026 — reconciliação deste arquivo, e o que mudou
desde o fecho do G-24 (23/09/2026, acima).** Este arquivo truncou por
acidente em 24/09/2026 e ficou com 1.357 das 5.619 linhas por 3 dias, sem
ninguém notar (alerta no topo do arquivo, detalhe completo lá). Reconciliado
nesta sessão a partir do commit `6821497` (a última versão íntegra) mais o
trabalho real feito depois, em cima do arquivo já truncado: a promoção do
G-03 (decidida e agendada para 29/09/2026 — sai da lista de decisões
pendentes abaixo) e o item novo desta sessão, renumerado **F-18**
(`monetaryValue`).

Das seis decisões que o parágrafo do G-24 fechava em 23/09/2026, sobram
cinco: **G-04 (peça 2), F-09, F-10, G-11 (item 1) e G-19.** F-18 se soma à
lista dos itens que esperam evento real, não decisão do dono — junto com
R-14 — porque o primeiro `won` desta operação ainda não aconteceu.

`build-wesales.md` sofreu o mesmo acidente (commit `c2dadb5`, 8.580 → 4.349
linhas) e segue truncado: não só as seções inteiras que faltam (§2.25 a
§2.44), mas conteúdo interno perdido em toda seção que sobreviveu (medido
seção a seção contra o commit `875d8d7` íntegro: de quase intacta, seção 11,
a mais da metade perdida, seção 6). Não reconcilia por colagem de seção
como este arquivo — precisa de diff parágrafo a parágrafo em cerca de
trinta seções, grande demais para esta execução. Quem pegar: `875d8d7` é a
base íntegra; o HEAD do momento tem trabalho real por cima (§2.45 a §2.47,
mais o que vier depois) que precisa sobreviver ao merge.

**Sessão automática seguinte, 27/09/2026 — as seções inteiras que faltavam
em `build-wesales.md` (§2.25 a §2.44, mais §4.1 e §5.5) foram coladas de
volta a partir de `875d8d7`, conferidas byte a byte.** Nenhuma tinha edição
real por cima na cópia truncada, então colar não arriscou apagar trabalho
novo. Isso reduz a peça 2 (diff parágrafo a parágrafo das seções que
"sobreviveram" à truncagem) de "cerca de trinta seções" para as que
realmente sobreviveram: 1, 2, 2.9 a 2.24, 3, 4, 5, 5.1 a 5.4, 6, 7, 8, 9,
10, 11 — e achou, ao chegar na seção 1, a mesma classe de colisão de número
que o F-07→F-18 já tinha mostrado neste arquivo: a cópia truncada reusara
`### 1.4` (que na base é o F-11, fechado em 22/09/2026) para o G-03,
decidido só depois do acidente. Detalhe completo no alerta do topo deste
arquivo. Zero campo, zero tag, zero escrita no CRM: reconciliação de
documentação, não depende de `APROVADO.md`.

**Mesma sessão, peça seguinte — seção 1 de `build-wesales.md` reconciliada
por inteiro.** Diff parágrafo a parágrafo (não colagem direta, por causa da
colisão do parágrafo acima): a seção 1 da base (`875d8d7`, 495 linhas,
incluindo a segunda renomeação de etapa do G-12 e a correção do G-13 que a
cópia truncada nunca chegou a ter) foi colada por inteiro, e o G-03 — que
uma colagem direta teria apagado — foi preservado como `### 1.5`, logo
depois do F-11 restaurado em `1.4`. Conferido byte a byte contra a base
(495/495 linhas idênticas) e por `grep -rn "seção 1.4" wesales/` que nenhum
outro documento cita esta seção referindo-se ao G-03 (as duas ocorrências
fora deste arquivo já apontavam para o F-11 desde sempre) — só o alerta
deste roadmap precisava da correção, feita no mesmo commit. Restam 13
seções/grupos da lista acima (2, 2.9 a 2.24, 3, 4, 5, 5.1 a 5.4, 6, 7, 8, 9,
10, 11) — cada uma pode esconder o mesmo tipo de colisão que a 1.4 acabou
de mostrar duas vezes neste projeto (F-07/F-18 e agora F-11/G-03), então
quem pegar a próxima confere número de seção contra o roadmap antes de
colar, não só o texto. Zero campo, zero tag, zero escrita no CRM. **G-04
(peça 2), F-09, F-10, G-11 (item 1) e G-19** continuam sendo as cinco
decisões que esperam o dono (G-03 já saiu desta lista — decidido e
agendado para 29/09/2026, parágrafo acima), sem novidade nesta sessão. CRM
reconfirmado por API: 56 campos de contato, sem mudança; **64 oportunidades
(39 `CONECTAR` open + 10 `NOVO LEAD` abandoned + 8 `CONECTAR` lost + 2
`NOVO LEAD` open + 2 `NEGOCIAR` open + 1 `NOVO LEAD` lost + 1 `NEGOCIAR`
lost + 1 `REUNIÃO DE DIAGNÓSTICO` open), 8 a mais que a última leitura
registrada (56) — composição consistente com o backfill do G-03 já
executado (seção 1.5 acima: 41 promovidas de `NOVO LEAD` para `CONECTAR`
em 24/09/2026), não investigada além disso nesta sessão.

**F-19 aberto e especificado em 27/09/2026, sessão automática seguinte — os
dois documentos que o acidente de 24/09 atingiu já estavam reconciliados
por inteiro (fecho anterior, acima); com nada represado por decisão do dono
nem por premissa técnica não testada, o passo honesto era a pesquisa de
concorrência que este roadmap sempre exige antes de declarar o bloco 6
esgotado.** CRM reconfirmado por API antes de desenhar: 64 oportunidades e
56 campos de contato, sem mudança frente à leitura anterior — G-04 (peça 2),
F-09, F-10, G-11 (item 1) e G-19 continuam sendo as cinco decisões que
esperam o dono, sem novidade. A lacuna veio de perguntar, para cada um dos
seis itens já fechados do bloco 6 (F-01 a F-06), "o que Outreach/Salesloft
fazem aqui que este projeto ainda não tem" — e achar que a Interceptação de
Sinal (F-01) nunca ganhou o filtro que o R-17 deu ao opt-out: uma
auto-resposta de ausência (comum em WhatsApp Business de lead B2B) passa
pelo mesmo `Customer Replied` sem nenhuma das 17 frases de opt-out, gera
sinal quente falso e, pior, é apagada da cadência em silêncio pelo
`Stop on Response` nativo (sem filtro de conteúdo possível, confirmado por
pesquisa, não suposto). Fechado como **F-19**: workflow novo especificado
nó a nó (`build-wesales.md`, seção 2.48), tag `resposta-automatica` (T-23) e
campo `Respostas automáticas` (C-33) especificados em `campos-e-tags.md`,
ambos nascendo `[ ]` em `APROVADO.md` pela regra de sempre. Zero campo, zero
tag, zero escrita no CRM nesta rodada — e um limite documentado em vez de
escondido: a plataforma não expõe "pausar e retomar" cadência por dentro do
próprio workflow (mesma classe de limite já registrada para a Faxina, G-19,
e para a abertura da operação, `ABERTURA.md`), então o item reduz o dano
(alarme falso, silêncio) em vez de prometer paridade completa com
Outreach/Salesloft nisto. Com isto, o bloco 6 fica em F-01 a F-06 e F-11 a
F-19 `FEITO`/especificado, F-07/F-08 `FEITO`, e só F-09/F-10 aguardando o
dono — sem mudança na lista de decisões pendentes.

**F-20 aberto e especificado em 27/09/2026, sessão automática seguinte —
`git fetch` limpo (nenhum commit novo na janela desta leitura), CRM
reconfirmado por API: 64 oportunidades e 56 campos de contato, sem mudança
frente à leitura do F-19 — G-04 (peça 2), F-09, F-10, G-11 (item 1) e G-19
continuam sendo as cinco decisões que esperam o dono, sem novidade.** A
auditoria de cinco auditorias somente-leitura (`auditoria_tudo.py`) também
veio limpa (exit 0), então a lacuna não veio de conferir a conta: veio de
aplicar a própria pergunta do F-19 ("o que Reev/Meetime/Outreach/Salesloft
cobrem que este item ainda não cobre") **ao próprio F-19**, um passo que
nenhuma sessão anterior tinha dado — até aqui a pergunta sempre mirava os
seis itens fechados do bloco 6 (F-01 a F-06), nunca o item que tinha acabado
de nascer na sessão imediatamente anterior. O F-19 escreveu seu filtro de
ausência com o mesmo recorte de canal (WhatsApp e SMS) da Interceptação de
Sinal que ele estava corrigindo, e nunca chegou ao e-mail — o único canal de
texto que o F-15 tinha aberto dias antes, e justamente aquele em que
"fora do escritório" automático é recurso padrão, não configuração rara
como no WhatsApp Business. Mesma classe de achado que o G-06/G-07 já
registraram (a guarda mais nova nunca alcança o canal mais novo), agora
com o intervalo mais curto já visto neste roadmap entre a guarda nascer e
a lacuna dela ser encontrada: uma sessão, não dias. Fechado como **F-20**:
workflow-irmão especificado nó a nó (`build-wesales.md`, seção 2.49),
reaproveitando **sem criar par novo** a tag `resposta-automatica` (T-23) e
o campo `Respostas automáticas` (C-33) que o F-19 já tinha especificado —
o evento que se mede ("auto-resposta na base") é o mesmo, só o canal muda.
Zero campo, zero tag, zero escrita no CRM nesta rodada; `campos-e-tags.md`
e `APROVADO.md` atualizados para registrar que T-23/C-33 agora cobrem dois
workflows, não pedindo aprovação nova — a mesma linha `[ ]` do F-19 passa a
valer para os dois. **Achado extra na mesma varredura:** o próprio F-19
(W25) nunca tinha ganhado linha na "Ordem de montagem" do
`GUIA-MONTAGEM.md` — o checklist manual parou em G-09 e pulou o item mais
recente antes deste. Corrigido no mesmo commit: W25 e o novo W26 (F-20)
ganharam linha própria ali, cada um citando o retoque pendente que só
existe na tela (o `Doesn't Contain` na Interceptação de Sinal, para o W25).
**Regra prática, generalizável, que estende o "quem
mais fala disso?" dos G-10/G-14/G-16/G-17/G-20 de nomes e números para
cobertura de canal:** todo item que fecha uma guarda por `Customer
Replied`/canal específico ganha, na sessão seguinte, a pergunta "essa
guarda existe em todo canal de texto que a operação usa, ou só no canal
que motivou o achado original?" — antes de declarar o bloco 6 esgotado de
novo.

**G-25 aberto em 27/09/2026, sessão automática seguinte — não veio da
pergunta acima (a cobertura de canal do F-19/F-20 segue completa, WhatsApp/
SMS e e-mail, sem lacuna nova ali). Veio de reler `ABERTURA.md`, o handoff
mais recente do projeto, que nenhuma das dez sessões entre `c98add1` e
`ce2a7ce` tinha voltado a conferir enquanto trabalhava F-07 a F-20 e a
reconciliação dos dois documentos truncados.** `git fetch` limpo; CRM
reconfirmado por API: 64 oportunidades (mesma composição de sempre) e 56
campos de contato, sem mudança — mas o achado desta rodada não é sobre
contagem, é sobre um risco com prazo fixo que nenhuma releitura anterior
tinha promovido a item de roadmap. **36-37 execuções da `Cadência Inbound`
estão paradas no nó 24 (`WhatsApp · MI-0`) e disparam juntas na próxima
abertura da janela nativa do workflow — segunda 28/09 08:30
`America/Sao_Paulo`, menos de 26h a partir desta sessão** — 6x o lote de
6/dia que o dono decidiu, um dia antes da data de abertura que ele mesmo
fixou (`ESTADO-E-PLANO.md`, 23/09) e que uma fala posterior dele (27/09,
"terça", citada em `ABERTURA.md`) pode ou não ter substituído; nenhum
documento deste projeto pode arbitrar sozinho qual das duas falas vale.
Verificado por amostra, não presumido: `Carlos Andrade`
(`7ECnj1bSeEIm5P58Ifd9`) segue com `dnd: true` e `Tentativa nº` = 0,
exatamente como o handoff descreveu — protegido, mas os outros 35-36 sem
essa proteção não. Fechado como **G-25**: a correção (`patch_janela_
abertura.py --fechar --aplicar`, ou o equivalente de 2 cliques na tela) já
está escrita e validada em `--dump` desde `eaaf007` — o que falta é
execução, e nenhuma sessão automática tem o bearer de sessão logada que
essa execução exige (confirmado, não suposto: o arquivo não existe neste
contêiner, e os domínios do GHL seguem bloqueados pelo proxy). Notificado o
dono diretamente, porque só ele decide a data e só ele tem o bearer.
**Diferente de todo G/F represado por "tela ou PC" que a lista abaixo já
cita (F-11 a F-22, G-07/G-08/G-11/G-17/G-18/G-21 a G-24): aqueles esperam
sem prazo, este tem prazo fixo e a mensagem que sair não volta** — por
isso entra à frente de todos eles, não atrás. Zero campo, zero tag, zero
escrita no CRM: item de escalonamento, não depende de `APROVADO.md`.

Com isso, **G-25 é o item de maior prioridade do roadmap inteiro enquanto
não estiver `FEITO`** — à frente de G-04 (peça 2), F-09, F-10, G-11
(item 1) e G-19, que continuam sendo as decisões que esperam o dono
sem prazo fixo (G-03 não entra mais nesta lista — decidido e agendado
para 29/09/2026, ver reconciliação acima). A próxima sessão confere
primeiro se a janela das duas
cadências mudou (ou se segunda 28/09 08:30 `America/Sao_Paulo` já passou)
antes de qualquer outro trabalho — inclusive antes da varredura de
coerência ou da pesquisa de concorrência que esta seção normalmente indica
como próximo passo. Se o risco já tiver se concretizado (mensagens
disparadas) ou a janela já tiver sido fechada por alguém com acesso à
tela, este parágrafo e o próprio G-25 acima são atualizados com o
resultado antes de qualquer outra linha de trabalho.

**Reconferido em 27/09/2026 ~11:05 UTC, sessão automática seguinte — a
janela não mudou, não abriu antes do previsto, e nenhum disparo aconteceu
(detalhe no próprio G-25, acima).** G-25 continua sendo o item de maior
prioridade do roadmap enquanto não estiver `FEITO`. Único fato novo: um
quarto caminho de correção automática foi conferido e também bate na mesma
parede (Composio/`gohighlevel` sem conta conectada, e conectar dependeria
do mesmo clique do dono que já resolveria o problema direto na tela) — e o
dono recebeu um aviso direto (push), não só o registro neste arquivo, dado
que faltam menos de 25h para a janela abrir. G-04 (peça 2), F-09,
F-10, G-11 (item 1) e G-19 continuam sendo as decisões sem prazo fixo
que esperam o dono, sem novidade nesta sessão.

**Reconferido em 27/09/2026 ~13:05 UTC, sessão automática seguinte —
faltam ~22h25min para a janela abrir, nada mudou.** `git fetch` limpo.
`opportunities_search-opportunity` (status `all`) confirma 64 oportunidades,
mesma composição (13 `NOVO LEAD`, 47 `CONECTAR`, 3 `NEGOCIAR`, 1 `REUNIÃO
DE DIAGNÓSTICO`; 43 `open`, 11 `lost`, 10 `abandoned`); `Carlos Andrade`
(`7ECnj1bSeEIm5P58Ifd9`) segue `dnd: true`, tag `atraso-1a-tentativa`
presente, campo `Tentativa nº` = 0 — protegido. Com o risco reconferido e
sem novidade, a sessão seguiu para a varredura de canal que o próprio F-20
deixou pronta ("essa guarda existe em todo canal de texto que a operação
usa, ou só no que motivou o achado original?") — aplicada desta vez à
própria Interceptação de Sinal (F-01, 2.9.3), não a uma guarda vizinha, e
achou o mesmo tipo de lacuna: nunca ganhou versão e-mail. Fechado como
**F-21** (acima, entre F-20 e G-25): workflow "Interceptação de Sinal —
E-mail" especificado nó a nó (`build-wesales.md`, seção 2.50), desenhado
para não repetir os dois erros que o 2.9.3 só corrigiu depois de publicado
(opt-out e ausência tratados como sinal quente) e para não aplicar
`fila-quente`/"ligar agora" a uma população que, por definição, não tem
telefone — reabre a oportunidade em `CONECTAR` (mesmo destino do R-08) e só
enfileira para ligação quando há telefone; senão, avisa o gestor com
instrução que já leva isso em conta. Zero campo, zero tag: uma opção nova
(`Resposta de e-mail`) no campo já existente `Sinal recebido` (C-13),
registrada em `campos-e-tags.md` e como linha própria `[ ]` em
`APROVADO.md` — mesma classe de limite (edição de tela, não sai por API)
já documentada para criação de campo. `GUIA-MONTAGEM.md` e
`IMPLEMENTACAO-WORKFLOWS.md` (W27) atualizados no mesmo commit. G-04
(peça 2), F-09, F-10, G-11 (item 1) e G-19 continuam sendo as
decisões sem prazo fixo que esperam o dono, sem novidade nesta sessão.

**Reconferido em 27/09/2026 ~14:05 UTC, sessão automática seguinte —
faltam ~21h25min para a janela abrir (segunda 28/09 08:30
`America/Sao_Paulo` = 11:30 UTC).** `git fetch` limpo (nenhum commit novo
na janela desta leitura). `opportunities_search-opportunity` (status
`all`) confirma 64 oportunidades, composição idêntica à leitura anterior
(13 `NOVO LEAD`, 47 `CONECTAR`, 3 `NEGOCIAR`, 1 `REUNIÃO DE DIAGNÓSTICO`;
43 `open`, 11 `lost`, 10 `abandoned`); `Carlos Andrade`
(`7ECnj1bSeEIm5P58Ifd9`) segue `dnd: true`, tag `atraso-1a-tentativa`
presente — protegido, nenhum disparo aconteceu. Com o risco reconferido e
sem novidade, a sessão seguiu a rotina obrigatória de todo item novo deste
roadmap (pesquisa de concorrência antes de declarar o bloco 6 esgotado),
mas mudou o alvo da pergunta: em vez de reaplicá-la às guardas de texto
(F-19/F-20/F-21 já esgotaram opt-out/ausência/sinal nos três canais), a
pergunta foi aos seis pilares do bloco 6 — e achou que a proteção de
infraestrutura de canal (F-07 WhatsApp, F-08/F-14 telefone) nunca ganhou
par para o e-mail, o canal que o F-15 abriu e que F-19/F-20/F-21/G-07 já
usam. Fechado como **F-22** (acima, entre F-21 e G-25): o GHL nativo tem,
desde 27/04/2026, rampa automática por 8 estágios para domínio
compartilhado — melhor que a rampa manual que Outreach/Salesloft exigem do
usuário, e esta subconta (criada 17/09/2026) se qualifica sozinha. O item
não constrói nada (a plataforma já rampa sozinha); documenta as duas
bifurcações que ninguém tinha registrado (domínio compartilhado vs.
dedicado, warmup manual só no segundo caso) e estende a tabela "Quando
olhar" do F-07 para o canal novo. Zero campo, zero tag, zero workflow,
zero escrita no CRM: item de documentação e pesquisa, não depende de
`APROVADO.md`. Detalhe nó a nó — na verdade sem nó, é rotina manual — em
`build-wesales.md`, seção 2.51. G-04 (peça 2), F-09, F-10, G-11
(item 1) e G-19 continuam sendo as decisões sem prazo fixo que
esperam o dono, sem novidade nesta sessão.

**Reconferido em 27/09/2026 ~16:05 UTC, sessão automática seguinte —
faltam ~19h25min para a janela abrir (segunda 28/09 08:30
`America/Sao_Paulo` = 11:30 UTC).** `opportunities_search-opportunity`
(status `all`) sobe de 64 para **65 oportunidades** (14 `NOVO LEAD` [3 open
+ 10 abandoned + 1 lost], 47 `CONECTAR` [39 open + 8 lost], 3 `NEGOCIAR` [2
open + 1 lost], 1 `REUNIÃO DE DIAGNÓSTICO` lost) — 1 lead novo frente à
última leitura, sem qualquer sinal do disparo em massa do G-25;
`locations_get-custom-fields` confirma 56 campos de contato, sem mudança;
`Carlos Andrade` (`7ECnj1bSeEIm5P58Ifd9`) segue `dnd: true`, tag
`atraso-1a-tentativa` presente — G-25 continua sem novidade, protegido.
Sweep de coerência de sempre (números/nomes tocados nas últimas rodadas —
F-19 a F-22, T-23, G-25/G-26 — em todo o `wesales/`) não achou nada novo em
texto; a correção do G-26 (número fixo tirado de `build-wesales.md`
§2.32) segue de pé, sem regressão. A sessão seguiu para a pergunta que
ainda não tinha sido feita depois do G-26: não "esta guarda de canal
existe em todo lugar?" (já esgotada por F-19-F-21), mas "todo workflow que
nasceu do mesmo motivo que criou uma guarda também herdou a guarda?" —
achou que o F-21 (2.50) reproduz o par `Allow Re-entry` + compromisso de
ligação que motivou o F-04, sem o teto que o F-04 criou para esse par
exato. Fechado como **F-23** (acima, entre F-22 e G-25): nó de portão de
frequência (6c/6d) e a tag `toque` acrescentados ao nó 6a da 2.50/W27,
mesmo tratamento que a 2.9.2/2.9.3 já dão ao teto batido. Zero campo, zero
tag, zero workflow novo, zero escrita no CRM: reaproveita `toque` (T-15) e
`Toques na semana` (C-26), correção de spec antes da publicação — não
depende de `APROVADO.md`. G-04 (peça 2), F-09, F-10, G-11 (item 1) e
G-19 continuam sendo as decisões sem prazo fixo que esperam o dono,
sem novidade nesta sessão.

**Reconferido em 27/09/2026 ~20:05 UTC, sessão automática seguinte — faltam
~15h25min para a janela abrir (segunda 28/09 08:30 `America/Sao_Paulo` =
11:30 UTC).** `git fetch` limpo. `Carlos Andrade` (`7ECnj1bSeEIm5P58Ifd9`)
segue `dnd: true`, tag `atraso-1a-tentativa` presente — protegido, nenhum
disparo. `opportunities_search-opportunity` confirma **64 oportunidades**,
mesma composição da leitura do G-29 (13 `NOVO LEAD`, 47 `CONECTAR`, 3
`NEGOCIAR`, 1 `REUNIÃO DE DIAGNÓSTICO`) — sem novidade no risco de prazo
fixo. Com o risco reconferido, a mesma reconferência de campos que fechou
G-27/G-28/G-29 achou um sétimo campo fora da lista, e desta vez fora do
padrão dos seis anteriores: não é campo criado à mão na tela de
qualificação, é o rastro de um recurso nativo (Voice AI/AI Employee do
HighLevel) que nenhum documento registra ter sido ligado nesta subconta.
Fechado como **G-30** (acima, entre G-29 e "Ordem sugerida"): registro do
achado, sem decisão — mesmo padrão do G-27/G-29, campo do dono, não meu.
G-04 (peça 2), F-09, F-10, G-11 (item 1), G-19, G-27/G-28, G-29 e G-30
continuam sendo as decisões sem prazo fixo que esperam o dono, sem
novidade além do achado nesta sessão; G-25 segue como item de maior
prioridade do roadmap enquanto a janela não passar sem disparo.

**Achado de coerência na mesma sessão, antes de fechar: `G-03` tinha
voltado à lista de decisões pendentes em cinco parágrafos depois de ter
saído dela.** A reconciliação de 27/09/2026 (acima, "G-03 já saiu desta
lista — decidido e agendado para 29/09/2026") tirou o G-03 corretamente
nos parágrafos do F-19/F-20 ("cinco decisões"), mas os parágrafos
seguintes — F-21, F-22, F-23 e a frase de prioridade do G-25 — reintroduziram
`G-03, ` no início da mesma lista e voltaram a contar "seis", sem nenhuma
decisão nova do dono sobre ele: cópia do parágrafo anterior sem checar se
a lista que estava sendo copiada ainda era a correta, a mesma classe de
erro que motivou o G-20 (número fixo fora da fonte vence de novo quando a
fonte muda) — aqui a fonte não é um número, é a própria lista, e ela tinha
mudado sem que o padrão de "copiar o parágrafo anterior e trocar o item
novo" percebesse. Corrigido nos quatro parágrafos (a frase de prioridade do
G-25 e F-21/F-22/F-23): `G-03` removido, e o número fixo (`seis`/`cinco`)
trocado por "as decisões sem prazo fixo", sem contagem — a mesma escolha
já usada no parágrafo de reconciliação e nesta entrada do G-30, para o
mesmo tipo de erro não se repetir sozinho na próxima vez que a lista mudar
de tamanho. Nenhum outro documento deste projeto cita essa lista com
número fixo (`grep -rn "seis decisões\|cinco decisões" wesales/*.md`
aponta só para este arquivo, todas as ocorrências fora da faixa 27/09
sendo histórico de datas anteriores, legítimo). Zero campo, zero tag, zero
escrita no CRM: coerência de documentação.

**G-25 fechado em 27/09/2026 ~21:05 UTC, sessão automática seguinte —
seguindo a própria instrução deste roadmap ("a próxima sessão confere
primeiro se a janela mudou... antes de qualquer outro trabalho").**
`contacts_get-contact` em `Carlos Andrade` (`7ECnj1bSeEIm5P58Ifd9`) — a
mesma leitura que confirmava "protegido" em toda rodada desde a abertura do
item — voltou `dnd: false` (era `true`) e `Prioridade` `= 4`,
`dateUpdated` `21:04:39Z`. Amostrados mais 13 dos 30 contatos da lista
"Recebe DND" de `ABERTURA.md`: todos com o mesmo par, todos com
`dateUpdated` entre 21:04:39 e 21:04:50 UTC — uma escrita em lote. A causa
não é deste branch (lido `faxina_tarefas.py` por completo: nunca toca
`dnd`) — é a branch `abertura-operacao-dnd-n7dnjv`, com sessão de navegador
logado ativa desde 27/09 01:27 UTC, que o dono usou para decidir, ao vivo,
soltar os 31 contatos protegidos (`dnd = false`) e deixar a `Prioridade`
(recalculada para 4) governar o ritmo — não fechar a janela `days` do
workflow como este item previa. Detalhe completo, a citação do
`DE-PARA-SESSOES-CRM.md` daquela branch e o achado maior (quatro branches
escrevendo na mesma subconta sem se cruzarem, ~10h de G-25 "prioritário"
depois de já resolvido do outro lado) estão no próprio G-25 e no novo
**G-31**, ambos acima. Pronto quando cumprido: a decisão do dono
(verificada por leitura independente, não suposta) responde ao critério
original. G-04 (peça 2), F-09, F-10, G-11 (item 1), G-19, G-27/G-28, G-29 e
G-30 continuam sendo as decisões sem prazo fixo que esperam o dono; G-31
(branches paralelas) também espera decisão do dono, sem prazo fixo. Nenhum
item "salta a fila" agora — a sessão seguinte volta à varredura de
coerência ou à pesquisa de concorrência normais.

**G-33 fechado em 27/09/2026, sessão automática seguinte — aplicando o
próprio aviso do parágrafo acima ("volta à varredura de coerência") ao
alvo que o G-31/G-32 já tinham mostrado ser produtivo: a lista de decisões
pendentes deste roadmap, não um campo novo.** `git branch -a` +
`DE-PARA-SESSOES-CRM.md` da branch `abertura-operacao-dnd-n7dnjv`
(atualizado 27/09 20:50, depois da leitura que fechou o G-32) mostram que
dois dos itens desta lista já estavam resolvidos do outro lado, um deles
publicado e relido, o outro por um fato já lido (não por recomendação
ainda em aberto): **G-04 (peça 2)** fechou porque `Pós-agendamento v2`
(v17→v18) ganhou ramos por igualdade exata para os valores que o Meta
grava fora da lista de opções — uma terceira saída, nem a Opção A nem a B
que o item previa; **G-30** fechou porque a sessão A confirmou **zero
agentes de Voice AI ativos** na conta, então o campo fica inerte, sem
decisão de negócio pendente. Detalhe completo, a ressalva de método (só o
que é verificável por API nesta sessão foi confirmado por conta própria; o
resto é relato da outra branch, mesmo padrão do G-32) e a recomendação
ainda sem confirmação do dono para G-27/G-29 (diferente das duas linhas
fechadas: aquela é pedido, não fato) estão no próprio **G-33**, acima. CRM
reconfirmado sem mudança (64 oportunidades, 60 campos de contato — os
mesmos do fechamento do G-32). Com isso, **F-09, F-10, G-11 (item 1), G-19,
G-27/G-28, G-29 e G-31 são as decisões sem prazo fixo que esperam o dono**
— sete, duas menos que antes deste fechamento, e G-27/G-29 com uma
recomendação registrada que ainda não é resposta. Nenhum item "salta a
fila": a sessão seguinte volta à varredura de coerência ou à pesquisa de
concorrência normais, como o parágrafo do G-31 já previa.

**G-34 fechado em 28/09/2026, sessão automática seguinte — sem parágrafo
próprio nesta seção até agora (lacuna desta mesma lista, não deste
fechamento).** Relendo o `DE-PARA-SESSOES-CRM.md` da sessão A linha a
linha, o G-33 tinha juntado três números (`G-27/G-28/G-29`) numa frase só
de "recomendação, ainda sem confirmação" — mas a fonte separava dois
grupos: `G-25/G-26/G-28/G-30` já resolvidos pela decisão ao vivo do dono, e
só `G-27/G-29` de fato pendentes. Corrigido: G-28 sai da lista de decisões
sem prazo fixo. Detalhe completo no próprio **G-34**, acima. Com isso,
**F-09, F-10, G-11 (item 1), G-19, G-27/G-29 (recomendação ainda sem
confirmação) e G-31** são as decisões sem prazo fixo que esperam o dono —
seis, uma a menos que a lista do G-33.

**G-35 fechado em 28/09/2026, sessão automática seguinte — CRM
reconfirmado sem mudança (56 campos de contato); `Carlos Andrade` e a
amostra dos 31 contatos do G-25 seguem `dnd: false` + `Prioridade: 4`,
nenhuma mensagem automática nova saiu ainda (janela da MI-0 abre 11:30 UTC
hoje, ~10h15min a esta sessão) — sem novidade no risco de prazo fixo, que
segue fechado.** A varredura de coerência desta vez não mirou nome de
campo, tag ou número somado — mirou uma citação a **estado do GitHub**
(não CRM, não `git log`), o único tipo de fato que nenhuma reconfirmação
de rotina deste projeto tinha voltado a checar depois de escrito. `G-19`
citava "PR #93" três vezes como o PR cujo merge dispararia o risco do
`checkout` pinado no `faxina-tarefas.yml` — `pull_request_read` (GitHub)
mostra que o #93 fechou **sem merge** em 24/09/2026, um dia depois de a
instrução ter sido escrita, e nunca vai mesclar; nenhuma rodada entre
24/09 e hoje notou. O PR de fato aberto para esta branch hoje é o
**#102** (`search_pull_requests`, criado 27/09/2026, ainda `open`, mesmo
par base/head do #93). Corrigidas as três citações correntes em `G-19` e
na instrução de "próxima rodada" logo após seu fecho, para não fixarem
número de PR de novo — apontam para "o PR aberto desta branch",
verificável a qualquer momento. Detalhe completo no próprio **G-35**,
acima. G-19 continua aberto (decisão do dono + fora de `wesales/`); F-09,
F-10, G-11 (item 1), G-27/G-29 e G-31 continuam sendo as decisões sem
prazo fixo que esperam o dono, sem mudança nesta rodada. Nenhum item
"salta a fila": a sessão seguinte volta à varredura de coerência ou à
pesquisa de concorrência normais.

**F-24 aberto e fechado em 28/09/2026, sessão automática seguinte —
seguindo exatamente essa instrução (pesquisa de concorrência, já que o
sweep de coerência de sempre não achou nada novo em texto).** CRM
reconfirmado por API antes de desenhar: 64 oportunidades, mesma composição
de sempre; 60 campos de contato (`Canal da tentativa`/G-32 e `Voice AI
Reason for Call`/G-30 já contavam, nenhum campo novo fora da lista desta
vez) — G-19 continua aberto (decisão do dono, fora de `wesales/`); F-09,
F-10, G-11 (item 1), G-27/G-29 e G-31 continuam sendo as decisões sem
prazo fixo que esperam o dono, sem mudança. A lacuna veio de aplicar a
pergunta do F-19/F-20/F-21 ("o que Reev/Meetime/Outreach/Salesloft cobrem
que este item ainda não cobre") ao próprio conjunto de sinais do F-01, não
a uma guarda de canal — e achar que abertura/clique de e-mail, sinal que
Outreach/Salesloft pontuam há anos, nunca foi lido por nenhum workflow
deste projeto. Fechado como **F-24**: dois workflows especificados nó a nó
(`build-wesales.md`, seção 2.55), campo `Pontos de engajamento e-mail`
(C-34) e tag `email-engajado` (T-24) especificados em `campos-e-tags.md`,
ambos nascendo `[ ]` em `APROVADO.md` pela regra de sempre;
`IMPLEMENTACAO-WORKFLOWS.md` (W28/W29) e `GUIA-MONTAGEM.md` atualizados no
mesmo commit. Desenhado de propósito para não repetir o erro que o F-19 já
ensinou (tratar todo sinal automático como sinal quente): só o clique
escalona, só uma vez por contato, nunca a abertura sozinha — e não herda o
teto de toques do F-04/F-23 porque não cria toque nenhum, só reordena a
fila que já existe. Zero campo, zero tag, zero escrita no CRM nesta
rodada.

**F-25 aberto e fechado em 28/09/2026, sessão automática seguinte — a
mesma pergunta de concorrência aplicada não a um sinal (F-24), mas à
higiene de base que o R-13 nunca estendeu ao e-mail.** CRM reconfirmado
por API antes de desenhar: 64 oportunidades, 60 campos de contato, sem
mudança — F-09, F-10, G-11 (item 1), G-27/G-29 e G-31 continuam sendo as
decisões sem prazo fixo que esperam o dono; G-19 continua aberto (decisão
do dono, fora de `wesales/`). A lacuna veio de perguntar ao R-13 ("base
suja infla métrica e queima SDR") a mesma pergunta que já tinha sido feita
a outras guardas mais velhas: ele cobre telefone (`telefone-invalido`,
T-09) desde 18/09/2026, mas o e-mail só ganhou disparo real quatro dias
depois (F-15) e nunca ganhou o par. Fechado como **F-25**: workflow
"Higiene de E-mail — Bounce" especificado nó a nó (`build-wesales.md`,
seção 2.56), reagindo ao gatilho nativo `Email Events`/`Bounced` que a
pesquisa confirmou existir (a própria HighLevel publica a receita —
`Email Events` → `Bounced` + DND escopado a `Outbound Email`); campo
`Bounces de e-mail` (C-35) e tag `email-invalido` (T-25) especificados em
`campos-e-tags.md`, ambos nascendo `[ ]` em `APROVADO.md`;
`IMPLEMENTACAO-WORKFLOWS.md` (W30) e `GUIA-MONTAGEM.md` atualizados no
mesmo commit. Desenhado para não repetir dois erros já vistos neste
roadmap: reaproveitar `nao-perturbe`/DND-em-todos-os-canais (como o
2.9.5/R-17) confundiria a auditoria de compliance do R-14 e pararia
telefone/WhatsApp por um motivo que é só do e-mail — por isso tag e DND
próprios, escopados ao canal; e tratar bounce como binário definitivo, que
a própria fonte da receita nativa desaconselha ("nem todo bounce é
permanente") — por isso o item avisa o gestor em vez de decidir sozinho
que o endereço morreu para sempre. Zero campo, zero tag, zero escrita no
CRM nesta rodada.

**F-26 aberto e fechado (especificação) em 28/09/2026, sessão automática
seguinte — antes de desenhar, reconferido se algum item "aguardando o
dono" já tinha resposta do outro lado (hábito do G-31/G-32/G-33): `git
fetch` nas branches irmãs (`abertura-operacao-dnd-n7dnjv`,
`abertura-operacao-dnd-ib6xaz`) e leitura do `DE-PARA-SESSOES-CRM.md` da
primeira (até 28/09 00:54) não achou resposta nova para F-09, F-10, G-11
(item 1), G-19 ou G-31 — só reforçou o G-29 (recomendação registrada,
ainda sem confirmação). CRM reconfirmado por API sem mudança: 64
oportunidades, 60 campos de contato (`SDR responsável` ainda só com
`Andreyna Siqueira`, `B · Quanto pode investir` sem consumidor — mesmo
estado do G-29/G-34).** Sem achado de reconciliação, a sessão foi à
pesquisa de concorrência de sempre (mesma pergunta do F-07/F-08/F-14: "o
que Reev/Meetime/Outreach/Salesloft protegem ou automatizam que este
projeto ainda não cobre") — achou que `Caixa Postal`/`Não atendeu`
(ramo idêntico, seção 4) nunca deixa mensagem nenhuma, e o GHL já tem
`Ringless Voicemail (Voicemail Drop)` nativo para isso. Fechado como
**F-26**: nós 5-9 do ramo, tag `voicemail-enviado` (T-26) e campo
`Voicemails automáticos` (C-36), ambos `[ ]` em `APROVADO.md`. Diferente
dos F-anteriores, este nasce com uma trava própria: o mesmo mecanismo soma
chamada extra no canal que F-08/F-14 já mediram perto do limite seguro, e
o item registra essa conta (~20-40 chamadas extras/dia) em vez de
recomendar ativação imediata — dependência explícita do F-09 em cinco
documentos (`APROVADO.md`, `campos-e-tags.md`, `build-wesales.md`,
`IMPLEMENTACAO-WORKFLOWS.md`, `GUIA-MONTAGEM.md`). F-09, F-10, G-11 (item
1), G-19, G-27/G-29 e G-31 continuam sendo as decisões sem prazo fixo que
esperam o dono, sem mudança nesta rodada.

**F-27 aberto e fechado (especificação) em 28/09/2026, sessão automática
seguinte — reconciliação de sempre antes de desenhar (hábito do
G-31/G-32/G-33/F-26): `git fetch` nas branches irmãs
(`abertura-operacao-dnd-n7dnjv`) e leitura do `DE-PARA-SESSOES-CRM.md`
(atualizado até 28/09 ~01:27 UTC, turnos flexíveis/comissão) não achou
resposta nova para F-09, F-10, G-11 (item 1), G-19 ou G-31 — só confirmou
de novo o estado do G-27/G-29 (`SDR responsável` e `B · Quanto pode
investir` ainda sem workflow lendo). CRM reconfirmado por API sem mudança
de estrutura: 64 oportunidades, 60 campos de contato.** Sem achado de
reconciliação, a sessão foi à pesquisa de concorrência de sempre — desta
vez não a um sinal ou a uma guarda de canal (já esgotados por F-19-F-26),
mas ao próprio nó 1 da seção 2.27 (F-06), que descarta toda chamada
`Inbound` numa frase só sem que nenhum outro item do projeto tivesse
voltado a essa linha desde então. Achou que o cenário mais provável de uma
chamada `Inbound` nesta subconta — o lead retornando uma tentativa de
telefone da própria régua enquanto o Power Dialer discava outro número —
cai no vácuo, e que o GHL trata o "Missed Call Text-Back" como sua própria
automação de maior ROI, um caso que nem Reev nem Meetime cobrem por não
serem operadora de telefonia. Fechado como **F-27**: workflow "Retorno de
Chamada Perdida" (gatilho nativo `Call Status`, Direção `Inbound`),
priorizando o lead e criando tarefa sem depender de campo ou tag nova —
só uma 4ª opção em `Sinal recebido` (C-13, mesma classe do F-21) fica
pendente de tela. `IMPLEMENTACAO-WORKFLOWS.md` (W31), `campos-e-tags.md`
(C-13), `APROVADO.md` (linha nova, `[ ]`) e `GUIA-MONTAGEM.md` atualizados
no mesmo commit. F-09, F-10, G-11 (item 1), G-19, G-27/G-29 e G-31
continuam sendo as decisões sem prazo fixo que esperam o dono, sem
mudança nesta rodada.

**F-28 aberto e fechado em 28/09/2026, sessão automática seguinte —
reconciliação de sempre antes de desenhar (hábito do G-31/G-32/G-33/F-26/
F-27): `git fetch` na branch irmã `abertura-operacao-dnd-n7dnjv` (atualizada
28/09 ~02:53 UTC, ~11 min antes desta sessão) e leitura de
`DE-PARA-SESSOES-CRM.md` não achou resposta nova para F-09, F-10, G-11
(item 1), G-19 ou G-31 — só reconfirmou G-27/G-29 (`SDR responsável` e
`B · Quanto pode investir` seguem sem workflow lendo, recomendação
registrada, sem confirmação). `opportunities_search-opportunity` (status
`all`) confirma 64 oportunidades, mesma composição de sempre;
`locations_get-custom-fields` confirma os campos de contato sem novidade —
C-15/C-16/C-17 (`Reunião foi qualificada`/`Motivo da desqualificação`/`Data
do veredito do closer`) já criados na tela (contagem exata em
`campos-e-tags.md`).** Sem achado de reconciliação, a sessão foi à
pesquisa de concorrência — mas desta vez não repetiu a pergunta já esgotada
sobre guarda de canal/sinal (F-19 a F-27): aplicou a mesma pergunta aos dois
pilares do bloco 6 que nunca tinham ganhado extensão, F-02 (horário
aprendido) e F-03 (loop do closer), e achou que o próprio "Pronto quando" do
F-03 — "dá pra dizer nota ≥ 70 acerta X%" — nunca foi calculado: o alerta em
tempo real do 5.1 resolve o caso isolado, nenhum lugar soma ao longo do
tempo. Fechado como **F-28**: script só-leitura
`wesales/tools/calibracao_regua.py` (zero escrita no CRM, não depende do
`APROVADO.md`), rodado nesta mesma sessão contra a subconta real via MCP (sem
`GHL_TOKEN` neste ambiente) — achou **zero vereditos reais** hoje, e que o
único veredito existente na subconta é do contato de teste "9940" (mesmo
contato do G-23), que o script exclui por ID fechado **e** por heurística de
nome/e-mail. Sem essa exclusão o relatório mentiria já na primeira leitura
(nota 23, veredito `Sim`, pareceria o pior caso de descalibração). Primeira
leitura real gravada em `wesales/RELATORIO-CALIBRACAO.md`, com nota de
proveniência explicando o caminho MCP em vez de `GHL_TOKEN`. Zero campo, zero
tag, zero escrita no CRM: reaproveita C-15 a C-17. F-09, F-10, G-11 (item 1),
G-19, G-27/G-29 e G-31 continuam sendo as decisões sem prazo fixo que
esperam o dono, sem mudança nesta rodada.

**G-36 fechado em 28/09/2026, sessão automática seguinte — o F-29 tinha
fechado sem o parágrafo de recapitulação que esta seção espera (detalhe
completo no próprio `### G-36`, corpo do Bloco 6, logo após o F-29).**
Reconciliação de sempre sem novidade: `git fetch` nas duas branches irmãs
não achou nada além do que o F-29 já tinha lido; CRM reconfirmado por API
sem mudança (64 oportunidades, 60 campos de contato). F-09, F-10, G-11
(item 1), G-19, G-27/G-29 e G-31 continuam sendo as decisões sem prazo
fixo que esperam o dono, sem mudança nesta rodada. Regra corrigida para a
próxima vez: o parágrafo de fechamento vale para qualquer prefixo (`F-`,
`G-`, `R-`) que altere esta lista ou feche citando "sem mudança nesta
rodada" — não só para `G-`, que era a única família em que a regra tinha
sido testada quando o G-24 a escreveu (`APRENDIZADOS-CRM.md`).

**F-30 aberto e fechado (especificação) em 28/09/2026, sessão automática
seguinte — reconciliação de sempre antes de desenhar, seguindo a própria
regra do G-36 acima (o parágrafo de fechamento vale para qualquer prefixo):**
`git fetch` nas duas branches irmãs (`abertura-operacao-dnd-n7dnjv`,
atualizada 28/09 ~02:53 UTC, mesmo commit que o F-29/G-36 já tinham lido;
`abertura-operacao-dnd-ib6xaz`, sem commit novo desde 27/09 18:03 UTC — o
único commit dela é de outro projeto deste repositório, fora de `wesales/`)
não achou resposta nova para F-09, F-10, G-11 (item 1), G-19, G-27/G-29 ou
G-31. CRM reconfirmado por API antes de desenhar: `opportunities_search-
opportunity` segue em 64 oportunidades, mesma composição; `locations_get-
custom-fields` segue em 60 campos de contato, sem novidade (`SDR
responsável` ainda só com `Andreyna Siqueira`, `Sinal recebido` ainda com
só duas das quatro opções que F-21/F-27 já pediram). Sem achado de
reconciliação, a sessão foi à pesquisa de concorrência de sempre — desta
vez relendo o próprio F-19 (que já citava o filtro `Intent Type` do
gatilho `Customer Replied` sem usá-lo) em vez de comparar contra
Reev/Meetime/Outreach/Salesloft direto. A lacuna: a Interceptação de Sinal
(2.9.3/2.50) só exclui opt-out (R-17) e auto-resposta (F-19/F-20) — uma
recusa educada e genuína ("não tenho interesse") ainda vira `Prioridade` =
5 e "ligar agora". Fechado como **F-30**: filtro nativo `Intent Type não é
Negative` acrescentado às duas Interceptações de Sinal (patch pendente na
2.9.3, já publicada; direto na especificação da 2.50, ainda não montada) e
workflow novo "Resposta com Intenção Negativa" cobrindo os três canais
desde o início (lição do F-19→F-20 aplicada de saída), tag
`resposta-negativa` (T-28) e campo `Respostas negativas` (C-38), ambos
nascendo `[ ]` em `APROVADO.md`. Duas pendências de confiança registradas,
não escondidas (mesmo padrão do F-06/F-29): se `Intent Type` classifica
tráfego `TYPE_CUSTOM_SMS` da Stevo, e o custo por execução do filtro — a
pesquisa não achou preço, e o domínio oficial (`gohighlevel.com`) segue
bloqueado pelo proxy deste contêiner para verificação ao vivo (mesmo
achado que `ABERTURA.md` já tinha registrado em 27/09/2026 para outro
fim). `IMPLEMENTACAO-WORKFLOWS.md` (W33) e `GUIA-MONTAGEM.md` atualizados
no mesmo commit. Zero campo, zero tag, zero escrita no CRM nesta rodada.
F-09, F-10, G-11 (item 1), G-19, G-27/G-29 e G-31 continuam sendo as
decisões sem prazo fixo que esperam o dono, sem mudança nesta rodada.

**F-31 aberto e fechado (especificação) em 28/09/2026, sessão automática
seguinte — reconciliação de sempre antes de desenhar, seguindo a regra do
G-36 (o parágrafo de fechamento vale para qualquer prefixo):** `git fetch`
nas duas branches irmãs não achou resposta nova para F-09, F-10, G-11
(item 1), G-19, G-27/G-29 ou G-31. CRM reconfirmado por API antes de
desenhar: `opportunities_search-opportunity` segue em 64 oportunidades,
mesma composição; `locations_get-custom-fields` segue em 60 campos de
contato, sem novidade. Sem achado de reconciliação, a sessão foi à
pesquisa de concorrência de sempre — desta vez não a um sinal, canal ou
conteúdo (esgotados por F-19 a F-30), mas à única lacuna de **execução**
que sobrava: a tabela do G-05 manda submeter 16 Templates ao Meta Business
Manager e nenhum documento dizia em qual categoria, escolha que vale 6× de
preço (referência de mercado) e expõe a um teto de frequência por
destinatário (`131049`) que nem o checklist de reputação do F-07 mede — um
número com Quality Rating perfeita ainda pode ter mensagem `Marketing`
descartada por saturação do **destinatário**, não da conta. Fechado como
**F-31**: os 16 códigos com categoria candidata, confiança e razão
(`build-wesales.md`, seção 2.61; coluna nova na tabela "Template Meta" de
`biblioteca-mensagens.md`), o caso mais incerto (`NS-1`) registrado como
incerto em vez de forçado, e o checklist do F-07 estendido com um quarto
hábito (distinguir, na tela nativa de Estatísticas do WhatsApp por
workflow, `Failed` por reputação de `Failed` por teto de frequência).
Zero campo, zero tag, zero workflow, zero escrita no CRM: item de
documentação pura, mesmo padrão do F-07/F-08, não depende de `APROVADO.md`.
F-09, F-10, G-11 (item 1), G-19, G-27/G-29 e G-31 continuam sendo as
decisões sem prazo fixo que esperam o dono, sem mudança nesta rodada.

**G-37 fechado em 28/09/2026, sessão automática seguinte — pegando o item de
maior prioridade ainda aberto (instrução desta rodada), o próprio comando
que separa item fechado de item aberto (`grep -n "^### [FGR]-[0-9]"`) mentiu
sete vezes: F-18, F-19, F-20, F-21, F-24, F-25 e F-26 tinham o corpo
inteiro fechado (especificados nó a nó, cross-referenciados em
`build-wesales.md`, `campos-e-tags.md`, `IMPLEMENTACAO-WORKFLOWS.md` e
`GUIA-MONTAGEM.md`, cada um com parágrafo de fechamento já escrito nesta
mesma seção) mas o `### cabeçalho` nunca ganhou a marca `FEITO` que
F-07/F-22/F-23/F-27/F-29/F-30/F-31 carregam — mesma classe de lapso que o
G-24 e o G-36 já corrigiram, desta vez no outro lado do par (o cabeçalho,
não o parágrafo de fechamento). Corrigidos os sete: seis com `FEITO em
27/09/2026 (especificação)` ou `FEITO em 28/09/2026 (especificação)` — a
mesma data que o parágrafo de fechamento de cada um já registrava —, e o
F-18 com `especificação fechada em 27/09/2026, execução aguarda o primeiro
won`, porque este item é o único dos sete que esta própria seção já dizia
esperar um evento real, não decisão do dono. Sem essa distinção, o F-18
teria ganhado `FEITO` como os outros seis e o roadmap passaria a afirmar
uma entrega que o próprio texto, três parágrafos acima, já negava. Detalhe
completo, inclusive a regra nova para a próxima rodada, no próprio
`### G-37`, acima. CRM reconfirmado sem mudança (64 oportunidades, 60
campos de contato). Zero campo, zero tag, zero escrita no CRM. Sem item de
`APROVADO.md` para marcar `[x]` nesta rodada — a fila do dono
(`APROVADO.md`) segue igual à da última leitura. F-09, F-10, G-11 (item 1),
G-19, G-27/G-29 e G-31 continuam sendo as decisões sem prazo fixo que
esperam o dono, sem mudança nesta rodada.

**F-32 aberto e fechado (especificação) em 28/09/2026, sessão automática
seguinte — reconciliação de sempre antes de desenhar (hábito do
G-31/G-32/G-33/F-26 em diante): `git fetch` nas duas branches irmãs sem
resposta nova para F-09, F-10, G-11 (item 1), G-19, G-27/G-29 ou G-31. CRM
reconfirmado por API direto nesta sessão (sem `GHL_TOKEN` neste ambiente,
mesmo caminho do F-28): `opportunities_search-opportunity` sobe de 64 para
**66** (2 leads novos de verdade, incluindo um durante a própria sessão);
`locations_get-custom-fields` segue em 60 campos de contato, sem
novidade.** Em vez de ir direto à pesquisa de concorrência, a sessão
releu o próprio F-02 (por que ele nunca fechou por inteiro) e conferiu por
dado, não por suposição, se a premissa "`Segmento` normalmente já vem
preenchido" (`script-de-ligacao.md`) se sustenta: 17 contatos reais lidos
por `contacts_get-contact`, 0 com `Segmento` preenchido — e nenhum dos 8
formulários do Meta que o G-04 já mapeou grava nesse campo. A lacuna veio
de olhar o `attributionSource.utmMedium` que a própria API já trazia: as
campanhas mais novas ("Fase 3") nomeiam o nicho no próprio texto ("LEADS I
NICHO ADVOCACIA BR I FASE 3", "... CONTABILIDADE ..."), e nada neste
projeto lê isso. Fechado como **F-32**: nós 0.8/0.8b especificados dentro
do nó de inicialização já existente da `Cadência 12x30` (seção 2.3/2.62 do
`build-wesales.md`, não um workflow novo), usando o `If/Else` nativo do
GHL sobre UTM Medium (First Attribution) com `Contains` — pesquisado
(`WebSearch`, confiança média, mesma ressalva de proxy bloqueado do
F-06/F-08/F-29/F-30) e confirmado por changelog oficial indexado que o
campo existe como condição de verdade, não só merge field. Dois limites
registrados, não escondidos: campanha de segmentação ampla não tem nicho
para extrair (comportamento esperado, não falha), e o rótulo da campanha é
candidato — o caso `Ana Ruth`/"NICHO CONTABILIDADE" já mostrou que o
anúncio pode mirar errado; o campo continua editável pelo SDR na ligação.
Zero campo novo, zero tag nova: reaproveita `Segmento` (Q-01), existente
desde 18/09/2026 — não depende de `APROVADO.md`. `campos-e-tags.md` (Q-01),
`script-de-ligacao.md` (seção 1) e `IMPLEMENTACAO-WORKFLOWS.md` (W11)
atualizados no mesmo commit. F-09, F-10, G-11 (item 1), G-19, G-27/G-29 e
G-31 continuam sendo as decisões sem prazo fixo que esperam o dono, sem
mudança nesta rodada.

### G-38 · A premissa "100% telefone, 12 de 12" do F-09 venceu em produção — o próprio dono já mudou a distribuição de canal em código, numa branch irmã, sem passar por este roadmap nem por `APROVADO.md` (28/09/2026) — **FEITO em 28/09/2026 (reconciliação)**

**Por quê:** pegando o item de maior prioridade ainda aberto desta rodada
(instrução desta execução), a reconciliação de sempre veio primeiro —
hábito que G-31 deixou e G-32/G-33/G-34/G-35 já aplicaram: `git fetch` nas
branches irmãs antes de desenhar qualquer coisa nova. `abertura-operacao-
dnd-n7dnjv` tinha um commit novo desde a última leitura (`58f3e07`/`69e034a`,
o mesmo conteúdo chegou também a `claude/stoic-hawking-tlxjtf`, a branch
onde o PR #118 foi mesclado) — e, diferente de toda reconciliação anterior
deste roadmap, o autor não é uma sessão automática: é `Pablo Sampaio
<sampaioopablo@gmail.com>`, o próprio dono, escrevendo `atuador_filas.py`
direto. O commit muda exatamente o ponto que o F-09 discute: a régua deixa
de ser 100% telefone (12 de 12 toques, decisão `d52e61d` de 22/09/2026) e
passa a intercalar telefone (toques 1,3,5,7,9,11,12 — **7 de 12**) com
ligação de WhatsApp (toques 2,4,6,8,10 — **5 de 12**), com leads antigos
entrando pela metade que a paridade do próprio ID escolhe. Conferido por
API, não só pelo diff do código: `locations_get-custom-fields` mostra os
campos `Canal da tentativa` (`AsZMGmsKVu1xEp36hyLb`, já registrado no G-32
como peça de um "redesenho do seletor de canal — o mesmo ponto que o F-09
discute") e `Canal que conectou` (`TxJmoWdkA8rTqC1uEsMW`, já registrado no
G-21) vivos na subconta real, com as opções exatas que o script grava —
não é plano, é o que já está rodando. `opportunities_search-opportunity`
confirma **66 oportunidades** (`meta.total`, não a contagem de itens da
página), 2 a mais que a última leitura registrada neste arquivo (F-32).

**Como:** não há nada para "aplicar" — a mudança já é fato consumado na
operação real, fora do que este conector ou `APROVADO.md` governam (o
próprio G-31 já tinha registrado que decidir qual branch é fonte de
verdade, ou consolidar as branches, é escolha do dono, não desta sessão).
O que esta rodada faz é o que a reconciliação sempre fez desde o G-32:
atualizar o item que a mudança afeta para não deixar uma decisão pendente
apoiada em número que já não é real. Corrigido dentro do próprio `### F-09`
(banner "Correção de 28/09/2026", acima): a tabela de opções A/B/C não
muda — o limiar de corte continua decisão do dono — mas a conta que a
coluna "Efeito" fazia sobre "12 toques de telefone" passa a valer para 7,
intercalados com WhatsApp, não seguidos. Não mexi na tabela em si (decidir
o número da opção não é desta sessão); só no texto que a contextualiza,
para quem for decidir não decidir sobre um cenário que não existe mais.

**O que este achado não é:** não é o dono escolhendo A, B ou C — a régua
continua sem freio de "não atendidas seguidas" nenhum, só ficou mais curta
por fora dele. Também não é motivo para fechar F-09: a exposição
regulatória que o abriu (Despacho 82/2026/RCTS/SRC, F-08) segue valendo
para os 7 toques de telefone que restam. E não é um caso novo de campo
órfão (G-27/G-29/G-30) — os dois campos que a API confirma já tinham
explicação registrada antes de hoje (G-21, G-32); o que faltava registrar
era que o *comportamento* que eles alimentam já mudou a régua de verdade,
não só o vocabulário do dado.

**Nota sobre o resto da documentação, sem tentar resolver tudo numa
rodada só:** `grep -rn "100% telefone\|12 de 12"` em todo o `wesales/`
acha a mesma premissa em pelo menos nove outros arquivos (`APROVADO.md`,
`build-wesales.md`, `GUIA-MONTAGEM.md`, `APRENDIZADOS-CRM.md`,
`ESTADO-E-PLANO.md`, `AGENTE-IA-CONEXAO.md`, além de outras menções neste
próprio roadmap). Nenhum deles está "errado" no sentido de descrever mal a
especificação que motivou — `build-wesales.md` e `GUIA-MONTAGEM.md`
continuam descrevendo corretamente a `Cadência 12x30` **como este roadmap a
especificou**, o workflow nativo do GHL que ainda não foi publicado na
tela. A divergência é que a operação real, na branch irmã, não está
rodando essa especificação: está rodando `atuador_filas.py`, um mecanismo
por tag e cron que faz uma coisa parecida por fora do GHL nativo — o mesmo
tipo de descolamento entre "documento medido" e "documento rastreado" que
G-16/G-17/G-19/G-21 já mediram para outros pontos. Reescrever os nove
arquivos para uma premissa que só vale para metade da operação (a metade
que ainda não foi publicada) trocaria uma verdade parcial por outra —
por isso esta rodada corrigiu só o item que a decisão do dono afeta
diretamente (F-09) e registrou aqui, para a próxima sessão que for mexer
em qualquer um dos nove não redescobrir sozinha por que o número não bate
mais com a tela. Zero campo, zero tag, zero escrita no CRM: item de
reconciliação entre branches e de coerência de premissa, não depende de
`APROVADO.md`.

**Pronto quando:** cumprido nesta rodada para o item que a mudança afeta
(F-09) — os outros nove arquivos ficam registrados como pendência
conhecida, não como trabalho represado: eles descrevem a especificação
correta para quem for publicar a `Cadência 12x30` na tela, e só precisam
de correção se o dono decidir que a operação real (branch A) é a fonte de
verdade daqui para frente, a mesma escolha (a) vs. (b) que o G-31 já
colocou para ele. F-09, F-10, G-11 (item 1), G-19, G-27/G-29 e G-31
continuam sendo as seis decisões sem prazo fixo que esperam o dono — a
mudança desta rodada não tira nem acrescenta nenhuma à lista, só atualiza
o cenário que uma delas (F-09) descreve. CRM reconfirmado por API antes de
fechar: 66 oportunidades, 60 campos de contato (`locations_get-custom-
fields`, `query_model=contact`), sem novidade além do já registrado acima.

### G-39 · T-17 (`fila-travada`) já está publicada e em uso — o documento dizia "não criada ainda" para uma tag que 5 de 5 leads reais conferidos já carregavam, com um relógio diferente do especificado (28/09/2026) — **FEITO em 28/09/2026 (reconciliação)**

**Por quê:** pegando o item de maior prioridade ainda aberto desta rodada,
a reconciliação de sempre veio primeiro (hábito do G-31 em diante): `git
fetch` nas branches irmãs antes de desenhar qualquer coisa nova. A única
com commit novo desde a última leitura (G-38) foi `abertura-operacao-dnd-
n7dnjv` (`a1ca792`, do próprio dono, 9 linhas em `DE-PARA-SESSOES-CRM.md`
sobre visão de Contatos/Conversas para WhatsApp — achado sem consequência
para nenhuma das seis decisões sem prazo fixo). Sem novidade aí, a sessão
reconfirmou o CRM por API (`opportunities_search-opportunity`: 66
oportunidades, mesma composição; `locations_get-custom-fields`: 60 campos
de contato, sem campo novo) e foi à releitura de premissa técnica que este
roadmap sempre recomenda quando reconciliação e CRM não acham nada
("reler os itens represados... a razão de esperar pode ter vencido sem
ninguém notar") — desta vez não um campo represado, mas o próprio F-02
(horário aprendido por segmento), para conferir se a "0 conexões reais"
que o bloqueia desde 19/09/2026 ainda é verdade. Não era mais só isso: ao
puxar 5 contatos reais em `CONECTAR` (Carlos Andrade, Gerson De Souza Pia,
Andreia, Wesley, Edson — `contacts_get-contact`, um a um, não a listagem
que atrasa) para checar `Hora da conexão` (C-25, segue vazio nos 5,
F-02 continua bloqueado) e `Segmento` (Q-01, também vazio nos 5, F-32
segue sem consumidor), os 5 traziam uma tag que nenhum documento deste
projeto cita: `fila-travada` — que **é** T-17, a tag que `campos-e-tags.md`
e `APROVADO.md` descreviam como "aguardando aprovação, não criada ainda".

**Como:** confirmado que não é falso positivo nem homônimo — a branch irmã
`abertura-operacao-dnd-n7dnjv` tem um arquivo que este roadmap ainda não
tinha lido, `DISCADOR-CONFIG-POR-FUNCAO.md`, e ele descreve o mecanismo
publicado: "O `Fila Travada` vigia `fila-tel`: se a tag ficar 8 h sem
resultado, avisa o gestor e põe `fila-travada`." É o mesmo T-17 (mesmo
nome de tag, mesmo propósito — avisar que uma tentativa ficou parada), com
um relógio **diferente** do que a especificação original (F-05, peça 2,
`build-wesales.md` seção 2.21) previa: **8 horas corridas desde a tag de
fila**, não "depois do fim do dia em que foi aplicada" (o relógio fixo às
19:00 que o nó 1 da seção 2.21 descreve) — mesma classe de divergência que
o G-23 já mediu para T-21 (5 dias vs. 3) e T-22. Um dos cinco contatos
(Carlos Andrade) tinha `fila-wa` presente junto com `fila-travada`, não só
`fila-tel` — evidência a favor de o relógio publicado vigiar os dois
canais como o desenho original propunha, mas o `DISCADOR-CONFIG-POR-
FUNCAO.md` só descreve `fila-tel` por extenso; registrado como indício, não
como confirmação, para a próxima rodada não tratar como fechado o que
ainda é leitura indireta (nenhum dump de workflow foi lido, o MCP não
expõe workflow). Corrigidos `campos-e-tags.md` (título da Etapa 3, o
parágrafo de contagem, a linha da T-17 e o parágrafo de fechamento — T-17
sai do grupo "nasce `[ ]` e ainda não saiu por API" e entra no grupo do
T-21/T-22, "já criada e publicada, dono não seguiu a fila do `[x]`") e
`APROVADO.md` (nota de registro sob a linha da T-17, mesmo padrão do
T-21/T-22 — **`[x]` não marcado**, regra 1 e a regra "Como autorizar" do
próprio arquivo).

**A mesma varredura trouxe uma segunda tag sem dono, menor, junto:**
`sem-cadencia`, presente nos 5 contatos junto com `fila-travada`. Também
sem nenhuma linha em `wesales/*.md` antes de hoje (`grep -rn` vazio), mas
com explicação de primeira na mesma branch irmã (`DE-PARA-SESSOES-CRM.md`):
marca os 36 leads que entraram entre 19 e 21/09/2026, antes de a Cadência
Inbound existir, e por isso nunca receberam `fila-tel` pela via normal — o
atuador da branch irmã os resgata aplicando `fila-tel` 1×/dia até 12
tentativas, sem WhatsApp automático (decisão do dono), e a tag some quando
o lead entra de fato na Cadência Inbound. Não é órfã nem bug: é rede de
resgate para quem ficou para trás de uma mudança de desenho, mesma classe
do achado de `Canal da tentativa` no G-32. Registrada em `campos-e-tags.md`
junto com as outras tags fora da numeração (agora 13, era 12) — a conta
tem hoje **31** tags no total (18 numeradas criadas + 13 fora da
numeração), não mais 29; os dois números corrigidos nos três lugares que
os citam (`campos-e-tags.md`, único dono da contagem — regra do próprio
arquivo).

**O que este achado não é:** não é uma nova decisão pendente do dono — T-17
já está resolvida (publicada, em uso), só o registro estava desatualizado.
Não é motivo para reabrir F-05 (a peça 2 continua "FEITO", o documento é
que mentia sobre o estado da tela). E não é confirmação de que F-02 ou
F-32 estão perto de destravar: os dois campos que eles precisam (`Hora da
conexão`, `Segmento`) seguem vazios na amostra real conferida — a operação
ao vivo roda por fora do `build-wesales.md`/`Cadência 12x30` nativa (o
mesmo descolamento que o G-38 já registrou, `atuador_filas.py` em vez do
workflow nativo), então os campos que só a `Cadência 12x30` publicada
escreveria continuam sem consumidor nenhum enquanto essa branch for a
operação real.

**Pronto quando:** cumprido nesta rodada — os três documentos que contam
tag (`APROVADO.md`, `campos-e-tags.md`, e este roadmap) concordam entre si
e com a conta real sobre T-17 e `sem-cadencia`. F-09, F-10, G-11 (item 1),
G-19, G-27/G-29 e G-31 continuam sendo as seis decisões sem prazo fixo que
esperam o dono, sem mudança nesta rodada — este achado não tira nem
acrescenta nenhuma a essa lista. CRM reconfirmado por API antes de fechar:
66 oportunidades, 60 campos de contato, sem novidade além do já registrado
acima.

### F-33 · A fila do dia trata "pra ontem" e "sem prazo" do mesmo jeito — o lead já declarou urgência no anúncio, antes de qualquer ligação, e a régua só lê isso no fim do funil (28/09/2026) — **FEITO em 28/09/2026 (especificação)**

**Por quê:** reconciliação de sempre antes de desenhar — `git fetch` nas
branches irmãs achou só um commit de documentação na `abertura-operacao-
dnd-n7dnjv` (playbook explicando os 41 workflows, sem consequência para
nenhuma das seis decisões sem prazo fixo de sempre) e nada na `ib6xaz`
(repositório diferente, máquina de vídeo). CRM reconfirmado por API: 66
oportunidades, mesma composição de G-38/G-39; 60 campos de contato, sem
campo novo. Sem achado de reconciliação, a sessão pegou o item de maior
prioridade ainda aberto por um caminho diferente do habitual: em vez de ir
direto à pesquisa de concorrência, conferiu se a própria seção 9.2 do
`build-wesales.md` (a tabela de `Prioridade`) bate com o que os nós de
fato fazem — `grep -n "Prioridade" build-wesales.md` mostra que 4 das 8
regras da tabela (3, 5, 6 e 7) nunca foram escritas como nó em lugar
nenhum. Conferido a fundo antes de tratar isso como bug: **não é** — o
efeito de cada uma já existe por outro caminho (regras 5-7: as listas
8.1/8.2/8.3 já ordenam por `Prioridade` desc e depois por `Tentativa nº`
asc, e como todo lead sem sinal empata em `Prioridade`, o segundo nível já
devolve fresco antes de velho; regra 3: qualquer resposta que não seja
opt-out/auto-resposta/negativa já vira `Prioridade` = 5 pela Interceptação
de Sinal, F-01, mais alto que o 4 que a regra 3 daria). Detalhe completo
dessa checagem, e a nota de coerência que ela deixou na própria seção 9.2,
em `build-wesales.md`, seções 2.63 e 9.2.

**A lacuna real, achada conferindo dado, não texto:** os 12 leads reais
mais recentes ainda não trabalhados por SDR nenhum (2 em `NOVO LEAD`, 10
em `CONECTAR`, todos com `Tentativa nº` = 0 e `Resultado da tentativa`
vazio — confirmado contato a contato, não pela listagem) já chegam com
`Prazo` preenchido em 9 de 12 e `Urgência` (o campo espelho que o G-04 já
registrou) em 11 de 12. O lead já escreveu, no formulário do anúncio, se
precisa "pra ontem" ou "sem prazo, só pesquisando" — 15 dos 45 pontos do
Bloco C (seção 9.1) disponíveis desde o instante em que o contato nasce.
Hoje esse dado fica parado até o Pós-agendamento somar a nota inteira, e a
fila do dia (`Prioridade` desc) não vê nada disso: os dois leads entram
empatados em `Prioridade` = 3 e só se separam pela ordem de chegada.

**Por que não é "rodar a régua de nota mais cedo":** testado e descartado
nesta própria rodada — os três campos do Bloco A (Fit, 30 pontos:
`Clientes novos por mês`, `Tem time comercial`, `Quem atende os leads`)
vêm **vazios em 12 de 12** dos mesmos leads (só o SDR preenche na
ligação), então rodar a fórmula cheia no nó 0 somaria no máximo ~40
pontos mesmo para o lead mais urgente — dentro da faixa "C — nutrição"
(25-44) das próprias faixas da 9.1, que rebaixaria `Prioridade` e moveria
a oportunidade para `abandoned`. Aplicar a régua cheia cedo demais
descartaria lead bom por falta de dado, o oposto do que o item quer. Por
isso o desenho não toca em `Nota de qualificação` nem nas faixas A/B/C/D:
é uma prioridade separada, de escopo estreito (só o degrau mais alto de
urgência, só até `Prioridade` = 4, nunca 5).

**Como — nós 0.9/0.9b, logo após o 0.8b do F-32, no nó de inicialização
já existente da `Cadência 12x30` (seção 2.3 do `build-wesales.md`, detalhe
na 2.63; espelhado em `IMPLEMENTACAO-WORKFLOWS.md`, W11; checklist de
montagem em `GUIA-MONTAGEM.md`):** `If/Else` `Prazo` é `Pra ontem` →
`Update Contact Field Prioridade = 4`; senão, fallback `Prazo` vazio **e**
`Urgência` é `Pra ontem` → mesmo update; senão, `Prioridade` continua 3.

**Achado incidental, registrado e não investigado a fundo:** em vários dos
12 contatos lidos, o valor gravado em `Urgência` pertence à lista de
opções de `Prazo` (ex.: "Pra ontem", "Sem prazo" aparecendo no campo
`Urgência`) — indício de mapeamento trocado entre os dois campos para
parte da base, mesma família do G-04 mas nunca registrado para este par
específico. **Correção de 28/09/2026 (G-40): o G-04 já tinha fechado seis
dias antes desta nota (G-33, 27/09/2026), por uma terceira saída que não
é nem a Opção A nem a B — não há mais "Opção A/B do G-04" para decidir.**
Quem for investigar o mapeamento trocado confere direto contra o que o
`Pós-agendamento v2` grava hoje (as igualdades exatas do G-33). Não teve
nó nem decisão nesta rodada — é nota para a próxima.

**O que este achado não é, e o limite honesto:** não substitui nem
antecipa a `Nota de qualificação` (9.1), que segue existindo só para o
veredito pós-ligação, sem mudança. E, como o próprio G-38/G-39 já
registraram, a operação ao vivo hoje roda por `atuador_filas.py` numa
branch irmã, não pela `Cadência 12x30` nativa deste desenho (0 inscritos,
`IMPLEMENTACAO-WORKFLOWS.md`) — então os nós 0.9/0.9b só valem quando essa
spec for publicada de verdade, ou como referência para quem for portar o
mesmo raciocínio (ler `Prazo`/`Urgência` cedo) para o mecanismo que roda
hoje. Zero campo novo, zero tag nova: reaproveita `Prazo` (Q-17) e
`Urgência`, os dois já na tela. Não depende de `APROVADO.md` — nenhuma
escrita por API nesta rodada, só especificação e leitura.

**Pronto quando:** os nós 0.9/0.9b estiverem montados na tela (ou
portados para o mecanismo que estiver rodando a operação real no
momento); um lead que declarou "pra ontem" no anúncio entrar em
`CONECTAR` com `Prioridade` = 4 sem o SDR ter feito nada ainda; e as
listas 8.1/8.2/8.3 mostrarem esse lead acima dos outros de mesma
`Tentativa nº` sem urgência declarada. F-09, F-10, G-11 (item 1), G-19,
G-27/G-29 e G-31 continuam sendo as seis decisões sem prazo fixo que
esperam o dono, sem mudança nesta rodada.

### G-40 · O G-04 fechou em 27/09/2026 (G-33), e o F-33, escrito seis dias-de-rodada depois, ainda mandava alguém "decidir a Opção A/B" que já não existia — **FEITO em 28/09/2026 (coerência entre documentos)**

**Por quê:** reconciliação de sempre antes de desenhar — `git fetch` na
`abertura-operacao-dnd-n7dnjv` não achou commit novo desde a leitura do
F-33 (`cd004af`, o playbook, sem consequência para nenhuma das seis
decisões sem prazo fixo). CRM reconfirmado por API: `opportunities_search-
opportunity` segue em **66** oportunidades, `locations_get-custom-fields`
(model `contact`) segue em **60** campos — os três novos frente à leitura
do F-32/F-33 (`SDR responsável`, `B · Quanto pode investir`, `Voice AI
Reason for Call`) já estavam explicados por G-27/G-29/G-30, nenhuma
novidade. Sem achado aí, a sessão seguiu a instrução deste roadmap de
varrer por nome tocado nas últimas rodadas antes de tratar o documento
como coerente — `grep -rn "G-04"` em todo o `wesales/` — em vez de ir
direto à pesquisa de concorrência.

**Como:** a varredura achou uma contradição dentro da própria família de
documentos que este roadmap gera. O `### G-04` (acima) ainda trazia no
cabeçalho "peça 2 (Investimento mensal) aguarda o dono" e no `Pronto
quando` "só a peça 2 segue aberta" — mas o **G-33** (27/09/2026, mais
abaixo neste mesmo arquivo) já tinha fechado essa peça, achado por
reconciliação de branch irmã: o dono aplicou uma terceira saída direto no
`Pós-agendamento v2` (v17→v18), nem a Opção A nem a Opção B que o G-04
desenhava. O `Pronto quando` do próprio G-33 já dizia "G-04 (peça 2) ...
sai da lista de decisões sem prazo fixo que esperam o dono" — e todo
recapitulativo posterior (G-34 em diante) respeitou isso, tirando G-04 da
lista. **O que nenhuma rodada corrigiu foi a entrada do G-04 em si**,
que continuou parada no texto de antes do G-33 — mesma classe de lapso do
G-24/G-36 (regra de fechamento cobre o recapitulativo, não o corpo do
item que ela recapitula) e do G-37 (cabeçalho atrasado em relação ao
fechamento real), só que desta vez o cabeçalho atrasado não estava sem a
marca `FEITO`: estava com uma frase que folheava a decisão errada.

A mesma varredura achou a contradição se espalhando: o **F-33** (seção
2.63 de `build-wesales.md`, escrito em 28/09/2026, um dia inteiro depois
do G-33) citou o G-04 no parágrafo "Achado incidental" como se a Opção
A/B ainda estivesse para alguém decidir — prova de que o texto desatualizado
do G-04 já tinha enganado uma rodada seguinte, exatamente o risco que este
tipo de lapso cria. E `IMPLEMENTACAO-WORKFLOWS.md` trazia a mesma
contradição **dentro do próprio arquivo**: uma linha da tabela "Corrigir"
(seção de campos) e um parágrafo sobre o Formulário SDR ainda descreviam
"decisão G-04 pendente"/"até o dono decidir", enquanto outras três
passagens do mesmo arquivo (a linha logo abaixo na mesma tabela, o
checklist de go-live e a fórmula da régua BANT) já diziam corretamente
"G-04 fechado em 27/09/2026".

**Corrigido nesta rodada, cinco pontos, sem tocar em nenhuma decisão de
negócio nova:** (1) cabeçalho e `Pronto quando` do próprio `### G-04`
(acima), agora contando a saída real (a terceira via, não A nem B) e
apontando para o G-33; (2) o parágrafo "Achado incidental" do próprio
`### F-33` (mais abaixo, seção "Ordem sugerida" tardia), que tinha a
mesma frase — editado no lugar, este arquivo não tem a regra de "só
acrescente no fim"; (3) o espelho dessa mesma frase na seção 2.63 de
`build-wesales.md` **não** foi editado no meio (regra do próprio arquivo
— sessões paralelas editam parágrafo no meio, isso colide) — ganhou a
seção **2.64**, nova, no fim do arquivo, corrigindo o encaminhamento sem
apagar o achado original; (4) e (5) as duas passagens de `IMPLEMENTACAO-
WORKFLOWS.md` (tabela "Corrigir" e o parágrafo do Formulário SDR),
editadas no lugar — este arquivo também não tem a regra de "só acrescente
no fim".

**O que este achado não é:** não é uma decisão de negócio nova, não muda
nenhum campo nem tag, não reabre o G-04 nem o G-33 — os dois continuam
`FEITO`, só o *registro* estava um passo atrás do que já tinha
acontecido. Também não é o mesmo defeito do G-37 (cabeçalho sem a marca
`FEITO`): ali faltava só o carimbo; aqui o texto ativamente apontava para
uma decisão que já não existia, o tipo de erro mais caro de achar tarde
porque parece, à primeira leitura, uma pendência real.

**Regra prática, ao lado da do G-24/G-36/G-37:** quando um item fecha por
um caminho que **nenhuma** das opções que ele mesmo desenhou previa (como
o G-04/G-33 — nem A nem B, uma terceira saída), procurar por outras
seções que ainda descrevem as opções originais como escolha em aberto —
elas tendem a sobreviver ao fechamento porque ninguém as está lendo como
"parte do G-04", só como contexto lateral (a seção 2.63 citou o G-04 de
passagem, num parágrafo sobre outro achado). O sweep de coerência de
sempre (`grep -rn` pelo nome do item) pega isso; a leitura linear do
arquivo, não.

**Pronto quando:** cumprido nesta rodada — as cinco passagens corrigidas
concordam entre si e com o G-33 sobre como o G-04 fechou de verdade. Zero
campo, zero tag, zero escrita no CRM: item de coerência entre documentos,
não depende de `APROVADO.md`. F-09, F-10, G-11 (item 1), G-19, G-27/G-29 e
G-31 continuam sendo as seis decisões sem prazo fixo que esperam o dono —
este achado não tira nem acrescenta nenhuma a essa lista (G-04 já tinha
saído dela pelo G-33; esta rodada só corrigiu o registro). CRM
reconfirmado por API antes de fechar: 66 oportunidades, 60 campos de
contato, sem novidade além do já registrado acima.

### G-41 · A própria regra 9.2 (`Prioridade`) tem uma ordem que perde a higiene de base e um furo de cobertura — os dois já documentados no script que roda a operação real, nunca promovidos a item deste roadmap (28/09/2026) — **FEITO em 28/09/2026 (correção de especificação)**

**Por quê:** reconciliação de sempre antes de desenhar — `git fetch` nas
branches irmãs não achou commit novo em `claude/abertura-operacao-dnd-
n7dnjv` (`cd004af`, mesmo do G-38/G-39/F-33/G-40) nem em `claude/abertura-
operacao-dnd-ib6xaz` (repositório da máquina de vídeo, sem relação com
`wesales/`). CRM reconfirmado por API: `opportunities_search-opportunity`
(`status=all`) confirma **67** oportunidades (1 a mais que a última leitura
— `Flávia Do`, lead novo em `NOVO LEAD`, crescimento orgânico, não achado);
`locations_get-custom-fields` (`model=contact`) segue em **60** campos, sem
campo novo. `mcp__github` confirma que o PR desta branch mudou de número
(#93, citado no G-19/G-35, fechou sem merge; o aberto hoje é o **#102**,
mesma base `claude/youtube-publication-next-steps-v7o4el`) — sem
consequência: o G-19 já generalizava "o número muda toda vez que um fecha e
outro abre", nada para corrigir. Sem achado de reconciliação, a sessão
conferiu se os seis itens que esperam decisão do dono (F-09, F-10, G-11
item 1, G-19, G-27/G-29, G-31) tiveram a premissa vencida — nenhuma: 0
oportunidades `won` (F-18 segue bloqueado), só 2 conversas automáticas
outbound e as duas são teste do próprio dono, não tráfego de cadência real
(R-14 segue corretamente bloqueada).

**Como — a lacuna veio de uma pergunta que nenhuma rodada tinha feito
ainda: por que 8 leads reais amostrados em `CONECTAR`, todos com
`Tentativa nº` = 0, carregavam `Prioridade` = 4 sem nenhum workflow deste
projeto ter escrito isso?** A primeira hipótese (o `T · Prazo` = "Pra
ontem" do F-33 já estaria influenciando `Prioridade`) não resistiu à
amostra — os 8 leads tinham "Pra ontem" **e** `Prioridade` = 4, mas também
tinham `atraso-1a-tentativa` (o tag de SLA do R-02) e zero tentativas,
então a amostra sozinha não separava as duas causas. A resposta real, lida
em `wesales/tools/atuador_filas.py` (branch irmã, só leitura — o script
**lê** `Prioridade` para montar fila, nunca escreve nela desde 28/09) e
depois em `wesales/tools/recalcula_prioridade.py` (mesma branch): o G-25
desta mesma sequência de rodadas já tinha registrado que o dono rodou
`recalcula_prioridade.py --aplicar` em 27/09 21:04 UTC para soltar os 31
leads represados na abertura — o script implementa a regra 9.2 **como
está escrita**, e por isso reproduz o defeito que ela já tinha antes de
qualquer script existir.

O docstring do script (lido por inteiro, não só o cabeçalho) já documentava
os dois defeitos, sem nenhuma rodada deste roadmap ter promovido isso a
item — mesma classe de G-16/G-17/G-19/G-21 ("achado técnico completo num
lugar vizinho, nunca promovido a item rastreável"), desta vez o "lugar
vizinho" é o docstring de um script na branch irmã, não um `.md` deste
projeto:

1. **Ordem perde a higiene.** A regra de `nutricao-90d`/`telefone-invalido`
   morava na posição 8 (a última); a regra de `Tentativa nº` ≤ 2 morava na
   5 e casa primeiro — "primeira regra que casar, ganha" (topo da seção
   9.2). Um lead com telefone inválido e 0-2 tentativas (o caso mais comum:
   a tag nasce perto da 1ª tentativa, quando o discador rejeita o número)
   nunca alcançava a regra 8: saía com `Prioridade` 4 (fila quente) em vez
   de 1. O `--dump` do script já marcava isso como `[9.2-r8-perdeu]`.
2. **Furo de cobertura.** A regra de `Tentativa nº` ≥ 8 só valia com
   `Total de conexões` = 0; um lead com 8+ tentativas que já conectou ao
   menos uma vez, mas nunca produziu `Pediu retorno` nem nota, não casava
   em regra nenhuma — o script marcava `[9.2-sem-regra]` e não escrevia
   nada, em vez de inventar valor.

**Corrigido na fonte, `build-wesales.md` seção 9.2 (não neste roadmap — a
tabela é lá; aqui só o registro):** a regra de higiene subiu para a posição
5, depois das quatro regras de sinal/nota (1-4, que continuam decidindo
primeiro quando há sinal real — um lead que respondeu ou tirou nota alta
não perde fila por uma tag de higiene que, nesses casos, já não descreve o
estado real dele) e antes das três regras de `Tentativa nº` (agora 6-8). A
condição `e Total de conexões = 0` da antiga regra 7 foi removida — 8+
tentativas envelhece a fila do mesmo jeito, tenha conectado antes ou não,
mesmo raciocínio que já separa as faixas 3-7 de 8+. A nota de coerência do
F-33 (mesma seção) foi renumerada para bater com a tabela corrigida (regras
3, 6, 7, 8 em vez de 3, 5, 6, 7). O achado do "nenhum workflow remove
`telefone-invalido` fora do F-11" (reenvio de formulário) ficou registrado
na própria seção 9.2, sem virar item novo — mesma classe de L-03/L-06,
achado sem urgência.

**O que este achado não é:** não é uma decisão de negócio — hygiene sempre
deveria vencer "lead fresco", não é escolha do dono, é bug de ordenação.
Não muda `Prioridade` de nenhum lead real (o script que a escreve mora na
branch irmã, fora do escopo desta sessão — regra 5, só `wesales/`); a
próxima vez que alguém rodar `recalcula_prioridade.py --aplicar` lá, a
tabela corrigida aqui é a referência para atualizar o script também, não
esta rodada. Não reabre G-25/G-31 (a soltura dos 31 leads em 27/09 já
aconteceu e não muda). Zero campo, zero tag, zero escrita no CRM: item de
correção de especificação, não depende de `APROVADO.md`.

**Pronto quando:** cumprido nesta rodada — a tabela da seção 9.2 não tem
mais regra que hygiene perde para `Tentativa nº`, nem faixa de `Tentativa
nº` sem regra que a cubra; a nota de coerência do F-33 bate com a nova
numeração. F-09, F-10, G-11 (item 1), G-19, G-27/G-29 e G-31 continuam
sendo as seis decisões sem prazo fixo que esperam o dono, sem mudança
nesta rodada. CRM reconfirmado por API antes de fechar: 67 oportunidades,
60 campos de contato, sem novidade além do já registrado acima.

### G-42 · Seis cabeçalhos de item (G-03, G-05, G-22, G-29, G-30, G-31) não carregavam nenhuma marca de status — mesmo bug que o G-37 já corrigiu para F-18 a F-26, desta vez na família G (28/09/2026) — **FEITO em 28/09/2026 (coerência da própria seção "Ordem sugerida")**

**Por quê:** reconciliação de sempre antes de pegar o item de maior
prioridade ainda aberto — `git fetch` nas branches irmãs achou um commit
novo em `claude/abertura-operacao-dnd-n7dnjv` (`9622b8e`, depois do
`cd004af` que o G-38/G-39/F-33/G-40/G-41 já tinham lido): só um registro
de infraestrutura (`DE-PARA-SESSOES-CRM.md`, "Relógio dos robôs no
GitHub" — o dono trocou os crons de `wesales-filas.yml`/
`wesales-wa-governador.yml` por um workflow novo, `wesales-relogio.yml`,
que roda `atuador_filas.py --aplicar`/`wa_governador.py --aplicar` a cada
30 min), sem consequência para nenhum item deste roadmap. CRM
reconfirmado por API: `opportunities_search-opportunity` (`status=all`)
confirma **68** oportunidades (1 a mais que a leitura do G-41 — mais
crescimento orgânico, não achado); `locations_get-custom-fields`
(`model=contact`) segue em **60** campos, sem campo novo.

Sem achado de reconciliação, a sessão seguiu a própria instrução deste
roadmap ("`grep -n '^### [FGR]-[0-9]'` é o comando que resolveu essa
pergunta em rodadas anteriores" — G-37) para achar o item de maior
prioridade ainda aberto. O resultado trouxe **seis** cabeçalhos sem
`FEITO`, `ABERTO` nem "especificação fechada": G-03, G-05, G-22, G-29,
G-30, G-31 — pareciam seis itens abertos.

**Cinco eram mesmo abertos, só sem o marcador explícito que G-11/F-09/F-10
já usam.** G-03 (execução idempotente já agendada para 29/09/2026 08:00,
confirmado no próprio corpo do item — falta só a data chegar); G-05
(peça 1/2 fechadas, falta a submissão dos Templates à Meta, já registrado
no próprio "O que falta para fechar o G-05 por inteiro"); G-29, G-30 e
G-31 (as três seguem, sem mudança, na lista de "decisões sem prazo fixo
que esperam o dono" que todo parágrafo de fechamento desde o G-29 já
carrega — só o cabeçalho de cada uma nunca ganhou o rótulo que essa lista
já dava por certo).

**G-22 era o caso genuinamente diferente: já estava fechado, e o
cabeçalho nunca recebeu a marca.** A própria seção "Ordem sugerida" (mais
abaixo neste arquivo) registra, desde 23/09/2026: "Fechado como **G-22**:
especificação nó a nó completa... `AGENTE-IA-CONEXAO.md` (§1, §8)
atualizado com o achado" — e o parágrafo seguinte já agrupava G-22 junto
com F-11, F-12, F-13, F-15, G-07, G-08, G-17, G-18 e G-21 como "itens com
desenho completo... só faltam ser montados/aplicados na tela". Todos os
outros nove dessa lista carregam `FEITO` no próprio `### cabeçalho`; só
G-22 tinha ficado para trás — mesma causa provável que o G-37 já registrou
para F-18 a F-26: a rodada que escreveu o parágrafo de fechamento no fim
da seção nunca voltou ao cabeçalho do item, lá no corpo do documento, para
acrescentar a mesma marca.

**Como:** seis cabeçalhos editados no lugar, cada um com a marca que o
próprio corpo do item já sustenta — `### G-03` recebeu "especificação
fechada em 24/09/2026, execução agendada para 29/09/2026"; `### G-05`
recebeu "especificação fechada em 22/09/2026, execução aguarda Templates
aprovados pela Meta"; `### G-22` recebeu "FEITO em 23/09/2026
(especificação nó a nó completa)"; `### G-29`, `### G-30` e `### G-31`
receberam "ABERTO, decisão do dono", mesmo rótulo que o `### G-11` já usa.
Nenhum texto de corpo mudou, só os seis cabeçalhos. Conferido depois:
`grep -n "^### [FGR]-[0-9]" ROADMAP-SALES-ENGAGEMENT.md | grep -v
"FEITO\|aguarda\|especificação fechada\|ABERTO"` volta vazio.

**O que este achado não é:** não é decisão de negócio nova — não muda
nenhum campo, tag ou desenho; G-22 continua sendo o mesmo desenho de
23/09/2026 (dois workflows sidecar, `Update Conversation AI Bot and
Status`), só o registro estava um passo atrás do que já tinha acontecido,
mesma classe do G-40 (para o G-04) e do G-37 (para F-18 a F-26). Não
reabre G-29/G-30/G-31: as três continuam abertas exatamente como estavam,
só agora com o rótulo que a lista de fechamento de cada rodada seguinte já
lhes dava. Zero campo, zero tag, zero escrita no CRM: item de coerência
entre documentos, não depende de `APROVADO.md`.

**Regra prática, ao lado da que o G-24/G-36/G-37 já deixaram:** a regra do
G-37 ("parágrafo de fechamento + marca `FEITO` no cabeçalho são as duas
metades da mesma entrega") vale também no sentido inverso — um item
genuinamente aberto também precisa do rótulo explícito (`ABERTO`,
"aguarda decisão do dono", "especificação fechada, execução aguarda...")
no próprio cabeçalho, não só no corpo ou na lista recapitulativa do fim da
seção. `grep -n "^### [FGR]-[0-9]"` sem nenhum dos quatro marcadores
(`FEITO`/`ABERTO`/`aguarda`/`especificação fechada`) na mesma linha é o
comando que verifica os dois lados de uma vez — a próxima rodada que abrir
ou fechar um item deve rodar esse grep antes de encerrar.

**Pronto quando:** cumprido nesta rodada — o grep de verificação volta
vazio; os seis cabeçalhos corrigidos são o próprio "Pronto quando", mesmo
padrão que já valia para o G-24/G-36/G-37/G-40/G-41.

F-09, F-10, G-11 (item 1), G-19, G-27/G-29 e G-31 continuam sendo as seis
decisões sem prazo fixo que esperam o dono, sem mudança nesta rodada. CRM
reconfirmado por API antes de fechar: 68 oportunidades, 60 campos de
contato, sem novidade além do já registrado acima.

### G-43 · O portão do governador de WhatsApp é um laço que espera 15 min e volta — e em lead real ele não volta: `wa-liberado` fica horas sem consumir, e nenhum monitor deste roadmap enxerga isso (28/09/2026) — **especificação fechada em 28/09/2026, execução aguarda o dono (troca de desenho em workflow publicado, sem `[x]`)**

**Por quê:** reconciliação de sempre. O branch `claude/stoic-hawking-0euxnd`
(a operação real) ganhou, depois do último cruzamento, um registro do dono
(`DE-PARA-SESSOES-CRM.md`, "28/09 noite"): o portão do governador
(`wa_governador.py`) faz o lead esperar com `wa-aguardando`, o script troca
por `wa-liberado`, e o workflow **deveria** ver a tag e enviar. Não envia.
Conferido por leitura direta nesta sessão (`contacts_get-contacts`,
contato de origem Meta): entrou 17:46 UTC, ainda carrega `wa-liberado` e a
tag do dia `wa-lib-2026-09-28` às ~22:10 UTC — mais de quatro horas com a
liberação dada e nada enviado. O relato do dono fala em 2h30 no mesmo
lead, então o problema não é pontual. O log de execução não sai por API
(404), o que explica por que ninguém viu antes: **nenhum dos monitores do
F-05 olha uma tag de portão parada**, e o lead até aparece como "tratado"
(tem tag de liberação do dia).

**Causa (hipótese do dono, coerente com o que se vê):** o laço "tem
`wa-liberado`? → não → espera 15 min → volta" (Go To) não reavalia nos leads
reais, só funcionou no teste em que a liberação veio em minutos. É o
desenho, não um lead: o mesmo laço existe em todos os workflows que ganharam
a trava.

**Como (o que um concorrente não copia olhando a tela):** trocar **espera
por evento**. A tag é a fila e o governador é o relógio; quem envia é um
workflow que **nasce da própria tag**, sem laço nenhum
(`build-wesales.md`, seção 2.65): gatilho `Contact Tag` = `wa-liberado`
adicionada, dispara no instante da liberação, uma vez por liberação, e o
texto do toque vem de `Tentativa nº` (C-01) — um único envio para todas as
cadências, em vez de um laço copiado em cada uma. Reaproveita tag, campo e
script que já existem: zero tag, zero campo novo.

**Pronto quando:** (1) a seção 2.65 existe nó a nó — feito nesta rodada;
(2) o dono montar o workflow na tela e religar um lead de teste
(`wa-aguardando` → governador → mensagem entregue em minutos, `wa-liberado`
removida); (3) o "Watchdog de portão" (2.65, peça B) cadastrado no
`atuador_filas.py`, que hoje o dono roda a cada 30 min no GitHub: lista
contato com `wa-liberado` há mais de 45 min e o devolve para `wa-aguardando`
mais um aviso na tela da SDR — assim, mesmo que a troca de desenho falhe, a
falha vira tarefa em 45 min e não silêncio de 4 h.

**Zero escrita no CRM nesta rodada:** trocar o desenho de workflow
publicado é decisão do dono, sem `[x]` em `APROVADO.md`. Esta sessão só leu.
F-09, F-10, G-11 (item 1), G-19, G-27/G-29 e G-31 seguem esperando o dono.

### G-44 · O SDR agora registra a ligação em UM campo (`Registro da ligação`), e nenhum documento desta branch sabe — o `GUIA-SDR.md` ainda manda marcar dois (29/09/2026) — **FEITO em 29/09/2026 (reconciliação)**

**Por quê.** Reconciliação de sempre antes de desenhar: CRM lido por API nesta
rodada — `locations_get-custom-fields` sobe de 60 para 61 campos de contato,
`opportunities_search-opportunity` de 66 para 81 oportunidades (leads novos de
verdade; o mais recente, às 14:06Z, já com `cad-inbound`, `fila-quente`,
`atraso-1a-tentativa` e `limpar-tarefas`). O campo novo é `Registro da ligação`
(id `2iqHW8jbd41AI6fZJr6P`, criado 11:37Z). A explicação estava numa branch
irmã, não nesta (hábito do G-31): commit `5d41401` (`tools/criar_registro_1_campo.py`)
e `DE-PARA-SESSOES-CRM.md` da `abertura-operacao-dnd-n7dnjv`. Pedido do dono:
menos cliques para a SDR.

**O que o relato diz que existe (não confirmado nó a nó daqui — o MCP não lê
workflow):** workflow `Registro da ligação — 1 campo` (id `9f70fac2`), gatilho
`contact_changed` / `has-changed` em `Registro da ligação`; cadeia de 10
If/Else, um por opção; cada ramo escreve `Canal da tentativa` (só as opções
`Telefone · …` e `WhatsApp · …`) e `Resultado da tentativa` num único nó
`update_contact_field`, depois limpa o campo novo. `Não ligar` e `Desqualificado`
gravam só o Resultado. O `Pós-ligação v3` não muda: continua disparando pela
mudança de `Resultado da tentativa`.

**O que a leitura do desenho encontrou (por que vale registrar):**
1. **Nenhum documento cita o campo.** `GUIA-SDR.md` (o que o SDR vê na tela)
   mandava marcar dois campos; corrigido com o atalho, mantendo os dois como
   reserva — o script do dono diz que continuam valendo.
2. **Canal e Resultado saem no mesmo nó**, então o `Pós-ligação v3` (que lê
   `Canal da tentativa` nos portões de `fila-wa`, G-38) não corre o risco de ler
   Resultado novo com Canal velho. É o desenho certo; o risco só volta se
   alguém separar em dois nós.
3. **O workflow roda duas vezes por marcação** (a limpeza do campo é uma nova
   mudança): a segunda execução cai em nenhum ramo e termina. Inofensivo,
   mas conta como execução no plano — F-10/monitor de custo devem saber.
4. **Marcar a mesma opção duas vezes seguidas funciona** justamente porque o
   campo é limpo ao fim; sem a limpeza, `has-changed` não dispararia na segunda
   "Não atendeu" seguida. É a mesma razão que faz o `Pós-ligação` limpar
   `Resultado da tentativa` (build-wesales.md, nó 5).
5. **Não há opção `WhatsApp · Caixa postal` nem `WhatsApp · Número errado`:**
   consistente com o mundo real (WhatsApp não tem caixa postal), mas o SDR que
   tiver número errado descoberto pelo WhatsApp precisa marcar
   `Telefone · Número errado`, que grava `Canal = Telefone` — cosmético, o
   Pós-ligação trata Número errado igual nos dois canais.

**Pendente, e por quê não fecho aqui:** (a) confirmar ao vivo que o workflow
9f70fac2 está publicado e cobre as 10 opções (leitura de workflow é
`tools/ghl_interno`, com token do PC — não disponível neste conector);
(b) `INVENTARIO-WORKFLOWS.md` não lista esse workflow — inclusão vale ser feita
por quem o ler ao vivo, não por relato de commit (o CLAUDE.md desta pasta já
avisa: dump/relato é candidato, não item). Zero escrita no CRM nesta rodada.

**Pronto quando:** `GUIA-SDR.md` e `campos-e-tags.md` deixam de contradizer a
conta (feito); o `INVENTARIO-WORKFLOWS.md` ganha a linha do workflow depois de
lido ao vivo (pendente, do PC).

### G-45 · Dois campos novos nasceram na conta na noite de 29/09/2026 — um explicado por código de branch irmã, o outro sem dono conhecido — e a lista de campos fora da numeração parava no nono (29/09/2026) — **FEITO em 29/09/2026 (reconciliação)**

**Por quê.** Mesma reconciliação de sempre antes de desenhar: `locations_get-custom-fields`
(model `contact`) sobe de 61 (G-44) para 63. Os dois novos: `Registro automático
em` (id `gf332esJXqwxY8LsA66e`, 22:16Z) e `Link: formulário + agenda` (id
`GX7Z8yRGeERXCUgNbL3W`, 22:20Z), ambos `TEXT`, ambos com posição 2800/2850 no
grupo de controle e placeholder `preenchido pelo robô`.

**O que a busca nas branches irmãs achou.** `Link: formulário + agenda` tem
autor: `tools/link_formulario.py` (commit `491d25d`, `claude/link-formulario`,
pedido do dono, coluna da Minha fila). Lido o código: escreve só em contato
`CONECTAR` ou com `confirmar-reuniao`, via `PUT /contacts` com o link montado
dos valores preenchidos, e só quando mudou — idempotente. `Registro automático
em` **não aparece em nenhuma branch** (busca por nome e por id): fica registrado
como sem dono conhecido, e proibido de alimentar regra até alguém confirmar.

**Riscos que a leitura do código mostrou (candidatos, não medidos ao vivo):**
1. O link carrega **telefone, e-mail e as respostas de qualificação** na query
   string, gravado em campo de contato. Quem tiver a coluna da Minha fila vê o
   link — igual ao que a SDR já vê no contato; mas colar o link em mensagem ao
   lead expõe dados dele na URL. Vale o `GUIA-SDR.md` dizer que o link é da SDR,
   não para reenviar.
2. O script varre `contatos()` inteiro a cada disparo do relógio. Com a base
   crescendo (66 → 81 oportunidades em uma semana) o custo cresce junto; medir
   antes de pôr no relógio de 5 min.
3. `sdr_responsvel` vai fixo `Andreyna Siqueira` no link: com o segundo SDR do
   R-10, todo lead do formulário nasce atribuído à mesma pessoa.

**Pendente, e por que não fecho aqui:** confirmar com o dono quem escreve
`Registro automático em`; nada foi escrito no CRM nesta rodada.

**Pronto quando:** `campos-e-tags.md` lista os dois campos com id e origem
(feito); o dono diz o que `Registro automático em` registra (pendente).


**Risco 1 do G-45 fechado em 30/09/2026:** `GUIA-SDR.md` (seção "O que o
sistema faz sozinho") agora diz que o `Link: formulário + agenda` é da SDR e não
deve ser colado em mensagem ao lead, porque a URL leva telefone, e-mail e
respostas de qualificação. Riscos 2 e 3 e a dúvida sobre `Registro automático
em` seguem pendentes do dono; CRM reconferido, sem campo novo desde 29/09 22:20Z.


### G-46 · Um campo novo nasceu na conta em 30/09/2026 (`Lead já tem reunião marcada?`) sem rastro em nenhuma branch — e ele duplica um fato que a operação já guarda em duas fontes (30/09/2026) — **FEITO em 30/09/2026 (reconciliação)**

**Por quê.** Mesma reconciliação de sempre antes de desenhar: `locations_get-custom-fields`
(model `contact`) sobe de 63 (G-45) para 64. O novo: `Lead já tem reunião
marcada?` (id `HKuJMWNg0TwXw6WQa0pS`, `SINGLE_OPTIONS` com `Não`/`Sim`,
12:14Z, posição 770, grupo de qualificação).

**O que a busca achou.** Nada: nome, chave `lead_j_tem_reunio_marcada` e id
procurados no branch de trabalho e nas branches `abertura-operacao-dnd-*`,
`calendly-crm`, `closer-para-sdr`, `link-formulario`, `responder`,
`wesales-filas-*` e `wesales-workflows-pc` — zero ocorrência. Lidos os contatos
(a base cabe numa página): nenhum tem valor no campo. Ou é pergunta de
formulário ainda sem resposta, ou campo criado e não ligado.

**Risco (candidato, não medido).** O fato "já tem reunião" hoje mora em `Data
agendado` e na tag `confirmar-reuniao`. Uma terceira fonte preenchida à mão
diverge das outras duas sem erro visível — mesmo padrão do G-27/G-29.

**Feito:** `campos-e-tags.md` lista o campo com id, opções e a proibição de
usá-lo em regra até o dono confirmar. Nada foi escrito no CRM.

**Pronto quando:** o dono diz quem escreve o campo e se ele substitui ou
complementa `Data agendado` (pendente).
