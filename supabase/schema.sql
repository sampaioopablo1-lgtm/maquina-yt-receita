-- Estado da maquina no Supabase.
-- O runner do GitHub Actions e efemero: e aqui que o historico sobrevive.
-- Aplique via: Supabase Dashboard > SQL Editor, ou `supabase db push`.

create table if not exists videos (
    slug          text primary key,
    status        text not null,
    formato       text not null check (formato in ('shorts', 'longo')),
    titulo        text,
    youtube_id    text unique,
    roteiro       jsonb,
    duracao_s     numeric,
    custo_usd     numeric default 0,
    erro          text,
    criado_em     timestamptz not null default now(),
    publicado_em  timestamptz,
    agendado_para timestamptz
);

create index if not exists idx_videos_status on videos (status);
create index if not exists idx_videos_publicado on videos (publicado_em desc);

-- Snapshots de performance. Serie temporal: um video gera varias linhas.
create table if not exists metricas (
    id                     bigserial primary key,
    youtube_id             text not null references videos (youtube_id) on delete cascade,
    coletado_em            timestamptz not null default now(),
    impressoes             integer default 0,
    views                  integer default 0,
    ctr                    numeric default 0,
    retencao_media_pct     numeric default 0,
    duracao_media_s        numeric default 0,
    inscritos_ganhos       integer default 0,
    receita_estimada_usd   numeric default 0,
    unique (youtube_id, coletado_em)
);

create index if not exists idx_metricas_video on metricas (youtube_id, coletado_em desc);

-- Ultima leitura de cada video, com o gargalo ja classificado.
-- E a consulta que responde "o que eu conserto primeiro".
-- security_invoker: sem isso a view roda com o privilegio de quem criou (dono),
-- ignorando as policies de RLS abaixo e vazando os dados para anon/authenticated
-- via PostgREST — o oposto do "acesso apenas via service_role" declarado ali.
create or replace view painel_pilares
    with (security_invoker = true) as
select distinct on (m.youtube_id)
    v.slug,
    v.titulo,
    v.formato,
    m.youtube_id,
    m.impressoes,
    m.views,
    m.ctr,
    m.retencao_media_pct,
    m.receita_estimada_usd,
    case
        when m.impressoes < 500                          then 'sem_dados'
        when m.ctr >= 0.05 and m.retencao_media_pct >= 30 then 'nenhum'
        when m.ctr >= 0.05                                then 'roteiro'
        when m.retencao_media_pct >= 30                   then 'thumbnail'
        else 'titulo'
    end as gargalo,
    m.coletado_em
from metricas m
join videos v on v.youtube_id = m.youtube_id
order by m.youtube_id, m.coletado_em desc;

-- Progresso rumo aos requisitos do YPP (1.000 inscritos + 4.000h em 12 meses).
create or replace view progresso_ypp
    with (security_invoker = true) as
select
    sum(inscritos_ganhos)                              as inscritos_ganhos_periodo,
    round(sum(views * duracao_media_s) / 3600.0, 1)    as horas_estimadas,
    round(sum(receita_estimada_usd), 2)                as receita_estimada_usd
from (
    select distinct on (youtube_id) *
    from metricas
    where coletado_em > now() - interval '365 days'
    order by youtube_id, coletado_em desc
) ultimas;

alter table videos   enable row level security;
alter table metricas enable row level security;

-- Acesso apenas via service_role (o job do Actions). Sem cliente publico.
-- Postgres nao aceita `create policy if not exists`; o drop antes mantem o
-- arquivo reaplicavel sem erro.
drop policy if exists "service_role_videos" on videos;
create policy "service_role_videos"
    on videos for all to service_role using (true) with check (true);

drop policy if exists "service_role_metricas" on metricas;
create policy "service_role_metricas"
    on metricas for all to service_role using (true) with check (true);

-- ============================================================
-- As quatro consultas de abertura (PLAYBOOK.md secao 0).
--
-- As tabelas base (canais, aprendizados, pautas_banco) foram criadas direto em
-- producao por sessoes anteriores e NAO estao neste arquivo — reaplicar este
-- schema.sql do zero NAO recria essas views porque as tabelas nao existem
-- aqui. Documentado como gap conhecido em `aprendizados` (categoria processo,
-- 2026-08-05); as definicoes abaixo servem para manter as views versionadas,
-- nao para reconstruir o banco do zero.
--
-- Todas com security_invoker=true: sem isso a view roda com o privilegio de
-- quem criou (SECURITY DEFINER, por omissao) e ignora a RLS das tabelas base,
-- vazando os dados para anon/authenticated via PostgREST — achado como ERROR
-- pelo Supabase Advisor em 2026-08-05 e corrigido nesta mesma sessao.
-- ============================================================

create or replace view v_maquina_estoque
    with (security_invoker = true) as
select count(distinct pacote) as pacotes,
    count(distinct pacote) filter (where status = 'publicado') as publicados,
    count(distinct pacote) filter (where status = 'erro') as com_erro,
    count(distinct pacote) filter (where status = 'listado_para_publicacao') as aguardando_publicacao,
    round(sum(duracao_s) filter (where formato = 'longo') / 3600.0, 1) as horas_de_longo,
    round(avg(duracao_s) filter (where formato = 'longo')) as duracao_media_s
from videos;

create or replace view v_maquina_fila
    with (security_invoker = true) as
select slug, nome, idioma, nicho, voz, estilo,
    (youtube_channel_id is not null) as no_youtube,
    pacotes, ultimo_pacote_em, trilha, fonte, duracao_alvo_s,
    nicho_mediana_vd, nicho_medido_em,
    (select count(distinct coalesce(v.pacote, regexp_replace(v.slug, '-short$', '')))
        from videos v
        where v.canal = c.slug
            and v.status not in ('erro', 'cancelado')
            and v.criado_em > now() - interval '24:00:00') as pacotes_24h,
    (select count(distinct coalesce(v.pacote, regexp_replace(v.slug, '-short$', '')))
        from videos v where v.canal = c.slug) as pacotes_registrados,
    (youtube_channel_id is not null) and (
        (select count(distinct coalesce(v.pacote, regexp_replace(v.slug, '-short$', '')))
            from videos v
            where v.canal = c.slug
                and v.status not in ('erro', 'cancelado')
                and v.criado_em > now() - interval '24:00:00') < 3
    ) as pode_produzir
from canais c
where ativo
order by (youtube_channel_id is null), ultimo_pacote_em nulls first;

-- v_maquina_rodizio, v_maquina_placar, v_maquina_meta_longos e
-- v_maquina_longos_liberados: criadas direto em producao apos o fix de
-- 2026-08-05 e nunca tinham passado por este arquivo nem levado
-- security_invoker — mesma classe de vazamento pra anon/authenticated via
-- PostgREST, achada de novo pelo Supabase Advisor em 2026-08-13. Definicoes
-- capturadas de producao via pg_get_viewdef, security_invoker adicionado.

create or replace view v_maquina_meta_longos
    with (security_invoker = true) as
select c.slug, c.idioma,
    count(*) filter (where v.formato = 'longo') as longos,
    count(*) filter (where v.formato = 'shorts') as shorts,
    10 as meta,
    greatest(0, 10 - count(*) filter (where v.formato = 'longo')) as faltam,
    round(coalesce(sum(v.duracao_s) filter (where v.formato = 'longo'), 0) / 3600.0, 2) as horas_no_ar
from canais c
left join videos v on v.canal = c.slug and v.status = 'publicado'
where c.ativo
group by c.slug, c.idioma;

create or replace view v_maquina_longos_liberados
    with (security_invoker = true) as
select slug, longos, faltam, horas_no_ar
from v_maquina_meta_longos
where faltam > 0;

create or replace view v_maquina_placar
    with (security_invoker = true) as
with ultima as (
    select distinct on (metricas.youtube_id) metricas.youtube_id, metricas.views
    from metricas
    order by metricas.youtube_id, metricas.coletado_em desc
)
select v.canal as slug, v.formato,
    count(*) as publicados,
    round(avg(extract(epoch from now() - v.publicado_em) / 86400.0), 1) as idade_media_dias,
    round(avg(coalesce(u.views, 0)::numeric / greatest(extract(epoch from now() - v.publicado_em) / 86400.0, 1)), 2) as views_por_dia,
    max(u.views) as melhor,
    count(*) filter (where u.views is null) as sem_metrica
from videos v
left join ultima u on u.youtube_id = v.youtube_id
where v.status = 'publicado'
    and v.canal is not null
    and v.publicado_em is not null
    and (now() - v.publicado_em) > interval '48:00:00'
group by v.canal, v.formato
order by (round(avg(coalesce(u.views, 0)::numeric / greatest(extract(epoch from now() - v.publicado_em) / 86400.0, 1)), 2)) desc nulls last;

create or replace view v_maquina_rodizio
    with (security_invoker = true) as
select f.slug, f.nome, f.idioma, f.nicho, f.voz, f.estilo,
    f.no_youtube, f.pacotes, f.ultimo_pacote_em, f.trilha, f.fonte, f.duracao_alvo_s,
    f.nicho_mediana_vd, f.nicho_medido_em, f.pacotes_24h, f.pacotes_registrados, f.pode_produzir,
    exists (select 1 from config g where g.chave = 'canais_verificados' and (g.valor -> 'allowed') ? f.slug) as verificado,
    coalesce(m.faltam, 10) as faltam_longos
from v_maquina_fila f
left join v_maquina_meta_longos m on m.slug = f.slug
where f.pode_produzir
    and exists (select 1 from config g where g.chave = 'yt_token_' || f.slug and (g.valor ->> 'refresh_token') is not null)
order by coalesce(m.faltam, 10) desc, f.ultimo_pacote_em nulls first;

create or replace view v_maquina_formatos
    with (security_invoker = true) as
select canal, formato, veredito, count(*) as n,
    round(percentile_cont(0.5) within group (order by views_dia::double precision)::numeric, 1) as mediana_vd,
    round(max(views_dia), 1) as topo_vd,
    max(medido_em) as medido_em
from pautas_banco
where formato is not null
group by canal, formato, veredito
order by canal, round(percentile_cont(0.5) within group (order by views_dia::double precision)::numeric, 1) desc;

create or replace view v_maquina_regras
    with (security_invoker = true) as
select categoria, severidade, titulo, regra, aplicado_em, confianca, evidencia
from aprendizados
where status = 'ativo'
order by array_position(array['critico','alto','medio','baixo'], severidade), categoria;
