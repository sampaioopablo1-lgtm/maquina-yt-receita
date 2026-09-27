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

## 4. O formulário virou o **Painel SDR** — e por quê (27/09 16:50)

O dono pediu, em 27/09 às 16:00: pré-preencher com o que veio do anúncio (o SDR só
confirma), ordem BANT (Necessidade, Tempo, Investimento, Autoridade), agenda do closer
na mesma tela com a disponibilidade real, closer recebendo tudo no card e na descrição
do evento, seletor do SDR puxado da lista de usuários do CRM. E: *"estude a fundo a API,
para que eu não precise fazer nada manual"*.

**Estudei o repositório oficial da API (`GoHighLevel/highlevel-api-docs`, clonado).** O
resultado é binário:

| o formulário nativo (`DNz54AK2ryRSW7uCuznP`) | pela API |
|---|---|
| editar campos, ordem, grupos | **não existe rota** — `forms.json` tem só `GET /forms/`, `GET /forms/submissions`, `POST /forms/upload-custom-files` |
| ler o contato ao abrir e pré-preencher | o widget não lê contato; abre vazio |
| mostrar a agenda do closer | o formulário não tem elemento de calendário |
| listar usuários do CRM num campo | não tem |

| o que o dono pediu | rota da API que faz | conferida no spec |
|---|---|---|
| ler o contato com os campos do anúncio | `GET /contacts/{id}` | sim |
| lista de usuários para o seletor de SDR | `GET /users/?locationId=` | sim |
| horários livres do closer | `GET /calendars/{id}/free-slots?startDate&endDate&timezone` | sim (janela ≤ 31 dias) |
| criar a reunião já confirmada, com tudo na descrição | `POST /calendars/events/appointments` com `description`, `appointmentStatus=confirmed`, `toNotify=true` | sim |
| gravar os campos BANT no contato | `PUT /contacts/{id}` `customFields[{id, field_value}]` | sim |
| tudo no card do closer | `POST /contacts/{id}/notes` | sim |
| campo novo `SDR responsável` | `POST /locations/{id}/customFields` com `model=contact` | sim — **a rota antiga aceita contato**; a nova (`/custom-fields/`) recusa (lição 2.19). Corrijo o que escrevi na §4-BIS: campo de contato **pode** ser criado por API; **pasta** continua não |

Então a resposta honesta ao pedido é: **o formulário nativo não chega lá por nenhum
caminho; uma página sobre a API chega em todos.** Construí a página.

### O Painel SDR — o que é

`supabase/functions/painel-sdr/` (Edge Function, Deno; `painel.html` é a tela). Endereço:

```
https://cscczluzpblzhvojxanp.supabase.co/functions/v1/painel-sdr
```

Entra-se com um **PIN** (o token do GHL fica no servidor; nunca vai ao navegador). O SDR
escolhe o próprio nome no topo — **lista viva de `GET /users/`**, não uma lista digitada.

**Tela, da esquerda para a direita:**

1. **Contato** — busca por nome/telefone/e-mail, ou o botão **Minha fila de hoje**, que
   puxa a tag `fila-sdr` (a mesma que o discador puxa: uma fila, dois lugares).
2. **Resultado da ligação (sem atendimento)** — um botão por opção do vocabulário de
   `Resultado da tentativa` (`Não atendeu`, `Caixa Postal`, `Pediu retorno` com data/hora,
   `Número errado`, `Não ligar`, `Desqualificado`). Um clique grava o campo, o
   `Pós-ligação v3` dispara, e o painel abre o próximo da fila. **É o elo fraco da rotina
   do discador, fechado.**
3. **O formulário, em grupos BANT** — natureza de cada pergunta identificada:

| grupo | campo | natureza | origem |
|---|---|---|---|
| **N · Necessidade** | Necessidade | o problema declarado | **anúncio** — mostrado em caixa amarela "respondeu no anúncio", não se pergunta; link *corrigir* se o SDR ouvir diferente |
| | Dor principal | o problema nas palavras do lead | SDR |
| | Clientes novos por mês · Quem atende os leads · Tem time comercial | tamanho e forma da operação (a nota lê os três) | SDR |
| | *(+ mais detalhes, recolhido)* Canal principal de venda · Usa CRM · Já teve agência? · Experiência com agência · Instagram · Site | contexto; não trava a ligação | SDR, se der tempo |
| **T · Tempo / urgência** | Urgência | quando quer resolver | **anúncio** — caixa amarela |
| | Prazo para começar | vocabulário fechado da nota | derivado do anúncio (§3), editável |
| **B · Investimento** | Investimento mensal em anúncios | quanto já gasta | **anúncio** (pré-selecionado; editável porque há dois vocabulários) |
| | Investe em anúncios hoje? | derivado (§3) | pré-selecionado, editável |
| | Plataformas de anúncio | onde gasta | SDR |
| | Budget para o projeto | tem / precisa aprovar / não tem | SDR |
| **A · Autoridade** | Decisor | sim / influencia / não decide | SDR |
| | Observações para o closer | texto livre | SDR |

   `Empresa` e `Segmento` ficam no cabeçalho do contato.

4. **Agenda do closer** — calendário `Reunião com closer` (`3uNQFjCEDe7b4gKZJuOZ`): 7 dias de
   horários livres reais, por `free-slots`, fuso `America/Sao_Paulo`. O SDR clica no
   horário combinado com o lead.
5. **Salvar** ou **Salvar e agendar** — em ordem:
   1. `PUT /contacts` com os campos + `Qualificação = SDR` + `SDR responsável = <nome>` +
      `Resultado da tentativa = Atendeu` (caixa marcada por padrão — dispara o
      `Pós-ligação v3`, que tira o lead das cadências e zera os contadores certos);
   2. `POST /calendars/events/appointments` **confirmado**, título *"Reunião de diagnóstico —
      Nome (Empresa)"*, **descrição = o BANT inteiro** (bloco por grupo + observações), o
      que dispara o `Pós-agendamento v2` (move para REUNIÃO DE DIAGNÓSTICO, calcula a
      nota, atribui dono, notifica o closer 30 min antes — tudo lido do roteiro publicado);
   3. `POST /contacts/{id}/notes` com a mesma descrição — **o closer abre o card e vê
      tudo sem abrir o evento.**

O painel **não** move etapa nem calcula nota: isso é dos workflows publicados, que
continuam donos das regras. Ele só produz os dois eventos que eles já esperam. Nunca
apaga contato, oportunidade ou lead.

### O que está feito e o que está travado

| | estado |
|---|---|
| código do painel (`index.ts`, `painel.html`, gerador) | no repositório |
| Edge Function publicada no Supabase (`cscczluzpblzhvojxanp`) | **no ar**, versão 1 |
| tabela `config` + PIN | criados |
| **token do GHL dentro do painel** | **NÃO** — ver abaixo |
| campo `SDR responsável` no CRM | **criado pela API** (run 36334862059): `LoSi8PQCbBRjmkMC8CH8`, HTTP 201, relido depois |

**Por que o token não entrou.** Primeira tentativa: gravar por PostgREST no projeto
`maquina-yt-dark` → **HTTP 402** *"restricted due to exceed_storage_size_quota"* (run
36333419041) — o projeto está com o gateway bloqueado por cota de storage, o mesmo
episódio de 25/08 documentado em `docs/publicar-na-virada-da-cota.md`. Mudei o painel
para o projeto saudável e criei a rota `POST /api/instalar` (aceita o token **uma única
vez**, e só se o GHL o reconhecer). A escrita do token por essa rota, a partir da Action,
foi **bloqueada pela política de segurança da sessão** ("gravação de segredo em serviço
externo"). Não vou contornar. Duas saídas, qualquer uma leva 1 minuto do dono:

1. **Autorizar** a Action a fazer isso (regra de permissão na sessão) — aí
   `wesales-finalizar` modo `formulario` entrega o token, cria o campo, sonda e prova
   `/api/saude`.
2. **Fazer à mão, uma vez:** no Supabase → projeto *sampaioopablo1-lgtm's Project* →
   Table editor → `config` → nova linha `chave = ghl_pit`, `valor = {"token":"<o PIT>"}`.
   Depois abrir `<endereço>/api/saude`: deve responder `"ok":true` com o número de usuários.

Sem o token o painel abre, pede o PIN e responde *"ghl_pit nao configurado"*. Nada
quebra no CRM.

**17:00 — o bloqueio é maior: a restrição de cota é da ORGANIZAÇÃO Supabase, não de um
projeto.** O run 36334772280 chamou `/api/saude` no projeto novo e recebeu o mesmo
**HTTP 402** *"restricted due to exceed_storage_size_quota — the project owner must
upgrade their plan or remove spend caps"*. Ou seja: **nenhuma Edge Function da conta
responde ao público** enquanto isso durar — é o episódio de 25/08 (`docs/publicar-na-
virada-da-cota.md`) ainda em vigor. A função está publicada e correta; o gateway na
frente dela está fechado pela conta.

Então a ordem real das saídas, todas do dono, é:

1. **Liberar a conta Supabase** (painel do Supabase → organização → *spend cap* / plano,
   ou apagar storage do `maquina-yt-dark` pelo dashboard). Sem isso nem o painel nem a
   `ponte` respondem. **Este é o item que destrava tudo.**
2. **Token**: linha `ghl_pit` na tabela `config` do projeto `cscczluzpblzhvojxanp`, ou
   autorizar a regra de permissão para a Action entregar.
3. Abrir `<endereço>/api/saude` e ver `"ok":true`.

Se a conta Supabase não for liberada até terça, o plano B é hospedar a mesma função em
outro lugar (Netlify Functions — há conector; o código é Deno/TS puro e porta em
minutos). Não fiz porque a hospedagem alternativa também precisaria do token, e o
token esbarra no mesmo ponto 2.

### O que a sonda do run 36334862059 mediu (vale para o painel e para a rotina)

| | medido |
|---|---|
| usuários no CRM (a lista do seletor de SDR) | **1** — `Pablo Santos` (`JdvhvOTEBTvUyRi0BXU8`). **O SDR precisa de um usuário próprio no CRM** (Configurações → Equipe) para aparecer na lista e para o `SDR responsável` ter o nome certo. Criar usuário por API é escopo de agência; é tela do dono, 1 minuto |
| calendário `Reunião com closer` | ativo, slot de **1 hora**, equipe = o dono. O painel passa `assignedUserId` = dono, porque a equipe tem um só membro |
| horários livres, próximos 7 dias | **35** (5 por dia, sáb 27/09 a sex 03/10) — a agenda do closer aparece no painel com esses |
| menu lateral no WeSales por API (`/custom-menus/`) | **401** com este token — é escopo de agência. O painel fica em favorito do navegador, não na barra lateral |

### O formulário nativo `Qualificação SDR`

Não precisa ser apagado (é do dono e não custa nada), mas **não deve ser usado**: pelo
link público cria lead novo (§4-BIS) e não faz nada do que está acima. A rotina do SDR
passa a ser: discador na aba `Fila de ligações` + painel aberto ao lado.

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
