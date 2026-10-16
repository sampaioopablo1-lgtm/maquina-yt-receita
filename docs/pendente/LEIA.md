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
