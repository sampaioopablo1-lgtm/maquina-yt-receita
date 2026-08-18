-- 13/08/2026 — parar de mandar o mesmo imóvel duas vezes.
--
-- O painel do Zap mostrou 176 anúncios bloqueados, e a razão da quase
-- totalidade é "este anúncio está duplicado em sua conta". São fichas
-- diferentes no Vista descrevendo o mesmo imóvel: 46824, 46828 e 46830 são
-- todos Rua Caxambu, Praia Grande, 55 m², 2 dormitórios, entre R$ 339.999 e
-- R$ 360.000; 46677 e 46687 são a mesma Helena Steimberg de 59 m².
--
-- Bloqueio no portal não é só desperdício de vaga: o anúncio ocupa slot do
-- contrato sem aparecer pra ninguém. Medido no acervo publicável, 188 fichas
-- eram excedentes de grupos duplicados — número que casa com os 176 do painel.
--
-- A chave usa logradouro + cidade + bairro + área + dormitórios + banheiros +
-- vagas + finalidade. Preço fica de fora de propósito: o portal considerou
-- duplicados anúncios com R$ 339.999 e R$ 360.000, então incluir preço faria
-- o feed mandar todos e o portal bloquear todos — pior que escolher um.
--
-- RESSALVA IMPORTANTE, e ela é de negócio, não técnica: no condomínio Recanto
-- Santa Bárbara existem 11 lotes distintos de 1.000 m², com preços de R$ 352
-- mil a R$ 596 mil. São terrenos reais e diferentes, e esta regra publica só
-- um deles. Não é acerto — é o menor prejuízo, porque o portal já bloqueava os
-- outros de qualquer jeito e cada bloqueado consumia uma vaga do contrato. A
-- correção de verdade é cadastrar quadra/lote no Vista, no logradouro ou no
-- título, dando ao portal o que distingue um do outro.
--
-- Sobrevive o mais completo do grupo: mais fotos, depois ficha mais rica,
-- depois o código mais recente como desempate estável. Os outros saem com
-- `motivo = 'duplicado_no_portal'`, que não se mistura com o bloqueio do gate
-- de XML — cada regra só religa o que ela mesma desligou.

create or replace function public.fn_dedup_feed_portal()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_bloqueados int := 0;
  v_liberados int := 0;
  v_grupos int := 0;
begin
  create temp table _dedup on commit drop as
  with pub as (
    select fp.id, fp.codigo_original as cod, fp.dados_normalizados d,
      (select count(*) from jsonb_array_elements_text(coalesce(fp.dados_normalizados->'fotos','[]'::jsonb)) f
        where f ~* '^https?://.+\.(jpe?g|png|webp)(\?|$)') as fotos
    from public.feed_properties fp
    where fp.ativo
      and coalesce(nullif(fp.dados_normalizados->>'endereco',''), '') <> ''
  ), chave as (
    select id, cod, fotos, d,
      lower(regexp_replace(translate(
          coalesce(d->>'endereco','')||'|'||coalesce(d->>'cidade','')||'|'||coalesce(d->>'bairro',''),
          'áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ','aaaaeeiooouucAAAAEEIOOOUUC'),'[^a-z0-9|]','','g'))
        ||'|'|| round(coalesce(nullif((d->>'area_util')::numeric,0), nullif((d->>'area_total')::numeric,0), 0))
        ||'|'|| coalesce(d->>'dormitorios','')
        ||'|'|| coalesce(d->>'banheiros','')
        ||'|'|| coalesce(d->>'vagas','')
        ||'|'|| coalesce(d->>'finalidade','') as k
    from pub
  )
  select id, cod, k, fotos,
         row_number() over (
           partition by k
           order by fotos desc,
                    (coalesce(d->>'cep','') <> '')::int desc,
                    (coalesce(d->>'descricao','') <> '')::int desc,
                    jsonb_array_length(coalesce(d->'caracteristicas','[]'::jsonb)) desc,
                    cod desc
         ) as posicao,
         count(*) over (partition by k) as no_grupo
  from chave;

  select count(distinct k) into v_grupos from _dedup where no_grupo > 1;

  -- Excedente do grupo sai do ar.
  insert into public.feed_property_portal_publicacao (property_id, portal, habilitado, motivo, atualizado_em)
  select d.id, 'vrsync_rede', false, 'duplicado_no_portal', now()
  from _dedup d where d.posicao > 1
  on conflict (property_id, portal) do update
    set habilitado = false, motivo = 'duplicado_no_portal', atualizado_em = now()
    where public.feed_property_portal_publicacao.habilitado
      and coalesce(public.feed_property_portal_publicacao.motivo, 'duplicado_no_portal') = 'duplicado_no_portal';
  get diagnostics v_bloqueados = row_count;

  -- Deixou de ser duplicado (o irmão saiu do acervo): volta pro ar.
  update public.feed_property_portal_publicacao p
     set habilitado = true, atualizado_em = now()
    from _dedup d
   where p.property_id = d.id
     and p.portal = 'vrsync_rede'
     and not p.habilitado
     and p.motivo = 'duplicado_no_portal'
     and d.posicao = 1;
  get diagnostics v_liberados = row_count;

  return jsonb_build_object('ok', true, 'grupos_duplicados', v_grupos,
                            'bloqueados', v_bloqueados, 'liberados', v_liberados);
end;
$$;

revoke all on function public.fn_dedup_feed_portal() from public, anon, authenticated;

select cron.schedule('feed-dedup-portal', '38 * * * *',
                     $cron$select public.fn_dedup_feed_portal();$cron$);

-- Bloqueios que o portal aplicou por motivo próprio, informados no painel.
insert into public.feed_property_portal_publicacao (property_id, portal, habilitado, motivo, atualizado_em)
select fp.id, 'vrsync_rede', false,
       case fp.codigo_original when '38296' then 'bloqueado_portal_lancamento'
                               else 'bloqueado_portal_regulamento' end, now()
from public.feed_properties fp where fp.codigo_original in ('38296','44956')
on conflict (property_id, portal) do update
  set habilitado = false, motivo = excluded.motivo, atualizado_em = now();
