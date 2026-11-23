// uso: FONTES_DIR=... node gera-gestor.js pasta_saida
// Criativos para GESTOR DE TRAFEGO (publico consciente): mostrar a solucao, nao ensinar o basico.
// Sem numero de resultado inventado; conversa marcada como ilustracao.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const out = path.resolve(process.argv[2]); fs.mkdirSync(out, { recursive: true });
const F = process.env.FONTES_DIR;
const top = `<div class="top"><span class="brand">📢 IA</span><span class="handle">@trafegocom.ia</span></div>`;
const cta = `<span class="cta">Saiba mais →</span>`;
const preco = `<div class="price">Clube por <b>R$ 29,90/mês</b> · cancele quando quiser</div>`;
const C = {
  'g1-operacional': `${top}<span class="tag">PRA GESTOR DE TRÁFEGO</span>
    <h1>O operacional está comendo <span class="k">sua agenda</span></h1>
    <div class="card">
      <div class="it"><span class="ck" style="background:#EF4444;color:#fff">✕</span>Relatório montado à mão</div>
      <div class="it"><span class="ck" style="background:#EF4444;color:#fff">✕</span>6 abas pra comparar conjunto</div>
      <div class="it"><span class="ck" style="background:#EF4444;color:#fff">✕</span>Cliente novo = mais horas suas</div></div>
    ${cta}${preco}`,
  'g2-conversa': `${top}<span class="tag">IA NO GERENCIADOR</span>
    <h1>Pergunte em <span class="k">português</span></h1>
    <div class="card">
      <div class="bub me"><div class="lab">Você</div>Qual conjunto está acima do CPA alvo nesta semana?</div>
      <div class="bub ai"><div class="lab">IA</div>O conjunto 2 da campanha B. Sugiro pausar e mover a verba pro 1.</div></div>
    <div class="price" style="font-size:28px;opacity:.7">Ilustração do processo</div>
    ${cta}`,
  'g3-mais-clientes': `${top}<span class="tag">GESTOR AUTÔNOMO</span>
    <h1>Mais clientes, <span class="k">mesma agenda</span></h1>
    <div class="sub">Conecte a IA ao Gerenciador: relatório, variações e campanhas em minutos. Tudo nasce pausado pra você revisar.</div>
    ${cta}${preco}`,
  'g4-estrategia': `${top}<span class="emoji">🧠</span>
    <h1>A IA faz o braço. <span class="k">Você faz a estratégia.</span></h1>
    <div class="sub">Pare de vender hora de operacional. Venda resultado.</div>
    ${cta}${preco}`,
};
(async () => {
  const b = await chromium.launch(); const base = fs.readFileSync(path.join(__dirname, 'criativo.html'), 'utf8');
  for (const [nome, html] of Object.entries(C)) {
    for (const [fmt, H, hs, gt] of [['feed', 1350, '100px', '200px'], ['stories', 1920, '114px', '420px']]) {
      const page = base.replace('FONT900', 'file://' + F + '/montserrat-latin-900-normal.woff2')
        .replace('FONT800', 'file://' + F + '/montserrat-latin-800-normal.woff2')
        .replace('HPX', H + 'px').replace('HSIZE', hs).replace('GLOWTOP', gt).replace('CONTEUDO', html);
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
