import json, subprocess, sys, os, asyncio
import cairosvg, edge_tts

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from maquina.media import duracao as _duracao, ffmpeg_bin  # fallback pro binario estatico do imageio-ffmpeg

def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def wrap(t, n):
    out, cur = [], ''
    for w in t.split():
        if len(cur)+len(w)+1 > n: out.append(cur); cur = w
        else: cur = (cur+' '+w).strip()
    if cur: out.append(cur)
    return out

def tsp(t, x, y, size, fill, n=30, anchor='middle', lh=1.25):
    o = f'<text x="{x}" y="{y}" font-family="DejaVu Sans" font-weight="bold" font-size="{int(size)}" fill="{fill}" text-anchor="{anchor}">'
    for i, l in enumerate(wrap(t, n)):
        o += f'<tspan x="{x}" dy="{0 if i==0 else int(size*lh)}">{esc(l)}</tspan>'
    return o + '</text>'

def svg_cena(c, pal, W, H):
    ink, c1, c2 = pal['ink'], pal['c1'], pal['c2']
    bg = pal.get('bg', '#FFFFFF'); lay = c.get('layout','titulo')
    if lay == 'cta': bg, ink2 = ink, '#FFFFFF'
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{bg}"/>'
    cx = W//2
    if lay in ('titulo','cta'):
        fg = c1 if lay=='titulo' else c2
        sub_fg = ink if lay=='titulo' else '#FFFFFF'
        big = c.get('kicker','')
        s += tsp(big, cx, H*0.40, H*(0.15 if len(big)<=10 else 0.09), fg, n=16)
        s += f'<path d="M {cx-W*0.26} {H*0.52} Q {cx} {H*0.55}, {cx+W*0.26} {H*0.52}" stroke="{c2 if lay=="titulo" else c1}" stroke-width="10" fill="none" stroke-linecap="round"/>'
        if c.get('sub'): s += tsp(c['sub'], cx, H*0.65, H*0.055, sub_fg, n=30)
    elif lay == 'lista':
        s += tsp(c.get('kicker',''), cx, H*0.18, H*0.08, ink, n=24)
        y = H*0.38
        for i, it in enumerate(c.get('itens', [])):
            col = [c1, c2, ink][i%3]
            s += f'<circle cx="{W*0.16}" cy="{y-H*0.02}" r="{H*0.025}" fill="{col}"/>'
            s += tsp(it, W*0.21, y, H*0.055, ink, n=36, anchor='start')
            y += H*0.17
    elif lay == 'barras':
        s += tsp(c.get('kicker',''), cx, H*0.16, H*0.08, ink, n=24)
        labs = c.get('itens', ['1','2','3','4']); n = len(labs); bw = W*0.64/n
        alt = c.get('alturas')
        for i, lb in enumerate(labs):
            bh = (H*0.12 + (alt[i]/max(alt))*H*0.48) if alt else (H*0.12 + i*H*0.48/max(n-1,1))
            x = W*0.18 + i*bw
            s += f'<rect x="{x}" y="{H*0.82-bh}" width="{bw*0.72}" height="{bh}" fill="{[c1,c2,ink][i%3]}"/>'
            s += tsp(str(lb), x+bw*0.36, H*0.90, H*0.038, ink, n=14)
    elif lay == 'item':
        s += f'<circle cx="{W*0.27}" cy="{H*0.55}" r="{H*0.22}" fill="none" stroke="{ink}" stroke-width="9"/>'
        s += f'<circle cx="{W*0.27}" cy="{H*0.55}" r="{H*0.14}" fill="{c2}" opacity="0.55"/>'
        s += tsp(c.get('kicker',''), W*0.63, H*0.36, H*0.07, ink, n=20)
        if c.get('preco'):
            s += f'<rect x="{W*0.51}" y="{H*0.5}" width="{W*0.24}" height="{H*0.13}" fill="{c1}"/>'
            s += tsp(c['preco'], W*0.63, H*0.59, H*0.06, '#FFFFFF', n=12)
    return s + '</svg>'

def dur(f):
    return _duracao(f)

def st(x):
    return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{x%60:06.3f}".replace(".",",")

async def vozes(cenas, voz, pref, d):
    for i, c in enumerate(cenas):
        com = edge_tts.Communicate(c["nar"], voz, rate="-4%")
        await com.save(f"{d}/{pref}{i:02d}.mp3")

def montar(spec_file):
    sp = json.load(open(spec_file))
    slug, pal, voz = sp["slug"], sp["paleta"], sp["voz"]
    d = f"/tmp/f/{slug}"; os.makedirs(d, exist_ok=True)
    for pref, cenas, W, H in (("l", sp["longo"], 1280, 720), ("s", sp["short"], 720, 1280)):
        for i, c in enumerate(cenas):
            cairosvg.svg2png(bytestring=svg_cena(c, pal, W, H).encode(), write_to=f"{d}/{pref}{i:02d}.png", output_width=W, output_height=H)
        asyncio.run(vozes(cenas, voz, pref, d))
    th = sp["thumb"]
    tsvg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720"><rect width="1280" height="720" fill="{pal["c1"]}"/><rect x="40" y="40" width="1200" height="640" fill="#FFFFFF"/>' + tsp(th["l1"], 640, 300, 150, pal["ink"], n=12) + tsp(th["l2"], 640, 480, 90, pal["c1"], n=16) + '</svg>'
    cairosvg.svg2png(bytestring=tsvg.encode(), write_to=f"{d}/thumbnail.png", output_width=1280, output_height=720)
    print(slug, "assets ok")

TRILHA_DIR = "/tmp/trilhas"
# Sem `-shortest`: o corte era feito pelo audio (a narracao crua), o que comia
# a folga de 0,5s no fim de cada cena — a fala terminava e a cena virava no
# mesmo quadro. Quem limita a duracao e o `-t` do clipe, entao a folga volta.
AUDIO_ARGS = ["-af","loudnorm=I=-14:TP=-1.5:LRA=11","-ac","2","-ar","48000","-c:a","aac","-b:a","192k"]

def trilha_do_canal(slug):
    """Faixa fixa por canal = assinatura sonora. CC-BY, credito no copy.md."""
    import glob
    fs = sorted(glob.glob(f"{TRILHA_DIR}/*.mp3"))
    return fs[sum(map(ord, slug)) % len(fs)] if fs else None

# Escala de render: o sandbox tem ~1GB de RAM e o zoompan e o maior consumidor.
# Renderiza menor, entrega em HD (upscale no concat, passe unico).
ESCALA_RENDER = 0.75
# Amplitude do Ken Burns por cena (7% = perceptivel sem cortar a arte).
AMP_ZOOM = 0.07
def render_wh(W, H):
    return (int(W * ESCALA_RENDER) // 2 * 2, int(H * ESCALA_RENDER) // 2 * 2)

# Em video explicador a trilha existe para tirar o silencio entre as frases,
# nao para ser ouvida: trilha alta e causa comum de abandono neste formato.
VOL_TRILHA = "-28dB"

def aplicar_trilha(d, out, slug):
    """Mixa a trilha CC-BY sob a narracao em UM passe, sobre o arquivo ja
    concatenado. Por clipe (ou com -stream_loop) estourava a RAM do sandbox;
    aqui o video sai em copy e so o audio e reencodado."""
    faixa = trilha_do_canal(slug)
    if not faixa:
        return
    alvo = f"{d}/{out}"
    dv = dur(alvo)
    # Loop barato: concat demuxer com stream copy ate cobrir o video.
    lista, bed = f"{d}/trilha_lista.txt", f"{d}/bed.mp3"
    with open(lista, "w") as f:
        f.write(f"file '{faixa}'\n" * (int(dv // dur(faixa)) + 2))
    subprocess.run([ffmpeg_bin(),"-nostdin","-y","-f","concat","-safe","0","-i",lista,"-c","copy",bed],check=True,capture_output=True)
    mix = f"{d}/mix_{out}"
    subprocess.run([ffmpeg_bin(),"-nostdin","-y","-i",alvo,"-i",bed,"-filter_complex",
        f"[1:a]volume={VOL_TRILHA}[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=0,"
        "loudnorm=I=-14:TP=-1.5:LRA=11[a]",
        "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-ac","2","-ar","48000",
        "-t",f"{dv:.2f}","-movflags","+faststart",mix],check=True,capture_output=True)
    os.replace(mix, alvo)
    os.remove(bed)

EST = "FontName=DejaVu Sans,Fontsize=14,Bold=1,PrimaryColour=&H00FFFFFF,BorderStyle=3,BackColour=&HB0000000,Outline=1,Shadow=0,MarginV=30"

def render(spec_file):
    sp = json.load(open(spec_file)); slug = sp["slug"]
    d = f"/tmp/f/{slug}"
    tempos = []
    for pref, cenas, W, H in (("l", sp["longo"], 1280, 720), ("s", sp["short"], 720, 1280)):
        for i, c in enumerate(cenas):
            dd = dur(f"{d}/{pref}{i:02d}.mp3") + 0.5
            open(f"{d}/{pref}{i:02d}.srt","w").write(f"1\n{st(0.2)} --> {st(dd-0.15)}\n{c['nar']}\n")
            RW, RH = render_wh(W, H)
            # Ken Burns em funcao de `on` (numero do frame), nao por incremento
            # acumulado: assim a amplitude e a mesma nas duas direcoes e ocupa a
            # cena inteira, seja ela de 8s ou de 15s. O incremento fixo anterior
            # fazia o zoom-in crescer sem teto (+23% numa cena de 13s, cortando
            # a borda do texto) e o zoom-out travar em 1.0 depois de 3,3s,
            # deixando metade das cenas imovel em ~75% da duracao.
            nf = max(int(dd * 30), 1)
            z = f"1+{AMP_ZOOM}*on/{nf}" if i % 2 else f"{1+AMP_ZOOM:.4g}-{AMP_ZOOM}*on/{nf}"
            saida = f"{d}/{pref}clip{i:02d}.mp4"  # RETOMA
            if os.path.exists(saida) and os.path.getsize(saida) > 10000:
                continue
            vf = f"zoompan=z='{z}':d={nf}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={RW}x{RH}:fps=30,subtitles={d}/{pref}{i:02d}.srt:force_style='{EST}'"
            subprocess.run([ffmpeg_bin(),"-nostdin","-y","-loop","1","-i",f"{d}/{pref}{i:02d}.png","-i",f"{d}/{pref}{i:02d}.mp3","-vf",vf,"-t",f"{dd:.2f}","-c:v","libx264","-preset","ultrafast","-crf","23","-pix_fmt","yuv420p",*AUDIO_ARGS,f"{d}/{pref}clip{i:02d}.mp4"],check=True,capture_output=True)
            # MANIFESTO: checkpoint por clipe — uma falha nunca custa o pacote
            with open(f"{d}/manifesto.txt","a") as mf:
                mf.write(f"{pref}clip{i:02d}.mp4\n")
        # Os tempos dos capitulos saem do clipe RENDERIZADO, nunca do mp3: o mp3
        # e a narracao crua, e a cena tem folga no fim. Estimar pelo mp3 dava um
        # erro que se acumulava cena a cena (+23s no fim de um video de 12 min),
        # jogando os capitulos do fim para depois do trecho que nomeiam.
        if pref == "l":
            tempos = [dur(f"{d}/lclip{i:02d}.mp4") for i in range(len(cenas))]
        with open(f"{d}/{pref}lista.txt","w") as f:
            for i in range(len(cenas)): f.write(f"file '{pref}clip{i:02d}.mp4'\n")
        out = "video.mp4" if pref=="l" else "short.mp4"
        RW, RH = render_wh(W, H)
        args = [ffmpeg_bin(),"-nostdin","-y","-f","concat","-safe","0","-i",f"{d}/{pref}lista.txt"]
        if (RW, RH) != (W, H):
            # Aqui nao ha zoompan, entao da para usar um preset eficiente sem
            # risco de OOM: `ultrafast` gerava 178 MB em 12 min (6x maior que
            # o necessario) e estourava o limite de upload de 50 MB.
            args += ["-vf",f"scale={W}:{H}:flags=lanczos","-c:v","libx264","-preset","veryfast","-crf","26","-pix_fmt","yuv420p","-c:a","copy"]
        else:
            args += ["-c","copy"]
        subprocess.run(args + ["-movflags","+faststart",f"{d}/{out}"],check=True,capture_output=True,cwd=d)
        aplicar_trilha(d, out, slug)
    # O YouTube exige capitulo >= 10s e descarta a LISTA INTEIRA se um so
    # violar. Cena tem ~11s e algumas ficam abaixo, entao agrupa: so abre
    # capitulo novo depois de MIN_CAP segundos (o primeiro e sempre 0:00).
    # Prefere abrir no `titulo` (a cena que abre secao neste formato), para o
    # capitulo levar um nome de secao e nao um slide qualquer do meio.
    MIN_CAP, MAX_CAP = 60, 150
    caps, t, ultimo = [], 0.0, -1e9
    for i, c in enumerate(sp["longo"]):
        dt = t - ultimo
        # `sem_cap` marca cenas de passagem (ponte de fim de capitulo): sao
        # layout `titulo` mas o texto delas nao nomeia secao nenhuma, e virava
        # capitulo chamado "Bridge — ...", que nao ajuda ninguem a navegar.
        pode = not c.get("sem_cap")
        if i == 0 or (pode and dt >= MIN_CAP and c.get("layout") == "titulo") or (pode and dt >= MAX_CAP):
            caps.append(f"{int(t//60)}:{int(t%60):02d} {c.get('cap', c.get('kicker','...'))}")
            ultimo = t
        t += tempos[i]
    # Credito CC-BY obrigatorio: sem ele o uso da faixa deixa de ser licenciado.
    faixa = trilha_do_canal(slug)
    credito = "—" if not faixa else (
        f"Music: {os.path.basename(faixa)[:-4].replace('_', ' ')} by Kevin MacLeod "
        "(incompetech.com) — Licensed under Creative Commons: By Attribution 4.0\n"
        "http://creativecommons.org/licenses/by/4.0/")
    copy = sp["copy"].replace("{CAPITULOS}", "\n".join(caps)).replace("{TRILHA}", credito)
    open(f"{d}/copy.md","w").write(copy)
    print(slug, "render ok", round(t))
if __name__ == "__main__":
    fn = sys.argv[1]; spec = sys.argv[2]
    montar(spec) if fn == "montar" else render(spec)