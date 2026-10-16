"""A pauta tem de saber ONDE O CANAL ESTA HOJE, e a minha nao sabia.

Pedido do dono em 16/10, palavras dele: *"Estas producoes estao muito distantes
do ultimo video produzido e publicado no canal labtreinamento"*.

MEDIDO antes de concordar, porque ele podia estar falando de forma e nao de
assunto. Das dez ultimas pecas daquele canal, o RANK da origem (1 = o longo mais
novo do canal) foi: 14, 13, 12, 7, 3, 2, 11, 1, 1, **14**. As duas anteriores a
ultima sairam do longo mais NOVO (`FtCtIJPsc_Q`, PROCV ou PROCX) e a seguinte
voltou catorze posicoes, para uma planilha de risco psicossocial.

E A CAUSA E A MINHA REGRA DE PAUTA, nao descuido de uma peca: o
`concentracao.py` manda "pegue a origem de MENOR contagem com capitulos
intocados", e esse criterio **nao carrega nenhuma nocao de tempo**. Eu conferi a
hipotese obvia — que espalhar uso puxaria sistematicamente para o passado — e
ela NAO se sustenta: Spearman(usos, rank) = -0,21 com uso quase plano (4 em doze
das catorze origens). Logo o criterio nao puxa para tras *em media*; ele e
simplesmente CEGO, e com uso empatado o desempate caiu em qualquer lugar.

O QUE ESTE MODULO NAO FAZ, e e deliberado: ele nao escolhe sozinho e nao inventa
peso entre "pouco usada" e "recente". Peso sem procedencia e critério inventado
(§10). Ele IMPRIME as duas coordenadas juntas, para que a escolha pare de ser
cega, e RECUSA recomendar quando a ordem que recebeu nao alcanca o topo do canal.

E A RECUSA E O CORACAO DISTO, pelo seguinte: a unica fonte de ordem que vive no
repo e o retrato `fabrica/ponte/videos.json`, de 06/10 — e ele **nao conhece os
longos publicados depois**, que sao exatamente os mais novos. Usar o retrato
sozinho responderia a pergunta "qual e o mais novo" com um numero velho, que e o
erro retratado em 12/10 (retrato tratado como estoque). Entao a ordem VIVA entra
por argumento, lida da playlist de uploads, e sem ela o relato diz o que falta
em vez de chutar.
"""
from __future__ import annotations

import json
import os

RAIZ = os.path.dirname(os.path.abspath(__file__))


def ordem_do_retrato(canal: str, caminho: str = None) -> list[str]:
    """Ordem do MAIS NOVO para o mais antigo, pelo retrato — e so como PISO.

    O retrato nao tem os longos publicados depois de 06/10, logo esta ordem
    nunca comeca no topo real do canal. Serve para completar o rabo da lista,
    nunca para responder "qual e o ultimo video".
    """
    alvo = caminho or os.path.join(RAIZ, "ponte", "videos.json")
    try:
        with open(alvo, encoding="utf-8") as fh:
            linhas = json.load(fh)
    except (OSError, ValueError):
        return []
    longos = [
        r for r in linhas
        if r.get("formato") == "longo" and r.get("youtube_id")
        and r.get("publicado_em") and (canal is None or r.get("canal") == canal)
    ]
    longos.sort(key=lambda r: r["publicado_em"], reverse=True)
    return [r["youtube_id"] for r in longos]


def rank(origem: str, ordem: list[str]) -> int | None:
    """Posicao na ordem, 1 = mais novo. None quando a ordem nao a conhece."""
    try:
        return ordem.index(origem) + 1
    except ValueError:
        return None


def distancia_do_topo(origem: str, ordem: list[str]) -> int | None:
    """Quantas publicacoes separam esta origem do ultimo video do canal."""
    r = rank(origem, ordem)
    return None if r is None else r - 1


def _cobre_o_topo(ordem: list[str], topo_vivo: str | None) -> bool:
    return bool(ordem) and (topo_vivo is None or ordem[0] == topo_vivo)


def analise(usos: dict[str, int], ordem: list[str],
            topo_vivo: str = None) -> dict:
    """As duas coordenadas de cada origem, e o que a escolha cega ignorou.

    `usos` vem do `concentracao.contagem`. `ordem` e a lista VIVA de uploads.
    `topo_vivo` e o id do ultimo video do canal; quando informado e a ordem nao
    comeca nele, a analise se declara INCOMPLETA em vez de ordenar.
    """
    if not usos:
        return {"ok": False, "motivo": "nenhum short com origem declarada"}
    if not _cobre_o_topo(ordem, topo_vivo):
        return {
            "ok": False,
            "motivo": (
                "a ordem recebida nao comeca no ultimo video do canal: ela nao"
                " responde 'de onde o canal esta falando agora'. Leia a"
                " playlist de uploads VIVA; o retrato de 06/10 e piso e nao"
                " conhece os longos publicados depois."
            ),
        }
    linhas = []
    for o, n in usos.items():
        linhas.append({"origem": o, "usos": n, "rank": rank(o, ordem),
                       "distancia": distancia_do_topo(o, ordem)})
    conhecidas = [l for l in linhas if l["rank"] is not None]
    menos_usada = min(linhas, key=lambda l: (l["usos"], l["origem"]))
    # A recomendacao e o MENOR uso ENTRE as mais recentes, e "recente" aqui e
    # declarado: a metade de cima da ordem que o canal conhece. Nao e peso
    # entre as duas coordenadas — e um corte, e ele vai escrito.
    corte = max(1, len(conhecidas) // 2)
    recentes = [l for l in conhecidas if l["rank"] <= corte]
    sugerida = min(recentes, key=lambda l: (l["usos"], l["rank"])) if recentes else None
    return {
        "ok": True,
        "linhas": sorted(linhas, key=lambda l: (l["rank"] is None, l["rank"] or 0)),
        "menos_usada": menos_usada,
        "sugerida": sugerida,
        "corte_de_recente": corte,
        "cega_custaria": (
            None if not sugerida or menos_usada["rank"] is None
            else menos_usada["rank"] - sugerida["rank"]
        ),
    }


def relato(usos: dict[str, int], ordem: list[str], topo_vivo: str = None) -> str:
    a = analise(usos, ordem, topo_vivo)
    if not a["ok"]:
        return f"RECENCIA: nao ordena — {a['motivo']}"
    out = [f"RECENCIA: {len(a['linhas'])} origens, 1 = o longo MAIS NOVO do canal."]
    for l in a["linhas"]:
        r = l["rank"] if l["rank"] is not None else "fora da ordem"
        out.append(f"  {l['origem']}  usos={l['usos']}  rank={r}")
    mu = a["menos_usada"]
    out.append(f"  menos usada: {mu['origem']} (usos={mu['usos']}, rank={mu['rank']})")
    if a["sugerida"]:
        s = a["sugerida"]
        out.append(
            f"  menor uso ENTRE as recentes (rank <= {a['corte_de_recente']}):"
            f" {s['origem']} (usos={s['usos']}, rank={s['rank']})"
        )
        if a["cega_custaria"] and a["cega_custaria"] > 0:
            out.append(
                f"  a escolha CEGA pelo uso iria {a['cega_custaria']} posicoes"
                " mais para o passado — foi isso que o dono apontou em 16/10."
            )
    out.append(
        "  (isto CONTA e nao reprova: o peso entre 'pouco usada' e 'recente'"
        " nao esta medido, e peso sem procedencia e critério inventado.)"
    )
    return "\n".join(out)


# ---------------------------------------------------------------------------
# A ORDEM VIVA, quando a API nao esta disponivel — medido em 16/10 as 12:2x
# ---------------------------------------------------------------------------
#
# ESTE MODULO EXIGIA A ORDEM VIVA POR ARGUMENTO E NAO DIZIA DE ONDE TIRA-LA.
# Eu o escrevi de manha com a recusa certa — "sem a ordem viva o relato diz o
# que falta" — e deixei a obtencao de fora, logo a regra dependia de eu lembrar
# de uma chamada de API que nesta sessao nao existe (o `execute_sql` esta negado
# pela quinta rodada, logo nao ha `pg_net` nem token).
#
# E A ROTA OBVIA FECHOU NA MESMA RODADA, com a assinatura que o `CLAUDE.md`
# nomeia: `youtube.com/channel/<id>/videos` devolveu **HTTP 200 com 1.196.398
# bytes e ZERO `videoRenderer`**, com cinco marcadores `CONSENT` e um `captcha`.
# Quem contasse o codigo HTTP leria "funcionou". **Conte o CAMPO.**
#
# A rota que respondeu foi o `yt-dlp` na playlist de uploads — o id do canal com
# `UC` trocado por `UU` — e ela devolve a ordem VIVA com duracao:
#
#     yt-dlp --flat-playlist --print "%(id)s|%(duration)s|%(title).70s" \
#            -I 1:120 "https://www.youtube.com/playlist?list=UU<resto do id>"
#
# Rodou no sandbox do Composio, 84 itens no `kolejny-poziom`. **Nao roda neste
# container** (o proxy nega o youtube.com), entao o que vive aqui e o PARSER,
# que e a parte testavel — a chamada fica no sandbox, e a saida entra por aqui.

LIMITE_DE_SHORT_S = 180  # acima disto o YouTube deixa de tratar como Short


def playlist_de_uploads(canal_id: str) -> str:
    """O id da playlist de uploads de um canal: `UC...` -> `UU...`."""
    if not canal_id.startswith("UC"):
        raise ValueError(f"id de canal comeca com UC, nao {canal_id[:4]!r}")
    return "UU" + canal_id[2:]


def ordem_viva(saida_do_ytdlp: str) -> list[str]:
    """A ordem VIVA de uploads, do mais novo para o mais antigo.

    Recebe a saida de `--print "%(id)s|%(duration)s|%(title)s"`. Linha malformada
    e IGNORADA em silencio de proposito: o `yt-dlp` mistura aviso em stdout em
    algumas versoes, e abortar por causa de um aviso perderia a ordem inteira.
    O que NAO se ignora e saida vazia — ela levanta, porque ordem vazia faria o
    `_cobre_o_topo` recusar com a mensagem errada (diria "a ordem nao alcanca o
    topo" quando o problema e que nao houve leitura nenhuma).
    """
    ids = []
    for linha in saida_do_ytdlp.splitlines():
        campos = linha.strip().split("|")
        if len(campos) < 2 or len(campos[0]) != 11:
            continue
        if campos[0] not in ids:
            ids.append(campos[0])
    if not ids:
        raise ValueError(
            "nenhum id na saida do yt-dlp — isto e AUSENCIA DE LEITURA, nao "
            "canal vazio; sonde a rota antes de concluir qualquer coisa"
        )
    return ids


def longos_na_ordem(saida_do_ytdlp: str,
                    limite_s: int = LIMITE_DE_SHORT_S) -> list[tuple[int, str]]:
    """Os LONGOS, com o rank entre TODOS os uploads — que e o rank que importa.

    O rank conta shorts tambem, de proposito: a pergunta do dono e sobre
    distancia do ULTIMO VIDEO PUBLICADO, e o canal publica as duas coisas.
    """
    fora = []
    n = 0
    for linha in saida_do_ytdlp.splitlines():
        campos = linha.strip().split("|")
        if len(campos) < 2 or len(campos[0]) != 11:
            continue
        n += 1
        try:
            dur = float(campos[1])
        except ValueError:
            continue  # duracao ausente (live, privado) nao e longo conhecido
        if dur > limite_s:
            fora.append((n, campos[0]))
    return fora


def topo_de_pauta(saida_do_ytdlp: str) -> str | None:
    """O longo MAIS NOVO — o que a regra de recencia manda servir primeiro.

    `None` quando nao ha longo nenhum na janela lida, e isso NAO e erro: pode
    ser canal que so publicou shorts ultimamente, e o relato tem de dizer isso
    em vez de devolver um short como se fosse origem.
    """
    longos = longos_na_ordem(saida_do_ytdlp)
    return longos[0][1] if longos else None
