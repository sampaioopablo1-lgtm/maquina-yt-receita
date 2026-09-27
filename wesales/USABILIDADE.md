# Usabilidade por função — renomear e agrupar, sem criar nada

Pedido do dono em 27/09/2026: *"confesso que ainda acho meio completo e confuso.
Importante é para as funções… defina a tag, lista de hoje, lista para ligar,
defina melhor o nome, e simplesmente começa a tocar a fila do dia da cadência.
Não quero que recrie do zero os campos, parâmetros — revise, teste, se coloque no
lugar das funções."*

**Regra deste documento: zero campo novo, zero tag nova** (com uma exceção
condicional, na §3). Só renomear, agrupar e escolher o que fica visível.

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

**1. Dois leads abertos em `NOVO LEAD` não têm nome.** Um vem com o nome
literalmente vazio, o outro com `Sem Nome` (`+5521969613820` e
`+5511951285383`), os dois com `cad-inbound` e `novo-lead-estagnado`. Os 38 de
`CONECTAR` têm nome, então o mapeamento de nome do formulário funciona em geral —
estes dois entraram por um caminho que não trouxe o campo. É a mesma família do
G-04 (resposta de formulário que não casa com o campo de destino), e o efeito é
concreto: o SDR abre a ligação sem ter como chamar a pessoa. Vale conferir de
qual formulário vieram antes de reativar a campanha a 10 leads/dia, senão
entram assim aos dez por dia.

**2. A única oportunidade aberta em `REUNIÃO DE DIAGNÓSTICO` é o próprio dono**
(`Pablo Sampaio`, `+5521987429940`) — o teste do calendário. Não é lead. Enquanto
estiver lá, as contagens mensais de funil (listas 8.9–8.12) e o widget de
agendamentos do painel contam o dono como reunião realizada. Descartar com
status `lost` (nunca excluir, regra 1) limpa isso.

**3. `FORMALIZAR` está vazia e não existe um `won` nas 64 oportunidades.** Já
sabido, mas agora com o número fechado do pipeline inteiro: a máquina nunca
levou ninguém até o fim. Não é defeito de configuração — é a razão de a abertura
existir.

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

## 4. Quatro pastas de campo, em vez de uma de 53

Reagrupar os campos que já existem. Nenhum criado, nenhum apagado.

| pasta | o que vai dentro | quem vê |
|---|---|---|
| **`1 · SDR PREENCHE`** | `Resultado da tentativa`, `Data de retorno`, `Hora do retorno`, `Motivo da desqualificação` | SDR |
| **`2 · NÃO MEXER — a máquina escreve`** | `Prioridade`, `Tentativa nº`, `Entrada em`, `1ª tentativa em`, os dois `Checkpoint`, `Toques na semana`, todos os contadores de ligação/conexão, `Template usado`, `Nota de qualificação` | ninguém edita |
| **`3 · CLOSER PREENCHE`** | `Reunião foi qualificada`, `Motivo da desqualificação`, `Data do veredito do closer` | closer |
| **`4 · VEIO DO ANÚNCIO`** | `Urgência`, `Necessidade`, `Dor principal`, `Prazo`, `Investimento mensal`, `Investe em anúncios`, `Budget`, `Decisor`, `Tem time comercial`, `Clientes novos por mês`, `Quem atende os leads`, `Canal principal de venda`, `Usa CRM`, `Já teve agência?`, `Segmento`, `Site`, `Instagram`, `Empresa` | SDR lê antes de ligar |

O nome da pasta 2 é metade do valor: **`NÃO MEXER`** é a instrução que a §3.1
tenta dar por documento ("quem 'ajuda' a automação à mão quebra a contagem e o
roteamento sem ver erro nenhum") e que a tela pode dar sozinha.

Criar e reatribuir pasta de campo **não sai pelo conector `GHL CRM`** (ele só lê
campo personalizado) — é trabalho de tela.

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
