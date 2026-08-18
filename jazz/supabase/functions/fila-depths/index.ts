import { createClient } from "npm:@supabase/supabase-js@2";

// Fila de fotos sem mapa de profundidade, para a fábrica de visita virtual.
// Existe porque os secrets SUPABASE_* do repositório apontam para o projeto
// da máquina YT, não o da Jazz — o runner acessa o projeto certo por aqui,
// com o token interno (mesmo esquema de fila-conversao/midia-upload).

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

  let lote = 800;
  try {
    const b = await req.json();
    const n = Number(b?.lote);
    if (Number.isFinite(n) && n > 0) lote = Math.min(2000, Math.floor(n));
  } catch (_e) { /* padrão */ }

  const { data, error } = await admin.rpc("fn_fotos_sem_depth", { p_n: lote });
  if (error) return Response.json({ ok: false, erro: error.message }, { status: 500 });
  return Response.json({ ok: true, fila: data ?? [] });
});
