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

## Fontes
- prospecthalo.ai (planos, FAQ "What happens when I hit my monthly limit", "Does it write the LinkedIn posts too") — lido em 09/09/2026
- help.prospecthalo.ai: *Understand plans and usage limits* · *Create and publish LinkedIn content with Autopilot* · *Connect LinkedIn and email accounts* · *Getting started* · *Create your first outreach agent* · *Why is my agent waiting for LinkedIn* · *Connect ProspectHalo to Claude with MCP*
- Conta do Pablo: `DIARIO — otimizacao.md` e `LICOES — mecanismos aprendidos.md` (08/09 e 09/09)
