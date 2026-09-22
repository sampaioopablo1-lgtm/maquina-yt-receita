// Le (sem alterar) a tela Sistema telefonico: numeros e configuracoes de voz.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1100 } });
  const page = ctx.pages()[0] || await ctx.newPage();
  const api = [];
  page.on('response', async (r) => {
    const u = r.url();
    if (!/leadconnectorhq\.com/.test(u) || !/phone|number|voice|twilio|record|transcri/i.test(u)) return;
    try { api.push({ u: u.slice(0, 180), b: (await r.text()).slice(0, 3000) }); } catch {}
  });
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/phone_number`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  let t = '';
  for (let i = 0; i < 40; i++) {
    await page.waitForTimeout(4000);
    t = await page.evaluate(() => document.body.innerText || '').catch(() => '');
    if (/\+55|\+1 |Número|Numbers/.test(t) && t.length > 1500) break;
  }
  await page.waitForTimeout(5000);
  t = await page.evaluate(() => document.body.innerText || '').catch(() => '');
  await page.screenshot({ path: path.join(LOCAL, 'telefonia.png') });
  const i = t.indexOf('Sistema telef');
  fs.writeFileSync(path.join(LOCAL, 'telefonia.txt'), t + '\n\n#### API\n' + JSON.stringify(api, null, 1), 'utf8');
  console.log(t.slice(Math.max(0, t.lastIndexOf('Números') - 200)).slice(0, 2500));
  await ctx.close(); process.exit(0);
})();
