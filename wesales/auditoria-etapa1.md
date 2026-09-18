# Etapa 1 — Auditoria da subconta (somente leitura)

Estado: **bloqueada por acesso**. O plano, as ferramentas e a tabela de
resultado estão prontos; falta a conexão.

## 1. Como conectar (caminho certo, confirmado na documentação)

O endpoint multi-conta da HighLevel para o Claude é:

```
https://services.leadconnectorhq.com/mcp/anthropic/v2
```

Ele autentica por **OAuth**, funciona no Claude.ai, no **Claude Code** e no
Claude Cowork, e expõe **625 operações em 40 domínios**, filtradas pelas
permissões que você autorizar.

### Os 4 passos

1. **claude.ai → Configurações → Conectores → Adicionar conector personalizado**
2. URL do servidor: `https://services.leadconnectorhq.com/mcp/anthropic/v2`
3. Clicar em conectar. Cai na tela de autorização do LeadConnector
   (`chooselocation`) — ali você **escolhe quais subcontas** a conexão pode
   acessar. Pode marcar mais de uma.
4. Abrir uma **conversa nova** do Claude Code neste repositório e pedir a
   Etapa 1.

### O detalhe que faz toda a diferença

**O fluxo começa no Claude, não no marketplace.** Instalar o app `lc-mcp -
Anthropic` pela página do marketplace autoriza o app na subconta, mas não cria
conector nenhum do lado do Claude — por isso a sessão continua sem ferramenta
alguma. É o "Adicionar conector personalizado" que dispara o OAuth e é ele que
leva à mesma tela de escolher subconta.

### Não precisa de token

O Private Integration Token (`pit-`) e o Location ID eram o caminho antigo. No
endpoint `/anthropic/v2` o `locationId` é opcional: cada requisição é escopada
a uma subconta, autorizada contra a instalação e executada com tokens de vida
curta. Na conversa, você troca de subconta só **dizendo o nome dela**.

Fica como plano B: subconta → Settings → Private Integrations → Create New
Integration, escopos, copiar o token (começa com `pit-`; chave v1 não funciona
e é a causa nº 1 de erro 401).

**Sem integração nenhuma:** me manda print ou export das 6 listas e eu preencho
a auditoria na mão. Para as Etapas 4 e 5 o resultado é idêntico.

## 2. O que esperar das ferramentas

Nomes já confirmados na documentação do servidor, no padrão `dominio_acao`:

| Domínio | Ferramentas |
|---|---|
| Contatos | `contacts_get-contacts`, `contacts_get-contact`, `contacts_create-contact`, `contacts_update-contact`, `contacts_upsert-contact` |
| Tags | `contacts_add-tags`, `contacts_remove-tags` |
| Tarefas | `contacts_get-all-tasks` |
| Conversas | `conversations_search-conversation`, `conversations_get-messages`, `conversations_send-a-new-message` |
| Oportunidades | `opportunities_search-opportunity`, `opportunities_get-opportunity`, `opportunities_update-opportunity` |
| Calendários | `calendars_get-calendar-events`, `calendars_get-appointment-notes` |
| Subconta | `locations_get-location`, `locations_get-custom-fields` |

Essa lista é a que os guias públicos mostram e é **pequena perto das 625
operações** que o endpoint anuncia. Ou seja: criar campo personalizado, ler
formulário e ler workflow — que eu tinha dado como provavelmente ausentes —
têm boa chance de estar cobertos. **Não vou chutar para nenhum dos lados.** A
primeira coisa que faço ao conectar é listar as ferramentas reais e refazer
esta seção e a tabela da seção 3 com o que existe de fato.

## 3. Cobertura da auditoria e das criações

A tabela abaixo é o **pior caso**: o que dá para garantir com a lista pequena
de ferramentas confirmadas. Com 625 operações no endpoint, a expectativa é que
várias linhas melhorem — mas eu só mudo esta tabela depois de medir.

| # | Item | Pelo MCP oficial | Alternativa |
|---|---|---|---|
| 1 | Pipelines e etapas | Via `opportunities_search-opportunity` (traz pipeline e stage); pipeline vazio pode não aparecer | `HIGHLEVEL_GET_PIPELINES` (Composio) lista direto |
| 2 | Campos personalizados | `locations_get-custom-fields` | — |
| 3 | Tags existentes | Não há listagem de tags da subconta na lista publicada | `HIGHLEVEL_LIST_TAGS` (Composio) |
| 4 | **Workflows** | Não aparece | Manual: Automação → Workflows |
| 5 | Calendários | `calendars_get-calendar-events` traz eventos, não a configuração do calendário | `HIGHLEVEL_GET_CALENDARS` (Composio) traz a configuração |
| 6 | **Formulários** | Não aparece | Manual: Sites → Formulários |
| 7 | Criar campos (Etapa 2) | Provavelmente não | Composio (`HIGHLEVEL_LOCATIONS_CREATE_CUSTOM_FIELD`) ou manual |
| 8 | Criar tags (Etapa 3) | Sim, aplicando a um contato de teste | Composio (`HIGHLEVEL_CREATE_TAG`) cria direto |
| 9 | Pipeline, workflows, calendário, formulário, listas | Não | Manual — é o `build-wesales.md` |

Ou seja: os dois caminhos se completam. O oficial é melhor para operar no dia
a dia (ler contatos, mexer em oportunidade, mandar mensagem, ler tarefa); o da
Composio cobre a configuração da subconta, que é o que as Etapas 1 a 3 pedem.
Vale ter os dois.

### A rota alternativa, se precisar dela

Toolkit **HighLevel via Composio**, mesma API v2, com auth config próprio em
[Set up highlevel](https://dashboard.composio.dev/~/org/connect/apps/highlevel?open=true).
Ferramentas medidas por mim: `HIGHLEVEL_GET_PIPELINES`,
`HIGHLEVEL_GET_CUSTOM_FIELDS`, `HIGHLEVEL_LIST_TAGS`, `HIGHLEVEL_CREATE_TAG`,
`HIGHLEVEL_GET_CALENDARS`, `HIGHLEVEL_SEARCH_LOCATIONS`,
`HIGHLEVEL_LOCATIONS_CREATE_CUSTOM_FIELD`.

### Fontes

- [LeadConnector MCP Server — HighLevel API](https://marketplace.gohighlevel.com/docs/other/mcp/)
- [Guide on How to Setup and Use the HighLevel MCP Server](https://help.gohighlevel.com/support/solutions/articles/155000005741-how-to-setup-and-use-the-highlevel-mcp-server)
- [MCP Server: Connect AI Agents to Your Account — LeadConnector](https://help.leadconnectorhq.com/support/solutions/articles/155000008185-mcp-server-connect-ai-agents-to-your-account)
- [HighLevel MCP Multi-Account Support for Claude](https://help.gohighlevel.com/support/solutions/articles/155000008360-highlevel-mcp-multi-account-support-for-claude)
- [Private Integrations Token](https://marketplace.gohighlevel.com/docs/Authorization/PrivateIntegrationsToken/)

## 4. Tabela a preencher (Etapa 1)

Formato em que vou te devolver, assim que houver acesso ou dados.

### 4.1 Pipelines e etapas
| Pipeline | ID | Etapas (ordem) | Conflito com "Pré-vendas"? |
|---|---|---|---|

### 4.2 Campos personalizados
| Nome | Objeto | Tipo | fieldKey | Parecido com campo novo? | Ação sugerida |
|---|---|---|---|---|---|

### 4.3 Tags
| Tag existente | Parecida com | Ação sugerida (reaproveitar / criar nova) |
|---|---|---|

### 4.4 Workflows
| Workflow | Status | Gatilho | Conflita com qual dos 6 novos? |
|---|---|---|---|

### 4.5 Calendários
| Calendário | Tipo | Duração | Sticky Contact | Formulário anexado | Serve como calendário do closer? |
|---|---|---|---|---|---|

### 4.6 Formulários
| Formulário | Campos | Usado em | Serve como formulário de qualificação? |
|---|---|---|---|

### 4.7 Conflitos e duplicidades
Fechamento obrigatório antes de qualquer criação: lista de tudo que já existe
com nome parecido, com a pergunta "reaproveito ou crio novo?" para cada item.

## 5. Riscos que a auditoria precisa confirmar

| # | Risco | Como checo |
|---|---|---|
| R-01 | Já existe pipeline de pré-vendas com outro nome, e criar "Pré-vendas" duplica a operação | Item 4.1 |
| R-02 | Já existem campos de qualificação (BANT) com nome diferente, e eu crio duplicados que ninguém preenche | Item 4.2 |
| R-03 | Já existe workflow ativo usando as tags `fila-*`, que vai reagir à minha cadência | Itens 4.3 + 4.4 |
| R-04 | O calendário do closer existente está com **Sticky Contact ligado** — isso sobrescreve o contato errado quando o SDR agenda pelo mesmo navegador | Item 4.5 |
| R-05 | A subconta não tem provedor de WhatsApp ativo, e metade da cadência não sai | Checar em Settings → Integrações antes de ligar o workflow |
