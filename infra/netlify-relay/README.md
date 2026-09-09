# Relé Meta Ads no Netlify (gratuito)

Função Netlify que repassa o protocolo MCP para o servidor oficial da Meta
(`https://mcp.facebook.com/ads`) com o token do usuário do sistema. É o `infra/meta-ads-mcp`
v9 portado para o Netlify, porque o Supabase está bloqueado por cota.

## Como ligar (uma vez, pelo celular)

1. app.netlify.com → **Add new project → Import an existing project → GitHub** →
   repositório `maquina-yt-receita`.
2. Branch: `claude/opc-pablo-reel-ryxld4`. **Base directory:** `infra/netlify-relay`.
   Build command e publish directory já vêm do `netlify.toml`. Deploy.
3. Project configuration → **Environment variables** → adicionar:
   - `META_ACCESS_TOKEN` — o token do usuário do sistema "Integracao" (marcar como *secret*)
   - `MCP_SHARED_SECRET` — uma senha longa, só letras e números
   - `META_MAX_DAILY_BUDGET_CENTS` — `5000`
4. Deploys → **Trigger deploy** (para a função enxergar as variáveis).
5. No claude.ai → Conectores → Adicionar conector personalizado →
   URL: `https://<nome-do-site>.netlify.app/mcp/<MCP_SHARED_SECRET>` — sem login.

Cada push nesta branch republica sozinho.
