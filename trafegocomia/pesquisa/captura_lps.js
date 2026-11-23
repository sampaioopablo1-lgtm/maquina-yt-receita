// Roda no runner: abre cada pagina de destino como celular, grava print da pagina inteira,
// o texto visivel e os links de checkout (Kiwify, Hotmart, Eduzz...). Segue o 1o checkout.
const fs = require('fs'), path = require('path');
const { chromium, devices } = require('playwright');
const OUT = 'trafegocomia/pesquisa/lps'; fs.mkdirSync(OUT, { recursive: true });
const CK = /kiwify|hotmart|eduzz|monetizze|greenn|ticto|perfectpay|kirvano|cakto|lastlink|pagar\.me|stripe|checkout|pay\./i;
(async () => {
  const b = await chromium.launch();
  const res = [];
  for (const url of JSON.parse(fs.readFileSync('trafegocomia/pesquisa/lps.json'))) {
    const nome = url.replace(/^https?:\/\//, '').replace(/[^a-z0-9.-]/gi, '_');
    const ctx = await b.newContext({ ...devices['iPhone 13'], locale: 'pt-BR' });
    const p = await ctx.newPage(); const r = { url, nome };
    try {
      await p.goto(url, { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {});
      await p.waitForTimeout(2500);
      r.final = p.url(); r.titulo = await p.title();
      const txt = await p.evaluate(() => document.body ? document.body.innerText : '');
      fs.writeFileSync(path.join(OUT, nome + '.txt'), txt);
      r.chars = txt.length;
      r.altura = await p.evaluate(() => document.body ? document.body.scrollHeight : 0);
      r.links = await p.evaluate(() => [...document.querySelectorAll('a[href]')].map(a => a.href));
      r.checkout = [...new Set(r.links.filter(h => /kiwify|hotmart|eduzz|monetizze|greenn|ticto|perfectpay|kirvano|cakto|lastlink|pay\.|checkout/i.test(h)))].slice(0, 5);
      r.precos = [...new Set((txt.match(/R\$\s?\d{1,4}(?:[.,]\d{2})?/g) || []))].slice(0, 12);
      r.ctas = await p.evaluate(() => [...document.querySelectorAll('a,button')].map(e => (e.innerText || '').trim()).filter(t => t && t.length < 60).slice(0, 40));
      delete r.links;
      await p.screenshot({ path: path.join(OUT, nome + '.jpg'), fullPage: true, type: 'jpeg', quality: 55, clip: undefined }).catch(e => r.erro_print = String(e));
      if (r.checkout[0]) {
        const q = await ctx.newPage();
        await q.goto(r.checkout[0], { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {});
        await q.waitForTimeout(2500);
        r.checkout_final = q.url();
        fs.writeFileSync(path.join(OUT, nome + '.checkout.txt'), await q.evaluate(() => document.body ? document.body.innerText : ''));
        await q.screenshot({ path: path.join(OUT, nome + '.checkout.jpg'), fullPage: true, type: 'jpeg', quality: 55 }).catch(() => {});
      }
    } catch (e) { r.erro = String(e).slice(0, 200); }
    res.push(r); console.log(JSON.stringify(r).slice(0, 300));
    await ctx.close();
  }
  fs.writeFileSync(path.join(OUT, 'resumo.json'), JSON.stringify(res, null, 1));
  await b.close();
})();
