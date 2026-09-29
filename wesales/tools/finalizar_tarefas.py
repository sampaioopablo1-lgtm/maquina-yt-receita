#!/usr/bin/env python3
"""Tarefa feita = tarefa fechada, sem a SDR clicar (29/09, pedido do dono).

O log mostrou 40 ligações da SDR e 0 tarefas concluídas: a tarefa ficava aberta depois da
ligação feita. Este robô (relógio, a cada ciclo) fecha a tarefa quando a AÇÃO dela já aconteceu:

  [CADENCIA] ... Ligar / [LIGAR AGORA] Lead novo / [LIGAR AGORA] Retornar ... / [RETORNO]
        -> houve ligação de pessoa para o contato DEPOIS da criação da tarefa (qualquer status:
           a tentativa foi feita; o próximo toque a cadência cria)
  [LIGAR AGORA] Agendou pelo Calendly
        -> ligação de pessoa com 25 s ou mais depois da criação (confirmar exige conversa)
  [COMPLETAR QUALIFICAÇÃO]
        -> Q1 a Q6 preenchidos na ficha
  [FECHAR HORÁRIO] / [NO-SHOW]
        -> reunião marcada (não cancelada) DEPOIS da criação da tarefa
  [RETORNO] Preencher Data e Hora
        -> Data de retorno e Hora do retorno preenchidas (não fecha com ligação)
  [RESPONDER] / [CADENCIA] Sinal: respondeu
        -> alguém respondeu no WhatsApp (CRM ou celular) ou ligou depois da criação. Aberta há 30+ min
           no horário (seg-sáb 08-21): tag `resposta-atrasada` -> workflow avisa o Pablo (1 vez).
  [GRUPO], análises, testes -> nunca (o sistema não enxerga a ação)

Só CONCLUI (nunca apaga). Ligação = mensagem TYPE_CALL de saída com userId (feita por pessoa).

    python3 finalizar_tarefas.py            # DRY
    python3 finalizar_tarefas.py --aplicar
"""
from __future__ import annotations

import re
import sys
from collections import Counter

from atuador_filas import LOC, contatos, pedir, valor

import datetime as dt

CONVERSA_S = 25
BR = dt.timezone(dt.timedelta(hours=-3))
RETORNO = ["IBOMNQecWtIUruHpNAs1", "IHXNFnguTPyNj5Q59ea2"]   # Data de retorno, Hora do retorno
Q = ["qmIKSSDVYNLl5E8vnr3f", "wmod0p91VuukwWDwKCgi", "xjEcIFfdt2h29wBaKMQO",
     "SZVgh0Y5HRcWWZG4fO9V", "3dphGCPCoFcYXEQC2jeB", "lAqbaJE9K4LDkq3t2zzc"]


def regra(titulo: str):
    t = titulo or ""
    if t.startswith("[RESPONDER]") or t.startswith("[CADENCIA] Sinal: respondeu"):
        return "resposta"
    if t.startswith("[RETORNO] Preencher Data e Hora"):
        return "retorno"
    if t.startswith("[LIGAR AGORA]") and "Calendly" in t:
        return "conversa"
    if (t.startswith("[CADENCIA]") and "ligar" in t.lower()) or t.startswith("[LIGAR AGORA]") or t.startswith("[RETORNO]"):
        return "ligacao"
    if t.startswith("[COMPLETAR QUALIFICAÇÃO]"):
        return "qualificacao"
    if t.startswith("[FECHAR HORÁRIO]") or t.startswith("[NO-SHOW]"):
        return "reuniao"
    return None


MSG = {"TYPE_CUSTOM_SMS", "TYPE_WHATSAPP", "TYPE_SMS"}


def historico(cid):
    """(ligações de pessoa [(quando, duração)], mensagens de pessoa [quando]).
    Mensagem de pessoa = saída que não veio de workflow (CRM com userId, ou celular pelo Stevo = "api")."""
    calls, msgs = [], []
    for cv in pedir("GET", "/conversations/search?locationId=%s&contactId=%s" % (LOC, cid)).get("conversations") or []:
        ms = (pedir("GET", "/conversations/%s/messages?limit=100" % cv["id"]).get("messages") or {}).get("messages") or []
        for m in ms:
            if m.get("direction") != "outbound":
                continue
            if m.get("messageType") == "TYPE_CALL" and m.get("userId"):
                calls.append((m.get("dateAdded") or "", ((m.get("meta") or {}).get("call") or {}).get("duration") or 0))
            elif m.get("messageType") in MSG and m.get("source") != "workflow" and (m.get("userId") or m.get("source") == "api"):
                msgs.append(m.get("dateAdded") or "")
    return calls, msgs


def decidir(t, c, calls, msgs=()) -> str | None:
    """Pura: motivo para fechar a tarefa, ou None."""
    r = regra(t.get("title"))
    criada = t.get("dateAdded") or ""
    if r == "resposta":
        feitas = sorted([x[0] for x in calls if x[0] > criada] + [m for m in msgs if m > criada])
        return "respondeu/ligou %s" % feitas[0][11:16] if feitas else None
    if r == "ligacao":
        feitas = [x for x in calls if x[0] > criada]
        return "ligou %s" % feitas[0][0][11:16] if feitas else None
    if r == "conversa":
        feitas = [x for x in calls if x[0] > criada and x[1] >= CONVERSA_S]
        return "conversou %ss" % feitas[0][1] if feitas else None
    if r == "qualificacao":
        return "Q1-Q6 preenchidos" if all(str(valor(c, q) or "").strip() for q in Q) else None
    if r == "retorno":
        return "data e hora do retorno preenchidas" if all(str(valor(c, f) or "").strip() for f in RETORNO) else None
    if r == "reuniao":
        # reunião marcada DEPOIS da tarefa (a agenda devolve hora local de São Paulo, sem fuso)
        for ap in reunioes(c["id"]):
            criada_ap = dt.datetime.strptime(ap["dateAdded"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=BR)
            if criada_ap > quando(criada) and str(ap.get("appointmentStatus")) not in ("cancelled", "invalid", "noshow"):
                return "reunião marcada %s" % str(ap.get("startTime", ""))[:16]
    return None


def atrasada(t, tags, agora) -> bool:
    """Pura: tarefa de resposta aberta há 30+ min, no horário (seg-sáb 08-21, São Paulo), sem aviso ainda."""
    if regra(t.get("title")) != "resposta" or tags & {"resposta-atrasada", "resposta-atrasada-avisada"}:
        return False
    local = agora.astimezone(BR)
    if local.weekday() == 6 or not 8 <= local.hour < 21:
        return False
    return agora - quando(t.get("dateAdded") or agora.isoformat()) >= dt.timedelta(minutes=30)


def reunioes(cid) -> list:
    return pedir("GET", "/contacts/%s/appointments" % cid).get("events") or []


def quando(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    agora = dt.datetime.now(dt.timezone.utc)
    cont = Counter()
    for c in contatos():
        tarefas = [t for t in (pedir("GET", "/contacts/%s/tasks" % c["id"]).get("tasks") or [])
                   if not t.get("completed") and regra(t.get("title"))]
        if not tarefas:
            continue
        calls, msgs = historico(c["id"]) if any(regra(t["title"]) != "qualificacao" for t in tarefas) else ([], [])
        tags = set(c.get("tags") or [])
        for t in tarefas:
            motivo = decidir(t, c, calls, msgs)
            if not motivo:
                if atrasada(t, tags, agora):
                    cont["avisar atraso"] += 1
                    print("  %-22s %-55s <- ATRASADA, avisar o Pablo" % ((c.get("firstNameLowerCase") or "?")[:22], t["title"][:55]))
                    if aplicar:
                        pedir("POST", "/contacts/%s/tags" % c["id"], {"tags": ["resposta-atrasada"]})
                    tags.add("resposta-atrasada")
                continue
            if regra(t["title"]) == "resposta" and "resposta-atrasada-avisada" in tags and aplicar:
                pedir("DELETE", "/contacts/%s/tags" % c["id"], {"tags": ["resposta-atrasada-avisada"]})
            cont[regra(t["title"])] += 1
            print("  %-22s %-55s <- %s" % ((c.get("firstNameLowerCase") or "?")[:22], t["title"][:55], motivo))
            if aplicar:
                pedir("PUT", "/contacts/%s/tasks/%s/completed" % (c["id"], t["id"]), {"completed": True})
    print("tarefas finalizadas%s: %s" % ("" if aplicar else " (DRY)", dict(cont) or "nenhuma"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
