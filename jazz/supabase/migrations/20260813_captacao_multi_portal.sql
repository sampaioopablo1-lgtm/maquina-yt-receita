-- 13/08/2026 — Pesquisa de captação passa a cobrir vários portais, em vez de
-- só Zap. Pedido do usuário: "Precisa ser pesquisa assíncrona, em todos os
-- portais, para encontrar sugestão de imóvel para ser captado."
--
-- Levantamento feito antes de mexer em código (chamadas de teste via
-- net.http_post, 1 crédito cada, corpo salvo em net._http_response):
--
--   zapimoveis.com.br   — PLP traz advertiser.phoneNumbers/license direto.
--   vivareal.com.br     — mesmo parser da Grupo Zap (glue-api), mesmo shape.
--   chavesnamao.com.br  — PLP traz advertiser.phones.{cellphone,landline} e,
--                          melhor que os outros dois, advertiser.type
--                          ("PJ"/"PF") — sinal direto de pessoa física, sem
--                          precisar do regex de nome que os outros exigem.
--   olx.com.br           — FICOU DE FORA. O item de listagem (PLP) não traz
--                          telefone nem anunciante, só "professionalAd":
--                          bool. Telefone só sai na página do anúncio (PDP),
--                          que cobra 1 crédito por imóvel — na prática 30x
--                          mais caro que 1 crédito por 30 imóveis do PLP.
--                          Decisão: não vale o custo para o volume que se
--                          busca aqui. Documentado, não esquecido.
--
-- businessType tem que ir em minúsculo ("sale"/"rent") — "RENTAL" (o que a
-- varredura antiga gravava) é rejeitado pela validação da GeckoAPI com 400.
-- "SALE" maiúsculo passava por coincidência (a API compara case-insensitive
-- só quando o valor bate com "sale"), mas "rent" exige minúsculo exato.

alter table public.captacao_varredura
  add column if not exists target text not null default 'zapimoveis.com.br';

alter table public.captacao_varredura drop constraint if exists captacao_varredura_cidade_uf_business_type_key;
alter table public.captacao_varredura
  add constraint captacao_varredura_cidade_uf_business_type_target_key
  unique (cidade, uf, business_type, target);

-- Cada cidade/operação ativa em Zap passa a ter irmã em VivaReal e Chaves na
-- Mão, largando do zero (página 1). Zap continua a fonte com mais páginas
-- lidas — as novas começam atrás de propósito, ninguém perde histórico.
insert into public.captacao_varredura (cidade, uf, business_type, target, ativa, proxima_pagina, paginas_lidas)
select cidade, uf, business_type, 'vivareal.com.br', true, 1, 0
from public.captacao_varredura
where target = 'zapimoveis.com.br' and ativa
on conflict (cidade, uf, business_type, target) do nothing;

insert into public.captacao_varredura (cidade, uf, business_type, target, ativa, proxima_pagina, paginas_lidas)
select cidade, uf, business_type, 'chavesnamao.com.br', true, 1, 0
from public.captacao_varredura
where target = 'zapimoveis.com.br' and ativa
on conflict (cidade, uf, business_type, target) do nothing;

-- Estoque de prospects agora conta por portal também, pra enxergar se um
-- portal parou de responder sem esconder atrás do total. Mantém intactos
-- todos os campos que já existiam (a fila de captação e o edge function
-- dependem deles) e só soma a quebra por fonte.
create or replace function public.fn_captacao_estoque()
returns jsonb
language sql
stable
security definer
set search_path = public
as $$
  select jsonb_build_object(
    'disponiveis', count(*) filter (where status='novo' and sugerido_em is null
                                      and telefone is not null and perfil in ('particular','indefinido')),
    'particulares', count(*) filter (where status='novo' and sugerido_em is null and perfil='particular'),
    'indefinidos', count(*) filter (where status='novo' and sugerido_em is null and perfil='indefinido'),
    'empresas_filtradas', count(*) filter (where perfil='empresa'),
    'descartados', count(*) filter (where perfil='descartar'),
    'ja_sugeridos', count(*) filter (where sugerido_em is not null),
    'total_coletado', count(*),
    'por_portal', (select coalesce(jsonb_object_agg(fonte, n), '{}'::jsonb)
                   from (select fonte, count(*) n from public.captacao_prospects
                         group by fonte) t)
  ) from public.captacao_prospects;
$$;
