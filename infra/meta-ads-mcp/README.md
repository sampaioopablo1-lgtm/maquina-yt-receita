# Servidor MCP da Meta Ads — O Próximo Cliente

Edge Function do Supabase que expõe a Meta Marketing API como servidor MCP. Existe porque
**nenhum caminho pronto funcionou**: o conector Meta Ads não pede `pages_manage_ads` e por isso
não cria anúncio de lead; o Composio bloqueia toda escrita por política de marketplace; e o
ambiente da sessão bloqueia `graph.facebook.com` na camada de rede (403 no CONNECT).

Este servidor roda na conta do Pablo, fala com a Meta a partir de lá, e é adicionado ao Claude
como conector — que é o uso previsto do protocolo, não um contorno.

## Onde está

| Item | Valor |
|---|---|
| Projeto Supabase | `vevocauwtarctfwngrch` (maquina-yt-dark) |
| Função | `meta-ads` |
| URL base | `https://vevocauwtarctfwngrch.supabase.co/functions/v1/meta-ads` |
| URL do conector | a URL base **mais uma barra e o `MCP_SHARED_SECRET`** |

## Segredos (Edge Function Secrets do projeto)

| Nome | O que é |
|---|---|
| `META_ACCESS_TOKEN` | token do usuário do sistema "Integracao", com `ads_management`, `ads_read`, `business_management`, `pages_manage_ads`, `pages_read_engagement` e `pages_show_list` |
| `META_AD_ACCOUNT_ID` | `1695865631502778` (sem o prefixo `act_`) |
| `META_PAGE_ID` | `1117439194786453` |
| `MCP_SHARED_SECRET` | senha longa; entra no caminho da URL |
| `META_MAX_DAILY_BUDGET_CENTS` | teto de orçamento em centavos. `5000` = R$50/dia |

O token **nunca** trafega pelo chat nem aparece em resposta ou log — ele vive só no Supabase.

## Decisões de segurança

**Nasce pausado.** `meta_criar_conjunto` e `meta_criar_anuncio` forçam `status: PAUSED`. Nada
começa a gastar sem alguém ligar.

**Teto de orçamento.** Qualquer operação que tente definir `daily_budget` ou `lifetime_budget`
acima de `META_MAX_DAILY_BUDGET_CENTS` é recusada antes de chegar à Meta — tanto na criação
quanto na edição.

**O segredo está no caminho, não em cabeçalho.** Conector remoto nem sempre permite configurar
cabeçalho. Sem o segredo correto, a função responde 404 para qualquer requisição, inclusive de
quem descubra a URL base.

**Escopo preso à conta.** Leituras e escritas montam o caminho a partir de `META_AD_ACCOUNT_ID`.
Não há como apontar para outra conta de anúncios sem trocar o segredo do projeto.

## Ferramentas

| Nome | O que faz |
|---|---|
| `meta_contexto` | conta, página, teto e se o token responde |
| `meta_ler` | campanhas, conjuntos, anúncios, criativos, públicos, imagens, vídeos |
| `meta_insights` | métricas com quebras por posicionamento, idade, gênero, dispositivo |
| `meta_criar_conjunto` | conjunto novo, com públicos, geo com exclusões e criativo dinâmico |
| `meta_criar_criativo` | criativo próprio ou publicação promovida; aceita `asset_feed_spec` |
| `meta_criar_anuncio` | anúncio dentro de um conjunto |
| `meta_editar` | renomear, pausar, ativar, orçamento, segmentação |

## Manutenção

O token do usuário do sistema **expira em 60 dias**. Quando expirar, gere outro pelo mesmo
caminho (Configurações do Business → Usuários do sistema → Integracao → Gerar token) e troque o
valor de `META_ACCESS_TOKEN` nos segredos. Nada mais precisa mudar.

Para republicar depois de editar `index.ts`, use `deploy_edge_function` no projeto
`vevocauwtarctfwngrch`, com o nome `meta-ads` e `verify_jwt: false`.
