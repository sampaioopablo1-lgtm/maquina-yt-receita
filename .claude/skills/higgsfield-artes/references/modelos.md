# Catálogo Muapi (Open Higgsfield AI)

Gerado de `config/muapi_modelos.json` (commit b578108 do app). Endpoint = id salvo onde indicado.
Campos entre parênteses são os aceitos pelo modelo; enums resumidos.

## Texto → imagem (51)

| id | endpoint | campos | proporções / resolução / duração |
|---|---|---|---|
| `nano-banana` | = | prompt, aspect_ratio | AR: 1:1 3:4 4:3 9:16 16:9 3:2 2:3 5:4 |
| `flux-dev` | flux-dev-image | prompt, width, height, num_images |  |
| `flux-dev-lora` | = | prompt, model_id, width, height, num_images |  |
| `flux-kontext-dev-t2i` | = | prompt, aspect_ratio, num_images | AR: 16:9 9:16 1:1 4:3 3:4 3:2 2:3 21:9 |
| `hidream-i1-fast` | = | prompt, width, height, num_images |  |
| `hidream-i1-dev` | = | prompt, width, height, num_images |  |
| `hidream-i1-full` | = | prompt, width, height, num_images |  |
| `ai-anime-generator` | = | prompt, width, height |  |
| `wan2.1-text-to-image` | = | prompt, width, height |  |
| `flux-kontext-pro-t2i` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 4:3 3:4 21:9 16:21 |
| `flux-kontext-max-t2i` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 4:3 3:4 21:9 16:21 |
| `gpt4o-text-to-image` | = | prompt, aspect_ratio, num_images | AR: 1:1 2:3 3:2 |
| `midjourney-v7-text-to-image` | = | prompt, speed, aspect_ratio, variety, stylization, weirdness | AR: 1:1 16:9 9:16 3:4 4:3 1:2 2:1 2:3 |
| `flux-schnell` | flux-schnell-image | prompt, width, height, num_images |  |
| `bytedance-seedream-v3` | = | prompt, aspect_ratio | AR: 1:1 16:9 9:16 3:4 4:3 |
| `qwen-image` | = | prompt, aspect_ratio, num_images | AR: 16:9 9:16 1:1 4:3 3:4 21:9 9:21 3:2 |
| `flux-pulid` | = | prompt, image_url, aspect_ratio | AR: 16:9 9:16 1:1 4:3 3:4 |
| `ideogram-v3-t2i` | = | prompt, render_speed, style, aspect_ratio, num_images | AR: 1:1 3:4 4:3 9:16 16:9 |
| `google-imagen4` | = | prompt, aspect_ratio, num_images | AR: 16:9 9:16 1:1 4:3 3:4 |
| `google-imagen4-fast` | = | prompt, aspect_ratio, num_images | AR: 16:9 9:16 1:1 4:3 3:4 |
| `google-imagen4-ultra` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 4:3 3:4 |
| `sdxl-image` | = | prompt, width, height |  |
| `bytedance-seedream-v4` | = | prompt, aspect_ratio, resolution, num_images | AR: 1:1 16:9 9:16 3:4 4:3 2:3 3:2 21:9; res: 1K 2K 4K |
| `hunyuan-image-2.1` | = | prompt, width, height |  |
| `chroma-image` | = | prompt, width, height |  |
| `flux-redux` | = | prompt, image_url, aspect_ratio, num_images | AR: 16:9 9:16 1:1 4:3 3:4 3:2 2:3 21:9 |
| `flux-krea-dev` | = | prompt, aspect_ratio, num_images | AR: 16:9 9:16 1:1 4:3 3:4 3:2 2:3 21:9 |
| `perfect-pony-xl` | = | prompt, width, height |  |
| `neta-lumina` | = | prompt, width, height |  |
| `wan2.5-text-to-image` | = | prompt, width, height |  |
| `hunyuan-image-3.0` | = | prompt, width, height |  |
| `leonardoai-phoenix-1.0` | = | prompt, aspect_ratio | AR: 1:1 16:9 9:16 3:4 4:3 4:5 5:4 2:3 |
| `leonardoai-lucid-origin` | = | prompt, aspect_ratio | AR: 1:1 16:9 9:16 3:4 4:3 4:5 5:4 2:3 |
| `reve-text-to-image` | = | prompt, aspect_ratio | AR: 21:9 16:9 4:3 1:1 3:4 9:16 9:21 |
| `grok-imagine-text-to-image` | = | prompt, aspect_ratio | AR: 9:16 16:9 2:3 3:2 1:1 |
| `nano-banana-pro` | = | prompt, aspect_ratio, resolution | AR: 1:1 3:4 4:3 9:16 16:9 3:2 2:3 5:4; res: 1k 2k 4k |
| `kling-o1-text-to-image` | = | prompt, aspect_ratio, resolution, num_images | AR: 16:9 9:16 1:1 4:3 3:4 2:3 3:2 21:9; res: 1k 2k |
| `z-image-turbo` | = | prompt, width, height |  |
| `flux-2-dev` | = | prompt, width, height |  |
| `flux-2-flex` | = | prompt, aspect_ratio, resolution | AR: 16:9 9:16 1:1 4:3 3:4 2:3 3:2; res: 1k 2k |
| `flux-2-pro` | = | prompt, aspect_ratio, resolution | AR: 16:9 9:16 1:1 4:3 3:4 2:3 3:2; res: 1k 2k |
| `vidu-q2-text-to-image` | = | prompt, aspect_ratio, resolution | AR: 16:9 9:16 1:1 4:3 3:4 2:3 3:2 21:9; res: 1k 2k 4k |
| `bytedance-seedream-v4.5` | = | prompt, aspect_ratio, quality | AR: 1:1 16:9 9:16 4:3 3:4 2:3 3:2 21:9 |
| `gpt-image-1.5` | = | prompt, aspect_ratio, quality | AR: 1:1 2:3 3:2 |
| `wan2.6-text-to-image` | = | prompt, width, height |  |
| `qwen-text-to-image-2512` | = | prompt, width, height |  |
| `flux-2-klein-4b` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 3:4 4:3 21:9 9:21 |
| `flux-2-klein-9b` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 3:4 4:3 21:9 9:21 |
| `z-image-base` | = | prompt, image_url, aspect_ratio, strength | AR: 16:9 9:16 1:1 3:4 4:3 21:9 9:21 |
| `nano-banana-2` | = | prompt, aspect_ratio, resolution, google_search, output_format | AR: 1:1 1:4 1:8 2:3 3:2 3:4 4:1 4:3; res: 1k 2k 4k |
| `seedream-5.0` | = | prompt, aspect_ratio, quality | AR: 1:1 16:9 9:16 4:3 3:4 2:3 3:2 21:9 |

## Imagem → imagem (57)

| id | endpoint | campos | proporções / resolução / duração |
|---|---|---|---|
| `ai-image-upscaler` | ai-image-upscale |  |  |
| `ai-image-face-swap` | = | target_index |  |
| `ai-dress-change` | = |  |  |
| `ai-background-remover` | = |  |  |
| `ai-product-shot` | = | scene_description |  |
| `ai-skin-enhancer` | = |  |  |
| `ai-color-photo` | = |  |  |
| `flux-kontext-dev-i2i` | = | prompt, aspect_ratio, num_images | AR: 16:9 9:16 1:1 4:3 3:4 3:2 2:3 21:9; até 10 refs |
| `ai-product-photography` | = | prompt |  |
| `ai-ghibli-style` | = |  |  |
| `ai-image-extension` | = |  |  |
| `ai-object-eraser` | = |  |  |
| `flux-kontext-pro-i2i` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 4:3 3:4 21:9 16:21; até 2 refs |
| `flux-kontext-max-i2i` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 4:3 3:4 21:9 16:21; até 2 refs |
| `gpt4o-image-to-image` | = | prompt, aspect_ratio, num_images | AR: 1:1 2:3 3:2; até 5 refs |
| `gpt4o-edit` | = | prompt, aspect_ratio, num_images | AR: 1:1 2:3 3:2 |
| `midjourney-v7-image-to-image` | = | prompt, speed, aspect_ratio, variety, stylization, weirdness | AR: 1:1 16:9 9:16 3:4 4:3 1:2 2:1 2:3 |
| `bytedance-seededit-v3` | bytedance-seededit-image | prompt |  |
| `midjourney-v7-style-reference` | = | prompt, speed, aspect_ratio, variety, stylization, weirdness | AR: 1:1 16:9 9:16 3:4 4:3 1:2 2:1 2:3 |
| `midjourney-v7-omni-reference` | = | prompt, speed, aspect_ratio, weight, variety, stylization | AR: 1:1 16:9 9:16 3:4 4:3 1:2 2:1 2:3 |
| `minimax-image-01-subject-reference` | minimax-01-subject-reference | prompt, aspect_ratio, num_images | AR: 16:9 9:16 1:1 4:3 3:4 3:2 2:3 21:9 |
| `ideogram-character` | = | prompt, render_speed, style, aspect_ratio, num_images | AR: 16:9 9:16 1:1 4:3 3:4 |
| `flux-pulid` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 4:3 3:4 |
| `qwen-image-edit` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 4:3 3:4 21:9 9:21 3:2 |
| `image-effects` | = | name |  |
| `nano-banana-edit` | = | prompt, aspect_ratio | AR: Auto 1:1 3:4 4:3 9:16 16:9 3:2 2:3; até 10 refs |
| `ideogram-v3-reframe` | = | aspect_ratio, render_speed, style, num_images | AR: 16:9 9:16 1:1 4:3 3:4 |
| `bytedance-seedream-edit-v4` | = | prompt, aspect_ratio, resolution, num_images | AR: 1:1 16:9 9:16 3:4 4:3 2:3 3:2 21:9; res: 1K 2K 4K; até 10 refs |
| `nano-banana-effects` | = | name, aspect_ratio | AR: Auto 1:1 3:4 4:3 9:16 16:9 3:2 2:3 |
| `flux-kontext-effects` | = | prompt, name |  |
| `flux-redux` | = | prompt, aspect_ratio, num_images | AR: 16:9 9:16 1:1 4:3 3:4 3:2 2:3 21:9 |
| `qwen-image-edit-plus` | = | prompt, width, height | até 3 refs |
| `wan2.5-image-edit` | = | prompt, width, height | até 2 refs |
| `higgsfield-soul-image-to-image` | = | prompt, style, aspect_ratio, strength, quality | AR: 16:9 9:16 1:1 4:3 3:4 4:5 5:4 21:9 |
| `reve-image-edit` | = | prompt |  |
| `topaz-image-upscale` | = | upscale_factor |  |
| `seedvr2-image-upscale` | = | resolution | res: 2k 4k 8k |
| `qwen-image-edit-plus-lora` | = | rotate_right_left, move_forward, vertical_angle, wide_angle_lens, width, height | até 3 refs |
| `nano-banana-pro-edit` | = | prompt, aspect_ratio, resolution | AR: 1:1 3:4 4:3 9:16 16:9 3:2 2:3 5:4; res: 1k 2k 4k; até 8 refs |
| `image-passthrough` | = | make_input |  |
| `kling-o1-edit-image` | = | prompt, aspect_ratio, resolution | AR: auto 16:9 9:16 1:1 4:3 3:4 2:3 3:2; res: 1k 2k; até 10 refs |
| `flux-2-dev-edit` | = | prompt, width, height | até 3 refs |
| `flux-2-flex-edit` | = | prompt, aspect_ratio, resolution | AR: auto 16:9 9:16 1:1 4:3 3:4 2:3 3:2; res: 1k 2k; até 8 refs |
| `flux-2-pro-edit` | = | prompt, aspect_ratio, resolution | AR: auto 16:9 9:16 1:1 4:3 3:4 2:3 3:2; res: 1k 2k; até 8 refs |
| `vidu-q2-reference-to-image` | = | prompt, aspect_ratio, resolution | AR: auto 16:9 9:16 1:1 4:3 3:4 2:3 3:2; res: 1k 2k 4k; até 7 refs |
| `bytedance-seedream-v4.5-edit` | = | prompt, aspect_ratio, quality | AR: 1:1 16:9 9:16 4:3 3:4 2:3 3:2 21:9; até 10 refs |
| `qwen-image-edit-2511` | = | prompt, width, height | até 3 refs |
| `wan2.6-image-edit` | = | prompt | até 3 refs |
| `qwen-text-to-image-2512` | = | prompt, width, height |  |
| `gpt-image-1.5-edit` | = | prompt, aspect_ratio, quality | AR: 1:1 2:3 3:2; até 10 refs |
| `grok-imagine-image-to-image` | = | prompt |  |
| `Api Node` | = | model_url, api_key |  |
| `flux-2-klein-4b-edit` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 3:4 4:3 21:9 9:21; até 4 refs |
| `flux-2-klein-9b-edit` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 3:4 4:3 21:9 9:21; até 4 refs |
| `add-image-watermark` | = | position, opacity, scale |  |
| `nano-banana-2-edit` | = | prompt, aspect_ratio, resolution, google_search, output_format | AR: 1:1 1:4 1:8 2:3 3:2 3:4 4:1 4:3; res: 1k 2k 4k; até 14 refs |
| `seedream-5.0-edit` | = | prompt, aspect_ratio, quality | AR: 1:1 16:9 9:16 4:3 3:4 2:3 3:2 21:9 |

## Texto → vídeo (42)

| id | endpoint | campos | proporções / resolução / duração |
|---|---|---|---|
| `seedance-lite-t2v` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16 1:1 4:3 3:4 21:9 9:21; res: 480p 720p 1080p |
| `seedance-pro-t2v` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16 1:1 4:3 3:4 21:9 9:21; res: 480p 720p 1080p |
| `seedance-pro-t2v-fast` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16 1:1 4:3 3:4 21:9; res: 480p 720p 1080p |
| `seedance-v1.5-pro-t2v` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16 1:1 3:4 4:3 21:9; res: 480p 720p 1080p |
| `seedance-v1.5-pro-t2v-fast` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16 1:1 3:4 4:3 21:9; res: 720p 1080p |
| `seedance-v2.0-t2v` | = | prompt, aspect_ratio, duration, quality | AR: 16:9 9:16 4:3 3:4; dur: 5 10 15 |
| `seedance-v2.0-extend` | = | request_id, prompt, duration, quality | dur: 5 10 15 |
| `kling-v2.1-master-t2v` | = | prompt, aspect_ratio, duration | AR: 16:9 9:16 1:1 |
| `kling-v2.5-turbo-pro-t2v` | = | prompt, aspect_ratio, duration | AR: 16:9 9:16 1:1 |
| `kling-v2.6-pro-t2v` | = | prompt, aspect_ratio, duration | AR: 16:9 9:16 1:1; dur: 5 10 |
| `kling-o1-text-to-video` | = | prompt, aspect_ratio, duration | AR: 16:9 9:16 1:1; dur: 5 10 |
| `kling-v3.0-pro-text-to-video` | = | prompt, aspect_ratio, duration | AR: 16:9 9:16 1:1 |
| `kling-v3.0-standard-text-to-video` | = | prompt, aspect_ratio, duration | AR: 16:9 9:16 1:1 |
| `veo3-text-to-video` | = | prompt, aspect_ratio | AR: 16:9 9:16 |
| `veo3-fast-text-to-video` | = | prompt, aspect_ratio | AR: 16:9 9:16 |
| `veo3.1-text-to-video` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16; res: 1080p; dur: 8 |
| `veo3.1-fast-text-to-video` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16; res: 1080p; dur: 8 |
| `runway-text-to-video` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16 1:1 4:3 3:4; res: 720p 1080p; dur: 5 8 |
| `wan2.1-text-to-video` | = | prompt, aspect_ratio, duration, resolution, quality | AR: 16:9 9:16; res: 480p 720p |
| `wan2.2-text-to-video` | = | prompt, aspect_ratio, duration, resolution, quality | AR: 16:9 9:16; res: 480p 720p |
| `wan2.2-5b-fast-t2v` | = | prompt, aspect_ratio, resolution | AR: 16:9 9:16 1:1; res: 480p 580p 720p |
| `wan2.5-text-to-video` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16; res: 480p 720p 1080p |
| `wan2.5-text-to-video-fast` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16; res: 720p 1080p |
| `wan2.6-text-to-video` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16; res: 720p 1080p; dur: 5 10 15 |
| `hunyuan-text-to-video` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 |
| `hunyuan-fast-text-to-video` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 |
| `pixverse-v4.5-t2v` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16 1:1 4:3 3:4; res: 360p 540p 720p 1080p |
| `pixverse-v5-t2v` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16 1:1 4:3 3:4; res: 360p 540p 720p 1080p |
| `pixverse-v5.5-t2v` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16 1:1 4:3 3:4; res: 360p 540p 720p 1080p; dur: 5 8 10 |
| `minimax-hailuo-02-standard-t2v` | = | prompt, duration, resolution | res: 768P; dur: 6 10 |
| `minimax-hailuo-02-pro-t2v` | = | prompt, duration, resolution | res: 1080P; dur: 6 |
| `minimax-hailuo-2.3-pro-t2v` | = | prompt, resolution | res: 1080p |
| `minimax-hailuo-2.3-standard-t2v` | = | prompt, duration | dur: 6 10 |
| `openai-sora` | = | prompt, aspect_ratio, resolution | AR: 16:9 9:16 1:1; res: 480p 720p 1080p |
| `openai-sora-2-text-to-video` | = | prompt, aspect_ratio, duration | AR: 16:9 9:16; dur: 10 15 |
| `openai-sora-2-pro-text-to-video` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16; res: 720p 1080p; dur: 10 15 25 |
| `vidu-v2.0-t2v` | = | prompt, aspect_ratio, duration, resolution | AR: 9:16; res: 1080p; dur: 4 |
| `ovi-text-to-video` | = | prompt, aspect_ratio | AR: 16:9 9:16 |
| `grok-imagine-text-to-video` | = | prompt, aspect_ratio, mode, duration | AR: 9:16 16:9 2:3 3:2 1:1; dur: 6 10 15 |
| `ltx-2-pro-text-to-video` | = | prompt, duration | dur: 6 8 10 |
| `ltx-2-fast-text-to-video` | = | prompt, duration | dur: 6 8 10 12 14 16 18 20 |
| `ltx-2-19b-text-to-video` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16; res: 480p 720p 1080p |

## Imagem → vídeo (61)

| id | endpoint | campos | proporções / resolução / duração |
|---|---|---|---|
| `ai-video-effects` | generate_wan_ai_effects | prompt, name, aspect_ratio, resolution, quality, duration | AR: 16:9 9:16 1:1; res: 480p 720p; dur: 5 10 |
| `motion-controls` | generate_wan_ai_effects | prompt, name, aspect_ratio, resolution, quality, duration | AR: 16:9 9:16 1:1; res: 480p 720p; dur: 5 10 |
| `vfx` | generate_wan_ai_effects | prompt, name, aspect_ratio, resolution, quality, duration | AR: 16:9 9:16 1:1; res: 480p 720p; dur: 5 10 |
| `veo3-image-to-video` | = | prompt, aspect_ratio | AR: 16:9 9:16 |
| `veo3-fast-image-to-video` | = | prompt, aspect_ratio | AR: 16:9 9:16 |
| `runway-image-to-video` | = | prompt, aspect_ratio, resolution, duration | AR: 16:9 9:16 1:1 4:3 3:4; res: 720p 1080p; dur: 5 8 |
| `wan2.1-image-to-video` | = | prompt, aspect_ratio, resolution, quality, duration | AR: 16:9 9:16; res: 480p 720p |
| `midjourney-v7-image-to-video` | = | prompt, aspect_ratio, resolution, num_videos, variety, stylization | AR: 1:1 16:9 9:16 3:4 4:3 1:2 2:1 2:3; res: 480p 1080p |
| `hunyuan-image-to-video` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 |
| `kling-v2.1-master-i2v` | = | prompt, aspect_ratio, duration | AR: 16:9 9:16 1:1 |
| `kling-v2.1-standard-i2v` | = | prompt, aspect_ratio, duration | AR: 16:9 9:16 1:1 |
| `kling-v2.1-pro-i2v` | = | prompt, aspect_ratio, duration | AR: 16:9 9:16 1:1 |
| `wan2.2-image-to-video` | = | prompt, aspect_ratio, resolution, quality, duration | AR: 16:9 9:16; res: 480p 720p |
| `runway-act-two-i2v` | = | aspect_ratio | AR: 16:9 9:16 1:1 4:3 3:4 21:9 |
| `pixverse-v4.5-i2v` | = | prompt, aspect_ratio, resolution, duration | AR: 16:9 9:16 1:1 4:3 3:4; res: 360p 540p 720p 1080p |
| `vidu-v2.0-i2v` | = | prompt, aspect_ratio, resolution, duration | AR: 16:9 1:1; res: 360p 720p 1080p; dur: 4 |
| `vidu-q1-reference` | = | prompt, aspect_ratio | AR: 16:9 9:16 1:1 |
| `minimax-hailuo-02-standard-i2v` | = | prompt, duration, resolution | res: 512P 768P; dur: 6 10 |
| `minimax-hailuo-02-pro-i2v` | = | prompt, duration, resolution | res: 1080p; dur: 6 |
| `video-effects` | = | name |  |
| `seedance-lite-i2v` | = | prompt, resolution, duration, camera_fixed | res: 480p 720p 1080p |
| `seedance-pro-i2v` | = | prompt, resolution, duration, camera_fixed | res: 480p 720p 1080p |
| `pixverse-v5-i2v` | = | prompt, aspect_ratio, resolution, duration | AR: 16:9 9:16 1:1 4:3 3:4; res: 360p 540p 720p 1080p |
| `seedance-lite-reference-video` | seedance-lite-reference-to-video | prompt, resolution, duration | res: 480p 720p |
| `wan2.1-reference-video` | = | prompt, resolution, aspect_ratio, duration | AR: 16:9 9:16; res: 480p 720p |
| `kling-v2.5-turbo-pro-i2v` | = | prompt, duration |  |
| `wan2.5-image-to-video` | = | prompt, resolution, duration | res: 480p 720p 1080p |
| `wan2.5-image-to-video-fast` | = | prompt, resolution, duration | res: 720p 1080p |
| `openai-sora-2-image-to-video` | = | prompt, aspect_ratio, duration, remove_watermark | AR: 16:9 9:16; dur: 10 15 |
| `ovi-image-to-video` | = | prompt |  |
| `openai-sora-2-pro-image-to-video` | = | prompt, aspect_ratio, duration, resolution, remove_watermark | AR: 16:9 9:16; res: 720p 1080p; dur: 10 15 25 |
| `leonardoai-motion-2.0` | = | prompt, aspect_ratio | AR: 16:9 9:16 |
| `higgsfield-dop-image-to-video` | = | prompt, motion, strength, options |  |
| `veo3.1-image-to-video` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16; res: 1080p; dur: 8 |
| `veo3.1-fast-image-to-video` | = | prompt, aspect_ratio, duration, resolution | AR: 16:9 9:16; res: 1080p; dur: 8 |
| `veo3.1-reference-to-video` | = | prompt, resolution, duration, generate_audio | res: 720p 1080p; dur: 8 |
| `seedance-pro-i2v-fast` | = | prompt, resolution, duration, camera_fixed | res: 480p 720p 1080p |
| `ltx-2-pro-image-to-video` | = | prompt, duration, generate_audio | dur: 6 8 10 |
| `ltx-2-fast-image-to-video` | = | prompt, duration, generate_audio | dur: 6 8 10 12 14 16 18 20 |
| `vidu-q2-reference` | = | prompt, resolution, aspect_ratio, duration, movement_amplitude | AR: 16:9 9:16 4:3 3:4 1:1; res: 360p 540p 720p 1080p |
| `vidu-q2-turbo-start-end-video` | = | prompt, resolution, duration, bgm, movement_amplitude | res: 720p 1080p |
| `vidu-q2-pro-start-end-video` | = | prompt, resolution, duration, bgm, movement_amplitude | res: 720p 1080p |
| `minimax-hailuo-2.3-pro-i2v` | = | prompt, resolution | res: 1080p |
| `minimax-hailuo-2.3-standard-i2v` | = | prompt, duration | dur: 6 10 |
| `minimax-hailuo-2.3-fast` | = | prompt, duration, go_fast | dur: 6 10 |
| `kling-v2.5-turbo-std-i2v` | = | prompt, duration |  |
| `grok-imagine-image-to-video` | = | prompt, mode, duration | dur: 6 10 15 |
| `kling-o1-image-to-video` | = | prompt, aspect_ratio, duration | AR: 16:9 9:16 1:1; dur: 5 10 |
| `kling-o1-reference-to-video` | = | prompt, aspect_ratio, duration, keep_original_sound | AR: 16:9 9:16 1:1 |
| `kling-v2.6-pro-i2v` | = | prompt, duration, sound | dur: 5 10 |
| `pixverse-v5.5-i2v` | = | prompt, style, thinking, aspect_ratio, resolution, duration | AR: 16:9 9:16 1:1 4:3 3:4; res: 360p 540p 720p 1080p; dur: 5 8 10 |
| `wan2.2-spicy-image-to-video` | = | prompt, resolution, duration | res: 480p 720p; dur: 5 8 |
| `wan2.6-image-to-video` | = | prompt, resolution, duration, shot_type | res: 720p 1080p; dur: 5 10 15 |
| `kling-o1-standard-image-to-video` | = | prompt, duration | dur: 5 10 |
| `kling-o1-standard-reference-to-video` | = | prompt, aspect_ratio, duration | AR: 16:9 9:16 1:1; dur: 5 10 |
| `seedance-v1.5-pro-i2v` | = | prompt, aspect_ratio, resolution, duration, generate_audio, camera_fixed | AR: 16:9 9:16 1:1 3:4 4:3 21:9; res: 480p 720p 1080p |
| `seedance-v1.5-pro-i2v-fast` | = | prompt, aspect_ratio, resolution, duration, generate_audio, camera_fixed | AR: 16:9 9:16 1:1 3:4 4:3 21:9; res: 720p 1080p |
| `ltx-2-19b-image-to-video` | = | prompt, resolution, duration | res: 480p 720p 1080p |
| `kling-v3.0-pro-image-to-video` | = | prompt, duration, generate_audio |  |
| `kling-v3.0-standard-image-to-video` | = | prompt, duration, generate_audio |  |
| `seedance-v2.0-i2v` | = | prompt, aspect_ratio, duration, quality | AR: 16:9 9:16 4:3 3:4; dur: 5 10 15 |

## Lip sync (9)

| id | endpoint | campos | proporções / resolução / duração |
|---|---|---|---|
| `infinitetalk-image-to-video` | = | resolution | res: 480p 720p |
| `wan2.2-speech-to-video` | = | resolution | res: 480p 720p |
| `ltx-2.3-lipsync` | = | resolution | res: 480p 720p 1080p |
| `ltx-2-19b-lipsync` | = | resolution | res: 480p 720p 1080p |
| `sync-lipsync` | = |  |  |
| `latent-sync` | latentsync-video |  |  |
| `creatify-lipsync` | = |  |  |
| `veed-lipsync` | = |  |  |
| `infinitetalk-video-to-video` | = | resolution | res: 480p 720p |

## Vídeo → vídeo (1)

| id | endpoint | campos | proporções / resolução / duração |
|---|---|---|---|
| `video-watermark-remover` | = |  |  |
