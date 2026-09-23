#!/usr/bin/env python3
"""A próxima peça da fila, pronta para publicar.

    python3 entregas/instagram/proxima.py                          # peça, URL e legenda
    python3 entregas/instagram/proxima.py --marcar "<permalink>"   # marca como publicada

Existe para a rotina diária não interpretar tabela em Markdown de cabeça: quem publica
lê daqui, e quem marca escreve por aqui, na mesma linha, com data e link.
"""
from __future__ import annotations

import datetime as dt
import pathlib
import re
import sys

AQUI = pathlib.Path(__file__).resolve().parent
FILA = AQUI / "FILA.md"


def linhas() -> list[str]:
    return FILA.read_text(encoding="utf-8").splitlines()


def proxima():
    for i, linha in enumerate(linhas()):
        c = [x.strip() for x in linha.split("|")]
        if len(c) >= 7 and c[5] == "pendente":
            return i, c[2], c[3], c[4]
    return None


def legenda(caminho: str) -> str:
    txt = (AQUI / caminho).read_text(encoding="utf-8")
    m = re.search(r"^LEGENDA\s*$", txt, re.M)
    return txt[m.end():].strip() if m else txt.strip()


def main() -> None:
    p = proxima()
    if "--marcar" in sys.argv:
        if not p:
            sys.exit("fila vazia: nada a marcar")
        link = sys.argv[sys.argv.index("--marcar") + 1]
        ls = linhas()
        i = p[0]
        c = ls[i].split("|")
        c[5] = " publicada "
        c[6] = f" {dt.datetime.now(dt.timezone.utc):%d/%m %H:%M} UTC · {link} "
        ls[i] = "|".join(c)
        FILA.write_text("\n".join(ls) + "\n", encoding="utf-8")
        print(f"marcada: {p[1]} -> {link}")
        return
    if not p:
        print("FILA VAZIA — produzir o próximo lote")
        sys.exit(2)
    _, peca, url, leg = p
    print(f"PECA {peca}\nURL {url}\nLEGENDA_ARQUIVO {leg}\n\n{legenda(leg)}")


if __name__ == "__main__":
    main()
