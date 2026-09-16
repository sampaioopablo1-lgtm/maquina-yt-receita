# -*- coding: utf-8 -*-
import os, subprocess
from plano import FALA, PLANOS, SRC, FPS, W, H, DISSOLVE, blocos

FF = "/usr/local/bin/ffmpeg"
os.makedirs("planos", exist_ok=True)
VF = ("scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,"
      "fps=%d,setsar=1,format=yuv420p" % (W, H, W, H, FPS))


def run(a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(a)); print(r.stderr[-1500:]); raise SystemExit(1)


bl, ini = blocos()
segs = []
for k, (p, (i0, ta, tb, d)) in enumerate(zip(PLANOS, bl)):
    tipo, fonte, entrada, idx, diss = p
    extra = DISSOLVE if diss else 0.0
    out = "planos/v%02d.mp4" % k
    if tipo == "rosto":
        # segue a mesma emenda do audio: um corte de video por trecho de fala
        partes = []
        for j, i in enumerate(idx):
            a, b, _ = FALA[i]
            ini_j = a - extra if j == 0 else a
            pp = "planos/v%02d_%d.mp4" % (k, j)
            run([FF, "-y", "-loglevel", "error", "-ss", "%.3f" % ini_j, "-i", SRC,
                 "-t", "%.3f" % (b - ini_j), "-an", "-vf", VF,
                 "-c:v", "libx264", "-crf", "16", "-preset", "medium", pp])
            partes.append(pp)
        lst = "planos/l%02d.txt" % k
        open(lst, "w").write("".join("file '%s'\n" % os.path.basename(x) for x in partes))
        run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", lst, "-c", "copy", out])
    else:
        # ARMADILHA que ja custou um video: se o b-roll for mais curto do que o
        # trecho de fala, o ffmpeg NAO da erro -- ele entrega um clipe curto, e o
        # video final sai truncado sem aviso. Confira antes de cortar.
        r = subprocess.run([FF, "-i", fonte], capture_output=True, text=True)
        import re as _re
        m = _re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
        disp = (int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
                - (entrada - extra)) if m else 0
        if disp < d + extra - 0.02:
            raise SystemExit("%s tem so %.2f s a partir de %.2f, e o bloco pede %.2f s"
                             % (fonte, disp, entrada - extra, d + extra))
        run([FF, "-y", "-loglevel", "error", "-ss", "%.3f" % (entrada - extra),
             "-i", fonte, "-t", "%.3f" % (d + extra), "-an", "-vf", VF,
             "-c:v", "libx264", "-crf", "16", "-preset", "medium", out])
    segs.append((out, d, diss))
    print("v%02d %-22s %.2f s%s" % (k, fonte.split('/')[-1], d, "  +dissolvencia" if diss else ""))

# encadeia: corte seco = concat, virada = xfade de 0,5 s
cur = segs[0][0]
acc = segs[0][1]
for k in range(1, len(segs)):
    nxt, d, diss = segs[k]
    out = "planos/x%02d.mp4" % k
    if diss:
        run([FF, "-y", "-loglevel", "error", "-i", cur, "-i", nxt,
             "-filter_complex", "[0][1]xfade=transition=fade:duration=%.2f:offset=%.3f,format=yuv420p"
             % (DISSOLVE, acc - DISSOLVE),
             "-c:v", "libx264", "-crf", "16", "-preset", "medium", out])
    else:
        lst = "planos/c%02d.txt" % k
        open(lst, "w").write("file '%s'\nfile '%s'\n" %
                             (os.path.basename(cur), os.path.basename(nxt)))
        run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", lst, "-c", "copy", out])
    cur, acc = out, round(acc + d, 3)
    print("  encadeado ate %.2f s (%s)" % (acc, "dissolvencia" if diss else "corte seco"))

run([FF, "-y", "-loglevel", "error", "-i", cur, "-c", "copy", "mudo.mp4"])
print("mudo.mp4 pronto, alvo %.2f s" % ini[-1])
