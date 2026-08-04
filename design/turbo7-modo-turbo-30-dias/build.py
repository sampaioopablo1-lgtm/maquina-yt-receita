#!/usr/bin/env python3
"""Gera o flyer do Programa Modo Turbo 30 Dias (Turbo 7).

Emite `flyer.html`, renderizado depois para PNG/PDF via Chromium headless.
Filosofia visual: CADENCIA INSTRUMENTAL (ver FILOSOFIA-DE-DESIGN.md).
"""

from pathlib import Path

RAIZ = Path(__file__).parent

# ── sistema de canais ────────────────────────────────────────────────
MSG, CALL_WA, CALL = "msg", "call_wa", "call"

# dia do ciclo -> canais acionados naquele toque.
# 12 toques em 30 dias; nos dias de pico, 2 a 3 canais se cruzam no mesmo dia.
CADENCIA = [
    (1,  (CALL_WA, MSG)),
    (3,  (MSG,)),
    (5,  (CALL, MSG)),
    (7,  (CALL_WA, MSG)),
    (10, (MSG,)),
    (13, (CALL, CALL_WA, MSG)),
    (16, (MSG,)),
    (19, (CALL_WA, MSG)),
    (22, (MSG,)),
    (25, (CALL, MSG)),
    (28, (MSG,)),
    (30, (CALL, CALL_WA, MSG)),
]

# total de contatos individuais — derivado, para o texto nunca divergir do mapa
TOTAL_CONTATOS = sum(len(canais) for _, canais in CADENCIA)

# toques 3 e 4 (dias 5 e 7) = onde a maioria dos times desiste
ABANDONO = (3, 4)
CONVERSAO = (5, 12)

PATH_FONE = ("M6.6 4.4h3.4l1.6 4.1-2.1 1.3a10.8 10.8 0 0 0 4.8 4.8l1.3-2.1 4.1 1.6v3.4"
             "a1.7 1.7 0 0 1-1.8 1.7A15.9 15.9 0 0 1 4.9 6.2a1.7 1.7 0 0 1 1.7-1.8Z")
PATH_BALAO = ("M6.9 4.3h10.2a3.3 3.3 0 0 1 3.3 3.3v5.9a3.3 3.3 0 0 1-3.3 3.3h-6.6L6.2 20.1"
              "v-3.9a3.3 3.3 0 0 1-2.6-3.2V7.6a3.3 3.3 0 0 1 3.3-3.3Z")


def glifo(canal: str, d: int = 44) -> str:
    """Glifo de canal: um sistema, tres estados."""
    r = d / 2
    if canal == MSG:
        return f"""<svg class="gl" viewBox="0 0 {d} {d}" width="{d}" height="{d}">
  <circle cx="{r}" cy="{r}" r="{r - 0.75}" fill="#7CF01E"/>
  <g transform="translate({r - 13.2} {r - 13.2}) scale(1.1)">
    <path d="{PATH_BALAO}" fill="#150425"/>
    <g fill="#7CF01E"><circle cx="8.4" cy="10.4" r="1.15"/><circle cx="12" cy="10.4" r="1.15"/>
      <circle cx="15.6" cy="10.4" r="1.15"/></g>
  </g></svg>"""
    cor = "#7CF01E" if canal == CALL_WA else "#E2E6EC"
    fundo = "rgba(124,240,30,.10)" if canal == CALL_WA else "rgba(226,230,236,.09)"
    return f"""<svg class="gl" viewBox="0 0 {d} {d}" width="{d}" height="{d}">
  <circle cx="{r}" cy="{r}" r="{r - 0.9}" fill="{fundo}" stroke="{cor}" stroke-width="1.5"/>
  <g transform="translate({r - 13.2} {r - 13.2}) scale(1.1)"><path d="{PATH_FONE}" fill="{cor}"/></g></svg>"""


def coluna(i: int, dia: int, canais: tuple[str, ...]) -> str:
    pilha = "".join(glifo(c, 30) for c in canais)
    pico = " pico" if len(canais) > 1 else ""
    return f"""<div class="col">
  <div class="idx mono">{i:02d}</div>
  <div class="stem"></div>
  <div class="node{pico}"><span class="nd mono">Dia</span><span class="nn">{dia:02d}</span></div>
  <div class="stem"></div>
  <div class="axis-hit"></div>
  <div class="stem"></div>
  <div class="canais">{pilha}</div>
</div>"""


def cinta(inicio: int, fim: int, texto: str, tom: str) -> str:
    """Chave de anotacao sobre um intervalo de toques (1-indexado)."""
    esq = (inicio - 1) / 12 * 100
    larg = (fim - inicio + 1) / 12 * 100
    return f"""<div class="cinta {tom}" style="left:{esq:.4f}%;width:{larg:.4f}%">
  <div class="cinta-lbl mono-b">{texto}</div>
  <div class="cinta-arco"><i></i><span></span><i></i></div>
</div>"""


LEGENDA = [
    (MSG, "Mensagem<br>de WhatsApp"),
    (CALL_WA, "Ligação<br>pelo WhatsApp"),
    (CALL, "Ligação<br>convencional"),
]

INCLUSOS = [
    ("01", "Fluxo de cadência por etapa do funil",
     "O contato certo, na hora certa, para o estágio exato de cada cliente."),
    ("02", "Playbook de vendas de alta performance",
     "Scripts validados, regras de cadência, comissionamento e plano de carreira."),
    ("03", "Implementação do CRM Turbo 7 Go",
     "Sua central de comando. Nenhum lead perdido por falta de follow-up."),
]

# O acompanhamento semanal deixou de ser um item de lista: virou seção.
GESTAO_LEAD = "A meta é conquistada nos detalhes do dia a dia."
GESTAO_TEXTO = (
    "Reuniões semanais de performance com o time inteiro, conduzidas por um diretor "
    "que <b>acompanha desempenho, ajusta diariamente e traciona resultados</b> — não um "
    "gestor que só cobra o número no fim do mês."
)
METRICAS = [
    ("Volume", "Total de ligações por dia"),
    ("Alcance", "Mensagens enviadas por captador"),
    ("Qualidade", "Análise de contexto das conversas"),
]


def construir() -> str:
    colunas = "".join(coluna(i, d, cs) for i, (d, cs) in enumerate(CADENCIA, 1))
    cintas = (
        cinta(*ABANDONO, "Onde a maioria<br>dos times para", "alerta")
        + cinta(*CONVERSAO, "Zona de conversão — 80% das vendas acontecem aqui", "ok")
    )
    legenda = "".join(
        f'<div class="lg">{glifo(c, 26)}<span class="sans">{t}</span></div>'
        for c, t in LEGENDA
    )
    metricas = "".join(
        f'<div class="met"><span class="met-k mono">{k}</span>'
        f'<span class="met-v sans">{v}</span></div>'
        for k, v in METRICAS
    )
    inclusos = "".join(
        f"""<div class="item">
  <div class="item-n mono-b">{n}</div>
  <div class="item-t sans-b">{t}</div>
  <div class="item-d sans">{d}</div>
</div>"""
        for n, t, d in INCLUSOS
    )
    return TEMPLATE.format(colunas=colunas, cintas=cintas, legenda=legenda,
                           inclusos=inclusos, metricas=metricas,
                           total=TOTAL_CONTATOS, lead=GESTAO_LEAD,
                           texto=GESTAO_TEXTO)


TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Turbo 7 — Programa Modo Turbo 30 Dias</title>
<style>
@font-face{{font-family:'BigShoulders';src:url('fonts/BigShoulders-Bold.ttf') format('truetype');font-weight:700;}}
@font-face{{font-family:'BigShoulders';src:url('fonts/BigShoulders-Regular.ttf') format('truetype');font-weight:400;}}
@font-face{{font-family:'Outfit';src:url('fonts/Outfit-Bold.ttf') format('truetype');font-weight:700;}}
@font-face{{font-family:'Outfit';src:url('fonts/Outfit-Regular.ttf') format('truetype');font-weight:400;}}
@font-face{{font-family:'GeistMono';src:url('fonts/GeistMono-Bold.ttf') format('truetype');font-weight:700;}}
@font-face{{font-family:'GeistMono';src:url('fonts/GeistMono-Regular.ttf') format('truetype');font-weight:400;}}

:root{{
  --ink:#120320; --green:#7CF01E; --white:#FFFFFF;
  --slate:#B3A2C6; --silver:#E2E6EC; --red:#FF4438;
  --hair:rgba(255,255,255,.13); --hair-soft:rgba(255,255,255,.065);
  --seam:rgba(255,255,255,.105);
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1200px;height:2000px;overflow:hidden;background:var(--ink);
  -webkit-font-smoothing:antialiased;}}

.page{{position:relative;width:1200px;height:2000px;overflow:hidden;
  background:radial-gradient(122% 64% at 50% -10%,#3D1168 0%,#270B45 40%,#180627 74%,#120320 100%);}}
.page .grid{{position:absolute;inset:0;
  background:repeating-linear-gradient(to right,rgba(255,255,255,.032) 0 1px,transparent 1px 48px),
             repeating-linear-gradient(to bottom,rgba(255,255,255,.032) 0 1px,transparent 1px 48px);
  -webkit-mask-image:radial-gradient(104% 76% at 50% 32%,#000 0%,rgba(0,0,0,.32) 56%,transparent 88%);}}
.page .glow{{position:absolute;inset:0;
  background:radial-gradient(74% 40% at 50% 116%,rgba(124,240,30,.13) 0%,transparent 60%);}}

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
h1{{font-family:'BigShoulders';font-weight:700;text-transform:uppercase;font-size:100px;
  line-height:1.0;letter-spacing:-.007em;color:var(--white);margin-top:13px;}}
h1 em{{font-style:normal;color:var(--green);}}

/* ALERTA */
.alert{{margin-top:26px;display:flex;border:1px solid rgba(255,68,56,.32);background:rgba(255,68,56,.05);}}
.alert .bar{{width:4px;background:var(--red);flex:none;}}
.alert .body{{padding:14px 24px 15px;}}
.alert .lbl{{display:flex;align-items:center;gap:9px;font-size:9px;color:var(--red);margin-bottom:7px;}}
.alert .lbl i{{width:6px;height:6px;background:var(--red);border-radius:50%;box-shadow:0 0 9px rgba(255,68,56,.8);}}
.alert p{{font-family:'Outfit';font-size:18px;line-height:1.44;color:#EDE3F5;}}
.alert p b{{font-weight:700;color:var(--white);}}

/* FIGURA */
.figwrap{{margin-top:30px;}}
.figbar{{display:flex;align-items:baseline;justify-content:space-between;
  padding-bottom:10px;border-bottom:1px solid var(--hair);}}
.figbar .t{{font-family:'Outfit';font-weight:700;font-size:16px;color:var(--white);text-transform:uppercase;
  letter-spacing:.03em;}}
.figbar .t s{{text-decoration:none;color:var(--green);}}
.figbar .n{{font-size:9.5px;color:var(--slate);}}

.stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--seam);}}
.stat{{background:rgba(255,255,255,.020);padding:14px 20px 15px;}}
.stat .v{{font-family:'BigShoulders';font-weight:700;font-size:44px;line-height:.80;color:var(--green);}}
.stat .v small{{font-size:19px;}}
.stat .k{{font-family:'GeistMono';font-size:8.5px;letter-spacing:.15em;text-transform:uppercase;
  color:var(--slate);margin-top:8px;line-height:1.75;}}

/* DIAGRAMA */
.chart{{position:relative;margin-top:24px;}}
.cintas{{position:relative;height:44px;}}
.cinta{{position:absolute;bottom:0;padding:0 5px;}}
.cinta-lbl{{font-size:8.5px;text-align:center;line-height:1.3;margin-bottom:6px;}}
.cinta-arco{{display:flex;align-items:center;height:7px;}}
.cinta-arco i{{width:1px;height:7px;display:block;}}
.cinta-arco span{{flex:1;height:1px;}}
.cinta.alerta .cinta-lbl{{color:var(--red);}}
.cinta.alerta i,.cinta.alerta span{{background:rgba(255,68,56,.65);}}
.cinta.ok .cinta-lbl{{color:var(--green);}}
.cinta.ok i,.cinta.ok span{{background:rgba(124,240,30,.55);}}

.cols{{position:relative;display:grid;grid-template-columns:repeat(12,1fr);}}
.cols .axis{{position:absolute;left:0;right:0;top:100px;height:1px;
  background:repeating-linear-gradient(to right,rgba(255,255,255,.34) 0 5px,transparent 5px 11px);}}
.col{{display:flex;flex-direction:column;align-items:center;}}
.idx{{font-size:8px;height:12px;line-height:12px;color:rgba(255,255,255,.52);}}
.stem{{width:1px;height:14px;background:rgba(255,255,255,.26);}}
.node{{width:60px;height:60px;border-radius:50%;display:flex;flex-direction:column;
  align-items:center;justify-content:center;border:1px solid rgba(255,255,255,.34);
  background:radial-gradient(70% 70% at 50% 22%,rgba(255,255,255,.10),rgba(255,255,255,.022));}}
.node.pico{{border-color:rgba(124,240,30,.55);
  background:radial-gradient(70% 70% at 50% 22%,rgba(124,240,30,.13),rgba(255,255,255,.022));}}
.node .nd{{font-size:7px;color:var(--slate);line-height:1;margin-bottom:2px;}}
.node .nn{{font-family:'BigShoulders';font-weight:700;font-size:27px;line-height:.8;color:var(--white);}}
.axis-hit{{width:5px;height:5px;border-radius:50%;background:var(--white);margin:-2px 0;}}
.canais{{display:flex;flex-direction:column;align-items:center;gap:4px;}}
.gl{{display:block;}}

/* LEGENDA */
.legenda{{display:flex;align-items:center;gap:36px;margin-top:24px;padding-top:16px;
  border-top:1px solid var(--hair-soft);}}
.lg{{display:flex;align-items:center;gap:11px;}}
.lg span{{font-size:13px;line-height:1.32;color:#D8CEE4;}}
.nota{{margin-left:auto;text-align:right;font-family:'GeistMono';font-size:9px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--slate);line-height:1.85;}}
.nota b{{color:var(--green);font-weight:700;}}

/* INCLUSOS */
.sec{{display:flex;align-items:baseline;justify-content:space-between;margin-top:24px;
  padding-bottom:10px;border-bottom:1px solid var(--hair);}}
.sec .t{{font-family:'Outfit';font-weight:700;font-size:16px;color:var(--white);text-transform:uppercase;
  letter-spacing:.03em;}}
.sec .n{{font-size:9.5px;color:var(--slate);}}
.itens{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--seam);}}
.item{{background:rgba(255,255,255,.020);padding:15px 22px 16px;}}
.item-n{{font-size:9px;color:var(--green);margin-bottom:8px;}}
.item-t{{font-size:15.5px;line-height:1.24;color:var(--white);text-transform:uppercase;letter-spacing:.01em;}}
.item-d{{font-size:13px;line-height:1.45;color:#C3B5D2;margin-top:7px;}}

/* OFERTA */
.oferta{{margin-top:36px;border:1px solid rgba(124,240,30,.42);background:
  linear-gradient(105deg,rgba(124,240,30,.09) 0%,rgba(124,240,30,.03) 46%,rgba(124,240,30,.10) 100%);
  display:flex;align-items:stretch;}}
.of-l{{flex:1;padding:19px 26px 20px;display:flex;flex-direction:column;justify-content:center;border-right:1px solid rgba(124,240,30,.26);}}
.of-k{{font-family:'GeistMono';font-size:8.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--slate);}}
.of-v{{font-family:'BigShoulders';font-weight:700;font-size:52px;line-height:.86;color:var(--white);margin-top:9px;}}
.of-v small{{font-size:22px;color:var(--slate);}}
.of-s{{font-family:'Outfit';font-size:12.5px;color:#C3B5D2;margin-top:8px;line-height:1.4;}}
.of-r{{flex:1.12;padding:19px 26px 20px;}}
.of-r .of-v{{color:var(--green);font-size:68px;}}
.of-q{{font-family:'Outfit';font-weight:700;font-size:19px;letter-spacing:.01em;color:var(--green);
  margin-top:4px;text-transform:uppercase;}}
.of-r .of-v small{{color:var(--green);font-size:26px;}}

.cta{{margin-top:16px;display:flex;align-items:center;justify-content:space-between;
  background:var(--green);padding:20px 28px 21px;}}
.cta .a{{font-family:'BigShoulders';font-weight:700;font-size:34px;line-height:.9;color:#0E0318;
  text-transform:uppercase;letter-spacing:.005em;}}
.cta .b{{display:flex;align-items:center;gap:14px;}}
.cta .b span{{font-family:'GeistMono';font-weight:700;font-size:15px;letter-spacing:.10em;color:#0E0318;}}
.cta .b svg{{display:block;}}

/* GESTAO */
.gestao{{display:flex;border:1px solid rgba(124,240,30,.34);
  background:linear-gradient(100deg,rgba(124,240,30,.075) 0%,rgba(124,240,30,.022) 62%,rgba(124,240,30,.06) 100%);}}
.gestao .rail{{width:4px;background:var(--green);flex:none;}}
.gestao-corpo{{padding:17px 26px 19px;flex:1;}}
.gestao-lead{{font-family:'BigShoulders';font-weight:700;font-size:44px;line-height:.94;
  text-transform:uppercase;color:var(--green);letter-spacing:-.004em;}}
.gestao-txt{{font-family:'Outfit';font-size:16.5px;line-height:1.46;color:#E4DAEE;
  margin-top:9px;max-width:96%;}}
.gestao-txt b{{font-weight:700;color:var(--white);}}
.metricas{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(124,240,30,.24);
  margin-top:18px;border-top:1px solid rgba(124,240,30,.24);}}
.met{{background:rgba(18,3,32,.42);padding:12px 16px 13px;display:flex;flex-direction:column;gap:5px;}}
.met-k{{font-size:8px;color:var(--green);}}
.met-v{{font-size:14.5px;line-height:1.3;color:var(--white);}}

/* RODAPE */
.foot{{margin-top:13px;padding-top:22px;border-top:1px solid var(--hair);
  display:flex;align-items:center;justify-content:space-between;}}
.foot .l{{font-family:'BigShoulders';font-weight:700;font-size:22px;color:var(--white);line-height:1;}}
.foot .l em{{font-style:normal;color:var(--green);}}
.foot .c{{font-family:'GeistMono';font-size:8.5px;letter-spacing:.20em;text-transform:uppercase;color:var(--slate);}}

@page{{size:12.5in 20.8333in;margin:0;}}
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
        <div>Programa <b>Modo Turbo</b></div>
        <div>Ciclo de <b>30 dias</b></div>
      </div>
    </div>
    <div class="rule-full"></div>

    <div class="kicker">
      <span class="dot"></span>
      <span class="k mono-b">Fluxo de cadência 12 × 30</span>
      <span class="sep"></span>
      <span class="ref mono">Doc. T7 / 001</span>
    </div>

    <h1>Quem não faz follow-up<br>está deixando<br><em>dinheiro na meta.</em></h1>

    <div class="alert">
      <div class="bar"></div>
      <div class="body">
        <div class="lbl mono-b"><i></i> Alerta crítico de perda de receita</div>
        <p>A maioria das tentativas de contato morre no <b>3º ou 4º toque</b> — e é
           exatamente nesse buraco do funil que o negócio vaza.</p>
      </div>
    </div>

    <div class="figwrap">
      <div class="figbar">
        <div class="t">O novo padrão: <s>cadência 12 × 30</s></div>
        <div class="n mono">Fig. 01 — mapa de contatos</div>
      </div>
      <div class="stats">
        <div class="stat"><div class="v">12</div>
          <div class="k">Toques programados<br>ao longo do ciclo</div></div>
        <div class="stat"><div class="v">30<small> dias</small></div>
          <div class="k">Janela de cadência<br>espaçada</div></div>
        <div class="stat"><div class="v">+80<small>%</small></div>
          <div class="k">Das conversões vêm da<br>4ª tentativa em diante</div></div>
      </div>

      <div class="chart">
        <div class="cintas">{cintas}</div>
        <div class="cols"><div class="axis"></div>{colunas}</div>
      </div>

      <div class="legenda">
        {legenda}
        <div class="nota">Nos dias de pico, <b>2 a 3 canais</b> se cruzam no mesmo dia<br>
          {total} contatos no ciclo · alimentação de <b>5 novos leads por dia</b></div>
      </div>
    </div>

    <div class="sec">
      <div class="t">O que está incluso no programa</div>
      <div class="n mono">Tab. 01 — escopo</div>
    </div>
    <div class="itens">{inclusos}</div>

    <div class="sec">
      <div class="t">Acompanhamento de performance</div>
      <div class="n mono">Tab. 02 — gestão semanal</div>
    </div>
    <div class="gestao">
      <div class="rail"></div>
      <div class="gestao-corpo">
        <div class="gestao-lead">{lead}</div>
        <p class="gestao-txt">{texto}</p>
        <div class="metricas">{metricas}</div>
      </div>
    </div>

    <div class="oferta">
      <div class="of-l">
        <div class="of-k">Investimento do programa</div>
        <div class="of-v">R$ 20.000</div>
        <div class="of-s">Implementação completa, playbook, CRM e gestão comercial.</div>
      </div>
      <div class="of-r">
        <div class="of-k">Você começa pagando</div>
        <div class="of-v">R$ 0</div>
        <div class="of-q">nos primeiros 30 dias</div>
        <div class="of-s">Condição exclusiva para novos clientes. Veja o volume de vendas
          escalar antes de colocar a mão no bolso.</div>
      </div>
    </div>

    <div class="cta">
      <div class="a">Reserve sua vaga</div>
      <div class="b">
        <span>WWW.TURBO7.COM.BR</span>
        <svg width="30" height="12" viewBox="0 0 30 12" fill="none">
          <path d="M0 6h27M22.5 1.5 28 6l-5.5 4.5" stroke="#0E0318" stroke-width="2"
                stroke-linecap="square"/></svg>
      </div>
    </div>

    <div class="foot">
      <div class="l">TURBO<em>7</em></div>
      <div class="c">Vagas limitadas por ciclo · turbo7.com.br</div>
    </div>

  </div>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    (RAIZ / "flyer.html").write_text(construir(), encoding="utf-8")
    print("flyer.html gerado")
