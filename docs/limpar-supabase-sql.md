# Limpar espaco no Supabase — MEDIDO em 12/10, e a resposta e "nao ha o que apagar"

O dono pediu em 12/10: *"qual codigo SQL rodar no sampaioopablo1-lgtm para
limpar/deletar e liberar espaco para uso exclusivo para construir e publicar
videos?"* — e depois: *"faca daqui"*.

**Feito daqui, e isto retrata o que eu havia escrito neste mesmo arquivo meia
hora antes.** Eu havia dito que nao conseguia rodar nada no projeto porque o
`list_projects` nao o mostrava. Consigo.

## O que a medicao devolveu

| | |
|---|---|
| `pg_database_size` | **26 MB** |
| `storage.objects` | **114 objetos, 1.679 kB no total**, o maior com **69 kB** |
| buckets | `videos-maquina` 112 objetos / 1.573 kB (05/08 a 24/08); `site` 2 / 106 kB |
| maiores tabelas | `videos` 9.712 kB (424 linhas), `aprendizados` 1.216 kB, `metricas` 1.072 kB (5.366 linhas) |

**Os 3,7 GB de Storage NAO EXISTEM.** O numero foi herdado da conclusao de
25/08 e eu o repeti por semanas — no `CLAUDE.md`, na rotina e ao dono — sem
nunca o verificar por tabela nem por bucket. Zero objetos sem tamanho declarado,
entao a soma nao esta escondendo nada.

**Logo nao ha o que apagar.** O projeto inteiro mede ~28 MB. Apagar as metricas
antigas renderia **menos de 1 MB**, e custaria a deteccao de replica atrasada,
que precisa das tres ultimas coletas. **Nao rode DELETE nenhum: o ganho e
irrelevante e a perda nao e.** Aprendizado 710.

E a consequencia maior: **o 402 nao e sobre ocupacao atual.** Ele e GB-Hrs ja
consumidos no ciclo, e nenhum DELETE desfaz consumo passado. O caminho continua
sendo o Pro — ou nada.

## O defeito de sonda que isto expos, e ele e meu

**`list_projects` nao e sonda de acesso.** Ele reflete a ORGANIZACAO a que o
conector esta ligado. O `execute_sql` alcanca o projeto **pelo `ref`** mesmo
quando ele nao aparece na lista. Eu usei o catalogo como se fosse capacidade, e
isso esta escrito como procedimento na §10 do `CLAUDE.md` e da rotina:
*"banco: `mcp__Supabase__list_projects` tem de mostrar `maquina-yt-dark`"*.
**Essa linha esta errada e e por causa dela que eu declarei o banco fora por
dias.** Sonde a capacidade, com uma query trivial. Aprendizado 709.

## E o que isso DESTRAVA, que e o que importa de verdade

Medido na mesma rodada, com `status_code` de cada chamada:

| rota | resultado |
|---|---|
| `execute_sql` no `vevocauwtarctfwngrch` | **funciona** |
| `pg_net` -> `ec.europa.eu` (Eurostat) | **200**, 20.048.657 bytes (req 931) |
| `pg_net` -> `www.googleapis.com` | **200**, 383.927 bytes (req 932) |
| REST / PostgREST | **402** (anotacao do `diario.yml`, run 38253582334, 13:07) |

**O 402 e do GATEWAY REST, nao do Postgres.** Entao: medicao aberta (YouTube API
pelo `pg_net`), registro aberto (`execute_sql`), e **fonte institucional
aberta** — o Eurostat respondeu 200 de dentro do Postgres, exatamente como a
rota documentada previa.

**Isto derruba a secao "REFILAR a pauta exige FONTE, e a fonte esta bloqueada na
rede" do `CLAUDE.md`.** O 403 ao CONNECT que eu medi as 10:15 e real, e e do
proxy DESTE container — e o `pg_net` nao passa por ele. Eu escrevi a rota certa
("a busca acontece dentro do Postgres, entao o proxy nao entra") e no paragrafo
seguinte a declarei indisponivel por causa do 402, sem testar.
**LONGO NOVO voltou a ser possivel.**

## A unica limpeza que esta rodada gerou foi MINHA

As duas sondas do `pg_net` gravaram 20,4 MB em `net._http_response`. O `DELETE`
delas estourou o timeout de 60 s do MCP, duas vezes, nos dois sentidos (as duas
linhas e uma linha so) — e isso e o aprendizado 621, o timeout INTERMITENTE.
Nao insisti: o proprio worker do `pg_net` apaga resposta por TTL, e o banco
subiu de 26 para 30 MB, que nao importa em nada.

**Licao de operacao: `pg_net` com resposta grande suja o banco.** Para sondar
disponibilidade de host, peca `HEAD` ou um endpoint pequeno, nao um dataflow de
20 MB.
