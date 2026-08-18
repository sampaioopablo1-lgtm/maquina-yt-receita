-- 13/08/2026 — Usuário viu sugestão de captação "Grupo Kaza Apolo 05" (e
-- dezenas de variantes numeradas: Kaza Jacareí NN, Kaza Satélite NN, Kaza
-- Aquarius NN — claramente uma rede/franquia, não pessoa física) marcada
-- como particular. Também "Grupo Intervale" (16 anúncios). Investigando:
-- bug de regex, não de classificação de negócio.
--
-- `fn_captacao_classificar()` usa `\b...\b` pra marcar palavra inteira
-- ("me", "mei", "epp", "spe", "cia", "grupo", "home", "homes", "house",
-- "prime", "elite", "vip", "master", "plan", "planej", "ventures", "corp",
-- "group"). Só que a engine de regex do Postgres (ARE, não PCRE) trata
-- `\b` como BACKSPACE, não fronteira de palavra — a fronteira certa é `\y`.
-- Confirmado: `'Grupo Kaza' ~ '(?i)\bgrupo\b'` → false; `~ '(?i)\ygrupo\y'`
-- → true. Nenhum desses termos com `\b` jamais excluiu nada desde que o
-- classificador foi escrito — passaram direto pro pool de "particular".
--
-- Fix: troca `\b` por `\y` em toda a regex de empresa. Reclassifica o
-- acervo inteiro e remove sugestões de captação já enviadas que eram, na
-- verdade, empresa sob a régua corrigida — pra não deixar rede de
-- revenda numerada sendo sugerida como proprietário particular.

create or replace function public.fn_captacao_classificar()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v jsonb;
  re_empresa text := '(?i)(ltda|s/?a\.?$|eireli|\yme\y|\ymei\y|\yepp\y|im[oó]v[eé]|imobili|corretor|corretag|'
                  || 'consultor|assessor|administrador|construtor|construç|incorporad|empreendim|urbanism|'
                  || 'loteador|realty|broker|invest|neg[oó]cio|patrim|holding|participa|\yspe\y|'
                  || 're/?max|century|coelho da fonseca|\ylopes\y|bossa|keller|engel|'
                  || 'imobili[aá]ria|\ygrupo\y|\ycia\y|& cia|assoc|servi[çc]os|solu[çc][oõ]es|'
                  || 'engenharia|arquitet|\yhome\y|\yhomes\y|\yhouse\y|\yprime\y|\yelite\y|\yvip\y|'
                  || '\ymaster\y|\yplan\y|\yplanej\y|\yventures?\y|\ycorp\y|\ygroup\y)';
  re_fone_falso text := '^\d{2}(\d)\1{7,}$';
begin
  update public.captacao_prospects p set
    perfil = case
      when p.telefone is null or p.telefone ~ re_fone_falso then 'descartar'
      when p.tem_creci then 'empresa'
      when coalesce(p.anunciante,'') ~ re_empresa then 'empresa'
      when array_length(regexp_split_to_array(btrim(coalesce(p.anunciante,'')), '\s+'), 1) >= 2 then 'particular'
      else 'indefinido'
    end,
    motivo_perfil = case
      when p.telefone is null or p.telefone ~ re_fone_falso then 'telefone ausente ou genérico'
      when p.tem_creci then 'CRECI informado no anúncio'
      when coalesce(p.anunciante,'') ~ re_empresa then 'nome com marca de empresa'
      when array_length(regexp_split_to_array(btrim(coalesce(p.anunciante,'')), '\s+'), 1) >= 2 then 'nome de pessoa, sem CRECI'
      else 'nome de uma palavra — não dá pra afirmar'
    end;

  select jsonb_build_object(
    'particular', count(*) filter (where perfil='particular'),
    'empresa', count(*) filter (where perfil='empresa'),
    'indefinido', count(*) filter (where perfil='indefinido'),
    'descartar', count(*) filter (where perfil='descartar')) into v
  from public.captacao_prospects;
  return v;
end;
$$;

select public.fn_captacao_classificar();

-- Remove sugestões de captação já enviadas cujo prospect virou "empresa"
-- sob a régua corrigida — reabre a solicitação pra ganhar sugestão de
-- verdade na próxima rodada do cron.
with tocadas as (
  delete from public.solicitacao_sugestoes_externas se
  using public.captacao_prospects p
  where se.prospect_id = p.id and p.perfil = 'empresa' and se.status = 'sugerido'
  returning se.solicitacao_id
)
update public.captacao_fila_solicitacoes f
set processado_em = null, tentativas = 0
from tocadas t
where f.solicitacao_id = t.solicitacao_id;
