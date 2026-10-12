#!/usr/bin/env python3
"""Imprime o registro da publicacao como ANOTACAO, com o youtube_id.

POR QUE ISTO EXISTE, e e conserto de um defeito MEU do mesmo dia.

Em 12/10 eu descobri que o `youtube_id` de uma publicacao bem-sucedida nao
chegava a nenhuma anotacao — o registro era so impresso no log, e log de job
nao se le por API quando o MCP do GitHub esta fora. Consertei no commit 1c79c79
pondo um `python3 - <<'PYFIM'` INLINE no `retomar.yml`... e o conserto saiu
errado: ele iterava o TOPO do registro em vez de `linhas`. O run 38223514079
publicou o `epomeno-epipedo-s017` e a anotacao saiu
`PUBLICADO epomeno-epipedo-s017  youtube_id=? titulo=`.

**A licao nao e "eu errei o dicionario". E que eu pus logica dentro do YAML,
onde ela nao tem teste.** O mesmo conserto, em modulo, falha na suite em vez de
falhar em producao — e por isso o parsing mudou de lugar junto com a correcao.

A FORMA REAL DO REGISTRO, lida do log do run 38217420591 e do 38223514079:

    {"canal": ..., "pacote": ..., "linhas": [
        {"slug", "status", "formato", "titulo", "youtube_id", "duracao_s",
         "duracao_short_s", "cenas", "capitulos", "supabase_url", "canal",
         "pacote", "fonte_pauta", "publicado_em"}]}

O registro NAO tem segredo — e youtube_id, titulo e duracao — e imprimi-lo e o
que permite que ele entre no banco pela rota que sobrou.
"""
from __future__ import annotations

import json
import sys


def linhas_do_registro(d) -> list:
    """As linhas publicadas, aceitando as tres formas que o arquivo ja teve.

    Tolerante na LEITURA de propositio, e nunca silenciosa: forma que nao
    produz linha nenhuma devolve `[]`, e quem chama emite aviso em vez de
    imprimir um `youtube_id=?` com cara de dado.
    """
    if isinstance(d, list):
        return [x for x in d if isinstance(x, dict)]
    if not isinstance(d, dict):
        return []
    if isinstance(d.get("linhas"), list):
        return [x for x in d["linhas"] if isinstance(x, dict)]
    # Linha solta, sem envelope: so vale se ela mesma tiver id.
    return [d] if d.get("youtube_id") else []


def anotacoes(d) -> list[str]:
    # O `pacote` do envelope serve de reserva: ele existe nas duas formas, e a
    # linha interna pode nao traze-lo.
    env = d.get("pacote") if isinstance(d, dict) else None
    fora = []
    for it in linhas_do_registro(d):
        yid = it.get("youtube_id")
        if not yid:
            fora.append(f"::warning::linha de registro SEM youtube_id em "
                        f"{it.get('pacote') or env or '?'} — publicou mas nao da para "
                        f"registrar no banco")
            continue
        fora.append(
            f"::notice::PUBLICADO {it.get('pacote') or env or '?'} "
            f"{it.get('formato') or ''} youtube_id={yid} "
            f"titulo={(it.get('titulo') or '')[:120]} "
            f"em={it.get('publicado_em') or '?'}")
    if not fora:
        fora.append("::warning::registro existe mas nao produziu nenhuma linha "
                    "legivel — a FORMA do arquivo mudou, veja "
                    "fabrica/registro_anota.py")
    return fora


def main() -> int:
    caminho = sys.argv[1] if len(sys.argv) > 1 else "/tmp/registro.json"
    try:
        d = json.load(open(caminho, encoding="utf-8"))
    except Exception as e:                                  # noqa: BLE001
        print(f"::warning::nao consegui ler {caminho}: {e}", flush=True)
        return 0
    for linha in anotacoes(d):
        print(linha, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
