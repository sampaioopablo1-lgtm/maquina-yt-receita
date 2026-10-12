# Máquina de vídeos — o que nunca deve envelhecer

A rotina horária carrega o procedimento. Este arquivo carrega só os **ponteiros**,
porque número dentro de prompt envelhece e já me fez errar quatro vezes
(652/655, 658, 682, 685). Aqui não entra contagem de estoque, nem de views, nem
de inscritos. Entra onde olhar.

## O dinamismo visual — o que mudou em 09/10 e a regra nova

O dono disse que os frames pareciam estáticos. **Medido, e ele estava certo com
folga** (aprendizado 690): no `labtreinamento-s011`, diferença **mediana** entre
quadros consecutivos de **0,39** numa escala de 0–255, e **375 de 414 quadros
(91%) abaixo de 1,0**. A média de 4,34 vinha inteira dos cinco cortes de cena.

Três causas, e a física diz onde está a alavanca:

    movimento por quadro = amplitude / (duração da cena x fps)

12% de zoom em 8,3 s dá **0,048% por quadro**. Aumentar a amplitude não
conserta — corta a borda do texto antes de ficar perceptível. **A alavanca é a
duração da cena.**

**Consertado, e é defeito e não experimento:**
- `fabrica/legenda.py` — a legenda queimada do short era UMA fala para a cena
  inteira: ~18 palavras paradas por oito segundos, na região que o olho lê.
  Agora são grupos de até **quatro** palavras, com tempo proporcional aos
  caracteres.
- `motion.filtro_bordas(dur, primeira=True)` — a cena ZERO perdeu o fade de
  entrada. Havia preto de t=0 a t=0,067, dentro do primeiro segundo, que é o que
  decide a distribuição. As emendas entre cenas continuam.

**Regra nova para spec de short solto: DEZ a ONZE cenas, mantendo a duração
total** (experimento 40). Não mexer em `ALVO_SHORT` — isso é o experimento 38, e
ele ainda não tem leitura de 12 h. O esqueleto novo quebra o `39 de 39` idêntico
de propósito: ritmo e esqueleto são a mesma mudança de forma, e com a forma nova
o aviso do portão `variedade` para de aparecer.

**CORREÇÃO, e é de uma regra que eu escrevi nesta mesma manhã:** eu havia posto
"dez a CATORZE" sem conferir a sobrecarga. Doze cenas estourariam o teto de 43,1
só em silêncio, então o teto real no alvo atual é **onze**.

**SEGUNDA CORREÇÃO, de 11/10, e é do número que eu pus aqui:** eu escrevi
"~1,9 s fixos por cena" e usei isso como se fosse da frota. **Não é fixo e não é
da frota** — a sobrecarga é `P + 0,300`, e **P é por VOZ e por FRASE**: 1,04 s no
pt-BR, 1,57 s no grego, 1,72 s no polonês. Os 1,9 s eram a voz polonesa, a de
maior P, generalizada para todos — o mesmo erro do 679 e do 698. O ponto de
equilíbrio também não é um número só: use **`chars_por_cena(voz, n, total)`** de
`fabrica/ensaio.py`, que faz a conta com os `n-1` intervalos. Ver a seção
"A sobrecarga por cena é POR VOZ" no fim deste arquivo.
O `kolejny-poziom-s015` saiu com 10 cenas, 41,8 est, **4,18 s por plano** contra
8,3 e **20 falas de legenda** contra 5.

## A correção do dinamismo FUNCIONOU — medida, e no mesmo método

**Aprendizado 699.** Com `fps=10, tblend=all_mode=difference, signalstats`, que é
o método do 690 e uma escala absoluta de 0–255:

| peça | mediana | congelados (<1,0) |
|---|---|---|
| `labtreinamento-s011` — 5 cenas, legenda de uma fala | **0,39** | **91%** (375/414) |
| `kolejny-poziom-s017` — 10 cenas, legenda em pedaços | **0,63** | **73%** (302/416) |

Mediana **+62%** e congelados de 91% para 73%. Confundidor declarado: canais e
vozes diferentes, n=1 contra n=1, e as duas mudanças vêm juntas. **Vale mesmo
com n=1** porque a escala é absoluta e o efeito é no quadro, não em contagem de
view com CV 0,66.

**Não use `mpdecimate` sem fixar `hi/lo/frac`:** na mesma peça ele devolveu
"1.254 de 1.255 quadros distintos", que não é comparável com o "8 de 273" que eu
medi na manhã. Os números de `blackdetect` e `signalstats` são absolutos; esse
não.

## "Matar os fades" DESCEU na fila — medido

**Aprendizado 700, e retrata uma estimativa minha.** Eu escrevi aqui "~9 emendas
escuras, ~2,2 s de escurecimento". Medido na peça de dez cenas (1.255 quadros,
30 fps):

- **nove** quadros de preto puro, um por emenda: **0,30 s** (0,72% da peça);
- abaixo de 75% da mediana (204): 45 quadros = **1,50 s** (3,6%);
- emendas em 4,77 / 8,83 / 13,27 / 17,30 / 21,23 / 25,20 / 28,87 / 32,40 / 36,57 s.

**A primeira emenda cai em 4,77 s — FORA dos três segundos que decidem**, porque
o preto de t=0 da cena zero já foi consertado. Então o item mexe em 3,6% dos
quadros, todos depois do ponto de decisão, e deixa de ser o próximo da fila. Na
frente dele ficam **pauta** (longo novo) e o que acontece DENTRO dos três
primeiros segundos.

**Experimento 33 (motion) foi ABORTADO** em 09/10. A própria hipótese dele
declarava "não mede o que quer medir", e ele travou três testes por dez dias
enquanto o defeito que deveria medir ficava no ar. Pode ser reaberto com
retenção de verdade quando o escopo voltar.

**O que o `chart=mostPopular` disse** (categoria 26, e isso é PROXY — 610), lido
em 09/10: o que tem milhões de views dura **10 a 35 s** — mediana 26 s no BR,
35 no PL, 30 no GR. Os nossos estão em 41–42 s porque eu os empurrei para lá.
Isso é dado contra o experimento 38, não a favor; não resolver antes da leitura
de 12 h.

**Busca na web para tendência continua inútil**, como a rotina avisa: voltou
blog de fornecedor de ferramenta de legenda, sem teste controlado e com números
que se contradizem. O único item aproveitável foi um limite de forma — quatro a
cinco palavras na tela por vez — e ele entrou porque é coerente com a medição,
não porque a fonte é boa.

## Autorização permanente do dono (09/10/2026)

Palavras dele: *"Deixe 100% automático, sem precisar de aprovação. Usando toda
cota possível nos 3 canais."* Vale como autorização durável para a produção:
**não pare para pedir aprovação de pauta, render, publicação ou pacote
completo.** O "pacote completo exige janela dedicada do dono" CAIU — era
aprovação, e ela foi dada.

**O que a autorização NÃO cobre, porque é irreversível e ele não falou disso:**
apagar vídeo publicado e apagar as 46 duplicatas. A trava continua.

**E o que ela não pode destravar, porque não é aprovação:** os três secrets
`YT_TOKEN_<CANAL>` no GitHub (o proxy desta sessão bloqueia a API de secrets) e
o clique no link de consentimento do Google. Ver
`docs/reautorizar-analytics.md`.

## A restrição real é PAUTA, não cota nem aprovação

Medido em 09/10: **10 origens livres** (epomeno 4, kolejny 4, labtreinamento 2),
contra ~14 peças publicadas no dia. **Menos de um dia de pauta.** Cota não é o
limite; origem é. E origem só nasce de LONGO novo.

Isso converge com o 689: o longo converte ~5x melhor por view **e** gera pauta
**e** satisfaz os 3 uploads públicos/90 dias da Porta 1. Logo **pacote completo
deixa de ser exceção e passa a ser a produção principal** quando a pauta estiver
baixa.

## Por que NÃO aumentar o número de canais

O dono deu liberdade para isso. A aritmética diz não: **os 500 inscritos são um
limite POR CANAL.** Dividir ~2.100 views/dia em mais canais afasta cada um do
limite em vez de aproximar — concentração vence dispersão quando o portão é por
canal. Ele mesmo cortou de 13 para 3 em 07/10, e a conversão medida (1,0 a 1,3
por mil) exige acumular view no MESMO canal. Reabrir canal só faz sentido depois
de UM canal passar a Porta 1.

## O escopo de analytics NÃO foi negado — nós o perdemos

**Corrige onze afirmações minhas** (aprendizado 689, `crítico`). O banco tem
**388 linhas de retenção real** vinda da YouTube Analytics API
(`averageViewPercentage`, `subscribersGained`), em **doze canais**, incluindo os
três da frota — e todas param em **20/09/2026**. O escopo funcionou e foi
perdido: `ESCOPOS` em `fabrica/tokens.py` lista só `youtube`,
`youtube.force-ssl` e `youtube.upload`, e o `tokeninfo` do token atual confirma
esses três e nenhum outro. Como os refresh tokens morriam de sete em sete dias
(303), cada reautorização reemitiu o token pela nossa lista, sem analytics.

**Antes de chamar uma capacidade de "não autorizada", procure no banco se ela já
produziu dado, e confira a lista de escopos do próprio código.**

O que esses dados já dizem, com atribuição POR VÍDEO:

| | retenção média | inscritos | views | por mil |
|---|---|---|---|---|
| shorts | **45,1%** (n=72) | 23 | 18.693 | **1,23** |
| longos | **20,9%** (n=103) | 17 | 2.733 | **6,22** |

O longo converte ~5x melhor **por view** — o que contradiz "o longo deixou de
ser alavanca". Amostra pequena e janela de uma coleta só: trate como o melhor
dado disponível, não como conclusão.

## A variância entre peças decide o que é mensurável — e condena views/peça

**Aprendizado 693, `crítico`.** Dispersão medida DENTRO do mesmo tratamento e
canal, só peças com ≥12 h e `processed`:

| grupo | pisos | fator | CV |
|---|---|---|---|
| epomeno antigo | 218–445 | 2,0 | 0,48 |
| kolejny antigo | 96–462 | **4,8** | 0,69 |
| labtreinamento antigo | 41–162 | 4,0 | 0,79 |

**CV médio 0,66.** Com 80% de poder e α 0,05, `n = 2(1,96+0,84)²CV²/d²`:

| detectar | n por braço |
|---|---|
| 25% | **109** |
| 50% | 28 |
| 100% | 7 |

**Views por peça é cego para qualquer efeito menor que o dobro.** Antes de dizer
que um tratamento funcionou, calcule o n necessário a partir do CV do próprio
grupo. Com CV 0,66, **uma peça lendo o dobro da mediana é normal, não sinal** —
e isso retira a confiança de várias leituras que eu dei como fortes hoje.

O caminho para decidir em tempo útil é **retenção**, medida por view e com
variância muito menor que contagem de view. É o quarto argumento independente
para o escopo de analytics.

## Antes de ler qualquer contador

**Três leituras na mesma rodada, e o estimador é o MÁXIMO declarado como PISO,
com a faixa ao lado — NÃO a mediana.** Medido em 09/10/2026 (aprendizado 688,
`crítico`): das 17 peças que mudaram entre três leituras de 3 s, **todas as 17
subiram na terceira e nenhuma na segunda**. View não sobe simultaneamente em 17
vídeos de três canais em três segundos — as leituras 1 e 2 caem numa réplica e a
3 numa mais fresca, e a mediana virou o mínimo em 17 de 17. Um contador de view
só **atrasa**, nunca adianta.

**Inscrito e view DE CANAL não se leem de hora em hora** (686): o
`channels.list` devolveu statistics byte a byte idênticas em duas leituras
separadas por uma hora, nos três canais, enquanto peças individuais subiam.
Compare só leituras separadas por ≥ ~4 h, e nunca conte N leituras horárias
iguais como N observações.

## Antes de escolher pauta
- `consultas/estoque.sql` — **rode a consulta.** É a única fonte de origem livre.
  Nenhuma lista de memória, à mão, ou escrita num prompt decide nada.
- `docs/estoque.md` — por que a lista à mão foi abolida, o aviso de PERFIL e as
  faixas de identidade por canal.
- **E quando o banco está em 402, a consulta NÃO roda** — escrever aqui só o
  caminho dela deixava a rodada sem pauta nenhuma. A reconstrução local está em
  `docs/rotina-ponta-a-ponta.md` (Passo 1b): o retrato
  `fabrica/ponte/videos.json` mais o `longo_existente` das specs. Ela **não** é
  a consulta: exclui duplicata por título repetido mais o documento, e não pela
  mesma construção — foi exatamente aí que nasceu o erro 658. Use-a com as três
  ressalvas escritas lá, e **confira a origem escolhida contra as specs antes de
  escrever**, uma a uma.

## Antes de dizer que a máquina está sã
- `python3 -m pytest tests -q --ignore=tests/test_mcp.py --ignore=tests/test_banco_de_pautas.py`
  Linha de base medida em **11/10/2026: 25 falham, 2.084 passam, 454 skip**
  (os passam/skip sobem com teste novo; o que importa é o CONJUNTO de falhas).
  **Falha nova é a sua — e meça a sua própria linha de base ANTES de mexer**,
  guardando a lista de `FAILED` para comparar depois. O número escrito aqui
  envelhece; o conjunto, não.
  **A composição das 25 NÃO é "título duplicado e Devanagari"** — eu escrevi
  isso e estava errado. São **15** specs que sairiam da matriz CALADAS (números
  demais numa frase, capítulo sem margem) mais oito espalhadas. Ver a seção
  "As 25 falhas da suíte NÃO são o que eu escrevi aqui" no fim deste arquivo.
- `python3 fabrica/prontidao.py fabrica/specs/<spec>.json` — **passe o caminho
  do .json**, não o nome do pacote. São **doze** portões, **onze** no short
  solto (`capitulos` sai de fora em vez de aprovar em silêncio).

## Os portões que decidem monetização, não estética
- `fabrica/variedade.py` — conteúdo **inautêntico** (elegibilidade do YPP, não
  remoção; renomeação de 15/07/2025). Reprova gancho acima de 12 palavras e
  thumbnail acima de 4; **avisa** quando o esqueleto do short repete.
  Leia `docs/mapa-canal-dark-o-que-entrou.md` antes de mexer nos limiares —
  eles são do mapa do dono, não meus, e o aviso só avisa por causa da trava do
  experimento 33.
- `fabrica/ensaio.py` → `ALVO_SHORT` — **onde** mirar dentro da faixa depende da
  VOZ: piso no polonês (resíduo positivo), topo no grego e no pt-BR.
- `fabrica/ensaio.py` → `ALVO_POR_CANAL` — **a mira é POR CANAL quando o canal
  mediu que a mira da frota o prejudica.** O `labtreinamento` tem override
  **(33,0 a 37,0)** desde 09/10: o gatilho do 682 disparou com **idade casada**
  (views lidas na janela de 9 a 21 h de vida), e as duas peças de mira nova caem
  **abaixo do mínimo** das oito antigas — 18 e 9 contra 20, 21, 34, 48, 60, 68,
  173, 196. Isso não depende da conta de poder do 693: sob a nula, uma peça
  abaixo do mínimo de oito tem ~1/9, e as duas ~1%. **O `ALVO_SHORT` global NÃO
  mudou**, porque o experimento 38 segue sem leitura nos outros dois canais e
  mexer no global apagaria o braço inteiro. Aprendizado 698.
  **E a lição de método: compare peça com peça na MESMA FAIXA DE IDADE**, lendo a
  janela do próprio `metricas`. Comparar piso atual de peças de idades diferentes
  é o efeito (D) da rotina, e foi o que viciou as minhas leituras anteriores
  deste canal.

## A mira de duração tem INTERAÇÃO CANAL × TRATAMENTO — e é por isso que ela é por canal

**Aprendizado 701, `alto`, observado.** Na janela **casada** de 4 a 8 h de vida,
no `kolejny`:

| mira | peças |
|---|---|
| nova (41–43 s) | **209** (s015, 10 cenas), **117** (s017, 10), **115** (s014, 5), **83** (s016, 10) |
| antiga (34–35 s) | **17**, **13**, **4**, **0** (s004 a s007) |

Sem sobreposição nos dois sentidos: os quatro novos acima dos quatro antigos dá
1/C(8,4) = **1,4%** sob a nula. **E no labtreinamento o sinal é o OPOSTO** (698).
Logo não existe "a mira certa do short" — existe a mira certa **de cada canal**, e
é assim que `ALVO_POR_CANAL` deve crescer.

**CONFUNDIDOR QUE NÃO SAI DO RELATO:** as peças de mira antiga são de 08/10 e as
de mira nova de 09/10. Crescimento do próprio canal entre os dias explica parte ou
tudo, e isto **não é aleatorizado no tempo**.

**Experimento 40 (dez cenas) ainda sem leitura:** na mesma janela, dez cenas
(83, 117, 209) contra cinco cenas (115) — n=1 de um lado.

## Dois `grava_metricas_janela` no mesmo statement colidem

**Aprendizado 702.** Dentro de um único statement o `now()` não avança, então a
segunda chamada viola `metricas_youtube_id_coletado_em_key`. **Um statement por
chamada.**

## O denominador da conversão NÃO é o `viewCount` do canal

**Aprendizado 697, `crítico`.** O `channels.list?part=statistics` devolveu
`viewCount` **byte a byte idêntico às 10:15 e às 18:10** — oito horas — nos três
canais, enquanto 17 peças somavam centenas de views. E em dois canais a soma das
peças da máquina **já é MAIOR** que o `viewCount` do canal: epomeno 15.454 contra
12.152, kolejny 10.625 contra 8.406. Logo ele não é a soma e não serve de
denominador (converge com o 638: não conta Shorts).

**O denominador é `sum(views)` das peças da própria máquina, coletadas na hora.**
Medido em 09/10 18:10, 153 ids em quatro lotes, todos `200`:

| canal | shorts | longos | conversão |
|---|---|---|---|
| epomeno | 13.745 (n=32, média 430) | 1.709 (n=18) | 17/15.454 = **1,10 por mil** |
| kolejny | 9.889 (n=41, média 241) | 736 (n=24) | 8/10.625 = **0,75 por mil** |
| labtreinamento | 4.165 (n=25, média 167) | 213 (n=13) | **não normalizável** (668) |

Isso retrata os 1,32 e 0,95 por mil que eu usei o dia inteiro. **Canal com acervo
anterior à máquina não tem normalização possível**, porque o numerador inclui
plateia que a máquina não trouxe.

**E o contador de canal NÃO é um instrumento uniforme** (aprendizado 703, `alto`,
medido às 22:10): entre 18:10 e 22:10 o kolejny subiu **+291** e o labtreinamento
**+358**, enquanto o epomeno ficou byte a byte igual pela **terceira** leitura
seguida — 10:15, 18:10, 22:10, **doze horas** — e no mesmo intervalo as peças do
epomeno somaram **+297** ao vivo (só o `ZxHWcfDNovM` indo de 445 a 724). **CORREÇÃO, às 02:10 (aprendizado 705):** o contador do epomeno **não estava
parado** — ele saltou de 12.152 para **12.935** (+783) de uma vez, um degrau de
~12 h. E a leitura se inverteu: agora foram kolejny e labtreinamento que vieram
byte a byte idênticos. **Cada canal tem o seu degrau e a sua fase, e o degrau
pode passar de 12 h**, então o contador de canal não serve de denominador nem
para declarar canal morto. O labtreinamento mostra o outro lado: canal +358 contra peças +78,
isto é, o crescimento é do acervo anterior à máquina (668).

Conversão às 22:15, com o denominador certo: epomeno 17/15.751 = **1,08 por mil**,
kolejny 8/10.830 = **0,74**, labtreinamento **não normalizável**.

## Antes de citar número de aprendizado
`select max(id) from aprendizados` no projeto **vevocauwtarctfwngrch**.
O `APRENDIZADOS.md` do repo está desatualizado contra o banco.

## Entrega
`docs/publicar-pela-sandbox.md` e `docs/schema-supabase.md`. O render é no
runner com `publicar=false`. O zip do artefato abre **flat** e o `conduz.py`
espera `f/<pacote>/`.

**RETRATAÇÃO DE 12/10, e é desta frase: "a publicação é pela ponte" deixou de
ser verdade.** O dono colou o `YT_OAUTH_JSON`, e a publicação passou a sair pelo
**`retomar.yml`**, que refresca o access token no próprio runner e não toca o
Supabase. Provado em produção duas vezes no mesmo dia: `epomeno-epipedo-s016` =
`6TNDVugoz5I` (run `38175747708`) e `labtreinamento-s013` = `byriXB1gSg8`
(`38211879374`). O `estado_b64` sai do `fabrica/corpus_publicados.json` e tem de
trazer `titulos_no_ar_n`, senão o runner recusa. A ponte continua existindo; ela
só não é mais o caminho.

## As travas que não se negociam
Estão na rotina horária, e nenhuma delas muda por conveniência de uma rodada.
A que mais custa esquecer: **não apague vídeo publicado sem o dono dizer.**

## A madrugada não produz leitura

**Aprendizado 706, `medio`, medido às 06:09 de 10/10.** O acervo inteiro da frota
— **153 ids em quatro lotes, os quatro `200`** — andou assim entre 02:10 e 06:09:

| canal | 02:10 | 06:09 | delta em 4 h |
|---|---|---|---|
| epomeno | 15.816 | **15.818** | **+2** |
| kolejny | 10.843 | **10.824** | **−19** (oscilação do 650) |
| labtreinamento | — | 4.542 | — |

As 17 peças do dia 09/10 somaram **3.085**, byte a byte igual à leitura das 04:08,
e só o `ZxHWcfDNovM` mudou (+1). Inscritos **17 / 8 / 67**, sem mudança desde
22:15. **Delta dessa ordem é menor que a oscilação da própria peça**, então a
janela da madrugada é cega por construção: rodada noturna é de medição e
engenharia, **nunca de veredito**. Conversão com o denominador certo (697):
epomeno **1,075 por mil**, kolejny **0,739**, labtreinamento não normalizável.

## `grava_metricas_janela` grava a réplica DAQUELA chamada, não o máximo

**Aprendizado 707, `alto`, medido às 07:09 de 10/10, e retrata parte do 688.**
O estimador é o **máximo** das três leituras (688), mas a gravação recebe **um**
`req_id`: se o máximo caiu em outra leitura, a tabela guarda a réplica atrasada e
**subestima para sempre**. No `ZxHWcfDNovM` as três leituras deram
**830, 833, 830** — o máximo caiu na **segunda**, e o `grava_metricas_janela(901)`
gravou 830.

**Duas consequências:**
1. **Descubra qual `req` tem o máximo ANTES de gravar, e grave esse** (em
   statement próprio, pelo 702).
2. **Cai a parte do 688 que dizia que a réplica fresca vem na TERCEIRA leitura.**
   Ela pode cair em qualquer uma, e a terceira pode voltar para a atrasada. O que
   sobrevive do 688 é só o estimador: **máximo como piso.**

## A réplica atrasada é por CHAMADA, não por peça

**Aprendizado 708, `alto`, medido às 08:08 de 10/10, e substitui o procedimento
do 707.** As quatro peças que divergiram entre as três leituras divergiram com a
**mesma forma — {alto, baixo, alto}**:

| peça | leitura 1 | leitura 2 | leitura 3 |
|---|---|---|---|
| `ZxHWcfDNovM` | 833 | **830** | 833 |
| `aT1y_jxUejM` | 91 | **90** | 91 |
| `cBBYHdP5JYA` | 23 | **22** | 23 |
| `JEnKrpgLJ0A` | 22 | **21** | 22 |

As outras dezesseis vieram idênticas nas três. A leitura 2 caiu **inteira** numa
réplica atrasada: **a réplica é da CHAMADA, não de cada id.**

**Procedimento, e é mais simples que o do 707:** compare a **soma** das três
chamadas, escolha a de soma máxima e chame `grava_metricas_janela` nessa **uma**
(um statement, pelo 702). Não cace o máximo peça por peça.

**E desde 11/10 isso NÃO se faz mais no olho:** `fabrica/replica.py` tem
`chamada_para_gravar`, `piso`, `faixa`, `divergentes` e `mesma_forma`, com os
números reais de 07/10 e 08/10 travados em teste. **Use `mesma_forma` antes de
gravar:** se os divergentes NÃO compartilham a forma, a divergência não é da
chamada, a hipótese do 708 não se aplica àquela rodada, e isso vai no relato em
vez de virar gravação automática. E `piso` não trata id ausente como zero —
ausência é silêncio, não leitura de zero.

**E isto enterra de vez a "terceira leitura" do 688:** a réplica fresca foi a
terceira em 09/10, a segunda às 07:09 e a primeira e a terceira às 08:08. A ordem
não tem regra; só o estimador sobrevive — **máximo como piso.**

## A credencial do GitHub ENTRA em sessão rodando — eu afirmei o contrário o dia todo

**Aprendizado de 11/10, e é uma RETRATAÇÃO minha.** Eu escrevi aqui e na rotina
que "reconectar no claude.ai NÃO entra numa sessão já rodando; isso pede sessão
nova", e repeti isso ao dono em várias rodadas. **É falso.** Às 02:40 de 11/10,
depois de o dono instalar o Claude GitHub App na conta `sampaioopablo1-lgtm`
(pelo link **"Instalar em outra conta"**, sem desvincular nada), esta mesma
sessão passou de `imobjazz-eng`/`push: false` para `sampaioopablo1-lgtm`/
`push: true` e o `git push` funcionou — sem sessão nova.

**O erro de raciocínio:** eu tratei "ficou vinte horas em 403" como prova de que
a credencial nunca atualiza. Era prova apenas de que ela não atualiza **enquanto
ninguém reconecta**. Ausência de mudança não é impossibilidade de mudança.

**E o caminho certo não é desvincular:** o bloco *Claude GitHub App* aceita
**várias contas instaladas ao mesmo tempo**. Instalar na segunda conta não tira
nada da primeira. Foi o dono quem viu isso na tela e perguntou; eu vinha pedindo
troca de conta, que era pior e desnecessário.

**O que eu escrevi aqui e que CAIU EM 12/10 — e é o MESMO erro de raciocínio
outra vez, dentro da correção dele.** Eu escrevi "o `mcp__github__*` NÃO se
recupera — segue com `invalid session` depois da troca". **Falso.** Na rodada das
08:07 de 12/10 o servidor reconectou sozinho e o `mcp__github__get_job_logs`
devolveu log completo, incluindo o traceback do `publicar.py:238` e o
`youtube_id` que a anotação não carregava.

Eu acabara de escrever, nesta mesma seção, que *"ausência de mudança não é
impossibilidade de mudança"* — e então apliquei exatamente o raciocínio proibido
à ferramenta seguinte. **Trate indisponibilidade de MCP como estado, nunca como
propriedade:** sonde antes de dizer que não há rota.

**O que continua valendo:** a rota das ANOTAÇÕES (abaixo) funciona SEM o MCP, e é
ela que se usa enquanto o MCP estiver fora. Ela só não substitui o log: ela
carrega os `::warning::`/`::notice::`, e o que não for emitido assim não aparece
— foi por isso que o motivo da falha de 07:21 e o `youtube_id` de 07:23 ficaram
invisíveis para mim por uma rodada inteira.

## Para ler um job quando o MCP está fora: ANOTAÇÕES

`gh` recusa redirecionamento entre hosts, e o resumo do job (`STEP_SUMMARY`) não
sai pela API. Mas os `::warning::` e `::notice::` saem, pela própria api.github.com:

    gh api repos/<owner>/<repo>/check-runs/<job_id>/annotations

Foi assim que eu li o ciclo de 02:43 de 11/10 inteiro sem o MCP.

## "É só esperar a virada do ciclo" — FALSIFICADO, e era afirmação nossa

**11/10, e corrige o que o `expurgo-storage.yml` dizia no próprio topo.** O
arquivo prometia que "a máquina destrava na virada e reestoura em uma semana",
e por isso o conselho que saía daqui era esperar. **O 402 é CONTÍNUO de 25/08 a
11/10 — 47 dias, atravessando pelo menos uma e provavelmente duas viradas de
ciclo.** A previsão está morta pelo resultado.

**E a explicação já estava escrita no mesmo arquivo, trinta linhas abaixo: o nó
é CIRCULAR.** O 402 bloqueia o Storage; o expurgo precisa do Storage para
apagar; os 3,7 GB nunca saíram; cada ciclo novo reestoura a cota no primeiro
dia. A virada chega com o mesmo 3,7 GB lá dentro.

**Duas consequências:**
1. **O remédio é humano** — Pro (levanta na hora E deixa o expurgo rodar) ou
   mover o projeto para outra organização. **Não diga ao dono "é só esperar".**
2. **A anotação de 402 do ciclo é TEXTO NOSSO, não leitura da API.** Ela vem de
   `expurgo-storage.yml:118` e repete a conclusão de 25/08. Tratar a própria
   anotação como evidência fresca é o efeito do §3.8 — portão verde fabrica
   "está tudo certo".

## A publicação sem banco: o código existe, o SEGREDO está vazio — medido

**11/10, run `38137596808`, e isto corrige duas afirmações minhas.** O dono
pediu para tirar a dependência da reconexão manual. Medido antes de propor:

1. **O 403 na API de secrets é do PROXY, não de permissão.** A mensagem literal
   é `"Access to this GitHub Actions path is not permitted through this proxy"`,
   e ela repete com **`admin: true`** no repo. Minha pendência dizia só "403 em
   `actions/secrets/public-key`", o que sugeria que credencial melhor resolveria.
   **Não resolve, e nunca ia.**
2. **Não existe ponte de Postgres DIRETO** no repo — nenhum `5432`, pooler ou
   `psycopg`. O 402 é do *gateway*, então conexão direta o contornaria em teoria,
   mas ela não foi construída e a senha do banco não está ao meu alcance.
3. **A rota sem banco JÁ EXISTE e está completa** (`retomar.yml`): o segredo
   `YT_OAUTH_JSON` guarda `{canal: {client_id, client_secret, refresh_token}}` e
   o runner refresca o access token direto no Google, sem Supabase.

**E a sonda provou que os quatro segredos estão VAZIOS** —
`YT_OAUTH_JSON` e os três `YT_TOKEN_*`, todos com **0 chars** no runner. Logo
**não falta código, falta CREDENCIAL**, e nenhuma engenharia inventa um token do
Google.

**ISTO CADUCOU EM 12/10, e fica retratado aqui em vez de só no fim do arquivo:**
o dono colou o `YT_OAUTH_JSON`, a sonda passou a ver os três canais e a
publicação funcionou. Os três `YT_TOKEN_*` seguem vazios **e não precisam
existir** — o `retomar.yml` refresca sozinho. O que a credencial colada **não**
trouxe é o escopo de analytics: a sonda diz `analytics=NAO` nos três, porque
isso depende do clique de consentimento do Google, não de segredo. Quem lê só o
parágrafo acima conclui "a máquina está parada por falta de credencial", e ela
não está.

**O instrumento ficou:** `fabrica/sonda_oauth.py` + `sonda-oauth.yml` dizem,
canal por canal, se o refresh vive e quais escopos vieram — **sem imprimir
refresh token, client_secret nem access token**. Rode depois de qualquer
colagem, em vez de supor.

**O caminho mínimo para o dono está em `docs/destravar-sem-reconexao.md`:** UMA
colagem de `YT_OAUTH_JSON`, com a consulta pronta para o SQL Editor do Supabase
(que **não passa pelo conector nem pelo REST**, então o 402 não atrapalha). Isso
mata a ponte e tira o Supabase do caminho da publicação. **Reconectar o conector
é a PIOR das três opções** — devolve o banco mas deixa a ponte e o 402 de pé.

## O 402 fecha a porta PARA O RUNNER TAMBÉM

**Medido em 11/10**, anotação literal do `diario.yml`:
`porta FECHADA (HTTP 402) — rodando pelo retrato de fabrica/ponte/, gerado em
2026-10-06`. Eu ia construir um workflow de medição aproveitando
`SUPABASE_SERVICE_ROLE_KEY` do runner, **e não adianta**: o `402` é da
organização e alcança o runner igual. A restrição de cobrança da org pessoal é o
gargalo único — ela bloqueia o REST, bloqueia o runner, e em 11/10 bloqueou até a
**transferência do projeto** para outra org ("can't be transferred to a Free
organization while the source organization is in an active grace period").

## O redisparo de pacote já publicado — consertado e verificado em produção

**Causa:** o orquestrador lia duplicata só da lista `videos`, que com a porta
fechada é o retrato de **06/10** — cego para o que foi publicado a partir de
07/10. O `prontidao` lia do `corpus_publicados.json`, atualizado a cada
publicação. **Duas fontes discordantes:** o portão pegava, o orquestrador não, e
a Frota morria todo ciclo com `kolejny-poziom-016`, `labtreinamento-010` e
`epomeno-epipedo-015` — 19:27, 22:49 e 01:27.

**Conserto:** `titulos_do_corpus()` entra por parâmetro `titulos_extra` em
`estado`/`proximo`/`relatorio`, ligado pelo `main`. `titulos_no_ar` continua
PURA — embutir a leitura nela quebrou quatro testes, incluindo fazer o teste do
token morto nunca alcançar o motivo do token.

**Verificação em produção:** ciclo `4ba1a12` às 02:43 devolveu **"Nenhum pacote
pronto"**, contra o `526255e` de 01:27 que disparou a Frota para a falha.
Confundidor declarado: eu disparei com `disparar=false`, então o que prova é a
anotação da matriz, não a ausência do run da Frota.

**E agora tem teste, que era o que faltava:**
`tests/test_duas_fontes_de_duplicata.py` (6 testes). Ele ancora nos TRES
pacotes que morreram de verdade, confere antes que eles ainda estao no corpus
(senao passaria por vacuidade), exige que `estado` e `relatorio` leiam a MESMA
segunda fonte, e exige que o `main` a ligue nas TRES acoes — ligar em duas e
esquecer a terceira reconstroi o defeito inteiro. Conserto sem teste volta, e
este voltava CALADO: a lista `videos` so fica cega com a porta fechada, que e
exatamente quando ninguem esta olhando.

**Fora do escopo, medido:** **86 das 183 specs (47%)** passam de 4 palavras na
thumbnail. O molde histórico viola o portão `variedade` em metade dos casos —
spec nova não deve se espelhar nele.

## O que entrou dos cinco projetos externos — e o que NÃO entrou

**11/10. O dono mandou estudar cinco repositórios e aplicar.** Estudados os cinco.
Entrou pouco, e **nada por autoridade da fonte** — só o que converge com medição
nossa, que é a mesma régua da §5 da rotina.

**NÃO adotados, com motivo:**
- `youtube-automation-agent` — pipeline Node completo e paralelo ao nosso. Não
  tem portão, nem corpus anti-duplicata, nem disciplina de medição. Trocar o
  nosso por ele seria **regressão**, não ganho.
- `ai-video-generator-claude` — prompts para Higgsfield. Os shorts soltos têm
  b-roll ZERO por decisão, e Higgsfield consome crédito: só se o dono pedir.
- `claude-youtube` (as *skills*) — andaime para criador humano e orientado a
  LONGO: o `hook.md` pede "gancho de 30 s, ~75 palavras", e o nosso short inteiro
  tem 41. Os scripts de execução dele usam **a YouTube Analytics API com OAuth**,
  isto é, o escopo que nós perdemos — **confirmação independente de que o clique
  de consentimento é o único caminho**, não um atalho.
- `claude-code-youtube-mcp` — exige Node, chave de API e instalação pelo dono.
  O que tem de novo e interessante é o **mapa de "most replayed"**, que é proxy
  de retenção em canal ALHEIO e por dado público. Fica como sugestão ao dono,
  não como dependência nova.
- `claude-real-video` — frames + transcrição sincronizada. Nós já fazemos análise
  de quadro com `ffmpeg`/`signalstats`, e o gargalo não é ler vídeo dos outros.

**ENTROU, por convergência (`references/shorts-playbook.md`):**
1. **Cadência de mudança visual a cada ~3 s.** Converge com a física que nós
   medimos sozinhos (690/699: a alavanca é a duração da cena).
2. **Faixa boa de 15 a 60 s, com picos em 13 s e 60 s.** É a **segunda** fonte
   independente contra o experimento 38 — a primeira foi o nosso próprio
   `chart=mostPopular` (10 a 35 s). Não muda `ALVO_SHORT` agora: 38 segue sem
   leitura de 12 h, e views/peça é cego sob CV 0,66.
3. **Conversão de "vídeo relacionado" abaixo de 1%.** Apoia o experimento 37
   (o CTA pedindo inscrição em vez de apontar para o longo).

Procedência declarada e mista: "estudo de 35 bilhões de views" sem nome, `vidIQ`
que é fornecedor de ferramenta, e Tubefilter/Digital i com nome e data.

## A sobrecarga por cena é POR VOZ, e é P — retrata o meu "~1,9 s fixos"

**Medido em 11/10, e corrige o número que eu mesmo escrevi acima.** Não há 1,9 s
fixos por cena. A sobrecarga é `P + 0,300`, onde **P é o silêncio de fim de FRASE
da própria voz** (já medido em `MODELO_VOZ`) e 0,300 s é o intervalo de montagem:

| voz | R | P | sobrecarga/cena |
|---|---|---|---|
| `pt-BR-ThalitaMultilingualNeural` | 17,47 | 0,737 | **1,04 s** |
| `el-GR-NestorasNeural` | 20,61 | 1,273 | **1,57 s** |
| `pl-PL-MarekNeural` | 20,07 | 1,419 | **1,72 s** |

O "12 cenas somam 21,9 s" que eu medi era a voz POLONESA, a de maior P — eu
generalizei o pior caso para a frota inteira, que é o mesmo erro do 679/698
(tratar como da frota o que é por voz/por canal).

**E P é por FRASE, não por cena:** cena com duas frases paga 2P. Logo **uma frase
curta por cena** é o que minimiza a sobrecarga.

**O que isso abre:** a cadência de 3 s **não** se alcança somando cenas a um short
de 41 s — ela se alcança ENCURTANDO o total. Com uma frase por cena:

| voz | chars/cena para cadência de 3,0 s | 11 cenas |
|---|---|---|
| pt-BR | **34** | **33,0 s** |
| el-GR | **29** | **33,0 s** |
| pl-PL | **25** | **33,0 s** |

E **33 s cai dentro do override medido do `labtreinamento` (33,0 a 37,0)**. Ou
seja, para aquele canal, três coisas apontam para o mesmo ponto: a mira que o
próprio canal mediu (698), a cadência externa de 3 s, e a faixa curta das duas
fontes de tendência. **No kolejny o sinal medido é o OPOSTO (701)** — lá a mira
longa ganhou, e isso não se mexe sem leitura.

**Nada disso muda `ALVO_SHORT` nem `ALVO_POR_CANAL` hoje.** Fica como desenho
pré-registrado para quando houver retenção: **labtreinamento, 11 cenas de uma
frase curta, ~33 s** — o primeiro teste em que cadência, duração e mira do canal
concordam.

## Quando o banco está fora, a rodada é de CONSTRUÇÃO — não de relatório vazio

**Pedido do dono em 11/10, ao sair:** *"coloque na rotina, auto ajuste,
construção, reparo do sistema"*. Vale como instrução permanente para toda rodada
que não consegue medir nem publicar.

**Antes de tudo, SONDE os dois bloqueios — uma vez, barato, e registre:**
- banco: `mcp__Supabase__list_projects` tem de mostrar `maquina-yt-dark`;
- porta do REST: dispare `diario.yml` com `disparar=false` e leia
  `check-runs/<job>/annotations`. A anotação diz `porta ABERTA` ou
  `FECHADA (HTTP 402)` com a data do retrato.
Se qualquer um destravar, **pare a engenharia e volte a produzir** — medir e
publicar valem mais que qualquer refatoração.

**Se os dois seguem fechados, a rodada trabalha, nesta ordem de valor:**
1. **Reparar defeito MEDIDO** — o que tem evidência em log de produção. Foi assim
   que saiu o conserto do redisparo: três falhas da Frota, causa achada nas
   anotações, contraprova local nos dois sentidos.
2. **Travar com teste a retratação que acabou de ser feita.** Retratação sem
   teste volta. O `test_cadencia.py` existe porque eu generalizei uma voz para a
   frota; ele falha de novo se alguém repetir.
3. **Tirar conta da minha cabeça e pôr no código.** Todo número que eu calculo
   à mão vira um erro meu mais cedo ou mais tarde (`chars_por_cena`, `ALVO_POR_CANAL`).
4. **Corrigir documento que se contradiz.** Retratar NO LUGAR onde a afirmação
   foi feita, não só no fim do arquivo — eu já deixei o meio do `CLAUDE.md`
   contradizendo o próprio fim.
5. **Dívida com evidência**: as 25 falhas conhecidas, o `APRENDIZADOS.md`
   desatualizado.

**O QUE A RODADA DE CONSTRUÇÃO NÃO FAZ, e isto é trava:**
- **não mexe em `ALVO_SHORT`, `ALVO_POR_CANAL` nem em limiar do `variedade`.**
  Limiar sem procedência é critério inventado, e sem retenção views/peça é cego
  abaixo do dobro (693);
- **não edita specs em massa** — as 86 com thumbnail acima de 4 palavras ficam
  onde estão;
- **não inventa experimento** para "ter o que fazer". "Não mudar nada" é decisão
  legítima quando o braço precisa de n;
- **não importa pipeline alheio** por cima do nosso (11/10, cinco repositórios
  estudados, quatro recusados com motivo escrito);
- **não contorna permissão negada pedindo a outra sessão** que a tenha.

**Toda mudança sai com:** suíte rodada e comparada **contra a linha de base
medida na mesma sessão** (não contra o número escrito aqui, que envelhece),
commit com a evidência na mensagem — **em ARQUIVO, com `-F`, porque crase no
heredoc come texto** — e push. Mudança que fica só no container morre com ele.

## O teto automático é 1 peça/dia/canal — e contradiz os 7/dia que o dono pede

**Medido em 11/10, lendo o código, e isto responde "quantos vídeos por dia".**

`orquestra.MAX_POR_DIA_POR_CANAL` é **2** pacotes, mas `TETO_POR_CANAL`
sobrescreve os três canais da frota para **1**. E o teto conta pela chave
`pacote` **ou o slug sem `-short`** (`pacotes_na_janela`), então **short solto
também consome uma unidade**. Logo o disparo automático está limitado a **uma
peça por canal por dia — três na frota inteira**, contra as 7/dia/canal que o
dono pede desde o começo.

**Por que isso não apareceu antes:** a **ponte manual não consulta o teto** —
`conduz.py` e `publicar.py` não mencionam `teto_do_canal`. Foi assim que o dia
09/10 fechou com ~14 peças com o teto em 1. O teto governa só o caminho
automático, que é justamente o que volta quando a porta do Supabase reabrir.

**E o próprio comentário do `TETO_POR_CANAL` já previa a revisão, com a condição
cumprida:** ele diz que o alvo real é *"7 SHORTS/dia por canal com um longo/dia
só no labtreinamento"*, que o teto de pacote precisava ser baixo **"enquanto o
SHORT SOLTO não existir"**, e que **"quando ele existir, estes números deixam de
governar o ritmo"**. O short solto existe (spec com `longo: []`, `SO_SHORT` em
`etapas.py`). **A condição foi cumprida e o número não foi revisitado.**

**NÃO mexi no teto**, e o motivo é a trava da seção anterior: é parâmetro de
produção, e o comentário dele carrega medição contrária que continua válida —
nove de treze longos com zero view, o `captions.insert` comendo ~400 das ~500
unidades de cota por pacote, e risco de spam não medido num canal de poucos
inscritos. **Subir isso é decisão do dono**, e tem uma forma barata que respeita
as duas coisas: subir o teto **só para short solto**, deixando o longo em 1/dia —
que é literalmente o alvo escrito no comentário.

**E o teste já reclamava disso o tempo todo:** `test_orquestra` diz
`labtreinamento esta no TETO_POR_CANAL com 1, que nao e maior que o teto geral 2
— entrada inutil ou erro`. Ele estava certo, estava contado entre "as 25
conhecidas", e ninguém leu o que ele dizia.

## As 25 falhas da suíte NÃO são o que eu escrevi aqui

**Retratação de 11/10.** Eu descrevi a linha de base como "specs já publicadas
que o `prontidao` recusa por título duplicado, e fonte Devanagari ausente".
**Medido, a composição é outra:**

- **15** de `test_narracao_das_specs` — specs que *"sairiam da matriz caladas"*,
  por **números demais numa frase** e por **capítulo sem margem** (63–64 s contra
  o piso de 60 s). A maioria é de canal parado, mas há três do epomeno
  (`-008`, `-009`, `-010`) e uma do labtreinamento (`-005`);
- **3** de `test_thumbnail_legivel`, **3** de `test_prontidao`;
- **1** do teto por canal (acima), **1** de acentuação turca, **1** de
  `ortografia`, **1** de `autor`, **1** de `confere_broll`.

**O remédio que o próprio teste prescreve não é silenciar:** ele existe para que
*"spec parada que ninguém sabe"* apareça, e aceita o inventário `PARADAS` com o
motivo escrito.

**E "são quinze julgamentos" era MEU enquadramento errado — retratado em 11/10,
com o levantamento em `docs/paradas-a-decidir.md`.** Medido, são **três
famílias**, e **onze das quinze são a mesma** (capítulo estimado em 61–64 s
contra o piso de 60 s, com a voz errando até 4,9% nos dois sentidos — o defeito
que matou o `setiap-level-014` em 01/09). O remédio dessas onze está escrito
pelo próprio portão e é mecânico: esticar o texto até 64 s estimados. As outras
quatro são três de "quatro números numa frase" (quebrar em progressão) e uma de
acentuação.

**E o que mais encurta a decisão: só QUATRO das quinze são de canal da FROTA** —
`epomeno-epipedo-008`, `-009`, `-010` e `labtreinamento-005`. As outras onze são
de canal PARADO, onde consertar não produz nada hoje; elas só ocupam a contagem
das 25. **Eu não conserto sozinho** porque a trava diz que rodada de construção
não edita specs em massa, e texto de capítulo é conteúdo que vai ao ar em canal
vivo.

## O cron `*/30` dispara 5 vezes por dia, não 48 — medido em 100 runs

**11/10, e isto derruba uma afirmação que está no `diario.yml`, na rotina e nos
comentários do `orquestra.py`.** O `diario.yml` declara `cron: "*/30 * * * *"` e
todo mundo aqui repete "o ciclo dispara de meia em meia hora". **Não dispara.**

Os **100** runs de evento `schedule` mais recentes, cobrindo **470,5 h**
(21/09 a 11/10):

| | |
|---|---|
| disparos por dia, na prática | **5,1** |
| mediana entre disparos | **287 min (4,8 h)** |
| menor intervalo observado | **129 min** |
| maior | **498 min (8,3 h)** |
| intervalos acima de 2 h | **99 de 99** |

**Nem uma única vez em vinte dias o cron andou de meia em meia hora.** O agendador
do GitHub Actions é melhor-esforço e atrasa ou descarta disparo sob carga; o nosso
cai em ~1/10 do declarado.

**Três consequências que importam:**
1. **O ritmo automático tem outro teto, e é mais apertado que o do `TETO_POR_CANAL`:**
   ~5 oportunidades de disparo por dia para a frota inteira. Mesmo subindo o teto
   por canal, o caminho automático não entrega 7/dia/canal.
2. **A lógica de janela horária fica comprometida.** O comentário do `proximo`
   diz que a faixa morta é só preferência, "não portão", porque *"a fila anda de
   meia em meia hora, então todo canal alcança a própria janela dentro do mesmo
   dia"*. Com mediana de 4,8 h entre disparos, **essa premissa é falsa** — um
   canal pode passar o dia sem que nenhum disparo caia na janela boa dele.
3. **Não adianta baixar o cron para `*/15`.** O limite não é o que pedimos, é o
   que o agendador entrega. Quem quiser ritmo garantido precisa de disparo
   EXTERNO (`workflow_dispatch`), que é o que eu fiz à mão hoje às 02:43 e 03:37.

**Como remedir, sem depender de mim:**

    gh api 'repos/<owner>/<repo>/actions/workflows/diario.yml/runs?per_page=100&event=schedule' --jq '.workflow_runs[].created_at'

e olhe os intervalos. **Conte disparo de `schedule` separado de
`workflow_dispatch`** — misturar os dois esconde exatamente este defeito, porque
os meus disparos manuais tapam os buracos do agendador.
