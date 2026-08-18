-- 18/08/2026 — Vídeo próprio por imóvel no campo de vídeo do portal.
--
-- Diretriz oficial VRSync (developers.grupozap.com, elemento Listing/Media):
--   "Somente serão processados os vídeos armazenados no Youtube;
--    Somente será recebido um vídeo por imóvel."
--
-- Por isso esta tabela tem DUAS colunas de URL: o mp4 que a fábrica gera
-- (bucket videos-imoveis) e o link do YouTube depois de publicado no canal.
-- Só o link do YouTube vai ao feed — mp4 direto o portal ignora.
--
-- E por isso o vídeo NÃO entra em <VirtualTourLink>: aquele campo exige
-- página contendo apenas tour; página de fotos/vídeo ali já foi testada em
-- 193 anúncios e pontuou 0%. Vídeo é vídeo, tour é tour.

create table if not exists public.feed_video_imovel (
  codigo_vista text primary key,
  mp4_url text,
  youtube_url text,
  status text not null default 'renderizado'
    check (status in ('renderizado','no_youtube','no_feed','erro')),
  erro text,
  criado_em timestamptz not null default now(),
  publicado_em timestamptz
);

alter table public.feed_video_imovel enable row level security;
-- Sem policy: só service_role, mesmo padrão das demais tabelas de feed.

-- Leva o link do YouTube ao campo que o gerador de XML já lê.
-- Nunca sobrescreve vídeo próprio que já exista no Vista — só preenche o
-- vazio ou substitui o institucional genérico.
create or replace function public.fn_video_imovel_publicar_no_feed()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_n int := 0;
  v_institucional text := 'https://www.youtube.com/watch?v=DlYDTuoHf3k';
begin
  update public.vista_imoveis_log v
     set video = t.youtube_url
    from public.feed_video_imovel t
   where t.codigo_vista = v.codigo_vista
     and t.youtube_url ~* '^https://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[A-Za-z0-9_\-]{6,}'
     and v.ativo_vista
     and coalesce(v.video,'') is distinct from t.youtube_url
     and (coalesce(v.video,'') = '' or v.video = v_institucional);
  get diagnostics v_n = row_count;

  update public.feed_video_imovel t
     set status = 'no_feed', publicado_em = now()
    from public.vista_imoveis_log v
   where v.codigo_vista = t.codigo_vista
     and v.video = t.youtube_url
     and t.status <> 'no_feed';

  return jsonb_build_object('ok', true, 'publicados_no_feed', v_n);
end;
$$;

revoke all on function public.fn_video_imovel_publicar_no_feed() from public, anon, authenticated;

select cron.schedule('video-imovel-publicar-no-feed', '7-57/10 * * * *',
  $$select public.fn_video_imovel_publicar_no_feed();$$);

-- Registro do piloto: mp4 pronto, aguardando o link do YouTube.
insert into public.feed_video_imovel (codigo_vista, mp4_url, status)
values ('40346',
  'https://cscczluzpblzhvojxanp.supabase.co/storage/v1/object/public/videos-imoveis/40346.mp4',
  'renderizado')
on conflict (codigo_vista) do update set mp4_url = excluded.mp4_url;
