-- 13/08/2026 — calibrar a régua de fotos pela meta real do portal.
--
-- O relatório de qualidade mostrou Imagens em 89%, com 330 anúncios
-- incompletos entre os 2.902 publicados. A distribuição do acervo elegível
-- explica o número: 173 anúncios têm de 7 a 9 fotos e 150 têm de 10 a 11 —
-- juntos, 323. A meta do portal para pontuar Imagens é, portanto, **12
-- fotos**, e não as 20 que o material de nota máxima sugeria.
--
-- Com 12 como piso sobram 2.996 anúncios elegíveis, contra 3.000 vagas do
-- contrato. Trocar 4 vagas por 20 pontos cheios na categoria é vantajoso:
-- os anúncios que saem são justamente os que o portal já não pontuava.
--
-- A régua fica aqui, no banco, e não na Edge Function, por dois motivos:
-- ajustar não exige republicar 48 KB de bundle, e se a calibração estiver
-- errada por uma foto (13 em vez de 12), o conserto é trocar o parâmetro do
-- cron. O gerador de XML já respeita `feed_property_portal_publicacao`.

create or replace function public.fn_gate_fotos_portal(p_min int default 12)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_bloqueados int := 0;
  v_liberados int := 0;
  v_min int := greatest(1, p_min);
begin
  create temp table _fotos on commit drop as
  select fp.id,
         (select count(*) from jsonb_array_elements_text(coalesce(fp.dados_normalizados->'fotos','[]'::jsonb)) f
           where f ~* '^https?://.+\.(jpe?g|png|webp)(\?|$)') as fotos
  from public.feed_properties fp
  where fp.ativo;

  insert into public.feed_property_portal_publicacao (property_id, portal, habilitado, motivo, atualizado_em)
  select id, 'vrsync_rede', false, 'fotos_abaixo_da_meta', now()
  from _fotos where fotos < v_min
  on conflict (property_id, portal) do update
    set habilitado = false, motivo = 'fotos_abaixo_da_meta', atualizado_em = now()
    where public.feed_property_portal_publicacao.habilitado
      and coalesce(public.feed_property_portal_publicacao.motivo, 'fotos_abaixo_da_meta') = 'fotos_abaixo_da_meta';
  get diagnostics v_bloqueados = row_count;

  -- Ganhou fotos no Vista: volta pro ar.
  update public.feed_property_portal_publicacao p
     set habilitado = true, atualizado_em = now()
    from _fotos f
   where p.property_id = f.id
     and p.portal = 'vrsync_rede'
     and not p.habilitado
     and p.motivo = 'fotos_abaixo_da_meta'
     and f.fotos >= v_min;
  get diagnostics v_liberados = row_count;

  return jsonb_build_object('ok', true, 'minimo', v_min,
                            'bloqueados', v_bloqueados, 'liberados', v_liberados,
                            'no_ar_estimado', (select count(*) from _fotos where fotos >= v_min));
end;
$$;

revoke all on function public.fn_gate_fotos_portal(int) from public, anon, authenticated;

select cron.schedule('feed-gate-fotos', '44 * * * *',
                     $cron$select public.fn_gate_fotos_portal(12);$cron$);
