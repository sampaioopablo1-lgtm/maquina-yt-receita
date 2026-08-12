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
    (select count(*) from videos v where v.canal = c.slug and v.criado_em > now() - interval '24:00:00') as pacotes_24h,
    (select count(distinct v.pacote) from videos v where v.canal = c.slug) as pacotes_registrados
from canais c
where ativo
order by (youtube_channel_id is null), ultimo_pacote_em nulls first;

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
