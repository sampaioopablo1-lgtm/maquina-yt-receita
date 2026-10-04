# maquina-yt-receita — guia para o Claude

Máquina de produção e publicação de vídeos para 13 canais do YouTube. Leia
nesta ordem antes de agir: `PLAYBOOK.md` (como a máquina opera), `ROTINA.md`
(o prompt do disparo horário), `APRENDIZADOS.md` (o que já quebrou e por quê).

## Regras curtas

- Supabase da máquina: projeto `vevocauwtarctfwngrch`. Nunca gravar vídeo em
  `cscczluzpblzhvojxanp` (é o CRM).
- Publicar só pela Upload-Post; nunca pela Composio `YOUTUBE_UPLOAD_VIDEO`;
  nunca `unlisted`/`private`; `tagbudget.py` antes de toda tag.
- Nunca criar triggers novos. Mudou o trigger horário → muda `ROTINA.md` no
  mesmo commit.
- Testes: `MAQ_LLM_PROVIDER=stub MAQ_TTS_PROVIDER=stub MAQ_IMAGE_PROVIDER=stub .venv/bin/pytest -q`.

## Artes, imagens e vídeos com IA

Use o skill **`higgsfield-artes`** (`.claude/skills/higgsfield-artes/SKILL.md`)
sempre que o pedido envolver criar ou melhorar conteúdo visual. Resumo:

- Open Higgsfield AI está vendido em `ferramentas/open-higgsfield-ai/` (estúdio
  web sobre a Muapi.ai, 221 modelos — catálogo em `config/muapi_modelos.json`).
- Fábrica: cena `layout: "arte"` + `arte_prompt` → `fabrica/arte.py` gera a
  imagem (etapa 1.6 do `etapas.py`) atrás do cartão. Sem chave, cai no fallback.
- Pipeline: `MAQ_IMAGE_PROVIDER=muapi` (`src/maquina/providers/muapi.py`).
- Chave: `MUAPI_API_KEY` ou `config.muapi_api_key` no banco. Guia:
  `docs/23-open-higgsfield-muapi.md`.
- MCP Higgsfield no chat (`mcp__Higgs_field__*`) para peças únicas e para o
  skill `vox-motion-graphics`.
