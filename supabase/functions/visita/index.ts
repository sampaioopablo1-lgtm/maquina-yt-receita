import { createClient } from "npm:@supabase/supabase-js@2";

// Visita virtual imersiva do imóvel, montada com as fotos REAIS dele.
//
// Contexto da decisão: o usuário precisa de tour virtual em TODOS os anúncios
// e não há captura 360 do acervo. Foto comum não vira esfera sem inventar
// ~83% da imagem — isso continua recusado. O que dá para entregar hoje, para
// todos, sem inventar um pixel: uma visita guiada imersiva pelas fotos
// verdadeiras, em tela cheia, com movimento e navegação por ambiente.
//
// Diretriz oficial do VirtualTourLink (developers.grupozap.com):
//   - a página deve conter APENAS o conteúdo do tour (sem cabeçalho, menu,
//     rodapé ou link de saída) — por isso esta página não tem nada disso;
//   - HTTPS com certificado válido — ok, domínio supabase.co;
//   - sem link encurtado — ok.
//
// Hierarquia dos links de tour no feed (fn_visita_publicar_no_feed):
//   1. tour de terceiro já cadastrado no Vista — nunca tocado;
//   2. panorama 360 real (rota /tour360/, Pannellum) — substitui a visita;
//   3. esta visita — o piso de cobertura para 100% do acervo.
//
// A rota /tour360/ continua servindo SÓ panorama real. Esta rota não fala
// "360" em lugar nenhum — não promete o que não é.

const esc = (s: string) =>
  String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));

function pagina(titulo: string, fotos: string[]): string {
  const dados = JSON.stringify(fotos);
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex">
<title>${esc(titulo)}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;background:#000;overflow:hidden;font-family:system-ui,sans-serif}
#palco{position:fixed;inset:0}
.cena{position:absolute;inset:0;opacity:0;transition:opacity .8s ease;overflow:hidden}
.cena.ativa{opacity:1}
.cena img{width:100%;height:100%;object-fit:cover;transform-origin:center}
.cena.ativa img{animation:kb 9s ease-in-out forwards}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.12)}}
.cena.rev img{animation-direction:reverse}
.seta{position:fixed;top:50%;transform:translateY(-50%);z-index:5;background:rgba(0,0,0,.4);
  border:none;color:#fff;font-size:28px;width:52px;height:76px;cursor:pointer;border-radius:10px}
#ant{left:12px}#prox{right:12px}
#pos{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);z-index:5;
  background:rgba(0,0,0,.55);color:#fff;padding:5px 14px;border-radius:99px;font-size:13px}
#pausa{position:fixed;bottom:16px;right:16px;z-index:5;background:rgba(0,0,0,.4);
  border:none;color:#fff;font-size:16px;padding:8px 12px;border-radius:10px;cursor:pointer}
@media (prefers-reduced-motion: reduce){.cena.ativa img{animation:none}}
</style></head><body>
<div id="palco"></div>
<button class="seta" id="ant" aria-label="Ambiente anterior">‹</button>
<button class="seta" id="prox" aria-label="Próximo ambiente">›</button>
<div id="pos"></div>
<button id="pausa" aria-label="Pausar">❘❘</button>
<script>
var F=${dados},i=0,autop=true,t=null;
var palco=document.getElementById('palco'),pos=document.getElementById('pos');
F.forEach(function(u,k){
  var d=document.createElement('div');d.className='cena'+(k%2?' rev':'');
  var m=document.createElement('img');m.loading=k<2?'eager':'lazy';m.src=u;m.alt='Ambiente '+(k+1);
  d.appendChild(m);palco.appendChild(d);
});
var cenas=palco.children;
function ir(n){
  cenas[i].classList.remove('ativa');
  i=(n+F.length)%F.length;
  var img=cenas[i].querySelector('img');
  img.style.animation='none';void img.offsetWidth;img.style.animation='';
  cenas[i].classList.add('ativa');
  pos.textContent=(i+1)+' / '+F.length;
  if((i+2)<F.length)cenas[i+1].querySelector('img').loading='eager';
}
function arma(){clearInterval(t);if(autop)t=setInterval(function(){ir(i+1)},6000)}
document.getElementById('prox').onclick=function(){ir(i+1);arma()};
document.getElementById('ant').onclick=function(){ir(i-1);arma()};
document.getElementById('pausa').onclick=function(){autop=!autop;this.textContent=autop?'❘❘':'▶';arma()};
document.addEventListener('keydown',function(e){
  if(e.key==='ArrowRight'){ir(i+1);arma()}
  if(e.key==='ArrowLeft'){ir(i-1);arma()}
});
var x0=null;
document.addEventListener('touchstart',function(e){x0=e.touches[0].clientX});
document.addEventListener('touchend',function(e){
  if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;
  if(Math.abs(dx)>40){ir(dx<0?i+1:i-1);arma()}
  x0=null;
});
ir(0);arma();
</script></body></html>`;
}

Deno.serve(async (req) => {
  const url = new URL(req.url);
  const codigo = url.pathname.split("/").filter(Boolean).pop() ?? "";
  if (!codigo || codigo === "visita") {
    return new Response("codigo do imovel ausente", { status: 400 });
  }

  const admin = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  const { data } = await admin.from("feed_properties")
    .select("dados_normalizados, ativo")
    .eq("codigo_original", codigo)
    .maybeSingle();

  const d = (data?.dados_normalizados ?? {}) as Record<string, unknown>;
  const fotos = (Array.isArray(d.fotos) ? d.fotos : []) as string[];
  if (!data?.ativo || fotos.length < 5) {
    // 5 é o mínimo de imagens que o próprio portal exige por anúncio.
    return new Response("visita nao disponivel para este imovel", { status: 404 });
  }

  const titulo = [d.tipo, d.bairro, d.cidade].filter(Boolean).join(" — ") || `Imóvel ${codigo}`;

  return new Response(pagina(String(titulo), fotos), {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Cache-Control": "public, max-age=600",
    },
  });
});
