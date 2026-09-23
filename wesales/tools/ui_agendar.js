// Marca uma reuniao de TESTE para o 9940 pela TELA da agenda (como uma pessoa).
// Nao le nem guarda token: so clica e tira print. Passos por argumento:
//   node ui_agendar.js abrir            -> abre a agenda, print + botoes
//   node ui_agendar.js novo             -> abrir + clica "Novo"/"Agendar", print + campos
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
const PASSO = process.argv[2] || 'abrir';
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'),
    { headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu', '--disable-extensions'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  const txt = async () => { let t = ''; for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n'; return t; };
  const foto = async (n) => { await page.screenshot({ path: path.join(LOCAL, 'ag-' + n + '.png') }); fs.writeFileSync(path.join(LOCAL, 'ag-' + n + '.txt'), await txt(), 'utf8'); };
  const botoes = async () => {
    const out = [];
    for (const f of page.frames()) {
      const b = await f.evaluate(() => [...document.querySelectorAll('button,[role=button],a')].map(e => (e.innerText || e.getAttribute('aria-label') || '').trim()).filter(Boolean)).catch(() => []);
      out.push(...b);
    }
    return [...new Set(out)].slice(0, 80);
  };
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/calendars/view`, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 30; i++) { await page.waitForTimeout(4000); if ((await txt()).length > 1500) break; }
  await page.waitForTimeout(4000);
  console.log('URL', page.url());
  await foto('0');
  console.log('BOTOES', JSON.stringify(await botoes()));
  if (PASSO === 'novo') {
    let ok = false;
    for (const re of [/^\s*\+?\s*Novo\s*$/i, /Novo agendamento|Novo compromisso|New appointment|Agendar/i]) {
      for (const f of page.frames()) {
        const l = f.getByRole('button', { name: re }).first();
        if (await l.count().catch(() => 0)) { await l.click({ force: true }).catch(() => {}); ok = true; break; }
      }
      if (ok) break;
    }
    console.log('clicou novo:', ok);
    await page.waitForTimeout(6000);
    await foto('1');
    console.log('BOTOES1', JSON.stringify(await botoes()));
  }
  if (PASSO === 'form') {
    for (const f of page.frames()) { const l = f.getByRole('button', { name: /^\s*\+?\s*Novo\s*$/i }).first(); if (await l.count().catch(() => 0)) { await l.click({ force: true }); break; } }
    await page.waitForTimeout(2500);
    for (const f of page.frames()) { const l = f.getByText(/Agendar compromisso/i).first(); if (await l.count().catch(() => 0)) { await l.click({ force: true }); break; } }
    await page.waitForTimeout(8000);
    await foto('2');
    const campos = [];
    for (const f of page.frames()) {
      campos.push(...await f.evaluate(() => [...document.querySelectorAll('input,textarea,select,[role=combobox]')].filter(e => e.offsetParent).map(e => ({
        tag: e.tagName, type: e.type, ph: e.placeholder || '', name: e.name || '', aria: e.getAttribute('aria-label') || '',
        val: (e.value || '').slice(0, 40), lab: (e.closest('label, .n-form-item, .form-group, div')?.innerText || '').slice(0, 60).replace(/\n/g, ' / ') }))).catch(() => []));
    }
    console.log('CAMPOS', JSON.stringify(campos, null, 0).slice(0, 4000));
  }
  if (PASSO === 'agendar') {
    for (const f of page.frames()) { const l = f.getByRole('button', { name: /^\s*\+?\s*Novo\s*$/i }).first(); if (await l.count().catch(() => 0)) { await l.click({ force: true }); break; } }
    await page.waitForTimeout(2500);
    for (const f of page.frames()) { const l = f.getByText(/Agendar compromisso/i).first(); if (await l.count().catch(() => 0)) { await l.click({ force: true }); break; } }
    await page.waitForTimeout(8000);
    await page.mouse.click(1050, 287);
    await page.keyboard.type('Pablo Sampaio', { delay: 80 });
    await page.waitForTimeout(6000);
    await foto('3');
    const opc = page.getByText(/teste9940@gmail/).first();
    if (!(await opc.count())) { console.log('CONTATO NAO APARECEU — nada agendado'); await ctx.close(); process.exit(3); }
    await opc.click({ force: true });
    await page.waitForTimeout(3000);
    await foto('4');
    const t4 = await txt();
    const m4 = t4.match(/set \d+, \d+:\d+ [AP]M[^\n]*/); console.log('HORARIO:', m4 && m4[0]); if (!/Pablo Sampaio/.test(t4) || !m4) { console.log('CONFERENCIA FALHOU — nada agendado'); await ctx.close(); process.exit(4); }
    await page.getByRole('button', { name: /^\s*Agendar compromisso\s*$/i }).last().click({ force: true });
    await page.waitForTimeout(8000);
    await foto('5');
    console.log('FINAL:', (await txt()).split('\n').filter(l => /sucesso|agendado|erro|error|conflito|indispon/i.test(l)).slice(0, 8).join(' | '));
  }
  await ctx.close(); process.exit(0);
})();
