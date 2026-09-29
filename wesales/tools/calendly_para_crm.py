#!/usr/bin/env python3
"""Calendly → CRM (28/09, pedido do dono). O Calendly fica (já está integrado às campanhas);
o CRM passa a saber de cada reunião marcada nele.

Roda no relógio do GitHub (a cada 30 min). Para cada evento ativo do Calendly que começa a
partir de agora e ainda não está no CRM:
  1. acha o contato por e-mail ou telefone (cria, se não existir), tag `calendly`;
  2. registra a reunião na agenda "Reunião com closer", no mesmo horário, com o closer como dono.
     Isso a faz aparecer na agenda do CRM e dispara o Pós-agendamento (confirmação, lembretes,
     tarefa do grupo, aviso ao closer);
  3. lead extremamente quente: Prioridade 5, `fila-quente` e tarefa "[LIGAR AGORA] Agendou pelo
     Calendly — confirmar a reunião" para a SDR (confirmar e completar Q1–Q6 antes da reunião).

Duplicidade: o título da reunião no CRM leva `calendly:<uuid do evento>`; se já existe, pula.
Cancelou ou remarcou no Calendly (remarcar = cancela o antigo e cria outro): a reunião antiga é
cancelada no CRM, para os lembretes não saírem para um horário morto; a nova entra pelo passo 2.
Só lê o Calendly (API v2, token pessoal em CALENDLY_TOKEN). Nunca cancela nem altera evento lá.

    CALENDLY_TOKEN=... GHL_PIT=... python calendly_para_crm.py            # DRY: só mostra
    CALENDLY_TOKEN=... GHL_PIT=... python calendly_para_crm.py --aplicar
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request

from campos_bant import ghl, LOC

CAL_CLOSER = "3uNQFjCEDe7b4gKZJuOZ"          # "Reunião com closer"
CLOSER = "JdvhvOTEBTvUyRi0BXU8"
SDR = "ML69c5kAJ93cliAGgBj6"
PRIORIDADE = "chuJMRlKzY0Uq1f0lSkX"
API = "https://api.calendly.com"


def calendly(caminho: str):
    tok = os.environ.get("CALENDLY_TOKEN")
    if not tok:
        sys.exit("sem CALENDLY_TOKEN no ambiente")
    url = caminho if caminho.startswith("http") else API + caminho
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + tok.strip(), "Content-Type": "application/json",
                                               "Accept": "application/json", "User-Agent": "wesales-crm/1.0 (+github actions)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit("Calendly %s -> HTTP %s %s" % (url.split("?")[0], e.code, e.read()[:300].decode("utf-8", "replace")))


def eventos_futuros(status="active"):
    eu = calendly("/users/me")["resource"]
    agora = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = "/scheduled_events?user=%s&status=%s&min_start_time=%s&sort=start_time:asc&count=100" % (
        urllib.request.quote(eu["uri"], safe=""), status, agora)
    out = []
    while url:
        r = calendly(url)
        out += r.get("collection", [])
        url = (r.get("pagination") or {}).get("next_page")
    return out


def convidado(ev):
    r = calendly(ev["uri"] + "/invitees?status=active&count=10")
    inv = (r.get("collection") or [None])[0]
    if not inv:
        return None
    tel = inv.get("text_reminder_number") or ""
    for qa in inv.get("questions_and_answers") or []:
        if not tel and re.search(r"telefone|whats|celular|phone", qa.get("question", ""), re.I):
            tel = qa.get("answer") or ""
    tel = re.sub(r"\D", "", tel)
    if tel and not tel.startswith("55") and len(tel) in (10, 11):
        tel = "55" + tel
    return {"nome": inv.get("name") or "", "email": (inv.get("email") or "").lower(),
            "telefone": ("+" + tel) if tel else "",
            "respostas": [(qa.get("question"), qa.get("answer")) for qa in inv.get("questions_and_answers") or []]}


def no_crm(uuid, inicio):
    t0 = int((inicio - dt.timedelta(hours=1)).timestamp() * 1000)
    t1 = int((inicio + dt.timedelta(hours=1)).timestamp() * 1000)
    st, r = ghl("GET", "/calendars/events?locationId=%s&calendarId=%s&startTime=%d&endTime=%d" % (LOC, CAL_CLOSER, t0, t1))
    return [e for e in r.get("events", []) if uuid in (e.get("title") or "")]


def cancelar_no_crm(aplicar):
    for ev in eventos_futuros("canceled"):
        uuid = ev["uri"].rsplit("/", 1)[-1]
        inicio = dt.datetime.fromisoformat(ev["start_time"].replace("Z", "+00:00"))
        for e in no_crm(uuid, inicio):
            if (e.get("appointmentStatus") or "").lower() == "cancelled":
                continue
            quando = inicio.astimezone(dt.timezone(dt.timedelta(hours=-3))).strftime("%d/%m %H:%M")
            print("  - cancelada no Calendly: %s · %s%s" % (e.get("title"), quando, "" if aplicar else " (DRY)"))
            if aplicar:
                st, _ = ghl("PUT", "/calendars/events/appointments/%s" % e["id"], {"appointmentStatus": "cancelled"})
                print("    agenda do CRM: cancelada, HTTP %s" % st)


def achar_ou_criar(p, aplicar):
    for campo in ("email", "telefone"):
        v = p["email"] if campo == "email" else p["telefone"]
        if not v:
            continue
        st, r = ghl("POST", "/contacts/search", {"locationId": LOC, "pageLimit": 1,
                                                  "filters": [{"field": "email" if campo == "email" else "phone",
                                                               "operator": "eq", "value": v}]})
        if r.get("contacts"):
            return r["contacts"][0]["id"], False
    if not aplicar:
        return None, True
    corpo = {"locationId": LOC, "name": p["nome"], "email": p["email"] or None, "phone": p["telefone"] or None,
             "source": "Calendly", "tags": ["calendly"], "assignedTo": SDR}
    st, r = ghl("POST", "/contacts/upsert", {k: v for k, v in corpo.items() if v})
    return (r.get("contact") or {}).get("id"), True


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    evs = eventos_futuros()
    print("Calendly: %d reunião(ões) futura(s) ativa(s)%s" % (len(evs), "" if aplicar else " (DRY)"))
    for ev in evs:
        uuid = ev["uri"].rsplit("/", 1)[-1]
        inicio = dt.datetime.fromisoformat(ev["start_time"].replace("Z", "+00:00"))
        fim = dt.datetime.fromisoformat(ev["end_time"].replace("Z", "+00:00"))
        if no_crm(uuid, inicio):
            continue
        p = convidado(ev)
        if not p:
            continue
        cid, novo = achar_ou_criar(p, aplicar)
        quando = inicio.astimezone(dt.timezone(dt.timedelta(hours=-3))).strftime("%d/%m %H:%M")
        print("  + %s <%s> %s · %s · %s%s" % (p["nome"], p["email"], p["telefone"] or "sem telefone", quando,
                                             "contato novo" if novo else "contato existente", "" if aplicar else " (DRY)"))
        if not aplicar or not cid:
            continue
        ghl("POST", "/contacts/%s/tags" % cid, {"tags": ["calendly", "fila-quente"]})
        ghl("PUT", "/contacts/%s" % cid, {"customFields": [{"id": PRIORIDADE, "value": 5}]})
        st, ap = ghl("POST", "/calendars/events/appointments", {
            "calendarId": CAL_CLOSER, "locationId": LOC, "contactId": cid, "assignedUserId": CLOSER,
            "startTime": inicio.isoformat(), "endTime": fim.isoformat(),
            "title": "%s · Calendly (calendly:%s)" % (p["nome"] or "Reunião", uuid),
            "appointmentStatus": "confirmed", "ignoreDateRange": True, "ignoreFreeSlotValidation": True,
            "toNotify": False})
        print("    agenda do CRM: HTTP %s" % st)
        resp = "; ".join("%s: %s" % (q, a) for q, a in p["respostas"] if a)[:800]
        ghl("POST", "/contacts/%s/tasks" % cid, {
            "title": "[LIGAR AGORA] Agendou pelo Calendly — confirmar a reunião de %s" % quando,
            "body": ("Lead extremamente quente: marcou reunião com o closer pelo Calendly para %s. Ligue agora, "
                     "confirme a presença e complete Q1–Q6 na ficha. Respostas do Calendly: %s" % (quando, resp or "—")),
            "dueDate": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "completed": False, "assignedTo": SDR})
    cancelar_no_crm(aplicar)
    return 0


if __name__ == "__main__":
    sys.exit(main())
