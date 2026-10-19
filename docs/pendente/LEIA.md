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

## Sétima rodada sem o banco — 15/10 às 17:1x

Sonda negada outra vez, antes e depois de publicar. O
`kolejny-poziom-s035` foi ao ar às 17:12 UTC como **`pgbq5Lw0aaM`**.

**O pendente foi a SETE linhas**, todas insert, nenhuma de prosa.

E esta rodada mostra o que o banco fechado custa NA PAUTA, não só na
medição: o `concentracao.py` nomeou **quatro** origens do `kolejny` usadas
uma vez só, e **três delas não têm spec local** — a rota da regra (h)
(`captions?part=snippet` pelo `pg_net`) depende do banco. Sobrou **uma**
origem escrevível, e ela foi usada. Se a próxima rodada cair neste canal,
a pauta dele passa a depender de origem de dois usos.

## Oitava rodada sem o banco — 15/10 às 18:1x

Sonda negada antes e depois de publicar. O `epomeno-epipedo-s037` foi ao ar
às 18:12 UTC como **`qLg-zNaRKSI`**.

**O pendente foi a OITO linhas**, todas insert.

**E o dia fecha em 4 / 4 / 3 peças** (labtreinamento / epomeno / kolejny),
contra as 7/dia POR CANAL que o dono pede. O limite de hoje não foi cota nem
pauta: foi **uma peça por rodada**, porque cada rodada gasta o tempo dela num
render e numa publicação. Subir isso é a pendência 4 (teto só para short solto)
mais a 5 (disparo externo), e as duas são decisão do dono.

## Nona rodada sem o banco — 15/10 às 19:1x

Sonda negada antes e depois de publicar. O `labtreinamento-s055` foi ao ar
às 19:12 UTC como **`X7c1utln5yw`**. **O pendente foi a NOVE linhas**, todas
insert.

E o caso especial da regra (g) — número que a própria fonte declara inventado —
apareceu em **dois dias seguidos**, no `kolejny-poziom-018` (capítulo 32) e no
`labtreinamento-012` (capítulo 32). Isso é hábito dos nossos longos, não
coincidência: o autor marca o exemplo numérico como ilustração. Vale como aviso
de que o short dessas origens nunca carrega o exemplo.

## Décima rodada sem o banco — 15/10 às 20:1x

Sonda negada antes e depois de publicar. O `kolejny-poziom-s036` foi ao ar
às 20:12 UTC como **`GHxK6JAORYc`**. **O pendente chegou a DEZ linhas**, todas
insert — e dez linhas de `videos` é o tamanho do que o 670 perde: a
`estoque.sql` não sabe que essas dez origens foram consumidas.

**E a previsão da rodada das 17:1x se cumpriu:** consumida a única origem
escrevível do `kolejny`, a pauta dele passou a depender de origem de **dois
usos**. As três origens de um uso só seguem inalcançáveis porque a rota da
regra (h) (`captions` pelo `pg_net`) depende do banco. Nenhum canal ficou sem
pauta hoje, mas a folga do kolejny acabou.

## Décima primeira rodada sem o banco — 15/10 às 21:1x

Sonda negada antes e depois de publicar. O `epomeno-epipedo-s038` foi ao ar
às 21:12 UTC como **`s4KbV20zFbM`**. **O pendente está em ONZE linhas.**

**O dia fecha em 5 / 5 / 4** (labtreinamento / epomeno / kolejny), contra as
7/dia POR CANAL. Onze peças em onze rodadas, uma por rodada — e o limite não foi
pauta nem cota: foi **o tempo de uma rodada**, que cabe um render e uma
publicação. As pendências 4 e 5 são o que destrava isso, e as duas são suas.

## Décima segunda rodada sem o banco — 15/10 às 22:1x

Sonda negada antes e depois de publicar. O `labtreinamento-s056` foi ao ar às
22:11 UTC como **`nkQWSScZXaA`**. **O pendente está em DOZE linhas.**

**O dia fecha em 6 / 5 / 4** (labtreinamento / epomeno / kolejny), 15 peças em
12 rodadas de hoje. E o LUFS desta peça saiu com **pico −0,6 dBTP** e LRA 3,5 —
o pico mais alto do dia (os outros ficaram entre −1,5 e −4,1). Não é defeito
medido e não reprova nada; fica anotado porque é a primeira vez que o pico
chega tão perto de zero, e se repetir vale olhar o `SOM` antes de supor.

## Décima terceira rodada sem o banco — 15/10 às 23:1x

Sonda negada antes e depois de publicar. O `kolejny-poziom-s037` foi ao ar às
23:11 UTC como **`LTC9nE-iEE4`**. **O pendente está em TREZE linhas.**

**O dia 15/10 fecha em 6 / 5 / 5** (labtreinamento / epomeno / kolejny), 16 peças
em 13 rodadas. Nenhum canal ficou sem pauta e nenhum portão reprovou peça
publicada.

E o pico de som voltou à faixa habitual (−3,4 dBTP) na peça seguinte à de
−0,6 — então aquilo foi um ponto, não uma tendência, como já estava dito.

## Decima quarta rodada sem o banco — 16/10, 00:1x

Sonda da CAPACIDADE (nao do catalogo, pelo 709/777): `execute_sql` com
`select pg_database_size(current_database())` em `vevocauwtarctfwngrch` ->
**negado** (`-32600`), antes e depois de publicar. Decima quarta rodada seguida.

**Publicado:** `epomeno-epipedo-s039` = `idkn35TYGE0` (00:17 UTC), provedor
**edge** MEDIDO (zero avisos no job `116740973441`), previsao edge 41,5 / piper
36,7, som LUFS -14,1 e pico -3,0 dBTP.

**Perdido:** 41o ponto da banda — `RESIDUO_N` segue 40, e agora sao **treze**
pecas sem leitura de duracao real, todas com a previsao escrita na copy. Sem
vigilancia do §3.2. A linha de `videos` ficou parqueada: o
`videos-a-inserir.sql` foi a **14 linhas**, cada uma com `origem_id` e
`on conflict (slug) do nothing`.

**E o custo em PAUTA apareceu outra vez, agora no epomeno.** As duas origens de
UM uso do canal (`eZ697VNYCPU`, `h66MCKjwAJ8`) nao tem spec local, e a rota da
regra (h) para elas — `captions?part=snippet&videoId=` — sai pelo `pg_net`, que
depende do `execute_sql` negado. Tive de pegar a banda de DOIS usos
(`wUHuwyO2HYo`). Em 15/10 isso aconteceu no `kolejny`; agora no epomeno. **O
banco fechado ja nao custa so medicao: ele empurra a escolha de origem para a
banda mais usada, que e o contrario do que a concentracao pede.**

Pendencia 2 segue sendo a unica que destrava isto: reconectar o conector do
Supabase **escolhendo a org do projeto `vevocauwtarctfwngrch`**.

## Decima quinta rodada sem o banco — 16/10, 01:0x

Sonda da CAPACIDADE negada (`-32600`), antes e depois de publicar. Decima quinta
rodada seguida.

**Publicado:** `labtreinamento-s057` = `n1VJoPqokm8` (01:12 UTC), provedor **edge**
MEDIDO (zero avisos no job `116757613240`), previsao edge 25,1 / piper 20,6 —
mira do canal VERDE nos dois mundos, com a exposicao do 740/748/774 declarada na
copy antes de publicar. Som LUFS -13,4, desvio **+0,6** (o maior das ultimas
pecas; com n=1 isso e um ponto, nao achado).

**Perdido:** 41o ponto da banda — `RESIDUO_N` segue 40, e agora sao **quatorze**
pecas sem leitura de duracao real. Sem vigilancia do §3.2. O
`videos-a-inserir.sql` foi a **15 linhas**.

**E o custo em PAUTA apareceu pela TERCEIRA rodada seguida, agora no
labtreinamento.** As tres origens de menor uso do canal empatam em tres shorts, e
DUAS delas (`StQNFMdpGdk`, `KRUERlNPzDw`) nao tem spec local — a rota da regra (h)
para elas sai pelo `pg_net`. Sobrou a terceira (`3KtwRYxl7_U`). Em 15/10 foi no
kolejny, as 00:1x no epomeno, agora aqui: **o banco fechado empurra a escolha de
origem para onde ha SPEC, nao para onde ha menos uso.** Nesta peca os capitulos
35 a 40 estavam intocados pelos tres irmaos, logo nao houve repeticao — mas isso
foi propriedade da origem, nao do procedimento.

## Decima sexta rodada sem o banco — 16/10, 02:0x

Sonda negada (`-32600`). **Publicado:** `kolejny-poziom-s038` = `fHUBz98PjgA`
(02:11 UTC), provedor **edge** MEDIDO (zero avisos no job `116774366810`),
previsao edge 41,6 / piper 35,4 (PISO do ALVO_SHORT, pelo 679 e pelo 772). Som
LUFS -14,0, desvio **0,0** — o +0,6 da peca anterior era um ponto isolado, como
eu disse que era.

**Perdido:** 41o ponto da banda (`RESIDUO_N` = 40, **quinze** pecas sem leitura de
duracao real). Sem vigilancia do §3.2. O `videos-a-inserir.sql` foi a **16 linhas**.

**E O PADRAO DA PAUTA FECHOU OS TRES CANAIS — quarta rodada seguida.** Em nenhum
dos tres a origem MENOS usada e alcancavel sem banco:

| canal | origens de menor uso | spec local |
|---|---|---|
| kolejny-poziom | `SP7Vz8qHdRY`, `MjI4ZGJAhIo`, `Xgt32iH8Ft8` (1 uso) | **nenhuma** |
| epomeno-epipedo | `eZ697VNYCPU`, `h66MCKjwAJ8` (1 uso) | **nenhuma** |
| labtreinamento | `StQNFMdpGdk`, `KRUERlNPzDw` (3 usos, as menores) | **nenhuma** |

A rota da regra (h) para todas elas e `captions?part=snippet&videoId=` pelo
`pg_net`. **Logo o banco fechado nao custa so medicao: ele torna INALCANCAVEL a
origem menos usada dos TRES canais**, e empurra toda rodada para a banda mais
usada — o contrario do que a concentracao pede, contra o portao `similaridade`,
que e o portao que estamos tentando passar. Isto e consequencia da pendencia 2,
e vale ser dito ao dono como custo, nao como inconveniencia.

## Decima setima rodada sem o banco — 16/10, 03:0x

Sonda negada (`-32600`), antes e depois de publicar. **Publicado:**
`epomeno-epipedo-s040` = `PA4k1nrpMMI` (03:13 UTC), provedor **edge** MEDIDO
(zero avisos no job `116790708006`), previsao edge 41,7 / piper 37,0 (piso do
ALVO_SHORT, pelo 772). Som LUFS -14,2, desvio -0,2, pico -3,3 dBTP.

**Perdido:** 41o ponto da banda (`RESIDUO_N` = 40, **dezesseis** pecas sem leitura
de duracao real). Sem vigilancia do §3.2. O `videos-a-inserir.sql` foi a
**17 linhas**.

Quinta rodada seguida com a escolha de origem empurrada para a banda mais usada,
pela causa ja tabelada na rodada das 02:0x: as sete origens de menor uso da frota
nao tem spec local e a rota da regra (h) para elas sai pelo `pg_net`.

**E o dia 16/10 vai em 4 pecas (1 epomeno + 1 labtreinamento + 1 kolejny + 1
epomeno) em quatro rodadas** — uma por rodada, que e o teto real desta condicao.
O dono pede 7/dia POR CANAL; o que destrava isso sao as pendencias 4 e 5, as
duas dele.

## 16/10, 03:5x — TRES BLOQUEIOS CAIRAM, e um por rodada nao era o teto

O dono pediu peca de 2 min com capa, publicada, mirando monetizacao. Saiu
`labtreinamento-s058` = `8DVWFC5agrg`, **124 s reais**, com **capa propria** (a
primeira da frota: `capa do short: ok`, e o 403 que eu previa por canal nao
verificado NAO veio).

**O SANDBOX DO COMPOSIO TEM SAIDA PARA A INTERNET, e isso derruba tres coisas
que eu reportei como bloqueadas por dezessete rodadas:**
 1. **MEDICAO** — pagina de watch da `lengthSeconds` e `viewCount`;
    `/channel/<id>/about` da inscritos. Primeira leitura de Porta 1 em 17
    rodadas: **68 / 20 / 8** (16/10 03:3x contra 15/10 07:13, 20,4 h, delta ZERO
    nos tres). E as **17 duracoes reais** parqueadas sairam todas.
 2. **REGRA (h)** — `yt-dlp` baixa a faixa de legenda (71 KB, 1.381 palavras).
    O `timedtext` direto volta vazio; nao insista nele.
 3. **FONTES INSTITUCIONAIS** — Sejm e Eurostat devolveram DADO REAL, ELSTAT 200,
    gov.br 301. **LONGO NOVO voltou a ser possivel**, e com ele o pedido de
    1 longo + 1 curto por canal por dia deixa de ser promessa vazia.

**E A FROTA ANDA ABAIXO DE 1,18 INSCRITO/DIA** — o "+1,79/dia" que eu carregava
desde 12/10 preveria ~1,5 inscrito nessas 20,4 h, e o delta foi zero nos tres
canais. Delta zero nao estabelece ritmo: estabelece um LIMITE SUPERIOR.

Pendencia 2 segue de pe para `execute_sql`/`videos` (18 linhas parqueadas) e a
pendencia 1 para RETENCAO, que o sandbox nao da (e Analytics, nao publico).

## 16/10, 04:1x — a rota nova mudou a PAUTA, e quatro testes meus cobravam identidade

**Publicado:** `kolejny-poziom-s039` = `RT_qRi_S1Mw`, **43/44 s**, `status OK`,
12 tags, **capa propria** (`maxres2` conferido no ar) — segunda peca da frota com
capa desenhada.

**E A ESCOLHA DE PAUTA DEIXOU DE SER EMPURRADA PELO BANCO.** As cinco rodadas
anteriores foram para a banda mais usada porque a origem de menor uso nao tinha
spec local e a regra (h) dependia do `pg_net`. Com o `yt-dlp` no sandbox a
`Xgt32iH8Ft8` — UM short so, pulada por dias — virou pauta: 1.375 palavras.

**41o ponto da banda, o PRIMEIRO lido pelo sandbox:** previsao edge 41,5 ->
real 44, provedor **edge MEDIDO** (zero avisos no job `116806511162`), residuo
**+2,5**, sinal ESTABELECIDO. `RESIDUO_N` = 41, 36 estabelecidos, limites
intocados. As outras 17 duracoes parqueadas NAO entraram: provedor nao medido.

**E QUATRO TESTES MEUS REPROVARAM POR IDENTIDADE na mesma rodada** — `== 40`
cravado em `test_TODOS_os_40_pontos_seguem_POSITIVOS`,
`test_a_banda_cobre_os_residuos_medidos`,
`test_a_contagem_de_estabelecidos_e_34_de_39` e
`test_a_banda_e_a_OBSERVADA_e_o_teto_dela_foi_AMPLIADO_pelo_752`. Mesma classe do
743/753/761, e eles iam reprovar **a cada peca nova** — que e o jeito mais rapido
de um teste deixar de avisar. Reescritos para propriedade monotona.

**O quarto so apareceu na suite INTEIRA** (26 contra a linha de base de 25): os
tres primeiros sairam no `-k`, e o quarto estava num arquivo que o filtro nao
pegava. **Rodar o `-k` nao substitui a suite** — foi o que me pegou aqui.

**Windsor: conectado, mas so com o `bling`.** O conector de YouTube (que puxa
Analytics, a pendencia 1) esta em
https://onboard.windsor.ai/connect?connector=youtube&next=/youtube/authorize
e exige escolher a **Conta de Marca** de cada canal. **Nao confirmei que ele
entrega retencao** — `get_fields` recusa sem conta conectada.

Banco negado: decima oitava rodada. 19 linhas parqueadas.

## 16/10 05:2x — epomeno-epipedo-s041 no ar, e o banco nega pela 20a rodada

`execute_sql` devolveu `-32600` ("You do not have permission") na **20a rodada
seguida**. Pelo 777 isto NAO diz se o conector foi reapontado ou se a permissao
do projeto foi retirada — as duas produzem a mesma resposta. O que segue
funcionando e a publicacao, pelo `retomar.yml` com o `YT_OAUTH_JSON`.

**Peca publicada:** `QH9xoIC69jM` (`epomeno-epipedo-s041`), origem
`h66MCKjwAJ8` — origem de UM short so e sem spec local, alcancada pela rota do
sandbox (yt-dlp, 1.208 palavras). Onze portoes verdes, provedor **edge**
MEDIDO (zero avisos no job `116823350313`), previsao 41,6 no PISO, real **42**.

**O que o dono precisa fazer, e a ordem mudou pelo 777:** reconectar o conector
do Supabase escolhendo a organizacao do projeto `vevocauwtarctfwngrch`. Sem
`execute_sql` nao ha `pg_net`, logo nao ha leitura de inscritos, nem duracao
real pelo banco, nem registro em `videos` — e as **20 linhas** parqueadas em
`docs/pendente/videos-a-inserir.sql` continuam fora do banco. Sem `origem_id`
em `videos`, a `consultas/estoque.sql` nao sabe que estas origens foram
consumidas (670).

**Storage em 402 outra vez:** `thumbnail.png` e `short.mp4` nao subiram ao
bucket. A publicacao no YouTube nao depende disso, e a capa propria foi
confirmada pela rota do sandbox (`maxresdefault` 200, 57 KB; `maxres2` 200).

## 16/10 06:1x — kolejny-poziom-s040 no ar, e o LIMITE da frota aperta

**Peca publicada:** `7KZjro4H8ls` (`kolejny-poziom-s040`), origem `MjI4ZGJAhIo`
— uma das duas menos usadas do canal, sem spec local, alcancada pela regra (h)
atraves da legenda `pl` (1.242 palavras). Onze portoes verdes, provedor **edge**
MEDIDO (zero avisos no job `116839333951`), previsao 41,7.

**LEITURA DE INSCRITOS QUE VALE A JANELA:** 16/10 06:1x contra 15/10 07:13, isto
e **23,1 h** — **68 / 20 / 8**, delta ZERO nos tres. O piso de resolucao dessa
janela e **1,04/dia**, logo os tres saem `indeterminado` (criterio do 723: duas
contagens) e o que se afirma e um LIMITE SUPERIOR: **a frota anda abaixo de
1,04 inscrito/dia.** E uma cota mais apertada que a de 1,18 da janela de 20,4 h
de 03:3x, e ela continua derrubando o "+1,79/dia" que eu carreguei desde 12/10.

**O que isto significa para "ate fim de outubro": segue impossivel por ordem de
grandeza.** O modulo pede, na conversao MEDIDA de 1,2 por mil, de **24.000 a
27.333 views/dia num unico canal** — contra ~2.100/dia da frota inteira. A 20 por
mil cairia para 1.440 a 1.640/dia, que e alcancavel; logo a alavanca continua
sendo CONVERSAO, e conversao nao se mede sem o escopo de analytics.

**A SINCRONIA DA ROTINA COM O PROMPT DO TRIGGER E UM BLOQUEIO, nao um atraso
meu — e agora esta MEDIDA.** O `get_trigger` devolveu o prompt gravado com
**64.506 bytes** (md5 `d03be9a6ff6ab79aee8dfd627faafb7f`) contra **64.891** do
`docs/ROTINA.md` (md5 `45d3629f36fb70a409e8ddede25f7e54`): **238 linhas
diferentes**, 111 so no prompt e 127 so no arquivo. O que falta no prompt e a
§6-bis — o processo de producao que o dono pediu em 16/10, as tres rotas do
sandbox e a tabela de estilo por canal.
**Por que eu nao aplico:** o `update_trigger` exige o corpo INTEIRO como
argumento, o que obriga a reproduzir 64.891 bytes pela minha propria saida. Uma
letra trocada dentro de uma trava e defeito SILENCIOSO e durável, e governaria
toda rodada futura — a mesma assinatura que matou tres runs no `estado_b64`.
**Enquanto nao houver caminho que LEIA o arquivo, quem governa e o `CLAUDE.md`**,
que o proprio prompt manda ler primeiro e que carrega a §6-bis com essa
declaracao escrita. Eu paro de prometer a sincronia a cada rodada.

## 16/10 07:1x — as rotas do sandbox DEGRADARAM em quatro horas

Sondadas uma a uma: inscritos (`/channel/<UC…>/about`) **abre**; fontes
institucionais **abrem** (Eurostat 200, Sejm 200); **duração FECHOU** (o
`/watch?v=` devolve HTTP 200 com 1,2 MB e ZERO `lengthSeconds`, com marcador
`CONSENT`); **legenda FECHOU** (`yt-dlp`: *"Sign in to confirm you're not a
bot"*). Cookie de consentimento, User-Agent de navegador e `&hl=en` nao
resolvem.

**Consequencia para o dono:** as duracoes reais do `7KZjro4H8ls` e do
`QH9xoIC69jM` ficaram sem medicao, e a regra (h) voltou a estar fechada. O que
devolve as duas e a **reconexao do conector do Supabase** na organizacao do
projeto `vevocauwtarctfwngrch` — com `execute_sql` volta o `pg_net`, e com ele a
leitura de duracao real e a de legenda pela API, que nao dependem desta rota.

## 16/10 08:2x — a rota VOLTOU, e o limite da frota caiu abaixo de 1/dia

**As rotas que eu medi fechadas as 07:1x voltaram as 08:1x** — `lengthSeconds` e
`yt-dlp`, as duas. Isso e a propria regra do achado funcionando: rota e ESTADO.
Com ela vieram os dois reais parqueados: `7KZjro4H8ls` 41,7 -> **43** (+1,3) e
`stj6tmBAOLI` 41,5 -> **43** (+1,5), os dois com provedor edge MEDIDO e sinal
estabelecido, os dois DENTRO da banda. `RESIDUO_N` = 44, 38 estabelecidos.

**INSCRITOS, leitura de 25,1 h (16/10 08:2x contra 15/10 07:13): 68 / 20 / 8,
delta ZERO nos tres.** O piso de resolucao da janela e **0,96/dia**, logo o
limite superior da frota passou a ser **menos de 1 inscrito por dia** — mais
apertado que o 1,04 de duas horas antes e que o 1,18 de 03:3x. Os tres canais
saem `indeterminado` pelo criterio das duas contagens (723).

**O que isto significa, e e aritmetica:** com a frota abaixo de 1/dia, os 432 que
faltam ao `labtreinamento` levam mais de 450 dias — passando de 1/FEV/2027, quando
a barra sobe de 500 para 1.000. **Nenhum canal fecha a Porta 1 no ritmo medido**,
e a alavanca continua sendo CONVERSAO, nao volume.

**Peca publicada:** `Z8KZL5z8nxI` (`labtreinamento-s059`), origem `FtCtIJPsc_Q` —
o longo que o dono apontou. 23 linhas agora parqueadas em
`videos-a-inserir.sql`, esperando `execute_sql`.

## 16/10 11:4x — eu fui pela rota LONGA por tres rodadas, e o texto estava no disco

**RETRATACAO medida, e quem me pegou foi um teste meu.** Eu afirmei em 14/10
(aprendizados 759/761) que `StQNFMdpGdk` e `KRUERlNPzDw` **nao tinham spec
local**, e por isso usei a rota da LEGENDA (regra h) nelas. Elas sao o
`labtreinamento-002` e o `-003`, com **87 e 84 capitulos** no disco.

O falso negativo era do RESOLVEDOR, nao do dado: o `segundo_angulo.pacote_do_id`
le o vinculo `origem -> pacote` da COPY de um short que nomeie o pacote, logo e
cego para origem que ainda nao gerou short com esse texto. O mapa
`youtube_id -> pacote` esta no retrato da ponte desde sempre.

**O custo:** tres rodadas pela rota longa para texto que estava a um `json.load`
de distancia. A rota da legenda funcionou e era legitima — ela so nao era
necessaria. **Consertado** (`concentracao.escrevivel` consulta o retrato como
ultimo recurso), com contraprova: `FtCtIJPsc_Q`, que de fato nao tem pacote no
retrato, continua `False`.

**E O RUN PODE SER MISTO — primeiro medido.** O job `116943785023` devolveu
**DOIS** avisos `NARRACAO PELO PIPER` em dez cenas: oito pelo edge, duas pelo
Piper. Eu vinha tratando a contagem como interruptor de duas posicoes (0 ou 10)
porque todos os pontos anteriores vieram assim. **Consequencia para a banda:**
run misto nao tem mundo de provedor, logo o ponto NAO entra na serie do residuo
— nem `edge` nem `piper` descreve a duracao de uma peca narrada pelos dois.

**Inscritos, janela de 28,2 h:** `epomeno-epipedo` de 20 para **21**, o primeiro
delta nao-zero da sessao. Os outros dois iguais. Piso de resolucao 0,85/dia, logo
e UMA contagem e sai `indeterminado` (723) — mas diz que o limite de ~0,85/dia
nao e um zero disfarcado.

## 16/10 — O ESTILO MS PAINT: estudado, montado, e BLOQUEADO por credito

O dono trouxe o prompt de geracao de imagem (stickman de MS Paint, um quadro por
timestamp) e pediu para estudar. Estudado contra o codigo:

**O QUE SO ELE RESOLVE, e e uma linha:** o saldo da Higgsfield esta em **ZERO
credito, plano free, sem cota de geracao gratuita** (`unlim.available: false`).
Hoje nao sai **uma** imagem de teste. Custo medido no preflight:
**0,25 credito por imagem** (`gpt_image_2_5`, a familia "GPT Image" que o
proprio prompt dele nomeia).

  short de 10 cenas ...........  2,50 cr
  peca de 2 min (40 cenas) ..... 10,00 cr
  longo de ~9 min (109 frases) . 27,25 cr
  no alvo de 7/dia/canal ....... ~52 cr/dia  (~1.575 cr/mes)

**O QUE JA ESTA PRONTO DO NOSSO LADO:** `fabrica/estilo_paint.py` monta o prompt
POR CENA a partir da fala do narrador, com o bloco de estilo e as proibicoes
dele inteiras, e `tests/test_estilo_paint.py` (oito testes) trava isso — tudo
testavel sem gastar credito, porque e transformacao de texto.

**E a rota de render NAO precisa de obra:** cena com `layout: "broll"` e
`broll_url` ja existe e e nao invasiva — se a imagem falhar, a cena cai no texto
sobre fundo escuro e o render nao para. Falta so o passo que gera e HOSPEDA os
PNG, e hospedar depende do Storage, que esta em 402.

**DUAS COISAS QUE EU MUDEI NO PROMPT DELE, com motivo:**
1. **aspecto por FORMATO**: ele pede 16:9 em toda imagem, o que descreve o
   LONGO; o short da maquina e 9:16. O estilo atravessa, o aspecto nao.
2. **imagem SEM TEXTO**: ele admite texto escrito a mao, e dois tercos da frota
   narram em grego e polones, onde gerador erra diacritico. O nosso texto sai do
   `cairosvg` e e o que os portoes `ortografia` e `variedade` conferem. Desenho
   embaixo, texto nosso em cima.

## 16/10 — O LONGO DE 8 MIN, QUADRO POR QUADRO: a distância NÃO é efeito

Você pediu: *"Preciso que entenda o vídeo publicado de 8 min do canal
labtreinamento frame por frame."* Está medido, e o resultado é o oposto do que eu
esperava.

**A rota voltou.** Uma hora antes eu lhe disse que os efeitos não estavam
medidos, porque o download do vídeo dava 403 em quatro clientes. No mesmo
sandbox, uma hora depois, a lista de formatos abriu inteira e o arquivo baixou em
menos de um segundo. É a mesma lição da tabela de rotas: **rota é estado.**

**Medido com o método do 690/699** (escala absoluta de 0 a 255):

| | mediana de movimento | quadros congelados |
|---|---|---|
| **a referência (este longo de 8 min)** | **0,072** | **96%** |
| nossa peça pior (`labtreinamento-s011`) | 0,39 | 91% |
| nossa peça consertada (`kolejny-poziom-s017`) | 0,63 | 73% |

**A referência é 5 a 9 vezes MAIS estática que as nossas peças.** Ela não tem
b-roll, não tem foto, não tem rosto, é monocromática (saturação 3,4 a 5,6) e
escura (nenhum quadro claro em 530). O mundo visual dela é exatamente o nosso.

**Então "replicar os efeitos" não é o caminho — nós já temos mais efeito que
ela.** A distância que você viu é outra, e são três coisas:

1. **Um trilho de capítulos permanente no topo** — `1 A armadilha | 2 Os três
   limites | 3 O que o PROCX muda | 4 Quando usar cada um`, com o capítulo atual
   destacado. É por isso que **nenhuma transição é dura**: o trilho e a marca
   d'água nunca saem da tela, só o painel central troca. O espectador sempre sabe
   onde está. Nós não temos isso.
2. **18,9 s por plano** (28 transições em 530 s). A nossa cadência é **3,1 s**.
   Seis vezes mais tempo por tela é o que dá espaço para mostrar uma fórmula e
   anotar cada argumento dela — o que em 3 s não cabe.
3. **Cinco layouts que o nosso `layout.py` não tem**: fórmula anotada argumento
   por argumento, comparação de duas colunas com ✗/✓, cartão de erro (`#REF!`,
   `#N/D`), divisor de parte (`PARTE 2`) e cartão de número grande (`2019`).

**E as três são de LONGO, não de short.** 18,9 s por plano não existe num short
de 40 s, e trilho de capítulo num 9:16 não tem onde morar. Isso cai exatamente na
**metade do seu pedido de 16/10 que ainda não começou** — *"1 vídeo longo e outro
curto"* por canal. Não mexi em nenhum parâmetro de short.

**A decisão que é sua:** se eu construo esses cinco layouts e o trilho de
capítulo para o LONGO. É trabalho de render, não de pauta, e não consome crédito
de imagem nenhum — é texto em painel, igual ao que já fazemos.

## 16/10 — PESQUISA: "quero bater recordes, destravar a máquina"

Você pediu para eu estudar GitHub, YouTube, blogs de fora e os artigos mais
lidos. Estudei. **O resultado é que o destravamento é UM clique seu, e agora eu
sei exatamente o que ele compra e o que não compra.**

### O que a web deu (quase nada) e o que a fonte primária deu (tudo)

Os blogs sobre "retenção nos três primeiros segundos" devolveram **10–30%,
15–25%, 30–50% e ">80%"** — quatro fontes, nenhuma oficial, todas se
contradizendo. Nada disso entrou.

O único item aproveitável foi o **nome** de uma métrica, que me levou à
documentação oficial da API. E lá estava o que importa:

- **`audienceWatchRatio`** — *"a proporção absoluta de espectadores assistindo
  ao vídeo em dado ponto"*. **É a curva de retenção, peça por peça.**
- **`relativeRetentionPerformance`** — *"quão bem o vídeo retém espectadores
  comparado a TODOS os vídeos do YouTube de duração semelhante"*, de 0 a 1,
  ponto a ponto.

**O segundo é o achado central de toda a pesquisa**, e a razão é aritmética: ele
já vem **normalizado contra a população do YouTube**. Isso dispensa construir
linha de base com 109 peças por braço — que é exatamente o número que hoje torna
os experimentos indecidíveis. Com ele, **uma peça já diz se o gancho prendeu.**

**A chamada é UMA por vídeo, e o escopo `yt-analytics.readonly` JÁ está no nosso
código desde 09/10.** Falta só o seu clique nos dois links de
`docs/reautorizar-analytics.md`.

**E o que o clique NÃO compra, para eu não lhe prometer:** a métrica de swipe
("Viewed vs swiped away"). Contei na página oficial: `swiped` aparece **zero**
vezes. Ela é só do Studio, não da API.

### Uma rota grátis que eu achei — e por que ela não nos serve ainda

`yt-dlp --dump-json` entrega um campo `heatmap` com **100 baldes** de 0 a 1, sem
OAuth, sem banco, sem custo. Funciona.

**Mas é a curva de REPLAY, não de retenção** — marca onde as pessoas VOLTAM, não
onde ficam. Lidos quatro vencedores do nosso nicho, o pico cai no **meio** da
peça (11,6 a 36,3 s) e a média dos três primeiros segundos é **menor** que a do
resto nos quatro. Quem lesse isso como abandono leria ao contrário.

**E ela exige escala que nós não temos.** Medi doze peças do nicho
`excel/planilha`:

| views | heatmap |
|---|---|
| 5.490 / 12.662 / 22.935 / 45.332 | **não** (4 de 4) |
| 63.492 a 839.127 | **sim** (8 de 8) |

O limiar está entre **45 e 63 mil views** — e não os "~10 mil" que um blog
afirmava. A melhor peça da frota tem ~1.600 views: estamos um fator ~30 abaixo.

**Para que ela serve, então:** ler a forma dos vídeos do nosso nicho que
**romperam**. É a única leitura de atenção disponível hoje sem o seu clique.

### O que eu NÃO sei, e vai dito

Se o relatório de retenção cobre **Shorts**. A documentação menciona Shorts, mas
não consigo testar sem o escopo. Prometer a curva do short antes do clique seria
afirmar sem medir.

**No código:** `fabrica/retencao.py` e dez testes, incluindo um que reprova se
alguém chamar o heatmap de "retenção" e um que abre o `tokens.py` para provar
que o escopo já está lá — ou seja, que a pendência é o clique e não o código.


## 16/10 17:2x — a rota da DURAÇÃO reabriu, e a da LISTAGEM não

`epomeno-epipedo-s045` = `53GpMFpGuks`, **44 s reais** contra previsão edge de
41,8 (provedor **edge** medido, zero avisos no job `117099160058`): resíduo
**+2,2 s**, dentro da banda e com o sinal estabelecido. A exposição que a copy
declarou — real podendo passar do teto de 45 — **não se realizou**, e isso fica
dito porque o acerto é out-of-sample.

**A rota da duração voltou**, logo a banda do resíduo tem instrumento outra vez;
o `s040` e o `s041` seguem sem leitura, e isso continua devendo.

**E a sonda das quatro rotas no mesmo minuto derrubou uma hipótese minha** que eu
nunca havia escrito nem testado: a de que o bloqueio era do sandbox, uma maré.
Não é — a listagem fecha enquanto três rotas abrem. Detalhe em `CLAUDE.md`.

**Sua, e é a décima negativa seguida:** o `execute_sql` segue negado, logo as
**32** linhas de `insert into videos` em `docs/pendente/videos-a-inserir.sql`
continuam fora do banco. E o clique dos dois consentimentos do Google segue sendo
a ação de maior valor da fila — `relativeRetentionPerformance` é o comparador que
funciona com **uma peça só**.

## 16/10 18:1x — a peça do kolejny e a contagem que saiu da minha linha de comando

`kolejny-poziom-s044` = `MvmwHqFmYvY`, **43 s reais** contra previsão edge de
41,7 (provedor **edge** medido, zero avisos no job `117122802245`): resíduo
**+1,3 s**, dentro da banda e com sinal estabelecido. Mirei o **PISO** do
`ALVO_SHORT`, que é o que a voz polonesa pede, e a exposição do teto de 45
declarada na copy **não** se realizou. Som LUFS −13,8, desvio 0,2, zero silêncios.

**E um item de construção que é hábito meu, não defeito de código:** eu vinha
contando o DIA — o número que escolhe qual canal produz — com um `re` escrito à
mão na linha de comando, uma vez por rodada. Agora é
`concentracao_frota.contagem_do_pendente(desde)`, irmão do `ultima_do_pendente`,
com o mesmo aviso de PISO e seis testes.

**Ele já mostrou a divergência do 771 de graça:** nesta rodada o **dia** dava
6/7/7 e a **janela móvel de 24 h** dava 8/8/9 — as duas ordenam a frota de formas
diferentes, e é a móvel que não se apaga na virada da meia-noite.

**Sua, e é a décima primeira negativa seguida:** sem `execute_sql` as **33**
linhas de `insert into videos` seguem fora do banco, e a Porta 1 continua sem
poder resolver ritmo (68 / 21 / 8, os três indeterminados em 14,6 h).

## 16/10 19:1x — o portão pegou família repetida, e o instrumento calava sobre ela

`labtreinamento-s063` = `BwrCyzuFQT0`, **27 s reais** contra previsão edge de
25,9 (provedor **edge** medido, zero avisos no job `117149072618`): resíduo
**+1,1 s**, dentro da banda e estabelecido. **FORA do teto da mira do canal
(26,0) com o `mira.py` verde nos dois mundos** — o tally do 744/754 vai a **dez
de treze**, e a copy declarou essa exposição antes de publicar.

**O achado da rodada é contra mim.** A pauta serviu o topo do canal
(`FtCtIJPsc_Q`, o longo da referência), que **não tem spec local** — rota da
regra (h), com a legenda sondada **aberta** depois de estar fechada às 07:1x. Eu
escrevi o short inteiro sobre o terceiro limite do longo, e o portão
`similaridade` reprovou com 0,69 e depois 0,73: **não era título parecido, era a
família que o `labtreinamento-s059` já havia usado, saindo da MESMA origem.**
Troquei o título duas vezes antes de entender que o portão falava de conteúdo.

**E o `segundo_angulo.py` tinha a informação e a jogava fora.** No ramo sem spec
local ele dizia "use o `capitulos.yml`" e **parava ali**, descartando a lista de
shorts daquela origem que ele mesmo sabe calcular. Consertado: o ramo passou a
nomear as peças anteriores, a dizer quando é primeiro ângulo, e a declarar o
ponto cego que sobra — sem spec local ele nomeia **peças**, não capítulos.

**E uma falha nova apareceu na suíte, e era de um teste MEU:** ele cobrava
`abs(rho) < 0,5` sobre Spearman(usos, rank), de dois lados, quando a hipótese que
ele nega é de **um** lado só. O `rho` foi a **−0,54** — sinal oposto ao da
hipótese descartada, e efeito esperado da regra de recência servindo o topo.
Corrigido para o lado certo, com contraprova.

**Sua, e é a décima segunda negativa seguida:** sem `execute_sql` as **34** linhas
de `insert into videos` seguem fora do banco. Porta 1 em 68 / 21 / 8, os três
indeterminados em 15,6 h.

## 16/10 20:1x — o dia fechou em 22 peças, e o "7/7/7" merece uma ressalva

`epomeno-epipedo-s046` = `FmD7olILCwo`, **42 s reais** (a página trouxe dois
`lengthSeconds`, 41 e 42 — vale o maior) contra previsão edge de 41,3: resíduo
**+0,7 s**, dentro da banda mas com o sinal **NÃO estabelecido** pelo critério do
770. Som LUFS −14,0, desvio **0,0**, zero silêncios.

**O dia inteiro:** 22 peças publicadas, **8 / 7 / 7** por canal — e no momento da
escolha de canal estava **7/7/7**, isto é, o alvo que você pede por canal foi
atingido nos três.

**E aqui vai a ressalva, porque sem ela o número engana:** essa contagem é de
peça **publicada**, e o seu alvo é peça **`processed`** (é a regra que nasceu da
retratação de 08/10). A condição `processed` vive no `videos.list` com
`part=status`, que pede token, que pede `pg_net`, que pede o `execute_sql` —
negado em **treze** rodadas seguidas. Então **eu não tenho hoje o número exato
que você pediu**, e dizer que tenho seria inventar.

**O que eu meço é um PISO, e ele está em `fabrica/vivacidade_publica.py`:** por
duas rotas públicas sem credencial — `lengthSeconds > 0`, que **nega** o `P0D`, e
`oembed` em 200, que diz pública e indexada. Medido nas 22 de hoje: **22 de 22 no
piso, nenhuma `P0D`**. O módulo imprime, em letra, a condição que ele não mede,
porque uma peça pode estar indexada e ainda fora de `processed` — já medimos isso.

**Sua, e é a décima terceira negativa:** as **35** linhas de `insert into videos`
seguem fora do banco. Porta 1 em 68 / 21 / 8, os três indeterminados em 16,6 h.

## 16/10 21:1x — o primeiro resíduo ZERO, e quatro testes meus caíram com ele

`kolejny-poziom-s045` = `keI7ycnCSmY`, **41 s reais** contra previsão edge de
**41,0** (provedor **edge** medido, zero avisos no job `117197352639`): resíduo
**0,0** — o primeiro da série em 55 pontos. Som LUFS −13,9, desvio 0,1, zero
silêncios.

**O que isso muda, e vai dito porque é piora:** o piso da banda cai de 0,1 para
**0,0**, a largura vai a **4,0 s** contra 1 s de granularidade do real, e a frase
que eu venho escrevendo desde o 734 — *"N de N acima da previsão"* — **cai pela
quarta vez**. A propriedade que a série sustenta passa a ser **não-negativo**; o
positivo estrito vale só nos pontos estabelecidos. **Quinta** correção da banda, e
todas as cinco a alargaram.

**E o sinal deste ponto não está estabelecido:** com arredondamento para cima,
real 41 significa duração verdadeira em (40; 41], e a previsão de 41,0 cai dentro
desse intervalo — o resíduo verdadeiro está em (−1,0; 0,0] e **pode ser negativo**.

**Quatro testes meus reprovaram, e os quatro estavam certos em reprovar.** O mais
útil: um deles cobrava que, na janela de 41–42 s, o real **maior** viesse da
previsão **menor** — o oposto de uma relação monótona. Com este ponto o extremo
inferior passou a casar no sentido monótono, e o teste caiu. **Nenhuma das duas
versões era a propriedade certa:** com 1,0 s de largura de previsão e 1 s de passo
no real, a janela **não ordena em sentido nenhum**. Reescrito para medir a
correlação — hoje **+0,32** com 29 pontos — e reprovar só se ela ficar forte.

**E a largura da janela chegou exatamente ao passo do instrumento (1,00 s)**, que
é a fronteira que o 768 nomeou. Registrada, não suavizada.

**Sua, e é a décima quarta negativa:** as **36** linhas de `insert into videos`
seguem fora do banco. Porta 1 em 68 / 21 / 8, os três indeterminados em 17,6 h.

## 16/10 22:1x — o número que eu vinha te reportando estava SUBCONTADO

`labtreinamento-s064` = `cInP4dHee4s`, **28 s reais** contra previsão edge de 25,9
(provedor **edge** medido, zero avisos no job `117219367300`): resíduo **+2,1 s**,
dentro da banda e estabelecido. Som LUFS −13,4, desvio 0,6, zero silêncios.

**E aqui vai uma correção que é minha e é do número que te interessa.** A
contradição que está na sua fila há dias — previsão **dentro** da mira do canal e
duração **real fora** dela — eu relatava a cada rodada: *"cinco de sete"*, *"dez
de treze"*, *"onze de quatorze"*. Esses números saíam da minha cabeça: eu
incrementava o da rodada anterior em vez de recontar a série.

**Medido agora, pelo código: 20 de 23.** Eu estava subcontando, e no sentido
pior — o erro fazia o problema parecer **menos frequente** do que é, justamente
no número que sustenta um pedido a você. Agora é
`mira.tally_fora_da_mira` / `relato_do_tally`, com sete testes.

**Ressalva que vai junto, porque é confundidor real:** o tally aplica a mira
**atual** a todas as peças da série, inclusive as escritas na fronteira do
override de 13/10. Para essas pode ser mira retroativa. O número é o melhor que
existe e não é limpo.

**O que isso muda na sua fila:** a decisão do 740/748 — mover a mira para o
estimado descontando o resíduo, ou parar de cobrar uma faixa de real sobre o
estimado — passa de "acontece em dez de treze" para **"acontece em 20 de 23"**.

**E a décima quinta negativa do `execute_sql`:** as **37** linhas de `insert into
videos` seguem fora do banco. Porta 1 em 68 / 21 / 8, os três indeterminados.

## 16/10 23:1x — previsão IDÊNTICA, real diferente em 10 dos 14 grupos

`epomeno-epipedo-s047` = `o88cB0-ml8A`, **41 s reais** contra previsão edge de
**41,0** — o **segundo resíduo zero**, e com a mesma previsão do primeiro (o
`kolejny-poziom-s045`, duas horas antes). Som LUFS −14,1, desvio −0,1, zero
silêncios. O dia fechou **8/8/8** por canal.

**E esse par repetido abriu a medição que faltava.** A reprodutibilidade da
previsão já foi afirmada e negada três vezes aqui, sempre com o mesmo defeito:
comparar peças de previsão **próxima**, onde o passo de 1 s do real explica
qualquer coisa. Agrupei por previsão **idêntica**, que remove esse confundidor:

| | |
|---|---|
| grupos de previsão idêntica | **14** |
| reproduzem o mesmo real | **4** |
| **divergem** | **10** |
| maior divergência | **2 inteiros** (25,0 → 27 e 29) |

E o grupo de 41,6 tem **oito** peças, devolvendo 42 e 43.

**Logo a mesma previsão não determina o real** — e isso é mais forte que tudo o
que eu disse antes sobre isso, porque não depende de janela. **Retrata uma
afirmação minha:** eu havia escrito que "a mesma previsão devolveu o mesmo real
duas vezes"; aquele par é um dos quatro que reproduzem, e eu generalizei de **um**
grupo. O que sobrevive é a aritmética da pinça, que não depende disso.

**O que isso não diz:** que a previsão seja inútil. Ela acerta o inteiro ou erra
por um na maioria dos grupos. O que cai é a palavra **determina** — e a
consequência prática é que a faixa que eu anuncio antes de publicar é o melhor
que existe, e não vai ficar mais estreita por medir mais.

**E a décima sexta negativa:** as **38** linhas de `insert into videos` seguem
fora do banco. Porta 1 em 68 / 21 / 8, os três indeterminados em 19,6 h.

## 17/10 00:1x — a meia-noite zerou o contador, e o conserto de 15/10 funcionou

`kolejny-poziom-s046` = `-j_lMIB5Yt0`, **43 s reais** contra previsão edge de 40,6
(provedor **edge** medido, zero avisos no job `117254439119`): resíduo **+2,4 s**,
dentro da banda e estabelecido. Som LUFS −14,0, desvio **0,0**, zero silêncios.
`RESIDUO_N` = 58.

**E esta rodada foi a primeira verificação em produção de um conserto de 15/10.**
Naquele dia o contador do dia devolveu 0/0/0 na virada da meia-noite e não ordenou
nada exatamente na rodada que precisava escolher canal; a saída foi a **janela
móvel de 24 h**. Depois disso todas as rodadas caíram dentro do dia, e o caso
nunca se repetiu — até agora:

| contagem | labtreinamento | epomeno | kolejny | ordena? |
|---|---|---|---|---|
| dia calendário (17/10) | 0 | 0 | 0 | **não** |
| janela móvel de 24 h | 8 | 9 | 8 | **sim** |

**Vinte e cinco peças das últimas 24 h sumiriam do critério** se só o dia
calendário decidisse. A móvel escolheu `kolejny-poziom`, e a peça saiu dali.
`tests/test_o_contador_do_DIA_zerou_na_virada_E_a_movel_ordenou.py`, seis testes.

**O que isso não reivindica:** que o canal escolhido seja o melhor. O valor do
conserto não é acertar o canal — é **não ficar sem critério** na única hora do dia
em que o contador do dia é cego.

**O dia 16/10 fechou em 8 / 9 / 8 por canal** pelas linhas parqueadas — acima dos
sete que você pede, nos três.

**E a décima sétima negativa:** as **39** linhas de `insert into videos` seguem
fora do banco. Porta 1 em 68 / 21 / 8, os três indeterminados — e vale a trava da
madrugada: rodada noturna é de medição e engenharia, nunca de veredito.

## 17/10 01:2x — décima oitava rodada sem banco

`execute_sql` negado outra vez. **São 40 linhas de `insert into videos`
parqueadas** em `docs/pendente/videos-a-inserir.sql`, e sem o banco eu também
não consigo ler `uploadStatus: processed`, que é o critério de contagem que o
dono pediu.

O que continua funcionando sem ele: render, publicação (`retomar.yml` com o
`YT_OAUTH_JSON`) e as leituras pela sandbox. `labtreinamento-s065` foi ao ar
nesta rodada (`a36Vk1kg62I`, 28 s reais).

**A reconexão do conector do Supabase segue sendo a única que devolve
`execute_sql` e `pg_net`** — e com eles a duração real, os inscritos pela API, a
rota da regra (h) pelo banco e o registro em `videos`.

## 17/10 02:1x — décima nona rodada sem banco, e o servidor MCP está DE PÉ

O `execute_sql` foi negado outra vez — e nesta rodada o **servidor MCP do Supabase
reconectou** no meio da sessão, com as chamadas de catálogo respondendo. Logo a
negação **não é servidor caído**: é acesso. São **41 linhas** parqueadas em
`docs/pendente/videos-a-inserir.sql`.

`epomeno-epipedo-s048` foi ao ar nesta rodada (`OhrGlJvnBoM`, 44 s reais).

## 17/10 03:1x — vigésima rodada sem banco, e a rota pública da duração fechou

`execute_sql` negado pela vigésima vez. **43 linhas** parqueadas.

E nesta rodada a rota pública que eu usava para ler a duração real **fechou** —
200 com 1,2 MB e zero `lengthSeconds`. Logo não consegui medir a duração de
`kolejny-poziom-s049` (`O5o2SnovdEo`), que foi ao ar normalmente. **Com o banco
de pé isso não aconteceria**, porque a duração sairia pela API com token.

## 17/10 04:1x — vigésima primeira negativa, e a rota pública da duração segue fechada

`execute_sql` negado. **43 linhas** parqueadas em `videos-a-inserir.sql`.

E agora há um segundo pendente: `docs/pendente/duracoes-a-medir.jsonl`, com as
**duas** peças publicadas enquanto a rota pública da duração está fechada
(`O5o2SnovdEo` e `6jHGn7fae4c`). **Com o banco de pé nenhuma delas estaria aí** —
a duração real sairia pela API com token, e a série de medição não teria parado.

## 17/10 05:1x — a rota pública reabriu, e os dois pendentes de duração saíram

A rota da duração voltou (controle conferido) e as duas peças parqueadas em
`duracoes-a-medir.jsonl` foram medidas: `O5o2SnovdEo` 44 s e `6jHGn7fae4c` 27 s.
Nenhuma medição foi perdida.

`execute_sql` segue negado (22ª vez) e as linhas de `videos` parqueadas vão a
**44**. Este é o pendente que não tem rota alternativa nenhuma.

## 17/10 07:3x — oitava peca do dia, e a 24a negativa do banco
`labtreinamento-s067` = `1pe2fp2CxV4` ("O recado é opcional"), **28 s reais**
contra previsao edge 25,6 (provedor MEDIDO: zero avisos de Piper no job
`117339028890`), residuo **+2,4 s**, dentro da banda e estabelecido.

**O que depende de voce, por ordem de valor:** (1) os dois cliques de
consentimento do Google (`docs/reautorizar-analytics.md`) — eles tambem destravam
a leitura de `processed`; (2) reconectar o conector do Supabase: sao **46** linhas
de `insert into videos` parqueadas em `docs/pendente/videos-a-inserir.sql`, e sem
`execute_sql` nenhuma entra; (3) a decisao do 740/748 — a mira deste canal
(20,0 a 26,0) e o real nao cabem juntos, e hoje sao **23 de 26** peças fora do
teto no mundo edge, todas com o `mira.py` verde.

## 17/10 08:1x — nona peca do dia, e a 25a negativa do banco
`epomeno-epipedo-s050` = `SFFlpK78uyo` ("Όχι η αρχική τιμή"), **43 s reais**
contra previsao edge 41,8 (provedor MEDIDO: zero avisos de Piper no job
`117349192781`), residuo **+1,2 s**, dentro da banda e estabelecido. **A peca
ficou ABAIXO do teto de 45** — ela foi escrita mirando o PISO da faixa, que e a
regra de redacao do 772.

**47** linhas de `insert into videos` seguem parqueadas em
`docs/pendente/videos-a-inserir.sql`, e sem `execute_sql` nenhuma entra.

## 17/10 09:1x — decima peca do dia, e a PRIMEIRA leitura de inscritos em 4 h
`kolejny-poziom-s051` = `RjlCqChKWJo` ("Poproś o harmonogram"), **42 s reais**
contra previsao edge 41,7 (provedor edge MEDIDO) — residuo +0,3 s, e o sinal
**NAO esta estabelecido** (abaixo do passo de 1 s do instrumento, pelo 770).

**INSCRITOS AO VIVO: 68 / 21 / 8**, contra os mesmos 68 / 21 / 8 de 05:0x —
janela de 4,1 h, **delta zero nos tres**. O `porta1.py` devolve os tres como
**indeterminado**: o piso de resolucao dessa janela e **5,85 inscritos/dia**, tres
vezes acima do ritmo medido da frota. **Para resolver ritmo nao bastam 4 h.**

**48** linhas de `insert into videos` seguem parqueadas, e sem `execute_sql`
nenhuma entra. A pendencia que mais vale continua sendo os dois cliques de
consentimento do Google.

## 17/10 10:1x — decima primeira peca do dia
`labtreinamento-s068` = `ogYsbBPzG_A` ("Uma fórmula, duas colunas"), **28 s
reais** contra previsao edge 25,9 (provedor edge MEDIDO), residuo **+2,1 s**,
dentro da banda e estabelecido. **49** linhas de `insert into videos` parqueadas.

**A pinça do 740/748 esta em 24 de 27** peças deste canal fora do teto da mira no
mundo edge, TODAS com o `mira.py` verde. Esta e a decisao 3 da sua fila, e ela
só piora com a contagem.

## 17/10 11:1x — decima segunda peca do dia, e a rota da duracao FECHOU
`epomeno-epipedo-s051` = `4v1ttezslTI` ("Κράτα και το όνομα"), publicada e
indexada. **A duracao REAL nao foi medida**, e o motivo e instrumento, nao peca:
a rota publica fechou, medida pela peca de CONTROLE `OhrGlJvnBoM` (44 s
conhecidos) — pagina de 1.208.851 bytes com ZERO `lengthSeconds`. A peca ficou
PARQUEADA e sai do pendente quando a rota reabrir.

**50** linhas de `insert into videos` parqueadas.

## 17/10 12:1x — decima terceira peca do dia, e a rota segue fechada
`kolejny-poziom-s052` = `GOrbPBGeCAY` ("Prawie to nie całość"), publicada.
**Duas pecas seguidas sem duracao REAL medida**, e a causa e instrumento: o
controle `OhrGlJvnBoM` (44 s conhecidos) voltou vazio em quatro sondagens desde
as 11:1x. As duas ficaram PARQUEADAS e saem do pendente quando a rota reabrir.

**51** linhas de `insert into videos` parqueadas. A pendencia que mais vale
continua sendo os dois cliques de consentimento do Google.

## 17/10 13:1x — decima quarta peca do dia, e a rota REABRIU
`labtreinamento-s069` = `7bD9doHFs-U` ("O que já está salvo"), **27 s reais**,
residuo +1,2 s estabelecido.

**A rota da duracao reabriu as 13:0x e os DOIS parqueados sairam de uma vez** —
`epomeno-epipedo-s051` (42 s) e `kolejny-poziom-s052` (43 s). Sem o parque esses
dois pontos estariam perdidos. O parque voltou a ZERO pendente, com onze peças
resolvidas.

**52** linhas de `insert into videos` parqueadas. A pinça do 740/748 esta em
**25 de 28** peças deste canal fora do teto da mira no mundo edge.

## 17/10 14:1x — decima quinta peca do dia
`epomeno-epipedo-s052` = `9r82v5RyVa4` ("Το σύνολο το φτιάχνεις"). **Duracao
REAL nao medida**: a rota fechou outra vez, confirmada pela peca de CONTROLE.
Parqueada; sai do pendente quando a rota reabrir (hoje ela abriu e fechou tres
vezes).

**INSCRITOS AO VIVO, janela de 5,0 h: 68 / 21 / 8** — delta ZERO nos tres, os
tres `indeterminado`. O piso de resolucao dessa janela e 4,8 inscritos/dia contra
~1,8 medido. **A leitura que de fato resolve ritmo cai depois das 22:1x.**

**53** linhas de `insert into videos` parqueadas.

## 17/10 15:1x — decima sexta peca do dia
`kolejny-poziom-s053` = `j_MvqNCT2h0` ("Bez kalkulatora"). Duracao REAL nao
medida — a rota segue fechada, confirmada pelo CONTROLE. **Dois parqueados**
(`epomeno-epipedo-s052`, `kolejny-poziom-s053`); eles saem juntos quando a rota
reabrir, como aconteceu as 13:0x.

**54** linhas de `insert into videos` parqueadas. **Dezesseis pecas hoje**, nos
tres canais, sem uma unica linha gravada em `videos` — e o motivo e a 32a negativa
seguida do `execute_sql`.

## 17/10 16:2x — labtreinamento-s070 no ar, e a rota da duracao reabriu pela SEGUNDA vez hoje

`KkhV7yI0nGo` ("O padrão trocou de lado"), 17a peca do dia. Provedor **edge**
MEDIDO (zero avisos `NARRACAO PELO PIPER` no job 117441677715). Previsao edge
**25,7** / piper 21,1, os doze portoes verdes, e a copy declarou a exposicao
ANTES de publicar: real entre 25,7 e 29,7 se o edge narrasse.

**Real 29 s** — residuo **+3,3 s**, DENTRO da banda (0,0 a 4,0) e com o sinal
ESTABELECIDO (29 − 25,7 > 1,0). `RESIDUO_N` = **74**, limites intocados.

A rota foi conferida pela peca de **CONTROLE** `OhrGlJvnBoM` ANTES de usar a
leitura: ela devolveu os **44 s** conhecidos, logo a rota estava ABERTA e o 29
e da peca. Parque em zero pendentes, catorze resolvidas.

**E o tally do 740/748 foi a 26 de 29:** 29 s contra um teto de mira de 26,0,
com o `mira.py` VERDE nos dois mundos. A decisao segue sendo sua.

**Parqueadas para `videos`: 55 linhas** em `docs/pendente/videos-a-inserir.sql`,
esperando o `execute_sql` voltar (34a rodada seguida de negacao).

## 17/10 17:1x — epomeno-epipedo-s053 no ar, e a rota da duracao FECHOU de novo

`WF3684zyRWo` ("Μετρά έδαφος, όχι εσένα"), 18a peca do dia. Provedor **edge**
MEDIDO (zero avisos no job 117454412202). Previsao edge **41,6** — o PISO do
`ALVO_SHORT`, pelo 772 — e piper 36,8, os doze portoes verdes.

**NAO HA PONTO DE RESIDUO NESTA RODADA, e a razao e medida.** A peca de CONTROLE
`OhrGlJvnBoM`, que leu **44 s** uma hora antes, voltou **VAZIA** na mesma
chamada. Peca de dias de vida nao desindexa, logo o que mudou foi a ROTA — e a
leitura vazia da peca nova nao diz nada sobre ela. A peca fica PARQUEADA e a
medicao vem quando a rota reabrir. Terceira vez hoje que ela abre e fecha.

**A ROTA DA LEGENDA ESTA FECHADA e isso custou a origem menos usada do canal.**
Sondadas na MESMA chamada: `yt-dlp --flat-playlist` devolveu a ordem viva com
duracao, e o download de legenda levou *"Sign in to confirm you're not a bot"*.
A regra (h) nao vale nesta rodada, logo o `eZ697VNYCPU` (um uso so, sem spec
local) ficou de fora por falta de INSTRUMENTO, nao por escolha.

Origem usada: `9U2h4HuAzLs`, rank **3** na ordem viva e **2 usos** — o rank 1
esta sob ALERTA de concentracao (12 de 52 shorts do canal).

**Porta 1 as 17:1x: 68 / 21 / 8**, janela de 8,0 h contra a leitura das 09:1x,
**indeterminado nos tres** — o piso de resolucao da janela e 3,00/dia contra
~1,8/dia medido. A primeira leitura que RESOLVE ritmo cai depois das **22:1x**.

**Parqueadas para `videos`: 56 linhas.** 35a rodada seguida sem `execute_sql`.

## 17/10 18:1x — kolejny-poziom-s054 no ar, e DUAS rodadas sem instrumento de duracao

`LuiLFR92AyQ` ("Nie brutto i nie netto"), 19a peca do dia. Provedor **edge**
MEDIDO (zero avisos no job 117466655474). Previsao edge **41,8** / piper 35,6.

**A rota da duracao SEGUE FECHADA** — a peca de CONTROLE `OhrGlJvnBoM` voltou
vazia outra vez, e com ela a peca parqueada da rodada anterior. **Duas peças
esperando medicao** (`epomeno-epipedo-s053` e esta), as duas por falta de
INSTRUMENTO e nao de peca. `RESIDUO_N` fica em 74.

**A rota dos INSCRITOS esta aberta: 68 / 21 / 8**, janela de 9,0 h contra as
09:1x — **indeterminado nos tres**, piso 2,67/dia contra ~1,8/dia medido. A
primeira leitura que RESOLVE ritmo cai depois das **22:1x**.

A peca nasceu **abaixo** do piso da mira (edge 39,5 contra piso 41,5) e foi
alongada em cinco passos ate 41,8. A exposicao vai declarada na copy: se o edge
narrar, o real cai entre 41,8 e 45,8 e PODE passar do teto de 45.

**Parqueadas para `videos`: 57 linhas.** 36a rodada seguida sem `execute_sql`.

## 17/10 19:1x — labtreinamento-s071 no ar, e TRES pontos de residuo numa rodada

`yFJUp1xhTe8` ("Fixo é o sinal do erro"), 20a peca do dia. Provedor **edge**
MEDIDO (zero avisos no job 117479645664). Previsao edge **25,2** / piper 20,7,
real **27** — residuo **+1,8 s**, dentro da banda e com o sinal ESTABELECIDO.

**A rota da duracao REABRIU pela TERCEIRA vez hoje**, conferida pela peca de
CONTROLE antes de usar a leitura, e as duas parqueadas sairam JUNTAS:
`epomeno-epipedo-s053` (41,6 -> 42, +0,4) e `kolejny-poziom-s054` (41,8 -> 42,
+0,2). Os dois sem sinal estabelecido pelo criterio do 770. Com o ponto desta
peca, **tres pontos numa rodada**. `RESIDUO_N` = **77**, limites intocados.

**E o tally do 740/748 foi a 27 de 30:** 27 s contra um teto de mira de 26,0,
com o `mira.py` VERDE nos dois mundos e a exposicao declarada antes de publicar.
A peca nasceu em edge 30,1, FORA da mira, e foi encurtada nas dez cenas de uma
vez.

A familia nova INVERTE o sinal de uma peca anterior do mesmo canal, e isso vai
dito na copy: no `s036` o desconto que VARIA e o sinal do erro; aqui o que NAO
varia e o sinal, porque o grupo tem base variavel por desenho.

**Porta 1 as 19:1x: 68 / 21 / 8**, janela de 10,0 h, indeterminado nos tres
(piso 2,40/dia). **Parqueadas para `videos`: 58 linhas.** 37a rodada sem
`execute_sql`.

## 17/10 20:1x — epomeno-epipedo-s054 no ar, e o PRIMEIRO residuo NEGATIVO em 78 pontos

`A4M3SLs8FEk` ("Λάθος στοιχεία, λάθος φόρος"), 21a peca do dia. Provedor **edge**
MEDIDO (zero avisos no job 117492664194). Previsao edge **41,6** e real **41** —
residuo **−0,6 s**, o primeiro NEGATIVO da serie.

**E o sinal dele ESTA estabelecido, ao contrario do que o meu proprio criterio
dizia.** O YouTube arredonda PARA CIMA, logo real 41 significa duracao verdadeira
em (40; 41], e 41,6 esta ACIMA de todo esse intervalo: o residuo verdadeiro vive
em (−1,6; −0,6] e e estritamente negativo. **O criterio do 770 era de UM LADO SO**
(`real − previsao > 1,0`) porque foi escrito quando todos os pontos eram
positivos — consertado para os dois lados, com nove testes.

**E isso derruba a frase "N de N acima" que eu venho escrevendo desde o 734.** Ela
nao vale mais. O que sobrevive e que a grande maioria e positiva. O piso da banda
foi a **−0,6**; `RESIDUO_N` = 78.

**E A ROTA DA LEGENDA REABRIU, tres horas depois de eu relatar a origem como fora
de alcance.** As 17:0x o `yt-dlp` no `eZ697VNYCPU` levou "Sign in to confirm
you're not a bot"; as 20:1x a MESMA chamada baixou 18,79 KB de VTT. Com isso a
origem **MENOS USADA do canal** (um short so, sem spec local) virou pauta pela
regra (h). Estado de ROTA, nao propriedade — a sonda vem antes de desistir.

**Porta 1 as 20:1x: 68 / 21 / 8**, janela de 11,0 h, indeterminado nos tres (piso
2,18/dia). **Parqueadas para `videos`: 59 linhas.** 38a rodada sem `execute_sql`.

## 17/10 21:1x — kolejny-poziom-s055 no ar, 22a peca do dia

`0DAQxf3d3JY` ("Milczenie to też wybór"), pl. Provedor **edge** MEDIDO (zero
avisos no job 117504992463). Previsao edge **42,2** / piper 35,9, real **43** —
residuo **+0,8 s**, dentro da banda e com o sinal NAO estabelecido pelo 770 (o
intervalo (42; 43] contem a previsao). `RESIDUO_N` = 79, limites intocados.
Rota aberta, conferida pelo controle (44 s) antes de usar a leitura.

Familia nova: **ACAO POR OMISSAO** — a renuncia nao e eterna, o reingresso volta
sozinho numa data da lei, e essa data se REPETE; logo nao agir e uma escolha.

**E a DATA e o caso mais claro da regra (g) que esta maquina ja encontrou:** ela e
o proprio ASSUNTO do short e ainda assim NAO entra, porque data de vigencia muda
por lei nova. O que nao muda e que ela existe e se repete.

**O caminho ate a duracao foi de vaivem, e as tres restricoes do 747 brigaram:**
40,4 (abaixo do piso) -> alongada -> o portao `ortografia` REPROVOU (3,4% de
letras acentuadas contra 6,9% do canal; em polones isso muda a pronuncia do TTS)
-> reescrita com palavras acentuadas (5,2%) subiu a 43,1, acima do topo ->
encurtada, fechou em 42,2. Prosodia e duracao se empurram.

**Porta 1 as 21:1x: 68 / 21 / 8**, janela de 12,0 h, indeterminado nos tres (piso
2,00/dia). **Parqueadas para `videos`: 60 linhas.** 39a rodada sem `execute_sql`.

## 17/10 22:1x — A LEITURA DE 13 H SAIU, e com ela o limite da frota

**Tres leituras na mesma rodada, as tres identicas: 68 / 21 / 8, delta ZERO nos
tres.** Janela de **13,0 h** contra as 09:1x — a primeira que o
`porta1.horas_para_resolver(1,79)` pedia. Piso de resolucao **1,85/dia**, logo o
que esta medido e um LIMITE SUPERIOR: **o ritmo da frota esta abaixo de
1,85/dia**. Os tres saem `indeterminado` pelo criterio do 723.

**O que isto NAO autoriza dizer:** que as 23 pecas de hoje trouxeram zero
inscrito. O contador de canal anda em DEGRAU que pode passar de 12 h (705), logo
inscrito ganho hoje pode nao ter aparecido ainda. O que esta medido e a JANELA,
nao a producao.

**O que isto derruba de vez:** o "+1,79/dia da frota" nao se sustenta em janela
nenhuma. A de 20,4 h de 16/10 ja o punha abaixo de 1,18/dia; esta confirma sem
contradizer. **O limite que vale e o menor: abaixo de 1,18/dia.** No melhor caso
isso poe os 432 inscritos que faltam ao labtreinamento a mais de um ano — depois
de 1/FEV/2027, quando a barra sobe para 1.000.

## A peca da rodada

`labtreinamento-s072` = `0cAcXlsjG3I` ("Quem fez não verifica"), 23a do dia.
Provedor **edge** MEDIDO, previsao edge **25,7** / piper 21,1, real **28** —
residuo **+2,3 s**, dentro da banda e ESTABELECIDO. `RESIDUO_N` = 80.

**A origem e a MENOS usada do canal (3 usos) e NAO tem spec local** — a que o
759/761 nomeia como a que eu vinha pulando. A rota da regra (h) estava aberta e o
texto saiu da faixa `pt-BR` de 13.737 bytes (a que a maquina subiu), nao da
automatica de 102.267.

**E o custo de RECENCIA vai declarado:** essa origem e o rank **13 de 14** na
ordem viva, doze posicoes atras do topo. Escolhi contagem contra recencia porque
concentracao ataca o portao `similaridade`, que e de monetizacao — mas o peso
entre as duas coordenadas nao esta medido, e isso fica como escolha, nao regra.

**Parqueadas para `videos`: 61 linhas.** 40a rodada sem `execute_sql`.

## 17/10 23:2x — epomeno-epipedo-s055 no ar, e o SEGUNDO residuo negativo

`Gxg3npta4Zo`, 41 s reais contra previsao edge de 41,5 (provedor MEDIDO, zero
avisos no job 117529604557): residuo -0,5, estabelecido pelo ramo negativo que
entrou as 20:1x. Os DOIS negativos da serie sao deste canal, com previsao 41,5 e
41,6 e real 41 — o negativo e raro (2 de 81) e mora na janela estreita do
768/769, nao e regime novo.

Rota da duracao ABERTA: a peca de CONTROLE (OhrGlJvnBoM) devolveu os 44 s
conhecidos na mesma chamada, que e o que separa rota fechada de peca nao
indexada.

Inscritos 68 / 21 / 8 — os tres `indeterminado`. A proxima leitura que pode
RESOLVER ritmo precisa de |delta| >= 2, o que no limite medido (abaixo de
1,18/dia) cai depois de ~41 h: nao antes da manha de 19/10.

O que segue na sua mao, por valor:
1. os dois cliques de consentimento do Google (`docs/reautorizar-analytics.md`) —
   e o unico caminho para RETENCAO, que e o que decide o que faz uma peca romper;
2. reconectar o conector do Supabase — e a unica rota que devolve `execute_sql` /
   `pg_net`, e com ela as 62 linhas parqueadas em `docs/pendente/videos-a-inserir.sql`;
3. a decisao do 740/748 (mira contra real), com a conta pronta.

## 18/10 00:1x — kolejny-poziom-s056 no ar, e o empate triplo chegou a SETE rodadas

`WGP0QtePCMU`, 43 s reais contra previsao edge de 41,7 (provedor MEDIDO, zero
avisos no job 117540417103): residuo +1,3, estabelecido, dentro da banda.
RESIDUO_N = 82. Rota da duracao ABERTA (controle OhrGlJvnBoM devolveu 44 s).

O contador de janela movel deu 7 / 7 / 7 — a frota esta perfeitamente
equilibrada ha sete rodadas, e o desempate vem saindo da peca mais antiga.

E a rodada teve a primeira vez em que as DUAS coordenadas da pauta concordam sem
desempate cego: a origem escolhida (`-5aMrDsxlZE`) e, ao mesmo tempo, do grupo de
MENOR uso (2, empatada com onze outras) e a de melhor rank na ordem VIVA (5 de
23). O peso entre as duas segue nao medido, e aqui nao foi preciso.

Inscritos 68 / 21 / 8 — os tres `indeterminado`. A janela desta rodada (15,0 h,
piso 1,60/dia) NAO aperta o limite da frota: o mais apertado segue sendo o
1,18/dia da janela de 20,4 h de 16/10. A proxima leitura que pode RESOLVER
ritmo precisa de |delta| >= 2, o que nesse limite cai depois de ~41 h — nao
antes da manha de 19/10.

Na sua mao, por valor:
1. os dois cliques de consentimento do Google (`docs/reautorizar-analytics.md`);
2. reconectar o conector do Supabase — unica rota que devolve `execute_sql` /
   `pg_net`, e com ela as 63 linhas de `docs/pendente/videos-a-inserir.sql`;
3. a decisao do 740/748 (mira contra real), com a conta pronta.

## 18/10 01:2x — labtreinamento-s073 no ar, e a playlist de uploads esta INCOMPLETA

`ixqFtjXC_AQ`, 28 s reais contra previsao edge de 26,0 (provedor MEDIDO, zero
avisos no job 117551494916): residuo +2,0, estabelecido, dentro da banda.
RESIDUO_N = 83. Rota da duracao ABERTA (controle devolveu 44 s).

TRES achados, e todos sao de instrumento meu:

1. A playlist `UU...` do labtreinamento devolve TREZE longos, e dois outros —
   StQNFMdpGdk (872 s) e XgqPVJuAk3o (785 s) — foram medidos como longos
   PUBLICOS do mesmo canal e NAO aparecem nela. O canal tem ao menos QUINZE.
   Eu vinha chamando essa playlist de "a ordem VIVA" e a usando como se fosse o
   conjunto completo; ela da a ORDEM, nao o conjunto.
2. A origem de ZERO usos era invisivel para quem escolhe pauta — o contador
   conta origem usada. O QiaGg03WSR0 (rank 4) nunca rendeu short e nunca foi
   oferecido. Instrumento novo: `concentracao.origens_sem_uso`.
3. DOIS shorts do kolejny (s004 e s035) declaram como origem um longo do
   LabTreinamento. O id esta errado, nao o conteudo. Consequencia que importa
   para o senhor: o `videos.origem_id` dessas duas pecas marca como consumida a
   origem ERRADA, logo a trava contra reusar origem esta cega na verdadeira.
   NAO corrigi o id, porque o id certo do kolejny-poziom-018 nao esta no retrato
   de 06/10 e sem `execute_sql` eu o adivinharia.

Inscritos 68 / 21 / 8 — os tres `indeterminado`, janela de 16,0 h (piso
1,50/dia). O limite mais apertado da frota segue sendo o 1,18/dia de 16/10.

Na sua mao, por valor: (1) os dois cliques de consentimento do Google; (2)
reconectar o conector do Supabase — 64 linhas parqueadas em
`docs/pendente/videos-a-inserir.sql`, e sem ele o item 3 acima fica sem conserto;
(3) a decisao do 740/748.

## 18/10 02:1x — epomeno-epipedo-s056 no ar, e o contador ordenou SOZINHO

`0lPTFY51IXs`, 43 s reais contra previsao edge de 41,5 (provedor MEDIDO, zero
avisos no job 117561762560): residuo +1,5, estabelecido, dentro da banda.
RESIDUO_N = 84. Rota da duracao ABERTA (controle devolveu 44 s).

A janela movel deu 8 / 8 / 7 — o epomeno sozinho no mais baixo, sem empate. E a
primeira rodada em sete em que o contador escolhe o canal por si, sem o
desempate pela peca mais antiga.

E a peca usou DUAS leituras de duracao na mesma pagina (42 e 43): foi usada a
MAIOR, que e a regra de 16/10, porque a banda foi construida sobre uma medida
que arredonda para cima.

A mira foi ao PISO (41,5) mesmo na voz grega, onde a regra antiga dizia que o
topo era seguro — porque foi mirando 42,5 que o `epomeno-epipedo-s032` saiu com
46 s reais, acima do teto do portao. O real deu 43: abaixo de 45.

E o instrumento novo de ontem (`origens_sem_uso`) devolveu LISTA VAZIA para este
canal — e isso NAO prova que nao ha origem livre, porque a playlist de uploads
omite longo publico. O proprio modulo avisa isso, e foi por ele que a escolha
caiu no grupo de uso minimo em vez de parar.

Inscritos 68 / 21 / 8 — os tres `indeterminado`, janela de 17,0 h (piso
1,41/dia). O limite mais apertado da frota segue sendo o 1,18/dia de 16/10.

Na sua mao, por valor: (1) os dois cliques de consentimento do Google; (2)
reconectar o conector do Supabase — 65 linhas parqueadas, e sem ele o id errado
de origem dos dois shorts do kolejny (achado de 01:2x) fica sem conserto; (3) a
decisao do 740/748.

## 18/10 03:1x — kolejny-poziom-s057 no ar, e o instrumento de ontem errou na primeira vez

`P2UxLtULR9E`, 42 s reais contra previsao edge de 41,5 (provedor MEDIDO, zero
avisos no job 117572513678): residuo +0,5, dentro da banda, e com o SINAL NAO
ESTABELECIDO — 42 - 41,5 fica dentro do passo de 1 s do instrumento, logo o
residuo verdadeiro pode ser negativo. RESIDUO_N = 85.

DOIS achados, e os dois sao de instrumento meu:

1. O `origens_sem_uso` que eu escrevi as 01:2x contava ID, nao TITULO. Neste
   canal ele devolveu SEIS origens de zero usos, e as SEIS tem o MESMO titulo —
   sao duplicatas, do grupo das 46 que aguardam a sua decisao. Por titulo
   distinto eram ZERO. Consertado, com o tamanho da inflacao contado (cinco).

   E ISTO TOCA UMA PENDENCIA SUA: enquanto as 46 duplicatas existirem, qualquer
   contagem de pauta por ID as conta como origem nova. O conserto do instrumento
   protege a escolha, mas as copias seguem no canal.

2. Um teste MEU de 12/10 reprovou, e a retratacao e dele, nao do codigo: ele
   cobrava `None` para tres origens, e uma passou a resolver CERTO — para um
   pacote de 77 capitulos — porque a copy desta rodada nomeou o pacote, que e
   exatamente a convencao que a funcao le. Eu havia travado identidade onde
   havia propriedade.

Suite de volta a 25 falhas, o conjunto da linha de base.

Inscritos 68 / 21 / 8 — os tres `indeterminado`, janela de 18,0 h (piso
1,33/dia). O limite mais apertado da frota segue sendo o 1,18/dia de 16/10.

Na sua mao, por valor: (1) os dois cliques de consentimento do Google; (2)
reconectar o conector do Supabase — 66 linhas parqueadas; (3) a decisao do
740/748; (4) as 46 duplicatas, que o achado 1 acima mostra custando na escolha
de pauta e nao so no teto de upload.

## 18/10 04:1x — a origem de maior valor do labtreinamento é de OUTRO IDIOMA

Peça da rodada: `labtreinamento-s074` = `lftQPiNJFgE`, pública, 28 s reais.

**O que esta rodada achou, e muda a pauta:** o instrumento de origem de zero
usos (escrito há três horas) escolheu pauta pela primeira vez e devolveu **uma**
origem no `labtreinamento` — e ela é um longo **POLONÊS** publicado naquele
canal pt-BR. Logo a origem de maior valor editorial do canal é inutilizável
nele. **Isso é consequência direta das 46 duplicatas**, que até agora eu só
reportava como custo de cota de upload: elas também poluem a pauta.

**Nada disso eu conserto sem você**, e são as mesmas duas decisões de sempre, na
mesma ordem:

1. **Os dois cliques de consentimento do Google** (`docs/reautorizar-analytics.md`).
   É a única rota para retenção, e retenção é a única medida que decide em tempo
   útil o que faz uma peça romper. Sem ela a pergunta "o que monetiza" não tem
   instrumento.
2. **Reconectar o conector do Supabase.** É a única rota que devolve
   `execute_sql`/`pg_net` — negado pela **quinta** rodada seguida. Sem ele: 67
   linhas de `videos` parqueadas sem entrar, nenhum registro de origem consumida,
   e o defeito dos dois shorts do kolejny que declaram origem de outro canal
   **não tem como ser corrigido** (o id certo não está em nenhum retrato local).

**Porta 1 nesta rodada:** 68 / 21 / 8 inscritos, delta **zero** nos três contra
19,1 h. Os três saem `indeterminado`. O piso desta janela é 1,26/dia e **não
aperta** o limite de 1,18/dia que já estava medido — então esta rodada não traz
leitura nova de ritmo, e isso vai dito em vez de apresentado como progresso. A
próxima leitura capaz de RESOLVER ritmo precisa de delta ≥ 2, que no limite
medido não cai antes da manhã de 19/10.

## 18/10 05:1x — a banda de resíduo cobre os dois extremos com igual conforto

Peça: `epomeno-epipedo-s057` = `04U8EeDbx_Q`, pública, 41 s reais.

**Esta rodada demonstrou, de propósito, por que a previsão de duração não
serve para prometer nada.** Eu escrevi na copy, ANTES de publicar, que o real
cairia entre 40,8 e 45,4 s e podia encostar no teto de 45 do portão. Saiu **41** —
o extremo oposto da faixa que eu mesmo anunciei. A banda tem 4,6 s de largura
contra 1 s de granularidade do instrumento: ela acomoda qualquer resultado.
**Isso não é defeito novo, é o custo das quatro ampliações da banda já
registradas.** Fica dito porque é o tipo de coisa que, não dita, viraria
"previsão confirmada".

**E o contador de concentração mudou a escolha de pauta pela primeira vez:** ele
alertou que uma origem carrega 12 dos 56 shorts do canal (21%), mais que o dobro
da segunda. Essa origem é justamente a mais recente — logo a regra "serve o longo
mais novo primeiro" e o alerta de concentração apontavam para lados opostos.
Segui o alerta, porque ele é de monetização: concentração ataca o portão
`similaridade`, que é o que estamos tentando passar.

**As duas decisões que seguem suas, na mesma ordem de sempre:**

1. **Os dois cliques de consentimento do Google** (`docs/reautorizar-analytics.md`).
   Única rota para retenção — e retenção é a única medida que responde "o que faz
   uma peça romper", que é a pergunta que decide a monetização.
2. **Reconectar o conector do Supabase.** `execute_sql` negado pela **sexta**
   rodada seguida. São **68** linhas de `videos` parqueadas sem entrar, nenhum
   registro de origem consumida, e o defeito dos dois shorts do kolejny com
   origem de outro canal continua sem como ser corrigido.

**Porta 1:** 68 / 21 / 8, delta **zero** em 20,1 h, três `indeterminado`. O piso
desta janela é 1,19/dia e **não aperta** o limite de 1,18/dia já medido — por
0,01. Nenhuma leitura nova de ritmo nesta rodada.

## 18/10 06:1x — o limite do ritmo APERTOU, e um método meu quase fabricou achado

Peça: `kolejny-poziom-s058` = `7ygrC7AbGHE`, pública, 42 s reais.

**A única notícia de medição em várias rodadas, e é pequena mas real:** a janela
de 21,1 h tem piso de resolução de **1,14 inscrito/dia**, abaixo do 1,18/dia que
vinha de 16/10. Com delta zero nos três canais, o limite superior do ritmo da
frota baixou: ela anda **abaixo de 1,14/dia**. Isso não diz que o ritmo caiu —
diz que agora sabemos um pouco mais sobre quão baixo ele é.

**E uma regra que eu escrevi há duas horas quase me fez relatar coisa falsa.** Eu
havia escrito "confira o idioma do título antes de escrever" e não disse ONDE
conferir. A listagem de uploads devolveu os quatro longos mais recentes do canal
polonês com título em inglês, o que pela minha própria regra se lê como "idioma
errado". Era o instrumento: o YouTube serve o título traduzido quando a chamada
não pede idioma. Lido na página com locale polonês, está tudo em polonês.

A conclusão de ontem (a origem livre do labtreinamento é polonesa) **continua
certa** — conferi pelo método correto —, mas o caminho que a produziu errou na
rodada seguinte. Travado com sete testes.

**As duas decisões seguem suas, inalteradas:**

1. **Os dois cliques de consentimento do Google** (`docs/reautorizar-analytics.md`).
2. **Reconectar o conector do Supabase** — `execute_sql` negado pela **sétima**
   rodada seguida; **69** linhas de `videos` parqueadas sem entrar.

Três peças publicadas nestas três rodadas, todas públicas e medidas.

## 18/10 07:1x — a lista de uploads do canal não é estável, e o ritmo apertou

Peça: `labtreinamento-s075` = `Bx5QjHPMR_Y`, pública, 29 s reais.

**Duas coisas medidas nesta rodada, e a primeira é sobre um instrumento que
decide pauta:** a lista de uploads que eu uso para saber quais longos o canal
tem devolveu **doze** peças às 07:00 e **treze** às 04:16. A que desapareceu
(`KRUERlNPzDw`) está no ar, é pública, é do canal e já rendeu quatro shorts —
nada foi publicado nem apagado entre as duas leituras. Logo essa lista **ordena,
mas não enumera**, e a contagem dela é um piso. Travei com sete testes; antes de
eu dizer "essa origem não existe mais", agora eu leio a página dela.

**A segunda é a única notícia boa de medição:** o limite do ritmo apertou pela
segunda rodada seguida. Com delta zero nos três canais em 22,1 h, o ritmo da
frota está agora medido **abaixo de 1,09 inscrito/dia** (era 1,14 na rodada
anterior, 1,18 em 16/10). Isso não diz que o ritmo caiu — diz que o teto do que
ele pode ser está mais baixo. Os três canais seguem `indeterminado`.

**As duas decisões seguem suas:**

1. **Os dois cliques de consentimento do Google** (`docs/reautorizar-analytics.md`).
2. **Reconectar o conector do Supabase** — negado pela **oitava** rodada seguida;
   **70** linhas de `videos` parqueadas sem entrar.

Quatro peças publicadas nestas quatro rodadas, todas públicas e medidas.

## 18/10 08:2x — epomeno-epipedo-s058 no ar, e um run perdido por chave ausente

* **Peça:** `lXFart_bsg0`, pública, **42 s reais**. Origem: o rank 3 da ordem viva
  do canal, não o rank 1 — o topo está em DOZE usos contra 4 do segundo, e o
  portão `similaridade` existe por causa disso.
* **O `execute_sql` segue negado — NONA rodada seguida.** As **71** linhas de
  `insert into videos` continuam parqueadas em `docs/pendente/videos-a-inserir.sql`
  e entram no minuto em que o conector voltar. **Reconectar o conector do Supabase
  é hoje a única rota que devolve duração real pelo banco, inscritos, a regra (h)
  e o registro em `videos`** — a ordem antiga da pendência 2 pressupunha um banco
  que funcionava.
* **Inscritos 68 / 21 / 8, delta ZERO nos três em 23,2 h.** O limite superior do
  ritmo da frota aperta para **abaixo de 1,03 inscrito/dia**. Porta 1
  `indeterminado` nos três canais.
* **Um run morreu de graça:** a spec saiu sem o campo `"longo": []` e o render
  estourou em `KeyError` **depois** de baixar as trilhas, com os onze portões
  verdes. Travado na suíte, não em portão novo — o disco já estava limpo, o
  buraco era latente.


## 18/10 09:1x — kolejny-poziom-s059 no ar, e a rota da duração fechou

* **Peça:** `8nCyWQxIRuc`, pública, *"Zwłoka nie dzieli się"*. É a **PRIMEIRA**
  peça tirada de uma origem que tinha **zero** shorts (`SZV9Vk5YFwI`, o grupo de
  seis cópias do mesmo título colapsado numa origem só, com 57 capítulos de spec
  local). O topo do canal está em **doze** usos.
* **Sem duração real medida nesta rodada**, e o motivo está medido, não suposto:
  o controle `OhrGlJvnBoM` (44 s conhecidos) voltou **vazio** da mesma chamada,
  logo a rota fechou — não é defeito da peça. Ela fica parqueada e a medição vem
  quando a rota abrir.
* **O `execute_sql` segue negado — DÉCIMA rodada seguida.** São **72** linhas de
  `insert into videos` parqueadas. **Reconectar o conector do Supabase é a única
  rota que devolve a leitura de duração pelo banco, inscritos, a regra (h) e o
  registro em `videos`.**
* **Inscritos 68 / 21 / 8, delta ZERO em 24,1 h.** O limite superior do ritmo da
  frota cruzou **1,00 inscrito/dia**. A consequência aritmética, e ela não é
  nova, só ficou mais larga: mesmo **no teto** desse limite o `labtreinamento`
  precisaria de 432 dias para os 500 — isto é, **dezembro de 2027**, bem depois
  de 1/FEV/2027, quando a barra sobe para 1.000. **O ritmo medido não fecha a
  Porta 1 nem no melhor caso que o instrumento ainda admite.**


## 18/10 10:1x — labtreinamento-s076 no ar; rota da duração fechada há duas rodadas

* **Peça:** `TgTa8nUcCpA`, pública, *"O teto descreve a sala dele"*. Origem rank 3
  (`Sr6VhvD_aPE`, 5 usos), família nova — a sexta distinta dessa origem.
* **Dois portões REPROVARAM antes de publicar, e isso é o sistema funcionando:**
  o `similaridade` achou 0,67 contra um short que já está no ar neste canal
  (teto 0,65), e o `variedade` contou 5 palavras na thumbnail (limite 4). Os dois
  foram corrigidos; sem o conserto de 15/10 o primeiro não teria comparado contra
  o que está no ar.
* **Sem duração real há DUAS rodadas**, com o controle sondado nas duas: a rota
  do YouTube está fechada, não é defeito das peças. Duas peças parqueadas
  esperando, e a banda do resíduo congelada em 90 pontos.
* **`execute_sql` negado pela 11ª rodada seguida** — **73** linhas de
  `insert into videos` parqueadas.
* **Inscritos 68 / 21 / 8, delta ZERO em 25,1 h.** Piso de resolução em
  **0,96/dia**: a frota anda abaixo de um inscrito por dia como limite superior.


## 18/10 11:1x — a rota reabriu, TRÊS pontos entraram, e achei um erro meu de contagem

* **Peça:** `-zbvpX7peIU`, pública, *"Ο συνάδελφος δεν μετρά"* (epomeno),
  **41 s reais**. Origem rank 4, família nova — a quarta distinta dessa origem.
* **A rota da duração REABRIU** depois de duas rodadas fechada, e o parqueamento
  pagou pela primeira vez: as duas peças que estavam esperando resolveram na
  mesma chamada (**+2,6** e **+2,3**), mais a desta rodada. Nenhum ponto se
  perdeu nas duas rodadas em que eu não conseguia medir.
* **Um erro MEU de contagem, corrigido:** a série do resíduo tinha um ponto
  **duplicado** e comentários de procedência deslocados, porque o meu `replace`
  casava o PREFIXO da linha em vez da linha inteira. `RESIDUO_N` estava errado
  por um desde as 09:0x — nenhum limite mudou, mas o número que eu reportei
  estava inflado. Agora são **93**, com teste que proíbe a repetição.
* **O piso da banda foi a −1,2** (sétima correção, todas alargando): o negativo
  saiu da janela estreita em que eu dizia que ele morava.
* **`execute_sql` negado pela 12ª rodada seguida** — **74** linhas parqueadas.
* **Inscritos 68 / 21 / 8, delta ZERO em 26,1 h.** Piso em **0,92/dia**.


## Rodada de 18/10 12:07 — kolejny-poziom-s060 = r05_ExUsXyQ

Peca publica, 43 s reais, provedor **edge** MEDIDO (zero avisos no job
117672928944). Residuo +1,3 s, estabelecido, DENTRO da banda — `RESIDUO_N`
= 94, limites intocados em (-1,2; 4,0). Som: LUFS -14,0, LRA 2,5, pico
-3,2 dBTP, desvio do alvo **0,0**, zero silencios.

Inscritos **68 / 21 / 8** contra 17/10 09:0x (27,1 h): delta ZERO nos tres.
Porta 1 `indeterminado` nos tres canais, e o limite superior do ritmo da
frota aperta de 0,92 para **0,89 inscrito/dia**. Isto nao e "o canal nao
cresce": e o teto do que a janela consegue resolver. Para RESOLVER ritmo e
preciso |delta| >= 2 (criterio do 723), o que no limite medido nao cai
antes de 19/10.

**O que o dono precisa decidir, e nada disto eu consigo sozinho:**
1. os dois cliques de consentimento do Google (`docs/reautorizar-analytics.md`)
   — segue o de maior valor, e o unico caminho a retencao;
2. reconectar o conector do Supabase — `execute_sql` negado pela **13a**
   rodada seguida. Sao **75** linhas de `insert into videos` parqueadas em
   `docs/pendente/videos-a-inserir.sql` esperando por ele, e sem ele o id
   de origem errado dos `kolejny-poziom-s004`/`-s035` continua sem conserto;
3. a decisao do 740/748 (mira contra real) — doze de quinze pecas do
   labtreinamento fora do teto da mira no mundo edge, todas com o portao
   verde;
4. as **46 duplicatas**: nesta rodada elas voltaram a poluir a escolha de
   pauta. O instrumento de origem sem uso devolveu UMA origem, e ela e copia
   do titulo que a rodada anterior acabou de consumir — por TITULO DISTINTO,
   zero origem nova no canal.

Suite: **25 falham / 2.812 passam / 892 skip** — o conjunto da linha de base,
nenhuma falha nova.

## Rodada de 18/10 13:07 — labtreinamento-s077 = DgvGXwefhxQ

Peca publica, 28 s reais, provedor **edge** MEDIDO (zero avisos no job
117684273256). Residuo +2,3 s, estabelecido, DENTRO da banda — `RESIDUO_N`
= 95, limites intocados. Som: LUFS -14,0, LRA 3,2, pico -1,8 dBTP, desvio
0,0, zero silencios.

Inscritos **68 / 21 / 8** contra 17/10 09:0x (28,1 h): delta ZERO. Porta 1
`indeterminado` nos tres, e o teto do ritmo aperta a **0,85 inscrito/dia**.

**E a rodada recusou uma resposta do proprio instrumento, com motivo medido.**
O `origens_sem_uso` do labtreinamento devolveu UMA origem de zero usos, e ela
e a **POLONESA** (`QiaGg03WSR0`, `language: pl`). O instrumento esta VERDE e
seguir a resposta dele produziria peca em idioma errado — o modo de falha mais
caro que existe aqui. Ele esta certo em nomea-la; ela e que nao serve ao canal
pt-BR. Conferido ANTES de escrever.

**E o tally da pinca do 740/748 foi a TREZE de dezesseis:** o real de 28 s
ficou fora do teto da mira deste canal (26,0) com o `mira.py` **VERDE nos dois
mundos**, exatamente como a copy declarou antes de publicar. Para o real caber
na mira o edge precisaria de <= 22,0, onde o piper cai a ~18,0 — abaixo do piso
de 20,0. **Nao existe spec deste canal que satisfaca as duas**, e a saida e sua:
mover a mira para o ESTIMADO descontando o residuo, ou parar de cobrar uma
faixa de REAL sobre o estimado.

Parque: 35 pecas, zero sem leitura. `execute_sql` negado pela **14a** rodada —
**76** linhas de insert parqueadas. Suite: 25 / 2.812 / 895, conjunto IDENTICO
a linha de base.

## Rodada de 18/10 14:07 — epomeno-epipedo-s060 = pSdQQa5beIw

Peca publica, 42 s reais, provedor **edge** MEDIDO (zero avisos no job
117697224890). Residuo +0,5, **sinal NAO estabelecido** (real 42 significa
duracao em (41; 42], e a previsao de 41,5 cai dentro) — `RESIDUO_N` = 96,
limites intocados. Som: LUFS -14,1, LRA 2,2, pico -3,2 dBTP, desvio -0,1,
zero silencios.

Inscritos **68 / 21 / 8** contra 17/10 09:0x (29,1 h): delta ZERO. Porta 1
`indeterminado` nos tres, teto do ritmo a **0,82 inscrito/dia**.

**Duas coisas desta rodada que valem para voce saber como a maquina esta
decidindo:**
1. o atalho que resolve a origem (`segundo_angulo.pacote_do_id`) devolveu
   **None** — a convencao de nome nao foi seguida naquele pacote. Em vez de
   trocar de origem, o pacote foi achado por BUSCA DE CONTEUDO. Falta de
   spec local nunca foi motivo para pular origem, e hoje isso foi aplicado;
2. o `origens_sem_uso` devolveu lista **VAZIA** neste canal — todas as 18
   origens da ordem viva ja renderam short. **Lista vazia nao prova ausencia
   de origem livre**, porque a playlist OMITE longo: ela ordena e nao enumera,
   logo 18 e um PISO. Isso e refil de pauta travado, e o que o destrava e a
   pendencia da rede (as quatro fontes institucionais) mais o banco.

`execute_sql` negado pela **15a** rodada seguida — **77** linhas de insert
parqueadas. Suite: 25 / 2.812 / 898, conjunto IDENTICO a linha de base.

## Rodada de 18/10 15:07 — kolejny-poziom-s061 = 7p8S5XIQA0M

Peca publica, 43 s reais, provedor **edge** MEDIDO (zero avisos no job
117710246704). Som: LUFS -14,0, LRA 2,7, pico -3,6 dBTP, desvio 0,0, zero
silencios.

Inscritos **68 / 21 / 8** contra 17/10 09:0x (30,1 h): delta ZERO. Porta 1
`indeterminado` nos tres, teto do ritmo a **0,80 inscrito/dia**.

**E esta peca achou um defeito no MEU proprio criterio de medicao.** Ela previa
42,0 e saiu com 43: residuo +1,0, e o instrumento disse "sinal nao
estabelecido". **A aritmetica diz que esta:** real 43 significa duracao
verdadeira em (42; 43], logo o residuo vive em (0; 1] — intervalo ABERTO
embaixo, cada valor dele positivo. Eu havia escrito o criterio como
`real - previsao > 1,0` quando a condicao certa e `>= 1,0`.

**Dois pontos da serie moram nessa borda**, e um deles estava classificado
errado desde 14/10 — logo a contagem de pontos estabelecidos que eu reportei
nesses quatro dias estava baixa por um. Consertado, com seis testes novos, e um
teste MEU de ontem foi retratado no lugar onde eu havia afirmado o contrario.
`RESIDUO_N` = 97; a banda nao mudou.

Isto e o tipo de coisa que a rodada faz quando nao pode medir mais nada: o
`execute_sql` segue negado pela **16a** rodada seguida, e sao **78** linhas de
insert parqueadas esperando por ele.

Suite: 25 / 2.818 / 901, conjunto IDENTICO a linha de base.

## Rodada de 18/10 16:07 — labtreinamento-s078 = wlwaHALIq7M

Peca publica, 28 s reais, provedor **edge** MEDIDO (zero avisos no job
117723657331). Residuo +2,2, estabelecido, dentro da banda — `RESIDUO_N` = 98.
Som: LUFS -14,2, LRA 2,9, pico -1,7 dBTP, desvio -0,2, zero silencios.

Inscritos **68 / 21 / 8** contra 17/10 09:0x (31,1 h): delta ZERO. Porta 1
`indeterminado` nos tres, teto do ritmo a **0,77 inscrito/dia**.

**O tally da pinca do 740/748 foi a CATORZE de dezessete:** o real de 28 s ficou
fora do teto da mira deste canal (26,0) com o `mira.py` VERDE nos dois mundos,
como a copy declarou antes de publicar. Para o real caber na mira o edge
precisaria de <= 22,0, onde o piper cai a ~18,0 — abaixo do piso de 20,0.
**Catorze medicoes dizem a mesma coisa, e a saida e sua:** mover a mira para o
ESTIMADO descontando o residuo, ou parar de cobrar uma faixa de REAL sobre o
estimado.

**E a origem de ZERO usos deste canal foi recusada pela SEGUNDA rodada seguida**,
com o mesmo motivo medido: ela e a POLONESA (`QiaGg03WSR0`, `language: pl`). O
instrumento a nomeia certo; seguir a resposta dele produziria peca de idioma
errado. Isso significa que a regra do idioma tem de ser aplicada a cada rodada —
e que **enquanto as 46 duplicatas e essa origem cruzada nao forem resolvidas, a
escolha de pauta carrega um passo manual que nao da para automatizar.**

`execute_sql` negado pela **17a** rodada seguida — **79** linhas de insert
parqueadas. Suite: 25 / 2.818 / 904, conjunto IDENTICO a linha de base.

## Rodada de 18/10 17:06 — epomeno-epipedo-s061 = 7mm9Frw_tbE

Peca publica, 41 s reais, provedor **edge** MEDIDO (zero avisos no job
117736668345). Residuo **-0,5**, estabelecido pelo ramo negativo, dentro da
banda — `RESIDUO_N` = 99. Som: LUFS -14,0, LRA 2,0, pico -3,3 dBTP, desvio 0,0,
zero silencios.

Inscritos **68 / 21 / 8** contra 17/10 09:0x (32,1 h): delta ZERO. Porta 1
`indeterminado` nos tres, teto do ritmo a **0,75 inscrito/dia**.

**E o achado desta rodada e sobre a nossa propria medicao, nao sobre a peca.**
Este e o QUINTO residuo negativo da serie, e varridos todos os cinco eles tem
**real EXATAMENTE 41** — com previsoes que variam de 41,4 a 42,2. Logo o
negativo nao e "a previsao erra para cima neste canal": e o inteiro 41
aparecendo, e 41 e o **PISO** do espalhamento daquela janela, onde o mesmo canal
ja deu 42, 43, 44 e 46. Isto retrata, pela terceira vez, a forma como eu
descrevia o fenomeno — as duas anteriores olhavam a PREVISAO, e a regularidade
esta no REAL.

**E TRES testes meus reprovaram com isso, pelo motivo certo:** eles cobravam
"o negativo e raro" com `<= 5% da serie`, e **o 5% era numero escolhido por
mim** quando havia UM negativo em 78 pontos. Com 5 de 99 ele reprovou.
**Afrouxar para 10% seria mover o numero para o teste passar** — exatamente o
defeito que este projeto ja nomeou tres vezes. Os tres passaram a cobrar a
propriedade MEDIDA: na janela de previsao onde o negativo ocorre, ele e minoria
contra os nao-negativos (5 contra 26). Sete testes novos guardam o achado.

`execute_sql` negado pela **18a** rodada seguida — **80** linhas de insert
parqueadas. Suite: 25 / 2.825 / 907, conjunto IDENTICO a linha de base.

## 18/10 18:2x — s062 do kolejny no ar; `execute_sql` negado pela 19a rodada

Peca: `kolejny-poziom-s062` = `44pLux0239U`, publica, **42 s reais** (previsao
edge 41,5; provedor **edge** medido, zero avisos no job `117751024537`).
Residuo **+0,5**, dentro da banda `(-1,2; 4,0)`; o sinal dele **nao** esta
estabelecido, porque `42 - 41,5` nao alcanca 1,0. `RESIDUO_N` = 100.

Inscritos **68 / 21 / 8**, delta ZERO nos tres contra a leitura de 17/10 09:0x
(33,2 h). O piso de resolucao dessa janela e **0,72 inscrito/dia** — era 0,75 na
rodada anterior —, logo o que esta medido e "a frota anda abaixo de 0,72/dia", e
nao "o ritmo e zero". Porta 1 `indeterminado` nos tres pela 7a rodada seguida.

**A unica noticia de medicao continua sendo esse limite apertando**, e ele
aperta por o tempo passar sem o contador andar, nao por leitura nova. Para
RESOLVER ritmo e preciso `|delta| >= 2`, o que no limite medido nao cai antes
de 19/10.

**O que segue na sua mao, por valor:** (1) os dois cliques de consentimento do
Google (`docs/reautorizar-analytics.md`) — e a unica rota para retencao, e sem
ela os experimentos 37/38/40 ficam indecidiveis; (2) reconectar o conector do
Supabase — e a unica que devolve `execute_sql`/`pg_net`, e sao **81** linhas de
`insert into videos` parqueadas esperando por ela; (3) a decisao do 740/748, com
o tally em **quatorze de dezessete** no labtreinamento.

## 18/10 19:2x — s079 no ar; e o CONTADOR DO KOLEJNY MEXEU: 8 -> 9

Peca: `labtreinamento-s079` = `skQt0Js1t-k`, publica, **27 s reais** (previsao
edge 25,8; provedor **edge** medido, zero avisos no job `117763741472`).
Residuo **+1,2**, ESTABELECIDO e dentro da banda. `RESIDUO_N` = 101.

**Inscritos 68 / 21 / 9 — o kolejny subiu UM, o primeiro movimento de contador
em sete rodadas.** Contra a leitura de 17/10 09:0x, 34,1 h. **E isso NAO e
ritmo medido:** o piso de resolucao dessa janela e 0,70/dia e o delta vale
exatamente 0,70/dia, logo e UMA contagem — a incerteza e da ordem do proprio
valor, e o criterio de duas contagens recusa. O canal sai `indeterminado`.

**O que muda de verdade e o que eu posso DIZER:** por sete rodadas eu escrevi
"delta zero nos tres, logo a frota anda abaixo de X/dia". Essa frase **cai para
o kolejny** — ele nao esta mais abaixo do piso, esta EM CIMA dele. Nos outros
dois ela segue valendo (abaixo de 0,70/dia). Para RESOLVER o kolejny agora basta
um segundo passo: se ele for a 10, o ritmo fica medido.

Tally do 740/748 em **quinze de dezoito**: o real 27 ficou acima do teto da mira
(26,0) com o `mira.py` VERDE nos dois mundos, e a exposicao estava declarada na
copy antes de publicar.

**O que segue na sua mao:** (1) os dois cliques de consentimento do Google; (2)
reconectar o conector do Supabase — **82** linhas de `insert into videos`
parqueadas, e o `execute_sql` esta negado pela 20a rodada seguida; (3) a decisao
do 740/748, agora com quinze de dezoito medidos.

## 18/10 20:2x — s062 do epomeno no ar; o +1 do kolejny SE REPRODUZIU

Peca: `epomeno-epipedo-s062` = `-MEIzb-MSh4`, publica, **43 s reais** (previsao
edge 42,1; provedor **edge** medido, zero avisos no job `117777340562`).
Residuo **+0,9**, dentro da banda, sinal NAO estabelecido (43 - 42,1 < 1,0).
`RESIDUO_N` = 102.

**Inscritos 68 / 21 / 9 — o 9 do kolejny voltou numa SEGUNDA leitura, uma hora
depois da primeira.** Isso descarta artefato de replica: o passo e real. **E
continua sendo UMA contagem contra a referencia de 17/10 09:0x (35,1 h), cujo
piso de resolucao e 0,68/dia** — o delta vale exatamente isso, logo a incerteza
e da ordem do proprio valor e o canal sai `indeterminado`. Para RESOLVER falta
um segundo passo: se ele for a 10, o ritmo fica medido.

Os outros dois seguem com delta zero, logo abaixo de 0,68/dia.

**O que segue na sua mao:** (1) os dois cliques de consentimento do Google; (2)
reconectar o conector do Supabase — **83** linhas de `insert into videos`
parqueadas e o `execute_sql` negado pela 21a rodada seguida; (3) a decisao do
740/748, com quinze de dezoito medidos no labtreinamento.

## 18/10 21:2x — s063 do kolejny no ar; o 9 confirmado na TERCEIRA leitura

Peca: `kolejny-poziom-s063` = `Z3vtiXCZlaU`, publica, **43 s reais** (previsao
edge 41,5 — o PISO exato; provedor **edge** medido, zero avisos no job
`117790725744`). Residuo **+1,5**, ESTABELECIDO e dentro da banda.
`RESIDUO_N` = 103.

Inscritos **68 / 21 / 9**. O 9 do kolejny saiu na TERCEIRA leitura seguida, logo
o passo nao e artefato de replica. Contra a referencia de 17/10 09:0x sao 36,1 h
e o piso de resolucao e **0,66/dia** — o delta de UMA unidade vale exatamente
isso, e o criterio de duas contagens recusa. Os tres seguem `indeterminado`.

**A unica coisa que mudou de verdade hoje nesse quadro:** o kolejny deixou de
estar ABAIXO do piso e passou a estar EM CIMA dele, e isso valeu para as tres
rodadas seguintes. Nos outros dois a frase antiga continua: abaixo de 0,66/dia.

Entregues HOJE nesta sessao: quatro pecas, uma por canal por rodada —
`kolejny-poziom-s062`, `labtreinamento-s079`, `epomeno-epipedo-s062` e
`kolejny-poziom-s063`. Todas `processed` e publicas, nenhuma fora de
`processed`, nenhum `P0D`.

**O que segue na sua mao:** (1) os dois cliques de consentimento do Google — sem
retencao os experimentos 37/38/40 ficam indecidiveis; (2) reconectar o conector
do Supabase: **84** linhas de `insert into videos` parqueadas, `execute_sql`
negado pela 22a rodada seguida; (3) a decisao do 740/748, com quinze de dezoito
medidos no labtreinamento.

## 18/10 22:2x — s080 no ar; e a ORIGEM foi trocada pela regra (f)

Peca: `labtreinamento-s080` = `16TcSYGClCs`, publica, **27 s reais** (previsao
edge 25,6; provedor **edge** medido, zero avisos no job `117804130785`).
Residuo **+1,4**, ESTABELECIDO e dentro da banda. `RESIDUO_N` = 104.

Inscritos **68 / 21 / 9** — quarta leitura seguida com o 9 do kolejny. Contra
17/10 09:0x sao 37,1 h, piso **0,65/dia**, delta de UMA unidade: os tres saem
`indeterminado`.

**O que esta rodada mostra sobre a PAUTA, e e o achado dela:** eu escolhi a
origem pelo contador (rank 5, menor patamar de uso, melhor rank dentro dele) e
tive de TROCAR, porque a unica familia nao usada daquela origem era de UNIDADE —
e uma peca de unidade (`s074`) ja saiu neste canal hoje. A escolha pelo contador
nao e suficiente: ela ordena por USO, e a regra (f) cobra por FAMILIA. Nesta
rodada as duas discordaram, e a regra (f) ganhou.

**A consequencia pratica para o dono:** com cinco a seis shorts por origem, as
familias nao usadas comecam a se repetir ENTRE origens do mesmo canal. Isso
aperta a pauta por um caminho novo — nao por falta de origem, mas por falta de
familia distinta no mesmo dia. E o reforco mais forte do pedido de LONGO NOVO,
que hoje esta bloqueado pelo 402.

Tally do 740/748 em **dezesseis de dezenove** no labtreinamento.

**O que segue na sua mao:** (1) os dois cliques do Google; (2) reconectar o
conector do Supabase — **85** linhas parqueadas, `execute_sql` negado pela 23a
rodada; (3) a decisao do 740/748.

## 18/10 23:2x — s063 do epomeno no ar; seis pecas nesta sessao hoje

Peca: `epomeno-epipedo-s063` = `JxnrtPMbHA4`, publica, **43 s reais** (DOIS
`lengthSeconds` na pagina, 42 e 43, usado o MAIOR; previsao edge 42,2; provedor
**edge** medido, zero avisos no job `117816895844`). Residuo **+0,8**, dentro da
banda, sinal NAO estabelecido. `RESIDUO_N` = 105.

Inscritos **68 / 21 / 9** — quinta leitura seguida com o 9. Contra 17/10 09:0x
sao 38,1 h, piso **0,63/dia**, delta de UMA unidade: os tres `indeterminado`.

Entregues nesta sessao hoje: **SEIS pecas**, uma por canal por rodada —
`kolejny-poziom-s062`, `labtreinamento-s079`, `epomeno-epipedo-s062`,
`kolejny-poziom-s063`, `labtreinamento-s080` e `epomeno-epipedo-s063`. Todas
`processed` e publicas, nenhuma fora de `processed`, nenhum `P0D`. Sao DUAS por
canal — o pedido de 16/10 ("pelo menos 2 por dia por canal") esta cumprido no
short; o LONGO de cada canal segue bloqueado pelo 402, porque longo exige numero
novo sobre o mundo e as fontes institucionais estao fechadas no proxy.

**Uma coisa que esta rodada cortou e que a regra (g) nao pegava:** a narracao
tinha "ha dois anos" e "duas vezes". Nenhuma das duas e taxa, indice nem data,
logo passavam pela regra — mas as duas AFIRMAM uma quantidade sobre o mundo que
eu nao medi. Sairam. Vale como regra: a regra (g) cobre numero que MUDA; o que
nao muda e tambem nao foi medido continua sendo invencao.

**O que segue na sua mao:** (1) os dois cliques do Google; (2) reconectar o
conector do Supabase — **86** linhas parqueadas, `execute_sql` negado pela 24a
rodada seguida; (3) a decisao do 740/748.

## 19/10 00:2x — MEDIDO: a cota é ~6/dia na FROTA, não por canal

**Os três canais compartilham UM projeto do Google Cloud: `777159180424`.**
Medido pela sonda no runner (job `117829119323`), lendo o número do projeto do
`client_id` — número que não é segredo. Logo o teto de `10.000/1.600` = **6
envios de vídeo por dia vale para a frota inteira.**

**E a consequência era imediata.** A cota zera à meia-noite do **Pacífico**, logo
a janela corre de **07:00 UTC a 07:00 UTC**. As seis peças de ontem (18:16 a
23:13 UTC) estão TODAS na janela que só fecha às 07:00 de hoje: **9.600 de
10.000 usadas, sobram 400, e um envio custa 1.600.**

**Por isso esta rodada NÃO publicou** — a sétima peça da janela levaria
`403 quota`. Não é escolha, é aritmética. E ontem a frota fechou o dia a **96%
da cota sem ninguém saber**: uma peça a mais em qualquer rodada teria falhado.

**O que isto significa para os seus 7/dia/canal:** são 21 envios = 33.600
unidades = **3,4x a cota**. O ritmo ATUAL (2/dia/canal) já bate no teto.

**As duas saídas, e a ordem mudou com a medição:**
1. **Separar em TRÊS projetos do Cloud** — multiplica o teto por três (6 → 18/dia)
   e **não depende de aprovação de ninguém**. Custa você criar dois projetos no
   console e colar um `YT_OAUTH_JSON` novo. **Esta passou na frente.**
2. **Extensão de cota** pelo formulário de auditoria do YouTube — levanta o teto
   dentro de um projeto, é grátis, e a resposta leva dias ou semanas.

**E uma regra operacional nova:** a janela de cota vira às 07:00 UTC, então
rodada entre 00:00 e 07:00 depois de um dia cheio é de engenharia por aritmética.
A produção volta às 07:0x.

Inscritos **68 / 21 / 9**, sexta leitura seguida com o 9; os três `indeterminado`.
`execute_sql` negado pela 25ª rodada; **86** linhas de `insert into videos`
parqueadas.
