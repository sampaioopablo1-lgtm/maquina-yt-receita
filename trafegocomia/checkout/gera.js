// uso: FONTES_DIR=... node gera.js pasta_saida
// Imagens dos componentes do checkout da Kiwify (Clube Trafego com IA).
// No celular o formulario vem primeiro: o que vende tem de estar nas imagens ACIMA dele.
// Netflix Padrao R$ 51,90 desde 15/10/2026 (Mobilebit/Diario da Midia). 29,90/30 = 0,997.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const out = path.resolve(process.argv[2]); fs.mkdirSync(out, { recursive: true });
const F = process.env.FONTES_DIR;
const top = `<div class="top"><span class="brand">📢 IA</span><span class="handle">@trafegocom.ia</span></div>`;
const B = [
  ['01-topo-celular', 1080, 1350, '96px', `${top}<span class="tag">CLUBE TRÁFEGO COM IA</span>
    <h1>Anúncios com IA que levam <span class="k">cliente pro seu WhatsApp</span></h1>
    <div class="card">
      <div class="it"><span class="ck">✓</span>Pra dono de negócio, sem agência</div>
      <div class="it"><span class="ck">✓</span>Você pede, a IA monta, você revisa</div>
      <div class="it"><span class="ck">✓</span>Cancele quando quiser</div></div>
    <span class="seta">↓ Preencha abaixo e entre agora</span>`],
  ['02-banner-desktop', 2000, 590, '92px', `<div class="row"><div>${top}<h1 style="margin-top:24px">Anúncios com IA que levam <span class="k">cliente pro WhatsApp</span></h1></div>
    <div style="text-align:center;flex:0 0 560px"><div class="price" style="font-size:44px">Clube por</div><div style="color:#fff;font-weight:900;font-size:120px;line-height:1;white-space:nowrap">R$ 29,90</div><div class="price" style="font-size:38px;white-space:nowrap">por mês</div><div class="price" style="font-size:34px;white-space:nowrap">cancele quando quiser</div></div></div>`],
  ['03-como-funciona', 1080, 1350, '90px', `<span class="tag">COMO FUNCIONA</span>
    <h1>Do pedido ao anúncio <span class="k">em 3 passos</span></h1>
    <div class="pasos">
      <div class="ps"><span class="n">1</span><span class="t">Conecte a IA ao Gerenciador<small>Uma vez só, sem escrever código</small></span></div>
      <div class="ps"><span class="n">2</span><span class="t">Peça em português<small>"Campanha de mensagens, R$ 10 por dia, até 3 km"</small></span></div>
      <div class="ps"><span class="n">3</span><span class="t">Revise e ative<small>Tudo nasce em pausa: quem decide é você</small></span></div></div>`],
  ['04-preco', 1080, 1080, '86px', `<h1>Menos que a <span class="k">Netflix</span></h1>
    <div class="barras">
      <div class="br"><div class="r">Netflix, plano Padrão</div><div class="tr"><div class="f" style="width:100%;background:#3f3f46">R$ 51,90</div></div></div>
      <div class="br"><div class="r">Clube Tráfego com IA</div><div class="tr"><div class="f" style="width:58%;background:#1D4ED8">R$ 29,90</div></div></div></div>
    <div class="sub">Uma você assiste. A outra te ensina a vender.</div>
    <div class="price" style="font-size:26px;opacity:.6">Netflix Padrão sem anúncios, preço de out/2026</div>`],
  ['05-garantia', 1080, 1080, '96px', `<span class="emoji">🛡️</span>
    <h1>7 dias pra <span class="k">testar</span></h1>
    <div class="sub">Entrou e não é pra você? Peça o reembolso em até 7 dias e recebe tudo de volta. Depois, cancela quando quiser, sem multa.</div>`],
  ['06-exit-popup', 1080, 1080, '104px', `<span class="tag">ESPERA</span>
    <h1>É <span class="k">menos de R$ 1</span> por dia</h1>
    <div class="sub">R$ 29,90 por mês pra aprender a anunciar com IA. E dá pra cancelar quando quiser.</div>
    <span class="cta">Quero entrar →</span>`],
];
(async () => {
  const b = await chromium.launch(); const base = fs.readFileSync(path.join(__dirname, 'bloco.html'), 'utf8');
  for (const [nome, W, H, hs, html] of B) {
    const page = base.replace('FONT900', 'file://' + F + '/montserrat-latin-900-normal.woff2')
      .replace('FONT800', 'file://' + F + '/montserrat-latin-800-normal.woff2')
      .replace('WPX', W + 'px').replace('HPX', H + 'px').replace('HSIZE', hs).replace('GLOWTOP', (H * 0.2) + 'px').replace('CONTEUDO', html);
    const tmp = path.join(out, '_tmp.html'); fs.writeFileSync(tmp, page);
    const p = await b.newPage({ viewport: { width: W, height: H } });
    await p.goto('file://' + tmp); await p.evaluate(() => document.fonts.ready);
    const sh = await p.evaluate(() => document.getElementById('wrap').scrollHeight);
    if (sh > H) console.log('ATENCAO transbordou:', nome, sh);
    await p.screenshot({ path: path.join(out, nome + '.png') }); await p.close(); fs.unlinkSync(tmp);
  }
  await b.close();
})();
