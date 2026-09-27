# Usabilidade por função — renomear e agrupar, sem criar nada

Pedido do dono em 27/09/2026: *"confesso que ainda acho meio completo e confuso.
Importante é para as funções… defina a tag, lista de hoje, lista para ligar,
defina melhor o nome, e simplesmente começa a tocar a fila do dia da cadência.
Não quero que recrie do zero os campos, parâmetros — revise, teste, se coloque no
lugar das funções."*

**Regra deste documento: zero campo novo, zero tag nova** (com uma exceção
condicional, na §3). Só renomear, agrupar e escolher o que fica visível.

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
| SDR | do login até a primeira discagem | ? | < 30 s, sem escolher nada |
| SDR | registrar o resultado de uma ligação | ? | < 15 s, um campo |
| closer | do aviso de agendamento até ver a nota e o BANT | ? | < 20 s, uma tela |
| gestor | saber se a fila estourou hoje | ? | < 10 s, um número |

Nenhum desses números foi medido. **Medir é o próximo passo real** — e quem mede
é quem tem a tela.

## 6. O que fica fora, de propósito

- **Não recriar campo, tag ou workflow.** A máquina está desenhada e testada; o
  problema é de apresentação.
- **Não apagar nada.** O `APROVADO.md` proíbe, e não é preciso: o que confunde
  fica escondido em pasta, não excluído.
- **Não mexer na IA de WhatsApp.** O dono usa outro mecanismo, e
  `botServiceEnabled` já é `false`.
