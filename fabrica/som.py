#!/usr/bin/env python3
"""Medir o som da peça RENDERIZADA: LUFS, pico real e silêncio. Absoluto.

POR QUE ISTO EXISTE, e NÃO é porque um pipeline alheio tinha. Em 12/10/2026 o
dono mandou o `pipeline_canal_dark_v1.2`. Estudado, a comparação deu o seguinte:

  * o ALVO de volume dele e o nosso são o MESMO — `loudnorm=I=-14`, e o nosso
    tem o pico mais apertado (`TP=-1.5` contra `TP=-6` no mixer dele). Logo não
    havia nada a importar ali;
  * o que ele tem e nós NÃO tínhamos é a **CONFERÊNCIA**: ele mede o arquivo
    final com `ebur128` e reprova se o LUFS sair a mais de 1,0 do alvo. Nós
    aplicamos o filtro e **nunca medimos o resultado**.

E essa é a assinatura do §3.8 outra vez: *portão verde fabrica "está tudo
certo"*. Ter `loudnorm=I=-14` na linha de comando não é evidência de que a peça
saiu a -14 — o `loudnorm` de UMA passada é um filtro dinâmico e pode errar o
alvo, e um erro desses é silencioso.

**O que isto mede é ABSOLUTO**, como o `signalstats` do 690/699 — então vale com
n=1 e não depende da conta de poder do 693.

VALIDAÇÃO DO INSTRUMENTO, medida em 12/10 neste container, com sinal controlado:
um tom de 220 Hz a -30 dB lido em **-52,0 LUFS**; o mesmo tom depois do nosso
`loudnorm=I=-14:TP=-1.5:LRA=11` lido em **-13,9 LUFS**. O instrumento responde e
o filtro acerta o alvo num sinal estável. **Isso NÃO é evidência sobre as peças
publicadas** — fala com música e corte de cena é outro sinal, e é exatamente o
que falta medir.

O que este módulo NÃO faz: não reprova nada. Ele reporta. Pôr um portão de
volume exige primeiro a medição das peças reais, e limiar sem procedência é
critério inventado.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys

# O alvo que a nossa própria fábrica já aplica (`fabrica.py AUDIO_ARGS`).
# Não é um limiar novo: é o número que já está no filtro, trazido para cá para
# que a conferência compare contra ele em vez de contra uma lembrança minha.
ALVO_LUFS = -14.0
TP_MAX_DBTP = -1.5

# Tolerância do RELATO, não de portão. O pipeline alheio reprova acima de 1,0;
# nós ainda não medimos peça real nenhuma, então aqui ela só classifica o texto.
TOLERANCIA_RELATO = 1.0


class SemAudio(Exception):
    """O arquivo não tem faixa de áudio — isso é defeito, não leitura de zero."""


def _ffmpeg(args: list[str]) -> str:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    return r.stderr


def tem_audio(caminho: str) -> bool:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=codec_type", "-of", "csv=p=0", caminho],
        capture_output=True, text=True).stdout
    return "audio" in out


def loudness(caminho: str) -> dict:
    """`lufs`, `lra` e `pico_dbtp` pelo `ebur128`, que é o padrão do streaming.

    Levanta `SemAudio` em vez de devolver None silencioso: arquivo de vídeo sem
    faixa de áudio é defeito de render, e o relato tem de dizer isso.
    """
    if not tem_audio(caminho):
        raise SemAudio(f"{caminho} nao tem faixa de audio")
    txt = _ffmpeg(["-i", caminho, "-map", "0:a:0",
                   "-af", "ebur128=peak=true", "-f", "null", "-"])
    resumo = txt[txt.rfind("Summary:"):] if "Summary:" in txt else txt
    def _num(padrao):
        m = re.search(padrao, resumo)
        if not m or m.group(1) == "-inf":
            return None
        return float(m.group(1))
    return {
        "lufs": _num(r"I:\s+(-?[\d.]+|-inf) LUFS"),
        "lra": _num(r"LRA:\s+(-?[\d.]+|-inf) LU"),
        "pico_dbtp": _num(r"Peak:\s+(-?[\d.]+|-inf) dBFS"),
    }


def silencios(caminho: str, ruido_db: float = -45.0,
              minimo_s: float = 1.0) -> list[tuple[float, float]]:
    """Trechos de silêncio acima de `minimo_s`, como (inicio, duracao).

    O piso de 1,0 s é mais apertado que o do pipeline alheio (2,0 s) por uma
    razão nossa e medida: a sobrecarga por cena é `P + 0,300`, e P vai de
    **1,04 s** no pt-BR a **1,72 s** no polonês. Com 2,0 s de piso o silêncio
    NORMAL de fim de frase da voz polonesa já quase dispara, e a medição não
    distinguiria defeito de modelo. Com 1,0 s eu vejo os dois e decido lendo.
    """
    txt = _ffmpeg(["-i", caminho, "-map", "0:a:0",
                   "-af", f"silencedetect=noise={ruido_db}dB:d={minimo_s}",
                   "-f", "null", "-"])
    pares = re.findall(r"silence_end: (-?[\d.]+) \| silence_duration: ([\d.]+)",
                       txt)
    return [(round(float(f) - float(d), 2), round(float(d), 2))
            for f, d in pares]


def desvio_do_alvo(lufs: float | None, alvo: float = ALVO_LUFS) -> float | None:
    """Quanto a peça está longe do alvo, com sinal. None quando não há leitura."""
    return None if lufs is None else round(lufs - alvo, 2)


def relato(caminho: str, alvo: float = ALVO_LUFS) -> str:
    try:
        lo = loudness(caminho)
    except SemAudio as e:
        return f"SOM: DEFEITO — {e}"
    d = desvio_do_alvo(lo["lufs"], alvo)
    sil = silencios(caminho)
    linhas = [f"SOM de {caminho}",
              f"  LUFS {lo['lufs']} (alvo {alvo}, desvio {d})",
              f"  LRA {lo['lra']} | pico {lo['pico_dbtp']} dBFS "
              f"(teto do nosso filtro: {TP_MAX_DBTP})"]
    if d is not None and abs(d) > TOLERANCIA_RELATO:
        linhas.append(f"  >> FORA do alvo por {abs(d)} LU. O `loudnorm` de uma "
                      "passada e dinamico e pode errar; isto e LEITURA, nao "
                      "portao.")
    if sil:
        linhas.append("  silencios >= 1,0 s: " + ", ".join(
            f"{i}s por {dur}s" for i, dur in sil[:6]))
        linhas.append("  (lembre: P de fim de frase vai de 1,04 s no pt-BR a "
                      "1,72 s no polones — parte disto e MODELO, nao defeito)")
    else:
        linhas.append("  nenhum silencio >= 1,0 s")
    return "\n".join(linhas)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        print("uso: som.py <arquivo.mp4> [--json]")
        return 2
    caminho = sys.argv[1]
    if "--json" in sys.argv:
        try:
            lo = loudness(caminho)
        except SemAudio as e:
            print(json.dumps({"erro": str(e)}, ensure_ascii=False))
            return 1
        lo["desvio_do_alvo"] = desvio_do_alvo(lo["lufs"])
        lo["silencios"] = silencios(caminho)
        print(json.dumps(lo, ensure_ascii=False))
        return 0
    print(relato(caminho))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
