-- Máquina de cold mail (coldmail/tools/cold.py). Rode uma vez no SQL Editor do Supabase.
-- RLS ligado e SEM policy: só a service_role (segredo do Actions) lê e grava. O repositório é público,
-- então nenhum dado de lead fica em arquivo; fica aqui.

create table if not exists cold_leads (
    id bigint generated always as identity primary key,
    email text not null unique,
    primeiro_nome text, empresa text, cargo text, site text, abertura text, extra text,
    status text not null default 'ativo',   -- ativo | concluido | respondeu | reuniao | nao_agora | descadastro | bounce | pausado
    passo int not null default 0,           -- índice do PRÓXIMO passo da sequência
    proximo_envio timestamptz,
    conta text,                             -- caixa que conversa com o lead (follow-up sai sempre dela)
    assunto text, thread_msgid text, ultimo_msgid text,
    categoria text, ghl_contato text,
    criado_em timestamptz not null default now(),
    atualizado_em timestamptz
);
create index if not exists cold_leads_fila on cold_leads (status, proximo_envio);

create table if not exists cold_envios (
    id bigint generated always as identity primary key,
    lead_id bigint not null references cold_leads (id) on delete cascade,
    conta text not null, passo int not null,
    message_id text not null, enviado_em timestamptz not null
);
create index if not exists cold_envios_dia on cold_envios (enviado_em);

create table if not exists cold_mensagens (
    message_id text primary key,            -- cada e-mail recebido é processado uma vez só
    lead_id bigint references cold_leads (id) on delete set null,
    conta text not null, recebido_em timestamptz not null,
    tipo text not null,                     -- resposta | bounce | ignorada | outra
    categoria text, confianca real, acao text
);
create index if not exists cold_mensagens_dia on cold_mensagens (recebido_em);

create table if not exists cold_bloqueio (     -- nunca mais recebe e-mail (descadastro, bounce)
    email text primary key, motivo text,
    criado_em timestamptz not null default now()
);

alter table cold_leads enable row level security;
alter table cold_envios enable row level security;
alter table cold_mensagens enable row level security;
alter table cold_bloqueio enable row level security;
