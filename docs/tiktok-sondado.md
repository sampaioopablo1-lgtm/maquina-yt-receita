# TikTok — sondado em 12/10/2026, e a resposta e "nao com o formato de hoje"

O dono perguntou: *"consegue conectar ao TikTok tambem? assim aumentamos as
chances de monetizacao"*. Sondado antes de responder, porque hoje eu ja declarei
duas coisas impossiveis que nao eram.

## A rota EXISTE

O MCP do Higgsfield traz `tiktok_connect`, `tiktok_accounts`,
`tiktok_prepare_publish`, `tiktok_publish_status`, `tiktok_reconnect` e
`tiktok_music_trending`. Sondado: `tiktok_accounts` devolveu **lista vazia** —
nenhuma conta ligada. Conectar pede UM clique do dono num `authorize_url` que o
`tiktok_connect` gera e que expira em ~10 minutos.

## O QUE MATA A IDEIA DE MONETIZACAO, e e medida nossa contra regra deles

O **Creator Rewards Program** do TikTok exige video de **60 segundos ou mais**.
Medido nesta mesma rodada, a duracao REAL das nove pecas de hoje:

| peca | real |
|---|---|
| `6TNDVugoz5I` | 42 s |
| `nUrSPWKHy8I`, `rusVeiFco9Q` | 38 s |
| `ROU_meInccE` | 36 s |
| `da0GzPaMDoY` | 35 s |
| `DQKMvUi2FF4` | 34 s |
| `byriXB1gSg8` | 32 s |
| `MjeP-_yDni4` | 30 s |
| `K-k8vT0IY2M` | 29 s |

**Nenhuma passa de 42 s.** Logo, postadas no TikTok, elas **nao geram receita**
— nem uma. Elas geram alcance, que e outra coisa.

**E o longo nao resolve pelo outro lado:** o `tiktok_prepare_publish` aceita
video de **3 a 600 segundos**, e os nossos longos medem ~751 s (12:31). Curto
demais para pagar, longo demais para subir. Teria de existir um corte de 60 a
600 s que hoje nao existe no `etapas.py`.

Os limiares de conta (10.000 seguidores e 100.000 views em 30 dias) sao
secundarios diante disso, e **a procedencia deles e fraca**: as fontes sao guias
de terceiros, nao a documentacao do TikTok, e elas se contradizem no numero de
views. Pela regra da §5, isso entra como indicio, nao como numero.

## E ha um custo de rota que nao e obvio

O `video_url` do `tiktok_prepare_publish` **tem de ser um asset hospedado no
Higgsfield** (o TikTok exige dominio de origem verificado). Os nossos MP4 vivem
em artefato do GitHub. Entao cada peca precisaria de um upload para o Higgsfield
antes — e o Higgsfield consome credito do dono. **Eu nao sei se `media_upload`
consome ou se so a geracao consome, e nao vou afirmar que sei.**

E `tiktok_prepare_publish` diz que o usuario revisa e submete um widget de
formulario, e que *"clients without MCP Apps cannot publish"*. Ou seja, mesmo
conectado, a publicacao nao e automatica como no YouTube: ela pede o dono na
tela a cada peca. Isso briga de frente com a autorizacao de 09/10, que existe
justamente para nao parar a cada peca.

## O que eu recomendo, e nao e "nao"

**Como monetizacao: nao, hoje.** Seria trabalho com retorno zero por regra
deles, e nao por opiniao minha.

**Como ALCANCE para o portao do YouTube: pode valer, e e um experimento
honesto.** O gargalo medido do YouTube nao e alcance, e **conversao** (1,0 a 1,3
inscrito por mil views). TikTok nao converte inscrito de YouTube — mas um short
que vai bem la pode trazer trafego para o canal, e isso e mensuravel: bastaria
comparar inscritos ganhos no canal nas semanas com e sem repost.

**E existe uma terceira coisa que muda a conta, e e decisao sua:** se a maquina
passasse a produzir **short de 60 a 90 s**, ele monetizaria no TikTok E
continuaria sendo Short no YouTube (o limite la e 3 minutos desde 2024). Isso e
uma mudanca de formato de producao, nao uma conexao — e ela briga com duas
medicoes nossas: o `chart=mostPopular` diz que o que explode dura 10 a 35 s, e o
playbook externo diz 15 a 60 s. **Short mais longo nao retem igual**, e sem
retencao eu nao sei dizer o custo.

## O que eu NAO fiz

Nao chamei `tiktok_connect`. Conectar uma conta nova de rede social e acao
externa e irreversivel na pratica (passa a existir um app autorizado na conta
dele), e a autorizacao de 09/10 cobre **pauta, render, publicacao e pacote** nos
TRES canais do YouTube — nao cobre abrir presenca em plataforma nova. Isso e
decisao dele, e agora ele tem os numeros para tomar.
