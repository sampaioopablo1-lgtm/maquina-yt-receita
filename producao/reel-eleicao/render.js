/**
 * Reel tipografico 1080x1920 — gancho da eleicao (ORGANICO, nunca anuncio).
 *
 * Por que organico: anuncio que menciona eleicao cai na politica de "temas
 * sociais, eleicoes ou politica" da Meta (exige autorizacao e selo) e, pela
 * Lei das Eleicoes, impulsionamento eleitoral so pode ser contratado por
 * candidato, partido, federacao ou coligacao. Agencia nao esta na lista.
 *
 * Sem candidato, sem partido, sem lado. O gancho e o calendario, nao a disputa.
 *
 * Uso:  node producao/reel-eleicao/render.js [saida.mp4]
 * Saida padrao: producao/reel-eleicao/out/reel-eleicao.mp4
 */
const { createCanvas, GlobalFonts } = require('@napi-rs/canvas')
const { spawn } = require('child_process')
const fs = require('fs')
const path = require('path')

const W = 1080, H = 1920, FPS = 30
const NAVY = '#0F2137', CREME = '#FAF8F5', AMBAR = '#E8A33D', FOSCO = '#7C8CA0'

// ---------------------------------------------------------------- tipografia
// As fontes nao sao versionadas (ver .gitignore): baixa na hora, igual ao
// resto da esteira.
const DIR_FONTES = path.join(__dirname, '..', '..', 'fontes', 'montserrat')
const PESOS = { 300: 'Montserrat-300.ttf', 600: 'Montserrat-600.ttf', 800: 'Montserrat-800.ttf' }

async function baixaFontes () {
  fs.mkdirSync(DIR_FONTES, { recursive: true })
  for (const [peso, arquivo] of Object.entries(PESOS)) {
    const destino = path.join(DIR_FONTES, arquivo)
    if (fs.existsSync(destino) && fs.statSync(destino).size > 50000) continue
    const css = await (await fetch(
      `https://fonts.googleapis.com/css2?family=Montserrat:wght@${peso}&display=swap`,
      { headers: { 'User-Agent': 'Mozilla/5.0' } }
    )).text()
    const url = css.match(/https:\/\/fonts\.gstatic\.com[^)]+/)[0]
    const ttf = Buffer.from(await (await fetch(url)).arrayBuffer())
    fs.writeFileSync(destino, ttf)
  }
  GlobalFonts.registerFromPath(path.join(DIR_FONTES, PESOS[300]), 'MontLight')
  GlobalFonts.registerFromPath(path.join(DIR_FONTES, PESOS[600]), 'MontMedio')
  GlobalFonts.registerFromPath(path.join(DIR_FONTES, PESOS[800]), 'MontBold')
}

// -------------------------------------------------------------------- roteiro
// cada cena: [inicio, fim] em segundos + linhas. `destaque` pinta a palavra
// em ambar sem quebrar o alinhamento (a linha e medida inteira antes).
const CENAS = [
  { t: [0.0, 3.2], fonte: 'MontBold', corpo: 128, cor: CREME,
    linhas: ['DOMINGO', 'O PAÍS', 'DECIDE.'], pontoAmbar: true },
  { t: [3.2, 6.4], fonte: 'MontBold', corpo: 128, cor: CREME,
    linhas: ['SEGUNDA,', 'QUEM DECIDE', 'É VOCÊ.'], pontoAmbar: true },
  { t: [6.4, 9.6], fonte: 'MontLight', corpo: 104, cor: CREME,
    linhas: ['Eleição', 'não traz', 'cliente.'] },
  { t: [9.6, 13.0], fonte: 'MontLight', corpo: 96, cor: FOSCO,
    linhas: ['Nem crise.', 'Nem governo.', 'Nem juro.'] },
  { t: [13.0, 16.4], fonte: 'MontMedio', corpo: 104, cor: CREME,
    linhas: ['Cliente vem de', 'anúncio', 'rodando.'], destaque: 2 },
]
const FIM = [16.4, 20.0]   // assinatura
const DURACAO = FIM[1]

// ----------------------------------------------------------------- utilidades
const clamp = (v, a, b) => Math.min(b, Math.max(a, v))
const easeOut = t => 1 - Math.pow(1 - clamp(t, 0, 1), 3)
const easeIn = t => Math.pow(clamp(t, 0, 1), 3)

function linhaCentrada (ctx, texto, y, corpo, fonte, cor, alpha, desloca) {
  ctx.font = `${corpo}px ${fonte}`
  ctx.globalAlpha = alpha
  ctx.fillStyle = cor
  ctx.textAlign = 'center'
  ctx.fillText(texto, W / 2, y + desloca)
  ctx.globalAlpha = 1
}

function fundo (ctx) {
  ctx.fillStyle = NAVY
  ctx.fillRect(0, 0, W, H)
  // vinheta discreta: tira o ar de slide de PowerPoint
  const g = ctx.createRadialGradient(W / 2, H / 2, H * 0.25, W / 2, H / 2, H * 0.72)
  g.addColorStop(0, 'rgba(0,0,0,0)')
  g.addColorStop(1, 'rgba(0,0,0,0.38)')
  ctx.fillStyle = g
  ctx.fillRect(0, 0, W, H)
}

function barra (ctx, t) {
  const p = clamp(t / DURACAO, 0, 1)
  ctx.fillStyle = 'rgba(250,248,245,0.14)'
  ctx.fillRect(80, H - 120, W - 160, 6)
  ctx.fillStyle = AMBAR
  ctx.fillRect(80, H - 120, (W - 160) * p, 6)
}

function assinatura (ctx, t) {
  const [ini, fim] = FIM
  const local = t - ini
  const e = easeOut(local / 0.7)
  const y = H / 2 - 40

  ctx.textAlign = 'center'
  ctx.font = '96px MontBold'
  ctx.globalAlpha = e
  ctx.fillStyle = CREME
  ctx.fillText('O PRÓXIMO', W / 2, y + (1 - e) * 40)

  // "CLIENTE" com o tracking esticado ate bater a largura da linha de cima,
  // que e a regra do logotipo.
  const alvo = ctx.measureText('O PRÓXIMO').width
  ctx.font = '96px MontLight'
  const palavra = 'CLIENTE'
  const bruto = ctx.measureText(palavra).width
  const espaco = (alvo - bruto) / (palavra.length - 1)
  let x = W / 2 - alvo / 2
  ctx.textAlign = 'left'
  const e2 = easeOut((local - 0.18) / 0.7)
  ctx.globalAlpha = e2
  for (const ch of palavra) {
    ctx.fillText(ch, x, y + 118 + (1 - e2) * 40)
    x += ctx.measureText(ch).width + espaco
  }
  // o ponto ambar, que e o unico elemento grafico da marca
  ctx.globalAlpha = easeOut((local - 0.45) / 0.5)
  ctx.fillStyle = AMBAR
  ctx.beginPath()
  ctx.arc(W / 2 + alvo / 2 + 34, y - 8, 15, 0, Math.PI * 2)
  ctx.fill()

  // chamada
  ctx.globalAlpha = easeOut((local - 0.9) / 0.6) * (1 - easeIn((local - 3.0) / 0.6))
  ctx.textAlign = 'center'
  ctx.font = '52px MontMedio'
  ctx.fillStyle = FOSCO
  ctx.fillText('comenta PRÓXIMO que eu te explico', W / 2, y + 300)
  ctx.globalAlpha = 1
}

function cena (ctx, c, t) {
  const [ini, fim] = c.t
  const local = t - ini
  const saida = fim - t
  const n = c.linhas.length
  const alturaLinha = c.corpo * 1.18
  const topo = H / 2 - ((n - 1) * alturaLinha) / 2

  c.linhas.forEach((texto, i) => {
    const entra = easeOut((local - i * 0.13) / 0.55)
    const some = 1 - easeIn((0.55 - saida) / 0.55)
    const alpha = clamp(entra, 0, 1) * clamp(some, 0, 1)
    if (alpha <= 0.001) return
    const desloca = (1 - entra) * 52 - (1 - clamp(some, 0, 1)) * 26
    const cor = (c.destaque === i) ? AMBAR : c.cor
    linhaCentrada(ctx, texto, topo + i * alturaLinha, c.corpo, c.fonte, cor, alpha, desloca)

    // o ponto final da ultima linha em ambar, mesma marca da assinatura
    if (c.pontoAmbar && i === n - 1 && texto.endsWith('.')) {
      ctx.font = `${c.corpo}px ${c.fonte}`
      const larg = ctx.measureText(texto).width
      const pt = ctx.measureText('.').width
      ctx.globalAlpha = alpha
      ctx.fillStyle = AMBAR
      ctx.textAlign = 'left'
      ctx.fillText('.', W / 2 + larg / 2 - pt, topo + i * alturaLinha + desloca)
      ctx.globalAlpha = 1
    }
  })
}

// ---------------------------------------------------------------------- render
async function main () {
  await baixaFontes()
  const saida = process.argv[2] || path.join(__dirname, 'out', 'reel-eleicao.mp4')
  fs.mkdirSync(path.dirname(saida), { recursive: true })

  const ff = spawn('ffmpeg', [
    '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', 'pipe:0',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
    '-movflags', '+faststart', saida,
  ], { stdio: ['pipe', 'ignore', 'pipe'] })
  let erroFF = ''
  ff.stderr.on('data', d => { erroFF += d.toString() })

  const canvas = createCanvas(W, H)
  const ctx = canvas.getContext('2d')
  const total = Math.round(DURACAO * FPS)

  for (let f = 0; f < total; f++) {
    const t = f / FPS
    fundo(ctx)
    const c = CENAS.find(c => t >= c.t[0] && t < c.t[1])
    if (c) cena(ctx, c, t)
    else if (t >= FIM[0]) assinatura(ctx, t)
    barra(ctx, t)

    const png = canvas.toBuffer('image/png')
    if (!ff.stdin.write(png)) await new Promise(r => ff.stdin.once('drain', r))
  }
  ff.stdin.end()

  const code = await new Promise(r => ff.on('close', r))
  if (code !== 0) { console.error(erroFF.split('\n').slice(-15).join('\n')); process.exit(1) }
  console.log(`${saida}  ${total} quadros  ${DURACAO}s  ${W}x${H}@${FPS}`)
}

main().catch(e => { console.error(e); process.exit(1) })
