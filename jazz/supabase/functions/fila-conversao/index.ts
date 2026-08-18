import { createClient } from "npm:@supabase/supabase-js@2";

// Fila de fotos PNG (com extensão .jpg) aguardando conversão para JPEG real.
// Quem consome é a máquina de conversão (scripts/converter_fotos_png.py no
// runner do Actions). Token-gated como as demais funções internas — pg_cron e
// runners não emitem JWT, então verify_jwt fica desligado e o segredo
// interno de integracao_credenciais faz a autorização.

Deno.serve(async (req) => {
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

  const { data, error } = await admin
    .from("feed_foto_dimensao")
    .select("codigo_vista, url")
    .eq("erro", "formato nao jpeg")
    .limit(500);
  if (error) return Response.json({ ok: false, erro: error.message }, { status: 500 });

  // só as que ainda não foram convertidas
  const { data: feitas } = await admin.from("feed_foto_convertida").select("url_original");
  const done = new Set((feitas ?? []).map((r: { url_original: string }) => r.url_original));
  const fila = (data ?? []).filter((r: { url: string }) => !done.has(r.url));

  return Response.json({ ok: true, fila });
});
