#!/usr/bin/env python3
"""Formulário "Qualificação e agendamento — SDR": pergunta "Lead já tem reunião marcada?" (30/09, pedido do dono).

O formulário sempre levava para a agenda ao enviar; para lead que já tinha reunião, isso abria a porta
para uma segunda reunião. Agora:
  - campo obrigatório "Lead já tem reunião marcada?" (Sim/Não), na seção "Agenda", antes do botão;
  - Sim  -> lógica condicional `displayCustomMessage`: salva a qualificação e encerra, sem agenda;
  - Não  -> nenhuma regra: vale o redirecionamento padrão do formulário (agenda com o contato fixo),
            que é o caminho que já funcionava — não foi recriado como regra de propósito.
O botão passa de "Enviar e agendar reunião" para "Enviar".

Salvar = POST /forms/{id} na API interna (o mesmo que o editor faz), com {name, formData}.
Idempotente. Backup do formulário em .local/ antes de gravar.

    python3 form_reuniao_marcada.py            # DRY: mostra o que mudaria
    python3 form_reuniao_marcada.py --aplicar  # precisa de GHL_PIT (campo) e do bearer (formulário)
"""
from __future__ import annotations

import copy
import json
import os
import sys
import time

import ghl_interno as gi
from atuador_filas import LOC, pedir as pit

FORM_ID = "ww2ruVG5CdJ7rWJ83Gbf"
PASTA_FICHA = "zHU4yGXKHdxBHnGxUmai"
NOME = "Lead já tem reunião marcada?"
OPCOES = ["Não", "Sim"]
BOTAO = '<p style="padding-left: 0px!important;">Enviar</p>'
CABECALHO = "<p><strong>Agenda</strong></p>"
MENSAGEM = ("<p style='font-family: Inter, sans-serif; font-size: 18px; font-weight: 600; text-align: center; margin: 0;'>✅</p>"
            "<p style='font-family: Inter, sans-serif; font-size: 16px; font-weight: 600; text-align: center; margin: 4px 0 0; color: #101828;'>"
            "Qualificação salva.</p>"
            "<p style='font-family: Inter, sans-serif; font-size: 14px; text-align: center; margin: 4px 0 0; color: #101828;'>"
            "Este lead já tem reunião marcada: não marque outra. Confira data e hora na ficha do contato.</p>")


def garantir_campo(aplicar: bool) -> dict | None:
    cf = pit("GET", "/locations/%s/customFields" % LOC)["customFields"]
    campo = next((f for f in cf if f["name"] == NOME), None)
    if campo or not aplicar:
        return campo
    r = pit("POST", "/locations/%s/customFields" % LOC,
            {"name": NOME, "dataType": "SINGLE_OPTIONS", "model": "contact", "options": OPCOES,
             "position": 595, "parentId": PASTA_FICHA})
    campo = r.get("customField") or r
    print("campo criado:", campo.get("id"), campo.get("fieldKey"))
    return campo


def elemento(campo: dict, modelo: dict) -> dict:
    """Elemento do formulário no mesmo formato do `SDR responsável` (single_options)."""
    el = copy.deepcopy(modelo)
    chave = campo["fieldKey"].split(".", 1)[1]
    el.update({"Id": campo["id"], "id": campo["id"], "tag": campo["id"], "customFieldLabel": NOME,
               "label": NOME, "name": NOME, "fieldKey": campo["fieldKey"], "hiddenFieldQueryKey": chave,
               "picklistOptions": OPCOES, "position": 595, "required": True, "placeholder": "",
               "dateAdded": campo.get("dateAdded", el.get("dateAdded"))})
    return el


def montar(form: dict, campo: dict) -> dict:
    """Pura: devolve o `form` novo (formData.form) com o campo, a regra e o botão."""
    fo = copy.deepcopy(form)
    fl = fo["fields"]
    if not any(x.get("tag") == campo["id"] for x in fl):
        modelo = next(x for x in fl if x.get("hiddenFieldQueryKey") == "sdr_responsvel")
        cab = copy.deepcopy(next(x for x in fl if x.get("tag") == "header"))
        cab["label"] = CABECALHO
        antes = next(i for i, x in enumerate(fl) if x.get("tag") in ("terms_and_conditions", "button"))
        fl[antes:antes] = [cab, elemento(campo, modelo)]
    for x in fl:
        if x.get("tag") == "button":
            x["label"] = BOTAO
    regra = {"conditions": [{"selectedField": campo["fieldKey"].split(".", 1)[1],
                             "selectedOperation": "isEqualTo", "inputValue": "Sim"}],
             "outcome": {"type": "displayCustomMessage", "value": MENSAGEM},
             "conditionalOperation": "then"}
    outras = [r for r in (fo.get("conditionalLogic") or [])
              if not any(c.get("selectedField") == regra["conditions"][0]["selectedField"] for c in r.get("conditions") or [])]
    fo["conditionalLogic"] = outras + [regra]
    fa = fo.get("formAction") or {}
    fa.setdefault("redirect_url", fa.get("redirectUrl"))   # o editor grava com esta chave
    return fo


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    campo = garantir_campo(aplicar)
    atual = gi.pedir("GET", "/forms/" + FORM_ID)
    atual = atual.get("form", atual)
    if not campo:
        print("DRY: criaria o campo `%s` (%s) e o poria no formulário" % (NOME, "/".join(OPCOES)))
        return 0
    novo = montar(atual["formData"]["form"], campo)
    labels = [str(x.get("label"))[:40] for x in novo["fields"]]
    print("campos:", len(atual["formData"]["form"]["fields"]), "->", len(labels), "| fim:", labels[-5:])
    print("regras:", json.dumps(novo["conditionalLogic"], ensure_ascii=False)[:300])
    if not aplicar:
        return 0
    aqui = os.path.dirname(os.path.abspath(__file__))
    bk = os.path.join(aqui, "..", ".local", "form-qualif-antes-%s.json" % time.strftime("%Y%m%d-%H%M%S"))
    json.dump(atual, open(bk, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    fd = copy.deepcopy(atual["formData"])
    fd["form"] = novo
    r = gi.pedir("POST", "/forms/" + FORM_ID, {"name": atual["name"], "formData": fd})
    time.sleep(5)   # medido 30/09: o GET logo após o POST ainda devolve a versão anterior
    salvo = gi.pedir("GET", "/forms/" + FORM_ID)
    salvo = salvo.get("form", salvo)["formData"]["form"]
    ok = (any(x.get("tag") == campo["id"] for x in salvo["fields"])
          and any(r2["outcome"]["type"] == "displayCustomMessage" for r2 in salvo.get("conditionalLogic") or [])
          and (salvo.get("formAction") or {}).get("redirectUrl") == (atual["formData"]["form"].get("formAction") or {}).get("redirectUrl"))
    print("salvo:", "OK" if ok else "CONFERIR", "| backup:", os.path.basename(bk), "| resposta:", str(r)[:120])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
