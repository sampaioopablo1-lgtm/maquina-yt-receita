import { createClient } from "npm:@supabase/supabase-js@2";

// Registra em feed_foto_convertida os pares URL original → URL JPEG que a
// máquina de conversão produziu. Token-gated: pg_cron/runner/sandbox não
// emitem JWT; o segredo interno de integracao_credenciais autoriza.
// Body: JSON array de {url_original, codigo_vista, url_jpeg}.

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

  let linhas: { url_original: string; codigo_vista: string; url_jpeg: string }[];
  try { linhas = await req.json(); } catch (_e) { return new Response("json invalido", { status: 400 }); }
  if (!Array.isArray(linhas) || linhas.length === 0 || linhas.length > 2000) {
    return new Response("esperado array de 1 a 2000 itens", { status: 400 });
  }
  for (const l of linhas) {
    if (typeof l?.url_original !== "string" || typeof l?.url_jpeg !== "string" ||
        !l.url_jpeg.startsWith(`${Deno.env.get("SUPABASE_URL")}/storage/v1/object/public/fotos-portal/`)) {
      return new Response("item invalido", { status: 400 });
    }
  }

  const { error } = await admin.from("feed_foto_convertida")
    .upsert(linhas, { onConflict: "url_original" });
  if (error) return Response.json({ ok: false, erro: error.message }, { status: 500 });

  return Response.json({ ok: true, registradas: linhas.length });
});
