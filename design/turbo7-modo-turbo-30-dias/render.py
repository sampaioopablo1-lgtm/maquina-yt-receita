#!/usr/bin/env python3
"""Renderiza flyer.html em PNG de alta resolução e PDF para impressão."""

import subprocess
import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
LARGURA, ALTURA = 1200, 2160          # canvas em px CSS
ESCALA = 2                            # 2400 × 4320 px na saída
NOME = "flyer-turbo7-modo-turbo-30-dias"

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


def png() -> Path:
    bruto = RAIZ / "_bruto.png"
    executar(BASE + [
        f"--force-device-scale-factor={ESCALA}",
        f"--window-size={LARGURA},{ALTURA + FOLGA}",
        f"--screenshot={bruto}", str(RAIZ / "flyer.html"),
    ])
    destino = RAIZ / f"{NOME}.png"
    with Image.open(bruto) as im:
        im.crop((0, 0, LARGURA * ESCALA, ALTURA * ESCALA)).save(destino, optimize=True)
    bruto.unlink()
    return destino


def pdf() -> Path:
    destino = RAIZ / f"{NOME}.pdf"
    executar(BASE + [
        f"--window-size={LARGURA},{ALTURA + FOLGA}",
        "--no-pdf-header-footer", f"--print-to-pdf={destino}",
        str(RAIZ / "flyer.html"),
    ])
    return destino


if __name__ == "__main__":
    for caminho in (png(), pdf()):
        print(f"{caminho.name}  ({caminho.stat().st_size // 1024} KB)")
