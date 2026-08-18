-- 13/08/2026 — fn_captacao_processar_fila ainda inseria em captacao_varredura
-- sem a coluna `target`, que a migração de multi-portal (mesma data,
-- captacao_multi_portal) trocou na chave única. Erro visto ao rodar:
-- "there is no unique or exclusion constraint matching the ON CONFLICT
-- specification" — a fila inteira ficava travada na varredura sem
-- prospect, porque o próprio gatilho de reposição quebrava.
--
-- Agora liga a varredura nos três portais (Zap, VivaReal, Chaves na Mão) de
-- uma vez, em vez de só Zap — consistente com a pesquisa multi-portal.
-- Motivo do texto de sugestão também deixou de dizer "no Zap" (source fixo)
-- e passou a citar o portal de origem do prospect.

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
begin
  for r in
    select f.solicitacao_id, s.cidade, s.valor_min, s.valor_max
    from public.captacao_fila_solicitacoes f
    join public.solicitacoes s on s.id = f.solicitacao_id
    where f.processado_em is null and f.tentativas < 5
    order by f.enfileirado_em
    limit greatest(1, p_lote)
  loop
    v_processadas := v_processadas + 1;

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

    -- Base fraca: puxa do que a API já coletou para a cidade, em qualquer portal.
    with pares as (
      select p.id as prospect_id, p.perfil, p.fonte,
             row_number() over (order by (p.perfil='particular') desc,
               abs(coalesce(p.preco,0) - ((coalesce(r.valor_min,0) + coalesce(r.valor_max, coalesce(r.valor_min,0)*2))/2.0)),
               p.coletado_em desc) as rn
      from public.captacao_prospects p
      where public.fn_norm_cidade(p.cidade) = public.fn_norm_cidade(r.cidade)
        and p.telefone is not null
        and p.perfil in ('particular','indefinido')
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
      -- Sem prospect para a cidade: liga a varredura nos três portais e tenta de novo depois.
      insert into public.captacao_varredura (cidade, uf, business_type, target, ativa)
      values
        (coalesce(r.cidade,'São José dos Campos'), 'SP', 'SALE', 'zapimoveis.com.br', true),
        (coalesce(r.cidade,'São José dos Campos'), 'SP', 'SALE', 'vivareal.com.br', true),
        (coalesce(r.cidade,'São José dos Campos'), 'SP', 'SALE', 'chavesnamao.com.br', true)
      on conflict (cidade, uf, business_type, target) do update set ativa = true;

      update public.captacao_fila_solicitacoes
         set tentativas = tentativas + 1,
             resultado = 'sem prospect na cidade — varredura acionada'
       where solicitacao_id = r.solicitacao_id;
      v_sem_material := v_sem_material + 1;
    end if;
  end loop;

  return jsonb_build_object('ok', true, 'processadas', v_processadas,
    'ja_cobertas_pela_base', v_ja_cobertas, 'atendidas_pela_api', v_com_api,
    'aguardando_varredura', v_sem_material);
end;
$$;
