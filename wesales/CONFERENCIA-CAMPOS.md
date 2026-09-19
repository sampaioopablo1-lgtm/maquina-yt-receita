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
| Falta `Hora do retorno` (TEXT) | só `Data de retorno` (DATE) existe | o par `Data do retorno` (DATE) + `Hora do retorno` (TEXT) — S-01 | `DATE` no GHL descarta a hora (registrado em `APRENDIZADOS-CRM.md`). Sem o par, "retorno às 15h" vira só "retorno hoje": a tarefa `[RETORNO]` nasce sem hora de vencimento e a lista `Retornos` não ordena o dia |
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
| `Empresa` | TEXT | o campo **nativo** `Company Name` (`{{contact.company_name}}`) | O `build-wesales.md` usa o nativo em tudo: o campo 4 do formulário (seção 7.2), o corpo da tarefa da cadência e a coluna "Empresa" de **nove** listas inteligentes. Se o formulário passar a gravar no `Empresa` custom, o SDR abre a fila e vê empresa em branco em todas elas |
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
`Plataformas de anúncio` continua `SINGLE_OPTIONS`.

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

**Segue aberto, sem mudança:** Tabela A inteira (`Hora do retorno`,
`Plataformas de anúncio`) e a decisão sobre `Necessidade`/`Urgência` na
Tabela F — nenhum dos dois é ajuste de texto, os dois pedem ação manual ou
decisão de negócio que este arquivo não toma sozinho.
