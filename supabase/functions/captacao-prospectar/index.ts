import { createClient } from "npm:@supabase/supabase-js@2";

// Repõe o estoque de prospects de captação consultando a GeckoAPI, e só quando
// precisa. Custo medido: 1 crédito por página de 30 anúncios.
//
// v3 — pesquisa em vários portais, em paralelo (pedido do usuário em 13/08:
// "Precisa ser pesquisa assíncrona, em todos os portais"). Cada cidade/
// operação agora tem um cursor por PORTAL em `captacao_varredura` (coluna
// `target`), e os cursores da rodada são disparados em ondas concorrentes
// (Promise.all) em vez de um por vez — antes era um for-await sequencial.
//
// Portais cobertos e por quê:
//   zapimoveis.com.br  — advertiser.phoneNumbers/license na própria listagem.
//   vivareal.com.br    — mesmo parser da Grupo Zap (glue-api), mesmo shape.
//   chavesnamao.com.br — advertiser.phones.{cellphone,landline} e, melhor
//                         que os outros dois, advertiser.type ("PJ"/"PF"):
//                         sinal direto de pessoa física, sem depender só do
//                         regex de nome.
//   olx.com.br          — DE FORA. A listagem (PLP) da OLX não traz telefone
//                         nem anunciante, só um "professionalAd": bool.
//                         Telefone só sai na página do anúncio (PDP), que
//                         cobra 1 crédito por imóvel — ~30x mais caro que 1
//                         crédito por 30 imóveis do PLP. Não compensa pro
//                         volume que se busca aqui.
//
// businessType vai sempre minúsculo ("sale"/"rent") — a validação da
// GeckoAPI rejeita "RENTAL" com 400; "SALE" maiúsculo passa por coincidência,
// "rent" exige minúsculo exato.
//
// Economia, na ordem em que age:
//   1. se o estoque de particulares já cobre o alvo, devolve sem gastar nada;
//   2. cada cidade+portal tem cursor próprio, então nunca relemos a mesma página;
//   3. dispara em ondas de `concorrencia` cursores e reavalia o estoque entre
//      ondas — pára assim que atinge o alvo, em vez de gastar créditos à toa;
//   4. tudo o que chega é gravado — uma chamada alimenta várias rodadas.

const BASE = "https://api.geckoapi.com.br";

type Cursor = {
  id: number; cidade: string; uf: string; business_type: string; target: string;
  proxima_pagina: number; paginas_lidas: number;
};

const texto = (v: unknown): string | null => {
  const s = String(v ?? "").trim();
  return s ? s : null;
};

const numero = (v: unknown): number | null => {
  const n = Number(Array.isArray(v) ? v[0] : v);
  return Number.isFinite(n) && n > 0 ? n : null;
};

// Normalizar em dígitos evita o mesmo proprietário entrar duas vezes na fila.
const fone = (v: unknown): string | null => {
  const d = String(v ?? "").replace(/\D/g, "");
  if (d.length < 10 || d.length > 13) return null;
  return d.startsWith("55") && d.length > 11 ? d.slice(2) : d;
};

// zapimoveis e vivareal usam o mesmo parser (glue-api da Grupo Zap):
// advertiser.{name,license,phoneNumbers,whatsAppNumber}, address.{city,
// neighborhood,street}, attributes.{usableAreas,bedrooms,parkingSpaces},
// prices tanto como objeto {mainValue} (zap) quanto array [{value}] (vivareal).
function extrairGrupoZap(itens: any[], target: string, cidadeFallback: string) {
  return itens.map((it) => {
    const ad = it?.advertiser ?? {};
    const end = it?.address ?? {};
    const creci = texto(ad.license);
    const preco = numero(it?.prices?.mainValue) ??
      numero(Array.isArray(it?.prices) ? it.prices[0]?.value : null);
    const businessRaw = String(it?.business ?? it?.businessType ??
      (Array.isArray(it?.prices) ? it.prices[0]?.businessType : "") ?? "").toUpperCase();
    return {
      fonte: target,
      anuncio_id: texto(it?.id),
      url: texto(it?.url),
      titulo: texto(it?.title)?.slice(0, 180) ?? null,
      tipo: texto(it?.listingType ?? it?.business),
      tipo_operacao: businessRaw.startsWith("RENT") ? "rent" : "sale",
      cidade: texto(end?.city) ?? cidadeFallback,
      bairro: texto(end?.neighborhood),
      endereco: texto(end?.street),
      preco,
      area: numero(it?.attributes?.usableAreas),
      quartos: numero(it?.attributes?.bedrooms),
      vagas: numero(it?.attributes?.parkingSpaces),
      anunciante: texto(ad.name),
      telefone: fone((ad.phoneNumbers ?? [])[0]) ?? fone(ad.whatsAppNumber),
      whatsapp: fone(ad.whatsAppNumber),
      tem_creci: creci !== null,
      creci,
      dados: { advertiser: ad, extraido_em: undefined },
    };
  }).filter((l) => l.anuncio_id !== null && l.telefone !== null);
}

// chavesnamao.com.br: advertiser.phones.{cellphone,landline}, advertiser.type
// ("PJ"/"PF" — guardado em dados pra um futuro ajuste do classificador),
// prices.rawPrice, counts.{bedrooms,garages}.count, area.total.
function extrairChavesNaMao(itens: any[], cidadeFallback: string) {
  return itens.map((it) => {
    const ad = it?.advertiser ?? {};
    const end = it?.address ?? {};
    const fones = ad?.phones ?? {};
    const creci = texto(ad.creci);
    const businessRaw = String(it?.businessType ?? it?.transaction ?? "").toUpperCase();
    return {
      fonte: "chavesnamao.com.br",
      anuncio_id: texto(it?.id),
      url: texto(it?.url),
      titulo: texto(it?.title)?.slice(0, 180) ?? null,
      tipo: texto(it?.transaction),
      tipo_operacao: businessRaw.startsWith("RENT") ? "rent" : "sale",
      cidade: texto(end?.city) ?? cidadeFallback,
      bairro: texto(end?.neighborhood),
      endereco: texto(end?.street),
      preco: numero(it?.prices?.rawPrice),
      area: numero(it?.area?.total),
      quartos: numero(it?.counts?.bedrooms?.count),
      vagas: numero(it?.counts?.garages?.count),
      anunciante: texto(ad.name),
      telefone: fone(fones.cellphone) ?? fone(fones.landline),
      whatsapp: fone(fones.cellphone),
      tem_creci: creci !== null,
      creci,
      dados: { advertiser_type: texto(ad.type) },
    };
  }).filter((l) => l.anuncio_id !== null && l.telefone !== null);
}

function extrair(target: string, itens: any[], cidadeFallback: string) {
  if (target === "chavesnamao.com.br") return extrairChavesNaMao(itens, cidadeFallback);
  return extrairGrupoZap(itens, target, cidadeFallback);
}

function businessTypeParaApi(bt: string): string {
  const t = String(bt ?? "").trim().toLowerCase();
  return t.startsWith("rent") || t === "aluguel" || t === "locação" ? "rent" : "sale";
}

async function processarCursor(admin: any, apiKey: string, c: Cursor) {
  const res = await fetch(`${BASE}/v1/extract`, {
    method: "POST",
    headers: { "X-API-Key": apiKey, "Content-Type": "application/json" },
    body: JSON.stringify({
      target: c.target, type: "plp",
      city: c.cidade, state: c.uf, businessType: businessTypeParaApi(c.business_type),
      page: c.proxima_pagina,
    }),
    signal: AbortSignal.timeout(120000),
  });

  if (!res.ok) {
    return { c, ok: false, erro: `HTTP ${res.status}`, pararTudo: res.status === 402 || res.status === 429 };
  }

  const json = await res.json();
  const d = json?.data ?? {};
  const itens: any[] = Array.isArray(d.items) ? d.items : [];
  const linhas = extrair(c.target, itens, c.cidade);

  let gravados = 0;
  if (linhas.length > 0) {
    const { error } = await admin.from("captacao_prospects")
      .upsert(linhas, { onConflict: "fonte,anuncio_id", ignoreDuplicates: true });
    if (error) return { c, ok: false, erro: `gravar: ${error.message}` };
    gravados = linhas.length;
  }

  await admin.from("captacao_varredura").update({
    proxima_pagina: Number(d.nextPage ?? c.proxima_pagina + 1),
    paginas_lidas: c.paginas_lidas + 1,
    total_resultados: Number(d.totalResults ?? 0) || null,
    ultima_coleta: new Date().toISOString(),
  }).eq("id", c.id);

  return { c, ok: true, gravados };
}

Deno.serve(async (req) => {
  const admin = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  let alvo = 30;          // particulares desejados em estoque
  let maxPaginas = 8;      // teto de créditos por execução
  let concorrencia = 4;    // cursores disparados em paralelo por onda
  try {
    const b = await req.json();
    const a = Number(b?.alvo); if (Number.isFinite(a) && a > 0) alvo = Math.min(5000, Math.floor(a));
    const m = Number(b?.maxPaginas); if (Number.isFinite(m) && m > 0) maxPaginas = Math.min(40, Math.floor(m));
    const cc = Number(b?.concorrencia); if (Number.isFinite(cc) && cc > 0) concorrencia = Math.min(8, Math.floor(cc));
  } catch (_e) { /* padrões */ }

  const { data: cred } = await admin.from("integracao_credenciais")
    .select("valor").eq("chave", "geckoapi_api_key").maybeSingle();
  const apiKey = (cred as any)?.valor;
  if (!apiKey) return Response.json({ ok: false, motivo: "credencial geckoapi ausente" }, { status: 500 });

  const { data: est0 } = await admin.rpc("fn_captacao_estoque");
  if (Number((est0 as any)?.particulares ?? 0) >= alvo) {
    return Response.json({ ok: true, creditos: 0, motivo: "estoque suficiente", estoque: est0 });
  }

  const { data: cursores } = await admin.from("captacao_varredura")
    .select("id, cidade, uf, business_type, target, proxima_pagina, paginas_lidas")
    .eq("ativa", true)
    .order("paginas_lidas", { ascending: true })
    .order("cidade", { ascending: true })
    .limit(maxPaginas);

  const fila = (cursores ?? []) as Cursor[];
  if (fila.length === 0) {
    return Response.json({ ok: false, motivo: "nenhuma cidade ativa na varredura" }, { status: 500 });
  }

  let creditos = 0, gravados = 0, erros = 0, ondas = 0;
  const falhas: string[] = [];
  const porCidade: Record<string, number> = {};
  const porPortal: Record<string, number> = {};
  let pararTudo = false;

  // Ondas concorrentes em vez de um cursor por vez: cada onda dispara até
  // `concorrencia` chamadas em paralelo (Promise.all), depois reavalia o
  // estoque — pára assim que o alvo é atingido, sem gastar as ondas restantes.
  for (let i = 0; i < fila.length && !pararTudo; i += concorrencia) {
    const onda = fila.slice(i, i + concorrencia);
    ondas++;
    const resultados = await Promise.all(onda.map((c) => processarCursor(admin, apiKey, c)));

    for (const r of resultados) {
      if (!r.ok) {
        erros++;
        falhas.push(`${r.c.target} ${r.c.cidade} p${r.c.proxima_pagina}: ${r.erro}`);
        if (r.pararTudo) pararTudo = true;
        continue;
      }
      creditos++;
      gravados += r.gravados;
      porCidade[r.c.cidade] = (porCidade[r.c.cidade] ?? 0) + r.gravados;
      porPortal[r.c.target] = (porPortal[r.c.target] ?? 0) + r.gravados;
    }

    await admin.rpc("fn_captacao_classificar");
    const { data: estAtual } = await admin.rpc("fn_captacao_estoque");
    if (Number((estAtual as any)?.particulares ?? 0) >= alvo) break;
  }

  await admin.rpc("fn_captacao_classificar");
  const { data: estFinal } = await admin.rpc("fn_captacao_estoque");

  return Response.json({
    ok: erros === 0, creditos, gravados, erros, ondas, falhas: falhas.slice(0, 10),
    por_cidade: porCidade, por_portal: porPortal, estoque: estFinal,
  });
});
