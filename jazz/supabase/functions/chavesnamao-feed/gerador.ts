// Gerador do XML do portal Chaves na Mão, no padrão publicado pelo próprio
// portal (documentação oficial "Documentação XML Chaves Na Mão", tags em
// minúsculo, raiz `<Document>`, UTF-8).
//
// Por que arquivo separado do `index.ts`: aqui não entra nada de Deno nem do
// Supabase, só função pura de dado para texto. Isso permite conferir a saída
// fora do runtime — foi assim que o formato foi validado contra o exemplo
// oficial antes de existir qualquer deploy.
//
// Três diferenças de fundo em relação ao VRSync (Grupo OLX), e todas vêm da
// documentação do Chaves na Mão, não de preferência:
//
// 1. PNG não entra. O portal processa JPG, JPEG e WEBP; PNG é descartado na
//    origem em vez de virar foto quebrada no anúncio. (O VRSync aceita PNG, e
//    por isso o filtro daqui é mais estreito que o do outro feed.)
// 2. O portal lê o arquivo UMA vez por dia. Então não existe aqui o truque de
//    centavos por semana que o feed do Zap usa para forçar reindexação: quem
//    sinaliza atualização neste padrão é a tag `data_atualizacao`, que o
//    portal lê explicitamente.
// 3. Todas as tags precisam existir, mesmo vazias ("é necessária a utilização
//    de todas as tags, mesmo que não sejam de preenchimento obrigatório"), e a
//    estrutura é case sensitive. Por isso o bloco é montado inteiro, sempre na
//    mesma ordem do documento, com string vazia onde não há dado — e não com
//    tag omitida.

export type ImovelNormalizado = {
  codigo: string;
  titulo?: string | null;
  descricao?: string | null;
  tipo?: string | null;
  finalidade?: string | null;
  valor_venda?: number | null;
  valor_locacao?: number | null;
  bairro?: string | null;
  cidade?: string | null;
  uf?: string | null;
  cep?: string | null;
  endereco?: string | null;
  endereco_viacep?: string | null;
  numero?: string | null;
  area_util?: number | null;
  area_total?: number | null;
  dormitorios?: number | null;
  suites?: number | null;
  vagas?: number | null;
  banheiros?: number | null;
  caracteristicas?: string[] | null;
  fotos?: string[] | null;
  iptu?: number | null;
  condominio?: number | null;
  ano_construcao?: number | null;
  video?: string | null;
  tour_virtual?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  indisponivel_espelho?: boolean | null;
};

export type LinhaFeed = {
  id: string;
  codigo_original: string;
  dados_normalizados: ImovelNormalizado;
  created_at?: string | null;
  updated_at?: string | null;
  feed_ai_content?:
    | { titulo_otimizado?: string | null; descricao_otimizada?: string | null; ativo?: boolean | null }
    | { titulo_otimizado?: string | null; descricao_otimizada?: string | null; ativo?: boolean | null }[]
    | null;
};

export type OpcoesCnm = {
  /** Link do imóvel no site da imobiliária. `{codigo}` é substituído pelo código do Vista. */
  linkTemplate?: string | null;
  /** 1 esconde o endereço no portal (saída de emergência se o portal recusar o número publicado). */
  esconderEndereco?: boolean;
  /** Teto de fotos por imóvel; o portal ignora o que passar de 30. */
  maxFotos?: number;
  /** Quantos anúncios do topo da fila de prioridade vão como destaque. */
  destaques?: number;
};

// ---------------------------------------------------------------------------
// Limites e vocabulários do portal
// ---------------------------------------------------------------------------

/** Documentação: "O limite hoje esta em 30 (trinta) fotos por imóvel." */
export const CNM_MAX_FOTOS = 30;
/** Documentação: descritivo com "tamanho máximo de 3000 caracteres". */
export const CNM_DESC_MAX = 3000;
export const CNM_TITULO_MAX = 100;
/** Documentação: "os formatos de imagem que são processados na integração são: JPG, JPEG e WEBP." */
const RE_FOTO_CNM = /^https?:\/\/.+\.(jpe?g|webp)(\?|$)/i;
const RE_URL_VIDEO = /youtube\.com|youtu\.be|vimeo\.com/i;

const UF_NOME: Record<string, string> = {
  AC: "Acre", AL: "Alagoas", AP: "Amapá", AM: "Amazonas", BA: "Bahia", CE: "Ceará",
  DF: "Distrito Federal", ES: "Espírito Santo", GO: "Goiás", MA: "Maranhão",
  MT: "Mato Grosso", MS: "Mato Grosso do Sul", MG: "Minas Gerais", PA: "Pará",
  PB: "Paraíba", PR: "Paraná", PE: "Pernambuco", PI: "Piauí", RJ: "Rio de Janeiro",
  RN: "Rio Grande do Norte", RS: "Rio Grande do Sul", RO: "Rondônia", RR: "Roraima",
  SC: "Santa Catarina", SP: "São Paulo", SE: "Sergipe", TO: "Tocantins",
};

function semAcento(s: string): string {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "");
}

const NOME_UF: Record<string, string> = Object.fromEntries(
  Object.entries(UF_NOME).map(([cod, nome]) => [semAcento(nome).toUpperCase().trim(), cod]),
);

export function ufAbreviacao(uf?: string | null): string {
  const raw = (uf ?? "").trim();
  if (!raw) return "SP";
  const upper2 = raw.slice(0, 2).toUpperCase();
  if (raw.length === 2 && UF_NOME[upper2]) return upper2;
  return NOME_UF[semAcento(raw).toUpperCase().trim()] ?? "SP";
}

// Tipos suportados pelo portal, copiados das tabelas "Residencial" e
// "Comercial" da documentação — acentuação e espaçamento exatamente como lá,
// porque o portal casa por string ("os nomes devem estar exatamente iguais").
// A finalidade anda colada ao tipo: "Sítio / Chácara" só existe na lista
// residencial e "Fazenda" só na comercial, então não há como escolher uma sem
// a outra. RU (rural) não é usado justamente por não ter lista de tipos.
const TIPO_CNM: Array<[RegExp, { finalidade: "RE" | "CO"; tipo: string }]> = [
  // Comercial primeiro: "casa comercial" é comércio, não casa.
  [/casa|sobrado/i, { finalidade: "CO", tipo: "Casa / Sobrado Comercial" }],
  [/sala|conjunto|escrit[óo]rio|andar/i, { finalidade: "CO", tipo: "Conj. Comercial / Sala" }],
  [/galp[ãa]o|dep[óo]sito|armaz[ée]m|industrial/i, { finalidade: "CO", tipo: "Galpão / Depósito" }],
  [/garagem|vaga|box/i, { finalidade: "CO", tipo: "Garagem" }],
  [/pr[ée]dio|edif[íi]cio|pousada|hotel|hostel/i, { finalidade: "CO", tipo: "Prédio" }],
  [/terreno|lote|[áa]rea/i, { finalidade: "CO", tipo: "Terreno comercial" }],
  [/loja|ponto|comercial/i, { finalidade: "CO", tipo: "Ponto Comercial" }],
];

const TIPO_CNM_RESIDENCIAL: Array<[RegExp, { finalidade: "RE" | "CO"; tipo: string }]> = [
  [/apartamento|apto/i, { finalidade: "RE", tipo: "Apartamento" }],
  [/cobertura/i, { finalidade: "RE", tipo: "Cobertura" }],
  [/kitnet|kitinete|studio|st[úu]dio|est[úu]dio/i, { finalidade: "RE", tipo: "Kitnet / Stúdio" }],
  [/loft/i, { finalidade: "RE", tipo: "Loft" }],
  [/flat/i, { finalidade: "RE", tipo: "Flat" }],
  [/fazenda/i, { finalidade: "CO", tipo: "Fazenda" }],
  [/ch[áa]cara|s[íi]tio|rural/i, { finalidade: "RE", tipo: "Sítio / Chácara" }],
  [/(terreno|lote)[^a-z]*(em)?[^a-z]*cond/i, { finalidade: "RE", tipo: "Terreno em Condomínio" }],
  [/terreno|lote/i, { finalidade: "RE", tipo: "Terreno / Lote" }],
  [/(casa|sobrado)[\s\S]*cond|cond[\s\S]*(casa|sobrado)/i, { finalidade: "RE", tipo: "Casa / Sobrado em Condomínio" }],
  [/casa|sobrado|resid[êe]ncia/i, { finalidade: "RE", tipo: "Casa / Sobrado" }],
];

/**
 * Traduz o tipo do Vista para o par (finalidade, tipo) do Chaves na Mão.
 * "Comercial" no texto manda no resultado: um "sobrado comercial" é comércio.
 */
export function tipoCnm(tipo?: string | null): { finalidade: "RE" | "CO"; tipo: string } {
  const t = (tipo ?? "").trim();
  if (!t) return { finalidade: "RE", tipo: "Casa / Sobrado" };
  if (/comercial|loja|ponto|galp[ãa]o|dep[óo]sito|sala|conjunto|pr[ée]dio|industrial|armaz[ée]m/i.test(t)) {
    for (const [re, v] of TIPO_CNM) if (re.test(t)) return v;
  }
  for (const [re, v] of TIPO_CNM_RESIDENCIAL) if (re.test(t)) return v;
  return { finalidade: "RE", tipo: "Casa / Sobrado" };
}

// Características → itens de área comum/privativa em português.
//
// O portal ignora silenciosamente item fora da lista dele ("itens não listados
// serão automaticamente ignorados"), então a tradução erra para o lado de
// mandar mais: item desconhecido não derruba o anúncio, item faltando custa
// filtro de busca. A origem traz dois vocabulários misturados — os termos
// nativos do VRSync que o Vista já emite em inglês (Pool, BBQ, Elevator...) e
// texto livre em português —, e os dois casam nas mesmas regras.
const AREA_COMUM: Array<[RegExp, string]> = [
  [/piscina|pool/i, "Piscina"],
  [/academia|fitness|gym/i, "Academia"],
  [/sauna/i, "Sauna"],
  [/playground/i, "Playground"],
  [/elevador|elevator/i, "Elevador"],
  [/quadra de t[êe]nis|tennis/i, "Quadra de tênis"],
  [/quadra|sports court/i, "Quadra esportiva"],
  [/sal[ãa]o de festas|party room/i, "Salão de festas"],
  [/sal[ãa]o de jogos|game room/i, "Salão de jogos"],
  [/espa[çc]o gourmet|gourmet/i, "Espaço gourmet"],
  [/churrasqueira|bbq|barbecue/i, "Churrasqueira"],
  [/portaria|seguran[çc]a 24|security guard|controlled access/i, "Portaria 24 horas"],
  [/condom[íi]nio fechado|gated community/i, "Condomínio fechado"],
  [/jardim|garden/i, "Jardim"],
  [/acessibilidade|accessib/i, "Acessibilidade"],
  [/bicicletario|bicicletário/i, "Bicicletário"],
  [/gerador|generator/i, "Gerador"],
  [/spa/i, "Spa"],
  [/lavanderia coletiva|lavanderia/i, "Lavanderia"],
];

const AREA_PRIVATIVA: Array<[RegExp, string]> = [
  [/varanda|sacada|terra[çc]o|balcony|veranda/i, "Varanda"],
  [/mobiliado|furnished/i, "Mobiliado"],
  [/ar.?condicionado|air conditioning|cooling/i, "Ar condicionado"],
  [/aquecedor|aquecimento|heating/i, "Aquecedor"],
  [/adega/i, "Adega"],
  [/closet/i, "Closet"],
  [/escrit[óo]rio|home office/i, "Escritório"],
  [/lareira|fireplace/i, "Lareira"],
  [/quintal|backyard|fenced yard/i, "Quintal"],
  [/arm[áa]rio|planejado/i, "Armários"],
  [/interfone|intercom/i, "Interfone"],
  [/vista para o mar|ocean view/i, "Vista para o mar"],
  [/despensa/i, "Despensa"],
  [/[áa]rea de servi[çc]o|laundry/i, "Área de serviço"],
  [/quarto de empregada|maids quarters/i, "Dependência de empregada"],
  [/hidromassagem|banheira/i, "Hidromassagem"],
];

function traduzirItens(caracteristicas: string[] | null | undefined, mapa: Array<[RegExp, string]>): string[] {
  const out = new Set<string>();
  for (const c of caracteristicas ?? []) {
    const t = String(c ?? "").trim();
    if (!t) continue;
    for (const [re, v] of mapa) if (re.test(t)) out.add(v);
  }
  return [...out];
}

export const itensAreaComum = (c?: string[] | null) => traduzirItens(c, AREA_COMUM);
export const itensAreaPrivativa = (c?: string[] | null) => traduzirItens(c, AREA_PRIVATIVA);

// Cômodos que o portal conta mas o Vista não numera. A característica só diz
// que EXISTE, então o feed publica 1 — nunca um número inventado. Subnotificar
// (dois closets virarem "1") tira nota; superestimar seria anúncio mentiroso.
const COMODOS_POR_CARACTERISTICA: Array<[keyof ComodosDerivados, RegExp]> = [
  ["closet", /closet/i],
  ["despensa", /despensa/i],
  ["bar", /\bbar\b|adega/i],
  ["quarto_empregada", /quarto de empregada|maids quarters|depend[êe]ncia de empregada/i],
  ["escritorio", /escrit[óo]rio|home office/i],
  ["area_servico", /[áa]rea de servi[çc]o|laundry/i],
  ["lareira", /lareira|fireplace/i],
  ["varanda", /varanda|sacada|balcony|veranda/i],
];

type ComodosDerivados = {
  closet: string; despensa: string; bar: string; quarto_empregada: string;
  escritorio: string; area_servico: string; lareira: string; varanda: string;
};

export function comodosDerivados(caracteristicas?: string[] | null): ComodosDerivados {
  const base: ComodosDerivados = {
    closet: "", despensa: "", bar: "", quarto_empregada: "",
    escritorio: "", area_servico: "", lareira: "", varanda: "",
  };
  for (const c of caracteristicas ?? []) {
    const t = String(c ?? "").trim();
    if (!t) continue;
    for (const [campo, re] of COMODOS_POR_CARACTERISTICA) if (re.test(t)) base[campo] = "1";
  }
  return base;
}

export function aceitaPet(caracteristicas?: string[] | null): string {
  const tem = (caracteristicas ?? []).some((c) => /aceita (pet|animais)|pets? allowed|pet friendly/i.test(String(c ?? "")));
  return tem ? "1" : "";
}

// ---------------------------------------------------------------------------
// Higiene de texto (mesma régua do feed VRSync)
// ---------------------------------------------------------------------------

const RE_EMOJI = /[\u{1F000}-\u{1FFFF}\u{2190}-\u{2BFF}\u{FE0F}\u{2600}-\u{27BF}]/gu;
const RE_FONE_TXT = /(?:\+?55[\s.-]?)?\(?\d{2}\)?[\s.-]?9?[\s.-]?\d{4}[\s.-]?\d{4}/g;
const RE_URL_TXT = /https?:\/\/\S+|www\.\S+/gi;
const RE_EMAIL_TXT = /[\w.+-]+@[\w-]+\.[\w.]+/g;
const SIGLAS_PERMITIDAS = new Set(["IPTU", "CRECI", "MCMV", "CDHU", "ITBI", "SPDA"]);

/** Tira contato, link, emoji e CAIXA ALTA — o que portal nenhum aceita no texto. */
export function sanitizarParaPortal(texto: string, max: number): string {
  let t = texto
    .replace(/<[^>]+>/g, " ")
    .replace(RE_EMOJI, "")
    .replace(RE_URL_TXT, "")
    .replace(RE_EMAIL_TXT, "")
    .replace(RE_FONE_TXT, "")
    .replace(/[ \t]{2,}/g, " ")
    .trim();
  t = t.replace(/\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{4,}\b/g, (w) =>
    SIGLAS_PERMITIDAS.has(w) ? w : w.charAt(0) + w.slice(1).toLowerCase(),
  );
  if (t.length > max) {
    t = t.slice(0, max);
    const corte = Math.max(t.lastIndexOf(". "), t.lastIndexOf(" "));
    if (corte > max * 0.6) t = t.slice(0, corte).trim();
  }
  return t;
}

const ABREVIACOES_PORTAL: Array<[RegExp, string]> = [
  [/\baptos\b\.?/gi, "apartamentos"],
  [/\bapto\b\.?/gi, "apartamento"],
  [/\bdorms?\b\.?/gi, "dormitórios"],
  [/\bwc\b\.?/gi, "banheiro"],
  [/\bvgs\b\.?/gi, "vagas"],
  [/\bvg\b\.?/gi, "vaga"],
];

function expandirAbreviacoes(texto: string): string {
  let t = texto;
  for (const [re, sub] of ABREVIACOES_PORTAL) {
    t = t.replace(re, (m) => (/^[A-ZÁÉÍÓÚÂÊÔÃÕÇ]/.test(m) ? sub.charAt(0).toUpperCase() + sub.slice(1) : sub));
  }
  return t;
}

const JARGOES_PORTAL = [
  /[óo]tima oportunidade/i, /excelente oportunidade/i, /oportunidade [úu]nica/i,
  /n[ãa]o perca/i, /imperd[íi]vel/i, /melhor\s+\S{0,20}\s*da cidade/i,
];

function removerJargoesPortal(texto: string): string {
  const temJargao = (s: string) => JARGOES_PORTAL.some((re) => re.test(s));
  if (!temJargao(texto)) return texto;
  const partes = texto.split(/(?<=[.!?])\s+|\n/);
  if (partes.length > 1) {
    return partes.filter((p) => !temJargao(p)).join("\n").replace(/\n{3,}/g, "\n\n").trim();
  }
  let t = texto;
  for (const re of JARGOES_PORTAL) t = t.replace(new RegExp(re.source, "gi"), "");
  return t.replace(/\s{2,}/g, " ").replace(/^[\s,\-—:!]+|[\s,\-—:]+$/g, "").trim();
}

const TIPOLOGIA_INICIO_RE =
  /^(apartamento|casa|sobrado|cobertura|kitnet|kitinete|studio|st[úu]dio|est[úu]dio|flat|terreno|lote|ch[áa]cara|s[íi]tio|fazenda|sala|loja|galp[ãa]o|ponto|pr[ée]dio|edif[íi]cio|pousada|hotel|[áa]rea)\b/i;

export function textoTransacao(d: ImovelNormalizado): string {
  const f = (d.finalidade ?? "").trim();
  if (f === "Aluguel") return "para alugar";
  if (f === "Venda e Aluguel") return "à venda e para alugar";
  if (f === "Venda") return "à venda";
  return d.valor_locacao && !d.valor_venda ? "para alugar" : "à venda";
}

function tituloFallback(d: ImovelNormalizado, max: number): string {
  const local = d.bairro && d.cidade ? `${d.bairro}, ${d.cidade}` : d.bairro ?? d.cidade ?? "";
  // Sem bairro nem cidade o título fecha na tipologia: "Imóvel para alugar em"
  // (com o "em" órfão do feed antigo) é título quebrado na vitrine do portal.
  const t = local
    ? `${d.tipo ?? "Imóvel"} ${textoTransacao(d)} em ${local}`
    : `${d.tipo ?? "Imóvel"} ${textoTransacao(d)}`;
  return sanitizarParaPortal(t.replace(/\s+/g, " ").trim(), max);
}

function tituloNota10(titulo: string, d: ImovelNormalizado, max: number): string {
  let t = expandirAbreviacoes(titulo.trim());
  if (/\bempreendimentos?\b/i.test(t) && d.tipo && !/empreendimento/i.test(d.tipo)) {
    t = t.replace(/\bempreendimentos?\b/gi, d.tipo);
  }
  if (!/\b(venda|vende|alug|loca[çc])/i.test(t)) {
    const transacao = textoTransacao(d);
    const m = t.match(TIPOLOGIA_INICIO_RE);
    if (m) t = `${m[0]} ${transacao}${t.slice(m[0].length)}`;
    else if (`${t}, ${transacao}`.length <= max) t = `${t}, ${transacao}`;
  }
  return sanitizarParaPortal(removerJargoesPortal(t), max);
}

function descricaoFallback(d: ImovelNormalizado, base: string): string {
  const linhas: string[] = [];
  const abertura = base.trim();
  if (abertura) linhas.push(abertura, "");
  const local = d.bairro
    ? `no bairro ${d.bairro}${d.cidade ? `, ${d.cidade}` : ""}`
    : d.cidade ? `em ${d.cidade}` : "";
  linhas.push(`${d.tipo ?? "Imóvel"} ${textoTransacao(d)} ${local}.`.replace(/\s+/g, " ").trim());

  const detalhes: string[] = [];
  if (d.area_util) detalhes.push(`- Área útil de ${Math.round(d.area_util)} metros quadrados`);
  if (d.area_total && Math.round(d.area_total) !== Math.round(d.area_util ?? 0)) {
    detalhes.push(`- Área total de ${Math.round(d.area_total)} metros quadrados`);
  }
  if (d.dormitorios) {
    detalhes.push(
      `- ${d.dormitorios} quarto${d.dormitorios > 1 ? "s" : ""}` +
        (d.suites ? `, sendo ${d.suites} suíte${d.suites > 1 ? "s" : ""}` : ""),
    );
  }
  if (d.banheiros) detalhes.push(`- ${d.banheiros} banheiro${d.banheiros > 1 ? "s" : ""}`);
  if (d.vagas) detalhes.push(`- ${d.vagas} vaga${d.vagas > 1 ? "s" : ""} de garagem`);
  if (d.ano_construcao && d.ano_construcao > 1900) detalhes.push(`- Construção de ${Math.round(d.ano_construcao)}`);
  if (detalhes.length) linhas.push("", "Especificações do imóvel:", ...detalhes);

  const caracteristicas = (d.caracteristicas ?? []).filter(Boolean);
  if (caracteristicas.length) linhas.push("", "Diferenciais:", ...caracteristicas.map((c) => `- ${c}`));

  const custos: string[] = [];
  if (d.condominio) custos.push(`- Condomínio de R$ ${Math.round(d.condominio)} mensais`);
  if (d.iptu) custos.push(`- IPTU de R$ ${Math.round(d.iptu)}`);
  if (custos.length) linhas.push("", "Custos:", ...custos);

  if (d.bairro && d.cidade) {
    linhas.push(
      "",
      `Localização: ${d.bairro}, ${d.cidade}. Boa opção para quem procura ${d.tipo ?? "imóvel"} ` +
        `${textoTransacao(d)} em ${d.bairro} ou na região de ${d.cidade}.`,
    );
  }
  linhas.push(
    "",
    `Agende sua visita com a Jazz Imobiliária e conheça este ${d.tipo ?? "imóvel"}` +
      `${d.cidade ? ` em ${d.cidade}` : ""}.`,
  );
  return sanitizarParaPortal(linhas.join("\n"), CNM_DESC_MAX);
}

export function tituloParaCnm(d: ImovelNormalizado, tituloIa?: string | null): string {
  let titulo = sanitizarParaPortal(tituloIa ?? d.titulo ?? "", CNM_TITULO_MAX);
  if (titulo.length < 10) titulo = tituloFallback(d, CNM_TITULO_MAX);
  return tituloNota10(titulo, d, CNM_TITULO_MAX);
}

export function descricaoParaCnm(d: ImovelNormalizado, descricaoIa?: string | null): string {
  const bruta = sanitizarParaPortal(descricaoIa ?? d.descricao ?? "", CNM_DESC_MAX);
  const descricao = removerJargoesPortal(expandirAbreviacoes(bruta));
  // Descrição curta rende mal em busca; abaixo de 900 caracteres a ficha
  // técnica completa o texto, como no feed do Zap.
  return descricao.length < 900 ? descricaoFallback(d, descricao) : descricao;
}

// ---------------------------------------------------------------------------
// Endereço, mídia e datas
// ---------------------------------------------------------------------------

/** Logradouro sem número e sem faixa de numeração do CRM ("Rua X - de 100 a 200"). */
export function enderecoPublico(d: ImovelNormalizado): string {
  if (!d.endereco) return (d.endereco_viacep ?? "").trim();
  const limpo = d.endereco
    .replace(/\s*[-–]?\s*\b(?:de|at[ée]|do\s+km)\s+\d[\d/]*\b.*$/i, "")
    .replace(/,?\s*\d+\s*$/, "")
    .trim();
  const viacep = (d.endereco_viacep ?? "").trim();
  if (limpo.length === 0) return viacep;
  if (/^[a-zà-ÿ]$/i.test(limpo)) return viacep;
  if (/^(um|dois|tr[êe]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|treze|catorze|quatorze|quinze|dezesseis|dezessete|dezoito|dezenove|vinte|trinta)$/i.test(limpo)) {
    return viacep;
  }
  return limpo;
}

function numeroPublicoEstavel(codigo: string): number {
  let h = 0;
  for (const c of `${codigo}:numero-publico`) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return (h % 899) + 101;
}

/**
 * Número de rua publicado: sorteado, estável por imóvel e nunca o real —
 * mesma decisão do feed VRSync (11/08), para não expor o endereço exato do
 * cliente e ainda assim entregar endereço completo ao portal.
 */
export function numeroParaPortal(codigo: string, numeroReal?: string | null): string {
  const real = (numeroReal ?? "").toString().replace(/\D/g, "");
  let n = numeroPublicoEstavel(codigo);
  if (real && String(n) === real) n = ((n - 101 + 1) % 899) + 101;
  return String(n);
}

export function separarFotosCnm(fotos?: string[] | null): { imagens: string[]; descartadas: string[] } {
  const imagens: string[] = [];
  const descartadas: string[] = [];
  for (const f of fotos ?? []) {
    if (RE_URL_VIDEO.test(f)) continue;
    if (RE_FOTO_CNM.test(f)) imagens.push(f);
    else descartadas.push(f); // PNG cai aqui: o Chaves na Mão não processa PNG.
  }
  return { imagens, descartadas };
}

/**
 * Vídeo: só YouTube, só link de navegador. A documentação é explícita —
 * "link do vídeo do Youtube (...) não pode ser utilizado embed" —, então
 * Vimeo, Shorts e /embed/ ficam de fora em vez de virar tag recusada.
 */
export function videoCnm(url?: string | null): string {
  if (!url) return "";
  const m = String(url).match(/https?:\/\/[^\s<>"']+/);
  if (!m) return "";
  let u: URL;
  try {
    u = new URL(m[0]);
  } catch {
    return "";
  }
  if (!/^https?:$/.test(u.protocol)) return "";
  const host = u.hostname.replace(/^www\./, "").toLowerCase();
  if (host === "youtu.be") return u.pathname.length > 1 ? u.toString() : "";
  if (!/(^|\.)youtube\.com$/.test(host)) return "";
  if (/\/shorts\/|\/embed\//i.test(u.pathname)) return "";
  return u.pathname === "/watch" && u.searchParams.get("v") ? u.toString() : "";
}

/** Tour 360 de verdade: link que não seja vídeo. YouTube/Vimeo é vídeo, não tour. */
export function tourCnm(url?: string | null): string {
  if (!url) return "";
  const texto = String(url).trim();
  let u: URL;
  try {
    u = new URL(texto);
  } catch {
    return "";
  }
  if (!/^https?:$/.test(u.protocol)) return "";
  return RE_URL_VIDEO.test(texto) ? "" : texto;
}

/** Formato de data/hora pedido pelo portal: AAAA-MM-DD HH:MM:SS. */
export function dataCnm(iso?: string | null): string {
  const d = iso ? new Date(iso) : new Date();
  if (Number.isNaN(d.getTime())) return "";
  return d.toISOString().slice(0, 19).replace("T", " ");
}

// ---------------------------------------------------------------------------
// Emissão
// ---------------------------------------------------------------------------

const esc = (s: unknown) =>
  String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const cdata = (s: unknown) => `<![CDATA[${String(s ?? "").replace(/\]\]>/g, "]] >")}]]>`;

const numero = (v?: number | null): string => (v && Number(v) > 0 ? String(Math.round(Number(v))) : "");

const inteiro = (v?: number | null): string =>
  v != null && Number.isFinite(Number(v)) && Number(v) > 0 && Number(v) <= 40 ? String(Math.round(Number(v))) : "";

export type Transacoes = {
  transacao: "V" | "L";
  transacao2: "" | "V" | "L";
  valor: string;
  valor_locacao: string;
  periodo_locacao: string;
};

/**
 * `valor` carrega a venda quando o imóvel tem as duas transações — é o que a
 * documentação manda ("caso possua dois tipos de transações, este campo deve
 * ser utilizado para informar o valor de venda"). Em locação pura, o valor de
 * locação vai em `valor`, e `periodo_locacao = 1` (por mês).
 */
export function transacoesCnm(d: ImovelNormalizado): Transacoes {
  const f = (d.finalidade ?? "").trim();
  const venda = Number(d.valor_venda) > 0;
  const locacao = Number(d.valor_locacao) > 0;
  const ambos = (f === "Venda e Aluguel" || (!f && venda && locacao)) && venda && locacao;
  if (ambos) {
    return {
      transacao: "V", transacao2: "L",
      valor: numero(d.valor_venda), valor_locacao: numero(d.valor_locacao), periodo_locacao: "1",
    };
  }
  const soLocacao = f === "Aluguel" || (!venda && locacao);
  if (soLocacao) {
    return { transacao: "L", transacao2: "", valor: numero(d.valor_locacao), valor_locacao: "", periodo_locacao: "1" };
  }
  return { transacao: "V", transacao2: "", valor: numero(d.valor_venda), valor_locacao: "", periodo_locacao: "" };
}

// Texto de IA só vale enquanto está ativo: a linha desativada fica na tabela
// (é histórico), então escolher a primeira do array publicaria texto aposentado.
function conteudoIa(linha: LinhaFeed) {
  const lista = Array.isArray(linha.feed_ai_content)
    ? linha.feed_ai_content
    : linha.feed_ai_content ? [linha.feed_ai_content] : [];
  return lista.find((ai) => ai?.ativo !== false);
}

/** Monta o bloco `<imovel>` completo — todas as tags, na ordem do documento. */
export function montarImovelCnm(linha: LinhaFeed, opcoes: OpcoesCnm = {}, destaque = false): string {
  const d = linha.dados_normalizados;
  const ai = conteudoIa(linha);
  const titulo = tituloParaCnm(d, ai?.titulo_otimizado);
  const descricao = descricaoParaCnm(d, ai?.descricao_otimizada);
  const { finalidade, tipo } = tipoCnm(d.tipo);
  const t = transacoesCnm(d);
  const { imagens } = separarFotosCnm(d.fotos);
  const fotos = imagens.slice(0, Math.min(opcoes.maxFotos ?? CNM_MAX_FOTOS, CNM_MAX_FOTOS));
  const atualizadoEm = dataCnm(linha.updated_at ?? linha.created_at);
  const comodos = comodosDerivados(d.caracteristicas);
  const logradouro = enderecoPublico(d);
  const esconder = opcoes.esconderEndereco || !logradouro;
  const cep = (d.cep ?? "").replace(/\D/g, "");
  const link = opcoes.linkTemplate ? opcoes.linkTemplate.replaceAll("{codigo}", encodeURIComponent(d.codigo)) : "";
  const comum = itensAreaComum(d.caracteristicas);
  const privativa = itensAreaPrivativa(d.caracteristicas);

  const fotosXml = fotos
    .map((url) => `        <foto>\n          <url>${esc(url)}</url>\n          <data_atualizacao>${atualizadoEm}</data_atualizacao>\n        </foto>`)
    .join("\n");
  const itensXml = (itens: string[]) =>
    itens.map((i) => `        <item>${esc(i)}</item>`).join("\n");

  return `    <imovel>
      <referencia>${esc(d.codigo)}</referencia>
      <codigo_cliente>${esc(d.codigo)}</codigo_cliente>
      <link_cliente>${esc(link)}</link_cliente>
      <titulo>${esc(titulo)}</titulo>
      <transacao>${t.transacao}</transacao>
      <transacao2>${t.transacao2}</transacao2>
      <finalidade>${finalidade}</finalidade>
      <finalidade2></finalidade2>
      <destaque>${destaque ? "1" : "0"}</destaque>
      <tipo>${esc(tipo)}</tipo>
      <tipo2></tipo2>
      <valor>${t.valor}</valor>
      <valor_locacao>${t.valor_locacao}</valor_locacao>
      <valor_iptu>${numero(d.iptu)}</valor_iptu>
      <valor_condominio>${numero(d.condominio)}</valor_condominio>
      <area_total>${numero(d.area_total)}</area_total>
      <area_util>${numero(d.area_util)}</area_util>
      <conservacao></conservacao>
      <quartos>${inteiro(d.dormitorios)}</quartos>
      <suites>${inteiro(d.suites)}</suites>
      <garagem>${inteiro(d.vagas)}</garagem>
      <banheiro>${inteiro(d.banheiros)}</banheiro>
      <closet>${comodos.closet}</closet>
      <salas></salas>
      <despensa>${comodos.despensa}</despensa>
      <bar>${comodos.bar}</bar>
      <cozinha></cozinha>
      <quarto_empregada>${comodos.quarto_empregada}</quarto_empregada>
      <escritorio>${comodos.escritorio}</escritorio>
      <area_servico>${comodos.area_servico}</area_servico>
      <lareira>${comodos.lareira}</lareira>
      <varanda>${comodos.varanda}</varanda>
      <lavanderia></lavanderia>
      <aceita_pet>${aceitaPet(d.caracteristicas)}</aceita_pet>
      <estado>${ufAbreviacao(d.uf)}</estado>
      <cidade>${esc(d.cidade ?? "")}</cidade>
      <bairro>${esc(d.bairro ?? "")}</bairro>
      <cep>${cep.length === 8 ? cep : ""}</cep>
      <endereco>${esc(logradouro.slice(0, 200))}</endereco>
      <numero>${logradouro ? numeroParaPortal(d.codigo, d.numero) : ""}</numero>
      <complemento></complemento>
      <esconder_endereco_imovel>${esconder ? "1" : "0"}</esconder_endereco_imovel>
      <descritivo>${cdata(descricao)}</descritivo>
      <fotos_imovel>
${fotosXml}
      </fotos_imovel>
      <data_atualizacao>${atualizadoEm}</data_atualizacao>
      <latitude>${d.latitude ?? ""}</latitude>
      <longitude>${d.longitude ?? ""}</longitude>
      <video>${esc(videoCnm(d.video))}</video>
      <tour_360>${esc(tourCnm(d.tour_virtual))}</tour_360>
      <area_comum>
${itensXml(comum)}
      </area_comum>
      <area_privativa>
${itensXml(privativa)}
      </area_privativa>
      <aceita_troca></aceita_troca>
      <periodo_locacao>${t.periodo_locacao}</periodo_locacao>
    </imovel>`;
}

export function montarXmlCnm(blocos: string[]): string {
  return `<?xml version="1.0" encoding="UTF-8"?>
<Document>
  <imoveis>
${blocos.join("\n")}
  </imoveis>
</Document>
`;
}

// ---------------------------------------------------------------------------
// Filtros de emissão (mesma régua do feed VRSync, para os dois portais verem
// o mesmo acervo e a auditoria valer para os dois)
// ---------------------------------------------------------------------------

const FINALIDADES_OFERTADAS = new Set(["Venda", "Aluguel", "Venda e Aluguel"]);
const PRECO_VENDA_MIN = 15_000;
const PRECO_VENDA_MAX = 150_000_000;

export function temOfertaValida(d: ImovelNormalizado): boolean {
  if (/empreendimento/i.test(d.tipo ?? "")) return false;
  const finalidade = (d.finalidade ?? "").trim();
  if (finalidade) return FINALIDADES_OFERTADAS.has(finalidade);
  return Number(d.valor_venda) > 0 || Number(d.valor_locacao) > 0;
}

/**
 * Cidade e bairro são obrigatórios na documentação do portal ("cidade SIM",
 * "bairro SIM"). Anúncio sem eles é ficha incompleta no Vista: seria recusado
 * na importação e ainda ocuparia vaga — fica de fora antes de virar XML.
 */
export function temLocalizacaoObrigatoria(d: ImovelNormalizado): boolean {
  return Boolean((d.cidade ?? "").trim() && (d.bairro ?? "").trim());
}

export function precoVendaForaDosLimites(d: ImovelNormalizado): boolean {
  const finalidade = (d.finalidade ?? "").trim();
  const vende = finalidade === "Venda" || finalidade === "Venda e Aluguel" ||
    (!finalidade && Number(d.valor_venda) > 0);
  if (!vende) return false;
  const v = Number(d.valor_venda) || 0;
  if (v <= 0) return false;
  return v < PRECO_VENDA_MIN || v > PRECO_VENDA_MAX;
}

export function temPrecoEmitivel(d: ImovelNormalizado): boolean {
  const t = transacoesCnm(d);
  return t.valor !== "";
}

function metaFotosPortal(tipo?: string | null): number {
  return /terreno|lote|comercial|sala|loja|galp[ãa]o|ponto/i.test(tipo ?? "") ? 10 : 20;
}

function dadosCompletosParaPortal(d: ImovelNormalizado): boolean {
  const temPreco = Number(d.valor_venda) > 0 || Number(d.valor_locacao) > 0;
  const temArea = Number(d.area_util) > 0 || Number(d.area_total) > 0;
  return Boolean(
    d.endereco && d.cep && d.bairro && d.cidade && temArea && temPreco &&
      d.dormitorios != null && Number(d.iptu) > 0 && Number(d.ano_construcao) > 1900 &&
      (d.caracteristicas?.length ?? 0) >= 2,
  );
}

/** Ordem da fila: book completo e ficha completa primeiro — quem sobra do teto sai por baixo. */
export function compararPrioridade(
  a: { d: ImovelNormalizado; nImgs: number },
  b: { d: ImovelNormalizado; nImgs: number },
): number {
  const nota = ({ d, nImgs }: { d: ImovelNormalizado; nImgs: number }) => {
    const book = nImgs >= metaFotosPortal(d.tipo);
    const ficha = dadosCompletosParaPortal(d);
    if (book && ficha) return 3;
    if (book) return 2;
    return ficha ? 1 : 0;
  };
  const pa = nota(a);
  const pb = nota(b);
  if (pa !== pb) return pb - pa;
  if (a.nImgs !== b.nImgs) return b.nImgs - a.nImgs;
  return String(a.d.codigo ?? "").localeCompare(String(b.d.codigo ?? ""));
}
