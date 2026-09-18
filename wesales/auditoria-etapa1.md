# Etapa 1 — Auditoria da subconta (somente leitura)

Estado: **bloqueada por acesso**. O plano, as ferramentas e a tabela de
resultado estão prontos; falta a conexão.

## 1. Por que está bloqueada

Nenhum servidor **MCP LeadConnector** está disponível nesta sessão. Verifiquei
de três formas: busca direta por `leadconnector`, busca por ferramentas de
GoHighLevel (contatos, pipelines, campos, tags) e a lista de servidores MCP
que a sessão carregou. Não há nada de LeadConnector nem de WeSales.

O que existe é o toolkit **HighLevel via Composio** — a mesma API v2 do GHL,
que é o que o white-label da WeSales roda por baixo. Ele está catalogado, mas
sem conexão ativa, e a Composio **não tem auth gerenciada** para HighLevel:

> Composio does not have managed auth for 'highlevel', so the user must set up
> their own auth config before connecting.

### O que você precisa fazer (uma vez)

1. Criar um app de marketplace no GHL/LeadConnector (Settings → My Apps, ou
   `marketplace.gohighlevel.com` → criar app) com escopos de leitura e, para
   as Etapas 2 e 3, de escrita:
   `locations.readonly`, `locations/customFields.readonly`,
   `locations/customFields.write`, `locations/tags.readonly`,
   `locations/tags.write`, `opportunities.readonly`, `calendars.readonly`,
   `contacts.readonly`, `contacts.write`, `forms.readonly`.
2. Registrar o Client ID / Client Secret desse app como auth config do
   HighLevel na Composio: [Set up highlevel](https://dashboard.composio.dev/~/org/connect/apps/highlevel?open=true)
3. Me avisar. Eu disparo a conexão, você autoriza escolhendo a subconta, e eu
   rodo a auditoria.

**Alternativa sem integração:** me manda print ou export das 6 listas e eu
preencho a auditoria na mão. O resultado é o mesmo para as Etapas 4 e 5.

## 2. Cobertura: o que o MCP lê e o que não lê

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
