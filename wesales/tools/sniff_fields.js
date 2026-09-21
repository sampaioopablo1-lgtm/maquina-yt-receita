// Abre a tela de Campos personalizados e grava TODOS os endpoints que ela
// chama, com origin e tamanho do bearer. Somente observa; nao cria nada.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
const PROFILE = path.join(LOCAL, 'chrome-profile');
const OUT = path.join(LOCAL, 'sniff-fields.json');

const CANDIDATAS = [
  `https://app.wesalescrm.com/v2/location/${LOC}/settings/fields`,
  `https://app.wesalescrm.com/v2/location/${LOC}/settings/custom_fields`,
  `https://app.wesalescrm.com/v2/location/${LOC}/settings/custom-fields`,
];

(async () => {
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: true, viewport: { width: 1400, height: 900 },
  });
  const page = ctx.pages()[0] || await ctx.newPage();

  const hits = [];
  ctx.on('request', (req) => {
    const u = req.url();
    if (!/leadconnectorhq\.com/.test(u)) return;
    const h = req.headers();
    hits.push({
      method: req.method(), url: u,
      origin: h['origin'] || '', referer: (h['referer'] || '').slice(0, 80),
      auth: h['authorization'] || '', authLen: (h['authorization'] || '').length,
      channel: h['channel'] || '', source: h['source'] || '', version: h['version'] || '',
    });
  });

  for (const u of CANDIDATAS) {
    hits.length = 0;
    console.log('\n>> ' + u);
    await page.goto(u, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
    for (let i = 0; i < 18; i++) { await page.waitForTimeout(5000); process.stdout.write('.'); }
    const txt = await page.evaluate(() => (document.body.innerText || '').slice(0, 200)).catch(() => '');
    console.log('\n   url final: ' + page.url());
    console.log('   tela: ' + txt.replace(/\n+/g, ' | ').slice(0, 160));
    const campo = hits.filter((h) => /field/i.test(h.url));
    console.log('   chamadas leadconnector: ' + hits.length + ' | com "field" na url: ' + campo.length);
    const vistos = new Set();
    for (const h of (campo.length ? campo : hits)) {
      const k = h.method + ' ' + h.url.split('?')[0];
      if (vistos.has(k)) continue;
      vistos.add(k);
      console.log(`     ${h.method} ${h.url.split('?')[0].slice(0, 110)}  origin=${h.origin.replace('https://', '')} auth=${h.authLen}`);
      if (vistos.size > 14) break;
    }
    if (campo.length) {
      fs.writeFileSync(OUT, JSON.stringify(campo, null, 2), 'utf8');
      console.log('   >>> detalhe salvo em ' + OUT);
      break;
    }
  }
  await ctx.close();
  process.exit(0);
})();
