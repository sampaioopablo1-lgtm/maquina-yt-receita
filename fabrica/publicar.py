#!/usr/bin/env python3
"""Publica um pacote no YouTube pela ROTA PROPRIA e fecha os passos de Studio.

Existe porque o que publicou os pacotes de 2026-08-11 era codigo solto dentro de
uma sessao: a cada disparo eu reescrevia o mesmo `videos.insert` resumable, e o
que estava certo num pacote nao estava no seguinte. Regra 'o que vive so no
sandbox esta perdido' — entao mora aqui.

Faz, nesta ordem (a ordem importa e esta medida):

  1. SHORT primeiro. Em canal frio o feed de Shorts entrega e o de longos nao:
     4 shorts entre 1,7 e 17,9 views/hora contra 4 longos entre 0 e 0,2.
     O short leva o link do longo na descricao, nunca o contrario.
  2. LONGO, com a descricao ja apontando para o short publicado.
  3. thumbnails/set — 403 aqui NAO e defeito do codigo: e canal sem verificacao
     por telefone. O upload do video continua valendo, so a capa fica pendente.
  4. captions.insert (multipart) — 409 e SUCESSO: o video ja tem faixa naquele
     idioma. Foi o erro que fez a regra 'nenhum video tem legenda' parecer viva
     depois de resolvida.
  5. playlistItems.insert — playlist por canal levanta sessao, e uma chamada.

Credencial: config.yt_token_<slug> no Supabase (nunca so no sandbox, que
recicla). O access_token de 1h e descartavel; o refresh_token e o que importa.

Uso:
    python3 fabrica/publicar.py <spec.json> --canal <slug> [--playlist <id>]
"""
import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"


def _ctx():
    """Um proxy que re-termina TLS quebra o edge-tts e tambem estas chamadas se
    o CA nao estiver no contexto. SSL_CERT_FILE cobre o caso sem desligar
    verificacao — que nao se desliga em nenhuma hipotese."""
    ca = os.environ.get("SSL_CERT_FILE")
    return ssl.create_default_context(cafile=ca) if ca else None


def _req(url, data=None, method="GET", headers=None, timeout=60):
    r = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    return urllib.request.urlopen(r, timeout=timeout, context=_ctx())


def token_do_canal(slug, sb_url, sb_key):
    """Le config.yt_token_<slug>. A tabela tem RLS para service_role, entao a
    chave anon nao serve aqui — e isso e proposital."""
    url = f"{sb_url}/rest/v1/config?chave=eq.yt_token_{slug}&select=valor"
    r = _req(url, headers={"Authorization": f"Bearer {sb_key}", "apikey": sb_key})
    linhas = json.load(r)
    if not linhas:
        raise SystemExit(f"sem credencial para {slug}: grave config.yt_token_{slug}")
    return linhas[0]["valor"]


def access_token(tok):
    data = urllib.parse.urlencode({
        "client_id": tok["client_id"], "client_secret": tok["client_secret"],
        "refresh_token": tok["refresh_token"], "grant_type": "refresh_token",
    }).encode()
    return json.load(_req(tok["token_uri"], data=data, method="POST"))["access_token"]


def subir(acc, caminho, meta):
    """videos.insert resumable. O corpo vai em JSON e o binario num PUT
    separado — mandar tudo junto estoura o limite de request simples."""
    corpo = json.dumps(meta).encode()
    tam = os.path.getsize(caminho)
    loc = _req(
        f"{UPLOAD}/videos?uploadType=resumable&part=snippet,status",
        data=corpo, method="POST",
        headers={"Authorization": "Bearer " + acc,
                 "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Length": str(tam),
                 "X-Upload-Content-Type": "video/mp4"},
    ).headers["Location"]
    with open(caminho, "rb") as f:
        binario = f.read()
    r = _req(loc, data=binario, method="PUT", timeout=900,
             headers={"Authorization": "Bearer " + acc,
                      "Content-Type": "video/mp4", "Content-Length": str(tam)})
    return json.load(r)["id"]


def thumbnail(acc, video_id, caminho):
    if not (caminho and os.path.exists(caminho)):
        return "sem arquivo"
    try:
        with open(caminho, "rb") as f:
            _req(f"{UPLOAD}/thumbnails/set?videoId={video_id}", data=f.read(),
                 method="POST", timeout=120,
                 headers={"Authorization": "Bearer " + acc, "Content-Type": "image/png"})
        return "ok"
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return "403: canal sem verificacao por telefone (youtube.com/verify)"
        return f"{e.code}: {e.read().decode()[:120]}"


def legenda(acc, video_id, caminho, idioma):
    """409 significa que a faixa daquele idioma ja existe — sucesso, nao falha."""
    if not (caminho and os.path.exists(caminho)):
        return "sem arquivo"
    with open(caminho, "rb") as f:
        srt = f.read()
    meta = json.dumps({"snippet": {"videoId": video_id, "language": idioma,
                                   "name": "", "isDraft": False}}).encode()
    bnd = uuid.uuid4().hex.encode()
    corpo = (b"--" + bnd + b"\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n" + meta +
             b"\r\n--" + bnd + b"\r\nContent-Type: application/octet-stream\r\n\r\n" + srt +
             b"\r\n--" + bnd + b"--\r\n")
    try:
        _req(f"{UPLOAD}/captions?part=snippet&uploadType=multipart", data=corpo,
             method="POST", timeout=180,
             headers={"Authorization": "Bearer " + acc,
                      "Content-Type": b"multipart/related; boundary=" + bnd})
        return "ok"
    except urllib.error.HTTPError as e:
        return "ja existia (409)" if e.code == 409 else f"{e.code}: {e.read().decode()[:120]}"


def na_playlist(acc, playlist_id, video_id):
    if not playlist_id:
        return "sem playlist"
    corpo = json.dumps({"snippet": {"playlistId": playlist_id,
                                    "resourceId": {"kind": "youtube#video",
                                                   "videoId": video_id}}}).encode()
    try:
        _req(f"{API}/playlistItems?part=snippet", data=corpo, method="POST",
             headers={"Authorization": "Bearer " + acc,
                      "Content-Type": "application/json; charset=UTF-8"})
        return "ok"
    except urllib.error.HTTPError as e:
        return f"{e.code}: {e.read().decode()[:120]}"


def orcamento_tags(tags, limite=480):
    """O limite de 500 do YouTube conta tag com espaco ENTRE ASPAS: custa
    len+2. Somar so os caracteres aprova lista que a API rejeita."""
    total, mantidas = 0, []
    for t in tags:
        custo = len(t) + (2 if " " in t else 0)
        if total + custo > limite:
            break
        total += custo
        mantidas.append(t)
    return mantidas, total


def meta_video(titulo, descricao, tags, idioma, publico=True):
    mantidas, _ = orcamento_tags(tags)
    return {
        "snippet": {"title": titulo[:100], "description": descricao, "tags": mantidas,
                    "categoryId": "27", "defaultLanguage": idioma,
                    "defaultAudioLanguage": idioma},
        # containsSyntheticMedia e obrigatorio e nao reduz alcance: a politica do
        # YouTube pune quem NAO divulga, nao quem divulga.
        "status": {"privacyStatus": "public" if publico else "private",
                   "selfDeclaredMadeForKids": False, "containsSyntheticMedia": True},
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("spec")
    p.add_argument("--canal", required=True)
    p.add_argument("--playlist", default=None)
    p.add_argument("--dir", default=None, help="workdir (padrao: /tmp/f/<pacote>)")
    args = p.parse_args()

    sb_url = os.environ["SUPABASE_URL"].rstrip("/")
    sb_key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    sp = json.load(open(args.spec))
    d = args.dir or f"/tmp/f/{sp.get('pacote') or sp['slug']}"
    idioma = sp.get("idioma") or "en"
    cp = sp["copy"]

    acc = access_token(token_do_canal(args.canal, sb_url, sb_key))
    saida = {}

    # 1) SHORT primeiro — e ele que recebe distribuicao em canal frio.
    curto = os.path.join(d, "short.mp4")
    if os.path.exists(curto):
        sid = subir(acc, curto, meta_video(
            cp.get("short_titulo", cp["titulo"]), cp.get("short_descricao", ""),
            cp.get("short_tags", cp.get("tags", []))[:8], idioma))
        saida["short"] = sid
        print("SHORT:", sid, "| playlist:", na_playlist(acc, args.playlist, sid))

    # 2) LONGO, ja apontando para o short.
    longo = os.path.join(d, "video.mp4")
    if os.path.exists(longo):
        desc = cp["descricao"]
        if saida.get("short"):
            desc += f"\n\nVersao curta: https://youtube.com/shorts/{saida['short']}"
        vid = subir(acc, longo, meta_video(cp["titulo"], desc, cp.get("tags", []), idioma))
        saida["longo"] = vid
        print("LONGO:", vid)
        print("  thumbnail:", thumbnail(acc, vid, os.path.join(d, "thumbnail.png")))
        print("  legenda  :", legenda(acc, vid, os.path.join(d, "legendas.srt"), idioma))
        print("  playlist :", na_playlist(acc, args.playlist, vid))

    print(json.dumps(saida))
    return saida


if __name__ == "__main__":
    main()
