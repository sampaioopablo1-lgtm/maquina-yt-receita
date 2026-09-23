// Abre o "Visualizar detalhes" de indice N (0 = mais recente) nos Registros de execucao.
const { chromium } = require('playwright');
const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const [WF, N] = [process.argv[2], parseInt(process.argv[3] || '5')];
const LOCAL = path.resolve(__dirname, '..', '.local');
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  const txt = async () => { let t=''; for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n'; return t; };
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/automation/workflow/${WF}`, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 40; i++) { await page.waitForTimeout(4000); if (/Registros de execu/.test(await txt())) break; }
  for (const f of page.frames()) { const l = f.getByText(/^Registros de execução$/).first(); if (await l.count().catch(() => 0)) { await l.click({ force: true }).catch(() => {}); break; } }
  await page.waitForTimeout(12000);
  for (const idx of process.argv.slice(3).map(Number)) {
    for (const f of page.frames()) {
      const l = f.getByText(/^Visualizar detalhes$/);
      if (await l.count().catch(() => 0)) { await l.nth(idx).click({ force: true }).catch(() => {}); break; }
    }
    await page.waitForTimeout(6000);
    const t = await txt();
    const i = Math.max(t.lastIndexOf('Detalhes'), 0);
    console.log('==== detalhe ' + idx + '\n' + t.slice(i, i + 1800));
    await page.screenshot({ path: path.join(LOCAL, 'execucao-det-' + idx + '.png') });
    await page.keyboard.press('Escape'); await page.waitForTimeout(2000);
  }
  await ctx.close(); process.exit(0);
})();
