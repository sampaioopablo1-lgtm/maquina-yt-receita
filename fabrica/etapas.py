#!/usr/bin/env python3
"""Roda um pacote em etapas SEQUENCIAIS, cada uma comecando so quando a anterior
retorna.

Existe por causa de um estrago concreto. Num pacote de 196 cenas, os clipes
(335 MB) + o concat (45 MB) + a trilha (95 MB) nao cabem nos 493 MB de tmpfs do
sandbox, entao era preciso liberar espaco no meio. A primeira tentativa usou um
processo em segundo plano que apagava os clipes quando `video.mp4` ficava 8s do
mesmo tamanho — tratando "parou de crescer" como "terminou".

Nao e sinal nenhum: a escrita do ffmpeg e em rajadas. Os clipes sumiram no meio
do concat e o video saiu com 1236,9s em vez de 1716s — 28% faltando, incluindo o
capitulo final e o CTA. E o log dizia "render ok 1716", porque a soma vinha dos
tempos medidos ANTES da limpeza: a saida estava truncada e o log parecia certo.

Daqui saem tres regras, todas aplicadas abaixo:
  1. quem libera espaco e o proprio fluxo, depois do subprocess RETORNAR;
  2. toda etapa que produz arquivo confere o proprio resultado (o assert do
     concat), em vez de reportar a medicao da entrada;
  3. limpeza usa padrao ancorado (`lclip*.mp4`, `l{i:02d}.png`) e nunca curinga
     de uma letra — `l*.srt` levou junto o `legendas.srt`, que era entregavel.

Uso:  python3 etapas.py <spec.json>
"""
import sys, os, json, glob, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fabrica as F

spec = sys.argv[1] if len(sys.argv) > 1 else "/tmp/fab/setiap-level-004.json"
sp = json.load(open(spec))
d = F.dir_trabalho(sp)


def log(m):
    print(m, flush=True)


# ---------------------------------------------------------------- 1. assets
if len(glob.glob(f"{d}/l*.mp3")) < len(sp["longo"]):
    log("etapa 1: montar")
    F.montar(spec)
log(f"etapa 1 ok: {len(glob.glob(f'{d}/l*.mp3'))} mp3")

# ------------------------------------------- 2. clipes, liberando um a um
log("etapa 2: clipes do longo")
cenas = sp["longo"]
W, H = 1280, 720
RW, RH = F.render_wh(W, H)
tempos = []
for i, c in enumerate(cenas):
    saida = f"{d}/lclip{i:02d}.mp4"
    if not (os.path.exists(saida) and os.path.getsize(saida) > 10000):
        dd = F.dur(f"{d}/l{i:02d}.mp3") + 0.5
        nf = max(int(dd * 30), 1)
        z, fx, fy = F.ken_burns(i, nf)
        vf = (f"zoompan=z='{z}':d={nf}:x='(iw-iw/zoom)*({fx})'"
              f":y='(ih-ih/zoom)*({fy})':s={RW}x{RH}:fps=30")
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-loop", "1",
            "-i", f"{d}/l{i:02d}.png", "-i", f"{d}/l{i:02d}.mp3", "-vf", vf,
            "-t", f"{dd:.2f}", "-c:v", "libx264", "-preset", "ultrafast",
            "-crf", "23", "-pix_fmt", "yuv420p", *F.AUDIO_ARGS, saida],
            check=True, capture_output=True)
    tempos.append(F.dur(saida))
    # padrao ancorado: nunca `l*.png`
    for ext in ("png", "mp3"):
        try:
            os.remove(f"{d}/l{i:02d}.{ext}")
        except OSError:
            pass
    if i % 40 == 0:
        log(f"  clipe {i}/{len(cenas)}")
log(f"etapa 2 ok: {len(tempos)} clipes, {sum(tempos):.1f}s")

# ------------------------------- 3. legenda ANTES de qualquer limpeza futura
with open(f"{d}/legendas.srt", "w", encoding="utf-8") as srt:
    t = 0.0
    for i, c in enumerate(cenas):
        fim = t + tempos[i]
        srt.write(f"{i+1}\n{F.st(t + 0.15)} --> {F.st(fim - 0.15)}\n{c['nar']}\n\n")
        t = fim
json.dump(tempos, open(f"{d}/tempos.json", "w"))
log("etapa 3 ok: legendas.srt + tempos.json")

# ------------------------------------ 4. concat: retorna so quando ffmpeg sai
log("etapa 4: concat")
with open(f"{d}/llista.txt", "w") as f:
    for i in range(len(cenas)):
        f.write(f"file 'lclip{i:02d}.mp4'\n")
crf = "29" if sum(tempos) >= 1100 else "26"
subprocess.run(["ffmpeg", "-nostdin", "-y", "-f", "concat", "-safe", "0",
    "-i", f"{d}/llista.txt", "-vf", f"scale={W}:{H}:flags=lanczos",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", crf,
    "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
    f"{d}/video.mp4"], check=True, capture_output=True, cwd=d)
dv = F.dur(f"{d}/video.mp4")
log(f"etapa 4 ok: video.mp4 {dv:.1f}s")
# A etapa confere a PROPRIA saida. Sem isto, um concat truncado passa batido
# atras de um log de sucesso montado com a medicao da entrada.
assert abs(dv - sum(tempos)) < 5, f"concat truncado: {dv:.1f} vs {sum(tempos):.1f}"

# ------------------------- 5. so agora, com o concat conferido, libera clipes
for f in glob.glob(f"{d}/lclip*.mp4"):
    os.remove(f)
log("etapa 5 ok: clipes liberados")

# ---------------------------------------------------------------- 6. trilha
log("etapa 6: trilha")
F.aplicar_trilha(d, "video.mp4", sp["slug"])
log(f"etapa 6 ok: {F.dur(f'{d}/video.mp4'):.1f}s, "
    f"{os.path.getsize(f'{d}/video.mp4') / 1e6:.1f} MB")
log("PACOTE OK")
