#!/usr/bin/env python3
"""Calendly → CRM (28/09, pedido do dono). O Calendly fica (já está integrado às campanhas);
o CRM passa a saber de cada reunião marcada nele.

Roda no relógio do GitHub (a cada 30 min). Para cada evento ativo do Calendly que começa a
partir de agora e ainda não está no CRM:
  1. acha o contato por e-mail ou telefone (cria, se não existir), tag `calendly`;
  2. registra a reunião na agenda "Reunião com closer", no mesmo horário, com o closer como dono.
     Isso a faz aparecer na agenda do CRM e dispara o Pós-agendamento (confirmação, lembretes,
     tarefa do grupo, aviso ao closer);
  3. lead ouro (marcou sozinho na agenda do dono): Prioridade 5, `fila-quente` e tarefa "[LIGAR AGORA] Agendou pelo
     Calendly — confirmar a reunião" para a SDR (confirmar e completar Q1–Q6 antes da reunião).
  4. tag `calendly-ouro` -> workflow "Calendly — lead ouro (aviso à SDR)" (criar_calendly_ouro.py)
     manda notificação interna à SDR: ligar, qualificar e criar o grupo.

Duplicidade: o título da reunião no CRM leva `calendly:<uuid do evento>`; se já existe, pula.
Cancelou ou remarcou no Calendly (remarcar = cancela o antigo e cria outro): a reunião antiga é
cancelada no CRM, para os lembretes não saírem para um horário morto; a nova entra pelo passo 2.
Mesmo link: o Calendly e o CRM estão na mesma agenda do Google e cada um gera o seu Meet. A reunião
no CRM leva o link do Calendly (o do convite que o lead recebeu), para os lembretes apontarem para
a mesma sala; as já gravadas com outro link são corrigidas a cada rodada.
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
import unicodedata
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
    return {"nome": inv.get("name") or "", "email": (inv.get("email") or "").lower(), "criado": inv.get("created_at") or "",
            "telefone": ("+" + tel) if tel else "",
            "respostas": [(qa.get("question"), qa.get("answer")) for qa in inv.get("questions_and_answers") or []]}


def no_crm(uuid, inicio):
    t0 = int((inicio - dt.timedelta(hours=1)).timestamp() * 1000)
    t1 = int((inicio + dt.timedelta(hours=1)).timestamp() * 1000)
    st, r = ghl("GET", "/calendars/events?locationId=%s&calendarId=%s&startTime=%d&endTime=%d" % (LOC, CAL_CLOSER, t0, t1))
    return [e for e in r.get("events", []) if uuid in (e.get("title") or "")]


def link_calendly(ev):
    loc = ev.get("location") or {}
    return loc.get("join_url") or (loc.get("location") if str(loc.get("location") or "").startswith("http") else "")


def nota_ouro(quando, link):
    """Destaque no topo das Observações da ficha (a nota mais nova fica em cima do roteiro)."""
    return ('<p><b>⭐⭐⭐ LEAD OURO — AGENDOU REUNIÃO SOZINHO PELO CALENDLY ⭐⭐⭐</b></p>'
            '<p><b>Reunião com o Pablo: %s</b>%s</p>'
            '<p><b>Ligue AGORA:</b> 1) confirme a presença; 2) qualifique Q1–Q6 no formulário; '
            '3) crie o grupo com o closer. <b>Não agende de novo — a reunião já está marcada.</b></p>'
            % (quando, (' · <a href="%s" target="_blank">link da reunião</a>' % link) if link else ""))


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


def _primeiro(nome):
    n = unicodedata.normalize("NFKD", nome or "").encode("ascii", "ignore").decode().lower().split()
    return n[0] if n else ""


def lead_do_formulario(p):
    """O lead preenche o formulário da Meta (nome, telefone, e-mail) e, na última etapa, marca no
    Calendly — que não pede telefone e onde ele às vezes digita outro e-mail (29/09: Ana Lucia,
    contato duplicado sem telefone). Casa pelo primeiro nome entre os contatos do Facebook criados
    nas 12 h antes do agendamento; só aceita se houver exatamente um."""
    nome = _primeiro(p["nome"])
    if not nome or not p.get("criado"):
        return None
    fim = dt.datetime.fromisoformat(p["criado"].replace("Z", "+00:00"))
    ini = fim - dt.timedelta(hours=12)
    st, r = ghl("POST", "/contacts/search", {"locationId": LOC, "pageLimit": 100, "filters": [
        {"field": "dateAdded", "operator": "range", "value": {
            "gte": ini.strftime("%Y-%m-%dT%H:%M:%SZ"), "lte": (fim + dt.timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")}}]})
    achados = [c for c in r.get("contacts", []) if (c.get("source") or "").lower() == "facebook" and c.get("phone")
               and _primeiro((c.get("firstName") or "") + " " + (c.get("lastName") or "")) == nome]
    if len(achados) == 1:
        print("    casado com o lead do formulário da Meta: %s %s" % (achados[0]["id"], achados[0].get("phone")))
        return achados[0]["id"]
    if len(achados) > 1:
        print("    %d leads do formulário com o nome %r — não caso sozinho" % (len(achados), nome))
    return None


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
    cid = lead_do_formulario(p)
    if cid:
        return cid, False
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
        link = link_calendly(ev)
        ja = no_crm(uuid, inicio)
        for e in ja:
            st, d = ghl("GET", "/calendars/events/appointments/%s" % e["id"])
            atual = ((d.get("appointment") or d) if isinstance(d, dict) else {}).get("address") or ""
            if link and atual != link:
                print("  ~ link: %s · CRM %s -> Calendly %s%s" % (e.get("title"), atual or "(vazio)", link, "" if aplicar else " (DRY)"))
                if aplicar:
                    st, _ = ghl("PUT", "/calendars/events/appointments/%s" % e["id"], {"address": link})
                    print("    agenda do CRM: link trocado, HTTP %s" % st)
        if ja:
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
            "appointmentStatus": "confirmed", "ignoreDateRange": True, **({"meetingLocationType": "custom", "address": link} if link else {}), "ignoreFreeSlotValidation": True,
            "toNotify": False})
        print("    agenda do CRM: HTTP %s" % st)
        resp = "; ".join("%s: %s" % (q, a) for q, a in p["respostas"] if a)[:800]
        ghl("POST", "/contacts/%s/tasks" % cid, {
            "title": "[LIGAR AGORA] Agendou pelo Calendly — confirmar a reunião de %s" % quando,
            "body": ("Lead extremamente quente: marcou reunião com o closer pelo Calendly para %s. Ligue agora, "
                     "confirme a presença e complete Q1–Q6 na ficha. Respostas do Calendly: %s" % (quando, resp or "—")),
            "dueDate": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "completed": False, "assignedTo": SDR})
        ghl("POST", "/contacts/%s/notes" % cid, {"body": nota_ouro(quando, link)})
        # dispara "Calendly — lead ouro (aviso à SDR)": notificação especial, depois o workflow tira a tag
        ghl("POST", "/contacts/%s/tags" % cid, {"tags": ["calendly-ouro"]})
    cancelar_no_crm(aplicar)
    return 0


if __name__ == "__main__":
    sys.exit(main())
