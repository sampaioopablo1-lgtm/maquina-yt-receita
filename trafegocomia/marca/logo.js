// uso: FONTES_DIR=... node logo.js pasta_saida — logo do @trafegocom.ia (o selo azul dos criativos)
const fs = require('fs'), path = require('path'); const { chromium } = require('playwright');
const out = path.resolve(process.argv[2]); fs.mkdirSync(out, { recursive: true }); const F = process.env.FONTES_DIR;
const css = `@font-face{font-family:M;font-weight:900;src:url("file://${F}/montserrat-latin-900-normal.woff2")}
@font-face{font-family:M;font-weight:800;src:url("file://${F}/montserrat-latin-800-normal.woff2")}
body{margin:0;font-family:M} .e{font-family:"Noto Color Emoji"}`;
const selo = s => `<div style="display:inline-flex;align-items:center;gap:${s*.12}px;background:#1D4ED8;color:#fff;font-weight:900;font-size:${s}px;padding:${s*.18}px ${s*.36}px;border-radius:${s*.34}px;line-height:1"><span class="e">📢</span>IA</div>`;
const L = [
  ['logo-quadrado', 1080, 1080, '#111827', `<div style="display:flex;flex-direction:column;align-items:center;gap:60px">${selo(230)}<div style="color:#fff;font-weight:900;font-size:130px;text-transform:uppercase;letter-spacing:-2px;text-align:center;line-height:1.05">Tráfego<br><span style="color:#3B82F6">com IA</span></div></div>`],
  ['logo-icone', 1080, 1080, '#111827', selo(300)],
  ['logo-horizontal', 1800, 400, '#111827', `<div style="display:flex;align-items:center;gap:50px">${selo(130)}<div style="color:#fff;font-weight:900;font-size:110px;text-transform:uppercase;letter-spacing:-2px;white-space:nowrap">Tráfego <span style="color:#3B82F6">com IA</span></div></div>`],
  ['logo-horizontal-fundo-claro', 1800, 400, '#FFFFFF', `<div style="display:flex;align-items:center;gap:50px">${selo(130)}<div style="color:#111827;font-weight:900;font-size:110px;text-transform:uppercase;letter-spacing:-2px;white-space:nowrap">Tráfego <span style="color:#1D4ED8">com IA</span></div></div>`],
];
(async () => {
  const b = await chromium.launch();
  for (const [nome, W, H, bg, html] of L) {
    for (const transp of [false, true]) {
      const t = path.join(out, '_l.html');
      fs.writeFileSync(t, `<html><head><style>${css} body{width:${W}px;height:${H}px;background:${transp ? 'transparent' : bg};display:flex;align-items:center;justify-content:center}</style></head><body>${html}</body></html>`);
      const p = await b.newPage({ viewport: { width: W, height: H } }); await p.goto('file://' + t); await p.evaluate(() => document.fonts.ready);
      await p.screenshot({ path: path.join(out, nome + (transp ? '-transparente' : '') + '.png'), omitBackground: transp }); await p.close(); fs.unlinkSync(t);
    }
  }
  await b.close();
})();
