-- 18/08/2026 — Publicação de tour/vídeo escreve nas DUAS camadas.
--
-- Diagnóstico (checagem de persistência do piloto 40346): o gerador de XML
-- lê feed_properties.dados_normalizados, e essa camada só reconstrói quando
-- o imóvel muda no Vista — o job de reprocesso geral (smart-feed-reprocessar)
-- está desativado. Escrever só em vista_imoveis_log deixava o link novo
-- esperando indefinidamente por uma mudança que talvez nunca viesse: 30 min
-- depois do rollout, o XML ainda emitia os 193 links antigos e zero /visita/.
--
-- Correção: as funções de publicação passam a gravar o mesmo valor nos dois
-- lugares — no espelho (fonte de reconstrução) e direto no JSON que o
-- gerador lê (efeito no próximo precompute, que roda de 10 em 10 min).
-- Verificado após aplicar: 3.474 tour_virtual atualizados na camada do feed,
-- zero slideshow antigo restante.

create or replace function public.fn_visita_publicar_no_feed()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_mirror int := 0;
  v_feed int := 0;
  v_base text := 'https://cscczluzpblzhvojxanp.supabase.co/functions/v1/visita/';
begin
  update public.vista_imoveis_log v
     set tour_360 = v_base || v.codigo_vista
    from public.feed_properties fp
   where fp.codigo_original = v.codigo_vista
     and fp.ativo
     and jsonb_array_length(coalesce(fp.dados_normalizados->'fotos','[]'::jsonb)) >= 5
     and v.ativo_vista
     and coalesce(v.tour_360,'') is distinct from (v_base || v.codigo_vista)
     and (coalesce(v.tour_360,'') = ''
          or v.tour_360 like '%supabase.co/functions/v1/tour/%');
  get diagnostics v_mirror = row_count;

  -- Alinha a camada que o gerador lê com o espelho. Cobre tour de terceiro,
  -- /tour360/ real e /visita/ — o espelho é a verdade única do campo.
  update public.feed_properties fp
     set dados_normalizados = jsonb_set(fp.dados_normalizados, '{tour_virtual}',
           coalesce(to_jsonb(nullif(v.tour_360,'')), 'null'::jsonb)),
         updated_at = now()
    from public.vista_imoveis_log v
   where v.codigo_vista = fp.codigo_original
     and fp.ativo
     and coalesce(fp.dados_normalizados->>'tour_virtual','') is distinct from coalesce(v.tour_360,'');
  get diagnostics v_feed = row_count;

  return jsonb_build_object('ok', true, 'espelho', v_mirror, 'camada_feed', v_feed);
end;
$$;

revoke all on function public.fn_visita_publicar_no_feed() from public, anon, authenticated;

create or replace function public.fn_video_imovel_publicar_no_feed()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_mirror int := 0;
  v_feed int := 0;
  v_institucional text := 'https://www.youtube.com/watch?v=DlYDTuoHf3k';
begin
  update public.vista_imoveis_log v
     set video = t.youtube_url
    from public.feed_video_imovel t
   where t.codigo_vista = v.codigo_vista
     and t.youtube_url ~* '^https://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[A-Za-z0-9_\-]{6,}'
     and v.ativo_vista
     and coalesce(v.video,'') is distinct from t.youtube_url
     and (coalesce(v.video,'') = '' or v.video = v_institucional);
  get diagnostics v_mirror = row_count;

  update public.feed_properties fp
     set dados_normalizados = jsonb_set(fp.dados_normalizados, '{video}', to_jsonb(v.video)),
         updated_at = now()
    from public.vista_imoveis_log v
    join public.feed_video_imovel t on t.codigo_vista = v.codigo_vista
   where v.codigo_vista = fp.codigo_original
     and fp.ativo and coalesce(v.video,'') <> ''
     and v.video = t.youtube_url
     and coalesce(fp.dados_normalizados->>'video','') is distinct from v.video;
  get diagnostics v_feed = row_count;

  update public.feed_video_imovel t
     set status = 'no_feed', publicado_em = now()
    from public.vista_imoveis_log v
   where v.codigo_vista = t.codigo_vista
     and v.video = t.youtube_url
     and t.status <> 'no_feed';

  return jsonb_build_object('ok', true, 'espelho', v_mirror, 'camada_feed', v_feed);
end;
$$;

revoke all on function public.fn_video_imovel_publicar_no_feed() from public, anon, authenticated;
