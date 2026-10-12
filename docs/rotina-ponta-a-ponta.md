# A rotina de ponta a ponta, com o banco fechado

**12/10/2026.** Até 11/10 a máquina dependia do Supabase em três pontos — pauta,
token e registro — e com o gateway em 402 ela parou. Dois deles caíram no mesmo
dia: o token passou a nascer no runner (`YT_OAUTH_JSON`) e a medição também
(`medir.yml`). Este documento é o ciclo inteiro **como ele funciona hoje**, com
o comando de cada passo, quem consegue executá-lo e o que ainda o bloqueia.

Ele não substitui `docs/ROTINA.md`, que é o prompt horário. Aquele diz *como
pensar*; este diz *o que rodar, em que ordem*.

---

## Passo 0 — Sondar os dois bloqueios (1 min, toda rodada)

```
mcp__Supabase__list_projects                      # tem de mostrar maquina-yt-dark
gh api repos/<owner>/<repo> --jq .default_branch  # NAO e main
gh api -X POST .../workflows/diario.yml/dispatches -f ref=<default> -f inputs[disparar]=false
gh api repos/<owner>/<repo>/check-runs/<job>/annotations
```

A anotação diz `porta ABERTA` ou `FECHADA (HTTP 402)`. **Se qualquer um
destravar, pare a engenharia e volte a produzir.**

---

## Passo 1 — PAUTA: de onde sai origem livre

Esta é a única restrição real do ritmo hoje. Em ordem de preferência:

**1a. Com o banco aberto:** `consultas/estoque.sql`. É a fonte canônica, e
exclui origem usada e grupo duplicado **por construção** (670).

**1b. Com o banco fechado — reconstrução local, medida em 12/10.** O retrato
`fabrica/ponte/videos.json` (06/10, 357 linhas) mais o `longo_existente` das
specs reproduz a conta:

```python
longos da frota no retrato            52
menos origens já usadas pelas specs  -44
menos ids do docs/duplicatas-a-apagar.md
menos grupo de título repetido
= 13 livres, das quais 5 TÊM youtube_id publicado
```

**Só as 5 com id servem**, porque o short precisa apontar para um longo que
existe. As outras 8 são longos sem id no retrato — pauta potencial, não atual.

**As três ressalvas, e elas não saem do relato:**
- o retrato é de **06/10**: longo publicado depois não aparece, então o número
  **subestima** — erra para o lado seguro;
- a exclusão de duplicata aqui é por **título repetido + o documento**, não pela
  mesma construção da consulta. Foi exatamente aqui que nasceu o erro 658;
- **5 origens são um a dois dias de produção**, não uma semana. Pauta nova só
  nasce de **longo novo**.

---

## Passo 2 — SPEC: escrever a peça

Ordem de escolha da origem em `docs/ROTINA.md` §4. O que o portão exige:

| portão | limite |
|---|---|
| `duracao` | 30 a 43,1 s estimados |
| mira | `alvo_short(canal)` — **por canal**, nunca a constante |
| esqueleto | 10 a 11 cenas, uma frase curta por cena |
| `variedade` | gancho ≤ 12 palavras; thumbnail ≤ 4 palavras |
| título | próprio, ≤ 45 caracteres |

Conferir com `python3 fabrica/prontidao.py fabrica/specs/<spec>.json` — **o
caminho do .json**, não o nome do pacote. Doze portões, onze no short solto.

---

## Passo 3 — RENDER (no runner, nunca aqui)

`frota.yml` com **`publicar: false` sempre**. Este container não sintetiza voz
(`speech.platform.bing.com` leva 403 no CONNECT), então render local está fora.

O artefato sai como `pacote-<slug>` e vive ~90 dias.

---

## Passo 4 — PUBLICAR, sem Supabase

Rota provada em 11/10 (run `38175747708`, `epomeno-epipedo-s016` =
`6TNDVugoz5I`). `retomar.yml` com:

| input | de onde sai |
|---|---|
| `pacote`, `canal`, `idioma` | da spec |
| `run_id` | o run que guarda o artefato do render |
| `access_token` | **VAZIO** — o runner refresca sozinho pelo `YT_OAUTH_JSON` |
| `estado_b64` | base64 de `{ja_publicado, titulos_no_ar, titulos_no_ar_n}`, montado do `fabrica/corpus_publicados.json` |

O runner confere `titulos_no_ar_n` contra o tamanho da lista e **recusa lista
truncada** — a trava que nasceu do erro de 26/08.

**Depois de publicar, no mesmo passo:** acrescentar o título ao
`corpus_publicados.json` e commitar. Sem isso a segunda fonte anti-duplicata
fica atrasada e o ciclo seguinte reoferece o pacote — o defeito consertado em
11/10.

---

## Passo 5 — MEDIR, sem Supabase

`medir.yml` → `fabrica/medir.py`. Três leituras, piso pelo máximo,
`replica.chamada_para_gravar` escolhe pela soma, denominador = soma das peças
da máquina casadas por título contra o corpus. Primeira rodada: `38186165873`.

**O que ele ainda NÃO faz:** gravar em `metricas`. O número sai em anotação e
precisa ser recuperado à mão quando a porta reabrir.

**O que ele ainda não pode medir:** retenção. Depende dos dois cliques de
consentimento (`docs/reautorizar-analytics.md`), e sem ela os experimentos 37,
38 e 40 são indecidíveis — views/peça é cego abaixo do dobro sob CV 0,66 (693).

---

## Passo 6 — VIGIAR

O próprio `medir.py` nomeia peça fora de `processed`. Em 12/10 eram **quatro**:
`Ta_KN8yXLaI`, `oHwlhhneIos` (epomeno), `ylsKfJ5Kv4s` (kolejny) e
`7cL4zLk5aUg` (labtreinamento) — este último descoberto pela primeira rodada do
medidor. Apagar e republicar é irreversível: **decisão do dono.**

---

## O que limita o ritmo, em ordem

1. **PAUTA** — 5 origens com id. É o teto de hoje.
2. **`TETO_POR_CANAL` = 1 peça/canal/dia** no caminho automático. A ponte manual
   não consulta o teto, então publicação dirigida não esbarra nele.
3. **O cron entrega 5,1 disparos/dia**, não 48. Ritmo garantido só por
   `workflow_dispatch`.
4. **Cota** — ~40 vídeos/janela. Não é o gargalo.

**Nada disso chega aos 7/dia/canal pedidos.** O caminho até lá passa por longo
novo (que fabrica pauta), não por mexer em teto.
