#!/usr/bin/env python3
"""Simulacao ponta a ponta das reguas de reuniao, SO no contato de teste.

Marca uma reuniao no calendario "Reuniao com closer", espera os workflows
rodarem, rele contato/oportunidade/notas, cancela a reuniao e rele de novo.
Exercita: Pos-agendamento v2, Lembretes da Reuniao v3 (confirmacao) e
Reuniao Cancelada (que tem janela seg-sex 08:30-18:30: fora dela, a mensagem
e a tarefa saem na abertura da proxima janela).

Trava: o contato e fixo. Nao ha parametro que aponte para lead real.
Nao exclui nada: a reuniao termina com status `cancelled`, visivel no historico.
"""
from __future__ import annotations

import datetime as dt
import sys
import time

sys.path.insert(0, __import__("os").path.dirname(__file__))
from campos_bant import ghl, LOC  # noqa: E402

TESTE_CONTATO = "rdaijzR0ZVCmXLAJ6jT2"      # "pablo sampaio", numero do dono
TESTE_OPP = "VSRNAwP0kCub56Zjw4ZB"
CALENDARIO = "3uNQFjCEDe7b4gKZJuOZ"         # Reuniao com closer
TZ = "America/Sao_Paulo"
ESPERA = 90


def nomes() -> dict:
    st, r = ghl("GET", "/locations/%s/customFields?model=contact" % LOC)
    return {c["id"]: c.get("name") for c in (r.get("customFields") or [])}


def foto(rot: str, nm: dict) -> dict:
    st, c = ghl("GET", "/contacts/%s" % TESTE_CONTATO)
    c = c.get("contact") or {}
    st, o = ghl("GET", "/opportunities/%s" % TESTE_OPP)
    o = o.get("opportunity") or {}
    campos = {nm.get(f["id"], f["id"]): f.get("value") for f in c.get("customFields") or []}
    print("\n--- %s" % rot)
    print("  oportunidade: etapa=%s status=%s" % (o.get("pipelineStageId"), o.get("status")))
    print("  tags: %s" % sorted(c.get("tags") or []))
    return {"tags": set(c.get("tags") or []), "campos": campos,
            "etapa": o.get("pipelineStageId"), "status": o.get("status")}


def diff(a: dict, b: dict) -> None:
    print("  tags +%s -%s" % (sorted(b["tags"] - a["tags"]), sorted(a["tags"] - b["tags"])))
    for k in sorted(set(a["campos"]) | set(b["campos"]), key=str):
        if a["campos"].get(k) != b["campos"].get(k):
            print("  campo %-40s %r -> %r" % (k, a["campos"].get(k), b["campos"].get(k)))


def notas() -> None:
    st, r = ghl("GET", "/contacts/%s/notes" % TESTE_CONTATO, tolerar=(400, 404))
    ns = (r.get("notes") if isinstance(r, dict) else None) or []
    ns = sorted(ns, key=lambda n: n.get("dateAdded", ""), reverse=True)[:4]
    for n in ns:
        print("  NOTA %s\n    %s" % (n.get("dateAdded"), (n.get("body") or "").replace("\n", "\n    ")[:1500]))


def horario() -> tuple[str, str]:
    hoje = dt.datetime.now(dt.timezone.utc)
    ini = int((hoje + dt.timedelta(days=3)).timestamp() * 1000)
    fim = int((hoje + dt.timedelta(days=10)).timestamp() * 1000)
    st, r = ghl("GET", "/calendars/%s/free-slots?startDate=%d&endDate=%d&timezone=%s"
                % (CALENDARIO, ini, fim, TZ))
    dias = sorted(k for k in r if k[:1].isdigit())
    for d in dias:
        slots = (r[d] or {}).get("slots") or []
        if slots:
            s = slots[-1]                    # ultimo horario do dia: menos chance de colidir
            e = dt.datetime.fromisoformat(s) + dt.timedelta(minutes=60)
            return s, e.isoformat()
    raise SystemExit("sem horario livre em 10 dias: %s" % str(r)[:300])


def main() -> int:
    nm = nomes()
    a = foto("ANTES", nm)
    s, e = horario()
    print("\n>> marca reuniao %s -> %s" % (s, e))
    st, r = ghl("POST", "/calendars/events/appointments", {
        "calendarId": CALENDARIO, "locationId": LOC, "contactId": TESTE_CONTATO,
        "startTime": s, "endTime": e, "title": "TESTE simulacao ponta a ponta",
        "appointmentStatus": "confirmed", "toNotify": False})
    ev = r.get("id") or (r.get("appointment") or {}).get("id")
    print("  HTTP %s id=%s" % (st, ev))
    time.sleep(ESPERA)
    b = foto("DEPOIS DE MARCAR (%ds)" % ESPERA, nm)
    diff(a, b)
    notas()
    print("\n>> cancela a reuniao %s" % ev)
    st, r = ghl("PUT", "/calendars/events/appointments/%s" % ev,
                {"appointmentStatus": "cancelled", "toNotify": False})
    print("  HTTP %s status=%s" % (st, r.get("appointmentStatus") or r.get("status")))
    time.sleep(ESPERA)
    c = foto("DEPOIS DE CANCELAR (%ds)" % ESPERA, nm)
    diff(b, c)
    notas()
    ok = b["etapa"] == "3d26fcd1-220d-49ed-8325-705dfe9055b1" and b["status"] == "open"
    print("\n  veredito: Pos-agendamento %s" % ("moveu para REUNIAO DE DIAGNOSTICO" if ok
                                               else "NAO moveu a oportunidade"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
