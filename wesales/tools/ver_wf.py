"""Imprime os nós de um workflow publicado (ordem, tipo, nome, texto curto).
Uso: python ver_wf.py "Nome do workflow" """
import io, os, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g
c = g.client()
ws = [w for w in c.request("GET", "/workflow/" + g.LOC) if w.get("name") == sys.argv[1]]
for w in ws:
    f = c.request("GET", "/workflow/" + g.LOC + "/" + w["id"]) or {}
    tpl = (f.get("workflowData") or {}).get("templates") or []
    print("%s %s status=%s janela=%s nós=%d" % (w["id"], w["name"], f.get("status"), f.get("window"), len(tpl)))
    for t in (f.get("triggers") or []):
        print("  GATILHO", t.get("type"), json.dumps(t.get("conditions"), ensure_ascii=False)[:300])
    for t in tpl:
        a = t.get("attributes") or {}
        txt = a.get("body") or a.get("title") or a.get("message") or ""
        extra = ""
        if t["type"] == "if_else":
            extra = json.dumps([[ (x.get("field") or x.get("subType"), x.get("operator"), x.get("value")) for x in (s.get("conditions") or [])] for s in (a.get("branches") or a.get("segments") or [])], ensure_ascii=False)[:250]
        print("  %-4s %-22s %-40s p=%s %s %s" % (t.get("order"), t["type"], (t.get("name") or "")[:40], (t.get("parent") or "")[:6], str(txt)[:90].replace("\n"," "), extra))
