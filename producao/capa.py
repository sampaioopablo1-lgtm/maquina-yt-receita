# -*- coding: utf-8 -*-
"""Capa do Reel: um quadro do proprio video, escolhido pelo rosto mais aberto.

Nao vale pegar o frame 0 -- e sempre ele comecando a abrir a boca. Varre o
primeiro plano de rosto e fica com o quadro mais nitido (variancia do laplaciano),
que na pratica e aquele em que ele esta parado e falando, nao piscando.
"""
import subprocess, sys, os
import numpy as np
from PIL import Image

FF = "/usr/local/bin/ffmpeg"


def capa(mp4, saida, ini=0.6, fim=4.0, passo=0.2):
    import cv2
    olhos = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    melhor, mq, aberto = None, -1, False
    t = ini
    while t <= fim:
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", "%.2f" % t, "-i", mp4,
                        "-frames:v", "1", "-update", "1", "/tmp/cap.png"], check=True)
        g = np.asarray(Image.open("/tmp/cap.png").convert("L").resize((270, 480)), float)
        lap = (g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:] - 4 * g[1:-1, 1:-1])
        q = lap.var()
        # descarta quadro de piscada: sem os dois olhos detectados, nao vira capa.
        # a primeira versao escolhia so pela nitidez e pegou ele de olho fechado.
        cinza = np.asarray(Image.open("/tmp/cap.png").convert("L"), np.uint8)
        dois = len(olhos.detectMultiScale(cinza[: int(len(cinza) * 0.55)], 1.1, 12,
                                          minSize=(60, 60))) >= 2
        if (dois and not aberto) or (dois == aberto and q > mq):
            if dois and not aberto:
                mq = -1
            aberto = aberto or dois
            if q > mq:
                mq, melhor = q, Image.open("/tmp/cap.png").convert("RGB")
        t += passo
    melhor.save(saida, quality=92)
    print("%-34s nitidez %.0f  olhos abertos: %s" % (os.path.basename(saida), mq, "sim" if aberto else "NAO ACHOU"))


if __name__ == "__main__":
    for mp4 in sys.argv[1:]:
        capa(mp4, os.path.basename(mp4).replace(".mp4", "_capa.jpg"))
