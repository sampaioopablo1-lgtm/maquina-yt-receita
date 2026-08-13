#!/usr/bin/env python3
"""So a NARRACAO de um pacote: gera os l*.mp3 e s*.mp3 e mais nada.

Existe por uma separacao fisica, nao estetica. As duas metades de `montar` tem
necessidades opostas:

  - TTS e REDE. Um mp3 de cena leva 1-2 s e nao usa CPU. Mas fala com
    speech.platform.bing.com, e nem toda maquina alcanca esse host.
  - Rasterizar e comprimir e CPU. O sandbox Composio tem 1 vCPU e faz 208 s por
    cena; uma maquina de 4 vCPU faz 10,3 s — 20x.

Medido em 13/08/2026: o container da sessao (4 vCPU, 16 GB, ffmpeg 6.1.1) tem
speech.platform.bing.com negado pela politica de egress (o proxy responde 403
ao CONNECT e registra connect_rejected). O sandbox Composio alcanca o host mas
tem 1 vCPU. Nenhum dos dois faz o pacote inteiro sozinho; juntos fazem.

Entao: este script roda ONDE HA REDE, os mp3 viajam pelo Storage, e o
`etapas.py` roda ONDE HA CPU — a guarda `_mp3_ok` da etapa 1 ja pula `montar`
quando os mp3 estao no lugar.

Importa edge_tts e nada mais. NAO importa fabrica.py, que puxa cairosvg na
linha 2: quem so precisa narrar nao pode ser obrigado a instalar a pilha de
render. E a mesma licao do copy_md.py, que so nasceu porque o job de reparo de
descricao morria num `import cairosvg` para formatar markdown.

Uso:
    python3 fabrica/vozes.py <spec.json> [--dir <workdir>]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os

import edge_tts

from caminhos import dir_trabalho

# Mesma taxa do fabrica.vozes: mudar aqui sem mudar la desalinha a legenda, que
# e cronometrada pela duracao real do mp3.
RATE = "-4%"
TIMEOUT_S = 90
TENTATIVAS = 3
MIN_BYTES = 1000


async def uma(texto: str, voz: str, alvo: str) -> bool:
    """Devolve True se gerou agora, False se ja existia."""
    if os.path.exists(alvo) and os.path.getsize(alvo) > MIN_BYTES:
        return False
    # O websocket do edge-tts ja pendurou sem erro nem timeout (15 min parado
    # na cena 82 do setiap-006). wait_for + 3 tentativas.
    for tentativa in range(TENTATIVAS):
        try:
            com = edge_tts.Communicate(texto, voz, rate=RATE)
            await asyncio.wait_for(com.save(alvo), timeout=TIMEOUT_S)
            if os.path.getsize(alvo) > MIN_BYTES:
                return True
            raise RuntimeError(f"mp3 vazio: {alvo}")
        except Exception:
            try:
                os.remove(alvo)
            except OSError:
                pass
            if tentativa == TENTATIVAS - 1:
                raise
    return False


async def narrar(sp: dict, d: str) -> tuple[int, int]:
    voz = sp["voz"]
    novos = existentes = 0
    for pref, bloco in (("l", "longo"), ("s", "short")):
        for i, c in enumerate(sp.get(bloco) or []):
            alvo = os.path.join(d, f"{pref}{i:02d}.mp3")
            if await uma(c["nar"], voz, alvo):
                novos += 1
                print(f"  {pref}{i:02d} ok", flush=True)
            else:
                existentes += 1
    return novos, existentes


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("spec")
    p.add_argument("--dir", default=None,
                   help="workdir (padrao: $FABRICA_WORKDIR/<pacote>, ou /tmp/f/<pacote>)")
    args = p.parse_args()

    sp = json.load(open(args.spec, encoding="utf-8"))
    d = args.dir or dir_trabalho(sp)
    os.makedirs(d, exist_ok=True)

    total = len(sp.get("longo") or []) + len(sp.get("short") or [])
    print(f"{sp.get('pacote') or sp['slug']}  voz={sp['voz']}  cenas={total}  ->  {d}")
    novos, existentes = asyncio.run(narrar(sp, d))
    print(f"  -> {novos} mp3 novos, {existentes} ja existiam, {total} no total")

    faltam = [
        f"{pref}{i:02d}"
        for pref, bloco in (("l", "longo"), ("s", "short"))
        for i in range(len(sp.get(bloco) or []))
        if not os.path.exists(os.path.join(d, f"{pref}{i:02d}.mp3"))
    ]
    if faltam:
        print("  FALTAM:", " ".join(faltam))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
