#!/usr/bin/env python3
"""Faz da FICHA DO CONTATO o formulario BANT — dentro do CRM, pela API publica.

POR QUE
-------
O dono decidiu em 27/09 17:20: tudo dentro do CRM, nenhum sistema externo para os
usuarios. O formulario nativo nao e editavel por API (forms.json so le). O que a
API edita e a ESTRUTURA DOS CAMPOS do contato: nome e posicao
(`PUT /locations/{id}/customFields/{id}`), criacao (`POST`, model=contact). A
ficha do contato ja mostra todos os campos, ja vem preenchida com o que o anuncio
trouxe, e o botao de agendar do proprio contato abre a agenda do closer. Entao a
ficha E o formulario — falta so estar na ordem certa e com os grupos visiveis.

Este script:
  --sondar   prova, num campo de teste proprio, o que a API aceita: renomear sem
             mudar o fieldKey (senao os merge fields dos workflows quebram),
             posicao, `parentId` (pasta) e `options` (lista de opcoes na criacao).
             Cria e apaga so o campo de sonda `zz-sonda-bant`. Nao toca em campo real.
  --aplicar  renomeia e reordena os campos que o SDR usa, em grupos BANT, e cria
             `SDR responsavel` como lista com os usuarios do CRM. Rele e sai 1 se
             nao convergir. Nunca apaga campo real; apaga so o `SDR responsavel`
             TEXTO criado por mim as 16:53 (vazio), para dar lugar a lista.

O que fica fora, e por que: editar o formulario nativo e a descricao do evento no
`Pos-agendamento v2` e API interna — precisa do `GHL_STORAGE_STATE` (ver
wesales/tools/renovar_bearer.js). Isso e do dono, uma vez.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

GHL = "https://services.leadconnectorhq.com"
VERSAO = "2021-07-28"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/131.0.0.0 Safari/537.36")
LOC = "1D53YTI9C7oIMBavcQxV"
SONDA = "zz-sonda-bant"
SDR_TEXTO_ANTIGO = "LoSi8PQCbBRjmkMC8CH8"   # `SDR responsavel` TEXT, criado 27/09 16:53, vazio
NOME_SDR = "SDR responsável"

# (id, nome novo, posicao). Prefixo = grupo BANT; "(anúncio)" = veio do formulario
# do Meta, o SDR confirma e nao pergunta. Posicao manda na ordem da ficha.
BANT = [
    # identidade
    ("zs7KhkmfUMyuXWQlyUv7", "Empresa", 100),
    ("Z7qwvDlagOLEhoCz5G5v", "Segmento", 110),
    ("2tLo2m4KLTcP6fTEq3LG", "Instagram", 120),
    ("f1jNltRYjcrgKUZlxo8z", "Site", 130),
    # N
    ("OJQEsl5dV37pfVY2sIaB", "N · Necessidade (anúncio)", 200),
    ("qmIKSSDVYNLl5E8vnr3f", "N · Dor principal", 210),
    ("wmod0p91VuukwWDwKCgi", "N · Clientes novos por mês", 220),
    ("xjEcIFfdt2h29wBaKMQO", "N · Quem atende os leads", 230),
    ("sJY6q3X7deZ5yGbjiORT", "N · Tem time comercial", 240),
    ("qxJhMydTz6DcM4td4F08", "N · Canal principal de venda", 250),
    ("dYKivcXqdw4MToQLwoA9", "N · Usa CRM", 260),
    ("O500dbTabWUJwnBKwuUl", "N · Já teve agência?", 270),
    ("QyEDg0qFlQ3gra5qZsJF", "N · Experiência com agência", 280),
    # T
    ("2LnUD4KYSGkIBwiUdzl3", "T · Urgência (anúncio)", 300),
    ("lAqbaJE9K4LDkq3t2zzc", "T · Prazo", 310),
    # B
    ("bQithNwReQIBGlZBaNlI", "B · Investimento mensal em anúncios (anúncio)", 400),
    ("x5JUx0YCWaZmH3Q85psI", "B · Investe em anúncios", 410),
    ("f5bd9nBObV1cGgejAzdv", "B · Plataformas de anúncio", 420),
    ("SZVgh0Y5HRcWWZG4fO9V", "B · Budget", 430),
    # A
    ("3dphGCPCoFcYXEQC2jeB", "A · Decisor", 500),
    # fechamento da ligacao
    ("nPafc9c0JdSSptdPhUlF", "Resultado da tentativa", 600),
    ("IBOMNQecWtIUruHpNAs1", "Data de retorno", 610),
    ("IHXNFnguTPyNj5Q59ea2", "Hora do retorno", 620),
    ("mJv4YcFBH4NsPfbh5Q3G", "Qualificação", 630),
    ("kdKnJecyZtssILfPPigl", "Permissão WhatsApp", 640),
    # closer
    ("c470gqXWCkwqE9yVrcEi", "Reunião foi qualificada", 700),
    ("5L0RMR1HZVQ7IevyjOQX", "Motivo da desqualificação", 710),
    ("ffIpN8kTlhncr7K00Xzy", "Data do veredito do closer", 720),
]
POS_SDR = 590  # `SDR responsavel` entra logo antes do fechamento

# Pasta da FICHA: a que o dono ja usava para `Urgencia` e `Empresa`. A sonda do run
# 36335476750 provou que `parentId` muda por PUT (o schema nao o lista, a API
# aceita). Pasta nova nao sai por API (400), entao a ficha do SDR vai para esta;
# os 30 campos da maquina ficam na grande. O nome da pasta so a tela mostra.
PASTA_FICHA = "zHU4yGXKHdxBHnGxUmai"


def env(nome: str) -> str:
    v = (os.environ.get(nome) or "").strip()
    if not v:
        raise SystemExit("sem %s no ambiente — este script roda na Action." % nome)
    return v


def ghl(metodo: str, rota: str, corpo=None, tolerar=()):
    dados = None if corpo is None else json.dumps(corpo).encode("utf-8")
    req = urllib.request.Request(GHL + rota, data=dados, method=metodo)
    req.add_header("Authorization", "Bearer " + env("GHL_PIT"))
    req.add_header("Version", VERSAO)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", UA)          # sem isto: Cloudflare 1010
    if dados is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            t = r.read().decode("utf-8")
            return r.status, (json.loads(t) if t else {})
    except urllib.error.HTTPError as e:
        det = ""
        try:
            det = e.read().decode("utf-8")[:300]
        except Exception:
            pass
        if e.code in tolerar:
            return e.code, det
        raise SystemExit("%s %s -> HTTP %s %s" % (metodo, rota, e.code, det))
    except urllib.error.URLError as e:
        raise SystemExit("%s %s -> rede recusou: %s" % (metodo, rota, e.reason))


def catalogo() -> dict:
    st, r = ghl("GET", "/locations/%s/customFields?model=contact" % LOC)
    return {c["id"]: c for c in (r.get("customFields") or [])}


def campo(cid: str) -> dict:
    st, r = ghl("GET", "/locations/%s/customFields/%s" % (LOC, cid))
    return r.get("customField") or r


def usuarios() -> list:
    """Os SDRs da conta — nao todos os usuarios.

    A versao anterior devolvia TODO usuario da subconta, e por isso a picklist
    `SDR responsavel` nasceu com `Pablo Santos` dentro. Pablo e closer, gestor e
    administrador do sistema; SDR e a Andreyna. Como esta funcao alimenta a
    picklist E a reconciliacao (o --aplicar reescreve as opcoes quando elas
    divergem), corrigir a lista na tela nao durava: o run seguinte recolocava o
    admin, calado. O filtro tem de ser aqui.

    O sinal e `roles.role`: quem foi criado como `user` entra, `admin` nao. Foi
    por isso que o SDR foi cadastrado como `user` em 27/09. Nao ha campo de
    funcao no GHL, e este e o unico sinal que a API devolve.
    """
    st, r = ghl("GET", "/users/?locationId=%s" % LOC)
    sdrs, fora = [], []
    for u in (r.get("users") or []):
        nome = (u.get("name") or "").strip()
        if not nome:
            continue
        papel = ((u.get("roles") or {}).get("role") or "").lower()
        (sdrs if papel != "admin" else fora).append("%s (%s)" % (nome, papel or "sem papel"))
    if fora:
        print("  fora da lista de SDR, por serem admin: %s" % ", ".join(fora))
    return [n.rsplit(" (", 1)[0] for n in sdrs]


# ---------------------------------------------------------------- sondar

def sondar() -> int:
    print("=" * 74)
    print("SONDA — o que a API aceita na estrutura de campo (campo de teste proprio)")
    print("=" * 74)
    cat = catalogo()
    # limpa sonda antiga, se sobrou de um run interrompido
    for c in cat.values():
        if c.get("name") == SONDA:
            ghl("DELETE", "/locations/%s/customFields/%s" % (LOC, c["id"]))
            print("  (sonda antiga apagada: %s)" % c["id"])

    # a) criar lista com opcoes
    st, r = ghl("POST", "/locations/%s/customFields" % LOC,
                {"name": SONDA, "dataType": "SINGLE_OPTIONS", "model": "contact",
                 "options": ["um", "dois"], "position": 9990}, tolerar=(400, 422))
    if st in (400, 422):
        print("  a) POST SINGLE_OPTIONS com `options` -> HTTP %s %s" % (st, r))
        print("     lista com opcoes NAO sai por esta rota; tentando TEXT para as outras sondas")
        st, r = ghl("POST", "/locations/%s/customFields" % LOC,
                    {"name": SONDA, "dataType": "TEXT", "model": "contact", "position": 9990})
        opcoes_ok = False
    else:
        opcoes_ok = True
    sid = (r.get("customField") or r).get("id")
    c0 = campo(sid)
    print("  a) criado %s · dataType=%s · picklistOptions=%s · fieldKey=%s · position=%s · parentId=%s"
          % (sid, c0.get("dataType"), c0.get("picklistOptions"), c0.get("fieldKey"),
             c0.get("position"), c0.get("parentId")))
    print("     lista com opcoes na criacao: %s" % ("SIM" if opcoes_ok and c0.get("picklistOptions") else "NAO"))

    # b) renomear: o fieldKey muda?
    ghl("PUT", "/locations/%s/customFields/%s" % (LOC, sid), {"name": SONDA + " renomeada", "model": "contact"})
    c1 = campo(sid)
    print("  b) renomeado -> name=%r · fieldKey=%s · %s"
          % (c1.get("name"), c1.get("fieldKey"),
             "fieldKey PRESERVADO (renomear e seguro)" if c1.get("fieldKey") == c0.get("fieldKey")
             else "fieldKey MUDOU — renomear quebraria merge fields; NAO renomear"))

    # c) posicao
    ghl("PUT", "/locations/%s/customFields/%s" % (LOC, sid), {"name": c1.get("name"), "position": 42, "model": "contact"})
    c2 = campo(sid)
    print("  c) position=42 -> lido %s · %s" % (c2.get("position"), "OK" if c2.get("position") == 42 else "IGNORADO"))

    # d) parentId (pasta) — nao esta no schema; so medindo
    alvo = "zHU4yGXKHdxBHnGxUmai"
    st, r = ghl("PUT", "/locations/%s/customFields/%s" % (LOC, sid),
                {"name": c1.get("name"), "parentId": alvo, "model": "contact"}, tolerar=(400, 422))
    c3 = campo(sid)
    print("  d) parentId=%s -> HTTP %s · lido %s · %s"
          % (alvo, st, c3.get("parentId"), "PASTA MUDOU POR API" if c3.get("parentId") == alvo else "ignorado (pasta segue tela)"))

    # e) opcoes na atualizacao
    if opcoes_ok:
        st, r = ghl("PUT", "/locations/%s/customFields/%s" % (LOC, sid),
                    {"name": c1.get("name"), "options": ["um", "dois", "tres"], "model": "contact"}, tolerar=(400, 422))
        c4 = campo(sid)
        print("  e) PUT options=[3] -> HTTP %s · picklistOptions=%s" % (st, c4.get("picklistOptions")))

    ghl("DELETE", "/locations/%s/customFields/%s" % (LOC, sid))
    print("  sonda apagada. usuarios do CRM hoje: %s" % usuarios())
    return 0


# ---------------------------------------------------------------- aplicar

def aplicar() -> int:
    print("=" * 74)
    print("APLICAR — ficha do contato em ordem BANT + `SDR responsavel` como lista")
    print("=" * 74)
    cat = catalogo()
    faltam = [i for i, _, _ in BANT if i not in cat]
    if faltam:
        raise SystemExit("  campos do mapa que nao existem na conta: %s — parando." % faltam)

    escritas = 0
    for cid, nome, pos in BANT:
        c = cat[cid]
        if c.get("name") == nome and int(c.get("position") or -1) == pos and c.get("parentId") == PASTA_FICHA:
            continue
        ghl("PUT", "/locations/%s/customFields/%s" % (LOC, cid),
            {"name": nome, "position": pos, "parentId": PASTA_FICHA, "model": "contact"})
        escritas += 1
        print("  %-22s -> %-48s pos %s" % (cid, nome, pos))

    # `SDR responsavel` como lista com os usuarios do CRM
    nomes = usuarios()
    lista = next((c for c in cat.values() if c.get("name") == NOME_SDR and c.get("dataType") == "SINGLE_OPTIONS"), None)
    if lista is None:
        # O fieldKey e derivado do nome: enquanto o TEXTO `SDR responsavel` existir, o
        # POST da lista devolve 400 "contact.sdr_responsvel already exists" (run
        # 36335610418). Entao o TEXTO — meu, de 16:53, vazio — sai ANTES.
        antigo = cat.get(SDR_TEXTO_ANTIGO)
        if antigo and antigo.get("dataType") == "TEXT" and antigo.get("name") == NOME_SDR:
            ghl("DELETE", "/locations/%s/customFields/%s" % (LOC, SDR_TEXTO_ANTIGO))
            print("  campo TEXTO provisorio %s apagado (era meu, vazio) para liberar o fieldKey" % SDR_TEXTO_ANTIGO)
        st, r = ghl("POST", "/locations/%s/customFields" % LOC,
                    {"name": NOME_SDR, "dataType": "SINGLE_OPTIONS", "model": "contact",
                     "options": nomes, "position": POS_SDR, "parentId": PASTA_FICHA}, tolerar=(400, 422))
        if st in (400, 422):
            print("  !! lista `%s` nao criada: HTTP %s %s" % (NOME_SDR, st, r))
        else:
            novo = (r.get("customField") or r).get("id")
            print("  lista `%s` criada: %s · opcoes %s" % (NOME_SDR, novo, nomes))
            escritas += 1
    else:
        if sorted(lista.get("picklistOptions") or []) != sorted(nomes):
            st, r = ghl("PUT", "/locations/%s/customFields/%s" % (LOC, lista["id"]),
                        {"name": NOME_SDR, "options": nomes, "position": POS_SDR, "parentId": PASTA_FICHA, "model": "contact"}, tolerar=(400, 422))
            print("  opcoes de `%s` -> %s (HTTP %s)" % (NOME_SDR, nomes, st))
            escritas += 1

    print("\n  escritas: %d — relendo a conta..." % escritas)
    cat2 = catalogo()
    erros = [(cid, nome, pos, cat2[cid].get("name"), cat2[cid].get("position"), cat2[cid].get("parentId"))
             for cid, nome, pos in BANT
             if cat2[cid].get("name") != nome or int(cat2[cid].get("position") or -1) != pos
             or cat2[cid].get("parentId") != PASTA_FICHA]
    for e in erros:
        print("  NAO convergiu: %s esperado (%r, %s, pasta ficha) lido (%r, %s, %s)" % e)
    na_ficha = sum(1 for c in cat2.values() if c.get("parentId") == PASTA_FICHA)
    print("  campos na pasta da ficha: %d (esperado %d)" % (na_ficha, len(BANT) + 1))
    tem_lista = any(c.get("name") == NOME_SDR and c.get("dataType") == "SINGLE_OPTIONS" for c in cat2.values())
    print("  `%s` como lista: %s" % (NOME_SDR, "SIM" if tem_lista else "NAO"))
    print("  veredito: %s" % ("CONVERGIU" if not erros else "NAO convergiu"))
    return 0 if not erros else 1


def main() -> int:
    a = sys.argv[1:]
    if "--sondar" in a:
        return sondar()
    if "--aplicar" in a:
        return aplicar()
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
