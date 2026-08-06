#!/usr/bin/env python3
"""Gera auditoria.ps1 embutindo auditoria_demo.py e demo_upload.mp4.

Existe para o .ps1 nunca ser editado a mao. Ele carrega copia do programa
dentro de si; copia mantida a mao e copia que se afasta da original sem
avisar — foi assim que o etapas.py ficou com um loop de clipe antigo e o
pacote sairia sem animacao passando em todos os asserts.

Uso: python3 gerar_ps1.py   (roda dentro de scripts/)
"""
import base64, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
py = open(os.path.join(AQUI, "auditoria_demo.py"), encoding="utf-8").read()
b64 = base64.b64encode(open(os.path.join(AQUI, "demo_upload.mp4"), "rb").read()).decode()
linhas = "\n".join(b64[i:i + 120] for i in range(0, len(b64), 120))

if "\n'@" in py:
    sys.exit("erro: o programa contem uma linha iniciando com '@ e fecharia "
             "o here-string do PowerShell cedo demais")

molde = open(os.path.join(AQUI, "auditoria.ps1.molde"), encoding="utf-8").read()
saida = molde.replace("@@PROGRAMA@@", py).replace("@@MP4_B64@@", linhas)
with open(os.path.join(AQUI, "auditoria.ps1"), "w",
          encoding="utf-8-sig", newline="\r\n") as f:
    f.write(saida)
print(f"auditoria.ps1 gerado: {len(saida)} bytes")
