// Renomeia a etapa AGENDAR -> REUNIAO DE DIAGNOSTICO no FUNIL DE VENDAS (mesmo id).
// SO_OLHAR=1 so fotografa o editor sem salvar.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
const NOVO = 'REUNIÃO DE DIAGNÓSTICO';
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  const txt = async () => { let t=''; for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n'; return t; };
  const noFrame = async (fn) => { for (const f of page.frames()) { const r = await fn(f).catch(() => null); if (r) return r; } return null; };
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/pipelines`, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 25; i++) { await page.waitForTimeout(4000); if (/FUNIL DE VENDAS/.test(await txt())) break; }
  await page.waitForTimeout(4000);
  await page.screenshot({ path: path.join(LOCAL, 'etapa-0-lista.png') });
  // abrir edicao do pipeline: icone de lapis/editar na linha do FUNIL DE VENDAS
  const abriu = await noFrame(async (f) => {
    const linha = f.locator('tr, .pipeline-row, [class*=row]').filter({ hasText: 'FUNIL DE VENDAS' }).first();
    if (!(await linha.count())) return null;
    const bt = linha.locator('button, [role=button], svg, i').filter({ hasNot: f.locator('xx') });
    const n = await bt.count();
    for (let i = 0; i < n; i++) {
      const b = bt.nth(i);
      const lab = ((await b.getAttribute('aria-label')) || (await b.getAttribute('title')) || (await b.getAttribute('id')) || '') + (await b.evaluate(e => e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className).catch(() => ''));
      if (/edit|pencil|editar/i.test(lab)) { await b.click({ force: true }); return 'lapis:' + lab.slice(0, 40); }
    }
    await linha.click({ force: true }); return 'linha';
  });
  console.log('abrir: ' + abriu);
  await page.waitForTimeout(7000);
  await page.screenshot({ path: path.join(LOCAL, 'etapa-1-editor.png') });
  const inputs = await noFrame(async (f) => {
    const l = f.locator('input'); const n = await l.count(); const out = [];
    for (let i = 0; i < n; i++) out.push(await l.nth(i).inputValue().catch(() => ''));
    return out.length ? out : null;
  });
  console.log('inputs: ' + JSON.stringify(inputs));
  if (process.env.SO_OLHAR) { await ctx.close(); process.exit(0); }
  const ok = await noFrame(async (f) => {
    const l = f.locator('input').filter({ hasText: '' });
    const n = await l.count();
    for (let i = 0; i < n; i++) { if ((await l.nth(i).inputValue()) === 'AGENDAR') { await l.nth(i).fill(NOVO); return true; } }
    return null;
  });
  console.log('preencheu: ' + !!ok);
  if (!ok) { await ctx.close(); process.exit(1); }
  await page.waitForTimeout(1500);
  const salvou = await noFrame(async (f) => { const b = f.getByRole('button', { name: /^(Salvar|Save|Atualizar|Update)$/i }).last(); if (!(await b.count())) return null; await b.click(); return true; });
  console.log('salvou: ' + !!salvou);
  await page.waitForTimeout(7000);
  await page.screenshot({ path: path.join(LOCAL, 'etapa-2-salvo.png') });
  await ctx.close(); process.exit(0);
})();
