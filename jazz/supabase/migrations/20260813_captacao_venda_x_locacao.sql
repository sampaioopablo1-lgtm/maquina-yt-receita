-- 13/08/2026 — Achado ao avaliar o fluxo (pedido do usuário: "Aproveito para
-- avaliar o fluxo, banco de todos os pontos que precisam da API"): a fila de
-- captação processava 118 solicitações e travava quase todas em "sem
-- prospect na cidade" mesmo depois do estoque saltar de 63 para 198
-- particulares. Causa: TODO o estoque foi coletado com businessType=SALE —
-- a varredura nunca ligou um cursor de locação — e boa parte da fila
-- pendente é Locação (69 das 74 de São José dos Campos). Comparar preço de
-- venda (centenas de milhares) contra aluguel pedido (R$ 1.600–2.400/mês)
-- nunca ia casar; a regra de tentativas<5 esgotou 105 das 118 solicitações
-- tentando algo estruturalmente impossível.
--
-- Correção: `captacao_prospects` passa a guardar `tipo_operacao` (sale/rent)
-- desde a extração, e o casamento da fila passa a exigir o mesmo tipo do
-- pedido. A varredura automática (quando "sem prospect") agora liga o
-- business_type certo — RENTAL para Locação, SALE para Venda — em vez de
-- sempre SALE.

alter table public.captacao_prospects
  add column if not exists tipo_operacao text check (tipo_operacao in ('sale','rent'));

-- Backfill do que já foi coletado: até aqui só existiam cursores SALE, então
-- é seguro (e verificado acima) marcar tudo como 'sale'.
update public.captacao_prospects set tipo_operacao = 'sale' where tipo_operacao is null;

create index if not exists captacao_prospects_tipo_operacao_idx on public.captacao_prospects (tipo_operacao);

-- Liga cursores de locação nas mesmas cidades/portais que já têm venda —
-- sem isso a fila de aluguel nunca teria de onde puxar.
insert into public.captacao_varredura (cidade, uf, business_type, target, ativa, proxima_pagina, paginas_lidas)
select cidade, uf, 'RENTAL', target, true, 1, 0
from public.captacao_varredura
where business_type = 'SALE' and ativa
on conflict (cidade, uf, business_type, target) do nothing;

create or replace function public.fn_captacao_processar_fila(
  p_lote int default 50, p_score_min numeric default 85, p_min_boas int default 3
)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_processadas int := 0;
  v_ja_cobertas int := 0;
  v_com_api int := 0;
  v_sem_material int := 0;
  r record;
  v_boas int;
  v_criadas int;
  v_tipo_op text;
  v_bt_varredura text;
begin
  for r in
    select f.solicitacao_id, s.cidade, s.valor_min, s.valor_max, s.tipo_operacao
    from public.captacao_fila_solicitacoes f
    join public.solicitacoes s on s.id = f.solicitacao_id
    where f.processado_em is null and f.tentativas < 5
    order by f.enfileirado_em
    limit greatest(1, p_lote)
  loop
    v_processadas := v_processadas + 1;

    -- Venda casa com prospect de venda, Locação com prospect de locação.
    -- Pedido sem tipo definido (raro) não filtra por tipo — melhor sugerir
    -- algo pra conferir na ligação do que travar por falta de dado.
    v_tipo_op := case when lower(coalesce(r.tipo_operacao,'')) like 'loca%' or lower(coalesce(r.tipo_operacao,'')) like 'alug%'
                       then 'rent' else 'sale' end;
    v_bt_varredura := case when v_tipo_op = 'rent' then 'RENTAL' else 'SALE' end;

    select count(*) into v_boas
    from public.solicitacao_sugestoes ss
    where ss.solicitacao_id = r.solicitacao_id and ss.status = 'sugerido' and ss.score >= p_score_min;

    if v_boas >= p_min_boas then
      update public.captacao_fila_solicitacoes
         set processado_em = now(), resultado = format('base já cobre (%s sugestões >= %s)', v_boas, p_score_min)
       where solicitacao_id = r.solicitacao_id;
      v_ja_cobertas := v_ja_cobertas + 1;
      continue;
    end if;

    -- Base fraca: puxa do que a API já coletou para a cidade, no mesmo tipo
    -- de operação (venda ou locação) e em qualquer portal.
    with pares as (
      select p.id as prospect_id, p.perfil, p.fonte,
             row_number() over (order by (p.perfil='particular') desc,
               abs(coalesce(p.preco,0) - ((coalesce(r.valor_min,0) + coalesce(r.valor_max, coalesce(r.valor_min,0)*2))/2.0)),
               p.coletado_em desc) as rn
      from public.captacao_prospects p
      where public.fn_norm_cidade(p.cidade) = public.fn_norm_cidade(r.cidade)
        and p.telefone is not null
        and p.perfil in ('particular','indefinido')
        and coalesce(p.tipo_operacao, 'sale') = v_tipo_op
        and (r.valor_min is null or p.preco is null or p.preco >= r.valor_min * 0.9)
        and (r.valor_max is null or p.preco is null or p.preco <= r.valor_max * 1.1)
        and not exists (select 1 from public.solicitacao_sugestoes_externas x
                         where x.solicitacao_id = r.solicitacao_id and x.prospect_id = p.id)
    ), gravados as (
      insert into public.solicitacao_sugestoes_externas (solicitacao_id, prospect_id, score, motivo)
      select r.solicitacao_id, prospect_id,
             case when perfil='particular' then 90 else 60 end,
             case when perfil='particular'
                  then format('anúncio de particular em %s — captação sob demanda', fonte)
                  else format('anunciante não identificado em %s — confirmar na ligação', fonte) end
      from pares where rn <= 6
      on conflict (solicitacao_id, prospect_id) do nothing
      returning 1
    )
    select count(*) into v_criadas from gravados;

    if v_criadas > 0 then
      update public.captacao_fila_solicitacoes
         set processado_em = now(), resultado = format('%s sugestões da API', v_criadas)
       where solicitacao_id = r.solicitacao_id;
      v_com_api := v_com_api + 1;
    else
      -- Sem prospect no tipo certo pra cidade: liga a varredura nos três
      -- portais, no business_type que o pedido precisa, e tenta de novo depois.
      insert into public.captacao_varredura (cidade, uf, business_type, target, ativa)
      values
        (coalesce(r.cidade,'São José dos Campos'), 'SP', v_bt_varredura, 'zapimoveis.com.br', true),
        (coalesce(r.cidade,'São José dos Campos'), 'SP', v_bt_varredura, 'vivareal.com.br', true),
        (coalesce(r.cidade,'São José dos Campos'), 'SP', v_bt_varredura, 'chavesnamao.com.br', true)
      on conflict (cidade, uf, business_type, target) do update set ativa = true;

      update public.captacao_fila_solicitacoes
         set tentativas = tentativas + 1,
             resultado = format('sem prospect de %s na cidade — varredura acionada', v_tipo_op)
       where solicitacao_id = r.solicitacao_id;
      v_sem_material := v_sem_material + 1;
    end if;
  end loop;

  return jsonb_build_object('ok', true, 'processadas', v_processadas,
    'ja_cobertas_pela_base', v_ja_cobertas, 'atendidas_pela_api', v_com_api,
    'aguardando_varredura', v_sem_material);
end;
$$;

-- As 105 solicitações que esgotaram tentativa tentando casar com o tipo
-- errado de imóvel merecem nova chance agora que o filtro está correto.
update public.captacao_fila_solicitacoes set tentativas = 0 where processado_em is null;
