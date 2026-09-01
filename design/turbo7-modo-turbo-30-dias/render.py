#!/usr/bin/env python3
"""Renderiza flyer.html em PNG de alta resolução e PDF para impressão."""

import subprocess
import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
ESCALA = 2                            # dobra a resolução da saída

# fonte HTML -> (nome de saída, largura, altura) do canvas em px CSS
PECAS = {
    "flyer.html": ("flyer-turbo7-modo-turbo-30-dias", 1200, 2160),
    "funil.html": ("funil-marketing-vendas-turbo7", 1200, 1584),
}

# O headless reserva ~87px de altura de janela; pede-se folga e recorta-se depois.
FOLGA = 120

BASE = [
    CHROME, "--headless", "--disable-gpu", "--no-sandbox",
    "--allow-file-access-from-files", "--hide-scrollbars",
    "--virtual-time-budget=8000", "--font-render-hinting=none",
]


def executar(args: list[str]) -> None:
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"chromium falhou:\n{r.stderr[-2000:]}")


def png(fonte: str, nome: str, largura: int, altura: int) -> Path:
    bruto = RAIZ / "_bruto.png"
    executar(BASE + [
        f"--force-device-scale-factor={ESCALA}",
        f"--window-size={largura},{altura + FOLGA}",
        f"--screenshot={bruto}", str(RAIZ / fonte),
    ])
    destino = RAIZ / f"{nome}.png"
    with Image.open(bruto) as im:
        im.crop((0, 0, largura * ESCALA, altura * ESCALA)).save(destino, optimize=True)
    bruto.unlink()
    return destino


def pdf(fonte: str, nome: str, largura: int, altura: int) -> Path:
    destino = RAIZ / f"{nome}.pdf"
    executar(BASE + [
        f"--window-size={largura},{altura + FOLGA}",
        "--no-pdf-header-footer", f"--print-to-pdf={destino}",
        str(RAIZ / fonte),
    ])
    return destino


if __name__ == "__main__":
    alvos = sys.argv[1:] or list(PECAS)
    for fonte in alvos:
        nome, largura, altura = PECAS[fonte]
        for caminho in (png(fonte, nome, largura, altura),
                        pdf(fonte, nome, largura, altura)):
            print(f"{caminho.name}  ({caminho.stat().st_size // 1024} KB)")
