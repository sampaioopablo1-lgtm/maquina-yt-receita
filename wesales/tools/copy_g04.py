#!/usr/bin/env python3
"""Grava no CRM a copy do `COPY-WHATSAPP.md` e o G-04 (opcao B), pela API interna.

Dono, 27/09: "tudo liberado, grave as informacoes no CRM".

POR QUE PELA ACTION
-------------------
A API publica do GHL so LE workflow. A interna escreve, com bearer de sessao
logada, e o conteiner nao alcanca `backend.leadconnectorhq.com`. O runner alcanca:
`renovar_bearer.js` troca o segredo `GHL_STORAGE_STATE` por um bearer e este
script usa `ghl_interno.put`, que preserva `status` e recusa os PUBLICADOS.

MODOS
-----
    --sondar    le tudo e imprime o que cada no-alvo tem hoje. Escreve nada.
    --aplicar   (vem depois da sonda, quando a forma dos nos estiver lida)

O repositorio e PUBLICO, e log de Action tambem: aqui so sai texto de mensagem e
estrutura de no — nunca token, nunca dado de contato.
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_interno as gi  # noqa: E402

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".local", "dumps")

# prefixo do id do no (8 hex, como o COPY-WHATSAPP.md cita) -> trecho do nome do workflow
ALVOS_COPY = {
    # Cadencia Inbound
    "bb08de48": "Inbound", "1ef37d68": "Inbound",
    # Cadencia 12x30 e parte 2
    "32443ee5": "12x30", "afa33deb": "12x30",
    "aee02070": "12x30", "2d46801f": "12x30", "1c210e54": "12x30",
    # Fechar Horario
    "50840639": "Fechar", "f3b453e0": "Fechar",
    # Nutricao
    "37a0e14d": "Nutri", "ce3c0f0c": "Nutri", "8c27d01c": "Nutri",
    "6d666618": "Nutri", "1075472b": "Nutri", "1d41123d": "Nutri",
    # No-show, Cancelada, Triagem
    "b14157d9": "No-show", "4f096401": "Cancelada",
    "fd3d4f52": "Triagem", "d92c81e4": "Triagem", "7553bed1": "Triagem",
    # Lembretes da Reuniao v3
    "b01ea94e": "Lembretes", "82a997ab": "Lembretes",
    "795abe36": "Lembretes", "8df54d1d": "Lembretes",
    "1e09f108": "Lembretes", "6137d10b": "Lembretes",
    "c3588d10": "Lembretes", "3cce8505": "Lembretes",
    "ba7131c5": "Lembretes", "4cc095fa": "Lembretes",
    "82e509f2": "Lembretes", "a7c110e8": "Lembretes",
    "266ce968": "Lembretes", "d0bd4bc3": "Lembretes",
    "db1826db": "Lembretes", "16bbd274": "Lembretes",
    "29bf8e07": "Lembretes", "66734cf2": "Lembretes",
    "d6b42f3a": "Lembretes", "2d34bd48": "Lembretes",
    "ab16456c": "Lembretes", "b94fcca3": "Lembretes",
}

G04_WORKFLOW = "Pós-agendamento v2"
G04_PALAVRAS = re.compile(
    r"investimento|investe|prazo|urg|necessidade|dor_principal|budget", re.I)


def todos() -> list:
    return gi.listar()


def curto(obj, n=2500) -> str:
    s = json.dumps(obj, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + " …(+%d)" % (len(s) - n)


def sondar() -> int:
    wfs = todos()
    print("workflows na subconta: %d" % len(wfs))
    os.makedirs(SAIDA, exist_ok=True)
    achados = {}
    lidos = {}
    for w in wfs:
        nome = w.get("name") or ""
        if not (any(t in nome for t in set(ALVOS_COPY.values()))
                or nome == G04_WORKFLOW):
            continue
        cur = gi.ler(w["id"])
        lidos[w["id"]] = cur
        with open(os.path.join(SAIDA, w["id"] + ".json"), "w", encoding="utf-8") as f:
            json.dump(cur, f, ensure_ascii=False, indent=1)
        tpl = (cur.get("workflowData") or {}).get("templates") or []
        print("\n=== %s | %s | v%s | %d nos | %s%s" % (
            nome, cur.get("status"), cur.get("version"), len(tpl), w["id"],
            "  [PUBLICADO-PROIBIDO]" if w["id"] in gi.PUBLICADOS else ""))
        for n in tpl:
            nid = str(n.get("id") or "")
            p = nid[:8]
            if p in ALVOS_COPY and ALVOS_COPY[p] in nome:
                achados.setdefault(p, []).append((nome, nid))
                print("--- no %s type=%s name=%r" % (nid, n.get("type"), n.get("name")))
                print("    attributes: " + curto(n.get("attributes")))
        if nome == G04_WORKFLOW:
            print("\n### G-04: nos com condicao que toca os campos do Meta")
            for n in tpl:
                if n.get("type") not in ("if_else", "condition", "if-else") and \
                        "if" not in str(n.get("type")):
                    continue
                s = json.dumps(n, ensure_ascii=False)
                if G04_PALAVRAS.search(s):
                    print("--- %s type=%s name=%r" % (n.get("id"), n.get("type"), n.get("name")))
                    print("    " + curto(n, 6000))
            tipos = {}
            for n in tpl:
                tipos[n.get("type")] = tipos.get(n.get("type"), 0) + 1
            print("tipos de no: %s" % tipos)

    faltam = [p for p in ALVOS_COPY if p not in achados]
    dup = {p: v for p, v in achados.items() if len(v) > 1}
    print("\nRESUMO: %d de %d nos-alvo achados; faltam %s; duplicados %s"
          % (len(achados), len(ALVOS_COPY), faltam or "-", dup or "-"))
    return 0


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--sondar", action="store_true")
    a = ap.parse_args()
    try:
        if a.sondar:
            return sondar()
    except (gi.SemBearer, gi.RecusadoPelaConta) as e:
        print("PAROU: %s" % e)
        return 2
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
