import { createClient, SupabaseClient } from "npm:@supabase/supabase-js@2";
import {
  compararPrioridade,
  LinhaFeed,
  montarImovelCnm,
  montarXmlCnm,
  precoVendaForaDosLimites,
  separarFotosCnm,
  temLocalizacaoObrigatoria,
  temOfertaValida,
  temPrecoEmitivel,
} from "./gerador.ts";

// Feed do portal Chaves na Mão.
//
// Lê o MESMO acervo que o feed VRSync publica (`feed_properties`, alimentada
// pelo `smart-feed-nativo`) e escreve um segundo XML, no padrão do Chaves na
// Mão. Nada aqui sincroniza o Vista: sincronização continua com uma função só,
// para não existir duas verdades sobre o que é imóvel ativo.
//
// Por que função separada, e não mais uma ação do `smart-feed-nativo`:
//
// - O incidente de 19/08 foi CPU. Precomputar 28 MB de 10 em 10 minutos
//   consumia a instância inteira. O Chaves na Mão lê o arquivo UMA vez por dia
//   ("a leitura desse arquivo é realizada 1 vez por dia"), então este feed roda
//   duas vezes por dia e não empurra o custo do outro para cima.
// - Falha isolada. Se este gerador quebrar, o feed do Grupo OLX — que é o que
//   tem contrato e vaga paga — continua subindo pelo caminho de sempre.
//
// O `index.ts` do `smart-feed-nativo` versionado no repo é bundle publicado,
// não fonte; por isso as regras de higiene de texto e de prioridade estão
// reescritas em `gerador.ts` em vez de importadas. Quando a fonte do
// smart-feed voltar ao repositório, as duas devem virar um módulo comum.

const PAGINA = 500;

function envNumero(nome: string, padrao: number): number {
  const v = Number(Deno.env.get(nome));
  return Number.isFinite(v) && v >= 0 ? Math.floor(v) : padrao;
}

const bucket = () => Deno.env.get("JAZZ_CNM_BUCKET") ?? "feeds-portais";
const objeto = () => Deno.env.get("JAZZ_CNM_OBJETO") ?? "chavesnamao.xml";
const maxListings = () => envNumero("JAZZ_CNM_MAX_LISTINGS", 3000) || Number.MAX_SAFE_INTEGER;
const minListings = () => envNumero("JAZZ_CNM_MIN_LISTINGS", 50);
const minFotos = () => envNumero("JAZZ_CNM_MIN_FOTOS", envNumero("JAZZ_FEED_MIN_FOTOS", 7));
const destaques = () => envNumero("JAZZ_CNM_DESTAQUES", 0);
const esconderEndereco = () => Deno.env.get("JAZZ_CNM_ESCONDER_ENDERECO") === "1";
const linkTemplate = () => Deno.env.get("JAZZ_CNM_LINK_TEMPLATE") ?? null;

/**
 * Bloqueios que valem para este portal.
 *
 * `feed_property_portal_publicacao` guarda as travas do feed. As do
 * `vrsync_rede` que descrevem o IMÓVEL — sumiu do XML do Vista
 * (`ausente_xml_vista`) ou é ficha duplicada (`duplicado_no_portal`) — valem
 * em qualquer portal: imóvel desativado no Vista não pode ser anunciado em
 * lugar nenhum, e mandar duplicado só rende bloqueio do outro lado.
 *
 * `fotos_abaixo_da_meta` NÃO vale aqui: aquela régua é a nota de Imagens do
 * Grupo OLX (12 fotos) num contrato de 3.000 vagas. O Chaves na Mão não
 * publica essa exigência, e derrubar anúncio por causa da régua de outro
 * portal seria jogar estoque fora de graça.
 *
 * Bloqueio manual feito por pessoa (motivo nulo) é respeitado dos dois lados —
 * quando alguém tira um imóvel do ar, tira do ar.
 */
async function bloqueios(admin: SupabaseClient): Promise<Set<string>> {
  const { data, error } = await admin
    .from("feed_property_portal_publicacao")
    .select("property_id, portal, motivo")
    .in("portal", ["chavesnamao", "vrsync_rede"])
    .eq("habilitado", false);
  if (error) throw new Error(`[cnm] falha ao ler bloqueios: ${error.message}`);
  const fora = new Set<string>();
  for (const r of data ?? []) {
    if (r.portal === "vrsync_rede" && r.motivo === "fotos_abaixo_da_meta") continue;
    fora.add(r.property_id);
  }
  return fora;
}

async function lerAcervo(admin: SupabaseClient): Promise<LinhaFeed[]> {
  const rows: LinhaFeed[] = [];
  for (let off = 0; ; off += PAGINA) {
    const { data, error } = await admin
      .from("feed_properties")
      .select(
        "id, codigo_original, dados_normalizados, created_at, updated_at, feed_ai_content(titulo_otimizado, descricao_otimizada, ativo)",
      )
      .eq("ativo", true)
      .order("codigo_original")
      .range(off, off + PAGINA - 1);
    if (error) throw new Error(`[cnm] falha ao ler feed_properties (offset ${off}): ${error.message}`);
    rows.push(...((data ?? []) as LinhaFeed[]));
    if (!data || data.length < PAGINA) break;
  }
  return rows;
}

type Resultado = { xml: string; emitidos: number; fotosDescartadas: number; semFoto: number };

async function gerar(admin: SupabaseClient): Promise<Resultado> {
  const rows = await lerAcervo(admin);
  const fora = await bloqueios(admin);

  let fotosDescartadas = 0;
  let semFoto = 0;

  const candidatos = rows
    .filter((r) => !fora.has(r.id))
    .filter((r) => temOfertaValida(r.dados_normalizados))
    .filter((r) => !precoVendaForaDosLimites(r.dados_normalizados))
    .filter((r) => temPrecoEmitivel(r.dados_normalizados))
    .filter((r) => temLocalizacaoObrigatoria(r.dados_normalizados))
    .map((r) => {
      const { imagens, descartadas } = separarFotosCnm(r.dados_normalizados.fotos);
      fotosDescartadas += descartadas.length;
      return { r, nImgs: imagens.length };
    })
    .filter(({ nImgs }) => {
      if (nImgs >= minFotos()) return true;
      semFoto += 1;
      return false;
    })
    .sort((a, b) => compararPrioridade(
      { d: a.r.dados_normalizados, nImgs: a.nImgs },
      { d: b.r.dados_normalizados, nImgs: b.nImgs },
    ))
    .slice(0, maxListings());

  const opcoes = {
    linkTemplate: linkTemplate(),
    esconderEndereco: esconderEndereco(),
    destaques: destaques(),
  };
  const blocos = candidatos.map(({ r }, i) => montarImovelCnm(r, opcoes, i < destaques()));

  // Guard de estoque: feed curto demais é sinal de leitura parcial da tabela,
  // e o portal substituiria a carga inteira por ela. Melhor devolver erro e
  // deixar o arquivo de ontem no ar do que publicar um acervo pela metade.
  if (blocos.length < minListings()) {
    throw new Error(
      `[cnm] guard de estoque mínimo: só ${blocos.length} imóvel(is) emitível(is) (< ${minListings()}) — ` +
        `feed_properties vazia/parcial; erro de propósito, para preservar a carga anterior no portal`,
    );
  }

  return { xml: montarXmlCnm(blocos), emitidos: blocos.length, fotosDescartadas, semFoto };
}

Deno.serve(async (req) => {
  const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  let acao = "";
  try {
    acao = (await req.json())?.acao ?? "";
  } catch (_e) {
    // GET/sem corpo cai no ramo de ação inválida, com a lista de ações.
  }

  try {
    if (acao === "precomputar" || acao === "prever") {
      const { xml, emitidos, fotosDescartadas, semFoto } = await gerar(admin);
      const bytes = new TextEncoder().encode(xml);

      if (acao === "prever") {
        return Response.json({
          ok: true, acao, emitidos, bytes: bytes.byteLength,
          fotos_descartadas: fotosDescartadas, sem_foto_suficiente: semFoto,
          amostra: xml.slice(xml.indexOf("<imovel>"), xml.indexOf("</imovel>") + 9),
        });
      }

      if (!xml.startsWith("<?xml") || !xml.includes("</Document>")) {
        return Response.json({ ok: false, motivo: "conteudo suspeito", bytes: bytes.byteLength }, { status: 500 });
      }

      const { error } = await admin.storage.from(bucket()).upload(objeto(), bytes, {
        contentType: "application/xml; charset=utf-8",
        upsert: true,
      });
      if (error) return Response.json({ ok: false, motivo: error.message }, { status: 500 });

      console.log(`[cnm] ${emitidos} imóveis, ${bytes.byteLength} bytes, ${fotosDescartadas} foto(s) fora do formato`);
      return Response.json({
        ok: true, emitidos, bytes: bytes.byteLength,
        fotos_descartadas: fotosDescartadas, sem_foto_suficiente: semFoto,
        objeto: `${bucket()}/${objeto()}`,
      });
    }

    return Response.json({ ok: false, motivo: "acao invalida (precomputar|prever)" }, { status: 400 });
  } catch (e) {
    console.error("[chavesnamao-feed]", e);
    return Response.json({ ok: false, erro: String(e) }, { status: 500 });
  }
});
