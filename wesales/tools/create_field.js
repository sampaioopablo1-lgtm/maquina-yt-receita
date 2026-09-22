// Cria campo personalizado na tela. Os seletores do dialogo sao componentes
// Naive UI: clica-se no VALOR visivel do seletor ("Linha unica",
// "Selecionar objeto", "Selecione a pasta"), nao no rotulo.
// Objeto "Contato", pasta "Additional Info" (id gabsbU3jsUN7oIXCnYab).
// Uso: node create_field.js "<Nome>" "<Tipo na tela>" ["<placeholder>"]
const { chromium } = require('playwright');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const PROFILE = path.resolve(__dirname, '..', '.local', 'chrome-profile');
const PASTA = 'Additional Info';

async function esperaTexto(page, re, maxMs) {
  const t0 = Date.now();
  while (Date.now() - t0 < maxMs) {
    const t = await page.evaluate(() => document.body.innerText || '').catch(() => '');
    if (re.test(t)) return t;
    await page.waitForTimeout(4000); process.stdout.write('.');
  }
  return '';
}

async function abreEEscolhe(page, valorAtualRe, opcaoRe, rotulo, filtro) {
  // o valor fica sob um .hr-base-selection-overlay__wrapper que intercepta o
  // clique -> force:true clica mesmo assim.
  // a lista e virtualizada: opcoes fora da janela visivel nao existem no DOM,
  // por isso digitamos para filtrar antes de clicar.
  const gatilho = page.getByText(valorAtualRe, { exact: false }).last();
  await gatilho.scrollIntoViewIfNeeded({ timeout: 20000 }).catch(() => {});
  await gatilho.click({ timeout: 30000, force: true });
  await page.waitForTimeout(3500);
  if (filtro) {
    await page.keyboard.type(filtro, { delay: 200 }).catch(() => {});
    await page.waitForTimeout(3500);
  }
  const op = page.getByText(opcaoRe, { exact: true }).last();
  await op.click({ timeout: 30000, force: true });
  await page.waitForTimeout(2500);
  console.log('  ' + rotulo + ' escolhido');
}

(async () => {
  const nome = process.argv[2];
  const tipo = process.argv[3];
  const ph = process.argv[4] || '';
  if (!nome || !tipo) { console.log('uso: node create_field.js "<Nome>" "<Tipo>" [ph]'); process.exit(1); }

  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: process.env.HEADED ? false : true, viewport: { width: 1600, height: 1000 },
  });
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/fields`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  console.log('abrindo tela');
  await esperaTexto(page, /Criar campo/i, 240000);
  await page.getByRole('button', { name: /^Criar campo$/i }).first().click({ timeout: 60000 });
  await esperaTexto(page, /Adicione ao objeto/i, 120000);
  await page.waitForTimeout(5000);
  console.log('\ndialogo aberto');

  try {
    // 1. objeto (primeiro: em alguns casos troca as opcoes de tipo)
    await abreEEscolhe(page, /Selecionar objeto/i, /^Contato$/, 'objeto=Contato');
    // 2. tipo
    if (!/^Linha única$/i.test(tipo)) {
      // filtra pelas 3 primeiras letras do tipo para a opcao existir no DOM
      const filtro = tipo.replace(/[()|]/g, '').slice(0, 3).toLowerCase();
      await abreEEscolhe(page, /^Linha única$/i, new RegExp('^' + tipo + '$'),
                         'tipo=' + tipo, filtro);
    } else { console.log('  tipo ja e Linha única'); }
    // 3. nome
    await page.getByPlaceholder('Insira o nome').first().fill(nome);
    console.log('  nome=' + nome);
    // 4. pasta
    await abreEEscolhe(page, /Selecione a pasta/i, new RegExp('^' + PASTA + '$'), 'pasta=' + PASTA);
    // 5. placeholder
    if (ph) {
      await page.getByPlaceholder(/Forneça uma dica/i).first().fill(ph).catch(() => {});
      console.log('  placeholder=' + ph);
    }
  } catch (e) {
    console.log('FALHOU no preenchimento: ' + e.message.slice(0, 200));
    await page.screenshot({ path: path.resolve(__dirname, '..', '.local', 'falha-campo.png') });
    await ctx.close(); process.exit(2);
  }

  await page.screenshot({ path: path.resolve(__dirname, '..', '.local', 'antes-salvar.png') });
  await page.getByRole('button', { name: /Criar campo personalizado/i }).last()
    .click({ timeout: 40000 });
  console.log('salvando');
  await page.waitForTimeout(14000);
  await page.screenshot({ path: path.resolve(__dirname, '..', '.local', 'depois-salvar.png') });
  console.log('FIM (confirme pela API)');
  await ctx.close();
  process.exit(0);
})();
