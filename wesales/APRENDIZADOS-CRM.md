# O que as execuções da rotina horária já descobriram

Memória entre rodadas. Antes de investigar de novo, procure aqui.

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
nenhuma tag.

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
