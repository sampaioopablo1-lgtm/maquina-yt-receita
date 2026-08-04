"""Narracao serverless com a voz clonada — Chatterbox indonesio no Modal.

Substitui o passo manual do Colab: o GitHub Actions chama este endpoint e
recebe o MP3. O free tier do Modal (US$ 30/mes recorrentes, ~50h de T4) cobre
o ritmo diario do canal com folga enorme (~3 min de GPU por video).

Setup (uma vez, ~10 min):
    pip install modal
    modal setup                                    # login pelo navegador
    modal secret create maquina-tts TOKEN=<invente-um-token-forte>
    modal run infra/modal_tts.py --ref assets/voice/referencia.wav   # sobe a voz
    modal deploy infra/modal_tts.py                # publica o endpoint

A URL impressa no deploy vai para o .env / secret do Actions:
    MAQ_TTS_PROVIDER=modal
    MAQ_TTS_URL=https://<workspace>--maquina-tts-narrar.modal.run
    MAQ_TTS_TOKEN=<o mesmo token>

Modelo: grandhigh/Chatterbox-TTS-Indonesian (Apache 2.0 — comercial liberado).
Para outros idiomas, troque por ResembleAI/chatterbox (MIT, 20+ linguas).
"""

from __future__ import annotations

import io

import modal

app = modal.App("maquina-tts")

MODELO_HF = "grandhigh/Chatterbox-TTS-Indonesian"
VOL_PESOS = modal.Volume.from_name("maquina-tts-pesos", create_if_missing=True)
VOL_VOZ = modal.Volume.from_name("maquina-tts-voz", create_if_missing=True)
REF_PATH = "/voz/referencia.wav"

imagem = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg")
    .pip_install(
        "chatterbox-tts",
        "huggingface_hub",
        "torchaudio",
        "fastapi[standard]",
    )
)


@app.function(
    image=imagem,
    gpu="T4",
    volumes={"/pesos": VOL_PESOS, "/voz": VOL_VOZ},
    secrets=[modal.Secret.from_name("maquina-tts")],
    # Janela curta: o container morre logo apos o uso e nao gasta credito parado.
    scaledown_window=120,
    timeout=600,
)
@modal.fastapi_endpoint(method="POST")
def narrar(item: dict):
    """POST {"text": "...", "token": "..."} -> audio/mpeg (MP3).

    Parametros opcionais: exaggeration (0.35), cfg_weight (0.4).
    """
    import os

    from fastapi import HTTPException
    from fastapi.responses import Response

    if item.get("token") != os.environ["TOKEN"]:
        raise HTTPException(401, "token invalido")

    texto = (item.get("text") or "").strip()
    if not texto:
        raise HTTPException(422, "campo 'text' vazio")
    if len(texto) > 4000:
        raise HTTPException(422, "texto acima de 4000 caracteres — divida por cena")

    import torchaudio
    from huggingface_hub import snapshot_download
    from chatterbox.tts import ChatterboxTTS

    ckpt = snapshot_download(MODELO_HF, cache_dir="/pesos")
    VOL_PESOS.commit()

    try:
        modelo = ChatterboxTTS.from_local(ckpt, device="cuda")
    except Exception:
        modelo = ChatterboxTTS.from_pretrained(device="cuda")

    wav = modelo.generate(
        texto,
        audio_prompt_path=REF_PATH,
        exaggeration=float(item.get("exaggeration", 0.35)),
        cfg_weight=float(item.get("cfg_weight", 0.4)),
    )

    buf = io.BytesIO()
    torchaudio.save(buf, wav, modelo.sr, format="mp3")
    return Response(content=buf.getvalue(), media_type="audio/mpeg")


@app.local_entrypoint()
def main(ref: str = ""):
    """`modal run infra/modal_tts.py --ref assets/voice/referencia.wav`"""
    if not ref:
        print("passe --ref <arquivo.wav> para subir a voz de referencia")
        return
    with open(ref, "rb") as f:
        dados = f.read()
    with VOL_VOZ.batch_upload(force=True) as up:
        up.put_file(io.BytesIO(dados), "/referencia.wav")
    print(f"voz de referencia enviada ({len(dados) / 1e6:.1f} MB) -> {REF_PATH}")
    print("agora: modal deploy infra/modal_tts.py")
