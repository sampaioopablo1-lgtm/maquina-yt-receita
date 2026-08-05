#!/usr/bin/env python3
"""Gera o mapa de funil: onde termina o marketing e onde começa vendas.

Peça irmã do flyer, mesma linguagem visual (ver FILOSOFIA-DE-DESIGN.md). Aqui o
argumento é a fronteira: o funil afunila, mas o que a peça precisa provar é
*quem responde por cada etapa* e em que ponto o bastão troca de mão.
"""

from pathlib import Path

RAIZ = Path(__file__).parent

MKT, VND = "mkt", "vnd"

# etapa -> (dono, nome, o que acontece, meta)
# As metas numéricas vêm do briefing do programa; as demais são definições de
# "pronto" — deliberadamente não são KPIs inventados.
ETAPAS = [
    (MKT, "Atração",
     "Anúncios, conteúdo e presença de marca geram demanda qualificada.",
     "5 novos leads por dia no topo", "Marketing"),
    (MKT, "Captura",
     "Formulário, WhatsApp e direct viram registro único no CRM.",
     "Contato e origem registrados", "Marketing"),
    (MKT, "Qualificação",
     "Perfil, interesse e momento de compra antes de virar tarefa de vendas.",
     "Lead classificado antes do repasse", "Marketing"),
    (VND, "Cadência 12 × 30",
     "12 toques em 30 dias, com 2 a 3 canais cruzados nos dias de pico.",
     "100 ligações por dia", "Captador"),
    (VND, "Agendamento",
     "Transformar a conversa em visita marcada na agenda.",
     "2 visitas agendadas por dia", "Captador"),
    (VND, "Visita e projeto",
     "Levantamento, apresentação do projeto e proposta.",
     "Proposta apresentada na visita", "Captador"),
    (VND, "Fechamento",
     "Negociação, contrato e assinatura.",
     "Contrato assinado", "Captador + Diretor"),
]

FRONTEIRA = {
    "titulo": "Passagem de bastão",
    "texto": "O lead vira <b>tarefa de vendas</b> no CRM. Antes disso, é do marketing; "
             "depois, é do captador. Sem essa linha, ninguém responde pelo lead parado.",
    "dono": "Quem responde pela fronteira: Diretor de Performance",
}

RODAPE = (
    "O Diretor de Performance acompanha as <b>duas pontas</b> — cobra o volume de leads "
    "do marketing e a execução da cadência em vendas. A reunião semanal é onde as duas "
    "metas se encontram."
)

LARGURA_TOPO, LARGURA_BASE = 100.0, 58.0   # % — o afunilamento


def faixa(i: int, dono: str, nome: str, desc: str, meta: str, resp: str) -> str:
    passo = (LARGURA_TOPO - LARGURA_BASE) / (len(ETAPAS) - 1)
    larg = LARGURA_TOPO - passo * i
    return f"""<div class="linha {dono}">
  <div class="faixa-col">
    <div class="faixa" style="width:{larg:.2f}%">
      <span class="et-n mono">{i + 1:02d}</span>
      <span class="et-nome">{nome}</span>
      <span class="et-desc sans">{desc}</span>
    </div>
  </div>
  <div class="dado">
    <span class="dado-k mono">Meta</span>
    <span class="dado-v sans-b">{meta}</span>
  </div>
  <div class="dado">
    <span class="dado-k mono">Responsável</span>
    <span class="dado-v sans-b">{resp}</span>
  </div>
</div>"""


def construir() -> str:
    corte = sum(1 for d, *_ in ETAPAS if d == MKT)
    fronteira = FRONTEIRA_HTML.format(**{f"f_{k}": v for k, v in FRONTEIRA.items()})
    linhas = []
    for i, (dono, nome, desc, meta, resp) in enumerate(ETAPAS):
        if i == corte:
            linhas.append(fronteira)
        linhas.append(faixa(i, dono, nome, desc, meta, resp))
    return TEMPLATE.format(
        linhas="".join(linhas), rodape=RODAPE,
        n_mkt=corte, n_vnd=len(ETAPAS) - corte,
    )


FRONTEIRA_HTML = """<div class="fronteira">
  <div class="fr-marca"></div>
  <div class="fr-corpo">
    <span class="fr-tag mono-b">{f_titulo}</span>
    <p class="fr-texto sans">{f_texto}</p>
    <p class="fr-dono mono">{f_dono}</p>
  </div>
</div>"""


TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Turbo 7 — Funil: marketing e vendas</title>
<style>
@font-face{{font-family:'BigShoulders';src:url('fonts/BigShoulders-Bold.ttf') format('truetype');font-weight:700;}}
@font-face{{font-family:'Outfit';src:url('fonts/Outfit-Bold.ttf') format('truetype');font-weight:700;}}
@font-face{{font-family:'Outfit';src:url('fonts/Outfit-Regular.ttf') format('truetype');font-weight:400;}}
@font-face{{font-family:'GeistMono';src:url('fonts/GeistMono-Bold.ttf') format('truetype');font-weight:700;}}
@font-face{{font-family:'GeistMono';src:url('fonts/GeistMono-Regular.ttf') format('truetype');font-weight:400;}}

:root{{
  --ink:#120320; --green:#7CF01E; --lilac:#A78BFA; --white:#FFFFFF;
  --slate:#B3A2C6; --hair:rgba(255,255,255,.13); --hair-soft:rgba(255,255,255,.065);
  --seam:rgba(255,255,255,.105);
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1200px;height:1584px;overflow:hidden;background:var(--ink);
  -webkit-font-smoothing:antialiased;}}

.page{{position:relative;width:1200px;height:1584px;overflow:hidden;
  background:radial-gradient(120% 62% at 50% -10%,#3D1168 0%,#270B45 40%,#180627 74%,#120320 100%);}}
.page .grid{{position:absolute;inset:0;
  background:repeating-linear-gradient(to right,rgba(255,255,255,.032) 0 1px,transparent 1px 48px),
             repeating-linear-gradient(to bottom,rgba(255,255,255,.032) 0 1px,transparent 1px 48px);
  -webkit-mask-image:radial-gradient(104% 76% at 50% 32%,#000 0%,rgba(0,0,0,.32) 56%,transparent 88%);}}
.page .glow{{position:absolute;inset:0;
  background:radial-gradient(70% 38% at 50% 112%,rgba(124,240,30,.11) 0%,transparent 60%);}}

.frame{{position:absolute;inset:54px 64px;display:flex;flex-direction:column;}}
.reg{{position:absolute;width:15px;height:15px;border:1px solid rgba(255,255,255,.20);}}
.reg.tl{{top:28px;left:32px;border-right:0;border-bottom:0;}}
.reg.tr{{top:28px;right:32px;border-left:0;border-bottom:0;}}
.reg.bl{{bottom:28px;left:32px;border-right:0;border-top:0;}}
.reg.br{{bottom:28px;right:32px;border-left:0;border-top:0;}}

.mono{{font-family:'GeistMono';font-weight:400;letter-spacing:.20em;text-transform:uppercase;}}
.mono-b{{font-family:'GeistMono';font-weight:700;letter-spacing:.20em;text-transform:uppercase;}}
.sans{{font-family:'Outfit';font-weight:400;}}
.sans-b{{font-family:'Outfit';font-weight:700;}}

/* HEADER */
.head{{display:flex;align-items:flex-end;justify-content:space-between;}}
.lockup{{display:flex;align-items:center;gap:15px;}}
.word .rule{{height:3px;background:var(--white);margin-bottom:6px;}}
.word .name{{font-family:'BigShoulders';font-weight:700;font-size:50px;line-height:.76;color:var(--white);}}
.word .name em{{font-style:normal;color:var(--green);}}
.word .tag{{font-family:'GeistMono';font-size:8.5px;letter-spacing:.40em;color:var(--slate);
  margin-top:7px;text-transform:uppercase;}}
.head .meta{{text-align:right;font-size:9.5px;color:var(--slate);line-height:2;}}
.head .meta b{{color:var(--white);font-weight:700;}}
.rule-full{{height:1px;background:var(--hair);margin-top:20px;}}

/* TITULO */
.kicker{{display:flex;align-items:center;gap:13px;margin-top:24px;}}
.kicker .dot{{width:7px;height:7px;background:var(--green);flex:none;box-shadow:0 0 11px rgba(124,240,30,.9);}}
.kicker .k{{font-size:10px;color:var(--green);}}
.kicker .sep{{flex:1;height:1px;background:var(--hair-soft);}}
.kicker .ref{{font-size:10px;color:var(--slate);}}
h1{{font-family:'BigShoulders';font-weight:700;text-transform:uppercase;font-size:82px;
  line-height:1.0;letter-spacing:-.007em;color:var(--white);margin-top:14px;}}
h1 em{{font-style:normal;color:var(--lilac);}}
h1 s{{text-decoration:none;color:var(--green);}}
.lide{{font-family:'Outfit';font-size:17.5px;line-height:1.5;color:#D6C9E4;margin-top:16px;
  max-width:78%;}}

/* CABECALHO DAS COLUNAS */
.colunas{{display:grid;grid-template-columns:1fr 260px 220px;gap:16px;margin-top:30px;
  padding-bottom:9px;border-bottom:1px solid var(--hair);}}
.colunas span{{font-size:9px;color:var(--slate);}}

/* FUNIL */
.linha{{display:grid;grid-template-columns:1fr 260px 220px;gap:16px;align-items:stretch;
  padding:9px 0;border-bottom:1px solid var(--hair-soft);}}
.faixa-col{{display:flex;justify-content:center;}}
.faixa{{position:relative;padding:13px 22px 14px 46px;display:flex;flex-direction:column;gap:3px;
  border:1px solid;}}
.linha.mkt .faixa{{border-color:rgba(167,139,250,.42);
  background:linear-gradient(100deg,rgba(167,139,250,.15),rgba(167,139,250,.045));}}
.linha.vnd .faixa{{border-color:rgba(124,240,30,.42);
  background:linear-gradient(100deg,rgba(124,240,30,.14),rgba(124,240,30,.04));}}
.et-n{{position:absolute;left:16px;top:15px;font-size:11px;}}
.linha.mkt .et-n{{color:var(--lilac);}}
.linha.vnd .et-n{{color:var(--green);}}
.et-nome{{font-family:'BigShoulders';font-weight:700;font-size:31px;line-height:.9;
  text-transform:uppercase;color:var(--white);}}
.et-desc{{font-size:13.5px;line-height:1.4;color:#C9BAD8;}}

.dado{{display:flex;flex-direction:column;gap:5px;justify-content:center;
  padding-left:16px;border-left:1px solid var(--hair-soft);}}
.dado-k{{font-size:8px;color:var(--slate);}}
.dado-v{{font-size:15px;line-height:1.3;color:var(--white);}}

/* FRONTEIRA */
.fronteira{{display:flex;align-items:stretch;margin:13px 0;
  border:1px solid rgba(124,240,30,.5);
  background:linear-gradient(100deg,rgba(124,240,30,.10),rgba(124,240,30,.03) 70%);}}
.fr-marca{{width:4px;background:var(--green);flex:none;}}
.fr-tag{{display:inline-block;background:var(--green);color:#0E0318;font-size:9px;
  padding:5px 11px 6px;margin-bottom:10px;}}
.fr-corpo{{padding:16px 24px 18px;flex:1;}}
.fr-texto{{font-size:17px;line-height:1.45;color:#EDE4F6;}}
.fr-texto b{{font-weight:700;color:var(--green);}}
.fr-dono{{font-size:9px;color:var(--green);margin-top:9px;}}

/* RODAPE */
.nota{{margin-top:22px;border-left:3px solid var(--green);padding:4px 0 4px 18px;}}
.nota p{{font-family:'Outfit';font-size:15.5px;line-height:1.5;color:#C9BAD8;max-width:88%;}}
.nota p b{{font-weight:700;color:var(--white);}}

.foot{{margin-top:auto;padding-top:20px;border-top:1px solid var(--hair);
  display:flex;align-items:center;justify-content:space-between;}}
.foot .l{{font-family:'BigShoulders';font-weight:700;font-size:22px;color:var(--white);line-height:1;}}
.foot .l em{{font-style:normal;color:var(--green);}}
.foot .c{{font-family:'GeistMono';font-size:8.5px;letter-spacing:.20em;text-transform:uppercase;color:var(--slate);}}

@page{{size:12.5in 16.5in;margin:0;}}
@media print{{html,body{{-webkit-print-color-adjust:exact;print-color-adjust:exact;}}}}
</style>
</head>
<body>
<div class="page">
  <div class="grid"></div><div class="glow"></div>
  <span class="reg tl"></span><span class="reg tr"></span>
  <span class="reg bl"></span><span class="reg br"></span>

  <div class="frame">

    <div class="head">
      <div class="lockup">
        <svg width="42" height="42" viewBox="0 0 40 40" fill="none">
          <path d="M20 3.6c4.8 5.3 7.2 11.4 7.2 18v6.6H12.8v-6.6c0-6.6 2.4-12.7 7.2-18Z"
                stroke="#7CF01E" stroke-width="1.7" stroke-linejoin="round"/>
          <circle cx="20" cy="16.6" r="3.3" stroke="#FFFFFF" stroke-width="1.7"/>
          <path d="M12.8 21.9 6.6 27.5v5.1l6.2-3.9ZM27.2 21.9l6.2 5.6v5.1l-6.2-3.9Z"
                stroke="#7CF01E" stroke-width="1.7" stroke-linejoin="round"/>
          <path d="M17.4 31.6h5.2" stroke="#FFFFFF" stroke-width="1.7" stroke-linecap="round"/>
        </svg>
        <div class="word">
          <div class="rule"></div>
          <div class="name">TURBO<em>7</em></div>
          <div class="tag">Marketing de Planejados</div>
        </div>
      </div>
      <div class="meta mono">
        <div><b>{n_mkt}</b> etapas de marketing</div>
        <div><b>{n_vnd}</b> etapas de vendas</div>
      </div>
    </div>
    <div class="rule-full"></div>

    <div class="kicker">
      <span class="dot"></span>
      <span class="k mono-b">Divisão de responsabilidade no funil</span>
      <span class="sep"></span>
      <span class="ref mono">Doc. T7 / 002</span>
    </div>

    <h1>Onde termina o <em>marketing</em>.<br>Onde começa <s>vendas</s>.</h1>
    <p class="lide">O funil é um só, mas o dono muda no meio do caminho. Este mapa mostra
      cada etapa, a meta que a define e quem responde por ela — para que nenhum lead fique
      parado na terra de ninguém.</p>

    <div class="colunas mono">
      <span>Etapa do funil</span><span>Meta da etapa</span><span>Responsável</span>
    </div>

    {linhas}

    <div class="nota"><p>{rodape}</p></div>

    <div class="foot">
      <div class="l">TURBO<em>7</em></div>
      <div class="c">Programa Modo Turbo · turbo7.com.br</div>
    </div>

  </div>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    (RAIZ / "funil.html").write_text(construir(), encoding="utf-8")
    print("funil.html gerado")
