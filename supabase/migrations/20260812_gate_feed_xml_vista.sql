-- 12/08/2026 — Trava definitiva contra anúncio inativo no portal.
--
-- Problema: o feed obedecia ao espelho `vista_imoveis_log`, e o espelho é cego
-- pra desativação — a sincronização do Vista lê a carteira ativa via API, e um
-- imóvel desativado simplesmente some da resposta em vez de vir marcado como
-- inativo. Resultado: 42426 (inativo desde 16/07) e 44666 seguiam com
-- `ativo_vista = true`, publicados com 33 fotos cada, gerando lead errado.
-- Na medição, 282 anúncios ativos no feed estavam ausentes do XML de portais
-- do Vista; 183 deles tinham book completo e estavam no ar.
--
-- Fonte de verdade adotada: o XML de portais do Vista. Se o Vista não exporta
-- o imóvel pros portais, a Jazz não publica. É exatamente a regra pedida —
-- "se ele estiver no Vista ativo, carrega no XML; estando desativado, não
-- carrega no XML" — só que ancorada num sinal que enxerga a desativação.
--
-- Onde a trava age: `feed_property_portal_publicacao`, que o gerador de XML já
-- consulta antes de emitir. Isso mantém a trava fora do caminho do sync, então
-- um ciclo de sincronização não desfaz o bloqueio (foi assim que 214 imóveis
-- com `vendido_em` voltaram ao ar em 11/08).
--
-- `motivo = 'ausente_xml_vista'` separa o bloqueio automático de um bloqueio
-- feito por pessoa: a regra só religa o que ela mesma desligou.

create table if not exists public.feed_vista_xml_snapshot (
  codigo text primary key,
  visto_em timestamptz not null default now()
);

alter table public.feed_property_portal_publicacao
  add column if not exists motivo text;

create or replace function public.fn_gate_feed_xml_vista()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_novos int := 0;
  v_frescos int := 0;
  v_ativos int := 0;
  v_bloquear int := 0;
  v_bloqueados int := 0;
  v_liberados int := 0;
  v_limite timestamptz := now() - interval '2 hours';
begin
  -- 1) absorve o ciclo corrente do sync (lista completa de códigos do XML do Vista).
  --    O sync roda de 5 em 5 minutos e reescreve `feed_sync_pendente_itens` a
  --    cada ciclo, então o retrato aqui fica contínuo mesmo com a tabela sendo
  --    apagada no fechamento de ciclo.
  insert into public.feed_vista_xml_snapshot (codigo, visto_em)
  select i.codigo, now() from public.feed_sync_pendente_itens i
  on conflict (codigo) do update set visto_em = excluded.visto_em;
  get diagnostics v_novos = row_count;

  select count(*) into v_frescos from public.feed_vista_xml_snapshot where visto_em >= v_limite;

  -- 2) guard de frescor: sem retrato recente do XML, não mexe em nada.
  if v_frescos < 500 then
    return jsonb_build_object('ok', false, 'motivo', 'snapshot do XML do Vista sem frescor',
                              'frescos', v_frescos, 'absorvidos', v_novos);
  end if;

  select count(*) into v_ativos from public.feed_properties where ativo;

  select count(*) into v_bloquear
  from public.feed_properties fp
  where fp.ativo
    and not exists (select 1 from public.feed_vista_xml_snapshot s
                    where s.codigo = fp.codigo_original and s.visto_em >= v_limite);

  -- 3) guard de massa: acima de 20% do acervo vira alerta, não vira ação —
  --    um XML truncado do Vista não pode zerar os portais em silêncio.
  if v_ativos > 0 and v_bloquear > greatest(50, (v_ativos * 0.2)::int) then
    insert into public.vista_alertas (codigo_vista, tipo, dados)
    values ('__feed__', 'feed_desativacao_massa_bloqueada',
            jsonb_build_object('candidatos', v_bloquear, 'ativos', v_ativos,
                               'frescos', v_frescos, 'origem', 'fn_gate_feed_xml_vista'));
    return jsonb_build_object('ok', false, 'motivo', 'bloqueio em massa barrado',
                              'candidatos', v_bloquear, 'ativos', v_ativos, 'frescos', v_frescos);
  end if;

  -- 4) ausente do XML sai do ar. Vale também pros inativos: se o sync reativar
  --    um deles pelo espelho, a trava já está posta e não abre janela de
  --    publicação até a próxima rodada.
  insert into public.feed_property_portal_publicacao (property_id, portal, habilitado, motivo, atualizado_em)
  select fp.id, 'vrsync_rede', false, 'ausente_xml_vista', now()
  from public.feed_properties fp
  where not exists (select 1 from public.feed_vista_xml_snapshot s
                    where s.codigo = fp.codigo_original and s.visto_em >= v_limite)
  on conflict (property_id, portal) do update
    set habilitado = false, motivo = 'ausente_xml_vista', atualizado_em = now()
    where public.feed_property_portal_publicacao.habilitado
      and coalesce(public.feed_property_portal_publicacao.motivo, 'ausente_xml_vista') = 'ausente_xml_vista';
  get diagnostics v_bloqueados = row_count;

  -- 5) voltou pro XML, volta pro ar — só o que esta regra desligou.
  update public.feed_property_portal_publicacao p
     set habilitado = true, atualizado_em = now()
   from public.feed_properties fp
  where p.property_id = fp.id
    and p.portal = 'vrsync_rede'
    and not p.habilitado
    and p.motivo = 'ausente_xml_vista'
    and exists (select 1 from public.feed_vista_xml_snapshot s
                where s.codigo = fp.codigo_original and s.visto_em >= v_limite);
  get diagnostics v_liberados = row_count;

  delete from public.feed_vista_xml_snapshot where visto_em < now() - interval '30 days';

  return jsonb_build_object('ok', true, 'absorvidos', v_novos, 'frescos', v_frescos,
                            'ativos', v_ativos, 'bloqueados', v_bloqueados, 'liberados', v_liberados);
end;
$$;

revoke all on function public.fn_gate_feed_xml_vista() from public, anon, authenticated;

-- Vigia da própria trava: anúncio ativo, ausente do XML e ainda liberado pro
-- portal é falha da trava, e falha de trava não pode passar em silêncio.
create or replace function public.fn_vigia_gate_xml_vista()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_frescos int;
  v_no_ar int := 0;
  v_alertas int := 0;
  v_limite timestamptz := now() - interval '2 hours';
begin
  select count(*) into v_frescos from public.feed_vista_xml_snapshot where visto_em >= v_limite;
  if v_frescos < 500 then
    insert into public.vista_alertas (codigo_vista, tipo, dados)
    select '__feed__', 'feed_espelho_parado',
           jsonb_build_object('fonte','snapshot_xml_vista','frescos',v_frescos,'detectado_em',now())
    where not exists (select 1 from public.vista_alertas a
                      where a.tipo='feed_espelho_parado' and a.codigo_vista='__feed__'
                        and a.created_at > now() - interval '6 hours');
    return jsonb_build_object('ok', false, 'motivo', 'snapshot sem frescor', 'frescos', v_frescos);
  end if;

  with no_ar as (
    select fp.codigo_original, fp.dados_normalizados->>'cidade' as cidade
    from public.feed_properties fp
    left join public.feed_property_portal_publicacao p
      on p.property_id = fp.id and p.portal = 'vrsync_rede'
    where fp.ativo
      and coalesce(p.habilitado, true)
      and not exists (select 1 from public.feed_vista_xml_snapshot s
                      where s.codigo = fp.codigo_original and s.visto_em >= v_limite)
  ), gravados as (
    insert into public.vista_alertas (codigo_vista, tipo, dados)
    select n.codigo_original, 'feed_anuncio_indevido_no_ar',
           jsonb_build_object('cidade', n.cidade, 'origem', 'ausente_xml_vista_sem_trava',
                              'detectado_em', now())
    from no_ar n
    where not exists (select 1 from public.vista_alertas a
                      where a.codigo_vista = n.codigo_original
                        and a.tipo = 'feed_anuncio_indevido_no_ar'
                        and a.created_at > now() - interval '24 hours')
    returning 1
  )
  select (select count(*) from no_ar), (select count(*) from gravados)
    into v_no_ar, v_alertas;

  if v_no_ar > 0 then
    raise warning '[vigia-gate-xml] % anuncio(s) ativo(s) e AUSENTE(s) do XML do Vista sem trava no portal', v_no_ar;
  end if;

  return jsonb_build_object('ok', true, 'frescos', v_frescos, 'no_ar_sem_trava', v_no_ar,
                            'alertas_novos', v_alertas);
end;
$$;

revoke all on function public.fn_vigia_gate_xml_vista() from public, anon, authenticated;

alter table public.vista_alertas drop constraint if exists vista_alertas_tipo_check;
alter table public.vista_alertas add constraint vista_alertas_tipo_check check (tipo = any (array[
  'venda_detectada','anuncio_parado','reativacao','imovel_sumiu','nome_ambiguo',
  'feed_anuncio_fora_do_ar','feed_anuncio_indevido_no_ar','feed_espelho_parado',
  'feed_desativacao_massa_bloqueada'
]));

-- Crons: a trava roda defasada do sync (*/5), o vigia uma vez por hora.
select cron.schedule('feed-gate-xml-vista', '4-59/5 * * * *', $$select public.fn_gate_feed_xml_vista();$$);
select cron.schedule('vigia-gate-xml-vista', '48 * * * *', $$select public.fn_vigia_gate_xml_vista();$$);
