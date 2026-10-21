#!/usr/bin/env python3
"""CHAMA o relatorio de retencao. O construtor da query existia e ninguem o usava.

POR QUE ISTO EXISTE (21/10/2026). O `retencao.query_de_retencao` esta escrito
desde 16/10, com a forma lida na fonte PRIMARIA — `audienceWatchRatio` e
`relativeRetentionPerformance` sobre `elapsedVideoTimeRatio`, um video por
chamada. **Nenhum caminho da fabrica o chamava**, e e a classe dos layouts
mortos: codigo escrito que ninguem chama PARECE pronto e nao esta no ar.

E a razao escrita para nao o chamar era esta, no proprio modulo: *"Escopo:
`yt-analytics.readonly` ... Falta so o clique de consentimento (pendencia 1)."*
**Isso foi FALSIFICADO por medicao em 21/10:** o `yt-analytics.readonly` esta
CONCEDIDO no segredo `YT_TOKEN_JSON`, nos TRES canais (run 39556791145, pelo
`sonda_oauth` lendo os dois blobs). O que faltava nao era o clique — era a
chamada.

**O QUE ISTO NAO AFIRMA, e a ressalva e o ponto:** que a retencao volta. Escopo
concedido nao e prova de que o dado vem. Esta chamada e o discriminador, e ela
distingue tres respostas que viravam o mesmo silencio:

  * **403** — o escopo nao serve de fato (ou o canal nao e o do token);
  * **200 com linhas** — retencao de verdade, e aí o 693 ganha comparador;
  * **200 SEM linhas** — a API respondeu e nao havia dado naquela janela, o que
    **NAO e retencao zero**. E a familia de 17/10: instrumento que devolve vazio
    nao prova ausencia.

O que ela NUNCA faz: nao imprime refresh token, client_secret nem access token;
nao publica, nao apaga, nao altera video. Imprime metrica e id de canal, que
nao e segredo.

Uso: python3 fabrica/chama_retencao.py <canal> [video_id] [dias]
"""
from __future__ import annotations

import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import publicar as P          # noqa: E402  — DONO do token e do access_token
import retencao as R          # noqa: E402  — DONO da forma da query

RELATORIO = "https://youtubeanalytics.googleapis.com/v2/reports"
CANAIS = "https://www.googleapis.com/youtube/v3/channels"

# Janela padrao de leitura. Nao e limiar de producao: e so quanto passado pedir.
DIAS_PADRAO = 90


def nota(msg: str) -> None:
    print(f"::notice::{msg}")


def aviso(msg: str) -> None:
    print(f"::warning::{msg}")


def janela(dias: int = DIAS_PADRAO, hoje: datetime.date | None = None):
    """(inicio, fim) em ISO. A API recusa fim no futuro, logo o fim e HOJE."""
    fim = hoje or datetime.date.today()
    return (fim - datetime.timedelta(days=dias)).isoformat(), fim.isoformat()


def url_do_relatorio(video_id: str, inicio: str, fim: str) -> str:
    """A URL completa, com os parametros vindos do DONO da forma.

    Remontar a query aqui criaria o segundo dono dela — a assinatura que
    congelou a legenda — e ela foi lida na fonte primaria, nao inventada.
    """
    return RELATORIO + "?" + urllib.parse.urlencode(
        R.query_de_retencao(video_id, inicio, fim))


def _get(url: str, acc: str, timeout: int = 60):
    req = urllib.request.Request(
        url, headers={"Authorization": "Bearer " + acc})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def resumo(resposta: dict) -> dict:
    """Le as linhas pelo NOME da coluna, nunca pela posicao.

    `columnHeaders` existe justamente para isso, e payload montado a mao contra
    uma forma documentada e o que matou tres runs (718/729/738).

    `vazio=True` com `linhas=0` quer dizer "a API respondeu e nao havia dado" —
    e isso NAO e retencao zero.
    """
    cols = [c.get("name") for c in (resposta or {}).get("columnHeaders") or []]
    linhas = (resposta or {}).get("rows") or []
    saida = {"colunas": cols, "linhas": len(linhas), "vazio": not linhas,
             "ponto_inicial": None, "retencao_media": None,
             "desempenho_relativo_medio": None}
    if not linhas:
        return saida

    def coluna(nome):
        return cols.index(nome) if nome in cols else None

    i_r = coluna("audienceWatchRatio")
    i_p = coluna("relativeRetentionPerformance")

    def media(i):
        vals = [l[i] for l in linhas
                if i is not None and i < len(l) and isinstance(l[i], (int, float))]
        return round(sum(vals) / len(vals), 4) if vals else None

    saida["retencao_media"] = media(i_r)
    saida["desempenho_relativo_medio"] = media(i_p)
    if i_r is not None and linhas and i_r < len(linhas[0]):
        saida["ponto_inicial"] = linhas[0][i_r]
    return saida


def relato(res: dict) -> str:
    """O relato DIZ qual das tres respostas veio. Silencio nao e resposta."""
    if res.get("erro"):
        return ("RETENCAO: %s — isto NAO e 'retencao zero', e falha de LEITURA."
                % res["erro"])
    r = res["resumo"]
    if r["vazio"]:
        return ("RETENCAO: a API respondeu 200 e devolveu ZERO linhas na janela "
                "pedida. Isso NAO e retencao zero: e ausencia de LEITURA, e a "
                "peca pode ser nova demais ou ter poucas views para o "
                "relatorio. (17/10: instrumento que devolve vazio nao prova "
                "ausencia.)")
    return ("RETENCAO MEDIDA: %d pontos, retencao media %s, desempenho "
            "relativo medio %s (0 a 1, JA normalizado contra videos de duracao "
            "semelhante — e esse comparador que dispensa a linha de base de 109 "
            "pecas por braco do 693). Ponto inicial %s."
            % (r["linhas"], r["retencao_media"],
               r["desempenho_relativo_medio"], r["ponto_inicial"]))


def _erro_legivel(e: urllib.error.HTTPError) -> str:
    try:
        det = json.loads(e.read().decode("utf-8", "replace"))
        msg = (det.get("error") or {}).get("message") or "(sem message)"
    except ValueError:
        msg = "(corpo ilegivel)"
    return f"HTTP {e.code} — {msg[:200]}"


def mede(canal: str, video_id: str, dias: int = DIAS_PADRAO) -> dict:
    """Devolve {canal_do_token, resumo} ou {erro}. Nunca levanta por HTTP."""
    sb = os.environ.get("SUPABASE_URL") or os.environ.get("SB")
    sk = (os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("KEY"))
    acc = P.access_token(P.token_do_canal(canal, sb, sk))
    fora: dict = {}
    try:
        dono = _get(CANAIS + "?part=id&mine=true", acc)
        ids = [i.get("id") for i in (dono.get("items") or [])]
        fora["canal_do_token"] = ids[0] if ids else None
    except urllib.error.HTTPError as e:
        fora["canal_do_token"] = "(nao lido: %s)" % _erro_legivel(e)
    inicio, fim = janela(dias)
    fora["janela"] = (inicio, fim)
    try:
        fora["resumo"] = resumo(_get(url_do_relatorio(video_id, inicio, fim),
                                     acc))
    except urllib.error.HTTPError as e:
        fora["erro"] = _erro_legivel(e)
    return fora


def _video_do_parque(canal: str) -> str | None:
    """A peca mais recente do canal que ja tem id publicado, lida do PARQUE.

    O parque (`docs/pendente/duracoes-a-medir.jsonl`) grava toda peca publicada
    com `youtube_id`, e ele e o dono dessa lista — contar de cabeca foi o erro
    de 19/10 as 05:4x.
    """
    import duracao_a_medir as DM

    linhas = [r for r in DM.carrega()
              if r.get("youtube_id") and (r.get("canal") == canal
                                          or r.get("pacote", "").startswith(canal))]
    if not linhas:
        return None
    return sorted(linhas, key=lambda r: r.get("em") or "")[-1]["youtube_id"]


def main() -> int:
    canal = sys.argv[1] if len(sys.argv) > 1 else "labtreinamento"
    video = sys.argv[2] if len(sys.argv) > 2 else (_video_do_parque(canal) or "")
    dias = int(sys.argv[3]) if len(sys.argv) > 3 else DIAS_PADRAO
    if not video:
        aviso(f"nenhuma peca de {canal} com youtube_id no parque — sem video "
              f"nao existe relatorio de retencao para pedir")
        return 0
    nota(f"pedindo retencao de {video} ({canal}), janela de {dias} dias")
    try:
        res = mede(canal, video, dias)
    except SystemExit as e:                  # credencial ausente, do dono
        aviso(f"sem credencial para {canal}: {e}")
        return 0
    nota(f"canal do token: {res.get('canal_do_token')}")
    nota(f"janela: {res.get('janela')}")
    if res.get("erro"):
        aviso(relato(res))
    else:
        nota(relato(res))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
