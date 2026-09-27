"""Exporta um criativo HTML de proximo-cliente/criativos/ para MP4 1080x1920.

O video e gravado em tempo real pelo Chromium do Playwright (modo #render do
criativo: palco em tela cheia, sem controles) e o audio sai de um
OfflineAudioContext (window.__renderAudio), mixado depois pelo ffmpeg do
imageio-ffmpeg. Rode de um diretorio temporario: grava render_page.html, vid/,
audio.wav, out.mp4 e thumb.jpg no diretorio atual.
"""
import os, time, base64, subprocess, pathlib, glob, shutil
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
SRC = pathlib.Path('/home/user/maquina-yt-receita/proximo-cliente/criativos/01-lead-esfria-5-minutos.html')
html = SRC.read_text()
doc = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>'
page_path = pathlib.Path('render_page.html'); page_path.write_text(doc)
vid_dir = pathlib.Path('vid'); shutil.rmtree(vid_dir, ignore_errors=True); vid_dir.mkdir()
EXE = glob.glob('/opt/pw-browsers/chromium-*/chrome-linux*/chrome')[0]
proxy = os.environ.get('HTTPS_PROXY')
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE, proxy={'server': proxy} if proxy else None, args=['--autoplay-policy=no-user-gesture-required'])
    # 1) áudio offline
    ctx = b.new_context(viewport={'width':1080,'height':1920})
    pg = ctx.new_page(); pg.goto(page_path.resolve().as_uri() + '#render'); pg.wait_for_timeout(1500)
    wav = base64.b64decode(pg.evaluate('window.__renderAudio()'))
    pathlib.Path('audio.wav').write_bytes(wav); ctx.close()
    # 2) vídeo em tempo real
    ctx = b.new_context(viewport={'width':1080,'height':1920}, record_video_dir=str(vid_dir), record_video_size={'width':1080,'height':1920})
    t_ctx = time.time()
    pg = ctx.new_page(); pg.goto(page_path.resolve().as_uri() + '#render')
    pg.evaluate('document.fonts.ready.then(()=>1)'); pg.wait_for_timeout(1500)
    fonts = pg.evaluate("document.fonts.check('800 20px Montserrat') && document.fonts.check('italic 700 20px \"Playfair Display\"')")
    t_play = time.time(); pg.evaluate('window.__play()')
    pg.wait_for_timeout(31000)
    ctx.close(); b.close()
off = t_play - t_ctx
webm = glob.glob(str(vid_dir/'*.webm'))[0]
print('fonts ok:', fonts, 'offset', round(off,2))
subprocess.run([FF,'-y','-loglevel','error','-ss',f'{off:.3f}','-i',webm,'-i','audio.wav','-t','30','-map','0:v','-map','1:a',
  '-vf','fps=30,scale=1080:1920,format=yuv420p','-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart','out.mp4'],check=True)
subprocess.run([FF,'-y','-loglevel','error','-ss','2.6','-i','out.mp4','-frames:v','1','thumb.jpg'],check=True)
print(os.path.getsize('out.mp4'))
