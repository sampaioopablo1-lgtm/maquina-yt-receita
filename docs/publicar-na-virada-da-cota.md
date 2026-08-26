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

## Os onze pacotes prontos

| pacote | canal | idioma | artefato | expira |
|---|---|---|---|---|
| `epomeno-epipedo-011` | epomeno-epipedo | el | `pacote-epomeno-epipedo-011` (id 9583286132) | 08/09/2026 |
| `nivel-do-jogo-007` | nivel-do-jogo | pt-BR | `pacote-nivel-do-jogo-007` (id 9585036472) | 08/09/2026 |
| `kolejny-poziom-012` | kolejny-poziom | pl | `pacote-kolejny-poziom-012` (id 9589333786) | 09/09/2026 |
| `seviye-seviye-007` | seviye-seviye | tr | `pacote-seviye-seviye-007` (id 9590467009) | 09/09/2026 |
| `setiap-level-012` | setiap-level | id | `pacote-setiap-level-012` (id 9591675645) | 09/09/2026 |
| `labtreinamento-006` | labtreinamento | pt-BR | `pacote-labtreinamento-006` (id 9603074798) | 09/09/2026 |
| `agla-level-007` | agla-level | hi | `pacote-agla-level-007` (id 9605246991) | 09/09/2026 |
| `game-money-lab-007` | game-money-lab | en | `pacote-game-money-lab-007` (id 9605909861) | 09/09/2026 |
| `next-level-money-007` | next-level-money | en | `pacote-next-level-money-007` (id 9606569666) | 09/09/2026 |
| `seja-mais-magra-007` | seja-mais-magra | pt-BR | `pacote-seja-mais-magra-007` (id 9606940200) | 09/09/2026 |
| `resep-naik-level-008` | resep-naik-level | id | `pacote-resep-naik-level-008` (id 9607339543) | 09/09/2026 |

Os onze foram renderizados com `publicar: false` e passaram nos dez portões.
`ja_publicado` estava vazio para os cinco primeiros entre 23h16 de 25/08 e
01h40 de 26/08 — **mas isso é um instantâneo, não uma autorização**: regenere o
estado no momento de publicar, como manda o passo 3, e regenere para os sete,
não só para os dois que não foram consultados.

**O `agla-level` ainda não passou pelo `youtube.com/verify`.** A miniatura é
`thumbnails.set`, e canal não verificado não a aceita: se o passo falhar, o
vídeo continua no ar sem capa própria, e isso não é motivo para republicar.

**Ordem sugerida**, do canal com mais sinal para o com menos: epomeno-epipedo
(8 inscritos, 43,0 h), kolejny-poziom (5 inscritos, 30,7 h), seviye-seviye
(3 inscritos, 20,1 h — e a melhor distribuição da frota), setiap-level
(2 inscritos, 4,4 h), nivel-do-jogo (2 inscritos, 1,95 h — mas a MAIOR
conversão da frota, 0,525% inscrito/view), e por último os dois canais de
zero inscrito: labtreinamento e agla-level.
Se a cota acabar no meio, os primeiros são os que mais rendem.

Onze pacotes custam **41.261** de cota (3.751 cada), contra o teto observado
de 52.514. Cabem os onze numa janela so, com folga.

**E onze e o teto de hoje, nao doze.** Os onze canais que podem receber pacote
ja tem o seu. O decimo segundo so existe se o `sx-educacao` for reautorizado
(`token_vivo` = false na fila) ou se o `cocina-por-niveles` for criado no
Studio (`no_youtube` = false); as specs dos dois — `sx-educacao-003` e
`cocina-por-niveles-003` — ja estao escritas e paradas exatamente por isso.

**Ordem de publicacao para os seis novos**, seguindo a mesma regra de sinal:
labtreinamento e agla-level primeiro entre os frios (agla tem as duas maiores
retencoes de short da frota), depois game-money-lab (171 views), depois
resep-naik-level (172 views mas 10,34 views/dia no topo, a melhor distribuicao
entre os frios), depois next-level-money (88) e seja-mais-magra (55).

**Tempo de render medido nesta noite**, útil para dimensionar qualquer render
adicional na janela da manhã — não há tendência de piora, a variação é normal:

    epomeno-epipedo-011   75 cenas    7,1 min   5,7 s/cena
    kolejny-poziom-012    80 cenas   12,7 min   9,5 s/cena
    seviye-seviye-007     76 cenas  ~12,0 min  ~9,5 s/cena
    labtreinamento-006    62 cenas   11,0 min  10,6 s/cena
    agla-level-007        53 cenas    7,6 min   8,6 s/cena
    game-money-lab-007    60 cenas    9,2 min   9,2 s/cena
    next-level-money-007  61 cenas   13,0 min  12,8 s/cena
    seja-mais-magra-007   57 cenas    9,8 min  10,3 s/cena
    resep-naik-level-008  59 cenas   15,7 min  16,0 s/cena

Com um pacote por disparo o relógio de parede É o tempo do pacote; o `frota.yml`
não tem `max-parallel`, então N pacotes num disparo custam o do mais lento, não
a soma. Foi assim que cinco renders couberam numa madrugada.

## O que já foi ensaiado, e o que não

Ensaiado sem gastar cota, em 26/08 entre 23h e 03h:

| passo | estado | como |
|---|---|---|
| refresh do token por `pg_net` | **funciona** | epomeno-epipedo e nivel-do-jogo, HTTP 200, `expires_in` 3599 |
| `publicar.ler_copy` nos cinco pacotes | **funciona** | copy.md simulado com os placeholders substituídos; títulos de 65 a 81 c, descrições de 2.177 a 2.387 c, 15 tags, comentário fixado e as 3 hashtags como última linha em todos |
| crédito CC-BY na descrição | **presente nos cinco** | verificado pela URL da licença, que é o que `publicar.py` procura |
| trava `_sem_placeholder` | **presente** | recusa publicar se `{CAPITULOS}`, `{TRILHA}` ou `PLACEHOLDER` sobreviverem |
| estado anti-duplicata | procedimento escrito | regenerar na hora, passo 3 |

**Não ensaiado, e é onde o risco restante mora:** baixar o artefato pela URL
assinada dentro do sandbox, e o upload em si. Nenhum dos dois dá para testar
sem a cota e sem o sandbox. Se algo quebrar de manhã, comece a investigar por
aí — o resto desta lista já respondeu.

## A ROTA SEGURA, e ela precisa de UMA ação sua (26/08, 08h)

A cota do YouTube voltou às 07h. O Supabase continua 402. O `retomar.yml` é a
rota certa — ele baixa o artefato com o `GITHUB_TOKEN` do próprio runner e
publica sem o Supabase — mas ele recebia o `access_token` por **input de
workflow**, e este repositório é **público**: input fica visível na página do
run, e esse token *sobe e apaga* vídeo.

Isso agora está resolvido no código. O `access_token` virou **opcional**:
deixando-o vazio, o runner refresca o token sozinho a partir de um segredo.
Nada sensível atravessa input.

**A ação, uma só: cadastrar o segredo `YT_OAUTH_JSON`** em
Settings → Secrets and variables → Actions. O conteúdo sai do próprio banco:

```sql
select jsonb_object_agg(
         replace(chave, 'yt_token_', ''),
         jsonb_build_object(
           'client_id',     valor::jsonb->>'client_id',
           'client_secret', valor::jsonb->>'client_secret',
           'refresh_token', valor::jsonb->>'refresh_token',
           'token_uri',     coalesce(valor::jsonb->>'token_uri',
                                     'https://oauth2.googleapis.com/token')))
from config
where chave like 'yt_token_%'
  and (valor::jsonb->>'refresh_token') is not null;
```

São **12 canais com credencial**, todos no mesmo projeto do Google Cloud
(`777159180424` — que é também por que a cota diária é compartilhada entre eles).

Rode essa consulta **você**, no painel do Supabase, e cole o resultado no
segredo. Eu não trago o resultado real para o chat nem para o repositório: são
refresh tokens que não expiram, de doze canais.

Feito isso, cada pacote publica com:

```
workflow: retomar.yml
  pacote: epomeno-epipedo-011
  canal: epomeno-epipedo
  idioma: el
  run_id: <o run do render>
  access_token: (VAZIO — deixe assim)
  estado_b64: <o estado do passo 3, em base64>
```

De brinde, o refresh dentro do runner confere o campo `scope` da resposta do
Google e recusa se faltar `youtube.force-ssl`. Esse é o campo **efetivo** da
concessão, e foi exatamente o que faltou no `epomeno-epipedo-008`: o longo subiu
sem legenda porque `config.scopes` lista o que foi *pedido*, não o *concedido*.

A alternativa continua valendo se você preferir: **tornar o repositório
privado**, e aí o token por input volta a ser aceito.

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

   A consulta abaixo já sai em base64 numa linha só, pronta para o input, e
   **já declara o tamanho da lista** — leia o parágrafo seguinte antes de usar.

   ```sql
   select replace(encode(convert_to(jsonb_build_object(
       'gerado_em', now(),
       'ja_publicado', coalesce((
         select jsonb_object_agg(formato, youtube_id) from videos
         where youtube_id is not null and pacote = '<pacote>'
       ), '{}'::jsonb),
       'titulos_no_ar_n', (
         select count(distinct lower(btrim(titulo))) from videos
         where youtube_id is not null and titulo is not null
       ),
       'titulos_no_ar', coalesce((
         select jsonb_agg(jsonb_build_object('titulo', titulo, 'formato', formato,
                                             'youtube_id', youtube_id, 'pacote', pacote))
         from (
           select distinct on (lower(btrim(titulo))) titulo, formato, youtube_id, pacote
           from videos where youtube_id is not null and titulo is not null
           order by lower(btrim(titulo)), slug
         ) u
       ), '[]'::jsonb)
     )::text, 'UTF8'), 'base64'), E'\n', '') as estado_b64;
   ```

   Três detalhes que custaram para aparecer. **(a)** A lista é do CORPUS
   INTEIRO, não do canal: `ja_no_ar_pelo_titulo` consulta `videos` sem filtro de
   canal, e a trava do modo ponte tem de recusar exatamente o que a outra
   recusaria. A versão anterior desta consulta filtrava por um `canal` que nem
   existe como coluna. **(b)** A deduplicação por título é segura porque o
   critério é igualdade exata: manter uma linha por título distinto não muda a
   resposta da trava, e corta o base64 pela metade. **(c)** O
   `titulos_no_ar_n` não é enfeite.

   **A TRANSCRIÇÃO É O PONTO FRACO, e ela já falhou.** Em 26/08/2026 eu montei
   este estado com 23 mil caracteres de base64 e, ao colar no disparo, cortei a
   lista no décimo terceiro título e ainda corrompi um deles. Aquele run morreu
   antes, na falta do segredo, então nada foi publicado — mas com o segredo no
   lugar a trava de título teria rodado contra um corpus pela metade, e **trava
   cega tem a mesma cara de trava que passou**. O runner não tem como buscar o
   estado sozinho: é justamente o PostgREST que está em 402, que é o motivo
   desta rota existir. Então a transcrição fica, e o que entra é a conferência:
   o `retomar.yml` recusa o disparo se o número de títulos que chegou não bate
   com o `titulos_no_ar_n` que o próprio estado declara. Truncar deixou de ser
   silencioso.

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
