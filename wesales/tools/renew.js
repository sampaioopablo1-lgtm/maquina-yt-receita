// Renova o bearer da API interna sozinho, a partir do perfil do Chrome que
// ja esta logado (wesales/.local/chrome-profile). So pede login humano se o
// perfil tiver perdido a sessao.
// Uso: node renew.js  [--headed]
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
    const p = JSON.parse(Buffer.from(
      tok.split('.')[1].replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString());
    return p.exp ? new Date(p.exp * 1000) : null;
  } catch { return null; }
}

(async () => {
  const headed = process.argv.includes('--headed');
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: !headed,
    viewport: { width: 1400, height: 900 },
  });

  let bearer = null;
  ctx.on('request', (req) => {
    if (!req.url().includes('leadconnectorhq.com')) return;
    const h = req.headers();
    const a = h['authorization'] || h['Authorization'];
    if (a && a.toLowerCase().startsWith('bearer ') && a.split('.').length === 3) {
      bearer = a.slice(7).trim();
    }
  });

  const page = ctx.pages()[0] || await ctx.newPage();
  // a tela de automacoes e a que fala com o backend de workflows
  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/automation/workflows`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});

  const deadline = Date.now() + 5 * 60 * 1000;
  while (Date.now() < deadline && !bearer) {
    await page.waitForTimeout(5000);
    process.stdout.write('.');
  }

  if (!bearer) {
    console.log('\nFALHOU: nenhum bearer no trafego. URL atual: ' + page.url());
    console.log('Se caiu na tela de login, rode: node login-capture.js');
    await ctx.close();
    process.exit(2);
  }

  const e = expOf(bearer);
  if (e && e.getTime() < Date.now() + 60000) {
    console.log('\nFALHOU: token capturado ja esta expirando.');
    await ctx.close();
    process.exit(3);
  }

  fs.writeFileSync(BEARER_FILE, bearer, 'utf8');
  await ctx.storageState({ path: STATE_FILE });
  console.log('\nBEARER RENOVADO  exp=' + (e ? e.toISOString() : 'n/a'));
  await ctx.close();
  process.exit(0);
})();
