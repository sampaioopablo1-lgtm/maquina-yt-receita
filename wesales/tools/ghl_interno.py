#!/usr/bin/env python3
"""Cliente da API interna do GHL (backend.leadconnectorhq.com) — SEM dependencia
externa: so biblioteca padrao.

POR QUE ESTE ARQUIVO EXISTE
---------------------------
Ja havia um cliente no projeto, `ghl_api.py`, e ele funciona — mas depende de duas
coisas que so existem no PC do dono:

1. o pacote `cli_anything.gohighlevel.utils.ghl_internal_client`, de um repositorio
   irmao (`gohighlevel-cli`) que **nao esta no GitHub** (conferido em 27/09/2026:
   a conta tem tres repositorios e nenhum e ele);
2. um `NODE_PATH` cravado em `C:\\Users\\sampa\\AppData\\Roaming\\npm\\node_modules`
   dentro do `renovar_bearer()`.

Enquanto isso valer, nenhuma sessao na nuvem edita workflow, e todo ajuste espera
uma pessoa. Este modulo remove a dependencia de codigo: fala HTTP direto, com
`urllib`, nos mesmos endpoints e com o mesmo corpo de PUT que o `ghl_api.py` usa
(lidos de `patch_funil_reuniao.put`, nao inventados).

O QUE ELE **NAO** RESOLVE, E NAO PODE
------------------------------------
- **O bearer.** A API interna aceita so token de sessao logada, que vive ~minutos.
  Quem renova e `renovar_bearer.py` (Playwright + estado de sessao), neste mesmo
  diretorio.
- **A rede do conteiner.** Medido em 27/09/2026: o proxy deste ambiente responde
  **403 na CONNECT** para `backend.leadconnectorhq.com` e
  `services.leadconnectorhq.com` — negacao de politica, nao falha de rede. Entao
  daqui este modulo nao alcanca a conta **ate o host ser liberado** na politica de
  rede do ambiente. Onde ele roda hoje sem mudanca nenhuma: **GitHub Actions**, que
  tem internet aberta.

Ou seja: o caminho desatendido e Action + segredo de sessao.

REGRA INVIOLAVEL PRESERVADA
---------------------------
`PUBLICADOS` lista os workflows que o dono proibiu de editar. `guard()` recusa, e
nenhuma funcao aqui publica nada sozinha — `put()` preserva o `status` que ja
estava lá.

USO
---
    python3 ghl_interno.py --token               # ha token? quanto dura?
    python3 ghl_interno.py --listar              # nomes, status, versao
    python3 ghl_interno.py --ler "Cadência Inbound" --salvar-em /tmp/x.json
    # escrita: sempre por script dedicado que importa este modulo
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

BASE = "https://backend.leadconnectorhq.com"
LOC = "1D53YTI9C7oIMBavcQxV"          # unica subconta permitida
_AQUI = os.path.dirname(os.path.abspath(__file__))
BEARER_FILE = os.path.join(_AQUI, "..", ".local", "_ghl_bearer.txt")
MAX_NOS = 450          # acima disto a conta pode recusar salvar (medido no projeto)

# Workflows PUBLICADOS que o dono proibiu de editar (copiado de ghl_api.py).
PUBLICADOS = {
    "e08a1580-975b-4c0f-934e-582fc6a0dbaa": "Porta de Entrada",
    "30da2c98-5f84-4af9-9ed2-71f628dc7c1e": "Mestre de saida",
    "cf6fa19d-6af8-4fcb-b0dd-6fcfcefde0cc": "Pos-ligacao",
    "94a837d0-d87a-438e-95f1-c620d55f1a7f": "Pos-agendamento",
    "ea0a49b7-f3a9-4d8a-8acd-802975d6db03": "Interceptacao de Sinal - Clique.",
    "7a1b4e6b-7e6e-4ed8-8ff4-cd98b88cdcff": "Interceptacao de Sinal - Resposta",
}


class SemBearer(RuntimeError):
    """Nao ha token de sessao — nada a fazer alem de avisar quem chamou."""


class RecusadoPelaConta(RuntimeError):
    """A conta respondeu erro. Nunca silencioso: o `ghl_api` aprendeu isso em
    23/09/2026, quando um PUT recusado passou por sucesso e o script seguiu
    imprimindo resumo de exito."""


def bearer() -> str:
    """Token de sessao: `GHL_BEARER` no ambiente, senao o arquivo local."""
    tok = (os.environ.get("GHL_BEARER") or "").strip()
    if not tok and os.path.exists(BEARER_FILE):
        tok = open(BEARER_FILE, encoding="utf-8").read().strip()
    if not tok:
        raise SemBearer(
            "sem token de sessao: defina GHL_BEARER ou grave "
            + BEARER_FILE + " (ver renovar_bearer.py)")
    if tok.count(".") != 2:
        raise SemBearer("GHL_BEARER nao parece um JWT (esperado a.b.c)")
    return tok


def minutos_restantes(tok: str | None = None) -> float:
    """Minutos ate o token vencer; negativo se venceu ou nao deu para ler."""
    import base64
    import time
    try:
        p = (tok or bearer()).split(".")[1]
        p += "=" * (-len(p) % 4)
        exp = json.loads(base64.urlsafe_b64decode(p)).get("exp", 0)
        return (float(exp) - time.time()) / 60.0
    except Exception:
        return -1.0


def pedir(metodo: str, caminho: str, corpo: dict | None = None, timeout: int = 60):
    """Uma chamada a API interna. Levanta em erro — nunca devolve falso sucesso."""
    url = BASE + caminho
    dados = None if corpo is None else json.dumps(corpo).encode("utf-8")
    req = urllib.request.Request(url, data=dados, method=metodo)
    req.add_header("authorization", "Bearer " + bearer())
    req.add_header("accept", "application/json")
    req.add_header("channel", "APP")
    req.add_header("source", "WEB_USER")
    req.add_header("version", "2021-07-28")
    if dados is not None:
        req.add_header("content-type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            bruto = r.read().decode("utf-8") or "{}"
    except urllib.error.HTTPError as e:
        detalhe = ""
        try:
            detalhe = e.read().decode("utf-8")[:400]
        except Exception:
            pass
        raise RecusadoPelaConta(
            "%s %s -> HTTP %s %s" % (metodo, caminho, e.code, detalhe)) from e
    except urllib.error.URLError as e:
        raise RecusadoPelaConta(
            "%s %s -> rede/politica recusou: %s. Se for 403 na CONNECT, o host "
            "esta negado na politica de rede deste ambiente."
            % (metodo, caminho, e.reason)) from e
    try:
        return json.loads(bruto)
    except ValueError:
        raise RecusadoPelaConta(
            "%s %s -> resposta nao era JSON: %r" % (metodo, caminho, bruto[:200]))


def guard(wf_id: str) -> None:
    if wf_id in PUBLICADOS:
        raise SystemExit(
            "RECUSADO: " + wf_id + " e o workflow PUBLICADO '"
            + PUBLICADOS[wf_id] + "'. Regra do dono: nunca editar.")


def listar() -> list:
    r = pedir("GET", "/workflow/" + LOC)
    return r if isinstance(r, list) else (r.get("workflows") or [])


def ler(wf_id: str) -> dict:
    return pedir("GET", "/workflow/" + LOC + "/" + wf_id)


def gatilhos(wf_id: str):
    return pedir("GET", "/workflow/" + LOC + "/trigger?workflowId=" + wf_id)


def por_nome(nome: str):
    for w in listar():
        if w.get("name") == nome:
            return w
    return None


def put(cur: dict, templates: list) -> dict:
    """Grava o workflow preservando o resto. Mesmo corpo do `patch_funil_reuniao.put`.

    Uma diferenca deliberada: **preserva o `status` que ja estava lá**, em vez de
    mandar `"published"` fixo como o helper original. Rascunho nao vira publicado
    por acidente.
    """
    guard(cur["id"])
    if len(templates) > MAX_NOS:
        raise RecusadoPelaConta(
            "%d nos: acima de ~%d a conta recusa salvar (medido no projeto)"
            % (len(templates), MAX_NOS))
    r = pedir("PUT", "/workflow/" + LOC + "/" + cur["id"], {
        "name": cur.get("name"),
        "status": cur.get("status", "draft"),
        "version": cur.get("version", 1),
        "allowMultiple": cur.get("allowMultiple", True),
        "stopOnResponse": cur.get("stopOnResponse", False),
        "allowMultipleOpportunity": cur.get("allowMultipleOpportunity", False),
        "timezone": cur.get("timezone", "account"),
        "window": cur.get("window"),
        "workflowData": {"templates": templates},
    })
    if not isinstance(r, dict) or r.get("_error"):
        raise RecusadoPelaConta(
            "PUT recusado em %r (%d nos): %s"
            % (cur.get("name"), len(templates),
               json.dumps(r, ensure_ascii=False)[:400]))
    return r


def exportar(wf_id: str, caminho: str) -> dict:
    """Le workflow + gatilhos e grava o JSON completo, como o `ghl_api.export`."""
    doc = {"workflow": ler(wf_id), "triggers": gatilhos(wf_id)}
    d = os.path.dirname(caminho)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    return doc


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(
        description="Cliente da API interna do GHL, sem dependencia externa.")
    ap.add_argument("--listar", action="store_true",
                    help="lista os workflows da subconta")
    ap.add_argument("--ler", metavar="NOME", help="le um workflow pelo nome exato")
    ap.add_argument("--salvar-em", metavar="ARQ", dest="salvar_em",
                    help="com --ler, grava o dump completo neste caminho")
    ap.add_argument("--token", action="store_true",
                    help="so diz se ha token de sessao e quanto ele ainda dura")
    a = ap.parse_args()

    if a.token:
        # `bearer()` primeiro, de proposito: `minutos_restantes` engole excecao e
        # devolve -1.0, entao perguntar so a ele confundiria "sem token" com
        # "token ilegivel". Foram dois estados diferentes num teste de 27/09.
        try:
            tok = bearer()
        except SemBearer as e:
            print("SEM TOKEN: %s" % e)
            return 2
        m = minutos_restantes(tok)
        if m < 0:
            print("token presente mas ILEGIVEL ou vencido (nao deu para ler o exp)")
            return 1
        print("token presente, vence em %.1f min" % m)
        return 0

    try:
        if a.listar:
            for w in sorted(listar(), key=lambda x: (x.get("name") or "")):
                print("%-42s %-10s v%-4s %s"
                      % ((w.get("name") or "")[:42], w.get("status"),
                         w.get("version"), w.get("id")))
            return 0
        if a.ler:
            w = por_nome(a.ler)
            if not w:
                print("nao existe nesta subconta: %r" % a.ler)
                return 1
            if a.salvar_em:
                exportar(w["id"], a.salvar_em)
                print("gravado em %s" % a.salvar_em)
            else:
                print(json.dumps(ler(w["id"]), ensure_ascii=False, indent=2)[:4000])
            return 0
    except (SemBearer, RecusadoPelaConta) as e:
        print("PAROU: %s" % e)
        return 2

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
