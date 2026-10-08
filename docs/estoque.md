# Estoque de origens livres (medido no banco, nao de memoria)

Atualizado: 2026-10-08, rodada 18:20. Aprendizados 658 a 662.

## Por que este arquivo existe

A rotina horaria carregava estas listas dentro do proprio prompt. Duas vezes
isso envelheceu e produziu erro:

- **652/655**: a rotina dizia "estoque de origem ZERO" porque eu havia contado
  longos das embalagens RECENTES. O banco tinha 55 longos.
- **658**: a rotina dizia "41 origens virgens" e apontava `_M8t8SPC_f0` como a
  melhor origem livre do kolejny. `_M8t8SPC_f0` e uma das **6 copias do mesmo
  video** listadas em `duplicatas-a-apagar.md`. Se eu tivesse construido a
  partir daquela lista, o CTA do short apontaria para um video marcado para
  exclusao.

Entao a lista mora aqui, versionada, e a rotina so aponta para este arquivo.

## A consulta (uma por chamada, sempre no banco)

Grupo duplicado a excluir inteiro (nao `row_number()=1` — a primeira copia
tambem sera apagada):

```sql
select canal, formato, titulo, count(*) from videos
 where youtube_id is not null and titulo is not null
 group by 1,2,3 having count(*) > 1;
```

Hoje retorna exatamente duas linhas, as duas do kolejny-poziom,
titulo `Emerytura z ZUS: 34,4%...`:
6 longos (`_M8t8SPC_f0 5gHnniPl0f8 jDa9SM8A7os qcY5XC1KtlQ SZV9Vk5YFwI YLGwalTND7M`)
e 5 shorts (`2ywuj5CvQLw IjogSl2TE4M Ry9BgorzJA8 tVKaCqnTR3g VUF-ZhmBJWI`).

Contagem honesta por **titulo DISTINTO**, excluido o grupo duplicado e todas as
origens ja usadas: epomeno 18/18 titulos, labtreinamento 13/13,
kolejny 24 longos mas **19 titulos**. Livres: 12 + 13 + 11 = **36** as 14:09; cinco consumidas em 08/10 (labtreinamento s004/s005, kolejny s008/s009, epomeno s009) -> **31**.

## Origens livres e limpas (11 por canal)

Numero entre parenteses = views do short que saiu daquele tema, quando existe.
E um proxy fraco e enviesado: premiava duplicacao (foi exatamente o defeito do
658). Use como tie-break, nunca como criterio unico.

### epomeno-epipedo (GR)
`TJZcjE-uv8E` (600) · `uWs-k_Wrn_w` (540) ·
`jAWKppvjAG8` (428) · `alZ97hpgqXo` (386) · `h66MCKjwAJ8` (311) ·
`P2q6w9y7j88` (301) · `os51d8fA0sY` (191) · `wUHuwyO2HYo` (1) ·
`GwNkPfM9pSY` (—) · `eZ697VNYCPU` (—)

Ja usada e fora da lista: `jUxJPvmA4Mk` (541, s009).

### kolejny-poziom (PL)
`Xgt32iH8Ft8` (165) ·
`kDkagIf2isA` (72) · `wb1RGIx7OJI` (69) · `SP7Vz8qHdRY` (68) ·
`iqV7m6tKb5A` (47) · `vcJf6WipLtY` (42) · `42hpD7eaptE` (34) ·
`EwUkhdwyuuo` (27) · `34SgUG7rf0U` (0)

Ja usadas e fora da lista: `Rj7beZkOeYo` (172, s008), `ef_oZmfmdz4` (86, s009).

### labtreinamento (BR)
`Sr6VhvD_aPE` (80) ·
`lau1nnOUm1U` (46) · `6BeNHqT2okA` (41) · `KRUERlNPzDw` (28) ·
`StQNFMdpGdk` (26) · `3KtwRYxl7_U` (22) · `yrWVyqQtw00` (21) ·
`XgqPVJuAk3o` (4)

Ja usadas e fora da lista: `4OYBkCHFTV8` (1111, s003), `bQoujWaY7Hw` (212, s004), `dsoEo103l1o` (82, s005),
`NNgAQLlpEzg`, `ntrMxq89I4o`.

## Regra de escolha de pauta (651)

No labtreinamento o espalhamento de ~30x e "de quem e o numero": dinheiro
proprio com papel na mao (1133, 1111) contra compliance corporativo (4-70).
Confundidor declarado: as embalagens de compliance tambem sao as mais antigas.
Prefira dinheiro proprio.

## Faixas de identidade (use a faixa ATUAL, nunca a paleta antiga da embalagem de origem)

| canal | paleta | fonte |
|---|---|---|
| labtreinamento | `#22333B #A4243B #D8973C #F4F1EA` | Inspired |
| epomeno-epipedo | `#12263A #2A9D8F #E8A33D #F5F2EC` | Inspired |
| kolejny-poziom | `#1B3A5C #2A9D8F #F5B841 #F4F1EA` | Wholesome |

## Como manter

Rode a consulta de duplicatas e a de estoque **antes de escolher pauta**, nao de
memoria, e reescreva este arquivo quando o resultado mudar. Toda origem usada
sai da lista no mesmo commit do short.

## Aviso sobre o perfil do estoque do labtreinamento (17:20 de 08/10)

As OITO origens livres que sobraram no labtreinamento sao **todas de
conformidade corporativa** — NR-1, ISO 9001, NR-10, FAP, CAT, treinamento
vencendo, custo por turma. E exatamente o perfil que o 651 mediu como ~30x PIOR
(4 a 70 views contra 1.111 e 1.133), porque ali o numero e do empregador e nao do
espectador. As duas de dinheiro proprio (`bQoujWaY7Hw`, `dsoEo103l1o`) foram
consumidas em 08/10.

Consequencia pratica: **contar origem livre sem olhar o PERFIL superestima o
estoque util.** O labtreinamento tem oito livres e zero do perfil que funciona.
A saida estrutural e PACOTE COMPLETO no canal (calendario liberado desde 07/10
09:46), que cria origem nova de dinheiro proprio, nao minerar compliance.
