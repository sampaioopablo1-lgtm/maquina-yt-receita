// SO OLHA: abre "Reuniao com closer" > Equipe e localizacao e lista as opcoes
// de local da reuniao. Nao salva nada.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'),
    { headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu', '--disable-extensions'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  const txt = async () => { let t = ''; for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n'; return t; };
  const foto = async (n) => { await page.screenshot({ path: path.join(LOCAL, 'loc-' + n + '.png') }); fs.writeFileSync(path.join(LOCAL, 'loc-' + n + '.txt'), await txt(), 'utf8'); };
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/calendars`, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 30; i++) { await page.waitForTimeout(4000); if ((await txt()).length > 2500) break; }
  await page.waitForTimeout(4000);
  await page.mouse.click(1413, 304);            // lapis de edicao (mesmo ponto do ver_calendario.js)
  await page.waitForTimeout(12000);
  for (const f of page.frames()) { const l = f.getByText(/Equipe e localização/i).first(); if (await l.count().catch(() => 0)) { await l.click({ force: true }).catch(() => {}); break; } }
  await page.waitForTimeout(6000);
  await foto('0');
  await page.mouse.click(1277, 457); await page.waitForTimeout(3000); await foto('1');
  await page.keyboard.press('Escape');
  const t = await txt();
  console.log(t.split('\n').filter(l => /local|location|meet|zoom|teams|link|confer|endere|telefone|personaliz|custom|integra/i.test(l)).slice(0, 40).join(' | '));
  await ctx.close(); process.exit(0);
})();
