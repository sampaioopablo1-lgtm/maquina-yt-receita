import glob, os, subprocess
from PIL import Image, ImageDraw, ImageFont
FF = "/usr/local/bin/ffmpeg"
fs = sorted(glob.glob("bx/q_*.mp4"))
fnt = ImageFont.truetype("fontes/Montserrat.ttf", 15)
rows = []
for f in fs:
    idn = os.path.basename(f)[2:-4]
    sh = "sheet_%s.jpg" % idn
    subprocess.run([FF, "-v", "error", "-y", "-i", f,
                    "-vf", "fps=1/1.5,scale=150:-1,tile=7x1", "-frames:v", "1", sh], check=False)
    if os.path.exists(sh):
        rows.append((idn, Image.open(sh)))
w = max(i.width for _, i in rows)
h = sum(i.height + 24 for _, i in rows)
out = Image.new("RGB", (w, h), "white")
d = ImageDraw.Draw(out)
y = 0
for idn, im in rows:
    d.text((4, y + 4), "%s   quadros em 0 / 1,5 / 3,0 / 4,5 / 6,0 / 7,5 / 9,0 s" % idn, fill="black", font=fnt)
    out.paste(im, (0, y + 22))
    y += im.height + 24
out.save("folha.jpg", quality=72)
print(out.size, os.path.getsize("folha.jpg"))
