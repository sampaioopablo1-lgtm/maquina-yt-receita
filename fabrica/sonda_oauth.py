#!/usr/bin/env python3
"""Diz se o runner consegue publicar SEM o Supabase — e nunca imprime segredo.

POR QUE ISTO EXISTE (11/10/2026). A maquina dependia de uma reconexao manual do
conector Supabase para alcancar `config.yt_token_<canal>`, e com o gateway em
402 nem o REST servia. O dono pediu para tirar essa dependencia.

O repo JA tem a rota sem banco, e ela estava escrita em `retomar.yml`: o segredo
`YT_OAUTH_JSON` guarda `{canal: {client_id, client_secret, refresh_token}}` e o
runner refresca o access token sozinho, direto no endpoint do Google. Nenhuma
chamada ao Supabase participa disso.

O que faltava era SABER se o segredo esta preenchido e se o refresh token ainda
vive — os refresh tokens morriam de sete em sete dias (303). Esta sonda responde
isso, e responde para cada canal da frota em separado, porque `YT_OAUTH_JSON` e
um mapa e pode ter um canal bom e outro morto.

O QUE ELA NUNCA FAZ, e isto e trava da rotina:
  * nao imprime refresh token, client_secret nem access token — nem truncado;
  * nao grava nada em arquivo;
  * nao publica, nao apaga, nao altera video.
Ela imprime: presenca, contagem de caracteres, e o resultado do refresh com o
ESCOPO concedido, que nao e segredo e e justamente o que decide se o longo sobe
com legenda (`youtube.force-ssl`) e se a retencao volta
(`yt-analytics.readonly`).
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

try:                                        # rodando como pacote
    from fabrica.oauth_mapa import desembrulha
except ImportError:                         # rodando o arquivo solto no runner
    from oauth_mapa import desembrulha

FROTA = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")
TOKEN_URI = "https://oauth2.googleapis.com/token"


def nota(msg: str) -> None:
    print(f"::notice::{msg}")


def aviso(msg: str) -> None:
    print(f"::warning::{msg}")


def presenca(nome: str) -> int:
    """Tamanho do segredo, ou 0. NUNCA o conteudo."""
    return len(os.environ.get(nome) or "")


def refresca(cfg: dict) -> tuple[bool, str]:
    """Troca refresh por access token. Devolve (ok, escopo ou erro).

    So o ESCOPO sai daqui. O access token fica nesta funcao e morre com ela.
    """
    corpo = json.dumps({
        "client_id": cfg["client_id"],
        "client_secret": cfg["client_secret"],
        "refresh_token": cfg["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(
        cfg.get("token_uri", TOKEN_URI), data=corpo,
        headers={"Content-Type": "application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        # O corpo do erro do Google traz `error`/`error_description`, que nao
        # sao segredo e sao o que distingue token revogado de cliente errado.
        try:
            det = json.loads(e.read().decode("utf-8", "replace"))
            cru = f"{det.get('error')}: {det.get('error_description')}"
        except ValueError:
            cru = "corpo ilegivel"
        return False, f"HTTP {e.code} — {cru}"
    except Exception as e:                                # noqa: BLE001
        return False, f"{type(e).__name__}"
    if "access_token" not in r:
        return False, "resposta 200 SEM access_token"
    return True, r.get("scope", "(sem campo scope)")


def main() -> int:
    oauth_n = presenca("YT_OAUTH_JSON")
    nota(f"YT_OAUTH_JSON: {'presente' if oauth_n else 'AUSENTE'} "
         f"({oauth_n} chars)")

    for canal in FROTA:
        nome = "YT_TOKEN_" + canal.upper().replace("-", "_")
        n = presenca(nome)
        nota(f"{nome}: {'presente' if n else 'AUSENTE'} ({n} chars)")

    if not oauth_n:
        aviso("sem YT_OAUTH_JSON o runner NAO publica sozinho — a rota sem "
              "banco depende deste segredo")
        return 0

    try:
        # `desembrulha` e nao `json.loads`: o copiar do SQL Editor embrulha o
        # valor numa coluna so, e em 11/10 isso fez a sonda ler "1 canal" com
        # os tres dentro (run 38175092152).
        mapa = desembrulha(os.environ["YT_OAUTH_JSON"])
    except ValueError:
        aviso("YT_OAUTH_JSON nao e JSON valido — formato esperado: "
              '{"<canal>": {"client_id", "client_secret", "refresh_token"}}')
        return 0

    nota(f"YT_OAUTH_JSON tem {len(mapa)} canal(is)")
    vivos = []
    for canal in FROTA:
        cfg = mapa.get(canal)
        if not cfg:
            aviso(f"{canal}: FORA do YT_OAUTH_JSON")
            continue
        faltam = [k for k in ("client_id", "client_secret", "refresh_token")
                  if not cfg.get(k)]
        if faltam:
            aviso(f"{canal}: entrada incompleta, falta {', '.join(faltam)}")
            continue
        ok, detalhe = refresca(cfg)
        if not ok:
            aviso(f"{canal}: refresh FALHOU — {detalhe}")
            continue
        vivos.append(canal)
        tem = lambda s: "sim" if s in detalhe else "NAO"   # noqa: E731
        nota(f"{canal}: refresh OK — upload={tem('youtube.upload')}, "
             f"force-ssl={tem('youtube.force-ssl')}, "
             f"analytics={tem('yt-analytics.readonly')}")

    if vivos:
        nota(f"PUBLICACAO SEM BANCO possivel em: {', '.join(vivos)}")
    else:
        aviso("nenhum canal da frota refresca — a rota sem banco esta morta "
              "e o destrave depende do dono")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
