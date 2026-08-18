-- 12/08/2026 — o espelho passa a ser alimentado pelo XML nativo do Vista.
--
-- POR QUE TROCAR
--
-- Auditoria do XML nativo (26,5 MB, 3.894 fichas, republicado no mesmo dia):
--   * 107.565 imagens — média de 27,6 fotos por ficha, máximo 150, só 5 sem foto
--   * Address e PostalCode preenchidos em 100% das fichas, nenhum vazio
--   * título, tipo, área, dormitórios, banheiros, IPTU e condomínio em 100%
--   * descrição em 99,8%, características em 80%
--   * coordenadas em 45%, ano de construção em 36%
-- Ele também reflete desativação quase em tempo real: caiu de 3.904 para 3.894
-- em poucas horas de observação.
--
-- A API /imoveis/listar, pelo mesmo critério, entrega 500 fichas por execução
-- com o cursor travado, e não distingue "desativado" de "não retornado".
--
-- O QUE A API CONTINUA FAZENDO
--
-- O XML não tem corretor, captador, data de cadastro, nem a carteira que o
-- Vista não exporta pros portais (711 fichas). Isso é matéria-prima do sistema
-- de captação e continua vindo da API — por isso os campos corretor_*,
-- captador_id, match_status, proprietário, vendido_em, data_cadastro e raw
-- NÃO são tocados aqui. Escrever null por cima deles apagaria o trabalho da
-- API em nome de uma fonte que nunca teve esse dado.
--
-- FONTE IMEDIATA
--
-- `feed_properties`, que já é o XML nativo parseado e normalizado pela Edge
-- Function a cada 5 minutos. Reparsear o XML aqui seria manter dois parsers
-- da mesma coisa, livres pra divergir.

create or replace function public.fn_espelhar_xml_no_vista_log()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_fonte int;
  v_atualizados int := 0;
  v_inseridos int := 0;
begin
  select count(*) into v_fonte from public.feed_properties;

  -- Guard: feed vazio ou truncado não vira verdade sobre o acervo.
  if v_fonte < 500 then
    return jsonb_build_object('ok', false, 'motivo', 'feed_properties sem massa', 'fonte', v_fonte);
  end if;

  with fonte as (
    select fp.codigo_original as codigo, fp.dados_normalizados d
    from public.feed_properties fp
  )
  update public.vista_imoveis_log v
     set visto_em         = now(),
         ativo_vista      = true,
         desaparecido_em  = null,
         categoria        = coalesce(nullif(f.d->>'tipo',''), v.categoria),
         finalidade       = coalesce(nullif(f.d->>'finalidade',''), v.finalidade),
         bairro           = coalesce(nullif(f.d->>'bairro',''), v.bairro),
         cidade           = coalesce(nullif(f.d->>'cidade',''), v.cidade),
         endereco         = coalesce(nullif(f.d->>'endereco',''), v.endereco),
         cep              = coalesce(nullif(f.d->>'cep',''), v.cep),
         valor_venda      = coalesce((f.d->>'valor_venda')::numeric, v.valor_venda),
         valor_locacao    = coalesce((f.d->>'valor_locacao')::numeric, v.valor_locacao),
         area_total       = coalesce((f.d->>'area_total')::numeric, v.area_total),
         area_util        = coalesce((f.d->>'area_util')::numeric, v.area_util),
         dormitorios      = coalesce((f.d->>'dormitorios')::numeric::int, v.dormitorios),
         suites           = coalesce((f.d->>'suites')::numeric::int, v.suites),
         vagas            = coalesce((f.d->>'vagas')::numeric::int, v.vagas),
         banheiros        = coalesce((f.d->>'banheiros')::numeric::int, v.banheiros),
         valor_iptu       = coalesce((f.d->>'iptu')::numeric, v.valor_iptu),
         valor_condominio = coalesce((f.d->>'condominio')::numeric, v.valor_condominio),
         ano_construcao   = coalesce((f.d->>'ano_construcao')::numeric::int, v.ano_construcao),
         descricao_web    = coalesce(nullif(f.d->>'descricao',''), v.descricao_web),
         caracteristicas  = coalesce(f.d->'caracteristicas', v.caracteristicas),
         video            = coalesce(nullif(f.d->>'video',''), v.video),
         tour_360         = coalesce(nullif(f.d->>'tour_virtual',''), v.tour_360),
         empreendimento   = coalesce(nullif(f.d->>'empreendimento',''), v.empreendimento),
         latitude         = coalesce((f.d->>'latitude')::numeric, v.latitude),
         longitude        = coalesce((f.d->>'longitude')::numeric, v.longitude),
         foto_destaque    = coalesce(f.d->'fotos'->>0, v.foto_destaque),
         updated_at       = now()
    from fonte f
   where v.codigo_vista = f.codigo;
  get diagnostics v_atualizados = row_count;

  -- Ficha nova no XML que a API ainda não trouxe: entra como pendente de
  -- match, sem captador — quem preenche isso é a API.
  insert into public.vista_imoveis_log (
    codigo_vista, data_cadastro, match_status, ativo_vista, visto_em,
    categoria, finalidade, bairro, cidade, endereco, cep,
    valor_venda, valor_locacao, area_total, area_util,
    dormitorios, suites, vagas, banheiros, descricao_web, foto_destaque)
  select fp.codigo_original, current_date, 'pendente', true, now(),
         nullif(fp.dados_normalizados->>'tipo',''),
         nullif(fp.dados_normalizados->>'finalidade',''),
         nullif(fp.dados_normalizados->>'bairro',''),
         nullif(fp.dados_normalizados->>'cidade',''),
         nullif(fp.dados_normalizados->>'endereco',''),
         nullif(fp.dados_normalizados->>'cep',''),
         (fp.dados_normalizados->>'valor_venda')::numeric,
         (fp.dados_normalizados->>'valor_locacao')::numeric,
         (fp.dados_normalizados->>'area_total')::numeric,
         (fp.dados_normalizados->>'area_util')::numeric,
         (fp.dados_normalizados->>'dormitorios')::numeric::int,
         (fp.dados_normalizados->>'suites')::numeric::int,
         (fp.dados_normalizados->>'vagas')::numeric::int,
         (fp.dados_normalizados->>'banheiros')::numeric::int,
         nullif(fp.dados_normalizados->>'descricao',''),
         fp.dados_normalizados->'fotos'->>0
  from public.feed_properties fp
  where not exists (select 1 from public.vista_imoveis_log v
                    where v.codigo_vista = fp.codigo_original);
  get diagnostics v_inseridos = row_count;

  return jsonb_build_object('ok', true, 'fonte', v_fonte,
                            'atualizados', v_atualizados, 'inseridos', v_inseridos);
end;
$$;

revoke all on function public.fn_espelhar_xml_no_vista_log() from public, anon, authenticated;

-- Roda no compasso do sync, defasada da trava de publicação.
select cron.schedule('espelho-do-xml-nativo', '6-59/10 * * * *',
                     $$select public.fn_espelhar_xml_no_vista_log();$$);
