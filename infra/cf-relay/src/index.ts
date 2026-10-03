// Relé MCP para o servidor oficial da Meta (https://mcp.facebook.com/ads), como Cloudflare Worker.
// Recebe do claude.ai, injeta o token do usuário do sistema (segredo META_ACCESS_TOKEN do
// worker), repassa para a Meta e devolve a resposta. O segredo de acesso entra no caminho:
// /mcp/<MCP_SHARED_SECRET>. Sem ele, 404. Nunca devolve 401 ao cliente.

export interface Env {
  META_ACCESS_TOKEN: string;
  MCP_SHARED_SECRET: string;
  META_MAX_DAILY_BUDGET_CENTS?: string;
}

const META_MCP = "https://mcp.facebook.com/ads";

const json = (v: unknown, status = 200) =>
  new Response(JSON.stringify(v), { status, headers: { "Content-Type": "application/json" } });

// Procura orçamento em qualquer profundidade dos argumentos e recusa acima do teto.
function conferirOrcamento(v: unknown, teto: number, trilha = ""): void {
  if (!v || typeof v !== "object") return;
  for (const [k, x] of Object.entries(v as Record<string, unknown>)) {
    if ((k === "daily_budget" || k === "lifetime_budget") && Number(x) > teto) {
      throw new Error(`Orcamento de ${x} centavos em ${trilha}${k} acima do teto de ${teto} deste rele.`);
    }
    conferirOrcamento(x, teto, trilha + k + ".");
  }
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const TOKEN = env.META_ACCESS_TOKEN ?? "";
    const SEGREDO = env.MCP_SHARED_SECRET ?? "";
    const TETO = Number(env.META_MAX_DAILY_BUDGET_CENTS ?? "5000");
    const p = new URL(req.url).pathname;

    if (!SEGREDO || !p.startsWith("/mcp/" + SEGREDO)) return new Response("nao encontrado", { status: 404 });
    if (!TOKEN) return json({ jsonrpc: "2.0", id: null, error: { code: -32000, message: "META_ACCESS_TOKEN nao configurado no worker" } }, 500);

    if (req.method === "GET") return json({ servidor: "rele meta-ads-opc (cloudflare)", destino: META_MCP, teto_orcamento_centavos: TETO });

    let corpoTexto = "";
    if (req.method === "POST") {
      corpoTexto = await req.text();
      try {
        const corpo = JSON.parse(corpoTexto);
        if (corpo?.method === "tools/call") conferirOrcamento(corpo?.params?.arguments, TETO);
      } catch (e) {
        if (e instanceof SyntaxError) return json({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "JSON invalido" } }, 400);
        return json({ jsonrpc: "2.0", id: null, error: { code: -32000, message: String((e as Error).message) } }, 400);
      }
    }

    const cab = new Headers();
    cab.set("Authorization", "Bearer " + TOKEN);
    cab.set("Content-Type", "application/json");
    cab.set("Accept", req.headers.get("accept") ?? "application/json, text/event-stream");
    const sessao = req.headers.get("mcp-session-id");
    if (sessao) cab.set("Mcp-Session-Id", sessao);
    const versao = req.headers.get("mcp-protocol-version");
    if (versao) cab.set("MCP-Protocol-Version", versao);

    const r = await fetch(META_MCP, { method: req.method, headers: cab, body: req.method === "POST" ? corpoTexto : undefined });

    const saida = new Headers();
    saida.set("Content-Type", r.headers.get("content-type") ?? "application/json");
    const sessaoVolta = r.headers.get("mcp-session-id");
    if (sessaoVolta) saida.set("Mcp-Session-Id", sessaoVolta);
    // 401 da Meta = token vencido. Devolvo 500 para o cliente não tentar login.
    return new Response(r.body, { status: r.status === 401 ? 500 : r.status, headers: saida });
  },
};
