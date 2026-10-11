# Destravar a publicação SEM reconectar o conector — o caminho medido

**11/10/2026.** O dono pediu: *"faça mudanças ou comece do zero sem depender
desta reconexão manual"*. Isto é o resultado, e começa pelo que foi **medido**,
não pelo que eu supunha.

## O que foi medido, e não suposto

| afirmação | como ficou |
|---|---|
| "a API de secrets é bloqueada para mim" | **verdade, mas o motivo era outro**: o 403 é do **PROXY** (`"not permitted through this proxy"`), não de permissão. Retestei com `admin: true` no repo e deu o mesmo. Trocar credencial nunca ia ajudar. |
| "dá para contornar o 402 por Postgres direto" | **não existe essa ponte**: nenhum `5432`, pooler ou `psycopg` no repo. O 402 é do *gateway*, então em teoria uma conexão direta passaria — mas ela nunca foi construída e a senha do banco não está em lugar nenhum que eu alcance. |
| "o runner pode publicar sozinho" | **o código existe e está completo** (`retomar.yml`), mas **o segredo está VAZIO**. |

**A sonda que provou isso:** `fabrica/sonda_oauth.py` +
`.github/workflows/sonda-oauth.yml`, run **38137596808**. Resultado literal, os
quatro com **0 chars**:

    YT_OAUTH_JSON: AUSENTE (0 chars)
    YT_TOKEN_LABTREINAMENTO: AUSENTE (0 chars)
    YT_TOKEN_EPOMENO_EPIPEDO: AUSENTE (0 chars)
    YT_TOKEN_KOLEJNY_POZIOM: AUSENTE (0 chars)

**Conclusão honesta: não falta código, falta CREDENCIAL.** Nenhuma engenharia
minha inventa um token do Google. O que eu pude fazer foi reduzir a ação humana
ao mínimo e deixá-la verificável.

## A rota certa é UMA colagem, e ela mata a ponte

O repo já chama isso de *"a rota segura"*: o segredo **`YT_OAUTH_JSON`** guarda
`{canal: {client_id, client_secret, refresh_token}}` e o runner **refresca o
access token direto no Google** (`retomar.yml`, passo "Refrescar o token dentro
do runner"). **Supabase não participa em ponto nenhum.**

Compare com o que eu vinha pedindo:

| o que fazer | custo | o que resolve |
|---|---|---|
| reconectar o conector Supabase | 3 cliques | devolve o banco, mas a ponte manual e o 402 continuam |
| **colar `YT_OAUTH_JSON`** | **1 colagem** | **o runner publica sozinho; a ponte MORRE; o Supabase deixa de ser necessário para publicar** |
| Supabase Pro | dinheiro | levanta o 402 e destrava o expurgo |

## CAMINHO A — montar o segredo pelo painel do Supabase (não precisa do conector)

O dono abre o **SQL Editor do projeto `vevocauwtarctfwngrch`** no site do
Supabase. Isso não passa pelo conector do Claude nem pelo REST, então **o 402
não atrapalha**. Roda:

```sql
select jsonb_pretty(jsonb_object_agg(
         replace(chave, 'yt_token_', ''),
         jsonb_build_object(
           'client_id',     valor::jsonb->>'client_id',
           'client_secret', valor::jsonb->>'client_secret',
           'refresh_token', valor::jsonb->>'refresh_token',
           'token_uri',     coalesce(valor::jsonb->>'token_uri',
                                     'https://oauth2.googleapis.com/token'))))
from config
where chave in ('yt_token_labtreinamento',
                'yt_token_epomeno-epipedo',
                'yt_token_kolejny-poziom');
```

O resultado é **exatamente** o valor do segredo. Ele vai em
**GitHub → Settings → Secrets and variables → Actions → New repository secret**,
com o nome `YT_OAUTH_JSON`.

**NÃO me mande esse valor no chat.** Eu não preciso vê-lo para nada, e segredo
colado em conversa fica registrado. A conferência é a sonda, que lê o segredo
dentro do runner e **nunca o imprime**.

## CAMINHO B — começar do zero, sem Supabase em nenhum passo

Serve se a consulta do caminho A voltar vazia, ou se o refresh token estiver
morto (eles morriam de sete em sete dias — aprendizado 303).

1. Abrir os **dois links de consentimento** de `docs/reautorizar-analytics.md`,
   escolhendo a conta de marca de cada canal. O `ESCOPOS` já inclui
   `yt-analytics.readonly` desde 09/10, então **este caminho também devolve a
   retenção** — que é a pendência que mais importa.
2. Da tela de consentimento sai uma URL com `?code=...`. O `client_id` e o
   `client_secret` estão no **Google Cloud Console** do próprio projeto OAuth
   (APIs e serviços → Credenciais), sem precisar do banco.
3. Trocar o `code` por `refresh_token` e montar o mesmo JSON do caminho A.

## A VERIFICAÇÃO, e ela é minha

Depois da colagem, eu disparo:

    gh api -X POST repos/<owner>/<repo>/actions/workflows/sonda-oauth.yml/dispatches -f ref=<branch default>

e leio as anotações. A sonda diz, **canal por canal**: refresh OK ou o erro
exato do Google (`invalid_grant` é token revogado, e distingue de cliente
errado), e quais escopos vieram — `youtube.upload`, `youtube.force-ssl` (decide
se o longo sobe com legenda) e `yt-analytics.readonly` (decide se a retenção
volta).

**O que a sonda nunca faz:** não imprime refresh token, client_secret nem access
token — nem truncados; não grava arquivo; não publica, não apaga, não altera
vídeo.

## E o que AINDA não é desbloqueado por isto

Publicar volta. **Medir não volta** — `metricas`, `videos` e
`consultas/estoque.sql` seguem no Supabase, atrás do 402 e do conector. E
**ritmo** tem dois tetos próprios já medidos: `TETO_POR_CANAL` em 1 peça/canal/dia
no caminho automático, e o cron entregando **5,1 disparos/dia** em vez de 48.

**E o limite de verdade de hoje não é cota, é PAUTA:** eram 10 origens livres em
09/10 contra ~14 peças consumidas no dia, e os ciclos seguem devolvendo "Nenhum
pacote pronto". Com o segredo colado, o que sai hoje é o `epomeno-epipedo-s016`
(renderizado, artefato vivo) — e depois a produção tem de virar **pacote
completo**, porque é o longo que fabrica pauta nova.
