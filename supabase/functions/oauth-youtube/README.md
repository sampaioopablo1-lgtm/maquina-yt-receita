# oauth-youtube

Recebe o redirect do Google e grava o `refresh_token` sozinho em
`config.yt_token_<slug>`.

## Por que existe (20/08/2026)

Com `redirect_uri=http://localhost` o dono tinha de copiar dez URLs de uma
pagina de erro e cola-las noutro lugar em menos de dez minutos, porque o
`code` e de uso unico e expira. Ele fez isso tres vezes e a maquina continuou
com dez tokens mortos. O gargalo nunca foi o consentimento — era o transporte
do codigo.

Aqui o proprio Google entrega o codigo neste endereco, a troca acontece na
hora, e a pagina responde "canal X reautorizado". Zero copiar e colar, zero
prazo.

## O que continua sendo manual, e por que

Um token do YouTube vale para UM canal: quem escolhe o canal e a pessoa na
tela de consentimento. Nao existe consentimento que cubra treze canais — e
limite do YouTube, nao deste codigo. Entao os cliques em "Permitir" continuam
sendo um por canal. O que esta funcao elimina e todo o resto.

## verify_jwt = false

Obrigatorio: quem chama e o navegador vindo do Google, que nao carrega JWT do
Supabase. As tres travas que substituem isso:

1. `state` tem de ser um slug que ja existe em `config.yt_token_<slug>`;
2. o canal e CONFIRMADO por `channels.list(mine=true)`, nunca assumido pelo slug;
3. se o canal confirmado divergir de `canais.youtube_channel_id`, recusa e nao grava.

Sem consentimento numa das contas do dono nao ha `code` valido, entao um
terceiro nao tem como gravar nada aqui.

## Pre-requisito no Google Cloud Console

O endereco abaixo precisa estar em **URIs de redirecionamento autorizados** do
client OAuth:

    https://vevocauwtarctfwngrch.supabase.co/functions/v1/oauth-youtube

E uma unica entrada, nao uma por canal.

## Gerar os links

    python3 scripts/links_reauth.py --edge          # aponta para esta funcao
    python3 scripts/links_reauth.py                 # aponta para http://localhost (antigo)
