// Captura a sessao logada do WeSales para o segredo GHL_STORAGE_STATE.
//
// Roda UMA vez, no PC do dono (precisa de janela — nao roda no runner):
//   npm install --no-save playwright && npx playwright install chromium
//   node wesales/tools/login-capture.js
// Abre o Chromium na tela de login do WeSales; o dono faz o login; quando a
// tela de workflows carregar, o script grava wesales/.local/storage-state.json
// (cookies + localStorage, o que o Playwright chama de storageState) e fecha.
// Depois, o conteudo vai para o segredo do repositorio:
//   gh secret set GHL_STORAGE_STATE < wesales/.local/storage-state.json
//
// Este arquivo estava citado em renovar_bearer.js e em varios documentos mas
// nao existia em nenhum branch (achado da sessao local em 27/09 18:25). E o
// unico passo do projeto que exige uma pessoa: a sessao e do dono.
//
// SEGURANCA, sem rodeio: o arquivo gerado E a sessao logada. Nunca commitar
// (wesales/.local esta no .gitignore), nunca colar em chat, trocar quando nao
// precisar mais. renovar_bearer.js nunca imprime o conteudo — este tambem nao.
const fs = require('fs');
const path = require('path');

let chromium;
try {
  ({ chromium } = require('playwright'));
} catch {
  console.error('Falta o Playwright. Rode antes:\n  npm install --no-save playwright && npx playwright install chromium');
  process.exit(2);
}

const LOC = '1D53YTI9C7oIMBavcQxV';
const ALVO = `https://app.wesalescrm.com/v2/location/${LOC}/automation/workflows`;
const LOCAL = path.resolve(__dirname, '..', '.local');
const SAIDA = path.join(LOCAL, 'storage-state.json');

(async () => {
  fs.mkdirSync(LOCAL, { recursive: true });
  const browser = await chromium.launch({ headless: false });
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.goto(ALVO, { waitUntil: 'domcontentloaded' }).catch(() => {});
  console.log('Faca o login na janela que abriu. Quando a tela de workflows carregar, o arquivo e gravado sozinho.');
  // Sai da espera quando a URL for do app (com /location/) e nao for tela de login.
  await page.waitForURL(
    (u) => /\/location\//.test(u.toString()) && !/login|auth/i.test(u.toString()),
    { timeout: 0 },
  );
  // O app grava os tokens no localStorage logo depois de navegar; um respiro
  // evita capturar o estado pela metade.
  await page.waitForTimeout(8000);
  await ctx.storageState({ path: SAIDA });
  const tamanho = fs.statSync(SAIDA).size;
  console.log(`gravado: ${SAIDA} (${tamanho} bytes)`);
  console.log('Agora: gh secret set GHL_STORAGE_STATE < wesales/.local/storage-state.json');
  console.log('Depois rode a Action wesales-interno para provar (ela imprime so o tempo de vida do bearer).');
  await browser.close();
})().catch((e) => {
  console.error('falhou:', e.message);
  process.exit(1);
});
