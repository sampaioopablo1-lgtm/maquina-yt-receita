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

insert into public.captacao_prospects (fonte,anuncio_id,anunciante,telefone,tem_creci,dados) values
 -- o resgate: PF declarado, nome de UMA palavra, um anúncio só
 ('chavesnamao.com.br','A1','Marcelo','11988880001',false,'{"advertiser_type":"PF"}'),
 -- PJ declarado, nome que NAO denuncia nada
 ('chavesnamao.com.br','A2','Solar do Vale','11988880002',false,'{"advertiser_type":"PJ"}'),
 -- logo cadastrado, nome limpo de duas palavras (viraria particular antes)
 ('zapimoveis.com.br','A3','Ana Ribeiro','11988880003',false,'{"advertiser":{"name":"Ana Ribeiro","logoUrl":"https://x/l.png"}}'),
 -- logo com OUTRO nome de chave: o sinal nao pode depender da grafia
 ('zapimoveis.com.br','A4','Bruno Tavares','11988880004',false,'{"advertiser":{"logotipo":"https://x/b.png"}}'),
 -- logo presente mas VAZIO: nao e sinal
 ('zapimoveis.com.br','A5','Carla Nunes','11988880005',false,'{"advertiser":{"logoUrl":""}}'),
 -- PF mas com carteira: 4 anuncios no mesmo telefone -> continua empresa
 ('chavesnamao.com.br','A6','Diego','11988880006',false,'{"advertiser_type":"PF"}'),
 ('chavesnamao.com.br','A7','Diego','11988880006',false,'{"advertiser_type":"PF"}'),
 ('chavesnamao.com.br','A8','Diego','11988880006',false,'{"advertiser_type":"PF"}'),
 ('chavesnamao.com.br','A9','Diego','11988880006',false,'{"advertiser_type":"PF"}'),
 -- os que ja funcionavam, que NAO podem mudar de classe
 ('vivareal.com.br','B1','Nelson Barbosa','11988880011',false,'{}'),
 ('vivareal.com.br','B2','SANT ANA INVESTIMENTOS','11988880012',false,'{}'),
 ('vivareal.com.br','B3','Fulano Imoveis Ltda','11988880013',false,'{}'),
 ('vivareal.com.br','B4','Joana Prado','11988880014',true,'{}'),
 ('vivareal.com.br','B5','Newcore','11988880015',false,'{}'),
 ('vivareal.com.br','B6','Sem Fone','11111111111',false,'{}');

select public.fn_captacao_classificar(4);

do $$
declare n int;
  procedure_falhou boolean := false;
begin
  -- 1. o resgate funciona
  select count(*) into n from captacao_prospects where anuncio_id='A1' and perfil='particular';
  assert n=1, 'A1: PF de uma palavra deveria ser particular';
  -- 2. PJ com nome inocente vira empresa
  select count(*) into n from captacao_prospects where anuncio_id='A2' and perfil='empresa';
  assert n=1, 'A2: PJ declarado deveria ser empresa';
  -- 3. logo pega quem o nome nao pegava
  select count(*) into n from captacao_prospects where anuncio_id='A3' and perfil='empresa';
  assert n=1, 'A3: logo deveria classificar como empresa';
  -- 4. grafia diferente da chave tambem
  select count(*) into n from captacao_prospects where anuncio_id='A4' and perfil='empresa';
  assert n=1, 'A4: logotipo deveria contar como logo';
  -- 5. logo vazio NAO e sinal
  select count(*) into n from captacao_prospects where anuncio_id='A5' and perfil='particular';
  assert n=1, 'A5: logo vazio nao pode virar empresa';
  -- 6. PF com carteira continua empresa
  select count(*) into n from captacao_prospects where anuncio_id='A6' and perfil='empresa';
  assert n=1, 'A6: PF com 4 anuncios deveria seguir empresa';
  -- 7..12 nada do que ja funcionava pode mudar
  select count(*) into n from captacao_prospects where anuncio_id='B1' and perfil='particular';
  assert n=1, 'B1: Nelson Barbosa deveria seguir particular';
  select count(*) into n from captacao_prospects where anuncio_id='B2' and perfil='empresa';
  assert n=1, 'B2: SANT ANA INVESTIMENTOS deveria seguir empresa';
  select count(*) into n from captacao_prospects where anuncio_id='B3' and perfil='empresa';
  assert n=1, 'B3: Ltda deveria seguir empresa';
  select count(*) into n from captacao_prospects where anuncio_id='B4' and perfil='empresa';
  assert n=1, 'B4: CRECI deveria seguir empresa';
  select count(*) into n from captacao_prospects where anuncio_id='B5' and perfil='indefinido';
  assert n=1, 'B5: Newcore deveria seguir indefinido';
  select count(*) into n from captacao_prospects where anuncio_id='B6' and perfil='descartar';
  assert n=1, 'B6: telefone falso deveria seguir descartar';
  raise notice 'TODAS AS 12 ASSERCOES PASSARAM';
end $$;

select anuncio_id, anunciante, perfil, motivo_perfil from captacao_prospects order by anuncio_id;
