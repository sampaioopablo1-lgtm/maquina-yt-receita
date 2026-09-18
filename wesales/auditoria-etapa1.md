# Etapa 1 — Auditoria da subconta (somente leitura)

Estado: **bloqueada por acesso**. O plano, as ferramentas e a tabela de
resultado estão prontos; falta a conexão.

## 1. Estado do acesso

Nenhum servidor **MCP LeadConnector** estava carregado na sessão em que este
documento nasceu. O caminho oficial existe e é o certo: o app
**`lc-mcp - Anthropic`** (publicado pela própria leadconnector, categoria CRM,
gratuito) no marketplace do LeadConnector — o mesmo marketplace que a WeSales
usa por baixo do white-label.

### O que você faz (uma vez)

1. No `marketplace.leadconnectorhq.com`, instalar o app `lc-mcp - Anthropic` e,
   na tela **Choose location**, escolher a subconta da operação de SDR.
2. Antes de autorizar, conferir a aba **Permissions**. A operação precisa de:
   contatos (ler e escrever), campos personalizados (ler e escrever), tags
   (ler e escrever), oportunidades (ler), calendários (ler), formulários (ler).
3. Me dizer **qual subconta** você autorizou.

### Detalhe que economiza uma frustração

Servidores MCP são carregados **no início da sessão**. Autorizar o app com uma
sessão já aberta não faz as ferramentas aparecerem nela. Depois de autorizar,
**abra uma sessão nova** e peça a auditoria — como tudo aqui está commitado, a
sessão nova já começa com o projeto inteiro em mãos.

### Caminho alternativo (só se o oficial não servir)

Toolkit **HighLevel via Composio**, que fala a mesma API v2. Exige auth config
próprio (a Composio não tem auth gerenciada para HighLevel), o que significa
criar um app de marketplace com Client ID/Secret e registrá-lo em
[Set up highlevel](https://dashboard.composio.dev/~/org/connect/apps/highlevel?open=true).
Mais trabalho, mesma API — use só se o `lc-mcp` não cobrir a subconta.

**Sem integração nenhuma:** me manda print ou export das 6 listas e eu preencho
a auditoria na mão. Para as Etapas 4 e 5 o resultado é idêntico.

## 2. O que a documentação do MCP oficial diz

Estudado em 18/09/2026. O servidor é hospedado pela própria HighLevel em
`https://services.leadconnectorhq.com/mcp/` e atende contatos, conversas,
calendários, oportunidades, pagamentos, locations e campos personalizados.

### Duas formas de autenticar

| Forma | Como | Quando usar |
|---|---|---|
| **App `lc-mcp - Anthropic`** | Instalar pelo marketplace e autorizar a subconta | É o caminho que estamos tomando. Sem token para copiar e colar |
| **Private Integration Token** | Subconta → Settings → Private Integrations → Create New Integration, escolher os escopos, copiar o token | Plano B. O token **começa com `pit-`**; chave de API comum ou v1 **não funciona** e é a causa nº 1 de erro 401 |

O PIT é por subconta (token + Location ID), então um token por cliente mantém
os dados separados e permite revogar um sem derrubar os outros.

### Ferramentas confirmadas na documentação

Nomes reais, como o servidor os expõe:

| Domínio | Ferramentas |
|---|---|
| Contatos | `contacts_get-contacts`, `contacts_get-contact`, `contacts_create-contact`, `contacts_update-contact`, `contacts_upsert-contact` |
| Tags | `contacts_add-tags`, `contacts_remove-tags` |
| Tarefas | `contacts_get-all-tasks` |
| Conversas | `conversations_search-conversation`, `conversations_get-messages`, `conversations_send-a-new-message` |
| Oportunidades | `opportunities_search-opportunity`, `opportunities_get-opportunity`, `opportunities_update-opportunity` |
| Calendários | `calendars_get-calendar-events`, `calendars_get-appointment-notes` |
| Subconta | `locations_get-location`, `locations_get-custom-fields` |

### O que isso significa para o nosso plano

Três consequências, e nenhuma delas é ruim se a gente souber antes:

1. **`locations_get-custom-fields` é leitura.** Não há
   `locations_create-custom-field` na lista publicada. Se confirmar,
   **a Etapa 2 não sai pelo MCP oficial** — ou vai pela API (rota Composio da
   seção 3) ou vira criação manual na tela, 26 campos.
2. **Tag se cria aplicando.** Não há ferramenta de criar tag solta, mas
   `contacts_add-tags` aplica uma tag a um contato e o GHL registra a tag na
   subconta nesse momento. Dá para nascer as 11 tags assim, num contato de
   teste. Funciona, mas é atalho — diga se prefere criar na tela.
3. **A rotina da Etapa 5 tem o que ler, falta confirmar o que escrever.**
   `contacts_get-all-tasks` lê as tarefas; concluir tarefa não aparece na
   lista publicada. Se não existir, a rotina horária vira relatório (aponta o
   que está fora de lugar) em vez de faxina automática.

**Nenhum desses três pontos está fechado.** A lista acima é a que a
documentação pública expõe e ela mesma se declara parcial. A primeira coisa
que faço ao conectar é listar as ferramentas reais e refazer esta seção — aí
sim com o que existe de verdade, não com o que está publicado.

## 3. Cobertura da auditoria e das criações

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

**Sem integração nenhuma:** me manda print ou export das 6 listas e eu preencho
a auditoria na mão. Para as Etapas 4 e 5 o resultado é idêntico.

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
