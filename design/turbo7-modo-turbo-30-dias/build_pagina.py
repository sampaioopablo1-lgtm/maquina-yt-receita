#!/usr/bin/env python3
"""Monta a página web de apresentação do flyer (Artifact autocontido).

Fontes e imagem entram como data URI: a página não faz nenhuma requisição
externa, o que é exigência do ambiente onde ela é publicada.
"""

import base64
import io
from pathlib import Path

from PIL import Image

from build import CADENCIA, CALL, CALL_WA, INCLUSOS, MSG

RAIZ = Path(__file__).parent
LARGURA_WEB = 1600  # o flyer nasce com 2400px; 1600 basta para leitura em tela

CANAIS = {
    MSG: ("Mensagem de WhatsApp", "msg"),
    CALL_WA: ("Ligação pelo WhatsApp", "callwa"),
    CALL: ("Ligação convencional", "call"),
}


def fonte(nome: str) -> str:
    dados = base64.b64encode((RAIZ / "fonts" / nome).read_bytes()).decode()
    return f"data:font/ttf;base64,{dados}"


def flyer_web() -> str:
    with Image.open(RAIZ / "flyer-turbo7-modo-turbo-30-dias.png") as im:
        altura = round(im.height * LARGURA_WEB / im.width)
        menor = im.resize((LARGURA_WEB, altura), Image.LANCZOS)
        buf = io.BytesIO()
        menor.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def toques() -> str:
    linhas = []
    for i, (dia, canal) in enumerate(CADENCIA, 1):
        rotulo, classe = CANAIS[canal]
        linhas.append(
            f'<li class="toque {classe}">'
            f'<span class="toque-n">{i:02d}</span>'
            f'<span class="toque-dia">Dia {dia}</span>'
            f'<span class="toque-canal">{rotulo}</span></li>'
        )
    return "\n".join(linhas)


def escopo() -> str:
    return "\n".join(
        f'<div class="escopo-item"><h3>{titulo}</h3><p>{desc}</p></div>'
        for _, titulo, desc in INCLUSOS
    )


PAGINA = """<title>Modo Turbo 30 Dias — Turbo 7</title>
<style>
@font-face{{font-family:'BigShoulders';src:url('{big}') format('truetype');font-weight:700;font-display:block;}}
@font-face{{font-family:'Outfit';src:url('{outfit}') format('truetype');font-weight:400;font-display:block;}}
@font-face{{font-family:'OutfitB';src:url('{outfit_b}') format('truetype');font-weight:700;font-display:block;}}
@font-face{{font-family:'GeistMono';src:url('{mono}') format('truetype');font-weight:400;font-display:block;}}

:root{{
  --ground:#F4F2F7; --surface:#FFFFFF; --ink:#1B0A2E; --muted:#6B5B7D;
  --line:rgba(27,10,46,.14); --accent:#4E0FA3; --accent-ink:#FFFFFF;
  --chip:rgba(78,15,163,.08);
  --msg:#3D8B0B; --callwa:#3D8B0B; --call:#6B5B7D;
}}
@media (prefers-color-scheme:dark){{
  :root{{
    --ground:#120320; --surface:#1C0733; --ink:#F2ECF8; --muted:#B3A2C6;
    --line:rgba(255,255,255,.14); --accent:#7CF01E; --accent-ink:#0E0318;
    --chip:rgba(124,240,30,.11);
    --msg:#7CF01E; --callwa:#7CF01E; --call:#D6DAE2;
  }}
}}
:root[data-theme="dark"]{{
  --ground:#120320; --surface:#1C0733; --ink:#F2ECF8; --muted:#B3A2C6;
  --line:rgba(255,255,255,.14); --accent:#7CF01E; --accent-ink:#0E0318;
  --chip:rgba(124,240,30,.11);
  --msg:#7CF01E; --callwa:#7CF01E; --call:#D6DAE2;
}}
:root[data-theme="light"]{{
  --ground:#F4F2F7; --surface:#FFFFFF; --ink:#1B0A2E; --muted:#6B5B7D;
  --line:rgba(27,10,46,.14); --accent:#4E0FA3; --accent-ink:#FFFFFF;
  --chip:rgba(78,15,163,.08);
  --msg:#3D8B0B; --callwa:#3D8B0B; --call:#6B5B7D;
}}

*{{box-sizing:border-box;}}
body{{margin:0;background:var(--ground);color:var(--ink);
  font-family:'Outfit',system-ui,sans-serif;font-size:17px;line-height:1.6;
  -webkit-font-smoothing:antialiased;}}

.wrap{{max-width:1080px;margin:0 auto;padding:56px 28px 96px;
  display:flex;flex-direction:column;gap:64px;}}

.eyebrow{{font-family:'GeistMono',monospace;font-size:11px;letter-spacing:.22em;
  text-transform:uppercase;color:var(--muted);}}

/* topo */
.topo{{display:flex;flex-direction:column;gap:22px;}}
.marca{{display:flex;align-items:baseline;gap:14px;}}
.marca .nome{{font-family:'BigShoulders',sans-serif;font-weight:700;font-size:40px;
  line-height:.8;letter-spacing:.01em;}}
.marca .nome em{{font-style:normal;color:var(--accent);}}
h1{{font-family:'BigShoulders',sans-serif;font-weight:700;font-size:clamp(46px,8vw,84px);
  line-height:.94;letter-spacing:-.01em;margin:0;text-transform:uppercase;text-wrap:balance;}}
h1 em{{font-style:normal;color:var(--accent);}}
.lide{{max-width:60ch;color:var(--muted);font-size:19px;margin:0;}}

/* prancha do flyer */
figure{{margin:0;display:flex;flex-direction:column;gap:14px;}}
figure img{{display:block;width:100%;height:auto;border:1px solid var(--line);
  box-shadow:0 22px 60px rgba(12,3,24,.28);}}
figcaption{{font-family:'GeistMono',monospace;font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--muted);}}

/* seções */
section{{display:flex;flex-direction:column;gap:24px;}}
h2{{font-family:'OutfitB',sans-serif;font-weight:700;font-size:15px;letter-spacing:.10em;
  text-transform:uppercase;margin:0;padding-bottom:12px;border-bottom:1px solid var(--line);}}

/* cadência — sequência real, por isso numerada */
.toques{{list-style:none;margin:0;padding:0;
  display:grid;grid-template-columns:repeat(auto-fill,minmax(158px,1fr));gap:1px;
  background:var(--line);border:1px solid var(--line);}}
.toque{{background:var(--surface);padding:16px 16px 18px;
  display:flex;flex-direction:column;gap:3px;}}
.toque-n{{font-family:'GeistMono',monospace;font-size:10px;letter-spacing:.18em;
  color:var(--muted);}}
.toque-dia{{font-family:'BigShoulders',sans-serif;font-weight:700;font-size:30px;
  line-height:.9;font-variant-numeric:tabular-nums;}}
.toque-canal{{font-size:13.5px;line-height:1.35;color:var(--muted);
  padding-left:15px;position:relative;}}
.toque-canal::before{{content:"";position:absolute;left:0;top:7px;width:8px;height:8px;
  border-radius:50%;}}
.msg .toque-canal::before{{background:var(--msg);}}
.callwa .toque-canal::before{{background:transparent;border:2px solid var(--callwa);}}
.call .toque-canal::before{{background:transparent;border:2px solid var(--call);}}

/* escopo */
.escopo{{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:1px;
  background:var(--line);border:1px solid var(--line);}}
.escopo-item{{background:var(--surface);padding:22px 24px 24px;
  display:flex;flex-direction:column;gap:7px;}}
.escopo-item h3{{font-family:'OutfitB',sans-serif;font-weight:700;font-size:16px;
  line-height:1.3;margin:0;text-transform:uppercase;letter-spacing:.02em;}}
.escopo-item p{{margin:0;font-size:15px;color:var(--muted);}}

/* oferta */
.oferta{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1px;
  background:var(--line);border:1px solid var(--line);}}
.preco{{background:var(--surface);padding:26px 26px 28px;
  display:flex;flex-direction:column;gap:6px;}}
.preco .rot{{font-family:'GeistMono',monospace;font-size:10.5px;letter-spacing:.20em;
  text-transform:uppercase;color:var(--muted);}}
.preco .val{{font-family:'BigShoulders',sans-serif;font-weight:700;font-size:56px;
  line-height:.88;font-variant-numeric:tabular-nums;}}
.preco.gratis .val{{color:var(--accent);}}
.preco .nota{{font-size:14.5px;color:var(--muted);}}

.cta{{display:inline-flex;align-items:center;gap:12px;align-self:flex-start;
  background:var(--accent);color:var(--accent-ink);text-decoration:none;
  padding:17px 26px;font-family:'BigShoulders',sans-serif;font-weight:700;
  font-size:26px;line-height:1;text-transform:uppercase;letter-spacing:.01em;
  transition:transform .16s ease,filter .16s ease;}}
.cta:hover{{transform:translateY(-2px);filter:brightness(1.06);}}
.cta:focus-visible{{outline:3px solid var(--accent);outline-offset:4px;}}
.cta span{{font-family:'GeistMono',monospace;font-size:13px;letter-spacing:.10em;}}
@media (prefers-reduced-motion:reduce){{.cta{{transition:none;}}.cta:hover{{transform:none;}}}}

/* ficha */
.ficha{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:22px;}}
.ficha div{{display:flex;flex-direction:column;gap:4px;}}
.ficha dt{{font-family:'GeistMono',monospace;font-size:10.5px;letter-spacing:.20em;
  text-transform:uppercase;color:var(--muted);}}
.ficha dd{{margin:0;font-size:15.5px;}}

.ressalva{{border-left:3px solid var(--accent);padding:2px 0 2px 18px;
  color:var(--muted);font-size:15px;max-width:70ch;}}

footer{{border-top:1px solid var(--line);padding-top:22px;
  display:flex;flex-wrap:wrap;gap:14px;justify-content:space-between;align-items:baseline;
  font-family:'GeistMono',monospace;font-size:10.5px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--muted);}}
footer a{{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line);}}
footer a:hover{{border-bottom-color:var(--accent);}}
</style>

<div class="wrap">

  <header class="topo">
    <div class="marca">
      <span class="nome">TURBO<em>7</em></span>
      <span class="eyebrow">Marketing de Planejados</span>
    </div>
    <h1>Programa Modo Turbo<br><em>30 dias</em></h1>
    <p class="lide">Cadência comercial de 12 contatos ao longo de 30 dias, playbook de
      vendas, CRM implantado e um diretor de performance acompanhando o time. Esta é a
      peça de divulgação do programa.</p>
  </header>

  <figure>
    <img src="{flyer}" width="1600" height="2400"
         alt="Flyer do Programa Modo Turbo 30 Dias, com o mapa de cadência 12 por 30,
              o escopo do programa e a oferta de 30 dias gratuitos.">
    <figcaption>Flyer — 2400 × 3600 px · também disponível em PDF para impressão</figcaption>
  </figure>

  <section>
    <h2>A cadência 12 × 30</h2>
    <ol class="toques">
{toques}
    </ol>
  </section>

  <section>
    <h2>O que está incluso</h2>
    <div class="escopo">
{escopo}
    </div>
  </section>

  <section>
    <h2>Investimento</h2>
    <div class="oferta">
      <div class="preco">
        <span class="rot">Valor do programa</span>
        <span class="val">R$ 20.000</span>
        <span class="nota">Implementação completa, playbook, CRM e gestão comercial.</span>
      </div>
      <div class="preco gratis">
        <span class="rot">Você começa pagando</span>
        <span class="val">R$ 0</span>
        <span class="nota">Nos primeiros 30 dias. Condição exclusiva para novos clientes.</span>
      </div>
    </div>
    <a class="cta" href="https://www.turbo7.com.br" target="_blank" rel="noopener">
      Reserve sua vaga <span>WWW.TURBO7.COM.BR</span></a>
  </section>

  <section>
    <h2>Ficha técnica</h2>
    <dl class="ficha">
      <div><dt>Formato</dt><dd>Vertical 2:3</dd></div>
      <div><dt>Imagem</dt><dd>PNG 2400 × 3600 px</dd></div>
      <div><dt>Impressão</dt><dd>PDF, 1 página, 12,5 × 18,75 in</dd></div>
      <div><dt>Tipografia</dt><dd>Big Shoulders, Outfit, Geist Mono</dd></div>
    </dl>
    <p class="ressalva">As estatísticas da peça — “+80% das conversões vêm da 4ª tentativa
      em diante” e “5 novos leads por dia” — são alegações da campanha, não números
      medidos. Vale conferir a fonte antes de veicular.</p>
  </section>

  <footer>
    <span>Turbo 7 · Programa Modo Turbo</span>
    <a href="https://www.turbo7.com.br" target="_blank" rel="noopener">turbo7.com.br</a>
  </footer>

</div>
"""


if __name__ == "__main__":
    destino = RAIZ / "apresentacao.html"
    destino.write_text(
        PAGINA.format(
            big=fonte("BigShoulders-Bold.ttf"),
            outfit=fonte("Outfit-Regular.ttf"),
            outfit_b=fonte("Outfit-Bold.ttf"),
            mono=fonte("GeistMono-Regular.ttf"),
            flyer=flyer_web(),
            toques=toques(),
            escopo=escopo(),
        ),
        encoding="utf-8",
    )
    print(f"{destino.name}  ({destino.stat().st_size // 1024} KB)")
