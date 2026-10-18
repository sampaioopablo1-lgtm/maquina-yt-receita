# Arquitetura — modo lista, 100% automático

*Desenhada em 14/09/2026 a pedido do Pablo: "pense modelo 100% automatizado, apenas vou subir a lista".*
*Complementa `ARQUITETURA — maquina de prospeccao.md`. O núcleo de conversa é o mesmo; muda só a entrada.*

## O que muda em relação ao desenho anterior

No desenho anterior a IA nunca mandava a primeira mensagem — o Pablo tocava 30 links por dia.
Aqui **o Pablo só sobe o CSV**. A primeira mensagem sai sozinha.

Isso troca a trava 1 por outra, mais precisa:

> **A IA nunca manda primeira mensagem fora de um modelo aprovado pela Meta, pela API oficial.**

Não é disparador em chip. Não é QR Code. É a Meta entregando, com a Meta sabendo.
Custa dinheiro e tem um risco próprio (abaixo). É o preço do "só subo a lista".

---

## O desenho

```
  CSV sobe (Drive ou Sheets)
     │
     ▼
  n8n: limpa, dedupe, normaliza 55+DDD, classifica ICP A/B/C
     │
     ▼
  ENRIQUECE: tem e-mail? não tem → tenta achar (site, CNPJ)
     │
     ├── TEM E-MAIL ──────────────▶ FAIXA GRÁTIS
     │                              cadência de 5 e-mails já pronta
     │                              (CADENCIA — 5 e-mails.md)
     │                              toque 3 leva o link wa.me
     │                              → lead escreve primeiro → grátis
     │
     └── SÓ WHATSAPP ─────────────▶ FAIXA PAGA
                                    modelo de marketing aprovado
                                    30/dia, R$ 0,30 cada
                                    um toque só, com opt-out
     │
     ▼
  LEAD RESPONDE → webhook → n8n → Claude qualifica → agenda no Calendar
                                          → avisa o Pablo
                                          → devolve pro humano nas 5 situações
     │
     ▼
  MEDIÇÃO diária: enviados, entregues, lidos, respostas, bloqueios, nota de qualidade
  AUTO-STOP se passar dos limites (abaixo)
```

---

## As duas faixas

### Faixa grátis — quem tem e-mail

E-mail frio para empresa é permitido no Brasil por interesse legítimo (LGPD Art. 7, IX).
A cadência de 5 toques já existe e já está orçada. O que muda: **o toque 3 carrega o link
`wa.me`** com texto pré-preenchido. Quem clica escreve primeiro → janela de atendimento → grátis
→ IA assume.

Custo do WhatsApp: **R$ 0**. Custo do e-mail: o que já está na cadência.

### Faixa paga — quem só tem WhatsApp

Modelo de marketing aprovado pela Meta, enviado pela Cloud API em coexistência.

| | |
|---|---|
| Volume | 30 contatos novos por dia (limite inicial do número: 250/dia — folga) |
| Preço | R$ 0,30 por mensagem (Brasil, marketing) |
| Por mês | 660 envios = **R$ 198** |
| Os 2.000 inteiros | **R$ 600**, em ~3 meses |
| Resposta do lead e tudo depois | R$ 0 (janela de atendimento; cota de 1.000/mês a partir de 01/10) |

**O modelo tem que ser honesto.** Diz quem é, por que está escrevendo (a prova específica do
anúncio dele), e como parar de receber. Modelo genérico é reprovado pela Meta e, se passar,
é denunciado pelo lead. Um modelo por segmento, com variáveis: `{{nome}}`, `{{prova}}`.

**Um toque só.** Quem não respondeu não recebe segundo modelo. Cadência só depois de engajar.

---

## O risco próprio desta faixa, dito sem rodeio

A política da Meta pede opt-in para mensagem iniciada pela empresa. Lista fria B2B não tem.
A Meta não bloqueia por isso na hora — ela **mede**: cada "bloquear" ou "denunciar" derruba a
nota de qualidade do número. Nota cai → limite diário cai → em caso extremo, número restrito.

Não é o mesmo risco do chip (detecção de robô, 48h, definitivo). É mais lento, é visível no
painel, e dá para parar antes de doer. Por isso o auto-stop existe.

**Se a lista for fria demais, a faixa paga vai se desligar sozinha.** E aí sobra a faixa grátis
e o anúncio. Isso é o sistema funcionando, não falhando.

---

## Auto-stop — a máquina se desliga sozinha quando

| Sinal | Limite | Ação |
|---|---|---|
| Bloqueios / enviados | > 2% no dia | pausa a faixa paga, avisa o Pablo |
| Nota de qualidade do número | sai de "alta" | pausa a faixa paga, avisa o Pablo |
| Taxa de resposta | < 5% em 3 dias seguidos | pausa e revisa o modelo antes de seguir |
| Erro 131049 (limite de marketing por pessoa) | qualquer | pula o contato, tenta em 7 dias |
| Modelo reprovado ou pausado pela Meta | qualquer | para tudo, avisa o Pablo |

Religar é sempre decisão do Pablo, nunca da máquina.

---

## O que o Pablo faz

1. **Sobe o CSV.** Só isso, no dia a dia.
2. Uma vez: verificar o Meta Business e habilitar a Cloud API em coexistência.
3. Uma vez: aprovar o texto do modelo (eu escrevo, ele diz sim, eu submeto à Meta).
4. Atender as reuniões que caírem na agenda.

## O que a máquina faz

Tudo o mais. Limpa, enriquece, decide a faixa, envia, espera, responde, qualifica, agenda,
mede, para quando tem que parar, e manda o relatório do dia.

---

## Custo mensal total

| Item | Valor |
|---|---|
| Faixa grátis (e-mail) | já orçado na cadência |
| Faixa paga (30/dia) | **R$ 198** |
| IA respondendo | R$ 0 (cota) |
| Servidor n8n | R$ 30 a 50 |
| Tokens Claude | R$ 20 a 40 |
| **Total** | **~R$ 250 a 290/mês** enquanto a faixa paga roda; **< R$ 100** depois |

A faixa paga tem fim: acaba a lista, acaba o custo. O resto fica.

---

## Ordem de construção

| Fase | O que | Depende de |
|---|---|---|
| 1 | Limpar, classificar, enriquecer o CSV | **Pablo mandar o CSV** |
| 2 | Cadência de e-mail com link wa.me no toque 3 | fase 1 |
| 3 | Subir n8n + MCP | **Pablo** (VPS) |
| 4 | Agente de conversa no n8n | fase 3 — monto daqui |
| 5 | Cloud API em coexistência | **Pablo** (Meta Business verificado) |
| 6 | Escrever e submeter o modelo | fase 5 + Pablo dizer sim ao texto |
| 7 | Ligar a faixa paga com auto-stop | fase 6 |
| 8 | Religar `WPP I CONVERSA I FS1` | fase 5 |

**Fases 1 e 2 já rodam sem WhatsApp nenhum** e já geram conversa grátis.

## O que continua fora

Multi-chip, aquecimento, intervalo aleatório, rodízio de número, QR Code. Nenhum entra.
O "100% automático" aqui é pela porta da frente da Meta, pagando o que ela cobra.
