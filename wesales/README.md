# WeSales — operação de SDR (pré-vendas B2B)

**Este diretório é do projeto da OPERAÇÃO DE SDR na WeSales (white-label do
GoHighLevel), não da máquina de YouTube e não da Jazz Imobiliária.**

Seguindo a convenção de `jazz/`, a fronteira é esta pasta: nada aqui toca
canais, vozes, produção ou publicação de vídeo — e nada da máquina deve
importar daqui. Se preferir, esta pasta migra para um repositório próprio
(`wesales-sdr`) sem quebrar nada.

## O que vive aqui

| Arquivo | Conteúdo |
|---|---|
| `briefing-sdr.md` | As instruções guardadas: a máquina que estamos construindo, cadência, regras e decisões em aberto |
| `auditoria-etapa1.md` | Etapa 1 — plano de auditoria, o que o MCP lê e o que não lê, e a tabela a preencher |
| `campos-e-tags.md` | Etapas 2 e 3 — lista exata de campos e tags para você confirmar antes de eu criar |
| `build-wesales.md` | Etapa 4 — especificação nó a nó do que é manual na tela |
| `rotina-limpar-tarefas.md` | Etapa 5 — prompt da rotina horária de manutenção |

## Estado do acesso (18/09/2026)

Não existe servidor MCP LeadConnector nesta sessão. O caminho viável é o
toolkit **HighLevel via Composio**, que ainda precisa de um auth config
próprio (a Composio não tem auth gerenciada para HighLevel). Detalhes e
cobertura em `auditoria-etapa1.md`.

**Nada foi criado, alterado ou excluído na subconta.** Todos os documentos
aqui são especificação.
