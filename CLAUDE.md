# Máquina de vídeos — o que nunca deve envelhecer

A rotina horária carrega o procedimento. Este arquivo carrega só os **ponteiros**,
porque número dentro de prompt envelhece e já me fez errar quatro vezes
(652/655, 658, 682, 685). Aqui não entra contagem de estoque, nem de views, nem
de inscritos. Entra onde olhar.

## A LEGENDA DO SHORT SOLTO ESTAVA CONGELADA — e é o caminho de TODA peça

**Pedido do dono em 19/10:** *"os vídeos publicados, me parecem todos a mesma
dinâmica, imagens, formas, estilo. Em todos os canais. Ajuste. Explore a
documentação."*

**MEDIDO ANTES DE CONCORDAR**, varrendo as 205 specs de short da frota:

| | |
|---|---|
| layouts que existem no short | **4** (titulo, item, lista, cta) |
| cenas em `item` + `titulo` | **1.554 de 1.667 = 93%** |
| esqueleto mais repetido | `titulo-titulo-titulo-titulo-cta`, **o MESMO nos três canais** |
| fundos | `#F3F7FA`, `#F4F1EA`, `#F5F3ED` — três claros quase iguais |
| `barras` | existe no render e foi usada **0 vezes em 205** |

**E o pior não estava na contagem: a legenda queimada do short SOLTO era a fala
INTEIRA, congelada pela cena toda.** Medido no próprio arquivo publicado
(`ANxWQYgtUAY`), baixado e lido quadro a quadro: a faixa escura da legenda vai de
**y=471 a y=562** num quadro de 360×640 — 91 px, **14% da altura, três linhas** —
e o perfil de pixels escuros por linha é **IDÊNTICO em t=1,0 s e t=2,8 s**.

**A causa é a assinatura que o próprio `etapas.py` já carrega: DOIS DONOS DA
MESMA REGRA, UM ATUALIZADO.** O `legenda.py` foi escrito em 09/10 porque ~18
palavras paradas por oito segundos deixavam 91% dos quadros congelados; o
conserto entrou no `fabrica.py:862` e **não entrou no `etapas.py:363`** — que é o
caminho do SHORT SOLTO, isto é, de praticamente toda peça da frota. É a mesma
forma do `assert 20 <= ds <= 60` cravado nesse mesmo arquivo, que em 16/10 matou
o run `38847013520`.

**CONSERTADO e MEDIDO no ar:** o `kolejny-poziom-s064` (`GESLIl-iUeo`) tem o
perfil da legenda **mudando dentro da mesma cena** (igual em 0,8/1,6/2,4 s e
DIFERENTE em 3,2 s), contra o perfil imóvel da peça anterior.
`tests/test_a_legenda_do_short_SOLTO_estava_congelada.py`, sete testes, com
contraprova no outro sentido — frase curta continua em UM bloco, porque quebrar
duas palavras em duas piscaria a tela sem motivo.

### E CADA CANAL PASSA A TER A PRÓPRIA IDENTIDADE, TIRADA DA DOCUMENTAÇÃO DELE

`fabrica/temas_do_dono.py` copia os **quatro** temas do `motor/config.py` do
pipeline que ele mandou, com a descrição escrita por ele, e atribui um por canal:

| canal | tema | procedência |
|---|---|---|
| labtreinamento | `noite` | **MEDIDO** — é a paleta do longo de referência dele |
| epomeno-epipedo | `papel` | a descrição DELE nomeia *"finanças pessoais"* |
| kolejny-poziom | `misterio` | **ELIMINAÇÃO**, e vai declarado como tal |

**A FONTE de cada tema NÃO atravessa, e o motivo vai escrito:** trocar família
arrisca glifo ausente em grego e polonês, e isso só aparece **depois** de
publicar. Fica como passo medido — conferir o que o runner tem instalado antes.

**E o `paleta_referencia.py` passou a LER do `temas_do_dono`** em vez de repetir
os hex: era o mesmo defeito de dois donos que congelou a legenda, agora pego
antes. O ajuste do `c2` do labtreinamento (painel em vez de acento, pelo SATAVG
medido nos 530 quadros) virou entrada explícita em `AJUSTES`, com a medida ao
lado. `tests/test_cada_canal_tem_a_PROPRIA_identidade.py`, doze testes — e
**canal desconhecido LEVANTA em vez de cair num padrão**, porque padrão
silencioso foi exatamente como os três fundos convergiram. O teste da fonte única
é por **AST**, porque o módulo CITA um hex na prosa para explicar a medida da
capa, e casar prosa pegaria a explicação em vez do código.

**O que isto NÃO conserta, e vai dito:** as 205 peças já publicadas seguem com a
legenda congelada e com a paleta antiga. Apagar ou substituir peça publicada
exige o dono. O conserto vale da `s064` em diante.

## OS LAYOUTS DO LONGO ESTAVAM ESCRITOS E MORTOS — medido em 19/10 às 04:2x

O `fabrica/layouts_longo.py` nasceu na madrugada com `comparar` e `numero`,
coordenadas copiadas do `motor/scenes.html` do pipeline do dono — e **nenhum
caminho do render os alcançava.** O despacho do `svg_cena` (16:9) conhecia
`broll`, `titulo`, `cta`, `lista`, `barras` e `item`; cena com `layout:
comparar` caía no ramo final e saía **como fundo vazio**. Sem erro, sem aviso:
um cartão em branco no meio do vídeo.

**É a mesma classe do defeito da legenda, pego três horas antes: código escrito
que ninguém chama PARECE pronto e não está no ar.** Lá eram dois donos da mesma
regra com um atualizado; aqui é um dono só, sem ninguém chamando. A diferença
prática é nenhuma — nos dois casos eu reportei a capacidade como existente.

**Consertado:** `svg_cena` chama `LL.desenha` logo depois do `broll`, e os dois
layouts desenham. **Só no 16:9** — a geometria deles é 1920×1080 e o retrato tem
conta própria, e há teste que **falha se o despacho entrar no
`svg_cena_retrato`**, porque ali ele produziria tinta na borda (o defeito do
`kp-plan-9233`).

`tests/test_os_layouts_de_longo_estavam_MORTOS.py`, sete testes, e o que vale é
a forma de dois deles: a varredura sai de **`LAYOUTS`**, não de uma lista minha
— layout novo entra na cobertura sozinho e **reprova se não tiver cena de
exemplo** —, e um cobra que o CONTEÚDO da cena chega ao SVG, porque o defeito
não era "não desenha", era "desenha o fundo e esquece a cena". Contraprova nos
dois sentidos: desligado o despacho, dois dos sete falham.

**O que isto NÃO faz:** não produz longo nenhum. Faltam os três layouts que a
medição do vídeo de referência nomeia (fórmula anotada, cartão de erro, divisor
de parte), a cadência de plano de ~18,9 s e o trilho de capítulos ligado ao
render. O que mudou é que dois dos cinco deixaram de ser promessa.

## E ESSA SEÇÃO ABAIXO FICOU OBSOLETA EM 19/10 — O PROMPT DEIXOU DE SER CÓPIA

**Pedido do dono em 19/10:** *"Não esqueça de otimizar a rotina YT, diretamente,
já ativa"* e, depois, *"já deixe este aprendizado na rotina, para ficar 100% auto,
após as correções. Na rotina também importante ter, para evolução do sistema."*

**O prompt do gatilho `trig_01Y6ZvwsrbxteyS933sgzqK4` é agora um NÚCLEO de 10 KB
que manda ler `docs/ROTINA.md`** — aplicado às 02:08:48Z e reemitido às 02:22:16Z,
com o `derived_state.prompt` voltando idêntico nas duas vezes. A cópia versionada
dele é `docs/ROTINA-NUCLEO.md`.

**Logo a seção seguinte — que existia para governar enquanto a sincronia não
fosse feita — perdeu o objeto.** O número da cota que ela corrige segue valendo
(e foi ele mesmo retratado depois, pela sétima peça da janela); o que caiu é a
PREMISSA dela: *"a sincronia com o trigger NÃO foi feita, e o motivo é que o
`update_trigger` substitui o prompt INTEIRO, logo aplicar exigiria reproduzir
~65 KB byte a byte"*. **Esse motivo estava certo e a saída era outra: parar de
pôr procedimento no prompt.** Eu tratei o teto como restrição a contornar por
seis dias, quando ele era o sintoma de um desenho errado.

**As três medições que derrubaram a cópia** estão na §11 do `docs/ROTINA.md`: a
cópia divergia (11, 12 e 13/10, mandando a mira "33 a 37" e a cota "~40
vídeos/janela" já retratadas), o teto de 65.536 bytes transformava correção em
migração de história, e a sincronia não cabia numa chamada (~32 mil tokens).

**O que FICOU no núcleo**, porque não pode se perder se o repo não abrir: a frota
e os ids, a autorização permanente **com o ciclo inteiro em letra** (terminar uma
correção NÃO é terminar a rodada), as travas, o passo zero da Porta 1, o formato
da resposta e a disciplina do instrumento. **O `update_trigger` só se chama
quando uma TRAVA, a AUTORIZAÇÃO, o PASSO ZERO ou o FORMATO mudarem** — nunca por
achado nem por número.

**E A EVOLUÇÃO DO SISTEMA VIROU PASSO DE TODA RODADA, não só da de construção**
(§11-bis): um instrumento no lugar de uma conta feita de cabeça, uma retratação
travada com teste que cobra PROPRIEDADE e não identidade, e um passo manual a
menos. **A medida de que evoluiu é UMA e é externa: a distância em DIAS para os
500 inscritos.** Instrumento que não muda essa distância é dívida com nome bonito.

**PONTO CEGO DECLARADO, e é da mesma classe do que ele conserta: nenhum teste
alcança o prompt VIVO.** `tests/test_rotina_cabe_no_trigger.py` (13 testes,
reescrito — ele cobrava o teto de 65.536 no corpo da rotina, que hoje tem 69.742
bytes de propósito) prova que o núcleo ESCRITO carrega as travas; que o gravado é
igual a ele depende de quem editar chamar o `update_trigger` no mesmo passo. A
diferença contra o desenho antigo é o TAMANHO do que precisa dessa disciplina:
10 KB que mudam quando uma trava muda, em vez de 64 KB que mudavam toda rodada.

**E O `comm` CONTRA A LINHA DE BASE PRECISA DO MESMO FORMATO NOS DOIS LADOS —
medido nesta rodada.** O `pytest -q` trunca a linha do `FAILED` com
` - AssertionEr...`; a base desta sessão tinha a linha inteira. O `comm` acusou
**duas falhas novas e duas desaparecidas que eram o MESMO teste nos dois lados.**
Normalize antes (`sed 's/ - .*$//' | sort`), senão o instrumento fabrica
regressão — a mesma classe do grep de 17/10 que quase me fez declarar a rota dos
inscritos fechada. Conferido assim: **25 falham, idêntico à base, nos dois
sentidos do `comm`.**

## A COTA DO PROMPT QUE VOCÊ ACABOU DE LER ESTÁ CORRIGIDA — E A CORREÇÃO É DAQUI

**Se o prompt que disparou esta rodada disser "COTA ~40 vídeos/janela (619)",
ele está DESATUALIZADO nessa linha.** O `docs/ROTINA.md` já foi corrigido em
18/10 às 23:4x; **a sincronia com o trigger NÃO foi feita**, e o motivo vai
escrito porque é decisão e não esquecimento: o `update_trigger` substitui o
prompt INTEIRO, logo aplicar exigiria reproduzir ~65 KB de markdown cheio de
travas byte a byte, e a conferência por md5 só acusaria o erro **depois** de o
texto gravado já ter sido trocado. Trava corrompida em silêncio é pior que número
velho documentado. **Enquanto isso, esta seção governa**, e ela é lida primeiro
por ordem do próprio prompt.

**O número certo: ~6 ENVIOS DE VÍDEO POR DIA POR PROJETO**, de `10.000 / 1.600`.
`videos.insert` custa **1.600** unidades, `captions.insert` **400**, e a cota
padrão de um projeto é **10.000/dia**. Os "~40 vídeos/janela" pediriam 64.000
unidades — 6,4x a cota.

**A conferência não dependeu de fonte externa**, e isso é o que a torna barata:
a contradição era entre dois documentos NOSSOS. A §4 da rotina sempre disse
*"~1.600 de cota"* para o short solto e *"~2.100"* para o pacote, enquanto o
`orquestra.py` dizia *"~500 unidades de um pacote"* — e um pacote não pode custar
menos que um short solto. Quem me fez olhar foi o guia do ZIP v2.0 que o dono
trouxe; o que provou foi a nossa própria aritmética.

**A CONSEQUÊNCIA ATINGE O PEDIDO DE 7/dia/canal, por uma via TERCEIRA.** As duas
que eu já reportava eram nossas ou do agendador: o `TETO_POR_CANAL` em 1/dia (que
o dono pode mudar) e o cron entregando 5,1 disparos/dia. **Esta não se resolve com
decisão nossa** — pede extensão de cota ao YouTube, pelo formulário de auditoria.

**E o que eu NÃO sei vai declarado: se a cota é por canal ou da frota inteira.**
Seis envios/dia por canal são dezoito na frota; seis para os três juntos são seis.
Depende de os três usarem UM projeto do Google Cloud ou três — o 667 diz que o par
`client_id`/`client_secret` é da linha `yt_token_<canal>`, mas o
`fabrica/tokens.py:205-206` mina token novo copiando o par de um **MODELO**, logo
pode ter propagado o mesmo projeto. Isso se lê no banco, e o `execute_sql` está
negado. **Em 18/10 a frota fechou o dia em seis peças — 9.600 de 10.000 —, logo se
o projeto for um só, a sétima teria levado `403 quota`.** Não publiquei uma sétima
para testar: gastar cota do dono num experimento que eu inventei é o que a §10
proíbe.

A conta inteira, a prova de que as peças são públicas e os quatro layouts do longo
estão em `docs/pipeline-canal-dark-v2-o-que-entrou.md`. Travado em
`tests/test_a_cota_de_40_videos_estava_errada.py`, nove testes.

### E EM 19/10 ÀS 00:2x ISSO FOI MEDIDO, e caiu no PIOR dos dois ramos

**Os três canais COMPARTILHAM um projeto do Google Cloud: `777159180424`.**
Medido pela `sonda_oauth` no runner (job `117829119323`), que passou a extrair o
número do projeto do `client_id` — número que não é segredo, ao contrário do
resto dele. **Logo o teto é ~6 vídeos/dia NA FROTA INTEIRA**, não por canal, e os
7/dia/canal que o dono pede são **21/dia = 33.600 unidades = 3,4x a cota.**

**E a consequência era imediata, não teórica.** A cota da YouTube Data API zera à
**meia-noite do Pacífico**, não em UTC — em outubro de 2026 isso é PDT, logo a
janela corre de **07:00 UTC a 07:00 UTC**. As seis peças de 18/10 saíram entre
18:16 e 23:13 UTC, **todas dentro da janela que só fecha às 07:00 de 19/10**:

| | |
|---|---|
| usado na janela | 6 × 1.600 = **9.600 de 10.000** |
| sobra | **400 unidades** |
| um `videos.insert` | **1.600** |
| cabe? | **NÃO** |

**Logo a rodada das 00:07 não publicou, e isso é aritmética e não escolha** — a
sétima peça da janela levaria `403 quota`. Ontem a frota fechou o dia a **96% da
cota sem ninguém saber**, e uma peça a mais em qualquer rodada teria falhado.

**A REGRA OPERACIONAL QUE SAI DISSO, e ela é nova: a janela de cota vira às
07:00 UTC, não à meia-noite.** Rodada entre 00:00 e 07:00 UTC herda a cota do dia
anterior; se o dia anterior entregou seis peças, essas rodadas são de
**ENGENHARIA por aritmética**, e a produção volta às 07:0x. Isso não substitui a
contagem — **conte as peças da JANELA (desde 07:00 UTC), não do dia calendário**,
que é a mesma classe de erro do 771, onde o dia calendário apagava as últimas
horas.

**O que isto NÃO afirma:** que a cota deste projeto é 10.000. Esse é o padrão, e
extensão eu não consigo ler (uso de cota só aparece no console do Cloud). Se um
envio passar com a janela nesta conta, **é prova de que o projeto tem extensão** —
e aí o teto sobe e isto se relê.

**As duas saídas, e agora com a ordem decidida pela medição:** separar em três
projetos do Cloud multiplica por três **sem depender de aprovação de ninguém** e
passa na frente da extensão de cota, que depende de prazo do YouTube. As duas são
do dono, e a primeira é uma colagem de `YT_OAUTH_JSON` nova.
`tests/test_a_sonda_le_o_PROJETO_sem_vazar_credencial.py`, nove testes; o teto e
a janela em `tests/test_a_janela_de_cota_vira_as_07_UTC.py`.

### E ÀS 00:4x A SÉTIMA PEÇA DA JANELA PASSOU — O TETO DE 6/DIA CAIU

**Medido em 19/10 às 00:49:51 UTC, e é o discriminador que a seção acima
declarou:** *"Se um envio passar com a janela nesta conta, é prova de que o
projeto tem extensão — e aí o teto sobe e isto se relê."* Ele passou.

O `labtreinamento-s081` (`a5BV9xEQKvw`) foi publicado pelo `retomar.yml`
(run `39182513094`, job `117838091540`) com `::notice:: PUBLICADO` e **sem
`403 quota`**. Ele é a **SÉTIMA** peça da janela que abriu às 07:00 UTC de 18/10:

| | |
|---|---|
| peças na janela | 6 de 18/10 (18:16 a 23:13) + esta | **7** |
| custo, a 1.600 cada | | **11.200** |
| cota padrão de um projeto | | **10.000** |
| passou? | | **SIM** |

**Logo o projeto `777159180424` NÃO tem a cota padrão.** A aritmética de
`10.000/1.600` = 6 continua certa como conta; **o que estava errado era a
premissa de que a cota deste projeto é 10.000.** Eu declarei essa premissa como
não verificada ("extensão eu não consigo ler") e ela foi falsificada pela
produção, não por leitura de console.

**O que isto estabelece é um PISO, não um teto: a cota é ≥ 11.200**, isto é,
≥ 7 envios por janela na frota inteira. **E O PISO SUBIU DUAS VEZES NA MESMA
JANELA, por produção e não por leitura:** o `labtreinamento-s082` (`84ADS0YGdog`,
01:37:45Z) foi a OITAVA e o `epomeno-epipedo-s064` (`ANxWQYgtUAY`, 02:30:25Z) a
NONA — as duas sem `403 quota`. Logo **a cota é ≥ 14.400**, isto é ≥ 9 envios por
janela na frota. **E a DÉCIMA passou às 02:48:23Z** (`kolejny-poziom-s064`,
`GESLIl-iUeo`) **a DÉCIMA PRIMEIRA às 03:12:04Z** (`epomeno-epipedo-s065`,
`pHtvqUUN4G8`) **e a DÉCIMA SEGUNDA às 04:12:14Z** (`kolejny-poziom-s065`,
`cq2Ws82UsZI`), logo **a cota é ≥ 19.200** — doze envios a 1.600 numa janela, sem
nenhum `403 quota`.

**E ESSA CONTAGEM DE DOZE ESTAVA ERRADA PELA METADE — medido em 19/10 às 05:4x,
e o erro é de JANELA, que é o erro que esta mesma seção nomeia.** Eu contei as
peças a partir das 18:16 de 18/10 e escrevi *"ontem a frota fechou o dia em seis
peças"*, quando a janela abriu às **07:00 UTC** daquele dia. Varrido o
`docs/pendente/duracoes-a-medir.jsonl`, que grava toda peça publicada com
`youtube_id`, a janela de 18/10 07:00 a 19/10 07:00 tem **24 envios, 24 ids
DISTINTOS, nenhum repetido** — de `labtreinamento-s075` às 07:15 até
`labtreinamento-s083` às 05:19. **Logo o piso é ≥ 38.400 unidades**, não 19.200,
e as "seis peças de 18/10" eram as seis ÚLTIMAS de dezessete.

**E é o 771 outra vez, na direção que eu já havia corrigido:** eu escrevi, nesta
seção, *"conte as peças da JANELA (desde 07:00 UTC), não do dia calendário"* — e
então contei um SUB-INTERVALO da janela. A regra estava certa e eu não a apliquei
ao meu próprio número. O instrumento existia: a contagem sai de uma varredura do
parque, não da minha memória das últimas rodadas.

O teto verdadeiro segue desconhecido,
e quem o descobre é o primeiro `403 quota` numa rodada normal, que não custa nada
porque requisição recusada não consome cota. **O teto verdadeiro segue desconhecido**,
e dizer "agora são N" seria trocar um número suposto por outro. Quem o
descobre é a produção: o primeiro `403 quota` numa rodada normal marca o limite,
e isso não custa nada porque a requisição recusada não consome cota.

**E a consequência atinge DUAS coisas que eu disse ao dono:**

1. **a rodada das 00:07 de 19/10 NÃO precisava ter sido de engenharia.** Eu
   escrevi que ela "não publicou, e isso é aritmética e não escolha". **Era
   escolha**, tomada sobre uma premissa não verificada que eu apresentei como
   conta. A regra da janela de 07:00 UTC **continua valendo** — ela é sobre
   QUANDO contar, não sobre quanto cabe — e o que cai é o número 6;
2. **a decisão dele de "manter os 6 por enquanto" foi tomada sobre esse
   número.** Ela fica retratada aqui para que a rodada seguinte não a use como
   teto: o que ele decidiu foi não perseguir a divisão em três projetos nem o
   formulário de extensão, e **essas duas seguem desnecessárias por outro
   motivo** — o projeto já tem extensão.

**O que NÃO cai:** que os três canais compartilham o projeto `777159180424`
(medido, job `117829119323`), e que a janela vira às 07:00 UTC. As duas seguem.

`tests/test_a_SETIMA_peca_da_janela_passou.py`.

### E A PEÇA DE 5 s É O PRIMEIRO PONTO DESSA FAIXA — pedido do dono em 19/10

Palavras dele: *"produza e publique vídeo teste, mas de alta qualidade e
performance, narração e poste agora. Vídeo de até 5 segundos."*

O `labtreinamento-s081` tem **duas cenas**, `short_alvo_s: [3.0, 6.0]` declarado
NA SPEC (o campo do formato de 2 min, de 16/10), previsão edge **4,37** e piper
**3,59** — e **5 s REAIS**, lidos com o controle `OhrGlJvnBoM` conferido em 44 s
na mesma chamada. Provedor **edge** MEDIDO (zero avisos no job `117837682861`).
Som `-14,1` LUFS, pico `-3,2` dBTP, zero silêncios. **2,2 s por plano**, mais
rápido que os 3,1 s da cadência medida.

**O resíduo é +0,63 e o SINAL NÃO ESTÁ ESTABELECIDO:** real 5 significa duração
verdadeira em `(4; 5]`, e a previsão de 4,37 cai DENTRO desse intervalo. Pelo
critério do 770 com a borda do 18/10, `5 − 4,37 = 0,63 < 1,0`.

**E ele NÃO entra na série do `mira.py`**, que é construída em peças de 23 a 44 s:
somar um ponto de 4,4 s ali é o erro de enquadramento do 679/698/725, o mesmo
motivo pelo qual a peça de 2 min (+4,8) ficou de fora. **Nesta faixa a banda tem
UM ponto, e ele é este.** `RESIDUO_N` segue 105.

**NADA de parâmetro mudou (§10):** `ALVO_SHORT` (41,5 a 43,0) e
`ALVO_POR_CANAL` do canal (20,0 a 26,0) estão intocados, e é por isso que o
`mira.py` reprova esta peça pelo PISO — esperado, porque ela declarou outra
faixa. O que ela testa é formato, e o veredito de desempenho dela é view, que
ainda não existe.

## EU DISSE AO DONO QUE "LONGO NOVO NÃO É POSSÍVEL" — E A GENERALIZAÇÃO ERA MINHA

**Retratação de 19/10 às 00:4x, provocada por uma CAPTURA DE TELA do dono** — a
aba *Vídeos* do `labtreinamento` no Studio, que é a lista de LONGOS.

Eu havia respondido que *"não consigo fazer longo novo hoje"*, pela regra 600
(número sobre o mundo exige duas fontes institucionais, e os quatro hosts estão
em 403 no proxy). **A frase está certa para UMA classe de longo e eu a escrevi
para TODAS.**

**O que a tela mostra, e é medição dele, não minha:**

| vídeo | duração | data | views |
|---|---|---|---|
| PROCV ou PROCX: qual usar no Excel | **8:51** | 14/out | 14 |
| Vale-Transporte: 6% de Qual Salário? | **8:40** | 7/out | 33 |
| Treinamento Cotado por Turma | **8:31** | 7/out | **0** |
| *Twoja Pierwsza Rata Jest Niższa* (POLONÊS) | — | 7/out | **79** |

**Duas coisas que eu não tinha juntado:**

1. **Os dois de 7/out são NOSSOS** — o de 8:40 é o `labtreinamento-013`
   (conferido: a copy dele é literalmente *"Vale-Transporte: 6% de Qual
   Salário?"*). Logo **a máquina já publica longo de ~8 min, inteiro e online**,
   e a pergunta do dono (*"é possível … de forma online sem ser pelo
   terminal?"*) já tinha resposta publicada no canal dele.
2. **O de 14/out é DELE, não nosso.** O `FtCtIJPsc_Q` não é nenhuma spec de longo
   do disco: ele aparece **só como ORIGEM** de treze shorts nossos (`s058` a
   `s070`). É a peça que eu medi quadro a quadro em 16/10 e chamei de "a
   REFERÊNCIA" — e ela é referência porque é **feita à mão pelo dono**, com o
   trilho de capítulos e os cinco layouts que o `layout.py` não tem. Eu escrevi
   "a distância são três coisas" sem dizer, em letra, **de quem é a peça do outro
   lado da distância.**

**A REGRA QUE SAI DISSO, e ela destrava a metade LONGA do pedido de 16/10:**
a trava de fonte é por **TIPO DE CONTEÚDO**, não por formato. Longo que carrega
número do mundo que MUDA (os 6% do vale-transporte, alíquota, prazo) exige as
duas fontes e segue bloqueado. **Longo de PROCEDIMENTO ou FERRAMENTA — PROCV
contra PROCX, uma função de planilha, um passo de cálculo — não carrega número
desses e não depende de fonte nenhuma que o proxy bloqueie.** O `-013` é do
primeiro tipo; o PROCV é do segundo.

**O que isto NÃO autoriza:** inventar número. A regra (g) continua valendo, e
longo de procedimento que escorregar para "a alíquota é X" volta a precisar das
duas fontes.

**E um achado da própria tela, que é do dono e não da máquina:** o
`Twoja Pierwsza Rata Jest Niższa` é **polonês e está no canal pt-BR**, com
**79 views — mais que os três brasileiros somados (47).** É o `QiaGg03WSR0`, o
mesmo id que em 18/10 o `origens_sem_uso` me ofereceu como pauta e que eu recusei
quatro vezes por idioma. A tela confirma, por fora, o que a medição dizia. **Não
mexi nele** — mover ou apagar vídeo publicado exige o dono.

## O PROCESSO DE PRODUÇÃO QUE O DONO PEDIU EM 16/10 — E AS TRÊS ROTAS QUE ABRIRAM

Palavras dele: *"crie próximo vídeo melhor de 2 min agora e publique, thumbnail,
e outras melhorias. Busca monetização dos canais"* e, em seguida, *"insira este
processo de produção na rotina, com estilo, narração, modelo para todos os canais
de cada idioma. pelo menos 2 vídeos por dia por canal, 1 vídeo longo e outro
curto"*.

**ESTÁ EM `docs/ROTINA.md`, §6-bis. E O PROMPT DO TRIGGER ESTÁ ATRÁS DO ARQUIVO** —
o corpo mede 64.891 bytes (md5 `45d3629f36fb70a409e8ddede25f7e54`) e o
`update_trigger` exige o texto inteiro como argumento, o que é o mesmo tipo de
passo que matou três runs no `estado_b64`. **Enquanto a sincronia não for feita,
é esta seção que governa** — e ela é lida primeiro por ordem do próprio prompt.

### O SANDBOX DO COMPOSIO TEM SAÍDA PARA A INTERNET, e isso derrubou TRÊS bloqueios

**E AS TRÊS ROTAS NÃO SÃO CAPACIDADES, SÃO ESTADOS — medido em 16/10 às 07:1x,
quatro horas depois de eu as abrir.** Eu escrevi esta seção como se fossem
propriedades do sandbox. Sondadas uma a uma na rodada seguinte:

| rota | 03:3x | 07:1x | como falha |
|---|---|---|---|
| inscritos (`/channel/<UC…>/about`) | abre | **abre** | — |
| duração (`/watch?v=` → `lengthSeconds`) | abre | **FECHA** | HTTP **200**, 1,2 MB, **zero** `lengthSeconds`, marcador `CONSENT` |
| legenda (`yt-dlp`) | abre | **FECHA** | *"Sign in to confirm you're not a bot"* |
| fontes institucionais | abre | **abre** | Eurostat 200, Sejm 200 |

**E EM 16/10 ÀS 12:2x A TABELA GANHOU UMA QUINTA LINHA, e ela é a pior:**
`youtube.com/channel/<UC…>/videos` (a LISTAGEM de uploads) devolveu **200 com
1.196.398 bytes e ZERO `videoRenderer`**, cinco marcadores `CONSENT` e um
`captcha` — enquanto `/about` (inscritos) e `/watch?v=` (duração, **dois**
`lengthSeconds`: 530 e 531, use o maior) responderam na mesma rodada. **A rota
que resolve é `yt-dlp --flat-playlist` na playlist `UU…`** (o id do canal com
`UC` trocado por `UU`), que devolve a ordem VIVA **com duração**, logo separa
longo de short numa leitura. Está em `fabrica/recencia.ordem_viva` /
`topo_de_pauta`, com oito testes — e o primeiro deles exige que saída vazia
**LEVANTE** dizendo `AUSENCIA DE LEITURA`, porque é aí que o 200-sem-campo
reaparece disfarçado de canal vazio.

**E EM 16/10 ÀS 17:2x AS QUATRO ROTAS FORAM SONDADAS NO MESMO MINUTO, e elas
DIVERGEM — o estado é por ROTA, não do sandbox.** Eu media uma rota por rodada,
pela rota de que precisava, e atribuía o resultado ao ambiente: isso sustentava,
sem dizer, a hipótese de uma **maré** que sobe e desce com todas juntas. Na mesma
chamada de bash, mesma sandbox: `/about` **ABRE**, `/watch?v=` **ABRE** (fechada
às 07:1x), `yt-dlp` legenda **ABRE** (fechada às 07:1x), e a LISTAGEM **FECHA** —
200 com 1.132.822 bytes, **zero** `videoRenderer`, um `CONSENT` e um `captcha`.

**Logo sondar uma rota NÃO informa sobre as outras**, e não existe "a maré do
ambiente" para consultar. As duas que fecharam às 07:1x voltaram **juntas**, e a
que fechou às 12:2x segue fechada 4,5 h depois — estado de rota tem duração
própria. **O que isto NÃO prova:** independência; três pontos no tempo e uma
sonda simultânea não medem correlação, e duas voltarem juntas é compatível com
dependência parcial. O que está medido é a negação.
`tests/test_as_rotas_nao_sobem_e_descem_JUNTAS.py`, sete testes — e o primeiro
assert que eu escrevi nele terminava em `or True`, isto é, passava com qualquer
tabela: **portão verde fabricado, §3.8, num arquivo escrito para guardar essa
lição.** Consertado com contraprova nos dois sentidos.

**E EM 17/10 ÀS 03:1x A ROTA DA DURAÇÃO FECHOU DENTRO DA HORA — e eu ia culpar
a peça.** O `kolejny-poziom-s049` (`O5o2SnovdEo`), publicado dois minutos antes,
devolveu **200 com 1.219.721 bytes e ZERO `lengthSeconds`**, cinco `CONSENT` e
dois `captcha`. Sozinha, essa leitura é **indistinguível** de peça que ainda não
indexou, que é o caminho normal do 672/758 — e era isso que eu ia relatar.

**O discriminador é uma peça de CONTROLE cujo valor eu já medi.** Na mesma
chamada eu reli o `OhrGlJvnBoM`, que havia lido **44 s** uma hora antes: ele
também voltou **vazio**. Peça de uma hora de vida não desindexa, logo o que mudou
foi a **ROTA** — e ela estava ABERTA às 02:1x e às 01:1x da mesma madrugada.

**A consequência vai dita em vez de estimada: não existe ponto de resíduo na
rodada das 03:06.** `fabrica/vivacidade_publica.veredito_da_rota` /
`relato_da_rota`, e `tests/test_a_rota_fechada_parece_peca_nao_indexada.py` com
nove testes — um deles a contraprova no outro sentido (controle responde → a
leitura vazia é da peça, e aí o 672 se aplica), sem a qual o veredito seria
sempre o mesmo.

**A regra que fica: antes de ler leitura vazia como defeito da peça, releia uma
peça de CONTROLE cujo valor você já conhece.**

**E EM 18/10 ÀS 01:2x A PLAYLIST `UU…` MOSTROU-SE INCOMPLETA — e ela é a base da
"ordem VIVA" que eu escrevi em 16/10.** O `yt-dlp --flat-playlist` na playlist
de uploads do `labtreinamento` devolveu **treze** longos. Dois outros,
`StQNFMdpGdk` (872 s) e `XgqPVJuAk3o` (785 s), foram **medidos** como longos do
mesmo canal (`author` LabTreinamento) e **públicos** (`isUnlisted: false`) — e
**não aparecem na playlist**. Logo o canal tem ao menos **quinze**, não treze.

**O que isto retrata:** eu escrevi que a playlist *"devolve a ordem VIVA"* e a
usei como se fosse o CONJUNTO. Ela dá uma **ordem**; não dá o conjunto completo.
A nota de 16/10 segue valendo para separar longo de short e para ordenar por
recência — e **não** vale para dizer "estes são os longos do canal".

**E A OMISSÃO *VARIA ENTRE LEITURAS* — medido em 18/10 às 07:0x, três horas
depois.** A mesma playlist do `labtreinamento` devolveu **DOZE** longos, não
treze: o `KRUERlNPzDw` saiu. Ele é **público** (`isUnlisted` e `isPrivate`
falsos), do mesmo canal (`author` LabTreinamento), 823 s, e **já rendeu quatro
shorts** — não é origem desconhecida. Nada foi publicado nem despublicado entre
as duas leituras.

**Logo eu estava tratando a omissão como um conjunto FIXO** (*"ela omite esses
dois"*), e ela não é. O que isto **não** prova: a causa, nem que a omissão seja
aleatória — duas leituras não medem distribuição. O que está medido é a negação.

**E a consequência bate na regra de 16/10** (*"a pauta serve o longo MAIS NOVO
primeiro"*): o rank de uma origem, e a própria presença dela, mudam de uma rodada
para a outra sem nada ter acontecido no canal. Logo **a ordem viva ORDENA, não
ENUMERA**, e a contagem de longos que ela devolve é um **PISO** em qualquer
leitura. Antes de dizer que uma origem não existe mais, leia a PÁGINA dela.
`tests/test_a_omissao_da_playlist_VARIA_entre_leituras.py`, sete testes — um
deles **falha se as duas leituras voltarem a coincidir**, para que isto seja
relido em vez de apagado, e um impede que esta nota apague a de 01:2x.

**E ela me deu DOIS falsos positivos na primeira execução de um detector novo.**
A primeira versão de `concentracao.origem_de_outro_canal` acusava a origem
**ausente** da playlist, e acusou exatamente esses dois — origens legítimas do
próprio canal. Reescrita para exigir **dono MEDIDO** (`{id: canal}`, do campo
`author` da página), e origem fora do mapa **não entra**: desconhecido não é "de
outro canal". É a regra do 725 — detector que inventa achado é pior que não ter
detector — pega antes de relatar.

**E A ORIGEM DE ZERO USOS ERA INVISÍVEL PARA QUEM ESCOLHE PAUTA.** A
`concentracao.contagem` conta origem **USADA**, logo origem com zero shorts
simplesmente não aparece nela — e é a de maior valor editorial. O
`QiaGg03WSR0` (rank 4 da ordem viva do `labtreinamento`) não rendeu short nenhum
e nunca foi oferecido. **É a cegueira do 762/771 na terceira direção**, e a pior
das três. Agora `concentracao.origens_sem_uso(canal, ordem)` a nomeia — e avisa
que **lista vazia não prova ausência**, porque a playlist omite longo.

**E DOIS SHORTS DO KOLEJNY DECLARAM ORIGEM DE OUTRO CANAL.** O
`kolejny-poziom-s004` e o `-s035` trazem `longo_existente: QiaGg03WSR0`, que é
**longo do LabTreinamento** — enquanto as FONTES das duas dizem que a origem é o
`kolejny-poziom-018`. Logo **o ID está errado, não o conteúdo**: os dois shorts
são poloneses e sobre crédito. Custa em dois lugares: a contagem credita ao
kolejny uma origem que não é dele, e o `videos.origem_id` dessas peças marca como
consumida a origem **errada**, logo a trava do 670 fica cega na verdadeira.
**Não corrigi o id**, porque o id certo do `kolejny-poziom-018` não está no
retrato de 06/10 e sem `execute_sql` eu não o resolvo sem adivinhar.
`tests/test_a_origem_de_zero_usos_e_invisivel.py`, dez testes — um deles **falha
se a nota do falso positivo for apagada**, porque é ela que impede a repetição.

**E O INSTRUMENTO DE ZERO USOS CONTAVA ID, NÃO TÍTULO — medido em 18/10 às 03:1x,
na PRIMEIRA vez que ele teve o que dizer.** No `kolejny-poziom` ele devolveu
**SEIS** origens de zero usos (ranks 16 a 20 e 22 da ordem viva) — e as **seis
têm o MESMO título**, medido na página de cada uma. São cópias, do grupo das 46
duplicatas. **Por TÍTULO DISTINTO eram ZERO origens novas, não seis.**

**E o efeito (C-2) da rotina nomeia isso desde o 658** — contar por id premia
duplicata — e eu escrevi o instrumento **sem a guarda, duas horas depois** de
escrever outro que também precisou de uma. Agora `origens_sem_uso` aceita
`titulo_de` e colapsa grupo de cópias no primeiro id da ordem; **título
desconhecido NÃO colapsa com nada**, porque isso inventaria duplicata. E
`copias_colapsadas` diz o tamanho da inflação — cinco, neste caso.
`tests/test_origem_sem_uso_contava_ID_e_nao_TITULO.py`, dez testes, com
contraprova nos dois sentidos.

**E NA PRIMEIRA VEZ QUE ELE ESCOLHEU PAUTA, A ORIGEM QUE ELE DEVOLVEU ERA DE
OUTRO IDIOMA — medido em 18/10 às 04:1x.** No `labtreinamento` o
`origens_sem_uso` com o mapa de títulos devolveu **UMA** origem:
`QiaGg03WSR0`, rank 4 da ordem viva — e o título dela, lido na própria playlist
de uploads **daquele** canal, é **POLONÊS** (*"Twoja Pierwsza Rata…"*, sobre
crédito). É o mesmo id que a nota de 01:2x já mostrava declarado por dois shorts
do kolejny.

**Logo o instrumento está CERTO e a origem NÃO SERVE ao canal, e isso é duas
coisas, não uma.** Short pt-BR dela reprovaria a identidade (601). Este é o modo
de falha mais caro que existe aqui: **o instrumento está VERDE e seguir a
resposta dele produz peça de idioma errado.** Não filtrei idioma dentro dele, e o
motivo vai escrito no módulo: filtrar **esconderia** a origem em vez de a nomear,
que é exatamente a cegueira do 762/771 que ele nasceu para desfazer.

**A regra que fica: origem devolvida não é origem utilizável — confira o IDIOMA
do título antes de escrever.** `tests/test_a_origem_de_zero_usos_e_de_outro_IDIOMA.py`,
seis testes, com contraprova nos dois sentidos (origem pt-BR de zero usos
continua saindo) e um que **falha se a nota do idioma for apagada do módulo**.

**E a pauta desta rodada foi ao rank 2 por isso**, não ao rank 1: o topo do canal
está em **DOZE** usos — o hábito de 13/10 outra vez, agora visível na contagem
**antes** de escolher.

**E DUAS HORAS DEPOIS ESSA REGRA QUASE ME FEZ FABRICAR UM ACHADO, porque ela não
dizia ONDE ler o idioma — medido em 18/10 às 06:1x.** O `yt-dlp --flat-playlist`
na playlist do `kolejny-poziom` devolveu os **quatro** longos mais recentes com
título em **INGLÊS** (*"Renting or a Mortgage?"*, *"Child Tax Credit"*, *"Real
Estate Tax"*, *"PPK: What Your Contribution Really Costs"*). Pela regra acima
isso se lê como "o topo de um canal polonês está em idioma errado", e era o que
eu ia relatar.

**Era o INSTRUMENTO: o título da playlist pode ser uma LOCALIZAÇÃO.** A chamada
não levava locale, e o YouTube serve o título traduzido. Lidos na página com
`Accept-Language: pl-PL`, os dois primeiros são poloneses — *"Wynajem czy
Kredyt?"* e *"Ulga na Dziecko"*.

**E a nota de 04:1x SOBREVIVEU à conferência, o que é sorte e não método:** o
`QiaGg03WSR0` devolve o **mesmo** título polonês com `Accept-Language` pt-BR,
pl-PL **e** en-US, e o `yt-dlp -J` declara `language: pl`. Logo a conclusão
daquela rodada está certa e a origem segue inutilizável no canal pt-BR — mas o
caminho que a produziu não garantia nada, e na rodada seguinte ele errou.

**A regra ganha o ONDE, que é a parte que faltava: título de playlist NÃO
estabelece idioma.** O discriminador é o campo `language` do próprio vídeo, ou o
`<meta name="title">` lido em mais de um `Accept-Language` — se não muda, é o
original. E **não** filtrei idioma dentro do instrumento, agora com um segundo
motivo além do 762/771: o campo que ele teria à mão é justamente o que o YouTube
localiza. `tests/test_o_titulo_da_playlist_pode_ser_LOCALIZACAO.py`, sete testes,
com contraprova nos dois sentidos.

**E UM TESTE MEU DE 12/10 REPROVOU NA MESMA RODADA, e a retratação é dele.** O
`test_as_TRES_origens_do_falso_positivo_devolvem_None` cobrava `None` para as
três origens do falso positivo do `segundo_angulo`, e o `SP7Vz8qHdRY` passou a
resolver para `kolejny-poziom-011`. **Conferido: a resolução está CERTA** —
aquele pacote tem **77** cenas de longo, e foi dele que saiu o
`kolejny-poziom-s057`. O que mudou foi a **convenção ter sido seguida**: o
`pacote_do_id` resolve pela copy do short que declara a origem, e a copy do
`s057` nomeia o pacote nas FONTES. **O docstring da própria função sempre disse
isso** — *"devolve None quando a convenção não foi seguida"* — logo `None` era
retrato de estado, não propriedade.

**A propriedade do falso positivo era OUTRA, e é ela que ficou cobrada:** o erro
de 12/10 era resolver para o **SLUG do canal** (dez cenas). O teste passou a
exigir "não é slug" e "tem ao menos 20 cenas de longo" — o limiar observado
daquela medição —, mais uma contraprova de que as outras duas seguem em `None`.
**Mesma classe do 743/753/761: eu travei identidade onde havia propriedade.**

**E EM 17/10 ÀS 09:0x EU QUASE DECLAREI A ROTA DOS INSCRITOS FECHADA — e o que
estava errado era o meu GREP.** Eu sondei os três canais com
`grep -o '"subscriberCountText":{[^}]*}'` e os três voltaram **VAZIO**. Pela
tabela de rotas isso se lê como fechamento, e era o que eu ia relatar. Abrindo a
página (1.189.592 bytes, **um** `CONSENT`, dois `captcha`), o campo
`subscriberCountText` está lá **uma vez** e o valor sai por
`grep -o -E '"[0-9,.]+ (inscritos|subscribers)"'`: **68 / 21 / 8**. A rota estava
ABERTA.

**A regra que fica é a do OCR, aplicada à rota: instrumento que devolve vazio não
prova ausência — confira o PADRÃO antes de culpar a rota.** O discriminador é
barato e é o mesmo do controle: contar o campo na página crua em vez de confiar na
primeira expressão que eu escrevi. A forma do JSON do YouTube muda; o texto
legível ("N inscritos") sobreviveu a todas as rodadas.

**E EM 17/10 ÀS 20:1x A FRASE "N DE N ACIMA" CAIU, e o que a derrubou foi um
critério MEU que só olhava um lado.** O `epomeno-epipedo-s054` (`A4M3SLs8FEk`)
previa **41,6** no edge — provedor MEDIDO, zero avisos no job `117492664194` — e
saiu com **41 s reais**: resíduo **−0,6**, o primeiro NEGATIVO em 78 pontos.

**E o sinal dele ESTÁ estabelecido, ao contrário do que o `duracao_a_medir` dizia.**
O YouTube arredonda **para cima**, logo real 41 significa duração verdadeira em
`(40; 41]`, e 41,6 está **acima de todo** esse intervalo: o resíduo verdadeiro
vive em `(−1,6; −0,6]` e é estritamente negativo. O critério do 770 era
`real − previsão > 1,0` — ele estabelece só o lado **positivo**, porque foi
escrito quando todos os pontos eram positivos, e **um critério sem o ramo que
falta devolve "não sei" onde a aritmética sabe.**

Agora `_sinal` devolve `+1`, `−1` ou `0`, com os dois ramos: positivo exige
`real − previsão > 1,0`, negativo exige `real − previsão < 0`, e entre os dois o
intervalo contém zero. `RESIDUO_OBSERVADO` foi a **(−0,6; 4,0)** — sexta correção
da banda, e a primeira que muda o SINAL do piso. `RESIDUO_N` = 78.

**O que isto derruba, e vai dito em vez de escorregar:** a frase *"N de N acima"*,
que eu venho escrevendo desde o 734, **não vale mais**. O que sobrevive é mais
fraco e verdadeiro: a série é dominada por resíduo positivo, e o negativo é raro.
**E o ponto caiu dentro da janela estreita do 768/769** — previsão variando menos
de 1 s produzindo real espalhado para os **dois** lados, que é exatamente o que
aquela nota afirma.

**Dez testes meus reprovaram com isso, e os dez eram afirmação minha, não
limiar:** quatro cravavam `RESIDUO_OBSERVADO == (0,0; 4,0)` por identidade
(743/753/761), três cobravam `real − previsão >= 0` em toda a série, um cravava a
largura em 4,0, um escrevia a faixa `"25.6 e 29.6"` à mão dentro do teste — o
defeito do 753 **aplicado ao próprio teste** — e dois do `pauta_viva` ancoravam
num **id vivo** (`eZ697VNYCPU`) que esta mesma rodada consumiu. Os dois últimos
passaram a **derivar** o id da contagem viva e a dizer quando não existe nenhum.
`tests/test_o_sinal_tambem_se_estabelece_para_BAIXO.py`, oito testes — e o
primeiro que eu escrevi nele **proibia a string** "N de N acima" no módulo, o que
proibiria também a própria retratação; corrigido para cobrar a QUEDA ao lado da
frase.

**A regra que fica: critério de sinal tem DOIS ramos, e quem escreve um só o
escreve no lado em que está olhando.**

**E O SEGUNDO NEGATIVO VEIO NA PEÇA SEGUINTE, no MESMO ponto da janela.** O
`epomeno-epipedo-s055` (`Gxg3npta4Zo`) previa **41,5** no edge — provedor MEDIDO,
zero avisos no job `117529604557` — e saiu com **41 s reais**: resíduo **−0,5**,
estabelecido pelo ramo novo, **dentro** da banda (o piso segue −0,6). `RESIDUO_N`
= 81.

**O que ele acrescenta não é a contagem, é o LUGAR:** os **dois** negativos são
do `epomeno-epipedo`, com previsão **41,5 e 41,6** e real **41** — isto é, o
negativo não está espalhado pela série, está concentrado num ponto da janela de
previsão. **E é a mesma janela de 0,4 s do 768/769**, onde a previsão não ordena
nada contra um real de passo 1 s: ali os reais já iam de 41 a 44. Logo o negativo
é o quarto inteiro dessa janela aparecendo, não um regime novo.

**O que eu NÃO afirmo:** que a voz grega produza resíduo negativo. São dois
pontos, do mesmo canal e da mesma faixa, e o 679/698/725 nomeia exatamente esse
enquadramento. O que está medido é que **o negativo existe, é raro (2 de 81) e
mora na janela estreita.**

**E O TERCEIRO NEGATIVO VEIO EM 18/10 ÀS 05:1x, e o que ele acrescenta é o
ESPALHAMENTO, não a contagem.** O `epomeno-epipedo-s057` (`04U8EeDbx_Q`) previa
**41,4** no edge — provedor MEDIDO, zero avisos no job `117593154113` — e saiu com
**41 s reais**: resíduo **−0,4**, estabelecido pelo ramo negativo e **dentro** da
banda (o piso segue −0,6). `RESIDUO_N` = 87.

**Os três negativos são do `epomeno-epipedo` e as três previsões caem em 0,2 s —
41,4, 41,5 e 41,6.** Isso parece um padrão de canal, e é por isso que vai com a
ressalva: **na MESMA janela este canal já deu 42, 43 e 44**, logo o que está
medido não é "o grego encurta", é que **o real desta janela espalha agora por
QUATRO inteiros (41 a 44) contra meio segundo de previsão.** É o 769 com uma
unidade a mais de espalhamento, e ele fica mais verdadeiro, não menos.

**E ela foi escrita mirando o PISO de propósito, pela regra de redação do 772 — e
a exposição que eu declarei não foi a que ocorreu.** A copy dizia, antes de
publicar, que *"se o edge narrar, o real deve cair entre 40,8 e 45,4 s, logo PODE
encostar no teto de 45"*. O real saiu **41**, isto é, no extremo OPOSTO da faixa
anunciada. **Acertar dentro de uma banda de 4,6 s não é previsão**, e declarar o
lado errado dela de propósito é o que prova isso: a banda cobre os dois extremos
com igual conforto, que é exactamente a perda de utilidade que o 774 nomeia.

**E ÀS 04:1x A ROTA SEGUIA FECHADA, com a sonda feita ANTES de prometer.** O
controle (`OhrGlJvnBoM`, 44 s medidos) voltou vazio outra vez, e com ele o
`labtreinamento-s066` recém-publicado. **Duas peças seguidas sem ponto de
resíduo** — a série do 739 parou de crescer por falta de instrumento, não de peça.

**E isso virou ARQUIVO, porque em 16/10 as dezessete durações parqueadas saíram
da minha CABEÇA e não de um instrumento.** `fabrica/duracao_a_medir.py` grava uma
linha JSON por peça em `docs/pendente/duracoes-a-medir.jsonl`, e **o campo que
carrega o risco é o PROVEDOR: ele é obrigatório na gravação.** O aviso
`::warning::NARRACAO PELO PIPER` vive na anotação do JOB, e anotação envelhece —
parquear sem o provedor obrigaria a rodada futura a **inferir** qual mundo narrou
pela distância entre previsão e real, que é exatamente o erro que o 733 nomeia e
que me custou três rodadas. O módulo **levanta** citando o 733 em vez de aceitar.
`residuos()` compara contra a previsão do provedor GRAVADO e aplica o critério do
770; ausência de leitura sai `None`, nunca zero.
`tests/test_a_duracao_nao_medida_fica_PARQUEADA.py`, dez testes.

**E ÀS 06:1x O PARQUEAMENTO VIROU INCONDICIONAL, pela assinatura do 726.** O
passo dependia de eu **notar** que a rota estava fechada: com ela aberta eu meço
na hora e não parqueio nada, logo o parque só recebia peça nas rodadas em que eu
lembrava de olhar o estado — que é exatamente a condição em que eu esqueço passo
(o corpus parou sete rodadas assim). Agora **toda peça publicada entra** e a
medição vem depois por `resolve(youtube_id, real)`; o arquivo é o **log** dos
pontos, e o pendente é o que ele ainda não resolveu, não o que eu anotei.
**Reescrever com valor DIFERENTE levanta** apontando a peça de controle, porque
duração de peça publicada não muda e duas leituras discordantes são da ROTA. E o
cabeçalho do `relato` dizia *"esperando duração REAL"* com tudo resolvido — relato
falso, pego na primeira execução e consertado para contar os dois baldes. Dezessete
testes.

**A rota da duração falha com 200 e página grande**, logo quem não contar o campo
lê "funcionou". Cookie `CONSENT=YES+1`, `User-Agent` de navegador e `&hl=en` **não
resolvem** — testados os três. O `oembed` segue em 200, e dá título, não duração.

**Três consequências:**
1. **A banda do resíduo volta a não ter instrumento** — o `s040` e o `s041`
   ficaram sem duração real medida, e eu havia anunciado que leria a do `s040`
   nesta rodada. Fica dito em vez de sumir;
2. **a regra (h) fecha outra vez**, e com ela a pauta de origem sem spec local;
3. **a pauta de origem COM spec local continua aberta, e o atalho é o retrato da
   ponte:** `fabrica/ponte/videos.json` mapeia `youtube_id → pacote`, logo a
   origem de um short vira o `epomeno-epipedo-0NN.json` com os capítulos no
   disco. **Isso NÃO é usar o retrato como estoque** — aquilo é o erro retratado
   em 12/10; é usá-lo como tabela de ids de peça ANTIGA, que é o que ele é.

**A regra que fica, e ela é a do 11/10 ao contrário: rota medida como aberta é
ESTADO, não propriedade.** Lá eu tratei indisponibilidade como permanente; aqui
eu tratei disponibilidade como permanente. **Sonde antes de prometer, e conte o
CAMPO, não o código HTTP.**

Medido em 16/10 às 03:3x–03:4x com `COMPOSIO_REMOTE_BASH_TOOL`. **O proxy DESTA
sessão nega o youtube.com; o sandbox não.** Sonde-o antes de dizer que não há
rota — eu reportei estes três como bloqueados por **dezessete rodadas**.

1. **MEDIR, sem Supabase.** `https://www.youtube.com/watch?v=<id>` →
   `"lengthSeconds"` e `"viewCount"`; `/channel/<UC…>/about` com
   `Accept-Language: pt-BR` → inscritos. **A página traz DOIS `lengthSeconds`
   diferentes** (43 e 44 na mesma peça): use o MAIOR, porque a banda foi
   construída sobre `contentDetails.duration`, que arredonda para cima. **Não dá
   retenção nem `subscribersGained`** — isso é Analytics, e segue na pendência 1.
2. **A REGRA (h), sem `pg_net`.** `pip install -q yt-dlp` e
   `yt-dlp --write-subs --write-auto-subs --sub-langs 'pt-BR,pt' --skip-download
   --sub-format vtt`. O `timedtext` direto volta **vazio** (o YouTube passou a
   exigir token); não insista nele. Foi assim que o `FtCtIJPsc_Q` virou pauta:
   71 KB de VTT, **1.381 palavras**, e nenhuma frase do short saída de TÍTULO.
3. **AS FONTES INSTITUCIONAIS respondem:** `api.sejm.gov.pl` e
   `ec.europa.eu/eurostat/api` devolveram **dado real**, `www.statistics.gr` 200,
   `www.gov.br` 301. **LONGO NOVO voltou a ser possível**, e a regra 600 (duas
   fontes que batam) volta a ser cumprível — logo o pedido de 1 longo/dia por
   canal deixa de ser promessa vazia. Isto RETRATA o que eu escrevia aqui: que o
   402 bloqueava o refil da pauta.

### O que a primeira leitura em dezessete rodadas disse

Inscritos em 16/10 às 03:3x contra 15/10 às 07:13, **20,4 h**: **68 / 20 / 8**,
delta **zero** nos três, e o piso de resolução da janela é 1,18/dia. **Isso
derruba o "+1,79 inscrito/dia" da frota que eu carregava desde 12/10** — ele
preveria ~1,5 inscrito nessa janela. Delta zero não estabelece ritmo: estabelece
um **limite superior**, e a frota anda **abaixo de 1,18/dia**.

E as **dezessete durações reais** parqueadas saíram todas: resíduo **+0,4 a
+2,9 s**, dezessete de dezessete positivos, todas dentro da banda. **Não atualizei
`RESIDUO_N`**, porque o provedor só está medido em quatro delas e comparar contra
o mundo `edge` sem contar os avisos é o erro que o 733 nomeia.

### O FORMATO DE 2 MIN, e o limite que morava em DOIS lugares

`labtreinamento-s058` = `8DVWFC5agrg`, **124 s reais**, 40 cenas, **3,1 s por
plano** (a cadência medida em 690/699), com **capa própria** — a primeira peça da
frota com capa desenhada, e o 403 que eu previa por canal não verificado **não
veio**.

**A faixa do short agora é POR SPEC: `short_alvo_s: [piso, teto]`, e sem o campo
vale a da frota (18 a 45 s)** — logo nenhuma spec antiga muda de julgamento, e
isso tem contraprova em teste. A fonte é **única**: `ensaio.faixa_do_short(sp)`.
**Teto absoluto 180 s**, porque acima disso o YouTube deixa de tratar a peça como
Short e o único caminho de monetização ainda vivo (3 M de views/90 d) depende
dessa classificação.

**Por que a fonte é única: eu mudei o portão e esqueci o render.** O run
`38847013520` passou os doze portões, montou o `short.mp4`, subiu o artefato de
4,9 MB — e morreu em `etapas.py:377`, num `assert 20 <= ds <= 60` cravado à mão,
**depois** de o arquivo existir. Mesma regra, dois donos, um atualizado. A peça
foi publicada do artefato daquele run.

**E a falha deu de graça a primeira medição real do formato:** previsão edge
**118,8** → real **124** (ffprobe 123,6), resíduo **+4,8 a +5,2 s**, acima do
teto de 4,0 da banda. **Mas a banda foi construída em peças de 23 a 44 s**, e
aplicá-la aqui seria o erro de enquadramento do 679/698/725. O que eu afirmo é só
o limite: **nesta faixa de duração não existe banda medida, e o primeiro ponto
dela é +4,8 s.**

### RITMO E MODELO POR CANAL

**Alvo: ao menos DOIS por canal por dia — UM LONGO e UM CURTO**, seis na frota. O
longo gera pauta, satisfaz os 3 uploads/90 d e converte ~5x melhor por view; o
curto entrega alcance em canal frio. **Rodada que só consegue uma peça diz QUAL
faltou e por quê.** O teto automático de 1/dia/canal segue sendo pendência 4.

| canal | idioma | voz (edge) | R | P | trilha | mira |
|---|---|---|---|---|---|---|
| labtreinamento | pt-BR | Thalita Multilingual | 17,47 | 0,737 | Inspired | 20,0–26,0 REAL |
| epomeno-epipedo | el | el-GR-Nestoras | 20,61 | 1,273 | Inspired | 41,5–43,0 |
| kolejny-poziom | pl | pl-PL-Marek | 20,07 | 1,419 | **Wholesome** | 41,5–43,0, mire o PISO |

**Nunca copie trilha nem paleta de outro canal** — eu levei reprovação do portão
`identidade` em 16/10 por colar `Inspired` no kolejny. `P` é por FRASE: **uma
frase curta por cena**, e `cenas ≈ total / 3` para manter a cadência.

## O LONGO DA REFERÊNCIA, MEDIDO QUADRO POR QUADRO — e a distância NÃO é efeito

**Pedido do dono, 16/10:** *"Preciso que entenda o vídeo publicado de 8 min do
canal labtreinamento frame por frame."*

**A rota do vídeo deu 403 e reabriu uma hora depois, no MESMO sandbox** — é a
tabela de rotas outra vez: estado, não propriedade. Eu havia relatado "efeitos
não medidos" em vez de inventar análise; uma rodada depois o formato 134 baixou.

Medido no `FtCtIJPsc_Q` (530,03 s) com o método do 690/699 — escala absoluta:

| | mediana | congelados |
|---|---|---|
| **a REFERÊNCIA** | **0,072** | **96%** |
| `labtreinamento-s011` (o defeito do 690) | 0,39 | 91% |
| `kolejny-poziom-s017` (depois do 699) | 0,63 | 73% |

**Ela é 5 a 9 vezes MAIS estática que nós.** Zero b-roll, zero rosto, SATAVG 3,4
a 5,6 (monocromática), nenhum quadro claro em 530. **O mundo visual dela é o
nosso** — logo a identidade por canal (601) não muda.

**Então "replicar os efeitos" é pedido sem objeto.** A distância são três coisas,
e as três são de LONGO:

1. **trilho de capítulos PERMANENTE no topo** (`1 A armadilha | 2 Os três limites
   | 3 O que o PROCX muda | 4 Quando usar cada um`), com o corrente destacado —
   e é por isso que **ZERO transições passam de scene 0,15**: o trilho e a marca
   d\'água nunca saem, só o painel troca;
2. **18,9 s por plano** (28 transições) contra os **3,1 s** nossos;
3. **cinco layouts que o `layout.py` não tem**: fórmula anotada argumento por
   argumento, duas colunas com ✗/✓, cartão de erro (`#REF!`), divisor de parte e
   cartão de número grande.

**NADA de parâmetro mudou (§10).** 18,9 s por plano não existe em short, e trilho
num 9:16 de 40 s não tem onde morar — isto especifica o LONGO, que é a metade não
começada do pedido de 16/10. Construir os layouts é decisão do dono.

**No código:** `fabrica/video_referencia.py` (`cadencia_s`, `mais_estatica_que`,
`relato`) e oito testes, um deles **falha se uma peça nossa ficar mais estática
que a referência**, para que a conclusão seja relida em vez de reaproveitada.

**E o método do OCR vale guardar:** `tesseract --psm 6` devolveu **zero texto nos
18 quadros** e eu quase relatei "o vídeo não tem texto na tela". Painel escuro com
texto claro precisa de `format=gray,negate` antes, e com `--psm 11` saiu a
estrutura inteira. **Instrumento que devolve vazio não prova ausência.**

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

**E ISSO VIROU UM DEFEITO MEDIDO EM 13/10 ÀS 09:1x — aprendizado 723, `alto`.**
Eu escrevi o parágrafo acima e **não o apliquei ao código**. A leitura ao vivo das
09:0x deu `labtreinamento` **68 → 67** numa janela de 13,6 h, cujo piso é
**1,76/dia** — e o `porta1.quadro` chamou isso de ritmo RESOLVIDO de −1,76/dia e
projetou **"chega NUNCA"**. O critério era `agora != antes`: **recusava delta zero
e aceitava UMA contagem**, assimetria sem justificativa nenhuma. É o mesmo erro
que eu corrigi para o kolejny em 12/10, do outro lado do sinal.

Agora é `abs(agora - antes) >= 2`, e `tests/test_porta1_uma_contagem.py` tem sete
testes, um deles ancorado nesta leitura real. **O quadro das 09:1x sai com os TRÊS
canais em `indeterminado`** — e isso é a leitura honesta: 67 / 19 / 8, com
|ritmo| ≤ 1,76/dia nos três.

**O que isto NÃO autoriza dizer:** que o labtreinamento está perdendo inscrito. Um
passo para baixo é o mínimo que o instrumento consegue expressar. **E o que ele
derruba:** o +0,60/dia que eu vinha usando para projetar 2028-10-06 **não se
confirmou na leitura seguinte** — ele era uma contagem, e a contagem seguinte foi
para o outro lado.

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

**E A LEITURA DE 14/10 ÀS 11:40 VALEU A JANELA E AINDA ASSIM DEU INDETERMINADO —
aprendizado 755.** Medido com `pg_net`, `status_code` 200 nos três canais, contra
a leitura de 13/10 22:1x, **13,4 h** (exatamente o que o
`porta1.horas_para_resolver(1,79)` pede):

| canal | antes | agora | delta |
|---|---|---|---|
| labtreinamento | 67 | **68** | +1 |
| epomeno-epipedo | 20 | **20** | 0 |
| kolejny-poziom | 8 | **8** | 0 |

**Os três saem `indeterminado`**, porque o critério do 723 exige **duas
contagens** e o maior delta foi UMA. E a linha que o módulo imprime —
*"frota +1,79/dia"* — **é ela mesma uma contagem**: o +1 em 13,4 h está
exatamente SOBRE o piso de resolução da janela. É a armadilha do 723 outra vez,
agora no agregado.

**A consequência prática:** a janela que resolve 1,79/dia **não basta quando o
delta real é de uma unidade**. Para resolver a partir de 13/10 22:1x é preciso
`|delta| ≥ 2`, o que no ritmo suposto cai perto de **15/10 01:30** — e qualquer
leitura antes disso só repete "indeterminado" com mais horas.

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

## E EU REPETI O HÁBITO UMA CAMADA ACIMA: 16 DE 16 PEÇAS NUM CANAL

**Aprendizado 762, `alto`, medido em 14/10 às 16:1x, no banco.** Das peças
publicadas em 14/10, **DEZESSEIS de dezesseis saíram no `labtreinamento`**, todas
`shorts`, de 00:12:48 a 15:12:24 — e **zero** no `epomeno-epipedo` e no
`kolejny-poziom`. O dono pede **7/dia POR CANAL**; dois dos três ficaram em zero o
dia inteiro.

**O `concentracao.py` não podia acusar isso**, e é por isso que o achado é meu e
não dele: ele conta origem **DENTRO** do canal. Eu construí o contador do meu
hábito em 13/10 e **repeti o mesmo hábito uma camada acima**, pela mesma razão —
era o canal que estava aberto na minha cabeça.

**E o que agrava é a nossa própria medição, o 713:** o par das dezesseis é
`labtreinamento/shorts`, com **0,07 inscrito/peça** — o penúltimo da lista — e o
melhor par medido é `epomeno-epipedo/longo`, com **0,33**, onde não saiu nada.

**O que isto NÃO prova, e a ressalva é grande:** que produzir no epomeno renderia
mais. O **693** diz que views/peça é cego abaixo do dobro, e o 713 é de 161 peças
para 19 inscritos. **E concentrar é o PLANO** — os 500 são limite POR CANAL, e o
alvo realista escrito neste arquivo pede *"5 a 7 peças/dia CONCENTRADAS num
canal"*. **O que o plano não diz é em QUAL canal**, e é essa escolha que nunca foi
medida: ela foi hábito.

**No código:** `fabrica/concentracao_frota.py` e onze testes. Rode junto com o
irmão, antes de escolher pauta:

    python3 fabrica/concentracao_frota.py

**E ELE ACHOU UM BURACO DELE MESMO NA PRIMEIRA EXECUÇÃO:** a contagem sai das
**specs**, que não têm data, logo mede o **ACERVO** — 50 / 25 / 22, que está
**dentro** do dobro (50 não é maior que 50) e **não alerta**. O **DIA** era
16 / 0 / 0, e alerta. **Acervo dilui rodada**, e um contador que só vê acervo
nunca acusaria o dia — a mesma cegueira que ele nasceu para consertar. Por isso o
`relato` aceita `por_dia=` (lido de `videos.publicado_em`), aplica o **mesmo**
limiar aos dois níveis, e **sem** esse argumento DIZ que está lendo acervo em vez
de calar.

**E O CONTADOR DO DIA NÃO ORDENA NADA NA VIRADA DA MEIA-NOITE — aprendizado
771, `alto`, medido em 15/10 às 00:0x.** Depois de escolher o canal em SEIS
rodadas seguidas, o `relato(por_dia=...)` devolveu **0 / 0 / 0** — o dia
calendário acabara de começar — e **não ordenou nada exatamente na rodada que
precisava escolher.**

**E a cegueira é SIMÉTRICA da que ele nasceu para consertar:** no 762 o ACERVO
diluía a rodada (50/29/26 está dentro do dobro e não alerta); aqui o dia
recém-começado **APAGA as últimas horas**. As duas contagens têm janela errada,
em sentidos opostos.

**A saída é a JANELA MÓVEL, e ela estava medida no mesmo instante:** com
`publicado_em >= now() - interval '24 hours'` os números eram **16 / 4 / 4**, que
alerta **e** preserva o empate dos dois canais baixos — a informação que a
meia-noite jogou fora. `relato` passou a aceitar `janela=` e `janela_h=`, com a
MESMA `analise` e o MESMO limiar do irmão, e quando o dia vem todo em zero ele
**diz que não ordena e para onde ir**, em vez de calar ou fingir alerta.
`tests/test_o_dia_calendario_nao_ordena_na_virada.py`, sete testes, um na
fronteira exata (8 contra 8 não alerta) e um que **falha se a nota do 762 tiver
sido apagada pelo conserto**.

**O limiar é o do irmão — mais que o dobro do segundo — e isso é deliberado:**
limiar novo aqui seria critério sem procedência. E a fronteira exata tem teste,
como no caso 10-contra-5 de 13/10.

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

**No código:** `fabrica/contagem_declarada.py` e nove testes.

**E O "1 CONFLITO EM 207 SPECS" QUE EU ESCREVI AQUI ERA ANALFABETO, NÃO LIMPO —
aprendizado 725, `alto`, medido em 13/10 às 12:1x.** O vocabulário do módulo era
inteiro em **português**, e as specs do epomeno são **gregas** e as do kolejny
**polonesas**. Então "0 conflitos" nelas não media nada — e eu reportei o 1 como
medição da FROTA. É o mesmo erro de enquadramento do 679/698: tratar como da
frota o que é de um terço dela.

Achado **à mão**, escolhendo pauta: o `epomeno-epipedo-006` declara
`Τέσσερα λάθη` no capítulo 73 e enumera **CINCO** — o 79 diz literalmente
*"Υπάρχει και ένα πέμπτο"*.

**Com os três idiomas são QUATRO**, e os quatro têm a MESMA assinatura autoral —
a fonte declara N e depois acrescenta *"existe também um N+1"*:

| spec | declara | enumera |
|---|---|---|
| `epomeno-epipedo-005` | 4 | **5** |
| `epomeno-epipedo-006` | 4 | **5** |
| `epomeno-epipedo-014` | 3 | **4** |
| `labtreinamento-009` | 5 | **6** |

**E O CONSERTO DEU TRÊS FALSOS POSITIVOS ANTES DE FICAR DE PÉ, os três na mesma
rodada — quatro correções do mesmo módulo em meia hora:**
1. **só o vocabulário** levou a frota de 1 para **13**, e **doze eram falsos**:
   `cztery błędy` com três kickers `<ordinal> błąd`, porque o **primeiro item
   mora na NARRAÇÃO** do capítulo que declara. Conserto: contar a **posição mais
   alta** alcançada, lendo kicker **e** narração;
2. ainda sobravam subcontagens (`quatro passos` contra 1): a fonte enumera com
   ordinal **nu seguido de dois-pontos** (`Primeiro:`, `Drugi:`) ou com o numeral
   **depois** do substantivo (`Passo um`). Conserto: **a regra é ASSIMÉTRICA** —
   só reporta quando a enumeração **passa** da declaração. Achar um quinto
   **prova** que existem cinco; não achar o primeiro prova apenas que eu não leio
   aquela forma. O módulo perde o caso oposto, e isso vai dito;
3. o **ordinal nu** acusava no outro sentido: `τις δύο στήλες` (são duas, de
   fato) pareou com `πρώτο/δεύτερο/τρίτο` de **outra lista** doze capítulos
   adiante. Conserto: ordinal sem o substantivo **não conta**, nem perto.

`tests/test_contagem_declarada_multilingue.py` tem dez testes — um por falso
positivo, um por conflito real, e um que **falha se a contagem voltar a UM**
(isto é, se o grego e o polonês saírem do vocabulário). E **dois testes meus de
hoje de manhã foram RETRATADOS no lugar**, porque travavam o comportamento
errado.

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

## A PAUTA IGNORAVA ONDE O CANAL ESTÁ HOJE — pedido do dono, 16/10

Palavras dele: *"Estas produções estão muito distantes do último vídeo produzido
e publicado no canal labtreinamento"*.

**Medido antes de concordar, porque ele podia estar falando de forma e não de
assunto.** Rank da origem das dez últimas peças daquele canal, pela playlist de
uploads VIVA (1 = o longo mais novo):

| peça | s051 | s052 | s053 | s054 | s055 | s056 | s057 | **s058** | **s059** | **s060** |
|---|---|---|---|---|---|---|---|---|---|---|
| rank | 14 | 13 | 12 | 7 | 3 | 2 | 11 | **1** | **1** | **14** |

**Duas peças seguidas no topo do canal e a seguinte treze posições atrás.** Ele
estava certo, e o número diz quanto.

**E A MINHA PRIMEIRA EXPLICAÇÃO ESTAVA ERRADA, o que fica registrado porque
custou uma conta:** eu supus que espalhar uso entre origens puxaria
sistematicamente para o passado. **Spearman(usos, rank) = −0,21**, com uso quase
plano (4 em doze das catorze origens). O critério não puxa para trás em média —
ele é **CEGO ao tempo**, e com uso empatado o desempate caiu em qualquer lugar.

**A CAUSA ESTRUTURAL é o filtro `escrevivel`, e ela é exata: entre as origens
recentes, a ÚNICA que ele exclui é o rank 1** — porque longo novo é justamente o
que ainda não tem spec local. Logo a pauta era empurrada para fora do topo por um
filtro que fala de **disponibilidade de texto**, não de valor editorial. (Os
outros `False` são os ranks 15 a 19, cópias do mesmo título, que não disputam
pauta.)

**A REGRA QUE FICA: a pauta serve o longo MAIS NOVO primeiro, e falta de spec
local não é motivo para pular o topo** — a rota é a regra (h), e ela está provada
nesse exato caso: o `s058` e o `s059` saíram do rank 1 por ela.

**No código:** `fabrica/recencia.py` (`ordem_do_retrato`, `rank`,
`distancia_do_topo`, `analise`, `relato`) e sete testes. Rode junto com os dois
contadores de concentração, **com a ordem VIVA**:

    python3 -c "import sys;sys.path.insert(0,'fabrica');import recencia;print(recencia.relato(USOS, ORDEM_VIVA, topo_vivo=ID_DO_ULTIMO))"

**E ele RECUSA ordenar pelo retrato de 06/10**, porque o retrato não conhece os
longos publicados depois — e são eles a pergunta. É a mesma disciplina do
`porta1` recusando janela curta. **Ele também não escolhe sozinho:** o peso entre
"pouco usada" e "recente" não está medido, e peso sem procedência é critério
inventado (§10). Ele imprime as duas coordenadas e o custo em posições da escolha
cega.

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
- **E A FRASE QUE ME FEZ PULAR AS DUAS ERA MINHA, E NUNCA FOI MEDIDA —
  aprendizado 761, `alto`, medido em 14/10 às 15:2x.** O docstring do
  `concentracao.py` dizia que `StQNFMdpGdk` e `KRUERlNPzDw` têm *"sete capítulos
  de TÍTULO e **nenhuma faixa de legenda da máquina** (medido pelo
  `capitulos.yml`, runs `38504585378` e `38504726301`)"*. **Os dois runs rodaram
  SEM `legenda=true`**: as anotações deles trazem só os sete títulos e a linha
  `7 capitulos:`. Eu perguntei pela DESCRIÇÃO e li a resposta como se fosse da
  LEGENDA — §3.8 na forma mais crua. As duas tinham faixa `standard` com 15.044 e
  13.941 caracteres, e viraram o `s049` e o `s050`. **Antes de dizer que uma
  origem não tem legenda, chame `captions?part=snippet&videoId=`** — lista de
  título de capítulo não responde essa pergunta.

  **E a suíte subiu para 26 na mesma rodada, por um teste MEU:** o
  `test_o_relato_NOMEIA_as_origens_pouco_usadas` cravava a frase
  `"usadas UMA vez"`, que só existe nos ramos de LISTA do relato. Quando o canal
  deixou de ter origem de um uso só — porque eu consumi as duas últimas — o
  relato passou ao ramo *"nenhuma origem usada UMA vez"* e o teste reprovou **por
  uma frase, não por uma propriedade**. Mesma classe do 743 e do 753. Agora ele
  cobra os dois casos: havendo pouco usadas elas vão NOMEADAS; não havendo, o
  relato tem de **dizer isso e para onde ir**, em vez de calar.

- **E A ROTA DA REGRA (h) EXISTE NESTA SESSÃO, sem runner — aprendizado 759,
  `alto`, medido em 14/10 às 14:1x.** Eu vinha pulando as **duas origens MENOS
  usadas** do `labtreinamento` (`StQNFMdpGdk` e `KRUERlNPzDw`, um short cada) por
  não terem spec local, pegando sempre a banda de três usos — e a
  `concentracao.py` vinha imprimindo isso há dias. **Falta de spec local não é
  motivo para trocar de origem**, e não precisa do `capitulos.yml`: a legenda sai
  pelo `pg_net`, com o token de `yt_token_<canal>`:

      captions?part=snippet&videoId=<id>        -> 200, lista as faixas
      captions/<id do track>?tfmt=srt           -> 200, o texto

  No `StQNFMdpGdk` vieram **duas faixas** — uma `asr` e uma **`standard`**, que é
  a que a própria máquina subiu — e o download da `standard` deu **15.044
  caracteres**. O `labtreinamento-s049` (`ufZmycVvTrk`) saiu daí, e **nenhuma
  frase veio de TÍTULO de capítulo**, que é a metade que a regra (h) chama de
  inventar conteúdo.

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
  mediu que a mira da frota o prejudica.**

  **ATENÇÃO, E ISTO É UMA CORREÇÃO DE 13/10 ÀS 20:2x: o número desta seção estava
  ATRASADO contra o código, e a rotina horária também.** O `labtreinamento` tem
  hoje **(20,0 a 26,0) de duração REAL** — não (33,0 a 37,0). A troca é do commit
  `5dfc87f` ("ASSUMI O CONTROLE") e o comentário do próprio `ensaio.py` carrega a
  procedência: a faixa de 33–37 *"não foi falsificada; ela ficou irrelevante,
  porque o alvo deixou de ser 'a melhor entre as nossas' e passou a ser
  'romper'"*. **Rode `ensaio.alvo_short(canal)`, nunca o número escrito aqui** —
  foi exatamente este parágrafo que envelheceu.

  E a divergência **era ativa**: a rotina mandava mirar 33–37, e o `mira.py`
  reprova 33–37 no `labtreinamento` desde 12/10. Quem seguisse a rotina escrevia
  peça que o instrumento recusa.

  O histórico de 09/10 fica, porque explica de onde veio o override: o gatilho do 682 disparou com **idade casada**
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

### E EM 13/10 ÀS 10:1x O FATOR DO PIPER FOI VALIDADO — aprendizado 724, `alto`

**Primeira validação contra duração REAL desde que o fator entrou.** Lidas as dez
peças publicadas hoje numa chamada (`status_code` 200), `contentDetails.duration`
contra `ensaio.duracao_real_prevista(..., 'piper')`:

| pacote | real | piper | desvio |
|---|---|---|---|
| `labtreinamento-s026` a `-s032` | 25, 24, 25, 24, 25, 26, 21 | 24,5 / 24,1 / 25,1 / 24,6 / 25,8 / 25,6 / 20,7 | −3,0% a +2,1% |
| `epomeno-epipedo-s020` / `-s021` | 37 / 39 | 37,8 / 37,4 | −2,2% / +4,3% |
| `kolejny-poziom-s022` | 35 | 35,5 | −1,5% |

**Mediana −0,5%, média −0,1%, e NOVE das dez dentro de 1 s** — que é a própria
granularidade, porque o YouTube arredonda para cima. Contra o 711, onde o
estimado do edge errava 10 a 20% nas peças do Piper, isto é o fator funcionando.

**E O ACHADO QUE VEM DE GRAÇA É MAIS IMPORTANTE QUE A VALIDAÇÃO: as DEZ casaram
com o Piper e NENHUMA com o edge** (que previa 25,3 a 42,7 contra 21 a 39 reais).
Sob a nula de meio a meio, 1/1024. **Em produção é o Piper que narra**, e o braço
edge-tts do 711 era `n=1`.

**A consequência atinge a mira, e ela é aritmética:** mirar o `ALVO_SHORT` pelo
**estimado** entrega peça **~12 a 15% mais curta** que a mira. O epomeno mirou
42,7 e saiu **37 e 39**; o kolejny mirou **41,8, deliberadamente o piso** da faixa,
e saiu **35** — abaixo do piso. **Eu acertei a mira no instrumento errado.**

**NÃO mexi em `ALVO_SHORT` nem em `ALVO_POR_CANAL`**, e o motivo é a trava da
§10: é parâmetro de produção, e a mira existe por medição de view que ainda não
existe. **O desenho pré-registrado é: mirar a faixa no mundo `piper`**, já que é
ele quem narra — e isso é decisão do dono, porque muda toda a produção.
`tests/test_fator_piper_contra_real.py`, seis testes, e um deles **falha se o
provedor do runner mudar** (ele exige edge acima do real em 10 de 10).

#### E ÀS 16:2x DO MESMO DIA A SEGUNDA FRASE DO 724 CAIU — e por medição

**As duas peças de 15:17 e 16:12 falsificam "em produção é o Piper que narra".**
Duração REAL contra as duas previsões, numa chamada, `status_code` 200:

| peça | real | edge | piper | casa com |
|---|---|---|---|---|
| `7qreIlqtUIU` (`epomeno-epipedo-s024`) | **44** | 43,1 | 38,2 | **EDGE** (+2,1% contra +15,2%) |
| `xlQvH6JjrB4` (`kolejny-poziom-s023`) | **39** | 43,1 | 36,7 | nenhum dos dois de perto |

E o `s024` é o caso duro: **o real ficou ACIMA da previsão do edge** (44 > 43,1),
que é justamente o que o meu teste das 10:1x declarava não acontecer. **Aquele
teste segue valendo para as DEZ peças em que foi ancorado e não se generaliza
para a frota** — o mesmo erro de enquadramento do 679/698/725, cometido por mim
seis horas antes.

**O código sempre disse isso e eu não li:** `fabrica.py:598-620` tenta o
`edge_tts` **três** vezes e só cai no Piper na terceira falha. Logo o provedor é
decidido **por cena e por run**, pelo estado da rede do runner — nunca por
configuração. As dez peças do 724 mediram um runner em que o edge estava caindo;
elas **não** mediram uma escolha.

**O que isto CONFIRMA, com motivo mais forte do que o que eu escrevi às 02:1x:**
o portão exigir a faixa nos DOIS mundos era a decisão certa. Eu escrevi "o
provedor se decide no runner"; agora está medido que ele se decide **de um run
para o outro**.

**E O QUE ISTO DERRUBA É UMA PROPOSTA MINHA DESTA MANHÃ:** o desenho
pré-registrado *"mirar a faixa no mundo `piper`, já que é ele quem narra"* **sai
da mesa.** Não se mira um mundo que não se controla. A mira tem de valer nos
dois, que é o que o `fabrica/mira.py` já relata e o portão já cobra — e isso
**remove uma das decisões que estavam na fila do dono**.
`tests/test_provedor_nao_e_fixo.py`, **oito** testes, e um deles **falha se
TODAS as peças passarem a casar com o mesmo mundo**, para que o raciocínio seja
relido.

**TERCEIRO PONTO às 17:2x, e ele CONFIRMA o 730 em vez de retratá-lo:** o
`0ZIOD-KOupY` (`kolejny-poziom-s024`) saiu com **44 s reais** contra edge 42,9 e
piper 36,5 — casa com o **edge**, e outra vez **acima** dele. Agora são **duas de
três** com o edge, e as duas por cima pela mesma margem pequena: **+2,1% e
+2,6%** — viés de ~2,5% no mundo edge, não ruído.

**E a consequência prática vai dita em vez de virar limiar:** mirar o TOPO da
faixa deixa **~1 s de folga** contra o teto de 45 quando é o edge que narra. Não
mexi na mira, porque é parâmetro de produção e a trava da §10 vale.
Aprendizado **731**, gravado como registro próprio porque o `UPDATE` no 730
levou **timeout de 60 s duas vezes** — é o aviso 621, e insistir não é conserto.

#### E ÀS 18:2x O 730 E O 731 CAÍRAM EM PARTE — aprendizado 732, e é duro

**Quatro peças da tarde, uma chamada, `status_code` 200:**

| pacote | edge | piper | REAL | desvio edge |
|---|---|---|---|---|
| `epomeno-epipedo-s025` | 42,1 | 37,3 | **44** | +4,5% |
| `kolejny-poziom-s024` | 42,9 | 36,5 | **44** | +2,6% |
| `epomeno-epipedo-s024` | 43,1 | 38,2 | **44** | +2,1% |
| `kolejny-poziom-s023` | 43,1 | 36,7 | **39** | −9,5% |

**TRÊS previsões diferentes devolveram o MESMO real de 44, e a previsão MAIOR
devolveu o MENOR real.** A ordem de previsto não reproduz a de real em sentido
nenhum.

**E ISSO FALSIFICA A DECISÃO QUE EU TOMEI NA MESMA RODADA.** Pelo 731 eu
encurtei o `s025` de edge **44,3 para 42,1** — 2,2 s a menos — para ganhar folga
contra o teto. **O real deu 44, igual ao das duas peças cuja previsão era
MAIOR.** Encurtar a previsão em 2,2 s não encurtou a peça em nada.

**O que CAI do 731:** o "viés de ~2,5% para cima no mundo edge". Era n=2; com o
terceiro ponto virou **+4,5%**, e o desvio **cresce quando a previsão diminui** —
assinatura de algo que não depende da previsão. **O que CAI do 730:** a frase
"casa com o EDGE", que descrevia a menor distância entre duas previsões ruins.

#### E EM 15/10 ÀS 04:1x O REAL PASSOU DOS 45 S — aprendizado 772, `alto`

**O `epomeno-epipedo-s032` (`XmSOfi_rnic`) saiu com 46 s reais e o portão estava
VERDE nos dois mundos:** edge **42,5** e piper **37,7**, os dois dentro de 18 a
45. Provedor **MEDIDO** pela anotação (zero avisos `NARRACAO PELO PIPER` no job
`116243667180`), logo foi o edge. Resíduo **+3,5 s**, dentro da banda e com o
sinal ESTABELECIDO. 34 pontos, 30 estabelecidos.

**Logo "o portão nos dois mundos está segurando a peça" vale para o ESTIMADO e
não para o REAL** — e a aritmética já estava escrita na própria banda: o resíduo
vai a **+3,7 s**, logo mirar o topo do `ALVO_SHORT` (43,0) admite real de até
**~46,7**. O teto do portão é 45. **As duas coisas não cabem juntas, e agora é a
FROTA, não a mira de um canal** — é o 740/748 um nível acima.

**E a copy declarou isso ANTES de publicar** ("o real deve cair entre 42,6 e
46,2 s — o topo PASSA do teto de 45"), logo é acerto out-of-sample. O que isso
NÃO autoriza é confiança: a faixa tem 3,6 s de largura contra 1 s de
granularidade.

**E O PRIMEIRO PONTO DEPOIS DA REGRA DE REDAÇÃO CAIU DENTRO, com n=1 de cada
lado e isso vai dito:** o `kolejny-poziom-s031` (`IqN1fQtcfP0`) foi escrito
mirando o **PISO** (edge 41,8), provedor **edge** medido (zero avisos no job
`116258798184`), e o real deu **44** — resíduo +2,2, dentro da banda e **abaixo
do teto de 45**. Contra o `s032`, que mirou 42,5 e deu 46. **O que isto NÃO é:**
prova de que o piso protege. São duas peças, de canais e vozes diferentes, e a
banda de 3,6 s cobre os dois resultados sem distinguir nada — pelo 768/769 uma
diferença de 0,7 s de previsão não ordena contra um real de passo 1 s. **O que
é:** a única escolha de redação disponível, aplicada, com o resultado registrado
para quando houver pontos bastantes.

**NADA de parâmetro mudou (§10):** a saída — mirar o piso por padrão, ou
descontar o resíduo da mira — é parâmetro de produção e vai para a fila do dono
junto com a decisão do 740/748. O que muda hoje é REDAÇÃO: **mire o PISO do
`ALVO_SHORT` quando a voz não exigir o topo**, e declare a exposição.
`tests/test_o_real_passou_do_teto_do_portao.py`, seis testes, e um deles **falha
se alguém transformar isto em limiar novo**.

**E ISTO MATOU A ÚLTIMA PERNA DA FRASE DO 763.** O apoio que eu dizia restar era
a LARGURA — *"o teto de 3,7 vem do `labtreinamento-s043` e nenhum ponto de outro
canal passou de +2,8"*. Este ponto, de outro canal, deu **+3,5**: encostou no
teto a **0,2 s**, margem menor que o passo de 1 s do instrumento. **Nem contagem
nem largura sustentam mais "a banda é de um canal"**, e o teste foi reescrito
para registrar a queda em vez de mover o número pela quarta vez.

**O que SOBREVIVE, e com mais razão:** o provedor não é fixo
(`fabrica.py:598-620`), e **o portão exigir 18 a 45 s nos DOIS mundos é o que
está segurando a peça** — a folga larga é necessária justamente porque a previsão
erra mais do que eu media.

**O que eu NÃO afirmo, pelo §3.8:** que existe teto de 44 s. A peça de 39
desmente, e n=4. **Hipótese declarada e INCOMPLETA:** a folga por cena imposta
pelo `-t` do clipe acumularia em dez cenas — mas **as quatro têm dez cenas**,
incluindo a de 39, logo cenas sozinhas não explicam.
`tests/test_previsao_nao_prediz_nesta_faixa.py`, sete testes, um deles ancorado
na decisão que falhou.

#### E ÀS 19:1x O 732 CAIU INTEIRO — aprendizado 733, e a medição era BARATA

**O `voz_piper.aviso_de_calibracao` emite `::warning::`, e `::warning::` SAI pelas
ANOTAÇÕES do job.** Logo o provedor de cada cena é **observável**, sem ler log
nenhum. Eu passei três rodadas **inferindo** o provedor pela distância entre
previsão e real, quando bastava contar avisos:

    gh api repos/<owner>/<repo>/check-runs/<job>/annotations \
      --jq '[.[]|select(.message|test("NARRACAO PELO PIPER"))]|length'

| peça | avisos | provedor | previsão **dele** | real | desvio |
|---|---|---|---|---|---|
| `kolejny-poziom-s023` | **10** | **PIPER** | 36,7 | 39 | **+6,4%** |
| `epomeno-epipedo-s024` | 0 | edge | 43,1 | 44 | +2,1% |
| `kolejny-poziom-s024` | 0 | edge | 42,9 | 44 | +2,5% |
| `epomeno-epipedo-s025` | 0 | edge | 42,1 | 44 | +4,5% |

**AS QUATRO CASAM COM O PROVEDOR QUE DE FATO NARROU**, e o viés é sempre
**positivo**. A frase central do 732 — *"a previsão não prediz"* — vinha de eu
comparar o real contra o mundo `edge` em **três das quatro** peças sem saber qual
mundo havia narrado, e numa delas o mundo era o outro. **Comparador escolhido sem
medir**, que é o efeito (C) da rotina.

**E o "paradoxo" das três previsões com o mesmo real cai pelo §3.8:** as três
caem dentro de **1,0 s** uma da outra, e o real tem granularidade de **1 s com
arredondamento para cima**. Três valores num intervalo de um segundo devolvendo o
mesmo inteiro não é ausência de relação — é **falta de resolução**. Eu chamei de
achado o limite do instrumento.

**E a terceira afirmação do 732 era comparador escolhido:** eu disse que
"encurtar 2,2 s não encurtou a peça", comparando o `s025` publicado com OUTRAS
peças. A primeira versão (edge 44,3) **nunca foi renderizada** — não existe o
real dela, e eu apresentei uma comparação como se fosse antes-e-depois da mesma
peça.

**O que sobrevive e sai FORTALECIDO:** o **730** (o provedor não é fixo) agora
tem prova **direta** — dez avisos num render e zero nos outros três, no mesmo
dia. E o **731** (viés para cima) volta a valer: mediana **+2,5%** no edge com
n=3, e **+6,4%** no piper com n=1. O portão nos dois mundos segue certo.

**A REGRA DE MÉTODO QUE FICA: antes de inferir qual provedor narrou, CONTE OS
AVISOS** — um por cena do Piper, zero se o edge venceu.

#### E O NÚMERO DO 733 CAIU NA PRIMEIRA PREVISÃO OUT-OF-SAMPLE — aprendizado 734

Eu escrevi na copy do `labtreinamento-s033`, **antes de publicar**, que o real
sairia **~26,3** (viés de 2,5% sobre a previsão edge de 25,7). Provedor medido
**edge** (zero avisos), real **27** — **+5,1%**, acima do maior desvio que eu
tinha observado.

| pacote | prev edge | real | resíduo | razão |
|---|---|---|---|---|
| `epomeno-epipedo-s024` | 43,1 | 44 | **+0,9 s** | +2,1% |
| `kolejny-poziom-s024` | 42,9 | 44 | **+1,1 s** | +2,5% |
| `epomeno-epipedo-s025` | 42,1 | 44 | **+1,9 s** | +4,5% |
| `labtreinamento-s033` | 25,7 | 27 | **+1,3 s** | +5,1% |

**O sinal e o método do 733 ficam de pé** — quatro de quatro acima, e o provedor
se mede pela anotação. **O que cai é o NÚMERO:** a mediana de +2,5% era de n=3
com as três na mesma faixa de 42 a 43 s, e não se generalizou para 25,7 s.

**E o ponto de método: com n=4 e granularidade de 1 s, percentual NÃO se distingue
de OFFSET.** O resíduo vai de **0,9 a 1,9 s** (razão 2,1) e de **2,1% a 5,1%**
(razão 2,4) — dispersões da mesma ordem, logo os dados não escolhem entre os dois
modelos. **O que eu afirmo é só o limite: o real ficou sempre acima, por no
máximo 1,9 s.**

**A consequência prática, e é a única de hoje:** quem mira perto do teto de 45 s
conta com **~2 s** de resíduo, não com 2,5%. Para 43 s previstos isso dá 45, no
limite. **Não mexi na mira nem no portão** — n=4, e a trava da §10 vale.
`tests/test_residuo_e_offset_ou_percentual.py`, seis testes.
`tests/test_provedor_medido_pela_anotacao.py`, sete testes, e um deles **falha se
alguém trocar o `::warning::` por `print`**, porque aí o provedor volta a ser
inferido no olho.

**E UM ERRO DE PROCESSO MEU, NA RODADA ANTERIOR:** eu disse ao dono que a nota do
731 tinha entrado neste arquivo. **Não tinha.** O meu `t.replace` rodou **sem
`assert`**, não achou a âncora, e gravou o arquivo inalterado — falha **silenciosa
e no sentido permissivo**, a mesma assinatura do corpus atrasado (726). A regra
que fica: **todo `replace` em documento leva `assert` antes de gravar**, e eu só
descobri porque a edição seguinte estourou o `AssertionError` que eu pus nesta.

**Vigilância do §3.2 na mesma chamada: as dez `processed` e `public`, nenhum
`P0D`.**

**Não corrigi `MODELO_VOZ` ainda**, e o motivo é que a spec declara a voz do
edge-tts mesmo quando o Piper é quem narra — o provedor se decide no runner,
depois das três tentativas. O conserto certo é a estimativa receber o PROVEDOR,
não a tabela ser reescrita por baixo. Desenho pré-registrado antes de mexer.

#### E O LIMITE DE 1,9 S DO 734 CAIU NO QUINTO PONTO — aprendizado 739, `alto`

**Medido em 13/10 às 22:2x, no `labtreinamento-s034` (`wWmHRDmQMO4`).** Provedor
**MEDIDO** pela anotação (zero avisos `NARRACAO PELO PIPER` no job
`115567940121`, logo **edge**), previsão edge **25,6** e real **28** — resíduo
**+2,4 s / +9,4%**, acima do maior desvio que eu já tinha visto nos dois eixos.

**E o ponto que mais corta é a comparação com a peça anterior do mesmo canal:** o
`s033` previa **25,7** e deu **27**; o `s034` previa **25,6** e deu **28**. Mesmo
canal, mesma voz, mesmas dez cenas, mesmo provedor medido, **previsões a UM
DÉCIMO de distância e reais diferentes em um segundo inteiro.** Logo **o OFFSET
constante também não descreve** — ele teria de ser igual nos dois — e o
percentual tampouco, porque os dois pontos curtos trazem justamente os maiores
percentuais (5,1% e 9,4%).

**O que sobrevive é o SINAL e o MÉTODO:** cinco de cinco acima da previsão do
provedor que de fato narrou, e o provedor se conta pela anotação (733), não se
infere.

**E A CONSEQUÊNCIA ATINGE A MIRA, que é a parte prática:** a mira do
`labtreinamento` é sobre a duração **REAL** (20,0 a 26,0) e o `mira.py` a cobra
sobre o **ESTIMADO**. As duas peças narradas pelo edge saíram em **27 e 28
reais** com o estimado DENTRO — ou seja, **estimado dentro nos dois mundos NÃO põe
o real dentro da mira.** As sete peças anteriores do canal (s026 a s032) ficaram
em 21 a 26 reais, e aquelas foram narradas pelo **Piper**.

**NÃO mexi na mira nem no `mira.py`** — n=5, e a trava da §10 vale. Fica dito, com
teste: `tests/test_residuo_quebra_o_limite_de_dois_segundos.py`, sete testes, um
deles **falha se o pior resíduo voltar para dentro de 1,9 s**, para que o 734 seja
relido em vez de reaproveitado.

**E O BURACO DO 739 FOI FECHADO NO INSTRUMENTO às 23:2x, sem virar portão:** o
`mira.py` passou a imprimir **onde o REAL deve cair** — a previsão mais a banda
OBSERVADA de 0,9 a 2,4 s — e a dizer quando ela passa do teto da mira. No
`labtreinamento-s034` ele agora diz *"se edge narrar, o REAL deve cair entre 26,5
e 28,0 s — PASSA do teto da mira (26,0)"*, que é exatamente o que aconteceu (real
28). **Ele INFORMA e NÃO reprova**, e o motivo vai escrito no módulo: com n=5 e
uma banda que varia por um fator 2,7 sem lei estável, reprovar seria inventar
portão com cinco pontos. `tests/test_mira_diz_onde_o_real_cai.py`, sete testes, um
deles **exige que o código de saída continue zero**.

**E ÀS 00:3x DE 14/10 ISSO VIROU UMA CONTRADIÇÃO ARITMÉTICA — aprendizado 740,
`alto`.** Assim que o relato passou a imprimir a banda, ficou visível que as duas
coisas que eu construí **não cabem na mesma faixa**. Para a PREVISÃO passar a
conferência da mira nos dois mundos é preciso `piper ≥ 20,0` e `edge ≤ 26,0`, o
que com a razão piper/edge de ~0,82 põe o edge em **[24,33; 26,00]**. Para o
**REAL** cair dentro de 20,0 a 26,0 é preciso `edge ≤ 23,60` (teto menos 2,4) e
`piper ≥ 19,10`, o que põe o edge em **[23,23; 23,60]**.

**As duas janelas não se tocam — vão de 0,73 s.** Logo **mira verde NÃO significa
real dentro**, e nenhuma spec de dez cenas deste canal satisfaz as duas.

**NÃO resolvi sozinho**, e o motivo é a trava da §10: as duas saídas — mover a
mira para o ESTIMADO descontando o resíduo, ou parar de conferir estimado contra
uma faixa de REAL — mexem em parâmetro de produção. Vai para a fila do dono **com
a conta pronta**. No `labtreinamento-s035` eu escolhi o ponto que mantém a mira
verde (edge 24,8 / piper 20,4), com o real em 21,3 a 22,8 se o Piper narrar e até
**1,2 s acima do teto** se o edge narrar — e isso vai **dito na copy**, não
escondido. `tests/test_a_mira_e_o_real_nao_cabem_juntos.py`, seis testes, e um
deles **falha se as janelas voltarem a se tocar**, para que a contradição seja
relida em vez de desaparecer.

**E a procedência dos dois insumos vai junto, porque ela é fraca:** a banda é
`n=5` e a mira vem do commit `5dfc87f`. A contradição é aritmética **dados esses
dois números**; se um deles mudar com motivo, ela pode deixar de existir.

**E A BANDA PASSOU O PRIMEIRO TESTE OUT-OF-SAMPLE NA MESMA RODADA — aprendizado
741, e o teste é FRACO.** A copy do `s035` anunciou, **antes de publicar**, que o
real cairia entre **25,7 e 27,2** se o edge narrasse. Provedor medido pela
anotação (zero avisos), real **27** — resíduo **+2,2 s**, dentro. Sexto ponto,
**seis de seis acima**. Mas a banda tem **1,5 s de largura** e o real tem
granularidade de 1 s: acertar dentro dela prova pouco, e isso vai dito em vez de
virar confiança. **E ela confirmou a consequência do 740:** 27 é **um segundo
acima do teto da mira**, exatamente o que a copy declarou que podia acontecer.

**E O SEGUNDO PONTO OUT-OF-SAMPLE TAMBÉM CAIU DENTRO — aprendizado 742.** O
`labtreinamento-s036` (`QJBgbHVjh94`) foi narrado pelo **edge** (provedor MEDIDO:
zero avisos `NARRACAO PELO PIPER` no job `115627232907`), previsão edge **25,3**,
e a copy anunciou **antes de publicar** que o real cairia entre **26,2 e 27,7**.
Real **27**, resíduo **+1,7 s**. Sétimo ponto, **sete de sete acima**.

**E o teste continua FRACO pelo motivo do 741**, que vai repetido em vez de
esquecido: a banda tem **1,5 s de largura** contra granularidade de **1 s**.
Acertar dentro dela prova pouco.

**E a contradição do 740 se repetiu na mesma peça:** 27 é **um segundo acima do
teto da mira** (26,0) com o `mira.py` **verde nos dois mundos**. Duas peças
seguidas confirmam que **mira verde não significa real dentro** — a decisão
continua na fila do dono, com a conta pronta.

**O que mudou no código, e é só contagem:** `RESIDUO_N` foi de 5 para **7**. Os
dois pontos novos caíram DENTRO, logo os **LIMITES (0,9 a 2,4) não mudaram** — só
o número de pontos que os sustenta. A mira e a banda seguem intocadas (§10).

**E O TERCEIRO PONTO OUT-OF-SAMPLE TAMBÉM CAIU DENTRO, mas o que importa agora é
OUTRA COISA — aprendizado 744.** O `labtreinamento-s037` (`W-SABH2ov_A`) foi
narrado pelo **edge** (zero avisos no job `115644313606`), previsão **25,8**,
faixa anunciada antes de publicar **26,7 a 28,2**, real **28**, resíduo **+2,2 s**.
Oitavo ponto, **oito de oito acima**, e o teste segue **fraco** pelo mesmo motivo.

**O achado é o padrão, não o acerto: as TRÊS peças seguidas do `labtreinamento`
narradas pelo edge saíram FORA da mira do canal** — `s035` 27, `s036` 27, `s037`
28, contra um teto de **26,0** — e **as três com o `mira.py` verde nos dois
mundos**. Isso deixa de ser a aritmética do 740 e passa a ser **três de três
medidos**: no mundo `edge`, a conferência da previsão **não protege** a mira deste
canal. `RESIDUO_N` foi para **8**; a mira e os limites da banda seguem intocados
(§10), porque a saída é decisão do dono.

**E O PADRÃO DO 744 CAIU NA PEÇA SEGUINTE — aprendizado 746, e ele mostra o que
FAZER.** O `labtreinamento-s038` (`EgcUqRhx9IY`) foi narrado pelo **edge** (zero
avisos no job do run `38505162272`), previsão **24,4**, banda anunciada **25,3 a
26,8** — e o real deu **26**, que é **exatamente o teto da mira**. Nono ponto,
**nove de nove acima** (resíduo +1,6 s), e a **primeira peça deste canal narrada
pelo edge a cair DENTRO da mira**: agora são três de quatro fora, não três de
três.

**O que isso ensina, e é operacional:** a diferença entre o `s037` (previsão 25,8
→ real 28, fora) e o `s038` (24,4 → 26, dentro) é **1,4 s de previsão**. A conta
do 740 dizia que para o real cair dentro com segurança o edge precisa de
**≤ 23,60**; 24,4 entregou 26 no limite. Logo **mirar o PISO da mira em vez do
topo é o que põe o real dentro** — e isso é escolha de redação, não mudança de
parâmetro. `RESIDUO_N` = 9; mira e banda intocadas.

**E O 746 CAIU UMA HORA DEPOIS — aprendizado 747, `alto`, e ele corrige o que eu
tinha ACABADO de escrever na ROTINA.** O `labtreinamento-s039` (`EOzaxvaCJhk`) foi
narrado pelo **edge** (zero avisos, run `38509958200`), previsão **24,7**, real
**27** — **FORA** da mira. Décimo ponto, **dez de dez acima** (resíduo +2,3,
dentro da banda).

| peça | prev edge | real | mira (teto 26,0) |
|---|---|---|---|
| `s037` | 25,8 | 28 | fora |
| `s038` | 24,4 | 26 | **dentro** |
| `s039` | 24,7 | 27 | fora |

**Zero vírgula três segundos de previsão viraram UM segundo de real.** Logo
*"mirar mais baixo"* **não basta** — só `edge ≤ 23,60` (a conta do 740) poria o
real dentro.

**E ali entra a TERCEIRA restrição, que eu descobri tentando:** a primeira versão
do `s039` mirava 23,6 e o portão **`ortografia` REPROVOU** — cortando tanto, a
narração perde acento (**2,0% contra 4,5%** das outras specs do canal) e o TTS
pt-BR muda a pronúncia. **Então peça de dez cenas neste canal não cabe nas três
restrições ao mesmo tempo: previsão na mira, real na mira, e prosódia.** A rotina
foi corrigida no mesmo passo e a folga vai **declarada na copy**.

**E A PINÇA FECHOU — aprendizado 748, `alto`, e esta é a forma FINAL da
contradição do 740.** O `labtreinamento-s040` (`R4K0ZJH5J7U`) saiu, na primeira
versão, com edge 23,5 e **piper 19,3 — FORA da mira pelo PISO**, o lado que eu
nunca havia tocado em dez peças. Alongada para edge **24,7** / piper 20,3, o real
deu **27** — **igual ao do `s039`, que tinha a MESMA previsão de 24,7**. Décimo
primeiro ponto, onze de onze acima.

**E a conta que fecha o caso, porque ela é de FORMA e não de valor:** o piso do
piper é uma **RAZÃO** (piper ≈ 0,82 × edge) e o teto do real é um **OFFSET**
(real ≈ edge + 0,9 a 2,4).

    piper ≥ 20,0  ⟺  edge ≥ 24,4
    real  ≤ 26,0  ⟺  edge ≤ 23,7   (no caso que ocorreu DUAS vezes)

**As duas faixas não se tocam — e mudar o número de cenas NÃO resolve**, porque
cena mexe na sobrecarga e não na razão entre os dois mundos. Logo **não existe
spec de dez cenas deste canal que satisfaça as duas**, e também não existe de oito
nem de doze: a incompatibilidade é estrutural. As saídas seguem sendo as duas que
já estão na fila do dono — mover a mira para o ESTIMADO descontando o resíduo, ou
parar de cobrar uma faixa de REAL sobre o estimado.

**E isto REFORÇA o que o 732 havia negado:** a mesma previsão devolveu o mesmo
real duas vezes. `tests/test_a_mira_e_o_real_nao_cabem_juntos.py` ganhou dois
testes — um que **falha se as faixas voltarem a se tocar** e um que trava a
reprodutibilidade.

**E O DÉCIMO SEGUNDO PONTO EMPATOU O TETO DA BANDA — aprendizado 750.** O
`labtreinamento-s041` (`qEyrPRd0H6w`) foi narrado pelo **edge** (zero avisos
`NARRACAO PELO PIPER` no job `115710862870`), previsão edge **24,6**, real **27**
— resíduo **+2,4 s**, exatamente o teto da banda observada. Doze de doze acima, e
**os LIMITES seguem intocados porque 2,4 já era o máximo**: o próximo ponto acima
dele QUEBRA a banda, e o teste do 739 existe para obrigar a reler quando isso
acontecer. `RESIDUO_N` = 12.

**E o padrão do 744/747 continua:** quatro das cinco peças deste canal narradas
pelo edge saíram FORA da mira (s037 28, s038 26 dentro, s039 27, s041 27), as
quatro com o `mira.py` **verde nos dois mundos**. A decisão do 740/748 segue na
fila do dono — eu declaro a exposição na copy e não prometo real dentro.

**E A PINÇA FICOU MEDIDA PELOS DOIS LADOS — aprendizado 751, `alto`, e é a
primeira coisa ACIONÁVEL que sai do 740.** O `labtreinamento-s042`
(`84JjQ2k0S84`) foi escrito **de propósito** com previsão edge **23,4** e piper
**19,2** — isto é, com o `mira.py` **REPROVANDO pelo PISO** — e o real deu
**25 s: DENTRO** da mira (teto 26,0). Provedor **edge** medido (zero avisos no job
`115728398595`), resíduo **+1,6 s**, décimo terceiro ponto, treze de treze acima.

| escolha | previsão edge | real | mira | real na mira |
|---|---|---|---|---|
| manter a mira verde (s037) | 25,8 | 28 | verde | **não** |
| idem (s039, s040) | 24,7 | 27 | verde | **não** |
| idem (s041) | 24,6 | 27 | verde | **não** |
| **inverter (s042)** | **23,4** | **25** | **vermelha (piso)** | **SIM** |

**Logo os dois lados da pinça estão medidos, não deduzidos:** mira verde entrega
real fora, e real dentro exige mira vermelha pelo piso. **E a TERCEIRA restrição
do 747 NÃO apertou aqui** — 5,2% de letras acentuadas contra os 2,0% que
reprovaram a primeira versão do `s039`, com os doze portões do `prontidao`
verdes. O custo de prosódia do `s039` era das palavras daquela peça, não de
encurtar até 23,4.

**NADA de parâmetro mudou** (trava da §10): a saída é escolha de REDAÇÃO, e a
decisão entre as duas saídas do 740 segue na fila do dono — agora com medição
dos dois lados em vez de aritmética.
`tests/test_a_mira_e_o_real_nao_cabem_juntos.py` ganhou um teste que **falha se
um dos dois lados da série desaparecer**.

**E O 751 CAIU NA PEÇA SEGUINTE, NA PARTE QUE IMPORTAVA — aprendizado 752,
`alto`, e com ele CAI O TETO DA BANDA.** O `labtreinamento-s043`
(`FKQWRA-ll60`) foi escrito **de propósito no mesmo lado** — previsão edge
**23,3** / piper 19,1, `mira.py` reprovando pelo piso — e a copy anunciou, antes
de publicar, que o real cairia em **24,2 a 25,7**. Provedor **edge** medido (zero
avisos no job `115749911129`), real **27**: resíduo **+3,7 s**, que **FURA a banda
observada de 0,9 a 2,4** que treze pontos sustentavam.

| peça | previsão edge | real | mira (teto 26,0) |
|---|---|---|---|
| `s042` | 23,4 | **25** | dentro |
| `s043` | **23,3** | **27** | **fora** |

**Um décimo de previsão, dois segundos de real.** É a mesma assinatura do 739
(`s033`/`s034`), agora do lado curto — e ela derruba a parte acionável do 751:
**mirar abaixo do piso do piper NÃO garante o real dentro da mira.** O que
sobrevive do 751 é só o par de observações, e o que sobrevive de tudo é o SINAL:
**quatorze de quatorze acima** da previsão do provedor que de fato narrou.

**No código, e é medição e não limiar novo:** `RESIDUO_OBSERVADO` passou a
**(0,9; 3,7)** e `RESIDUO_N` a 14. O teto da banda é o maior resíduo **já
observado**, logo ele se move quando a observação sai dele — e a largura foi de
1,5 para **2,8 s**, o que torna a banda **menos útil** como previsão. Isso vai
dito.

**E ESTE TETO CAIU DE NOVO EM 15/10 ÀS 10:2x — aprendizado 774, `alto`, e é a
SEGUNDA ampliação.** O `labtreinamento-s052` (`w5a8m3GiQUE`) previa **25,0** no
edge — provedor **MEDIDO** pela anotação (zero avisos `NARRACAO PELO PIPER` no
job `116368125417`) — e saiu com **29 s reais**: resíduo **+4,0 s**, contra o
máximo de 3,7 que **trinta e nove** pontos sustentavam. Sinal estabelecido.
`RESIDUO_OBSERVADO` está em **(0,1; 4,0)**, `RESIDUO_N` = 40, 35 estabelecidos.

**O que vale guardar não é o número: as QUATRO correções da banda a ALARGARAM.**
Teto 2,4 → 3,7 (752) → **4,0** (774); piso 0,9 → 0,5 (769) → 0,1 (770). Largura
de 1,5 para **3,9 s** contra **1 s** de granularidade — ela cobre quase quatro
inteiros de real. Isso é próprio de um limite definido pelo **extremo
observado**, e significa que a banda informa cada vez menos. Vai dito em vez de
escondido.

**E O DEFEITO DO 753 REAPARECEU UMA CAMADA ACIMA, no DOCSTRING do `mira.py`:**
ele dizia *"a banda vive em `RESIDUO_OBSERVADO` — hoje 0,9 a 3,7 s"* quando a
constante era `(0.1, 3.7)`. **O piso havia baixado no 770 e a frase ficou atrás
sem ninguém ver**, porque o teste do 753 cobra a **mensagem do `relato`** e não o
docstring do módulo. A regra do 753 vale para o módulo INTEIRO, comentário e
docstring incluídos — agora o docstring manda ler a constante, e há teste que
reprova se um par antigo voltar a aparecer sem a marca de que é história.

**E DOIS TESTES MEUS REPROVARAM POR IDENTIDADE, não por propriedade** — mesma
classe do 743/753/761: um cravava `dono == ["labtreinamento-s043"]` (o dono do
teto trocou de peça, e o que importa é ele ser **estabelecido** e do canal
dominante) e outro cravava `largura == 3.6`. Corrigidos no lugar, para propriedade
monótona.

**A pinça do 740/748 PIOROU outra vez:** com resíduo de até 4,0 s, `real ≤ 26,0`
exige `edge ≤ 22,0`, onde o piper cai a **~18,0** — ainda mais longe do piso de
20,0. E o tally do 754/757/758 foi a **nove de doze**: o `s052` saiu em 29 contra
um teto de mira de 26,0, com o `mira.py` **verde nos dois mundos** e a copy
declarando a exposição antes de publicar.
`tests/test_o_teto_da_banda_foi_AMPLIADO_a_SEGUNDA_vez.py`, nove testes.

**E A PINÇA DO 740/748 ABRIU, o que é PIOR:** com resíduo de até 3,7 s, `real ≤
26,0` passa a exigir `edge ≤ 22,3`, onde o piper cai para **~18,3** — bem abaixo
do piso de 20,0. O vão entre as duas janelas foi de **0,73 s para ~2,0 s**. Não
existe spec deste canal que satisfaça as duas, e agora com folga maior.
**A decisão do 740 ficou mais urgente, e segue sendo do dono.**
`tests/test_a_mira_e_o_real_nao_cabem_juntos.py` tem um teste que **falha se o
vão ENCOLHER**, para que isto seja relido em vez de comemorado, e os meus testes
que cravavam 2,4 foram atualizados no lugar.

**E O RELATO DA MIRA TINHA A BANDA CRAVADA NO TEXTO — aprendizado 753, e o
defeito durou uma rodada.** Depois de o 752 ampliar `RESIDUO_OBSERVADO` para
(0,9; 3,7), o `mira.py` seguia imprimindo **"por 0,9 a 2,4 s"** ao lado da faixa
que ele já calculava com 3,7 — **as duas coisas na MESMA linha do relato**. Eu só
vi na rodada seguinte, lendo a saída antes de escrever a peça.

**A regra que fica: número que o módulo CALCULA não se repete escrito em string
nenhuma do mesmo módulo.** E o teste que eu tinha conferia os números da FAIXA,
não os da FRASE — por isso passou. Agora
`test_a_MENSAGEM_do_relato_le_a_banda_da_constante` reprova se o par antigo
reaparecer em qualquer lugar do relato.

**E a POSTURA DE MIRA VOLTOU ATRÁS no `labtreinamento-s044` (`MGe9N8i7fYc`),
porque o 752 derrubou a saída do 751:** com resíduo de até 3,7 s não existe mais
o ponto que punha o real dentro, então eu volto a manter a mira **verde** (edge
24,9 / piper 20,5) e a declarar a exposição. Real **27** — resíduo +2,1, dentro
da banda, e FORA da mira, exatamente como a copy disse antes de publicar.
Quinze de quinze acima; `RESIDUO_N` = 15, limites intocados.

**E A CONTAGEM DO 744 FOI A SETE — aprendizado 754.** O `labtreinamento-s045`
(`K0UCkskqpJE`, previsão edge 24,5, provedor **edge** medido, real **27**,
resíduo +2,5 dentro da banda) é o décimo sexto ponto, dezesseis de dezesseis
acima. E o que vale guardar é o **tally** deste canal no mundo `edge`:

| real | peças |
|---|---|
| **FORA** do teto de 26,0 | `s037` 28, `s039` 27, `s041` 27, `s044` 27, `s045` 27 |
| dentro | `s038` 26, `s042` 25 |

**Cinco de sete, todas com o `mira.py` verde nos dois mundos.** Isso já não é a
aritmética do 740: é **frequência medida**. A decisão segue do dono, e eu declaro
a exposição na copy de cada peça antes de publicar.

**E o portão `variedade` pegou o esqueleto outra vez:** ele avisou que o `s045`
seria a **sexta de 45** com a mesma sequência de layouts. Troquei a ordem — que é
conteúdo, não limiar — e o aviso parou. É o defeito de 12/10 às 20:1x
reaparecendo: a forma nova vira molde próprio se ninguém contar.

**E O TALLY DO 754 FOI A SEIS DE NOVE — aprendizado 757** (o id **756 queimou**
numa violação de `aprendizados_categoria_check`: a categoria é
`pauta|roteiro|producao|render|entrega|distribuicao|processo`, e eu mandei
`medicao`). O `labtreinamento-s047` (`9O8L92gDyYw`) foi narrado pelo **edge**
(provedor MEDIDO: zero avisos `NARRACAO PELO PIPER` no job `115845575478`),
previsão edge **25,4** / piper 20,9, `mira.py` **VERDE nos dois mundos**, e a copy
anunciou antes de publicar que o real cairia entre **26,3 e 29,1 s**. Real **27**
— resíduo **+1,6**, dentro da banda. Décimo oitavo ponto, **dezoito de dezoito
acima**.

| real | peças |
|---|---|
| **FORA** do teto de 26,0 | `s037` 28, `s039` 27, `s041` 27, `s044` 27, `s045` 27, **`s047` 27** |
| dentro | `s038` 26, `s042` 25, `s046` 26 |

**Seis de nove, todas com a mira verde.** `RESIDUO_N` = 18; os **limites não
mudaram**, porque o ponto caiu dentro. A decisão do 740/748 segue do dono.

**E O DÉCIMO NONO PONTO LEVOU O TALLY A SETE DE DEZ — aprendizado 758.** O
`labtreinamento-s048` (`OMZT7QPkNMA`) foi narrado pelo **edge** (zero avisos
`NARRACAO PELO PIPER` no job `115870662966`), previsão edge **25,0** / piper 20,5,
`mira.py` **verde nos dois mundos**, copy anunciando **25,9 a 28,7 s** antes de
publicar. Real **27** — resíduo **+2,0**, dentro da banda. **Dezenove de dezenove
acima.** Sete das dez peças deste canal narradas pelo edge saíram FORA do teto de
26,0, **as sete com a mira verde**; dentro ficaram só `s038` 26, `s042` 25 e
`s046` 26. `RESIDUO_N` = 19, limites intocados.

**E a vigilância do §3.2 pegou uma coisa que NÃO é defeito, e vai dita para não
virar alarme:** aos ~2 min a peça lia `uploadStatus: uploaded` com
`duration: PT27S`. **Duração presente com `uploaded` é indexação em curso, não
`P0D`** — a releitura seguinte deu `processed`. O 665 fala de `P0D` **depois de
2 h**; `uploaded` nos primeiros minutos é o caminho normal, e confundir os dois
fabricaria peça morta onde não há nenhuma.

**E O VIGÉSIMO PONTO LEVOU O TALLY A OITO DE ONZE — aprendizado 759 (a mesma
rodada da regra (h)).** O `labtreinamento-s049` (`ufZmycVvTrk`) foi narrado pelo
**edge** (zero avisos no job `115900510998`), previsão edge **25,1** / piper 20,6
— e a **primeira versão tinha piper 19,8, FORA pelo PISO**, o lado que o 748
descreve; foi alongada. Real **27**, resíduo **+1,9**, dentro da banda. **Vinte de
vinte acima**, e o real FORA do teto de 26,0 com a mira verde: agora oito fora
(`s037`, `s039`, `s041`, `s044`, `s045`, `s047`, `s048`, `s049`) contra três
dentro (`s038`, `s042`, `s046`). `RESIDUO_N` = 20, limites intocados.

**E A IDADE DA PEÇA SE MEDE PELO `now()`, NÃO PELA MINHA NOÇÃO DE QUANTO TEMPO
PASSOU — aprendizado 760, medido em 14/10 às 15:1x.** O `labtreinamento-s050`
(`o5BJKDlfVNc`) leu **`tags: 0`** na primeira conferência. O 672 diz que tag nula
**antes de 2 min não decide nada**, e eu supus pelo MEU relógio que já tinham
passado ~5 min — ia relatar falha de snippet. O `now()` da própria chamada disse
**33 SEGUNDOS** desde o `em=` do notice. Cinco minutos depois, a mesma chamada
devolveu **15 tags**.

**A regra que fica: a idade sai do `now()` da MESMA chamada contra o `em=` do
notice.** Sem isso o 672 deixa de proteger e passa a fabricar acusação — é o §3.8
na forma mais barata de evitar, porque o número certo vem de graça no mesmo
`select`.

**E o vigésimo primeiro ponto levou o tally a NOVE de doze:** previsão edge
**24,9** (verde nos dois mundos na primeira versão), provedor **edge** medido
(zero avisos no job `115931257797`), real **27**, resíduo **+2,1**, dentro da
banda. Vinte e um de vinte e um acima. `RESIDUO_N` = 21, limites intocados.

**E a pauta deste canal fechou um ciclo:** com o `s049` e o `s050` as **treze
origens** do `labtreinamento` passaram a ter **pelo menos dois shorts cada** — as
duas que estavam em um uso só eram justamente as sem spec local, que a regra (h)
já mandava usar.

**E EU IA ESCREVER QUE A BANDA ERA DE UM CANAL — aprendizado 763, `alto`, e quem
me pegou foi o primeiro teste que eu escrevi para travar a afirmação.** O
`epomeno-epipedo-s026` (`rbbz6DNuXL4`) foi narrado pelo **edge** (zero avisos no
job `115963870489`), previa **41,4** e saiu com **43 s reais** — resíduo **+1,6**,
dentro da banda. Eu ia registrar isso como *"o primeiro ponto FORA do
labtreinamento"* e travar a série como sendo de um canal. **Falso:** ela tem
`epomeno-epipedo-s024`, `-s025` e `kolejny-poziom-s024` **desde o 734** — é
multicanal desde o primeiro dia, e o ponto novo **pertence** a ela.
`RESIDUO_N` = 22, vinte e dois de vinte e dois acima.

**E o que sobra é melhor do que o que eu ia escrever:** a série é **dominada por
um canal** (18 de 22) e **bimodal na previsão** — dezoito pontos entre 23 e 26 s,
quatro entre 41 e 44 — e o teto de **3,7 vem do `labtreinamento-s043`**. Logo
*"0,9 a 3,7"* é, na prática, **a banda do `labtreinamento` usando crachá de
frota**, e isso vai dito em vez de desaparecer na contagem.

**A regra que fica: antes de escrever que uma série é de UM canal, CONTE os
canais dela.** `tests/test_a_banda_e_de_UM_canal.py` guarda os dois fatos — que
ela é multicanal e que um canal a domina — e **reprova se a dominância cair**,
para que esta nota seja relida em vez de reaproveitada.

**E O CONTADOR ESCOLHEU O CANAL, QUE É O QUE O 762 PEDIA — aprendizado 765** (o
id **764 queimou** numa violação de not-null: `aprendizados.titulo` é
obrigatório, e eu mandei o INSERT sem ele). Às 17:0x de 14/10 o
`concentracao_frota.py` com `por_dia=` acusou o DIA em **16 / 1 / 0** — o
`kolejny-poziom` em **zero** pelo dia inteiro — e a peça desta rodada saiu *daí*,
não do canal que estava aberto na minha cabeça. O `kolejny-poziom-s025`
(`siWX30h6B0A`) veio da origem `Rj7beZkOeYo` (kolejny-poziom-006, 85 capítulos,
**um** short só), com família de entrada errada nova no canal: **escolher o PRAZO
pela tabela de ofertas em vez do próprio horizonte**.

Provedor **edge** MEDIDO (zero avisos `NARRACAO PELO PIPER` no job
`115994083347`), previsão edge **41,2** — o PISO do `ALVO_SHORT` da frota, porque
`kolejny` **não** tem `ALVO_POR_CANAL` — e real **44**: resíduo **+2,8 s**,
dentro da banda e o **segundo maior valor dela**. Vinte e três de vinte e três
acima. `RESIDUO_N` = 23, limites intocados.

**E ele refina o 763 em vez de confirmá-lo:** o maior resíduo **fora** do
`labtreinamento` passou de 1,6 para **2,8**, e a dominância daquele canal na
série caiu de 0,818 para **0,783**. Segue acima de 0,75, logo *"0,9 a 3,7"*
continua sendo a banda do `labtreinamento` com crachá de frota — mas por menos, e
o teto de 3,7 continua vindo do `s043`.

**E A DOMINÂNCIA DA BANDA CAIU A EXATAMENTE 0,750, E O TESTE REPROVOU DE NOVO —
aprendizado 766, `alto`, e é a SEGUNDA vez em duas rodadas que ele me obriga a
reler em vez de reaproveitar.** O `epomeno-epipedo-s027` (`MNMazdcSGOc`) foi
narrado pelo **edge** (zero avisos no job `116021258977`), previa **41,3** e saiu
com **43 s** — resíduo **+1,7**, dentro da banda. Vinte e quatro de vinte e
quatro acima. A escolha do canal saiu outra vez do `concentracao_frota.py`, que
deu o DIA em **16 / 1 / 1**; entre os dois empatados em uma peça, o epomeno é o
do melhor par medido no 713.

**Dois achados, e o segundo é o que importa:**
1. **A previsão REPRODUZ nesta faixa.** O `s026`, uma hora antes, previa **41,4**
   e deu **43** — mesmo par, mesmo real. É o que o 732 havia negado e o 748 já
   tinha visto do lado curto. **ESTE ITEM PERDEU O APOIO UMA HORA DEPOIS —
   aprendizado 767, e a retratação vai aqui porque foi aqui que eu afirmei.** Os
   dois pontos do `kolejny` na MESMA faixa **invertem**: o `s025` previa **41,2**
   e deu **44**; o `s026` previa **41,6** e deu **43**. Previsão MAIOR, real
   MENOR, mesmo canal, mesma voz, mesmo provedor medido. Eu generalizei de `n=2`
   num canal — o erro de enquadramento do 679/698/725 outra vez.
   **O que eu NÃO afirmo, pelo §3.8:** que a previsão não prediga. A inversão é
   de **um segundo**, que é exatamente a granularidade do real (o YouTube
   arredonda para cima), logo ela não prova o contrário — ela só **retira o apoio
   da minha frase**. O que sobrevive é o sinal, agora com **25 pontos**.

   **E AS DUAS AFIRMAÇÕES — a minha e a retratação dela — ERAM INDECIDÍVEIS:
   aprendizado 768, `alto`.** O quinto ponto desta faixa (`epomeno-epipedo-s028`,
   41,5 → **43**) fecha a conta: **as cinco previsões caem numa janela de 0,4 s e
   o real tem passo de 1 s.** Janela mais estreita que o passo do instrumento
   **não ordena nada**, em sentido nenhum. Os reais são 43, 43, 43, 43 e **44**, e
   o único 44 vem da previsão **MENOR** da janela — o oposto de uma relação
   monótona, o que não prova desordem: prova **falta de resolução**.

   **E o 733 já havia nomeado este erro exato** ao desmontar o "paradoxo" do 732
   (três previsões dentro de 1,0 s devolvendo o mesmo inteiro). **Eu reapliquei,
   duas vezes, em duas horas, o erro que aquele aprendizado nomeia.** O que
   sobrevive dos três é só o **SINAL**: positivo em 26 de 26.

   **A regra que fica: para decidir reprodutibilidade é preciso previsão separada
   por MAIS de 1 s** — isso é DESENHO, não releitura dos dados que já existem.
   `tests/test_a_janela_de_previsao_e_mais_estreita_que_o_instrumento.py`, seis
   testes, e um deles **reprova quando a janela passar de 1 s**, porque aí a série
   passa a poder ordenar e esta nota tem de ser relida.

   **E O SEXTO PONTO DA MESMA JANELA FORTALECEU ISTO, além de derrubar o PISO da
   banda — aprendizado 769, `alto`.** O `kolejny-poziom-s027` (`djz6oq7m4eE`)
   previa **41,5** no edge (provedor medido, zero avisos no job `116106368092`) e
   saiu com **42 s**: resíduo **+0,5 s**, que **quebra o piso de 0,9** que vinte e
   seis pontos sustentavam. É a **primeira vez que o piso se move** — o teto se
   moveu no 752. `RESIDUO_OBSERVADO` passou a **(0,5; 3,7)** e a largura foi de
   2,8 para **3,2 s**: a banda ficou **ainda menos útil** como previsão, e isso
   vai dito. Vinte e sete de vinte e sete seguem positivos.

   **E o que importa mais é o efeito na janela:** os reais passaram de
   43/43/43/43/44 para **42/43/43/43/43/44** — **três inteiros de espalhamento
   contra 0,4 s de largura de previsão**. Logo a propriedade que eu havia travado
   (*"o real é quase constante"*) era **acidente de amostra pequena**, e a certa é
   outra: **a dispersão do real não cabe na largura da previsão.** Uma previsão
   que varia 0,4 s não produz 2 s de real por relação nenhuma — o que produz isso
   é o que a previsão **não modela**. O teste foi **reescrito no lugar** como
   `test_o_real_da_janela_ESPALHA_mais_do_que_a_previsao_explica`.

   **E um terceiro efeito, que eu declaro em vez de comemorar:** no 740/748 a
   janela **otimista** abriu de menos de 1,0 para **1,11 s**, porque ela depende
   do PISO. Isso **não alivia a contradição** — o caso que de fato ocorreu duas
   vezes é o **pessimista**, que depende do teto e segue sem interseção.
   **Quatro testes meus reprovaram** com a queda do piso, e os quatro foram
   corrigidos no lugar.
   **E ÀS 22:2x A FRASE "N DE N ACIMA" CAIU — aprendizado 770, `alto`, e ela
   nunca foi inteira.** O `epomeno-epipedo-s029` (`AINVslOwBJM`) previa **41,9**
   no edge (provedor MEDIDO, zero avisos no job `116135075389`) e saiu com
   **42 s**: resíduo nominal **+0,1**, que derruba o piso de 0,5 do 769. **E o
   sinal DESTE ponto não está estabelecido:** o YouTube arredonda **para cima**,
   logo real 42 significa duração verdadeira em **(41; 42]**, e a previsão de
   41,9 cai DENTRO desse intervalo — o resíduo verdadeiro está em
   **(−0,9; +0,1]** e pode ser negativo.

   **O critério é aritmético: o sinal só está estabelecido quando
   `real − previsão > 1,0`**, porque só aí a janela de arredondamento fica toda
   acima da previsão. Conferida a série, **três dos 28 pontos não passam** — e
   são exatamente **os três que definiram o PISO da banda** ao longo do tempo: o
   `epomeno-epipedo-s024` (+0,9, piso do 734), o `kolejny-poziom-s027` (+0,5,
   piso do 769) e este (+0,1). Logo o que eu venho escrevendo desde o 734 é, na
   verdade, **25 de 28 estabelecidos**, e entre esses o piso nominal é **1,1**.

   **É a terceira vez em dois dias que o limite do INSTRUMENTO aparece como se
   fosse achado** (733, 768, agora este), e a assinatura é a mesma: ler o inteiro
   como se fosse a medida.

   **O que NÃO cai:** o teto de 3,7 vem do `labtreinamento-s043` (23,3 → 27,
   folga de 3,7, muito acima de 1,0), logo é ponto **estabelecido**; e cobrar a
   faixa nos dois mundos segue certo.

   **As duas consequências práticas, e as duas são pioras:** (1) a banda foi a
   **(0,1; 3,7)**, largura **3,6 s** contra 1 s de granularidade — ela cobre
   quase quatro inteiros de real e informa cada vez menos; (2) por isso o relato
   do `labtreinamento-s034` caiu de *"PASSA do teto da mira"* para *"pode passar
   do teto"* — **o aviso FORTE virou fraco numa peça cujo real foi 28**. As duas
   vão ditas em vez de escondidas, e há teste cobrando cada uma.
   `tests/test_o_sinal_do_residuo_nem_sempre_esta_estabelecido.py`, sete testes,
   um deles **falha se o piso subir** (porque aí alguém o reescreveu à mão) e um
   **falha se o aviso forte voltar**. Cinco testes meus foram corrigidos no
   lugar; a janela otimista do 740/748 abriu de 1,11 para **1,51 s**, e isso
   **não alivia** a contradição — o caso que ocorreu é o pessimista, que depende
   do teto e segue sem interseção.

   **E O 30o PONTO REFINA O 770, corrigindo uma frase minha de uma hora antes.**
   O `epomeno-epipedo-s030` (`oMQSIMx92c0`) previa **41,6** no edge (provedor
   medido, zero avisos no job `116175136800`) e saiu com **42 s** — resíduo
   nominal **+0,4**, dentro da banda, e com o **sinal NÃO estabelecido**
   (42 − 41,6 ≤ 1,0). **Mas ele NÃO moveu o piso.** Logo a frase que eu escrevi
   no 770 — que os não-estabelecidos eram *"exatamente os que definiram o PISO"*
   — era coincidência de três pontos. **A implicação vale de um lado só:**
   resíduo pequeno o bastante para ser piso é necessariamente pequeno o bastante
   para não ser estabelecido; a volta não vale. Estabelecidos: **26 de 30**, e o
   teste foi **reescrito no lugar** para cobrar a implicação num sentido e exigir
   que exista não-estabelecido que não seja o piso.

   **E o 29o ponto, uma hora depois, e ESTABELECIDO:** o `kolejny-poziom-s028`
   (`lmBOUA-uAgY`) previa **41,6** no edge (provedor medido, zero avisos no job
   `116154957122`) e saiu com **43 s** — resíduo **+1,4**, dentro da banda, e com
   `43 − 41,6 > 1,0`, logo a janela de arredondamento fica toda acima da previsão.
   **Os estabelecidos vão a 26 de 29**, `RESIDUO_N` = 29, limites intocados. Dois
   testes meus que cravavam 28 foram corrigidos no lugar — é a contagem fazendo o
   trabalho dela, não achado novo.

2. **A frase do 763 perdeu o apoio da CONTAGEM.** Com o `kolejny-poziom-s025` e
   este, a dominância do `labtreinamento` foi de **0,818 → 0,783 → 0,750**,
   saindo do `> 0,75` que eu havia cravado no teste. Seis dos vinte e quatro
   pontos são de outros dois canais, e o modo longo da previsão (41 a 44 s) foi
   de quatro para **seis**. Então *"a banda é do labtreinamento com crachá de
   frota"* **já não se diz pela contagem.**

**E ÀS 01:2x DE 15/10 O ARGUMENTO DE CONTAGEM MORREU, pelo PISO que eu mesmo
declarei.** O `kolejny-poziom-s029` (`L0dQBPurBzo`, previsão edge **41,7**,
provedor medido no job `116192969235`, real **43**, resíduo **+1,3** e sinal
ESTABELECIDO) é o 31º ponto, e com ele a dominância do `labtreinamento` caiu a
**0,581** — abaixo do 0,60 da faixa observada. **Treze dos trinta e um pontos
são de outros dois canais** e o modo longo (41 a 44 s) tem **nove**. Logo não
existe mais leitura da contagem que sustente *"a banda é de um canal"* — e o
teste reprovou pela TERCEIRA vez para me obrigar a reler em vez de mover o
número. O piso da faixa foi ao valor OBSERVADO (0,58) e **quem carrega a
afirmação agora é o teste da LARGURA**. `RESIDUO_N` = 31, 27 estabelecidos.

**E ÀS 02:3x O TESTE DA DOMINÂNCIA FOI REESCRITO, porque ele passou a reprovar
TODA rodada.** Com o `epomeno-epipedo-s031` (`V1CslnNkHRg`, 41,6 → **43**,
resíduo **+1,4**, sinal estabelecido, 32º ponto) a dominância caiu a **0,563** —
e, com o contador de canal mandando produzir nos outros dois canais, a faixa de
dois lados reprovaria a cada peça nova. **Teste que reprova sempre deixa de
avisar**, que é exatamente o argumento pelo qual o `mira.py` não virou portão
(44 avisos). E ele reprovava medindo um número cuja afirmação eu **já havia
retratado** uma rodada antes.

Ficou a forma **monótona** do que sobreviveu: `dominância < 0,75`, isto é, ela
não voltou ao patamar em que a frase se dizia pela contagem — não precisa de
edição a cada ponto, e **reprova se subir de novo**, que é o caso que exige
releitura. `RESIDUO_N` = 32, 28 estabelecidos.

**O que ainda sustenta a frase é só a LARGURA**, e isso é mais honesto do que o
que eu vinha escrevendo: o teto de **3,7 continua sendo o `labtreinamento-s043`**
e **nenhum ponto de outro canal passou de +2,8**. É a largura que define a faixa
impressa no relato do `mira.py`, logo é ela que importa para quem usa a banda.

**No código:** o limiar do `test_a_banda_e_de_UM_canal.py` deixou de ser
`> 0,75` e passou a ser a **faixa OBSERVADA** (0,60 a 0,82), que reprova nos dois
sentidos, mais um teste novo que cobra a **largura** em vez da contagem — ele
falha se um canal não dominante encostar no teto da banda. `RESIDUO_N` = 24;
os limites da banda seguem intocados.

**E o vigésimo quinto ponto é o do 767:** `kolejny-poziom-s026`
(`TpqcjfLsreg`), provedor **edge** medido (zero avisos no job `116049268931`),
previsão **41,6** e real **43** — resíduo **+1,4**, dentro da banda. **Vinte e
cinco de vinte e cinco acima.** `RESIDUO_N` = 25, limites intocados, e a
dominância do `labtreinamento` na série caiu a **0,720** — dentro da faixa
observada (0,60 a 0,82) que o 766 passou a cobrar, em vez de reprovar.

**E o canal saiu do contador pela TERCEIRA rodada seguida** (762/765/767): o
`concentracao_frota.py` com `por_dia=` deu o dia em **16 / 2 / 1**, e a peça saiu
do mais baixo. Isso já não é achado, é procedimento — o que vale guardar é que
ele sobreviveu a três rodadas sem eu voltar ao canal que estava aberto na minha
cabeça.

**E O `pacotes` DO `frota.yml` É LISTA DE OBJETOS — aprendizado 738.** Eu mandei
`["labtreinamento-s034"]` e o run `38476203962` morreu: o job `preparar` dá
**SUCCESS** (o `jq` monta `{include:[...]}` de qualquer coisa) e o run dá
**FAILURE** com `matrix.pacote` vazio e **zero anotação útil**. A forma certa está
escrita na descrição do próprio input:
`[{"canal":...,"pacote":...,"idioma":...}]`. **Quarta vez da mesma assinatura** —
payload montado à mão contra uma forma que o arquivo documenta (718, 729, 702).

**E A LEITURA DE SOM VOLTOU, de graça, na anotação do render:** `labtreinamento-s034`
com **LUFS −13,7**, LRA 2,8, pico −2,2 dBTP, desvio do alvo 0,3 e **nenhum
silêncio**. Era um item meu em aberto desde o `s020`, e ele não exigia baixar
artefato nenhum: sai pelo `::notice:: SOM` do próprio job.

## A MIRA PAROU DE CONFERIR E DISSE QUE NÃO HAVIA MIRA — e eram TRÊS donos do canal

**Medido em 19/10 às 05:2x, escrevendo o `labtreinamento-s083`.** O relato do
`mira.py` saiu com `canal 'labtreinamento-s083' nao tem ALVO_POR_CANAL medido` —
e aquele canal TEM mira medida desde 09/10 (20,0 a 26,0).

**A causa é a assinatura de sempre: `mira.confere` lia `spec["slug"]` como se
fosse o canal.** Enquanto a spec de short solto trazia `slug: "labtreinamento"`
as duas coisas coincidiam por acidente; quando o `slug` passou a ser o PACOTE, o
canal deixou de ser achado no `ALVO_POR_CANAL` e o instrumento passou a devolver
`tem_mira: False`. **A falha é PERMISSIVA — ele não reprova nada, só para de
avisar**, que é o pior sentido, o mesmo do corpus atrasado.

**O custo está medido e é de SEIS peças:** da `s077` à `s082`, publicadas com a
mira nunca conferida — e nas seis eu escrevi na copy *"os dois DENTRO da mira
medida do canal"* **fazendo a conta de cabeça**. É literalmente o item 3 da §10:
toda conta que eu faço à mão vira um erro meu.

**E eram TRÊS donos da mesma regra, não dois.** O `tally_fora_da_mira`, escrito
depois, derivava CERTO com `pacote.rsplit("-s", 1)[0]`. E o
`registro_videos.linhas_dos_notices` lia o `slug` para a coluna `canal` de
`videos`: varrido o pendente, **DEZENOVE linhas parqueadas estavam com
`canal = '<canal>-s0NN'`, nos TRÊS canais** — de `kolejny-poziom-s060`,
`epomeno-epipedo-s060` e `labtreinamento-s077` em diante. **Elas não chegaram ao
banco porque o `execute_sql` está negado, e isso é sorte e não método:** com elas
dentro, a coluna que o `concentracao_frota` e a `estoque.sql` agrupam ficaria
cega. As dezenove foram reconstruídas.

**Consertado com UM dono: `fabrica/canal.py`**, com `da_spec` e `do_pacote`, e os
dois chamadores passaram a usá-lo. **E ele reprovou a primeira versão da `s083`
(edge 26,1 contra teto 26,0) antes do render** — a primeira peça em sete em que o
instrumento de fato conferiu.
`tests/test_a_mira_deixou_de_conferir_quando_o_slug_virou_PACOTE.py`, oito
testes: a varredura sai do DISCO e **reprova se ficar vazia**, um exige que a
convenção NOVA de slug continue existindo (senão o arquivo passa por vacuidade),
um é contraprova no outro sentido — **canal sem mira segue sem mira**, porque
inventar faixa seria pior que a cegueira —, um varre a fábrica INTEIRA por AST
procurando quem volte a derivar canal sozinho, e um cobra a coluna `canal` do
pendente. **Contraprova nos dois sentidos:** desligado o conserto, três dos oito
falham; e uma cópia CERTA da derivação em outro módulo também reprova, porque o
que o teste cobra é haver UM dono, não a conta estar certa duas vezes.

## ACRESCENTAR PONTO NA SÉRIE DEIXOU DE SER PASSO MEU

**O terceiro passo manual a menos (§11-bis), e ele é o que já corrompeu dados
DUAS vezes.** Acrescentar um ponto de resíduo era eu editar dois arquivos à mão:
a lista `SERIE` dentro do teste que a ancora e o `RESIDUO_N` no `mira.py`. Foi
assim que nasceu o ponto FANTASMA de 18/10 às 11:2x — `replace` casando PREFIXO
de linha, porque a âncora que eu escrevia não tinha o comentário `# job` que a
linha no arquivo tem.

`fabrica/serie_residuo.py` lê a série por **AST** (e **não a migra**: mover a
lista para um `.json` criaria um terceiro dono e perderia os comentários de
procedência, que são o que distingue ponto medido de número escrito), insere por
**LINHA INTEIRA**, **recusa** pacote repetido, job repetido e provedor não
MEDIDO (733), e **sincroniza o `RESIDUO_N` no mesmo passo** — logo os dois não
podem mais divergir. O `limites()` **deriva** a banda da série, e há teste que
reprova se ela divergir do `RESIDUO_OBSERVADO` escrito à mão no `mira.py`: duas
contas da mesma coisa têm de concordar.

**Primeira execução em produção foi o ponto da `s083`** (25,1 → 29, resíduo
**+3,9**, estabelecido, **a 0,1 s do teto da banda**), e o diff saiu com uma
linha só e o comentário anterior intacto.
`tests/test_a_serie_do_residuo_deixou_de_ser_passo_meu.py`, onze testes, um deles
gravando numa CÓPIA para provar a inserção sem tocar o arquivo real.

## O PORTÃO NÃO COBRA A CHAVE QUE O RENDER EXIGE — medido em 18/10 às 08:1x

**O `epomeno-epipedo-s058` passou os ONZE portões do `prontidao` e o render morreu
em `KeyError: 'longo'`.** Eu escrevi a spec de short solto sem o campo
`"longo": []` — lista VAZIA, porque não há longo a renderizar — e nenhum portão
olha para isso: eles conferem duração nos dois mundos, identidade, variedade,
ortografia, título duplicado, similaridade e números. **Nenhum abre a spec como
o render a abre.**

O custo foi um run inteiro: o `39110638169` instalou o ffmpeg, baixou as **três**
trilhas do incompetech e só então estourou, com `::warning:: No files were found`
no lugar de causa. **E o `KeyError` NÃO sai pelas anotações** — o que o job
emitiu foi o aviso do artefato vazio, que é indistinguível de render que não
produziu arquivo por outro motivo. A causa saiu do LOG, e nesta sessão o `gh`
recusa o redirecionamento para o blob (`refusing a redirect to
productionresultssa14.blob.core.windows.net`), logo a leitura foi `curl -sL` **no
sandbox do Composio** sobre a URL assinada que o `get_job_logs` devolve. Fica
registrado porque é a terceira rota para ler job, ao lado do MCP e das anotações.

**A regra que fica: ausência de chave não é valor vazio.** E o portão que nunca
lê a spec pelo caminho do render não protege contra isso — é o §3.8 outra vez,
com verde fabricado antes de um `KeyError`.

**NÃO virou portão novo**, e o motivo é o do `mira.py`: varrido o disco, **zero**
das specs de short solto estão sem a chave, logo o buraco é **LATENTE** e o lugar
dele é a suíte. `tests/test_o_portao_nao_cobra_a_CHAVE_que_o_render_exige.py`,
sete testes — um varre toda spec de short solto, um **falha se a varredura ficar
vazia** (que é o defeito do 743 em forma de glob), um **falha se alguém
transformar isto em portão**, e um distingue chave ausente de lista vazia. **E o
assert da contraprova estava ERRADO na primeira execução:** eu escrevi que o
`.get` mascara a diferença, e o `.get` **nu** devolve `None`, que é distinguível
de `[]`. Quem mascara é o **default** — `get(k, [])` —, e foi corrigido para
cobrar as três comparações.

## CONSUMIR A PAUTA REPROVA O TESTE QUE ANCORA NELA — medido em 18/10 às 09:2x

**SETE testes meus reprovaram porque a rodada FEZ O QUE ELES MEDIAM**, e nenhum
deles media um limiar: seis do `test_origem_sem_uso_contava_ID_e_nao_TITULO.py`,
escrito por mim **um dia antes**, e um do `test_pauta_local.py`.

A causa é uma só. O arquivo das seis cópias cravava a **lista exata** das origens
de zero usos do `kolejny` e o id da que fica depois do colapso — e esta rodada
**consumiu a primeira delas** (`SZV9Vk5YFwI` virou o `kolejny-poziom-s059`). Logo
sobram cinco, a que fica é outra, e a inflação é quatro em vez de cinco. **É a
classe do 743/753/761 — identidade onde havia propriedade — pela QUARTA vez.**

**A propriedade era outra, e é ela que ficou cobrada:** das cópias do grupo, as
que **ainda não renderam short** saem uma a uma sem o mapa de títulos e colapsam
em **UMA** com ele, que é a **primeira delas na ordem viva**. Isso vale com seis,
com cinco e com duas — e os testes agora **derivam** o conjunto livre em vez de
listá-lo, com um assert que **falha dizendo que perdeu a âncora** quando sobrar
menos de duas, em vez de passar por vacuidade.

**E o sétimo é mais interessante, porque o teste estava CERTO ao reprovar.** Ele
cobrava `ids > grupos` sobre `pauta_local.livres()` e disse *"sem nenhum grupo com
cópia, este teste não está medindo nada"* — exatamente o que havia acontecido: a
origem consumida era o último grupo com cópia do retrato de 06/10. **Ele media no
lugar que o consumo esvazia.** A confusão entre ID e GRUPO que produziu o "cinco"
de 12/10 mora no **AGRUPAMENTO**, que não depende de a pauta ter andado; sobre
`livres()` a diferença é consequência. Reescrito para medir no acervo, com o caso
vazio **dito** em vez de reprovado.

**A regra que fica: teste que ancora em id de origem LIVRE reprova quando a pauta
for consumida — e consumir pauta é o trabalho.** Ancore na propriedade e derive o
id do estado vivo, ou o teste passa a punir a produção. A nota de 17/10 às 20:1x
já descrevia isto nos dois testes do `pauta_viva` que ancoravam no `eZ697VNYCPU`;
**eu escrevi o arquivo das seis cópias no dia seguinte com o mesmo defeito.**

## A SERIE DO RESIDUO PAROU DE CRESCER POR FALTA DE INSTRUMENTO — 18/10, 09:0x e 10:1x

**Duas rodadas seguidas sem ponto de resíduo**, e a causa está medida nas duas:
o controle `OhrGlJvnBoM` (44 s conhecidos, lido às 08:1x) voltou **vazio** às
09:0x e outra vez às 10:1x, e com ele as peças recém-publicadas. `RESIDUO_N`
está congelado em **90** desde o `epomeno-epipedo-s058`.

**O que isto NÃO é:** peça que não indexou. O discriminador do 17/10 às 03:1x é
exatamente este — peça de minutos e peça de dias falhando na MESMA chamada é a
rota, não a indexação — e ele foi aplicado antes de concluir nas duas rodadas.

**E o parque está fazendo o trabalho dele:** o `duracao_a_medir` tem **32**
linhas com **duas** sem leitura, e elas entram na banda no minuto em que a rota
abrir. Isso é o 726 ao contrário: o passo que **tem** instrumento sobrevive à
rodada em que eu não consigo medir. Antes do parqueamento incondicional das
06:1x, estas duas peças teriam saído da série sem registro.

**O que fica dito em vez de estimado:** a banda de `(−0,6; 4,0)` é de ontem, e
qualquer peça publicada nestas duas rodadas é **ponto futuro**, não ponto. Eu
não leio resíduo de leitura que a rota não deu.

## O QUARTO NEGATIVO SAIU DA JANELA ESTREITA — e o piso da banda foi a −1,2

**Medido em 18/10 às 11:1x.** O `epomeno-epipedo-s059` (`-zbvpX7peIU`) previa
**42,2** no edge — provedor MEDIDO (zero avisos `NARRACAO PELO PIPER` no job
`117660019973`) — e saiu com **41 s reais**: resíduo **−1,2**, **estabelecido**
pelo ramo negativo (real 41 significa duração em `(40; 41]`, e 42,2 está acima de
todo esse intervalo).

**É a SÉTIMA correção da banda, e a segunda que move o piso para baixo:**
`RESIDUO_OBSERVADO` foi a **(−1,2; 4,0)**, largura de 4,6 para **5,2 s** contra
1 s de granularidade. As sete correções **alargaram** — nenhuma estreitou — e isso
é propriedade de limite definido pelo extremo observado. A banda informa cada vez
menos, e isso vai dito.

**O que ele acrescenta não é a contagem, é o LUGAR — e ele derruba uma frase
minha.** Eu escrevia desde o 17/10 que o negativo *"mora na janela estreita"* de
41,4 a 41,6. **Este é o primeiro negativo FORA dela:** previsão 42,2, isto é
0,6 s acima do maior dos três anteriores. Os quatro seguem sendo do
`epomeno-epipedo`, mas a janela do negativo passou de **0,2 s para 0,8 s**, e o
que sobra é mais fraco e verdadeiro: **o negativo é raro (4 de 93), é deste
canal, e não está confinado a um ponto da previsão.**

**E a pinça do 740/748 NÃO melhorou com isso.** O piso mais baixo abre a janela
otimista, e o caso que de fato ocorreu **doze vezes** é o pessimista, que depende
do **teto** — intocado em 4,0. `RESIDUO_N` = 93.

## O MEU `replace` CASAVA PREFIXO DE LINHA, e a série do resíduo ganhou um ponto FANTASMA

**Medido em 18/10 às 11:2x, porque `RESIDUO_N` e `len(SERIE)` divergiram: 93
contra 94.** O `epomeno-epipedo-s058` estava na série **duas vezes**.

A causa é a forma como eu acrescento ponto, e ela é minha:

    t.replace(ancora, ancora + "\n" + linha_nova)

**A âncora que eu escrevo é a linha SEM o comentário de job** — por exemplo
`("labtreinamento-s075", 25.8, 29, "edge"),` — e a linha no arquivo **TEM**
comentário. Logo o `replace` casa um **PREFIXO**: a linha nova entra no MEIO da
antiga, e o comentário que estava no fim dela fica pendurado no fim da NOVA.
Repetido por seis rodadas, isso acumulou **seis jobs numa linha só**, apagou a
procedência das linhas anteriores e por fim duplicou um ponto, quando uma âncora
passou a casar dentro da linha corrompida.

**E o `assert t.count(ancora) == 1` que eu uso para me proteger NÃO pega isso:**
o prefixo é único mesmo quando a linha inteira não é. A guarda media o que eu
pedi, e o que eu pedi era insuficiente — a assinatura do §3.8 **dentro da
própria guarda**, que é a mesma forma do `or True` de 16/10.

**A consequência na medição vai dita:** a banda contava um ponto que não existe.
Nenhum limite mudou (o duplicado era +0,5, bem dentro), mas **`RESIDUO_N` é
número que eu reporto ao dono, e ele estava errado por um** desde a rodada das
09:0x. Agora são **93** pontos, zero repetidos, e os nove comentários de job das
últimas rodadas foram reconstruídos um a um.

**A regra que fica: âncora de `replace` é a linha INTEIRA, ou insira por LINHA —
e confira a contagem de pontos DISTINTOS depois de gravar.**
`tests/test_a_serie_do_residuo_nao_aceita_ponto_DUPLICADO.py`, seis testes: um
proíbe pacote repetido, um proíbe duas marcas `# job` na mesma linha (o sintoma
visível antes da duplicata), um exige que `RESIDUO_N` bata com o arquivo — foi
essa divergência que revelou tudo —, um proíbe o mesmo job em dois pontos, e um
**falha se a varredura ficar vazia**, porque um regex que deixa de casar faria
todos passarem.

## OS CINCO NEGATIVOS TEM O MESMO REAL, e isso NAO e um regime — e o PISO do espalhamento

**Medido em 18/10 as 17:2x, no QUINTO negativo.** O `epomeno-epipedo-s061`
(`7mm9Frw_tbE`) previa **41,5** no edge — provedor MEDIDO (zero avisos
`NARRACAO PELO PIPER` no job `117736668345`) — e saiu com **41 s reais**:
residuo **-0,5**, estabelecido pelo ramo negativo e **dentro** da banda (o piso
segue -1,2). `RESIDUO_N` = 99.

**O que ele acrescenta e uma propriedade que eu nao tinha olhado: os CINCO
negativos tem real EXATAMENTE 41.** Varridos da serie:

| peca | previsao | real | residuo |
|---|---|---|---|
| `epomeno-epipedo-s054` | 41,6 | **41** | -0,6 |
| `epomeno-epipedo-s055` | 41,5 | **41** | -0,5 |
| `epomeno-epipedo-s057` | 41,4 | **41** | -0,4 |
| `epomeno-epipedo-s059` | 42,2 | **41** | -1,2 |
| `epomeno-epipedo-s061` | 41,5 | **41** | -0,5 |

**Logo o negativo nao e "a previsao erra para cima neste canal" — e o inteiro
41 aparecendo.** As previsoes variam (41,4 a 42,2) e o real nao varia nada: o
residuo negativo e so a distancia entre uma previsao qualquer da janela e o
MENOR real que essa janela produz. Nesta mesma janela o canal ja deu 42, 43 e
44, logo 41 e o **piso do espalhamento** descrito no 769/771, nao um regime
proprio.

**E isso retrata, pela terceira vez, a forma como eu descrevia a coisa.** No
17/10 eu escrevi que o negativo *"mora na janela estreita"*; em 18/10 as 11:1x o
quarto ponto saiu dela e eu escrevi que *"nao esta confinado a um ponto da
previsao"*. As duas frases olhavam a PREVISAO. **A regularidade esta no REAL**, e
ela e mais simples: **os cinco negativos sao os cinco casos em que o real deu o
menor inteiro da janela.**

**O que isto NAO prova:** que o canal grego produza 41 com mais frequencia que
os outros produziriam, nem que 41 seja um piso fisico. Cinco pontos de um canal,
e o 679/698/725 nomeia esse enquadramento. **O que esta medido:** o negativo e
raro (5 de 99), e deste canal, e **em todos os cinco o real e o mesmo inteiro**.

**E EM 19/10 ÀS 02:3x ISTO FOI CONFIRMADO PELO OUTRO LADO DA JANELA.** O
`epomeno-epipedo-s064` (`ANxWQYgtUAY`) previa **41,6** no edge — provedor MEDIDO
(zero avisos `NARRACAO PELO PIPER` no job `117861303311`) — e saiu com **44 s
reais**: resíduo **+2,4**, **estabelecido** e dentro da banda. **Mesma janela de
previsão dos cinco negativos (41,4 a 42,2), e o real deu o MAIOR inteiro dela.**
Logo o 41 dos negativos é o **piso do espalhamento**, não regime do canal — que é
exatamente o que a nota acima afirma, agora com o ponto do outro extremo.
`RESIDUO_N` = 107, limites intocados. **E a copy declarou a exposição antes de
publicar** (40,4 a 45,6): o real caiu dentro, e isso **prova pouco**, porque a
banda tem 5,2 s de largura contra 1 s de granularidade.

**A consequencia pratica e de redacao, nao de parametro (§10):** mirar o PISO da
mira neste canal nao reduz o real — ele ja esta no fundo da janela. O que a mira
baixa faz e aumentar a chance de o residuo sair NEGATIVO, e isso vai declarado
na copy em vez de vendido como protecao.
`tests/test_os_cinco_negativos_tem_o_MESMO_real.py`, sete testes — um varre a
serie e exige que todo negativo tenha real igual, um **falha se aparecer
negativo com real diferente** (porque ai esta nota tem de ser relida), um trava
que eles sao do mesmo canal e um **falha se a varredura ficar vazia**.

## O MEU CRITERIO DE SINAL PERDIA A BORDA DO INTERVALO — e ele e do 770

**Medido em 18/10 as 15:2x, no PRIMEIRO ponto que caiu exatamente nela.** O
`kolejny-poziom-s061` (`7p8S5XIQA0M`) previa **42,0** no edge — provedor MEDIDO
(zero avisos `NARRACAO PELO PIPER` no job `117710246704`) — e saiu com **43 s
reais**: residuo nominal **+1,0**, e o `_sinal` devolveu **0**, isto e "nao
estabelecido".

**E a aritmetica diz que ele ESTA estabelecido.** O YouTube arredonda para cima,
logo real 43 significa duracao verdadeira em `(42; 43]`, e com previsao 42,0 o
residuo verdadeiro vive em `(0; 1]` — **cada valor desse intervalo e
estritamente positivo.** O intervalo e **ABERTO embaixo**, e e exatamente isso
que o meu criterio nao respeitava: eu escrevi `real - previsao > 1,0` quando a
condicao certa e `>= 1,0`.

**Logo o criterio do 770 era SUFICIENTE e nao necessario**, e chamava de
indecidivel um sinal provado. Nao e afrouxamento nem limiar novo: e a mesma
aritmetica daquele aprendizado com a desigualdade certa na borda do intervalo
que ele proprio descreve.

**Dois pontos da serie moram nessa borda, e os dois sao `42,0 -> 43`:** este e o
`kolejny-poziom-s043`, que estava contado como nao estabelecido **desde o 770** —
logo a contagem de estabelecidos que eu venho reportando estava baixa por um
desde aquele dia. O ramo NEGATIVO **nao muda**: `(d-1, d]` so e todo negativo
com `d < 0`, porque com `d == 0` o intervalo e `(-1; 0]` e contem o zero.

**A regra que fica, e e a do 771 numa forma mais fina: criterio sobre INTERVALO
tem de respeitar de que lado ele esta ABERTO.** No 771 eu escrevi um criterio
com um ramo so porque estava olhando para um lado; aqui eu escrevi os dois ramos
e errei a BORDA de um deles.
`tests/test_o_criterio_do_sinal_perdia_a_BORDA.py`, seis testes — um varre a
vizinhanca da borda nos dois sentidos, um trava que o ramo negativo nao mudou, um
**falha se os dois pontos da borda sairem da serie** (sem eles o arquivo nao mede
nada) e um **falha se o MOTIVO sair do modulo**, porque conserto sem motivo
escrito volta calado.

## O timeout do `execute_sql` no UPDATE correlaciona com o TAMANHO do texto

**Observado em 13/10, quatro tentativas, e refina o aviso 621 — que eu vinha
tratando como "intermitente".** Nesta sessão:

| chamada | texto | resultado |
|---|---|---|
| `update ... evidencia = evidencia \|\| <jsonb grande>` | ~800 ch | **timeout 60 s** |
| idem, segunda tentativa | ~700 ch | **timeout 60 s** |
| `update ... invalidado_motivo = <texto longo>` | ~900 ch | **timeout 60 s** |
| `update ... status='invalidado'` | ~55 ch | **passou** |
| `update ... invalidado_motivo = <texto curto>` | ~130 ch | **passou** |

**Quatro de quatro longos estouraram; dois de dois curtos passaram.** E `INSERT`
com `evidencia` jsonb grande passa sem problema — então **não é o tamanho do
payload em geral, é o UPDATE com texto longo.** Isto é `observado`, não `medido`:
n pequeno e eu não controlei a hora nem a carga.

**O procedimento que sai disso:** retratação vai em **dois statements curtos** —
`status` primeiro, `invalidado_motivo` resumido depois, com o detalhe vivendo no
registro NOVO. E **confira com `select` depois de cada um**, porque o timeout
**não** aplica a mudança e eu já relatei como feito o que não tinha sido.

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

**E ESSA MESMA FRASE ERA UM DEFEITO NO PORTÃO, medido em 15/10 às 08:2x —
aprendizado 773, `crítico`.** O corpus guarda o `## TITULO SHORT`, e o
`prontidao._titulo_do_copy` devolvia o `## TITULO` **LONGO**. Logo a trava de
título idêntico **comparava uma forma contra um corpus da outra, e não podia
casar nunca** em short solto.

**O custo foi medido e é exatamente UM:** o `labtreinamento-s051`
(`iRSJ6w03lj0`) foi ao ar com o MESMO título curto do `labtreinamento-s038`
(`EgcUqRhx9IY`) — *"Conclusão não é situação"* — e com a **mesma família de
entrada errada**. Os doze portões passaram. Varridas todas as specs, essa é a
**única** colisão de título curto da frota inteira.

**E a mesma causa cegava um SEGUNDO portão:** o `_titulos_do_canal` atribui canal
cruzando specs com o corpus, também pelo título longo — **zero** specs do
`labtreinamento` casavam, logo a similaridade "contra o MESMO canal" comparava só
títulos de geração antiga, nunca os cinquenta shorts que estão no ar.

**E é a MESMA CLASSE de erro que o docstring daquela função já descrevia**, uma
camada adiante: a primeira versão dela lia a DESCRIÇÃO pela linha `# `.
Consertaram a leitura da spec e não a correspondência com o corpus.

Agora `_titulos_do_copy` devolve **lista** (o curto primeiro) e
`_outra_spec_com_o_titulo` evita reprovar peça publicada contra a própria
publicação — portão que reprova sempre deixa de avisar, que é o argumento do
`mira.py`. **Ponto cego declarado no código:** spec nova que copie título de peça
antiga SEM spec no disco passa, porque o corpus é lista nua e não diz de quem é o
título. `tests/test_o_corpus_guarda_o_titulo_curto.py`, sete testes.

**A peça publicada NÃO foi apagada** — apagar vídeo publicado exige o dono.

**No código:** `fabrica/corpus_atrasado.py` (`titulos_dos_notices`, `faltantes`,
`aplicar`, `relato`) e dez testes ancorados nos sete títulos reais. O
`titulo=` do próprio notice é a forma certa; linha com `youtube_id=?` (run
abortado) **não entra**. Rode depois de publicar:

    <notices do retomar.yml> | python3 fabrica/corpus_atrasado.py --aplicar

### E O REGISTRO TEM DOIS PASSOS — eu automatizei um e PERDI o outro

**Aprendizado 726, `alto`, medido em 13/10 às 14:1x.** Eu fui gravar métrica das
doze peças de hoje e levei:

    violates foreign key constraint "metricas_youtube_id_fkey"
    Key (youtube_id)=(CdUiplaeP5g) is not present in table "videos"

**As doze peças publicadas hoje não tinham linha em `videos`** — o passo que a
§9 da rotina pede em letra, *"registro: linha em `videos` COM `origem_id`"*, e
que eu não fiz nenhuma vez em doze publicações.

**A causa é sobre automatizar pela metade, e é o que vale guardar.** O registro
manual tinha DOIS passos: o título no `corpus_publicados.json` e a linha em
`videos`. Medido no banco, as linhas de `videos` existem até o
`labtreinamento-s025` (12/10 às 23:12) e **param ali — exatamente onde eu escrevi
o `corpus_atrasado.py`**, às 00:2x de hoje. Dei instrumento a um dos dois passos,
passei a fazer aquele com disciplina, e **soltei o que não tinha instrumento**.

**E a falha é RUIDOSA, não permissiva** — ao contrário da do corpus. Só que ela
só levanta **quando alguém tenta medir**, e eu não tentei por catorze horas.
**Barulho que ninguém ouve é silêncio.**

**E a medição do tamanho quase saiu inflada, pelo efeito (C):** eu montei à mão
uma lista de pacotes suspeitos e ela trouxe `kolejny-poziom-s020` e `-s021` como
faltantes. **Esses pacotes não existem** — nem spec, nem publicação. O atraso real
era exatamente as doze de hoje.

**No código:** `fabrica/registro_videos.py` (`linhas_dos_notices`, `sql_insert`,
`relato`) e onze testes ancorados nos doze notices reais. Ele lê **a mesma fonte**
do `corpus_atrasado` — o notice do `retomar.yml` — para que os dois passos não
divirjam outra vez. E **não executa SQL sozinho**: imprime o `INSERT` para rodar
por `execute_sql`, com `on conflict (slug) do nothing`. Rode os dois juntos:

    <notices> | python3 fabrica/corpus_atrasado.py --aplicar
    <notices> | python3 fabrica/registro_videos.py

**Consequência extra que o `origem_id` ausente causava:** sem ele a
`consultas/estoque.sql` **não sabe que a origem foi consumida** (670) — a trava
contra reusar origem fica cega pelo mesmo motivo.

### E O MESMO DEFEITO DO 729 ESTAVA NO OUTRO MÓDULO, E EU O ESCREVI

**Medido em 15/10 às 15:2x, pelo arquivo no disco.** Eu rodei
`<notices> | python3 fabrica/registro_videos.py | tee -a docs/pendente/videos-a-inserir.sql`
e o `.sql` ficou com **três linhas de prosa portuguesa dentro** — `REGISTRO: 1
linha(s)...`, `epomeno-epipedo-s036 -> R4Ldmvcu9k8` e o conselho de rodar por
`execute_sql`. Quem abrisse o arquivo e colasse no SQL Editor levaria erro de
sintaxe nas linhas 5 a 7, e **o INSERT da linha 9 não entraria**.

**É a assinatura do 729 do outro lado.** No 729 a nota legível do
`estado_ponte.py` grudou no base64 porque **eu** redirecionei stderr para dentro
do payload; aqui ela grudou no SQL porque o **MÓDULO** a imprimia em stdout. O
conserto do 729 foi *stdout puro*, com teste — e eu **não o apliquei** ao módulo
que escrevi no 726, dois dias depois. Mesmo defeito, dois donos.

Agora o `relato` sai por **stderr** e o stdout é SQL que cola sem limpeza.
`tests/test_o_sql_parqueado_nao_leva_prosa.py`, oito testes, um deles por **AST**
(porque o docstring do módulo NOMEIA stdout para se explicar, e casar prosa
pegaria a explicação em vez do código) e um que cobra `origem_id` e
`on conflict (slug) do nothing` em **toda** linha parqueada, pelo 670.

**E o que isto NÃO conserta:** o pendente continua sendo um ARQUIVO. Sem
`execute_sql` as cinco linhas não entram em `videos`, e o 726 segue aberto.

**E NÃO MONTE O `estado_b64` À MÃO — rode `python3 fabrica/estado_ponte.py`**
(aprendizado 718), **e NÃO redirecione stderr para dentro do payload** — isto é
de 13/10 às 15:1x e é a TERCEIRA vez que o `estado_b64` montado por mim mata um
run. O run `38420599010` morreu em `base64: invalid input` porque eu escrevi
`estado_ponte.py > arq 2>&1`: o `2>&1` anexou ao arquivo a **nota legível** que
o script escreve em stderr de propósito (`estado: 269 titulos | 29396 chars
b64`), e o `tr -d '\n'` seguinte colou a nota no fim do base64. **O script já
estava certo** — eu transformei a ajuda dele em corrupção. A forma é

    python3 fabrica/estado_ponte.py 2>/dev/null | head -1

e `tests/test_estado_ponte_stdout_puro.py` (seis testes, aprendizado **729**) trava a propriedade da
qual eu dependi sem conferir: stdout é base64 **puro**, uma linha só, decodifica
sem nenhuma limpeza, e um dos testes **falha se a nota voltar para stdout**.

E o erro de 12/10 fica: o `titulos_no_ar` é lista de **OBJETOS** com a chave
`titulo`; lista de strings faz a trava por título levantar `AttributeError` e o
run morre em *"Conferir o estado antes de publicar"*. Em 12/10 eu montei à mão e
perdi o run `38290045583` — **e o docstring do próprio `estado_ponte.py` descreve
exatamente esse erro.** Código e aviso escritos não servem de nada se a rodada
não os procura antes de improvisar. A ponte continua existindo; ela
só não é mais o caminho.

## O PROMPT DA ROTINA TEM TETO DE 65.536 BYTES — e o arquivo passou dele

**Aprendizado 737, `alto`, medido em 13/10 às 21:3x pela RECUSA do servidor.** Eu
fui aplicar o `docs/ROTINA.md` corrigido no trigger e levei
`prompt must be at most 65536 bytes (invalid_prompt)`. O corpo media **68.118
bytes**, 2.582 acima — e **cruzou o teto no commit `5eb5ed9`, da rodada anterior**
(o `ab1bcc0` media 65.131). Então a sincronia arquivo↔prompt, que a própria rotina
manda fazer "passando o corpo depois da linha `---`", tinha um **limite físico que
ninguém media**.

**O que eu NÃO afirmo, pelo §3.8:** que o teto explica as divergências de 11/10 e
12/10. Medido pelos commits, o arquivo só passou do teto nesta última rodada;
aquelas foram eu **não chamar o `update_trigger`**, que é outro defeito e é meu.

**A regra que fica: quando a margem acabar, o que sai do prompt é HISTÓRIA, nunca
REGRA nem TRAVA.** O bloco migra para cá e no prompt fica a regra com o ponteiro.
Esta rodada devolveu **4,6 KB** assim — o dinamismo visual, a credencial do
GitHub, os passos da ponte pelo Composio, a composição das 25 falhas e a lista das
quedas — e `tests/test_rotina_cabe_no_trigger.py` (oito testes) reprova se o corpo
passar do teto, se a margem cair abaixo de 500 bytes, **ou se encolher tiver
removido uma trava, o passo zero do dono ou a autorização permanente.**

**Aplicado e CONFERIDO:** corpo em **64.501 bytes**, md5
`4db38df10d4abfd064afe541161fb1e7`, e o prompt gravado no trigger voltou
**idêntico byte a byte** — margem de 1.035 bytes.

**E a rodada achou DOIS documentos que ordenavam coisa errada, os dois meus:**
1. **a rotina ainda carregava os números do 691**, que o **713** retratou em 12/10
   — inscrito por peça somado por LINHA de `metricas` em vez do máximo POR PEÇA,
   inflado de 3x a 11x, **e a ordem inverte**. Quem seguisse a §1 escolheria canal
   pelo `kolejny` short (que é o QUARTO), exatamente o erro que o 713 corrigiu;
2. **a §7 ainda dizia "publicação pela ponte"**, retratado em 12/10 — ela sai pelo
   **`retomar.yml`** desde que o dono colou o `YT_OAUTH_JSON`.
É o mesmo defeito da mira do labtreinamento das 20:2x: **retratar no banco e no
`CLAUDE.md` não retrata a ROTINA**, e é a rotina que governa a rodada seguinte.

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

**E ESSE ARQUIVO NÃO EXISTIA — aprendizado 743, `alto`, medido em 14/10 às
02:3x.** Eu escrevi "está em `references/shorts-playbook.md`" aqui, na rotina, no
`docs/pipeline-canal-dark-estudado.md` e num comentário do `fabrica/ensaio.py` — e
**`git log --all -- references` não devolve commit nenhum.** Por três dias quatro
documentos apontaram para uma fonte inexistente, e um deles é a **procedência da
faixa `ALVO_POR_CANAL` do `labtreinamento` (20,0 a 26,0)**, que é parâmetro de
PRODUÇÃO: quem fosse conferir de onde vem o número chegava a um
`No such file or directory`.

**E O TESTE QUE EU ESCREVI PARA GUARDAR ISSO PASSAVA.** O
`test_a_PROCEDENCIA_das_decisoes_continua_escrita_no_codigo` exigia que a
**string** `"shorts-playbook"` estivesse no `ensaio.py` e **nunca abriu o caminho
citado**. É o §3.8 em forma de documento: portão verde fabricando "a procedência
está escrita" — ele guardava a CITAÇÃO, não a FONTE.

**Consertado, e a reconstrução vai DECLARADA dentro do próprio arquivo**, porque
ela é parte do achado: o conteúdo é a transcrição dos três itens que já governam
o código, com a procedência mista à vista, e o arquivo diz em letra que **não vale
como leitura fresca** dos repositórios. `tests/test_referencia_citada_existe.py`,
seis testes, e a contraprova nos dois sentidos: **sem o arquivo, cinco dos seis
falham**. A regra que fica: **citar caminho é afirmar que o caminho existe**, e o
teste que guarda procedência tem de ABRIR o arquivo.

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

  **E A TABELA FECHOU EM 15/10 ÀS 14:1x — aprendizado 777, `alto`, e é mais forte
  que o 709.** Na quarta rodada seguida com o `execute_sql` negado eu fiz as duas
  chamadas de catálogo: `list_organizations` e `list_projects` devolveram **200**,
  com uma org e um projeto — `imobjazz-eng's`. Isto é **byte a byte o catálogo de
  12/10, quando o acesso FUNCIONAVA.** Logo:
    * **o catálogo não informa acesso em sentido NENHUM.** O 709 provou que ele
      não prova acesso; o 777 prova que ele também não prova a FALTA dele. Eu
      concluiria hoje "o escopo mudou" e seria o mesmo erro do outro lado;
    * **o servidor MCP funciona** — duas chamadas com 200 na mesma rodada em que o
      `execute_sql` foi negado. A negação **não é servidor caído**, que era a
      hipótese barata;
    * **e a causa fica DECLARADA como indeterminada**: conector reapontado para
      outra org e permissão retirada do projeto produzem o MESMO par de respostas.
      Escolher uma seria comparador escolhido sem medir (efeito C).

  **E a consequência muda a FILA DO DONO, que é o que importa mais que a
  diagnose:** a pendência 2 da rotina diz *"não peça a reconexão do conector como
  primeira opção: ela é a PIOR das três"* — e **essa ordem pressupunha que o banco
  funcionava**, com só o REST em 402. Sem `execute_sql` não há `pg_net`, logo não
  há token, leitura de duração real, leitura de inscritos, rota da regra (h) nem
  registro em `videos`. **A reconexão passou a ser a única que devolve isso.** O
  que NÃO caiu: a publicação, que sai pelo `retomar.yml` com o `YT_OAUTH_JSON` e
  não toca o Supabase — quatro peças foram ao ar nestas quatro rodadas.
  `tests/test_o_catalogo_nao_informa_acesso_em_sentido_NENHUM.py`, oito testes, e
  um deles **falha se o catálogo deixar de ser igual ao de 12/10**, porque é a
  igualdade que sustenta a conclusão. Aviso ao dono em `docs/pendente/LEIA.md`;
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
