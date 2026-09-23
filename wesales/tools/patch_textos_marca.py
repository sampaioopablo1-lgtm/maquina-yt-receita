"""Tira {{user.first_name}} e {{location.name}} das mensagens automaticas.
Medido 23/09/2026 com o numero do dono: user.first_name saiu VAZIO e
location.name saiu "Pablo Santos's Account" (nome interno da conta). Troca pelo
nome da marca, fixo. So muda o texto dos nos `sms` (mesmos ids).
Uso: python patch_textos_marca.py [--aplicar]"""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_funil_reuniao import put, g
MARCA = "O Próximo Cliente"
TROCAS = [("aqui é o {{user.first_name}} da {{location.name}}", "aqui é da " + MARCA),
          ("{{location.name}}", MARCA), (" o {{user.first_name}}", ""), ("{{user.first_name}}", MARCA)]


def limpa(txt):
    for a, b in TROCAS:
        txt = txt.replace(a, b)
    return txt


aplicar = "--aplicar" in sys.argv
c = g.client()
for w in c.request("GET", "/workflow/" + g.LOC):
    if w.get("status") != "published":
        continue
    cur = c.request("GET", "/workflow/" + g.LOC + "/" + w["id"])
    tpl = copy.deepcopy(cur["workflowData"]["templates"])
    mud = []
    for t in tpl:
        if t.get("type") == "sms":
            b = t["attributes"].get("body") or ""
            nb = limpa(b)
            if nb != b:
                t["attributes"]["body"] = nb
                mud.append("%s: %s…" % (t.get("name"), nb[:70]))
    if not mud:
        continue
    print("== %s: %d mensagem(ns)" % (w["name"], len(mud)))
    for m in mud:
        print("   " + m)
    if aplicar:
        put(c, cur, tpl)
        v = c.request("GET", "/workflow/" + g.LOC + "/" + w["id"])
        resto = sum(1 for t in v["workflowData"]["templates"] if t.get("type") == "sms"
                    and ("{{user." in t["attributes"]["body"] or "{{location." in t["attributes"]["body"]))
        print("   conferido: status=%s restantes=%d ids iguais=%s" % (v.get("status"), resto,
              [x["id"] for x in v["workflowData"]["templates"]] == [x["id"] for x in tpl]))
