-- 18/08/2026 — Vigia do XML vira auditor de conteúdo, de hora em hora.
--
-- O vigia existente (fn_vigia_feed + fn_vigia_feed_coletar) só conferia se o
-- XML precomputado respondia 200 e quantos bytes tinha. O usuário pediu mais:
-- "verifique erros de imóveis duplicados, inativos, dentre outros problemas
-- que estejam no XML novo (...) já ajuste".
--
-- A auditoria roda em cima da MESMA resposta que o vigia já baixa (nada de
-- segunda requisição de 28MB):
--
--   1. DUPLICADO   — <ListingID> repetido dentro do XML;
--   2. INATIVO     — código emitido cujo espelho diz inativo, vendido ou
--                    bloqueado por webhook de baixa do Vista;
--   3. FALTANDO    — imóvel ativo e habilitado que sumiu do XML;
--   4. DADO SUJO   — placeholder de template, CRECI ou telefone no texto;
--   5. TETO        — mais listings que o teto contratado (3.000).
--
-- AJUSTE AUTOMÁTICO (o "já ajuste"): inativo emitido no XML é desabilitado
-- na hora em feed_property_portal_publicacao (motivo 'vigia:inativo_no_xml'),
-- o que o tira do próximo precompute sem esperar ninguém. Duplicado e
-- faltando não têm ajuste seguro automático — ficam registrados com os
-- códigos para investigação.
--
-- Duas cicatrizes da primeira rodada, gravadas nas regras:
--   - o join por LIKE ('req 6%') casou a rodada com a resposta errada (id 6
--    em vez de 62) e a auditoria saiu sobre conteúdo que não era o XML,
--    acusando "0 listings, todos faltando". Agora o id é extraído por regex
--    e comparado por igualdade, o tamanho precisa bater com o registrado, e
--    XML com menos de 100 listings suspende o ajuste automático;
--   - o padrão '\[Seu ' casou com 'CDATA[Seu sonho...' (o '[' era da
--    abertura do CDATA) e deu falso positivo de placeholder. Os padrões
--    agora são os tokens exatos dos templates já vistos no acervo.

alter table public.vigia_feed_runs add column if not exists problemas jsonb;

create or replace function public.fn_vigia_feed_auditar()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_run_id bigint;
  v_conteudo text;
  v_result jsonb;
  v_ajustados int := 0;
begin
  select v.id, r.content into v_run_id, v_conteudo
    from vigia_feed_runs v
    join net._http_response r
      on r.id = (substring(v.detalhe from '^req ([0-9]+)'))::bigint
   where v.status_code = 200 and v.problemas is null
     and abs(length(r.content) - v.bytes) < v.bytes / 20
   order by v.executado_em desc limit 1;

  if v_conteudo is null then
    return jsonb_build_object('ok', true, 'auditadas', 0,
      'motivo', 'nenhuma rodada pendente com resposta integra disponivel');
  end if;

  create temp table _codigos_xml on commit drop as
    select m[1] as codigo, count(*) as vezes
    from regexp_matches(v_conteudo, '<ListingID>([^<]+)</ListingID>', 'g') m
    group by 1;

  with
  duplicados as (
    select array_agg(codigo order by codigo) arr from _codigos_xml where vezes > 1
  ),
  inativos as (
    select array_agg(x.codigo order by x.codigo) arr
    from _codigos_xml x
    join public.vista_imoveis_log v on v.codigo_vista = x.codigo
    left join public.feed_properties fp on fp.codigo_original = x.codigo
    left join public.feed_property_portal_publicacao p
           on p.property_id = fp.id and p.portal = 'vrsync_rede'
    where not v.ativo_vista or v.vendido_em is not null
       or (p.property_id is not null and not p.habilitado)
  ),
  faltando as (
    select array_agg(fp.codigo_original order by fp.codigo_original) arr
    from public.feed_properties fp
    left join public.feed_property_portal_publicacao p
           on p.property_id = fp.id and p.portal = 'vrsync_rede'
    where fp.ativo and coalesce(p.habilitado, true)
      and jsonb_array_length(coalesce(fp.dados_normalizados->'fotos','[]'::jsonb)) >= 5
      and not exists (select 1 from _codigos_xml x where x.codigo = fp.codigo_original)
  )
  select jsonb_build_object(
    'listings',        (select count(*) from _codigos_xml),
    'duplicados',      coalesce((select arr from duplicados), '{}'),
    'inativos_no_xml', coalesce((select arr from inativos), '{}'),
    'faltando_no_xml', coalesce((select arr from faltando), '{}'),
    'placeholder',     v_conteudo ~ '\[Inserir' or v_conteudo ~* '\[seu telefone' or v_conteudo ~ '\[Valor\]',
    'creci_exposto',   v_conteudo ~* 'creci[ :]*[0-9]{3}',
    'telefone_exposto', v_conteudo ~ '\(1[0-9]\)[ ]?9[0-9]{4}[-. ][0-9]{4}',
    'acima_do_teto',   (select count(*) from _codigos_xml) > 3000
  ) into v_result;

  -- Trava de sanidade: XML aparentemente quebrado não dispara ajuste — só
  -- registro. Auditoria sobre arquivo mutilado já causou falso positivo.
  if (v_result->>'listings')::int < 100 then
    v_result := v_result || jsonb_build_object(
      'ajuste_suspenso', 'xml com menos de 100 listings — provavel arquivo quebrado');
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
end;
$$;

revoke all on function public.fn_vigia_feed_auditar() from public, anon, authenticated;

-- Vigia de hora em hora; o auditor fecha o ciclo minutos depois da coleta.
select cron.unschedule('vigia-feed-interno')
 where exists (select 1 from cron.job where jobname='vigia-feed-interno');
select cron.schedule('vigia-feed-interno', '3 * * * *', $$select public.fn_vigia_feed();$$);
select cron.schedule('vigia-feed-auditar', '11 * * * *', $$select public.fn_vigia_feed_auditar();$$);

-- Visão para acompanhar sem precisar de SQL.
create or replace view public.v_vigia_feed_ultimas as
select executado_em, status_code, bytes,
       problemas->>'listings' listings,
       problemas->'duplicados' duplicados,
       problemas->'inativos_no_xml' inativos_no_xml,
       problemas->'faltando_no_xml' faltando_no_xml,
       problemas->>'inativos_desabilitados_agora' ajustados,
       problemas->>'placeholder' placeholder,
       problemas->>'creci_exposto' creci,
       problemas->>'telefone_exposto' telefone
from public.vigia_feed_runs
where problemas is not null
order by executado_em desc limit 48;

grant select on public.v_vigia_feed_ultimas to authenticated;
