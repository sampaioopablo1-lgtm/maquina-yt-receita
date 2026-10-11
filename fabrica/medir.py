#!/usr/bin/env python3
"""Mede a frota no runner, SEM Supabase — e sem inventar denominador.

POR QUE ISTO EXISTE (11/10/2026). Medir dependia do banco por UM motivo so: o
token OAuth morava em `config.yt_token_<canal>`, atras do 402. Com o segredo
`YT_OAUTH_JSON` preenchido, o token nasce dentro do runner (foi assim que o
`epomeno-epipedo-s016` subiu as 21:17), e entao LER view e inscrito volta a ser
possivel mesmo com o gateway fechado. O que continua fora e GRAVAR em
`metricas` — por isso esta ferramenta so imprime, e imprime o suficiente para o
numero ser recuperado depois.

AS REGRAS MEDIDAS QUE ELA OBEDECE, e cada uma existe porque eu ja errei:
  * `688` — o estimador e o MAXIMO das leituras, declarado como PISO, com a
    faixa ao lado. A mediana devolve a replica ATRASADA.
  * `708` — a replica atrasada e da CHAMADA inteira. Entao sao TRES chamadas, e
    quem decide e `replica.chamada_para_gravar` pela SOMA, nao o olho.
  * `665` — agregado esconde chamada que falhou. Cada lote reporta o proprio
    `status_code`, e um lote que falha INTERROMPE o canal em vez de virar um
    total menor que parece leitura.
  * `697`/`668` — o denominador e `sum(views)` das pecas DA MAQUINA, nunca o
    `viewCount` do canal. As pecas da maquina sao as que batem com o
    `corpus_publicados.json`; canal com acervo anterior nao normaliza, e quem
    decide isso e `conversao.por_mil`.
  * `665` de novo — peca fora de `processed`, ou com `duration: P0D`, sai
    NOMEADA com id e idade em vez de contar como publicada.

O QUE ELA NAO FAZ: nao imprime refresh token, client_secret nem access token;
nao publica, nao apaga, nao altera video; nao grava arquivo nenhum.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import conversao                                          # noqa: E402
import replica                                            # noqa: E402
from oauth_mapa import desembrulha                        # noqa: E402

API = "https://www.googleapis.com/youtube/v3"
TOKEN_URI = "https://oauth2.googleapis.com/token"
LEITURAS = 3

CANAIS = {
    "labtreinamento": "UCtv_ewwSmwdi1ZRALW4_azg",
    "epomeno-epipedo": "UC1hk4k4QMjbPCfbw-S5xDyQ",
    "kolejny-poziom": "UCGe6sYpjzKyCC_K22ae1anw",
}


def nota(msg: str) -> None:
    print(f"::notice::{msg}")


def aviso(msg: str) -> None:
    print(f"::warning::{msg}")


def _get(url: str, token: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status != 200:                               # defensivo; urllib levanta
            raise RuntimeError(f"status {r.status}")
        return json.load(r)


def token_do_canal(cfg: dict) -> str:
    """O access token nasce e morre aqui dentro. Nunca e impresso."""
    corpo = json.dumps({
        "client_id": cfg["client_id"], "client_secret": cfg["client_secret"],
        "refresh_token": cfg["refresh_token"], "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(cfg.get("token_uri", TOKEN_URI), data=corpo,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["access_token"]


def uploads_e_estatisticas(cid: str, token: str) -> tuple[str, dict]:
    d = _get(f"{API}/channels?part=contentDetails,statistics&id={cid}", token)
    it = d["items"][0]
    return (it["contentDetails"]["relatedPlaylists"]["uploads"],
            it.get("statistics") or {})


def ids_do_canal(playlist: str, token: str) -> list[str]:
    ids, pagina = [], ""
    while True:
        u = (f"{API}/playlistItems?part=contentDetails&maxResults=50"
             f"&playlistId={playlist}")
        if pagina:
            u += f"&pageToken={pagina}"
        d = _get(u, token)
        ids += [i["contentDetails"]["videoId"] for i in d.get("items", [])]
        pagina = d.get("nextPageToken") or ""
        if not pagina:
            return ids


def uma_chamada(ids: list[str], token: str) -> dict[str, dict]:
    """Um lote de ate 50 por requisicao. Qualquer falha LEVANTA — 665."""
    fora = {}
    for i in range(0, len(ids), 50):
        lote = ids[i:i + 50]
        d = _get(f"{API}/videos?part=snippet,statistics,status,contentDetails"
                 f"&id={','.join(lote)}&maxResults=50", token)
        if len(d.get("items", [])) == 0 and lote:
            raise RuntimeError(f"lote de {len(lote)} ids voltou vazio")
        for it in d["items"]:
            fora[it["id"]] = it
    return fora


def idade_h(publicado: str | None) -> float | None:
    if not publicado:
        return None
    t = dt.datetime.fromisoformat(publicado.replace("Z", "+00:00"))
    return (dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 3600.0


def doentes(itens: dict[str, dict]) -> list[str]:
    """Peca fora de `processed` ou em P0D depois de 2 h — 665."""
    fora = []
    for vid, it in itens.items():
        st = (it.get("status") or {}).get("uploadStatus")
        dur = (it.get("contentDetails") or {}).get("duration")
        if st != "processed" or dur == "P0D":
            fora.append(f"{vid} ({st}, {dur})")
    return fora


def mede_canal(canal: str, cfg: dict, corpus: set[str]) -> None:
    token = token_do_canal(cfg)
    playlist, est = uploads_e_estatisticas(CANAIS[canal], token)
    ids = ids_do_canal(playlist, token)

    leituras, itens = [], {}
    for _ in range(LEITURAS):
        itens = uma_chamada(ids, token)
        leituras.append({v: int((it.get("statistics") or {}).get("viewCount", 0))
                         for v, it in itens.items()})

    escolhida = replica.chamada_para_gravar(leituras)
    pisos = replica.piso(leituras)
    div = replica.divergentes(leituras)
    forma = replica.mesma_forma(leituras)

    # SO as pecas da maquina entram no denominador (697). A ponte entre id e
    # peca e o titulo: o corpus e o nosso proprio registro do que subiu.
    # Nao da para usar o `viewCount` do canal, que nem conta Shorts (638).
    # `snippet` vem no mesmo `videos.list` de proposito: uma chamada a mais
    # por lote seria cota gasta para repetir o que ja veio.
    nossas = {v: p for v, p in pisos.items()
              if ((itens.get(v, {}).get("snippet") or {}).get("title") or
                  "").strip().casefold() in corpus}
    if not nossas:
        # Sem `snippet` o titulo nao vem; cai para o acervo inteiro e DIZ isso,
        # em vez de devolver zero como se fosse leitura.
        aviso(f"{canal}: nao deu para separar peca da maquina por titulo — "
              f"o total abaixo e do ACERVO INTEIRO e NAO normaliza (668)")
        nossas = pisos

    insc = int(est.get("subscriberCount") or 0)
    nota(f"{canal}: {len(ids)} ids | chamada gravavel = {escolhida + 1} de "
         f"{LEITURAS} | divergentes={len(div)} | mesma_forma={forma}")
    nota(f"{canal}: PISO somado das pecas da maquina = {sum(nossas.values())} "
         f"(n={len(nossas)}) | inscritos={insc}")
    nota(f"{canal}: {conversao.relato_por_mil(canal, insc, nossas.values())}")
    for d in doentes(itens):
        aviso(f"{canal}: FORA de processed — {d}")
    if div and not forma:
        aviso(f"{canal}: os divergentes NAO compartilham a forma do 708 — a "
              f"hipotese da replica por chamada nao se aplica a esta rodada")


def main() -> int:
    cru = os.environ.get("YT_OAUTH_JSON") or ""
    if not cru:
        aviso("sem YT_OAUTH_JSON nao ha token, e sem token nao ha medicao")
        return 0
    mapa = desembrulha(cru)
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    corpus = {t.strip().casefold() for t in json.load(
        open(os.path.join(raiz, "fabrica/corpus_publicados.json")))["titulos"]}
    nota(f"corpus: {len(corpus)} titulos")

    ruim = 0
    for canal in CANAIS:
        cfg = mapa.get(canal)
        if not cfg:
            aviso(f"{canal}: FORA do YT_OAUTH_JSON")
            ruim += 1
            continue
        try:
            mede_canal(canal, cfg, corpus)
        except urllib.error.HTTPError as e:
            # 665: chamada que falhou NAO vira total menor em silencio.
            aviso(f"{canal}: HTTP {e.code} — leitura ABORTADA, nao ha numero "
                  f"deste canal nesta rodada")
            ruim += 1
        except Exception as e:                            # noqa: BLE001
            aviso(f"{canal}: {type(e).__name__} — leitura ABORTADA")
            ruim += 1
    if ruim:
        aviso(f"{ruim} de {len(CANAIS)} canais sem leitura nesta rodada")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
