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
// Modelados nos estaticos validados da Biblioteca (trafegocomia/pesquisa/analise-2026-11-23.md):
// 05 carrossel = estrutura Tintim/Pai do Low Ticket (carrossel 7-10 cards, 174-243 dias), gancho Hotmart
//    ("nao parou de funcionar, mas nao funciona como antes: a IA decide quem ve");
// 06 carrossel = estrutura Pablo Sehn (273 dias): "a IA nao substitui, acelera" + lista do que ela faz;
// 07 imagem = LM (173 dias): contraponto "nao e mais diferencial, e essencial";
// 08 imagem = Clube DeliveryAds / Anuncios para Corretores (173 e 110 dias): fala com UM tipo de negocio.
C['07-essencial'] = `${top}<span class="tag">2026</span>
    <h1>Anunciar não é mais diferencial. <span class="k">É essencial.</span></h1>
    <div class="sub">A diferença é saber anunciar do jeito certo, com IA do seu lado.</div>
    ${cta}${preco}`;
C['08-negocio-local'] = `${top}<span class="emoji">🍕✂️🦷</span>
    <h1>Pizzaria, salão, clínica: <span class="k">anúncio com IA</span> pro seu bairro</h1>
    <div class="sub">Clientes chamando no seu WhatsApp, sem depender de agência.</div>
    ${cta}${preco}`;
C['09-claude-gerenciador'] = `${top}<span class="tag">CLAUDE + META ADS</span>
    <h1>Conecte o Claude ao seu <span class="k">Gerenciador</span></h1>
    <div class="card">
      <div class="bub me"><div class="lab">Você</div>Cria uma campanha de mensagens pra minha pizzaria. R$ 10 por dia, até 3 km daqui.</div>
      <div class="bub ai"><div class="lab">Claude</div>Pronto: campanha, público e 3 anúncios criados. Tudo em pausa para você revisar. ✓</div>
    </div>
    ${cta}${preco}`;
const SW = '<span class="swipe">Arraste →</span>';
const CAR = {
  '05-carrossel-mudou': [
    `${top}<span class="tag">ATENÇÃO</span><h1>O tráfego pago não parou de funcionar.</h1><div class="big">Ele <span style="color:#3B82F6">mudou.</span></div>${SW}`,
    `<span class="emoji">🤖</span><h1>Hoje a IA da Meta decide <span class="k">quem vê</span> seu anúncio</h1><div class="sub">Quando, onde e pra quem. Bem menos botão pra você apertar.</div>${SW}`,
    `<span class="emoji">🎨</span><h1>O que sobrou pra você é o <span class="k">criativo</span></h1><div class="sub">A imagem e o texto viraram a principal alavanca.</div>${SW}`,
    `<span class="tag">ERRO COMUM</span><h1>Subir <span class="k">1 anúncio</span> e torcer</h1><div class="sub">Sem comparação, você não sabe se o problema é o texto, a imagem ou a oferta.</div>${SW}`,
    `<span class="emoji">⚡</span><h1>Com IA você cria <span class="k">3 versões</span> em minutos</h1><div class="sub">Sobe as três e deixa o resultado escolher a melhor.</div>${SW}`,
    `${top}<h1>Aprenda a anunciar <span class="k">com IA</span> do seu lado</h1><div class="sub">Clube Tráfego com IA, pra dono de negócio.</div>${cta}${preco}`,
  ],
  '06-carrossel-acelera': [
    `${top}<h1>A IA não faz seu anúncio <span class="k">sozinha.</span></h1><div class="big">Ela <span style="color:#3B82F6">acelera</span> você.</div>${SW}`,
    `<span class="emoji">✍️</span><h1>Escreve o <span class="k">texto</span></h1><div class="sub">Você descreve o negócio, ela devolve várias versões.</div>${SW}`,
    `<span class="emoji">🧪</span><h1>Cria <span class="k">variações</span> pra testar</h1><div class="sub">Gancho de problema, de resultado, de pergunta.</div>${SW}`,
    `<span class="emoji">📊</span><h1>Ajuda a <span class="k">ler o resultado</span></h1><div class="sub">Você cola os números e pergunta o que cortar e o que manter.</div>${SW}`,
    `<span class="tag">O SEGREDO</span><h1>Não é usar IA. É <span class="k">saber usar.</span></h1>${SW}`,
    `${top}<h1>Aprenda no <span class="k">Clube Tráfego com IA</span></h1><div class="sub">Anúncios com IA pra trazer clientes pro WhatsApp.</div>${cta}${preco}`,
  ],
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
  for (const [nome, slides] of Object.entries(CAR)) {
    for (let i = 0; i < slides.length; i++) {
      const page = base.replace('FONT900', 'file://' + F + '/montserrat-latin-900-normal.woff2')
        .replace('FONT800', 'file://' + F + '/montserrat-latin-800-normal.woff2')
        .replace('HPX', '1350px').replace('HSIZE', '96px').replace('GLOWTOP', (i % 2 ? '500px' : '150px'))
        .replace('CONTEUDO', `<span class="num">${i + 1}/${slides.length}</span>` + slides[i]);
      const tmp = path.join(out, '_tmp.html'); fs.writeFileSync(tmp, page);
      const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
      await p.goto('file://' + tmp); await p.evaluate(() => document.fonts.ready);
      const over = await p.evaluate(() => document.getElementById('wrap').scrollHeight > window.innerHeight);
      if (over) console.log('ATENCAO transbordou:', nome, i + 1);
      await p.screenshot({ path: path.join(out, `${nome}-${i + 1}.png`) }); await p.close(); fs.unlinkSync(tmp);
    }
  }
  await b.close();
})();
