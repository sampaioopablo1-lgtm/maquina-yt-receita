#!/usr/bin/env python3
"""Mantem as filas do discador — `fila-sdr` e `fila-closer` — sozinhas.

O PROBLEMA
----------
O Call Center do WeSales puxa por pipeline+estagio ou por TAG, e entrega lista
plana. Puxar por pipeline arrastaria os 42 protegidos que tem telefone (medido em
27/09), porque o discador nao le `Prioridade` nem DND. Entao a tag e o unico jeito
seguro de alimentar o discador — e tag so serve se alguem a mantiver.

Este arquivo e esse alguem.

    entra em fila-sdr    : etapa CONECTAR, Prioridade >= 3, sem DND,
                           sem `nao-perturbe`, com telefone
    entra em fila-closer : etapa REUNIAO DE DIAGNOSTICO ou NEGOCIAR,
                           sem DND, com telefone
    sai das duas         : deixou de satisfazer a regra

**Remover importa tanto quanto por.** Tag que fica e lead discado sem motivo, e
aqui o discador liga de verdade — nao e lista para olhar.

POR QUE ISTO NAO MEXE EM `sdr-lotado` NEM EM `fila-wa`
------------------------------------------------------
As duas estao na lista de "portao que le o que ninguem escreve", e eu ia inclui-
las. Fui ler os dumps dos workflows publicados antes, e os dois casos sao piores
do que eu estimava:

**`sdr-lotado`** e lido como `conditionType: contact_detail`,
`conditionSubType: tags`, `conditionOperator: index-of-true` — em 15 portoes das
`Cadencia 12x30`, `12x30 parte 2` e `Inbound`. E tag **por contato**. Entao o
freio de capacidade exigiria marcar e desmarcar ~47 leads pagos a cada ciclo do
cron. Churn de tag em massa sobre lead pago, por um freio que hoje nao dói (5
leads), e risco sem retorno. Fica especificado, nao implementado.

**`fila-wa`** e **removida** pelas cadencias publicadas em dezenas de nos
`remove_contact_tag`. Um atuador que a aplicasse em cron brigaria com o workflow:
o cron poe, o proximo toque tira, e a tag pisca. Se um portao le a tag, o
comportamento passa a depender de quem escreveu por ultimo. Antes de aplicar
`fila-wa` e preciso ler o portao que a LE e decidir de quem e a autoridade — e
isso nao se faz no escuro.

`fila-sdr` e `fila-closer` nao tem esse problema: **nenhum workflow as toca.** Fui
eu que as criei em 27/09, justamente para ficarem fora do caminho da maquina.

NUNCA APAGA LEAD
----------------
Este arquivo usa `DELETE /contacts/{id}/tags`, que remove a **associacao de tag**,
nunca o contato. A regra 1 do projeto proibe excluir lead, contato e oportunidade,
e nada aqui chega perto disso: nao existe chamada a `DELETE /contacts/{id}`.
Remover a tag da fila e requisito de corretude — sem isso o SDR disca quem nao
deveria.

USO
---
    python3 atuador_filas.py            # DRY: calcula e imprime, escreve nada
    python3 atuador_filas.py --aplicar  # escreve as diferencas
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://services.leadconnectorhq.com"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/131.0.0.0 Safari/537.36")
LOC = "1D53YTI9C7oIMBavcQxV"
VERSION = "2021-07-28"
PIPELINE = "0Fo2xbeayE4EP6yuSUtq"

CONECTAR = "deb60542"
DO_CLOSER = ("3d26fcd1", "cbcf0229")   # REUNIAO DE DIAGNOSTICO, NEGOCIAR

PRIORIDADE = "chuJMRlKzY0Uq1f0lSkX"
TAG_SDR = "fila-sdr"
TAG_CLOSER = "fila-closer"

# Contato de teste nao entra em fila de discagem. E heuristica de nome, e por isso
# o script IMPRIME quem excluiu por este motivo em toda execucao: heuristica que
# ninguem ve e heuristica que erra calada.
TESTE = re.compile(r"(^|\b)(zz|teste|test lead|dummy)\b", re.I)


def token() -> str:
    t = (os.environ.get("GHL_PIT") or "").strip()
    if not t:
        raise SystemExit("sem GHL_PIT no ambiente — este script roda na Action.")
    return t


def pedir(metodo: str, caminho: str, corpo: dict | None = None):
    dados = None if corpo is None else json.dumps(corpo).encode("utf-8")
    req = urllib.request.Request(BASE + caminho, data=dados, method=metodo)
    req.add_header("Authorization", "Bearer " + token())
    req.add_header("Version", VERSION)
    req.add_header("Accept", "application/json")
    # Sem User-Agent de navegador a API devolve 403 Cloudflare 1010
    # "browser_signature_banned". Medido em 27/09 — nao e escopo de token.
    req.add_header("User-Agent", UA)
    if dados is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            corpo_resp = r.read().decode("utf-8")
            return json.loads(corpo_resp) if corpo_resp else {}
    except urllib.error.HTTPError as e:
        detalhe = ""
        try:
            detalhe = e.read().decode("utf-8")[:300]
        except Exception:
            pass
        raise SystemExit("%s %s -> HTTP %s %s" % (metodo, caminho, e.code, detalhe))
    except urllib.error.URLError as e:
        raise SystemExit("%s %s -> rede recusou: %s" % (metodo, caminho, e.reason))


def etapa_por_contato() -> dict:
    """contactId -> prefixo do estagio, para as oportunidades ABERTAS do funil."""
    mapa, pagina = {}, None
    while True:
        q = {"location_id": LOC, "pipeline_id": PIPELINE,
             "status": "open", "limit": "100"}
        if pagina:
            q["page"] = str(pagina)
        r = pedir("GET", "/opportunities/search?" + urllib.parse.urlencode(q))
        lote = r.get("opportunities") or []
        for o in lote:
            cid = o.get("contactId") or (o.get("contact") or {}).get("id")
            if cid:
                mapa[cid] = (o.get("pipelineStageId") or "")[:8]
        prox = (r.get("meta") or {}).get("nextPage")
        if not prox or not lote:
            break
        pagina = prox
    return mapa


def contatos() -> list:
    todos, depois = [], None
    while True:
        corpo = {"locationId": LOC, "pageLimit": 100}
        if depois:
            corpo["searchAfter"] = depois
        r = pedir("POST", "/contacts/search", corpo)
        lote = r.get("contacts") or []
        todos += lote
        total = r.get("total") or 0
        if not lote or len(todos) >= total:
            break
        depois = lote[-1].get("searchAfter")
        if not depois:
            break
    return todos


def valor(c, campo_id):
    for cf in (c.get("customFields") or []):
        if cf.get("id") == campo_id:
            return cf.get("value")
    return None


def decidir(cs, etapas):
    """Devolve (desejado_sdr, desejado_closer, atual_sdr, atual_closer, excluidos)."""
    d_sdr, d_clo, a_sdr, a_clo, excl = set(), set(), set(), set(), []
    for c in cs:
        cid = c["id"]
        tags = set(c.get("tags") or [])
        if TAG_SDR in tags:
            a_sdr.add(cid)
        if TAG_CLOSER in tags:
            a_clo.add(cid)

        nome = c.get("contactName") or ""
        if TESTE.search(nome):
            excl.append((cid, nome, "nome de teste"))
            continue
        if not c.get("phone"):
            continue
        if c.get("dnd"):
            continue

        etapa = etapas.get(cid)
        if etapa == CONECTAR and "nao-perturbe" not in tags:
            try:
                p = float(valor(c, PRIORIDADE) or 0)
            except (TypeError, ValueError):
                p = 0
            if p >= 3:
                d_sdr.add(cid)
        elif etapa in DO_CLOSER:
            d_clo.add(cid)
    return d_sdr, d_clo, a_sdr, a_clo, excl


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    print("=" * 74)
    print("ATUADOR DAS FILAS DO DISCADOR — %s"
          % ("APLICANDO" if aplicar else "DRY (escreve nada)"))
    print("=" * 74)

    etapas = etapa_por_contato()
    cs = contatos()
    print("  oportunidades abertas mapeadas: %d | contatos lidos: %d"
          % (len(etapas), len(cs)))

    d_sdr, d_clo, a_sdr, a_clo, excl = decidir(cs, etapas)
    nome = {c["id"]: (c.get("contactName") or "?") for c in cs}

    if excl:
        print("\n  excluidos por heuristica de nome de teste (%d):" % len(excl))
        for cid, n, _ in excl:
            print("     %s  %s" % (cid, n))

    plano = []
    for tag, desejado, atual in ((TAG_SDR, d_sdr, a_sdr),
                                 (TAG_CLOSER, d_clo, a_clo)):
        por = sorted(desejado - atual)
        tirar = sorted(atual - desejado)
        print("\n  %s: %d desejados, %d com a tag hoje" % (tag, len(desejado), len(atual)))
        for cid in por:
            print("     + %s  %s" % (cid, nome.get(cid, "?")))
            plano.append(("POST", cid, tag))
        for cid in tirar:
            print("     - %s  %s" % (cid, nome.get(cid, "?")))
            plano.append(("DELETE", cid, tag))
        if not por and not tirar:
            print("     (nada a mudar)")

    print("\n  total de escritas: %d" % len(plano))
    if not aplicar:
        print("  DRY: nada foi escrito. Rode com --aplicar para executar.")
        return 0

    for metodo, cid, tag in plano:
        pedir(metodo, "/contacts/%s/tags" % cid, {"tags": [tag]})
        print("  %s %s %s -> ok" % (metodo, tag, cid))

    # Rele a conta: a resposta da escrita nao e o estado (licao 2.15). A busca do GHL
    # indexa a tag com atraso (27/09: releitura imediata viu 24 de 36; minutos depois,
    # 36 de 36) — por isso espera e tenta de novo antes de declarar que nao convergiu.
    import time
    print("\n  conferindo relendo a conta...")
    for espera in (0, 30, 60):
        time.sleep(espera)
        cs2 = contatos()
        d2_sdr, d2_clo, a2_sdr, a2_clo, _ = decidir(cs2, etapa_por_contato())
        ok = (d2_sdr == a2_sdr) and (d2_clo == a2_clo)
        if ok:
            break
    print("  fila-sdr    desejado=%d atual=%d" % (len(d2_sdr), len(a2_sdr)))
    print("  fila-closer desejado=%d atual=%d" % (len(d2_clo), len(a2_clo)))
    print("  veredito: %s" % ("CONVERGIU" if ok else "NAO convergiu"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
