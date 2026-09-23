// So OLHA a tela de Integracoes Privadas (nao cria nada).
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  const txt = async () => { let t=''; for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n'; return t; };
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/private-integrations`, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 25; i++) { await page.waitForTimeout(4000); if ((await txt()).length > 1500) break; }
  await page.waitForTimeout(5000);
  const t = await txt();
  fs.writeFileSync(path.join(LOCAL, 'pit.txt'), t, 'utf8');
  await page.screenshot({ path: path.join(LOCAL, 'pit-0.png') });
  const i = t.search(/Integra|Private/i);
  console.log(t.slice(Math.max(0, i - 100), i + 1500));
  await ctx.close(); process.exit(0);
})();
