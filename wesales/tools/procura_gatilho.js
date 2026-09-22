// Abre o painel de gatilhos (workflow de teste, sem salvar) e mostra o que
// aparece para cada termo buscado. Uso: node procura_gatilho.js agend schedul
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const WF = process.env.WF || 'e0792c83-8fa5-480d-a3fb-f10268507699'; // ZZ TESTE API
const LOCAL = path.resolve(__dirname, '..', '.local');
const termos = process.argv.slice(2);
async function noFrame(page, fn) {
  for (const f of page.frames()) { const r = await fn(f).catch(() => null); if (r) return r; }
  return null;
}
const txt = async (page) => {
  let t = '';
  for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + String.fromCharCode(10);
  return t;
};
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/automation/workflow/${WF}`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 50; i++) { await page.waitForTimeout(4000); if (/Adicionar novo acionador/i.test(await txt(page))) break; }
  await noFrame(page, async (f) => {
    const b = f.getByText(/Adicionar novo acionador/i).last();
    if (!(await b.count())) return null;
    await b.click({ force: true, timeout: 15000 }); return true;
  });
  await page.waitForTimeout(5000);
  let saida = '';
  for (const termo of termos) {
    await noFrame(page, async (f) => {
      const i = f.locator('input[placeholder*="esquis" i], input[placeholder*="earch" i], input[placeholder*="usca" i]').last();
      if (!(await i.count())) return null;
      await i.fill(termo); return true;
    });
    await page.waitForTimeout(3500);
    const t = await txt(page);
    const bloco = t.slice(t.search(/Adicionar acionador/i));
    saida += '### ' + termo + String.fromCharCode(10) + bloco.slice(0, 1200) + String.fromCharCode(10);
    console.log('### ' + termo + ': ' + bloco.replace(/\s+/g, ' ').slice(0, 300));
  }
  fs.writeFileSync(path.join(LOCAL, 'procura-gatilho.txt'), saida, 'utf8');
  await page.screenshot({ path: path.join(LOCAL, 'procura-gatilho.png') });
  await ctx.close(); process.exit(0);
})();
