#!/usr/bin/env python3
"""Gera os links de reautorizacao OAuth, um por canal.

Existe porque `maquina auth-youtube` precisa de terminal interativo e o Pablo
autoriza pelo navegador do celular. Aqui sai a URL pronta.

POR QUE OS LINKS SAO QUASE IGUAIS: os treze canais usam UM client OAuth
(medido em 2026-08-12: um unico client_id em todos os config.yt_token_<canal>).
Entao a URL nao seleciona canal — quem seleciona e voce, na tela de
consentimento. O que muda entre os links e so o `state`, que carrega o slug de
volta na URL de retorno para o token ir para a linha certa do banco. Sem ele,
treze codigos identicos voltam sem dizer de quem sao.

`prompt=consent` e obrigatorio: sem ele o Google devolve so um access_token
quando ja existe consentimento, e o refresh_token — que e o que a maquina
guarda — nao vem.

Uso:
    python3 scripts/links_reauth.py            # todos
    python3 scripts/links_reauth.py setiap-level labtreinamento
"""

import sys
import urllib.parse

# Nao e segredo: client_id vai na barra de enderecos por design. O
# client_secret, que e segredo, fica so em config.yt_token_<canal>.
CLIENT_ID = "777159180424-p853u21ksnlhgjd4s9d2f5bum9hllumo.apps.googleusercontent.com"

# Espelha ESCOPOS de src/maquina/stages/youtube.py. force-ssl e o que
# captions.insert exige; yt-analytics.readonly e o que falta para medir
# retencao/CTR/impressoes (aprendizados.id=144) — nenhum dos 13 tokens tem.
ESCOPOS = " ".join([
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
])

CANAIS = [
    "setiap-level", "labtreinamento", "kolejny-poziom", "seja-mais-magra",
    "sx-educacao", "next-level-money", "cocina-por-niveles", "agla-level",
    "nivel-do-jogo", "game-money-lab", "resep-naik-level", "seviye-seviye",
    "epomeno-epipedo",
]


def link(slug: str) -> str:
    q = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "redirect_uri": "http://localhost",
        "response_type": "code",
        "scope": ESCOPOS,
        "access_type": "offline",
        "prompt": "consent",
        "state": slug,
    }, quote_via=urllib.parse.quote)
    return "https://accounts.google.com/o/oauth2/v2/auth?" + q


if __name__ == "__main__":
    alvos = sys.argv[1:] or CANAIS
    for slug in alvos:
        print(f"\n### {slug}\n{link(slug)}")
    print("\nDepois de autorizar, o navegador vai para http://localhost e da erro "
          "de pagina — isso e esperado. Copie a URL INTEIRA da barra de enderecos: "
          "ela traz ?code=... e &state=<canal>.")
