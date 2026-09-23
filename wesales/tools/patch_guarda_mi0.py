#!/usr/bin/env python3
"""Trava de etapa antes da MI-0 da `Cadência Inbound` (23/09/2026).

O PROBLEMA, medido ao vivo: a Inbound dispara ao entrar em CONECTAR e manda a
MI-0 (WhatsApp automatico) depois de tres checagens — cad-inbound, telefone,
permissao em branco — e NENHUMA olha a etapa. Fora da janela (seg-sex
08:30-18:30) a execucao fica parada NO NO DA MI-0 e manda assim que a janela
abre. Um lead que entrou em CONECTAR por engano e voltou para NOVO LEAD
(Carlos Andrade, 23/09 19:01) receberia a MI-0 na manha seguinte: voltar de
etapa nao desinscreve.

O CONSERTO: entre o `Update contact field` (permissao = "Nao solicitado") e a
MI-0, um `if_else` "MI-0 · Ainda vale mandar?" com as MESMAS condicoes do
`TI1 · Ainda vale ligar?` (CONECTAR, aberta, sem nao-perturbe, resultado !=
Nao ligar...). Sim -> MI-0 (fluxo de hoje). Nao -> fim.

Clona os 3 nos do `TI1 · Ainda vale ligar?` (if_else + Branch + None) com
uuids novos — atributos iguais ao que o GHL ja aceitou. +3 nos.

Limite honesto: uma execucao JA parada no no da MI-0 nao passa pela trava
nova (por isso o Carlos ficou com DND ate a abertura de 28/09).

Uso:  python patch_guarda_mi0.py [--aplicar]
"""
import copy
import json
import os
import re
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_funil_reuniao import put, g

ALVO = "Cadência Inbound"
DOADOR = "TI1 · Ainda vale ligar?"
NOME = "MI-0 · Ainda vale mandar?"
AQUI = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(AQUI, "..", "workflows-json")
BACKUP = os.path.join(DUMPS, "_antes-guarda-mi0")
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def insere(tpl0):
    tpl = copy.deepcopy(tpl0)
    if any(t.get("name") == NOME for t in tpl):
        return tpl, "ja existe — nada a fazer"
    mi0 = next(t for t in tpl if t.get("name") == "WhatsApp · MI-0")
    pai = next(t for t in tpl if t["id"] == mi0["parentKey"])
    av = next(t for t in tpl if t.get("name") == DOADOR)
    filhos = [t for t in tpl if t.get("parentKey") == av["id"]]
    assert len(filhos) == 2, "doador sem Branch/None"
    grupo = [av] + filhos
    bruto = json.dumps(grupo, ensure_ascii=False)
    ids_grupo = {t["id"] for t in grupo}
    # remapeia so uuids que so existem dentro do grupo (ids, branches[].id,
    # __segmentId, __conditionId). O id da etapa CONECTAR e o `next` do
    # Branch/None aparecem fora do grupo -> ficam como estao.
    fora = json.dumps([t for t in tpl if t["id"] not in ids_grupo], ensure_ascii=False)
    internos = {u for u in set(UUID.findall(bruto)) if u in ids_grupo or u not in fora}
    mapa = {u: str(uuid.uuid4()) for u in internos}
    for v, n in mapa.items():
        bruto = bruto.replace(v, n)
    novo_if, b1, b2 = json.loads(bruto)
    sim, nao = (b1, b2) if not (b1.get("attributes") or {}).get("else") else (b2, b1)
    novo_if["name"] = NOME
    novo_if["parent"] = novo_if["parentKey"] = pai["id"]
    sim["next"] = mi0["id"]
    nao.pop("next", None)
    pai["next"] = novo_if["id"]
    mi0["parent"] = mi0["parentKey"] = sim["id"]
    pos = next(k for k, t in enumerate(tpl) if t["id"] == mi0["id"])
    tpl[pos:pos] = [novo_if, sim, nao]
    return tpl, "+3 nos: %s entre %s e MI-0" % (NOME, pai["id"][:8])


def confere(tpl, antes):
    erros = []
    ids = [t["id"] for t in tpl]
    conhecidos = set(ids)
    if len(ids) != len(conhecidos):
        erros.append("id repetido")
    for t in tpl:
        if t.get("parentKey") and t["parentKey"] not in conhecidos:
            erros.append("%s parentKey orfao" % t["id"][:8])
        nx = t.get("next")
        for n in (nx if isinstance(nx, list) else [nx] if nx else []):
            if n not in conhecidos:
                erros.append("%s (%r) next orfao %s" % (t["id"][:8], t.get("name"), str(n)[:8]))
    if len(tpl) != len(antes) + 3:
        erros.append("%d nos, esperava %d" % (len(tpl), len(antes) + 3))
    return erros


def main():
    aplicar = "--aplicar" in sys.argv
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    cur = c.request("GET", "/workflow/" + g.LOC + "/" + ids[ALVO])
    tpl = (cur.get("workflowData") or {}).get("templates") or []
    novo, msg = insere(tpl)
    print("%s: %d nos [%s]\n   %s" % (ALVO, len(tpl), cur.get("status"), msg))
    if len(novo) == len(tpl):
        return 0
    erros = confere(novo, tpl)
    if erros:
        print("CONFERENCIA FALHOU:", erros)
        return 1
    print("   conferencia ok: ids unicos, parentKey e next sem orfao, %d -> %d" % (len(tpl), len(novo)))
    if not aplicar:
        print("\n(nada foi gravado)")
        return 0
    os.makedirs(BACKUP, exist_ok=True)
    g.export(c, ids[ALVO], os.path.join(BACKUP, ALVO + ".json"))
    r = put(c, cur, novo)
    if r is None or (isinstance(r, dict) and r.get("_error")):
        print("PUT RECUSADO:", r)
        return 1
    v = c.request("GET", "/workflow/" + g.LOC + "/" + ids[ALVO])
    vt = (v.get("workflowData") or {}).get("templates") or []
    print("gravado: status=%s nos=%d trava ao vivo=%d" % (
        v.get("status"), len(vt), sum(1 for t in vt if t.get("name") == NOME)))
    g.export(c, ids[ALVO], os.path.join(DUMPS, ALVO + ".json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
