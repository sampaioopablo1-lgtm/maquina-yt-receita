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
create or replace view painel_pilares as
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
create or replace view progresso_ypp as
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
create policy if not exists "service_role_videos"
    on videos for all to service_role using (true) with check (true);
create policy if not exists "service_role_metricas"
    on metricas for all to service_role using (true) with check (true);
