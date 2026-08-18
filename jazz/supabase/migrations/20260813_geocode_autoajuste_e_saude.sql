-- 13/08/2026 — o geocodificador passa a se ajustar sozinho.
--
-- O risco do trabalho não terminar não é a fila ser grande: é ninguém perceber
-- que ela parou. As formas de parar são conhecidas — Nominatim devolvendo 429,
-- rede caindo, o banco ficando pesado como ficou hoje, ou a fila simplesmente
-- acabando e o cron continuar batendo à toa.
--
-- Esta função olha as últimas duas horas de resultado e mexe no próprio ritmo:
-- acelera quando está limpo e tem fila, desacelera quando aparece erro, religa
-- o disparo se ele foi desligado e a fila voltou a encher, alerta quando há
-- trabalho e nenhuma tentativa, e se desliga quando não há mais o que fazer.
-- Cada decisão fica registrada em `feed_geocode_saude` com o motivo, pra que a
-- supervisão veja o porquê e não só o efeito.

create table if not exists public.feed_geocode_saude (
  id bigserial primary key,
  medido_em timestamptz not null default now(),
  na_fila int,
  processados_2h int,
  ok_2h int,
  erro_2h int,
  taxa_erro numeric(5,2),
  ritmo text,
  decisao text,
  motivo text
);

create or replace function public.fn_geocode_saude_e_ajuste()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_fila int;
  v_proc int;
  v_ok int;
  v_erro int;
  v_taxa numeric(5,2) := 0;
  v_ritmo text;
  v_decisao text := 'manter';
  v_motivo text := 'dentro do esperado';
  v_ativo boolean;
  v_cron text := '*/5 * * * *';
begin
  select count(*) into v_fila from public.feed_geocode_fila where entregue_em is null
     or entregue_em < now() - interval '30 minutes';

  select count(*), count(*) filter (where status = 'ok'), count(*) filter (where status = 'erro')
    into v_proc, v_ok, v_erro
  from public.feed_geocode_log where ultima_tentativa >= now() - interval '2 hours';

  if v_proc > 0 then v_taxa := round((v_erro::numeric / v_proc) * 100, 2); end if;

  select schedule, active into v_ritmo, v_ativo from cron.job where jobname = 'feed-geocode-enderecos';

  -- 1) Acabou o serviço: desliga o disparo e para de bater no Nominatim à toa.
  if v_fila = 0 then
    if v_ativo is true then
      perform cron.unschedule('feed-geocode-enderecos');
      v_decisao := 'desligado';
      v_motivo := 'fila zerada — trabalho concluído';
    else
      v_decisao := 'ocioso';
      v_motivo := 'fila zerada e disparo já desligado';
    end if;

  -- 2) Fila voltou a encher (imóvel novo, ou reposição semanal) e o disparo
  --    estava desligado: religa.
  elsif v_ativo is not true then
    perform cron.schedule('feed-geocode-enderecos', v_cron, $cron$
      select net.http_post(
        url := 'https://cscczluzpblzhvojxanp.supabase.co/functions/v1/geocode-enderecos',
        headers := jsonb_build_object(
          'apikey','sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
          'Authorization','Bearer sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
          'Content-Type','application/json'),
        body := '{"lote":60}'::jsonb,
        timeout_milliseconds := 180000)
    $cron$);
    v_decisao := 'religado';
    v_motivo := format('fila com %s pendentes e disparo desligado', v_fila);

  -- 3) Erro demais: recua. Nominatim reclamando ou rede instável não se
  --    resolve insistindo mais forte.
  elsif v_proc >= 20 and v_taxa >= 30 then
    perform cron.unschedule('feed-geocode-enderecos');
    perform cron.schedule('feed-geocode-enderecos', '*/20 * * * *', $cron$
      select net.http_post(
        url := 'https://cscczluzpblzhvojxanp.supabase.co/functions/v1/geocode-enderecos',
        headers := jsonb_build_object(
          'apikey','sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
          'Authorization','Bearer sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
          'Content-Type','application/json'),
        body := '{"lote":25}'::jsonb,
        timeout_milliseconds := 180000)
    $cron$);
    v_decisao := 'desacelerado';
    v_motivo := format('%s%% de erro em %s tentativas nas últimas 2h', v_taxa, v_proc);

  -- 4) Parou de processar apesar de ter fila: alguma coisa travou.
  elsif v_proc = 0 and v_fila > 0 then
    insert into public.vista_alertas (codigo_vista, tipo, dados)
    select '__geocode__', 'feed_espelho_parado',
           jsonb_build_object('origem','fn_geocode_saude_e_ajuste','na_fila',v_fila,
                              'detalhe','2h sem nenhuma tentativa registrada','detectado_em',now())
    where not exists (select 1 from public.vista_alertas a
                      where a.codigo_vista = '__geocode__'
                        and a.created_at > now() - interval '6 hours');
    v_decisao := 'alerta';
    v_motivo := 'fila com trabalho e nenhuma tentativa em 2h';

  -- 5) Limpo e com fila: volta ao ritmo cheio se estiver recuado.
  elsif v_taxa < 5 and v_fila > 200 and v_ritmo <> '*/5 * * * *' then
    perform cron.unschedule('feed-geocode-enderecos');
    perform cron.schedule('feed-geocode-enderecos', v_cron, $cron$
      select net.http_post(
        url := 'https://cscczluzpblzhvojxanp.supabase.co/functions/v1/geocode-enderecos',
        headers := jsonb_build_object(
          'apikey','sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
          'Authorization','Bearer sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
          'Content-Type','application/json'),
        body := '{"lote":60}'::jsonb,
        timeout_milliseconds := 180000)
    $cron$);
    v_decisao := 'acelerado';
    v_motivo := format('%s%% de erro e %s na fila', v_taxa, v_fila);
  end if;

  insert into public.feed_geocode_saude (na_fila, processados_2h, ok_2h, erro_2h, taxa_erro,
                                         ritmo, decisao, motivo)
  values (v_fila, v_proc, v_ok, v_erro, v_taxa,
          coalesce((select schedule from cron.job where jobname='feed-geocode-enderecos'), 'desligado'),
          v_decisao, v_motivo);

  return jsonb_build_object('ok', true, 'na_fila', v_fila, 'processados_2h', v_proc,
                            'ok_2h', v_ok, 'erro_2h', v_erro, 'taxa_erro', v_taxa,
                            'decisao', v_decisao, 'motivo', v_motivo);
end;
$$;

revoke all on function public.fn_geocode_saude_e_ajuste() from public, anon;

select cron.schedule('feed-geocode-saude', '13,33,53 * * * *',
                     $cron$select public.fn_geocode_saude_e_ajuste();$cron$);
