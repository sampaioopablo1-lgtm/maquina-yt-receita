"""Aplica correções pontuais em workflows PUBLICADOS a partir de uma lista (JSON).

Cada correção: {"wf": "<nome exato>", "no": "<id8 ou id>", "op": ..., ...}
  op "set"      -> {"campo": "body" | "html" | "title" | "notification.body" | ..., "valor": "..."}
                   (caminho com ponto dentro de attributes; cria se não existir)
  op "trocar"   -> {"de": "...", "para": "..."}   troca texto dentro dos attributes do nó
  op "nome"     -> {"valor": "novo nome do nó"}
  op "remover"  -> tira um nó LINEAR (next string ou nenhum) religando pai e filho
Por workflow: backup em workflows-json/_antes-auditoria/, conferência de
ponteiros (next/parentKey/goto sem órfão), PUT, releitura e export.

Uso: python corrigir.py correcoes.json [--aplicar]
"""
import copy, io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g
from patch_funil_reuniao import put

AQUI = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(AQUI, "..", "workflows-json")
BACKUP = os.path.join(DUMPS, "_antes-auditoria")
WF = []   # ids de todos os workflows (preenchido em main)


def acha(tpl, no):
    m = [t for t in tpl if t["id"] == no or t["id"].startswith(no)]
    if len(m) != 1:
        raise SystemExit("nó %s: %d correspondências" % (no, len(m)))
    return m[0]


def aplica(tpl, c):
    t = acha(tpl, c["no"])
    a = t.setdefault("attributes", {})
    op = c["op"]
    if op == "set":
        alvo, partes = a, c["campo"].split(".")
        for p in partes[:-1]:
            alvo = alvo.setdefault(p, {})
        antes = alvo.get(partes[-1])
        alvo[partes[-1]] = c["valor"]
        return "set %s: %r -> %r" % (c["campo"], str(antes)[:60], str(c["valor"])[:60])
    if op == "trocar":
        s = json.dumps(a, ensure_ascii=False)
        de, para = json.dumps(c["de"], ensure_ascii=False)[1:-1], json.dumps(c["para"], ensure_ascii=False)[1:-1]
        n = s.count(de)
        if not n:
            raise SystemExit("nó %s: texto %r não encontrado" % (c["no"], c["de"][:50]))
        t["attributes"] = json.loads(s.replace(de, para))
        return "trocar x%d: %r -> %r" % (n, c["de"][:50], c["para"][:50])
    if op == "apontar":
        alvo = acha(tpl, c["alvo"])["id"]
        antes = a.get("targetNodeId"); a["targetNodeId"] = alvo
        return "apontar: %s -> %s" % (str(antes)[:8], alvo[:8])
    if op == "nome":
        antes = t.get("name"); t["name"] = c["valor"]
        return "nome: %r -> %r" % (antes, c["valor"])
    if op == "remover":
        nx = t.get("next")
        if isinstance(nx, list):
            raise SystemExit("nó %s tem ramos — não removo" % c["no"])
        pai = next((x for x in tpl if x["id"] == t.get("parentKey")), None)
        filho = next((x for x in tpl if x["id"] == nx), None) if nx else None
        if pai is not None:
            if isinstance(pai.get("next"), list):
                raise SystemExit("pai de %s é ramificação — não removo" % c["no"])
            if nx: pai["next"] = nx
            else: pai.pop("next", None)
        if filho is not None:
            filho["parentKey"] = t.get("parentKey")
            if "parent" in filho: filho["parent"] = t.get("parent", t.get("parentKey"))
        tpl.remove(t)
        return "removido %s «%s»" % (t["id"][:8], t.get("name"))
    if op in ("tirar_cond", "add_cond"):
        conds = a["branches"][0]["segments"][0]["conditions"]
        if op == "tirar_cond":
            antes = len(conds)
            conds[:] = [x for x in conds if x.get("conditionValue") not in c["valores"]]
            return "tirar_cond: %d -> %d condições" % (antes, len(conds))
        modelo = next(x for x in conds if x.get("conditionSubType") == c["sub"])
        for v in c["valores"]:
            n = copy.deepcopy(modelo)
            n["conditionOperator"] = c.get("operador", modelo["conditionOperator"])
            n["conditionValue"] = v
            n["__conditionId"] = g.uid()
            conds.append(n)
        return "add_cond: +%d (%s %s)" % (len(c["valores"]), c["sub"], c.get("operador"))
    if op == "inserir":
        nx = t.get("next")
        if isinstance(nx, list):
            raise SystemExit("nó %s tem ramos — insira depois de outro" % c["no"])
        if c["tipo"] == "sms":
            novo = {"id": g.uid(), "name": c.get("nome", "WhatsApp"), "type": "sms",
                    "attributes": {"type": "sms", "body": c["texto"], "attachments": []}}
        elif c["tipo"] == "nota":
            novo = g.note_step(c.get("nome", "Nota"), "<p>%s</p>" % c["texto"])
        elif c["tipo"] in ("+tag", "-tag"):
            novo = g.tag_step(c["tags"], remove=c["tipo"] == "-tag")
        elif c["tipo"] == "oportunidade":
            novo = g.opp_step(c.get("status", "open"), g.STAGES[c["etapa"]], c.get("nome", "Criar/Atualizar Oportunidade"))
        elif c["tipo"] == "clonar":
            m = acha(tpl, c["modelo"])
            s = json.dumps({k: v for k, v in m.items() if k not in ("next", "parent", "parentKey", "order", "stats")},
                           ensure_ascii=False)
            for de, para in c.get("trocas", []):
                s = s.replace(de, para)
            novo = json.loads(s); novo["id"] = g.uid()
        elif c["tipo"] == "goto":
            novo = g.goto_step(acha(tpl, c["alvo"])["id"])
        elif c["tipo"] == "tirar_de":
            novo = {"id": g.uid(), "name": c.get("nome", "Remove from Workflow"), "type": "remove_from_workflow",
                    "attributes": {"type": "remove_from_workflow", "workflow_id": [
                        next(i for i in WF if i.startswith(w[1:])) if w.startswith("@") else w for w in c["workflows"]]}}
        else:
            raise SystemExit("tipo desconhecido " + c["tipo"])
        novo["parentKey"] = t["id"]
        if "parent" in t or True:
            novo["parent"] = t["id"]
        novo["order"] = (t.get("order") or 0) + 1
        if nx:
            novo["next"] = nx
            filho = next(x for x in tpl if x["id"] == nx)
            filho["parentKey"] = novo["id"]
            if "parent" in filho: filho["parent"] = novo["id"]
        t["next"] = novo["id"]
        tpl.insert(tpl.index(t) + 1, novo)
        return "inserido %s depois de %s" % (c["tipo"], t["id"][:8])
    if op == "guardar":
        # insere ANTES do nó c["no"] uma cópia do if_else c["doador"] (com Branch/None).
        # SIM -> segue para o nó; NÃO -> c["nao"] ("fim" ou id de um nó para goto).
        import re, uuid as _u
        UU = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
        doa = acha(tpl, c["doador"])
        ramos = [x for x in tpl if x.get("parentKey") == doa["id"]]
        grupo = [doa] + ramos
        gids = {x["id"] for x in grupo}
        bruto = json.dumps([{k: v for k, v in x.items() if k != "next"} | ({"next": x["next"]} if x is doa else {}) for x in grupo], ensure_ascii=False)
        fora = json.dumps([x for x in tpl if x["id"] not in gids], ensure_ascii=False)
        mapa = {u: str(_u.uuid4()) for u in set(UU.findall(bruto)) if u in gids or u not in fora}
        for v0, v1 in mapa.items():
            bruto = bruto.replace(v0, v1)
        nif, r1, r2 = json.loads(bruto)
        sim, nao = (r1, r2) if not (r1.get("attributes") or {}).get("else") else (r2, r1)
        pai = next(x for x in tpl if x["id"] == t.get("parentKey"))
        if isinstance(pai.get("next"), list):
            raise SystemExit("pai de %s é ramificação — guarde depois do Branch/None" % c["no"])
        nif["name"] = c.get("nome", doa.get("name"))
        nif["parentKey"] = nif["parent"] = pai["id"]
        pai["next"] = nif["id"]
        if c.get("inverter"):
            # SIM -> goto c["sim_vai"]; NÃO -> segue para o nó
            gt = g.goto_step(acha(tpl, c["sim_vai"])["id"])
            gt["parentKey"] = gt["parent"] = sim["id"]; sim["next"] = gt["id"]; gt["order"] = 1
            nao["next"] = t["id"]; t["parentKey"] = nao["id"]
            if "parent" in t: t["parent"] = nao["id"]
            i = tpl.index(t); tpl[i:i] = [nif, sim, gt, nao]
            return "guardar(invertido): «%s» antes de %s (SIM -> %s)" % (nif["name"], t["id"][:8], c["sim_vai"])
        sim["next"] = t["id"]
        t["parentKey"] = sim["id"]
        if "parent" in t: t["parent"] = sim["id"]
        if c.get("nao", "fim") == "fim":
            nao.pop("next", None)
            novos = [nif, sim, nao]
        else:
            gt = g.goto_step(acha(tpl, c["nao"])["id"])
            gt["parentKey"] = gt["parent"] = nao["id"]; nao["next"] = gt["id"]; gt["order"] = 1
            novos = [nif, sim, nao, gt]
        i = tpl.index(t)
        tpl[i:i] = novos
        return "guardar: «%s» antes de %s (NÃO -> %s)" % (nif["name"], t["id"][:8], c.get("nao", "fim"))
    raise SystemExit("op desconhecida " + op)


def confere(tpl):
    ids = {t["id"] for t in tpl}
    err = []
    for t in tpl:
        if t.get("parentKey") and t["parentKey"] not in ids:
            err.append("parentKey órfão em %s" % t["id"][:8])
        nx = t.get("next")
        for n in (nx if isinstance(nx, list) else [nx] if nx else []):
            if n not in ids:
                err.append("next órfão em %s" % t["id"][:8])
        if t["type"] == "goto" and (t.get("attributes") or {}).get("targetNodeId") not in ids:
            err.append("goto órfão em %s" % t["id"][:8])
    return err


def main():
    lista = json.load(open(sys.argv[1], encoding="utf-8"))
    aplicar = "--aplicar" in sys.argv
    c = g.client()
    ids = {w["name"]: w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    WF.extend(ids.values())
    por_wf = {}
    for x in lista:
        por_wf.setdefault(x["wf"], []).append(x)
    ok_geral = True
    for nome, corr in por_wf.items():
        cur = c.request("GET", "/workflow/" + g.LOC + "/" + ids[nome])
        tpl = copy.deepcopy(cur["workflowData"]["templates"])
        print("== %s (%d nós, %s)" % (nome, len(tpl), cur.get("status")))
        for x in corr:
            if x["op"] == "config":
                antes = cur.get(x["chave"]); cur[x["chave"]] = x["valor"]
                print("   config %s: %r -> %r" % (x["chave"], antes, x["valor"]))
                continue
            print("   " + aplica(tpl, x))
        err = confere(tpl)
        if err:
            print("   CONFERÊNCIA FALHOU:", err); ok_geral = False; continue
        if not aplicar:
            continue
        os.makedirs(BACKUP, exist_ok=True)
        g.export(c, ids[nome], os.path.join(BACKUP, nome + ".json"))
        r = put(c, cur, tpl)
        if r is None or (isinstance(r, dict) and r.get("_error")):
            print("   PUT RECUSADO:", r); ok_geral = False; continue
        v = c.request("GET", "/workflow/" + g.LOC + "/" + ids[nome])
        print("   gravado: %s, %d nós" % (v.get("status"), len(v["workflowData"]["templates"])))
        g.export(c, ids[nome], os.path.join(DUMPS, nome + ".json"))
    if not aplicar:
        print("\n(nada gravado — rode com --aplicar)")
    return 0 if ok_geral else 1


if __name__ == "__main__":
    sys.exit(main())
