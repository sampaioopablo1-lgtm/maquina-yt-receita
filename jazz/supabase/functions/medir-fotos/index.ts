import { createClient } from "npm:@supabase/supabase-js@2";

// Mede a resolução real de cada foto publicada e grava em feed_foto_dimensao.
//
// Por que medir em vez de confiar na contagem: o relatório do portal cobra
// Imagens em 86%, e só metade disso é falta de foto. A outra metade é foto
// pequena — a amostra de 147 arquivos achou 65% abaixo do recomendado de
// 1024x768, coisa que contagem nenhuma revela. Sem esta medição, a lista de
// recaptura manda o captador ao imóvel errado.
//
// Lê só os primeiros 32KB de cada arquivo (HTTP Range) e procura o marcador
// SOF do JPEG, que carrega largura e altura. Não baixa a imagem inteira: são
// 94.856 fotos, e baixar tudo seria dezenas de GB de tráfego para obter dois
// números por arquivo.
//
// verify_jwt desligado porque quem chama é o pg_cron pelo pg_net, que não
// emite JWT. A autorização é o token próprio guardado em
// integracao_credenciais — o valor nunca entra no repositório.

async function dimensoes(url: string): Promise<{ w: number; h: number } | null> {
  const res = await fetch(url, { headers: { Range: "bytes=0-32767" }, signal: AbortSignal.timeout(15000) });
  if (!res.ok && res.status !== 206) throw new Error(`HTTP ${res.status}`);
  const buf = new Uint8Array(await res.arrayBuffer());
  if (buf[0] !== 0xff || buf[1] !== 0xd8) return null; // PNG/WebP: fora do escopo
  let i = 2;
  while (i < buf.length - 9) {
    if (buf[i] !== 0xff) { i++; continue; }
    const m = buf[i + 1];
    const ehSOF = m >= 0xc0 && m <= 0xcf && m !== 0xc4 && m !== 0xc8 && m !== 0xcc;
    if (ehSOF) {
      const h = (buf[i + 5] << 8) | buf[i + 6];
      const w = (buf[i + 7] << 8) | buf[i + 8];
      return w > 0 && h > 0 ? { w, h } : null;
    }
    const tam = (buf[i + 2] << 8) | buf[i + 3];
    if (tam <= 0) return null;
    i += 2 + tam;
  }
  return null;
}

Deno.serve(async (req) => {
  const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

  const { data: cred } = await admin.from("integracao_credenciais")
    .select("valor").eq("chave", "auditoria_interna_token").maybeSingle();
  const segredo = (cred as { valor?: string } | null)?.valor;
  if (!segredo || req.headers.get("x-auditoria-token") !== segredo) {
    return new Response("nao autorizado", { status: 401 });
  }

  let lote = 300;
  try {
    const b = await req.json();
    const n = Number(b?.lote);
    if (Number.isFinite(n) && n > 0) lote = Math.min(1000, Math.floor(n));
  } catch (_e) { /* padrão */ }

  const { data } = await admin.rpc("fn_fotos_a_medir", { p_n: lote });
  const fila = (data ?? []) as { codigo: string; url: string }[];
  if (fila.length === 0) return Response.json({ ok: true, restantes: 0, medidas: 0 });

  const linhas: Record<string, unknown>[] = [];
  for (let i = 0; i < fila.length; i += 15) {
    const bloco = fila.slice(i, i + 15);
    const r = await Promise.all(bloco.map(async (f) => {
      try {
        const d = await dimensoes(f.url);
        return { url: f.url, codigo_vista: f.codigo, largura: d?.w ?? null, altura: d?.h ?? null,
                 erro: d ? null : "formato nao jpeg" };
      } catch (e) {
        return { url: f.url, codigo_vista: f.codigo, largura: null, altura: null,
                 erro: (e instanceof Error ? e.message : String(e)).slice(0, 200) };
      }
    }));
    linhas.push(...r);
  }

  // upsert por url: reprocessar um lote nunca duplica linha
  const { error } = await admin.from("feed_foto_dimensao").upsert(linhas, { onConflict: "url" });
  if (error) return Response.json({ ok: false, erro: error.message }, { status: 500 });

  const pequenas = linhas.filter((l) => typeof l.largura === "number" &&
    ((l.largura as number) < 1024 || (l.altura as number) < 768)).length;

  return Response.json({ ok: true, medidas: linhas.length, abaixo_1024x768: pequenas });
});
