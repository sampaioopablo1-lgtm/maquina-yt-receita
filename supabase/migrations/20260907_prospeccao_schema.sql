-- Schema da maquina de prospeccao (src/prospeccao). Espelha o SQLite local
-- (src/prospeccao/storage.py) para o estado sobreviver a um runner efemero,
-- no mesmo espirito da tabela `videos` da maquina de video.
--
-- RLS liberada so para a service_role: o app fala com o Supabase usando
-- SUPABASE_SERVICE_ROLE_KEY (nunca a anon key), entao nao ha usuario final
-- multi-tenant para isolar aqui.

create table if not exists leads (
    id               text primary key,
    status           text not null,
    etapa_sequencia  integer not null default 0,
    proxima_acao_em  timestamptz,
    payload          jsonb not null,
    criado_em        timestamptz not null,
    atualizado_em    timestamptz not null
);
create index if not exists idx_leads_status on leads(status);
create index if not exists idx_leads_proxima_acao on leads(proxima_acao_em);

create table if not exists mensagens (
    id          bigint generated always as identity primary key,
    lead_id     text not null references leads(id) on delete cascade,
    canal       text not null,
    etapa       integer not null,
    texto       text not null,
    resposta    boolean not null default false,
    enviado_em  timestamptz not null
);
create index if not exists idx_mensagens_lead on mensagens(lead_id);

create table if not exists reunioes (
    id                  bigint generated always as identity primary key,
    lead_id             text not null references leads(id) on delete cascade,
    inicio              timestamptz not null,
    fim                 timestamptz not null,
    calendar_event_id   text,
    meet_url            text,
    criado_em           timestamptz not null
);
create index if not exists idx_reunioes_lead on reunioes(lead_id);

create table if not exists envios_dia (
    dia    date not null,
    canal  text not null,
    tipo   text not null,
    total  integer not null default 0,
    primary key (dia, canal, tipo)
);

alter table leads enable row level security;
alter table mensagens enable row level security;
alter table reunioes enable row level security;
alter table envios_dia enable row level security;

create policy "service_role_all_leads" on leads for all
    using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy "service_role_all_mensagens" on mensagens for all
    using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy "service_role_all_reunioes" on reunioes for all
    using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy "service_role_all_envios_dia" on envios_dia for all
    using (auth.role() = 'service_role') with check (auth.role() = 'service_role');

create view funil_prospeccao as
    select status, count(*) as total
    from leads
    group by status;
