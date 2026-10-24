"""CRM (HighLevel): contato, oportunidade, tarefa e nota.

A máquina não marca reunião (decisão de 02/10): todo lead interessado vira tarefa da SDR, que liga ou chama
no WhatsApp, confirma dia e horário e marca na agenda "Reunião com closer". Assim o que já existe depois do
agendamento continua valendo sem mudança: pós-agendamento, convite com Meet, lembretes, reunioes_robo.py.

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
import urllib.parse
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
SDR = os.environ.get("COLDMAIL_SDR_ID") or "ML69c5kAJ93cliAGgBj6"
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


def contato(lead: dict, tags: list[str], telefone: str = "") -> str:
    """Cria o contato ou acha o que já existe (por e-mail ou telefone).

    Contato que já existe NÃO é sobrescrito: o `tags` do upsert substitui todas as tags dele, e nome,
    empresa e origem trocariam os do cadastro original (achado no teste de 02/10). Para quem já existe,
    só acrescenta as tags e o telefone, se faltar."""
    existente = _buscar(lead["email"]) or (_buscar(telefone) if telefone else None)
    if existente:
        cid = existente["id"]
        pedir("POST", "/contacts/%s/tags" % cid, {"tags": tags})
        if telefone and not existente.get("phone"):
            pedir("PUT", "/contacts/%s" % cid, {"phone": telefone})
        return cid
    corpo = {"locationId": LOC, "email": lead["email"], "phone": telefone or None,
             "firstName": lead.get("primeiro_nome") or None,
             "companyName": lead.get("empresa") or None, "website": lead.get("site") or None,
             "source": "Cold e-mail", "tags": tags, "assignedTo": SDR}
    r = pedir("POST", "/contacts/upsert", {k: v for k, v in corpo.items() if v})
    return ((r or {}).get("contact") or {}).get("id") or ""


def _buscar(chave: str) -> dict | None:
    """Contato por e-mail ou telefone (+55...), via busca de duplicados do GHL."""
    campo = "email" if "@" in chave else "number"
    r = pedir("GET", "/contacts/search/duplicate?locationId=%s&%s=%s"
              % (LOC, campo, urllib.parse.quote(chave)))
    return (r or {}).get("contact") or None


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
