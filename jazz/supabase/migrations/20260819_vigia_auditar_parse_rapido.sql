-- 19/08/2026 — Vigia do XML: parse rápido e sem falso alarme de omissão.
--
-- Dois defeitos apareceram na primeira hora de operação depois do incidente:
--
-- 1. A auditoria horária passou a FALHAR por estouro do limite de 120 s. O
--    `regexp_matches(conteudo, '<ListingID>([^<]+)</ListingID>', 'g')`
--    percorre 28 MB com retrocesso e materializa 2.949 casamentos — caro
--    demais depois que o feed cresceu. Trocado por uma passada única:
--    quebra o texto em '<ListingID>' e corta cada pedaço no fechamento.
--    Mesmo resultado, sem regex. A função também passa a definir seu próprio
--    limite de 110 s, em vez de depender do padrão global.
--
-- 2. Ela acusava como "faltando no XML" um imóvel que apenas tinha entrado
--    no acervo DEPOIS da última geração (o 47149 entrou 11:30, o XML era das
--    11:04). Isso é o ciclo seguinte, não omissão. Agora só é apontado como
--    faltante o imóvel que já existia quando o XML foi gerado.
--
-- Resultado da primeira execução corrigida: 2.949 anúncios, zero duplicados,
-- zero inativos, zero dado pessoal.

create or replace function public.fn_vigia_feed_auditar()
returns jsonb language plpgsql security definer set search_path = public as $$
declare
  v_run_id bigint; v_conteudo text; v_result jsonb; v_ajustados int := 0; v_xml_em timestamptz;
begin
  perform set_config('statement_timeout', '110s', true);

  select v.id, r.content into v_run_id, v_conteudo
    from vigia_feed_runs v
    join net._http_response r on r.id = (substring(v.detalhe from '^req ([0-9]+)'))::bigint
   where v.status_code = 200 and v.problemas is null
     and abs(length(r.content) - v.bytes) < v.bytes / 20
   order by v.executado_em desc limit 1;

  if v_conteudo is null then
    return jsonb_build_object('ok', true, 'auditadas', 0,
      'motivo', 'nenhuma rodada pendente com resposta integra disponivel');
  end if;

  select updated_at into v_xml_em from storage.objects where bucket_id='feeds-precomputados' limit 1;

  create temp table _codigos_xml on commit drop as
    select split_part(p, '</ListingID>', 1) as codigo, count(*) as vezes
    from unnest(string_to_array(v_conteudo, '<ListingID>')) with ordinality t(p, i)
    where i > 1 group by 1;

  with
  duplicados as (select array_agg(codigo order by codigo) arr from _codigos_xml where vezes > 1),
  inativos as (
    select array_agg(x.codigo order by x.codigo) arr
    from _codigos_xml x
    join public.vista_imoveis_log v on v.codigo_vista = x.codigo
    left join public.feed_properties fp on fp.codigo_original = x.codigo
    left join public.feed_property_portal_publicacao p on p.property_id = fp.id and p.portal = 'vrsync_rede'
    where not v.ativo_vista or v.vendido_em is not null
       or (p.property_id is not null and not p.habilitado)
  ),
  faltando as (
    select array_agg(fp.codigo_original order by fp.codigo_original) arr
    from public.feed_properties fp
    left join public.feed_property_portal_publicacao p on p.property_id = fp.id and p.portal = 'vrsync_rede'
    where fp.ativo and coalesce(p.habilitado, true)
      and jsonb_array_length(coalesce(fp.dados_normalizados->'fotos','[]'::jsonb)) >= 5
      -- imóvel alterado DEPOIS da geração ainda não teve chance de entrar:
      -- não é omissão, é o ciclo seguinte
      and (v_xml_em is null or fp.updated_at < v_xml_em)
      and not exists (select 1 from _codigos_xml x where x.codigo = fp.codigo_original)
  )
  select jsonb_build_object(
    'listings', (select count(*) from _codigos_xml),
    'duplicados', coalesce((select arr from duplicados), '{}'),
    'inativos_no_xml', coalesce((select arr from inativos), '{}'),
    'faltando_no_xml', coalesce((select arr from faltando), '{}'),
    'placeholder', v_conteudo ~ '\[Inserir' or v_conteudo ~* '\[seu telefone' or v_conteudo ~ '\[Valor\]',
    'creci_exposto', v_conteudo ~* 'creci[ :]*[0-9]{3}',
    'telefone_exposto', v_conteudo ~ '\(1[0-9]\)[ ]?9[0-9]{4}[-. ][0-9]{4}',
    'acima_do_teto', (select count(*) from _codigos_xml) > 3000
  ) into v_result;

  if (v_result->>'listings')::int < 100 then
    v_result := v_result || jsonb_build_object('ajuste_suspenso','xml com menos de 100 listings — provavel arquivo quebrado');
    update vigia_feed_runs set problemas = v_result where id = v_run_id;
    return jsonb_build_object('ok', false, 'run', v_run_id) || v_result;
  end if;

  update public.feed_property_portal_publicacao p
     set habilitado = false, motivo = 'vigia:inativo_no_xml', atualizado_em = now()
    from public.feed_properties fp, public.vista_imoveis_log v
   where p.property_id = fp.id and p.portal = 'vrsync_rede' and p.habilitado
     and fp.codigo_original = v.codigo_vista
     and fp.codigo_original in (select codigo from _codigos_xml)
     and (not v.ativo_vista or v.vendido_em is not null);
  get diagnostics v_ajustados = row_count;

  v_result := v_result || jsonb_build_object('inativos_desabilitados_agora', v_ajustados);
  update vigia_feed_runs set problemas = v_result where id = v_run_id;
  return jsonb_build_object('ok', true, 'run', v_run_id) || v_result;
end; $$;

revoke all on function public.fn_vigia_feed_auditar() from public, anon, authenticated;
