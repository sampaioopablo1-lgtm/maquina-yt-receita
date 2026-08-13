"""Onde o pacote mora em disco. Uma definicao so, sem stack de render.

Existe por um defeito medido em 15/08/2026 no sandbox Composio. O
`fabrica.dir_trabalho` ja sabia de tudo isto — inclusive que o default mora no
tmpfs — mas ele vive em `fabrica.py`, que abre com `import cairosvg, edge_tts`.
Quem nao pode pagar essa stack copiou a linha: o `vozes.py` copiou o
`os.environ.get(...)` inteiro, e o `publicar.py` copiou so a METADE, com
`/tmp/f/<pacote>` escrito a mao e sem ler a variavel.

E a metade que ele copiou e a que quebra em silencio. Renderizando com
FABRICA_WORKDIR apontado para disco real, o render termina certo em
/home/user/f/<pacote> e o publicar.py vai procurar em /tmp/f/<pacote>: ou nao
acha nada, ou — pior — acha o resto de uma tentativa anterior e publica o
video ERRADO, com o nome certo.

POR QUE O DEFAULT PRECISA SER MUDAVEL. No sandbox, /tmp e tmpfs: e RAM, nao
disco. Medido em 15/08/2026, `df` dava 493 MB de teto para /tmp num container
de 985 MB, e 355 MB ja estavam ocupados por renders antigos baixados para
auditoria. Sobraram 160 MB, e o ffmpeg do primeiro clipe do
resep-naik-level-003 — tres camadas, zoompan, loudnorm — morreu com SIGKILL:

    oom-kill:constraint=CONSTRAINT_MEMCG, task=ffmpeg, anon-rss:185748kB

SIGKILL nao diz "sem espaco" nem "sem memoria": diz 9. O traceback mostra a
linha de comando do ffmpeg inteira e parece defeito de filtro. O gasto de
disco de um pacote (86 clipes + mp3 + video final) passa de 300 MB, entao ele
nao cabe no tmpfs nem com o /tmp vazio — o default so funciona onde /tmp e
disco de verdade, como no runner do Actions.
"""

from __future__ import annotations

import os

# Sobrevive por compatibilidade: e onde o Actions renderiza, e la /tmp e disco.
RAIZ_PADRAO = "/tmp/f"


def raiz() -> str:
    return os.environ.get("FABRICA_WORKDIR", RAIZ_PADRAO)


def dir_trabalho(sp) -> str:
    """Diretorio de trabalho do PACOTE, nao do canal.

    O 'slug' da spec e o do canal — ele escolhe a trilha. Usar o mesmo slug como
    diretorio faz dois pacotes do mesmo canal dividirem a mesma pasta, e ai o
    RETOMA pula clipes do pacote ANTERIOR: sai um video costurando dois roteiros
    sem erro nenhum. Specs novas declaram "pacote"; as antigas seguem no slug.
    """
    return os.path.join(raiz(), sp.get("pacote") or sp["slug"])
