#!/usr/bin/env python3
"""Gera o PDF da proposta, em A4, a partir da mesma página.

Nada é remontado aqui: o conteúdo vem de `build_publico.construir()`, e este
arquivo só acrescenta a folha de impressão. Papel não tem tema escuro, não tem
hover e não tem rolagem — tem quebra de página, que é o problema real. As regras
abaixo tratam disso: nenhum bloco parte no meio, nenhum título fica órfão no pé
da página, e os fundos chapados são impressos em vez de virarem branco.
"""

import re
import subprocess
import sys
from pathlib import Path

import build_publico

RAIZ = Path(__file__).parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

IMPRESSAO = """
<style>
@page{size:A4;margin:14mm 15mm 16mm;}
@media print{
  /* O fundo chapado do preço e do bônus é argumento, não decoração: precisa sair
     impresso. Sem isto o navegador os descarta para poupar tinta. */
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  body{background:#fff;font-size:10.5pt;}
  .wrap{max-width:100%;padding:0;gap:22px;}

  /* Os blocos não partem no meio — mas a seção pode. Proibir a quebra da seção
     inteira é o que enche o PDF de página pela metade: basta um bloco não caber
     no rodapé para a seção inteira pular adiante. */
  .etapa,.fase,.troca,.comp,.escopo-item,.met,.toque,.veredito,.contexto,
  .mensalidade,.crono,.gestao,.bonus,.goteira,.cond,.toques,.escopo,
  .compromissos{break-inside:avoid;}
  h1,h2,h3,.frase{break-after:avoid;}
  footer{break-before:avoid;}
  h2{padding-bottom:8px;}

  h1{font-size:40pt;}
  .frase{font-size:17pt;}
  .lide{font-size:11.5pt;}
  .perguntas p{font-size:11pt;}
  .etapa h3{font-size:18pt;}
  .gestao-lead,.veredito h3{font-size:20pt;}
  .m-val{font-size:38pt;}
  .toque-dia{font-size:16pt;}
  .alvo b,.premio b{font-size:26pt;}
  .cta{font-size:15pt;padding:11px 18px;}

  /* Encolhe a torneira: em tela ela divide a largura com a lista, no papel a
     lista precisa do espaço. */
  .goteira{grid-template-columns:132px 1fr;gap:22px;}

  a{text-decoration:none;color:inherit;}
  .cta:hover{transform:none;}
}
</style>
</head>"""


def construir() -> str:
    doc = build_publico.construir()
    # Papel é sempre claro: fixa o tema para não depender do sistema de quem imprime.
    doc = doc.replace('<html lang="pt-BR">', '<html lang="pt-BR" data-theme="light">')
    return doc.replace("</head>", IMPRESSAO, 1)


if __name__ == "__main__":
    fonte = RAIZ / "_proposta-impressao.html"
    fonte.write_text(construir(), encoding="utf-8")
    destino = RAIZ / "proposta-modo-turbo-de-vendas.pdf"
    r = subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--allow-file-access-from-files", "--hide-scrollbars",
        "--virtual-time-budget=12000", "--font-render-hinting=none",
        "--no-pdf-header-footer", f"--print-to-pdf={destino}", str(fonte),
    ], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"chromium falhou:\n{r.stderr[-2000:]}")
    fonte.unlink()
    print(f"{destino.name}  ({destino.stat().st_size // 1024} KB)")
