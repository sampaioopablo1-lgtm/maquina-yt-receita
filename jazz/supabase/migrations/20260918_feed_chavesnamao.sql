-- 18/09/2026 — segundo portal: Chaves na Mão.
--
-- Até aqui o acervo saía num formato só, o VRSync do Grupo OLX (Zap/VivaReal/
-- OLX). O Chaves na Mão não lê VRSync: tem padrão próprio, documentado pelo
-- portal — raiz `<Document>`, tags em minúsculo, todas presentes mesmo vazias,
-- e leitura de uma URL pública UMA vez por dia.
--
-- O que esta migração faz é só a infraestrutura em volta do gerador (a Edge
-- Function `chavesnamao-feed`): onde o arquivo mora e quando ele é gerado.
--
-- BUCKET SEPARADO, DE PROPÓSITO. O arquivo NÃO vai para `feeds-precomputados`,
-- que hoje guarda o `vrsync.xml`. Motivo concreto: `fn_vigia_feed_auditar()`
-- descobre a idade do XML com
--     select updated_at from storage.objects where bucket_id='feeds-precomputados' limit 1
-- — sem filtro de nome. Um segundo objeto no mesmo bucket faria o vigia do
-- feed do Zap passar a ler, de vez em quando, a data do arquivo do outro
-- portal, e auditoria que mede a coisa errada é pior que auditoria nenhuma.
-- Corrigir aquela consulta (fixar `name = 'vrsync.xml'`) é o certo, mas exige
-- reescrever a função inteira contra o estado de produção; enquanto isso não
-- for conferido em produção, bucket separado resolve sem tocar no que está no
-- ar. O bucket é público porque o portal precisa baixar o arquivo sem
-- credencial ("o cliente deverá disponibilizar uma URL na internet").
--
-- CADÊNCIA. Duas vezes por dia, e não de 10 em 10 minutos como o VRSync. O
-- portal lê uma vez por dia, e o incidente de 19/08 (CPU da instância estourada
-- por precompute caro demais, feed fora do ar por horas) é caro o bastante para
-- não repetir a dose com um segundo arquivo. As 06:40 e 18:40 UTC são 03:40 e
-- 15:40 em Brasília, fora do pico do sync e defasadas dos vigias horários.

insert into storage.buckets (id, name, public)
values ('feeds-portais', 'feeds-portais', true)
on conflict (id) do update set public = true;

-- URL que vai para o portal:
--   https://cscczluzpblzhvojxanp.supabase.co/storage/v1/object/public/feeds-portais/chavesnamao.xml

select cron.unschedule('feed-precomputar-chavesnamao')
where exists (select 1 from cron.job where jobname = 'feed-precomputar-chavesnamao');

select cron.schedule('feed-precomputar-chavesnamao', '40 6,18 * * *', $cron$
  select net.http_post(
    url := 'https://cscczluzpblzhvojxanp.supabase.co/functions/v1/chavesnamao-feed',
    headers := jsonb_build_object(
      'apikey','sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
      'Authorization','Bearer sb_publishable_9E12YLZmV_zq1yN64wUBoQ_ZADvi5JW',
      'Content-Type','application/json'),
    body := '{"acao":"precomputar"}'::jsonb,
    timeout_milliseconds := 180000)
$cron$);

-- Bloqueio por portal: a tabela de publicação já é por portal (`portal` é
-- texto livre), então basta passar a usar a chave 'chavesnamao' para tirar um
-- imóvel só deste feed. O gerador respeita, além dela, os bloqueios de
-- `vrsync_rede` que falam do imóvel (ausente do XML do Vista, ficha duplicada)
-- e ignora `fotos_abaixo_da_meta`, que é régua de nota do Grupo OLX.
--
-- Exemplo (tirar um imóvel só do Chaves na Mão):
--   insert into public.feed_property_portal_publicacao (property_id, portal, habilitado, motivo, atualizado_em)
--   select id, 'chavesnamao', false, 'pedido_do_proprietario', now()
--     from public.feed_properties where codigo_original = '46824'
--   on conflict (property_id, portal) do update
--     set habilitado = false, motivo = excluded.motivo, atualizado_em = now();
