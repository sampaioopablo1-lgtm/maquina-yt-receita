// Abre o builder de um workflow e grava as respostas que descrevem os
// TIPOS DE ACAO disponiveis nesta versao do CRM. Somente leitura.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const WF = 'e0792c83-8fa5-480d-a3fb-f10268507699'; // ZZ TESTE API (rascunho)
const PROFILE = path.resolve(__dirname, '..', '.local', 'chrome-profile');
const OUT = path.resolve(__dirname, '..', '.local', 'acoes.json');

(async () => {
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: true, viewport: { width: 1600, height: 1000 },
  });
  const page = ctx.pages()[0] || await ctx.newPage();

  const candidatos = [];
  page.on('response', async (r) => {
    const u = r.url();
    if (!/leadconnectorhq\.com|wesalescrm/.test(u)) return;
    const ct = (r.headers()['content-type'] || '');
    if (!/json|javascript/.test(ct)) return;
    try {
      const txt = await r.text();
      // procura respostas que citem tipos de acao conhecidos
      if (/add_contact_tag/.test(txt) && /opportunit/i.test(txt)) {
        candidatos.push({ url: u.slice(0, 160), tamanho: txt.length, txt });
      }
    } catch { /* corpo indisponivel */ }
  });

  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/automation/workflow/${WF}`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 30; i++) { await page.waitForTimeout(5000); process.stdout.write('.'); }

  console.log('\nrespostas candidatas: ' + candidatos.length);
  const tipos = new Set();
  for (const c of candidatos) {
    console.log('  ' + c.url + '  (' + c.tamanho + ' bytes)');
    // extrai tokens que parecem tipo de acao ligados a oportunidade
    for (const m of c.txt.matchAll(/"([a-z][a-z0-9_]*opportunit[a-z0-9_]*)"/gi)) tipos.add(m[1]);
    for (const m of c.txt.matchAll(/"(opportunit[a-z0-9_]*)"/gi)) tipos.add(m[1]);
  }
  console.log('TIPOS COM "opportunity": ' + [...tipos].join(', '));
  fs.writeFileSync(OUT, JSON.stringify(
    candidatos.map((c) => ({ url: c.url, tamanho: c.tamanho })), null, 2), 'utf8');
  // guarda o maior corpo inteiro para eu vasculhar offline
  if (candidatos.length) {
    const maior = candidatos.sort((a, b) => b.tamanho - a.tamanho)[0];
    fs.writeFileSync(path.resolve(__dirname, '..', '.local', 'acoes-corpo.txt'),
      maior.txt, 'utf8');
    console.log('corpo maior salvo em .local/acoes-corpo.txt');
  }
  await ctx.close();
  process.exit(0);
})();
