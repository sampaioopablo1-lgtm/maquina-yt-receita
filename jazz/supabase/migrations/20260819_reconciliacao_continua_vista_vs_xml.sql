-- 19/08/2026 — Reconciliação contínua: nenhum imóvel inativo no XML.
--
-- Exigência do usuário: "não podemos ter imóvel inativo ou não publicado no
-- XML". As defesas que já existiam cobrem parte do caminho, mas a auditoria
-- de hoje achou a brecha que faltava:
--
--   Em 2 dias chegaram 730 webhooks do Vista classificados como
--   'desconhecido', envolvendo 170 códigos — e 98 deles são imóveis que
--   publicamos. O corpo desses webhooks traz SÓ `{"code": "47233"}`, sem
--   status, e o worker não registra a query string (onde o Vista põe o nome
--   do evento). Ou seja: sabemos que algo mudou naqueles imóveis, mas não
--   sabemos o quê — inclusive se foram EXCLUÍDOS.
--
-- A correção não tenta adivinhar o evento. Ela pergunta ao Vista qual é o
-- estado real de cada imóvel publicado, e trata dois casos de baixa:
--
--   1. STATUS DE BAIXA — o Vista devolve o imóvel com status de
--      vista_status_baixa (Vendido/Alugado/Suspenso/Pendente);
--   2. SUMIÇO — o Vista simplesmente NÃO devolve o código consultado.
--      É o caso da exclusão, que nenhum webhook nosso distinguia. Este é o
--      mais perigoso: o imóvel deixa de existir na origem e continuaria no ar.
--
-- Prioridade da fila: primeiro quem tem webhook recente não processado
-- (mudou agora), depois quem está há mais tempo sem conferência. Assim o
-- acervo inteiro é varrido continuamente, e quem mexeu fura a fila.
--
-- Limite da API do Vista: 50 resultados por página (400 acima disso).

create table if not exists public.feed_reconciliacao_vista (
  codigo_vista text primary key,
  verificado_em timestamptz,
  status_vista text,
  ausente_no_vista boolean not null default false,
  baixado_em timestamptz
);

create index if not exists feed_reconciliacao_ordem
  on public.feed_reconciliacao_vista (verificado_em nulls first);

alter table public.feed_reconciliacao_vista enable row level security;
-- Sem policy: só service_role.

create table if not exists public.feed_reconciliacao_lote (
  id bigserial primary key,
  req_id bigint not null,
  codigos text[] not null,
  criado_em timestamptz not null default now(),
  colhido_em timestamptz
);

alter table public.feed_reconciliacao_lote enable row level security;

create or replace function public.fn_reconciliar_vista_pedir(p_lote int default 50)
returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  v_key text;
  v_codigos text[];
  v_req bigint;
begin
  select decrypted_secret into v_key from vault.decrypted_secrets where name='vista_api_key';
  if v_key is null then return jsonb_build_object('ok', false, 'motivo','sem chave vista'); end if;

  select array_agg(cod) into v_codigos from (
    select fp.codigo_original cod,
           exists (select 1 from public.vista_webhooks_recebidos w
                    where w.payload->>'code' = fp.codigo_original
                      and not w.processado
                      and w.recebido_em > now() - interval '7 days') mexeu,
           r.verificado_em
    from public.feed_properties fp
    left join public.feed_property_portal_publicacao p
           on p.property_id = fp.id and p.portal = 'vrsync_rede'
    left join public.feed_reconciliacao_vista r on r.codigo_vista = fp.codigo_original
    where fp.ativo and coalesce(p.habilitado, true)
    order by mexeu desc, r.verificado_em nulls first
    limit least(50, greatest(1, p_lote))
  ) s;

  if v_codigos is null then return jsonb_build_object('ok', true, 'pedidos', 0); end if;

  select net.http_get(
    url := 'https://rafaelak-rest.vistahost.com.br/imoveis/listar?key=' || v_key ||
      '&pesquisa={"fields":["Codigo","Status"],"filter":{"Codigo":[' ||
      (select string_agg('"'||c||'"', ',') from unnest(v_codigos) c) ||
      ']},"paginacao":{"pagina":1,"quantidade":50}}',
    headers := '{"Accept":"application/json"}'::jsonb,
    timeout_milliseconds := 120000) into v_req;

  insert into public.feed_reconciliacao_lote (req_id, codigos) values (v_req, v_codigos);
  return jsonb_build_object('ok', true, 'pedidos', array_length(v_codigos,1), 'req', v_req);
end;
$$;

revoke all on function public.fn_reconciliar_vista_pedir(int) from public, anon, authenticated;

create or replace function public.fn_reconciliar_vista_colher()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  l record;
  v_resp jsonb;
  v_baixados int := 0;
  v_ausentes int := 0;
  v_conferidos int := 0;
begin
  for l in
    select fl.id, fl.req_id, fl.codigos, r.content, r.status_code
    from public.feed_reconciliacao_lote fl
    join net._http_response r on r.id = fl.req_id
    where fl.colhido_em is null
  loop
    if l.status_code <> 200 then
      update public.feed_reconciliacao_lote set colhido_em = now() where id = l.id;
      continue;
    end if;

    begin
      v_resp := l.content::jsonb;
    exception when others then
      update public.feed_reconciliacao_lote set colhido_em = now() where id = l.id;
      continue;
    end;

    insert into public.feed_reconciliacao_vista (codigo_vista, verificado_em, status_vista, ausente_no_vista)
    select c, now(), v_resp->c->>'Status', (v_resp ? c) is false
    from unnest(l.codigos) c
    on conflict (codigo_vista) do update
      set verificado_em = excluded.verificado_em,
          status_vista = excluded.status_vista,
          ausente_no_vista = excluded.ausente_no_vista;

    v_conferidos := v_conferidos + coalesce(array_length(l.codigos,1),0);
    update public.feed_reconciliacao_lote set colhido_em = now() where id = l.id;
  end loop;

  with alvo as (
    select r.codigo_vista from public.feed_reconciliacao_vista r
    join public.vista_status_baixa b on b.status = r.status_vista
    where r.baixado_em is null
  ), desliga as (
    update public.feed_property_portal_publicacao p
       set habilitado = false, motivo = 'reconciliacao:status_baixa', atualizado_em = now()
      from public.feed_properties fp, alvo a
     where p.property_id = fp.id and p.portal = 'vrsync_rede'
       and fp.codigo_original = a.codigo_vista and p.habilitado
    returning 1
  ), espelho as (
    update public.vista_imoveis_log v
       set ativo_vista = false
      from alvo a where v.codigo_vista = a.codigo_vista and v.ativo_vista
    returning 1
  )
  select count(*) from desliga into v_baixados;

  with alvo as (
    select codigo_vista from public.feed_reconciliacao_vista
    where ausente_no_vista and baixado_em is null
  ), desliga as (
    update public.feed_property_portal_publicacao p
       set habilitado = false, motivo = 'reconciliacao:ausente_no_vista', atualizado_em = now()
      from public.feed_properties fp, alvo a
     where p.property_id = fp.id and p.portal = 'vrsync_rede'
       and fp.codigo_original = a.codigo_vista and p.habilitado
    returning 1
  ), espelho as (
    update public.vista_imoveis_log v
       set ativo_vista = false
      from alvo a where v.codigo_vista = a.codigo_vista and v.ativo_vista
    returning 1
  )
  select count(*) from desliga into v_ausentes;

  update public.feed_reconciliacao_vista
     set baixado_em = now()
   where baixado_em is null
     and (ausente_no_vista or status_vista in (select status from public.vista_status_baixa));

  update public.vista_webhooks_recebidos w
     set processado = true, processado_em = now()
    from public.feed_reconciliacao_vista r
   where w.payload->>'code' = r.codigo_vista
     and not w.processado and r.verificado_em > w.recebido_em;

  return jsonb_build_object('ok', true, 'conferidos', v_conferidos,
    'baixados_por_status', v_baixados, 'baixados_por_sumico', v_ausentes);
end;
$$;

revoke all on function public.fn_reconciliar_vista_colher() from public, anon, authenticated;

-- 50 imóveis a cada 10 min = ~7.200/dia: o acervo publicado (2.949) é varrido
-- por inteiro mais de duas vezes ao dia, e quem tem webhook fura a fila.
select cron.schedule('reconciliar-vista-pedir',  '3,13,23,33,43,53 * * * *',
  $$select public.fn_reconciliar_vista_pedir(50);$$);
select cron.schedule('reconciliar-vista-colher', '7,17,27,37,47,57 * * * *',
  $$select public.fn_reconciliar_vista_colher();$$);
