-- 18/08/2026 — Publicação de tour virtual 360 REAL, via VirtualTourEasy.
--
-- Contexto da decisão (importante para quem mexer nisto depois):
--
-- O VirtualTourEasy tem dois caminhos. O de IA (`/api/v1/tours/from-images`
-- e `/from-url`, parâmetro `method: outpaint | reimagine`) converte foto
-- comum em panorama esférico — e para isso precisa INVENTAR ~83% dos pixels,
-- porque uma foto cobre ~60° e a esfera cobre 360°. Isso foi recusado: são
-- cômodos, paredes e janelas que não existem no imóvel anunciado. Além do
-- risco de derrubada do feed inteiro pelo portal, é enganoso com o comprador.
--
-- Esta migração usa o OUTRO caminho: `/api/v1/tours/:uuid/scenes`, que aceita
-- panorama equiretangular JÁ PRONTO e só monta a navegação entre cômodos.
-- Nada é gerado — o insumo é captura real do imóvel real (photosphere de
-- celular, câmera 360, ou vídeo processado por terceiro).
--
-- Por que não mexe no bundle do gerador: auditoria de 18/08 confirmou que os
-- 193 <VirtualTourLink> emitidos hoje saem todos de
-- `vista_imoveis_log.tour_360` (193 de 193 batem). Então basta gravar o link
-- do tour real nesse campo e o XML passa a emiti-lo no próximo ciclo, sem
-- redeploy da Edge Function que gera o feed.

-- Bucket público para os panoramas capturados. Público porque o
-- VirtualTourEasy precisa baixar a imagem pela URL para montar a cena.
insert into storage.buckets (id, name, public)
values ('tours-360', 'tours-360', true)
on conflict (id) do nothing;

create table if not exists public.feed_tour_360 (
  codigo_vista text primary key,
  -- [{ "url": "...", "nome": "Sala" }, ...] na ordem de navegação
  panoramas jsonb not null default '[]'::jsonb,
  vte_tour_uuid text,
  viewer_url text,
  mls_viewer_url text,
  status text not null default 'pendente'
    check (status in ('pendente','publicado','erro','descartado')),
  erro text,
  criado_em timestamptz not null default now(),
  publicado_em timestamptz
);

create index if not exists feed_tour_360_pendentes
  on public.feed_tour_360 (criado_em) where status = 'pendente';

alter table public.feed_tour_360 enable row level security;
-- Sem policy: só service_role (que ignora RLS) lê e escreve. Mesmo padrão da
-- credencial da GeckoAPI.

-- Slot da credencial. O valor NÃO entra no repositório — é inserido à parte,
-- direto no banco, como foi feito com a GeckoAPI.
--
--   insert into public.integracao_credenciais (chave, valor)
--   values ('virtualtoureasy_api_key', 'vte_live_...')
--   on conflict (chave) do update set valor = excluded.valor;

-- Publica no XML: grava o link do tour no campo que o gerador já lê.
-- Só mexe em imóvel que existe e está ativo no espelho, e nunca sobrescreve
-- um tour de terceiro que já esteja lá (só substitui as páginas de fotos do
-- piloto, que apontam para o nosso próprio domínio).
create or replace function public.fn_tour_360_publicar_no_feed()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare v_n int := 0;
begin
  update public.vista_imoveis_log v
     set tour_360 = t.mls_viewer_url
    from public.feed_tour_360 t
   where t.codigo_vista = v.codigo_vista
     and t.status = 'publicado'
     and coalesce(t.mls_viewer_url,'') <> ''
     and v.ativo_vista
     and coalesce(v.tour_360,'') is distinct from t.mls_viewer_url
     and (coalesce(v.tour_360,'') = ''
          or v.tour_360 like '%supabase.co/functions/v1/tour/%');
  get diagnostics v_n = row_count;
  return jsonb_build_object('ok', true, 'publicados_no_feed', v_n);
end;
$$;

revoke all on function public.fn_tour_360_publicar_no_feed() from public, anon, authenticated;

-- De 10 em 10 minutos, logo após o ciclo de precompute do XML.
select cron.schedule('tour-360-publicar-no-feed', '5-55/10 * * * *',
  $$select public.fn_tour_360_publicar_no_feed();$$);
