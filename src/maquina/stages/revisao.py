"""Ferramentas de revisao para canal em idioma que o operador nao le.

Operar um canal em indonesio a partir do portugues cria duas lacunas reais:
nao dar para julgar a naturalidade da saida, e nao dar para ler os comentarios
— que sao a fonte mais barata de diagnostico, normalmente aparecendo antes do
grafico de retencao. Este modulo fecha as duas.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from ..config import Config
from ..models import Roteiro
from ..providers.base import LLM, TTS

log = logging.getLogger("maquina.revisao")

# Texto curto e representativo do tom do canal, para avaliar o clone de voz.
# Frases com numeros e termos do nicho: e onde o sotaque aparece primeiro.
AMOSTRA_PROMPT = """Escreva um paragrafo de 4 frases em {idioma}, no tom do canal
(tema: {tema}; estilo: {estilo}).

Requisitos: inclua pelo menos um numero, um termo tecnico do nicho e uma
pergunta direta ao ouvinte. Este texto sera lido por uma voz sintetizada e
avaliado por um falante nativo — use construcoes naturais do idioma falado,
nao linguagem escrita formal.

Responda apenas com o paragrafo, sem aspas e sem comentarios."""

TRADUZIR_PROMPT = """Traduza para {destino} o texto abaixo, que esta em {origem}.

Alem da traducao, avalie a NATURALIDADE do original: um falante nativo diria
isso naturalmente, ou soa como texto traduzido/artificial?

JSON:
{{"traducao":"...","naturalidade":"natural|aceitavel|artificial","observacao":"..."}}

Texto:
{texto}"""

RESUMIR_COMENTARIOS_PROMPT = """Abaixo estao comentarios de um video do YouTube,
em {origem}. Traduza e sintetize para {destino}.

Procure especificamente por sinais acionaveis de problema tecnico: reclamacao de
volume de musica, qualidade ou naturalidade da voz, ritmo, legendas, audio. Esses
sinais costumam aparecer nos comentarios antes de aparecerem na curva de retencao.

JSON:
{{"resumo":"...",
  "sinais_tecnicos":["..."],
  "sentimento":"positivo|misto|negativo",
  "comentarios_relevantes":[{{"original":"...","traducao":"..."}}]}}

Comentarios:
{comentarios}"""


@dataclass
class AmostraVoz:
    texto: str
    audio: Path


def gerar_amostra_voz(
    llm: LLM, tts: TTS, cfg: Config, destino: Path, voice_id: str = ""
) -> AmostraVoz:
    """Gera um trecho curto para um falante nativo avaliar o clone de voz.

    Rodar isto antes de produzir o primeiro video inteiro: 15 minutos de teste
    evitam semanas de video com retencao ruim por sotaque.
    """
    texto = llm.completar(
        AMOSTRA_PROMPT.format(
            idioma=cfg.canal.idioma,
            tema=cfg.canal.tema,
            estilo=cfg.canal.estilo_narracao,
        )
    ).strip()

    destino.mkdir(parents=True, exist_ok=True)
    audio = tts.sintetizar(texto, destino / "amostra_voz.mp3", voice_id=voice_id)
    log.info("amostra gerada: %s", audio)
    return AmostraVoz(texto=texto, audio=audio)


def traduzir(llm: LLM, cfg: Config, texto: str) -> dict:
    """Traduz e avalia naturalidade — usado na revisao do roteiro."""
    from .roteiro import _json_do_llm

    return _json_do_llm(
        llm.completar(
            TRADUZIR_PROMPT.format(
                origem=cfg.canal.idioma,
                destino=cfg.canal.idioma_revisao,
                texto=texto[:6000],
            )
        )
    )


def revisar_roteiro(llm: LLM, cfg: Config, roteiro: Roteiro) -> dict:
    """Traduz o roteiro para o idioma do operador antes da aprovacao."""
    return traduzir(llm, cfg, roteiro.texto_completo)


def buscar_comentarios(cfg: Config, video_id: str, limite: int = 50) -> list[str]:
    """Puxa os comentarios de topo de um video."""
    from .youtube import _servico

    yt = _servico(cfg)
    resp = (
        yt.commentThreads()
        .list(part="snippet", videoId=video_id, maxResults=min(limite, 100),
              order="relevance", textFormat="plainText")
        .execute()
    )
    return [
        item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        for item in resp.get("items", [])
    ]


def analisar_comentarios(llm: LLM, cfg: Config, comentarios: list[str]) -> dict | None:
    """Traduz e extrai sinais tecnicos acionaveis dos comentarios."""
    if not comentarios:
        return None

    from .roteiro import _json_do_llm

    return _json_do_llm(
        llm.completar(
            RESUMIR_COMENTARIOS_PROMPT.format(
                origem=cfg.canal.idioma,
                destino=cfg.canal.idioma_revisao,
                comentarios="\n".join(f"- {c[:300]}" for c in comentarios[:50]),
            ),
            max_tokens=4096,
        )
    )
