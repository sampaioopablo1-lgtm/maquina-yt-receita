-- Dois sinais que já chegavam do portal e a régua ignorava.
--
-- Diagnóstico de 14/09/2026, com o print da busca real na mão: as dez opções
-- vieram marcadas "Imobiliária", e ESTAVAM CERTAS — "SANT ANA INVESTIMENTOS"
-- casa em `invest` no regex de nome. Ou seja, o classificador não errou. O que
-- falta é OFERTA de particular: quando não há dez donos na fila, a busca
-- completa o número com carteira.
--
-- Então o ganho não está em apertar contra imobiliária. Está em parar de
-- perder o dono de verdade — e em usar o que o portal já diz e ninguém lia.
--
-- ------------------------------------------------------------------ sinal 1
-- PF / PJ, do Chaves na Mão.
--
-- O extrator já grava `dados.advertiser_type` desde 13/08, e o comentário no
-- próprio código dizia: "guardado em dados pra um futuro ajuste do
-- classificador". O futuro é agora. É o sinal mais direto que existe na
-- coleta: o portal declarando pessoa física ou jurídica, sem depender de
-- adivinhar pelo nome.
--
-- Vale nos dois sentidos, e o sentido que mais rende é o PF:
--
--   PJ -> empresa, direto.
--   PF -> resgata o dono que a régua de nome deixava em `indefinido`.
--
-- O resgate importa porque a regra de nome exige DUAS palavras para dizer
-- "particular" — quem anuncia como "Marcelo" ficava indefinido e não entrava
-- na fila. Com PF declarado e telefone em um anúncio só, é dono.
--
-- ------------------------------------------------------------------ sinal 2
-- Logo do anunciante.
--
-- Observação do usuário em 14/09, olhando os resultados: "as imagens, com
-- logo, normalmente são de imobiliárias". Está certo, e não é preciso olhar
-- pixel nenhum para usar isso: quem tem logo tem CADASTRO DE LOGO no portal, e
-- o objeto `advertiser` que já guardamos inteiro carrega esse campo. Pessoa
-- física que anuncia a própria casa não sobe logotipo.
--
-- A varredura é por NOME DE CHAVE que contenha "logo", e não por uma chave
-- fixa, de propósito: o campo aparece como `logoUrl` no glue-api da Grupo Zap,
-- mas já vi `logo` e `logotipo` em respostas do mesmo grupo, e fixar um nome
-- faria o sinal sumir calado no dia em que o portal renomear. Chave que casa e
-- valor não vazio é logo.

create or replace function public.fn_captacao_anunciante_tipo(p_dados jsonb)
returns text
language sql
immutable
as $$
  -- 'PF' / 'PJ' / null. Aceita o campo solto ou dentro de `advertiser`, porque
  -- o extrator do Chaves na Mão grava no topo e o da Grupo Zap aninha tudo.
  select case upper(btrim(coalesce(
           p_dados->>'advertiser_type',
           p_dados->'advertiser'->>'type',
           '')))
         when 'PF' then 'PF'
         when 'PJ' then 'PJ'
         else null
         end;
$$;

create or replace function public.fn_captacao_anunciante_tem_logo(p_dados jsonb)
returns boolean
language sql
immutable
as $$
  -- Qualquer chave cujo NOME contenha "logo", com valor não vazio, em
  -- `advertiser` ou na raiz. Ver o cabeçalho: chave fixa quebraria calada.
  select exists (
    select 1
      from jsonb_each_text(
             case when jsonb_typeof(coalesce(p_dados->'advertiser', p_dados)) = 'object'
                  then coalesce(p_dados->'advertiser', p_dados)
                  else '{}'::jsonb end) as kv(k, v)
     where kv.k ~* 'logo'
       and btrim(coalesce(kv.v, '')) not in ('', 'null', 'false')
  );
$$;

-- Diagnóstico para calibrar contra a base real ANTES de confiar no sinal 2.
-- Devolve quantos prospects têm cada chave de logo, por fonte. Se vier tudo
-- zero, o campo não está sendo entregue nessa coleta e o sinal é inerte — não
-- quebra nada, mas também não ajuda, e é melhor saber disso por medida do que
-- por suposição.
create or replace function public.fn_captacao_diagnostico_anunciante()
returns table(fonte text, total bigint, com_tipo_pf bigint, com_tipo_pj bigint,
              com_logo bigint, chaves_de_logo text)
language sql
stable
as $$
  select p.fonte,
         count(*) as total,
         count(*) filter (where public.fn_captacao_anunciante_tipo(p.dados) = 'PF') as com_tipo_pf,
         count(*) filter (where public.fn_captacao_anunciante_tipo(p.dados) = 'PJ') as com_tipo_pj,
         count(*) filter (where public.fn_captacao_anunciante_tem_logo(p.dados))    as com_logo,
         coalesce(string_agg(distinct k.k, ', ' order by k.k), '—') as chaves_de_logo
    from public.captacao_prospects p
    left join lateral (
      select kv.k
        from jsonb_each_text(
               case when jsonb_typeof(coalesce(p.dados->'advertiser', p.dados)) = 'object'
                    then coalesce(p.dados->'advertiser', p.dados)
                    else '{}'::jsonb end) as kv(k, v)
       where kv.k ~* 'logo'
    ) k on true
   group by p.fonte
   order by p.fonte;
$$;

-- ---------------------------------------------------------------------------
-- a régua, com os dois sinais no lugar certo da ordem
-- ---------------------------------------------------------------------------
-- A ordem é por FORÇA DE EVIDÊNCIA, não por conveniência:
--
--   1. telefone impossível        -> descartar
--   2. PJ declarado pelo portal   -> empresa   (o portal afirmando, não eu inferindo)
--   3. CRECI no anúncio           -> empresa
--   4. logo de anunciante         -> empresa   (sinal novo)
--   5. nome com marca de empresa  -> empresa
--   6. telefone em N anúncios     -> empresa
--   7. PF declarado + 1 anúncio   -> PARTICULAR (o resgate)
--   8. telefone no limite         -> indefinido
--   9. nome com 2+ palavras       -> particular
--  10. resto                      -> indefinido
--
-- O resgate (7) fica DEPOIS da contagem de telefone de propósito: corretor
-- autônomo é pessoa física de verdade, e o que o denuncia não é o cadastro, é
-- o mesmo número em catorze anúncios. PF com carteira continua sendo carteira.

-- Os DOIS drops são obrigatórios, e o segundo é o que quase escapou.
--
-- A assinatura nova tem dois parâmetros com default. Deixar a de UM argumento
-- viva ao lado dela faz `fn_captacao_classificar(4)` — a chamada que o pg_cron
-- e `fn_captacao_preparar` usam — virar AMBÍGUA: o Postgres responde
-- "function public.fn_captacao_classificar(integer) is not unique" e a rotina
-- de captação para. Medido aqui em 14/09, aplicando a migração sobre a régua
-- de 09/09; foi o teste que pegou, não a leitura.
drop function if exists public.fn_captacao_classificar();
drop function if exists public.fn_captacao_classificar(int);

create or replace function public.fn_captacao_classificar(
  p_limite_carteira int default 4,
  p_teto_logo numeric default 0.60   -- acima disso, logo não discrimina nada
)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v jsonb;
  re_empresa text := '(?i)(ltda|\ys[./]?a\.?$|eireli|\yme\y|\ymei\y|\yepp\y|im[oó]v[eé]|imobili|corretor|corretag|'
                  || 'consultor|assessor|administrador|construtor|construç|incorporad|empreendim|urbanism|'
                  || 'loteador|realty|broker|invest|neg[oó]cio|patrim|holding|participa|\yspe\y|'
                  || 're/?max|century|coelho da fonseca|\ylopes\y|bossa|keller|engel|'
                  || 'imobili[aá]ria|\ygrupo\y|\ycia\y|& cia|assoc|servi[çc]os|solu[çc][oõ]es|'
                  || 'engenharia|arquitet|\yhome\y|\yhomes\y|\yhouse\y|\yprime\y|\yelite\y|\yvip\y|'
                  || '\ymaster\y|\yplan\y|\yplanej\y|\yventures?\y|\ycorp\y|\ygroup\y)';
  re_fone_falso text := '^\d{2}(\d)\1{7,}$';
  v_lim int := greatest(coalesce(p_limite_carteira, 4), 2);
  v_share_logo numeric;
  v_usa_logo boolean;
begin
  -- TRAVA DO SINAL DE LOGO, e ela existe por um modo de falha concreto.
  --
  -- O sinal vale porque logo é raro entre donos. Se o portal passar a devolver
  -- logo (ou um avatar padrão) para TODO anunciante, a regra deixa de separar
  -- nada e marca a base inteira como empresa — zerando a oferta de particular,
  -- que é justamente o problema que este arquivo veio resolver. Falharia para
  -- o lado pior, e calada.
  --
  -- Então o sinal só vale enquanto for minoria. Acima do teto ele se desliga
  -- sozinho, e o retorno diz que desligou — quem lê o JSON vê, em vez de
  -- descobrir pela fila vazia.
  select coalesce(avg(case when public.fn_captacao_anunciante_tem_logo(dados)
                           then 1 else 0 end), 0)
    into v_share_logo
    from public.captacao_prospects
   where telefone is not null;
  v_usa_logo := v_share_logo <= coalesce(p_teto_logo, 0.60);

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
      when public.fn_captacao_anunciante_tipo(p.dados) = 'PJ'      then 'empresa'
      when p.tem_creci                                             then 'empresa'
      when v_usa_logo and public.fn_captacao_anunciante_tem_logo(p.dados)
                                                                   then 'empresa'
      when coalesce(p.anunciante,'') ~ re_empresa                  then 'empresa'
      when coalesce(p.anuncios_no_telefone, 1) >= v_lim            then 'empresa'
      when public.fn_captacao_anunciante_tipo(p.dados) = 'PF'
       and coalesce(p.anuncios_no_telefone, 1) = 1                 then 'particular'
      when coalesce(p.anuncios_no_telefone, 1) = v_lim - 1         then 'indefinido'
      when array_length(regexp_split_to_array(btrim(coalesce(p.anunciante,'')), '\s+'), 1) >= 2
                                                                   then 'particular'
      else 'indefinido'
    end,
    motivo_perfil = case
      when p.telefone is null or p.telefone ~ re_fone_falso then 'telefone ausente ou genérico'
      when public.fn_captacao_anunciante_tipo(p.dados) = 'PJ' then 'portal declara pessoa jurídica'
      when p.tem_creci then 'CRECI informado no anúncio'
      when v_usa_logo and public.fn_captacao_anunciante_tem_logo(p.dados)
        then 'anunciante tem logo cadastrado — perfil de imobiliária'
      when coalesce(p.anunciante,'') ~ re_empresa then 'nome com marca de empresa'
      when coalesce(p.anuncios_no_telefone, 1) >= v_lim
        then 'mesmo telefone em ' || p.anuncios_no_telefone || ' anúncios — carteira, não dono'
      when public.fn_captacao_anunciante_tipo(p.dados) = 'PF'
       and coalesce(p.anuncios_no_telefone, 1) = 1
        then 'portal declara pessoa física, telefone em 1 anúncio'
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
    'limite_carteira', v_lim,
    'logo_share', round(v_share_logo, 4),
    'logo_em_uso', v_usa_logo) into v
  from public.captacao_prospects;
  return v;
end;
$$;
