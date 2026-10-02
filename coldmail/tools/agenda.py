"""Agenda e CRM (HighLevel): horários livres, contato, reunião, tarefa e nota.

A reunião entra na MESMA agenda que o calendly_para_crm.py usa ("Reunião com closer"), então tudo o que
já existe depois dela continua valendo sem mudança: pós-agendamento, convite com Meet, lembretes,
reunioes_robo.py (confirmação, resultado, no-show). A agenda do CRM está ligada ao Google Agenda do
closer, por isso os horários livres já descontam o que ele marcou por fora.

Só lead que respondeu com interesse vira contato no CRM: a lista fria inteira lá dentro dispararia a
Porta de Entrada (oportunidade em NOVO LEAD) para milhares de pessoas que nunca levantaram a mão.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "wesales" / "tools"))
import privacidade  # noqa: E402  (mascara nome/e-mail no log público do Actions)

GHL = "https://services.leadconnectorhq.com"
VERSAO = "2021-07-28"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/131.0.0.0 Safari/537.36")
BR = dt.timezone(dt.timedelta(hours=-3))

LOC = os.environ.get("GHL_LOCATION_ID") or "1D53YTI9C7oIMBavcQxV"
AGENDA = os.environ.get("COLDMAIL_AGENDA_ID") or "3uNQFjCEDe7b4gKZJuOZ"    # "Reunião com closer"
CLOSER = os.environ.get("COLDMAIL_CLOSER_ID") or "JdvhvOTEBTvUyRi0BXU8"
SDR = os.environ.get("COLDMAIL_SDR_ID") or "ML69c5kAJ93cliAGgBj6"
DURACAO_MIN = int(os.environ.get("COLDMAIL_DURACAO_MIN") or 30)
FUNIL = os.environ.get("COLDMAIL_FUNIL_ID") or "0Fo2xbeayE4EP6yuSUtq"                     # FUNIL DE VENDAS
ETAPA = os.environ.get("COLDMAIL_ETAPA_ID") or "7ae9c950-9bcf-4e60-8bc5-cb7388c87b7d"     # NOVO LEAD


def ativo() -> bool:
    return bool(os.environ.get("GHL_PIT"))


def pedir(metodo: str, rota: str, corpo=None):
    dados = None if corpo is None else json.dumps(corpo).encode("utf-8")
    for tentativa in range(4):
        req = urllib.request.Request(GHL + rota, data=dados, method=metodo)
        req.add_header("Authorization", "Bearer " + os.environ["GHL_PIT"])
        req.add_header("Version", VERSAO)
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", UA)          # sem isto: Cloudflare 1010
        if dados is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                t = r.read().decode("utf-8")
                saida = json.loads(t) if t else {}
                privacidade.registrar(saida)
                return saida
        except urllib.error.HTTPError as e:
            det = e.read().decode("utf-8", "replace")[:300]
            if (e.code == 429 or e.code >= 500) and tentativa < 3:
                time.sleep(2 ** tentativa * 3)
                continue
            raise RuntimeError("%s %s -> HTTP %s %s" % (metodo, rota.split("?")[0], e.code, det))
        except urllib.error.URLError as e:
            if tentativa < 3:
                time.sleep(2 ** tentativa * 3)
                continue
            raise RuntimeError("%s %s -> rede recusou: %s" % (metodo, rota.split("?")[0], e.reason))


def escolher_horarios(slots: list[str], agora: dt.datetime, por_dia: int = 2, dias: int = 3,
                      antecedencia_h: int = 4) -> list[str]:
    """Dos horários livres da agenda, oferece poucos e espalhados: até `por_dia` por dia (um de manhã e
    um à tarde, quando dá) em `dias` dias úteis, nunca antes de `antecedencia_h` horas a partir de agora."""
    limite = agora + dt.timedelta(hours=antecedencia_h)
    por_data: dict[dt.date, list[dt.datetime]] = {}
    for s in slots:
        try:
            t = dt.datetime.fromisoformat(s)
        except ValueError:
            continue
        if t.tzinfo is None:
            t = t.replace(tzinfo=BR)
        if t < limite or t.astimezone(BR).isoweekday() > 5:
            continue
        por_data.setdefault(t.astimezone(BR).date(), []).append(t)
    saida = []
    for data in sorted(por_data)[:dias]:
        ts = sorted(por_data[data])
        manha = [t for t in ts if t.astimezone(BR).hour < 12]
        tarde = [t for t in ts if t.astimezone(BR).hour >= 12]
        escolhidos = ([manha[len(manha) // 2]] if manha else []) + ([tarde[len(tarde) // 2]] if tarde else [])
        for t in (escolhidos or ts)[:por_dia]:
            saida.append(t.astimezone(BR).isoformat())
    return saida


def horarios_livres(agora: dt.datetime, dias_busca: int = 7) -> list[str]:
    inicio = int(agora.timestamp() * 1000)
    fim = int((agora + dt.timedelta(days=dias_busca)).timestamp() * 1000)
    r = pedir("GET", "/calendars/%s/free-slots?startDate=%d&endDate=%d&timezone=America/Sao_Paulo"
              % (AGENDA, inicio, fim))
    slots = []
    for chave, valor in (r or {}).items():
        if isinstance(valor, dict) and isinstance(valor.get("slots"), list):
            slots.extend(valor["slots"])
    return escolher_horarios(slots, agora)


def contato(lead: dict, tags: list[str]) -> str:
    corpo = {"locationId": LOC, "email": lead["email"], "firstName": lead.get("primeiro_nome") or None,
             "companyName": lead.get("empresa") or None, "website": lead.get("site") or None,
             "source": "Cold e-mail", "tags": tags, "assignedTo": SDR}
    r = pedir("POST", "/contacts/upsert", {k: v for k, v in corpo.items() if v})
    return ((r or {}).get("contact") or {}).get("id") or ""


def oportunidade(contato_id: str, nome: str) -> str:
    """Oportunidade em FUNIL DE VENDAS > NOVO LEAD. Se o contato já tem uma aberta nesse funil (criada pela
    Porta de Entrada ou por outra resposta), reaproveita: nunca duplica."""
    r = pedir("GET", "/opportunities/search?location_id=%s&contact_id=%s&pipeline_id=%s&status=open"
              % (LOC, contato_id, FUNIL))
    abertas = (r or {}).get("opportunities") or []
    if abertas:
        return abertas[0].get("id") or ""
    r = pedir("POST", "/opportunities/", {
        "pipelineId": FUNIL, "pipelineStageId": ETAPA, "locationId": LOC, "contactId": contato_id,
        "name": nome, "status": "open", "source": "Cold e-mail", "assignedTo": SDR})
    return ((r or {}).get("opportunity") or {}).get("id") or ""


def marcar(contato_id: str, inicio_iso: str, titulo: str) -> str:
    inicio = dt.datetime.fromisoformat(inicio_iso)
    fim = inicio + dt.timedelta(minutes=DURACAO_MIN)
    r = pedir("POST", "/calendars/events/appointments", {
        "calendarId": AGENDA, "locationId": LOC, "contactId": contato_id, "assignedUserId": CLOSER,
        "startTime": inicio.isoformat(), "endTime": fim.isoformat(), "title": titulo,
        "appointmentStatus": "confirmed", "toNotify": True})
    return (r or {}).get("id") or ""


def tarefa(contato_id: str, titulo: str, corpo: str, responsavel: str | None = None) -> None:
    pedir("POST", "/contacts/%s/tasks" % contato_id, {
        "title": titulo, "body": corpo[:2000],
        "dueDate": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "completed": False, "assignedTo": responsavel or SDR})


def nota(contato_id: str, corpo: str) -> None:
    pedir("POST", "/contacts/%s/notes" % contato_id, {"body": corpo[:5000]})


def por_extenso(iso: str) -> str:
    dias = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
    t = dt.datetime.fromisoformat(iso).astimezone(BR)
    return "%s, %d/%d, às %dh%s" % (dias[t.weekday()], t.day, t.month, t.hour,
                                     "%02d" % t.minute if t.minute else "")
