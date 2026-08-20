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
# Voz nova entra MEDIDA, nunca estimada.
#
# E MEDIDA EM PRODUCAO, nao em amostra de laboratorio. Os valores originais
# vinham de duas amostras sinteticas por voz (uma de 2 frases longas, outra de
# 12 curtas) e TODOS erravam para o mesmo lado, de +6,6% a +18,0%. Nove de nove
# subestimando e vies, nao ruido: duas amostras nao cobrem a distribuicao de
# tamanho de frase de um roteiro de 86 cenas.
#
# O QUE ISSO CUSTOU: o resep-naik-level-003 foi dimensionado para 14,2 min,
# passou no portao (teto 15,0) e saiu com 16:14 — 74 s acima do teto, publicado.
#
# ESTES VALORES SAO DE 19/08/2026, e pela primeira vez as DOZE vozes vem do
# mesmo lugar: ajuste por minimos quadrados cena-a-cena sobre os `legendas.srt`
# que os proprios pacotes publicados deixaram no bucket. Antes disso o
# calibra_voz.py existia mas nunca alcancava o bucket — faltava o workflow
# `calibrar-vozes.yml`, que roda onde o repositorio e o Storage sao alcancaveis
# ao mesmo tempo. Sao 2.317 cenas reais no total.
#
# Como o erro do modelo ANTERIOR se distribuia (real/previsto - 1, entao
# POSITIVO = o video sai mais longo que o previsto, que e o lado perigoso):
#
#     pt-BR-Francisca  -7,0%      pl-PL-Marek      -1,5%
#     en-US-Andrew     +3,8%      es-MX-Dalia      -0,1%
#     id-ID-Gadis      +3,4%      el-GR-Nestoras   -0,1%
#     tr-TR-Ahmet      +2,2%      hi-IN-Madhur     +0,0%
#     en-GB-Ryan       +1,2%      pt-BR-Thalita    +0,3%
#     id-ID-Ardi       +0,7%      pt-BR-Antonio    -0,4%
#
# A Francisca e o caso que mais movimentou: P caiu de 1,036 para 0,298 com
# n=149. Ja tinha sido avisado antes que nesta voz o erro mora em P e nao em R
# — conferir so chars/s deixa passar uma voz cuja pausa entre frases e que
# estoura o roteiro. Agora vale ao contrario: a pausa dela e MENOR do que se
# supunha, e o modelo antigo alongava o roteiro em 7%.
MODELO_VOZ = {                       # voz: (R chars/s de fala, P s por frase)
    # Todas medidas cena-a-cena nos .srt publicados, 19/08/2026.
    "el-GR-NestorasNeural":            (20.61, 1.273),   # n=519
    "en-GB-RyanNeural":                (18.92, 1.162),   # n=121
    "en-US-AndrewNeural":              (16.00, 0.119),   # n=79
    "es-MX-DaliaNeural":               (17.48, 1.242),   # n=91
    "hi-IN-MadhurNeural":              (11.92, 1.194),   # n=140
    "id-ID-ArdiNeural":                (18.96, 1.124),   # n=540
    "id-ID-GadisNeural":               (14.12, 1.318),   # n=75
    "pl-PL-MarekNeural":               (20.07, 1.419),   # n=409
    "pt-BR-AntonioNeural":             (16.68, 1.040),   # n=214
    "pt-BR-FranciscaNeural":           (15.24, 0.298),   # n=149
    "pt-BR-ThalitaMultilingualNeural": (17.47, 0.737),   # n=171
    "tr-TR-AhmetNeural":               (15.35, 1.337),   # n=73
}

# O ajuste do Nestoras foi refeito EM PAR com o conserto do FIM_DE_FRASE, como
# o aprendizado 313 exigia — mudar o divisor de frase sem recalibrar a voz
# trocaria um vies por outro. Medido nos mesmos 429 pares, antes e depois:
#
#     antes do conserto ... R 20,35  P 1,251
#     depois .............. R 20,40  P 1,257
#
# O deslocamento e pequeno porque as pontes gregas ja terminavam em ";" e o
# portao do gancho (tabela GANCHO) ja as aceitava; o que mudou foi a contagem
# passar a enxergar essas perguntas como frase inteira. As outras onze vozes
# saíram IDENTICAS nas duas medicoes, que e a prova de que a tabela por idioma
# nao vazou para polones, portugues nem indonesio.


def duracao_cena(nar: str, voz: str) -> float:
    """Segundos que esta narracao vai ocupar, pelos dois termos.

    Conta frase com `narracao.frases`, que e quem ja sabe que o fim de frase em
    devanagari e o danda e nao o ponto. Contar aqui de outro jeito faria o
    portao medir o hindi como uma frase unica de mil caracteres.
    """
    from narracao import frases

    # O idioma sai do PREFIXO da voz, nao de um parametro novo: quem chama aqui
    # nem sempre tem a spec na mao, e o nome da voz do edge-tts sempre comeca
    # pelo idioma (el-GR-NestorasNeural -> el). Sem isso, `frases` usaria o
    # divisor padrao e o grego voltaria a contar pergunta como meia frase.
    R, P = MODELO_VOZ[voz]
    return len(nar) / R + len(frases(nar, voz.split("-")[0])) * P


# Intervalo de MONTAGEM entre uma cena e a seguinte, medido no render.
#
# MEDIDO em 17/08/2026 sobre os .srt de treze pacotes publicados: 1.056
# intervalos, TODOS exatamente 0,300 s. Valor unico, sem dispersao — a esteira
# insere um intervalo fixo, nao uma folga variavel.
#
# O 0,517 que estava aqui era ARTEFATO DO ENSAIO, nao propriedade do render. O
# ensaio gera silencio com a duracao que o MODELO previa; quando o modelo errava
# 11% para menos, o video do ensaio saia mais longo que a soma prevista e a
# diferenca era creditada a "sobra de montagem". Media-se o erro do modelo e
# chamava-se de padding — e por isso o numero era `n=1, confirmar depois`.
#
# Com o modelo recalibrado em producao, o resto e so o intervalo: no
# resep-naik-level-003 os clipes somam 948,3 s, mais 85 intervalos de 0,3 s da
# 973,8 s, contra 974,2 s de video real. Sobram 0,4 s no pacote inteiro.
#
# Sao os INTERVALOS que contam, e ha um a menos que cenas: n cenas, n-1
# intervalos. Multiplicar por n somava uma cena fantasma no fim.
GAP_CENA_S = 0.300


def duracao_estimada(cenas, voz: str) -> float:
    """Duracao do video montado: a fala de cada cena mais os intervalos."""
    return (sum(duracao_cena(c.get("nar", ""), voz) for c in cenas)
            + GAP_CENA_S * max(len(cenas) - 1, 0))


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
