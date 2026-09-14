drop table if exists public.captacao_prospects cascade;
create table public.captacao_prospects (
  id bigserial primary key, fonte text not null, anuncio_id text, url text, titulo text,
  tipo text, cidade text, bairro text, endereco text, preco numeric, area numeric,
  quartos int, vagas int, anunciante text, telefone text, whatsapp text,
  tem_creci boolean not null default false, creci text, perfil text, motivo_perfil text,
  anuncios_no_telefone int, dados jsonb,
  coletado_em timestamptz not null default now(), sugerido_em timestamptz,
  status text not null default 'novo'
);
\i /home/user/maquina-yt-receita/jazz/supabase/migrations/20260914_captacao_sinais_pf_pj_e_logo.sql
-- aplicar DUAS vezes: a migração tem de ser idempotente
\i /home/user/maquina-yt-receita/jazz/supabase/migrations/20260914_captacao_sinais_pf_pj_e_logo.sql

-- 9 de 10 com logo: o portal passou a carimbar todo mundo
insert into public.captacao_prospects (fonte,anuncio_id,anunciante,telefone,dados)
select 'zapimoveis.com.br','L'||g, 'Pessoa Numero'||g, '1198888'||lpad(g::text,4,'0'),
       '{"advertiser":{"logoUrl":"https://x/l.png"}}'::jsonb
  from generate_series(1,9) g;
insert into public.captacao_prospects (fonte,anuncio_id,anunciante,telefone,dados)
values ('zapimoveis.com.br','L10','Maria Souza','11988889999','{"advertiser":{}}');

select public.fn_captacao_classificar(4) as com_trava;

do $$
declare n int; j jsonb;
begin
  select public.fn_captacao_classificar(4) into j;
  assert (j->>'logo_em_uso')::boolean = false, 'a trava deveria ter desligado o sinal de logo';
  select count(*) into n from captacao_prospects where perfil='particular';
  assert n = 10, format('com a trava, os 10 deveriam seguir particular, vieram %s', n);
  -- e com o teto solto, o sinal volta e engole 9
  select public.fn_captacao_classificar(4, 1.0) into j;
  assert (j->>'logo_em_uso')::boolean = true, 'com teto 1.0 o sinal deveria estar ligado';
  select count(*) into n from captacao_prospects where perfil='empresa';
  assert n = 9, format('sem trava, 9 deveriam virar empresa, vieram %s', n);
  raise notice 'TRAVA OK: desliga sozinha e preserva os 10 particulares';
end $$;
