# Open Higgsfield AI + Muapi — artes, imagens, vídeos e lip sync

Instalado em 22/09/2026 a partir de
[Autom8AI/Open-Higgsfield-AI](https://github.com/Autom8AI/Open-Higgsfield-AI)
(commit `b578108`, idêntico ao zip `Open-Higgsfield-AI-main.zip` enviado pelo
Pablo). O código vive em **`ferramentas/open-higgsfield-ai/`**, sem os 14 MB de
mídia de demonstração de `docs/assets`.

## O que é

Um estúdio web open-source (Next.js + React) com quatro abas — **Image Studio**,
**Video Studio**, **Lip Sync** e **Cinema Studio** — em cima da API da
[Muapi.ai](https://muapi.ai), que expõe **221 modelos** com uma única chave:

| Categoria | Modelos | Exemplos |
|---|---|---|
| texto → imagem | 51 | Flux Schnell/Dev/2, Nano Banana 2, Seedream 5.0, Ideogram v3, Imagen 4, GPT Image 1.5 |
| imagem → imagem | 57 | Nano Banana 2 Edit (14 refs), Flux Kontext, upscalers, remover fundo, face swap |
| texto → vídeo | 42 | Kling v3, Veo 3.1, Sora 2, Wan 2.6, Seedance 2.0, Hailuo 2.3, LTX 2 |
| imagem → vídeo | 61 | Kling I2V, Veo 3.1 I2V, Wan 2.2 I2V, Seedance I2V, Runway, Grok Imagine |
| lip sync | 9 | Infinite Talk, Wan 2.2 S2V, LTX 2.3 Lipsync, Sync, LatentSync, Veed |
| vídeo → vídeo | 1 | remover marca d'água |

O catálogo inteiro, com o `endpoint` de cada id e os enums de `aspect_ratio`,
`resolution` e `duration`, está em **`config/muapi_modelos.json`**
(gerado por `node scripts/catalogo_muapi.mjs` a partir do `models.js` do app).

A API tem duas etapas e é a mesma para tudo:

```
POST https://api.muapi.ai/api/v1/<endpoint>            x-api-key: <chave>   → {"request_id"}
GET  https://api.muapi.ai/api/v1/predictions/<id>/result                     → status + outputs[0]
POST https://api.muapi.ai/api/v1/upload_file            multipart            → URL (referências)
```

## Chave

1. Conta em [muapi.ai](https://muapi.ai) → **API Keys**. Uma chave serve ao estúdio
   web, à fábrica e à pipeline.
2. Onde gravar:
   - `.env` local: `MUAPI_API_KEY=...`
   - GitHub Actions: secret `MUAPI_API_KEY` (o `frota.yml` já o exporta no render)
   - Supabase (rota do sandbox, como o Pexels):
     ```sql
     insert into config (chave, valor) values ('muapi_api_key', to_jsonb('<chave>'::text))
     on conflict (chave) do update set valor = excluded.valor;
     ```
   `fabrica/arte.py` procura primeiro no ambiente, depois no banco, e diz no log
   onde achou (ou não achou) — a mesma disciplina do `broll.py`.

## Três portas para a mesma coisa

### 1. Estúdio web (para explorar e para o Pablo gerar à mão)

```bash
cd ferramentas/open-higgsfield-ai
npm install            # já validado aqui: 869 pacotes, build ok
npm run dev            # http://localhost:3000 → pede a chave na primeira abertura
```

Serve para testar prompt e modelo antes de colocar numa spec, e para gerar
peças avulsas (thumbnail alternativa, capa de canal, avatar). O que sair daqui
e for usado num pacote entra em `arte_creditos.json` / copy como conteúdo
sintético, como qualquer outra imagem gerada.

### 2. Fábrica — layout `arte` (o que a rotina usa)

Cena nova na spec, irmã do `broll`:

```json
{"layout": "arte", "kicker": "Biaya yang tidak kamu setujui", "sub": "…",
 "arte_prompt": "close-up of a bank statement with small recurring fees highlighted, desk lamp, moody",
 "cap": "Biaya tersembunyi", "nar": "…"}
```

- `arte_prompt` em inglês, descrevendo cena, não texto. A fábrica acrescenta
  sozinha `no text, no letters, no watermark` e o `arte_estilo` da spec (um
  bloco fixo por canal, para as cenas pertencerem ao mesmo vídeo).
- `arte_modelo` opcional por cena; o padrão é `flux-schnell` (barato, ~2 s).
  `MUAPI_MODELO_IMAGEM` muda o padrão do run.
- A etapa **1.6** do `etapas.py` gera a imagem, escurece 18%, e compõe o cartão
  transparente por cima. `elementos()` devolve 0, o clipe segue o Ken Burns de
  sempre. Sem chave, sem rede ou com a API em erro a cena cai no fallback
  (cartão sobre preto) e o render **nunca** para — arte é enfeite.
- Capítulo pode abrir em `arte`, como abre em `titulo` e `broll`
  (`prontidao.py`, `copy_md.py`).
- Regra editorial (em `estilo.py`, que a autoria lê): no máximo uma cena
  `arte` a cada quatro, nunca no short, e sempre com o mesmo `arte_estilo`.

Gerar só as artes de um pacote, sem renderizar:

```bash
python3 fabrica/arte.py fabrica/specs/<pacote>.json   # workdir de caminhos.dir_trabalho
```

### 3. Pipeline `src/maquina` — provider `muapi`

```bash
MAQ_IMAGE_PROVIDER=muapi MAQ_IMAGE_MODEL=nano-banana-2 maquina produzir "Título"
```

`ImagemMuapi` implementa `GeradorImagem` (cenas + fundo da thumbnail).
`VideoMuapi` expõe `de_imagem`, `de_texto` e `lipsync` para quem quiser clipes
gerados ou um apresentador falando — não entra na pipeline sozinho, porque
custa crédito por segundo e ainda não há medida de retenção que o justifique.

## Custo e cuidado

- Imagem: centavos (Flux Schnell é o piso). Vídeo: cobrado por segundo e por
  modelo — **não** ponha vídeo gerado numa spec sem registrar o experimento em
  `experimentos` e sem teto de gasto.
- Toda peça gerada é conteúdo sintético: a publicação já manda
  `containsSyntheticMedia=true`; o copy continua dizendo isso.
- Identidade visual é do **canal** (paleta, cartão, fonte). A arte gerada fica
  atrás do cartão justamente para não virar identidade de pacote.
- Prompt nunca pede texto na imagem: letras geradas saem erradas no idioma do
  canal e o TTS/legenda já carregam o texto.

## Manutenção

- Atualizar o app: substituir `ferramentas/open-higgsfield-ai/` pelo upstream
  (sem `docs/assets`), rodar `node scripts/catalogo_muapi.mjs` e o
  `tests/test_arte.py` (ele confere que todo id com endpoint diferente no app
  está no mapa `ENDPOINTS` de `fabrica/muapi.py`).
- `node_modules`, `.next`, `dist` e `release` estão no `.gitignore`.
