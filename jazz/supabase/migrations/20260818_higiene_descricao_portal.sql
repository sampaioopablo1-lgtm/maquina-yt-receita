-- 18/08/2026 — Higiene das descrições publicadas nos portais.
--
-- O relatório de qualidade do portal deixa Descrição em 96% (25 pontos, 108
-- anúncios incompletos) com a instrução: "inclua palavras chaves e evite
-- informações como dados pessoais". A auditoria achou o que estava por trás:
--
--   1. PLACEHOLDER DE TEMPLATE NÃO PREENCHIDO — 4 anúncios no ar com o texto
--      literal do modelo: "[Inserir número de contato]" (39143), "[Seu
--      Telefone/Link]" (44413), "Valor de Locação: [Inserir Valor]" (37883)
--      e "[Valor]" (40274). Texto de IA colado sem revisão.
--
--   2. DADO PESSOAL EXPOSTO — 47159 traz "Contato: Fabi da Jazz -
--      19 99180.6378 / CRECI 180.666" dentro da descrição.
--
--   3. CHAMADA PARA CONTATO FORA DO PORTAL — 5 anúncios pedem contato por
--      WhatsApp. Portal trata como desvio de lead.
--
--   4. EMOJI CORROMPIDO — ~260 descrições com "?" solto onde havia emoji que
--      perdeu a codificação ("? AGENDE SUA VISITA", "24h ?").
--
-- Onde a correção mora: `feed_ai_content.descricao_otimizada` com
-- `ativo = true`. É o override que o gerador de XML já consulta (foi assim
-- que 42234, sem descrição nenhuma no Vista, saiu com texto completo no XML).
-- Mexer em `feed_properties.dados_normalizados` não adiantaria — o sync
-- reescreve aquele campo a cada 5 minutos.
--
-- Uma lição da primeira versão desta função, que ficou registrada aqui para
-- não se repetir: a regra original apagava a FRASE inteira que continha o
-- placeholder. Em texto sem ponto final — comum em anúncio que lista cômodos
-- separados por ponto e vírgula — isso engoliu parágrafos inteiros: o 40274
-- perdeu 285 caracteres, incluindo dormitórios, banheiros e vagas. Agora o
-- placeholder sai sozinho e a frase fica. Vírgula órfã é preferível a
-- informação real perdida. A regra de WhatsApp, que precisa remover a frase
-- toda (é chamada pura), ficou limitada a 200 caracteres pelo mesmo motivo.

create or replace function public.fn_higienizar_descricao(txt text)
returns text
language sql
immutable
as $$
  select nullif(btrim(
    regexp_replace(
    regexp_replace(
    regexp_replace(
    regexp_replace(
    regexp_replace(
    regexp_replace(
    regexp_replace(
      coalesce(txt,''),
      -- 1) só o placeholder sai; a frase fica
      '\[[^\]]{2,40}\]', '', 'g'),
      -- 2) linha com telefone e/ou CRECI
      '(?i)^.*(?:\(?\d{2}\)?[\s.-]?9?\d{4}[\s.-]?\d{4}|creci[\s:]*[\d.\-\/]+).*$', '', 'gm'),
      -- 3) chamada fora do portal, limitada a 200 chars de cada lado
      '(?i)[^.!?\n]{0,200}\y(?:whats\s?app|wpp)\y[^.!?\n]{0,200}[.!?]?', ' ', 'g'),
      -- 4) emoji corrompido: "?" após espaço ou início de linha. Interrogação
      --    de verdade cola na palavra ("quer visitar?"), então não é tocada.
      '(^|[[:space:]])\?+', '\1', 'g'),
      -- 5) pontuação órfã deixada pela remoção
      '([:,])\s*([.,;)])', '\2', 'g'),
      '[ \t]{2,}', ' ', 'g'),
      '(\r?\n[ \t]*){3,}', E'\n\n', 'g')
  ), '');
$$;

-- Aplica a higiene gravando no override que o gerador já lê. Só grava quando
-- a limpeza mudou algo E o resultado continua com corpo (>= 400 caracteres)
-- — nunca troca um texto ruim por um texto vazio.
create or replace function public.fn_aplicar_higiene_descricao(p_lote int default 500)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_criados int := 0;
  v_ignorados_curtos int := 0;
begin
  with alvo as (
    select fp.id, fp.codigo_original,
           fp.dados_normalizados->>'descricao' as original,
           public.fn_higienizar_descricao(fp.dados_normalizados->>'descricao') as limpa
    from public.feed_properties fp
    where fp.ativo
      and coalesce(fp.dados_normalizados->>'descricao','') <> ''
      and not exists (select 1 from public.feed_ai_content a
                       where a.property_id = fp.id and a.ativo)
    limit greatest(1, p_lote)
  ), mudou as (
    select * from alvo where limpa is distinct from original
  ), boas as (
    select * from mudou where length(limpa) >= 400
  ), gravados as (
    insert into public.feed_ai_content
      (property_id, versao, estrategia, descricao_original, descricao_otimizada, ativo, modelo)
    select id, 1, 'higiene_portal', original, limpa, true, 'regra_sql'
    from boas
    on conflict (property_id) where ativo do nothing
    returning 1
  )
  select (select count(*) from gravados),
         (select count(*) from mudou) - (select count(*) from boas)
    into v_criados, v_ignorados_curtos;

  return jsonb_build_object('ok', true, 'higienizados', v_criados,
                            'ignorados_por_ficarem_curtos', v_ignorados_curtos);
end;
$$;

revoke all on function public.fn_aplicar_higiene_descricao(int) from public, anon, authenticated;

-- De hora em hora: pega o que o sync trouxe de novo.
select cron.schedule('feed-higiene-descricao', '27 * * * *',
  $$select public.fn_aplicar_higiene_descricao(500);$$);
