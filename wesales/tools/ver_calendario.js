// So OLHA as configuracoes do calendario (notificacoes/lembretes). Nao salva.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV', CAL = '3uNQFjCEDe7b4gKZJuOZ';
const LOCAL = path.resolve(__dirname, '..', '.local');
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), { headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  const txt = async () => { let t=''; for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n'; return t; };
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/calendars`, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 30; i++) { await page.waitForTimeout(4000); if ((await txt()).length > 2500) break; }
  await page.waitForTimeout(5000);
  fs.writeFileSync(path.join(LOCAL, 'cal-0.txt'), await txt(), 'utf8');
  await page.screenshot({ path: path.join(LOCAL, 'cal-0.png') });
  await page.mouse.click(1413, 304);   // lapis de edicao da linha do calendario
  await page.waitForTimeout(12000);
  fs.writeFileSync(path.join(LOCAL, 'cal-edit.txt'), await txt(), 'utf8');
  await page.screenshot({ path: path.join(LOCAL, 'cal-edit.png') });
  for (const re of [/Notificações/i, /Lembrete/i]) {
    for (const f of page.frames()) { const l = f.getByText(re).first(); if (await l.count().catch(() => 0)) { await l.click({ force: true }).catch(() => {}); break; } }
    await page.waitForTimeout(4000);
  }
  fs.writeFileSync(path.join(LOCAL, 'cal-1.txt'), await txt(), 'utf8');
  await page.screenshot({ path: path.join(LOCAL, 'cal-1.png') });
  const t = await txt();
  console.log(t.split('\n').filter(l => /lembrete|reminder|notifica|confirma|sms|whatsapp|antes|before/i.test(l)).slice(0, 30).join(' | '));
  await ctx.close(); process.exit(0);
})();
