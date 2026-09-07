#!/usr/bin/env python3
"""Onde o rosto esta no bruto, e quanto o video precisa descer.

Existe por causa de um defeito que foi ao ar: a primeira entrega saiu com a
cabeca cortada. A faixa navy do card ocupa o topo do quadro; o bruto do celular
tem o rosto comecando em 0.201 da altura; a faixa vai ate 0.344. Ou seja, ela
passava por cima dos 274px de cima da cabeca — e nada reclamava, porque cor,
duracao e ate o OCR do card continuavam certos.

A licao esta na medida que pega isso: o detector de rosto achou rosto em 1 de 12
quadros do render e em 12 de 12 do bruto. Essa queda e o sintoma; e ela que este
modulo transforma em numero antes do render, em vez de depois.

O alvo (`estilo.ROSTO_TOPO_ALVO`) saiu do Reel r1, o mais apertado dos tres no
ar: rosto comecando logo abaixo da faixa. Os outros dois sao mais folgados;
usar o apertado mantem o rosto o maior possivel sem encostar.

Uso:
    python3 opc/enquadrar.py BRUTO.mp4          # imprime o deslocamento
    python3 opc/enquadrar.py BRUTO.mp4 --json   # para encadear no render
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import estilo  # noqa: E402


def _duracao(video: str) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", video],
        capture_output=True, text=True, check=True).stdout.strip())


def medir_rosto(video: str, amostras: int = 10) -> tuple[float | None, int, int]:
    """Mediana da posicao do topo do rosto, em fracao da altura do quadro.

    Devolve tambem em quantos quadros houve deteccao: essa razao e o alarme.
    Cair de 12/12 para 1/12 entre o bruto e o render significa que alguma coisa
    passou por cima do rosto.
    """
    try:
        import cv2
    except ImportError:
        raise SystemExit("opencv ausente: pip install 'opencv-python-headless<5'")

    cascata = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if cascata.empty():
        raise SystemExit("cascata de rosto nao carregou")

    duracao = _duracao(video)
    topos = []
    for i in range(amostras):
        t = duracao * (i + 0.5) / amostras
        quadro = f"/tmp/opc_enq_{os.getpid()}_{i}.png"
        subprocess.run(["ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", video,
                        "-frames:v", "1", "-update", "1", quadro, "-loglevel", "error"],
                       check=True)
        imagem = cv2.imread(quadro)
        os.unlink(quadro)
        if imagem is None:
            continue
        altura, largura = imagem.shape[:2]
        achados = cascata.detectMultiScale(
            cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY), 1.15, 6,
            minSize=(int(largura * 0.10), int(largura * 0.10)))
        if len(achados):
            x, y, w, h = max(achados, key=lambda r: r[2] * r[3])
            topos.append(y / altura)
    if not topos:
        return None, 0, amostras
    return statistics.median(topos), len(topos), amostras


def janela(video: str) -> tuple[int, float, int, int]:
    """Em que linha da FONTE comeca a janela que aparece abaixo da faixa navy.

    E esse numero que o `render.py` consome. A conta e direta: para o rosto, que
    esta em `rosto_topo_px` na fonte, aparecer em `alvo_px` no quadro final, e
    sabendo que a janela visivel comeca em `video_topo` do quadro final —

        janela = rosto_topo_px - (alvo_px - video_topo)

    Grampeado em zero: se o rosto ja esta alto na fonte nao ha de onde tirar
    imagem acima dele, e insistir so geraria borda preta.
    """
    k = estilo.chave()
    topo, n, total = medir_rosto(video)
    if topo is None:
        raise SystemExit(f"nenhum rosto detectado em {total} quadros de {video} — "
                         "se o bruto nao e talking head, passe --janela 0 no render")
    altura = k["formato"]["altura"]
    alvo_px = k["geometria"]["rosto_topo_alvo"] * altura
    corte = int(round(topo * altura - (alvo_px - k["geometria"]["video_topo"])))
    return max(0, corte), topo, n, total


def main() -> None:
    ap = argparse.ArgumentParser(description="Mede o rosto e diz onde comeca a janela visivel")
    ap.add_argument("bruto")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    corte, topo, n, total = janela(a.bruto)
    k = estilo.chave()
    if a.json:
        print(json.dumps({"janela": corte, "rosto_topo": round(topo, 3),
                          "deteccoes": n, "amostras": total}))
        return
    altura = k["formato"]["altura"]
    print(f"rosto no bruto: topo em {topo:.3f} ({int(topo * altura)}px de {altura}), "
          f"detectado em {n}/{total} quadros")
    print(f"alvo da marca:  {k['geometria']['rosto_topo_alvo']} "
          f"({int(k['geometria']['rosto_topo_alvo'] * altura)}px)")
    print(f"janela comeca em: {corte}px da fonte")
    print(f"\n  python3 opc/render.py {a.bruto} SAIDA.mp4 --cards cards.json "
          f"--legenda legenda.ass --janela {corte}")
    if n < total * 0.6:
        print(f"\nAVISO: rosto detectado em so {n} de {total} quadros. Confira o bruto: "
              "esse numero cai quando alguma coisa cobre a cabeca.")


if __name__ == "__main__":
    main()
