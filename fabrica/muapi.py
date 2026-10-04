"""Cliente minimo da Muapi.ai — o motor por tras do Open Higgsfield AI.

O Open Higgsfield AI (ferramentas/open-higgsfield-ai) e uma interface web:
quatro estudios (imagem, video, lip sync, cinema) sobre a API da Muapi, com
mais de duzentos modelos (Flux, Nano Banana, Seedream, Kling, Veo, Wan, Sora,
Infinite Talk...). A fabrica nao tem browser: o que ela precisa e o mesmo
protocolo de duas etapas que o `packages/studio/src/muapi.js` usa —

  1. POST https://api.muapi.ai/api/v1/<endpoint>   (header x-api-key)
     -> {"request_id": "..."}
  2. GET  https://api.muapi.ai/api/v1/predictions/<request_id>/result
     ate status completed | succeeded | success, com `outputs[0]` = URL.

So stdlib, como o broll.py: o sandbox e o runner instalam a fabrica com
`pip install edge-tts cairosvg pydantic pillow` e nada mais. O catalogo com o
endpoint de cada modelo esta em config/muapi_modelos.json (gerado por
scripts/catalogo_muapi.mjs a partir do models.js do app); aqui vai so o mapa
dos poucos ids cujo endpoint difere do id, para a fabrica funcionar mesmo
quando o sandbox recebe apenas fabrica/*.py.
"""
from __future__ import annotations

import json
import mimetypes
import os
import ssl
import time
import urllib.error
import urllib.request
import uuid

BASE = "https://api.muapi.ai/api/v1"
UA = "maquina-yt-receita/fabrica (+open-higgsfield-ai)"

# ids do models.js cujo endpoint nao e o proprio id. Tudo que nao esta aqui
# usa endpoint == id, que e a regra do app (`modelInfo?.endpoint || model`).
ENDPOINTS = {
    "flux-dev": "flux-dev-image",
    "flux-schnell": "flux-schnell-image",
    "bytedance-seededit-v3": "bytedance-seededit-image",
    "latent-sync": "latentsync-video",
    "seedance-lite-reference-video": "seedance-lite-reference-to-video",
    "ai-image-upscaler": "ai-image-upscale",
    "ai-video-effects": "generate_wan_ai_effects",
    "motion-controls": "generate_wan_ai_effects",
    "vfx": "generate_wan_ai_effects",
}

# Modelos que recebem width/height em vez de aspect_ratio (familia Flux).
POR_PIXEL = {"flux-dev", "flux-schnell", "flux-dev-lora", "flux-krea-dev"}

TERMINOU = {"completed", "succeeded", "success"}
FALHOU = {"failed", "error", "cancelled", "canceled"}


class ErroMuapi(RuntimeError):
    """Falha da API — recuperavel do lado de quem chama (cai no fallback)."""


def _ctx():
    return ssl.create_default_context()


def endpoint_de(modelo: str) -> str:
    return ENDPOINTS.get(modelo, modelo)


def _req(url, chave, dados=None, metodo=None, content_type="application/json"):
    corpo = None
    headers = {"x-api-key": chave, "User-Agent": UA}
    if dados is not None:
        corpo = dados if isinstance(dados, bytes) else json.dumps(dados).encode()
        headers["Content-Type"] = content_type
    return urllib.request.Request(url, data=corpo, headers=headers,
                                  method=metodo or ("POST" if corpo else "GET"))


def _json(req, timeout):
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ctx()) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        texto = e.read(400).decode("utf-8", "replace")
        raise ErroMuapi(f"HTTP {e.code} em {req.full_url}: {texto}") from None


def submeter(chave: str, modelo: str, payload: dict, timeout=60) -> str:
    """Dispara a geracao e devolve o request_id."""
    r = _json(_req(f"{BASE}/{endpoint_de(modelo)}", chave, payload), timeout)
    rid = r.get("request_id") or r.get("id")
    if not rid:
        raise ErroMuapi(f"resposta sem request_id: {json.dumps(r)[:300]}")
    return rid


def esperar(chave: str, request_id: str, *, max_s=600, intervalo=3.0,
            dormir=time.sleep) -> dict:
    """Consulta ate terminar. Devolve o resultado com `url` normalizada."""
    fim = time.monotonic() + max_s
    ultimo = None
    while time.monotonic() < fim:
        dormir(intervalo)
        try:
            r = _json(_req(f"{BASE}/predictions/{request_id}/result", chave), 60)
        except ErroMuapi as e:
            # 5xx no meio da fila nao e veredito: o app tambem segue consultando.
            if "HTTP 5" in str(e):
                ultimo = e
                continue
            raise
        status = str(r.get("status", "")).lower()
        if status in TERMINOU:
            saidas = r.get("outputs") or []
            url = saidas[0] if saidas else r.get("url")
            if not url and isinstance(r.get("output"), dict):
                url = r["output"].get("url")
            if not url:
                raise ErroMuapi(f"terminou sem URL de saida: {json.dumps(r)[:300]}")
            r["url"] = url
            return r
        if status in FALHOU:
            raise ErroMuapi(f"geracao falhou: {r.get('error') or r}")
    raise ErroMuapi(f"tempo esgotado ({max_s}s) esperando {request_id}"
                    + (f" — ultimo erro: {ultimo}" if ultimo else ""))


def baixar(url: str, destino: str, timeout=120) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout, context=_ctx()) as r, \
            open(destino, "wb") as f:
        while True:
            peda = r.read(1 << 20)
            if not peda:
                break
            f.write(peda)
    return destino


def upload(chave: str, caminho: str, timeout=120) -> str:
    """POST /upload_file (multipart) -> URL hospedada, para modelos que
    recebem imagem/audio/video de referencia (i2i, i2v, lip sync)."""
    limite = uuid.uuid4().hex
    nome = os.path.basename(caminho)
    mime = mimetypes.guess_type(nome)[0] or "application/octet-stream"
    corpo = (f"--{limite}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"{nome}\"\r\nContent-Type: {mime}\r\n\r\n").encode()
    corpo += open(caminho, "rb").read() + f"\r\n--{limite}--\r\n".encode()
    r = _json(_req(f"{BASE}/upload_file", chave, corpo,
                   content_type=f"multipart/form-data; boundary={limite}"), timeout)
    url = r.get("url") or r.get("file_url") or (r.get("data") or {}).get("url")
    if not url:
        raise ErroMuapi(f"upload sem URL: {json.dumps(r)[:300]}")
    return url


def payload_imagem(modelo: str, prompt: str, largura: int, altura: int,
                   **extras) -> dict:
    """O corpo certo para o modelo: Flux quer pixels (multiplos de 64), o
    resto quer aspect_ratio."""
    p = {"prompt": prompt}
    if modelo in POR_PIXEL:
        p["width"] = max(128, min(2048, largura // 64 * 64))
        p["height"] = max(128, min(2048, altura // 64 * 64))
    else:
        p["aspect_ratio"] = proporcao(largura, altura)
    p.update({k: v for k, v in extras.items() if v is not None})
    return p


def proporcao(w: int, h: int) -> str:
    r = w / h
    tabela = [("16:9", 16 / 9), ("9:16", 9 / 16), ("1:1", 1.0), ("4:3", 4 / 3),
              ("3:4", 3 / 4), ("3:2", 1.5), ("2:3", 2 / 3), ("21:9", 21 / 9)]
    return min(tabela, key=lambda t: abs(t[1] - r))[0]


def gerar_imagem(chave: str, modelo: str, prompt: str, destino: str, *,
                 largura=1280, altura=720, max_s=300, **extras) -> dict:
    """Texto -> arquivo de imagem em `destino`. Devolve o resultado da API."""
    rid = submeter(chave, modelo, payload_imagem(modelo, prompt, largura, altura, **extras))
    r = esperar(chave, rid, max_s=max_s)
    baixar(r["url"], destino)
    return r


def gerar_video(chave: str, modelo: str, prompt: str, destino: str, *,
                image_url: str | None = None, max_s=1200, **extras) -> dict:
    """Texto (ou imagem + texto) -> arquivo de video em `destino`."""
    p = {"prompt": prompt}
    if image_url:
        p["image_url"] = image_url
    p.update({k: v for k, v in extras.items() if v is not None})
    rid = submeter(chave, modelo, p)
    r = esperar(chave, rid, max_s=max_s, intervalo=5.0)
    baixar(r["url"], destino)
    return r


def lipsync(chave: str, modelo: str, audio_url: str, destino: str, *,
            image_url: str | None = None, video_url: str | None = None,
            max_s=1200, **extras) -> dict:
    """Retrato + audio (ou video + audio) -> video falando."""
    p = {"audio_url": audio_url}
    if image_url:
        p["image_url"] = image_url
    if video_url:
        p["video_url"] = video_url
    p.update({k: v for k, v in extras.items() if v is not None})
    rid = submeter(chave, modelo, p)
    r = esperar(chave, rid, max_s=max_s, intervalo=5.0)
    baixar(r["url"], destino)
    return r
