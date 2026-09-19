# CAMINHO — publicar os anúncios pelo Supermetrics

Medido em 11/09/2026, consultando a documentação e as ferramentas do próprio
Supermetrics. Este arquivo existe para que, no minuto em que a conexão existir,
a publicação seja **uma chamada só** — sem redescobrir nada.

## Por que este caminho

O app "OPC Automação" está em **Development mode**. Todo criativo de formulário
instantâneo criado por um token desse app volta `1885183`. Isso não é permissão
nem código: é o modo do app. Os quatro caminhos testados até aqui:

| Caminho | Formulário? | `pages_manage_ads`? | App Live? | Resultado medido |
|---|---|---|---|---|
| Conector Facebook MCP | ✗ | ✗ | ✓ | `1892181` |
| Token de usuário do sistema, Graph direto | ✓ | ✓ | ✗ | `1885183` |
| Composio `metaads` (mesma credencial) | ✓ | ✓ | ✗ | `1885183` |
| **Supermetrics `manage_campaign`** | ✓ | — | ✓ **app próprio, Live** | falta só a conta conectada |

O Supermetrics é o único que resolve o `1885183` sem o Pablo mexer no painel de
desenvolvedor: os anúncios saem pelo **app do Supermetrics**, que é Live e já
passou pela revisão da Meta. Ele suporta `lead_gen_form_id` no criativo, que é
exatamente o campo que o conector do claude.ai não tem.

## O que falta (um clique, uma vez)

`accounts_discovery(ds_id="FA")` lista 49 contas do time
"Team sampaioopablo1" (ID 1140774) e **a conta `1695865631502778` não está
entre elas** — confirmado também filtrando pelo id e por "pr".

A conexão FA existe e está autenticada (via "Pablo Sampaio", id
997185549809464), só não alcança essa conta. Conserto:

1. Abrir <https://hub.supermetrics.com/token-management?team_id=1140774#dataSourceFA>
   (ou pedir um link de login novo — `manage_user_and_team`, ação
   `login_data_source`, `ds_id: FA`; vale 24 h, por isso **não fica escrito
   aqui**).
2. Relogar a origem Facebook Ads com o perfil que enxerga a conta
   "O Próximo Cliente" (`1695865631502778`).
3. Marcar essa conta na lista de contas liberadas.

Depois disso `accounts_discovery(ds_id="FA", filter="1695865631502778")`
devolve a conta, e a publicação roda.

## A chamada de publicação

`manage_campaign`, **sem nenhum campo de orçamento** (trava 1 da REGRA — corte
de anúncio em 48 horas: dinheiro é decisão do Pablo):

```
ds_id: "FA"
account_id: "1695865631502778"
campaign_id: <campanha da FASE 3>
ad_groups:
  - id: "120247356527930766"        # AG01..AG05
    ads: [ {name, creative, platform_settings}, ... ]
  - id: "120247356496360766"        # AG06..AG10
    ads: [ ... ]
```

Cada anúncio:

```
name: <slug do spec>
status: "PAUSED"                     # o Pablo ativa; ele pediu assim
creative:
  headlines:    [<headline>]
  descriptions: [<message>]
  call_to_action: "SIGN_UP"
  lead_gen_form_id: "2412763482587375"
  asset_url: <hotlink do Drive, do spec>
platform_settings:
  page_id: "1117439194786453"
```

Fonte dos valores: `entregas/campanha/ANUNCIOS — spec dos conjuntos.json`. É o
mesmo spec que `fabrica/anuncios_meta.py` usa no caminho Graph direto — os dois
caminhos leem a mesma verdade, então trocar de caminho não reescreve as peças.

`asset_url` aceita URL pública e o Supermetrics baixa e sobe para a conta. Os
hotlinks `lh3.googleusercontent.com/d/<id>` do spec servem; `drive.google.com/uc`
não serve (devolve HTML).

## A outra porta, se esta demorar

`developers.facebook.com/apps/2159128187972575/settings/basic/` → App Mode:
Development → **Live**. Aí o `fabrica/anuncios_meta.py` publica sozinho a cada
push no spec, sem depender de app externo nenhum. As duas portas dão no mesmo
lugar; a diferença é quem é o dono do app que assina o criativo.
