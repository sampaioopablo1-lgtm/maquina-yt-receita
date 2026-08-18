-- 18/08/2026 — Enriquecimento das descrições finas via Gemini, com trava
-- anti-invenção verificável.
--
-- O relatório mantém Descrição em 96% (108 anúncios incompletos). Medição no
-- acervo publicado: 90 descrições têm menos de 700 caracteres — texto fino
-- demais para "contemplar todas as especificações". A prosa é gerada pelo
-- Gemini a partir EXCLUSIVAMENTE dos campos do cadastro, e a colheita só
-- aceita o texto se TODO número presente na saída existir também na entrada
-- — número inventado (metragem, valor, quantidade) reprova automaticamente.
-- Depois da aceitação o texto passa pela mesma esteira de todos: higiene +
-- ficha técnica + teto de 3.000 (cron feed-descricao-completa).
--
-- Modelo: gemini-3.6-flash. O primeiro lote usou gemini-2.5-flash e levou
-- 404 ("no longer available to new users") — a própria resposta da API
-- indicou o modelo novo.
--
-- A chave já vivia no vault do projeto; copiada para integracao_credenciais
-- (mesma proteção: RLS sem policy, só service_role), porque o pg_net roda no
-- banco e o vault não é acessível de Edge Function.

insert into public.integracao_credenciais (chave, valor)
select 'gemini_api_key', decrypted_secret from vault.decrypted_secrets where name='gemini_api_key'
on conflict (chave) do nothing;

create table if not exists public.feed_descricao_rica (
  codigo_vista text primary key,
  req_id bigint,
  status text not null default 'pedida'
    check (status in ('pedida','aceita','reprovada','erro')),
  motivo text,
  pedida_em timestamptz not null default now()
);

alter table public.feed_descricao_rica enable row level security;

create or replace function public.fn_descricao_rica_pedir(p_lote int default 30)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_key text;
  r record;
  v_req bigint;
  v_n int := 0;
begin
  select valor into v_key from public.integracao_credenciais where chave='gemini_api_key';
  if v_key is null then return jsonb_build_object('ok', false, 'motivo', 'sem chave'); end if;

  for r in
    select fp.codigo_original cod, fp.dados_normalizados d,
           coalesce(a.descricao_otimizada, fp.dados_normalizados->>'descricao','') atual
    from public.feed_properties fp
    left join public.feed_property_portal_publicacao p on p.property_id=fp.id and p.portal='vrsync_rede'
    left join public.feed_ai_content a on a.property_id=fp.id and a.ativo
    where fp.ativo and coalesce(p.habilitado,true)
      and length(coalesce(a.descricao_otimizada, fp.dados_normalizados->>'descricao','')) < 700
      and not exists (select 1 from public.feed_descricao_rica q
                       where q.codigo_vista = fp.codigo_original
                         and q.status in ('pedida','aceita'))
    limit greatest(1, p_lote)
  loop
    select net.http_post(
      url := 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key=' || v_key,
      headers := '{"Content-Type":"application/json"}'::jsonb,
      body := jsonb_build_object('contents', jsonb_build_array(jsonb_build_object(
        'parts', jsonb_build_array(jsonb_build_object('text',
          'Escreva uma descrição imobiliária em português para anúncio em portal, com 1100 a 1600 caracteres, em 3 a 4 parágrafos corridos.' ||
          E'\nREGRAS OBRIGATÓRIAS:' ||
          E'\n- Use EXCLUSIVAMENTE as informações do JSON abaixo; não invente nenhuma característica, medida, valor ou detalhe.' ||
          E'\n- NÃO escreva nenhum número que não esteja no JSON.' ||
          E'\n- Sem telefone, e-mail, CRECI, nome de pessoa, colchetes ou emojis.' ||
          E'\n- Não faça lista de tópicos: a ficha técnica é acrescentada automaticamente depois.' ||
          E'\n- Termine convidando a agendar uma visita com a Jazz Imobiliária.' ||
          E'\nResponda SOMENTE com o texto da descrição.' ||
          E'\nJSON do imóvel: ' ||
          (select jsonb_build_object(
            'tipo', r.d->>'tipo', 'bairro', r.d->>'bairro', 'cidade', r.d->>'cidade',
            'finalidade', r.d->>'finalidade', 'dormitorios', r.d->>'dormitorios',
            'suites', r.d->>'suites', 'banheiros', r.d->>'banheiros', 'vagas', r.d->>'vagas',
            'area_util_m2', r.d->>'area_util', 'area_total_m2', r.d->>'area_total',
            'empreendimento', r.d->>'empreendimento', 'ano_construcao', r.d->>'ano_construcao',
            'caracteristicas', (select coalesce(jsonb_agg(m.ptbr), '[]'::jsonb)
                                 from jsonb_array_elements_text(coalesce(r.d->'caracteristicas','[]'::jsonb)) c
                                 join public.feed_caracteristica_ptbr m on m.codigo = c),
            'descricao_atual', left(r.atual, 800)
          )::text)
        ))))),
      timeout_milliseconds := 120000
    ) into v_req;

    insert into public.feed_descricao_rica (codigo_vista, req_id, status)
    values (r.cod, v_req, 'pedida')
    on conflict (codigo_vista) do update set req_id = excluded.req_id, status = 'pedida', pedida_em = now();
    v_n := v_n + 1;
  end loop;

  return jsonb_build_object('ok', true, 'pedidas', v_n);
end;
$$;

revoke all on function public.fn_descricao_rica_pedir(int) from public, anon, authenticated;

create or replace function public.fn_descricao_rica_colher()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  q record;
  v_texto text;
  v_final text;
  v_nums_saida text[];
  v_entrada text;
  v_aceitas int := 0;
  v_reprovadas int := 0;
begin
  for q in
    select fr.codigo_vista, fr.req_id, r.content, r.status_code, fp.id fp_id, fp.dados_normalizados d
    from public.feed_descricao_rica fr
    join net._http_response r on r.id = fr.req_id
    join public.feed_properties fp on fp.codigo_original = fr.codigo_vista
    where fr.status = 'pedida'
  loop
    begin
      if q.status_code <> 200 then
        update public.feed_descricao_rica set status='erro', motivo='http '||q.status_code where codigo_vista=q.codigo_vista;
        continue;
      end if;

      v_texto := btrim(q.content::jsonb #>> '{candidates,0,content,parts,0,text}');
      v_texto := public.fn_higienizar_descricao(v_texto);

      -- Trava anti-invenção: todo número da saída precisa existir na entrada
      -- (campos do cadastro). Ano/valor/metragem inventado reprova.
      v_entrada := q.d::text;
      select coalesce(array_agg(distinct m[1]), '{}') into v_nums_saida
        from regexp_matches(v_texto, '([0-9]+)', 'g') m;
      if exists (select 1 from unnest(v_nums_saida) n
                  where length(n) > 1 and position(n in v_entrada) = 0) then
        update public.feed_descricao_rica set status='reprovada', motivo='numero inventado' where codigo_vista=q.codigo_vista;
        v_reprovadas := v_reprovadas + 1;
        continue;
      end if;

      if v_texto is null or length(v_texto) < 700 or length(v_texto) > 2400
         or v_texto ~ '\[' or v_texto ~* 'creci' then
        update public.feed_descricao_rica set status='reprovada', motivo='fora do padrao' where codigo_vista=q.codigo_vista;
        v_reprovadas := v_reprovadas + 1;
        continue;
      end if;

      v_final := public.fn_descricao_ficha(v_texto, q.d);

      insert into public.feed_ai_content
        (property_id, versao, estrategia, descricao_original, descricao_otimizada, ativo, modelo)
      values (q.fp_id, 1, 'gemini_rica', q.d->>'descricao', v_final, true, 'gemini-3.6-flash')
      on conflict (property_id) where ativo
      do update set descricao_otimizada = excluded.descricao_otimizada,
                    estrategia = 'gemini_rica', modelo = 'gemini-3.6-flash', updated_at = now();

      update public.feed_descricao_rica set status='aceita', motivo=null where codigo_vista=q.codigo_vista;
      v_aceitas := v_aceitas + 1;
    exception when others then
      update public.feed_descricao_rica set status='erro', motivo=left(sqlerrm,200) where codigo_vista=q.codigo_vista;
    end;
  end loop;

  return jsonb_build_object('ok', true, 'aceitas', v_aceitas, 'reprovadas', v_reprovadas);
end;
$$;

revoke all on function public.fn_descricao_rica_colher() from public, anon, authenticated;

-- Pede e colhe em ciclos de 15 min até a fila secar (o alvo <700 encolhe a
-- cada aceitação; reprovada volta a ser elegível no pedido seguinte).
select cron.schedule('descricao-rica-pedir', '1,16,31,46 * * * *',
  $$select public.fn_descricao_rica_pedir(30);$$);
select cron.schedule('descricao-rica-colher', '6,21,36,51 * * * *',
  $$select public.fn_descricao_rica_colher();$$);
