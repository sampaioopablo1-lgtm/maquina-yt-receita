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
import json
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


def _linha(fonte: str, texto: str, cor: str, corpo: int, y: int, entrada: str, saida: str,
           janela: tuple[float, float] | None = None) -> str:
    """Uma linha do card. Com `janela`, ela so existe naquele intervalo — e assim
    que o card troca ao longo do video, que e o que separa a peca da referencia
    de um cartaz congelado."""
    ativa = f":enable='between(t,{janela[0]},{janela[1]})'" if janela else ""
    return (
        f"[{entrada}]drawtext=fontfile='{resolver_fonte(fonte)}':text='{_escapar(texto)}':"
        f"fontcolor={_cor(cor)}:fontsize={corpo}:x=(w-text_w)/2:y={y}{ativa}[{saida}]"
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
    return filtro_cards([{"setup": setup, "apoio": apoio, "chave": chave, "punch": punch}])


def e_retrato(bruto: str) -> bool:
    """A orientacao REAL do bruto, com a rotacao dos metadados ja aplicada.

    Gravacao de celular chega 1920x1080 com `rotation=90` — deitada no arquivo e
    em pe na tela. O ffprobe do stream, depois do corte, ja devolve 1080x1920.
    Ignorar isso foi o defeito que estragou a primeira entrega: o `pad` foi
    escrito para encaixar video deitado, recebeu um 9:16, nao coube, e o texto do
    card foi parar em cima do rosto em vez de sobre a faixa navy.
    """
    saida = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", bruto],
        capture_output=True, text=True, check=True).stdout.strip()
    largura, altura = (int(x) for x in saida.split(",")[:2])
    return altura >= largura


def filtro_cards(cards: list[dict], legenda: str | None = None, retrato: bool = False,
                 janela_fonte: int = 0) -> str:
    """O grafo inteiro: fundo, os cards em sequencia e a legenda queimada.

    Cada card e um dicionario com setup/apoio/chave/punch e, opcionalmente, `de`
    e `ate` em segundos. Sem `de`/`ate` o card vale o video inteiro — que e o
    caso de um card so, e foi exatamente o que deu errado na primeira versao.

    Sao dois layouts, e qual usar depende da orientacao do bruto:

    * bruto DEITADO — o video e reduzido e encaixado, e o `pad` cria a faixa
      navy ao redor dele;
    * bruto EM PE — nao ha o que encaixar (um 9:16 nao cabe dentro de outro).
      Recorta-se da fonte a janela que vai aparecer abaixo da faixa, e o `pad`
      de cima E a faixa. Onde essa janela comeca (`janela_fonte`) sai de
      `opc/enquadrar.py`, que mede o rosto: cobrir a cabeca com a faixa foi o
      defeito que estragou a entrega anterior.
    """
    k = estilo.chave()
    p, t, f, g = k["paleta"], k["tipografia"], k["formato"], k["geometria"]
    if retrato:
        # Bruto ja vertical: recorta da fonte EXATAMENTE a janela que aparece
        # abaixo da faixa, e o `pad` de cima vira a propria faixa navy. `janela`
        # e a linha da fonte onde essa janela comeca — e `opc/enquadrar.py` que
        # a calcula, a partir de onde o rosto esta.
        #
        # A versao que aumentava o quadro para depois cortar (pad para 2234px)
        # foi morta pelo OOM killer duas vezes: o sandbox tem 1 GB. Esta faz
        # uma alocacao so, do tamanho do quadro final.
        alto = f["altura"] - g["video_topo"]
        partes = [
            (f"[0:v]scale={f['largura']}:-2,crop={f['largura']}:{alto}:0:{max(0, janela_fonte)},"
             f"pad={f['largura']}:{f['altura']}:0:{g['video_topo']}:color={_cor(p['navy'])}[v0]")
        ]
    else:
        partes = [
            (f"[0:v]scale={g['video_largura']}:-2,"
             f"pad={f['largura']}:{f['altura']}:(ow-iw)/2:{g['video_topo']}:"
             f"color={_cor(p['navy'])}[v0]")
        ]
    rotulo = "v0"
    for i, card in enumerate(cards):
        janela = None
        if card.get("de") is not None and card.get("ate") is not None:
            janela = (card["de"], card["ate"])
        ativa = f":enable='between(t,{janela[0]},{janela[1]})'" if janela else ""
        for nivel, y in [("setup", g["y_setup"]), ("apoio", g["y_apoio"]),
                         ("chave", g["y_chave"]), ("punch", g["y_punch"])]:
            texto = card.get(nivel)
            if not texto:
                continue
            d = t[nivel]
            proximo = f"c{i}{nivel}"
            partes.append(_linha(d["fonte"], texto, d["cor"], d["corpo"], y,
                                 rotulo, proximo, janela))
            rotulo = proximo
        if card.get("punch"):
            proximo = f"c{i}regua"
            partes.append(
                f"[{rotulo}]drawbox=x=(iw-{g['regua_largura']})/2:y={g['y_regua']}:"
                f"w={g['regua_largura']}:h={g['regua_altura']}:color={_cor(p['laranja'])}:"
                f"t=fill{ativa}[{proximo}]")
            rotulo = proximo

    if legenda:
        # `fontsdir` e obrigatorio: o libass casa a fonte por NOME DE FAMILIA no
        # fontconfig, e as fontes da marca vivem em opc/fontes/, fora dele.
        caminho = legenda.replace("\\", "/").replace(":", r"\:")
        dir_fontes = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontes")
        partes.append(f"[{rotulo}]subtitles='{caminho}':fontsdir='{dir_fontes}'[out]")
    else:
        partes.append(f"[{rotulo}]null[out]")
    return ";".join(partes)


def comando(bruto: str, saida: str, setup: str = "", apoio: str = "", chave: str = "",
            punch: str = "", de: float | None = None, ate: float | None = None,
            cards: list[dict] | None = None, legenda: str | None = None,
            janela_fonte: int = 0) -> list[str]:
    """O argv do ffmpeg. Separado de quem executa para poder ser inspecionado e testado."""
    k = estilo.chave()
    if cards is None:
        cards = [{"setup": setup, "apoio": apoio, "chave": chave, "punch": punch}]
    cmd = ["ffmpeg", "-y"]
    if de is not None:
        cmd += ["-ss", str(de)]
    if ate is not None:
        cmd += ["-to", str(ate)]
    cmd += [
        "-i", bruto,
        "-filter_complex", filtro_cards(cards, legenda, e_retrato(bruto), janela_fonte),
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
    ap = argparse.ArgumentParser(description="Renderiza os cards da marca sobre um bruto")
    ap.add_argument("bruto")
    ap.add_argument("saida")
    ap.add_argument("--cards", help="JSON com a sequencia de cards [{de, ate, setup, ...}]")
    ap.add_argument("--legenda", help="arquivo .ass a queimar (opc/legenda.py gera)")
    ap.add_argument("--janela", type=int, default=0,
                    help="linha da fonte onde comeca a janela visivel (opc/enquadrar.py calcula)")
    ap.add_argument("--setup", default="")
    ap.add_argument("--apoio", default="")
    ap.add_argument("--chave", default="")
    ap.add_argument("--punch", default="")
    ap.add_argument("--de", type=float)
    ap.add_argument("--ate", type=float)
    a = ap.parse_args()

    if a.cards:
        with open(a.cards, encoding="utf-8") as fh:
            cards = json.load(fh)
    else:
        cards = [{"setup": a.setup, "apoio": a.apoio, "chave": a.chave, "punch": a.punch}]

    for c in cards:
        conferir_largura(c.get("setup", ""), c.get("apoio", ""),
                         c.get("chave", ""), c.get("punch", ""))

    cmd = comando(a.bruto, a.saida, de=a.de, ate=a.ate, cards=cards,
                  legenda=a.legenda, janela_fonte=a.janela)
    subprocess.run(cmd, check=True)
    print(f"{a.saida}: {conferir_duracao(a.saida):.1f}s, {len(cards)} card(s)"
          + (", com legenda queimada" if a.legenda else ""))


if __name__ == "__main__":
    main()
