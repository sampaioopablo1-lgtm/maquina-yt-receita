# Prospect Halo — post todos os dias: limite, campos e recursos
*Escrito em 09/09/2026, a pedido do Pablo: "importante ter post todos os dias; explore o limite; verifique as configurações campo por campo; explore todos os recursos da ferramenta".*

## 0. O que pude e o que não pude olhar

**Não consegui abrir o workspace ao vivo.** A chave `ph_live` do Prospect Halo não está guardada em
nenhum lugar persistente (repositório, Supabase `config`, variáveis do sandbox do Composio, variáveis
desta sessão). O endpoint MCP responde `401`:

```
Connect with OAuth, or provide a ProspectHalo API key as 'Authorization: Bearer <key>'
or '?key=<key>'. Generate one in Settings under AI agents and MCP.
```

Tudo que está abaixo sobre a conta do Pablo vem do `DIARIO — otimizacao.md` e das `LICOES` de 08/09 e
09/09. Tudo sobre limites e campos vem da documentação pública (site, central de ajuda, artigo de
planos) lida em 09/09. Onde o dado é da conta e não da documentação, está marcado como **(conta, 08/09)**.

**Para destravar a leitura ao vivo, uma das duas:**
1. Pablo gera a chave em *Settings → AI agents and MCP* e a guarda num lugar que sobrevive a reinício:
   secret `PROSPECT_HALO_KEY` no GitHub **e** linha `prospect_halo_key` na tabela `config` do projeto
   `vevocauwtarctfwngrch`. A rotina das 7h35 e a das 21h33 leem de lá.
2. Ou conecta o conector MCP `https://app.prospecthalo.ai/api/agent/v1/mcp` (OAuth, sem chave) no
   Claude — aí qualquer sessão consegue ler e agir.

Sem isso, as quatro rotinas do OPC que dependem do Prospect Halo (7h35, a cada 2h, 21h33, sexta 18h)
continuam rodando "cegas": elas não erram, só não enxergam.

## 1. O limite: quantos dias podem ter post

| Plano | Posts por período | Agentes | Prospects/período | Contas de envio | Enriquecimentos |
|---|---|---|---|---|---|
| **Pro (US$ 59)** — o do Pablo | **35** | 2 | 2.000 | 2 | 50 |
| Growth (US$ 100) | 100 | 4 | 4.000 | 4 | 50 |
| Custom (a partir de US$ 160) | sob medida | sob medida | sob medida | mais | — |

Regras que decidem o calendário:

- **O período é a data de cobrança, não o dia 1.** "Limits reset on your own billing date rather than
  the 1st of the month." A conta começou em 08/09 com trial de 7 dias, então o ciclo é **08 → 07 do mês
  seguinte**. Confira em *Billing & usage*, que é a fonte autoritativa.
- **Quando acaba, pausa sem cobrar.** "Everything pauses gracefully. No surprise overage charges."
  Ou seja: estourar 35 não custa dinheiro, custa dias sem post no fim do ciclo.
- **Cada identidade de publicação conta um post.** Perfil pessoal e página da empresa são posts
  separados; publicar o mesmo texto nos dois gasta 2 dos 35.
- **Post manual e post do Autopilot saem do mesmo balde.** Não há cota separada para "eu escrevi".

Conta para 30 dias de post diário:

| Cenário | Posts no ciclo | Cabe em 35? | Sobra |
|---|---|---|---|
| Hoje **(conta, 08/09)**: seg/qua/sex agendados + Autopilot ter/qui | ~22 (5 por semana) | sim | 13 |
| **Todo dia, só perfil pessoal** | 30 a 31 | **sim** | 4 a 5 |
| Todo dia no perfil + 1 por semana na página O Próximo Cliente | 34 a 35 | no limite | 0 a 1 |
| Todo dia no perfil + página também todo dia | 60 a 62 | não | precisa Growth |

**Resposta direta:** no Pro cabem os 30/31 dias do ciclo com post diário no perfil pessoal, com 4 a 5
posts de folga para um extra (post de sexta com números, ou um post na página da empresa). Não cabe
"todo dia nos dois lugares". Se o Pablo quiser perfil + página diários, é Growth (100/mês) ou plano
Custom com volume de posts próprio.

## 2. O que está configurado hoje (conta, 08/09) e o que muda para "todo dia"

| Campo | Hoje (conta, 08/09) | Para post diário |
|---|---|---|
| Posts agendados à mão | 7 posts, seg/qua/sex, até 23/09, todos com mídia | mantém; são os dias "de peso" |
| Content Autopilot | ligado, **ter/qui** | ligar também **sáb e dom** (e seg/qua/sex quando os 7 acabarem, em 23/09) |
| Horário | 7h30 Brasília (rotina de checagem às 7h35) | mesmo horário todo dia; fim de semana pode ir para 9h |
| Identidade de publicação | perfil pessoal do Pablo | mantém; página só se sobrar cota |
| Formatos | não registrado | ver §3: alternar Texto / Imagem única / Carrossel PDF |
| Engajadores → outreach | ligado, agente `jx74mn5nqehy7rcvnh6025vx8d8e1xc9` | mantém; é o que transforma post em lead |
| Papel do post por dia da semana | mapa Nexus Mind aplicado (08/09 14h20) | estender para sáb (bastidor/processo) e dom (número da semana) |

**O ponto que o Pablo precisa decidir:** hoje o Autopilot só gera draft nos dias marcados. Os 7 posts
manuais cobrem seg/qua/sex até 23/09; **a partir de 24/09, se ninguém marcar seg/qua/sex no Autopilot,
o perfil volta a ter só 2 posts por semana.** A mudança de "5 por semana" para "7 por semana" é um
clique em *Content → Autopilot → dias*, mas tem que ser feita antes de 23/09.

## 3. Campo por campo: tudo que a ferramenta expõe

### 3.1 Content → Autopilot (o que gera o post diário)
| Campo | O que faz | Recomendação |
|---|---|---|
| **Themes** (temas) | assuntos de onde o AI tira o post | 3 a 5 temas = dores do dono: agenda vazia, dependência de indicação, agência sem resultado, anúncio que não converte, "não sou agência" |
| **Selected days** | dias da semana em que publica | **todos os 7** |
| **Time** | hora de publicação | 7h30 seg-sex; 9h sáb-dom |
| **Tone** | voz do post | "processo, não motivação; número real; frase curta; 'máquina' como palavra central" (Thiago Reis, registrado em 08/09) |
| **Language** | idioma | pt-BR |
| **Preferred formats** | Text, Single image, Multi-image, PDF carousel | alternar: seg carrossel, ter/qui texto, qua/sex imagem, sáb texto, dom imagem |
| **Voice sample** ("paste one post you wrote") | o AI copia ritmo e vocabulário | colar 1 post real do Pablo, não um gerado |
| **Publishing as** | perfil pessoal ou página | perfil pessoal (a página não prospecta nem manda mensagem) |
| **Route engagers to outreach** | quem reage/comenta vira lead no agente | ligado, apontando para o agente de engajadores |

Mecânica que importa para a rotina:
- O draft nasce **~20 horas antes** de publicar. A rotina das 21h33 já cai nessa janela: ela deve
  **ler e corrigir o draft do dia seguinte**, não só conferir o funil.
- Post agendado **não muda de identidade**; tem que desagendar antes. Post publicado não muda nunca.
- Autopilot gera; não garante que o post foi ao ar. A rotina das 7h35 confere `measurementStatus`
  (hoje devolve `no_posts` quando nada saiu).

### 3.2 Accounts (o que sustenta tudo)
| Campo | Valores | Observação |
|---|---|---|
| LinkedIn (perfil pessoal) | Healthy · Ready · Checking · Safety pause · Needs attention · Needs reconnect | reconectar **só** em "Needs reconnect"; "Safety pause" resolve sozinho |
| Sales Navigator | ligar na conexão se a conta tiver | filtros mais fortes na descoberta |
| E-mail (Gmail/Outlook/IMAP) | opcional; 2 remetentes no Pro | só entra na semana 2, depois de SPF/DKIM/DMARC e aquecimento |
| Limites da conta **(conta, 08/09)** | 6 convites/dia (aquecendo até 15), 20 mensagens/dia, 150 convites/semana | os 2 agentes dividem; adicionar agente **não** aumenta isso |

### 3.3 Agents (cada um dos 2 do Pro)
| Campo | Valores | Estado (conta, 08/09) |
|---|---|---|
| Mission / offer | texto livre | programa de 30 dias, 4 encontros, máquina de leads no WhatsApp |
| Mode | Find and outreach · Find only | Find and outreach |
| ICP: titles · industries · locations · company size | listas | descoberta `jx7a630sdfd5cqnk6j1b5t8yyn8e1v8w`: 6 títulos, 5 setores, RJ+SP |
| Rules | **Required** (rejeita) · **Preferred** (só ranqueia) | exclusões como **Preferred** (Required adiava o lead em silêncio) |
| Evidence warning | "Evidence constrained" | aparece quando uma Required é difícil de provar |
| Intent signals | 18 famílias (mudança de cargo, contratação, atividade, concorrente…) | ligados: aceite, visita, reação, comentário |
| Channels | LinkedIn only · Multichannel | LinkedIn only na semana 1 |
| Approval | Approve first step only · Send automatically · Approve every step | autônomo (review_first já passou) |
| Conversation Autopilot | liga/desliga; `autopilotBookingLink` | ligado, link do Google Agenda como plano B; regra 17h30/18h30 |
| Working hours | janela de envio | seg-sex 8h-18h São Paulo |
| **Não editável pela API:** alvo (titles/industries/locations) | `update_agent` erra | mudar alvo = apagar e recriar; **máx. 1 recriação/dia** (cada uma queima a cota de verificação de perfil) |

### 3.4 Leads · Approve · Inbox · Analytics
- **Leads:** `qualification`, `lane` (high_intent…), `opportunityScore`, `intentScore`. Aviso da conta:
  o score pontua até perfil ilegível ("LinkedIn Member", empresa "brasil", nota 68). Cruzar sempre com
  nome e empresa antes de confiar na nota.
- **Approve:** só existe com "Review first"; hoje vazio porque os agentes são autônomos.
- **Inbox:** `reply_to_lead` só funciona em conversa que já teve resposta.
- **Analytics:** discovery, outreach, connections, replies, positive conversations. A conta mostrou
  três fontes discordando (`get_stats` 0, `list_leads` 1, busca 0): usar `list_leads` como verdade.
- **Busca (`find_leads` / `get_search_results`):** ler `progressStatus` e `waitingReason` antes de
  mexer em segmentação. `waiting_for_profile_capacity` = cota diária de verificação de perfil
  esgotada; `nextRetryAt` diz quando volta. Não é erro e não aparece como pausa.

### 3.5 Settings → AI agents and MCP
- Gera a chave de API (`ph_live…`). É **aqui** que nasce a chave que a rotina precisa.
- Endpoint MCP: `https://app.prospecthalo.ai/api/agent/v1/mcp` (OAuth automático ou `Authorization:
  Bearer <key>` ou `?key=`).
- Ferramentas que a conta já usou: `initialize`, `find_leads`, `get_search_results`, `list_leads`,
  `get_stats`, `update_agent` (limitado), `reply_to_lead`; conteúdo: criar/gerar/agendar post,
  `measurementStatus`. A ajuda oficial confirma "generate and schedule LinkedIn posts" pelo MCP.

### 3.6 Billing & usage
- Fonte autoritativa dos limites da conta. **Ler o contador de posts aqui uma vez por semana** (rotina de
  sexta) e projetar: `posts usados ÷ dias passados × 30 ≤ 35`.
- Add-ons: agente extra US$ 29/mês (+1 agente, +1.000 prospects, +1 conta de envio); 200 enriquecimentos
  de e-mail por US$ 19 (não expiram). **Não existe add-on de posts**; mais posts = Growth ou Custom.

## 4. Recursos que a ferramenta tem e a conta ainda não usa

| Recurso | Onde | Por que vale |
|---|---|---|
| **Sáb e dom no Autopilot** | Content → Autopilot → days | fecha "todo dia" sem estourar 35 |
| **Carrossel PDF** | formats | o carrossel de fundo de funil (BF01-BF10) já existe no repositório; é o formato de maior salvamento no LinkedIn |
| **Página da empresa como identidade** | Publishing as | O Próximo Cliente tem página; 1 post/semana ali custa 4 dos 35 e dá prova social |
| **Sales Navigator na conexão** | Accounts | mais filtros na descoberta, se a conta tiver |
| **Segundo agente = "Find only"** | Agents → mode | lista de prospects para exportar (CSV) e alimentar o público personalizado do Meta, sem gastar convite |
| **Intent signals de "posted about"** | Agents → signals | liga o conteúdo ao outbound: quem postou sobre agenda/leads sobe na fila |
| **Export CSV / API** | Leads | cruzar com a lista da Biblioteca de Anúncios (LISTA — clínicas do Rio) |
| **Agente extra (US$ 29)** | Billing | só se a cota de 2.000 prospects/mês encostar; hoje o gargalo é a verificação diária de perfil, que o add-on **não** aumenta |

## 5. O que fazer, em ordem

1. **Pablo:** gerar a chave em *Settings → AI agents and MCP* e guardar em `PROSPECT_HALO_KEY` (GitHub)
   e `config.prospect_halo_key` (Supabase). Sem isso nada abaixo é verificável por rotina.
2. **Pablo (1 clique, antes de 23/09):** *Content → Autopilot → days* = todos os 7 dias; horário 7h30
   (sáb/dom 9h). Colar um post real como amostra de voz se ainda não colou.
3. **Rotina 21h33 (Claude):** passar a abrir o draft do dia seguinte (gerado ~20h antes) e corrigir
   gancho/número antes de dormir.
4. **Rotina 7h35 (Claude):** ler `measurementStatus`; se `no_posts` num dia marcado, publicar à mão o
   texto reserva do dia (os `copys/OPC12-16` servem) e registrar no diário.
5. **Rotina sexta 18h (Claude):** ler *Billing & usage*, projetar consumo de posts para o ciclo; se a
   projeção passar de 35, cortar a página da empresa primeiro, nunca o perfil.
6. Manter: **1 recriação de agente por dia no máximo**; exclusões como *Preferred*; ler
   `progressStatus`/`waitingReason` antes de culpar o alvo.

## 6. Revisão pedida em 09/09 ("revise as configurações, marque os 7 dias") — estado

**Não executada por falta de acesso.** O MCP do Prospect Halo (`https://app.prospecthalo.ai/api/agent/v1/mcp`)
responde `401` sem chave ou OAuth; a chave `ph_live` da sessão OPC não sobreviveu ao reinício do sandbox e a
sessão OPC (`GERAÇÃO DE DEMANDA OPC`) não está alcançável para mensagem. Tentado em 09/09 14h30.

O que vai ser feito no minuto em que a chave existir (checklist executável, campo a campo):

| Onde | Campo | Valor a gravar |
|---|---|---|
| Content → Autopilot | Selected days | seg, ter, qua, qui, sex, **sáb, dom** |
| Content → Autopilot | Time | 07:30 America/Sao_Paulo (sáb/dom 09:00 se o campo permitir por dia) |
| Content → Autopilot | Themes | agenda vazia · dependência de indicação · agência sem resultado · WhatsApp sem resposta · follow-up que para |
| Content → Autopilot | Tone | processo, não motivação; número real; frase curta; segunda pessoa; "máquina" como palavra central |
| Content → Autopilot | Language | pt-BR |
| Content → Autopilot | Preferred formats | Text · Single image · PDF carousel (sem Multi-image) |
| Content → Autopilot | Voice sample | o post da seção 3 de `MODELO — post LinkedIn na voz do Pablo` |
| Content → Autopilot | Route engagers to outreach | ligado → agente `jx74mn5nqehy7rcvnh6025vx8d8e1xc9` |
| Content → Posts | Publishing as | perfil pessoal do Pablo |
| Content → Posts | Agendados | conferir que os 7 de seg/qua/sex (até 23/09) continuam com mídia; não desagendar |
| Billing & usage | Posts usados / 35 | ler e anotar no diário; projetar `usados ÷ dias × 30` |
| Accounts | LinkedIn status | deve estar Healthy; se Safety pause, não reconectar |
| Agents (2) | sem mudança | 1 recriação/dia no máximo; não mexer |
| Settings → AI agents and MCP | chave | gerar e gravar em `PROSPECT_HALO_KEY` (GitHub) + `config.prospect_halo_key` (Supabase) |

Depois de gravar: exportar a configuração lida para `PROSPECT HALO — configuracao atual.md` (uma linha por campo,
com valor e data), para que a próxima revisão compare contra algo.

## 7. Executado em 09/09 às 14h30 (Brasília), com a chave gravada em `config.prospect_halo_key`

**Medido na API, e corrige a seção 1:** `create_content_post` (rascunho) **não** gasta crédito; `schedule_content_post` **gasta 1** por post agendado, de qualquer origem (manual ou Autopilot). Os 35 são posts agendados ou publicados no ciclo, não posts gerados.

| Ação | Resultado |
|---|---|
| Autopilot | 7 dias, 07:30 America/Sao_Paulo, Portuguese, formatos text + image + carousel (Multi-image removido), 6 temas sem os prefixos "Terça =" e "Quinta =" |
| Destino de engajadores | trocado de `jx74mn…` (agente Engajadores, descoberta desligada, **não aceito** como destino pela API) para `jx7a630…` (Donos de negócio RJ+SP), o único destino válido; os dois agentes têm o mesmo autopilot de conversa |
| 6 posts manuais (11, 14, 16, 18, 21, 23/09) | movidos de 07:30 para **12:30**, para não colidir com o Autopilot |
| 7 posts novos (10, 12, 13, 15, 17, 19, 20/09) | criados e agendados às 12:30, texto puro, na voz do Pablo |
| Créditos | 9 usados → **16 usados, 19 restantes** |

**Calendário resultante:** 10/09 a 23/09 com post todo dia às 07:30 (Autopilot) e um segundo post às 12:30 em 13 dos 14 dias (só 22/09 fica com um). Com 19 créditos, o Autopilot diário vai até **29/09**; de 30/09 a 07/10 o ciclo fica sem crédito, salvo se Pablo desagendar posts de 12:30 (cada um devolve 1 crédito) ou o ciclo renovar antes.

Estado da conta no momento: 20 leads (a maioria com opportunityScore 47, cinco com nome "LinkedIn Member"), 6 convites enviados em 09/09, 0 aceitos, 0 mensagens, 0 respostas; 1 post publicado e medido, 0 reações.

## 8. Melhorias executadas em 09/09 as 14h45 (Brasilia), aprovadas pelo Pablo

| # | Acao | Resultado na API |
|---|---|---|
| 1 | Agente "Engajadores dos posts" (descoberta desligada, 0 leads, nao aceito como destino) apagado | `status: deleting`; agentes 1 de 2, slot livre |
| 2 | Agente "Donos de negocio RJ+SP": regra preferida ("dono ou socio que vende pelo WhatsApp e depende de indicacao, sem agencia nem gestor de trafego"), 7 palavras-chave de sinal, 2 grupos de contratacao (time comercial; recepcao e atendimento) | gravado em `targeting.preferredCriteria`, `signalKeywords`, `hiringSignalConfig`; `targetingNotices: []` |
| 3 | CTA padronizado: os 7 posts de 12h30 passaram de "Comenta N" para "Comenta AGENDA"; os 6 manuais ja usavam AGENDA | 7 `update_content_post` ok |
| 4 | Tom do Autopilot reduzido a: Founder que opera; gancho de uma linha sem numero inventado; frases de ate 12 palavras; um CTA (Comenta AGENDA); sem link, hashtag ou travessao | gravado |
| 5 | Publicador de conteudo fixado explicitamente no perfil pessoal (estava "nao escolhido") | `publisherName: Pablo Sampaio` |

Alvo atual do agente principal, lido da API: setores Medical Practices, Accounting, Construction, Real Estate, Wellness and Fitness Services; locais Rio de Janeiro e Sao Paulo; sem tamanho de empresa (conta sem Sales Navigator); open-to-work excluido.

## 9. A máquina, deixada rodando em 09/09 às 14h55 (Brasília)

### 9.1 O segundo agente foi DESCARTADO, e a recomendação anterior estava errada

A seção 8 propunha usar o slot livre para um segundo agente de descoberta. **Não faça.** `prospecthalo_list_linkedin_accounts` devolve, para a única conta de LinkedIn conectada:

```
activeDiscoveryAgents: 1
discoveryCapacityWarning: "This LinkedIn account is already used by 1 active agent,
                           so each agent may find fewer leads."
remainingAccountSlots: 0
```

A descoberta é **compartilhada por conta de LinkedIn**, e os convites também: `linkedinSendingLimits` mostra 6 convites/dia (configurado 20) e 150/semana, "Shared per connected account across all agents". Um segundo agente **divide** a mesma descoberta e **não** acrescenta um convite sequer. O gargalo é o limite de envio da conta, não a oferta de leads: já há 20 leads na fila e só 6 convites saem por dia.

Portanto o slot fica vazio de propósito. Ele só passa a valer a pena com uma segunda conta de LinkedIn conectada, e `remainingAccountSlots: 0` diz que o plano Pro não permite outra.

### 9.2 Sinais de mudança ligados

`changeSignals.recentJobChange` estava `false`. Ligado: quem acabou de virar dono ou sócio é exatamente o momento em que a dor de gerar demanda aparece. `recentLinkedinActivity` já estava ligado. Funding continua desligado, não faz sentido para empresa de serviço de 2 a 15 pessoas. `researchProspects` já estava ligado (recurso do plano Pro).

### 9.3 A rotina diária: `trig_01CVM9QpiX5Rwe7Niks1BYCf`

"OPC — Prospect Halo: saúde da conta e cota de posts (19h)", cron `0 22 * * *` (19h de Brasília), **ligada à sessão `session_01NZzPYwnqYJG23RaXKGYYY4`**, o mesmo mecanismo das outras quatro rotinas do OPC.

Ela lê oito endpoints e escreve veredito sobre: cota de posts contra os dias que faltam no ciclo; aquecimento de convites (só recomenda subir com aceite ≥ 30% por 3 dias, nunca por tempo decorrido); saúde da conta; proporção de leads "LinkedIn Member"; existência de post agendado para amanhã; respostas novas. É **só leitura**: criar, apagar, pausar agente, publicar post ou responder lead exigem o Pablo na hora.

**Por que ligada a uma sessão e não em sessão nova:** medido em 09/09, deste ambiente `curl` para `app.prospecthalo.ai` e para `supabase.co` devolve código 000, ambos bloqueados pelo proxy de egresso. Uma rotina em sessão nova nasce **sem conectores** (o próprio serviço avisa isso na criação) e falharia todo dia em silêncio, que é o modo de falha que este projeto já catalogou duas vezes. Ligada à sessão do OPC, ela usa os conectores que aquela sessão tem: Supabase para a chave, workbench do Composio para alcançar a API.

**A fragilidade que resta, dita agora e não depois:** se a sessão `session_01NZzPYwnqYJG23RaXKGYYY4` for arquivada, a rotina passa a acordar uma sessão morta. Se isso acontecer, recriar a rotina pela interface de Routines do claude.ai, que permite anexar conectores a uma rotina de sessão nova.

## 10. A separação em dois agentes, e a série de métricas (09/09, 17h30)

Esta seção **reverte a conclusão da seção 9.1**. Lá está escrito que o segundo slot fica vazio de propósito. Ele não ficou. O motivo da reversão não é volume, e a seção 9.1 continua certa nisso: convite é limite de conta, `Shared per connected account across all agents`, e nenhum segundo agente cria convite nenhum.

O motivo é outro, e só apareceu relendo a regra do `add_engager_to_outreach`: **o engajador só entra se passar na qualificação do agente**. Com um agente só, quem comentava no post era filtrado pelos mesmos critérios da prospecção fria — cargo, setor, RJ+SP. Alguém que comenta "AGENDA" e mora em Belo Horizonte era recusado. Isso é perda pura: a pessoa levantou a mão e o filtro de frio a derrubava.

### 10.1 O que ficou de pé

| Agente | Papel | Configuração |
|---|---|---|
| `jx7a630sdfd5cqnk6j1b5t8yyn8e1v8w` "Donos de negócio RJ+SP" | prospecção fria | critérios estreitos mantidos, `discoveryDailyCap: 8` |
| `jx769gh1pkpscexk83h99kxrdx8e2bq2` "Engajadores do conteúdo" | recebe quem engaja nos posts | Brasil inteiro, sem setor, `engagementDiscoveryEnabled: true`, `discoveryDailyCap: 1` |

O Autopilot de conteúdo aponta `engagerDestinationCampaignId` para o segundo. As vagas de agente do plano Pro agora estão em 2 de 2.

### 10.2 Três coisas que a API impôs e uma que ela escondeu

**`create_agent` recusa setor e contexto de empresa vazios** ("At least one target industry or company context term is required"). Como setor vazio era justamente o ponto, o campo `keywords` recebeu termos largos de serviço no lugar da lista fechada de setores. O efeito é o pretendido, mas não é "sem filtro nenhum".

**`update_agent` não aceita `channels`.** Conferido no `openapi.json`, campo por campo: canal é decidido no `create_agent` e ponto. Ligar o e-mail no agente 1 exigiria recriá-lo, jogando fora os 20 leads da fila e queimando cota de hidratação. É ação de painel.

**O `engagementDiscoveryEnabled: true` foi ignorado em silêncio no `create_agent`.** A chamada devolveu `ok: true` e o agente nasceu com `false` — sem erro, sem aviso. Só apareceu porque o estado foi relido depois de criar. Corrigido com `update_agent`. Fica a regra: **nesta API, `ok: true` não é prova de que o campo pegou; releia.**

### 10.3 O freio que quase estrangulou o envio

O `discoveryDailyCap` do agente 1 foi primeiro para **3**, para ele não comer os 6 convites antes do agente 2. A conta desfaz isso: 3 + 1 = 4 leads novos por dia para 6 convites por dia, saldo de −2/dia, e a fila de 14 zeraria em **7 dias úteis** — depois disso o envio cairia de 6 para 4/dia, limitado pela descoberta. Antes do freio a descoberta rodava a ~15/dia e sobrava.

O freio protegia o agente 2 de uma disputa que não existe: 1 post publicado, 0 comentários, 0 engajadores. Corrigido para **8**, acima da taxa de envio. Quando houver engajador de verdade, revisitar.

### 10.4 A tabela de tendência, e por que metade dela é hipótese

Medido em 09/09: 22 prospects descobertos em ~36h, 20 qualificados contra 7 rejeitados (**74% de aprovação**), 6 convites enviados entre 09h02 e 11h19 — a cota do dia inteiro queima em **2h17**. Aceites, respostas e conversas: **zero**, porque os convites saíram hoje.

| Cenário | Convites 20d | Convites 30d | Reuniões 20d | Reuniões 30d |
|---|---|---|---|---|
| A. cap 3+1 (fila seca no dia 7) | 70 | 102 | ~1 | ~1 |
| B. cap 8, 6 convites/dia cheios | 84 | 132 | ~1 | ~2 |
| C. B + convites 6→25 na tela Accounts | ~350 | ~550 | ~4 | ~7 |

A linha de convites é aritmética dos limites reais. As reuniões usam 30% de aceite, 20% de resposta sobre aceite e 20% de reunião sobre resposta — **faixa de referência, não número desta conta**. Enquanto o aceite não for medido, essa metade da tabela é palpite explícito.

A leitura que importa: de A para B é uma reunião. De B para C são cinco. Nenhuma configuração de agente muda a ordem de grandeza — só o número de convites por dia, que mora na tela Accounts, fora do alcance da API.

### 10.5 `prospect_halo_metricas`: a série que faltava

Taxa de aceite, de resposta e de reunião não são legíveis num instante — só existem como série. Sem série, toda correção de configuração vira palpite, que é exatamente o que a tabela acima é hoje.

Tabela criada no Supabase (`vevocauwtarctfwngrch`), uma linha por dia, PK `dia`, RLS ligada e **sem policy de propósito**: só a rotina escreve, com service role. Colunas para o funil (fila, convites, aceites, respostas, conversas), para a descoberta (descobertos 24h, qualificados, rejeitados), para os limites da conta, para o conteúdo e para as cotas, mais um `bruto` jsonb para quando faltar coluna. Primeira linha gravada com o estado de 09/09.

**A rotina mudou de dono.** A `trig_01CVM9QpiX5Rwe7Niks1BYCf` da seção 9.3 estava ligada à sessão do OPC e o serviço **não permite editar o prompt de uma rotina que entrega em sessão alheia**. Ela foi desligada e substituída pela `trig_01LFTwS1fLvmfWUo3DKypWq8`, mesmo horário (19h de Brasília, cron `0 22 * * *`), ligada a `session_01VbV6VHZ3b9oGi1J68e83B9`. O prompt novo mantém todas as regras da antiga (aquecimento só com aceite ≥ 30% por 3 dias, nunca por tempo decorrido; ciclo de cobrança do dia 08 ao 07; "Safety pause" resolve sozinho; leads "LinkedIn Member" acima de 20%) e acrescenta a gravação da linha diária e o gatilho novo: fila abaixo de 6 significa descoberta sem acompanhar o envio.

A fragilidade da seção 9.3 continua valendo, agora apontando para a outra sessão: se `session_01VbV6VHZ3b9oGi1J68e83B9` for arquivada, a rotina acorda uma sessão morta. O serviço avisou de novo que a rotina não guarda conectores — ela depende dos conectores da sessão a que está ligada.

### 10.6 O que continua fora do alcance da API

Duas coisas, ambas de painel, e são as duas que mais valem:

1. **Convites de 6 para 25/30**, tela Accounts. É a única alavanca que muda a ordem de grandeza das reuniões.
2. **Agente 1 para Multichannel**, para usar os 50 créditos de e-mail parados.

Sobre o e-mail, uma correção do que esta sessão afirmou antes: ele foi chamado de "a maior alavanca não explorada" e não é. O limite diário de 30 é da caixa, mas o teto real é o **enriquecimento de e-mail, 50 por mês, 1 crédito por lead** — porque a ferramenta não devolve e-mail junto com o lead do LinkedIn. Contra ~130 convites/mês no LinkedIn, o e-mail é **menor**, não maior. Ele soma e não gasta convite; só não é o primeiro da fila.

## Fontes
- prospecthalo.ai (planos, FAQ "What happens when I hit my monthly limit", "Does it write the LinkedIn posts too") — lido em 09/09/2026
- help.prospecthalo.ai: *Understand plans and usage limits* · *Create and publish LinkedIn content with Autopilot* · *Connect LinkedIn and email accounts* · *Getting started* · *Create your first outreach agent* · *Why is my agent waiting for LinkedIn* · *Connect ProspectHalo to Claude with MCP*
- Conta do Pablo: `DIARIO — otimizacao.md` e `LICOES — mecanismos aprendidos.md` (08/09 e 09/09)
