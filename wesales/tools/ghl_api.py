"""WeSales - helpers da API interna do GHL (backend.leadconnectorhq.com).

Formatos de no e de gatilho foram lidos de workflows REAIS desta subconta
(Mestre de saida, 21/09/2026), nao inventados. Todo workflow nasce RASCUNHO:
nenhuma funcao aqui publica.
"""
from __future__ import annotations

import json
import os
import sys
import time
import uuid

LOC = "1D53YTI9C7oIMBavcQxV"          # UNICA subconta permitida
PIPELINE = "0Fo2xbeayE4EP6yuSUtq"
STAGES = {
    "NOVO LEAD": "7ae9c950-9bcf-4e60-8bc5-cb7388c87b7d",
    "CONECTAR": "deb60542-a5cd-43ae-b875-b467b120a72c",
    "AGENDAR": "3d26fcd1-220d-49ed-8325-705dfe9055b1",
    "NEGOCIAR": "cbcf0229-5e19-4fdb-8c50-6c641b78b3bb",
    "FORMALIZAR": "b8485ec0-98e8-459f-b990-f40a5e3bd25b",
}
USER = "JdvhvOTEBTvUyRi0BXU8"

_HERE = os.path.dirname(os.path.abspath(__file__))
BEARER_FILE = os.path.join(_HERE, "..", ".local", "_ghl_bearer.txt")
CLI_PATH = os.path.abspath(os.path.join(_HERE, "..", "..", "gohighlevel-cli"))

# workflows PUBLICADOS: nunca editar (regra inviolavel do dono)
PUBLICADOS = {
    "e08a1580-975b-4c0f-934e-582fc6a0dbaa": "Porta de Entrada",
    "30da2c98-5f84-4af9-9ed2-71f628dc7c1e": "Mestre de saida",
    "cf6fa19d-6af8-4fcb-b0dd-6fcfcefde0cc": "Pos-ligacao",
    "94a837d0-d87a-438e-95f1-c620d55f1a7f": "Pos-agendamento",
    "ea0a49b7-f3a9-4d8a-8acd-802975d6db03": "Interceptacao de Sinal - Clique.",
    "7a1b4e6b-7e6e-4ed8-8ff4-cd98b88cdcff": "Interceptacao de Sinal - Resposta",
}


NODE_PATH_GLOBAL = r"C:\Users\sampa\AppData\Roaming\npm\node_modules"


def _minutos_restantes(tok: str) -> float:
    import base64
    try:
        p = tok.split(".")[1]
        p += "=" * (-len(p) % 4)
        exp = json.loads(base64.urlsafe_b64decode(p)).get("exp", 0)
        return (float(exp) - time.time()) / 60.0
    except Exception:
        return -1.0


def renovar_bearer() -> bool:
    """Roda o renew.js (headless, perfil ja logado) e recarrega o token."""
    import subprocess
    env = dict(os.environ, NODE_PATH=NODE_PATH_GLOBAL)
    r = subprocess.run(["node", os.path.join(_HERE, "renew.js")],
                       capture_output=True, text=True, timeout=420,
                       cwd=_HERE, env=env)
    ok = r.returncode == 0
    print("  [bearer] renovacao " + ("ok" if ok else "FALHOU: " + r.stdout[-300:]))
    return ok


def client(min_minutos: float = 8.0):
    """Cliente da API interna, renovando o bearer se estiver perto de vencer."""
    if CLI_PATH not in sys.path:
        sys.path.insert(0, CLI_PATH)
    tok = open(BEARER_FILE, encoding="utf-8").read().strip()
    if _minutos_restantes(tok) < min_minutos:
        print("  [bearer] faltam %.1f min - renovando" % _minutos_restantes(tok))
        if renovar_bearer():
            tok = open(BEARER_FILE, encoding="utf-8").read().strip()
    os.environ["GHL_BACKEND_BEARER"] = tok
    from cli_anything.gohighlevel.utils.ghl_internal_client import (
        TokenManager, InternalGHLClient)
    return InternalGHLClient(TokenManager(), LOC)


def uid() -> str:
    return str(uuid.uuid4())


def guard(wf_id: str) -> None:
    if wf_id in PUBLICADOS:
        raise SystemExit(
            "RECUSADO: " + wf_id + " e o workflow PUBLICADO '"
            + PUBLICADOS[wf_id] + "'. Regra do dono: nunca editar.")


# -- nos (formato lido de workflow real) ---------------------------------

def token(var: str) -> str:
    """Merge field no formato que a tela grava (span data-cv-variable)."""
    return ('<span data-cv-variable="' + var + '" data-cv-token="true">'
            + "{{" + var + "}}" + "</span>")


def note_step(title: str, html_body: str, color: str = "#FEF0C7") -> dict:
    return {
        "id": uid(), "name": "Note", "type": "add_notes",
        "attributes": {
            "html": '<p style="padding-left: 0px!important;">' + html_body + "</p>",
            "color": color, "type": "add_notes", "title": title,
        },
    }


def tag_step(tags: list, remove: bool = False) -> dict:
    return {
        "id": uid(),
        "name": "Remove Tag" if remove else "Add Tag",
        "type": "remove_contact_tag" if remove else "add_contact_tag",
        "attributes": {"tags": tags},
    }


def wait_step(value: int, unit: str = "days") -> dict:
    api_unit = {"minutes": "minutes", "hours": "hour", "hour": "hour",
                "days": "days"}.get(unit, unit)
    label = {"minutes": "Minutes", "hour": "Hour", "hours": "Hours",
             "days": "Days"}.get(unit, unit.title())
    disp = "Wait " + str(value) + " " + label
    return {
        "id": uid(), "name": disp, "type": "wait", "cat": "",
        "attributes": {
            "type": "time",
            "startAfter": {"type": api_unit, "value": value, "when": "after"},
            "name": disp, "cat": "", "isHybridAction": True,
            "hybridActionType": "wait", "convertToMultipath": False,
            "transitions": [],
        },
    }


def link(steps: list) -> list:
    """Encadeia nos lineares com order/parentKey/next."""
    out = []
    for i, s in enumerate(steps):
        s = dict(s)
        s["order"] = i
        s["parentKey"] = steps[i - 1]["id"] if i > 0 else None
        if i < len(steps) - 1:
            s["next"] = steps[i + 1]["id"]
        out.append(s)
    return out


def tag_trigger(name: str, tag: str) -> dict:
    return {
        "status": "draft", "schedule_config": {},
        "conditions": [{"operator": "index-of-true", "field": "tagsAdded",
                        "value": tag, "title": "Tag Added", "type": "select",
                        "id": "tag-added"}],
        "type": "contact_tag", "masterType": "highlevel", "name": name,
        "active": True, "triggersChanged": True, "location_id": LOC,
    }


# -- montagem ------------------------------------------------------------

def create_workflow(c, name: str) -> str:
    r = c.request("POST", "/workflow/" + LOC, {"name": name})
    if not r or r.get("_error") or not r.get("id"):
        raise SystemExit("falha ao criar workflow '" + name + "': " + str(r))
    return r["id"]


def build(c, name: str, steps: list, triggers: list,
          tags_to_create=None, allow_reentry: bool = True,
          stop_on_response: bool = False) -> str:
    """Cria workflow RASCUNHO com nos e gatilhos. Devolve o id."""
    wf = create_workflow(c, name)
    steps = link(steps)

    for t in (tags_to_create or []):
        c.create_location_tag(t)

    saved = []
    for tdef in triggers:
        body = dict(tdef)
        body["workflowId"] = wf
        body["location_id"] = LOC
        body["actions"] = [{"workflow_id": wf, "type": "add_to_workflow"}]
        tr = c.request("POST", "/workflow/" + LOC + "/trigger", body)
        if not tr or tr.get("_error") or not tr.get("id"):
            print("  ! gatilho '" + str(tdef.get("name")) + "' falhou: " + str(tr))
            continue
        tid = tr["id"]
        c.request("PUT", "/workflow/" + LOC + "/trigger/" + tid,
                  dict(body, targetActionId=steps[0]["id"],
                       advanceCanvasMeta={"position": {"x": 57.5, "y": -73}}))
        saved.append(dict(body, id=tid))

    put = c.request("PUT", "/workflow/" + LOC + "/" + wf,
                    {"name": name, "version": 1,
                     "workflowData": {"templates": steps}})
    if not put or put.get("_error"):
        raise SystemExit("falha ao salvar nos de '" + name + "': " + str(put))

    cur = c.request("GET", "/workflow/" + LOC + "/" + wf)
    now = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    tl = []
    for t in saved:
        t = dict(t, workflow_id=wf, location_id=LOC, belongs_to="workflow",
                 deleted=False, date_added=now, date_updated=now,
                 advanceCanvasMeta={"position": {"x": 57.5, "y": -73}})
        for k in ("company_id", "company_age", "triggersChanged",
                  "workflowId", "status"):
            t.pop(k, None)
        tl.append(t)
    meta = (cur.get("meta") or {}) if isinstance(cur, dict) else {}
    meta["advanceCanvasMeta"] = {"enabled": True, "enabledAt": now}
    swm = []
    for i, s in enumerate(steps):
        s = dict(s, advanceCanvasMeta={"position": {"x": 400 + i * 300, "y": 0}})
        s.setdefault("cat", "")
        swm.append(s)
    ver = cur.get("version", 2) if isinstance(cur, dict) else 2
    # status='draft' e OBRIGATORIO: sem ele o workflow existe na API mas nao
    # aparece na lista da tela (a lista filtra por status). Descoberto no
    # PASSO 1, 21/09/2026. 'draft' nunca publica.
    c.request("PUT", "/workflow/" + LOC + "/" + wf,
              {"name": name, "status": "draft", "version": ver, "meta": meta,
               "allowMultiple": allow_reentry,
               "stopOnResponse": stop_on_response,
               "workflowData": {"templates": swm},
               "triggersChanged": bool(tl), "oldTriggers": tl,
               "newTriggers": tl})
    return wf


def export(c, wf_id: str, path: str) -> dict:
    """Le workflow + gatilhos de volta e grava o JSON completo."""
    wf = c.request("GET", "/workflow/" + LOC + "/" + wf_id)
    tr = c.request("GET", "/workflow/" + LOC + "/trigger?workflowId=" + wf_id)
    doc = {"workflow": wf, "triggers": tr}
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    return doc
