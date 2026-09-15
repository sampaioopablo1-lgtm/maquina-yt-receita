#!/usr/bin/env python3
"""Resolve o b-roll do Pexels FORA do runner e grava o link na spec.

POR QUE ISTO EXISTE, com o numero que o motivou.

O `broll.py` funciona: o agla-level-004 saiu com footage e credito em
`broll_creditos.json`. Mas em 19/08/2026 o epomeno-epipedo-004 perdeu SETE de
sete cenas com `TimeoutError: The read operation timed out`, e o kolejny-005 e
o kolejny-006 registraram "SEM BROLL: o Pexels da TimeoutError a partir do
runner". A mesma chave responde do sandbox: medido em 07/09/2026,
`api.pexels.com` devolve HTTP 200 com TLS em 68 ms de la.

Isso nao e lentidao, e bloqueio contra a faixa de IP do runner do GitHub. Retry
nao vence bloqueio: as tres tentativas do `buscar()` so gastam 90 s por cena
antes de cair no fallback, e um longo com oito cenas de broll perde doze
minutos de render para nao trazer footage nenhum.

A SAIDA E QUE SAO DOIS HOSTS DIFERENTES. `api.pexels.com` e a API autenticada;
`videos.pexels.com` e o CDN dos arquivos. So a API precisa de chave e so ela
mostrou o bloqueio. Entao a BUSCA sai do runner — este script roda onde a API
responde (sandbox, ou a sua maquina), escolhe o clipe de cada cena e grava
`broll_url` e `broll_credito` na propria spec. O runner passa a so baixar do
CDN, sem chave e sem cota.

O QUE ISSO TAMBEM RESOLVE, de graca: a spec passa a ser reproduzivel. Hoje dois
renders da mesma spec podem pegar clipes diferentes, porque a busca e refeita e
o Pexels reordena. Com o link gravado, o pacote rende igual amanha.

E O QUE ISSO **NAO** RESOLVE: se o CDN tambem estiver bloqueado no runner, o
download morre igual — so que agora o log diz exatamente isso, em vez de somar
a falha da busca com a do download. Rode `--conferir` para saber antes de
gastar render.

USO:
    # com SB/KEY no ambiente (le config.pexels_api_key), ou PEXELS_API_KEY
    python3 fabrica/prebusca_broll.py fabrica/specs/<pacote>.json
    python3 fabrica/prebusca_broll.py fabrica/specs/<pacote>.json --conferir
"""
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broll  # noqa: E402


# Folga sobre a duracao ESTIMADA da cena. A duracao real so existe depois do
# TTS, e o `escolher` recusa clipe mais curto que a fala — cortar clipe curto
# congela o ultimo frame, que e a estatica que o broll veio matar. Tres
# segundos cobrem com folga o desvio do modelo de voz, que chega a 4,9%.
FOLGA_S = 3.0


def _dur_estimada(cena, voz):
    from ensaio import duracao_cena
    return duracao_cena(cena.get("nar") or "", voz) + FOLGA_S


def _cdn_responde(link):
    """O CDN entrega os primeiros bytes? Sem baixar o arquivo inteiro."""
    req = urllib.request.Request(
        link, headers={"User-Agent": "curl/8", "Range": "bytes=0-1023"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=broll._ctx()) as r:
            return len(r.read(1024)) > 0
    except Exception as e:
        print(f"    CDN recusou: {type(e).__name__}: {e}")
        return False


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    caminho = argv[0]
    conferir = "--conferir" in argv

    sp = json.load(open(caminho, encoding="utf-8"))
    voz = sp.get("voz", "")
    cenas = sp.get("longo") or []
    alvos = [(i, c) for i, c in enumerate(cenas) if c.get("layout") == "broll"]
    if not alvos:
        print(f"{caminho}: nenhuma cena com layout `broll` — nada a fazer.")
        return 0

    api_key = broll.chave()
    print(f"chave do Pexels: {broll.ORIGEM_DA_CHAVE}")
    if not api_key:
        print("sem chave: exporte PEXELS_API_KEY, ou SB/KEY para ler "
              "config.pexels_api_key.")
        return 1

    achou = faltou = 0
    for i, c in alvos:
        q = (c.get("broll_q") or "").strip()
        if not q:
            print(f"  cena {i:2d}: sem broll_q — pulada")
            faltou += 1
            continue
        dd = _dur_estimada(c, voz)
        try:
            resultado = broll.escolher(broll.buscar(q, api_key), dd)
        except Exception as e:
            print(f"  cena {i:2d}: busca falhou — {type(e).__name__}: {e}")
            faltou += 1
            continue
        if not resultado:
            print(f"  cena {i:2d}: sem candidato para {q!r} "
                  f"(paisagem, >= {dd + 1:.1f}s, >= 1280px)")
            faltou += 1
            continue
        link, credito = resultado
        if conferir and not _cdn_responde(link):
            faltou += 1
            continue
        c["broll_url"] = link
        c["broll_credito"] = credito
        achou += 1
        print(f"  cena {i:2d}: {q!r} -> pexels {credito['pexels_id']} "
              f"({credito.get('autor') or 'sem autor'})")

    if conferir:
        print(f"\nCONFERIDO, nada gravado: {achou}/{len(alvos)} cenas com "
              f"clipe que o CDN entrega.")
        return 0 if faltou == 0 else 1

    json.dump(sp, open(caminho, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\n{caminho}: {achou}/{len(alvos)} cenas com broll_url gravado"
          + (f", {faltou} sem" if faltou else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
