// Gera o roteiro do dia com Gemini e grava na tabela `videos`.
// Deployado no projeto Supabase (funcao "gerar-roteiro"). O cerebro roda no
// Supabase; o runner (Actions/Modal) renderiza o que encontrar aqui com
// status='roteirizado'. Segredo gemini_api_key vive no Vault, lido via RPC
// maquina_secret (security definer, so service_role).
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

const EIXOS = [
  "pergunta provocativa: kenapa X acontece",
  "paradoxo: tem X mas continua Y",
  "alerta de risco iminente para quem faz X",
  "comparacao entre duas escolhas de carreira",
  "realidade dura desmontada com dados",
  "habilidade ou metodo pratico que muda o jogo",
  "geracao ou grupo social sob analise",
];

const CHAVES = "kenapa, kok bisa, orang kaya, orang miskin, mental miskin, mindset, gaji, kerja, karyawan, karier, dipecat, cari kerja, uang, skill, alasan, realita, kelas sosial, biaya hidup, keuangan pribadi, pendapatan, gaya hidup, ekonomi indonesia";

function slugify(t: string): string {
  const base = t.toLowerCase().normalize("NFD").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60);
  const h = Array.from(t).reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 0).toString(16).slice(0, 6);
  return `${base}-${h}`;
}

Deno.serve(async (req: Request) => {
  const supa = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  const { data: chave, error: errSecret } = await supa.rpc("maquina_secret", { nome: "gemini_api_key" });
  if (errSecret || !chave) {
    return Response.json({ erro: "segredo gemini_api_key ausente no Vault" }, { status: 500 });
  }

  const corpo = await req.json().catch(() => ({}));
  const formato = corpo.formato === "shorts" ? "shorts" : "longo";
  const durMin = formato === "shorts" ? 0.8 : 8;
  const nCenas = formato === "shorts" ? 5 : 13;
  const tituloPedido = (corpo.titulo ?? "").trim();

  // Rotaciona o eixo pela contagem de videos ja criados (variacao estrutural).
  const { count } = await supa.from("videos").select("*", { count: "exact", head: true });
  const eixo = EIXOS[(count ?? 0) % EIXOS.length];

  const { data: publicados } = await supa.from("videos").select("titulo").not("titulo", "is", null).limit(30);
  const listaPublicados = (publicados ?? []).map((v: { titulo: string }) => `- ${v.titulo}`).join("\n") || "(nenhum)";

  const prompt = `Voce e roteirista de um canal YouTube indonesio sem rosto ("Setiap Level": dinheiro, trabalho, status e decisoes). Escreva EM INDONESIO natural e falado.

Regras: conteudo com valor proprio (dados, exemplos, tese), nunca generico; gancho concreto nos primeiros 15s; sem promessa financeira; frases com pontuacao natural.

${tituloPedido ? `Titulo do video: ${tituloPedido}` : `Crie um titulo novo usando estas palavras-chave validadas: ${CHAVES}. NAO repita temas ja usados:\n${listaPublicados}`}
Eixo estrutural OBRIGATORIO desta rodada: ${eixo}
Formato: ${formato}, ~${durMin} min, ${nCenas} cenas (cada cena = bloco auto-contido de 2-4 frases com UMA ideia).

Para cada cena, inclua prompt_visual EM INGLES no estilo do canal: "simple doodle illustration, white background, irregular hand-drawn black lines, minimal color palette (2-3 accent colors), no text" + a composicao concreta.

Responda APENAS com JSON valido:
{"titulo":"...","gancho":"...","cenas":[{"narracao":"...","prompt_visual":"..."}],"descricao":"...","tags":["..."],"prompt_thumbnail":"...","texto_thumbnail":"max 3 palavras"}`;

  const r = await fetch(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent",
    {
      method: "POST",
      headers: { "x-goog-api-key": chave, "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [{ role: "user", parts: [{ text: prompt }] }],
        generationConfig: { maxOutputTokens: 8192, responseMimeType: "application/json" },
      }),
    },
  );
  if (!r.ok) {
    return Response.json({ erro: `gemini ${r.status}`, detalhe: (await r.text()).slice(0, 300) }, { status: 502 });
  }

  const dados = await r.json();
  const texto = (dados.candidates?.[0]?.content?.parts ?? []).map((p: { text?: string }) => p.text ?? "").join("");
  let roteiro;
  try {
    roteiro = JSON.parse(texto.replace(/^```(json)?|```$/gm, "").trim());
  } catch {
    return Response.json({ erro: "gemini devolveu JSON invalido", amostra: texto.slice(0, 200) }, { status: 502 });
  }

  const cenas = (roteiro.cenas ?? []).map((c: Record<string, string>, i: number) => ({
    indice: i, narracao: c.narracao ?? "", prompt_visual: c.prompt_visual ?? "",
    audio_path: null, imagem_path: null, duracao_s: null,
  }));
  if (!cenas.length) return Response.json({ erro: "roteiro sem cenas" }, { status: 502 });

  const titulo = roteiro.titulo ?? tituloPedido;
  const slug = slugify(titulo);
  const payload = {
    slug, status: "roteirizado", formato, titulo,
    roteiro: { titulo, gancho: roteiro.gancho ?? "", cenas, descricao: roteiro.descricao ?? "", tags: roteiro.tags ?? [], prompt_thumbnail: roteiro.prompt_thumbnail ?? "", texto_thumbnail: (roteiro.texto_thumbnail ?? "").slice(0, 40) },
  };

  const { error: errIns } = await supa.from("videos").upsert(payload);
  if (errIns) return Response.json({ erro: `insert: ${errIns.message}` }, { status: 500 });

  return Response.json({ ok: true, slug, titulo, cenas: cenas.length, eixo });
});
