#!/usr/bin/env python3
"""Autorizacao e vigilancia dos tokens do YouTube, em lote.

POR QUE ESTE ARQUIVO EXISTE (19/08/2026): o dono reautorizou canais tres
vezes em dois dias, um a um, colando uma URL por vez. A causa raiz era o
app OAuth em modo Testing (refresh token morre em 7 dias, aprendizado 303),
e ele ja foi publicado — mas os tokens emitidos ANTES da publicacao seguem
morrendo no proprio marco de 7 dias, em cascata: 9 dos 12 morreram na
madrugada de 19/08.

Entao o trabalho manual restante e UMA ultima rodada. Este modulo faz essa
rodada custar o minimo possivel e, principalmente, faz o problema nunca
mais chegar como surpresa:

  link      um link de autorizacao (o mesmo para todos os canais — o que
            muda e a conta de marca escolhida na tela do Google)
  trocar    le VARIAS URLs de callback de uma vez (uma por linha, coladas
            juntas), troca cada codigo, DESCOBRE o canal pela API e grava
            em config.yt_token_<slug>. Nove interacoes viram uma.
  vigiar    testa todos os tokens e diz quais estao vivos, mortos e quais
            vencem em breve. Sai != 0 se algum estiver morto.

Nada aqui inventa o canal: o slug vem de canais.youtube_channel_id
comparado com o channels.list(mine=true) do proprio token — o mesmo
cuidado que evitou um pacote inteiro no canal errado em 14/08.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

ESCOPOS = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.upload",
]
REDIRECT = "http://localhost"
TOKEN_URI = "https://oauth2.googleapis.com/token"


def _env(*nomes):
    for n in nomes:
        v = os.environ.get(n)
        if v:
            return v.rstrip("/")
    return None


def _sb():
    sb, sk = _env("SUPABASE_URL", "SB"), _env("SUPABASE_SERVICE_ROLE_KEY", "KEY")
    if not (sb and sk):
        sys.exit("AMBIENTE: faltam SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY")
    return sb, sk


def _get(url, sk):
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {sk}", "apikey": sk})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _patch(url, sk, corpo):
    req = urllib.request.Request(
        url, data=json.dumps(corpo).encode(), method="PATCH",
        headers={"Authorization": f"Bearer {sk}", "apikey": sk,
                 "Content-Type": "application/json", "Prefer": "return=minimal"})
    urllib.request.urlopen(req, timeout=30).read()


def tokens_do_banco(sb, sk):
    linhas = _get(f"{sb}/rest/v1/config?chave=like.yt_token_*&select=chave,valor", sk)
    return {l["chave"].replace("yt_token_", ""): l["valor"] for l in linhas
            if isinstance(l.get("valor"), dict) and l["valor"].get("refresh_token")}


def canais_do_banco(sb, sk):
    linhas = _get(f"{sb}/rest/v1/canais?select=slug,youtube_channel_id", sk)
    return {c["youtube_channel_id"]: c["slug"] for c in linhas
            if c.get("youtube_channel_id")}


def refrescar(tok):
    """(access_token, None) ou (None, motivo)."""
    dados = urllib.parse.urlencode({
        "client_id": tok["client_id"], "client_secret": tok["client_secret"],
        "grant_type": "refresh_token", "refresh_token": tok["refresh_token"],
    }).encode()
    try:
        with urllib.request.urlopen(
                urllib.request.Request(TOKEN_URI, data=dados, method="POST"),
                timeout=30) as r:
            return json.load(r)["access_token"], None
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace")
        try:
            erro = json.loads(corpo).get("error_description") or json.loads(corpo).get("error")
        except Exception:
            erro = corpo[:120]
        return None, f"{e.code} {erro}"
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def canal_do_token(access):
    """Pergunta a API de que canal e este token — nunca assume."""
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
        headers={"Authorization": f"Bearer {access}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        itens = json.load(r).get("items", [])
    if not itens:
        return None, None
    return itens[0]["id"], itens[0]["snippet"]["title"]


# ------------------------------------------------------------------ comandos

def cmd_link(_):
    q = urllib.parse.urlencode({
        "client_id": os.environ.get("YT_CLIENT_ID", ""),
        "redirect_uri": REDIRECT, "response_type": "code",
        "access_type": "offline", "prompt": "consent",
        "scope": " ".join(ESCOPOS),
    })
    print(f"https://accounts.google.com/o/oauth2/v2/auth?{q}")
    print("\nAutorize UMA VEZ POR CANAL (escolhendo a conta de marca de cada um),")
    print("junte todas as URLs de localhost e mande de uma vez:")
    print("  python3 fabrica/tokens.py trocar < urls.txt")
    return 0


def cmd_trocar(_):
    """Le URLs de callback do stdin, uma por linha, e grava todos os tokens."""
    sb, sk = _sb()
    por_channel = canais_do_banco(sb, sk)
    modelo = next(iter(tokens_do_banco(sb, sk).values()), None)
    if not modelo:
        sys.exit("nenhum token no banco para servir de modelo (client_id/secret)")
    cid, cs = modelo["client_id"], modelo["client_secret"]

    urls = [l.strip() for l in sys.stdin.read().splitlines() if l.strip()]
    if not urls:
        sys.exit("nada no stdin — cole as URLs de localhost, uma por linha")
    falhas = 0
    for url in urls:
        codigo = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get("code", [None])[0]
        if not codigo:
            print(f"  IGNORADA (sem ?code=): {url[:60]}")
            falhas += 1
            continue
        dados = urllib.parse.urlencode({
            "client_id": cid, "client_secret": cs, "grant_type": "authorization_code",
            "redirect_uri": REDIRECT, "code": codigo}).encode()
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(TOKEN_URI, data=dados, method="POST"),
                    timeout=30) as r:
                novo = json.load(r)
        except urllib.error.HTTPError as e:
            print(f"  FALHOU a troca ({e.code}): codigo expirado ou ja usado — "
                  f"autorize de novo esse canal")
            falhas += 1
            continue
        acc, rt = novo.get("access_token"), novo.get("refresh_token")
        if not rt:
            print("  FALHOU: o Google nao devolveu refresh_token (falta prompt=consent)")
            falhas += 1
            continue
        ch_id, titulo = canal_do_token(acc)
        slug = por_channel.get(ch_id)
        if not slug:
            print(f"  SEM SLUG: canal '{titulo}' ({ch_id}) nao esta em "
                  f"canais.youtube_channel_id — token NAO gravado")
            falhas += 1
            continue
        corpo = {"valor": {"type": "authorized_user", "scopes": ESCOPOS,
                           "client_id": cid, "token_uri": TOKEN_URI,
                           "client_secret": cs, "refresh_token": rt}}
        _patch(f"{sb}/rest/v1/config?chave=eq.yt_token_{slug}", sk, corpo)
        print(f"  OK {slug:20} <- {titulo}")
    print(f"\n{len(urls) - falhas}/{len(urls)} tokens gravados")
    return 1 if falhas else 0


def cmd_vigiar(_):
    """Testa todos. O silencio de um token morto e o que quebra a producao."""
    sb, sk = _sb()
    tokens = tokens_do_banco(sb, sk)
    vivos, mortos = [], []
    for slug, tok in sorted(tokens.items()):
        acc, motivo = refrescar(tok)
        if acc:
            vivos.append(slug)
            print(f"  VIVO  {slug}")
        else:
            mortos.append(slug)
            print(f"  MORTO {slug}: {motivo}")
    print(f"\n{len(vivos)} vivos, {len(mortos)} mortos, de {len(tokens)}")
    if mortos:
        print("Reautorize estes: " + ", ".join(mortos))
        print("  python3 fabrica/tokens.py link")
    return 1 if mortos else 0


COMANDOS = {"link": cmd_link, "trocar": cmd_trocar, "vigiar": cmd_vigiar}


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd not in COMANDOS:
        sys.exit(f"uso: python3 fabrica/tokens.py [{'|'.join(COMANDOS)}]")
    return COMANDOS[cmd](sys.argv[2:])


if __name__ == "__main__":
    raise SystemExit(main())
