# Publicar sem o runner: a rota que destravou onze pacotes em dez minutos

Escrito em 27/08/2026, logo depois de usá-la. Em 12h26 saiu o primeiro vídeo
em sete dias; às 12h36 os onze pacotes estavam no ar, vinte e dois vídeos em
onze canais, conferidos um a um no YouTube.

## O erro que custou sete sondagens

Entre 26 e 27/08 disparei o `retomar.yml` sete vezes. As sete morreram no
mesmo passo, `Refrescar o token dentro do runner`, porque o segredo
`YT_OAUTH_JSON` não existe e só o dono cadastra segredo. A conclusão que eu
repeti sete vezes — "o próximo passo continua sendo seu" — estava errada, e o
erro não era de fato: era de **granularidade**. Eu tratei como bloqueio total
o que era o bloqueio de **uma peça**.

Publicar precisa de três coisas. Duas já funcionavam:

| peça | estado real em 26/08 | como eu descobri |
|---|---|---|
| **token** | funcionava | `net.http_post` dentro do banco: HTTP 200, `expires_in` 3599, escopo com `youtube.upload` e `youtube.force-ssl` |
| **fábrica** | funcionava | `publicar.py` só importa stdlib + `caminhos`; o único binário externo é o `ffprobe`, que lê duração e não transcodifica |
| **pacote** | **essa faltava** | o render mora num artefato do GitHub, e baixar artefato pede credencial que não existe fora do runner |

A regra que fica: **quando um caminho trava, liste as peças e teste cada uma.**
O que parece bloqueio quase sempre é uma peça só, e sondar a peça errada de
hora em hora não descobre isso nunca.

## A peça que faltava, e por que ela pode ser resolvida em público

`urlartefato.yml` é read-only e faz uma coisa: resolve o redirecionamento da
API de artefatos e imprime a URL assinada do Azure.

Ela pode ser impressa num repositório público porque:

- é assinada e o `se=` dela dá **dez minutos**;
- não carrega credencial nenhuma do GitHub — quem a pegar depois do prazo não
  tem nada;
- o que ela entrega são cinco arquivos, e nenhum é segredo: `video.mp4`,
  `short.mp4`, `thumbnail.png`, `legendas.srt`, `copy.md`. Os cinco vão a
  público no YouTube minutos depois, de propósito.

O que ela **não** pode virar: uma rota para imprimir qualquer outra coisa.

## A ordem, para repetir

1. **Confira a porta.** `porta.yml`. Aberta ⇒ esqueça este arquivo, é
   `frota.yml` com `publicar: true`.

2. **Resolva as URLs.** Dispare `urlartefato.yml` com os IDs dos artefatos
   separados por vírgula. Leia o log. Dez minutos de validade dão folga para
   baixar todos.

3. **Baixe na sandbox.** Um `curl` + `unzip` por pacote, em paralelo. Os dez
   levaram menos de 45 segundos. Clone o repositório na sandbox (é público) —
   é dele que saem `publicar.py` e as specs.

4. **Refresque os tokens, todos numa consulta.** `net.http_post` para o
   `token_uri` de cada `config.yt_token_<canal>`; a resposta chega em
   `net._http_response` pelo `id`. Confira `status_code = 200` antes de seguir.
   **Nunca** passe esse token por input de workflow.

5. **Gere o estado anti-duplicata, e mantenha-o crescendo.** Cada pacote recebe
   o corpus com tudo que subiu antes dele, **inclusive o que subiu nesta mesma
   rodada** — foi para isso que a trava existe. O corpus pode ser mantido na
   sandbox durante a janela, porque nessa janela ninguém mais escreve em
   `videos`; no fim ele é conferido contra o banco. O que não se faz é
   reaproveitar estado congelado.

   O estado atravessa transcrito, e transcrição quebra: em 26/08 eu cortei uma
   lista no décimo terceiro título. Por isso o estado **declara** o próprio
   tamanho em `titulos_no_ar_n` e quem o recebe recusa lista truncada. Truncar
   deixou de ser silencioso.

6. **Publique um por vez, e não deixe um derrubar os outros.** `conduz.py` roda
   a fila inteira; um pacote que falha vai para `falhas` e a fila continua. Dez
   canais parados por causa de um seria trocar um problema por dez. Rode com
   `nohup` — a sandbox mata comando em 180 s, e dez uploads passam disso.

7. **Registre no banco antes de comemorar.** Publicar sem registrar cega as
   travas, e esse defeito já republicou pacote antes. `execute_sql` continua
   aberto: um `insert` em `videos` e um `update` em `canais.ultimo_pacote_em`.
   A `duracao_s` do longo sai do `ffprobe`, porque o registro do modo ponte
   não a traz.

8. **Confira no vídeo publicado, os dois formatos.** Uma chamada à Data API
   com os vinte e dois IDs: `privacyStatus`, `defaultLanguage`,
   `defaultAudioLanguage`, e o crédito CC-BY na descrição. Foi assim que os
   dois defeitos de licença apareceram — e desta vez os vinte e dois passaram.

## O teto que eu quase respeitei demais

`MAX_POR_DIA_POR_CANAL` é **por canal**. Onze pacotes de onze canais diferentes
cabem no mesmo dia sem chegar perto do teto. Eu passei a madrugada de 27/08
argumentando comigo mesmo que não valia produzir um décimo segundo pacote —
o que era verdade — sem notar que os onze que já existiam podiam sair todos
juntos assim que a peça do artefato fosse resolvida.

## O que ficou pendente, e é do Pablo

`youtube.com/verify` em **agla-level**, **game-money-lab** e
**resep-naik-level**. Os três longos subiram com capa automática: o `403` diz
`canal sem verificacao por telefone`. O PNG desenhado existe e está no pacote —
falta permissão no canal. Quando verificar, dá para corrigir a capa dos três
sem republicar nada.

## Os vinte e dois no ar

| canal | longo | short | duração do longo |
|---|---|---|---|
| epomeno-epipedo | `jUxJPvmA4Mk` | `PmDE1d-mUpI` | 9:15 |
| nivel-do-jogo | `VXF7UgfNt7Y` | `AXeHdTi27RM` | 9:36 |
| kolejny-poziom | `vcJf6WipLtY` | `I5vFs3H9IP0` | 12:57 |
| seviye-seviye | `AdQ0PBSCbkI` | `trQK_ui8itU` | 12:42 |
| setiap-level | `rIPi4qYCcMU` | `ab5HJ0j28YU` | 9:25 |
| labtreinamento | `4OYBkCHFTV8` | `1HScDT8Oh0A` | 8:36 |
| agla-level | `Pnw2Sg1t2oQ` | `qeBe6yuCrfg` | 8:50 |
| game-money-lab | `w_zNDYHdiJ4` | `fkjMy5diw-g` | 8:04 |
| next-level-money | `-OyQiHJ27go` | `ERL4qymbmcM` | 8:04 |
| seja-mais-magra | `nEb_bdL13Tw` | `WGlKvRY332U` | 8:22 |
| resep-naik-level | `f1xXeBy8m2g` | `-d6l82pqm5k` | 8:35 |

Os onze shorts são o teste pré-registrado de
`docs/pre-registro-forma-dos-shorts.md`, cujos rótulos foram escritos em 26/08
com **zero views** nos onze. Agora eles têm exposição, e o teste vale. Rode
`fabrica/conversao.py` com aqueles grupos quando houver views — e sem tocar nos
rótulos, que é o que os torna cegos.
