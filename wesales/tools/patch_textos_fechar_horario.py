#!/usr/bin/env python3
"""A8 — textos do `Fechar Horário` relidos com olhos de lead (23/09/2026).

1. MFH2 dizia "Tenho horarios amanha de manha e a tarde". A janela do
   workflow e seg-sex: enviada na sexta, oferece sabado.
2. MFH1/MFH2 abriam com `{{contact.first_name}},`. A Porta de Entrada grava o
   nome do WhatsApp como vier (medido: `156766977421470`, `o`, `sem` nos
   contatos da casa). Mensagem automatica abre sem nome.

So troca `body` de dois nos `sms` — zero no novo, zero religacao.

Uso:  python patch_textos_fechar_horario.py [--aplicar]
"""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_funil_reuniao import put, g

ALVO = "Fechar Horário"
AQUI = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(AQUI, "..", "workflows-json")
BACKUP = os.path.join(DUMPS, "_antes-textos-fechar-horario")
TEXTOS = {
    "WhatsApp · MFH1-v1": "Oi! Foi bom falar com você. Pra gente seguir, qual o melhor "
                          "dia e horário para a nossa reunião de diagnóstico (30 minutos)? "
                          "Pode me responder por aqui mesmo.",
    "WhatsApp · MFH2-v1": "Oi! Passando pra fechar a nossa reunião de diagnóstico. Tenho "
                          "horários nos próximos dias, de manhã e à tarde — qual fica "
                          "melhor pra você?",
}


def main():
    aplicar = "--aplicar" in sys.argv
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    cur = c.request("GET", "/workflow/" + g.LOC + "/" + ids[ALVO])
    tpl = copy.deepcopy((cur.get("workflowData") or {}).get("templates") or [])
    trocas = 0
    for t in tpl:
        novo = TEXTOS.get(t.get("name"))
        if t.get("type") != "sms" or not novo:
            continue
        a = t.setdefault("attributes", {})
        print("%s\n   antes:  %s\n   depois: %s" % (t["name"], a.get("body"), novo))
        if a.get("body") != novo:
            a["body"] = novo
            trocas += 1
    if trocas != len(TEXTOS):
        print("esperava %d trocas, achei %d" % (len(TEXTOS), trocas))
    if not aplicar or not trocas:
        print("\n(nada foi gravado)")
        return 0
    os.makedirs(BACKUP, exist_ok=True)
    g.export(c, ids[ALVO], os.path.join(BACKUP, ALVO + ".json"))
    r = put(c, cur, tpl)
    if r is None or r.get("_error"):
        print("PUT RECUSADO:", r)
        return 1
    v = c.request("GET", "/workflow/" + g.LOC + "/" + ids[ALVO])
    vt = (v.get("workflowData") or {}).get("templates") or []
    ok = sum(1 for t in vt if t.get("name") in TEXTOS and TEXTOS[t["name"]] == (t.get("attributes") or {}).get("body"))
    print("gravado: status=%s nos=%d textos novos ao vivo=%d" % (v.get("status"), len(vt), ok))
    g.export(c, ids[ALVO], os.path.join(DUMPS, ALVO + ".json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
