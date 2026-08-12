"""Selecao de provider com degradacao para stub.

Regra: se a credencial nao existe, a pipeline nao quebra — ela avisa e continua
offline. Isso mantem o CI verde e permite testar edicao e render sem gastar
credito.
"""

from __future__ import annotations

import logging

from ..config import Config
from .base import ErroOrcamento, ErroProvider, GeradorImagem, LLM, TTS
from .stubs import ImagemStub, LLMStub, TTSStub

log = logging.getLogger("maquina.providers")


def _fallback(nome: str, erro: Exception, stub):
    log.warning("provider %s indisponivel (%s) — usando stub offline", nome, erro)
    return stub


class LLMCadeia:
    """Cadeia de LLMs que troca de fornecedor NA CHAMADA, nao so na construcao.

    A versao anterior escolhia o provider uma vez, no inicio do run, e ficava
    presa nele. Quando o Gemini devolveu 429 as 22:14 de 12/08/2026 — cota
    diaria do free tier — nao havia para onde ir: o job morreu com a Anthropic
    disponivel e ociosa. Trocar so na construcao protege contra chave ausente,
    que e o problema raro; nao protege contra provider que cai no meio, que e o
    problema real.

    Um elo que falha fica marcado como morto pelo resto do run: se a cota do
    dia acabou na primeira chamada, ela nao volta na quinta.
    """

    def __init__(self, elos: list[tuple[str, object]]):
        self._elos = elos            # [(nome, fabrica)] na ordem de preferencia
        self._construidos: dict[str, object] = {}
        self._mortos: set[str] = set()

    @property
    def custo_usd(self) -> float:
        # Soma TODOS os construidos, inclusive os que morreram depois: um elo
        # que gastou US$ 0,50 em quatro chamadas e caiu na quinta gastou os
        # US$ 0,50 do mesmo jeito, e o custo por video precisa saber disso.
        return sum(getattr(llm, "custo_usd", 0.0) for llm in self._construidos.values())

    def completar(
        self, prompt: str, *, sistema: str = "", max_tokens: int = 4096, esforco: str = ""
    ) -> str:
        erros = []
        for nome, fabrica in self._elos:
            if nome in self._mortos:
                continue
            try:
                llm = self._construidos.get(nome)
                if llm is None:
                    llm = self._construidos[nome] = fabrica()
                    log.info("llm: usando %s", nome)
                return llm.completar(
                    prompt, sistema=sistema, max_tokens=max_tokens, esforco=esforco
                )
            except ErroOrcamento:
                # Teto de gasto e decisao do operador, nao falha de fornecedor:
                # cair para o proximo elo so mudaria de bolso.
                raise
            except ErroProvider as e:
                log.warning("llm: %s falhou (%s) — proximo da cadeia", nome, e)
                erros.append(f"{nome}: {e}")
                self._mortos.add(nome)

        raise ErroProvider(
            "nenhum LLM da cadeia respondeu: " + " | ".join(erros or ["cadeia vazia"])
        )


def obter_llm(cfg: Config) -> LLM:
    """Seleciona o LLM.

    A ordem de preferencia e Anthropic -> OpenAI -> Gemini. O Gemini saiu da
    frente em 13/08/2026: o free tier de 20 requisicoes/dia nao cabe seis
    pacotes diarios, e roteiro e a peca que decide o video. Ele fica no fim da
    fila como rede de seguranca gratuita, nao como padrao.

    Sem nenhuma chave, cai no stub offline — e o que mantem o CI verde. Mas se
    HA chave e o provider morre no meio, a cadeia levanta erro em vez de
    escorregar para o stub: roteiro de stub publicado e pior que run falho.
    """
    if cfg.llm_provider == "stub":
        return LLMStub()

    import os

    from .reais import LLMAnthropic, LLMGemini, LLMOpenAI

    def _anthropic():
        return LLMAnthropic(
            cfg.llm_model, esforco=cfg.llm_esforco, teto_usd=cfg.llm_teto_usd
        )

    catalogo = {
        "anthropic": ("ANTHROPIC_API_KEY", _anthropic),
        "openai": ("OPENAI_API_KEY", lambda: LLMOpenAI(cfg.llm_model_openai)),
        "gemini": ("GEMINI_API_KEY", lambda: LLMGemini(cfg.llm_model_gemini)),
    }

    if cfg.llm_provider == "auto":
        ordem = ["anthropic", "openai", "gemini"]
    elif cfg.llm_provider in catalogo:
        # Provider explicito e escolha, nao sugestao: sem cadeia atras dele.
        ordem = [cfg.llm_provider]
    else:
        return _fallback(
            cfg.llm_provider,
            ErroProvider(f"llm_provider desconhecido: {cfg.llm_provider}"),
            LLMStub(),
        )

    elos = [(nome, catalogo[nome][1]) for nome in ordem if os.getenv(catalogo[nome][0])]
    if not elos:
        return _fallback("auto", ErroProvider("nenhuma chave de LLM presente"), LLMStub())
    return LLMCadeia(elos)


def obter_tts(cfg: Config) -> TTS:
    if cfg.tts_provider == "stub":
        return TTSStub()
    if cfg.tts_provider == "lote":
        from .lote import TTSLote

        return TTSLote()
    try:
        from .reais import TTSEdge, TTSElevenLabs, TTSFishAudio, TTSModal, TTSOpenAI

        if cfg.tts_provider == "edge":
            return TTSEdge(cfg.canal.voz_edge or "id-ID-ArdiNeural")
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
        from .reais import ImagemOpenAI, ImagemPollinations

        if cfg.image_provider == "pollinations":
            return ImagemPollinations()
        if cfg.image_provider == "openai":
            return ImagemOpenAI(cfg.image_model)
        raise ErroProvider(f"image_provider desconhecido: {cfg.image_provider}")
    except ErroProvider as e:
        return _fallback(cfg.image_provider, e, ImagemStub())


__all__ = [
    "obter_llm",
    "obter_tts",
    "obter_imagem",
    "ErroProvider",
    "ErroOrcamento",
    "LLMCadeia",
]
