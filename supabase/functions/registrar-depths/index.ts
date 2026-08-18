import { createClient } from "npm:@supabase/supabase-js@2";

// Registra em feed_visita_depth os mapas de profundidade produzidos pela
// fábrica. Token-gated — mesmo esquema das demais funções internas.
// Body: JSON array de {url, codigo_vista, hash}.

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("use POST", { status: 405 });

  const admin = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  const { data: cred } = await admin.from("integracao_credenciais")
    .select("valor").eq("chave", "auditoria_interna_token").maybeSingle();
  const segredo = (cred as { valor?: string } | null)?.valor;
  if (!segredo || req.headers.get("x-auditoria-token") !== segredo) {
    return new Response("nao autorizado", { status: 401 });
  }

  let linhas: { url: string; codigo_vista: string; hash: string }[];
  try { linhas = await req.json(); } catch (_e) { return new Response("json invalido", { status: 400 }); }
  if (!Array.isArray(linhas) || linhas.length === 0 || linhas.length > 2000) {
    return new Response("esperado array de 1 a 2000 itens", { status: 400 });
  }
  for (const l of linhas) {
    if (typeof l?.url !== "string" || !/^[0-9a-f]{8}$/.test(l?.hash ?? "")) {
      return new Response("item invalido", { status: 400 });
    }
  }

  const { error } = await admin.from("feed_visita_depth")
    .upsert(linhas, { onConflict: "url" });
  if (error) return Response.json({ ok: false, erro: error.message }, { status: 500 });

  return Response.json({ ok: true, registradas: linhas.length });
});
