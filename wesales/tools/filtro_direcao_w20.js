// Abre o gatilho do W20 e acrescenta o filtro Direcao = Saida (outbound).
// SO_OLHAR=1 para fotografar sem salvar.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const WF = process.env.WF || '5fbb2e5d-88f5-4d84-a7ec-4c87c7078198';
const LOCAL = path.resolve(__dirname, '..', '.local');
const shot = (n, p) => p.screenshot({ path: path.join(LOCAL, n) });
const txt = async (page) => {
  let t = '';
  for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + String.fromCharCode(10);
  return t;
};
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
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/automation/workflow/${WF}`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 60; i++) { await page.waitForTimeout(4000); const s = await txt(page); if (/Type is/i.test(s) && /Adicionar novo acionador|Construtor/i.test(s)) break; }
  if (/Construtor avan/i.test(await txt(page))) {
    await clica(page, /Construtor avan/i, 'seletor de construtor');
    await clica(page, /^Construtor padrão$/i, 'Construtor padrão');
    await page.waitForTimeout(6000);
  }
  await clica(page, /Type is|Transcript Generated/i, "abrir o gatilho");
  await page.waitForTimeout(3000);
  await clica(page, /Adicionar filtros/i, 'adicionar filtro');
  await page.waitForTimeout(2500);
  fs.writeFileSync(path.join(LOCAL, 'w20-filtro-painel.txt'), await txt(page), 'utf8');
  await shot('w20-6-filtro.png', page);
  // o segundo seletor vazio e o do novo filtro
  const n = await noFrame(page, async (f) => {
    const v = f.getByText(/^(Selecionar|Selecione|Select)$/);
    const c = await v.count(); if (!c) return null;
    await v.last().click({ force: true }); return c;
  });
  console.log('  seletores vazios: ' + n);
  await page.waitForTimeout(3000);
  await shot('w20-7-lista.png', page);
  fs.writeFileSync(path.join(LOCAL, 'w20-lista.txt'), await txt(page), 'utf8');
  if (process.env.SO_OLHAR) { console.log('so olhar'); await ctx.close(); process.exit(0); }
  await clica(page, /^(Direction|Direção)$/i, 'campo Direção');
  await page.waitForTimeout(2000);
  await clica(page, /^(Selecionar|Selecione|Select)$/, 'abrir valores');
  await clica(page, /^(Outgoing|Saída|Saida|Efetuada)$/i, 'valor Saída');
  await shot('w20-8-antes-salvar.png', page);
  await clica(page, /^(Salvar acionador|Save Trigger|Salvar)$/i, 'salvar');
  await page.waitForTimeout(7000);
  await shot('w20-9-salvo.png', page);
  await ctx.close(); process.exit(0);
})();
