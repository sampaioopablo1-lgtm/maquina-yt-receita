"""Montagem final do video e da thumbnail."""

from __future__ import annotations

import logging
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .. import media
from ..models import Formato, Roteiro
from ..providers.base import GeradorImagem

log = logging.getLogger("maquina.render")

TRILHA_PADRAO = Path("assets/musica/trilha.mp3")


def montar(
    roteiro: Roteiro,
    destino: Path,
    formato: Formato,
    *,
    legendas: Path | None = None,
    trilha: Path | None = None,
) -> tuple[Path, float]:
    """Compoe as cenas em um MP4 pronto para upload. Devolve (caminho, duracao)."""
    clipes_dir = destino / "clipes"
    clipes_dir.mkdir(parents=True, exist_ok=True)

    clipes: list[Path] = []
    for cena in roteiro.cenas:
        if not (cena.audio_path and cena.imagem_path):
            raise ValueError(f"cena {cena.indice} sem audio ou imagem")

        clipe = clipes_dir / f"cena_{cena.indice:03d}.mp4"
        if not clipe.exists():
            # Alterna a intensidade do zoom por cena: variacao visual e o que
            # separa "edicao" de "template automatico".
            zoom = 0.16 if cena.indice % 2 == 0 else 0.09
            media.clipe_de_imagem(
                Path(cena.imagem_path), Path(cena.audio_path), clipe, formato, zoom=zoom
            )
        clipes.append(clipe)
        log.info("clipe %d/%d montado", cena.indice + 1, len(roteiro.cenas))

    atual = media.concatenar(clipes, destino / "bruto.mp4")

    trilha_path = trilha or TRILHA_PADRAO
    if trilha_path.exists():
        atual = media.aplicar_trilha(atual, trilha_path, destino / "com_trilha.mp4")
    else:
        log.info("sem trilha de fundo (%s nao encontrado)", trilha_path)

    if legendas and legendas.exists():
        atual = media.gravar_legendas(atual, legendas, destino / "com_legenda.mp4", formato)

    final = destino / "final.mp4"
    final.unlink(missing_ok=True)
    atual.rename(final)

    dur = media.duracao(final)
    log.info("video final: %s (%.1fs)", final, dur)
    return final, dur


def montar_thumbnail(
    gerador: GeradorImagem, roteiro: Roteiro, destino: Path
) -> Path:
    """Thumbnail no padrao validado: imagem de fundo + texto curto no topo.

    Ver docs/02-playbook-youtube.md — texto de ate 3 palavras, alto contraste,
    legivel em tela de celular.
    """
    largura, altura = 1280, 720
    fundo = destino / "thumb_fundo.png"
    if not fundo.exists():
        prompt = roteiro.prompt_thumbnail or f"cinematic background for: {roteiro.titulo}"
        gerador.gerar(prompt, fundo, largura=largura, altura=altura)

    img = Image.open(fundo).convert("RGB").resize((largura, altura), Image.LANCZOS)

    # Escurece o topo para o texto ter contraste garantido sobre qualquer imagem.
    faixa = Image.new("L", (largura, altura), 0)
    ImageDraw.Draw(faixa).rectangle([0, 0, largura, int(altura * 0.42)], fill=190)
    faixa = faixa.filter(ImageFilter.GaussianBlur(40))
    img = Image.composite(Image.new("RGB", img.size, (0, 0, 0)), img, faixa)

    texto = " ".join((roteiro.texto_thumbnail or roteiro.titulo).split()[:3]).upper()
    d = ImageDraw.Draw(img)
    tamanho = 120
    fonte = None
    caminhos = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    while tamanho > 40:
        for c in caminhos:
            try:
                fonte = ImageFont.truetype(c, tamanho)
                break
            except OSError:
                continue
        if fonte is None:
            fonte = ImageFont.load_default()
            break
        if d.textlength(texto, font=fonte) <= largura * 0.9:
            break
        tamanho -= 6

    linhas = textwrap.wrap(texto, width=18) or [texto]
    y = int(altura * 0.10)
    for linha in linhas:
        d.text(
            (largura // 2, y),
            linha,
            font=fonte,
            fill=(255, 255, 255),
            anchor="ma",
            stroke_width=8,
            stroke_fill=(0, 0, 0),
        )
        y += tamanho + 10

    saida = destino / "thumbnail.jpg"
    # Limite do YouTube e 2 MB.
    for qualidade in (92, 85, 75, 65):
        img.save(saida, "JPEG", quality=qualidade, optimize=True)
        if saida.stat().st_size < 2_000_000:
            break
    return saida
