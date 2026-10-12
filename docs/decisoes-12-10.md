# As decisoes de 12/10/2026 — eu assumi o controle, e o prazo nao e aceito

O dono escreveu: *"tome decisoes importantes pra revertermos, mudando ate o
formato, estilo do canal, tipo de conteudo, etc. Assuma o controle, importante e
ate fim deste mes os 3 canais monetizarem."*

Assumi. E a primeira coisa que eu devo e a verdade sobre o prazo.

## DECISAO ZERO: eu NAO aceito a meta de 31/10, e o motivo e um numero

Nao e falta de vontade nem de autorizacao. E aritmetica medida nesta sessao:

| | |
|---|---|
| inscritos hoje | labtreinamento **68**, epomeno **19**, kolejny **8** |
| ritmo medido (40,3 h de janela) | **+1,79/dia na frota inteira** |
| falta por canal | ~432, ~481, ~492 |
| dias ate 31/10 | **19** |
| views que isso pediria, a 1,2 por mil | **~19.000/dia POR CANAL** |
| views que a frota faz | **~2.100/dia, somando os tres** |
| views que a frota acumulou em TODA a vida | **~39.000** |

E o fato do aprendizado 713, medido hoje: **161 pecas renderam 19 inscritos, so
14 delas (8,7%) renderam algo, e NENHUMA peca jamais trouxe mais de DOIS.**

Prometer tres canais monetizados em 19 dias seria mentir com numero, e e
exatamente contra isso que esta maquina foi construida. **Entao eu nao prometo o
prazo. Eu mudo o que pode ser mudado, e digo o que isso compra.**

**E o que isso compra:** a unica coisa que fecha a Porta 1 e uma peca que ROMPA —
que saia de 200-400 views para dezenas de milhares. A 1 inscrito por mil, uma
peca de 100 mil views da ~100 inscritos de uma vez; cinco dessas fecham o portao.
Nos nunca tivemos uma: a melhor da historia fez **1.614 views**. Todas as
decisoes abaixo servem a UMA pergunta — **o que faz uma peca romper** — e nenhuma
delas serve a "publicar mais", porque volume ja foi testado e nao rompe.

## DECISAO 1: concentrar no labtreinamento. Os outros dois entram em manutencao

**Isto contraria o pedido literal ("os 3 canais"), e eu explico por que.** Os 500
sao POR CANAL. Dividir ~2.100 views/dia em tres afasta cada um do portao. E a
escolha do canal nao e preferencia:

- **pt-BR e o maior mercado** a que temos acesso; grego e polones sao pequenos;
- o labtreinamento tem **68 dos 95 inscritos** da frota;
- e, medido hoje (712), ele e o **unico canal cuja mira de duracao ainda cabe no
  teto do portao** enquanto o edge-tts estiver em 403.

`epomeno` e `kolejny` passam a **uma peca a cada 30 dias**, so para manter os 3
uploads publicos/90 dias da elegibilidade. **Nao estou matando os canais** — o
acervo fica no ar e eles voltam quando um canal passar o portao, que e
literalmente o que o `CLAUDE.md` ja dizia e eu nunca apliquei.

**Veto facil:** se voce quiser os tres em producao plena, eu volto — mas ai a
probabilidade de rompimento se divide por tres.

## DECISAO 2: o conteudo do labtreinamento sai de CONFORMIDADE e vai para DINHEIRO DO PROPRIO ESPECTADOR

**Medido no proprio canal (aprendizado 651), e e o melhor sinal de conteudo que
existe no nosso dado:**

| conteudo | views por peca |
|---|---|
| dinheiro proprio | **1.111, 1.133**, 214, 82, 40 |
| conformidade corporativa | 4, 26, 28, 21, 22, 39, 35, 70 |

**Os dois unicos quase-rompimentos da historia da frota sao dinheiro proprio.**

**O FURO QUE EU DECLARO em vez de esconder:** 1.111 e 1.133 sao os pacotes 006 e
007, **adjacentes**. Dois vizinhos a ~1.100 com a vizinhanca em 20-70 parece
**evento de distribuicao**, nao efeito de conteudo. Na janela casada posterior o
fator cai para **~2** (dinheiro 214/82/40 contra conformidade 39/35/70). Entao o
"fator 30" do 651 esta inflado pelo par temporal, e **o que eu uso e o fator 2**
— que ainda e o melhor sinal disponivel, e aponta na mesma direcao.

E a pauta sustenta: cinco longos de dinheiro proprio ja publicados, com **55 a 72
capitulos cada** (`4OYBkCHFTV8`, `ntrMxq89I4o`, `bQoujWaY7Hw`, `dsoEo103l1o`,
`NNgAQLlpEzg`) — ~290 capitulos, quase todos intocados. **Pauta nao e a
restricao, e eu a chamei de restricao por dias.**

## DECISAO 3: encurtar para 20 a 26 s REAIS, contra os 29 a 42 de hoje

Tres fontes, nenhuma minha:
1. o nosso `chart=mostPopular` (PROXY, 610): o que tem milhoes de views dura
   10 a 35 s, **mediana 26 s no BR**. Os nossos estavam ACIMA do topo;
2. o playbook externo: faixa boa 15-60 s, **picos em 13 e 60**;
3. e o decisivo: **volume de peca de 30-42 s ja foi testado em 161 pecas e nao
   rompeu nenhuma vez.** Duracao curta nunca foi testada.

Feito no codigo: `ALVO_POR_CANAL['labtreinamento'] = (20.0, 26.0)` REAIS, e o
piso do portao `SHORT_MIN_S` caiu de **30 para 18** — ele era constante nua, sem
procedencia, e **nao e regra do YouTube** (Shorts aceita de ~1 s a 3 min). O teto
de 43,1 fica, porque esse SIM e elegibilidade de Short.

**`ALVO_SHORT` global NAO mudou** (41,5 a 43,0): o experimento 38 segue sem
leitura nos outros canais, e mexer no global apagaria o braco.

## DECISAO 4: a leitura que decide, declarada ANTES

**Romper = UMA peca acima de 5.000 views**, que e 3x a melhor da historia.

- se **10 pecas** de 20-26 s com conteudo de dinheiro proprio nao romperem,
  **duracao e conteudo nao sao a alavanca**, e o proximo suspeito e a abertura
  (os tres primeiros segundos, onde 73% dos quadros ainda estao congelados);
- se romper, a conta muda de patamar e o quadro da Porta 1 e refeito na hora.

**Por que 10 e nao 3:** com CV 0,66, tres pecas nao medem nada abaixo do dobro
(693). Dez tambem nao mediriam um efeito de 25% — mas ROMPIMENTO nao e efeito de
25%, e um efeito de 3x, e para isso dez bastam.

## O QUE EU NAO FACO, mesmo com o controle

- **nao apago video publicado** nem as 46 duplicatas: irreversivel, e a
  autorizacao nunca cobriu isso;
- **nao abro canal novo** nem plataforma nova: concentracao e a decisao 1, e o
  TikTok esta medido em `docs/tiktok-sondado.md` (receita zero com peca abaixo de
  60 s);
- **nao prometo prazo por volume.** Nunca mais. O 713 fechou essa porta.

## As duas coisas que SO VOCE pode fazer, e agora elas valem mais que antes

1. **Os dois cliques de consentimento do Google.** Com a decisao 4 eu vou julgar
   rompimento por VIEW, que e o instrumento cego — views por peca nao detecta
   nada abaixo do dobro. Com retencao eu vejo onde o espectador abandona DENTRO
   dos tres primeiros segundos, que e o mecanismo que decide o rompimento. Sem
   isso, cada ciclo de dez pecas custa dois dias e responde "sim ou nao" em vez
   de "por que".
2. **O Supabase Pro.** Hoje medir e registrar funcionam pelo Postgres, mas o
   Storage e o caminho automatico seguem fechados, e o ritmo depende de eu
   disparar a mao.
