// Cria campo "Lista suspensa (única)" com opcoes, na pasta Additional Info.
// Uso: node create_select_field.js "<Nome>" "Op1|Op2|..."
const { chromium } = require('playwright');
const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
const nome = process.argv[2];
const opcoes = (process.argv[3] || '').split('|').filter(Boolean);

async function escolhe(page, atualRe, opRe, filtro) {
  await page.getByText(atualRe).last().click({ force: true, timeout: 30000 });
  await page.waitForTimeout(3000);
  if (filtro) { await page.keyboard.type(filtro, { delay: 200 }); await page.waitForTimeout(2500); }
  await page.getByText(opRe, { exact: true }).last().click({ force: true, timeout: 30000 });
  await page.waitForTimeout(2500);
}

(async () => {
  if (!nome || !opcoes.length) { console.log('uso: node create_select_field.js "<Nome>" "A|B"'); process.exit(1); }
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1000 } });
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/fields`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 50; i++) {
    const t = await page.evaluate(() => document.body.innerText || '').catch(() => '');
    if (/Criar campo/i.test(t)) break; await page.waitForTimeout(4000);
  }
  try {
    await page.getByRole('button', { name: /^Criar campo$/i }).first().click({ timeout: 60000 });
    await page.waitForTimeout(8000);
    await escolhe(page, /Selecionar objeto/i, /^Contato$/);
    await escolhe(page, /^Linha única$/i, /^Lista suspensa \(única\)$/, 'lis');
    await page.getByPlaceholder('Insira o nome').first().fill(nome);
    await escolhe(page, /Selecione a pasta/i, /^Additional Info$/);
    for (let i = 0; i < opcoes.length; i++) {
      if (i > 0) {
        await page.getByText(/Adicionar opção/).last().click({ force: true });
        await page.waitForTimeout(1500);
      }
      const cel = page.getByText(/^Insira a opção$/).last();
      await cel.click({ force: true, timeout: 20000 });
      await page.waitForTimeout(800);
      await page.keyboard.type(opcoes[i], { delay: 120 });
      await page.waitForTimeout(1200);
      console.log('  opção ' + opcoes[i]);
    }
  } catch (e) {
    console.log('FALHOU: ' + e.message.slice(0, 200));
    await page.screenshot({ path: path.join(LOCAL, 'falha-campo.png') });
    await ctx.close(); process.exit(2);
  }
  // linha vazia sobrando trava o botao de salvar: remove pelo icone da lixeira
  const vazias = await page.getByText(/^Insira a opção$/).count().catch(() => 0);
  if (vazias) {
    await page.evaluate(() => {
      const cel = [...document.querySelectorAll('*')].filter(e => e.childElementCount === 0 && /^Insira a opção$/.test((e.placeholder || e.innerText || '').trim())).pop()
        || [...document.querySelectorAll('input')].filter(e => e.placeholder === 'Insira a opção' && !e.value).pop();
      const linha = cel && cel.closest('tr, [role=row], .n-data-table-tr');
      const lixo = linha && linha.querySelector('svg, button, [class*=trash], [class*=delete]:last-child');
      const alvo = linha ? [...linha.querySelectorAll('button, svg, i, span')].pop() : null;
      (alvo || lixo) && (alvo || lixo).dispatchEvent(new MouseEvent('click', { bubbles: true }));
    });
    await page.waitForTimeout(1500);
    console.log('  linhas vazias antes: ' + vazias + ' / depois: ' + await page.getByText(/^Insira a opção$/).count().catch(() => -1));
  }
  await page.screenshot({ path: path.join(LOCAL, 'antes-salvar.png') });
  if (process.env.SO_OLHAR) { console.log('só olhar: não salvei'); await ctx.close(); process.exit(0); }
  await page.getByRole('button', { name: /Criar campo personalizado/i }).last().click({ timeout: 40000 });
  await page.waitForTimeout(12000);
  await page.screenshot({ path: path.join(LOCAL, 'depois-salvar.png') });
  console.log('salvo (confirme pela API)');
  await ctx.close(); process.exit(0);
})();
