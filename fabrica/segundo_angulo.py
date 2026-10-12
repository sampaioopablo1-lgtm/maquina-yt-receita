#!/usr/bin/env python3
"""Capitulos AINDA NAO USADOS de um longo que ja rendeu short. Tudo local.

POR QUE ISTO EXISTE (12/10/2026, e nasce do passo que eu fiz A MAO na rodada das
11:07). O achado da rodada anterior foi que **a unidade de pauta e (longo,
familia de capitulo), nao o longo**: 48 das 49 origens tinham sido usadas UMA vez
e eu tratava cada longo como uso unico por habito.

Para escrever o primeiro segundo angulo eu precisei de tres passos, e dois deles
eram frageis:

  1. listar origens usadas uma vez — `pauta_viva.por_uso` ja faz, mas ele roda no
     RUNNER porque le a playlist de uploads;
  2. **achar qual spec LOCAL carrega os capitulos daquele longo** — eu descobri
     lendo a PROSA do AVISO do short ("...do longo labtreinamento-010
     (6BeNHqT2okA)"). Isso e adivinhacao de texto, e quebra na primeira spec que
     escrever o aviso de outro jeito;
  3. ver quais capitulos o short existente ja consumiu.

**E A MINHA PRIMEIRA TENTATIVA DE CONSERTO ESTAVA ERRADA, medido no ato:** eu
escrevi este modulo resolvendo `youtube_id -> pacote` pelo retrato
`fabrica/ponte/videos.json`, e fui testar no caso real. O retrato **nao tem** o
`6BeNHqT2okA` nem o pacote `labtreinamento-010` — nenhum dos dois, em nenhuma
linha. O longo e anterior ao retrato ou nunca foi registrado nele. Logo **nao
existe mapeamento estruturado local de id de origem para spec de pacote**: o par
existe so na PROSA que eu mesmo escrevi no aviso do short.

**O que o modulo faz no lugar:** procura, dentro da copy do short, o nome de uma
spec que EXISTE em `fabrica/specs/`. Isso nao e adivinhacao de prosa — e casar
contra um vocabulario FECHADO, o conjunto dos nomes de spec do repositorio, e
qualquer acerto e verificavel abrindo o arquivo.

**A limitacao que fica declarada:** isso depende da convencao de o aviso do short
nomear o pacote de origem. E convencao, nao garantia. Quando falha, o modulo diz
que falhou e manda usar o `capitulos.yml` com `legenda=true`, que nao depende de
convencao nenhuma.

**E ELE DEU FALSO POSITIVO NA PRIMEIRA VEZ QUE EU O USEI PARA ESCOLHER — medido
as 12:1x de 12/10, uma rodada depois de eu o escrever.** Tres origens do kolejny
(`MjI4ZGJAhIo`, `SP7Vz8qHdRY`, `Xgt32iH8Ft8`) resolveram para a spec
`kolejny-poziom`, que e o SLUG DO CANAL e tem dez cenas de longo. E verdade
conhecida que isso esta errado em pelo menos um caso: o docstring do
`kolejny-poziom-s017` diz, escrito por mim em 11/10, que o `Xgt32iH8Ft8` e do
pacote `kp-plan-9233-20260811` e que **nao tem spec em `fabrica/specs/`**. A
resposta certa ali e None, e o modulo devolvia um pacote.

Duas causas, e as duas tem conserto:
  1. **o nome casava sem FRONTEIRA**, entao `kolejny-poziom` casava dentro de
     `kolejny-poziom-s017`. Agora a busca exige que o nome nao seja seguido nem
     precedido de `-` ou de caractere de palavra;
  2. **o slug do canal nao e nome de pacote.** A spec homonima do canal e
     generica ou legada, e por isso ela sai da lista de candidatos.

**E o que sobra de duvida sai MARCADO, nao escondido:** pacote resolvido com
menos de VINTE cenas de longo vira `suspeito=True`, porque os longos de verdade
da frota medem **56 a 90 capitulos** e os unicos casos de dez eram esse falso
positivo. O limiar e observado, nao inventado, e a procedencia esta nesta linha.

**O QUE ELE NAO FAZ, e nao e timidez:** ele nao escolhe capitulo e nao nomeia familia —
familia. Capitulo e conteudo que vai ao ar, e a familia de entrada errada e
julgamento — a regra (e) pede ARITMETICA, a (f) pede familia nao repetida no dia,
e o `similaridade` tem a palavra final. O modulo entrega a lista; a escolha e de
quem escreve.

**E ele nao garante que o capitulo esta livre.** Ele marca os que a copy do short
existente MENCIONA pelo kicker, o que e indicio e nao prova: um short pode usar o
conteudo de um capitulo sem citar o kicker dele. Por isso a saida separa
"mencionado" de "nao mencionado" em vez de dizer "usado" e "livre".
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPECS = os.path.join(RAIZ, "fabrica", "specs")


# Cenas de longo abaixo disto: nao e longo, e a resolucao vai MARCADA.
# OBSERVADO na frota — os longos de verdade medem 56 a 90 capitulos, e os unicos
# casos de dez eram o falso positivo do slug do canal (12/10 12:1x).
MIN_CAPITULOS_PLAUSIVEL = 20


def slugs_de_canal(dir_specs: str = SPECS) -> set:
    """Os `slug` que as specs declaram. Slug de canal NAO e nome de pacote."""
    fora = set()
    for p in glob.glob(os.path.join(dir_specs, "*.json")):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            continue
        if sp.get("slug"):
            fora.add(str(sp["slug"]))
    return fora


def nomes_de_spec(dir_specs: str = SPECS) -> list:
    """O vocabulario FECHADO: os nomes de spec que existem no repositorio.

    SEM os nomes que sao slug de canal: a spec homonima do canal e generica ou
    legada, e foi ela que produziu o falso positivo de 12/10 em tres origens.
    Ordenado do mais longo para o mais curto, para que `labtreinamento-010` case
    antes de um hipotetico `labtreinamento-01`.
    """
    slugs = slugs_de_canal(dir_specs)
    nomes = [os.path.basename(p)[:-5]
             for p in glob.glob(os.path.join(dir_specs, "*.json"))]
    return sorted((n for n in nomes if n not in slugs), key=len, reverse=True)


def _casa_inteiro(nome: str, texto: str) -> bool:
    """O nome aparece como identificador INTEIRO, nao como prefixo de outro.

    Sem isto `kolejny-poziom` casa dentro de `kolejny-poziom-s017`.
    """
    return re.search(r"(?<![\w-])" + re.escape(nome) + r"(?![\w-])",
                     texto, re.IGNORECASE) is not None


def pacote_do_id(yid: str, dir_specs: str = SPECS) -> str | None:
    """`youtube_id` -> spec de pacote que carrega os capitulos daquele longo.

    Resolvido pela copy do SHORT que declara esta origem: procura nela o nome de
    uma spec que EXISTE, e exige que essa spec tenha cenas de longo. Casar contra
    vocabulario fechado, e nao contra um padrao de texto.

    Devolve None quando a convencao nao foi seguida — e aí a rota e o
    `capitulos.yml` com `legenda=true`, que nao depende de convencao.
    """
    vocab = nomes_de_spec(dir_specs)
    for nome, copy in shorts_da_origem(yid, dir_specs):
        for cand in vocab:
            if cand == nome or not _casa_inteiro(cand, copy):
                continue
            if capitulos_do_pacote(cand, dir_specs):
                return cand
    return None


def capitulos_do_pacote(pacote: str, dir_specs: str = SPECS) -> list:
    """Os kickers das cenas do LONGO daquele pacote. Lista vazia se nao houver."""
    p = os.path.join(dir_specs, f"{pacote}.json")
    if not os.path.exists(p):
        return []
    try:
        sp = json.load(open(p, encoding="utf-8"))
    except Exception:                                       # noqa: BLE001
        return []
    return [(c.get("kicker") or "").strip()
            for c in (sp.get("longo") or []) if isinstance(c, dict)]


def shorts_da_origem(yid: str, dir_specs: str = SPECS) -> list:
    """As specs de short que declaram `longo_existente == yid`."""
    fora = []
    for p in sorted(glob.glob(os.path.join(dir_specs, "*.json"))):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            continue
        if sp.get("longo_existente") == yid:
            fora.append((os.path.basename(p)[:-5], sp.get("copy") or ""))
    return fora


def nao_mencionados(yid: str, dir_specs: str = SPECS) -> dict:
    """Capitulos cujo kicker NAO aparece na copy de nenhum short desta origem.

    "Nao mencionado" e INDICIO de capitulo livre, nao prova: um short pode usar o
    conteudo sem citar o kicker. A saida devolve as duas listas para que quem
    escreve decida olhando, em vez de confiar num rotulo.
    """
    pacote = pacote_do_id(yid, dir_specs)
    caps = capitulos_do_pacote(pacote, dir_specs) if pacote else []
    usados = shorts_da_origem(yid, dir_specs)
    copys = " ".join(c for _, c in usados).lower()
    men, nao = [], []
    for k in caps:
        if not k:
            continue
        (men if k.lower() in copys else nao).append(k)
    return {"pacote": pacote, "n_capitulos": len(caps),
            "suspeito": bool(pacote) and 0 < len(caps) < MIN_CAPITULOS_PLAUSIVEL,
            "shorts": [n for n, _ in usados],
            "mencionados": men, "nao_mencionados": nao}


def main() -> int:
    if len(sys.argv) > 1:
        alvos = sys.argv[1:]
    else:
        # Sem argumento: toda origem que JA rendeu short, uma vez ou mais.
        vistos = {}
        for p in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
            try:
                sp = json.load(open(p, encoding="utf-8"))
            except Exception:                               # noqa: BLE001
                continue
            le = sp.get("longo_existente")
            if le:
                vistos.setdefault(le, 0)
                vistos[le] += 1
        alvos = sorted(vistos)
    for yid in alvos:
        d = nao_mencionados(yid)
        if not d["pacote"]:
            print(f"{yid}: a copy do short nao nomeia nenhuma spec de pacote com "
                  f"cenas de longo. Use capitulos.yml com legenda=true (regra h).")
            continue
        if not d["n_capitulos"]:
            print(f"{yid}: pacote {d['pacote']} sem cenas de longo na spec — "
                  f"use capitulos.yml com legenda=true.")
            continue
        marca = "  *** SUSPEITO: poucas cenas para um longo — confira com " \
                "capitulos.yml antes de usar" if d["suspeito"] else ""
        print(f"{yid} | pacote {d['pacote']} | {d['n_capitulos']} capitulos | "
              f"shorts: {', '.join(d['shorts']) or 'nenhum'}{marca}")
        print(f"   mencionados pela copy ({len(d['mencionados'])}): "
              f"{', '.join(d['mencionados'][:6])}")
        print(f"   NAO mencionados ({len(d['nao_mencionados'])}) — indicio, nao "
              f"prova: {', '.join(d['nao_mencionados'][:10])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
