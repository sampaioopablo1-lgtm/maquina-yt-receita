# Associações de campo: Meta Ads → CRM → formulário da SDR

Pedido do dono em 27/09/2026: *"Investigue, define você as associações. Associe campos da
Meta, formulário do SDR aos campos do CRM. Com campos da campanha sendo preenchidos, o SDR
deve visualizar ao abrir o formulário de qualificação e agendamento e não perguntar de
novo."*

Este arquivo é a definição. **Nome sem data de propósito** — é para ser atualizado no
lugar.

Tudo aqui foi **medido na conta**, não copiado de documento anterior. Onde a fonte é uma
leitura, ela está citada.

---

## 1. O formulário do Meta faz exatamente TRÊS perguntas

Não foi suposição, e não precisou da API de anúncios (que está fechada — conta
`UNSETTLED`, `is_queryable: false`). A própria Meta deixou a resposta na conta: o contato
de teste que ela injeta (`<test lead: dummy data for …>`) carrega **o nome da pergunta**
dentro do valor de cada campo.

| pergunta no formulário do Meta | campo do CRM | id |
|---|---|---|
| `quando_você_pretende_resolver_isso?` | `Urgência` | `2LnUD4KYSGkIBwiUdzl3` |
| `o_que_você_busca_hoje?` | `Necessidade` | `OJQEsl5dV37pfVY2sIaB` |
| `quanto_você_investe_hoje_por_mês_para_atrair_clientes?` | `Investimento mensal em anúncios` | `bQithNwReQIBGlZBaNlI` |

Mais os padrão: nome → `firstName`, telefone → `phone`, e-mail → `email`.

**Nada além disso chega do anúncio.** Conferido: nenhum `customField` fora dos 56 aparece
nos contatos, e `companyName`, `website`, `city`, `state`, `postalCode` estão todos em
0/64. Resposta não mapeada não vai para campo padrão — desaparece.

### Os vocabulários exatos, lidos dos leads reais

Isto importa porque a §9.1 compara texto, e texto que não bate vale zero.

**`Urgência`** — 2 valores:
`Pra ontem` · `Posso esperar e ver oque acontece`

**`Necessidade`** — 5 valores:
`Já faço anúncios e quero melhorar meus resultados` ·
`Quero aprender a gerar meus próprios leads para o WhatsApp` ·
`Quero contratar alguém para gerar meus leads (Agência).` ·
`Falta de novos clientes` · `Vivemos por indicação`

**`Investimento mensal em anúncios`** — 4 valores:
`Não invisto nada ainda` · `Até R$ 1.000` · `Abaixo de 5k` · `Acima de 10k`

E a picklist configurada no campo é `Até 1k` / `1k a 5k` / `5k a 10k` / `Acima de 10k`.
**Só `Acima de 10k` coincide.** É o G-04, agora com o vocabulário exato dos dois lados —
e é o motivo pelo qual a recomendação é a **opção B** (ler por `Contains`), não arrumar
picklist em nove formulários.

---

## 2. Um defeito de mapeamento achado e corrigido

**Formulário `1026163897118958`**, 8 leads. `Urgência` recebeu `Acima de 10k` e
`Abaixo de 5k` — valores de **investimento** — e `Investimento mensal` ficou **vazio**.

Os 8 leads entraram em **11 segundos** (00:40:29 → 00:40:40) e os valores se alternam, o
que descarta "mudança de versão ao longo do tempo". A leitura que sobra: **esse formulário
manda duas perguntas para o mesmo campo `Urgência`**, e a última sobrescreve a primeira.

| contato | estava | ficou |
|---|---|---|
| CM Construções | `Urgência` = Acima de 10k | `Investimento` = Acima de 10k, `Urgência` vazia |
| Valéria | `Urgência` = Acima de 10k | `Investimento` = Acima de 10k, `Urgência` vazia |
| Francisco | `Urgência` = Abaixo de 5k | `Investimento` = Abaixo de 5k, `Urgência` vazia |
| Marcos Alves da | `Urgência` = Abaixo de 5k | `Investimento` = Abaixo de 5k, `Urgência` vazia |

**Aplicado em 27/09 14:41.** Varri os 64 antes: exatamente 4 casos, nenhum com
`Investimento` já preenchido (zero risco de sobrescrever), e nenhuma contaminação no
sentido inverso.

**Por que limpar a `Urgência` em vez de deixar:** o dado não se perde — ele foi para o
campo certo. O que a `Urgência` guardava era um valor que a SDR leria como "prazo
respondido", quando o prazo desse lead é **desconhecido**. Vazio é a informação honesta
(§1.2 das lições: campo vazio é "ainda não", não "faltou").

**Isto não conserta o formulário.** O mapeamento no GHL continua errado e o próximo lead
desse formulário vai entrar torto. Consertar é tela da integração de Lead Ads.

---

## 3. A associação que responde ao pedido: o que a SDR NÃO pergunta de novo

Esta é a definição central. Para cada campo que o formulário de qualificação pediria, a
decisão é: **o anúncio já respondeu?**

| campo do CRM | o anúncio responde? | o que a SDR faz |
|---|---|---|
| `Prazo` | **SIM** — é a mesma pergunta que `Urgência` | **não pergunta.** Vem derivado |
| `Investe em anúncios` | **SIM** — derivável de `Investimento mensal` | **não pergunta.** Vem derivado |
| `Investimento mensal em anúncios` | **SIM** — direto | **não pergunta.** Só confere |
| `Dor principal` | **parcial** — `Necessidade` dá o vetor | **confirma e aprofunda**, não pergunta do zero |
| `Já teve agência?` | **pista** — `Necessidade` = "Quero contratar alguém (Agência)" | pergunta, com o contexto na tela |
| `Budget` | não | pergunta |
| `Decisor` | não | pergunta |
| `Tem time comercial` | não | pergunta |
| `Clientes novos por mês` | não | pergunta |
| `Quem atende os leads` | não | pergunta |
| `Canal principal de venda` | não | pergunta |
| `Usa CRM` | não | pergunta |
| `Plataformas de anúncio` | não | pergunta **só se** `Investe em anúncios` ≠ `Nunca` |
| `Segmento`, `Site`, `Instagram`, `Empresa` | não | pergunta |

**Resultado: 3 perguntas saem do roteiro da SDR e 2 mudam de "perguntar" para
"confirmar".** É exatamente o "não perguntar de novo" do pedido.

### As duas derivações, com vocabulário fechado

```
Urgência  ->  Prazo
    "Pra ontem"                        -> "Pra ontem"
    "Posso esperar e ver oque acontece" -> "Sem prazo"

Investimento mensal  ->  Investe em anúncios
    "Não invisto nada ainda" -> "Nunca"
    "Até R$ 1.000"           -> "Sim"
    "Abaixo de 5k"           -> "Sim"
    "Acima de 10k"           -> "Sim"
```

**O vocabulário é fechado de propósito, e isso pegou um defeito na minha própria regra
antes de ela rodar.** A primeira versão dizia "qualquer coisa diferente de `Não invisto
nada ainda` significa que investe". Com essa regra, o contato `<test lead>` da Meta
receberia `Investe em anúncios = Sim` derivado de uma **string de teste**. Valor fora do
vocabulário conhecido agora não deriva nada — e o `<test lead>` foi corretamente ignorado.

**Aplicado em 27/09 14:45–14:48, em 37 contatos:**

| derivação | escritas |
|---|---|
| `Prazo` = `Pra ontem` | 32 |
| `Prazo` = `Sem prazo` | 1 |
| `Investe em anúncios` = `Sim` | 17 |
| `Investe em anúncios` = `Nunca` | 15 |

Nenhuma escrita sobrescreveu valor existente: a regra só preenche campo vazio.

**Procedência, para quem auditar:** `Prazo` e `Investe em anúncios` destes 37 contatos
**não foram respondidos pela SDR** — são tradução da resposta que o próprio lead deu no
anúncio. Se um dia a SDR contradisser, a palavra dela vale mais: é ela que falou com a
pessoa.

---

## 4. O formulário de qualificação e agendamento, como ele deve ser

Ordem e comportamento. O que está em **cinza** a SDR lê, não digita.

```
┌─ JÁ RESPONDIDO PELO LEAD NO ANÚNCIO — confira, não pergunte ──────────┐
│  Urgência                          (cinza, leitura)                   │
│  Necessidade                       (cinza, leitura)                    │
│  Investimento mensal em anúncios   (cinza, leitura)                    │
└───────────────────────────────────────────────────────────────────────┘
┌─ DERIVADO DO ANÚNCIO — corrija só se o lead disser outra coisa ───────┐
│  Prazo                             (pré-preenchido, editável)          │
│  Investe em anúncios               (pré-preenchido, editável)          │
└───────────────────────────────────────────────────────────────────────┘
┌─ PERGUNTE AGORA — é o que decide a reunião ──────────────────────────┐
│  Budget                                                                │
│  Decisor                                                               │
│  Dor principal          (a Necessidade acima é o gancho da pergunta)   │
│  Tem time comercial                                                    │
│  Clientes novos por mês                                                │
│  Quem atende os leads                                                  │
│  Canal principal de venda                                              │
│  Usa CRM                                                               │
│  Já teve agência?                                                      │
│  Plataformas de anúncio   (só aparece se Investe em anúncios ≠ Nunca)  │
│  Segmento · Site · Instagram · Empresa                                 │
└───────────────────────────────────────────────────────────────────────┘
```

**Por que a ordem é essa:** a SDR abre o formulário já sabendo o que o lead quer, quando
quer e quanto gasta. Ela entra na ligação com contexto em vez de começar por perguntas que
a pessoa já respondeu para o anúncio — que é a forma mais rápida de queimar a paciência de
um lead que pagou clique para ser atendido.

**O que falta para isso existir na tela:** o formulário em si. `apps/forms.json` do spec
oficial tem apenas `GET /forms/`, `GET /forms/submissions` e
`POST /forms/upload-custom-files` — **não existe rota para criar ou editar formulário**.
Então a montagem é tela, e esta seção é a especificação exata dela.

O que **já está feito** e faz metade do trabalho sem formulário nenhum: os 3 campos do
anúncio e os 2 derivados estão preenchidos no contato, então a SDR que abrir o registro já
vê tudo. O agrupamento em pastas (§4 do `USABILIDADE.md`) é o que coloca isso em blocos
legíveis — e depende da API interna, não do dono.

---

## 5. O que ainda está errado na origem, e não dá para consertar daqui

| problema | escala | onde conserta |
|---|---|---|
| formulário `1026163897118958` manda 2 perguntas para `Urgência` | 8 leads, 4 corrompidos | tela da integração Lead Ads |
| **5 dos 9 formulários não mapeiam nada** | 5 leads entraram só com nome e telefone | tela, formulário por formulário |
| picklist de `Investimento mensal` não bate com nenhum valor real menos um | 24 de 30 | G-04: opção **B** resolve sem tocar em formulário |
| `leadgen_tos_accepted: false` na página | impede criar Lead Ads novo | Meta, do dono |

**A regra que fica:** todo formulário novo de Lead Ads tem de mapear as três perguntas da
§1 para os três campos da §1, com os nomes exatos. Formulário que nasce sem isso entrega
lead cego — e lead cego custa o mesmo clique que lead com contexto.
