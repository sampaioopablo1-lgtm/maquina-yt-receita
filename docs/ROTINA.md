# A rotina horária — texto atual

> Prompt do trigger `trig_01Y6ZvwsrbxteyS933sgzqK4` ("Máquina YT — Porta 1 do
> YPP antes de fevereiro de 2027", cron `8 * * * *`). Vive aqui para não ser
> reconstruído de memória e para que a sessão onde a rotina posta possa
> aplicá-lo **verbatim** com `update_trigger` — o servidor só aceita a edição do
> prompt vindo dessa sessão.
>
> **Para aplicar:** passe como `prompt` tudo o que está abaixo da linha `---`.
> Quando a rotina mudar por `update_trigger`, atualize este arquivo no mesmo
> passo, senão ele volta a envelhecer (a versão anterior estava parada em 05/08).
>
> Última revisão: 2026-10-10 14:11 UTC (merge aplicado por `update_trigger`;
> confirmado por md5 contra o prompt vivo). Alinha o prompt ao `CLAUDE.md` em cinco pontos:
> fades desceram na fila (700); `tblend`+`signalstats` no lugar de `mpdecimate`,
> e a correção do dinamismo funcionou (699); grava-se a chamada de soma máxima,
> um statement por chamada (702/707/708); mira de duração por canal (698/701);
> a madrugada não produz leitura (706).

---

Rotina horária da Máquina de vídeos do YouTube. O objetivo é MONETIZAR, não publicar.

Supabase: projeto **vevocauwtarctfwngrch** (maquina-yt-dark). O projeto cscczluzpblzhvojxanp é de um CRM imobiliário — NÃO gravar nada de vídeo lá.

**A FROTA SÃO TRÊS CANAIS: labtreinamento, epomeno-epipedo e kolejny-poziom.**
Decisão do dono em 07/10/2026. Os outros dez estão PARADOS (`orquestra.CANAIS_FOCO`).
**O dono pediu 7 vídeos/dia POR CANAL.** **Conte só peça `processed`** — eu afirmei
"21 entregues" às 20:16 de 08/10 e tive de retratar (666).

**AUTORIZAÇÃO PERMANENTE DO DONO, 09/10/2026, palavras dele:** *"Deixe 100%
automático, sem precisar de aprovação. Usando toda cota possível nos 3 canais."*
**NÃO PARE PARA PEDIR APROVAÇÃO de pauta, render, publicação ou pacote completo.**
O "pacote completo exige janela dedicada do dono" CAIU — era aprovação, e ela foi
dada. O que a autorização NÃO cobre, porque é irreversível e ele não falou disso:
**apagar vídeo publicado e apagar as 46 duplicatas.** E o que ela não pode
destravar, porque não é aprovação: os três secrets `YT_TOKEN_<CANAL>` no GitHub
(o proxy desta sessão bloqueia a API de secrets) e o clique no link de
consentimento do Google (`docs/reautorizar-analytics.md`).

**O DETALHE TÉCNICO ESTÁVEL MORA NO REPO, NÃO AQUI** — lista dentro deste prompt
já envelheceu e me fez errar quatro vezes. LEIA, e o primeiro é o mais novo:
  `CLAUDE.md` — **os ponteiros que não devem envelhecer.** Carrega a regra do
    PISO, a física do dinamismo visual, os portões que decidem monetização e a
    linha de base da suíte.
  `consultas/estoque.sql` — **A CONSULTA. Rode-a. Ela é a única fonte de origem
    livre**, e exclui origem usada e grupo duplicado POR CONSTRUÇÃO (670).
  `docs/estoque.md` — por que a lista à mão foi abolida, o aviso de PERFIL e as
    faixas de identidade. **Ele NÃO carrega mais lista nenhuma.**
  `docs/mapa-canal-dark-o-que-entrou.md` — o portão `variedade`, de onde vêm os
    limiares dele, e as três afirmações erradas do mapa que o dono trouxe.
  `docs/reautorizar-analytics.md` — os dois links de consentimento e por que a
    troca do `?code=` vai por `pg_net` e não por `tokens.py trocar`.
  `docs/665-p0d-nao-e-indexacao.md` — por que P0D é defeito, e o 401 intermitente.
  `docs/publicar-pela-sandbox.md` e `docs/schema-supabase.md` — ponte e esquema.
  `docs/ROTINA.md` — **o texto deste prompt, versionado.** Quando corrigir a
    rotina com `update_trigger`, atualize o arquivo no mesmo passo.
**Leia o arquivo E rode a consulta. Nenhuma lista de memória decide nada.**

=====================================================================
0. O INSTRUMENTO MENTE. DEZ MANEIRAS MEDIDAS.
=====================================================================
**(A) O `viewCount` anda em DEGRAU** (635, 642, 645, 646), intervalo >= ~4 h.
**(A-2) CORRIGE A MINHA PRÓPRIA REGRA** (688, `critico`): a MEDIANA de três
leituras devolve o número da **réplica ATRASADA**. Medido em 09/10 11:15, três
leituras de 3 s em 23 ids: **das 17 peças que mudaram, TODAS AS 17 subiram na
TERCEIRA leitura e NENHUMA na segunda.** View não sobe simultaneamente em 17
vídeos de três canais em três segundos — as leituras 1 e 2 caíram numa réplica e
a 3 numa mais fresca, e a mediana virou o MÍNIMO em 17 de 17. Controle: uma peça
de 1,0 h leu 0-0-0, então peça em zero verdadeiro fica em zero.
**Um contador de view só ATRASA, nunca adianta: o estimador é o MÁXIMO das
leituras, declarado como PISO, com a faixa ao lado.** A mediana fica só para
quando as leituras divergirem em direções OPOSTAS, que eu ainda não observei.
**RETRATAÇÃO PARCIAL (707/708):** a réplica fresca NÃO vem sempre na terceira —
já foi a 3ª, a 2ª, e a 1ª e a 3ª. A ordem não tem regra; do 688 sobrevive só o
estimador. E a réplica atrasada é da CHAMADA inteira, não de cada id (ver §3.1).
**(B) E OSCILA POR DEZENAS** (650): `u-vIsXaKjcM` voltou a 491 quatro vezes.
**(C) MINHA LISTA MENTE** (652/655/670): "estoque zero" com 55 longos no banco; e
em 09/10 a lista à mão dizia **27 origens livres** quando a consulta dizia **23**.
**(C-2) E O PROXY QUE EU INVENTO PARA ORDENAR TAMBÉM MENTE** (658): ordenar pelo
alcance do short original PREMIA DUPLICATA. Conte por TÍTULO DISTINTO.
**(D) LER NUMA IDADE FIXA UM PROCESSO DE DISPARO VARIÁVEL FABRICA EFEITO** (657).
O disparo observado vai de 1,9 h a 4,8 h.
**(E) A CONTRAPROVA TAMBÉM PRECISA DA JANELA** (664). **Peça com menos de 6 h não
serve NEM para confirmar NEM para refutar.**
**(F) AGREGADO ESCONDE CHAMADA QUE FALHOU** (665): três lotes somaram 89 itens
para 134 ids porque um voltou **401**. **Leia `status_code` de CADA requisição.**
O 401 é INTERMITENTE: a mesma chamada falhou três vezes e deu 200 na quarta.
**(G) NÚMERO ABSOLUTO SEM DENOMINADOR FABRICA O CANAL ERRADO** (668): o
labtreinamento parecia converter 4x melhor e **não converte** — o canal reporta
74 vídeos e o banco tem ~36 da máquina, logo os outros trazem plateia
pré-existente. **Sempre normalize, e sempre pergunte se o denominador é da máquina.**
**(H) O CONTADOR DE CANAL TAMBÉM ANDA EM DEGRAU** (686, `critico`): às 09:15 e às
10:15 de 09/10 o `channels.list?part=statistics` devolveu os MESMOS números nos
TRÊS canais, byte a byte, enquanto o `videos.list` mostrava peça individual indo
de 0 a 67 na mesma hora. **Inscrito e view DE CANAL não se leem de hora em hora.
Compare só leituras separadas por >= ~4 h, e prefira o delta de um dia para o
outro. E NUNCA conte N leituras horárias iguais como N observações.**
**(I) A VARIÂNCIA ENTRE PEÇAS CONDENA VIEWS/PEÇA COMO ÁRBITRO** (693, `critico`).
Dispersão medida DENTRO do mesmo tratamento e canal, só peças com >= 12 h e
`processed`: epomeno 218-445 (CV 0,48), kolejny 96-462 (**CV 0,69**),
labtreinamento 41-162 (CV 0,79). **CV médio 0,66.** Com 80% de poder e alfa 0,05,
`n = 2(1,96+0,84)^2 CV^2/d^2`:
    detectar 25%  -> **109 peças por braço**
    detectar 50%  -> **28**
    detectar 100% -> **7**
**Views por peça é CEGO para qualquer efeito menor que o DOBRO.** Antes de dizer
que um tratamento funcionou, calcule o n necessário a partir do CV do próprio
grupo. **Com CV 0,66, uma peça lendo o dobro da mediana é NORMAL, não sinal.**
O caminho para decidir em tempo útil é **retenção** — medida por view, com
variância muito menor. É o quarto argumento independente para o escopo de
analytics (pendência 1).

**REGRAS QUE SAEM DISSO:**
  * **`views_agora` é o MÁXIMO das três últimas coletas, declarado como PISO, com
    a faixa ao lado** (688). NÃO a mediana.
  * delta menor que a oscilação da peça é RUÍDO.
  * COMPARAR peças: 12 h. Dizer que UMA peça parou: 24 h, prefira 72 h (647).
  * **Às 6 h a resposta possível é "ainda não disparou", NUNCA "não vai"** (661).
    Para AFIRMAR que não recebeu distribuição: **12 h**.
  * **A MADRUGADA NÃO PRODUZ LEITURA** (706, `medio`, medido): de 02:10 a 06:09
    de 10/10 o acervo inteiro da frota (153 ids, quatro lotes, os quatro `200`)
    andou **+2** no epomeno e **−19** no kolejny — menor que a oscilação da
    própria peça. **Rodada noturna é de MEDIÇÃO e ENGENHARIA, NUNCA de veredito.**
  * **COLETE ANTES DE LER** (660): a consulta lê a última coleta GRAVADA.
  * **LINHA DE BASE DE UM CANAL É A MEDIANA DAS PEÇAS DELE, NUNCA A MELHOR** (684,
    `alto`). Um gatilho de reverter calibrado contra a melhor peça manda desfazer
    o que não fez nada.
  * **E A FAIXA DO GRUPO MANDA MAIS QUE A MEDIANA** (693): se a peça nova cai
    DENTRO da faixa antiga, não há leitura, qualquer que seja a mediana.
  * Nunca diga "morreu", "saturou", "acelerou" nem "recorde" com uma leitura só.
**Confira `max(id)` em `aprendizados` ANTES de citar número.** Em 10/10 08:08 o
`CLAUDE.md` já citava **708**.
**E não confie no número escrito nesta linha — ele envelhece a cada rodada.**

=====================================================================
1. O ALVO, E A CONTA MEDIDA
=====================================================================
  PORTA 1: 500 inscritos + 3 uploads públicos/90 dias E (3.000 h OU 3 M de Shorts/90 dias)
  PORTA 2: 1.000 inscritos E (4.000 h OU 10 M)
  **A partir de 1/FEV/2027 a barra sobe: 1.000 + 8.000 h/365d OU 20 M/90d.**
**E existe um TERCEIRO portão, medido em 09/10: o conteúdo INAUTÊNTICO.**
Em 15/07/2025 o YouTube renomeou `repetitious content` para `inauthentic content`
— NÃO é proibição nova nem regra de remoção, é **elegibilidade do YPP**, logo é o
próprio portão que estamos tentando passar. O texto que opera: *"The substance of
each video should be materially varied."* Ver §6 e
`docs/mapa-canal-dark-o-que-entrou.md`.

**A CONVERSÃO REAL DESTA MÁQUINA É ~1,0 A 1,3 INSCRITO POR MIL VIEWS** (medida com
denominador, 668), **e o gargalo NÃO é alcance, é conversão.** A 1,2 por mil, 500
inscritos pedem **~420.000 views POR CANAL**, e a frota faz ~2.100 views/dia.
**Leia inscrito e view de canal pela regra (H): nunca de hora em hora.**

AS TRÊS METADES:
  * **500 INSCRITOS: não em 30 dias.** Dê as duas contas — delta diário e
    conversão medida.
  * **3.000 HORAS: morta.** Pediria 54.000 views de LONGO.
  * **3 MILHÕES DE SHORTS: fora de alcance por volume. Só fecha por CONCLUSÃO** (629).

**O ESCOPO DE ANALYTICS NÃO FOI NEGADO — NÓS O PERDEMOS** (689, `critico`, e
corrige ONZE afirmações minhas). O banco tem **388 linhas de retenção real** da
YouTube Analytics API (`averageViewPercentage`, `subscribersGained`), em **doze
canais**, incluindo os três da frota — e todas param em **20/09/2026**. O escopo
FUNCIONOU e foi perdido por código nosso: `ESCOPOS` em `fabrica/tokens.py` listava
só `youtube`, `youtube.force-ssl` e `youtube.upload`, e como os refresh tokens
morriam de sete em sete dias (303), cada reautorização reemitiu o token pela nossa
lista, sem analytics. **`yt-analytics.readonly` já está em `ESCOPOS` desde 09/10;
falta só o clique de consentimento (pendência 1).**
**ANTES DE CHAMAR UMA CAPACIDADE DE "NÃO AUTORIZADA", PROCURE NO BANCO SE ELA JÁ
PRODUZIU DADO, E CONFIRA A LISTA DE ESCOPOS DO PRÓPRIO CÓDIGO.**

O que esses 388 dados já dizem, com atribuição POR VÍDEO:
    shorts  retenção **45,1%** (n=72)  / 23 inscritos / 18.693 views / **1,23 por mil**
    longos  retenção **20,9%** (n=103) / 17 inscritos /  2.733 views / **6,22 por mil**
Por canal e formato (691): epomeno longo **1,25 inscrito/peça**, kolejny short
1,00, epomeno short 0,45, labtreinamento short 0,29, kolejny longo 0,12,
labtreinamento longo 0,00. **O longo converte ~5x melhor POR VIEW, e isso é do
EPOMENO** — não da frota. Amostra pequena, uma coleta só: melhor dado disponível,
não conclusão.

RETRATAÇÕES QUE FICAM: `viewCount` de `channels.list` não conta Shorts (638); não
existe teto de 1.150 (646); o "+392 → 525" estava inflado (650); o estoque não é a
restrição do ritmo (655); a quarta peça do dia recebe distribuição (657); o zero
de uma peça não é posição no dia (663); "21 entregues" era 20 vivas mais 3 mortas
(666); o labtreinamento NÃO converte melhor (668); "o CRM alheio desperdiça 1.303
minutos de Actions" era falso — o repositório é PÚBLICO e Actions é grátis nele;
"o tratamento novo abriu um buraco de fator 30 no labtreinamento" era comparador
escolhido a dedo (684); "nove leituras iguais de inscritos" não eram nove
observações (686); "a mediana de três leituras é o número bom" — ela é a réplica
atrasada (688); **"o dono não autorizou `yt-analytics.readonly`" era FALSO — o
escopo foi perdido pelo nosso próprio `ESCOPOS` (689)**; **"o longo deixou de ser
alavanca" era falso por view, e o "5x melhor" é do epomeno e não da frota (691)**;
**"matar os fades é o próximo item" — desceu na fila por medição (700)**;
**"a fresca vem na terceira leitura" — a ordem não tem regra (707/708)**;
e **a confiança que eu dei a várias leituras de 09/10, retirada retroativamente
pela conta de poder do 693.**

=====================================================================
2. AS DUAS ALAVANCAS
=====================================================================
**A RESTRIÇÃO REAL É PAUTA, não cota nem aprovação.** Medido em 09/10: **10
origens livres** contra ~14 peças publicadas no dia — **menos de um dia de
pauta**. E origem só nasce de LONGO novo. Isso converge com o 689/691: o longo
converte melhor por view, **gera pauta** e satisfaz os 3 uploads públicos/90 dias
da Porta 1. **Logo pacote completo deixa de ser exceção e passa a ser a produção
principal quando a pauta estiver baixa** — e a autorização do dono já cobre isso.

**POR QUE NÃO AUMENTAR O NÚMERO DE CANAIS**, mesmo com o dono dando liberdade: os
**500 inscritos são limite POR CANAL**. Dividir ~2.100 views/dia em mais canais
afasta cada um do limite em vez de aproximar. Ele mesmo cortou de 13 para 3 em
07/10. **Reabrir canal só faz sentido depois de UM canal passar a Porta 1.**

**(I) CONVERSÃO EM INSCRITO. EXPERIMENTO 37, ABERTO:** o CTA do short gastava o
único pedido apontando para o LONGO (493) e nunca pedia inscrição. Agora o kicker
do CTA pede a inscrição e a DESCRIÇÃO mantém o caminho do longo. Primeira peça:
`epomeno-epipedo-s011`. **Indecidível pelo contador de canal (686) e pela
variância (693): só retenção/`subscribersGained` por vídeo o resolve.**
**NÃO adicione peça só para "dar mais chance ao 37".**

**(II) ALCANCE POR SHORT, pela CONCLUSÃO.** Lote semeado de 200 a 500 impressões;
sai dali se o abandono nos TRÊS PRIMEIROS SEGUNDOS for baixo. **O LOTE É VISÍVEL
NO CONTADOR** (653). TAMANHO NÃO COMPRA DISTRIBUIÇÃO.

**EXPERIMENTO 38, ABERTO, SEM VEREDITO** (669): a mira de "35 a 37 estimados" era
HÁBITO MEU, não limite do portão. `prontidao` sempre permitiu **43,14**.
**Mire `ALVO_SHORT` de `fabrica/ensaio.py`: 41,5 a 43,0 estimados — EXCETO no
canal que tem override em `ALVO_POR_CANAL` (hoje o labtreinamento, ver §6).**
**NÃO mexa em `ALVO_SHORT`** antes da leitura de 12 h.
**DADO CONTRA o 38, e vai dito:** o `chart=mostPopular` (categoria 26, PROXY, 610)
lido em 09/10 diz que o que tem milhões de views dura **10 a 35 s** — mediana 26 s
no BR, 35 no PL, 30 no GR. Os nossos estão em 41-42 s porque EU os empurrei.
**RESSALVA QUE NÃO PODE CAIR: short mais longo não retém igual.**

**EXPERIMENTO 33 (motion) FOI ABORTADO em 09/10.** A própria hipótese dele
declarava "não mede o que quer medir", e ele travou três testes por dez dias
enquanto o defeito que deveria medir ficava no ar. **A FILA ESTÁ DESTRAVADA: a
linha "NÃO abra nenhum antes do 33 fechar" CAIU.** Pode ser reaberto com retenção
de verdade quando o escopo voltar.
**ABERTOS AGORA: 37, 38, 39 (esqueleto do short) e 40 (dez a onze cenas).**
Ainda na fila, não iniciados: short de 22 a 26 s; `broll` na cena 1; **matar os
fades entre cenas — DESCEU NA FILA** (700, medido, e retrata a minha estimativa
de "~2,2 s de escurecimento"): na peça de dez cenas (1.255 quadros, 30 fps) são
**nove** quadros de preto puro, **0,30 s** (0,72%), e 45 quadros abaixo de 75% da
mediana, **1,50 s** (3,6%). **A primeira emenda cai em 4,77 s — FORA dos três
segundos que decidem**, porque o preto de t=0 da cena zero já foi consertado.
**Na frente dele: PAUTA (longo novo) e o que acontece DENTRO dos três primeiros
segundos.**

**O DINAMISMO VISUAL — defeito medido e consertado em 09/10.** O dono disse que os
frames pareciam estáticos e **ele estava certo com folga**: no
`labtreinamento-s011`, diferença **mediana** entre quadros consecutivos de
**0,39** em 0-255, e **375 de 414 quadros (91%) abaixo de 1,0**. A física diz onde
está a alavanca: `movimento por quadro = amplitude / (duração da cena x fps)`;
12% de zoom em 8,3 s dá 0,048% por quadro, e aumentar a amplitude corta a borda do
texto antes de ficar perceptível. **A alavanca é a DURAÇÃO DA CENA.**
Consertado como DEFEITO, não experimento: `fabrica/legenda.py` (a legenda queimada
era UMA fala para a cena inteira, ~18 palavras paradas por oito segundos; agora
são grupos de até QUATRO palavras com tempo proporcional aos caracteres) e
`motion.filtro_bordas(dur, primeira=True)` (a cena ZERO tinha preto de t=0 a
t=0,067, dentro do primeiro segundo).
**A CORREÇÃO FUNCIONOU — medida no mesmo método** (699): com
`fps=10, tblend=all_mode=difference, signalstats` (o método do 690, escala
ABSOLUTA 0-255), `labtreinamento-s011` (5 cenas, legenda de uma fala) mediana
**0,39** e congelados (<1,0) **91%**; `kolejny-poziom-s017` (10 cenas, legenda em
pedaços) mediana **0,63** e congelados **73%**. Mediana +62%. Confundidor
declarado: canais e vozes diferentes, n=1 contra n=1, duas mudanças juntas — vale
mesmo assim porque a escala é absoluta e o efeito é no quadro, não em view.
**CUIDADO COM A MÉTRICA:** YAVG sobre o quadro inteiro é INSENSÍVEL a legenda (o
texto é ~3% dos pixels) e me fez ler "92% congelado" antes e depois. **E NÃO use
`mpdecimate` sem fixar `hi/lo/frac`:** na mesma peça ele devolveu "1.254 de 1.255
quadros distintos", incomparável com o "3 -> 8 de 273" que eu medi de manhã. **O
instrumento é `tblend` + `signalstats`.**

=====================================================================
3. CORREÇÃO DO MODELO A CADA RODADA — PEDIDO DO DONO, OBRIGATÓRIO
=====================================================================
 1. **MEDIR, COLETANDO PRIMEIRO.** Token por `pg_net` (`Content-Type:
    application/json` EXATO; o body vai como `jsonb_build_object`). **O PAR
    client_id/client_secret É DA PRÓPRIA LINHA `yt_token_<canal>` de `config`,
    NUNCA o de `yt_oauth_client`** (667): com o global o token endpoint devolve
    `401 unauthorized_client` e a chamada seguinte `403 unregistered callers` —
    que se parece com token revogado e NÃO É.
    Depois `videos?part=statistics,status,contentDetails&id=<até 50>`, **TRÊS
    leituras na mesma rodada, e o estimador é o MÁXIMO como PISO, com a faixa ao
    lado** (688).
    **GRAVE A CHAMADA CERTA (707/708, `alto`, medido):** `grava_metricas_janela`
    grava a réplica DAQUELA chamada, não o máximo — gravar a errada SUBESTIMA PARA
    SEMPRE. E a réplica atrasada é da **CHAMADA inteira, não de cada id**: às
    08:08 de 10/10 quatro peças divergiram com a MESMA forma {alto, baixo, alto}
    e as outras dezesseis vieram idênticas. **Procedimento: compare a SOMA das
    três chamadas, escolha a de soma máxima e chame `grava_metricas_janela(<req>)`
    nessa UMA.** Não cace o máximo peça por peça.
    **UM STATEMENT POR CHAMADA** (702): dois `grava_metricas_janela` no mesmo
    statement colidem em `metricas_youtube_id_coletado_em_key`, porque o `now()`
    não avança dentro do statement.
    **A ordem das réplicas NÃO tem regra** (a fresca já foi a 3ª, a 2ª, a 1ª e a
    3ª): não leia nada na ORDEM. **Nada se conclui abaixo de 6 h.**
    **O access token NÃO precisa sair do Postgres:** a chamada à API pode ir pelo
    próprio `pg_net` com `'Bearer ' || (content::jsonb)->>'access_token'`, e é
    assim que se lê a descrição de um longo publicado quando a origem não tem
    spec local.
 2. **VIGIE O PROCESSAMENTO, NÃO SÓ O TETO** (665, `critico`): `status_code` de
    cada chamada. **`uploadStatus` fora de `processed` ou `duration: P0D` depois
    de 2 h é FALHA DE PROCESSAMENTO, não indexação** — a peça conta como NÃO
    PUBLICADA e vai NOMEADA com id e idade.
 3. ORDENAR pelo PISO, por FAIXA DE IDADE (632), nunca por views/hora.
 4. **ACHAR O PAR** — melhor e pior, e uma pergunta: o que têm de diferente que eu
    POSSO mudar? "Assunto" e "canal" são respostas erradas. **Confirme que as DUAS
    passaram das 6 h, que o comparador é a MEDIANA DO GRUPO (684), e que a
    diferença é maior que a FAIXA do grupo (693).**
 5. **MUDAR UMA COISA SÓ**, com o número de partida escrito. Consertar o
    INSTRUMENTO conta. **Se o número VIVO do dia está entregue, a rodada vira
    engenharia.** **E "não mudar nada" é uma decisão legítima quando o braço
    precisa de n** (693) — escreva isso no docstring em vez de inventar mudança.
 6. SE O DADO CONTRARIAR ESTA ROTINA, CORRIJA-A com `update_trigger` e diga ao
    dono — **e atualize `docs/ROTINA.md` no mesmo passo.** Já aconteceu TRINTA E
    TRÊS vezes. **E não adie: eu adiei esta correção três rodadas e o prompt
    ficou mandando travar experimentos já abertos.**
    **Confira esta rotina contra o `CLAUDE.md` a cada rodada: em 10/10 ela estava
    atrás dele em cinco pontos (700, 699, 702/707/708, 698/701, 706).**
 7. SE UMA MUDANÇA NÃO MOVER O NÚMERO EM TRÊS PACOTES, DESFAÇA — **a menos que o
    instrumento não consiga medir o número, e aí o que se desfaz é o instrumento,
    não a mudança** (686). **E com CV 0,66, três pacotes NÃO medem nada menor que
    o dobro (693): não desfaça por n=3.**
 8. **ANTES DE CHAMAR UM ACHADO DE ACHADO, PERGUNTE SE O INSTRUMENTO PODE
    PRODUZI-LO.** Janela curta fabrica morte e saturação; views/hora fabrica "o
    novo é melhor"; portão verde fabrica "está tudo certo"; o máximo de série que
    oscila fabrica recorde; enumerar pelos pacotes recentes fabrica "estoque
    zero"; ordenar por alcance do short original fabrica "melhor origem livre";
    ler em idade fixa fabrica "não recebeu distribuição"; agregado de três
    chamadas fabrica "134/134 vivos" quando uma deu 401; coincidência temporal com
    a sua própria correção fabrica "a correção funcionou"; número absoluto sem
    denominador fabrica o canal errado; a MELHOR peça de um grupo como linha de
    base fabrica "o tratamento quebrou o canal"; N leituras horárias de um
    contador em degrau fabricam "N observações iguais"; a MEDIANA de três leituras
    fabrica "a peça está em zero"; **n pequeno sob CV 0,66 fabrica "o tratamento
    funcionou" a partir de UMA peça boa**; **YAVG do quadro inteiro fabrica "a
    correção de legenda não fez nada"**; **`mpdecimate` sem limiar fixo fabrica
    "1.254 de 1.255 quadros distintos"**; **gravar a chamada errada fabrica um
    piso que subestima para sempre**; **a madrugada fabrica "parou"**; e **"o
    dono não autorizou" fabrica pendência alheia onde o defeito era do nosso
    código.**
    **VINTE E SETE dos meus erros têm essa assinatura** — um DENTRO da correção
    de outro, e um dentro de uma regra que eu acabara de escrever aqui.

=====================================================================
4. RITMO E PAUTA
=====================================================================
Short solto: spec com `longo: []`, `etapas.py` marca `SO_SHORT`. ~1.600 de cota
contra ~2.100 do pacote. O limite é **PAUTA** antes de ser cota.

**ESCOLHA DE ORIGEM, em ordem:**
  a) **rode `consultas/estoque.sql`** — nunca lista de memória, nunca lista à mão,
     **e nunca o número que estiver escrito aqui**: ele envelhece a cada publicação;
  b) PRIMEIRO ÂNGULO de longo virgem;
  c) **PERFIL (651)**: longo cujo número é do PRÓPRIO espectador, com papel na
     mão. Dinheiro próprio 1.133 e 1.111; conformidade corporativa 4 a 70.
     Confundidor declarado: os de conformidade são os mais antigos.
     **E LEIA O PERFIL PELO DONO DO NÚMERO, NÃO PELO ASSUNTO** — uma PLANILHA que
     o espectador preenche É papel na mão mesmo com assunto de conformidade;
  d) **NÃO ordene pelo alcance do short original** (658);
  e) a entrada errada vem do capítulo que o short ORIGINAL não usou, e é ARITMÉTICA;
  f) **não repita a mesma FAMÍLIA de entrada errada no mesmo canal no mesmo dia**
     (limiar, composição, ordem, unidade... são famílias distintas);
  g) **número que MUDA (taxa, índice, alíquota, limite anual, data de vigência)
     fica FORA do short** — o short carrega a REGRA, que não envelhece, e o
     descarte vai ESCRITO no AVISO. **Caso especial: número que o próprio longo
     diz ser ESCOLHA e não norma não entra de jeito nenhum.**
  h) **ORIGEM LIVRE PODE NÃO TER SPEC LOCAL** (medido em 09/10 com `Xgt32iH8Ft8`,
     pacote de 11/08, anterior à convenção de nome atual): nem por nome de arquivo
     nem por varredura de conteúdo. **Leia os capítulos da DESCRIÇÃO PUBLICADA
     pela `videos.list`** — isso não é motivo para trocar de origem.
**AO PUBLICAR, GRAVE `videos.origem_id`** com o `longo_existente` da spec (670).

IDS: labtreinamento `UCtv_ewwSmwdi1ZRALW4_azg`, epomeno `UC1hk4k4QMjbPCfbw-S5xDyQ`,
kolejny `UCGe6sYpjzKyCC_K22ae1anw`. **`videos` não tem coluna `id`** — é `slug`.
**Diga o número REAL, nunca o pedido.**

=====================================================================
5. TENDÊNCIA E LIÇÕES DO CANAL
=====================================================================
NÃO use busca na web para tendência: devolve blog de SEO — remedido em 09/10,
voltou blog de fornecedor de ferramenta de legenda, sem teste controlado e com
números que se contradizem. Use `pg_net`:
`videos?part=snippet&chart=mostPopular&regionCode=<BR|GR|PL>&videoCategoryId=26
&maxResults=15`. **SEMPRE 26 e DIGA QUE É PROXY** (610). Confira `content->'error'`
antes de confiar em lista vazia. **COPIE A FORMA, NUNCA O ASSUNTO.** O chart repete
14 de 15 em quatro horas e meia (623). **Se não leu o feed, DIGA que não leu.**
**A FORMA DO TÍTULO É POR CANAL, NÃO DA FROTA** (09/10): pergunta pura é sinal
**POLONÊS** (seis de quinze); BR e GR ficam em dois a três. O BR premia **endereço
direto com a consequência surpreendente**; o GR, **imperativo de segunda pessoa**.
**Limite de forma que sobreviveu à busca ruim, porque é coerente com a medição:
quatro a cinco palavras de legenda na tela por vez.**
PESQUISA DE MÉTODO é outra coisa e o dono pediu: limiar de retenção, mecânica de
distribuição, requisito de YPP — web e GitHub servem. Traga número e fonte.

`select * from v_maquina_licoes where canal='<canal>'` — OBEDEÇA.
Três frases no docstring: o que deu certo, o que não deu, o que vou mudar.
Similaridade <= 0,65 contra o MESMO canal. A pauta serve o SHORT primeiro.
Nunca titule short com sigla de órgão ou cifra oficial (609).

FONTES — duas institucionais que batam (600). BR `planalto.gov.br` abre por
`pg_net` com `User-Agent` de navegador; PL API ELI do Sejm; GR ELSTAT + Eurostat.
Número que não bate em duas fontes NÃO entra, e o descarte vai ESCRITO no AVISO.
**Short de longo já publicado não precisa de fonte nova** se não introduzir número
novo sobre o mundo — e isso vai dito, com o id do longo. Respeite `robots=noai` e
`tdm-reservation=1`.

=====================================================================
6. PRODUÇÃO
=====================================================================
- `frota.yml` com `publicar: false` SEMPRE.
- SHORT 9:16, **30 a 45 s**; o portão `duracao` recusa >43,1 s E <30 s.
- **USE `alvo_short(canal)` de `fabrica/ensaio.py`, NUNCA a constante.** Sem
  canal a função devolve a mira da FROTA, e isso tem de ser escolha, não descuido.
  **MIRE `ALVO_SHORT` (41,5 a 43,0 estimados)** (669) — **ou `ALVO_POR_CANAL`
  quando o canal tiver override** — mas **ONDE dentro da faixa depende da VOZ** (679):
    `pl-PL-MarekNeural`   centro **+2,2%** → **MIRE O PISO, 41,5.**
    `el-GR-NestorasNeural` centro **-3,2%** → o topo é seguro.
    `pt-BR-ThalitaMultilingualNeural` centro **-3,7%** → o topo é seguro.
  **A LARGURA é ~5 pontos em TODAS as vozes; o que muda é o CENTRO.** Não prometa
  precisão de décimo. **E SEPARE POR FORMATO antes de tirar o centro** (683).
  O YouTube **ARREDONDA A DURAÇÃO PARA CIMA**.
- **A MIRA É POR CANAL quando o canal mediu que a da frota o prejudica**
  (`ALVO_POR_CANAL` em `fabrica/ensaio.py`):
    **labtreinamento: 33,0 a 37,0** desde 09/10 (698). Com IDADE CASADA (views na
    janela de 9 a 21 h de vida) as duas peças de mira nova caíram ABAIXO do mínimo
    das oito antigas — 18 e 9 contra 20, 21, 34, 48, 60, 68, 173, 196; sob a nula
    ~1/9 cada, ~1% as duas.
    **kolejny: sinal OPOSTO** (701, `alto`, observado). Janela casada de 4 a 8 h:
    mira nova 209, 117, 115, 83 contra antiga 17, 13, 4, 0 — sem sobreposição,
    1/C(8,4) = 1,4% sob a nula. **CONFUNDIDOR QUE NÃO SAI DO RELATO:** as antigas
    são de 08/10 e as novas de 09/10; crescimento do canal entre os dias explica
    parte ou tudo, e isso NÃO é aleatorizado no tempo.
  **Não existe "a mira certa do short" — existe a de CADA CANAL**, e é assim que
  `ALVO_POR_CANAL` cresce. **O `ALVO_SHORT` global NÃO muda** — o 38 segue sem
  leitura e mexer no global apagaria o braço. **Compare peça com peça na MESMA
  FAIXA DE IDADE**, lendo a janela do próprio `metricas`; piso atual de peças de
  idades diferentes é o efeito (D) e viciou as minhas leituras do labtreinamento.
- **ESQUELETO DO SHORT SOLTO: DEZ A ONZE CENAS, mantendo a duração total**
  (experimento 40). **Onze é o TETO REAL e isso é medido:** há **~1,9 s fixos por
  cena** no `ensaio` (12 cenas de um caractere já somam 21,9 s), então doze cenas
  gastariam 22 s só em padding e estourariam o teto de 43,1. **Ponto de
  equilíbrio: 10 cenas de ~40 caracteres, ou 11 de ~34.** Eu escrevi "dez a
  CATORZE" nesta mesma rotina sem conferir a sobrecarga, e tive de corrigir na
  mesma manhã. O esqueleto novo quebra o `39 de 39` idêntico de propósito.
  **Experimento 40 ainda sem leitura:** na janela de 4 a 8 h do kolejny, dez cenas
  (83, 117, 209) contra cinco (115) — n=1 de um lado.
- **`prontidao.py <spec.json>`: DOZE portões, ONZE no short solto** (o `capitulos`
  sai de fora em vez de aprovar em silêncio), exit 2 se travar.
  **Passe o CAMINHO do .json, não o nome do pacote.**
- **O PORTÃO `variedade` É O DA MONETIZAÇÃO**, não da estética. Ver
  `fabrica/variedade.py` e `docs/mapa-canal-dark-o-que-entrou.md`:
    **REPROVA** gancho acima de **12 palavras** na PRIMEIRA FRASE da cena 1;
    **REPROVA** thumbnail acima de **4 palavras** somando `l1` e `l2`;
    **AVISA** quando o esqueleto do short repete no canal.
  Os limiares 12 e 4 vêm do mapa que o dono trouxe, não de mim — limiar sem
  procedência é critério inventado. **Com o esqueleto de dez a onze cenas o aviso
  para de aparecer.**
- TÍTULO PRÓPRIO do short, `## TITULO SHORT`, até 45 caracteres.
- **NÚMEROS POR EXTENSO — REGRA SEM PORTÃO** (640): o `narracao` conta QUANTIDADES
  por frase (máx. três), NÃO dígito cru. **Confira dígito à mão.**
- **O `ortografia` mede só a NARRAÇÃO** (597). Leia os campos de tela e a copy.
- **O ponto de interrogação grego é `;`** — um checador de `endswith('?')` rejeita
  título grego que É pergunta. Use `("?", ";", ";")`.
- `## CONFIGURACOES DO STUDIO` é DECLARATIVA; o código ignora o `categoryId` (610).
- **USE A FAIXA DE IDENTIDADE ATUAL, nunca a paleta do pacote de origem** (601).
- `visual.conferir` AMOSTRA n=12 e isso ESCONDE DEFEITO SISTEMÁTICO (648/649).
- Motion LIGADO no short. **Os soltos têm b-roll ZERO.** `get-brolls` exige
  aprovação de pessoa: NÃO use. `vox-motion-graphics` consome crédito: só se o
  dono pedir.
- **ESTE CONTAINER TEM `pytest`, `httpx`, `ffmpeg`, `imageio-ffmpeg` e `pypdf`.**
  **Linha de base da suíte em 09/10: 25 falham, 2.048 passam, 436 skip** (as 25
  são specs já publicadas que o `prontidao` recusa por título duplicado e fonte
  Devanagari ausente — as duas são o portão funcionando). **Falha nova é sua.**
  **Ele NÃO sintetiza voz: `speech.platform.bing.com` leva 403 no CONNECT** —
  render continua no runner.
- **NUNCA rode duas tarefas que mexem na mesma árvore de trabalho ao mesmo
  tempo:** um `git stash -q -u` de um teste apagou arquivos novos de baixo da
  outra rodada em 09/10. Recuperado com `git stash pop`, mas foi erro meu.
- **A NARRAÇÃO TEM FORNECEDOR ÚNICO** e isso é um buraco conhecido:
  `edge_tts.Communicate` em `fabrica.py:598`. Não instale costura de plano B sem
  um segundo provedor de verdade — costura vazia só adiciona risco.

=====================================================================
7. ENTREGA — A PONTE
=====================================================================
O REST do Supabase devolve **402** desde 25/08 (cota da organização; o projeto
está `ACTIVE_HEALTHY`, não é pausa). **Render no runner com `publicar=false`,
publicação pela ponte.** Passo a passo em `docs/publicar-pela-sandbox.md`.
**A PONTE MORRE NO DIA EM QUE OS TRÊS SECRETS ENTRAREM** (pendência 1):
`publicar.token_do_canal` já lê `YT_TOKEN_<CANAL>` do ENV antes do REST, recusa
token que nomeia outro canal (a trava do erro de 14/08) e o `frota.yml` já passa
os três nos dois passos.
  * o input do `urlartefato.yml` chama **`artefatos`**, não `ids` (422 se errar).
  * o `gh` recusa redirecionamento entre hosts: leia a URL assinada com
    `mcp__github__get_job_logs` e `return_content: true`.
  * a URL do artefato vive ~10 min e **ESTE CONTAINER NÃO A BAIXA** (403 no
    CONNECT do Azure). Baixe pela sandbox do Composio, PREPARADA ANTES de pedir a
    URL. **O `sandbox_id_suffix` muda sem aviso**; se o clone sumiu, refaça em
    `/home/user/maq` e reconstrua `/home/user/pub/corpus.json` CONFERINDO o md5.
  * **O CORPUS SAI DO PRÓPRIO `fabrica/corpus_publicados.json` DO CLONE**, e aí
    não se transcreve título nenhum: basta conferir o md5 em ordem de byte contra
    o banco. Em 10/10 bateu de primeira, 238 títulos.
  * **o zip abre FLAT** (`short.mp4`, `thumbnail.png`, `copy.md`) e o `conduz.py`
    espera `f/<pacote>/`. Descompacte JÁ dentro de `f/<pacote>/`, senão o erro que
    aparece é "copy ainda tem {TRILHA}" e parece falha de render.
  * **refaça o `corpus.json` DEPOIS do `git fetch`** do clone, não antes.
  * `nohup` no `conduz.py` (sandbox mata em 180 s, MCP corta em 60 s).
  * **O HTTP 410 no PUT do binário é CAMINHO NORMAL** (654): "0 publicados, 1
    falharam" e o vídeo ESTÁ no ar. **Pergunte ao canal ANTES de retentar.**
  * **CONFIRA `tags` NO VÍDEO depois de publicar** (662). **Tag nula ANTES de
    2 min não decide nada** (672): é corrida de indexação. Nula DEPOIS de 2 min,
    ou OITO tags, é falha — refaça por `pg_net` um PUT de `part=snippet` com o
    snippet INTEIRO.
  * registro: linha em `videos` **com `origem_id`**; corpus contra o banco com
    **DISTINCT**; ao regravar `fabrica/corpus_publicados.json` use **`indent=2`**.
    **Para conferir o md5 ordene em BYTE nos dois lados:**
    `string_agg(titulo, E'\n' order by titulo collate "C")`.
  * as travas anti-duplicata rodam IGUAIS na ponte e PEGAM (641).
  * **cuidado com crase em mensagem de commit pelo heredoc do bash**: uma palavra
    entre crases vira substituição de comando e sai do texto, silenciosamente.
    Já aconteceu, e em 09/10 apagou quatro palavras de uma mensagem. Escreva a
    mensagem num ARQUIVO e use `-F`.
  * **JSON despejado dentro de um `.build.py` sai com `true`/`false`/`null`
    minúsculos e dá `NameError`.** Converta para `True`/`False`/`None`.
  * **A CREDENCIAL DO GITHUB É DA SESSÃO E NÃO SE ATUALIZA SOZINHA** (10/10):
    uma sessão nasceu autenticada numa conta SEM `push` e ficou **vinte horas em
    403** enquanto eu repetia "reconecte o GitHub" — que não era o conserto.
    **Antes de insistir num 403, leia QUEM você é:** `gh api user` e
    `gh api repos/<owner>/<repo>` (campo `permissions`). Reconectar no claude.ai
    **NÃO entra numa sessão já rodando**; isso pede sessão nova. E "conectado"
    não é o mesmo que "conectado com a conta que pode escrever". O mesmo vale
    para o `mcp__github__*`: `invalid session` depois de a credencial trocar só
    morre com sessão nova, e sem ele a URL assinada fica ilegível e a ponte PARA.
  * **O classificador do modo automático recusa colar token em linha de comando
    do shell** ("Credential Materialization"). Faça a chamada pelo `pg_net`, onde
    o segredo não sai do Postgres — é mais seguro e funciona.

=====================================================================
8. TRAVAS QUE NÃO SE NEGOCIAM
=====================================================================
- NUNCA publique pela Composio YOUTUBE_UPLOAD_VIDEO (6/6 apagados).
- NUNCA criar novos triggers.
- **NÃO APAGUE VÍDEO PUBLICADO SEM O DONO DIZER.** É irreversível, e a
  autorização de 09/10 NÃO cobre isso.
- **O ARQUIVO DOS VÍDEOS É O GOOGLE DRIVE, NÃO O BANCO.**
- Não mande x-upsert; não use `upload_local_file` do workbench.
- NÃO passe token OAuth por input de workflow.
- NUNCA imprima refresh token. O access token sai do `pg_net`, e o refresh token
  não precisa sair do Postgres.
- `privacyStatus=public` sempre; idiomas no idioma real do canal.
- UMA consulta por chamada quando o resultado decide algo.
- **CONFIRA NO VÍDEO PUBLICADO, não no código.** `videos.list` omite tags enquanto
  indexa; `processingDetails` dá 403 em token de outro canal. **E `P0D` só é
  indexação nos primeiros minutos — depois de 2 h é defeito (665).**
- COTA ~40 vídeos/janela (619). 403 `quota` na legenda → SEGURE o pacote.
  403 `reason=forbidden location=id` → NÃO retente (622).
- **O AUTO-DISPARO DO `frota.yml` ESTÁ EXPLICADO:** é
  `.github/workflows/diario.yml`, cron `*/30 * * * *`. Ele guarda contra run em
  voo e só manda `publicar=true` quando a porta do Supabase está ABERTA — e ela
  está FECHADA, então hoje dispara com `publicar=false`. **NÃO MEXA sem o dono**,
  mas pare de reportar como desconhecido.
- O EXPURGO DO BUCKET NÃO RESOLVE O 402. O proxy recusa `.go.id` e
  `planalto.gov.br` no CONNECT: use `pg_net`.

=====================================================================
9. REGISTRO
=====================================================================
`videos` + `canais.ultimo_pacote_em` + `metricas` via `grava_metricas_janela`
(**na chamada de soma máxima, um statement por chamada — §3.1**).
Esquema em `docs/schema-supabase.md`. O que mais me fez errar: `aprendizados`
exige `categoria` (distribuicao, entrega, pauta, processo, producao, render,
roteiro), `titulo`, `regra`, `evidencia` (jsonb) e `severidade` (**critico, alto,
medio, baixo** — não "media"), NÃO tem `texto` nem `canal`, e a força é
`confianca` (**medido, observado, hipotese**); `experimentos` tem `variavel`,
`hipotese`, `valor`, `metrica_alvo`, `status` (**aberto, concluido, abortado** — e
só isso; `pre-registrado` é RECUSADO pela constraint), e NÃO tem `nome` nem
`notas`.
`videos.fonte_pauta_vd` é NUMÉRICO (é um escore, não um id) — a origem do short
vai em `origem_id`.
Retratar = `status='invalidado'` + `invalidado_motivo` + registro NOVO. Retratação
PARCIAL (o número certo, a leitura errada) também vai em `invalidado_motivo`.
**AS SEQUÊNCIAS DE `id` ESTÃO ATRÁS DO `max(id)` nas duas tabelas** — se o insert
der `duplicate key`, rode
`select setval(pg_get_serial_sequence('<tabela>','id'), (select max(id) from <tabela>))`
e repita. **UPDATE por este MCP estoura o timeout de 60 s de forma INTERMITENTE**
(621) — um statement curto por chamada, e CONFIRA.

**Não se limite ao que está escrito.** Esta rotina já foi corrigida por medição
TRINTA E TRÊS vezes. Caíram, entre outras: "view de short é rajada que morre"; "os
500 fecham em 33 dias"; "existe um teto de 1.150"; "views nunca caem"; "o estoque
é a restrição do ritmo"; "a quarta peça do dia não recebe distribuição"; "P0D é só
indexação"; "o labtreinamento converte melhor"; "a mira do short é 35 a 37" — era
hábito meu e custava 19% de watch time por peça; "o resíduo cresce com a narração"
— é a VOZ; "cinco de quinze em pergunta no BR" — a pergunta é polonesa; "o
tratamento novo quebrou o labtreinamento" — o comparador era a melhor peça; "nove
leituras iguais de inscritos" — o contador de canal anda em degrau; "a mediana de
três leituras é o número bom" — é a réplica atrasada; **"o dono não autorizou o
escopo de analytics" — nós o perdemos no nosso próprio código (689)**; **"o longo
deixou de ser alavanca" — ele converte melhor por view e é ele que gera pauta
(691)**; **"pacote completo exige janela dedicada do dono" — a aprovação foi
dada**; **"dez a catorze cenas" — o teto real é onze, por ~1,9 s fixos por cena**;
**"matar os fades é o próximo item" — 0,30 s de preto, tudo depois dos três
segundos (700)**; **"conte quadros com `mpdecimate`" — sem limiar fixo ele não é
instrumento (699)**; **"a fresca vem na terceira" e "grave o máximo" — a réplica é
da chamada e se grava a de soma máxima (707/708)**; **"a madrugada mostra se o
tratamento pegou" — ela é cega por construção (706)**; e **"uma mira de short para
a frota" — a mira é por canal (698/701).**
**Se você errou, retrate no mesmo lugar onde afirmou.**
**DESCONFIE DE PORTÃO QUE PASSA EM SILÊNCIO, DE MEDIÇÃO QUE NÃO GRAVA, DE AMOSTRA
ESPARSA, DE LEITURA ÚNICA, DE TRÊS LEITURAS QUE SUBIRAM JUNTAS, DE LISTA DE
MEMÓRIA, DE LISTA ESCRITA À MÃO, DE LISTA DENTRO DESTE PROMPT, DE NÚMERO SEM
DENOMINADOR, DE LEITURA EM IDADE FIXA, DE LEITURA DE MADRUGADA, DE AGREGADO SEM
`status_code`, DE COMPARADOR QUE VOCÊ ESCOLHEU, DE CRITÉRIO QUE VOCÊ MESMO
INVENTOU, DE n PEQUENO SOB CV ALTO, DE MÉTRICA QUE MEDIA 3% DOS PIXELS, DA
CHAMADA QUE VOCÊ GRAVOU SEM COMPARAR AS SOMAS, DE COINCIDÊNCIA COM A SUA PRÓPRIA
CORREÇÃO, E DA SUA PRÓPRIA CORREÇÃO.**

PENDÊNCIAS QUE SÓ O DONO RESOLVE:
1. **O ESCOPO DE ANALYTICS — PRÉ-CONDIÇÃO, e agora são DOIS cliques dele, não uma
   negativa minha.** `yt-analytics.readonly` JÁ está em `ESCOPOS`; falta ele abrir
   os dois links de `docs/reautorizar-analytics.md` (um por cliente OAuth,
   escolhendo a conta de marca de cada canal) e devolver as três URLs com
   `?code=...`. **Sem retenção, os experimentos 37, 38 e 40 são indecidíveis
   (693), porque views por peça é cego abaixo do dobro.** É a pendência que mais
   importa, e são agora QUATRO argumentos independentes para ela.
2. **Colar os três secrets no GitHub** — `YT_TOKEN_LABTREINAMENTO`,
   `YT_TOKEN_EPOMENO_EPIPEDO`, `YT_TOKEN_KOLEJNY_POZIOM`. Com eles a frota publica
   sozinha e a ponte morre. **A API de secrets é bloqueada para mim** (403 em
   `actions/secrets/public-key`) — eu não consigo fazer isso.
3. **As peças mortas** em `uploaded`/`P0D`: `Ta_KN8yXLaI` e `oHwlhhneIos`
   (epomeno) e `ylsKfJ5Kv4s` (kolejny). Apagar e republicar, ou deixar.
   Irreversível, dele.
4. **Apagar as 46 duplicatas** (`docs/duplicatas-a-apagar.md`). Já NÃO contaminam
   a escolha de pauta (670). Sobra o teto de upload.
5. Supabase Pro — tira o 402 e devolve o Drive como arquivo.
6. `youtube.com/verify` nos 5 canais — destrava a capa desenhada.
7. `ANTHROPIC_API_KEY` para o `autoria.yml` — e para o prompt 6 do mapa, a
   revisão anti-molde, que ataca o mesmo risco do experimento 39.
8. Plugins que exigem sessão INTERATIVA dele: `oh-my-claudecode`, Chrome DevTools
   MCP, Vercel (OAuth). O Supabase JÁ está ligado como MCP.
9. **Liberar `speech.platform.bing.com` na política de rede do ambiente** (Network
   access → Allowed domains, deixando "Allow package managers" marcado). Hoje o
   CONNECT leva 403 e por isso este container não sintetiza voz nem renderiza. É o
   que tornaria a rodada local, e é também o plano B da narração que a §6 pede.
DÍVIDA TÉCNICA: **25 testes falham** — specs já publicadas que o `prontidao`
recusa por título duplicado e fonte Devanagari ausente, as duas o portão
funcionando. `APRENDIZADOS.md` está desatualizado contra o banco.

RESPOSTA FINAL (curta e objetiva, o dono pediu):
quantos pacotes e shorts a rodada entregou DE VERDADE — **e se foi zero, por quê**
→ canal → título → duração real → link → **o que mudou no modelo e o número de
partida** → o feed de tendência, ou que não foi lido → **vigilância: vivos,
públicos, e PEÇAS FORA DE `processed` NOMEADAS com id e idade** → **inscritos ao
vivo COM views do canal (a razão por mil), só se a última leitura tiver >= ~4 h**
e distância em DIAS para os 500 → o que muda na próxima rodada.
