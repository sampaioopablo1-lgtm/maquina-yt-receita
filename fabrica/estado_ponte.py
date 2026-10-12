#!/usr/bin/env python3
"""Monta o `estado_b64` do `retomar.yml` a partir do corpus. No formato certo.

POR QUE ISTO EXISTE (12/10/2026, e e um defeito MEDIDO, nao precaucao).

No run `38217254505` a publicacao do `kolejny-poziom-s018` morreu no passo
"Publicar pela ponte" com um `AttributeError: 'str' object has no attribute
'get'` dentro de `publicar._iguais_no_estado`. A causa foi minha: eu montei o
estado a mao com `titulos_no_ar` como lista de STRINGS, e a trava por titulo
espera lista de OBJETOS com a chave `titulo`.

Tres coisas nesse episodio merecem conserto, e esta e a primeira:

  1. **a conta estava na minha cabeca.** Eu montei o JSON a mao duas vezes no
     mesmo dia, e na segunda errei a forma. Numero e formato que eu calculo a
     mao viram erro meu mais cedo ou mais tarde;
  2. a conferencia do runner contava o TAMANHO da lista e nao a FORMA dela,
     entao ela passou verde num estado que a trava nao sabia ler. Portao verde
     fabricando "esta tudo certo" e o efeito do 3.8;
  3. o motivo da falha nao chegou a nenhuma anotacao, e o log de job nao e
     legivel por aqui (o `gh` recusa redirecionamento entre hosts). Falha muda
     e pior que falha.

O que NAO foi consertado, de proposito: a trava continuou levantando. Ela
recusou publicar com um estado que nao sabia ler, o que e o comportamento certo
— **o estado malformado nao virou "nenhum titulo no ar"**, que publicaria
duplicata calada. Se ela tivesse sido "corrigida" para tolerar string, o preco
seria duplicata em vez de traceback.
"""
from __future__ import annotations

import base64
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORPUS = os.path.join(RAIZ, "fabrica", "corpus_publicados.json")


def titulos(caminho: str = CORPUS) -> list[str]:
    d = json.load(open(caminho, encoding="utf-8"))
    t = d.get("titulos")
    if not isinstance(t, list) or not t:
        raise SystemExit(f"{caminho} sem a lista `titulos` — sem ela a trava "
                         f"por titulo rodaria contra corpus vazio, que e o "
                         f"mesmo que nao rodar.")
    return [x for x in t if isinstance(x, str) and x.strip()]


def monta(caminho: str = CORPUS) -> dict:
    """O estado no formato que `publicar._iguais_no_estado` LE de verdade.

    `titulos_no_ar` e lista de OBJETOS com a chave `titulo`. Lista de strings
    atravessa a conferencia de tamanho e explode na trava — foi o run
    38217254505.
    """
    t = titulos(caminho)
    return {
        # `{}` e nao `False`: a trava faz `estado.get("ja_publicado") or {}`, e
        # as duas formas funcionam ali, mas `{}` e o que o resto do codigo
        # espera encontrar e nao obriga quem le a conferir a diferenca.
        "ja_publicado": {},
        "titulos_no_ar": [{"titulo": x} for x in t],
        "titulos_no_ar_n": len(t),
    }


def confere(estado: dict) -> list[str]:
    """Os motivos pelos quais este estado NAO serve. Lista vazia = serve.

    Devolve TODOS os motivos, nao o primeiro: quem esta montando o disparo
    quer corrigir de uma vez, nao descobrir um por rodada.
    """
    problemas = []
    n = estado.get("titulos_no_ar_n")
    t = estado.get("titulos_no_ar")
    if n is None:
        problemas.append("sem `titulos_no_ar_n`: sem ele nao da para saber se "
                         "a lista chegou inteira (defeito de 26/08/2026)")
    if not isinstance(t, list) or not t:
        problemas.append("`titulos_no_ar` ausente ou vazio — a trava por "
                         "titulo rodaria contra corpus vazio")
        return problemas
    if n is not None and len(t) != n:
        problemas.append(f"TRUNCADO: chegaram {len(t)} e o estado declara {n}")
    maus = [i for i, x in enumerate(t) if not isinstance(x, dict)]
    if maus:
        problemas.append(
            f"{len(maus)} de {len(t)} entradas de `titulos_no_ar` NAO sao "
            f"objetos (a primeira e o indice {maus[0]}, tipo "
            f"{type(t[maus[0]]).__name__}). A trava faz `l.get('titulo')` e "
            f"levanta AttributeError — foi o run 38217254505.")
    elif not any((x.get("titulo") or "").strip() for x in t):
        problemas.append("nenhuma entrada tem a chave `titulo` preenchida — a "
                         "trava compararia contra vazio e nunca barraria nada")
    return problemas


def titulos_da_spec(caminho_spec: str) -> list[str]:
    """Os titulos que uma spec coloca NO AR, e so eles.

    Short solto (`longo: []`) poe no ar o `TITULO SHORT` e NAO o `TITULO` — o
    segundo e a copy do longo que nao existe. Conferido no corpus de 12/10: as
    pecas `epomeno-epipedo-s016` e `labtreinamento-s013` estao la pelo titulo
    do SHORT, e o do longo nao esta em nenhuma das duas.
    """
    sp = json.load(open(caminho_spec, encoding="utf-8"))
    copy = sp.get("copy") or ""
    fora = []

    def _campo(marca):
        if marca not in copy:
            return None
        return copy.split(marca)[1].split("\n")[0].strip() or None

    curto = _campo("## TITULO SHORT\n")
    longo = _campo("## TITULO\n")
    if sp.get("short") and curto:
        fora.append(curto)
    # So quando ha longo DE VERDADE nesta rodada.
    if sp.get("longo") and longo:
        fora.append(longo)
    if not fora:
        raise SystemExit(f"{caminho_spec}: nenhum titulo a somar — a copy nao "
                         f"tem `## TITULO SHORT` nem ha longo nesta spec.")
    return fora


def adiciona(caminho_spec: str, caminho_corpus: str = CORPUS) -> list[str]:
    """Soma os titulos de uma spec publicada ao corpus. Devolve o que entrou.

    POR QUE ISTO E CODIGO E NAO UM `vim`: nada no repositorio escreve o
    `corpus_publicados.json` — ele e versionado e mantido a mao. Quando ele fica
    atras do que esta no ar, a trava anti-duplicata fica CEGA, e foi assim que o
    `kolejny-poziom-016`, o `labtreinamento-010` e o `epomeno-epipedo-015`
    morreram em tres ciclos seguidos (19:27, 22:49 e 01:27 de 11/10). Esquecer
    de somar e o modo de falha, entao a soma deixa de depender de eu lembrar.

    Idempotente: titulo que ja esta nao entra duas vezes. A lista sai ORDENADA,
    como o arquivo ja e, para o diff ficar legivel.
    """
    d = json.load(open(caminho_corpus, encoding="utf-8"))
    atuais = list(d.get("titulos") or [])
    entrou = [t for t in titulos_da_spec(caminho_spec) if t not in atuais]
    if entrou:
        d["titulos"] = sorted(atuais + entrou)
        with open(caminho_corpus, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return entrou


def main() -> int:
    if len(sys.argv) > 2 and sys.argv[1] == "adiciona":
        entrou = adiciona(sys.argv[2])
        print(f"entraram no corpus: {entrou or 'nada (ja estavam)'}",
              file=sys.stderr)
        return 0
    est = monta(sys.argv[1] if len(sys.argv) > 1 else CORPUS)
    ruins = confere(est)
    if ruins:
        for r in ruins:
            print(f"::error::estado invalido: {r}", file=sys.stderr)
        return 2
    b = base64.b64encode(json.dumps(est, ensure_ascii=False).encode()).decode()
    print(b)
    print(f"estado: {est['titulos_no_ar_n']} titulos | {len(b)} chars b64",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
