// Monta o checkout com as larguras MEDIDAS da Kiwify e tira print no computador e no celular.
const path = require('path'), fs = require('fs'); const { chromium } = require('playwright');
const D = path.resolve(process.argv[2]); const OUT = path.resolve(process.argv[3]);
const u = f => 'file://' + path.join(D, f);
const campos = n => Array.from({ length: n }, (_, i) => `<div class="in">${['Nome', 'E-mail', 'Telefone', 'CPF'][i]}</div>`).join('');
const lado = `<div class="lado"><div class="bx">✓ Acesso imediato após o pagamento</div><div class="bx">✓ Pix ou cartão</div><div class="bx">✓ 7 dias de garantia</div><div class="bx">✓ Cancele quando quiser</div></div>`;
const html = movel => `<html><body style="margin:0;background:#0b0f19;font-family:sans-serif">
<style>.c{width:${movel ? 'auto' : '984px'};margin:0 auto;padding:${movel ? '0' : '16px 0'}} img{display:block;width:100%}
.g{display:flex;gap:22px;margin-top:16px;${movel ? 'flex-direction:column;gap:0' : ''}} .m{flex:0 0 ${movel ? 'auto' : '672px'}} .lado{flex:1;${movel ? 'padding:12px' : ''}}
.f{background:#fff;border-radius:8px;padding:${movel ? '14px' : '24px'};margin-top:${movel ? 0 : 16}px} .in{border:1px solid #ccc;border-radius:6px;padding:14px;margin:0 0 12px;color:#888;font-size:16px}
.bt{background:#22c55e;color:#fff;text-align:center;font-weight:bold;padding:16px;border-radius:6px;font-size:18px}
.bx{background:#fff;border:2px solid #1d4ed8;border-radius:8px;padding:16px;margin-bottom:14px;font-weight:bold;font-size:16px;color:#111}</style>
<div class="c"><img src="${u('02-cabecalho.png')}"><div class="g"><div class="m"><img src="${u('01-topo.png')}">
<div class="f">${campos(3)}<div class="bt">Pagar agora · R$ 29,90/mês</div></div>
<img src="${u('03-como-funciona.png')}" style="margin-top:16px"><img src="${u('04-preco.png')}" style="margin-top:16px"><img src="${u('05-garantia.png')}" style="margin-top:16px"></div>${lado}</div></div></body></html>`;
(async () => {
  const b = await chromium.launch();
  for (const [nome, vp, mv] of [['computador-1440', { width: 1440, height: 900 }, false], ['celular-390', { width: 390, height: 844, deviceScaleFactor: 2 }, true]]) {
    const t = path.join(OUT, '_sim.html'); fs.writeFileSync(t, html(mv));
    const p = await b.newPage({ viewport: vp }); await p.goto('file://' + t); await p.waitForTimeout(500);
    await p.screenshot({ path: path.join(OUT, `simulacao-${nome}.png`) });
    await p.screenshot({ path: path.join(OUT, `simulacao-${nome}-inteira.png`), fullPage: true });
    await p.close(); fs.unlinkSync(t);
  }
  await b.close();
})();
