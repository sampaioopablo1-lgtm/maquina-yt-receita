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
| Guia de estilo | `opc/GUIA_ESTILO.md` (gerado) |
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

### 3. Cortar em passagem unica
Nunca gere segmentos intermediarios: o sandbox mata comando em ~180 s e
mp4 cortado no meio fica sem `moov atom` e **parece corrompido** quando so
estava incompleto. Uma passagem so, com `trim`/`atrim` + `concat`, e em `nohup`
com marcador de fim:

    nohup bash cortar.sh > corte.log 2>&1 &   # a ultima linha do .sh ecoa CORTE_PRONTO

Corte fora o CTA de anuncio ("clica nesse video") quando o post for organico.

### 4. Gerar a legenda queimada
Sem ela a peca fica parada e perde para a referencia — foi o motivo da primeira
reprovacao. Transcreva com `word_timestamps=True`, **revise os erros de ASR** (o
modelo `base` troca palavras; o `small` estoura a memoria do sandbox) e gere:

    python3 opc/legenda.py palavras.json legenda.ass

Legenda com palavra errada e pior que sem legenda. Corrija so onde a fala e
inequivoca; nao "melhore" o que a pessoa disse.

### 5. Aplicar os cards

    bash opc/fontes.sh                      # instancia os pesos exatos da marca
    python3 opc/render.py CORTADO.mp4 SAIDA.mp4 \
      --cards cards.json --legenda legenda.ass

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

Depois de renderizar, confira **em que linha a faixa navy termina** e compare
com `geometria.video_topo` da chave. Duracao, cor e OCR do card passam mesmo
quando o texto esta escrito sobre a imagem — essa medida e a unica que pega.

### 6. Escrever a legenda do post em cinco blocos
1. Frase-choque com numero concreto · 2. A virada, com "Mas" · 3. Explicacao em
2-3 frases com travessao · 4. Consequencia dura · 5. CTA fixo + hashtags.

CTA e hashtags saem de `estilo.chave()["copy"]`. **Sem emoji e sem "link na
bio"** — essa e a geracao antiga de legenda, ja substituida no perfil.

### 7. Publicar
Instagram sao dois passos (o primeiro so cria o container):

    INSTAGRAM_POST_IG_USER_MEDIA          -> creation_id
    INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH  -> id publicado (max_wait_seconds>=60)

Facebook publica direto em `FACEBOOK_CREATE_VIDEO_POST`. A pagina certa e
**"O Proximo Cliente" (`1117439194786453`)** — a conta administra mais de vinte
paginas de clientes e postar na errada e estrago em negocio alheio. Confira
sempre pelo id, nunca pelo nome parecido.

### 8. Registrar antes de comemorar
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
