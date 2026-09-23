#!/usr/bin/env python3
"""G-17, segunda metade: os dois portoes de capacidade na `Recuperação de No-show`.

Decisao do dono em 23/09/2026 ("siga as suas recomendacoes"): opcao (A) — a
cadencia passa a respeitar `sdr-lotado` e o teto semanal, como a 12x30.
`pausado` ela ja le, dentro de `NS{n} · Ainda vale recuperar?`.

ONDE. So nos toques que esperam antes (NS1 e NS2): entre o ramo Sim de
`NS{n} · Ainda vale recuperar?` e o `Add Tag fila-tel` que vem nele.

    Ainda vale recuperar? --Sim-->  Teto de toques da semana?  ->  SDR lotado?  ->  fila-tel

De proposito FICA SEM portao:
  - o toque imediato (NS-1 + `fila-tel` logo depois do no-show): e a ligacao
    que mais recupera reuniao, e o lead ainda esta quente;
  - o ramo Sim do NS3: nao poe ninguem em fila, so encerra (campo + nutricao).

O `Reengajamento 90 dias` do G-17 NAO EXISTE MAIS na conta: foi substituido em
22/09 pela `Nutrição — WhatsApp a cada 15 dias` (mesmo id `37eb32e4`), 100%
automatica, sem `toque` e sem `fila-tel`. O dump antigo e que enganava a
`auditoria_portoes.py`.

Mesma tecnica e mesmos parametros do `patch_portao_inbound.py` (clona o grupo
de 5 nos da `Cadência 12x30 — parte 2`, uuids remapeados): 2 portoes x 2
toques x 5 nos = 20 nos novos.

Uso:  python patch_portao_noshow.py            # le a conta, so imprime o plano
      python patch_portao_noshow.py --aplicar   # grava, com backup e conferencia
"""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch_portao_inbound as pi              # grupo(), clona(), DOADOR, PORTOES
from patch_funil_reuniao import put, g

ALVO = "Recuperação de No-show"
TOQUES = ["NS1", "NS2"]
BACKUP = os.path.join(pi.DUMPS, "_antes-portao-noshow")


def insere(tpl_alvo, tpl_doador):
    tpl = copy.deepcopy(tpl_alvo)
    grupos = [pi.grupo(tpl_doador, s) for s in pi.PORTOES]
    log = []
    for toque in TOQUES:
        nome = "%s · Ainda vale recuperar?" % toque
        porta = next((t for t in tpl if t.get("name") == nome), None)
        if porta is None:
            log.append("%s: nao achei %r — PULADO" % (toque, nome))
            continue
        sim = next((t for t in tpl if t.get("parentKey") == porta["id"]
                    and not (t.get("attributes") or {}).get("else")), None)
        filhos = [t for t in tpl if sim and t.get("parentKey") == sim["id"]]
        if len(filhos) != 1 or (filhos[0].get("attributes") or {}).get("tags") != ["fila-tel"]:
            log.append("%s: ramo Sim nao comeca por Add Tag fila-tel — PULADO" % toque)
            continue
        depois = filhos[0]
        novos, entra = [], sim["id"]
        base_x = (porta.get("advanceCanvasMeta") or {}).get("position", {}).get("x", 0)
        for j, (g5, none_id) in enumerate(grupos):
            bloco, entra = pi.clona(g5, none_id, "%s · %s" % (toque, pi.PORTOES[j]),
                                    entra, base_x + 1100 * (j + 1))
            novos += bloco
        depois["parent"] = depois["parentKey"] = entra
        pos = max(k for k, t in enumerate(tpl)
                  if t["id"] in {porta["id"], sim["id"]}
                  or t.get("parentKey") == porta["id"]) + 1
        tpl[pos:pos] = novos
        log.append("%s: +%d nos (%s), fila-tel religada ao ultimo portao"
                   % (toque, len(novos), " -> ".join(pi.PORTOES)))
    return tpl, log


def main():
    aplicar = "--aplicar" in sys.argv
    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    doador = c.request("GET", "/workflow/" + g.LOC + "/" + ids[pi.DOADOR])
    alvo = c.request("GET", "/workflow/" + g.LOC + "/" + ids[ALVO])
    td = (doador.get("workflowData") or {}).get("templates") or []
    ta = (alvo.get("workflowData") or {}).get("templates") or []
    print("doador %s: %d nos | alvo %s: %d nos [%s]\n"
          % (pi.DOADOR, len(td), ALVO, len(ta), alvo.get("status")))

    novo, log = insere(ta, td)
    for l in log:
        print("   " + l)
    pi.TOQUES = TOQUES                       # confere() conta por toque
    erros = pi.confere(novo, ta)
    print("\n%d -> %d nos" % (len(ta), len(novo)))
    if erros:
        print("CONFERENCIA FALHOU — nao aplico:")
        for e in erros:
            print("   " + e)
        return 1
    print("conferencia ok: ids unicos, nenhum pai orfao, todo goto aponta para no que")
    print("existe, os dois portoes aparecem %dx cada." % len(TOQUES))
    if not aplicar:
        print("\n(nada foi gravado — rode com --aplicar)")
        return 0

    os.makedirs(BACKUP, exist_ok=True)
    g.export(c, ids[ALVO], os.path.join(BACKUP, ALVO + ".json"))
    put(c, alvo, novo)
    v = c.request("GET", "/workflow/" + g.LOC + "/" + ids[ALVO])
    vt = (v.get("workflowData") or {}).get("templates") or []
    trs = [t.get("active") for t in
           c.request("GET", "/workflow/" + g.LOC + "/trigger?workflowId=" + ids[ALVO])
           if not t.get("deleted")]
    print("gravado: status=%s nos=%d gatilhos=%s" % (v.get("status"), len(vt), trs))
    g.export(c, ids[ALVO], os.path.join(pi.DUMPS, ALVO + ".json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
