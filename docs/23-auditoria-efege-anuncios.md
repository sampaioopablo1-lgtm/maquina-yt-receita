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
