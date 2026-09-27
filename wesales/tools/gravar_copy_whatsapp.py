#!/usr/bin/env python3
"""Grava no CRM os textos do COPY-WHATSAPP.md e a pontuação G-04 (§12 do ESTADO-27-09).

Só texto e condições; nenhuma espera, trilha ou nó é criado/apagado. Para cada
workflow:
  1. relê ao vivo e confere que o texto antigo de cada nó-alvo é o do backup
     conferido (`.local/bkp-copy-27-09/<chave>.json`) — se mudou, PARA;
  2. troca `body` (WhatsApp) ou `html` (e-mail; assunto não muda), ou acrescenta
     condições OR aos portões do G-04;
  3. grava com `ghl_interno.put` (preserva `status`);
  4. relê e compara nó a nó: só os alvos podem ter mudado, e para o texto novo.

Os textos vêm do próprio COPY-WHATSAPP.md (parse das tabelas), não redigitados.

    python gravar_copy_whatsapp.py --wf inbound --seco   # mostra o que mudaria
    python gravar_copy_whatsapp.py --wf inbound          # grava e relê
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys

import ghl_interno as g

AQUI = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(AQUI, "..", "COPY-WHATSAPP.md")
BKP = os.path.join(AQUI, "..", ".local", "bkp-copy-27-09")

WF = {
    "inbound": "c2375e2f-b4cb-4947-8377-7c1e0529ba82",
    "12x30": "c64a808b-3040-431e-8015-642a265e1022",
    "12x30p2": "17e6dc19-3eca-42e8-83ff-e25a9d5c28e8",
    "fechar": "82dd1fad-1bdd-44f7-8214-3a685521e2b4",
    "triagem": "e7738b57-b047-4fdb-b3cb-06c72f2ca103",
    "nutricao": "37eb32e4-4c21-4c69-bba1-36879ae0886c",
    "noshow": "050052db-5ae8-43fe-8e94-b0f747563d57",
    "cancelada": "37ee2c13-3492-4f80-9471-835f3976fd09",
    "lembretes": "10065adb-aad7-4d12-92df-6941f05d130c",
    "posag": "81815fcc-ff4f-4b72-8a1f-7dbf44ce6911",
}
NOME_DOC = {
    "Cadência Inbound": "inbound", "Cadência 12x30": "12x30",
    "12x30 parte 2": "12x30p2", "Fechar Horário": "fechar", "Nutrição": "nutricao",
    "Recuperação de No-show": "noshow", "Reunião Cancelada": "cancelada",
    "Triagem": "triagem",
}

# G-04 (§12): campo -> valores do Meta acrescentados como OR em cada portão.
INVEST = "bQithNwReQIBGlZBaNlI"   # Investimento mensal em anúncios
URG = "2LnUD4KYSGkIBwiUdzl3"      # Urgência
G04 = {
    "260464f4": [(INVEST, "Abaixo de 5k")],                      # 1k a 5k -> +6
    "a242208e": [(INVEST, "Até R$ 1.000")],                      # Até 1k -> +2
    "43c48e38": [(URG, "Posso esperar e ver oque acontece")],    # Sem prazo -> +2
    "30103ffb": [(INVEST, "Até R$ 1.000"), (INVEST, "Abaixo de 5k"),
                 (INVEST, "Acima de 10k")],                      # Investe=Sim -> +13
    "e69e4ad8": [(INVEST, "Não invisto nada ainda")],            # Investe=Nunca -> +4
}


def textos() -> dict:
    """{chave_wf: {prefixo_no: texto}} lido das duas tabelas do documento."""
    out: dict = {}
    for linha in open(DOC, encoding="utf-8"):
        if not linha.startswith("| ") or "`" not in linha:
            continue
        cols = [c.strip() for c in linha.strip().strip("|").split("|")]
        ids = re.findall(r"`([0-9a-f]{8})`", cols[0])
        if not ids:
            continue
        texto = cols[-1].replace("<br>", "\n")
        if "·" in cols[0] and cols[0].split("·")[0].strip() in NOME_DOC:
            chave = NOME_DOC[cols[0].split("·")[0].strip()]
        else:
            chave = "lembretes"
        for i in ids:
            out.setdefault(chave, {})[i] = texto
    return out


def html_de(texto: str) -> str:
    esc = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return "".join('<p style="margin:0px 0px 12px 0px;">%s</p>' % l
                   for l in esc.split("\n") if l.strip())


def no(templates, prefixo):
    m = [n for n in templates if n["id"].startswith(prefixo)]
    if len(m) != 1:
        raise SystemExit("PAROU: prefixo %s casa %d nós" % (prefixo, len(m)))
    return m[0]


def aplicar(chave: str, t: list) -> dict:
    """Muda `t` no lugar; devolve {id_completo: descrição} dos nós alterados."""
    mudou = {}
    if chave == "posag":
        for p, extra in G04.items():
            n = no(t, p)
            br = n["attributes"]["branches"][0]
            seg = br["segments"][0]
            base = seg["conditions"][0]
            if len(br["segments"]) != 1 or len(seg["conditions"]) != 1:
                raise SystemExit("PAROU: portão %s já não tem 1 condição" % p)
            for campo, valor in extra:
                c = copy.deepcopy(base)
                c["conditionSubType"] = campo
                c["conditionValue"] = valor
                c["__conditionId"] = "g04-%s-%d" % (p, len(seg["conditions"]))
                seg["conditions"].append(c)
            seg["operator"] = "or"
            br["operator"] = "or"
            mudou[n["id"]] = "%s + %s" % (n.get("name"), [v for _, v in extra])
        return mudou
    for p, novo in textos()[chave].items():
        n = no(t, p)
        a = n["attributes"]
        if n["type"] == "sms":
            a["body"] = novo
        elif n["type"] == "email":
            a["html"] = html_de(novo)
        else:
            raise SystemExit("PAROU: nó %s é %s" % (p, n["type"]))
        mudou[n["id"]] = n.get("name")
    return mudou


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wf", required=True, choices=list(WF))
    ap.add_argument("--seco", action="store_true")
    a = ap.parse_args()
    chave, wid = a.wf, WF[a.wf]

    if g.minutos_restantes() < 5:
        raise SystemExit("PAROU: bearer vence em menos de 5 min — renove antes")
    bkp = json.load(open(os.path.join(BKP, chave + ".json"), encoding="utf-8"))["workflow"]
    cur = g.ler(wid)
    t_bkp = bkp["workflowData"]["templates"]
    t = cur["workflowData"]["templates"]
    # 1. nada mudou desde o backup conferido (mesma versão, mesmos nós)
    if cur.get("version") != bkp.get("version") or t != t_bkp:
        raise SystemExit("PAROU: %s mudou desde o backup (v%s -> v%s)"
                         % (cur.get("name"), bkp.get("version"), cur.get("version")))
    if cur.get("status") != "published":
        raise SystemExit("PAROU: %s não está publicado" % cur.get("name"))
    antes = copy.deepcopy(t)
    novo_t = copy.deepcopy(t)
    mudou = aplicar(chave, novo_t)
    print("%s v%s, %d nós, %d a alterar" % (cur["name"], cur["version"], len(t), len(mudou)))
    for i, d in mudou.items():
        print("   ", i[:8], d)
    if a.seco:
        return 0

    g.put(cur, novo_t)
    # 4. releitura
    dep = g.ler(wid)
    td = dep["workflowData"]["templates"]
    erros = []
    if dep.get("status") != "published":
        erros.append("status virou %s" % dep.get("status"))
    if len(td) != len(antes):
        erros.append("nº de nós %d -> %d" % (len(antes), len(td)))
    esperado = {n["id"]: n for n in novo_t}
    for n in td:
        if n != esperado.get(n["id"]):
            erros.append("nó %s difere do gravado" % n["id"][:8])
    for k in ("name", "allowMultiple", "stopOnResponse", "timezone", "window",
              "autoMarkAsRead", "removeContactFromLastStep", "senderAddress"):
        if dep.get(k) != cur.get(k):
            erros.append("campo %s mudou: %r -> %r" % (k, cur.get(k), dep.get(k)))
    print("gravado: v%s -> v%s, status %s, %d nós"
          % (cur["version"], dep.get("version"), dep.get("status"), len(td)))
    if erros:
        print("RELEITURA COM DIFERENÇA:")
        for e in erros:
            print("   ", e)
        return 1
    print("RELEITURA CONFIRMADA: só os %d nós-alvo mudaram, e para o texto novo" % len(mudou))
    return 0


if __name__ == "__main__":
    sys.exit(main())
