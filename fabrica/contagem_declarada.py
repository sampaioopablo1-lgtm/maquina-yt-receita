#!/usr/bin/env python3
"""A FONTE declara "esses cinco casos" e enumera SEIS: achar isso antes de copiar.

POR QUE ISTO EXISTE, e e defeito da FONTE e nao meu. Em 13/10/2026, as 05:0x,
escrevendo um short a partir do longo `labtreinamento-009` (`dsoEo103l1o`), eu
li no capitulo 35 *"depois de descartar esses CINCO casos"* — e os capitulos 28 a
33 enumeram **SEIS**. O proprio longo tambem diz "os seis casos" em outro ponto,
logo ele se contradiz sozinho.

**Por que isso importa mais do que parece:** o short carrega o que o longo diz, e
numero de contagem passa por todos os nossos portoes. O `narracao` conta
QUANTIDADES por frase, nao confere se a quantidade e verdadeira; a regra (g) tira
numero que MUDA (aliquota, data), e contagem de casos nao muda — logo nada barra
"os cinco casos" num short cujo longo tem seis. Seria numero errado no ar, com
portao verde: a assinatura do paragrafo 3.8.

**E O PRIMEIRO DETECTOR QUE EU ESCREVI SOBRECONTAVA.** Ele comparava a declaracao
com QUALQUER kicker ordinal do longo, e no `labtreinamento-009` havia um
"Primeiro passo" alem dos seis "<ordinal> caso" — sete ordinais, logo ele acusava
"cinco contra sete" e "seis contra sete", sendo que a enumeracao de CASOS e seis.
Reportar aquilo como achado seria inventar dois defeitos e errar o terceiro.
**O detector tem de casar o SUBSTANTIVO:** "cinco casos" compara com os kickers
`<ordinal> caso`, nao com `<ordinal> passo`.

O que ele NAO faz: nao corrige texto e nao reprova spec. Ele aponta, e quem
escreve decide — no `s031` a decisao foi **omitir a contagem**, porque eu nao sei
qual numero o autor quis e inventar um e pior que nao dizer.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

NUMERAL = {"dois": 2, "duas": 2, "tres": 3, "três": 3, "quatro": 4, "cinco": 5,
           "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10}
ORDINAL = ["primeiro", "segundo", "terceiro", "quarto", "quinto", "sexto",
           "setimo", "sétimo", "oitavo", "nono", "decimo", "décimo"]

# Plural -> singular dos substantivos que a fonte costuma enumerar. Fechado de
# proposito: lista curta e previsivel vale mais que stemmer que erra calado.
SINGULAR = {"casos": "caso", "passos": "passo", "razoes": "razao",
            "razões": "razão", "pontos": "ponto", "itens": "item",
            "motivos": "motivo", "etapas": "etapa", "regras": "regra",
            "criterios": "critério", "critérios": "critério"}

_DECL = re.compile(
    r"(?:esses|estes|essas|estas|os|as)\s+(" + "|".join(NUMERAL) + r")\s+("
    + "|".join(SINGULAR) + r")\b")


def _norm(s: str) -> str:
    return (s or "").strip().lower()


JANELA = 12          # capitulos de distancia que ainda contam como "a mesma lista"


def enumerados(longo: list[dict], singular: str, perto_de: int = None) -> int:
    """Quantos capitulos tem kicker `<ordinal> <singular>` — ou so `<ordinal>`.

    O casamento do SUBSTANTIVO e o ponto: sem ele, um "Primeiro passo" entra na
    contagem de "casos" e o detector inventa divergencia. Quando NENHUM kicker
    traz o substantivo, caimos nos ordinais nus (que e como varios longos
    escrevem: "Primeiro caso" / "Segundo" / "Terceiro"), e isso vai declarado no
    retorno como `por_ordinal_nu`.
    """
    com_sub, nus = 0, []
    for i, c in enumerate(longo):
        k = _norm(c.get("kicker"))
        k = re.sub(r"^(o|a)\s+", "", k)
        m = re.match(r"(" + "|".join(ORDINAL) + r")\b(.*)$", k)
        if not m:
            continue
        resto = m.group(2).strip()
        if resto.startswith(singular):
            com_sub += 1
        elif not resto:
            nus.append(i)
    if com_sub:
        return com_sub
    # SEGUNDO FALSO POSITIVO DO MESMO DETECTOR, medido na mesma rodada: no
    # `labtreinamento-010` a declaracao "os dois casos" esta no capitulo 20 e
    # fala de dois TIPOS de acidente, enquanto os quatro ordinais nus (59 a 62)
    # sao um checklist de fechamento — outra lista, outro assunto. Pareei as
    # duas por proximidade NENHUMA e acusei "dois contra quatro".
    # Logo o ordinal nu so conta quando esta PERTO da declaracao: no 009 a
    # declaracao esta no 35 e os casos no 28 a 33.
    if perto_de is None:
        return 0
    return sum(1 for i in nus if abs(i - perto_de) <= JANELA)


def divergencias(spec: dict) -> list[dict]:
    """Declaracoes de contagem que NAO batem com a enumeracao do mesmo longo."""
    longo = spec.get("longo") or []
    if not longo:
        return []
    out, vistos = [], set()
    for idx, c in enumerate(longo):
        texto = _norm(c.get("nar")) + " " + _norm(c.get("kicker"))
        for m in _DECL.finditer(texto):
            declarado, plural = NUMERAL[m.group(1)], m.group(2)
            singular = SINGULAR[plural]
            n = enumerados(longo, singular, perto_de=idx)
            chave = (m.group(0), n)
            if n and declarado != n and chave not in vistos:
                vistos.add(chave)
                out.append({"declaracao": m.group(0), "declarado": declarado,
                            "enumerados": n, "substantivo": singular,
                            "capitulo": idx})
    return out


def relato(caminho: str) -> str:
    with open(caminho, encoding="utf-8") as f:
        spec = json.load(f)
    d = divergencias(spec)
    nome = os.path.basename(caminho)
    if not d:
        return f"{nome}: nenhuma contagem declarada em conflito."
    linhas = [f"{nome}: {len(d)} contagem(ns) declarada(s) em CONFLITO com a "
              "enumeracao do proprio longo."]
    for x in d:
        linhas.append(f"  \"{x['declaracao']}\" — mas o longo enumera "
                      f"{x['enumerados']} `{x['substantivo']}`.")
    linhas.append("  NAO copie a contagem para o short. Omitir e melhor que "
                  "inventar: o autor pode ter querido qualquer um dos dois.")
    return "\n".join(linhas)


def main() -> int:
    alvos = sys.argv[1:] or sorted(glob.glob(
        os.path.join(os.path.dirname(__file__), "specs", "*.json")))
    achou = 0
    for a in alvos:
        t = relato(a)
        if "CONFLITO" in t:
            print(t)
            achou += 1
    print(f"\n{achou} spec(s) com conflito, de {len(alvos)} conferida(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
