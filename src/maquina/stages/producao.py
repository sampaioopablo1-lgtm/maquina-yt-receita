"""Narracao, visuais e legendas: transforma o roteiro em assets."""

from __future__ import annotations

import logging
from pathlib import Path

from .. import media
from ..models import Formato, Roteiro
from ..providers.base import GeradorImagem, TTS

log = logging.getLogger("maquina.producao")


def narrar(tts: TTS, roteiro: Roteiro, destino: Path, voice_id: str = "") -> None:
    """Sintetiza a narracao de cada cena e mede a duracao real do audio.

    A duracao vem do arquivo, nao de estimativa — e ela que sincroniza imagem e
    legenda. Estimar aqui e a origem classica de legenda dessincronizada.
    """
    pasta = destino / "audio"
    pasta.mkdir(parents=True, exist_ok=True)

    for cena in roteiro.cenas:
        saida = pasta / f"cena_{cena.indice:03d}.mp3"
        if not saida.exists():
            tts.sintetizar(cena.narracao, saida, voice_id=voice_id)
        cena.audio_path = str(saida)
        cena.duracao_s = media.duracao(saida)
        log.info("cena %d narrada (%.1fs)", cena.indice, cena.duracao_s)


def ilustrar(
    gerador: GeradorImagem, roteiro: Roteiro, destino: Path, formato: Formato
) -> None:
    pasta = destino / "imagens"
    pasta.mkdir(parents=True, exist_ok=True)
    largura, altura = formato.resolucao

    for cena in roteiro.cenas:
        saida = pasta / f"cena_{cena.indice:03d}.png"
        if not saida.exists():
            gerador.gerar(cena.prompt_visual, saida, largura=largura, altura=altura)
        cena.imagem_path = str(saida)
        log.info("cena %d ilustrada", cena.indice)


def _timestamp(segundos: float) -> str:
    ms = int(round(segundos * 1000))
    h, resto = divmod(ms, 3_600_000)
    m, resto = divmod(resto, 60_000)
    s, ms = divmod(resto, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def gerar_legendas(roteiro: Roteiro, saida: Path, max_chars: int = 42) -> Path:
    """SRT a partir das duracoes reais de cada cena.

    Quebra a narracao da cena em linhas curtas e divide a duracao da cena
    proporcionalmente ao numero de caracteres de cada linha — aproximacao boa o
    bastante sem exigir alinhamento forcado por Whisper.
    """
    blocos: list[str] = []
    indice = 1
    tempo = 0.0

    for cena in roteiro.cenas:
        dur = cena.duracao_s or 0.0
        if dur <= 0:
            continue

        linhas: list[str] = []
        atual = ""
        for palavra in cena.narracao.split():
            if len(atual) + len(palavra) + 1 > max_chars and atual:
                linhas.append(atual)
                atual = palavra
            else:
                atual = f"{atual} {palavra}".strip()
        if atual:
            linhas.append(atual)
        if not linhas:
            tempo += dur
            continue

        total_chars = sum(len(l) for l in linhas) or 1
        for linha in linhas:
            fatia = dur * len(linha) / total_chars
            blocos.append(
                f"{indice}\n{_timestamp(tempo)} --> {_timestamp(tempo + fatia)}\n{linha}\n"
            )
            indice += 1
            tempo += fatia

    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(blocos), encoding="utf-8")
    return saida
