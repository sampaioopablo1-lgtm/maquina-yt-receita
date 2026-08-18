#!/usr/bin/env python3
"""Converte para JPEG real as fotos PNG que estão com extensão .jpg.

O portal só importa jpg ("Serão importados somente imagens no formato jpg");
PNG disfarçado é descartado em silêncio e o anúncio perde a foto. A fila vem
da Edge Function fila-conversao (alimentada pela auditoria medir-fotos), o
arquivo convertido sobe pelo midia-upload para o bucket fotos-portal, e o
registro em feed_foto_convertida faz o cron do banco trocar a URL no feed.

Uso: AUDITORIA_TOKEN=... python3 converter_fotos_png.py
"""
import io
import json
import os
import sys
import urllib.request

from PIL import Image

BASE = "https://cscczluzpblzhvojxanp.supabase.co/functions/v1"
TOKEN = os.environ["AUDITORIA_TOKEN"]


def djb2(s: str) -> str:
    h = 5381
    for c in s:
        h = ((h * 33) + ord(c)) & 0xFFFFFFFF
    return format(h, "08x")


def chamada(caminho: str, corpo: bytes | None = None, tipo: str = "application/json"):
    req = urllib.request.Request(f"{BASE}{caminho}", data=corpo,
                                 method="POST" if corpo else "GET")
    req.add_header("x-auditoria-token", TOKEN)
    req.add_header("Content-Type", tipo)
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def main() -> None:
    fila = chamada("/fila-conversao")["fila"]
    if not fila:
        print("fila vazia")
        return

    registros, erros = [], 0
    for item in fila:
        cod, url = item["codigo_vista"], item["url"]
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                im = Image.open(io.BytesIO(r.read())).convert("RGB")
            buf = io.BytesIO()
            im.save(buf, format="JPEG", quality=90)
            h = djb2(url)
            resp = chamada(f"/midia-upload?bucket=fotos-portal&caminho={cod}/{h}.jpg",
                           corpo=buf.getvalue(), tipo="image/jpeg")
            assert resp.get("ok"), resp
            registros.append({"url_original": url, "codigo_vista": cod,
                              "url_jpeg": resp["url_publica"]})
        except Exception as e:  # noqa: BLE001 — uma foto ruim não derruba o lote
            erros += 1
            print(f"erro {cod}: {e}", file=sys.stderr)

    if registros:
        r = chamada("/registrar-conversao", corpo=json.dumps(registros).encode())
        assert r.get("ok"), r
    print(f"convertidas {len(registros)} · erros {erros}")


if __name__ == "__main__":
    main()
