#!/usr/bin/env python3
"""Fábrica de mapas de profundidade das visitas virtuais.

Para cada foto real de anúncio, gera um mapa de profundidade com MiDaS small
(Intel, open-source, ONNX, roda em CPU a ~1s/foto) e publica em
visitas/depths/<djb2(url)>.jpg. A página /visita/ detecta o mapa e liga o
parallax 2.5D — movimento tridimensional DENTRO da foto verdadeira, sem
inventar um pixel. Foto sem mapa continua caindo no Ken Burns.

IMPORTANTE — por que este script NÃO usa os secrets SUPABASE_* do repositório:
eles apontam para o projeto Supabase da máquina YT, não para o projeto da
Jazz (a primeira execução falhou com 404 na RPC por causa disso). Todo o
acesso ao projeto da Jazz passa por Edge Functions token-gated (fila-depths,
midia-upload, registrar-depths) usando só AUDITORIA_TOKEN.

Uso: AUDITORIA_TOKEN=... python3 gerar_depths.py [lote]
"""
import io
import json
import os
import socket
import sys
import urllib.request

import numpy as np
import onnxruntime as ort
from PIL import Image

socket.setdefaulttimeout(30)

BASE = "https://cscczluzpblzhvojxanp.supabase.co/functions/v1"
TOKEN = os.environ["AUDITORIA_TOKEN"]
LOTE = int(sys.argv[1]) if len(sys.argv) > 1 else 800
MODELO_URL = "https://github.com/isl-org/MiDaS/releases/download/v2_1/model-small.onnx"
MODELO = "/tmp/midas_small.onnx"


def djb2(s: str) -> str:
    """Mesmo hash da página /visita/ — os dois lados precisam bater."""
    h = 5381
    for c in s:
        h = ((h * 33) + ord(c)) & 0xFFFFFFFF
    return format(h, "08x")


def chamada(caminho: str, corpo: bytes | None = None, tipo: str = "application/json"):
    req = urllib.request.Request(f"{BASE}{caminho}", data=corpo,
                                 method="POST" if corpo is not None else "GET")
    req.add_header("x-auditoria-token", TOKEN)
    req.add_header("Content-Type", tipo)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def main() -> None:
    if not os.path.exists(MODELO):
        urllib.request.urlretrieve(MODELO_URL, MODELO)

    fila = chamada("/fila-depths", corpo=json.dumps({"lote": LOTE}).encode())["fila"]
    if not fila:
        print("fila vazia — todas as fotos publicadas têm mapa")
        return

    sess = ort.InferenceSession(MODELO, providers=["CPUExecutionProvider"])
    entrada = sess.get_inputs()[0].name
    media = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    desvio = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    feitos, erros = 0, 0
    linhas = []
    for item in fila:
        url, codigo = item["url"], item["codigo"]
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                im = Image.open(io.BytesIO(r.read())).convert("RGB")
            x = np.asarray(im.resize((256, 256), Image.BILINEAR), dtype=np.float32) / 255.0
            x = ((x - media) / desvio).transpose(2, 0, 1)[None]
            d = sess.run(None, {entrada: x})[0][0]
            d = (d - d.min()) / max(1e-6, d.max() - d.min())
            dep = Image.fromarray((d * 255).astype(np.uint8)).resize(im.size, Image.BILINEAR)
            dep = dep.resize((im.size[0] // 2, im.size[1] // 2), Image.BILINEAR)
            buf = io.BytesIO()
            dep.save(buf, format="JPEG", quality=80)

            h = djb2(url)
            resp = chamada(f"/midia-upload?bucket=visitas&caminho=depths/{h}.jpg",
                           corpo=buf.getvalue(), tipo="image/jpeg")
            assert resp.get("ok"), resp
            linhas.append({"url": url, "codigo_vista": codigo, "hash": h})
            feitos += 1
            # registra de 100 em 100 para não perder trabalho se o runner cair
            if len(linhas) >= 100:
                chamada("/registrar-depths", corpo=json.dumps(linhas).encode())
                linhas = []
        except Exception as e:  # noqa: BLE001 — uma foto ruim não derruba o lote
            erros += 1
            print(f"erro em {codigo}: {e}", file=sys.stderr)

    if linhas:
        chamada("/registrar-depths", corpo=json.dumps(linhas).encode())

    print(f"mapas gerados: {feitos} · erros: {erros}")


if __name__ == "__main__":
    main()
