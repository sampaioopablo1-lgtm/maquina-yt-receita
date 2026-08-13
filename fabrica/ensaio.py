#!/usr/bin/env python3
"""Roda a esteira INTEIRA sem TTS, para achar defeito de render antes do runner.

O prontidao.py responde se a spec passa nos portoes ESTATICOS. Ele nao responde
a pergunta que custa caro: o `etapas.py` chega ao fim com esta spec? Entre um e
outro estao a rasterizacao em camadas, a montagem de cada clipe, o zoompan, a
mixagem da trilha, o loudnorm, o srt, o copy.md e os dois testes visuais — e
qualquer um deles pode quebrar numa spec especifica, depois de doze minutos de
render, dentro de um runner que so existe enquanto o job vive.

Aqui a narracao e substituida por silencio com a DURACAO que o TTS produziria
(chars/R + frases*P, os dois termos medidos por voz). Todo o resto e real: os mesmos PNG, o
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

# Duracao de fala TTS tem DOIS termos, nao um. Uma taxa unica de chars/s nao
# prediz nada, porque a pausa entre frases domina em roteiro de frase curta.
#
# A prova, medida em 14/08/2026 na id-ID-GadisNeural: dois textos da MESMA voz,
# um com duas frases longas e outro com doze curtas, devolveram 15,19 e 8,19
# chars/s. A mesma voz, 85% de diferenca — a "taxa medida" da voz depende do
# roteiro que voce usou para medir, entao ela nao e uma propriedade da voz.
#
# O modelo com dois termos separa o que e da voz do que e do roteiro:
#
#     duracao = chars / R + frases * P
#
# R = chars por segundo de FALA. P = segundos de silencio por ponto final.
# Cada voz foi medida com duas amostras no idioma dela (uma de 2 frases longas,
# outra de 12 curtas), e o par de equacoes resolve R e P sem chute.
#
# Isto ja estava registrado em `aprendizados` como critico para a id-ID-Ardi
# ("duracao = chars/20,58 + frases x 0,96") e mesmo assim o portao de duracao
# seguia dividindo por uma taxa unica. Agora nao.
#
# Voz nova entra MEDIDA com as duas amostras, nunca estimada.
MODELO_VOZ = {                       # voz: (R chars/s de fala, P s por frase)
    "pt-BR-AntonioNeural":            (18.56, 0.980),
    "pt-BR-ThalitaMultilingualNeural": (19.09, 0.571),
    "pt-BR-FranciscaNeural":          (16.97, 0.310),
    "id-ID-GadisNeural":              (17.42, 1.376),
    "id-ID-ArdiNeural":               (23.76, 1.277),
    "es-MX-DaliaNeural":              (21.14, 1.163),
    "en-GB-RyanNeural":               (21.90, 1.131),
    "en-US-AndrewNeural":             (18.45, 0.243),
    "pl-PL-MarekNeural":              (22.75, 1.291),
    "tr-TR-AhmetNeural":              (16.96, 1.289),
    "el-GR-NestorasNeural":           (25.37, 1.315),
    "hi-IN-MadhurNeural":             (13.10, 1.165),
}


def duracao_cena(nar: str, voz: str) -> float:
    """Segundos que esta narracao vai ocupar, pelos dois termos.

    Conta frase com `narracao.frases`, que e quem ja sabe que o fim de frase em
    devanagari e o danda e nao o ponto. Contar aqui de outro jeito faria o
    portao medir o hindi como uma frase unica de mil caracteres.
    """
    from narracao import frases

    R, P = MODELO_VOZ[voz]
    return len(nar) / R + len(frases(nar)) * P


# Sobra de MONTAGEM, medida no render e nao no TTS. O clipe pronto e mais longo
# que o audio dele: sobra um resto dentro da cena e um intervalo ate a proxima.
#
# MEDIDO em 14/08/2026 no ensaio completo do resep-naik-level-003: o modelo de
# TTS somava 849,9 s e o video.mp4 saiu com 894,4 s. Sao 44,5 s em 86 cenas.
# Duas medicoes independentes batem — o .srt mostra 0,3 s de intervalo entre o
# fim de uma cena e o inicio da seguinte, mais 0,26 s de mediana de folga dentro
# da cena.
#
# POR QUE IMPORTA: sem este termo o portao aprovou 14,2 min para um video que
# saiu com 14,9, contra um teto de 15,0. Sobraram cinco segundos. Um roteiro
# um pouco maior passa no portao e estoura o teto sem ninguem ver.
#
# n=1 spec. Confirmar num segundo render antes de tratar como constante firme.
#
# E fica FORA de `duracao_cena` de proposito: o ensaio gera o silencio pela
# duracao do TTS, e a montagem adiciona a sobra depois. Somar aqui faria o
# silencio ja nascer com a sobra e o video sairia mais longo ainda.
PADDING_CENA_S = 0.517


def duracao_estimada(cenas, voz: str) -> float:
    return (sum(duracao_cena(c.get("nar", ""), voz) for c in cenas)
            + PADDING_CENA_S * len(cenas))


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

    voz = sp["voz"]
    feitos = 0
    for pref, bloco in (("l", "longo"), ("s", "short")):
        for i, c in enumerate(sp.get(bloco) or []):
            alvo = os.path.join(d, f"{pref}{i:02d}.mp3")
            if os.path.exists(alvo) and os.path.getsize(alvo) > 500:
                continue
            silencio(duracao_cena(c["nar"], voz), alvo)
            feitos += 1
    return d, feitos, voz


def ensaia(spec_caminho: str) -> dict:
    nome = os.path.basename(spec_caminho)[:-5]
    d, feitos, voz = prepara(spec_caminho)

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
        "mp3_gerados": feitos, "voz": voz, "saidas": saidas, "log": log,
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
