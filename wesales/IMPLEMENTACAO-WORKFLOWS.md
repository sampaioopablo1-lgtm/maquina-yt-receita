# Implementação — configuração exata do CRM, dos workflows e da operação

Referência de montagem **clique a clique** do projeto inteiro na tela da
WeSales (GoHighLevel), em três partes: **Parte 1 — Estrutura** (o que existe
antes de qualquer workflow: pipeline, campos, tags, calendário, formulário,
listas, dashboard, pausas, usuários), **Parte 2 — Workflows** (cada nó de cada
um) e **Parte 3 — Operação** (como SDR, closer e gestor usam isso todo dia,
e o que nunca fazer na tela). Escrito em 21/09/2026 depois de três tentativas do
"Construir com IA" do construtor inventarem campos que não existem
(`APRENDIZADOS-CRM.md`) — este arquivo existe para que cada nó seja montado
**à mão, com o nome exato** de campo, opção, tag, etapa e workflow.

**Divisão de trabalho entre os documentos:**
- `build-wesales.md` — o **porquê** de cada nó, a pesquisa, as decisões. É a
  fonte da lógica; se este arquivo divergir dele, ele manda.
- **Este arquivo** — o **como clicar**: ação, campo, operador, valor, ramo.
  Nenhuma explicação além de uma linha; o número da seção do
  `build-wesales.md` está no título de cada workflow para quem quiser o
  motivo.
- `GUIA-MONTAGEM.md` — a **ordem** das fases e o **estado** do que já foi
  montado.

**Três regras antes de montar qualquer nó:**
1. **Não use "Construir com IA"** para nada que compare ou escreva campo
   personalizado. Monte manual ("Point & Edit"). A IA já trocou `Reunião foi
   qualificada` por `Tags`, `Rescheduled`, `score` e `Last appointment at`
   três vezes seguidas, e mantém a condição errada por trás de um nó mesmo
   depois de renomeá-lo.
2. **Nome é chave.** Etapa, tag, opção de campo e nome de workflow são
   comparados como texto exato pelo GHL. Copie deste arquivo, não digite de
   cabeça — `Caixa Postal` ≠ `Caixa postal`, `IA Whatsapp` ≠ `IA WhatsApp`.
3. **Publique, dispare uma vez num contato de teste e leia o rastro.** A
   seção "Teste" de cada workflow diz o que mudar e o que deve aparecer no
   contato. Workflow "Publicado" sem rastro no campo não rodou
   (`APRENDIZADOS-CRM.md`, 21/09).

---

## 0. Dicionário de nomes reais (lido da subconta por API em 21/09/2026)

### 0.1 Pipeline e etapas

Pipeline: **`FUNIL DE VENDAS`** (id `0Fo2xbeayE4EP6yuSUtq`). No seletor de
etapa do GHL a etapa aparece como `[FUNIL DE VENDAS] - NOME`.

| Etapa | id | Papel |
|---|---|---|
| `NOVO LEAD` | `7ae9c950-9bcf-4e60-8bc5-cb7388c87b7d` | Entrou pela Porta de Entrada, ainda sem cadência |
| `CONECTAR` | `deb60542-a5cd-43ae-b875-b467b120a72c` | Correndo a cadência (12x30, Inbound ou Reengajamento) |
| `AGENDAR` | `3d26fcd1-220d-49ed-8325-705dfe9055b1` | Atendeu, ainda sem reunião marcada |
| `NEGOCIAR` | `cbcf0229-5e19-4fdb-8c50-6c641b78b3bb` | Reunião marcada / com o closer |
| `FORMALIZAR` | `b8485ec0-98e8-459f-b990-f40a5e3bd25b` | Fechamento (closer) |

**Status da oportunidade** é um campo separado da etapa: `open` (ativa),
`abandoned` (ex-"Nutrição", 90 dias), `lost` (ex-"Descartado"), `won`.
Sair de cadência quase sempre muda **só o status**, sem sair de `CONECTAR`
(`build-wesales.md`, tabela 1.0). Todo portão "o lead ainda está ativo?"
checa **etapa E status**.

### 0.2 Tags (exatamente assim, minúsculas, com hífen)

| Tag | Uso | Existe na tela? |
|---|---|---|
| `fila-quente` | Fila prioritária do SDR | sim |
| `fila-tel` | Tarefa de telefone aberta hoje | sim |
| `fila-wa` | Tarefa de ligação WhatsApp aberta hoje | sim |
| `fila-linkedin` | Reserva (L-03) | sim |
| `conectado-hoje` | Atendeu hoje | sim |
| `nao-perturbe` | Opt-out (sempre junto do DND nativo) | sim |
| `limpar-tarefas` | Rotina de higiene pode fechar tarefas `[CADENCIA]` vencidas | sim |
| `nutricao-90d` | Em nutrição; **é o gatilho** do Reengajamento 90 dias | sim |
| `telefone-invalido` | Sem telefone ou número errado | sim |
| `cad-inbound` / `cad-outbound` | Origem do lead (decide qual cadência) | sim |
| `atraso-1a-tentativa` | Speed-to-lead estourou | sim |
| `reengajamento-ativo` | Na régua TR1–TR4 | sim |
| `pausado` | Represado pelo SDR, sem ser opt-out | sim |
| `toque` | Pulso: cada tarefa/mensagem aplica e o Contador de Toques remove | sim |
| `novo-lead-estagnado` | F-05 peça 1: 24h em `NOVO LEAD` | **não** — `[ ]` em `APROVADO.md` |
| `fila-travada` | F-05 peça 2: `fila-tel`/`fila-wa` que o nó 9 da cadência não removeu | **não** — `[ ]` em `APROVADO.md` |

### 0.3 Campos personalizados (nome na tela → chave de merge field → tipo → opções exatas)

Merge field: `{{contact.CHAVE}}`. O GHL **remove** a letra acentuada ao
gerar a chave (`qualificação` → `qualificao`); use a chave desta tabela,
nunca a transliteração.

**Controle da cadência**

| Nome na tela | Chave | Tipo | Opções exatas |
|---|---|---|---|
| `Tentativa nº` | `tentativa_n` | NUMERICAL | — |
| `Resultado da tentativa` | `resultado_da_tentativa` | SINGLE_OPTIONS | `Atendeu` · `Caixa Postal` · `Não atendeu` · `Número errado` · `Pediu retorno` · `Não ligar` |
| `WA não atendidas seguidas` | `wa_no_atendidas_seguidas` | NUMERICAL | — |
| `Permissão WhatsApp` | `permisso_whatsapp` | SINGLE_OPTIONS | `Sim` · `Não` · `Não solicitado` |
| `Prioridade` | `prioridade` | NUMERICAL | 1 a 5 |
| `Entrada em` | `entrada_em` | TEXT | ver nota `{{right_now}}` abaixo |
| `1ª tentativa em` | `1_tentativa_em` | TEXT | idem |
| `Template usado` | `template_usado` | TEXT | código da mensagem (`M1-a`, `M2-v1`…) |
| `Tentativas telefone` / `Tentativas WhatsApp` | `tentativas_telefone` / `tentativas_whatsapp` | NUMERICAL | — |
| `Conexões telefone` / `Conexões WhatsApp` | `conexes_telefone` / `conexes_whatsapp` | NUMERICAL | — |
| `Total de ligações` / `Total de conexões` | `total_de_ligaes` / `total_de_conexes` | NUMERICAL | — |
| `Sinal recebido` | `sinal_recebido` | SINGLE_OPTIONS | `Clique em link` · `Resposta de mensagem` |
| `Data e hora do sinal` | `data_e_hora_do_sinal` | TEXT | não usado desde 19/09 (seção 2.9.2) |
| `Nota de qualificação` | `nota_de_qualificao` | NUMERICAL | 0–100 |
| `Reunião foi qualificada` | `reunio_foi_qualificada` | SINGLE_OPTIONS | `Sim` · `Não` · `Parcial` |
| `Motivo da desqualificação` | `motivo_da_desqualificao` | SINGLE_OPTIONS | `Sem fit` · `Sem budget` · `Timing errado` · `Não é decisor` · `Concorrente` · `Duplicado ou já cliente` |
| `Data do veredito do closer` | `data_do_veredito_do_closer` | DATE | só data |
| `Data conectado` / `Data agendado` / `Data compareceu` | `data_conectado` / `data_agendado` / `data_compareceu` | DATE | só data |
| `Nº de no-shows` | `n_de_noshows` | NUMERICAL | — |
| `Data de retorno` | `data_de_retorno` | DATE | (S-01; o `build-wesales.md` chama de `Data do retorno`) |
| `Site` / `Instagram` / `Empresa` / `Segmento` | `site` / `instagram` / `empresa` / `segmento` | TEXT | — |

**Qualificação (lidos pela régua 9.1 e pelo formulário)**

| Nome na tela | Chave | Opções exatas |
|---|---|---|
| `Clientes novos por mês` | `clientes_novos_por_ms` | `10` · `11-30` · `31-100` · `+101` |
| `Tem time comercial` | `tem_time_comercial` | `Só dono` · `1-5` · `6-10` · `+10` |
| `Quem atende os leads` | `quem_atende_os_leads` | `Dono` · `SDR` · `Vendedor` · `Ninguém fixo` |
| `Investe em anúncios` | `investe_em_anncios` | `Sim` · `Já investiu e parou` · `Nunca` |
| `Investimento mensal em anúncios` | `investimento_mensal_em_anncios` | `Até 1k` · `1k a 5k` · `5k a 10k` · `Acima de 10k` — **o Meta grava outros valores (G-04)** |
| `Plataformas de anúncio` | `plataformas_de_anncio` | `Meta` · `Google` · `Tiktok` · `Outros` |
| `Já teve agência?` | `j_teve_agncia` | `Tem hoje` · `Já teve` · `Nunca teve` |
| `Experiência com agência` | `experincia_com_agncia` | texto |
| `Usa CRM` | `usa_crm` | `Sim` · `Não` |
| `Canal principal de venda` | `canal_principal_de_venda` | `WhatsApp` · `Telefone` · `Loja` · `Online` |
| `Budget` | `budget` | `Tem` · `Precisa aprovar` · `Não tem` |
| `Decisor` | `decisor` | `Sim` · `Influencia` · `Não decide` |
| `Prazo` | `prazo` | `Pra ontem` · `Espera 30 dias` · `Este ano` · `Sem prazo` — **o Meta grava em `Urgência`, não aqui (G-04)** |
| `Dor principal` | `dor_principal` | texto |
| `Qualificação` | `qualificao` | `SDR` · `IA Whatsapp` · `Vendedor` |
| `Necessidade` / `Urgência` | `necessidade` / `urgncia` | texto — onde o Meta Lead Ads grava hoje (`CONFERENCIA-CAMPOS.md`, Tabela H) |

**Campos que a especificação usa e que NÃO existem na tela ainda** (criar
antes do nó que os usa — `campos-e-tags.md`): `Toques na semana` (C-26,
NUMERICAL — Contador de Toques e portões 2.5c/3c), `Hora da conexão` (C-25,
TEXT — Pós-ligação nós 7b/7c), `Hora do retorno` (S-01, TEXT).

**Campos nativos usados em condição:** `Phone` (telefone), `Assigned User`
(dono do contato), `DND`, `Tags`, `Pipeline stage`, `Opportunity status`.
Merge fields nativos: `{{contact.name}}`, `{{contact.first_name}}`,
`{{contact.source}}`, `{{user.name}}`, `{{appointment.start_time}}`,
`{{opportunity.status}}`, `{{location.name}}`.

**`{{right_now}}` — pendência aberta (`GUIA-MONTAGEM.md`, "Antes da Fase
5"):** ao vivo na tela, o seletor de valor de `Update Contact Field` num
campo TEXT não ofereceu "data/hora atual". Onde este arquivo diz
`= {{right_now}}`, tente primeiro o merge field digitado no `{}`; se não
renderizar, grave a **marca fixa `sim`** (o Alerta de Speed-to-lead só
pergunta se o campo está vazio, não que horas são — seção 2.9.2). Em campo
DATE (`Data conectado` etc.) o seletor tem "data atual" nativo.

**`{{opportunity.pipeline_stage}}` — confirmado quebrado na tela (21/09):** a
nota do Mestre de saída publicado renderiza a etapa em branco. Abra o `{}`
do nó de nota e pegue o token real de "Pipeline Stage" da lista (o GHL usa
um nome interno diferente do documentado); `{{opportunity.status}}`
renderiza certo.

### 0.4 Nomes exatos dos workflows (para `Remove from Workflow` / `Add to Workflow`)

`Porta de Entrada` · `Mestre de saída` · `Pós-ligação` · `Pós-agendamento` ·
`Loop do closer` · `Registro de Comparecimento` · `Recuperação de No-show` ·
`SLA do Closer — No-show` · `Qualificação por IA no WhatsApp` · `Cadência
12x30` · `Cadência Inbound` · `Interceptação de Sinal — Clique` ·
`Interceptação de Sinal — Resposta` · `Opt-out por Palavra-chave` · `Alerta
de Speed-to-lead` · `Reengajamento 90 dias` · `Contador de Toques` ·
`Monitor de Capacidade` · `Lead Esquecido em NOVO LEAD` · `Fila Travada` ·
`Higiene de Número — Validação Automática`.

Na tela o Loop do closer foi criado como **`Post-Meeting Closer Loop`** —
renomeie para `Loop do closer` ou use o nome da tela em todo lugar que o
cita (Pós-agendamento nó 3 não o cita; nenhum outro workflow remove dele, o
nome só precisa bater consigo mesmo).

### 0.5 Outros objetos

| Objeto | Nome exato |
|---|---|
| Calendário do closer | `Reunião com closer` |
| Trigger Link | `Agendar com o closer` (destino: URL pública do calendário) |
| Usuário (único hoje) | id `JdvhvOTEBTvUyRi0BXU8` — vira o grupo de round robin com uma pessoa |
| Fuso da subconta | `America/Sao_Paulo` |
| Contatos de teste | `Teste Atendeu` `Lj96CIFYaGKPiC0opzbc` (em `NEGOCIAR`) · `Teste Não Atende` `OIvOGQfdGg2Ndr5GtcAG` · `Teste Retorno` `vrwdERfR24ax6GylG6No` · `Teste Número Errado` `qkHSdIMPJTB2JK5ECGrY` · `Teste Não Ligar` `2MXzDPjxGjuvvsxlp5V1` (DND ligado) · `ZZ TESTE ESTRUTURA` `c5r3ZxiAd8T5adL1Bt6j` (tem todas as tags) |

### 0.6 Ações do construtor — nome em inglês (documentação) e como aparecem na tela em português

| Ação (EN) | Na tela (pt-BR, pode variar com a versão) |
|---|---|
| If/Else | Se/Senão · ramos **Branch** (verdadeiro) e **None** (nenhuma condição bateu) |
| Update Contact Field | Atualizar campo do contato |
| Math Operation | Operação matemática (dentro de "Atualizar campo" em versões novas) |
| Add / Remove Contact Tag | Adicionar tag / Remover tag |
| Add Task | Adicionar tarefa |
| Add Note | Adicionar nota |
| Internal Notification | Notificação interna |
| Send WhatsApp | Enviar mensagem WhatsApp |
| Wait → Time Delay / Until specific time / Condition / Contact Replied | Aguardar → Atraso de tempo / Até horário específico / Condição / Resposta do contato |
| Create/Update Opportunity | Criar/atualizar oportunidade |
| Update Opportunity (status/etapa) | Atualizar oportunidade |
| Find opportunity | Buscar oportunidade |
| Assign to User | Atribuir a usuário |
| Add to / Remove from Workflow | Adicionar ao / Remover do fluxo de trabalho |
| Set Contact DND | Definir DND do contato |
| Split | Dividir (teste A/B) |
| Date/Time Formatter | Formatador de data/hora |
| Conversation AI | IA de conversa |

**Configurações do workflow** ficam na aba **Configurações** (canto superior):
`Allow Re-entry` = "Permitir reentrada"; `Stop on Response` = "Parar ao
responder"; janela = "Janela de tempo" (dias + horário + fuso).

---


---

# PARTE 1 — ESTRUTURA (antes de qualquer workflow)

Tudo aqui é criado uma vez, na tela. Nada sai pelo conector `GHL CRM`
(campo, calendário, formulário, lista, dashboard não têm ferramenta de
criação nele — `APRENDIZADOS-CRM.md`). Ordem: 1.1 → 1.2 → 1.3 → 1.4 → 1.5 →
1.6, depois os workflows (Parte 2), depois 1.7 → 1.10.

## 1.1 Pipeline — já existe, não mexer

Configurações → Pipelines → `FUNIL DE VENDAS`. As 5 etapas da seção 0.1 já
estão na tela desde 18/09/2026 com cor e probabilidade próprias. **Não
renomear etapa** — todo `If/Else` e todo gatilho compara o nome exato; e
**não excluir etapa** (regra 1; hoje há oportunidades reais em `NOVO LEAD` e
`NEGOCIAR`). A tabela de 7 etapas antiga do `GUIA-MONTAGEM.md`, Fase 1, é
histórico — está marcada como tal lá.

## 1.2 Campos personalizados

Configurações → Campos personalizados → **Adicionar campo** → Objeto:
**Contato** → Tipo → Nome → (opções, uma por linha, texto **exato**) →
Pasta.

A lista completa, com nome, chave, tipo e opções exatas, é a tabela da
seção 0.3 (é a mesma da `campos-e-tags.md`, que é a fonte). Estado na tela em
21/09/2026: **tudo da 0.3 já existe**, exceto o que segue.

**Criar agora (bloqueiam workflows da Parte 2):**

| Nome exato | Tipo | Opções | Pasta | Quem precisa |
|---|---|---|---|---|
| `Toques na semana` | NUMERICAL | — | mesma dos campos de controle (`gabsbU3jsUN7oIXCnYab`) | W1 Contador de Toques; portões 2.5c (W11) e 3c (W13) |
| `Hora da conexão` | TEXT | placeholder `HH` | idem | W4 nós A7b/A7c (F-02); lista 8.19 |
| `Hora do retorno` | TEXT | placeholder `HH:MM` | idem | W4 ramo `Pediu retorno` (vencimento com hora); lista 8.4 |

**Corrigir (não dá para trocar tipo de campo criado — criar novo, deixar o
antigo parado, nunca excluir):**

| Hoje | Problema | O que fazer |
|---|---|---|
| `Plataformas de anúncio` — SINGLE_OPTIONS | lead que anuncia em Meta **e** Google só registra um | criar `Plataformas de anúncio (múltipla)` MULTIPLE_OPTIONS com `Meta`, `Google`, `Tiktok`, `Outros`; apontar formulário (1.5) e prompt da IA (W10) para o novo |
| `Investimento mensal em anúncios` — opções `Até 1k` / `1k a 5k` / `5k a 10k` / `Acima de 10k` | o Meta Lead Ads grava `Não invisto nada ainda` / `Até R$ 1.000` / `Abaixo de 5k` / `Acima de 10k` — três valores fora da lista, a régua 9.1 nunca casa | **decisão G-04** (`CONFERENCIA-CAMPOS.md`, Tabela H): Opção A — trocar as opções pelos 4 textos exatos do Meta e reponderar a régua (12/6/3/1); Opção B — régua lê `Urgência`/`Necessidade` por `Contains` |
| `Prazo` / `Dor principal` chegam vazios do Meta; `Urgência` / `Necessidade` cheios | o formulário do anúncio mapeia para os campos que a tela criou sozinha | G-04, mesma decisão: apontar os 8 formulários do Meta para `Prazo`/`Dor principal` (Opção A) ou ler os outros dois (Opção B) |

**Regras ao criar campo:** o nome vira a chave de merge field sem acento
(`Urgência` → `urgncia`) — depois de criar, leia a chave real em
Configurações → Campos → ícone `{}` ou por `locations_get-custom-fields`, e
use **essa** nos nós; opção de lista é comparada por texto exato; campo
`DATE` guarda só a data (hora em TEXT); nunca renomear campo em uso (o
`Update Contact Field` dos workflows aponta por id, mas o merge field nas
notas aponta por chave).

## 1.3 Tags

Configurações → Tags → **Nova tag** (ou aplicar a um contato — o GHL cria
na hora). Minúsculas, hífen, exatamente como a seção 0.2. Estado: as 15
primeiras existem (aplicadas ao contato `ZZ TESTE ESTRUTURA`); faltam
`novo-lead-estagnado` (W17) e `fila-travada` (W17b) — as duas nascem `[ ]`
em `APROVADO.md` e só saem por API depois do `[x]` do dono.

Três famílias, e a regra de quem mexe:

| Família | Tags | Quem aplica / remove |
|---|---|---|
| **Fila** (aparece nas listas do dia) | `fila-quente`, `fila-tel`, `fila-wa`, `fila-linkedin` | **só workflow**. O SDR nunca aplica nem remove à mão — a fila do dia é consequência da cadência, não decisão |
| **Estado** (sobrevive à saída de cadência) | `nao-perturbe`, `telefone-invalido`, `nutricao-90d`, `cad-inbound`, `cad-outbound`, `conectado-hoje`, `pausado` | workflow, exceto `pausado` (**SDR**, à mão, para represar um lead sem opt-out) e `cad-inbound` (integração/formulário na entrada) |
| **Pulso e alarme** | `toque`, `limpar-tarefas`, `atraso-1a-tentativa`, `reengajamento-ativo`, `novo-lead-estagnado`, `fila-travada` | só workflow; o gestor **lê** (listas 8.5, 8.8, 8.14, 8.20, 8.21), não aplica |

## 1.4 Calendário `Reunião com closer` — já existe

Calendários → `Reunião com closer` → Configurações. Confira contra isto
(`build-wesales.md`, 7.1):

| Configuração | Valor |
|---|---|
| Tipo | Round Robin (mais de um closer) ou Simple |
| Duração | 1 hora (decisão do dono, 18/09) |
| Intervalo entre slots | 15 min |
| Aviso mínimo | 2 horas |
| Máximo por dia | conforme o closer |
| Disponibilidade | seg–sex, horário comercial |
| Confirmação automática | ligada — é o status `Confirmed` que dispara o W5 |
| Fuso | **do contato** |
| **Sticky Contact** | **DESLIGADO** — ligado, o SDR agendando vários leads na mesma aba sobrescreve os dados de um no outro |
| Reagendamento pelo lead | ligado |
| Convidados adicionais | desligado |
| Notificações | e-mail de confirmação ao lead e ao closer; **lembretes de WhatsApp não** (saem do W5, nós 8–10) |
| Formulário anexado | `Qualificação SDR` (1.5), em Calendário → Formulários → Formulário personalizado |

Os status que os workflows leem: `Confirmed`/`Booked` (W5), `Showed` (W7),
`No Show` (W8 e W9). O closer marca `Showed`/`No Show` **no agendamento** —
é o único jeito de disparar 5.2/5.3/5.4.

## 1.5 Formulário `Qualificação SDR` — já existe

Sites → Formulários → `Qualificação SDR`. 23 campos, uma coluna, sem
paginação, sem captcha:

| # | Campo do formulário | Grava em | Obrig. |
|---|---|---|---|
| 1 | Nome | `first_name` / `last_name` (nativos) | sim |
| 2 | Telefone | `phone` | sim |
| 3 | E-mail | `email` | sim |
| 4 | Empresa | `Empresa` (personalizado — o nativo `Company Name` não aparece no construtor) | sim |
| 5 | Segmento | `Segmento` | sim |
| 6 | Site | `Site` | não |
| 7 | Instagram | `Instagram` | não |
| 8 | Clientes novos por mês | `Clientes novos por mês` | sim |
| 9 | Investe em anúncios | `Investe em anúncios` | sim |
| 10 | Investimento mensal | `Investimento mensal em anúncios` | não |
| 11 | Plataformas | `Plataformas de anúncio` (trocar pelo campo múltiplo quando existir) | não |
| 12 | Já teve agência? | `Já teve agência?` | sim |
| 13 | Experiência com agência | `Experiência com agência` | não |
| 14 | Tem time comercial | `Tem time comercial` | sim |
| 15 | Quem atende os leads | `Quem atende os leads` | sim |
| 16 | Usa CRM | `Usa CRM` | não |
| 17 | Canal principal de venda | `Canal principal de venda` | não |
| 18 | Budget | `Budget` | sim |
| 19 | Decisor | `Decisor` | sim |
| 20 | Dor principal | `Dor principal` | sim |
| 21 | Prazo | `Prazo` | sim |
| 22 | Qualificação | `Qualificação` — valor padrão `SDR` | sim |
| 23 | Consentimento de contato | checkbox | sim |

Configurações do formulário: **Sticky Contact desligado**; "Atualizar só
campos vazios" **desligado** (o SDR corrige o que o lead disse errado);
**`Necessidade` e `Urgência` não entram** neste formulário (são o destino do
Meta Lead Ads, G-04).

**Formulários do Meta Lead Ads (8 campanhas, `CONFERENCIA-CAMPOS.md` H):**
em Marketing → Integrações → Facebook → Mapeamento de campos, cada formulário
deve gravar: "o que você busca hoje?" → `Dor principal`; "quando pretende
resolver?" → `Prazo`; "quanto investe por mês?" → `Investimento mensal em
anúncios` — com as **opções do campo iguais, letra por letra, ao texto da
resposta no anúncio** (é a Opção A do G-04; até o dono decidir, o mapeamento
atual continua gravando em `Necessidade`/`Urgência`).

## 1.6 Trigger Link `Agendar com o closer` — já existe

Marketing → Trigger Links → `Agendar com o closer` → URL: a pública do
calendário `Reunião com closer`. É o gatilho do W13-Clique e o link
inserido em `M2-v1`/`M3-v1` pelo `{}` → Custom Values → Trigger Links.
**Nunca cole a URL do calendário direto na mensagem** — sem o trigger link
o clique não é rastreado e o F-01 não dispara.

## 1.7 Listas inteligentes (Contatos → Filtros → Salvar como lista inteligente → ⭐ favorita)

Coluna `Empresa` = o campo **personalizado** `Empresa` (o seletor mostra dois
"Empresa"; o nativo fica vazio). Fonte da lógica: `build-wesales.md`, 8.

| # | Nome exato | Filtros | Colunas | Ordenação | Para quem |
|---|---|---|---|---|---|
| 8.1 | `Fila Quente` | tag `fila-quente` **E** não `nao-perturbe` **E** etapa em (`CONECTAR`, `AGENDAR`) | Nome · `Empresa` · Telefone · `Prioridade` · `Tentativa nº` · `Resultado da tentativa` · `Nota de qualificação` · Última atividade | `Prioridade` desc, `Tentativa nº` asc | SDR — abre primeiro |
| 8.2 | `Fila Telefone Hoje` | tag `fila-tel` **E** não `nao-perturbe` **E** não `telefone-invalido` **E** não `conectado-hoje` **E** etapa = `CONECTAR` | Nome · `Empresa` · Telefone · `Tentativa nº` · `Prioridade` · `Resultado da tentativa` · Tarefas abertas | `Prioridade` desc, `Tentativa nº` asc | SDR |
| 8.3 | `Fila WhatsApp Hoje` | tag `fila-wa` **E** não `nao-perturbe` **E** não `conectado-hoje` **E** `Permissão WhatsApp` = `Sim` **E** etapa = `CONECTAR` | Nome · `Empresa` · Telefone · `Tentativa nº` · `WA não atendidas seguidas` · `Prioridade` | `Prioridade` desc, `WA não atendidas seguidas` asc | SDR |
| 8.4 | `Retornos` | `Resultado da tentativa` = `Pediu retorno` **E** não `nao-perturbe` | Nome · `Empresa` · Telefone · `Data de retorno` · `Prioridade` · `Nota de qualificação` · Tarefas abertas | `Data de retorno` asc | SDR |
| 8.5 | `Sem resultado ontem` | tag `limpar-tarefas` **E** não `fila-tel` **E** não `fila-wa` | Nome · `Tentativa nº` · `Resultado da tentativa` · Última atividade | Última atividade asc | Gestor — diário |
| 8.6 | `Conexão por Tentativa` | `Total de conexões` ≥ 1 | Nome · `Tentativa nº` · `Total de ligações` · `Total de conexões` · `Tentativas telefone` · `Conexões telefone` · `Tentativas WhatsApp` · `Conexões WhatsApp` | `Tentativa nº` asc | Gestor — semanal |
| 8.7 | `Calibração da Régua` | `Reunião foi qualificada` não vazio | Nome · `Nota de qualificação` · `Reunião foi qualificada` · `Motivo da desqualificação` · `Data do veredito do closer` | `Nota de qualificação` desc | Gestor — semanal |
| 8.8 | `Atraso na 1ª Tentativa` | tag `atraso-1a-tentativa` | Nome · `Empresa` · Telefone · `Entrada em` · `1ª tentativa em` · Tarefas abertas | Última atividade asc | Gestor — diário |
| 8.9 | `Funil — Entraram no Mês` | pipeline `FUNIL DE VENDAS` **E** data de criação da oportunidade = este mês (se o filtro não existir em Contatos, use a lista de Oportunidades) | Nome · `Empresa` · Etapa · Data de criação | Data de criação desc | Gestor — mensal |
| 8.10 | `Funil — Conectaram no Mês` | `Data conectado` = este mês | Nome · `Empresa` · `Data conectado` · `Tentativa nº` | `Data conectado` desc | Gestor — mensal |
| 8.11 | `Funil — Agendaram no Mês` | `Data agendado` = este mês | Nome · `Empresa` · `Data agendado` · `Nota de qualificação` | `Data agendado` desc | Gestor — mensal |
| 8.12 | `Funil — Compareceram no Mês` | `Data compareceu` = este mês | Nome · `Empresa` · `Data compareceu` · `Reunião foi qualificada` | `Data compareceu` desc | Gestor — mensal |
| 8.13 | `Resposta por Template` | `Sinal recebido` = `Resposta de mensagem` | Nome · `Template usado` · `Data e hora do sinal` · Etapa | `Template usado` asc | Gestor — A/B |
| 8.14 | `Reengajamento em Curso` | tag `reengajamento-ativo` | Nome · `Empresa` · Telefone · `Tentativa nº` · `Prioridade` · `Template usado` · Tarefas abertas | `Tentativa nº` asc | Gestor |
| 8.15 | `Pausados Individualmente` | tag `pausado` | Nome · `Empresa` · Telefone · `Tentativa nº` · Etapa · Última atividade | Última atividade asc | Gestor — semanal |
| 8.16 | `Fila do Dia — Total` | (tag `fila-tel` **OU** tag `fila-wa`) **E** não `nao-perturbe` | Nome · `Empresa` · Telefone · `Tentativa nº` · `Prioridade` | `Prioridade` desc, `Tentativa nº` asc | Gestor — 11:00 e 15:00 |
| 8.17 | `Recuperação de No-show` | `Nº de no-shows` ≥ 1 **E** etapa = `NEGOCIAR` **E** não `nao-perturbe` | Nome · `Empresa` · Telefone · `Nº de no-shows` · `Template usado` · Última atividade · Tarefas abertas | `Nº de no-shows` desc | Gestor / closer |
| 8.18 | `Higiene — Sem Telefone Válido` | `Phone` vazio **OU** tag `telefone-invalido` | Nome · `Empresa` · E-mail · `Site` · `Instagram` · Etapa · Data de criação | Data de criação asc | Gestor — semanal |
| 8.19 | `Conexão por Segmento e Horário` | `Hora da conexão` não vazio | Nome · `Segmento` · `Hora da conexão` · `Data conectado` · `Tentativa nº` | `Segmento` asc, `Hora da conexão` asc | Gestor — mensal |
| 8.20 | `Saúde — NOVO LEAD Estagnado` | tag `novo-lead-estagnado` | Nome · `Empresa` · Telefone · Origem · Data de criação · Etapa | Data de criação asc | Gestor — diário |
| 8.21 | `Saúde — Fila Travada` | tag `fila-travada` | Nome · Telefone · Etapa · `Tentativa nº` · `Resultado da tentativa` | — (deve ficar vazia) | Gestor — diário |

Com um segundo SDR: duplicar 8.1, 8.2 e 8.3 por pessoa acrescentando o
filtro `Atribuído a = <nome>` (o GHL não tem "usuário atual" em lista).

## 1.8 Dashboard `Painel do Gestor — Pré-vendas` (Reporting → Dashboards → Novo)

| Widget | Configuração |
|---|---|
| Appointment Report | calendário `Reunião com closer` — agendados, cancelados, no-show, comparecimento |
| Opportunities | pipeline `FUNIL DE VENDAS`, por etapa (foto de agora) |
| Tasks | criadas / concluídas / vencidas por dia (proxy de ligações/dia; filtre por título `[CADENCIA]` se a tela permitir) |
| Custom Metric `Estouro da Fila` | `contagem(tag fila-tel OU fila-wa) − 100` — número único |
| Custom Metric `Atrasos de Speed-to-lead` | `contagem(tag atraso-1a-tentativa)` |
| Custom Metric `Taxa de Conexão — Telefone` | `soma(Conexões telefone) ÷ soma(Tentativas telefone) × 100` |
| Custom Metric `Taxa de Conexão — WhatsApp` | `soma(Conexões WhatsApp) ÷ soma(Tentativas WhatsApp) × 100` |

Custom Metrics depende do plano (`trialing` hoje — confira em Reporting →
Custom Metrics antes). Sem elas, os três widgets nativos + listas 8.16/8.8/8.6
cobrem o mesmo dado.

## 1.9 Pausas de feriado e Number Validation

**Automação → Configurações → Global Workflow Settings → Pause Workflow.**
Marcar **só** `Cadência 12x30`, `Cadência Inbound`, `Reengajamento 90 dias`
(os que criam tarefa ou mandam mensagem). `Annually`: 01/01 · 21/04 · 01/05
· 07/09 · 12/10 · 02/11 · 15/11 · 25/12. Sem `Annually`, uma vez por ano:
Carnaval (2 dias), Sexta-feira Santa, Corpus Christi; férias do SDR em blocos
de até 15 dias. Só aparece workflow **publicado** no seletor — fazer depois
da Parte 2.

**Number Validation** (Configurações → Telefone): opcional, pago por
validação; só ligar depois de conferir custo/plano; habilita o W19.

## 1.10 Usuários, papéis e round robin

| Papel | Permissões mínimas | Onde entra na máquina |
|---|---|---|
| **SDR** | Contatos, Oportunidades (mover só `NOVO LEAD` → `CONECTAR`), Conversas, Calendário (agendar), listas favoritas 8.1–8.4 | dono do lead (`Assigned User`, sorteado no nó 0.7b/0.8b); recebe as notificações internas "ligar agora" (W13) e "lead inbound aguardando" (W12) |
| **Closer** | Calendário (marcar `Showed`/`No Show`), Contatos (editar `Reunião foi qualificada` e `Motivo`), Oportunidades (`NEGOCIAR` → `FORMALIZAR`, status `won`) | dono do horário no calendário (W5 nó 11); recebe o alerta de no-show (W9 nó 3) |
| **Gestor** | tudo, inclusive Automação e Reporting | recebe todos os `Internal Notification` "ao gestor" (W3-N4, W8-D5, W9-6, W11-0.0c, W15-4, W17-4, W17b-4, W18-1, W6-5/6) |

Grupo de round robin dos nós 0.7b (W11) e 0.8b (W12): **um só**, com todos
os SDRs — hoje só o dono (`JdvhvOTEBTvUyRi0BXU8`). Ao contratar o segundo
SDR: adicioná-lo nos dois nós e duplicar as listas 8.1–8.3 (1.7).

---

# PARTE 2 — WORKFLOWS

## Ordem de montagem (a mesma de `build-wesales.md`)

| # | Workflow | Estado na tela (19–21/09) | Pré-requisito que falta |
|---|---|---|---|
| 1 | Contador de Toques | não existe | campo `Toques na semana` |
| 2 | Porta de Entrada | **publicado, funciona** | — |
| 3 | Mestre de saída | **publicado, 4 retoques** | — |
| 4 | Pós-ligação | **publicado, 1 retoque** | — |
| 5 | Pós-agendamento | **publicado, nó 4 não grava** | decisão G-04 antes de refazer a nota |
| 6 | Loop do closer | rascunho, montado pela IA com campos errados — **refazer** | — |
| 7 | Registro de Comparecimento | não existe | — |
| 8 | Recuperação de No-show | rascunho | — |
| 9 | SLA do Closer — No-show | não existe | — |
| 10 | Qualificação por IA no WhatsApp | rascunho (placeholder?) | Conversation AI no plano |
| 11 | Cadência 12x30 | rascunho, 0 inscritos | `Toques na semana`, decisão `{{right_now}}`, Trigger Link |
| 12 | Cadência Inbound | não existe | Cadência 12x30 publicada |
| 13 | Interceptação de Sinal — Clique / — Resposta | **publicados**, 1 retoque (filtro opt-out) | — |
| 14 | Opt-out por Palavra-chave | não existe | — |
| 15 | Alerta de Speed-to-lead | não existe | — |
| 16 | Reengajamento 90 dias | não existe | — |
| 17 | Lead Esquecido em NOVO LEAD (F-05 peça 1) | não existe | tag `novo-lead-estagnado` (`APROVADO.md`) |
| 17b | Fila Travada (F-05 peça 2) | não existe | tag `fila-travada` (`APROVADO.md`) |
| 18 | Monitor de Capacidade | não existe | lista 8.16 |
| 19 | Higiene de Número (opcional) | não existe | Number Validation ligado |

---

## W1 · Contador de Toques — `build-wesales.md` 2.19

**Gatilho:** `Contact Tag Added` → Tag: `toque`

| Configuração | Valor |
|---|---|
| Allow Re-entry | Ligado |
| Stop on Response | Desligado |
| Janela | Sem janela |

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 1 | Remove Contact Tag | `toque` | 2 |
| 2 | Update Contact Field → Math | `Toques na semana` = `Toques na semana` **+ 1** | 3 |
| 3 | Wait → Time Delay | **7 dias** | 4 |
| 4 | Update Contact Field → Math | `Toques na semana` = `Toques na semana` **− 1** | fim |

**Pré-requisito:** o campo `Toques na semana` (NUMERICAL) **não existe** na
tela — crie em Configurações → Campos personalizados antes (não sai por
este conector).

**Teste:** aplique a tag `toque` em `ZZ TESTE ESTRUTURA` (ou por API,
`contacts_add-tags`). Em segundos: tag `toque` removida, `Toques na semana`
= 1. Aplique de novo → 2.

---

## W2 · Porta de Entrada — `build-wesales.md` 1.3 — PUBLICADO

**Gatilho:** `Contact Created` — sem filtro.

| Configuração | Valor |
|---|---|
| Allow Re-entry | não se aplica |
| Janela | Sem janela |

| # | Ação | Configuração exata |
|---|---|---|
| 1 | Create/Update Opportunity | Pipeline `FUNIL DE VENDAS` · Etapa `NOVO LEAD` · Nome `{{contact.name}}` · Status `open` · **Allow Duplicate Opportunities: desligado** |

**Rastro confirmado (21/09):** 50 oportunidades, ~5 leads/dia entrando
sozinhos. Nada a corrigir. Lead importado por CSV não dispara — usar `Add
to Workflow` em massa.

---

## W3 · Mestre de saída — `build-wesales.md` 3 — PUBLICADO, com retoques

**Gatilhos (dois, em OU no mesmo workflow):**
1. `Opportunity Stage Changed` → Pipeline `FUNIL DE VENDAS` · qualquer etapa de destino
2. `Opportunity Status Changed` → Pipeline `FUNIL DE VENDAS` · status `Lost` **ou** `Abandoned`

| Configuração | Valor |
|---|---|
| Allow Re-entry | Ligado |
| Stop on Response | Desligado |
| Janela | Sem janela |

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 0 | Remove Contact Tag | `novo-lead-estagnado` (só depois de a tag existir — F-05) | 1 |
| 1 | If/Else | `Opportunity status` é `open` **E** `Pipeline stage` é uma de `[FUNIL DE VENDAS] - NOVO LEAD`, `[FUNIL DE VENDAS] - CONECTAR` → **FIM** (retoque 21/09: a versão publicada só tem `CONECTAR`) · **None:** segue | 2 |
| 2 | Remove from Workflow | `Cadência 12x30` | 2b |
| 2b | Remove from Workflow | `Cadência Inbound` (quando existir) | 2c |
| 2c | Remove from Workflow | `Reengajamento 90 dias` (quando existir) | 3 |
| 3 | Remove from Workflow | `Qualificação por IA no WhatsApp` | 4 |
| 4 | Remove Contact Tag | `fila-quente`, `fila-tel`, `fila-wa`, `fila-linkedin`, `atraso-1a-tentativa`, `reengajamento-ativo`, `pausado`, `fila-travada` (quando a tag existir) | 5 |
| 5 | Add Contact Tag | `limpar-tarefas` | 6 |
| 6 | Add Note | `Saída de cadência · etapa: {{opportunity.pipeline_stage}} · status: {{opportunity.status}} · tentativa {{contact.tentativa_n}} · resultado {{contact.resultado_da_tentativa}}` | fim |

**Retoques obrigatórios na versão publicada (evidência em 21/09):**
1. **Nó 1 — `NOVO LEAD` também encerra.** Confirmado por API: a Porta de
   Entrada cria a oportunidade e 4 segundos depois este workflow grava a
   nota "Saída de cadência · status: open" e aplica `limpar-tarefas` em
   **todo lead novo** (os 10 leads criados desde 19/09 nasceram com a tag).
   O portão atual só protege `CONECTAR`+`open`; a criação em `NOVO LEAD`
   cai no `None` e roda a limpeza inteira. Incluir `NOVO LEAD` na condição
   resolve; as tags/nota já gravadas ficam (regra 1).
2. Nós 2b/2c: entram quando `Cadência Inbound` e `Reengajamento 90 dias`
   existirem (o dropdown só lista workflows criados).
3. Nó 0: entra quando a tag `novo-lead-estagnado` for aprovada e criada.
4. Nó 6: `{{opportunity.pipeline_stage}}` renderiza vazio — trocar pelo
   token real do seletor `{}` (seção 0.3).

**Teste:** em `Teste Não Atende` (`NOVO LEAD`), mude o status da oportunidade
para `abandoned` por API (`opportunities_update-opportunity`) → tags de fila
removidas, `limpar-tarefas` aplicada, nota gravada. Depois volte para `open`.

---

## W4 · Pós-ligação — `build-wesales.md` 4 — PUBLICADO, 1 retoque

**Gatilho:** `Contact Changed` → Filtro: campo `Resultado da tentativa` · `Foi alterado`. **Só esse filtro** (sem filtro de `Tags`).

| Configuração | Valor |
|---|---|
| Allow Re-entry | Ligado |
| Janela | Sem janela |

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 1 | If/Else | `Resultado da tentativa` **está vazio** → **FIM** · None → segue | 2 |
| 2 | If/Else | `Tags` inclui `fila-wa` → Math `Tentativas WhatsApp` + 1 · None → Math `Tentativas telefone` + 1 (os dois lados seguem para 3) | 3 |
| 3 | Math | `Total de ligações` + 1 | 3b |
| 3b | Remove Contact Tag | `fila-quente` — incondicional, **depois** do nó 2 (que lê `fila-wa`). Retoque de 21/09: falta na versão publicada; sem ele o lead que deu sinal e não atendeu fica na `Fila Quente` para sempre | 4 |
| 4 | If/Else múltiplo (Condition) | por `Resultado da tentativa`: 6 ramos abaixo | ramo |

**Ramo `Atendeu`**

| # | Ação | Configuração exata |
|---|---|---|
| A1 | If/Else | `Tags` inclui `fila-wa` → Math `Conexões WhatsApp` + 1 · None → Math `Conexões telefone` + 1 |
| A2 | Math | `Total de conexões` + 1 — **retoque: este nó não existe/não grava na versão publicada** (24 execuções, `Conexões telefone` = 8, `Total de conexões` vazio) |
| A3 | Update Contact Field | `WA não atendidas seguidas` = `0` |
| A4 | Add Contact Tag | `conectado-hoje` |
| A5 | Remove Contact Tag | `fila-tel`, `fila-wa` |
| A6 | Update Opportunity | Etapa → `AGENDAR` (status fica `open`) |
| A7 | Update Contact Field | `Data conectado` = data atual |
| A7b | Date/Time Formatter | entrada `{{right_now}}` · formato `HH` — **só depois de criar `Hora da conexão`** |
| A7c | Update Contact Field | `Hora da conexão` = saída do A7b |
| A8 | Add Task | Título `[CONECTADO] Qualificar e agendar` · vence hoje · Atribuir `Contact Owner` |
| A9 | Add Note | `Atendeu na T{{contact.tentativa_n}}` |

**Ramos `Caixa Postal` e `Não atendeu` (idênticos, montar duas vezes)**

| # | Ação | Configuração exata |
|---|---|---|
| C1 | If/Else | `Tags` inclui `fila-wa` → Math `WA não atendidas seguidas` + 1 · None → Update `WA não atendidas seguidas` = `0` |
| C2 | Remove Contact Tag | `fila-tel`, `fila-wa` |
| C3 | Add Contact Tag | `limpar-tarefas` |

**Ramo `Número errado`**

| # | Ação | Configuração exata |
|---|---|---|
| N1 | Add Contact Tag | `telefone-invalido` |
| N2 | Remove Contact Tag | `fila-tel`, `fila-wa` |
| N3 | If/Else | `Email` não está vazio **OU** `Instagram` não está vazio → Update Opportunity status = `abandoned` + Add Tag `nutricao-90d` · None → Update Opportunity status = `lost` |
| N4 | Internal Notification | ao gestor: `Telefone inválido: {{contact.name}} — revisar a fonte da lista` |

**Ramo `Pediu retorno`**

| # | Ação | Configuração exata |
|---|---|---|
| R1 | Update Contact Field | `Prioridade` = `5` |
| R2 | Remove Contact Tag | `fila-tel`, `fila-wa` |
| R3 | Add Contact Tag | `fila-quente` |
| R4 | Add Task | `[RETORNO] Ligar de volta` · vence: `Data de retorno` (se vazio, amanhã) · Atribuir `Contact Owner` |

**Ramo `Não ligar`**

| # | Ação | Configuração exata |
|---|---|---|
| L1 | Add Contact Tag | `nao-perturbe` |
| L2 | Set Contact DND | ligado, todos os canais |
| L3 | Remove Contact Tag | `fila-tel`, `fila-wa`, `fila-quente` |
| L4 | Remove from Workflow | `Cadência 12x30`, `Cadência Inbound`, `Reengajamento 90 dias`, `Qualificação por IA no WhatsApp` (os que já existirem) |
| L5 | Update Opportunity | status = `lost` |
| L6 | Add Note | `Opt-out registrado em {{right_now}}` |

**Teste:** os 6 ramos do lado telefone já foram confirmados por log em
19/09. Faltam A2 e 3b: mude `Resultado da tentativa` = `Atendeu` num contato
de teste em `CONECTAR` e confira `Total de conexões` subir.

---

## W5 · Pós-agendamento — `build-wesales.md` 5 — PUBLICADO, nó 4 não grava

**Gatilho:** `Appointment Status` → Calendário `Reunião com closer` · Status `Confirmed` (marque também `Booked`/`New` se a tela listar separado). **Não** use `Customer Booked Appointment`.

| Configuração | Valor |
|---|---|
| Allow Re-entry | Ligado (reagendamento) |
| Janela | Sem janela |

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 1 | Update Opportunity | Etapa → `NEGOCIAR` (status `open`) | 2 |
| 2 | Update Contact Field | `Data agendado` = data atual | 3 |
| 3 | Remove from Workflow | `Cadência 12x30` · `Qualificação por IA no WhatsApp` · `Recuperação de No-show` · `SLA do Closer — No-show` (os que existirem) | 4 |
| 4 | **Nota de qualificação** — ver bloco abaixo | Math em série (seção 9.1) | 5 |
| 5 | Update Contact Field | `Prioridade` = `5` | 6 |
| 6 | Add Note | modelo da seção 5 (`build-wesales.md`), com as chaves da seção 0.3 | 7 |
| 7 | Send WhatsApp | confirmação (texto na seção 5) | 8 |
| 8 | Wait → relativo ao início do compromisso | 24h antes → Send WhatsApp lembrete | 9 |
| 9 | Wait | 3h antes → Send WhatsApp lembrete | 10 |
| 10 | Wait | 30 min antes → Send WhatsApp lembrete curto | 11 |
| 11 | Assign to User | closer dono do horário | 12 |
| 12 | Internal Notification | e-mail + SMS ao closer (SMS interno é permitido) | fim |

**Nó 4 — como montar a nota (o que a IA fez como "custom code" e não grava):**

```
Update Contact Field: Nota de qualificação = 0
Bloco A
  If Clientes novos por mês = "10"     → Math Nota + 3
  If Clientes novos por mês = "11-30"  → Math Nota + 6
  If Clientes novos por mês = "31-100" → Math Nota + 8
  If Clientes novos por mês = "+101"   → Math Nota + 10
  If Tem time comercial = "Só dono" → +3 · "1-5" → +7 · "6-10" → +9 · "+10" → +10
  If Quem atende os leads = "Ninguém fixo" → +10 · "Dono" → +7 · "Vendedor" → +5 · "SDR" → +3
Bloco B
  If Investe em anúncios = "Sim" → +13 · "Já investiu e parou" → +9 · "Nunca" → +4
  If Investimento mensal em anúncios = "Acima de 10k" → +12 · "5k a 10k" → +10 · "1k a 5k" → +6 · "Até 1k" → +2
     ⚠ G-04: o Meta grava "Abaixo de 5k", "Até R$ 1.000", "Não invisto nada ainda" — só monte este
       If/Else depois de o dono decidir a Tabela H de CONFERENCIA-CAMPOS.md
Bloco C
  If Budget = "Tem" → +15 · "Precisa aprovar" → +9 · "Não tem" → +0
  If Decisor = "Sim" → +15 · "Influencia" → +8 · "Não decide" → +2
  If Prazo = "Pra ontem" → +15 · "Espera 30 dias" → +11 · "Este ano" → +6 · "Sem prazo" → +2
     ⚠ G-04: o Meta grava a resposta em Urgência, não em Prazo
Corte: If Budget = "Não tem" E Prazo = "Sem prazo" → Add Tag nutricao-90d + Update Opportunity status = abandoned
```

Cada linha é um `If/Else` (campo · é · opção exata) cujo ramo Branch tem um
`Math: Nota de qualificação + N` e cujo None segue para o próximo If/Else.
São ~25 nós — é o preço de não usar código. Alternativa: manter o nó de
código da IA, mas ele precisa ler as chaves da seção 0.3 e **escrever** em
`nota_de_qualificao`; hoje não escreve (3 leads passaram, nota vazia nos 3).

**Retoques na versão publicada:** nó 4 (acima); nó 6 — a nota gravada em
19/09 saiu com `nota /100`, `Empresa`, `Segmento`, `Agendado por`, `Para`,
`conexões` e `T.` em branco: conferir cada merge field contra a seção 0.3
(`{{user.name}}` e `{{appointment.start_time}}` só existem se o gatilho for
de agendamento; `{{contact.empresa}}` só se o formulário gravar em
`Empresa`).

**Teste:** marque um agendamento em `Reunião com closer` para `Teste Não
Atende` → etapa `NEGOCIAR`, `Data agendado`, `Prioridade` 5, **`Nota de
qualificação` preenchida**, nota com todos os campos.

---

## W6 · Loop do closer — `build-wesales.md` 5.1 — REFAZER

Estado: criado pela IA como `Post-Meeting Closer Loop`, rascunho, com
condições em `Tags`/`Rescheduled`/`Opportunity status`/`score`/`Last
appointment at`. Teste por API em 21/09 18:44 UTC não disparou. Apague os nós
da IA e monte:

**Gatilho:** `Contact Changed` → Filtro: `Reunião foi qualificada` · `Foi alterado`. Só esse (apague o filtro `Tags`).

| Configuração | Valor |
|---|---|
| Allow Re-entry | Ligado |
| Stop on Response | Desligado |
| Janela | Sem janela |

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 1 | If/Else | `Reunião foi qualificada` **está vazio** → **FIM** · None → segue | 2 |
| 2 | Update Contact Field | `Data do veredito do closer` = data atual | 3 |
| 3 | Add Note | `Veredito do closer: {{contact.reunio_foi_qualificada}} · motivo: {{contact.motivo_da_desqualificao}} · nota do SDR/IA na hora: {{contact.nota_de_qualificao}}` | 4 |
| 4 | If/Else múltiplo (Condition), campo `Reunião foi qualificada` | **= `Sim`** → nenhuma ação, FIM · **= `Parcial`** → Update Opportunity status = `abandoned` → Add Tag `nutricao-90d` · **= `Não`** → nó 4b | 5 |
| 4b | If/Else (dentro do ramo `Não`) | `Motivo da desqualificação` é `Timing errado` → Update Opportunity status = `abandoned` → Add Tag `nutricao-90d` · None → Update Opportunity status = `lost` | 5 |
| 5 | If/Else | `Nota de qualificação` **≥ 70** E `Reunião foi qualificada` é `Não` → Internal Notification ao gestor: `Nota {{contact.nota_de_qualificao}} mas o closer marcou Não ({{contact.motivo_da_desqualificao}}) — revisar a régua da seção 9 com {{contact.name}}.` · None → 6 | 6 |
| 6 | If/Else | `Nota de qualificação` **< 45** E `Reunião foi qualificada` é `Sim` → Internal Notification ao gestor: `Nota baixa ({{contact.nota_de_qualificao}}) mas o closer marcou Sim — a régua pode estar descartando lead bom. Revisar {{contact.name}}.` · None → FIM | fim |

Nenhum ramo muda a **etapa**: a oportunidade fica em `NEGOCIAR`, só o
status muda. Nós 5 e 6 ficam **depois** do 4 na mesma linha (o 4 não os
bloqueia).

**Teste (já preparado em 21/09):** `Teste Atendeu` está com `Nota de
qualificação` = 80, `Reunião foi qualificada` = `Não`, `Motivo` = `Sem fit`.
Depois de publicar, mude `Reunião foi qualificada` para `Parcial` e, 10 s
depois, de volta para `Não` (Re-entry ligado). Esperado: `Data do veredito`
= hoje, nota "Veredito do closer: Não · motivo: Sem fit · nota 80",
oportunidade `lost` (etapa `NEGOCIAR`), notificação do nó 5 ao gestor.

---

## W7 · Registro de Comparecimento — `build-wesales.md` 5.2

**Gatilho:** `Appointment Status` → Calendário `Reunião com closer` · Status `Showed`

| Configuração | Valor |
|---|---|
| Allow Re-entry | Ligado |
| Janela | Sem janela |

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 1 | If/Else | `Data compareceu` **está vazio** → segue · None → **FIM** | 2 |
| 2 | Update Contact Field | `Data compareceu` = data atual | 3 |
| 3 | Update Contact Field | `Nº de no-shows` = `0` | 4 |
| 4 | Add Note | `Compareceu à reunião · {{right_now}}` | fim |

Sem mudança de etapa. **Teste:** marque `Showed` no agendamento do contato de teste → os 3 campos.

---

## W8 · Recuperação de No-show — `build-wesales.md` 5.3 — rascunho na tela

**Gatilho:** `Appointment Status` → Calendário `Reunião com closer` · Status `No Show`

| Configuração | Valor |
|---|---|
| Allow Re-entry | Ligado |
| Stop on Response | **Ligado** |
| Janela | 08:30–18:30, seg–sex, fuso da subconta |

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 1 | If/Else | `Pipeline stage` é `[FUNIL DE VENDAS] - NEGOCIAR` **E** `Opportunity status` é `open` → segue · None → **FIM** | 2 |
| 2 | Math | `Nº de no-shows` + 1 | 3 |
| 3 | If/Else | `Nº de no-shows` **≥ 2** → ramo Descarte · None → ramo Recuperação | ramo |

**Ramo Descarte**

| # | Ação | Configuração exata |
|---|---|---|
| D1 | Remove Contact Tag | `fila-tel` |
| D2 | Add Contact Tag | `limpar-tarefas` |
| D3 | Update Opportunity | status = `lost` (etapa fica `NEGOCIAR`) |
| D4 | Add Note | `Descartado após {{contact.n_de_noshows}}º no-show seguido sem reagendar — regra de proteção de agenda do closer (R-12)` |
| D5 | Internal Notification | ao gestor: `{{contact.name}} descartado automaticamente após {{contact.n_de_noshows}}º no-show — nenhuma ação necessária, é a regra de proteção de agenda` |

**Ramo Recuperação**

| # | Ação | Configuração exata |
|---|---|---|
| R1 | Send WhatsApp | texto `NS-1` (`biblioteca-mensagens.md`) |
| R2 | Update Contact Field | `Template usado` = `NS-1` |
| R3 | Add Contact Tag | `fila-tel` (→ depois, quando o Contador existir: Add Tag `toque`) |
| R4 | Add Task | `[CADENCIA] NS1 · Ligar (telefone) — Recuperação de no-show` · vence hoje · `Contact Owner` |
| R5 | Wait → Until specific time | dia seguinte (D1) 10:00 |
| R6 | If/Else | `Pipeline stage` é `[FUNIL DE VENDAS] - NEGOCIAR` **E** `Opportunity status` é `open` **E** `Tags` não inclui `nao-perturbe` **E** `Tags` não inclui `pausado` → segue · None → Remove from Workflow (este) |
| R7 | Add Contact Tag | `fila-tel` |
| R8 | Add Task | `[CADENCIA] NS2 · Ligar (telefone) — Recuperação de no-show` · vence hoje · `Contact Owner` |
| R9 | Wait → Until specific time | D3 15:00 |
| R10 | If/Else | mesmo do R6 |
| R11 | Add Contact Tag | `fila-tel` |
| R12 | Add Task | `[CADENCIA] NS3 · Ligar (telefone) — Recuperação de no-show` · vence hoje · `Contact Owner` |
| R13 | Wait → Time Delay | 1 dia |
| R14 | If/Else | `Pipeline stage` é `[FUNIL DE VENDAS] - NEGOCIAR` **E** `Opportunity status` é `open` → segue · None → Remove from Workflow (este) |
| R15 | Send WhatsApp | texto `NS-2` |
| R16 | Update Contact Field | `Template usado` = `NS-2` |
| R17 | Update Contact Field | `Resultado da tentativa` = vazio |
| R18 | Remove Contact Tag | `fila-tel` |
| R19 | Add Contact Tag | `nutricao-90d` |
| R20 | Update Opportunity | status = `abandoned` (etapa fica `NEGOCIAR`) |

**Teste:** com os Waits reduzidos a minutos, marque `No Show` no agendamento de um contato de teste em `NEGOCIAR` → `Nº de no-shows` 1, `fila-tel`, tarefa NS1. Segundo `No Show` → status `lost`, nota, aviso.

---

## W9 · SLA do Closer — No-show — `build-wesales.md` 5.4

**Gatilho:** `Appointment Status` → Calendário `Reunião com closer` · Status `No Show` (o mesmo do W8 — são dois workflows de propósito)

| Configuração | Valor |
|---|---|
| Allow Re-entry | Ligado |
| Stop on Response | Desligado |
| Janela | Sem janela |

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 1 | If/Else | `Pipeline stage` é `[FUNIL DE VENDAS] - NEGOCIAR` **E** `Opportunity status` é `open` → segue · None → FIM | 2 |
| 2 | If/Else | `Nº de no-shows` **≥ 2** → FIM · None → segue | 3 |
| 3 | Internal Notification | ao closer (`Contact Owner`): `{{contact.name}} não compareceu à reunião de {{appointment.start_time}}. A recuperação automática (NS1) já dispara em instantes — se preferir reagendar você mesmo agora, é mais rápido para o lead e evita o SDR ligar à toa.` | 4 |
| 4 | Wait → Time Delay | 2 horas | 5 |
| 5 | If/Else | mesmo do nó 1 → segue · None → FIM | 6 |
| 6 | Internal Notification | ao gestor: `Closer não deu retorno em 2h após o no-show de {{contact.name}} ({{appointment.start_time}}) — a recuperação automática (NS1) já está tentando reconectar, mas vale conferir com o closer.` | fim |

---

## W10 · Qualificação por IA no WhatsApp — `build-wesales.md` 6

**Sem gatilho.** Entra só por `Add to Workflow` (Cadência 12x30, nó 2.7).

| Configuração | Valor |
|---|---|
| Allow Re-entry | Desligado |
| Stop on Response | **Desligado** |
| Janela | 08:30–20:00, seg–sáb |

**Caminho A (recomendado, exige Conversation AI no plano)**

| # | Ação | Configuração exata |
|---|---|---|
| 1 | Conversation AI | Canal WhatsApp · Modo Query + Appointment Booking · Calendário `Reunião com closer` · uma pergunta por mensagem, máx. 8 · mapeamento: pergunta → campo (seção 0.3, coluna Qualificação) · prompt: o bloco de código da seção 6 do `build-wesales.md`, colado inteiro |
| 2 | Update Contact Field | `Qualificação` = `IA Whatsapp` (W minúsculo — opção real) |
| 3 | Nota de qualificação | mesmo bloco de Math do W5 nó 4 |
| 4 | If/Else | `Nota de qualificação` ≥ 45 → Add Tag `fila-quente` → Update `Prioridade` = `5` → Internal Notification ao SDR: `lead qualificado pela IA, ligar hoje` |
| 5 | If/Else | `Nota de qualificação` < 25 **E** `Budget` é `Não tem` → Update Opportunity status = `abandoned` → Add Tag `nutricao-90d` |

**Caminho B (sem Conversation AI):** 8 blocos `Send WhatsApp (pergunta)` →
`Wait → Contact Replied, 24h` → `Update Contact Field` (campo da pergunta),
na ordem do prompt; no tempo limite pula para a próxima. Depois, nós 2–5.

**Estado na tela:** rascunho — confirmar se é o placeholder vazio criado
para o Mestre de saída apontar, ou se já tem o nó de IA dentro.

---

## W11 · Cadência 12x30 — `build-wesales.md` 2 — rascunho, 0 inscritos

**Gatilho:** `Opportunity Stage Changed` → Pipeline `FUNIL DE VENDAS` · Para a etapa `CONECTAR` · Filtros: `Tags` **não inclui** `cad-inbound` **E** `Tags` **não inclui** `reengajamento-ativo`

| Configuração | Valor |
|---|---|
| Janela | 08:30–18:30 · seg–sex · fuso da subconta |
| Stop on Response | **Ligado** |
| Allow Re-entry | **Desligado** (D-06) |
| Contato em múltiplos workflows | permitido |

**Antes de montar:** criar `Toques na semana` (para 2.5c/2.5d) e decidir
`{{right_now}}` (seção 0.3). Trigger Link `Agendar com o closer` já existe.

### Nó 0 — inicialização (uma vez)

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 0.0 | If/Else | `Phone` **está vazio** → 0.0b · None → 0.1 | |
| 0.0b | Add Contact Tag | `telefone-invalido` | 0.0c |
| 0.0c | If/Else | `Site` não vazio **OU** `Instagram` não vazio → Update Opportunity status = `abandoned` → Add Tag `nutricao-90d` → Remove from Workflow (este) · None → Update Opportunity status = `lost` → Internal Notification ao gestor: `Lead sem telefone: {{contact.name}} — revisar a fonte da lista antes de qualquer tentativa` → Remove from Workflow (este) | fim |
| 0.1 | Update Contact Field | `Tentativa nº` = `0` | 0.2 |
| 0.2 | Update Contact Field | `WA não atendidas seguidas` = `0` | 0.3 |
| 0.3 | Update Contact Field | `Resultado da tentativa` = vazio | 0.4 |
| 0.4 | If/Else | `Permissão WhatsApp` está vazio → Update `Permissão WhatsApp` = `Não solicitado` | 0.5 |
| 0.5 | Update Contact Field | `Prioridade` = `3` | 0.6 |
| 0.6 | Update Contact Field | `Entrada em` = `{{right_now}}` (ou `sim`) | 0.7 |
| 0.7 | If/Else | `Assigned User` está vazio → 0.7b · None → M1.1 | |
| 0.7b | Assign to User | modo `Round Robin` · usuários: todos os SDRs (hoje só o dono) | M1.1 |

### M1 — abertura com teste A/B (D1 08:45)

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| M1.0 | Wait → Until specific time | 08:45 | M1.1 |
| M1.1 | If/Else (portão) | `Pipeline stage` é `[FUNIL DE VENDAS] - CONECTAR` E `Opportunity status` é `open` E `Tags` não inclui `nao-perturbe` E `Resultado da tentativa` não é `Não ligar` → M1.2 · None → 3b | |
| M1.2 | Split | Caminho A 50% · Caminho B 50% | |
| M1.3a | Send WhatsApp | texto `M1-a` | M1.4a |
| M1.4a | Update Contact Field → Add Contact Tag | `Template usado` = `M1-a` → `toque` | M1.5 |
| M1.3b | Send WhatsApp | texto `M1-b` | M1.4b |
| M1.4b | Update Contact Field → Add Contact Tag | `Template usado` = `M1-b` → `toque` | M1.5 |
| M1.5 | Wait → Contact Replied | tempo limite 2h (respondeu → Stop on Response tira do fluxo) | T1 |

Ligue **as duas pontas** do Split ao M1.5 manualmente.

### Bloco padrão de uma tentativa T{n} — repita 12 vezes

Valores por tentativa na tabela seguinte. `{n}` = número; canal = telefone ou WhatsApp.

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 1 | Wait → Time Delay | delta em dias da tabela (0 d = sem este nó) | 2 |
| 2 | Wait → Until specific time | horário da tabela | 2.5 |
| 2.5 | If/Else | `Tags` inclui `pausado` → 2.5b · None → 2.5c | |
| 2.5b | Wait → Time Delay | 1 dia → **liga de volta ao 2.5** | 2.5 |
| 2.5c | If/Else | `Toques na semana` **≥ 6** → 2.5d · None → 3 | |
| 2.5d | Wait → Time Delay | 1 dia → **liga de volta ao 2.5c** | 2.5c |
| 3 | If/Else (portão) | `Pipeline stage` é `[FUNIL DE VENDAS] - CONECTAR` E `Opportunity status` é `open` E `Tags` não inclui `nao-perturbe` E `Resultado da tentativa` não é `Não ligar` E (só telefone) `Tags` não inclui `telefone-invalido` → 4 ou 5 · None → 3b | |
| 3b | Remove Contact Tag → Add Contact Tag → Remove from Workflow | `fila-tel`, `fila-wa`, `fila-quente` → `limpar-tarefas` → este | fim |
| 4 | If/Else (só tentativas WhatsApp) | `Permissão WhatsApp` é `Sim` E `WA não atendidas seguidas` < 2 → ramo WA · None → ramo telefone (mesmos nós 5–10 com `fila-tel` e título telefone) | 5 |
| 5 | Update Contact Field | `Resultado da tentativa` = vazio · `Tentativa nº` = `{n}` | 5c (só T1) / 6 |
| 5c | (só T1) Update Contact Field | `1ª tentativa em` = `{{right_now}}` (ou `sim`) | 5d |
| 5d | (só T1) Remove Contact Tag | `atraso-1a-tentativa` | 6 |
| 6 | Add Contact Tag | `fila-tel` ou `fila-wa` | 7 |
| 7 | Add Task → Add Contact Tag | título da tabela · vence hoje no horário da tentativa · Atribuir `Contact Owner` → tag `toque` | 8 |
| 8 | Wait → Condition | `Resultado da tentativa` não está vazio · tempo limite: hoje 18:30 | 9 |
| 9 | Remove Contact Tag | `fila-tel`, `fila-wa` | 10 |
| 10 | If/Else | `Resultado da tentativa` é `Atendeu` OU `Pediu retorno` OU `Número errado` OU `Não ligar` → Remove from Workflow (este) · None → 10b | |
| 10b | If/Else | `Resultado da tentativa` está vazio (tempo limite) → Update `Resultado da tentativa` = `Não atendeu` → Add Tag `limpar-tarefas` · None → próxima tentativa | T{n+1} |

| T | Delta (nó 1) | Horário (nó 2) | Canal | Tag | Título da tarefa |
|---|---|---|---|---|---|
| 1 | 0 d | 10:30 | telefone | `fila-tel` | `[CADENCIA] T1 · Ligar (telefone)` |
| 2 | 0 d | 16:10 | WhatsApp | `fila-wa` | `[CADENCIA] T2 · Ligar (WhatsApp)` |
| 3 | 1 d | 09:20 | telefone | `fila-tel` | `[CADENCIA] T3 · Ligar (telefone)` |
| 4 | 0 d | 17:20 | WhatsApp | `fila-wa` | `[CADENCIA] T4 · Ligar (WhatsApp)` |
| — | depois da T4: nós 2.7a/2.7b (entrada na IA) | | | | |
| 5 | 2 d | 11:00 | WhatsApp | `fila-wa` | `[CADENCIA] T5 · Ligar (WhatsApp)` |
| 6 | 3 d | 09:00 | telefone | `fila-tel` | `[CADENCIA] T6 · Ligar (telefone)` |
| 7 | 0 d | 15:30 | WhatsApp | `fila-wa` | `[CADENCIA] T7 · Ligar (WhatsApp)` |
| 8 | 3 d | 11:40 | telefone | `fila-tel` | `[CADENCIA] T8 · Ligar (telefone)` |
| — | depois da T8: M2 | | | | |
| 9 | 4 d | 16:40 | WhatsApp | `fila-wa` | `[CADENCIA] T9 · Ligar (WhatsApp)` |
| 10 | 6 d | 10:15 | telefone | `fila-tel` | `[CADENCIA] T10 · Ligar (telefone)` |
| 11 | 10 d | 09:40 | telefone | `fila-tel` | `[CADENCIA] T11 · Ligar (telefone)` |
| 12 | 0 d | 17:00 | WhatsApp | `fila-wa` | `[CADENCIA] T12 · Ligar (WhatsApp)` |
| — | depois da T12: M3 e encerramento | | | | |

### Entrada na IA (depois do nó 10b da T4)

| # | Ação | Configuração exata |
|---|---|---|
| 2.7a | If/Else | `Tentativa nº` ≥ 2 E `Resultado da tentativa` não é `Atendeu` E `Permissão WhatsApp` não é `Não` → 2.7b · None → T5 |
| 2.7b | Add to Workflow | `Qualificação por IA no WhatsApp` → T5 |

### M2 (depois da T8) e M3 (depois da T12)

| # | Ação | Configuração exata |
|---|---|---|
| M2.0 | Wait → Until specific time | 13:30 |
| M2.1 | If/Else | mesmo portão do M1.1 → M2.2 · None → 3b |
| M2.2 | Send WhatsApp | texto `M2-v1`, com o Trigger Link `Agendar com o closer` inserido pelo `{}` → Custom Values → Trigger Links |
| M2.3 | Update Contact Field → Add Contact Tag | `Template usado` = `M2-v1` → `toque` → T9 |
| M3.0 | Wait → Until specific time | 17:45 |
| M3.1 | If/Else | mesmo portão → M3.2 · None → 3b |
| M3.2 | Send WhatsApp | texto `M3-v1`, com o Trigger Link |
| M3.3 | Update Contact Field → Add Contact Tag | `Template usado` = `M3-v1` → `toque` |
| M3.4 | Update Contact Field | `Resultado da tentativa` = vazio |
| M3.5 | Add Contact Tag | `nutricao-90d` |
| M3.6 | Update Opportunity | status = `abandoned` (etapa fica `CONECTAR`) → FIM |

**Teste (seção 10 do `build-wesales.md`):** mova `Teste Não Atende` para
`CONECTAR` por API. Esperado em segundos: `Tentativa nº` 0, `Prioridade` 3,
`Permissão WhatsApp` `Não solicitado`, `Entrada em`; às 08:45 (ou reduza o
Wait) M1 sai — sem telefone o 0.0 já descarta, então dê um telefone seu
(`APROVADO.md`, linha "Mensagens", ainda `[ ]`).

---

## W12 · Cadência Inbound — `build-wesales.md` 2.10

**Gatilho:** `Opportunity Stage Changed` → Pipeline `FUNIL DE VENDAS` · Para a etapa `CONECTAR` · Filtro: `Tags` **inclui** `cad-inbound`

| Configuração | Valor |
|---|---|
| Janela | 08:30–18:30 · seg–sex · fuso da subconta |
| Allow Re-entry | Desligado |
| Stop on Response | Ligado |

**Nó 0:** igual ao W11 (0.0 a 0.4), com estas diferenças: 0.0c avisa `Lead
inbound sem telefone: {{contact.name}} — revisar o formulário de origem`;
0.5 `Prioridade` = `5`; 0.7 `Add Contact Tag fila-quente`; 0.8/0.8b =
0.7/0.7b do W11 (**mesmo** grupo de round robin).

**MI-0:** Send WhatsApp texto `MI-0` → Update `Template usado` = `MI-0`.

**Bloco por tentativa TI{n}** = bloco do W11 com estas trocas:
- nó 1: `Wait → Time Delay` **relativo** (tabela abaixo); sem nó 2 de horário
- nó 1.5/1.5b: pausa individual com laço de **30 min** (não 1 dia); sem portão de teto (2.5c) — quando ligar o toque aqui, use o padrão "pula e registra" da Interceptação, não represar
- nó 6 (tarefa): título `[CADENCIA] TI{n} · Ligar (telefone|WhatsApp) — Inbound` · vence **agora**
- nó 7 novo: Internal Notification ao SDR: `Lead inbound {{contact.name}} aguardando retorno — TI{n}.`
- nó 8: tempo limite = delta até a tentativa seguinte (não 18:30)
- 5c/5d só na TI1

| TI | Wait (nó 1) | Canal |
|---|---|---|
| 1 | 5 min | telefone |
| 2 | 25 min | telefone |
| 3 | 1 h 30 | WhatsApp (seletor) |
| 4 | 22 h | telefone + WhatsApp (seletor) |
| 5 | 2 dias | telefone |

**Handoff (TI5 sem resposta, no lugar de "próxima tentativa"):** Send
WhatsApp `MI-F` → Update `Template usado` = `MI-F` → Add to Workflow
`Cadência 12x30` → Remove from Workflow (este).

**Pré-requisito:** `Cadência 12x30` publicada (o Add to Workflow precisa dela).

---

## W13 · Interceptação de Sinal — Clique / — Resposta — `build-wesales.md` 2.9.2 / 2.9.3 — PUBLICADOS

**Gatilho Clique:** `Trigger Link Clicked` → Link `Agendar com o closer`
**Gatilho Resposta:** `Customer Replied` → Canal `WhatsApp` · **Filtro (retoque R-17):** corpo da mensagem `Doesn't Contain` cada frase da lista do W14, em E.

| Configuração | Valor |
|---|---|
| Janela | Sem restrição, 24/7 |
| Allow Re-entry | Ligado |
| Stop on Response | Desligado |

| # | Ação | Configuração exata (Clique) | Resposta: o que muda |
|---|---|---|---|
| 1 | Find opportunity | Pipeline `FUNIL DE VENDAS` · "Most recently created" · Not Found → FIM · Found → 2 | igual |
| 2 | If/Else | `Pipeline stage` é `[FUNIL DE VENDAS] - CONECTAR` **E** `Opportunity status` **não é** `lost` → 3 · None → FIM | igual |
| 3 | If/Else | `Tags` inclui `nao-perturbe` → FIM · None → 3c | igual |
| 3c | If/Else | `Toques na semana` ≥ 6 → 9 · None → 4 (só depois de o campo existir) | igual |
| 4 | Update Contact Field | `Prioridade` = `5` | igual |
| 5 | Update Contact Field | `Sinal recebido` = `Clique em link` | `Resposta de mensagem` |
| 6 | Add Contact Tag | `fila-quente` | igual |
| 7 | Add Task → Add Contact Tag | `[CADENCIA] Sinal: clicou no link — ligar agora` · vence agora · `Contact Owner` → `toque` | `[CADENCIA] Sinal: respondeu mensagem — ligar agora` · descrição `Lead respondeu mensagem fora do fluxo normal da cadência. Ligar imediatamente, prioridade 5.` |
| 8 | Internal Notification | ao SDR: `{{contact.first_name}} clicou no link de agendar agora. Prioridade 5.` | `{{contact.first_name}} respondeu agora fora do fluxo normal. Prioridade 5.` |
| 9 | Add Note | `Sinal: clique em link` (vindo do 3c: `Sinal: clique em link (teto de toques da semana batido — sem tarefa nova, ver Toques na semana)`) | `Sinal: resposta de mensagem` |

**Retoque na Resposta (publicada):** adicionar o filtro `Doesn't Contain` no gatilho — sem ele, "pare de mandar mensagem" vira tarefa "ligar agora".

---

## W14 · Opt-out por Palavra-chave — `build-wesales.md` 2.9.5

**Gatilho:** `Customer Replied` → Canal `WhatsApp` · corpo `Contains` (uma linha por frase, ou a lista numa linha se a tela aceitar OU):

`pare de` · `pare com` · `para de mandar` · `para de me mandar` · `não quero mais mensagem` · `não quero mais contato` · `não quero receber mensagem` · `não quero receber mais` · `remove meu contato` · `tira meu número` · `descadastr` · `cancelar inscri` · `não me liga mais` · `não me mande mais` · `sai da lista` · `me tira da lista` · `unsubscribe`

**Nunca** `pare`, `stop`, `não quero mais` soltos (casam "parece ótimo"). Esta lista e a do filtro do W13-Resposta são a mesma.

| Configuração | Valor |
|---|---|
| Janela | Sem restrição, 24/7 |
| Allow Re-entry | Ligado |
| Stop on Response | Desligado |

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 1 | Find opportunity | Pipeline `FUNIL DE VENDAS` · "Most recently created" · **os dois ramos seguem** para 2 | 2 |
| 2 | Add Contact Tag | `nao-perturbe` | 3 |
| 3 | Set Contact DND | ligado, todos os canais | 4 |
| 4 | Remove Contact Tag | `fila-tel`, `fila-wa`, `fila-quente` | 5 |
| 5 | Remove from Workflow | `Cadência 12x30` · `Cadência Inbound` · `Reengajamento 90 dias` · `Qualificação por IA no WhatsApp` · `Interceptação de Sinal — Clique` · `Interceptação de Sinal — Resposta` (os que existirem) | 6 |
| 6 | If/Else | oportunidade encontrada **E** `Pipeline stage` é `[FUNIL DE VENDAS] - CONECTAR` **E** `Opportunity status` é `open` → Update Opportunity status = `lost` · None → Internal Notification ao `Contact Owner`: `Opt-out por palavra-chave: {{contact.name}} pediu para parar, oportunidade já em {{opportunity.pipeline_stage}}/{{opportunity.status}} — DND ligado, revisar se o negócio segue antes de qualquer novo contato` | 6b |
| 6b | Internal Notification (**sempre**) | ao `Contact Owner`: `Opt-out por palavra-chave: {{contact.name}} — DND ligado e saiu de todas as réguas. Mensagem que disparou: revisar no histórico. Se foi falso positivo, desligar o DND na mão é a única volta.` | 7 |
| 7 | Add Note | `Opt-out por palavra-chave detectado em {{right_now}} · DND ligado · removido de todas as réguas automáticas` | fim |

---

## W15 · Alerta de Speed-to-lead — `build-wesales.md` 2.11

**Gatilho:** `Opportunity Stage Changed` → Pipeline `FUNIL DE VENDAS` · Para a etapa `CONECTAR` (sem filtro de tag — dispara junto com as duas cadências)

| Configuração | Valor |
|---|---|
| Allow Re-entry | Ligado |
| Janela | Sem janela |
| Stop on Response | Desligado |

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 0 | If/Else | `Tags` inclui `cad-inbound` → 1a · None → 1b | |
| 1a | Wait → Time Delay | 15 min | 2 |
| 1b | Wait → Time Delay | 1 hora | 2 |
| 2 | If/Else | `Pipeline stage` é `[FUNIL DE VENDAS] - CONECTAR` **E** `Opportunity status` é `open` **E** `1ª tentativa em` está vazio **E** `Tags` não inclui `pausado` → 3 · None → FIM | 3 |
| 3 | Add Contact Tag | `atraso-1a-tentativa` | 4 |
| 4 | Internal Notification | ao gestor: `{{contact.name}} está há mais de 1h em cadência sem a 1ª tentativa. Entrada: {{contact.entrada_em}}.` | 5 |
| 5 | Add Note | `Alerta speed-to-lead: sem 1ª tentativa 1h após a entrada · {{right_now}}` | fim |

Ligue os dois Waits (1a e 1b) ao **mesmo** nó 2.

---

## W16 · Reengajamento 90 dias — `build-wesales.md` 2.12

**Gatilho:** `Contact Tag Added` → Tag `nutricao-90d`

| Configuração | Valor |
|---|---|
| Allow Re-entry | Ligado |
| Janela | 08:30–18:30 · seg–sex · fuso da subconta |
| Stop on Response | Ligado |

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 1 | Wait → Time Delay | 90 dias | 2 |
| 2 | If/Else | `Opportunity status` é `abandoned` **E** `Tags` inclui `nutricao-90d` **E** `Tags` não inclui `nao-perturbe` → 3 · None → Remove from Workflow (este) | 3 |
| 3 | Update Contact Field (6 campos) | `Tentativa nº` = `0` · `WA não atendidas seguidas` = `0` · `Resultado da tentativa` = vazio · `Prioridade` = `3` · `Entrada em` = `{{right_now}}` (ou `sim`) · `1ª tentativa em` = vazio | 4 |
| 4 | Remove Contact Tag → Remove Contact Tag → Add Contact Tag → Add Contact Tag | `nutricao-90d` → `cad-inbound` → `cad-outbound` → `reengajamento-ativo` | 5 |
| 5 | Update Opportunity | Etapa → `CONECTAR` **E** status → `open` (no mesmo nó) | 6 |
| 6 | Send WhatsApp → Update Contact Field | texto `RE-1` → `Template usado` = `RE-1` | 7 |
| 7 | Wait → Contact Replied | tempo limite 2h | TR1 |

**TR1–TR4:** bloco padrão do W11 (com 2.5/2.5b, 3/3b, 10/10b; sem 2.5c até o campo existir), título `[CADENCIA] TR{n} · Ligar (canal) — Reengajamento`, 5c/5d só na TR1:

| TR | Delta | Horário | Canal | Tag |
|---|---|---|---|---|
| 1 | 0 d | 14:00 | telefone | `fila-tel` |
| 2 | 3 d | 10:00 | WhatsApp | `fila-wa` |
| 3 | 4 d | 15:30 | telefone | `fila-tel` |
| 4 | 3 d | 11:00 | telefone | `fila-tel` |

**Fim da TR4 sem resposta:** Send WhatsApp `RE-2` → Update `Template usado`
= `RE-2` → Update `Resultado da tentativa` = vazio → Add Tag `nutricao-90d`
(reabre o relógio de 90 dias) → Update Opportunity status = `abandoned`.

---

## W17 · Lead Esquecido em NOVO LEAD — `build-wesales.md` 2.20 (F-05)

**Gatilho:** `Opportunity Stage Changed` → Pipeline `FUNIL DE VENDAS` · Para a etapa `NOVO LEAD`

| Configuração | Valor |
|---|---|
| Allow Re-entry | Ligado |
| Janela | Sem janela, 24/7 |
| Stop on Response | Desligado |

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 1 | Wait → Time Delay | 24 horas | 2 |
| 2 | If/Else | `Pipeline stage` é `[FUNIL DE VENDAS] - NOVO LEAD` **E** `Opportunity status` é `open` → 3 · None → FIM | 3 |
| 3 | Add Contact Tag | `novo-lead-estagnado` | 4 |
| 4 | Internal Notification | ao gestor: `{{contact.name}} está há mais de 24h em NOVO LEAD sem revisão. Origem: {{contact.source}}.` | 5 |
| 5 | Add Note | `Alerta de saúde: NOVO LEAD sem revisão em 24h · {{right_now}}` | fim |

**Pré-requisito:** tag `novo-lead-estagnado` (`APROVADO.md`, `[ ]`). Depois de
publicar, `Add to Workflow` em massa nos leads já parados.

---

## W17b · Fila Travada — `build-wesales.md` 2.21 (F-05 peça 2)

**Gatilhos (dois, em OU):** `Contact Tag Added` → `fila-tel` · `Contact Tag Added` → `fila-wa`

| Configuração | Valor |
|---|---|
| Allow Re-entry | Ligado |
| Janela | Sem janela, 24/7 |
| Stop on Response | Desligado |

| # | Ação | Configuração exata | Vai para |
|---|---|---|---|
| 0 | Remove Contact Tag | `fila-travada` | 1 |
| 1 | Wait → Until specific time | **19:00 do mesmo dia** (não "24h depois" — tentativas vizinhas ficam a menos de 24h uma da outra) | 2 |
| 2 | If/Else | `Tags` inclui `fila-tel` **OU** `Tags` inclui `fila-wa` → 3 · None → FIM | 3 |
| 3 | Add Contact Tag | `fila-travada` | 4 |
| 4 | Internal Notification | ao gestor: `{{contact.name}} está com fila-tel/fila-wa presa desde antes de hoje às 18:30 — o nó 9 da cadência não rodou. Tentativa nº {{contact.tentativa_n}}.` | 5 |
| 5 | Add Note | `Alerta de saúde: fila-tel/fila-wa travada, nó 9 não removeu até 18:30 · {{right_now}}` | fim |

**Pré-requisito:** tag `fila-travada` (`APROVADO.md`, `[ ]`). Lista 8.21 filtra por ela.

---

## W18 · Monitor de Capacidade — `build-wesales.md` 2.15

**Gatilho:** `Scheduler` (sem contato) · seg–sex · **11:00** e **15:00** · fuso `America/Sao_Paulo`

| # | Ação | Configuração exata |
|---|---|---|
| 1 | Internal Notification | ao gestor: `Confira "Estouro da Fila" no dashboard (ou a lista "Fila do Dia — Total") — a meta é 100 tarefas/dia.` + link da lista 8.16 |

Pré-requisito: lista `Fila do Dia — Total` (seção 8.16) e, se o plano tiver, Custom Metric `Estouro da Fila` = contagem(`fila-tel` OU `fila-wa`) − 100.

---

## W19 · Higiene de Número — Validação Automática (opcional) — `build-wesales.md` 2.16

Só depois de ligar **Number Validation** (Configurações → Telefone) e confirmar
custo/plano. **Gatilho:** `Number Validation` (sem filtro). Allow Re-entry
ligado, sem janela.

| # | Ação | Configuração exata |
|---|---|---|
| 1 | If/Else | status da validação é `Invalid` → ramo A · None → 2 |
| 2 | If/Else | status é `Landline` → ramo B · None → FIM |
| A1 | Add Contact Tag | `telefone-invalido` |
| A2 | If/Else | (`Pipeline stage` é `[FUNIL DE VENDAS] - NOVO LEAD` OU `- CONECTAR`) **E** `Opportunity status` é `open` → A3 · None → A4 |
| A3 | If/Else | `Site` ou `Instagram` não vazio → Update Opportunity status = `abandoned` + Add Tag `nutricao-90d` · None → Update Opportunity status = `lost` |
| A4 | Internal Notification | ao gestor: `Telefone inválido (validação automática): {{contact.name}} — revisar a fonte da lista` |
| B1 | If/Else | `Permissão WhatsApp` está vazio OU é `Não solicitado` → Update `Permissão WhatsApp` = `Não` · None → FIM |

Nomes dos status (`Invalid`/`Landline`) a confirmar na tela.

---


---

# PARTE 3 — OPERAÇÃO (a dinâmica de alta produtividade)

A máquina só rende se cada papel mexer **apenas** no que é dele. A regra
mais importante desta parte: o SDR preenche **um** campo por tentativa
(`Resultado da tentativa`) e tudo o mais acontece sozinho. Quem "ajuda" a
automação à mão — movendo etapa, aplicando tag de fila, criando tarefa
`[CADENCIA]` — quebra a contagem e o roteamento sem ver erro nenhum.

## 3.1 O dia do SDR

Meta do briefing: **100 ligações/dia** com ~10 leads novos/dia
(`briefing-sdr.md`). Os horários da cadência (tabela do W11) concentram
telefone de manhã e WhatsApp à tarde — o dia abaixo segue essa forma.

| Hora | O que fazer | Onde |
|---|---|---|
| 08:30 | Abrir as 4 listas favoritas, nesta ordem: `Fila Quente` → `Retornos` → `Fila Telefone Hoje` → `Fila WhatsApp Hoje`. Não pular a ordem: `Fila Quente` tem quem deu sinal ontem à noite | 1.7 |
| 08:30–08:45 | Promover para `CONECTAR` os leads de `NOVO LEAD` com telefone válido (é a **única** mudança de etapa manual do SDR; decisão G-03 pode automatizar) | Oportunidades |
| 09:00–12:00 | Bloco de telefone: `Fila Telefone Hoje` de cima para baixo (já vem por `Prioridade` desc, `Tentativa nº` asc — lead novo primeiro, porque converte mais) | 8.2 |
| a cada ligação | Abrir o contato → gravar **`Resultado da tentativa`** (um dos 6 valores) e **nada mais**. O Pós-ligação (W4) faz o resto em segundos: contadores, tags, etapa, tarefa | contato |
| se `Atendeu` | Abrir o link do calendário `Reunião com closer` na mesma tela → preencher o formulário `Qualificação SDR` **enquanto fala** (perguntas na ordem do `script-de-ligacao.md`) → escolher o horário → enviar. Isso dispara o W5 (etapa `NEGOCIAR`, nota, confirmação ao lead) | 1.4 / 1.5 |
| se `Pediu retorno` | Gravar `Data de retorno` (e `Hora do retorno`, quando existir) **antes** do resultado — a tarefa `[RETORNO]` vence nessa data | contato |
| se `Não ligar` | Só quando o lead **pediu**. Liga DND em todos os canais e marca `lost` — não tem volta automática | contato |
| se `Número errado` | Só depois de confirmar (recado da operadora, pessoa diz que não é). Vai para nutrição se houver e-mail/Instagram, senão `lost` | contato |
| 12:00–13:30 | Conversas: responder quem respondeu (W13 já criou tarefa "ligar agora" e pôs em `Fila Quente`) | Conversas |
| 13:30 | M2 sai sozinha para quem está no D10 — nada a fazer | — |
| 14:00–17:30 | Bloco de WhatsApp: `Fila WhatsApp Hoje` (só aparece quem tem `Permissão WhatsApp = Sim`); resto do telefone | 8.3 / 8.2 |
| durante o dia | Notificação "clicou no link" / "respondeu agora" (W13) ou "lead inbound aguardando — TI{n}" (W12): **ligar em até 10 min**, é o único caso em que se interrompe o bloco | notificações |
| lead pediu "me liga mês que vem" (sem opt-out) | Aplicar a tag **`pausado`** à mão; retirar quando voltar. A tentativa fica represada no mesmo ponto da régua | contato → tags |
| 18:30 | Tudo o que ficou sem resultado o W11 classifica sozinho como `Não atendeu` (nó 10b) e entra na lista `Sem resultado ontem` do gestor — **é a lista que mostra tentativa não feita**. Classificar de verdade antes disso | — |

**Nunca (SDR):** mover etapa além de `NOVO LEAD` → `CONECTAR`; aplicar ou
remover `fila-*`, `toque`, `limpar-tarefas`; criar tarefa `[CADENCIA]` à mão;
editar `Tentativa nº`, contadores ou `Template usado`; marcar `Não ligar`
para se livrar de um lead difícil; mandar WhatsApp por fora (a mensagem
manual não grava `Template usado` e o lead pode ter DND).

## 3.2 O closer

| Momento | O que fazer | O que dispara |
|---|---|---|
| ao ser notificado do agendamento (W5 nó 12) | ler a nota "REUNIÃO AGENDADA" no contato: nota de qualificação, BANT, dor, histórico | — |
| na hora da reunião | marcar o agendamento como **`Showed`** ou **`No Show`** no calendário — não deixar em `Confirmed` | `Showed` → W7 (`Data compareceu`, zera no-shows) · `No Show` → W8 (NS1 ao SDR) + W9 (SLA) |
| no-show | responder em **2 h**: reagendar pelo calendário (o W5 tira o lead da recuperação sozinho) ou deixar o SDR recuperar (NS1–NS3). Segundo no-show seguido descarta sozinho | W9 nó 6 avisa o gestor se passar de 2 h |
| até o fim do dia da reunião | preencher **`Reunião foi qualificada`** (`Sim`/`Não`/`Parcial`) e, se `Não`, **`Motivo da desqualificação`** — no contato | W6: carimbo, nota, `abandoned`/`lost` conforme o veredito, alerta de calibração ao gestor |
| negociação | trabalhar em `NEGOCIAR`; fechou → mover para `FORMALIZAR` e status `won`; perdeu → status `lost` com motivo | Mestre de saída limpa o que sobrar |

**Nunca (closer):** mover o lead de volta para `CONECTAR` (o SDR não vai
recebê-lo — `Allow Re-entry` da 12x30 é desligado; quem recicla é o
Reengajamento, 90 dias depois de `nutricao-90d`); apagar `nao-perturbe`/DND.

## 3.3 O gestor

| Cadência | O que olhar | Sinal de problema |
|---|---|---|
| **diário, 08:15** | `Sem resultado ontem` (8.5) | lista crescendo = tentativa que o SDR não fez, classificada às 18:30 pelo nó 10b |
| diário | `Atraso na 1ª Tentativa` (8.8), `Saúde — NOVO LEAD Estagnado` (8.20), `Saúde — Fila Travada` (8.21) | qualquer linha: speed-to-lead estourou (15 min inbound / 1 h outbound), lead esquecido 24 h, ou o motor travou |
| **11:00 e 15:00** (W18 lembra) | `Estouro da Fila` no dashboard / `Fila do Dia — Total` (8.16) | positivo = mais de 100 tarefas hoje → segurar entrada ou remanejar SDR |
| semanal | `Conexão por Tentativa` (8.6), `Calibração da Régua` (8.7), `Pausados Individualmente` (8.15), `Higiene — Sem Telefone Válido` (8.18) | tentativa que nunca conecta (cortar da régua); nota ≥ 70 com veredito `Não` repetido (régua 9.1 desregulada); pausado há semanas (decidir); lista suja (fonte de lead) |
| mensal | `Funil — Entraram/Conectaram/Agendaram/Compareceram no Mês` (8.9–8.12), `Resposta por Template` (8.13), `Conexão por Segmento e Horário` (8.19) | taxa de conexão = 8.10 ÷ 8.9; declarar vencedor do A/B (editar o Split para 100/0 e registrar em `biblioteca-mensagens.md`); ajustar horário por segmento (2.18) quando houver volume |
| por notificação | alertas "ao gestor": telefone inválido (W4-N4, W11-0.0c), speed-to-lead (W15), calibração (W6-5/6), no-show sem retorno (W9-6), descarte por 2º no-show (W8-D5), lead esquecido (W17), fila travada (W17b), opt-out (W14-6b) | cada um diz o que fazer no próprio texto |
| a cada hora (automático) | `rotina-limpar-tarefas.md` fecha as tarefas `[CADENCIA]` vencidas de quem tem `limpar-tarefas` | se parar de rodar, tarefas vencidas se acumulam na tela do SDR |

**Decisões que só o gestor/dono toma** (nada disso sai por API nem por
rotina): G-03 (promoção `NOVO LEAD` → `CONECTAR`), G-04 (mapeamento do Meta
e opções de `Investimento mensal`), `[x]` das tags `novo-lead-estagnado` e
`fila-travada` em `APROVADO.md`, número de teste para WhatsApp, pausas de
feriado/férias (1.9), vencedor do A/B, teto de toques (6/semana — editar
no nó 2.5c/3c), segundo SDR (1.10).

## 3.4 Regras de convivência com a automação — o que nunca fazer na tela

1. **Não excluir** contato, campo, tag, workflow, pipeline, oportunidade
   (regra 1 do projeto). Descartar é `status = lost`.
2. **Não renomear** etapa, tag, opção de campo ou workflow em uso — todo
   `If/Else`, filtro de gatilho e `Remove from Workflow` compara o nome exato
   e passa a nunca casar, sem erro visível.
3. **Não editar/republicar** `Cadência 12x30`, `Cadência Inbound`,
   `Reengajamento 90 dias` ou `Contador de Toques` com contatos parados em
   `Wait` — o GHL pode reposicionar as instâncias (`build-wesales.md`, 2.8).
   Editar fora do expediente e conferir `Toques na semana` depois.
4. **Não usar "Construir com IA"** para nó com campo personalizado.
5. **Não criar campo paralelo** para a mesma informação (`SDR responsável`,
   "canal desta tentativa"…) — campo com dois donos diverge.
6. **Não mandar mensagem manual** para lead com `nao-perturbe`/DND, nem
   para lead em cadência sem gravar `Template usado`.
7. **Testar em contato fictício** (seção 0.5), nunca em lead real; espaçar
   dois disparos no mesmo contato em ≥ 5 s.
8. **Mudou algo na tela? Mude o documento.** `build-wesales.md` é a fonte;
   `CONFERENCIA-CAMPOS.md` registra o que a tela tem; este arquivo, o
   clique. Divergência entre os três é bug em espera.

## 3.5 Metas e números que a máquina persegue (fonte de cada um)

| Métrica | Alvo | Onde vive | Onde se lê |
|---|---|---|---|
| Leads novos/dia | ~10 | `briefing-sdr.md` | 8.9 / dashboard |
| Ligações/dia por SDR | 100 | `briefing-sdr.md` | widget Tasks / 8.16 |
| Tarefas abertas/dia | ≤ 100 | `build-wesales.md` 2.15 | `Estouro da Fila` |
| Speed-to-lead | 1ª tentativa em ≤ 15 min (inbound) / ≤ 1 h (outbound) | 2.11 | 8.8 |
| Tentativas por lead | 12 em 30 dias (outbound) · 5 em 3 dias (inbound) · 4 em 10 dias (reengajamento) · 3 em 4 dias (no-show) | 2.5 / 2.10 / 2.12 / 5.3 | `Tentativa nº` |
| Toques por semana por lead | ≤ 6 | 2.19 | `Toques na semana` |
| No-shows seguidos antes de descartar | 2 | 5.3 | 8.17 |
| Nutrição | 90 dias, depois reativa sozinho | 2.12 | 8.14 |
| Nota de qualificação | A ≥ 70 · B 45–69 · C 25–44 · D < 25 | 9.1 | 8.7 |
| Retorno do closer após no-show | 2 h | 5.4 | notificação W9 |

## 3.6 Checklist de go-live (na ordem)

1. **Decisões do dono:** G-03, G-04, `{{right_now}}` (testar na tela), número
   de teste para WhatsApp (`APROVADO.md`), `[x]` de `novo-lead-estagnado` e
   `fila-travada`.
2. **Estrutura:** criar os 3 campos (1.2); corrigir `Plataformas de anúncio`;
   aplicar a decisão G-04 nos campos e nos 8 formulários do Meta; criar as
   2 tags (por API, depois do `[x]`).
3. **Retoques nos publicados** (tabela do `GUIA-MONTAGEM.md`): Mestre de
   saída (nó 1 `NOVO LEAD`, nó 0, nó 4 `fila-travada`, token da nota),
   Pós-ligação (A2, 3b), Pós-agendamento (nó 4 nota, merge fields do nó 6),
   Interceptação — Resposta (filtro opt-out).
4. **Montar e publicar, nesta ordem:** W1 Contador de Toques → W6 Loop do
   closer (refazer) → W7 → W9 (+ publicar W8) → W10 (confirmar conteúdo) →
   **W11 Cadência 12x30** → W12 → W14 → W15 → W16 → W17 → W17b → W18.
5. **Testar** cada um com o contato fictício indicado na seção "Teste"
   (checklist completo: `build-wesales.md`, seção 10) — e ler o rastro por
   API (apêndice).
6. **Só então** promover o estoque de `NOVO LEAD` para `CONECTAR` (G-03) —
   promover antes de publicar a 12x30 manda os leads para um evento que
   ninguém escuta (`APRENDIZADOS-CRM.md`, 21/09).
7. Listas 8.1–8.21 favoritas por papel; dashboard; pausas de feriado (só
   lista workflow publicado).
8. Primeira semana: gestor abre 8.5, 8.8, 8.20, 8.21 **todo dia** — são os
   sensores de que a máquina está rodando de verdade.

---

# APÊNDICE — validação por API


O conector `GHL CRM` lê contato, oportunidade, notas e tarefas — não lê
workflow. Então o teste é sempre: **mudar um campo/etapa num contato de
teste, esperar ≥ 10 s, ler de volta**.

| Para disparar | Ferramenta |
|---|---|
| campo de contato (gatilhos `Contact Changed`) | `contacts_update-contact` com `customFields: [{id, fieldValue}]` (ids na seção 0.3 — use o `id` do campo, lido por `locations_get-custom-fields`) |
| tag (gatilhos `Contact Tag Added`) | `contacts_add-tags` / `contacts_remove-tags` |
| etapa ou status (gatilhos de oportunidade) | `opportunities_update-opportunity` com `pipelineStageId` (seção 0.1) ou `status` |
| agendamento (gatilhos `Appointment Status`) | só na tela — o conector não cria/edita agendamento |

| Para ler o rastro | Ferramenta |
|---|---|
| campos e tags | `contacts_get-contact` |
| etapa, status, **notas** e tarefas da oportunidade | `opportunities_search-opportunity` com `query_contact_id`, `query_getNotes=true`, `query_getTasks=true` |
| tarefas do contato | `contacts_get-all-tasks` |

Regras que já custaram tempo: espaçar dois disparos no mesmo contato em
≥ 5 s (o GHL pula o segundo); `contacts_get-contacts` (lista) atrasa em
relação à escrita — leia pelo id; DATE grava só a data.
