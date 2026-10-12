#!/usr/bin/env python3
"""Origem livre lida da PLAYLIST DE UPLOADS, ao vivo. Sem banco e sem retrato.

POR QUE ISTO EXISTE (12/10/2026, e substitui uma reconstrucao que estava CEGA).

Com o gateway do Supabase em 402 eu passei a reconstruir a pauta do retrato
`fabrica/ponte/videos.json` (`fabrica/pauta_local.py`). Aquele arquivo e de
**06/10**, e eu escrevi a ressalva certa — "longo publicado depois nao aparece,
entao o numero SUBESTIMA" — e depois **tratei o numero como se fosse o estoque**,
tres rodadas seguidas, concluindo "a pauta acabou".

**A ressalva nao era um detalhe: era o buraco.** O `medir.py` ja enumerava a
playlist de UPLOADS de cada canal pela API (`ids_do_canal`), isto e, a lista VIVA
do que esta no ar, sem banco e sem retrato. O instrumento certo existia e estava
a um import de distancia.

Isto e o efeito (C) da rotina na forma mais teimosa: **minha lista mente** — e
desta vez a lista era um arquivo congelado que eu mesmo sabia estar congelado.

**O QUE ESTE MODULO FAZ, e o que ele NAO resolve:**
  * ele le titulo, duracao e id de TUDO que esta no ar, agora;
  * separa LONGO de SHORT pela duracao real (`contentDetails.duration`), nao pelo
    nome do pacote — nome de pacote erra, duracao nao;
  * agrupa por TITULO DISTINTO, pela licao do 658/670 e pelo grupo de dez copias
    que me fez contar dez origens onde havia uma;
  * subtrai o `longo_existente` que as specs ja consomem.
  * **so conta longo DA MAQUINA**, cruzando o titulo contra o
    `corpus_publicados.json`. Isto NAO e zelo: na primeira execucao (run
    38228176339) o modulo devolveu **65 "origens livres" no labtreinamento** —
    e eram os VIDEOS DE CURSO DO DONO, anteriores a maquina ("1.Seja
    bem-vindo", "2. Backstage", "Transmissao ao vivo"). E o aprendizado 668 na
    forma de pauta: aquele canal tem acervo anterior, e tratar acervo alheio
    como origem produziria short derivado de aula de Microsoft Project.
    Conferido nos dois sentidos: os tres longos da maquina estao no corpus, os
    tres videos de curso NAO estao;
  * **NAO substitui `consultas/estoque.sql`** no que a consulta faz melhor: ela
    exclui grupo duplicado POR CONSTRUCAO e conhece `origem_id`. Aqui a exclusao
    de duplicata e por titulo, e titulos diferentes para o mesmo conteudo
    passariam.

Roda no RUNNER, onde o `YT_OAUTH_JSON` vive. Nunca imprime segredo.

**E A UNIDADE DE PAUTA NAO E O LONGO — e o par (LONGO, FAMILIA DE CAPITULO).**
Medido em 12/10, e isto retrata "a pauta acabou" pela TERCEIRA vez no mesmo dia:
das 49 origens que as specs consomem, **48 foram usadas UMA vez e uma foi usada
DUAS** (`h04-UVlVevs` -> `epomeno-epipedo-s002` e `-s006`, as duas publicadas, com
entradas erradas diferentes: periodo errado numa, media-contra-marginal na outra).

A regra (e) da rotina ja dizia isso em letra — *"a entrada errada vem do capitulo
que o short ORIGINAL nao usou"* — o que pressupoe que o mesmo longo rende mais de
um short. Eu tratei cada longo como uso UNICO por HABITO, nao por regra, e com
~9 capitulos por longo isso deixou a maior parte da pauta parada.

Por isso o relato traz as DUAS contagens: origem sem nenhum short (o que eu
chamava de "livre") e origem com UM short, que ainda tem capitulo intocado. A
segunda nao e automatica — precisa de familia diferente e de passar o
`similaridade` — mas ela existe e eu nao estava olhando.
"""
from __future__ import annotations

import collections
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

from medir import (CANAIS, ids_do_canal, nota, aviso,          # noqa: E402
                   token_do_canal, uma_chamada, uploads_e_estatisticas)
from oauth_mapa import desembrulha                             # noqa: E402

# Abaixo disto e SHORT. O portao `duracao` recusa short acima de 43,1 s, e o
# longo mais curto da frota passa de dez minutos — nao ha zona cinzenta real,
# mas o limiar fica generoso de proposito: classificar longo como short PERDE
# pauta, e isso e o erro caro aqui.
SEG_MIN_LONGO = 120


def segundos(iso: str | None) -> int | None:
    """`PT12M31S` -> 751. None quando a duracao nao e legivel (P0D inclusive)."""
    if not iso or iso == "P0D":
        return None
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    if not m:
        return None
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    total = h * 3600 + mi * 60 + s
    return total or None


def origens_usadas(dir_specs: str | None = None) -> set:
    dir_specs = dir_specs or os.path.join(RAIZ, "fabrica", "specs")
    fora = set()
    for p in glob.glob(os.path.join(dir_specs, "*.json")):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:                                      # noqa: BLE001
            continue
        if sp.get("longo_existente"):
            fora.add(sp["longo_existente"])
    return fora


def titulos_da_maquina(caminho: str | None = None) -> set:
    """Os titulos que a MAQUINA publicou. O corpus e a unica lista que sabe isso.

    Sem este filtro o modulo conta o acervo anterior a maquina como pauta — foi
    o que aconteceu no run 38228176339 com os 65 videos de curso do
    labtreinamento.
    """
    caminho = caminho or os.path.join(RAIZ, "fabrica", "corpus_publicados.json")
    d = json.load(open(caminho, encoding="utf-8"))
    t = d.get("titulos")
    if not isinstance(t, list) or not t:
        raise SystemExit(f"{caminho} sem a lista `titulos` — sem ela o filtro "
                         f"de acervo alheio nao existe, e o modulo contaria "
                         f"video de terceiro como origem.")
    return {x.strip() for x in t if isinstance(x, str) and x.strip()}


def longos_no_ar(canal: str, cfg: dict, da_maquina: set | None = None) -> dict:
    """{id: (titulo, segundos)} dos LONGOS `processed` DA MAQUINA, ao vivo."""
    token = token_do_canal(cfg)
    playlist, _ = uploads_e_estatisticas(CANAIS[canal], token)
    ids = ids_do_canal(playlist, token)
    itens = uma_chamada(ids, token)
    fora = {}
    for vid, it in itens.items():
        st = (it.get("status") or {}).get("uploadStatus")
        dur = segundos((it.get("contentDetails") or {}).get("duration"))
        # Peca fora de `processed` nao e origem: ela pode nem ficar no ar (665).
        if st != "processed" or not dur or dur < SEG_MIN_LONGO:
            continue
        titulo = ((it.get("snippet") or {}).get("title") or "").strip()
        # Acervo anterior a maquina NAO e pauta (668).
        if da_maquina is not None and titulo not in da_maquina:
            continue
        fora[vid] = titulo
    return {v: (t, 0) for v, t in fora.items()}


def livres(por_canal: dict, usadas: set) -> dict:
    """{canal: [(titulo, [ids...])]} por TITULO DISTINTO, so o que sobrou.

    Grupo em que QUALQUER copia ja foi usada sai INTEIRO: o titulo ja esta
    servido, e um short apontando para a copia irma seria a mesma pauta. Foi
    assim que o `W_iFAIQWvi8` entrou na minha conta errada de 08:2x.
    """
    fora = {}
    for canal, itens in por_canal.items():
        grupos = {}
        for vid, (titulo, _) in itens.items():
            grupos.setdefault(titulo, []).append(vid)
        fora[canal] = [(t, sorted(ids)) for t, ids in sorted(grupos.items())
                       if not any(v in usadas for v in ids)]
    return fora


def por_uso(por_canal: dict, usadas: set) -> dict:
    """{canal: {"sem_short": [...], "um_short": [...]}} por titulo distinto.

    `um_short` e a pauta que eu nao estava vendo: longo com um short publicado e
    capitulos intocados. Ela NAO e automatica — exige familia de entrada errada
    diferente e passar o `similaridade` contra o mesmo canal — mas o precedente
    existe e esta no ar (`h04-UVlVevs` rendeu `epomeno-epipedo-s002` e `-s006`).
    """
    quantos = collections.Counter()
    for p in glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json")):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:                                      # noqa: BLE001
            continue
        if sp.get("longo_existente"):
            quantos[sp["longo_existente"]] += 1
    fora = {}
    for canal, itens in por_canal.items():
        grupos = {}
        for vid, (titulo, _) in itens.items():
            grupos.setdefault(titulo, []).append(vid)
        sem, um = [], []
        for titulo, ids in sorted(grupos.items()):
            # MAX e nao soma: o grupo de copias do mesmo titulo conta uma vez.
            n = max((quantos.get(v, 0) for v in ids), default=0)
            if n == 0:
                sem.append((titulo, sorted(ids)))
            elif n == 1:
                um.append((titulo, sorted(ids)))
        fora[canal] = {"sem_short": sem, "um_short": um}
    return fora


def main() -> int:
    bruto = os.environ.get("YT_OAUTH_JSON") or ""
    if not bruto.strip():
        print("::error::YT_OAUTH_JSON vazio — este modulo roda no RUNNER")
        return 2
    mapa = desembrulha(bruto)
    usadas = origens_usadas()
    da_maquina = titulos_da_maquina()

    por_canal, total_livre, total_ids = {}, 0, 0
    for canal in CANAIS:
        cfg = mapa.get(canal)
        if not cfg:
            aviso(f"{canal}: sem entrada no YT_OAUTH_JSON — NAO contado, e isso "
                  f"faz o total SUBESTIMAR")
            continue
        try:
            por_canal[canal] = longos_no_ar(canal, cfg, da_maquina)
        except Exception as e:                                 # noqa: BLE001
            # Falha de chamada NAO vira "zero origens" (665): grita e sai de fora
            # da conta, em vez de virar silencio com cara de estoque vazio.
            aviso(f"{canal}: leitura FALHOU ({type(e).__name__}) — o total nao "
                  f"inclui este canal")

    L = livres(por_canal, usadas)
    for canal, grupos in L.items():
        total_livre += len(grupos)
        total_ids += sum(len(i) for _, i in grupos)
        nota(f"{canal}: {len(por_canal[canal])} longos DA MAQUINA no ar | "
             f"{len(grupos)} ORIGENS LIVRES (titulo distinto)")
        for titulo, ids in grupos:
            extra = f" [{len(ids)} COPIAS — valem UMA]" if len(ids) > 1 else ""
            nota(f"  {canal} {ids[0]} {titulo[:70]}{extra}")
    nota(f"TOTAL: {total_livre} origens SEM NENHUM short, {total_ids} ids, "
         f"contra {len(usadas)} origens ja usadas por spec")

    # A pauta que eu nao estava vendo: longo com UM short e capitulos intocados.
    U = por_uso(por_canal, usadas)
    soma_um = sum(len(v["um_short"]) for v in U.values())
    for canal, d in U.items():
        if d["um_short"]:
            nota(f"{canal}: +{len(d['um_short'])} longos com UM short e "
                 f"capitulos intocados (pauta de SEGUNDO angulo)")
    nota(f"SEGUNDO ANGULO: {soma_um} longos ja usados UMA vez. A unidade de "
         f"pauta e (longo, familia de capitulo), nao o longo — precedente no ar: "
         f"h04-UVlVevs rendeu epomeno-epipedo-s002 e -s006, familias diferentes. "
         f"NAO e automatico: exige familia nova e passar o similaridade.")
    nota("LIDO DA PLAYLIST DE UPLOADS, ao vivo — nao do retrato de 06/10. "
         "So conta longo DA MAQUINA (titulo no corpus): acervo anterior a "
         "maquina nao e pauta (668). Ressalva que fica: a exclusao de duplicata "
         "aqui e por TITULO, nao pela construcao de consultas/estoque.sql.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
