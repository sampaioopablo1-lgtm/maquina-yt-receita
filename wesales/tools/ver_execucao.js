// So LE a aba "Registros de execucao" de um workflow. Uso: node ver_execucao.js <workflowId>
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const WF = process.argv[2];
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
  const t = await txt();
  fs.writeFileSync(path.join(LOCAL, 'execucao.txt'), t, 'utf8');
  await page.screenshot({ path: path.join(LOCAL, 'execucao.png') });
  const i = t.indexOf('Registros de execu');
  console.log(t.slice(i, i + 2500));
  await ctx.close(); process.exit(0);
})();
