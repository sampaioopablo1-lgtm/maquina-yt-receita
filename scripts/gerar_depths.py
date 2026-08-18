#!/usr/bin/env python3
"""Fábrica de mapas de profundidade das visitas virtuais.

Para cada foto real de anúncio, gera um mapa de profundidade com MiDaS small
(Intel, open-source, ONNX, roda em CPU a ~1s/foto) e publica em
visitas/depths/<djb2(url)>.jpg. A página /visita/ detecta o mapa e liga o
parallax 2.5D — movimento tridimensional DENTRO da foto verdadeira, sem
inventar um pixel. Foto sem mapa continua caindo no Ken Burns.

Roda no runner do GitHub (fabrica-visita.yml, de hora em hora). Prioridade:
imóvel de maior valor primeiro (fn_fotos_sem_depth ordena assim).

Uso: SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... python3 gerar_depths.py [lote]
"""
import io
import json
import os
import sys
import urllib.request

import numpy as np
import onnxruntime as ort
from PIL import Image

SB = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
LOTE = int(sys.argv[1]) if len(sys.argv) > 1 else 800
MODELO_URL = "https://github.com/isl-org/MiDaS/releases/download/v2_1/model-small.onnx"
MODELO = "/tmp/midas_small.onnx"


def djb2(s: str) -> str:
    """Mesmo hash da página /visita/ — os dois lados precisam bater."""
    h = 5381
    for c in s:
        h = ((h * 33) + ord(c)) & 0xFFFFFFFF
    return format(h, "08x")


def api(caminho: str, corpo: bytes | None = None, tipo: str = "application/json",
        metodo: str = "GET", extra: dict | None = None) -> bytes:
    req = urllib.request.Request(f"{SB}{caminho}", data=corpo, method=metodo)
    req.add_header("apikey", KEY)
    req.add_header("Authorization", f"Bearer {KEY}")
    req.add_header("Content-Type", tipo)
    for k, v in (extra or {}).items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def main() -> None:
    if not os.path.exists(MODELO):
        urllib.request.urlretrieve(MODELO_URL, MODELO)

    fila = json.loads(api("/rest/v1/rpc/fn_fotos_sem_depth", metodo="POST",
                          corpo=json.dumps({"p_n": LOTE}).encode()))
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
            api(f"/storage/v1/object/visitas/depths/{h}.jpg", corpo=buf.getvalue(),
                tipo="image/jpeg", metodo="POST", extra={"x-upsert": "true"})
            linhas.append({"url": url, "codigo_vista": codigo, "hash": h})
            feitos += 1
        except Exception as e:  # noqa: BLE001 — uma foto ruim não derruba o lote
            erros += 1
            print(f"erro em {codigo}: {e}", file=sys.stderr)

    if linhas:
        api("/rest/v1/feed_visita_depth", metodo="POST",
            corpo=json.dumps(linhas).encode(),
            extra={"Prefer": "resolution=merge-duplicates"})

    print(f"mapas gerados: {feitos} · erros: {erros} · restam na fila: sob demanda")


if __name__ == "__main__":
    main()
