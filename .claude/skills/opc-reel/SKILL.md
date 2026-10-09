---
name: opc-reel
description: "Produz e publica um Reel da marca O Proximo Cliente (@oproximocliente) inteiro na nuvem: acha o bruto no Google Drive, transcreve, corta pelo texto, aplica o card da marca, publica no Instagram e no Facebook e registra no Supabase. Use quando o pedido envolver criar, editar ou publicar video/Reel/post do O Proximo Cliente, ou quando pedirem para transformar uma gravacao bruta do Drive em post publicado. Nao use para outros canais nem para o canal de YouTube (esse e o fabrica/)."
---

# Reel do O Proximo Cliente, do bruto ao post

Pipeline em nuvem, sem editor local. Um Reel sai do `.MOV` cru no Drive e chega
publicado sem ninguem abrir programa nenhum.

## A regra que segura tudo: uma verdade so

Cor, fonte, corpo e geometria vivem **exclusivamente** em `opc/estilo.py`. O
`opc/render.py` importa de la e o `opc/GUIA_ESTILO.md` e gerado de la. Se voce
digitar `#FF7A1B` em qualquer outro lugar, a marca passou a ter duas verdades e
a proxima mudanca vai sair pela metade.

    python3 opc/estilo.py            # o guia, gerado
    python3 opc/estilo.py --json     # a chave, como dado

## Onde estao as coisas

| O que | Onde |
|---|---|
| Brutos de gravacao | Drive: `Computadores > Meu laptop (1) > Proximo cliente` |
| Roteiros A1-A10 | Drive: `O proximo Cliente/` (Doc "A1 — Seu problema nao e preco") |
| Guia de estilo | `opc/GUIA_ESTILO.md` (gerado por `opc/estilo.py`) |
| Por que 3 entregas foram reprovadas | `opc/ESTUDO_FORMATO.md` — leia ANTES de mexer no formato |
| Corte pelo texto, N janelas | `opc/cortar.py` |
| Montagem em planos | `opc/montagem.py` |
| Regua sobre o mp4 pronto | `opc/conferir.py` |
| Registro do que foi ao ar | Supabase, tabela `opc_posts` |

## O caminho, na ordem

### 1. Escolher o bruto e transcrever
Baixe pelo Composio (`GOOGLEDRIVE_DOWNLOAD_FILE` devolve `s3url`) e transcreva
no sandbox remoto — a sessao em nuvem nao alcanca CDN externo, o sandbox alcanca:

    pip install -q faster-whisper
    ffmpeg -i BRUTO.mov -vn -ac 1 -ar 16000 a.wav
    # modelo 'base', language='pt', vad_filter=True

Transcrever antes de cortar e o que permite cortar **pelo argumento**, e nao
pelo relogio.

### 2. Passar na trava anti-duplicata — sempre
Um bruto parecido com um post no ar nao e material novo, e republicacao.
Transcreva tambem o Reel publicado suspeito (`INSTAGRAM_GET_IG_MEDIA` da o
`media_url`) e compare o texto. O `duration_s` vem embutido no proprio
`media_url` e ja elimina metade dos candidatos sem baixar nada.

Um take que fala do mesmo TEMA nao e duplicata; o mesmo take editado, e.

### 3. Cortar pelo texto, com quantas janelas precisar

    python3 opc/cortar.py bruto.MOV cortado.mp4 --janelas 10.20-21.02 28.92-50.90 \
        --transcricao transc.json --transcricao-saida transc_cortada.json

Quase nunca ha 30 segundos bons em sequencia. No IMG_2318 a tese estava em
10-21s, o fechamento em 29-51s, e no meio o locutor dizia "clica nesse video" —
o CTA que `estilo.py` marca como PROIBIDO. Com janela unica so dava para
entregar 22s (abaixo do minimo) ou deixar o CTA velho entrar.

O `cortar.py` emenda as janelas num arquivo continuo E remapeia a transcricao,
entao a montagem depois nao sabe que houve corte.

SEMPRE em segundo plano com `setsid`, e NUNCA com o `&` simples: a chamada de
bash tem teto de 60 s e mata o grupo de processos ao expirar.

    setsid bash -c 'python3 ... > log 2>&1; echo "CODIGO=$?" >> log' < /dev/null > /dev/null 2>&1 &

### 4. Gerar a legenda queimada
Sem ela a peca fica parada e perde para a referencia — foi o motivo da primeira
reprovacao. Transcreva com `word_timestamps=True`, **revise os erros de ASR** (o
modelo `base` troca palavras; o `small` estoura a memoria do sandbox) e gere:

    python3 opc/legenda.py palavras.json legenda.ass

Legenda com palavra errada e pior que sem legenda. Corrija so onde a fala e
inequivoca; nao "melhore" o que a pessoa disse.

### 5. Enquadrar o rosto ANTES de renderizar

    python3 opc/enquadrar.py CORTADO.mp4      # imprime a linha da janela

A faixa navy ocupa o topo do quadro. Se o rosto do bruto estiver acima dela, ela
passa por cima da cabeca — e isso ja foi ao ar. O `enquadrar.py` mede onde o
rosto esta e devolve de que linha da fonte a janela visivel deve comecar.

O sintoma que denuncia o defeito e a taxa de deteccao de rosto: no render
reprovado o detector achou rosto em **1 de 12** quadros; no bruto, em 12 de 12.

### 6. Montar em planos (NAO em um layout so)

    python3 opc/montagem.py cortado.mp4 saida.mp4 --de 0 --ate 32.8 \
        --cards cards.json --legenda legenda.ass --janela 345 \
        --broll apoio1.mp4 apoio2.mp4

Este passo substituiu o `render.py` de card unico, e o motivo esta em
`opc/ESTUDO_FORMATO.md`: um grafo de filtros valido para o video inteiro da uma
peca cuja fracao de navy varia UM ponto percentual em 33 segundos. Foi reprovada
duas vezes. Nenhum parametro conserta — falta poder ter planos diferentes.

Sao quatro, alternando a cada ~5s: `pessoa_card` (painel navy em cima),
`pessoa_cheia` (sem painel), `broll` (apoio do Pexels, ninguem na tela) e
`cartela` (navy cheio no fim). A narracao NAO e cortada: os planos trocam o
video e o audio corre inteiro por baixo.

O b-roll vem do Pexels (`PEXELS_SEARCH_VIDEOS`, `orientation: portrait`), e o
clipe entra pelo link `hd_1080_1920`.

### 6b. Aplicar os cards

    bash opc/fontes.sh                      # instancia os pesos exatos da marca
    python3 opc/render.py CORTADO.mp4 SAIDA.mp4 \
      --cards cards.json --legenda legenda.ass --janela <o numero acima>

`cards.json` e uma SEQUENCIA, com `de`/`ate` em segundos — os Reels da marca
trocam de card ao longo do video e revelam o punchline laranja depois do setup.
Um card so para o video inteiro e o erro que ja foi cometido.

Tres guardas existem de proposito e nao devem ser contornadas:

* **fonte faltando levanta** — card com fonte parecida passa no terminal e nao
  passa no feed;
* **linha larga demais levanta** antes do render — ela sairia cortada nas bordas
  e isso so apareceria no mp4 pronto (o limite util e 960px de 1080);
* **a orientacao do bruto decide o layout** — video de celular vem `1920x1080`
  com `rotation=90`, ou seja ja e 9:16 na tela. Encaixar 9:16 dentro de 9:16 nao
  cabe, e foi assim que o texto do card foi parar em cima do rosto.

### 7. Conferir por medida, nunca por "parece certo"

Duracao, cor e OCR do card passam mesmo com a peca errada. Estas tres medidas
sao as que pegam, e todas tem numero de referencia medido nos Reels no ar:

Isso agora e codigo, e nao uma tabela para conferir na mao:

    python3 opc/conferir.py entrega.mp4     # sai 0 se aprovado

Ele abre o mp4 PRONTO e mede dez coisas. Os alvos de cada uma estao no proprio
arquivo, com o numero medido nas tres referencias ao lado. Os que mais pegam:

| Medida | Referencias | O reprovado |
|---|---|---|
| Variacao da fracao de navy | 35 a 75 pp | **1 pp** |
| Altura da caixa alta da legenda | 63 / 91 / 111 px | **32 px** |
| Linha de base da legenda | 0,68 a 0,78 | **0,65** |
| Volume integrado | -14,1 a -14,3 LUFS | (a peca da maquina saiu -17,2) |

REGRA DE OURO DA REGUA: antes de confiar num limiar novo, rode-o contra as tres
referencias. Cinco reguas minhas reprovavam Reels que estao no ar e funcionando
— piso de cortes alto demais, faixa da legenda medindo a borda do meu proprio
recorte, rosto do b-roll lido como o locutor, teto de duracao por quatro
decimos, e uma contagem de cortes inflada porque eu contava linhas de
`showinfo` (que sao varias por quadro) em vez de `pts_time:`.
Quando a regua reprova a peca que funciona, o defeito esta na regua.

O detector de rosto e o `haarcascade_frontalface_default` do OpenCV
(`pip install 'opencv-python-headless<5'` — na 5.x o modulo `objdetect` nao vem
no build headless).

### Memoria: o sandbox tem 1 GB

**Olhe /tmp ANTES de culpar o render.** La ele e um tmpfs, ou seja MEMORIA. Os
intermediarios de 1080x1920 tinham enchido /tmp com 303 MB numa maquina de
985 MB, e eu passei tres OOMs seguidos culpando o passo que estava rodando.
Limpar devolveu a memoria disponivel de 213 MB para 486 MB. Por isso o
diretorio de trabalho nasce em `~/opc_planos` e nao em /tmp.

    df -h /tmp && free -m     # primeira coisa, sempre

O que mais ja matou render aqui, tudo com SIGKILL e sem mensagem util:
fonte `color` infinita combinada por `overlay`; `pad` para um quadro maior que
a saida; queimar a legenda sobre a peca inteira (o `montagem.py` faz por plano
justamente por isso); `loudnorm` junto com o encode do video (rode sozinho);
e `veryfast` com a memoria apertada — o mesmo plano caiu para 0,9 quadro por
segundo antes de morrer.

E uma armadilha que nao e memoria mas parece: com `-stream_loop`, o carimbo de
tempo volta a zero na volta do loop e o filtro `fps` fica esperando um instante
que nunca chega — o render trava em `frame=136` para sempre. Cure com
`setpts=N/FRAME_RATE/TB` no fim da cadeia.

### 8. Escrever a legenda do post em cinco blocos
1. Frase-choque com numero concreto · 2. A virada, com "Mas" · 3. Explicacao em
2-3 frases com travessao · 4. Consequencia dura · 5. CTA fixo + hashtags.

CTA e hashtags saem de `estilo.chave()["copy"]`. **Sem emoji e sem "link na
bio"** — essa e a geracao antiga de legenda, ja substituida no perfil.

### 9. Publicar
Instagram sao dois passos (o primeiro so cria o container):

    INSTAGRAM_POST_IG_USER_MEDIA          -> creation_id
    INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH  -> id publicado (max_wait_seconds>=60)

Facebook publica direto em `FACEBOOK_CREATE_VIDEO_POST`. A pagina certa e
**"O Proximo Cliente" (`1117439194786453`)** — a conta administra mais de vinte
paginas de clientes e postar na errada e estrago em negocio alheio. Confira
sempre pelo id, nunca pelo nome parecido.

### 10. Registrar antes de comemorar
`opc_posts` no Supabase, com os ids do Instagram e do Facebook, o bruto de
origem e o corte usado. Publicar sem registrar cega a trava anti-duplicata — e
esse defeito ja republicou pacote no projeto de YouTube deste mesmo repositorio.

## Quando publicar

Janela da marca: **segunda-feira, 12h30** (almoco do dono de comercio), no
maximo **1 Reel por dia**. A Graph API do Instagram nao agenda nem salva
rascunho; para respeitar a janela, agende uma rotina (cron) que dispare a
publicacao na hora — o efeito e o mesmo. O que a API nao faz de jeito nenhum e
audio em alta: isso e do app do celular, a 5-10% de volume, so para entrar na
distribuicao.

## O que nao fazer

- Publicar de uma sessao em nuvem com `curl` direto na CDN: o egress e bloqueado.
  Todo download e upload de midia passa pelo sandbox do Composio.
- Contar com o helper `composio_workbench` (`upload_local_file`): o kernel do
  sandbox recicla e ele some no meio da sessao. Para levar arquivo do sandbox
  para o Drive ou para a publicacao, hospede em URL temporaria e use
  `GOOGLEDRIVE_UPLOAD_FROM_URL` / o campo `video_url` do Instagram — funciona
  sempre e ainda serve para os dois destinos de uma vez.
- Escrever cor ou fonte fora de `opc/estilo.py`.
- Tratar `Material base/` como cheia: ela esta vazia. Cobertura vem de Pexels
  (conectado no Composio) ou do Canva, e so como cobertura — o principal e sempre
  a gravacao propria.
