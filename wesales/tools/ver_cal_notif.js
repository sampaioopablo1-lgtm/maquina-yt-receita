// So OLHA Calendarios > Configuracoes > Notificacoes (nao salva nada).
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), { headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  const txt = async () => { let t=''; for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n'; return t; };
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/calendars`, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 30; i++) { await page.waitForTimeout(4000); if (/Reunião com closer/.test(await txt())) break; }
  for (const re of [/^Configurações$/, /^Notificações$/]) {
    let ok = false;
    for (const f of page.frames()) { const l = f.getByText(re); const n = await l.count().catch(() => 0); for (let k = n - 1; k >= 0 && !ok; k--) { const b = await l.nth(k).boundingBox().catch(() => null); if (b && b.x > 240) { await page.mouse.click(b.x + b.width / 2, b.y + b.height / 2); ok = true; } } if (ok) break; }
    console.log('clique ' + re + ': ' + ok); await page.waitForTimeout(7000);
  }
  const t = await txt(); fs.writeFileSync(path.join(LOCAL, 'calnotif.txt'), t, 'utf8');
  await page.screenshot({ path: path.join(LOCAL, 'calnotif.png') });
  await ctx.close(); process.exit(0);
})();
