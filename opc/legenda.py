#!/usr/bin/env python3
"""Legenda queimada palavra a palavra, no estilo que a marca usa.

Este arquivo existe por causa de um erro concreto: a primeira entrega do
pipeline em nuvem foi um card estatico por 33 segundos, e foi reprovada com
"ficou pior dos videos feito no Drift". Estava certo. Cor e fonte estavam
medidas; o que faltava era a peca se mexer junto com a fala.

DUAS DECISOES QUE PARECEM DETALHE E NAO SAO:

1. NAO uso a tag `\\k` do ASS. Ela e a tag de karaoke classico: a linha inteira
   aparece e o preenchimento varre as palavras. Isso e bom para musica e ruim
   para Reel. O que performa em vertical e um grupo curto na tela com a palavra
   corrente destacada — entao aqui cada palavra vira um EVENTO proprio que
   redesenha o grupo inteiro com uma cor diferente na palavra atual.

2. O contorno e grosso de proposito (6px). O Instagram reentrega o Reel em
   720x1280 a menos de 1 Mbps; contorno fino desaparece na recompressao e a
   legenda encosta no fundo. O arquivo que o espectador ve nao e o que sai daqui.

Uso:
    python3 opc/legenda.py transcricao.json legenda.ass
    # onde transcricao.json = [{"inicio": 0.14, "fim": 0.53, "palavra": "Em"}, ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import estilo  # noqa: E402


def _ass_cor(hexa: str) -> str:
    """`#RRGGBB` -> `&HAABBGGRR`. O ASS inverte a ordem dos canais e o alfa e
    invertido tambem (00 = opaco). Escrever isso errado nao quebra o render: so
    sai com a cor trocada, que e o defeito que passa despercebido."""
    h = hexa.lstrip("#")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}"


def _tempo(s: float) -> str:
    """Segundos -> `H:MM:SS.cc`. O ASS conta centesimos, nao milesimos."""
    cs = int(round(s * 100))
    h, resto = divmod(cs, 360000)
    m, resto = divmod(resto, 6000)
    seg, cs = divmod(resto, 100)
    return f"{h:d}:{m:02d}:{seg:02d}.{cs:02d}"


def _grupos(palavras: list[dict], por_grupo: int) -> list[list[dict]]:
    """Quebra a transcricao em grupos curtos.

    A quebra respeita pontuacao: uma palavra terminada em . ! ? , fecha o grupo
    mesmo antes do limite. Sem isso o grupo atravessa o fim da frase e a legenda
    passa a contradizer a respiracao de quem fala.
    """
    grupos, atual = [], []
    for p in palavras:
        atual.append(p)
        fim_de_frase = p["palavra"].strip().endswith((".", "!", "?", ",", ";", ":"))
        if len(atual) >= por_grupo or fim_de_frase:
            grupos.append(atual)
            atual = []
    if atual:
        grupos.append(atual)
    return grupos


def cabecalho() -> str:
    k = estilo.chave()
    f, l = k["formato"], k["legenda"]
    margem_v = int(f["altura"] * (1 - l["y"]))
    return "\n".join([
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {f['largura']}",
        f"PlayResY: {f['altura']}",
        # 0, nao 2. O WrapStyle 2 desliga a quebra automatica: com corpo 64 as
        # linhas cabiam por sorte, e com 100 um grupo de tres palavras longas
        # sairia pelas bordas sem nada reclamar. O 0 quebra sozinho e ainda
        # deixa a linha de cima mais larga, que e a forma da referencia.
        "WrapStyle: 0",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        ("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
         "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
         "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"),
        (f"Style: OPC,{l['familia']},{l['corpo']},{_ass_cor(l['cor'])},{_ass_cor(l['cor'])},"
         f"&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,{l['contorno']},{l['sombra']},"
         f"2,80,80,{margem_v},1"),
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ])


def eventos(palavras: list[dict]) -> list[str]:
    """Um evento por palavra: o grupo inteiro na tela, a palavra corrente em laranja."""
    k = estilo.chave()["legenda"]
    ativa = _ass_cor(k["cor_ativa"])
    linhas = []
    for grupo in _grupos(palavras, k["palavras_por_grupo"]):
        for i, p in enumerate(grupo):
            partes = []
            for j, q in enumerate(grupo):
                txt = q["palavra"].strip().upper()
                partes.append(f"{{\\c{ativa}}}{txt}{{\\c}}" if i == j else txt)
            # O "pop": a palavra entra 12% maior e assenta em 90ms. E o unico
            # movimento da legenda — mais que isso cansa em 30 segundos.
            corpo = "{\\fscx112\\fscy112\\t(0,90,\\fscx100\\fscy100)}" + " ".join(partes)
            linhas.append(
                f"Dialogue: 0,{_tempo(p['inicio'])},{_tempo(p['fim'])},OPC,,0,0,0,,{corpo}")
    return linhas


def gerar(palavras: list[dict]) -> str:
    return cabecalho() + "\n" + "\n".join(eventos(palavras)) + "\n"


def _seg(t: str) -> float:
    """`H:MM:SS.cc` -> segundos."""
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def recortar(ass: str, de: float, ate: float) -> str:
    """A mesma legenda, deslocada para uma janela que comeca em zero.

    Existe porque a legenda passou a ser queimada PLANO A PLANO, e nao sobre o
    video montado. O motivo e memoria: queimar sobre a peca inteira levou
    SIGKILL do OOM killer num sandbox de 1 GB (`total-vm:1133724kB`), enquanto
    cada plano de 5s cabe com folga. De quebra, cada quadro passa por um encode
    so em vez de dois — o texto sai mais limpo.

    Cada plano recebe um .ass proprio: os eventos que caem na janela, com os
    tempos recuados para o inicio dela. Sem o recuo, o evento de t=12s nao
    apareceria num plano que comeca a contar do zero.
    """
    cab, saida = [], []
    for linha in ass.splitlines():
        if not linha.startswith("Dialogue:"):
            cab.append(linha)
            continue
        campos = linha.split(",", 9)
        ini, fim = _seg(campos[1]), _seg(campos[2])
        if fim <= de or ini >= ate:
            continue
        campos[1] = _tempo(max(0.0, ini - de))
        campos[2] = _tempo(min(ate, fim) - de)
        saida.append(",".join(campos))
    return "\n".join(cab + saida) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="Gera a legenda ASS da marca")
    ap.add_argument("transcricao", help="JSON com [{inicio, fim, palavra}, ...]")
    ap.add_argument("saida", help="arquivo .ass de saida")
    a = ap.parse_args()
    with open(a.transcricao, encoding="utf-8") as fh:
        palavras = json.load(fh)
    with open(a.saida, "w", encoding="utf-8") as fh:
        fh.write(gerar(palavras))
    print(f"{a.saida}: {len(palavras)} palavras em {len(_grupos(palavras, estilo.chave()['legenda']['palavras_por_grupo']))} grupos")


if __name__ == "__main__":
    main()
