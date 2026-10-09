-- Estoque de origens livres — DERIVADO, nunca lembrado.
--
-- Por que este arquivo existe. Ate 09/10/2026 a lista de origens livres era
-- escrita A MAO em docs/estoque.md a cada rodada, e tres erros nasceram ali:
--
--   652/655  contei longos das embalagens recentes e declarei "estoque ZERO"
--            quando o banco tinha 55 longos;
--   658      apontei `_M8t8SPC_f0` como a melhor origem livre do kolejny. Era
--            uma das seis copias do MESMO video, marcadas para exclusao. Se eu
--            tivesse construido dali, o CTA apontaria para um video a apagar;
--   09/10    a lista dizia 27 livres. Esta consulta diz 23. A mao estava errada
--            em quatro, e nao havia como eu saber qual numero valia.
--
-- A causa raiz nao era desatencao: a origem consumida NAO EXISTIA no banco.
-- `fonte_pauta_vd` e numerico e `fonte_pauta` e o texto da pesquisa do longo.
-- Entao "quais origens ja usei" so existia na minha lista. A migracao
-- `videos_origem_id` criou `videos.origem_id` e o backfill leu os 27 shorts
-- soltos das proprias specs (`longo_existente`) — inclusive revelando que
-- epomeno-s002 e s006 usaram a MESMA origem (`h04-UVlVevs`), o que ninguem
-- podia ter visto antes porque nao havia onde ver.
--
-- Com isto, origem usada e titulo duplicado saem POR CONSTRUCAO, nao por eu
-- lembrar de excluir. Rode esta consulta antes de escolher pauta; nao reescreva
-- a lista a mao.
--
-- O QUE ELA AINDA NAO SABE: o PERFIL da origem (aprendizado 651 — dinheiro
-- proprio com papel na mao rende ~30x mais que conformidade corporativa). Isso
-- continua sendo leitura, nao consulta. Por isso ela devolve o titulo tambem.
with dup as (
  -- Grupo duplicado INTEIRO, nao `row_number() = 1`: a primeira copia tambem
  -- sera apagada, entao nenhuma das copias serve de origem.
  select canal, formato, titulo from videos
   where youtube_id is not null and titulo is not null
   group by 1,2,3 having count(*) > 1),
usadas as (
  select distinct origem_id from videos where origem_id is not null)
select l.canal, l.youtube_id, l.titulo
  from videos l
  left join dup d
    on d.canal = l.canal and d.formato = l.formato and d.titulo = l.titulo
 where l.formato = 'longo'
   and l.youtube_id is not null
   and l.titulo is not null
   and l.canal in ('labtreinamento', 'epomeno-epipedo', 'kolejny-poziom')
   and d.titulo is null
   and l.youtube_id not in (select origem_id from usadas)
 order by l.canal, l.titulo;
