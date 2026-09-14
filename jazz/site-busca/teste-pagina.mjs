import { chromium } from 'playwright';
const F = 'file://' + new URL('.', import.meta.url).pathname.replace(/\/$/,'') + '/index.html';
const erros = [];
const b = await chromium.launch();
const ok = (n,c)=>console.log((c?'PASS':'FALHA')+' · '+n);
let p = await (await b.newContext()).newPage();
p.on('pageerror', e => erros.push(String(e)));
p.on('console', m => { if (m.type()==='error' && !/ERR_CERT_AUTHORITY_INVALID/.test(m.text())) erros.push('console: '+m.text()); });
await p.goto(F); await p.waitForTimeout(400);

const nCards = await p.locator('.card').count();
ok('cards renderizam na carga ('+nCards+')', nCards > 0);

// busca
await p.fill('#q','apartamento 3 quartos em Boa Viagem ate 800 mil');
await p.press('#q','Enter'); await p.waitForTimeout(300);
const n2 = await p.locator('.card').count();
ok('busca por frase retorna resultados ('+n2+')', n2 > 0);

// URL compartilhavel
const url = p.url();
ok('URL carrega ?q= da busca', /[?&]q=/.test(url));

// ficha
await p.locator('.card .card-body').first().click(); await p.waitForTimeout(250);
ok('clique no card abre a ficha', await p.locator('#ficha').evaluate(d=>d.open));
const temWa = await p.locator('#ficha a[href*="wa.me"]').count();
ok('ficha tem botao WhatsApp', temWa === 1);
await p.keyboard.press('Escape'); await p.waitForTimeout(200);
ok('Esc fecha a ficha', !(await p.locator('#ficha').evaluate(d=>d.open)));

// refino reescreve a barra
const antes = await p.inputValue('#q');
await p.selectOption('#rf-quartos','2'); await p.waitForTimeout(300);
const depois = await p.inputValue('#q');
ok('refino reescreve a frase da barra', depois !== antes && /2 quartos/.test(depois));

// favoritos
await p.locator('.fav').first().click(); await p.waitForTimeout(200);
const salvos = await p.evaluate(()=>JSON.parse(localStorage.getItem('jazz-favoritos')||'[]'));
ok('favorito persiste no localStorage ('+salvos.length+')', salvos.length === 1);
await p.reload(); await p.waitForTimeout(400);
const marcado = await p.locator('.fav[aria-pressed="true"]').count();
ok('favorito sobrevive ao reload', marcado === 1);

// round-trip do link
const p2 = await (await b.newContext()).newPage();
p2.on('pageerror', e => erros.push('p2: '+String(e)));
await p2.goto(F + '?q=' + encodeURIComponent('casa em Casa Forte'));
await p2.waitForTimeout(400);
ok('link ?q= reabre a mesma busca', (await p2.inputValue('#q')) === 'casa em Casa Forte' && (await p2.locator('.card').count()) > 0);

ok('zero erros de JS', erros.length === 0);
if (erros.length) console.log(erros.join('\n'));
await b.close();

process.exit(erros.length ? 1 : 0);
