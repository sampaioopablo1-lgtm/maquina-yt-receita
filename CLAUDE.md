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
"dez a CATORZE" sem conferir a sobrecarga. Há **~1,9 s fixos por cena** no
`ensaio` (medido: 12 cenas de um caractere já somam 21,9 s). Doze cenas gastariam
22 s só em padding e estourariam o teto de 43,1. O teto real no alvo atual é
**onze**, e o ponto de equilíbrio é **10 cenas de ~40 caracteres** ou 11 de ~34.
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

## Antes de dizer que a máquina está sã
- `python3 -m pytest tests -q --ignore=tests/test_mcp.py --ignore=tests/test_banco_de_pautas.py`
  Linha de base medida em 09/10/2026: **25 falham, 2.048 passam, 436 skip.**
  Falha nova é a sua; as 25 são conhecidas (specs já publicadas que o
  `prontidao` recusa por título duplicado, e fonte Devanagari ausente — as duas
  são o portão funcionando).
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
runner com `publicar=false`; a publicação é pela ponte. O zip do artefato abre
**flat** e o `conduz.py` espera `f/<pacote>/`.

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
