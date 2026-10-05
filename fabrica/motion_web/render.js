const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(__dirname, 'quadro.html'));
  await p.waitForFunction(() => document.fonts.status === 'loaded');
  const el = await p.$('#s');
  for (let on = 0; on < 120; on++) {
    await p.evaluate(n => window.quadro(n), on);
    await el.screenshot({ path: path.join(__dirname, 'frames', String(on).padStart(4,'0') + '.jpg'), type: 'jpeg', quality: 96 });
  }
  const fim = await p.evaluate(() => window.quadro(119));
  console.log('ultimo quadro:', JSON.stringify(fim));
  await b.close();
})();
