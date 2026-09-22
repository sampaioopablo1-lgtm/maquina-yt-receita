// Abre o builder do ZZ TESTE API, abre o painel "Adicionar gatilho" e grava
// as respostas que descrevem os TIPOS DE GATILHO desta versao do CRM.
// Somente leitura: nao clica em salvar.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const WF = 'e0792c83-8fa5-480d-a3fb-f10268507699'; // ZZ TESTE API (rascunho)
const LOCAL = path.resolve(__dirname, '..', '.local');
const PROFILE = path.join(LOCAL, 'chrome-profile');

(async () => {
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: true, viewport: { width: 1600, height: 1000 },
    args: ['--disable-gpu', '--disable-extensions'],
  });
  const page = ctx.pages()[0] || await ctx.newPage();
  const achados = [];
  page.on('response', async (r) => {
    const u = r.url();
    if (!/leadconnectorhq\.com|wesalescrm|msgsndr/.test(u)) return;
    try {
      const txt = await r.text();
      if (/schedul/i.test(txt) && /trigger/i.test(txt) && txt.length < 8e6) {
        achados.push({ url: u.slice(0, 200), tamanho: txt.length, txt });
      }
    } catch { /* sem corpo */ }
  });

  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/automation/workflow/${WF}`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 20; i++) { await page.waitForTimeout(5000); process.stdout.write('.'); }

  // o builder mora num iframe; procura o botao de gatilho em todos os frames
  let clicou = false;
  for (const f of page.frames()) {
    const b = f.getByText(/Add New Trigger|Adicionar novo gatilho|Adicionar gatilho|Novo gatilho/i).first();
    if (await b.count().catch(() => 0)) {
      await b.click({ force: true, timeout: 15000 }).catch(() => {});
      clicou = true; break;
    }
  }
  console.log('\nclicou gatilho: ' + clicou);
  for (let i = 0; i < 6; i++) { await page.waitForTimeout(5000); process.stdout.write('.'); }
  // digita no filtro para forcar o painel a carregar o esquema do Scheduler
  for (const f of page.frames()) {
    const s = f.locator('input[placeholder*="earch" i], input[placeholder*="esquis" i]').first();
    if (await s.count().catch(() => 0)) {
      await s.fill('Schedul').catch(() => {});
      await page.waitForTimeout(3000);
      const op = f.getByText(/^(Scheduler|Agendador)$/i).first();
      if (await op.count().catch(() => 0)) {
        await op.click({ force: true }).catch(() => {});
        console.log('abriu Scheduler');
      }
      break;
    }
  }
  for (let i = 0; i < 4; i++) { await page.waitForTimeout(5000); process.stdout.write('.'); }
  await page.screenshot({ path: path.join(LOCAL, 'sniff-gatilhos.png') });

  // textos visiveis do painel do scheduler, para conferir os campos
  let painel = '';
  for (const f of page.frames()) {
    const t = await f.evaluate(() => document.body.innerText || '').catch(() => '');
    if (/Scheduler|Agendador/i.test(t)) painel += t.slice(0, 4000) + '\n----\n';
  }
  fs.writeFileSync(path.join(LOCAL, 'sniff-gatilhos-painel.txt'), painel, 'utf8');
  console.log('\nrespostas com "schedul": ' + achados.length);
  achados.forEach((a, i) => {
    console.log('  ' + a.url + ' (' + a.tamanho + ')');
    fs.writeFileSync(path.join(LOCAL, 'sniff-gatilhos-' + i + '.txt'), a.txt, 'utf8');
  });
  await ctx.close();
  process.exit(0);
})();
