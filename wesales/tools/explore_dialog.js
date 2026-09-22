// Inspeciona o DOM do dialogo "Criar campo": acha os comboboxes reais.
// NAO salva nada.
const { chromium } = require('playwright');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const PROFILE = path.resolve(__dirname, '..', '.local', 'chrome-profile');

async function esperaTexto(page, re, maxMs) {
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
    headless: false, viewport: { width: 1600, height: 1000 },
  });
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/fields`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  await esperaTexto(page, /Criar campo/i, 240000);
  await page.getByRole('button', { name: /^Criar campo$/i }).first().click({ timeout: 60000 });
  await esperaTexto(page, /Adicione ao objeto/i, 120000);
  await page.waitForTimeout(5000);

  const info = await page.evaluate(() => {
    const roles = [...document.querySelectorAll('[role]')]
      .map((e) => e.getAttribute('role'))
      .reduce((a, r) => (a[r] = (a[r] || 0) + 1, a), {});
    // acha o bloco que contem "Tipo de campo" e devolve o html dele
    let bloco = null;
    for (const e of document.querySelectorAll('div')) {
      if ((e.innerText || '').startsWith('Tipo de campo') && (e.innerText || '').length < 120) {
        bloco = e; break;
      }
    }
    const pai = bloco ? bloco.parentElement : null;
    return {
      roles,
      blocoHtml: bloco ? bloco.outerHTML.slice(0, 900) : '(nao achei)',
      paiHtml: pai ? pai.outerHTML.slice(0, 1600) : '(sem pai)',
      comboTexts: [...document.querySelectorAll('[role=combobox],[role=listbox],[aria-haspopup]')]
        .map((e) => ({ role: e.getAttribute('role'), txt: (e.innerText || '').trim().slice(0, 40),
                       cls: (e.className || '').toString().slice(0, 60) })).slice(0, 12),
    };
  }).catch((e) => ({ erro: String(e) }));

  console.log('\nROLES PRESENTES: ' + JSON.stringify(info.roles));
  console.log('\nCOMBOBOXES: ' + JSON.stringify(info.comboTexts, null, 1).slice(0, 1200));
  console.log('\nBLOCO "Tipo de campo":\n' + info.blocoHtml);
  console.log('\nPAI:\n' + (info.paiHtml || '').slice(0, 1400));

  await ctx.close();
  process.exit(0);
})();
