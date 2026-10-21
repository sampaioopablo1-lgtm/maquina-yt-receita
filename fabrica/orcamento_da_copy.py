# -*- coding: utf-8 -*-
"""Os limites que a copy paga, com a FOLGA de cada um, ANTES de escrever.

**POR QUE EXISTE (20/10 as 21:3x).** Os portoes `copy` e `variedade` cobram
cinco limites da copy, e nenhum deles tinha quem dissesse **quanto ainda cabe**:
eles respondem *"esta dentro?"* depois de a copy existir. **E a assinatura e a
mesma do `mira.orcamento` de 19/10 as 14:2x** — o relato dizia se a peca ESTAVA
na mira e nunca quanto escrever para entrar.

**O CUSTO E MEDIDO EM PASSADAS, e sao SETE nesta sessao:** thumbnail com CINCO
palavras contra o limite de quatro no `kolejny-poziom-s071`, na primeira versao
do `labtreinamento-s089`, no `epomeno-epipedo-s075` e no `labtreinamento-s095`;
titulo com 106 caracteres contra 100 no `labtreinamento-s092`; e `## TAGS`
quebrado em varias linhas, que o portao le como *"sem tags"*, no
`epomeno-epipedo-s072` e no `labtreinamento-s092`. **Todas foram pegas pelo
`antes_do_render`** — logo nenhuma chegou ao ar, e isto nao e um buraco: e
friccao que se paga uma passada por vez, e o item 3 da §10 nomeia exatamente
isso.

**TODO LIMITE E LIDO DO DONO, por import e nunca copiado:** o das quatro
palavras da thumbnail e do `variedade.THUMB_MAX_PALAVRAS`, o das doze do gancho
do `variedade.GANCHO_MAX_PALAVRAS`, e os do titulo, da descricao e das tags do
`prontidao` (`MIN_PALAVRAS_DESCRICAO`, `MAX_DESCRICAO`, `RESERVA_LINK_SHORT`).
Copiar qualquer um aqui criaria o segundo dono, que e a assinatura que congelou
a legenda — e aqui ela seria pior que de costume, porque o numero copiado
pareceria orcamento e o portao cobraria outro.

**NAO E PORTAO e nao reprova nada**, pelo argumento do `mira.py`: quem reprova
sao os dois portoes, e este diz a FOLGA. Codigo de saida sempre zero.

**E a leitura da copy e DELEGADA ao `publicar.ler_copy`**, que e o dono da
classificacao de secoes — reimplementar a regex aqui faria o orcamento medir uma
copy que o portao le de outro jeito, e foi assim que o `## TAGS` em varias linhas
passou a sair como *"sem tags"* sem eu entender por que.
"""
import os

import prontidao as P
import variedade as V

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def limites() -> dict:
    """Os cinco limites, LIDOS dos donos."""
    return {
        "thumb_palavras": V.THUMB_MAX_PALAVRAS,
        "gancho_palavras": V.GANCHO_MAX_PALAVRAS,
        "titulo_chars": 100,            # do `_gate_copy`, que o cobra literal
        "descricao_min_palavras": P.MIN_PALAVRAS_DESCRICAO,
        "descricao_max_chars": P.MAX_DESCRICAO - P.RESERVA_LINK_SHORT,
    }


def _copy_lida(sp: dict):
    """A copy como o PORTAO a le, pelo dono da classificacao de secoes."""
    import publicar as PB

    bruto = sp.get("copy")
    if not isinstance(bruto, str) or len(bruto) < 200:
        return None
    falso = dict(sp)
    falso["copy"] = bruto.replace("{CAPITULOS}", "0:00 abertura").replace(
        "{TRILHA}", "Music: por Kevin MacLeod — CC BY 4.0")
    try:
        return PB.ler_copy(falso, os.path.join(RAIZ, "nao-existe"))
    except SystemExit:
        return None


def orcamento(sp: dict) -> dict | None:
    """Para cada limite: o valor de hoje, o limite, e a FOLGA que sobra."""
    lim = limites()
    cp = _copy_lida(sp)
    if cp is None:
        return None
    th = sp.get("thumb") or {}
    n_thumb = len((str(th.get("l1") or "") + " "
                   + str(th.get("l2") or "")).split())
    short = sp.get("short") or []
    prim = V.primeira_frase((short[0].get("nar") or "")) if short else ""
    n_gancho = len(prim.split())
    desc = cp.get("descricao") or ""
    itens = {
        "thumb_palavras": n_thumb,
        "gancho_palavras": n_gancho,
        "titulo_chars": len(cp.get("titulo") or ""),
        "descricao_max_chars": len(desc),
    }
    saida = {}
    for k, v in itens.items():
        saida[k] = {"valor": v, "limite": lim[k], "folga": lim[k] - v,
                    "sentido": "teto"}
    pal = len(desc.split())
    saida["descricao_min_palavras"] = {
        "valor": pal, "limite": lim["descricao_min_palavras"],
        "folga": pal - lim["descricao_min_palavras"], "sentido": "piso"}
    saida["tags"] = {"valor": len(cp.get("tags") or []), "limite": None,
                     "folga": None, "sentido": "presenca"}
    return saida


def relato(caminho=None, spec=None) -> str:
    """A MESMA convencao dos outros relatos: `(caminho, spec=None)`.

    Ela nascera com UM parametro cujo nome dizia aceitar os dois, e o
    despachante decide pela ARIDADE — logo a passada declarava "NAO aceita
    rascunho" sobre um modulo que aceitava (21/10, 23:2x).
    """
    if isinstance(caminho, dict):     # compatibilidade: a spec na 1a posicao
        caminho, spec = None, caminho
    sp_ou_caminho = spec if spec is not None else caminho
    import json

    sp = sp_ou_caminho
    if isinstance(sp, str):
        sp = json.load(open(sp, encoding="utf-8"))
    orc = orcamento(sp)
    if orc is None:
        return ("ORCAMENTO DA COPY: a copy nao e markdown seccionado — o portao"
                " `copy` aborta antes de medir limite nenhum.")
    L = [f"ORCAMENTO DA COPY de {sp.get('pacote', '?')}:"]
    for k in ("thumb_palavras", "gancho_palavras", "titulo_chars",
              "descricao_min_palavras", "descricao_max_chars"):
        d = orc[k]
        if d["sentido"] == "piso":
            L.append(f"  {k}: {d['valor']} (piso {d['limite']}), sobra"
                     f" {d['folga']}")
        else:
            L.append(f"  {k}: {d['valor']} de {d['limite']}, cabe mais"
                     f" {d['folga']}")
    t = orc["tags"]
    L.append(f"  tags: {t['valor']} lida(s) — ZERO aqui quer dizer que o"
             " `## TAGS` nao esta em UMA linha, e o portao le isso como 'sem"
             " tags' (aconteceu duas vezes nesta sessao).")
    # FRONTEIRA: o portao reprova ACIMA do teto (`> THUMB_MAX_PALAVRAS`) e
    # ABAIXO do piso (`< MIN_PALAVRAS_DESCRICAO`), logo folga ZERO ainda PASSA.
    # A primeira versao usava `<= 0` e acusava a peca desta rodada, que tem
    # exatamente quatro palavras na thumbnail e passa o portao: era o
    # instrumento inventando achado (725) na fronteira.
    apertados = [k for k, d in orc.items()
                 if d["folga"] is not None and d["folga"] < 0]
    if apertados:
        L.append("  >> JA ESTOURA: " + ", ".join(sorted(apertados))
                 + " — o portao vai reprovar, e isto so INFORMA.")
    rentes = [k for k, d in orc.items()
              if d["folga"] is not None and d["folga"] == 0]
    if rentes:
        L.append("  no LIMITE exato (passa, e nao sobra nada): "
                 + ", ".join(sorted(rentes)))
    L.append("  todo limite e LIDO do dono (`variedade`, `prontidao`), e a copy"
             " e lida pelo `publicar.ler_copy`: nenhum numero daqui.")
    return "\n".join(L)


if __name__ == "__main__":
    import sys

    print(relato(sys.argv[1]))
