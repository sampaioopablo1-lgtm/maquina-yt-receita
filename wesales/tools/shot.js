// Screenshot de um workflow na tela da WeSales.
// A UI de automacoes roda num iframe cross-origin
// (client-app-automation-workflows.leadconnectorhq.com) e a lista e paginada
// (10 por pagina, ordem alfabetica) -> uso a busca da propria tela.
// Uso: node shot.js "<nome do workflow>" <out.png>
const { chromium } = require('playwright');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const PROFILE = path.resolve(__dirname, '..', '.local', 'chrome-profile');
const FRAME_RE = /client-app-automation-workflows\.leadconnectorhq\.com/;

async function frameReady(page, maxMs) {
  const t0 = Date.now();
  while (Date.now() - t0 < maxMs) {
    const f = page.frames().find((fr) => FRAME_RE.test(fr.url()));
    if (f) {
      const t = await f.evaluate(() => document.body ? document.body.innerText : '').catch(() => '');
      if (t && t.length > 300 && !/Loading fresh data/i.test(t)) return { frame: f, txt: t };
    }
    await page.waitForTimeout(5000);
    process.stdout.write('.');
  }
  return { frame: null, txt: '' };
}

(async () => {
  const nome = process.argv[2];
  const out = path.resolve(process.argv[3]);
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: false, viewport: { width: 1600, height: 1000 },
  });
  const page = ctx.pages()[0] || await ctx.newPage();

  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/automation/workflows`,
    { waitUntil: 'domcontentloaded', timeout: 120000 }).catch(() => {});

  console.log('esperando o iframe');
  let { frame } = await frameReady(page, 240000);
  if (!frame) { console.log('\nIFRAME NAO CARREGOU'); await ctx.close(); process.exit(2); }

  // busca pelo nome para escapar da paginacao
  try {
    const box = frame.getByPlaceholder(/Pesquisar|Search/i).first();
    await box.click({ timeout: 30000 });
    await box.fill(nome.slice(0, 20));
    console.log('\nbusquei por: ' + nome.slice(0, 20));
    await page.waitForTimeout(12000);
  } catch (e) {
    console.log('\nbusca indisponivel: ' + e.message.slice(0, 120));
  }

  let txt = await frame.evaluate(() => document.body.innerText).catch(() => '');
  console.log('ACHOU NA LISTA: ' + txt.includes(nome));

  try {
    const el = frame.getByText(nome, { exact: false }).first();
    await el.click({ timeout: 30000 });
    console.log('cliquei; esperando o builder desenhar');
    await page.waitForTimeout(25000);
    const r2 = await frameReady(page, 180000);
    console.log('\n--- BUILDER ---');
    console.log((r2.txt || '').replace(/\n{2,}/g, '\n').slice(0, 1000));
  } catch (e) {
    console.log('clique falhou: ' + e.message.slice(0, 180));
  }

  await page.screenshot({ path: out });
  console.log('SCREENSHOT: ' + out);
  console.log('URL: ' + page.url());
  await ctx.close();
  process.exit(0);
})();
