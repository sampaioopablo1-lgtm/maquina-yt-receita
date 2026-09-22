# Conferência dos campos — tela contra especificação

Lido da subconta `1D53YTI9C7oIMBavcQxV` por `locations_get-custom-fields` em
18/09/2026, 22:2x UTC, depois de a Fase 2 do `GUIA-MONTAGEM.md` ser montada na
tela. Comparado linha por linha com `campos-e-tags.md`.

**Resultado geral (primeira leitura, 18/09 22:2x): 43 campos existem. Os 24 de controle (C-01 a C-24) estão
todos lá, com o tipo certo. Os 18 de qualificação (Q-01 a Q-18) também.** O que
sobra são divergências de nome, de opção e de tipo — e um campo que ficou pela
metade.

Por que isso importa mesmo com tudo "criado": os workflows da seção 2 em diante
do `build-wesales.md` comparam **valor de opção** em nós `If/Else` e escrevem em
campo **por nome**. Opção escrita diferente não casa no `If/Else`; nome diferente
não casa na merge field. A régua de nota (seção 6) pontua **por faixa**, então
faixa trocada muda a nota do lead.

## A — Corrigir na tela: aqui se perde função

| O quê | Na tela | Deveria ser | O que quebra |
|---|---|---|---|
| ~~Falta `Hora do retorno` (TEXT)~~ — **fechado em 21/09/2026 23:18** | o par completo existe: `Data de retorno` (DATE) + `Hora do retorno` (TEXT, placeholder `HH:MM`) | — | Era: `DATE` no GHL descarta a hora, então sem o par "retorno às 15h" virava só "retorno hoje". **Não crie este campo, ele já está na tela** (Tabela K). O que sobrou da L-01 é fiação de workflow e lista, não campo |
| `Plataformas de anúncio` | `SINGLE_OPTIONS` | `MULTIPLE_OPTIONS` (Q-07) | Lead que anuncia no Meta **e** no Google só registra um. O GHL não troca `dataType` de campo já criado: o caminho é criar um campo novo com o tipo certo e parar de usar este — **sem excluir** (regra 1 do briefing) |

## B — Nomes que divergem

O nome da tela é o que vale para merge field e para a ação "Update Contact Field"
do workflow. Onde o nome da tela é igual de bom, o documento se ajusta; onde ele
confunde, vale renomear na tela (renomear não perde dado).

| # | Na tela | No documento | Sugestão |
|---|---|---|---|
| Q-08 | `Já teve agência?` | `Já teve agência` | manter a tela, ajustar o documento — mas o `?` no nome é atrito em toda referência; renomear na tela é mais limpo |
| Q-18 | `Qualificação` | `Qualificação preenchida por` | renomear na tela: `Qualificação` sozinho colide com "Nota de qualificação" e com a etapa `Qualificado` na leitura de quem monta |
| S-01 | `Data de retorno` | `Data do retorno` | manter a tela, ajustar o documento (só uma preposição) |

## C — Valores de opção que divergem

| # | Campo | Na tela | No documento | Peso |
|---|---|---|---|---|
| C-02 | Resultado da tentativa | `Caixa Postal` | `Caixa postal` | só a maiúscula, mas o `If/Else` compara texto: ajustar o documento e usar sempre a grafia da tela |
| Q-04 | Clientes novos por mês | `10`, `11-30`, `31-100`, `+101` | `Até 10`, `11-30`, `31-100`, `100+` | mesma faixa, rótulo diferente — ajustar o documento |
| Q-06 | Investimento mensal em anúncios | `Até 1k`, `1k a 5k`, `5k a 10k`, `Acima de 10k` | `Até 1 mil`, `1-5 mil`, `5-15 mil`, `15 mil+` | **faixa diferente**: o documento tinha um degrau em 15 mil, a tela corta em 10 mil. Decisão do dono, porque a régua de nota pontua por faixa |
| Q-08 | Já teve agência | `Nunca teve` | `Nunca` | ajustar o documento |
| Q-10 | Tem time comercial | `Só dono`, `1-5`, `6-10`, `+10` | `Só o dono`, `1-2 pessoas`, `3-5`, `6+` | **faixa diferente**: a tela junta 1-5 numa faixa só. Decisão do dono, mesmo motivo do Q-06 |
| Q-15 | Decisor | `Sim` | `É o decisor` | ajustar o documento |
| Q-17 | Prazo | `Pra ontem`, `Espera 30 dias`, `Este ano`, `Sem prazo` | `Agora`, `Até 30 dias`, `1-3 meses`, `Sem prazo` | **faixa diferente** no terceiro degrau (`Este ano` é bem mais largo que `1-3 meses`). Decisão do dono |
| Q-18 | Qualificação | `SDR`, `IA Whatsapp`, `Vendedor` | `SDR`, `IA WhatsApp`, `Automático` | a tela trocou "Automático" por "Vendedor" — são coisas diferentes. Decisão do dono: o campo responde "quem preencheu" |

## D — Tipo diferente, sem perda

Registrado para o documento parar de pedir outra coisa.

| # | Campo | Na tela | No documento | Leitura |
|---|---|---|---|---|
| Q-01 | Segmento | `TEXT` | `SINGLE_OPTIONS` (opções pendentes desde a primeira rodada) | `TEXT` destrava sem esperar a lista de segmentos. Custo: não filtra bem em lista inteligente. Vira `SINGLE_OPTIONS` no dia em que a lista existir — campo novo, o antigo fica |
| Q-09 | Experiência com agência | `TEXT` | `LARGE_TEXT` | resposta longa cabe menos bem, mas funciona |
| Q-16 | Dor principal | `TEXT` | `LARGE_TEXT` | idem |
| Q-12 | Usa CRM | `SINGLE_OPTIONS` (Sim/Não) | `TEXT` | **a tela ficou melhor** que o documento: agora filtra em lista inteligente |

## E — Detalhe de organização

`Conexões WhatsApp` (C-12) está numa pasta diferente dos outros 42 campos
(`parentId` `vCqedGd185RiQKNlU870`, contra `gabsbU3jsUN7oIXCnYab` do resto). Não
afeta workflow nem lista — afeta só onde o campo aparece na ficha do contato.

## Onde mexer quando as decisões saírem

Cada nome e valor citado acima aparece em mais de um arquivo. Quem for ajustar:

| O que muda | Arquivos que citam |
|---|---|
| `Caixa postal` | `campos-e-tags.md`, `build-wesales.md`, `GUIA-MONTAGEM.md`, `script-de-ligacao.md`, `APRENDIZADOS-CRM.md` |
| `Já teve agência` | `campos-e-tags.md`, `build-wesales.md`, `script-de-ligacao.md` |
| `Qualificação preenchida por` | `campos-e-tags.md`, `build-wesales.md`, `GUIA-MONTAGEM.md`, `script-de-ligacao.md` |
| `Data do retorno` / `Hora do retorno` | `campos-e-tags.md`, `build-wesales.md`, `GUIA-MONTAGEM.md`, `ROADMAP-SALES-ENGAGEMENT.md`, `briefing-sdr.md`, `APRENDIZADOS-CRM.md` |
| `Plataformas de anúncio` | `campos-e-tags.md`, `build-wesales.md`, `GUIA-MONTAGEM.md`, `script-de-ligacao.md` |
| Faixas de Q-06, Q-10, Q-17 | `campos-e-tags.md`, `build-wesales.md` (régua de nota, seção 6), `GUIA-MONTAGEM.md` |

**Regra para não criar contradição nova:** a tela é a realidade; o documento se
ajusta a ela, não o contrário — exceto nos dois itens da Tabela A, que são perda
de função, e nas três faixas marcadas "decisão do dono", que mudam a nota do lead
e por isso não são ajuste de texto.

## F — Três campos novos que a tela criou sozinha (relido em 19/09, 00:2x UTC)

Entre 23:52 e 00:17 a subconta passou de 43 para 46 campos. Os três novos não
estão em `campos-e-tags.md` e têm cara de campo que o construtor de formulário
do GHL cria por conta própria quando alguém adiciona uma pergunta que não casa
com campo existente — dois deles nasceram numa pasta separada
(`zHU4yGXKHdxBHnGxUmai`), fora da pasta dos 43 primeiros.

| Campo novo | Tipo | Já existe quem faça esse papel | O problema |
|---|---|---|---|
| `Empresa` | TEXT | o campo **nativo** `Company Name` (`{{contact.company_name}}`) | Resolvido em 19/09 (fica o personalizado — o construtor de formulário não lista campo nativo). **Mas o aviso desta linha saiu pior do que previa:** medido em 21/09, os dois campos estão vazios em **todos** os 50 contatos, porque nada a montante coleta nome de empresa — ver Tabela J |
| `Necessidade` | TEXT | `Dor principal` (Q-16) | Dois campos para a mesma resposta. Quem preenche um deixa o outro vazio, e a nota de qualificação lê só um |
| `Urgência` | TEXT | `Prazo` (Q-17, `SINGLE_OPTIONS`) | Idem — e `Prazo` tem opções fechadas, que filtram em lista; `Urgência` é texto livre, que não filtra |

**O que fazer:** decidir de que lado fica cada informação **antes** de o
formulário entrar no ar, porque depois o dado já estará dividido entre dois
campos e ninguém vai saber qual está certo. O caminho mais barato é apontar as
perguntas do formulário para os campos que já existem (`Company Name` nativo,
`Dor principal`, `Prazo`) e deixar estes três parados — **sem excluir**, pela
regra 1 do briefing. É o mesmo raciocínio que o R-10 já aplicou ao reaproveitar
`Assigned User` em vez de criar `SDR responsável`: campo com dois donos diverge
na primeira edição feita direto na tela.

**Resolvido em 19/09, e a minha recomendação estava errada num ponto:** eu
sugeri apontar o formulário para o `Company Name` nativo. O construtor de
formulário do GHL **não oferece campo nativo** nesse seletor (confirmado na
tela: nem "Adição rápida" nem "Adicionar campos de objeto" listam
`Company Name`), então o personalizado `Empresa` é o único caminho —
`build-wesales.md` já grava nele no formulário e no modelo de nota. O que
faltava fechar era o outro lado: as **14 linhas de coluna** das listas
inteligentes diziam só "Empresa", e o seletor de colunas mostra a padrão e a
personalizada com nome parecido. Agora dizem `` `Empresa` `` e a seção 8 abre
avisando qual é qual.

`Necessidade` e `Urgência` continuam duplicando `Dor principal` e `Prazo` —
a decisão sobre esses dois não foi tomada.

**Continua aberto da Tabela A:** `Hora do retorno` ainda não existe, e
`Plataformas de anúncio` continua `SINGLE_OPTIONS`. *(Era verdade em 19/09;
`Hora do retorno` foi criado em 21/09 23:18 — Tabela K.)*

## G — Tabelas B, C e D aplicadas nos documentos (19/09/2026)

As correções que este arquivo listava como "ajustar o documento" (Tabelas B,
C e D) tinham ficado só catalogadas — `campos-e-tags.md` e a régua de nota
(`build-wesales.md`, seção 9.1) continuavam com os rótulos sugeridos da
primeira rodada quando esta execução leu `locations_get-custom-fields` de
novo, 46 campos, mesmos valores desta tabela. Aplicado agora: as duas
tabelas de `campos-e-tags.md` (Controle da cadência e Qualificação) e a
seção 9.1 do `build-wesales.md` usam os rótulos reais; `GUIA-MONTAGEM.md`,
`script-de-ligacao.md` e as duas referências a `Qualificação preenchida
por` na seção 6 do `build-wesales.md` também foram corrigidas. **Lição
generalizável:** um arquivo de auditoria como este documenta o achado, não
a correção — quem pegar o próximo item precisa conferir se o "ajustar o
documento" recomendado aqui já virou edição de verdade nos arquivos de
especificação, não só assumir que aparecer aqui significa resolvido.

O único remapeamento de pontuação de verdade (não só troca de rótulo) foi
`Tem time comercial`: a tela juntou dois degraus do plano original
(`1-2 pessoas`=6, `3-5`=8) num só (`1-5`), que ficou com 7. As outras duas
faixas marcadas "decisão do dono" nesta tabela (`Investimento mensal`,
`Prazo`) bateram degrau a degrau com o plano original — só o texto do
rótulo mudou, a pontuação de cada posição não.

**Segue aberto, sem mudança:** Tabela A inteira (`Hora do retorno` —
criado depois, em 21/09 23:18, Tabela K —, `Plataformas de anúncio`) e a decisão sobre `Necessidade`/`Urgência` na
Tabela F — nenhum dos dois é ajuste de texto, os dois pedem ação manual ou
decisão de negócio que este arquivo não toma sozinho.

## H — A Tabela F se resolveu sozinha, pelos dados: `Necessidade` e `Urgência` são onde o formulário do Meta grava (lido em 21/09/2026)

Lidos os 50 contatos por `contacts_get-contacts` (base inteira, `meta.total`
= 50) e cruzado campo a campo. O que a Tabela F chamava de "três campos que
a tela criou sozinha, duplicando `Dor principal` e `Prazo`" não é
duplicata parada — é o **destino real das respostas do Meta Lead Ads**:

| Campo | Tipo | Contatos com valor | O que chega nele |
|---|---|---|---|
| `Urgência` (`contact.urgncia`) | TEXT | **39** | A pergunta "quando você pretende resolver isso?": `Pra ontem`, `Posso esperar e ver oque acontece` — o mesmo conteúdo que `Prazo` (Q-17) deveria receber |
| `Necessidade` (`contact.necessidade`) | TEXT | **34** | A pergunta "o que você busca hoje?": `Quero aprender a gerar meus próprios leads para o WhatsApp`, `Já faço anúncios e quero melhorar meus resultados`, `Quero contratar alguém para gerar meus leads (Agência).`, `Falta de novos clientes`, `Vivemos por indicação` |
| `Dor principal` (Q-16) | TEXT | 5 | **As mesmas respostas de `Necessidade`**, só nos 5 leads mais novos (19-21/09: Carlos Andrade, Gerson, Ana Ruth, Ricardo, Andreia) — o mapeamento do formulário foi trocado para `Dor principal` em algum momento de 19/09; os 34 anteriores ficaram em `Necessidade` |
| `Investimento mensal em anúncios` (Q-06) | SINGLE_OPTIONS (`Até 1k`, `1k a 5k`, `5k a 10k`, `Acima de 10k`) | 32 | `Não invisto nada ainda`, `Até R$ 1.000`, `Abaixo de 5k`, `Acima de 10k` — **só o último existe na lista de opções** |
| `Prazo` (Q-17) | SINGLE_OPTIONS | 3 | Só os três leads qualificados à mão (Daniel, Genilson, Teste Atendeu) |

**O que isso quebra, e é pior do que a Tabela F previa:**

1. **A régua de nota (`build-wesales.md`, seção 9.1) lê `Prazo` e
   `Investimento mensal` — o Meta escreve em `Urgência` e escreve em
   `Investimento mensal` valores que não são opção do campo.** Um `If/Else`
   comparando `Investimento mensal = "Até 1k"` nunca casa com `Até R$ 1.000`;
   `= "1k a 5k"` nunca casa com `Abaixo de 5k`; `Não invisto nada ainda` não
   tem degrau nenhum. Para todo lead vindo do Meta (37 dos 50), o Bloco B da
   nota sai zerado em silêncio — a mesma classe de bug que a Tabela C/G já
   corrigiu no *documento*, agora na *origem do dado*. Corrigir o rótulo no
   documento não resolve: o valor gravado é que está fora da lista.
2. **O formulário do Meta não é um só.** Em 4 contatos (`cm construções`,
   `valéria`, `francisco`, `marcos alves`) a resposta de investimento
   (`Acima de 10k`/`Abaixo de 5k`) caiu em `Urgência`, e `Investimento
   mensal` ficou vazio — pelo menos um dos formulários de anúncio mapeia as
   perguntas em ordem diferente. Também há um contato `<test lead: dummy
   data for ...>` (teste do próprio Meta) com placeholders nos três campos.
3. `Prazo` e `Dor principal` — os campos que o script de ligação
   (`script-de-ligacao.md`) manda o SDR preencher — chegam **vazios** para o
   SDR mesmo quando o lead já respondeu exatamente isso no anúncio. O SDR
   pergunta de novo o que o lead já disse.

**Quantos formulários existem, medido em 21/09/2026 — muda o custo da Opção
A:** o achado 2 acima ("o formulário do Meta não é um só") tem número. Cada
contato traz `attributions[].mediumId`, que é o **id do formulário de Lead
Ads**. Contando a base inteira, são **oito formulários distintos** alimentando
esta subconta:

| `mediumId` (formulário) | Atribuições | Observação |
|---|---|---|
| `2412763482587375` | 42 | **`formName` real, lido por API em 22/09: `O PROXIMO CLIENTE FORMS v1`** (a descrição anterior, "o formulário 'Conversar no WhatsApp' dos 15 anúncios de nicho", era inferida do anúncio, não o nome do formulário — é por este nome que ele aparece no Gerenciador de Anúncios) |
| `1026163897118958` | 16 | |
| `28266780626312413` | 14 | O formulário WhatsApp do conjunto INTERESSE |
| `1751104652676702` | 2 | |
| `1065515179587826` · `1471351778171903` · `1606774301099773` · `1054520230548260` | 1 cada | Quatro formulários com um lead cada — provavelmente anúncios antigos ou testes |

(`utmSessionSource`: `Paid Social` 78, `Social media` 6 · `medium`:
`facebook` 78, `instagram` 6.)

Isso explica o achado 2 sem adivinhação — formulários diferentes, ordens de
pergunta diferentes — e cobra o preço da **Opção A**: "apontar as perguntas
do Meta para `Prazo`/`Dor principal`" é trabalho **oito vezes**, na tela do
Gerenciador de Anúncios, um formulário por vez, e todo formulário novo
criado depois nasce errado até alguém lembrar. A **Opção B** se aplica numa
só vez, no CRM, e cobre os oito de imediato.

**O que vale para A e para B, e nenhuma das duas dizia:** a régua tem de ler
**os dois campos**, `Necessidade` **e** `Dor principal`, combinados em OU.
Hoje 34 leads têm a resposta em `Necessidade` e 5 em `Dor principal` (o
mapeamento trocou no meio) — qualquer régua que leia só um dos dois está
errada para uma parte da base, e continuará errada durante a transição,
qualquer que seja a opção escolhida. O mesmo vale para `Urgência`/`Prazo`.

**O que fazer (decisão do dono, porque muda a nota do lead e o formulário
do anúncio — nada aqui sai por API neste conector):**

- **Opção A — a tela vira a fonte:** apontar as perguntas do Meta Lead Ads
  para `Prazo` e `Dor principal` (o mais novo já faz isso para `Dor
  principal`), e trocar as opções de `Investimento mensal em anúncios` para
  os quatro textos **exatos** que o Meta manda (`Não invisto nada ainda`,
  `Até R$ 1.000`, `Abaixo de 5k`, `Acima de 10k`) — a régua 9.1 se ajusta a
  esses quatro degraus (proposta de pontos abaixo). `Urgência`/`Necessidade`
  ficam paradas, sem excluir (regra 1). Os 34+39 valores antigos ficam onde
  estão; para a nota dos leads antigos, uma ação em massa "copiar
  `Necessidade` → `Dor principal`" só sai por workflow com `Update Contact
  Field` lendo o outro campo (confirmar na tela se o seletor de valor
  dinâmico oferece campo `TEXT` — `APRENDIZADOS-CRM.md`, entrada
  `{{right_now}}`, diz que a expansão recente cobre Numeric/Select/Monetary).
- **Opção B — o documento vira a fonte:** a régua 9.1 passa a ler
  `Urgência` e `Necessidade` (texto livre, comparando `Contains`), e Q-06
  ganha as opções do Meta. Mais barato hoje, mas texto livre não filtra em
  lista inteligente e qualquer mudança de copy no anúncio quebra a régua sem
  aviso.

Proposta de degraus para `Investimento mensal` se o dono for pela Opção A
(mantém o espírito 12/10/6/2 da 9.1): `Acima de 10k` = 12 · `Abaixo de 5k`
= 6 · `Até R$ 1.000` = 3 · `Não invisto nada ainda` = 1. `Espera 30
dias`/`Este ano` de `Prazo` não têm equivalente no Meta (`Pra ontem` e
`Posso esperar e ver oque acontece` são os dois únicos valores vistos) —
mapear `Posso esperar...` = `Sem prazo` (2 pontos) ou criar essa opção em
`Prazo` com o texto exato.

**Continua aberto da Tabela A:** `Hora do retorno` e `Plataformas de
anúncio`, sem mudança. *(`Hora do retorno` foi criado horas depois desta
leitura, em 21/09 23:18 — Tabela K.)*

---

## I — Os dois nós silenciosos da Tabela H têm causa (21/09/2026, mesma leitura de dados)

O achado 3 da Tabela H listou três rastros ausentes sem explicá-los. Dois
ficam resolvidos pela leitura dos **contadores vizinhos** do mesmo contato,
sem abrir a tela:

| Sintoma | O que o dado mostra | Causa |
|---|---|---|
| `Total de conexões` vazio, Pós-ligação com 24 execuções | "teste atendeu": `Total de ligações` 24 · `Tentativas telefone` 24 · `Conexões telefone` **8** · `Total de conexões` **vazio** | O ramo `Atendeu` rodou 8 vezes e o par vizinho fecha dos dois lados → o Math funciona e o ramo é alcançado. **Falta o nó 2 do ramo `Atendeu` na tela** (a especificação o pede) |
| `Nota de qualificação` vazia nos 3 de `NEGOCIAR` | Os 3 têm `Investimento mensal`, `Decisor`, `Budget` e `Prazo` preenchidos, e `Prioridade` = 5 (nó **5**, posterior ao Math) | Entradas presentes + nó posterior escrito = **o fluxo passou pelo nó 4 e não escreveu**. Math com campo não selecionado, mesmo defeito do assistente de IA já registrado |

O terceiro (leads novos chegando com `limpar-tarefas`) foi resolvido em
`build-wesales.md`, seção 3: o portão do nó 1 do Mestre de saída não
reconhecia chegada em `NOVO LEAD`.

Os dois retoques estão na tabela do `GUIA-MONTAGEM.md`, na faixa "dá para
fazer hoje". O método de diagnóstico ficou em `APRENDIZADOS-CRM.md`
("Diagnóstico por contador vizinho").

---

## J — A coluna `Empresa` das listas está vazia para 100% da base, e o debate "nativo vs. personalizado" era indiferente (21/09/2026)

A Tabela F tratou `Empresa` como uma escolha entre o campo **nativo**
(`{{contact.company_name}}`) e o **personalizado** (`contact.empresa`), com
o aviso: "se o formulário passar a gravar no personalizado, o SDR abre a
fila e vê empresa em branco". A decisão foi tomada em 19/09 (personalizado,
porque o construtor de formulário não lista campo nativo) e as colunas das
listas foram ajustadas.

Medido agora, nos 50 contatos:

| Campo | Contatos preenchidos |
|---|---|
| `companyName` (nativo) | **0** |
| `Empresa` (personalizado) | **0** |

Nenhum dos dois tem dado, porque **nada a montante coleta o nome da
empresa**: os formulários do Meta Lead Ads não perguntam isso, e o
formulário `Qualificação SDR` (seção 7.2), que perguntaria, só roda quando o
SDR agenda a reunião — depois das ligações, não antes. O debate era entre
dois campos igualmente vazios.

**O que isso custa, e por que a hora de resolver é agora:** `Empresa` é
coluna em **20 lugares** do `build-wesales.md`, quase todos listas
inteligentes de fila. O SDR abriria a fila do dia e veria uma coluna em
branco em todas elas. As listas ainda **não foram montadas** (Fase 6 do
`GUIA-MONTAGEM.md` segue aberta) — então isto se conserta trocando a coluna
antes de existir, não depois de montar 20 listas.

**Recomendação (decisão do dono, porque é o que ele vê na fila):** trocar
`Empresa` por uma coluna que tenha dado hoje e ajude na ligação:

| Coluna candidata | Contatos com valor | Por que serve |
|---|---|---|
| `Necessidade` + `Dor principal` | 34 + 5 = **39** | A resposta do lead, nas palavras dele, sobre o que procura — é a primeira frase do script |
| `Investimento mensal em anúncios` | **32** | Qualifica antes de discar (com a ressalva do G-04: os valores gravados não são as opções do campo) |
| `Urgência` + `Prazo` | 39 + 3 = **42** | Quem tem pressa aparece primeiro |

Manter `Empresa` também é legítimo **se** o dono acrescentar a pergunta aos
formulários do anúncio — mas são oito formulários (Tabela H) e cada pergunta
a mais derruba conversão de Lead Ads. Não recomendo.

---

## K — Os 5 campos que a tela criou em 21/09 nunca chegaram a este arquivo, e a Tabela A ficou pedindo um campo que já existe (22/09/2026)

Este arquivo existe para reconciliar tela e especificação, e estava **dois
dias atrasado exatamente no único avanço manual que houve.** Lido por API em
22/09/2026, com `locationId` explícito:

| Campo | `id` | `fieldKey` real | Tipo | Placeholder | Criado em | Item |
|---|---|---|---|---|---|---|
| `Toques na semana` | `c1xuCuLyJheHOQoJ3grH` | `contact.toques_na_semana` | NUMERICAL | — | 21/09 23:15:43 | C-26 / F-04 |
| `Hora da conexão` | `5hU72B0HuoMApZvO1Qk7` | `contact.hora_da_conexo` | TEXT | `HH` | 21/09 23:17:11 | C-25 / F-02 |
| `Hora do retorno` | `IHXNFnguTPyNj5Q59ea2` | `contact.hora_do_retorno` | TEXT | `HH:MM` | 21/09 23:18:32 | **metade `TEXT` de S-01** |
| `Checkpoint — Tentativa nº` | `BRcN6IGXtDr0u52QtfiF` | `contact.checkpoint__tentativa_n` | NUMERICAL | — | 21/09 23:19:54 | C-27 / F-05 peça 3 |
| `Checkpoint — Data de retorno` | `el7xNMvPE8ZiyfysRff9` | `contact.checkpoint__data_de_retorno` | DATE | — | 21/09 23:33:28 | C-28 / F-05 peça 6 |

Total na subconta: **51 campos** (eram 46). Todos os cinco conferem com a
especificação em nome, tipo e placeholder — inclusive as escolhas finas de
`TEXT` onde a hora importa, que é a razão de S-01 ser um par.

**A linha da Tabela A sobre `Hora do retorno` está fechada desde 21/09
23:18.** Ficou aberta aqui por mais um dia, e isso não é erro de texto: um
arquivo que lista pendências manuais é lido *na tela*, com a tela aberta.
Pedir a criação de um campo que já existe convida exatamente o duplicado que
a regra 3 do briefing manda evitar — e pior, esconde o que de fato
sobrou. Com o campo criado, o que resta da L-01 **não é mais criar campo**, é
fiação:

| O que sobrou da L-01 | Onde |
|---|---|
| A tarefa `[RETORNO]` usar `{{contact.hora_do_retorno}}` como hora de vencimento | `build-wesales.md` seção 4, ramo `Pediu retorno` |
| A lista `Retornos` ordenar o dia por essa hora | `build-wesales.md` seção 6 |
| O monitor de retorno vencido ler `{{contact.checkpoint__data_de_retorno}}` no `Wait → Dynamic` | `build-wesales.md` seção 2.24 |

**Da Tabela A, segue aberto só `Plataformas de anúncio`** (`SINGLE_OPTIONS`
onde a função pede `MULTIPLE_OPTIONS`) — e essa não se resolve criando o que
falta, e sim criando um campo novo com o tipo certo e parando de usar o
antigo, sem excluir.

**A lição, que vale além destes cinco:** o dono criou os campos às 23:15 e a
rodada seguinte registrou a novidade em `APRENDIZADOS-CRM.md` (onde ela
rendeu o achado do travessão no `fieldKey`) sem voltar aqui. Achado anotado
no lugar de quem investiga, não no lugar de quem executa. **Toda leva de
campo novo na tela precisa fechar a linha correspondente da Tabela A no
mesmo commit** — a auditoria de merge field órfão pega chave errada, não pega
pendência que deixou de ser pendência.

---

## L — Dois campos nativos do contato que o Meta não preenche: `country` e `timezone` (22/09/2026)

Observado ao ler o lead mais recente por API (`Carlos Andrade`, entrada do Meta
Lead Ads em 21/09). Não é item de roadmap, é registro para não ser investigado
duas vezes:

| Campo nativo | Valor real | Consequência |
|---|---|---|
| `country` | **`US`** | Lead brasileiro, telefone `+55…`. O formulário do Meta não envia país e o GHL assume `US`. **Vale conferir**, quando o R-13 (Number Validation, seção 2.16) for montado, se a validação de telefone usa o país do contato — se usar, um `US` com número `+55` pode reprovar número válido. Não testado, e não dá para testar por API: fica como conferência acoplada ao R-13, não como afirmação |
| `timezone` | **`null`** | **Já neutralizado pela especificação, por acaso feliz:** a decisão D-02 (`briefing-sdr.md`) e a tabela da seção 2.4 do `build-wesales.md` mandam usar **fuso da subconta**, com a justificativa explícita "não use fuso do contato: o SDR trabalha no fuso dele". Como nenhum nó lê fuso do contato, o `null` não quebra nada. Se algum workflow futuro escolher "fuso do contato" num `Wait` ou numa janela de envio, vai cair em fallback silencioso — é o motivo de registrar aqui |

Os dois valem para os **10 leads reais** do Meta; os 40 do backfill não foram
conferidos campo a campo neste ponto.

---

## M — O texto real das perguntas do formulário do Meta, e por que ele decide o G-04 (22/09/2026)

O contato de teste que o próprio Meta injeta (`eNqNOQI7FT2CBwYAHGrN`,
`test@meta.com`, `dateAdded` 19/09 00:42) guarda o que faltava para o G-04 ser
decidido sem abrir o Gerenciador de Anúncios: **os placeholders dele são o
texto literal de cada pergunta**, e cada um está gravado no campo que aquela
pergunta alimenta. Lido por API:

| Pergunta, como está escrita no formulário | Cai em | O que a régua lê |
|---|---|---|
| `Como podemos chamá-lo?` | `firstName` (nativo) | — |
| `quando_você_pretende_resolver_isso?` | `Urgência` (C-…, `2LnUD4KYSGkIBwiUdzl3`) | **`Prazo`** (Q-… ) |
| `o_que_você_busca_hoje?` | `Necessidade` (`OJQEsl5dV37pfVY2sIaB`) | **`Dor principal`** |
| `quanto_você_investe_hoje_por_mês_para_atrair_clientes?` | `Investimento mensal em anúncios` (`bQithNwReQIBGlZBaNlI`) | o mesmo campo ✔ (o problema aqui é o **valor**, fora da lista de opções — achado original do G-04) |

**Isto é evidência a favor da Opção B, não só argumento.** As duas primeiras
perguntas são, pelo texto, exatamente `Prazo` e `Dor principal` — os campos que
a régua de nota lê e que o script manda o SDR preencher. Elas não caem lá por
acidente de configuração de um formulário: caem em `Urgência`/`Necessidade`
porque quem montou os formulários usou os próprios rótulos, e são **oito
formulários** (tabela H). Corrigir a origem é oito vezes o mesmo trabalho, com
todo formulário futuro nascendo errado; fazer a régua ler onde o dado já cai
resolve os oito de uma vez e é imune ao nono.

**Método, para quem quiser nomear os outros sete formulários sem abrir o
Gerenciador:** `attributionSource.formName` e `attributionSource.formId` vêm em
**todo** contato (`contacts_get-contact`). Basta um contato por `mediumId` da
tabela H para preencher a coluna de nomes inteira — dois campos que o projeto
lia como `mediumId` anônimo e que na verdade trazem o nome do formulário de
graça.

**Ressalva de amostra:** o texto das perguntas acima é do formulário
`2412763482587375` (42 atribuições, o maior). Os outros sete podem ter perguntas
e ordens diferentes — é exatamente o achado 2 desta seção ("o formulário do Meta
não é um só"), e o motivo de a Opção A custar oito vezes.
