# -*- coding: utf-8 -*-
"""Fala emendada + whoosh antes de cada troca + UM grave na virada.
Efeitos REAIS (catalogo opc.midia), nunca sintetizados. Teto do PCM em 0,86."""
import os, subprocess, wave
import numpy as np
from plano import FALA, PLANOS, SRC, WHOOSH_ANTES, TETO_PCM, blocos

FF = "/usr/local/bin/ffmpeg"
SR = 48000


def run(a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(a)); print(r.stderr[-1200:]); raise SystemExit(1)


def le(p):
    w = wave.open(p, "rb")
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    n = w.getnchannels(); w.close()
    return x.reshape(-1, n).mean(axis=1) if n > 1 else x


def wav(src, dst, ss=None, t=None):
    a = [FF, "-y", "-loglevel", "error"]
    if ss is not None: a += ["-ss", "%.3f" % ss]
    a += ["-i", src]
    if t is not None: a += ["-t", "%.3f" % t]
    run(a + ["-vn", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", dst])
    return le(dst)


# 1) fala
fala = np.concatenate([wav(SRC, "/tmp/f%d.wav" % i, a, b - a)
                       for i, (a, b, _) in enumerate(FALA)])
print("fala %.2f s" % (len(fala) / SR))

# 2) trilha de efeitos, do tamanho da fala
sfx = np.zeros_like(fala)
whoosh = wav("sfx/whoosh_fs.mp3", "/tmp/wh.wav")
boom = wav("sfx/boom.mp3", "/tmp/bo.wav")
whoosh = whoosh / (np.abs(whoosh).max() + 1e-9)
boom = boom / (np.abs(boom).max() + 1e-9)

bl, ini = blocos()
trocas = [b[1] for b in bl[1:]]          # inicio de cada plano, menos o primeiro
virada = trocas[0]                        # a virada de assunto

def poe(buf, som, t, g):
    i = int(round(t * SR))
    if i < 0:
        som = som[-i:]; i = 0
    n = min(len(som), len(buf) - i)
    if n > 0: buf[i:i + n] += som[:n] * g


def ataque(som):
    """Onde o som chega a 90% do pico -- e este ponto que tem de cair no corte."""
    return int(np.argmax(np.abs(som) > 0.9 * np.abs(som).max())) / SR


aw, ab = ataque(whoosh), ataque(boom)
# o whoosh marca o corte: o pico dele cai WHOOSH_ANTES antes da troca
for t in trocas:
    poe(sfx, whoosh, t - WHOOSH_ANTES - aw, 0.42)
# o grave estoura NA virada
poe(sfx, boom, virada - ab, 0.30)
print("%d whooshes (ataque %.3f s); 1 grave em %.2f s (ataque %.3f s)"
      % (len(trocas), aw, virada, ab))

# 3) mistura com teto real
mix = fala * 0.97 + sfx
pico = np.abs(mix).max()
mix = mix * (TETO_PCM / pico)
print("pico antes %.3f -> depois %.3f" % (pico, np.abs(mix).max()))

os.makedirs("saida", exist_ok=True)
w = wave.open("mix.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
print("mix.wav %.2f s" % (len(mix) / SR))
