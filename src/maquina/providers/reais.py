"""Providers de producao (Anthropic, OpenAI, ElevenLabs)."""

from __future__ import annotations

import base64
import os
import time
from pathlib import Path

import httpx

from .base import ErroProvider

TIMEOUT = httpx.Timeout(300.0, connect=30.0)

# Precos por 1M de tokens / por unidade. Usados so para estimar custo por video.
PRECO_ANTHROPIC = {"entrada": 3.00, "saida": 15.00}
PRECO_OPENAI_LLM = {"entrada": 2.50, "saida": 10.00}
PRECO_ELEVENLABS_POR_MIL_CHARS = 0.30
PRECO_FISH_POR_MILHAO_BYTES = 15.0
PRECO_IMAGEM_UNIDADE = 0.04


class LLMAnthropic:
    def __init__(self, modelo: str):
        self.modelo = modelo
        self.custo_usd = 0.0
        chave = os.getenv("ANTHROPIC_API_KEY")
        if not chave:
            raise ErroProvider("ANTHROPIC_API_KEY ausente")
        self._cli = httpx.Client(
            base_url=os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com"),
            headers={
                "x-api-key": chave,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            timeout=TIMEOUT,
        )

    def completar(self, prompt: str, *, sistema: str = "", max_tokens: int = 4096) -> str:
        corpo: dict = {
            "model": self.modelo,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if sistema:
            corpo["system"] = sistema

        r = self._cli.post("/v1/messages", json=corpo)
        if r.status_code >= 400:
            raise ErroProvider(f"Anthropic {r.status_code}: {r.text[:400]}")
        dados = r.json()

        uso = dados.get("usage", {})
        self.custo_usd += (
            uso.get("input_tokens", 0) / 1e6 * PRECO_ANTHROPIC["entrada"]
            + uso.get("output_tokens", 0) / 1e6 * PRECO_ANTHROPIC["saida"]
        )
        return "".join(b.get("text", "") for b in dados.get("content", []))


class LLMOpenAI:
    def __init__(self, modelo: str):
        self.modelo = modelo
        self.custo_usd = 0.0
        chave = os.getenv("OPENAI_API_KEY")
        if not chave:
            raise ErroProvider("OPENAI_API_KEY ausente")
        self._cli = httpx.Client(
            base_url="https://api.openai.com/v1",
            headers={"Authorization": f"Bearer {chave}"},
            timeout=TIMEOUT,
        )

    def completar(self, prompt: str, *, sistema: str = "", max_tokens: int = 4096) -> str:
        mensagens = ([{"role": "system", "content": sistema}] if sistema else []) + [
            {"role": "user", "content": prompt}
        ]
        r = self._cli.post(
            "/chat/completions",
            json={"model": self.modelo, "messages": mensagens, "max_tokens": max_tokens},
        )
        if r.status_code >= 400:
            raise ErroProvider(f"OpenAI {r.status_code}: {r.text[:400]}")
        dados = r.json()

        uso = dados.get("usage", {})
        self.custo_usd += (
            uso.get("prompt_tokens", 0) / 1e6 * PRECO_OPENAI_LLM["entrada"]
            + uso.get("completion_tokens", 0) / 1e6 * PRECO_OPENAI_LLM["saida"]
        )
        return dados["choices"][0]["message"]["content"]


class LLMGemini:
    """Plano B do roteiro: Google Gemini, com free tier real.

    O free tier do AI Studio (aistudio.google.com -> Get API key) cobre o ritmo
    diario do canal sem cartao de credito. Qualidade de roteiro levemente
    inferior ao caminho principal, mas plenamente utilizavel.
    """

    def __init__(self, modelo: str = "gemini-flash-latest"):
        self.modelo = modelo
        self.custo_usd = 0.0  # free tier
        chave = os.getenv("GEMINI_API_KEY")
        if not chave:
            raise ErroProvider("GEMINI_API_KEY ausente")
        # x-goog-api-key e o metodo atual; cobre tanto chaves AIza classicas
        # quanto os formatos novos do AI Studio.
        self._cli = httpx.Client(
            base_url="https://generativelanguage.googleapis.com/v1beta",
            headers={"x-goog-api-key": chave},
            timeout=TIMEOUT,
        )

    def completar(self, prompt: str, *, sistema: str = "", max_tokens: int = 4096) -> str:
        corpo: dict = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": max_tokens},
        }
        if sistema:
            corpo["systemInstruction"] = {"parts": [{"text": sistema}]}

        r = self._cli.post(f"/models/{self.modelo}:generateContent", json=corpo)
        if r.status_code >= 400:
            raise ErroProvider(f"Gemini {r.status_code}: {r.text[:400]}")

        dados = r.json()
        partes = (
            (dados.get("candidates") or [{}])[0]
            .get("content", {})
            .get("parts", [])
        )
        texto = "".join(p.get("text", "") for p in partes)
        if not texto:
            raise ErroProvider(f"Gemini sem texto na resposta: {str(dados)[:300]}")
        return texto


class TTSElevenLabs:
    """Narracao com voz clonada do operador (ver docs/00-decisoes.md)."""

    def __init__(self, modelo: str, voice_id: str):
        self.modelo = modelo
        self.voice_id = voice_id
        self.custo_usd = 0.0
        chave = os.getenv("ELEVENLABS_API_KEY")
        if not chave:
            raise ErroProvider("ELEVENLABS_API_KEY ausente")
        self._cli = httpx.Client(
            base_url="https://api.elevenlabs.io/v1",
            headers={"xi-api-key": chave},
            timeout=TIMEOUT,
        )

    def sintetizar(self, texto: str, saida: Path, *, voice_id: str = "") -> Path:
        vid = voice_id or self.voice_id
        if not vid:
            raise ErroProvider("MAQ_TTS_VOICE_ID ausente — rode `maquina voice-clone`")

        r = self._cli.post(
            f"/text-to-speech/{vid}",
            json={
                "text": texto,
                "model_id": self.modelo,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "style": 0.15,
                    "use_speaker_boost": True,
                },
            },
        )
        if r.status_code >= 400:
            raise ErroProvider(f"ElevenLabs {r.status_code}: {r.text[:400]}")

        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_bytes(r.content)
        self.custo_usd += len(texto) / 1000 * PRECO_ELEVENLABS_POR_MIL_CHARS
        return saida

    def clonar_voz(self, nome: str, amostras: list[Path]) -> str:
        """Registra a voz do operador e devolve o voice_id."""
        arquivos = [
            ("files", (p.name, p.read_bytes(), "audio/mpeg")) for p in amostras
        ]
        r = self._cli.post("/voices/add", data={"name": nome}, files=arquivos)
        if r.status_code >= 400:
            raise ErroProvider(f"ElevenLabs clone {r.status_code}: {r.text[:400]}")
        return r.json()["voice_id"]


class TTSFishAudio:
    """Narracao via Fish Audio — onde a voz clonada do operador ja existe.

    A voz "Pablo (eu)" foi clonada na conta do operador; o voice_id (model id
    do Fish) vai em MAQ_TTS_VOICE_ID. A chave NUNCA no codigo: apenas na env
    FISH_AUDIO_API_KEY — a chave anterior vazou em chat e deve estar revogada.
    """

    def __init__(self, voice_id: str):
        self.voice_id = voice_id
        self.custo_usd = 0.0
        chave = os.getenv("FISH_AUDIO_API_KEY")
        if not chave:
            raise ErroProvider("FISH_AUDIO_API_KEY ausente")
        self._cli = httpx.Client(
            base_url="https://api.fish.audio",
            headers={"Authorization": f"Bearer {chave}"},
            timeout=TIMEOUT,
        )

    def sintetizar(self, texto: str, saida: Path, *, voice_id: str = "") -> Path:
        vid = voice_id or self.voice_id
        if not vid:
            raise ErroProvider(
                "MAQ_TTS_VOICE_ID ausente — use o id do modelo de voz do Fish "
                "(o trecho final da URL fish.audio/m/<id>)"
            )

        r = self._cli.post(
            "/v1/tts",
            json={
                "text": texto,
                "reference_id": vid,
                "format": "mp3",
                "mp3_bitrate": 192,
                "normalize": True,
                "latency": "normal",
            },
        )
        if r.status_code >= 400:
            raise ErroProvider(f"Fish Audio {r.status_code}: {r.text[:400]}")

        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_bytes(r.content)
        self.custo_usd += len(texto.encode("utf-8")) / 1e6 * PRECO_FISH_POR_MILHAO_BYTES
        return saida


class TTSModal:
    """Narracao serverless no Modal — Chatterbox indonesio com a voz clonada.

    Endpoint publicado por `modal deploy infra/modal_tts.py`. O free tier do
    Modal (US$30/mes recorrentes) cobre o ritmo diario do canal, entao o custo
    contabilizado aqui e zero.
    """

    custo_usd = 0.0

    def __init__(self):
        self.url = os.getenv("MAQ_TTS_URL", "")
        self.token = os.getenv("MAQ_TTS_TOKEN", "")
        if not self.url:
            raise ErroProvider(
                "MAQ_TTS_URL ausente — rode `modal deploy infra/modal_tts.py` "
                "e aponte a URL publicada (ver docs/09-voz-gratuita.md)"
            )
        self._cli = httpx.Client(timeout=TIMEOUT)

    def sintetizar(self, texto: str, saida: Path, *, voice_id: str = "") -> Path:
        r = self._cli.post(self.url, json={"text": texto, "token": self.token})
        if r.status_code >= 400:
            raise ErroProvider(f"Modal TTS {r.status_code}: {r.text[:300]}")
        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_bytes(r.content)
        return saida


class TTSEdge:
    """Microsoft Edge TTS — gratuito, sem chave de API.

    Voz padrao: id-ID-ArdiNeural (indonesio masculino, natural).
    Lista completa: `edge-tts --list` ou docs/09-voz-gratuita.md.
    Qualidade inferior ao clone de voz do operador, mas plenamente usavel para
    validar o roteiro e medir retencao antes de investir em TTS pago.
    """

    custo_usd = 0.0

    def __init__(self, voz: str = "id-ID-ArdiNeural"):
        try:
            import edge_tts  # noqa: F401
        except ImportError:
            raise ErroProvider(
                "edge-tts nao instalado — `pip install edge-tts` ou "
                "`pip install -e '.[gratuito]'`"
            )
        self.voz = voz

    def sintetizar(self, texto: str, saida: Path, *, voice_id: str = "") -> Path:
        import asyncio
        import edge_tts

        voz = voice_id or self.voz
        saida.parent.mkdir(parents=True, exist_ok=True)

        async def _gerar():
            communicate = edge_tts.Communicate(texto, voz)
            await communicate.save(str(saida))

        asyncio.run(_gerar())
        return saida


class TTSOpenAI:
    def __init__(self, modelo: str = "gpt-4o-mini-tts", voz: str = "onyx"):
        self.modelo = modelo
        self.voz = voz
        self.custo_usd = 0.0
        chave = os.getenv("OPENAI_API_KEY")
        if not chave:
            raise ErroProvider("OPENAI_API_KEY ausente")
        self._cli = httpx.Client(
            base_url="https://api.openai.com/v1",
            headers={"Authorization": f"Bearer {chave}"},
            timeout=TIMEOUT,
        )

    def sintetizar(self, texto: str, saida: Path, *, voice_id: str = "") -> Path:
        r = self._cli.post(
            "/audio/speech",
            json={
                "model": self.modelo,
                "voice": voice_id or self.voz,
                "input": texto,
                "response_format": "mp3",
            },
        )
        if r.status_code >= 400:
            raise ErroProvider(f"OpenAI TTS {r.status_code}: {r.text[:400]}")
        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_bytes(r.content)
        self.custo_usd += len(texto) / 1e6 * 12.0
        return saida


class ImagemPollinations:
    """Geracao de imagem via Pollinations.AI — gratuito, sem chave de API.

    API publica: GET https://image.pollinations.ai/prompt/{prompt}
    Parametros: width, height, model (flux), nologo=true, seed.
    Qualidade cinematografica real; adequada para as cenas do canal.
    """

    custo_usd = 0.0

    # 429 = fila cheia (limite de 1 requisicao concorrente por IP no plano gratuito);
    # 5xx = instabilidade do servico. Ambos passam com uma pausa curta.
    _STATUS_TRANSITORIOS = {429, 500, 502, 503, 504}
    _TENTATIVAS = 4
    _ESPERA_S = 8

    def gerar(self, prompt: str, saida: Path, *, largura: int, altura: int) -> Path:
        import urllib.parse

        prompt_enc = urllib.parse.quote(prompt[:500])
        url = (
            f"https://image.pollinations.ai/prompt/{prompt_enc}"
            f"?width={largura}&height={altura}&model=flux&nologo=true&seed=42"
        )
        ultimo_erro: Exception | None = None
        for tentativa in range(1, self._TENTATIVAS + 1):
            try:
                r = httpx.get(url, timeout=120.0, follow_redirects=True)
            except httpx.TransportError as e:
                ultimo_erro = e
            else:
                if r.status_code < 400:
                    saida.parent.mkdir(parents=True, exist_ok=True)
                    saida.write_bytes(r.content)
                    return saida
                ultimo_erro = ErroProvider(f"Pollinations {r.status_code}: {r.text[:200]}")
                if r.status_code not in self._STATUS_TRANSITORIOS:
                    raise ultimo_erro
            if tentativa < self._TENTATIVAS:
                time.sleep(self._ESPERA_S * tentativa)
        raise ultimo_erro


class ImagemOpenAI:
    def __init__(self, modelo: str = "gpt-image-1"):
        self.modelo = modelo
        self.custo_usd = 0.0
        chave = os.getenv("OPENAI_API_KEY")
        if not chave:
            raise ErroProvider("OPENAI_API_KEY ausente")
        self._cli = httpx.Client(
            base_url="https://api.openai.com/v1",
            headers={"Authorization": f"Bearer {chave}"},
            timeout=TIMEOUT,
        )

    def gerar(self, prompt: str, saida: Path, *, largura: int, altura: int) -> Path:
        # A API aceita um conjunto fechado de tamanhos; escolhe pela orientacao.
        tamanho = "1024x1536" if altura > largura else "1536x1024"
        r = self._cli.post(
            "/images/generations",
            json={"model": self.modelo, "prompt": prompt, "size": tamanho, "n": 1},
        )
        if r.status_code >= 400:
            raise ErroProvider(f"OpenAI Images {r.status_code}: {r.text[:400]}")

        item = r.json()["data"][0]
        conteudo = (
            base64.b64decode(item["b64_json"])
            if "b64_json" in item
            else httpx.get(item["url"], timeout=TIMEOUT).content
        )
        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_bytes(conteudo)
        self.custo_usd += PRECO_IMAGEM_UNIDADE
        return saida
