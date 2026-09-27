#!/usr/bin/env python3
"""Instala e prova o Painel SDR (supabase/functions/painel-sdr) — roda na Action.

O QUE E O PAINEL
----------------
A pagina de qualificacao e agendamento do SDR, servida por uma Edge Function do
Supabase, falando com a API publica do GHL. Substitui o formulario nativo
`Qualificacao SDR` (DNz54AK2ryRSW7uCuznP), que a API nao edita e que nao le o
contato, nao mostra a agenda do closer e nao lista usuarios.

O QUE ESTE SCRIPT FAZ (`--instalar`)
------------------------------------
1. Pergunta ao painel se o token do GHL ja esta guardado. NAO o entrega: a
   entrega automatica foi barrada pela politica de seguranca da sessao; e o
   dono quem poe a linha `ghl_pit` na tabela `config` (ver token_no_painel).
2. Cria o campo `SDR responsavel` (texto, contato) se nao existir — e o campo
   que guarda QUEM qualificou, escolhido da lista de usuarios do CRM.
   `Qualificacao` ja existe mas e o canal (SDR / IA / Vendedor), nao a pessoa.
   Rota: POST /locations/{id}/customFields, que ACEITA model=contact. E a rota
   antiga; a nova (/custom-fields/) recusa contato — licao 2.19.
3. Sonda o que o painel usa e imprime: usuarios, calendario do closer, horarios
   livres nos proximos 7 dias, e se o PIT consegue criar menu lateral
   (POST /custom-menus/ costuma exigir token de agencia; aqui so mede).
4. Chama `/api/saude` do painel e SAI 1 se ele nao responder ok. O sucesso do
   job e a prova de que o painel esta no ar com o token certo.

Nunca apaga nada. Escreve: uma linha na tabela `config`, um campo novo (uma
vez), e nada mais.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

GHL = "https://services.leadconnectorhq.com"
VERSAO = "2021-07-28"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/131.0.0.0 Safari/537.36")
LOC = "1D53YTI9C7oIMBavcQxV"
CALENDARIO = "3uNQFjCEDe7b4gKZJuOZ"
FUSO = "America/Sao_Paulo"
CAMPO_SDR = "SDR responsável"
PAINEL = "https://cscczluzpblzhvojxanp.supabase.co/functions/v1/painel-sdr"


def env(nome: str) -> str:
    v = (os.environ.get(nome) or "").strip()
    if not v:
        raise SystemExit("sem %s no ambiente — este script roda na Action." % nome)
    return v


def http(metodo: str, url: str, corpo=None, cabecalhos=None, tolerar=()):
    dados = None if corpo is None else json.dumps(corpo).encode("utf-8")
    req = urllib.request.Request(url, data=dados, method=metodo)
    # UA de navegador SO para o GHL (Cloudflare 1010). O Supabase faz o inverso:
    # recusa a chave secreta quando o User-Agent parece navegador ("Forbidden use
    # of secret API key in browser", medido no run 36333353072). Um UA para cada.
    req.add_header("User-Agent", UA if url.startswith(GHL) else "wesales-painel-sdr/1 (GitHub Actions)")
    req.add_header("Accept", "application/json")
    if dados is not None:
        req.add_header("Content-Type", "application/json")
    for k, v in (cabecalhos or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            t = r.read().decode("utf-8")
            return r.status, (json.loads(t) if t.strip().startswith(("{", "[")) else t)
    except urllib.error.HTTPError as e:
        detalhe = ""
        try:
            detalhe = e.read().decode("utf-8")[:400]
        except Exception:
            pass
        if e.code in tolerar:
            return e.code, detalhe
        raise SystemExit("%s %s -> HTTP %s %s" % (metodo, url, e.code, detalhe))
    except urllib.error.URLError as e:
        raise SystemExit("%s %s -> rede recusou: %s" % (metodo, url, e.reason))


def ghl(metodo: str, rota: str, corpo=None, tolerar=()):
    return http(metodo, GHL + rota, corpo,
                {"Authorization": "Bearer " + env("GHL_PIT"), "Version": VERSAO}, tolerar)


# ---------------------------------------------------------------- passos

def token_no_painel() -> bool:
    """O token do GHL dentro do painel e responsabilidade do DONO, nao deste script.

    A entrega automatica (a Action mandar o segredo GHL_PIT para o painel) foi
    barrada duas vezes pela politica de seguranca da sessao em 27/09 — gravacao
    de segredo em servico externo. Fica registrado e nao contornado. O dono poe a
    linha `ghl_pit` na tabela `config` do Supabase (projeto cscczluzpblzhvojxanp)
    ou autoriza a regra de permissao; aqui so se PERGUNTA ao painel se ja tem.
    """
    st, r = http("GET", PAINEL + "/api/saude", tolerar=(400, 401, 403, 404, 500, 502, 503))
    tem = st == 200 and isinstance(r, dict) and bool(r.get("token_guardado"))
    print("  1. token do GHL no painel: %s" % ("SIM" if tem else "NAO — ver docstring de token_no_painel()"))
    return tem


def campo_sdr() -> str:
    st, r = ghl("GET", "/locations/%s/customFields?model=contact" % LOC)
    lista = r.get("customFields") or []
    for c in lista:
        if c.get("name") == CAMPO_SDR:
            print("  2. campo `%s` ja existe: %s" % (CAMPO_SDR, c["id"]))
            return c["id"]
    st, r = ghl("POST", "/locations/%s/customFields" % LOC,
                {"name": CAMPO_SDR, "dataType": "TEXT", "model": "contact",
                 "placeholder": "nome do SDR que qualificou (preenchido pelo painel)"})
    novo = (r.get("customField") or r).get("id")
    print("  2. campo `%s` CRIADO pela API: %s (HTTP %s)" % (CAMPO_SDR, novo, st))
    # Rele: a resposta da escrita nao e o estado (licao 2.15).
    st, r = ghl("GET", "/locations/%s/customFields?model=contact" % LOC)
    if not any(c.get("id") == novo for c in (r.get("customFields") or [])):
        raise SystemExit("  campo criado nao aparece na releitura — parando.")
    return novo


def sondar() -> None:
    st, r = ghl("GET", "/users/?locationId=%s" % LOC)
    us = r.get("users") or []
    print("  3a. usuarios do CRM (lista do seletor de SDR): %d" % len(us))
    for u in us:
        print("      - %s  %s  <%s>" % (u.get("id"), u.get("name"), u.get("email")))

    st, r = ghl("GET", "/calendars/%s" % CALENDARIO)
    c = r.get("calendar") or r
    print("  3b. calendario %s: `%s` · slot %s %s · equipe %s · ativo=%s"
          % (CALENDARIO, c.get("name"), c.get("slotDuration"), c.get("slotDurationUnit"),
             [m.get("userId") for m in (c.get("teamMembers") or [])], c.get("isActive")))

    ini = int(time.time() * 1000)
    fim = ini + 7 * 86_400_000
    st, r = ghl("GET", "/calendars/%s/free-slots?%s" % (
        CALENDARIO, urllib.parse.urlencode({"startDate": ini, "endDate": fim, "timezone": FUSO})))
    dias = {k: len((v or {}).get("slots") or []) for k, v in r.items() if k != "traceId"}
    print("  3c. horarios livres do closer nos proximos 7 dias: %s (total %d)"
          % (dias or "nenhum", sum(dias.values())))
    if not dias:
        print("      !! sem horario livre: o SDR nao vai conseguir agendar. Conferir a")
        print("         disponibilidade do calendario `Reuniao com closer` na tela.")

    st, r = ghl("GET", "/custom-menus/?locationId=%s" % LOC, tolerar=(400, 401, 403, 404, 422))
    print("  3d. GET /custom-menus/ com o PIT -> HTTP %s %s"
          % (st, ("(menu lateral por API: NAO com este token — e escopo de agencia)"
                  if st != 200 else "(menu lateral por API: possivel)")))


def saude() -> bool:
    st, r = http("GET", PAINEL + "/api/saude", tolerar=(400, 401, 403, 404, 500, 502, 503))
    print("  4. painel /api/saude -> HTTP %s %s" % (st, json.dumps(r, ensure_ascii=False)[:300]))
    return st == 200 and isinstance(r, dict) and bool(r.get("ok"))


def instalar() -> int:
    print("=" * 74)
    print("PAINEL SDR — instalar e provar")
    print("=" * 74)
    token_no_painel()
    campo_sdr()
    sondar()
    ok = saude()
    print("\n  endereco do painel: %s" % PAINEL)
    print("  veredito: %s" % ("PAINEL NO AR" if ok else "PAINEL NAO RESPONDEU OK"))
    return 0 if ok else 1


def main() -> int:
    if "--instalar" in sys.argv[1:]:
        return instalar()
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
