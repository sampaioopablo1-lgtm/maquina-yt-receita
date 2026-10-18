// Renderiza capa.html em PNG no tamanho recomendado pelo Facebook (1640×624).
// Uso: NODE_PATH=$(npm root -g) node render.js
//      (gera capa-1640x624.png e capa-preview-celular.png)
const { chromium } = require("playwright");
const { pathToFileURL } = require("node:url");
const { join } = require("node:path");

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1640, height: 624 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(join(__dirname, "capa.html")).href);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: join(__dirname, "capa-1640x624.png"), clip: { x: 0, y: 0, width: 1640, height: 624 } });
  // Recorte que o celular mostra: os 1280 px centrais (o Facebook corta as laterais).
  await page.screenshot({ path: join(__dirname, "capa-preview-celular.png"), clip: { x: 180, y: 0, width: 1280, height: 624 } });
  await browser.close();
  console.log("ok: capa-1640x624.png e capa-preview-celular.png");
})();
