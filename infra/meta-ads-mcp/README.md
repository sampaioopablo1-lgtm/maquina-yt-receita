# Servidor MCP da Meta Ads — O Próximo Cliente

## Estado em 09/09/2026

**O caminho pelo Supabase está morto até a cota voltar.** A organização inteira do Supabase responde
`HTTP 402 — exceed_egress_quota, exceed_storage_size_quota` no gateway, antes de qualquer função rodar.
Foi por isso que as quatro tentativas de conectar o conector no claude.ai falharam — não foi protocolo.
Volta quando o mês virar, quando o plano subir, ou quando o bucket `videos-maquina` (622 MB) for esvaziado.

**O caminho oficial existe e não depende do Supabase.** A Meta hospeda um servidor MCP em
`https://mcp.facebook.com/ads`, aberto a qualquer app próprio desde 16/07/2026. É ele que o
conector "Facebook MCP" do claude.ai já usa — só que com o app da Meta. Com o app do Pablo
(OPC Automação, id `2159128187972575`) entra-se pelo mesmo servidor.

## Duas formas de entrar no servidor oficial

| Forma | Como | O que carrega |
|---|---|---|
| OAuth (conector personalizado no claude.ai) | URL `https://mcp.facebook.com/ads`, client_id = id do app; redirecionamento `https://claude.ai/api/mcp/auth_callback` no Login do Facebook para Empresas | escopos fixos: `ads_management ads_read catalog_management business_management pages_show_list instagram_basic ads_mcp_management` |
| Token de usuário do sistema | `Authorization: Bearer <token>` na requisição | tudo que o token tiver — inclusive `pages_manage_ads`, que o anúncio de lead exige |

O claude.ai não deixa configurar cabeçalho fixo. Por isso a segunda forma precisa de um relé:
`index.ts` (v9) é esse relé — recebe do claude.ai, injeta o token do segredo, repassa ao servidor da
Meta, e recusa orçamento acima do teto. Roda em qualquer host que sirva uma função HTTP; hoje está
escrito para o Supabase (`meta-ads`, projeto `vevocauwtarctfwngrch`, `verify_jwt: false`).

## Segredos do relé

| Nome | O que é |
|---|---|
| `META_ACCESS_TOKEN` | token do usuário do sistema "Integracao", com `ads_management`, `ads_read`, `business_management`, `pages_manage_ads`, `pages_read_engagement`, `pages_show_list` |
| `MCP_SHARED_SECRET` | senha longa; entra no caminho da URL |
| `META_MAX_DAILY_BUDGET_CENTS` | teto de orçamento em centavos. `5000` = R$50/dia |

O token **nunca** trafega pelo chat nem aparece em resposta ou log.

## Regras de segurança

- **Nasce pausado.** O servidor da Meta cria campanha, conjunto e anúncio pausados; ativar é uma chamada separada.
- **Teto de orçamento.** O relé recusa `daily_budget`/`lifetime_budget` acima de `META_MAX_DAILY_BUDGET_CENTS`.
- **Regras do Business.** Configurações do Business Suite → Integrações → *Servidor MCP de anúncios* permite bloquear criação de campanha e edição de orçamento por conta. O servidor da Meta aplica.
- **Segredo no caminho.** Sem ele, o relé responde 404.

## Manutenção

O token do usuário do sistema expira em 60 dias. Gere outro em Configurações do Business →
Usuários do sistema → Integracao → Gerar token, e troque `META_ACCESS_TOKEN`.

## Fontes

- Blog da Meta, 16/07/2026: https://developers.facebook.com/blog/post/2026/07/16/meta-ads-mcp-server/
- Documentação: https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started
- Central de Ajuda (regras e conectores): https://www.facebook.com/business/help/1456422242197840
- Metadados vivos: `https://mcp.facebook.com/.well-known/oauth-protected-resource/ads` e `https://mcp.facebook.com/.well-known/oauth-authorization-server/ads`
