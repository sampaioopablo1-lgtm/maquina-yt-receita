# O que ficou pendente porque o banco recusou

**Medido em 15/10 às 11:1x, aprendizado 775.** O `execute_sql` do MCP do Supabase
passou a recusar com `MCP error -32600: You do not have permission to perform
this action` — inclusive na **sonda de capacidade**
(`select pg_database_size(current_database())`), que é o teste que o 709 manda
usar em vez do `list_projects`. Logo não é catálogo, é capacidade.

**Trate como ESTADO, nunca como propriedade** (a lição de 11/10 sobre o
`mcp__github__*`, que se recuperou sozinho): **sonde antes de dizer que não há
rota.** A sonda é uma chamada e é barata.

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
