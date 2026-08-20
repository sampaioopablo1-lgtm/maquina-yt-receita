#!/usr/bin/env python3
"""Diz QUAIS canais precisam de reautorizacao — e so esses.

Reautorizar e um clique humano por canal, e treze cliques e o tipo de tarefa
que nao acontece. Este script existe para reduzir treze a "os que de fato
faltam", e para provar quais sao em vez de supor.

COMO SABE: o endpoint de refresh do Google devolve, junto com o access_token,
o campo `scope` com o que aquele refresh_token realmente carrega. Nao e
inferencia — e o proprio Google dizendo. Um refresh nao consome nada e nao
invalida o token.

O que NAO da para evitar: o consentimento em si. Os treze canais usam um unico
client OAuth, mas o token do YouTube fica preso ao canal escolhido na tela, e
`captions.insert` exige token do canal dono do video. Nao existe token que
sirva para todos. O que da para fazer e o que este script permite: autorizar
so quando o canal for publicar, um por vez, em vez de treze de uma vez.

Uso (precisa de SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY no ambiente):
    python3 scripts/auditar_escopos.py
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

FORCE_SSL = "https://www.googleapis.com/auth/youtube.force-ssl"
SB = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]


def config_tokens():
    url = f"{SB}/rest/v1/config?chave=like.yt_token_*&select=chave,valor"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
    linhas = json.load(urllib.request.urlopen(req, timeout=60))
    return {l["chave"].replace("yt_token_", ""): l["valor"] for l in linhas}


def escopos_de(tok):
    """Refresh so para ler o campo `scope` da resposta."""
    d = urllib.parse.urlencode({
        "client_id": tok["client_id"], "client_secret": tok["client_secret"],
        "refresh_token": tok["refresh_token"], "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(tok.get("token_uri", "https://oauth2.googleapis.com/token"),
                                 data=d, method="POST")
    r = json.load(urllib.request.urlopen(req, timeout=60))
    return r.get("scope", ""), r.get("access_token")


def canal_de(access_token):
    """Nunca assumir de quem e o token: perguntar."""
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
        headers={"Authorization": "Bearer " + access_token})
    itens = json.load(urllib.request.urlopen(req, timeout=60)).get("items", [])
    return itens[0]["snippet"]["title"] if itens else "(sem canal)"


def marcar(vivos: dict) -> None:
    """Escreve token_vivo/token_testado_em em config.yt_token_<slug>.

    Le e reescreve o jsonb inteiro de proposito: PATCH numa coluna jsonb
    substitui o valor todo, e mandar so os dois campos apagaria o
    refresh_token. Ler antes custa uma chamada e evita destruir a credencial
    que este script existe para auditar.
    """
    from datetime import datetime, timezone
    agora = datetime.now(timezone.utc).isoformat()
    atuais = config_tokens()
    for slug, vivo in sorted(vivos.items()):
        valor = dict(atuais.get(slug) or {})
        if not valor:
            continue
        valor["token_vivo"] = vivo
        valor["token_testado_em"] = agora
        url = (f"{SB}/rest/v1/config?chave=eq."
               f"{urllib.parse.quote('yt_token_' + slug, safe='')}")
        req = urllib.request.Request(
            url, data=json.dumps({"valor": valor}).encode(), method="PATCH",
            headers={"apikey": KEY, "Authorization": f"Bearer {KEY}",
                     "Content-Type": "application/json",
                     "Prefer": "return=minimal"})
        try:
            urllib.request.urlopen(req, timeout=30)
        except Exception as e:
            # Auditoria que falha ao gravar ainda serve pelo log. Derrubar o
            # script aqui perderia o relatorio inteiro por causa do rodape.
            print(f"  (nao consegui marcar {slug}: {type(e).__name__}: {e})")


def main():
    faltam, ok, quebrados = [], [], []
    for slug, tok in sorted(config_tokens().items()):
        try:
            escopos, at = escopos_de(tok)
            titulo = canal_de(at)
            if FORCE_SSL in escopos:
                ok.append((slug, titulo))
            else:
                faltam.append((slug, titulo))
        except urllib.error.HTTPError as e:
            quebrados.append((slug, f"HTTP {e.code}: {e.read().decode()[:120]}"))
        except Exception as e:
            quebrados.append((slug, f"{type(e).__name__}: {e}"))

    print(f"\nCOM force-ssl ({len(ok)}) — publicam com legenda:")
    for s, t in ok:
        print(f"  {s:20} {t}")
    print(f"\nSEM force-ssl ({len(faltam)}) — publicam SEM legenda ate reautorizar:")
    for s, t in faltam:
        print(f"  {s:20} {t}")
    if quebrados:
        print(f"\nTOKEN QUEBRADO ({len(quebrados)}) — nao publicam de jeito nenhum:")
        for s, e in quebrados:
            print(f"  {s:20} {e}")

    if faltam:
        print("\nLinks so dos que faltam:")
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from links_reauth import link
        for s, _ in faltam:
            print(f"\n### {s}\n{link(s)}")

    json.dump({"com_force_ssl": [s for s, _ in ok],
               "sem_force_ssl": [s for s, _ in faltam],
               "quebrados": [s for s, _ in quebrados]},
              open("escopos.json", "w"), indent=1)

    # O resultado volta para o banco, e nao so para o log do Actions.
    #
    # Em 20/08/2026 a fila me entregou o sx-educacao como proximo da vez, eu
    # escrevi 78 cenas e so descobri o token morto no passo de conferencia do
    # render. A fila nao tinha como saber: ela le `canais` e `videos`, e saude
    # de token nao mora em nenhum dos dois. Gravar aqui e o que permite a
    # `v_maquina_fila` deixar canal sem rota de publicacao por ultimo.
    #
    # Grava o RESULTADO, nunca o veredito humano: `token_vivo` diz se o refresh
    # respondeu agora, e `token_testado_em` diz quando. Sem a data o campo
    # envelhece calado e vira a mesma armadilha que ele existe para fechar.
    marcar({s: True for s, _ in ok} | {s: True for s, _ in faltam}
           | {s: False for s, _ in quebrados})


if __name__ == "__main__":
    main()
