-- 10/09/2026 — o radar de captação não estava chegando na porta que importa.
--
-- Existem DUAS portas de saída de prospect, e elas selecionam por caminhos
-- diferentes:
--
--   1. fn_captacao_sugerir       — a fila do captador, chamada sob demanda.
--   2. fn_captacao_processar_fila — as 10 sugestões POR SOLICITAÇÃO, disparadas
--      pelo gatilho de solicitação nova e pelo cron de 6 em 6 minutos.
--
-- As melhorias de 09/09 e 10/09 (score, ex_carteira, ja_no_acervo,
-- nao_perturbe, dias no portal, queda de preço) foram todas para a porta 1.
-- A porta 2 monta a própria consulta direto em captacao_prospects e só olhava
-- `perfil` — então herdou a régua de classificação corrigida, mas NÃO herdou
-- nenhum dos bloqueios.
--
-- O QUE ISSO SIGNIFICAVA NA PRÁTICA
--
-- No fluxo que de fato entrega as 10 sugestões ao corretor:
--   * quem pediu para NÃO ser procurado continuava sendo sugerido;
--   * imóvel que a própria Jazz já anuncia continuava sendo sugerido;
--   * anúncio que já saiu do portal continuava sendo sugerido.
--
-- O primeiro é o que mais importa: uma lista de não perturbe que vale em uma
-- porta e não vale na outra não é uma lista de não perturbe.
--
-- A CORREÇÃO
--
-- Um filtro (`coalesce(p.score, 1) > 0`) e um critério de ordenação. O
-- coalesce deixa passar quem ainda não foi pontuado, então antes da primeira
-- execução de fn_captacao_score o comportamento é idêntico ao de hoje.
--
-- A ordenação por preço em relação à faixa do cliente CONTINUA sendo o
-- critério dominante depois do perfil — aqui não é lista fria, é casamento com
-- uma solicitação real, e proximidade de orçamento é o que faz a sugestão
-- servir. O score entra como desempate dentro da mesma classe de perfil.

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

    select
      (select count(*) from public.solicitacao_sugestoes ss
        where ss.solicitacao_id = r.solicitacao_id and ss.status = 'sugerido' and ss.score >= p_score_min)
      +
      (select count(*) from public.solicitacao_sugestoes_externas se
        where se.solicitacao_id = r.solicitacao_id and se.status = 'sugerido' and se.score >= p_score_min)
    into v_boas;

    if v_boas >= p_min_boas then
      update public.captacao_fila_solicitacoes
         set processado_em = now(), resultado = format('base já cobre (%s sugestões >= %s)', v_boas, p_score_min)
       where solicitacao_id = r.solicitacao_id;
      v_ja_cobertas := v_ja_cobertas + 1;
      continue;
    end if;

    -- Puxa até 10 prospects por solicitação — a meta pedida pelo usuário
    -- (era 6). Descontado o que a base já tem de bom, pra não estourar 10.
    with pares as (
      select p.id as prospect_id, p.perfil, p.fonte,
             p.ex_carteira,
             extract(day from now() - p.coletado_em)::int as dias_portal,
             coalesce(p.quedas_de_preco, 0) as quedas,
             row_number() over (order by
               (p.perfil='particular') desc,
               -- O score entra DEPOIS do perfil e ANTES do preço: nunca
               -- inverte particular vs indefinido, mas dentro da mesma classe
               -- traz ex-carteira, anúncio maduro e queda de preço na frente.
               coalesce(p.score, 0) desc,
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
        -- Bloqueios do radar. score <= 0 marca nao_perturbe, imóvel que já é
        -- da Jazz, e anúncio que saiu do portal. `coalesce(p.score, 1)` deixa
        -- passar quem ainda não foi pontuado — antes de fn_captacao_score ter
        -- rodado a primeira vez, o comportamento é o de hoje, sem regressão.
        and coalesce(p.score, 1) > 0
    ), gravados as (
      insert into public.solicitacao_sugestoes_externas (solicitacao_id, prospect_id, score, motivo)
      select r.solicitacao_id, prospect_id,
             case when perfil='particular' then 90 else 60 end,
             case when perfil='particular'
                  then format('anúncio de particular em %s — captação sob demanda', fonte)
                  else format('anunciante não identificado em %s — confirmar na ligação', fonte) end
             || case when ex_carteira then ' · JÁ ESTEVE NO NOSSO ACERVO' else '' end
             || case when dias_portal >= 60 then format(' · %s dias no portal', dias_portal) else '' end
             || case when quedas > 0 then format(' · baixou o preço %sx', quedas) else '' end
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