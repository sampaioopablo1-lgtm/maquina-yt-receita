// Abre o dialogo "Criar campo", abre o seletor de tipo e lista as opcoes.
// Depois escolhe o tipo de lista de opcao unica e fotografa o formulario.
// Somente leitura: fecha sem salvar.
const { chromium } = require('playwright');
const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1000 } });
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/fields`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 50; i++) {
    const t = await page.evaluate(() => document.body.innerText || '').catch(() => '');
    if (/Criar campo/i.test(t)) break; await page.waitForTimeout(4000);
  }
  await page.getByRole('button', { name: /^Criar campo$/i }).first().click({ timeout: 60000 });
  await page.waitForTimeout(8000);
  await page.getByText(/Selecionar objeto/i).last().click({ force: true });
  await page.waitForTimeout(3000);
  await page.getByText(/^Contato$/, { exact: true }).last().click({ force: true });
  await page.waitForTimeout(3000);
  await page.getByText(/^Linha única$/i).last().click({ force: true });
  await page.waitForTimeout(3000);
  await page.keyboard.type('lis', { delay: 200 }); await page.waitForTimeout(2500);
  await page.getByText(/^Lista suspensa \(única\)$/, { exact: true }).last().click({ force: true });
  await page.waitForTimeout(4000);
  const info = await page.evaluate(() => ({
    inputs: [...document.querySelectorAll('input,textarea')].map(e => e.placeholder).filter(Boolean),
    botoes: [...document.querySelectorAll('button,[role=button]')].map(e => e.innerText.trim()).filter(t => t && t.length < 40) }));
  console.log('FORM: ' + JSON.stringify(info));
  await page.screenshot({ path: path.join(LOCAL, 'probe-tipos.png') });
  await ctx.close(); process.exit(0);
})();
