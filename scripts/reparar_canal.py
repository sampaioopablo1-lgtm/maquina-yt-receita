"""Recarimba videos.canal a partir do dono real do video no YouTube.

Por que existe: `canal` foi adicionado a tabela so em 12/08/2026, entao as
linhas antigas nasceram sem ele — e um sync rodando codigo pre-a864060 apaga
o campo de novo, porque aquela versao mandava `canal: None` e o upsert
sobrescrevia. Aconteceu duas vezes no mesmo dia; da segunda, o passo
`if: always()` de um run CANCELADO ressuscitou a versao antiga e zerou o canal
de 17 linhas publicadas.

Sem `canal`, a v_maquina_rodizio nao ve o video, o canal parece parado ha mais
tempo do que esta e o cron manda producao para o lugar errado. O teto por canal
da compliance tambem para de separar um canal dos outros doze.

O reparo NAO adivinha pelo prefixo do slug. Pergunta a fonte autoritativa: o
`snippet.channelId` de cada video, cruzado com o `id` do canal de cada token.
Slug e convencao nossa e ja divergiu do dono real (setiap-level publicou
videos com slug generico gerado do titulo).

Uso:
    python scripts/reparar_canal.py            # mostra o que faria
    python scripts/reparar_canal.py --aplicar  # grava

Precisa de SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY no ambiente.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request

CLIENT_ID = "777159180424-p853u21ksnlhgjd4s9d2f5bum9hllumo.apps.googleusercontent.com"
# videos.list aceita 50 ids por chamada.
LOTE = 50


def _req(url: str, headers: dict, dados: bytes | None = None, metodo: str = "GET"):
    req = urllib.request.Request(url, data=dados, method=metodo)
    for k, v in headers.items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=60) as r:
        corpo = r.read().decode()
    return json.loads(corpo) if corpo.strip() else None


def _supabase() -> tuple[str, dict]:
    url = os.environ["SUPABASE_URL"].rstrip("/")
    chave = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    return url, {
        "apikey": chave,
        "Authorization": f"Bearer {chave}",
        "Content-Type": "application/json",
    }


def acesso(refresh_token: str, client_secret: str) -> str:
    corpo = urllib.parse.urlencode(
        {
            "client_id": CLIENT_ID,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
    ).encode()
    return _req(
        "https://oauth2.googleapis.com/token", {}, corpo, "POST"
    )["access_token"]


def donos() -> tuple[dict[str, str], str]:
    """{channelId: slug} e um access_token qualquer para consultar videos."""
    url, h = _supabase()
    linhas = _req(f"{url}/rest/v1/config?chave=like.yt_token_*&select=chave,valor", h)
    mapa, token_qualquer = {}, ""
    for linha in linhas or []:
        valor = linha["valor"]
        if not valor.get("refresh_token"):
            continue
        slug = linha["chave"].removeprefix("yt_token_")
        try:
            tok = acesso(valor["refresh_token"], valor["client_secret"])
            canal = _req(
                "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true",
                {"Authorization": f"Bearer {tok}"},
            )
            mapa[canal["items"][0]["id"]] = slug
            token_qualquer = tok
        except Exception as e:
            print(f"  aviso: {slug} nao respondeu ({e})", file=sys.stderr)
    return mapa, token_qualquer


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    url, h = _supabase()

    orfas = _req(
        f"{url}/rest/v1/videos?canal=is.null&youtube_id=not.is.null"
        "&select=slug,youtube_id",
        h,
    ) or []
    if not orfas:
        print("Nenhuma linha publicada sem canal.")
        return 0
    print(f"{len(orfas)} linha(s) publicada(s) sem canal.")

    mapa, tok = donos()
    if not tok:
        print("Nenhum token utilizavel — nada a fazer.", file=sys.stderr)
        return 1

    por_id = {o["youtube_id"]: o["slug"] for o in orfas}
    ids = list(por_id)
    achados: dict[str, str] = {}
    for i in range(0, len(ids), LOTE):
        pedaco = ids[i : i + LOTE]
        r = _req(
            "https://www.googleapis.com/youtube/v3/videos?part=snippet&id="
            + ",".join(pedaco),
            {"Authorization": f"Bearer {tok}"},
        )
        for item in (r or {}).get("items", []):
            slug_canal = mapa.get(item["snippet"]["channelId"])
            if slug_canal:
                achados[item["id"]] = slug_canal

    for yt_id, slug in sorted(por_id.items()):
        print(f"  {yt_id:<14} {slug[:44]:<46} -> {achados.get(yt_id, 'DESCONHECIDO')}")

    perdidos = [i for i in ids if i not in achados]
    if perdidos:
        print(
            f"\n{len(perdidos)} video(s) sem dono identificado — apagados do "
            f"YouTube ou de canal fora da frota: {', '.join(perdidos)}"
        )

    if not aplicar:
        print("\nNada gravado. Rode com --aplicar para escrever.")
        return 0

    for yt_id, slug_canal in achados.items():
        _req(
            f"{url}/rest/v1/videos?youtube_id=eq.{yt_id}&canal=is.null",
            {**h, "Prefer": "return=minimal"},
            json.dumps({"canal": slug_canal}).encode(),
            "PATCH",
        )
    print(f"\n{len(achados)} linha(s) recarimbada(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
