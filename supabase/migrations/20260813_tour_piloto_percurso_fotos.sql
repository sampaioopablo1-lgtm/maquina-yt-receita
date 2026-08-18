-- 13/08/2026 — piloto de tour virtual, depois de achar a regra real do portal.
--
-- A conclusão anterior estava errada, e vale registrar o erro. Quando a v7
-- pontuou 0% na categoria Tour, eu conclui que o portal recusava página
-- própria e passei a recomendar provedor externo. Duas verificações mostraram
-- que a causa era outra:
--
--   1) A página da v7 respondia 200 e existia — não era link quebrado.
--   2) A documentação oficial do Grupo OLX
--      (developers.grupozap.com/feeds/vrsync/elements/listing.html) lista três
--      exigências para `VirtualTourLink`, e nenhuma é provedor:
--        - a página contenha APENAS o conteúdo do tour virtual;
--        - a página não seja um link encurtado;
--        - a página esteja em https com certificado válido.
--
-- A página da v7 trazia título, cabeçalho e navegação em volta da galeria.
-- Violava a primeira exigência — que é objetiva e verificável, não uma
-- preferência do avaliador.
--
-- A Edge Function `tour` foi reescrita para conter só o visualizador: sem h1,
-- nav, header ou footer, HTTPS do próprio Supabase, URL direta.
--
-- O que este tour é, dito sem eufemismo: percurso em tela cheia pelas fotos
-- reais do imóvel. NÃO é panorâmica 360. O acervo não tem nenhuma — medição de
-- 13/08 sobre 241 fotos amostradas achou zero equirretangulares; a única em
-- proporção 2:1 tinha 640×317 px, que é recorte widescreen e não esfera.
-- Se um dia houver captura 360 de verdade, `tour_360` do Vista tem prioridade
-- na emissão e esta página sai de cena sozinha.
--
-- Piloto em 200 anúncios, não nos 2.996, porque a hipótese ainda não foi
-- confirmada pelo avaliador do portal. Se a categoria sair de 0%, escala; se
-- continuar em 0%, o campo volta a ficar vazio e fica provado que o portal
-- exige panorâmica — aí o caminho é captação 360 mesmo.

update public.feed_properties fp
   set dados_normalizados = fp.dados_normalizados
         || jsonb_build_object('tour_virtual',
              'https://cscczluzpblzhvojxanp.supabase.co/functions/v1/tour/' || fp.codigo_original,
              'tour_origem','piloto_percurso_fotos'),
       updated_at = now()
from (
  select fp2.id
  from public.feed_properties fp2
  left join public.feed_property_portal_publicacao p
    on p.property_id = fp2.id and p.portal = 'vrsync_rede'
  where fp2.ativo and coalesce(p.habilitado, true)
    and coalesce(fp2.dados_normalizados->>'tour_virtual','') = ''
  order by (select count(*) from jsonb_array_elements_text(coalesce(fp2.dados_normalizados->'fotos','[]'::jsonb)) f
             where f ~* '^https?://.+\.(jpe?g|png|webp)(\?|$)') desc,
           fp2.codigo_original
  limit 200
) a
where a.id = fp.id;

-- Para desfazer o piloto:
--   update public.feed_properties
--      set dados_normalizados = dados_normalizados - 'tour_virtual' - 'tour_origem'
--    where dados_normalizados->>'tour_origem' = 'piloto_percurso_fotos';
