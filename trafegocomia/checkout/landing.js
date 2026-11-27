// uso: FONTES_DIR=... node landing.js pasta_saida
// Pagina de vendas inteira em UMA imagem (1080 de largura) para por ACIMA do formulario do checkout Kiwify.
// Na coluna principal ela aparece com ~670 px no computador e ~390 no celular (medido): menor texto 44 px.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const out = path.resolve(process.argv[2]); fs.mkdirSync(out, { recursive: true });
const F = process.env.FONTES_DIR;
const cfg = JSON.parse(fs.readFileSync(path.join(__dirname, 'landing.json')));
const sec = (cls, html) => `<section class="${cls}">${html}</section>`;
const ck = t => `<div class="it"><span class="ck">✓</span><span>${t}</span></div>`;
const xx = t => `<div class="it"><span class="ck no">✕</span><span>${t}</span></div>`;
const S = [
  sec('hero', `<div class="top"><span class="brand">📢 IA</span><span class="handle">@trafegocom.ia</span></div>
    <span class="tag">PRA DONO DE NEGÓCIO</span>
    <h1>Anúncios com IA que levam <span class="k">cliente pro seu WhatsApp</span></h1>
    <p class="sub">Aprenda a usar IA no Gerenciador de Anúncios e pare de depender de agência ou do botão de impulsionar.</p>
    <div class="preco"><small>Clube Tráfego com IA</small><b>R$ 29,90</b><small>por mês · cancele quando quiser</small></div>`),
  sec('alt', `<span class="tag red">O ERRO MAIS CARO</span>
    <h2>Impulsionar post é <span class="k">deixar o botão decidir por você</span></h2>
    <div class="lista">${xx('Público no automático')}${xx('Objetivo errado: paga por quem só olha')}${xx('Um anúncio só, sem saber o que funciona')}</div>`),
  sec('', `<span class="emoji">🤖</span>
    <h2>O tráfego pago não parou de funcionar. <span class="k">Ele mudou.</span></h2>
    <p class="sub">Hoje a IA da Meta decide quem vê o seu anúncio. O que sobrou pra você é o que ela não faz sozinha: o anúncio certo, testado do jeito certo.</p>`),
  sec('alt', `<span class="tag">COMO FUNCIONA</span>
    <h2>Do pedido ao anúncio <span class="k">em 3 passos</span></h2>
    <div class="pasos">
      <div class="ps"><span class="n">1</span><span class="t">Conecte a IA ao Gerenciador<small>Uma vez só, sem escrever código</small></span></div>
      <div class="ps"><span class="n">2</span><span class="t">Peça em português<small>Como pediria pra uma pessoa</small></span></div>
      <div class="ps"><span class="n">3</span><span class="t">Revise e ative<small>Tudo nasce em pausa: nada roda sem você</small></span></div></div>`),
  sec('', `<span class="tag">EXEMPLO DE CONVERSA</span>
    <div class="chat">
      <div class="bub me"><div class="lab">Você</div>Cria uma campanha de mensagens pra minha pizzaria. R$ 10 por dia, até 3 km daqui.</div>
      <div class="bub ai"><div class="lab">IA</div>Pronto: campanha, público e 3 versões do anúncio. Tudo em pausa pra você revisar.</div>
      <div class="bub me"><div class="lab">Você</div>Qual está com o clique mais barato?</div>
      <div class="bub ai"><div class="lab">IA</div>O anúncio 2. Sugiro manter ele e pausar o 3.</div></div>
    <p class="nota">Ilustração do processo. Os valores são do seu negócio.</p>`),
  cfg.recebe.length ? sec('alt', `<span class="tag">O QUE VOCÊ RECEBE</span><h2>Dentro do <span class="k">Clube</span></h2><div class="lista">${cfg.recebe.map(ck).join('')}</div>`) : '',
  sec(cfg.recebe.length ? '' : 'alt', `<h2>É pra você <span class="k">se…</span></h2>
    <div class="lista">${ck('Você tem um negócio e vende pelo WhatsApp')}${ck('Já gastou com impulsionar e não viu retorno')}${ck('Quer anunciar sem pagar agência todo mês')}</div>
    <h2 style="margin-top:50px">Não é pra você se…</h2>
    <div class="lista">${xx('Procura dinheiro fácil sem trabalhar')}${xx('Não quer investir nada em anúncio')}</div>`),
  sec(cfg.recebe.length ? 'alt' : '', `<h2>Menos que a <span class="k">Netflix</span></h2>
    <div class="barras">
      <div class="br"><div class="r">Netflix Padrão</div><div class="tr"><div class="f" style="width:100%;background:#3f3f46">R$ 51,90</div></div></div>
      <div class="br"><div class="r">Clube Tráfego com IA</div><div class="tr"><div class="f" style="width:58%;background:#1D4ED8">R$ 29,90</div></div></div></div>
    <p class="sub">Uma você assiste. A outra te ensina a vender.<br>É <b>menos de R$ 1 por dia</b>.</p>
    <p class="nota">Netflix Padrão sem anúncios, preço de out/2026</p>`),
  sec(cfg.recebe.length ? '' : 'alt', `<span class="emoji">🛡️</span>
    <h2>7 dias pra <span class="k">testar</span></h2>
    <p class="sub">Entrou e não é pra você? Peça o reembolso em até 7 dias e recebe tudo de volta. Depois, cancela quando quiser, sem multa.</p>`),
  sec(cfg.recebe.length ? 'alt' : '', `<span class="tag">PERGUNTAS</span>
    <div class="faq"><b>Preciso saber programar?</b><p>Não. A conexão é feita uma vez e o resto é conversa em português.</p></div>
    <div class="faq"><b>Quanto preciso gastar em anúncio?</b><p>Você escolhe a verba. Dá pra começar pequeno e aumentar no que der resultado.</p></div>
    <div class="faq"><b>Como cancelo?</b><p>Quando quiser, sem multa. Nos primeiros 7 dias, com reembolso.</p></div>`),
  sec('fim', `<h2>Entre agora por <span class="k">R$ 29,90/mês</span></h2>
    <p class="sub">Pix ou cartão. Acesso imediato após o pagamento.</p>
    <div class="seta">↓ Preencha seus dados abaixo ↓</div>`),
];
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:M;font-weight:900;src:url("file://${F}/montserrat-latin-900-normal.woff2")}
@font-face{font-family:M;font-weight:800;src:url("file://${F}/montserrat-latin-800-normal.woff2")}
*{box-sizing:border-box} body{margin:0;width:1080px;background:#111827;font-family:M;color:#fff}
section{padding:110px 80px;display:flex;flex-direction:column;align-items:center;gap:40px;text-align:center;
  background:radial-gradient(circle at 50% 0%,rgba(29,78,216,.35),transparent 60%),#111827}
section.alt{background:#0b1220}
section.fim{background:linear-gradient(180deg,#111827,#1D4ED8);padding-bottom:90px}
.top{display:flex;gap:16px;align-items:center}
.brand{background:#1D4ED8;font-weight:900;font-size:44px;padding:12px 28px;border-radius:18px}
.handle{font-weight:800;font-size:44px;opacity:.85}
.tag{background:#22C55E;color:#0b1220;font-weight:900;font-size:44px;padding:12px 32px;border-radius:999px}
.tag.red{background:#EF4444;color:#fff}
h1,h2{margin:0;font-weight:900;text-transform:uppercase;letter-spacing:-2px;line-height:1.04}
h1{font-size:96px} h2{font-size:78px}
.k{color:#3B82F6}
.sub{margin:0;font-weight:800;font-size:48px;line-height:1.3;color:#E5E7EB}
.nota{margin:0;font-weight:800;font-size:44px;opacity:.6;line-height:1.25}
.preco{display:flex;flex-direction:column;background:#fff;color:#111827;border-radius:30px;padding:34px 70px}
.preco small{font-weight:800;font-size:44px} .preco b{font-size:130px;line-height:1.05}
.lista{width:100%;display:flex;flex-direction:column;gap:22px;text-align:left}
.it{display:flex;gap:26px;align-items:center;background:rgba(255,255,255,.06);border:3px solid rgba(255,255,255,.12);border-radius:26px;padding:26px 32px;font-weight:900;font-size:50px;line-height:1.2}
.ck{flex:0 0 76px;height:76px;border-radius:50%;background:#22C55E;color:#0b1220;display:flex;align-items:center;justify-content:center;font-size:44px}
.ck.no{background:#EF4444;color:#fff}
.pasos{width:100%;display:flex;flex-direction:column;gap:24px}
.ps{display:flex;gap:28px;align-items:center;background:rgba(255,255,255,.06);border:3px solid rgba(255,255,255,.14);border-radius:26px;padding:28px 34px;text-align:left}
.ps .n{flex:0 0 96px;height:96px;border-radius:50%;background:#1D4ED8;font-weight:900;font-size:56px;display:flex;align-items:center;justify-content:center}
.ps .t{font-weight:900;font-size:52px;line-height:1.15} .ps .t small{display:block;font-weight:800;font-size:44px;opacity:.75;margin-top:6px}
.chat{width:100%;display:flex;flex-direction:column;gap:24px}
.bub{border-radius:32px;padding:26px 34px;font-weight:800;font-size:46px;line-height:1.3;max-width:88%;text-align:left}
.bub .lab{font-size:44px;opacity:.7;margin-bottom:6px}
.bub.me{background:#1D4ED8;margin-left:auto} .bub.ai{background:#F3F4F6;color:#111827}
.barras{width:100%;display:flex;flex-direction:column;gap:30px;text-align:left}
.br .r{font-weight:800;font-size:46px;margin-bottom:12px}
.br .tr{height:120px;background:rgba(255,255,255,.07);border-radius:20px;overflow:hidden}
.br .f{height:100%;border-radius:20px;display:flex;align-items:center;justify-content:flex-end;padding:0 30px;font-weight:900;font-size:64px}
.emoji{font-family:"Noto Color Emoji";font-size:170px;line-height:1}
.faq{width:100%;text-align:left;background:rgba(255,255,255,.06);border-radius:26px;padding:32px 36px}
.faq b{font-weight:900;font-size:52px} .faq p{margin:10px 0 0;font-weight:800;font-size:46px;line-height:1.3;color:#D1D5DB}
.seta{background:#22C55E;color:#0b1220;font-weight:900;font-size:56px;padding:26px 50px;border-radius:999px}
</style></head><body>${S.join('')}</body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const tmp = path.join(out, '_landing.html'); fs.writeFileSync(tmp, html);
  await p.goto('file://' + tmp); await p.evaluate(() => document.fonts.ready);
  const H = await p.evaluate(() => document.body.scrollHeight);
  await p.screenshot({ path: path.join(out, 'landing-inteira.jpg'), fullPage: true, type: 'jpeg', quality: 86 });
  // a mesma pagina em pedacos (para o caso de a Kiwify limitar altura ou peso de uma imagem)
  const cortes = await p.evaluate(() => [...document.querySelectorAll('section')].map(s => [s.offsetTop, s.offsetHeight]));
  let i = 0, y0 = 0, acc = 0;
  for (const [y, h] of cortes) {
    if (acc + h > 2600 && acc > 0) { await p.screenshot({ path: path.join(out, `landing-parte-${++i}.jpg`), clip: { x: 0, y: y0, width: 1080, height: acc }, fullPage: true, type: 'jpeg', quality: 86 }); y0 = y; acc = 0; }
    acc += h;
  }
  await p.screenshot({ path: path.join(out, `landing-parte-${++i}.jpg`), clip: { x: 0, y: y0, width: 1080, height: acc }, fullPage: true, type: 'jpeg', quality: 86 });
  fs.unlinkSync(tmp); await b.close();
  console.log('altura', H, 'partes', i);
})();
