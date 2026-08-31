# Medir sem sandbox: a Data API do YouTube lida de dentro do Postgres

Escrito em 31/08/2026, na rodada em que os vinte e dois vídeos de 27/08
finalmente foram medidos — quatro dias depois de irem ao ar, e não dois, porque
a sessão ficou parada.

## A confusão que este arquivo desfaz

`docs/publicar-pela-sandbox.md` descreve a rota ponte inteira, e ela passa pela
sandbox do Composio. É correto para **publicar**: upload precisa do arquivo, e
o arquivo mora num artefato do GitHub.

**Medir não precisa de arquivo.** E quando não precisa, a sandbox é um desvio
que só serve para fazer o `access_token` atravessar uma chamada de ferramenta
sem necessidade nenhuma.

O `pg_net` já está no banco, já sabe falar HTTP, e já é como o token nasce.
Então ele também lê a Data API — e o token nasce e morre dentro do Postgres.

## A rota, em três consultas

```sql
-- 1. o token nasce
select net.http_post(
  url := (valor->>'token_uri'),
  body := jsonb_build_object(
    'client_id',     valor->>'client_id',
    'client_secret', valor->>'client_secret',
    'refresh_token', valor->>'refresh_token',
    'grant_type',    'refresh_token'),
  headers := '{"Content-Type": "application/json"}'::jsonb,
  timeout_milliseconds := 20000) as req_id
from config where chave = 'yt_token_epomeno-epipedo';

-- 2. o token vira Authorization SEM sair do banco. `net._http_response`
--    guarda a resposta pelo id; a consulta lê de lá e monta o header na
--    mesma expressão. O access_token nunca aparece num resultado.
with tok as (select content::jsonb->>'access_token' as at
               from net._http_response where id = 87),
     ids as (select string_agg(youtube_id, ',') as lista
               from videos where publicado_em > '2026-08-27')
select net.http_get(
  url := 'https://www.googleapis.com/youtube/v3/videos'
         || '?part=statistics,contentDetails,status&id=' || ids.lista,
  headers := jsonb_build_object('Authorization', 'Bearer ' || tok.at,
                                'Accept', 'application/json'),
  timeout_milliseconds := 20000) as req_id
from tok, ids;

-- 3. o resultado entra direto em `metricas`, sem passar por lugar nenhum
insert into metricas (youtube_id, coletado_em, views, impressoes, ctr,
                      retencao_media_pct, duracao_media_s,
                      inscritos_ganhos, receita_estimada_usd)
select it->>'id', now(), (it->'statistics'->>'viewCount')::int,
       0, 0, 0, 0, 0, 0
from net._http_response r,
     lateral jsonb_array_elements(r.content::jsonb->'items') it
where r.id = 88
on conflict (youtube_id, coletado_em) do nothing;
```

Vinte e dois vídeos numa chamada (o limite da `videos.list` é cinquenta ids), e
`channels.list` faz o mesmo para os inscritos de todos os canais de uma vez.

Serve também para o passo 8 do runbook — conferir no vídeo publicado.
`part=status` traz `privacyStatus`, e é a mesma consulta.

## O buraco que essa rota NÃO tapa, e é o importante

A Data API dá **views, likes, comentários e o estado do vídeo**. Ela não dá:

- retenção média e duração média assistida (os SEGUNDOS VISTOS da alavanca B);
- inscritos ganhos por vídeo (o numerador da alavanca A).

Esses dois vêm da **YouTube Analytics API**, e os tokens da frota carregam
apenas `youtube`, `youtube.upload` e `youtube.force-ssl`. A Composio também não
expõe nenhuma ação de Analytics — conferido em 31/08, o catálogo dela é todo
Data API.

Consequência prática, e ela dói: **os dois números que decidem a máquina não
são mensuráveis hoje.** Em 31/08 os vinte e dois vídeos entraram em `metricas`
com `retencao_media_pct` e `inscritos_ganhos` em zero por AUSÊNCIA DE FONTE,
não porque sejam zero. Quem ler essas linhas sem ler isto aqui vai concluir
errado.

O que destrava: reautorizar os tokens dos canais incluindo o escopo
`https://www.googleapis.com/auth/yt-analytics.readonly`.

## Enquanto isso, o que dá para medir

Inscritos **por canal**, que é o alvo do YPP. Não existia série temporal
nenhuma disso até 31/08 — `metricas.inscritos_ganhos` é por vídeo e depende do
escopo que falta, e `canais` não guarda o total. A tabela `canais_snapshot` e a
view `v_maquina_inscritos` passam a guardar, e toda coleta grava as duas.

E uma armadilha que a primeira leitura revelou: **`labtreinamento` e
`sx-educacao` são canais pré-existentes**, não criados pela máquina. O
labtreinamento tem 47 vídeos públicos contra 12 pacotes da máquina, e 8.310
views de canal contra 1.210 dos vídeos da máquina. Os 64 inscritos dele não são
da máquina. Sempre compare `videos_publicos` com os pacotes registrados antes
de somar inscrito ao placar.
