-- 13/08/2026 — Usuário mostrou print da tela do captador: solicitação de
-- venda (goncalves goncalves, SJC, R$650-800 mil) aparecendo com "0
-- pendentes" e "nenhum imóvel pra trabalhar aqui agora", mesmo já
-- processada pela rotina de captação.
--
-- Causa: `solicitacao_sugestoes` (a tabela que a migração anterior somou à
-- contagem de "já está coberta") tem `imovel_id` — são matches contra o
-- ESTOQUE JÁ CADASTRADO no Vista (o motor de vendas, pra oferecer imóvel
-- existente ao comprador). Não tem nada a ver com CAPTAÇÃO — encontrar
-- proprietário novo pra captar. A correção anterior (que somava as duas
-- tabelas pra corrigir o empilhamento infinito) resolveu um bug e causou
-- outro: uma solicitação com 18 matches de estoque e ZERO sugestão de
-- captação passou a ser marcada "já cobre, não mexe mais" — exatamente o
-- caso do print.
--
-- Fix: a contagem de "já está coberta" pra fins de CAPTAÇÃO volta a olhar
-- só `solicitacao_sugestoes_externas`. O empilhamento infinito que a
-- correção anterior evitava continua evitado, porque essa tabela por si só
-- já tem "not exists" contra o que já foi sugerido — o bug de somar as
-- duas tabelas era desnecessário pra esse fim.

create or replace function public.fn_captacao_processar_fila(
  p_lote int default 50, p_score_min numeric default 85, p_min_boas int default 10
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

    v_tipo_op := case when lower(coalesce(r.tipo_operacao,'')) like 'loca%' or lower(coalesce(r.tipo_operacao,'')) like 'alug%'
                       then 'rent' else 'sale' end;
    v_bt_varredura := case when v_tipo_op = 'rent' then 'RENTAL' else 'SALE' end;

    -- Só conta sugestão de CAPTAÇÃO (imóvel pra captar de fora), não match
    -- contra o estoque já cadastrado — são coisas diferentes.
    select count(*) into v_boas
    from public.solicitacao_sugestoes_externas se
    where se.solicitacao_id = r.solicitacao_id and se.status = 'sugerido' and se.score >= p_score_min;

    if v_boas >= p_min_boas then
      update public.captacao_fila_solicitacoes
         set processado_em = now(), resultado = format('captação já cobre (%s sugestões >= %s)', v_boas, p_score_min)
       where solicitacao_id = r.solicitacao_id;
      v_ja_cobertas := v_ja_cobertas + 1;
      continue;
    end if;

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
      from pares where rn <= greatest(0, greatest(10, p_min_boas) - v_boas)
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

-- Reabre pra reprocessar tudo que foi marcado "coberta" só por causa do
-- estoque (imovel_id), sem nenhuma sugestão de captação de verdade.
update public.captacao_fila_solicitacoes f
set processado_em = null, tentativas = 0
where f.processado_em is not null
  and (select count(*) from public.solicitacao_sugestoes_externas se
       where se.solicitacao_id = f.solicitacao_id and se.status='sugerido' and se.score >= 85) < 10;
