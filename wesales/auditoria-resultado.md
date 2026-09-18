# Etapa 1 — resultado da auditoria

Executada em 18/09/2026 via conector `GHL CRM` (MCP oficial da LeadConnector).
Somente leitura: **nada foi criado, alterado ou excluído.**

Subconta: **Pablo Santos's Account** — `1D53YTI9C7oIMBavcQxV`

## 0. A subconta

| Item | Valor |
|---|---|
| Nome | Pablo Santos's Account |
| ID | `1D53YTI9C7oIMBavcQxV` |
| Fuso | `America/Sao_Paulo` |
| Moeda | BRL |
| Criada em | 17/09/2026 23:57 |
| Modo SaaS | ativado, assinatura em `trialing` |
| Contato duplicado | bloqueado (identificadores: e-mail e telefone) |
| Oportunidade duplicada | bloqueada |

**A subconta tem menos de um dia de vida.** Isso muda o tom de toda a auditoria:
não há histórico para conflitar, e sim uma folha quase em branco.

Módulos habilitados que o projeto usa: `workflowsEnabled`, `formsEnabled`,
`opportunitiesEnabled`, `appointmentsEnabled`, `conversationsEnabled`,
`tagsEnabled`, `phoneCallEnabled`, `triggersEnabled`. Nada bloqueado.

Dois desligados, sem impacto aqui: `botServiceEnabled` e `htmlBuilderEnabled`.
**Atenção:** `botServiceEnabled: false` é o Conversation AI. O workflow de
qualificação por IA (seção 6 do `build-wesales.md`) depende dele no caminho A —
ou se habilita o módulo, ou usa o caminho B (corrente de nós).

## 1. Pipelines e etapas

Um pipeline, 14 etapas.

| # | Etapa | Cor | Prob. de ganho |
|---|---|---|---|
| 0 | ENTROU EM CONTATO | azul | 6,67% |
| 1 | RESPONDEU O PRIMEIRO CONTATO | azul | 13,33% |
| 2 | NÃO RESPONDEU | vermelho | 20% |
| 3 | CONVERSA EM ANDAMENTO | turquesa | 26,67% |
| 4 | EM FOLLOW UP | vermelho | 33,33% |
| 5 | COTAÇÃO REALIZADA | verde | 40% |
| 6 | DOCUMENTOS ENVIADOS | verde | 46,67% |
| 7 | PAGAMENTO FEITO | verde | 53,33% |
| 8 | NÃO FECHOU PÓS COTAÇÃO | vermelho | 60% |
| 9 | ATIVAR FOLLOW UP AUTOMATIZADO | roxo | 66,67% |
| 10 | Geladeira 30D | rosa | 73,33% |
| 11 | Geladeira 60D | rosa | 80% |
| 12 | Geladeira 90D | rosa | 86,67% |
| 13 | NÃO TEM INTERESSE | cinza | 93,33% |

`FUNIL DE VENDAS` — `0Fo2xbeayE4EP6yuSUtq`. Veio de um snapshot
(`originId` presente em todas as etapas).

### Conflito com o pipeline "Pré-vendas"

**Não conflita, mas encosta.** É um funil de venda com cotação, documentos e
pagamento — outro negócio, não pré-vendas. Há sobreposição conceitual em três
pontos: "NÃO RESPONDEU" ≈ cadência, "CONVERSA EM ANDAMENTO" ≈ Conectado, e as
três "Geladeira 30/60/90D" ≈ Nutrição.

**Recomendação: criar o "Pré-vendas" separado, não adaptar este.** Misturar os
dois faria o portão da cadência (que consulta a etapa) disparar em lead que
está em processo de venda.

### Defeito encontrado, de graça

As probabilidades de ganho estão numa **progressão automática de 6,67%** até o
fim, e não na realidade do funil. O resultado é que **"NÃO TEM INTERESSE" está
com 93,33% de probabilidade de ganho** e "NÃO FECHOU PÓS COTAÇÃO" com 60%. Todo
relatório de previsão desse funil está inflado. É conserto de um minuto na tela
e não tem nada a ver com o nosso projeto — mas você ia descobrir isso do jeito
ruim, olhando um forecast mentiroso.

## 2. Campos personalizados

**Nenhum.** Zero campos de contato, zero de oportunidade.

| Consequência | |
|---|---|
| Conflito com os campos da Etapa 2 | **Nenhum** |
| Risco de duplicidade | **Nenhum** |
| Nomes livres | Todos |

## 3. Tags

O conector **não expõe listagem de tags da subconta** — só `contacts_add-tags`
e `contacts_remove-tags`, que agem sobre um contato.

Como a subconta tem **0 contatos**, não há tag aplicada a inferir. Na prática:
lista provavelmente vazia. **Confirme na tela** (Configurações → Tags) antes de
eu criar as 11 — é o único item da auditoria que eu não consegui fechar sozinho.

## 4. Workflows

Não exposto pelo conector. Com a subconta de um dia e 0 contatos, a chance de
haver workflow ativo consumindo as tags `fila-*` é mínima, mas o snapshot que
trouxe o pipeline pode ter trazido automações junto.

**Confirme na tela** (Automação → Workflows). É o segundo item aberto.

## 5. Calendários

O conector só lê **eventos** de calendário, não a configuração. Sem contatos e
sem oportunidades, não há agendamento para inferir.

**Confirme na tela** (Calendários) — principalmente se já existe algum com
Sticky Contact ligado, que é o risco R-04.

## 6. Formulários

Não exposto pelo conector. `formsEnabled: true`. **Confirme na tela.**

## 7. Volume atual

| | Total |
|---|---|
| Contatos | 0 |
| Oportunidades (todos os status) | 0 |

## Conflitos e duplicidades — conclusão

**Praticamente nenhum.** A subconta é nova e vazia. As Etapas 2 e 3 podem rodar
sem risco de duplicar nada. O único cuidado é não reaproveitar o
`FUNIL DE VENDAS` para pré-vendas.

## O que o conector cria e o que não cria

Medido na lista real de ferramentas do conector (36 ferramentas):

| Operação | Ferramenta | Sai por API? |
|---|---|---|
| Criar tag | `contacts_add-tags` (nasce ao aplicar num contato) | **Sim** |
| Criar/atualizar contato | `contacts_create-contact`, `contacts_upsert-contact` | Sim |
| Mover oportunidade de etapa | `opportunities_update-opportunity` | Sim |
| Ler tarefas | `contacts_get-all-tasks` | Sim |
| Mandar mensagem | `conversations_send-a-new-message` | Sim |
| **Criar campo personalizado** | — | **Não** |
| Criar pipeline/etapas | — | Não |
| Criar workflow | — | Não |
| Criar calendário/formulário | — | Não |
| **Concluir tarefa** | — | **Não** |

Duas consequências diretas:

1. **Etapa 2 vira manual.** Os campos são criados na tela. A lista com tipo e
   opções, pronta para copiar, está em `campos-e-tags.md`.
2. **A rotina da Etapa 5 vira relatório.** Sem ferramenta de concluir tarefa,
   ela aponta o que está fora de lugar e você fecha na tela. O prompt já está
   preparado para os dois modos.

## Próximos passos, na ordem

1. Você confirma na tela: tags, workflows, calendários e formulários (itens 3 a 6)
2. Você confirma a lista de campos e tags (`campos-e-tags.md`), inclusive as
   opções do campo `Segmento`, que continuam faltando
3. ~~Eu crio as tags por API~~ — **feito em 18/09/2026** (`APROVADO.md`)
4. Você cria os campos na tela (a lista cresce com o roadmap; conte em `campos-e-tags.md`)
5. Você monta pipeline e workflows pelo `build-wesales.md`
