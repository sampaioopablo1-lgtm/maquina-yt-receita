-- 03/09/2026 — busca de imóveis em linguagem natural (barra única, estilo Google).
--
-- O PROBLEMA
--
-- O site de listagem hoje só sabe filtrar por combos (tipo, cidade, faixa de
-- preço). Quem chega da mídia paga digita frase: "apartamento 3 quartos no
-- Jardim Aquarius até 700 mil". Cada combo a mais é um clique a mais antes do
-- primeiro imóvel na tela — e é onde o lead cai.
--
-- A DECISÃO
--
-- Uma barra só. O parser roda no banco (fn_interpretar_busca), não no
-- frontend, por três motivos: o dicionário de bairro/cidade É o acervo (sai de
-- vista_imoveis_log, não de uma lista mantida à mão); a mesma interpretação
-- serve site, WhatsApp e CRM sem reescrever; e o filtro precisa virar SQL no
-- mesmo lugar onde o índice está.
--
-- O que a frase não disser, ninguém filtra: campo ausente é campo livre.
-- O que ela disser e o parser não entender vira busca textual no tsvector.
--
-- SUPERFÍCIE PÚBLICA
--
-- rpc_buscar_imoveis(q, limite, pagina, ordenar) — security definer, só
-- devolve ficha ativa e só coluna de vitrine. corretor, captador, proprietário
-- e raw NÃO passam por aqui: o site é anônimo.

create extension if not exists unaccent;
create extension if not exists pg_trgm;

-- ---------------------------------------------------------------------------
-- normalização
-- ---------------------------------------------------------------------------

-- unaccent/1 é STABLE (resolve o dicionário em runtime); a forma de 2
-- argumentos com regdictionary literal é IMMUTABLE, e é isso que permite usar
-- em coluna gerada e em índice.
create or replace function public.fn_norm(t text)
returns text
language sql
immutable
parallel safe
set search_path = public, extensions
as $$
  select lower(unaccent('unaccent'::regdictionary, coalesce(t, '')))
$$;

-- "500 mil", "1,2 milhão", "450.000", "700k", "1.2M" -> numeric em reais.
create or replace function public.fn_valor_br(num text, escala text)
returns numeric
language plpgsql
immutable
parallel safe
as $$
declare
  v numeric;
  s text := lower(coalesce(escala, ''));
begin
  -- 1.234.567,89 (pt-BR) vs 1234.56: ponto só é decimal quando não há vírgula
  -- e sobra no máximo 2 casas depois dele.
  if num like '%,%' then
    v := nullif(replace(replace(num, '.', ''), ',', '.'), '')::numeric;
  elsif num ~ '^\d+\.\d{1,2}$' then
    v := num::numeric;
  else
    v := nullif(replace(num, '.', ''), '')::numeric;
  end if;

  if v is null then
    return null;
  end if;

  if s in ('mil', 'k') then
    v := v * 1000;
  elsif s in ('milhao', 'milhoes', 'mi', 'm') then
    v := v * 1000000;
  end if;

  -- "apartamento de 700" quer dizer 700 mil, não R$ 700. Só corrige quando a
  -- frase não trouxe escala nenhuma.
  if s = '' and v < 10000 then
    v := v * 1000;
  end if;

  return v;
exception when others then
  return null;
end;
$$;

-- Coluna gerada não aceita subquery; a planificação do jsonb tem que morar
-- numa função IMMUTABLE própria.
create or replace function public.fn_texto_caracteristicas(c jsonb)
returns text
language sql
immutable
parallel safe
as $$
  select coalesce(
    case jsonb_typeof(c)
      when 'array'  then (select string_agg(x, ' ') from jsonb_array_elements_text(c) x)
      when 'object' then (select string_agg(k || ' ' || coalesce(v #>> '{}', ''), ' ')
                            from jsonb_each(c) as e(k, v))
      when 'string' then c #>> '{}'
      else null
    end, '')
$$;

-- ---------------------------------------------------------------------------
-- índice de busca textual
-- ---------------------------------------------------------------------------

alter table public.vista_imoveis_log
  add column if not exists busca_texto tsvector
  generated always as (
    setweight(to_tsvector('portuguese',
      public.fn_norm(coalesce(empreendimento, '') || ' ' ||
                     coalesce(bairro, '')        || ' ' ||
                     coalesce(cidade, '')        || ' ' ||
                     coalesce(categoria, ''))), 'A')
    ||
    setweight(to_tsvector('portuguese',
      public.fn_norm(coalesce(endereco, '') || ' ' ||
                     coalesce(descricao_web, ''))), 'B')
    ||
    setweight(to_tsvector('portuguese',
      public.fn_norm(public.fn_texto_caracteristicas(caracteristicas))), 'C')
  ) stored;

create index if not exists ix_vista_imoveis_busca_texto
  on public.vista_imoveis_log using gin (busca_texto);

-- Filtros que a barra gera com mais frequência.
create index if not exists ix_vista_imoveis_vitrine
  on public.vista_imoveis_log (ativo_vista, finalidade, categoria, dormitorios)
  where ativo_vista;

create index if not exists ix_vista_imoveis_bairro_trgm
  on public.vista_imoveis_log using gin (public.fn_norm(bairro) gin_trgm_ops);

-- ---------------------------------------------------------------------------
-- dicionário de lugares: sai do acervo, não de lista mantida à mão
-- ---------------------------------------------------------------------------

create materialized view if not exists public.busca_lugares as
select 'bairro'::text as campo, bairro as valor, public.fn_norm(bairro) as norma, count(*) as fichas
  from public.vista_imoveis_log
 where ativo_vista and coalesce(bairro, '') <> ''
 group by bairro
union all
select 'cidade', cidade, public.fn_norm(cidade), count(*)
  from public.vista_imoveis_log
 where ativo_vista and coalesce(cidade, '') <> ''
 group by cidade;

create unique index if not exists ix_busca_lugares on public.busca_lugares (campo, valor);
create index if not exists ix_busca_lugares_norma on public.busca_lugares using gin (norma gin_trgm_ops);

create or replace function public.fn_busca_lugares_refresh()
returns void
language sql
security definer
set search_path = public
as $$
  refresh materialized view concurrently public.busca_lugares;
$$;

-- ---------------------------------------------------------------------------
-- o parser
-- ---------------------------------------------------------------------------

create or replace function public.fn_interpretar_busca(q text)
returns jsonb
language plpgsql
stable
set search_path = public, extensions
as $$
declare
  t          text;
  resto      text;
  r          jsonb := '{}'::jsonb;
  m          text[];
  v_bairro   text;
  v_cidade   text;
  v_cat      text;
begin
  t := public.fn_norm(q);
  t := regexp_replace(t, '[^a-z0-9,\.\s]', ' ', 'g');
  t := btrim(regexp_replace(t, '\s+', ' ', 'g'));

  if t = '' then
    return jsonb_build_object('texto_livre', null);
  end if;

  resto := t;

  -- finalidade -----------------------------------------------------------
  if resto ~ '\y(aluguel|alugar|alugo|locacao|para alugar)\y' then
    r := r || jsonb_build_object('finalidade', 'locacao');
    resto := regexp_replace(resto, '\y(aluguel|alugar|alugo|locacao|para alugar)\y', ' ', 'g');
  elsif resto ~ '\y(venda|comprar|compra|vender|a venda)\y' then
    r := r || jsonb_build_object('finalidade', 'venda');
    resto := regexp_replace(resto, '\y(venda|comprar|compra|vender|a venda)\y', ' ', 'g');
  end if;

  -- área ----------------------------------------------------------------
  -- Antes do preço de propósito: em "acima de 250 m2" o número é metragem, e
  -- o regex de piso de preço casaria nele primeiro.
  m := regexp_match(resto, '\y(\d+)\s*(?:m2|m|metros|metros quadrados)\y');
  if m is not null then
    r := r || jsonb_build_object('area_min', m[1]::numeric);
    resto := regexp_replace(resto, '\y\d+\s*(?:m2|m|metros|metros quadrados)\y', ' ');
  end if;

  -- preço ----------------------------------------------------------------
  -- teto: "ate 700 mil", "no maximo 1,2 milhao", "abaixo de 500000"
  m := regexp_match(resto,
    '\y(?:ate|abaixo de|no maximo|maximo|max|menos de)\s+(?:r\$\s*)?([\d\.,]+)\s*(mil|milhao|milhoes|mi|k|m)?\y');
  if m is not null then
    r := r || jsonb_build_object('preco_max', public.fn_valor_br(m[1], m[2]));
    resto := regexp_replace(resto,
      '\y(?:ate|abaixo de|no maximo|maximo|max|menos de)\s+(?:r\$\s*)?[\d\.,]+\s*(mil|milhao|milhoes|mi|k|m)?\y', ' ');
  end if;

  -- piso: "acima de 400 mil", "a partir de 300000"
  m := regexp_match(resto,
    '\y(?:acima de|a partir de|no minimo|minimo|min|mais de)\s+(?:r\$\s*)?([\d\.,]+)\s*(mil|milhao|milhoes|mi|k|m)?\y');
  if m is not null then
    r := r || jsonb_build_object('preco_min', public.fn_valor_br(m[1], m[2]));
    resto := regexp_replace(resto,
      '\y(?:acima de|a partir de|no minimo|minimo|min|mais de)\s+(?:r\$\s*)?[\d\.,]+\s*(mil|milhao|milhoes|mi|k|m)?\y', ' ');
  end if;

  -- faixa: "entre 400 e 600 mil"
  m := regexp_match(resto,
    '\yentre\s+(?:r\$\s*)?([\d\.,]+)\s*(mil|milhao|milhoes|mi|k|m)?\s+e\s+(?:r\$\s*)?([\d\.,]+)\s*(mil|milhao|milhoes|mi|k|m)?\y');
  if m is not null then
    -- "entre 400 e 600 mil": a escala do segundo número vale pros dois.
    r := r || jsonb_build_object(
      'preco_min', public.fn_valor_br(m[1], coalesce(nullif(m[2], ''), m[4])),
      'preco_max', public.fn_valor_br(m[3], m[4]));
    resto := regexp_replace(resto,
      '\yentre\s+(?:r\$\s*)?[\d\.,]+\s*(mil|milhao|milhoes|mi|k|m)?\s+e\s+(?:r\$\s*)?[\d\.,]+\s*(mil|milhao|milhoes|mi|k|m)?\y', ' ');
  end if;

  -- contagens ------------------------------------------------------------
  m := regexp_match(resto, '\y(\d+)\s*(?:quartos?|dormitorios?|dorms?|qtos?|qts?)\y');
  if m is not null then
    r := r || jsonb_build_object('dormitorios', m[1]::int);
    resto := regexp_replace(resto, '\y\d+\s*(?:quartos?|dormitorios?|dorms?|qtos?|qts?)\y', ' ');
  end if;

  m := regexp_match(resto, '\y(\d+)\s*(?:suites?)\y');
  if m is not null then
    r := r || jsonb_build_object('suites', m[1]::int);
    resto := regexp_replace(resto, '\y\d+\s*suites?\y', ' ');
  end if;

  m := regexp_match(resto, '\y(\d+)\s*(?:vagas?|garagens?)\y');
  if m is not null then
    r := r || jsonb_build_object('vagas', m[1]::int);
    resto := regexp_replace(resto, '\y\d+\s*(?:vagas?|garagens?)\y', ' ');
  end if;

  m := regexp_match(resto, '\y(\d+)\s*(?:banheiros?|wcs?)\y');
  if m is not null then
    r := r || jsonb_build_object('banheiros', m[1]::int);
    resto := regexp_replace(resto, '\y\d+\s*(?:banheiros?|wcs?)\y', ' ');
  end if;

  -- categoria: sinônimo do corretor -> valor que o Vista grava -----------
  v_cat := case
    when resto ~ '\y(apartamentos?|apto?s?|aptos?)\y'      then 'Apartamento'
    when resto ~ '\y(sobrados?)\y'                          then 'Sobrado'
    when resto ~ '\y(coberturas?)\y'                        then 'Cobertura'
    when resto ~ '\y(kitnets?|kitchenettes?|studios?)\y'    then 'Kitnet'
    when resto ~ '\y(casas?|residencias?)\y'                then 'Casa'
    when resto ~ '\y(terrenos?|lotes?)\y'                   then 'Terreno'
    when resto ~ '\y(chacaras?|sitios?)\y'                  then 'Chácara'
    when resto ~ '\y(salas?|conjuntos?|escritorios?)\y'     then 'Sala'
    when resto ~ '\y(galpoes?|galpao)\y'                    then 'Galpão'
    when resto ~ '\y(lojas?|pontos? comerciais?)\y'         then 'Loja'
    when resto ~ '\y(predios?|edificios?)\y'                then 'Prédio'
    else null
  end;
  if v_cat is not null then
    r := r || jsonb_build_object('categoria', v_cat);
    resto := regexp_replace(resto,
      '\y(apartamentos?|apto?s?|aptos?|sobrados?|coberturas?|kitnets?|kitchenettes?|studios?|casas?|residencias?|terrenos?|lotes?|chacaras?|sitios?|salas?|conjuntos?|escritorios?|galpoes?|galpao|lojas?|pontos? comerciais?|predios?|edificios?)\y',
      ' ', 'g');
  end if;

  -- lugar: casa o texto contra o dicionário do acervo, maior nome primeiro
  -- ("jardim aquarius" tem que ganhar de "jardim").
  select valor into v_bairro
    from public.busca_lugares
   where campo = 'bairro'
     and length(norma) >= 4
     and resto like '%' || norma || '%'
   order by length(norma) desc, fichas desc
   limit 1;
  if v_bairro is not null then
    r := r || jsonb_build_object('bairro', v_bairro);
    resto := replace(resto, public.fn_norm(v_bairro), ' ');
  end if;

  select valor into v_cidade
    from public.busca_lugares
   where campo = 'cidade'
     and length(norma) >= 4
     and resto like '%' || norma || '%'
   order by length(norma) desc, fichas desc
   limit 1;
  if v_cidade is not null then
    r := r || jsonb_build_object('cidade', v_cidade);
    resto := replace(resto, public.fn_norm(v_cidade), ' ');
  end if;

  -- código Vista digitado direto na barra ("AP1234", "12345")
  m := regexp_match(t, '\y([a-z]{0,3}\d{4,})\y');
  if m is not null and r = '{}'::jsonb then
    r := r || jsonb_build_object('codigo', upper(m[1]));
    resto := '';  -- código é busca exata; não repescar como texto livre
  end if;

  -- o que sobrou: palavra de cauda ("piscina", "mobiliado", nome de
  -- condomínio que não está no dicionário) vira busca textual.
  resto := btrim(regexp_replace(resto, '\y(de|do|da|dos|das|no|na|nos|nas|em|com|para|pra|e|o|a|os|as|um|uma|imovel|imoveis|acima|abaixo|ate|maximo|max|minimo|min|entre|partir|mais|menos|m2|m|metros|quadrados|r)\y', ' ', 'g'));
  resto := btrim(regexp_replace(resto, '\s+', ' ', 'g'));

  return r || jsonb_build_object('texto_livre', nullif(resto, ''), 'consulta', q);
end;
$$;

-- ---------------------------------------------------------------------------
-- a RPC que o site chama
-- ---------------------------------------------------------------------------

create or replace function public.rpc_buscar_imoveis(
  q        text default null,
  limite   int  default 24,
  pagina   int  default 1,
  ordenar  text default 'relevancia'
)
returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  f        jsonb;
  tsq      tsquery;
  v_total  bigint := 0;
  v_itens  jsonb  := '[]'::jsonb;
  v_lim    int    := least(greatest(coalesce(limite, 24), 1), 60);
  v_off    int;
  v_ord    text   := coalesce(ordenar, 'relevancia');
  v_frouxo boolean := false;
begin
  v_off := (greatest(coalesce(pagina, 1), 1) - 1) * v_lim;
  f := public.fn_interpretar_busca(q);

  if nullif(f->>'texto_livre', '') is not null then
    tsq := plainto_tsquery('portuguese', f->>'texto_livre');
    if coalesce(tsq::text, '') = '' then
      tsq := null;  -- frase só de stopword não deve virar filtro
    end if;
  end if;

  -- Duas leituras (total e página) sobre o mesmo conjunto: materializa uma vez.
  -- Chamadas em sequência na mesma transação reencontrariam a temp anterior.
  if to_regclass('pg_temp._busca_res') is not null then
    drop table _busca_res;
  end if;
  create temporary table _busca_res on commit drop as
  select v.codigo_vista, v.categoria, v.finalidade, v.bairro, v.cidade, v.endereco,
         v.empreendimento, v.valor_venda, v.valor_locacao, v.valor_condominio,
         v.valor_iptu, v.area_util, v.area_total, v.dormitorios, v.suites,
         v.banheiros, v.vagas, v.foto_destaque, v.video, v.tour_360,
         v.latitude, v.longitude, v.updated_at,
         coalesce(nullif(v.valor_venda, 0), v.valor_locacao) as preco,
         case when tsq is null then 0::real else ts_rank(v.busca_texto, tsq) end as rank_texto
    from public.vista_imoveis_log v
   where v.ativo_vista
     and (f->>'codigo'      is null or v.codigo_vista = f->>'codigo')
     and (f->>'finalidade'  is null or public.fn_norm(v.finalidade) = public.fn_norm(f->>'finalidade'))
     and (f->>'categoria'   is null or public.fn_norm(v.categoria)  = public.fn_norm(f->>'categoria'))
     and (f->>'bairro'      is null or v.bairro = f->>'bairro')
     and (f->>'cidade'      is null or v.cidade = f->>'cidade')
     and (f->>'dormitorios' is null or v.dormitorios >= (f->>'dormitorios')::int)
     and (f->>'suites'      is null or v.suites      >= (f->>'suites')::int)
     and (f->>'vagas'       is null or v.vagas       >= (f->>'vagas')::int)
     and (f->>'banheiros'   is null or v.banheiros   >= (f->>'banheiros')::int)
     and (f->>'area_min'    is null or coalesce(v.area_util, v.area_total) >= (f->>'area_min')::numeric)
     and (f->>'preco_min'   is null or coalesce(nullif(v.valor_venda, 0), v.valor_locacao) >= (f->>'preco_min')::numeric)
     and (f->>'preco_max'   is null or coalesce(nullif(v.valor_venda, 0), v.valor_locacao) <= (f->>'preco_max')::numeric)
     and (tsq is null or v.busca_texto @@ tsq);

  select count(*) into v_total from _busca_res;

  -- Frase inteira sem casar no AND devolveria tela vazia com acervo cheio.
  -- Repete sem o corte textual e marca a resposta como ampliada, pro site
  -- poder dizer "não achamos X, veja o que temos perto".
  if v_total = 0 and tsq is not null then
    v_frouxo := true;
    drop table _busca_res;
    create temporary table _busca_res on commit drop as
    select v.codigo_vista, v.categoria, v.finalidade, v.bairro, v.cidade, v.endereco,
           v.empreendimento, v.valor_venda, v.valor_locacao, v.valor_condominio,
           v.valor_iptu, v.area_util, v.area_total, v.dormitorios, v.suites,
           v.banheiros, v.vagas, v.foto_destaque, v.video, v.tour_360,
           v.latitude, v.longitude, v.updated_at,
           coalesce(nullif(v.valor_venda, 0), v.valor_locacao) as preco,
           0::real as rank_texto
      from public.vista_imoveis_log v
     where v.ativo_vista
       and (f->>'finalidade'  is null or public.fn_norm(v.finalidade) = public.fn_norm(f->>'finalidade'))
       and (f->>'categoria'   is null or public.fn_norm(v.categoria)  = public.fn_norm(f->>'categoria'))
       and (f->>'bairro'      is null or v.bairro = f->>'bairro')
       and (f->>'cidade'      is null or v.cidade = f->>'cidade')
       and (f->>'dormitorios' is null or v.dormitorios >= (f->>'dormitorios')::int)
       and (f->>'preco_min'   is null or coalesce(nullif(v.valor_venda, 0), v.valor_locacao) >= (f->>'preco_min')::numeric)
       and (f->>'preco_max'   is null or coalesce(nullif(v.valor_venda, 0), v.valor_locacao) <= (f->>'preco_max')::numeric);
    select count(*) into v_total from _busca_res;
  end if;

  select coalesce(jsonb_agg(
           jsonb_build_object(
             'codigo',         p.codigo_vista,
             'categoria',      p.categoria,
             'finalidade',     p.finalidade,
             'bairro',         p.bairro,
             'cidade',         p.cidade,
             'endereco',       p.endereco,
             'empreendimento', p.empreendimento,
             'valor_venda',    p.valor_venda,
             'valor_locacao',  p.valor_locacao,
             'condominio',     p.valor_condominio,
             'iptu',           p.valor_iptu,
             'area_util',      p.area_util,
             'area_total',     p.area_total,
             'dormitorios',    p.dormitorios,
             'suites',         p.suites,
             'banheiros',      p.banheiros,
             'vagas',          p.vagas,
             'foto_destaque',  p.foto_destaque,
             'video',          p.video,
             'tour_360',       p.tour_360,
             'latitude',       p.latitude,
             'longitude',      p.longitude,
             'relevancia',     round(p.rank_texto::numeric, 6)
           ) order by p.ord), '[]'::jsonb)
    into v_itens
    from (
      select r.*,
             row_number() over (
               order by
                 case when v_ord = 'preco_asc'  then r.preco end asc  nulls last,
                 case when v_ord = 'preco_desc' then r.preco end desc nulls last,
                 case when v_ord = 'recentes'   then r.updated_at end desc nulls last,
                 r.rank_texto desc,
                 r.foto_destaque is null,
                 r.updated_at desc nulls last
             ) as ord
        from _busca_res r
    ) p
   where p.ord > v_off and p.ord <= v_off + v_lim;

  return jsonb_build_object(
    'ok', true,
    'total', v_total,
    'pagina', greatest(coalesce(pagina, 1), 1),
    'limite', v_lim,
    'ordenar', v_ord,
    'busca_ampliada', v_frouxo,
    'interpretacao', f,
    'itens', v_itens
  );
end;
$$;

revoke all on function public.rpc_buscar_imoveis(text, int, int, text) from public;
grant execute on function public.rpc_buscar_imoveis(text, int, int, text) to anon, authenticated;
grant execute on function public.fn_interpretar_busca(text) to anon, authenticated;
