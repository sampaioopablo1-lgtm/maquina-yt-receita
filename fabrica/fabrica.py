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

# Fonte do canal. O padrao cobre latino, grego e cirilico, mas nao tem
# devanagari: em hindi o cairosvg desenhava os glifos soltos (o halant ficava
# visivel e a matra caia do lado errado) e a legenda queimada saia VAZIA, porque
# nao havia nenhuma fonte com o script instalada. Specs em hindi declaram
# "fonte": "Noto Sans Devanagari", e ai os dois motores passam a shapear.
FONTE = "DejaVu Sans"

def tsp(t, x, y, size, fill, n=30, anchor='middle', lh=1.25):
    o = f'<text x="{x}" y="{y}" font-family="{FONTE}" font-weight="bold" font-size="{int(size)}" fill="{fill}" text-anchor="{anchor}">'
    for i, l in enumerate(wrap(t, n)):
        o += f'<tspan x="{x}" dy="{0 if i==0 else int(size*lh)}">{esc(l)}</tspan>'
    return o + '</text>'

def usar_fonte(nome):
    """Troca a fonte do canal e CONFERE que ela existe. Sem a conferencia, uma
    fonte ausente nao da erro: o SVG cai num fallback qualquer e a legenda
    queimada sai vazia — defeito que so aparece assistindo ao video pronto.
    A fonte vive em ~/.fonts do sandbox, entao some quando ele recicla."""
    global FONTE, EST
    if not nome:
        return
    fams = subprocess.run(["fc-list","--format=%{family}\n"], capture_output=True, text=True).stdout
    if nome not in fams:
        raise RuntimeError(
            f"fonte '{nome}' nao instalada no sandbox. Instale em ~/.fonts e rode fc-cache -f. "
            "Sem ela a legenda queimada sai VAZIA e o texto de tela sai sem shaping.")
    EST = EST.replace(f"FontName={FONTE}", f"FontName={nome}")
    FONTE = nome

def elementos(c):
    """Quantos elementos desta cena entram em cena separadamente.

    Zero significa cena de uma peca so — ela vai inteira no fundo. Acima de
    zero, `svg_cena(..., camada=k)` devolve o k-esimo elemento sozinho, sobre
    tela transparente, e quem monta o clipe faz cada um entrar no seu tempo.
    """
    lay = c.get('layout', 'titulo')
    if lay in ('lista', 'barras'):
        return len(c.get('itens', []))
    if lay in ('titulo', 'cta'):
        return 2 if c.get('sub') else 1
    if lay == 'item':
        return 2 if c.get('preco') else 1
    return 0


def svg_cena_retrato(c, pal, W, H):
    """Cena 9:16 com geometria propria, dimensionada pela LARGURA.

    O svg_cena dimensiona fonte e formas por H, que em paisagem e o lado
    menor. Em retrato H e o lado MAIOR: o circulo do layout `item` saia com
    borda esquerda em x negativo e o kicker de `titulo` nao cabia na largura.
    O visual.py pegou 6/6 quadros do short com tinta na borda (3-6,3%) — e os
    shorts anteriores foram publicados assim, porque so o longo era conferido.
    Medido no kp-plan-9233: esta geometria devolve margem 0,00%.
    """
    ink, c1, c2 = pal['ink'], pal['c1'], pal['c2']
    bg = pal.get('bg', '#FFFFFF'); lay = c.get('layout', 'titulo')
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
    s += f'<rect width="{W}" height="{H}" fill="{bg}"/>'
    cx = W // 2
    if lay in ('titulo', 'cta'):
        fg = c1 if lay == 'titulo' else c2
        big = c.get('kicker', '')
        s += tsp(big, cx, H*0.40, W*(0.15 if len(big) <= 8 else 0.10), fg, n=11)
        s += f'<path d="M {cx-W*0.30} {H*0.50} Q {cx} {H*0.52}, {cx+W*0.30} {H*0.50}" stroke="{c2 if lay=="titulo" else c1}" stroke-width="9" fill="none" stroke-linecap="round"/>'
        if c.get('sub'):
            s += tsp(c['sub'], cx, H*0.58, W*0.055, ink, n=22)
    elif lay == 'item':
        s += f'<circle cx="{cx}" cy="{H*0.28}" r="{W*0.24}" fill="none" stroke="{ink}" stroke-width="8"/>'
        s += f'<circle cx="{cx}" cy="{H*0.28}" r="{W*0.15}" fill="{c2}" opacity="0.55"/>'
        s += tsp(c.get('kicker', ''), cx, H*0.50, W*0.085, ink, n=14)
        if c.get('preco'):
            s += f'<rect x="{cx-W*0.26}" y="{H*0.56}" width="{W*0.52}" height="{H*0.075}" fill="{c1}"/>'
            s += tsp(c['preco'], cx, H*0.615, W*0.075, '#FFFFFF', n=12)
    elif lay == 'lista':
        s += tsp(c.get('kicker', ''), cx, H*0.16, W*0.08, ink, n=16)
        y = H * 0.30
        for i, it in enumerate(c.get('itens', [])):
            col = [c1, c2, ink][i % 3]
            s += f'<circle cx="{W*0.12}" cy="{y-H*0.012}" r="{W*0.022}" fill="{col}"/>'
            s += tsp(it, W*0.18, y, W*0.055, ink, n=26, anchor='start')
            y += H * 0.10
    elif lay == 'barras':
        labs = c.get('itens', ['1', '2', '3', '4']); n = len(labs); bw = W*0.76/n
        alt = c.get('alturas')
        s += tsp(c.get('kicker', ''), cx, H*0.14, W*0.08, ink, n=16)
        s += f'<line x1="{W*0.10}" y1="{H*0.60}" x2="{W*0.90}" y2="{H*0.60}" stroke="{ink}" stroke-width="3" opacity="0.35"/>'
        for i, lb in enumerate(labs):
            bh = (H*0.06 + (alt[i]/max(alt))*H*0.28) if alt else (H*0.06 + i*H*0.28/max(n-1, 1))
            x = W*0.12 + i*bw
            s += f'<rect x="{x}" y="{H*0.60-bh}" width="{bw*0.72}" height="{bh}" fill="{[c1,c2,ink][i%3]}"/>'
            s += tsp(str(lb), x+bw*0.36, H*0.65, W*0.035, ink, n=12)
    return s + '</svg>'


def svg_cena(c, pal, W, H, camada=None):
    """camada=None: a cena inteira (comportamento historico, e o do short).
    camada='base': so o fundo e o que nao se move.
    camada=k (0-based): so o k-esimo elemento, sobre fundo transparente.

    Existe porque a cena estatica era o defeito de retencao mais visivel do
    formato: quatro itens de uma lista apareciam juntos e ficavam parados os
    dez segundos inteiros em que o narrador os percorre um a um. Com os
    elementos entrando no tempo da fala, o olho tem motivo para continuar.

    Retrato (short 9:16) desvia para svg_cena_retrato: a geometria daqui e
    16:9 e estoura as bordas laterais quando H > W.
    """
    if H > W and camada is None:
        return svg_cena_retrato(c, pal, W, H)
    ink, c1, c2 = pal['ink'], pal['c1'], pal['c2']
    bg = pal.get('bg', '#FFFFFF'); lay = c.get('layout','titulo')

    def quer(k):
        """Este elemento entra nesta camada?"""
        if camada is None:
            return True
        if camada == 'base':
            return k is None      # k=None marca o mobiliario fixo da cena
        return k == camada

    fundo = (camada is None or camada == 'base')
    # A cena de CTA invertia o fundo (escuro com texto claro). Como sao as tres
    # ultimas de cada video, a virada de cor no fim lia como defeito de render,
    # nao como cartao de encerramento. Agora o CTA segue a identidade do canal.
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
    if fundo:
        s += f'<rect width="{W}" height="{H}" fill="{bg}"/>'
    cx = W//2
    if lay in ('titulo','cta'):
        fg = c1 if lay=='titulo' else c2
        # sub_fg era branco no cta — o que so funcionava com o fundo invertido.
        # Sem a inversao, branco sobre fundo claro sumia por completo.
        sub_fg = ink
        big = c.get('kicker','')
        if quer(0):
            s += tsp(big, cx, H*0.40, H*(0.15 if len(big)<=10 else 0.09), fg, n=16)
            s += f'<path d="M {cx-W*0.26} {H*0.52} Q {cx} {H*0.55}, {cx+W*0.26} {H*0.52}" stroke="{c2 if lay=="titulo" else c1}" stroke-width="10" fill="none" stroke-linecap="round"/>'
        if c.get('sub') and quer(1):
            s += tsp(c['sub'], cx, H*0.65, H*0.055, sub_fg, n=30)
    elif lay == 'lista':
        if quer(None):
            s += tsp(c.get('kicker',''), cx, H*0.18, H*0.08, ink, n=24)
        y = H*0.38
        for i, it in enumerate(c.get('itens', [])):
            if quer(i):
                col = [c1, c2, ink][i%3]
                s += f'<circle cx="{W*0.16}" cy="{y-H*0.02}" r="{H*0.025}" fill="{col}"/>'
                s += tsp(it, W*0.21, y, H*0.055, ink, n=36, anchor='start')
            y += H*0.17
    elif lay == 'barras':
        labs = c.get('itens', ['1','2','3','4']); n = len(labs); bw = W*0.64/n
        alt = c.get('alturas')
        if quer(None):
            s += tsp(c.get('kicker',''), cx, H*0.16, H*0.08, ink, n=24)
            # A linha de base fica no fundo: e o chao contra o qual as barras
            # sobem, e sem ela as primeiras parecem flutuar no vazio.
            s += f'<line x1="{W*0.15}" y1="{H*0.82}" x2="{W*0.85}" y2="{H*0.82}" stroke="{ink}" stroke-width="3" opacity="0.35"/>'
        for i, lb in enumerate(labs):
            if not quer(i):
                continue
            bh = (H*0.12 + (alt[i]/max(alt))*H*0.48) if alt else (H*0.12 + i*H*0.48/max(n-1,1))
            x = W*0.18 + i*bw
            s += f'<rect x="{x}" y="{H*0.82-bh}" width="{bw*0.72}" height="{bh}" fill="{[c1,c2,ink][i%3]}"/>'
            s += tsp(str(lb), x+bw*0.36, H*0.90, H*0.038, ink, n=14)
    elif lay == 'item':
        if quer(None):
            s += f'<circle cx="{W*0.27}" cy="{H*0.55}" r="{H*0.22}" fill="none" stroke="{ink}" stroke-width="9"/>'
            s += f'<circle cx="{W*0.27}" cy="{H*0.55}" r="{H*0.14}" fill="{c2}" opacity="0.55"/>'
        if quer(0):
            s += tsp(c.get('kicker',''), W*0.63, H*0.36, H*0.07, ink, n=20)
        if c.get('preco') and quer(1):
            s += f'<rect x="{W*0.51}" y="{H*0.5}" width="{W*0.24}" height="{H*0.13}" fill="{c1}"/>'
            s += tsp(c['preco'], W*0.63, H*0.59, H*0.06, '#FFFFFF', n=12)
    return s + '</svg>'

def dur(f):
    return _duracao(f)

def st(x):
    return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{x%60:06.3f}".replace(".",",")

async def vozes(cenas, voz, pref, d):
    for i, c in enumerate(cenas):
        alvo = f"{d}/{pref}{i:02d}.mp3"
        # RETOMA: mp3 valido nao se refaz — cada restart pos-crash custava
        # ~10 min de TTS refeito do zero.
        if os.path.exists(alvo) and os.path.getsize(alvo) > 1000:
            continue
        # O websocket do edge-tts ja pendurou sem erro nem timeout (15 min
        # parado na cena 82 do setiap-006). wait_for + 3 tentativas.
        for tentativa in range(3):
            try:
                com = edge_tts.Communicate(c["nar"], voz, rate="-4%")
                await asyncio.wait_for(com.save(alvo), timeout=90)
                if os.path.getsize(alvo) > 1000:
                    break
                raise RuntimeError(f"mp3 vazio: {alvo}")
            except Exception:
                try:
                    os.remove(alvo)
                except OSError:
                    pass
                if tentativa == 2:
                    raise

def dir_trabalho(sp):
    """Diretorio de trabalho do PACOTE, nao do canal.

    O 'slug' da spec e o do canal — ele escolhe a trilha. Usar o mesmo slug como
    diretorio faz dois pacotes do mesmo canal dividirem a mesma pasta, e ai o
    RETOMA pula clipes do pacote ANTERIOR: sai um video costurando dois roteiros
    sem erro nenhum. Specs novas declaram "pacote"; as antigas seguem no slug.

    Raiz configuravel via FABRICA_WORKDIR — o default /tmp/f mora no tmpfs do
    sandbox (985 MB de RAM total) e um render de 130+ cenas mata o ffmpeg por
    OOM perto do clipe 40 (~250 MB por clipe de 4 camadas). Apontar para disco
    real (ex.: /home/user/frender/f, ext4) resolve sem mexer no resto da
    fabrica: FABRICA_WORKDIR=/home/user/frender/f python3 etapas.py <spec>.
    """
    raiz = os.environ.get("FABRICA_WORKDIR", "/tmp/f")
    return f"{raiz}/{sp.get('pacote') or sp['slug']}"


def montar(spec_file):
    sp = json.load(open(spec_file))
    usar_fonte(sp.get("fonte"))
    slug, pal, voz = sp["slug"], sp["paleta"], sp["voz"]
    d = dir_trabalho(sp); os.makedirs(d, exist_ok=True)
    for pref, cenas, W, H in (("l", sp["longo"], 1280, 720), ("s", sp["short"], 720, 1280)):
        for i, c in enumerate(cenas):
            # O longo entra em camadas (base + um png por elemento). O short
            # nao: sao 30s com legenda queimada, e ali a entrada escalonada
            # rouba tempo de leitura em vez de dar ritmo.
            if pref == "l":
                cairosvg.svg2png(bytestring=svg_cena(c, pal, W, H, camada='base').encode(),
                                 write_to=f"{d}/{pref}{i:02d}.png", output_width=W, output_height=H)
                for k in range(elementos(c)):
                    cairosvg.svg2png(bytestring=svg_cena(c, pal, W, H, camada=k).encode(),
                                     write_to=f"{d}/{pref}{i:02d}_{k}.png",
                                     output_width=W, output_height=H)
            else:
                cairosvg.svg2png(bytestring=svg_cena(c, pal, W, H).encode(),
                                 write_to=f"{d}/{pref}{i:02d}.png", output_width=W, output_height=H)
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

def trilha_ok(f):
    """Um download que falhou vira um .mp3 com HTML dentro. Ele passa no glob,
    passa no teste de tamanho, e so estoura no ffprobe — depois de a fabrica ja
    ter gasto o render inteiro. Entao valida decodificando de verdade."""
    try:
        return dur(f) > 30
    except Exception:
        return False

def trilha_do_canal(slug):
    """Faixa fixa por canal = assinatura sonora. CC-BY, credito no copy.md."""
    import glob
    fs = [f for f in sorted(glob.glob(f"{TRILHA_DIR}/*.mp3")) if trilha_ok(f)]
    return fs[sum(map(ord, slug)) % len(fs)] if fs else None

# Escala de render: o sandbox tem ~1GB de RAM e o zoompan e o maior consumidor.
# Renderiza menor, entrega em HD (upscale no concat, passe unico).
ESCALA_RENDER = 0.75
# Amplitude do Ken Burns por cena (7% = perceptivel sem cortar a arte).
AMP_ZOOM = 0.12
# Fracao da margem disponivel que o pan percorre. 1.0 encostaria na borda e
# cortaria ate 11% de um dos lados — o suficiente para comer o fim de um item
# de lista. 0.5 mantem o enquadramento centrado e ainda da deslocamento visivel.
AMP_PAN = 0.5


def ken_burns(i, nf):
    """Zoom + pan em 4 direcoes alternadas, em funcao de `on` (numero do frame).

    Retorna (expressao de zoom, fracao horizontal, fracao vertical). As fracoes
    valem 0 a 1 sobre a margem que o zoom abriu; 0.5 e o centro. Alternar em 4
    (nao em 2) evita que cenas vizinhas facam o mesmo movimento espelhado, que
    o olho le como repeticao.
    """
    p = f"on/{nf}"
    dentro = f"1+{AMP_ZOOM}*{p}"
    fora = f"{1 + AMP_ZOOM:.4g}-{AMP_ZOOM}*{p}"
    meio = 0.5
    ini = (1 - AMP_PAN) / 2                      # 0.25
    varre = f"{ini}+{AMP_PAN}*{p}"               # 0.25 -> 0.75
    volta = f"{ini + AMP_PAN}-{AMP_PAN}*{p}"     # 0.75 -> 0.25
    return [
        (dentro, varre, meio),   # aproxima varrendo para a direita
        (fora,   volta, meio),   # afasta varrendo para a esquerda
        (dentro, meio,  varre),  # aproxima descendo
        (fora,   meio,  volta),  # afasta subindo
    ][i % 4]
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
        # Num pacote escalonado (25-30 min) o audio passa a dominar o arquivo:
        # 192k por 26 min ja da ~37 MB e o video inteiro nao cabe no limite de
        # 50 MB do upload padrao do Supabase. Para narracao com trilha a -28 dB,
        # 128k e indistinguivel e devolve ~7 MB.
        "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac",
        "-b:a", "192k" if dv < 1100 else "128k", "-ac","2","-ar","48000",
        "-t",f"{dv:.2f}","-movflags","+faststart",mix],check=True,capture_output=True)
    os.replace(mix, alvo)
    os.remove(bed)

# MarginL/R forcam a quebra de linha antes da caixa encostar nas laterais do
# 9:16 — sem eles a legenda queimada tocava as duas bordas em TODO quadro do
# short (medido pelo visual.py: 3-6,3% de tinta na borda; com margens, 0,00%).
EST = f"FontName={FONTE},Fontsize=13,Bold=1,PrimaryColour=&H00FFFFFF,BorderStyle=3,BackColour=&HB0000000,Outline=1,Shadow=0,MarginV=36,MarginL=18,MarginR=18"

def render(spec_file):
    sp = json.load(open(spec_file)); slug = sp["slug"]
    usar_fonte(sp.get("fonte"))
    d = dir_trabalho(sp)
    tempos = []
    for pref, cenas, W, H in (("l", sp["longo"], 1280, 720), ("s", sp["short"], 720, 1280)):
        for i, c in enumerate(cenas):
            # A checagem do RETOMA vem ANTES de medir o mp3: quando os lotes ja
            # renderizaram tudo, o png/mp3 foi apagado para caber no tmpfs, e
            # medir aqui quebrava o render inteiro num clipe que ja existia.
            saida = f"{d}/{pref}clip{i:02d}.mp4"  # RETOMA
            if os.path.exists(saida) and os.path.getsize(saida) > 10000:
                continue
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
            z, fx, fy = ken_burns(i, nf)
            # x/y ficavam presos no centro, entao o movimento era zoom puro de
            # 7% em ~10s — imperceptivel, o video lia como imagem parada. Agora
            # ha deslocamento de verdade, em 4 direcoes alternadas.
            vf = (f"zoompan=z='{z}':d={nf}"
                  f":x='(iw-iw/zoom)*({fx})':y='(ih-ih/zoom)*({fy})'"
                  f":s={RW}x{RH}:fps=30")
            # Legenda queimada so no short. No longo ela rouba area util e
            # impede a legenda propria do YouTube (que traduz e e indexada);
            # o pacote entrega um .srt para subir junto, melhor que a automatica.
            if pref == "s":
                vf += f",subtitles={d}/{pref}{i:02d}.srt:force_style='{EST}'"
            clipe_cena(d, pref, i, c, dd, nf, RW, RH)
            # MANIFESTO: checkpoint por clipe — uma falha nunca custa o pacote
            with open(f"{d}/manifesto.txt","a") as mf:
                mf.write(f"{pref}clip{i:02d}.mp4\n")
        # Os tempos dos capitulos saem do clipe RENDERIZADO, nunca do mp3: o mp3
        # e a narracao crua, e a cena tem folga no fim. Estimar pelo mp3 dava um
        # erro que se acumulava cena a cena (+23s no fim de um video de 12 min),
        # jogando os capitulos do fim para depois do trecho que nomeiam.
        if pref == "l":
            tempos = [dur(f"{d}/lclip{i:02d}.mp4") for i in range(len(cenas))]
            # Legenda de verdade para subir no Studio. Sai dos clipes
            # renderizados, entao bate ao milissegundo com o video final —
            # e e melhor que a automatica do YouTube, que erra nomes proprios
            # e numeros justamente onde este formato se apoia.
            with open(f"{d}/legendas.srt", "w", encoding="utf-8") as srt:
                t = 0.0
                for i, c in enumerate(cenas):
                    fim = t + tempos[i]
                    srt.write(f"{i+1}\n{st(t + 0.15)} --> {st(fim - 0.15)}\n{c['nar']}\n\n")
                    t = fim
        with open(f"{d}/{pref}lista.txt","w") as f:
            for i in range(len(cenas)): f.write(f"file '{pref}clip{i:02d}.mp4'\n")
        out = "video.mp4" if pref=="l" else "short.mp4"
        RW, RH = render_wh(W, H)
        args = [ffmpeg_bin(),"-nostdin","-y","-f","concat","-safe","0","-i",f"{d}/{pref}lista.txt"]
        if (RW, RH) != (W, H):
            # Aqui nao ha zoompan, entao da para usar um preset eficiente sem
            # risco de OOM: `ultrafast` gerava 178 MB em 12 min (6x maior que
            # o necessario) e estourava o limite de upload de 50 MB.
            # E o CRF sobe nos pacotes escalonados pelo mesmo motivo: em arte
            # vetorial chapada com zoom lento, crf 29 e visualmente igual a 26.
            crf = "26" if pref != "l" or sum(dur(f"{d}/lclip{i:02d}.mp4") for i in range(len(cenas))) < 1100 else "29"
            args += ["-vf",f"scale={W}:{H}:flags=lanczos","-c:v","libx264","-preset","veryfast","-crf",crf,"-pix_fmt","yuv420p","-c:a","copy"]
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

# --------------------------------------------------------------- animacao
ENTRADA = 0.40      # segundos que cada elemento leva para entrar
DESLIZE = 26        # pixels que ele sobe enquanto entra
INICIO = 0.45       # atraso do primeiro elemento, para a cena assentar
OCUPA = 0.62        # fracao da cena em que todos ja entraram


def tempos_entrada(n, dd):
    """Quando cada um dos n elementos entra, numa cena de dd segundos.

    Espalha as entradas pelos primeiros 62% da cena. Nao ha alinhamento por
    palavra — nao temos timestamp do TTS — mas o narrador percorre a lista na
    mesma ordem e no mesmo ritmo, entao a coincidencia e boa o bastante para o
    olho e muito melhor do que tudo aparecer junto.
    """
    if n <= 0:
        return []
    fim = max(INICIO + ENTRADA, dd * OCUPA)
    if n == 1:
        return [INICIO]
    passo = (fim - INICIO) / (n - 1)
    return [INICIO + i * passo for i in range(n)]


def filtro_camadas(n, dd, i_cena, nf, RW, RH):
    """Monta o filter_complex: base + n camadas entrando, e o Ken Burns no fim.

    Cada camada e uma tela transparente do tamanho do quadro, entao o overlay
    vai em x=0 e so o y anima — nao ha coordenada para acertar aqui, o SVG ja
    colocou o elemento no lugar certo.
    """
    z, fx, fy = ken_burns(i_cena, nf)
    if n == 0:
        return (f"[0:v]zoompan=z='{z}':d={nf}:x='(iw-iw/zoom)*({fx})'"
                f":y='(ih-ih/zoom)*({fy})':s={RW}x{RH}:fps=30[v]")
    partes, atual = [], "0:v"
    for k, t0 in enumerate(tempos_entrada(n, dd)):
        partes.append(f"[{k+1}:v]format=rgba,fade=in:st={t0:.2f}:d={ENTRADA}:alpha=1[a{k}]")
        y = f"{DESLIZE}*max(0\\,1-(t-{t0:.2f})/{ENTRADA})"
        partes.append(f"[{atual}][a{k}]overlay=x=0:y='{y}':format=auto[o{k}]")
        atual = f"o{k}"
    partes.append(f"[{atual}]zoompan=z='{z}':d=1:x='(iw-iw/zoom)*({fx})'"
                  f":y='(ih-ih/zoom)*({fy})':s={RW}x{RH}:fps=30[v]")
    return ";".join(partes)


def clipe_cena(d, pref, i, c, dd, nf, RW, RH, est=None):
    """Renderiza UM clipe de cena. Fonte unica para fabrica.render e etapas.py.

    Existe porque o etapas.py mantinha a propria copia deste loop, e as duas
    saiam do lugar sem avisar: a composicao em camadas entrou aqui e o etapas.py
    continuou no caminho antigo de zoompan sobre imagem unica. O pacote sairia
    sem animacao nenhuma, e nada acusaria — o video tem a duracao certa, o
    tamanho certo e passa em todos os asserts.
    """
    saida = f"{d}/{pref}clip{i:02d}.mp4"
    n_cam = elementos(c) if pref == "l" else 0
    if n_cam:
        args = [ffmpeg_bin(), "-nostdin", "-y",
                "-framerate", "30", "-loop", "1", "-t", f"{dd:.2f}",
                "-i", f"{d}/{pref}{i:02d}.png"]
        for k in range(n_cam):
            args += ["-framerate", "30", "-loop", "1", "-t", f"{dd:.2f}",
                     "-i", f"{d}/{pref}{i:02d}_{k}.png"]
        args += ["-i", f"{d}/{pref}{i:02d}.mp3",
                 "-filter_complex", filtro_camadas(n_cam, dd, i, nf, RW, RH),
                 "-map", "[v]", "-map", f"{n_cam+1}:a"]
    else:
        z, fx, fy = ken_burns(i, nf)
        vf = (f"zoompan=z='{z}':d={nf}:x='(iw-iw/zoom)*({fx})'"
              f":y='(ih-ih/zoom)*({fy})':s={RW}x{RH}:fps=30")
        if pref == "s":
            vf += f",subtitles={d}/{pref}{i:02d}.srt:force_style='{est or EST}'"
        args = [ffmpeg_bin(), "-nostdin", "-y", "-loop", "1",
                "-i", f"{d}/{pref}{i:02d}.png", "-i", f"{d}/{pref}{i:02d}.mp3",
                "-vf", vf]
    subprocess.run(args + ["-t", f"{dd:.2f}", "-c:v", "libx264",
                           "-preset", "ultrafast", "-crf", "23",
                           "-pix_fmt", "yuv420p", *AUDIO_ARGS, saida],
                   check=True, capture_output=True)
    return saida
