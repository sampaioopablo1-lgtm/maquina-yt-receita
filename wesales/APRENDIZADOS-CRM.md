# O que as execuções da rotina horária já descobriram

Memória entre rodadas. Antes de investigar de novo, procure aqui.

## Os dados de produção são a terceira auditoria — e acharam o que texto e tela não achavam — 21/09/2026, a pedido do dono

Pedido ao vivo: "consulte o que foi configurado no CRM, atualize os
documentos". Até aqui o projeto tinha duas auditorias: a de **texto**
(grep por nome de etapa, merge field órfão — G-02) e a de **tela**
(lista de workflows colada pelo dono, `locations_get-custom-fields`). Esta
rodada leu a **terceira**: os valores gravados nos 50 contatos e 50
oportunidades, e o que os workflows publicados deixaram neles. Três
achados que nenhuma das outras duas podia ver:

1. **`Investimento mensal em anúncios` recebe do Meta quatro textos, e só
   um é opção do campo.** `SINGLE_OPTIONS` no GHL não recusa valor fora da
   lista quando quem escreve é a integração do Lead Ads — grava o texto do
   anúncio como veio (`Não invisto nada ainda`, `Até R$ 1.000`, `Abaixo de
   5k`). A régua 9.1 compara contra `Até 1k`/`1k a 5k`/`5k a 10k` e nunca
   casa. É a classe de bug do R-16 (rótulo que a tela não tem), só que o
   R-16 corrigiu o *documento* contra a *tela*; aqui a tela também está
   errada contra o *dado*. **Regra prática:** para todo campo `SINGLE_OPTIONS`
   alimentado por integração (Meta, formulário, API), conferir os valores
   *gravados* (`contacts_get-contacts`, `customFields[].value`) contra
   `picklistOptions` — não basta conferir o documento contra a tela.
2. **`Necessidade`/`Urgência` não eram duplicatas paradas** (Tabela F de
   `CONFERENCIA-CAMPOS.md` esperava decisão há dois dias) — são onde o Meta
   grava, com 34 e 39 contatos preenchidos. Enquanto o documento discutia
   "de que lado fica", o dado já tinha escolhido o lado errado. E o
   mapeamento mudou no meio (os 5 leads mais novos caem em `Dor
   principal`): auditoria de campo precisa olhar *quando* cada valor
   chegou, não só *se* chegou.
3. **Rastro de execução vale mais que status "Publicado".** Pós-agendamento
   está publicado com 3 ativos, e os 3 têm `Prioridade` e `Data agendado`
   gravados — mas `Nota de qualificação` vazia nos 3. Pós-ligação rodou 24
   vezes num contato e `Total de conexões` continua vazio. Os 10 leads
   nascidos depois do Mestre de saída ir ao ar chegaram com
   `limpar-tarefas`. Nenhum desses três aparece na lista de workflows nem
   num grep — só no valor do campo. **Regra prática:** depois de publicar um
   workflow, ler os campos que cada nó deveria ter escrito nos contatos que
   passaram por ele; nó que não deixou rastro não rodou, esteja o workflow
   "Publicado" ou não.

Detalhe e opções de correção: `CONFERENCIA-CAMPOS.md` (Tabela H) e
`GUIA-MONTAGEM.md` ("Estado da montagem em 21/09/2026"). Novo item G-04 no
`ROADMAP-SALES-ENGAGEMENT.md`. Zero escrita no CRM: tudo é decisão do dono
(formulário do anúncio, opções de campo, nós de workflow — nada sai por
API neste conector). Confirmado também pelo lado das conversas: **zero
mensagem de WhatsApp/SMS enviada pela operação até hoje** — R-14 segue
esperando com razão.

Limite desta leitura, registrado para ninguém confiar além do que ela
prova: `calendars_get-calendar-events` por `userId` voltou vazio para o
dono das 3 oportunidades em `NEGOCIAR`, embora `Data agendado` tenha sido
gravada pelo gatilho `Appointment Status` — a busca por usuário pode não
enxergar evento sem responsável, e o conector não lista calendários para
buscar por `calendarId`. Não dá para afirmar por API se os 3 agendamentos
existem.

## F-05 destravado pelo próprio G-03: "espera volume" tinha prazo de validade — 21/09/2026, sessão automática

Sweep de coerência de sempre (limpo — zero merge field órfão, zero nome de
etapa antigo fora da tabela 1.0, listas de réguas batendo com as listas de
remoção do Mestre de saída). Antes de procurar lacuna nova do zero, reli o
F-05 (Monitor de Saúde da Operação) com a pergunta que a nota final do
roadmap já sugeria: "por que ele está esperando, e essa razão ainda é
verdade?" A "Ordem sugerida" dizia "F-05 só morde quando há mais de uma
cadência no ar" — **e essa frase nunca foi verdade**: as invariantes do
F-05 (lead parado numa etapa, tarefa vencida) checam **um** lead contra
**uma** régua de cada vez, nunca comparam réguas entre si. A frase
confundiu "por que o item ainda não incomodou ninguém" (não havia lead de
verdade correndo cadência nenhuma) com "o que o item precisa para fazer
sentido" (lead de verdade, ponto — não importa quantas réguas existem). E
lead de verdade é exatamente o que G-03 (Bloco 0, mesma data) achou: 47
oportunidades pagas paradas em `NOVO LEAD` há mais de 24h, e ninguém — nem
uma automação, nem um dashboard — avisou sozinho. Isso não é só "F-05
deixou de esperar volume"; é a prova em produção de que o problema que o
F-05 existe para pegar já aconteceu, sem F-05 no ar para pegá-lo.

**Regra prática, generalizável:** "este item espera X" é uma afirmação
com data de validade, igual ao achado já registrado abaixo ("número medido
dentro de uma instrução tem data de validade") — mas aqui a validade não
era de um número, era do **raciocínio**. Vale reler o "por quê estamos
esperando" de todo item represado a cada rodada sem tela, não só reconferir
se o número mudou: às vezes o número que faltava já chegou por um caminho
diferente do que o enunciado original previa.

**Desenhada só a primeira peça (lead esquecido em `NOVO LEAD`, que nem
estava nas seis invariantes originais do "Como") — decisão de escopo,
registrada no roadmap (F-05).** Achado que vale por si, para não redesenhar
a mesma coisa depois, e que exige cuidado para não confundir duas
invariantes parecidas: "tarefa vencida sem resultado" **já não existe como
risco** neste desenho — o nó 10b do bloco padrão de tentativa
(`build-wesales.md`, seção 2.4) já classifica sozinho `Resultado da
tentativa = Não atendeu` quando o prazo do dia estoura sem o SDR agir, e a
lista 8.5 já mostra esse volume; não sobra "vencida sem resultado" pendurada
em lugar nenhum. **Isto não vale para a invariante vizinha da mesma
lista original, `fila-tel`/`fila-wa` presente há mais de 24h** — essa
continua um risco de verdade e diferente: se a tag ainda está lá depois de
24h é porque o nó 9 (que remove a tag sempre, todo dia até 18:30) não
rodou, sinal de workflow travado ou instância perdida, não de SDR lento.
Quase escrevi as duas como a mesma coisa por causa do nome parecido — vale
a mesma pergunta antes de desenhar qualquer invariante futura do F-05:
"isso ainda é um risco no desenho atual, ou o desenho já mudou debaixo
dela — e é exatamente esta invariante, ou uma vizinha de nome parecido?"

**Achado de desenho, mesma classe de bug que a entrada "A regra certa
estava no portão errado" (abaixo) já descreveu para outras réguas, aqui
achado *ao especificar*, não *depois de publicado*:** o Mestre de saída
(seção 3) só alcança seu nó de remoção de tag quando a oportunidade **sai**
de `CONECTAR`/`open` — a transição `NOVO LEAD` → `CONECTAR`, que é como o
alerta de F-05 se resolve na prática, cai no ramo de no-op dele (nó 1) e
nunca chega lá. Resolvido com um nó 0 novo, incondicional, antes do portão
— `Remove Contact Tag` de quem não tem a tag não custa nada, mesmo
raciocínio já usado para `Remove from Workflow`. Registrar aqui porque é a
primeira vez que este projeto pega esta classe de bug **durante o desenho**
em vez de descobri-la numa migração posterior — vale perguntar "este alerta
se resolve numa transição que o Mestre de saída trata como no-op?" toda vez
que uma tag nova precisar de limpeza automática.

Zero escrita no CRM nesta rodada: item de especificação
(`build-wesales.md`, seções 2.20, 3 e 8.20; `campos-e-tags.md`, T-16;
`ROADMAP-SALES-ENGAGEMENT.md`, F-05) mais uma tag nova **proposta**, não
criada — `novo-lead-estagnado` nasce `[ ]` em `APROVADO.md`, não `[x]`
(mesma regra do incidente da T-15, 19/09/2026, aplicada desde o primeiro
dia desta vez, não como correção depois). Subconta reconfirmada via
`opportunities_get-pipelines`/`opportunities_search-opportunity`/
`locations_get-custom-fields`: mesmas 5 etapas do `FUNIL DE VENDAS`, 46
campos, 50 oportunidades (47 `NOVO LEAD` + 3 `NEGOCIAR`, status `open` em
todas) — sem mudança desde a última rodada; G-03 segue aguardando o dono.

## R-17: resposta de opt-out tratada como sinal quente por um workflow já publicado — 21/09/2026, sessão automática

Depois do sweep de coerência de sempre (limpo, ver entrada abaixo), reli o
2.9.3 (`Interceptação de Sinal — Resposta`) com atenção ao invés de só
conferir nome de etapa — mesmo método do G-02. Achado: o gatilho
`Customer Replied` não olha o **conteúdo** da resposta, só o canal. Um lead
que responde "pare, não me manda mais mensagem" recebia `Prioridade` = 5,
tag `fila-quente` e tarefa "ligar agora" — o mesmo tratamento de quem
demonstra interesse. E não é achado de documento parado: `GUIA-MONTAGEM.md`
("Estado da montagem em 19/09/2026, mais tarde") já registrava esse
workflow como **Publicado**, 1 inscrito — o defeito estava ativo na
subconta, não só na especificação.

**Pesquisado (`WebSearch`, já que os domínios de suporte da HighLevel
seguem bloqueados neste ambiente — mesma limitação de sempre):** o
changelog oficial da HighLevel (`Customer Replied Trigger: Improved Message
Filters`) confirma que o gatilho aceita filtro pelo **corpo da mensagem**
com operadores `Contains`/`Doesn't Contain`/`Exact Match`, além de canal,
tag (`Has Tag`/`Doesn't Have Tag`), tipo de intenção e canal de resposta.
Isso fecha duas dúvidas de uma vez: dá para restringir um `Customer Replied`
por palavra-chave sem precisar de um nó dentro do workflow, e dá para
**excluir** por palavra-chave o gatilho de um workflow vizinho — é o que
permite dois workflows ouvindo o mesmo evento nunca disparar para a mesma
mensagem (`Contains` num, `Doesn't Contain` a mesma lista no outro).
**Nível de confiança: médio** — confirmado por busca (resultado de IA sobre
página de suporte + changelog oficial), não testado na tela desta subconta;
a especificação (`build-wesales.md`, seção 2.9.5) já avisa para confirmar
na tela se o campo aceita várias frases numa linha só (OR) ou se precisa de
uma linha por frase — o desenho não depende de qual das duas for verdade.

**Regra prática, generalizável:** todo gatilho `Customer Replied` já
montado ou a montar neste projeto (2.9.2 não precisa, é `Trigger Link
Clicked`; 2.9.3 e qualquer futuro workflow que reaja a resposta de texto)
devia nascer perguntando "e se a resposta for um pedido para parar?" antes
de decidir a ação — não é um caso de borda raro, é a única resposta que a
operação inteira existe para nunca tratar como oportunidade.

Zero escrita no CRM: item de documentação e especificação pura
(`build-wesales.md` seção 2.9.5 + retoque no gatilho da 2.9.3,
`ROADMAP-SALES-ENGAGEMENT.md` R-17, retoque em `GUIA-MONTAGEM.md`), não
depende de `APROVADO.md` — workflow e filtro de gatilho não saem por API,
igual a todo o resto do projeto.

## Sweep de coerência limpo — a lacuna nova estava nos dados de produção, não no texto — 21/09/2026, sessão automática

Sessão sem tela e sem R-14/F-05/F-06 desbloqueados (mesmo cenário de sempre).
Repeti a varredura que fechou o G-02: `grep` por nome de etapa antigo fora da
tabela 1.0 (limpo — só prosa histórica e a própria tabela), comparação de
merge field usado contra `fieldKey` real via `locations_get-custom-fields`
(zero órfão), e o par de greps que a entrada "A regra certa estava no portão
errado" pediu (réguas que existem vs. réguas que o Mestre de saída remove —
as duas listas fecham: `Cadência 12x30`, `Cadência Inbound`, `Reengajamento
90 dias`). Nada para corrigir — o `ROADMAP-SALES-ENGAGEMENT.md` já avisava
que isso podia acontecer e mandava procurar lacuna nova antes de encerrar
sem commit.

**A lacuna nova não estava em nenhum documento — estava em como os dados
mudaram desde a última leitura.** `opportunities_search-opportunity` por
etapa: `NOVO LEAD` foi de 40 (19/09) para **47** (21/09), todas reais
(Facebook Ads pago, nomes/telefone/e-mail/atribuição de campanha genuínos,
a mais recente criada hoje às 09:17 UTC), e **nenhuma** chegou a `CONECTAR`
— confirma que a lacuna L-07 (`briefing-sdr.md`, "promoção `NOVO LEAD` →
`CONECTAR` é manual, ninguém construiu gatilho") não é mais hipótese: é
lead pago de verdade parado há mais de 24h sem qualquer tentativa, o
oposto exato do que R-02/G-01 foram construídos para garantir. Escalado
como G-03 novo em `ROADMAP-SALES-ENGAGEMENT.md`, com três opções desenhadas
(promoção automática pura, promoção automática com janela de revisão,
ação manual em massa só para destravar o estoque de hoje) — nenhuma
executada: mover 47 oportunidades reais de etapa é ação em massa em dado
de produção (regra 2 do briefing) e a fila manual de hoje é decisão
deliberada do SDR registrada desde a primeira versão do projeto, não bug —
trocá-la é mudança de processo que só o dono decide, mesma régua já usada
para L-02/D-04.

**Regra prática, generalizável:** a varredura de coerência de documentos
(nomes, merge fields, contagens) não é a mesma varredura que detecta uma
lacuna que só aparece em produção — vale reler os números reais da
subconta (`opportunities_search-opportunity` por etapa, não só o total) a
cada rodada sem tela, mesmo com o texto todo consistente, porque uma
lacuna pode ficar dormente por dias até o volume a tornar urgente (mesma
lição, de novo, do achado "número medido dentro de uma instrução tem data
de validade" — lá era uma instrução envelhecendo, aqui é uma lacuna
acordando).

Zero escrita no CRM: as três opções do G-03 ficam propostas, não `[x]` em
`APROVADO.md`. Subconta reconfirmada: 46 campos, mesmas 5 etapas do
`FUNIL DE VENDAS`, 50 oportunidades (47 `NOVO LEAD` + 3 `NEGOCIAR`, dois
leads reais — `Daniel` e `Genilson | Bombeiro` — mais o contato fictício
`Teste Atendeu` do checklist, cujas tags batem com o cenário esperado da
seção 10).

## G-02 fechado: as últimas peças do checklist, e um checklist de teste mandando excluir oportunidade — 21/09/2026, sessão automática

Fechei o que restava do checklist de migração de nomes de etapa
(`GUIA-MONTAGEM.md`, Fase 1; `ROADMAP-SALES-ENGAGEMENT.md`, G-02): seções
2.6.1/2.7/2.8/2.9–2.9.4 (zero achado — já estavam certas, só faltava
marcar), seção 6, seção 8 completa (8.5–8.19), seção 9 e o checklist de
teste inteiro (seção 10). `grep -n "Em cadência\|Nutrição\|Retorno
agendado\|Descartado\|Pré-vendas" wesales/build-wesales.md` confirma:
sobra só tabela de tradução (1.0) e prosa histórica.

**Achado real, sétima ocorrência da mesma classe:** a lista `Recuperação de
No-show` (8.17) tinha um filtro **ativo** comparando etapa contra `Reunião
agendada` — nome que não existe mais na tela desde 18/09/2026. Mesma
classe de bug silencioso já documentada seis vezes nas entradas abaixo
(seção 3, 2.10, 2.11, 2.12, 2.16, família 5.3/5.4): quem escreveu a lista
sabia que a oportunidade fica em `NEGOCIAR` (a própria seção 5.3, migrada
antes, já dizia isso no título de uma subseção), mas a lista em si nunca
recebeu o mesmo tratamento — reforça a regra prática já registrada:
"seções já migradas" não significa "todo lugar que cita aquela seção já
está migrado".

**Achado fora do escopo de nome de etapa, generalizável:** a régua de
prioridade (9.2, regra 1) comparava `Resultado da tentativa = Pediu
retorno` **ou** `etapa = "Retorno agendado"` — a segunda metade do `ou`
nunca podia casar (etapa não existe) e nunca fazia falta (todo lead que
pede retorno já bate na primeira metade). Um `ou` morto não quebra nada
sozinho, mas é peso morto que qualquer leitura futura pode interpretar
como sinal de que a condição da esquerda não basta — removido, mesmo
raciocínio que a lista `Retornos` (8.4) já tinha aplicado.

**Achado que não é de nome de etapa, e por isso quase passou despercebido
numa rodada de G-02:** a última linha do checklist de teste (seção 10)
instruía "**apague as 5 oportunidades** e desative os 5 contatos" ao fim
do teste — viola a regra 1 do projeto (nunca excluir contato, campo, tag,
workflow, pipeline **ou oportunidade**), presente desde a primeira versão
do documento e nunca antes achada porque nenhuma rodada de migração de
etapa tinha motivo para ler essa linha final com atenção. **Regra
prática:** uma varredura de "nome de etapa antigo" não é a mesma varredura
que pega "instrução que viola regra inviolável" — vale reler o documento
inteiro, não só a área do achado que a rodada está caçando, antes de
declarar uma seção fechada. Corrigida para marcar `status = lost` em vez
de excluir.

Zero escrita no CRM: item de documentação pura, não depende de
`APROVADO.md`. Subconta reconfirmada via `opportunities_get-pipelines`/
`locations_get-custom-fields`: mesmas 5 etapas do `FUNIL DE VENDAS`
(`dateUpdated` ainda 18/09/2026 19:56 UTC) e 46 campos personalizados —
sem mudança desde a última rodada.

## Quando a previsão do bug está escrita e o bug acontece do mesmo jeito — 21/09/2026 (causa-raiz do achado 3 da auditoria)

A auditoria de dados desta rodada achou que **os 10 leads nascidos depois do
Mestre de saída ir ao ar chegaram com `limpar-tarefas`**, e registrou o
sintoma sem causa. A causa é o nó 1 do próprio Mestre de saída: gatilho
`Opportunity Stage Changed` para **qualquer** etapa de destino, Porta de
Entrada criando a oportunidade em `NOVO LEAD`, e portão que só encerrava para
`CONECTAR`/`open`. Todo lead novo rodava a limpeza de saída na chegada:
`limpar-tarefas` aplicada e nota "Saída de cadência" num lead que nunca
entrou em régua nenhuma.

O que vale guardar não é o bug, é o formato dele. **A seção 2.12 tinha escrito
essa consequência antes de ela acontecer**, palavra por palavra, como
argumento para o Reengajamento não passar por `NOVO LEAD`:

> "…ele rodaria a limpeza inteira (incluindo aplicar `limpar-tarefas` e
> gravar a nota 'Saída de cadência' num contato que não estava, de fato,
> saindo de cadência nenhuma)… risco de corrida real com a rotina horária de
> manutenção."

O raciocínio estava certo e foi usado para desviar **um** workflow. Ninguém
perguntou "e quem mais passa por `NOVO LEAD`?" — a resposta era *todo lead da
operação*, pelo caminho mais movimentado que existe.

**Regra, a mais afiada da série "achado num lugar, ignorado nos outros N":**
quando uma seção explica por que **evita** um caminho, esse parágrafo é um
relatório de bug sobre o caminho, não uma justificativa de design. A pergunta
seguinte é obrigatória: **quem mais passa por aí, e por que está tudo bem
para eles?** Se a resposta for "ninguém pensou nisso", o bug já existe — só
não foi medido ainda.

Corrigido no nó 1 (`open` **e** etapa em `NOVO LEAD`/`CONECTAR` → encerra) e
na tabela de retoques do `GUIA-MONTAGEM.md`, marcado como o mais urgente dos
que dão para fazer hoje: o workflow está publicado e sujando o histórico de
todo lead que entra.

## A tabela de retoques de tela também é uma lista que alguém esquece de atualizar — 21/09/2026

A rodada do F-05 desenhou o Monitor de Saúde certo e, de quebra, achou um
detalhe fino: a limpeza da tag `novo-lead-estagnado` não podia entrar na
lista do nó 4 do Mestre de saída, porque o portão do nó 1 encerra em no-op
justamente na transição `NOVO LEAD` → `CONECTAR`, que é como o alerta se
resolve. Solução certa: um nó 0 incondicional, antes do portão.

O que faltou: **o Mestre de saída está publicado na tela**, e o nó 0 é
mudança numa peça que já roda. A tabela "retoques de tela pendentes" do
`GUIA-MONTAGEM.md` — que existe exatamente para isso — não recebeu a linha.
Especificação alterada + peça publicada = linha na tabela, sempre.

Duas melhorias que saíram daí:

1. A tabela ganhou a distinção **"dá para fazer hoje"** vs. "espera workflow
   que não existe". Sem isso, quatro linhas bloqueadas escondiam a única que
   estava pronta para executar — o nó 0 não depende de nada.
2. O texto de abertura dizia "**Dois** retoques pendentes" com cinco linhas
   embaixo. Número fixo fora da fonte vira mentira na rodada seguinte, que é
   a regra que o próprio prompt da rotina já manda seguir; agora não conta,
   só aponta para a tabela.

**Padrão, já com nome:** toda vez que uma rodada muda a especificação de uma
peça **publicada**, a pergunta é "onde fica a lista de coisas a mexer na
tela?" — e a resposta tem que ser essa tabela, no mesmo commit. Foi assim
que o R-17 acertou (entrou na tabela sozinho) e assim que o F-05 escorregou.

## `Contains` casa pedaço de palavra: `pare` está dentro de "parece ótimo" — 21/09/2026

A rodada do R-17 achou um bug real e importante (resposta de opt-out no
WhatsApp virava sinal quente: `Prioridade` 5 e tarefa "ligar agora" para quem
pediu silêncio) e desenhou o workflow certo. O problema estava na lista de
palavras-chave: começava com `pare` solto.

`Contains` do GHL casa **substring**, não palavra. `pare` está dentro de
*parece*, *aparelho*, *comparecer*, *preparei*, *separado*, *transparente*.
A resposta mais positiva que um lead brasileiro manda — **"parece ótimo, me
liga"** — contém `pare`. E como o 2.9.3 ganhou o filtro espelhado
(`Doesn't Contain`), o falso positivo custava duas vezes na mesma mensagem:

| O que acontecia com "parece ótimo, me liga" | Onde |
|---|---|
| DND em todos os canais + tag `nao-perturbe` | 2.9.5, nós 2-3 |
| Saída de todas as 6 réguas automáticas | 2.9.5, nó 5 |
| `status` da oportunidade = `lost` | 2.9.5, nó 6 |
| **Nenhuma** tarefa de sinal quente | 2.9.3, filtro espelhado |
| **Nenhum** aviso a ninguém | o único aviso estava no ramo raro do nó 6 |

O lead mais quente do dia virava o lead mais morto do CRM, em silêncio.
Nenhuma automação deste projeto desfaz DND, e nenhuma lista mostra "DND
aplicado hoje".

**Três regras:**

1. **Palavra-chave de opt-out é frase, nunca pedaço.** Antes de pôr uma na
   lista: *ela aparece dentro de alguma palavra comum do português?* `pare` →
   `pare de`/`pare com`. Saíram também `não quero mais` e `não quero receber`
   soltos, porque neste negócio é assim que o lead descreve a dor ("não quero
   mais perder cliente"). E `stop`, que em WhatsApp brasileiro não é palavra
   reservada como o TCPA faz no SMS americano — só traria falso positivo sem
   compensar nada.
2. **Ação irreversível por automação avisa sempre, não só no caminho
   estranho.** O aviso do nó 6 só existia no ramo raro; o caso comum não
   avisava ninguém. Opt-out são poucos por dia por definição, então aviso
   sempre é barato. Regra geral: se a automação faz algo que nenhuma
   automação desfaz, alguém tem que ficar sabendo no minuto.
3. **Duas listas que precisam ser iguais são uma lista com dois lugares.**
   O 2.9.5 e o filtro do 2.9.3 usam a mesma lista de frases. Isso está
   escrito nos dois lados, com "lista canônica" num e "idênticas" no outro —
   sem isso, mexer num lado reabre o bug original (os dois disparando) ou o
   inverso (opt-out que não silencia).

## Gatilho de workflow é evento, não estado: promover lead antes de publicar a régua gasta o evento no vácuo — 21/09/2026

Ao conferir o G-03 (47 leads pagos parados em `NOVO LEAD`, três opções
escritas para o dono escolher), faltava uma precondição que nenhuma das três
mencionava: a `Cadência 12x30` está **em rascunho**. O gatilho dela é
`Opportunity Stage Changed → CONECTAR` — um evento. Promover os 47 agora faz
o evento acontecer sem ninguém escutando, e **publicar a cadência depois não
inscreve quem já está na etapa**: workflow do GHL inscreve no instante do
gatilho, não varre o estado atual do pipeline.

O resultado seria pior que o problema: 47 leads fora de `NOVO LEAD` (logo
fora da lista de triagem) e fora da cadência — um limbo que nenhuma lista
mostra.

**Regra:** antes de qualquer promoção em massa de etapa, conferir se o
workflow que deveria reagir àquela etapa está **publicado**. Régua em
rascunho + movimento em massa = evento gasto. A ordem é sempre publicar,
testar com 1-2 leads, e só então mover o estoque.

Recuperação, se acontecer: `Add to Workflow` em massa pela lista de
contatos, ou tirar e recolocar a etapa para gerar evento novo (o
`Allow Re-entry` desligado da D-06 não bloqueia quem nunca entrou neste
workflow — a própria seção 2.1 do `build-wesales.md` explica por quê). Mas
as duas alternativas tocam dado de produção duas vezes.

## Número medido dentro de uma instrução é verdade com data de validade — 21/09/2026

Varredura depois de dois dias sem sessão ao vivo. A `Fase 1` do
`GUIA-MONTAGEM.md` — a página que o dono abre para clicar — mandava
**excluir 7 etapas** do `FUNIL DE VENDAS`, e justificava assim:

> "confirmado por aqui, via `opportunities_search-opportunity`: **0
> oportunidades no pipeline inteiro**, em qualquer status. Pode apagar sem
> medo de perder negócio real."

Era verdade em 18/09. Em 21/09 o pipeline tem **50 oportunidades** (47 em
`NOVO LEAD`, 3 em `NEGOCIAR`) — a Porta de Entrada ficou rodando. Seguir a
instrução hoje apagaria etapa com oportunidade dentro, que é exatamente a
regra 1 do projeto ("NUNCA exclua"). A mesma seção também mandava renomear
as etapas para os 7 nomes antigos, o que quebraria todo workflow publicado.

O documento **não estava errado quando foi escrito**, e não havia mentira
em lugar nenhum: a correção existia, na seção "Resolvido ao vivo em chat" —
oitenta linhas **depois** do passo a passo. Quem lê de cima para baixo
executa antes de chegar nela.

**Duas regras que saem daqui:**

1. **Instrução destrutiva justificada por medição precisa ser remedida na
   hora de executar.** O número envelhece sozinho e não avisa. Onde o
   documento não puder remedir, ele tem que mandar quem executa remedir.
2. **Correção vai para cima do que ela corrige, não para o fim da seção.**
   Marcar o trecho velho como histórico custa três linhas; deixar a
   correção no rodapé aposta que ninguém lê na ordem.

Aplicado: a Fase 1 ganhou um aviso de bloqueio no topo, com a contagem de
21/09 e o motivo, e o checklist "terminou certo" (que pedia 7 etapas)
ficou marcado como histórico.

## G-02, sexta confirmação do mesmo padrão: "etapa sem status" falha também em nó opcional/de baixa prioridade — 19/09/2026, sessão automática

Fechando as seções 2.13 a 2.17 (Regras de pausa, Distribuição de leads,
Monitor de Capacidade, Higiene de Número, Dashboard do Gestor) do checklist
de migração de nomes de etapa (G-02, `ROADMAP-SALES-ENGAGEMENT.md`). Achado
real só na 2.16 (Higiene de Número — Validação Automática, item **opcional**
do roadmap): o nó 2 do Ramo A (`Invalid`) comparava etapa da oportunidade
contra `Novo lead`/`Em cadência`/`Retorno agendado` (segue) vs. `Conectado`/
`Reunião agendada`/`Nutrição`/`Descartado` (não segue) — nomes que não
existem mais na tela, e a "senão" misturava etapa avançada com status de
saída, que a tabela 1.0 já trata como coisas diferentes.

**Por que registrar mais uma vez o mesmo padrão já anotado para a seção 3,
a 2.12 e a 2.11:** esta é a **sexta** vez que "o nó decide se o lead ainda
está ativo, comparando só contra etapa" se mostra insuficiente — e a
primeira vez que o item era **opcional** (2.16 é o único item de R-13 que
"fica em espera indefinida sem prejudicar o resto" se o plano não cobrir o
recurso). A prioridade baixa do item não isentou o achado: um nó pouco
usado com bug de migração ainda quebra do mesmo jeito quando alguém liga o
recurso um dia. Corrigido para `NOVO LEAD`/`CONECTAR` **e** `status é open`
(segue) vs. `AGENDAR`/`NEGOCIAR` ou `status` já `abandoned`/`lost` (não
segue) — mesma condição composta que a 2.4, a 2.10, a 2.11, a 2.12, o
Mestre de saída e a família 5.3/5.4 já usam. **Regra prática para quem
pegar as seções que ainda faltam (2.6.1, 2.7, 2.8, 2.9-2.9.4, seção 6,
listas 8.5+, seção 9, checklist da seção 10):** a pergunta "este nó decide
se o lead ainda está ativo?" vale a mesma checagem mesmo em seção marcada
como opcional, de baixa prioridade ou pouco usada — o padrão não respeita
prioridade do roadmap.

As outras quatro subseções (2.13, 2.14, 2.15, 2.17) não tinham nó ativo com
nome de etapa antigo: só uma menção solta em texto corrido na 2.13
(`Em cadência` → `CONECTAR`, sem efeito em nó nenhum) e duas referências
informais já esperadas — `Nutrição` em prosa na 2.14 (mesmo uso que a 1.2 e
a 2.12 já fazem para o status `abandoned`) e `Pré-vendas` como apelido do
pipeline na 2.17 (documentado na seção 1 desde a primeira migração). Zero
escrita no CRM nesta rodada — o item é documentação pura (tradução de nome
de etapa), não pede campo, tag ou nó novo, então não depende de
`APROVADO.md`; a subconta foi só relida para reconfirmar estado (detalhe no
fim desta entrada). Trabalho de documentação: `build-wesales.md` (seções
2.13-2.17), `GUIA-MONTAGEM.md` (checklist da Fase 1) e
`ROADMAP-SALES-ENGAGEMENT.md` (item G-02).

Subconta reconfirmada nesta execução via `locations_get-custom-fields`
(`query_model=all`)/`opportunities_get-pipelines`: 46 campos personalizados
(mesma contagem da última checagem), pipeline `FUNIL DE VENDAS` com as
mesmas 5 etapas (`NOVO LEAD`/`CONECTAR`/`AGENDAR`/`NEGOCIAR`/`FORMALIZAR`),
mesma cor e probabilidade, `dateUpdated` ainda 18/09/2026 19:56 UTC — sem
mudança desde a última rodada. As ferramentas do conector `GHL CRM`
apareceram como ferramentas **adiadas** desta sessão (carregadas por
`ToolSearch` antes do primeiro uso, não pré-carregadas na lista inicial) —
registrado aqui só porque o briefing desta rodada avisa para não concluir
"sem acesso" cedo demais: valeu a pena checar antes de assumir.

## "Construir com IA" do GHL não lê os campos personalizados da conta — hipotetiza nome de campo genérico, mesmo depois de corrigido — 19/09/2026, ao vivo em chat

Sessão ao vivo com o dono, montando o `Loop do closer — veredito
pós-reunião` (seção 5.1). Ele usou o assistente "Construir com IA" do
construtor de workflow do GHL, colando um prompt com os nomes reais dos
campos (`Reunião foi qualificada`, `Motivo da desqualificação`, `Nota de
qualificação`). **Resultado, em três tentativas seguidas, cada uma depois
de pedir correção pelo chat da própria IA:**

1. 1ª tentativa: gatilho com filtro em `Tags` (não em `Reunião foi
   qualificada`); ramo "Veredito = Sim" condicionado a um campo
   `Rescheduled` = `True`; ramo "Veredito = Parcial" usando `Opportunity
   status`; um segmento comparando `Lost reason` contra um valor vazio
   (erro "detalhes do segmento ausentes" — a própria IA deixou a
   comparação incompleta).
2. Pedido de correção pelo chat → 2ª tentativa: trocou os campos errados
   por **outros** campos errados (`score` no lugar de `Nota de
   qualificação`, `Last appointment at` no lugar de qualquer coisa
   relacionada à reunião) — não convergiu para os campos reais, só
   redistribuiu o erro.
3. O dono então editou manualmente (fora do chat de IA, direto no nó) o
   gatilho — aí sim ficou certo (`Reunião foi qualificada` / `Foi
   alterado`, mais um segundo filtro `Tags`/`Adicionado` sobrando de uma
   tentativa anterior da IA, removido). Mas o nó de condição seguinte
   (`Se 'Reunião foi qualificada' está vazio?`), apesar de ter o **nome**
   corrigido, manteve a condição de verdade **igual à da 1ª tentativa**
   (`Campo "Tags" não está em branco`) — a IA não limpa o que já colocou
   por trás de um nó só porque o rótulo mudou.

**Nenhum destes campos inventados (`Tags` neste contexto, `Rescheduled`,
`Opportunity status` como condição de veredito, `Lost reason`, `score`,
`Last appointment at`) existe no projeto.** Nenhum deles é nem parecido
com nome de campo nativo do GHL que faria sentido aqui — parecem nomes
genéricos de CRM em inglês que a IA usa como default quando não encontra
(ou não procura) o campo real da conta.

**Regra prática, generalizável, e a segunda confirmação da mesma classe de
falha (a primeira foi o Pós-ligação, `GUIA-MONTAGEM.md`, "Fase 2"/"Estado
da montagem 19/09"):** para qualquer workflow deste projeto que compare
**campo personalizado** em condição (`If/Else`, `Condition` múltiplo,
segmento de filtro), não usar "Construir com IA" do GHL, nem tentar
corrigi-lo pedindo ajuste pelo chat da própria IA — ela troca um campo
errado por outro campo errado em vez de convergir para o certo, e pode
deixar a condição de verdade desalinhada do rótulo do nó (nome certo,
lógica errada por trás). Montar manual, clicando campo por campo no editor
("Point & Edit"), é mais lento no relógio mas não gera esse retrabalho.
Vale só para nós que citam **gatilho ou fluxo simples sem condição sobre
campo personalizado** (ex.: um `Send WhatsApp` isolado) — não testado se a
IA erra também nesses casos mais simples, mas o risco é bem menor porque
não há campo pra confundir.

## A regra certa estava no portão errado: quem *limpa* também precisa conhecer todas as réguas — 19/09/2026 (conferência da rodada acima)

A rodada anterior fechou a 2.11 e generalizou bem: "qualquer nó que decida
'o lead ainda está correndo cadência?' precisa de etapa **e** `status`".
A generalização foi escrita, mas aplicada só no nó que a rodada estava
olhando. Varrendo os outros portões da mesma pergunta, sobraram três:

| Onde | O que faltava | Consequência real |
|---|---|---|
| Seção 2.4, nó 3 (portão do bloco padrão) | `status é open` | Tentativa seguinte rodando para lead já descartado, na janela entre a saída e o `Remove from Workflow` |
| Seção 2.10, nó 2 (mesmo portão na Cadência Inbound) | `status é open` | Idem, e aqui sem rede: ver a linha seguinte |
| Seção 3, nó 2 (Mestre de saída) | Remover também de `Cadência Inbound` e `Reengajamento 90 dias` | **A pior das três:** a limpeza conhecia só a `Cadência 12x30`. Um lead inbound descartado pelo portão de higiene seguia recebendo TI2 a TI5 — tarefa e mensagem — porque a régua que estava rodando não era a que a limpeza removia |

**A lição que não é sobre `status`:** o Mestre de saída estava *certo* no
nó 1 (o portão que a rodada da 2.11 citou como modelo) e *incompleto* no nó
2, escrito quando existia uma régua só. Uma peça pode ter o raciocínio
correto e a lista desatualizada — conferir o portão não conferiu a ação que
vem depois dele. Sempre que uma seção nova criar um workflow que reaproveita
o bloco padrão da 2.4, o nó 2 do Mestre de saída ganha uma linha; isso não
aparece em nenhum grep de nome de etapa.

**Checagem barata, para não depender de lembrar:** toda régua tem título de
tarefa `[CADENCIA]`. O que o Mestre de saída remove tem que ser a mesma
lista.

```
sed -n '/^## 3\. Workflow/,/^## 4\. Workflow/p' wesales/build-wesales.md \
  | grep 'Remove from Workflow'
grep -o '^## 2[.0-9]* Workflow "[^"]*"' wesales/build-wesales.md
```

A segunda lista (as réguas que existem) não pode ter nenhum workflow de
cadência que a primeira (o que o Mestre de saída remove) não tenha. Hoje as
duas fecham em três: `Cadência 12x30`, `Cadência Inbound`,
`Reengajamento 90 dias` — mais `Qualificação por IA no WhatsApp`, que só
aparece na primeira porque não é régua de cadência (seção 2.7).

**Quarta ocorrência, achada na rodada seguinte (mesma lista, outro
workflow):** o nó 3 do Pós-agendamento (seção 5) também removia de
`Cadência 12x30` e não das outras duas réguas. Efeito menor — o nó 1 move
para `NEGOCIAR` e isso aciona o Mestre de saída —, mas o nó 3 existe para
fechar a janela de segundos até a limpeza chegar, então a omissão é a
mesma. E quinta ocorrência no mesmo grep: o ramo `Não ligar` do Pós-ligação
(seção 4), que é o mais caro dos três — na janela entre o nó 4 e a limpeza
cai tarefa de ligação para quem acabou de pedir para não ser procurado.

Conclusão que vale guardar: **`Remove from Workflow` aparece em quatro
lugares deste documento, e cada um tem sua própria lista.** Quando nasce uma
régua nova, o grep é por `Remove from Workflow` em todo o arquivo, não só na
seção 3:

```
grep -n 'Remove from Workflow' wesales/build-wesales.md
```

Dos quatro, só o ramo `Número errado` (seção 4) fica de fora de propósito:
ele não tem lista, delega inteiro ao Mestre de saída, e isso está escrito no
próprio parágrafo dele.

**Onde `status` não entra, de propósito:** o nó 2 da Interceptação de Sinal
(2.9.2/2.9.3) ganhou `status não é lost`, não `status é open`. `abandoned` é
o lead em nutrição, e um clique dele no link de agendar é o único sinal que
o Reengajamento 90 dias (relógio, não sensor) nunca vê. Aplicar a regra
mecanicamente teria trocado um alarme falso por um sinal perdido — pior
troca. Registrado na seção 2.9.2 como decisão do dono, com a linha exata a
mudar se ele preferir o contrário.

Zero escrita no CRM nesta conferência (46 campos e as mesmas 5 etapas
antes e depois, por `locations_get-custom-fields` e
`opportunities_get-pipelines`).

## Migração de etapa: um portão que só olha a etapa também engana um alerta, não só o Mestre de saída — 19/09/2026

Sessão automática, mesmo cenário de sempre (R-14/F-05/F-06 esperando
volume/mensagem real). Continuei o checklist de migração de nomes de etapa
(`GUIA-MONTAGEM.md`, Fase 1) a partir de onde a rodada anterior parou e
fechei a seção 2.11 (Alerta de Speed-to-lead) do `build-wesales.md`.

A tradução mecânica (`Pré-vendas`/`Em cadência` → `FUNIL DE
VENDAS`/`CONECTAR`) era só metade do trabalho. O portão do nó 2 decide se o
alerta dispara comparando "etapa é `Em cadência`" — no plano de 7 etapas,
sair de cadência por qualquer motivo sempre movia a etapa, então bastava.
No modelo real de 5 etapas, o nó 0.0b (seção 2.3, R-13) pode descartar um
lead sem telefone (`Update Opportunity status = abandoned`/`lost`) **sem
tirá-lo de `CONECTAR`**, e isso acontece antes de qualquer tentativa
rodar — exatamente a janela que este alerta observa. Traduzindo só o nome
da etapa, o portão continuaria lendo "ainda em `CONECTAR`, `1ª tentativa
em` vazio" como sinal de atraso, e aplicaria `atraso-1a-tentativa` num lead
que já saiu de cadência, só que por `status`, não por etapa — um alarme
falso, silencioso, sem erro nenhum na tela. Corrigido acrescentando
`status é open` à condição do nó 2, a mesma composta que a seção 3 (Mestre
de saída) já usa.

**Por que isso generaliza, e por que vale procurar antes de traduzir
qualquer seção que sobrar:** esta é a **terceira** seção onde "etapa sem
status" se mostra insuficiente neste modelo (a primeira foi a seção 3, a
segunda a reentrada da 2.12) — qualquer nó que decida algo a partir de "o
lead ainda está correndo cadência?" precisa das duas condições juntas, não
só do nome da etapa. Ao pegar as seções que ainda faltam (2.13 a 2.17,
seção 5 e 5.1-5.4, seção 6, listas 8.5+, seção 9, checklist da seção 10),
vale perguntar primeiro "este nó compara contra etapa para decidir se o
lead ainda está ativo?" antes de assumir que é troca de nome — pelo
histórico das três seções já migradas, a resposta vem sendo "precisa do
`status` junto" mais vezes do que "é só o nome".

Zero escrita no CRM nesta rodada (confirmado por
`opportunities_get-pipelines`/`opportunities_search-opportunity`/
`locations_get-custom-fields` antes de editar: pipeline com as mesmas 5
etapas, 46 campos sem mudança). Trabalho só de documentação:
`build-wesales.md` (seção 2.11), `GUIA-MONTAGEM.md` (checklist da Fase 1)
e `ROADMAP-SALES-ENGAGEMENT.md` (item G-02).

**Achado à parte, não relacionado à seção 2.11, registrado para a próxima
rodada não redescobrir sozinha:** das 40 oportunidades, 39 seguem em
`NOVO LEAD`, mas o contato `Daniel` (`c0uQwq5EqYM0vA8SGA0W`) apareceu em
`NEGOCIAR` com a tag `limpar-tarefas`, `lastStageChangeAt` 19/09/2026
06:41 UTC — a primeira oportunidade do projeto inteiro que já saiu de
`NOVO LEAD`. Como nenhum workflow deste projeto está publicado ainda
(`GUIA-MONTAGEM.md`, Fases 3+ seguem manuais), é mais provável mão humana
na tela do que automação; não investiguei mais fundo porque é read-only e
fora do escopo desta rodada (G-02), mas fica registrado para quem pegar o
próximo item não estranhar o número mudando sem explicação.

## Migração de etapa: reentrar em `CONECTAR` sem resetar `status` engana o Mestre de saída — 19/09/2026

Sessão automática, sem os três itens do roadmap desbloqueados (R-14/F-05/F-06
seguiam todos esperando volume/mensagem real, mesmo motivo já documentado na
entrada abaixo). Em vez de encerrar sem commit, voltei para o checklist de
migração de nomes de etapa que `GUIA-MONTAGEM.md` (Fase 1) já rastreava desde
18/09/2026 com várias seções ainda `[ ]` — um `build-wesales.md` que ainda
cita `Em cadência`/`Nutrição` como se fossem etapa é o mesmo tipo de bug
silencioso que o achado de `fieldKey` (abaixo) e o R-16 já descreveram para
merge field e rótulo de opção, aqui em nome de etapa: um gatilho ou portão
que compara contra etapa que não existe nunca casa, e ninguém vê erro nenhum
na tela até notar que o workflow simplesmente não dispara. Fechei a seção
2.12 (Reengajamento 90 dias) — a maior pendência do checklist, sinalizada
como tal desde a entrada "Seção 3... 18/09/2026" abaixo.

**Achado que a tabela de tradução (seção 1.0 do `build-wesales.md`) não
previa, generalizável para o resto do checklist:** qualquer workflow que
reative uma oportunidade **de volta** para `CONECTAR` depois que ela passou
por `status = abandoned`/`lost` precisa resetar o `status` para `open`
explicitamente, no mesmo nó que muda a etapa. Motivo: o Mestre de saída
(seção 3) decide se limpa ou não pela condição composta "etapa é `CONECTAR`
**e** `status` é `open`" — ela existe justamente porque, no modelo de 5
etapas, sair de cadência nem sempre move etapa (vira só mudança de
`status`). Se um workflow de reativação mover a etapa sem tocar no
`status`, a oportunidade chega em `CONECTAR` ainda com `status = abandoned`
da rodada anterior: a condição composta fica falsa, e o Mestre de saída lê a
**chegada** como se fosse uma **saída**, disparando a limpeza (tirar de
fila, apagar tag) no exato momento em que o lead está entrando de novo na
cadência — o oposto do "no-op" que todo o desenho pressupõe para entrada.
2.12 tinha exatamente esse buraco (nó "Reentrada no funil"); corrigido
adicionando `status → open` ao mesmo nó que move a etapa. **Ao migrar
2.10, 2.13 ou qualquer outra seção que mova oportunidade de volta para
`CONECTAR`, conferir se ela também precisa desse reset** — não é
específico do Reengajamento, é uma propriedade do modelo de 5 etapas +
status que a migração de 18/09/2026 introduziu sem essa peça.

Zero escrita no CRM nesta rodada (confirmado por
`opportunities_get-pipelines`/`opportunities_search-opportunity`/
`locations_get-custom-fields` antes de editar: pipeline com as mesmas 5
etapas, custom fields sem mudança desde o R-16/F-04 — nenhum C-25/C-26/C-27
novo ainda, esperado, são criação manual pendente). Trabalho só de
documentação: `build-wesales.md` (seção 2.12 e a linha da seção 2.1 que
apontava para ela), `GUIA-MONTAGEM.md` (checklist da Fase 1) e
`ROADMAP-SALES-ENGAGEMENT.md` (novo item G-02, Bloco 0, registrando esta
frente de trabalho para quem só lê o roadmap).

## F-04 fechado: a exposição real não era a do enunciado do roadmap — 19/09/2026

Auditoria desta rodada (`locations_get-custom-fields`, `opportunities_get-pipelines`,
`opportunities_search-opportunity`) reconfirmou: 46 campos (sem mudança desde
o R-16), pipeline `FUNIL DE VENDAS` com as mesmas 5 etapas, **40 oportunidades,
todas `open` em `NOVO LEAD`** (nenhuma ainda promovida a `CONECTAR` — L-07
continua aberto por decisão, não por bug). Rodei também o grep de merge field
órfão (`contact\.[a-zA-Z0-9_]*` em todo `wesales/*.md` contra os `fieldKey`
reais) que o achado do `fieldKey` (abaixo) recomenda depois de qualquer
criação de campo em lote: **zero órfãos** — as correções anteriores seguram.

Com tudo isso batendo e nenhum item do roadmap literalmente aberto e
desbloqueado (R-14/F-04/F-05/F-06 eram os quatro sem `FEITO`, e os quatro
tinham motivo documentado para esperar), quase fechei a rodada sem commit.
Antes disso, reli o "Como" do F-04 com calma e achei que o motivo original
("lead em duas cadências recebe o dobro de toques") não é o risco real deste
projeto: Cadência Inbound e Cadência 12x30 já são mutuamente exclusivas por
tag no próprio gatilho (R-07), e o Reengajamento já blinda a 12x30 contra
reentrada dupla (T-13, R-08). **Quem não tem nenhum teto é a Interceptação de
Sinal (F-01, seção 2.9):** ela roda com `Allow Re-entry` ligado de propósito
("cada clique é um sinal novo") em paralelo com qualquer cadência, sem saber
quantos toques a cadência principal já gastou — um lead que clica o link ou
responde várias vezes no mesmo dia empilha tarefa + aviso ao SDR sem limite
nenhum. Esse é o achado que tornou o F-04 buildável de verdade nesta rodada,
em vez de mais uma linha "precisa de volume" — a exposição já existe hoje,
independente de volume.

**Regra prática, generalizável:** quando um item do roadmap tem um "Como" que
parece vago ou já coberto por outro mecanismo, vale reler os itens vizinhos
(aqui, F-01) antes de assumir que o item inteiro está bloqueado por falta de
dado. Às vezes o "Como" original mirou no lugar errado e o item mesmo assim
vale a pena, só que por um motivo mais específico do que o enunciado original.

Desenho escolhido, pesquisado contra o mercado antes de montar: Outreach.io
resolve "duas sequências" com **Sequence Exclusivity** — trava de
**admissão**, não de frequência (`support.outreach.io/hc/en-us/articles/
360001587093-Sequence-Exclusivity-Settings`). Não serve para o caso real
encontrado aqui (não são duas cadências ao mesmo tempo, é sinal em paralelo
por desenho). Optei por um contador `NUMERICAL` por contato, janela **móvel**
de 7 dias (soma no toque, desconta 7 dias depois — o próprio workflow agenda
o desconto via `Wait → Time Delay`), acionado por uma tag-pulso (`toque`,
T-15) que qualquer nó de toque aplica e o workflow "Contador de Toques" já
remove no primeiro nó — mesma lógica de "tag como pulso de evento" que a
Interceptação de Sinal já usa, evitando a armadilha que o R-02 documentou
(aritmética de data não funciona sobre campo `TEXT`, e não existe campo de
data com hora — um contador incremental em `NUMERICAL` não tem esse problema).
Detalhe completo: `build-wesales.md`, seção 2.19.

**Escopo explícito, não esquecimento:** o toque e o portão de teto só foram
ligados nos dois pontos de maior risco (Cadência 12x30 e as duas
Interceptações de Sinal) nesta rodada — Cadência Inbound, Reengajamento e
Recuperação de No-show reaproveitam o mesmo mecanismo sem precisar de nada
novo, só falta ligar o nó em cada uma (registrado em `build-wesales.md`,
seção 2.19, tabela "Onde o toque é emitido").

## Pesquisa que corrobora (não fecha) o `{{right_now}}` em aberto no `GUIA-MONTAGEM.md` — 19/09/2026

O `GUIA-MONTAGEM.md` tem um item não marcado, "Antes da Fase 5, resolver
`{{right_now}}`", pedindo para alguém abrir `Update Contact Field` → `Entrada
em` na tela e ver se existe uma opção de data/hora atual — a sessão ao vivo já
tinha testado isso na tela e não achou. Rodei `WebSearch` (esta rotina não tem
acesso à tela, só à API) para tentar corroborar ou refutar isso à distância,
sem conseguir fechar o item (só quem tem a tela aberta fecha), mas achei duas
peças que reforçam o achado ao vivo, confiança média (não é leitura direta do
texto oficial — `help.gohighlevel.com` e `ideas.gohighlevel.com` seguem
bloqueados pelo proxy deste ambiente, mesma limitação de sempre):

1. **"Right Now Merge Fields" existe e é documentado**, mas como parte do
   guia oficial "Merge Fields Guide for **Personalized Messages and
   Documents**" — ou seja, o caso de uso documentado é composição de
   mensagem/documento (SMS, e-mail, `{}` dentro da caixa de texto de um
   envio), não a ação de workflow `Update Contact Field` sobre um campo de
   contato.
2. Um changelog oficial (`ideas.gohighlevel.com/changelog/update-contact-
   field-action-dynamic-custom-value-picker-expanded-field-support`, achado
   só por `WebSearch`) descreve uma expansão **recente** do seletor de valor
   dinâmico da ação `Update Contact Field` para os tipos **Numeric,
   Select/Dropdown e Monetary** — não cita `Text` nem `Date`, e mesmo essa
   expansão é sobre copiar de "passos anteriores ou campos já armazenados",
   não sobre inserir um relógio ao vivo.

Nenhuma das duas fontes confirma nem nega 100% — é evidência circunstancial
de que campo `TEXT` na ação `Update Contact Field` provavelmente não expõe
"agora" como valor pronto, o que bate com o que a sessão ao vivo já viu na
tela. **Não fechei o checkbox do `GUIA-MONTAGEM.md`** porque isso exige
alguém com a tela aberta confirmando, não pesquisa à distância — deixo aqui
para quem for testar não precisar repetir a mesma busca.

## Auditoria escrita não é auditoria aplicada — 19/09/2026

`CONFERENCIA-CAMPOS.md` já existia com um levantamento completo, feito em
18-19/09, comparando a tela contra `campos-e-tags.md`: nove campos
(`Q-01, Q-04, Q-06, Q-08, Q-10, Q-12, Q-15, Q-17, Q-18`) tinham nome, opção
ou tipo diferente do que a especificação sugeria. O arquivo até dizia
literalmente, na sua própria conclusão (`GUIA-MONTAGEM.md`, seção
"Pendências que sobraram"): "a régua de qualificação... precisa ser
reescrita para usar os rótulos reais... tarefa de documentação ainda
pendente". Essa rodada leu isso, conferiu `locations_get-custom-fields` de
novo e achou os rótulos **ainda errados** em `campos-e-tags.md` e na seção
9.1 do `build-wesales.md` — o achado tinha sido catalogado, nunca aplicado.

**Por que isso importa:** a régua de nota (seção 9.1) compara texto em
`If/Else`. Rótulo sugerido que não existe mais na tela nunca casa — a
mesma classe de erro silencioso que o achado de `fieldKey` logo abaixo já
descreve para merge field, só que aqui o efeito é pior: a nota de
qualificação do lead sai errada sem nenhum erro visível, e ninguém percebe
porque o workflow não quebra, só pontua mal.

**Regra prática, generalizável:** quando um documento de auditoria lista
"ajustar o documento" como próximo passo, isso é uma tarefa em aberto, não
um problema resolvido — confira se a edição foi feita de verdade nos
arquivos de especificação antes de assumir que aparecer no arquivo de
auditoria significa que já está corrigido. Um achado escrito e um achado
corrigido são coisas diferentes, e só o segundo protege o workflow.

## Como matar a classe de erro do `fieldKey`, em vez de um por vez — 19/09/2026

O GHL **remove** a letra acentuada ao gerar o `fieldKey`, não translitera:
`anúncios` → `anncios`, `qualificação` → `qualificao`, `agência` → `agncia`,
`Tentativa nº` → `tentativa_n`. Escrever "como se lê" dá merge field em branco,
e o erro não aparece em teste nenhum: a nota sai com um pedaço faltando e
ninguém nota.

Corrigir um nó por vez não fecha o buraco — em 19/09 houve dois commits
seguidos achando o mesmo `tentativa_no` em lugares diferentes (nó 6 do Mestre
de saída, depois nó 9 do Pós-ligação), e ainda sobraram quatro chaves erradas
que nenhum dos dois pegou. **A verificação que fecha de uma vez** é comparar
tudo que o documento cita contra o que a subconta tem:

```
# o que os documentos citam
grep -rho "contact\.[a-z0-9_]*" wesales/*.md | sort -u > /tmp/usados.txt
# o que existe de verdade: os fieldKey de locations_get-custom-fields
# mais os nativos (first_name, last_name, name, phone, email, company_name)
comm -23 /tmp/usados.txt /tmp/reais.txt
```

Saída vazia = nenhum merge field órfão. Em 19/09 essa comparação achou quatro
de uma vez (`motivo_da_desqualificacao`, `n_de_no_shows`,
`nota_de_qualificacao`, `reuniao_foi_qualificada`), corrigidos no mesmo commit.
**Rode isto depois de qualquer rodada que acrescente merge field**, e depois de
criar campo novo na tela — é mais barato que descobrir pela nota vazia.

## Pesquisa de mercado que valeu a pena guardar (F-02) — 19/09/2026

Pesquisado ao especificar o horário aprendido por segmento
(`ROADMAP-SALES-ENGAGEMENT.md`, F-02; mecanismo em `build-wesales.md`,
seção 2.18): a literatura de outbound (Gong.io, HubSpot, achada por
`WebSearch`) converge em janelas **médias de mercado** — manhã tarde
(10h-11h) e fim de tarde (16h-17h) — como melhor horário de ligação, sem
segmentar por indústria do lead. **Salesloft** anuncia send-time
optimization (recurso "Rhythm") só para e-mail; a documentação de
**Outreach** fala em "segment-level analysis" para desempenho de
mensagem, não em horário de ligação aprendido por segmento. Nenhuma das
duas plataformas de prateleira citadas no enunciado do projeto aprende
horário de **ligação** por segmento a partir da conexão real da própria
base do cliente — é a lacuna que o F-02 fecha, e é o tipo de diferencial
que um concorrente não replica só olhando a tela, porque o dado é da
operação, não do produto.

**Confiança média, não confirmado na tela:** se a ação `Date/Time
Formatter` do GHL aceita um "To Format" que isola só a hora (`HH`) de um
carimbo completo — achado só por busca (`growthable.io`, `consultevo.com`,
`gohighlevele.com`); `help.gohighlevel.com` segue bloqueado pelo proxy
deste ambiente para leitura direta, mesma limitação registrada desde o
R-09. A ação existe e aceita formato customizado de saída — confirmado por
três fontes convergentes —, mas o token exato para "só a hora" precisa ser
confirmado na tela antes de montar os nós 7b/7c da seção 4. Se a tela não
oferecer esse recorte, o plano B documentado na seção 2.18 é gravar
`{{right_now}}` completo (como C-14/C-18/C-19 já fazem) e o gestor lê os
dois últimos dígitos de hora na lista 8.19 — mais trabalho manual, mesmo
dado.

## A migração de pipeline vazou para fora de `build-wesales.md` — `rotina-limpar-tarefas.md` também citava as 7 etapas antigas — 19/09/2026

O checklist de migração do `GUIA-MONTAGEM.md` ("Fase 1") só rastreia seções
de `build-wesales.md`. Ao revisar coerência entre documentos antes de pegar
um item do roadmap, achei que `rotina-limpar-tarefas.md` — um prompt
**autocontido**, feito para rodar numa rotina separada sem depender desta
conversa — ainda buscava oportunidades no pipeline `"Pré-vendas"` (nome que
nunca existiu na tela; o pipeline real chama `FUNIL DE VENDAS`, reaproveitado
por decisão do dono) e mapeava prefixo de tarefa pelas 7 etapas do plano
abandonado, incluindo `Retorno agendado` como se ainda fosse etapa própria.

**Por que isso não apareceu antes:** a rotina nunca rodou de verdade contra
o pipeline real — a subconta ainda tem 0 oportunidades, então o PASSO 2 do
prompt nunca teve o que buscar. Um bug assim só aparece na primeira vez que
alguém tentar rodar a rotina com oportunidade de verdade na tela.

**Achado que generaliza para qualquer migração futura de nome de
etapa/pipeline:** o `grep` de verificação do `GUIA-MONTAGEM.md` está escopado
só a `wesales/build-wesales.md` — qualquer outro arquivo do projeto que cite
etapa por nome literal (não pela tabela de tradução 1.0) precisa do mesmo
grep rodado contra ele. Rodei `grep -rn` pelos nomes antigos em todo o
`wesales/` desta vez; os outros arquivos que aparecem (`ROADMAP-SALES-ENGAGEMENT.md`,
`APRENDIZADOS-CRM.md`, `briefing-sdr.md`, `biblioteca-mensagens.md`,
`auditoria-*.md`) usam o nome antigo só como narrativa histórica ou como
termo conceitual já coberto pela convenção da tabela 1.0 — não como valor
literal que uma chamada de API vai comparar contra a tela. Só
`rotina-limpar-tarefas.md` tinha os dois problemas ao mesmo tempo (nome de
pipeline errado E comparação literal de etapa), porque é o único documento
do projeto, fora de `build-wesales.md`, escrito para ser colado direto numa
sessão que fala com o CRM.

**Correção:** detalhe completo em `rotina-limpar-tarefas.md` (PASSO 2/3
reescritos) e `GUIA-MONTAGEM.md` (novo item marcado na lista de migração).
A régua nova também passou a checar o `status` da oportunidade, não só a
etapa — sem isso, um lead que esgotou as 12 tentativas (`status = abandoned`,
parado em `CONECTAR`) teria as tarefas `[CADENCIA]` tratadas como válidas
para sempre, porque `CONECTAR` sozinho não diferencia "ainda na régua" de
"saiu sem mudar de etapa" (a maioria das saídas de cadência no modelo de 5
etapas muda só o `status`, não a etapa — tabela 1.0, `build-wesales.md`).

## Migração das 5 etapas continuou: Seção 3 (Mestre de saída) precisava de um segundo gatilho, não só troca de nome — 18/09/2026

A tarefa de migração aberta em `GUIA-MONTAGEM.md` ("Fase 1", checklist de
seções) tratava a maioria das seções como troca de nome (`Em cadência` →
`CONECTAR` etc.). Ao migrar de verdade a seção 3 (Mestre de saída) e a seção
4 (Pós-ligação), apareceu um problema que troca de nome sozinha não resolve:
no plano de 7 etapas, **toda** saída de cadência (conectou, número errado,
não ligar, 12 tentativas esgotadas) era um movimento de etapa, e um gatilho
só de `Opportunity Stage Changed` bastava para a limpeza rodar. Na tela
real (5 etapas), só "conectou" continua sendo movimento de etapa
(`CONECTAR` → `AGENDAR`) — os outros três viraram `status` da oportunidade
(`abandoned`/`lost`) **sem sair de `CONECTAR`** (é a própria tradução já
registrada na tabela 1.0 de `build-wesales.md`, seção 1.0). Um Mestre de
saída só com `Opportunity Stage Changed` deixaria de limpar a fila para o
caminho mais comum de saída (12 tentativas esgotadas nunca move etapa) —
teria ficado tag `fila-tel`/`fila-wa` presa em quase todo lead que esgota a
régua sem conectar, sem ninguém perceber até a fila entupir.

**Pesquisado antes de corrigir, confiança alta (WebSearch, não bloqueado
pelo proxy deste ambiente):**
- **`Opportunity Status Changed` é gatilho nativo, separado de
  `Opportunity Stage Changed`/`Pipeline Stage Changed`** — dispara quando o
  `status` da oportunidade muda (`open`/`won`/`lost`/`abandoned`), com
  filtro por status de destino. Fonte:
  `help.gohighlevel.com/support/solutions/articles/155000003252-workflow-trigger-opportunity-status-changed`
  (achado só por `WebSearch`, que roda fora do proxy bloqueado; o domínio
  `help.gohighlevel.com` em si segue inacessível por `WebFetch` direto,
  mesma limitação já registrada desde o R-09).
- **Um workflow do GHL aceita mais de um gatilho, em OR** — "stack multiple
  triggers on one workflow", confirmado por várias fontes de busca
  convergentes (`growthable.io`, `howtohighlevel.com`, `tkturners.com`).
  Isso é o que permite o Mestre de saída escutar `Opportunity Stage Changed`
  **e** `Opportunity Status Changed` no mesmo workflow, sem duplicar a
  lógica de limpeza em dois lugares — regra prática, generalizável para
  qualquer item futuro que precise reagir a "duas formas diferentes de
  chegar no mesmo estado final" (ao contrário de "dois relógios correndo em
  paralelo", que aí sim pede dois workflows — achado já registrado no R-12).

**A correção, resumida:** o portão (nó 1) do Mestre de saída trocou de
"etapa de destino é `Em cadência` → encerra" para "etapa **é** `CONECTAR`
**E** `status` **é** `open` → encerra". A condição composta cobre os dois
gatilhos com uma regra só: verdadeira só quando o lead está de fato correndo
a cadência ainda (entrando ou no meio dela), falsa em qualquer saída real —
movimento de etapa ou mudança de status. Detalhe completo, com os casos
percorridos um a um (entrada, 12 esgotadas, número errado, não ligar,
atendeu, progressões seguintes): `build-wesales.md`, seção 3.

**Progresso desta rodada no checklist de migração** (detalhe em
`GUIA-MONTAGEM.md`, "Fase 1"): seção 3 (Mestre de saída) e seção 4
(Pós-ligação) migradas por completo; dentro da seção 2, as subseções 2.1
(gatilho), 2.3 (nó 0.0b) e 2.4 (nó 3) migradas, mais o fim da 2.6 (M3 → 12
tentativas esgotadas); dentro da seção 8, as listas 8.1 a 8.4. Continuam
usando o nome antigo (tradução pela tabela 1.0 até serem migradas): 2.10,
2.11, 2.12 (a maior peça que falta — o gatilho dela hoje é `Opportunity
Stage Changed → Nutrição`, que não existe mais como etapa, precisa virar
`Contact Tag Added → nutricao-90d`), 2.13 a 2.17, seção 5 e 5.1–5.4, seção
6, seção 8.5 em diante, seção 9, e o checklist de teste da seção 10.

**Reconfirmado nesta rodada:** pipeline `FUNIL DE VENDAS` continua com as
mesmas 5 etapas (`NOVO LEAD`/`CONECTAR`/`AGENDAR`/`NEGOCIAR`/`FORMALIZAR`,
mesma probabilidade e cor, `dateUpdated` ainda 18/09/2026 19:56 UTC — sem
mudança desde a última verificação) e os campos personalizados batendo com
`campos-e-tags.md` — quantos existem de fato, e onde divergem da
especificação, fica em `CONFERENCIA-CAMPOS.md`, que é quem compara os dois
lados. Nenhuma escrita no CRM nesta rodada: o trabalho foi
só migração de documento, sem campo/tag/contato novo exigido.

## Fase 2 (campos) começou fora de ordem, e 3 dos 24 campos não batem com a especificação — 18/09/2026 ~21h UTC

Rodada anterior tinha reconfirmado "0 campos, 0 contatos" ao fechar o
R-15 (mesma checagem repetida cinco vezes seguidas até ali, sempre igual).
Esta rodada, a mesma chamada (`locations_get-custom-fields`) devolveu
**24 campos**, todos com `dateAdded` entre 20:18 e 21:01 UTC de
18/09/2026 — trabalho manual de verdade na tela, não coisa desta rotina
(o conector `GHL CRM` não tem ferramenta de criar campo, ver seção
"O que o conector cria e o que não cria" abaixo).

**Regra prática, generalizável: nunca confie só na contagem depois de uma
criação em lote manual — confira nome e tipo, campo a campo, contra
`campos-e-tags.md`.** Rodei essa conferência linha a linha e achei três
divergências que a contagem batendo (24 campos ≈ ~24 esperados) teria
escondido:

1. **Dois campos da tabela não existem**: C-03 (`WA não atendidas
   seguidas`) e C-04 (`Permissão WhatsApp`) — o segundo é o campo mais
   referenciado do projeto depois de `Tentativa nº`/`Resultado da
   tentativa` (14+ pontos do `build-wesales.md`).
2. **Um campo tem o tipo errado**: C-11 (`Conexões telefone`) foi criado
   como `PHONE`, não `NUMERICAL` — quebra a ação `Math: + 1` que o
   Pós-ligação precisa fazer nele.
3. Uma opção de picklist com capitalização diferente da documentação
   (`Caixa Postal` vs. `Caixa postal`) — cosmético, não bloqueia nada.

Detalhe completo, com as fontes de pesquisa sobre "dá para editar o tipo
de um campo depois de criado" (resposta: não, só apagar e recriar) e o
checklist de correção: `GUIA-MONTAGEM.md`, seção "Fase 2 — Campos
personalizados (verificação do que já foi criado)".

**Por que isso importa além deste achado específico:** a Fase 1
(pipeline) segue travada sem confirmação há mais de uma rodada (ver
achado abaixo), e mesmo assim alguém já avançou para a Fase 2 por fora da
ordem do `GUIA-MONTAGEM.md`. Regra prática: não assumir que as fases
avançam em ordem só porque o guia sugere isso — reconferir o estado real
da subconta inteira (pipeline **e** campos) a cada rodada, não só a peça
que a rodada anterior estava tratando.

## O `FUNIL DE VENDAS` mudou de novo, e não para o desenho do projeto — 18/09/2026 ~20h UTC

Rodada anterior fechou às 19:52 UTC com o `GUIA-MONTAGEM.md` recém-criado,
ensinando a Fase 1 (editar as 14 etapas antigas para as 7 do projeto).
Esta rodada reconferiu o pipeline (`opportunities_get-pipelines`) antes de
pegar o próximo item do roadmap, como toda rodada faz — e desta vez o
resultado **mudou**: `dateUpdated` do pipeline marca 19:56 UTC, 4 minutos
depois daquele commit. Só que o que está lá agora não são as 7 etapas
pedidas: são 5 etapas novas (`NOVO LEAD`, `CONECTAR`, `AGENDAR`,
`NEGOCIAR`, `FORMALIZAR`, probabilidade redonda de 10 em 10: 30/40/50/60/
70%), nenhuma batendo em nome com `Em cadência`/`Conectado`/`Retorno
agendado`/`Reunião agendada`/`Nutrição`/`Descartado` a partir da posição
1. Detalhe completo, tabela lado a lado e as duas hipóteses (início
manual com estilo próprio vs. reaplicação de snapshot da agência):
`GUIA-MONTAGEM.md`, seção "Verificação em 18/09/2026, ~20h UTC".

**Verificado antes de reagir, não só assumido:** `opportunities_search-opportunity`
(`query_status=all`) no pipeline confirmou **0 oportunidades** — nenhum
dado de negócio foi perdido nessa troca, então não há urgência de conter
dano, só de não seguir construindo (Fase 2 em diante) em cima de nomes de
etapa que não existem na tela.

**Regra prática, generalizável para qualquer rodada futura que dependa de
nome exato de etapa de pipeline (todo gatilho `Opportunity Stage Changed`
do projeto depende disso):** não confiar que uma verificação de uma
rodada atrás continua valendo — o pipeline é a única peça deste projeto
que muda por fora da rotina (edição manual na tela, ou possivelmente
snapshot de agência) e sem aviso. Reconferir via `opportunities_get-pipelines`
a cada rodada antes de assumir que os nomes de etapa batem com
`build-wesales.md`, exatamente como já se fazia para campo/tag/contato —
a diferença é que campo/tag só cresciam (nunca regrediam), e o pipeline
acabou de mostrar que pode mudar de forma incompatível com o desenho.
Nenhum item do roadmap foi fechado nesta rodada por causa disso: builder
em cima de nome de etapa que não existe seria trabalho perdido na certa.

## "Não sai por API" tinha dois motivos diferentes — separados em 18/09/2026

Até esta rodada, o documento inteiro tratava "campo personalizado", "pipeline",
"workflow" e "calendário/formulário" como o mesmo tipo de bloqueio: "não sai
por API, só na tela". Pedido do dono ("estude a documentação oficial, blogs,
comunidades") levou a checar isso a sério, e a resposta **não é uma coisa só**.

**Método:** `highlevel.stoplight.io` e `marketplace.gohighlevel.com`
continuam bloqueados pelo proxy de rede deste ambiente (mesma limitação já
registrada para R-09/R-13). Em vez de desistir na busca, a verificação foi
direto na fonte: `github.com/GoHighLevel/highlevel-api-docs`, o repositório
público oficial que alimenta aqueles sites (README confirma: "source
documentation for the GoHighLevel API V2"). Ler o JSON OpenAPI de cada
recurso é leitura de spec, não snippet de busca — **confiança alta** nos
pontos abaixo, marcados um a um.

**Pipeline (criar) — confirmado NÃO EXISTE na API, é limitação da
plataforma.** `apps/opportunities.json` e `apps/v3/opportunities-v3.json`
só têm `GET /opportunities/pipelines`; `docs/oauth/Scopes.md` confirma que
`opportunities.write` cobre criar/mover/excluir **oportunidade**, não
pipeline. Existe uma issue aberta no próprio repo oficial pedindo isso
(`github.com/GoHighLevel/highlevel-api-docs/issues/248`, "Create Pipelines
and Stages API", sem resposta de implementação) — confirma que nem
desenvolvedores terceiros conseguem. Achado curioso, não conclusivo: existe
uma string de escopo `pipelines.create` dentro de `apps/v3/users-v3.json`
(a API de permissões de usuário), órfã — nenhum endpoint documentado a usa.
Pode ser um recurso interno ainda não exposto. **Não confie em criar
pipeline por API até essa issue fechar.**

**Workflow (criar/publicar) — confirmado NÃO EXISTE, é limitação da
plataforma.** `apps/workflows.json` só tem `GET /workflows/`. Sem POST em
nenhuma versão do spec. Existe workaround parcial (não é criar workflow):
Custom Workflow Actions/Triggers via Marketplace deixam um app aparecer
como passo dentro de um workflow que um humano monta na tela — não cria o
workflow em si.

**Formulário (criar) — confirmado NÃO EXISTE, é limitação da plataforma.**
`apps/forms.json` só tem `GET /forms/` (listar), `GET /forms/submissions`
(ler respostas) e `POST /forms/upload-custom-files` (upload de arquivo
anexado a uma resposta, não cria estrutura de formulário).

**Campo personalizado (criar) — EXISTE na API oficial. É este conector que
não implementa, não a HighLevel.** `apps/locations.json` documenta
`POST /locations/{locationId}/customFields`, escopo
`locations/customFields.write`. Corpo obrigatório: `name` + `dataType`
(TEXT, NUMERICAL, PHONE, RADIO, CHECKBOX etc.); opcional `model` (`contact`
ou `opportunity` — um endpoint só, os dois tipos de campo deste projeto) e
mais placeholder/position/opções de lista. Existe também GET/PUT/DELETE por
ID e upload para campo de arquivo. **Toda a Etapa 2 deste projeto (os ~24
campos de `campos-e-tags.md`) poderia sair por API — só não sai porque o
conector `GHL CRM` conectado nesta sessão não tem essa ferramenta.**

**Calendário (criar) — EXISTE na API oficial. Mesmo caso do campo.**
`apps/calendars.json` documenta `POST /calendars/`, escopo
`calendars.write`, corpo obrigatório `locationId`+`name`, e dezenas de
campos opcionais (`slotDuration`, `openHours`, `availabilities`,
`teamMembers`, `formId`, `eventType`, tipo de calendário, buffers,
confirmação automática). Também há `POST /calendars/groups`,
`POST /calendars/schedules`, `POST /calendars/resources/{resourceType}`.
**O calendário `Reunião com closer` (seção 7.1 do `build-wesales.md`)
poderia sair por API** — mesmo motivo do campo: o conector atual só expõe
leitura de calendário (`calendars_get-appointment-notes`,
`calendars_get-calendar-events`), não criação.

**O que fazer com isso:** fechar o gap não depende de esperar a HighLevel
lançar nada — depende de trocar/ampliar o conector. Duas rotas conhecidas,
nenhuma delas testada ainda nesta subconta: (1) o toolkit HighLevel via
**Composio**, citado desde a primeira rodada em `briefing-sdr.md` ("Estado
do acesso") como caminho alternativo — este ambiente tem ferramentas
`mcp__Composio__*` presentes, mas **nenhuma conta HighLevel conectada por
Composio ainda** (a lista de apps já conectados via Composio, vista nesta
rodada, não inclui HighLevel/GoHighLevel — só facebook, googlecalendar,
googledrive, instagram, metaads, pexels, youtube); conectar exigiria um
fluxo de OAuth que só o dono da conta pode autorizar (link clicável), então
não é algo para a rotina fazer sozinha sem perguntar antes. (2) Pedir para
quem administra o conector `GHL CRM` (fora desta rotina) adicionar as duas
ferramentas que faltam. Enquanto nenhuma das duas acontecer, campo e
calendário continuam manuais na prática, mesmo não sendo limitação da
HighLevel.

Fontes lidas direto (alta confiança), todas em 18/09/2026:
- `github.com/GoHighLevel/highlevel-api-docs` (README)
- `.../blob/main/apps/opportunities.json`, `.../apps/v3/opportunities-v3.json`
- `.../blob/main/apps/locations.json`
- `.../blob/main/apps/workflows.json`
- `.../blob/main/apps/calendars.json`
- `.../blob/main/apps/forms.json`
- `.../blob/main/docs/oauth/Scopes.md`
- `.../blob/main/apps/v3/users-v3.json`
- `github.com/GoHighLevel/highlevel-api-docs/issues/248`

Fontes só de busca (confiança média, corroboram sem serem prova primária):
`marketplace.gohighlevel.com/docs/ghl/locations/create-custom-field/`,
`.../custom-fields/custom-fields-v-2-api/`, `.../calendars/calendars/`,
`.../forms/forms-api`, `ideas.gohighlevel.com/apis/p/api-to-create-workflows`,
`ghldesk.com/gohighlevel-api/`. Uma URL vista em busca
(`highlevel.stoplight.io/.../create-pipeline`, com exemplo de código de SDK
não-oficial) **não foi verificada** — o spec oficial lido direto não tem
esse endpoint, então trata-se como não confirmado até alguém abrir a página
manualmente.

## Conector `GHL CRM` — confirmado nesta rodada (18/09/2026)

As ferramentas `mcp__GHL-CRM__*` **estavam presentes** nesta sessão. Rodei
`locations_get-custom-fields`, `contacts_get-contacts` e
`opportunities_get-pipelines` na subconta `1D53YTI9C7oIMBavcQxV` para
reconferir o estado antes de mexer no roadmap: 0 campos personalizados, 0
contatos, 1 pipeline (`FUNIL DE VENDAS`, o que já existia, não o
`Pré-vendas` do projeto). Bate exatamente com `auditoria-resultado.md` —
nada mudou na subconta desde a auditoria. Reconfirmado de novo ao fechar o
R-07 (mesma rodada, mesmo resultado), outra vez ao fechar o R-08, outra vez
ao fechar o R-09 e outra vez ao fechar o R-10: estado inalterado nas cinco
checagens.

**Primeira mudança real na subconta, 18/09/2026:** executadas as 11 tags
aprovadas em `APROVADO.md` — contato `ZZ TESTE ESTRUTURA`
(`c5r3ZxiAd8T5adL1Bt6j`) criado com as 11 tags do projeto. A partir de
agora `contacts_get-contacts` retorna 1, não 0 — não é regressão, é a
primeira escrita de verdade que a rotina fez na subconta. Campos
personalizados e pipeline `Pré-vendas` seguem em zero (só saem manual).
Reconfirmado de novo ao fechar o R-11 (mesma rodada, mesma data): 0 campos,
1 contato (o de estrutura), só o `FUNIL DE VENDAS` — nenhuma escrita nova
neste item, ele não abre campo nem tag.

**Segunda rodada de escrita, mesma data, pedido explícito do dono ao vivo
em chat ("aplique todas os estudos... CRM fique mais completo possível"):**
1. As 3 tags que ainda esperavam aprovação (T-12 `atraso-1a-tentativa`,
   T-13 `reengajamento-ativo`, T-14 `pausado`) foram aprovadas na hora
   (registrado em `APROVADO.md`) e criadas via `contacts_add-tags` no mesmo
   contato de estrutura — a subconta tem as **14 tags do projeto**,
   nenhuma faltando.
2. Os 5 contatos fictícios do checklist (seção 10, `build-wesales.md`)
   foram criados: `Teste Atendeu`, `Teste Não Atende`, `Teste Retorno`,
   `Teste Número Errado`, `Teste Não Ligar` — sem telefone (falta o número
   real do dono, ver `APROVADO.md` seção Mensagens) e sem tag/oportunidade
   (pipeline `Pré-vendas` não existe ainda). Existem como registro,
   prontos para ganhar telefone e entrar no pipeline quando a montagem
   manual acontecer.
3. **Não criado:** nenhuma oportunidade (pipeline não existe — bloqueio de
   capacidade, não de aprovação) e nenhuma mensagem (falta o telefone real).

Estado da subconta após esta rodada: 0 campos personalizados, 6 contatos
(1 de estrutura + 5 fictícios), 14 tags aplicadas ao contato de estrutura,
só o pipeline `FUNIL DE VENDAS` pré-existente. Reconfirmado de novo ao
fechar o R-12 (rodada seguinte, mesma data): estado idêntico — nenhuma
escrita nova, porque este item só abriu um campo (`Nº de no-shows`, C-24) e
nenhuma tag. Reconfirmado outra vez ao fechar o R-13 (rodada seguinte,
mesma data): estado idêntico — este item não escreve no CRM (reaproveita a
tag `telefone-invalido` já existente e o campo nativo `Phone`, zero campo e
zero tag novos), então não havia nada para criar. Reconfirmado mais uma vez
ao fechar o R-15 (rodada seguinte, mesma data): estado idêntico — dashboard
e Custom Metrics não saem por API, e o item reaproveita C-09 a C-12 (R-01)
e `atraso-1a-tentativa` (T-12), zero campo e zero tag novos de novo.

## Pesquisa externa que valeu a pena guardar (R-13)

**Number Validation é um recurso nativo de conta do GHL**, não uma
integração de terceiro montada por fora: Configurações → Telefone expõe um
toggle (agência, depois subconta) que liga uma checagem de
operadora/formato/alcançabilidade por número, cobrada por checagem
(referências de mercado citam a Veriphone como provedor por trás e um
custo de ordem de US$0,005/validação — não confirmado na tela da WeSales, e
o plano/trial da subconta pode nem expor o recurso, mesma cautela já
registrada para o Custom Metrics do R-11). Uma vez ligado, existe um
gatilho de workflow próprio, **Number Validation**, que dispara com o
resultado da checagem (`Valid`/`Invalid`/`Landline` são os nomes vistos na
busca) — dá para reagir automaticamente sem precisar que o SDR discar
primeiro. **Nível de confiança médio:** só achado por busca
(`consultevo.com`, `growthable.io`, `gohighlevele.com`) — `help.gohighlevel.com`
segue bloqueado pelo proxy deste ambiente, mesma limitação já registrada
para R-09 a R-12 —, então os nomes exatos dos status e a disponibilidade
por plano **precisam ser confirmados na tela** antes de montar o workflow
da seção 2.16. Registrado como item opcional/dispensável no `build-wesales.md`
de propósito: a parte estrutural do R-13 (contato sem telefone nenhum)
resolve só com `If/Else` nativo sobre o campo `Phone`, sem depender deste
recurso pago nem da confirmação acima.

**Achado que gerou a mudança de desenho mais importante deste item:** o
portão por tentativa (nó 3, seção 2.4) já bloqueava telefone quando
`telefone-invalido` está presente, mas nunca bloqueou WhatsApp por essa
tag — porque o desenho original assumia que a tag só nascia depois de o
SDR confirmar "número errado" numa ligação de verdade (ramo da seção 4),
quando o lead já estava saindo de cadência de qualquer jeito. Ao desenhar
uma verificação **proativa** (antes de qualquer tentativa), reaproveitar
só o portão do nó 3 teria deixado a T1 inteira (mensagem + telefone +
WhatsApp) disparar para um contato sem telefone nenhum, porque WhatsApp
neste projeto também depende do número de telefone do contato
(`briefing-sdr.md`, "A máquina") — não é um canal independente. Regra
prática, generalizável para qualquer verificação futura que precise
travar **antes** da primeira ação de um workflow: um portão dentro do
bloco padrão de tentativa (nó 3) é tarde demais para isso — a verificação
proativa precisa ser um nó novo na inicialização (nó 0), não uma condição
a mais dentro de um portão que já existe para outro propósito (bloquear
canal por canal, tentativa por tentativa).

## `contacts_get-contacts` (lista) atrasa em relação à escrita — não confie nele logo após criar em lote

Descoberto ao criar os 5 contatos fictícios em sequência, 18/09/2026: cada
`contacts_create-contact` respondeu 201 com o contato completo, e
`contacts_get-contact` por ID confirmou cada um individualmente logo em
seguida — mas `contacts_get-contacts` (a lista, que a própria descrição da
ferramenta já marca como **deprecated** em favor de "search contacts")
continuou devolvendo só 1 contato (o mais antigo) por um tempo depois das 5
criações nas duas chamadas seguintes. Não é perda de dado: é o índice de
busca por trás da listagem ficando para trás da escrita (latência de
indexação), não o registro em si. Regra prática, generalizável: depois de
criar ou marcar vários contatos na mesma rodada, **verifique cada um pelo
ID retornado na criação** (`contacts_get-contact`), não pela contagem da
lista — a lista pode subcontar por um tempo mesmo com a escrita já
confirmada.

## `contacts_create-contact` exige nome ou identificador — `name` sozinho não basta

Descoberto ao criar o contato de estrutura das 11 tags, 18/09/2026: chamar
`contacts_create-contact` só com `body_name` (sem `firstName`/`lastName`
nem `email`/`phone`) devolve erro 422 — "Contacts without email, phone,
firstName and lastName are not allowed". `body_name` sozinho não conta como
identificador para essa regra, mesmo aparecendo depois no contato criado.
Passar `body_firstName`/`body_lastName` (pode ser texto livre, não precisa
ser um nome "de verdade" — usei `"ZZ TESTE"` e `"ESTRUTURA"`) resolve sem
precisar de e-mail nem telefone fake. Regra prática, generalizável: todo
contato de estrutura ou fictício criado por API neste projeto (a ordem
sugerida das 5 fictícias da seção 10, qualquer outro que surgir) precisa de
`firstName`+`lastName` (ou e-mail/telefone) no corpo da chamada — `name`
como único campo de identificação falha sempre. `contacts_create-contact`
aceita `tags` direto no corpo da criação — não precisa de uma segunda
chamada a `contacts_add-tags` quando o contato já nasce com as tags certas.

## `Allow Re-entry` bloqueia por workflow, não por evento — mesmo via `Add to Workflow`

Pesquisado ao fechar o R-08 (reengajamento dos 90 dias), 18/09/2026, porque
o primeiro desenho cogitado (devolver o lead reativado direto para a
Cadência 12x30) esbarrava nisso sem eu ter percebido de início. `Allow
Re-entry` desligado bloqueia um contato que **já passou por aquele
workflow específico** de entrar de novo nele — para sempre, não só "no
mesmo dia" ou "na mesma sessão do gatilho". A entrada `Add to Workflow`
não reavalia o filtro do gatilho de destino (já registrado acima, no
fechamento do R-07), **mas continua respeitando `Allow Re-entry`** — as
duas coisas são independentes, e é fácil ler a primeira e assumir que ela
cobre a segunda. Na prática: se um workflow tem `Allow Re-entry` desligado
por um motivo legítimo (aqui, D-06 em `briefing-sdr.md` — evitar tentativa
duplicada), **nenhum caminho nativo** (gatilho de novo, `Add to Workflow`,
reentrada manual) devolve um contato que já passou por ele uma vez. Regra
prática para qualquer item futuro que precise reciclar um lead por um
workflow que ele já visitou: não tente reaproveitar aquele workflow — crie
um novo, mesmo que pequeno, com sua própria configuração de reentrada.
Foi a saída usada no R-08 (workflow `Reengajamento 90 dias`, isolado da
Cadência 12x30).

## `Add to Workflow` não reavalia o filtro do gatilho de destino

Pesquisado ao fechar o R-07 (cadência inbound), 18/09/2026, porque o desenho
inteiro do handoff (seção 2.10 do `build-wesales.md`) depende disso. A
documentação oficial da HighLevel confirma: a ação **Add to Workflow**
insere o contato direto na sequência de ações do workflow de destino, **sem
reavaliar o filtro do gatilho** daquele workflow — o filtro só vale para a
entrada automática pelo próprio gatilho. Isso é o que permite um workflow
com filtro de tag "X ausente" (a Cadência 12x30, filtrando `cad-inbound`
ausente) receber de volta, por `Add to Workflow`, um contato que **tem** a
tag X — sem precisar remover a tag antes. É o mesmo mecanismo, sem essa
observação registrada antes, que a Qualificação por IA (seção 2.7) já usava
silenciosamente desde a primeira rodada.

**Cuidado que a mesma busca trouxe e que não se aplica aqui, mas vale**
**registrar para não confundir depois:** "Allow Re-entry" do workflow de
destino segue valendo — `Add to Workflow` não ignora essa configuração, só
o filtro do gatilho. Se o contato já tivesse passado por aquele workflow
antes (não é o caso do handoff do R-07: é a primeira entrada dele na
Cadência 12x30), `Allow Re-entry` desligado bloquearia a nova entrada.

## Pesquisa de mercado que valeu a pena guardar (R-07)

Meetime documenta que a taxa de ligação conectada bate 64% (o teto da
métrica) quando o retorno ao lead inbound sai em até 10 minutos, e
recomenda SLA de até 5 minutos para lead inbound direto — meta que a
literatura de speed-to-lead (benchmarks citando Velocify/InsideSales) reforça
com "conversão até 21x maior respondendo nos primeiros 5 minutos" contra
responder depois de 30. Confirmado também: Outreach e Salesloft são
desenhados para cadência **outbound** — nenhum dos dois tem, nativamente,
uma régua em minutos para lead entrante. Isso valida os degraus do roadmap
(5 min a 3 dias) como alinhados ao que a categoria trata como piso de
excelência, não como número arbitrário — e mostra que fechar isso com
workflow nativo do GHL, sem software de terceiro, é genuinamente competir na
faixa que as duas plataformas de prateleira do enunciado deixam de fora.

Se numa execução futura o conector **não** estiver na sessão, o problema
provável é o mesmo já resolvido antes (ver `rotina-horaria.md`): a rotina
precisa nascer com `GHL-CRM` anexado. Não é falta de acesso à subconta — é
falta do conector na sessão. Registre e siga com o item de backlog que não
depende do CRM, como a instrução manda.

- **Pesquisado ao fechar o R-15 (dashboard do gestor), 18/09/2026:** dois
  achados que mudam o alcance de qualquer item futuro que precise de tela
  agregada. **Custom Metrics aceita `Sum`/`Min`/`Max`/`Average` sobre campo
  `NUMERICAL`/`MONETARY`**, não só "contagem de contatos com tag" (o único
  uso que o R-11 tinha mapeado) — o Formula Editor mostra a agregação como
  opção assim que o campo existe, sem configuração extra. Isso é o que
  deixou os contadores do R-01 (`Tentativas telefone`, `Conexões telefone`
  etc., C-09 a C-12) virarem métrica de dashboard sem campo novo — regra
  prática, generalizável: qualquer contador numérico já existente no
  projeto pode virar Custom Metric por soma, sem precisar duplicar o dado
  em outro lugar. **Confirmado por ausência, não testado na tela:** Smart
  List **não** pode ser adicionada como widget de Dashboard — é pedido em
  aberto na base de ideias pública da HighLevel ("Add option to put smart
  lists on dashboards", sem previsão). Regra prática, generalizável para
  qualquer item futuro que precise "mostrar uma lista filtrada numa tela
  de gestor": o dashboard nunca substitui a lista, só aponta para ela (link
  ou nota, como o Monitor de Capacidade do R-11 já fazia) — não vale tempo
  tentando encontrar o widget certo para embutir uma Smart List, porque
  ele não existe. **Nível de confiança médio nos dois:** vieram de busca
  (`ghlexperts.com`, `consultevo.com`, changelog e base de ideias da
  HighLevel), não de teste na tela — `help.gohighlevel.com` segue
  bloqueado pelo proxy deste ambiente para leitura direta, mesma limitação
  registrada desde o R-09; confirme os nomes exatos dos widgets
  ("Appointment Report", "Opportunities", "Tasks") antes de montar a seção
  2.17 do `build-wesales.md`.

## O que o conector cria e o que não cria (reconfirmado)

Sem mudança desde `auditoria-resultado.md`: 36 ferramentas, cria tag (via
`contacts_add-tags`), contato, atualiza oportunidade, lê tarefas, manda
mensagem. **Não cria** campo personalizado, pipeline, workflow, calendário,
formulário, trigger link. Etapas 2/3 (parte de campo) e a montagem de
`build-wesales.md` inteira continuam manuais por natureza da API, não por
limitação do conector.

## Pesquisa externa que valeu a pena guardar

- **`Trigger Link Clicked`** é gatilho nativo de workflow no GHL (Marketing →
  Trigger Links → criar link → usar como gatilho ou inserir via `{}` →
  Custom Values → Trigger Links dentro de uma mensagem). Não precisa de
  landing page nova: qualquer URL, incluindo a de um calendário já existente,
  vira um link rastreável.
- **`Customer Replied`** é gatilho nativo de workflow (não só um tipo de nó
  `Wait`), com filtro por canal (SMS, WhatsApp, e-mail) e por frase. Serve
  para reagir a uma resposta **sem** depender do fluxo em que ela chegou —
  é o que fecha a lacuna F-01 do roadmap sem inventar nada fora do GHL.
- **RESPONDIDO em 18/09/2026:** campo `DATE` do GHL guarda **só a data**. A
  hora é descartada mesmo quando se envia um ISO completo pela API, e não
  existe tipo DateTime para campo de contato — é pedido aberto na base de
  ideias da HighLevel há tempo. Não adianta tentar por outro caminho de
  escrita: o corte é no tipo do campo.

  **Consequência, e ela é grande:** três itens dependiam disso sem saber.
  `Data do sinal` (C-14) perde a hora do clique; `Data do retorno` (S-01)
  perde a hora do retorno combinado; e o **R-02 (speed-to-lead) não fecha**
  com dois campos `DATE`, porque a métrica é em minutos e a diferença entre
  duas datas sem hora é zero no mesmo dia.

  **Saída:** guardar carimbo de tempo em campo `TEXT`, no formato
  `AAAA-MM-DD HH:MM`, e manter o `DATE` só quando a granularidade de dia
  bastar (filtro de lista, vencimento de tarefa). Onde a hora importa, TEXT.
  A ação premium `Date/Time Formatter` do workflow monta a string.

  **Consequência de segunda ordem, descoberta ao fechar o R-02:** um campo
  `TEXT` guardando carimbo de tempo resolve a escrita, mas quebra a leitura —
  lista inteligente não faz aritmética de data sobre campo `TEXT` ("mais de
  1h atrás" não é filtro disponível). Filtro relativo de data só existe para
  campo `DATE`, que é exatamente o tipo que a gente evitou por perder a hora.
  Não tem os dois ao mesmo tempo: hora certa e filtro relativo nativo.

  **Saída, generalizável para qualquer SLA em minutos/horas daqui pra
  frente:** não filtrar — **marcar**. Um workflow curto (`Wait → Time Delay`
  do tamanho do SLA, depois `If/Else` checando se o carimbo ainda está vazio)
  aplica uma tag quando o prazo estoura. A lista inteligente filtra a tag, não
  a data — zero aritmética, funciona com campo `TEXT`. É o desenho do
  `Alerta de Speed-to-lead` (`build-wesales.md`, seção 2.11): o relógio mora
  no workflow, a lista só lê a marca.

- **Pesquisado ao fechar o R-03 (funil por período), 18/09/2026:** o GHL tem
  filtro nativo `Last Stage Change Date` em oportunidades, com opção relativa
  "This Month" — parece resolver "quantos conectaram este mês" sem campo
  novo. **Não usar para funil histórico:** ele só reflete a **etapa atual**.
  Assim que a oportunidade avança (ex.: de `Conectado` para `Reunião
  agendada`), o dado de quando ela passou pela etapa anterior desaparece do
  filtro — o funil do mês subcontaria todo mundo que já avançou. Carimbo
  próprio por marco (campo `DATE`, um por evento) não tem esse defeito: grava
  uma vez e não muda com o avanço de etapa. Confirmado também: filtro
  relativo "neste mês"/"in month" já existe nativamente para campo `DATE`
  (não só para os campos padrão de data), então C-20/C-21/C-22 (`Data
  conectado`/`Data agendado`/`Data compareceu`) não precisam do truque de
  tag-alarme do R-02 — `DATE` filtra por mês direto, o truque de tag só era
  necessário porque C-14/C-18/C-19 são `TEXT` (por precisarem da hora, que
  `DATE` descarta). Regra prática: granularidade de **dia** e filtro
  relativo → `DATE` direto; granularidade de **minuto** → `TEXT` + tag.
  Para "quantos entraram este mês", nem carimbo novo: `Data de criação` da
  oportunidade já é nativa e imutável (não muda com o avanço de etapa, pelo
  mesmo motivo que `Last Stage Change Date` muda).

- **Pesquisado ao fechar o R-09 (regras de pausa), 18/09/2026:** a janela de
  envio (Send Window) de um workflow do GHL **não** tem exceção de data —
  é só dia-da-semana + horário, sem calendário de feriado embutido (é pedido
  em aberto na base de ideias pública da HighLevel, "Automation - Time
  Window - turn off messaging during holidays", sem previsão). Regra
  prática: não tente simular feriado dentro da janela de envio de um nó de
  espera.

  **O que resolve isso de verdade:** um recurso de **conta**, separado de
  qualquer workflow — Automação → Configurações → Global Workflow Settings
  → **Pause Workflow** ("Pausar Workflows em Datas Específicas"). Você
  escolhe um intervalo de datas e marca quais workflows **publicados**
  pausam nele (só lista publicados — monte isso por último, depois de
  publicar o que vai pausar). Confirmado: até 15 intervalos cadastrados,
  cada um com no máximo 15 dias entre início e fim, e uma opção `Annually`
  que repete o mesmo intervalo todo ano sem precisar recadastrar — perfeita
  para feriado de data fixa (Natal, Tiradentes etc.), não serve para feriado
  móvel (Carnaval, Páscoa), que precisa de recadastro manual anual.

  **O detalhe que decide se isso presta para "não gerar tarefa no feriado":**
  a documentação da HighLevel (achada via busca, não lida direto — ver nota
  de acesso abaixo) descreve que a pausa não segura só quem entra pelo
  gatilho durante o intervalo: um contato que já estava dentro do workflow,
  parado num nó de espera, **segue esperando normalmente**, mas a próxima
  ação de verdade (enviar e-mail é o exemplo citado; a mesma lógica deve
  valer para criar tarefa e mandar WhatsApp, que são o mesmo tipo de "ação"
  no motor de workflow) que ele encontrar enquanto a pausa está ativa fica
  represada até o intervalo acabar — Wait e If/Else não seguram, só a ação
  seguinte a eles. Isso é o que faria o recurso cobrir quem já está no meio
  de uma cadência de 30 dias, não só quem entra novo; sem isso, pausar só a
  entrada deixaria passar a maioria das ~120 tarefas/dia (a maior parte da
  fila em regime está em tentativa 3+, não na T1). **Nível de confiança:**
  alto, mas não é leitura direta do texto oficial — `help.gohighlevel.com`
  e os demais domínios de suporte da HighLevel estão bloqueados pelo proxy
  de rede deste ambiente (`WebFetch` retorna `EGRESS_BLOCKED` em todos os
  espelhos testados: `help.gohighlevel.com`, `help.leadconnectorhq.com`,
  `ideas.gohighlevel.com`, `actionera.freshdesk.com`, `consultevo.com`); só
  `WebSearch` (que roda em infraestrutura própria, fora deste proxy) trouxe
  o conteúdo, em resumo. Antes de confiar 100% nisso para uma operação de
  volume real, vale testar na prática com um contato de teste parado numa
  tentativa e uma pausa de calendário curta. Generalizável: para qualquer
  necessidade futura de "não toque em ninguém por um período"
  (calendário-wide), este recurso de conta é o caminho certo a pesquisar
  primeiro — reserve tag customizada só para pausa **individual** (um lead
  específico), que é o que o recurso de conta não cobre.

- **Pesquisado ao fechar o R-05 (teste A/B da abertura), 18/09/2026:** o GHL
  tem ação nativa de workflow **Split**, que sorteia contatos entre até 5
  caminhos por percentual configurável e **mantém o contato no mesmo
  caminho** se ele passar pela mesma ação de novo (não sorteia de novo a
  cada reentrada). É melhor que um If/Else alternando por paridade de
  campo/ID para qualquer teste A/B futuro no projeto: alternância por ordem
  correlaciona a variante com o horário/dia de entrada do lead (viés), e
  sorteio aleatório não. **Detalhe que custa caro se ignorado:** o Split não
  rejunta os caminhos sozinho — cada caminho precisa ser conectado
  manualmente ao mesmo próximo nó se a intenção é convergir de volta ao
  fluxo principal (como em `build-wesales.md`, seção 2.6.1, onde os dois
  caminhos de M1 precisam apontar para o mesmo Wait → Contact Replied).
  Regra prática, generalizável: qualquer item futuro do roadmap que precise
  dividir tráfego por percentual (não por condição) usa Split, não If/Else.

- **Pesquisado ao fechar o R-10 (distribuição de leads), 18/09/2026:** o GHL
  tem ação nativa de workflow **Assign to User** com quatro modos —
  `Contact Owner` (mantém quem já é dono), `Selected User` (fixo),
  `Any User` (qualquer usuário elegível) e `Round Robin` (roda entre os
  escolhidos). Resolve "round robin de lead" sem workflow customizado.
  **Nível de confiança: médio-alto** — veio só de busca, os domínios de
  suporte da HighLevel continuam bloqueados neste ambiente (mesma limitação
  já registrada para o R-09); não testado numa subconta com 2+ usuários
  porque esta só tem o dono. Verificar de verdade é o item 28 do checklist
  da seção 10 de `build-wesales.md`, na primeira vez que houver um segundo
  usuário na subconta.

  **Achado que muda o desenho de qualquer lista "por usuário logado"
  daqui pra frente:** Smart Lists de contato no GHL **não** têm filtro
  dinâmico "Atribuído a = usuário atual" — é pedido em aberto no fórum de
  ideias da própria HighLevel (`ideas.gohighlevel.com`, mais de uma thread
  pedindo isso), sem previsão. O filtro "Atribuído a" só aceita um usuário
  fixo escolhido na hora de montar a lista. Regra prática, generalizável:
  qualquer lista futura que precise "mostrar só o que é meu" para cada
  membro do time precisa de **uma cópia da lista por pessoa**, com o nome
  dela fixado no filtro — não existe lista única que se adapte sozinha a
  quem está logado. É trabalho manual que se repete a cada contratação, não
  uma vez só; documentado como procedimento em `build-wesales.md`, seção
  2.14, em vez de lista já criada, porque com 1 usuário não há o que
  filtrar ainda.

  **Não confirmado, registrar quando testar:** se a ação `Add Task` aceita
  `Contact Owner` como destino dinâmico do campo "Atribuir a" (o desenho do
  R-10 depende disso para que toda tarefa de uma cadência de 30 dias siga
  o mesmo dono sem precisar sortear de novo a cada tentativa). Se a tela
  não oferecer essa opção, o caminho alternativo mais provável é o botão de
  valor personalizado (`{}`) ao lado do campo, inserindo o merge field do
  usuário atribuído do contato — não confirmado por falta de subconta com
  2+ usuários para testar. Não criar um segundo mecanismo de round robin
  dentro do `Add Task` como alternativa: isso sorteia por tarefa em vez de
  por lead, o oposto do que o R-10 decidiu de propósito (ver "A decisão que
  separa isto de uma cópia de tela", seção 2.14).

- **Pesquisado ao fechar o R-12 (handoff e no-show), 18/09/2026:** o GHL tem
  gatilho nativo `Appointment Status` com status `No Show`, mesma família do
  `Showed` já usado no R-03 — confirmado por busca (`consultevo.com`,
  `help.gohighlevel.com` segue bloqueado pelo proxy deste ambiente, mesma
  limitação já registrada para R-09/R-10/R-11) e coerente com a estrutura do
  calendário `Reunião com closer` já montada. Outreach e Salesloft resolvem
  recuperação de no-show via integração com ferramenta de agendamento de
  terceiro (Chili Piper é o exemplo mais citado) — nenhum dos dois tem
  automação nativa de no-show sozinho, o mesmo padrão de "precisa de
  parceiro externo" já visto no R-07 para inbound em minutos. A literatura
  de operação de vendas (Zapier, AskElephant, blogs de RevOps) converge em
  dois pontos: mensagem automática de "sentimos sua falta" imediata, e
  escalar para contato pessoal de um closer/AE em até 1 hora útil quando o
  lead vale a pena — nenhuma fonte encontrada trata **no-show repetido**
  como gatilho de decisão automática (descarte), só como métrica de
  relatório. É a lacuna que a regra "2º no-show seguido descarta sozinho"
  do R-12 fecha, e é o tipo de coisa que só aparece lendo o workflow, não
  olhando a tela.

  **Reaproveitando a lição do R-08 sem repetir o preço dela:** o R-08
  (reengajamento) só descobriu o problema do `Allow Re-entry` desligado da
  Cadência 12x30 (D-06) depois de cogitar reentrar por ela — teve que
  resolver com tag de blindagem e troca de origem. O R-12 aplicou a lição
  **antes** de desenhar: em vez de devolver o lead no-show para `Em
  cadência`, a régua de recuperação roda com a oportunidade parada em
  `Reunião agendada` o tempo todo. Resultado: zero tag nova precisou nascer
  para este item (usa só um campo `NUMERICAL` novo, `Nº de no-shows`) e zero
  risco de bater no mesmo `Allow Re-entry`. Regra prática, generalizável:
  antes de desenhar qualquer recuperação futura que aconteça **dentro** de
  uma etapa que já tem um workflow com `Allow Re-entry` desligado, pergunte
  primeiro se dá para resolver **sem sair daquela etapa** — nem toda
  recuperação precisa voltar o lead para o começo do funil.

  **Sobre rodar dois relógios ao mesmo tempo no mesmo gatilho:** o motor de
  workflow do GHL não bifurca um nó em dois caminhos que continuam em
  paralelo — `If/Else` e `Split` escolhem sempre **um só** caminho por
  contato. Para o R-12 precisar de duas coisas simultâneas e independentes
  (a régua de recuperação do SDR e o relógio de SLA do closer, cada uma com
  seu próprio tempo de espera), a saída nativa é a mesma já usada pela
  seção 5/5.1/5.2 deste projeto: dois workflows curtos escutando o mesmo
  evento, não um workflow tentando fazer as duas coisas. Regra prática,
  generalizável: **"preciso de dois relógios correndo ao mesmo tempo para o
  mesmo contato" é sinal de dois workflows, nunca de um workflow com dois
  ramos** — ramos de `If/Else` são exclusivos, não paralelos.

- **Pesquisado ao fechar o R-11 (alerta de capacidade), 18/09/2026 — o achado
  mais importante para qualquer alerta de agregado futuro:** o motor de
  workflow do GHL **não tem** nenhuma ação nem condição que leia "quantos
  contatos passam por este filtro/lista agora" — todo nó de workflow executa
  no escopo de **um** contato, o mesmo em contexto desde o gatilho. Confirmado
  por ausência, não por documentação direta (os domínios de suporte da
  HighLevel continuam bloqueados neste ambiente, mesma limitação já registrada
  para R-09/R-10): a própria base de ideias pública da HighLevel tem o pedido
  "trazer métricas do dashboard como custom value" em aberto, sem previsão —
  se essa ponte não existe, também não existe um "If/Else" nativo comparando
  a contagem de uma Smart List contra um número. **Regra prática,
  generalizável para F-04 (teto de toques por semana) e F-05 (monitor de
  saúde), que vão bater na mesma parede:** nenhum dos dois consegue nascer
  como "workflow que conta e decide" — F-04 se resolve por contador por
  **contato** (campo `Toques na semana`, incrementado e checado no escopo de
  cada lead, sem agregado — esse sim é nativo e comum no projeto, ex.: `WA
  não atendidas seguidas`); F-05 (que por definição precisa comparar
  contagens entre contatos, ex. "quantos estão há mais de 24h em `fila-tel`")
  não tem solução dentro de um único workflow — a saída é o mesmo padrão do
  R-11: uma Smart List que já faz o filtro certo (o cálculo mora no filtro,
  não num contador) mais um **Custom Metric** e/ou um aviso agendado, nunca
  um workflow tentando comparar quantidades.

  **Duas peças novas descobertas nesta busca, primeira vez que aparecem no
  projeto:**
  - **Gatilho de workflow `Scheduler`** — contactless (roda sem contato em
    contexto, ao contrário de todo outro gatilho já usado no projeto),
    dispara por relógio (diário/semanal/mensal/intervalo), respeita fuso e
    pode pular fim de semana. **Não pode dividir o workflow com outro tipo de
    gatilho** — é o único caso do projeto até agora em que uma nova
    automação precisa nascer como workflow próprio por essa razão, e não por
    `Allow Re-entry` (a razão que já apareceu no R-08). Ações compatíveis
    citadas na documentação: webhook, integrações (Slack, Asana, Airtable,
    Google Sheets), e-mail/SMS interno para a equipe, atualização de custom
    value, criação de tarefa — nenhuma delas lê contagem de contato. Serve
    para qualquer aviso ou rotina que precise rodar "todo dia às X", sem
    depender de um contato específico entrar em algum lugar.
  - **Custom Metrics (Reporting → Custom Metrics)** — fórmula combinando até
    4 métricas com operadores matemáticos e constantes; uma das métricas
    disponíveis é "Contagem de contatos com Tag" (aceita OR/AND entre tags,
    igual ao filtro de Smart List). É o único lugar nativo onde dá para
    transformar uma contagem em "contagem menos a meta", plantando o alarme
    dentro do número em vez de deixar o gestor comparar contra a meta de
    cabeça. **Atenção:** encontrado como disponível "a partir de planos
    $497+" — não confirmado se a subconta/plano da WeSales inclui; qualquer
    item que dependa disso precisa checar isso na tela antes de montar, e
    tem que sobreviver sem o recurso se ele não existir (a Smart List sozinha
    sempre existe, independente de plano).
