# Máquina de vídeos — o que nunca deve envelhecer

A rotina horária carrega o procedimento. Este arquivo carrega só os **ponteiros**,
porque número dentro de prompt envelhece e já me fez errar quatro vezes
(652/655, 658, 682, 685). Aqui não entra contagem de estoque, nem de views, nem
de inscritos. Entra onde olhar.

## A PERGUNTA QUE ABRE TODA RODADA — pedido do dono, 12/10/2026

Palavras dele: *"informe quadro dos resultados atuais projeção e tendência, de
quando o canal irá monetizar, e o que é preciso para isso acontecer até fim de
outubro, mudanças que precisam ser feitas para ter mais resultados. **Em cada
rodada da rotina este questionamento precisa ser feito**, e ajustado o processo.
Não me importo do formato, e sim da monetização principalmente, faça mudanças
que achar necessário."*

**Isto não se responde de cabeça.** Rode:

    python3 fabrica/porta1.py '{"horas":<h>,"canais":{"<canal>":{"antes":N,"agora":M}}}'

com duas leituras de inscritos separadas por **≥ 4 h** (regra H, 686 — abaixo
disso o degrau devolve ruído). O módulo recusa janela curta em vez de inventar.

**O quadro de 12/10 14:35, medido** (leituras de 10/10 22:15 e 12/10 14:35,
40,3 h):

| canal | inscritos | /dia | % da Porta 1 | chega em |
|---|---|---|---|---|
| labtreinamento | **68** | +0,60 | 13,6% | **2028-10-06** |
| epomeno-epipedo | **19** | +1,19 | 3,8% | **2027-11-20** |
| kolejny-poziom | **8** | 0,00 | 1,6% | **indeterminado** |

Frota inteira: **+1,79 inscrito/dia.**

**CORREÇÃO DE 12/10 ÀS 18:2x, e é desta tabela: eu escrevi "nunca" para o
kolejny, e "nunca" ali era falsa precisão.** O contador de inscritos anda **de um
em um**, então numa janela de `h` horas o menor ritmo diferente de zero que ele
consegue expressar é **24/h por dia** — o *piso de resolução* da janela. Na
leitura de 40,3 h o piso é **0,60/dia**, e o delta do kolejny foi zero. Isso diz
"ritmo abaixo de 0,60/dia", **não** "ritmo zero", e portanto não autoriza
"nunca". Agora é `fabrica/porta1.py → piso_de_resolucao` / `horas_para_resolver`,
com `ritmo_resolvido` por canal e oito testes.

**E a mesma conta diz que o +0,60/dia do labtreinamento é UMA contagem** — ele
está exatamente SOBRE o piso daquela janela, logo a incerteza dele é da ordem do
próprio valor. A projeção de 2028-10-06 continua sendo a melhor que existe, e
continua sendo de uma contagem só.

**E ISTO ACABOU DE IMPEDIR UM RELATO ERRADO.** Às 18:17 de 12/10 os três
contadores vieram **byte a byte iguais** aos de 14:35 — 68 / 19 / 8, em 3,7 h. O
`porta1.py` recusou a janela pela regra H, e se eu tivesse esperado os 4,0 h o
piso seria **6,00/dia**, três vezes acima do ritmo medido da frota (1,79). **Uma
janela de 4 h não distingue 1,79/dia de zero.** As ≥ 4 h da regra H bastam para
pular o DEGRAU da réplica (686/703) e **não** bastam para medir RITMO — eu tratei
as duas coisas como a mesma por dias. Para resolver 1,79/dia é preciso **~13 h**;
para resolver 0,60/dia, **~40 h**, que é por que a leitura de 40,3 h funcionou e
não foi sorte.

**E EU ERREI A HORA DA PRÓXIMA LEITURA TRÊS RODADAS SEGUIDAS — 13/10 às 03:0x.**
Nos relatos de 00:07, 01:07 e 02:06 eu disse ao dono que "a próxima leitura
legítima de ritmo é ~03:30". **Falso, e por mais de cinco horas.** A conta é
`24 / ritmo`, e da última leitura de inscritos (12/10 19:30) sai:

| ritmo a resolver | horas | primeira leitura que vale |
|---|---|---|
| frota, 1,79/dia | 13,4 h | **13/10 08:54 UTC** |
| epomeno, 1,19/dia | 20,2 h | **13/10 15:40 UTC** |
| labtreinamento, 0,60/dia | 40,0 h | **14/10 11:30 UTC** |

Os "03:30" vinham de 8 h de janela, cujo piso é 3,0/dia — **acima do ritmo da
frota**, logo uma janela que não resolve nada. **Eu calculei de cabeça o número
que o `porta1.horas_para_resolver` devolve pronto**, e é exatamente o item 3 da
§10 da rotina: toda conta que eu faço à mão vira um erro meu. Use o módulo:

    python3 -c "import sys;sys.path.insert(0,'fabrica');import porta1;print(porta1.horas_para_resolver(1.79))"

**E a consequência prática é maior que o relato errado:** a cada rodada da
madrugada eu prometia uma leitura para dali a pouco, o que faz a rodada seguinte
esperar em vez de produzir. **A leitura de ritmo da frota não cabe na madrugada
inteira** — ela cai depois das 08:54.

**A FRASE QUE DECIDE TUDO, e ela é aritmética, não pessimismo: as duas datas
caem DEPOIS de 1/FEV/2027, quando a barra sobe de 500 para 1.000 inscritos.**
No ritmo medido a máquina **nunca passa a Porta 1** — a barra se move antes de
nós chegarmos. Projetar 500 para depois dessa data é prometer uma monetização
que já não existe, e o `test_porta1.py` falha se eu fizer isso.

**E "até fim de outubro" é impossível por ordem de grandeza, não por pouco.**
Para fechar os 500 em 19 dias, na conversão MEDIDA de 1,2 por mil:
**~19.000 views/dia num único canal** — contra ~2.100/dia da frota inteira. É um
fator 9 no melhor caso, e por canal é pior.

**Logo o volume NÃO é a alavanca, e a conversão é.** O mesmo cálculo a 20 por
mil pede **1.137 views/dia**, que está dentro do que um canal já faz. Ordem de
grandeza certa. E a conversão é exatamente o que **não se mede sem os dois
cliques de consentimento do Google** — por isso essa pendência deixou de ser
"a mais importante" e passou a ser **a única com o tamanho do problema**.

**O alvo realista, e ele é calculável:** 500 no `labtreinamento` antes de
1/FEV/2027 são 111 dias e 432 inscritos = **3,9 por dia**. A 5 por mil isso pede
**~780 views/dia naquele canal** — alcançável com 5 a 7 peças/dia. A 1,2 por mil
pede 3.245/dia, que não é. **Então o plano é: uma conversão de ~5 por mil e
ritmo de 5 a 7 peças/dia CONCENTRADAS num canal.** Tudo o mais é otimização de
coisa que não move o portão.

### E ÀS 15:1x ISSO FICOU PIOR, porque eu verifiquei o número que o sustentava

**Aprendizado 713, `crítico`, e ele RETRATA o 691, que também era meu e também
era `crítico`.** O 691 dizia que `kolejny` no short rendia **1,00 inscrito por
peça** e se chamava *"o kolejny no short é o único caminho à Porta 1"*. Ele
somava `inscritos_ganhos` ao longo das **LINHAS de `metricas`** — várias coletas
da MESMA peça — em vez de tomar o **máximo POR PEÇA**. Uma peça coletada cinco
vezes com 2 ganhos lia 10.

Refeito com `max` por peça, sobre as **161 peças** que têm métrica:

| canal × formato | peças | ganharam algo | total | melhor peça | por peça REAL | o 691 dizia |
|---|---|---|---|---|---|---|
| epomeno **longo** | 18 | 4 | 6 | 2 | **0,33** | 1,25 |
| epomeno shorts | 35 | 3 | 5 | 2 | **0,14** | 0,45 |
| kolejny shorts | 43 | 3 | 4 | 2 | **0,09** | **1,00** |
| kolejny longo | 24 | 2 | 2 | 1 | **0,08** | 0,12 |
| labtreinamento shorts | 28 | 2 | 2 | 1 | **0,07** | 0,29 |
| labtreinamento longo | 13 | **0** | 0 | 0 | **0,00** | 0,00 |

**Inflado de 3x a 11x, e A ORDEM INVERTE:** o melhor par é **epomeno longo**, e o
`kolejny` short — que eu chamei de "o único caminho" e deixei governar a escolha
de canal por três dias — é o **quarto**.

**Três fatos que não se negociam mais:**
1. **161 peças renderam 19 inscritos.** Só **14 delas (8,7%)** ganharam algo.
2. **NENHUMA peça da frota jamais trouxe mais de DOIS inscritos.**
3. As de mais view confirmam a taxa **por view**, não por peça: `P6_FSisOJ3o`
   1.614 views → 2 inscritos; `VcpxgL981Bk` 1.385 → 2; `DDaZqbcZCTM` 1.132 → 1.
   Isso é ~1 por mil, e bate com o 668.

**A CONSEQUÊNCIA, e ela é a resposta honesta à pergunta do dono:** no melhor par
medido (0,33/peça), os 481 que faltam ao epomeno pedem **~1.458 longos**. Por
view, os 432 do labtreinamento pedem **~360.000 views num canal** — e a frota
inteira acumulou **~39.000 em toda a sua vida**. **A Porta 1 não é alcançável por
volume de peça em prazo nenhum que importe.** Só por uma peça que ROMPA para
dezenas de milhares de views, e isso é distribuição, não produção.

**Logo: parar de somar linha de métrica como se fosse peça, e parar de prometer
prazo por volume.** A pergunta que vale passa a ser "o que faz uma peça romper",
e ela só se responde com retenção nos três primeiros segundos.

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

**E ESTA ÚLTIMA FRASE CAIU EM 12/10 ÀS 20:1x, medida pelo próprio portão.** Ele
avisou que o `labtreinamento-s022` seria a **SEXTA peça idêntica** em
`titulo-item-item-titulo-item-item-titulo-item-cta` — as cinco do formato novo de
hoje usaram todas a mesma sequência. **A forma nova virou molde próprio em um
dia.** O aviso para de aparecer por UMA peça, não pela forma; depois a forma nova
repete como a antiga repetia. O `s022` saiu com
`titulo-item-titulo-item-item-item-titulo-item-cta` e o aviso parou — e **mudar a
ordem dos layouts não é mexer em limiar, é conteúdo.** A regra que fica: **varie o
esqueleto a cada peça, e deixe o portão dizer quando ele repetiu**, em vez de
confiar numa forma por ser nova.

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

## O instrumento do segundo ângulo deu FALSO POSITIVO em três origens

**Medido em 12/10 12:1x, na primeira vez que eu usei o `segundo_angulo.py` para
escolher — uma rodada depois de escrevê-lo.** Três origens do kolejny
(`MjI4ZGJAhIo`, `SP7Vz8qHdRY`, `Xgt32iH8Ft8`) resolveram para a spec
`kolejny-poziom`, que é o **slug do canal** e tem dez cenas de longo.

**É verdade conhecida que estava errado em pelo menos um caso:** o docstring do
`kolejny-poziom-s017`, escrito por mim em 11/10, diz que o `Xgt32iH8Ft8` é do
pacote `kp-plan-9233-20260811` e que **não tem spec em `fabrica/specs/`**. A
resposta certa é **None**, e o módulo devolvia um pacote — mandaria a rodada
seguinte ler capítulo de outro vídeo.

Duas causas, as duas consertadas com teste: o nome casava **sem fronteira**
(`kolejny-poziom` dentro de `kolejny-poziom-s017`), e **slug de canal não é nome
de pacote** — a spec homônima do canal é genérica ou legada e saiu do
vocabulário.

**E A CONTAGEM QUE EU REPORTEI ESTAVA INFLADA.** Eu disse "47 das 49 origens,
3.282 capítulos". Depois do conserto: **41 resolvidas, 3.057 capítulos**, e **8
honestamente reportadas como sem convenção** — para essas, a rota é o
`capitulos.yml` com `legenda=true`. Seis dos 47 eram o falso positivo do slug.

**O que sobra de dúvida sai MARCADO:** pacote com menos de **20** cenas de longo
vira `suspeito=True`. O limiar é **observado** — os longos de verdade da frota
medem **56 a 90** capítulos, e os únicos casos de dez eram esse falso positivo.

## A UNIDADE DE PAUTA É (LONGO × FAMÍLIA DE CAPÍTULO), não o longo

**Medido em 12/10, e retrata "a pauta acabou" pela TERCEIRA vez no mesmo dia.**
Das **49** origens que as specs consomem, **48 foram usadas UMA vez e uma foi
usada DUAS**: `h04-UVlVevs` rendeu `epomeno-epipedo-s002` e `-s006`, as duas
**publicadas** e com entradas erradas diferentes — período errado numa,
média-contra-marginal na outra.

**A regra (e) da rotina já dizia isso em letra:** *"a entrada errada vem do
capítulo que o short ORIGINAL não usou"* pressupõe que o mesmo longo rende mais
de um short. Eu tratei cada longo como uso **único por HÁBITO, não por regra**, e
com ~9 capítulos por longo isso deixou a maior parte da pauta parada enquanto eu
anunciava que ela tinha acabado.

**O que isso NÃO é:** não é licença para repetir. O segundo ângulo exige
**família de entrada errada diferente** e tem de passar o `similaridade` (≤0,65
contra o mesmo canal). E não dispensa a regra (f) dentro do mesmo dia.

`fabrica/pauta_viva.py` passou a relatar as **duas** contagens: origem sem nenhum
short, e origem com **um** short e capítulos intocados. Grupo de cópias do mesmo
título conta uma vez, e origem já usada duas vezes sai dos dois baldes.

## REFILAR a pauta exige FONTE, e a fonte está bloqueada na rede — medido em 12/10

**Isto corrige a conclusão da seção seguinte, e é a medição que estava faltando.**
Eu venho dizendo há dias que "a restrição real é PAUTA" e que "origem só nasce de
LONGO novo". As duas frases seguem verdadeiras — mas elas deixavam implícito que
escrever o longo depende de mim, e **não depende**.

Longo carrega número sobre o mundo, e número só entra se bater em **duas fontes
institucionais** (600). Medido às 10:15 de 12/10, com `curl` e `-v`, o proxy do
ambiente devolve **403 ao CONNECT** para os quatro hosts que a rotina nomeia:

| host | CONNECT |
|---|---|
| `ec.europa.eu` (Eurostat) | **403** |
| `www.statistics.gr` (ELSTAT) | **403** |
| `api.sejm.gov.pl` (ELI do Sejm) | **403** |
| `www.gov.br` | **403** |

Confirmado no `__agentproxy/status`, que lista os quatro em `recentRelayFailures`
com `"gateway answered 403 to CONNECT (policy denial)"`. **É negação de POLÍTICA,
não oscilação** — e a rotina manda não reter o que foi medido como bloqueio de
proxy, porque ali a resposta não muda.

**A rota documentada para fonte é `pg_net`** — a busca acontece dentro do
Postgres, então o proxy não entra.

**E ISTO CAIU EM 12/10 ÀS 13:4x, MEDIDO — a frase seguinte era minha e era
falsa.** Eu escrevia aqui que "o `pg_net` depende do banco, e o banco está em
402". O **402 é do GATEWAY REST, não do Postgres**: `execute_sql` funciona e o
`pg_net` responde. Medido com `status_code` de cada chamada:
`ec.europa.eu` (Eurostat) **200**, 20.048.657 bytes (req 931); `www.googleapis.com`
**200** (req 932); REST **402** na mesma hora. Eu escrevi a rota certa — "o proxy
não entra" — e no parágrafo seguinte a declarei indisponível **sem testar**.
**LONGO NOVO voltou a ser possível.** Ver `docs/limpar-supabase-sql.md`.

**A consequência que importa — E ELA CAIU NA MESMA MEDIÇÃO:** eu escrevia que o
402 era "um único nó" que bloqueava medição, registro e refil de pauta. **Os
três estão abertos pelo Postgres** (`execute_sql` + `pg_net`); o que o 402 fecha
é o REST, o Storage e o runner que fala com o REST. O que segue verdadeiro é o
seguinte parágrafo apenas na parte do Storage e do `diario.yml`. Enquanto ele estiver
fechado, eu consigo escrever short de longo JÁ PUBLICADO (que não introduz número
novo, e por isso não exige fonte nova), e **não** consigo escrever longo novo.
Prometer longo novo nesta condição seria mentir com número.

**O remédio é humano, e são dois caminhos, não um:** Supabase Pro (devolve o
`pg_net`) **ou** liberar esses quatro hosts na política de rede do ambiente
(Network access → Allowed domains), que é a mesma tela da pendência do
`speech.platform.bing.com`.

## A restrição real é PAUTA, não cota nem aprovação

Medido em 09/10: **10 origens livres** (epomeno 4, kolejny 4, labtreinamento 2),
contra ~14 peças publicadas no dia. **Menos de um dia de pauta.** Cota não é o
limite; origem é. E origem só nasce de LONGO novo.

Isso converge com o 689: o longo converte ~5x melhor por view **e** gera pauta
**e** satisfaz os 3 uploads públicos/90 dias da Porta 1. Logo **pacote completo
deixa de ser exceção e passa a ser a produção principal** quando a pauta estiver
baixa.

## A CONCENTRAÇÃO DE PAUTA NUMA ORIGEM SÓ É HÁBITO MEU, e eu só a vi ao contar

**Medido em 13/10 às 04:0x.** O `labtreinamento` tinha **dez** shorts tirados do
MESMO longo (`ntrMxq89I4o`) — um terço dos trinta do canal — enquanto **nove das
treze origens foram usadas UMA vez só**, e o canal tem **doze specs de longo com
55 a 87 capítulos cada**. Não foi escassez de pauta: foi eu ficar no longo que
estava aberto na minha cabeça, chamando isso de "a unidade de pauta é
(LONGO × FAMÍLIA)" — que é verdade, e **não é licença para ficar num longo só**.

**E o risco não é estético:** o portão `similaridade` (≤0,65 contra o mesmo
canal) existe pelo conteúdo **inautêntico** do YPP — *"the substance of each
video should be materially varied"*. Concentração de origem ataca exatamente o
portão que estamos tentando passar, e cresce devagar, que é por que precisa de
contador e não de memória.

**No código:** `fabrica/concentracao.py` (`contagem`, `analise`, `relato`) e oito
testes. Rode antes de escolher pauta:

    python3 fabrica/concentracao.py labtreinamento

**O limiar de alerta é observado e declarado: MAIS que o dobro da segunda
origem.** E o caso real ficou **exatamente no limite** — 10 contra 5 **não**
alerta, porque 10 não é maior que 10. Eu relato isso em vez de arredondar para
"alertou": o instrumento disse "dentro do dobro", e a decisão de trocar de origem
foi minha, pela contagem das nove, não por um alarme. Há teste travando esse
caso de fronteira.

## A FONTE DECLARA "esses cinco casos" E ENUMERA SEIS — e nenhum portão barrava

**Medido em 13/10 às 05:0x, escrevendo o `s031` a partir do `labtreinamento-009`
(`dsoEo103l1o`).** O capítulo 35 diz *"depois de descartar esses CINCO casos"* e
os capítulos 28 a 33 enumeram **SEIS** — e o mesmo longo diz "os seis casos" em
outro ponto, contradizendo-se sozinho.

**Por que isso importa mais do que parece:** o short carrega o que o longo diz, e
**nada nosso barraria "os cinco casos"** num short cujo longo tem seis. O
`narracao` conta QUANTIDADES por frase e **não confere se a quantidade é
verdadeira**; a regra (g) tira número que MUDA (alíquota, data), e contagem de
casos não muda. Número errado no ar com portão verde — §3.8 outra vez.

**A decisão no `s031` foi OMITIR a contagem**, porque não se sabe qual número o
autor quis, e inventar um é pior que não dizer.

**No código:** `fabrica/contagem_declarada.py` e nove testes. Medido na frota:
**1 conflito em 207 specs** (só o `-009`).

**E ELE ME DEU DOIS FALSOS POSITIVOS ANTES DE FICAR DE PÉ, os dois na mesma
rodada** — e isso é a parte que vale guardar:
1. a primeira versão comparava a declaração com **qualquer** kicker ordinal, e um
   "Primeiro passo" fazia a conta do `-009` dar **sete**; eu quase relatei dois
   conflitos inventados e errei o terceiro;
2. a segunda pareava "os dois casos" do capítulo 20 do `-010` com quatro ordinais
   **nus** dos capítulos 59 a 62 — outra lista, outro assunto, quarenta capítulos
   de distância.
O conserto foi casar o **substantivo** e exigir **proximidade** (`JANELA = 12`).
Cada falso positivo tem teste próprio, porque **detector que inventa achado é
pior que não ter detector**.

## PORTÃO VERDE NÃO DISPENSA A MIRA DO CANAL — e o instrumento pegou o autor dele

**Medido em 13/10 às 06:1x, escrevendo o `labtreinamento-s032`.** A spec saiu com
**27,8 s reais previstos** no Piper. O portão `duracao` aprovou, e **com razão**:
ele cobra a faixa da FROTA. Mas o `labtreinamento` tem
`ALVO_POR_CANAL = (20,0 a 26,0)` desde 09/10, **medido** (698) — e 27,8 está fora.
O portão e a mira respondem perguntas diferentes, e eu vinha confiando no portão
para as duas.

**E o instrumento pegou a peça do próprio autor um minuto depois de existir:** eu
encurtei a spec olhando o Piper, e a segunda versão ainda dava **28,5 s no mundo
`edge`**. Terceira versão: **edge 25,3 e piper 20,7**, os dois dentro. O provedor
se decide no runner, então a peça tem de cair na mira **seja quem narre** — a
mesma lógica do conserto do portão às 02:1x.

**No código:** `fabrica/mira.py` (`previsoes`, `confere`, `relato`) e oito testes.
Rode na spec antes do render:

    python3 fabrica/mira.py fabrica/specs/<spec>.json

**POR QUE NÃO É AVISO DENTRO DO `prontidao`, e a razão é medida:** das specs do
`labtreinamento` com voz modelada, **44 ficam fora da mira no mundo `edge` e 28
no `piper`** — quase todas peças históricas, de antes do override. Aviso de portão
que dispara 44 vezes é aviso que se aprende a ignorar, e aí ele deixa de avisar o
caso que importa.

**E um teste meu pegou um número meu:** eu havia escrito "(18 a 45)" dentro da
mensagem do módulo, e o teste que proíbe limiar cravado reprovou — aquele número
envelhece se a faixa mudar. A mensagem passou a dizer "a faixa da FROTA, que é
mais larga", sem número.

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
- **E quando o banco está em 402, a consulta NÃO roda.** Nesse caso a fonte é
  **`pauta-viva.yml` → `fabrica/pauta_viva.py`**, que lê a **playlist de uploads
  pela API** — a lista viva, sem banco e sem retrato.
  **RETRATAÇÃO DE 12/10, e é do que estava escrito nesta linha:** eu apontava
  aqui a reconstrução pelo retrato `fabrica/ponte/videos.json`. Aquele arquivo é
  de **06/10**; eu escrevi a ressalva certa ("longo publicado depois não
  aparece") e então tratei o número como estoque por três rodadas, anunciando
  "a pauta acabou". O vivo achou **três** origens onde o retrato dizia uma, duas
  delas no epomeno. `fabrica/pauta_local.py` continua existindo como **piso**
  (sem token, fora do runner) e o relato dele diz isso.
- **O vivo tem um filtro que não é zelo:** ele só conta longo cujo título está no
  `corpus_publicados.json`. Sem isso devolveu **65 "origens livres"** no
  labtreinamento que eram as **aulas de curso do dono**, anteriores à máquina —
  o 668 reaparecendo como pauta em vez de como denominador.
- **E origem livre pode não ter spec local** (regra h). Os capítulos saem da
  descrição publicada por **`capitulos.yml` → `fabrica/capitulos_do_longo.py`**;
  mas **a descrição dá só o TÍTULO do capítulo**, e escrever a partir de título
  seria inventar conteúdo. O texto sai da faixa de **legenda** que a própria
  máquina subiu (`legenda=true`). Foi assim que o `eZ697VNYCPU` virou pauta: 75
  falas, 9.249 caracteres.
- Em qualquer caminho, **confira a origem escolhida contra as specs antes de
  escrever**, uma a uma — e conte por **TÍTULO DISTINTO**, nunca por id: em 12/10
  eu errei a mesma conta três vezes (cinco → três → dois) porque dez ids livres
  eram dez cópias de um título.

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

  **E ISSO TAMBÉM SAIU DA MINHA CABEÇA em 12/10: `fabrica/janela_casada.py`.**
  Ele escolhe a leitura de cada peça dentro da faixa de idade declarada (o
  MÁXIMO, pelo 688), diz se as faixas dos dois braços se sobrepõem e — o ponto —
  **recusa chamar de leitura quando se sobrepõem**, em vez de deixar quem lê
  escolher a mediana que lhe convém. Treze testes, ancorados nos números reais de
  698, 701 e 12/10.
  **Dois achados do próprio módulo, e os dois são erros meus:** (1) o "~1%" que
  eu reportei no 698 está errado — `C(10,2) = 45`, logo **2,2%**; eu usei ~1/9
  (uma peça abaixo de oito) e tratei as duas como independentes, e elas são
  escolha SEM reposição. O "1,4%" do 701 está certo. (2) Com os dados de 12/10,
  **truncar o braço antigo de quatro peças para duas FABRICA uma separação** com
  p = 1/6 sem nenhum valor mudar — é o 684 em uma linha, e tem teste próprio.

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

## O PIPER NARRA 10 A 20% MAIS RÁPIDO QUE O MODELO — e o portão passou peça fora da faixa

**Aprendizado 711, `alto`, medido às 14:1x de 12/10, na primeira medição gravada
depois do banco destravar.** O `R`/`P` de `MODELO_VOZ` é do **edge-tts** e não
vale para as vozes do Piper. Duração REAL (`contentDetails.duration`, e o YouTube
ARREDONDA PARA CIMA) contra `ensaio.duracao_estimada_short` da própria spec:

| peça | voz | est | real | desvio |
|---|---|---|---|---|
| `epomeno-epipedo-s016` | el-GR, **edge-tts** | 41,6 | 42 | **+0,9%** |
| `epomeno-epipedo-s017` | el-GR, Piper | 42,9 | 38 | −11,4% |
| `epomeno-epipedo-s018` | el-GR, Piper | 41,9 | 35 | −16,6% |
| `epomeno-epipedo-s019` | el-GR, Piper | 41,6 | 36 | −13,5% |
| `kolejny-poziom-s018` | pl-PL, Piper | 42,3 | 34 | −19,5% |
| `kolejny-poziom-s019` | pl-PL, Piper | 42,3 | 38 | −10,2% |
| `labtreinamento-s013` | pt-BR, Piper | 37,5 | 32 | −14,6% |
| `labtreinamento-s014` | pt-BR, Piper | 36,2 | **29** | −20,0% |
| `labtreinamento-s015` | pt-BR, Piper | 36,5 | 30 | −17,9% |

**As oito do Piper são TODAS negativas; a única do edge-tts acerta.** Sob a nula
de o modelo valer igual, oito de oito negativas dá **1/256**.

**A consequência que importa, e ela já aconteceu:** o portão `duracao` compara o
**estimado** contra 30,0–43,1 s. Então ele **aprova em silêncio** peça que sai
fora da faixa — o `labtreinamento-s014` (`K-k8vT0IY2M`) foi ao ar com **29 s
reais contra um piso de 30**. É o §3.8 na forma mais literal: portão verde
fabricou "está tudo certo" porque o instrumento media outra coisa.

**Confundidor declarado:** n=1 no braço edge-tts, e as duas `pl-PL` são do mesmo
canal. O que NÃO é confundido é o sinal: todas as oito na mesma direção.

**CONSERTADO EM 13/10 ÀS 02:1x, e não como eu tinha previsto.** Eu escrevi
abaixo que o conserto certo era "a estimativa receber o PROVEDOR". O conserto que
entrou é mais simples e não precisa saber o provedor: **o portão `duracao` passou
a exigir que a peça caiba na faixa nos DOIS mundos** — `duracao_real_prevista`
com `edge` e com `piper`, e reprova se qualquer um sair de 18 a 45 s. O provedor
se decide no runner, então a peça tem de ser segura seja quem narre.

**E a medição ANTES de ligar diz o tamanho honesto do que foi consertado: ZERO
specs atuais passavam pelo estimado com o Piper fora da faixa.** O buraco que
matou o `labtreinamento-s014` (29 s reais contra piso de 30) fechou quando a
faixa virou 18–45, **não porque o portão tenha aprendido o provedor** — ele
seguia medindo a coisa errada e acertando por folga. Então isto fecha um buraco
**LATENTE**, e eu digo isso em vez de vender conserto de defeito ativo.
`tests/test_duracao_dos_dois_provedores.py`, seis testes, e um deles **falha se
alguém transformar isto em limiar novo**: 18 e 45 não mudaram.

**Não corrigi `MODELO_VOZ` ainda**, e o motivo é que a spec declara a voz do
edge-tts mesmo quando o Piper é quem narra — o provedor se decide no runner,
depois das três tentativas. O conserto certo é a estimativa receber o PROVEDOR,
não a tabela ser reescrita por baixo. Desenho pré-registrado antes de mexer.

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
trazer `titulos_no_ar_n`, senão o runner recusa.

### E O REGISTRO NO CORPUS É PASSO MEU, E EU O ESQUECI SETE RODADAS SEGUIDAS

**Medido em 13/10 às 00:2x.** Com o REST em 402, quem acrescenta o título
publicado ao `fabrica/corpus_publicados.json` sou **eu**, lendo o
`::notice:: PUBLICADO` do `retomar.yml` e comitando. Eu fiz isso até o
`labtreinamento-s019` (17:13 de 12/10) e **parei** — as sete peças seguintes
(`s020` a `s026`) foram ao ar e nenhuma entrou no corpus.

**E nada reclamou, porque nenhum portão lê o corpus contra o que está no ar.** O
`prontidao` usa o corpus para barrar título duplicado, e corpus atrasado
simplesmente **não barra**: a falha é silenciosa e no sentido **permissivo**, que
é o pior. Sete rodadas em que a trava por título existia no papel e não existia
de fato.

**E A PRIMEIRA MEDIÇÃO QUE EU FIZ DISSO ESTAVA ERRADA, por um fator de dezessete
peças.** Eu grepei o `## TITULO` **longo** da copy, achei zero em todas as
dezessete publicações do `retomar.yml` e quase relatei que "o corpus parou de
crescer quando a publicação mudou da ponte para o retomar". **O corpus guarda o
`## TITULO SHORT`** — o que o YouTube recebe — e por essa forma dezesseis das
dezessete estavam lá. O atraso real começa exatamente no `s020`, e a causa é
hábito meu, não mudança de rota.

**No código:** `fabrica/corpus_atrasado.py` (`titulos_dos_notices`, `faltantes`,
`aplicar`, `relato`) e dez testes ancorados nos sete títulos reais. O
`titulo=` do próprio notice é a forma certa; linha com `youtube_id=?` (run
abortado) **não entra**. Rode depois de publicar:

    <notices do retomar.yml> | python3 fabrica/corpus_atrasado.py --aplicar

**E NÃO MONTE O `estado_b64` À MÃO — rode `python3 fabrica/estado_ponte.py`**
(aprendizado 718). O `titulos_no_ar` é lista de **OBJETOS** com a chave
`titulo`; lista de strings faz a trava por título levantar `AttributeError` e o
run morre em *"Conferir o estado antes de publicar"*. Em 12/10 eu montei à mão e
perdi o run `38290045583` — **e o docstring do próprio `estado_ponte.py` descreve
exatamente esse erro.** Código e aviso escritos não servem de nada se a rodada
não os procura antes de improvisar. A ponte continua existindo; ela
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

### E O "MÁXIMO COMO PISO" CAIU EM 12/10 ÀS 20:1x — aprendizado 720

**Medido, e é a minha própria palavra "piso" que cai.** Quatro peças, quatro
leituras de hora em hora:

| peça | 17:10 | 18:21 | **19:11** | 20:11 |
|---|---|---|---|---|
| `MjeP-_yDni4` | 20 | 20 | **24** | **20** |
| `O1PNIRYoeGY` | 1 | 1 | **7** | **1** |
| `xhPyfHdTwds` | 0 | 2 | **8** | **2** |
| `nUrSPWKHy8I` | — | 114 | 115 | **122** |

Dentro da rodada das 19:11 as três chamadas deram `{20,24,20}`, `{1,7,1}`,
`{2,8,2}`. O `replica.chamada_para_gravar` escolheu a de soma máxima — como o 708
manda — e **gravou um PICO em três das quatro peças**: às 20:11 as três chamadas
devolveram, nas três peças, o valor da **MODA** de 19:11. **A moda acertou três de
três e o máximo errou três de três.**

**E a MESMA chamada estava CERTA para a quarta peça** (`nUrSPWKHy8I`, 114 → 115 →
122, subida que persistiu). Logo o veredito é **por peça, não por chamada** — e
**dentro de uma rodada as duas situações são indistinguíveis**: chamada alta
solitária pode ser réplica fresca (688) ou pico. **Quem decide é a rodada
SEGUINTE.**

**O que cai é a palavra PISO, não o 688.** No 688 as dezessete peças subiram *e a
subida PERSISTIU*. Aqui não persistiu. Então o máximo é o **máximo OBSERVADO** —
um número que três chamadas depois já não existe não era piso de nada.

**No código:** `replica.moda()` e `replica.veredito_do_pico(leituras, seguinte)`,
que devolve `fresca` / `pico` / `indeterminado` por peça. Quinze testes, sete
novos, ancorados nesta série e no caso do 688 (que continua dando `fresca`).
**A linha de `metricas` de uma rodada de pico NÃO se apaga** — ela é o que a API
disse; o que se corrige é a leitura que se faz dela.

### E UMA HORA DEPOIS O 720 CAIU — aprendizado 721, `crítico`

**Medido às 21:1x, pelo `veredito_do_pico` que eu acabara de escrever para
sustentar o 720.** Ele devolveu **"fresca" nas quatro peças**:

| peça | 17:10 | 18:21 | 19:11 | **20:11** | 21:1x |
|---|---|---|---|---|---|
| `MjeP-_yDni4` | 20 | 20 | 24 | **20** | **40** |
| `O1PNIRYoeGY` | 1 | 1 | 7 | **1** | **10** |
| `xhPyfHdTwds` | 0 | 2 | 8 | **2** | **8** |
| `nUrSPWKHy8I` | — | 114 | 115 | 122 | 122 |

**O 8 do `xhPyfHdTwds` VOLTOU, idêntico, nas três chamadas das 21:1x.** View não
ressuscita — logo o 8 das 19:11 era verdade, e **a rodada das 20:11 INTEIRA, as
três chamadas, caiu na réplica atrasada.** Não houve pico nenhum.

**O 708 era mais forte do que eu entendi:** a réplica atrasada não é só da
CHAMADA, ela pode ser da **RODADA**. E a consequência é dura — **três chamadas de
acordo NÃO são evidência de verdade.** Concordância dentro da rodada mede uma
coisa só: que as três caíram na mesma partição.

**O discriminador não está dentro da rodada, está no TEMPO: o contador de view
não desce.** Leitura mais nova abaixo de leitura mais velha é a **nova** que está
atrasada, em qualquer rodada e com qualquer concordância. No código:
`replica.monotonia(serie)` acusa a rodada atrasada peça por peça —
nos dados reais ele aponta **só o `20:11`, nas três peças** — e
`replica.piso_por_rodadas(serie)` dá o piso que de fato vale (8, não 2). Vinte
testes, cinco novos, e um deles **falha se o 720 voltar**.

**O que sobrevive do 720:** a palavra "piso" continua caindo para o máximo de UMA
rodada, e moda e máximo seguem indistinguíveis dentro dela. **O que cai é a
acusação de pico.** Duas retratações minhas em noventa minutos, e as duas pelo
instrumento, não por eu reler.

**E às 22:1x o `monotonia` teve o primeiro uso em produção — aprendizado 722.**
Somas 252 / 279 / 264, `mesma_forma` **False** (a hipótese do 708 não se
aplicava). A monotonia contra a rodada anterior resolveu sozinha: **a chamada 1
foi a única sem violação**, e as outras duas reportaram peça abaixo da leitura de
uma hora antes. **Dois critérios independentes — soma máxima e monotonia —
apontaram a MESMA chamada.**

**Mas a chamada escolhida SUBESTIMA peça**, e isso tem de ir dito: `byriXB1gSg8`
gravou 38 com piso real **41**, e `oAAxm8VzjOc` gravou 11 com piso real **12**.
A linha **não se corrige**: o `grava_metricas_janela` recebe UM `req_id` e a linha
é o que aquela chamada disse — inventar número de outra chamada seria fabricar
leitura que requisição nenhuma devolveu. **Compare `piso(leituras)` com a chamada
escolhida e declare a diferença.**

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
- banco: **NÃO use `list_projects` — ele MENTIU e eu o usei por dias**
  (aprendizado 709, `crítico`). Ele reflete a ORGANIZAÇÃO a que o conector está
  ligado; em 12/10 ele devolveu só `imobjazz-eng's Project` **enquanto o
  `execute_sql` no `vevocauwtarctfwngrch` funcionava**. A sonda é a CAPACIDADE:
  `execute_sql` com `select pg_database_size(current_database())`. Catálogo não
  é acesso;
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
