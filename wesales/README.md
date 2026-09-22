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
| `auditoria-resultado.md` | **Etapa 1 — resultado**, rodado em 18/09/2026 na subconta real |
| `campos-e-tags.md` | Etapas 2 e 3 — lista exata de campos e tags para você confirmar antes de eu criar |
| `build-wesales.md` | Etapa 4 — especificação nó a nó do que é manual na tela |
| `rotina-limpar-tarefas.md` | Etapa 5 — prompt da rotina horária de manutenção |
| `ROADMAP-SALES-ENGAGEMENT.md` | **A distância até um Reev/Meetime** — lacunas medidas e priorizadas. É o backlog que a rotina horária trabalha |
| `APROVADO.md` | O freio de mão: o que a rotina pode escrever no CRM |
| `rotina-horaria.md` | Como a rotina de construção contínua funciona |
| `conectar.md` | **Como conectar o CRM** — caminho curto, por Private Integration Token, sem OAuth e sem e-mail |
| `APRENDIZADOS-CRM.md` | O que as execuções da rotina já descobriram sobre o conector e o GHL, para não redescobrir 24 vezes por dia |
| `biblioteca-mensagens.md` | R-04 — textos das mensagens automáticas, versionados por código; fonte única, `build-wesales.md` só referencia |
| `script-de-ligacao.md` | R-06 — o que o SDR fala numa ligação: abertura, perguntas de diagnóstico na ordem da régua de qualificação, ponte para o agendamento e as 8 objeções mais comuns |
| `GUIA-MONTAGEM.md` | Passo a passo, fase por fase, para quem vai clicar na tela e montar o que o `build-wesales.md` especifica — pipeline, campos, calendário, workflows, listas |
| `IMPLEMENTACAO-WORKFLOWS.md` | **O documento de implementação, em três partes:** Estrutura (pipeline, campos, tags, calendário, formulário, listas, dashboard, pausas, papéis), Workflows (cada nó de cada um: ação, campo, operador, valor, ramo, com os nomes reais lidos da subconta) e Operação (o dia do SDR, do closer e do gestor, regras de convivência com a automação, metas, checklist de go-live). Para montar e operar à mão, sem "Construir com IA" |
| `AGENTE-IA-CONEXAO.md` | Definição do agente de IA "Conexão — Inbound" para a tela (Agentes de AI → IA v2): trabalho do agente, regra do portão, valores de cada aba, prompt do sistema e os rótulos exatos dos campos |
| `CONFERENCIA-CAMPOS.md` | O que a tela tem contra o que o `campos-e-tags.md` pede, campo por campo, depois da Fase 2 montada — o que falta, o que divergiu de nome, de opção e de tipo |
| `ESTADO-E-PLANO.md` | Leitura completa da subconta (documentos + API ao vivo + workflows), pedida pelo dono antes de implementar — o que está medido, o que os dumps de workflow não dizem, e o plano de continuidade por etapas |

## Estado do acesso (18/09/2026)

O caminho está em `conectar.md`. Resumo do que foi medido: a allowlist de rede
deste ambiente bloqueia `services.leadconnectorhq.com`, então servidor de
`.mcp.json` — que conecta de dentro do contêiner — não sobe. **Conector do
claude.ai conecta pela infraestrutura do Claude e não passa por esse proxy**,
então é por ali que o CRM entra: conector personalizado com a URL do MCP e o
Private Integration Token num cabeçalho estático.

Servidores MCP carregam no início da sessão: configure e abra uma sessão nova.
Cobertura das ferramentas em `auditoria-etapa1.md`.

**Nada foi criado, alterado ou excluído na subconta.** Todos os documentos
aqui são especificação.
