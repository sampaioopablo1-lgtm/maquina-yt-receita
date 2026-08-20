#!/usr/bin/env python3
"""Testa o token OAuth do canal ANTES de gastar render.

Existe por causa de 19/08/2026: o agla-level-004 renderizou 20 minutos, foi
entregue no Storage e so entao a publicacao descobriu que o refresh token
tinha morrido — 45 minutos DEPOIS de eu mesmo o ter testado vivo. Naquela
madrugada 9 dos 12 tokens morreram em cascata (aprendizado 303/304): os
emitidos enquanto o app OAuth ainda estava em modo Testing expiram no seu
proprio marco de 7 dias, um a um, sem aviso.

Falhar aqui custa 30 segundos e deixa a mensagem certa no log; falhar no
passo de publicacao custa o render inteiro e um pacote parado.

Desde 20/08/2026 ele confere mais que "o token vive". O epomeno-epipedo-008 foi
publicado e a legenda do longo levou 403 "permissions not sufficient", porque a
concessao real do Google nao tinha `youtube.force-ssl` — enquanto
`config.yt_token_epomeno-epipedo.scopes` a LISTAVA. Esse campo guarda o que foi
PEDIDO no fluxo de autorizacao, nao o que foi CONCEDIDO, e eu o li como prova de
permissao numa auditoria dos treze canais. Nao e prova.

A prova existe e e de graca: a resposta do refresh traz o campo `scope`, que e a
lista EFETIVA. Este arquivo le esse campo e exige force-ssl — sem ela o longo
sobe sem legenda, que nao e cosmetico em canal de idioma nao-ingles
(aprendizado 93).

O campo `scopes` do banco continua como esta, DE PROPOSITO. Eu cheguei a
escrever aqui um passo que o corrigia com a resposta do Google, e o desfiz antes
de rodar: `config.valor` e uma coluna jsonb unica, um PATCH nela substitui o
objeto INTEIRO, e dentro desse objeto mora o `refresh_token`. Consertar um campo
descritivo nao vale o risco de apagar a credencial dos treze canais. A saida
certa e nao confiar no campo — e e o que este arquivo faz agora, perguntando ao
Google toda vez em vez de ler o registro.

Uso: python3 fabrica/confere_token.py <canal>
Ambiente: SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY (ou SB/KEY).
"""
import json
import os
import sys
import urllib.parse
import urllib.request


def _env(*nomes):
    for n in nomes:
        v = os.environ.get(n)
        if v:
            return v.rstrip("/") if n.endswith("URL") or n == "SB" else v
    return None


def token_do_canal(canal, sb, sk):
    url = (f"{sb}/rest/v1/config?chave=eq."
           f"{urllib.parse.quote('yt_token_' + canal, safe='')}&select=valor")
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {sk}", "apikey": sk})
    with urllib.request.urlopen(req, timeout=30) as r:
        linhas = json.load(r)
    if not linhas:
        sys.exit(f"config.yt_token_{canal} nao existe no banco — o canal nunca "
                 f"foi autorizado. Peca o link de autorizacao ao Pablo.")
    return linhas[0]["valor"]


ESCOPOS_NECESSARIOS = {
    # captions.insert do longo. Sem ela o video sobe, e sobe MUDO para a busca.
    "https://www.googleapis.com/auth/youtube.force-ssl": (
        "enviar a faixa de legenda do longo"),
    # videos.insert.
    "https://www.googleapis.com/auth/youtube.upload": ("publicar o video"),
}


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python3 fabrica/confere_token.py <canal>")
    canal = sys.argv[1]
    sb = _env("SUPABASE_URL", "SB")
    sk = _env("SUPABASE_SERVICE_ROLE_KEY", "KEY")
    if not (sb and sk):
        sys.exit("AMBIENTE: sem SUPABASE_URL/SUPABASE_SERVICE_ROLE_KEY")
    tok = token_do_canal(canal, sb, sk)
    dados = urllib.parse.urlencode({
        "client_id": tok["client_id"], "client_secret": tok["client_secret"],
        "grant_type": "refresh_token", "refresh_token": tok["refresh_token"],
    }).encode()
    req = urllib.request.Request(tok["token_uri"], data=dados, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resposta = json.load(r)
        resposta["access_token"]
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace")[:300]
        sys.exit(
            f"TOKEN MORTO ({canal}): {e.code} {corpo}\n"
            f"O refresh token expirou ou foi revogado. Nada aqui se conserta "
            f"sozinho: o Pablo precisa reautorizar ESTE canal pelo link de "
            f"autorizacao e colar a URL do localhost. O render foi abortado de "
            f"proposito — renderizar sem rota de publicacao gasta 20 minutos "
            f"para produzir um pacote parado (aprendizado 304)."
        )
    # `scope` vem da resposta do proprio Google: e o que foi CONCEDIDO. Se o
    # campo faltar (algumas respostas de refresh o omitem), nao da para concluir
    # nada — e dizer "nao deu para conferir" e melhor que inventar aprovacao.
    bruto = resposta.get("scope")
    if not bruto:
        print(f"token de {canal}: vivo (a resposta do refresh nao trouxe "
              f"`scope`; os escopos efetivos ficam por conferir)")
        return 0

    concedidos = set(bruto.split())
    faltando = [d for e, d in ESCOPOS_NECESSARIOS.items() if e not in concedidos]
    if faltando:
        sys.exit(
            f"ESCOPO FALTANDO ({canal}): a concessao do Google nao permite "
            f"{', '.join(faltando)}.\n"
            f"Concedidos: {' '.join(sorted(concedidos)) or '(nenhum)'}\n"
            f"O token VIVE — o que falta e permissao, e reautorizar e a unica "
            f"saida. O Pablo precisa refazer a autorizacao DESTE canal marcando "
            f"todas as caixas do consentimento.\n"
            f"O render foi abortado de proposito: publicar um longo que nao "
            f"pode levar legenda e publicar mudo para a busca (aprendizado 93), "
            f"e publicacao nao se desfaz."
        )
    print(f"token de {canal}: vivo, com os {len(ESCOPOS_NECESSARIOS)} escopos "
          f"necessarios concedidos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
