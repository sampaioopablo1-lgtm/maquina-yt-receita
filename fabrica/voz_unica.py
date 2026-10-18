#!/usr/bin/env python3
"""UMA VOZ SO POR PECA — o provedor de narracao e decidido pela PECA, nunca pela cena.

POR QUE ISTO EXISTE, medido antes de existir. O `fabrica.py` tenta o edge-tts
tres vezes POR CENA e cai no Piper na terceira falha. Em 16/10/2026 isso
produziu TRES pecas publicadas com voz MISTA, contadas pelos avisos
`NARRACAO PELO PIPER` na anotacao do job do render:

    labtreinamento-s060   2 de 10 cenas pelo Piper   job 116943785023
    labtreinamento-s061   1 de 10                    job 116989849294
    labtreinamento-s062   2 de 10                    job 117070798289

E o Piper do pt-BR e `pt_BR-faber-medium`, voz MASCULINA, dentro de um short
narrado pela Thalita, FEMININA (`voz_piper.VOZES`). Logo essas tres pecas
trocam de voz E de genero no meio de quarenta segundos — e o portao
`identidade` (601) nao as pegou, porque ele le a SPEC e nao o audio. O
`tests/test_o_run_pode_ser_MISTO.py` registrou o regime misto como problema
da BANDA (ponto sem mundo de provedor). Ele e tambem um defeito AUDIVEL, e
foi ao ar tres vezes.

A CONVERGENCIA, e e por ela que isto entrou agora: o `pipeline_canal_dark_v2.0`
que o dono mandou em 18/10 tem a regra escrita — *"uma voz so por video: se a
online cair no meio, os blocos ja feitos sao refeitos com a local, para o video
nao trocar de voz"* (`guia/04_VOZ.md`, `motor/narracao.py`). Entra pela regra
da §5: a medicao e NOSSA (tres pecas), a fonte so nomeou a saida.

A SAIDA, em duas etapas, e nesta ordem:
  1. Para cada cena que caiu no Piper, UMA tentativa a mais do edge. A queda
     medida foi de 1 a 2 cenas em 10, logo o edge estava de pe no run — a
     chance de recuperar a voz do canal (que e identidade, 601) e alta e custa
     no maximo um timeout por cena.
  2. Se ainda sobrar cena do Piper, TODAS as cenas do edge sao refeitas pelo
     Piper. Para o Piper e nao para o edge porque o edge acabou de falhar duas
     vezes neste run e o Piper e offline — unificar para o lado que falha e
     promessa, unificar para o que acabou de funcionar e certeza.

E A CONSEQUENCIA PARA O INSTRUMENTO DO 733: a contagem de avisos volta a ser
0 ou N (cenas), nunca entre os dois. O aviso sai UMA vez por cena no estado
FINAL, depois da unificacao — imprimi-lo na hora da queda deixaria a anotacao
contando um estado que a peca publicada nao tem.

O que este modulo NAO faz: nao sintetiza nada e nao importa nada pesado. Ele
decide (`plano`) e marca no disco qual cena foi narrada pelo Piper (`marcar`),
porque a RETOMA do `fabrica.py` reaproveita mp3 valido de um run anterior e
sem marca nao haveria como saber quem narrou aquele arquivo.
"""
from __future__ import annotations

import os

# Arquivo lateral ao mp3 da cena: `s03.mp3.piper`. Sem ele, a cena e do edge.
MARCA = ".piper"

REGIMES = ("nenhuma", "edge", "piper", "misto")


def marca(alvo_mp3: str) -> str:
    return alvo_mp3 + MARCA


def marcar(alvo_mp3: str) -> None:
    with open(marca(alvo_mp3), "w", encoding="utf-8") as f:
        f.write("piper\n")


def desmarcar(alvo_mp3: str) -> None:
    try:
        os.remove(marca(alvo_mp3))
    except OSError:
        pass


def marcado(alvo_mp3: str) -> bool:
    return os.path.exists(marca(alvo_mp3))


def regime(pela_piper, total: int) -> str:
    """'edge', 'piper' ou 'misto' — a leitura do 733 com os tres valores, nao dois."""
    if total <= 0:
        return "nenhuma"
    n = len(set(pela_piper) & set(range(total)))
    if n == 0:
        return "edge"
    if n == total:
        return "piper"
    return "misto"


def plano(pela_piper, total: int) -> dict:
    """O que refazer para a peca ter UMA voz.

    Em regime misto devolve as cenas do EDGE (as que faltam para o Piper
    cobrir a peca inteira). Nos outros regimes nao ha nada a refazer.
    """
    r = regime(pela_piper, total)
    refazer = sorted(set(range(total)) - set(pela_piper)) if r == "misto" else []
    return {"regime": r, "refazer": refazer, "com": "piper" if refazer else None}


def relato(pela_piper, total: int, recuperadas=()) -> str:
    r = regime(pela_piper, total)
    base = f"narracao: regime {r} ({len(set(pela_piper))} de {total} cenas pelo Piper)"
    if recuperadas:
        base += f"; {len(recuperadas)} cena(s) voltaram ao edge na tentativa extra"
    return base
