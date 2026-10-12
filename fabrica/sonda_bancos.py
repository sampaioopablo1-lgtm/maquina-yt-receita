#!/usr/bin/env python3
"""Diz, do RUNNER, quais bancos de imagem abrem e quais pedem chave.

POR QUE ISTO EXISTE (12/10/2026). O dono pediu b-roll de banco aberto. A
pergunta que decide o desenho nao e qual banco e melhor — e qual deles o
runner alcanca, porque e no runner que o render acontece. Deste container os
nove voltam `000` (o proxy recusa no CONNECT), e concluir dai que "nao da"
seria o erro do §10: dizer impossivel sem medir onde a coisa roda.

A segunda pergunta e de LICENCA, e ela e mais importante que a primeira. Cada
banco aqui devolve, junto com a imagem, o campo que diz sob que licenca ela
esta e quem deve ser creditado. A sonda imprime esses campos para que o
coletor nasca ja obrigado a registrar procedencia — b-roll sem licenca
registrada e passivo, nao material.

NAO baixa midia, NAO publica, NAO gasta cota de video. So cabecalho, contagem
e os campos de licenca do primeiro resultado.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request

UA = "maquina-yt-receita/1.0 (sonda de disponibilidade; contato pelo repo)"
TERMO = "calendar"


def nota(msg: str) -> None:
    print(f"::notice::{msg}")


def aviso(msg: str) -> None:
    print(f"::warning::{msg}")


def pega(url: str, cab: dict | None = None) -> tuple[int, dict | None]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(cab or {})})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:                                    # noqa: BLE001
        print(f"  ({type(e).__name__})")
        return 0, None


def wikimedia() -> None:
    """Commons: SEM chave. A licenca vem em `extmetadata`."""
    u = ("https://commons.wikimedia.org/w/api.php?action=query&format=json"
         "&generator=search&gsrnamespace=6&gsrlimit=3"
         f"&gsrsearch={urllib.parse.quote(TERMO)}"
         "&prop=imageinfo&iiprop=url|extmetadata"
         "&iiextmetadatafilter=LicenseShortName|Artist|UsageTerms")
    st, d = pega(u)
    if st != 200 or not d:
        aviso(f"wikimedia commons: HTTP {st} — sem leitura")
        return
    paginas = list((d.get("query") or {}).get("pages", {}).values())
    nota(f"wikimedia commons: HTTP 200, SEM CHAVE, {len(paginas)} resultados")
    if paginas:
        ii = (paginas[0].get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata") or {}
        lic = (meta.get("LicenseShortName") or {}).get("value", "?")
        nota(f"  licenca do 1o: {lic}")


def nasa() -> None:
    """NASA Images: SEM chave. Dominio publico na maioria dos itens."""
    st, d = pega("https://images-api.nasa.gov/search?media_type=image&q="
                 + urllib.parse.quote(TERMO))
    if st != 200 or not d:
        aviso(f"nasa images: HTTP {st} — sem leitura")
        return
    itens = ((d.get("collection") or {}).get("items") or [])
    nota(f"nasa images: HTTP 200, SEM CHAVE, {len(itens)} resultados")


def openverse() -> None:
    """Openverse (Wikimedia Foundation): SEM chave para uso leve."""
    st, d = pega("https://api.openverse.org/v1/images/?page_size=3&q="
                 + urllib.parse.quote(TERMO))
    if st != 200 or not d:
        aviso(f"openverse: HTTP {st} — sem leitura (pode exigir registro)")
        return
    r = d.get("results") or []
    nota(f"openverse: HTTP 200, SEM CHAVE, {d.get('result_count')} no total")
    if r:
        nota(f"  licenca do 1o: {r[0].get('license')} "
             f"{r[0].get('license_version') or ''}")


def pexels() -> None:
    """Pexels: chave GRATUITA, obrigatoria. Video tambem."""
    k = os.environ.get("PEXELS_KEY") or ""
    if not k:
        nota("pexels: SEM a chave PEXELS_KEY no repo — nao sondado "
             "(a chave e gratuita em pexels.com/api)")
        return
    st, d = pega("https://api.pexels.com/v1/search?per_page=3&query="
                 + urllib.parse.quote(TERMO), {"Authorization": k})
    if st != 200 or not d:
        aviso(f"pexels: HTTP {st} — chave invalida ou bloqueio")
        return
    nota(f"pexels: HTTP 200, COM CHAVE, {d.get('total_results')} resultados")


def pixabay() -> None:
    """Pixabay: chave GRATUITA, obrigatoria."""
    k = os.environ.get("PIXABAY_KEY") or ""
    if not k:
        nota("pixabay: SEM a chave PIXABAY_KEY no repo — nao sondado "
             "(a chave e gratuita em pixabay.com/api/docs)")
        return
    st, d = pega(f"https://pixabay.com/api/?key={k}&per_page=3&q="
                 + urllib.parse.quote(TERMO))
    if st != 200 or not d:
        aviso(f"pixabay: HTTP {st} — chave invalida ou bloqueio")
        return
    nota(f"pixabay: HTTP 200, COM CHAVE, {d.get('totalHits')} resultados")


def main() -> int:
    nota(f"sondando com o termo '{TERMO}' — nenhuma midia e baixada")
    for f in (wikimedia, nasa, openverse, pexels, pixabay):
        try:
            f()
        except Exception as e:                                # noqa: BLE001
            aviso(f"{f.__name__}: {type(e).__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
