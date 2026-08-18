import { createClient } from "npm:@supabase/supabase-js@2";

// Geocodifica o logradouro real dos anúncios sem coordenada, via Nominatim
// (OpenStreetMap). A política de uso pede no máximo 1 consulta por segundo e
// um User-Agent que identifique quem está chamando — os dois são respeitados
// aqui, e é por isso que o lote é pequeno e existe pausa entre as chamadas.
//
// v2 — conferência do nome da via. Passar o CEP melhora muito o acerto, mas
// faz o Nominatim casar pelo CEP e devolver OUTRA rua quando o logradouro não
// existe na base: "Atlantica, Caraguatatuba" voltou como "Avenida Geraldo
// Nogueira da Silva". Coordenada errada é pior que coordenada ausente — o
// comprador filtra por mapa —, então o resultado só vale se o nome da via
// retornada contiver o logradouro que pedimos.

const UA = "JazzImobiliariaFeedGeocoder/1.0 (contato: rafael@imobiliariajazz.com.br)";
const PAUSA_MS = 1200;
const LOTE_PADRAO = 40;
const LOTE_MAX = 120;

const dormir = (ms: number) => new Promise((r) => setTimeout(r, ms));

function limparLogradouro(endereco: string): string {
  // Tira faixa de numeração que o CRM às vezes carrega ("Rua X - de 100 a 200")
  // e número solto no fim, que atrapalham o casamento no OSM.
  return endereco
    .replace(/\s*[-–]?\s*\b(?:de|at[ée]|do\s+km)\s+\d[\d/]*\b.*$/i, "")
    .replace(/,?\s*\d+\s*$/, "")
    .trim();
}

function normalizar(s: string): string {
  return s
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9 ]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

// Tipos de via e ligações não distinguem endereço nenhum: "Rua das Flores" e
// "Flores" são o mesmo logradouro pra quem procura.
const PALAVRAS_VAZIAS = new Set([
  "rua", "r", "avenida", "av", "alameda", "al", "travessa", "tv", "praca", "praco",
  "rodovia", "rod", "estrada", "est", "largo", "viela", "via", "marginal", "passagem",
  "de", "do", "da", "dos", "das", "e", "em", "no", "na",
]);

function nucleo(s: string): string[] {
  return normalizar(s).split(" ").filter((p) => p.length > 2 && !PALAVRAS_VAZIAS.has(p));
}

// A via retornada precisa carregar o miolo do logradouro pedido. Exigimos que
// TODOS os termos significativos apareçam — com um só termo, "Jardim Bela
// Vista" casaria com "Vista Alegre".
function viaConfere(pedido: string, displayName: string): boolean {
  const termos = nucleo(pedido);
  if (termos.length === 0) return false;
  const via = normalizar(String(displayName ?? "").split(",")[0] ?? "");
  if (!via) return false;
  return termos.every((t) => via.includes(t));
}

function montarUrl(c: { endereco: string; cidade: string | null; cep: string | null }): string {
  const u = new URL("https://nominatim.openstreetmap.org/search");
  u.searchParams.set("format", "jsonv2");
  u.searchParams.set("limit", "1");
  u.searchParams.set("countrycodes", "br");
  u.searchParams.set("street", limparLogradouro(c.endereco));
  if (c.cidade) u.searchParams.set("city", c.cidade);
  u.searchParams.set("state", "São Paulo");
  if (c.cep && c.cep.length === 8) u.searchParams.set("postalcode", c.cep);
  return u.toString();
}

Deno.serve(async (req) => {
  const admin = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  let lote = LOTE_PADRAO;
  try {
    const body = await req.json();
    const n = Number(body?.lote);
    if (Number.isFinite(n) && n > 0) lote = Math.min(LOTE_MAX, Math.floor(n));
  } catch (_e) { /* sem corpo: usa o padrão */ }

  const { data: candidatos, error } = await admin.rpc("fn_geocode_candidatos", { p_limite: lote });
  if (error) {
    return Response.json({ ok: false, motivo: `falha ao ler candidatos: ${error.message}` }, { status: 500 });
  }
  if (!candidatos || candidatos.length === 0) {
    return Response.json({ ok: true, candidatos: 0, gravados: 0 });
  }

  let gravados = 0, semResultado = 0, viaDivergente = 0, foraDeSp = 0, erros = 0;

  for (let i = 0; i < candidatos.length; i++) {
    const c = candidatos[i] as any;
    if (i > 0) await dormir(PAUSA_MS);

    try {
      const res = await fetch(montarUrl(c), {
        headers: { "User-Agent": UA, "Accept": "application/json" },
        signal: AbortSignal.timeout(20000),
      });

      if (res.status === 429 || res.status === 503) {
        // Nominatim pedindo calma: para o lote inteiro em vez de insistir.
        console.warn(`[geocode] ${res.status} do Nominatim — encerrando lote em ${i}/${candidatos.length}`);
        break;
      }
      if (!res.ok) {
        erros++;
        await admin.rpc("fn_geocode_registrar", {
          p_codigo: c.codigo, p_status: "erro", p_detalhe: `HTTP ${res.status}`,
        });
        continue;
      }

      const json = await res.json();
      const hit = Array.isArray(json) ? json[0] : null;
      const lat = hit ? Number(hit.lat) : NaN;
      const lon = hit ? Number(hit.lon) : NaN;
      const display = String(hit?.display_name ?? "");

      if (!hit || !Number.isFinite(lat) || !Number.isFinite(lon)) {
        semResultado++;
        await admin.rpc("fn_geocode_registrar", {
          p_codigo: c.codigo, p_status: "sem_resultado", p_detalhe: limparLogradouro(c.endereco),
        });
        continue;
      }

      if (!viaConfere(limparLogradouro(c.endereco), display)) {
        viaDivergente++;
        await admin.rpc("fn_geocode_registrar", {
          p_codigo: c.codigo,
          p_status: "via_divergente",
          p_detalhe: `pedido: ${limparLogradouro(c.endereco)} | veio: ${display.slice(0, 200)}`,
        });
        continue;
      }

      const dentroDeSp = lat >= -25.35 && lat <= -19.75 && lon >= -53.35 && lon <= -44;
      if (!dentroDeSp) foraDeSp++;

      const { data: gravou } = await admin.rpc("fn_geocode_registrar", {
        p_codigo: c.codigo,
        p_status: dentroDeSp ? "ok" : "fora_de_sp",
        p_lat: lat,
        p_lon: lon,
        p_detalhe: display.slice(0, 300),
      });
      if (gravou === true) gravados++;
    } catch (e) {
      erros++;
      const msg = e instanceof Error ? e.message : String(e);
      await admin.rpc("fn_geocode_registrar", {
        p_codigo: c.codigo, p_status: "erro", p_detalhe: msg.slice(0, 300),
      });
    }
  }

  return Response.json({
    ok: true, candidatos: candidatos.length, gravados, semResultado, viaDivergente, foraDeSp, erros,
  });
});
