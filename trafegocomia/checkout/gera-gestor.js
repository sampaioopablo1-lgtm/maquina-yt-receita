// uso: FONTES_DIR=... node gera.js pasta_saida
// Imagens dos componentes do checkout da Kiwify (Clube Trafego com IA).
// No celular o formulario vem primeiro: o que vende tem de estar nas imagens ACIMA dele.
// Netflix Padrao R$ 51,90 desde 15/10/2026 (Mobilebit/Diario da Midia). 29,90/30 = 0,997.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const out = path.resolve(process.argv[2]); fs.mkdirSync(out, { recursive: true });
const F = process.env.FONTES_DIR;
const top = `<div class="top"><span class="brand">📢 IA</span><span class="handle">@trafegocom.ia</span></div>`;
// Medido no runner (trafegocomia/pesquisa/lps/desktop/medidas.json): no computador o checkout tem 984 px;
// o cabecalho ocupa 984, a coluna principal ~670 e a lateral ~284. No celular tudo vira ~390.
// Regra: nenhum texto abaixo de ~15 px na tela MENOR em que a imagem aparece.
//  - imagens 1080 de largura: menor texto 44 px (celular 390/1080 -> 15,9 px; computador 670/1080 -> 27 px)
//  - cabecalho 2000x590: menor texto 80 px (celular 390/2000 -> 15,6 px; computador 984/2000 -> 39 px)
//  - coluna lateral (284 px): NAO usar imagem com texto; usar componente de texto nativo da Kiwify.
const B = [
  ['01-topo', 1080, 756, '74px', `<span class="tag" style="font-size:44px">PRA GESTOR DE TRÁFEGO</span>
    <h1>Conecte a IA ao Gerenciador e <span class="k">atenda mais clientes</span></h1>
    <div style="color:#fff;font-weight:900;font-size:46px;line-height:1.25">Relatório, variações e campanhas<br>pedidos em português.</div>
    <span class="seta" style="font-size:46px">↓ Preencha abaixo e entre agora</span>`],
  ['03-como-funciona', 1080, 1080, '84px', `<span class="tag" style="font-size:44px">COMO FUNCIONA</span>
    <h1>Do pedido à campanha <span class="k">em 3 passos</span></h1>
    <div class="pasos">
      <div class="ps"><span class="n">1</span><span class="t" style="font-size:48px">Conecte a IA à conta, uma vez</span></div>
      <div class="ps"><span class="n">2</span><span class="t" style="font-size:48px">Peça em português</span></div>
      <div class="ps"><span class="n">3</span><span class="t" style="font-size:48px">Revise e publique: nada roda sem você</span></div></div>`],
  ['06-exit-popup', 1080, 1080, '104px', `<span class="tag" style="font-size:44px">ESPERA</span>
    <h1>É <span class="k">menos de R$ 1</span> por dia</h1>
    <div class="sub">R$ 29,90 por mês pra tirar o operacional da sua agenda. Cancele quando quiser.</div>
    <span class="cta">Quero entrar →</span>`],
];
(async () => {
  const b = await chromium.launch(); const base = fs.readFileSync(path.join(__dirname, 'bloco.html'), 'utf8');
  for (const [nome, W, H, hs, html] of B) {
    const page = base.replace('FONT900', 'file://' + F + '/montserrat-latin-900-normal.woff2')
      .replace('FONT800', 'file://' + F + '/montserrat-latin-800-normal.woff2')
      .replace('WPX', W + 'px').replace('HPX', H + 'px').replace('HSIZE', hs).replace('GLOWTOP', (H * 0.2) + 'px').replace('CONTEUDO', html);
    const tmp = path.join(out, '_tmp.html'); fs.writeFileSync(tmp, page);
    const p = await b.newPage({ viewport: { width: W, height: H } });
    await p.goto('file://' + tmp); await p.evaluate(() => document.fonts.ready);
    const sh = await p.evaluate(() => document.getElementById('wrap').scrollHeight);
    if (sh > H) console.log('ATENCAO transbordou:', nome, sh);
    await p.screenshot({ path: path.join(out, nome + '.png') }); await p.close(); fs.unlinkSync(tmp);
  }
  await b.close();
})();
