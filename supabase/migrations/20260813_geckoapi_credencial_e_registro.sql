-- 13/08/2026 — GeckoAPI: a chave que faltava, e o que ela realmente é.
--
-- A chave `pk_live_...` circulou em sessões anteriores como sendo do Genspark.
-- Não é: é da GeckoAPI (geckoapi.com.br), uma API brasileira de extração de
-- dados de sites. Isso encerra a investigação que não fechava — o Genspark não
-- tem API pública, e por isso nada batia.
--
-- Validado em 13/08 contra a API real:
--   * base            https://api.geckoapi.com.br   (não geckoapi.com.br)
--   * autenticação    header `X-API-Key` (ou Bearer)
--   * saldo           GET /v1/me/credits → 10.100 créditos, plano developer,
--                     zero consumo em 30 dias (a chave nunca havia sido usada)
--   * extração        POST /v1/extract com {target, type, ...}
--                     `target` = domínio, `type` = pdp|plp|review|quote|search
--
-- Fontes imobiliárias suportadas: zapimoveis.com.br, vivareal.com.br,
-- olx.com.br, chavesnamao.com.br, portalzuk.com.br (leilões) — além de
-- casadosdados.com.br para CNPJ e google.com para busca e places.
--
-- Teste real (Campinas/SP, venda): 136.978 resultados, 30 por página, e cada
-- anúncio traz `advertiser` com nome, CRECI, telefone, WhatsApp e verificação.
-- É o dado que o módulo de captação precisava e que estava parado por falta da
-- FIRECRAWL_API_KEY.
--
-- O que NÃO dá: filtrar por anunciante. Testei `keyword: "Jazz Imobiliaria"` e
-- a busca procura no texto do anúncio, não no nome da imobiliária — voltaram
-- 6.528 resultados, nenhum nosso. Auditar nossa própria presença por essa via
-- exigiria varrer 4.566 páginas só de Campinas. O painel do Zap já dá esse
-- número de graça.
--
-- A credencial fica em tabela com RLS ligado e sem policy: nenhum papel do
-- PostgREST lê, só service_role (que ignora RLS) dentro de Edge Function.
-- Não vai para variável de ambiente nem para o repositório.

create table if not exists public.integracao_credenciais (
  chave text primary key,
  valor text not null,
  descricao text,
  atualizado_em timestamptz not null default now()
);

alter table public.integracao_credenciais enable row level security;

revoke all on public.integracao_credenciais from anon, authenticated;

-- O valor real é inserido fora do controle de versão:
--   insert into public.integracao_credenciais (chave, valor, descricao)
--   values ('geckoapi_api_key', '<a chave>', 'GeckoAPI — extração de portais.')
--   on conflict (chave) do update set valor = excluded.valor, atualizado_em = now();
