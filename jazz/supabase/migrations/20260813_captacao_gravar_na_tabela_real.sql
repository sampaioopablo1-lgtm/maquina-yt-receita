-- 13/08/2026 — Usuário mandou print do painel completo do captador: TODAS
-- as solicitações mostravam "0 pendentes / nenhum imóvel pra trabalhar",
-- mesmo depois dos fixes anteriores. Investigando a fundo (tabelas, FKs,
-- funções): o pipeline inteiro que eu construí hoje
-- (`captacao_prospects` → `solicitacao_sugestoes_externas`) é uma tabela
-- paralela que **nada no app lê**. A tela do captador usa outro caminho:
--
--   solicitacoes → solicitacao_sugestoes (imovel_id) → imoveis
--                                                    ↓
--                                          fn_gerar_tarefa_passo1()
--                                                    ↓
--                                           tarefas_captacao (o que a
--                                           tela realmente renderiza,
--                                           com "Reservar 7d"/"Captado")
--
-- `imoveis` é a tabela real de candidatos a captar — em essência, a
-- planilha Plancap digitalizada (6.309 registros com origem='manual', 7
-- com 'importacao_lista'; a constraint já previa 'externo' e 'plancap'
-- como origens válidas, mas nenhuma nunca foi usada). `solicitacao_sugestoes`
-- é usada tanto para venda de imóvel existente quanto para CAPTAÇÃO — o
-- imovel_id aponta pra `imoveis` nos dois casos, não tem tabela separada.
-- `fn_gerar_tarefa_passo1()` só promove UMA sugestão de cada vez pra virar
-- tarefa visível, e só se o captador não tiver tarefa ativa pra aquela
-- solicitação — por isso "0 pendentes" também pode significar captador
-- sobrecarregado (ex.: Camila com 349 tarefas abertas contra limite de 50),
-- não necessariamente falta de sugestão.
--
-- Correção definitiva: os prospects coletados (particular/indefinido, com
-- telefone) entram direto em `imoveis` (origem='externo',
-- status_captacao='Disponível' — os mesmos valores que a constraint já
-- previa) e viram `solicitacao_sugestoes` reais para as solicitações
-- compatíveis. Dedup por `codigo_jazz` (índice único parcial já existente)
-- usando o id do prospect, então rodar de novo não duplica.
--
-- O pipeline anterior (captacao_prospects, captacao_fila_solicitacoes,
-- solicitacao_sugestoes_externas) fica no lugar — continua alimentando o
-- estoque de prospects que este INSERT consome, só que agora grava onde o
-- app enxerga.

-- Tipo do imóvel a partir do título/tipo coletado — vocabulário livre em
-- `imoveis.tipo_imovel`, mas segue o que já existe na tabela.
create or replace function public.fn_captacao_tipo_imovel(titulo text, tipo text)
returns text
language sql
immutable
as $$
  select case
    when coalesce(titulo,'') ~* 'apartamento|apto\.?\s' or coalesce(tipo,'') ~* 'apartment' then 'Apartamento'
    when coalesce(titulo,'') ~* '\bsobrado\b' then 'Sobrado'
    when coalesce(titulo,'') ~* '\bcasa\b' then 'Casa'
    when coalesce(titulo,'') ~* 'ch[aá]cara|s[ií]tio' then 'Chácara / Sítio'
    when coalesce(titulo,'') ~* '\bterreno\b|\blote\b' then 'Terreno'
    when coalesce(titulo,'') ~* 'galp[aã]o' then 'Galpão'
    when coalesce(titulo,'') ~* 'sala comercial' then 'Sala Comercial'
    when coalesce(titulo,'') ~* 'ponto comercial|com[eé]rcio' then 'Ponto Comercial'
    else 'Imóvel'
  end;
$$;

with novos as (
  insert into public.imoveis (
    codigo_jazz, codigo, cidade, bairro, endereco, zona,
    tipo_imovel, tipo_negocio, valor, valor_locacao,
    proprietarios, telefone, status_captacao, origem,
    link_contato, observacao, created_at
  )
  select
    'EXT-' || p.id, 'EXT-' || p.id, p.cidade, p.bairro, p.endereco, null,
    public.fn_captacao_tipo_imovel(p.titulo, p.tipo),
    case when p.tipo_operacao = 'rent' then 'Locação' else 'Venda' end,
    case when p.tipo_operacao = 'rent' then null else p.preco end,
    case when p.tipo_operacao = 'rent' then p.preco else null end,
    p.anunciante, p.telefone, 'Disponível', 'externo',
    p.url, format('Captado via %s — %s', p.fonte, p.motivo_perfil), p.coletado_em
  from public.captacao_prospects p
  where p.telefone is not null
    and p.perfil in ('particular', 'indefinido')
  on conflict (codigo_jazz) where codigo_jazz is not null do nothing
  returning id, codigo_jazz, cidade, tipo_negocio, valor, valor_locacao
),
candidatos as (
  select
    s.id as solicitacao_id,
    n.id as imovel_id,
    case when p.perfil = 'particular' then 90 else 60 end as score,
    format('Prospect de captação (%s) — %s', p.perfil, p.motivo_perfil) as motivo,
    -- Um imóvel não deve virar sugestão pra dezenas de solicitações de
    -- uma vez só porque a faixa de preço é larga: fica só com as 15 mais
    -- próximas em preço.
    row_number() over (
      partition by n.id
      order by abs(coalesce(n.valor, n.valor_locacao, 0) -
        ((coalesce(s.valor_min,0) + coalesce(s.valor_max, coalesce(s.valor_min,0)*2)) / 2.0))
    ) as rn
  from novos n
  join public.captacao_prospects p on 'EXT-' || p.id = n.codigo_jazz
  join public.solicitacoes s
    on s.status in ('Trabalhando na busca do imóvel','Em Atendimento','Pendente','Aguardando Aprovação Pablo')
    and public.fn_norm_cidade(s.cidade) = public.fn_norm_cidade(n.cidade)
    and (
      (n.tipo_negocio = 'Venda' and lower(coalesce(s.tipo_operacao,'')) not like 'loca%' and lower(coalesce(s.tipo_operacao,'')) not like 'alug%'
        and (s.valor_min is null or n.valor is null or n.valor >= s.valor_min * 0.9)
        and (s.valor_max is null or n.valor is null or n.valor <= s.valor_max * 1.1))
      or
      (n.tipo_negocio = 'Locação' and (lower(coalesce(s.tipo_operacao,'')) like 'loca%' or lower(coalesce(s.tipo_operacao,'')) like 'alug%')
        and (s.valor_min is null or n.valor_locacao is null or n.valor_locacao >= s.valor_min * 0.9)
        and (s.valor_max is null or n.valor_locacao is null or n.valor_locacao <= s.valor_max * 1.1))
    )
), pares as (
  select solicitacao_id, imovel_id, score, motivo from candidatos where rn <= 15
)
insert into public.solicitacao_sugestoes (solicitacao_id, imovel_id, score, status, motivo)
select solicitacao_id, imovel_id, score, 'sugerido', motivo
from pares
on conflict (solicitacao_id, imovel_id) do nothing;
