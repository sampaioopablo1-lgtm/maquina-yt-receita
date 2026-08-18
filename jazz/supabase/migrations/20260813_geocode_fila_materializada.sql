-- 13/08/2026 — a fila do geocodificador vira tabela, em vez de ser recalculada
-- a cada lote.
--
-- Motivo: com lotes de 120 a cada 5 minutos, o banco passou a recusar conexões.
-- `fn_geocode_candidatos` varria as 3.911 linhas de `feed_properties` lendo
-- campos de dentro do JSON, com join e ordenação por valor convertido — tudo
-- isso a cada chamada, concorrendo com o sync, o precomputar e os demais crons
-- no mesmo banco que atende o CRM e os leads.
--
-- Agora a varredura pesada roda uma vez por hora e grava o resultado; cada
-- lote só faz um SELECT indexado — medido em 15 ms contra o scan completo de
-- antes. O processo continua o mesmo e igualmente completo: o que muda é
-- quantas vezes o trabalho caro é refeito.

create table if not exists public.feed_geocode_fila (
  codigo text primary key,
  endereco text not null,
  bairro text,
  cidade text,
  cep text,
  valor numeric,
  aproximado boolean not null default false,
  entregue_em timestamptz,
  criado_em timestamptz not null default now()
);

create index if not exists idx_feed_geocode_fila_ordem
  on public.feed_geocode_fila (aproximado, valor desc nulls last)
  where entregue_em is null;

create or replace function public.fn_geocode_repor_fila()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_inseridos int := 0;
  v_limpos int := 0;
begin
  -- Sai da fila quem já resolveu ou esgotou tentativas.
  delete from public.feed_geocode_fila f
  using public.feed_geocode_log g
  where g.codigo = f.codigo
    and (g.status = 'ok' or g.tentativas >= 3);
  get diagnostics v_limpos = row_count;

  insert into public.feed_geocode_fila (codigo, endereco, bairro, cidade, cep, valor, aproximado)
  select fp.codigo_original,
         coalesce(nullif(fp.dados_normalizados->>'endereco',''),
                  nullif(fp.dados_normalizados->>'endereco_viacep','')),
         nullif(fp.dados_normalizados->>'bairro',''),
         nullif(fp.dados_normalizados->>'cidade',''),
         nullif(regexp_replace(coalesce(fp.dados_normalizados->>'cep',''),'\D','','g'),''),
         (fp.dados_normalizados->>'valor_venda')::numeric,
         fp.dados_normalizados->>'latitude' is not null
  from public.feed_properties fp
  left join public.feed_property_portal_publicacao p
    on p.property_id = fp.id and p.portal = 'vrsync_rede'
  left join public.feed_geocode_log g on g.codigo = fp.codigo_original
  where fp.ativo
    and coalesce(p.habilitado, true)
    and (fp.dados_normalizados->>'latitude' is null
         or fp.dados_normalizados->>'gps_origem' = 'cep_vizinho')
    and coalesce(nullif(fp.dados_normalizados->>'endereco',''),
                 nullif(fp.dados_normalizados->>'endereco_viacep','')) is not null
    and (g.codigo is null
         or (g.status <> 'ok' and g.tentativas < 3
             and coalesce(g.ultima_tentativa, 'epoch'::timestamptz) < now() - interval '7 days'))
  on conflict (codigo) do nothing;
  get diagnostics v_inseridos = row_count;

  return jsonb_build_object('ok', true, 'inseridos', v_inseridos, 'removidos', v_limpos,
                            'na_fila', (select count(*) from public.feed_geocode_fila where entregue_em is null));
end;
$$;

-- Entrega barata: um SELECT pelo índice, marcando o que saiu pra não reentregar
-- no lote seguinte. Se o lote morrer no meio, a reserva vence em 30 minutos.
create or replace function public.fn_geocode_candidatos(p_limite int default 40)
returns table(codigo text, endereco text, bairro text, cidade text, cep text)
language sql
security definer
set search_path = public
as $$
  with escolhidos as (
    select f.codigo from public.feed_geocode_fila f
    where f.entregue_em is null
       or f.entregue_em < now() - interval '30 minutes'
    order by f.aproximado, f.valor desc nulls last
    limit greatest(1, p_limite)
  ), reservados as (
    update public.feed_geocode_fila f set entregue_em = now()
    where f.codigo in (select codigo from escolhidos)
    returning f.codigo, f.endereco, f.bairro, f.cidade, f.cep
  )
  select codigo, endereco, bairro, cidade, cep from reservados;
$$;

revoke all on function public.fn_geocode_repor_fila() from public, anon;
revoke all on function public.fn_geocode_candidatos(int) from public, anon;

select public.fn_geocode_repor_fila();

select cron.schedule('feed-geocode-repor-fila', '7 * * * *',
                     $cron$select public.fn_geocode_repor_fila();$cron$);

-- Ritmo: 60 a cada 5 minutos. Com o lote barato, o limite passa a ser o
-- Nominatim (1,2s entre chamadas), não o banco.
select cron.unschedule('feed-geocode-enderecos');
select cron.schedule('feed-geocode-enderecos', '*/5 * * * *', $cron$
  select net.http_post(
    url := 'https://cscczluzpblzhvojxanp.supabase.co/functions/v1/geocode-enderecos',
    headers := jsonb_build_object(
      'apikey','sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
      'Authorization','Bearer sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
      'Content-Type','application/json'),
    body := '{"lote":60}'::jsonb,
    timeout_milliseconds := 180000)
$cron$);
