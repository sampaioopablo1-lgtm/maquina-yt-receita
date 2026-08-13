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

# Taxas MEDIDAS, com a fonte de cada uma. Onde nao ha medicao, o default entra
# declarado — estimar duracao errada aqui nao invalida o ensaio (ele procura
# quebra, nao duracao), mas registrar de onde veio o numero evita que alguem
# use esta tabela como se fosse medicao.
TAXA_CHARS_S = {
    "pt-BR-AntonioNeural": 14.30,          # config/canais/sx-educacao.yaml
    "pt-BR-ThalitaMultilingualNeural": 16.52,  # config/canais/labtreinamento.yaml
    "id-ID-GadisNeural": 14.37,            # medido 13/08/2026, 199 chars/13,848 s
}
TAXA_PADRAO = 14.50   # NAO medida: media grosseira das tres acima


def taxa(voz: str) -> float:
    return TAXA_CHARS_S.get(voz, TAXA_PADRAO)


def _ffmpeg(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def silencio(segundos: float, alvo: str) -> None:
    """mp3 mudo de duracao exata. lavfi anullsrc nao precisa de rede."""
    _ffmpeg(["-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
             "-t", f"{max(segundos, 0.4):.3f}", "-q:a", "9", alvo])


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
    return {
        "spec": nome, "ok": p.returncode == 0, "segundos": round(gasto, 1),
        "mp3_gerados": feitos, "taxa": t, "saidas": saidas,
        "erro": (p.stderr or p.stdout)[-900:] if p.returncode else "",
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
            for linha in r["erro"].splitlines()[-12:]:
                print("        ", linha)
    print(f"\n-> {len(alvos) - falhou}/{len(alvos)} chegaram ao fim da esteira")
    return 1 if falhou else 0


if __name__ == "__main__":
    raise SystemExit(main())
