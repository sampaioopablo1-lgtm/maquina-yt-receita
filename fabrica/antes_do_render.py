# -*- coding: utf-8 -*-
"""Eu rodava os MEUS instrumentos no rascunho e nao o PORTAO.

MEDIDO em 19/10 as 22:1x, depois de duas rodadas seguidas em que a peca precisou
de passada de conserto por um limite BARATO:

| rodada | o que reprovou | portao | custo medido |
|---|---|---|---|
| 21:1x (`epomeno-epipedo-s070`) | gancho com 13 palavras, limite 12 | `variedade` | **0,05 s** |
| 22:1x (`kolejny-poziom-s071`) | thumbnail com 5 palavras, limite 4 | `variedade` | **0,05 s** |

**Nas duas eu rodei `mira`, `acento` e (na segunda) `gancho` no rascunho — e NAO
rodei o portao.** Os instrumentos que eu escolhi rodar foram os que eu mesmo
havia escrito; o portao que pegaria as duas custa cinquenta milissegundos.

**E o argumento do custo NAO sustenta a minha escolha, e isso vai dito em vez de
me servir de desculpa.** Medido portao por portao sobre uma peca de verdade:

| | |
|---|---|
| os DEZ portoes baratos, somados | **0,65 s** |
| o portao `layout`, sozinho (ele RENDERIZA) | **8,0 s** |
| total do `prontidao` | 8,6 s |

Oito segundos e meio nunca foi barreira. **A causa e procedural: eu tratava o
`prontidao` como passo FINAL** e, antes dele, escolhia a dedo quais instrumentos
rodar. E a assinatura de "nao chamar quem ja sabe" — a quarta do `mira.py`, a do
contador de canal que eu reescrevi cinco vezes a mao — agora no meu PROCEDIMENTO
e nao num modulo.

**O que este modulo e: UMA chamada para o rascunho.** Ele roda os portoes baratos
(delegando ao `prontidao`, que e o dono deles) e os tres instrumentos de redacao
(`mira`, `acento`, `gancho`), e imprime tudo junto. **Nao e portao e nao reprova:
codigo de saida sempre zero** — quem reprova continua sendo o `prontidao`, e ele
ainda tem de rodar inteiro antes do render, porque o `layout` e o que pega cartao
em branco e tinta na borda.

**O conjunto CARO vai DECLARADO com a medida ao lado, e o teste o reconfere.**
Derivar por cronometragem em tempo de execucao seria frageis — maquina ocupada
mudaria o conjunto. Entao ele e declarado aqui e `tests/` TEMPORIZA os portoes e
reprova se um barato passar a ser caro ou o contrario: numero medido que ninguem
reconfere envelhece calado (753).
"""
import io
import json
import os
import sys
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(RAIZ, "fabrica") not in sys.path:
    sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

# Portoes que RENDERIZAM, medidos em 19/10 as 22:1x sobre o
# `kolejny-poziom-s071`: o `layout` levou 8,0 s contra 0,65 s dos outros dez
# somados. O teste deste arquivo recronometra e reprova se isto mudar.
PORTOES_CAROS = ("layout",)
SEGUNDOS_CAROS_MEDIDOS = 8.0
SEGUNDOS_BARATOS_MEDIDOS = 0.65

# Os instrumentos de REDACAO, cada um dono da sua conta. Eles nao reprovam.
# E O SEXTO ENTROU EM 21/10 AS 03:3x, pelo que QUASE passou nesta rodada: o
# primeiro rascunho da `labtreinamento-s097` usava
# `titulo-lista-item-barras-item-cta`, que JA EXISTE na frota, e eu so peguei
# porque listei as formas de seis cenas a mao antes de escrever. NADA antes do
# render perguntava isso — o portao `variedade` avisa a partir de SEIS iguais
# DENTRO de um canal, e forma que atravessa canal ele nao ve (33 das 34).
#
# E a pergunta e feita em TODA rodada recente: medido no disco, **35 das 252**
# copies de short solto AFIRMAM novidade de esqueleto e **43** citam a forma.
# O `esqueleto_entre_canais.relato` ja aceitava o caminho da spec e ja aplicava
# o `exceto` da propria peca — ele so nao era chamado. SETIMA vez da assinatura
# "nao chamar quem ja sabe".
INSTRUMENTOS = ("mira", "acento", "gancho", "paleta_da_spec",
                "orcamento_da_copy", "esqueleto_entre_canais",
                "copy_secoes", "contagem_declarada", "layouts_do_short",
                "numerais_falados")

# E EM 21/10 AS 05:3x A PERGUNTA VIROU VARREDURA, em vez de eu descobrir um
# instrumento ausente por rodada. Varridos os modulos da fabrica com um
# `relato` cujo PRIMEIRO argumento e spec ou caminho de spec, **CINCO** estavam
# fora da passada — e DOIS pertenciam:
#
#   `contagem_declarada` ... o detector de "a fonte declara CINCO e enumera
#                            SEIS" (13/10). Ele achou QUATRO conflitos reais no
#                            acervo e nunca rodou antes do render;
#   `layouts_do_short` ..... a SONDA do render (19/10, 19:1x), que pega cartao
#                            em branco SEM renderizar — isto e, um proxy barato
#                            do portao `layout`, que fica fora da passada
#                            justamente por renderizar.
#
# Os outros TRES ficam de fora, e o motivo de cada um vai ESCRITO: decisao
# silenciosa foi o que deixou os dois de cima fora por dias.
FORA_DA_PASSADA = {
    "som": "exige a FAIXA DE AUDIO de um mp4 renderizado, nao uma spec — ele "
           "proprio responde 'DEFEITO: nao tem faixa de audio' quando recebe "
           "uma. O som se le na anotacao do job, depois do render.",
    "pauta_local": "nao fala da PECA: ele responde sobre origem livre e ignora "
                   "o argumento. A pauta se escolhe ANTES de haver spec, pelo "
                   "`pauta_do_momento`.",
    "estilo_paint": "e um relato de CUSTO (credito de geracao de imagem) de um "
                    "estilo opcional que o dono trouxe em 16/10 e que a "
                    "producao nao usa. Rodar aqui informaria credito em toda "
                    "peca sem haver decisao a tomar.",
}


def portoes_baratos():
    """Os portoes que NAO renderizam, lidos do `prontidao` que e o dono deles."""
    import prontidao

    return [(n, f) for n, f in prontidao.PORTOES if n not in PORTOES_CAROS]


def _aplicaveis(nome, sp):
    import prontidao

    if nome in prontidao.PORTOES_SO_DO_LONGO and not sp.get("longo"):
        return False
    return True


def portoes(caminho: str) -> dict:
    """Roda os portoes BARATOS e devolve {portao: [problemas]}."""
    with open(caminho, encoding="utf-8") as f:
        sp = json.load(f)
    fora = {}
    for nome, fn in portoes_baratos():
        if not _aplicaveis(nome, sp):
            continue
        try:
            r = fn(caminho, sp)
        except Exception as e:  # ambiente, nao a spec
            r = [f"AMBIENTE, nao a spec: {e}"]
        # alguns portoes devolvem (problemas, avisos)
        if isinstance(r, tuple):
            r = list(r[0]) + list(r[1])
        fora[nome] = list(r or [])
    return fora


def _relato_do_instrumento(nome: str, caminho: str) -> str:
    """Chama o `relato` do instrumento, que e o dono da conta dele."""
    mod = __import__(nome)
    try:
        return mod.relato(caminho)
    except Exception as e:
        return f"{nome}: AMBIENTE, nao a spec: {e}"


def relato(caminho: str) -> str:
    linhas = []
    t0 = time.time()
    p = portoes(caminho)
    dt = time.time() - t0
    ruins = {k: v for k, v in p.items() if v}
    linhas.append(
        "PORTOES BARATOS (%d de %d, em %.2f s — o `layout` NAO entra porque "
        "renderiza):" % (len(p), len(p) + len(PORTOES_CAROS), dt)
    )
    if not ruins:
        linhas.append("  todos limpos.")
    for k, v in ruins.items():
        linhas.append("  %s: %d problema(s)" % (k, len(v)))
        for x in v:
            linhas.append("    - " + str(x)[:160])
    for nome in INSTRUMENTOS:
        linhas.append("")
        linhas.append(_relato_do_instrumento(nome, caminho))
    linhas.append("")
    linhas.append(
        ">> ISTO NAO REPROVA e NAO substitui o `prontidao`: o portao `layout` "
        "renderiza e e ele que pega cartao em branco e tinta na borda. Rode o "
        "`prontidao` inteiro antes do render."
    )
    return "\n".join(linhas)


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python3 fabrica/antes_do_render.py <spec.json>")
        return 0
    print(relato(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
