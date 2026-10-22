#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""As guardas que o CONSTRUTOR da peca deve carregar, num lugar que sobrevive.

**Medido em 22/10 as 20:4x, na DECIMA vez que a thumbnail saiu com mais
palavras que o limite nesta sessao.** A peca se escreve num construtor que vive
FORA do repo — no diretorio de rascunho da sessao —, e as guardas dele eu
**redigito a cada rodada**: o `assert layout in SONDADOS` entrou depois do
cartao em branco de 19/10 as 18:18Z e eu o reescrevo de memoria, e a guarda da
thumbnail **nunca existiu**, porque nao havia onde ela morar.

**Logo o conjunto de guardas do construtor era a minha memoria**, e a evidencia
e a contagem: a thumbnail estourou o limite em **dez** rodadas desta sessao, e
em 18/10 as 08:1x um render inteiro morreu em `KeyError: 'longo'` porque a spec
de short solto saiu sem a chave. Nos dois casos o conserto existia uma camada
adiante — a passada de pre-render e o portao — e o custo era uma passada a mais
por rodada.

**E NAO E PORTAO, e o numero vem antes da decisao.** Varridas as **433** specs
com short do disco, **86** tem thumbnail acima do limite e **1** tem layout que
o retrato nao desenha (o `epomeno-epipedo-s069`, o cartao em branco de 19/10,
que esta publicado). Portao aqui reprovaria o acervo, que e o argumento pelo
qual o `mira.py` tambem nao e portao. **Isto LEVANTA porque so ve a peca que
esta sendo escrita AGORA** — nunca o acervo —, e levantar na mesa e mais barato
que reprovar no portao.

**TODO limite e LIDO do dono, nunca copiado:** o da thumbnail e do gancho saem
do `variedade`, o conjunto de layouts e SONDADO no render pelo
`layouts_do_short`, a paleta e comparada pelo `paleta_da_spec` e o canal sai do
`canal`. Copiar qualquer um deles aqui criaria o segundo dono — a assinatura que
congelou a legenda.

Uso, no construtor, antes de gravar:

    import guardas_do_construtor as GC
    GC.exige(sp)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import canal as CA            # noqa: E402  — DONO do canal da spec
import layouts_do_short as LS  # noqa: E402  — SONDA o render
import paleta_da_spec as PS   # noqa: E402  — DONO da comparacao de paleta
import temas_do_dono as TD   # noqa: E402  — DONO da paleta de cada canal
import variedade as V         # noqa: E402  — DONO dos limites de redacao


class GuardaDoConstrutor(AssertionError):
    """Levanta com o motivo e com o que fazer, nao so com o fato."""


def _palavras_da_thumb(spec: dict) -> list:
    th = spec.get("thumb") or {}
    return ("%s %s" % (th.get("l1", ""), th.get("l2", ""))).split()


def confere(spec: dict) -> dict:
    """Os vereditos, sem levantar — para o `relato` e para os testes."""
    out = {}

    cenas = spec.get("short") or []
    desenham = set(LS.desenham())
    fora = sorted({c.get("layout") for c in cenas
                   if c.get("layout") not in desenham})
    out["layouts"] = {
        "ok": not fora, "fora": fora, "desenham": sorted(desenham),
        "motivo": None if not fora else (
            "cena com layout %r: o retrato do SHORT nao o desenha, logo ela "
            "sai como CARTAO EM BRANCO — o retangulo do fundo e mais nada. "
            "Medido em 19/10 as 19:1x, numa peca publicada 40 minutos antes. "
            "O conjunto e SONDADO no render e vale %r" % (fora, sorted(desenham))),
    }

    pal = _palavras_da_thumb(spec)
    lim = V.THUMB_MAX_PALAVRAS
    out["thumb"] = {
        "ok": len(pal) <= lim, "palavras": len(pal), "limite": lim,
        "motivo": None if len(pal) <= lim else (
            "thumbnail com %d palavra(s) somando as duas linhas e o limite e "
            "%d, LIDO do `variedade`. Estourou em DEZ rodadas desta sessao, e "
            "em todas quem pegou foi a passada de pre-render ou o portao — "
            "depois de a peca estar escrita" % (len(pal), lim)),
    }

    pri = V.primeira_frase((cenas[0].get("nar") if cenas else "") or "")
    ng = len(pri.split())
    limg = V.GANCHO_MAX_PALAVRAS
    out["gancho"] = {
        "ok": ng <= limg, "palavras": ng, "limite": limg,
        "motivo": None if ng <= limg else (
            "gancho com %d palavra(s) e o limite e %d, LIDO do `variedade` — "
            "ele reprovou o `epomeno-epipedo-s070` em 19/10 as 21:1x"
            % (ng, limg)),
    }

    # AUSENCIA DE CHAVE NAO E VALOR VAZIO (18/10, 08:1x): o render faz
    # `spec["longo"]` e morreu num `KeyError` depois de os onze portoes
    # passarem, porque nenhum deles abre a spec pelo caminho do render.
    tem = "longo" in spec
    out["longo"] = {
        "ok": tem, "presente": tem,
        "motivo": None if tem else (
            "a chave `longo` esta AUSENTE. Em short solto o valor certo e a "
            "lista VAZIA, e ausencia de chave nao e valor vazio: o render faz "
            "`spec['longo']` e morreu em `KeyError` em 18/10 as 08:1x, com os "
            "onze portoes verdes e um run inteiro gasto"),
    }

    # O `identidade` compara o `pacote` com o NOME DO ARQUIVO, e o rascunho
    # ainda nao tem nome — logo a unica conferencia possivel aqui e interna.
    mesmo = spec.get("pacote") == spec.get("slug")
    out["pacote"] = {
        "ok": mesmo, "pacote": spec.get("pacote"), "slug": spec.get("slug"),
        "motivo": None if mesmo else (
            "`pacote` %r e `slug` %r divergem: o portao `identidade` compara o "
            "`pacote` com o nome do ARQUIVO, e o `canal.do_pacote` deriva o "
            "canal do pacote — divergir aqui cega os dois"
            % (spec.get("pacote"), spec.get("slug"))),
    }

    try:
        c = CA.da_spec(spec)
    except Exception as e:                      # canal desconhecido LEVANTA
        c, erro = None, e
    else:
        erro = None
    if c is None:
        out["paleta"] = {"ok": False, "motivo":
                         "o canal da spec nao resolve (%s), logo a paleta do "
                         "dono nao tem contra o que ser comparada" % erro}
    else:
        # O TERCEIRO ESTADO E NECESSARIO, e o teste me pegou sem ele: canal
        # PARADO nao tem tema atribuido no `temas_do_dono`, logo nao existe
        # paleta do dono contra a qual comparar — e dizer "ok" ali seria o
        # sentido PERMISSIVO, que e a classe da mira que parou de avisar por
        # seis pecas. A guarda passa (nao ha o que comparar) e DIZ que nao
        # conferiu, do jeito que o `porta1` recusa janela curta.
        try:
            TD.paleta_do_canal(c)
        except Exception as sem:
            out["paleta"] = {
                "ok": True, "canal": c, "sem_tema": True, "conflitos": {},
                "motivo": ("o canal %r nao tem tema atribuido no "
                           "`temas_do_dono` (%s), logo a paleta NAO foi "
                           "conferida — isto nao e compatibilidade, e ausencia "
                           "de comparador" % (c, sem)),
            }
            out["ok"] = all(v.get("ok") for k, v in out.items() if k != "ok")
            return out
        conf = PS.conflitos(spec)
        ruins = conf.get("conflitos") or {}
        out["paleta"] = {
            "ok": not ruins, "canal": c, "sem_tema": False, "conflitos": ruins,
            "motivo": None if not ruins else (
                "a paleta divergE da do dono em %d chave(s): %r. Ela sai de "
                "`temas_do_dono.paleta_do_canal`, NUNCA escrita a mao — e os "
                "dez portoes baratos passaram limpos com ela errada em 20/10 "
                "as 00:3x, porque o `identidade` confere trilha e faixa e NAO "
                "compara a paleta" % (len(ruins), sorted(ruins))),
        }

    out["ok"] = all(v.get("ok") for k, v in out.items() if k != "ok")
    return out


def exige(spec: dict) -> dict:
    """Levanta na PRIMEIRA guarda violada, com o motivo e o que fazer.

    Devolve a propria spec, para poder ser usado em linha no construtor.
    """
    q = confere(spec)
    for nome in ("pacote", "longo", "layouts", "thumb", "gancho", "paleta"):
        v = q.get(nome) or {}
        if not v.get("ok"):
            raise GuardaDoConstrutor(
                "guarda %r do construtor: %s" % (nome, v.get("motivo")))
    return spec


def relato(caminho=None, spec=None) -> str:
    """A MESMA convencao dos outros relatos: `(caminho, spec=None)` — e o
    despachante do `antes_do_render` decide pela ARIDADE, nao pelo nome do
    parametro (a licao de 20/10 as 11:3x)."""
    if isinstance(caminho, dict):
        caminho, spec = None, caminho
    if spec is None:
        import json
        spec = json.load(open(caminho, encoding="utf-8"))
    q = confere(spec)
    L = ["GUARDAS DO CONSTRUTOR de %s: %s"
         % (spec.get("pacote", "?"), "todas limpas" if q["ok"] else "VIOLADA")]
    for nome in ("pacote", "longo", "layouts", "thumb", "gancho", "paleta"):
        v = q.get(nome) or {}
        L.append("  %-8s %s%s" % (nome, "ok" if v.get("ok") else "VIOLADA",
                                  "" if v.get("ok") else " — " + str(v.get("motivo"))))
    L.append("  os limites sao LIDOS dos donos (`variedade`, "
             "`layouts_do_short`, `paleta_da_spec`, `canal`) — copiar qualquer "
             "um aqui criaria o segundo dono.")
    L.append("  e isto LEVANTA no construtor em vez de informar: ele so ve a "
             "peca que esta sendo escrita, nunca o acervo (86 das 433 specs "
             "com short tem thumbnail acima do limite).")
    return "\n".join(L)


if __name__ == "__main__":
    print(relato(sys.argv[1] if len(sys.argv) > 1 else None))
    sys.exit(0)   # SEMPRE zero: quem levanta e o `exige`, no construtor.
