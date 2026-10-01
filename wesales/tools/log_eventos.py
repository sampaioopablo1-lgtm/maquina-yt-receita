#!/usr/bin/env python3
"""Log de eventos do CRM — tudo o que acontece, automático ou manual (29/09, pedido do dono).

Fonte: o log de auditoria do próprio CRM (Configurações → Registros de auditoria), lido em
`services.leadconnectorhq.com/audit/search/v2`. Ele registra contato, tag, campo, nota,
tarefa, oportunidade, agenda e lista, com antes/depois e a ORIGEM de cada mudança:

    WEB_USER / MOBILE_APP  pessoa (sourceName = quem)     -> origem "pessoa"
    WORKFLOW_NEW           workflow (sourceId = id)        -> origem "workflow"
    INTEGRATION            nossos robôs (token de API)     -> origem "robo"
    FORM, CALENDAR, ...    o próprio CRM                   -> origem "sistema"

O CRM guarda só ~60 dias; este arquivo copia para `wesales/dados/eventos/AAAA-MM-DD.jsonl.gz`
(uma linha por evento, compacta, deduplicada pelo id do evento), que fica para sempre.
Guarda só em arquivo: na nuvem o `wesales-log.yml` grava no repositório PRIVADO `opc-crm-dados` (01/10, regra do
dono: rotina do CRM não usa Supabase; o envio para `opc.crm_eventos` foi retirado).

Limite: o log de auditoria só aceita token de SESSÃO (o PIT responde 401 "not authorized for
this scope"). Na nuvem precisa do segredo GHL_STORAGE_STATE + renovar_bearer.js.

    python log_eventos.py --dias 2          # coleta ontem e hoje
    python log_eventos.py --dias 60         # tudo o que o CRM ainda guarda
    python log_eventos.py --resumo 7        # contagem dos últimos 7 dias gravados
"""
from __future__ import annotations

import datetime as dt
import gzip
import json
import os
import sys
import urllib.parse
import urllib.request
from collections import Counter

import ghl_interno as g

# Na nuvem (wesales-log.yml) aponta para o clone do repositório PRIVADO opc-crm-dados: este repo é
# público e nunca recebe dado de lead.
DIR = os.environ.get("EVENTOS_DIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".local", "eventos")
BR = dt.timezone(dt.timedelta(hours=-3))
PESSOA = {"WEB_USER", "MOBILE_APP", "MOBILE_USER", "USER"}
DO_CONTATO = {"CONTACT", "NOTE", "TASK", "OPPORTUNITY", "CALENDAR_EVENT", "APPOINTMENT"}


def origem(src: str) -> str:
    if src in PESSOA:
        return "pessoa"
    if src == "WORKFLOW_NEW":
        return "workflow"
    if src in ("INTEGRATION", "PUBLIC_API"):
        return "robo"
    return "sistema"


def curto(v, n=200):
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + "…"


def resumo_lado(lado) -> dict:
    """Antes/depois compactos: campos pelo nome, tags, etapa, texto cortado."""
    if not isinstance(lado, dict):
        return {}
    out = {}
    for k, v in lado.items():
        if k == "customFields" and isinstance(v, list):
            for f in v:
                out[f.get("fieldName") or f.get("id")] = curto(f.get("fieldValue"), 120)
        elif k in ("body", "title", "name", "status", "pipelineStageId", "assignedTo", "completed",
                   "tagsAdded", "tagsRemoved", "tags", "dnd", "monetaryValue", "startTime", "appointmentStatus"):
            out[k] = curto(v, 200)
    return out


def normalizar(x: dict) -> dict:
    meta_cb = (((x.get("meta") or {}).get("after") or {}).get("createdBy") or {})
    src = x.get("source") or ""
    if src == "UNKNOWN_SOURCE" and meta_cb.get("source"):
        src = meta_cb["source"]
    return {
        "id": x.get("_id"),
        "ts": x.get("createdAt"),
        "doc": x.get("documentType"),
        "tipo": x.get("type"),
        "doc_id": x.get("id"),
        "contato": x.get("secondaryId") if x.get("documentType") in DO_CONTATO else None,
        "nome": (x.get("documentName") or "").strip()[:60],
        "origem": origem(src),
        "fonte": src,
        "quem": x.get("sourceName") if x.get("sourceName") not in (None, "UNKNOWN") else x.get("sourceId"),
        "campos": x.get("changedFields") or [],
        "antes": resumo_lado(x.get("before")),
        "depois": resumo_lado(x.get("after")),
    }


def buscar(ini: str, fim: str) -> list:
    """Todos os eventos entre ini e fim (ISO UTC), paginando pelo cursor do CRM."""
    cab = {"authorization": "Bearer " + g.bearer(), "version": "2021-07-28", "channel": "APP",
           "source": "WEB_USER", "accept": "application/json", "user-agent": "Mozilla/5.0"}
    todos, vistos, cur, pag = [], set(), None, 1
    while pag <= 500:
        q = {"page": pag, "pageSize": 100, "startAt": ini, "endAt": fim, "locationId": g.LOC}
        if cur:
            q["cursorToken"] = cur
        req = urllib.request.Request("https://services.leadconnectorhq.com/audit/search/v2?"
                                     + urllib.parse.urlencode(q), headers=cab)
        r = json.load(urllib.request.urlopen(req, timeout=90))
        novos = [x for x in r.get("logs") or [] if x.get("_id") not in vistos]
        vistos.update(x["_id"] for x in novos)
        todos += novos
        p = r.get("pagination") or {}
        if not p.get("hasMore") or not novos:
            break
        cur, pag = p.get("cursorToken"), pag + 1
    return todos


CANAL_MSG = {"TYPE_CALL": "LIGACAO", "TYPE_CUSTOM_SMS": "WHATSAPP", "TYPE_WHATSAPP": "WHATSAPP",
             "TYPE_SMS": "SMS", "TYPE_EMAIL": "EMAIL", "TYPE_CUSTOM_CALL": "LIGACAO"}


def conversas(desde: dt.datetime) -> list:
    """Ligações e mensagens (fora do log de auditoria), com o token de API: quem ligou, quanto durou."""
    from atuador_filas import contatos, pedir
    try:
        nomes = {u["id"]: u.get("name") or u.get("firstName")
                 for u in pedir("GET", "/users/?locationId=%s" % g.LOC).get("users", [])}
    except Exception:
        nomes = {}
    out = []
    for c in contatos():
        for cv in pedir("GET", "/conversations/search?locationId=%s&contactId=%s" % (g.LOC, c["id"])).get("conversations") or []:
            if (cv.get("lastMessageDate") or 0) and dt.datetime.fromtimestamp(cv["lastMessageDate"] / 1000, dt.timezone.utc) < desde:
                continue
            ms = (pedir("GET", "/conversations/%s/messages?limit=100" % cv["id"]).get("messages") or {}).get("messages") or []
            for x in ms:
                canal = CANAL_MSG.get(x.get("messageType"))
                if not canal or (x.get("dateAdded") or "") < desde.strftime("%Y-%m-%dT%H:%M:%S"):
                    continue
                src = x.get("source") or ""
                # Stevo (WhatsApp pelo QR) sincroniza o celular pela API: "api" + saída = alguém
                # digitou no celular, não robô. Entrada é sempre o lead.
                orig = "lead" if x.get("direction") == "inbound" else "workflow" if src == "workflow" else "pessoa"
                quem = nomes.get(x.get("userId"), x.get("userId")) if src != "api" else "celular (WhatsApp)"
                call = (x.get("meta") or {}).get("call") or {}
                out.append({
                    "id": x["id"], "ts": x.get("dateAdded"), "doc": canal, "tipo": x.get("direction"),
                    "doc_id": x.get("conversationId"), "contato": c["id"],
                    "nome": (c.get("firstNameLowerCase") or "")[:60], "origem": orig, "fonte": src,
                    "quem": quem if orig == "pessoa" else None,
                    "campos": [], "antes": {},
                    # sem o texto da mensagem (privacidade: o Stevo traz conversas pessoais do celular)
                    "depois": {k: v for k, v in {"status": x.get("status") or call.get("status"),
                                                 "duracao_s": call.get("duration"),
                                                 "tamanho": len(x.get("body") or "")}.items() if v not in (None, "")},
                })
    return out


def arquivo(dia: dt.date) -> str:
    return os.path.join(DIR, dia.isoformat() + ".jsonl.gz")


def ler_dia(dia: dt.date) -> list:
    if not os.path.exists(arquivo(dia)):
        return []
    with gzip.open(arquivo(dia), "rt", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def gravar_dia(dia: dt.date, novos: list) -> tuple:
    ant = {e["id"]: e for e in ler_dia(dia)}
    n0 = len(ant)
    for e in novos:
        ant[e["id"]] = e
    linhas = sorted(ant.values(), key=lambda e: e["ts"] or "")
    os.makedirs(DIR, exist_ok=True)
    with gzip.open(arquivo(dia), "wt", encoding="utf-8") as f:
        for e in linhas:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")) + "\n")
    return n0, len(linhas)


def dia_br(ts: str) -> dt.date:
    return dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(BR).date()


def coletar(dias: int) -> None:
    hoje = dt.datetime.now(BR).date()
    desde = dt.datetime.combine(hoje - dt.timedelta(days=dias - 1), dt.time(0, 0), BR).astimezone(dt.timezone.utc)
    por_dia = {}
    sem_sessao = False
    try:
        for k in range(dias - 1, -1, -1):
            dia = hoje - dt.timedelta(days=k)
            ini = dt.datetime.combine(dia, dt.time(0, 0), BR).astimezone(dt.timezone.utc)
            fim = ini + dt.timedelta(days=1) - dt.timedelta(milliseconds=1)
            f = lambda t: t.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (t.microsecond // 1000)
            por_dia.setdefault(dia, []).extend(normalizar(x) for x in buscar(f(ini), f(fim)))
    except g.SemBearer as e:
        sem_sessao = True
        print("auditoria pulada (sem token de sessão): %s" % e)
    for e in conversas(desde):
        por_dia.setdefault(dia_br(e["ts"]), []).append(e)
    for dia in sorted(por_dia):
        antes, depois = gravar_dia(dia, por_dia[dia])
        print("%s: %d eventos coletados, arquivo %d -> %d" % (dia, len(por_dia[dia]), antes, depois))
    if sem_sessao:
        print("AVISO: só ligações/mensagens; o log de auditoria precisa do segredo GHL_STORAGE_STATE")


def resumo(dias: int) -> None:
    hoje = dt.datetime.now(BR).date()
    for k in range(dias - 1, -1, -1):
        dia = hoje - dt.timedelta(days=k)
        es = ler_dia(dia)
        if not es:
            continue
        o = Counter(e["origem"] for e in es)
        p = Counter(e["quem"] for e in es if e["origem"] == "pessoa")
        print("%s  %4d eventos | %s | pessoas: %s" % (dia, len(es), dict(o), dict(p.most_common(4))))


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--resumo" in a:
        resumo(int(a[a.index("--resumo") + 1]))
    else:
        coletar(int(a[a.index("--dias") + 1]) if "--dias" in a else 2)
