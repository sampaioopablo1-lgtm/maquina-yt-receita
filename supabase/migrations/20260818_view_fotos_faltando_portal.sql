-- 18/08/2026 — Lista de trabalho para a categoria Imagens do portal.
--
-- A categoria vale 20 pontos e está em 86% (414 anúncios incompletos), o que
-- custa 2,8 pontos da nota. Duas coisas foram medidas antes de criar isto:
--
--   1. O feed NÃO trunca fotos. Conferido no XML publicado: 94.584 tags de
--      imagem emitidas contra 94.584 fotos no banco. Emitimos tudo o que
--      temos, então não há nada a corrigir em código — as fotos precisam
--      existir no Vista.
--
--   2. A régua real do portal é 17 fotos, não 12 (nosso gate de emissão) nem
--      20 (o que o material de nota máxima sugere). Deduzido cruzando os 414
--      incompletos do relatório com a distribuição de fotos do acervo:
--      limiar 16 → 373 incompletos, limiar 17 → 474. O 414 cai entre os dois.
--
-- Esta view existe para transformar isso em trabalho de campo priorizado, em
-- vez de "adicionem fotos". A ordem importa: 204 anúncios precisam de apenas
-- 1 ou 2 fotos e resolvem 306 das 1.392 fotos faltantes — é o melhor retorno
-- por esforço da nota inteira.
--
-- Decisão consciente de NÃO fazer o atalho: subir o gate de emissão de 12
-- para 17 zeraria a categoria na hora (+2,8 pontos), mas tiraria 475
-- anúncios do ar — 16% do estoque publicado, sem nada para repor, já que os
-- bloqueados têm ainda menos fotos. Trocar 16% dos anúncios por 2,8 pontos é
-- mau negócio: anúncio no ar gera lead, nota não. Se algum dia essa troca
-- fizer sentido, é só mudar o parâmetro de `fn_gate_fotos_portal`.

create or replace view public.v_fotos_faltando_portal as
with publicados as (
  select fp.id, fp.codigo_original,
         jsonb_array_length(coalesce(fp.dados_normalizados->'fotos','[]'::jsonb)) as fotos
  from public.feed_properties fp
  left join public.feed_property_portal_publicacao p
    on p.property_id = fp.id and p.portal = 'vrsync_rede'
  where fp.ativo and coalesce(p.habilitado, true)
)
select pb.codigo_original as codigo_vista,
       pb.fotos as fotos_hoje,
       17 - pb.fotos as fotos_faltando,
       v.cidade, v.bairro, v.categoria,
       coalesce(v.valor_venda, v.valor_locacao) as valor,
       v.corretor_nome_vista as corretor,
       case when pb.fotos >= 15 then 'A - falta 1 ou 2'
            when pb.fotos >= 12 then 'B - falta 3 a 5'
            else 'C - falta 6+' end as prioridade
from publicados pb
left join public.vista_imoveis_log v on v.codigo_vista = pb.codigo_original
where pb.fotos < 17
order by pb.fotos desc, coalesce(v.valor_venda, v.valor_locacao) desc nulls last;

grant select on public.v_fotos_faltando_portal to authenticated;
