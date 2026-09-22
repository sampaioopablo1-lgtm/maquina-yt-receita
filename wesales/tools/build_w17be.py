"""W17b - Fila Travada  e  W17e - Retorno Vencido.

W17b (spec W17b): gatilhos Contact Tag Added fila-tel E fila-wa (dois)
  0 Remove tag fila-travada
  1 Wait ate 19:00
  2 If/Else Tags inclui fila-tel OU fila-wa
       sim -> Add tag fila-travada -> notifica gestor -> Note
       nao -> FIM

W17e (spec W17e): gatilho Contact Changed em 'Data de retorno'
  1 Update  Checkpoint - Data de retorno = {{contact.data_de_retorno}}
  2 Wait ate 19:00 da data do checkpoint (merge field)
  3 If/Else 'Data de retorno' == checkpoint   nao -> FIM (promessa renovada)
  4 If/Else resultado=='Pediu retorno' E etapa==CONECTAR E status==open
       sim -> Add tag retorno-vencido -> notifica gestor -> Note
       nao -> FIM
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

CAMPOS = json.load(open(os.path.join(os.path.dirname(__file__), "campos.json"),
                        encoding="utf-8"))
DATA_RET = CAMPOS["Data de retorno"]
CHK_DATA = CAMPOS["Checkpoint — Data de retorno"]
RESULTADO = CAMPOS["Resultado da tentativa"]
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "workflows-json"))
VAL_DATA_RET = "{{contact." + DATA_RET["chave"].split(".", 1)[1] + "}}"
VAL_CHK = "{{contact." + CHK_DATA["chave"].split(".", 1)[1] + "}}"


def entrega(c, nome, passos, gatilhos, tags=()):
    for t in tags:
        c.create_location_tag(t)
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)
           if w.get("type") == "workflow"}
    if nome in ids:
        wf = ids[nome]
        g.preencher(c, wf, nome, passos, gatilhos)
        print("  reescrito: " + wf)
    else:
        wf = g.build(c, nome, passos, gatilhos,
                     allow_reentry=True, stop_on_response=False)
        print("  criado: " + wf)
    doc = g.export(c, wf, os.path.join(JSON_DIR, nome + ".json"))
    w = doc["workflow"]
    tpl = (w.get("workflowData") or {}).get("templates") or []
    print("  nos=%d re-entry=%s" % (len(tpl), w.get("allowMultiple")))
    for s in tpl:
        a = s.get("attributes") or {}
        det = ""
        if s.get("nodeType") == "condition-node":
            seg = a["branches"][0]["segments"][0]
            det = "%s: %s" % (seg["operator"].upper(),
                              " / ".join("%s %s %s" % (x["conditionSubType"][:22],
                                                       x["conditionOperator"],
                                                       x["conditionValue"])
                                         for x in seg["conditions"]))
        elif s["type"] == "wait":
            det = "%s h=%s m=%s data=%s" % (a.get("type"),
                                            a.get("specificTimeHour"),
                                            a.get("specificTimeMinute"),
                                            a.get("specificDate"))
        elif s["type"] in ("add_contact_tag", "remove_contact_tag"):
            det = str(a.get("tags"))
        elif s["type"] == "update_contact_field":
            f = a["fields"][0]
            det = "%s = %s" % (f["title"], f["value"])
        print("    %-16s %s" % (s.get("nodeType") or s["type"], det))
    print("  " + ("PUBLICADO" if g.publicar(c, wf) else "NAO PUBLICOU"))


c = g.client()

# ---------------- W17b ----------------
print("########## Fila Travada (W17b)")
passos_b = [
    g.tag_step(["fila-travada"], remove=True),
    g.wait_step(8, "hours"),   # fecha o dia: ver nota do W11
    g.Branch(
        "Fila ainda presa?",
        [g.cond("contact_detail", "tags", "index-of-true", ["fila-tel"]),
         g.cond("contact_detail", "tags", "index-of-true", ["fila-wa"])],
        operador="or",
        sim=[
            g.tag_step(["fila-travada"]),
            g.notify_user_step(
                "Fila travada",
                "{{contact.name}} está com fila-tel/fila-wa presa desde antes "
                "de hoje às 18:30 — o nó 9 da cadência não rodou. "
                "Tentativa nº {{contact.tentativa_n}}."),
            g.note_step("Alerta de saúde",
                        "Alerta de saúde: fila-tel/fila-wa travada, nó 9 não "
                        "removeu até 18:30 · " + g.token("right_now")),
        ],
        nao=[],
    ),
]
gat_b = [g.tag_trigger("Fila Tel", "fila-tel"),
         g.tag_trigger("Fila Wa", "fila-wa")]
entrega(c, "Fila Travada", passos_b, gat_b, tags=["fila-travada"])

# ---------------- W17e ----------------
print("\n########## Retorno Vencido (W17e)")
b4 = g.Branch(
    "Promessa vencida sem reclassificar?",
    [g.cond("contact_detail", RESULTADO["id"], "==", "Pediu retorno"),
     g.cond("opportunities", "pipelineStageId", "==", g.STAGES["CONECTAR"]),
     g.cond("opportunities", "status", "==", "open")],
    sim=[
        g.tag_step(["retorno-vencido"]),
        g.notify_user_step(
            "Retorno prometido venceu",
            "{{contact.name}} tinha retorno prometido para " + VAL_DATA_RET
            + " e ainda não foi reclassificado."),
        g.note_step("Alerta de saúde",
                    "Alerta de saúde: retorno vencido sem nova classificação · "
                    + g.token("right_now")),
    ],
    nao=[],
)
passos_e = [
    g.field_step(CHK_DATA["id"], "Checkpoint — Data de retorno",
                 VAL_DATA_RET, "date"),
    # LIMITACAO CONHECIDA: a spec pede esperar ATE a data prometida.
    # O wait `specific_date` exige specificDate + specificTimePeriod e,
    # mesmo com os dois, nao passou na publicacao; e nao ha operador de
    # comparacao de datas para conferir "ja passou". Esperar 2 dias e uma
    # aproximacao: pega a maioria dos retornos prometidos, mas alerta cedo
    # para promessa longa. Revisitar quando houver comparacao de data.
    g.wait_step(2, "days"),
    g.Branch(
        "A data ainda é a mesma?",
        [g.cond("contact_detail", DATA_RET["id"], "==", VAL_CHK)],
        sim=[b4], nao=[],
    ),
]
gat_e = [{
    "status": "draft", "schedule_config": {},
    "type": "contact_changed", "masterType": "highlevel",
    "name": "Contato Alterado", "active": True, "triggersChanged": True,
    "location_id": g.LOC,
    "conditions": [{"operator": "has-changed",
                    "field": "contact." + DATA_RET["id"],
                    "title": "Data de retorno", "type": "select",
                    "id": DATA_RET["id"]}],
}]
entrega(c, "Retorno Vencido", passos_e, gat_e, tags=["retorno-vencido"])
