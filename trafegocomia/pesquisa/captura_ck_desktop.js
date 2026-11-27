// Mede o layout do checkout Kiwify no computador: largura das colunas e de cada imagem.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const OUT = 'trafegocomia/pesquisa/lps/desktop'; fs.mkdirSync(OUT, { recursive: true });
const URLS = ['https://pay.kiwify.com.br/6D9z3sn', 'https://pay.kiwify.com.br/3gOJi2z'];
(async () => {
  const b = await chromium.launch(); const res = [];
  for (const [vw, vh] of [[1440, 900], [1280, 720], [1920, 1080]]) {
    for (const url of URLS) {
      const ctx = await b.newContext({ viewport: { width: vw, height: vh }, locale: 'pt-BR' });
      const p = await ctx.newPage();
      await p.goto(url, { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {});
      await p.waitForTimeout(3000);
      const m = await p.evaluate(() => {
        const r = e => { const b = e.getBoundingClientRect(); return { x: Math.round(b.x), y: Math.round(b.y + scrollY), w: Math.round(b.width), h: Math.round(b.height) }; };
        const imgs = [...document.images].filter(i => i.getBoundingClientRect().width > 80).map(i => ({ src: i.src.slice(0, 90), nat: [i.naturalWidth, i.naturalHeight], ...r(i) }));
        const form = [...document.querySelectorAll('input')].filter(i => i.getBoundingClientRect().width > 100).map(r);
        const btn = [...document.querySelectorAll('button')].filter(b => /pagar|comprar|finalizar|pay/i.test(b.innerText)).map(r);
        return { imgs, form: form.slice(0, 3), btn, altura: document.body.scrollHeight };
      });
      const nome = url.split('/').pop() + '-' + vw;
      await p.screenshot({ path: path.join(OUT, nome + '.jpg'), type: 'jpeg', quality: 60 });
      await p.screenshot({ path: path.join(OUT, nome + '-inteira.jpg'), type: 'jpeg', quality: 50, fullPage: true });
      res.push({ url, vw, vh, ...m }); console.log(JSON.stringify({ url, vw, ...m }).slice(0, 600));
      await ctx.close();
    }
  }
  fs.writeFileSync(path.join(OUT, 'medidas.json'), JSON.stringify(res, null, 1)); await b.close();
})();
