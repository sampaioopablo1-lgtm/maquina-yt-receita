// So OLHA: apps instalados, conversa de WhatsApp (Stevo) e menu lateral, atras de ligacao de WhatsApp.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  const txt = async () => { let t=''; for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n'; return t; };
  const alvos = [
    ['apps', `/v2/location/${LOC}/integration`],
    ['conv', `/v2/location/${LOC}/conversations/conversations/eEVYEzAeanIE9MtaolT7`],
  ];
  for (const [nome, url] of alvos) {
    await page.goto('https://app.wesalescrm.com' + url, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
    for (let i = 0; i < 20; i++) { await page.waitForTimeout(4000); if ((await txt()).length > 2500) break; }
    await page.waitForTimeout(8000);
    const t = await txt();
    fs.writeFileSync(path.join(LOCAL, 'cw-' + nome + '.txt'), t, 'utf8');
    await page.screenshot({ path: path.join(LOCAL, 'cw-' + nome + '.png') });
    const botoes = await page.evaluate(() => [...document.querySelectorAll('button,[role=button],a')].map(e => (e.getAttribute('aria-label') || e.title || e.innerText || '').trim()).filter(s => s && s.length < 60));
    console.log('=====', nome, t.length);
    console.log(t.split('\n').filter(l => /chamad|call|liga|stevo|whatsapp|voice|voz|discad/i.test(l)).slice(0, 30).join(' | '));
    console.log('BOTOES', [...new Set(botoes)].filter(s => /chamad|call|liga|stevo|whats|voice|voz|phone|telefone/i.test(s)).join(' | '));
  }
  await ctx.close(); process.exit(0);
})();
