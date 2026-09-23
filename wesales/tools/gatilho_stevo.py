"""E10: resposta pela Stevo (WhatsApp nao oficial) nao disparava nada.

`Interceptação de Sinal — Resposta v2` e `Opt-out por Palavra-chave` tem
gatilho `customer_reply` com `message.type == 19` (WhatsApp oficial). A Stevo
entra no GHL pelo canal de SMS personalizado e chega como tipo 20 (lido numa
conversa real da Stevo, `messageTypes: [20]`; Instagram = 18). Resultado: um
lead respondendo pela Stevo nao gerava "ligar agora", e um "pare" nao virava DND.

Correcao: acrescenta a cada um um SEGUNDO gatilho identico, com tipo 20,
apontando para o mesmo primeiro no. O gatilho do tipo 19 fica (vale se um dia
houver WhatsApp oficial). Nao mexe em no nenhum.

Uso: python gatilho_stevo.py            -> so mostra
     python gatilho_stevo.py --aplicar  -> cria e confere
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

ALVOS = ["Interceptação de Sinal — Resposta v2", "Opt-out por Palavra-chave"]
STEVO = 20
LIXO = ("id", "date_added", "date_updated", "company_id", "company_age",
        "deleted", "_id", "__v")


def main():
    aplicar = "--aplicar" in sys.argv
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    for nome in ALVOS:
        wf = ids[nome]
        trs = [t for t in c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + wf)
               if not t.get("deleted")]
        tipos = [next((x.get("value") for x in t.get("conditions") or []
                       if x.get("field") == "message.type"), None) for t in trs]
        print("== %s: %d gatilho(s), canais %s, alvo %s"
              % (nome, len(trs), tipos, [t.get("targetActionId") for t in trs]))
        if STEVO in tipos:
            print("   ja tem o canal 20 - nada a fazer")
            continue
        base = next(t for t, v in zip(trs, tipos) if v == 19)
        novo = {k: v for k, v in base.items() if k not in LIXO}
        novo["conditions"] = [dict(x, value=STEVO) if x.get("field") == "message.type" else x
                              for x in base.get("conditions") or []]
        novo["name"] = (base.get("name") or "Customer Replied") + " — Stevo"
        novo["workflowId"] = wf
        print("   novo gatilho:", json.dumps(novo["conditions"], ensure_ascii=False)[:300])
        if not aplicar:
            continue
        tr = c.request("POST", "/workflow/" + g.LOC + "/trigger", novo)
        if not tr or tr.get("_error") or not tr.get("id"):
            print("   FALHOU ao criar:", str(tr)[:200])
            continue
        c.request("PUT", "/workflow/" + g.LOC + "/trigger/" + tr["id"],
                  dict(novo, targetActionId=base.get("targetActionId"),
                       advanceCanvasMeta=base.get("advanceCanvasMeta")
                       or {"position": {"x": 400, "y": -73}}))
        depois = [t for t in c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + wf)
                  if not t.get("deleted")]
        print("   conferido:", [(t.get("name"), t.get("active"),
                                 [x.get("value") for x in t.get("conditions") or []
                                  if x.get("field") == "message.type"],
                                 t.get("targetActionId") == base.get("targetActionId"))
                                for t in depois])


if __name__ == "__main__":
    main()
