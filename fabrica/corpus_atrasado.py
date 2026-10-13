#!/usr/bin/env python3
"""Dizer quando o CORPUS anti-duplicata ficou atras do que ja esta no ar.

POR QUE ISTO EXISTE, e e um defeito meu de SETE rodadas seguidas. Medido em
13/10/2026 as 00:2x: o `fabrica/corpus_publicados.json` estava atualizado ate o
`labtreinamento-s019` (`oAAxm8VzjOc`, 17:13 de 12/10) e NAO continha nenhuma das
sete pecas seguintes:

    s020 JMCd5A3EkAk  "O meio-termo tem dono"
    s021 _7elt-RrXtc  "O maior trabalho do ano engana"
    s022 XF4vlWrTlgs  "Desculpa de preco tem prazo"
    s023 hIwgOn6ISWc  "Um e caso, tres e padrao"
    s024 BdRrDImJBgk  "Quem ja sabe esta vendendo"
    s025 Gzx7m87SSus  "Nao anotou? Da para reconstruir"
    s026 CdUiplaeP5g  "Mude uma coisa so no seu preco"

O passo de registro e MANUAL enquanto o REST do Supabase esta em 402: o
`retomar.yml` publica e emite o `::notice:: PUBLICADO`, e sou EU que acrescento
o titulo ao corpus e comito. Eu fiz isso ate o s019 e parei, sem que nada
reclamasse — porque **nenhum portao le o corpus contra o que esta no ar**. O
`prontidao` le o corpus para barrar titulo duplicado, e um corpus atrasado
simplesmente nao barra: a falha e SILENCIOSA e no sentido permissivo, que e o
pior sentido. Assinatura do paragrafo 3.8 mais uma vez.

E CUIDADO COM A FORMA DO TITULO, porque eu errei isto na primeira medicao desta
mesma rodada: o corpus guarda o **TITULO SHORT** (`## TITULO SHORT` da copy, que
e o titulo que o YouTube recebe no short), e NAO o `## TITULO` longo. Eu grepei
a forma longa, achei zero, e quase relatei que "o corpus parou de crescer quando
a publicacao mudou para o retomar.yml" — conclusao errada por um fator de
dezessete pecas. O `titulo=` do proprio notice do runner e a forma certa.

Este modulo NAO fala com o GitHub e NAO adivinha: ele recebe os titulos que
estao no ar (a forma mais barata e colar os `titulo=` dos notices do
`retomar.yml`) e diz quais faltam. Comparar por igualdade exata depois de
normalizar espaco — nao por similaridade — porque aqui a pergunta e "este
titulo exato ja esta registrado?", e nao "parece com algum?".
"""
from __future__ import annotations

import json
import os
import re
import sys

CORPUS = os.path.join(os.path.dirname(__file__), "corpus_publicados.json")


def _norm(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def carrega(caminho: str = CORPUS) -> list[str]:
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)["titulos"]


def titulos_dos_notices(texto: str) -> list[tuple[str, str, str]]:
    """(pacote, youtube_id, titulo) de cada linha `PUBLICADO ...` do runner.

    A linha tem a forma
      PUBLICADO <pacote> shorts youtube_id=<id> titulo=<titulo> em=<iso>
    e o titulo pode conter espaco, entao ele vai ate o ` em=` final. Linha sem
    `youtube_id` de verdade (o `youtube_id=?` que aparece em run abortado) e
    DESCARTADA: registrar titulo de peca que nao subiu poluiria a trava.
    """
    out = []
    for m in re.finditer(
            r"PUBLICADO\s+(\S+)\s+\S+\s+youtube_id=(\S+)\s+titulo=(.*?)\s+em=",
            texto):
        pacote, yid, titulo = m.group(1), m.group(2), _norm(m.group(3))
        if yid in ("?", "") or not titulo:
            continue
        out.append((pacote, yid, titulo))
    return out


def faltantes(no_ar: list[str], corpus: list[str] | None = None) -> list[str]:
    """Titulos que estao no ar e NAO estao no corpus, na ordem recebida."""
    if corpus is None:
        corpus = carrega()
    tem = {_norm(t) for t in corpus}
    vistos, falta = set(), []
    for t in no_ar:
        n = _norm(t)
        if n not in tem and n not in vistos:
            vistos.add(n)
            falta.append(n)
    return falta


def aplicar(novos: list[str], caminho: str = CORPUS) -> int:
    """Acrescenta os que faltam ao fim do corpus. Devolve quantos entraram."""
    with open(caminho, encoding="utf-8") as f:
        d = json.load(f)
    falta = faltantes(novos, d["titulos"])
    if not falta:
        return 0
    d["titulos"].extend(falta)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    return len(falta)


def relato(no_ar: list[str], corpus: list[str] | None = None) -> str:
    if corpus is None:
        corpus = carrega()
    falta = faltantes(no_ar, corpus)
    linhas = [f"CORPUS: {len(corpus)} titulos registrados, "
              f"{len(no_ar)} titulos conferidos."]
    if not falta:
        linhas.append("  em dia — nada a acrescentar.")
        return "\n".join(linhas)
    linhas.append(f"  ATRASADO em {len(falta)}: a trava por titulo do "
                  "`prontidao` NAO esta barrando estes, e a falha e silenciosa "
                  "e permissiva.")
    linhas += [f"    - {t}" for t in falta]
    linhas.append("  rode com --aplicar para acrescentar, e COMITE: mudanca "
                  "que fica no container morre com ele.")
    return "\n".join(linhas)


def main() -> int:
    texto = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not texto:
        print(__doc__)
        print("uso: <notices do retomar.yml> | corpus_atrasado.py [--aplicar]")
        return 2
    no_ar = [t for _, _, t in titulos_dos_notices(texto)]
    if not no_ar:
        no_ar = [l.strip() for l in texto.splitlines() if l.strip()]
    print(relato(no_ar))
    if "--aplicar" in sys.argv:
        n = aplicar(no_ar)
        print(f"  acrescentados: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
