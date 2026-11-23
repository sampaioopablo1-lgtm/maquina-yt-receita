#!/usr/bin/env python3
"""Motor v2 do @trafegocomia: tipografia animada sincronizada com a fala.

Uso: python3 produz.py roteiro.json saida.mp4 [capa.png]

1. narra cada cena com edge-tts (pt-BR-AntonioNeural) pedindo WordBoundary,
   logo cada palavra tem o instante exato em que e dita;
2. monta a linha do tempo (cenas + palavras + quando cada item de lista entra);
3. renderiza quadro a quadro o cena.html no Chromium (render.js);
4. mistura voz + efeitos (whoosh na troca de cena, pop nos itens) e normaliza.

Nao publica nada.
"""
import asyncio, json, os, subprocess, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
VOZ, RITMO, GAP = "pt-BR-AntonioNeural", "+12%", 0.22
PROXY = os.environ.get("HTTPS_PROXY") or None


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if c.isalnum() and unicodedata.category(c) != "Mn")


async def narra(texto, mp3):
    kw = dict(rate=RITMO, boundary="WordBoundary")
    if PROXY:
        kw["proxy"] = PROXY
    palavras, audio = [], bytearray()
    for _ in range(3):
        try:
            palavras, audio = [], bytearray()
            async for ch in edge_tts.Communicate(texto, VOZ, **kw).stream():
                if ch["type"] == "audio":
                    audio += ch["data"]
                elif ch["type"] == "WordBoundary":
                    palavras.append({"w": ch["text"], "t": ch["offset"] / 1e7,
                                     "d": ch["duration"] / 1e7})
            if audio:
                break
        except Exception as e:  # noqa: BLE001
            print("edge falhou:", e, flush=True)
    if not audio:
        raise RuntimeError("sem narracao: " + texto)
    open(mp3, "wb").write(audio)
    return palavras


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", f], capture_output=True, text=True).stdout)


def sh(*a):
    subprocess.run(list(a), check=True, capture_output=True)


def main():
    rot, saida = sys.argv[1], sys.argv[2]
    capa = sys.argv[3] if len(sys.argv) > 3 else None
    R = json.load(open(rot))
    tmp = os.path.splitext(saida)[0] + "_trab"
    os.makedirs(tmp, exist_ok=True)
    t, cenas, todas, partes = 0.0, [], [], []
    for i, c in enumerate(R["cenas"]):
        mp3 = f"{tmp}/n{i:02d}.mp3"
        ws = asyncio.run(narra(c["nar"], mp3))
        d = dur(mp3)
        c2 = dict(c, t0=round(t, 3))
        for w in ws:
            todas.append({"w": w["w"], "t": round(t + w["t"], 3), "d": round(w["d"], 3)})
        if c.get("list"):
            lt = []
            for it in c["list"]:
                alvo = norm(it.split()[0])
                hit = next((w for w in ws if norm(w["w"]).startswith(alvo[:5])), None)
                lt.append(round(t + hit["t"] - 0.05, 3) if hit else None)
            c2["list_t"] = lt
        if c.get("vs"):
            vt, desde = [], 0
            for it in c["vs"]:
                alvo = norm(it["r"].split()[0])
                k = next((k for k in range(desde, len(ws)) if norm(ws[k]["w"]).startswith(alvo[:5])), None)
                vt.append(round(t + ws[k]["t"], 3) if k is not None else None)
                if k is not None:
                    desde = k + 1
            c2["vs_t"] = vt
        cenas.append(c2)
        partes.append((mp3, d))
        t += d + GAP
    total = round(t + 0.6, 3)
    tl = {"cenas": cenas, "palavras": todas, "total": total, "tema": R.get("tema")}
    json.dump(tl, open(f"{tmp}/timeline.json", "w"), ensure_ascii=False)

    # voz em uma faixa, com o mesmo espacamento da linha do tempo
    with open(f"{tmp}/voz.txt", "w") as f:
        for mp3, d in partes:
            f.write(f"file '{os.path.abspath(mp3)}'\n")
    sil = f"{tmp}/gap.wav"
    sh("ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono",
       "-t", str(GAP), sil)
    filtro, ins = [], []
    for k, (mp3, d) in enumerate(partes):
        ins += ["-i", mp3]
    n = len(partes)
    cat = "".join(f"[{k}:a]aresample=48000,apad=pad_dur={GAP}[a{k}];" for k in range(n))
    cat += "".join(f"[a{k}]" for k in range(n)) + f"concat=n={n}:v=0:a=1[v]"
    sh("ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", cat, "-map", "[v]",
       "-ac", "1", f"{tmp}/voz.wav")

    # efeitos: whoosh nas trocas de cena, pop nos itens de lista
    sh("ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
       "anoisesrc=color=pink:d=0.45:a=0.6", "-af",
       "highpass=f=400,lowpass=f=6000,afade=t=in:d=0.25,afade=t=out:st=0.25:d=0.2,volume=0.5",
       "-ar", "48000", "-ac", "1", f"{tmp}/whoosh.wav")
    sh("ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "sine=f=1200:d=0.09",
       "-af", "afade=t=out:st=0.01:d=0.08,volume=0.5", "-ar", "48000", "-ac", "1", f"{tmp}/pop.wav")
    eventos = [("whoosh", c["t0"] - 0.18) for c in cenas[1:]]
    for c in cenas:
        for x in c.get("list_t") or []:
            if x is not None:
                eventos.append(("pop", x))
    ins, mix = ["-i", f"{tmp}/voz.wav"], ["[0:a]"]
    for k, (nome, at) in enumerate(eventos, 1):
        ins += ["-i", f"{tmp}/{nome}.wav"]
        ms = max(0, int(at * 1000))
        mix.append(f"[s{k}]")
    fc = ";".join(f"[{k}:a]adelay={max(0,int(at*1000))}|{max(0,int(at*1000))}[s{k}]"
                  for k, (_, at) in enumerate(eventos, 1))
    fc += ";" + "".join(mix) + f"amix=inputs={len(mix)}:normalize=0,apad=whole_dur={total}," \
          "loudnorm=I=-14:TP=-1.5:LRA=11[a]"
    sh("ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", fc, "-map", "[a]",
       "-ar", "48000", "-ac", "2", f"{tmp}/audio.wav")

    env = dict(os.environ, FONTES_DIR=os.environ.get("FONTES_DIR",
               os.path.join(AQUI, "..", "fontes")))  # Montserrat no repo (OFL): sessao nova nao tem node_modules
    subprocess.run(["node", os.path.join(AQUI, "render.js"), f"{tmp}/timeline.json",
                    f"{tmp}/mudo.mp4"], check=True, env=env)
    sh("ffmpeg", "-y", "-v", "error", "-i", f"{tmp}/mudo.mp4", "-i", f"{tmp}/audio.wav",
       "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", saida)
    if capa:
        subprocess.run(["node", os.path.join(AQUI, "render.js"), f"{tmp}/timeline.json",
                        capa, "0.5"], check=True, env=env)
    print(json.dumps({"video": saida, "duracao": round(dur(saida), 1), "capa": capa}))


if __name__ == "__main__":
    import edge_tts  # noqa: E402
    main()
