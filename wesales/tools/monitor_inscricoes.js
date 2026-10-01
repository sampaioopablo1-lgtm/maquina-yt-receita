// Histórico de inscrições de cada workflow, pela rota da TELA (a API pública não tem; o bearer sozinho
// devolve vazio — precisa dos cabeçalhos que o editor manda, capturados aqui com a sessão logada).
// Só leitura. Usado pelo monitor.py para achar inscrição presa.
//
//   GHL_STORAGE_STATE='{...}' node monitor_inscricoes.js saida.json <workflowId> [<workflowId> ...]
//
// Saída: { "<workflowId>": { http, total, statuses: [{contactId, status, passo, criada, mexida, retoma}] } }
// Códigos de saída: 0 ok · 2 sem sessão · 3 a tela não mandou os cabeçalhos (sessão vencida?).
const fs = require('fs');
const path = require('path');

const LOC = '1D53YTI9C7oIMBavcQxV';
const [saida, ...WFS] = process.argv.slice(2);

function estado() {
  if (process.env.GHL_STORAGE_STATE) return JSON.parse(process.env.GHL_STORAGE_STATE);
  const f = path.join(__dirname, '..', '.local', 'storage-state.json');
  if (fs.existsSync(f)) return JSON.parse(fs.readFileSync(f, 'utf8'));
  return null;
}

(async () => {
  const st = estado();
  if (!st || !saida || !WFS.length) { console.log('sem sessão, sem saída ou sem workflows'); process.exit(2); }
  const { chromium } = require('playwright');
  const b = await chromium.launch({ headless: true });
  const ctx = await b.newContext({ storageState: st });
  const p = await ctx.newPage();
  let H = null;
  p.on('request', r => { if (r.url().includes('/workflows/status/search/') && !H) H = r.headers(); });
  await p.goto(`https://app.wesalescrm.com/v2/location/${LOC}/automation/workflow/${WFS[0]}`,
    { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(() => {});
  for (let i = 0; i < 60 && !H; i++) await p.waitForTimeout(1000);
  if (!H) {
    for (const f of p.frames()) {
      const l = f.getByText('Histórico de inscrições');
      if (await l.count().catch(() => 0)) { await l.first().click().catch(() => {}); break; }
    }
    for (let i = 0; i < 20 && !H; i++) await p.waitForTimeout(1000);
  }
  if (!H) { console.log('a tela não mandou os cabeçalhos (sessão vencida?)'); await b.close(); process.exit(3); }
  const hh = {};
  for (const k of ['authorization', 'token-id', 'channel', 'source', 'version']) if (H[k]) hh[k] = H[k];
  const res = {};
  for (const w of WFS) {
    const u = `https://backend.leadconnectorhq.com/workflows/status/search/workflow-with-filter?workflowId=${w}&locationId=${LOC}&action=first&limit=100`;
    try {
      const r = await ctx.request.get(u, { headers: hh });
      const j = await r.json().catch(() => null);
      res[w] = {
        http: r.status(), total: j && j.count,
        statuses: ((j && j.statuses) || []).map(s => ({
          contactId: s.contactId, status: s.status, passo: s.currentStepName || '',
          criada: s.createdAt, mexida: s.updatedAt, retoma: s.executeOn || null,
        })),
      };
    } catch (e) { res[w] = { http: 0, erro: String(e).slice(0, 120), statuses: [] }; }
  }
  fs.writeFileSync(saida, JSON.stringify(res));
  console.log('inscrições lidas de', Object.keys(res).length, 'workflows');
  await b.close();
})().catch(e => { console.error('FALHOU', String(e).slice(0, 200)); process.exit(1); });
