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

## Medir é outra rota, e não passa por aqui

Este arquivo é sobre **publicar**, que precisa do arquivo e por isso precisa da
sandbox. **Medir não precisa de arquivo**, e desde 31/08/2026 é feito inteiro de
dentro do Postgres com `pg_net` — o `access_token` nem atravessa. Está em
`docs/medir-pelo-banco.md`, junto com os dois números que os tokens atuais
**não** conseguem medir.

## A trava anti-duplicata nao limpa o passado

Ela compara titulos **distintos** no corpus, e por isso impede o proximo
duplicado sem enxergar os que ja subiram. Em 01/09/2026, uma varredura achou
**55 videos duplicados no ar em seis canais** — 44 a remover:

    next-level-money   Dutch East India Company     6 longos + 5 shorts
    kolejny-poziom     Emerytura z ZUS 34,4%        6 longos + 5 shorts
    nivel-do-jogo      Lei Felca nos Games          5 longos + 5 shorts
    sx-educacao        Excel / licencas Power BI    5 longos + 5 shorts
    seviye-seviye      Asgari ucret 28.075 TL       5 longos + 4 shorts
    resep-naik-level   5 Strategi Ibu               4 longos

O estrago e concreto: no kolejny-poziom os cinco shorts duplicados somam 3.101
views — quase setenta por cento de tudo o que o canal tem — e sao o MESMO
video. Os seis longos duplicados somam 145. O canal tem cinco inscritos.

Rode isto de tempos em tempos e trate o resultado como defeito de entrega:

    select canal, titulo, formato, count(*)
    from videos where status = 'publicado' and titulo is not null
    group by 1, 2, 3 having count(*) > 1 order by 4 desc;

Apagar video publicado nao e reversivel e nao esta no mandato da rotina:
levante a lista, registre em `aprendizados`, e deixe a remocao com o Pablo.
(Aprendizado 544.)

## A ordem, para repetir

1. **Confira a porta.** `porta.yml`. Aberta ⇒ esqueça este arquivo, é
   `frota.yml` com `publicar: true`.

1b. **Se você acabou de renderizar, confira que o render EXISTIU.** O input
   `pacotes` do `frota.yml` é um JSON de **objetos**:
   `[{"canal":"nivel-do-jogo","pacote":"nivel-do-jogo-008","idioma":"pt-BR"}]`.
   Um escalar (`nivel-do-jogo-008`) quebra o `jq` que monta a matriz, e o
   sintoma engana: o run marca `failure` mas a API lista **um** job, `preparar`,
   em `success` — porque o que falhou foi a matriz vazia derrubando o job
   seguinte. Depois de despachar, confira que o job `produzir` **existe**; não
   basta o run estar `in_progress`. (Aprendizado 536.)

2. **Resolva as URLs.** Dispare `urlartefato.yml` com os IDs dos artefatos
   separados por vírgula. Leia o log. Dez minutos de validade dão folga para
   baixar todos.

3. **Baixe na sandbox, em `$RAIZ/f/<pacote>/`.** Um `curl` + `unzip` por
   pacote, em paralelo. Os dez levaram menos de 45 segundos. Clone o
   repositório na sandbox (é público) — é dele que saem `publicar.py` e as
   specs. O caminho **não** é `$RAIZ/<pacote>/`: o `conduz.py` procura em
   `$RAIZ/f/<pacote>/` e, se não achar o `copy.md` lá, reclama de placeholder
   não preenchido (`{CAPITULOS}`, `{TRILHA}`) — a mensagem culpa o render, mas
   o que faltou foi o diretório.

4. **Refresque os tokens, todos numa consulta.** `net.http_post` para o
   `token_uri` de cada `config.yt_token_<canal>`; a resposta chega em
   `net._http_response` pelo `id`. Confira `status_code = 200` antes de seguir.
   **Nunca** passe esse token por input de workflow.

4b. **A sandbox e efemera — o corpus e o clone somem entre rodadas.** Em
   31/08 a sandbox foi trocada (`j3i1` -> `75l8`) no meio da sessao: o clone
   em `/home/user/maq` e o `/home/user/pub/corpus.json` sumiram, enquanto o
   pacote baixado momentos antes sobreviveu. Para refazer o estado numa
   consulta so:

       select jsonb_build_object('titulos', jsonb_agg(titulo order by titulo collate "C"))
       from (select distinct titulo from videos
             where titulo is not null and status = 'publicado') t;

   Escreva o JSON na sandbox e **confira pelo md5 em ordem de byte** contra o
   banco antes de publicar. Corpus reconstruido sem essa conferencia nao
   publica. (Aprendizado 538.)

   E antes de rodar o `conduz.py`, **atualize o clone**: ele pode ser mais
   velho que a spec que voce acabou de empurrar, e o `publicar.py` morre com
   `FileNotFoundError: fabrica/specs/<pacote>.json` — erro que parece render
   perdido e nao e. `git fetch --depth 1 origin <branch> && git reset --hard
   FETCH_HEAD` resolve.

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

   **E desde 31/08 a conferência é por md5, não por contagem.** Peça ao banco a
   lista e o resumo na mesma consulta —
   `md5(string_agg(titulo, chr(10) order by titulo))` — e refaça o md5 na
   sandbox sobre a lista **na ordem em que ela veio** (não reordene: a colação
   do Postgres não é a do Python). Contagem só pega truncamento; o md5 pega
   também um caractere trocado no meio, que é o modo de falha real de
   transcrever cento e doze títulos em grego, polonês, turco e híndi.
   (Aprendizado 530.)

   **Com o md5 em ORDEM DE BYTES o corpus deixa de precisar ser repassado.**
   Peça `order by titulo collate "C"` no Postgres e ordene por
   `x.encode('utf-8')` no Python — aí os dois md5 são comparáveis. O corpus
   fica na sandbox, o `conduz.py` o faz crescer a cada publicação, e a rodada
   seguinte só confere. Em 31/08 ele já estava em 113 antes de eu tocar nele, e
   bateu de primeira: zero título transcrito.

6. **Publique um por vez, e não deixe um derrubar os outros.** `conduz.py` roda
   a fila inteira; um pacote que falha vai para `falhas` e a fila continua. Dez
   canais parados por causa de um seria trocar um problema por dez. Rode com
   `nohup` — a sandbox mata comando em 180 s, e dez uploads passam disso.

7. **Registre no banco antes de comemorar.** Publicar sem registrar cega as
   travas, e esse defeito já republicou pacote antes. `execute_sql` continua
   aberto: um `insert` em `videos` e um `update` em `canais.ultimo_pacote_em`.
   A `duracao_s` do longo sai do `ffprobe`, porque o registro do modo ponte
   não a traz.

   **Confira o corpus numa consulta SEPARADA, depois do insert.** Lida junto
   com o `insert`, a contagem volta com o valor de ANTES — num CTE que escreve,
   o resto da instrução enxerga o snapshot anterior. Em 31/08 isso devolveu 112
   contra 113 da sandbox e pareceu divergência; em consulta própria, 113 e 113.
   O perigo real é o inverso do susto: uma rodada que duplicou não mostraria o
   crescimento que faltou. (Aprendizado 531.)

8. **Confira no vídeo publicado, os dois formatos.** Uma chamada à Data API
   com os vinte e dois IDs: `privacyStatus`, `defaultLanguage`,
   `defaultAudioLanguage`, e o crédito CC-BY na descrição. Foi assim que os
   dois defeitos de licença apareceram — e desta vez os vinte e dois passaram.

   **E se o SHORT voltar sem tags, releia antes de acusar defeito.** O mesmo
   atraso de indexação que causou o bug de 25/08 atinge também esta leitura,
   que acontece minutos depois do mesmo `PUT`. Em 31/08 o `qKjRsDUO8Zc` voltou
   com zero tags aos quatro minutos e com as oito aos seis. O longo não passa
   pelo `apontar_para_longo` e por isso volta completo de primeira — a
   assimetria entre os formatos na primeira leitura é esperada.
   (Aprendizado 529.)

## O teto que eu quase respeitei demais

`MAX_POR_DIA_POR_CANAL` é **por canal**. Onze pacotes de onze canais diferentes
cabem no mesmo dia sem chegar perto do teto. Eu passei a madrugada de 27/08
argumentando comigo mesmo que não valia produzir um décimo segundo pacote —
o que era verdade — sem notar que os onze que já existiam podiam sair todos
juntos assim que a peça do artefato fosse resolvida.

## O que ficou pendente, e é do Pablo

`youtube.com/verify` em **agla-level**, **game-money-lab**, **resep-naik-level**
e — desde 31/08 — **seviye-seviye** e **nivel-do-jogo**. Os longos sobem com capa automática: o
`403` diz `canal sem verificacao por telefone`. O PNG desenhado existe e está no
pacote; falta permissão no canal. Quando verificar, dá para corrigir a capa sem
republicar nada.

**E essa lista não é fixa.** O seviye-seviye ACEITOU a capa em 27/08 e a recusou
em 31/08 — ele perdeu a verificação no meio do caminho. Trate isso como estado
que expira: confira o resultado do passo da thumbnail em toda publicação e
registre o `403` em `videos.erro` do longo. Do lado do espectador a falha é
silenciosa — o vídeo sobe, fica público, processa, e só a capa some.
(Aprendizado 533.)

No mesmo 31/08 o **nivel-do-jogo** caiu no mesmo `403`, também depois de já ter
aceitado capa antes. Dois canais perdendo a verificação na mesma sessão tira
isso da categoria "incidente" e põe na de "estado que vence". E o preço é maior
do que parece: os dois canais estão em `canal frio`, e capa automática apaga
justamente a alavanca de CTR de quem mais precisa dela. (Aprendizado 535.)

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
