#!/usr/bin/env python3
"""Gera o PDF da proposta em A4 — como documento, não como página impressa.

O conteúdo vem de `build_publico.construir()`: nada é redigitado, e mudar a
proposta muda o PDF. O que este arquivo acrescenta é o que um documento comercial
tem e uma página web não: capa, sumário, folhas de página inteira nos dois
momentos em que a peça precisa de peso — o veredito da goteira e o investimento —
e um fecho. Entre elas, as páginas claras de leitura.

Por que montar em partes e juntar depois: uma folha que sangra até a borda exige
página sem margem, e o miolo exige margem. As duas coisas no mesmo documento não
convivem — com margem negativa o fundo escorre para o rodapé da página anterior;
com `@page` nomeada o Chromium reduz a escala do documento inteiro para "caber" e
sobra moldura branca em tudo. Cada peça vira um PDF com a geometria de que
precisa, e a ordem é remontada no fim. Sai determinístico e sem página sobrando.
"""

import re
import subprocess
import sys
from pathlib import Path

import pypdfium2 as pdfium

import build_proposta
import build_publico

RAIZ = Path(__file__).parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
TEMP = RAIZ / "_pdf"

# Sumário: o mapa do documento. A numeração sai da lista, e os títulos espelham
# as seções — se a proposta ganhar uma seção, esta lista é o único lugar a tocar.
ROTEIRO = [
    ("O diagnóstico", "Oito perguntas que localizam a goteira"),
    ("O funil", "Onde termina o marketing, onde começa vendas"),
    ("O método", "A cadência 12 × 30, igual para todo lead"),
    ("O escopo", "CRM, playbook e gestão de performance"),
    ("O incentivo", "O bônus que a meta diária destrava"),
    ("A implantação", "Três fases ao longo do primeiro trimestre"),
    ("O combinado", "O que o programa depende de você"),
    ("O investimento", "Mensalidade, condições e validade"),
]

MARCA = ('<div class="marca-doc"><span class="nome">TURBO<em>7</em></span>'
         '<span class="eyebrow">Marketing de Planejados</span></div>')

COMUM = """
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  a{text-decoration:none;color:inherit;}
  .marca-doc{display:flex;align-items:baseline;gap:12px;}
  .marca-doc .nome{font-family:'BigShoulders',sans-serif;font-weight:700;
    font-size:26pt;line-height:.8;}
  .marca-doc .nome em{font-style:normal;color:var(--accent);}
  .marca-doc .eyebrow{font-family:'GeistMono',monospace;font-size:7.5pt;
    letter-spacing:.24em;text-transform:uppercase;color:var(--muted);}
"""

# A folha ocupa a página inteira porque a página não tem margem: o respiro é
# padding e o fundo é do próprio elemento. Sem fluxo paginado, sem surpresa.
CSS_FOLHA = """
<style>
@page{size:A4;margin:0;}
@media print{
""" + COMUM + """
  html,body{margin:0;background:#fff;}
  .folha{width:210mm;height:297mm;padding:20mm;box-sizing:border-box;
    position:relative;display:flex;flex-direction:column;overflow:hidden;
    break-after:page;}
  .folha:last-child{break-after:auto;}
  .folha.escura{background:#120320;color:#F2ECF8;
    --ink:#F2ECF8;--muted:#B3A2C6;--line:rgba(255,255,255,.16);--accent:#7CF01E;
    --surface:#1C0733;--chip:rgba(124,240,30,.11);--accent-ink:#0E0318;}
  .folha.clara{background:#F4F2F7;color:#1B0A2E;
    --ink:#1B0A2E;--muted:#6B5B7D;--line:rgba(27,10,46,.16);--accent:#4E0FA3;}

  /* Marcas de registro: dois cantos bastam para assinar a página. */
  .folha.escura::before,.folha.escura::after{content:"";position:absolute;
    width:13mm;height:13mm;border:.35mm solid rgba(124,240,30,.6);}
  .folha.escura::before{top:11mm;left:11mm;border-right:0;border-bottom:0;}
  .folha.escura::after{bottom:11mm;right:11mm;border-left:0;border-top:0;}

  /* A folha tem altura fixa: sem isto, um conteúdo alto faz o flex encolher os
     irmãos, e os blocos baixos — a marca, o título — são espremidos a zero e
     desaparecem sob o `overflow:hidden`. Levei um susto com isso. */
  .folha > *{flex:none;}
  .pe{margin-top:auto;}

  /* capa */
  .capa-corpo{margin-top:auto;display:flex;flex-direction:column;gap:13mm;}
  .capa-tag{font-family:'GeistMono',monospace;font-size:8pt;letter-spacing:.30em;
    text-transform:uppercase;color:#7CF01E;align-self:flex-start;
    border:.35mm solid rgba(124,240,30,.55);padding:3.6mm 6mm 3mm;}
  .capa-h{font-family:'BigShoulders',sans-serif;font-weight:700;font-size:60pt;
    line-height:.86;text-transform:uppercase;margin:0;color:#fff;}
  .capa-h em{font-style:normal;color:#7CF01E;}
  .capa-frase{font-family:'BigShoulders',sans-serif;font-weight:700;font-size:19pt;
    line-height:1.06;text-transform:uppercase;color:#7CF01E;margin:0;max-width:26ch;}
  .capa-pe{margin:13mm 0 0;padding-top:5mm;border-top:.3mm solid rgba(255,255,255,.25);
    display:grid;grid-template-columns:1.1fr 1.4fr .7fr;gap:6mm;}
  .capa-pe dt{font-family:'GeistMono',monospace;font-size:7pt;letter-spacing:.22em;
    text-transform:uppercase;color:#B3A2C6;margin-bottom:2.5mm;}
  .capa-pe dd{margin:0;font-size:10pt;border-bottom:.3mm solid rgba(255,255,255,.3);
    padding-bottom:2mm;}

  /* sumário */
  .folha-h{font-family:'BigShoulders',sans-serif;font-weight:700;font-size:28pt;
    line-height:.96;text-transform:uppercase;margin:13mm 0 0;color:#fff;}
  .sumario{list-style:none;margin:9mm 0 0;padding:0;}
  .sumario li{display:grid;grid-template-columns:14mm 58mm 1fr;gap:5mm;
    align-items:baseline;padding:3.9mm 0;border-top:.3mm solid rgba(255,255,255,.16);}
  .sumario li:last-child{border-bottom:.3mm solid rgba(255,255,255,.16);}
  .s-n{font-family:'GeistMono',monospace;font-size:8pt;letter-spacing:.2em;
    color:#7CF01E;}
  .s-t{font-family:'OutfitB',sans-serif;font-weight:700;font-size:12pt;
    text-transform:uppercase;letter-spacing:.02em;color:#F2ECF8;}
  .s-d{font-size:10.5pt;color:#B3A2C6;}
  .folha-pe{font-family:'GeistMono',monospace;font-size:7.5pt;letter-spacing:.18em;
    text-transform:uppercase;color:#B3A2C6;margin:0;}

  /* veredito */
  .veredito{border:0;background:transparent;padding:0;margin:auto 0 0;
    display:flex;flex-direction:column;gap:8mm;}
  .veredito h3{font-family:'BigShoulders',sans-serif;font-weight:700;
    font-size:34pt;line-height:.96;text-transform:uppercase;color:#7CF01E;margin:0;}
  .veredito p{font-size:12.5pt;line-height:1.6;max-width:58ch;color:#F2ECF8;margin:0;}
  .veredito-nota{margin:10mm 0 0;font-family:'GeistMono',monospace;font-size:8pt;
    letter-spacing:.2em;text-transform:uppercase;color:#B3A2C6;
    padding-top:5mm;border-top:.3mm solid rgba(255,255,255,.25);}

  /* investimento */
  .h-invest{font-family:'GeistMono',monospace;font-size:8pt;letter-spacing:.3em;
    text-transform:uppercase;color:#7CF01E;margin:14mm 0 5mm;}
  .mensalidade{grid-template-columns:1fr;border:.3mm solid rgba(255,255,255,.2);}
  .m-corpo{background:#7CF01E;color:#0E0318;}
  .m-lado{background:#1C0733;flex-direction:row;flex-wrap:wrap;
    align-items:center;gap:5mm 9mm;}
  .m-val{font-size:40pt;}
  .m-nota{margin:0;max-width:46ch;}
  .selo{background:rgba(124,240,30,.14);color:#7CF01E;}
  .m-de s{text-decoration-color:#7CF01E;}
  .condicoes{margin-top:7mm;}
  .cond dt{color:#7CF01E;}
  .cond dd{color:#B3A2C6;}
  .ressalva{margin:auto 0 0;border-left:.8mm solid #7CF01E;color:#B3A2C6;}

  /* fecho */
  .fecho-h{font-family:'BigShoulders',sans-serif;font-weight:700;font-size:44pt;
    line-height:.9;text-transform:uppercase;margin:0;color:#fff;}
  .fecho-h em{font-style:normal;color:#7CF01E;}
  .fecho-lide{margin:0;font-size:12pt;line-height:1.55;max-width:52ch;color:#B3A2C6;}
  .fecho-pe{margin-top:13mm;padding-top:5mm;
    border-top:.3mm solid rgba(255,255,255,.25);
    display:flex;justify-content:space-between;align-items:baseline;}
  .fecho-pe .nome{font-family:'BigShoulders',sans-serif;font-weight:700;
    font-size:22pt;color:#fff;}
  .fecho-pe .nome em{font-style:normal;color:#7CF01E;}
  .fecho-url{font-family:'GeistMono',monospace;font-size:8pt;letter-spacing:.24em;
    text-transform:uppercase;color:#7CF01E;}
}
</style>
"""

CSS_MIOLO = """
<style>
@page{size:A4;margin:16mm 15mm 16mm;}
@media print{
""" + COMUM + """
  body{background:#fff;font-size:10.5pt;}
  .wrap{max-width:100%;padding:0;gap:22px;}

  /* Os blocos não partem no meio — mas a seção pode. Proibir a quebra da seção
     inteira é o que enche o PDF de página pela metade: basta um bloco não caber
     no rodapé para a seção inteira pular adiante. */
  .etapa,.fase,.troca,.comp,.escopo-item,.met,.toque,.contexto,.crono,.gestao,
  .bonus,.cond,.toques,.escopo,.compromissos{break-inside:avoid;}
  h1,h2,h3{break-after:avoid;}
  h2{padding-bottom:8px;}

  .lide{font-size:11.5pt;}
  .perguntas p{font-size:11pt;}
  .etapa h3{font-size:18pt;}
  .gestao-lead{font-size:20pt;}
  .toque-dia{font-size:16pt;}
  .alvo b,.premio b{font-size:26pt;}
  .goteira{grid-template-columns:132px 1fr;gap:22px;}
}
</style>
"""


def _base() -> str:
    doc = build_publico.construir()
    return doc.replace('<html lang="pt-BR">', '<html lang="pt-BR" data-theme="light">')


def _documento(base: str, css: str, corpo: str) -> str:
    """Troca o corpo do documento preservando a folha de estilo.

    `build_publico` emite o `<style>` dentro do `<body>` — é assim que o Artifact
    espera o fragmento. Trocar o corpo inteiro levaria o sistema visual junto, e
    as páginas sairiam sem estilo nenhum.
    """
    estilo = re.search(r"<style>.*?</style>", base, re.S).group(0)
    # A folha da peça entra DEPOIS da base: mesma especificidade, ganha quem vem
    # por último. É o que deixa a folha escura desmontar a moldura que o bloco
    # tem na tela sem precisar de `!important` em cada regra.
    return re.sub(r"<body>.*</body>", f"<body>{estilo}{css}{corpo}</body>",
                  base, flags=re.S)


def _capa() -> str:
    return (f'<div class="folha escura">{MARCA}'
            f'<div class="capa-corpo">'
            f'<span class="capa-tag">Proposta comercial</span>'
            f'<h1 class="capa-h">Programa<br>Modo Turbo<br><em>de Vendas</em></h1>'
            f'<p class="capa-frase">{build_proposta.FRASE}</p></div>'
            f'<dl class="capa-pe">'
            f'<div><dt>Preparado para</dt><dd>&nbsp;</dd></div>'
            f'<div><dt>Emitido por</dt><dd>Turbo 7 · Marketing de Planejados</dd></div>'
            f'<div><dt>Validade</dt><dd>15 dias</dd></div></dl></div>')


def _sumario() -> str:
    linhas = "".join(
        f'<li><span class="s-n">{i:02d}</span><span class="s-t">{t}</span>'
        f'<span class="s-d">{d}</span></li>'
        for i, (t, d) in enumerate(ROTEIRO, 1))
    return (f'<div class="folha escura">{MARCA}'
            f'<h2 class="folha-h">O que você vai encontrar</h2>'
            f'<ol class="sumario">{linhas}</ol>'
            f'<p class="folha-pe pe">{build_proposta.VALIDADE}</p></div>')


def _fecho() -> str:
    return ('<div class="folha escura"><div class="capa-corpo">'
            '<span class="capa-tag">Próximo passo</span>'
            '<h1 class="fecho-h">A fase 1 começa na<br>semana seguinte'
            '<br><em>ao aceite.</em></h1>'
            '<p class="fecho-lide">Implantação do CRM e treinamento do time '
            'comercial. As oito perguntas do começo passam a ter resposta em '
            'número já no primeiro relatório semanal.</p>'
            '<div class="fecho-pe"><span class="nome">TURBO<em>7</em></span>'
            '<span class="fecho-url">turbo7.com.br</span></div></div></div>')


def _pecas() -> list[tuple[str, str]]:
    """(nome, html) na ordem final do documento."""
    base = _base()
    corpo = re.search(r'<div class="wrap">(.*)</div>\s*</body>', base, re.S).group(1)
    secoes = re.findall(r"<section>.*?</section>", corpo, re.S)
    perguntas, resto, investimento = secoes[0], secoes[1:8], secoes[8]

    veredito = re.search(r'<div class="veredito">.*?</div>\s*(?=</section>)',
                         perguntas, re.S).group(0)
    nota = re.search(r'<p class="torneira-nota">(.*?)</p>', perguntas, re.S).group(1)
    perguntas = perguntas.replace(veredito, "")
    invest = (investimento.replace("<section>", "").replace("</section>", "")
              .replace("<h2>Investimento</h2>",
                       '<h2 class="h-invest">Investimento</h2>'))

    def miolo(html: str) -> str:
        return _documento(base, CSS_MIOLO, f'<div class="wrap">{html}</div>')

    def folha(html: str) -> str:
        return _documento(base, CSS_FOLHA, html)

    # Todas as folhas num único documento, e não uma por arquivo: renderizadas
    # isoladamente, algumas corridas do Chromium terminam antes de a fonte
    # embutida ficar pronta e o texto em Big Shoulders simplesmente não é
    # pintado — a caixa fica lá, vazia. Juntas, carregam uma vez só.
    folhas = folha(
        _capa()
        + _sumario()
        + f'<div class="folha escura">{MARCA}{veredito}'
          f'<p class="veredito-nota">{nota}</p></div>'
        + f'<div class="folha escura">{MARCA}{invest}</div>'
        + _fecho())
    return [("folhas", folhas), ("perguntas", miolo(perguntas)),
            ("miolo", miolo("".join(resto)))]


def _imprimir(nome: str, html: str) -> Path:
    fonte = TEMP / f"{nome}.html"
    fonte.write_text(html, encoding="utf-8")
    destino = TEMP / f"{nome}.pdf"
    r = subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--allow-file-access-from-files", "--hide-scrollbars",
        "--virtual-time-budget=12000", "--font-render-hinting=none",
        "--no-pdf-header-footer", f"--print-to-pdf={destino}", str(fonte),
    ], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"chromium falhou em {nome}:\n{r.stderr[-1500:]}")
    return destino


# A ordem final: cada item é (peça, páginas). `None` significa "todas".
MONTAGEM = [("folhas", [0, 1]), ("perguntas", None), ("folhas", [2]),
            ("miolo", None), ("folhas", [3, 4])]


def construir() -> Path:
    TEMP.mkdir(exist_ok=True)
    pecas = {nome: _imprimir(nome, html) for nome, html in _pecas()}

    final = pdfium.PdfDocument.new()
    abertos = []
    for nome, paginas in MONTAGEM:
        doc = pdfium.PdfDocument(pecas[nome])
        abertos.append(doc)
        final.import_pages(doc, pages=paginas)
    destino = RAIZ / "proposta-modo-turbo-de-vendas.pdf"
    final.save(destino)
    for doc in abertos:
        doc.close()
    for arquivo in TEMP.iterdir():
        arquivo.unlink()
    TEMP.rmdir()
    return destino


if __name__ == "__main__":
    caminho = construir()
    with pdfium.PdfDocument(caminho) as doc:
        paginas = len(doc)
    print(f"{caminho.name}  ({caminho.stat().st_size // 1024} KB, {paginas} páginas)")
