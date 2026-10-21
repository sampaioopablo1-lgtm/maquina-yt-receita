#!/usr/bin/env python3
"""Diz se o runner consegue publicar SEM o Supabase — e nunca imprime segredo.

POR QUE ISTO EXISTE (11/10/2026). A maquina dependia de uma reconexao manual do
conector Supabase para alcancar `config.yt_token_<canal>`, e com o gateway em
402 nem o REST servia. O dono pediu para tirar essa dependencia.

O repo JA tem a rota sem banco, e ela estava escrita em `retomar.yml`: o segredo
`YT_OAUTH_JSON` guarda `{canal: {client_id, client_secret, refresh_token}}` e o
runner refresca o access token sozinho, direto no endpoint do Google. Nenhuma
chamada ao Supabase participa disso.

O que faltava era SABER se o segredo esta preenchido e se o refresh token ainda
vive — os refresh tokens morriam de sete em sete dias (303). Esta sonda responde
isso, e responde para cada canal da frota em separado, porque `YT_OAUTH_JSON` e
um mapa e pode ter um canal bom e outro morto.

O QUE ELA NUNCA FAZ, e isto e trava da rotina:
  * nao imprime refresh token, client_secret nem access token — nem truncado;
  * nao grava nada em arquivo;
  * nao publica, nao apaga, nao altera video.
Ela imprime: presenca, contagem de caracteres, e o resultado do refresh com o
ESCOPO concedido, que nao e segredo e e justamente o que decide se o longo sobe
com legenda (`youtube.force-ssl`) e se a retencao volta
(`yt-analytics.readonly`).
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

try:                                        # rodando como pacote
    from fabrica.oauth_mapa import desembrulha
except ImportError:                         # rodando o arquivo solto no runner
    from oauth_mapa import desembrulha

FROTA = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")
TOKEN_URI = "https://oauth2.googleapis.com/token"

# Os escopos que mudam o que a maquina consegue fazer. Nao e lista decorativa:
# force-ssl decide se o longo sobe com legenda (93) e yt-analytics decide se a
# retencao volta (689), que e a unica alavanca do tamanho do problema.
ESCOPOS_QUE_DECIDEM = (
    ("upload", "youtube.upload"),
    ("force-ssl", "youtube.force-ssl"),
    ("analytics", "yt-analytics.readonly"),
)

# Quem LE cada segredo de credencial. A sonda lia um so, e por isso ela nao
# podia ver a divergencia de 21/10 — ver `_relata_divergencia`.
LEITORES = {
    "YT_OAUTH_JSON": "o `retomar.yml`, que e quem PUBLICA nas rodadas",
    "YT_TOKEN_JSON": "o `publicar.py`/`confere_token.py` dentro do `frota.yml`",
}


def nota(msg: str) -> None:
    print(f"::notice::{msg}")


def aviso(msg: str) -> None:
    print(f"::warning::{msg}")


def presenca(nome: str) -> int:
    """Tamanho do segredo, ou 0. NUNCA o conteudo."""
    return len(os.environ.get(nome) or "")


def projeto_do_client_id(cid: str) -> str:
    """Numero do PROJETO do Google Cloud, extraido do `client_id`.

    POR QUE ISTO EXISTE (19/10/2026). Em 18/10 o zip v2.0 que o dono trouxe me
    fez achar um erro nosso de cota: o teto nao e "~40 videos/janela", e
    `10.000 / 1.600` = SEIS envios de video por dia **por projeto**. E aí abriu
    uma pergunta que decide o dobro do triplo: seis por CANAL (dezoito na frota)
    ou seis para os TRES juntos? Depende de a frota usar um projeto do Cloud ou
    tres, e isso ninguem sabia — o 667 diz que o par client_id/secret e da linha
    `yt_token_<canal>`, mas `tokens.py:205-206` mina token novo copiando o par
    de um MODELO, logo pode ter propagado o mesmo projeto para os tres.

    A resposta estava a vista e nao dependia do banco: o `client_id` de um
    cliente OAuth tem a forma `<numero do projeto>-<aleatorio>.apps.
    googleusercontent.com`, e o numero do projeto NAO e segredo — e o mesmo
    numero que aparece na barra do console do Cloud.

    **O QUE ESTA FUNCAO NAO FAZ, e e a trava desta sonda:** ela devolve SO os
    digitos iniciais. Nao devolve o client_id inteiro, nem a parte aleatoria,
    nem nada que se pareca com credencial. Entrada que nao tem a forma esperada
    devolve string vazia em vez de devolver o que sobrou — porque devolver "o
    resto" e como um client_id mal formado viraria vazamento.
    """
    cabeca = (cid or "").split("-", 1)[0]
    return cabeca if cabeca.isdigit() and len(cabeca) >= 6 else ""


def refresca(cfg: dict) -> tuple[bool, str]:
    """Troca refresh por access token. Devolve (ok, escopo ou erro).

    So o ESCOPO sai daqui. O access token fica nesta funcao e morre com ela.
    """
    corpo = json.dumps({
        "client_id": cfg["client_id"],
        "client_secret": cfg["client_secret"],
        "refresh_token": cfg["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(
        cfg.get("token_uri", TOKEN_URI), data=corpo,
        headers={"Content-Type": "application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        # O corpo do erro do Google traz `error`/`error_description`, que nao
        # sao segredo e sao o que distingue token revogado de cliente errado.
        try:
            det = json.loads(e.read().decode("utf-8", "replace"))
            cru = f"{det.get('error')}: {det.get('error_description')}"
        except ValueError:
            cru = "corpo ilegivel"
        return False, f"HTTP {e.code} — {cru}"
    except Exception as e:                                # noqa: BLE001
        return False, f"{type(e).__name__}"
    if "access_token" not in r:
        return False, "resposta 200 SEM access_token"
    return True, r.get("scope", "(sem campo scope)")


def escopos_de_um_token(cfg: dict) -> set | None:
    """Os escopos CONCEDIDOS de uma entrada de credencial, ou None se nao vive.

    So o conjunto de escopos sai daqui — o access token morre no `refresca`.
    """
    faltam = [k for k in ("client_id", "client_secret", "refresh_token")
              if not (cfg or {}).get(k)]
    if faltam:
        return None
    ok, detalhe = refresca(cfg)
    return set(detalhe.split()) if ok else None


def divergencias(quadro: dict) -> list:
    """Escopo que um blob tem e o outro nao, por canal.

    `quadro` e `{blob: {canal: set(escopos) | None}}`. Devolve tuplas
    `(canal, rotulo, blob_que_tem, blob_que_nao)`.

    POR QUE ISTO EXISTE (21/10/2026, e o achado e de UMA hora). O
    `confere_token` abortou o render de um short solto dizendo que faltava
    `youtube.force-ssl`, e esta sonda, na MESMA hora, respondeu
    `force-ssl=sim` nos tres canais. As duas estavam certas: elas leem
    segredos DIFERENTES. O `confere_token` cai no `YT_TOKEN_JSON` (os
    `YT_TOKEN_<CANAL>` estao ausentes) e o `YT_OAUTH_JSON` e o que o
    `retomar.yml` usa para publicar — e os dois divergem nos DOIS escopos que
    decidem, em sentidos OPOSTOS: um tem force-ssl e nao tem analytics, o outro
    o contrario.

    Os dois jobs que a mediram: **119070898648** (o `confere_token` dentro do
    render, lendo `YT_TOKEN_JSON`) e **119073920894** (esta sonda, lendo
    `YT_OAUTH_JSON`). E a metade que vale para a monetizacao e que o
    `yt-analytics.readonly` — reportado como PERDIDO desde o aprendizado
    **689** — existe num dos dois; escopo concedido nao e prova de que o dado
    vem, e a chamada a Analytics API ainda nao foi feita.

    Com um blob so, a leitura disponivel era "o dono reautorizou e perdeu o
    force-ssl", que e falsa. Comparar os dois era conta MINHA, feita a mao
    cruzando dois jobs — e o item 3 da §10 diz onde isso termina.
    """
    saida = []
    for canal in FROTA:
        for rotulo, escopo in ESCOPOS_QUE_DECIDEM:
            tem = [b for b, m in quadro.items()
                   if m.get(canal) and any(escopo in s for s in m[canal])]
            nao = [b for b, m in quadro.items()
                   if m.get(canal) is not None and b not in tem]
            if tem and nao:
                saida.append((canal, rotulo, sorted(tem), sorted(nao)))
    return saida


# MEDIDO em 21/10 (run 39560816227): o `YT_TOKEN_JSON` desta conta pertence ao
# canal `UCf4-ZFoZQWKJotZNdi4Yl7w` (Setiap Level), que NAO e da frota, e nao
# declara `canal` no proprio JSON.
CANAL_MEDIDO_DO_TOKEN_JSON = "UCf4-ZFoZQWKJotZNdi4Yl7w"


def divergencia_entre_blobs(por_canal: dict, do_token: set | None) -> list:
    """Compara o blob POR CANAL com o token UNICO, blob contra blob.

    RETRATACAO de 21/10, e e de uma coisa que eu relatei ao dono: a primeira
    versao punha os escopos do `YT_TOKEN_JSON` em `{canal: escopos}` para os
    TRES canais da frota e deixava a comparacao por canal — e eu reportei
    "o analytics existe nos tres canais". **Falso.** O `YT_TOKEN_JSON` e um
    token UNICO de UM canal (`publicar.py:139` o usa como reserva de qualquer
    slug), e esse canal foi MEDIDO como estando FORA da frota. Atribuir o escopo
    dele aos tres canais e a familia "atribuir o numero ao orgao errado": a
    conta fecha e a origem esta errada.

    Devolve `(rotulo, tem, nao)` com `tem`/`nao` em nomes de BLOB, nunca de
    canal — e `[]` quando o token unico nao foi lido, porque uma leitura so nao
    mede divergencia (17/10).
    """
    if not do_token:
        return []
    saida = []
    for rotulo, escopo in ESCOPOS_QUE_DECIDEM:
        no_token = any(escopo in s for s in do_token)
        # No blob por canal, o escopo vale quando TODO canal lido o tem; canal
        # sem leitura nao conta como ausencia.
        lidos = [s for s in por_canal.values() if s]
        no_oauth = bool(lidos) and all(any(escopo in x for x in s)
                                       for s in lidos)
        if no_token != no_oauth:
            tem = ["YT_TOKEN_JSON"] if no_token else ["YT_OAUTH_JSON"]
            nao = ["YT_OAUTH_JSON"] if no_token else ["YT_TOKEN_JSON"]
            saida.append((rotulo, tem, nao))
    return saida


def _relata_entre_blobs(por_canal: dict, do_token: set | None) -> None:
    if do_token is None:
        aviso("o YT_TOKEN_JSON nao foi lido, logo a divergencia entre os dois "
              "segredos NAO foi medida nesta passada — ausencia de leitura nao "
              "e ausencia de divergencia")
        return
    nota(f"o YT_TOKEN_JSON e um token UNICO de UM canal, e o canal dele foi "
         f"MEDIDO como {CANAL_MEDIDO_DO_TOKEN_JSON} (fora da frota) — logo os "
         f"escopos dele NAO se atribuem aos tres canais da frota")
    div = divergencia_entre_blobs(por_canal, do_token)
    if not div:
        nota("os dois segredos CONCORDAM nos escopos que decidem")
        return
    for rotulo, tem, nao in div:
        aviso(f"DIVERGENCIA entre os segredos: {rotulo} existe em "
              f"{', '.join(tem)} e NAO em {', '.join(nao)} — "
              f"{'; '.join(LEITORES.get(b, b) + ' le ' + b for b in tem + nao)}")


def _relata_divergencia(quadro: dict) -> None:
    div = divergencias(quadro)
    if len(quadro) < 2:
        aviso("so UM segredo de credencial foi lido, logo a divergencia entre "
              "eles NAO foi medida nesta passada — ausencia de leitura nao e "
              "ausencia de divergencia")
        return
    if not div:
        nota("os segredos de credencial lidos CONCORDAM nos escopos que "
             "decidem (upload, force-ssl, analytics)")
        return
    for canal, rotulo, tem, nao in div:
        aviso(f"DIVERGENCIA em {canal}: {rotulo} existe em {', '.join(tem)} e "
              f"NAO em {', '.join(nao)} — e quem le cada um e outro passo "
              f"({'; '.join(LEITORES.get(b, b) + ' le ' + b for b in tem + nao)})")


def main() -> int:
    oauth_n = presenca("YT_OAUTH_JSON")
    nota(f"YT_OAUTH_JSON: {'presente' if oauth_n else 'AUSENTE'} "
         f"({oauth_n} chars)")

    for canal in FROTA:
        nome = "YT_TOKEN_" + canal.upper().replace("-", "_")
        n = presenca(nome)
        nota(f"{nome}: {'presente' if n else 'AUSENTE'} ({n} chars)")

    if not oauth_n:
        aviso("sem YT_OAUTH_JSON o runner NAO publica sozinho — a rota sem "
              "banco depende deste segredo")
        return 0

    try:
        # `desembrulha` e nao `json.loads`: o copiar do SQL Editor embrulha o
        # valor numa coluna so, e em 11/10 isso fez a sonda ler "1 canal" com
        # os tres dentro (run 38175092152).
        mapa = desembrulha(os.environ["YT_OAUTH_JSON"])
    except ValueError:
        aviso("YT_OAUTH_JSON nao e JSON valido — formato esperado: "
              '{"<canal>": {"client_id", "client_secret", "refresh_token"}}')
        return 0

    nota(f"YT_OAUTH_JSON tem {len(mapa)} canal(is)")
    vivos = []
    projetos: dict[str, str] = {}
    escopos: dict[str, set] = {}
    for canal in FROTA:
        cfg = mapa.get(canal)
        if not cfg:
            aviso(f"{canal}: FORA do YT_OAUTH_JSON")
            continue
        faltam = [k for k in ("client_id", "client_secret", "refresh_token")
                  if not cfg.get(k)]
        if faltam:
            aviso(f"{canal}: entrada incompleta, falta {', '.join(faltam)}")
            continue
        ok, detalhe = refresca(cfg)
        if not ok:
            aviso(f"{canal}: refresh FALHOU — {detalhe}")
            continue
        vivos.append(canal)
        projetos[canal] = projeto_do_client_id(cfg["client_id"])
        tem = lambda s: "sim" if s in detalhe else "NAO"   # noqa: E731
        nota(f"{canal}: refresh OK — upload={tem('youtube.upload')}, "
             f"force-ssl={tem('youtube.force-ssl')}, "
             f"analytics={tem('yt-analytics.readonly')}")
        escopos[canal] = set(detalhe.split())

    _relata_cota(projetos)

    # O SEGUNDO blob, que e o que o `frota.yml` usa — a sonda era cega para ele
    # ate 21/10, e foi essa cegueira que produziu um diagnostico errado.
    quadro = {"YT_OAUTH_JSON": {c: escopos.get(c) for c in FROTA}}
    do_token = None
    bruto = os.environ.get("YT_TOKEN_JSON") or ""
    nota(f"YT_TOKEN_JSON: {'presente' if bruto else 'AUSENTE'} "
         f"({len(bruto)} chars)")
    if bruto:
        try:
            tok = desembrulha(bruto)
        except ValueError:
            aviso("YT_TOKEN_JSON nao e JSON valido")
            tok = None
        if isinstance(tok, dict) and tok.get("refresh_token"):
            # Ele e um token UNICO e serve de reserva para QUALQUER canal
            # (`publicar.py:139`), logo o canal que ele diz ser nao e segredo e
            # e exatamente o que decide se a reserva publica no canal certo.
            dono = tok.get("canal") or tok.get("slug") or "(nao declara canal)"
            esc = escopos_de_um_token(tok)
            if esc is None:
                aviso(f"YT_TOKEN_JSON: refresh FALHOU (declara {dono})")
            else:
                tem2 = lambda s: "sim" if any(s in x for x in esc) else "NAO"  # noqa: E731
                nota(f"YT_TOKEN_JSON (declara {dono}): refresh OK — "
                     f"upload={tem2('youtube.upload')}, "
                     f"force-ssl={tem2('youtube.force-ssl')}, "
                     f"analytics={tem2('yt-analytics.readonly')}")
                do_token = esc
    _relata_entre_blobs(quadro["YT_OAUTH_JSON"], do_token)

    if vivos:
        nota(f"PUBLICACAO SEM BANCO possivel em: {', '.join(vivos)}")
    else:
        aviso("nenhum canal da frota refresca — a rota sem banco esta morta "
              "e o destrave depende do dono")
    return 0


def _relata_cota(projetos: dict[str, str]) -> None:
    """Diz se o teto de envio e 6/dia POR CANAL ou 6/dia na FROTA.

    Nao inventa limiar: `videos.insert` custa 1.600 unidades e a cota padrao de
    um projeto e 10.000/dia, logo `10.000/1.600` = 6. O que esta funcao decide e
    o DENOMINADOR — quantos projetos existem —, e isso ela LE, nao supoe.
    """
    lidos = {c: p for c, p in projetos.items() if p}
    if not lidos:
        aviso("NUMERO DO PROJETO nao lido em nenhum canal — o teto de cota "
              "segue INDETERMINADO entre 6/dia na frota e 6/dia por canal")
        return
    distintos = sorted(set(lidos.values()))
    nota("projetos do Cloud por canal: "
         + ", ".join(f"{c}=projeto {p}" for c, p in sorted(lidos.items())))
    if len(distintos) == 1 and len(lidos) > 1:
        aviso(f"os {len(lidos)} canais lidos COMPARTILHAM o projeto "
              f"{distintos[0]} — logo o teto de envio e ~6 VIDEOS/DIA NA FROTA "
              "INTEIRA (10.000/1.600), e nao por canal. Os 7/dia/canal que o "
              "dono pede ficam 3,5x acima disso.")
    else:
        nota(f"{len(distintos)} projetos distintos em {len(lidos)} canais — "
             f"cada projeto tem cota propria, logo o teto e ~6 videos/dia POR "
             f"CANAL (~{6 * len(distintos)} na frota). Os 7/dia/canal seguem "
             "pouco acima do teto de UM projeto.")
    if len(lidos) < len(FROTA):
        aviso(f"so {len(lidos)} de {len(FROTA)} canais tiveram o projeto lido "
              "— o veredito acima vale para esses, nao para a frota")


if __name__ == "__main__":
    raise SystemExit(main())
