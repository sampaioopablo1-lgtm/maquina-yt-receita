#!/usr/bin/env python3
"""Pós-ligação v3: o canal da ligação vem do campo `Canal da tentativa`, não da tag `fila-wa`.

`fila-wa` não é aplicada por nenhum workflow (ESTADO §2.2/§10), então todo registro caía
em "telefone". Troca a condição dos 3 portões de canal por `Canal da tentativa ==
WhatsApp` e, no fim de cada ramo, limpa o campo para a próxima ligação — exceto no ramo
"Resultado vazio?", para não apagar o canal que a SDR marcou antes do resultado.
Grava preservando `status`, relê e compara nó a nó.
"""
import copy, json, sys, uuid
import ghl_interno as g
from gravar_portao_wa import grafo_ok

WID = "8b86e5cb-97ae-4c84-ae3a-6fa11f9fe1a4"
CANAL = "AsZMGmsKVu1xEp36hyLb"
PORTOES = ("0e83c66e", "232f5964", "49e68349")
NAO_LIMPAR = ("058d61dc",)   # Branch de "Resultado vazio?"


def main(seco: bool) -> int:
    cur = g.ler(WID)
    t = cur["workflowData"]["templates"]
    if cur["version"] != 6 or cur["status"] != "published":
        raise SystemExit("PAROU: esperava v6 publicado, li v%s %s" % (cur["version"], cur["status"]))
    novo = copy.deepcopy(t)
    base = [n for n in novo if n.get("name") == "Atendeu?"][0]
    modelo = base["attributes"]["branches"][0]["segments"][0]["conditions"][0]
    for p in PORTOES:
        n = [x for x in novo if x["id"].startswith(p)][0]
        cs = n["attributes"]["branches"][0]["segments"][0]["conditions"]
        if len(cs) != 1 or cs[0]["conditionValue"] != ["fila-wa"]:
            raise SystemExit("PAROU: portão %s não é o descrito" % p)
        c = copy.deepcopy(modelo)
        c.update({"conditionSubType": CANAL, "conditionOperator": "==",
                  "conditionValue": "WhatsApp", "__conditionId": str(uuid.uuid4())})
        n["attributes"]["branches"][0]["segments"][0]["conditions"] = [c]
        print("portão", p, n["name"], "-> Canal da tentativa == WhatsApp")
    fins = [x for x in novo if not x.get("next") and x["type"] != "goto"
            and not x["id"].startswith(NAO_LIMPAR)]
    for x in fins:
        c = {"id": str(uuid.uuid4()), "name": "Limpa Canal da tentativa",
             "type": "update_contact_field", "order": int(x.get("order") or 0) + 1,
             "parent": x["id"], "parentKey": x["id"], "cat": "",
             "attributes": {"type": "update_contact_field", "actionType": "update_field_data",
                            "fields": [{"field": CANAL, "value": "", "title": "Canal da tentativa",
                                        "type": "select", "date": ""}]}}
        x["next"] = c["id"]
        novo.append(c)
    print("limpeza no fim de %d ramos; grafo %s; %d -> %d nós"
          % (len(fins), grafo_ok(novo) or "ok", len(t), len(novo)))
    if seco or grafo_ok(novo):
        return 0
    g.put(cur, novo)
    dep = g.ler(WID)
    td = dep["workflowData"]["templates"]
    esp = {n["id"]: n for n in novo}
    dif = [n["id"][:8] for n in td if n != esp.get(n["id"])]
    print("gravado v%s -> v%s %s %d nós difs %s" % (cur["version"], dep["version"], dep["status"],
                                                   len(td), dif or "nenhuma"))
    return 0 if not dif and dep["status"] == "published" else 1


if __name__ == "__main__":
    sys.exit(main("--seco" in sys.argv))
