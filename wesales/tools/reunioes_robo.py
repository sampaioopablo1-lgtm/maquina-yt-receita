#!/usr/bin/env python3
"""Reunião confirmada de verdade e resultado sempre registrado (30/09, auditoria da agenda).

Achados que motivaram: 100% de no-show até 30/09; a confirmação por ligação não aconteceu (ligações de
11-19 s), só reunião do Calendly ganhava tarefa de confirmação, e reunião que passava sem o closer marcar
Compareceu/No-show deixava o lead parado em REUNIÃO (nada dispara).

  1. CONFIRMAR: toda reunião "confirmed" das duas agendas que começa nas próximas 26 h ganha a tarefa
     "[LIGAR AGORA] Confirmar a reunião de dd/mm HH:MM" (SDR) e a tag `confirmar-reuniao` (nível 10 da
     Minha fila). Fecha só com conversa (ligação de 25 s ou mais, ou Registro da ligação "Atendeu").
  2. RESULTADO: reunião que terminou há 15 min e segue "confirmed" ganha a tarefa "[RESULTADO] ..." para o
     closer. Fecha sozinha quando o status muda (Compareceu, No-show, Cancelada).
  3. SEM RESULTADO ATÉ 10:00 DO DIA SEGUINTE: marca No-show (nota explicando) e a cadência 6x15 começa
     (cadencia_noshow.py). Regra do dono: tarefa pendente não é fechada sem a ação; aqui a ação é o
     próprio registro que faltou, e o lead não fica esquecido em REUNIÃO.

    python3 reunioes_robo.py            # DRY
    python3 reunioes_robo.py --aplicar
"""
from __future__ import annotations

import datetime as dt
import sys

from atuador_filas import LOC, pedir

BR = dt.timezone(dt.timedelta(hours=-3))
AGENDAS = {"oOfR9ADPJM0WyVyHRgKE": "Reunião com closer", "3uNQFjCEDe7b4gKZJuOZ": "Agendamento pela SDR"}
SDR, CLOSER = "ML69c5kAJ93cliAGgBj6", "JdvhvOTEBTvUyRi0BXU8"
TAG_CONF = "confirmar-reuniao"


def local(s: str) -> dt.datetime:
    d = dt.datetime.fromisoformat(s.replace(" ", "T").replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=BR)


def utc(d: dt.datetime) -> str:
    return d.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def tarefas(cid):
    return pedir("GET", "/contacts/%s/tasks" % cid).get("tasks") or []


def acao(agora, e):
    """Pura: 'confirmar' | 'resultado' | 'noshow' | None para um evento."""
    if (e.get("appointmentStatus") or "") != "confirmed" or not e.get("contactId"):
        return None
    ini, fim = local(e["startTime"]), local(e.get("endTime") or e["startTime"])
    if agora < ini <= agora + dt.timedelta(hours=26):
        return "confirmar"
    limite = dt.datetime.combine(ini.astimezone(BR).date() + dt.timedelta(days=1), dt.time(10, 0), BR)
    if agora >= limite:
        return "noshow"
    if agora >= fim + dt.timedelta(minutes=15):
        return "resultado"
    return None


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    agora = dt.datetime.now(dt.timezone.utc)
    ini, fim = int((agora - dt.timedelta(days=4)).timestamp() * 1000), int((agora + dt.timedelta(hours=27)).timestamp() * 1000)
    evs = []
    for cal in AGENDAS:
        evs += pedir("GET", "/calendars/events?locationId=%s&calendarId=%s&startTime=%d&endTime=%d"
                     % (LOC, cal, ini, fim)).get("events") or []
    # [RESULTADO] fecha quando o status da reunião deixou de ser "confirmed"
    por_quando = {(e.get("contactId"), local(e["startTime"]).astimezone(BR).strftime("%d/%m %H:%M")): e for e in evs}
    for e in evs:
        cid = e.get("contactId")
        if not cid:
            continue
        quando = local(e["startTime"]).astimezone(BR).strftime("%d/%m %H:%M")
        # Confirmação de reunião que já começou (ou saiu da agenda) não tem mais como ser feita: a tarefa fecha.
        # Não fecha se há outra reunião do mesmo lead, no mesmo horário, ainda por confirmar (remarcada em cima).
        if (local(e["startTime"]) <= agora or (e.get("appointmentStatus") or "") != "confirmed") and not any(
                o is not e and o.get("contactId") == cid and o["startTime"] == e["startTime"] and acao(agora, o) == "confirmar" for o in evs):
            for t in tarefas(cid):
                if "onfirmar a reunião de %s" % quando in (t.get("title") or "") and not t.get("completed"):
                    print("  fecha confirmação %s %s (reunião passou ou status %s)" % (quando, cid, e.get("appointmentStatus")))
                    if aplicar:
                        pedir("PUT", "/contacts/%s/tasks/%s/completed" % (cid, t["id"]), {"completed": True})
        if (e.get("appointmentStatus") or "") != "confirmed":
            for t in tarefas(cid):
                if t.get("title", "").startswith("[RESULTADO] Reunião de %s" % quando) and not t.get("completed"):
                    print("  fecha [RESULTADO] %s %s (status %s)" % (quando, cid, e.get("appointmentStatus")))
                    if aplicar:
                        pedir("PUT", "/contacts/%s/tasks/%s/completed" % (cid, t["id"]), {"completed": True})
            continue
        a = acao(agora, e)
        if not a:
            continue
        c = pedir("GET", "/contacts/%s" % cid).get("contact") or {}
        nome = (c.get("firstName") or c.get("contactName") or "?").strip()
        if c.get("dnd") or "nao-perturbe" in (c.get("tags") or []):
            continue
        ts = tarefas(cid)
        if a == "confirmar":
            da_reuniao = [t for t in ts if "onfirmar a reunião de %s" % quando in (t.get("title") or "")]
            ja = bool(da_reuniao)
            tem_tag = TAG_CONF in (c.get("tags") or [])
            # tarefa já concluída = reunião confirmada: a tag não volta (01/10: voltava a cada rodada e o lead
            # confirmado seguia no topo da Minha fila fora do horário do ordem_fila.py)
            if ja and (tem_tag or all(t.get("completed") for t in da_reuniao)):
                continue
            print("  confirmar  %-22s reunião %s%s" % (nome[:22], quando, "" if not ja else " (só a tag)"))
            if aplicar:
                if not ja:
                    link = e.get("address") or ""
                    pedir("POST", "/contacts/%s/tasks" % cid, {
                        "title": "[LIGAR AGORA] Confirmar a reunião de %s — %s" % (quando, nome),
                        "body": "Ligue e confirme a presença (conversa de verdade: a tarefa só fecha com ligação atendida "
                                "de 25 s ou mais, ou com o Registro da ligação \"Atendeu\"). Não atendeu: mande no WhatsApp "
                                "o link %s e peça \"Responde SIM pra confirmar\". Pediu para mudar: remarque ou cancele na "
                                "agenda na hora, para os lembretes pararem." % (link or "da reunião"),
                        "dueDate": utc(agora), "completed": False, "assignedTo": SDR})
                if not tem_tag:
                    pedir("POST", "/contacts/%s/tags" % cid, {"tags": [TAG_CONF]})
        elif a == "resultado":
            if any((t.get("title") or "").startswith("[RESULTADO] Reunião de %s" % quando) for t in ts):
                continue
            print("  resultado  %-22s reunião %s" % (nome[:22], quando))
            if aplicar:
                pedir("POST", "/contacts/%s/tasks" % cid, {
                    "title": "[RESULTADO] Reunião de %s — %s: compareceu, faltou ou remarcou?" % (quando, nome),
                    "body": "Calendários → a reunião → Status: Compareceu (Showed) ou Não compareceu (No-show); se "
                            "remarcou, mude a data. Depois, na ficha, preencha \"Reunião foi qualificada\". Sem registro "
                            "até as 10:00 de amanhã, o sistema marca No-show e a SDR começa a recuperação.",
                    "dueDate": utc(agora), "completed": False, "assignedTo": CLOSER})
        elif a == "noshow":
            print("  NO-SHOW    %-22s reunião %s (sem resultado até 10:00)" % (nome[:22], quando))
            if aplicar:
                pedir("PUT", "/calendars/events/appointments/%s" % e["id"], {"appointmentStatus": "noshow"})
                pedir("POST", "/contacts/%s/notes" % cid, {"body": "Reunião de %s marcada como No-show automaticamente: "
                      "o closer não registrou o resultado até as 10:00 do dia seguinte (reunioes_robo.py)." % quando})
    return 0


if __name__ == "__main__":
    sys.exit(main())
