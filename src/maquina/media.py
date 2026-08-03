"""Wrapper de ffmpeg. Toda composicao de video passa por aqui."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from .models import Formato


def ffmpeg_bin() -> str:
    """Usa o ffmpeg do sistema; cai para o binario estatico do imageio-ffmpeg.

    O runner do GitHub Actions ja tem ffmpeg no PATH. Localmente, o pip resolve.
    """
    if found := shutil.which("ffmpeg"):
        return found
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def ffprobe_bin() -> str | None:
    return shutil.which("ffprobe")


def _run(args: list[str]) -> None:
    proc = subprocess.run(args, capture_output=True, text=True)
    if proc.returncode != 0:
        cauda = "\n".join(proc.stderr.strip().splitlines()[-15:])
        raise RuntimeError(f"ffmpeg falhou ({proc.returncode}):\n{cauda}")


def duracao(path: Path) -> float:
    """Duracao em segundos de um asset de midia."""
    if probe := ffprobe_bin():
        proc = subprocess.run(
            [probe, "-v", "quiet", "-print_format", "json", "-show_format", str(path)],
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0:
            return float(json.loads(proc.stdout)["format"]["duration"])

    # Sem ffprobe: ffmpeg decodifica para null e reporta o tempo final.
    proc = subprocess.run(
        [ffmpeg_bin(), "-i", str(path), "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    marca = 0.0
    for linha in proc.stderr.splitlines():
        if "time=" in linha:
            trecho = linha.split("time=")[-1].split()[0]
            try:
                h, m, s = trecho.split(":")
                marca = max(marca, int(h) * 3600 + int(m) * 60 + float(s))
            except ValueError:
                continue
    if marca <= 0:
        raise RuntimeError(f"nao consegui medir a duracao de {path}")
    return marca


def clipe_de_imagem(
    imagem: Path,
    audio: Path,
    saida: Path,
    formato: Formato,
    zoom: float = 0.12,
) -> Path:
    """Uma cena: imagem estatica + Ken Burns + a narracao daquela cena.

    O movimento de camera existe por retencao: imagem 100% parada derruba a
    curva. O zoom e sutil e alterna a direcao por cena (ver `render.py`) para
    nao virar o padrao repetitivo que o YouTube marca como conteudo de template.
    """
    larg, alt = formato.resolucao
    dur = duracao(audio)
    fps = 30
    quadros = max(int(dur * fps), 1)

    # Renderiza num canvas maior e faz zoompan para nao serrilhar a borda.
    escala = f"scale={larg * 2}:{alt * 2}:force_original_aspect_ratio=increase"
    corte = f"crop={larg * 2}:{alt * 2}"
    zp = (
        f"zoompan=z='min(zoom+{zoom / quadros:.8f},{1 + zoom})'"
        f":d={quadros}:s={larg}x{alt}:fps={fps}"
        f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    )

    _run(
        [
            ffmpeg_bin(), "-y",
            "-loop", "1", "-i", str(imagem),
            "-i", str(audio),
            "-filter_complex", f"[0:v]{escala},{corte},{zp},setsar=1[v]",
            "-map", "[v]", "-map", "1:a",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-t", f"{dur:.3f}",
            str(saida),
        ]
    )
    return saida


def concatenar(clipes: list[Path], saida: Path) -> Path:
    """Junta as cenas. Reencoda para garantir timebase uniforme."""
    lista = saida.parent / "concat.txt"
    lista.write_text(
        "".join(f"file '{c.resolve()}'\n" for c in clipes), encoding="utf-8"
    )
    _run(
        [
            ffmpeg_bin(), "-y",
            "-f", "concat", "-safe", "0", "-i", str(lista),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            str(saida),
        ]
    )
    lista.unlink(missing_ok=True)
    return saida


def aplicar_trilha(video: Path, musica: Path, saida: Path, ganho_db: float = -22.0) -> Path:
    """Mixa trilha de fundo bem abaixo da voz.

    -22 dB nao e arbitrario: musica alta e a reclamacao mais recorrente nos
    comentarios e um dos motivos diretos de queda de retencao.
    """
    _run(
        [
            ffmpeg_bin(), "-y",
            "-i", str(video),
            "-stream_loop", "-1", "-i", str(musica),
            "-filter_complex",
            f"[1:a]volume={ganho_db}dB[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(saida),
        ]
    )
    return saida


def gravar_legendas(video: Path, srt: Path, saida: Path, formato: Formato) -> Path:
    """Queima legendas no video (essencial em consumo mobile com som off)."""
    # Atencao: `force_style` do libass e interpretado sobre o PlayRes do script
    # (~288 de altura quando o SRT nao traz cabecalho ASS), NAO sobre os pixels
    # do video. Por isso os numeros abaixo sao pequenos: sao ~1/288 da altura.
    # Shorts sobe a legenda para escapar da UI do player; longo fica mais baixo.
    tamanho = 17 if formato is Formato.SHORTS else 13
    margem = 62 if formato is Formato.SHORTS else 28
    estilo = (
        f"FontName=DejaVu Sans,Fontsize={tamanho},Bold=1,"
        "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
        f"BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV={margem}"
    )
    caminho = str(srt).replace("\\", "/").replace(":", "\\:")
    _run(
        [
            ffmpeg_bin(), "-y",
            "-i", str(video),
            "-vf", f"subtitles='{caminho}':force_style='{estilo}'",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-c:a", "copy",
            str(saida),
        ]
    )
    return saida


def _codec_audio(saida: Path) -> str:
    """Container MP3 nao aceita AAC — o codec precisa seguir a extensao."""
    return "libmp3lame" if saida.suffix.lower() == ".mp3" else "aac"


def silencio(saida: Path, segundos: float) -> Path:
    """Audio silencioso — usado pelo TTS stub para a pipeline rodar offline."""
    saida.parent.mkdir(parents=True, exist_ok=True)
    _run(
        [
            ffmpeg_bin(), "-y",
            "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
            "-t", f"{segundos:.3f}",
            "-c:a", _codec_audio(saida), "-b:a", "192k",
            str(saida),
        ]
    )
    return saida
