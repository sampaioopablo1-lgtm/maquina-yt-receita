# -*- coding: utf-8 -*-
"""Escolha de SFX e por MEDIDA: duracao, tempo de ataque, % de energia abaixo de 200 Hz."""
import subprocess, wave, sys, glob
import numpy as np
FF = "/usr/local/bin/ffmpeg"
SR = 48000


def le(p, t=None):
    a = [FF, "-y", "-loglevel", "error", "-i", p]
    if t: a += ["-t", str(t)]
    a += ["-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", "/tmp/x.wav"]
    subprocess.run(a, check=True)
    w = wave.open("/tmp/x.wav", "rb")
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    w.close()
    return x


def mede(nome, p, t=None):
    x = le(p, t)
    pico = np.abs(x).max()
    ataque = int(np.argmax(np.abs(x) > 0.9 * pico)) / SR
    f = np.fft.rfft(x * np.hanning(len(x))); hz = np.fft.rfftfreq(len(x), 1 / SR)
    pw = np.abs(f) ** 2
    grave = 100 * pw[hz < 200].sum() / pw.sum()
    alto = 100 * pw[hz > 2000].sum() / pw.sum()
    cen = (hz * pw).sum() / pw.sum()
    print("%-22s dur %.2fs  pico %.2f  ataque %.3fs  grave<200Hz %5.1f%%  >2kHz %5.1f%%  centroide %5.0f Hz"
          % (nome, len(x) / SR, pico, ataque, grave, alto, cen))
    return dict(ataque=ataque, grave=grave, alto=alto, cen=cen)


print("CRITERIO whoosh: ataque < 0,100 s  e  grave < 5%")
print("CRITERIO grave : grave > 80%\n")
mede("whoosh (catalogo id1)", "sfx/whoosh.mp3")
mede("whoosh-velocity id4", "sfx/whoosh_vel.mp3")
mede("whoosh-velocity 0,6s", "sfx/whoosh_vel.mp3", 0.6)
mede("boom (catalogo id2)", "sfx/boom.mp3")
