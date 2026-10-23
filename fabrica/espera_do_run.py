# -*- coding: utf-8 -*-
"""O LACO DE ESPERA do run nao tinha dono — e ele falhou TRES vezes por INVOCACAO.

O `anotacoes_do_run.terminou` da o veredito de que um run acabou, e desde
23/10 as 00:1x ele devolve `None` (INDETERMINADO) quando o run ainda esta
aberto com zero pendente, porque a lista de jobs ainda esta sendo POVOADA.
O que NAO tinha dono era o LACO que pergunta a ele, e eu o redigitava a cada
rodada na linha de comando. As tres falhas estao medidas:

  20/10 as 01:4x  `until ! pgrep -f "pytest tests"` — a propria linha de
                  comando casava o padrao, logo o laco nunca saia. O conserto
                  entrou no MODULO (`processo_vivo.sou_eu`) e o laco continuou
                  a ser digitado.
  20/10           a linha documentada no `CLAUDE.md` saiu SEM o `!`, e com
                  saida 0 = vivo o `until` para quando o comando ACERTA: ela
                  esperava o processo COMECAR. "Conserto no modulo nao protege
                  contra a invocacao" — e aqui a invocacao errada estava
                  escrita por mim, no documento que a rodada seguinte copia.
  23/10 as 00:07  `until ... | grep -q '0 pendente'` saiu com o job da matriz
                  ainda por criar, porque naquele instante a contagem de
                  pendentes ERA zero. E na MESMA rodada eu escrevi o `until`
                  sem `sleep`, deixando dois lacos OCUPADOS girando.

A terceira e a que este modulo fecha de vez, e ela viola uma regra escrita
deste repo: **codigo de saida, contagem e veredito saem do ESTADO, nunca do
texto que o modulo imprime** (19/10 as 17:2x, quando o `main` do `mira` decidia
por um `grep` na propria prosa). Um laco que faz `grep` na saida do relato e
exatamente esse defeito, uma camada acima — e foi o que eu digitei em 00:07 e
outra vez em 01:1x de 23/10.

O que ele garante, e cada ponto e uma das falhas acima:
  * o veredito sai de `terminou(...)["todos_terminaram"] is True`, e o relato
    NAO entra na decisao (ha teste por AST);
  * INDETERMINADO **nao** encerra a espera — e o caso do 00:07;
  * existe TETO e ele e respeitado: run que nunca termina devolve
    `desistiu: True` e codigo de saida 1, em vez de girar para sempre;
  * ele DORME entre as consultas, e o intervalo e maior que zero.

E O TETO NAO DEPENDE DO RELOGIO SOZINHO, e isso saiu de uma contraproba desta
mesma rodada: retirada a dormida, o laco nao REPROVOU o teste — ele **girou
para sempre**, porque com o relogio injetado quem fazia o tempo andar era a
propria dormida. Logo um teto medido so em segundos e refem da dormida que ele
deveria tornar desnecessaria. Agora ele conta tambem as CONSULTAS, derivadas do
par (teto, intervalo), e o laco termina mesmo sem dormir.

O TETO e o INTERVALO sao REDACAO declarada e nao medida: `LIMITE_S` vem do
maior render observado nesta sessao com folga, e `INTERVALO_S` do custo de uma
consulta contra a granularidade de um job que leva minutos. Nenhum dos dois sai
de distribuicao nenhuma, logo nenhum deles e limiar com procedencia — quem
precisar de outro passa o argumento.
"""

import math
import sys
import time

import anotacoes_do_run as AR

# REDACAO declarada (ver docstring): nao sao medida.
LIMITE_S = 1800.0
INTERVALO_S = 25.0


def veredito(run, api=None) -> dict:
    """O veredito de UMA consulta, com os DOIS campos que o `terminou` pede.

    O status do RUN vem de uma segunda chamada de proposito: o payload dos
    jobs nao o traz, e sem ele o `todos_terminaram` sai True sobre uma lista
    ainda sendo povoada (23/10 as 00:1x).
    """
    if run is None or str(run).strip() == "":
        raise ValueError(
            "sem `run` nao ha o que esperar. Ausencia de id nao e run terminado — "
            "vazio de instrumento nao prova ausencia (17/10)."
        )
    chamar = api or AR._api
    jobs = chamar("repos/%s/actions/runs/%s/jobs" % (AR.REPO, run)) or {}
    cab = chamar("repos/%s/actions/runs/%s" % (AR.REPO, run)) or {}
    return AR.terminou(jobs, (cab or {}).get("status"))


def espera(run,
           limite_s: float = None,
           intervalo_s: float = None,
           api=None,
           dorme=None,
           agora=None) -> dict:
    """Pergunta ao `terminou` ate ele dizer SIM, ou ate o TETO.

    A decisao sai do ESTADO (`todos_terminaram is True`) e nunca do texto:
    `None` (INDETERMINADO) e `False` seguem esperando, porque nenhum dos dois
    e "terminou". Devolve o ultimo veredito com `desistiu`, `polls` e
    `esperou_s` ao lado — e NAO imprime nada, para quem chama poder decidir.
    """
    teto = LIMITE_S if limite_s is None else float(limite_s)
    passo = INTERVALO_S if intervalo_s is None else float(intervalo_s)
    if passo <= 0:
        raise ValueError(
            "intervalo tem de ser > 0: laco sem dormida e laco OCUPADO, e foi "
            "isso que eu escrevi em 23/10 as 00:07."
        )
    relogio = agora or time.monotonic
    pausa = dorme or time.sleep
    # o teto conta TEMPO e CONSULTAS: so o tempo o deixa refem da dormida (ver
    # docstring — a contraproba sem dormida girou para sempre em vez de falhar).
    teto_polls = int(math.ceil(teto / passo)) + 1

    t0 = relogio()
    polls = 0
    q = None
    while True:
        q = veredito(run, api=api)
        polls += 1
        if q.get("todos_terminaram") is True:
            desistiu = False
            break
        if (relogio() - t0) >= teto or polls >= teto_polls:
            desistiu = True
            break
        pausa(passo)

    saida = dict(q)
    saida["polls"] = polls
    saida["esperou_s"] = round(relogio() - t0, 1)
    saida["desistiu"] = desistiu
    saida["limite_s"] = teto
    saida["intervalo_s"] = passo
    saida["limite_polls"] = teto_polls
    return saida


def relato_da_espera(q: dict) -> str:
    """Uma linha com o veredito e, se desistiu, o teto que ele bateu."""
    rot = {True: "SIM", False: "NAO", None: "INDETERMINADO"}[q.get("todos_terminaram")]
    L = ["ESPERA DO RUN: TERMINOU: %s — %d consulta(s) em %.1f s" % (
        rot, q.get("polls") or 0, q.get("esperou_s") or 0.0)]
    if q.get("desistiu"):
        L.append("  >> DESISTIU no teto de %.0f s, e isto NAO e 'terminou': o run segue "
                 "aberto ou com job pendente. Codigo de saida 1." % (q.get("limite_s") or 0))
    L.append("  o veredito sai de `terminou`, que le os PASSOS — e o campo `conclusion` "
             "e o `status` do run ja mentiram nos DOIS sentidos (22/10 as 13:4x e 19:4x).")
    return "\n".join(L)


def main(argv: list = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    run = argv[0] if argv else None
    q = espera(run)
    print(relato_da_espera(q))
    # codigo de saida do ESTADO, nunca do texto (19/10 as 17:2x).
    return 0 if q.get("todos_terminaram") is True else 1


if __name__ == "__main__":
    sys.exit(main())
