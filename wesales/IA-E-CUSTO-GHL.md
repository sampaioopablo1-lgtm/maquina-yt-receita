# IA do GHL e o que consome crédito — levantamento de 27/09/2026

Pedido do dono: *"Quando falei módulo de IA me refiro funcionalidades do GHL,
confira na documentação oficial."* Antes disso ele havia decidido: *"Apenas os
agentes de IA, por enquanto vamos dar uma segurada. Como IA no whatsapp, IA na
ligação. Porque gastam crédito, custo."*

Este arquivo existe para que a regra "nada de IA" na rotina ativa aponte para
**nomes de produto reais**, não para uma ideia vaga de "agente".

## Limite de método, dito de saída

`WebFetch` para `help.gohighlevel.com` é **bloqueado pelo proxy de egresso** deste
ambiente (`EGRESS_BLOCKED`), e `curl` para os domínios do GHL responde `000`. O que
funciona é `WebSearch`, que roda fora do contêiner — então o conteúdo abaixo vem dos
**resumos de busca** dos artigos oficiais, não da leitura página a página.

Consequência prática: **os nomes dos produtos e o modelo de cobrança são
confiáveis; os valores em dólar merecem conferência na tela** antes de qualquer
compromisso, porque o GHL muda preço e promoção com frequência (há inclusive uma
promoção "Summer of AI" citada nos artigos, que zera parte da cobrança por tempo
limitado). Não vou tratar número de preço como fato estável.

## As funcionalidades de IA que o GHL vende

O guarda-chuva chama-se **AI Employee**, e reúne:

| produto | o que faz | onde encostaria nesta operação |
|---|---|---|
| **Conversation AI** | responde sozinho por SMS, Facebook e Instagram, 24/7 | é o W10 do projeto (IA no WhatsApp). **Parado por decisão do dono** |
| **Voice AI** | atende chamada perdida, colhe dados do interessado, resolve dúvida básica | é a "IA na ligação". Encostaria no `Receber` do Call Center e no `lc-phone-api` |
| **Reviews AI** | responde avaliações sozinho | é o item 3 da §5 do `ESTADO-27-09.md` (pedir avaliação depois de `won`) |
| **Content AI** | gera copy, design e ideia de campanha | encostaria na biblioteca de mensagens |
| **Ask AI** | assistente que responde perguntas sobre a própria conta | seria atalho para o que hoje eu faço lendo a API |
| **AI Studio** | monta site/funil e ativos por IA, cobrado por uso conforme a complexidade | fora do escopo desta operação |

Uma exceção que vale registrar, porque **não** cai na regra do dono:

- **Workflow AI Assistant** (o "Generate with AI" dentro do construtor de workflow,
  para escrever SMS, e-mail, código). A documentação diz que ele **deixou de
  consumir crédito de IA**. Mesmo assim, o `IMPLEMENTACAO-WORKFLOWS.md` §3.4 já
  proíbe usá-lo por outro motivo, técnico e anterior: *"Não usar 'Construir com IA'
  para nó com campo personalizado."* Então segue proibido aqui — por qualidade, não
  por custo.

## Como o dinheiro sai

Três planos, por subconta:

- **AI Employee Unlimited** — uso ilimitado de Conversation AI, Voice AI, Reviews AI
  e Content AI, mais franquia maior de Ask AI e AI Studio, sujeito a política de uso
  justo (o GHL pode limitar uso excessivo).
- **AI Employee Growth** — franquia mensal definida em toda a suíte.
- **Pay-Per-Use** — **é o plano de quem não assinou nenhum dos dois.** Sem
  mensalidade, e o uso é cobrado **a custo de token**, conforme modelo e ação.

O ponto que importa para a decisão do dono está nessa terceira linha: **não existe
"IA desligada por falta de plano"**. Sem plano, a conta cai automaticamente em
pay-per-use, e o gasto sai da **Carteira da Agência** — que, quando fica abaixo do
mínimo, **recarrega sozinha no cartão da agência**. A mesma carteira paga telefone,
e-mail, validação de e-mail, autocompletar endereço e os recursos premium de
workflow.

Ou seja: ligar uma função de IA "só para testar" não bate num limite que avisa. Bate
no cartão. É exatamente o risco que o dono nomeou.

Existe um **AI Usage Dashboard** no GHL para acompanhar o gasto de IA — vale abrir
antes e depois de qualquer experimento, se algum dia houver.

## O que a conta desta operação mostra hoje

Lido por API (`locations_get-location`, 27/09):

- **`botServiceEnabled: false`** — é o único flag de IA que o payload público expõe,
  e é o interruptor do Conversation AI. Está **desligado**.
- O resto da suíte AI Employee **não aparece** nesse payload: é configuração de
  nível de agência, por subconta. Então a API não confirma nem desmente Voice AI,
  Reviews AI, Content AI, Ask AI e AI Studio — **isso só a tela da agência responde**.
- `subscriptionStatus: "trialing"`, SaaS mode ativado, rebilling de Twilio com 20% de
  markup e de Mailgun com 100%.

## E o que a máquina realmente usa — medido, não suposto

Censo dos tipos de nó nos **36 workflows de produção** (dumps do branch
`claude/amazing-johnson-mclksg`): **nenhum nó de IA**. Os tipos em uso são todos
nativos e sem custo por execução:

```
if_else 1171 · goto 414 · update_contact_field 188 · wait 168 · sms 150
select 141 · add_contact_tag 135 · remove_from_workflow 104 · remove_contact_tag 99
math_operation 80 · add_notes 64 · create_opportunity 63 · task-notification 55
appointment 52 · add_to_workflow 47 …
```

**Um falso positivo que eu quase reportei como achado:** a string `ai_agent` aparece
em **todos** os 36 dumps. Fui conferir onde, e está sempre dentro de
`nestedDropdownTypes` — o **catálogo** de tipos que o construtor oferece, não um nó
montado. Contar string teria produzido "36 workflows usam IA", que é falso. O que
vale é o campo `type` de cada nó.

## Recursos premium de workflow — o custo que já é real, e não é IA

A documentação descreve **Workflow Premium Features**: gatilhos e ações que saem do
conjunto nativo — integração com Slack, Google Sheets, webhook customizado, captura
de webhook de entrada. Cobrança: **100 execuções grátis e depois US$ 0,01 por
execução**, debitado da carteira da agência, salvo rebilling.

**Boa notícia, medida:** nenhum dos tipos de nó em uso é premium. Não há `webhook`,
`google_sheets` nem `slack` em nenhum dos 36 workflows. Então **a máquina como está
não tem exposição a custo por execução** — nem de IA, nem de premium.

Isso é um dado de projeto, não só uma checagem: significa que o desenho atual roda
com o que o plano já cobre, e qualquer conta que apareça na carteira vem de
telefone/e-mail (que têm rebilling ligado), não da automação.

## A regra que fica valendo na rotina ativa

1. **Não ligar nem montar**: Conversation AI (W10), Voice AI, Reviews AI, Content AI,
   Ask AI, AI Studio. Não mexer em `botServiceEnabled`.
2. **Não usar "Construir com IA"** no construtor de workflow — proibição que já
   existia na §3.4, por causa de campo personalizado.
3. **Não introduzir ação premium** (webhook, Google Sheets, Slack) sem o dono
   decidir, porque cada execução passa a custar.
4. Se uma melhoria **depender** de IA para funcionar, ela é **documentada e não
   executada** — e a documentação diz qual produto seria, quanto custaria pelo
   modelo acima, e o que se perde sem ele.

## Fontes

- [HighLevel AI Products Pricing: Voice AI, Agent Studio & More](https://help.gohighlevel.com/support/solutions/articles/155000006652-ai-product-pricing)
- [AI Employee Plans: Voice AI Pricing & Rebilling Guide](https://help.gohighlevel.com/support/solutions/articles/155000003906-ai-employee-overview)
- [HighLevel AI Tools: Features, Use Cases, and Pricing](https://help.gohighlevel.com/support/solutions/articles/155000002166-ai-tools-in-highlevel)
- [HighLevel Pricing & Billing: Wallets, Charges, Rebilling](https://help.gohighlevel.com/support/solutions/articles/155000001156-highlevel-pricing-guide)
- [How to enable and rebill Premium Features for Workflows](https://help.gohighlevel.com/support/solutions/articles/155000005678-how-to-enable-and-rebill-premium-features-for-workflows)
- [How to Enable and Rebill Workflow AI?](https://help.gohighlevel.com/support/solutions/articles/155000000169-how-to-enable-and-rebill-workflow-ai-)
- [AI Usage Dashboard in HighLevel](https://help.gohighlevel.com/support/solutions/articles/155000007742-ai-usage-dashboard)
- [Workflow AI Assistant](https://help.gohighlevel.com/support/solutions/articles/155000003970-workflow-ai-assistant)
- [Managed Agents, Conversation AI & Ask AI: What's the Difference?](https://help.gohighlevel.com/support/solutions/articles/155000008362-managed-agents-conversation-ai-ask-ai-what-s-the-difference-)
- [AI Studio - Pricing](https://help.gohighlevel.com/support/solutions/articles/155000008322-ai-studio-pricing)
