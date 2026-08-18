-- 18/08/2026 — Duas correções na trava de status por webhook do Vista.
--
-- 1) BUG (meu, introduzido na migração de 17/08): a função decidia olhando
--    apenas os eventos de BAIXA de cada imóvel, ignorando eventos de
--    reativação posteriores. Um imóvel que foi "Suspenso" em julho e voltou
--    como "Venda" em agosto continuava bloqueado — o evento novo nunca era
--    considerado porque o filtro de baixa acontecia ANTES de escolher o
--    evento mais recente.
--
--    Estrago medido: 11 anúncios válidos derrubados (46738, 46235, 44623,
--    45977, 42652, 41021, 44299, 36017, 46821, 46560, 46513) — todos com
--    ativo_vista = true e último evento Venda/Aluguel.
--
--    Correção: escolhe o evento mais recente de CADA código primeiro, e só
--    então decide. Último evento é baixa → bloqueia. Último evento é ativo →
--    religa (mas só o que esta regra desligou, mesmo critério da trava de
--    12/08: `motivo like 'baixa_vista:%'`, para nunca desfazer bloqueio
--    feito por pessoa ou por outra regra).
--
-- 2) 'Pendente' passa a contar como baixa, a pedido do usuário. Eu havia
--    deixado de fora por ser estado de transição; a decisão de negócio é
--    dele. Com o fix acima o risco cai bastante: se o imóvel sair de
--    Pendente e voltar para Venda/Aluguel, agora ele religa sozinho no
--    próximo ciclo, em vez de ficar preso.

insert into public.vista_status_baixa (status, motivo) values
  ('Pendente', 'pendente no Vista (decisão do usuário em 18/08)')
on conflict (status) do nothing;

create or replace function public.fn_processar_webhooks_status_vista(p_lote int default 2000)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_bloqueados int := 0;
  v_religados int := 0;
  v_marcados int := 0;
begin
  with pendentes as (
    -- Todo evento com status, processado ou não: o estado atual de um imóvel
    -- depende do histórico inteiro, não só do que ainda não foi lido.
    select w.id, w.payload->>'code' as codigo, w.payload->>'status' as status,
           w.recebido_em, w.processado
    from public.vista_webhooks_recebidos w
    where w.assinatura_ok
      and w.payload->>'code' is not null
      and w.payload->>'status' is not null
  ), estado_atual as (
    -- O evento mais recente de cada código manda. É isto que consertou o
    -- bug: filtrar por baixa aqui embaixo, e não antes da escolha.
    select distinct on (codigo) codigo, status
    from pendentes
    order by codigo, recebido_em desc
  ), bloqueio as (
    insert into public.feed_property_portal_publicacao (property_id, portal, habilitado, motivo, atualizado_em)
    select fp.id, 'vrsync_rede', false, 'baixa_vista:' || e.status, now()
    from estado_atual e
    join public.vista_status_baixa b on b.status = e.status
    join public.feed_properties fp on fp.codigo_original = e.codigo
    on conflict (property_id, portal) do update
      set habilitado = false,
          motivo = excluded.motivo,
          atualizado_em = now()
      where public.feed_property_portal_publicacao.habilitado
    returning 1
  ), religa as (
    -- Voltou ao mercado: religa só o que esta regra desligou.
    update public.feed_property_portal_publicacao p
       set habilitado = true, motivo = null, atualizado_em = now()
      from estado_atual e
      join public.feed_properties fp on fp.codigo_original = e.codigo
     where p.property_id = fp.id
       and p.portal = 'vrsync_rede'
       and not p.habilitado
       and p.motivo like 'baixa_vista:%'
       and not exists (select 1 from public.vista_status_baixa b where b.status = e.status)
    returning 1
  ), marcados as (
    update public.vista_webhooks_recebidos w
       set processado = true, processado_em = now(), erro = null, evento = 'STATUS_IMOVEL'
     where not w.processado
       and w.assinatura_ok
       and w.payload->>'code' is not null
       and w.payload->>'status' is not null
    returning 1
  )
  select (select count(*) from bloqueio), (select count(*) from religa), (select count(*) from marcados)
    into v_bloqueados, v_religados, v_marcados;

  return jsonb_build_object('ok', true, 'bloqueados', v_bloqueados,
                            'religados', v_religados, 'webhooks_processados', v_marcados);
end;
$$;

revoke all on function public.fn_processar_webhooks_status_vista(int) from public, anon, authenticated;

-- Mesmo motivo: o carimbo de vendido_em só vale se a baixa for o estado
-- atual do imóvel. Limpa o carimbo de quem voltou ao mercado.
create or replace function public.fn_carimbar_vendidos_por_webhook()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare v_carimbados int := 0; v_limpos int := 0;
begin
  with estado_atual as (
    select distinct on (w.payload->>'code')
      w.payload->>'code' as codigo, w.payload->>'status' as status, w.recebido_em
    from public.vista_webhooks_recebidos w
    where w.assinatura_ok and w.payload->>'code' is not null
      and w.payload->>'status' is not null
    order by w.payload->>'code', w.recebido_em desc
  ), carimba as (
    update public.vista_imoveis_log v
       set vendido_em = coalesce(v.vendido_em, e.recebido_em)
      from estado_atual e
     where v.codigo_vista = e.codigo
       and v.vendido_em is null
       and (e.status like 'Vendido%' or e.status like 'Alugado%')
    returning 1
  ), limpa as (
    update public.vista_imoveis_log v
       set vendido_em = null
      from estado_atual e
     where v.codigo_vista = e.codigo
       and v.vendido_em is not null
       and e.status in ('Venda', 'Aluguel', 'Venda e Aluguel')
    returning 1
  )
  select (select count(*) from carimba), (select count(*) from limpa)
    into v_carimbados, v_limpos;
  return jsonb_build_object('ok', true, 'carimbados', v_carimbados, 'limpos', v_limpos);
end;
$$;

revoke all on function public.fn_carimbar_vendidos_por_webhook() from public, anon, authenticated;
