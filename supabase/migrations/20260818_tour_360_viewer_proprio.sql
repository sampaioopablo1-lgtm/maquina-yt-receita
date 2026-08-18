-- 18/08/2026 — Tour 360 hospedado por nós. Sem fornecedor, sem mensalidade.
--
-- O VirtualTourEasy só libera a API no plano Professional, que não vamos
-- contratar. A dependência era desnecessária: já temos bucket público, Edge
-- Functions e domínio HTTPS válido. O visualizador virou a Edge Function
-- `tour360`, que serve Pannellum (MIT, 21KB, tour multi-ambiente nativo).
-- Custo: zero. Volume: ilimitado. Testado com panorama equiretangular real:
-- HTTP 200 e HTML válido.
--
-- O que NÃO mudou, e não muda: só entra panorama equiretangular capturado no
-- imóvel. Sem panorama real a função devolve 404 e nenhum link vai ao XML —
-- link de tour que não abre tour é pior que link nenhum.

-- Passa a publicar a nossa própria URL. O campo mls_viewer_url continua na
-- tabela para não perder o histórico de quem chegou a ser publicado lá, mas
-- deixa de ser a fonte do link.
create or replace function public.fn_tour_360_publicar_no_feed()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_n int := 0;
  v_base text := 'https://cscczluzpblzhvojxanp.supabase.co/functions/v1/tour360/';
begin
  update public.vista_imoveis_log v
     set tour_360 = v_base || t.codigo_vista
    from public.feed_tour_360 t
   where t.codigo_vista = v.codigo_vista
     and t.status in ('pendente','publicado')
     and jsonb_array_length(coalesce(t.panoramas,'[]'::jsonb)) > 0
     and v.ativo_vista
     and coalesce(v.tour_360,'') is distinct from (v_base || t.codigo_vista)
     -- nunca sobrescreve tour de terceiro; só preenche vazio ou substitui a
     -- página de fotos do piloto, que aponta para o nosso próprio domínio
     and (coalesce(v.tour_360,'') = ''
          or v.tour_360 like '%supabase.co/functions/v1/tour/%');
  get diagnostics v_n = row_count;
  return jsonb_build_object('ok', true, 'publicados_no_feed', v_n);
end;
$$;

revoke all on function public.fn_tour_360_publicar_no_feed() from public, anon, authenticated;

-- Limpa a linha de teste usada para validar o visualizador.
delete from public.feed_tour_360 where codigo_vista = 'TESTE-360';
