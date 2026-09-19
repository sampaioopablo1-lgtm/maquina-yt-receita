// Agente de WhatsApp da O Próximo Cliente, como Cloudflare Worker.
// Cloud API oficial da Meta (coexistência com o número atual) -> espera 8 s -> Claude -> resposta.
// Só responde. Nunca inicia conversa. Devolve pro Pablo quando o roteiro manda.
import Anthropic from "@anthropic-ai/sdk";
import { SYSTEM } from "./prompt";

export interface Env {
  KV: KVNamespace;
  META_ACCESS_TOKEN: string;
  WA_PHONE_NUMBER_ID: string;
  WA_VERIFY_TOKEN: string;
  WA_APP_SECRET?: string;
  ANTHROPIC_API_KEY: string;
  CALENDLY_URL: string;
  OWNER_WHATSAPP: string;
  BUFFER_SECONDS: string;
  CLAUDE_MODEL: string;
}

const GRAPH = "https://graph.facebook.com/v22.0";
const MAX_HISTORY = 30;

const TOOLS: Anthropic.Tool[] = [
  {
    name: "agendar_reuniao",
    description: "Gera o link de agendamento do diagnóstico para este contato, já com nome preenchido. Chame só quando a pessoa for o cliente certo e tiver aceitado marcar.",
    input_schema: {
      type: "object",
      properties: {
        nome: { type: "string" },
        empresa: { type: "string" },
        resumo: { type: "string", description: "Uma linha: negócio, bairro, se anuncia, dor principal." },
      },
      required: ["nome", "empresa", "resumo"],
      additionalProperties: false,
    },
    strict: true,
  },
  {
    name: "passar_para_humano",
    description: "Devolve a conversa para o Pablo e para de responder. Use nas situações do roteiro.",
    input_schema: {
      type: "object",
      properties: { motivo: { type: "string" } },
      required: ["motivo"],
      additionalProperties: false,
    },
    strict: true,
  },
];

// ---------- WhatsApp ----------
async function waPost(env: Env, payload: unknown): Promise<void> {
  const r = await fetch(`${GRAPH}/${env.WA_PHONE_NUMBER_ID}/messages`, {
    method: "POST",
    headers: { Authorization: `Bearer ${env.META_ACCESS_TOKEN}`, "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!r.ok) console.log("WA erro", r.status, await r.text());
}
const sendText = (env: Env, to: string, body: string) =>
  waPost(env, { messaging_product: "whatsapp", to, type: "text", text: { preview_url: true, body } });
const readAndTyping = (env: Env, message_id: string) =>
  waPost(env, { messaging_product: "whatsapp", status: "read", message_id, typing_indicator: { type: "text" } });
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function sendSplit(env: Env, to: string, reply: string): Promise<void> {
  for (const p of reply.split("\n\n").map((s) => s.trim()).filter(Boolean)) {
    await sendText(env, to, p);
    await sleep(Math.min(4000, 1000 + p.length * 5));
  }
}

// ---------- memória (KV) ----------
async function getHist(env: Env, user: string): Promise<Anthropic.MessageParam[]> {
  return (await env.KV.get(`hist:${user}`, "json")) ?? [];
}
async function setHist(env: Env, user: string, h: Anthropic.MessageParam[]): Promise<void> {
  while (h.length > MAX_HISTORY) { h.shift(); while (h.length && h[0].role !== "user") h.shift(); }
  await env.KV.put(`hist:${user}`, JSON.stringify(h), { expirationTtl: 60 * 60 * 24 * 30 });
}
async function log(env: Env, tipo: string, user: string, data: Record<string, unknown>): Promise<void> {
  const ts = new Date().toISOString();
  await env.KV.put(`lead:${ts}:${user}`, JSON.stringify({ ts, tipo, whatsapp: user, ...data }));
}

// ---------- Claude ----------
async function reply(env: Env, user: string, text: string): Promise<{ text: string; stop: boolean }> {
  const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
  const h = await getHist(env, user);
  h.push({ role: "user", content: text });
  const out: string[] = [];
  let stop = false;
  for (let i = 0; i < 4; i++) {
    const resp = await client.messages.create({
      model: env.CLAUDE_MODEL || "claude-opus-5",
      max_tokens: 1024,
      system: [{ type: "text", text: SYSTEM, cache_control: { type: "ephemeral" } }],
      tools: TOOLS,
      messages: h,
    });
    h.push({ role: "assistant", content: resp.content });
    for (const b of resp.content) if (b.type === "text") out.push(b.text);
    if (resp.stop_reason !== "tool_use") break;
    const results: Anthropic.ToolResultBlockParam[] = [];
    for (const b of resp.content) {
      if (b.type !== "tool_use") continue;
      const inp = b.input as Record<string, string>;
      let content = "";
      if (b.name === "agendar_reuniao") {
        const link = `${env.CALENDLY_URL}?${new URLSearchParams({ name: inp.nome, a1: user })}`;
        await log(env, "reuniao_oferecida", user, { ...inp, link });
        content = JSON.stringify({ link });
      } else if (b.name === "passar_para_humano") {
        await env.KV.put(`pause:${user}`, "1");
        await log(env, "handoff", user, inp);
        content = JSON.stringify({ ok: true });
        stop = true;
      } else content = JSON.stringify({ erro: "ferramenta desconhecida" });
      results.push({ type: "tool_result", tool_use_id: b.id, content });
    }
    h.push({ role: "user", content: results });
    if (stop) break;
  }
  await setHist(env, user, h);
  return { text: out.map((t) => t.trim()).filter(Boolean).join("\n\n"), stop };
}

// ---------- fila com espera (junta mensagens em sequência) ----------
async function enqueue(env: Env, user: string, text: string, ctx: ExecutionContext): Promise<void> {
  const key = `buf:${user}`;
  const cur = ((await env.KV.get(key, "json")) as { msgs: string[]; v: number } | null) ?? { msgs: [], v: 0 };
  cur.msgs.push(text); cur.v += 1;
  await env.KV.put(key, JSON.stringify(cur), { expirationTtl: 300 });
  const minha = cur.v;
  ctx.waitUntil((async () => {
    await sleep(Number(env.BUFFER_SECONDS || "8") * 1000);
    const agora = (await env.KV.get(key, "json")) as { msgs: string[]; v: number } | null;
    if (!agora || agora.v !== minha) return; // chegou mensagem nova depois de mim: quem processa é ela
    await env.KV.delete(key);
    try {
      const r = await reply(env, user, agora.msgs.join("\n"));
      if (r.text) await sendSplit(env, user, r.text);
      if (r.stop && env.OWNER_WHATSAPP)
        await sendText(env, env.OWNER_WHATSAPP, `Conversa devolvida pra você: wa.me/${user}\nÚltima mensagem: ${agora.msgs.join(" | ").slice(0, 200)}`);
    } catch (e) { console.log("erro", user, String(e)); }
  })());
}

// ---------- assinatura ----------
async function signedOk(req: Request, raw: string, secret?: string): Promise<boolean> {
  if (!secret) return true;
  const sig = (req.headers.get("X-Hub-Signature-256") ?? "").replace("sha256=", "");
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = new Uint8Array(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(raw)));
  const hex = [...mac].map((b) => b.toString(16).padStart(2, "0")).join("");
  return hex === sig;
}

export default {
  async fetch(req: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(req.url);
    if (url.pathname !== "/webhook") return new Response("opc-whatsapp", { status: 200 });

    if (req.method === "GET") {
      if (url.searchParams.get("hub.verify_token") === env.WA_VERIFY_TOKEN)
        return new Response(url.searchParams.get("hub.challenge") ?? "", { status: 200 });
      return new Response("forbidden", { status: 403 });
    }

    const raw = await req.text();
    if (!(await signedOk(req, raw, env.WA_APP_SECRET))) return new Response("forbidden", { status: 403 });
    let body: any = {};
    try { body = JSON.parse(raw); } catch { return new Response("ok", { status: 200 }); }

    for (const entry of body.entry ?? []) for (const ch of entry.changes ?? []) for (const m of ch.value?.messages ?? []) {
      if (m.type !== "text") continue;
      const user: string = m.from;
      if (await env.KV.get(`pause:${user}`)) continue; // devolvido pro Pablo
      ctx.waitUntil(readAndTyping(env, m.id));
      await enqueue(env, user, m.text.body, ctx);
    }
    return new Response("ok", { status: 200 });
  },
};
