#!/usr/bin/env python3
"""Roda a esteira INTEIRA sem TTS, para achar defeito de render antes do runner.

O prontidao.py responde se a spec passa nos portoes ESTATICOS. Ele nao responde
a pergunta que custa caro: o `etapas.py` chega ao fim com esta spec? Entre um e
outro estao a rasterizacao em camadas, a montagem de cada clipe, o zoompan, a
mixagem da trilha, o loudnorm, o srt, o copy.md e os dois testes visuais — e
qualquer um deles pode quebrar numa spec especifica, depois de doze minutos de
render, dentro de um runner que so existe enquanto o job vive.

Aqui a narracao e substituida por silencio com a DURACAO que o TTS produziria
(chars dividido pela taxa medida da voz). Todo o resto e real: os mesmos PNG, o
mesmo ffmpeg, os mesmos asserts, o mesmo visual.py sobre o video pronto.

O que este ensaio NAO cobre, e e bom dizer: a voz em si, a pronuncia de numero
por extenso, e o desvio entre a duracao estimada e a real. Ele cobre o que
quebra o pipeline, nao o que estraga o audio.

SEGURANCA: o ensaio roda numa raiz propria (/tmp/ensaio por padrao, nunca
/tmp/f) e deixa um arquivo ENSAIO-NAO-PUBLICAR ao lado dos artefatos. Video
mudo publicado seria pior que video nenhum, e a unica coisa que separa um do
outro e o diretorio.

Uso:
    python3 fabrica/ensaio.py <spec.json> [<spec.json> ...]
"""
from __future__ import annotations

import glob
import json
import os
import subprocess
import sys
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAIZ_ENSAIO = os.environ.get("ENSAIO_WORKDIR", "/tmp/ensaio")
MARCA = "ENSAIO-NAO-PUBLICAR"

# Taxas MEDIDAS, todas as onze vozes do portfolio, rate=-4%, numeros por
# extenso. As oito ultimas sairam de uma bateria unica no sandbox Composio em
# 13/08/2026; as tres primeiras vieram dos configs de canal.
#
# Por que isto importa mais do que parece: eu usava 14,50 como padrao e a taxa
# real varia de 10,75 (hindi) a 17,60 (indonesio) — 64% de diferenca entre as
# pontas. Com o padrao errado a agla-level-003 media 8:30 e o short 26s, e eu
# quase reescrevi um roteiro que estava certo: com a taxa medida ela e 11,1 min
# e o short 34s, dentro da faixa.
TAXA_CHARS_S = {
    # dos configs de canal
    "pt-BR-AntonioNeural": 14.30,
    "pt-BR-ThalitaMultilingualNeural": 16.52,
    "id-ID-GadisNeural": 14.37,
    # medidas em 13/08/2026 (chars / duracao do mp3 de teste)
    "hi-IN-MadhurNeural": 10.75,     #  98 chars / 9,120 s
    "tr-TR-AhmetNeural": 13.32,      #  94 chars / 7,056 s
    "es-MX-DaliaNeural": 15.94,      # 114 chars / 7,152 s
    "en-GB-RyanNeural": 16.72,       # 120 chars / 7,176 s
    "pl-PL-MarekNeural": 16.75,      # 119 chars / 7,104 s
    "en-US-AndrewNeural": 17.21,     # 121 chars / 7,032 s
    "el-GR-NestorasNeural": 17.40,   # 119 chars / 6,840 s
    "id-ID-ArdiNeural": 17.60,       # 117 chars / 6,648 s
    "pt-BR-FranciscaNeural": 15.51,  # 131 chars / 8,448 s
}
# Com esta, as TREZE vozes do portfolio estao medidas. Nenhum canal fica com
# orcamento de caracteres chutado — que foi como um roteiro de 11,1 min
# apareceu como 8:30 e quase virou reescrita.
# Voz nova entra medida, nunca estimada. Este valor existe so para o ensaio nao
# abortar; ele NAO serve para dimensionar roteiro.
TAXA_PADRAO = 14.50


def taxa(voz: str) -> float:
    return TAXA_CHARS_S.get(voz, TAXA_PADRAO)


def _ffmpeg(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


# Ruido inaudivel, NAO silencio digital. `anullsrc` produz amostras exatamente
# zero, e o loudnorm=I=-14 da esteira precisa de ganho infinito para levar zero
# a -14 LUFS: o encoder AAC recebe NaN/Inf e o clipe morre com "Input contains
# (near) NaN/+-Inf".
#
# Medido em 13/08/2026: com anullsrc a agla-level-003 quebrou na cena 65 de 72,
# e o game-money-lab-002 passou inteiro — a falha depende do trecho, entao um
# ensaio com silencio puro reprova specs BOAS de forma intermitente, que e o
# pior defeito possivel numa ferramenta de conferencia.
#
# -60 dBFS e inaudivel e da ao loudnorm um sinal finito para medir.
AMPLITUDE = 0.001   # ~-60 dBFS


def silencio(segundos: float, alvo: str) -> None:
    """mp3 de duracao exata com ruido inaudivel. lavfi nao precisa de rede."""
    _ffmpeg(["-f", "lavfi",
             "-i", f"anoisesrc=r=24000:c=pink:a={AMPLITUDE}",
             "-t", f"{max(segundos, 0.4):.3f}", "-ac", "1", "-q:a", "9", alvo])


def trilhas_falsas(destino: str) -> int:
    """As quatro faixas, para trilha_do_canal escolher a MESMA da producao.

    Ela escolhe por hash do slug sobre os arquivos presentes: com um
    subconjunto, o canal receberia outra faixa e o ensaio validaria uma mixagem
    que nao e a que vai ao ar.
    """
    os.makedirs(destino, exist_ok=True)
    n = 0
    for faixa in ("Wholesome", "Inspired", "Deliberate_Thought", "Cipher2"):
        alvo = os.path.join(destino, f"{faixa}.mp3")
        if not os.path.exists(alvo):
            silencio(30.0, alvo)
        n += 1
    return n


def prepara(spec_caminho: str) -> str:
    sp = json.load(open(spec_caminho, encoding="utf-8"))
    pacote = sp.get("pacote") or sp["slug"]
    d = os.path.join(RAIZ_ENSAIO, pacote)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, MARCA), "w").write(
        "Os mp3 deste diretorio sao SILENCIO. Nada daqui vai ao ar.\n"
    )

    t = taxa(sp["voz"])
    feitos = 0
    for pref, bloco in (("l", "longo"), ("s", "short")):
        for i, c in enumerate(sp.get(bloco) or []):
            alvo = os.path.join(d, f"{pref}{i:02d}.mp3")
            if os.path.exists(alvo) and os.path.getsize(alvo) > 500:
                continue
            silencio(len(c["nar"]) / t, alvo)
            feitos += 1
    return d, feitos, t


def ensaia(spec_caminho: str) -> dict:
    nome = os.path.basename(spec_caminho)[:-5]
    d, feitos, t = prepara(spec_caminho)

    env = dict(os.environ, FABRICA_WORKDIR=RAIZ_ENSAIO)
    inicio = time.time()
    p = subprocess.run(
        [sys.executable, os.path.join(RAIZ, "fabrica", "etapas.py"), spec_caminho],
        env=env, capture_output=True, text=True,
    )
    gasto = time.time() - inicio

    saidas = {a: os.path.getsize(os.path.join(d, a))
              for a in ("video.mp4", "short.mp4", "thumbnail.png",
                        "legendas.srt", "copy.md")
              if os.path.exists(os.path.join(d, a))}

    # A saida INTEIRA vai para o disco. Truncar aqui ja me custou uma
    # investigacao: o corte pelos ultimos 900 chars comeu o inicio da linha de
    # comando do ffmpeg, eu reproduzi o comando SEM o PNG base e persegui um
    # "stream specifier matches no streams" que nunca existiu.
    log = os.path.join(d, "ensaio.log")
    with open(log, "w", encoding="utf-8") as f:
        f.write(p.stdout or "")
        f.write("\n--- stderr ---\n")
        f.write(p.stderr or "")
    return {
        "spec": nome, "ok": p.returncode == 0, "segundos": round(gasto, 1),
        "mp3_gerados": feitos, "taxa": t, "saidas": saidas, "log": log,
        "erro": (p.stderr or p.stdout).strip().splitlines()[-6:] if p.returncode else [],
    }


def main() -> int:
    alvos = sys.argv[1:]
    if not alvos:
        print(__doc__.strip().splitlines()[-1])
        return 2

    n = trilhas_falsas("/tmp/trilhas")
    print(f"trilhas para o ensaio: {n} faixas em /tmp/trilhas (silencio)\n")

    falhou = 0
    for caminho in alvos:
        r = ensaia(caminho)
        marca = "OK  " if r["ok"] else "QUEBROU"
        arte = " ".join(f"{k}={v // 1024}kB" for k, v in r["saidas"].items())
        print(f"{marca} {r['spec']:24} {r['segundos']:7.1f}s  {arte}")
        if not r["ok"]:
            falhou += 1
            for linha in r["erro"]:
                print("        ", linha)
            print(f"         (saida completa em {r['log']})")
    print(f"\n-> {len(alvos) - falhou}/{len(alvos)} chegaram ao fim da esteira")
    return 1 if falhou else 0


if __name__ == "__main__":
    raise SystemExit(main())
