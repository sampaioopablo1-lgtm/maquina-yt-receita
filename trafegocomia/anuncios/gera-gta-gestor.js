// uso: FONTES_DIR=... node gera-gta.js pasta_saida
// Modelos da Biblioteca: trafegocomia/pesquisa/analise-gta6-2026-11-23.md (11 = espera, Kong Games;
// 12 = licao de marketing, Bruno Ads; 13 = ancora de preco, Kong Games).
// Variacoes "GTA 6" (lancado em 19/11/2026). Paleta de por do sol de cidade de praia como
// REFERENCIA de clima; sem logo, arte, personagem ou fonte do jogo: e citacao de noticia.
// Numeros: lancamento 19/11/2026 e US$ 3,79 bi no 1o dia (Rockstar via Forbes/IstoE/Olhar
// Digital); edicao padrao R$ 449,90 (Tecnoblog/Investidor10/Canaltech). 449,90/29,90 = 15,05.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const out = path.resolve(process.argv[2]); fs.mkdirSync(out, { recursive: true });
const F = process.env.FONTES_DIR;
const top = `<div class="top"><span class="brand">📢 IA</span><span class="handle">@trafegocom.ia</span></div>`;
const cta = `<span class="cta">Saiba mais →</span>`;
const preco = `<div class="price">Clube por <b>R$ 29,90/mês</b> · cancele quando quiser</div>`;
const C = {
  'gta-11-13-anos': `${top}<span class="tag">LANÇOU 19/11</span>
    <h1>GTA 6 levou <span class="k">13 anos</span> pra sair.</h1>
    <div class="paineis">
      <div class="p"><span class="e">🎮</span><span class="t">13 anos</span></div>
      <div class="p"><span class="e">🤖</span><span class="t">vs minutos</span></div>
      <div class="p"><span class="e">📊</span><span class="t">campanha pronta</span></div></div>
    <div class="sub">A campanha do seu cliente não precisa: peça à IA no Gerenciador e revise antes de publicar.</div>
    ${cta}${preco}`,
  'gta-12-trailer': `${top}<span class="tag">US$ 3,79 BI NO 1º DIA</span>
    <h1>Antes de vender, <span class="k">testaram trailers.</span></h1>
    <div class="sub">O criativo é o trailer. Com IA, mais variações pros seus clientes, sem mais horas.</div>
    <div class="paineis">
      <div class="p"><span class="e">🎬</span><span class="t">variação</span></div>
      <div class="p"><span class="e">📊</span><span class="t">teste</span></div>
      <div class="p"><span class="e">🏆</span><span class="t">vencedor</span></div></div>
    ${cta}`,
  'gta-13-15-meses': `${top}<span class="tag">A CONTA</span>
    <h1>1 GTA 6 = <span class="k">15 meses</span> de Clube</h1>
    <div class="vs">
      <div class="box a"><div class="r">GTA 6</div><div class="v">R$ 449,90</div><div class="s">você joga</div></div>
      <div class="box b"><div class="r">Clube Tráfego com IA</div><div class="v">R$ 29,90</div><div class="s">por mês · tira o operacional</div></div></div>
    ${cta}
    <div class="nota">GTA 6 edição padrão no Brasil, nov/2026 · plano da IA cobrado à parte</div>`,
};
(async () => {
  const b = await chromium.launch(); const base = fs.readFileSync(path.join(__dirname, 'criativo-vc.html'), 'utf8');
  for (const [nome, html] of Object.entries(C)) {
    for (const [fmt, H, hs, sol, mar] of [['feed', 1350, '104px', '160px', '260px'], ['stories', 1920, '118px', '260px', '420px']]) {
      const page = base.replace('FONT900', 'file://' + F + '/montserrat-latin-900-normal.woff2')
        .replace('FONT800', 'file://' + F + '/montserrat-latin-800-normal.woff2')
        .replace('HPX', H + 'px').replace('HSIZE', hs).replace('SOLB', sol).split('MARH').join(mar).replace('CONTEUDO', html);
      const tmp = path.join(out, '_tmp.html'); fs.writeFileSync(tmp, page);
      const p = await b.newPage({ viewport: { width: 1080, height: H } });
      await p.goto('file://' + tmp); await p.evaluate(() => document.fonts.ready);
      const sh = await p.evaluate(() => document.getElementById('wrap').scrollHeight);
      if (sh > H) console.log('ATENCAO transbordou:', nome, fmt, sh);
      await p.screenshot({ path: path.join(out, `${nome}-${fmt}.png`) }); await p.close(); fs.unlinkSync(tmp);
    }
  }
  await b.close();
})();
