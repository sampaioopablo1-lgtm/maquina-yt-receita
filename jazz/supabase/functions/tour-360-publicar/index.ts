import { createClient } from "npm:@supabase/supabase-js@2";

// Publica tours virtuais 360 REAIS no VirtualTourEasy e devolve o link que o
// XML dos portais vai emitir.
//
// O que esta função NÃO faz, de propósito: não usa `/api/v1/tours/from-images`
// nem `/from-url` nem `/api/v1/ai/full-tour`. Esses endpoints têm o parâmetro
// `method: outpaint | reimagine` — eles CONVERTEM foto comum em esfera 360
// inventando ~83% dos pixels (uma foto cobre ~60°, a esfera cobre 360°). O
// resultado é um cômodo que não existe no imóvel anunciado. Recusado por ser
// enganoso com o comprador e por risco de derrubada do feed inteiro.
//
// O que ela faz: usa `/api/v1/tours/:uuid/scenes`, que aceita panorama
// equiretangular já pronto e só monta a navegação. O insumo é captura real —
// photosphere de celular, câmera 360, ou vídeo processado por terceiro.
//
// Guarda de integridade: antes de mandar uma imagem como cena 360, a função
// confere a proporção lendo o cabeçalho do JPEG por HTTP Range (mesma técnica
// de `amostrar-dimensoes-fotos`). Panorama equiretangular é 2:1. Se alguém
// subir uma foto comum por engano, ela é recusada aqui em vez de virar um
// "tour" quebrado no portal — a trava existe para que o erro humano não vire
// anúncio enganoso.

const BASE = "https://api.virtualtoureasy.com";
const RAZAO_ALVO = 2.0;
const TOLERANCIA = 0.06; // 2:1 com folga para reamostragem do provedor

type Panorama = { url: string; nome?: string };

// Lê largura/altura do JPEG sem baixar o arquivo inteiro: busca os marcadores
// SOF0..SOF15 no começo do arquivo, via Range.
async function dimensoesJpeg(url: string): Promise<{ w: number; h: number } | null> {
  try {
    const res = await fetch(url, {
      headers: { Range: "bytes=0-32767" },
      signal: AbortSignal.timeout(20000),
    });
    if (!res.ok && res.status !== 206) return null;
    const buf = new Uint8Array(await res.arrayBuffer());
    if (buf[0] !== 0xff || buf[1] !== 0xd8) return null; // não é JPEG

    let i = 2;
    while (i < buf.length - 9) {
      if (buf[i] !== 0xff) { i++; continue; }
      const marcador = buf[i + 1];
      // SOF0-SOF3, SOF5-SOF7, SOF9-SOF11, SOF13-SOF15 carregam as dimensões.
      const ehSOF = (marcador >= 0xc0 && marcador <= 0xcf) &&
        marcador !== 0xc4 && marcador !== 0xc8 && marcador !== 0xcc;
      if (ehSOF) {
        const h = (buf[i + 5] << 8) | buf[i + 6];
        const w = (buf[i + 7] << 8) | buf[i + 8];
        if (w > 0 && h > 0) return { w, h };
        return null;
      }
      const tam = (buf[i + 2] << 8) | buf[i + 3];
      if (tam <= 0) return null;
      i += 2 + tam;
    }
    return null;
  } catch (_e) {
    return null;
  }
}

async function ehPanorama360(url: string): Promise<{ ok: boolean; motivo?: string }> {
  const d = await dimensoesJpeg(url);
  if (!d) return { ok: true, motivo: "dimensoes_ilegiveis" }; // não bloqueia: pode ser PNG/WebP
  const razao = d.w / d.h;
  if (Math.abs(razao - RAZAO_ALVO) > TOLERANCIA) {
    return { ok: false, motivo: `proporcao ${razao.toFixed(2)}:1 (${d.w}x${d.h}) — panorama equiretangular precisa ser 2:1` };
  }
  return { ok: true };
}

Deno.serve(async (req) => {
  const admin = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  let lote = 10;
  try {
    const b = await req.json();
    const n = Number(b?.lote);
    if (Number.isFinite(n) && n > 0) lote = Math.min(50, Math.floor(n));
  } catch (_e) { /* padrão */ }

  const { data: cred } = await admin.from("integracao_credenciais")
    .select("valor").eq("chave", "virtualtoureasy_api_key").maybeSingle();
  const apiKey = (cred as any)?.valor;
  if (!apiKey) {
    return Response.json({
      ok: false,
      motivo: "credencial virtualtoureasy ausente — inserir em integracao_credenciais (chave: virtualtoureasy_api_key)",
    }, { status: 500 });
  }

  const cab = { "Authorization": `Bearer ${apiKey}`, "Content-Type": "application/json" };

  const { data: pendentes } = await admin.from("feed_tour_360")
    .select("codigo_vista, panoramas")
    .eq("status", "pendente")
    .order("criado_em", { ascending: true })
    .limit(lote);

  const fila = (pendentes ?? []) as { codigo_vista: string; panoramas: Panorama[] }[];
  if (fila.length === 0) {
    return Response.json({ ok: true, pendentes: 0, publicados: 0 });
  }

  let publicados = 0, recusados = 0, erros = 0;
  const detalhes: string[] = [];

  for (const item of fila) {
    const panoramas = Array.isArray(item.panoramas) ? item.panoramas : [];
    if (panoramas.length === 0) {
      await admin.from("feed_tour_360").update({
        status: "erro", erro: "sem panoramas cadastrados",
      }).eq("codigo_vista", item.codigo_vista);
      erros++;
      continue;
    }

    try {
      // 1) Conferência de proporção antes de gastar chamada na API.
      const invalidos: string[] = [];
      for (const p of panoramas) {
        const v = await ehPanorama360(p.url);
        if (!v.ok) invalidos.push(`${p.nome ?? p.url}: ${v.motivo}`);
      }
      if (invalidos.length > 0) {
        await admin.from("feed_tour_360").update({
          status: "erro",
          erro: `imagem não é panorama 360 — ${invalidos.slice(0, 3).join(" | ")}`,
        }).eq("codigo_vista", item.codigo_vista);
        recusados++;
        detalhes.push(`${item.codigo_vista}: recusado (${invalidos.length} imagem(ns) fora de 2:1)`);
        continue;
      }

      // 2) Cria o tour vazio.
      const rTour = await fetch(`${BASE}/api/v1/tours`, {
        method: "POST", headers: cab,
        body: JSON.stringify({
          title: `Imóvel ${item.codigo_vista} — Jazz Imobiliária`,
          description: `Tour virtual 360 do imóvel ${item.codigo_vista}.`,
        }),
        signal: AbortSignal.timeout(60000),
      });
      if (!rTour.ok) throw new Error(`criar tour: HTTP ${rTour.status} ${(await rTour.text()).slice(0, 200)}`);
      const jTour = await rTour.json();
      const uuid = jTour?.tour?.uuid;
      if (!uuid) throw new Error("resposta sem tour.uuid");

      // 3) Uma cena por panorama, na ordem cadastrada.
      for (let i = 0; i < panoramas.length; i++) {
        const p = panoramas[i];
        const rCena = await fetch(`${BASE}/api/v1/tours/${uuid}/scenes`, {
          method: "POST", headers: cab,
          body: JSON.stringify({
            name: p.nome ?? `Ambiente ${i + 1}`,
            image_url: p.url,
            type: "equirectangular",
          }),
          signal: AbortSignal.timeout(60000),
        });
        if (!rCena.ok) throw new Error(`cena ${i + 1}: HTTP ${rCena.status} ${(await rCena.text()).slice(0, 200)}`);
      }

      // 4) Publica.
      const rPub = await fetch(`${BASE}/api/v1/tours/${uuid}`, {
        method: "PATCH", headers: cab,
        body: JSON.stringify({ status: "published", visibility: "public" }),
        signal: AbortSignal.timeout(60000),
      });
      if (!rPub.ok) throw new Error(`publicar: HTTP ${rPub.status} ${(await rPub.text()).slice(0, 200)}`);

      // 5) Guarda os links. Preferimos o mls_viewer_url (versão sem marca),
      //    que é o formato que os portais esperam no campo de tour.
      const viewer = jTour?.tour?.viewer_url ?? null;
      const mls = jTour?.tour?.mls_viewer_url ?? viewer;

      await admin.from("feed_tour_360").update({
        vte_tour_uuid: uuid,
        viewer_url: viewer,
        mls_viewer_url: mls,
        status: "publicado",
        erro: null,
        publicado_em: new Date().toISOString(),
      }).eq("codigo_vista", item.codigo_vista);

      publicados++;
      detalhes.push(`${item.codigo_vista}: publicado (${panoramas.length} cenas)`);
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      await admin.from("feed_tour_360").update({
        status: "erro", erro: msg.slice(0, 400),
      }).eq("codigo_vista", item.codigo_vista);
      erros++;
      detalhes.push(`${item.codigo_vista}: ${msg.slice(0, 120)}`);
    }
  }

  // Leva os links publicados para o campo que o gerador de XML já lê.
  const { data: noFeed } = await admin.rpc("fn_tour_360_publicar_no_feed");

  return Response.json({
    ok: erros === 0,
    processados: fila.length,
    publicados, recusados_por_nao_ser_360: recusados, erros,
    levados_ao_feed: noFeed,
    detalhes: detalhes.slice(0, 20),
  });
});
