// So OLHA: fotografa Configuracoes > WhatsApp e procura qualquer opcao de chamada.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  const txt = async () => { let t=''; for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n'; return t; };
  for (const [nome, url] of [['wa', `/v2/location/${LOC}/settings/whatsapp`], ['int', `/v2/location/${LOC}/settings/integrations`]]) {
    await page.goto('https://app.wesalescrm.com' + url, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
    for (let i = 0; i < 15; i++) { await page.waitForTimeout(4000); if ((await txt()).length > 1500) break; }
    await page.waitForTimeout(5000);
    const t = await txt();
    fs.writeFileSync(path.join(LOCAL, 'wa-' + nome + '.txt'), t, 'utf8');
    await page.screenshot({ path: path.join(LOCAL, 'wa-' + nome + '.png') });
    console.log(nome, t.length, t.split('\n').filter(l => /chamad|call|liga|stevo|whatsapp/i.test(l)).slice(0, 25).join(' | '));
  }
  await ctx.close(); process.exit(0);
})();
