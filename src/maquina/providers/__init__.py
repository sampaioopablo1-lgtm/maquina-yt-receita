"""Selecao de provider com degradacao para stub.

Regra: se a credencial nao existe, a pipeline nao quebra — ela avisa e continua
offline. Isso mantem o CI verde e permite testar edicao e render sem gastar
credito.
"""

from __future__ import annotations

import logging

from ..config import Config
from .base import ErroProvider, GeradorImagem, LLM, TTS
from .stubs import ImagemStub, LLMStub, TTSStub

log = logging.getLogger("maquina.providers")


def _fallback(nome: str, erro: Exception, stub):
    log.warning("provider %s indisponivel (%s) — usando stub offline", nome, erro)
    return stub


def obter_llm(cfg: Config) -> LLM:
    if cfg.llm_provider == "stub":
        return LLMStub()
    try:
        from .reais import LLMAnthropic, LLMOpenAI

        if cfg.llm_provider == "anthropic":
            return LLMAnthropic(cfg.llm_model)
        if cfg.llm_provider == "openai":
            return LLMOpenAI(cfg.llm_model)
        raise ErroProvider(f"llm_provider desconhecido: {cfg.llm_provider}")
    except ErroProvider as e:
        return _fallback(cfg.llm_provider, e, LLMStub())


def obter_tts(cfg: Config) -> TTS:
    if cfg.tts_provider == "stub":
        return TTSStub()
    if cfg.tts_provider == "lote":
        from .lote import TTSLote

        return TTSLote()
    try:
        from .reais import TTSElevenLabs, TTSFishAudio, TTSModal, TTSOpenAI

        if cfg.tts_provider == "modal":
            return TTSModal()
        if cfg.tts_provider == "fish":
            return TTSFishAudio(cfg.tts_voice_id)
        if cfg.tts_provider == "elevenlabs":
            return TTSElevenLabs(cfg.tts_model, cfg.tts_voice_id)
        if cfg.tts_provider == "openai":
            return TTSOpenAI()
        raise ErroProvider(f"tts_provider desconhecido: {cfg.tts_provider}")
    except ErroProvider as e:
        return _fallback(cfg.tts_provider, e, TTSStub())


def obter_imagem(cfg: Config) -> GeradorImagem:
    if cfg.image_provider == "stub":
        return ImagemStub()
    try:
        from .reais import ImagemOpenAI

        if cfg.image_provider == "openai":
            return ImagemOpenAI(cfg.image_model)
        raise ErroProvider(f"image_provider desconhecido: {cfg.image_provider}")
    except ErroProvider as e:
        return _fallback(cfg.image_provider, e, ImagemStub())


__all__ = ["obter_llm", "obter_tts", "obter_imagem", "ErroProvider"]
