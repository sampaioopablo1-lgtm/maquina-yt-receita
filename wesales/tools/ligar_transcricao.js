// Liga "Habilitar Transcrição de Chamadas" (Sistema de telefonia > Voz).
// Autorizado pelo dono em 22/09/2026 ("ative tudo, até gravação da
// transcrição"). Cobranca por minuto transcrito.
const { chromium } = require('playwright');
const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/phone_number`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  const txt = async () => await page.evaluate(() => document.body.innerText || '').catch(() => '');
  for (let i = 0; i < 40; i++) { await page.waitForTimeout(4000); if (/Voz/.test(await txt())) break; }
  await page.getByText(/^Voz$/).last().click({ force: true }).catch(() => {});
  for (let i = 0; i < 20; i++) { await page.waitForTimeout(4000); if (/Transcrição de chamada/.test(await txt())) break; }
  await page.getByText(/^Transcrição de chamada$/).last().click({ force: true }).catch(() => {});
  await page.waitForTimeout(8000);

  const estado = () => page.evaluate(() => {
    const alvo = [...document.querySelectorAll('*')].find(e => e.childElementCount === 0 &&
      /Habilitar Transcri/i.test(e.innerText || ''));
    const caixa = alvo && alvo.closest('div');
    const cb = document.querySelector('input[type=checkbox], [role=checkbox]');
    return { achou: !!alvo, marcado: cb ? (cb.checked !== undefined ? cb.checked : cb.getAttribute('aria-checked')) : null };
  });
  console.log('antes: ' + JSON.stringify(await estado()));
  await page.screenshot({ path: path.join(LOCAL, 'transc-antes.png') });

  const cb = page.locator('input[type=checkbox], [role=checkbox], .hr-checkbox').first();
  if (await cb.count()) { await cb.click({ force: true, timeout: 20000 }).catch((e) => console.log('clique: ' + e.message.slice(0, 80))); }
  else { await page.getByText(/Habilitar Transcrição de Chamadas/i).first().click({ force: true }).catch(() => {}); }
  await page.waitForTimeout(9000);
  console.log('depois: ' + JSON.stringify(await estado()));
  await page.screenshot({ path: path.join(LOCAL, 'transc-depois.png') });
  const t = await txt();
  console.log(t.split('\n').filter(l => /sucesso|success|habilitad|ativad|erro|error|falh/i.test(l)).slice(0, 6).join(' | '));
  await ctx.close(); process.exit(0);
})();
