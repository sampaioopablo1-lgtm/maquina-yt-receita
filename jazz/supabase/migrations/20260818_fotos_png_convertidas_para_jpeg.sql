-- 18/08/2026 — Fotos PNG disfarçadas de .jpg convertidas para JPEG real.
--
-- Achado da auditoria de resolução: 279 fotos publicadas têm assinatura PNG
-- (89 50 4E 47) apesar da extensão .jpg. A diretriz do portal é explícita:
-- "Serão importados somente imagens no formato jpg" — essas fotos são
-- descartadas em silêncio na importação. É a causa dos "Erros de upload de
-- imagem" do painel e de parte do gap de Imagens: o 41569, por exemplo, tem
-- as 42 fotos em PNG — o anúncio está sem NENHUMA imagem no portal.
--
-- Correção: cada PNG é convertido para JPEG de verdade e hospedado no bucket
-- público fotos-portal; esta tabela mapeia URL original → URL convertida, e
-- o cron troca as URLs dentro de dados_normalizados.fotos. Mesmo padrão
-- autocurativo das duas camadas do tour: se o sync do Vista reconstruir o
-- JSON com a URL original, a troca reaplica em até 10 minutos.
--
-- A troca de URL também força o portal a reimportar (a spec diz que URL nova
-- = novo download), que é exatamente o que queremos.

insert into storage.buckets (id, name, public) values ('fotos-portal','fotos-portal', true)
on conflict (id) do nothing;

create table if not exists public.feed_foto_convertida (
  url_original text primary key,
  codigo_vista text,
  url_jpeg text not null,
  criado_em timestamptz not null default now()
);

create index if not exists feed_foto_convertida_codigo on public.feed_foto_convertida (codigo_vista);

alter table public.feed_foto_convertida enable row level security;
-- Sem policy: só service_role.

create or replace function public.fn_trocar_fotos_convertidas()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare v_n int := 0;
begin
  with alvo as (
    select fp.id,
           (select jsonb_agg(coalesce(c.url_jpeg, f.u) order by f.ord)
              from jsonb_array_elements_text(fp.dados_normalizados->'fotos')
                     with ordinality f(u, ord)
              left join public.feed_foto_convertida c on c.url_original = f.u
           ) as fotos_novas
    from public.feed_properties fp
    where fp.ativo
      and exists (
        select 1 from jsonb_array_elements_text(fp.dados_normalizados->'fotos') f(u)
        join public.feed_foto_convertida c on c.url_original = f.u)
  ), upd as (
    update public.feed_properties fp
       set dados_normalizados = jsonb_set(fp.dados_normalizados, '{fotos}', a.fotos_novas),
           updated_at = now()
      from alvo a
     where fp.id = a.id
       and fp.dados_normalizados->'fotos' is distinct from a.fotos_novas
    returning 1
  )
  select count(*) from upd into v_n;
  return jsonb_build_object('ok', true, 'anuncios_com_fotos_trocadas', v_n);
end;
$$;

revoke all on function public.fn_trocar_fotos_convertidas() from public, anon, authenticated;

select cron.schedule('feed-trocar-fotos-convertidas', '8-58/10 * * * *',
  $$select public.fn_trocar_fotos_convertidas();$$);
