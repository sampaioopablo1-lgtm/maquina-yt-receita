---
name: higgsfield-artes
description: >
  Como esta máquina gera artes, imagens, clipes de vídeo, thumbnails e lip
  sync com IA — pelo Open Higgsfield AI (ferramentas/open-higgsfield-ai, motor
  Muapi.ai, 221 modelos) e pelo MCP Higgsfield quando ele está conectado no
  chat. Use SEMPRE que o pedido envolver criar ou melhorar conteúdo visual:
  "gera uma arte", "imagem para a cena", "thumbnail", "b-roll gerado",
  "vídeo curto com IA", "avatar falando", "lip sync", "clipe cinemático",
  "cena com layout arte", "modelo de imagem", "Flux/Nano Banana/Kling/Veo",
  ou quando uma spec da fábrica precisar de visual além do SVG. Também vale
  para decidir qual modelo usar e quanto custa.
---

# Artes com IA nesta máquina (Open Higgsfield AI / Muapi + MCP Higgsfield)

Duas rotas, uma regra: **arte é enfeite** — nunca derruba render, nunca vira
identidade de pacote, sempre é declarada como conteúdo sintético.

## Rota A — Muapi (Open Higgsfield AI), a rota do repositório

Vale em qualquer sessão: sandbox, GitHub Actions, CLI local.

| Preciso de | Faça |
|---|---|
| imagem numa cena do longo | cena `{"layout": "arte", "arte_prompt": "...", "kicker": ..., "sub": ...}` na spec; a etapa 1.6 do `fabrica/etapas.py` gera e compõe |
| gerar as artes de um pacote sem renderizar | `python3 fabrica/arte.py fabrica/specs/<pacote>.json` (workdir de `caminhos.dir_trabalho`, `FABRICA_WORKDIR` sobrepõe) |
| imagem avulsa por script | `fabrica/muapi.py`: `gerar_imagem(chave, "flux-schnell", prompt, "saida.png", largura=1280, altura=720)` |
| clipe de vídeo a partir de imagem | `fabrica/muapi.py`: `gerar_video(chave, "kling-v2.1-standard-i2v", prompt, "clip.mp4", image_url=upload(chave, "img.png"), duration=5)` |
| retrato + áudio → avatar falando | `lipsync(chave, "infinitetalk-image-to-video", upload(chave,"voz.mp3"), "fala.mp4", image_url=upload(chave,"rosto.png"), resolution="720p")` |
| pipeline `src/maquina` com imagens geradas | `MAQ_IMAGE_PROVIDER=muapi MAQ_IMAGE_MODEL=nano-banana-2` |
| explorar modelos/prompts com interface | `cd ferramentas/open-higgsfield-ai && npm install && npm run dev` |

Chave: `MUAPI_API_KEY` no ambiente, ou `config.muapi_api_key` no Supabase
(`vevocauwtarctfwngrch`). `arte.chave()` diz de onde veio; se não houver,
**diga ao Pablo** que falta a chave em vez de fingir que a arte saiu.

Protocolo (se precisar chamar à mão com curl):
```
POST https://api.muapi.ai/api/v1/<endpoint>   -H "x-api-key: $MUAPI_API_KEY"  → request_id
GET  https://api.muapi.ai/api/v1/predictions/<request_id>/result           → status, outputs[0]
```
Endpoint ≠ id em poucos casos (`flux-schnell` → `flux-schnell-image`): consulte
`config/muapi_modelos.json` ou `fabrica/muapi.py::ENDPOINTS`.

## Rota B — MCP Higgsfield (quando as ferramentas `mcp__Higgs_field__*` existem no chat)

Use `generate_image`, `generate_video`, `generate_audio`, `models_explore(action:'recommend')`,
`get_workflow_instructions` (explicadores multi-etapa), `shorts_studio_*`,
`upscale_image`, `remove_background`. Para vídeos narrados estilo Vox use o
skill `vox-motion-graphics`. Antes da primeira geração paga, poste um plano
curto (peças, modelo, crédito estimado) e siga sem esperar aprovação, salvo
se o Pablo pedir para ser consultado. Baixe o resultado e trate como qualquer
arte: crédito, disclosure, identidade do canal.

Se as duas rotas existem, prefira a **A** para o que vai para o repositório
(reprodutível, sem depender da sessão) e a **B** para peças únicas no chat.

## Escolha de modelo (referência em `references/modelos.md`)

| Uso | Modelo | Por quê |
|---|---|---|
| cena do longo (volume, barato) | `flux-schnell` | ~2 s, menor custo; aceita width/height |
| thumbnail / peça de destaque | `nano-banana-2` (2k) ou `seedream-5.0` (high) | composição e luz melhores; aspect_ratio 16:9 |
| edição com referência (manter rosto/objeto) | `nano-banana-2-edit` (até 14 refs), `flux-kontext-pro-i2i` | edição por instrução |
| clipe curto a partir de imagem | `kling-v2.1-standard-i2v` (5 s), `wan2.2-image-to-video` (720p) | custo/qualidade |
| clipe cinematográfico premium | `veo3.1-fast-image-to-video`, `kling-v3.0-pro-image-to-video` | só com experimento registrado |
| avatar falando | `infinitetalk-image-to-video` (720p) | retrato + áudio; `ltx-2.3-lipsync` para 1080p |
| lip sync em vídeo existente | `sync-lipsync`, `latent-sync` | vídeo + áudio |
| upscale / fundo | `topaz-image-upscale`, `ai-background-remover` | pós-produção |

## Regras que não se negociam

1. **Prompt em inglês, sem texto na imagem.** `arte.py` já acrescenta
   `no text, no letters, no watermark, no logos`; não peça letras nem números.
2. **Estilo é do canal.** Um `arte_estilo` por spec, derivado de
   `config/canais/<slug>.yaml` (`estilo_visual`, paleta). Cena a cena com estilo
   diferente lê como colagem.
3. **Proporção do formato.** Longo 16:9 (1280×720); short 9:16 (720×1280);
   thumbnail 1280×720 com até 3 palavras **desenhadas pela fábrica**, nunca pela IA.
4. **Vídeo gerado custa por segundo.** Só com linha em `experimentos`, teto
   de crédito dito antes, e nunca substituindo o Ken Burns do pacote inteiro.
5. **Disclosure.** Toda peça gerada entra em `arte_creditos.json` e a
   publicação vai com `containsSyntheticMedia=true` (já obrigatório).
6. **Falha não é silêncio.** Log com `ULTIMO_MOTIVO`/origem da chave; na
   resposta final diga quantas cenas saíram com arte e quantas caíram no fallback.
7. **Nunca** mandar a chave para o git, nem para o copy, nem para o log.

## Quando atualizar o app

Substituir `ferramentas/open-higgsfield-ai/` pelo upstream (sem `docs/assets`),
rodar `node scripts/catalogo_muapi.mjs` e `pytest tests/test_arte.py`.
