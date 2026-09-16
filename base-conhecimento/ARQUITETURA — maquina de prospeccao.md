# Arquitetura da máquina de prospecção — O Próximo Cliente

*Desenhada em 14/09/2026, a partir de toda a pesquisa da pasta e dos ativos que já existem na conta.*
*Leia junto: `README.md` (o que é seguro), `../entregas/campanha/PESQUISA — maquina de prospeccao por WhatsApp.md` (por quê).*

## Princípio que governa o desenho

**Três portas de entrada, um só núcleo de conversa.**

A IA **nunca inicia** contato. Ela só entra depois que a pessoa falou — seja porque clicou num
anúncio, preencheu um formulário, ou respondeu a uma mensagem que o Pablo mandou na mão.

Isso não é limitação: é o que permite a máquina ser 100% automática **depois do primeiro "oi"**,
sem chip caindo, sem violar política e sem exposição na LGPD.

---

## O desenho

```
  ENTRADA                              NÚCLEO                      AÇÃO

  A. FRIO MANUAL (base de 2.000)
     fila diária de 30 links wa.me
     com a mensagem já preenchida  ─┐
     → o Pablo toca e envia         │
                                    │
  B. CLICK-TO-WHATSAPP              │    ┌──────────────┐      ┌─ agenda no
     campanha WPP I CONVERSA I FS1  ├──▶ │  WHATSAPP    │      │  Google Calendar
     (pausada, pronta para religar) │    │ coexistência │      │  20 min + Meet
     → janela de 72h GRÁTIS         │    └──────┬───────┘      │
                                    │           │ webhook      ├─ grava no Clint
  C. FORMULÁRIO DE LEAD             │           ▼              │
     já rodando: 20 leads a R$ 8,18 ┘    ┌──────────────┐      ├─ avisa o Pablo
     → opt-in registrado                 │     n8n      │──────┤
                                         │  buffer 8s   │      └─ devolve pro humano
                                         │  Claude (nó) │         quando a trava manda
                                         │  memória     │
                                         └──────────────┘
```

---

## Camada 1 — Preparação (roda sozinha, eu faço)

| O que | Como | Saída |
|---|---|---|
| Limpar a base de 2.000 | dedup, normalizar telefone (55+DDD), validar | base limpa |
| Classificar por ICP | Rio, dono, setor, porte | nota A/B/C |
| **Cruzar com a Biblioteca de Anúncios** | `ads_library_search` por nome da empresa | quem anuncia **e erra** |
| Escrever a mensagem | a prova daquele contato, com data | 1 mensagem por contato |
| Montar a fila do dia | 30 melhores ainda não tocados | **página com 30 links `wa.me` pré-preenchidos** |

O `wa.me` é recurso oficial: o link carrega número **e texto**. O Pablo toca, o WhatsApp abre com
a mensagem escrita, ele confere e envia. **30 contatos em 10 a 15 minutos.**

**Por que isso importa mais que qualquer automação:** mensagem genérica responde 1-5%; mensagem
com prova específica responde 15-25%. A diferença entre as duas é esta camada.

## Camada 2 — Entrada

| Porta | Quem inicia | Custo de mensagem | Estado |
|---|---|---|---|
| **A. Frio manual** | Pablo, na mão | R$ 0 | falta a fila |
| **B. Click-to-WhatsApp** | o lead, clicando no anúncio | **R$ 0 por 72h** | campanha pausada, pronta |
| **C. Formulário** | o lead, preenchendo | R$ 0 | **rodando** |

**Coexistência** é a peça que junta tudo: o mesmo número fica no WhatsApp Business (onde o Pablo
manda as 30 na mão) **e** na Cloud API (onde a IA responde), com histórico compartilhado.

## Camada 3 — Núcleo de conversa (n8n)

Reaproveita integralmente a lógica do `PROMPT — agente WhatsApp`, trocando Flask por n8n:

| Peça | Comportamento |
|---|---|
| **Buffer com debounce** | espera 8s desde a última mensagem; várias mensagens seguidas viram **um só turno** |
| **Claude** | nó nativo do n8n (Anthropic Chat Model / AI Agent) |
| **Memória** | histórico por contato, truncado nas últimas 20 mensagens |
| **Resposta fatiada** | quebra por parágrafo e envia em mensagens separadas |
| **Presença** | "digitando" entre os pedaços, pausa proporcional ao tamanho |

**O roteiro da IA, em três passos:** qualifica (3 perguntas: quem cuida do anúncio hoje · há quanto
tempo está assim · qual a verba mensal) → decide (dentro do perfil segue, fora agradece e encerra)
→ agenda (dois horários concretos).

## Camada 4 — Ação

- **Google Calendar** — evento de 20 min com Meet, título `Diagnóstico — [nome] ([empresa])`
- **Clint** — cria ou move o negócio no funil
- **Aviso ao Pablo** — com o resumo da conversa antes da reunião

## Camada 5 — Medição

Cada etapa logada. As rodadas horárias leem e reportam: enviadas → respostas → qualificados →
reuniões → fechados, **cortado por defeito, nicho e bairro**. Em um mês, os benchmarks viram dado
do Pablo e a projeção deixa de ser estimativa.

---

## As travas — o que a máquina nunca faz

1. **A IA nunca manda a primeira mensagem.** Nunca. É o que separa esta arquitetura de um disparador.
2. **A IA se identifica:** *"Aqui é o assistente do Pablo."* Nunca finge ser ele. Mensagem pessoal
   seguida de IA disfarçada, quando descoberta, custa o lead e a reputação.
3. **Devolve para o humano** quando: perguntam preço além da tabela · demonstram irritação ·
   perguntam fora do roteiro · dizem "é robô?" · 2 turnos sem avanço · palavra `#humano`.
4. **Frio é UM toque.** Sem cadência para quem não respondeu — é o comportamento que mais gera
   denúncia, e denúncia é o que derruba número. Cadência longa só **depois** do engajamento.
5. **Opt-out é permanente.** Quem pedir para não receber entra em lista de bloqueio definitiva.
6. **Orçamento é decisão do Pablo.** A máquina nunca mexe.

## APIs em jogo

| API | Para quê | Estado |
|---|---|---|
| **WhatsApp Cloud API** | receber e responder, coexistência | falta habilitar |
| **Meta Marketing API** | anúncios, públicos, Click-to-WhatsApp | **ativa** (via MCP) |
| **Ad Library API** | achar o defeito de cada empresa | **ativa** (via MCP) |
| **Anthropic** | o cérebro da conversa | nó nativo do n8n |
| **Google Calendar** | agendar com Meet | **ativa** (via Composio) |
| **Clint** | CRM | **sem autorização** |
| **n8n MCP** | eu montar e alterar o fluxo daqui | falta subir o n8n |

## Custo mensal

| Item | Valor |
|---|---|
| Mensagens que o Pablo manda na mão | R$ 0 |
| Mensagens recebidas | R$ 0 |
| IA respondendo (janela de 24h) | ~1.000 grátis/mês; excedente a ~R$ 0,05 → **~R$ 5** |
| Click-to-WhatsApp (72h) | **R$ 0** |
| Servidor do n8n | R$ 30 a 50 |
| Tokens de IA | R$ 20 a 40 |
| **Total** | **menos de R$ 100/mês** |

Sem chip, sem reposição, sem risco de banimento.

## Ordem de construção

| Fase | O que | Depende de |
|---|---|---|
| **1** | Autorizar o Clint | **Pablo** (2 min) |
| **2** | Limpar a base, classificar, cruzar com a Biblioteca | Pablo mandar o CSV |
| **3** | Primeira fila de 30 links `wa.me` | fase 2 |
| **4** | Subir n8n + conectar MCP | **Pablo** (VPS) |
| **5** | Montar o agente no n8n | fase 4 — eu monto daqui |
| **6** | Habilitar Cloud API em coexistência | **Pablo** (Meta Business verificado) |
| **7** | Religar `WPP I CONVERSA I FS1` | fase 6 |
| **8** | Corrigir o "90 dias" no formulário | **Pablo** (manual no Gerenciador) |

**As fases 1, 2 e 3 não dependem de nada técnico e já entregam resultado** — é o funil manual
rodando enquanto o resto é construído.

## Decisão em aberto

**Número atual em coexistência, ou número novo só para prospecção?**

- **Atual:** histórico preservado, número com reputação, coexistência resolve. Risco: se algo der
  errado, é o número que ele usa com cliente.
- **Novo:** isola o risco. Custo: começa sem reputação, e número novo mandando para desconhecidos
  é o perfil que mais chama atenção.

**Recomendação: o atual, em coexistência.** O risco real vem de denúncia, e a abordagem com prova
quase não é denunciada. Um número novo trocaria um risco pequeno por um problema de partida.
