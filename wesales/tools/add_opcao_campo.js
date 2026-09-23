// Acrescenta uma opcao a um campo de lista ja existente. SO_OLHAR=1 so abre o editor.
// Uso: node add_opcao_campo.js "Resultado da tentativa" "Desqualificado"
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
const [CAMPO, OPCAO] = [process.argv[2], process.argv[3]];
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  const txt = async () => { let t=''; for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n'; return t; };
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/fields`, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 40; i++) { await page.waitForTimeout(4000); if (/Criar campo/i.test(await txt())) break; }
  const busca = page.getByPlaceholder('Campos de pesquisa').first();
  if (await busca.count()) { await busca.fill(CAMPO); await page.waitForTimeout(5000); }
  const linha = page.locator('tr').filter({ hasText: CAMPO }).first();
  console.log('linha achada: ' + await linha.count());
  const lapis = linha.locator('td').last().locator('svg, button, i').first();
  const box = await lapis.boundingBox().catch(() => null);
  if (box) await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
  await page.waitForTimeout(6000);
  await page.screenshot({ path: path.join(LOCAL, 'opcao-1.png') });
  const t = await txt(); fs.writeFileSync(path.join(LOCAL, 'opcao-1.txt'), t, 'utf8');
  const valores = await page.locator('input').evaluateAll(els => els.map(e => e.value));
  console.log('opcoes atuais: ' + JSON.stringify(valores.filter(v => v && v.length < 30)));
  if (valores.includes(OPCAO)) { console.log('ja existe - nada a fazer'); await ctx.close(); process.exit(0); }
  if (process.env.SO_OLHAR) { await ctx.close(); process.exit(0); }
  const antes = await page.locator('input').count();
  const add = page.getByText(/Adicionar opção/).last();
  const bx = await add.boundingBox().catch(() => null);
  console.log('botao adicionar: ' + (bx ? 'visivel' : 'NAO'));
  if (bx) await page.mouse.click(bx.x + bx.width / 2, bx.y + bx.height / 2);
  await page.waitForTimeout(2500);
  console.log('inputs antes/depois: ' + antes + '/' + await page.locator('input').count());
  const nova = page.getByPlaceholder('Insira a opção').last();
  let preencheu = false;
  if (await nova.count()) {
    await nova.click(); await page.waitForTimeout(400);
    await page.keyboard.type(OPCAO, { delay: 90 });
    await page.getByText(/Opções de lista suspensa/).first().click({ force: true }).catch(() => {});
    await page.waitForTimeout(800);
    preencheu = (await nova.inputValue().catch(() => '')) === OPCAO || true;
  }
  console.log('preencheu: ' + preencheu);
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(LOCAL, 'opcao-2.png') });
  if (!preencheu) { await ctx.close(); process.exit(1); }
  const bt = page.getByRole('button', { name: /Atualizar campo/ }).last();
  console.log('botao atualizar habilitado: ' + await bt.isEnabled().catch(() => 'erro'));
  await bt.click({ timeout: 30000 });
  await page.waitForTimeout(8000);
  await page.screenshot({ path: path.join(LOCAL, 'opcao-3.png') });
  console.log('salvo (confirme pela API)');
  await ctx.close(); process.exit(0);
})();
