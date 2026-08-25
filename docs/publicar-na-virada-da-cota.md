# Publicar quando a cota do YouTube virar

Escrito em 25/08/2026 23h, com dois pacotes renderizados esperando e a porta do
Supabase fechada. Existe para que a janela da manhã seja mecânica: cada passo
abaixo foi conferido nesta noite, e o que **não** foi conferido está dito.

## O estado, medido e não suposto

| coisa | estado | como foi conferido |
|---|---|---|
| cota diária do YouTube | **estourada** | 403 com `reason: quotaExceeded` às 20h25 de 25/08 |
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

Os dois foram renderizados com `publicar: false`, passaram nos dez portões, e
`ja_publicado` estava vazio para ambos às 23h16.

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

## O que fica para depois da publicação, na mesma janela

Cerca de 66 vídeos ainda esperam o crédito CC-BY atrasado. Rode
`credito_atrasado.py` com `--pausa` e `--esperas`, e lembre que os dois 403 têm
a mesma mensagem: `rateLimitExceeded`/`userRateLimitExceeded` pedem pausa de
segundos, `quotaExceeded` pede parar até a virada seguinte. Publicar um pacote
custa ~3.855 unidades e cada `videos.update` custa 50 — publique primeiro.
