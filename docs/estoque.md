# Estoque de origens livres

Atualizado: 2026-10-09. **Este arquivo nao carrega mais a lista.**

## O que mudou, e por que

A lista de origens livres morava aqui, escrita a mao a cada rodada. Antes disso
morava dentro do prompt da rotina horaria. Nos dois lugares ela envelheceu e
produziu erro:

- **652/655** — "estoque de origem ZERO" porque contei longos das embalagens
  recentes. O banco tinha 55 longos.
- **658** — apontei `_M8t8SPC_f0` como a melhor origem livre do kolejny. Era uma
  das **seis copias do mesmo video**, marcadas para exclusao em
  `duplicatas-a-apagar.md`. O CTA do short teria apontado para um video a apagar.
- **09/10** — a lista dizia **27 livres**. A consulta derivada diz **23**. A mao
  estava errada em quatro, e nao havia como eu saber qual numero valia.

A causa raiz nao era desatencao, e levou dois meses para aparecer: **a origem
consumida nao existia no banco.** `fonte_pauta_vd` e numerico (score) e
`fonte_pauta` e o texto da pesquisa do longo. Logo "quais origens eu ja usei" so
existia na minha lista escrita a mao — e uma lista a mao e um instrumento que
mente sem avisar.

## O conserto

1. Migracao `videos_origem_id`: coluna `videos.origem_id`, indexada.
2. Backfill dos 27 shorts soltos lendo o `longo_existente` da propria spec.
   Isso revelou de imediato um defeito invisivel ate entao: **epomeno-s002 e
   epomeno-s006 usaram a MESMA origem** (`h04-UVlVevs`).
3. `consultas/estoque.sql` — a consulta canonica. Origem usada e titulo
   duplicado saem **por construcao**.

**Rode `consultas/estoque.sql` antes de escolher pauta. Nao reescreva a lista
aqui.** Toda spec nova grava `origem_id` quando publica, entao a consulta se
mantem sozinha.

## O que a consulta NAO sabe

O **perfil** da origem. O aprendizado 651 mediu espalhamento de ~30x no
labtreinamento entre dinheiro proprio com papel na mao (1.111 e 1.133 views) e
conformidade corporativa (4 a 70) — e as **seis** livres que restam naquele canal
sao todas do segundo tipo. Contar origem livre sem olhar o perfil **superestima o
estoque util**. Por isso a consulta devolve o titulo: o perfil continua sendo
leitura, nao consulta.

A saida estrutural no labtreinamento e **pacote completo** (calendario liberado
desde 07/10), que cria origem nova de dinheiro proprio, nao minerar conformidade.

## Faixas de identidade

Use a faixa ATUAL do canal, nunca a paleta da embalagem de origem (601).

| canal | paleta | trilha |
|---|---|---|
| labtreinamento | `#22333B #A4243B #D8973C #F4F1EA` | Inspired |
| epomeno-epipedo | `#12263A #2A9D8F #E8A33D #F5F2EC` | Inspired |
| kolejny-poziom | `#1B3A5C #2A9D8F #F5B841 #F4F1EA` | Wholesome |

## Duplicatas a apagar

Em `docs/duplicatas-a-apagar.md`. Sao 46 e **dependem do dono**: apagar video
publicado e irreversivel. A consulta acima ja as exclui como origem, entao elas
nao contaminam mais a escolha de pauta — o que restava era o teto de upload.
