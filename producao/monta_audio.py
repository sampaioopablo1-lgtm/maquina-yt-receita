# -*- coding: utf-8 -*-
"""Trilha do Reel: fala emendada + camada de efeitos em ESTEREO.

Por que mudou (pedido do Pablo em 07/09/2026: "os efeitos estao basicos demais"):
a versao v1 tinha exatamente dois sons -- um unico whoosh repetido em todo corte
e um grave na virada. Repetir o MESMO whoosh cinco vezes e o que denuncia edicao
amadora: o ouvido decora o som no segundo corte e para de sentir o corte.

O que existe agora, tudo som real (Mixkit, uso comercial livre), escolhido por
MEDIDA entre 36 candidatos -- nunca sintetizado:

  cama.mp3      46 s, centroide 546 Hz, 31% de grave. Roda por baixo do video
                inteiro em -26 dB. Nao se ouve; sente-se. E ela que tira o som
                de "gravado no celular" e da corpo ao silencio entre as frases.
  wh_curto      0,48 s, centroide 3642 Hz -- corte seco, rapido
  wh_medio      1,76 s, centroide 3184 Hz -- corte com um pouco mais de ar
  wh_longo      1,33 s, centroide 3704 Hz -- o mais aberto dos tres
  whoosh_fs     1,37 s, centroide 1817 Hz -- o whoosh historico do canal
                Os quatro se REVEZAM na ordem dos cortes, e cada um entra por um
                lado do estereo (esquerda, direita, esquerda...). Dois cortes
                seguidos nunca soam iguais nem vem do mesmo lugar.
  riser.mp3     2,49 s, sobe ate o pico em 1,93 s. Entra ANTES da virada e o
                pico dele cai junto com o corte: e o que faz a virada ser
                esperada em vez de so acontecer.
  sub.mp3       1,10 s, 92% abaixo de 200 Hz, pico em 0,30 s. O impacto da
                virada. Substitui o boom.mp3 antigo, que tinha 2,04 s de ataque
                e obrigava a posicionar o arquivo dois segundos antes do corte.
  boom_curto    2,32 s, 84% de grave. Um so, na entrada do plano de fecho (CTA),
                para o pedido final ter peso.

Regras que continuam valendo: todo efeito e posicionado pelo PICO, nunca pelo
inicio do arquivo; teto do PCM em TETO_PCM; a fala manda -- se a soma dos
efeitos empurrar o pico, quem cede sao os efeitos, nao a voz.
"""
import os, subprocess, wave
import numpy as np
from plano import FALA, PLANOS, SRC, WHOOSH_ANTES, TETO_PCM, blocos

FF = "/usr/local/bin/ffmpeg"
SR = 48000
os.makedirs("tmp", exist_ok=True)   # temporarios LOCAIS: dois videos podem
                                     # renderizar ao mesmo tempo em pastas diferentes

# ganho de cada camada, ja calibrado contra a fala normalizada
G_CAMA, G_WHOOSH, G_RISER, G_SUB, G_BOOM = 0.050, 0.38, 0.26, 0.34, 0.22
# quanto o whoosh puxa para um lado (1,0 = centro nos dois canais)
LADO_FORTE, LADO_FRACO = 1.0, 0.45


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


def efeito(nome):
    """Carrega um efeito normalizado no pico."""
    x = wav("sfx/%s" % nome, "tmp/e_%s.wav" % nome.replace(".", "_"))
    return x / (np.abs(x).max() + 1e-9)


def pico_em(som):
    """Instante em que o som chega a 90% do pico. E ESTE ponto que cai no corte."""
    return int(np.argmax(np.abs(som) > 0.9 * np.abs(som).max())) / SR


# ---------------------------------------------------------------- 1) a fala
fala = np.concatenate([wav(SRC, "tmp/f%d.wav" % i, a, b - a)
                       for i, (a, b, _) in enumerate(FALA)])
N = len(fala)
print("fala %.2f s" % (N / SR))

bl, ini = blocos()
trocas = [b[1] for b in bl[1:]]     # inicio de cada plano, menos o primeiro
virada = trocas[0]
fecho = bl[-1][1]                   # inicio do ultimo plano: o pedido final

# ------------------------------------------------- 2) as camadas de efeito
esq = np.zeros(N, dtype=np.float32)
dir = np.zeros(N, dtype=np.float32)


def poe(t, som, g, pan=0):
    """pan: -1 esquerda, +1 direita, 0 centro. t e onde o PICO deve cair."""
    som = som * g
    i = int(round((t - pico_em(som)) * SR))
    corte = 0
    if i < 0:
        corte, i = -i, 0
    n = min(len(som) - corte, N - i)
    if n <= 0:
        return
    ge = LADO_FORTE if pan <= 0 else LADO_FRACO
    gd = LADO_FORTE if pan >= 0 else LADO_FRACO
    esq[i:i + n] += som[corte:corte + n] * ge
    dir[i:i + n] += som[corte:corte + n] * gd


# a cama, esticada ate o fim do video, com abertura e fecho suaves
cama = efeito("cama.mp3")
cama = np.tile(cama, int(N / len(cama)) + 1)[:N]
env = np.ones(N, dtype=np.float32)
sobe, desce = int(1.2 * SR), int(1.5 * SR)
env[:sobe] = np.linspace(0, 1, sobe)
env[-desce:] = np.linspace(1, 0, desce)
# o lado direito entra 11 ms depois: alarga a cama sem mexer na voz
atraso = int(0.011 * SR)
esq += cama * env * G_CAMA
dir += np.concatenate([np.zeros(atraso, np.float32), cama[:-atraso]]) * env * G_CAMA

# os whooshes, revezando som e lado
paleta = [efeito("whoosh_fs.mp3"), efeito("wh_medio.mp3"),
          efeito("wh_curto.mp3"), efeito("wh_longo.mp3")]
nomes = ["whoosh_fs", "wh_medio", "wh_curto", "wh_longo"]
for k, t in enumerate(trocas):
    poe(t - WHOOSH_ANTES, paleta[k % 4], G_WHOOSH, -1 if k % 2 == 0 else 1)
    print("  corte %.2f s  %-10s  %s" % (t, nomes[k % 4], "esquerda" if k % 2 == 0 else "direita"))

# o riser sobe para dentro da virada e o sub estoura nela
poe(virada, efeito("riser.mp3"), G_RISER)
poe(virada, efeito("sub.mp3"), G_SUB)
print("  virada %.2f s: riser + sub" % virada)

# um grave curto na entrada do fecho, para o pedido final ter peso
if fecho > virada + 1.0:
    poe(fecho, efeito("boom_curto.mp3"), G_BOOM)
    print("  fecho  %.2f s: grave curto" % fecho)

# ------------------------------------------------------ 3) mistura e teto
mixE = fala * 0.97 + esq
mixD = fala * 0.97 + dir
pico = max(np.abs(mixE).max(), np.abs(mixD).max())
k = TETO_PCM / pico
mixE, mixD = mixE * k, mixD * k
print("pico antes %.3f -> depois %.3f" % (pico, max(np.abs(mixE).max(), np.abs(mixD).max())))

st = np.empty(N * 2, dtype=np.float32)
st[0::2], st[1::2] = mixE, mixD
w = wave.open("mix.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
print("mix.wav estereo %.2f s" % (N / SR))
