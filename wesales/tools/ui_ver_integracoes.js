// SO OLHA: Meu perfil -> calendarios/integracoes conectadas (Google/Zoom/Teams). Nao salva.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'),
    { headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu', '--disable-extensions'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  const txt = async () => { let t = ''; for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n'; return t; };
  for (const [n, url] of [['perfil', `/v2/location/${LOC}/settings/profile`], ['calcon', `/v2/location/${LOC}/settings/calendars/connections`], ['integ', `/v2/location/${LOC}/settings/integrations/list`]]) {
    await page.goto('https://app.wesalescrm.com' + url, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
    for (let i = 0; i < 20; i++) { await page.waitForTimeout(3000); if ((await txt()).length > 2000) break; }
    await page.waitForTimeout(4000);
    await page.screenshot({ path: path.join(LOCAL, 'int-' + n + '.png') });
    const t = await txt();
    console.log('==', n, page.url().replace(/.*location\/[^/]+/, ''));
    console.log(t.split('\n').filter(l => /google|zoom|teams|outlook|conect|connect|integra|meet/i.test(l)).slice(0, 25).join(' | '));
  }
  await ctx.close(); process.exit(0);
})();
