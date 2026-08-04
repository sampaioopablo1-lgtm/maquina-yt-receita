#!/usr/bin/env python3
"""Monta o site público (pasta `site/`) a partir da mesma página do Artifact.

O Artifact recebe um fragmento e embrulha o documento por conta própria; um host
comum não faz isso, então aqui o fragmento entra num HTML completo, com as metas
de compartilhamento que fazem o link render um preview decente no WhatsApp.
"""

import shutil
from pathlib import Path

from build_pagina import montar

RAIZ = Path(__file__).parent
SITE = RAIZ / "site"

# Preenchido depois do primeiro deploy: crawlers de link exigem URL absoluta.
BASE_URL = "https://modo-turbo-turbo7.netlify.app"

TITULO = "Programa Modo Turbo 30 Dias — Turbo 7"
DESCRICAO = (
    "Cadência comercial de 12 toques em 30 dias, playbook de vendas, CRM "
    "implantado e reuniões semanais de performance. Os primeiros 30 dias são "
    "gratuitos para novos clientes."
)
FLYER = "flyer-modo-turbo-30-dias.png"
PDF = "flyer-modo-turbo-30-dias.pdf"

DOCUMENTO = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{descricao}">
<meta name="theme-color" content="#120320">
<link rel="canonical" href="{base}/">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23120320'/%3E%3Cpath d='M16 4c3.8 4.2 5.8 9.1 5.8 14.4v5.3H10.2v-5.3C10.2 13.1 12.2 8.2 16 4Z' fill='none' stroke='%237CF01E' stroke-width='2'/%3E%3Ccircle cx='16' cy='13.3' r='2.6' fill='none' stroke='%23fff' stroke-width='2'/%3E%3C/svg%3E">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Turbo 7">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:url" content="{base}/">
<meta property="og:image" content="{base}/{flyer}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titulo}">
<meta name="twitter:description" content="{descricao}">
<meta name="twitter:image" content="{base}/{flyer}">
</head>
<body>
{corpo}

<div class="wrap" style="padding-top:0">
  <section>
    <h2>Baixar a peça</h2>
    <div class="baixar">
      <a class="arq" href="{flyer}" download>
        <span class="arq-k">PNG · 2400 × 4320 px</span>
        <span class="arq-v">Flyer para WhatsApp e redes</span>
      </a>
      <a class="arq" href="{pdf}" download>
        <span class="arq-k">PDF · 1 página</span>
        <span class="arq-v">Versão para impressão</span>
      </a>
    </div>
  </section>
</div>

<style>
.baixar{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));gap:1px;
  background:var(--line);border:1px solid var(--line);}}
.arq{{background:var(--surface);padding:20px 24px 22px;text-decoration:none;color:inherit;
  display:flex;flex-direction:column;gap:5px;transition:background .16s ease;}}
.arq:hover{{background:var(--ground);}}
.arq:focus-visible{{outline:3px solid var(--accent);outline-offset:-3px;}}
.arq-k{{font-family:'GeistMono',monospace;font-size:10px;letter-spacing:.20em;
  text-transform:uppercase;color:var(--accent);}}
.arq-v{{font-family:'OutfitB',sans-serif;font-weight:700;font-size:16px;}}
@media (prefers-reduced-motion:reduce){{.arq{{transition:none;}}}}
</style>
</body>
</html>
"""


def construir() -> Path:
    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text(
        DOCUMENTO.format(
            corpo=montar(), titulo=TITULO, descricao=DESCRICAO,
            base=BASE_URL, flyer=FLYER, pdf=PDF,
        ),
        encoding="utf-8",
    )
    shutil.copy(RAIZ / "flyer-turbo7-modo-turbo-30-dias.png", SITE / FLYER)
    shutil.copy(RAIZ / "flyer-turbo7-modo-turbo-30-dias.pdf", SITE / PDF)
    (SITE / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    return SITE


if __name__ == "__main__":
    pasta = construir()
    for arquivo in sorted(pasta.iterdir()):
        print(f"{arquivo.name}  ({arquivo.stat().st_size // 1024} KB)")
