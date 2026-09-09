// Servidor MCP para a Meta Marketing API — O Próximo Cliente
// Roda como Edge Function do Supabase. O token da Meta vive em META_ACCESS_TOKEN
// (secret do projeto) e nunca aparece em requisição, resposta ou log.

import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const GRAPH = "https://graph.facebook.com/v21.0";
const TOKEN = Deno.env.get("META_ACCESS_TOKEN") ?? "";
const CONTA = Deno.env.get("META_AD_ACCOUNT_ID") ?? "";
const PAGINA = Deno.env.get("META_PAGE_ID") ?? "";
const SEGREDO = Deno.env.get("MCP_SHARED_SECRET") ?? "";
// Teto de seguranca: nenhuma operacao daqui pode definir orcamento acima disto.
const TETO_CENTAVOS = Number(Deno.env.get("META_MAX_DAILY_BUDGET_CENTS") ?? "5000");

const jsonrpc = (id: unknown, result: unknown) =>
  new Response(JSON.stringify({ jsonrpc: "2.0", id, result }), {
    headers: { "Content-Type": "application/json" },
  });

const erro = (id: unknown, code: number, message: string) =>
  new Response(JSON.stringify({ jsonrpc: "2.0", id, error: { code, message } }), {
    headers: { "Content-Type": "application/json" },
  });

const texto = (v: unknown) => ({
  content: [{ type: "text", text: typeof v === "string" ? v : JSON.stringify(v, null, 2) }],
});

// ---------------------------------------------------------------- Graph API

async function graph(
  metodo: "GET" | "POST",
  caminho: string,
  params: Record<string, unknown> = {},
) {
  const url = new URL(GRAPH + "/" + caminho.replace(/^\//, ""));
  const corpo = new URLSearchParams();
  corpo.set("access_token", TOKEN);

  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null) continue;
    const valor = typeof v === "object" ? JSON.stringify(v) : String(v);
    if (metodo === "GET") url.searchParams.set(k, valor);
    else corpo.set(k, valor);
  }
  if (metodo === "GET") url.searchParams.set("access_token", TOKEN);

  const r = await fetch(url.toString(), {
    method: metodo,
    ...(metodo === "POST"
      ? { body: corpo, headers: { "Content-Type": "application/x-www-form-urlencoded" } }
      : {}),
  });

  const dados = await r.json().catch(() => ({ falha: "resposta nao e JSON" }));
  if (!r.ok) {
    const e = (dados as Record<string, unknown>)?.error ?? dados;
    throw new Error("Meta respondeu " + r.status + ": " + JSON.stringify(e));
  }
  return dados;
}

// Recusa orcamento acima do teto, venha ele de onde vier.
function conferirOrcamento(p: Record<string, unknown>) {
  for (const campo of ["daily_budget", "lifetime_budget"]) {
    const v = p[campo];
    if (v !== undefined && Number(v) > TETO_CENTAVOS) {
      throw new Error(
        "Orcamento de " + v + " centavos acima do teto de " + TETO_CENTAVOS +
          " configurado neste servidor. Ajuste META_MAX_DAILY_BUDGET_CENTS se for mesmo a intencao.",
      );
    }
  }
}

// ---------------------------------------------------------------- ferramentas

const FERRAMENTAS = [
  {
    name: "meta_contexto",
    description:
      "Mostra a que conta e pagina este servidor esta amarrado, o teto de orcamento, e se o token responde. " +
      "Use para conferir a configuracao antes de criar qualquer coisa.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "meta_ler",
    description:
      "Le objetos e colecoes da conta: campanhas, conjuntos, anuncios, criativos, publicos, imagens, videos. " +
      "Caminhos uteis: campaigns, adsets, ads, adcreatives, customaudiences, adimages, advideos, promote_pages. " +
      "Tambem aceita um id direto para ler um objeto especifico. Somente leitura.",
    inputSchema: {
      type: "object",
      properties: {
        caminho: { type: "string", description: "Colecao da conta (ex.: adsets) ou id de um objeto." },
        campos: { type: "string", description: "Campos separados por virgula. Ex.: name,status,daily_budget" },
        limite: { type: "number", description: "Quantos itens trazer. Padrao 25." },
        filtro: { type: "string", description: "JSON de filtering da Marketing API, opcional." },
      },
      required: ["caminho"],
    },
  },
  {
    name: "meta_insights",
    description:
      "Metricas de um objeto (conta, campanha, conjunto ou anuncio), com quebras opcionais por posicionamento, idade, genero ou dispositivo.",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string", description: "Id do objeto. Omita para a conta inteira." },
        campos: { type: "string", description: "Padrao: impressions,clicks,spend,reach,cpm,ctr" },
        periodo: { type: "string", description: "today, yesterday, last_7d, last_30d, maximum..." },
        quebras: { type: "string", description: "Ex.: publisher_platform,platform_position" },
        nivel: { type: "string", description: "account, campaign, adset ou ad" },
      },
    },
  },
  {
    name: "meta_criar_conjunto",
    description:
      "Cria um conjunto de anuncios dentro de uma campanha existente. Nasce PAUSADO. " +
      "Aceita publicos personalizados e semelhantes, segmentacao geografica com exclusoes, e criativo dinamico.",
    inputSchema: {
      type: "object",
      properties: {
        campanha_id: { type: "string" },
        nome: { type: "string" },
        objetivo_otimizacao: {
          type: "string",
          description: "LEAD_GENERATION, LINK_CLICKS, CONVERSATIONS, THRUPLAY, REACH, OFFSITE_CONVERSIONS...",
        },
        evento_cobranca: { type: "string", description: "Padrao IMPRESSIONS." },
        destino: { type: "string", description: "ON_AD (formulario), WEBSITE, WHATSAPP, MESSENGER..." },
        objeto_promovido: { type: "string", description: "JSON. Ex.: {\"page_id\":\"123\"}" },
        segmentacao: { type: "string", description: "JSON do targeting spec completo." },
        criativo_dinamico: { type: "boolean" },
        orcamento_diario: { type: "number", description: "Centavos. So se a campanha nao tiver orcamento proprio." },
      },
      required: ["campanha_id", "nome", "objetivo_otimizacao", "segmentacao"],
    },
  },
  {
    name: "meta_criar_criativo",
    description:
      "Cria um criativo. Pode promover uma publicacao existente (object_story_spec com object_story_id) ou montar " +
      "um criativo proprio com titulo, texto, imagem ou video e botao. Para criativo dinamico use asset_feed_spec.",
    inputSchema: {
      type: "object",
      properties: {
        nome: { type: "string" },
        especificacao: { type: "string", description: "JSON da especificacao do criativo." },
        campo: { type: "string", description: "object_story_spec (padrao) ou asset_feed_spec." },
      },
      required: ["nome", "especificacao"],
    },
  },
  {
    name: "meta_criar_anuncio",
    description: "Cria um anuncio dentro de um conjunto, usando um criativo que ja existe. Nasce PAUSADO.",
    inputSchema: {
      type: "object",
      properties: {
        conjunto_id: { type: "string" },
        nome: { type: "string" },
        criativo_id: { type: "string" },
      },
      required: ["conjunto_id", "nome", "criativo_id"],
    },
  },
  {
    name: "meta_editar",
    description:
      "Edita um objeto existente: renomear, pausar, ativar, mudar orcamento, trocar segmentacao. " +
      "Passe o id e os campos a alterar. Orcamento acima do teto e recusado.",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string" },
        campos: { type: "string", description: "JSON com os campos. Ex.: {\"status\":\"PAUSED\"}" },
      },
      required: ["id", "campos"],
    },
  },
];

async function executar(nome: string, a: Record<string, unknown>) {
  switch (nome) {
    case "meta_contexto": {
      const eu = await graph("GET", "me", { fields: "id,name" });
      return {
        conta_de_anuncios: CONTA,
        pagina: PAGINA,
        teto_orcamento_centavos: TETO_CENTAVOS,
        token_responde_como: eu,
      };
    }

    case "meta_ler": {
      const c = String(a.caminho);
      const alvo = /^\d+$/.test(c) ? c : "act_" + CONTA + "/" + c;
      return await graph("GET", alvo, {
        fields: a.campos,
        limit: a.limite ?? 25,
        filtering: a.filtro,
      });
    }

    case "meta_insights": {
      const alvo = a.id ? String(a.id) : "act_" + CONTA;
      return await graph("GET", alvo + "/insights", {
        fields: a.campos ?? "impressions,clicks,spend,reach,cpm,ctr",
        date_preset: a.periodo ?? "last_7d",
        breakdowns: a.quebras,
        level: a.nivel,
      });
    }

    case "meta_criar_conjunto": {
      const p: Record<string, unknown> = {
        name: a.nome,
        campaign_id: a.campanha_id,
        optimization_goal: a.objetivo_otimizacao,
        billing_event: a.evento_cobranca ?? "IMPRESSIONS",
        targeting: a.segmentacao,
        status: "PAUSED",
      };
      if (a.destino) p.destination_type = a.destino;
      if (a.objeto_promovido) p.promoted_object = a.objeto_promovido;
      if (a.criativo_dinamico) p.is_dynamic_creative = true;
      if (a.orcamento_diario) {
        p.daily_budget = a.orcamento_diario;
        p.bid_strategy = "LOWEST_COST_WITHOUT_CAP";
      }
      conferirOrcamento(p);
      return await graph("POST", "act_" + CONTA + "/adsets", p);
    }

    case "meta_criar_criativo": {
      const campo = String(a.campo ?? "object_story_spec");
      const p: Record<string, unknown> = { name: a.nome };
      p[campo] = a.especificacao;
      return await graph("POST", "act_" + CONTA + "/adcreatives", p);
    }

    case "meta_criar_anuncio":
      return await graph("POST", "act_" + CONTA + "/ads", {
        name: a.nome,
        adset_id: a.conjunto_id,
        creative: { creative_id: a.criativo_id },
        status: "PAUSED",
      });

    case "meta_editar": {
      const campos = typeof a.campos === "string" ? JSON.parse(a.campos) : a.campos;
      conferirOrcamento(campos as Record<string, unknown>);
      return await graph("POST", String(a.id), campos as Record<string, unknown>);
    }

    default:
      throw new Error("Ferramenta desconhecida: " + nome);
  }
}

// ---------------------------------------------------------------- MCP

Deno.serve(async (req: Request) => {
  const url = new URL(req.url);

  // O segredo viaja no caminho, porque conector remoto nem sempre deixa
  // configurar cabecalho. Sem ele, o servidor nao responde nada.
  if (!SEGREDO || !url.pathname.includes(SEGREDO)) {
    return new Response("nao encontrado", { status: 404 });
  }
  if (req.method !== "POST") {
    return new Response("use POST", { status: 405 });
  }

  let corpo: Record<string, unknown>;
  try {
    corpo = await req.json();
  } catch {
    return erro(null, -32700, "JSON invalido");
  }

  const id = corpo.id;
  const method = corpo.method as string | undefined;
  const params = corpo.params as Record<string, unknown> | undefined;

  if (method === "initialize") {
    return jsonrpc(id, {
      protocolVersion: "2024-11-05",
      capabilities: { tools: {} },
      serverInfo: { name: "meta-ads-opc", version: "1.0.0" },
    });
  }

  if (method === "notifications/initialized") {
    return new Response(null, { status: 202 });
  }

  if (method === "tools/list") {
    return jsonrpc(id, { tools: FERRAMENTAS });
  }

  if (method === "tools/call") {
    const nome = String(params?.name ?? "");
    const args = (params?.arguments ?? {}) as Record<string, unknown>;
    if (!TOKEN) {
      return jsonrpc(id, {
        ...texto("META_ACCESS_TOKEN nao esta configurado neste projeto do Supabase."),
        isError: true,
      });
    }
    try {
      return jsonrpc(id, texto(await executar(nome, args)));
    } catch (e) {
      return jsonrpc(id, { ...texto(String((e as Error).message ?? e)), isError: true });
    }
  }

  return erro(id ?? null, -32601, "Metodo nao suportado: " + method);
});
