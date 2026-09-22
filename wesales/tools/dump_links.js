// Salva os Trigger Links (id, nome, url) capturando a resposta que a tela
// de Marketing -> Links de acionamento recebe. Somente leitura.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const PROFILE = path.resolve(__dirname, '..', '.local', 'chrome-profile');
const OUT = path.resolve(__dirname, 'links.json');

(async () => {
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: true, viewport: { width: 1400, height: 900 },
  });
  const page = ctx.pages()[0] || await ctx.newPage();

  let dados = null;
  page.on('response', async (r) => {
    if (!/\/links/.test(r.url())) return;
    try {
      const j = await r.json();
      const arr = j.links || j.data || (Array.isArray(j) ? j : null);
      if (Array.isArray(arr) && arr.length) dados = arr;
    } catch { /* nao-json */ }
  });

  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/marketing/trigger-links`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 36 && !dados; i++) {
    await page.waitForTimeout(5000); process.stdout.write('.');
  }

  if (!dados) { console.log('\nnao capturei'); await ctx.close(); process.exit(2); }
  const mapa = {};
  for (const l of dados) {
    mapa[l.name] = { id: l.id || l._id, url: l.redirectTo || l.url,
                     key: l.fieldKey || l.linkKey };
  }
  fs.writeFileSync(OUT, JSON.stringify(mapa, null, 2), 'utf8');
  console.log('\nlinks: ' + JSON.stringify(mapa, null, 1));
  await ctx.close();
  process.exit(0);
})();
