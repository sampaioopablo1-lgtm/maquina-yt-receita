# -*- coding: utf-8 -*-
"""Confere DECODIFICANDO o mp4 final -- a unica conferencia que vale."""
import subprocess, wave
import numpy as np
from plano import blocos

FF = "/usr/local/bin/ffmpeg"
V = "OPC06_previsibilidade.mp4"
SR = 48000

subprocess.run([FF, "-y", "-loglevel", "error", "-i", V, "-vn", "-ac", "1",
                "-ar", str(SR), "-c:a", "pcm_f32le", "-f", "f32le", "/tmp/dec.raw"], check=True)
x = np.fromfile("/tmp/dec.raw", dtype=np.float32)
print("1) PICO do audio decodificado: %.3f  %s" % (np.abs(x).max(),
      "OK (< 1,0)" if np.abs(x).max() < 1.0 else "CLIPANDO"))

# brilho (>2 kHz) em janela de 300 ms em torno de cada corte
bl, ini = blocos()
trocas = [b[1] for b in bl[1:]]


def brilho(t):
    i = int((t - 0.15) * SR); n = int(0.30 * SR)
    seg = x[max(0, i):max(0, i) + n]
    if len(seg) < 1000:
        return None
    f = np.fft.rfft(seg * np.hanning(len(seg)))
    hz = np.fft.rfftfreq(len(seg), 1 / SR)
    p = np.abs(f) ** 2
    return 100.0 * p[hz > 2000].sum() / (p.sum() + 1e-12)


sem = [brilho(t) for t in (3.0, 8.5, 14.0, 26.0)]
print("2) BRILHO >2 kHz")
print("   sem troca: %s  (media %.1f%%)" % (["%.1f" % s for s in sem], np.mean(sem)))
for t in trocas:
    print("   troca em %5.2f s: %.1f%%" % (t, brilho(t)))

d = float(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries",
                          "format=duration", "-of", "csv=p=0", V],
                         capture_output=True, text=True).stdout or 0)
print("3) duracao %.2f s" % (len(x) / SR))
