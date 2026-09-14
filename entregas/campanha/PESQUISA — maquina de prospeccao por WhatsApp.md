# Máquina de prospecção por WhatsApp — o que a pesquisa achou

*Pesquisado em 14/09/2026, a pedido do Pablo: "criar máquina de prospecção via WhatsApp, com 5, 10
ou mais chips, com IA, conectada para qualificar e agendar reunião".*

## A resposta curta

**O plano de múltiplos chips deixou de ser viável em janeiro de 2026.** E o caminho legal para
prospecção fria em massa pelo WhatsApp **não existe** — não é questão de ferramenta, é de política
da Meta somada à LGPD.

O que existe, e o Pablo já tem rodando, é o caminho com opt-in.

## Por que o multi-chip morreu

As ferramentas que permitem vários chips — **Baileys, WPPConnect, Venom, Evolution API no modo QR**
— funcionam imitando o WhatsApp Web por engenharia reversa. Em **janeiro de 2026 a Meta passou a
detectar e derrubar isso de forma agressiva**: relatos consistentes de número banido em até **48
horas**, sem aviso e sem recurso.

O custo real do modelo não é o chip: é o ciclo comprar → aquecer → disparar → perder → repetir,
levando junto o histórico de quem já tinha respondido.

## As três arquiteturas

| | Como funciona | Risco de ban | Permite frio? |
|---|---|---|---|
| Não oficial (QR, multi-chip) | imita o WhatsApp Web | **altíssimo — 48h** | até cair |
| **API Oficial (Cloud API)** | acesso formal da Meta | zero por método | **não, sem opt-in** |
| **Coexistência** | mesmo número no app E na API, com histórico | zero | não muda a regra |

**Coexistência** é a novidade útil (em produção desde 2024/2025): o mesmo número fica no WhatsApp
Business normal **e** na Cloud API ao mesmo tempo, sem perder conversa. O Pablo continua atendendo
no celular e a IA atende junto. Não suporta chamada de voz/vídeo nem algumas funções, mas para
atendimento e agendamento resolve. **Não autoriza mensagem fria** — isso é regra de conteúdo, não
de conexão.

## As duas camadas legais que impedem o frio

**1. Política da Meta.** Mensagem de marketing iniciada pela empresa exige **opt-in registrado**.
Além disso há **limite de ~2 mensagens de marketing por pessoa por dia somando todas as empresas**
(estourou, bloqueia — erro 131049), níveis de envio (250 → 1.000 → 10.000 → 100 mil → ilimitado) e
**nota de qualidade** que trava a escalada se ficar vermelha.

**2. LGPD.** A ANPD está autuando; multa até **R$ 50 milhões por infração**. Exigências mínimas:
base legal documentada, registro auditável do consentimento (data, hora, texto exato), opt-out
fácil, retenção limitada. Base comprada ou raspada não tem nada disso.

## O que isso significa para o OPC

**A máquina certa já está rodando, e é a versão legal disto.**

O anúncio no Meta leva a um formulário de lead. Quem preenche **dá opt-in** — por vontade própria,
com registro, dentro da lei. Em 14 dias: **20 leads a R$ 8,18**, com 17% dos cliques virando lead.

É exatamente o que a máquina de chip tentaria comprar, só que sem risco de banimento, sem exposição
à LGPD e mais barato que chip + aquecimento + reposição.

**E essas 20 pessoas estão paradas sem ninguém saber se foram respondidas**, porque o Clint segue
sem autorização. Montar um segundo cano, mais arriscado, enquanto o primeiro jorra e ninguém segura
o balde, é a decisão errada na ordem errada.

## A ordem recomendada

1. **Fechar o que existe.** Autorizar o Clint e ligar a IA de qualificação/agendamento no fluxo que
   **já tem opt-in**. Mesma tecnologia, canal legítimo.
2. **A ponte de opt-in para a base fria.** A base existente não pode receber WhatsApp frio, mas
   pode receber **anúncio**: sobe como público personalizado (já é o conjunto CNAE RJ), o anúncio
   leva ao formulário, e quem preenche entra no WhatsApp com consentimento. Mais lento, e é o único
   jeito que não queima.
3. **Só então a Cloud API**, com número em coexistência.

## A pilha, se for adiante

- **Evolution API** — https://github.com/evolution-foundation/evolution-api — roda nos **dois
  modos**. No QR é o risco alto; **no modo Cloud API é segura**. A ferramenta não é o problema.
- **n8n** para orquestrar — https://github.com/enescingoz/awesome-n8n-templates
- **Template de SDR B2B com IA** — https://github.com/iPythoning/b2b-sdr-agent-template
- **Agente WhatsApp com IA em n8n** — https://github.com/IvynTonui/n8n-whatsapp-ai-agent

## Cuidado com os números de "case real"

Fornecedor de ferramenta publica **"42% de resposta no WhatsApp"**. Os benchmarks honestos dizem
**1% a 5% em frio de verdade**; 15-25% só com mensagem pesquisada individualmente, que não escala
com 10 chips. LinkedIn pós-conexão ~10%, e-mail frio 1-5%.

**O WhatsApp não é mágico — ele é melhor no aquecido.** Que é exatamente onde o OPC já está.

## Fontes

- Meta banindo WhatsApp não oficial 2026 — https://www.cubosuite.com.br/blog/meta-banindo-whatsapp-nao-oficial-em-2026-o-que-mudou-e-o-que-fazer
- API Oficial vs Não Oficial 2026 — https://www.agenciarollin.com/blog/api-oficial-whatsapp-vs-nao-oficial-guia-completo-2026
- Coexistência explicada — https://www.ycloud.com/blog/whatsapp-business-app-coexistence-meta-update
- LGPD e WhatsApp Business 2026 — https://www.messagecentral.com/blog/lgpd-whatsapp-business
- Limites de mensagem 2026 — https://chatarmin.com/en/blog/whats-app-messaging-limits
- Messaging Limits (Meta) — https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits
- Benchmarks de outreach frio — https://outreaches.ai/blog/cold-outreach-benchmarks

---

# Pesquisa: existe caminho seguro E gratuito? (14/09/2026)

Pergunta do Pablo: "pesquise hacks, blogs, que conseguiram caminho seguro, gratuito".

## A resposta curta

Não existe hack que seja gratuito **e** seguro **e** frio ao mesmo tempo. As três coisas juntas
não coexistem. Todo material que promete isso é publicado por quem vende disparador.

Mas existem quatro mecanismos oficiais de custo zero. Todos têm a mesma condição: **o lead
escreve primeiro.** É esse o único gatilho que zera a conta na API da Meta.

## Os quatro mecanismos gratuitos reais

| Mecanismo | Janela grátis | Condição | Custo |
|---|---|---|---|
| Cliente escreve primeiro | 24h (hoje) | qualquer origem | R$ 0 |
| Anúncio clique-para-WhatsApp | **72h, tudo grátis** | lead vem de anúncio FB/IG | só a mídia |
| Botão CTA da página do Facebook | **72h, tudo grátis** | lead clica no botão da página | R$ 0 |
| Cota de atendimento | 1.000 msg/mês por número | a partir de 01/10/2026 | R$ 0 |

A janela de 72h é o ponto de entrada gratuito (*free entry point*). Ela cobre **qualquer tipo
de mensagem**, inclusive modelos aprovados — é a única situação em que a Meta não cobra nem
o que você manda por iniciativa própria.

## O que muda em 01/10/2026

Mensagem de atendimento (aquela dentro da janela de 24h, hoje grátis sem limite) passa a ser
cobrada. A Meta mantém as **primeiras 1.000 por mês em cada número** de graça. A janela de 72h
do anúncio **não muda** — continua grátis.

## O achado que resolve a lista dos 2.000

O caminho gratuito para uma lista fria não passa por WhatsApp. Passa por e-mail.

E-mail frio B2B é permitido no Brasil por interesse legítimo (LGPD Art. 7, IX) — telefone e
e-mail de pessoa jurídica, mensagem relevante ao negócio, identificação clara e descadastro
imediato. WhatsApp frio não tem essa proteção: exige opt-in.

Então: **o e-mail carrega o link `wa.me`. O lead clica e escreve primeiro. A janela abre grátis
e a IA atende.**

Isso não é hack — é o desenho correto. E o Pablo já tem metade dele pronto:
`CADENCIA — 5 e-mails, 1.000 envios por dia.md`, 200 prospects novos/dia, custo já orçado.

Comparação para os 2.000 contatos:

| Caminho | Custo do primeiro contato | Risco ao número |
|---|---|---|
| Disparo de modelo de marketing | R$ 0,30 × 2.000 = **R$ 600** | queda de qualidade, limite cortado |
| E-mail com link wa.me | **~R$ 0** (cadência já existe) | nenhum |
| Anúncio clique-para-WhatsApp | orçamento de mídia já ativo | nenhum |

## O que NÃO entra

Aparece muito em blog brasileiro e não vai ser construído aqui:
- Múltiplos chips com aquecimento diário
- Randomização de intervalo para "parecer humano"
- Rodízio de números para reciclar a cota grátis de 1.000/mês

Os três existem para escapar de fiscalização, não para reduzir risco. Um estudo com 800 PMEs
em 2026 achou perda média de 3,4 números em 6 meses em quem usou app não oficial — R$ 12 mil
em base perdida e migração, contra R$ 1.188/ano da via oficial.

## Fontes

- Agendor — janela de atendimento na API oficial
- Pagebot — preços da API Cloud
- SleekFlow — modelo mundial de preços 2026/2027
- SocialHub — API gratuita 2026, opt-in e LGPD, captação B2B de serviço
- Data Stone — riscos de comprar lista de WhatsApp
- Golber Dória — fim do WhatsApp gratuito para atendimento
- Leadjet — guia honesto de WhatsApp marketing B2B

---

# Pesquisa: disparo por conta própria, controlado e 100% gratuito (14/09/2026, noite)

Pergunta do Pablo: "mandando por conta própria, investigue no youtube, artigos, linkedin, encontre
meio de disparo por conta própria de forma controlada para ficar 100% gratuito o processo com o Claude".

## O mecanismo que fecha a conta em zero

A coexistência tem uma propriedade que ninguém vende porque não dá dinheiro a ninguém:

**Mensagem enviada pelo app WhatsApp Business no celular é grátis** — não passa pela tabela da
API. E ela é **espelhada para o webhook** (evento `smb_message_echoes`), então o sistema sabe
que o contato foi tocado. Quando o lead responde, a resposta entra pelo webhook como conversa
iniciada pelo cliente → janela de atendimento → **grátis**. A IA assume dali em diante.

Confirmado em três fontes independentes (docs da 360dialog, YCloud, Marcus Barboza):
- "Messages sent via the WhatsApp Business app are sent to the phone number's webhook URL, via an smb_message_echoes event."
- "Mensagens enviadas pelo app não são cobradas pela Cloud API."
- "As mensagens enviadas pela sua equipe no WhatsApp Business App continuam gratuitas, mesmo com um número conectado à API."

## O desenho

```
Claude prepara (n8n, de madrugada)
  → página do dia com 30 botões, cada um = link wa.me com mensagem pronta e personalizada
Pablo toca (app, de manhã, ~5 min)
  → toca no botão, abre o WhatsApp Business já com o texto, toca em enviar. 30 vezes.
Webhook recebe o eco
  → n8n marca o contato como "tocado em dd/mm" na planilha
Lead responde
  → webhook inbound → n8n → Claude qualifica, contorna, agenda
  → grátis (janela de atendimento)
```

Nenhum modelo aprovado. Nenhum disparador. Nenhuma detecção de robô, porque o envio é humano
de verdade, pelo app de verdade. Nenhum custo de Meta.

## A conta do mês

| | |
|---|---|
| Primeiros contatos | 30/dia × 22 dias = **660/mês** |
| Custo de envio | **R$ 0** (app) |
| Respostas a ~20% | ~130 conversas |
| Mensagens da IA a ~5 por conversa | ~650/mês |
| Custo dessas até 30/09 | R$ 0 (ilimitado) |
| Custo dessas de 01/10 em diante | R$ 0 (cabe na cota de 1.000/mês do número) |
| Servidor n8n | R$ 0 self-hosted, ou R$ 30-50 em VPS |
| API do Claude | ~R$ 5-20/mês nesse volume |

Os 2.000 contatos levam **~3 meses** a 30/dia. É o ritmo que o próprio Pablo pediu.

## O que fica de trabalho manual e por quê

Os 30 toques. ~5 minutos. É o único pedaço que não é automatizado, e é de propósito: é ele que
mantém o envio dentro da regra da Meta e fora do disparo por robô. Automatizar o toque
(Web, Playwright, biblioteca QR) devolve o número à fila de bloqueio — e viola a trava desta
operação: envio na conta do Pablo é sempre dele.

## Vídeos e artigos consultados

- YouTube: "N8N + Claude: Automação Completa com WhatsApp e IA em Minutos" — mostra o nó nativo
- YouTube: "N8N + WhatsApp GRÁTIS: Crie seu Agente de IA sem gastar NADA" — usa WAHA (QR, não oficial; serve só de referência de fluxo)
- YouTube: "N8N + WhatsApp: Responda Mensagens utilizando um Agente de IA"
- Hashtag Treinamentos — Claude + n8n + MCP para WhatsApp
- SocialHub — gerador de link wa.me com mensagem pré-preenchida e UTM
- 360dialog — coexistence webhooks (`smb_message_echoes`)
- YCloud, X-Apps, Marcus Barboza — coexistência em português
- SleekFlow, EvoTalks, ChatLabs, HelenaCRM, Moovyi — o que muda em 01/10/2026
