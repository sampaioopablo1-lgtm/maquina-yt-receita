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
longos da frota publicados COM youtube_id no retrato   46
menos origens já usadas pelas specs                   -34
= 12 ids livres
```

**RETRATAÇÃO DE 12/10, 08:2x, e é do número que eu mesmo escrevi aqui ontem
("13 livres, das quais 5 com id"). Medido agora, os 12 ids livres são TRÊS
origens, não doze** — porque **dez dos doze carregam o MESMO TÍTULO**,
`Emerytura z ZUS: 34,4% pensji w 2050 roku`, publicado onze vezes por um cron
entre 13 e 17/08. É um grupo de DUPLICATA, e a regra 658/670 manda contar por
**título DISTINTO**:

| origem distinta | canal | id |
|---|---|---|
| ΕΝΦΙΑ, a dedução de 20% | epomeno | `uWs-k_Wrn_w` |
| Emerytura z ZUS (dez cópias no ar, vale UMA) | kolejny | `IjogSl2TE4M` …e nove irmãs |
| Próg Podatkowy 120 000 zł | kolejny | `W_iFAIQWvi8` |

**E esses dez não estão em `docs/duplicatas-a-apagar.md`** — o filtro daquele
documento não os pega, então uma reconstrução que só subtrai o documento **conta
dez origens que não existem**. Era o que a minha conta de ontem fazia.

**Logo a pauta real é TRÊS origens, e não cinco.** Contar id em vez de título
distinto é literalmente o efeito (C-2) da rotina: *"ordenar pelo alcance do short
original PREMIA DUPLICATA"*, na sua forma mais crua — somar duplicata como
estoque.

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
| `estado_b64` | **`python3 fabrica/estado_ponte.py`** — não monte à mão |

**NÃO MONTE O `estado_b64` À MÃO, e isto é retratação de um parágrafo que estava
aqui.** Este documento dizia só "base64 de `{ja_publicado, titulos_no_ar,
titulos_no_ar_n}`", e eu montei duas vezes no mesmo dia seguindo essa frase. Na
segunda errei a forma: `titulos_no_ar` como lista de **strings**, quando a trava
`publicar._iguais_no_estado` lê lista de **objetos** com a chave `titulo`. O run
`38217254505` baixou o pacote, passou pela conferência e morreu em
`AttributeError`. `fabrica/estado_ponte.py` monta e confere; o `retomar.yml`
agora chama `estado_ponte.confere` e **para antes de baixar** se a forma
estiver errada.

O runner confere `titulos_no_ar_n` contra o tamanho da lista e **recusa lista
truncada** — a trava que nasceu do erro de 26/08. Conferir o tamanho **não
basta**: era exatamente o que ele fazia quando a forma errada passou verde.

**Depois de publicar, no mesmo passo:**
```
python3 fabrica/estado_ponte.py adiciona fabrica/specs/<spec>.json
```
e commitar. Idempotente, ordenado, e sabe que **short solto entra pelo `##
TITULO SHORT`, nunca pelo `## TITULO`** — o título do longo nunca foi ao ar.
Sem essa soma a segunda fonte anti-duplicata fica atrasada e o ciclo seguinte
reoferece o pacote: foi o defeito consertado em 11/10, e o corpus estava
atrasado outra vez em 12/10.

**O `youtube_id` sai em `::notice::`** desde 12/10. Antes ele só era impresso no
log, e log de job não se lê por API daqui — a publicação do `s018` deu certo
(run `38217420591`) e ficou sem id nomeado por causa disso.

---

## Passo 5 — MEDIR, sem Supabase

`medir.yml` → `fabrica/medir.py`. Três leituras, piso pelo máximo,
`replica.chamada_para_gravar` escolhe pela soma, denominador = soma das peças
da máquina casadas por título contra o corpus. Primeira rodada: `38186165873`.

**O que ele ainda NÃO faz:** gravar em `metricas`. O número sai em anotação e
precisa ser recuperado à mão quando a porta reabrir.

**A narração hoje é do PIPER, não do edge-tts.** O `edge_tts` devolve 403 no
handshake do runner desde 12/10 (runs `38198672898` e `38202568056`, e de novo
nas duas peças do dia), então `voz_piper` entra como fallback e cada peça sai com
`::warning::` de calibração. **O `R` e o `P` de `MODELO_VOZ` são do edge-tts e
não valem para essas vozes** — é o erro do 679/698 se alguém usar o número delas
para mira ou para o portão `duracao`. O instrumento para remedir é
`calibra-piper.yml` → `fabrica/calibra_piper.py`, que mede com o texto das specs
reais e **não escreve em `ensaio.py`**: colar é decisão, e ainda falta decidir o
que fazer com a tabela quando o edge-tts voltar.

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
