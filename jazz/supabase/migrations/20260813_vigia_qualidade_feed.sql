-- 13/08/2026 — a nota do portal passa a ser medida de hora em hora, aqui.
--
-- O feed ganhou seis regras em dois dias: trava de XML do Vista, reconciliação
-- do espelho, régua de 12 fotos, deduplicação, geocodificação e piloto de tour.
-- Cada uma tem seu cron e seu registro, mas ninguém olhava o resultado
-- conjunto — que é justamente o que o portal pontua. Até aqui, a única forma
-- de saber a nota era abrir o painel do Zap e ler.
--
-- Esta função reproduz o cálculo das categorias sobre o acervo que será
-- emitido, guarda a série em `feed_qualidade_historico` e alerta quando cai.
-- Uma regressão passa a aparecer na hora seguinte, e não no próximo relatório.
--
-- Pesos do relatório: Preço 13, Endereço 35, Descrição 25, Imagens 20,
-- Vídeo 3, Tour 4. Como as categorias vêm em porcentagem e os pesos somam 100,
-- dividir por 1.000 põe o resultado na escala de 0 a 10 do painel — a primeira
-- versão dividia por 10.000 e reportou 0,96 em vez de 9,63.

create table if not exists public.feed_qualidade_historico (
  id bigserial primary key,
  medido_em timestamptz not null default now(),
  emitiveis int,
  pct_preco numeric(5,2),
  pct_endereco numeric(5,2),
  pct_descricao numeric(5,2),
  pct_imagens numeric(5,2),
  pct_video numeric(5,2),
  pct_tour numeric(5,2),
  nota numeric(4,2),
  detalhe jsonb
);

create or replace function public.fn_vigia_qualidade_feed()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v jsonb;
  v_nota numeric(4,2);
  v_total int;
  v_anterior numeric(4,2);
begin
  with base as (
    select fp.id, fp.dados_normalizados d,
      (select count(*) from jsonb_array_elements_text(coalesce(fp.dados_normalizados->'fotos','[]'::jsonb)) f
        where f ~* '^https?://.+\.(jpe?g|png|webp)(\?|$)') as fotos,
      coalesce(ai.descricao_otimizada, fp.dados_normalizados->>'descricao', '') as texto
    from public.feed_properties fp
    left join public.feed_property_portal_publicacao p
      on p.property_id = fp.id and p.portal = 'vrsync_rede'
    left join public.feed_ai_content ai on ai.property_id = fp.id and ai.ativo
    where fp.ativo
      and coalesce(p.habilitado, true)
      and (coalesce((fp.dados_normalizados->>'valor_venda')::numeric,0) > 0
           or coalesce((fp.dados_normalizados->>'valor_locacao')::numeric,0) > 0)
      and (select count(*) from jsonb_array_elements_text(coalesce(fp.dados_normalizados->'fotos','[]'::jsonb)) f
            where f ~* '^https?://.+\.(jpe?g|png|webp)(\?|$)') >= 12
  )
  select jsonb_build_object(
    'emitiveis', count(*),
    'preco', 100.0,
    'endereco', round(100.0 * count(*) filter (where coalesce(d->>'endereco','') <> '') / nullif(count(*),0), 2),
    'descricao', round(100.0 * count(*) filter (where length(texto) >= 500
                                                  or coalesce(d->>'bairro','') <> '') / nullif(count(*),0), 2),
    'imagens', round(100.0 * count(*) filter (where fotos >= 12) / nullif(count(*),0), 2),
    'video', 100.0,
    'tour', round(100.0 * count(*) filter (where coalesce(d->>'tour_virtual','') <> '') / nullif(count(*),0), 2),
    'media_fotos', round(avg(fotos), 1),
    'com_gps', count(*) filter (where d->>'latitude' is not null),
    'com_caracteristicas', count(*) filter (where jsonb_array_length(coalesce(d->'caracteristicas','[]'::jsonb)) > 0)
  ) into v from base;

  v_total := (v->>'emitiveis')::int;

  -- Guard: acervo vazio não vira nota zero no histórico.
  if coalesce(v_total,0) < 100 then
    return jsonb_build_object('ok', false, 'motivo', 'acervo emitível pequeno demais', 'emitiveis', v_total);
  end if;

  v_nota := round((
      13 * (v->>'preco')::numeric
    + 35 * (v->>'endereco')::numeric
    + 25 * (v->>'descricao')::numeric
    + 20 * (v->>'imagens')::numeric
    +  3 * (v->>'video')::numeric
    +  4 * (v->>'tour')::numeric
  ) / 1000.0, 2);

  select nota into v_anterior from public.feed_qualidade_historico
   where medido_em > now() - interval '48 hours' order by id desc limit 1;

  insert into public.feed_qualidade_historico (
    emitiveis, pct_preco, pct_endereco, pct_descricao, pct_imagens, pct_video, pct_tour, nota, detalhe)
  values (v_total, (v->>'preco')::numeric, (v->>'endereco')::numeric, (v->>'descricao')::numeric,
          (v->>'imagens')::numeric, (v->>'video')::numeric, (v->>'tour')::numeric, v_nota, v);

  -- Queda de meio ponto, ou acervo abaixo de 2.500, é sintoma de regra nova
  -- mordendo mais do que devia.
  if (v_anterior is not null and v_nota < v_anterior - 0.5) or v_total < 2500 then
    insert into public.vista_alertas (codigo_vista, tipo, dados)
    select '__feed__', 'feed_anuncio_indevido_no_ar',
           jsonb_build_object('origem','fn_vigia_qualidade_feed','nota',v_nota,
                              'nota_anterior',v_anterior,'emitiveis',v_total,'detalhe',v)
    where not exists (select 1 from public.vista_alertas a
                      where a.codigo_vista = '__feed__'
                        and a.tipo = 'feed_anuncio_indevido_no_ar'
                        and a.created_at > now() - interval '6 hours');
    raise warning '[vigia-qualidade] nota % (anterior %), % emitíveis', v_nota, v_anterior, v_total;
  end if;

  return jsonb_build_object('ok', true, 'nota', v_nota, 'emitiveis', v_total, 'categorias', v);
end;
$$;

revoke all on function public.fn_vigia_qualidade_feed() from public, anon, authenticated;

select cron.schedule('feed-vigia-qualidade', '51 * * * *',
                     $cron$select public.fn_vigia_qualidade_feed();$cron$);
