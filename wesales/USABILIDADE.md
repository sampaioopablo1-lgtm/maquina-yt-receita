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

## 3. A fila do dia e o Power Dialer

**O que eu não sei, e não vou fingir que sei:** não alcanço a tela do Power
Dialer, então não sei se ele recebe **lista inteligente** ou exige **tag**. Os
dois desenhos, para quem estiver na tela escolher:

**Se aceita lista inteligente** (o esperado): a entrada é `3 · FILA DO DIA`,
filtrando `Prioridade` > 0 e ordenando desc. **Nada a criar** — o
`recalcula_prioridade.py` já mantém a `Prioridade` correta, e o 0 já tira da fila
quem está em DND, `pausado` ou `nao-perturbe`.

**Se exige tag:** uma tag só, **`fila-do-dia`**, mantida pelo mesmo runner —
`Prioridade` >= 3 põe, o resto tira. Idempotente, uma escrita por lead que
mudou. É a única coisa neste documento que cria algo, é condicional, e precisa de
linha `[x]` no `APROVADO.md`.

**O que NÃO fazer:** tag diária por lead sem o campo numérico atrás. Em 300 leads
são ~600 escritas/dia, e todo lead cuja remoção falha fica com a tag de ontem —
o SDR liga para quem não devia e para de confiar na lista. Esse apodrecimento já
tem nome no projeto (`rotina-limpar-tarefas.md`).

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
