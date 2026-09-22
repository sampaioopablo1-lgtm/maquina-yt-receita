// WeSales — abre o CRM em janela visivel, espera o login do dono e captura
// o bearer da API interna (backend.leadconnectorhq.com) + o storage state.
// Nada aqui vai para commit: tudo grava em wesales/.local/ (gitignored).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
const PROFILE = path.join(LOCAL, 'chrome-profile');
const BEARER_FILE = path.join(LOCAL, '_ghl_bearer.txt');
const STATE_FILE = path.join(LOCAL, 'storage-state.json');

function expOf(tok) {
  try {
    const p = JSON.parse(Buffer.from(tok.split('.')[1].replace(/-/g,'+').replace(/_/g,'/'), 'base64').toString());
    return p.exp ? new Date(p.exp * 1000) : null;
  } catch { return null; }
}

(async () => {
  fs.mkdirSync(PROFILE, { recursive: true });
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: false,
    viewport: null,
    args: ['--start-maximized'],
  });

  let bearer = null;
  ctx.on('request', (req) => {
    const u = req.url();
    if (!u.includes('leadconnectorhq.com')) return;
    const h = req.headers();
    const a = h['authorization'] || h['Authorization'];
    if (a && a.toLowerCase().startsWith('bearer ') && a.split('.').length === 3) {
      const t = a.slice(7).trim();
      if (t !== bearer) { bearer = t; }
    }
  });

  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto('https://app.wesalescrm.com/', { waitUntil: 'domcontentloaded' }).catch(()=>{});

  console.log('JANELA ABERTA. Faca o login em app.wesalescrm.com.');
  console.log('Assim que logar, eu navego sozinho ate os workflows e capturo o token.');

  const deadline = Date.now() + 15 * 60 * 1000;
  let nudged = false;
  while (Date.now() < deadline) {
    await page.waitForTimeout(3000);
    const url = page.url();
    const loggedIn = /\/(v2\/)?location\//.test(url) || /dashboard/.test(url);
    if (loggedIn && !nudged) {
      nudged = true;
      console.log('LOGIN DETECTADO -> abrindo a tela de workflows para forcar as chamadas internas');
      await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/automation/workflows`,
        { waitUntil: 'domcontentloaded' }).catch(()=>{});
      await page.waitForTimeout(12000);
    }
    if (bearer) {
      const e = expOf(bearer);
      if (!e || e.getTime() > Date.now() + 60000) {
        fs.writeFileSync(BEARER_FILE, bearer, 'utf8');
        await ctx.storageState({ path: STATE_FILE });
        console.log('BEARER_OK len=' + bearer.length + ' exp=' + (e ? e.toISOString() : 'n/a'));
        console.log('SALVO EM ' + BEARER_FILE);
        await ctx.close();
        process.exit(0);
      }
    }
    if (nudged) {
      // relê a lista de workflows de tempos em tempos até o token aparecer
      await page.reload({ waitUntil: 'domcontentloaded' }).catch(()=>{});
      await page.waitForTimeout(8000);
    }
  }
  console.log('TIMEOUT: nao capturei o bearer em 15 min.');
  await ctx.close();
  process.exit(2);
})();
