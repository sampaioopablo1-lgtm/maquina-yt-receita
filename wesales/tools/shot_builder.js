// Screenshot do CANVAS do builder: busca o workflow na lista, clica no nome
// (que abre o builder, as vezes em nova aba) e espera o canvas desenhar.
// Calibrado para maquina/internet lentas: esperas longas, uma janela so.
// Uso: node shot_builder.js "<nome>" <out.png>
const { chromium } = require('playwright');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const PROFILE = path.resolve(__dirname, '..', '.local', 'chrome-profile');
const FRAME_RE = /client-app-automation-workflows\.leadconnectorhq\.com/;

async function frameText(p) {
  const f = p.frames().find((fr) => FRAME_RE.test(fr.url()));
  if (!f) return { f: null, t: '' };
  const t = await f.evaluate(() => (document.body ? document.body.innerText : '')).catch(() => '');
  return { f, t };
}

async function waitFrame(p, maxMs, want) {
  const t0 = Date.now();
  while (Date.now() - t0 < maxMs) {
    const { f, t } = await frameText(p);
    if (f && t && t.length > 200 && !/Loading fresh data/i.test(t)) {
      if (!want || want.test(t)) return { f, t };
    }
    await p.waitForTimeout(5000);
    process.stdout.write('.');
  }
  return await frameText(p);
}

(async () => {
  const nome = process.argv[2];
  const out = path.resolve(process.argv[3]);
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: false, viewport: { width: 1600, height: 1000 },
  });
  const page = ctx.pages()[0] || await ctx.newPage();

  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/automation/workflows`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  console.log('lista');
  let { f: frame } = await waitFrame(page, 300000);
  if (!frame) { console.log('\niframe nao carregou'); await ctx.close(); process.exit(2); }

  try {
    const box = frame.getByPlaceholder(/Pesquisar|Search/i).first();
    await box.click({ timeout: 60000 });
    await box.fill(nome.slice(0, 20));
    await page.waitForTimeout(15000);
    console.log('\nbusquei');
  } catch (e) { console.log('\nsem busca: ' + e.message.slice(0, 100)); }

  const popupP = ctx.waitForEvent('page', { timeout: 60000 }).catch(() => null);
  try {
    await frame.getByText(nome, { exact: false }).first().click({ timeout: 60000 });
    console.log('cliquei no nome');
  } catch (e) { console.log('clique falhou: ' + e.message.slice(0, 120)); }

  const popup = await popupP;
  const target = popup || page;
  if (popup) console.log('abriu nova aba: ' + popup.url());
  await target.waitForTimeout(20000);

  console.log('esperando o canvas');
  const { t } = await waitFrame(target, 300000, /Gatilho|Trigger|Publicar|Rascunho|Nota|Note/i);
  console.log('\n--- CANVAS ---');
  console.log((t || '').replace(/\n{2,}/g, ' | ').slice(0, 900));

  await target.screenshot({ path: out });
  console.log('SCREENSHOT: ' + out);
  console.log('URL: ' + target.url());
  await ctx.close();
  process.exit(0);
})();
