#!/usr/bin/env python3
"""Renderiza a semana do @trafegocomia com as pecas da fabrica deste repo.

Uso:  python3 trafegocomia/render_semana.py trafegocomia/semana-AAAA-MM-DD.json

Usa as funcoes da propria fabrica (svg_cena_retrato, legenda.srt, clipe_cena,
loudnorm do AUDIO_ARGS), mas em 1080x1920 direto, sem upscale: o etapas.py
renderiza o short em 720x1280, e o pedido e 1080x1920.

NAO publica nada. Nao chama publicar.py, retomar.yml nem rede social nenhuma.

A narracao: edge-tts pt-BR-AntonioNeural (masculina). Se o edge falhar tres
vezes, cai no Piper pt_BR-faber-medium (tambem masculina, qualidade menor) pelo
voz_piper da fabrica. O provedor de cada video vai no relatorio.

Duracao: o pedido e 30 a 45 s. O ritmo sai do mais rapido que caiba na faixa
(+12%, depois +6%, +0%); se nenhum cair dentro, o video e gerado assim mesmo e
o relatorio diz em letra que ficou fora.
"""
import asyncio
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))
sys.path.insert(0, os.path.join(RAIZ, "src"))

import cairosvg                      # noqa: E402
import fabrica as F                  # noqa: E402
import legenda as LG                 # noqa: E402

W, H = 1080, 1920
PALETA = {"bg": "#111827", "ink": "#FFFFFF", "c1": "#FFFFFF", "c2": "#1D4ED8"}
VOZ = "pt-BR-AntonioNeural"
RITMOS = ["+12%", "+6%", "+0%"]
FAIXA = (30.0, 45.0)
PAUSA = 0.45  # respiro depois de cada fala

# Legenda grande: o EST da fabrica usa Fontsize=13 (~87 px a 1920 de altura);
# aqui 16 (~107 px), caixa escura atras, sempre visivel, acima da faixa onde
# Reels/TikTok poem botoes.
EST = ("FontName=DejaVu Sans,Fontsize=16,Bold=1,PrimaryColour=&H00FFFFFF,"
       "BorderStyle=3,BackColour=&HC0000000,Outline=2,Shadow=0,"
       "MarginV=60,MarginL=20,MarginR=20")


def edge(texto, rate, alvo):
    import edge_tts
    for _ in range(3):
        try:
            asyncio.run(edge_tts.Communicate(texto, VOZ, rate=rate).save(alvo))
            if os.path.getsize(alvo) > 1000:
                return True
        except Exception as e:                              # noqa: BLE001
            print(f"  edge falhou: {e}", flush=True)
    return False


def piper(texto, alvo):
    import voz_piper as VP
    # a chave Thalita no VOZES mapeia para pt_BR-faber-medium, voz masculina
    return VP.sintetiza(texto, "pt-BR-ThalitaMultilingualNeural", alvo)


def narra(cenas, d, rate):
    """Gera s00.mp3.. Devolve (provedor, duracoes)."""
    prov = set()
    for i, c in enumerate(cenas):
        mp3 = f"{d}/s{i:02d}.mp3"
        if os.path.exists(mp3):
            os.remove(mp3)
        if edge(c["nar"], rate, mp3):
            prov.add("edge")
        elif piper(c["nar"], mp3):
            prov.add("piper")
        else:
            raise RuntimeError(f"sem narracao para a cena {i}: edge e piper falharam")
    durs = [F.dur(f"{d}/s{i:02d}.mp3") + PAUSA for i in range(len(cenas))]
    return "+".join(sorted(prov)), durs


def png(c, alvo):
    cairosvg.svg2png(bytestring=F.svg_cena_retrato(c, PALETA, W, H).encode(),
                     write_to=alvo, output_width=W, output_height=H)


def svg_capa(titulo, n):
    """Capa 1080x1920: titulo grande ancorado pela ULTIMA linha acima do traco
    (subindo=True), para titulo de tres linhas nao atropelar o traco nem o @."""
    bg, ink, acc = PALETA["bg"], PALETA["ink"], PALETA["c2"]
    cx = W // 2
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{bg}"/>')
    s += f'<rect x="0" y="0" width="{W}" height="{H*0.012}" fill="{acc}"/>'
    s += (f'<rect x="{cx-W*0.12}" y="{H*0.20}" width="{W*0.24}" height="{H*0.045}" '
          f'rx="{H*0.022}" fill="{acc}"/>')
    s += F.tsp(f"DICA {n:02d}", cx, H*0.235, W*0.045, ink, n=12)
    s += F.tsp(titulo, cx, H*0.56, W*0.115, ink, n=12, subindo=True,
               largura=W*F.LARGURA_SEGURA)
    s += (f'<rect x="{cx-W*0.30}" y="{H*0.60}" width="{W*0.60}" height="{H*0.008}" '
          f'rx="{H*0.004}" fill="{acc}"/>')
    s += F.tsp("@trafegocomia", cx, H*0.68, W*0.055, ink, n=20)
    return s + "</svg>"


def video(v, n, saida_dir, trab):
    d = os.path.join(trab, f"{n:02d}")
    os.makedirs(d, exist_ok=True)
    cenas = v["cenas"]
    escolhido = None
    for rate in RITMOS:
        prov, durs = narra(cenas, d, rate)
        total = sum(durs)
        print(f"  ritmo {rate}: {total:.1f}s ({prov})", flush=True)
        if FAIXA[0] <= total <= FAIXA[1]:
            escolhido = (rate, prov, durs)
            break
        if total > FAIXA[1]:          # ja passou: mais devagar so piora
            escolhido = (rate, prov, durs)
            break
        escolhido = (rate, prov, durs)
    rate, prov, durs = escolhido
    for i, c in enumerate(cenas):
        dd = durs[i]
        png(c, f"{d}/s{i:02d}.png")
        with open(f"{d}/s{i:02d}.srt", "w") as f:
            f.write(LG.srt(c["nar"], dd))
        F.clipe_cena(d, "s", i, c, dd, max(int(dd * 30), 1), W, H, est=EST)
    with open(f"{d}/lista.txt", "w") as f:
        for i in range(len(cenas)):
            f.write(f"file 'sclip{i:02d}.mp4'\n")
    nome = f"{n:02d}-{v['slug']}"
    mp4 = os.path.join(saida_dir, nome + ".mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-f", "concat", "-safe", "0",
                    "-i", f"{d}/lista.txt", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", mp4], check=True, capture_output=True)
    capa = os.path.join(saida_dir, nome + "-capa.png")
    cairosvg.svg2png(bytestring=svg_capa(v["capa"], n).encode(), write_to=capa,
                     output_width=W, output_height=H)
    ds = F.dur(mp4)
    wh = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                         "-show_entries", "stream=width,height", "-of", "csv=p=0", mp4],
                        capture_output=True, text=True).stdout.strip()
    return {"video": os.path.relpath(mp4, RAIZ), "capa": os.path.relpath(capa, RAIZ),
            "duracao_s": round(ds, 1), "resolucao": wh, "ritmo": rate,
            "provedor": prov, "na_faixa": FAIXA[0] <= ds <= FAIXA[1],
            "cta": cenas[-1]["nar"]}


def main():
    sem = json.load(open(sys.argv[1]))
    saida_dir = os.path.join(RAIZ, "saida", f"semana-{sem['semana']}")
    os.makedirs(saida_dir, exist_ok=True)
    trab = os.environ.get("TRAB", "/tmp/trafegocomia")
    rel = []
    for n, v in enumerate(sem["videos"], 1):
        print(f"video {n:02d} {v['slug']}", flush=True)
        try:
            rel.append(video(v, n, saida_dir, trab))
        except Exception as e:                              # noqa: BLE001
            rel.append({"video": f"{n:02d}-{v['slug']}", "erro": repr(e)[:400]})
            print(f"::error::video {n:02d} falhou: {e}", flush=True)
    with open(os.path.join(saida_dir, "relatorio.json"), "w") as f:
        json.dump(rel, f, ensure_ascii=False, indent=1)
    for r in rel:
        print(json.dumps(r, ensure_ascii=False), flush=True)
    sys.exit(1 if any("erro" in r for r in rel) else 0)


if __name__ == "__main__":
    main()
