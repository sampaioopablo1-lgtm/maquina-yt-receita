-- 13/08/2026 — coordenada de verdade para os anúncios sem GPS.
--
-- 1.506 anúncios no ar não têm coordenada. A propagação por CEP idêntico, que
-- já roda, está esgotada: sobraram 4 casos. A alternativa fácil seria usar a
-- média do bairro (505 casos teriam vizinhos suficientes), mas isso põe o pin
-- no centroide do bairro — quilômetros longe do imóvel, e incoerente com o
-- endereço que publicamos por extenso. Número inventado com cara de precisão.
--
-- Em vez disso, geocodificamos o logradouro real via Nominatim (OpenStreetMap),
-- que é gratuito. A contrapartida é o ritmo: a política de uso pede no máximo
-- uma consulta por segundo, então o processamento é em lotes de 40 a cada 15
-- minutos, com pausa de 1,2s entre chamadas dentro do lote.
--
-- O controle de tentativas mora em tabela própria e não em `dados_normalizados`
-- porque o sync reescreve esse JSON a cada ciclo — o marcador se perderia e o
-- mesmo endereço sem solução seria consultado pra sempre.

create table if not exists public.feed_geocode_log (
  codigo text primary key,
  status text not null default 'pendente',
  tentativas int not null default 0,
  latitude numeric,
  longitude numeric,
  detalhe text,
  ultima_tentativa timestamptz,
  atualizado_em timestamptz not null default now()
);

create index if not exists idx_feed_geocode_log_status on public.feed_geocode_log (status, ultima_tentativa);

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
    and fp.dados_normalizados->>'latitude' is null
    and coalesce(nullif(fp.dados_normalizados->>'endereco',''),
                 nullif(fp.dados_normalizados->>'endereco_viacep','')) is not null
    -- nunca tentado, ou falhou pouco e faz tempo: endereço ruim não vira fila infinita
    and (g.codigo is null
         or (g.status <> 'ok' and g.tentativas < 3
             and coalesce(g.ultima_tentativa, 'epoch'::timestamptz) < now() - interval '7 days'))
  order by (fp.dados_normalizados->>'valor_venda')::numeric desc nulls last
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
  -- do geocodificador, não endereço exótico.
  if p_status = 'ok' and p_lat is not null and p_lon is not null
     and p_lat between -25.35 and -19.75 and p_lon between -53.35 and -44 then
    update public.feed_properties
       set dados_normalizados = dados_normalizados
             || jsonb_build_object('latitude', p_lat, 'longitude', p_lon,
                                   'gps_origem', 'nominatim'),
           updated_at = now()
     where codigo_original = p_codigo
       and dados_normalizados->>'latitude' is null;
    v_gravou := found;
  end if;

  return v_gravou;
end;
$$;

revoke all on function public.fn_geocode_candidatos(int) from public, anon;
revoke all on function public.fn_geocode_registrar(text, text, numeric, numeric, text) from public, anon;

-- Chave publishable, a mesma que os demais crons deste projeto usam: ela é
-- pública por definição (vai no front-end), o que protege a função é o RLS.
select cron.schedule('feed-geocode-enderecos', '*/15 * * * *', $cron$
  select net.http_post(
    url := 'https://cscczluzpblzhvojxanp.supabase.co/functions/v1/geocode-enderecos',
    headers := jsonb_build_object(
      'apikey','sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
      'Authorization','Bearer sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
      'Content-Type','application/json'),
    body := '{"lote":40}'::jsonb,
    timeout_milliseconds := 120000)
$cron$);
