-- 10/09/2026 — a varredura vê o mesmo anúncio 3x por dia e joga fora.
--
-- O DESPERDÍCIO
--
-- captacao-prospectar grava com `ignoreDuplicates: true` em (fonte,
-- anuncio_id). Toda vez que a varredura reencontra um anúncio já conhecido —
-- o que acontece a cada rodada, três vezes por dia — o resultado é descartado.
--
-- Com isso a operação não sabe, de nenhum anúncio:
--   * há quantos dias ele está no ar;
--   * se o preço caiu, e quanto;
--   * quando ele saiu do portal.
--
-- POR QUE ISSO É O ATIVO, E NÃO UM DETALHE
--
-- Lista comprada é foto. Quem varre todos os dias tem filme, e o filme é a
-- única vantagem desta operação que um concorrente com mais orçamento não
-- consegue comprar pronta.
--
-- O que o filme diz, em ordem de valor pro captador:
--
--   1. PARTICULAR PARADO HÁ MUITO TEMPO. Dono anunciando sozinho há 90 dias
--      já tentou e não conseguiu. É o lead mais maduro que existe e o mais
--      fácil de abordar, porque a dor é dele e ele já sabe que ela existe.
--      Ligar no dia 3 é oferecer ajuda a quem ainda acha que não precisa.
--
--   2. QUEDA DE PREÇO. Dono que baixa o preço está declarando urgência antes
--      de qualquer conversa. Duas quedas seguidas é urgência confirmada.
--
--   3. SUMIÇO. Sumiu em três semanas: vendeu — e vendeu sem a Jazz, o que é
--      informação de mercado que vale a pena medir por bairro. Sumiu depois
--      de quatro meses: desistiu. Desistiu atende telefone.
--
--   4. REINCIDÊNCIA. Mesmo imóvel anunciado, retirado e reanunciado meses
--      depois: dono que quer vender, não consegue, e tenta de novo. Se ele já
--      passou por dois ciclos sozinho, o terceiro ele aceita ajuda.
--
-- O QUE MUDA NO CÓDIGO DA COLETA
--
-- Uma linha em captacao-prospectar/index.ts:166. De:
--     .upsert(linhas, { onConflict: "fonte,anuncio_id", ignoreDuplicates: true })
-- Para:
--     .upsert(linhas.map(l => ({ ...l, visto_em: new Date().toISOString() })),
--             { onConflict: "fonte,anuncio_id" })
--
-- O resto acontece aqui: o trigger abaixo registra a mudança de preço e
-- preserva `coletado_em` (primeira vez) enquanto `visto_em` (última vez) anda.
--
-- Sem essa linha, esta migração não quebra nada — só fica sem alimentar
-- histórico, e todos os sinais ficam nulos, que é exatamente o estado de hoje.

alter table public.captacao_prospects
  add column if not exists visto_em         timestamptz,
  add column if not exists sumiu_em         timestamptz,
  add column if not exists preco_inicial    numeric,
  add column if not exists quedas_de_preco  int not null default 0,
  add column if not exists ciclos           int not null default 1;

-- Anúncio já conhecido: a primeira vista é a que já está gravada.
update public.captacao_prospects
   set visto_em = coalesce(visto_em, coletado_em),
       preco_inicial = coalesce(preco_inicial, preco)
 where visto_em is null or preco_inicial is null;

create index if not exists idx_captacao_prospects_visto
  on public.captacao_prospects (visto_em desc nulls last);

-- ---------------------------------------------------------------------------
-- histórico de preço
-- ---------------------------------------------------------------------------

create table if not exists public.captacao_prospect_precos (
  id           bigserial primary key,
  prospect_id  bigint not null references public.captacao_prospects(id) on delete cascade,
  preco        numeric not null,
  visto_em     timestamptz not null default now()
);

create index if not exists idx_captacao_precos_prospect
  on public.captacao_prospect_precos (prospect_id, visto_em desc);

-- ---------------------------------------------------------------------------
-- o trigger que transforma reencontro em sinal
-- ---------------------------------------------------------------------------

create or replace function public.tg_captacao_prospect_visto()
returns trigger
language plpgsql
as $$
begin
  -- coletado_em é a PRIMEIRA vez. O upsert não pode empurrá-la para frente,
  -- senão "dias no portal" vira sempre zero — que é o bug que este arquivo
  -- existe para não criar.
  new.coletado_em  := old.coletado_em;
  new.preco_inicial := coalesce(old.preco_inicial, old.preco);
  new.visto_em     := greatest(coalesce(new.visto_em, now()), coalesce(old.visto_em, old.coletado_em));

  -- Reapareceu depois de ter sumido: novo ciclo do mesmo dono.
  if old.sumiu_em is not null then
    new.ciclos   := coalesce(old.ciclos, 1) + 1;
    new.sumiu_em := null;
  else
    new.ciclos   := coalesce(old.ciclos, 1);
  end if;

  -- Queda de preço: registra e conta. Só queda; reajuste para cima não é
  -- sinal de urgência, é dono testando o mercado.
  if new.preco is not null and old.preco is not null and new.preco < old.preco then
    new.quedas_de_preco := coalesce(old.quedas_de_preco, 0) + 1;
    insert into public.captacao_prospect_precos (prospect_id, preco, visto_em)
    values (old.id, new.preco, coalesce(new.visto_em, now()));
  else
    new.quedas_de_preco := coalesce(old.quedas_de_preco, 0);
  end if;

  -- Anúncio que voltou à fila merece nova chance com o captador: o motivo de
  -- ligar mudou (agora tem tempo de portal e talvez queda de preço).
  if new.quedas_de_preco > coalesce(old.quedas_de_preco, 0) and old.status = 'sugerido' then
    new.status := 'novo';
    new.sugerido_em := null;
  end if;

  return new;
end;
$$;

drop trigger if exists trg_captacao_prospect_visto on public.captacao_prospects;
create trigger trg_captacao_prospect_visto
  before update on public.captacao_prospects
  for each row execute function public.tg_captacao_prospect_visto();

-- ---------------------------------------------------------------------------
-- quem sumiu do portal
-- ---------------------------------------------------------------------------

-- Chamada depois de cada varredura completa de uma cidade. Marca como sumido
-- quem não foi revisto na última passagem.
create or replace function public.fn_captacao_marcar_sumidos(p_dias int default 3)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare n int;
begin
  -- GUARDA CONTRA ESVAZIAR A FILA NO DIA UM.
  --
  -- `visto_em` foi retro-preenchido a partir de `coletado_em` nesta migração,
  -- e a Edge Function só passa a escrevê-lo depois da mudança no index.ts. Sem
  -- esta guarda, a primeira execução marcaria como sumida a base inteira —
  -- medido no teste: 37 de 37 linhas — e sumido vale score -1000, ou seja, a
  -- fila do captador zerava.
  --
  -- Só é candidato a sumido quem a coleta nova já reviu ao menos uma vez, o
  -- que se prova por visto_em ter andado além de coletado_em. Quem nunca foi
  -- revisto não é "sumido": é desconhecido, e desconhecido continua na fila.
  update public.captacao_prospects
     set sumiu_em = now()
   where sumiu_em is null
     and visto_em is not null
     and visto_em > coletado_em + interval '1 hour'
     and visto_em < now() - make_interval(days => greatest(p_dias, 1));
  get diagnostics n = row_count;

  return jsonb_build_object(
    'marcados_agora', n,
    'sumidos_total',  (select count(*) from public.captacao_prospects where sumiu_em is not null),
    -- Sumiu rápido = vendeu. Sumiu devagar = desistiu. A fronteira em 45 dias
    -- é palpite; medir por bairro quando houver massa.
    'vendeu_rapido',  (select count(*) from public.captacao_prospects
                        where sumiu_em is not null and sumiu_em - coletado_em < interval '45 days'),
    'desistiu',       (select count(*) from public.captacao_prospects
                        where sumiu_em is not null and sumiu_em - coletado_em >= interval '45 days'));
end;
$$;

-- ---------------------------------------------------------------------------
-- os sinais entram no score
-- ---------------------------------------------------------------------------

create or replace function public.fn_captacao_score()
returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  v jsonb;
begin
  with regua as (
    select public.fn_norm(cidade) c, public.fn_norm(bairro) b,
           percentile_cont(0.5) within group (
             order by valor_venda / nullif(coalesce(area_util, area_total), 0)) as m2
      from public.vista_imoveis_log
     where ativo_vista and valor_venda > 0
       and coalesce(area_util, area_total) > 0
     group by 1, 2
    having count(*) >= 4
  ),
  calc as (
    select p.preco / nullif(p.area, 0) as m2_anuncio,
           r.m2 as m2_bairro,
           extract(day from now() - p.coletado_em)::int as dias_no_portal,
           (select 1 from public.captacao_nao_perturbe n
             where n.telefone = regexp_replace(coalesce(p.telefone,''), '\D', '', 'g')) as bloqueado,
           p.*
      from public.captacao_prospects p
      left join regua r on r.c = public.fn_norm(p.cidade)
                       and r.b = public.fn_norm(p.bairro)
  )
  update public.captacao_prospects p set
    score = case when c.bloqueado is not null or c.ja_no_acervo
                   or c.sumiu_em is not null then -1000 else
        0
      + case when c.ex_carteira then 40 else 0 end
      + case when c.perfil = 'particular' then 1000
             when c.perfil = 'indefinido' then 100
             else -5000 end
      + case when c.m2_anuncio is not null and c.m2_bairro is not null
                  and c.m2_anuncio < c.m2_bairro * 0.90 then 15 else 0 end
      + case when c.whatsapp is not null then 5 else 0 end
      + case when coalesce(c.anuncios_no_telefone, 1) = 1 then 10 else 0 end
      -- DIMENSÃO TEMPO. Inverte a régua antiga de propósito: o anúncio velho
      -- vale MAIS que o novo. Dono no dia 3 ainda acha que vende sozinho;
      -- dono no dia 90 já sabe que não vende.
      + case when c.dias_no_portal >= 90 then 45
             when c.dias_no_portal >= 60 then 35
             when c.dias_no_portal >= 30 then 20
             when c.dias_no_portal >= 14 then 8
             else 0 end
      -- Queda de preço é urgência declarada.
      + least(coalesce(c.quedas_de_preco, 0), 3) * 20
      -- Já tentou e voltou: cada ciclo é uma frustração a mais.
      + (greatest(coalesce(c.ciclos, 1), 1) - 1) * 25
      end,
    score_motivos = jsonb_strip_nulls(jsonb_build_object(
      'bloqueado_nao_perturbe', case when c.bloqueado is not null then true end,
      'ja_no_acervo',  case when c.ja_no_acervo then true end,
      'saiu_do_portal', case when c.sumiu_em is not null then true end,
      'ex_carteira',   case when c.ex_carteira then true end,
      'perfil',        c.perfil,
      'anuncios_no_telefone', c.anuncios_no_telefone,
      'dias_no_portal', c.dias_no_portal,
      'quedas_de_preco', nullif(coalesce(c.quedas_de_preco,0), 0),
      'preco_inicial',  case when c.quedas_de_preco > 0 then c.preco_inicial end,
      'ciclos',        nullif(coalesce(c.ciclos,1), 1),
      'm2_anuncio',    round(c.m2_anuncio),
      'm2_bairro',     round(c.m2_bairro),
      'abaixo_do_bairro', case when c.m2_anuncio is not null and c.m2_bairro is not null
                                and c.m2_anuncio < c.m2_bairro * 0.90 then true end,
      'acervo_codigo', c.acervo_codigo,
      'acervo_confianca', c.acervo_confianca))
    from calc c where p.id = c.id;

  select jsonb_build_object(
    'pontuados',  count(*),
    'chamaveis',  count(*) filter (where score > 0 and status = 'novo' and sugerido_em is null),
    'bloqueados', count(*) filter (where score = -1000),
    'maduros_60d', count(*) filter (where score > 0 and coletado_em < now() - interval '60 days'),
    'com_queda',  count(*) filter (where score > 0 and quedas_de_preco > 0),
    'score_max',  max(score)) into v
  from public.captacao_prospects;
  return v;
end;
$$;

-- A fila mostra o porquê temporal, que é o que abre a ligação.
drop function if exists public.fn_captacao_sugerir(int, text);
create function public.fn_captacao_sugerir(p_n int default 10, p_cidade text default null)
returns table(
  r_anuncio_id text, r_url text, r_titulo text, r_tipo text, r_cidade text, r_bairro text,
  r_preco numeric, r_area numeric, r_quartos int, r_anunciante text, r_telefone text,
  r_whatsapp text, r_perfil text, r_observacao text,
  r_score int, r_ex_carteira boolean, r_acervo_codigo text, r_acervo_confianca text,
  r_dias_no_portal int, r_quedas_de_preco int, r_preco_inicial numeric, r_ciclos int,
  r_score_motivos jsonb)
language plpgsql
security definer
set search_path = public
as $$
begin
  return query
  with candidatos as (
    select distinct on (p.telefone) p.id, p.telefone, p.score, p.coletado_em
      from public.captacao_prospects p
     where p.status = 'novo' and p.sugerido_em is null
       and p.telefone is not null
       and p.perfil in ('particular','indefinido')
       and coalesce(p.score, 0) > 0
       and (p_cidade is null or p.cidade ilike p_cidade)
     order by p.telefone, p.score desc nulls last, p.coletado_em desc
  ), escolhidos as (
    select c.id from candidatos c
     order by c.score desc nulls last, c.coletado_em asc   -- empate: o mais velho primeiro
     limit greatest(1, p_n)
  ), marcados as (
    update public.captacao_prospects p set sugerido_em = now(), status = 'sugerido'
     where p.id in (select id from escolhidos) returning p.*
  )
  select m.anuncio_id, m.url, m.titulo, m.tipo, m.cidade, m.bairro, m.preco, m.area,
         m.quartos, m.anunciante, m.telefone, m.whatsapp, m.perfil, m.motivo_perfil,
         m.score, m.ex_carteira, m.acervo_codigo, m.acervo_confianca,
         extract(day from now() - m.coletado_em)::int, m.quedas_de_preco,
         case when m.quedas_de_preco > 0 then m.preco_inicial end, m.ciclos,
         m.score_motivos
    from marcados m order by m.score desc nulls last, m.coletado_em asc;
end;
$$;

create or replace function public.fn_captacao_preparar(p_limite_carteira int default 4)
returns jsonb
language sql
security definer
set search_path = public
as $$
  select jsonb_build_object(
    'classificacao', public.fn_captacao_classificar(p_limite_carteira),
    'acervo',        public.fn_captacao_casar_acervo(),
    'sumidos',       public.fn_captacao_marcar_sumidos(),
    'score',         public.fn_captacao_score());
$$;

revoke all on function public.fn_captacao_marcar_sumidos(int) from public, anon;
revoke all on function public.fn_captacao_score() from public, anon;
revoke all on function public.fn_captacao_sugerir(int, text) from public, anon;
revoke all on function public.fn_captacao_preparar(int) from public, anon;
