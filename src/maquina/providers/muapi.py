"""Muapi.ai — o motor do Open Higgsfield AI, como provider da pipeline.

O Open Higgsfield AI (ferramentas/open-higgsfield-ai) e o estudio web; este
modulo e o mesmo protocolo de duas etapas (submeter -> consultar resultado)
falado em httpx, no idioma dos outros providers de `reais.py`:

  POST {BASE}/{endpoint}                  header x-api-key  -> request_id
  GET  {BASE}/predictions/{id}/result     ate completed     -> outputs[0]

Dois usos na pipeline:
  * `ImagemMuapi` implementa `GeradorImagem` (cenas e fundo da thumbnail) —
    ativa com MAQ_IMAGE_PROVIDER=muapi e MUAPI_API_KEY;
  * `VideoMuapi` gera clipes de video (texto ou imagem -> video) e lip sync,
    para quem quiser ir alem do Ken Burns. Nao entra na pipeline sozinho.

O catalogo com os 221 modelos e seus endpoints esta em
config/muapi_modelos.json (gerado de models.js do app). A mesma logica, em
stdlib, vive em fabrica/muapi.py para o sandbox — os dois nao se importam de
proposito: a fabrica roda sem o pacote instalado.
"""

from __future__ import annotations

import json
import logging
import os
import time
from functools import lru_cache
from pathlib import Path

import httpx

from .base import ErroProvider

log = logging.getLogger("maquina.muapi")

BASE = "https://api.muapi.ai/api/v1"
CATALOGO = Path(__file__).resolve().parents[3] / "config" / "muapi_modelos.json"
TERMINOU = {"completed", "succeeded", "success"}
FALHOU = {"failed", "error", "cancelled", "canceled"}

# Preco de referencia por imagem (US$). A Muapi cobra por modelo; este e um
# teto conservador para o `maquina custo` nao mostrar zero enquanto a fatura
# real nao entra no banco.
PRECO_IMAGEM_REFERENCIA = 0.01

MODELO_IMAGEM_PADRAO = "flux-schnell"
MODELO_VIDEO_PADRAO = "kling-v2.1-standard-i2v"
MODELO_LIPSYNC_PADRAO = "infinitetalk-image-to-video"


@lru_cache(maxsize=1)
def catalogo() -> dict[str, dict]:
    """id -> entrada do catalogo. Vazio se o JSON nao estiver no disco."""
    try:
        dados = json.loads(CATALOGO.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {m["id"]: m for m in dados.get("modelos", [])}


def endpoint_de(modelo: str) -> str:
    return catalogo().get(modelo, {}).get("endpoint", modelo)


def proporcao(w: int, h: int, aceitas: list[str] | None = None) -> str:
    r = w / h
    tabela = {"16:9": 16 / 9, "9:16": 9 / 16, "1:1": 1.0, "4:3": 4 / 3,
              "3:4": 3 / 4, "3:2": 1.5, "2:3": 2 / 3, "21:9": 21 / 9}
    if aceitas:
        tabela = {k: v for k, v in tabela.items() if k in aceitas} or tabela
    return min(tabela, key=lambda k: abs(tabela[k] - r))


class Muapi:
    """Cliente bruto: submete, espera, baixa, sobe arquivo."""

    def __init__(self, chave: str = "", *, timeout: float = 60.0, dormir=time.sleep):
        chave = chave or os.getenv("MUAPI_API_KEY", "")
        if not chave:
            raise ErroProvider("MUAPI_API_KEY ausente")
        self._cli = httpx.Client(
            base_url=BASE, headers={"x-api-key": chave}, timeout=timeout
        )
        self._dormir = dormir

    def submeter(self, modelo: str, payload: dict) -> str:
        r = self._cli.post(f"/{endpoint_de(modelo)}", json=payload)
        if r.status_code >= 400:
            raise ErroProvider(f"Muapi {r.status_code} em {modelo}: {r.text[:300]}")
        dados = r.json()
        rid = dados.get("request_id") or dados.get("id")
        if not rid:
            raise ErroProvider(f"Muapi sem request_id: {r.text[:300]}")
        return rid

    def esperar(self, request_id: str, *, max_s: float = 600, intervalo: float = 3.0) -> dict:
        fim = time.monotonic() + max_s
        while time.monotonic() < fim:
            self._dormir(intervalo)
            r = self._cli.get(f"/predictions/{request_id}/result")
            if r.status_code >= 500:
                continue  # fila instavel nao e veredito; o app tambem insiste
            if r.status_code >= 400:
                raise ErroProvider(f"Muapi {r.status_code} consultando {request_id}: {r.text[:300]}")
            dados = r.json()
            status = str(dados.get("status", "")).lower()
            if status in TERMINOU:
                saidas = dados.get("outputs") or []
                url = saidas[0] if saidas else dados.get("url")
                if not url and isinstance(dados.get("output"), dict):
                    url = dados["output"].get("url")
                if not url:
                    raise ErroProvider(f"Muapi terminou sem URL: {r.text[:300]}")
                dados["url"] = url
                return dados
            if status in FALHOU:
                raise ErroProvider(f"Muapi falhou: {dados.get('error') or dados}")
        raise ErroProvider(f"Muapi: tempo esgotado ({max_s}s) em {request_id}")

    def baixar(self, url: str, destino: Path) -> Path:
        r = self._cli.get(url, follow_redirects=True, timeout=300.0)
        if r.status_code >= 400 or not r.content:
            raise ErroProvider(f"Muapi: download {r.status_code} vazio de {url}")
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(r.content)
        return destino

    def upload(self, caminho: Path) -> str:
        with open(caminho, "rb") as f:
            r = self._cli.post("/upload_file", files={"file": (caminho.name, f)}, timeout=300.0)
        if r.status_code >= 400:
            raise ErroProvider(f"Muapi upload {r.status_code}: {r.text[:300]}")
        d = r.json()
        url = d.get("url") or d.get("file_url") or (d.get("data") or {}).get("url")
        if not url:
            raise ErroProvider(f"Muapi upload sem URL: {r.text[:300]}")
        return url

    def gerar(self, modelo: str, payload: dict, destino: Path, *, max_s: float = 600,
              intervalo: float = 3.0) -> dict:
        rid = self.submeter(modelo, payload)
        log.info("muapi: %s request_id=%s", modelo, rid)
        r = self.esperar(rid, max_s=max_s, intervalo=intervalo)
        self.baixar(r["url"], destino)
        return r


def payload_imagem(modelo: str, prompt: str, largura: int, altura: int) -> dict:
    campos = catalogo().get(modelo, {}).get("campos", [])
    p: dict = {"prompt": prompt}
    if "width" in campos or (not campos and modelo.startswith("flux-")):
        p["width"] = max(128, min(2048, largura // 64 * 64))
        p["height"] = max(128, min(2048, altura // 64 * 64))
    else:
        p["aspect_ratio"] = proporcao(largura, altura, catalogo().get(modelo, {}).get("aspect_ratio"))
    return p


class ImagemMuapi:
    """GeradorImagem sobre a Muapi. Modelo em MAQ_IMAGE_MODEL (ou o padrao)."""

    def __init__(self, modelo: str = ""):
        self.modelo = modelo if modelo and modelo in catalogo() else MODELO_IMAGEM_PADRAO
        if modelo and self.modelo != modelo:
            log.warning("muapi: modelo %r nao e de imagem no catalogo — usando %s",
                        modelo, self.modelo)
        self.custo_usd = 0.0
        self._api = Muapi()

    def gerar(self, prompt: str, saida: Path, *, largura: int, altura: int) -> Path:
        self._api.gerar(self.modelo, payload_imagem(self.modelo, prompt, largura, altura),
                        saida, max_s=300)
        self.custo_usd += PRECO_IMAGEM_REFERENCIA
        return saida


class VideoMuapi:
    """Clipes de video e lip sync. Fora da pipeline padrao: quem chama decide."""

    def __init__(self, modelo: str = MODELO_VIDEO_PADRAO):
        self.modelo = modelo
        self._api = Muapi()

    def de_imagem(self, imagem: Path, prompt: str, saida: Path, *, duracao: int | None = None,
                  aspect_ratio: str | None = None) -> Path:
        p: dict = {"prompt": prompt, "image_url": self._api.upload(imagem)}
        if duracao:
            p["duration"] = duracao
        if aspect_ratio:
            p["aspect_ratio"] = aspect_ratio
        self._api.gerar(self.modelo, p, saida, max_s=1200, intervalo=5.0)
        return saida

    def de_texto(self, prompt: str, saida: Path, *, modelo: str = "", duracao: int | None = None,
                 aspect_ratio: str | None = None) -> Path:
        p: dict = {"prompt": prompt}
        if duracao:
            p["duration"] = duracao
        if aspect_ratio:
            p["aspect_ratio"] = aspect_ratio
        self._api.gerar(modelo or self.modelo, p, saida, max_s=1200, intervalo=5.0)
        return saida

    def lipsync(self, retrato: Path, audio: Path, saida: Path, *,
                modelo: str = MODELO_LIPSYNC_PADRAO, resolution: str = "720p") -> Path:
        p = {"image_url": self._api.upload(retrato), "audio_url": self._api.upload(audio),
             "resolution": resolution}
        self._api.gerar(modelo, p, saida, max_s=1800, intervalo=5.0)
        return saida
