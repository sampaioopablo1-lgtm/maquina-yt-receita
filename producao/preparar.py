# -*- coding: utf-8 -*-
"""Um comando so: extrai audio, corta silencio e transcreve com tempo por palavra.
   python3 preparar.py IMG_2010.MOV
Depois disso so falta escolher os trechos e escrever o plano."""
import json, subprocess, sys, os
from faster_whisper import WhisperModel

FF = "/usr/local/bin/ffmpeg"
src = sys.argv[1]
base = os.path.splitext(os.path.basename(src))[0]

subprocess.run([FF, "-y", "-loglevel", "error", "-i", src, "-vn", "-ac", "1",
                "-ar", "16000", "-c:a", "pcm_s16le", "%s.wav" % base], check=True)
subprocess.run(["python3", "cortar_silencio.py", "%s.wav" % base, "insp_%s.json" % base],
               check=True)

m = WhisperModel("fw", device="cpu", compute_type="int8", cpu_threads=4, local_files_only=True)
segs, _ = m.transcribe("%s.wav" % base, language="pt", word_timestamps=True, vad_filter=False)
out = []
for s in segs:
    out.append({"s": round(s.start, 2), "e": round(s.end, 2), "t": s.text.strip(),
                "w": [{"s": round(w.start, 2), "e": round(w.end, 2), "t": w.word.strip()}
                      for w in (s.words or [])]})
    print("[%6.2f-%6.2f] %s" % (s.start, s.end, s.text.strip()), flush=True)
json.dump(out, open("tr_%s.json" % base, "w"), ensure_ascii=False, indent=1)
print("\n-> tr_%s.json e insp_%s.json prontos" % (base, base))
