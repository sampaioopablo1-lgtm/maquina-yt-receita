"""Ajuste cirurgico nas 3 cadencias PUBLICADAS (autorizado pelo dono em
22/09/2026, excecao a regra "nunca edite um publicado").

1. `Entrada em` / `1a tentativa em`: o valor 'sim' vira
   '{{right_now.date}} {{right_now.time}}' (medido em teste_relogio.py:
   `{{right_now}}` sozinho grava '[object Object]').
2. Pre-requisito 6 do W20: no no que abre cada tentativa (o que zera
   `Resultado da tentativa` e grava `Tentativa no`), acrescenta
   `Conexao real` = vazio.

Por que patch e nao v2: `Pos-ligacao v2` e `Pos-agendamento v2` apontam
para o id da `Cadencia 12x30`, e rebuild pelo builder troca os ids dos nos
(contato parado num Wait se perderia). Aqui so muda `value`/`fields`; id do
workflow e ids dos nos ficam iguais.

Uso:
  python patch_relogio_cadencias.py            -> so simula e lista
  python patch_relogio_cadencias.py --aplicar  -> backup + PUT + confere
"""
import copy
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

AQUI = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(AQUI, "campos.json"), encoding="utf-8"))
ENTRADA = C["Entrada em"]["id"]
PRIMEIRA = C["1ª tentativa em"]["id"]
RESULT = C["Resultado da tentativa"]["id"]
TENT = C["Tentativa nº"]["id"]
CONEXAO = C["Conexão real"]["id"]
AGORA = "{{right_now.date}} {{right_now.time}}"

ALVOS = {
    "c64a808b-3040-431e-8015-642a265e1022": "Cadência 12x30",
    "c2375e2f-b4cb-4947-8377-7c1e0529ba82": "Cadência Inbound",
    "37eb32e4-4c21-4c69-bba1-36879ae0886c": "Reengajamento 90 dias",
}
BACKUP = os.path.join(AQUI, "..", "workflows-json", "_antes-patch-relogio")


def corrigir(templates):
    """Devolve (templates novos, lista do que mudou). Nao toca em ids."""
    novos = copy.deepcopy(templates)
    mudou = []
    for t in novos:
        if t.get("type") != "update_contact_field":
            continue
        campos = (t.get("attributes") or {}).get("fields") or []
        ids = {f.get("field") for f in campos}
        for f in campos:
            if f.get("field") in (ENTRADA, PRIMEIRA) and f.get("value") == "sim":
                f["value"] = AGORA
                mudou.append("%s: %s 'sim' -> hora" % (t["id"][:8], f.get("title")))
        if RESULT in ids and TENT in ids and CONEXAO not in ids:
            campos.append({"field": CONEXAO, "value": "", "title": "Conexão real",
                           "type": "select", "date": ""})
            tent = [f.get("value") for f in campos if f.get("field") == TENT][0]
            mudou.append("%s: tentativa %s + zera Conexão real" % (t["id"][:8], tent))
    return novos, mudou


def put(c, cur, templates):
    """Mesmo corpo do g.publicar (preserva allowMultiple etc.)."""
    return c.request("PUT", "/workflow/" + g.LOC + "/" + cur["id"],
                     {"name": cur.get("name"), "status": "published",
                      "version": cur.get("version", 1),
                      "allowMultiple": cur.get("allowMultiple", True),
                      "stopOnResponse": cur.get("stopOnResponse", False),
                      "allowMultipleOpportunity": cur.get("allowMultipleOpportunity", False),
                      "timezone": cur.get("timezone", "account"),
                      "window": cur.get("window"),
                      "workflowData": {"templates": templates}})


if __name__ == "__main__":
    aplicar = "--aplicar" in sys.argv
    c = g.client()
    os.makedirs(BACKUP, exist_ok=True)
    for wf, nome in ALVOS.items():
        cur = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
        tpl = (cur.get("workflowData") or {}).get("templates") or []
        novos, mudou = corrigir(tpl)
        print("== %s (%s) status=%s nos=%d mudancas=%d"
              % (nome, wf[:8], cur.get("status"), len(tpl), len(mudou)))
        for m in mudou:
            print("   " + m)
        if not aplicar or not mudou:
            continue
        g.export(c, wf, os.path.join(BACKUP, nome + ".json"))
        r = put(c, cur, novos)
        if r and r.get("_error"):
            print("   FALHA no PUT: " + str(r.get("message"))[:200])
            continue
        volta = c.request("GET", "/workflow/" + g.LOC + "/" + wf)
        vt = (volta.get("workflowData") or {}).get("templates") or []
        mesmos_ids = [t["id"] for t in vt] == [t["id"] for t in tpl]
        _, resto = corrigir(vt)
        tr = c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + wf)
        print("   conferido: status=%s nos=%d ids iguais=%s pendencias=%d "
              "allowMultiple=%s gatilhos ativos=%s"
              % (volta.get("status"), len(vt), mesmos_ids, len(resto),
                 volta.get("allowMultiple"), [t.get("active") for t in tr]))
        g.export(c, wf, os.path.join(AQUI, "..", "workflows-json", nome + ".json"))
