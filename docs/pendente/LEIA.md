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
