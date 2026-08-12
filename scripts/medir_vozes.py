"""Mede caracteres por segundo de cada voz edge-tts usada pela frota.

Por que existe: `roteiro.escrever_roteiro` dimensiona o texto em CARACTERES,
porque e caractere que o TTS converte em tempo. A conta e

    chars_alvo = duracao_alvo_s * taxa

e a duracao que sai e `chars_alvo / taxa_real`. Ou seja, o video so alcanca o
alvo se a taxa ASSUMIDA for maior ou igual a real. Assumir menos que a real
encurta o video na mesma proporcao.

Isso torna o padrao de 12,0 perigoso, nao conservador. As vozes vao de 9,85 a
20,02 chars/s. Numa voz de 20, assumir 12 entrega 60% da duracao pedida: 780 s
viram 468 s, sete minutos e meio — ABAIXO do piso de 8 min, e o video e barrado
depois de ja ter custado o render inteiro.

Em 12/08/2026, nove dos treze canais usavam voz sem taxa medida. Este script
tira a duvida: sintetiza o mesmo texto em cada voz e divide caracteres pela
duracao real do mp3.

Roda no runner do Actions (.github/workflows/medir-vozes.yml) — o container do
agente nao alcanca speech.platform.bing.com.

Uso:
    pip install edge-tts
    python scripts/medir_vozes.py                    # todas as vozes da frota
    python scripts/medir_vozes.py pl-PL-MarekNeural  # so estas
"""

from __future__ import annotations

import asyncio
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

# Texto de medicao: numeros POR EXTENSO, como a fabrica escreve, porque digito
# cru muda a duracao (o TTS soletra "2026" de formas diferentes por idioma) e
# contaminaria a taxa. Comprimento parecido com uma cena real.
TEXTO = (
    "Este e um texto de calibracao com duracao suficiente para medir a taxa de "
    "fala desta voz com precisao razoavel. Ele contem numeros por extenso, como "
    "mil novecentos e noventa e nove, duzentos e cinquenta, e tres virgula sete "
    "por cento, porque digito cru muda a duracao e contaminaria a medida. "
    "Tambem contem frases de comprimento variado. Algumas curtas. Outras mais "
    "longas, com virgulas e subordinadas, do jeito que uma narracao real se "
    "comporta quando o roteirista escreve para o ouvido e nao para o olho."
)

# Mesmo rate que a producao usa. Medir com outro rate invalida a medida.
RATE = "-4%"


def vozes_da_frota() -> list[str]:
    achadas = []
    for arquivo in sorted((ROOT / "config" / "canais").glob("*.yaml")):
        dados = yaml.safe_load(arquivo.read_text(encoding="utf-8")) or {}
        voz = (dados.get("canal") or {}).get("voz_edge", "")
        if voz and voz not in achadas:
            achadas.append(voz)
    padrao = yaml.safe_load((ROOT / "config" / "default.yaml").read_text(encoding="utf-8"))
    voz = (padrao.get("canal") or {}).get("voz_edge", "")
    if voz and voz not in achadas:
        achadas.append(voz)
    return achadas


def duracao_s(caminho: Path) -> float:
    """Duracao do mp3, com ffprobe se houver e ffmpeg se nao houver.

    O runner do Actions tem ffmpeg e NAO tem ffprobe — descoberto na primeira
    execucao deste script, que sintetizou as doze vozes e perdeu todas na hora
    de medir. Sao dois binarios distintos e so um vem na imagem.
    """
    if probe := shutil.which("ffprobe"):
        saida = subprocess.run(
            [probe, "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(caminho)],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return float(saida)

    # Sem ffprobe: decodifica para o vazio e le o `time=` final do stderr, que e
    # a duracao real processada.
    proc = subprocess.run(
        [_ffmpeg(), "-i", str(caminho), "-f", "null", "-"],
        capture_output=True, text=True,
    )
    marcas = re.findall(r"time=(\d+):(\d\d):(\d\d\.\d+)", proc.stderr)
    if not marcas:
        raise RuntimeError(f"nao consegui medir {caminho.name}:\n{proc.stderr[-400:]}")
    h, m, s = marcas[-1]
    return int(h) * 3600 + int(m) * 60 + float(s)


def _ffmpeg() -> str:
    if achado := shutil.which("ffmpeg"):
        return achado
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


async def medir(voz: str, destino: Path) -> float:
    import edge_tts

    mp3 = destino / f"{voz}.mp3"
    # Retentativa: o edge-tts recusa IP de datacenter de forma intermitente, e
    # uma recusa nao e motivo para deixar a voz sem taxa.
    for tentativa in range(4):
        try:
            await edge_tts.Communicate(TEXTO, voz, rate=RATE).save(str(mp3))
            if mp3.exists() and mp3.stat().st_size > 0:
                break
        except Exception as e:
            if tentativa == 3:
                raise
            print(f"    tentativa {tentativa + 1} falhou ({e}) — repetindo", flush=True)
        await asyncio.sleep(3 * (tentativa + 1))
    return len(TEXTO) / duracao_s(mp3)


async def principal(vozes: list[str]) -> int:
    resultados: dict[str, float] = {}
    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp)
        for voz in vozes:
            print(f"  medindo {voz}...", flush=True)
            try:
                resultados[voz] = await medir(voz, destino)
            except Exception as e:
                print(f"    FALHOU: {e}", flush=True)

    if not resultados:
        print("Nenhuma voz medida.", file=sys.stderr)
        return 1

    print(f"\n{len(TEXTO)} caracteres de texto, rate={RATE}\n")
    print("Cole em src/maquina/stages/roteiro.py:\n")
    print("CHARS_POR_S = {")
    for voz, taxa in sorted(resultados.items()):
        print(f'    "{voz}": {taxa:.2f},')
    print("}")

    maior = max(resultados.values())
    print(
        f"\nMaior taxa medida: {maior:.2f} chars/s. O padrao de quem nao esta na "
        f"tabela precisa ser >= isso — assumir menos que a taxa real encurta o "
        f"video na mesma proporcao."
    )
    return 0


if __name__ == "__main__":
    alvos = sys.argv[1:] or vozes_da_frota()
    print(f"{len(alvos)} voz(es) para medir.")
    sys.exit(asyncio.run(principal(alvos)))
