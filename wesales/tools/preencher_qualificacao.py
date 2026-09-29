#!/usr/bin/env python3
"""Qualificação pré-preenchida com o que o lead já respondeu no anúncio (29/09, pedido do dono).

A derivação de ASSOCIACOES-DE-CAMPO.md §3 rodou uma vez à mão (27/09); lead que chegou depois
ficava com Prazo e Investe em anúncios vazios. Este robô roda no relógio a cada ciclo.

Regras (vocabulário FECHADO: valor desconhecido não deriva nada; só preenche campo VAZIO —
se a SDR já marcou, a palavra dela vale mais):
    Urgência (anúncio)      -> Q6 · Prazo
    Investimento (anúncio)  -> B · Investe em anúncios
    Necessidade (anúncio)   -> Q1 · Dor principal (cópia do texto; a SDR confirma e aprofunda)
Q1 com o valor-lixo "Necessidade (anúncio)" (rótulo gravado no lugar da resposta) é tratado como vazio.

    python3 preencher_qualificacao.py            # DRY
    python3 preencher_qualificacao.py --aplicar
"""
from __future__ import annotations

import sys
from collections import Counter

from atuador_filas import contatos, pedir, valor

URGENCIA, PRAZO = "2LnUD4KYSGkIBwiUdzl3", "lAqbaJE9K4LDkq3t2zzc"
INVEST, INVESTE = "bQithNwReQIBGlZBaNlI", "x5JUx0YCWaZmH3Q85psI"
NECESSIDADE, DOR = "OJQEsl5dV37pfVY2sIaB", "qmIKSSDVYNLl5E8vnr3f"

MAPA_PRAZO = {
    "pra ontem": "Pra ontem",
    "posso esperar e ver oque acontece": "Sem prazo",
    "posso esperar e ver o que acontece": "Sem prazo",
    "meu negócio não tem urgência de ter mais clientes": "Sem prazo",
}
MAPA_INVESTE = {
    "não invisto nada ainda": "Nunca",
    "até r$ 1.000": "Sim", "até 1k": "Sim", "abaixo de 5k": "Sim", "1k a 5k": "Sim",
    "5k a 10k": "Sim", "acima de 10k": "Sim",
}
NECESSIDADES = {
    "já faço anúncios e quero melhorar meus resultados",
    "quero aprender a gerar meus próprios leads para o whatsapp",
    "quero contratar alguém para gerar meus leads (agência).",
    "falta de novos clientes", "vivemos por indicação", "gerar leads qualificados",
}
LIXO_DOR = {"necessidade (anúncio)"}


def txt(v) -> str:
    return str(v or "").strip()


def plano(c) -> dict:
    """Pura: {campo_id: valor} a escrever neste contato."""
    out = {}
    if not txt(valor(c, PRAZO)):
        p = MAPA_PRAZO.get(txt(valor(c, URGENCIA)).lower())
        if p:
            out[PRAZO] = p
    if not txt(valor(c, INVESTE)):
        i = MAPA_INVESTE.get(txt(valor(c, INVEST)).lower())
        if i:
            out[INVESTE] = i
    dor = txt(valor(c, DOR))
    if not dor or dor.lower() in LIXO_DOR:
        n = txt(valor(c, NECESSIDADE))
        if n.lower() in NECESSIDADES:
            out[DOR] = n
    return out


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    nomes = {PRAZO: "Prazo", INVESTE: "Investe em anúncios", DOR: "Dor principal"}
    cont = Counter()
    for c in contatos():
        p = plano(c)
        if not p:
            continue
        for k, v in p.items():
            cont["%s=%s" % (nomes[k], v[:30])] += 1
        print("  %-28s %s" % ((c.get("firstNameLowerCase") or "sem nome")[:28],
                              ", ".join("%s: %s" % (nomes[k], v[:40]) for k, v in p.items())))
        if aplicar:
            pedir("PUT", "/contacts/%s" % c["id"],
                  {"customFields": [{"id": k, "value": v} for k, v in p.items()]})
    print("qualificação do anúncio%s: %s" % ("" if aplicar else " (DRY)", dict(cont) or "nada a preencher"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
