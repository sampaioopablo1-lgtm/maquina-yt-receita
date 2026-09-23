"""A3: na Recuperacao de No-show, a mensagem NS-1 sai sozinha pela Stevo (no
`sms`) no inicio do ramo de recuperacao (1o no-show), antes da tarefa NS1 do SDR.
Sem link: quem responde cai na conversa e dispara o sinal para o SDR (mesmo
padrao das MFH do Fechar Horario). O texto da tarefa NS1 passa a avisar que a
mensagem ja saiu, para o SDR nao mandar de novo.
Uso: python patch_noshow_ns1.py [--aplicar]   (TESTE: --wf <id> aplica numa copia)"""
import copy, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_funil_reuniao import put, g

NS1 = ("Oi {{contact.first_name}}, vi que não conseguimos nos falar no horário combinado "
       "— imagino que bateu algum imprevisto! Sem problema nenhum: me responde por aqui "
       "com o melhor dia e horário que eu remarco a nossa reunião de diagnóstico pra você.")
AVISO = " A mensagem NS-1 (remarcar) já saiu sozinha pelo WhatsApp — não mande de novo; ligue."
aplicar = "--aplicar" in sys.argv
c = g.client()
if "--wf" in sys.argv:
    wf = sys.argv[sys.argv.index("--wf") + 1]
else:
    wf = [w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
          if w.get("name") == "Recuperação de No-show" and w.get("status") == "published"][0]
cur = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
T = copy.deepcopy(cur["workflowData"]["templates"])
by = {t["id"]: t for t in T}
if any(t["type"] == "sms" for t in T):
    sys.exit("ja tem mensagem - nada a fazer")
# ramo de recuperacao = o que contem a tarefa "Tentativa 1 de 3"
t1 = next(t for t in T if t["type"] == "task-notification"
          and "Tentativa 1 de 3" in (t["attributes"].get("body") or ""))
ramo = by[t1["parent"]]
filhos = sorted([t for t in T if t.get("parent") == ramo["id"]], key=lambda t: t["order"])
primeiro = filhos[0]
assert ramo.get("next") == primeiro["id"], "estrutura inesperada"
msg = {"id": g.uid(), "name": "WhatsApp · NS-1 (remarcar)", "type": "sms",
       "parent": ramo["id"], "parentKey": ramo["id"], "next": primeiro["id"], "order": 0, "cat": "",
       "attributes": {"type": "sms", "body": NS1, "attachments": []},
       "advanceCanvasMeta": primeiro.get("advanceCanvasMeta")}
for f in filhos:
    f["order"] += 1
ramo["next"] = msg["id"]
primeiro["parentKey"] = msg["id"]
T.insert(T.index(primeiro), msg)
b = t1["attributes"]["body"]
if "NS-1" not in b:
    t1["attributes"]["body"] = b.replace("</p>", AVISO + "</p>", 1) if "</p>" in b else b + AVISO
print("ramo %s -> msg %s -> %s (%s) | nós %d" % (ramo["id"][:8], msg["id"][:8], primeiro["id"][:8],
                                                 primeiro["type"], len(T)))
print("tarefa NS1:", t1["attributes"]["body"][:300])
if aplicar:
    g.export(c, wf, os.path.join("..", "workflows-json", "_antes-patch-ns1", cur["name"] + ".json"))
    put(c, cur, T)
    v = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
    vt = v["workflowData"]["templates"]
    print("conferido: status=%s nós=%d sms=%d gatilhos=%s" % (
        v.get("status"), len(vt), sum(x["type"] == "sms" for x in vt),
        [t.get("active") for t in c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + wf)
         if not t.get("deleted")]))
    g.export(c, wf, os.path.join("..", "workflows-json", cur["name"] + ".json"))
