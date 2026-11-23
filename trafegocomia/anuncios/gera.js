// uso: FONTES_DIR=... node gera.js pasta_saida
// Gera os criativos estaticos do @trafegocom.ia em 4:5 (1080x1350) e 9:16 (1080x1920).
// Textos so com o que esta na bio do perfil: nada de depoimento ou resultado inventado.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const out = path.resolve(process.argv[2]); fs.mkdirSync(out, { recursive: true });
const F = process.env.FONTES_DIR;
const top = `<div class="top"><span class="brand">📢 IA</span><span class="handle">@trafegocom.ia</span></div>`;
const cta = `<span class="cta">Saiba mais →</span>`;
const preco = `<div class="price">Clube por <b>R$ 29,90/mês</b> · cancele quando quiser</div>`;
const C = {
  '01-pare-de-impulsionar': `${top}<span class="tag">ERRO Nº 1</span>
    <h1>Impulsionar post é <span class="k">jogar dinheiro fora</span></h1>
    <div class="sub">Aprenda a criar anúncios com IA no Gerenciador e trazer clientes pro seu WhatsApp.</div>
    ${cta}${preco}`,
  '02-anuncio-em-10s': `${top}<span class="tag">COM IA</span>
    <h1>Seu anúncio <span class="b">pronto</span> em 10 segundos</h1>
    <div class="card">
      <div class="bub me"><div class="lab">Você</div>Crie 3 anúncios para a minha pizzaria no bairro</div>
      <div class="bub ai"><div class="lab">IA</div>1. "Fome às 20h? A pizza chega antes da novela."<br>2. "Borda recheada grátis no 1º pedido."</div>
    </div>
    ${cta}${preco}`,
  '03-menos-de-1-real': `${top}<span class="tag">CLUBE TRÁFEGO COM IA</span>
    <h1>Menos de <span class="k">R$ 1 por dia</span></h1>
    <div class="card">
      <div class="it"><span class="ck">✓</span>Anúncios com IA</div>
      <div class="it"><span class="ck">✓</span>Para donos de negócio</div>
      <div class="it"><span class="ck">✓</span>Mais clientes no WhatsApp, gastando menos</div>
    </div>
    ${cta}${preco}`,
  '04-meta-ja-usa-ia': `${top}<span class="emoji">🤖</span>
    <h1>A Meta já usa IA pra escolher <span class="k">quem vê</span> seu anúncio</h1>
    <div class="sub">E você ainda cria no improviso? Aprenda a usar IA do seu lado.</div>
    ${cta}${preco}`,
};
(async () => {
  const b = await chromium.launch(); const base = fs.readFileSync(path.join(__dirname, 'criativo.html'), 'utf8');
  for (const [nome, html] of Object.entries(C)) {
    for (const [fmt, H, hs, gt] of [['feed', 1350, '104px', '200px'], ['stories', 1920, '118px', '420px']]) {
      const page = base.replace('FONT900', 'file://' + F + '/montserrat-latin-900-normal.woff2')
        .replace('FONT800', 'file://' + F + '/montserrat-latin-800-normal.woff2')
        .replace('HPX', H + 'px').replace('HSIZE', hs).replace('GLOWTOP', gt).replace('CONTEUDO', html);
      const tmp = path.join(out, '_tmp.html'); fs.writeFileSync(tmp, page);
      const p = await b.newPage({ viewport: { width: 1080, height: H } });
      await p.goto('file://' + tmp); await p.evaluate(() => document.fonts.ready);
      // guarda: nada pode transbordar da tela
      const over = await p.evaluate(() => document.getElementById('wrap').scrollHeight > window.innerHeight);
      if (over) console.log('ATENCAO transbordou:', nome, fmt, await p.evaluate(() => document.getElementById('wrap').scrollHeight));
      await p.screenshot({ path: path.join(out, `${nome}-${fmt}.png`) }); await p.close();
      fs.unlinkSync(tmp);
    }
  }
  await b.close();
})();
