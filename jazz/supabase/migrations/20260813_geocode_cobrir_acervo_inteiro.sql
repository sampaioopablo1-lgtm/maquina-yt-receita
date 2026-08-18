-- 13/08/2026 — o geocodificador passa a cobrir todo o acervo publicado.
--
-- Além dos 1.487 sem GPS, entram os 482 marcados `gps_origem = cep_vizinho`:
-- coordenada herdada da média dos vizinhos de mesmo CEP, que acerta a rua mas
-- não o imóvel. Trocar aproximação por logradouro geocodificado é ganho real.
--
-- O que continua intocado são as coordenadas vindas do próprio Vista.
-- Conferido contra o XML nativo: das 1.607 fichas que o Vista publica com
-- coordenada, só 19 estão sem GPS aqui e 11 estão aproximadas — o backfill de
-- ficha já capturou o resto. Não há motivo pra reconsultar o que a fonte já
-- respondeu, nem pra mexer no bundle da Edge Function por 30 casos.

create or replace function public.fn_geocode_candidatos(p_limite int default 40)
returns table(codigo text, endereco text, bairro text, cidade text, cep text)
language sql
security definer
set search_path = public
as $$
  select fp.codigo_original,
         coalesce(nullif(fp.dados_normalizados->>'endereco',''),
                  nullif(fp.dados_normalizados->>'endereco_viacep','')),
         nullif(fp.dados_normalizados->>'bairro',''),
         nullif(fp.dados_normalizados->>'cidade',''),
         nullif(regexp_replace(coalesce(fp.dados_normalizados->>'cep',''),'\D','','g'),'')
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
  -- quem não tem nada primeiro; depois os aproximados, do mais caro pro mais barato
  order by (fp.dados_normalizados->>'latitude' is not null),
           (fp.dados_normalizados->>'valor_venda')::numeric desc nulls last
  limit greatest(1, p_limite);
$$;

create or replace function public.fn_geocode_registrar(
  p_codigo text, p_status text, p_lat numeric default null,
  p_lon numeric default null, p_detalhe text default null)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare
  v_gravou boolean := false;
begin
  insert into public.feed_geocode_log (codigo, status, tentativas, latitude, longitude, detalhe,
                                       ultima_tentativa, atualizado_em)
  values (p_codigo, p_status, 1, p_lat, p_lon, p_detalhe, now(), now())
  on conflict (codigo) do update
    set status = excluded.status,
        tentativas = public.feed_geocode_log.tentativas + 1,
        latitude = coalesce(excluded.latitude, public.feed_geocode_log.latitude),
        longitude = coalesce(excluded.longitude, public.feed_geocode_log.longitude),
        detalhe = excluded.detalhe,
        ultima_tentativa = now(),
        atualizado_em = now();

  -- Só grava coordenada plausível pra São Paulo; fora disso é match errado
  -- do geocodificador, não endereço exótico. E só por cima de quem não tem
  -- coordenada ou tem a aproximada por CEP vizinho — nunca por cima do Vista.
  if p_status = 'ok' and p_lat is not null and p_lon is not null
     and p_lat between -25.35 and -19.75 and p_lon between -53.35 and -44 then
    update public.feed_properties
       set dados_normalizados = dados_normalizados
             || jsonb_build_object('latitude', p_lat, 'longitude', p_lon,
                                   'gps_origem', 'nominatim'),
           updated_at = now()
     where codigo_original = p_codigo
       and (dados_normalizados->>'latitude' is null
            or dados_normalizados->>'gps_origem' = 'cep_vizinho');
    v_gravou := found;
  end if;

  return v_gravou;
end;
$$;

-- Ritmo maior pra fechar o acervo em algumas horas: 60 a cada 10 minutos dá
-- 0,1 consulta por segundo em média, bem abaixo do teto de 1/s do Nominatim.
select cron.unschedule('feed-geocode-enderecos');
select cron.schedule('feed-geocode-enderecos', '*/10 * * * *', $cron$
  select net.http_post(
    url := 'https://cscczluzpblzhvojxanp.supabase.co/functions/v1/geocode-enderecos',
    headers := jsonb_build_object(
      'apikey','sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
      'Authorization','Bearer sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
      'Content-Type','application/json'),
    body := '{"lote":60}'::jsonb,
    timeout_milliseconds := 180000)
$cron$);
