#!/usr/bin/env python3
"""Cada video publicado esta no canal que o banco diz que esta?

Existe por um caso medido em 14/08/2026: o pacote resep-naik-level-002 inteiro
— longo le6IBDH7u6M e short IdcluUKbwJ4 — foi publicado no canal
UCf4-ZFoZQWKJotZNdi4Yl7w (Setiap Level) e nao no UCjxE5J3V0XNThBfwaznihDA
(Resep Naik Level), que e o registrado. Auditando os 42 publicados, exatamente
estes dois estavam fora do lugar.

POR QUE NENHUMA TRAVA PEGAVA. Quem escolhe o canal de destino nao e a spec nem
o publicar.py — e o PERFIL da Upload-Post. A spec declara slug, idioma e voz, e
todos os tres estavam certos; o video simplesmente caiu noutra caixa. O
publicar.py recusa republicacao e resolve idioma, mas nunca pergunta onde o
video foi parar depois de subir.

E O DISFARCE E O PIOR POSSIVEL: nao aparece como erro. Aparece como conteudo
que nao performa. O longo marcou 0,0 views/dia em 8,3 dias contra mediana de
38,0 no grupo de pares — e sem esta conferencia a leitura obvia seria "a pauta
nao pegou", que levaria a reescrever um roteiro que estava certo.

Alem disso a contagem de estoque mente: `orquestra.py` conta longos pela tabela
`videos`, entao o resep-naik-level aparecia com um longo no ar quando o canal
proprio tem zero.

Uso:
    python3 fabrica/auditoria_canal.py            # audita todos
    python3 fabrica/auditoria_canal.py <slug>     # so um canal

Precisa de SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY. O token do YouTube sai de
config.yt_token_<slug>, pelo mesmo caminho que o publicar.py usa — a leitura de
credencial nao e reescrita aqui.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

from publicar import API, _req  # noqa: E402


def _sb(caminho, sb_url, sb_key):
    return json.load(_req(f"{sb_url}/rest/v1/{caminho}",
                          headers={"Authorization": f"Bearer {sb_key}",
                                   "apikey": sb_key}))


def canais_registrados(sb_url, sb_key):
    linhas = _sb("canais?select=slug,youtube_channel_id", sb_url, sb_key)
    return {l["slug"]: l["youtube_channel_id"] for l in linhas
            if l.get("youtube_channel_id")}


def publicados(sb_url, sb_key, slug=None):
    q = "videos?youtube_id=not.is.null&select=canal,pacote,formato,youtube_id"
    if slug:
        q += f"&canal=eq.{urllib.parse.quote(slug, safe='')}"
    return _sb(q, sb_url, sb_key)


def canal_real(acc, ids):
    """channelId de cada video, em lotes de 50 (o teto do videos.list)."""
    achados = {}
    for i in range(0, len(ids), 50):
        lote = ids[i:i + 50]
        r = json.load(_req(f"{API}/videos?part=snippet&id={','.join(lote)}",
                           headers={"Authorization": "Bearer " + acc}))
        for it in r.get("items", []):
            achados[it["id"]] = (it["snippet"]["channelId"],
                                 it["snippet"]["channelTitle"])
    return achados


def audita(sb_url, sb_key, slug=None):
    registro = canais_registrados(sb_url, sb_key)
    vids = publicados(sb_url, sb_key, slug)
    de_canal = {cid: s for s, cid in registro.items()}

    erradas, ausentes, ok = [], [], 0
    por_canal = {}
    for v in vids:
        por_canal.setdefault(v["canal"], []).append(v)

    for canal, linhas in sorted(por_canal.items()):
        esperado = registro.get(canal)
        if not esperado:
            print(f"  {canal}: sem youtube_channel_id no banco — nao da para auditar",
                  file=sys.stderr)
            continue
        # O token de QUALQUER canal serve: videos.list e leitura publica. Este
        # comentario ja estava aqui, mas o codigo nao fazia o que ele promete:
        # usava so o token do proprio canal e morria em traceback cru se ele
        # estivesse morto. Com dez dos doze tokens mortos em 19/08/2026, a
        # auditoria parava no PRIMEIRO canal e nao auditava nada — e o que ela
        # procura (video no canal errado) nao aparece como falha em lugar
        # nenhum, so como pauta que nao pegou. Perder a conferencia em silencio
        # e pior que o traceback.
        acc = _algum_access_token(canal, sb_url, sb_key)
        if acc is None:
            print(f"  {canal}: nenhum token vivo na frota — nao da para auditar. "
                  f"Reautorize com `python3 fabrica/tokens.py link`.",
                  file=sys.stderr)
            continue
        reais = canal_real(acc, [l["youtube_id"] for l in linhas])
        for l in linhas:
            real = reais.get(l["youtube_id"])
            if real is None:
                ausentes.append(l)
            elif real[0] != esperado:
                erradas.append((l, real, de_canal.get(real[0], real[0])))
            else:
                ok += 1
    return ok, erradas, ausentes


_TOKENS: dict = {}          # slug -> access token, ou None se o refresh falhou


def _algum_access_token(preferido, sb_url, sb_key):
    """Access token de leitura: o do canal pedido, ou o de qualquer outro.

    `videos.list` e leitura publica, entao serve o token de QUALQUER canal da
    frota — a auditoria nao pode depender de um so. Cada refresh e feito no
    maximo uma vez por execucao (`_TOKENS`), entao auditar treze canais com um
    token vivo custa um refresh, nao treze.
    """
    import tokens as T

    if "_todos" not in _TOKENS:
        _TOKENS["_todos"] = T.tokens_do_banco(sb_url, sb_key)
    todos = _TOKENS["_todos"]

    def vivo(slug):
        if slug not in _TOKENS:
            _TOKENS[slug] = T.refrescar(todos[slug])[0]
        return _TOKENS[slug]

    if preferido in todos and vivo(preferido):
        return _TOKENS[preferido]
    for slug in sorted(k for k in todos if k != preferido):
        if vivo(slug):
            return _TOKENS[slug]
    return None


def ja_publicado_pelo_titulo(copys, sb_url, sb_key):
    """Quais destes copy.md do bucket descrevem um video que JA esta no ar.

    Cruza por TITULO, nunca por nome de pacote. Medido em 15/08/2026: o mesmo
    render vive no bucket sob DOIS nomes — o da spec (kolejny-poziom-002) e o
    da rodada (kp-plan-9233-20260811) — e `videos.pacote` guarda o segundo.
    Cruzando por nome, tres renders ja publicados apareceram como ineditos, e
    eu so nao publiquei as tres duplicatas porque li o copy.md antes de subir.

    O titulo e o que o espectador ve, entao e ele que decide se e o mesmo
    video. `copys` e uma lista de (nome_do_objeto, texto_do_copy_md) — quem
    chama baixa, porque listar o bucket exige service role no Storage e esta
    funcao nao inventa rota.
    """
    no_ar = {(l.get("titulo") or "").strip().casefold()
             for l in _sb("videos?youtube_id=not.is.null&select=titulo",
                          sb_url, sb_key)
             if l.get("titulo")}

    veredito = []
    for nome, texto in copys:
        m = re.search(r"^## +[^\n]*\n+(.+)$", texto, re.M)
        titulo = (m.group(1).strip() if m else "")
        veredito.append((nome, titulo, titulo.casefold() in no_ar))
    return veredito


def main() -> int:
    sb_url = os.environ["SUPABASE_URL"].rstrip("/")
    sb_key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    slug = sys.argv[1] if len(sys.argv) > 1 else None

    ok, erradas, ausentes = audita(sb_url, sb_key, slug)
    print(f"no canal certo: {ok}")
    for l, (cid, titulo), real_slug in erradas:
        print(f"CANAL ERRADO  {l['youtube_id']}  pacote={l['pacote']} "
              f"formato={l['formato']}")
        print(f"              registrado em {l['canal']}, esta em "
              f"{real_slug} ({titulo}, {cid})")
    for l in ausentes:
        print(f"AUSENTE       {l['youtube_id']}  pacote={l['pacote']} — a API nao "
              f"devolve o video (removido, privado ou bloqueado)")
    if erradas:
        print(f"\n-> {len(erradas)} video(s) no canal errado. Isso nao aparece como "
              f"falha em lugar nenhum: aparece como pauta que nao pegou.")
    return 1 if erradas else 0


if __name__ == "__main__":
    raise SystemExit(main())

