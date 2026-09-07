#!/usr/bin/env python3
"""Corta o bruto PELO TEXTO, em uma ou mais janelas, e remapeia a transcricao.

POR QUE MAIS DE UMA JANELA. A gravacao real quase nunca tem os 30 segundos bons
em sequencia. No bruto que motivou este arquivo (IMG_2318), a tese da peca esta
entre 10s e 21s e o fechamento entre 29s e 51s — e no meio, entre 21s e 24s, o
locutor diz "clica nesse video", que e exatamente a geracao de CTA que
`opc/estilo.py` marca como PROIBIDA (`LEGENDA_PROIBIDA`), porque foi substituida.

Com janela unica so havia duas saidas: entregar 22s (abaixo do minimo de 28s da
marca) ou deixar entrar o CTA velho. Cortar em duas janelas resolve as duas.

COMO SE ENCAIXA NO RESTO. Este modulo produz UM arquivo continuo, com video e
audio ja emendados, e uma transcricao com os tempos recalculados para a linha do
tempo nova. Dai para a frente `opc/montagem.py` nao sabe que houve corte — ele
recebe um bruto normal. Foi de proposito: a alternativa, ensinar a montagem a
lidar com varias janelas, espalharia a conversao de tempo por todo o codigo, e
conversao de tempo espalhada e onde os erros de um quadro se escondem.

O corte e re-CODIFICADO, e nao copiado. Copia so corta em quadro-chave, entao a
emenda cairia ate um segundo longe de onde a frase termina — e o que se ouviria
seria a silaba seguinte grudada na anterior.

Uso:
    python3 opc/cortar.py BRUTO.MOV cortado.mp4 --janelas 10.0-21.2 28.9-51.6 \\
        --transcricao transc.json --transcricao-saida transc_cortada.json
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess

# Mesmo motivo de `opc/montagem.py`: no sandbox /tmp e tmpfs, ou seja memoria.
TRABALHO_PADRAO = os.environ.get("OPC_TRABALHO", os.path.expanduser("~/opc_planos"))


def janela(texto: str) -> tuple[float, float]:
    """`10.0-21.2` -> (10.0, 21.2)."""
    de, ate = texto.split("-", 1)
    de, ate = float(de), float(ate)
    if ate <= de:
        raise ValueError(f"janela invalida: {texto!r} (o fim tem de ser depois do inicio)")
    return de, ate


def remapear(palavras: list[dict], janelas: list[tuple[float, float]]) -> list[dict]:
    """A transcricao na linha do tempo do arquivo cortado.

    Uma palavra que cai fora de todas as janelas SOME — ela nao vai ser dita no
    arquivo novo. Uma palavra que atravessa a borda e cortada na borda: deixar
    passar faria a legenda continuar na tela depois que o audio dela ja acabou.
    """
    fora, deslocamento = [], 0.0
    for de, ate in janelas:
        for p in palavras:
            if p["fim"] <= de or p["inicio"] >= ate:
                continue
            ini = max(p["inicio"], de) - de + deslocamento
            fim = min(p["fim"], ate) - de + deslocamento
            fora.append({"inicio": round(ini, 2), "fim": round(fim, 2),
                         "palavra": p["palavra"]})
        deslocamento += ate - de
    return fora


def cortar(bruto: str, saida: str, janelas: list[tuple[float, float]],
           trabalho: str = TRABALHO_PADRAO) -> float:
    """Emenda as janelas num arquivo so. Devolve a duracao total."""
    os.makedirs(trabalho, exist_ok=True)
    pedacos = []
    for i, (de, ate) in enumerate(janelas):
        alvo = os.path.join(trabalho, f"corte{i:02d}.mp4")
        # `-ss` antes do `-i` para o ffmpeg buscar rapido, mas com re-encode
        # para o corte cair no quadro pedido e nao no quadro-chave anterior.
        # `-map 0:v:0 -map 0:a:0` sem interrogacao: bruto sem audio tem de
        # falhar aqui, e nao virar um Reel mudo tres passos adiante.
        r = subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{de:.3f}", "-to", f"{ate:.3f}", "-i", bruto,
             "-map", "0:v:0", "-map", "0:a:0",
             "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
             "-pix_fmt", "yuv420p", "-threads", "1",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
             "-avoid_negative_ts", "make_zero", alvo],
            capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f"janela {de}-{ate}s falhou:\n{r.stderr[-1200:]}")
        pedacos.append(alvo)

    lista = os.path.join(trabalho, "cortes.txt")
    with open(lista, "w", encoding="utf-8") as fh:
        for p in pedacos:
            fh.write(f"file '{os.path.abspath(p)}'\n")
    r = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lista,
                        "-c", "copy", saida], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"emenda falhou:\n{r.stderr[-1200:]}")
    return sum(ate - de for de, ate in janelas)


def main() -> None:
    ap = argparse.ArgumentParser(description="Corta o bruto pelo texto")
    ap.add_argument("bruto")
    ap.add_argument("saida")
    ap.add_argument("--janelas", nargs="+", required=True,
                    help="uma ou mais, no formato inicio-fim em segundos")
    ap.add_argument("--transcricao")
    ap.add_argument("--transcricao-saida")
    ap.add_argument("--trabalho", default=TRABALHO_PADRAO)
    a = ap.parse_args()

    js = [janela(t) for t in a.janelas]
    dur = cortar(a.bruto, a.saida, js, a.trabalho)
    print(f"{a.saida}: {dur:.1f}s de {len(js)} janela(s)")

    if a.transcricao and a.transcricao_saida:
        with open(a.transcricao, encoding="utf-8") as fh:
            palavras = json.load(fh)
        novo = remapear(palavras, js)
        with open(a.transcricao_saida, "w", encoding="utf-8") as fh:
            json.dump(novo, fh, ensure_ascii=False, indent=0)
        print(f"{a.transcricao_saida}: {len(novo)} de {len(palavras)} palavras")


if __name__ == "__main__":
    main()
