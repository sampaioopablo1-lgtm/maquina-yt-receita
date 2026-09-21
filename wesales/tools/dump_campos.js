// Salva o mapa de campos personalizados (nome -> id, chave, tipo, pasta)
// capturando a RESPOSTA que a propria tela de Campos personalizados recebe.
// Nao contem segredo: so metadado de campo. Somente leitura.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const PROFILE = path.resolve(__dirname, '..', '.local', 'chrome-profile');
const OUT = path.resolve(__dirname, 'campos.json');

(async () => {
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: true, viewport: { width: 1400, height: 900 },
  });
  const page = ctx.pages()[0] || await ctx.newPage();

  let dados = null;
  page.on('response', async (r) => {
    if (!/customFields\/search/.test(r.url())) return;
    try {
      const j = await r.json();
      const arr = j.customFields || j.fields || j.data || [];
      if (Array.isArray(arr) && arr.length) dados = arr;
    } catch { /* resposta nao-json */ }
  });

  await page.goto(`https://app.wesalescrm.com/v2/location/${LOC}/settings/fields`,
    { waitUntil: 'domcontentloaded', timeout: 180000 }).catch(() => {});
  for (let i = 0; i < 40 && !dados; i++) {
    await page.waitForTimeout(5000); process.stdout.write('.');
  }

  if (!dados) { console.log('\nnao capturei a resposta'); await ctx.close(); process.exit(2); }

  const mapa = {};
  for (const c of dados) {
    if (c.documentType && c.documentType !== 'field') continue;
    mapa[c.name] = {
      id: c.id, chave: c.fieldKey, tipo: c.dataType,
      pasta: c.parentId, opcoes: c.picklistOptions || undefined,
    };
  }
  fs.writeFileSync(OUT, JSON.stringify(mapa, null, 2), 'utf8');
  console.log('\ncampos salvos: ' + Object.keys(mapa).length + ' -> ' + OUT);
  for (const n of ['Toques na semana', 'Hora da conexão', 'Hora do retorno',
                   'Checkpoint — Tentativa nº', 'Checkpoint — Data de retorno']) {
    console.log('  ' + n + ': ' + (mapa[n] ? mapa[n].id + ' | ' + mapa[n].chave + ' | ' + mapa[n].tipo : 'AUSENTE'));
  }
  await ctx.close();
  process.exit(0);
})();
