-- 13/08/2026 — sugestões vindas da API, para as solicitações que secaram.
--
-- Situação medida: 1.564 solicitações ativas, média de 19,2 sugestões cada.
-- Mas 120 estavam com menos de 10 e 52 zeradas — e a concentração é
-- reveladora: das 22 solicitações de Campinas, as 22 sem nenhuma sugestão;
-- Caraguatatuba 6 zeradas, Bragança 7, Atibaia 2. São José dos Campos, com
-- 1.518 solicitações, tinha 75 carentes e 9 zeradas.
--
-- O acervo próprio não cobre essas praças. A GeckoAPI cobre: imóveis
-- anunciados por particulares, com telefone, que a Jazz pode captar sob
-- demanda para atender quem já está na fila.
--
-- POR QUE TABELA SEPARADA
--
-- `solicitacao_sugestoes` tem 32.789 linhas, FK obrigatória para `imoveis` e
-- unique (solicitacao_id, imovel_id). Um prospect externo não existe em
-- `imoveis` — forçá-lo ali exigiria afrouxar a FK de uma tabela que o app usa
-- em produção. A tabela paralela carrega a mesma semântica sem tocar no que já
-- funciona, e `vw_solicitacao_sugestoes_todas` junta as duas na leitura.
--
-- Ressalva: o app hoje lê `solicitacao_sugestoes`. Estas sugestões ficam
-- disponíveis por consulta e exportação; aparecer na tela do captador depende
-- de ajuste no front, que vive no worker — fora do alcance de deploy daqui.

create table if not exists public.solicitacao_sugestoes_externas (
  id bigserial primary key,
  solicitacao_id uuid not null references public.solicitacoes(id) on delete cascade,
  prospect_id bigint not null references public.captacao_prospects(id) on delete cascade,
  score numeric,
  motivo text,
  status text not null default 'sugerido',
  data_criacao timestamptz not null default now(),
  data_acao timestamptz,
  unique (solicitacao_id, prospect_id)
);

create index if not exists idx_sse_solicitacao on public.solicitacao_sugestoes_externas (solicitacao_id, status);

-- "BRAGANCA PAULISTA", "Bragança Paulista" e "caraguatatuba" convivem nas
-- solicitações; sem normalizar, o casamento perde metade dos pares.
create or replace function public.fn_norm_cidade(t text)
returns text language sql immutable as $$
  select lower(regexp_replace(translate(coalesce(t,''),
    'áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ','aaaaeeiooouucaaaaeeiooouuc'), '[^a-z ]', '', 'g'));
$$;

create or replace function public.fn_casar_prospects_solicitacoes(p_max_por_solicitacao int default 5)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_inseridos int := 0;
  v_solicitacoes int := 0;
begin
  with carentes as (
    select s.id, s.cidade, s.valor_min, s.valor_max,
           (select count(*) from public.solicitacao_sugestoes ss
             where ss.solicitacao_id = s.id and ss.status = 'sugerido') as internas,
           (select count(*) from public.solicitacao_sugestoes_externas se
             where se.solicitacao_id = s.id and se.status = 'sugerido') as externas
    from public.solicitacoes s
    where s.status in ('Trabalhando na busca do imóvel','Em Atendimento','Pendente','Aguardando Aprovação Pablo')
      and coalesce(s.cidade,'') <> ''
  ), alvo as (
    select * from carentes where internas + externas < 10
  ), pares as (
    -- Faixa com 10% de folga em cada ponta: quem pede até 500 mil não deveria
    -- deixar de ver um imóvel de 520 mil que a negociação resolve.
    select a.id as solicitacao_id, p.id as prospect_id, p.perfil,
           row_number() over (partition by a.id order by
             (p.perfil = 'particular') desc,
             abs(coalesce(p.preco,0) - ((coalesce(a.valor_min,0) + coalesce(a.valor_max, coalesce(a.valor_min,0)*2)) / 2.0)),
             p.coletado_em desc) as rn
    from alvo a
    join public.captacao_prospects p
      on public.fn_norm_cidade(p.cidade) = public.fn_norm_cidade(a.cidade)
     and p.telefone is not null
     and p.perfil in ('particular','indefinido')
     and (a.valor_min is null or p.preco is null or p.preco >= a.valor_min * 0.9)
     and (a.valor_max is null or p.preco is null or p.preco <= a.valor_max * 1.1)
    where not exists (
      select 1 from public.solicitacao_sugestoes_externas x
       where x.solicitacao_id = a.id and x.prospect_id = p.id)
  ), gravados as (
    insert into public.solicitacao_sugestoes_externas (solicitacao_id, prospect_id, score, motivo)
    select solicitacao_id, prospect_id,
           case when perfil = 'particular' then 90 else 60 end,
           case when perfil = 'particular'
                then 'anúncio de particular no Zap — captação sob demanda'
                else 'anunciante não identificado no Zap — confirmar na ligação' end
    from pares where rn <= greatest(1, p_max_por_solicitacao)
    on conflict (solicitacao_id, prospect_id) do nothing
    returning solicitacao_id
  )
  select count(*), count(distinct solicitacao_id) into v_inseridos, v_solicitacoes from gravados;

  return jsonb_build_object('ok', true, 'sugestoes_criadas', v_inseridos,
                            'solicitacoes_atendidas', v_solicitacoes);
end;
$$;

create or replace view public.vw_solicitacao_sugestoes_todas as
select ss.solicitacao_id, 'acervo'::text as origem, ss.imovel_id::text as ref,
       ss.score, ss.status, ss.data_criacao, null::text as telefone, null::text as anunciante
from public.solicitacao_sugestoes ss
union all
select se.solicitacao_id, 'geckoapi'::text, se.prospect_id::text,
       se.score, se.status, se.data_criacao, p.telefone, p.anunciante
from public.solicitacao_sugestoes_externas se
join public.captacao_prospects p on p.id = se.prospect_id;

revoke all on function public.fn_casar_prospects_solicitacoes(int) from public, anon;
revoke all on public.vw_solicitacao_sugestoes_todas from anon;

select cron.schedule('captacao-casar-solicitacoes', '36 * * * *',
                     $cron$select public.fn_casar_prospects_solicitacoes(6);$cron$);
