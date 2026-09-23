// Troca a localizacao da reuniao do calendario "Reuniao com closer" para Google Meet e salva.
// Pedido do dono (23/09/2026): o evento gerado precisa ter link do Google Meet.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'),
    { headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu', '--disable-extensions'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  const txt = async () => { let t = ''; for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n'; return t; };
  const foto = async (n) => { await page.screenshot({ path: path.join(LOCAL, 'meet-' + n + '.png') }); };
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/calendars`, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 30; i++) { await page.waitForTimeout(4000); if ((await txt()).length > 2500) break; }
  await page.waitForTimeout(4000);
  await page.mouse.click(1413, 304);
  await page.waitForTimeout(12000);
  if (!/Editar - Reunião com closer/.test(await txt())) { console.log('NAO ABRIU o calendario certo'); await ctx.close(); process.exit(2); }
  for (const f of page.frames()) { const l = f.getByText(/Equipe e localização/i).first(); if (await l.count().catch(() => 0)) { await l.click({ force: true }).catch(() => {}); break; } }
  await page.waitForTimeout(6000);
  await page.mouse.click(1277, 457); await page.waitForTimeout(3000);
  await foto('dd');
  { let ok = false; for (const f of page.frames()) { const l = f.getByText('Google Meet', { exact: true }).first(); if (await l.count().catch(() => 0)) { await l.click({ force: true }); ok = true; break; } } console.log('clicou Meet:', ok); if (!ok) { await ctx.close(); process.exit(4); } }
  await page.waitForTimeout(4000);
  await foto('0');
  const t0 = await txt();
  console.log('ANTES DE SALVAR:', t0.split('\n').filter(l => /Google Meet|Personaliz|Localização/i.test(l)).slice(0, 8).join(' | '));
  if (!/Google Meet/.test(t0)) { console.log('Meet nao ficou selecionado — nao salvo'); await ctx.close(); process.exit(3); }
  { for (const f of page.frames()) { const b = f.getByRole('button', { name: /Salvar alterações/i }).first(); if (await b.count().catch(() => 0)) { await b.click({ force: true }); break; } } }
  await page.waitForTimeout(8000);
  await foto('1');
  console.log('DEPOIS:', (await txt()).split('\n').filter(l => /salv|sucesso|atualiz|erro|error/i.test(l)).slice(0, 6).join(' | '));
  await ctx.close(); process.exit(0);
})();
