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

## 2. Cobertura: o que o MCP lê e o que não lê

A tabela abaixo mede o toolkit **HighLevel via Composio**, que é o que eu
consegui inspecionar sem conexão. **Ela não descreve o `lc-mcp`**: o conjunto
de ferramentas do app oficial eu só vejo quando ele estiver carregado numa
sessão. Primeira coisa que faço ao conectar é refazer esta tabela com o que o
`lc-mcp` realmente expõe — inclusive workflows e formulários, que podem muito
bem estar cobertos lá.

| # | Item da auditoria | Ferramenta | Cobertura |
|---|---|---|---|
| 1 | Pipelines e etapas | `HIGHLEVEL_GET_PIPELINES` | Total |
| 2 | Campos personalizados de contato e oportunidade | `HIGHLEVEL_GET_CUSTOM_FIELDS` (`model=all`) e `HIGHLEVEL_GET_CUSTOM_FIELDS_BY_OBJECT_KEY` | Total |
| 3 | Tags existentes | `HIGHLEVEL_LIST_TAGS` | Total |
| 4 | **Workflows (nome e status)** | — | **Não exposta.** A API v2 tem `GET /workflows/`, mas o toolkit não publica essa ferramenta |
| 5 | Calendários | `HIGHLEVEL_GET_CALENDARS` (`showDrafted=true`) | Total |
| 6 | **Formulários** | — | **Não exposta.** A API v2 tem `GET /forms/`, mas o toolkit não publica essa ferramenta |
| — | Subcontas disponíveis | `HIGHLEVEL_SEARCH_LOCATIONS`, `HIGHLEVEL_GET_LOCATION` | Total — é assim que eu te mostro as subcontas para você escolher |

Para os itens 4 e 6, o caminho é manual: **Automação → Workflows** e
**Sites → Formulários**, com print ou a lista copiada. Se depois da conexão eu
encontrar as ferramentas (o catálogo da Composio muda), eu te aviso e puxo.

## 3. Escrita (Etapas 2 e 3) — cobertura

| Operação | Ferramenta | Cobertura |
|---|---|---|
| Criar campo TEXT, NUMERICAL, DATE, URL | `HIGHLEVEL_LOCATIONS_CREATE_CUSTOM_FIELD` | Total |
| Criar campo de **lista** (SINGLE_OPTIONS) e **múltipla** (MULTIPLE_OPTIONS) | `HIGHLEVEL_CREATE_CUSTOM_FIELD` | **Parcial** — a ferramenta antiga não aceita `options`; a nova aceita, mas exige `objectKey`/`fieldKey`/`parentId`. Se as opções não entrarem pela API, eu crio o campo e você completa as opções na tela. Eu te digo caso por caso |
| Criar tag | `HIGHLEVEL_CREATE_TAG` | Total |
| Criar pipeline/etapas, workflow, calendário, formulário, lista inteligente | — | **Não suportado pelo MCP.** É o conteúdo do `build-wesales.md` |

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
