-- 17/08/2026 — Causa raiz de "imóvel vendido/alugado continua no portal".
--
-- O Vista JÁ AVISA, na hora, quando um imóvel sai do mercado: existe webhook
-- registrado na conta (código 11457, "Jazz Conecta DESATIVAR_IMOVEL")
-- apontando para o worker `jazz-lead-conecta`, e os eventos chegam de fato —
-- 14.360 recebidos desde 19/07, com assinatura válida.
--
-- Só que 100% deles foram gravados como evento 'desconhecido', com o erro
-- "evento 'desconhecido' sem handler — só auditado". Zero processados. O
-- motivo: o Vista manda o NOME do evento na query string da URL registrada
-- (`?evento=DESATIVAR_IMOVEL`), não dentro do corpo; o corpo traz apenas
-- `{"code": "41240", "status": "Vendido Terceiros"}`. O receptor do worker
-- classifica pelo corpo, então nunca reconheceu nenhum evento.
--
-- Resultado medido no momento desta migração: 365 códigos distintos que o
-- Vista marcou como fora do mercado, dos quais **26 ainda estavam ativos no
-- feed** — publicados nos portais como se estivessem disponíveis.
--
-- Correção aqui é deliberadamente no BANCO, não no worker: o payload que
-- chega já é suficiente (`code` + `status`), e o banco é onde o gate de
-- publicação vive. Assim a trava funciona mesmo sem alterar o worker
-- (que está fora deste repositório).
--
-- Vocabulário de status observado na própria conta (todos os valores
-- distintos recebidos em 14.360 eventos):
--   ativo:    Venda | Aluguel | Venda e Aluguel
--   baixa:    Vendido Terceiros | Vendido Imobiliária
--             Alugado Terceiros | Alugado Imobiliária | Suspenso
--   ambíguo:  Pendente  → NÃO tratado como baixa de propósito; é estado de
--             transição no Vista, derrubar anúncio por ele daria falso
--             positivo. Fica só auditado.
-- A documentação oficial (vs-public-api-documentation.loft.com.br) avisa que
-- esses rótulos são configuráveis por imobiliária, então a lista vive numa
-- tabela e não fixa no código.

create table if not exists public.vista_status_baixa (
  status text primary key,
  motivo text not null
);

insert into public.vista_status_baixa (status, motivo) values
  ('Vendido Terceiros',   'vendido por terceiros'),
  ('Vendido Imobiliária', 'vendido pela imobiliária'),
  ('Alugado Terceiros',   'alugado por terceiros'),
  ('Alugado Imobiliária', 'alugado pela imobiliária'),
  ('Suspenso',            'suspenso no Vista')
on conflict (status) do nothing;

-- Processa os webhooks pendentes: para cada código que o Vista marcou como
-- fora do mercado, desliga a publicação no portal. Grava em
-- `feed_property_portal_publicacao` (e não em `feed_properties.ativo`)
-- porque é ali que mora o gate que o gerador de XML respeita, e um ciclo de
-- sincronização não desfaz o bloqueio — mesma razão da trava de 12/08.
create or replace function public.fn_processar_webhooks_status_vista(p_lote int default 2000)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_bloqueados int := 0;
  v_marcados int := 0;
begin
  with pendentes as (
    select w.id, w.payload->>'code' as codigo, w.payload->>'status' as status, w.recebido_em
    from public.vista_webhooks_recebidos w
    join public.vista_status_baixa b on b.status = w.payload->>'status'
    where not w.processado
      and w.assinatura_ok
      and w.payload->>'code' is not null
    order by w.recebido_em
    limit greatest(1, p_lote)
  ), por_codigo as (
    -- O mesmo imóvel costuma ter vários eventos no histórico; o INSERT abaixo
    -- não pode tocar a mesma linha duas vezes no mesmo comando, então fica
    -- só o evento mais recente de cada código.
    select distinct on (codigo) codigo, status
    from pendentes
    order by codigo, recebido_em desc
  ), bloqueio as (
    insert into public.feed_property_portal_publicacao (property_id, portal, habilitado, motivo, atualizado_em)
    select fp.id, 'vrsync_rede', false, 'baixa_vista:' || p.status, now()
    from por_codigo p
    join public.feed_properties fp on fp.codigo_original = p.codigo
    on conflict (property_id, portal) do update
      set habilitado = false,
          motivo = excluded.motivo,
          atualizado_em = now()
      where public.feed_property_portal_publicacao.habilitado
    returning 1
  ), marcados as (
    update public.vista_webhooks_recebidos w
       set processado = true, processado_em = now(),
           erro = null,
           evento = 'STATUS_IMOVEL'
      from pendentes p
     where w.id = p.id
    returning 1
  )
  select (select count(*) from bloqueio), (select count(*) from marcados)
    into v_bloqueados, v_marcados;

  return jsonb_build_object('ok', true, 'bloqueados', v_bloqueados, 'webhooks_processados', v_marcados);
end;
$$;

revoke all on function public.fn_processar_webhooks_status_vista(int) from public, anon, authenticated;

-- Também carimba vendido_em no espelho, para o resto do pipeline (que já
-- respeita esse campo desde a v10) enxergar a baixa.
create or replace function public.fn_carimbar_vendidos_por_webhook()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare v_n int := 0;
begin
  with baixas as (
    select distinct on (w.payload->>'code')
      w.payload->>'code' as codigo, w.recebido_em
    from public.vista_webhooks_recebidos w
    join public.vista_status_baixa b on b.status = w.payload->>'status'
    where w.assinatura_ok and w.payload->>'code' is not null
      and (b.status like 'Vendido%' or b.status like 'Alugado%')
    order by w.payload->>'code', w.recebido_em desc
  )
  update public.vista_imoveis_log v
     set vendido_em = coalesce(v.vendido_em, b.recebido_em)
    from baixas b
   where v.codigo_vista = b.codigo and v.vendido_em is null;
  get diagnostics v_n = row_count;
  return jsonb_build_object('ok', true, 'carimbados', v_n);
end;
$$;

revoke all on function public.fn_carimbar_vendidos_por_webhook() from public, anon, authenticated;

-- De 5 em 5 minutos, defasado do gate de XML (que roda em 4-59/5).
select cron.schedule('vista-webhook-status', '2-59/5 * * * *',
  $$select public.fn_processar_webhooks_status_vista(2000);$$);
