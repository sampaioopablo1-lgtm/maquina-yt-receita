-- 09/09/2026 — captação: o rendimento de 6% não é limite da fonte, é da régua.
--
-- O NÚMERO QUE INCOMODA
--
-- A auditoria de 13/08 mediu, em 192 anúncios coletados: 156 empresas, 16
-- telefones genéricos, 10 ambíguos e 10 particulares. Dez ligações por 192
-- anúncios lidos. A leitura fácil é "a fonte é pobre, precisamos de outra".
--
-- A leitura certa é outra: a régua atual decide com DOIS campos do anúncio —
-- o CRECI e o nome do anunciante — e joga fora tudo que esses dois não
-- resolvem. O que falta pra decidir já está no banco, em duas coisas que a
-- Jazz tem e nenhum vendedor de lista tem:
--
--   1. o histórico da própria captacao_prospects, onde o MESMO telefone
--      reaparece anúncio após anúncio;
--   2. o acervo real (vista_imoveis_log, 3.894 fichas), que sabe quais imóveis
--      já são nossos, quais já foram, e quanto vale o metro quadrado do bairro.
--
-- O QUE MUDA
--
-- (1) Telefone repetido vira sinal de classificação.
--
-- Proprietário tem um imóvel, às vezes dois. Corretor autônomo sem CRECI no
-- anúncio e com nome de duas palavras — "Marcos Silva" — passa hoje como
-- `particular` e queima uma ligação. O que o denuncia não é o nome: é o mesmo
-- telefone em catorze anúncios. A tabela já tem esse dado e já tem índice por
-- telefone; ninguém contava.
--
-- (2) `s/?a$` estava comendo proprietário de sobrenome comum.
--
-- A régua tem `s/?a\.?$` para pegar "S/A" no fim do nome. Sem fronteira de
-- palavra antes do `s`, ela casa com QUALQUER nome terminado em "sa".
-- Medido: 'Nelson Barbosa', 'Ana Sousa', 'Marta Rosa', 'Jose Pedrosa' e
-- 'Rita Feitosa' são classificados como EMPRESA hoje e nunca chegam ao
-- captador. Barbosa e Sousa estão entre os sobrenomes mais comuns do país —
-- é volume perdido em silêncio, todo dia, desde que a régua existe.
--
-- E o erro anda nos dois sentidos: 'Predial S.A.' NÃO é pego hoje, porque o
-- ponto entre o S e o A quebra o casamento, e vai pro captador como
-- particular. `\ys[./]?a\.?$` corrige os dois de uma vez.
--
-- (2b) Nome de uma palavra continua `indefinido`, de propósito.
--
-- Foi tentador promover a `particular` quem tem nome de uma palavra e um
-- anúncio só — recuperaria os ~10 `indefinido` de cada 192 direto pra fila.
-- Mas 'Newcore', empresa listada na própria auditoria de 13/08, tem
-- exatamente esse formato: uma palavra, um anúncio. A promoção teria mandado
-- empresa pro captador rotulada como proprietário.
--
-- `indefinido` já entra na fila hoje. Quem resolve a ordem é o score, e o
-- motivo vai escrito na linha pra quem liga decidir com o dado à vista.
--
-- A régua de NOME não muda aqui. A correção de `\b` para `\y` (em Postgres
-- `\b` é backspace; fronteira de palavra é `\y`) já foi feita em
-- 20260813_captacao_fix_fronteira_regex, depois do episódio "Grupo Kaza
-- Apolo 05". Este arquivo carrega a versão corrigida por cópia, para aplicar
-- sozinho fora de ordem sem regredir aquilo.
--
-- (3) Cruzamento com o acervo, nos dois sentidos — e só quando é prova.
--
-- Imóvel que JÁ é nosso não pode ir pro captador: ele liga oferecendo captação
-- de algo que a Jazz já anuncia, e perde a credibilidade na primeira frase.
--
-- E o inverso é o lead mais quente que existe nesta operação: imóvel que
-- esteve no acervo, saiu (ativo_vista = false), e reaparece anunciado por
-- particular. O dono tirou da imobiliária e está tentando vender sozinho. Ele
-- já provou que quer vender, já provou que aceita intermediação, e agora está
-- descobrindo o trabalho que dá. Nenhuma base comprada sabe disso; só o
-- histórico da casa sabe.
--
-- (4) A fila passa a ser ordenada por score, não por data.
--
-- Dez ligações por rodada é pouco pra desperdiçar em ordem de coleta. O score
-- usa o acervo como régua de preço: anúncio de particular abaixo da mediana do
-- bairro é dono com pressa ou preço errado — os dois querem corretor.
--
-- O QUE NÃO MUDA, DE PROPÓSITO
--
-- Não há enriquecimento por CPF, e não haverá. Não existe fonte pública no
-- Brasil que ligue CPF a telefone; o que o mercado vende como "enriquecimento
-- cadastral" vem de vazamento. Cruzar isso aqui contaminaria a base inteira e
-- não teria volta. O telefone que entra continua sendo só o que o próprio
-- anunciante publicou no anúncio, para ser contatado.
--
-- E entra o que faltava do outro lado: captacao_nao_perturbe. Quem pede pra
-- não ser mais procurado sai da fila para sempre, por telefone, mesmo que
-- reapareça em anúncio novo daqui a um ano.

-- ---------------------------------------------------------------------------
-- dependência
-- ---------------------------------------------------------------------------

-- fn_norm veio da migração da busca (20260903). Recriada aqui com o mesmo
-- corpo pra que esta migração aplique sozinha, fora de ordem, sem quebrar.
create extension if not exists unaccent;

create or replace function public.fn_norm(t text)
returns text
language sql
immutable
parallel safe
set search_path = public, extensions
as $$
  select lower(unaccent('unaccent'::regdictionary, coalesce(t, '')))
$$;

-- ---------------------------------------------------------------------------
-- colunas novas
-- ---------------------------------------------------------------------------

alter table public.captacao_prospects
  add column if not exists anuncios_no_telefone int,
  add column if not exists ja_no_acervo   boolean not null default false,
  add column if not exists ex_carteira    boolean not null default false,
  add column if not exists acervo_codigo  text,
  add column if not exists acervo_confianca text,   -- 'forte' | 'fraca'
  add column if not exists score          int,
  add column if not exists score_motivos  jsonb;

create index if not exists idx_captacao_prospects_score
  on public.captacao_prospects (score desc nulls last)
  where status = 'novo' and sugerido_em is null;

-- ---------------------------------------------------------------------------
-- lista de não perturbe
-- ---------------------------------------------------------------------------

create table if not exists public.captacao_nao_perturbe (
  telefone   text primary key,
  motivo     text,
  registrado_em timestamptz not null default now(),
  registrado_por text
);

comment on table public.captacao_nao_perturbe is
  'Telefones que pediram para não ser procurados. Vale para sempre e para '
  'qualquer anúncio futuro do mesmo número. Nunca remover sem pedido do titular.';

create or replace function public.fn_captacao_nao_perturbe(
  p_telefone text, p_motivo text default null, p_por text default null)
returns void
language sql
security definer
set search_path = public
as $$
  insert into public.captacao_nao_perturbe (telefone, motivo, registrado_por)
  values (regexp_replace(coalesce(p_telefone,''), '\D', '', 'g'), p_motivo, p_por)
  on conflict (telefone) do update
    set motivo = coalesce(excluded.motivo, public.captacao_nao_perturbe.motivo);
$$;

-- ---------------------------------------------------------------------------
-- classificação v2: o telefone repetido entra como sinal
-- ---------------------------------------------------------------------------

-- A versão de 13/08 não recebe argumento. Deixar as duas torna
-- `fn_captacao_classificar()` AMBÍGUA — medido: "function is not unique" —
-- e quebraria o pg_cron e o script da fábrica que já chamam sem argumento.
drop function if exists public.fn_captacao_classificar();

create or replace function public.fn_captacao_classificar(
  p_limite_carteira int default 4   -- anúncios no mesmo telefone a partir do
)                                   -- qual o número é carteira, não dono
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v jsonb;
  -- Régua de nome inalterada: foi calibrada contra anúncios reais e as classes
  -- de acento cobrem IMOVÉIS / IMÓVEIS / IMOVEIS, que apareceram todas.
  re_empresa text := '(?i)(ltda|\ys[./]?a\.?$|eireli|\yme\y|\ymei\y|\yepp\y|im[oó]v[eé]|imobili|corretor|corretag|'
                  || 'consultor|assessor|administrador|construtor|construç|incorporad|empreendim|urbanism|'
                  || 'loteador|realty|broker|invest|neg[oó]cio|patrim|holding|participa|\yspe\y|'
                  || 're/?max|century|coelho da fonseca|\ylopes\y|bossa|keller|engel|'
                  || 'imobili[aá]ria|\ygrupo\y|\ycia\y|& cia|assoc|servi[çc]os|solu[çc][oõ]es|'
                  || 'engenharia|arquitet|\yhome\y|\yhomes\y|\yhouse\y|\yprime\y|\yelite\y|\yvip\y|'
                  || '\ymaster\y|\yplan\y|\yplanej\y|\yventures?\y|\ycorp\y|\ygroup\y)';
  re_fone_falso text := '^\d{2}(\d)\1{7,}$';
  v_lim int := greatest(coalesce(p_limite_carteira, 4), 2);
begin
  -- Quantos anúncios distintos existem por telefone, no acervo inteiro de
  -- prospects. É o que separa dono de carteira, e não custa coleta nenhuma.
  with contagem as (
    select telefone, count(distinct coalesce(anuncio_id, id::text)) as n
      from public.captacao_prospects
     where telefone is not null
     group by telefone
  )
  update public.captacao_prospects p
     set anuncios_no_telefone = c.n
    from contagem c
   where p.telefone = c.telefone
     and p.anuncios_no_telefone is distinct from c.n;

  update public.captacao_prospects p set
    perfil = case
      when p.telefone is null or p.telefone ~ re_fone_falso        then 'descartar'
      when p.tem_creci                                             then 'empresa'
      when coalesce(p.anunciante,'') ~ re_empresa                  then 'empresa'
      when coalesce(p.anuncios_no_telefone, 1) >= v_lim            then 'empresa'
      when coalesce(p.anuncios_no_telefone, 1) = v_lim - 1         then 'indefinido'
      when array_length(regexp_split_to_array(btrim(coalesce(p.anunciante,'')), '\s+'), 1) >= 2
                                                                   then 'particular'
      else 'indefinido'
    end,
    motivo_perfil = case
      when p.telefone is null or p.telefone ~ re_fone_falso then 'telefone ausente ou genérico'
      when p.tem_creci then 'CRECI informado no anúncio'
      when coalesce(p.anunciante,'') ~ re_empresa then 'nome com marca de empresa'
      when coalesce(p.anuncios_no_telefone, 1) >= v_lim
        then 'mesmo telefone em ' || p.anuncios_no_telefone || ' anúncios — carteira, não dono'
      when coalesce(p.anuncios_no_telefone, 1) = v_lim - 1
        then 'telefone em ' || p.anuncios_no_telefone || ' anúncios — no limite, confirmar na ligação'
      when array_length(regexp_split_to_array(btrim(coalesce(p.anunciante,'')), '\s+'), 1) >= 2
        then 'nome de pessoa, sem CRECI, telefone em ' || coalesce(p.anuncios_no_telefone,1) || ' anúncio(s)'
      else 'nome de uma palavra em ' || coalesce(p.anuncios_no_telefone,1) || ' anúncio(s) — confirmar na ligação'
    end;

  select jsonb_build_object(
    'particular',  count(*) filter (where perfil='particular'),
    'empresa',     count(*) filter (where perfil='empresa'),
    'indefinido',  count(*) filter (where perfil='indefinido'),
    'descartar',   count(*) filter (where perfil='descartar'),
    'limite_carteira', v_lim) into v
  from public.captacao_prospects;
  return v;
end;
$$;

-- ---------------------------------------------------------------------------
-- cruzamento com o acervo
-- ---------------------------------------------------------------------------

create or replace function public.fn_captacao_casar_acervo()
returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  v_endereco int := 0;
  v_ficha    int := 0;
  v jsonb;
begin
  update public.captacao_prospects p
     set ja_no_acervo = false, ex_carteira = false, acervo_codigo = null
   where p.ja_no_acervo or p.ex_carteira or p.acervo_codigo is not null;
  update public.captacao_prospects set acervo_confianca = null
   where acervo_confianca is not null;

  -- Casamento forte: endereço normalizado na mesma cidade. Só vale com
  -- endereço de rua E número dos dois lados — "Rua das Flores" sem número
  -- casaria meio bairro.
  with alvo as (
    select p.id, v.codigo_vista, v.ativo_vista
      from public.captacao_prospects p
      join public.vista_imoveis_log v
        on public.fn_norm(v.cidade) = public.fn_norm(p.cidade)
       and public.fn_norm(v.endereco) = public.fn_norm(p.endereco)
     where coalesce(p.endereco,'') ~ '\d'
       and coalesce(v.endereco,'') ~ '\d'
  )
  update public.captacao_prospects p
     set ja_no_acervo  = a.ativo_vista,
         ex_carteira   = not a.ativo_vista,
         acervo_codigo = a.codigo_vista,
         acervo_confianca = 'forte'
    from alvo a where p.id = a.id;
  get diagnostics v_endereco = row_count;

  -- Casamento fraco: mesma cidade, bairro, tipo, quartos, área ±5% e preço
  -- ±10%. NÃO define ex_carteira nem ja_no_acervo, e não pontua.
  --
  -- Medido na fixture: essa régua casou 174 anúncios contra UMA ficha, porque
  -- imóvel padrão de bairro padrão tem tipo, quartos, área e faixa de preço
  -- iguais aos milhares. Como ex_carteira vale +40 no score, deixar o
  -- casamento fraco defini-lo jogaria lixo pro topo da fila do captador — o
  -- oposto do que este arquivo existe pra fazer.
  --
  -- Então ele só anota o código pra ligação conferir. Suspeita é suspeita.
  with alvo as (
    select distinct on (p.id) p.id, v.codigo_vista
      from public.captacao_prospects p
      join public.vista_imoveis_log v
        on public.fn_norm(v.cidade)  = public.fn_norm(p.cidade)
       and public.fn_norm(v.bairro)  = public.fn_norm(p.bairro)
       and public.fn_norm(v.categoria) = public.fn_norm(p.tipo)
       and coalesce(v.dormitorios, -1) = coalesce(p.quartos, -1)
       and p.area  between coalesce(v.area_util, v.area_total) * 0.95
                       and coalesce(v.area_util, v.area_total) * 1.05
       and p.preco between v.valor_venda * 0.90 and v.valor_venda * 1.10
     where p.acervo_codigo is null
       and p.area > 0 and p.preco > 0
     order by p.id, v.ativo_vista desc, v.codigo_vista
  )
  update public.captacao_prospects p
     set acervo_codigo = a.codigo_vista, acervo_confianca = 'fraca'
    from alvo a where p.id = a.id;
  get diagnostics v_ficha = row_count;

  select jsonb_build_object(
    'casados_por_endereco', v_endereco,
    'casados_por_ficha_fraco', v_ficha,
    'ja_no_acervo',         count(*) filter (where ja_no_acervo),
    'ex_carteira',          count(*) filter (where ex_carteira))
    into v from public.captacao_prospects;
  return v;
end;
$$;

-- ---------------------------------------------------------------------------
-- score: dez ligações por rodada merecem ordem
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
  -- Régua de preço do próprio acervo: mediana do m² por bairro, só de ficha
  -- ativa e à venda. Bairro com menos de 4 fichas não faz mediana confiável.
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
    -- p.* já traz o id; declará-lo de novo deixa a coluna ambígua no update.
    select p.preco / nullif(p.area, 0) as m2_anuncio,
           r.m2 as m2_bairro,
           (select 1 from public.captacao_nao_perturbe n
             where n.telefone = regexp_replace(coalesce(p.telefone,''), '\D', '', 'g')) as bloqueado,
           p.*
      from public.captacao_prospects p
      left join regua r on r.c = public.fn_norm(p.cidade)
                       and r.b = public.fn_norm(p.bairro)
  )
  update public.captacao_prospects p set
    score = case when c.bloqueado is not null or c.ja_no_acervo then -1000 else
        0
      + case when c.ex_carteira then 40 else 0 end
      -- O peso do perfil é DOMINANTE de propósito: a régua de 13/08 garante
      -- que todo `particular` vem antes de todo `indefinido`, e o score não
      -- pode inverter isso. Medido: com pesos próximos, 'Newcore' (empresa de
      -- uma palavra, um anúncio) subiu na frente de proprietários por ser
      -- recente. Os outros sinais só ordenam DENTRO da mesma classe.
      + case when c.perfil = 'particular' then 1000
             when c.perfil = 'indefinido' then 100
             else -5000 end
      + case when c.m2_anuncio is not null and c.m2_bairro is not null
                  and c.m2_anuncio < c.m2_bairro * 0.90 then 15 else 0 end
      + case when c.whatsapp is not null then 5 else 0 end
      + case when c.coletado_em > now() - interval '7 days' then 10
             when c.coletado_em > now() - interval '30 days' then 5
             else 0 end
      + case when coalesce(c.anuncios_no_telefone, 1) = 1 then 10 else 0 end
      end,
    score_motivos = jsonb_strip_nulls(jsonb_build_object(
      'bloqueado_nao_perturbe', case when c.bloqueado is not null then true end,
      'ja_no_acervo',  case when c.ja_no_acervo then true end,
      'ex_carteira',   case when c.ex_carteira then true end,
      'perfil',        c.perfil,
      'anuncios_no_telefone', c.anuncios_no_telefone,
      'm2_anuncio',    round(c.m2_anuncio),
      'm2_bairro',     round(c.m2_bairro),
      'abaixo_do_bairro', case when c.m2_anuncio is not null and c.m2_bairro is not null
                                and c.m2_anuncio < c.m2_bairro * 0.90 then true end,
      'acervo_codigo', c.acervo_codigo,
      'acervo_confianca', c.acervo_confianca))
    from calc c where p.id = c.id;

  select jsonb_build_object(
    'pontuados', count(*),
    'chamaveis', count(*) filter (where score > 0 and status = 'novo' and sugerido_em is null),
    'bloqueados', count(*) filter (where score = -1000),
    'score_max', max(score)) into v
  from public.captacao_prospects;
  return v;
end;
$$;

-- Uma chamada só, na ordem certa, pro pg_cron e pro Actions.
create or replace function public.fn_captacao_preparar(p_limite_carteira int default 4)
returns jsonb
language sql
security definer
set search_path = public
as $$
  select jsonb_build_object(
    'classificacao', public.fn_captacao_classificar(p_limite_carteira),
    'acervo',        public.fn_captacao_casar_acervo(),
    'score',         public.fn_captacao_score());
$$;

-- ---------------------------------------------------------------------------
-- a fila, agora por score
-- ---------------------------------------------------------------------------

drop function if exists public.fn_captacao_sugerir(int, text);
create function public.fn_captacao_sugerir(p_n int default 10, p_cidade text default null)
returns table(
  r_anuncio_id text, r_url text, r_titulo text, r_tipo text, r_cidade text, r_bairro text,
  r_preco numeric, r_area numeric, r_quartos int, r_anunciante text, r_telefone text,
  r_whatsapp text, r_perfil text, r_observacao text,
  r_score int, r_ex_carteira boolean, r_acervo_codigo text, r_acervo_confianca text,
  r_score_motivos jsonb)
language plpgsql
security definer
set search_path = public
as $$
begin
  return query
  with candidatos as (
    -- Dedupe por telefone continua: mesmo dono com três anúncios é uma ligação.
    select distinct on (p.telefone) p.id, p.telefone, p.score, p.coletado_em
      from public.captacao_prospects p
     where p.status = 'novo' and p.sugerido_em is null
       and p.telefone is not null
       and p.perfil in ('particular','indefinido')
       and coalesce(p.score, 0) > 0          -- corta bloqueado e já-no-acervo
       and (p_cidade is null or p.cidade ilike p_cidade)
     order by p.telefone, p.score desc nulls last, p.coletado_em desc
  ), escolhidos as (
    select c.id from candidatos c
     order by c.score desc nulls last, c.coletado_em desc
     limit greatest(1, p_n)
  ), marcados as (
    update public.captacao_prospects p set sugerido_em = now(), status = 'sugerido'
     where p.id in (select id from escolhidos) returning p.*
  )
  select m.anuncio_id, m.url, m.titulo, m.tipo, m.cidade, m.bairro, m.preco, m.area,
         m.quartos, m.anunciante, m.telefone, m.whatsapp, m.perfil, m.motivo_perfil,
         m.score, m.ex_carteira, m.acervo_codigo, m.acervo_confianca, m.score_motivos
    from marcados m order by m.score desc nulls last, m.coletado_em desc;
end;
$$;

create or replace function public.fn_captacao_estoque()
returns jsonb
language sql
security definer
set search_path = public
as $$
  select jsonb_build_object(
    'disponiveis',   count(*) filter (where status='novo' and sugerido_em is null
                                        and telefone is not null and coalesce(score,0) > 0
                                        and perfil in ('particular','indefinido')),
    'particulares',  count(*) filter (where status='novo' and sugerido_em is null and perfil='particular'),
    'indefinidos',   count(*) filter (where status='novo' and sugerido_em is null and perfil='indefinido'),
    'ex_carteira',   count(*) filter (where status='novo' and sugerido_em is null and ex_carteira),
    'empresas_filtradas', count(*) filter (where perfil='empresa'),
    'ja_no_acervo',  count(*) filter (where ja_no_acervo),
    'nao_perturbe',  (select count(*) from public.captacao_nao_perturbe),
    'descartados',   count(*) filter (where perfil='descartar'),
    'ja_sugeridos',  count(*) filter (where sugerido_em is not null),
    'total_coletado', count(*)
  ) from public.captacao_prospects;
$$;

revoke all on function public.fn_captacao_classificar(int) from public, anon;
revoke all on function public.fn_captacao_casar_acervo() from public, anon;
revoke all on function public.fn_captacao_score() from public, anon;
revoke all on function public.fn_captacao_preparar(int) from public, anon;
revoke all on function public.fn_captacao_sugerir(int, text) from public, anon;
revoke all on function public.fn_captacao_estoque() from public, anon;
revoke all on function public.fn_captacao_nao_perturbe(text, text, text) from public, anon;
