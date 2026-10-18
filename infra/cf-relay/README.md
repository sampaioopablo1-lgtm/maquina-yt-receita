# Relé Meta Ads no Cloudflare Workers (gratuito)

Worker que repassa o protocolo MCP para o servidor oficial da Meta
(`https://mcp.facebook.com/ads`) com o token do usuário do sistema. Mesmo relé do
`infra/meta-ads-mcp` v9; Supabase e Netlify estão sem cota, o Cloudflare não.

## Como ligar (uma vez, no PC)

1. dash.cloudflare.com → **Workers & Pages** → **Create** → aba **Workers** →
   **Import a repository** → GitHub → `maquina-yt-receita`.
2. Configuração:
   - **Project name:** `opc-meta-ads-relay`
   - **Production branch:** `claude/opc-pablo-reel-ryxld4`
   - **Root directory:** `infra/cf-relay`
   - **Build command:** deixar vazio
   - **Deploy command:** `npx wrangler deploy`
   - **Save and Deploy**.
3. Worker → **Settings → Variables and Secrets → Add**:
   - `META_ACCESS_TOKEN` (tipo **Secret**) — token do usuário do sistema "Integracao"
   - `MCP_SHARED_SECRET` (tipo **Secret**) — senha longa, só letras e números
4. **Deployments → Retry / Redeploy** (para o worker enxergar os segredos).
5. A URL fica `https://opc-meta-ads-relay.<sua-conta>.workers.dev/mcp/<MCP_SHARED_SECRET>`.
   No claude.ai → Conectores → Adicionar conector personalizado → colar → sem login.

Cada push nesta pasta republica sozinho.
