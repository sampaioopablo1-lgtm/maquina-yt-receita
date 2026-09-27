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

## 4. O formulário é a FICHA DO CONTATO — tudo dentro do CRM (27/09 17:30)

Decisão do dono às 17:20: *"use outro meio, não o Supabase; tudo pelo CRM, não sair
dele, nenhum sistema ou front-end para os usuários."* O Painel SDR externo (16:00-17:00)
foi **retirado** — código fora do repositório, funções no Supabase inertes (não têm o
token). O que fica é o que cabe dentro do CRM.

### O que a API pública faz e não faz, lido do spec oficial

| | pela API |
|---|---|
| editar o formulário nativo `Qualificação SDR` (campos, ordem, grupos) | **não** — `forms.json` tem só 3 rotas, todas de leitura |
| editar o `Pós-agendamento v2` (pôr o BANT na descrição do evento) | **não** pela pública; **sim** pela interna, que exige `GHL_STORAGE_STATE` |
| **nome** e **posição** de um campo do contato | **sim** — `PUT /locations/{id}/customFields/{id}` |
| criar campo do contato | **sim** — `POST /locations/{id}/customFields`, `model=contact` (feito às 16:53: `SDR responsável`) |
| pasta do campo | **não** no schema; sondado num campo de teste (ver run) |
| lista de usuários do CRM | **sim** — `GET /users/` (hoje 1 usuário: o dono) |
| agenda do closer com disponibilidade | **nativa**: na ficha do contato, aba de compromissos → agendar no calendário `Reunião com closer` (35 horários livres nos próximos 7 dias, medido) |

### A ficha do contato como formulário BANT

A ficha **já é** o formulário que o dono descreveu: mostra todos os campos, **já vem
preenchida** com o que o anúncio trouxe (o SDR confirma, não pergunta), grava direto no
contato (que é o card que o closer abre) e agenda no calendário do closer sem sair da
tela. O que faltava era **ordem e grupo**. `wesales/tools/campos_bant.py` faz isso pela
API — o grupo entra no **nome** do campo e a ordem na **posição**:

| posição | campo (nome novo) | natureza | quem responde |
|---|---|---|---|
| 100–130 | Empresa · Segmento · Instagram · Site | identidade | SDR |
| 200 | **N · Necessidade (anúncio)** | o problema declarado | **anúncio** — confirmar |
| 210 | N · Dor principal | o problema nas palavras do lead | SDR |
| 220–240 | N · Clientes novos por mês · Quem atende os leads · Tem time comercial | tamanho e forma da operação (a nota lê os três) | SDR |
| 250–280 | N · Canal principal de venda · Usa CRM · Já teve agência? · Experiência com agência | contexto | SDR, se der tempo |
| 300 | **T · Urgência (anúncio)** | quando quer resolver | **anúncio** — confirmar |
| 310 | T · Prazo | vocabulário fechado da nota | derivado do anúncio (§3), confirmar |
| 400 | **B · Investimento mensal em anúncios (anúncio)** | quanto já gasta | **anúncio** — confirmar |
| 410 | B · Investe em anúncios | derivado (§3) | confirmar |
| 420–430 | B · Plataformas de anúncio · Budget | onde gasta · tem/precisa aprovar/não tem | SDR |
| 500 | A · Decisor | sim / influencia / não decide | SDR |
| 590 | **SDR responsável** — lista com os usuários do CRM | quem qualificou | SDR escolhe o próprio nome |
| 600–640 | Resultado da tentativa · Data/Hora do retorno · Qualificação · Permissão WhatsApp | fechamento da ligação | SDR |
| 700–720 | Reunião foi qualificada · Motivo da desqualificação · Data do veredito | closer | closer |
| (resto) | os 30 campos que a máquina escreve | não mexer | workflows |

Renomear é seguro **só se o `fieldKey` não mudar** (os merge fields dos workflows, como
`{{contact.nota_de_qualificao}}`, usam a chave). Por isso o script tem dois modos:
`--sondar` cria um campo de teste próprio, renomeia, muda posição, tenta pasta e
opções, mede o que aconteceu e o apaga; `--aplicar` só roda depois, e relê a conta e
sai 1 se não convergir. Modos da Action `wesales-finalizar`: `formulario` = sonda,
`pastas` = aplicar.

**Rotina do SDR, inteira dentro do CRM:** discador (`Fila de ligações`, tag `fila-sdr`)
→ atendeu → abre o contato → confirma os três campos "(anúncio)" → preenche N, T, B, A
de cima para baixo → escolhe o próprio nome em `SDR responsável` → `Resultado da
tentativa = Atendeu` → aba de compromissos, agenda no `Reunião com closer`. O
`Pós-ligação v3` e o `Pós-agendamento v2` fazem o resto (etapa, nota, dono, aviso ao
closer 30 min antes, nota "REUNIÃO AGENDADA" no card).

### O que continua faltando, e o único item que destrava

**A descrição do evento com o BANT inteiro** e **o formulário nativo reorganizado** são
edição de workflow e de formulário: **API interna**, que precisa do `GHL_STORAGE_STATE`.
Gerar esse segredo é uma vez, no PC do dono: `node wesales/tools/login-capture.js`
(abre a janela, o dono faz login, o arquivo vai para o segredo do repositório). Com ele,
a Action `wesales-interno` edita o `Pós-agendamento v2` e publica o `Reunião Cancelada`
que está em rascunho desde a semana passada. Sem ele, o closer recebe a nota
"REUNIÃO AGENDADA · nota X/100" que o workflow já escreve e abre o card — onde está
tudo, na ordem BANT.

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
