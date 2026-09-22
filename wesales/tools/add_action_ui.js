// Abre o builder de um rascunho e o painel "Adicionar acao", procura uma
// acao pelo nome e descreve o que aparece. Serve para descobrir a forma
// exata de um no que a API recusa.
// Uso: node add_action_ui.js <workflowId> "<busca>"
const { chromium } = require('playwright');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const PROFILE = path.resolve(__dirname, '..', '.local', 'chrome-profile');
const FRAME_RE = /client-app-automation-workflows\.leadconnectorhq\.com/;

async function frame(page, maxMs, re) {
  const t0 = Date.now();
  while (Date.now() - t0 < maxMs) {
    const f = page.frames().find((fr) => FRAME_RE.test(fr.url()));
    if (f) {
      const t = await f.evaluate(() => (document.body ? document.body.innerText : '')).catch(() => '');
      if (t && t.length > 150 && (!re || re.test(t))) return { f, t };
    }
    await page.waitForTimeout(5000); process.stdout.write('.');
  }
  const f = page.frames().find((fr) => FRAME_RE.test(fr.url()));
  return { f, t: f ? await f.evaluate(() => document.body.innerText).catch(() => '') : '' };
}

(async () => {
  const wf = process.argv[2];
  const busca = process.argv[3] || 'oportunidade';
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: false, viewport: { width: 1600, height: 1000 },
  });
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/automation/workflow/${wf}`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});

  console.log('esperando o builder');
  let { f } = await frame(page, 300000, /Adicionar|Rascunho/i);
  if (!f) { console.log('\nsem builder'); await ctx.close(); process.exit(2); }
  await page.waitForTimeout(6000);

  try {
    await f.getByRole("button", { name: /Adicionar/ }).last().click({ timeout: 40000, force: true });
    console.log('\nabri o painel de acoes');
  } catch (e) {
    console.log('\nnao achei "Adicionar": ' + e.message.slice(0, 120));
  }
  await page.waitForTimeout(6000);

  // procura a acao
  try {
    await page.keyboard.type(busca, { delay: 180 });
    await page.waitForTimeout(5000);
  } catch { /* sem foco no campo de busca */ }

  const t = await f.evaluate(() => document.body.innerText).catch(() => '');
  console.log('--- PAINEL ---');
  console.log(t.replace(/\n{2,}/g, '\n').slice(-1800));
  await page.screenshot({ path: path.resolve(__dirname, '..', '.local', 'painel-acoes.png') });
  console.log('screenshot em .local/painel-acoes.png');
  await ctx.close();
  process.exit(0);
})();
