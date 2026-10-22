# -*- coding: utf-8 -*-
"""O DESPACHO DA RODADA TINHA DOIS PASSOS E A ROTA MORAVA NA MINHA MEMORIA.

Medido em 22/10 as 23:5x, e o erro aconteceu nesta rodada. A rota de
producao sao DUAS chamadas: o `frota.yml` RENDERIZA e o `retomar.yml`
PUBLICA do artefato daquele run. Eu as digitava a cada rodada — o JSON do
`pacotes`, o `run_id`, o `estado_b64` — e com elas digitava tambem a unica
coisa que nao e obvia: o `publicar` do `frota.yml` tem de ir **FALSE**.

NESTA RODADA EU DIGITEI `true` E ISSO MATOU O RENDER. Medido na API, nos
30 dispatches anteriores do `frota.yml`:

    passo "Conferir token do canal" SKIPPED    28 de 28 que rodaram
    passo RODOU                                 1 — esta rodada
    e nela ele REPROVOU, com o render inteiro pulado

Logo a rota em uso e `publicar=false` em 28 de 28, e **o input do
`frota.yml` tem DEFAULT `true`**: a rota da rodada e a NAO-padrao, e ela
vivia na minha memoria.

E O PORTAO QUE ME REPROVOU LE O SEGREDO QUE A PUBLICACAO NAO USA. A
`sonda-oauth` do run 39874361957 mediu a divergencia entre os dois
segredos, e ela e por ESCOPO:

    force-ssl   existe em YT_OAUTH_JSON   e NAO em YT_TOKEN_JSON
    analytics   existe em YT_TOKEN_JSON   e NAO em YT_OAUTH_JSON

O `confere_token.py` dentro do `frota.yml` le **YT_TOKEN_JSON**; quem
PUBLICA nas rodadas — o `retomar.yml` — le **YT_OAUTH_JSON**, e a sonda
diz que ali o refresh dos tres canais esta vivo com `upload` e
`force-ssl`. Logo o portao reprova, com o segredo A, um canal que a rota
de publicacao em uso publica com o segredo B.

**ISTO NAO MUDA QUAL SEGREDO O PORTAO LE, de proposito:** dentro do
`frota.yml` o portao e o passo de publicar leem o MESMO segredo, logo
ali ele nao mente — o comentario do proprio passo cobra isso em letra
("portao mais severo que o passo que ele guarda e portao que mente").
Trocar o segredo do portao faria ele discordar do passo que ele guarda, e
reconciliar os dois segredos e colagem do DONO (a pendencia 3 da rotina).
O que este modulo faz e nao deixar a rodada cair nesse ramo por
digitacao.

O QUE ELE NAO FAZ: nao dispara nada. Ele monta e VALIDA os dois payloads
e imprime os dois comandos prontos — a rede fica fora de proposito, para
ele poder ser chamado de graca antes de cada despacho.

E as duas formas que ja mataram run vao cobradas aqui:

  * `pacotes` e lista de OBJETOS, nao de strings — o run 38476203962
    morreu com `matrix.pacote` vazio e ZERO anotacao util porque eu mandei
    `["labtreinamento-s034"]` (738);
  * o `estado_b64` sai do DONO (`estado_ponte.b64`), nunca montado aqui —
    monta-lo a mao matou tres runs (718, 729, e o `2>&1` de 13/10 as 15:1x,
    que colou a nota legivel no fim do payload).

Nao e portao e o codigo de saida e sempre ZERO.
"""
from __future__ import annotations

import json
import os
import sys

import canal
import estado_ponte

SPECS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "specs")

REPO = "sampaioopablo1-lgtm/maquina-yt-receita"
BRANCH = "claude/youtube-publication-next-steps-v7o4el"

# O valor da rota MEDIDA, com o motivo no docstring. Ele e False e o input
# do `frota.yml` e True: e por isso que ele mora aqui e nao na memoria.
PUBLICAR_NO_RENDER = False

# A medida que autoriza a frase, para ela nao envelhecer calada (753).
DISPATCHES_MEDIDOS = 28       # com o passo do token SKIPPED
DISPATCHES_COM_O_PORTAO = 1   # esta rodada, e ele reprovou


def _spec(pacote: str, dir_specs: str = SPECS) -> dict:
    """A spec NO DISCO, e ela LEVANTA quando nao esta la.

    O runner faz `checkout` do repo: spec que nao foi comitada nao existe
    para ele, e o render sai com `No files were found` — a mesma anotacao
    que o `KeyError: 'longo'` de 18/10 as 08:1x produziu, logo ela nao
    distingue as duas causas. Recusar aqui custa nada.
    """
    caminho = os.path.join(dir_specs, "%s.json" % pacote)
    if not os.path.exists(caminho):
        raise ValueError(
            "a spec %r NAO esta no disco (%s): o runner faz checkout do repo, "
            "logo despachar antes de comitar renderiza NADA e a anotacao que "
            "volta e `No files were found`, que nao distingue a causa"
            % (pacote, caminho))
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def payload_do_render(pacote: str, dir_specs: str = SPECS,
                      publicar: bool | None = None) -> dict:
    """Os inputs do `frota.yml`, com `pacotes` como lista de OBJETOS.

    O canal e o idioma saem da SPEC — o canal pelo dono (`canal.da_spec`),
    porque derivar canal por conta propria foi o defeito de 19/10 as 05:2x
    que parou a mira de conferir por seis pecas.
    """
    sp = _spec(pacote, dir_specs)
    if publicar is None:
        publicar = PUBLICAR_NO_RENDER
    if publicar:
        raise ValueError(
            "publicar=True no `frota.yml` liga o passo `Conferir token do "
            "canal`, que le YT_TOKEN_JSON — e a sonda mediu que `force-ssl` "
            "existe em YT_OAUTH_JSON e NAO nele. Em %d de %d dispatches a "
            "rota foi publicar=false, e na unica em que foi true o portao "
            "REPROVOU e o render inteiro foi pulado. Quem publica e o "
            "`retomar.yml`." % (DISPATCHES_MEDIDOS, DISPATCHES_MEDIDOS))
    um = {"canal": canal.da_spec(sp), "pacote": pacote,
          "idioma": sp["idioma"]}
    return {"pacotes": json.dumps([um], ensure_ascii=False),
            "publicar": "true" if publicar else "false"}


def payload_do_retomar(pacote: str, run_id, dir_specs: str = SPECS,
                       corpus: str | None = None) -> dict:
    """Os inputs do `retomar.yml`, com o `estado_b64` vindo do DONO.

    `access_token` fica VAZIO de proposito: o input diz, em letra, que
    vazio faz o runner refrescar sozinho pelo `YT_OAUTH_JSON`, "que e a
    rota segura" — e a trava proibe mandar token OAuth por input de
    workflow.
    """
    sp = _spec(pacote, dir_specs)
    if not str(run_id or "").strip():
        raise ValueError(
            "o `retomar.yml` publica do ARTEFATO de um run de render: sem "
            "`run_id` ele nao tem de onde baixar o mp4")
    b = (estado_ponte.b64(corpus) if corpus else estado_ponte.b64())
    return {"pacote": pacote, "canal": canal.da_spec(sp),
            "idioma": sp["idioma"], "run_id": str(run_id),
            "estado_b64": b}


def _gh(workflow: str, inputs: dict) -> str:
    partes = ["gh api -X POST",
              "repos/%s/actions/workflows/%s/dispatches" % (REPO, workflow),
              "-f ref=%s" % BRANCH]
    for k, v in inputs.items():
        if k == "estado_b64":
            partes.append("-f \"inputs[%s]=$(cat <arquivo>)\"" % k)
        else:
            partes.append("-f 'inputs[%s]=%s'" % (k, v))
    return " \\\n  ".join(partes)


def comandos(pacote: str, run_id=None, dir_specs: str = SPECS) -> list:
    """Os dois comandos, na ORDEM da rota: render primeiro, publicar depois."""
    fora = [_gh("frota.yml", payload_do_render(pacote, dir_specs))]
    if run_id:
        fora.append(_gh("retomar.yml",
                        payload_do_retomar(pacote, run_id, dir_specs)))
    return fora


def _linha_da_rota() -> str:
    """UM dono da frase da rota, e ela sai nos DOIS ramos do relato."""
    return ("ROTA MEDIDA: `frota.yml` com publicar=**false** (so render) e "
            "depois `retomar.yml` com o `run_id` daquele render. Em %d de %d "
            "dispatches o passo do token saiu SKIPPED; na unica em que ele "
            "rodou (esta rodada) ele REPROVOU, e o render foi pulado. O input "
            "do `frota.yml` tem DEFAULT true, logo a rota da rodada e a "
            "NAO-padrao." % (DISPATCHES_MEDIDOS, DISPATCHES_MEDIDOS))


def relato(pacote: str, run_id=None, dir_specs: str = SPECS) -> str:
    linhas = ["DESPACHO DA RODADA para %s:" % pacote, "  " + _linha_da_rota()]
    try:
        cs = comandos(pacote, run_id, dir_specs)
    except ValueError as e:
        linhas.append("  >> RECUSADO: %s" % e)
        return "\n".join(linhas)
    linhas.append("")
    linhas.append("  1) RENDER (sem publicar):")
    linhas.append("     " + cs[0].replace("\n", "\n     "))
    if len(cs) > 1:
        linhas.append("")
        linhas.append("  2) PUBLICAR (do artefato do render):")
        linhas.append("     " + cs[1].replace("\n", "\n     "))
        linhas.append("     o `estado_b64` sai de `estado_ponte.b64()`, que e "
                      "o dono — grave-o num arquivo e passe com $(cat), "
                      "porque ele tem ~44 mil caracteres.")
    else:
        linhas.append("")
        linhas.append("  2) PUBLICAR: passe o `run_id` do render para este "
                      "modulo montar o segundo comando.")
    linhas.append("")
    linhas.append("  e o portao do `frota.yml` le YT_TOKEN_JSON enquanto o "
                  "`retomar.yml` le YT_OAUTH_JSON — a sonda mediu que "
                  "`force-ssl` existe neste e NAO naquele. Reconciliar os dois "
                  "segredos e colagem do DONO (pendencia 3); este modulo "
                  "apenas nao deixa a rodada cair nesse ramo por digitacao.")
    linhas.append("  >> isto NAO dispara nada e nao reprova: codigo de saida "
                  "sempre zero.")
    return "\n".join(linhas)


def main(argv=None) -> int:
    a = list(sys.argv[1:] if argv is None else argv)
    if not a:
        print("uso: python3 fabrica/despacho_da_rodada.py <pacote> [run_id]")
        return 0
    print(relato(a[0], a[1] if len(a) > 1 else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
