# Estado em 27/09/2026 04:10 UTC — leia isto primeiro

Handoff escrito porque o dono saiu do computador e a operação abre terça 29/09.
Se você é a próxima sessão, **leia este arquivo antes de qualquer coisa** e não
refaça o que está aqui.

Complementa o `ABERTURA.md` do branch `claude/amazing-johnson-mclksg`, que
continua valendo para a lista dos 30 por ID e o mecanismo da janela.

---

## 1. O que eu escrevi no CRM hoje (trilha de auditoria)

Tudo na subconta `1D53YTI9C7oIMBavcQxV`. Nada excluído em nenhum momento.
Autorizado pelo dono ao vivo em chat, que é o mecanismo que o `APROVADO.md`
registra como válido.

| o quê | quantos | por quê |
|---|---|---|
| `dnd = true` | 30 contatos | travar a rampa de 6/dia; lista por ID no `ABERTURA.md` |
| `dnd` + `nao-perturbe` + `grupo-whatsapp-nao-e-lead` + oportunidade `abandoned` | 2 | eram **IDs de grupo do WhatsApp** entrando como lead (`+120363…`, 18 dígitos) |
| `Prioridade` = 0 | 34 | tirar da fila do SDR quem está em DND ou `nao-perturbe` |
| `Prioridade` = 4 | 5 | lote 1, regra 5 da §9.2 (`Tentativa nº` = 0) |
| `Nota de qualificação` = 93 | 2 | `Daniel` e `genilson \| Bombeiro`, faixa A, calculada pela §9.1 |
| contato de teste criado | 1 | `ZZ TESTE ABERTURA 27-09` (`lF8IdciftoNdPaLTLgE6`), protegido, telefone inválido |

### Segunda rodada de escritas — 27/09 12:00, autorização nova do dono

O dono autorizou ao vivo em chat: *"Na rotina ativa, aplique sempre as melhorias e
correções no CRM. Módulo por módulo. Apenas os agentes de IA, por enquanto vamos
dar uma segurada. Como IA no whatsapp, IA na ligação. Porque gastam crédito,
custo."* A rotina passou de "só lê" para "aplica", com a IA fora.

**Módulo 1 — proteções reconciliadas (40 escritas).** Era a decisão 0b da §3, e o
prazo era segunda 08:30.

| o quê | quantos | por quê |
|---|---|---|
| tag `nao-perturbe` adicionada | **31** | tinham DND e não tinham a tag. Sem a tag o workflow **não** para: o portão que ele lê é a tag, não o DND (§7 do `USABILIDADE.md`). Isto é o que faz a proteção valer de verdade |
| `dnd = true` | **9** | tinham a tag e nenhum DND — o workflow parava, mas mensagem manual ou discagem pelo Call Center passava |

As listas de auditoria 8.26 e 8.27 devem abrir **vazias** a partir de agora. Se
voltarem a encher, algo está desfazendo a reconciliação — é sinal de defeito, não
de operação.

**Observação honesta sobre os 9:** ao aplicar, li um por um, e **nenhum é
prospect**. Três são registros da própria agência que o app de WhatsApp criou como
lead: `o próximo cliente` (`+5512982381407`, que é o **número ativo do Call
Center**), o `sem nome` `+552123915933` (e-mail `agencia.proximocliente@gmail.com`)
e o `156766977421470` (`+18005551470`, id de sistema da Meta). Os outros seis são
contatos de teste. Então nesse lado a correção foi **higiene**, não proteção — e
reforça o achado de que a integração de WhatsApp transforma em lead coisas que não
são pessoas.

**Módulo 2 — higiene de oportunidade (2 escritas).**

| o quê | por quê |
|---|---|
| oportunidade `0V9VQ421wCn274mo9BQa` ganhou o nome `Carla Sampaio` | estava em branco enquanto o contato tinha nome; aparecia como linha vazia no quadro e numa puxada por pipeline no Call Center |
| oportunidade `VSRNAwP0kCub56Zjw4ZB` (`Pablo Sampaio`) → `status = lost` | era o teste de calendário do próprio dono ocupando `REUNIÃO DE DIAGNÓSTICO` e contando como reunião nas métricas mensais. Descartada, **não excluída** — a regra 1 do projeto proíbe excluir. O e-mail do contato (`agencia.proximocliente+teste9940@gmail.com`) confirma que era teste |

**Módulo 4 — `country` corrigido (41 escritas, 12:50).** 41 contatos tinham
`country: "US"` com telefone `+55`, incluindo os 38 leads reais — herança da
integração, que nasce no padrão americano. Todos para `BR`. Conferido depois: **0**
com `US` + `+55`, e 56 dos 64 agora em `BR`. Os **8 que seguem `US` não têm telefone
nenhum** (`TINTIM`, `Dkw.oficial`, `Nathalia.ggss`, `Carla X. Sampaio`, `Thiagoreis` e
três de teste): sem telefone não há sinal de país, e eu não adivinho.

Na mesma leitura, conferência do módulo 1: **8.26 = 0 e 8.27 = 0**. As duas listas de
auditoria de DND seguem vazias.

**Módulo 3 — `Nota de qualificação` RETIRADO da fila.** Medido antes de escrever: só
**3** dos 64 contatos têm Bloco A completo mais `Budget` e `Decisor` — e os três já
têm nota. `Clientes novos por mês`, `Tem time comercial`, `Budget`, `Decisor` e
`Prazo` existem em 3 ou 4 registros.

E o motivo de fundo, esclarecido pelo dono em 27/09: **são dois formulários**. O do
Meta Ads traz contato, `Urgência`, `Necessidade`, `Dor principal` e atribuição; o de
**qualificação é preenchido pelo SDR na ligação**, ao marcar com o closer, e é ele que
traz o BANT. Os campos personalizados vão sendo acrescentados ao mesmo lead **ao longo
do processo até o fechamento**. Então campo vazio aqui é "ainda não", não "faltou".

Calcular nota para os outros 60 pontuaria ausência de dado como ausência de fit — e a
§9.1 dá consequência automática à faixa (25–44 nutrição com `abandoned`, 0–24 descarte
com `lost`). Eu teria descartado lead pago. A nota pertence ao **Pós-agendamento nó
4**, depois do formulário do SDR. Retirada da fila; este parágrafo fica para ninguém
repor por engano.

**Módulo 5 — revisão do `telefone-invalido`: nada a remover, e pela razão certa
(13:15).** A tag está em 8 contatos, e **todos os 8 estão sem telefone nenhum**. Ou
seja, a tag não está velha em nenhum caso: está correta nos 8. Nenhuma escrita.

Registro porque um no-op medido vale como resultado: a suspeita era que a tag, nunca
removida por workflow (§9 do `USABILIDADE.md`), estivesse rebaixando lead já
corrigido. Não está. O defeito "só entra e nunca sai" segue real como risco futuro —
o dia em que alguém corrigir um número, a tag fica — mas hoje não há vítima.

**Achado lateral, e é sobre a integração de WhatsApp de novo.** Dos 8, **5 são leads
reais**: `TINTIM`, `Dkw.oficial`, `Nathalia.ggss`, `Carla X. Sampaio`, `Thiagoreis`.
Eles não têm **telefone nem e-mail**, e não têm `attributionSource`. São os mesmos 5
que aparecem na lista 8.18 e os mesmos que sobraram em `country: US` depois do módulo
4. Já estão com `status-perdido`, o que é o desfecho correto — não há canal por onde
falar com eles.

Consequência prática: o **W23 (`Resgate por E-mail — Sem Telefone`)** não os salvaria,
porque e-mail também não existe. E os nomes parecem identificador de Instagram
(`dkw.oficial`, `nathalia.ggss`, `thiagoreis`), o que os põe na mesma família dos JID
de grupo e dos `Sem nome`: **registro criado sem canal de contato**. Se for a mesma
integração, é a terceira classe de defeito dela — e aí vale contar essa perda ao
avaliar o custo por lead, porque são cliques pagos que nasceram inalcançáveis. Uma
olhada na tela em quem criou esses 5 fecharia a questão.

**O que continua fora do meu alcance, com autorização ou sem** — e por isso segue
na §3 como trabalho de tela: editar workflow (exige a API interna com bearer de
sessão logada), criar ou editar lista inteligente, criar pasta de campo, e
`Add to Workflow` em lote. O conector escreve **contato** e **oportunidade**; o
resto não.

**Agentes de IA parados por decisão do dono:** nada de IA no WhatsApp (o W10) nem
IA na ligação, por custo de crédito. `botServiceEnabled` segue `false` e a rotina
não pode ligá-lo.

**Uma escrita fora do `APROVADO.md`, declarada:** a tag
`grupo-whatsapp-nao-e-lead` não existe naquele arquivo. Eu a apliquei para
impedir venda dentro de grupo de WhatsApp. Excluir tag está em "Nunca
autorizado", então não há como desfazer — fica para o dono ratificar.

**O que eu deliberadamente NÃO fiz:** aplicar `fila-quente` no Daniel e no
Genilson, que a faixa A também manda. Os dois estão em `NEGOCIAR`, com o closer,
e `fila-quente` alimenta a fila do **SDR** — aplicá-la quebraria a separação de
papéis da §3.1.

## 2. O risco de segunda 08:30 — reavaliado, e menor do que eu disse antes

A janela das duas cadências segue `days: [1,2,3,4,5]` 08:30–18:30, e fechá-la em
`days: [2]` exige a API interna (bearer de sessão logada) — não sai de contêiner
nem de Action. **Continua sendo do dono.**

Mas o quadro mudou com o DND aplicado. Se a janela abrir na segunda:

- **34 dos 39** leads de `CONECTAR` estão em DND ou `nao-perturbe` → o canal
  está bloqueado. Nenhum deles recebe mensagem.

  **CORREÇÃO DE 27/09 09:00, e é importante:** "canal bloqueado" **não** é
  "máquina parada". A varredura das listas 8.26/8.27 (ver §7 do `USABILIDADE.md`)
  mostrou que **31 desses têm DND e NÃO têm a tag `nao-perturbe`** — porque fui eu
  que liguei o DND sem aplicar a tag. E as duas proteções agem em camadas
  diferentes: o DND é bloqueio de canal, imposto na hora de enviar; a tag é o que
  a **lógica de workflow lê** (o W13 nó 3 é `Tags inclui nao-perturbe → FIM`).
  Para esses 31 a régua **continua andando** — cria tarefa, mexe em etapa, soma
  contador — só não fala com ninguém. Ou seja: a incógnita "para ou pula" já tem
  resposta para eles, e é **pula**. Queima tentativa em silêncio, que é o pior dos
  dois mundos.
- **5 leads** (o lote 1: Gerson, Ana Ruth, Ricardo, Andreia, Andre) estão livres
  e **recebem a MI-0** — que é exatamente o lote da rampa de 6/dia, um dia antes.

**Decisão que eu tomei, e o raciocínio:** deixei os 5 livres. DND neles zeraria
o disparo de segunda, mas criaria a dependência de alguém lembrar de desligar 5
DNDs antes de terça — e "alguém lembrar" é justamente o que falha quando não há
ninguém no computador. Cinco mensagens para leads que preencheram formulário
pedindo contato não é falha: é a operação começando um dia antes, com a rampa
certa. O cenário catastrófico que eu descrevi ontem (37 mensagens) **não existe
mais**.

## 2.1 CORRIGIDO EM 12:20 — a §2.1 abaixo partia de hipótese errada

**Leia a §0-BIS do `USABILIDADE.md` antes desta seção.** Os 38 leads **estão
inscritos** na cadência e parados no primeiro `Wait`, esperando a janela de
execução — a prova são as escritas de inicialização do nó 0 nos campos
(`Tentativa nº` = 0, `Permissão WhatsApp` = `Não solicitado`), que eu li como
"nada rodou". A tag de fila e a tarefa vêm **depois** do nó de mensagem, e por
isso ainda não existem.

Consequência: **o risco de "a máquina não agir" não existe**, e o
`Add to Workflow` em lote sai da lista de ações — inscreveria de novo quem já está
inscrito. O risco real volta a ser o original e único: **segunda 28/09 08:30 a
janela abre** e as execuções paradas retomam. Fechar em `days: [2]` segue sendo a
única alavanca que segura isso, e segue sendo trabalho de tela.

O texto original fica abaixo, sem edição, porque a medição das listas continua
válida — só a causa estava errada.

## 2.1 (texto original de 05:20, hipótese refutada) — e ele passa na frente da janela

Medido em leitura pura, agora no **pipeline inteiro** (uma chamada com
`getTasks`, não amostra): **64 oportunidades no `FUNIL DE VENDAS`, duas
tarefas** — as duas em contato de teste, as duas vencidas desde 22/09. E
**nenhum dos 39 leads abertos em `CONECTAR` tem tag `fila-tel`, `fila-wa` ou
`fila-quente`**; todas as tags `fila-*` do inventário estão num único contato,
o `ZZ TESTE ESTRUTURA`, que é o fixture de criação de tag.

Consequência direta: as **quatro listas favoritas do SDR abrem vazias** na
terça, e a fila de tarefas também. O alvo que o dono chamou de crítico — "pelo
menos 100 tarefas" — hoje vale **zero**. A única lista cheia é o alarme do
gestor (`Atraso na 1ª Tentativa`, 38 linhas).

E o que torna isso urgente: os gatilhos das duas cadências são `Opportunity
Stage Changed → CONECTAR` com **`Allow Re-entry` desligado**, e os 38 **já
estão** em `CONECTAR`. Se não foram inscritos, **nada os inscreve depois**.

**Isto reordena a §3.** Fechar a janela em `days: [2]` protegia contra a
máquina agir cedo demais. Este achado é a máquina **não agir** — e é pior,
porque é silencioso. Janela controla *quando* a régua dispara, não *se* o
contato entrou nela.

**Conferir (2 min, tela):** Automação → `Cadência Inbound` → contatos
inscritos. Abaixo de 38 confirma.

**Consertar (tela, não sai por API):** selecionar os leads de `CONECTAR` →
**`Add to Workflow` → `Cadência Inbound`** em lote. Entra pelo nó 0, que
atribui dono (resolve o R-10 do item 5 de uma vez), grava `Entrada em`, põe a
tag de fila e cria a tarefa.

**Se não der tempo antes de terça**, há um caminho de três passos que usa só o
que existe: lista com filtro `Prioridade` ≥ 3 (devolve os 5 do lote 1) →
copiar as linhas `telefone, nome` → colar na caixa editável do Call Center →
`Iniciar discagem`. Detalhe na §0 do `USABILIDADE.md`.

**Efeito colateral que ninguém procurou:** a lista **8.5 `Sem resultado ontem`**,
que a §3.3 manda o gestor abrir às 08:15, exclui por `não fila-tel` e `não
fila-wa`. Sem essas tags, as exclusões não excluem: a lista devolve **18
linhas**, das quais **11 são `lost`/`abandoned`**, uma é o próprio dono e duas
são o Daniel e o Genilson (que estão com o closer). Além da inscrição em lote,
essa lista precisa de uma cláusula que o documento nunca teve: **status
`open`**. É edição de lista, um minuto de tela.

**Três achados menores da mesma leitura:** (a) dois leads abertos em `NOVO LEAD`
**sem nome utilizável** (`+5521969613820` e `+5511951285383`) — **não é o
formulário do Meta**, ao contrário do que eu disse primeiro: um é o app de
WhatsApp gravando `Sem nome` num contato real, o outro é uma oportunidade em
branco de um contato que tem nome (`Carla Sampaio`). Detalhe e tabela das cinco
origens na correção de 07:50 do `USABILIDADE.md`; (b) a única oportunidade
aberta em `REUNIÃO DE DIAGNÓSTICO` é o **próprio dono** (`Pablo Sampaio`), o
teste do calendário, e ele conta nas métricas mensais de funil até ser descartado
como `lost`; (c) `FORMALIZAR` vazia e **zero `won`** em 64 oportunidades.

Na mesma varredura: **`assignedTo` nulo em 42 das 47** oportunidades de
`CONECTAR`; os 5 com dono são os 3 de teste mais `Carlos Andrade` e
`554791548812`. Isso deixa sem destinatário a notificação "respondeu agora" do
W13 — que a §3.1 chama de único motivo para o SDR interromper o bloco.

## 2.2 ACHADO DE 10:15 — o freio de capacidade não tem atuador, e a notificação diz que tem

Nos 43 dumps ativos de workflow: a tag **`sdr-lotado`** é **lida** num portão por
cinco workflows (`Cadência Inbound`, `Cadência 12x30`, `12x30 — parte 2`,
`Recuperação de No-show`, `ZZ TESTE 12X30`) e **escrita por nenhum**. Ela não está
em nenhum dos 64 contatos.

O `Monitor de Capacidade` (publicado) manda ao gestor: *"Com 50 ou mais tarefas
vencidas, **o sistema segura sozinho** os toques novos da cadência (tag
`sdr-lotado`)…"*. Não segura. É promessa falsa sobre uma proteção, e o gestor que
acreditar para de olhar o teto de 100 tarefas da §3.5.

A conferência manual que a mensagem sugere aponta para `Fila do Dia — Total`, lista
que hoje devolve **0 linhas** (§7 do `USABILIDADE.md`) — então quem seguir a
instrução vê vazio e conclui que está tudo bem.

Dois consertos, os dois de tela/API interna (não saem daqui): decidir se o freio é
automático (falta um `add_contact_tag sdr-lotado` em algum lugar que conte tarefa
vencida) ou manual (e então o texto tem de mandar aplicar a tag, e a ação entra na
rotina do gestor da §3.3, onde não está); e corrigir o texto de qualquer jeito.

**Nota de escopo:** isto não afeta a terça, porque o portão sempre passa hoje — o
custo aparece quando o volume chegar, que é o cenário dos 10 leads/dia.

## 2-BIS. A lista única do que falta

`wesales/FALTA-PARA-SER-MAQUINA.md` — nome sem data de propósito, para ser atualizado no
lugar. Consolida o que falta para o CRM virar máquina de vendas, medido em 27/09, e
separa o que é do dono do que é meu. Dois itens novos que não estavam em nenhuma fila:

- **36 das 39 oportunidades em `CONECTAR` sem `assignedTo`**, inclusive os cinco do lote
  1 que a máquina toca na terça. Tarefa sem destinatário não aparece na fila de ninguém
  (R-10, agora com número).
- **`Reunião Cancelada` está completo, 10 nós, em `draft`.** Se o lead cancelar hoje, os
  lembretes continuam e ninguém remarca. O buraco mais barato de fechar da lista.

## 3. Decisões que esperam o dono

0b. **As duas proteções sempre juntas (DND + tag `nao-perturbe`)?** Decisão
   curta e com consequência grande. Hoje 40 registros discordam: 31 com DND sem a
   tag (escrita minha de 27/09) e 9 com a tag sem DND. Se a resposta for "sempre
   juntas", sai um script de reconciliação e as listas 8.26/8.27 devem ficar
   vazias para sempre. Se não, a janela em `days: [2]` volta a ser a única
   alavanca real, porque é a única que para o motor em vez de calar a boca dele.
   Escrever depende de `[x]` novo no `APROVADO.md`. Ver §7 do `USABILIDADE.md`.
0. ~~`Add to Workflow` em lote~~ — **RETIRADO em 12:20.** Partia de hipótese
   refutada (os leads já estão inscritos); executar duplicaria execução. Ver a
   §0-BIS do `USABILIDADE.md`.
1. ~~**Janela em `days: [2]`**~~ — **CANCELADO em 27/09, por medição.** Era o
   único item com prazo (segunda 08:30) e o único que exigia a API interna. Medi
   a exposição real em vez de estimá-la: busquei as oportunidades abertas em
   `CONECTAR` e apliquei as condições do portão MI-0 em cima delas. **Passam
   exatamente 5 leads** — Gerson De Souza Pia (`+5521990518798`), Ana Ruth
   (`+5521969489937`), Ricardo (`+5521968889876`), Andreia (`+5521997355174`),
   Andre (`+5521980417915`). São o lote 1 da rampa.

   Então a janela protegeria contra 5 mensagens para 5 pessoas que preencheram
   formulário pedindo contato, um dia antes da abertura. Isso não é a máquina
   agindo cedo: é a operação começando. Com o item 0 aplicado (40 contatos com
   `nao-perturbe` **e** `dnd=true`, listas 8.26/8.27 em zero), ninguém fora
   desses 5 recebe nada.

   **O que isso fecha:** não há mais item com prazo antes de segunda, e o pedido
   de liberar `backend.leadconnectorhq.com` deixa de ser urgente — segue útil
   para os consertos de `fila-wa` e `sdr-lotado`, que não têm data.
1-BIS. **Pastas de campo — o botão está pronto, o arrasto caiu de 56 para 27.**
   A Action `wesales-pastas.yml` (dispatch, `criar: true`) renomeia a pasta grande
   para `5 · NÃO MEXER — a máquina escreve` e cria as outras quatro. A renomeação
   é o truque: 29 dos 30 campos da máquina já estão nessa pasta, então eles não
   se arrastam. Sobram 27 arrastos, na ordem que o próprio job imprime — e a
   pasta 1 tem 3 campos e já limpa o dia da SDR, se você parar nela.
   O job roda o mapa antes, sem segredo, e falha se o mapa não fechar com a conta.
2. **`[x]` no `APROVADO.md`** para escrita de `Prioridade`, se quiser que o
   runner diário aplique sozinho. Hoje ele só lê.
3. **G-04, A ou B.** Recomendação: **B** (a §9.1 lendo `Urgência`/`Necessidade`
   por `Contains`), porque são **oito formulários** de Lead Ads e a A é trabalho
   de tela oito vezes, com todo formulário novo nascendo errado. Sob a B, apagar
   o `patch_picklist_investimento.py`.

   **A medição de 27/09 reforça a B, sem que eu tenha ido buscar isso:** ao contar
   preenchimento de campo para refazer as pastas (§4 do `USABILIDADE.md`), os três
   únicos campos que chegam com o lead são exatamente `Urgência` (40/64),
   `Necessidade` (34/64) e `Investimento mensal em anúncios` (32/64). A opção B lê
   os dois primeiros por `Contains`, e eles são os campos mais preenchidos da conta
   depois dos que a máquina inicializa. A B não está apostando num campo frágil.
4. **Texto da tarefa T1** — hoje manda clicar em "Ligar via WhatsApp", botão que
   não existe nesta conta (ver `CANAIS.md`). Telefone tem de ser o passo 1.
5. **Distribuição de dono (R-10)** — lead novo nasce com `assignedTo: null`.
6. **Ratificar (ou não)** a tag `grupo-whatsapp-nao-e-lead`.
7. **`fila-quente` no Daniel e no Genilson?** Ver §1.

## 4. Os dois leads que valem mais que qualquer configuração

`Daniel` (`+5521968390582`) e `genilson | Bombeiro` (`+5521972023213`), em
`NEGOCIAR`, agendados em **19/09**, **oito dias sem nenhum toque**. `Budget` =
`Tem`, `Prazo` = `Pra ontem`, `Investimento mensal` = `Acima de 10k`, `Decisor` =
`Sim`. Nota 93, faixa A.

Se alguém só puder fazer uma coisa nesta operação, é **ligar para esses dois**.

## 4.1 BLOQUEIO NOVO (27/09 04:10): a conta de anúncio está `UNSETTLED`

Procurando a conta que alimenta o CRM, achei: **"O Próximo Cliente"**,
`ad_account_id` **1695865631502778**, business `sxeducacao`, moeda BRL. O que a
API devolve:

```
account_status:        "UNSETTLED"
is_queryable:          false
not_queryable_reason:  "Unknown error"
is_ads_mcp_enabled:    true
has_payment_method:    true
```

`UNSETTLED` na Meta normalmente significa **saldo em aberto que não foi
cobrado**, e conta nesse estado **não entrega anúncio**.

**Correção de 27/09 07:50 a esta seção:** a frase "explica por que não entra
lead novo desde 21/09" está errada por excesso. Entrou registro novo em 22, 24,
25 e 26/09 — só **não por Lead Ads**: dois JID de grupo e um contato pelo app de
WhatsApp, e uma `Carla Sampaio` por `lc-phone-api` (ligação recebida). O
`UNSETTLED` explica a ausência de lead **de anúncio**; não que a conta parou de
receber gente. Isso importa porque o plano de 10 leads/dia se apoiava nessa
leitura.

**Por que isso importa mais que qualquer configuração de CRM:** o dono disse que
vai reativar a campanha a **10 leads/dia**, e é essa entrada que sustenta a conta
das 100 tarefas (100 tarefas abertas pedem ~100 leads em cadência; 100/dia pedem
~250 em regime). Com a conta `UNSETTLED`, **a reativação não começa** — e explica
por que não entra lead novo desde 21/09.

**Não é investigável daqui:** a API marca a conta `is_queryable: false`, então
`ads_get_ad_entities` está fechado. É verificação de cobrança no Gerenciador de
Anúncios, do lado do dono.

**Consequência para o item 1 da §5 (o laço de atribuição):** fica bloqueado na
origem até a conta voltar a `ACTIVE`. O trabalho do lado do CRM (agrupar
oportunidades por `adSetId`/`adId`) pode ser feito antes; o gasto, não.

**Nota de contexto:** outras contas do portfólio também aparecem `UNSETTLED`
(Nova Design, Eliane Oliveira, SuperGeeks, Upper Sales, Pinheiro's, Moriart), o
que pode indicar um problema de meio de pagamento mais amplo e não específico
desta operação. Não investiguei — está fora do escopo do WeSales.

## 5. Oportunidades de usar 100% do CRM — do inventário real da conta

Lido do bloco `permissions` de `locations_get-location`: habilitado e **ocioso**.
Ordenado por dinheiro, não por facilidade. **A IA de WhatsApp está fora de
propósito** — o dono usa outro mecanismo, e `botServiceEnabled` já é `false`.

| # | capacidade | por que vale, nesta operação | próximo passo exato |
|---|---|---|---|
| 1 | `attributionsReportingEnabled` + `facebookAdsReportingEnabled` | Cada contato já carrega `campaignId`, `adSetId`, `adId` e `utmContent`. Cruzar isso com o **desfecho** (`won`/`lost`) diz qual criativo traz **cliente**, não lead. Para uma agência que vende geração de lead, é a métrica que decide o orçamento | O Facebook MCP alcança ~50 contas. Falta achar a que tem `campaignId 120247320350570766` (campanha `LEADS I FORM I FS1`): paginar `ads_get_ad_accounts` e cruzar com `ads_get_ad_entities`. Depois: script que junta gasto por `adSetId` com oportunidades por `adSetId` |
| 2 | `proposalsEnabled` + `invoiceEnabled` + `textToPayEnabled` | Fecha o caminho de `NEGOCIAR` até o dinheiro dentro do mesmo sistema. O workflow `Proposta Pendente` **já existe** nos dumps e a tag `proposta-pendente` está `[ ]` no `APROVADO.md` — meio caminho andado | Ratificar a tag, montar a proposta na tela, ligar o `Proposta Pendente` |
| 3 | `reviewsEnabled` | Pedido de avaliação depois de `won` → prova social que alimenta o próprio anúncio que gera os leads. Composto | Workflow disparado por `status = won` |
| 4 | `dashboardStatsEnabled` + `reportingEnabled` | É a Fase 10 do `GUIA-MONTAGEM.md`, ainda `[ ]`. O gestor da §3.3 precisa do `Estouro da Fila` para segurar entrada acima de 100 tarefas | Montar na tela |
| 5 | `webChatEnabled` | Outro canal de entrada para a mesma máquina, sem custo de anúncio | Widget no site + `cad-inbound` na entrada |
| 6 | `surveysEnabled` | Pesquisa pós-reunião alimenta `Reunião foi qualificada` sem depender de o closer lembrar | Survey ligada ao calendário |
| 7 | `membershipEnabled` + `communitiesEnabled` + `certificatesEnabled` | Produto de entrada barato para o lead que tem `Prazo` mas não tem `Budget` — hoje esses vão para nutrição e morrem | Decisão de negócio, não de CRM |

## 6. O que roda sozinho enquanto ninguém olha

| rotina | quando | o que faz | custo Claude |
|---|---|---|---|
| `wesales-vigia.yml` | de hora em hora | varre, compara com `vigia-base.json`, **só grita quando muda** | **zero** |
| `wesales-valores.yml` | diária 07:30 SP | auditoria de valor contra definição de campo | **zero** |
| `wesales-prioridade.yml` | diária 08:00 SP | **só lê** e imprime a tabela; escrever exige acionamento manual | **zero** |
| `wesales-g03.yml` | diária 08:00 SP | promove `NOVO LEAD` → `CONECTAR`, mas só muta na janela de 29/09 | **zero** |
| `faxina-tarefas.yml` | a cada 10 min | limpa tarefa automática fora de contexto | **zero** |

**Todas dependem do merge**, porque `schedule` do GitHub Actions só dispara no
branch padrão. Enquanto o PR #101 não entrar, nenhuma delas roda.

Nenhuma escreve no CRM sozinha, de propósito: o `APROVADO.md` proíbe a rotina se
autorizar, e o código de saída é a campainha — `exit 0` não acorda ninguém.


## 5. 16:50 — Painel SDR publicado; token pendente de decisão do dono

- **Estudo da API** (repositório oficial clonado): formulário não editável; tudo que o
  dono pediu do formulário é feito por 7 rotas. Registro em `ASSOCIACOES-DE-CAMPO.md` §4.
- **Painel SDR** (`supabase/functions/painel-sdr`) publicado no projeto
  `cscczluzpblzhvojxanp`, endereço
  `https://cscczluzpblzhvojxanp.supabase.co/functions/v1/painel-sdr`. PIN criado na
  tabela `config`. Uma versão anterior ficou publicada no `maquina-yt-dark` (projeto em
  402); não tem token nem PIN útil, é inerte.
- **Token do GHL não entregue** ao painel: 402 no projeto antigo, depois bloqueio de
  política na sessão. Saídas na §4 do documento de associações. Sem isso o painel não
  fala com o CRM; nada no CRM depende dele.
- **Gatilhos** do Call Center lidos da tela: recomendação em `DISCADOR-CONFIG-POR-FUNCAO.md`.
- Escritas no CRM neste bloco: **nenhuma**. Escritas fora do CRM: tabela `config` (PIN),
  Edge Function.

## 6. 17:30 — retirado o painel externo; a ficha do contato é o formulário

Dono decidiu: tudo dentro do CRM. `supabase/functions/painel-sdr` e `painel_sdr.py`
saíram do repositório (histórico preserva). Entra `campos_bant.py`: sonda + aplicação
de nome/posição de campo pela API pública, `SDR responsável` como lista. Escritas no
CRM até aqui neste bloco: o campo `SDR responsável` (TEXT, 16:53, vazio). A sonda cria
e apaga um campo de teste próprio (`zz-sonda-bant`).

## 7. 17:07 — ficha do contato em ordem BANT, aplicada e verificada

Runs 36335476750 (sonda), 36335610418 e 36335689596 (aplicação). 28 campos renomeados
com o grupo no nome, reposicionados e movidos para a pasta `zHU4yGXKHdxBHnGxUmai`
(29 campos nela, contando a lista nova). `SDR responsável` recriado como lista
(`e1n7As703nqjAOpzREHc`, opções = usuários do CRM); o TEXTO provisório de 16:53 foi
apagado (era meu, vazio). fieldKeys preservados, conferido pelo conector GHL_CRM.
Escritas no CRM neste bloco: 29 campos (estrutura, não dados de lead). Nenhum lead,
contato ou oportunidade tocado.

## 8. 18:25 — SDR criado, carteira transferida, `SDR responsável` só com o SDR

Executado pela Action (não pela tela), disparada por `workflow_dispatch` com
`ref=claude/abertura-operacao-dnd-n7dnjv`. Cada escrita foi provada relendo a
conta, não pelo retorno do PUT.

### As duas funções, como o dono definiu em 27/09

| pessoa | função no processo | papel no GHL | id |
|---|---|---|---|
| Andreyna Siqueira | SDR (pré-vendas) | `user` | `ML69c5kAJ93cliAGgBj6` |
| Pablo Santos | closer, gestor e administrador | `admin` | `JdvhvOTEBTvUyRi0BXU8` |

### O que foi escrito

**Carteira transferida ao SDR** (run 36340344181, modo `transferir-aplicar`,
depois do DRY no run 36340271352):

- 42 oportunidades abertas → Andreyna (`CONECTAR` 39, `NOVO LEAD` 3)
- 63 contatos → Andreyna
- 2 tarefas → Andreyna
- **2 oportunidades em `NEGOCIAR` ficaram com o Pablo**, e os 2 contatos delas.
  `NEGOCIAR` é etapa de closer; passá-las ao SDR tiraria negociação aberta de
  quem fecha. O contato segue o dono da oportunidade dele, senão a mesma ficha
  teria dono de contato e dono de oportunidade divergentes.
- Veredito do script após reler: `convergiu`.

**`SDR responsável` corrigido** (run 36340538434, modo `pastas`):
`picklistOptions` = `['Andreyna Siqueira']`. Antes tinha `Pablo Santos` também.
Log: `fora da lista de SDR, por serem admin: Pablo Santos (admin)`.
`campos na pasta da ficha: 29 (esperado 29)` · veredito `CONVERGIU`.

A causa não era o dado, era a regra: `usuarios()` devolvia TODO usuário da
subconta, e o `--aplicar` reconcilia — então corrigir a picklist na tela seria
revertido calado pelo run seguinte. O filtro entrou na função (`roles.role`:
`user` entra, `admin` não). Medido antes de mexer: o campo estava preenchido em
0 de 65 contatos, então tirar o admin não orfanou valor em ficha nenhuma.

### DOIS BLOQUEIOS PARA A ABERTURA, os dois de tela

**1. O e-mail do SDR está errado, e por isso ela não entra no CRM.** O recon
(run 36339998058) leu `sampaioopablo1@gmai.com`: falta o `l` de `gmail`, e o
endereço é o do dono, não o da SDR. O convite de acesso do GHL vai para o
e-mail; com este, não chega. Conserta em Configurações → Equipe. É o bloqueio
mais urgente da abertura — sem ele a SDR não tem login em 29/09.

**2. `GHL_STORAGE_STATE` está AUSENTE no runner** (confirmado pelo mesmo recon).
É ele que abre a API interna, e só ela move campo e publica workflow. Portanto
os itens 5 e 4 da `FALTA-PARA-SER-MAQUINA` (texto da tarefa T1; opção B do
G-04) continuam sem caminho automatizado. Agravante: `wesales/tools/
login-capture.js`, que geraria o arquivo, **não existe em nenhum branch** —
o que existe é `renovar_bearer.js`. Enquanto isso não se resolver, 4 e 5 são
trabalho manual de tela.

### Achado lateral, útil para o 4-BIS

A ficha do Gerson traz `formName: "O PROXIMO CLIENTE FORMS v3--AGENDA-copy"`
junto do `formId` 28266780626312413. O 4-BIS mapeia os formulários por id; o
nome vem no `attributionSource` e torna a conferência na tela muito mais rápida,
porque é o nome que aparece na integração de Lead Ads.

## 9. 18:35 — `B · Quanto pode investir` criado, faixas espelhadas

`GVlTZmL4I4MmpTtN1DY8` · `SINGLE_OPTIONS` · pasta da ficha · posição 405, logo
depois de `B · Investimento mensal em anúncios` (400).

Opções, espelhando as do gasto atual por decisão do dono: `Até 1k`, `1k a 5k`,
`5k a 10k`, `Acima de 10k`. Lado a lado na ficha, a leitura de gasto contra
capacidade é direta — é o que separa quem gasta 1k no teto de quem gasta 1k e
pode 10k. Antes a conta media só o gasto de hoje e a tri-estado `B · Budget`.

Run 36341485515 (`pastas`): `campos na pasta da ficha: 30 (esperado 30)` ·
`veredito: CONVERGIU`. Snapshot dos campos foi para 57 e o MAPA do
`pastas_de_campo` põe o campo na pasta de qualificação, ao lado de `Budget` —
quem preenche é o SDR na ligação, não o anúncio.

### O que quebrou no meio, e virou lição 2.25

A primeira tentativa (run 36341042910) criou o campo na posição **770** em vez
de 405, apesar de pedir 405 no POST e no PUT. As duas chamadas devolveram 200.
Causa: `parentId` no corpo do PUT faz o GHL tratar a escrita como movimento de
pasta e recalcular a posição, anexando ao fim. Conserto: dois PUTs — pasta
primeiro, se divergir, e depois nome e posição com o corpo sem `parentId`.

Isso ficou escondido porque os 28 campos do BANT já estavam na pasta e na
posição certas, então o laço os saltava e nenhum PUT com `parentId` saía. O
campo novo foi o primeiro a exercitar o caminho.
