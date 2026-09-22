// Adiciona o gatilho Scheduler ao W18: seg-sex, 11:00 e 15:00.
// SO_OLHAR=1 fotografa o painel sem salvar.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const WF = process.env.WF || '63cbb270-5fc8-4c04-8c30-e5ebeaa2eb6d';
const LOCAL = path.resolve(__dirname, '..', '.local');
const shot = (n, p) => p.screenshot({ path: path.join(LOCAL, n) });
async function noFrame(page, fn) {
  for (const f of page.frames()) { const r = await fn(f).catch(() => null); if (r) return r; }
  return null;
}
const txt = async (page) => {
  let t = '';
  for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + String.fromCharCode(10);
  return t;
};
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
  for (let i = 0; i < 50; i++) {
    await page.waitForTimeout(4000);
    const s = await txt(page);
    if (/Adicionar novo acionador/i.test(s)) break;
    if (/Construtor avan/i.test(s)) {
      await clica(page, /Construtor avan/i, 'seletor de construtor');
      await clica(page, /^Construtor padrão$/i, 'Construtor padrão');
      await page.waitForTimeout(8000);
    }
  }
  if (/Construtor avan/i.test(await txt(page))) {
    await clica(page, /Construtor avan/i, 'seletor de construtor');
    await clica(page, /^Construtor padrão$/i, 'Construtor padrão');
    await page.waitForTimeout(6000);
  }
  await clica(page, /Adicionar novo acionador|Adicionar acionador/i, 'abrir gatilhos');
  await noFrame(page, async (f) => {
    const i = f.locator('input[placeholder*="esquis" i], input[placeholder*="earch" i]').last();
    if (!(await i.count())) return null;
    await i.fill('Schedul'); return true;
  });
  await page.waitForTimeout(3500);
  await clica(page, /^Scheduler$/i, 'escolher Scheduler');
  await page.waitForTimeout(4000);
  await shot('w18-1-painel.png', page);
  fs.writeFileSync(path.join(LOCAL, 'w18-painel.txt'), await txt(page), 'utf8');
  await clica(page, /^(Selecionar|Selecione|Select)$/, 'abrir Intervalo');
  await page.waitForTimeout(2500);
  fs.writeFileSync(path.join(LOCAL, 'w18-intervalos.txt'), await txt(page), 'utf8');
  await shot('w18-2-intervalos.png', page);
  await clica(page, /^Cron$/, 'Intervalo=Cron');
  await page.waitForTimeout(4000);
  await shot('w18-4-cron.png', page);
  fs.writeFileSync(path.join(LOCAL, 'w18-cron.txt'), await txt(page), 'utf8');
  const ins = await noFrame(page, async (f) => {
    const l = f.locator('.hl_trigger-panel input, aside input, input[type=text]');
    const n = await l.count(); const out = [];
    for (let i = 0; i < n; i++) out.push(await l.nth(i).evaluate(e => [e.placeholder, e.value, e.name, e.offsetParent !== null].join('|')));
    return out.length ? out : null;
  });
  console.log('inputs: ' + JSON.stringify(ins));
  if (process.env.SO_OLHAR) { console.log('so olhar: nao salvei'); await ctx.close(); process.exit(0); }
  const CRON = process.env.CRON || '0 11,15 * * 1-5';
  const ok = await noFrame(page, async (f) => {
    const l = f.locator('input[placeholder="Valor"]').last();
    if (!(await l.count())) return null;
    await l.fill(CRON); await l.press('Tab'); return true;
  });
  console.log('cron preenchido: ' + !!ok);
  await page.waitForTimeout(2500);
  await clica(page, /^Verificar$/, 'Verificar');
  await page.waitForTimeout(3000);
  fs.writeFileSync(path.join(LOCAL, 'w18-verificar.txt'), await txt(page), 'utf8');
  await shot('w18-5-verificar.png', page);
  await clica(page, /^Salvar acionador$/, 'Salvar acionador');
  await page.waitForTimeout(6000);
  await shot('w18-6-salvo.png', page);
  await ctx.close(); process.exit(0);
})();
