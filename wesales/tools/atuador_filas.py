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
# 28/09: lista "Minha agenda — Closer" filtra por esta tag (a tela não aceita OU de etapas).
# = oportunidade aberta em REUNIÃO DE DIAGNÓSTICO, NEGOCIAR ou FORMALIZAR (com ou sem telefone).
TAG_CLOSER_ATIVO = "closer-ativo"
# 28/09 (PENDENTES-CRM item 1/2): `fila-wa` alimenta a visão "Ligar pelo WhatsApp" em Conversas
# (botão de ligar do WhatsApp lá dentro). Nenhum workflow publicado põe a tag (só tiram), então
# o atuador põe: CONECTAR, com telefone, sem DND/nao-perturbe/falou-hoje/wa-feito-hoje, ao menos
# 1 tentativa por telefone e nenhuma conexão. `wa-feito-hoje` (workflow "WhatsApp tentado hoje",
# 12 h) garante 1 ligação de WhatsApp por lead por dia. Cadências e Pós-ligação tiram a tag a cada
# toque; o atuador põe de novo na rodada seguinte se o lead continuar elegível.
TAG_WA = "fila-wa"
FORMALIZAR = "b8485ec0"
# Trava de canal (28/09): quem falou com a SDR nas ultimas 12 h (atendeu o discador ou
# Resultado = Atendeu/Pediu retorno) nao entra na fila do discador nem na lista "Ligar pelo
# WhatsApp". A tag e posta e tirada pelo workflow "Trava de canal — falou hoje"; este arquivo
# so a le e, como rede de seguranca, poe no workflow quem atendeu o discador e ficou sem ela.
TAG_FALOU = "falou-hoje"
WF_TRAVA = "c4a3aab7-5fb2-4d05-80cf-0364a0a90bc5"
TENT_TEL = "wCzdqF7uLQwtrZ1JyZRn"
CONEX_TEL = "LB11ao0AdSI1QSHyZBOP"

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
        if etapa == CONECTAR and "nao-perturbe" not in tags and TAG_FALOU not in tags:
            try:
                p = float(valor(c, PRIORIDADE) or 0)
            except (TypeError, ValueError):
                p = 0
            # 28/09: fila-sdr aposentada (dono): a SDR puxa só fila-tel. O conjunto desejado
            # fica vazio, então o atuador tira a tag de quem ainda a tem.
            pass
        elif etapa in DO_CLOSER:
            d_clo.add(cid)
    return d_sdr, d_clo, a_sdr, a_clo, excl


def atendeu_recente(cid, horas=12):
    """Ligacao de saida completada com 20 s ou mais nas ultimas `horas` (mesma regra das
    analises semanais)."""
    import datetime as dt
    limite = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=horas)
    r = pedir("GET", "/conversations/search?locationId=%s&contactId=%s" % (LOC, cid))
    for cv in r.get("conversations") or []:
        m = pedir("GET", "/conversations/%s/messages?limit=30" % cv["id"])
        for x in ((m.get("messages") or {}).get("messages") or []):
            if x.get("messageType") != "TYPE_CALL" or x.get("direction") != "outbound":
                continue
            quando = dt.datetime.fromisoformat(x["dateAdded"].replace("Z", "+00:00"))
            call = (x.get("meta") or {}).get("call") or {}
            if quando >= limite and call.get("status") == "completed" and (call.get("duration") or 0) >= 20:
                return True
    return False


def rede_trava(cs, etapas, aplicar):
    """Candidatos da lista "Ligar pelo WhatsApp" (CONECTAR, 2+ tentativas por telefone, nenhuma
    conexao registrada) que atenderam o discador e ainda nao tem `falou-hoje`: entram no
    workflow da trava. Cobre o caso de o gatilho nativo da ligacao nao disparar."""
    n = 0
    for c in cs:
        tags = set(c.get("tags") or [])
        if TAG_FALOU in tags or etapas.get(c["id"]) != CONECTAR or not c.get("phone"):
            continue
        try:
            tent = float(valor(c, TENT_TEL) or 0); con = float(valor(c, CONEX_TEL) or 0)
        except (TypeError, ValueError):
            continue
        if tent < 1 or con > 0:
            continue
        if atendeu_recente(c["id"]):
            n += 1
            print("  trava: %s %s atendeu o discador sem trava%s" % (
                c["id"], c.get("contactName") or "?", "" if aplicar else " (DRY)"))
            if aplicar:
                pedir("POST", "/contacts/%s/workflow/%s" % (c["id"], WF_TRAVA), {})
    print("  rede da trava de canal: %d contato(s)" % n)


def dono_por_turno(cs, etapas, aplicar):
    """Turnos flexíveis (dono, 28/09): lead em CONECTAR que ninguém tentou ainda, cujo dono é
    uma SDR fora do turno, passa para uma SDR em turno (a com menos leads novos), levando as
    tarefas abertas. Assim o lead das 09:00 não espera a SDR das 13:00. Turnos em
    `wesales/equipe.json`; com uma SDR só cadastrada, não faz nada."""
    import datetime as dt
    try:
        from turnos import em_turno, ids
    except Exception as e:
        print("  turnos: equipe.json indisponível (%s)" % e)
        return
    sdrs, agora_turno = set(ids("sdrs")), em_turno(dt.datetime.now(dt.timezone.utc))
    if len(sdrs) < 2 or not agora_turno:
        print("  turnos: %d SDR(s) cadastrada(s), %d em turno agora: nada a redistribuir"
              % (len(sdrs), len(agora_turno)))
        return
    carga = {u: 0 for u in agora_turno}
    novos = []
    limite = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=24)
    for c in cs:
        if etapas.get(c["id"]) != CONECTAR or c.get("assignedTo") not in sdrs:
            continue
        # só lead que ENTROU nas últimas 24 h: os antigos têm contador vazio (os contadores
        # nasceram em 27/09) e não podem ser redistribuídos em massa.
        try:
            entrou = dt.datetime.fromisoformat((c.get("dateAdded") or "").replace("Z", "+00:00"))
        except ValueError:
            continue
        if entrou < limite:
            continue
        try:
            tent = float(valor(c, TENT_TEL) or 0) + float(valor(c, "5j9SerJeZ6ngfZCPb2Wg") or 0)
        except (TypeError, ValueError):
            tent = 1
        if tent:
            continue
        if c["assignedTo"] in carga:
            carga[c["assignedTo"]] += 1
        else:
            novos.append(c)
    for c in novos:
        para = min(carga, key=carga.get)
        carga[para] += 1
        de = c["assignedTo"]
        print("  turno: %s %s  %s -> %s%s" % (c["id"], c.get("contactName") or "?", de, para,
                                             "" if aplicar else " (DRY)"))
        if not aplicar:
            continue
        pedir("PUT", "/contacts/%s" % c["id"], {"assignedTo": para})
        for t in (pedir("GET", "/contacts/%s/tasks" % c["id"]).get("tasks") or []):
            if not t.get("completed") and t.get("assignedTo") == de:
                pedir("PUT", "/contacts/%s/tasks/%s" % (c["id"], t["id"]), {"assignedTo": para})
    print("  turnos: %d lead(s) novo(s) passado(s) para SDR em turno" % len(novos))


def filas_por_sdr(cs, aplicar):
    """Duas SDRs no mesmo horário não podem puxar a mesma `fila-tel` (ligariam para os mesmos
    leads). Com 2+ SDRs com usuário em equipe.json, mantém para cada uma a tag `tag_fila` =
    contatos com `fila-tel` cujo dono é ela. Com uma SDR só, não faz nada (ela puxa fila-tel)."""
    try:
        from turnos import equipe
        sdrs = [p for p in equipe()["sdrs"] if p.get("userId") and p.get("tag_fila")]
    except Exception as e:
        print("  filas por SDR: equipe.json indisponível (%s)" % e)
        return
    if len(sdrs) < 2:
        print("  filas por SDR: %d SDR com usuário: todas puxam fila-tel" % len(sdrs))
        return
    for p in sdrs:
        tag = p["tag_fila"]
        quer = {c["id"] for c in cs if "fila-tel" in (c.get("tags") or []) and c.get("assignedTo") == p["userId"]}
        tem = {c["id"] for c in cs if tag in (c.get("tags") or [])}
        print("  %s: %d desejados, %d com a tag" % (tag, len(quer), len(tem)))
        if not aplicar:
            continue
        for cid in quer - tem:
            pedir("POST", "/contacts/%s/tags" % cid, {"tags": [tag]})
        for cid in tem - quer:
            pedir("DELETE", "/contacts/%s/tags" % cid, {"tags": [tag]})


SEM_CAD = "sem-cadencia"
WF_INBOUND = "c2375e2f-b4cb-4947-8377-7c1e0529ba82"
TENT_N = "qHJGJKZBccASOKkKP8ge"      # Tentativa nº (0 = cadência nunca tocou)
CONEX_WA = "Og1CkI9x9OztsV242nIM"
MAX_TENT = 12


def ultima_ligacao_horas(cid):
    import datetime as dt
    agora = dt.datetime.now(dt.timezone.utc)
    r = pedir("GET", "/conversations/search?locationId=%s&contactId=%s" % (LOC, cid))
    ult = None
    for cv in r.get("conversations") or []:
        m = pedir("GET", "/conversations/%s/messages?limit=30" % cv["id"])
        for x in ((m.get("messages") or {}).get("messages") or []):
            if x.get("messageType") == "TYPE_CALL" and x.get("direction") == "outbound":
                q = dt.datetime.fromisoformat(x["dateAdded"].replace("Z", "+00:00"))
                ult = q if ult is None or q > ult else ult
    return None if ult is None else (agora - ult).total_seconds() / 3600


def ritmo_sem_cadencia(cs, etapas, aplicar):
    """Leads `sem-cadencia` (os 36 de 19-21/09, que entraram antes da Cadência Inbound; o dono
    decidiu em 28/09 ligar sem mandar WhatsApp automático): o atuador faz o papel da cadência
    só na ligação. Põe `fila-tel` no máximo 1 vez por dia (sem ligação nas últimas 24 h), até
    12 tentativas; o Pós-ligação v3 tira a tag quando a SDR registra o Resultado. Para quando
    o lead conecta, pede para não ligar, fica sem telefone ou sai de CONECTAR."""
    n = 0
    for c in cs:
        tags = set(c.get("tags") or [])
        if SEM_CAD not in tags or "fila-tel" in tags:
            continue
        if etapas.get(c["id"]) != CONECTAR or not c.get("phone") or c.get("dnd"):
            continue
        if tags & {"nao-perturbe", TAG_FALOU, "telefone-invalido"}:
            continue
        try:
            tent = float(valor(c, TENT_TEL) or 0)
            con = float(valor(c, CONEX_TEL) or 0) + float(valor(c, CONEX_WA) or 0)
        except (TypeError, ValueError):
            continue
        if con > 0 or tent >= MAX_TENT:
            continue
        h = ultima_ligacao_horas(c["id"])
        if h is not None and h < 24:
            continue
        n += 1
        if aplicar:
            pedir("POST", "/contacts/%s/tags" % c["id"], {"tags": ["fila-tel"]})
    print("  sem cadência: %d lead(s) voltam para a fila-tel%s" % (n, "" if aplicar else " (DRY)"))


def rede_orfaos(cs, etapas, aplicar):
    """Lead novo que ficou fora da cadência: em CONECTAR, com `atraso-1a-tentativa`, Tentativa
    nº 0, sem `fila-tel`, entrou há mais de 2 h e menos de 3 dias -> entra na Cadência Inbound
    (fluxo normal, com WhatsApp). A cadência não aceita o mesmo lead duas vezes, então quem já
    está nela (esperando janela ou teto) não é afetado."""
    import datetime as dt
    agora = dt.datetime.now(dt.timezone.utc)
    n = 0
    for c in cs:
        tags = set(c.get("tags") or [])
        if "atraso-1a-tentativa" not in tags or "fila-tel" in tags or SEM_CAD in tags:
            continue
        if etapas.get(c["id"]) != CONECTAR or not c.get("phone") or TESTE.search(c.get("contactName") or ""):
            continue
        try:
            if float(valor(c, TENT_N) or 0) > 0:
                continue
            entrou = dt.datetime.fromisoformat((c.get("dateAdded") or "").replace("Z", "+00:00"))
        except (TypeError, ValueError):
            continue
        idade = (agora - entrou).total_seconds() / 3600
        if not (2 <= idade <= 72):
            continue
        n += 1
        print("  órfão: %s %s entra na Cadência Inbound%s" % (c["id"], c.get("contactName") or "?",
                                                              "" if aplicar else " (DRY)"))
        if aplicar:
            pedir("POST", "/contacts/%s/workflow/%s" % (c["id"], WF_INBOUND), {})
    print("  rede de órfãos: %d lead(s)" % n)


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

    rede_trava(cs, etapas, aplicar)
    ritmo_sem_cadencia(cs, etapas, aplicar)
    rede_orfaos(cs, etapas, aplicar)
    dono_por_turno(cs, etapas, aplicar)
    filas_por_sdr(cs, aplicar)
    d_sdr, d_clo, a_sdr, a_clo, excl = decidir(cs, etapas)
    nome = {c["id"]: (c.get("contactName") or "?") for c in cs}

    if excl:
        print("\n  excluidos por heuristica de nome de teste (%d):" % len(excl))
        for cid, n, _ in excl:
            print("     %s  %s" % (cid, n))

    plano = []
    d_ativo = {c["id"] for c in cs if etapas.get(c["id"]) in DO_CLOSER + (FORMALIZAR,)}

    def quer_wa(c):
        tags = set(c.get("tags") or [])
        if etapas.get(c["id"]) != CONECTAR or not c.get("phone") or c.get("dnd") or TESTE.search(c.get("contactName") or ""):
            return False
        if tags & {"nao-perturbe", TAG_FALOU, "wa-feito-hoje", "telefone-invalido"}:
            return False
        try:
            tel = float(valor(c, TENT_TEL) or 0)
            con = float(valor(c, CONEX_TEL) or 0) + float(valor(c, "Og1CkI9x9OztsV242nIM") or 0)
        except (TypeError, ValueError):
            return False
        return tel >= 1 and con == 0
    d_wa = {c["id"] for c in cs if quer_wa(c)}
    a_wa = {c["id"] for c in cs if TAG_WA in (c.get("tags") or [])}
    a_ativo = {c["id"] for c in cs if TAG_CLOSER_ATIVO in (c.get("tags") or [])}
    for tag, desejado, atual in ((TAG_SDR, d_sdr, a_sdr),
                                 (TAG_CLOSER, d_clo, a_clo),
                                 (TAG_CLOSER_ATIVO, d_ativo, a_ativo),
                                 (TAG_WA, d_wa, a_wa)):
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
