// Painel SDR — o formulario de qualificacao e agendamento, fora do GHL.
//
// POR QUE EXISTE
// A API publica do GHL nao edita formularios (forms.json: so GET /forms/,
// GET /forms/submissions, POST /forms/upload-custom-files — conferido no
// repositorio oficial em 27/09/2026). O formulario nativo tambem nao le o
// contato ao abrir, nao mostra a agenda do closer e nao lista usuarios. Entao
// o que o dono pediu — pre-preenchido pelo anuncio, ordem BANT, agenda do
// closer na mesma tela, SDR escolhido da lista do CRM, closer recebendo tudo
// no card e no evento — nao cabe no formulario. Cabe numa pagina que fala
// com a API. Esta pagina.
//
// O QUE FAZ, por rota
//   GET  /                      a pagina (painel.ts)
//   GET  /api/saude             sem PIN: o token esta guardado? o GHL responde?
//   GET  /api/inicio            usuarios, calendario do closer, catalogo de campos
//   GET  /api/contatos?q=|tag=  busca; `tag=fila-sdr` e a fila do dia
//   GET  /api/contato/:id       contato + oportunidade aberta
//   GET  /api/slots?data=       horarios livres do closer, 7 dias a partir da data
//   POST /api/resultado         marca `Resultado da tentativa` (nao atendeu, etc.)
//   POST /api/salvar            grava os campos, marca Atendeu + Qualificacao=SDR,
//                               cria o compromisso confirmado com a descricao BANT
//                               e deixa uma nota no contato.
//
// O que NAO faz de proposito: nao move etapa da oportunidade nem calcula a
// nota. Isso e do `Pos-agendamento v2` (gatilho: compromisso confirmado neste
// calendario) e do `Pos-ligacao v3` (gatilho: `Resultado da tentativa` mudou).
// O painel so produz os dois eventos que esses workflows ja esperam.
//
// SEGREDOS
// O token do GHL (`config.ghl_pit`) chega pela rota POST /api/instalar, que a
// Action wesales-finalizar (modo `formulario`) chama com o segredo GHL_PIT.
// A rota so aceita ENQUANTO nao ha token guardado (primeira escrita vence) e
// so guarda um token que o GHL aceita — depois disso e uma porta fechada.
// Trocar o token = apagar a linha `ghl_pit` da tabela e rodar a Action de novo.
// O token nunca vai ao navegador. O SDR entra com um PIN
// (`config.painel_sdr_pin`). verify_jwt fica DESLIGADO porque o SDR nao tem
// conta no Supabase; o PIN e a porta. Nunca apaga contato, oportunidade ou lead.
//
// Projeto: cscczluzpblzhvojxanp. O maquina-yt-dark (vevocauwtarctfwngrch) esta
// em restricao de cota de storage e o gateway responde 402 (run 36333419041).
import { createClient } from "jsr:@supabase/supabase-js@2";
import { PAGINA } from "./painel.ts";

const LOC = "1D53YTI9C7oIMBavcQxV";
const CALENDARIO = "3uNQFjCEDe7b4gKZJuOZ"; // "Reuniao com closer"
const FUSO = "America/Sao_Paulo";
const GHL = "https://services.leadconnectorhq.com";
const VERSAO = "2021-07-28";
// Sem User-Agent de navegador o Cloudflare do GHL devolve 403 erro 1010.
const UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36";

const C = {
  resultado: "nPafc9c0JdSSptdPhUlF",
  dataRetorno: "IBOMNQecWtIUruHpNAs1",
  horaRetorno: "IHXNFnguTPyNj5Q59ea2",
  qualificacao: "mJv4YcFBH4NsPfbh5Q3G",
};
const NOME_CAMPO_SDR = "SDR responsável"; // criado pela Action; achado pelo nome

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

async function config(chave: string): Promise<Record<string, string> | null> {
  const { data } = await db.from("config").select("valor").eq("chave", chave).maybeSingle();
  return (data?.valor as Record<string, string>) ?? null;
}

function json(corpo: unknown, status = 200) {
  return new Response(JSON.stringify(corpo), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
  });
}

class ErroGHL extends Error {
  constructor(public status: number, public corpo: string, public rota: string) {
    super(`${rota} -> HTTP ${status} ${corpo.slice(0, 300)}`);
  }
}

let pitCache: string | null = null;
async function pit(): Promise<string> {
  if (pitCache) return pitCache;
  const v = await config("ghl_pit");
  if (!v?.token) throw new Error("ghl_pit nao configurado — rode a Action wesales-finalizar, modo formulario");
  pitCache = v.token;
  return pitCache;
}

async function ghl(metodo: string, rota: string, corpo?: unknown) {
  const r = await fetch(GHL + rota, {
    method: metodo,
    headers: {
      Authorization: "Bearer " + (await pit()),
      Version: VERSAO,
      Accept: "application/json",
      "User-Agent": UA,
      ...(corpo !== undefined ? { "Content-Type": "application/json" } : {}),
    },
    body: corpo !== undefined ? JSON.stringify(corpo) : undefined,
  });
  const texto = await r.text();
  if (!r.ok) throw new ErroGHL(r.status, texto, `${metodo} ${rota}`);
  return texto ? JSON.parse(texto) : {};
}

// ---------- catalogo de campos (cache por isolate, 10 min) ----------
type Campo = { id: string; name: string; dataType: string; picklistOptions?: string[] };
let catalogo: { quando: number; campos: Campo[] } | null = null;
async function campos(): Promise<Campo[]> {
  if (catalogo && Date.now() - catalogo.quando < 600_000) return catalogo.campos;
  const r = await ghl("GET", `/locations/${LOC}/customFields?model=contact`);
  const lista = (r.customFields ?? []) as Campo[];
  catalogo = { quando: Date.now(), campos: lista };
  return lista;
}

function valorDe(contato: Record<string, unknown>, id: string): string {
  const cf = (contato.customFields as Array<{ id: string; value: unknown }>) ?? [];
  const v = cf.find((x) => x.id === id)?.value;
  return v === undefined || v === null ? "" : Array.isArray(v) ? v.join(", ") : String(v);
}

// ---------- rotas ----------
async function inicio() {
  const [usuarios, cal, cat] = await Promise.all([
    ghl("GET", `/users/?locationId=${LOC}`),
    ghl("GET", `/calendars/${CALENDARIO}`),
    campos(),
  ]);
  const c = cal.calendar ?? cal;
  return {
    usuarios: ((usuarios.users ?? []) as Array<Record<string, string>>).map((u) => ({
      id: u.id,
      nome: u.name || `${u.firstName ?? ""} ${u.lastName ?? ""}`.trim(),
      email: u.email,
    })),
    calendario: {
      id: CALENDARIO,
      nome: c.name,
      duracao: Number(c.slotDuration ?? 60),
      unidade: c.slotDurationUnit ?? "mins",
      equipe: ((c.teamMembers ?? []) as Array<Record<string, unknown>>).map((m) => m.userId),
    },
    campos: cat.map((f) => ({ id: f.id, nome: f.name, tipo: f.dataType, opcoes: f.picklistOptions ?? [] })),
    campoSdr: cat.find((f) => f.name === NOME_CAMPO_SDR)?.id ?? null,
  };
}

async function contatos(q: string, tag: string) {
  const corpo: Record<string, unknown> = { locationId: LOC, pageLimit: 50 };
  if (q) corpo.query = q;
  if (tag) corpo.filters = [{ field: "tags", operator: "eq", value: tag }];
  const r = await ghl("POST", "/contacts/search", corpo);
  return ((r.contacts ?? []) as Array<Record<string, unknown>>).map((c) => ({
    id: c.id,
    nome: c.contactName || `${c.firstName ?? ""} ${c.lastName ?? ""}`.trim(),
    telefone: c.phone ?? "",
    email: c.email ?? "",
    tags: c.tags ?? [],
    dnd: !!c.dnd,
  }));
}

async function contato(id: string) {
  const [c, o] = await Promise.all([
    ghl("GET", `/contacts/${id}`),
    ghl("GET", `/opportunities/search?location_id=${LOC}&contact_id=${id}`),
  ]);
  const ct = c.contact ?? c;
  const cf: Record<string, string> = {};
  for (const x of (ct.customFields ?? []) as Array<{ id: string; value: unknown }>) {
    cf[x.id] = valorDe(ct, x.id);
  }
  const opp = ((o.opportunities ?? []) as Array<Record<string, unknown>>).find((x) => x.status === "open") ??
    (o.opportunities ?? [])[0] ?? null;
  return {
    id: ct.id,
    nome: ct.contactName || `${ct.firstName ?? ""} ${ct.lastName ?? ""}`.trim(),
    telefone: ct.phone ?? "",
    email: ct.email ?? "",
    tags: ct.tags ?? [],
    dnd: !!ct.dnd,
    dono: ct.assignedTo ?? null,
    campos: cf,
    oportunidade: opp
      ? { id: opp.id, etapa: opp.pipelineStageId, status: opp.status, nome: opp.name, valor: opp.monetaryValue }
      : null,
  };
}

async function slots(data: string) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(data)) throw new Error("data invalida");
  const ini = Date.parse(`${data}T00:00:00-03:00`);
  const fim = ini + 7 * 86_400_000 - 1;
  const r = await ghl("GET", `/calendars/${CALENDARIO}/free-slots?startDate=${ini}&endDate=${fim}&timezone=${FUSO}`);
  const dias: Record<string, string[]> = {};
  for (const [k, v] of Object.entries(r)) {
    if (k === "traceId") continue;
    dias[k] = ((v as { slots?: string[] }).slots ?? []);
  }
  return { dias };
}

async function resultado(p: { contactId: string; resultado: string; dataRetorno?: string; horaRetorno?: string }) {
  const cat = await campos();
  const opcoes = cat.find((f) => f.id === C.resultado)?.picklistOptions ?? [];
  if (!opcoes.includes(p.resultado)) throw new Error(`resultado fora do vocabulario: ${p.resultado}`);
  const cf: Array<{ id: string; field_value: string }> = [{ id: C.resultado, field_value: p.resultado }];
  if (p.resultado === "Pediu retorno") {
    if (!p.dataRetorno) throw new Error("Pediu retorno exige data de retorno");
    cf.push({ id: C.dataRetorno, field_value: p.dataRetorno });
    if (p.horaRetorno) cf.push({ id: C.horaRetorno, field_value: p.horaRetorno });
  }
  await ghl("PUT", `/contacts/${p.contactId}`, { customFields: cf });
  return { ok: true, gravado: cf };
}

function fmtSP(iso: string) {
  return new Intl.DateTimeFormat("pt-BR", {
    timeZone: FUSO, weekday: "short", day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit",
  }).format(new Date(iso));
}

type Salvar = {
  contactId: string;
  campos: Record<string, string>;
  sdr: { id: string; nome: string };
  atendeu: boolean;
  agendamento: { inicio: string; fim: string } | null;
  observacoes?: string;
};

async function salvar(p: Salvar) {
  if (!p.contactId || !p.sdr?.nome) throw new Error("faltam contactId ou SDR");
  const cat = await campos();
  const porId = new Map(cat.map((f) => [f.id, f]));

  // So grava campo que existe no catalogo e, se for lista, valor da lista.
  const cf: Array<{ id: string; field_value: string }> = [];
  for (const [id, v] of Object.entries(p.campos ?? {})) {
    const f = porId.get(id);
    if (!f) continue;
    const val = (v ?? "").toString().trim();
    if (!val) continue;
    if (f.picklistOptions?.length && !f.picklistOptions.includes(val)) continue;
    cf.push({ id, field_value: val });
  }
  cf.push({ id: C.qualificacao, field_value: "SDR" });
  const campoSdr = cat.find((f) => f.name === NOME_CAMPO_SDR);
  if (campoSdr) cf.push({ id: campoSdr.id, field_value: p.sdr.nome });
  if (p.atendeu) cf.push({ id: C.resultado, field_value: "Atendeu" });

  // 1. campos primeiro: o Pos-agendamento le os campos para calcular a nota.
  await ghl("PUT", `/contacts/${p.contactId}`, { customFields: cf });

  const ct = await contato(p.contactId);
  const linha = (id: string) => {
    const f = porId.get(id);
    const v = ct.campos[id];
    return f && v ? `- ${f.name}: ${v}` : null;
  };
  const bloco = (titulo: string, ids: string[]) => {
    const ls = ids.map(linha).filter(Boolean);
    return ls.length ? `${titulo}\n${ls.join("\n")}` : null;
  };
  const N = ["OJQEsl5dV37pfVY2sIaB", "qmIKSSDVYNLl5E8vnr3f", "wmod0p91VuukwWDwKCgi", "xjEcIFfdt2h29wBaKMQO",
    "sJY6q3X7deZ5yGbjiORT", "Z7qwvDlagOLEhoCz5G5v", "qxJhMydTz6DcM4td4F08", "dYKivcXqdw4MToQLwoA9",
    "O500dbTabWUJwnBKwuUl", "QyEDg0qFlQ3gra5qZsJF"];
  const T = ["2LnUD4KYSGkIBwiUdzl3", "lAqbaJE9K4LDkq3t2zzc"];
  const B = ["bQithNwReQIBGlZBaNlI", "x5JUx0YCWaZmH3Q85psI", "f5bd9nBObV1cGgejAzdv", "SZVgh0Y5HRcWWZG4fO9V"];
  const A = ["3dphGCPCoFcYXEQC2jeB"];
  const empresa = ct.campos["zs7KhkmfUMyuXWQlyUv7"] || "";
  const descricao = [
    `QUALIFICAÇÃO BANT · por ${p.sdr.nome} · ${fmtSP(new Date().toISOString())}`,
    `${ct.nome}${empresa ? " — " + empresa : ""} · ${ct.telefone}${ct.email ? " · " + ct.email : ""}`,
    bloco("NECESSIDADE", N), bloco("TEMPO / URGÊNCIA", T), bloco("INVESTIMENTO", B), bloco("AUTORIDADE", A),
    p.observacoes?.trim() ? `OBSERVAÇÕES DO SDR\n${p.observacoes.trim()}` : null,
  ].filter(Boolean).join("\n\n");

  let compromisso: unknown = null;
  if (p.agendamento?.inicio) {
    const cal = await ghl("GET", `/calendars/${CALENDARIO}`);
    const c = cal.calendar ?? cal;
    const equipe = ((c.teamMembers ?? []) as Array<{ userId: string }>).map((m) => m.userId);
    const corpo: Record<string, unknown> = {
      calendarId: CALENDARIO,
      locationId: LOC,
      contactId: p.contactId,
      startTime: p.agendamento.inicio,
      endTime: p.agendamento.fim,
      title: `Reunião de diagnóstico — ${ct.nome}${empresa ? " (" + empresa + ")" : ""}`,
      appointmentStatus: "confirmed",
      description: descricao,
      toNotify: true,
    };
    if (equipe.length === 1) corpo.assignedUserId = equipe[0];
    // 2. compromisso confirmado: e o evento que dispara o Pos-agendamento v2.
    compromisso = await ghl("POST", "/calendars/events/appointments", corpo);
  }

  // 3. nota no contato: o closer abre o card e ve tudo, mesmo sem abrir o evento.
  await ghl("POST", `/contacts/${p.contactId}/notes`, {
    userId: p.sdr.id || undefined,
    body: (p.agendamento?.inicio ? `REUNIÃO MARCADA para ${fmtSP(p.agendamento.inicio)}\n\n` : "") + descricao,
  });

  return { ok: true, gravados: cf.length, compromisso, descricao };
}

// ---------- servidor ----------
Deno.serve(async (req) => {
  const url = new URL(req.url);
  // O caminho chega como /painel-sdr/api/... (ou /functions/v1/painel-sdr/...)
  const rota = url.pathname.replace(/^.*?\/painel-sdr/, "") || "/";

  if (req.method === "GET" && (rota === "/" || rota === "")) {
    return new Response(PAGINA, { headers: { "Content-Type": "text/html; charset=utf-8" } });
  }

  if (req.method === "POST" && rota === "/api/instalar") {
    const ja = (await config("ghl_pit"))?.token;
    if (ja) return json({ erro: "token ja instalado; para trocar, apague config.ghl_pit e rode de novo" }, 409);
    const { token } = await req.json().catch(() => ({ token: "" }));
    if (!token || typeof token !== "string") return json({ erro: "falta token" }, 400);
    // So guarda o que o GHL aceita: um token errado nao pode ocupar a vaga.
    const prova = await fetch(`${GHL}/users/?locationId=${LOC}`, {
      headers: { Authorization: "Bearer " + token, Version: VERSAO, Accept: "application/json", "User-Agent": UA },
    });
    if (!prova.ok) return json({ erro: `GHL recusou o token: HTTP ${prova.status}` }, 400);
    const { error } = await db.from("config").upsert({ chave: "ghl_pit", valor: { token }, atualizado_em: new Date().toISOString() });
    if (error) return json({ erro: error.message }, 500);
    pitCache = token;
    return json({ ok: true, usuarios: ((await prova.json()).users ?? []).length });
  }

  if (rota === "/api/saude") {
    const tem = !!(await config("ghl_pit"))?.token;
    let ghlOk: unknown = null;
    if (tem) {
      try {
        const u = await ghl("GET", `/users/?locationId=${LOC}`);
        ghlOk = { usuarios: (u.users ?? []).length };
      } catch (e) {
        ghlOk = { erro: String(e) };
      }
    }
    return json({ ok: tem && ghlOk && !(ghlOk as { erro?: string }).erro, token_guardado: tem, ghl: ghlOk });
  }

  const pinCfg = await config("painel_sdr_pin");
  const pinDado = req.headers.get("x-pin") ?? "";
  if (!pinCfg?.pin || pinDado !== pinCfg.pin) return json({ erro: "PIN invalido" }, 401);

  try {
    if (req.method === "GET" && rota === "/api/inicio") return json(await inicio());
    if (req.method === "GET" && rota === "/api/contatos") {
      return json(await contatos(url.searchParams.get("q") ?? "", url.searchParams.get("tag") ?? ""));
    }
    const m = rota.match(/^\/api\/contato\/([A-Za-z0-9]+)$/);
    if (req.method === "GET" && m) return json(await contato(m[1]));
    if (req.method === "GET" && rota === "/api/slots") return json(await slots(url.searchParams.get("data") ?? ""));
    if (req.method === "POST" && rota === "/api/resultado") return json(await resultado(await req.json()));
    if (req.method === "POST" && rota === "/api/salvar") return json(await salvar(await req.json()));
    return json({ erro: `rota desconhecida: ${req.method} ${rota}` }, 404);
  } catch (e) {
    if (e instanceof ErroGHL) return json({ erro: e.message, status: e.status, rota: e.rota }, 502);
    return json({ erro: String(e) }, 500);
  }
});
