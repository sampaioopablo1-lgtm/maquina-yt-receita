#!/usr/bin/env python3
"""Gera a versão da proposta que vai para o host público.

O conteúdo é o mesmo de `proposta.html` — mesma função `montar()`, então não há
como as duas divergirem. Muda só o empacotamento das fontes: em vez das quatro
TTF inteiras em data URI (368 KB), aqui elas são reduzidas aos 127 caracteres que
a página de fato usa e convertidas para WOFF2, o que as leva a ~46 KB.

Isso importa por um motivo prático: a página é servida de dentro de uma Edge
Function do Supabase, e o HTML precisa caber no código da função. Com o subset,
a página inteira fica em ~100 KB e continua sem nenhuma requisição externa — as
fontes seguem embutidas, então o desenho não depende de CDN nenhum.
"""

import base64
import io
import re
from pathlib import Path

from fontTools import subset

import build_proposta

RAIZ = Path(__file__).parent

TITULO = "Programa Modo Turbo de Vendas — Turbo 7"
DESCRICAO = ("Oito perguntas que revelam onde a sua operação comercial está vazando, "
             "o método que fecha cada goteira e a implantação em três fases. "
             "Para lojas que já fazem marketing e querem escalar a venda.")

# Além do texto da página, garante o alfabeto inteiro: o conteúdo muda, o subset
# não pode quebrar por causa de uma letra que ninguém usou nesta versão.
EXTRA = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
         "áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ.,;:!?()[]{}<>/\\-–—+×·%$&@#*\"'“”‘’ ")

DOCUMENTO = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descricao}">
<meta name="theme-color" content="#120320">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23120320'/%3E%3Cpath d='M16 4c3.8 4.2 5.8 9.1 5.8 14.4v5.3H10.2v-5.3C10.2 13.1 12.2 8.2 16 4Z' fill='none' stroke='%237CF01E' stroke-width='2'/%3E%3Ccircle cx='16' cy='13.3' r='2.6' fill='none' stroke='%23fff' stroke-width='2'/%3E%3C/svg%3E">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Turbo 7">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{titulo}">
<meta name="twitter:description" content="{descricao}">
</head>
<body>
{corpo}
</body>
</html>
"""


def _glifos() -> str:
    bruto = re.sub(r"<[^>]+>", " ", build_proposta.montar())
    return "".join(sorted({c for c in set(bruto) | set(EXTRA) if c.isprintable()}))


def woff2(nome: str, texto: str) -> str:
    buf = io.BytesIO()
    opts = subset.Options(flavor="woff2", layout_features=["*"], desubroutinize=True)
    fonte = subset.load_font(RAIZ / "fonts" / nome, opts)
    sub = subset.Subsetter(options=opts)
    sub.populate(text=texto)
    sub.subset(fonte)
    subset.save_font(fonte, buf, opts)
    return "data:font/woff2;base64," + base64.b64encode(buf.getvalue()).decode()


def _enxuga(corpo: str) -> str:
    """Colapsa a folha de estilo. O HTML servido não é lugar de indentação: o
    fonte legível é o `build_*.py`, e cada quilobyte aqui é quilobyte que a
    função precisa carregar."""
    def compacta(m):
        css = re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S)
        css = re.sub(r"\s*\n\s*", "", css)
        return "<style>" + css + "</style>"
    return re.sub(r"<style>(.*?)</style>", compacta, corpo, flags=re.S)


def construir() -> str:
    texto = _glifos()
    original = build_proposta.fonte
    build_proposta.fonte = lambda nome: woff2(nome, texto)
    try:
        corpo = build_proposta.montar()
    finally:
        build_proposta.fonte = original

    corpo = corpo.replace("format('truetype')", "format('woff2')")
    corpo = _enxuga(corpo)
    corpo = re.sub(r"^<title>.*?</title>\n", "", corpo)
    # o atalho aponta para a apresentação, que não é publicada neste host
    corpo = re.sub(r'\s*<a class="atalho" href="\./">.*?</a>', "", corpo, flags=re.S)
    return DOCUMENTO.format(corpo=corpo, titulo=TITULO, descricao=DESCRICAO)


ROTA_FONTES = "modo-turbo-fontes"   # nome da Edge Function que serve a folha


def separar() -> tuple[str, str]:
    """Divide a página em (HTML, CSS das fontes).

    No Supabase cada peça vira uma Edge Function, e o código de uma função é
    enviado como texto: 100 KB num arquivo só é grande demais para caber com
    folga numa chamada. Separadas, a folha de fontes é servida da mesma origem
    (`/functions/v1/<rota>`), então nada sai para fora — só deixa de estar no
    mesmo arquivo.
    """
    pagina = construir()
    faces = re.findall(r"@font-face\{[^}]*\}", pagina)
    css = "".join(faces)
    pagina = pagina.replace(css, "")
    pagina = pagina.replace(
        "</head>",
        f'<link rel="stylesheet" href="{ROTA_FONTES}">\n</head>')
    return pagina, css


if __name__ == "__main__":
    destino = RAIZ / "publico.html"
    destino.write_text(construir(), encoding="utf-8")
    print(f"{destino.name}  ({destino.stat().st_size // 1024} KB)")

    pasta = RAIZ / "publico"
    pasta.mkdir(exist_ok=True)
    html, css = separar()
    (pasta / "index.html").write_text(html, encoding="utf-8")
    (pasta / "fontes.css").write_text(css, encoding="utf-8")
    for arq in sorted(pasta.iterdir()):
        print(f"publico/{arq.name}  ({arq.stat().st_size // 1024} KB)")
