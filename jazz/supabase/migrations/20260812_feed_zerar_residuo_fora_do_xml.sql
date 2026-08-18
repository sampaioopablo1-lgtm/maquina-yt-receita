-- 12/08/2026 — reconstrução do acervo do feed a partir do zero.
--
-- Regra que passa a valer: no feed só existe quem o Vista exporta hoje no XML
-- de portais. Nada de acervo herdado — o feed carregava 4.354 linhas contra
-- 3.904 no XML, e essas 450 sobras eram o material de onde saíam os anúncios
-- fantasmas.
--
-- As linhas removidas vão pra `feed_properties_arquivo` junto com o conteúdo
-- de IA que tinham (54 dos 450 tinham descrição otimizada). Se o imóvel voltar
-- ao XML, o sync o reconstrói sozinho; o arquivo serve pra conferir o que
-- existia antes, não pra restaurar automaticamente.
--
-- Nenhuma das 450 estava ativa: a v15 da Edge Function já as havia desligado
-- no fechamento de ciclo, e a trava de publicação já as bloqueava antes disso.
-- Esta migração remove o resíduo, não corrige exposição.

create table if not exists public.feed_properties_arquivo (
  id uuid primary key,
  source_id uuid,
  codigo_original text,
  dados_normalizados jsonb,
  score int,
  score_sugestoes jsonb,
  ativo boolean,
  created_at timestamptz,
  updated_at timestamptz,
  ia_conteudo jsonb,
  arquivado_em timestamptz not null default now(),
  motivo text
);

insert into public.feed_properties_arquivo (
  id, source_id, codigo_original, dados_normalizados, score, score_sugestoes,
  ativo, created_at, updated_at, ia_conteudo, motivo)
select fp.id, fp.source_id, fp.codigo_original, fp.dados_normalizados, fp.score,
       to_jsonb(fp.score_sugestoes), fp.ativo, fp.created_at, fp.updated_at,
       (select jsonb_agg(to_jsonb(a)) from public.feed_ai_content a where a.property_id = fp.id),
       'ausente_xml_vista'
from public.feed_properties fp
where fp.codigo_original not in (
  select codigo from public.feed_vista_xml_snapshot where visto_em >= now() - interval '2 hours')
on conflict (id) do nothing;

-- feed_ai_content, feed_performance e feed_property_portal_publicacao caem
-- por cascade — daí o arquivo guardar o conteúdo de IA antes do delete.
delete from public.feed_properties fp
where fp.codigo_original not in (
  select codigo from public.feed_vista_xml_snapshot where visto_em >= now() - interval '2 hours');
