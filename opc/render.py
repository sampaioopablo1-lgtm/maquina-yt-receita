#!/usr/bin/env python3
"""Monta o card da marca em cima de um bruto — lendo a chave, nunca redigitando.

Este modulo nao tem nenhuma cor, nenhum corpo de fonte e nenhuma coordenada
propria. Tudo vem de `opc/estilo.py`. Se voce encontrar um `#FF7A1B` escrito
aqui, e um defeito: significa que a marca passou a ter duas verdades de novo.

A fonte e resolvida por BUSCA, nao por caminho fixo, porque o render roda em tres
lugares diferentes (sandbox, runner, maquina do Pablo) e um caminho absoluto
quebra em dois deles. Quando a fonte da marca nao existe, o render NAO cai
silenciosamente numa fonte parecida: ele avisa qual faltou. Card com a fonte
errada passa despercebido no terminal e nao passa no feed.

Uso:
    python3 opc/render.py BRUTO.mov SAIDA.mp4 \\
        --setup "R$ 10 MIL DE ALUGUEL" --apoio "VOCE PAGA SEM PENSAR." \\
        --chave "anunciar" --punch "VOCE ACHA CARO." --de 12.5 --ate 46.0
"""
from __future__ import annotations

import argparse
import glob
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import estilo  # noqa: E402

# Onde procurar as fontes da marca, em ordem. O primeiro hit vence.
DIRS_FONTE = [
    os.path.expanduser("~/.fonts"),
    "/usr/share/fonts",
    "/usr/local/share/fonts",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontes"),
]


def resolver_fonte(nome: str) -> str:
    """Acha o .ttf da fonte pedida. Levanta se nao achar — nunca substitui calado."""
    for d in DIRS_FONTE:
        for caminho in glob.glob(os.path.join(d, "**", f"{nome}.ttf"), recursive=True):
            return caminho
    raise FileNotFoundError(
        f"fonte '{nome}.ttf' nao encontrada em {DIRS_FONTE}. "
        "Instale a fonte da marca — cair numa fonte parecida descaracteriza o card."
    )


def _escapar(texto: str) -> str:
    """Escapa o que o drawtext do ffmpeg trata como sintaxe."""
    for de, para in [("\\", r"\\"), (":", r"\:"), ("'", r"\'"), ("%", r"\%")]:
        texto = texto.replace(de, para)
    return texto


def _cor(hexa: str) -> str:
    """`#RRGGBB` -> `0xRRGGBB`. O ffmpeg aceita os dois, mas o `#` e o caractere
    de comentario de varios shells e ja se perdeu tempo com isso."""
    return hexa.replace("#", "0x")


def conferir_largura(setup: str, apoio: str, chave: str, punch: str) -> None:
    """Recusa linha que estoura a caixa ANTES de gastar minutos de render.

    Uma linha larga demais nao quebra o ffmpeg: ela sai cortada nas bordas, e
    isso so aparece quando alguem olha o mp4 pronto. Medir antes custa
    milissegundos. A margem de 60px de cada lado e a do card publicado.
    """
    try:
        from PIL import ImageFont
    except ImportError:
        print("AVISO: Pillow ausente, largura das linhas nao conferida", file=sys.stderr)
        return
    k = estilo.chave()
    limite = k["formato"]["largura"] - 120
    for nivel, texto in [("setup", setup), ("apoio", apoio), ("chave", chave), ("punch", punch)]:
        d = k["tipografia"][nivel]
        fonte = ImageFont.truetype(resolver_fonte(d["fonte"]), d["corpo"])
        largura = fonte.getbbox(texto)[2]
        if largura > limite:
            raise ValueError(
                f"a linha '{nivel}' tem {largura}px e o limite e {limite}px: "
                f"encurte o texto ou ela sai cortada no card. ({texto!r})")


def _linha(fonte: str, texto: str, cor: str, corpo: int, y: int, entrada: str, saida: str) -> str:
    return (
        f"[{entrada}]drawtext=fontfile='{resolver_fonte(fonte)}':text='{_escapar(texto)}':"
        f"fontcolor={_cor(cor)}:fontsize={corpo}:x=(w-text_w)/2:y={y}[{saida}]"
    )


def filtro(setup: str, apoio: str, chave: str, punch: str) -> str:
    """O grafo de filtros do card, montado a partir da chave de estilo.

    O fundo navy vem de um `pad` sobre o proprio video, e NAO de uma fonte
    `color` combinada por `overlay`. A versao com `color` foi morta pelo OOM
    killer na primeira execucao: fonte sintetica nao tem fim, entao ela produz
    quadros mais rapido do que o overlay consome e o buffer cresce ate o
    processo levar SIGKILL. O `pad` nao tem esse modo de falha porque nao existe
    segunda entrada — e ainda economiza uma composicao por quadro.
    """
    k = estilo.chave()
    p, t, f, g = k["paleta"], k["tipografia"], k["formato"], k["geometria"]
    partes = [
        (f"[0:v]scale={g['video_largura']}:-2,"
         f"pad={f['largura']}:{f['altura']}:(ow-iw)/2:{g['video_topo']}:"
         f"color={_cor(p['navy'])}[base]"),
        _linha(t["setup"]["fonte"], setup, t["setup"]["cor"], t["setup"]["corpo"], g["y_setup"], "base", "l1"),
        _linha(t["apoio"]["fonte"], apoio, t["apoio"]["cor"], t["apoio"]["corpo"], g["y_apoio"], "l1", "l2"),
        _linha(t["chave"]["fonte"], chave, t["chave"]["cor"], t["chave"]["corpo"], g["y_chave"], "l2", "l3"),
        _linha(t["punch"]["fonte"], punch, t["punch"]["cor"], t["punch"]["corpo"], g["y_punch"], "l3", "l4"),
        (f"[l4]drawbox=x=(iw-{g['regua_largura']})/2:y={g['y_regua']}:"
         f"w={g['regua_largura']}:h={g['regua_altura']}:color={p['laranja']}:t=fill[out]"),
    ]
    return ";".join(partes)


def comando(bruto: str, saida: str, setup: str, apoio: str, chave: str, punch: str,
            de: float | None = None, ate: float | None = None) -> list[str]:
    """O argv do ffmpeg. Separado de quem executa para poder ser inspecionado e testado."""
    k = estilo.chave()
    cmd = ["ffmpeg", "-y"]
    if de is not None:
        cmd += ["-ss", str(de)]
    if ate is not None:
        cmd += ["-to", str(ate)]
    cmd += [
        "-i", bruto,
        "-filter_complex", filtro(setup, apoio, chave, punch),
        "-map", "[out]", "-map", "0:a?",
        "-r", str(k["formato"]["fps"]),
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
        saida,
    ]
    return cmd


def conferir_duracao(saida: str) -> float:
    """A duracao entregue tem de cair na faixa medida nos Reels no ar."""
    k = estilo.chave()["formato"]
    d = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", saida],
        capture_output=True, text=True, check=True).stdout.strip())
    if not (k["dur_min_s"] <= d <= k["dur_max_s"]):
        print(f"AVISO: {d:.1f}s esta fora da faixa {k['dur_min_s']}-{k['dur_max_s']}s da marca",
              file=sys.stderr)
    return d


def main() -> None:
    ap = argparse.ArgumentParser(description="Renderiza o card da marca sobre um bruto")
    ap.add_argument("bruto")
    ap.add_argument("saida")
    ap.add_argument("--setup", required=True)
    ap.add_argument("--apoio", required=True)
    ap.add_argument("--chave", required=True)
    ap.add_argument("--punch", required=True)
    ap.add_argument("--de", type=float)
    ap.add_argument("--ate", type=float)
    a = ap.parse_args()
    conferir_largura(a.setup, a.apoio, a.chave, a.punch)
    cmd = comando(a.bruto, a.saida, a.setup, a.apoio, a.chave, a.punch, a.de, a.ate)
    subprocess.run(cmd, check=True)
    print(f"{a.saida}: {conferir_duracao(a.saida):.1f}s")


if __name__ == "__main__":
    main()
