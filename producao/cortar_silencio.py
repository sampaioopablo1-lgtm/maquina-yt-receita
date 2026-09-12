import json, io, sys, wave
import numpy as np
WAV, OUT = sys.argv[1], sys.argv[2]
MIN_SILENCIO = float(sys.argv[3]) if len(sys.argv) > 3 else 0.30
FOLGA        = float(sys.argv[4]) if len(sys.argv) > 4 else 0.05
LIMIAR       = float(sys.argv[5]) if len(sys.argv) > 5 else 0.035
w = wave.open(WAV, "rb"); SR = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32); w.close()
DUR = len(x)/SR
HOP, JAN = 0.01, 0.03
n, h = int(JAN*SR), int(HOP*SR)
e = np.array([np.sqrt((x[i:i+n]**2).mean()+1e-9) for i in range(0, max(1,len(x)-n), h)])
e = e/(np.percentile(e,95)+1e-9)
mudo = e < LIMIAR
sil, i = [], 0
while i < len(mudo):
    if mudo[i]:
        j = i
        while j < len(mudo) and mudo[j]: j += 1
        if (j-i)*HOP >= MIN_SILENCIO: sil.append((i*HOP, j*HOP))
        i = j
    else: i += 1
fala, pos = [], 0.0
for a,b in sil:
    if a-pos > 0.12: fala.append((pos,a))
    pos = b
if DUR-pos > 0.12: fala.append((pos,DUR))
ajust = [(max(0.0,a-FOLGA), min(DUR,b+FOLGA)) for a,b in fala]
clipes, t = [], 0.0
for k,(a,b) in enumerate(ajust):
    d = round(b-a,3)
    clipes.append({"id":"c%02d"%k,"start":round(t,3),"duration":d,"inPoint":round(a,3),"outPoint":round(b,3)})
    t += d
json.dump({"clipes":clipes}, io.open(OUT,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("%.2fs -> %.2fs em %d clipes (%d silencios, %.2fs cortados)" % (DUR,t,len(clipes),len(sil),DUR-t))
for c in clipes: print("  %s tl %6.2f dur %5.2f fonte %6.2f -> %6.2f" % (c["id"],c["start"],c["duration"],c["inPoint"],c["outPoint"]))
