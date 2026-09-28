// Renova o bearer da API interna do GHL a partir de ESTADO DE SESSAO em variavel
// de ambiente — sem perfil de Chrome no disco e sem caminho do PC de ninguem.
//
// POR QUE ESTE ARQUIVO, TENDO `renew.js`
// --------------------------------------
// O `renew.js` funciona, mas so no PC do dono: ele abre
// `chromium.launchPersistentContext(wesales/.local/chrome-profile)`, isto e, um
// perfil de Chrome que ja esta logado naquela maquina, e o `ghl_api.renovar_bearer`
// que o chama crava `NODE_PATH=C:\Users\sampa\AppData\Roaming\npm\node_modules`.
// Enquanto for assim, toda edicao de workflow espera uma pessoa sentada.
//
// Aqui o estado de sessao entra por `GHL_STORAGE_STATE` (o JSON que o Playwright
// chama de storageState: cookies + localStorage). Isso roda em GitHub Actions, em
// contêiner, em qualquer lugar com internet — sem perfil e sem interacao.
//
// COMO OBTER O `GHL_STORAGE_STATE` (uma vez, no PC do dono)
// --------------------------------------------------------
//   node wesales/tools/login-capture.js      # abre janela, dono faz login
//   # ele grava wesales/.local/storage-state.json
// O conteudo desse arquivo vai para o segredo do repositorio `GHL_STORAGE_STATE`.
// Renovar so quando o GHL invalidar a sessao.
//
// O QUE ISTO E, EM TERMOS DE SEGURANCA — dito sem rodeio
// -----------------------------------------------------
// O storageState **e** a sessao logada: quem o tem entra no CRM como o dono. Nao e
// um token de leitura. Por isso: guardar apenas como segredo (nunca em commit,
// nunca em log), preferir um usuario do CRM com o menor papel que resolva em vez da
// conta de dono, e trocar quando nao precisar mais. Este script nunca imprime o
// token nem o estado — so o tempo de vida.
//
// USO
// ---
//   GHL_STORAGE_STATE='{...}' node renovar_bearer.js            # grava em .local
//   GHL_STORAGE_STATE='{...}' node renovar_bearer.js --stdout   # imprime o bearer
//
// Codigos de saida: 0 capturou · 2 sem estado de sessao ou sessao invalida ·
// 3 navegou mas nenhum bearer no trafego (normalmente sessao expirada).

const fs = require('fs');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const LOCAL = path.resolve(__dirname, '..', '.local');
const BEARER_FILE = path.join(LOCAL, '_ghl_bearer.txt');
const ALVO = `https://app.wesalescrm.com/v2/location/${LOC}/automation/workflows`;

function minutosDe(tok) {
  try {
    const p = JSON.parse(Buffer.from(
      tok.split('.')[1].replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString());
    return p.exp ? (p.exp * 1000 - Date.now()) / 60000 : null;
  } catch { return null; }
}

(async () => {
  const bruto = (process.env.GHL_STORAGE_STATE || '').trim();
  if (!bruto) {
    console.error('SEM ESTADO: defina GHL_STORAGE_STATE (ver o cabecalho deste arquivo).');
    process.exit(2);
  }
  let estado;
  try {
    estado = JSON.parse(bruto);
  } catch (e) {
    console.error('GHL_STORAGE_STATE nao e JSON valido: ' + e.message);
    process.exit(2);
  }

  const { chromium } = require('playwright');
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    storageState: estado,
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

  const page = await ctx.newPage();
  // A tela de automacoes e a que conversa com o backend de workflows, entao e ela
  // que carrega o header que interessa.
  await page.goto(ALVO, { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});

  const limite = Date.now() + 3 * 60 * 1000;
  while (Date.now() < limite && !bearer) {
    await page.waitForTimeout(3000);
  }

  const url = page.url();
  // Opcional: grava a sessão depois do acesso (os tokens podem ter sido renovados) sem os
  // caches `statsig`, para caber no limite de 48 KB de um segredo do GitHub.
  if (process.env.GHL_STORAGE_OUT) {
    const st = await ctx.storageState();
    for (const o of st.origins || []) o.localStorage = (o.localStorage || []).filter((i) => !i.name.startsWith('statsig'));
    fs.writeFileSync(process.env.GHL_STORAGE_OUT, JSON.stringify(st));
  }
  await browser.close();

  if (!bearer) {
    console.error('NENHUM BEARER no trafego. URL final: ' + url);
    if (/login|auth/i.test(url)) {
      console.error('A URL final parece tela de login: o estado de sessao expirou. '
        + 'Regere com login-capture.js no PC do dono e troque o segredo.');
    }
    process.exit(3);
  }

  const m = minutosDe(bearer);
  if (m !== null && m < 1) {
    console.error('Bearer capturado ja esta vencendo (%.1f min) — sessao ruim.', m);
    process.exit(3);
  }

  if (process.argv.includes('--stdout')) {
    process.stdout.write(bearer);
  } else {
    fs.mkdirSync(LOCAL, { recursive: true });
    fs.writeFileSync(BEARER_FILE, bearer, 'utf-8');
    console.error('bearer gravado em .local (%s min de vida)',
      m === null ? '?' : m.toFixed(1));
  }
  process.exit(0);
})().catch((e) => {
  console.error('FALHOU: ' + (e && e.message ? e.message : e));
  process.exit(3);
});
