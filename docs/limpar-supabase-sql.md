# Limpar espaco no Supabase por SQL — o que funciona e o que NAO funciona

Escrito em 12/10/2026, a pedido do dono: *"qual codigo SQL rodar no
sampaioopablo1-lgtm para limpar/deletar e liberar espaco para uso exclusivo para
construir e publicar videos?"*

**Rode tudo no SQL Editor do site do Supabase**, no projeto
`vevocauwtarctfwngrch` (maquina-yt-dark). O SQL Editor nao passa pelo conector
nem pelo REST, entao o 402 nao o atrapalha. O conector desta sessao enxerga
apenas `imobjazz-eng's Project`, logo eu nao consigo rodar nem medir isto daqui.

## A ressalva que vem ANTES do codigo, e ela e a resposta principal

**Nenhum SQL levanta o 402.** A restricao e de Fair Use da ORGANIZACAO e e
medida em **GB-Hrs ja consumidos no ciclo**: o consumo aconteceu, e apagar
arquivo nao o desfaz. Medido: o 402 e continuo de 25/08 a 11/10, 47 dias,
atravessando pelo menos uma virada de ciclo. O proprio `expurgo-storage.yml`
prometia "destrava na virada" e isso esta FALSIFICADO pelo resultado.

E os 3,7 GB estao no **Storage**, nao em linha de tabela. `DELETE` em tabela nao
os move. O no e circular: o 402 bloqueia o Storage, o expurgo precisa do Storage
para apagar, os 3,7 GB nunca saem, e cada ciclo novo reestoura a cota no
primeiro dia com o mesmo 3,7 GB lá dentro.

**O que levanta: Pro** (levanta na hora E deixa o expurgo rodar), ou mover o
projeto para outra organizacao — e isso em 11/10 foi recusado com
*"can't be transferred to a Free organization while the source organization is
in an active grace period"*.

## PASSO 1 — MEDIR. Nao apague nada antes disto.

Eu herdei o numero "3,7 GB" e nunca o verifiquei por tabela. Receitar `DELETE`
sem medir e o erro que este repositorio documenta dezenas de vezes.

```sql
-- 1a. Tamanho total do banco
select pg_size_pretty(pg_database_size(current_database())) as banco;

-- 1b. As vinte maiores relacoes, com tabela e indice separados
select n.nspname as esquema,
       c.relname as objeto,
       pg_size_pretty(pg_total_relation_size(c.oid)) as total,
       pg_size_pretty(pg_relation_size(c.oid))       as dados,
       pg_size_pretty(pg_indexes_size(c.oid))        as indices,
       c.reltuples::bigint                           as linhas_aprox
  from pg_class c
  join pg_namespace n on n.oid = c.relnamespace
 where c.relkind in ('r','m','p')
   and n.nspname not in ('pg_catalog','information_schema')
 order by pg_total_relation_size(c.oid) desc
 limit 20;

-- 1c. O STORAGE, que e onde o Fair Use foi gasto. Isto NAO e tabela de dados:
--     e o indice dos objetos. O byte real esta no backend de arquivos.
select bucket_id,
       count(*)                                           as objetos,
       pg_size_pretty(sum((metadata->>'size')::bigint))    as bytes,
       min(created_at)::date                               as mais_antigo,
       max(created_at)::date                               as mais_recente
  from storage.objects
 group by bucket_id
 order by sum((metadata->>'size')::bigint) desc nulls last;
```

**Leia o 1c antes de decidir qualquer coisa.** Se o peso estiver todo em
`storage.objects`, o passo 2 nao resolve e o passo 3 e o unico caminho — e o
passo 3 tem uma incerteza que eu declaro lá.

## PASSO 2 — limpar o que E limpavel por SQL, sem perder nada que importa

Estas tres sao seguras e reversiveis no sentido que importa: nenhuma delas apaga
registro de video publicado, de metrica ou de aprendizado.

```sql
-- 2a. Metricas antigas, mantendo as TRES ultimas coletas de cada peca.
--     Tres e o minimo do estimador: o piso e o MAXIMO das tres leituras.
--     Apagar abaixo de tres cega a leitura de replica atrasada.
with ranqueadas as (
  select ctid,
         row_number() over (partition by youtube_id
                            order by coletado_em desc) as n
    from metricas
)
delete from metricas m
 using ranqueadas r
 where m.ctid = r.ctid
   and r.n > 3;

-- 2b. Devolver o espaco ao sistema operacional. Sem isto o DELETE acima nao
--     reduz o tamanho em disco, so marca as paginas como reutilizaveis.
--     FULL pede bloqueio exclusivo e o dobro do tamanho da tabela em disco
--     durante a operacao -- rode fora de janela de publicacao.
vacuum (full, analyze) metricas;

-- 2c. Conferir o ganho
select pg_size_pretty(pg_total_relation_size('metricas')) as metricas_agora,
       pg_size_pretty(pg_database_size(current_database())) as banco_agora;
```

**O que NAO apagar, e isto e trava:**

- `videos` — e o registro do que esta no ar e a base das travas anti-duplicata;
- `aprendizados` com `status = 'ativo'` — e a memoria da maquina;
- `config` — carrega os pares `client_id`/`client_secret` por canal, e o par
  errado produz `401 unauthorized_client` que se parece com token revogado e
  NAO e (aprendizado 667);
- `canais`;
- qualquer tabela do esquema `auth`.

## PASSO 3 — o Storage, e a incerteza que eu declaro em vez de esconder

Se o 1c mostrar que o peso esta no Storage, a pergunta e se apagar linha de
`storage.objects` pelo SQL Editor devolve a cota, dado que a API de Storage esta
em 402.

**Eu nao sei, e nao vou afirmar que sei.** O que eu sei: a linha e o indice; o
byte vive no backend de arquivos. Apagar a linha pode deixar o arquivo orfao e
cobrado. **Logo isto se MEDE antes de se fazer em massa:** apague UM objeto
grande, espere o painel de Usage atualizar, e veja se o numero de Storage caiu.

```sql
-- 3a. Primeiro OLHE o que ha, do maior para o menor. So leitura.
select id, bucket_id, name,
       pg_size_pretty((metadata->>'size')::bigint) as tamanho,
       created_at
  from storage.objects
 order by (metadata->>'size')::bigint desc nulls last
 limit 30;

-- 3b. O TESTE de um objeto so. Troque o id pelo maior do 3a, rode, e olhe o
--     painel de Usage depois. Se o numero nao cair, pare: a rota e o Pro.
-- delete from storage.objects where id = 'COLE_O_ID_AQUI';
```

O `delete` do 3b esta **comentado de proposito**. Descomentar e decisao do dono,
e vale a trava geral: o arquivo dos videos e o Google Drive, nao o banco — mas
confirme que o objeto que vai sair tem copia lá antes de apagar.

## O que este arquivo NAO faz

Nao apaga video publicado, nao apaga as 46 duplicatas e nao toca em parametro de
producao. As tres coisas sao irreversiveis ou sao decisao do dono.
