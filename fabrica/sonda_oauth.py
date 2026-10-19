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


def projeto_do_client_id(cid: str) -> str:
    """Numero do PROJETO do Google Cloud, extraido do `client_id`.

    POR QUE ISTO EXISTE (19/10/2026). Em 18/10 o zip v2.0 que o dono trouxe me
    fez achar um erro nosso de cota: o teto nao e "~40 videos/janela", e
    `10.000 / 1.600` = SEIS envios de video por dia **por projeto**. E aí abriu
    uma pergunta que decide o dobro do triplo: seis por CANAL (dezoito na frota)
    ou seis para os TRES juntos? Depende de a frota usar um projeto do Cloud ou
    tres, e isso ninguem sabia — o 667 diz que o par client_id/secret e da linha
    `yt_token_<canal>`, mas `tokens.py:205-206` mina token novo copiando o par
    de um MODELO, logo pode ter propagado o mesmo projeto para os tres.

    A resposta estava a vista e nao dependia do banco: o `client_id` de um
    cliente OAuth tem a forma `<numero do projeto>-<aleatorio>.apps.
    googleusercontent.com`, e o numero do projeto NAO e segredo — e o mesmo
    numero que aparece na barra do console do Cloud.

    **O QUE ESTA FUNCAO NAO FAZ, e e a trava desta sonda:** ela devolve SO os
    digitos iniciais. Nao devolve o client_id inteiro, nem a parte aleatoria,
    nem nada que se pareca com credencial. Entrada que nao tem a forma esperada
    devolve string vazia em vez de devolver o que sobrou — porque devolver "o
    resto" e como um client_id mal formado viraria vazamento.
    """
    cabeca = (cid or "").split("-", 1)[0]
    return cabeca if cabeca.isdigit() and len(cabeca) >= 6 else ""


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
    projetos: dict[str, str] = {}
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
        projetos[canal] = projeto_do_client_id(cfg["client_id"])
        tem = lambda s: "sim" if s in detalhe else "NAO"   # noqa: E731
        nota(f"{canal}: refresh OK — upload={tem('youtube.upload')}, "
             f"force-ssl={tem('youtube.force-ssl')}, "
             f"analytics={tem('yt-analytics.readonly')}")

    _relata_cota(projetos)

    if vivos:
        nota(f"PUBLICACAO SEM BANCO possivel em: {', '.join(vivos)}")
    else:
        aviso("nenhum canal da frota refresca — a rota sem banco esta morta "
              "e o destrave depende do dono")
    return 0


def _relata_cota(projetos: dict[str, str]) -> None:
    """Diz se o teto de envio e 6/dia POR CANAL ou 6/dia na FROTA.

    Nao inventa limiar: `videos.insert` custa 1.600 unidades e a cota padrao de
    um projeto e 10.000/dia, logo `10.000/1.600` = 6. O que esta funcao decide e
    o DENOMINADOR — quantos projetos existem —, e isso ela LE, nao supoe.
    """
    lidos = {c: p for c, p in projetos.items() if p}
    if not lidos:
        aviso("NUMERO DO PROJETO nao lido em nenhum canal — o teto de cota "
              "segue INDETERMINADO entre 6/dia na frota e 6/dia por canal")
        return
    distintos = sorted(set(lidos.values()))
    nota("projetos do Cloud por canal: "
         + ", ".join(f"{c}=projeto {p}" for c, p in sorted(lidos.items())))
    if len(distintos) == 1 and len(lidos) > 1:
        aviso(f"os {len(lidos)} canais lidos COMPARTILHAM o projeto "
              f"{distintos[0]} — logo o teto de envio e ~6 VIDEOS/DIA NA FROTA "
              "INTEIRA (10.000/1.600), e nao por canal. Os 7/dia/canal que o "
              "dono pede ficam 3,5x acima disso.")
    else:
        nota(f"{len(distintos)} projetos distintos em {len(lidos)} canais — "
             f"cada projeto tem cota propria, logo o teto e ~6 videos/dia POR "
             f"CANAL (~{6 * len(distintos)} na frota). Os 7/dia/canal seguem "
             "pouco acima do teto de UM projeto.")
    if len(lidos) < len(FROTA):
        aviso(f"so {len(lidos)} de {len(FROTA)} canais tiveram o projeto lido "
              "— o veredito acima vale para esses, nao para a frota")


if __name__ == "__main__":
    raise SystemExit(main())
