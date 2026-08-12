"""Providers de producao (Anthropic, OpenAI, ElevenLabs)."""

from __future__ import annotations

import base64
import json
import logging
import os
import time
from pathlib import Path
from typing import Callable

import httpx

from .base import ErroOrcamento, ErroProvider

log = logging.getLogger("maquina.providers")

TIMEOUT = httpx.Timeout(300.0, connect=30.0)

# Erros transitorios do lado do provider (rate limit, sobrecarga) — a mesma
# chamada tende a funcionar minutos depois. Ver ROTINA.md/APRENDIZADOS.md:
# Gemini 503 e Pollinations 429 ja derrubaram lotes inteiros de producao.
_STATUS_TRANSITORIOS = {429, 500, 502, 503, 504}


def _com_retry(
    fazer_chamada: Callable[[], httpx.Response],
    *,
    tentativas: int = 3,
    espera_inicial: float = 4.0,
) -> httpx.Response:
    """Repete uma chamada HTTP em erro transitorio, com backoff exponencial."""
    r = fazer_chamada()
    tentativa = 0
    while r.status_code in _STATUS_TRANSITORIOS and tentativa < tentativas - 1:
        time.sleep(espera_inicial * (2**tentativa))
        tentativa += 1
        r = fazer_chamada()
    return r


# Precos por 1M de tokens / por unidade. Usados so para estimar custo por video.
PRECO_ANTHROPIC = {
    "claude-opus-5": {"entrada": 5.00, "saida": 25.00},
    "claude-sonnet-5": {"entrada": 3.00, "saida": 15.00},
    "claude-haiku-4-5": {"entrada": 1.00, "saida": 5.00},
}
# Desconhecido cobra como o mais caro: subestimar gasto derrota o teto.
PRECO_ANTHROPIC_PADRAO = {"entrada": 5.00, "saida": 25.00}
PRECO_OPENAI_LLM = {"entrada": 2.50, "saida": 10.00}
PRECO_ELEVENLABS_POR_MIL_CHARS = 0.30
PRECO_FISH_POR_MILHAO_BYTES = 15.0
PRECO_IMAGEM_UNIDADE = 0.04


class _Transitorio(RuntimeError):
    """Falha que vale repetir na mesma chamada (429, 5xx, queda de conexao)."""


class LLMAnthropic:
    """Roteirista da maquina desde 13/08/2026 — saimos do Gemini.

    O free tier do Gemini da 20 requisicoes por DIA e cada pacote consome de 2 a
    5 (ideacao, roteiro, ate duas extensoes, short companheiro). Com seis
    disparos diarios a cota estoura antes do meio-dia: foi o 429 que derrubou
    next-level-money em 12/08/2026. O teto nao era de qualidade, era de
    quantidade — a maquina nao cabia no plano gratuito.

    Tres decisoes que valem explicacao:

    * `thinking: {type: "adaptive"}` — o roteiro e a unica peca que decide se o
      video presta; o modelo pensa o quanto o problema pedir. `budget_tokens`
      NAO existe mais nesta familia (400 na hora).
    * `stream: True` sempre — o roteiro do longo pede 16k tokens de saida e a
      chamada nao-streaming estoura o limite de tempo do request antes de
      terminar. Streaming tambem e o que a API exige acima de ~21k.
    * `max_tokens` recebe RESERVA_PENSAMENTO por cima do pedido, porque o
      pensamento sai do mesmo orcamento da resposta. Sem a folga o modelo pensa
      e e cortado no meio do JSON — que aparece la na frente como
      "JSON invalido", sem dizer que a causa foi truncamento.
    """

    MODELO_PADRAO = "claude-opus-5"
    RESERVA_PENSAMENTO = 8192
    TENTATIVAS = 3

    def __init__(self, modelo: str = "", *, esforco: str = "medium", teto_usd: float = 0.0):
        self.modelo = modelo or self.MODELO_PADRAO
        self.esforco = esforco
        self.teto_usd = teto_usd
        self.custo_usd = 0.0
        # Guarda contra o mesmo campo `llm_model` servir a tres providers: com
        # `llm_model: gemini-flash-latest` no YAML, esta classe pedia um modelo
        # do Google a api.anthropic.com e tomava 404 no meio da producao.
        if not self.modelo.startswith("claude-"):
            raise ErroProvider(
                f"llm_model '{self.modelo}' nao e um modelo Anthropic — use "
                f"llm_model_gemini/llm_model_openai para os outros providers"
            )
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

    def completar(
        self, prompt: str, *, sistema: str = "", max_tokens: int = 4096, esforco: str = ""
    ) -> str:
        if self.teto_usd and self.custo_usd >= self.teto_usd:
            raise ErroOrcamento(
                f"LLM ja gastou US$ {self.custo_usd:.2f} neste run e o teto e "
                f"US$ {self.teto_usd:.2f} — run interrompido antes de gastar mais. "
                f"Ajuste MAQ_LLM_TETO_USD se o teto e que esta baixo."
            )

        corpo: dict = {
            "model": self.modelo,
            "max_tokens": max_tokens + self.RESERVA_PENSAMENTO,
            "messages": [{"role": "user", "content": prompt}],
            "thinking": {"type": "adaptive"},
            "output_config": {"effort": esforco or self.esforco},
            "stream": True,
        }
        if sistema:
            corpo["system"] = sistema

        texto, uso, parou_por = self._com_retry_stream(corpo)

        preco = PRECO_ANTHROPIC.get(self.modelo, PRECO_ANTHROPIC_PADRAO)
        self.custo_usd += (
            uso.get("input_tokens", 0) / 1e6 * preco["entrada"]
            + uso.get("output_tokens", 0) / 1e6 * preco["saida"]
        )

        if parou_por == "max_tokens":
            raise ErroProvider(
                f"Anthropic cortou a resposta em max_tokens ({max_tokens} + "
                f"{self.RESERVA_PENSAMENTO} de pensamento). O texto veio pela "
                f"metade — nao e JSON invalido, e resposta truncada."
            )
        if not texto.strip():
            raise ErroProvider("Anthropic devolveu resposta sem texto")
        return texto

    def _com_retry_stream(self, corpo: dict) -> tuple[str, dict, str]:
        ultimo = ""
        for tentativa in range(self.TENTATIVAS):
            try:
                return self._uma_chamada(corpo)
            except _Transitorio as e:
                ultimo = str(e)
                if tentativa < self.TENTATIVAS - 1:
                    espera = 4.0 * (2**tentativa)
                    log.warning("Anthropic transitorio (%s) — repete em %.0fs", e, espera)
                    time.sleep(espera)
        raise ErroProvider(f"Anthropic falhou em {self.TENTATIVAS} tentativas: {ultimo}")

    def _uma_chamada(self, corpo: dict) -> tuple[str, dict, str]:
        pedacos: list[str] = []
        uso: dict = {}
        parou_por = ""
        try:
            with self._cli.stream("POST", "/v1/messages", json=corpo) as r:
                if r.status_code >= 400:
                    r.read()
                    msg = f"Anthropic {r.status_code}: {r.text[:400]}"
                    if r.status_code in _STATUS_TRANSITORIOS:
                        raise _Transitorio(msg)
                    raise ErroProvider(msg)

                for linha in r.iter_lines():
                    if not linha.startswith("data:"):
                        continue
                    evento = json.loads(linha[5:].strip())
                    tipo = evento.get("type")
                    if tipo == "content_block_delta":
                        delta = evento.get("delta", {})
                        # Blocos de pensamento vem no mesmo stream; so o texto
                        # entra na resposta.
                        if delta.get("type") == "text_delta":
                            pedacos.append(delta.get("text", ""))
                    elif tipo == "message_start":
                        uso.update(evento.get("message", {}).get("usage", {}))
                    elif tipo == "message_delta":
                        uso.update(evento.get("usage", {}))
                        parou_por = evento.get("delta", {}).get("stop_reason") or parou_por
                    elif tipo == "error":
                        raise _Transitorio(f"evento de erro no stream: {str(evento)[:300]}")
        except httpx.TransportError as e:
            # Stream longo cai por rede com mais frequencia que POST curto.
            raise _Transitorio(f"{type(e).__name__}: {e}") from e

        return "".join(pedacos), uso, parou_por


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

    def completar(
        self, prompt: str, *, sistema: str = "", max_tokens: int = 4096, esforco: str = ""
    ) -> str:
        mensagens = ([{"role": "system", "content": sistema}] if sistema else []) + [
            {"role": "user", "content": prompt}
        ]
        r = _com_retry(
            lambda: self._cli.post(
                "/chat/completions",
                json={"model": self.modelo, "messages": mensagens, "max_tokens": max_tokens},
            )
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

    def completar(
        self, prompt: str, *, sistema: str = "", max_tokens: int = 4096, esforco: str = ""
    ) -> str:
        corpo: dict = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": max_tokens},
        }
        if sistema:
            corpo["systemInstruction"] = {"parts": [{"text": sistema}]}

        r = _com_retry(
            lambda: self._cli.post(f"/models/{self.modelo}:generateContent", json=corpo)
        )
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

        r = _com_retry(
            lambda: self._cli.post(
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

        r = _com_retry(
            lambda: self._cli.post(
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
        r = _com_retry(
            lambda: self._cli.post(self.url, json={"text": texto, "token": self.token})
        )
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

    # O endpoint da Microsoft nega pedido de IP de datacenter de forma
    # INTERMITENTE, e o erro nao diz isso: vem como NoAudioReceived, "verifique
    # seus parametros", que aponta para a voz ou o texto. Os parametros estavam
    # certos. Medido em 2026-08-12: o mesmo runner narrou um video inteiro as
    # 14:46 e as 16:50 nao recebeu audio nenhum; a mesma voz e o mesmo texto
    # funcionaram no sandbox no mesmo minuto.
    #
    # Sem retry, UMA cena recusada derruba o lote inteiro — e um longo tem 78
    # cenas, entao a chance de nenhuma ser recusada e baixa. O custo de errar
    # aqui e o pacote todo; o custo de tentar de novo sao segundos.
    TENTATIVAS = 4
    ESPERA_S = 3

    def sintetizar(self, texto: str, saida: Path, *, voice_id: str = "") -> Path:
        import asyncio
        import time

        import edge_tts

        voz = voice_id or self.voz
        saida.parent.mkdir(parents=True, exist_ok=True)

        async def _gerar():
            communicate = edge_tts.Communicate(texto, voz)
            await communicate.save(str(saida))

        ultimo: Exception | None = None
        for tentativa in range(1, self.TENTATIVAS + 1):
            try:
                asyncio.run(_gerar())
                # Arquivo vazio conta como falha: o edge-tts as vezes fecha o
                # stream sem erro e deixa um mp3 de zero byte, que so apareceria
                # depois, na concatenacao, como cena muda.
                if saida.exists() and saida.stat().st_size > 0:
                    return saida
                ultimo = ErroProvider(f"edge-tts devolveu arquivo vazio para {saida.name}")
            except Exception as e:  # NoAudioReceived, ClientResponseError, timeout
                ultimo = e
            if tentativa < self.TENTATIVAS:
                time.sleep(self.ESPERA_S * tentativa)  # 3s, 6s, 9s

        raise ErroProvider(
            f"edge-tts falhou em {self.TENTATIVAS} tentativas para a voz {voz}: "
            f"{type(ultimo).__name__}: {ultimo}. "
            "NoAudioReceived costuma ser recusa por IP de datacenter, nao "
            "parametro errado — a mesma chamada tende a funcionar fora do runner."
        ) from ultimo


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
        r = _com_retry(
            lambda: self._cli.post(
                "/audio/speech",
                json={
                    "model": self.modelo,
                    "voice": voice_id or self.voz,
                    "input": texto,
                    "response_format": "mp3",
                },
            )
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

    def gerar(self, prompt: str, saida: Path, *, largura: int, altura: int) -> Path:
        import urllib.parse

        prompt_enc = urllib.parse.quote(prompt[:500])
        url = (
            f"https://image.pollinations.ai/prompt/{prompt_enc}"
            f"?width={largura}&height={altura}&model=flux&nologo=true&seed=42"
        )
        # Retry mais paciente que o padrao (3 tentativas, 12 s no total): a
        # Pollinations limita por janela de tempo, e 12 s nao atravessa a janela.
        # Medido: o video kenapa-karyawan-... morreu inteiro com
        # "Pollinations 429: Too Many Requests" numa cena so.
        #
        # Aqui esperar e de graca e falhar custa o pacote: um longo tem 78 cenas
        # geradas em sequencia, entao a chance de nenhuma cair numa janela cheia
        # e baixa. 5 tentativas com 8/16/32/64 s cobrem dois minutos de limite.
        r = _com_retry(
            lambda: httpx.get(url, timeout=120.0, follow_redirects=True),
            tentativas=5,
            espera_inicial=8.0,
        )
        if r.status_code >= 400:
            raise ErroProvider(
                f"Pollinations {r.status_code} apos 5 tentativas: {r.text[:200]}. "
                "429 aqui e limite de taxa, nao prompt invalido."
            )
        # Corpo vazio com status 200 acontece quando a geracao expira do lado
        # deles. Sem esta checagem o arquivo entra no video como cena preta.
        if not r.content:
            raise ErroProvider("Pollinations devolveu 200 com corpo vazio")
        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_bytes(r.content)
        return saida


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
        r = _com_retry(
            lambda: self._cli.post(
                "/images/generations",
                json={"model": self.modelo, "prompt": prompt, "size": tamanho, "n": 1},
            )
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
