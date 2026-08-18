-- 18/08/2026 — Fila da fábrica de profundidade (parallax 2.5D das visitas).
--
-- A visita virtual v2 procura, para cada foto real, um mapa de profundidade
-- em visitas/depths/<djb2(url)>.jpg. Quem produz os mapas é a fábrica horária
-- (.github/workflows/fabrica-visita.yml), que roda MiDaS (Intel, open-source)
-- em CPU no runner: ~1s por foto, custo zero. Esta tabela é o controle do que
-- já foi feito; a ordem de produção prioriza imóvel de maior valor — o tour
-- mais rico aparece primeiro onde o lead vale mais.
--
-- Piloto validado antes disto: 30 mapas do imóvel 40346 gerados e no ar,
-- 364KB no total. Escala: 94 mil fotos ≈ 26h de CPU, distribuídas nas
-- rodadas horárias (~5 dias); depois, só foto nova do sync.

create table if not exists public.feed_visita_depth (
  url text primary key,
  codigo_vista text,
  hash text not null,
  criado_em timestamptz not null default now()
);

create index if not exists feed_visita_depth_codigo on public.feed_visita_depth (codigo_vista);

alter table public.feed_visita_depth enable row level security;
-- Sem policy: só service_role.

-- Próximo lote de fotos sem mapa, do imóvel mais caro para o mais barato.
create or replace function public.fn_fotos_sem_depth(p_n int default 800)
returns table (codigo text, url text)
language sql
security definer
set search_path = public
as $$
  select fp.codigo_original, u
  from public.feed_properties fp
  left join public.feed_property_portal_publicacao p
         on p.property_id = fp.id and p.portal = 'vrsync_rede'
  left join public.vista_imoveis_log v on v.codigo_vista = fp.codigo_original,
  lateral jsonb_array_elements_text(coalesce(fp.dados_normalizados->'fotos','[]'::jsonb)) u
  where fp.ativo and coalesce(p.habilitado, true)
    and not exists (select 1 from public.feed_visita_depth d where d.url = u)
  order by coalesce(v.valor_venda, v.valor_locacao) desc nulls last
  limit greatest(1, p_n);
$$;

revoke all on function public.fn_fotos_sem_depth(int) from public, anon, authenticated;

-- Registro do piloto 40346 (mapas já no ar), para a fábrica não refazer.
insert into public.feed_visita_depth (url, codigo_vista, hash)
select u, '40346', ''
from public.feed_properties fp,
lateral jsonb_array_elements_text(fp.dados_normalizados->'fotos') u
where fp.codigo_original = '40346'
on conflict (url) do nothing;
