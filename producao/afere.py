# -*- coding: utf-8 -*-
"""Confere a trilha DECODIFICANDO o mp4 final -- pico, brilho e largura estereo
nos cortes contra os mesmos numeros durante a fala. E a unica prova de que os
efeitos existem no arquivo entregue, e nao so no script."""
import subprocess, sys, os
import numpy as np
from plano import blocos
FF = "/usr/local/bin/ffmpeg"; SR = 48000
v = sys.argv[1]
os.makedirs("tmp", exist_ok=True)
subprocess.run([FF, "-y", "-loglevel", "error", "-i", v, "-vn", "-ac", "2", "-ar", str(SR),
                "-c:a", "pcm_f32le", "-f", "f32le", "tmp/a.raw"], check=True)
x = np.fromfile("tmp/a.raw", dtype=np.float32).reshape(-1, 2)
bl, ini = blocos(); trocas = [b[1] for b in bl[1:]]


def med(t, w=0.30):
    i = int((t - 0.15) * SR); s = x[max(0, i):max(0, i) + int(w * SR)]
    if len(s) < 1000: return None
    m = s.mean(1); f = np.fft.rfft(m * np.hanning(len(m)))
    hz = np.fft.rfftfreq(len(m), 1 / SR); p = np.abs(f) ** 2
    d = s[:, 0] - s[:, 1]
    return (100 * p[hz > 2000].sum() / p.sum(), 100 * p[hz < 200].sum() / p.sum(),
            np.sqrt((d ** 2).mean()) / (np.sqrt((m ** 2).mean()) + 1e-9))


cor = [med(t) for t in trocas]
# so mede "fala pura": longe de qualquer corte, senao a amostra pega o whoosh
longe = [t for t in np.arange(1.0, ini[-1] - 1.0, 0.9)
         if all(abs(t - c) > 1.6 for c in trocas)]
meio = [m for m in (med(t) for t in longe) if m]
ag_c = np.mean([c[0] for c in cor]); ag_f = np.mean([m[0] for m in meio])
la_c = np.mean([c[2] for c in cor]); la_f = np.mean([m[2] for m in meio])
print("%-32s pico %.3f  brilho corte/fala %4.1f%% x %4.1f%%  largura %.2f x %.2f  %s"
      % (os.path.basename(v), np.abs(x).max(), ag_c, ag_f, la_c, la_f,
         "OK" if np.abs(x).max() < 1.0 and ag_c > 2 * ag_f and la_c > 2 * la_f else "CONFERIR"))
