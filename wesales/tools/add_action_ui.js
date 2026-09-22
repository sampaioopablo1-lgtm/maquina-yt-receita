// Adiciona uma acao pela TELA num rascunho, para descobrir a forma exata do
// no que a API recusa. Clica no "+" abaixo do ultimo no do canvas.
// Uso: node add_action_ui.js <workflowId> "<busca>" [--salvar]
const { chromium } = require('playwright');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const PROFILE = path.resolve(__dirname, '..', '.local', 'chrome-profile');
const FRAME_RE = /client-app-automation-workflows\.leadconnectorhq\.com/;
const SHOT = (n) => path.resolve(__dirname, '..', '.local', n);

async function frameReady(page, maxMs, re) {
  const t0 = Date.now();
  while (Date.now() - t0 < maxMs) {
    const f = page.frames().find((fr) => FRAME_RE.test(fr.url()));
    if (f) {
      const t = await f.evaluate(() => (document.body ? document.body.innerText : '')).catch(() => '');
      if (t && t.length > 150 && (!re || re.test(t))) return { f, t };
    }
    await page.waitForTimeout(5000); process.stdout.write('.');
  }
  const f = page.frames().find((fr) => FRAME_RE.test(fr.url()));
  return { f, t: '' };
}

(async () => {
  const wf = process.argv[2];
  const busca = process.argv[3] || 'oportunidade';
  const salvar = process.argv.includes('--salvar');

  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: false, viewport: { width: 1600, height: 1000 },
  });
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/automation/workflow/${wf}`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});

  console.log('esperando o canvas');
  const { f } = await frameReady(page, 300000, /FIM|Rascunho/i);
  if (!f) { console.log('\nsem canvas'); await ctx.close(); process.exit(2); }
  await page.waitForTimeout(8000);

  // acha o "+" imediatamente acima do no FIM e clica nele
  const alvo = await f.evaluate(() => {
    const els = [...document.querySelectorAll('*')];
    const fim = els.find((e) => (e.innerText || '').trim() === 'FIM');
    if (!fim) return null;
    const rf = fim.getBoundingClientRect();
    // o "+" fica logo acima do FIM, na mesma coluna
    let melhor = null;
    for (const e of els) {
      const r = e.getBoundingClientRect();
      if (r.width < 8 || r.width > 42 || r.height < 8 || r.height > 42) continue;
      if (Math.abs((r.left + r.width / 2) - (rf.left + rf.width / 2)) > 30) continue;
      if (r.top >= rf.top || r.top < rf.top - 120) continue;
      if (!melhor || r.top > melhor.top) melhor = r;
    }
    return melhor ? { x: melhor.left + melhor.width / 2, y: melhor.top + melhor.height / 2 } : null;
  }).catch(() => null);

  console.log('\n"+" encontrado em: ' + JSON.stringify(alvo));
  if (!alvo) { await page.screenshot({ path: SHOT('sem-mais.png') }); await ctx.close(); process.exit(3); }

  const box = await (await f.frameElement()).boundingBox();
  await page.mouse.click(box.x + alvo.x, box.y + alvo.y);
  await page.waitForTimeout(9000);
  await page.screenshot({ path: SHOT('painel-acoes.png') });

  const t = await f.evaluate(() => document.body.innerText).catch(() => '');
  console.log('--- PAINEL APOS CLICAR NO "+" ---');
  console.log(t.replace(/\n{2,}/g, '\n').slice(-1600));

  // procura a acao pelo nome
  try {
    await page.keyboard.type(busca, { delay: 170 });
    await page.waitForTimeout(6000);
    const t2 = await f.evaluate(() => document.body.innerText).catch(() => '');
    console.log('--- APOS BUSCAR "' + busca + '" ---');
    console.log(t2.replace(/\n{2,}/g, '\n').slice(-900));
    await page.screenshot({ path: SHOT('painel-busca.png') });
  } catch (e) { console.log('busca falhou: ' + e.message.slice(0, 100)); }

  if (salvar) {
    console.log('(modo --salvar: escolha e gravacao ficam para o proximo passo)');
  }
  await ctx.close();
  process.exit(0);
})();
