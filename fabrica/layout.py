#!/usr/bin/env python3
"""Confere o enquadramento de cada cena ANTES do render.

O `visual.py` ja media tinta na borda, mas so no video PRONTO e amostrando 12
quadros. Custo de descobrir um texto estourado: 17 minutos de render e uma vaga
de publicacao. Medido em 13/08/2026, run 31659140900: o nivel-do-jogo-002
reprovou em t=250,1s com 1,2% de tinta na borda, depois de renderizar os 51
clipes e a trilha. A cena era a 14 — dois rotulos de barra com frase inteira
onde cabe rotulo de eixo.

E amostragem de 12 quadros num video de 51 cenas ve UMA cena em quatro: o
defeito pode passar. Aqui cada cena e rasterizada sozinha, sem TTS e sem
ffmpeg, e TODAS entram na conta. Roda em segundos.

Uso:
    python3 fabrica/layout.py <spec.json>
"""
from __future__ import annotations

import io
import json
import os
import sys
import types

# fabrica.py importa edge_tts (rede) so para narrar; aqui e SVG puro.
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cairosvg  # noqa: E402
from PIL import Image  # noqa: E402

import fabrica as F  # noqa: E402

# O LIMITE era o mesmo do visual.py; a REGUA nao era, e por isso este portao
# aprovava o que o outro reprovava.
#
# `MARGEM_PX = 12` olhava os doze pixels extremos — 1,7% da altura em 1280x720.
# O visual.py mede 4%, e mede no video EM MOVIMENTO. Entre os dois esta o Ken
# Burns: com AMP_ZOOM 0,12 e AMP_PAN 0,5, o zoom corta ate 8,04% de um dos lados.
# Texto a 20 pixels da borda esta fora dos doze extremos (passa aqui) e dentro do
# quadro que o zoom empurra para fora (reprova la).
#
# MEDIDO em 17/08/2026 no seja-mais-magra-002: sete portoes verdes, 0 erros em 80
# cenas aqui, e o video reprovado em t=162,8s com 2,18% de tinta na borda, depois
# de nove minutos de render. Refazendo a conta com a faixa abaixo, as QUATRO
# cenas acima do limite eram as quatro de layout `barras` — o layout desenha o
# rotulo em y=0,90H — e nenhuma das outras 71.
#
# A faixa sai dos parametros REAIS do movimento, e nao de um numero escolhido:
# se alguem mexer em AMP_ZOOM ou AMP_PAN, esta conta acompanha.
MARGEM_VISUAL = 0.04     # a mesma faixa que o visual.py chama de borda
LIMITE_PCT = 1.0
TOLERA_COR = 40   # distancia RGB que conta como "diferente do fundo"


def corte_do_ken_burns() -> float:
    """Fracao maxima de um lado que o zoom+pan tira do quadro.

    O zoom deixa visivel 1/(1+AMP_ZOOM) da imagem, entao sobra
    1 - 1/(1+AMP_ZOOM) de margem. O pan distribui essa margem entre os dois
    lados e percorre AMP_PAN dela, indo de (1-AMP_PAN)/2 a (1+AMP_PAN)/2 — logo
    o pior lado leva (0,5 + AMP_PAN/2) do total.
    """
    margem = 1 - 1 / (1 + F.AMP_ZOOM)
    return margem * (0.5 + F.AMP_PAN / 2)


def faixa_de_risco() -> float:
    """O que o zoom corta MAIS o que o visual.py ainda chama de borda."""
    return corte_do_ken_burns() + MARGEM_VISUAL


def _borda(im, fundo, largura: int, altura: int) -> float:
    """% de pixels diferentes do fundo na faixa que o visual.py chama de borda."""
    mx, my = max(int(largura * MARGEM_VISUAL), 1), max(int(altura * MARGEM_VISUAL), 1)
    pontos = [(x, y) for x in range(largura)
              for y in list(range(my)) + list(range(altura - my, altura))]
    pontos += [(x, y) for y in range(my, altura - my)
               for x in list(range(mx)) + list(range(largura - mx, largura))]
    fora = sum(
        1 for p in pontos
        if sum(abs(a - b) for a, b in zip(im.getpixel(p), fundo)) > TOLERA_COR
    )
    return 100.0 * fora / len(pontos)


def _janelas(largura: int, altura: int, i: int):
    """Os recortes EXTREMOS que o Ken Burns da cena `i` vai mostrar.

    Nao adianta medir a borda do quadro parado: o clipe nunca mostra o quadro
    parado. O zoom deixa visivel 1/z da imagem e o pan escolhe ONDE. Como
    `ken_burns` alterna quatro movimentos por indice, da para reproduzir aqui
    exatamente o par de extremos daquela cena — e e neles que o texto encosta.
    """
    z = 1 + F.AMP_ZOOM
    lv, av = largura / z, altura / z          # o que cabe na tela no zoom cheio
    mx, my = largura - lv, altura - av        # margem que o zoom abriu
    ini, fim = (1 - F.AMP_PAN) / 2, (1 + F.AMP_PAN) / 2
    horizontal = i % 4 in (0, 1)
    fx = (ini, fim) if horizontal else (0.5, 0.5)
    fy = (0.5, 0.5) if horizontal else (ini, fim)
    return [(int(mx * a), int(my * b), int(mx * a + lv), int(my * b + av))
            for a, b in zip(fx, fy)]


def tinta_na_borda(svg: str, largura: int, altura: int, i: int = 0) -> float:
    """A PIOR borda entre os enquadramentos que a cena vai mostrar de fato.

    Mede o que o visual.py mediria, sem render: recorta a janela do zoom nos
    extremos do pan e olha a faixa de 4% de cada recorte.
    """
    png = cairosvg.svg2png(
        bytestring=svg.encode(), output_width=largura, output_height=altura
    )
    im = Image.open(io.BytesIO(png)).convert("RGB")
    fundo = im.getpixel((2, 2))
    return max(_borda(im.crop(j), fundo, j[2] - j[0], j[3] - j[1])
               for j in _janelas(largura, altura, i))


# A moldura da thumbnail tem 40 px de cor CHAPADA, e cor chapada e escura em
# tons de cinza. Amostrar a largura inteira faz toda linha de 0 a 719 parecer
# ter tinta, e ai o portao reprova as dezenove specs — inclusive as boas.
# Aconteceu comigo na primeira versao. A janela de amostra fica dentro da
# caixa branca, com folga.
FOLGA = 22


def _faixa_de_tinta(svg: str, largura: int, altura: int,
                    caixa: int = 40) -> tuple[int, int] | None:
    """Primeira e ultima linha com tinta DENTRO da caixa branca.

    None quando nao ha texto — que e o caso proposital ao renderizar uma linha
    de cada vez para comparar as faixas.
    """
    png = cairosvg.svg2png(bytestring=svg.encode(),
                           output_width=largura, output_height=altura)
    im = Image.open(io.BytesIO(png)).convert("L")
    x0, x1 = caixa + FOLGA, largura - caixa - FOLGA
    y0, y1 = caixa + FOLGA, altura - caixa - FOLGA
    linhas = [y for y in range(y0, y1)
              if min(im.getpixel((x, y)) for x in range(x0, x1, 4)) < 140]
    return (linhas[0], linhas[-1]) if linhas else None


def analisa_thumb(spec: dict) -> list[str]:
    """A thumbnail e a unica imagem que decide o clique, e nao passava por
    portao nenhum: o layout mede as CENAS, o visual amostra o VIDEO.

    Medido em 13/08/2026: com posicao fixa (l1 em y=300 corpo 150, l2 em
    y=480), toda thumbnail cujo titulo quebrasse em duas linhas saia com os
    dois textos empilhados um sobre o outro. Estava assim em TODO pacote com
    titulo longo — sx-educacao-001 e nivel-do-jogo-002 entre eles.

    Tinta na borda nao pegaria isso: a colisao acontece no meio da imagem. Por
    isso o teste renderiza cada linha SOZINHA e compara a faixa vertical que
    cada uma ocupa. Sobreposicao de faixa e sobreposicao de texto.
    """
    th, pal = spec.get("thumb"), spec["paleta"]
    if not th:
        return ["spec sem `thumb` — o video subiria sem capa e o CTR morre"]

    W, H = 1280, 720
    F.usar_fonte(spec.get("fonte", ""))
    erros = []

    g = F.geometria_thumb(th, H)
    if g["linhas1"] and g["linhas2"] and g["base1"] > g["topo2"]:
        erros.append(
            f"thumbnail: as duas linhas se sobrepoem — o titulo termina em "
            f"{g['base1']:.0f} e o subtitulo comeca em {g['topo2']:.0f}. "
            f"l1={th['l1']!r} l2={th['l2']!r}"
        )

    # A moldura colorida tem 40 px; texto invadindo ela some no player. Aqui a
    # medida e do PIXEL, e nao da conta: o wrap pode estourar a largura mesmo
    # com a altura certa, e so a rasterizacao mostra isso.
    # LARGURA. Medida pela conta, e nao pelo pixel, por um motivo que so
    # aparece olhando a capa: `l2` e desenhado em `c1`, a MESMA cor da moldura.
    # Uma linha que transborda nao sai cortada — sai INVISIVEL, verde sobre
    # verde, e qualquer varredura por luminancia a confunde com a moldura.
    # Medido em 18/08/2026 no setiap-level-007: 'BERAPA LAMA?' calculado em
    # 1.101 px pela constante 0,62 e renderizado com 1.251, com as duas pontas
    # dentro da moldura. O portao aprovava, porque so olhava a faixa vertical.
    util = W - 2 * g["margem"]
    for rotulo, linhas, corpo in (("titulo", g["l1"], g["s1"]),
                                  ("subtitulo", g["l2"], g["s2"])):
        for linha in linhas:
            larg = F.largura_do_texto(linha, corpo)
            if larg > util:
                erros.append(
                    f"thumbnail: {rotulo} {linha!r} tem {larg:.0f} px no corpo "
                    f"{corpo} e a caixa branca so tem {util} px — a sobra cai "
                    f"na moldura, e em `c1` ela some em vez de aparecer cortada"
                )

    juntos = _faixa_de_tinta(F.svg_thumb(th, pal), W, H)
    if juntos is None:
        erros.append("thumbnail: nenhuma tinta dentro da caixa — capa em branco")
    elif juntos[0] < 40 or juntos[1] > H - 40:
        erros.append(
            f"thumbnail: texto fora da caixa branca (tinta de {juntos[0]} a "
            f"{juntos[1]}, caixa de 40 a {H - 40})"
        )
    return erros


def analisa(spec: dict) -> list[str]:
    pal = spec["paleta"]
    F.usar_fonte(spec.get("fonte", ""))
    erros = []
    for bloco, (W, H) in (("longo", (1280, 720)), ("short", (1080, 1920))):
        for i, cena in enumerate(spec.get(bloco) or []):
            pct = tinta_na_borda(F.svg_cena(cena, pal, W, H), W, H, i)
            if pct >= LIMITE_PCT:
                erros.append(
                    f"{bloco} cena {i:02d} ({cena.get('layout')}): {pct:.2f}% de tinta "
                    f"na borda — texto cortado ou encostando. "
                    f"kicker={cena.get('kicker','')!r} itens={cena.get('itens')}"
                )
    return erros


def main() -> int:
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    erros = analisa(spec)
    for e in erros:
        print("  ERRO  ", e)
    total = len(spec.get("longo") or []) + len(spec.get("short") or [])
    print(f"  -> {len(erros)} erro(s) em {total} cenas")
    return 1 if erros else 0


if __name__ == "__main__":
    raise SystemExit(main())
