"""Diz quais canais da frota estao verificados por telefone — sem efeito colateral.

Por que existe: em 12/08/2026 o video iSby7u2ltf8 (nivel-do-jogo) subiu com
`hasCustomThumbnail: false`. Nao era bug de codigo — o `thumbnails().set`
respondeu 403 youtube.thumbnail/forbidden, "the authenticated user doesn't have
permissions to upload and set custom video thumbnails". Thumbnail custom exige
canal verificado, e cinco dos treze nao estavam.

O jeito obvio de descobrir isso — tentar setar uma thumbnail e ver se falha —
suja um video real quando da certo. `channels.list(part=status)` da a mesma
resposta lendo: `longUploadsStatus` e destravado pela MESMA verificacao por
telefone que libera thumbnail custom.

    allowed   -> verificado: thumbnail custom e upload acima de 15 min liberados
    eligible  -> pode verificar, mas NAO verificou: thumbnail custom da 403
    disallowed-> canal com restricao ativa

Uso:
    python scripts/auditar_verificacao.py

Le os tokens de config.yt_token_<slug> no Supabase (SUPABASE_URL e
SUPABASE_SERVICE_ROLE_KEY no ambiente).
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request

CLIENT_ID = "777159180424-p853u21ksnlhgjd4s9d2f5bum9hllumo.apps.googleusercontent.com"
EXPLICACAO = {
    "allowed": "verificado — thumbnail custom ok",
    "eligible": "NAO VERIFICADO — youtube.com/verify",
    "disallowed": "restricao ativa no canal",
}


def _get(url: str, headers: dict) -> object:
    req = urllib.request.Request(url)
    for k, v in headers.items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def tokens() -> list[tuple[str, str, str]]:
    url = os.environ["SUPABASE_URL"].rstrip("/")
    chave = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    linhas = _get(
        f"{url}/rest/v1/config?chave=like.yt_token_*&select=chave,valor",
        {"apikey": chave, "Authorization": f"Bearer {chave}"},
    )
    saida = []
    for linha in linhas:  # type: ignore[union-attr]
        valor = linha["valor"]
        if valor.get("refresh_token"):
            saida.append(
                (
                    linha["chave"].removeprefix("yt_token_"),
                    valor["refresh_token"],
                    valor["client_secret"],
                )
            )
    return sorted(saida)


def acesso(refresh_token: str, client_secret: str) -> str:
    corpo = urllib.parse.urlencode(
        {
            "client_id": CLIENT_ID,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
    ).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=corpo)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["access_token"]


def main() -> int:
    # `nao_medidos` existe porque a ausencia de resposta NAO e resposta. Antes
    # deste contador o resumo somava apenas os `eligible`: com dez dos doze
    # tokens mortos em 19/08/2026, o script imprimia ERRO em dez linhas e
    # terminava com "0 canal(is) sem verificacao" e codigo 0 — atestado de
    # saude para uma frota que ele nao conseguiu medir. Mesmo defeito que
    # deixou a auditoria de canal auditar zero e ninguem perceber.
    #
    # `longUploadsStatus` so vale quando pedido com o token DO PROPRIO canal
    # (`mine=true`, que e o que este script faz). Com token de outro canal a
    # API devolve `longUploadsUnspecified`, que parece medida e nao e — por
    # isso qualquer valor fora dos tres conhecidos entra em nao_medidos.
    pendentes, verificados, nao_medidos = [], [], []
    print(f"{'canal':<20} {'estado':<11} {'inscr':>6} {'vids':>5}  observacao")
    print("-" * 78)
    for slug, rt, cs in tokens():
        try:
            tok = acesso(rt, cs)
            dados = _get(
                "https://www.googleapis.com/youtube/v3/channels"
                "?part=status,statistics&mine=true",
                {"Authorization": f"Bearer {tok}"},
            )
        except Exception as e:  # token revogado, canal sem permissao, rede
            nao_medidos.append((slug, str(e)[:60]))
            print(f"{slug:<20} {'NAO MEDIDO':<11} {'':>6} {'':>5}  {e}")
            continue
        item = (dados.get("items") or [{}])[0]  # type: ignore[union-attr]
        estado = item.get("status", {}).get("longUploadsStatus", "?")
        stats = item.get("statistics", {})
        if estado == "eligible":
            pendentes.append(slug)
        elif estado == "allowed":
            verificados.append(slug)
        else:
            nao_medidos.append((slug, f"estado inesperado: {estado}"))
        print(
            f"{slug:<20} {estado:<11} {stats.get('subscriberCount','?'):>6} "
            f"{stats.get('videoCount','?'):>5}  {EXPLICACAO.get(estado, '')}"
        )

    print(f"\n{len(verificados)} verificado(s), {len(pendentes)} sem verificacao, "
          f"{len(nao_medidos)} NAO medido(s).")
    if pendentes:
        print(
            f"\n{len(pendentes)} canal(is) sem verificacao: {', '.join(pendentes)}\n"
            "Entre com a conta de cada um em youtube.com/verify. Enquanto nao "
            "verificar, todo video desses canais sai com a thumbnail que o "
            "YouTube escolher, e o teto de duracao e 15 min."
        )
    if nao_medidos:
        print(
            f"\n{len(nao_medidos)} canal(is) que este relatorio NAO conseguiu medir "
            f"— pode haver canal sem verificacao escondido aqui:\n"
            + "\n".join(f"  {s}: {m}" for s, m in nao_medidos)
        )
    return 1 if (pendentes or nao_medidos) else 0


if __name__ == "__main__":
    sys.exit(main())
