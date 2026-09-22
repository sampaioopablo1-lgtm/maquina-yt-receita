// Pente fino nos modulos que nao saem por API: tags, calendarios,
// formularios, links de gatilho, valores personalizados. Somente leitura.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const PROFILE = path.resolve(__dirname, '..', '.local', 'chrome-profile');
const OUT = path.resolve(__dirname, '..', '.local', 'sweep.txt');

const PAGINAS = [
  ['TAGS', `/v2/location/${LOC}/settings/tags`],
  ['VALORES PERSONALIZADOS', `/v2/location/${LOC}/settings/custom_values`],
  ['CALENDARIOS', `/v2/location/${LOC}/calendars/settings`],
  ['LINKS DE GATILHO', `/v2/location/${LOC}/marketing/trigger-links`],
  ['FORMULARIOS', `/v2/location/${LOC}/form-builder-v2/`],
];

async function texto(page, maxMs) {
  const t0 = Date.now();
  let melhor = '';
  while (Date.now() - t0 < maxMs) {
    await page.waitForTimeout(5000);
    let t = await page.evaluate(() => document.body.innerText || '').catch(() => '');
    for (const f of page.frames()) {
      if (f === page.mainFrame()) continue;
      const ft = await f.evaluate(() => (document.body ? document.body.innerText : '')).catch(() => '');
      if (ft && ft.length > t.length) t = ft;
    }
    if (t.length > melhor.length) melhor = t;
    if (melhor.length > 700 && !/Loading fresh data/i.test(melhor)) break;
    process.stdout.write('.');
  }
  return melhor;
}

(async () => {
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: true, viewport: { width: 1600, height: 1000 },
  });
  const page = ctx.pages()[0] || await ctx.newPage();
  const linhas = [];

  for (const [nome, rota] of PAGINAS) {
    console.log('\n>> ' + nome);
    await page.goto('https://app.wesalescrm.com' + rota,
      { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
    const t = await texto(page, 200000);
    // tira o menu lateral, que se repete em toda pagina
    const corte = t.indexOf('Notificações');
    const limpo = (corte > 0 ? t.slice(corte + 14) : t).replace(/\n{2,}/g, '\n').trim();
    linhas.push('===== ' + nome + ' (' + rota + ') =====\n' + limpo.slice(0, 3000) + '\n');
    console.log('   ' + limpo.slice(0, 220).replace(/\n/g, ' | '));
  }

  fs.writeFileSync(OUT, linhas.join('\n'), 'utf8');
  console.log('\nrelatorio completo em ' + OUT);
  await ctx.close();
  process.exit(0);
})();
