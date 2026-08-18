-- 18/08/2026 — Saneia os 6 "tours de terceiro" que eram cadastro errado.
--
-- A verificação final da rodada achou por que o XML emitia 2.957 tours e não
-- 2.963: os 6 restantes tinham no campo de tour do Vista um link de YouTube
-- (5 casos — vídeo não é tour, e o gerador os descarta do VirtualTourLink) ou
-- lixo literal ('&quot;', 1 caso). Nenhum provedor real de tour.
--
-- Correção: o link de YouTube migra para o campo de VÍDEO do mesmo imóvel
-- (onde é válido e vale mais que o institucional genérico), e os 6 passam a
-- emitir a visita imersiva no campo de tour, como todo o resto do acervo.
-- A guarda "nunca tocar tour de terceiro" segue valendo para provedores
-- reais (http, não-YouTube) — hoje, nenhum no acervo.
--
-- Depois de aplicar: 2.963 de 2.963 publicados com visita no campo de tour,
-- zero sem, e 97 anúncios com vídeo próprio (92 que já tinham + 5 migrados).

update public.vista_imoveis_log v
   set video = v.tour_360
 where v.ativo_vista
   and v.tour_360 ~* '^https://(www\.)?youtube\.com/(watch|shorts)'
   and (coalesce(v.video,'') = ''
        or v.video = 'https://www.youtube.com/watch?v=DlYDTuoHf3k');

update public.feed_properties fp
   set dados_normalizados = jsonb_set(fp.dados_normalizados, '{video}', to_jsonb(v.video)),
       updated_at = now()
  from public.vista_imoveis_log v
 where v.codigo_vista = fp.codigo_original and fp.ativo
   and v.tour_360 ~* '^https://(www\.)?youtube\.com/(watch|shorts)'
   and v.video = v.tour_360;

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
          or v.tour_360 like '%supabase.co/functions/v1/tour/%'
          -- vídeo não é tour: YouTube no campo de tour cede lugar à visita
          or v.tour_360 ~* '^https://(www\.)?youtube\.com/'
          -- lixo (não é URL https) também cede
          or v.tour_360 !~* '^https://');
  get diagnostics v_mirror = row_count;

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
