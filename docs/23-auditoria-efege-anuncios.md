# Auditoria da conta de anúncios ÉFGE

Levantada em 17/09/2026 via Meta Ads MCP. Conta `507623595571273`
("EFGE - T7", BM *FG Móveis*, BRL, status ACTIVE, Opportunity Score **86/100**).
Página promovida: ÉFGE Móveis Planejados (`1927123870636305`).

Janela principal: **últimos 30 dias (18/08 → 16/09/2026)**, comparada com os
30 dias anteriores (19/07 → 17/08/2026).

## O número que importa

| Métrica | 19/07–17/08 | 18/08–16/09 | Variação |
|---|---|---|---|
| Investimento | R$ 4.077,22 | R$ 3.700,55 | −9,2% |
| Leads (formulário) | 110 | 84 | **−23,6%** |
| CPL na campanha de leads | R$ 33,20 | R$ 33,99 | +2,4% |
| **CPL sobre o gasto total da conta** | R$ 37,07 | **R$ 44,05** | **+18,8%** |

O CPL "de vitrine" está estável, mas a conta entregou 26 leads a menos gastando
R$ 377 a menos. A conta piorou 18,8% no custo por lead real porque o volume caiu
mais rápido que a verba e porque 23% do dinheiro (R$ 845) foi para
reconhecimento e tráfego, que não devolvem lead atribuído.

E as três únicas campanhas que entregam estão **todas com custo por resultado
subindo** (tendência da própria Meta):

| Conjunto entregando | CPR | CTR | CVR |
|---|---|---|---|
| EFGE I 13/08 INFLUENCER — RMK | +13,0% ✗ | +4,2% ✓ | **−21,8% ✗** |
| EFGE I FORMS I 29/05 INFLUENCER | **+182,6% ✗** | −64,1% ✗ | +2,7% ✓ |
| EFGE I INSTAGRAM I 03/07 | +51,0% ✗ | −11,5% ✗ | — |

## Para onde foi a verba (30 dias)

| Campanha | Objetivo | Gasto | % | Resultado | Custo/result. |
|---|---|---|---|---|---|
| EFGE I FORMS I 29/05 INFLUENCER | LEADS | R$ 2.855,31 | 77,2% | 84 leads | R$ 33,99 |
| EFGE I RECONHECIMENTO — público quente | AWARENESS | R$ 561,68 | 15,2% | 23.366 ThruPlay | R$ 0,02 |
| EFGE I TRAFEGO I 03/07 instagram | ENGAGEMENT | R$ 283,56 | 7,7% | 346 visitas ao perfil | R$ 0,82 |

Todo o resto da conta gastou **R$ 0,00**.

## Cinco problemas, em ordem de dinheiro

### 1. 88% da verba de lead está no conjunto 60% mais caro

| Conjunto | Meta | Gasto | Leads | CPL | Freq. | Público |
|---|---|---|---|---|---|---|
| EFGE I 13/08 INFLUENCER — RMK | QUALITY_LEAD | R$ 2.513,60 | 69 | **R$ 36,43** | 2,67 | 11,6k–13,6k |
| EFGE I FORMS I 29/05 INFLUENCER | QUALITY_LEAD | R$ 341,71 | 15 | **R$ 22,78** | 1,63 | prospecção |

O conjunto de remarketing leva 88% do orçamento a um CPL 60% maior que o de
prospecção. Pior: ele roda sobre um público de 11,6k–13,6k pessoas (a Meta já
sinaliza como "restrito") e já bateu frequência 2,67 em 30 dias — que é
exatamente o desenho de fadiga que aparece no CVR caindo 21,8%.

O conjunto de tráfego no Instagram roda em público ainda menor: **3,8k–4,5k**.

### 2. A malha de leads qualificados está furada

Dois conjuntos ainda pedem otimização por *Leads qualificados*
(`QUALITY_LEAD`), mas a Meta devolve a coluna como "Not available" e continua
recomendando `conversion_leads_optimization` (+3 pontos, "CPL qualificado 24%
menor"). O motivo está nos datasets:

| Dataset | Estado | Último evento |
|---|---|---|
| `[Efge][Forms][Conjunto de Dados]` | ativo, **em lotes** | 16/09/2026 |
| `EFGE Offline Tintim` | **zero eventos em 28 dias** | 20/07/2026 |
| `Pixel T7` | parado | 01/05/2026 |
| `pixelfgmoveis` | ativo | 16/09/2026 |
| `Marcenaria em São Caetano do Sul` | **nunca disparou** | — |
| `FG MOVEIS 1` | **nunca disparou** | — |

O feed de status do CRM chega aos trancos: nos 30 dias houve 69 `QUALIFIED`,
35 `SCHEDULED` e 24 `DISQUALIFIED`, mas **57 dos qualificados entraram todos no
dia 08/09** num único lote — e ainda aparecem rótulos soltos em português
(`AGENDADO`, `CRIADO`) misturados aos nomes canônicos.

Otimização por lead qualificado aprende com retorno rápido e nomenclatura
estável. Do jeito que está, o algoritmo recebe o veredito do lead semanas
depois, em lote, com nome trocado — ou seja, não recebe. O offline do Tintim,
que deveria fechar esse ciclo, morreu em 20/07.

### 3. 16 campanhas "Ativas" que não existem mais

Nas 50 campanhas da primeira página, 19 estão marcadas ACTIVE — mas só 3
entregam. As outras 16 têm conjuntos ACTIVE, com orçamento diário definido, e
**data de término no passado**. Conferi seis delas:

| Conjunto ACTIVE | Orçamento/dia | Terminou em |
|---|---|---|
| CONJUNTO ALTO PADRÃO | R$ 50 | 31/10/2025 |
| CONJUNTO ALTO PADRÃO | R$ 100 | 03/10/2025 |
| PLANEJADOS AGOSTO | R$ 120 | 31/08/2025 |
| Cozinhas | R$ 70 | 04/08/2025 |
| RECEBER MENSAGENS WHATS 09/06 | — | 16/06/2025 |
| Campanha leads Formulario 2 | R$ 70 | 12/06/2025 |

Somando os conjuntos ACTIVE parados, são **R$ 690/dia de orçamento configurado**
esperando apenas alguém estender uma data. Não gastam hoje (a agenda venceu), e
por isso não é sangria — é armadilha: qualquer edição de período reativa
R$ 20 mil/mês de anúncios de 2025. Enquanto isso, o Gerenciador fica ilegível.

### 4. 14 anúncios de lead disputando R$ 2.855

Seis anúncios receberam menos de R$ 20 em 30 dias e nunca saíram do
aprendizado — e a Meta cobra caro por essas migalhas:

| Anúncio | Gasto | Leads | CPL | CPM | Qualidade |
|---|---|---|---|---|---|
| AP FB INFLUENCER 02 | R$ 1.560,76 | 46 | R$ 33,93 | R$ 29,91 | **Acima da média** |
| CLOSET FB INFLUENCER 01 | R$ 429,17 | 10 | R$ 42,92 | R$ 33,57 | Média |
| ADS 03 FB narrado | R$ 422,36 | 10 | R$ 42,24 | R$ 45,71 | Média |
| AP FB INFLUENCER 02 Casal | R$ 197,43 | 7 | **R$ 28,20** | R$ 28,34 | Média |
| CLOSET FB INFLUENCER 01 (prosp.) | R$ 111,59 | 5 | **R$ 22,32** | R$ 23,91 | — |
| AP FB INFLUENCER 02 (prosp.) | R$ 26,27 | 3 | **R$ 8,76** | R$ 28,25 | Acima da média |
| ADS 03 FB copy T7 | R$ 54,86 | 2 | R$ 27,43 | **R$ 89,20** | Média |
| ADS 01 | R$ 16,37 | 1 | R$ 16,37 | **R$ 83,52** | — |
| ADS 02 / ADS 03 FB / ADS 03 FB / ADS 06 / ADS 05 / ADS 04 | R$ 36,50 | **0** | — | R$ 40–92 | — |

Os anúncios famintos rodam com CPM de R$ 67 a R$ 92, contra R$ 29–34 dos que
entregam. `AP FB INFLUENCER 02` é o criativo da casa: é o único "Acima da média"
com volume, e na prospecção fez lead a R$ 8,76.

### 5. Cobrança e placements

- Três anúncios (da campanha `EFGE I FORMS I 29/05`, hoje pausada) carregam erro
  **"Your account is unsettled"** — saldo em aberto que falhou na cobrança. A
  conta aparece como ACTIVE e com meio de pagamento, então é provável resíduo de
  uma cobrança antiga; mas **cinco outras contas do mesmo login estão UNSETTLED
  agora**, então vale abrir a Central de Faturamento antes de subir verba.
- A página ÉFGE aparece com `leadgen_tos_accepted: false`. Campanhas de
  formulário já rodam, mas esse flag bloqueia a criação de novos conjuntos de
  lead — conferir em [facebook.com/legal/leadgen/tos](https://www.facebook.com/legal/leadgen/tos).
- Os dois conjuntos de lead estão **só no Instagram** (`publisher_platforms:
  [instagram]`). O conjunto de tráfego, que inclui Facebook, é o de melhor CTR da
  conta (3,27% contra 1,63%).
- A Meta sinaliza duas campanhas elegíveis a **Reels** (`+2 pontos`) e uma que
  roda só um formato (`mixed_formats`, `+1 ponto`).

## Plano, em ordem

1. **Faturamento** — resolver/confirmar o saldo em aberto e o ToS de lead da
   página. Sem isso, qualquer escala é falsa.
2. **Fechar o ciclo do lead qualificado** — padronizar os status em
   `QUALIFIED` / `SCHEDULED` / `DISQUALIFIED` (sem `AGENDADO`/`CRIADO`) e passar
   o envio de lote semanal para diário via CAPI; reativar ou desligar de vez o
   `EFGE Offline Tintim`. É a única mudança que ataca o CPL qualificado na raiz
   (a própria Meta estima −24%).
3. **Rebalancear** — mover R$ 30–40/dia do conjunto RMK para a prospecção, que
   faz lead 60% mais barato, e ampliar o público do RMK (11,6k é pequeno demais
   para frequência 2,67 e CVR caindo).
4. **Consolidar criativos** — desligar os 6 anúncios com menos de R$ 20 em 30
   dias; manter `AP FB INFLUENCER 02`, `AP FB INFLUENCER 02 Casal`,
   `CLOSET FB INFLUENCER 01` e `ADS 03 FB narrado`. Menos anúncios, CPM menor.
5. **Limpar a conta** — pausar/arquivar as 16 campanhas ACTIVE com agenda
   vencida e zerar os R$ 690/dia de orçamento configurado nelas.
6. **Testes seguintes** — abrir placements de Facebook nos conjuntos de lead
   (o CTR lá é o dobro) e aceitar o opt-in de Reels nas duas campanhas
   sinalizadas.

## Como refazer este levantamento

```
ads_get_ad_accounts                    # acha 507623595571273 ("EFGE - T7")
ads_get_ad_entities  level=campaign|adset|ad, date_preset=last_30d
ads_get_errors       entity_ids=[507623595571273]
ads_get_opportunity_score
ads_insights_anomaly_signal
ads_insights_performance_trend
ads_insights_auction_ranking_benchmarks
ads_get_datasets     +  ads_get_dataset_stats aggregation=event
```

`ads_account_get_activity_logs` (histórico de alterações) ainda não está
liberado para esta conta — o histórico de quem mudou o que teve de ser inferido
por `updated_time`.

---

# Aprofundamento: os microajustes

Segunda passada, em 17/09/2026, descendo a placement, faixa de idade, público,
criativo e qualidade de sinal. Cada item traz o valor **atual** e o **alvo**,
para poder ser executado sem reinterpretação.

## 0. O que quebrou entre 15 e 17/09

O dia a dia da campanha de leads, para contexto de urgência:

| Dia | Gasto | Impressões | CPM | Leads |
|---|---|---|---|---|
| 10/09 | R$ 173,28 | 5.043 | R$ 34,36 | 7 |
| 11/09 | R$ 172,09 | 5.305 | R$ 32,44 | 3 |
| 12/09 | R$ 168,77 | 6.129 | R$ 27,54 | 7 |
| 13/09 | R$ 114,98 | 3.911 | R$ 29,40 | 6 |
| 14/09 | R$ 125,98 | 4.473 | R$ 28,16 | 4 |
| 15/09 | R$ 114,88 | 2.563 | R$ 44,82 | 2 |
| 16/09 | R$ 103,45 | 2.140 | R$ 48,34 | **0** |
| 17/09 (parcial) | R$ 59,23 | 1.109 | R$ 53,41 | **0** |

CPM quase dobrou e a entrega caiu a um quinto. O gasto converge para os
R$ 100/dia de orçamento da campanha, o que sugere um corte de verba por volta de
13/09 — não confirmável aqui, porque `ads_account_get_activity_logs` não está
liberado nesta conta.

## 1. Sinal: o EMQ do evento qualificado é 0

O diagnóstico mais duro da conta. No dataset `[Efge][Forms]`
(`2367389037119638`):

| Canal | Evento | Composite score | Match keys |
|---|---|---|---|
| web | `QUALIFIED` | **0** | nenhuma |
| crm | `QUALIFIED` | **0** | nenhuma |

Score 0 com `match_key_feedback` vazio significa que os eventos chegam **sem
nenhum identificador** — sem e-mail, telefone, `fbc`/`fbp`, nada com que a Meta
possa casar o lead qualificado à pessoa que clicou. Somado a isso,
`ads_get_customconversions` devolve **zero conversões personalizadas** na conta.

Ou seja: não é só o lote atrasado. Otimizar por `QUALITY_LEAD` hoje é pedir ao
algoritmo que aprenda com um sinal que ele literalmente não consegue atribuir a
ninguém. É por isso que a coluna *Leads qualificados* volta "Not available".

**Microajustes:**
- Enviar, em cada evento de status, ao menos `em` (e-mail com hash) e `ph`
  (telefone com hash E.164) — os dois campos que o formulário já coleta — mais
  `lead_id` do formulário para fechar o laço.
- Repassar `fbc`/`fbp` quando o lead vier de site; nos leads de formulário, usar
  o `lead_id` como chave.
- Padronizar a nomenclatura: só `QUALIFIED`, `SCHEDULED`, `DISQUALIFIED`.
  Hoje convivem `AGENDADO` (1 evento) e `CRIADO` (1 evento) — cada rótulo novo
  vira um evento separado aos olhos da Meta.
- Passar o envio de lote semanal para **diário**, idealmente horário via CAPI.
  Referência do que está acontecendo: 57 dos 69 `QUALIFIED` do mês entraram
  todos no dia 08/09.
- Criar a conversão personalizada de lead qualificado (hoje não existe nenhuma)
  e só então religar `QUALITY_LEAD`. Até lá, `LEAD_GENERATION` entrega mais
  previsível.
- Decidir o destino do `EFGE Offline Tintim` (`1146055467653750`): **zero
  eventos em 28 dias**, último em 20/07/2026. Ou reconecta ou desativa, para não
  poluir o diagnóstico.
- Arquivar `Pixel T7` (parado em 01/05/2026), `Marcenaria em São Caetano do Sul`
  e `FG MOVEIS 1` (**nunca dispararam**).

## 2. Placement: Stories carrega a conta, Feed sangra

Mesma janela de 30 dias, os dois conjuntos de lead somados:

| Placement | Gasto | % verba | Leads | % leads | CPL |
|---|---|---|---|---|---|
| Instagram Stories | R$ 1.380,67 | 48,4% | 46 | 54,8% | **R$ 30,01** |
| Instagram Reels | R$ 923,65 | 32,3% | 25 | 29,8% | R$ 36,95 |
| Instagram Feed | R$ 551,01 | 19,3% | 13 | 15,5% | **R$ 42,39** |

Aberto por conjunto, a diferença fica mais nítida — e inverte:

| Conjunto | Stories | Reels | Feed |
|---|---|---|---|
| RMK (`120255016298420226`) | R$ 33,67 | R$ 34,81 | **R$ 51,91** |
| Prospecção (`120253830178070226`) | **R$ 14,99** | **R$ 61,51** | R$ 20,95 |

**Microajustes:**
- No RMK, cortar Feed (`instagram_positions` sem `stream`): 18,6% da verba
  produzindo lead 54% mais caro que Stories.
- Na prospecção, cortar Reels: R$ 123,03 para 2 leads a R$ 61,51, enquanto
  Stories fez 9 leads a R$ 14,99 com verba parecida.
- Não generalizar: Reels é bom no RMK (R$ 34,81) e ruim na prospecção. O ajuste
  é por conjunto, não por conta.
- Aceitar os dois opt-in de Reels que a Meta sinaliza (`+2 pontos`) apenas nas
  campanhas onde Reels já converte.

## 3. Idade: 55+ custa 2,4x e entrega 4,8%

Os dois conjuntos de lead somados:

| Faixa | Gasto | % verba | Leads | CPL |
|---|---|---|---|---|
| 25–34 | R$ 917,40 | 32,1% | 28 | R$ 32,76 |
| 35–44 | R$ 970,73 | 34,0% | 33 | **R$ 29,42** |
| 45–54 | R$ 660,36 | 23,1% | 19 | R$ 34,76 |
| 55–64 | R$ 215,62 | 7,6% | 3 | **R$ 71,87** |
| 65+ | R$ 85,03 | 3,0% | 1 | **R$ 85,03** |
| idade/gênero desconhecidos | R$ 6,17 | 0,2% | 0 | — |

**25–54: R$ 2.548,49 → 80 leads → CPL R$ 31,86.
55+: R$ 300,65 → 4 leads → CPL R$ 75,16.**

O CPM escala de forma brutal com a idade dentro desse raio: 25–34 feminino custa
R$ 19,39/mil; 65+ feminino, R$ 105,99/mil — **5,5x**. É o sinal clássico de
público pequeno demais: a Meta paga caro para achar gente mais velha dentro de
4–8 km.

Recortes com gasto e **zero lead**: 55–64 masculino (R$ 44,03), 65+ masculino
(R$ 25,31), 35–44 masculino na prospecção (R$ 23,41), 45–54 masculino na
prospecção (R$ 17,24).

**Microajustes:**
- Fechar em `age_min: 27, age_max: 54`. Libera ~R$ 300/mês que hoje compra 4
  leads a R$ 75.
- Atenção ao detalhe que faz isso falhar: os dois conjuntos estão com
  `targeting_automation.advantage_audience: 1`, e com Advantage+ Audience ligado
  **a faixa de idade é tratada como sugestão, não como teto** — é por isso que
  há entrega em 65+ com `age_max: 65`. Para virar teto de verdade é preciso
  `advantage_audience: 0`.
- Não cortar por gênero. A tentação existe, mas o CPL por gênero está
  equilibrado no RMK (feminino R$ 36,62, masculino R$ 35,45); o desequilíbrio é
  de idade, não de gênero.

## 4. Público: o funil se estrangula no cruzamento

O conjunto RMK empilha três coisas ao mesmo tempo: união de 3 públicos de
engajamento (`T7 - INST` 8,5–10k, `T7 - FACE` 1,2–1,5k, `T7 - VV` 22,6–26,6k),
**mais** dois blocos de interesses, **mais** raio de 4 km e 8 km. A união dos
públicos daria ~32–38 mil pessoas; o cruzamento com interesse e geo derruba o
alcance estimado para **11,6–13,6 mil**. Com frequência 2,67 em 30 dias, é esse
cruzamento que produz o CPM de R$ 48 do dia 16.

E há 26 públicos personalizados na conta, **14 deles INACTIVE**:

| Público | Tamanho | Status |
|---|---|---|
| `T7 - VV` | 22.600–26.600 | ACTIVE |
| `T7 - INST` | 8.500–10.000 | ACTIVE |
| `T7 - FACE` | **1.200–1.500** | ACTIVE |
| `RMK 90d` | 3.500–4.100 | ACTIVE |
| `Lista C.N. EFGE` (lista subida) | **1.000** | ACTIVE |
| 13 semelhantes 1% | **todos em 1.000** | 11 INACTIVE |
| `visitou instagram`, `videi v 25%` (de 2024) | 1.000 | INACTIVE |

Os semelhantes de 1% para o Brasil deveriam ter ~1,4 milhão de pessoas. Estão
todos travados no piso de 1.000 e a maioria INACTIVE — inclusive os três criados
em 13/08 a partir de `T7 - FACE`/`INST`/`VV`, que um mês depois nunca ficaram
utilizáveis. Semente pequena não gera semelhante.

**Microajustes:**
- Soltar o cruzamento no RMK: remover os interesses e deixar só público +
  geo. Remarketing com filtro de interesse por cima é redundante — quem já
  interagiu já é o sinal.
- Ampliar o raio de 4 km/8 km para 12–15 km, ou trocar os dois raios pela
  cidade de Santo André + São Caetano, como o conjunto de reconhecimento já faz.
- **Excluir quem já é lead.** Nenhum dos dois conjuntos tem
  `excluded_custom_audiences`: quem preencheu o formulário continua recebendo o
  mesmo anúncio. Criar o público de quem abriu/enviou o formulário e excluir
  dos dois.
- Excluir o público do RMK da prospecção. Hoje um engajado que também casa com
  os interesses entra nos dois conjuntos — a conta disputa leilão contra si
  mesma, exatamente o que o diagnóstico de sobreposição da Meta penaliza.
- Parar de gerar semelhantes de 1% sobre sementes de 1.000–1.500 pessoas.
  Juntar `T7 - VV` (a única semente com massa) numa base única antes de
  derivar; e alimentar `Lista C.N. EFGE` com a base real de clientes, que hoje
  tem 1.000.
- Apagar os 14 públicos INACTIVE, os 6 de 2024 incluídos.
- Unificar `location_types`: o RMK usa `["home","recent"]`, a prospecção usa
  `["frequently_in","home","recent"]`. Duas definições diferentes de "estar em
  São Caetano" no mesmo funil.
- Remover as 12 exclusões de estado (Bahia, Ceará, Paraná…) dos conjuntos que
  já miram um raio de 4 km. É inofensivo, mas é sinal de configuração copiada —
  e esconde o que de fato está sendo excluído.

## 5. Criativo: 17 anúncios, 2 textos

Na primeira página de criativos da conta, 17 dos 20 têm **o mesmo texto
principal** ("Pegou as chaves do seu novo imóvel?…") e 3 têm o outro
("ABC e região!!…"). Todo o "teste de criativo" é troca de vídeo sobre a mesma
mensagem — e os lotes de 13/08 e 10/09 são duplicatas um do outro.

Abrindo os criativos (`2129971087922079`, `2888188731539247`,
`28608446992177358`):

| Campo | Valor atual | Problema |
|---|---|---|
| `object_type` | `VIDEO` | ok |
| `title` (título) | **`""`** | slot vazio nos três |
| `call_to_action_type` | **`SIGN_UP`** ("Cadastre-se") | o texto promete "Agende sua visita ao showroom" |
| `body` | ver abaixo | repetição interna |

O corpo de um deles, na íntegra:

> ABC e região!!
> Móveis planejados ÉFGE. Projeto autoral, acabamento premium, instalação impecável.
> **Sua casa merece começar no nível mais alto.**
> **Agende sua visita ao showroom.**
> ÉFGE Móveis Planejados em São Caetano.
> **Chaves na mão? Comece do nível mais alto.**

"Começar no nível mais alto" aparece duas vezes no mesmo texto, "São Caetano"
duas vezes, e o convite para agendar aparece antes da razão para agendar. Não há
oferta, âncora de preço, prazo, prova (nº de projetos entregues, tempo de casa)
nem diferencial além de adjetivos.

**Microajustes:**
- Preencher o `title` dos anúncios de formulário. Hoje são três slots em branco.
- Trocar o CTA de `SIGN_UP` para `BOOK_NOW` ("Agende agora") ou `REQUEST_TIME` —
  alinhado ao que o próprio texto pede. Botão e promessa hoje discordam.
- Cortar a repetição: um único fechamento, não dois.
- Testar **texto**, não só vídeo: 3 ângulos distintos (preço/parcelamento,
  prazo de entrega, prova social do showroom) sobre o mesmo vídeo vencedor.
  Hoje não existe teste de mensagem na conta.
- Consolidar em 4 anúncios por conjunto. Desligar os 6 que receberam menos de
  R$ 20 em 30 dias — eles rodam a CPM de R$ 67 a R$ 92 contra R$ 29–34 dos que
  entregam, porque nunca saíram do aprendizado.
- Manter `AP FB INFLUENCER 02` como criativo-base: é o único "Acima da média" em
  qualidade com volume (46 leads), e na prospecção fez lead a R$ 8,76.
- Aceitar o `mixed_formats` que a Meta sinaliza na campanha de reconhecimento
  (`120255015839610226`): hoje ela roda um formato só.
- Revisar o filtro de conteúdo: os três conjuntos estão em
  `FACEBOOK_RELAXED` / `AN_RELAXED` / `FEED_RELAXED`. Para marca de alto padrão,
  moderado é a escolha usual.

## 6. Ordem de execução

Do mais barato e reversível para o mais estrutural:

| # | Ajuste | Onde | Ganho estimado |
|---|---|---|---|
| 1 | Pausar as 16 campanhas com agenda vencida | conta | legibilidade, risco |
| 2 | Desligar os 6 anúncios com < R$ 20/30d | ambos os conjuntos | CPM médio |
| 3 | Fechar idade em 27–54 **com** `advantage_audience: 0` | ambos | ~R$ 300/mês |
| 4 | Cortar Feed no RMK e Reels na prospecção | por conjunto | ~R$ 250/mês |
| 5 | Excluir leads existentes e cruzar exclusão entre conjuntos | ambos | frequência, sobreposição |
| 6 | Título + CTA `BOOK_NOW` nos criativos | criativos | CTR |
| 7 | Soltar interesses no RMK e ampliar raio | RMK | CPM, fadiga |
| 8 | Rebalancear verba para a prospecção | campanha | CPL |
| 9 | `em`/`ph`/`lead_id` + envio diário + conversão personalizada | dados | CPL qualificado (−24% est. Meta) |
| 10 | Limpar públicos e datasets mortos | conta | diagnóstico |

Os itens 1 a 6 são reversíveis em um clique e não mexem em aprendizado de
campanha. Os itens 7 e 8 reiniciam aprendizado — fazer um por vez, com 4 a 7
dias entre eles, para saber qual mexeu o ponteiro. O item 9 é o único que
depende de quem mantém a integração do CRM.
