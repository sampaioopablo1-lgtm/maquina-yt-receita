# Os 9 canais que faltam

> Escrito em 05/08/2026, quando ficou claro que este é o único gargalo real.

## O diagnóstico, em uma linha

**18 pacotes prontos, 0 publicáveis.** O canal que existe (`setiap-level`) tem
**zero** aguardando — tudo dele já está no ar. Os 18 restantes pertencem a 9
canais que não existem no YouTube.

Não é produção: os arquivos estão renderizados, no Storage e no Drive.
Não é cota: restam 6 uploads no mês e o plano grátis aceita 2 perfis.
Não é bug: a rota de publicação está validada, 4/4 sobreviveram.

É uma ação de **~2 minutos por canal** que só o dono da conta pode fazer.

## Prioridade

| ordem | canal | idioma | pacotes prontos | mediana do nicho |
|---|---|---|---|---|
| **1** | Cocina por Niveles | es-MX | 3 | **127 v/d** ← a maior medida |
| 2 | Next Level Money | en | 3 | 4 v/d |
| 3 | Seviye Seviye | tr | 3 | não medido |
| 4 | Agla Level | hi | 3 | não medido |
| 5 | Epomeno Epipedo | el | 2 | 40 v/d |
| 6 | Kolejny Poziom | pl | 2 | 44,6 v/d |
| 7 | Game Money Lab | en | 2 | não medido |
| 8 | Resep Naik Level | id | 2 | não medido |
| 9 | Nível do Jogo | pt-BR | 2 | não medido |

Cocina primeiro por dois motivos que se somam: tem o maior número de pacotes
prontos e o nicho com a maior mediana de views/dia já medida no portfólio —
**quase 3× a do canal que está no ar hoje**.

## O que já está pronto do meu lado

Perfil `cocinaporniveles` criado na Upload-Post e link de conexão gerado
(validade de 48h — se expirar, eu gero outro em um comando).

Assim que o canal existir e o link for clicado, publico os 3 pacotes sem mais
nada: 2 longos de ~14:30 e 2 shorts, 4 uploads dos 6 que restam no mês.

## Como criar (2 min cada)

1. youtube.com → avatar → **Trocar de conta** → **Criar canal**
2. Nome exatamente como na tabela acima
3. Idioma do canal = o da tabela (isso alimenta a recomendação por região)
4. Foto e banner podem ficar para depois — não bloqueiam publicação

Feito isso, me passe o nome do canal criado. Eu pego o `youtube_channel_id`
pela API, gravo em `canais`, e o disparo seguinte já publica.

## Por que não publicar tudo no canal que existe

Porque destruiria o único ativo que está funcionando. O Setiap Level é
indonésio, de finanças e carreira, e o algoritmo do YouTube aprende o público
de um canal pelo histórico. Jogar vídeo em grego, turco e espanhol no mesmo
canal ensina o sistema que ele não tem público definido — e aí ele para de
recomendar também o que estava certo.
