#!/usr/bin/env python3
"""9c, metade do `Pós-ligação v2`: grava `Canal que conectou` no ramo `Atendeu`.

Complemento do `patch_canal_conectou.py`, que ficou esperando o
`patch_remove_atendeu.py` (G-18) ir ao ar primeiro — foi em 23/09/2026.

O ramo SABE o canal: depois de `Resultado da tentativa = Atendeu` ele testa a
tag `fila-wa` (presente = a ligacao foi pelo WhatsApp). Cada caminho `Atendeu`
ja tem um `update_contact_field` (grava `uJnePU1Tl1Zr1fTxYKIz`); o campo entra
no array dele — zero no novo, zero religacao.

| no update | caminho                          | grava              |
|-----------|----------------------------------|--------------------|
| feb677cf  | copia 2, telefone (CAMINHO REAL) | `Ligação normal`   |
| d23291df  | copia 2, WhatsApp                | `Ligação WhatsApp` |
| 62a57a2a  | copia 1, WhatsApp                | `Ligação WhatsApp` |

A copia 1 / telefone (`a39fe8fc`) e codigo morto (G-18) e nao tem update.

Uso:  python patch_canal_posligacao.py            # plano, sem gravar
      python patch_canal_posligacao.py --aplicar   # grava, com backup
"""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch_canal_conectou as pc                 # campo(), CAMPO, DUMPS
from patch_funil_reuniao import put, g

ALVO = "Pós-ligação v2"
PONTOS = {"feb677cf": "Ligação normal",
          "d23291df": "Ligação WhatsApp",
          "62a57a2a": "Ligação WhatsApp"}
BACKUP = os.path.join(pc.DUMPS, "_antes-canal-posligacao")


def aplica(tpl0):
    tpl = copy.deepcopy(tpl0)
    log, feitos = [], 0
    for pref, valor in PONTOS.items():
        no = next((t for t in tpl if t["id"].startswith(pref)), None)
        if not no or no.get("type") != "update_contact_field":
            log.append("%s: nao achei o update_contact_field — PULADO" % pref)
            continue
        campos = no.setdefault("attributes", {}).setdefault("fields", [])
        if any(f.get("field") == pc.CAMPO for f in campos):
            log.append("%s: ja grava — nada a fazer" % pref)
            continue
        campos.append(pc.campo(valor))
        feitos += 1
        log.append("%s: + `Canal que conectou` = %r (%d campos)" % (pref, valor, len(campos)))
    return tpl, log, feitos


def main():
    aplicar = "--aplicar" in sys.argv
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    cur = c.request("GET", "/workflow/" + g.LOC + "/" + ids[ALVO])
    tpl = (cur.get("workflowData") or {}).get("templates") or []
    print("%s: %d nos [%s]" % (ALVO, len(tpl), cur.get("status")))
    novo, log, feitos = aplica(tpl)
    for l in log:
        print("   " + l)
    if len(novo) != len(tpl):
        print("numero de nos mudou — nao aplico")
        return 1
    if not aplicar or not feitos:
        print("\n(nada foi gravado)")
        return 0
    os.makedirs(BACKUP, exist_ok=True)
    g.export(c, ids[ALVO], os.path.join(BACKUP, ALVO + ".json"))
    r = put(c, cur, novo)
    if r is None or r.get("_error"):
        print("PUT RECUSADO:", r)
        return 1
    v = c.request("GET", "/workflow/" + g.LOC + "/" + ids[ALVO])
    vt = (v.get("workflowData") or {}).get("templates") or []
    n = sum(1 for t in vt if t.get("type") == "update_contact_field"
            for f in ((t.get("attributes") or {}).get("fields") or [])
            if f.get("field") == pc.CAMPO)
    print("gravado: status=%s nos=%d campo ao vivo=%dx" % (v.get("status"), len(vt), n))
    g.export(c, ids[ALVO], os.path.join(pc.DUMPS, ALVO + ".json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
