import { createClient } from "npm:@supabase/supabase-js@2";

// Visita virtual imersiva do imóvel, montada com as fotos REAIS dele.
//
// v2 — parallax por profundidade (2.5D): um modelo de profundidade (MiDaS,
// Intel, open-source) roda sobre cada foto real e gera um mapa de relevo
// (fábrica: .github/workflows/fabrica-visita.yml + scripts/gerar_depths.py).
// A página projeta a foto em WebGL e move a câmera dentro dela — os pixels
// são todos da foto verdadeira; o relevo só dá profundidade ao que já está
// lá. É a técnica dos "3D photos" — nenhum cômodo inventado, ao contrário
// do outpaint 360 (que fabrica ~83% da esfera e continua recusado).
//
// O mapa mora em visitas/depths/<djb2(url)>.jpg. Foto sem mapa (ou que falhe
// no pré-carregamento CORS) cai no movimento Ken Burns sem quebrar — a
// fábrica horária vai preenchendo o acervo por ordem de valor do imóvel.
//
// Diretriz do VirtualTourLink (developers.grupozap.com): página só com o
// conteúdo do tour, HTTPS com certificado válido, sem link encurtado.
// CORS conferido em 18/08: cdn.vistahost.com.br e o Storage respondem
// access-control-allow-origin: * — o WebGL pode usar as texturas.

const esc = (s: string) =>
  String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));

const DEPTH_BASE = "https://cscczluzpblzhvojxanp.supabase.co/storage/v1/object/public/visitas/depths/";

function pagina(titulo: string, fotos: string[]): string {
  const dados = JSON.stringify(fotos);
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex">
<title>${esc(titulo)}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;background:#000;overflow:hidden;font-family:system-ui,sans-serif}
#palco{position:fixed;inset:0;transition:opacity .5s ease}
#palco.escuro{opacity:0}
canvas,#foto{position:absolute;inset:0;width:100%;height:100%}
#foto{object-fit:cover;display:none;transform-origin:center}
#foto.kb{display:block;animation:kb 9s ease-in-out forwards}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.12)}}
.seta{position:fixed;top:50%;transform:translateY(-50%);z-index:5;background:rgba(0,0,0,.4);
  border:none;color:#fff;font-size:28px;width:52px;height:76px;cursor:pointer;border-radius:10px}
#ant{left:12px}#prox{right:12px}
#pos{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);z-index:5;
  background:rgba(0,0,0,.55);color:#fff;padding:5px 14px;border-radius:99px;font-size:13px}
#pausa{position:fixed;bottom:16px;right:16px;z-index:5;background:rgba(0,0,0,.4);
  border:none;color:#fff;font-size:16px;padding:8px 12px;border-radius:10px;cursor:pointer}
</style></head><body>
<div id="palco"><canvas id="tela"></canvas><img id="foto" alt="Ambiente"></div>
<button class="seta" id="ant" aria-label="Ambiente anterior">‹</button>
<button class="seta" id="prox" aria-label="Próximo ambiente">›</button>
<div id="pos"></div>
<button id="pausa" aria-label="Pausar">❘❘</button>
<script>
var F=${dados},DB='${DEPTH_BASE}',i=0,autop=true,t=null;
function djb2(s){var h=5381;for(var k=0;k<s.length;k++){h=(Math.imul(h,33)+s.charCodeAt(k))>>>0}
  return ('0000000'+h.toString(16)).slice(-8)}
var palco=document.getElementById('palco'),tela=document.getElementById('tela'),
    foto=document.getElementById('foto'),pos=document.getElementById('pos');
var gl=tela.getContext('webgl',{antialias:false});
var prog=null,texImg=null,texDep=null,imgW=1,imgH=1,temGL=false;
if(gl){
  var sh=function(tp,src){var s=gl.createShader(tp);gl.shaderSource(s,src);gl.compileShader(s);return s};
  prog=gl.createProgram();
  gl.attachShader(prog,sh(gl.VERTEX_SHADER,
    'attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;v.y=1.-v.y;gl_Position=vec4(p,0.,1.);}'));
  gl.attachShader(prog,sh(gl.FRAGMENT_SHADER,
    'precision mediump float;varying vec2 v;uniform sampler2D I,D;uniform vec2 esc,off;'+
    'void main(){vec2 uv=(v-.5)*esc+.5;float d=texture2D(D,uv).r;'+
    'gl_FragColor=texture2D(I,uv+off*(d-.5));}'));
  gl.linkProgram(prog);gl.useProgram(prog);
  var b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);
  gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
  var lp=gl.getAttribLocation(prog,'p');gl.enableVertexAttribArray(lp);gl.vertexAttribPointer(lp,2,gl.FLOAT,false,0,0);
  texImg=gl.createTexture();texDep=gl.createTexture();temGL=true;
}
function subir(tex,un,img){gl.activeTexture(un);gl.bindTexture(gl.TEXTURE_2D,tex);
  gl.texImage2D(gl.TEXTURE_2D,0,gl.RGB,gl.RGB,gl.UNSIGNED_BYTE,img);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE)}
var mx=0,my=0,girX=0,girY=0,modo3d=false,ini=0;
function quadro(ts){
  if(modo3d&&temGL){
    if(!ini)ini=ts;var s=(ts-ini)/1000;
    tela.width=innerWidth;tela.height=innerHeight;gl.viewport(0,0,tela.width,tela.height);
    var arT=tela.width/tela.height,arI=imgW/imgH,ex,ey;
    if(arT>arI){ex=1/1.08;ey=(arI/arT)/1.08}else{ex=(arT/arI)/1.08;ey=1/1.08}
    gl.uniform2f(gl.getUniformLocation(prog,'esc'),ex,ey);
    var ax=Math.sin(s*.45)*.016+mx*.012+girY*.02, ay=Math.cos(s*.33)*.010+my*.010+girX*.02;
    gl.uniform2f(gl.getUniformLocation(prog,'off'),ax,ay);
    gl.uniform1i(gl.getUniformLocation(prog,'I'),0);gl.uniform1i(gl.getUniformLocation(prog,'D'),1);
    gl.drawArrays(gl.TRIANGLES,0,3);
  }
  requestAnimationFrame(quadro);
}
requestAnimationFrame(quadro);
addEventListener('pointermove',function(e){mx=e.clientX/innerWidth*2-1;my=e.clientY/innerHeight*2-1});
addEventListener('deviceorientation',function(e){girX=(e.beta||0)/45;girY=(e.gamma||0)/45});
function carregaImg(u){return new Promise(function(res,rej){
  var m=new Image();m.crossOrigin='anonymous';m.onload=function(){res(m)};m.onerror=rej;m.src=u})}
var vez=0;
function ir(n){
  i=(n+F.length)%F.length;pos.textContent=(i+1)+' / '+F.length;
  var minha=++vez,u=F[i];
  palco.classList.add('escuro');
  Promise.all([
    carregaImg(u).catch(function(){return null}),
    carregaImg(DB+djb2(u)+'.jpg').catch(function(){return null})
  ]).then(function(par){
    if(minha!==vez)return;
    var img=par[0],dep=par[1];
    if(img&&dep&&temGL){
      modo3d=true;foto.classList.remove('kb');foto.style.display='none';tela.style.display='block';
      imgW=img.naturalWidth;imgH=img.naturalHeight;ini=0;
      subir(texImg,gl.TEXTURE0,img);subir(texDep,gl.TEXTURE1,dep);
    }else{
      // sem mapa (ou pré-carregamento falhou): a tag <img> carrega direto,
      // sem exigência de CORS — a cena nunca fica preta
      modo3d=false;tela.style.display='none';
      foto.src=u;foto.classList.remove('kb');void foto.offsetWidth;
      foto.style.display='block';foto.classList.add('kb');
    }
    palco.classList.remove('escuro');
  });
}
function arma(){clearInterval(t);if(autop)t=setInterval(function(){ir(i+1)},7000)}
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
