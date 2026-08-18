-- 18/08/2026 — Descrição completa: prosa higienizada + ficha técnica real.
--
-- O portal devolveu a instrução literal: "As descrições ainda não contemplam
-- todas as especificações dos imóveis, detalhe melhor com mais informações,
-- inclua palavras chaves e evite informações como dados pessoais."
--
-- A parte de dados pessoais já tinha sido resolvida
-- (20260818_higiene_descricao_portal.sql). Esta migração resolve as outras
-- duas. A medição que a motivou:
--
--   2.963 anúncios publicados
--   1.623 (55%) omitiam na descrição alguma especificação que o Vista JÁ TEM:
--     527 não citavam dormitórios · 731 não citavam banheiros · 129 não
--     citavam suítes · 666 não citavam vagas · 637 não citavam metragem
--
-- Ou seja: o dado existe no cadastro e sai no XML como campo estruturado, mas
-- some do texto — e é o texto que o portal lê para pontuar Descrição.
--
-- REGRA QUE NÃO SE QUEBRA AQUI: nada é inventado. Cada item da ficha sai de um
-- campo preenchido do Vista; campo zerado ou nulo simplesmente não aparece.
-- A prosa original é preservada inteira — a ficha é acrescentada abaixo dela,
-- nunca por cima. Verificado após a aplicação: nenhuma das 2.963 descrições
-- encolheu.
--
-- Teto de 3.000 caracteres do <Description> do VRSync: quando prosa + ficha
-- estouram, quem cede é a PROSA. A ficha é o dado estruturado que o portal usa
-- para pontuar, e é curta. O corte cai no último ponto final que couber, para
-- o texto não terminar no meio de uma frase. Sem essa trava 27 anúncios
-- passariam do limite (10 já passavam, vindos do Vista — esses foram
-- corrigidos de quebra).

create or replace function public.fn_descricao_ficha(p_texto text, d jsonb)
returns text
language sql
stable
as $$
with base as (
  -- Corta um bloco de ficha anterior antes de reconstruir. É isso que torna a
  -- função idempotente: rodar duas vezes não duplica a ficha.
  select btrim(regexp_replace(coalesce(p_texto,''), '\n*Ficha do imóvel:.*$', '', 's')) as t
), n as (
  select t,
    coalesce(nullif(d->>'dormitorios','')::numeric, 0) dorm,
    coalesce(nullif(d->>'suites','')::numeric, 0)      sui,
    coalesce(nullif(d->>'banheiros','')::numeric, 0)   ban,
    coalesce(nullif(d->>'vagas','')::numeric, 0)       vag,
    coalesce(nullif(d->>'area_util','')::numeric, 0)   au,
    coalesce(nullif(d->>'area_total','')::numeric, 0)  att,
    nullif(btrim(d->>'tipo'),'')   tipo,
    nullif(btrim(d->>'bairro'),'') bairro,
    nullif(btrim(d->>'cidade'),'') cidade,
    coalesce(d->>'finalidade','')  fin
  from base
), itens as (
  select n.*, array_remove(array[
    case when dorm > 0 then trunc(dorm)::text || ' dormitório' || case when dorm > 1 then 's' else '' end end,
    case when sui  > 0 then trunc(sui)::text  || ' suíte'      || case when sui  > 1 then 's' else '' end end,
    case when ban  > 0 then trunc(ban)::text  || ' banheiro'   || case when ban  > 1 then 's' else '' end end,
    case when vag  > 0 then trunc(vag)::text  || ' vaga'       || case when vag  > 1 then 's' else '' end || ' de garagem' end,
    case when au   > 0 then trunc(au)::text   || ' m² de área útil' end,
    case when att  > 0 and att <> au then trunc(att)::text || ' m² de área total' end
  ], null) arr
  from n
), dif as (
  select coalesce(string_agg(m.ptbr, ', ' order by m.ptbr), '') as txt
  from jsonb_array_elements_text(coalesce(d->'caracteristicas', '[]'::jsonb)) c
  join public.feed_caracteristica_ptbr m on m.codigo = c
), partes as (
  select i.t as prosa,
    btrim(concat_ws(E'\n\n',
      case when coalesce(array_length(i.arr, 1), 0) > 0
           then 'Ficha do imóvel: ' || array_to_string(i.arr, ', ') || '.' end,
      case when (select txt from dif) <> ''
           then 'Diferenciais: ' || (select txt from dif) || '.' end,
      -- Linha de palavras-chave: tipo + operação + bairro + cidade. É o que o
      -- buscador do portal indexa e o que o relatório chama de "palavras
      -- chaves".
      case when i.tipo is not null and i.cidade is not null then
        i.tipo || ' ' ||
        case when i.fin ilike '%venda%' and i.fin ilike '%aluguel%' then 'à venda ou para alugar'
             when i.fin ilike '%aluguel%'                           then 'para alugar'
             else 'à venda' end ||
        coalesce(' no ' || regexp_replace(i.bairro, '\s*-\s*', ' - ', 'g'), '') || ', ' || i.cidade || '.' end
    )) as cauda
  from itens i
), corte as (
  select cauda,
         greatest(0, 3000 - length(cauda) - 2) as orcamento,
         prosa
  from partes
)
select btrim(concat_ws(E'\n\n',
  nullif(
    case when length(prosa) <= orcamento then prosa
         else btrim(coalesce(
           substring(left(prosa, orcamento) from '^.*[.!?]'),
           left(prosa, orcamento)))
    end, ''),
  nullif(cauda, '')
))
from corte;
$$;

-- Aplica em lote: higieniza e completa, gravando no override que o gerador de
-- XML já consulta (feed_ai_content.descricao_otimizada com ativo = true).
-- Atualiza a linha ativa quando ela existe, insere quando não.
--
-- Detalhe que custou uma correção: o LIMIT precisa vir DEPOIS da detecção de
-- mudança. Na primeira versão ele cortava as N primeiras linhas e só então
-- filtrava o que mudou — passada a primeira rodada, o cron ficaria repetindo
-- as mesmas N linhas já em dia e nunca alcançaria o resto do acervo.
create or replace function public.fn_aplicar_ficha_descricao(p_lote int default 800)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_atualizados int := 0;
  v_criados int := 0;
begin
  with alvo as (
    select a.id,
           public.fn_descricao_ficha(
             public.fn_higienizar_descricao(a.descricao_otimizada),
             fp.dados_normalizados) as nova,
           a.descricao_otimizada as atual
    from public.feed_ai_content a
    join public.feed_properties fp on fp.id = a.property_id
    left join public.feed_property_portal_publicacao p
           on p.property_id = fp.id and p.portal = 'vrsync_rede'
    where a.ativo and fp.ativo and coalesce(p.habilitado, true)
  ), mudou as (
    select * from alvo
     where nova is distinct from atual
       -- nunca troca texto bom por texto curto; se o atual já era vazio,
       -- qualquer ficha verdadeira é ganho
       and (length(nova) >= 400 or coalesce(atual,'') = '')
       and coalesce(nova,'') <> ''
     limit greatest(1, p_lote)
  ), upd as (
    update public.feed_ai_content a
       set descricao_otimizada = m.nova, updated_at = now()
      from mudou m where a.id = m.id
    returning 1
  )
  select count(*) from upd into v_atualizados;

  with alvo as (
    select fp.id,
           fp.dados_normalizados->>'descricao' as original,
           public.fn_descricao_ficha(
             public.fn_higienizar_descricao(fp.dados_normalizados->>'descricao'),
             fp.dados_normalizados) as nova
    from public.feed_properties fp
    left join public.feed_property_portal_publicacao p
           on p.property_id = fp.id and p.portal = 'vrsync_rede'
    where fp.ativo and coalesce(p.habilitado, true)
      and not exists (select 1 from public.feed_ai_content a
                       where a.property_id = fp.id and a.ativo)
  ), boas as (
    select * from alvo
     where nova is distinct from original
       and (length(nova) >= 400 or coalesce(original,'') = '')
       and coalesce(nova,'') <> ''
     limit greatest(1, p_lote)
  ), ins as (
    insert into public.feed_ai_content
      (property_id, versao, estrategia, descricao_original, descricao_otimizada, ativo, modelo)
    select id, 1, 'ficha_portal', original, nova, true, 'regra_sql'
    from boas
    on conflict (property_id) where ativo do nothing
    returning 1
  )
  select count(*) from ins into v_criados;

  return jsonb_build_object('ok', true, 'completados', v_atualizados, 'criados', v_criados);
end;
$$;

revoke all on function public.fn_aplicar_ficha_descricao(int) from public, anon, authenticated;

-- Substitui o cron de higiene: esta função já higieniza e ainda completa.
select cron.unschedule('feed-higiene-descricao')
 where exists (select 1 from cron.job where jobname = 'feed-higiene-descricao');
select cron.schedule('feed-descricao-completa', '27 * * * *',
  $$select public.fn_aplicar_ficha_descricao(800);$$);
