-- 18/08/2026 — Auditoria de resolução das fotos publicadas.
--
-- A categoria Imagens vale 20 pontos e está em 86% (414 anúncios incompletos).
-- Até aqui só se media QUANTIDADE de foto. A amostragem de 147 fotos reais
-- mostrou que o problema tem uma segunda metade, invisível na contagem:
--
--   largura mínima 245 · mediana 1052 · máxima 4032
--   1 foto abaixo do mínimo absoluto do portal (300x300)
--   95 de 147 (65%) abaixo do recomendado de 1024x768
--
-- Três hipóteses de correção em CÓDIGO foram testadas e todas descartadas:
--
--   1. Variante maior no CDN — não existe. O cdn.vistahost.com.br é
--      armazenamento estático puro: tirar o token do nome devolve 403 e
--      `?w=1920` devolve o mesmo arquivo, byte por byte (31.367 bytes).
--   2. Estarmos publicando a miniatura — não estamos. O Vista expõe `Foto` e
--      `FotoPequena` (sufixo `_p`); conferido no imóvel 41020, publicamos
--      `Foto`, a maior das duas.
--   3. Ordem/capa errada — está certa. O Vista manda as fotos numa chave
--      desordenada (20, 13, 1, 2...) com o campo `Ordem` à parte, e o sync
--      respeita `Ordem`/`Destaque`: a capa do 41020 é a marcada como
--      Destaque=Sim, Ordem=1.
--
-- Conclusão honesta: a foto pequena é pequena na origem, subida assim pelo
-- captador. Não há rewrite de URL que resolva. O que dá para fazer é parar de
-- adivinhar e medir todas as 94.856 fotos, para a lista de recaptura apontar
-- exatamente quais anúncios precisam de foto NOVA — e não só de MAIS foto.

create table if not exists public.feed_foto_dimensao (
  url text primary key,
  codigo_vista text,
  largura int,
  altura int,
  medido_em timestamptz not null default now(),
  erro text
);

create index if not exists feed_foto_dimensao_codigo on public.feed_foto_dimensao (codigo_vista);

alter table public.feed_foto_dimensao enable row level security;
-- Sem policy: só service_role. Mesmo padrão das demais tabelas de feed.

-- Fila: fotos publicadas que ainda não foram medidas.
create or replace function public.fn_fotos_a_medir(p_n int default 200)
returns table (codigo text, url text)
language sql security definer set search_path = public as $$
  select fp.codigo_original, u
  from public.feed_properties fp
  left join public.feed_property_portal_publicacao p
         on p.property_id = fp.id and p.portal = 'vrsync_rede',
  lateral jsonb_array_elements_text(coalesce(fp.dados_normalizados->'fotos','[]'::jsonb)) u
  where fp.ativo and coalesce(p.habilitado, true)
    and not exists (select 1 from public.feed_foto_dimensao d where d.url = u)
  limit greatest(1, p_n);
$$;

revoke all on function public.fn_fotos_a_medir(int) from public, anon, authenticated;

-- Lista de recaptura: junta as duas carências numa ordem de prioridade só.
-- Falta de foto e foto pequena são o mesmo trabalho de campo (ir ao imóvel),
-- então precisam sair na mesma lista — senão o captador vai duas vezes ao
-- mesmo endereço.
create or replace view public.v_recaptura_fotos_portal as
with pub as (
  select fp.id, fp.codigo_original,
         jsonb_array_length(coalesce(fp.dados_normalizados->'fotos','[]'::jsonb)) as fotos
  from public.feed_properties fp
  left join public.feed_property_portal_publicacao p
         on p.property_id = fp.id and p.portal = 'vrsync_rede'
  where fp.ativo and coalesce(p.habilitado, true)
), med as (
  select codigo_vista,
         count(*) filter (where largura is not null) medidas,
         count(*) filter (where largura < 1024 or altura < 768) pequenas,
         min(largura) menor_largura
  from public.feed_foto_dimensao group by 1
)
select pb.codigo_original as codigo_vista,
       pb.fotos as fotos_hoje,
       greatest(0, 17 - pb.fotos) as fotos_faltando,
       coalesce(m.pequenas, 0) as fotos_abaixo_1024x768,
       m.menor_largura,
       v.cidade, v.bairro, v.categoria,
       coalesce(v.valor_venda, v.valor_locacao) as valor,
       v.corretor_nome_vista as corretor,
       case when pb.fotos >= 15 and coalesce(m.pequenas,0) = 0 then 'A - falta 1 ou 2 fotos'
            when pb.fotos >= 12 and coalesce(m.pequenas,0) = 0 then 'B - falta 3 a 5 fotos'
            when coalesce(m.pequenas,0) > 0 and pb.fotos >= 17  then 'C - quantidade ok, resolução baixa'
            else 'D - recaptura completa' end as prioridade
from pub pb
left join med m on m.codigo_vista = pb.codigo_original
left join public.vista_imoveis_log v on v.codigo_vista = pb.codigo_original
where pb.fotos < 17 or coalesce(m.pequenas, 0) > 0
order by prioridade, coalesce(v.valor_venda, v.valor_locacao) desc nulls last;

grant select on public.v_recaptura_fotos_portal to authenticated;

-- Varredura. São 94.856 fotos publicadas; a 500 por rodada, de 3 em 3 minutos,
-- a primeira passada leva ~9h e depois o job só encontra foto nova (o que o
-- sync trouxer), custando segundos por rodada.
--
-- O token vem de integracao_credenciais e é lido em tempo de execução, para o
-- valor não ficar gravado no comando do cron nem no repositório.
select cron.schedule('feed-medir-fotos', '*/3 * * * *', $$
  select net.http_post(
    url := 'https://cscczluzpblzhvojxanp.supabase.co/functions/v1/medir-fotos',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'x-auditoria-token', (select valor from public.integracao_credenciais
                             where chave = 'auditoria_interna_token')),
    body := '{"lote":500}'::jsonb,
    timeout_milliseconds := 170000);
$$);

-- Slot do token. O valor NÃO entra no repositório — foi gerado direto no banco:
--
--   insert into public.integracao_credenciais (chave, valor)
--   values ('auditoria_interna_token', encode(gen_random_bytes(24),'hex'))
--   on conflict (chave) do nothing;
