import { createClient } from "npm:@supabase/supabase-js@2";

// Tour virtual 360 hospedado por nós, sem fornecedor e sem mensalidade.
//
// Por que existe: o VirtualTourEasy exige plano Professional para liberar a
// API, e o volume aqui é de milhares de anúncios. Como já temos bucket,
// Edge Functions e domínio HTTPS válido, hospedar o tour é de graça e sem
// limite. Usa Pannellum (MIT, 21KB), que tem tour multi-ambiente nativo.
//
// A especificação oficial do portal (developers.grupozap.com) pede que a
// página do <VirtualTourLink> contenha SOMENTE o tour — sem cabeçalho, menu,
// rodapé ou qualquer conteúdo do site. É por isso que esta página não tem
// nada além do visualizador.
//
// IMPORTANTE — o que entra aqui: apenas panorama equiretangular REAL,
// capturado no imóvel (photosphere de celular ou câmera 360). Sequência de
// fotos comuns NÃO é tour: já foi testado em 193 anúncios e o portal pontuou
// 0% na categoria, além de não ser 360 de verdade. A rota antiga `/tour/`
// servia isso; esta é separada de propósito, para o portal avaliar um
// endereço limpo.
//
// Se o imóvel não tiver panorama real cadastrado, responde 404 em vez de
// servir um substituto — link de tour que não abre tour é pior que link
// nenhum.

const PANNELLUM_JS = "https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js";
const PANNELLUM_CSS = "https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css";

type Panorama = { url: string; nome?: string };

const esc = (s: string) =>
  String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));

function paginaTour(titulo: string, panoramas: Panorama[]): string {
  // Uma cena por ambiente. Os hotspots ligam cada cena à seguinte, em
  // círculo, para o visitante percorrer o imóvel inteiro sem sair da página.
  const cenas: Record<string, unknown> = {};
  panoramas.forEach((p, i) => {
    const id = `c${i}`;
    const proximo = `c${(i + 1) % panoramas.length}`;
    cenas[id] = {
      type: "equirectangular",
      panorama: p.url,
      title: p.nome ?? `Ambiente ${i + 1}`,
      autoLoad: true,
      hotSpots: panoramas.length > 1
        ? [{
            pitch: -5, yaw: 0, type: "scene", sceneId: proximo,
            text: panoramas[(i + 1) % panoramas.length].nome ?? "Próximo ambiente",
          }]
        : [],
    };
  });

  const config = {
    default: { firstScene: "c0", sceneFadeDuration: 800, autoLoad: true },
    scenes: cenas,
  };

  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>${esc(titulo)}</title>
<link rel="stylesheet" href="${PANNELLUM_CSS}">
<style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;width:100%;background:#000;overflow:hidden}
#tour{position:fixed;inset:0}
</style>
</head><body>
<div id="tour"></div>
<script src="${PANNELLUM_JS}"></script>
<script>
pannellum.viewer('tour', ${JSON.stringify(config)});
</script>
</body></html>`;
}

Deno.serve(async (req) => {
  const url = new URL(req.url);
  // .../functions/v1/tour360/<codigo>
  const codigo = url.pathname.split("/").filter(Boolean).pop() ?? "";

  if (!codigo || codigo === "tour360") {
    return new Response("codigo do imovel ausente", { status: 400 });
  }

  const admin = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  const { data } = await admin.from("feed_tour_360")
    .select("panoramas, status")
    .eq("codigo_vista", codigo)
    .maybeSingle();

  const panoramas = (data?.panoramas ?? []) as Panorama[];
  if (!Array.isArray(panoramas) || panoramas.length === 0) {
    return new Response("tour 360 nao disponivel para este imovel", { status: 404 });
  }

  const { data: imovel } = await admin.from("vista_imoveis_log")
    .select("categoria, bairro, cidade")
    .eq("codigo_vista", codigo)
    .maybeSingle();

  const titulo = imovel
    ? `${imovel.categoria ?? "Imóvel"} — ${imovel.bairro ?? ""}, ${imovel.cidade ?? ""}`.replace(/ — , /, " — ")
    : `Imóvel ${codigo}`;

  return new Response(paginaTour(titulo, panoramas), {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      // Cache curto: o portal revisita, e trocar um panorama não pode ficar
      // preso em cache por horas.
      "Cache-Control": "public, max-age=600",
    },
  });
});
