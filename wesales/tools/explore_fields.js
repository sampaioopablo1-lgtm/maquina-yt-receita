// Reconhece a tela de Campos personalizados DENTRO do iframe de settings.
// Somente leitura.
const { chromium } = require('playwright');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const PROFILE = path.resolve(__dirname, '..', '.local', 'chrome-profile');
const SHOT = path.resolve(__dirname, '..', '.local', 'campos-tela.png');

(async () => {
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: false, viewport: { width: 1600, height: 1000 },
  });
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/fields`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});

  let best = null;
  for (let i = 0; i < 36; i++) {
    await page.waitForTimeout(5000);
    for (const f of page.frames()) {
      if (f === page.mainFrame()) continue;
      const t = await f.evaluate(() => (document.body ? document.body.innerText : '')).catch(() => '');
      if (t && t.length > 200) best = { f, t };
    }
    if (best && /Adicionar|Add |Pasta|Folder|campo/i.test(best.t)) break;
    process.stdout.write('.');
  }

  console.log('\nFRAMES:');
  for (const f of page.frames()) console.log('  ' + f.url().slice(0, 120));

  if (best) {
    console.log('\n--- TEXTO DO IFRAME ---');
    console.log(best.t.replace(/\n{2,}/g, '\n').slice(0, 2500));
    const botoes = await best.f.evaluate(() => {
      const out = [];
      document.querySelectorAll('button,[role=button],a').forEach((b) => {
        const t = (b.innerText || '').trim();
        if (t && t.length < 45) out.push(t);
      });
      return [...new Set(out)];
    }).catch(() => []);
    console.log('--- BOTOES DO IFRAME ---');
    console.log(botoes.join(' | ').slice(0, 900));
  } else {
    console.log('\nnenhum iframe com conteudo');
  }

  await page.screenshot({ path: SHOT });
  console.log('screenshot: ' + SHOT);
  await ctx.close();
  process.exit(0);
})();
