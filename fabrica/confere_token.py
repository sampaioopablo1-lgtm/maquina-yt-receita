#!/usr/bin/env python3
"""Testa o token OAuth do canal ANTES de gastar render.

Existe por causa de 19/08/2026: o agla-level-004 renderizou 20 minutos, foi
entregue no Storage e so entao a publicacao descobriu que o refresh token
tinha morrido — 45 minutos DEPOIS de eu mesmo o ter testado vivo. Naquela
madrugada 9 dos 12 tokens morreram em cascata (aprendizado 303/304): os
emitidos enquanto o app OAuth ainda estava em modo Testing expiram no seu
proprio marco de 7 dias, um a um, sem aviso.

Falhar aqui custa 30 segundos e deixa a mensagem certa no log; falhar no
passo de publicacao custa o render inteiro e um pacote parado.

Uso: python3 fabrica/confere_token.py <canal>
Ambiente: SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY (ou SB/KEY).
"""
import json
import os
import sys
import urllib.parse
import urllib.request


def _env(*nomes):
    for n in nomes:
        v = os.environ.get(n)
        if v:
            return v.rstrip("/") if n.endswith("URL") or n == "SB" else v
    return None


def token_do_canal(canal, sb, sk):
    url = (f"{sb}/rest/v1/config?chave=eq."
           f"{urllib.parse.quote('yt_token_' + canal, safe='')}&select=valor")
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {sk}", "apikey": sk})
    with urllib.request.urlopen(req, timeout=30) as r:
        linhas = json.load(r)
    if not linhas:
        sys.exit(f"config.yt_token_{canal} nao existe no banco — o canal nunca "
                 f"foi autorizado. Peca o link de autorizacao ao Pablo.")
    return linhas[0]["valor"]


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python3 fabrica/confere_token.py <canal>")
    canal = sys.argv[1]
    sb = _env("SUPABASE_URL", "SB")
    sk = _env("SUPABASE_SERVICE_ROLE_KEY", "KEY")
    if not (sb and sk):
        sys.exit("AMBIENTE: sem SUPABASE_URL/SUPABASE_SERVICE_ROLE_KEY")
    tok = token_do_canal(canal, sb, sk)
    dados = urllib.parse.urlencode({
        "client_id": tok["client_id"], "client_secret": tok["client_secret"],
        "grant_type": "refresh_token", "refresh_token": tok["refresh_token"],
    }).encode()
    req = urllib.request.Request(tok["token_uri"], data=dados, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            json.load(r)["access_token"]
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace")[:300]
        sys.exit(
            f"TOKEN MORTO ({canal}): {e.code} {corpo}\n"
            f"O refresh token expirou ou foi revogado. Nada aqui se conserta "
            f"sozinho: o Pablo precisa reautorizar ESTE canal pelo link de "
            f"autorizacao e colar a URL do localhost. O render foi abortado de "
            f"proposito — renderizar sem rota de publicacao gasta 20 minutos "
            f"para produzir um pacote parado (aprendizado 304)."
        )
    print(f"token de {canal}: vivo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
