// Adiciona o gatilho "Transcript Generated" (Tipo=Ligacoes, Direcao=Saida)
// ao W20 pela tela. SO_OLHAR=1 para so fotografar o painel sem salvar.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const WF = process.env.WF || '5fbb2e5d-88f5-4d84-a7ec-4c87c7078198';
const LOCAL = path.resolve(__dirname, '..', '.local');
const shot = (n, p) => p.screenshot({ path: path.join(LOCAL, n) });

async function noFrame(page, fn) {
  for (const f of page.frames()) { const r = await fn(f).catch(() => null); if (r) return r; }
  return null;
}
async function clica(page, re, rot) {
  const ok = await noFrame(page, async (f) => {
    const l = f.getByText(re).last();
    if (!(await l.count())) return null;
    await l.click({ force: true, timeout: 15000 }); return true;
  });
  console.log('  ' + rot + ': ' + (ok ? 'ok' : 'NAO ACHEI'));
  await page.waitForTimeout(3500);
  return !!ok;
}
async function textos(page) {
  let t = '';
  for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n';
  return t;
}

(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/automation/workflow/${WF}`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 40; i++) {
    await page.waitForTimeout(4000);
    if (/Adicionar novo acionador|Add New Trigger/i.test(await textos(page))) break;
  }
  // o workflow pode abrir no Construtor avancado, que nao tem o botao de
  // gatilho: troca para o padrao antes.
  if (/Construtor avan/i.test(await textos(page))) {
    await clica(page, /Construtor avan/i, 'abrir seletor de construtor');
    await clica(page, /^Construtor padrão$/i, 'Construtor padrão');
    await page.waitForTimeout(6000);
    await shot('w20-0-padrao.png', page);
  }
  await clica(page, /Adicionar novo acionador|Add New Trigger/i, 'abrir gatilhos');
  await noFrame(page, async (f) => {
    const i = f.locator('input[placeholder*="esquis" i], input[placeholder*="earch" i], input[placeholder*="usca" i]').last();
    if (!(await i.count())) return null;
    await i.fill('Transcri'); return true;
  });
  await page.waitForTimeout(3500);
  await shot('w20-1-busca.png', page);
  await clica(page, /^(Transcript Generated|Transcrição gerada|Transcrição Gerada)$/i, 'escolher Transcript Generated');
  await page.waitForTimeout(3000);
  await shot('w20-2-painel.png', page);
  const painel = await textos(page);
  fs.writeFileSync(path.join(LOCAL, 'w20-painel.txt'), painel, 'utf8');
  if (process.env.SO_OLHAR) { console.log('so olhar: nao salvei'); await ctx.close(); process.exit(0); }

  // Tipo = Ligacoes
  await clica(page, /^(Selecione|Select|Selecionar)$/i, 'abrir Tipo');
  await clica(page, /^(Calls|Ligações|Chamadas)$/i, 'Tipo=Ligações');
  await shot('w20-3-tipo.png', page);
  // Direcao = Saida
  await clica(page, /^(Selecione|Select|Selecionar)$/i, 'abrir Direção');
  await clica(page, /^(Outgoing|Saída|Efetuada|Enviada)$/i, 'Direção=Saída');
  await shot('w20-4-direcao.png', page);
  await clica(page, /^(Salvar acionador|Save Trigger|Salvar gatilho|Salvar)$/i, 'salvar gatilho');
  await page.waitForTimeout(6000);
  await shot('w20-5-salvo.png', page);
  await ctx.close(); process.exit(0);
})();
