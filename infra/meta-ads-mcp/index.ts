import "jsr:@supabase/functions-js/edge-runtime.d.ts";

// v9 — relé para o servidor MCP oficial da Meta.
// Recebe do claude.ai, injeta o token do usuário do sistema, repassa para
// https://mcp.facebook.com/ads e devolve a resposta. Nunca responde 401: quem
// tem o segredo no caminho já está autorizado, e assim o cliente não tenta OAuth.

const META_MCP = "https://mcp.facebook.com/ads";
const TOKEN = Deno.env.get("META_ACCESS_TOKEN") ?? "";
const SEGREDO = Deno.env.get("MCP_SHARED_SECRET") ?? "";
const TETO_CENTAVOS = Number(Deno.env.get("META_MAX_DAILY_BUDGET_CENTS") ?? "5000");

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "*",
  "Access-Control-Expose-Headers": "Mcp-Session-Id",
  "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
};

const json = (v: unknown, status = 200) =>
  new Response(JSON.stringify(v), { status, headers: { "Content-Type": "application/json", ...CORS } });

// Procura orçamento em qualquer profundidade dos argumentos e recusa acima do teto.
function conferirOrcamento(v: unknown, trilha = ""): void {
  if (!v || typeof v !== "object") return;
  for (const [k, x] of Object.entries(v as Record<string, unknown>)) {
    if ((k === "daily_budget" || k === "lifetime_budget") && Number(x) > TETO_CENTAVOS) {
      throw new Error(`Orcamento de ${x} centavos em ${trilha}${k} acima do teto de ${TETO_CENTAVOS} deste rele.`);
    }
    conferirOrcamento(x, trilha + k + ".");
  }
}

Deno.serve(async (req: Request) => {
  const url = new URL(req.url);
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
  if (!SEGREDO || !url.pathname.includes(SEGREDO)) return new Response("nao encontrado", { status: 404, headers: CORS });
  if (!TOKEN) return json({ jsonrpc: "2.0", id: null, error: { code: -32000, message: "META_ACCESS_TOKEN nao configurado" } }, 500);

  if (req.method === "GET") {
    return json({ servidor: "rele meta-ads-opc v9", destino: META_MCP, teto_orcamento_centavos: TETO_CENTAVOS });
  }

  let corpoTexto = "";
  if (req.method === "POST") {
    corpoTexto = await req.text();
    try {
      const corpo = JSON.parse(corpoTexto);
      if (corpo?.method === "tools/call") conferirOrcamento(corpo?.params?.arguments);
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

  const r = await fetch(META_MCP, {
    method: req.method,
    headers: cab,
    body: req.method === "POST" ? corpoTexto : undefined,
  });

  const saida = new Headers(CORS);
  saida.set("Content-Type", r.headers.get("content-type") ?? "application/json");
  const sessaoVolta = r.headers.get("mcp-session-id");
  if (sessaoVolta) saida.set("Mcp-Session-Id", sessaoVolta);
  // O 401 da Meta significa token vencido; devolvo como 500 para o cliente não tentar OAuth.
  const status = r.status === 401 ? 500 : r.status;
  return new Response(r.body, { status, headers: saida });
});
