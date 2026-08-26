# Publicar quando a cota do YouTube virar

Escrito em 25/08/2026 23h, com dois pacotes renderizados esperando e a porta do
Supabase fechada. Existe para que a janela da manhã seja mecânica: cada passo
abaixo foi conferido nesta noite, e o que **não** foi conferido está dito.

## O estado, medido e não suposto

| coisa | estado | como foi conferido |
|---|---|---|
| cota diária do YouTube | **estourada** | 403 com `reason: quotaExceeded` às 20h25 de 25/08, e de novo à 01h35 de 26/08 |
| virada da cota | ~07:00 UTC | meia-noite no Pacífico, que é como o Google conta |
| PostgREST / Storage / Edge | **402 nos três** | `porta.yml`, run 32909973867, 23h15 de 25/08 |
| refresh de token por `pg_net` | **funciona** | epomeno-epipedo e nivel-do-jogo, HTTP 200, `expires_in` 3599, 23h16 de 25/08 |
| `execute_sql` (Management API) | **funciona** | usado a noite toda para ler `videos` e gravar `aprendizados` |

Porta fechada nos três ⇒ **modo ponte**. O caminho normal (`frota.yml` com
`publicar: true`) não serve: ele chama `confere_token.py` e a trava de nome de
pacote pelo PostgREST, e as duas tomam 402 antes do upload acontecer.

Cuidado com uma leitura falsa: no `frota.yml` o passo **Entregar no Storage** é
`continue-on-error: true`. Ele **conclui como sucesso mesmo tomando 402** — só
emite `::error::`. Ver o passo verde não é evidência de que o Storage voltou.
Quem responde isso é o `porta.yml`, e só ele.

## Os dois pacotes prontos

| pacote | canal | idioma | artefato | expira |
|---|---|---|---|---|
| `epomeno-epipedo-011` | epomeno-epipedo | el | `pacote-epomeno-epipedo-011` (id 9583286132) | 08/09/2026 |
| `nivel-do-jogo-007` | nivel-do-jogo | pt-BR | `pacote-nivel-do-jogo-007` (id 9585036472) | 08/09/2026 |
| `kolejny-poziom-012` | kolejny-poziom | pl | `pacote-kolejny-poziom-012` (id 9589333786) | 09/09/2026 |
| `seviye-seviye-007` | seviye-seviye | tr | `pacote-seviye-seviye-007` (id 9590467009) | 09/09/2026 |

Os três foram renderizados com `publicar: false` e passaram nos dez portões.
`ja_publicado` estava vazio para os dois primeiros às 23h16 de 25/08 e para o
terceiro à 01h40 de 26/08 — **mas isso é um instantâneo, não uma autorização**:
regenere o estado no momento de publicar, como manda o passo 3.

**Ordem sugerida**, do canal com mais sinal para o com menos: epomeno-epipedo
(8 inscritos, 43,0 h), kolejny-poziom (5 inscritos, 30,7 h), seviye-seviye
(3 inscritos, 20,1 h — e a melhor distribuição da frota), nivel-do-jogo
(2 inscritos, 1,95 h — mas a MAIOR conversão da frota, 0,525% inscrito/view).
Se a cota acabar no meio, os primeiros são os que mais rendem.

**Tempo de render medido nesta noite**, útil para dimensionar qualquer render
adicional na janela da manhã — não há tendência de piora, a variação é normal:

    epomeno-epipedo-011   75 cenas    7,1 min   5,7 s/cena
    kolejny-poziom-012    80 cenas   12,7 min   9,5 s/cena
    seviye-seviye-007     76 cenas  ~12,0 min  ~9,5 s/cena

## A ordem

1. **Confira a porta antes de qualquer coisa.** Dispare `porta.yml`. Se ela
   estiver ABERTA, esqueça o resto deste arquivo: é só `frota.yml` com
   `publicar: true`, que rerenderiza e publica num passo só.

2. **Refresque o token dentro do banco**, por `execute_sql`. O `refresh_token`
   não sai do Postgres; só o `access_token` de uma hora atravessa:

   ```sql
   select c.chave, net.http_post(
     url     := (c.valor::jsonb->>'token_uri'),
     body    := jsonb_build_object(
                  'client_id',     c.valor::jsonb->>'client_id',
                  'client_secret', c.valor::jsonb->>'client_secret',
                  'refresh_token', c.valor::jsonb->>'refresh_token',
                  'grant_type',    'refresh_token'),
     headers := '{"Content-Type": "application/json"}'::jsonb) as req_id
   from config c where c.chave = 'yt_token_<canal>';
   ```

   A resposta é assíncrona: ela chega em `net._http_response` pelo `id` que a
   chamada devolveu. Confira `status_code = 200` antes de seguir.

   **Nunca** passe esse token por input de workflow — input fica gravado no run
   e o scanner de segredos recusa, com razão.

3. **Gere o estado anti-duplicata NA HORA.** Não reaproveite arquivo salvo: uma
   trava anti-duplicata rodando contra estado velho é exatamente como a mesma
   coisa vai ao ar duas vezes. Uma consulta, no momento de publicar:

   ```sql
   select jsonb_build_object(
     'ja_publicado', coalesce((select jsonb_object_agg(formato, youtube_id)
        from videos where pacote = '<pacote>' and youtube_id is not null), '{}'::jsonb),
     'titulos_no_ar', coalesce((select jsonb_agg(jsonb_build_object(
          'titulo', titulo, 'formato', formato,
          'youtube_id', youtube_id, 'pacote', pacote))
        from videos where canal = '<canal>' and youtube_id is not null), '[]'::jsonb));
   ```

   Se `ja_publicado` vier com qualquer formato preenchido, **pare**: o pacote já
   está no ar e o resto seria duplicata.

4. **Baixe o artefato no sandbox** pela URL assinada do Azure. O
   `archive_download_url` da API responde com um redirect 302 para uma URL curta
   e sem credencial do GitHub — é essa que atravessa.

5. **Publique** com `publicar.py` em modo ponte:

   ```
   python3 fabrica/publicar.py spec.json --canal <canal> --idioma <idioma> \
       --access-token <token> --estado-json estado.json --registro-json registro.json
   ```

   `--access-token` e `--estado-json` andam juntos: sem o estado o próprio
   script recusa, porque as duas travas ficariam cegas.

6. **Registre** o conteúdo de `registro.json` em `videos` por `execute_sql`, e
   atualize `canais.ultimo_pacote_em`.

7. **Confira no vídeo publicado, não no código, e nos DOIS formatos.** Foi assim
   que apareceram os dois defeitos de licença: 186 vídeos sem o crédito CC-BY, e
   depois o short sem ele mesmo com o longo já corrigido.

## O teto por canal continua valendo

No máximo **um longo por canal por dia** (`orquestra.MAX_POR_DIA_POR_CANAL`).
O epomeno-epipedo publicou o `-010` às 09h37 de 25/08, então o `-011` só pode
ir ao ar em 26/08 — que é justamente quando a cota vira.

## Quanto cabe na janela — o custo por pacote, e o que eu NÃO sei

Custo em unidades, somando as chamadas que o `publicar.py` faz de verdade
(tabela oficial da API v3):

    longo    videos.insert 1600 + thumbnails.set 50 + captions.insert 400
             + playlistItems.insert 50                            = 2.100
    short    videos.insert 1600 + thumbnails.set 50
             + playlistItems.insert 50                            = 1.700
    apontar  videos.list 1 + videos.update 50                     =    51
    ------------------------------------------------------------------------
    PACOTE                                                        = 3.851

    5 pacotes                                                     = 19.255
    crédito CC-BY, 66 vídeos (list + update)                      =  3.366
    TOTAL da manhã                                                = 22.621

**O teto do projeto eu não sei** — não alcanço o console do Google Cloud daqui.
O que sei é o que a própria frota já fez: em **20/08 saíram 14 pacotes num só
dia**, o que a esta conta dá cerca de **54 mil unidades**, todas bem-sucedidas.
Então 22.621 cabe com folga larga.

Há uma tensão que fica registrada em vez de escondida: em 25/08 a cota estourou
por volta das 20h20 depois de 9 pacotes (~34.700) somados a cerca de noventa
`videos.update` do crédito CC-BY (~4.600), o que dá ~39.000 — abaixo dos ~54.000
de 20/08. As duas medições não fecham entre si, e eu não sei qual variável
explica a diferença. Por isso a regra de ordem abaixo vale de qualquer jeito.

**Ordem, e ela é a decisão que essa incerteza governa:** publique os cinco
pacotes ANTES do crédito CC-BY. O crédito é o trabalho descartável se a cota
acabar no meio; um pacote publicado pela metade não é.

## O que fica para depois da publicação, na mesma janela

Cerca de 66 vídeos ainda esperam o crédito CC-BY atrasado. Rode
`credito_atrasado.py` com `--pausa` e `--esperas`, e lembre que os dois 403 têm
a mesma mensagem: `rateLimitExceeded`/`userRateLimitExceeded` pedem pausa de
segundos, `quotaExceeded` pede parar até a virada seguinte. Publicar um pacote
custa ~3.855 unidades e cada `videos.update` custa 50 — publique primeiro.
