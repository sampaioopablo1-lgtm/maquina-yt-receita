# Auditoria de valor — 27/09/2026, véspera da abertura

Rodada sobre **os 38 contatos da etapa `CONECTAR`** e **as 56 definições de campo
personalizado** da subconta `1D53YTI9C7oIMBavcQxV`, lidos um a um pela API.
**73 achados.**

> **Correção de escopo (mesma noite).** A varredura ficou **restrita a
> `CONECTAR`**, e isso invalida parte do achado `campo-morto`: campo preenchido
> em contato de outra etapa aparece como morto. Confirmado num caso: a `Carla
> Sampaio` (`NOVO LEAD`, entrou em 25/09 por `lc-phone-api`) tem `Duração da
> ligação` = 40 e `Conexão real` = `Não` — dois dos campos que a lista abaixo
> declara mortos. Os números de `fora-da-picklist`, `campos-gemeos` e
> `telefone-improvavel` não são afetados, porque dependem do valor e não do
> escopo. A varredura do `vigia` roda **sem escopo** e vai estabelecer o número
> real de campos mortos na primeira rodada com rede.

Não é auditoria de estrutura — as cinco que já existem fazem isso. Esta pergunta
uma coisa só: *o valor gravado neste campo é um valor que este campo aceita?*

| tipo de achado | quantos |
|---|---|
| `campo-morto` | **45** |
| `fora-da-picklist` | **24** |
| `campos-gemeos` | 2 |
| `telefone-improvavel` | 2 |

---

## 1. `campo-morto` — 45 de 56 campos nunca foram preenchidos

O achado maior, e o que explica todos os outros. **Só 11 dos 56 campos têm
valor em algum dos 38 leads.** Entre os 45 vazios:

`Resultado da tentativa` · `Nota de qualificação` · `Canal que conectou` ·
`Prazo` · `Total de conexões` · `Toques na semana` · `Decisor` · `Budget` ·
`Tentativas telefone` · `Tentativas WhatsApp` · `Conexões telefone` ·
`Conexões WhatsApp` · `Data de retorno` · `Hora do retorno` · `Segmento` ·
`Usa CRM` · `Tem time comercial` · `Quem atende os leads` ·
`Motivo da desqualificação` · `Template usado` · `Data agendado` ·
`Data conectado` · `Data compareceu` · `Nº de no-shows` · `Empresa` · `Site` ·
`Instagram` · (e mais 18)

**O que isso significa, com a precisão que a correção de escopo obriga:** a
**régua de cadência** nunca executou um ciclo. `Resultado da tentativa` vazio em
38 de 38 é a prova — é o campo que dispara todo o roteamento do Pós-ligação.
Nenhuma ligação foi classificada pelo SDR, nenhuma régua avançou.

Mas **outros workflows estão executando**: a `Carla Sampaio` tem `Duração da
ligação` e `Conexão real` gravados, o que só o workflow de Qualidade da Conexão
faz. Então o certo é: o caminho de **ligação registrada pelo sistema** roda; o
caminho de **cadência classificada pelo SDR** nunca rodou.

Não é defeito de campo. É consequência de a cadência estar parada na janela:
campo e tag de entrada rodam fora do horário, o resto espera. Mas vira defeito
no instante em que a operação abrir e alguém confiar num relatório construído
sobre esses campos.

**Falso positivo esperado:** campos de etapas adiantadas (`Data do veredito do
closer`, `Reunião foi qualificada`) estão legitimamente vazios — ninguém chegou
lá. A varredura não sabe distinguir, e não deve: o relatório é para quem lê.

## 2. `fora-da-picklist` — 24 valores inválidos, todos no mesmo campo

> **Isto não é achado novo.** Está catalogado desde **21/09/2026** em
> `CONFERENCIA-CAMPOS.md` (Tabela H) e aberto no roadmap como **G-04**, com os
> mesmos quatro valores. A `IMPLEMENTACAO-WORKFLOWS.md` (§3.3) registra que a
> metade `Prazo`/`Urgência` **foi resolvida em 22/09 sem precisar de decisão**, e
> que só resta a metade das **opções de `Investimento mensal`**, que é decisão do
> dono. O que esta varredura acrescentou são as contagens de hoje e a deteção
> automática — o diagnóstico é de seis dias antes.

`Investimento mensal em anúncios` é `SINGLE_OPTIONS` com quatro opções:
`Até 1k` · `1k a 5k` · `5k a 10k` · `Acima de 10k`.

| valor gravado | leads | está na picklist? |
|---|---|---|
| `Não invisto nada ainda` | **15** | não |
| `Abaixo de 5k` | **6** | não |
| `Até R$ 1.000` | **3** | não |
| `Acima de 10k` | 3 | sim |

**24 de 27 valores preenchidos não existem na picklist do próprio campo.**
Qualquer `If/Else` de workflow ou filtro de lista que compare contra as opções
falha calado para 24 dos 27 leads — e nunca aparece em log nenhum.

*(Correção: numa leitura parcial anterior eu disse "19 de 22". A varredura
completa dá **24 de 27**.)*

## 3. `campos-gemeos` — dois pares, achados sozinhos

**`Necessidade` × `Dor principal`** — valores em comum: `Falta de novos
clientes`, `Quero aprender a gerar meus próprios leads para o WhatsApp`, `Quero
contratar alguém para gerar meus leads (Agência).` A mesma pergunta do
formulário cai em `Dor principal` para os leads dos formulários v1/v3 e em
`Necessidade` para os outros. **Lista ou workflow que filtre por um vê metade da
base.**

**`Urgência` × `Investimento mensal em anúncios`** — valores em comum:
`Abaixo de 5k`, `Acima de 10k`. `Urgência` é TEXT e está recebendo resposta de
**budget** em 4 leads (Francisco, Marcos Alves, Valéria, CM Construções) — e
esses mesmos 4 estão **sem** `Investimento mensal`. É deslocamento de uma
pergunta numa versão do formulário do Meta.

E o campo certo para o que está na `Urgência` existe e está vazio: **`Prazo`**,
`SINGLE_OPTIONS` com exatamente `Pra ontem` / `Espera 30 dias` / `Este ano` /
`Sem prazo` — as respostas que estão caindo em texto livre.

## 4. `telefone-improvavel` — 2 grupos de WhatsApp

`+120363226349138496` e `+120363294985523330`: 18 dígitos (E.164 permite 15) e
prefixo `120363`, de JID de grupo. Tratados em 27/09 com `dnd`, `nao-perturbe`,
`grupo-whatsapp-nao-e-lead` e oportunidade `abandoned` — nada excluído.

---

## Sobre as 100 tarefas para o SDR

> **A rotina do SDR já está especificada** em `IMPLEMENTACAO-WORKFLOWS.md` §3.1,
> hora a hora, com as 4 listas favoritas (`Fila Quente` → `Retornos` →
> `Fila Telefone Hoje` → `Fila WhatsApp Hoje`) e as regras de "Nunca (SDR)". E o
> §3.3 trata **100 tarefas como teto a vigiar, não meta**: o gestor olha
> `Estouro da Fila` às 11:00 e 15:00, e "positivo = mais de 100 tarefas hoje →
> segurar entrada ou remanejar SDR". A conta abaixo é sobre quando a fila
> **chega** a esse teto.

Hoje a etapa `CONECTAR` inteira tem **1 tarefa**, do contato de teste
`Teste Não Atende`, vencida desde 22/09. Os 38 leads reais têm **zero**.

Não é problema de filtro — não há tarefa para filtrar. A conta:

| objetivo | leads em cadência | entrada/dia | quando |
|---|---|---|---|
| 100 tarefas **abertas** na fila | ~100 (uma tarefa por lead) | 10/dia | **~10 dias** de campanha |
| 100 tarefas **por dia** | ~250 (12 tentativas / 30 dias = 0,4 por lead/dia) | ~8,3/dia | **~30 dias**, em regime |

Com a campanha reativada a 10 leads/dia, o regime dá **~120 tarefas/dia** — passa
dos 100. Mas um SDR entrega ~90 discagens/dia na janela 08:30–18:30, então o
ajuste é **quantas das 12 tentativas são discagem humana**: com 7 de 12, cai
para ~70/dia e cabe; com 9, dá 90 e fica no limite.

**O que trava hoje não é volume nem filtro: é que a cadência nunca criou
tarefa.** Enquanto `Resultado da tentativa` estiver vazio em 38 de 38, não
existe fila, não existe roteamento e não existe nota de qualificação para
ordenar nada.
