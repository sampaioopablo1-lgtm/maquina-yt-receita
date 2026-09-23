# Agente de IA "Conexão — Inbound" — definição para a tela

Escrito em 22/09/2026 a pedido do dono, que estava montando o agente em
**Agentes de AI → IA v2 → Novo Agente**. Tudo aqui é colado no que o projeto
já especificou: abertura e perguntas do `script-de-ligacao.md` (R-06), régua
de pontuação da seção 9.1 do `build-wesales.md`, e os **rótulos exatos** que
`locations_get-custom-fields` devolve.

## 0. Antes de tudo: qual é o trabalho deste agente

A operação é **100% telefone** desde 22/09. A leitura da base do mesmo dia
mediu o buraco que o telefone não cobre:

| | |
|---|---|
| Contatos sem telefone | 9 |
| Desses, com e-mail | 1 (e é lead de teste) |
| **Leads reais do Instagram, sem telefone e sem e-mail** | **5** |

Esses 5 estão num ciclo fechado: o nó 3 da `Cadência 12x30` (`phone
has_no_value`) manda para `abandoned` + `nutricao-90d`, e o `Reengajamento
90 dias` recicla tudo que está `abandoned` de volta — eles voltam, batem no
mesmo portão e voltam, de 90 em 90 dias, **sem nunca receber uma tentativa**.

**O trabalho do agente é esse:** ser o canal de quem chega por mensagem e não
tem telefone, qualificar com a mesma régua do SDR e agendar. Não é "mais um
canal" — é o único caminho para essa fatia da base.

## 1. A regra do portão — a mais importante

A seção 6 do `build-wesales.md` já tinha escrito, para a IA de WhatsApp:

> "Só por `Add to Workflow` vindo da Cadência. **Sem gatilho próprio — assim
> você nunca tem IA conversando com lead que não passou pelo portão.**"

Com **Agente Principal ligado**, este agente responde **todas** as mensagens
iniciais — inclusive de um lead que o SDR está ligando hoje. Dois contatos
simultâneos, com discursos diferentes, é pior que nenhum.

**Regra a implementar (aba `Funil` ou `Avançado`, onde houver filtro de
entrada):** o agente **não responde** contato que tenha qualquer destas tags:

| Tag | Significa |
|---|---|
| `fila-tel` | está na fila de ligação de hoje |
| `conectado-hoje` | o SDR já falou com ele hoje |
| `nao-perturbe` | pediu para não ser procurado |
| `pausado` | pausa individual (R-09) |
| `fechar-horario` | **acrescentada em 23/09.** Estado novo: o SDR conectou e está fechando o horário da reunião de diagnóstico. Hoje ela é redundante, porque o `Pós-ligação v2` aplica `fechar-horario` e `conectado-hoje` no mesmo nó e nada remove a segunda. **Ela deixa de ser redundante no momento em que a saída A da seção 2.31 do `build-wesales.md` for implementada** (`Wait 24h` → `Remove Tag conectado-hoje`): a partir daí, um lead 25h dentro da tentativa de fechar horário teria `fechar-horario` sem `conectado-hoje`, e o agente entraria por cima do SDR. Por isso ela entra agora, antes da correção, e não depois |

Sobre a linha `fechar-horario`: é o mesmo erro que já custou caro neste projeto
(cláusula redundante que vira dependência escondida quando a vizinha muda —
F-16). A tag entra no portão **agora**, enquanto é inofensiva, exatamente para
não ser esquecida quando passar a importar.

Se a tela não oferecer filtro por tag na entrada do agente, isto vira
pendência e o agente **não deve ficar como Agente Principal** até existir.

**Segunda camada, que não depende da tela — G-22
(`ROADMAP-SALES-ENGAGEMENT.md`), especificada em 23/09/2026.** O filtro
acima é uma configuração de tela nunca confirmada (item 3 da seção 8), e a
pesquisa que abriu o G-22 achou que "Channel Management" roteia por
prioridade de tag, não por lista de exclusão — não é garantido que a tela
ofereça o que este parágrafo pede do jeito que pede. Existe uma proteção
que não depende de nenhuma tela: a ação de workflow nativa `Update
Conversation AI Bot and Status`, que liga/desliga um bot específico por
contato (`Active`/`Inactive`), chamada por dois workflows novos e
isolados (não editam a Cadência 12x30 nem o Pós-ligação v2 já publicados):

| Workflow novo | Gatilho | Condições | Ação |
|---|---|---|---|
| **"Bot IA — Pausar por Fila"** | `Tag Added` — `fila-tel` OU `fila-wa` OU `conectado-hoje` OU `nao-perturbe` OU `pausado` OU `fechar-horario` | — | `Update Conversation AI Bot and Status` → bot `Conexão — Inbound` → `Inactive` |
| **"Bot IA — Retomar"** | `Tag Removed` — mesma lista de 6 tags | If/Else: nenhuma das 6 tags presente no contato | Verdadeiro → `Update Conversation AI Bot and Status` → bot `Conexão — Inbound` → `Active`. Falso → fim, sem ação |

Fica valendo em paralelo ao filtro de tag da tela, se ele existir — as
duas camadas não competem. Detalhe completo, fontes da pesquisa e por que
o roteamento por prioridade não bastava sozinho: `G-22` no
`ROADMAP-SALES-ENGAGEMENT.md`.

## 2. Aba Geral — valores

| Campo | Valor | Por que |
|---|---|---|
| Nome do Agente | `Conexão — Inbound` | aparece em log e handoff |
| Descrição | `Atende quem chega por mensagem, qualifica pela régua da seção 9.1 e agenda com o closer. Não fala com lead em cadência de telefone.` | é o que lembra do portão daqui a um mês |
| Agente Principal | **Ligado** — só depois do portão da seção 1 existir | ele é o primeiro a responder |
| Habilitado | Ligado | — |
| **Agrupar Mensagens (debounce)** | **10 segundos** (estava 3) | lead digita em rajada: "oi" / "vi o anúncio" / "quanto custa". Com 3s a IA responde a primeira e atropela as outras duas |
| **Pausa ao assumir** | **60 minutos** (estava 5) | você entra na conversa, resolve, e 5 min depois a IA volta a falar por cima de você no meio do atendimento |

## 2.1 Método — o que o mercado faz, e por que 10 perguntas é o desenho errado

Pesquisado em 22/09/2026. A primeira versão deste documento portou as 10
perguntas do `script-de-ligacao.md` para o chat. **Está errado**, e a
literatura é consistente sobre por quê: no telefone a conversa é síncrona e
10 perguntas fluem; em mensagem assíncrona elas viram interrogatório e o lead
some no meio.

| Fonte | Achado | O que muda aqui |
|---|---|---|
| Drift, playbook de conversational marketing | lead que bate **2+ critérios** → dispara a oferta de reunião **imediatamente**; baixa intenção recebe **valor primeiro**, depois requalifica | não qualificar tudo antes de agendar |
| MIT/InsideSales; HBR (1,25 mi de leads, 42 empresas) | resposta em 5 min → **21×** mais chance de qualificar; em 1h → 7×; após 24h → 60× menos | responder em segundos é a maior vantagem da IA sobre a régua de telefone |
| Meetime — benchmark de pré-venda no Brasil | inbound: 1º toque em 5 min, conversão lead→oportunidade **23%**, no-show até **20%** | metas realistas; justifica confirmação antes da reunião |
| Qualified / Fin — guias de AI SDR 2026 | fluxo de **4 estágios**, **2-3 perguntas de dor** no máximo; fluxo rígido quebra quando o lead sai do script | 3 perguntas, e o agente precisa improvisar dentro da etapa |

**E o detalhe que vale mais que toda a pesquisa:** os leads desta base **já
responderam três perguntas no formulário do Meta** — `Urgência` (preenchido
em 40 de 50), `Necessidade` (34) e `Investimento mensal em anúncios` (32).
Repetir essas perguntas é o erro mais caro do inbound: mostra que ninguém leu.
O agente **lê e cita** o que a pessoa já disse.

## 2.2 As cinco etapas conversacionais

| # | Etapa | Objetivo | Mensagens | Sai quando |
|---|---|---|---|---|
| 1 | **Conectar** | responder rápido, citar o anúncio e o que ela já respondeu, pedir licença | 1 | ela respondeu qualquer coisa |
| 2 | **Entender** | 3 perguntas, uma por vez | 3-4 | as 3 respondidas, ou ela puxou o assunto do preço |
| 3 | **Ajudar** | devolver o diagnóstico em uma frase + 1 insight concreto | 1 | entregue |
| 4 | **Agendar** | 2 horários reais do closer, confirmar, registrar | 1-2 | agendado |
| 5 | **Saídas** | sem fit · handoff humano · sem resposta | — | — |

**`Prazo`, `Decisor` e `Budget` — os 45 pontos de BANT — não são perguntados
no chat.** Vão no formulário anexo ao calendário do closer (seção 7 do
`build-wesales.md`) e na própria reunião. É a regra do Drift aplicada: a
reunião é o evento de conversão, não o formulário completo.

As 3 perguntas da etapa 2, escolhidas por peso na régua da seção 9.1 e por
não queimar rapport:

| # | Pergunta | Campo | Peso |
|---|---|---|---|
| 1 | maior perrengue pra trazer cliente novo | `Dor principal` | apoio — mas é o gancho da etapa 3 |
| 2 | investe em anúncio hoje? quanto? | `Investe em anúncios` + `Investimento mensal em anúncios` | **25 de 100** |
| 3 | quem atende o lead quando ele chega? | `Quem atende os leads` | 10 de 30 |

## 3. Aba IA — configuração e prompt

### 3.1 Os três campos antes do prompt

| Campo | Está | Para | Por quê |
|---|---|---|---|
| **Temperatura** | 0.7 | **0.3** | ele precisa gravar `1-5`, `Pra ontem`, `Acima de 10k` **exatos**. A 0.7 ele parafraseia e o `If/Else` nunca casa — o projeto já perdeu uma régua inteira assim (`CONFERENCIA-CAMPOS.md`, Tabela C) |
| **Modelo** | GPT-4o Mini *(Legacy)* | o mais atual do dropdown | "Mini" + "Legacy" é o elo fraco para uma máquina de estados com escrita exata de rótulo |
| **Max Tokens** | 500 | 500 | é teto, não alvo — quem controla o tamanho é o prompt |

### 3.2 Prompt do Sistema — colar como está

```
Você é o pré-vendas da O Próximo Cliente, agência de marketing. Conversa
por mensagem com quem respondeu um anúncio nosso. Seu trabalho é entender
o negócio, devolver um diagnóstico útil e agendar 30 minutos com o
especialista. Você NÃO vende, NÃO passa preço e NÃO promete resultado.

TOM
Português do Brasil, informal e direto, como um humano no WhatsApp.
No máximo 3 linhas por mensagem. UMA pergunta por mensagem — nunca duas.
Sem emoji em excesso. Se a pessoa escreve pouco, escreva pouco.

ANTES DE PERGUNTAR QUALQUER COISA
Leia o que já está preenchido no contato: Urgência, Necessidade e
Investimento mensal em anúncios vêm do formulário do anúncio. NUNCA
pergunte de novo algo que já está preenchido — cite, confirme e siga.
Exemplo: "vi aqui que o que mais pega hoje é {Necessidade}".

VOCÊ TRABALHA EM 4 ETAPAS. Nunca pule etapa, nunca volte.

ETAPA 1 — CONECTAR (1 mensagem)
Cumprimente pelo primeiro nome, diga que é da O Próximo Cliente, cite o
anúncio e o que ela já respondeu, e peça licença para 2 perguntas rápidas.
Termine com pergunta. Exemplo de tom, não copie literal:
"Oi, {nome}! Aqui é da O Próximo Cliente. Você respondeu nosso anúncio e
marcou que {Urgência}. Posso te fazer duas perguntas rápidas pra entender
onde tá o gargalo?"

ETAPA 2 — ENTENDER (no máximo 3 perguntas, uma por mensagem)
Pule a que já estiver preenchida.
a) "Qual o maior perrengue hoje pra trazer cliente novo?"  -> Dor principal
b) "Vocês investem em anúncio hoje? Mais ou menos quanto por mês?"
   -> Investe em anúncios + Investimento mensal em anúncios
c) "E quem cuida de atender o lead quando ele chega — você, vendedor,
   alguém fixo?"  -> Quem atende os leads
Se a pessoa perguntar preço aqui, responda que depende do tamanho da
operação, que é exatamente o que o especialista vê na conversa, e siga
para a ETAPA 3. Não invente valor.

ETAPA 3 — AJUDAR (1 mensagem, e é a mais importante)
Devolva o diagnóstico em UMA frase, ligando o que ela disse, e dê UM
insight concreto e verificável. Não elogie, não faça discurso. Padrão:
"Pelo que você contou: {dor} + {quem atende} = {consequência}. Na prática
o que costuma estar acontecendo é {insight}."
Exemplos de insight aceitáveis:
- lead chega e ninguém fixo atende -> o lead esfria antes de alguém falar
  com ele, e quem responde primeiro leva a venda
- investe em anúncio mas o time comercial é só o dono -> o gargalo não é
  gerar lead, é atender
- já teve agência e não deu certo -> quase sempre é falta de processo de
  atendimento, não de mídia
Nunca prometa número, percentual ou prazo de resultado.

ETAPA 4 — AGENDAR
Só depois da ETAPA 3. Ofereça DOIS horários concretos da agenda do
especialista, nunca "quando você pode?". Confirme o escolhido e diga que
vai chegar a confirmação. Se recusar os dois, ofereça outros dois. Se
recusar de novo, pergunte o melhor dia e passe para humano.

QUANDO NÃO HÁ FIT
Se ficar claro que não serve — concorrente pesquisando preço, já é
cliente, ou não tem nenhuma condição de investir e nada indica que muda —
NÃO force o agendamento. Agradeça com cortesia, sem prometer retorno.

PASSE PARA HUMANO IMEDIATAMENTE SE
- pedirem falar com uma pessoa;
- houver reclamação, tom hostil ou ameaça;
- perguntarem preço três vezes seguidas;
- a conversa sair do assunto duas vezes seguidas.

NUNCA
- Nunca invente preço, prazo, case, número ou percentual.
- Nunca prometa retorno de investimento.
- Nunca diga que é uma IA; se perguntarem direto, diga que é o assistente
  da O Próximo Cliente e que um especialista assume a seguir. Não afirme
  ser humano.
- Nunca insista depois de "não tenho interesse".
- Nunca peça CPF, cartão, senha ou dado bancário.
- Nunca escreva mais de 3 linhas.
```

**Sobre o nome "ETAPA 4 — AGENDAR" dentro do prompt:** é nome de etapa da
**conversa**, para o modelo se orientar, e não tem relação com a etapa do
funil. A do funil se chama `REUNIÃO DE DIAGNÓSTICO` desde 22/09 (id
`3d26fcd1-220d-49ed-8325-705dfe9055b1`, o mesmo de antes da renomeação). O
prompt acima é para colar como está, sem acrescentar nada: **nome de etapa do
funil, id e data não entram nele** — o modelo não precisa dessa informação e
ela só gasta contexto e arrisca aparecer na conversa com o lead. Quem configura
etapa é a aba `Funil` (seção 7), não o prompt.

### 3.3 Custom Tools — o que o agente precisa poder fazer

O prompt acima só funciona se a aba `Custom Tools` der estas ações. Confira
quais existem; o que faltar vira nó de workflow em vez de ação do agente.

| Ação | Para que etapa |
|---|---|
| Gravar campo personalizado do contato | 2 (as respostas) |
| Ler campo personalizado | 1 (não repetir o que o Meta já trouxe) |
| Consultar horários livres do calendário do closer | 4 |
| Criar agendamento | 4 |
| Aplicar/remover tag | 4 e 5 |
| Mover etapa da oportunidade | 4 |

### 3.4 Documentos e Follow-up

**Documentos** é a base de conhecimento do agente. Suba os 3 insights da
ETAPA 3 e as 8 objeções do `script-de-ligacao.md`, seção 5 — assim ele
responde objeção com o material da casa em vez de improvisar.

**Follow-up**: se o lead parar de responder no meio, 2 toques — 3h depois e
24h depois — e só. O terceiro toque sem resposta vira `nutricao-90d`.

## 4. Campos — os rótulos exatos, e por que isso não é detalhe

O agente tem de gravar **exatamente** estes textos. O projeto já perdeu uma
régua inteira por comparar contra rótulo que não existia mais: chave ou
rótulo errado não dá erro, o `If/Else` só nunca casa e a nota fica errada em
silêncio (`CONFERENCIA-CAMPOS.md`, Tabela C).

| Pergunta | Campo | Opções válidas — texto exato |
|---|---|---|
| 1 | `Clientes novos por mês` | `10` · `11-30` · `31-100` · `+101` |
| 2 | `Quem atende os leads` | `Dono` · `SDR` · `Vendedor` · `Ninguém fixo` |
| 3 | `Tem time comercial` | `Só dono` · `1-5` · `6-10` · `+10` |
| 4 | `Investe em anúncios` | `Sim` · `Já investiu e parou` · `Nunca` |
| 4a | `Investimento mensal em anúncios` | `Até 1k` · `1k a 5k` · `5k a 10k` · `Acima de 10k` |
| 4b | `Plataformas de anúncio` | `Meta` · `Google` · `Tiktok` · `Outros` |
| 5 | `Já teve agência?` | `Tem hoje` · `Já teve` · `Nunca teve` |
| 5a | `Experiência com agência` | texto livre |
| 6 | `Canal principal de venda` | `WhatsApp` · `Telefone` · `Loja` · `Online` |
| 7 | `Dor principal` | texto livre |
| 8 | `Prazo` | `Pra ontem` · `Espera 30 dias` · `Este ano` · `Sem prazo` |
| 9 | `Decisor` | `Sim` · `Influencia` · `Não decide` |
| 10 | `Budget` | `Tem` · `Precisa aprovar` · `Não tem` |
| sem fit | `Motivo da desqualificação` | `Sem fit` · `Sem budget` · `Timing errado` · `Não é decisor` · `Concorrente` · `Duplicado ou já cliente` |

**Cuidado conhecido:** `Resultado da tentativa` ainda **não** tem a opção
`Desqualificado` (R-18, pendente na tela). Então, no caso "sem fit", o agente
grava só `Motivo da desqualificação` — não tente gravar um resultado que não
existe como opção.

## 5. Aba Horário

| | |
|---|---|
| Janela | **08:30–20:00, segunda a sábado** |
| Fuso | da subconta (`America/Sao_Paulo`) |

Mais larga que a janela do telefone (08:30–18:30, seg–sex) de propósito, e é
o que a seção 6 já tinha definido: mensagem fora do horário comercial ainda é
bem recebida, ligação não. Quem responde 21h no sábado é lead quente.

## 6. Aba Memória

Ligue a memória por contato e guarde: o que já foi perguntado (para não
repetir), a dor da pergunta 7, e se já houve handoff. Sem isso o agente
recomeça a entrevista a cada retomada — que é o defeito mais visível de
agente de inbound.

## 7. Aba Funil — o que acontece ao fim da conversa

| Situação | O que o agente faz |
|---|---|
| Agendou | move a oportunidade para **`REUNIÃO DE DIAGNÓSTICO`** (`3d26fcd1-220d-49ed-8325-705dfe9055b1`), tag `conectado-hoje`, remove `fila-tel` e `fechar-horario`. **Corrigido em 23/09:** esta linha dizia `AGENDAR`, nome que a etapa deixou de ter na renomeação de 22/09 — o id é o mesmo, então nada quebrou, mas o documento estava mandando configurar por um nome que não existe mais na tela. A remoção de `fechar-horario` é a mesma correção que o nó 4 do `Pós-agendamento v2` precisa (seção 2.31.2): quem agenda tem de sair desse estado, e aqui é o agente que conduz |
| Qualificado, não agendou | mantém em `CONECTAR`, aplica `fila-tel` para o SDR ligar. **Não aplicar `conectado-hoje`** — o agente conversou, o SDR ainda não, e essa tag hoje é permanente: aplicá-la aqui tiraria o lead das filas 8.2/8.3 para sempre sem ninguém nunca ter ligado para ele. É a armadilha do F-16 vista do lado do agente |
| Sem fit | grava `Motivo da desqualificação`, `status = lost` sem mudar de etapa |
| Pediu para não ser procurado | tag `nao-perturbe` **e** DND nativo — os dois, nunca só um (é o que a auditoria R-14 confere) |
| Handoff | notificação interna. **`conectado-hoje` sai desta linha (23/09)** pelo mesmo motivo da linha "Qualificado, não agendou": handoff é o agente passando a bola, não conexão do SDR. Com a tag permanente, aplicá-la no handoff entrega ao SDR um lead que já está fora das filas dele — o oposto do que um handoff quer |

## 8. O que falta confirmar na tela — não consigo ver por API

1. **A IA v2 está desativada** (aviso amarelo). Nada roda sem ativar — e vale
   saber se há custo por mensagem antes de ligar.
2. **Quais canais este agente atende.** A aba diz `IA · proximo-cliente-1`, e
   há abas separadas de WhatsApp/Voice/Grupos. **Se ele só responde WhatsApp,
   não alcança os 5 do Instagram** — que são o motivo principal dele existir.
   **Corrigido em 23/09/2026 (G-09, roadmap):** esta frase dizia "o WhatsApp
   está desconectado" — valia até 21/09/2026. Desde 22/09/2026 a subconta tem
   a integração não-oficial Stevo (QR) conectada, e ela já está gerando
   contato de teste sozinha (`APRENDIZADOS-CRM.md`). O que continua sem
   confirmação de tela, e importa mais agora que existe tráfego real: a aba
   "WhatsApp" da IA v2 escuta o canal nativo (Meta) ou também reconhece uma
   integração não-oficial que entrega mensagem como SMS por baixo
   (`TYPE_CUSTOM_SMS`, confirmado por API)? Se só reconhecer o nativo, este
   agente não vê a Stevo, mesmo com ela conectada e recebendo mensagem —
   mesma pergunta que o G-09 deixou em aberto para os workflows por trás do
   canal WhatsApp deste projeto.

   **Reduzido em 23/09/2026 (G-22, roadmap), sem fechar por inteiro:**
   pesquisado (`WebSearch`, confiança média — documentação oficial da
   HighLevel, `help.gohighlevel.com` bloqueado pelo proxy deste ambiente
   para leitura direta, não testado nesta subconta) — Instagram **é** canal
   nativamente suportado por Conversation AI Bot Channels, a IA v2 não está
   limitada a WhatsApp por desenho de plataforma. O que resta em aberto não
   é mais "o produto suporta isto?" — é só "esta subconta específica tem o
   canal Instagram ligado à aba `IA · proximo-cliente-1`?", a mesma
   pergunta de tela do parágrafo acima, agora estendida de WhatsApp/Stevo
   para Instagram também.
3. **Se existe filtro de entrada por tag** (seção 1). Sem ele, não ligue o
   Agente Principal **como única proteção** — a seção 1 já ganhou uma
   segunda camada que não depende desta confirmação de tela (G-22,
   workflows "Bot IA — Pausar por Fila"/"Bot IA — Retomar"). Continue
   preferindo o filtro de tela se ele existir (reduz ainda mais a chance de
   sobreposição), mas a ausência dele deixou de ser bloqueio sozinha.
4. **Quais campos a aba `IA` oferece** — prompt livre, modelo, temperatura — e
   se `Custom Tools` permite gravar campo personalizado e mover oportunidade.
   É isso que decide se a seção 7 sai por configuração ou vira workflow.

---

## 9. As 5 conversas de teste — o que decide o provedor

Escritas em 22/09/2026. Rode **as mesmas 5 em cada provedor que você
configurar**, com o mesmo prompt, e compare lado a lado. Cada uma testa um
modo de falha diferente, e todas terminam com a mesma conferência: **abrir o
contato e olhar se os campos foram gravados com o texto exato**.

Mande as mensagens **uma por vez**, esperando a resposta, como um lead real.

### Teste 1 — o caminho feliz

| Você manda | O que tem de acontecer |
|---|---|
| `oi, vi o anúncio de vocês` | ETAPA 1: cumprimenta, cita o anúncio e o que ela já respondeu no formulário, pede licença, termina com pergunta |
| `pode perguntar` | ETAPA 2a: pergunta o maior perrengue |
| `to gastando com anúncio e não fecha ninguém` | ETAPA 2b: pergunta se investe e quanto — **uma pergunta só** |
| `uns 3 mil por mês no meta` | ETAPA 2c: pergunta quem atende o lead |
| `sou eu mesmo que respondo` | **ETAPA 3**: devolve o diagnóstico em uma frase + um insight. **Não** pode pular direto para o agendamento |
| `faz sentido` | ETAPA 4: oferece **dois horários concretos** |

**Reprova se:** pular a etapa 3 · fizer duas perguntas na mesma mensagem ·
perguntar "quando você pode?" em vez de oferecer dois horários · escrever mais
de 3 linhas.

### Teste 2 — preço cedo (o mais comum de todos)

| Você manda | O que tem de acontecer |
|---|---|
| `oi` | ETAPA 1 |
| `quanto custa?` | desvia sem inventar valor, diz que depende do tamanho da operação, **e continua o fluxo** |
| `mas me dá uma ideia, 2 mil? 5 mil?` | continua sem dar número, oferece a conversa com o especialista |

**Reprova se:** citar qualquer valor, faixa, "a partir de", ou percentual.
Este é o teste que mais reprova modelo fraco.

### Teste 3 — lead monossilábico

| Você manda | O que tem de acontecer |
|---|---|
| `oi` | ETAPA 1 |
| `sim` | entende como permissão e faz a 1ª pergunta |
| `não sei` | **não trava**: reformula ou segue para a próxima pergunta |
| `talvez` | continua conduzindo, não fica repetindo a mesma pergunta |

**Reprova se:** repetir a mesma pergunta duas vezes · responder algo sem
sentido · desistir e mandar o link do calendário sem passar pela etapa 3.

### Teste 4 — sai do assunto

| Você manda | O que tem de acontecer |
|---|---|
| `oi` | ETAPA 1 |
| `vocês fazem site também?` | responde curto e traz de volta |
| `e quanto tempo vocês estão no mercado?` | **segunda saída do assunto → passa para humano**, como manda o prompt |

**Reprova se:** continuar respondendo perguntas soltas indefinidamente ·
inventar história da empresa · não passar para humano.

### Teste 5 — pede humano / hostil

| Você manda | O que tem de acontecer |
|---|---|
| `quero falar com uma pessoa` | passa para humano **imediatamente**, sem insistir, sem mais perguntas |
| *(em outra conversa)* `vocês só enchem o saco, me tira daqui` | encerra com cortesia, não insiste, e aplica o caminho de opt-out |

**Reprova se:** tentar mais uma pergunta antes de passar · argumentar · pedir
para a pessoa reconsiderar.

### A conferência que vale mais que as respostas

Depois dos 5 testes, abra o contato no CRM e confira **o texto gravado**:

| Campo | Tem de estar exatamente |
|---|---|
| `Dor principal` | texto livre, o que a pessoa disse |
| `Investe em anúncios` | `Sim` · `Já investiu e parou` · `Nunca` |
| `Investimento mensal em anúncios` | `Até 1k` · `1k a 5k` · `5k a 10k` · `Acima de 10k` |
| `Quem atende os leads` | `Dono` · `SDR` · `Vendedor` · `Ninguém fixo` |

No teste 1, `3 mil por mês` tem de virar **`1k a 5k`** — não `3k`, não
`R$ 3.000`, não `3 mil`. E `sou eu mesmo que respondo` tem de virar
**`Dono`**. Modelo que erra isso passa despercebido na conversa e estraga a
régua de qualificação em silêncio, que é exatamente o modo de falha que este
projeto já viveu uma vez.

**Critério final:** quem passar nos 5 e gravar os 4 campos certos, ganha.
Empate, fique com o mais rápido — pela regra dos 5 minutos, latência é
vantagem real.

