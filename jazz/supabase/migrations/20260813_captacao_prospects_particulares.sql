-- 13/08/2026 — captação de proprietários: reposição da plancap via GeckoAPI.
--
-- A planilha de sugestões esgota e cada rodada precisa de imóveis novos, com
-- telefone, e de particulares — não de imobiliárias.
--
-- SEPARAR PARTICULAR DE EMPRESA
--
-- O Zap devolve, por anúncio, um bloco `advertiser` com nome, telefone,
-- WhatsApp e `license` (o CRECI). A primeira versão usou license vazia como
-- sinal de particular: numa página de 30 anúncios, 13 sem CRECI e todos com
-- telefone — 43%, parecia ótimo.
--
-- A auditoria da primeira lista derrubou isso. Entre os "sem CRECI" saíram
-- `Re/Max Rede Nardo`, `J R J RIZZI - IMOVEIS`, `Kasa Construtora`, `Newcore` e
-- `Bom Negocio Atividades De Internet Ltda` — este com telefone 1122222222,
-- que é preenchimento genérico. Mandar isso pro captador queima a lista dele.
--
-- Passaram a valer três sinais combinados:
--   1. CRECI preenchido → empresa ou corretor;
--   2. nome com marca de empresa → empresa, mesmo sem CRECI. As classes de
--      acento cobrem grafia livre: IMOVÉIS, IMÓVEIS e IMOVEIS apareceram todas
--      em anúncios reais, e a primeira régua deixou passar "CHRIS MARIA
--      DECOLAR IMOVÉIS" por não cobrir o É;
--   3. telefone de dígito repetido → descarta, não é contato real.
-- Sobra `particular` para nome de duas ou mais palavras sem termo corporativo,
-- e `indefinido` para nome de uma palavra só, que não dá pra afirmar nem negar.
--
-- Com a régua completa o rendimento real caiu para ~6%: em 192 anúncios
-- coletados, 156 empresas, 16 telefones genéricos, 10 ambíguos e 10
-- particulares. É bem menos que os 43% da régua ingênua — e é o número certo.
--
-- Continua sendo indício, não certeza: proprietário pode anunciar como "Casa
-- do João" e corretor autônomo pode usar o nome próprio. Por isso o nome do
-- anunciante e o motivo da classificação vão junto na sugestão — quem liga
-- decide com o dado à vista.
--
-- ECONOMIA DE CRÉDITOS
--
-- Custo medido: 1 crédito por página de 30 anúncios; erro de validação não
-- cobra. Quatro mecanismos seguram o consumo:
--   1. se o estoque de particulares cobre o alvo, não chama a API;
--   2. cursor por cidade nunca relê página já varrida;
--   3. classifica a cada página e para assim que atinge o alvo;
--   4. dedupe por telefone — mesmo dono com três anúncios é uma ligação.
-- Uma rodada de 10 sugestões custa ~6 créditos com cache vazio, e zero com
-- estoque. Os 10.000 créditos dão para mais de mil rodadas.

create table if not exists public.captacao_prospects (
  id bigserial primary key,
  fonte text not null default 'zapimoveis.com.br',
  anuncio_id text,
  url text,
  titulo text,
  tipo text,
  cidade text,
  bairro text,
  endereco text,
  preco numeric,
  area numeric,
  quartos int,
  vagas int,
  anunciante text,
  telefone text,
  whatsapp text,
  tem_creci boolean not null default false,
  creci text,
  perfil text,
  motivo_perfil text,
  dados jsonb,
  coletado_em timestamptz not null default now(),
  sugerido_em timestamptz,
  status text not null default 'novo'
);

-- Índice único SEM predicado: ON CONFLICT não casa com índice parcial, e a
-- primeira versão perdeu 3 créditos gravando zero por causa disso.
create unique index if not exists uq_captacao_prospects_anuncio
  on public.captacao_prospects (fonte, anuncio_id);
create index if not exists idx_captacao_prospects_fila
  on public.captacao_prospects (perfil, sugerido_em, coletado_em) where status = 'novo';
create index if not exists idx_captacao_prospects_telefone
  on public.captacao_prospects (telefone) where telefone is not null;

create table if not exists public.captacao_varredura (
  id bigserial primary key,
  cidade text not null,
  uf text not null default 'SP',
  business_type text not null default 'SALE',
  proxima_pagina int not null default 1,
  paginas_lidas int not null default 0,
  total_resultados int,
  ultima_coleta timestamptz,
  ativa boolean not null default true,
  unique (cidade, uf, business_type)
);

insert into public.captacao_varredura (cidade, uf, business_type)
select distinct fp.dados_normalizados->>'cidade', 'SP', 'SALE'
from public.feed_properties fp
where fp.ativo and coalesce(fp.dados_normalizados->>'cidade','') <> ''
on conflict (cidade, uf, business_type) do nothing;

create or replace function public.fn_captacao_classificar()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v jsonb;
  re_empresa text := '(?i)(ltda|s/?a\.?$|eireli|\bme\b|\bmei\b|\bepp\b|im[oó]v[eé]|imobili|corretor|corretag|'
                  || 'consultor|assessor|administrador|construtor|construç|incorporad|empreendim|urbanism|'
                  || 'loteador|realty|broker|invest|neg[oó]cio|patrim|holding|participa|\bspe\b|'
                  || 're/?max|century|coelho da fonseca|\blopes\b|bossa|keller|engel|'
                  || 'imobili[aá]ria|\bgrupo\b|\bcia\b|& cia|assoc|servi[çc]os|solu[çc][oõ]es|'
                  || 'engenharia|arquitet|\bhome\b|\bhomes\b|\bhouse\b|\bprime\b|\belite\b|\bvip\b|'
                  || '\bmaster\b|\bplan\b|\bplanej\b|\bventures?\b|\bcorp\b|\bgroup\b)';
  re_fone_falso text := '^\d{2}(\d)\1{7,}$';
begin
  update public.captacao_prospects p set
    perfil = case
      when p.telefone is null or p.telefone ~ re_fone_falso then 'descartar'
      when p.tem_creci then 'empresa'
      when coalesce(p.anunciante,'') ~ re_empresa then 'empresa'
      when array_length(regexp_split_to_array(btrim(coalesce(p.anunciante,'')), '\s+'), 1) >= 2 then 'particular'
      else 'indefinido'
    end,
    motivo_perfil = case
      when p.telefone is null or p.telefone ~ re_fone_falso then 'telefone ausente ou genérico'
      when p.tem_creci then 'CRECI informado no anúncio'
      when coalesce(p.anunciante,'') ~ re_empresa then 'nome com marca de empresa'
      when array_length(regexp_split_to_array(btrim(coalesce(p.anunciante,'')), '\s+'), 1) >= 2 then 'nome de pessoa, sem CRECI'
      else 'nome de uma palavra — não dá pra afirmar'
    end;

  select jsonb_build_object(
    'particular', count(*) filter (where perfil='particular'),
    'empresa', count(*) filter (where perfil='empresa'),
    'indefinido', count(*) filter (where perfil='indefinido'),
    'descartar', count(*) filter (where perfil='descartar')) into v
  from public.captacao_prospects;
  return v;
end;
$$;

drop function if exists public.fn_captacao_sugerir(int, text);
create function public.fn_captacao_sugerir(p_n int default 10, p_cidade text default null)
returns table(
  r_anuncio_id text, r_url text, r_titulo text, r_tipo text, r_cidade text, r_bairro text,
  r_preco numeric, r_area numeric, r_quartos int, r_anunciante text, r_telefone text,
  r_whatsapp text, r_perfil text, r_observacao text)
language plpgsql
security definer
set search_path = public
as $$
begin
  return query
  with candidatos as (
    select distinct on (p.telefone) p.id, p.telefone, p.perfil, p.coletado_em
    from public.captacao_prospects p
    where p.status = 'novo' and p.sugerido_em is null
      and p.telefone is not null
      and p.perfil in ('particular','indefinido')
      and (p_cidade is null or p.cidade ilike p_cidade)
    order by p.telefone, (p.perfil = 'particular') desc, p.coletado_em desc
  ), escolhidos as (
    select c.id from candidatos c
    order by (c.perfil = 'particular') desc, c.coletado_em desc
    limit greatest(1, p_n)
  ), marcados as (
    update public.captacao_prospects p set sugerido_em = now(), status = 'sugerido'
     where p.id in (select id from escolhidos) returning p.*
  )
  select m.anuncio_id, m.url, m.titulo, m.tipo, m.cidade, m.bairro, m.preco, m.area,
         m.quartos, m.anunciante, m.telefone, m.whatsapp, m.perfil, m.motivo_perfil
  from marcados m order by (m.perfil = 'particular') desc, m.coletado_em desc;
end;
$$;

create or replace function public.fn_captacao_estoque()
returns jsonb
language sql
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
    'total_coletado', count(*)
  ) from public.captacao_prospects;
$$;

revoke all on function public.fn_captacao_classificar() from public, anon;
revoke all on function public.fn_captacao_sugerir(int, text) from public, anon;
revoke all on function public.fn_captacao_estoque() from public, anon;

-- Reposição três vezes ao dia; classificação de hora em hora.
select cron.schedule('captacao-repor-prospects', '26 7,13,19 * * *', $cron$
  select net.http_post(
    url := 'https://cscczluzpblzhvojxanp.supabase.co/functions/v1/captacao-prospectar',
    headers := jsonb_build_object(
      'apikey','sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
      'Authorization','Bearer sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
      'Content-Type','application/json'),
    body := '{"alvo":30,"maxPaginas":8}'::jsonb,
    timeout_milliseconds := 240000)
$cron$);

select cron.schedule('captacao-classificar', '56 * * * *',
                     $cron$select public.fn_captacao_classificar();$cron$);
