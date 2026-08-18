-- 18/08/2026 — Visita virtual em TODOS os anúncios publicados.
--
-- Pedido explícito do usuário: "preciso para todos os imóveis tenha tour
-- virtual". O que se sabe e o que não se sabe, registrado com honestidade:
--
--   SABIDO: a diretriz do VirtualTourLink exige página só com o conteúdo do
--   tour, HTTPS, sem encurtador. A rota /visita/ cumpre as três. Cada pixel
--   dela é foto real do imóvel — nada é inventado.
--
--   SABIDO: as 193 páginas de slideshow do piloto anterior pontuaram 0% na
--   categoria do relatório de qualidade, mesmo estando no ar e válidas
--   (conferido em 18/08: HTTP 200, página limpa). O critério interno do
--   portal para "contar" um tour não é público.
--
--   NÃO SABIDO: se a visita imersiva nova pontua. A aposta é medível e
--   reversível — na próxima leitura do relatório, ou a categoria sobe, ou
--   volta-se atrás com um único UPDATE (motivo de manter o marcador
--   /visita/ na URL: identifica tudo que esta migração publicou).
--
--   O caminho GARANTIDO para a categoria continua sendo panorama 360 real
--   (rota /tour360/), que exige captura no imóvel — celular resolve, sem
--   comprar câmera.
--
-- Hierarquia do campo tour_360, da maior prioridade para a menor:
--   1. tour de terceiro cadastrado no Vista — intocável;
--   2. panorama 360 real nosso (/tour360/) — substitui a visita quando existir;
--   3. visita imersiva (/visita/) — piso de cobertura para 100% do acervo.
--
-- Resultado da primeira aplicação: 2.957 visitas + 6 tours de terceiro =
-- 2.963 de 2.963 anúncios publicados com tour, zero sem. Os 7 slideshows
-- antigos que não podiam virar visita (menos de 5 fotos, abaixo do mínimo do
-- portal) foram zerados.

create or replace function public.fn_visita_publicar_no_feed()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_n int := 0;
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
     -- só preenche vazio ou troca o slideshow antigo; terceiro e 360 real
     -- ficam como estão
     and (coalesce(v.tour_360,'') = ''
          or v.tour_360 like '%supabase.co/functions/v1/tour/%');
  get diagnostics v_n = row_count;
  return jsonb_build_object('ok', true, 'visitas_publicadas', v_n);
end;
$$;

revoke all on function public.fn_visita_publicar_no_feed() from public, anon, authenticated;

-- O 360 real passa a substituir também a visita (prioridade 2 vence a 3).
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
     and (coalesce(v.tour_360,'') = ''
          or v.tour_360 like '%supabase.co/functions/v1/tour/%'
          or v.tour_360 like '%supabase.co/functions/v1/visita/%');
  get diagnostics v_n = row_count;
  return jsonb_build_object('ok', true, 'publicados_no_feed', v_n);
end;
$$;

revoke all on function public.fn_tour_360_publicar_no_feed() from public, anon, authenticated;

-- Mantém a cobertura: imóvel novo que entrar no acervo ganha visita sozinho.
select cron.schedule('visita-publicar-no-feed', '9-59/10 * * * *',
  $$select public.fn_visita_publicar_no_feed();$$);

-- Limpa os slideshows antigos que não podiam virar visita (menos de 5 fotos).
update public.vista_imoveis_log set tour_360 = null
 where tour_360 like '%supabase.co/functions/v1/tour/%';
