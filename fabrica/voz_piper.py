#!/usr/bin/env python3
"""Segundo provedor de narracao — Piper, neural e OFFLINE. O plano B medido.

POR QUE ISTO EXISTE (12/10/2026). O `edge_tts` e fornecedor UNICO desde sempre,
e a rotina ja avisava que isso era buraco. Em 12/10 ele caiu: o handshake de
`wss://speech.platform.bing.com` devolve **403 no runner**, com a versao mais
recente (7.2.8) e em duas vozes diferentes, reproduzido em dois runs
independentes (38198672898 e 38202568056). Nao e versao, e nao e oscilacao.

Antes disso o 403 era conhecido so NESTE container, e o `CLAUDE.md` e a rotina
diziam "render continua no runner". **Essa frase estava errada**, e ficou
escondida porque a Frota morria no portao de glifos, ANTES do render, nos oito
runs desde 09/10 17:14.

A rotina proibe costura vazia: *"nao instale plano B sem um segundo provedor de
verdade"*. O Piper e de verdade — neural, sem chave, e a sintese nao toca a
rede. Medido no runner: importou, sintetizou 63 KB de audio, e as quatro vozes
dos tres idiomas da frota existem publicadas.

**O QUE ESTE MODULO NAO RESOLVE, e vai gritado no log em vez de ficar calado:**
o `MODELO_VOZ` tem R e P medidos POR VOZ (R 17,47/20,61/20,07 e P
0,737/1,273/1,419 para pt-BR, grego e polones). Esses numeros sao do edge-tts.
Com o Piper eles **nao valem**, e sao eles que alimentam a estimativa de
duracao, que alimenta o portao `duracao` e a mira. Entao toda peca narrada por
aqui sai com AVISO, e a calibracao precisa ser remedida antes de alguem confiar
na estimativa dela. Fingir que o numero antigo serve seria o erro do 679/698
outra vez — usar a constante de uma voz para outra.

**A voz MUDA, e isso e audivel.** Identidade de canal nao e detalhe. Por isso
este modulo e FALLBACK, nunca substituto: se o edge-tts voltar, a frota volta
sozinha a voz original, sem ninguem precisar lembrar de desfazer nada.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import urllib.request

BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main"

# Chaveado pela voz do edge-tts, que e o que a spec declara — assim nenhuma
# spec muda para o fallback funcionar.
#
# A grega so tem `low` publicada; as outras duas tem `medium`. Isso e diferenca
# de qualidade REAL entre os canais, e esta escrito aqui para quem for comparar
# retencao depois nao atribuir a diferenca ao roteiro.
VOZES = {
    "pt-BR-ThalitaMultilingualNeural":
        ("pt/pt_BR/faber/medium", "pt_BR-faber-medium"),
    "el-GR-NestorasNeural":
        ("el/el_GR/rapunzelina/low", "el_GR-rapunzelina-low"),
    "pl-PL-MarekNeural":
        ("pl/pl_PL/darkman/medium", "pl_PL-darkman-medium"),
}

# O edge-tts e chamado com rate="-4%". O Piper nao tem `rate`; tem
# `length_scale`, que multiplica a duracao. Falar 4% mais devagar e durar
# 1/0,96 do tempo.
LENGTH_SCALE = 1 / 0.96

CACHE = os.environ.get("PIPER_CACHE") or "/tmp/piper-vozes"


def disponivel() -> bool:
    try:
        import piper                                       # noqa: F401
        return True
    except Exception:                                      # noqa: BLE001
        return False


def modelo(voz_edge: str) -> str | None:
    """Baixa o .onnx e o .json UMA vez. Devolve o caminho, ou None."""
    alvo = VOZES.get(voz_edge)
    if not alvo:
        return None
    caminho, nome = alvo
    os.makedirs(CACHE, exist_ok=True)
    onnx = f"{CACHE}/{nome}.onnx"
    if os.path.exists(onnx) and os.path.getsize(onnx) > 1_000_000:
        return onnx
    for sufixo in (".onnx", ".onnx.json"):
        url = f"{BASE}/{caminho}/{nome}{sufixo}"
        try:
            with urllib.request.urlopen(url, timeout=180) as r, \
                 open(f"{CACHE}/{nome}{sufixo}", "wb") as f:
                shutil.copyfileobj(r, f)
        except Exception:                                  # noqa: BLE001
            return None
    return onnx if os.path.getsize(onnx) > 1_000_000 else None


def sintetiza(texto: str, voz_edge: str, alvo_mp3: str, ffmpeg: str = "ffmpeg") -> bool:
    """Gera o mp3 que o resto da fabrica espera. True se saiu audio util."""
    onnx = modelo(voz_edge)
    if not onnx:
        return False
    wav = alvo_mp3 + ".piper.wav"
    try:
        r = subprocess.run(
            ["python3", "-m", "piper", "--model", onnx,
             "--length_scale", f"{LENGTH_SCALE:.4f}", "--output_file", wav],
            input=texto.encode(), capture_output=True, timeout=180)
        if r.returncode or not os.path.exists(wav) or os.path.getsize(wav) < 1000:
            return False
        # mp3 porque todo o resto da fabrica — concat, loudnorm, duracao —
        # ja espera mp3. Trocar o formato aqui espalharia a mudanca.
        r2 = subprocess.run(
            [ffmpeg, "-y", "-v", "error", "-i", wav, "-c:a", "libmp3lame",
             "-q:a", "2", alvo_mp3], capture_output=True, timeout=180)
        return r2.returncode == 0 and os.path.getsize(alvo_mp3) > 1000
    except Exception:                                      # noqa: BLE001
        return False
    finally:
        try:
            os.remove(wav)
        except OSError:
            pass


def aviso_de_calibracao(voz_edge: str) -> str:
    """A frase que TEM de aparecer no log de toda peca narrada pelo Piper."""
    return (f"::warning::NARRACAO PELO PIPER (fallback) na voz {voz_edge}: o "
            f"R e o P de MODELO_VOZ sao do edge-tts e NAO valem para esta voz. "
            f"A estimativa de duracao desta peca nao esta calibrada — remeca "
            f"antes de usar o numero dela para mira ou para o portao duracao.")
