import { createClient } from "npm:@supabase/supabase-js@2";

// Recebe um arquivo de mídia e grava no Storage. Existe porque as máquinas
// que RENDERIZAM (runner do Actions, sandbox de rede aberta) não carregam a
// service key — só esta função, que roda dentro do projeto, tem a credencial.
// Quem chama se identifica com o token interno de auditoria, o mesmo esquema
// de medir-fotos: token em integracao_credenciais, valor fora do repositório.
//
// Só aceita os buckets de mídia dos anúncios, e só mp4/jpg — não é um
// upload genérico. 'visitas' guarda os mapas de profundidade (parallax 2.5D)
// e 'fotos-portal' as fotos convertidas de PNG para JPEG real (o portal só
// importa jpg).

const BUCKETS = new Set(["videos-imoveis", "tours-360", "visitas", "fotos-portal"]);
const TIPOS: Record<string, string> = {
  ".mp4": "video/mp4",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
};
const MAX_BYTES = 200 * 1024 * 1024;

Deno.serve(async (req) => {
  if (req.method !== "POST" && req.method !== "PUT") {
    return new Response("use POST", { status: 405 });
  }

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

  const url = new URL(req.url);
  const bucket = url.searchParams.get("bucket") ?? "";
  const caminho = url.searchParams.get("caminho") ?? "";
  if (!BUCKETS.has(bucket)) return new Response("bucket invalido", { status: 400 });
  if (!/^[A-Za-z0-9_\-\/\.]{1,120}$/.test(caminho) || caminho.includes("..")) {
    return new Response("caminho invalido", { status: 400 });
  }
  const ext = caminho.slice(caminho.lastIndexOf(".")).toLowerCase();
  const tipo = TIPOS[ext];
  if (!tipo) return new Response("so mp4/jpg", { status: 400 });

  const corpo = new Uint8Array(await req.arrayBuffer());
  if (corpo.byteLength === 0) return new Response("corpo vazio", { status: 400 });
  if (corpo.byteLength > MAX_BYTES) return new Response("arquivo grande demais", { status: 413 });

  const { error } = await admin.storage.from(bucket)
    .upload(caminho, corpo, { contentType: tipo, upsert: true });
  if (error) return Response.json({ ok: false, erro: error.message }, { status: 500 });

  return Response.json({
    ok: true,
    bytes: corpo.byteLength,
    url_publica: `${Deno.env.get("SUPABASE_URL")}/storage/v1/object/public/${bucket}/${caminho}`,
  });
});
