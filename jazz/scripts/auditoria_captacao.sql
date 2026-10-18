-- Auditoria da máquina de captação de particulares.
-- Cole no SQL Editor do Supabase (projeto cscczluzpblzhvojxanp) e rode inteiro.
-- Só lê. Não altera nada.
--
-- Responde, com o dado real: a máquina existe, está coletando, e o que ela
-- entrega é telefone de pessoa física ou de corretor?

\echo '=== 1. A MÁQUINA ESTÁ LIGADA? ==='
select jobname, schedule, active,
       (select max(start_time) from cron.job_run_details d where d.jobid = j.jobid) as ultima_execucao,
       (select count(*) from cron.job_run_details d
         where d.jobid = j.jobid and d.status = 'failed'
           and d.start_time > now() - interval '5 days') as falhas_5d
  from cron.job j
 where jobname like 'captacao%'
 order by jobname;

\echo ''
\echo '=== 2. COLETOU O QUÊ, NOS ÚLTIMOS 5 DIAS? ==='
select date_trunc('day', coletado_em)::date as dia,
       count(*)                                   as anuncios,
       count(*) filter (where telefone is not null) as com_telefone,
       count(distinct telefone)                    as telefones_distintos,
       count(distinct fonte)                       as portais
  from public.captacao_prospects
 where coletado_em > now() - interval '5 days'
 group by 1 order by 1 desc;

\echo ''
\echo '=== 3. O QUE A RÉGUA DIZ QUE É PESSOA FÍSICA ==='
select perfil, count(*),
       round(100.0*count(*)/nullif(sum(count(*)) over (), 0), 1) as pct,
       count(*) filter (where telefone is not null) as com_telefone
  from public.captacao_prospects
 group by perfil order by 2 desc;

\echo ''
\echo '=== 4. O TESTE DE VERDADE: quantos anúncios por telefone? ==='
-- Proprietário tem 1, às vezes 2. Quem tem 4+ é carteira de corretor.
-- Se muita linha classificada como `particular` tem telefone repetido,
-- a lista do captador está cheia de corretor.
with c as (
  select telefone, perfil, count(distinct coalesce(anuncio_id, id::text)) n
    from public.captacao_prospects
   where telefone is not null and perfil = 'particular'
   group by telefone, perfil
)
select case when n = 1 then '1 anúncio  (dono)'
            when n = 2 then '2 anúncios (dono, plausível)'
            when n = 3 then '3 anúncios (suspeito)'
            else n || '+ anúncios (CARTEIRA DE CORRETOR)' end as faixa,
       count(*) as telefones, sum(n) as anuncios
  from c group by 1, (n>=4), n order by min(n);

\echo ''
\echo '=== 5. QUANTO O BUG DO SOBRENOME CUSTA (Barbosa/Sousa/Rosa/Pedrosa) ==='
-- Régua atual: s/?a$ sem fronteira de palavra come qualquer nome em "sa".
select count(*) filter (where anunciante ~ '(?i)s/?a\.?$')      as pega_a_regua_atual,
       count(*) filter (where anunciante ~ '(?i)\ys[./]?a\.?$') as pega_a_corrigida,
       count(*) filter (where anunciante ~ '(?i)s/?a\.?$'
                         and anunciante !~ '(?i)\ys[./]?a\.?$') as PROPRIETARIOS_PERDIDOS
  from public.captacao_prospects;

select anunciante, telefone, perfil
  from public.captacao_prospects
 where anunciante ~ '(?i)s/?a\.?$' and anunciante !~ '(?i)\ys[./]?a\.?$'
 order by anunciante limit 25;

\echo ''
\echo '=== 6. A MELHORIA JÁ FOI APLICADA NESTE BANCO? ==='
select
  (to_regclass('public.captacao_nao_perturbe') is not null)                     as tem_nao_perturbe,
  exists (select 1 from information_schema.columns
           where table_name='captacao_prospects' and column_name='score')       as tem_score,
  exists (select 1 from information_schema.columns
           where table_name='captacao_prospects' and column_name='ex_carteira') as tem_ex_carteira,
  (select count(*) from pg_proc p join pg_namespace n on n.oid=p.pronamespace
    where n.nspname='public' and p.proname='fn_captacao_classificar')           as assinaturas_classificar;
-- tudo false/1 = a migração 20260909 NÃO foi aplicada; o banco está na régua de 13/08.

\echo ''
\echo '=== 7. O FUNIL FECHOU? sugerido -> virou solicitação -> virou captação ==='
select count(*) filter (where sugerido_em is not null)                          as ja_sugeridos,
       count(*) filter (where sugerido_em > now() - interval '5 days')          as sugeridos_5d,
       count(*) filter (where status not in ('novo','sugerido'))                as com_desfecho_registrado
  from public.captacao_prospects;
