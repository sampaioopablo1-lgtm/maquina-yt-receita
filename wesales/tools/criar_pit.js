// Cria a Integracao Privada "Faxina de Tarefas" e entrega o token por STDOUT
// (so a linha TOKEN=...), para ser canalizado direto ao `gh secret set` sem
// aparecer em log. SO_OLHAR=1 para antes de criar.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
const ESCOPOS = [/View Contacts|Visualizar contatos|contacts\.readonly/i, /Edit Contacts|Editar contatos|contacts\.write/i,
                 /View Opportunities|Visualizar oportunidades|opportunities\.readonly/i,
                 /tasks\.readonly|View Tasks|Visualizar tarefas/i];
const log = (m) => process.stderr.write(m + '\n');
(async () => {
  const ctx = await chromium.launchPersistentContext(path.join(LOCAL, 'chrome-profile'), {
    headless: true, viewport: { width: 1600, height: 1000 }, args: ['--disable-gpu'] });
  const page = ctx.pages()[0] || await ctx.newPage();
  const txt = async () => { let t=''; for (const f of page.frames()) t += (await f.evaluate(() => document.body.innerText || '').catch(() => '')) + '\n'; return t; };
  const clica = async (re, rot) => { for (const f of page.frames()) { const l = f.getByText(re).last(); if (await l.count().catch(() => 0)) { await l.click({ force: true }).catch(() => {}); log('  ' + rot + ': ok'); await page.waitForTimeout(3500); return true; } } log('  ' + rot + ': NAO ACHEI'); return false; };
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/private-integrations`, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 25; i++) { await page.waitForTimeout(4000); if (/Criar nova Integra/.test(await txt())) break; }
  await clica(/^Criar nova Integração$/, 'criar nova');
  await page.waitForTimeout(4000);
  await page.screenshot({ path: path.join(LOCAL, 'pit-1.png') });
  fs.writeFileSync(path.join(LOCAL, 'pit-1.txt'), await txt(), 'utf8');
  // nome e descricao
  for (const f of page.frames()) {
    const ins = f.locator('input:visible, textarea:visible'); const n = await ins.count().catch(() => 0);
    if (n >= 1) { await ins.nth(0).fill('Faxina de Tarefas'); if (n >= 2) await ins.nth(1).fill('GitHub Actions: exclui tarefa automatica fora de contexto e controla capacidade do SDR'); log('  nome/descricao: ok (' + n + ' campos)'); break; }
  }
  await clica(/^(Próximo|Proximo|Next|Continuar)$/, 'proximo');
  await page.waitForTimeout(4000);
  await page.screenshot({ path: path.join(LOCAL, 'pit-2.png') });
  const t2 = await txt(); fs.writeFileSync(path.join(LOCAL, 'pit-2.txt'), t2, 'utf8');
  log('  tela de escopos: ' + t2.split('\n').filter(l => /contact|contato|opportunit|oportunidade|task|tarefa/i.test(l)).slice(0, 20).join(' | '));
  // abre o seletor de escopos e escolhe cada um digitando o filtro
  const abrir = async () => { for (const f of page.frames()) { const l = f.getByText(/^Selecionar Escopos$/).first(); if (await l.count().catch(() => 0)) { await l.click({ force: true }); await page.waitForTimeout(2500); return true; } } return false; };
  log('  abrir seletor: ' + await abrir());
  await page.screenshot({ path: path.join(LOCAL, 'pit-2b.png') });
  let opcoes = [];
  for (const f of page.frames()) {
    const o = await f.evaluate(() => [...document.querySelectorAll('[role=option], .n-base-select-option, .el-select-dropdown__item, .multiselect__option, li, .hr-select-option')].map(e => (e.innerText || '').trim()).filter(Boolean)).catch(() => []);
    opcoes = opcoes.concat(o);
  }
  fs.writeFileSync(path.join(LOCAL, 'pit-escopos.txt'), opcoes.join(String.fromCharCode(10)), 'utf8');
  log('  opcoes (amostra): ' + opcoes.filter(o => /contact|opportunit|task/i.test(o)).slice(0, 25).join(' | '));
  if (process.env.SO_OLHAR) { await ctx.close(); process.exit(0); }
  const QUERO = ['contacts.readonly', 'contacts.write', 'opportunities.readonly', 'locations/tasks.readonly'];
  for (const q of QUERO) {
    let ok = false;
    // sem busca no seletor: rola ate a linha e clica com o mouse de verdade
    // (clique forcado no texto nao marca a caixa - visto em pit-3-selecao.png)
    // volta ao topo da lista e desce com a roda ate a linha existir e estar visivel
    await page.mouse.move(900, 650);
    for (let k = 0; k < 60; k++) await page.mouse.wheel(0, -400);
    await page.waitForTimeout(600);
    for (let passo = 0; passo < 120 && !ok; passo++) {
      for (const f of page.frames()) {
        const l = f.getByText(' - ' + q, { exact: false });
        const n = await l.count().catch(() => 0);
        for (let i = 0; i < n && !ok; i++) {
          const el = l.nth(i);
          const txt = ((await el.innerText().catch(() => '')) || '').trim();
          if (!txt.endsWith(' - ' + q)) continue;
          const box = await el.boundingBox();
          if (box && box.y > 500 && box.y < 760) { await page.mouse.click(box.x + 20, box.y + box.height / 2); ok = true; }
        }
        if (ok) break;
      }
      if (!ok) { await page.mouse.wheel(0, 120); await page.waitForTimeout(250); }
    }
    log('  escopo ' + q + ': ' + ok);
    await page.waitForTimeout(1200);
  }
  let sel = '';
  for (const f of page.frames()) { const t = await f.evaluate(() => document.body.innerText).catch(() => ''); const m = t.match(/(\d+) de 162 selecionados/); if (m) sel = m[1]; }
  log('  selecionados: ' + sel);
  await page.screenshot({ path: path.join(LOCAL, 'pit-3-selecao.png') });
  if (sel !== '4') { log('  ABORTADO: esperava 4 escopos'); await ctx.close(); process.exit(1); }
  await page.keyboard.press('Escape'); await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(LOCAL, 'pit-3.png') });
  const criou = await (async () => { for (const f of page.frames()) { const b = f.getByRole('button', { name: /^Criar$/ }).last(); if (await b.count().catch(() => 0)) { await b.click(); return true; } } return false; })();
  log('  criar: ' + criou);
  await page.waitForTimeout(8000);
  await page.screenshot({ path: path.join(LOCAL, 'pit-4.png') });
  // o token aparece uma unica vez num campo/texto; pega o valor que parece um token
  const tok = await page.evaluate(() => {
    const vals = [...document.querySelectorAll('input, textarea, code, span, div')].map(e => (e.value || e.innerText || '').trim());
    return vals.find(v => /^pit-[0-9a-f-]{20,}$/i.test(v)) || '';
  });
  if (tok) process.stdout.write(tok); else log('  TOKEN NAO ENCONTRADO na tela (ver pit-4.png)');
  await ctx.close(); process.exit(0);
})();
