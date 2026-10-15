# O que ficou pendente porque o banco recusou

**Medido em 15/10 às 11:1x, aprendizado 775.** O `execute_sql` do MCP do Supabase
passou a recusar com `MCP error -32600: You do not have permission to perform
this action` — inclusive na **sonda de capacidade**
(`select pg_database_size(current_database())`), que é o teste que o 709 manda
usar em vez do `list_projects`. Logo não é catálogo, é capacidade.

**Trate como ESTADO, nunca como propriedade** (a lição de 11/10 sobre o
`mcp__github__*`, que se recuperou sozinho): **sonde antes de dizer que não há
rota.** A sonda é uma chamada e é barata.

## O QUE SÓ O DONO PODE FAZER, medido em 15/10 às 14:1x (aprendizado 777)

**Quatro rodadas seguidas com o `execute_sql` negado**, e três chamadas desta
rodada localizam o que dá para localizar:

| chamada | resultado |
|---|---|
| `execute_sql` em `vevocauwtarctfwngrch` | **negado** (`-32600`) |
| `list_organizations` | **200** — uma org, `imobjazz-eng's Org` |
| `list_projects` | **200** — um projeto, `imobjazz-eng's Project` |

**O servidor MCP funciona** (duas chamadas com 200 na mesma rodada), logo não é
servidor caído. **E o catálogo não explica a negação**, porque ele é
*indistinguível* do catálogo de 12/10 — quando o `execute_sql` no
`vevocauwtarctfwngrch` **funcionava**. Duas leituras compatíveis com o que eu vejo
(conector reapontado para outra org, ou permissão retirada do projeto) produzem o
MESMO par de respostas, então **eu não atribuo a causa daqui**.

**O que o dono precisa fazer: reconectar o conector do Supabase escolhendo a
organização do projeto `maquina-yt-dark` (`vevocauwtarctfwngrch`).**

**E ISTO MUDA A ORDEM DA FILA que a rotina escreve.** A pendência 2 diz *"NÃO
peça a reconexão do conector como primeira opção: ela é a PIOR das três"* — e
essa ordem **pressupunha que o banco funcionava** e que só o REST estava em 402.
Ali a reconexão devolvia o que eu já tinha e deixava o 402 de pé. **Com o
`execute_sql` negado a premissa caiu:** sem ele não há `pg_net`, logo não há
token, logo não há leitura de duração real, nem de inscritos, nem a rota da regra
(h), nem o registro em `videos`.

**O que NÃO caiu, e vai dito para a decisão não sair errada:** a publicação
continua funcionando — quatro peças foram ao ar nestas quatro rodadas pelo
`retomar.yml`, que usa o segredo `YT_OAUTH_JSON` e **não toca o Supabase**. A
pendência 3 já está feita, e é por isso.


## `videos-a-inserir.sql`

São as linhas de `videos` que o `fabrica/registro_videos.py` imprimiu e que **não
foram aplicadas** — o segundo dos dois passos de registro (aprendizado 726). O
primeiro passo (o título no `fabrica/corpus_publicados.json`) **foi** feito, por
ser local.

**Rode isto na PRIMEIRA rodada que reabrir o banco**, por `execute_sql`, e depois
apague o arquivo. Cada linha tem `on conflict (slug) do nothing`, logo rodar duas
vezes não dói.

**E por que isto existe em arquivo em vez de ficar na minha cabeça:** sem
`origem_id` em `videos` a `consultas/estoque.sql` não sabe que a origem foi
consumida (670), e a trava contra reusar origem fica cega. A falha de `videos` é
ruidosa, mas **só levanta quando alguém tenta medir** — barulho que ninguém ouve
é silêncio, e foi assim que eu perdi doze publicações em 13/10.

## Quinta rodada sem o banco — 15/10 às 15:2x

A sonda de capacidade (`select pg_database_size(current_database())`) foi feita
duas vezes nesta rodada, antes e depois de publicar, e foi **negada as duas**.
Trato isso como ESTADO e não como propriedade, então ela é refeita a cada rodada.

**A produção NÃO parou:** o `epomeno-epipedo-s036` foi ao ar às 15:19 UTC como
`R4Ldmvcu9k8`, porque a publicação sai pelo `retomar.yml` com o `YT_OAUTH_JSON`
e não toca o Supabase.

**O que o banco fechado continua custando, e é o mesmo de ontem:**
- as **cinco** linhas de `videos` seguem parqueadas em
  `docs/pendente/videos-a-inserir.sql`, e sem `origem_id` em `videos` a
  `consultas/estoque.sql` não sabe que aquelas cinco origens foram consumidas;
- **não há leitura de inscritos** (Porta 1), porque ela depende do `pg_net`;
- **não há leitura de duração real**, logo a banda de resíduo segue congelada em
  `RESIDUO_N = 40` e já são **cinco** peças sem ponto;
- as origens da regra (h) — as que só têm legenda e não têm spec local —
  seguem inalcançáveis.

## Sexta rodada sem o banco — 15/10 às 16:1x

Sonda negada outra vez, antes e depois de publicar. O
`labtreinamento-s054` foi ao ar às 16:12 UTC como **`P_rWsua8Zb0`**, pelo
`retomar.yml`, que não toca o Supabase.

**O pendente foi a SEIS linhas** — e esta foi a primeira vez que o conserto do
`registro_videos.py` (relato em stderr, stdout puro) rodou em produção: o
arquivo ficou com seis inserts e **zero linha de prosa**, contra as três que
vazaram na rodada anterior.

Sem `execute_sql` seguem indisponíveis: leitura de inscritos (Porta 1), leitura
de duração real (a banda está congelada em `RESIDUO_N = 40`, e agora são **cinco**
peças sem ponto), as origens da regra (h), e a inserção destas seis linhas em
`videos`.
