#!/usr/bin/env python3
"""WhatsApp tentado hoje (28/09, item 2 do PENDENTES-CRM.md): quando a SDR marca Canal da
tentativa = WhatsApp, o lead ganha `wa-feito-hoje` por 12 h. O atuador não o põe de volta em
`fila-wa` (visão "Ligar pelo WhatsApp" em Conversas) enquanto a tag existir: 1 ligação de
WhatsApp por lead por dia."""
import sys
from criar_workflows_27 import Cadeia
from criar_capi import criar_varios
from criar_trava_canal import espera_horas
import ghl_interno as g

NOME = "WhatsApp tentado hoje"
CANAL = "AsZMGmsKVu1xEp36hyLb"


def montar():
    c = Cadeia()
    t = c.add(None, "add_contact_tag", "WhatsApp tentado hoje", {"tags": ["wa-feito-hoje"]})
    r = c.add(t, "remove_contact_tag", "Sai da visão", {"tags": ["fila-wa"]})
    w = c.add(r, "wait", "Wait 12 Hours", espera_horas(12))
    c.add(w, "remove_contact_tag", "Fim do dia", {"tags": ["wa-feito-hoje"]})
    gat = {"type": "contact_changed", "name": "Canal da tentativa = WhatsApp", "conditions": [
        {"operator": "==", "field": "contact." + CANAL, "value": "WhatsApp", "title": "Canal da tentativa",
         "type": "select", "id": CANAL}]}
    return c.nos, [gat]


if __name__ == "__main__":
    nos, gats = montar()
    seco = "--seco" in sys.argv
    criar_varios(NOME, nos, gats, seco)
    if not seco:
        w = g.por_nome(NOME); cur = g.ler(w["id"]); cur["window"] = None; cur["allowMultiple"] = True
        g.put(cur, cur["workflowData"]["templates"]); d = g.ler(w["id"])
        print("final:", w["id"], d["status"], "v%s" % d["version"], d.get("window"), [(t["name"], t.get("active")) for t in g.gatilhos(w["id"])])
