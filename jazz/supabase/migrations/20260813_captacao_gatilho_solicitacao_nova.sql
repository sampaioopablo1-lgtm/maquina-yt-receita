-- 13/08/2026 — Gatilho automático de captação por API. Pedido do usuário:
-- "Insira, crie, ative rotina de que quando abrir uma solicitação, acione
-- automaticamente API, e sugeri os imóveis, caso na base, não tenha ao
-- menos 85% de score, sugera da API."
--
-- Aplicada ao banco nesta mesma sessão, mas ficou sem versão no repositório
-- por um corte de contexto — commitando agora pra existir histórico. As
-- versões seguintes de `fn_captacao_processar_fila` (multi-portal, venda x
-- locação, meta de 10 sugestões, todas datadas de 13/08 também) já
-- pressupõem que esta migração existe primeiro.
--
-- Desenho: a trigger só ENFILEIRA (grava uma linha em
-- captacao_fila_solicitacoes) — nenhuma chamada HTTP dentro da transação do
-- corretor. Quem de fato processa é o cron `captacao-processar-fila`, de 6
-- em 6 minutos, fora do caminho crítico de quem está criando a solicitação.

create table if not exists public.captacao_fila_solicitacoes (
  solicitacao_id uuid primary key references public.solicitacoes(id) on delete cascade,
  enfileirado_em timestamptz not null default now(),
  processado_em timestamptz,
  tentativas int not null default 0,
  resultado text
);

create index if not exists idx_captacao_fila_pendente
  on public.captacao_fila_solicitacoes (enfileirado_em) where (processado_em is null);

create or replace function public.trg_solicitacao_enfileira_captacao()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  if new.status in ('Trabalhando na busca do imóvel','Em Atendimento','Pendente','Aguardando Aprovação Pablo') then
    insert into public.captacao_fila_solicitacoes (solicitacao_id)
    values (new.id) on conflict (solicitacao_id) do nothing;
  end if;
  return new;
end;
$$;

drop trigger if exists tg_solicitacao_captacao on public.solicitacoes;
create trigger tg_solicitacao_captacao
  after insert on public.solicitacoes
  for each row execute function public.trg_solicitacao_enfileira_captacao();

-- p_min_boas=3 é o valor original desta migração; a migração
-- captacao_meta_dez_sugestoes (mesma data, aplicada depois) sobe pra 10 e
-- corrige um bug de contagem descoberto na sequência — não editar aqui.
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

    with pares as (
      select p.id as prospect_id, p.perfil,
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
                  then 'anúncio de particular no Zap — captação sob demanda'
                  else 'anunciante não identificado no Zap — confirmar na ligação' end
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
      insert into public.captacao_varredura (cidade, uf, business_type, ativa)
      values (coalesce(r.cidade,'São José dos Campos'), 'SP', 'SALE', true)
      on conflict (cidade, uf, business_type) do update set ativa = true;

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

select cron.schedule('captacao-processar-fila', '*/6 * * * *',
  $$select public.fn_captacao_processar_fila(60, 85, 3);$$);
