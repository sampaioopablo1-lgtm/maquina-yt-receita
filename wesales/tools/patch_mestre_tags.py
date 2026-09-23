"""A8 (auditoria_tags, pergunta 1): quem sai do funil de prospeccao pelo Mestre
de saida v2 (etapa alem de CONECTAR, perdido ou nutricao) levava embora as tags
de fila, mas nao as que DISPARAM cadencia. Como `remove_from_workflow` pula os
Remove Tag finais de Fechar Horario / 12x30 parte 2, `fechar-horario`,
`cadencia-12x30-p2`, `cad-outbound` e `toque` ficavam no contato - e numa
volta futura, pôr de novo uma tag que ja existe NAO dispara o gatilho.
Aqui so a lista de tags do Remove Tag cresce; nada mais muda. `cad-inbound`
fica (marca de origem; ninguem a re-aplica). NAO se acrescenta remocao de
cadencia: o fim da 12x30 poe a oportunidade em nutricao e seria cortado.
Uso: python patch_mestre_tags.py [--aplicar]"""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_funil_reuniao import put, g

NOVAS = ["cad-outbound", "cadencia-12x30-p2", "fechar-horario", "toque",
         "proposta-pendente", "negociacao-estagnada"]   # alerta vale so na etapa em que nasceu
c = g.client()
wf = [w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
      if w.get("name") == "Mestre de saída v2" and w.get("status") == "published"][0]
cur = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
T = copy.deepcopy(cur["workflowData"]["templates"])
rt = [t for t in T if t["type"] == "remove_contact_tag"]
assert len(rt) == 1, "esperava 1 Remove Tag"
antes = list(rt[0]["attributes"]["tags"])
rt[0]["attributes"]["tags"] = antes + [t for t in NOVAS if t not in antes]
print("antes:", antes)
print("depois:", rt[0]["attributes"]["tags"])
if "--aplicar" in sys.argv and rt[0]["attributes"]["tags"] != antes:
    g.export(c, wf, os.path.join("..", "workflows-json", "_antes-patch-mestre", "Mestre de saída v2.json"))
    put(c, cur, T)
    v = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
    print("conferido: status=%s tags=%s gatilhos=%s" % (
        v.get("status"),
        [t["attributes"]["tags"] for t in v["workflowData"]["templates"] if t["type"] == "remove_contact_tag"],
        [t.get("active") for t in c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + wf)
         if not t.get("deleted")]))
    g.export(c, wf, os.path.join("..", "workflows-json", "Mestre de saída v2.json"))
