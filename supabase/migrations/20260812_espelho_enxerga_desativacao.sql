-- 12/08/2026 — o espelho passa a enxergar desativação.
--
-- DIAGNÓSTICO
--
-- `vista_imoveis_log.visto_em` não é sinal de "existe hoje no Vista". O cron
-- `vista-sync-diario` (worker jazz-lead-conecta) pagina a API do Vista por
-- DataHoraAtualizacao e para em 500 imóveis por execução — 10 páginas de 50 —
-- com o offset travado no teto (224 dias, `proximoOffset = teto`). De hora em
-- hora ele revisita as mesmas ~500 fichas: `{"total":500,"novos":0,
-- "atualizados":500}`, execução após execução. Nos 10 dias anteriores a 12/08
-- o espelho registrou entre 1 e 18 registros tocados por dia, contra 5.510
-- marcados ativos. A varredura, na prática, não varre.
--
-- Daí o buraco: um imóvel desativado no Vista some da API em vez de vir
-- marcado como inativo, e o espelho, que só sabe marcar presença, nunca
-- registra a ausência. Foi assim que 42426 (inativo desde 16/07) e 44666
-- seguiram publicados com 33 fotos cada, gerando lead errado.
--
-- O worker tem um detector de "sumido" — desativa quem não é visto há 7 dias.
-- Ele responde `sumidosDetectados: 0` a cada execução, embora 1.473 registros
-- se qualifiquem, então o código publicado não é o do repositório. E ainda
-- bem: com a varredura alcançando 500 fichas, esse bloco desativaria o acervo
-- inteiro a 500 por hora. Religá-lo seria trocar um erro por um pior.
--
-- SINAL ADOTADO
--
-- O XML de portais do Vista, que chega completo e diário: 3.904 fichas, todas
-- presentes no espelho, nenhuma marcada inativa. `feed_vista_xml_snapshot`
-- guarda a última vez que cada código apareceu nele, e sumir de lá por 7 dias
-- seguidos é o que desativa.
--
-- O QUE A REGRA DELIBERADAMENTE NÃO FAZ
--
-- Desativar quem nunca apareceu no snapshot. 711 fichas estão ativas na API e
-- fora do XML: imóvel ativo no CRM que o Vista não exporta pros portais. Sobre
-- esses não temos sinal, e não ter sinal não é ter sinal negativo.
--
-- PASSIVO
--
-- 856 fichas seguem marcadas ativas sem aparecer no XML e sem a API tocá-las
-- há 7 a 63 dias. Não são desativadas automaticamente — o critério que as
-- pegaria é o `visto_em` do espelho, que é justamente o dado corrompido pela
-- varredura quebrada. Ficam na view `vw_espelho_suspeitos_inativos` para
-- conferência (42 delas têm captador responsável). Nenhuma está no ar: a
-- trava de publicação (20260812_gate_feed_xml_vista.sql) já as bloqueou.

create index if not exists idx_feed_vista_xml_snapshot_visto_em
  on public.feed_vista_xml_snapshot (visto_em);

create or replace function public.fn_reconciliar_espelho_vista(p_dias int default 7)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_frescos int;
  v_ativos int;
  v_candidatos int;
  v_desativados int := 0;
  v_alertas int := 0;
  v_teto int;
  v_limite_fresco timestamptz := now() - interval '2 hours';
  v_limite_ausencia timestamptz := now() - make_interval(days => greatest(1, p_dias));
begin
  select count(*) into v_frescos from public.feed_vista_xml_snapshot where visto_em >= v_limite_fresco;
  if v_frescos < 500 then
    return jsonb_build_object('ok', false, 'motivo', 'snapshot do XML sem frescor', 'frescos', v_frescos);
  end if;

  select count(*) into v_ativos from public.vista_imoveis_log where ativo_vista;
  v_teto := greatest(25, (v_ativos * 0.05)::int);

  create temp table _sumidos on commit drop as
  select v.codigo_vista, v.captador_id, v.bairro, v.cidade,
         v.valor_venda, v.valor_locacao, v.finalidade, s.visto_em as ultimo_xml
  from public.vista_imoveis_log v
  join public.feed_vista_xml_snapshot s on s.codigo = v.codigo_vista
  where v.ativo_vista
    and s.visto_em < v_limite_ausencia;

  select count(*) into v_candidatos from _sumidos;
  if v_candidatos = 0 then
    return jsonb_build_object('ok', true, 'candidatos', 0, 'desativados', 0,
                              'frescos', v_frescos, 'ativos', v_ativos);
  end if;

  -- Guard de massa: some gente demais de uma vez é sintoma de XML truncado,
  -- não de 5% do acervo ter saído do mercado no mesmo dia.
  if v_candidatos > v_teto then
    insert into public.vista_alertas (codigo_vista, tipo, dados)
    values ('__espelho__', 'feed_desativacao_massa_bloqueada',
            jsonb_build_object('candidatos', v_candidatos, 'teto', v_teto, 'ativos', v_ativos,
                               'frescos', v_frescos, 'origem', 'fn_reconciliar_espelho_vista'));
    return jsonb_build_object('ok', false, 'motivo', 'desativação em massa barrada',
                              'candidatos', v_candidatos, 'teto', v_teto, 'ativos', v_ativos);
  end if;

  update public.vista_imoveis_log v
     set ativo_vista = false,
         desaparecido_em = coalesce(v.desaparecido_em, now()),
         status_vista = 'Fora do XML do Vista'
    from _sumidos s
   where v.codigo_vista = s.codigo_vista;
  get diagnostics v_desativados = row_count;

  -- O captador confirma o que aconteceu: vendido, locado ou pausado.
  insert into public.vista_alertas (codigo_vista, tipo, captador_id, dados)
  select s.codigo_vista, 'imovel_sumiu', s.captador_id,
         jsonb_build_object('bairro', s.bairro, 'cidade', s.cidade,
                            'valor_venda', s.valor_venda, 'valor_locacao', s.valor_locacao,
                            'finalidade', s.finalidade, 'ultimo_xml', s.ultimo_xml,
                            'origem', 'fora_do_xml_vista', 'detectado_em', now())
  from _sumidos s
  where not exists (select 1 from public.vista_alertas a
                    where a.codigo_vista = s.codigo_vista and a.tipo = 'imovel_sumiu');
  get diagnostics v_alertas = row_count;

  return jsonb_build_object('ok', true, 'candidatos', v_candidatos, 'desativados', v_desativados,
                            'alertas', v_alertas, 'teto', v_teto, 'ativos', v_ativos,
                            'frescos', v_frescos, 'dias', greatest(1, p_dias));
end;
$$;

revoke all on function public.fn_reconciliar_espelho_vista(int) from public, anon, authenticated;

create or replace view public.vw_espelho_suspeitos_inativos as
select v.codigo_vista,
       v.captador_id,
       v.bairro,
       v.cidade,
       v.finalidade,
       v.valor_venda,
       v.valor_locacao,
       v.visto_em            as espelho_visto_em,
       s.visto_em            as xml_visto_em,
       (s.codigo is not null) as ja_esteve_no_xml,
       date_part('day', now() - v.visto_em)::int as dias_sem_ser_visto
from public.vista_imoveis_log v
left join public.feed_vista_xml_snapshot s
  on s.codigo = v.codigo_vista and s.visto_em >= now() - interval '2 hours'
where v.ativo_vista
  and s.codigo is null
  and (v.visto_em is null or v.visto_em < now() - interval '7 days');

revoke all on public.vw_espelho_suspeitos_inativos from anon;

select cron.schedule('espelho-reconciliar-xml', '52 6 * * *',
                     $$select public.fn_reconciliar_espelho_vista(7);$$);
