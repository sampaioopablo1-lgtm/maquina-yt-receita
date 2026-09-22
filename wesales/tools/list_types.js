// Lista TODAS as opcoes do seletor "Tipo de campo" lendo o DOM do menu
// (a lista rola, entao ler o innerText da pagina nao basta). NAO salva nada.
const { chromium } = require('playwright');
const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const PROFILE = path.resolve(__dirname, '..', '.local', 'chrome-profile');

async function espera(page, re, maxMs) {
  const t0 = Date.now();
  while (Date.now() - t0 < maxMs) {
    const t = await page.evaluate(() => document.body.innerText || '').catch(() => '');
    if (re.test(t)) return t;
    await page.waitForTimeout(4000); process.stdout.write('.');
  }
  return '';
}

(async () => {
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: false, viewport: { width: 1600, height: 1000 } });
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/fields`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  await espera(page, /Criar campo/i, 240000);
  await page.getByRole('button', { name: /^Criar campo$/i }).first().click({ timeout: 60000 });
  await espera(page, /Adicione ao objeto/i, 120000);
  await page.waitForTimeout(5000);
  // objeto PRIMEIRO: a lista de tipos pode depender dele
  await page.getByText(/Selecionar objeto/i).last().click({ timeout: 30000, force: true });
  await page.waitForTimeout(3500);
  await page.getByText(/^Contato$/).last().click({ timeout: 30000, force: true });
  await page.waitForTimeout(3500);
  console.log('objeto=Contato');
  await page.getByText(/^Linha única$/i).last().click({ timeout: 30000, force: true });
  await page.waitForTimeout(4000);
  // o seletor pode ser filtravel: digita para procurar um tipo de data
  await page.keyboard.type('dat', { delay: 220 }).catch(() => {});
  await page.waitForTimeout(4000);
  const filtrado = await page.evaluate(() => {
    const s = new Set();
    document.querySelectorAll('[class*="select-option"],[role="option"]')
      .forEach((e) => { const t = (e.innerText || '').trim(); if (t && t.length < 50) s.add(t); });
    return [...s];
  }).catch(() => []);
  console.log('FILTRADO POR "dat": ' + JSON.stringify(filtrado));
  await page.keyboard.press('Backspace').catch(() => {});
  await page.keyboard.press('Backspace').catch(() => {});
  await page.keyboard.press('Backspace').catch(() => {});
  await page.waitForTimeout(3000);

  // menu virtualizado: rola o container e coleta a cada passo
  const opts = await page.evaluate(async () => {
    const colher = () => {
      const set = new Set();
      document.querySelectorAll('[class*="select-option"],[role="option"]')
        .forEach((e) => {
          const t = (e.innerText || '').trim();
          if (t && t.length < 50) set.add(t);
        });
      return set;
    };
    // acha o container rolavel que contem as opcoes
    let cont = null;
    for (const e of document.querySelectorAll('div')) {
      if (e.scrollHeight > e.clientHeight + 20 && e.querySelector('[class*="select-option"],[role="option"]')) {
        cont = e; break;
      }
    }
    const todas = new Set([...colher()]);
    if (cont) {
      for (let y = 0; y < cont.scrollHeight + 400; y += 120) {
        cont.scrollTop = y;
        await new Promise((r) => setTimeout(r, 220));
        for (const t of colher()) todas.add(t);
      }
    }
    return { opts: [...todas], achouContainer: !!cont };
  }).catch(() => ({ opts: [], achouContainer: false }));

  console.log('\n--- TODAS AS OPCOES DE TIPO (' + opts.length + ') ---');
  opts.opts.forEach((o) => console.log("  " + JSON.stringify(o)));
  await ctx.close(); process.exit(0);
})();
