#!/usr/bin/env python3
"""Monta a variação de venda da página: a proposta do Modo Turbo.

Mesma espinha da apresentação — funil, cadência, flyer, escopo, gestão e bônus —
na ordem que uma proposta comercial pede: primeiro o diagnóstico do problema,
depois o método, depois o plano de implantação e só então o preço. Quem lê o
valor antes de enxergar a goteira acha caro qualquer número.

Nada aqui é redigitado da apresentação: as seções compartilhadas são as mesmas
funções de `build_pagina`, então as duas páginas não conseguem divergir.
"""

from pathlib import Path

from build import GESTAO_LEAD, GESTAO_TEXTO, TOTAL_CONTATOS
from build_pagina import (CONTEXTO, CSS_BASE, bonus, escopo, fonte, funil,
                          metricas, toques)

RAIZ = Path(__file__).parent

# ---------------------------------------------------------------- oferta

MERCADO = 50_000       # valor de mercado do programa, a âncora
CLIENTE = 25_000       # preço para quem já é cliente
AVISTA = 20_000        # preço à vista — hoje fora da peça, mantido para retomar
PARCELAS = 6

# A peça mostra a mensalidade, não o valor cheio: é o número que o cliente compara
# com o próprio caixa. O total continua impresso ao lado da parcela — anunciar
# parcela sem informar o total, além de desonesto, é vedado pelo CDC.
MENSAL = CLIENTE / PARCELAS                               # R$ 4.166,67
DESCONTO_CLIENTE = round((1 - CLIENTE / MERCADO) * 100)   # 50%
DESCONTO_AVISTA = round((1 - AVISTA / MERCADO) * 100)     # 60%
ECONOMIA_AVISTA = CLIENTE - AVISTA                        # R$ 5.000


def moeda(valor: float, centavos: bool = False) -> str:
    texto = f"{valor:,.2f}" if centavos else f"{valor:,.0f}"
    return "R$ " + texto.replace(",", "·").replace(".", ",").replace("·", ".")


# ------------------------------------------------------------------ fases
#
# `janela` é (coluna inicial, coluna final) na régua de meses — a barra do
# cronograma sai daí, não de largura escrita à mão. A régua tem MESES colunas;
# a última é aberta, porque a escala não tem data de término.

MESES = ["Mês 1", "Mês 2", "Mês 3", "Mês 4 →"]

FASES = [
    (
        "Implementação e treinamento",
        "1 mês",
        (1, 2),
        "Colocar o processo de pé e o time operando a cadência.",
        [
            "CRM Turbo 7 Go implantado, com a base de leads migrada",
            "Playbook de vendas entregue e treinado com o time comercial",
            "Cadência 12 × 30 configurada e rodando no primeiro lote de leads",
            "Metas diárias definidas por captador",
        ],
        "Todo lead novo entra no CRM e tem a cadência iniciada no mesmo dia.",
    ),
    (
        "Medição e otimização do processo comercial",
        "2 meses",
        (2, 4),
        "Transformar a operação em número e corrigir o que o número mostra.",
        [
            "Reuniões semanais de performance conduzidas pelo diretor",
            "Acompanhamento de ligações por dia, mensagens por captador e "
            "análise de contexto das conversas",
            "Ajuste de script, horário de contato e ordem dos canais na cadência",
            "Correção do gargalo na passagem de bastão entre marketing e vendas",
        ],
        "As metas diárias — 100 ligações e 2 visitas agendadas — se sustentam "
        "semana após semana, e não só na semana boa.",
    ),
    (
        "Escala",
        "A partir do 3º mês",
        (3, 5),
        "Crescer volume sem perder a taxa de conversão conquistada.",
        [
            "Aumento do investimento em mídia com o custo por lead sob controle",
            "Playbook replicado para os novos captadores do time",
            "Meta individual por captador, com o bônus de performance valendo",
            "Revisão mensal do funil inteiro, de atração a fechamento",
        ],
        "Mais leads por mês sem estourar os R$ 50 de custo por lead nem derrubar "
        "a taxa de agendamento.",
    ),
]

CONTEXTO_FASES = (
    "O programa não entrega tudo no primeiro mês — e prometer isso seria o começo "
    "de uma frustração. São três fases, cada uma com um objetivo próprio e um sinal "
    "claro de que ela terminou. A terceira não tem data de fim: é o regime em que a "
    "operação passa a viver."
)

CONDICOES = [
    ("Desconto de cliente", f"Os {DESCONTO_CLIENTE}% de desconto valem para quem já é "
                            "cliente Turbo 7 com contrato ativo."),
    ("O que o valor cobre", "Implantação do CRM, playbook, treinamento do time e a "
                            "gestão semanal de performance. Tudo no mesmo valor."),
    # A terceira condição não repete o preço — o cartão já o mostrou. Ela responde
    # a pergunta seguinte do cliente: por quanto tempo isso dura.
    ("Vigência", "As três fases cobrem o primeiro trimestre. A fase de escala não "
                 "tem data de término: segue enquanto o programa estiver ativo."),
]


# ------------------------------------------------------------- diagnóstico
#
# As perguntas vêm antes do preço de propósito: quem não enxerga a goteira acha
# caro qualquer valor. Nenhuma delas é retórica — todas têm resposta numérica,
# e é exatamente por isso que funcionam: ou o número existe, ou ele está saindo
# caro. As três últimas cobrem o que as cinco primeiras deixam de fora — o lead
# que parou, o fundo do funil e o processo que mora na cabeça de uma pessoa só.

PERGUNTAS = [
    "Quantas ligações seu captador faz em cada lead até conseguir agendar uma visita?",
    "Depois da visita marcada, quantas ligações ele faz para o cliente realmente "
    "aparecer na loja?",
    "Quantas mensagens seus captadores enviam — e seguindo qual script? Ou cada um "
    "faz do seu jeito?",
    "Como o cliente é abordado na ligação? Qual é a primeira frase que ele ouve?",
    "Em quanto tempo um lead novo é respondido: minutos, horas ou no dia seguinte?",
    "Dos leads que entraram no mês passado, quantos pararam na segunda tentativa e "
    "nunca mais foram tocados?",
    "Das visitas agendadas na semana passada, quantas viraram proposta apresentada?",
    "Se o seu melhor captador sair amanhã, o método dele fica na empresa ou vai "
    "embora junto com ele?",
]

ABERTURA = (
    "Antes de olhar preço, responda estas {n} perguntas sobre a sua operação — em voz "
    "alta, agora, sem consultar ninguém. Nenhuma tem pegadinha: todas têm resposta "
    "numérica. Ou você sabe o número, ou ele está saindo caro."
)

VEREDITO_TITULO = "Cada “não sei dizer” é uma goteira"
VEREDITO = (
    "Se a maioria das respostas for “não sei dizer”, o problema da sua operação não é "
    "falta de lead. É goteira: venda que escapa gota a gota, sem barulho e sem culpado "
    "— e por isso ninguém conserta.<br><br>"
    "Nenhuma dessas perguntas exige um sistema caro para ser respondida. Exige processo "
    "escrito, cadência definida e alguém olhando o número toda semana. É exatamente "
    "isso que o Modo Turbo instala — e é por isso que a fase 2 inteira é medição."
)
VEREDITO_NOTA = (
    "Torneira pingando não estoura a conta de uma vez. Ela só faz a conta chegar "
    "maior todo mês."
)

# Ilustração própria, não banco de imagem: corpo cheio em --ink com especular em
# --surface para dar volume ao metal, gota e poça em --accent. Só tokens do tema,
# então um desenho serve ao claro e ao escuro. A gota é o dado, o pontilhado é a
# trajetória, os anéis são o acumulado — a peça inteira conta a mesma história.
TORNEIRA = """<svg class="torneira" viewBox="0 0 240 330" role="img"
     aria-label="Uma torneira pingando sobre uma poça: cada gota é uma venda que escapa.">
  <!-- a poça: o acumulado do que já vazou, em anéis -->
  <ellipse cx="184" cy="306" rx="44" ry="9" fill="var(--accent)" opacity=".10"/>
  <ellipse cx="184" cy="306" rx="30" ry="6" fill="var(--accent)" opacity=".14"/>
  <ellipse cx="184" cy="306" rx="16" ry="3.2" fill="var(--accent)" opacity=".22"/>

  <!-- a bancada termina antes do bico: o que cai, cai na cuba -->
  <path d="M28 268h112" stroke="var(--ink)" stroke-width="3" opacity=".2"
        stroke-linecap="round"/>

  <g fill="var(--ink)">
    <rect x="76" y="250" width="64" height="18" rx="7"/>
    <rect x="93" y="140" width="30" height="116" rx="11"/>
    <rect x="88" y="158" width="40" height="14" rx="5"/>
    <rect x="167" y="204" width="34" height="17" rx="5"/>
    <rect x="173" y="219" width="22" height="8" rx="4"/>
    <circle cx="50" cy="154" r="12"/>
  </g>
  <path d="M108 150c0-56 76-56 76 0v62" fill="none" stroke="var(--ink)"
        stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M108 178 56 156" fill="none" stroke="var(--ink)" stroke-width="15"
        stroke-linecap="round"/>

  <!-- especular: o volume do metal, sem sair da paleta -->
  <rect x="99" y="154" width="5" height="92" rx="2.5" fill="var(--surface)" opacity=".38"/>
  <rect x="172" y="208" width="4" height="9" rx="2" fill="var(--surface)" opacity=".34"/>

  <!-- a trajetória e as gotas: o que está saindo agora -->
  <path d="M184 236v62" stroke="var(--accent)" stroke-width="1.5"
        stroke-dasharray="2 9" opacity=".3"/>
  <g fill="var(--accent)">
    <g transform="translate(184 240) scale(.72)">
      <path d="M0 0c-6 9-9 13-9 18a9 9 0 0 0 18 0c0-5-3-9-9-18Z"/>
      <ellipse cx="-3.4" cy="16.5" rx="2.4" ry="3.4" fill="var(--surface)" opacity=".55"/>
    </g>
    <g transform="translate(184 272) scale(.5)" opacity=".5">
      <path d="M0 0c-6 9-9 13-9 18a9 9 0 0 0 18 0c0-5-3-9-9-18Z"/></g>
    <g transform="translate(184 294) scale(.34)" opacity=".26">
      <path d="M0 0c-6 9-9 13-9 18a9 9 0 0 0 18 0c0-5-3-9-9-18Z"/></g>
  </g>
</svg>"""


# --------------------------------------------------------- co-responsabilidade
#
# Proposta que só lista o que o fornecedor entrega esconde metade do combinado.
# Estes são os quatro pontos em que o programa depende do cliente — e é melhor
# que apareçam antes da assinatura do que na terceira semana da fase 1.

COMPROMISSOS = [
    ("Acesso à base", "O histórico de leads e o CRM atual, para migrar tudo sem "
                      "perder ninguém no caminho."),
    ("Agenda do time", "Os captadores disponíveis para o treinamento da fase 1. "
                       "Playbook não se aprende por e-mail."),
    ("Um ponto focal", "Uma pessoa da sua equipe como interlocutor único do "
                       "programa, com autoridade para decidir."),
    ("Presença na reunião", "A reunião semanal de performance só corrige rota se "
                            "quem decide estiver na sala."),
]

VALIDADE = "Esta proposta é válida por 15 dias a partir da data de envio."

# A frase de posicionamento. Ela precisa dizer duas coisas em uma linha: que o
# marketing já foi feito e entregou, e que o que vem agora é a loja escalar em
# cima disso. Sem depreciar o trabalho anterior — é o mesmo cliente que o pagou.
FRASE = "O marketing já trouxe o lead até a sua porta. Agora a sua loja escala."


def compromissos() -> str:
    return "\n".join(
        f'<div class="comp"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in COMPROMISSOS
    )


def perguntas() -> str:
    return "\n".join(
        f'<li><span class="q-n">{i:02d}</span><p>{p}</p></li>'
        for i, p in enumerate(PERGUNTAS, 1)
    )


def regua() -> str:
    return "".join(f"<span>{m}</span>" for m in MESES)


def barras() -> str:
    partes = []
    for i, (nome, duracao, (a, b), *_) in enumerate(FASES, 1):
        partes.append(
            f'<div class="barra n{i}" style="--a:{a};--b:{b}">'
            f'<b>Fase {i}</b><span>{nome}</span>'
            f'<i>{duracao}</i></div>'
        )
    return "\n".join(partes)


def cartoes() -> str:
    partes = []
    for i, (nome, duracao, (_, fim), objetivo, entregas, sinal) in enumerate(FASES, 1):
        itens = "".join(f"<li>{e}</li>" for e in entregas)
        # Uma fase que encosta na coluna aberta da régua não fecha — ela vira regime.
        # O rótulo do sinal muda junto, senão a peça promete um fim que não existe.
        rotulo = ("Sinal de que a fase está saudável" if fim > len(MESES)
                  else "Sinal de que a fase fechou")
        partes.append(
            f'<article class="etapa n{i}">'
            f'<header><span class="etapa-n">Fase {i}</span>'
            f'<span class="etapa-t">{duracao}</span></header>'
            f'<h3>{nome}</h3>'
            f'<p class="etapa-obj">{objetivo}</p>'
            f'<ul class="entregas">{itens}</ul>'
            f'<p class="sinal"><span>{rotulo}</span>{sinal}</p>'
            f'</article>'
        )
    return "\n".join(partes)


def condicoes() -> str:
    return "\n".join(
        f'<div class="cond"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in CONDICOES
    )


CSS_PROPOSTA = """
/* diagnóstico — a torneira segura o argumento, a lista faz o trabalho */
.goteira{display:grid;grid-template-columns:200px 1fr;gap:34px;align-items:start;}
.torneira{width:100%;height:auto;color:var(--accent);display:block;}
.torneira-nota{font-family:'GeistMono',monospace;font-size:10px;letter-spacing:.14em;
  text-transform:uppercase;line-height:1.9;color:var(--muted);margin:16px 0 0;}
.perguntas{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1px;
  background:var(--line);border-top:1px solid var(--line);border-bottom:1px solid var(--line);}
.perguntas li{background:var(--ground);padding:15px 2px 17px;
  display:grid;grid-template-columns:38px 1fr;gap:6px;align-items:baseline;}
.q-n{font-family:'GeistMono',monospace;font-size:10px;letter-spacing:.18em;
  color:var(--accent);}
.perguntas p{margin:0;font-size:17px;line-height:1.45;max-width:56ch;text-wrap:pretty;}

.veredito{border:1px solid var(--accent);border-left-width:4px;background:var(--chip);
  padding:26px 28px 28px;display:flex;flex-direction:column;gap:12px;}
.veredito h3{font-family:'BigShoulders',sans-serif;font-weight:700;
  font-size:clamp(28px,4.4vw,42px);line-height:.98;text-transform:uppercase;
  color:var(--accent);margin:0;text-wrap:balance;}
.veredito p{margin:0;max-width:66ch;}

/* abaixo de 700px a torneira vira faixa horizontal acima das perguntas */
@media (max-width:699px){
  .goteira{grid-template-columns:1fr;gap:20px;}
  .torneira{width:118px;margin:0 auto;}
  .torneira-nota{text-align:center;}
}

/* a frase de posicionamento: entra entre a manchete e a lide */
.frase{font-family:'BigShoulders',sans-serif;font-weight:700;
  font-size:clamp(24px,3.4vw,34px);line-height:1.05;text-transform:uppercase;
  color:var(--accent);margin:0;max-width:24ch;text-wrap:balance;}

/* mensalidade: um número só, do tamanho da decisão */
.mensalidade{display:grid;grid-template-columns:1.15fr 1fr;gap:1px;
  background:var(--line);border:1px solid var(--line);}
.m-corpo{background:var(--accent);color:var(--accent-ink);
  padding:30px 30px 32px;display:flex;flex-direction:column;gap:8px;}
.m-corpo .rot{font-family:'GeistMono',monospace;font-size:10.5px;letter-spacing:.20em;
  text-transform:uppercase;opacity:.8;}
.m-val{font-family:'BigShoulders',sans-serif;font-weight:700;
  font-size:clamp(56px,9vw,86px);line-height:.84;font-variant-numeric:tabular-nums;
  display:flex;align-items:baseline;gap:6px;}
.m-val i{font-style:normal;font-size:.42em;}
.m-val b{font-family:'GeistMono',monospace;font-size:.17em;font-weight:400;
  letter-spacing:.14em;opacity:.85;}
.m-sub{font-family:'OutfitB',sans-serif;font-weight:700;font-size:15px;opacity:.9;}
.m-lado{background:var(--surface);padding:30px 30px 32px;
  display:flex;flex-direction:column;gap:12px;align-items:flex-start;}
.m-de{font-family:'GeistMono',monospace;font-size:10.5px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--muted);}
.m-de s{font-family:'BigShoulders',sans-serif;font-size:26px;letter-spacing:0;
  text-decoration-thickness:2px;text-decoration-color:var(--accent);}
.m-lado .selo{margin-top:0;}
.m-nota{font-size:15px;color:var(--muted);margin-top:auto;max-width:34ch;}
@media (max-width:719px){.mensalidade{grid-template-columns:1fr;}}

/* co-responsabilidade */
.compromissos{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(360px,100%),1fr));
  gap:1px;background:var(--line);border:1px solid var(--line);margin:0;}
.comp{background:var(--surface);padding:20px 24px 22px;
  display:flex;flex-direction:column;gap:6px;}
.comp dt{font-family:'OutfitB',sans-serif;font-weight:700;font-size:15.5px;
  text-transform:uppercase;letter-spacing:.02em;}
.comp dd{margin:0;font-size:15px;color:var(--muted);}

/* oferta — a âncora primeiro, o preço depois */
.precos{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(250px,100%),1fr));
  gap:1px;background:var(--line);border:1px solid var(--line);}
.p{background:var(--surface);padding:26px 26px 28px;display:flex;flex-direction:column;gap:7px;}
.p .rot{font-family:'GeistMono',monospace;font-size:10.5px;letter-spacing:.20em;
  text-transform:uppercase;color:var(--muted);}
.p .val{font-family:'BigShoulders',sans-serif;font-weight:700;font-size:clamp(44px,6vw,60px);
  line-height:.86;font-variant-numeric:tabular-nums;}
.p .nota{font-size:14.5px;color:var(--muted);}
.p.ancora .val{color:var(--muted);text-decoration:line-through;
  text-decoration-thickness:3px;text-decoration-color:var(--accent);}
.p.destaque{background:var(--accent);color:var(--accent-ink);}
.p.destaque .rot,.p.destaque .nota{color:inherit;opacity:.82;}
.selo{display:inline-flex;align-self:flex-start;background:var(--chip);color:var(--accent);
  font-family:'GeistMono',monospace;font-size:10px;letter-spacing:.20em;
  text-transform:uppercase;padding:5px 10px 6px;margin-top:2px;}
.p.destaque .selo{background:var(--accent-ink);color:var(--accent);opacity:1;}

.condicoes{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));
  gap:22px;margin:0;}
.cond{display:flex;flex-direction:column;gap:4px;}
.cond dt{font-family:'GeistMono',monospace;font-size:10px;letter-spacing:.20em;
  text-transform:uppercase;color:var(--accent);}
.cond dd{margin:0;font-size:15px;color:var(--muted);}

/* cronograma — a barra é o dado, não um enfeite */
.crono{border:1px solid var(--line);background:var(--surface);padding:20px 22px 24px;
  display:flex;flex-direction:column;gap:12px;}
.regua{display:grid;grid-template-columns:repeat(var(--cols),1fr);gap:1px;
  font-family:'GeistMono',monospace;font-size:10px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--muted);}
.regua span{padding:0 0 9px 10px;border-left:1px solid var(--line);}
.barras{display:grid;grid-template-columns:repeat(var(--cols),1fr);gap:8px 1px;}
.barra{grid-column:var(--a)/var(--b);padding:13px 15px 15px;
  display:flex;flex-direction:column;gap:2px;border-left:3px solid var(--accent);
  background:var(--chip);min-width:0;}
.barra b{font-family:'GeistMono',monospace;font-size:9.5px;letter-spacing:.20em;
  text-transform:uppercase;color:var(--accent);font-weight:400;}
.barra span{font-family:'OutfitB',sans-serif;font-weight:700;font-size:15px;line-height:1.25;}
.barra i{font-style:normal;font-family:'GeistMono',monospace;font-size:10px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-top:3px;}
.barra.n2{background:color-mix(in srgb,var(--accent) 16%,transparent);}
.barra.n3{background:var(--accent);color:var(--accent-ink);
  border-left-color:var(--accent-ink);}
.barra.n3 b,.barra.n3 i{color:inherit;opacity:.78;}
.crono-nota{font-family:'GeistMono',monospace;font-size:10px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--muted);margin:0;}

/* abaixo de 720px a régua de meses não cabe: as barras viram blocos empilhados */
@media (max-width:719px){
  .regua{display:none;}
  .barras{grid-template-columns:1fr;}
  .barra{grid-column:1/2;}
}

/* fases em detalhe */
.etapas{display:flex;flex-direction:column;gap:1px;background:var(--line);
  border:1px solid var(--line);}
.etapa{background:var(--surface);padding:24px 26px 26px;
  display:flex;flex-direction:column;gap:11px;border-left:4px solid var(--accent);}
.etapa header{display:flex;flex-wrap:wrap;gap:14px;align-items:baseline;
  font-family:'GeistMono',monospace;font-size:10px;letter-spacing:.20em;
  text-transform:uppercase;}
.etapa-n{color:var(--accent);}
.etapa-t{color:var(--muted);}
.etapa h3{font-family:'BigShoulders',sans-serif;font-weight:700;
  font-size:clamp(28px,4vw,38px);line-height:.94;text-transform:uppercase;margin:0;}
.etapa-obj{margin:0;font-size:16.5px;max-width:62ch;}
.entregas{margin:4px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:8px;}
.entregas li{position:relative;padding-left:22px;font-size:15px;color:var(--muted);
  max-width:64ch;}
.entregas li::before{content:"";position:absolute;left:2px;top:9px;width:9px;height:1px;
  background:var(--accent);}
.sinal{margin:8px 0 0;padding-top:14px;border-top:1px solid var(--line);
  font-size:15px;max-width:64ch;display:flex;flex-direction:column;gap:4px;}
.sinal span{font-family:'GeistMono',monospace;font-size:9.5px;letter-spacing:.20em;
  text-transform:uppercase;color:var(--muted);}

"""

PAGINA = """<title>Programa Modo Turbo de Vendas — Turbo 7</title>
<style>
@font-face{{font-family:'BigShoulders';src:url('{big}') format('truetype');font-weight:700;font-display:block;}}
@font-face{{font-family:'Outfit';src:url('{outfit}') format('truetype');font-weight:400;font-display:block;}}
@font-face{{font-family:'OutfitB';src:url('{outfit_b}') format('truetype');font-weight:700;font-display:block;}}
@font-face{{font-family:'GeistMono';src:url('{mono}') format('truetype');font-weight:400;font-display:block;}}
{css}
{css_proposta}
</style>

<div class="wrap">

  <header class="topo">
    <div class="marca">
      <span class="nome">TURBO<em>7</em></span>
      <span class="eyebrow">Marketing de Planejados</span>
    </div>
    <h1>Programa Modo Turbo<br><em>de Vendas</em></h1>
    <p class="frase">{frase}</p>
    <p class="lide">O marketing já faz a sua parte: o lead chega. O que falta é o
      processo que impede esse lead de esfriar — cadência definida, script único, CRM
      que não perde ninguém e um diretor olhando o número toda semana. É isso que o
      programa instala na sua loja, em três fases, ao longo do primeiro trimestre.</p>
  </header>

  <section>
    <h2>{n_perguntas} perguntas antes de qualquer coisa</h2>
    <p class="contexto">{abertura}</p>
    <div class="goteira">
      <div>
        {torneira}
        <p class="torneira-nota">{veredito_nota}</p>
      </div>
      <ol class="perguntas">
{perguntas}
      </ol>
    </div>
    <div class="veredito">
      <h3>{veredito_titulo}</h3>
      <p>{veredito}</p>
    </div>
  </section>

  <section>
    <h2>Onde termina o marketing, onde começa vendas</h2>
    <p class="contexto">{contexto}</p>
    <ol class="funil">
{funil}
    </ol>
  </section>

  <section>
    <h2>O método: a cadência 12 × 30</h2>
    <p class="contexto">A resposta para as três primeiras perguntas deixa de ser
      “depende do captador”. São 12 toques em 30 dias, somando {total} contatos, com
      2 a 3 canais cruzados nos dias de pico — o mesmo desenho para todo lead, todo
      captador, todo dia.</p>
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
    <h2>Acompanhamento de performance</h2>
    <div class="gestao">
      <p class="gestao-lead">{lead}</p>
      <p>{texto}</p>
      <div class="metricas">
{metricas}
      </div>
    </div>
  </section>

  <section>
    <h2>Bônus por performance diária</h2>
    <div class="bonus">
      <span class="bonus-tag">A cereja do bolo</span>
      <div class="bonus-eq">
{bonus}
      </div>
    </div>
  </section>

  <section>
    <h2>Como a implantação acontece</h2>
    <p class="contexto">{contexto_fases}</p>
    <div class="crono" style="--cols:{colunas}">
      <div class="regua">{regua}</div>
      <div class="barras">
{barras}
      </div>
      <p class="crono-nota">A escala começa enquanto a otimização ainda roda — no 3º mês
        as duas fases convivem.</p>
    </div>
    <div class="etapas">
{cartoes}
    </div>
  </section>

  <section>
    <h2>O que precisamos de você</h2>
    <p class="contexto">O programa é implantado dentro da sua operação, não ao lado
      dela. Estes quatro pontos dependem do seu time — e é melhor combiná-los agora
      do que descobri-los na terceira semana.</p>
    <dl class="compromissos">
{compromissos}
    </dl>
  </section>

  <section>
    <h2>Investimento</h2>
    <div class="mensalidade">
      <div class="m-corpo">
        <span class="rot">Investimento mensal</span>
        <span class="m-val"><i>R$</i>{mensal}<b>/mês</b></span>
        <span class="m-sub">{parcelas} parcelas · total de {cliente}</span>
      </div>
      <div class="m-lado">
        <span class="m-de">Valor de mercado <s>{mercado}</s></span>
        <span class="selo">−{desc_cliente}% para cliente Turbo 7</span>
        <span class="m-nota">É menos do que custa manter um captador parado num
          lead que já foi pago.</span>
      </div>
    </div>
    <dl class="condicoes">
{condicoes}
    </dl>
    <p class="ressalva">{validade}</p>
  </section>

  <section>
    <h2>Próximo passo</h2>
    <p class="lide" style="font-size:16px">A fase 1 começa na semana seguinte ao aceite:
      implantação do CRM e treinamento do time comercial. As oito perguntas do começo
      passam a ter resposta em número já no primeiro relatório semanal.</p>
    <a class="cta" href="https://www.turbo7.com.br" target="_blank" rel="noopener">
      Quero começar <span>WWW.TURBO7.COM.BR</span></a>
    <a class="atalho" href="./">Ver a apresentação do programa
      <span>Funil, cadência e flyer</span></a>
  </section>

  <footer>
    <span>Turbo 7 · Programa Modo Turbo</span>
    <a href="https://www.turbo7.com.br" target="_blank" rel="noopener">turbo7.com.br</a>
  </footer>

</div>
"""


def montar() -> str:
    """O fragmento da página, sem <html>/<head> — igual à apresentação."""
    return PAGINA.format(
        css=CSS_BASE,
        css_proposta=CSS_PROPOSTA,
        big=fonte("BigShoulders-Bold.ttf"),
        outfit=fonte("Outfit-Regular.ttf"),
        outfit_b=fonte("Outfit-Bold.ttf"),
        mono=fonte("GeistMono-Regular.ttf"),
        total=TOTAL_CONTATOS,
        contexto=CONTEXTO,
        funil=funil(),
        toques=toques(),
        compromissos=compromissos(),
        validade=VALIDADE,
        n_perguntas=len(PERGUNTAS),
        abertura=ABERTURA.format(n=len(PERGUNTAS)),
        torneira=TORNEIRA,
        perguntas=perguntas(),
        veredito_titulo=VEREDITO_TITULO,
        veredito=VEREDITO,
        veredito_nota=VEREDITO_NOTA,
        mercado=moeda(MERCADO),
        cliente=moeda(CLIENTE),
        avista=moeda(AVISTA),
        parcelas=PARCELAS,
        parcela=moeda(CLIENTE / PARCELAS, centavos=True),
        mensal=f"{MENSAL:,.2f}".replace(",", "·").replace(".", ",").replace("·", "."),
        frase=FRASE,
        economia=moeda(ECONOMIA_AVISTA),
        desc_cliente=DESCONTO_CLIENTE,
        desc_avista=DESCONTO_AVISTA,
        condicoes=condicoes(),
        contexto_fases=CONTEXTO_FASES,
        colunas=len(MESES),
        regua=regua(),
        barras=barras(),
        cartoes=cartoes(),
        escopo=escopo(),
        lead=GESTAO_LEAD,
        texto=GESTAO_TEXTO,
        metricas=metricas(),
        bonus=bonus(),
    )


if __name__ == "__main__":
    destino = RAIZ / "proposta.html"
    destino.write_text(montar(), encoding="utf-8")
    print(f"{destino.name}  ({destino.stat().st_size // 1024} KB)")
