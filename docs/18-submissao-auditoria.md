# Submissão da auditoria — texto pronto para colar

> `docs/10-auditoria-api.md` explica **por que** auditar e como preparar o projeto.
> Este arquivo é o **conteúdo da submissão**: o que escrever e o que gravar.
> Escrito em 2026-08-05, depois de confirmar que a auditoria pede três coisas —
> descrição do caso de uso, **vídeo demonstrando o fluxo de OAuth**, e aceite dos
> Termos. O vídeo é o item que trava a maioria de quem tenta.

## Projeto a usar

Use o projeto que **já existe**: `Youtube RECEITA`. Não crie outro. Um projeto do
Google Cloud comporta várias APIs — o Gemini já está ativo nele, e a YouTube Data
API v3 entra ao lado. A auditoria é do projeto, não da API isolada.

Falta só: **APIs e serviços → Biblioteca → ativar YouTube Data API v3**, e anotar
o *Project number* da página inicial.

---

## 1. Descrição do caso de uso

> Cole no campo de descrição. Está em inglês porque o formulário é revisado em
> inglês. Descreve o que a máquina faz de verdade — não há nada aqui que
> precise ser suavizado, e uma descrição que não bate com o comportamento
> observado é o que reprova a submissão.

```
WHAT THE APPLICATION DOES

This is a single-operator content production pipeline. It researches a topic,
writes a script, renders an educational video, and uploads it to YouTube
channels that I own. There is no third-party user base: the only person who
authenticates is me, the channel owner, and the only channels it touches are
mine.

The application is not a product offered to others. It is internal tooling for
my own channels.

HOW THE API IS USED

Read: youtube.search.list and youtube.videos.list, to measure the public
performance of videos in a topic area before deciding what to produce. The
application computes views-per-day across a sample and identifies which formats
underperform, so that it does not produce content that duplicates what already
exists.

Write: youtube.videos.insert, to upload a finished video with its title,
description, tags, category, thumbnail and subtitle file. Roughly one to three
uploads per day at most, per channel.

The application does not comment, does not subscribe, does not rate, does not
message users, and does not read or store any data belonging to other users.

SCOPES REQUESTED

- youtube.upload — to upload my own finished videos
- youtube.readonly — to confirm upload status and read public metrics of my
  own channels

NATURE OF THE CONTENT

Original educational content on personal finance and household economics,
produced for non-English-speaking audiences that are underserved in these
topics. Each video is written from primary institutional sources — national
statistics offices, central banks, and financial regulators — and the specific
figures used are cited in the video description so viewers can verify them.

The narration is synthesised from a script I author. Every upload is flagged
with containsSyntheticMedia set to true and carries a written disclosure in the
description. The videos are not reuploads, not compilations of third-party
material, and contain no content owned by anyone else. Background music is
licensed under Creative Commons with attribution in the description.

DATA HANDLING

The application stores, for my own videos only: the video id, title, duration,
publication timestamp and the public view count. No personal data of any kind
is collected, and no data about other users is retrieved or retained. There is
no user-facing surface, so there is nothing to display to third parties.
```

---

## 2. Roteiro do vídeo de demonstração do OAuth

O revisor quer ver **a tela de consentimento e o que o app faz com o acesso** —
não o conteúdo publicado. Grave a tela, ~60 a 90 segundos, sem edição e sem
música. Narração é opcional; se narrar, em inglês. Pode ser gravação de tela do
celular apontada para o monitor se for mais rápido — o que importa é ser legível.

**Sequência a gravar, nesta ordem:**

1. **(0:00–0:10) O ponto de partida.** Mostre o terminal ou a tela do app antes
   de qualquer autenticação. Deixe visível que não há sessão ativa.

2. **(0:10–0:25) Disparar o login.** Execute o comando que inicia o fluxo. Mostre
   a URL de consentimento sendo aberta no navegador.

3. **(0:25–0:45) A tela de consentimento — este é o trecho que importa.**
   Enquadre a tela inteira, sem cortar, de forma que se leia:
   - o nome do projeto/app,
   - a conta Google que está autorizando,
   - **a lista de permissões pedidas** (upload e readonly),
   - o botão de permitir.

   Pare um segundo aqui. É o quadro que o revisor vai olhar com atenção.

4. **(0:45–0:55) O consentimento concedido.** Clique em permitir e mostre o
   retorno ao app com a confirmação de autenticação.

5. **(0:55–1:20) O que o app faz com o acesso.** Mostre um upload real
   acontecendo: o comando, a resposta da API com o id do vídeo, e o vídeo
   aparecendo no seu Studio. Deixe visível que o destino é um canal seu.

6. **(1:20–1:30) O encerramento.** Mostre a tela do Studio com o vídeo listado.

**O que NÃO fazer no vídeo:**

- Não corte a tela de consentimento nem borre as permissões — é o item central.
- Não mostre a chave nem o `client_secret.json` aberto.
- Não acelere o vídeo. Revisor precisa conseguir ler.
- Não mostre canal que não seja seu.

---

## 3. Aceite dos Termos

Último passo do formulário. Leia antes de aceitar: os pontos que importam para
nós são a proibição de reupload de conteúdo de terceiros e a exigência de
divulgação de mídia sintética — a máquina já cumpre os dois, e é por isso que a
descrição acima pode ser literal.

---

## Formulário

📋 **[YouTube API Services — Audit and Quota Extension Form](https://support.google.com/youtube/contact/yt_api_form)**

## Depois de enviar

O prazo não é publicado e há relato de fila passando do esperado. Enquanto isso
a máquina continua produzindo e entregando ao Storage sem gastar cota nenhuma —
o estoque cresce e a publicação segue pela Upload-Post, dentro dos 10/mês.

No dia da aprovação: `videos.insert` público passa a valer, **100 uploads/dia,
de graça, sem intermediário e sem mensalidade.**
