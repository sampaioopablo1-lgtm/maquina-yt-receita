# Estado do sistema e plano de continuidade — leitura de 22/09/2026, 19:55 UTC

Leitura completa pedida pelo dono antes de implementar qualquer coisa:
documentos, API ao vivo e workflows. **Tudo abaixo foi medido nesta rodada**,
não herdado de rodada anterior. Onde não deu para medir, está dito.

## 1. A subconta

| | |
|---|---|
| Nome / id | Pablo Santos's Account · `1D53YTI9C7oIMBavcQxV` |
| País / locale / moeda | **`BR`** · `pt_BR` · `BRL` |
| Cidade / fuso | São José dos Campos–SP · `America/Sao_Paulo` |
| Telefone da conta | `+5512982381407` |
| Plano | `saasMode: activated`, assinatura **`trialing`** |
| Campos personalizados de contato | **55** |
| Pipeline | 1 — `FUNIL DE VENDAS`, 5 etapas (NOVO LEAD → CONECTAR → AGENDAR → NEGOCIAR → FORMALIZAR) |

## 2. A base, medida

| Medida | Número |
|---|---|
| Contatos | **50** |
| Oportunidades | **50** (1:1 com contato — a Porta de Entrada funciona) |
| Leads reais do Facebook | 39 |
| Contatos de teste/estrutura do projeto | 6 |
| Contatos sem `source` (chegaram por Instagram) | 5 |
| Com telefone | 41 (**9 sem**) |
| Com e-mail | 39 |
| **Sem dono (`assignedTo` vazio)** | **44 de 50** |
| **Sem nenhuma tag** | **33 de 50** |
| `country` = `US` e `timezone` = vazio | **50 de 50** |
| Telefone ou e-mail duplicado | nenhum |

### Oportunidades por etapa e status

| Etapa | Status | Quantas |
|---|---|---|
| NOVO LEAD | `open` | **45** |
| CONECTAR | `lost` | 2 |
| NEGOCIAR | `open` | 2 |
| NEGOCIAR | `lost` | 1 |

Idade na etapa: **37 oportunidades com 3 a 4 dias** paradas, 9 com 2 a 3 dias.
A mais antiga tem 3,7 dias. `monetaryValue` = 5000 em todas as 50 (valor
padrão do workflow de entrada, não estimativa real). `lostReasonId` = vazio
nas 50 — confirma o F-12.

### Entrada por dia

| Dia | Contatos novos |
|---|---|
| 18/09 | 6 |
| 19/09 | 37 (backfill da carga inicial) |
| 20/09 | 6 |
| 21/09 | 1 |
| 22/09 | **0** |

### Preenchimento de campos

As três respostas do formulário do Meta chegam: `Urgência` 40, `Necessidade`
34, `Investimento mensal em anúncios` 32. **Todo o resto da régua de
qualificação (`Decisor`, `Budget`, `Prazo`, `Tem time comercial`) aparece em
3 contatos — e os 3 são de teste.** Nenhum lead real foi qualificado ainda,
porque nenhum foi trabalhado ainda.

## 3. O diagnóstico, em uma frase

**A máquina está construída e a esteira não está ligada.** 20 workflows
publicados, 55 campos, 21 tags, pipeline montado — e 45 leads pagos parados
em `NOVO LEAD`, sem dono, sem tag de fila, há até 3,7 dias. O que falta não é
mais automação: é o passo que coloca o lead na esteira.

Isso é exatamente o **L-07 / G-03**, aberto desde o primeiro dia do projeto:
não existe gatilho que promova `NOVO LEAD` → `CONECTAR`. A `Cadência 12x30`
está publicada e correta, e não roda para ninguém porque ninguém entra nela.

## 4. Canais: o que a especificação não viu

Duas descobertas desta leitura, nenhuma das duas está em nenhum documento:

**Instagram está conectado e vivo.** Página `O Próximo Cliente`
(`pageId 17841480745368398`), 5 conversas com mensagem real de DM. Os 5
contatos correspondentes têm oportunidade aberta em `NOVO LEAD`, carregam só
`limpar-tarefas` e **nenhum tem telefone**. Numa cadência 100% telefone, são
inalcançáveis por construção.

Ressalva de leitura, para não repetir erro deste projeto: as mensagens vêm com
`direction: outbound` e `from` = a conta, e uma delas é claramente pessoal
("Felicidades em seu coração prima"). **Não afirmo que são leads pedindo
preço** — afirmo que o canal existe, tem tráfego real e não está governado por
nada.

**E-mail está livre e sem uso.** 39 contatos têm e-mail; nenhuma régua usa o
canal. É o único canal que eu consigo instrumentar por API (`emails_create-template`)
e o único que **não** disputa a rampa de aquecimento do telefone (F-14).

## 5. O que eu consigo fazer daqui, medido nesta rodada

| Ação | Por API? | Prova |
|---|---|---|
| Corrigir `country` e `timezone` do contato | **Sim** | testado em `ZZ TESTE ESTRUTURA`: virou `BR` / `America/Sao_Paulo`, e as 14 tags sobreviveram |
| Atribuir dono ao contato (`assignedTo`) | **Sim** | parâmetro existe no schema |
| Gravar valor em campo personalizado | **Sim** | `body_customFields` aceita id + valor |
| Adicionar / remover tag | **Sim** | já usado no projeto |
| Mover etapa, status, dono da oportunidade | **Sim** | `opportunities_update-opportunity` |
| Criar template de e-mail | **Sim** | `emails_create-template` |
| Criar workflow, pipeline, campo, calendário, lista inteligente, dashboard | **Não** | seção 11 do `build-wesales.md`; calendário e campo existem na API oficial mas não neste conector |

**Armadilha registrada:** `body_tags` no update **sobrescreve todas as tags**
do contato. Nunca passar esse parâmetro num update que não seja de tags.

**Limitação nova, medida hoje:** `calendars_get-calendar-events` devolve 422
"Either of userId, calendarId or groupId is required" **mesmo passando
`userId`** — o conector não repassa o parâmetro. Não consigo auditar o
calendário do closer por API.

## 6. O que os 24 dumps de workflow não dizem

Os 24 arquivos de `workflows-json/` — incluindo `Monitor de Capacidade` e
`Qualidade da Conexão`, criados hoje — trazem **todos** `status: draft` e
`triggers: []`. É artefato do dump (fotografia do payload antes de publicar),
não estado do CRM: o `GUIA-MONTAGEM.md` lista 20 publicados com rastro lido
por API. **Nenhum arquivo deste repositório responde "isto está ligado e em
qual gatilho?"** — só a tela responde.

## 7. Plano de continuidade, em etapas

Ordem por alavanca, não por facilidade. As etapas 1 a 3 são de escrita em
dados reais e **esperam confirmação do dono** (regra 2 do briefing).

### Etapa A — ligar a esteira (a que vale mais)
Promover os leads reais de `NOVO LEAD` → `CONECTAR` com dono atribuído, em
lotes. É o que faz os 20 workflows publicados começarem a rodar.
**Decisão necessária:** tamanho do lote. Ver a conta da rampa F-14 — 6/dia
devolve a curva segura, 10-13/dia estoura o teto da semana 1 no dia 2.

### Etapa B — consertar o país e o fuso dos 49 contatos restantes — **rebaixada**, era o item que eu tinha vendido como o mais fácil de aprovar

~~`country: US` + `timezone: vazio` em base 100% brasileira afeta janela de
horário de workflow, validação de número (W19) e qualquer nó que use fuso do
contato.~~

**Corrigido em 22/09/2026, 21:25 UTC — eu superestimei esta etapa, e a medição
que me refuta já estava no projeto.** A Tabela L do `CONFERENCIA-CAMPOS.md`
tinha fechado os dois lados antes de eu escrever isto:

| O que eu afirmei | O que a Tabela L já tinha medido |
|---|---|
| "afeta janela de horário de workflow" | **Não afeta.** A decisão D-02 e a seção 2.4 mandam usar fuso **da subconta**, com a justificativa explícita "não use fuso do contato: o SDR trabalha no fuso dele". Nenhum nó lê fuso do contato, então o `null` não quebra nada |
| "afeta validação de número (W19)" | A Tabela L registrou isso como **conferência acoplada ao R-13, não afirmação** — e o W19 saiu **por decisão do dono** (`c945077`), então não há o que destravar |

**O que sobra, honestamente:** higiene de dado. Uma base brasileira marcada
como americana está errada, e a própria Tabela L aponta o risco real — se
algum workflow futuro escolher "fuso do contato" num `Wait` ou numa janela de
envio, cai em fallback silencioso. Isso é **prevenção**, não conserto: barato,
reversível e **sem urgência nenhuma**. Não deve ser a primeira coisa a
aprovar, e eu a apresentei como se fosse.

O erro de método foi o ponto 12 do meu próprio checklist: a conclusão existia
num documento (Tabela L), eu citei essa mesma tabela para outra coisa na mesma
rodada, e não carreguei a conclusão dela para dentro da minha proposta.

### Etapa C — enriquecer `Empresa`
O campo está vazio em 100% da base (Tabela J). Muitos nomes de lead do Meta
carregam o nome do negócio (`Zenilson Fonseca, Serviços E Instalações`,
`Ana Ruth / Especialista em Cabelos`, `TINTIM | Rastreie suas conversas`).
Dá para extrair e gravar por API, com revisão do dono numa lista antes.

### Etapa D — rota para os 9 sem telefone — **agora com o número que faltava**
Numa operação 100% telefone eles são inalcançáveis. Medido em 22/09, 21:25:
dos 9 sem telefone, **1 tem e-mail** (e é lead de teste do Meta) e **8 não
têm**; os 5 leads reais do Instagram não têm telefone **nem** e-mail. Então
"campanha de e-mail" **não é rota para este público** — o único canal que os
alcança é o **DM do Instagram**. Isso derruba a premissa do F-15; correção
completa na seção 2.30 do `build-wesales.md`.

### Etapa E — canal de e-mail (não disputa a rampa do telefone)
Criar templates por API a partir da `biblioteca-mensagens.md`, com sequência
própria. É o único canal que consigo instrumentar daqui de ponta a ponta e o
único que não consome o teto de ligações/dia do F-14.

### Etapa F — governar o Instagram
Definir o que acontece com DM: quem responde, em quanto tempo, e como o lead
entra no funil. Hoje não há regra nenhuma.

## 8. Pendências do dono que travam outras coisas

| # | Pendência | O que destrava |
|---|---|---|
| 1 | **Aviso de gravação (LGPD)** antes de ligar gravação por número | a transcrição já está ligada na subconta; o clique da gravação não passa pelo W20 |
| 2 | Formato de `Entrada em` / `1ª tentativa em` — hora ou a string `sim`? | se for `sim`, o R-02 speed-to-lead não mede nada |
| 3 | Lote do G-03 contra a rampa do F-14 | Etapa A acima |
| 4 | Entrada de leads parada (Gerenciador de Anúncios) | a esteira sem alimentação |
| 5 | Marcar as 6 tags e os 4 campos no `APROVADO.md` | coerência do freio de mão |
| 6 | Pré-requisito 6 do W20 (`Conexão real = vazio` antes de cada tentativa) | sem ele, um `Sim` antigo sobrevive às tentativas seguintes |
