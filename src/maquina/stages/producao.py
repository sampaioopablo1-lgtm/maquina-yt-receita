"""Narracao, visuais e legendas: transforma o roteiro em assets."""

from __future__ import annotations

import logging
import time
from pathlib import Path

from .. import media
from ..models import Formato, Roteiro
from ..providers.base import GeradorImagem, TTS

log = logging.getLogger("maquina.producao")

# Teto de tempo por cena, em segundos, para cada etapa que fala com provider
# externo. Nao e uma estimativa do normal — e o ponto a partir do qual desistir
# vale mais que insistir.
#
# O normal medido e ~5 s por cena no TTS e ~15 s na imagem. Em 12/08/2026 um job
# ficou DUAS HORAS no passo de producao sem terminar e sem nada que o
# interrompesse: as retentativas de TTS e de Pollinations nao tem teto agregado,
# entao um provider degradado consome os 300 min de timeout do job inteiro e o
# unico sinal e o silencio.
#
# Com teto, um provider ruim custa alguns minutos e devolve um erro que diz onde
# parou. Os arquivos ja gerados ficam em disco e `maquina retomar <slug>`
# continua de la — desistir aqui nao joga trabalho fora.
ORCAMENTO_TTS_S = 60.0
ORCAMENTO_IMAGEM_S = 90.0


class OrcamentoEstourado(RuntimeError):
    """Etapa passou do teto de tempo. Os artefatos parciais estao preservados."""


def _vigia(etapa: str, total: int, por_cena: float):
    """Devolve uma funcao que levanta quando o tempo acumulado passa do teto."""
    inicio = time.monotonic()
    teto = por_cena * max(total, 1)

    def conferir(feitas: int) -> None:
        gasto = time.monotonic() - inicio
        if gasto > teto:
            raise OrcamentoEstourado(
                f"{etapa} passou do teto: {gasto / 60:.1f} min para {feitas} de "
                f"{total} cenas (teto {teto / 60:.1f} min, {por_cena:.0f} s/cena). "
                "Provider degradado. Os arquivos prontos ficaram em disco — "
                "`maquina retomar <slug>` continua daqui."
            )

    return conferir


def narrar(tts: TTS, roteiro: Roteiro, destino: Path, voice_id: str = "") -> None:
    """Sintetiza a narracao de cada cena e mede a duracao real do audio.

    A duracao vem do arquivo, nao de estimativa — e ela que sincroniza imagem e
    legenda. Estimar aqui e a origem classica de legenda dessincronizada.
    """
    pasta = destino / "audio"
    pasta.mkdir(parents=True, exist_ok=True)

    conferir = _vigia("narracao", len(roteiro.cenas), ORCAMENTO_TTS_S)
    for feitas, cena in enumerate(roteiro.cenas, 1):
        saida = pasta / f"cena_{cena.indice:03d}.mp3"
        if not saida.exists():
            tts.sintetizar(cena.narracao, saida, voice_id=voice_id)
        cena.audio_path = str(saida)
        cena.duracao_s = media.duracao(saida)
        log.info("cena %d/%d narrada (%.1fs)", feitas, len(roteiro.cenas), cena.duracao_s)
        conferir(feitas)


def ilustrar(
    gerador: GeradorImagem, roteiro: Roteiro, destino: Path, formato: Formato
) -> None:
    pasta = destino / "imagens"
    pasta.mkdir(parents=True, exist_ok=True)
    largura, altura = formato.resolucao

    conferir = _vigia("ilustracao", len(roteiro.cenas), ORCAMENTO_IMAGEM_S)
    for feitas, cena in enumerate(roteiro.cenas, 1):
        saida = pasta / f"cena_{cena.indice:03d}.png"
        if not saida.exists():
            gerador.gerar(cena.prompt_visual, saida, largura=largura, altura=altura)
        cena.imagem_path = str(saida)
        log.info("cena %d/%d ilustrada", feitas, len(roteiro.cenas))
        conferir(feitas)


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
