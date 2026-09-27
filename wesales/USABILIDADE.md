# Usabilidade por função — renomear e agrupar, sem criar nada

Pedido do dono em 27/09/2026: *"confesso que ainda acho meio completo e confuso.
Importante é para as funções… defina a tag, lista de hoje, lista para ligar,
defina melhor o nome, e simplesmente começa a tocar a fila do dia da cadência.
Não quero que recrie do zero os campos, parâmetros — revise, teste, se coloque no
lugar das funções."*

**Regra deste documento: zero campo novo, zero tag nova** (com uma exceção
condicional, na §3). Só renomear, agrupar e escolher o que fica visível.

---

## 0-BIS. CORREÇÃO DA §0 (27/09 12:20) — os leads ESTÃO inscritos, e parados na janela

A §0 abaixo está preservada como foi escrita, porque o raciocínio dela ainda
explica o que o SDR vê. Mas **a hipótese central estava errada**, e a prova estava
no próprio repositório — no docstring do `wesales/tools/patch_janela_abertura.py`
(branch `claude/amazing-johnson-mclksg`), escrito hoje mais cedo:

> *"Pior: a cadência JÁ ENTROU e está parada. Prova nos campos do `Carlos Andrade`:
> `Tentativa nº` = 0 e `Permissão WhatsApp` = 'Não solicitado' (os nós de campo
> rodaram), e `atraso-1a-tentativa` ainda presente (a 1ª tentativa NÃO rodou).
> Campo e tag rodam fora do horário; **só a mensagem espera a janela.**"*

E os mesmos carimbos estão nos leads que eu li. No `Gerson`: `Tentativa nº` = 0,
`Permissão WhatsApp` = `Não solicitado`, `WA não atendidas seguidas` = 0,
`Checkpoint — Tentativa nº` = 0. **São exatamente as escritas de inicialização do
nó 0.** Eu li isso como "nada rodou". É o contrário: rodou o nó 0 e **parou no
primeiro `Wait`**, porque o que vem depois é o nó de mensagem, e esse espera a
janela de execução.

**A ordem no fluxo publicado explica o resto.** A tag de fila e a tarefa ficam
**depois** do nó de mensagem. Então a ausência delas não é defeito: é a fila do
dia que **ainda não começou**. Quando a janela abrir — segunda 28/09 08:30 — as
execuções paradas retomam, a MI-0 sai, e aí a tag e a tarefa aparecem.

### O que isso muda, item por item

| o que eu disse na §0 | o que é, corrigido |
|---|---|
| "as cadências não inscreveram os 38" | **inscreveram**; estão parados antes do primeiro toque |
| "`Allow Re-entry` desligado ⇒ nada os inscreve depois" | irrelevante — já estão dentro |
| "a terça abre com fila vazia" | a fila se enche sozinha quando a janela abrir |
| "risco de a máquina NÃO agir" | **não existe.** O risco real é o original: ela agir **segunda**, um dia antes |
| `Add to Workflow` em lote é o conserto | **não é conserto, é dano**: inscreveria de novo quem já está inscrito |

**Retiro o `Add to Workflow` em lote da lista de ações.** Era a recomendação
errada, derivada da hipótese errada, e executá-la duplicaria execução.

### O que sobrevive da §0, e continua valendo

- **A `fila-wa` nunca é aplicada por workflow nenhum** (§9). Esse achado é
  independente e não é resolvido pela janela: a lista 8.3 e o bloco de WhatsApp da
  §3.1 seguem sem fila.
- **A lista 8.5 do gestor** segue com 18 linhas e precisa da cláusula `status open`.
- **O `sdr-lotado`** segue lido por quatro workflows e escrito por nenhum (§8).
- **A pergunta de tela continua útil**, só mudou de motivo: a contagem de inscritos
  na `Cadência Inbound` agora serve para **confirmar** que são ~38 parados, não
  para descobrir se alguém entrou.

### E o que a correção diz sobre a escrita do módulo 1

Conferi os portões da cadência publicada antes de concluir. Os dois que decidem
toque e mensagem exigem a tag **ausente**:

```
MI-0 · Ainda vale mandar?   →  contact_detail · tags · index-of-false · ['nao-perturbe']
TI1 · Ainda vale ligar?      →  contact_detail · tags · index-of-false · ['nao-perturbe']
```

Então a tag que eu apliquei nos 31 é exatamente o que a cadência consulta antes de
mandar a MI-0. Com ela presente, o ramo de envio não é tomado. **A escrita está
certa e é proteção real**, não cosmética.

Com uma ressalva honesta, que o `patch_janela_abertura.py` já havia levantado: não
consigo provar pelo dump se o ramo alternativo **encerra** o fluxo ou **pula e
segue** para a tentativa seguinte. Se pular, a régua avança sem falar com ninguém —
custo de posição na cadência, não de reputação nem de gasto. Por isso a tag **não
substitui** fechar a janela em `days: [2]`: a janela segura toda execução parada e
se desfaz numa linha. A tag garante que nenhuma mensagem sai; a janela garante que
nem o avanço acontece. As duas juntas é o certo, e a janela continua sendo sua.

---

## 0. O achado que vem antes de tudo: a fila do SDR não existe como dado

Medido em 27/09/2026, leitura pura pelo conector `GHL CRM`, nenhuma escrita.
Isto foi procurado porque o pedido do dono era claro — *"importante e crítico
é o SDR, ao filtrar, ter pelo menos 100 tarefas, de forma clara e
organizada"*. Fui conferir quantas tarefas ele tem hoje.

### O que a conta devolve

Varrendo as **39 oportunidades abertas** em `CONECTAR` e contando as tags de
cada contato:

| tag | em quantos dos 39 |
|---|---|
| `etapa-conectar` | 39 |
| `cad-inbound` | 38 |
| `atraso-1a-tentativa` | 38 |
| `limpar-tarefas` | 5 |
| `nao-perturbe` | 3 |
| **`fila-tel`** | **0** |
| **`fila-wa`** | **0** |
| **`fila-quente`** | **0** |

E as tarefas. A primeira leitura foi por amostra de 6 contatos; refiz com
`getTasks` no pipeline inteiro, que é exato e custa uma chamada:

**64 oportunidades no `FUNIL DE VENDAS`. Duas tarefas.** As duas em contato de
**teste**, as duas vencidas em **22/09** (cinco dias), as duas ainda abertas:

| tarefa | contato | vence |
|---|---|---|
| `[CADENCIA] T1 · WhatsApp → Ligar` | `Teste Não Atende` | 22/09 |
| `[TESTE] tarefa variante A` | `Teste Retorno` | 22/09 |

O corpo da primeira manda *"Ligar pelo WhatsApp (botão **Ligar via WhatsApp** na
conversa)"* — o botão que o `CANAIS.md` provou não existir nesta conta.

**Nenhum lead real do funil tem uma única tarefa.** E as tags `fila-*` do
inventário pertencem todas a **um** contato: `ZZ TESTE ESTRUTURA`, abandonado em
`NOVO LEAD`, que carrega as 20 tags do projeto de uma vez — é o fixture de
criação de tag, não um lead.

### O que isso faz com a tela do SDR na terça

As quatro listas favoritas dele (§1.7 da `IMPLEMENTACAO-WORKFLOWS.md`)
filtram assim:

| lista | filtro principal | linhas hoje |
|---|---|---|
| 8.1 `Fila Quente` | tag `fila-quente` | **0** |
| 8.2 `Fila Telefone Hoje` | tag `fila-tel` | **0** |
| 8.3 `Fila WhatsApp Hoje` | tag `fila-wa` | **0** |
| 8.4 `Retornos` | `Resultado da tentativa` = `Pediu retorno` | **0** (o campo está vazio em 38 de 38) |

**As quatro listas do SDR abrem vazias, e a fila de tarefas também.** O alvo
do dono era 100 tarefas; o número é zero.

A única lista que enche é a do **gestor**: 8.8 `Atraso na 1ª Tentativa`, com
**38 linhas** — a tag `atraso-1a-tentativa` está em 38 dos 39. A conta hoje
mostra o alarme e esconde o trabalho.

### Por que, e o que separa hipótese de fato

O que é **fato**: as tags `fila-*` e a tarefa `[CADENCIA]` são escritas pelo
bloco de tentativa das cadências (nós 6 e 0.7 do W11/W12). Nenhum artefato de
cadência aparece nos 38 — sem tag de fila, sem tarefa, `Template usado`
vazio, `Tentativa nº` = 0. Ao mesmo tempo, `atraso-1a-tentativa` está em 38
deles, e esse alerta é o **W15, que roda sem janela**.

O que é **hipótese**: que as duas cadências não inscreveram os 38, enquanto o
alerta sem janela rodou. O padrão aponta para lá, mas a leitura por API **não
enxerga inscrição em workflow** — não há endpoint para isso. Quem distingue é
a contagem de *contatos inscritos* na tela de cada cadência, e leva dez
segundos.

### A consequência que torna isso urgente, e não só feio

Os dois gatilhos são `Opportunity Stage Changed → CONECTAR`, e **`Allow
Re-entry` está desligado nas duas** (§W11/W12). Os 38 **já estão** em
`CONECTAR`. Então, se eles nunca foram inscritos, **nada os inscreve depois** —
nem terça, nem nunca. Fechar a janela em `days: [2]`, que era o item com
prazo, não resolve isto: janela controla *quando* a régua dispara, não *se* o
contato entrou nela.

Dito ao contrário: o risco que eu vinha tratando como o principal (mensagem
saindo cedo demais na segunda) é o risco de a máquina **agir**. Este é o risco
de ela **não agir** — e ele é maior, porque não faz barulho.

**Como conferir, na tela, em dois minutos:** Automação → `Cadência Inbound` →
aba de contatos inscritos. Se der 0 ou algo bem abaixo de 38, está confirmado.

**Como consertar, e é trabalho de tela (não sai por API):** selecionar os
leads em `CONECTAR` e usar **`Add to Workflow` → `Cadência Inbound`** em lote.
Isso entra pela porta certa: o nó 0 atribui dono, grava `Entrada em`, põe a
tag de fila e cria a tarefa. Mover para outra etapa e trazer de volta também
funciona, mas mexe no funil e suja o histórico de etapa — pior caminho.

### Uma terça que funciona sem depender de nada disso

Se a inscrição em lote não acontecer antes de 29/09, ainda há um caminho de
três passos que usa **só o que já existe**, sem tag nova, sem campo novo e
sem workflow:

1. Lista inteligente nova com um filtro só: **`Prioridade` ≥ 3**. Hoje isso
   devolve exatamente os **5 do lote 1** — a rampa de 6/dia, que é a meta da
   semana de abertura. Os 34 travados ficam de fora sozinhos, porque estão em
   `Prioridade` 0.
2. Copiar dali as 5 linhas `telefone, nome`.
3. Call Center → `Fila de ligações` → colar na **caixa de texto editável** →
   `Iniciar discagem`.

Cinco linhas colam à mão sem esforço. Isso também **contorna o risco do
"puxar por pipeline"** descrito na §3 (que traria os 39, incluindo os 34 em
DND) sem precisar esperar o teste de 10 segundos.

### O efeito colateral que ninguém procurou: a lista do gestor também quebrou

A lista **8.5 `Sem resultado ontem`** — a que a §3.3 manda o gestor abrir todo
dia às 08:15 como *"tentativa que o SDR não fez"* — filtra tag
`limpar-tarefas` **E não** `fila-tel` **E não** `fila-wa`.

`limpar-tarefas` está em **19** contatos. Como só o `ZZ TESTE ESTRUTURA` tem tag
`fila-*`, as duas cláusulas de exclusão **não excluem ninguém**, e a lista
devolve **18 linhas**. Dessas, **11 são `lost` ou `abandoned`**, uma é o
`Pablo Sampaio` (o próprio dono) e duas são o `Daniel` e o `Genilson` — os dois
melhores leads da conta, que estão com o **closer** em `NEGOCIAR` e não têm nada
a ver com tentativa de SDR.

Ou seja: a mesma causa esvazia as quatro listas do SDR **e** enche a do gestor
de lixo. Um alarme que aponta 18 nomes errados todo dia às 08:15 deixa de ser
lido na primeira semana.

Dois consertos, de tamanhos diferentes:

- a inscrição em lote devolve as tags `fila-*` e as exclusões voltam a excluir;
- e a 8.5 precisa de uma cláusula que o documento nunca teve: **status `open`**
  (e, se o gestor quiser, etapa = `CONECTAR`). Sem ela, lead descartado continua
  aparecendo para sempre, porque `limpar-tarefas` não sai no descarte. Isso é
  edição de lista, não workflow — cabe na tela em um minuto.

### Três coisas menores, achadas na mesma leitura

**1. Dois leads abertos em `NOVO LEAD` aparecem sem nome utilizável**
(`+5521969613820` e `+5511951285383`). **A causa que eu atribuí primeiro — o
formulário do Meta — estava errada**; ver a correção logo abaixo, que é mais
útil: um é o app de WhatsApp gravando `Sem nome`, o outro é uma oportunidade em
branco de um contato que tem nome.

**2. A única oportunidade aberta em `REUNIÃO DE DIAGNÓSTICO` é o próprio dono**
(`Pablo Sampaio`, `+5521987429940`) — o teste do calendário. Não é lead. Enquanto
estiver lá, as contagens mensais de funil (listas 8.9–8.12) e o widget de
agendamentos do painel contam o dono como reunião realizada. Descartar com
status `lost` (nunca excluir, regra 1) limpa isso.

**3. `FORMALIZAR` está vazia e não existe um `won` nas 64 oportunidades.** Já
sabido, mas agora com o número fechado do pipeline inteiro: a máquina nunca
levou ninguém até o fim. Não é defeito de configuração — é a razão de a abertura
existir.

### CORREÇÃO (27/09 07:50) — os "leads sem nome" não vêm do formulário

Na rodada anterior eu escrevi que dois leads abertos em `NOVO LEAD` chegaram sem
nome e que valia conferir o formulário do Meta antes de reativar a campanha.
**A causa estava errada.** Fui ler os cinco registros um por um; nenhum veio de
Lead Ads.

| registro | criado | `createdBy.source` | o que é de verdade |
|---|---|---|---|
| `+120363294985523330` | 24/09 | `INTEGRATION`/OAUTH `…mawx7is9` | JID de grupo do WhatsApp (18 dígitos) — já tratado |
| `+120363226349138496` | 26/09 | idem | JID de grupo do WhatsApp — já tratado |
| `+5511951285383` | 24/09 | idem — o **app de WhatsApp** | **pessoa real**, 13 dígitos, tem foto de perfil do WhatsApp. Aberto em `NOVO LEAD` |
| `+552123915933` | 22/09 | — | fixo do Rio (12 dígitos), `abandoned` |
| `+5521969613820` | 25/09 | **`lc-phone-api`** | **`Carla Sampaio`** — o contato TEM nome; é a **oportunidade** que está em branco |

Duas coisas diferentes, e as duas mais úteis do que "formulário errado":

**1. O app de WhatsApp grava `Sem nome` como nome do contato.** `+5511951285383`
é gente de verdade — tem foto de perfil — e o CRM chama a pessoa de `Sem nome`,
porque é isso que o app põe quando o WhatsApp não expõe nome de exibição. É o
**mesmo `sourceId` (`…mawx7is9`) que traz os JID de grupo**: uma integração só
responde pelos dois defeitos. Consequência na tela: o SDR abre a ligação sem ter
como chamar a pessoa. O conserto não é no formulário — é decidir o que fazer
quando o app manda `Sem nome` (usar o telefone como rótulo já seria melhor, e é
o que o `554791548812` de `CONECTAR` mostra que acontece por outro caminho).

**2. A oportunidade da Carla está sem nome, e o contato não.** No quadro de
Oportunidades e numa puxada por pipeline no Call Center (que devolve
`número, nome`), essa linha aparece **em branco**. É defeito de exibição do
nó que cria a oportunidade, não de captação.

### O que o `lc-phone-api` revela sobre o `Receber` — resposta parcial, e é a primeira evidência do caminho de entrada

A `Carla Sampaio` foi criada em **25/09 por `lc-phone-api`**, ou seja **por uma
ligação recebida**, e carrega `Duração da ligação` = **40** e `Conexão real` =
`Não` (coerente com a regra do F-06, que só conta acima de 60 s).

Isso é a **primeira evidência em todo o projeto de que o caminho de entrada
produz dado**: chamada de entrada chega neste número, gera contato e é medida.

**O que isso NÃO prova**, e não vou esticar: os 40 segundos podem ser tempo de
toque em vez de conversa, e a leitura é de **25/09** — anterior à tela em que eu
vi o `Receber` em `Desativado`. Então a pergunta da §3 continua valendo, só
deixou de ser no escuro: já existe um registro de entrada atendido o bastante
para virar contato e número. O teste de ligar do celular para `5512982381407`
segue sendo o que decide.

### O segundo achado da mesma varredura: 42 de 47 leads não têm dono

`assignedTo` está **nulo em 42 das 47 oportunidades** de `CONECTAR`. Os cinco
que têm dono são os **três contatos de teste** mais `Carlos Andrade` e
`554791548812` — ou seja, exatamente os que passaram pela máquina. O registro
de contato do Gerson não traz campo de dono nenhum.

Isso é o **R-10** da §3 do `ESTADO-27-09.md`, e a varredura mostra por que ele
não é cosmético:

- W13 nó 7 entrega a tarefa "ligar agora" ao **`Contact Owner`**. Sem dono, a
  tarefa nasce sem ninguém.
- W13 nó 8 e W14 nós 6/6b mandam `Internal Notification` ao **`Contact Owner`**.
  Sem dono, o aviso não tem destinatário.
- A §3.1 diz que a notificação "respondeu agora" é **o único caso em que o SDR
  interrompe o bloco**, com SLA de 10 minutos. É justamente esse aviso que não
  chega.

Com **um** SDR isso passa despercebido nas listas (elas não filtram por dono —
a §1.7 registra que o GHL não tem "usuário atual" em lista). Mas passa a doer
em dois lugares hoje: na tarefa sem responsável e no aviso sem destinatário.

O `Add to Workflow` em lote do item acima **resolve os dois de uma vez**,
porque o nó 0.8b é o round robin que atribui o dono. É outra razão para ele ser
a primeira coisa a fazer na tela.

### O que isso muda neste documento

A §2 (renomear listas) e a §4 (quatro pastas de campo) continuam válidas e
valem pouco **agora**: são apresentação em cima de uma fila vazia. Lista
renomeada que devolve zero linha não fica menos confusa — fica mais, porque o
nome promete trabalho que não está lá. **A ordem certa é: inscrever os leads,
depois arrumar a vitrine.**

---

## 1. Por que está confuso — medido, não opinado

Contando os `parentId` das 56 definições que `locations_get-custom-fields`
devolve:

| pasta | campos |
|---|---|
| `gabsbU3jsUN7oIXCnYab` | **53** |
| `zHU4yGXKHdxBHnGxUmai` | 2 (`Urgência`, `Empresa`) |
| `vCqedGd185RiQKNlU870` | 1 (`Conexões WhatsApp`) |

**53 de 56 campos numa única pasta.** O SDR abre o contato e vê tudo em bloco —
e ele preenche **um** campo por tentativa (`Resultado da tentativa`, §3.1 da
`IMPLEMENTACAO-WORKFLOWS.md`). O resto é contador que ele não deve tocar, campo
do closer e resposta do formulário.

A confusão não vem de excesso de recurso. Vem de **agrupamento que o GHL oferece
e ninguém usou**.

Mesma coisa nas listas: as 4 favoritas do SDR têm uma ordem de abrir que existe
**só no documento**. Às 08:30 ele precisa lembrar qual vem primeiro.

## 2. O nome carrega a ordem

A tela passa a dizer o que fazer, e o prefixo numérico faz as favoritas se
ordenarem sozinhas.

| nome hoje | nome proposto | por quê |
|---|---|---|
| `Fila Quente` | **`1 · LIGAR AGORA`** | é quem sinalizou; atrasar isto é perder a conversa |
| `Retornos` | **`2 · HORA MARCADA`** | tem hora combinada, fura a fila |
| `Fila Telefone Hoje` | **`3 · FILA DO DIA`** | é a entrada do Power Dialer |
| `Fila WhatsApp Hoje` | **`4 · WHATSAPP (só com permissão)`** | o nome avisa por que está vazia hoje: `Permissão WhatsApp` = `Não solicitado` em 38 de 38 |

Para o gestor, o mesmo princípio de nome que diz a ação:

| hoje | proposto |
|---|---|
| `Estouro da Fila` | **`ALERTA · Fila passou de 100 hoje`** |
| `Sem resultado ontem` | **`ALERTA · Tentativa não feita ontem`** |
| `Atraso na 1ª Tentativa` | **`ALERTA · Lead novo sem toque`** |

Para o closer, duas listas e nada mais:

| proposto | filtro |
|---|---|
| **`1 · AGENDA DE HOJE`** | agendamento hoje, status `Confirmed` |
| **`2 · VEREDITO PENDENTE`** | compareceu e `Reunião foi qualificada` vazio |

## 3. A fila do dia e o discador — CORRIGIDO com a tela real (27/09)

**Atenção: a versão anterior desta seção estava errada.** Eu pesquisei o Power
Dialer *nativo* do GHL (alimentado por workflow com `Manual Action: Call`, rodado
em Conversas → Ações Manuais). **Não é essa a ferramenta desta conta.** O dono
mandou a tela: é um **"Call Center" próprio do WeSales CRM** (white-label, em
`app.wesalescrm.com`), com mecânica diferente. A pesquisa sobre o dialer nativo
não se aplica e foi descartada.

### O que a tela realmente tem

Menu: `Call center` · **`Fila de ligações`** · `Disparo` · `Gatilhos` ·
`Mensagens rápidas` · `Dashboard`.

Na `Fila de ligações`, o bloco **"PUXAR DO CRM"** com exatamente dois modos:

| modo | o que oferece |
|---|---|
| **Pipeline** | escolher um pipeline + um estágio (ou `Todos os estágios`) → `Puxar leads deste pipeline` |
| **Tag** | escolher uma tag → `Puxar contatos desta tag` |

O resultado cai numa **caixa de texto editável** (`número, nome`, uma por linha),
que o SDR pode colar ou corrigir à mão. Abaixo: `TOQUE MÁX. (S)` = 30,
`PAUSA ENTRE LIGAÇÕES (S)` = 3, e o botão **`Iniciar discagem`**.

No topo: **`NÚMERO ATIVO: O Próximo Cliente · 5512982381407`** — confirma que há
número configurado, e é o mesmo do campo `phone` da subconta. Isso fecha uma
pergunta que a API não respondia.

### A consequência ruim, e é a mais importante deste documento

**A `Prioridade` não chega ao discador.** Ele puxa por pipeline+estágio ou por
tag e entrega uma **lista plana**. Toda a reconciliação de `Prioridade` feita em
27/09 ordena a **lista inteligente**, que é outra tela. O discador ignora.

E o risco concreto: se o SDR puxar por `Pipeline → FUNIL DE VENDAS → CONECTAR`,
ele provavelmente traz **os 39**, incluindo os **34 em DND**. A `Prioridade` = 0
não protege aqui, porque o discador não lê esse campo.

Isso promove a tag de "otimização" para **única forma segura de alimentar o
discador**.

### O teste que decide, e leva 10 segundos na tela

`Fila de ligações → Pipeline → FUNIL DE VENDAS → CONECTAR → Puxar leads deste
pipeline`, e **contar os nomes na caixa**:

- **5 nomes** → o "puxar" respeita DND. A tag vira conveniência, não necessidade.
- **39 nomes** → o "puxar" **ignora DND**. Discar por pipeline liga para quem
  está travado, e a tag `fila-do-dia` passa a ser **obrigatória antes de terça**.

Enquanto esse teste não for feito, a regra segura é: **não puxar por pipeline.**

### O desenho, dado o que a tela permite

**`fila-do-dia`** — uma tag, mantida pelo `recalcula_prioridade.py`: entra quem
tem `Prioridade` >= 3, sai quem caiu abaixo. O SDR abre `Fila de ligações → Tag →
fila-do-dia → Puxar contatos desta tag → Iniciar discagem`. Três cliques, sem
escolher nada, sem risco de trazer lead travado.

Detalhes que não são opcionais:

- **Remover a tag importa tanto quanto pôr.** Tag que fica é lead discado sem
  motivo — e aqui o discador liga de verdade, não é uma lista para olhar.
- **A ordem dentro da fila se perde.** Se a ordem importar, o caminho é a tag
  por faixa (`fila-5`, `fila-4`…) e o SDR puxa a de cima primeiro. Mais tags,
  mais manutenção — só fazer se o volume justificar.
- Precisa de `[x]` no `APROVADO.md`: é tag nova e a rotina não se autoriza.

### ACHADO NA PRÓPRIA TELA: `Receber` está **Desativado**

No topo do Call Center, ao lado do número ativo, há um interruptor **`Receber`**
com o rótulo **`Desativado`** abaixo — e o botão aparece desligado.

**Por que isso importa mais do que parece:** a operação vai discar dezenas de
vezes por dia com `TOQUE MÁX.` de 30 segundos. Lead que não atende e vê a chamada
perdida **liga de volta** — é o retorno mais barato que existe, porque o lead já
está com o telefone na mão e a intenção fresca. Com `Receber` desligado, essa
ligação não é atendida aqui.

**O que eu não sei, e não vou afirmar:** se `Desativado` significa que o número
rejeita a chamada de entrada, que ela cai em caixa postal, ou apenas que **esta
aba do navegador** não toca (o padrão em softphone). As três consequências são
diferentes, e só quem tem a tela distingue.

**Como conferir, e é rápido:** ligar do celular para `5512982381407` e ver o que
acontece — toca na tela, cai em algum lugar, ou dá ocupado. Cinco minutos, e
decide se a operação está perdendo o retorno mais fácil do funil.

### O que ainda não foi olhado nessa ferramenta

`Disparo`, `Gatilhos`, `Mensagens rápidas` e `Dashboard` são quatro telas do
mesmo Call Center que ninguém examinou. `Gatilhos` em especial pode mudar o
desenho de novo — vale abrir antes de fechar qualquer decisão.

## 4. Cinco pastas de campo, em vez de uma de 53

Reagrupar os campos que já existem. Nenhum criado, nenhum apagado.

**Esta seção foi refeita em 27/09** e o motivo importa mais que o resultado. A versão
anterior tinha quatro pastas, e uma delas se chamava `4 · VEIO DO ANÚNCIO` com **20
campos** — todo o BANT (`Budget`, `Decisor`, `Prazo`, `Tem time comercial`…). O dono
corrigiu o entendimento: **são dois formulários diferentes.** O do Meta Ads traz o
lead; o de qualificação é preenchido **pela SDR** para marcar a reunião com o closer,
e os campos entram no lead ao longo do processo até o fechamento.

Em vez de supor qual campo vem de onde, medi. Contagem de preenchimento nos 64
contatos da conta, versionada em `wesales/dados/campos-27-09.json`:

| campo | preenchidos | leitura |
|---|---|---|
| `Urgência` | **40 / 64** | vem do anúncio |
| `Necessidade` | **34 / 64** | vem do anúncio |
| `Investimento mensal em anúncios` | **32 / 64** | vem do anúncio |
| `Dor principal` | 6 / 64 | a SDR preenche |
| `Budget`, `Decisor`, `Prazo`, `Tem time comercial` | 3 / 64 | a SDR preenche |
| `Segmento`, `Site`, `Instagram`, `Usa CRM`, `Empresa` | **0 / 64** | ninguém preencheu ainda |

A separação é limpa: **três campos** chegam com o lead; os outros 17 do bloco antigo
ficam entre 0 e 6. Se viessem do formulário do anúncio, os 64 teriam.

**Por que isso não é cosmético:** chamar de "veio do anúncio" um campo que a SDR precisa
preencher esconde trabalho dela na tela. O campo vazio pareceria dado que o anúncio não
mandou, em vez de pergunta que falta fazer — que é exatamente o erro da §1.2 do
`LICOES-DO-PROJETO.md` ("campo vazio pode ser 'ainda não', não 'faltou'").

| pasta | o que vai dentro | quem vê |
|---|---|---|
| **`1 · SDR PREENCHE A CADA TENTATIVA`** | `Resultado da tentativa`, `Data de retorno`, `Hora do retorno` | SDR, a cada ligação |
| **`2 · SDR PREENCHE NA QUALIFICAÇÃO`** | `Budget`, `Decisor`, `Prazo`, `Dor principal`, `Tem time comercial`, `Clientes novos por mês`, `Quem atende os leads`, `Canal principal de venda`, `Usa CRM`, `Investe em anúncios`, `Plataformas de anúncio`, `Já teve agência?`, `Experiência com agência`, `Segmento`, `Site`, `Instagram`, `Empresa` | SDR, para marcar com o closer |
| **`3 · VEIO DO ANÚNCIO`** | `Urgência`, `Necessidade`, `Investimento mensal em anúncios` | SDR lê antes de ligar |
| **`4 · CLOSER PREENCHE`** | `Reunião foi qualificada`, `Motivo da desqualificação`, `Data do veredito do closer` | closer |
| **`5 · NÃO MEXER — a máquina escreve`** | `Prioridade`, `Tentativa nº`, `Entrada em`, `1ª tentativa em`, os dois `Checkpoint`, `Toques na semana`, todos os contadores de ligação/conexão, `Template usado`, `Nota de qualificação`, `Permissão WhatsApp`, e os campos de data do fluxo — 30 no total | ninguém edita |

O `Motivo da desqualificação` aparecia nas pastas 1 e 3 da versão antiga, nas duas. É do
closer, pela picklist (`Sem fit`, `Sem budget`, `Timing errado`…) e pelo par com
`Data do veredito do closer`. Ficou só na pasta do closer.

### Metade do arrasto sai de graça — renomeando, não movendo

Mover campo não sai por API, mas **renomear pasta sai**: `PUT /custom-fields/folder/{id}`,
corpo `{name, locationId}` — conferido no spec, não suposto (a §2.12 existe por eu ter
suposto uma vez).

E a pasta única `gabsbU3jsUN7oIXCnYab` já contém **29 dos 30 campos que a máquina
escreve**. Então a pasta 5 não precisa ser criada e povoada: ela **é** essa pasta, com
outro nome. Os 29 campos ficam exatamente onde estão.

| | arrastos na tela |
|---|---|
| criar 5 pastas vazias e mover tudo | **56** |
| renomear a grande e criar 4 | **27** |

Os 27 são 3 + 17 + 3 + 3, mais `Conexões WhatsApp` sozinho — o único campo da máquina
que mora fora da pasta grande (`vCqedGd185RiQKNlU870`).

As duas pastas pequenas ficam vazias depois do arrasto e **não são apagadas**: pasta
vazia não machuca ninguém, e apagar exigiria o verbo que a regra 1 proíbe.

O mapa está no código, não só aqui: `wesales/tools/pastas_de_campo.py`. O modo `--plano`
**confere** o mapa contra o snapshot da conta e falha se algum campo sobrar, faltar ou
aparecer em duas pastas — os 56 fecham. Isso roda na Action sem segredo nenhum, antes de
qualquer escrita, porque mapa escrito à mão erra em silêncio: campo com nome trocado
nunca apareceria no arrasto.

O nome da pasta 5 é metade do valor: **`NÃO MEXER`** é a instrução que a §3.1
tenta dar por documento ("quem 'ajuda' a automação à mão quebra a contagem e o
roteamento sem ver erro nenhum") e que a tela pode dar sozinha.

### Por qual caminho isso sai — conferido no spec oficial em 27/09

O conector `GHL CRM` só **lê** campo personalizado, então por ele não sai. Fui ao
spec oficial da API pública (`GoHighLevel/highlevel-api-docs`, clonado do GitHub
porque os domínios do GHL são negados pelo proxy) e a resposta é dividida:

| o que | rota | dá? |
|---|---|---|
| criar as 5 pastas | `POST /custom-fields/folder` | **sim** |
| renomear pasta | `PUT /custom-fields/folder/{id}` | **sim** |
| campo **novo** já nascer em pasta | `POST /custom-fields/` (aceita `parentId`) | **sim** |
| **mover campo existente** para uma pasta | `PUT /custom-fields/{id}` | **NÃO** — o corpo não tem `parentId` |

**Registro de um erro meu, porque ele quase virou script:** ao ver as duas primeiras
rotas eu anunciei ao dono que o reagrupamento dos 53 campos estava destravado por
API. Fui escrever o script, li o `requestBody` do `PUT`, e não tem `parentId`. O único
caminho por API seria criar campo novo em pasta e apagar o antigo — e apagar campo é
proibido pela regra 1 e destruiria o dado de todos os contatos.

**Um segundo erro, achado antes de rodar:** a primeira versão do script leu só a lista
`fields` da resposta do `GET /custom-fields/object-key/{objectKey}` e procurou pasta lá
dentro, para não recriar o que já existe. O spec mostra que a resposta tem **duas**
listas, `fields` e `folders` — então a checagem nunca acharia nada e o script criaria as
cinco pastas de novo a cada execução. O que escondeu isso: o conector MCP também
devolve só `fields`, e a conta já tem três pastas em uso (`gabsbU3jsUN7oIXCnYab` com 53
campos, `zHU4yGXKHdxBHnGxUmai` com `Urgência` e `Empresa`, `vCqedGd185RiQKNlU870` com
`Conexões WhatsApp`) que nenhuma das duas leituras mostrou.

**Então isto segue trabalho de tela**, e segue valendo: é a origem da queixa do dono
("meio completo e confuso"), com 53 de 56 campos numa pasta só. A lição virou entrada
2.12 do `LICOES-DO-PROJETO.md`: endpoint existir não é capacidade — ler
`requestBody.properties` antes de anunciar.

## 5. O teste de usabilidade, que é o único jeito de saber

Sentar na cadeira de cada função e cronometrar:

| função | tarefa | hoje | alvo |
|---|---|---|---|
| SDR | do login até a primeira discagem | **não tem como medir: as quatro listas devolvem zero linha (§0)** | < 30 s, sem escolher nada |
| SDR | registrar o resultado de uma ligação | ? | < 15 s, um campo |
| closer | do aviso de agendamento até ver a nota e o BANT | ? | < 20 s, uma tela |
| gestor | saber se a fila estourou hoje | ? | < 10 s, um número |

Dos quatro, o primeiro já tem resposta e ela é a da §0: **não há o que
cronometrar enquanto a fila estiver vazia**. Os outros três seguem sem medição,
e quem mede é quem tem a tela.

## 6. O que fica fora, de propósito

- **Não recriar campo, tag ou workflow.** A máquina está desenhada e testada; o
  problema é de apresentação.
- **Não apagar nada.** O `APROVADO.md` proíbe, e não é preciso: o que confunde
  fica escondido em pasta, não excluído.
- **Não mexer na IA de WhatsApp.** O dono usa outro mecanismo, e
  `botServiceEnabled` já é `false`.

## 7. As dez listas que faltavam, medidas contra a conta (27/09 09:00)

Mesmo método da §0: ler o filtro declarado na §1.7 da `IMPLEMENTACAO-WORKFLOWS.md`
e contar quantas linhas ele devolve **de verdade**. Uma chamada
(`contacts_get-contacts`, 64 contatos, que ao contrário da busca de oportunidade
traz `dnd`, `dndSettings`, tags e campos personalizados). Leitura pura.

| lista | filtro | linhas hoje | veredito |
|---|---|---|---|
| 8.26 `Auditoria — tag sem DND nativo` | tag `nao-perturbe` **E** DND desligado | **9** | acende, e por motivo real |
| 8.27 `Auditoria — DND sem tag` | DND ligado **E** sem tag `nao-perturbe` | **31** | acende, **e a causa fui eu** |
| 8.18 `Higiene — Sem Telefone Válido` | sem telefone **OU** `telefone-invalido` | **12** (7 de teste, 5 reais) | funciona, mostra sujeira de verdade |
| 8.25a `Entrada — últimas 24h` | criado há < 1 dia | 2 | funciona |
| 8.25b `Entrada — últimos 7 dias` | criado há < 7 dias | 21 | funciona |
| 8.14 `Reengajamento em Curso` | tag `reengajamento-ativo` | 1 (o fixture) | vazia na prática |
| 8.16 `Fila do Dia — Total` | `fila-tel` **OU** `fila-wa`, sem `nao-perturbe` | **0** | vazia pelo motivo da §0 |
| 8.6 `Conexão por Tentativa` | `Total de conexões` ≥ 1 | **1**, e é contato de teste | sem insumo real |
| 8.7 `Calibração da Régua` | `Reunião foi qualificada` não vazio | **2**: `Pablo Sampaio` e `Teste Atendeu` | sem insumo real |
| 8.13 `Resposta por Template` | `Sinal recebido` não vazio | **1** (`Rafaela de Paula`) | um sinal na conta inteira |
| 8.17 `Recuperação de No-show` | `Nº de no-shows` ≥ 1 | **0** | nunca teve insumo |

Três grupos, e cada um quer coisa diferente:

- **8.26 e 8.27 acendem por defeito real** — abaixo, é o achado da rodada.
- **8.18, 8.25a e 8.25b funcionam.** A 8.18 aponta cinco leads reais sem telefone
  usável (`TINTIM`, `Dkw.oficial`, `Nathalia.ggss`, `Carla X. Sampaio`,
  `Thiagoreis`), todos já `lost` em `CONECTAR`. É a única lista de gestor que hoje
  entrega trabalho legítimo.
- **8.6, 8.7, 8.13, 8.17 e 8.14 estão vazias porque o funil nunca produziu o
  insumo** — não porque o filtro esteja errado. Não há no-show porque não houve
  reunião; não há calibração porque não houve veredito de closer real; há **um**
  `Sinal recebido` na conta inteira. Isso não é defeito para consertar, é o
  retrato de uma máquina que ainda não rodou. Vale saber para não sair "arrumando"
  filtro que está correto.

### O achado: DND e a tag `nao-perturbe` NÃO são a mesma proteção — e 40 registros discordam

**31 contatos têm DND ligado e não têm a tag `nao-perturbe`. Outros 9 têm a tag e
não têm DND.** Quarenta registros onde as duas proteções discordam, nos dois
sentidos.

E os 31 **são consequência direta de escrita minha**: em 27/09 eu liguei
`dnd = true` em 30 contatos para travar a rampa (`ESTADO-27-09.md` §1) e **não**
apliquei a tag. Os 31 são esses 30 mais o `Carlos Andrade`, que já estava em DND
desde 23/09. A lista 8.27 existe exatamente para pegar essa inconsistência, e vai
abrir com 31 linhas na terça por causa do que eu fiz.

**Por que isso é funcional e não cosmético**, e é a parte que muda o entendimento
do projeto: as duas proteções agem em camadas diferentes.

- **DND** é bloqueio de canal, imposto pela camada de mensagem. Impede o envio.
- **`nao-perturbe`** é o que a **lógica de workflow lê**. O W13 nó 3 é
  `Tags inclui nao-perturbe → FIM`; o W14 aplica a tag; as listas excluem por ela.

Então, para os 31: o DND impede a mensagem sair, mas **o workflow não para**.
Ele segue criando tarefa, mexendo em etapa, incrementando contador e escrevendo
`Prioridade` — porque o portão que ele consulta é a tag, e a tag não está lá.

Isso **explica o experimento** que o `AUDITORIA-27-09.md` registrou como
incógnita: o contato de teste recebeu `Prioridade` 5 e `atraso-1a-tentativa`
"com as duas proteções ligadas". Com esta leitura, a frase fica mais precisa —
o que estava ligado era o canal, não o portão.

E corrige, por consequência, a §2 do `ESTADO-27-09.md`, que diz "34 dos 39 estão
em DND ou `nao-perturbe` → o canal está bloqueado". O canal está; **a régua,
não**. Para 31 deles a máquina continua andando por dentro, em silêncio, gastando
tentativa da régua sem nunca falar com ninguém — que é o pior dos dois mundos,
porque queima a cadência sem produzir contato.

**Os 9 do outro lado** são o espelho: a tag está lá, então o workflow para, mas
**não há DND nenhum** — nem `dnd`, nem canal em `dndSettings`. Mensagem manual,
ou uma discagem pelo Call Center (que não lê tag), passa. Entre eles há três
registros que não são de teste: `francisca`, `o próximo cliente` e um `sem nome`.

### O que fazer, e o que não dá para fazer daqui

O conserto é reconciliar as duas proteções, e tem forma de script — o mesmo
padrão do `recalcula_prioridade.py`: onde `dnd` está ligado, aplicar
`nao-perturbe`; onde a tag está e o DND não, ligar o DND. **Escrever depende de
`[x]` novo no `APROVADO.md`** — a rotina não se autoriza, e nem vou propor que se
autorize.

O que dá para fazer antes disso é a decisão, que é do dono e é curta: **as duas
proteções sempre juntas?** Se sim, sai um script e um par de listas que devem
ficar vazias para sempre (é justamente o desenho que a 8.26/8.27 já tinha em
mente). Se não, então a §2 do `ESTADO` precisa dizer que travar o canal **não**
trava a régua, e a janela em `days: [2]` volta a ser a única alavanca de verdade
— porque é a única que para o motor, em vez de calar a boca dele.


## 8. O que os dumps publicados dizem — e o freio de capacidade que não freia (27/09 10:05)

Os 128 dumps de workflow do branch `claude/amazing-johnson-mclksg` (último commit
`875d8d7`, auditoria de 23/09) carregam `status` e `version`. Ler isso é offline,
barato, e testa a hipótese da §0 sem depender de tela.

### Duas coisas que a §0 supunha e que agora estão eliminadas

| suposição | o que o dump diz | efeito na §0 |
|---|---|---|
| a cadência estaria em rascunho | `Cadência 12x30`: **`status: published`, version 35** · `Cadência Inbound`: **`published`, version 21** | eliminada. Em 23/09 as duas já escutavam; os 38 foram promovidos em **24/09**, depois disso |
| faltariam nós (tag, dono, tarefa) | o dump da Inbound tem `add_contact_tag` com `fila-quente`/`fila-tel`/`fila-wa`/`toque`, um `assign_user` atrás do portão `Sem dono?`, e nós `task-notification` | eliminada. A máquina publicada contém tudo o que o documento promete |

O cabeçalho da `IMPLEMENTACAO-WORKFLOWS.md` ainda diz "W11 · Cadência 12x30 —
**rascunho, 0 inscritos**". Contra o dump de 23/09, esse cabeçalho está
**desatualizado** — vale corrigir na fonte quando alguém mexer nela.

**A §0 fica mais estreita e continua aberta.** Não é "não publicado" nem "nó
faltando". O que sobra: ou a inscrição não aconteceu na mudança de etapa em lote,
ou a execução morreu num portão que o dump não deixa rastrear (as ramificações
`if_else` guardam a continuação fora do `next`, então o grafo não se percorre de
fora). Quem distingue continua sendo **a contagem de contatos inscritos na tela da
`Cadência Inbound`** — segue sendo a pergunta nº 1, e eu não vou fingir que
respondi.

Vale registrar que o próprio projeto já documentou este modo de falha: o item 6 do
checklist de go-live (§3.6) diz *"Só então promover o estoque de `NOVO LEAD` para
`CONECTAR` — promover antes de publicar a 12x30 manda os leads para um evento que
ninguém escuta"*, citando o `APRENDIZADOS-CRM.md` de 21/09. Já aconteceu uma vez,
e por isso a ordem está escrita. Não afirmo que é a causa **desta** vez — os dumps
dizem que em 23/09 havia quem escutasse.

### ACHADO NOVO: o freio de capacidade está pendurado numa tag que ninguém aplica

Dentro da `Cadência Inbound` publicada, o portão **`TI1 · SDR lotado?`** testa uma
condição exata:

```
conditionType: contact_detail · conditionSubType: tags
conditionOperator: index-of-true · conditionValue: ["sdr-lotado"]
```

Se a tag estiver presente, o fluxo cai num laço de `Wait 1 Hours` e **não cria a
tarefa**. É o freio que segura a fila quando o SDR passa da capacidade.

**A tag `sdr-lotado` não está em nenhum dos 64 contatos da conta.** Nem no fixture
`ZZ TESTE ESTRUTURA`, que carrega as outras 20.

### E fechando a pergunta: ninguém escreve essa tag, e a notificação promete que alguém escreve

Varri os **43 dumps ativos** procurando `sdr-lotado`, separando quem **lê** (num
`if_else`) de quem **escreve** (num `add_contact_tag`):

| dump | lê | escreve |
|---|---|---|
| `Cadência Inbound` | sim | **não** |
| `Cadência 12x30` | sim | **não** |
| `Cadência 12x30 — parte 2` | sim | **não** |
| `Recuperação de No-show` | sim | **não** |
| `ZZ TESTE 12X30` | sim | **não** |
| `Monitor de Capacidade` | — | **não** — aparece só no texto da notificação |

**Cinco workflows leem a tag num portão. Nenhum a escreve.** Quatro deles são de
produção.

E o texto que o `Monitor de Capacidade` manda ao gestor, transcrito do dump:

> *"Capacidade do SDR: no máximo 100 ligações (toques) por dia. Com 50 ou mais
> tarefas vencidas, **o sistema segura sozinho** os toques novos da cadência (tag
> `sdr-lotado`) até as vencidas caírem abaixo de 50. Confira em Contatos → Smart
> Lists → 'Fila do Dia — Total' e zere as vencidas antes do fim do expediente."*

A mensagem afirma que **o sistema segura sozinho**. Não segura: nada aplica a tag.
O gestor lê que existe um freio automático, deixa de se preocupar com o teto, e o
freio não existe — está publicado, lido por quatro workflows, e sem atuador.

Pior: a conferência manual que a própria mensagem sugere aponta para a lista
**`Fila do Dia — Total`**, que a §7 mediu em **0 linhas**. Quem seguir a instrução
ao pé da letra vê uma lista vazia e conclui que está tudo bem.

**O que consertar, e são duas coisas independentes:**

1. **Decidir se o freio é automático ou manual.** Se automático, falta um
   `add_contact_tag sdr-lotado` em algum lugar que conte tarefa vencida — e isso é
   edição de workflow, que exige a API interna e não sai daqui. Se manual, o texto
   tem de dizer *"aplique a tag `sdr-lotado`"* em vez de *"o sistema segura
   sozinho"*, e a ação precisa entrar na rotina do gestor (§3.3), onde hoje não
   está.
2. **Corrigir o texto de qualquer jeito**, porque hoje ele é uma promessa falsa
   sobre uma proteção — é o tipo de frase que faz a operação confiar no que não
   há. Editar texto de notificação também é tela/API interna, então entra na lista
   do dono.

Isto é o mesmo padrão da §7 levado ao limite: a peça existe, está publicada, está
ligada a quatro workflows — e não recebe insumo. A diferença é que o custo aparece
**exatamente quando a operação der certo**: o freio falta na hora do volume, não
agora.

## 9. Varredura lê-vs-escreve em 28 tags, nos 36 dumps de produção (27/09 11:35)

Método: para cada tag do inventário, contar em quantos workflows ela aparece num
`if_else` (**lê**), num `add_contact_tag` (**escreve**) e num `remove_contact_tag`
(**apaga**). Portão que lê o que ninguém escreve é peça morta; tag que só entra e
nunca sai é lixo acumulando. Os 36 dumps de produção do branch
`claude/amazing-johnson-mclksg`, ignorando os `ZZ TESTE` e as pastas `_antes-*`.

| tag | lê | add | rem | leitura |
|---|---|---|---|---|
| `fila-wa` | 3 | **0** | 7 | **defeito** — ver abaixo, é o mais grave |
| `sdr-lotado` | 4 | **0** | 0 | defeito, já na §8 |
| `reengajamento-ativo` | 1 | **0** | 3 | **defeito** — ver abaixo |
| `pausado` | 5 | 0 | 1 | **correto por desenho** — ver abaixo |
| `telefone-invalido` | 4 | 4 | **0** | **defeito** — só entra |
| `limpar-tarefas` | 0 | 7 | **0** | **defeito** — só entra; é a causa da 8.5 com 18 linhas |
| `nao-perturbe` | 12 | 4 | **0** | correto por desenho (opt-out é definitivo) |
| `agendar-estagnado` | 0 | 1 | 0 | moot: o `AGENDAR Estagnado` foi despublicado em 23/09 (G-13) |
| `fila-quente` | 0 | 4 | 7 | simétrico, ok |
| `fila-tel` | 1 | 4 | 8 | simétrico, ok |

### O mais grave: `fila-wa` é apagada em 90 lugares e criada em nenhum

`fila-wa` aparece **mais de noventa vezes** nos dumps de produção. Conferi uma por
uma: **todas** são `remove_contact_tag` ou condição de `if_else`. As duas cadências
removem a tag uma vez por bloco de tentativa (10 vezes na Inbound, 13 na 12x30 —
o par "Remove Tag / Add Tag" de cada toque), e o que elas **adicionam** é sempre
`fila-tel`. Nunca `fila-wa`.

Consequência direta, e independente da §0: a lista **8.3 `Fila WhatsApp Hoje`
nunca pode ter uma linha**, porque o filtro dela é a tag. E o bloco de WhatsApp da
§3.1 — **14:00 às 17:30, metade do dia do SDR** — não tem fila por construção.

Isto **soma** com o que já se sabia (`Permissão WhatsApp` = `Não solicitado` em 38
de 38), mas é mais fundo: mesmo que todo mundo dê permissão amanhã, e mesmo que a
inscrição da §0 seja consertada, a tag continua não sendo aplicada e a lista
continua vazia. São dois motivos independentes, e só um deles estava catalogado.

O conserto é edição de workflow — precisa da API interna, não sai daqui. O que sai
daqui é a medida: o par simétrico existe para `fila-tel` nos mesmos nós, então o
desenho previa os dois e um ficou pelo caminho.

### `reengajamento-ativo`: três workflows apagam, nenhum cria — e o workflow que criaria não tem dump

A tag é lida pela `Cadência 12x30` e apagada por três (`Mestre de saída v2`,
`Nutrição — WhatsApp a cada 15 dias`, `Triagem da Nutrição`). Nenhum dump de
produção a adiciona.

E a explicação provável está na lista de arquivos: **não existe
`Reengajamento 90 dias.json` entre os 36 dumps ativos** — ele só aparece dentro de
`_antes-12x30-multicanal/`, que é backup. Duas leituras, e não consigo separar
daqui:

- o workflow **existe na conta** e nunca foi re-dumpado depois de 23/09; ou
- ele **não existe**, e a meta da §3.5 *"Nutrição: 90 dias, depois reativa
  sozinho"* não tem motor.

O dado da conta é compatível com as duas: a lista 8.14 tem **1 linha**, e é o
fixture. Nenhum lead real jamais entrou em reengajamento. **Um olhar na tela
(Automação → procurar `Reengajamento 90 dias`) decide**, e vale entrar na lista de
perguntas.

### `pausado`: parece morta e NÃO é — é manual de propósito

Cinco workflows leem `pausado` num portão e nenhum a escreve. Pela regra mecânica
seria peça morta, mas a §3.1 da `IMPLEMENTACAO-WORKFLOWS.md` diz explicitamente:

> *"lead pediu 'me liga mês que vem' (sem opt-out) → Aplicar a tag **`pausado`** à
> mão; retirar quando voltar."*

É manual por desenho, e está documentado. O único `remove` é no `Mestre de saída
v2`, que roda quando o lead deixa o funil — tirar a pausa ali é correto, não é a
máquina despausando alguém por conta própria. **Nada a consertar**, e registro
porque a varredura mecânica marcaria como defeito.

É exatamente a diferença que separa este caso do `sdr-lotado`: ali a notificação
**afirma** que o sistema aplica sozinho. Aqui o documento manda a pessoa aplicar.

### Duas tags que só entram

**`telefone-invalido`** — quatro workflows aplicam (`Cadência 12x30`, `Cadência
Inbound`, `Pós-ligação v2` e `v3`) e **nenhum remove**. Se o número for corrigido,
a tag fica para sempre: o lead segue na lista 8.18 e — isto é responsabilidade do
meu próprio código — a regra 8 da §9.2 no `recalcula_prioridade.py` o rebaixa para
`Prioridade` 1 **permanentemente**. Vale uma linha no docstring da ferramenta
avisando que a tag não tem volta automática.

**`limpar-tarefas`** — sete workflows aplicam, nenhum remove, e nenhum workflow a
lê (quem lê é a faxina em Python, fora do CRM). Isto **fecha o mecanismo** do
achado da §0: a lista 8.5 mostra 18 linhas porque a tag entra em todo lead que
passa pela máquina e nunca sai. Não é só a falta de `fila-*` nas exclusões; é
também que o lado positivo do filtro cresce para sempre.
