import subprocess, numpy as np, cv2
FF = "/usr/local/bin/ffmpeg"
SRC = "IMG_2007.MOV"
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
tops, chins, ws = [], [], []
for t in [2, 10, 20, 30, 40, 50, 60, 70]:
    p = "/tmp/m_%d.png" % t
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(t), "-i", SRC,
                    "-frames:v", "1", "-update", "1", p], check=False)
    im = cv2.imread(p)
    if im is None:
        continue
    h, w = im.shape[:2]
    det = casc.detectMultiScale(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), 1.15, 6,
                               minSize=(int(w * .10), int(w * .10)))
    if len(det):
        x, y, fw, fh = max(det, key=lambda r: r[2] * r[3])
        tops.append(y); chins.append(y + fh); ws.append(fw)
        print("t=%2d  quadro %dx%d  rosto x=%d y=%d w=%d h=%d" % (t, w, h, x, y, fw, fh))
print("MEDIANA topo=%.0f queixo=%.0f largura=%.0f  (quadro %dx%d)" %
      (np.median(tops), np.median(chins), np.median(ws), w, h))
