// Cria um Trigger Link na tela (Marketing -> Links de acionamento).
// A API interna recusa /links/ com o bearer do app de workflows.
// Uso: node create_trigger_link.js "<nome>" "<url de destino>"
const { chromium } = require('playwright');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const PROFILE = path.resolve(__dirname, '..', '.local', 'chrome-profile');
const SHOT = (n) => path.resolve(__dirname, '..', '.local', n);

async function espera(page, re, maxMs) {
  const t0 = Date.now();
  while (Date.now() - t0 < maxMs) {
    let t = await page.evaluate(() => document.body.innerText || '').catch(() => '');
    for (const f of page.frames()) {
      if (f === page.mainFrame()) continue;
      const ft = await f.evaluate(() => (document.body ? document.body.innerText : '')).catch(() => '');
      if (ft.length > t.length) t = ft;
    }
    if (re.test(t)) return t;
    await page.waitForTimeout(5000); process.stdout.write('.');
  }
  return '';
}

(async () => {
  const nome = process.argv[2];
  const destino = process.argv[3];
  if (!nome || !destino) { console.log('uso: node create_trigger_link.js "<nome>" "<url>"'); process.exit(1); }

  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: false, viewport: { width: 1600, height: 1000 },
  });
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/marketing/trigger-links`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});

  console.log('esperando a tela de links');
  await espera(page, /Add Link|Adicionar link|Trigger Links/i, 240000);
  await page.waitForTimeout(6000);

  try {
    await page.getByRole('button', { name: /Add Link|Adicionar/i }).first()
      .click({ timeout: 40000, force: true });
    console.log('\nabri o formulario');
  } catch (e) {
    console.log('\nnao achei o botao: ' + e.message.slice(0, 120));
    await page.screenshot({ path: SHOT('links-sem-botao.png') });
    await ctx.close(); process.exit(2);
  }
  await page.waitForTimeout(7000);

  // o formulario costuma ter dois campos de texto: nome e URL
  try {
    await page.getByPlaceholder(/Insira o nome/i).first().fill(nome);
    await page.getByPlaceholder(/Insira o URL do link/i).first().fill(destino);
    console.log('preenchi nome e destino');
  } catch (e) {
    console.log('falhei ao preencher: ' + e.message.slice(0, 120));
    await page.screenshot({ path: SHOT('links-form.png') });
    await ctx.close(); process.exit(3);
  }
  await page.screenshot({ path: SHOT('links-antes-salvar.png') });

  try {
    await page.getByRole('button', { name: /^(Save|Salvar|Create|Criar|Add)/i }).last()
      .click({ timeout: 40000, force: true });
    console.log('salvei');
  } catch (e) { console.log('nao achei salvar: ' + e.message.slice(0, 120)); }

  await page.waitForTimeout(12000);
  const fim = await espera(page, new RegExp(nome.slice(0, 12), 'i'), 90000);
  console.log('link aparece na lista: ' + (fim ? 'SIM' : 'nao confirmei'));
  await page.screenshot({ path: SHOT('links-depois.png') });
  await ctx.close();
  process.exit(0);
})();
