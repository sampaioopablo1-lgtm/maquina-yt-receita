#!/usr/bin/env python3
"""Imprime titulo, duracao e CAPITULOS de um longo publicado. Regra (h).

POR QUE ISTO EXISTE (12/10/2026). A rotina ja dizia, desde 09/10, que **origem
livre pode nao ter spec local** — foi medido com o `Xgt32iH8Ft8`, de 11/08,
anterior a convencao de nome atual — e que nesse caso os capitulos saem da
DESCRICAO PUBLICADA pela `videos.list`. A regra existia; o instrumento nao, e
cada vez que o caso aparecia eu montava a chamada a mao.

Em 12/10 o caso voltou duas vezes na mesma hora: o `pauta_viva.py` achou duas
origens livres no epomeno (`eZ697VNYCPU` e `GwNkPfM9pSY`) que **nao tem spec no
repositorio** — elas sao anteriores ou foram publicadas por outro caminho.

Roda no RUNNER, pelo `YT_OAUTH_JSON`. Nao imprime segredo: o access token nasce
e morre dentro do processo, como no `medir.py`.

**O que ele NAO faz:** nao escolhe capitulo e nao escreve roteiro. Capitulo e
conteudo que vai ao ar; a leitura e mecanica, a escolha nao.
"""
from __future__ import annotations

import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

from medir import API, CANAIS, _get, nota, token_do_canal   # noqa: E402
from oauth_mapa import desembrulha                          # noqa: E402

# `00:00 Titulo` ou `0:00 - Titulo`. O marcador de capitulo do YouTube exige o
# primeiro em 00:00, mas aqui a leitura e tolerante: o que interessa e o texto.
MARCA = re.compile(r"^\s*((?:\d{1,2}:)?\d{1,2}:\d{2})\s*[-—–]?\s*(.+?)\s*$")


def capitulos(descricao: str) -> list[tuple[str, str]]:
    fora = []
    for linha in (descricao or "").splitlines():
        m = MARCA.match(linha)
        if m:
            fora.append((m.group(1), m.group(2)))
    return fora


def main() -> int:
    vid = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("VIDEO_ID", "")).strip()
    canal = (sys.argv[2] if len(sys.argv) > 2 else os.environ.get("CANAL", "")).strip()
    if not vid or canal not in CANAIS:
        print(f"::error::uso: capitulos_do_longo.py <video_id> <canal>; "
              f"canais {list(CANAIS)}")
        return 2
    bruto = os.environ.get("YT_OAUTH_JSON") or ""
    if not bruto.strip():
        print("::error::YT_OAUTH_JSON vazio — este modulo roda no RUNNER")
        return 2
    cfg = desembrulha(bruto).get(canal)
    if not cfg:
        print(f"::error::{canal} sem entrada no YT_OAUTH_JSON")
        return 2

    token = token_do_canal(cfg)
    d = _get(f"{API}/videos?part=snippet,contentDetails,status&id={vid}", token)
    itens = d.get("items") or []
    if not itens:
        # Lista vazia NAO e "video sem capitulo": e id errado, canal errado ou
        # peca fora do ar (665). Grita em vez de devolver silencio.
        print(f"::error::{vid} nao voltou nenhum item — id errado, canal errado "
              f"ou peca fora do ar")
        return 2
    it = itens[0]
    sn = it.get("snippet") or {}
    nota(f"{vid} | {sn.get('title','')}")
    nota(f"duracao {(it.get('contentDetails') or {}).get('duration')} | "
         f"status {(it.get('status') or {}).get('uploadStatus')} | "
         f"publicado {sn.get('publishedAt')}")
    caps = capitulos(sn.get("description") or "")
    if not caps:
        nota("NENHUM capitulo marcado na descricao — a descricao inteira sai "
             "abaixo, em pedacos, e a leitura e sua")
        texto = (sn.get("description") or "").strip()
        for i in range(0, min(len(texto), 6000), 600):
            nota(f"desc[{i}:{i+600}] {texto[i:i+600]}")
        return 0
    nota(f"{len(caps)} capitulos:")
    for t, nome in caps:
        nota(f"  {t}  {nome}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
