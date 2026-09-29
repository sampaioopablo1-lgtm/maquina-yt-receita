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

CONVERSA_S = 25
Q = ["qmIKSSDVYNLl5E8vnr3f", "wmod0p91VuukwWDwKCgi", "xjEcIFfdt2h29wBaKMQO",
     "SZVgh0Y5HRcWWZG4fO9V", "3dphGCPCoFcYXEQC2jeB", "lAqbaJE9K4LDkq3t2zzc"]


def regra(titulo: str):
    t = titulo or ""
    if t.startswith("[LIGAR AGORA]") and "Calendly" in t:
        return "conversa"
    if (t.startswith("[CADENCIA]") and "Ligar" in t) or t.startswith("[LIGAR AGORA]") or t.startswith("[RETORNO]"):
        return "ligacao"
    if t.startswith("[COMPLETAR QUALIFICAÇÃO]"):
        return "qualificacao"
    return None


def ligacoes(cid) -> list:
    out = []
    for cv in pedir("GET", "/conversations/search?locationId=%s&contactId=%s" % (LOC, cid)).get("conversations") or []:
        ms = (pedir("GET", "/conversations/%s/messages?limit=100" % cv["id"]).get("messages") or {}).get("messages") or []
        for m in ms:
            if m.get("messageType") == "TYPE_CALL" and m.get("direction") == "outbound" and m.get("userId"):
                out.append((m.get("dateAdded") or "", ((m.get("meta") or {}).get("call") or {}).get("duration") or 0))
    return out


def decidir(t, c, calls) -> str | None:
    """Pura: motivo para fechar a tarefa, ou None."""
    r = regra(t.get("title"))
    criada = t.get("dateAdded") or ""
    if r == "ligacao":
        feitas = [x for x in calls if x[0] > criada]
        return "ligou %s" % feitas[0][0][11:16] if feitas else None
    if r == "conversa":
        feitas = [x for x in calls if x[0] > criada and x[1] >= CONVERSA_S]
        return "conversou %ss" % feitas[0][1] if feitas else None
    if r == "qualificacao":
        return "Q1-Q6 preenchidos" if all(str(valor(c, q) or "").strip() for q in Q) else None
    return None


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    cont = Counter()
    for c in contatos():
        tarefas = [t for t in (pedir("GET", "/contacts/%s/tasks" % c["id"]).get("tasks") or [])
                   if not t.get("completed") and regra(t.get("title"))]
        if not tarefas:
            continue
        calls = ligacoes(c["id"]) if any(regra(t["title"]) != "qualificacao" for t in tarefas) else []
        for t in tarefas:
            motivo = decidir(t, c, calls)
            if not motivo:
                continue
            cont[regra(t["title"])] += 1
            print("  %-22s %-55s <- %s" % ((c.get("firstNameLowerCase") or "?")[:22], t["title"][:55], motivo))
            if aplicar:
                pedir("PUT", "/contacts/%s/tasks/%s/completed" % (c["id"], t["id"]), {"completed": True})
    print("tarefas finalizadas%s: %s" % ("" if aplicar else " (DRY)", dict(cont) or "nenhuma"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
