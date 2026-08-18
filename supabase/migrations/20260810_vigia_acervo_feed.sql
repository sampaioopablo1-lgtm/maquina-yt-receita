-- Vigia do acervo publicado: detecta queda de anuncios no feed antes que
-- alguem perceba por acaso. Nasceu de 203 anuncios que ficaram desligados
-- de 04/08 a 10/08 sem ninguem notar.

create table if not exists public.feed_acervo_snapshot (
  dia            date primary key,
  ativos         integer not null,
  publicaveis    integer not null,
  divergentes    integer not null default 0,
  queda_pct      numeric(6,2),
  criado_em      timestamptz not null default now(),
  atualizado_em  timestamptz not null default now()
);

comment on table public.feed_acervo_snapshot is
  'Foto diaria do acervo do feed. publicaveis = ativos que passam nos filtros de emissao do XML (>=5 fotos validas e preco). divergentes = ativos no espelho do Vista porem desligados no feed.';

-- o tipo novo precisa ser liberado na constraint antes do vigia rodar
alter table public.vista_alertas drop constraint if exists vista_alertas_tipo_check;
alter table public.vista_alertas add constraint vista_alertas_tipo_check
  check (tipo = any (array[
    'venda_detectada','anuncio_parado','reativacao',
    'imovel_sumiu','nome_ambiguo','feed_anuncio_fora_do_ar'
  ]));

create or replace function public.fn_vigia_acervo_feed()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_ativos        integer;
  v_publicaveis   integer;
  v_divergentes   integer;
  v_ontem         integer;
  v_queda_pct     numeric(6,2) := null;
  v_novos_alertas integer := 0;
begin
  select count(*) filter (where fp.ativo),
         count(*) filter (where fp.ativo and fp.fotos_ok >= 5 and fp.tem_preco)
    into v_ativos, v_publicaveis
  from (
    select p.ativo,
           (select count(*)
              from jsonb_array_elements_text(coalesce(p.dados_normalizados->'fotos','[]'::jsonb)) f
             where f ~* '^https?://.+\.(jpe?g|png|webp)(\?|$)') as fotos_ok,
           (coalesce((p.dados_normalizados->>'valor_venda')::numeric,0) > 0
            or coalesce((p.dados_normalizados->>'valor_locacao')::numeric,0) > 0) as tem_preco
      from feed_properties p
  ) fp;

  -- invariante: ativo no Vista => publicado no XML
  select count(*) into v_divergentes
  from feed_properties fp
  join vista_imoveis_log v
    on v.codigo_vista = fp.codigo_original and v.ativo_vista is true
  where fp.ativo is false;

  with divergentes as (
    select fp.codigo_original, fp.dados_normalizados->>'cidade' as cidade
    from feed_properties fp
    join vista_imoveis_log v
      on v.codigo_vista = fp.codigo_original and v.ativo_vista is true
    where fp.ativo is false
  ), novos as (
    insert into vista_alertas (codigo_vista, tipo, dados)
    select d.codigo_original, 'feed_anuncio_fora_do_ar',
           jsonb_build_object('cidade', d.cidade, 'detectado_em', now())
    from divergentes d
    where not exists (
      select 1 from vista_alertas a
      where a.codigo_vista = d.codigo_original
        and a.tipo = 'feed_anuncio_fora_do_ar'
        and a.created_at > now() - interval '24 hours'
    )
    returning 1
  )
  select count(*) into v_novos_alertas from novos;

  select s.publicaveis into v_ontem
  from feed_acervo_snapshot s where s.dia < current_date
  order by s.dia desc limit 1;

  if v_ontem is not null and v_ontem > 0 then
    v_queda_pct := round(((v_ontem - v_publicaveis)::numeric / v_ontem) * 100, 2);
  end if;

  insert into feed_acervo_snapshot (dia, ativos, publicaveis, divergentes, queda_pct)
  values (current_date, v_ativos, v_publicaveis, v_divergentes, v_queda_pct)
  on conflict (dia) do update
    set ativos=excluded.ativos, publicaveis=excluded.publicaveis,
        divergentes=excluded.divergentes, queda_pct=excluded.queda_pct,
        atualizado_em=now();

  if v_queda_pct is not null and v_queda_pct >= 2 then
    raise warning '[vigia-acervo] queda de %%% no acervo publicavel: % -> %',
      v_queda_pct, v_ontem, v_publicaveis;
  end if;
  if v_divergentes > 0 then
    raise warning '[vigia-acervo] % anuncio(s) ativo(s) no Vista porem desligado(s) no feed', v_divergentes;
  end if;

  return jsonb_build_object('ativos',v_ativos,'publicaveis',v_publicaveis,
    'divergentes',v_divergentes,'queda_pct',v_queda_pct,'alertas_novos',v_novos_alertas);
end;
$$;

revoke all on function public.fn_vigia_acervo_feed() from public, anon, authenticated;

select cron.schedule('vigia-acervo-feed', '23 * * * *', 'select public.fn_vigia_acervo_feed();');
