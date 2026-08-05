#!/usr/bin/env python3
"""Monta a variação de venda da página: a proposta comercial do Modo Turbo.

A apresentação explica o programa; esta página o vende. Muda o eixo — abre pela
oferta e pelo cronograma das três fases — mas reaproveita o mesmo sistema visual
e os mesmos dados de escopo, cadência, gestão e bônus, para que as duas peças
não possam divergir.
"""

from pathlib import Path

from build import GESTAO_LEAD, GESTAO_TEXTO, TOTAL_CONTATOS
from build_pagina import CSS_BASE, bonus, escopo, fonte, metricas

RAIZ = Path(__file__).parent

# ---------------------------------------------------------------- oferta

MERCADO = 50_000       # valor de mercado do programa, a âncora
CLIENTE = 25_000       # preço para quem já é cliente
AVISTA = 20_000        # preço à vista
PARCELAS = 6

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
    ("Parcelamento", f"Até {PARCELAS}× de {moeda(CLIENTE / PARCELAS, centavos=True)}, "
                     "sem entrada."),
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

# Glifo próprio, no mesmo traço dos ícones de canal do flyer: a gota é o dado, o
# pontilhado é a trajetória e a poça é o acumulado. currentColor deixa a peça
# seguir o tema claro/escuro sem uma segunda versão do desenho.
TORNEIRA = """<svg class="torneira" viewBox="0 0 200 300" fill="none" role="img"
     aria-label="Uma torneira pingando sobre uma poça: cada gota é uma venda que escapa.">
  <g stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
    <path d="M100 236V140"/>
    <path d="M100 140c0-40 52-40 52 0v28"/>
    <path d="M92 152h16"/>
    <path d="M100 158 58 146"/>
    <path d="M88 250v-14h24v14"/>
    <path d="M143 168h18l-4 12h-10z"/>
  </g>
  <circle cx="53" cy="145" r="7" stroke="currentColor" stroke-width="4"/>
  <path d="M40 250h86" stroke="currentColor" stroke-width="2" opacity=".38"/>
  <path d="M152 190v92" stroke="currentColor" stroke-width="1.5"
        stroke-dasharray="2 9" opacity=".28"/>
  <g fill="currentColor">
    <g transform="translate(152 192) scale(.66)">
      <path d="M0 0c-6 9-9 13-9 18a9 9 0 0 0 18 0c0-5-3-9-9-18Z"/></g>
    <g transform="translate(152 228) scale(.52)" opacity=".55">
      <path d="M0 0c-6 9-9 13-9 18a9 9 0 0 0 18 0c0-5-3-9-9-18Z"/></g>
    <g transform="translate(152 258) scale(.4)" opacity=".3">
      <path d="M0 0c-6 9-9 13-9 18a9 9 0 0 0 18 0c0-5-3-9-9-18Z"/></g>
  </g>
  <ellipse cx="152" cy="288" rx="30" ry="4.5" fill="currentColor" opacity=".18"/>
</svg>"""


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

PAGINA = """<title>Proposta — Programa Modo Turbo | Turbo 7</title>
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
    <h1>Modo Turbo<br><em>Proposta comercial</em></h1>
    <p class="lide">A máquina de vendas montada dentro da sua operação: CRM implantado,
      playbook treinado, cadência de {total} contatos em 30 dias e um diretor conduzindo
      a performance do time. Implantação em três fases, ao longo do primeiro trimestre.</p>
  </header>

  <section>
    <h2>{n_perguntas} perguntas antes de falar em preço</h2>
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
    <h2>Investimento</h2>
    <div class="precos">
      <div class="p ancora">
        <span class="rot">Valor de mercado</span>
        <span class="val">{mercado}</span>
        <span class="nota">O que uma implantação equivalente custa fora daqui.</span>
      </div>
      <div class="p">
        <span class="rot">Para quem já é cliente</span>
        <span class="val">{cliente}</span>
        <span class="nota">Em até {parcelas}× de {parcela}.</span>
        <span class="selo">−{desc_cliente}%</span>
      </div>
      <div class="p destaque">
        <span class="rot">À vista</span>
        <span class="val">{avista}</span>
        <span class="nota">{economia} a menos que o parcelado.</span>
        <span class="selo">−{desc_avista}%</span>
      </div>
    </div>
    <dl class="condicoes">
{condicoes}
    </dl>
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
    <h2>Próximo passo</h2>
    <p class="lide" style="font-size:16px">A fase 1 começa na semana seguinte ao aceite:
      implantação do CRM e treinamento do time comercial.</p>
    <a class="cta" href="https://www.turbo7.com.br" target="_blank" rel="noopener">
      Quero começar <span>WWW.TURBO7.COM.BR</span></a>
    <a class="atalho" href="./">Ver a apresentação completa do programa
      <span>Funil, cadência e flyer</span></a>
  </section>

  <footer>
    <span>Turbo 7 · Programa Modo Turbo · Proposta comercial</span>
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
