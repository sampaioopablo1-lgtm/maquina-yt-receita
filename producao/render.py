# -*- coding: utf-8 -*-
import json, subprocess
from legendas import Y

FF = "/usr/local/bin/ffmpeg"
meta = json.load(open("leg/meta.json"))

ins, filt, cur = [], [], "[0:v]"
for i, m in enumerate(meta):
    ins += ["-i", m["png"]]
    nxt = "[v%d]" % i
    filt.append("%s[%d:v]overlay=0:%d:enable='between(t,%.2f,%.2f)'%s"
                % (cur, i + 2, Y, m["ini"], m["fim"], nxt))
    cur = nxt
fc = ";".join(filt)

cmd = ([FF, "-y", "-loglevel", "error", "-i", "mudo.mp4", "-i", "mix.wav"] + ins +
       ["-filter_complex", fc, "-map", cur, "-map", "1:a",
        "-c:v", "libx264", "-profile:v", "high", "-crf", "18", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-shortest", "OPC06_previsibilidade.mp4"])
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stderr[-2000:] if r.returncode else "OPC05_agencia.mp4 pronto")
