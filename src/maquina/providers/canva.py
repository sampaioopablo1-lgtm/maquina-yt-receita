"""Thumbnail via Canva Connect API (autofill em brand template).

Fluxo CI sem browser:
  1. client_credentials → access_token efemero
  2. Upload do fundo PNG (gerado pelo OpenAI/outro provider)
  3. Autofill no brand template com o texto e a imagem
  4. Poll ate o job concluir → obtém design_id
  5. Export como PNG → poll → baixar
  6. Converter para JPEG ≤ 2 MB (limite YouTube)

Setup (uma vez por operador):
  1. developer.canva.com → "Create integration" → OAuth2 app
     Escopo minimo: asset:read asset:write design:content:read
                    design:content:write design:meta:read
  2. No Canva Studio: criar template 1280×720 (YouTube Thumbnail)
     Nomear o campo de imagem como "fundo" e o de texto como "titulo"
  3. Abrir o template → URL contem o ID (ex.: DAFxxxxxxx)
  4. Adicionar secrets no GitHub:
       CANVA_CLIENT_ID, CANVA_CLIENT_SECRET, CANVA_TEMPLATE_ID
"""

from __future__ import annotations

import base64
import logging
import os
import time
from pathlib import Path

import httpx
from PIL import Image

log = logging.getLogger("maquina.canva")

_TOKEN_URL = "https://api.canva.com/rest/v1/oauth/token"
_BASE = "https://api.canva.com/rest/v1"
_TIMEOUT = 30.0
_EXPORT_ESPERA_MAX = 90  # segundos


def configurado() -> bool:
    return bool(
        os.getenv("CANVA_CLIENT_ID")
        and os.getenv("CANVA_CLIENT_SECRET")
        and os.getenv("CANVA_TEMPLATE_ID")
    )


def _token() -> str:
    r = httpx.post(
        _TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": os.environ["CANVA_CLIENT_ID"],
            "client_secret": os.environ["CANVA_CLIENT_SECRET"],
            "scope": (
                "asset:read asset:write "
                "design:content:read design:content:write design:meta:read"
            ),
        },
        timeout=_TIMEOUT,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"Canva auth falhou {r.status_code}: {r.text[:200]}")
    return r.json()["access_token"]


def _headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _upload_asset(cli: httpx.Client, caminho: Path, token: str) -> str:
    """Faz upload de um arquivo PNG para os assets do Canva. Retorna o asset_id."""
    metadata = base64.b64encode(f'{{"name":"{caminho.name}"}}'.encode()).decode()
    with caminho.open("rb") as f:
        r = cli.post(
            f"{_BASE}/assets",
            content=f.read(),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/octet-stream",
                "Asset-Upload-Metadata": metadata,
            },
            timeout=60.0,
        )
    if r.status_code >= 400:
        raise RuntimeError(f"upload asset {r.status_code}: {r.text[:200]}")
    return r.json()["asset"]["id"]


def _autofill(cli: httpx.Client, template_id: str, titulo: str, asset_id: str) -> str:
    """Cria job de autofill e aguarda conclusao. Retorna o design_id gerado."""
    r = cli.post(
        f"{_BASE}/autofills",
        json={
            "brand_template_id": template_id,
            "title": f"thumb_{titulo[:40]}",
            "data": {
                "titulo": {"type": "text", "text": titulo},
                "fundo": {"type": "image", "asset_id": asset_id},
            },
        },
        timeout=_TIMEOUT,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"autofill {r.status_code}: {r.text[:200]}")
    job_id = r.json()["job"]["id"]

    # Poll ate concluir (normalmente < 10s)
    prazo = time.monotonic() + _EXPORT_ESPERA_MAX
    while time.monotonic() < prazo:
        time.sleep(3)
        s = cli.get(f"{_BASE}/autofills/{job_id}", timeout=_TIMEOUT)
        s.raise_for_status()
        job = s.json()["job"]
        if job["status"] == "success":
            return job["result"]["design"]["id"]
        if job["status"] == "failed":
            raise RuntimeError(f"autofill falhou: {job}")
    raise TimeoutError("autofill nao concluiu no tempo limite")


def _exportar(cli: httpx.Client, design_id: str) -> bytes:
    """Exporta o design como PNG e devolve os bytes."""
    r = cli.post(
        f"{_BASE}/exports",
        json={
            "design_id": design_id,
            "format": {"type": "png", "quality": "pro"},
            "pages": [1],
        },
        timeout=_TIMEOUT,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"export {r.status_code}: {r.text[:200]}")
    export_id = r.json()["job"]["id"]

    prazo = time.monotonic() + _EXPORT_ESPERA_MAX
    while time.monotonic() < prazo:
        time.sleep(3)
        s = cli.get(f"{_BASE}/exports/{export_id}", timeout=_TIMEOUT)
        s.raise_for_status()
        job = s.json()["job"]
        if job["status"] == "success":
            url = job["urls"][0]
            img_r = httpx.get(url, timeout=60.0)
            img_r.raise_for_status()
            return img_r.content
        if job["status"] == "failed":
            raise RuntimeError(f"export falhou: {job}")
    raise TimeoutError("export nao concluiu no tempo limite")


def gerar_thumbnail(
    texto: str,
    imagem_fundo: Path,
    destino: Path,
) -> Path:
    """Pipeline completo: upload → autofill → export → JPEG ≤ 2 MB.

    Args:
        texto: Texto curto do thumbnail (≤ 40 chars).
        imagem_fundo: PNG gerado pelo provider de imagens.
        destino: Caminho de saida (.jpg).

    Returns:
        Path do arquivo JPEG gravado em `destino`.
    """
    token = _token()

    with httpx.Client(timeout=_TIMEOUT) as cli:
        log.info("canva: enviando imagem de fundo...")
        asset_id = _upload_asset(cli, imagem_fundo, token)

        template_id = os.environ["CANVA_TEMPLATE_ID"]
        log.info("canva: autofill no template %s...", template_id)
        design_id = _autofill(cli, template_id, texto, asset_id)

        log.info("canva: exportando design %s...", design_id)
        png_bytes = _exportar(cli, design_id)

    # Salvar como JPEG ≤ 2 MB (limite YouTube)
    destino.parent.mkdir(parents=True, exist_ok=True)
    png_tmp = destino.with_suffix(".tmp.png")
    png_tmp.write_bytes(png_bytes)

    img = Image.open(png_tmp).convert("RGB")
    for qualidade in (92, 85, 75, 65):
        img.save(destino.with_suffix(".jpg"), "JPEG", quality=qualidade, optimize=True)
        if destino.with_suffix(".jpg").stat().st_size < 2_000_000:
            break
    png_tmp.unlink(missing_ok=True)

    resultado = destino.with_suffix(".jpg")
    log.info("thumbnail Canva salvo: %s", resultado)
    return resultado
